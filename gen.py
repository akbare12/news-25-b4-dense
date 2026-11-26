#!/usr/bin/env python3
"""Render news-image-20261125 entry (Dense-40, winner-template control). PIL only."""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 240, 230); INK = (20, 28, 46); NAVY = (18, 38, 74); RED = (192, 0, 32)
GREY = (110, 110, 108); LGREY = (228, 222, 210); GREEN = (22, 110, 60)
TEAL = (14, 110, 110); GOLD = (176, 132, 0); ORANGE = (198, 84, 0)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FB2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FS2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS2I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

def F(p, s):
    return ImageFont.truetype(p, s)

def wrap(d, text, font, maxw):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def txt(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def para(d, x, y, text, font, maxw, lh, fill=INK, maxlines=99):
    lines = wrap(d, text, font, maxw)[:maxlines]
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh

def chip(d, x, y, label, bg, fg=(255, 255, 255), size=10):
    f = F(FB2, size); w = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 15], 3, fill=bg)
    d.text((x + 5, y + 2), label, font=f, fill=fg)
    return w

def badge(d, x, y, n, r=14):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    f = F(FB2, 15)
    d.text((x + r, y + r), str(n), font=f, fill=(255, 255, 255), anchor="mm")

# ---- region colours ----
RC = {"MIDDLE EAST": (192, 0, 32), "NORTH AMERICA": (18, 38, 74), "GLOBAL": (90, 60, 140),
      "AFRICA": (198, 84, 0), "LATIN AMERICA": (22, 110, 60), "E ASIA": (14, 110, 110),
      "OCEANIA": (0, 110, 160), "SE ASIA": (176, 132, 0), "S ASIA": (150, 40, 90),
      "EUROPE": (60, 90, 160),
      "EAST ASIA": (14, 110, 110), "SOUTHEAST ASIA": (176, 132, 0), "SOUTH ASIA": (150, 40, 90),
      "LATAM": (22, 110, 60)}

HEROES = [
    dict(n=1, region="MIDDLE EAST", kick="RAS TANURA · RIYADH · MIDDLE EAST",
         head="Houthis strike Saudi oil heartland and capital",
         deck="Four drones downed over Ras Tanura refinery; missiles at Riyadh stopped. Brent +3.5%.",
         src="Reuters · SPA · Al Jazeera", chip="REPORTED", scene="refinery"),
    dict(n=2, region="MIDDLE EAST", kick="STRAIT OF HORMUZ · MIDDLE EAST",
         head="Two tankers hit mines and burn in Hormuz",
         deck="Iran's Guard says two tankers struck mines and burned in the busiest oil strait. No names given.",
         src="Reuters · IRNA", chip="CLAIM", scene="tanker"),
    dict(n=3, region="GLOBAL", kick="WASHINGTON · TRADE · GLOBAL",
         head="Trump hits 14 partners with new tariffs",
         deck="China faces 20%, the EU 15%, after an 8-month probe. Up to 40% if the truce lapses 10 January.",
         src="Reuters · USTR", chip="OFFICIAL", scene="tariff"),
]

CARDS = [
    dict(n=4, region="MIDDLE EAST", kick="GAZA CITY · GAZA",
         head="Israel kills Hamas security chief and family",
         deck="Abuelouf, 47, his wife and two daughters die in Shati camp.",
         src="Reuters · Xinhua", chip="OFFICIAL", scene="gaza"),
    dict(n=5, region="AFRICA", kick="CAIRO · EGYPT",
         head="Fuel tanker fire kills 31 on Cairo ring road",
         deck="Tanker overturns in Warraq; fire spreads to 27 vehicles.",
         src="AP · CNN", chip="REPORTED", scene="fire"),
    dict(n=6, region="LATIN AMERICA", kick="CARTAGENA · COLOMBIA",
         head="All 76 supermarket hostages freed",
         deck="Police storm Exito store; siege ends, one captor killed.",
         src="Reuters · BBC", chip="OFFICIAL", scene="rescue"),
    dict(n=7, region="E ASIA", kick="JIUQUAN · CHINA",
         head="First foreign astronaut boards Tiangong",
         deck="Shenzhou-24 lifts off 08:18; Pakistan's Zeeshan Ali aboard.",
         src="Xinhua · Reuters", chip="OFFICIAL", scene="space"),
    dict(n=8, region="OCEANIA", kick="CANBERRA · PACIFIC",
         head="Australia signs $740m security treaty",
         deck="Solomons name Australia defence partner of choice.",
         src="pm.gov.au · Reuters", chip="OFFICIAL", scene="treaty"),
    dict(n=9, region="NORTH AMERICA", kick="MIDDLETOWN, IOWA · USA",
         head="Army blows up 5 tons of toxic explosive",
         deck="9,500 lbs of lead azide detonated; EPA finds no lead.",
         src="AP · WSJ", chip="OFFICIAL", scene="blast"),
    dict(n=10, region="NORTH AMERICA", kick="MADRID · SPAIN",
         head="Abrego Garcia lands in Spain, free",
         deck="'I am leaving with my freedom,' says Abrego Garcia, 31.",
         src="Reuters · CNN", chip="REPORTED", scene="plane"),
    dict(n=11, region="NORTH AMERICA", kick="WALL STREET · USA",
         head="S&P puts Nvidia on downgrade watch",
         deck="CreditWatch negative after Huang's return; shares -3.9%.",
         src="Reuters · S&P", chip="REPORTED", scene="chart"),
    dict(n=12, region="NORTH AMERICA", kick="NEW YORK · USA",
         head="Macy's parade delayed, a first in 100 years",
         deck="100th parade moves to Saturday; gusts hit 65 mph.",
         src="Reuters · AP", chip="OFFICIAL", scene="parade"),
    dict(n=13, region="NORTH AMERICA", kick="WASHINGTON · USA",
         head="US economy grew 4.3% in Q3",
         deck="Growth revised up to 4.3%; core inflation 3.3%; confidence jumps.",
         src="Reuters", chip="OFFICIAL", scene="gdp"),
]

ALSO = [
    (14, "AFRICA", "Damazin: RSF strikes reported, 19 civilians killed", "Reuters", "REPORTED"),
    (15, "MIDDLE EAST", "US tells its citizens to leave Iran at once", "US Embassy", "OFFICIAL"),
    (16, "MIDDLE EAST", "Coalition strikes Hodeidah port after warning civilians", "SPA", "REPORTED"),
    (17, "MIDDLE EAST", "Minor damage at Jazan port; drones downed near Jeddah", "Coalition", "REPORTED"),
    (18, "GLOBAL", "Brent oil +3.5% to $94.81; WTI up 2%", "Reuters", "REPORTED"),
    (19, "NORTH AMERICA", "S&P 500 closes down 0.25% on tariff news", "Reuters", "REPORTED"),
    (20, "LATIN AMERICA", "Brazil's Embraer jets face a 10% US tariff", "USTR", "OFFICIAL"),
    (21, "EUROPE", "EU tariff capped at 15%; Vietnam 20%, India 17%", "Reuters", "OFFICIAL"),
    (22, "NORTH AMERICA", "Tariff hearing set 25 Jan; duties may slip to January", "USTR", "OFFICIAL"),
    (23, "EAST ASIA", "Shenzhou-24 docks with Tiangong 3.5 hours after launch", "Xinhua", "OFFICIAL"),
    (24, "SOUTH ASIA", "Ali stays 5-10 days, returns aboard Shenzhou-23", "Xinhua", "OFFICIAL"),
    (25, "OCEANIA", "Treaty bars foreign militarisation of Solomons sites", "DFAT", "OFFICIAL"),
    (26, "NORTH AMERICA", "EPA: no lead detected after Iowa blast, reading 0.0", "EPA", "OFFICIAL"),
    (27, "NORTH AMERICA", "Abrego Garcia: stay in Spain is temporary, lawyer says", "Reuters", "REPORTED"),
    (28, "NORTH AMERICA", "Nvidia market value down to $3.6tn from over $5tn", "Reuters", "REPORTED"),
    (29, "NORTH AMERICA", "Parade balloons grounded if gusts pass 34 mph", "NWS", "OFFICIAL"),
    (30, "MIDDLE EAST", "Second Gaza strike hits Karama, one killed", "Reuters", "REPORTED"),
    (31, "LATIN AMERICA", "10 hostages, incl. elderly women, freed on Tuesday", "Police", "REPORTED"),
    (32, "AFRICA", "Cairo fire: 27 vehicles burned, 39 ambulances deployed", "Health Ministry", "REPORTED"),
    (33, "NORTH AMERICA", "US consumer confidence at highest in nearly two years", "Reuters", "REPORTED"),
    (34, "NORTH AMERICA", "Fed's favoured core inflation stuck at 3.3%", "Reuters", "REPORTED"),
    (35, "MIDDLE EAST", "Houthi spokesman Saree claims strikes in 'three phases'", "Reuters", "CLAIM"),
    (36, "MIDDLE EAST", "Riyadh residents hear blast; missiles intercepted", "Coalition", "REPORTED"),
    (37, "MIDDLE EAST", "Iran claims a third tanker hit a mine, restricted zone", "Fars", "CLAIM"),
    (38, "GLOBAL", "Mexico and Norway spared from the new tariffs, for now", "Reuters", "OFFICIAL"),
    (39, "SOUTHEAST ASIA", "Indonesia, Malaysia, Thailand, Cambodia face 18%", "Reuters", "OFFICIAL"),
    (40, "SOUTHEAST ASIA", "Singapore tariff set at 10%, lowest of the 14", "Reuters", "OFFICIAL"),
]

NUMBERS = [("+3.5%", "Brent oil\nrises Wed"), ("2", "tankers hit\nmines"), ("20%", "new US tariff\non China"),
           ("31", "killed in Cairo\ntanker fire"), ("76", "hostages freed\nin Cartagena"), ("550,000", "barrels/day\nRas Tanura")]
UTC = [("00:18", "Shenzhou lifts off"), ("03:56", "Shenzhou docks"), ("06:30", "Cartagena stormed"),
       ("15:00", "Iowa blast"), ("17:00", "Cairo tanker fire"), ("21:00", "Riyadh blast heard")]
REGIONS = [("MIDDLE EAST", 10), ("NORTH AMERICA", 13), ("GLOBAL", 3), ("AFRICA", 3),
           ("LATAM", 3), ("E ASIA", 2), ("OCEANIA", 2), ("SE ASIA", 2),
           ("S ASIA", 1), ("EUROPE", 1)]
CHIPCOL = {"OFFICIAL": GREEN, "REPORTED": NAVY, "CLAIM": RED, "ONGOING": GOLD}

def _scene_draw(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    d.rectangle([x, y, x + w, y + int(h * 0.62)], fill=(176, 205, 228))
    if kind == "refinery":
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 110, 95))
        for i, bx in enumerate([8, 44, 84, 128, 172, 216, 258]):
            d.rectangle([x + bx, y + h - 62 + (i % 3) * 8, x + bx + 26, y + h - 26], fill=(70, 76, 88))
            d.rectangle([x + bx + 4, y + h - 74 + (i % 3) * 8, x + bx + 8, y + h - 62 + (i % 3) * 8], fill=(70, 76, 88))
        d.ellipse([x + w - 52, y + 8, x + w - 16, y + 44], fill=(255, 214, 120))
        d.polygon([(x + 150, y + 22), (x + 168, y + 46), (x + 132, y + 46)], fill=(60, 64, 74))
        for fx, fy in [(x + 60, y + 30), (x + 240, y + 18)]:
            d.polygon([(fx, fy), (fx + 14, fy + 18), (fx - 14, fy + 18)], fill=(240, 120, 40))
    elif kind == "tanker":
        d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(44, 90, 130))
        d.rectangle([x + 40, y + h - 52, x + w - 40, y + h - 30], fill=(140, 30, 30))
        d.rectangle([x + 60, y + h - 74, x + w - 90, y + h - 52], fill=(90, 90, 100))
        d.rectangle([x + w - 84, y + h - 92, x + w - 64, y + h - 52], fill=(200, 200, 200))
        for fx, fy, r in [(x + 90, y + 22, 16), (x + 200, y + 12, 20), (x + 260, y + 30, 12)]:
            d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(255, 150, 30))
            d.ellipse([fx - r // 2, fy - r // 2, fx + r // 2, fy + r // 2], fill=(255, 220, 80))
        d.ellipse([x + 14, y + h - 18, x + 30, y + h - 8], fill=(20, 20, 30))
    elif kind == "tariff":
        d.rectangle([x, y + h - 30, x + w, y + h], fill=(120, 110, 95))
        d.text((x + w // 2, y + 4), "20%", font=F(FB2, 26), fill=RED, anchor="ma")
        d.text((x + w // 2, y + 34), "14 NATIONS", font=F(FB2, 12), fill=INK, anchor="ma")
        cols = [(192, 0, 32), (18, 38, 74), (22, 110, 60), (176, 132, 0)]
        for i in range(4):
            bx = x + 12 + i * 74
            d.rectangle([bx, y + h - 52, bx + 62, y + h - 14], fill=cols[i])
            d.rectangle([bx + 4, y + h - 58, bx + 58, y + h - 52], fill=(240, 240, 240))
    elif kind in ("gaza", "fire", "blast"):
        d.rectangle([x, y + h - 24, x + w, y + h], fill=(90, 88, 84))
        for i, bx in enumerate([6, 52, 100, 150]):
            bh = 40 + (i % 2) * 14
            d.rectangle([x + bx, y + h - 24 - bh, x + bx + 40, y + h - 24], fill=(120, 118, 110))
        for fx, fy, r in [(x + 30, y + 16, 12), (x + 130, y + 10, 16)]:
            d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(255, 140, 30))
        if kind == "blast":
            d.ellipse([x + w // 2 - 18, y + 6, x + w // 2 + 18, y + 42], fill=(255, 220, 120))
    elif kind == "rescue":
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(120, 110, 95))
        d.rectangle([x + 10, y + 14, x + w - 10, y + h - 22], fill=(200, 210, 220))
        d.rectangle([x + 30, y + 30, x + w - 30, y + h - 30], fill=(90, 140, 90))
        d.text((x + w // 2, y + h // 2 - 4), "76 FREED", font=F(FB2, 13), fill=(255, 255, 255), anchor="mm")
    elif kind == "space":
        d.rectangle([x, y, x + w, y + h], fill=(12, 20, 44))
        d.ellipse([x + w - 70, y + 6, x + w - 14, y + 62], fill=(90, 140, 200))
        d.ellipse([x + w - 62, y + 14, x + w - 22, y + 54], fill=(150, 190, 235))
        d.rectangle([x + 20, y + h // 2 - 8, x + w - 90, y + h // 2 + 8], fill=(200, 200, 210))
        d.polygon([(x + w - 90, y + h // 2 - 8), (x + w - 60, y + h // 2 - 22), (x + w - 60, y + h // 2 + 22), (x + w - 90, y + h // 2 + 8)], fill=(240, 120, 40))
        for sx, sy in [(x + 30, y + 12), (x + 80, y + 26), (x + 130, y + 10), (x + 160, y + 40)]:
            d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    elif kind == "treaty":
        d.rectangle([x + 20, y + 10, x + w - 20, y + h - 12], fill=(255, 255, 255), outline=(150, 150, 150))
        d.text((x + w // 2, y + 16), "TREATY", font=F(FB2, 12), fill=NAVY, anchor="ma")
        d.line([x + 34, y + 34, x + w - 34, y + 34], fill=GREY, width=1)
        d.line([x + 34, y + 42, x + w - 60, y + 42], fill=GREY, width=1)
        d.line([x + 34, y + 50, x + w - 44, y + 50], fill=GREY, width=1)
        d.ellipse([x + w // 2 - 10, y + h - 30, x + w // 2 + 10, y + h - 10], fill=RED)
    elif kind == "plane":
        d.rectangle([x, y + h - 20, x + w, y + h], fill=(120, 110, 95))
        d.ellipse([x + 20, y + 18, x + w - 20, y + 46], fill=(235, 235, 240))
        d.polygon([(x + w - 20, y + 22), (x + w - 2, y + 8), (x + w - 2, y + 40)], fill=(18, 38, 74))
        d.rectangle([x + 60, y + 46, x + 90, y + 58], fill=(18, 38, 74))
        d.rectangle([x + w - 90, y + 46, x + w - 60, y + 58], fill=(18, 38, 74))
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        pts = [(x + 10, y + 14), (x + 60, y + 18), (x + 110, y + 12), (x + 150, y + 26), (x + 190, y + 40)]
        d.line(pts, fill=RED, width=3)
        d.line([(x + 10, y + h - 10), (x + w - 10, y + h - 10)], fill=GREY, width=1)
        d.text((x + 34, y + 6), "-3.9%", font=F(FB2, 13), fill=RED, anchor="la")
    elif kind == "parade":
        d.ellipse([x + 20, y + 8, x + 110, y + h - 14], fill=(240, 90, 90))
        d.ellipse([x + 120, y + 14, x + 170, y + h - 20], fill=(90, 140, 240))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 110, 95))
        for i in range(3):
            d.line([x + 30 + i * 50, y + h - 12, x + 36 + i * 50, y + 20], fill=(60, 60, 60), width=1)
    elif kind == "gdp":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        bars = [18, 26, 22, 40]
        for i, bh in enumerate(bars):
            d.rectangle([x + 16 + i * 44, y + h - 8 - bh, x + 16 + i * 44 + 30, y + h - 8], fill=(22, 110, 60) if i == 3 else (150, 170, 190))
        d.text((x + 34, y + 6), "+4.3%", font=F(FB2, 13), fill=GREEN, anchor="la")
    else:
        d.rectangle([x + 20, y + 12, x + w - 20, y + h - 12], fill=(200, 210, 220))


def scene(im, x, y, w, h, kind):
    tmp = Image.new("RGB", (w, 103), (214, 226, 238))
    td = ImageDraw.Draw(tmp)
    _scene_draw(td, 0, 0, w, 103, kind)
    im.paste(tmp.resize((w, h), Image.LANCZOS), (x, y))

# ---- simplified world map (equirectangular, lon/lat boxes per continent) ----
LAND = [
    # (lon0, lat0, lon1, lat1) rough continent blocks
    (-168, 66, -140, 71), (-140, 60, -125, 71), (-125, 49, -95, 60), (-95, 60, -60, 70),
    (-120, 30, -95, 49), (-95, 25, -80, 40), (-105, 15, -85, 30), (-80, 8, -60, 25),
    (-80, -5, -50, 10), (-70, -35, -40, -5), (-60, -55, -50, -35),
    (-18, 36, 30, 60), (-10, 36, 10, 43), (10, 43, 30, 60), (30, 45, 60, 70),
    (20, 35, 40, 45), (30, 12, 45, 35), (45, 25, 60, 40), (35, 5, 50, 15),
    (5, 5, 30, 20), (10, -20, 35, 5), (30, -35, 50, -15), (40, -35, 50, -20),
    (60, 50, 90, 70), (90, 50, 135, 70), (135, 45, 180, 65), (70, 10, 100, 30),
    (100, 5, 125, 25), (125, 30, 145, 45), (95, -10, 110, 5), (110, -40, 155, -10),
    (130, -40, 150, -12), (155, -40, 180, -35), (165, -45, 180, -35),
]
PINS = [(1, 50, 26), (2, 57, 26), (3, -100, 39), (4, 34, 31), (5, 31, 30), (6, -75, 10),
        (7, 113, 40), (8, 149, -25), (9, -93, 42), (10, -4, 40), (11, -76, 40),
        (12, -72, 41), (13, -79, 38)]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    d.rectangle([x, y, x + w, y + h], outline=(150, 160, 170), width=1)
    for lon0, lat0, lon1, lat1 in LAND:
        px0 = x + (lon0 + 180) / 360 * w; px1 = x + (lon1 + 180) / 360 * w
        py0 = y + (90 - lat1) / 180 * h; py1 = y + (90 - lat0) / 180 * h
        d.rectangle([px0, py0, px1, py1], fill=(170, 178, 168))
    for n, lon, lat in PINS:
        px = x + (lon + 180) / 360 * w; py = y + (90 - lat) / 180 * h
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), str(n), font=F(FB2, 9), fill=(255, 255, 255), anchor="mm")

def hero_panel(im, d, x, y, w, h, it):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(190, 185, 175), width=1)
    scene(im, x + 1, y + 1, w - 2, 103, it["scene"])
    badge(d, x + 8, y + 8, it["n"])
    chip(d, x + w - 78, y + 8, it["chip"], CHIPCOL[it["chip"]])
    cy = y + 112
    d.text((x + 8, cy), it["kick"], font=F(FB2, 11), fill=RED)
    cy += 16
    cy = para(d, x + 8, cy, it["head"], F(FB, 22), w - 16, 25, maxlines=2)
    cy += 4
    cy = para(d, x + 8, cy, it["deck"], F(FS2, 12), w - 16, 15, maxlines=3)
    d.text((x + 8, y + h - 16), it["src"], font=F(FS2I, 10), fill=GREY)

def card_panel(im, d, x, y, w, h, it):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(190, 185, 175), width=1)
    scene(im, x + 1, y + 1, w - 2, 44, it["scene"])
    badge(d, x + 6, y + 6, it["n"], r=11)
    chip(d, x + w - 72, y + 6, it["chip"], CHIPCOL[it["chip"]], size=9)
    cy = y + 50
    d.text((x + 6, cy), it["kick"], font=F(FB2, 10), fill=RC[it["region"]])
    cy += 14
    cy = para(d, x + 6, cy, it["head"], F(FB2, 14), w - 12, 16, maxlines=2)
    cy += 2
    cy = para(d, x + 6, cy, it["deck"], F(FS2, 11), w - 12, 13, maxlines=2)
    d.text((x + 6, y + h - 13), it["src"], font=F(FS2I, 9), fill=GREY)

def build():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    # kicker bar
    d.rectangle([0, 0, W, 23], fill=NAVY)
    d.text((8, 12), "THE WORLD IN ONE DAY", font=F(FB2, 11), fill=(255, 255, 255), anchor="lm")
    d.text((W - 8, 12), "40 STORIES · 10 REGIONS · EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026", font=F(FB2, 11), fill=(255, 255, 255), anchor="rm")
    # masthead
    d.text((W // 2, 30), "Wednesday, 25 November 2026", font=F(FB, 52), fill=INK, anchor="ma")
    d.line([8, 99, W - 8, 99], fill=INK, width=1)
    # sub-kicker
    d.text((W // 2, 106), "Houthi strikes spread · Hormuz mines · Trump tariffs", font=F(FS2I, 17), fill=RED, anchor="ma")
    # NUMBERS strip
    y0 = 128
    for i, (num, lab) in enumerate(NUMBERS):
        x = 8 + i * 168
        nf = F(FB2, 20) if len(num) > 5 else F(FB2, 26)
        d.text((x, y0), num, font=nf, fill=RED)
        nw = int(d.textlength(num, font=nf))
        lx = x + nw + 8
        for j, ln in enumerate(lab.split("\n")):
            d.text((lx, y0 + 4 + j * 13), ln, font=F(FS2, 10), fill=INK)
        if i < 5:
            d.line([x + 164, y0 + 4, x + 164, y0 + 40], fill=(200, 195, 185), width=1)
    d.line([8, 178, W - 8, 178], fill=(200, 195, 185), width=1)
    # UTC strip
    d.rectangle([8, 180, W - 8, 200], fill=(232, 226, 214))
    chip(d, 12, 184, "WEDNESDAY IN UTC", NAVY, size=10)
    for i, (tm, ev) in enumerate(UTC):
        x = 150 + i * 144
        d.text((x, 184), tm, font=F(FB2, 11), fill=GOLD)
        d.text((x + 38, 184), ev, font=F(FS2, 10), fill=INK)
    # region bar
    tot = sum(v for _, v in REGIONS)
    rx = 8; rw = W - 16
    for name, v in REGIONS:
        seg = rw * v / tot
        d.rectangle([rx, 202, rx + seg, 222], fill=RC[name])
        lab = f"{name} {v}"
        if d.textlength(lab, font=F(FB2, 8)) > seg - 1:
            lab = str(v)
        d.text((rx + seg / 2, 212), lab, font=F(FB2, 8), fill=(255, 255, 255), anchor="mm")
        rx += seg
    # heroes
    for i, it in enumerate(HEROES):
        hero_panel(im, d, 8 + i * 340, 228, 328, 232, it)
    # cards rows
    for r in range(2):
        for c in range(5):
            it = CARDS[r * 5 + c]
            card_panel(im, d, 8 + c * 200, 468 + r * 148, 192, 144, it)
    # section headers
    d.text((8, 768), "WHERE IT HAPPENED", font=F(FB2, 13), fill=INK)
    d.text((352, 768), "ALSO ON WEDNESDAY 25 NOVEMBER — STORIES 14–40", font=F(FB2, 13), fill=INK)
    d.line([8, 786, W - 8, 786], fill=INK, width=1)
    # map
    draw_map(d, 8, 792, 328, 122)
    d.text((8, 916), "Pins carry story numbers 1–13.", font=F(FS2I, 10), fill=GREY)
    # ALSO two columns: 14 rows, y 792..956
    for i, (n, reg, head, src, ch) in enumerate(ALSO):
        col = 0 if i < 14 else 1
        row = i if i < 14 else i - 14
        x = 352 + col * 332
        yy = 792 + int(row * 11.7)
        d.ellipse([x, yy + 1, x + 13, yy + 13], fill=RC[reg])
        d.text((x + 6.5, yy + 7), str(n), font=F(FB2, 8), fill=(255, 255, 255), anchor="mm")
        d.text((x + 17, yy + 1), head, font=F(FS2, 10), fill=INK)
    # legend under the map (left column)
    ly = 926
    d.text((8, ly), "HOW SURE:", font=F(FB2, 11), fill=INK)
    d.text((8, ly + 14), "OFFICIAL = on the record · REPORTED = wires / outlets", font=F(FS2, 10), fill=INK)
    d.text((8, ly + 27), "CLAIM = one side, unverified", font=F(FS2, 10), fill=INK)
    # DATE CHECK
    d.rectangle([8, 960, W - 8, 1014], outline=RED, width=2)
    d.rectangle([8, 960, 140, 1014], fill=RED)
    d.text((74, 987), "DATE CHECK", font=F(FB2, 13), fill=(255, 255, 255), anchor="mm")
    dc1 = "Left out — happened other days. Mon 23 Nov: Nvidia reinstates Jensen Huang · 3 tankers hit mines in Hormuz ·"
    dc2 = "Tue 24 Nov: PIF Tower drone strike, 11 hurt · Huawei guilty on 10 of 12 counts · Naeem Abu Nahel killed · Sun 22 Nov: COP31 ends with no deal"
    d.text((148, 970), dc1, font=F(FS2, 11.5), fill=INK)
    d.text((148, 986), dc2, font=F(FS2, 11.5), fill=INK)
    d.text((8, 1017), "Compiled after Wednesday ended in UTC · Pictures drawn in code, not photos · Sources: Reuters, AP, BBC, CNN, Xinhua, USTR, pm.gov.au",
           font=F(FS2I, 9), fill=GREY)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    im.save(out)
    print("saved", out)

if __name__ == "__main__":
    build()
