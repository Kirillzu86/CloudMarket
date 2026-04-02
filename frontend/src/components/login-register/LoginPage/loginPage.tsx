import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { api, saveAuth } from "../../../api";
import "./loginPage.css";

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const payload = await api.login({ email, password });
      saveAuth(payload);
      navigate("/personalsection");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="main-section auth-page-shell">
      <section className="auth-card auth-card--enhanced">
        <header className="auth-header">
          <p className="section-label">Welcome Back</p>
          <h1 className="auth-title">Log in</h1>
          <p className="auth-subtitle">Enter your details to access your account and saved products.</p>
        </header>
        <form className="auth-form" onSubmit={handleSubmit}>
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
            {submitting ? "Signing in..." : "Log in"}
          </button>
        </form>
        <p className="auth-switch">
          No account yet? <Link to="/register" className="btn-link">Create one</Link>
        </p>
      </section>
    </main>
  );
}
