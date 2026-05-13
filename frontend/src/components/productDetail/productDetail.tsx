import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { Link, useParams } from "react-router-dom";

import { getStoredUser } from "../../api";
import { useShopActions } from "../../context/useShopActions";
import { products as fallbackProducts } from "../../data/store";
import { useCatalogProduct, useCatalogProducts } from "../../hooks/useCatalog";
import Card from "../shop/cards/card";
import "./productDetail.css";

type ProductComment = {
  id: string;
  author: string;
  text: string;
  createdAt: string;
};

export default function ProductDetailsPage() {
  const { slug } = useParams();
  const { product, error } = useCatalogProduct(slug);
  const { products } = useCatalogProducts();
  const { addToCart, toggleWishlist, isInCart, isWishlisted } = useShopActions();
  const [comments, setComments] = useState<ProductComment[]>([]);
  const [commentText, setCommentText] = useState("");
  const storedUser = useMemo(() => getStoredUser(), []);
  const commentsStorageKey = `cloudmarket_product_comments_${product.id}`;
  const relatedProducts = (products.length > 0 ? products : fallbackProducts)
    .filter((item) => item.id !== product.id)
    .slice(0, 3);

  useEffect(() => {
    const savedComments = localStorage.getItem(commentsStorageKey);
    if (!savedComments) {
      setComments([]);
      return;
    }

    try {
      setComments(JSON.parse(savedComments) as ProductComment[]);
    } catch {
      setComments([]);
    }
  }, [commentsStorageKey]);

  function handleCommentSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedText = commentText.trim();
    if (!trimmedText) {
      return;
    }

    const nextComments = [
      {
        id: crypto.randomUUID(),
        author: storedUser?.full_name || "Guest customer",
        text: trimmedText,
        createdAt: new Date().toISOString(),
      },
      ...comments,
    ];

    setComments(nextComments);
    localStorage.setItem(commentsStorageKey, JSON.stringify(nextComments));
    setCommentText("");
  }

  return (
    <main className="product-page">
      <section className="product-section">
        <div className="site-shell product-layout">
          <div className="product-gallery">
            <div className="product-gallery__main">
              <img src={product.image} alt={product.title} className="product-gallery__image" />
            </div>
            <div className="product-gallery__thumbs">
              {product.thumbnails.map((thumb, index) => (
                <img
                  key={`${product.id}-${index}`}
                  src={thumb}
                  alt={`${product.title} ${index + 1}`}
                  className="product-gallery__thumb"
                />
              ))}
            </div>
          </div>

          <div className="product-info">
            {error ? <p className="catalog-status">Using local product fallback.</p> : null}
            <p className="section-label">{product.category}</p>
            <h1 className="product-info__title">{product.title}</h1>
            <p className="product-info__subtitle">{product.description}</p>

            <div className="product-info__rating">Rating {product.rating} / 5 - {product.reviews} reviews</div>

            <div className="product-info__price">
              <span className="product-info__price-current">${product.price}</span>
              {product.oldPrice ? <span className="card-price-original">${product.oldPrice}</span> : null}
            </div>

            <div className="product-info__group">
              <span className="product-info__label">Color</span>
              <div className="product-swatches">
                {product.colors.map((color) => (
                  <span key={color} className="product-swatch" style={{ backgroundColor: color }} />
                ))}
              </div>
            </div>

            <div className="product-info__group">
              <span className="product-info__label">Size</span>
              <div className="product-sizes">
                {product.sizes.map((size) => (
                  <button
                    key={size}
                    type="button"
                    className={`product-size${size === "M" ? " product-size--active" : ""}`}
                  >
                    {size}
                  </button>
                ))}
              </div>
            </div>

            <div className="product-actions product-actions--detail">
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => addToCart(product.id)}
              >
                {isInCart(product.id) ? "Added to cart" : "Add to cart"}
              </button>
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => toggleWishlist(product.id)}
              >
                {isWishlisted(product.id) ? "Saved in wishlist" : "Save to wishlist"}
              </button>
            </div>

            <div className="product-benefits">
              <div><strong>Free shipping</strong><span>Orders over $120</span></div>
              <div><strong>Easy return</strong><span>Within 14 days</span></div>
              <div><strong>Secure checkout</strong><span>Stripe and PayPal supported</span></div>
            </div>
          </div>
        </div>
      </section>

      <section className="comments-section">
        <div className="site-shell comments-section__inner">
          <div className="section-heading-row">
            <div>
              <p className="section-label">Customer comments</p>
              <h2>Comments for {product.title}</h2>
            </div>
            <span className="comments-count">{comments.length} comments</span>
          </div>

          <form className="comment-form" onSubmit={handleCommentSubmit}>
            <label className="comment-form__label" htmlFor="product-comment">
              Your comment
            </label>
            <textarea
              id="product-comment"
              className="comment-form__field"
              value={commentText}
              onChange={(event) => setCommentText(event.target.value)}
              placeholder="Share what you think about this product"
              rows={4}
              maxLength={600}
            />
            <div className="comment-form__footer">
              <span>{commentText.trim().length}/600</span>
              <button type="submit" className="btn btn-primary" disabled={!commentText.trim()}>
                Add comment
              </button>
            </div>
          </form>

          <div className="comments-list">
            {comments.length > 0 ? (
              comments.map((comment) => (
                <article className="comment-item" key={comment.id}>
                  <div className="comment-item__header">
                    <strong>{comment.author}</strong>
                    <time dateTime={comment.createdAt}>
                      {new Intl.DateTimeFormat("en", {
                        day: "numeric",
                        month: "short",
                        year: "numeric",
                      }).format(new Date(comment.createdAt))}
                    </time>
                  </div>
                  <p>{comment.text}</p>
                </article>
              ))
            ) : (
              <p className="comments-empty">No comments yet. Be the first to write one.</p>
            )}
          </div>
        </div>
      </section>

      <section className="related-section">
        <div className="site-shell related-section__inner">
          <div className="section-heading-row">
            <div>
              <p className="section-label">You may also like</p>
              <h2>Related products</h2>
            </div>
            <Link to="/products" className="section-link">Back to catalog</Link>
          </div>
          <Card items={relatedProducts} />
        </div>
      </section>
    </main>
  );
}
