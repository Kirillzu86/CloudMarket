from __future__ import annotations

import html
import zipfile
from pathlib import Path


OUT = Path(__file__).resolve().parent / "output" / "CloudMarket-sales-pitch.pptx"
EMU = 914400
SLIDE_W = 13.333
SLIDE_H = 7.5
CX = int(SLIDE_W * EMU)
CY = int(SLIDE_H * EMU)

COLORS = {
    "paper": "F7F3EA",
    "ink": "121826",
    "muted": "667085",
    "line": "D8CCBC",
    "teal": "176B87",
    "gold": "B7791F",
    "green": "2F7D5B",
    "dark": "101827",
    "white": "FFFFFF",
    "cream": "FFF9F0",
    "bluegray": "243044",
    "red": "B54708",
}


def emu(value: float) -> int:
    return int(value * EMU)


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def fill(color: str) -> str:
    return f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'


def line(color: str | None = None, width: int = 0) -> str:
    if not color or width <= 0:
        return '<a:ln><a:noFill/></a:ln>'
    return f'<a:ln w="{width}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln>'


def para(value: str, size: int, color: str, bold: bool, font: str, align: str) -> str:
    b = ' b="1"' if bold else ""
    return (
        f'<a:p><a:pPr algn="{align}"/>'
        f'<a:r><a:rPr lang="ru-RU" sz="{size * 100}"{b}>'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="{esc(font)}"/><a:cs typeface="{esc(font)}"/>'
        f'</a:rPr><a:t>{esc(value)}</a:t></a:r><a:endParaRPr lang="ru-RU" sz="{size * 100}"/></a:p>'
    )


class Slide:
    def __init__(self, n: int, label: str):
        self.n = n
        self.sid = 1
        self.parts: list[str] = []
        self.rect(0, 0, SLIDE_W, SLIDE_H, COLORS["paper"])
        self.rect(0, 0, SLIDE_W, 0.14, COLORS["dark"])
        self.rect(0.45, 0.46, 0.08, 0.08, COLORS["teal"] if n % 2 else COLORS["gold"])
        self.text(label.upper(), 0.62, 0.40, 3.9, 0.2, 9, COLORS["muted"], bold=True)
        self.text(f"{n:02}", 12.35, 6.88, 0.5, 0.2, 10, COLORS["muted"], bold=True, align="r")

    def next(self) -> int:
        self.sid += 1
        return self.sid

    def rect(self, x: float, y: float, w: float, h: float, color: str, border: str | None = None) -> None:
        sid = self.next()
        self.parts.append(
            f"""<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Shape {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{fill(color)}{line(border, 9000 if border else 0)}</p:spPr></p:sp>"""
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
        bg: str | None = None,
    ) -> None:
        sid = self.next()
        paragraphs = "".join(para(line_value or " ", size, color, bold, font, align) for line_value in str(value).split("\n"))
        self.parts.append(
            f"""<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Text {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{fill(bg) if bg else '<a:noFill/>'}<a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0"/><a:lstStyle/>{paragraphs}</p:txBody></p:sp>"""
        )

    def title(self, value: str, w: float = 9.2) -> None:
        self.text(value, 0.6, 0.82, w, 0.95, 34, COLORS["ink"], bold=True, font="Georgia")

    def sub(self, value: str, x: float, y: float, w: float, h: float, size: int = 13) -> None:
        self.text(value, x, y, w, h, size, COLORS["muted"])

    def rule(self, x: float, y: float, w: float, color: str = COLORS["line"]) -> None:
        self.rect(x, y, w, 0.018, color)

    def card(self, title: str, note: str, x: float, y: float, w: float, color: str) -> None:
        self.rect(x, y, w, 1.08, COLORS["cream"], COLORS["line"])
        self.rect(x, y, 0.07, 1.08, color)
        self.text(title, x + 0.2, y + 0.18, w - 0.35, 0.24, 16, COLORS["ink"], bold=True)
        self.text(note, x + 0.2, y + 0.52, w - 0.35, 0.38, 10, COLORS["muted"])

    def metric(self, value: str, label: str, x: float, y: float, color: str) -> None:
        self.rect(x, y, 0.04, 0.58, color)
        self.text(value, x + 0.14, y - 0.02, 1.7, 0.34, 24, COLORS["ink"], bold=True, font="Georgia")
        self.text(label, x + 0.14, y + 0.36, 1.9, 0.22, 9, COLORS["muted"], bold=True)

    def footer(self, note: str = "CloudMarket sales pitch") -> None:
        self.rule(0.6, 6.62, 11.1)
        self.text(note, 0.6, 6.86, 7.4, 0.2, 8, COLORS["muted"])

    def xml(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/><a:chOff x="0" y="0"/><a:chExt cx="{CX}" cy="{CY}"/></a:xfrm></p:grpSpPr>{''.join(self.parts)}</p:spTree></p:cSld>
<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"""


def slides() -> list[Slide]:
    out: list[Slide] = []

    s = Slide(1, "Коммерческое предложение")
    s.rect(7.75, 0, 5.58, 7.5, COLORS["dark"])
    s.rect(8.65, 1.0, 3.05, 4.7, COLORS["bluegray"])
    s.rect(9.0, 1.35, 2.35, 0.28, COLORS["cream"])
    s.rect(9.0, 1.92, 0.95, 1.25, COLORS["teal"])
    s.rect(10.15, 1.92, 1.2, 1.25, COLORS["gold"])
    s.rect(9.0, 3.45, 2.35, 0.3, COLORS["white"])
    s.rect(9.0, 4.02, 2.35, 0.3, COLORS["white"])
    s.rect(9.42, 4.85, 1.5, 0.38, COLORS["green"])
    s.text("CloudMarket", 0.62, 1.50, 6.5, 0.75, 55, COLORS["ink"], bold=True, font="Georgia")
    s.text("готовая основа для онлайн-магазина одежды", 0.66, 2.42, 5.7, 0.35, 22, COLORS["teal"], bold=True)
    s.text("Проект можно продавать как стартовую e-commerce платформу: витрина, каталог, карточки товаров, личный кабинет, корзина и платежный сценарий уже собраны в единую систему.", 0.66, 3.22, 6.1, 0.75, 15, COLORS["muted"])
    s.metric("MVP", "можно показать заказчику", 0.72, 5.08, COLORS["teal"])
    s.metric("Fullstack", "frontend + backend + БД", 3.02, 5.08, COLORS["gold"])
    s.metric("Deploy", "готовность к запуску", 5.45, 5.08, COLORS["green"])
    s.footer("Позиционирование: продаем не код, а готовый старт магазина")
    out.append(s)

    s = Slide(2, "Проблема рынка")
    s.title("Малому бренду нужен магазин быстрее, чем команда успеет написать его с нуля.")
    s.sub("Типичная боль заказчика: товары есть, бренд есть, но продажи завязаны на соцсети, сообщения вручную и разрозненные инструменты.", 0.62, 1.86, 8.8, 0.46, 14)
    s.card("Запуск затягивается", "Разработка с нуля требует времени на каталог, API, авторизацию, корзину и деплой.", 0.78, 3.0, 3.4, COLORS["red"])
    s.card("Продажи выглядят несистемно", "Без сайта сложнее красиво показать ассортимент, размеры, цены и историю бренда.", 4.95, 3.0, 3.4, COLORS["gold"])
    s.card("Нет основы для роста", "Когда нет архитектуры, трудно добавить оплату, заказы, аналитику или админ-панель.", 9.12, 3.0, 3.4, COLORS["teal"])
    s.rect(1.18, 4.95, 10.7, 0.72, COLORS["dark"])
    s.text("Что продаем", 1.55, 5.13, 1.6, 0.2, 11, "CBD5E1", bold=True)
    s.text("CloudMarket сокращает путь от идеи магазина до демонстрируемого продукта: заказчик получает не макет, а работающую fullstack-основу.", 3.0, 5.08, 8.1, 0.28, 16, COLORS["white"], bold=True)
    s.footer()
    out.append(s)

    s = Slide(3, "Решение")
    s.title("CloudMarket превращает бренд в понятный онлайн-магазин с готовым покупательским сценарием.")
    s.card("Витрина", "Главная страница показывает стиль бренда, подборки и преимущества.", 0.75, 2.45, 2.75, COLORS["teal"])
    s.card("Каталог", "Товары загружаются через API и имеют fallback, если сервер недоступен.", 3.95, 2.45, 2.75, COLORS["gold"])
    s.card("Карточка товара", "Покупатель видит описание, цену, изображения, размеры и ключевую информацию.", 7.15, 2.45, 2.75, COLORS["green"])
    s.card("Корзина и оплата", "Сценарий заказа подготовлен для подключения реальной оплаты и статусов.", 10.35, 2.45, 2.2, COLORS["teal"])
    s.rule(1.15, 4.3, 10.8)
    s.text("Коммерческий смысл", 0.9, 4.85, 2.5, 0.28, 20, COLORS["ink"], bold=True, font="Georgia")
    s.text("Заказчик получает основу, которую можно адаптировать под конкретный бренд: заменить товары, цвета, тексты, домен и подключить реальные платежи.", 3.2, 4.8, 8.4, 0.45, 15, COLORS["muted"])
    s.footer("Функции подтверждаются кодом frontend/src и backend/main.py")
    out.append(s)

    s = Slide(4, "Что получает заказчик")
    s.title("Проект можно упаковать как быстрый старт интернет-магазина.")
    s.rect(0.8, 2.05, 3.55, 3.35, COLORS["dark"])
    s.text("Для бизнеса", 1.15, 2.38, 2.2, 0.32, 24, COLORS["white"], bold=True, font="Georgia")
    s.text("Быстрый запуск\nЕдиный каталог\nКрасивое представление товара\nГотовая логика заказов\nПотенциал масштабирования", 1.17, 3.08, 2.7, 1.7, 15, "DDE7F2")
    s.rect(4.9, 2.05, 3.55, 3.35, COLORS["cream"], COLORS["line"])
    s.text("Для разработчика", 5.25, 2.38, 2.5, 0.32, 24, COLORS["ink"], bold=True, font="Georgia")
    s.text("Понятная структура\nReact-компоненты\nFastAPI endpoints\nSQLAlchemy модели\nDocker-ready подход", 5.27, 3.08, 2.65, 1.7, 15, COLORS["ink"])
    s.rect(9.0, 2.05, 3.1, 3.35, COLORS["cream"], COLORS["line"])
    s.text("Для клиента", 9.35, 2.38, 2.3, 0.32, 24, COLORS["teal"], bold=True, font="Georgia")
    s.text("Удобная навигация\nИзбранное\nКорзина\nЛичный раздел\nПонятный checkout", 9.37, 3.08, 2.2, 1.7, 15, COLORS["ink"])
    s.footer()
    out.append(s)

    s = Slide(5, "Почему проект надежный")
    s.title("Техническая часть работает как аргумент доверия, а не как самоцель.")
    s.card("Frontend", "React + Vite + TypeScript дают быстрый интерфейс и понятную компонентную структуру.", 0.75, 2.45, 3.3, COLORS["teal"])
    s.card("Backend", "FastAPI + SQLAlchemy отделяют бизнес-логику от интерфейса и дают расширяемое API.", 4.95, 2.45, 3.3, COLORS["gold"])
    s.card("Данные и деплой", "SQLite, seed-данные, Dockerfile и переменные окружения упрощают запуск.", 9.15, 2.45, 3.3, COLORS["green"])
    s.rect(1.1, 4.65, 10.9, 0.86, COLORS["cream"], COLORS["line"])
    s.text("Как это объяснить покупателю", 1.45, 4.9, 2.8, 0.24, 14, COLORS["teal"], bold=True)
    s.text("Архитектура не привязывает магазин к одному экрану или одной базе: можно добавлять фильтры, админку, историю заказов, аналитику и новые способы оплаты.", 4.0, 4.86, 7.3, 0.28, 14, COLORS["muted"])
    s.footer("Стек: React, Vite, TypeScript, FastAPI, SQLAlchemy, SQLite, Docker")
    out.append(s)

    s = Slide(6, "Модель продажи")
    s.title("CloudMarket можно продавать пакетами: от демонстрационного MVP до доработки под бренд.")
    rows = [
        ("Старт", "Настройка проекта, замена контента, базовый запуск", "быстрый сайт-витрина"),
        ("Бизнес", "Фильтры, оплата, статусы заказов, оформление бренда", "готовность к продажам"),
        ("Рост", "Админ-панель, аналитика, история заказов, SEO", "масштабирование"),
    ]
    for i, (pack, scope, result) in enumerate(rows):
        y = 2.28 + i * 1.18
        color = [COLORS["teal"], COLORS["gold"], COLORS["green"]][i]
        s.rect(0.95, y, 11.0, 0.82, COLORS["cream"], COLORS["line"])
        s.rect(0.95, y, 0.1, 0.82, color)
        s.text(pack, 1.3, y + 0.2, 1.5, 0.24, 18, color, bold=True, font="Georgia")
        s.text(scope, 3.0, y + 0.18, 5.8, 0.24, 13, COLORS["ink"], bold=True)
        s.text(result, 9.35, y + 0.2, 2.2, 0.22, 12, COLORS["muted"], bold=True)
    s.text("Такой подход помогает продать проект не как «учебный код», а как основу коммерческого решения с понятными этапами внедрения.", 1.05, 5.95, 10.4, 0.32, 16, COLORS["ink"], bold=True)
    s.footer()
    out.append(s)

    s = Slide(7, "Roadmap")
    s.title("Следующие доработки прямо повышают коммерческую ценность.")
    items = [
        ("Фильтры и поиск", "быстрее найти товар", COLORS["teal"]),
        ("Админ-панель", "управлять каталогом без кода", COLORS["gold"]),
        ("История заказов", "возвраты и повторные продажи", COLORS["green"]),
        ("SEO и аналитика", "привлечение трафика", COLORS["teal"]),
        ("Расширенная оплата", "больше способов checkout", COLORS["gold"]),
    ]
    for i, (head, note, color) in enumerate(items):
        x = 0.78 + i * 2.42
        s.rect(x, 2.72, 1.9, 0.12, color)
        s.card(head, note, x, 3.02, 1.9, color)
        if i < len(items) - 1:
            s.rule(x + 1.9, 3.62, 0.5, COLORS["line"])
    s.rect(1.2, 5.28, 10.8, 0.58, COLORS["dark"])
    s.text("Продажа через roadmap", 1.55, 5.45, 2.4, 0.2, 11, "CBD5E1", bold=True)
    s.text("Сначала продается рабочая база, затем дополнительные модули как отдельные этапы.", 3.6, 5.4, 7.4, 0.24, 15, COLORS["white"], bold=True)
    s.footer()
    out.append(s)

    s = Slide(8, "Финальный оффер")
    s.title("CloudMarket - это быстрый путь от идеи бренда к работающему онлайн-магазину.")
    s.text("Что можно сказать на защите или встрече:", 0.75, 2.18, 4.8, 0.3, 18, COLORS["teal"], bold=True)
    s.rect(0.9, 2.78, 11.4, 1.28, COLORS["dark"])
    s.text("«Я предлагаю не просто набор страниц, а готовую fullstack-основу интернет-магазина. Ее можно адаптировать под бренд, подключить реальные товары и развивать как коммерческий продукт».", 1.28, 3.08, 10.65, 0.55, 22, COLORS["white"], bold=True, font="Georgia")
    s.metric("1", "готовый пользовательский сценарий", 1.0, 4.86, COLORS["teal"])
    s.metric("2", "серверная логика и база", 4.2, 4.86, COLORS["gold"])
    s.metric("3", "понятный план монетизации", 7.15, 4.86, COLORS["green"])
    s.metric("4", "простое развитие под заказчика", 10.1, 4.86, COLORS["teal"])
    s.footer("Финальная идея: проект можно продавать как MVP + этапы доработки")
    out.append(s)

    return out


def content_types(n: int) -> str:
    overrides = "".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, n + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>{overrides}</Types>"""


def presentation_xml(n: int) -> str:
    ids = "".join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1, n + 1))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{n+1}"/></p:sldMasterIdLst><p:sldIdLst>{ids}</p:sldIdLst><p:sldSz cx="{CX}" cy="{CY}" type="wide"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>"""


def rels_root() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>"""


def rels_presentation(n: int) -> str:
    rels = "".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, n + 1)
    )
    rels += f'<Relationship Id="rId{n+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}</Relationships>"""


def slide_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>"""


def master_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/><a:chOff x="0" y="0"/><a:chExt cx="{CX}" cy="{CY}"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>"""


def master_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>"""


def layout_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/><a:chOff x="0" y="0"/><a:chExt cx="{CX}" cy="{CY}"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>"""


def layout_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>"""


def theme_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="CloudMarket Sales"><a:themeElements><a:clrScheme name="CloudMarket"><a:dk1><a:srgbClr val="121826"/></a:dk1><a:lt1><a:srgbClr val="F7F3EA"/></a:lt1><a:dk2><a:srgbClr val="101827"/></a:dk2><a:lt2><a:srgbClr val="FFF9F0"/></a:lt2><a:accent1><a:srgbClr val="176B87"/></a:accent1><a:accent2><a:srgbClr val="B7791F"/></a:accent2><a:accent3><a:srgbClr val="2F7D5B"/></a:accent3><a:accent4><a:srgbClr val="667085"/></a:accent4><a:accent5><a:srgbClr val="D8CCBC"/></a:accent5><a:accent6><a:srgbClr val="243044"/></a:accent6><a:hlink><a:srgbClr val="176B87"/></a:hlink><a:folHlink><a:srgbClr val="B7791F"/></a:folHlink></a:clrScheme><a:fontScheme name="CloudMarket"><a:majorFont><a:latin typeface="Georgia"/><a:cs typeface="Georgia"/></a:majorFont><a:minorFont><a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:minorFont></a:fontScheme><a:fmtScheme name="CloudMarket"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>"""


def app_xml(n: int) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application><PresentationFormat>Wide</PresentationFormat><Slides>{n}</Slides><Company>CloudMarket</Company></Properties>"""


def core_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>CloudMarket sales pitch</dc:title><dc:creator>Codex</dc:creator><cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">2026-05-20T00:00:00Z</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">2026-05-20T00:00:00Z</dcterms:modified></cp:coreProperties>"""


def build() -> None:
    deck = slides()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types(len(deck)))
        z.writestr("_rels/.rels", rels_root())
        z.writestr("docProps/app.xml", app_xml(len(deck)))
        z.writestr("docProps/core.xml", core_xml())
        z.writestr("ppt/presentation.xml", presentation_xml(len(deck)))
        z.writestr("ppt/_rels/presentation.xml.rels", rels_presentation(len(deck)))
        z.writestr("ppt/slideMasters/slideMaster1.xml", master_xml())
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels())
        z.writestr("ppt/slideLayouts/slideLayout1.xml", layout_xml())
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels())
        z.writestr("ppt/theme/theme1.xml", theme_xml())
        for i, slide in enumerate(deck, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide.xml())
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels())
    print(OUT)


if __name__ == "__main__":
    build()
