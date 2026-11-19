#!/usr/bin/env python3
"""Render the front page for Thursday 19 November 2026 (1024x1024 PNG).

Render path (Pillow + DejaVu, available on the build machine) draws the page
from the story data below. Fallback path (no Pillow) copies the pre-rendered
entry.png beside this file using only the standard library. Both write
$MAKEFUN_OUTPUT_DIR/entry.png and exit 0.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (24, 24, 22)
MUTED = (96, 91, 80)
CARD = (255, 253, 247)
CARD_LINE = (205, 198, 180)
HERO_BG = (14, 59, 46)
HERO_GOLD = (201, 162, 39)
HERO_TEXT = (250, 248, 240)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (tag, tag colour, headline, deck)
ROW2 = [
    ("DIPLOMACY", (176, 28, 28),
     "TRUMP, XI & PUTIN MEET IN SHENZHEN",
     "First three-way talks of the US, China and Russia, 90 minutes at APEC. "
     "Nuclear arms, Ukraine, Iran, trade and AI on the table. No breakthrough."),
    ("MARKETS / AI", (22, 101, 52),
     "ANTHROPIC DEBUTS ON NASDAQ AS ANT",
     "Priced at $83, above its $70-78 range. A record $81.3bn raised, "
     "~$1.5tn valuation."),
]
ROW3 = [
    ("WEATHER", (29, 78, 216),
     "CYCLONE AKVAN BEARS DOWN ON INDIA",
     "440 km off Narsapur; landfall due noon Fri 20 Nov. "
     "Red alert; 50,000 moved to safety."),
    ("DIPLOMACY", (146, 64, 14),
     "INDIA-JAPAN 2+2 TALKS IN TOKYO",
     "Fourth dialogue. UNICORN naval-mast pact fast-tracked; "
     "maritime security."),
    ("EUROPE", (153, 27, 27),
     "UKRAINE HITS CRIMEA BRIDGE AGAIN",
     "Third strike this week halts rail traffic; 40 killed in "
     "Zaporizhzhia as Russia hits back."),
]
ROW4 = [
    ("MIDDLE EAST", (120, 53, 15),
     "ISRAEL PUSHES PAST GAZA'S YELLOW LINE",
     "Tanks roll into central Gaza near Nuseirat, first ground move "
     "since the ceasefire. 3 killed."),
    ("MIDDLE EAST", (120, 53, 15),
     "IRAN HITS US SITES IN THE GULF",
     "Strikes on US sites in Kuwait and Bahrain after US hits Qeshm "
     "island. Drones intercepted."),
    ("EUROPE", (153, 27, 27),
     "EU'S 45BN UKRAINE LOAN GOES TO BERLIN",
     "Allies meet over a 2027 loan repaid from Russian reparations. "
     "UK pledges 1,000 long-range missiles."),
]

NUMBERS = [
    ("$79.99", "GTA VI PRICE"),
    ("$83", "ANT IPO PRICE"),
    ("45bn", "EU UKRAINE LOAN"),
    ("1,000", "UK MISSILES"),
    ("589m", "CHILDREN IN CONFLICT"),
    ("2.3m", "GTA VI ON TWITCH"),
]

ALSO = [
    "IAEA: N. Korea expanded enrichment",
    "ICJ to rule on Myanmar genocide case",
    "US-Venezuela anti-drug military pact",
    "Xi shakes hands with Japan's Takaichi",
    "Merchant gets 27.5 years for Trump plot",
    "Carney meets Trump 20 min; no tariff deal",
    "Markets: Hang Seng -2.8%, FTSE -1.3%, Brent $89.3",
    "Yesterday: Voyager 1 passed one light-day",
]

STORY_COUNT = 1 + len(ROW2) + len(ROW3) + len(ROW4) + len(ALSO)


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, text, width, max_lines, start_size, font_path):
    from PIL import ImageFont
    size = start_size
    while size > 14:
        font = ImageFont.truetype(font_path, size)
        lines = wrap(draw, text, font, width)
        if len(lines) <= max_lines:
            return font, lines
        size -= 1
    font = ImageFont.truetype(font_path, size)
    return font, wrap(draw, text, font, width)[:max_lines]


def render():
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_serif_b = lambda s: ImageFont.truetype(SERIF_B, s)
    f_serif = lambda s: ImageFont.truetype(SERIF, s)
    f_sans_b = lambda s: ImageFont.truetype(SANS_B, s)
    f_sans = lambda s: ImageFont.truetype(SANS, s)

    # ---- masthead ----
    d.line([(28, 22), (996, 22)], fill=INK, width=4)
    title = "THE WORLD IN ONE DAY"
    tf = f_serif_b(56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 30), title, font=tf, fill=INK)
    d.line([(28, 104), (996, 104)], fill=INK, width=2)
    sf = f_sans_b(19)
    d.text((28, 112), "THURSDAY, 19 NOVEMBER 2026", font=sf, fill=INK)
    mid = "THE DAY IN WORLD NEWS"
    mf = f_sans(16)
    mw = d.textlength(mid, font=mf)
    d.text(((W - mw) / 2, 115), mid, font=mf, fill=MUTED)
    cnt = "%d STORIES" % STORY_COUNT
    cw = d.textlength(cnt, font=sf)
    d.text((996 - cw, 112), cnt, font=sf, fill=INK)
    d.line([(28, 142), (996, 142)], fill=INK, width=4)

    # ---- numbers strip ----
    ny, nh = 150, 54
    d.rectangle([28, ny, 996, ny + nh], fill=(238, 231, 214))
    d.line([(28, ny + nh), (996, ny + nh)], fill=CARD_LINE, width=1)
    lf = f_sans_b(13)
    d.text((40, ny + 10), "THE DAY IN", font=lf, fill=MUTED)
    d.text((40, ny + 28), "NUMBERS", font=lf, fill=MUTED)
    d.line([(146, ny + 8), (146, ny + nh - 8)], fill=CARD_LINE, width=1)
    col0 = 158
    col_w = (996 - col0) / 6.0
    for i, (num, lab) in enumerate(NUMBERS):
        cx = col0 + i * col_w
        d.text((cx, ny + 8), num, font=f_sans_b(24), fill=INK)
        d.text((cx, ny + 36), lab, font=f_sans(11), fill=MUTED)
        if i:
            d.line([(cx - 8, ny + 10), (cx - 8, ny + nh - 10)],
                   fill=CARD_LINE, width=1)

    # ---- hero ----
    hx, hy, hw, hh = 28, 212, 968, 196
    d.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=6, fill=HERO_BG)
    tx = hx + 22
    tw_text = 640
    d.text((tx, hy + 14), "CULTURE  —  HERO STORY", font=f_sans_b(15),
           fill=HERO_GOLD)
    hf, hlines = fit_headline(d, "GTA VI LAUNCHES WORLDWIDE", tw_text, 1, 48,
                              SERIF_B)
    y = hy + 38
    for ln in hlines:
        d.text((tx, y), ln, font=hf, fill=HERO_TEXT)
        y += 52
    deck = ("Midnight local time, market by market, from New Zealand "
            "\u2014 13 years after GTA V \u2014 on PlayStation 5 and "
            "Xbox Series X|S.")
    df = f_sans(18)
    dlines = wrap(d, deck, df, tw_text)
    y += 4
    for ln in dlines[:2]:
        d.text((tx, y), ln, font=df, fill=(226, 232, 226))
        y += 22
    chips = ["$79.99", "METACRITIC 99", "2.3M ON TWITCH", "VICE CITY"]
    cx = tx
    cy = hy + hh - 34
    cf = f_sans_b(14)
    for ch in chips:
        wch = d.textlength(ch, font=cf) + 22
        d.rounded_rectangle([cx, cy, cx + wch, cy + 26], radius=13,
                            outline=HERO_GOLD, width=2)
        d.text((cx + 11, cy + 5), ch, font=cf, fill=HERO_GOLD)
        cx += wch + 10
    # big VI numeral, in its own column, clear of all text
    vf = f_serif_b(150)
    d.text((hx + hw - 215, hy + 26), "VI", font=vf, fill=HERO_GOLD)

    # ---- cards ----
    def card(x, y, w, h, tag, tag_col, headline, deck, hsize, dsize):
        d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=CARD,
                            outline=CARD_LINE, width=1)
        d.rectangle([x + 1, y + 1, x + w - 1, y + 6], fill=tag_col)
        px = x + 16
        d.text((px, y + 14), tag, font=f_sans_b(13), fill=tag_col)
        hf2, hl = fit_headline(d, headline, w - 32, 2, hsize, SERIF_B)
        yy = y + 36
        for ln in hl:
            d.text((px, yy), ln, font=hf2, fill=INK)
            yy += int(hf2.size * 1.12)
        df2 = f_sans(dsize)
        dl = wrap(d, deck, df2, w - 32)
        line_h = dsize + 5
        room = (y + h - 8) - yy
        max_dl = max(0, room // line_h)
        yy += 2
        for ln in dl[:max_dl]:
            d.text((px, yy), ln, font=df2, fill=(48, 46, 42))
            yy += line_h

    gap = 8
    cw2 = (968 - gap) // 2
    for i, (tag, col, head, deck) in enumerate(ROW2):
        card(28 + i * (cw2 + gap), 416, cw2, 174, tag, col, head, deck, 30, 16)
    cw3 = (968 - 2 * gap) // 3
    for i, (tag, col, head, deck) in enumerate(ROW3):
        card(28 + i * (cw3 + gap), 598, cw3, 160, tag, col, head, deck, 25, 15)
    for i, (tag, col, head, deck) in enumerate(ROW4):
        card(28 + i * (cw3 + gap), 766, cw3, 160, tag, col, head, deck, 25, 15)

    # ---- also today ----
    ay, ah = 934, 64
    d.rectangle([28, ay, 996, ay + ah], fill=INK)
    af = f_sans(14)
    ab = f_sans_b(14)
    label = "ALSO TODAY:  "
    lx = 40
    d.text((lx, ay + 6), label, font=ab, fill=(232, 196, 90))
    lw = d.textlength(label, font=ab)
    body = "  \u2022  ".join(ALSO)
    blines = wrap(d, body, af, 968 - 12 - lw)
    yy = ay + 6
    for ln in blines[:3]:
        d.text((lx + lw, yy), ln, font=af, fill=(245, 242, 232))
        yy += 19
    # ---- footer ----
    ff = f_sans(11)
    d.text((28, 1004),
           "Sources: Reuters \u00b7 AP \u00b7 USA Today \u00b7 Le Monde \u00b7 BusinessWorld \u00b7 "
           "IMD \u00b7 SEC filings \u00b7 NASA. All events 19 November 2026 unless noted "
           "as forecast or context.",
           font=ff, fill=MUTED)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    target = os.path.join(OUT, "entry.png")
    try:
        img = render()
        img.save(target, format="PNG", optimize=True)
    except Exception:
        src = os.path.join(HERE, "entry.png")
        shutil.copyfile(src, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
