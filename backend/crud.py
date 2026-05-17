from collections import Counter
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from auth import create_access_token, hash_password, verify_password
from models import Order, OrderItem, Product, User
from payments import create_yookassa_payment
from serializers import serialize_product
from seed import seed_database
from schemas import AuthResponse, OrderItemRead, OrderRead, PaymentCreateResponse, UserCreate, UserRead


def ensure_seeded(db: Session) -> None:
    seed_database(db)


def get_products(db: Session, skip: int = 0, limit: int = 20) -> list:
    stmt = (
        select(Product)
        .where(Product.is_active.is_(True))
        .options(
            selectinload(Product.category),
            selectinload(Product.images),
            selectinload(Product.sizes),
        )
        .offset(skip)
        .limit(limit)
    )
    products = list(db.scalars(stmt).all())
    return [serialize_product(product) for product in products]


def get_product_by_slug(db: Session, slug: str):
    stmt = (
        select(Product)
        .where(Product.is_active.is_(True))
        .options(
            selectinload(Product.category),
            selectinload(Product.images),
            selectinload(Product.sizes),
        )
    )
    products = list(db.scalars(stmt).all())
    for product in products:
        serialized = serialize_product(product)
        if serialized.slug == slug:
            return serialized
    return None


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email.lower().strip())
    return db.scalar(stmt)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


def get_order_by_id(db: Session, order_id: int, user_id: int | None = None) -> Order | None:
    stmt = (
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
        )
    )
    if user_id is not None:
        stmt = stmt.where(Order.user_id == user_id)
    return db.scalar(stmt)


def get_order_by_payment_id(db: Session, payment_id: str) -> Order | None:
    stmt = (
        select(Order)
        .where(Order.yookassa_payment_id == payment_id)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
        )
    )
    return db.scalar(stmt)


def serialize_order(order: Order) -> OrderRead:
    return OrderRead(
        id=order.id,
        status=order.status,
        total_amount=float(order.total_amount),
        currency=order.currency,
        payment_id=order.yookassa_payment_id,
        confirmation_url=order.confirmation_url,
        items=[
            OrderItemRead(
                product_id=item.product_id,
                title=item.product.name,
                quantity=item.quantity,
                unit_price=float(item.unit_price),
            )
            for item in order.items
        ],
    )


def create_payment_for_products(db: Session, user_id: int, product_ids: list[int]) -> PaymentCreateResponse:
    if not product_ids:
        raise ValueError("Cart is empty")

    quantities = Counter(product_ids)
    products = list(
        db.scalars(
            select(Product)
            .where(Product.id.in_(list(quantities.keys())), Product.is_active.is_(True))
            .options(selectinload(Product.images), selectinload(Product.sizes), selectinload(Product.category))
        ).all()
    )
    if len(products) != len(quantities):
        raise ValueError("Some products are unavailable")

    total = sum((Decimal(product.price) * quantities[product.id] for product in products), Decimal("0.00"))
    order = Order(
        user_id=user_id,
        status="pending",
        total_amount=total,
        currency="RUB",
    )
    db.add(order)
    db.flush()

    for product in products:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantities[product.id],
                unit_price=product.price,
            )
        )

    payment = create_yookassa_payment(
        order_id=order.id,
        amount=total,
        description=f"CloudMarket order #{order.id}",
    )
    confirmation_url = payment.get("confirmation", {}).get("confirmation_url")
    payment_id = payment.get("id")
    if not payment_id or not confirmation_url:
        raise ValueError("YooKassa did not return payment confirmation URL")

    order.yookassa_payment_id = payment_id
    order.confirmation_url = confirmation_url
    order.status = payment.get("status", "pending")
    db.commit()

    return PaymentCreateResponse(
        order_id=order.id,
        payment_id=payment_id,
        status=order.status,
        confirmation_url=confirmation_url,
        total_amount=float(order.total_amount),
        currency=order.currency,
    )


def apply_payment_status(db: Session, payment: dict) -> Order | None:
    payment_id = payment.get("id")
    if not payment_id:
        return None

    order = get_order_by_payment_id(db, payment_id)
    if order is None:
        return None

    status = payment.get("status")
    paid = bool(payment.get("paid"))
    if status == "succeeded" and paid:
        order.status = "paid"
        if order.paid_at is None:
            order.paid_at = datetime.utcnow()
    elif status == "canceled":
        order.status = "canceled"
    elif status:
        order.status = status

    db.commit()
    db.refresh(order)
    return order


def register_user(db: Session, payload: UserCreate) -> AuthResponse:
    existing_user = get_user_by_email(db, payload.email)
    if existing_user is not None:
        raise ValueError("User with this email already exists")

    user = User(
        full_name=payload.full_name.strip(),
        email=payload.email.lower().strip(),
        password_hash=hash_password(payload.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return AuthResponse(access_token=create_access_token(user.id), user=UserRead.model_validate(user))


def authenticate_user(db: Session, email: str, password: str) -> AuthResponse | None:
    user = get_user_by_email(db, email)
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return AuthResponse(access_token=create_access_token(user.id), user=UserRead.model_validate(user))
