import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";

import { api, type Order } from "../../api";
import { useShopActions } from "../../context/useShopActions";
import "./paymentSuccess.css";

export default function PaymentSuccess() {
  const [searchParams] = useSearchParams();
  const orderId = useMemo(() => Number(searchParams.get("order_id")), [searchParams]);
  const { clearCart } = useShopActions();
  const [order, setOrder] = useState<Order | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!Number.isFinite(orderId) || orderId <= 0) {
      setError("Order was not found in the payment return URL.");
      setIsLoading(false);
      return;
    }

    api
      .getOrder(orderId)
      .then((data) => {
        setOrder(data);
        if (data.status === "paid" || data.status === "succeeded") {
          clearCart();
        }
      })
      .catch((requestError) => {
        setError(requestError instanceof Error ? requestError.message : "Unable to load order");
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [clearCart, orderId]);

  return (
    <main className="payment-page">
      <section className="payment-section">
        <div className="site-shell payment-layout">
          <div className="payment-panel">
            <p className="section-label">Checkout</p>
            <h1>{order?.status === "paid" ? "Payment received" : "Payment is being checked"}</h1>
            {isLoading ? <p>Loading your order...</p> : null}
            {error ? <p className="payment-error">{error}</p> : null}
            {order ? (
              <>
                <div className="payment-status">
                  <span>Order #{order.id}</span>
                  <strong>{order.status}</strong>
                </div>
                <div className="payment-status">
                  <span>Total</span>
                  <strong>
                    {order.total_amount} {order.currency}
                  </strong>
                </div>
                <div className="payment-actions">
                  <Link className="btn btn-primary" to="/products">
                    Continue shopping
                  </Link>
                  {order.confirmation_url && order.status !== "paid" ? (
                    <a className="btn btn-secondary" href={order.confirmation_url}>
                      Return to payment
                    </a>
                  ) : null}
                </div>
              </>
            ) : null}
          </div>
        </div>
      </section>
    </main>
  );
}
