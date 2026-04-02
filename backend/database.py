from pathlib import Path
from tempfile import gettempdir

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import Base

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(gettempdir()) / "cloudmarket"
DATA_DIR.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite:///{(DATA_DIR / 'shop.db').as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
