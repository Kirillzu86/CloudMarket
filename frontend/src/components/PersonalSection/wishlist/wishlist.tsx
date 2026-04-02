import { Link } from "react-router-dom";

import { useShopActions } from "../../../context/useShopActions";
import { products as fallbackProducts } from "../../../data/store";
import { useCatalogProducts } from "../../../hooks/useCatalog";
import "./wishlist.css";

export default function Wishlist() {
  const { products } = useCatalogProducts();
  const { wishlist, removeFromWishlist, addToCart } = useShopActions();
  const catalog = products.length > 0 ? products : fallbackProducts;
  const wishlistItems = catalog.filter((item) => wishlist.includes(item.id));

  if (wishlistItems.length === 0) {
    return (
      <main className="wishlist-page">
        <section className="wishlist-section">
          <div className="site-shell wishlist-empty">
            <div className="wishlist-empty__icon">WL</div>
            <p className="section-label">My Wishlist</p>
            <h1>No saved products yet</h1>
            <p className="wishlist-empty__text">
              Start collecting your favorite pieces and return here when you are ready to shop.
            </p>
            <Link to="/products" className="btn btn-primary">Explore products</Link>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="wishlist-page">
      <section className="wishlist-section">
        <div className="site-shell wishlist-list">
          <div className="wishlist-header">
            <p className="section-label">My Wishlist</p>
            <h1>Saved products</h1>
          </div>
          {wishlistItems.map((item) => (
            <article key={item.id} className="wishlist-item">
              <img src={item.image} alt={item.title} className="wishlist-item__image" />
              <div className="wishlist-item__content">
                <div>
                  <h2>{item.title}</h2>
                  <p>{item.subtitle}</p>
                </div>
                <div className="wishlist-item__actions">
                  <strong>${item.price}</strong>
                  <button type="button" className="btn btn-primary" onClick={() => addToCart(item.id)}>
                    Add to cart
                  </button>
                  <button type="button" className="btn btn-outline" onClick={() => removeFromWishlist(item.id)}>
                    Remove
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
