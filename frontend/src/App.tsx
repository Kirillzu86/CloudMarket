import { BrowserRouter, Route, Routes } from "react-router-dom";

import "../../base.css";
import "./App.css";

import { ShopActionsProvider } from "./context/ShopActionsContext";
import NavigationOverlay from "./components/Navigates/Navigate";
import Cart from "./components/PersonalSection/cart/cart";
import PersonalSection from "./components/PersonalSection/personalSection";
import Wishlist from "./components/PersonalSection/wishlist/wishlist";
import About from "./components/about/about";
import SiteFooter from "./components/layout/SiteFooter";
import LoginPage from "./components/login-register/LoginPage/loginPage";
import RegisterPage from "./components/login-register/RegisterPage/regPage";
import ProductDetailsPage from "./components/productDetail/productDetail";
import ProductsPage from "./components/products/productsPage";
import Shop from "./components/shop/shop";

function App() {
  return (
    <BrowserRouter>
      <ShopActionsProvider>
        <div className="app-shell">
          <NavigationOverlay />
          <Routes>
            <Route path="/" element={<Shop />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/products/:slug" element={<ProductDetailsPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/personalsection" element={<PersonalSection />} />
            <Route path="/about" element={<About />} />
            <Route path="/wishlist" element={<Wishlist />} />
            <Route path="*" element={<ProductsPage />} />
          </Routes>
          <SiteFooter />
        </div>
      </ShopActionsProvider>
    </BrowserRouter>
  );
}

export default App;
