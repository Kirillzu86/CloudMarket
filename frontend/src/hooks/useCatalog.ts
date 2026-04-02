import { useEffect, useState } from "react";

import { api } from "../api";
import { products as fallbackProducts, type Product } from "../data/store";

export function useCatalogProducts() {
  const [products, setProducts] = useState<Product[]>(fallbackProducts);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadProducts() {
      try {
        const items = await api.getProducts();
        if (active && items.length > 0) {
          setProducts(items);
        }
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : "Failed to load products");
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadProducts();

    return () => {
      active = false;
    };
  }, []);

  return { products, loading, error };
}

export function useCatalogProduct(slug?: string) {
  const fallbackProduct =
    fallbackProducts.find((item) => item.slug === slug) ?? fallbackProducts[0];
  const [product, setProduct] = useState<Product>(fallbackProduct);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) {
      setLoading(false);
      return;
    }

    const currentSlug = slug;

    let active = true;

    async function loadProduct() {
      try {
        const item = await api.getProductBySlug(currentSlug);
        if (active) {
          setProduct(item);
        }
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : "Failed to load product");
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadProduct();

    return () => {
      active = false;
    };
  }, [slug]);

  return { product, loading, error };
}
