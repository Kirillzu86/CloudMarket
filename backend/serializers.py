import re

from models import Product
from schemas import ProductRead
from seed_data import SEED_PRODUCTS


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "product"


SEED_LOOKUP = {slugify(item.name): item for item in SEED_PRODUCTS}


def serialize_product(product: Product) -> ProductRead:
    slug = slugify(product.name)
    seed = SEED_LOOKUP.get(slug)
    image_urls = [image.url for image in product.images]
    first_image = image_urls[0] if image_urls else ""

    return ProductRead(
        id=product.id,
        slug=slug,
        title=product.name,
        subtitle=seed.subtitle if seed else (product.description or "")[:64],
        category=product.category.name,
        price=float(product.price),
        old_price=seed.old_price if seed else None,
        rating=seed.rating if seed else 4.5,
        reviews=seed.reviews if seed else 0,
        badge=seed.badge if seed else None,
        colors=seed.colors if seed else ["#16181d"],
        sizes=[size.size for size in product.sizes],
        image=first_image,
        thumbnails=image_urls or [first_image],
        description=product.description or "",
    )
