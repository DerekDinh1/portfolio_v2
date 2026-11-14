"""Lab scene for the starter select: a small research lab seen from above, GBA-interior style.

Only rows 0..111 show above the text box. The room layer is 240 wide and tiles sideways, so
wall furniture keeps clear of the seam; the table lives on the platform image, which is drawn
once in the middle. Day and night share all geometry.
"""
from __future__ import annotations

import random

import numpy as np

from common import H, W, Canvas, Layer, RoleSet, Variant, grid
from habitats.water import lobe

NAME = "lab"
WALL_H = 40            # wall rows; the floor starts below the baseboard
PLATFORM = dict(file="platform.png", w=232, h=48, cx=120, cy=86)   # covers x 4..235, y 62..109
OX, OY = 4, 62         # platform origin in scene coordinates
SLOTS = (84, 120, 156)  # capsule centres on the table

ROLES = RoleSet([
    "ceil", "wall_hi", "wall", "wall_lo", "wall_sh", "trim_hi", "trim", "trim_dk",
    "fl_a", "fl_b", "fl_line", "fl_sh", "rug_hi", "rug", "rug_dk",
    "win", "sky_a", "sky_b", "cloud", "star",
    "shelf_hi", "shelf", "shelf_dk", "book1", "book2", "book3", "book4", "paper",
    "mach_hi", "mach", "mach_sh", "mach_dk", "screen", "glow", "led_on", "led_off",
    "leaf_hi", "leaf", "leaf_dk", "pot", "pot_dk",
    "tbl_hi", "tbl", "tbl_sh", "tbl_dk", "shadow",
    "pad_hi", "pad", "pad_dk", "c_water", "c_fire", "c_grass",
])

DAY = dict(
    ceil="#8890A8", wall_hi="#F0F0E0", wall="#D8DCD0", wall_lo="#B8C0C0", wall_sh="#A0A8B0",
    trim_hi="#C89868", trim="#A07048", trim_dk="#684838",
    fl_a="#C8D8D8", fl_b="#B0C8D0", fl_line="#90A8B8", fl_sh="#8098A8", rug_hi="#F0A870", rug="#D87850", rug_dk="#A84840",
    win="#F8F8F0", sky_a="#58A8F8", sky_b="#98D0F8", cloud="#FFFFFF", star="#98D0F8",
    shelf_hi="#C89868", shelf="#A07048", shelf_dk="#583828",
    book1="#D85048", book2="#3890D8", book3="#58A848", book4="#E8C048", paper="#F8F8E8",
    mach_hi="#E0E8F0", mach="#A8B8C8", mach_sh="#7888A0", mach_dk="#404860",
    screen="#183848", glow="#58E0C0", led_on="#F8E060", led_off="#806838",
    leaf_hi="#98E060", leaf="#48A840", leaf_dk="#286838", pot="#C87048", pot_dk="#803830",
    tbl_hi="#F0D098", tbl="#D0A068", tbl_sh="#A07048", tbl_dk="#603828", shadow="#7088A0",
    pad_hi="#E0F8F8", pad="#88C8D8", pad_dk="#406888", c_water="#3890D8", c_fire="#E86830", c_grass="#58A848",
)
NIGHT = dict(
    ceil="#202848", wall_hi="#7880B0", wall="#5860A0", wall_lo="#484C88", wall_sh="#383870",
    trim_hi="#806088", trim="#584068", trim_dk="#302040",
    fl_a="#405088", fl_b="#384478", fl_line="#283060", fl_sh="#202850", rug_hi="#A86080", rug="#804868", rug_dk="#582C50",
    win="#9098C8", sky_a="#080C30", sky_b="#182058", cloud="#182058", star="#F8F4D0",
    shelf_hi="#806088", shelf="#584068", shelf_dk="#281830",
    book1="#904060", book2="#3058A8", book3="#307868", book4="#A89058", paper="#A8B0D8",
    mach_hi="#8898C8", mach="#5868A0", mach_sh="#404878", mach_dk="#181C40",
    screen="#081830", glow="#78F8D8", led_on="#F8E878", led_off="#484060",
    leaf_hi="#48A888", leaf="#287868", leaf_dk="#184850", pot="#784868", pot_dk="#402040",
    tbl_hi="#A888A0", tbl="#806078", tbl_sh="#584060", tbl_dk="#281830", shadow="#182040",
    pad_hi="#B0F8F8", pad="#4898C0", pad_dk="#204070", c_water="#3880D0", c_fire="#D05830", c_grass="#409858",
)
PALETTES = {"day": DAY, "night": NIGHT}


def cv(h=H, w=W) -> Canvas:
    return Canvas(w, h, ROLES)


def box(c, x0, y0, x1, y1, fill, hi=None, sh=None, edge=None):
    """Inclusive rectangle with an optional lit top-left, shaded bottom-right and outline."""
    c.rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1, fill)
    if hi:
        c.hline(x0, x1, y0, hi)
        c.rect(x0, y0, 1, y1 - y0 + 1, hi)
    if sh:
        c.hline(x0, x1, y1, sh)
        c.rect(x1, y0, 1, y1 - y0 + 1, sh)
    if edge:
        c.hline(x0, x1, y0 - 1, edge)
        c.hline(x0, x1, y1 + 1, edge)
        c.rect(x0 - 1, y0, 1, y1 - y0 + 1, edge)
        c.rect(x1 + 1, y0, 1, y1 - y0 + 1, edge)


def room() -> Canvas:
    """Two frames stacked: the console's lights and trace change between them."""
    c = cv(H * 2)
    xs, ys = grid(W, H)
    rng = random.Random(12)
    books = []
    for shelf_y in (16, 27, 38):                  # books: (x, top, width, colour) per shelf, back wall
        x = 16
        while x < 50:
            w = rng.choice((2, 2, 3, 3, 4))
            if x + w > 51:
                break
            if rng.random() < 0.14:
                x += w
                continue                          # a gap on the shelf
            books.append((x, shelf_y - rng.randint(6, 9), w, shelf_y - 1, rng.choice(("book1", "book2", "book3", "book4", "paper"))))
            x += w + (1 if rng.random() < 0.25 else 0)

    for f in range(2):
        oy = f * H
        fr = Canvas(W, H, ROLES)
        # wall: ceiling shadow, panels, wainscot
        fr.rect(0, 0, W, WALL_H, "wall")
        fr.rect(0, 0, W, 3, "ceil")
        fr.paint((ys == 3) & (xs % 2 == 0), "ceil")
        fr.rect(0, 30, W, 10, "wall_lo")
        fr.hline(0, W - 1, 29, "trim_hi")
        for x in range(0, W, 40):
            fr.rect(x, 4, 1, 25, "wall_sh")
            fr.rect(x + 1, 4, 1, 25, "wall_hi")
            fr.rect(x, 31, 1, 9, "wall_sh")
        fr.hline(0, W - 1, 40, "trim")
        fr.hline(0, W - 1, 41, "trim_dk")
        # floor: two-tone tiles with grout, shaded under the wall
        fl = ys >= WALL_H + 2
        tile = ((xs // 16) + ((ys - 42) // 16)) % 2 == 0
        fr.paint(fl & tile, "fl_a")
        fr.paint(fl & ~tile, "fl_b")
        fr.paint(fl & ((xs % 16 == 0) | ((ys - 42) % 16 == 0)), "fl_line")
        fr.paint(fl & (ys <= 44), "fl_sh")
        fr.paint(fl & (ys == 45) & (xs % 2 == 0), "fl_sh")

        # window with sky, clouds by day and stars by night
        box(fr, 100, 7, 139, 25, "sky_a", edge="win")
        fr.rect(100, 17, 40, 9, "sky_b")
        fr.paint((ys == 16) & (xs >= 100) & (xs <= 139) & (xs % 2 == 0), "sky_b")
        for cx, cy, r in ((110, 14, 3), (114, 13, 4), (119, 15, 3), (131, 21, 2), (134, 20, 3)):
            lobe(fr, cx, cy, r, ["cloud"] * 4, under=False, clip_y=16 if cy < 17 else 23)
        for x, y in ((104, 10), (123, 9), (136, 12), (128, 19), (107, 21), (117, 23)):
            fr.put(x, y, "star")
        fr.rect(119, 7, 2, 19, "win")
        fr.hline(100, 139, 16, "win")
        fr.hline(98, 141, 27, "trim_hi")
        fr.hline(98, 141, 28, "trim")

        # bookshelf
        box(fr, 14, 7, 52, 39, "shelf_dk", edge="shelf_dk")
        for y in (6, 17, 28, 39):
            fr.hline(13, 53, y, "shelf_hi" if y == 6 else "shelf")
        fr.rect(13, 6, 1, 34, "shelf_hi")
        fr.rect(53, 6, 1, 34, "shelf")
        for x, top, w, bot, role in books:
            fr.rect(x, top, w, bot - top + 1, role)
            fr.hline(x, x + w - 1, top + 2, "shelf_dk" if role == "paper" else "paper")
        # chart of the three types, pinned to the wall
        box(fr, 64, 9, 86, 23, "paper", edge="trim_dk")
        for i, role in enumerate(("c_water", "c_fire", "c_grass")):
            fr.rect(67 + i * 6, 12, 4, 4, role)
            fr.hline(67 + i * 6, 70 + i * 6, 19 + (i % 2), "wall_sh")
        fr.hline(67, 83, 21, "wall_lo")
        # console: screen, lights, vents
        box(fr, 186, 11, 226, 39, "mach", hi="mach_hi", sh="mach_sh", edge="mach_dk")
        box(fr, 191, 15, 211, 26, "screen", edge="mach_dk")
        trace = (3, 2, 4, 1, 3, 5, 2, 3, 4, 2, 1, 3, 4, 2, 3, 5, 3, 2, 4)
        for i, v in enumerate(trace):
            fr.put(192 + i, 24 - trace[(i + f * 5) % len(trace)], "glow")
        for i, (x, y) in enumerate(((216, 15), (221, 15), (216, 20), (221, 20), (216, 25), (221, 25))):
            fr.rect(x, y, 3, 3, "led_on" if (i + f) % 3 == 0 else "led_off")
        for y in (31, 33, 35):
            fr.hline(191, 211, y, "mach_sh")
        fr.rect(215, 31, 9, 5, "mach_dk")
        fr.hline(216, 222, 33, "glow" if f else "mach_sh")
        # potted plant on the floor, left of the table
        for cx, cy, r in ((27, 84, 5), (33, 80, 5), (24, 78, 4), (30, 74, 4), (36, 86, 3)):
            lobe(fr, cx, cy, r, ["leaf_hi", "leaf", "leaf", "leaf_dk"], under=False)
        box(fr, 23, 91, 36, 93, "pot", hi="pot", sh="pot_dk")
        box(fr, 25, 94, 34, 101, "pot", sh="pot_dk")
        fr.hline(24, 37, 102, "shadow")
        # rug under the table
        rug = (xs >= 50) & (xs <= 190) & (ys >= 60) & (ys <= 106)
        corner = ((xs < 53) | (xs > 187)) & ((ys < 63) | (ys > 103)) & ~(((xs - 53) ** 2 + (ys - 63) ** 2 <= 10) | ((xs - 187) ** 2 + (ys - 63) ** 2 <= 10)
                                                                 | ((xs - 53) ** 2 + (ys - 103) ** 2 <= 10) | ((xs - 187) ** 2 + (ys - 103) ** 2 <= 10))
        rug &= ~corner
        inner = (xs >= 53) & (xs <= 187) & (ys >= 63) & (ys <= 103)
        fr.paint(rug, "rug_dk")
        fr.paint(rug & inner, "rug")
        fr.paint(rug & inner & ((xs == 55) | (xs == 185) | (ys == 65) | (ys == 101)) & (xs >= 55) & (xs <= 185) & (ys >= 65) & (ys <= 101), "rug_hi")
        c.a[oy:oy + H] = fr.a
    return c


def platform() -> Canvas:
    """The lab table with three capsule rests."""
    pw, ph = PLATFORM["w"], PLATFORM["h"]
    c = cv(ph, pw)
    xs, ys = grid(pw, ph)
    # table: lit top, wood grain, shaded front, shadow on the rug
    x0, x1, top, lip, foot = 62 - OX, 178 - OX, 68 - OY, 85 - OY, 93 - OY
    c.rect(x0 + 2, foot + 1, x1 - x0 - 1, 2, "shadow")
    c.rect(x0, top, x1 - x0 + 1, lip - top, "tbl")
    c.rect(x0, lip, x1 - x0 + 1, foot - lip + 1, "tbl_sh")
    c.hline(x0, x1, top, "tbl_hi")
    c.hline(x0, x1, top + 1, "tbl_hi")
    c.hline(x0, x1, lip, "tbl_dk")
    c.hline(x0, x1, foot, "tbl_dk")
    for gy, gx0, ln in ((4, 10, 22), (7, 60, 30), (10, 24, 18), (12, 78, 26), (5, 92, 14), (14, 40, 12)):
        c.hline(x0 + gx0, x0 + gx0 + ln, top + gy, "tbl_sh")
    for cx_, cy_ in ((x0, top), (x1, top), (x0, foot), (x1, foot)):   # rounded corners
        c.a[cy_, cx_] = 0
    for sx in SLOTS:                                                # a round rest under each capsule
        cx_, cy_ = sx - OX, 81 - OY
        ring = ((xs - cx_) / 7.5) ** 2 + ((ys - cy_) / 3.2) ** 2
        c.paint(ring <= 1.0, "tbl_dk")
        c.paint(ring <= 0.62, "tbl_sh")
    return c


def build(variant: str) -> Variant:
    pal = PALETTES[variant]
    v = Variant()
    v.layers.append(Layer(f"{variant}/00-room.png", room().to_rgba(pal), 0, 2, 2))
    v.platform = platform().to_rgba(pal)
    v.platform_file = f"{variant}/platform.png"
    return v
