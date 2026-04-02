import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import Base

BASE_DIR = Path(__file__).resolve().parent


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    data_dir = Path(os.getenv("CLOUDMARKET_DATA_DIR", BASE_DIR / "data")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{(data_dir / 'shop.db').as_posix()}"


DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
