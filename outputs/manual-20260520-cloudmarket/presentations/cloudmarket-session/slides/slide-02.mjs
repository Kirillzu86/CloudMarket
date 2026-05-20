import { bg, footer, line, node, rect, style, sub, text, title } from "./helpers.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, 2, "Идея проекта");
  title(slide, ctx, "Проект решает понятную задачу: собрать интернет-магазин как единую систему.", 82, 910, 34);
  sub(slide, ctx, "Для сессии важно показать не набор отдельных страниц, а связанный пользовательский сценарий и серверную часть, которая этот сценарий обслуживает.", 62, 180, 820, 46, { size: 14 });
  node(slide, ctx, "Пользователь", "Смотрит товары, открывает карточку, добавляет в корзину и избранное.", 70, 292, 310, style.teal);
  node(slide, ctx, "Интерфейс", "React-компоненты и маршруты собирают витрину, каталог и личные разделы.", 486, 292, 310, style.amber);
  node(slide, ctx, "Сервер", "FastAPI отдает товары, регистрирует пользователей и создает заказы.", 902, 292, 310, style.green);
  line(slide, ctx, 380, 338, 106, style.teal, 2);
  line(slide, ctx, 796, 338, 106, style.amber, 2);
  rect(slide, ctx, 126, 468, 1026, 86, style.dark);
  text(slide, ctx, "Главная мысль для защиты", 160, 488, 230, 22, { size: 12, color: "#CBD5E1", bold: true });
  text(slide, ctx, "CloudMarket демонстрирует практическую fullstack-разработку: клиент, API, база данных, авторизация и платежный контур работают как части одной архитектуры.", 160, 518, 930, 26, { size: 16, color: style.white, bold: true });
  footer(slide, ctx);
  return slide;
}
