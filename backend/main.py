# main.py — только верх + один маршрут (остальное по аналогии)
from fastapi import FastAPI, Depends
from database import SessionLocal
from models import Product

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/products")
def get_products(db=Depends(get_db)):
    return db.query(Product).all()