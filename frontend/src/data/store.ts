export type Product = {
  id: number;
  slug: string;
  title: string;
  subtitle: string;
  category: string;
  price: number;
  oldPrice?: number;
  rating: number;
  reviews: number;
  badge?: "New" | "Sale" | "Best Seller";
  colors: string[];
  sizes: string[];
  image: string;
  thumbnails: string[];
  description: string;
};

export const products: Product[] = [
  {
    id: 1,
    slug: "amber-blaze-knit-sweater",
    title: "Amber Blaze Knit Sweater",
    subtitle: "Soft oversized knit for everyday layering.",
    category: "Women",
    price: 89,
    oldPrice: 120,
    rating: 4.8,
    reviews: 214,
    badge: "Best Seller",
    colors: ["#f08a18", "#1f2430", "#f3f1ed"],
    sizes: ["XS", "S", "M", "L"],
    image:
      "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=900&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=500&q=80",
      "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=500&q=80",
      "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=500&q=80",
    ],
    description:
      "A warm statement knit with a relaxed silhouette, textured finish, and elevated color tone inspired by late autumn light.",
  },
  {
    id: 2,
    slug: "minimal-ivory-tee",
    title: "Minimal Ivory Tee",
    subtitle: "Clean everyday essential in premium cotton.",
    category: "Basics",
    price: 42,
    rating: 4.6,
    reviews: 96,
    badge: "New",
    colors: ["#f8f5ef", "#cfc8bd"],
    sizes: ["S", "M", "L", "XL"],
    image:
      "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=500&q=80",
      "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=500&q=80",
    ],
    description:
      "Cut from structured cotton jersey with a crisp neckline and easy drape that works across all seasons.",
  },
  {
    id: 3,
    slug: "charcoal-urban-hoodie",
    title: "Charcoal Urban Hoodie",
    subtitle: "Street-ready silhouette with soft brushed interior.",
    category: "Hoodies",
    price: 74,
    oldPrice: 98,
    rating: 4.7,
    reviews: 180,
    badge: "Sale",
    colors: ["#565f6f", "#16181d"],
    sizes: ["M", "L", "XL"],
    image:
      "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=500&q=80",
      "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=500&q=80",
    ],
    description:
      "Designed for movement with a dense knit shell, roomy hood, and refined finish that keeps its shape.",
  },
  {
    id: 4,
    slug: "ember-track-set",
    title: "Ember Track Set",
    subtitle: "Bold monochrome fit made for active city days.",
    category: "Sets",
    price: 109,
    rating: 4.5,
    reviews: 67,
    colors: ["#d8671c", "#f6d9bf"],
    sizes: ["S", "M", "L"],
    image:
      "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=500&q=80",
    ],
    description:
      "Lightweight coordinated set with sharp lines and a confident orange tone that stands out without shouting.",
  },
  {
    id: 5,
    slug: "navy-tailored-jacket",
    title: "Navy Tailored Jacket",
    subtitle: "Structured outer layer with modern relaxed cut.",
    category: "Outerwear",
    price: 132,
    rating: 4.9,
    reviews: 141,
    badge: "New",
    colors: ["#1f3558", "#8ea2be"],
    sizes: ["M", "L", "XL"],
    image:
      "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=900&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=500&q=80",
    ],
    description:
      "Relaxed tailoring, deep navy fabric, and a versatile drape that works with denim, trousers, or layered knitwear.",
  },
  {
    id: 6,
    slug: "clean-white-oversized-tee",
    title: "Clean White Oversized Tee",
    subtitle: "Breathable staple with generous proportions.",
    category: "Basics",
    price: 38,
    rating: 4.4,
    reviews: 58,
    colors: ["#ffffff", "#e9e7e2"],
    sizes: ["S", "M", "L", "XL"],
    image:
      "https://images.unsplash.com/photo-1527719327859-c6ce80353573?auto=format&fit=crop&w=900&q=80",
    thumbnails: [
      "https://images.unsplash.com/photo-1527719327859-c6ce80353573?auto=format&fit=crop&w=500&q=80",
    ],
    description:
      "An airy oversized tee with a polished shoulder drop and elevated finishing for a premium essentials wardrobe.",
  },
];

export const categories = [
  { name: "Men", theme: "light", blurb: "Sharp daily layers and relaxed tailoring." },
  { name: "Women", theme: "blue", blurb: "Statement silhouettes with confident palettes." },
  { name: "Kids", theme: "dark", blurb: "Comfort-driven pieces built for motion." },
  { name: "Accessories", theme: "light", blurb: "Bags, caps, socks, and finishing touches." },
];

export const stats = [
  { label: "Products", value: "250+" },
  { label: "Collections", value: "12" },
  { label: "Rating", value: "4.8" },
];

export const profileStats = [
  { label: "Orders", value: "12" },
  { label: "Wishlist", value: "08" },
  { label: "Discount", value: "15%" },
];

export const footerGroups = {
  pages: ["Home", "Shop", "Product", "Wishlist", "Account", "Login"],
  support: ["FAQs", "Shipping", "Returns", "Track Order", "Privacy", "Terms"],
};
