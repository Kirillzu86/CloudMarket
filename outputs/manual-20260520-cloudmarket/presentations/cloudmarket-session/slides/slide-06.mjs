import { bg, footer, line, rect, style, sub, text, title } from "./helpers.mjs";

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, 6, "API и данные");
  title(slide, ctx, "API показывает, как интерфейс связан с серверной логикой.", 82, 840, 34);
  const rows = [
    ["GET", "/api/products", "получить каталог"],
    ["GET", "/api/products/{slug}", "открыть карточку товара"],
    ["POST", "/api/auth/register", "создать пользователя"],
    ["POST", "/api/auth/login", "получить токен входа"],
    ["POST", "/api/payments", "создать заказ и платеж"],
    ["GET", "/api/orders/{order_id}", "прочитать статус заказа"],
  ];
  rect(slide, ctx, 72, 216, 650, 300, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Метод", 100, 244, 80, 18, { size: 10, bold: true, color: style.muted });
  text(slide, ctx, "Endpoint", 208, 244, 250, 18, { size: 10, bold: true, color: style.muted });
  text(slide, ctx, "Зачем нужен", 474, 244, 170, 18, { size: 10, bold: true, color: style.muted });
  rows.forEach((row, i) => {
    const y = 286 + i * 36;
    line(slide, ctx, 100, y - 10, 574, style.line, 1);
    text(slide, ctx, row[0], 100, y, 70, 16, { size: 10, bold: true, color: row[0] === "GET" ? style.teal : style.amber });
    text(slide, ctx, row[1], 208, y, 240, 16, { size: 10.5, color: style.ink });
    text(slide, ctx, row[2], 474, y, 190, 16, { size: 10, color: style.muted });
  });
  rect(slide, ctx, 818, 216, 318, 300, style.dark);
  text(slide, ctx, "Модель данных", 850, 246, 230, 24, { size: 22, face: style.serif, bold: true, color: style.white });
  sub(slide, ctx, "User\nProduct\nCategory\nProductImage\nProductSize\nOrder\nOrderItem", 850, 304, 170, 160, { size: 17, color: "#DDE7F2" });
  rect(slide, ctx, 1024, 338, 62, 62, style.teal);
  rect(slide, ctx, 1058, 374, 62, 62, style.amber);
  footer(slide, ctx, "README.md: список публичных API endpoints");
  return slide;
}
