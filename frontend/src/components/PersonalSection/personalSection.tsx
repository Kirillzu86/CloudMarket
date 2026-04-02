import { useEffect, useState } from "react";

import { api, clearAuth, getStoredUser, type AuthUser } from "../../api";
import { products } from "../../data/store";
import "./personalSection.css";

export default function PersonalSection() {
  const [user, setUser] = useState<AuthUser | null>(getStoredUser());
  const [error, setError] = useState("");
  const [wishlistCount, setWishlistCount] = useState(0);

  useEffect(() => {
    async function loadUser() {
      try {
        const currentUser = await api.getCurrentUser();
        setUser(currentUser);
      } catch (err) {
        if (getStoredUser()) {
          setError(err instanceof Error ? err.message : "Failed to load account");
        }
      }
    }

    void loadUser();
  }, []);

  useEffect(() => {
    try {
      const raw = localStorage.getItem("cloudmarket_wishlist");
      if (!raw) {
        setWishlistCount(0);
        return;
      }

      const parsed = JSON.parse(raw) as unknown;
      setWishlistCount(Array.isArray(parsed) ? parsed.length : 0);
    } catch {
      setWishlistCount(0);
    }
  }, []);

  function handleLogout() {
    clearAuth();
    setUser(null);
  }

  const profileStats = [
    { label: "Orders", value: user ? "01" : "00" },
    { label: "Wishlist", value: String(wishlistCount).padStart(2, "0") },
    { label: "Discount", value: user ? "15%" : "0%" },
  ];

  return (
    <main className="profile-page">
      <section className="profile-hero">
        <div className="site-shell profile-hero__inner">
          <div>
            <p className="section-label">Personal Section</p>
            <h1 className="profile-title">Welcome back, {user?.full_name ?? "Guest"}.</h1>
            <p className="profile-subtitle">
              {user
                ? `Signed in as ${user.email}. Your profile, recent order activity, and saved pieces all in one place.`
                : "Create an account or sign in to manage your profile, orders, and saved pieces."}
            </p>
            {error ? <p className="profile-note">{error}</p> : null}
            {user ? (
              <button type="button" className="profile-logout" onClick={handleLogout}>
                Log out
              </button>
            ) : null}
          </div>
          <div className="profile-summary">
            {profileStats.map((item) => (
              <div key={item.label} className="profile-summary__item">
                <strong>{item.value}</strong>
                <span>{item.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="profile-content">
        <div className="site-shell profile-content__grid">
          <div className="profile-panel">
            <h2>Recent order</h2>
            <div className="profile-order">
              <img src={products[0].image} alt={products[0].title} className="profile-order__image" />
              <div>
                <strong>{products[0].title}</strong>
                <p>{user ? "Order #CM-1427 - Processing" : "No active orders yet"}</p>
                <span>{user ? "Expected delivery: 04 Apr 2026" : "Sign in to track your orders"}</span>
              </div>
            </div>
          </div>

          <div className="profile-panel profile-panel--light">
            <h2>Saved preferences</h2>
            <ul className="profile-list">
              <li>Preferred size: {user ? "M" : "Not selected"}</li>
              <li>Wishlist items: {wishlistCount}</li>
              <li>Account status: {user ? "Active" : "Guest"}</li>
            </ul>
          </div>
        </div>
      </section>
    </main>
  );
}
