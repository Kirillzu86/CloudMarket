from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Category, Product, ProductImage, ProductSize
from seed_data import SEED_PRODUCTS


def seed_database(db: Session) -> None:
    existing_product = db.scalar(select(Product.id).limit(1))
    if existing_product is not None:
        return

    categories: dict[str, Category] = {}
    for item in SEED_PRODUCTS:
        category = categories.get(item.category)
        if category is None:
            category = Category(name=item.category)
            db.add(category)
            db.flush()
            categories[item.category] = category

        product = Product(
            name=item.name,
            description=item.description,
            price=item.price,
            stock=item.stock,
            is_active=True,
            category_id=category.id,
        )
        db.add(product)
        db.flush()

        for size_name in item.sizes:
            db.add(ProductSize(product_id=product.id, size=size_name, stock=item.stock))

        for image_url in item.images:
            db.add(ProductImage(product_id=product.id, url=image_url))

    db.commit()
