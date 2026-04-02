import { Link } from "react-router-dom";
import { products } from "../../data/store";
import "./about.css";

export default function About() {
  return (
    <main className="about-page">
      <section className="about-hero">
        <div className="site-shell about-hero__inner">
          <div>
            <p className="section-label">About VTM</p>
            <h1 className="about-title">A modern label built around clarity and confidence.</h1>
          </div>
          <p className="about-copy">
            We design a compact wardrobe for people who want fewer, better pieces. The visual system,
            product stories, and editorial layouts all work together to make shopping feel intentional.
          </p>
        </div>
      </section>

      <section className="about-values">
        <div className="site-shell about-values__grid">
          <article className="about-value-card">
            <h2>Premium materials</h2>
            <p>Dense knits, structured cottons, and durable finishing that stays sharp after repeat wear.</p>
          </article>
          <article className="about-value-card about-value-card--accent">
            <h2>Seasonal color</h2>
            <p>Neutral foundations paired with amber, cobalt, charcoal, and crisp ivory drops.</p>
          </article>
          <article className="about-value-card about-value-card--dark">
            <h2>Designed for city pace</h2>
            <p>Easy layering, practical silhouettes, and fast delivery for people always in motion.</p>
          </article>
        </div>
      </section>

      <section className="about-feature">
        <div className="site-shell about-feature__inner">
          <img src={products[2].image} alt={products[2].title} className="about-feature__image" />
          <div className="about-feature__copy">
            <p className="section-label">Our Promise</p>
            <h2>Fashion that feels sharp online and even better in real life.</h2>
            <p>
              Every collection is built to be mixed together. That means better product pages, clearer sizing,
              and a cleaner visual hierarchy that helps customers decide faster.
            </p>
            <Link to="/products" className="btn btn-primary">Shop the collection</Link>
          </div>
        </div>
      </section>
    </main>
  );
}
