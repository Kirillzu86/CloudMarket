import { BrowserRouter, Routes, Route } from 'react-router-dom'

import './App.css'

import LoginPage from './components/login-register/LoginPage/loginPage'
import RegisterPage from './components/login-register/RegisterPage/regPage'
import Shop from './components/shop/shop'
import Cart from './components/PersonalSection/cart/cart'
import PersonalSection from './components/PersonalSection/personalSection'
import NavigationOverlay from './components/Navigates/Navigate'
import About from './components/about/about'

function App() {

  return (
    <>
      <BrowserRouter>
        <NavigationOverlay />
        <Routes>
          <Route path="/" element={<Shop />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/personalsection" element={<PersonalSection />} />
          <Route path="/About" element={<About />} />
          <Route path="*" element={<div>404 Not Found</div>} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App