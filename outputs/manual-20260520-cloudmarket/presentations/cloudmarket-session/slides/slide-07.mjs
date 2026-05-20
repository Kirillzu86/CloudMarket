import { bg, footer, node, rect, style, sub, text, title } from "./helpers.mjs";

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, 7, "Запуск и деплой");
  title(slide, ctx, "Проект подготовлен к локальному запуску и контейнерному деплою.", 82, 860, 34);
  node(slide, ctx, "Локально", "Backend: uvicorn на 8000. Frontend: Vite dev server с VITE_API_BASE_URL.", 84, 246, 320, style.teal);
  node(slide, ctx, "Docker", "Отдельные Dockerfile для backend и frontend; nginx проксирует /api/*.", 480, 246, 320, style.amber);
  node(slide, ctx, "Coolify", "Два сервиса, persistent storage для /app/data и переменные окружения.", 876, 246, 320, style.green);
  rect(slide, ctx, 150, 430, 982, 88, style.cream, { lineColor: style.line, weight: 1 });
  text(slide, ctx, "Конфигурация вынесена наружу", 184, 454, 300, 20, { size: 15, bold: true, color: style.teal });
  sub(slide, ctx, "DATABASE_URL, CLOUDMARKET_DATA_DIR, CLOUDMARKET_ALLOWED_ORIGINS, FRONTEND_BASE_URL, YOOKASSA_SHOP_ID и YOOKASSA_SECRET_KEY позволяют менять окружение без изменения кода.", 184, 488, 860, 24, { size: 11.5 });
  footer(slide, ctx, "README.md и Dockerfile: production notes + Coolify deployment");
  return slide;
}
