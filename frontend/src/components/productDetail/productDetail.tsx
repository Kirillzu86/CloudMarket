import { Link, useParams } from "react-router-dom";

import { useShopActions } from "../../context/useShopActions";
import { products as fallbackProducts } from "../../data/store";
import { useCatalogProduct, useCatalogProducts } from "../../hooks/useCatalog";
import Card from "../shop/cards/card";
import "./productDetail.css";

export default function ProductDetailsPage() {
  const { slug } = useParams();
  const { product, error } = useCatalogProduct(slug);
  const { products } = useCatalogProducts();
  const { addToCart, toggleWishlist, isInCart, isWishlisted } = useShopActions();
  const relatedProducts = (products.length > 0 ? products : fallbackProducts)
    .filter((item) => item.id !== product.id)
    .slice(0, 3);

  return (
    <main className="product-page">
      <section className="product-section">
        <div className="site-shell product-layout">
          <div className="product-gallery">
            <div className="product-gallery__main">
              <img src={product.image} alt={product.title} className="product-gallery__image" />
            </div>
            <div className="product-gallery__thumbs">
              {product.thumbnails.map((thumb, index) => (
                <img
                  key={`${product.id}-${index}`}
                  src={thumb}
                  alt={`${product.title} ${index + 1}`}
                  className="product-gallery__thumb"
                />
              ))}
            </div>
          </div>

          <div className="product-info">
            {error ? <p className="catalog-status">Using local product fallback.</p> : null}
            <p className="section-label">{product.category}</p>
            <h1 className="product-info__title">{product.title}</h1>
            <p className="product-info__subtitle">{product.description}</p>

            <div className="product-info__rating">Rating {product.rating} / 5 - {product.reviews} reviews</div>

            <div className="product-info__price">
              <span className="product-info__price-current">${product.price}</span>
              {product.oldPrice ? <span className="card-price-original">${product.oldPrice}</span> : null}
            </div>

            <div className="product-info__group">
              <span className="product-info__label">Color</span>
              <div className="product-swatches">
                {product.colors.map((color) => (
                  <span key={color} className="product-swatch" style={{ backgroundColor: color }} />
                ))}
              </div>
            </div>

            <div className="product-info__group">
              <span className="product-info__label">Size</span>
              <div className="product-sizes">
                {product.sizes.map((size) => (
                  <button
                    key={size}
                    type="button"
                    className={`product-size${size === "M" ? " product-size--active" : ""}`}
                  >
                    {size}
                  </button>
                ))}
              </div>
            </div>

            <div className="product-actions product-actions--detail">
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => addToCart(product.id)}
              >
                {isInCart(product.id) ? "Added to cart" : "Add to cart"}
              </button>
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => toggleWishlist(product.id)}
              >
                {isWishlisted(product.id) ? "Saved in wishlist" : "Save to wishlist"}
              </button>
            </div>

            <div className="product-benefits">
              <div><strong>Free shipping</strong><span>Orders over $120</span></div>
              <div><strong>Easy return</strong><span>Within 14 days</span></div>
              <div><strong>Secure checkout</strong><span>Stripe and PayPal supported</span></div>
            </div>
          </div>
        </div>
      </section>

      <section className="related-section">
        <div className="site-shell related-section__inner">
          <div className="section-heading-row">
            <div>
              <p className="section-label">You may also like</p>
              <h2>Related products</h2>
            </div>
            <Link to="/products" className="section-link">Back to catalog</Link>
          </div>
          <Card items={relatedProducts} />
        </div>
      </section>
    </main>
  );
}
