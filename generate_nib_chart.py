# =========================
# Configuration (all mm)
# =========================

PAGE_WIDTH_MM = 210
PAGE_HEIGHT_MM = 297
MARGIN_MM = 12
TITLE_FONT_SIZE = 7      # pt
SMALL_FONT_SIZE = 3
PANEL_SPACING_MM = 6
PANEL_HEIGHT_MM = 75
LINE_LENGTH_MM = 60
VERTICAL_LINE_HEIGHT_MM = 18
HORIZONTAL_LINE_LENGTH_MM = 60
RULER_LENGTH_MM = 50

VERTICAL_SPACING_MM = 7
HORIZONTAL_ROW_SPACING_MM = 5.4

VERTICAL_LABEL_OFFSET_MM = 4
HORIZONTAL_LABEL_OFFSET_MM = 3

LEFT_COL_WIDTH = 122
RIGHT_COL_X = LEFT_COL_WIDTH + 8      # 8 mm gap between columns

ROWS = 5
COLUMN_WIDTH = 34          # mm between columns
ROW_HEIGHT = 5             # mm between rows
LINE_LENGTH = 18           # mm
LABEL_OFFSET = 2           # mm after the line

FONT_FAMILY = "Arial, Liberation Sans, sans-serif"
WIDTHS = [
    0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50,
    0.60, 0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30,
    1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00
]

# =========================
# SVG helpers
# =========================

def svg_header():
    return f'''<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" version="1.1"
width="{PAGE_WIDTH_MM}mm"
height="{PAGE_HEIGHT_MM}mm"
preserveAspectRatio="xMidYMid meet"
viewBox="0 0 {PAGE_WIDTH_MM} {PAGE_HEIGHT_MM}"><g font-family="{FONT_FAMILY}" fill="none" stroke="none" stroke-linecap="butt">'''

def svg_footer():
    return "</g>\n</svg>\n"

def svg_line(x1, y1, x2, y2, stroke_width=0.2):
    # return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-width="{stroke_width}mm" />\n'
    return f'<rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" fill="black" />'

def svg_hbar(x, y, length, thickness):
    return f'<rect x="{x}" y="{y - thickness/2:.3f}" width="{length}" height="{thickness}" fill="black"/>\n'


def svg_vbar(x, y, height, thickness):
    return f'<rect x="{x - thickness/2:.3f}" y="{y}" width="{thickness}" height="{height}" fill="black"/>\n'

def svg_text(x, y, text, size=9, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" stroke="none" fill="black" '
        f'font-size="{size}pt" '
        f'text-anchor="{anchor}" '
        f'font-family="Arial, Liberation Sans, sans-serif">'
        f'{text}</text>\n'
    )

def svg_rect(x, y, w, h, stroke_width=0.2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="black" stroke-width="{stroke_width}" />\n'

# =========================
# Layout helpers
# =========================

def content_width():
    return PAGE_WIDTH_MM - 2 * MARGIN_MM

def panel_x():
    return MARGIN_MM

def panel_width():
    return content_width()

def fmt_width(w):
    s = f"{w:.2f}"
    return s.rstrip("0").rstrip(".")

# =========================
# Ruler
# =========================

def draw_ruler(x, y):
    svg = []
    y += SMALL_FONT_SIZE + 4
    svg.append(svg_text(x, y, "Print Verification - Measure this ruler after printing", SMALL_FONT_SIZE - 1))

    x += 1
    y += SMALL_FONT_SIZE + VERTICAL_SPACING_MM * 0.5

    # Main ruler line
    svg.append(svg_hbar(x, y, RULER_LENGTH_MM, 0.25))

    for i in range(RULER_LENGTH_MM + 1):
        if i % 10 == 0:
            tick = 3
        elif i % 5 == 0:
            tick = 2
        else:
            tick = 1

        svg.append(
            svg_vbar(x + i, y - tick / 2, tick, 0.2)
        )

        if i % 10 == 0:
            svg.append(
                svg_text(x + i, y - 1.5, str(i), 2.5, "middle")
            )

    return "".join(svg)

# =========================
# Panels
# =========================

def draw_panel(x, y, panel_index):
    svg = []
    svg.append(svg_rect(x, y, panel_width(), PANEL_HEIGHT_MM, 0.2))

    # ----- Left column -----
    left = x + 3
    cursor = y + 6

    svg.append(svg_text(left, cursor, "Pen: ______________________", SMALL_FONT_SIZE))
    cursor += 6

    svg.append(svg_text(left, cursor, "Nib: ______________________", SMALL_FONT_SIZE))
    cursor += 8

    svg.append(draw_vertical_scale(left, cursor))
    cursor += VERTICAL_LINE_HEIGHT_MM + 14
    svg.append(draw_horizontal_scale(left, cursor))

    # ----- Right column -----
    comments_x = x + RIGHT_COL_X
    svg.append(draw_comments(comments_x, y + 6))

    return "".join(svg)

def draw_vertical_scale(x, y):
    svg = []

    svg.append(svg_text(
        x, y + 0, "Vertical Calibration", SMALL_FONT_SIZE,
    ))

    x = x + 2  # Added padding to left

    for i, width in enumerate(WIDTHS):
        lx = x + i * HORIZONTAL_ROW_SPACING_MM

        svg.append(svg_vbar(lx, y + 2, VERTICAL_LINE_HEIGHT_MM - 1, width))

        svg.append(
            svg_text(
                lx, y + VERTICAL_LINE_HEIGHT_MM + VERTICAL_LABEL_OFFSET_MM,
                fmt_width(width), 2.2, anchor="middle"
            )
        )

    return "".join(svg)

def draw_horizontal_scale(x, y):
    svg = []

    svg.append(
        svg_text(x, y - 3, "Horizontal Calibration", SMALL_FONT_SIZE)
    )

    for i, width in enumerate(WIDTHS):
        col = i // ROWS
        row = i % ROWS

        x0 = x + col * COLUMN_WIDTH
        y0 = y + row * ROW_HEIGHT

        svg.append(
            svg_hbar(x0, y0, LINE_LENGTH, width)
        )

        svg.append(
            svg_text(x0 + LINE_LENGTH + LABEL_OFFSET, y0 + 1.0, fmt_width(width), 2.2)
        )

    return "".join(svg)

def draw_comments(x, y):
    svg = []

    svg.append(svg_text(x, y, "Notes", SMALL_FONT_SIZE))

    line_y = y + 5

    for _ in range(4):
        svg.append(svg_hbar(x, line_y, 52, 0.2))
        line_y += 5

    line_y += 2

    svg.append(svg_text(x, line_y,      "☐ Normal", SMALL_FONT_SIZE))
    svg.append(svg_text(x + 28, line_y, "☐ Wet", SMALL_FONT_SIZE))

    line_y += 5

    svg.append(svg_text(x, line_y,      "☐ Reversed", SMALL_FONT_SIZE))
    svg.append(svg_text(x + 28, line_y, "☐ Dry", SMALL_FONT_SIZE))

    return "".join(svg)

# =========================
# Page
# =========================

def draw_page():
    svg = []
    svg.append(svg_header())

    # Title
    y = MARGIN_MM + TITLE_FONT_SIZE
    svg.append(svg_text(MARGIN_MM, y, "Fountain Pen Nib Width Calibration Chart", TITLE_FONT_SIZE))

    y += TITLE_FONT_SIZE 
    svg.append(svg_text(MARGIN_MM, y, "Print at 100% scale - A4 - All units in millimetres", SMALL_FONT_SIZE))

    y += SMALL_FONT_SIZE + VERTICAL_SPACING_MM

    # Ruler
    svg.append(draw_ruler(MARGIN_MM, 25))

    # Panels
    y += VERTICAL_SPACING_MM * 1.75
    for i in range(3):
        svg.append(draw_panel(MARGIN_MM, y, i))
        y += PANEL_HEIGHT_MM + PANEL_SPACING_MM

    svg.append(svg_footer())
    return "".join(svg)

# =========================
# Main
# =========================

def main():
    svg_content = draw_page()
    with open("nib_width_calibration_a4.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("DONE")


if __name__ == "__main__":
    main()
