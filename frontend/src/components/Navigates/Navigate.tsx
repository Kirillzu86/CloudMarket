import { createPortal } from 'react-dom';
import { NavLink } from 'react-router-dom';

const NavigationOverlay = () => {
  if (!document) return null;

  return createPortal(
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        height: '70px',
        background: 'rgba(15, 15, 15, 0.95)',
        backdropFilter: 'blur(10px)',
        zIndex: 9999,
        padding: '0 2rem',
        display: 'flex',
        alignItems: 'center',
        boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
      }}
    >
      <nav style={{ display: 'flex', gap: '2rem', color: 'white', fontWeight: '500' }}>
        <NavLink to="/" style={{ textDecoration: 'none', color: 'white' }}>
          Главная
        </NavLink>
        <NavLink to="/about" style={{ textDecoration: 'none', color: 'white' }}>
          О нас
        </NavLink>
        <NavLink to="/personalsection" style={{ textDecoration: 'none', color: 'white' }}>
          Личный кабинет
        </NavLink>
        <NavLink to="/login" style={{ textDecoration: 'none', color: 'white' }}>
          Войти
        </NavLink>
        <NavLink to="/cart" style={{ textDecoration: 'none', color: 'white' }}>
          Корзина
        </NavLink>
      </nav>
    </div>,
    document.body
  );
};

export default NavigationOverlay;