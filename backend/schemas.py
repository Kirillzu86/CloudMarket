from pydantic import BaseModel, ConfigDict


class ProductRead(BaseModel):
    id: int
    slug: str
    title: str
    subtitle: str
    category: str
    price: float
    old_price: float | None = None
    rating: float
    reviews: int
    badge: str | None = None
    colors: list[str]
    sizes: list[str]
    image: str
    thumbnails: list[str]
    description: str


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    is_active: bool


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class PaymentCreate(BaseModel):
    product_ids: list[int]


class PaymentCreateResponse(BaseModel):
    order_id: int
    payment_id: str
    status: str
    confirmation_url: str
    total_amount: float
    currency: str


class OrderItemRead(BaseModel):
    product_id: int
    title: str
    quantity: int
    unit_price: float


class OrderRead(BaseModel):
    id: int
    status: str
    total_amount: float
    currency: str
    payment_id: str | None
    confirmation_url: str | None
    items: list[OrderItemRead]
