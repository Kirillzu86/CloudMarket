export const style = {
  bg: "#F6F1E8",
  ink: "#111827",
  muted: "#64748B",
  soft: "#E7DDD0",
  line: "#D5C8B8",
  teal: "#176B87",
  amber: "#C47F2C",
  green: "#2F7D5B",
  dark: "#101827",
  white: "#FFFFFF",
  cream: "#FFF9F0",
  serif: "Georgia",
  sans: "Arial",
};

export function text(slide, ctx, value, x, y, w, h, opts = {}) {
  return ctx.addText(slide, {
    text: String(value ?? ""),
    left: x,
    top: y,
    width: w,
    height: h,
    fontSize: opts.size ?? 18,
    color: opts.color ?? style.ink,
    bold: Boolean(opts.bold),
    typeface: opts.face ?? style.sans,
    align: opts.align ?? "left",
    valign: opts.valign ?? "top",
    fill: opts.fill ?? "#00000000",
    line: opts.line ?? ctx.line(),
    insets: opts.insets ?? { left: 0, right: 0, top: 0, bottom: 0 },
    name: opts.name,
  });
}

export function rect(slide, ctx, x, y, w, h, fill, opts = {}) {
  return ctx.addShape(slide, {
    left: x,
    top: y,
    width: w,
    height: h,
    geometry: opts.geometry ?? "rect",
    fill,
    line: opts.line ?? ctx.line(opts.lineColor ?? "#00000000", opts.weight ?? 0),
    radius: opts.radius,
    name: opts.name,
  });
}

export function line(slide, ctx, x, y, w, color = style.line, weight = 1) {
  rect(slide, ctx, x, y, w, weight, color);
}

export function bg(slide, ctx, page, label = "CloudMarket") {
  rect(slide, ctx, 0, 0, 1280, 720, style.bg);
  rect(slide, ctx, 0, 0, 1280, 18, style.dark);
  text(slide, ctx, label.toUpperCase(), 58, 38, 260, 18, {
    size: 9,
    bold: true,
    color: style.muted,
    name: `kicker-${page}-label`,
    valign: "mid",
  });
  rect(slide, ctx, 42, 43, 8, 8, page % 2 ? style.teal : style.amber, {
    name: `kicker-${page}-marker`,
  });
  text(slide, ctx, String(page).padStart(2, "0"), 1198, 664, 38, 20, {
    size: 10,
    bold: true,
    color: style.muted,
    align: "right",
  });
}

export function title(slide, ctx, value, y = 82, w = 820, size = 34) {
  text(slide, ctx, value, 58, y, w, 92, {
    size,
    face: style.serif,
    bold: true,
    color: style.ink,
  });
}

export function sub(slide, ctx, value, x, y, w, h, opts = {}) {
  text(slide, ctx, value, x, y, w, h, {
    size: opts.size ?? 13,
    color: opts.color ?? style.muted,
    ...opts,
  });
}

export function pill(slide, ctx, value, x, y, w, color = style.teal) {
  rect(slide, ctx, x, y, w, 30, "#FFFFFF", { lineColor: color, weight: 1 });
  text(slide, ctx, value, x + 12, y + 7, w - 24, 14, {
    size: 9.5,
    bold: true,
    color,
    align: "center",
  });
}

export function node(slide, ctx, value, note, x, y, w, color = style.teal) {
  rect(slide, ctx, x, y, w, 92, style.cream, { lineColor: style.line, weight: 1 });
  rect(slide, ctx, x, y, 6, 92, color);
  text(slide, ctx, value, x + 18, y + 16, w - 32, 24, {
    size: 15,
    bold: true,
    color: style.ink,
  });
  text(slide, ctx, note, x + 18, y + 48, w - 32, 30, {
    size: 10,
    color: style.muted,
  });
}

export function arrow(slide, ctx, x1, y, w, color = style.line) {
  line(slide, ctx, x1, y, w, color, 2);
  rect(slide, ctx, x1 + w - 7, y - 4, 8, 8, color, { geometry: "triangle" });
}

export function footer(slide, ctx, note = "Источник: код проекта CloudMarket") {
  line(slide, ctx, 58, 638, 1064, style.line, 1);
  text(slide, ctx, note, 58, 660, 720, 18, { size: 8.5, color: style.muted });
}
