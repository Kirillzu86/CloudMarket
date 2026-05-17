import { useEffect, useMemo, useState, type ReactNode } from "react";

import { CART_KEY, readStoredIds, ShopActionsContext, type ShopActionsContextValue, WISHLIST_KEY } from "./shopActions";

export function ShopActionsProvider({ children }: { children: ReactNode }) {
  const [wishlist, setWishlist] = useState<number[]>(() => readStoredIds(WISHLIST_KEY));
  const [cart, setCart] = useState<number[]>(() => readStoredIds(CART_KEY));

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
      clearCart: () => {
        setCart([]);
      },
      isWishlisted: (productId) => wishlist.includes(productId),
      isInCart: (productId) => cart.includes(productId),
    }),
    [wishlist, cart],
  );

  return <ShopActionsContext.Provider value={value}>{children}</ShopActionsContext.Provider>;
}
