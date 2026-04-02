import { useContext } from "react";

import { ShopActionsContext } from "./shopActions";

export function useShopActions() {
  const context = useContext(ShopActionsContext);
  if (!context) {
    throw new Error("useShopActions must be used within ShopActionsProvider");
  }
  return context;
}
