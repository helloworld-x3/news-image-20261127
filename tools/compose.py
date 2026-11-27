#!/usr/bin/env python3
"""Compose the news-image-20261127 entry: one 1024x1024 daily-news card.

Real photographs from Wikimedia Commons, laid out as a restrained daily
briefing card: warm-white paper, one oxblood-red accent, serif headlines,
small-caps kickers, generous whitespace, hairline rules, one-line photo
captions. No AI imagery, no gloss, no gradients.

Masthead: "THE WORLD TODAY" in large black serif on the paper, thin black
rules above and below, one hairline red rule as the only red accent up top.

Layout (1024x1024):
  top row    date left, red REC dot right
  masthead   nameplate + rules
  grey box   one-line standfirst naming all four stories
  lead card  storm photo left, kicker + headline + subhead right
  three cards in a row, each: photo, kicker, headline, subhead, caption
  footer     photo credits left, news sources right

Facts are the verified ones in SOURCES.md. Two photos are file photos and
their captions say so: the parade picture is from 2024 (this year's parade
was postponed, so no 2026 parade photo exists), and the tanker picture
shows a different vessel (no free photo of the Med Emre exists).

Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
Reads photos from <repo>/photos/ and writes entry.png (JPEG bytes under
the name entry.png) into the repository root.
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PHOTOS = os.path.join(REPO, "photos")

W = H = 1024
M = 36
CW = W - 2 * M

PAPER = (253, 252, 248)
INK = (25, 25, 25)
BODY = (58, 56, 52)
GREY = (110, 106, 99)
RED = (158, 27, 50)
HAIR = (217, 212, 199)
BOX = (241, 238, 230)

FONTS = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS_I = lambda s: font("LiberationSans-Italic.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=SANS_B(16), fill=RED)


def photo(path, box_w, box_h, centering=(0.5, 0.5)):
    img = Image.open(os.path.join(PHOTOS, path)).convert("RGB")
    return ImageOps.fit(img, (box_w, box_h), Image.LANCZOS, centering=centering)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top row: date left, red REC dot right.
    d.text((M, 30), "Friday, November 27, 2026", font=SANS(19), fill=INK)
    rec = "REC"
    rw = d.textlength(rec, font=SANS_B(18))
    d.ellipse((W - M - rw - 24, 33, W - M - rw - 12, 45), fill=RED)
    d.text((W - M - rw, 30), rec, font=SANS_B(18), fill=RED)

    # Masthead with rules.
    d.line((M, 58, W - M, 58), fill=INK, width=2)
    name = "THE WORLD TODAY"
    size = 88
    while d.textlength(name, font=SERIF_B(size)) > CW and size > 40:
        size -= 2
    d.text((M, 66), name, font=SERIF_B(size), fill=INK)
    d.line((M, 168, W - M, 168), fill=INK, width=1)
    d.line((M, 172, W - M, 172), fill=RED, width=2)

    # Standfirst box.
    d.rectangle((M, 186, W - M, 242), fill=BOX)
    stand = ("Thanksgiving storm batters the US East Coast \u00b7 Tokyo inflation "
             "stays hot \u00b7 Tanker capsizes off Ibiza \u00b7 Delhi police free 164 "
             "in \u2018cyber slavery\u2019 raid")
    lines = wrap(d, stand, SANS(18), CW - 32)
    y = 186 + (56 - len(lines) * 24) // 2
    for line in lines:
        d.text(((W - d.textlength(line, font=SANS(18))) / 2, y), line,
               font=SANS(18), fill=BODY)
        y += 24

    # Lead card: storm.
    d.text((M, 258), "", font=SANS(1))
    img.paste(photo("storm-parade.jpg", 452, 268, centering=(0.5, 0.35)),
              (M, 258))
    x = 512
    kicker(d, x, 262, "UNITED STATES \u2014 WEATHER")
    head = wrap(d, "Thanksgiving storm batters US East Coast",
                SERIF_B(40), W - M - x)
    y = draw_lines(d, head, x, 292, SERIF_B(40), INK, 48)
    sub = wrap(d, "Power out for 836,000 as the 100th Macy\u2019s parade is "
                  "postponed for weather \u2014 a first.", SANS(20), W - M - x)
    draw_lines(d, sub, x, y + 8, SANS(20), BODY, 27)
    d.text((M, 534), "The Macy\u2019s parade in 2024; this year\u2019s was postponed.",
           font=SANS_I(15), fill=GREY)

    # Divider.
    d.line((M, 562, W - M, 562), fill=HAIR, width=1)

    # Three cards.
    cards = [
        ("tokyo-boj.jpg", "JAPAN \u2014 ECONOMY",
         "Tokyo inflation stays hot at 2.9%",
         "Core prices top the BOJ\u2019s 2% target for a third month; a "
         "December rate rise looks likelier.",
         "Bank of Japan headquarters, Tokyo."),
        ("ibiza-tanker.jpg", "SPAIN \u2014 MARITIME",
         "Diesel tanker capsizes off Ibiza; one dead",
         "Med Emre, carrying up to 7,000 tonnes of diesel, went down "
         "56 km off Ibiza; 17 crew rescued.",
         "A chemical tanker at sea \u2014 file photo."),
        ("delhi-police.jpg", "INDIA \u2014 CRIME",
         "Delhi police free 164 in \u2018cyber slavery\u2019 raid",
         "Foreign nationals freed from a Noida call centre; 355 phones "
         "and 174 passports seized.",
         "Delhi Police headquarters."),
    ]
    col_w = 301
    gap = 24
    for i, (pic, kick, head, sub, cap) in enumerate(cards):
        cx = M + i * (col_w + gap)
        img.paste(photo(pic, col_w, 170), (cx, 580))
        kicker(d, cx, 758, kick)
        hl = wrap(d, head, SERIF_B(26), col_w)
        y = draw_lines(d, hl, cx, 782, SERIF_B(26), INK, 32)
        sl = wrap(d, sub, SANS(17), col_w)
        y = draw_lines(d, sl, cx, y + 6, SANS(17), BODY, 23)
        d.text((cx, y + 8), cap, font=SANS_I(14), fill=GREY)

    # Footer.
    d.line((M, 952, W - M, 952), fill=HAIR, width=1)
    d.text((M, 964), "Photos: A. Quintano \u00b7 R. Spekking \u00b7 Ji-Elle \u00b7 BOJ HQ (public domain)",
           font=SANS(14), fill=GREY)
    src = "Sources: Reuters \u00b7 AP \u00b7 NDTV \u00b7 Deccan Herald"
    d.text((W - M - d.textlength(src, font=SANS(14)), 964), src,
           font=SANS(14), fill=GREY)

    out = os.path.join(REPO, "entry.png")
    img.save(out, "JPEG", quality=88)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
