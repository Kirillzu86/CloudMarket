import type { Product } from "./data/store";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "/").replace(/\/+$/, "");

type ApiProduct = {
  id: number;
  slug: string;
  title: string;
  subtitle: string;
  category: string;
  price: number;
  old_price: number | null;
  rating: number;
  reviews: number;
  badge: Product["badge"] | null;
  colors: string[];
  sizes: string[];
  image: string;
  thumbnails: string[];
  description: string;
};

export type AuthUser = {
  id: number;
  full_name: string;
  email: string;
  is_active: boolean;
};

export type AuthPayload = {
  access_token: string;
  token_type: string;
  user: AuthUser;
};

function mapApiProduct(product: ApiProduct): Product {
  return {
    id: product.id,
    slug: product.slug,
    title: product.title,
    subtitle: product.subtitle,
    category: product.category,
    price: product.price,
    oldPrice: product.old_price ?? undefined,
    rating: product.rating,
    reviews: product.reviews,
    badge: product.badge ?? undefined,
    colors: product.colors,
    sizes: product.sizes,
    image: product.image,
    thumbnails: product.thumbnails,
    description: product.description,
  };
}

function getStoredToken(): string | null {
  return localStorage.getItem("cloudmarket_token");
}

export function saveAuth(payload: AuthPayload): void {
  localStorage.setItem("cloudmarket_token", payload.access_token);
  localStorage.setItem("cloudmarket_user", JSON.stringify(payload.user));
}

export function clearAuth(): void {
  localStorage.removeItem("cloudmarket_token");
  localStorage.removeItem("cloudmarket_user");
}

export function getStoredUser(): AuthUser | null {
  const raw = localStorage.getItem("cloudmarket_user");
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw) as AuthUser;
  } catch {
    return null;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getStoredToken();
  const headers = new Headers(init?.headers);
  if (!headers.has("Content-Type") && init?.body) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
  });
  if (!response.ok) {
    let message = `Request failed: ${response.status}`;
    try {
      const errorData = (await response.json()) as { detail?: string };
      if (errorData.detail) {
        message = errorData.detail;
      }
    } catch {
      // ignore JSON parse issues for non-JSON errors
    }
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export const api = {
  getProducts: async (): Promise<Product[]> => {
    const data = await request<ApiProduct[]>("/api/products");
    return data.map(mapApiProduct);
  },

  getProductBySlug: async (slug: string): Promise<Product> => {
    const data = await request<ApiProduct>(`/api/products/${slug}`);
    return mapApiProduct(data);
  },

  register: async (payload: { full_name: string; email: string; password: string }): Promise<AuthPayload> => {
    return request<AuthPayload>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  login: async (payload: { email: string; password: string }): Promise<AuthPayload> => {
    return request<AuthPayload>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  getCurrentUser: async (): Promise<AuthUser> => {
    return request<AuthUser>("/api/auth/me");
  },
};
