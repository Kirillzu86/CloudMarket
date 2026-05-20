import { bg, footer, line, node, rect, style, sub, text, title } from "./helpers.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, 5, "Backend");
  title(slide, ctx, "Бэкенд закрывает данные, пользователей, заказы и платежный контур.", 82, 880, 34);
  node(slide, ctx, "FastAPI", "Маршруты /api/products, /api/auth, /api/payments и /api/orders.", 74, 238, 300, style.teal);
  node(slide, ctx, "SQLAlchemy", "Модели User, Product, Category, Order и OrderItem.", 490, 238, 300, style.amber);
  node(slide, ctx, "SQLite", "Локальная база, автосоздание таблиц и seed-данные при старте.", 906, 238, 300, style.green);
  line(slide, ctx, 374, 286, 116, style.teal, 2);
  line(slide, ctx, 790, 286, 116, style.amber, 2);
  rect(slide, ctx, 106, 420, 474, 96, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Авторизация", 132, 444, 180, 20, { size: 15, bold: true, color: style.teal });
  sub(slide, ctx, "Регистрация, вход, хэширование пароля, access token и защищенный /api/auth/me.", 132, 476, 380, 22, { size: 11 });
  rect(slide, ctx, 700, 420, 474, 96, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Оплата", 726, 444, 180, 20, { size: 15, bold: true, color: style.amber });
  sub(slide, ctx, "Создание заказа, YooKassa confirmation_url и webhook для обновления статуса.", 726, 476, 380, 22, { size: 11 });
  footer(slide, ctx, "Бэкенд: main.py, crud.py, models.py, payments.py");
  return slide;
}
