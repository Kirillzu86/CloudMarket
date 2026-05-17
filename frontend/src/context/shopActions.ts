import { createContext } from "react";

export type ShopActionsContextValue = {
  wishlist: number[];
  cart: number[];
  addToWishlist: (productId: number) => void;
  removeFromWishlist: (productId: number) => void;
  toggleWishlist: (productId: number) => void;
  addToCart: (productId: number) => void;
  removeFromCart: (productId: number) => void;
  clearCart: () => void;
  isWishlisted: (productId: number) => boolean;
  isInCart: (productId: number) => boolean;
};

export const WISHLIST_KEY = "cloudmarket_wishlist";
export const CART_KEY = "cloudmarket_cart";

export const ShopActionsContext = createContext<ShopActionsContextValue | null>(null);

export function readStoredIds(key: string): number[] {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) {
      return [];
    }

    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed.filter((item): item is number => typeof item === "number");
  } catch {
    return [];
  }
}
