import { bg, footer, line, node, rect, style, sub, text, title } from "./helpers.mjs";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, 4, "Frontend");
  title(slide, ctx, "Фронтенд разделен на маршруты, компоненты и общий API-клиент.", 82, 840, 34);
  rect(slide, ctx, 72, 230, 280, 310, style.dark);
  text(slide, ctx, "React Router", 102, 262, 210, 28, { size: 22, face: style.serif, bold: true, color: style.white });
  sub(slide, ctx, "/\n/products\n/products/:slug\n/login\n/register\n/cart\n/wishlist\n/payment/success", 106, 318, 190, 170, { size: 16, color: "#DDE7F2" });
  node(slide, ctx, "Компоненты", "Shop, ProductsPage, ProductDetails, Cart, Wishlist, Login/Register.", 430, 226, 320, style.teal);
  node(slide, ctx, "Состояние действий", "ShopActionsProvider объединяет действия магазина в одном контексте.", 430, 350, 320, style.amber);
  node(slide, ctx, "API-клиент", "api.ts мапит серверные DTO в тип Product и добавляет токен авторизации.", 430, 474, 320, style.green);
  rect(slide, ctx, 848, 226, 300, 310, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Почему это удобно", 880, 256, 230, 28, { size: 22, face: style.serif, bold: true });
  line(slide, ctx, 880, 304, 210, style.line, 1);
  sub(slide, ctx, "1. Каждая страница отвечает за свой экран.\n2. API скрыт за одной прослойкой.\n3. Типы TypeScript уменьшают риск ошибок.\n4. Fallback делает каталог устойчивее.", 882, 332, 220, 130, { size: 13, color: style.ink });
  footer(slide, ctx, "Фронтенд: React 19, Vite 7, TypeScript, React Router");
  return slide;
}
