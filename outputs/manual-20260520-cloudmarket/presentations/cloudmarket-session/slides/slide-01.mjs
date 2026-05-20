import { bg, footer, line, node, pill, rect, style, sub, text } from "./helpers.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, 1, "Сессия / fullstack проект");
  rect(slide, ctx, 760, 0, 520, 720, style.dark);
  rect(slide, ctx, 842, 112, 286, 410, "#223044");
  rect(slide, ctx, 874, 144, 222, 24, style.cream);
  rect(slide, ctx, 874, 190, 86, 122, style.teal);
  rect(slide, ctx, 982, 190, 114, 122, style.amber);
  rect(slide, ctx, 874, 334, 222, 26, "#FFFFFF");
  rect(slide, ctx, 874, 386, 222, 26, "#FFFFFF");
  rect(slide, ctx, 916, 456, 138, 34, style.green);
  text(slide, ctx, "CloudMarket", 58, 158, 620, 74, {
    size: 58,
    face: style.serif,
    bold: true,
  });
  text(slide, ctx, "Интернет-магазин на React, FastAPI и SQLite", 62, 248, 545, 42, {
    size: 24,
    color: style.teal,
    bold: true,
  });
  sub(slide, ctx, "Учебный fullstack-проект: витрина товаров, каталог, авторизация, корзина, избранное, заказы и интеграция платежного сценария.", 62, 318, 570, 78, { size: 16 });
  pill(slide, ctx, "React + Vite + TypeScript", 62, 442, 210, style.teal);
  pill(slide, ctx, "FastAPI + SQLAlchemy", 292, 442, 190, style.amber);
  pill(slide, ctx, "SQLite + Docker", 502, 442, 150, style.green);
  node(slide, ctx, "Цель", "Показать полный цикл веб-приложения: интерфейс, API, база данных и деплой.", 62, 532, 520, style.teal);
  footer(slide, ctx, "CloudMarket: монорепозиторий frontend + backend");
  return slide;
}
