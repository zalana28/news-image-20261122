#!/usr/bin/env python3
"""Draw the v2 news poster for make.fun news-image-20261122.

One day of world news, Sunday 22 November 2026, as a newspaper front
page: 24 stories, a UTC timeline, a region breakdown, a confidence
label on every story, and a date-check box. Everything is drawn with
Pillow from data in this file: no network, no randomness, no clock,
so two runs write byte-identical PNGs.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
PAPER = (247, 242, 231)
INK = (27, 27, 27)
MUTED = (90, 84, 72)
RULE = (27, 27, 27)
RED = (163, 22, 33)
NAVY = (29, 53, 87)
TEAL = (15, 118, 110)
GOLD = (138, 109, 0)
GREEN = (27, 122, 61)
AMBER = (183, 121, 31)
GREY = (102, 102, 102)
LIGHT_LINE = (196, 188, 172)

FONT_DIR = os.path.expanduser("~/workspace/fonts")


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


F_TITLE = lambda s: font("PlayfairDisplay-Bold.ttf", s)
F_BOLD = lambda s: font("PlusJakartaSans-Bold.ttf", s)
F_SEMI = lambda s: font("PlusJakartaSans-SemiBold.ttf", s)
F_MED = lambda s: font("PlusJakartaSans-Medium.ttf", s)
F_REG = lambda s: font("PlusJakartaSans-Regular.ttf", s)
F_IT = lambda s: font("PlusJakartaSans-Italic.ttf", s)

FIELD_COLOR = {
    "Conflict": RED,
    "Sport": TEAL,
    "Politics": NAVY,
    "Climate": (46, 125, 50),
    "Science": (106, 76, 147),
    "Disaster": (192, 86, 33),
    "Markets": GOLD,
    "Security": (74, 74, 74),
    "Society": (123, 45, 139),
}

CONF_COLOR = {
    "CONFIRMED": GREEN,
    "OFFICIAL": NAVY,
    "REPORTED": AMBER,
    "CLAIM": RED,
    "FORECAST": GREY,
}

# (number, region, field, confidence, headline, body, source)
LEADS = [
    (1, "ANTALYA", "Climate", "CONFIRMED",
     "COP31 ends with no deal",
     "The summit collapses after the EU rejects a draft with no mention "
     "of fossil fuels.",
     "CNN / Reuters"),
    (2, "BENGHAZI", "Conflict", "REPORTED",
     "Russian warship sunk at Benghazi",
     "Suspected Ukrainian sea drones hit the corvette Merkury. It capsizes; "
     "a second ship is hit.",
     "Reuters / AP"),
    (3, "WASHINGTON", "Politics", "CONFIRMED",
     "Democrats clinch 258 House seats",
     "Hubbard's win in N. Carolina seals the biggest House majority since "
     "1992; +44 seats.",
     "AP / Reuters"),
    (4, "BAHRAIN", "Conflict", "CONFIRMED",
     "Iran strikes US bases in Bahrain",
     "Missiles and drones hit Al-Riffa and Awali. Bahrain confirms a plant "
     "hit, two hurt.",
     "Xinhua / Reuters"),
]

# (number, region, field, confidence, headline, body, source)
GRID = [
    (5, "DYMER", "Conflict", "CONFIRMED",
     "Drone flattens Kyiv block",
     "Drone hits a Kyiv block: 1 dead, 14 missing.",
     "Reuters"),
    (6, "MERCURY", "Science", "CONFIRMED",
     "BepiColombo enters orbit",
     "ESA probe slips into orbit around Mercury.",
     "AP"),
    (7, "CIKANDE", "Disaster", "CONFIRMED",
     "Candy factory fire kills 3",
     "Blaze at a Banten candy factory: 3 dead, 37 missing.",
     "AP"),
    (8, "PORTIMAO", "Sport", "CONFIRMED",
     "Marquez takes eighth crown",
     "P8 at Portimao seals the title, level with Agostini.",
     "Reuters"),
    (9, "TURIN", "Sport", "CONFIRMED",
     "Alcaraz wins ATP Finals",
     "Beats world No 1 Zverev 6-2, 7-6 for a first title.",
     "BBC"),
    (10, "LIVERPOOL", "Sport", "CONFIRMED",
     "Liverpool thrash Man Utd 4-0",
     "Ten-man United collapse in Pochettino's debut.",
     "Reuters"),
    (11, "RABIGH", "Conflict", "CLAIM",
     "Houthis claim refinery hit",
     "Claims a direct hit; Riyadh has not confirmed it.",
     "Reuters"),
    (12, "RAMALLAH", "Conflict", "CONFIRMED",
     "Settlers torch 12 vehicles",
     "Settlers burn vehicles and homes in West Bank villages.",
     "AP"),
    (13, "SHANGHAI", "Markets", "CONFIRMED",
     "China cuts margin to 80%",
     "Exchanges cut the margin ratio to steady shares.",
     "Reuters"),
    (14, "LAS VEGAS", "Sport", "CONFIRMED",
     "Verstappen wins in Vegas",
     "Red Bull's Verstappen takes the Las Vegas GP.",
     "FIA"),
]

# (number, headline, source, confidence)
ALSO = [
    (15, "KC Current win first NWSL title, 2-1 over Washington Spirit", "Al Jazeera", "CONFIRMED"),
    (16, "Gerwyn Price wins Grand Slam of Darts, 16-11 over Van Veen", "BBC", "CONFIRMED"),
    (17, "Thitikul wins LPGA finale for a third straight year", "BBC", "CONFIRMED"),
    (18, "UK set to host the 2035 Women's World Cup, FIFA to confirm", "BBC", "FORECAST"),
    (19, "Boca Juniors win Copa Sudamericana, 2-0 over Atletico Mineiro", "One Turn", "CONFIRMED"),
    (20, "Poland: Russia tried twice to kill rapper Kyivstoner", "AP", "CONFIRMED"),
    (21, "S. Africa lowers flags for Mlambo-Ngcuka; state funeral 28 Nov", "SA Presidency", "CONFIRMED"),
    (22, "Finland: Russia towing drone-hit cargo ship after Baltic attack", "Euronews", "CONFIRMED"),
    (23, "Skubal agrees $450M Mets deal, a record for a pitcher", "Reuters / CNN", "REPORTED"),
    (24, "McBurnie's late double earns Hull a win over Brighton", "BBC", "CONFIRMED"),
]

# (utc time, text)
TIMELINE = [
    ("00:15", "Iran claims strikes on US bases in Bahrain"),
    ("09:31", "BepiColombo confirmed in orbit around Mercury"),
    ("12:45", "Dymer: 1 dead, 14 missing after drone strike"),
    ("13:57", "Marquez seals his eighth MotoGP crown"),
    ("17:51", "Houthis claim the Rabigh refinery hit"),
    ("EVENING", "COP31 ends with no deal in Antalya"),
]

BY_FIELD = [
    ("Sport", 11), ("Conflict", 6), ("Politics", 1), ("Climate", 1),
    ("Science", 1), ("Disaster", 1), ("Markets", 1), ("Security", 1),
    ("Society", 1),
]

REGIONS = [
    ("Europe", 10, NAVY), ("Americas", 6, TEAL), ("Middle East", 3, RED),
    ("Africa", 2, GOLD), ("Asia", 2, (106, 76, 147)), ("Space", 1, GREY),
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, step):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def conf_chip(draw, x, y, label):
    """Small filled confidence chip; returns width used."""
    fnt = F_BOLD(10)
    w = int(draw.textlength(label, font=fnt)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3,
                           fill=CONF_COLOR[label])
    draw.text((x + 6, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- illustrations
# Flat, simple drawings for the four lead stories. Each gets a square
# panel (x, y, size) and draws only with Pillow primitives.

def ill_cop31(draw, x, y, s):
    """Globe with a red 'no deal' slash: the climate talks collapse."""
    draw.rectangle([x, y, x + s, y + s], fill=(223, 238, 232))
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 14
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(47, 125, 100),
                 outline=(27, 27, 27), width=2)
    for k in (-2, -1, 0, 1, 2):
        draw.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12,
                  cy + r], start=270 if k < 0 else 90,
                 end=90 if k < 0 else 270, fill=(255, 255, 255), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    draw.ellipse([cx - r, cy - 12, cx + r, cy + 12], outline=(255, 255, 255),
                 width=2)
    draw.line([cx - r + 8, cy + r - 8, cx + r - 8, cy - r + 8],
              fill=RED, width=7)
    draw.line([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
              fill=RED, width=7)


def ill_ship(draw, x, y, s):
    """A corvette on the sea, hit: explosion starburst and smoke."""
    draw.rectangle([x, y, x + s, y + s], fill=(29, 53, 87))
    sea_y = y + s * 2 // 3
    draw.rectangle([x, sea_y, x + s, y + s], fill=(52, 96, 140))
    for i in range(3):
        wy = sea_y + 14 + i * 16
        draw.line([x + 8, wy, x + s - 8, wy], fill=(180, 210, 235), width=2)
    # hull
    draw.polygon([(x + 18, sea_y + 6), (x + s - 18, sea_y + 6),
                  (x + s - 34, sea_y + 30), (x + 34, sea_y + 30)],
                 fill=(120, 124, 128), outline=(27, 27, 27))
    draw.rectangle([x + s // 2 - 6, sea_y - 26, x + s // 2 + 6, sea_y + 6],
                   fill=(90, 94, 98), outline=(27, 27, 27))
    draw.rectangle([x + s // 2 - 16, sea_y - 12, x + s // 2 + 16, sea_y - 2],
                   fill=(200, 200, 200))
    # explosion starburst above the funnel
    ex, ey = x + s // 2 + 22, sea_y - 34
    pts = []
    import math
    for i in range(12):
        ang = i * math.pi / 6
        rr = 26 if i % 2 == 0 else 12
        pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
    draw.polygon(pts, fill=(255, 176, 32), outline=(163, 22, 33))
    draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(163, 22, 33))
    # smoke puffs
    for dx, dy, r in ((-52, -30, 10), (-38, -48, 13), (-20, -40, 10)):
        draw.ellipse([x + s // 2 + dx - r, sea_y + dy - r,
                      x + s // 2 + dx + r, sea_y + dy + r],
                     fill=(210, 210, 205))


def ill_house(draw, x, y, s):
    """Capitol dome under a big 258: the House majority."""
    draw.rectangle([x, y, x + s, y + s], fill=(29, 53, 87))
    cx = x + s // 2
    draw.text((cx, y + 8), "258", font=F_BOLD(34), fill=(255, 255, 255),
              anchor="ma")
    draw.pieslice([cx - 30, y + s - 92, cx + 30, y + s - 32], start=180,
                  end=360, fill=(255, 255, 255))
    draw.rectangle([cx - 2, y + s - 102, cx + 2, y + s - 92],
                   fill=(255, 255, 255))
    draw.rectangle([x + 22, y + s - 40, x + s - 22, y + s - 32],
                   fill=(255, 255, 255))
    for i in range(6):
        col_x = x + 30 + i * ((s - 60) // 5)
        draw.rectangle([col_x, y + s - 66, col_x + 7, y + s - 40],
                       fill=(255, 255, 255))
    draw.rectangle([x + 22, y + s - 74, x + s - 22, y + s - 66],
                   fill=(255, 255, 255))
    draw.rectangle([x + 22, y + s - 26, x + s - 22, y + s - 20],
                   fill=(255, 255, 255))


def ill_iran(draw, x, y, s):
    """Desert sky, dashed missile arcs, a radar dish: the Bahrain strikes."""
    draw.rectangle([x, y, x + s, y + s], fill=(232, 214, 178))
    draw.rectangle([x, y + s * 3 // 4, x + s, y + s], fill=(198, 164, 110))
    # dashed arcs (missile paths)
    for k, (ax, ay) in enumerate(((14, s - 20), (30, s - 8))):
        pts = []
        import math
        for t in range(0, 21):
            tt = t / 20.0
            px = x + ax + tt * (s - 40)
            py = y + ay - math.sin(tt * math.pi) * 52 - k * 8
            pts.append((px, py))
        for i in range(0, len(pts) - 1, 2):
            draw.line([pts[i], pts[i + 1]], fill=RED, width=3)
    # radar dish
    dx, dy = x + s - 44, y + s - 44
    draw.line([dx, dy, dx - 12, dy + 22], fill=(27, 27, 27), width=3)
    draw.pieslice([dx - 22, dy - 26, dx + 22, dy + 8], start=200, end=340,
                  fill=(120, 124, 128), outline=(27, 27, 27))
    # impact burst
    ex, ey = x + s - 26, y + 34
    draw.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 176, 32),
                 outline=RED, width=2)


ILLUSTRATIONS = {1: ill_cop31, 2: ill_ship, 3: ill_house, 4: ill_iran}


# ---------------------------------------------------------------- sections

def draw_masthead(draw):
    draw.line([MARGIN, 8, W - MARGIN, 8], fill=RULE, width=2)
    draw.text((W // 2, 13), "ONE DAY OF WORLD NEWS, ONE PICTURE",
              font=F_BOLD(11), fill=MUTED, anchor="ma")
    draw.text((W // 2, 26), "Sunday 22 November 2026",
              font=F_TITLE(42), fill=INK, anchor="ma")
    draw.text((W // 2, 76),
              "24 STORIES  ·  6 REGIONS  ·  9 FIELDS  ·  EVERY ONE FROM THIS SUNDAY",
              font=F_SEMI(12), fill=MUTED, anchor="ma")
    draw.line([MARGIN, 94, W - MARGIN, 94], fill=RULE, width=2)


def draw_by_field(draw, y):
    # label chip behind "BY FIELD"
    draw.rectangle([MARGIN - 6, y, MARGIN + 62, y + 18], fill=INK)
    draw.text((MARGIN, y + 3), "BY FIELD", font=F_BOLD(11), fill=(255, 255, 255))
    x = MARGIN + 76
    for name, count in BY_FIELD:
        label = f"{name} {count}"
        draw.text((x, y + 3), label, font=F_SEMI(12),
                  fill=FIELD_COLOR.get(name, INK))
        x += int(draw.textlength(label, font=F_SEMI(12))) + 16
    draw.line([MARGIN, y + 24, W - MARGIN, y + 24], fill=LIGHT_LINE, width=1)
    return y + 28


def draw_timeline(draw, y):
    draw.text((MARGIN, y), "THE DAY IN UTC", font=F_BOLD(11), fill=RED)
    draw.line([MARGIN, y + 18, W - MARGIN, y + 18], fill=LIGHT_LINE, width=1)
    col_w = (W - 2 * MARGIN) // 3
    row_h = 26
    for i, (when, text) in enumerate(TIMELINE):
        cx = MARGIN + (i % 3) * col_w
        cy = y + 26 + (i // 3) * row_h
        draw.text((cx, cy), when, font=F_BOLD(12), fill=RED)
        tw = int(draw.textlength(when, font=F_BOLD(12))) + 8
        lines = wrap(draw, text, F_REG(12), col_w - tw - 8)
        draw.text((cx + tw, cy + 1), lines[0] if lines else "",
                  font=F_REG(12), fill=INK)
    return y + 26 + 2 * row_h + 4


def draw_lead(draw, story, x, y, w, h):
    num, region, field, conf, headline, body, source = story
    draw.rectangle([x, y, x + w, y + h], outline=LIGHT_LINE, width=1)
    ILLUSTRATIONS[num](draw, x + 1, y + 1, h - 2)
    tx = x + h + 10
    tw = w - h - 18
    draw.text((tx, y + 6), f"{num}  {region}  ·  {field.upper()}",
              font=F_BOLD(11), fill=FIELD_COLOR[field])
    conf_chip(draw, tx, y + 22, conf)
    hl = wrap(draw, headline, F_BOLD(19), tw)
    yy = draw_lines(draw, hl[:2], tx, y + 42, F_BOLD(19), INK, 23)
    bl = wrap(draw, body, F_REG(13), tw)
    yy = draw_lines(draw, bl[:2], tx, y + 92, F_REG(13), MUTED, 16)
    draw.text((tx, y + h - 16), source, font=F_IT(11), fill=MUTED)


def draw_grid_card(draw, story, x, y, w, h):
    num, region, field, conf, headline, body, source = story
    draw.rectangle([x, y, x + w, y + h], outline=LIGHT_LINE, width=1)
    draw.text((x + 8, y + 7), f"{num}  {region}  ·  {field.upper()}",
              font=F_BOLD(10), fill=FIELD_COLOR[field])
    hl = wrap(draw, headline, F_BOLD(15), w - 16)
    yy = draw_lines(draw, hl[:2], x + 8, y + 24, F_BOLD(15), INK, 18)
    bl = wrap(draw, body, F_REG(12), w - 16)
    draw_lines(draw, bl[:2], x + 8, y + 62, F_REG(12), MUTED, 15)
    draw.text((x + 8, y + h - 16), source, font=F_IT(10), fill=MUTED)
    chip_w = int(draw.textlength(conf, font=F_BOLD(10))) + 12
    conf_chip(draw, x + w - 8 - chip_w, y + h - 16, conf)


def draw_also(draw, y):
    draw.text((MARGIN, y), "ALSO ON SUNDAY 22 NOVEMBER",
              font=F_BOLD(11), fill=RED)
    draw.line([MARGIN, y + 18, W - MARGIN, y + 18], fill=LIGHT_LINE, width=1)
    col_w = (W - 2 * MARGIN) // 2
    for i, (num, text, source, conf) in enumerate(ALSO):
        cx = MARGIN + (i % 2) * col_w
        cy = y + 26 + (i // 2) * 19
        draw.ellipse([cx, cy, cx + 16, cy + 16], fill=CONF_COLOR[conf])
        draw.text((cx + 8, cy + 2), str(num), font=F_BOLD(10),
                  fill=(255, 255, 255), anchor="ma")
        draw.text((cx + 22, cy + 1), text, font=F_REG(12), fill=INK)
        sw = int(draw.textlength(text, font=F_REG(12)))
        draw.text((cx + 22 + sw + 6, cy + 1), source, font=F_IT(10),
                  fill=MUTED)
    return y + 26 + 5 * 19 + 4


def draw_where_and_sure(draw, y):
    draw.text((MARGIN, y), "WHERE IT HAPPENED",
              font=F_BOLD(11), fill=RED)
    x = MARGIN + 148
    for name, count, color in REGIONS:
        draw.ellipse([x, y + 2, x + 9, y + 11], fill=color)
        label = f"{name} {count}"
        draw.text((x + 13, y), label, font=F_SEMI(12), fill=INK)
        x += int(draw.textlength(label, font=F_SEMI(12))) + 24
    y2 = y + 20
    draw.text((MARGIN, y2), "HOW SURE", font=F_BOLD(11), fill=RED)
    x = MARGIN + 82
    for label, note in [("CONFIRMED", "2+ outlets"),
                        ("OFFICIAL", "the body itself"),
                        ("REPORTED", "one outlet"),
                        ("CLAIM", "one side"),
                        ("FORECAST", "expected")]:
        w = conf_chip(draw, x, y2, label)
        draw.text((x + w + 5, y2 + 1), note, font=F_REG(11), fill=MUTED)
        x += w + 5 + int(draw.textlength(note, font=F_REG(11))) + 18
    draw.text((x, y2 + 1), "· number colour = confidence",
              font=F_IT(11), fill=MUTED)
    return y2 + 18


def draw_date_check(draw, y):
    draw.rectangle([MARGIN, y, W - MARGIN, y + 50], outline=RED, width=2)
    draw.text((MARGIN + 10, y + 6), "DATE CHECK", font=F_BOLD(11), fill=RED)
    text = ("Left out on purpose: El Chapo Isidro's capture (raid 20 Nov, "
            "announced 21 Nov); the EU-Indonesia trade deal (signed 21 Nov); "
            "the Trump-Xi-Putin summit (19-20 Nov); the ICJ Myanmar verdict "
            "(20 Nov); Argentina's LNG approval (20 Nov); the Nigeria boat "
            "(20 Nov).")
    lines = wrap(draw, text, F_REG(12), W - 2 * MARGIN - 20)
    draw_lines(draw, lines[:2], MARGIN + 10, y + 22, F_REG(12), INK, 15)
    return y + 56


def draw_footer(draw, y):
    draw.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    draw.text((MARGIN, y + 5),
              "Sources: AP, Reuters, BBC, CNN, Euronews, AFP, Xinhua, QNA, FIA, "
              "motogp.com, Al Jazeera, ISW, Standard Topic, One Turn.",
              font=F_REG(11), fill=MUTED)
    draw.text((MARGIN, y + 20),
              "Every story here happened or was first reported on Sunday 22 November 2026.",
              font=F_IT(11), fill=MUTED)
    return y + 34


# ---------------------------------------------------------------- build

def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    y = draw_by_field(draw, 100)
    y = draw_timeline(draw, y)
    # leads: 2 x 2
    lead_w = (W - 2 * MARGIN - 8) // 2
    lead_h = 150
    for i, story in enumerate(LEADS):
        lx = MARGIN + (i % 2) * (lead_w + 8)
        ly = y + (i // 2) * (lead_h + 8)
        draw_lead(draw, story, lx, ly, lead_w, lead_h)
    y = y + 2 * lead_h + 8 + 8
    # grid: 5 x 2
    grid_w = (W - 2 * MARGIN - 4 * 8) // 5
    grid_h = 108
    for i, story in enumerate(GRID):
        gx = MARGIN + (i % 5) * (grid_w + 8)
        gy = y + (i // 5) * (grid_h + 8)
        draw_grid_card(draw, story, gx, gy, grid_w, grid_h)
    y = y + 2 * grid_h + 8 + 8
    y = draw_also(draw, y)
    y = draw_where_and_sure(draw, y + 4)
    y = draw_date_check(draw, y + 4)
    draw_footer(draw, y + 2)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG",
             optimize=True)
    print("wrote", os.path.join(out_dir, "entry.png"),
          img.size, "bytes:",
          os.path.getsize(os.path.join(out_dir, "entry.png")))


if __name__ == "__main__":
    main()
