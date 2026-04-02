import { useMemo, useState } from "react";
import Card from "../shop/cards/card";
import { useCatalogProducts } from "../../hooks/useCatalog";
import "./productsPage.css";

const filters = ["All", "Women", "Basics", "Hoodies", "Outerwear", "Sets"];

export default function ProductsPage() {
  const [activeFilter, setActiveFilter] = useState("All");
  const [query, setQuery] = useState("");
  const { products, loading, error } = useCatalogProducts();

  const filteredProducts = useMemo(() => {
    return products.filter((product) => {
      const matchesFilter = activeFilter === "All" || product.category === activeFilter;
      const term = query.trim().toLowerCase();
      const matchesQuery =
        term.length === 0 ||
        product.title.toLowerCase().includes(term) ||
        product.subtitle.toLowerCase().includes(term);

      return matchesFilter && matchesQuery;
    });
  }, [activeFilter, query]);

  return (
    <main className="products-page">
      <section className="products-hero">
        <div className="site-shell products-hero__inner">
          <div>
            <p className="section-label">All Products</p>
            <h1 className="products-title">Curated daily essentials</h1>
            <p className="products-subtitle">
              Explore the full line of elevated basics, statement knitwear, and city-ready layers.
            </p>
          </div>

          <div className="products-toolbar">
            <div className="search-box products-search">
              <input
                className="search-box-input"
                placeholder="Search products"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
              />
            </div>
            <span className="products-count">{filteredProducts.length} items</span>
          </div>
        </div>
      </section>

      <section className="products-content">
        <div className="site-shell products-content__inner">
          {loading ? <p className="catalog-status">Loading catalog...</p> : null}
          {error ? <p className="catalog-status">Backend unavailable, showing local catalog.</p> : null}
          <div className="products-filters">
            {filters.map((filter) => (
              <button
                key={filter}
                type="button"
                className={`filter-btn${activeFilter === filter ? " active" : ""}`}
                onClick={() => setActiveFilter(filter)}
              >
                {filter}
              </button>
            ))}
          </div>
          <Card items={filteredProducts} />
        </div>
      </section>
    </main>
  );
}
