import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

type ShopActionsContextValue = {
  wishlist: number[];
  cart: number[];
  addToWishlist: (productId: number) => void;
  removeFromWishlist: (productId: number) => void;
  toggleWishlist: (productId: number) => void;
  addToCart: (productId: number) => void;
  removeFromCart: (productId: number) => void;
  isWishlisted: (productId: number) => boolean;
  isInCart: (productId: number) => boolean;
};

const WISHLIST_KEY = "cloudmarket_wishlist";
const CART_KEY = "cloudmarket_cart";

const ShopActionsContext = createContext<ShopActionsContextValue | null>(null);

function readStoredIds(key: string): number[] {
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

export function ShopActionsProvider({ children }: { children: ReactNode }) {
  const [wishlist, setWishlist] = useState<number[]>([]);
  const [cart, setCart] = useState<number[]>([]);

  useEffect(() => {
    setWishlist(readStoredIds(WISHLIST_KEY));
    setCart(readStoredIds(CART_KEY));
  }, []);

  useEffect(() => {
    localStorage.setItem(WISHLIST_KEY, JSON.stringify(wishlist));
  }, [wishlist]);

  useEffect(() => {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
  }, [cart]);

  const value = useMemo<ShopActionsContextValue>(
    () => ({
      wishlist,
      cart,
      addToWishlist: (productId) => {
        setWishlist((current) => (current.includes(productId) ? current : [...current, productId]));
      },
      removeFromWishlist: (productId) => {
        setWishlist((current) => current.filter((id) => id !== productId));
      },
      toggleWishlist: (productId) => {
        setWishlist((current) =>
          current.includes(productId)
            ? current.filter((id) => id !== productId)
            : [...current, productId],
        );
      },
      addToCart: (productId) => {
        setCart((current) => [...current, productId]);
      },
      removeFromCart: (productId) => {
        setCart((current) => {
          const next = [...current];
          const index = next.indexOf(productId);
          if (index >= 0) {
            next.splice(index, 1);
          }
          return next;
        });
      },
      isWishlisted: (productId) => wishlist.includes(productId),
      isInCart: (productId) => cart.includes(productId),
    }),
    [wishlist, cart],
  );

  return <ShopActionsContext.Provider value={value}>{children}</ShopActionsContext.Provider>;
}

export function useShopActions() {
  const context = useContext(ShopActionsContext);
  if (!context) {
    throw new Error("useShopActions must be used within ShopActionsProvider");
  }
  return context;
}
