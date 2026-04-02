# main.py — только верх + один маршрут (остальное по аналогии)
from collections.abc import Generator

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
from auth import decode_access_token
from database import SessionLocal, create_tables
from schemas import AuthResponse, ProductRead, UserCreate, UserLogin, UserRead

app = FastAPI(title="CloudMarket API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_tables()
    db = SessionLocal()
    try:
        crud.ensure_seeded(db)
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> UserRead:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token") from exc

    user = crud.get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return UserRead.model_validate(user)


@app.get("/api/products", response_model=list[ProductRead])
def get_products(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[ProductRead]:
    crud.ensure_seeded(db)
    return crud.get_products(db=db, skip=skip, limit=limit)


@app.get("/api/products/{slug}", response_model=ProductRead)
def get_product(slug: str, db: Session = Depends(get_db)) -> ProductRead:
    crud.ensure_seeded(db)
    product = crud.get_product_by_slug(db=db, slug=slug)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/api/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> AuthResponse:
    try:
        return crud.register_user(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@app.post("/api/auth/login", response_model=AuthResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> AuthResponse:
    auth_response = crud.authenticate_user(db, payload.email, payload.password)
    if auth_response is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return auth_response


@app.get("/api/auth/me", response_model=UserRead)
def me(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    return current_user
