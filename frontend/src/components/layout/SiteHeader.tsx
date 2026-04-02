import { Link, NavLink } from "react-router-dom";
import "./siteLayout.css";

const links = [
  { to: "/", label: "Home" },
  { to: "/products", label: "Products" },
  { to: "/about", label: "About" },
  { to: "/personalsection", label: "Account" },
];

export default function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-shell site-header__inner">
        <nav className="site-header__nav" aria-label="Primary">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `site-header__link${isActive ? " site-header__link--active" : ""}`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        <Link to="/" className="site-header__brand">
          VTM
        </Link>

        <div className="site-header__actions">
          <NavLink to="/login" className="site-header__icon" aria-label="Login">
            <span className="site-header__icon-mark">AC</span>
          </NavLink>
          <NavLink to="/wishlist" className="site-header__icon" aria-label="Wishlist">
            <span className="site-header__icon-mark">WL</span>
          </NavLink>
          <NavLink to="/cart" className="site-header__icon" aria-label="Cart">
            <span className="site-header__icon-mark">BG</span>
          </NavLink>
        </div>
      </div>
    </header>
  );
}
