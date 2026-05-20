import { bg, footer, line, rect, style, sub, text, title } from "./helpers.mjs";

export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, 8, "Итог");
  title(slide, ctx, "CloudMarket показывает полный набор практических fullstack-навыков.", 82, 860, 34);
  rect(slide, ctx, 78, 232, 340, 254, style.dark);
  text(slide, ctx, "Что уже есть", 112, 262, 220, 28, { size: 24, face: style.serif, bold: true, color: style.white });
  sub(slide, ctx, "Каталог\nДетальная страница\nРегистрация и вход\nКорзина и избранное\nЗаказы и платежный сценарий", 114, 320, 240, 132, { size: 16, color: "#DDE7F2" });
  rect(slide, ctx, 500, 232, 340, 254, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Что доказано", 534, 262, 220, 28, { size: 24, face: style.serif, bold: true });
  sub(slide, ctx, "Разделение ответственности\nРабота с API и БД\nТипизация данных\nАвторизация\nГотовность к деплою", 536, 320, 240, 132, { size: 16, color: style.ink });
  rect(slide, ctx, 922, 232, 260, 254, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Дальше", 956, 262, 180, 28, { size: 24, face: style.serif, bold: true, color: style.teal });
  sub(slide, ctx, "Фильтры\nИстория заказов\nАдмин-панель\nРасширенная оплата\nТесты", 958, 320, 160, 132, { size: 16, color: style.ink });
  line(slide, ctx, 78, 560, 1104, style.line, 1);
  text(slide, ctx, "Финальная фраза", 84, 590, 160, 18, { size: 10, bold: true, color: style.muted });
  text(slide, ctx, "Это не отдельная страница, а учебная e-commerce система с понятной архитектурой и точками роста.", 250, 582, 820, 30, { size: 18, bold: true, color: style.ink });
  footer(slide, ctx, "Материалы для речи: папка «Сессия»");
  return slide;
}
