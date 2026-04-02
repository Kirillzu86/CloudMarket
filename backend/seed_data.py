from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class SeedProduct:
    name: str
    category: str
    description: str
    price: Decimal
    stock: int
    sizes: list[str]
    images: list[str]
    subtitle: str
    old_price: float | None
    rating: float
    reviews: int
    badge: str | None
    colors: list[str]


SEED_PRODUCTS: list[SeedProduct] = [
    SeedProduct(
        name="Amber Blaze Knit Sweater",
        category="Women",
        description="A warm statement knit with a relaxed silhouette, textured finish, and elevated color tone inspired by late autumn light.",
        price=Decimal("89.00"),
        stock=24,
        sizes=["XS", "S", "M", "L"],
        images=[
            "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=500&q=80",
            "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=500&q=80",
        ],
        subtitle="Soft oversized knit for everyday layering.",
        old_price=120,
        rating=4.8,
        reviews=214,
        badge="Best Seller",
        colors=["#f08a18", "#1f2430", "#f3f1ed"],
    ),
    SeedProduct(
        name="Minimal Ivory Tee",
        category="Basics",
        description="Cut from structured cotton jersey with a crisp neckline and easy drape that works across all seasons.",
        price=Decimal("42.00"),
        stock=48,
        sizes=["S", "M", "L", "XL"],
        images=[
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=500&q=80",
        ],
        subtitle="Clean everyday essential in premium cotton.",
        old_price=None,
        rating=4.6,
        reviews=96,
        badge="New",
        colors=["#f8f5ef", "#cfc8bd"],
    ),
    SeedProduct(
        name="Charcoal Urban Hoodie",
        category="Hoodies",
        description="Designed for movement with a dense knit shell, roomy hood, and refined finish that keeps its shape.",
        price=Decimal("74.00"),
        stock=31,
        sizes=["M", "L", "XL"],
        images=[
            "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=500&q=80",
        ],
        subtitle="Street-ready silhouette with soft brushed interior.",
        old_price=98,
        rating=4.7,
        reviews=180,
        badge="Sale",
        colors=["#565f6f", "#16181d"],
    ),
    SeedProduct(
        name="Ember Track Set",
        category="Sets",
        description="Lightweight coordinated set with sharp lines and a confident orange tone that stands out without shouting.",
        price=Decimal("109.00"),
        stock=18,
        sizes=["S", "M", "L"],
        images=[
            "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80",
        ],
        subtitle="Bold monochrome fit made for active city days.",
        old_price=None,
        rating=4.5,
        reviews=67,
        badge=None,
        colors=["#d8671c", "#f6d9bf"],
    ),
    SeedProduct(
        name="Navy Tailored Jacket",
        category="Outerwear",
        description="Relaxed tailoring, deep navy fabric, and a versatile drape that works with denim, trousers, or layered knitwear.",
        price=Decimal("132.00"),
        stock=14,
        sizes=["M", "L", "XL"],
        images=[
            "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=900&q=80",
        ],
        subtitle="Structured outer layer with modern relaxed cut.",
        old_price=None,
        rating=4.9,
        reviews=141,
        badge="New",
        colors=["#1f3558", "#8ea2be"],
    ),
    SeedProduct(
        name="Clean White Oversized Tee",
        category="Basics",
        description="An airy oversized tee with a polished shoulder drop and elevated finishing for a premium essentials wardrobe.",
        price=Decimal("38.00"),
        stock=52,
        sizes=["S", "M", "L", "XL"],
        images=[
            "https://images.unsplash.com/photo-1527719327859-c6ce80353573?auto=format&fit=crop&w=900&q=80",
        ],
        subtitle="Breathable staple with generous proportions.",
        old_price=None,
        rating=4.4,
        reviews=58,
        badge=None,
        colors=["#ffffff", "#e9e7e2"],
    ),
]
