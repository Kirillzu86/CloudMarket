from __future__ import annotations

import html
import zipfile
from pathlib import Path


OUT = Path(__file__).resolve().parent / "output" / "CloudMarket-session.pptx"
EMU = 914400
SLIDE_W = 13.333
SLIDE_H = 7.5
CX = int(SLIDE_W * EMU)
CY = int(SLIDE_H * EMU)

COLORS = {
    "bg": "F6F1E8",
    "ink": "111827",
    "muted": "64748B",
    "line": "D5C8B8",
    "teal": "176B87",
    "amber": "C47F2C",
    "green": "2F7D5B",
    "dark": "101827",
    "white": "FFFFFF",
    "cream": "FFF9F0",
    "slate": "223044",
    "pale": "DDE7F2",
}


def emu(value: float) -> int:
    return int(value * EMU)


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def fill_xml(color: str) -> str:
    return f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'


def line_xml(color: str | None = None, width: int = 0) -> str:
    if not color or width <= 0:
        return '<a:ln><a:noFill/></a:ln>'
    return f'<a:ln w="{width}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln>'


def tx_paragraph(line: str, size: int, color: str, bold: bool, font: str, align: str) -> str:
    b = ' b="1"' if bold else ""
    return (
        f'<a:p><a:pPr algn="{align}"/>'
        f'<a:r><a:rPr lang="ru-RU" sz="{size * 100}"{b}>'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="{esc(font)}"/><a:cs typeface="{esc(font)}"/>'
        f'</a:rPr><a:t>{esc(line)}</a:t></a:r><a:endParaRPr lang="ru-RU" sz="{size * 100}"/></a:p>'
    )


class Slide:
    def __init__(self, number: int, label: str):
        self.number = number
        self.shapes: list[str] = []
        self.shape_id = 2
        self.rect(0, 0, SLIDE_W, SLIDE_H, COLORS["bg"])
        self.rect(0, 0, SLIDE_W, 0.18, COLORS["dark"])
        self.rect(0.44, 0.45, 0.08, 0.08, COLORS["teal"] if number % 2 else COLORS["amber"])
        self.text(label.upper(), 0.61, 0.39, 3.1, 0.22, 9, COLORS["muted"], bold=True)
        self.text(f"{number:02}", 12.35, 6.91, 0.55, 0.2, 10, COLORS["muted"], bold=True, align="r")

    def next_id(self) -> int:
        self.shape_id += 1
        return self.shape_id

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        color: str,
        line_color: str | None = None,
        line_width: int = 0,
    ) -> None:
        sid = self.next_id()
        self.shapes.append(
            f"""
            <p:sp>
              <p:nvSpPr><p:cNvPr id="{sid}" name="Shape {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
              <p:spPr>
                <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                {fill_xml(color)}
                {line_xml(line_color, line_width)}
              </p:spPr>
            </p:sp>
            """
        )

    def text(
        self,
        value: str,
        x: float,
        y: float,
        w: float,
        h: float,
        size: int,
        color: str = COLORS["ink"],
        bold: bool = False,
        font: str = "Arial",
        align: str = "l",
        fill: str | None = None,
    ) -> None:
        sid = self.next_id()
        paragraphs = "".join(
            tx_paragraph(line if line else " ", size, color, bold, font, align)
            for line in str(value).split("\n")
        )
        fill_part = fill_xml(fill) if fill else "<a:noFill/>"
        self.shapes.append(
            f"""
            <p:sp>
              <p:nvSpPr><p:cNvPr id="{sid}" name="TextBox {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
              <p:spPr>
                <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                {fill_part}
                <a:ln><a:noFill/></a:ln>
              </p:spPr>
              <p:txBody>
                <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0"/>
                <a:lstStyle/>
                {paragraphs}
              </p:txBody>
            </p:sp>
            """
        )

    def rule(self, x: float, y: float, w: float, color: str = COLORS["line"], h: float = 0.02) -> None:
        self.rect(x, y, w, h, color)

    def node(self, title: str, note: str, x: float, y: float, w: float, color: str) -> None:
        self.rect(x, y, w, 0.96, COLORS["cream"], COLORS["line"], 9000)
        self.rect(x, y, 0.06, 0.96, color)
        self.text(title, x + 0.18, y + 0.16, w - 0.32, 0.24, 15, COLORS["ink"], bold=True)
        self.text(note, x + 0.18, y + 0.50, w - 0.32, 0.34, 10, COLORS["muted"])

    def footer(self, note: str = "Источник: код проекта CloudMarket") -> None:
        self.rule(0.6, 6.65, 11.05)
        self.text(note, 0.6, 6.88, 7.5, 0.2, 8, COLORS["muted"])

    def title(self, value: str, y: float = 0.86, w: float = 8.8, size: int = 34) -> None:
        self.text(value, 0.6, y, w, 0.95, size, COLORS["ink"], bold=True, font="Georgia")

    def xml(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/><a:chOff x="0" y="0"/><a:chExt cx="{CX}" cy="{CY}"/></a:xfrm></p:grpSpPr>
      {''.join(self.shapes)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def build_slides() -> list[Slide]:
    slides: list[Slide] = []

    s = Slide(1, "Сессия / fullstack проект")
    s.rect(7.92, 0, 5.41, 7.5, COLORS["dark"])
    s.rect(8.78, 1.16, 2.98, 4.28, COLORS["slate"])
    s.rect(9.12, 1.50, 2.32, 0.25, COLORS["cream"])
    s.rect(9.12, 1.98, 0.9, 1.27, COLORS["teal"])
    s.rect(10.24, 1.98, 1.18, 1.27, COLORS["amber"])
    s.rect(9.12, 3.48, 2.32, 0.27, COLORS["white"])
    s.rect(9.12, 4.02, 2.32, 0.27, COLORS["white"])
    s.rect(9.56, 4.75, 1.44, 0.35, COLORS["green"])
    s.text("CloudMarket", 0.6, 1.65, 6.5, 0.8, 54, COLORS["ink"], bold=True, font="Georgia")
    s.text("Интернет-магазин на React, FastAPI и SQLite", 0.65, 2.58, 5.7, 0.44, 22, COLORS["teal"], bold=True)
    s.text("Учебный fullstack-проект: витрина товаров, каталог, авторизация, корзина, избранное, заказы и интеграция платежного сценария.", 0.65, 3.32, 5.9, 0.7, 15, COLORS["muted"])
    for x, t, c, w in [
        (0.65, "React + Vite + TypeScript", COLORS["teal"], 2.3),
        (3.08, "FastAPI + SQLAlchemy", COLORS["amber"], 2.05),
        (5.3, "SQLite + Docker", COLORS["green"], 1.62),
    ]:
        s.rect(x, 4.6, w, 0.34, COLORS["white"], c, 9000)
        s.text(t, x + 0.08, 4.69, w - 0.16, 0.12, 9, c, bold=True, align="ctr")
    s.node("Цель", "Показать полный цикл веб-приложения: интерфейс, API, база данных и деплой.", 0.65, 5.55, 5.4, COLORS["teal"])
    s.footer("CloudMarket: монорепозиторий frontend + backend")
    slides.append(s)

    s = Slide(2, "Идея проекта")
    s.title("Проект решает понятную задачу: собрать интернет-магазин как единую систему.", w=9.5)
    s.text("Для сессии важно показать не набор отдельных страниц, а связанный пользовательский сценарий и серверную часть, которая этот сценарий обслуживает.", 0.65, 1.86, 8.6, 0.5, 13, COLORS["muted"])
    s.node("Пользователь", "Смотрит товары, открывает карточку, добавляет в корзину и избранное.", 0.72, 3.04, 3.2, COLORS["teal"])
    s.node("Интерфейс", "React-компоненты и маршруты собирают витрину, каталог и личные разделы.", 5.05, 3.04, 3.2, COLORS["amber"])
    s.node("Сервер", "FastAPI отдает товары, регистрирует пользователей и создает заказы.", 9.38, 3.04, 3.2, COLORS["green"])
    s.rule(3.92, 3.52, 1.1, COLORS["teal"])
    s.rule(8.25, 3.52, 1.1, COLORS["amber"])
    s.rect(1.25, 4.9, 10.7, 0.9, COLORS["dark"])
    s.text("Главная мысль для защиты", 1.66, 5.1, 2.4, 0.24, 11, "CBD5E1", bold=True)
    s.text("CloudMarket демонстрирует практическую fullstack-разработку: клиент, API, база данных, авторизация и платежный контур работают как части одной архитектуры.", 1.66, 5.42, 9.6, 0.28, 15, COLORS["white"], bold=True)
    s.footer()
    slides.append(s)

    s = Slide(3, "Пользовательский сценарий")
    s.title("Путь пользователя проходит от витрины до подтверждения заказа.", w=8.6)
    flow = [
        ("Витрина", "главная страница и категории", COLORS["teal"]),
        ("Каталог", "список товаров из API", COLORS["amber"]),
        ("Карточка", "описание, цена, размеры", COLORS["green"]),
        ("Корзина", "товары и сумма заказа", COLORS["teal"]),
        ("Оплата", "создание заказа и redirect", COLORS["amber"]),
    ]
    for i, (head, note, color) in enumerate(flow):
        x = 0.72 + i * 2.47
        s.node(head, note, x, 2.92, 1.9, color)
        if i < len(flow) - 1:
            s.rule(x + 1.92, 3.40, 0.48, color)
    s.rect(1.25, 4.88, 4.4, 0.78, COLORS["cream"], COLORS["line"], 9000)
    s.text("Fallback-каталог", 1.52, 5.08, 2.2, 0.2, 14, COLORS["teal"], bold=True)
    s.text("Если API недоступно, интерфейс не пустеет: используются локальные данные из store.ts.", 1.52, 5.38, 3.6, 0.22, 10, COLORS["muted"])
    s.rect(6.77, 4.88, 4.45, 0.78, COLORS["cream"], COLORS["line"], 9000)
    s.text("Авторизация", 7.04, 5.08, 2.0, 0.2, 14, COLORS["amber"], bold=True)
    s.text("Токен хранится на клиенте и передается в защищенные запросы через Authorization: Bearer.", 7.04, 5.38, 3.7, 0.22, 10, COLORS["muted"])
    s.footer("Фронтенд: App.tsx, api.ts, useCatalog.ts")
    slides.append(s)

    s = Slide(4, "Frontend")
    s.title("Фронтенд разделен на маршруты, компоненты и общий API-клиент.", w=8.8)
    s.rect(0.75, 2.36, 2.92, 3.22, COLORS["dark"])
    s.text("React Router", 1.06, 2.73, 2.2, 0.32, 22, COLORS["white"], bold=True, font="Georgia")
    s.text("/\n/products\n/products/:slug\n/login\n/register\n/cart\n/wishlist\n/payment/success", 1.1, 3.32, 2.0, 1.78, 15, COLORS["pale"])
    s.node("Компоненты", "Shop, ProductsPage, ProductDetails, Cart, Wishlist, Login/Register.", 4.48, 2.36, 3.32, COLORS["teal"])
    s.node("Состояние действий", "ShopActionsProvider объединяет действия магазина в одном контексте.", 4.48, 3.65, 3.32, COLORS["amber"])
    s.node("API-клиент", "api.ts мапит серверные DTO в тип Product и добавляет токен авторизации.", 4.48, 4.95, 3.32, COLORS["green"])
    s.rect(8.82, 2.36, 3.12, 3.22, COLORS["cream"], COLORS["line"], 9000)
    s.text("Почему это удобно", 9.15, 2.68, 2.4, 0.3, 22, COLORS["ink"], bold=True, font="Georgia")
    s.rule(9.15, 3.18, 2.2)
    s.text("1. Каждая страница отвечает за свой экран.\n2. API скрыт за одной прослойкой.\n3. Типы TypeScript уменьшают риск ошибок.\n4. Fallback делает каталог устойчивее.", 9.16, 3.46, 2.32, 1.4, 12, COLORS["ink"])
    s.footer("Фронтенд: React 19, Vite 7, TypeScript, React Router")
    slides.append(s)

    s = Slide(5, "Backend")
    s.title("Бэкенд закрывает данные, пользователей, заказы и платежный контур.", w=9.2)
    s.node("FastAPI", "Маршруты /api/products, /api/auth, /api/payments и /api/orders.", 0.77, 2.48, 3.12, COLORS["teal"])
    s.node("SQLAlchemy", "Модели User, Product, Category, Order и OrderItem.", 5.10, 2.48, 3.12, COLORS["amber"])
    s.node("SQLite", "Локальная база, автосоздание таблиц и seed-данные при старте.", 9.44, 2.48, 3.12, COLORS["green"])
    s.rule(3.89, 2.98, 1.2, COLORS["teal"])
    s.rule(8.22, 2.98, 1.2, COLORS["amber"])
    s.rect(1.1, 4.38, 4.94, 1.0, COLORS["cream"], COLORS["line"], 9000)
    s.text("Авторизация", 1.38, 4.64, 1.9, 0.2, 15, COLORS["teal"], bold=True)
    s.text("Регистрация, вход, хэширование пароля, access token и защищенный /api/auth/me.", 1.38, 4.98, 4.0, 0.24, 10, COLORS["muted"])
    s.rect(7.28, 4.38, 4.94, 1.0, COLORS["cream"], COLORS["line"], 9000)
    s.text("Оплата", 7.56, 4.64, 1.9, 0.2, 15, COLORS["amber"], bold=True)
    s.text("Создание заказа, YooKassa confirmation_url и webhook для обновления статуса.", 7.56, 4.98, 4.0, 0.24, 10, COLORS["muted"])
    s.footer("Бэкенд: main.py, crud.py, models.py, payments.py")
    slides.append(s)

    s = Slide(6, "API и данные")
    s.title("API показывает, как интерфейс связан с серверной логикой.", w=8.7)
    s.rect(0.75, 2.25, 6.77, 3.12, COLORS["cream"], COLORS["line"], 9000)
    s.text("Метод", 1.04, 2.54, 0.8, 0.18, 10, COLORS["muted"], bold=True)
    s.text("Endpoint", 2.16, 2.54, 2.6, 0.18, 10, COLORS["muted"], bold=True)
    s.text("Зачем нужен", 4.95, 2.54, 1.8, 0.18, 10, COLORS["muted"], bold=True)
    rows = [
        ("GET", "/api/products", "получить каталог"),
        ("GET", "/api/products/{slug}", "открыть карточку товара"),
        ("POST", "/api/auth/register", "создать пользователя"),
        ("POST", "/api/auth/login", "получить токен входа"),
        ("POST", "/api/payments", "создать заказ и платеж"),
        ("GET", "/api/orders/{order_id}", "прочитать статус заказа"),
    ]
    for i, (method, path, why) in enumerate(rows):
        y = 2.98 + i * 0.38
        s.rule(1.04, y - 0.10, 5.98)
        s.text(method, 1.04, y, 0.7, 0.16, 10, COLORS["teal"] if method == "GET" else COLORS["amber"], bold=True)
        s.text(path, 2.16, y, 2.5, 0.16, 10, COLORS["ink"])
        s.text(why, 4.95, y, 1.9, 0.16, 10, COLORS["muted"])
    s.rect(8.52, 2.25, 3.3, 3.12, COLORS["dark"])
    s.text("Модель данных", 8.85, 2.56, 2.4, 0.28, 22, COLORS["white"], bold=True, font="Georgia")
    s.text("User\nProduct\nCategory\nProductImage\nProductSize\nOrder\nOrderItem", 8.85, 3.16, 1.8, 1.65, 16, COLORS["pale"])
    s.rect(10.65, 3.52, 0.65, 0.65, COLORS["teal"])
    s.rect(11.0, 3.9, 0.65, 0.65, COLORS["amber"])
    s.footer("README.md: список публичных API endpoints")
    slides.append(s)

    s = Slide(7, "Запуск и деплой")
    s.title("Проект подготовлен к локальному запуску и контейнерному деплою.", w=9.0)
    s.node("Локально", "Backend: uvicorn на 8000. Frontend: Vite dev server с VITE_API_BASE_URL.", 0.87, 2.56, 3.33, COLORS["teal"])
    s.node("Docker", "Отдельные Dockerfile для backend и frontend; nginx проксирует /api/*.", 5.0, 2.56, 3.33, COLORS["amber"])
    s.node("Coolify", "Два сервиса, persistent storage для /app/data и переменные окружения.", 9.12, 2.56, 3.33, COLORS["green"])
    s.rect(1.56, 4.48, 10.23, 0.92, COLORS["cream"], COLORS["line"], 9000)
    s.text("Конфигурация вынесена наружу", 1.92, 4.72, 3.2, 0.2, 15, COLORS["teal"], bold=True)
    s.text("DATABASE_URL, CLOUDMARKET_DATA_DIR, CLOUDMARKET_ALLOWED_ORIGINS, FRONTEND_BASE_URL, YOOKASSA_SHOP_ID и YOOKASSA_SECRET_KEY позволяют менять окружение без изменения кода.", 1.92, 5.07, 9.0, 0.24, 11, COLORS["muted"])
    s.footer("README.md и Dockerfile: production notes + Coolify deployment")
    slides.append(s)

    s = Slide(8, "Итог")
    s.title("CloudMarket показывает полный набор практических fullstack-навыков.", w=9.0)
    s.rect(0.82, 2.42, 3.54, 2.65, COLORS["dark"])
    s.text("Что уже есть", 1.17, 2.74, 2.3, 0.3, 24, COLORS["white"], bold=True, font="Georgia")
    s.text("Каталог\nДетальная страница\nРегистрация и вход\nКорзина и избранное\nЗаказы и платежный сценарий", 1.18, 3.34, 2.5, 1.4, 15, COLORS["pale"])
    s.rect(5.2, 2.42, 3.54, 2.65, COLORS["cream"], COLORS["line"], 9000)
    s.text("Что доказано", 5.56, 2.74, 2.3, 0.3, 24, COLORS["ink"], bold=True, font="Georgia")
    s.text("Разделение ответственности\nРабота с API и БД\nТипизация данных\nАвторизация\nГотовность к деплою", 5.58, 3.34, 2.5, 1.4, 15, COLORS["ink"])
    s.rect(9.6, 2.42, 2.7, 2.65, COLORS["cream"], COLORS["line"], 9000)
    s.text("Дальше", 9.95, 2.74, 1.8, 0.3, 24, COLORS["teal"], bold=True, font="Georgia")
    s.text("Фильтры\nИстория заказов\nАдмин-панель\nРасширенная оплата\nТесты", 9.98, 3.34, 1.7, 1.4, 15, COLORS["ink"])
    s.rule(0.82, 5.84, 11.48)
    s.text("Финальная фраза", 0.88, 6.12, 1.7, 0.18, 10, COLORS["muted"], bold=True)
    s.text("Это не отдельная страница, а учебная e-commerce система с понятной архитектурой и точками роста.", 2.6, 6.04, 8.5, 0.32, 17, COLORS["ink"], bold=True)
    s.footer("Материалы для речи: папка «Сессия»")
    slides.append(s)

    return slides


def content_types(slide_count: int) -> str:
    slide_overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {slide_overrides}
</Types>"""


def presentation_xml(slide_count: int) -> str:
    ids = "\n".join(
        f'<p:sldId id="{255 + i}" r:id="rId{i}"/>' for i in range(1, slide_count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{slide_count + 1}"/></p:sldMasterIdLst>
  <p:sldIdLst>{ids}</p:sldIdLst>
  <p:sldSz cx="{CX}" cy="{CY}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""


def presentation_rels(slide_count: int) -> str:
    rels = [
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, slide_count + 1)
    ]
    rels.append(
        f'<Relationship Id="rId{slide_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {''.join(rels)}
</Relationships>"""


def basic_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""


def slide_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""


def master_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/><a:chOff x="0" y="0"/><a:chExt cx="{CX}" cy="{CY}"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>"""


def master_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""


def layout_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/><a:chOff x="0" y="0"/><a:chExt cx="{CX}" cy="{CY}"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""


def layout_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""


def theme_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="CloudMarket">
  <a:themeElements>
    <a:clrScheme name="CloudMarket"><a:dk1><a:srgbClr val="111827"/></a:dk1><a:lt1><a:srgbClr val="F6F1E8"/></a:lt1><a:dk2><a:srgbClr val="101827"/></a:dk2><a:lt2><a:srgbClr val="FFF9F0"/></a:lt2><a:accent1><a:srgbClr val="176B87"/></a:accent1><a:accent2><a:srgbClr val="C47F2C"/></a:accent2><a:accent3><a:srgbClr val="2F7D5B"/></a:accent3><a:accent4><a:srgbClr val="64748B"/></a:accent4><a:accent5><a:srgbClr val="D5C8B8"/></a:accent5><a:accent6><a:srgbClr val="223044"/></a:accent6><a:hlink><a:srgbClr val="176B87"/></a:hlink><a:folHlink><a:srgbClr val="C47F2C"/></a:folHlink></a:clrScheme>
    <a:fontScheme name="CloudMarket"><a:majorFont><a:latin typeface="Georgia"/><a:cs typeface="Georgia"/></a:majorFont><a:minorFont><a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="CloudMarket"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
  </a:themeElements>
</a:theme>"""


def app_xml(slide_count: int) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application><PresentationFormat>Wide</PresentationFormat><Slides>{slide_count}</Slides><Company>CloudMarket</Company>
</Properties>"""


def core_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>CloudMarket session presentation</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-05-20T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-05-20T00:00:00Z</dcterms:modified>
</cp:coreProperties>"""


def build() -> None:
    slides = build_slides()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types(len(slides)))
        z.writestr("_rels/.rels", basic_rels())
        z.writestr("docProps/app.xml", app_xml(len(slides)))
        z.writestr("docProps/core.xml", core_xml())
        z.writestr("ppt/presentation.xml", presentation_xml(len(slides)))
        z.writestr("ppt/_rels/presentation.xml.rels", presentation_rels(len(slides)))
        z.writestr("ppt/slideMasters/slideMaster1.xml", master_xml())
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels())
        z.writestr("ppt/slideLayouts/slideLayout1.xml", layout_xml())
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels())
        z.writestr("ppt/theme/theme1.xml", theme_xml())
        for i, slide in enumerate(slides, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide.xml())
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels())
    print(OUT)


if __name__ == "__main__":
    build()
