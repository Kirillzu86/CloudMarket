import { Link } from "react-router-dom";
import "./siteLayout.css";

const pageLinks = [
  { to: "/", label: "Home" },
  { to: "/products", label: "Shop" },
  { to: "/wishlist", label: "Wishlist" },
  { to: "/personalsection", label: "Account" },
  { to: "/login", label: "Login" },
  { to: "/about", label: "About" },
];

const supportLinks = ["FAQs", "Shipping", "Returns", "Track Order", "Privacy", "Terms"];

export default function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="site-shell site-footer__content">
        <div className="site-footer__intro">
          <Link to="/" className="footer-logo">
            VTM
          </Link>
          <p className="footer-description">
            CloudMarket is a concept fashion store with premium essentials, modern color stories,
            and clean product experiences.
          </p>
          <div className="social-links">
            <a className="social-icon" href="/" aria-label="Instagram">ig</a>
            <a className="social-icon" href="/" aria-label="Twitter">tw</a>
            <a className="social-icon" href="/" aria-label="Dribbble">db</a>
            <a className="social-icon" href="/" aria-label="Pinterest">pt</a>
          </div>
        </div>

        <div>
          <h3 className="footer-col-title">Pages</h3>
          <ul className="footer-nav">
            {pageLinks.map((item) => (
              <li key={item.label}>
                <Link to={item.to} className="footer-nav-link">
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="footer-col-title">Support</h3>
          <ul className="footer-nav">
            {supportLinks.map((item) => (
              <li key={item}>
                <a href="/" className="footer-nav-link">{item}</a>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="footer-col-title">Contact</h3>
          <div className="contact-info">
            <div className="contact-item">4517 Washington Ave. Manchester, Kentucky 39495</div>
            <div className="contact-item">+1 (555) 307-4101</div>
            <div className="contact-item">hello@cloudmarket.store</div>
          </div>
        </div>
      </div>

      <div className="site-shell site-footer__bottom">
        <p className="copyright">© 2026 CloudMarket. Crafted for the storefront concept.</p>
        <div className="payment-badges">
          <span className="badge">Visa</span>
          <span className="badge">Mastercard</span>
          <span className="badge">PayPal</span>
          <span className="badge">Apple Pay</span>
        </div>
        <div className="legal-nav">
          <a href="/" className="footer-nav-link">Terms</a>
          <a href="/" className="footer-nav-link">Privacy</a>
          <a href="/" className="footer-nav-link">Cookies</a>
        </div>
      </div>
    </footer>
  );
}
