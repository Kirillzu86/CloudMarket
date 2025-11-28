# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Product, ProductSize

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 20):
    result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()