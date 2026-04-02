import { Link } from "react-router-dom";
import { categories, products as fallbackProducts, stats } from "../../data/store";
import { useCatalogProducts } from "../../hooks/useCatalog";
import Card from "./cards/card";
import "./shop.css";

export default function Shop() {
  const { products, error } = useCatalogProducts();
  const featuredProducts = products.slice(0, 6);
  const heroProduct = featuredProducts[0] ?? fallbackProducts[0];
  const promoProduct = featuredProducts[4] ?? featuredProducts[0] ?? fallbackProducts[4];

  return (
    <main className="home-page">
      <section className="hero-section section">
        <div className="site-shell hero-grid">
          <div className="hero-copy">
            <p className="section-label hero-eyebrow">New Era</p>
            <h1 className="hero-title">
              Modern <br /> brand <br /> with <span>meaning</span>
            </h1>
            <p className="hero-text">
              Contemporary essentials with bold color direction, premium materials,
              and a storefront experience built to feel editorial.
            </p>
            <div className="hero-actions">
              <Link to="/products" className="btn btn-primary">
                Shop Collection
              </Link>
              <Link to="/about" className="btn btn-outline">
                Our Story
              </Link>
            </div>
            <div className="hero-stats">
              {stats.map((item) => (
                <div key={item.label} className="hero-stat">
                  <strong>{item.value}</strong>
                  <span>{item.label}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="hero-visual">
            <div className="hero-card">
              <img
                src={heroProduct.image}
                alt={heroProduct.title}
                className="hero-image"
              />
              <div className="hero-floating hero-floating--left">Since 2017</div>
              <div className="hero-floating hero-floating--right">New Drop</div>
              <div className="hero-floating hero-floating--bottom">Soft knit / clean fit</div>
            </div>
          </div>
        </div>
      </section>

      <section className="categories-section section">
        <div className="site-shell">
          <div className="section-heading-row">
            <div>
              <p className="section-label">Shop By Style</p>
              <h2>Curated categories</h2>
            </div>
            <Link to="/products" className="section-link">
              See all products
            </Link>
          </div>

          <div className="category-grid">
            {categories.map((category) => (
              <Link
                key={category.name}
                to="/products"
                className={`category-card${
                  category.theme === "blue"
                    ? " category-card--blue"
                    : category.theme === "dark"
                    ? " category-card--dark"
                    : ""
                }`}
              >
                <span className="category-chip">{category.name}</span>
                <div>
                  <h3 className="category-card-title">{category.name}</h3>
                  <p className="category-card-text">{category.blurb}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="featured-section section">
        <div className="site-shell">
          {error ? <p className="catalog-status">Using local catalog fallback.</p> : null}
          <div className="section-heading-row">
            <div>
              <p className="section-label">Amber Glow</p>
              <h2>Featured products</h2>
            </div>
            <div className="filter-pills">
              <button type="button" className="filter-btn active">All</button>
              <button type="button" className="filter-btn">Women</button>
              <button type="button" className="filter-btn">Men</button>
              <button type="button" className="filter-btn">New In</button>
            </div>
          </div>

          <Card items={featuredProducts} />
        </div>
      </section>

      <section className="promo-section section">
        <div className="site-shell promo-banner">
          <div className="promo-image-wrap">
            <img src={promoProduct.image} alt={promoProduct.title} className="promo-image" />
          </div>
          <div className="promo-copy">
            <p className="section-label">Drop Of The Week</p>
            <h2>Streetwear redefined</h2>
            <p>
              Tailored outerwear, sharper knitwear, and relaxed essentials combined into one
              strong seasonal edit.
            </p>
            <div className="promo-points">
              <span>Premium fabrics</span>
              <span>Fast shipping</span>
              <span>Easy returns</span>
            </div>
            <div className="hero-actions">
              <Link to={`/products/${promoProduct.slug}`} className="btn btn-primary">
                View Product
              </Link>
              <Link to="/products" className="btn btn-outline">
                Browse More
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="newsletter-section section">
        <div className="site-shell newsletter-box">
          <p className="section-label">Join The Club</p>
          <h2>Weekly updates from the latest drop</h2>
          <p className="newsletter-text">
            Be first to access launches, limited colors, and special pricing.
          </p>
          <form className="newsletter-form">
            <input type="email" className="newsletter-input" placeholder="Your email address" />
            <button type="submit" className="btn btn-secondary">Subscribe</button>
          </form>
        </div>
      </section>
    </main>
  );
}
