import { arrow, bg, footer, node, rect, style, sub, text, title } from "./helpers.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, 3, "Пользовательский сценарий");
  title(slide, ctx, "Путь пользователя проходит от витрины до подтверждения заказа.", 82, 820, 34);
  const y = 282;
  const items = [
    ["Витрина", "главная страница и категории", style.teal],
    ["Каталог", "список товаров из API", style.amber],
    ["Карточка", "описание, цена, размеры", style.green],
    ["Корзина", "товары и сумма заказа", style.teal],
    ["Оплата", "создание заказа и redirect", style.amber],
  ];
  items.forEach((item, i) => {
    const x = 68 + i * 238;
    node(slide, ctx, item[0], item[1], x, y, 180, item[2]);
    if (i < items.length - 1) arrow(slide, ctx, x + 184, y + 46, 48, item[2]);
  });
  rect(slide, ctx, 120, 468, 420, 74, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Fallback-каталог", 146, 488, 220, 18, { size: 14, bold: true, color: style.teal });
  sub(slide, ctx, "Если API недоступно, интерфейс не пустеет: используются локальные данные из store.ts.", 146, 516, 350, 20, { size: 10.5 });
  rect(slide, ctx, 650, 468, 430, 74, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Авторизация", 676, 488, 220, 18, { size: 14, bold: true, color: style.amber });
  sub(slide, ctx, "Токен хранится на клиенте и передается в защищенные запросы через Authorization: Bearer.", 676, 516, 350, 20, { size: 10.5 });
  footer(slide, ctx, "Фронтенд: App.tsx, api.ts, useCatalog.ts");
  return slide;
}
