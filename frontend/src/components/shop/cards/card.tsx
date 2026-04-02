import { Link } from "react-router-dom";
import { useShopActions } from "../../../context/ShopActionsContext";
import type { Product } from "../../../data/store";
import "./card.css";

type CardProps = {
  items: Product[];
};

export default function Card({ items }: CardProps) {
  const { toggleWishlist, addToCart, isWishlisted, isInCart } = useShopActions();

  return (
    <div className="product-grid">
      {items.map((product) => (
        <article key={product.id} className="product-card card">
          <Link to={`/products/${product.slug}`} className="product-card__image-link">
            {product.badge ? (
              <span
                className={`card-badge${product.badge === "New" ? " card-badge--new" : product.badge === "Sale" ? " card-badge--sale" : ""}`}
              >
                {product.badge}
              </span>
            ) : null}
            <img className="product-image" src={product.image} alt={product.title} />
          </Link>

          <div className="product-body">
            <div className="product-meta-row">
              <span className="product-category">{product.category}</span>
              <span className="product-rating">{product.rating} / 5</span>
            </div>

            <Link to={`/products/${product.slug}`} className="product-title-link">
              <h3 className="card-title product-title">{product.title}</h3>
            </Link>
            <p className="product-subtitle">{product.subtitle}</p>

            <div className="product-price-row">
              <span className="card-price">${product.price}</span>
              {product.oldPrice ? <span className="card-price-original">${product.oldPrice}</span> : null}
            </div>

            <div className="product-actions">
              <button
                className="btn btn-primary btn-card-primary"
                type="button"
                onClick={() => addToCart(product.id)}
              >
                {isInCart(product.id) ? "Added" : "Add to cart"}
              </button>
              <button
                className="btn-card-ghost"
                type="button"
                onClick={() => toggleWishlist(product.id)}
              >
                {isWishlisted(product.id) ? "Saved" : "Save"}
              </button>
            </div>
            <Link to={`/products/${product.slug}`} className="product-card__details-link">
              Open details
            </Link>
          </div>
        </article>
      ))}
    </div>
  );
}
