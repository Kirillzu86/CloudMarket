import { useShopActions } from "../../../context/useShopActions";
import { products as fallbackProducts } from "../../../data/store";
import { useCatalogProducts } from "../../../hooks/useCatalog";
import "./cart.css";

export default function Cart() {
  const { products } = useCatalogProducts();
  const { cart, removeFromCart } = useShopActions();
  const catalog = products.length > 0 ? products : fallbackProducts;
  const cartItems = cart
    .map((id) => catalog.find((item) => item.id === id))
    .filter((item) => item !== undefined);
  const subtotal = cartItems.reduce((sum, item) => sum + item.price, 0);

  if (cartItems.length === 0) {
    return (
      <main className="cart-page">
        <section className="cart-section">
          <div className="site-shell cart-layout">
            <div className="cart-list">
              <div className="cart-heading">
                <p className="section-label">Shopping Bag</p>
                <h1>Your cart</h1>
              </div>
              <p className="cart-empty-state">Your cart is empty. Add a few pieces from the catalog.</p>
            </div>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="cart-page">
      <section className="cart-section">
        <div className="site-shell cart-layout">
          <div className="cart-list">
            <div className="cart-heading">
              <p className="section-label">Shopping Bag</p>
              <h1>Your cart</h1>
            </div>

            {cartItems.map((item) => (
              <article key={item.id} className="cart-item">
                <img src={item.image} alt={item.title} className="cart-item__image" />
                <div className="cart-item__content">
                  <div>
                    <h2>{item.title}</h2>
                    <p>{item.subtitle}</p>
                  </div>
                  <div className="cart-item__meta">
                    <span>Size M</span>
                    <span>Qty 1</span>
                    <strong>${item.price}</strong>
                    <button type="button" className="cart-remove" onClick={() => removeFromCart(item.id)}>
                      Remove
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </div>

          <aside className="cart-summary">
            <h2>Order summary</h2>
            <div className="cart-summary__row"><span>Subtotal</span><strong>${subtotal}</strong></div>
            <div className="cart-summary__row"><span>Shipping</span><strong>Free</strong></div>
            <div className="cart-summary__row"><span>Total</span><strong>${subtotal}</strong></div>
            <button type="button" className="btn btn-primary">Proceed to checkout</button>
          </aside>
        </div>
      </section>
    </main>
  );
}
