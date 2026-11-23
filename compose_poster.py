#!/usr/bin/env python3
"""Draw the 22 November 2026 front page: THE WORLD IN ONE DAY.

Builds a 1024x1024 newspaper poster from assets/hero.png and the six
verified stories below, using PIL and the bundled Playfair / Jakarta fonts.
Run:  python3 compose_poster.py   -> writes entry.png in this directory.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONTS = os.path.join(ASSETS, "fonts")

PAGE = 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
BODY_INK = (51, 48, 42)
RED = (179, 38, 30)
MUTED = (90, 100, 112)
GOLD = (201, 162, 39)

MASTHEAD = "THE WORLD IN ONE DAY"
DATE_LINE = "SUNDAY, 22 NOVEMBER 2026"
LEAD_HEADLINE = "COP31 COLLAPSES \u2014 NO DEAL IN ANTALYA"

# (kicker, headline, body) — every fact verified against reporting dated
# 22 November 2026; see NOTES.md for the sources.
STORIES = [
    ("ANTALYA",
     "COP31 ends with no deal",
     "Talks collapse on Sunday as the EU rejects a draft with no "
     "fossil-fuel language \u2014 the longest COP ever, and the first to "
     "fail since 2009."),
    ("BAHRAIN",
     "Iran strikes U.S. bases in Bahrain",
     "Tehran claims missile and drone strikes on the Al-Riffa and Awali "
     "bases. Bahrain says an industrial site was hit and two people "
     "were hurt."),
    ("DYMER, UKRAINE",
     "Drone flattens Kyiv apartment block",
     "A Russian drone hits a five-storey block north of Kyiv early on "
     "Sunday. One person is dead, 14 are missing and nine were pulled "
     "out alive."),
    ("CIKANDE, INDONESIA",
     "Candy factory fire kills three",
     "A blaze at a candy factory in Banten leaves three dead and 36 "
     "missing as rescuers search the ruins for survivors."),
    ("MERCURY",
     "BepiColombo slips into Mercury orbit",
     "Europe and Japan\u2019s probe enters orbit around Mercury \u2014 but "
     "a thruster glitch cuts its braking burn short."),
    ("PORTIM\u00c3O",
     "M\u00e1rquez takes eighth MotoGP crown",
     "Eighth place in Portugal seals the title with a round to spare, "
     "after overturning a 102-point deficit to equal Agostini."),
]

FOOTER_MAIN = "All six stories verified against reporting dated Sunday 22 November 2026."
FOOTER_SOURCES = "Sources: CNN \u00b7 Reuters \u00b7 AP \u00b7 UN News \u00b7 Euronews \u00b7 Xinhua \u00b7 MotoGP.com"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width; returns a list of lines."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_block(draw, x, y, width, kicker, headline, body, fonts):
    """One story block: red kicker, bold headline, regular body."""
    kick_f, head_f, body_f = fonts
    # thin rule above the block, red square + kicker
    draw.line([(x, y), (x + width, y)], fill=INK, width=2)
    draw.rectangle([x, y + 14, x + 9, y + 23], fill=RED)
    draw.text((x + 17, y + 12), kicker, font=kick_f, fill=RED)
    # headline, at most two lines
    head_lines = wrap(draw, headline, head_f, width)[:2]
    hy = y + 38
    for line in head_lines:
        draw.text((x, hy), line, font=head_f, fill=INK)
        hy += 30
    # body, at most three lines
    body_lines = wrap(draw, body, body_f, width)[:3]
    by = hy + 4
    for line in body_lines:
        draw.text((x, by), line, font=body_f, fill=BODY_INK)
        by += 22


def hero_crop(hero, target_w, target_h, top_frac=0.18):
    """Centre-crop the hero to the target aspect, keeping the skyline band."""
    w, h = hero.size
    crop_h = int(w * target_h / target_w)
    top = int((h - crop_h) * top_frac)
    return hero.crop((0, top, w, top + crop_h)).resize((target_w, target_h))


def main():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)

    # newspaper frame: heavy outer rule, hairline inner rule
    draw.rectangle([10, 10, PAGE - 11, PAGE - 11], outline=INK, width=3)
    draw.rectangle([18, 18, PAGE - 19, PAGE - 19], outline=GOLD, width=1)

    # masthead
    mast_f = font("PlayfairDisplay-Bold.ttf", 56)
    date_f = font("PlusJakartaSans-SemiBold.ttf", 20)
    draw.text((PAGE // 2, 62), MASTHEAD, font=mast_f, fill=INK, anchor="mm")
    draw.text((PAGE // 2, 106), DATE_LINE, font=date_f, fill=MUTED, anchor="mm")
    draw.line([(44, 126), (PAGE - 44, 126)], fill=INK, width=3)
    draw.line([(44, 132), (PAGE - 44, 132)], fill=INK, width=1)

    # hero band with the lead headline on a dark strip
    hero = Image.open(os.path.join(ASSETS, "hero.png")).convert("RGB")
    hero_top, hero_h = 142, 268
    band = hero_crop(hero, PAGE - 88, hero_h)
    page.paste(band, (44, hero_top))
    strip = Image.new("RGBA", (PAGE - 88, 62), (10, 12, 18, 205))
    page.paste(strip, (44, hero_top + hero_h - 62), strip)
    strip_draw = ImageDraw.Draw(page)
    lead_f = font("PlusJakartaSans-Bold.ttf", 29)
    strip_draw.text((64, hero_top + hero_h - 31), LEAD_HEADLINE,
                    font=lead_f, fill=(255, 255, 255), anchor="lm")

    # six stories in a 2 x 3 grid
    kick_f = font("PlusJakartaSans-Bold.ttf", 18)
    head_f = font("PlusJakartaSans-Bold.ttf", 26)
    body_f = font("PlusJakartaSans-Regular.ttf", 18)
    block_fonts = (kick_f, head_f, body_f)
    col_w = 454
    col_x = [44, 526]
    row_y = [424, 600, 776]
    for i, (kicker, headline, body) in enumerate(STORIES):
        draw_block(draw, col_x[i % 2], row_y[i // 2], col_w,
                   kicker, headline, body, block_fonts)

    # footer: verification note and sources
    foot_f = font("PlusJakartaSans-Regular.ttf", 16)
    foot_s = font("PlusJakartaSans-Regular.ttf", 15)
    draw.line([(44, 956), (PAGE - 44, 956)], fill=MUTED, width=1)
    draw.text((PAGE // 2, 970), FOOTER_MAIN, font=foot_f, fill=MUTED,
              anchor="mm")
    draw.text((PAGE // 2, 990), FOOTER_SOURCES, font=foot_s, fill=MUTED,
              anchor="mm")

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG")
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
