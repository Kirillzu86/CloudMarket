import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { api, saveAuth } from "../../../api";
import "./regPage.css";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const payload = await api.register({
        full_name: fullName,
        email,
        password,
      });
      saveAuth(payload);
      navigate("/personalsection");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="main-section auth-page-shell">
      <section className="auth-card auth-card--enhanced">
        <header className="auth-header">
          <p className="section-label">Create Account</p>
          <h1 className="auth-title">Join now</h1>
          <p className="auth-subtitle">Create your profile to save favorites, manage orders, and shop faster.</p>
        </header>
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">Full name</label>
            <div className="input-container">
              <span className="input-icon">O</span>
              <input
                id="name"
                className="form-input"
                type="text"
                placeholder="Alex Morgan"
                value={fullName}
                onChange={(event) => setFullName(event.target.value)}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="email">Email</label>
            <div className="input-container">
              <span className="input-icon">@</span>
              <input
                id="email"
                className="form-input"
                type="email"
                placeholder="hello@cloudmarket.store"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <div className="input-container">
              <span className="input-icon">*</span>
              <input
                id="password"
                className="form-input"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
            </div>
          </div>
          {error ? <p className="auth-error">{error}</p> : null}
          <button type="submit" className="btn-submit" disabled={submitting}>
            {submitting ? "Creating..." : "Create account"}
          </button>
        </form>
        <p className="auth-switch">
          Already registered? <Link to="/login" className="btn-link">Log in</Link>
        </p>
      </section>
    </main>
  );
}
