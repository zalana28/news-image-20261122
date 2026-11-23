#!/usr/bin/env python3
"""Draw the v3 news poster for make.fun news-image-20261122.

One day of world news, Sunday 22 November 2026, as a newspaper front
page: 44 stories (4 illustrated leads in one row, 12 grid cards in two
rows of six, 28 numbered ALSO items in three columns), a one-row UTC
timeline, a BY FIELD bar, region chips, a confidence label on every
story, and a date-check box. Layout follows the 20261118 winner
(icantcodefyi, 52 stories): density + structure + verification.
Everything is drawn with Pillow from data in this file: no network,
no randomness, no clock, so two runs write byte-identical PNGs.
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
    "Technology": (0, 102, 153),
    "Culture": (146, 64, 14),
    "Health": (194, 65, 121),
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
     "Candy factory blaze: 3 dead, 37 missing.",
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
     "Settlers burn vehicles, homes in West Bank.",
     "AP"),
    (13, "SHANGHAI", "Markets", "CONFIRMED",
     "China cuts margin to 80%",
     "Exchanges cut the margin ratio to steady shares.",
     "Reuters"),
    (14, "LAS VEGAS", "Sport", "CONFIRMED",
     "Verstappen wins in Vegas",
     "Red Bull's Verstappen takes the Las Vegas GP.",
     "FIA"),
    (15, "BARCELONA", "Sport", "CONFIRMED",
     "Barca rally to beat Villarreal 3-2",
     "Down 2-0, Barca win 3-2 at Camp Nou.",
     "LiveScore"),
    (16, "GENEVA", "Science", "CONFIRMED",
     "Riemann proof passes open checks",
     "Volunteers certify the proof in a day.",
     "NPR"),
]

# (number, headline, source, confidence)
ALSO = [
    (17, "KC Current win first NWSL title", "Al Jazeera", "CONFIRMED"),
    (18, "Price wins Grand Slam of Darts 16-11", "BBC", "CONFIRMED"),
    (19, "Thitikul wins LPGA finale, 3rd straight", "BBC", "CONFIRMED"),
    (20, "UK to host 2035 Women's World Cup", "BBC", "FORECAST"),
    (21, "Boca win Copa Sudamericana 2-0", "One Turn", "CONFIRMED"),
    (22, "Poland: Russia tried to kill Kyivstoner", "AP", "CONFIRMED"),
    (23, "S. Africa mourns Mlambo-Ngcuka", "SA Presidency", "CONFIRMED"),
    (24, "Finland tows drone-hit cargo ship", "Euronews", "CONFIRMED"),
    (25, "Skubal agrees $450M Mets deal", "Reuters", "REPORTED"),
    (26, "McBurnie double earns Hull win", "BBC", "CONFIRMED"),
    (27, "AC Milan rout Frosinone 5-1", "LiveScore", "CONFIRMED"),
    (28, "Juventus beat Venezia 4-0", "LiveScore", "CONFIRMED"),
    (29, "Atalanta 4-4 Inter, Esposito treble", "AllSports", "CONFIRMED"),
    (30, "Real Madrid beat Celta Vigo 2-1", "LiveScore", "CONFIRMED"),
    (31, "Wembanyama scores 50 in Spurs win", "Al Jazeera", "CONFIRMED"),
    (32, "France reach Nations final, 45-17", "Sky Sports", "CONFIRMED"),
    (33, "Miley Cyrus marries Maxx Morando", "BBC", "CONFIRMED"),
    (34, "Princess Kate speaks on cancer film", "France 24", "CONFIRMED"),
    (35, "Together AI discloses prompt leak", "OpenRouter", "CONFIRMED"),
    (36, "UN killer-robot talks end, no rules", "CBC", "CONFIRMED"),
    (37, "FBI crime database reportedly hacked", "BBC", "REPORTED"),
    (38, "S. Korea minister quits over AI cheating", "BBC", "CONFIRMED"),
    (39, "Istanbul protests over media takeover", "Le Monde", "CONFIRMED"),
    (40, "Likud-Yashar talks end with no deal", "Al Jazeera", "REPORTED"),
    (41, "Khartoum drones hit homes, UN site", "France 24", "REPORTED"),
    (42, "Bolsonaro stable in intensive care", "UPI", "CONFIRMED"),
    (43, "Lewis Pugh swims Strait of Hormuz", "Euronews", "CONFIRMED"),
    (44, "Brent holds near $90 as Gulf attacks go on", "CNBC", "REPORTED"),
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
    ("Sport", 18), ("Conflict", 7), ("Politics", 4), ("Culture", 2),
    ("Technology", 2), ("Security", 2), ("Society", 2), ("Markets", 2),
    ("Science", 2), ("Climate", 1), ("Disaster", 1), ("Health", 1),
]

REGIONS = [
    ("Europe", 20, NAVY), ("Americas", 11, TEAL), ("Middle East", 6, RED),
    ("Africa", 3, GOLD), ("Asia", 3, (106, 76, 147)), ("Space", 1, GREY),
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
# Flat, simple drawings for the four lead stories, drawn into a WIDE
# panel (x, y, w, h) with Pillow primitives only.

def ill_cop31(draw, x, y, w, h):
    """Globe with a red 'no deal' slash + NO DEAL text: the talks collapse."""
    import math
    draw.rectangle([x, y, x + w, y + h], fill=(223, 238, 232))
    cx, cy, r = x + 62, y + h // 2, h // 2 - 8
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(47, 125, 100),
                 outline=(27, 27, 27), width=2)
    for k in (-2, -1, 0, 1, 2):
        draw.arc([cx - r + abs(k) * 10, cy - r, cx + r - abs(k) * 10,
                  cy + r], start=270 if k < 0 else 90,
                 end=90 if k < 0 else 270, fill=(255, 255, 255), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    draw.ellipse([cx - r, cy - 10, cx + r, cy + 10],
                 outline=(255, 255, 255), width=2)
    draw.line([cx - r + 6, cy + r - 6, cx + r - 6, cy - r + 6],
              fill=RED, width=6)
    draw.line([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
              fill=RED, width=6)
    draw.text((x + 112, y + h // 2 - 12), "NO", font=F_BOLD(22), fill=RED)
    draw.text((x + 112, y + h // 2 + 12), "DEAL", font=F_BOLD(22), fill=RED)


def ill_ship(draw, x, y, w, h):
    """A corvette on the sea, hit: explosion starburst and smoke."""
    import math
    draw.rectangle([x, y, x + w, y + h], fill=(29, 53, 87))
    sea_y = y + h * 3 // 5
    draw.rectangle([x, sea_y, x + w, y + h], fill=(52, 96, 140))
    for i in range(2):
        wy = sea_y + 10 + i * 12
        draw.line([x + 8, wy, x + w - 8, wy], fill=(180, 210, 235), width=2)
    # hull
    hx0, hx1 = x + 34, x + w - 34
    draw.polygon([(hx0, sea_y + 4), (hx1, sea_y + 4),
                  (hx1 - 14, sea_y + 22), (hx0 + 14, sea_y + 22)],
                 fill=(120, 124, 128), outline=(27, 27, 27))
    mx = x + w // 2
    draw.rectangle([mx - 5, sea_y - 18, mx + 5, sea_y + 4],
                   fill=(90, 94, 98), outline=(27, 27, 27))
    draw.rectangle([mx - 14, sea_y - 8, mx + 14, sea_y - 1],
                   fill=(200, 200, 200))
    # explosion starburst above the funnel
    ex, ey = mx + 34, sea_y - 24
    pts = []
    for i in range(12):
        ang = i * math.pi / 6
        rr = 22 if i % 2 == 0 else 10
        pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
    draw.polygon(pts, fill=(255, 176, 32), outline=(163, 22, 33))
    draw.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(163, 22, 33))
    # smoke puffs
    for dx, dy, r in ((-46, -22, 9), (-32, -36, 11), (-16, -28, 8)):
        draw.ellipse([mx + dx - r, sea_y + dy - r,
                      mx + dx + r, sea_y + dy + r],
                     fill=(210, 210, 205))


def ill_house(draw, x, y, w, h):
    """Capitol dome under a big 258: the House majority."""
    draw.rectangle([x, y, x + w, y + h], fill=(29, 53, 87))
    cx = x + w // 2
    draw.text((cx, y + 4), "258", font=F_BOLD(30), fill=(255, 255, 255),
              anchor="ma")
    draw.pieslice([cx - 26, y + h - 44, cx + 26, y + h - 8], start=180,
                  end=360, fill=(255, 255, 255))
    draw.rectangle([cx - 2, y + h - 52, cx + 2, y + h - 44],
                   fill=(255, 255, 255))
    draw.rectangle([x + 30, y + h - 20, x + w - 30, y + h - 14],
                   fill=(255, 255, 255))
    for i in range(6):
        col_x = x + 38 + i * ((w - 76) // 5)
        draw.rectangle([col_x, y + h - 40, col_x + 6, y + h - 20],
                       fill=(255, 255, 255))
    draw.rectangle([x + 30, y + h - 46, x + w - 30, y + h - 40],
                   fill=(255, 255, 255))


def ill_iran(draw, x, y, w, h):
    """Desert sky, dashed missile arcs, a radar dish: the Bahrain strikes."""
    import math
    draw.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    draw.rectangle([x, y + h * 3 // 4, x + w, y + h], fill=(198, 164, 110))
    # dashed arcs (missile paths)
    for k, ay in enumerate((h - 18, h - 6)):
        pts = []
        for t in range(0, 21):
            tt = t / 20.0
            px = x + 12 + tt * (w - 60)
            py = y + ay - math.sin(tt * math.pi) * 44 - k * 6
            pts.append((px, py))
        for i in range(0, len(pts) - 1, 2):
            draw.line([pts[i], pts[i + 1]], fill=RED, width=3)
    # radar dish
    dx, dy = x + w - 42, y + h - 30
    draw.line([dx, dy, dx - 10, dy + 18], fill=(27, 27, 27), width=3)
    draw.pieslice([dx - 20, dy - 22, dx + 20, dy + 6], start=200, end=340,
                  fill=(120, 124, 128), outline=(27, 27, 27))
    # impact burst
    ex, ey = x + w - 24, y + 26
    draw.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=(255, 176, 32),
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
              "44 STORIES  ·  6 REGIONS  ·  12 FIELDS  ·  EVERY ONE FROM THIS SUNDAY",
              font=F_SEMI(12), fill=MUTED, anchor="ma")
    draw.line([MARGIN, 94, W - MARGIN, 94], fill=RULE, width=2)


def draw_by_field(draw, y):
    draw.rectangle([MARGIN - 6, y, MARGIN + 62, y + 18], fill=INK)
    draw.text((MARGIN, y + 3), "BY FIELD", font=F_BOLD(11), fill=(255, 255, 255))
    # fit 12 fields on one line; shrink the font if the 12pt run is too wide
    for size in (12, 11):
        fnt = F_SEMI(size)
        total = sum(int(draw.textlength(f"{n} {c}", font=fnt)) + 16
                    for n, c in BY_FIELD) - 16
        if MARGIN + 76 + total <= W - MARGIN:
            break
    x = MARGIN + 76
    for name, count in BY_FIELD:
        label = f"{name} {count}"
        draw.text((x, y + 3), label, font=fnt,
                  fill=FIELD_COLOR.get(name, INK))
        x += int(draw.textlength(label, font=fnt)) + 16
    draw.line([MARGIN, y + 24, W - MARGIN, y + 24], fill=LIGHT_LINE, width=1)
    return y + 28


def draw_timeline(draw, y):
    draw.text((MARGIN, y), "THE DAY IN UTC", font=F_BOLD(11), fill=RED)
    draw.line([MARGIN, y + 18, W - MARGIN, y + 18], fill=LIGHT_LINE, width=1)
    col_w = (W - 2 * MARGIN) // 6
    for i, (when, text) in enumerate(TIMELINE):
        cx = MARGIN + i * col_w
        draw.text((cx, y + 24), when, font=F_BOLD(12), fill=RED)
        lines = wrap(draw, text, F_REG(11), col_w - 10)
        draw_lines(draw, lines[:2], cx, y + 40, F_REG(11), INK, 13)
    return y + 68


def draw_lead(draw, story, x, y, w, h):
    num, region, field, conf, headline, body, source = story
    draw.rectangle([x, y, x + w, y + h], outline=LIGHT_LINE, width=1)
    ILLUSTRATIONS[num](draw, x + 1, y + 1, w - 2, 90)
    ty = y + 96
    label = f"{num}  {region}  ·  {field.upper()}"
    label_font = F_BOLD(11)
    chip_w = int(draw.textlength(conf, font=F_BOLD(10))) + 12
    if 8 + int(draw.textlength(label, font=label_font)) + 6 + chip_w > w - 8:
        label_font = F_BOLD(10)
    draw.text((x + 8, ty), label, font=label_font, fill=FIELD_COLOR[field])
    conf_chip(draw, x + w - 8 - chip_w, ty, conf)
    hl = wrap(draw, headline, F_BOLD(17), w - 16)
    yy = draw_lines(draw, hl[:2], x + 8, ty + 18, F_BOLD(17), INK, 20)
    bl = wrap(draw, body, F_REG(12), w - 16)
    draw_lines(draw, bl[:3], x + 8, ty + 62, F_REG(12), MUTED, 15)
    draw.text((x + 8, y + h - 16), source, font=F_IT(11), fill=MUTED)


def draw_grid_card(draw, story, x, y, w, h):
    num, region, field, conf, headline, body, source = story
    draw.rectangle([x, y, x + w, y + h], outline=LIGHT_LINE, width=1)
    draw.rectangle([x, y, x + w, y + 5], fill=FIELD_COLOR[field])
    draw.text((x + 8, y + 10), f"{num}  {region}  ·  {field.upper()}",
              font=F_BOLD(10), fill=FIELD_COLOR[field])
    hl = wrap(draw, headline, F_BOLD(14), w - 16)
    draw_lines(draw, hl[:2], x + 8, y + 27, F_BOLD(14), INK, 17)
    bl = wrap(draw, body, F_REG(11), w - 16)
    draw_lines(draw, bl[:2], x + 8, y + 64, F_REG(11), MUTED, 14)
    draw.text((x + 8, y + h - 16), source, font=F_IT(10), fill=MUTED)
    chip_w = int(draw.textlength(conf, font=F_BOLD(10))) + 12
    conf_chip(draw, x + w - 8 - chip_w, y + h - 16, conf)


def draw_also(draw, y):
    draw.text((MARGIN, y), "ALSO ON SUNDAY 22 NOVEMBER",
              font=F_BOLD(11), fill=RED)
    draw.line([MARGIN, y + 18, W - MARGIN, y + 18], fill=LIGHT_LINE, width=1)
    col_w = (W - 2 * MARGIN) // 3
    row_h = 16
    for i, (num, text, source, conf) in enumerate(ALSO):
        cx = MARGIN + (i % 3) * col_w
        cy = y + 24 + (i // 3) * row_h
        draw.ellipse([cx, cy, cx + 15, cy + 15], fill=CONF_COLOR[conf])
        draw.text((cx + 7, cy + 1), str(num), font=F_BOLD(9),
                  fill=(255, 255, 255), anchor="ma")
        draw.text((cx + 20, cy + 1), text, font=F_REG(12), fill=INK)
        sw = int(draw.textlength(text, font=F_REG(12)))
        draw.text((cx + 20 + sw + 6, cy + 1), source, font=F_IT(10),
                  fill=MUTED)
    rows = (len(ALSO) + 2) // 3
    return y + 24 + rows * row_h + 2


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
              "motogp.com, Al Jazeera, ISW, One Turn, LiveScore, AllSports, Sky "
              "Sports, CBC, Le Monde, UPI.",
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
    # leads: 1 row x 4
    lead_w = (W - 2 * MARGIN - 3 * 8) // 4
    lead_h = 228
    for i, story in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + 8)
        draw_lead(draw, story, lx, y, lead_w, lead_h)
    y = y + lead_h + 8
    # grid: 2 rows x 6
    grid_w = (W - 2 * MARGIN - 5 * 8) // 6
    grid_h = 124
    for i, story in enumerate(GRID):
        gx = MARGIN + (i % 6) * (grid_w + 8)
        gy = y + (i // 6) * (grid_h + 8)
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
