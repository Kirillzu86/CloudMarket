from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from auth import create_access_token, hash_password, verify_password
from models import Product, User
from serializers import serialize_product
from seed import seed_database
from schemas import AuthResponse, UserCreate, UserRead


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
