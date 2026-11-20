"""Lost-trail scene for the 404 page: a dark field at dusk with one lit patch of grass, and a
hiking pack somebody set down there (bedroll on top, trail map in the side pocket).

Only rows 0..111 show above the text box. The field layer is 240 wide and tiles sideways;
the patch and the pack live on the platform image, which is drawn once in the middle.
Day and night share all geometry. The pack is hand-drawn, one character per pixel.
"""
from __future__ import annotations

import random

import numpy as np

from common import H, W, Canvas, Layer, RoleSet, Variant, checker, grid, tile_noise

NAME = "lost"
PLATFORM = dict(file="platform.png", w=176, h=96, cx=120, cy=64)   # covers x 32..207, y 16..111
OX, OY = 32, 16
PATCH = dict(cx=120, cy=76, rx=76, ry=25)
PACK_X, PACK_Y = 91, 31      # top-left of the pack in scene coordinates

ROLES = RoleSet([
    "bg", "bg_dk", "bg_hi", "blade",
    "g_hi", "g", "g_md", "g_dk", "fl_w", "fl_y",
    "ink", "pk_hi", "pk", "pk_sh", "pk_dk",
    "st_hi", "st", "st_dk", "buckle",
    "roll_hi", "roll", "roll_sh", "map", "map_sh", "ribbon",
])

DAY = dict(
    bg="#285830", bg_dk="#204828", bg_hi="#306838", blade="#184020",
    g_hi="#B8F088", g="#88D860", g_md="#60B848", g_dk="#409038", fl_w="#F8F8F0", fl_y="#F8D848",
    ink="#182030", pk_hi="#80B8E0", pk="#4888C0", pk_sh="#306098", pk_dk="#203868",
    st_hi="#F0C888", st="#C08848", st_dk="#805030", buckle="#F8E070",
    roll_hi="#F8F0D8", roll="#E0D0A0", roll_sh="#A89868", map="#F8F8E8", map_sh="#C0C0A8", ribbon="#D84838",
)
NIGHT = dict(
    bg="#101830", bg_dk="#081020", bg_hi="#182840", blade="#080818",
    g_hi="#70C8A0", g="#409880", g_md="#287868", g_dk="#185858", fl_w="#D0E0F8", fl_y="#D8C070",
    ink="#080818", pk_hi="#6088C8", pk="#3860A0", pk_sh="#284078", pk_dk="#182850",
    st_hi="#B898A0", st="#886070", st_dk="#583850", buckle="#D8C878",
    roll_hi="#C0C8E0", roll="#98A0C0", roll_sh="#606890", map="#C8D0E8", map_sh="#8890B0", ribbon="#B04858",
)
PALETTES = {"day": DAY, "night": NIGHT}

KEY = {
    "K": "ink", "h": "pk_hi", "B": "pk", "b": "pk_sh", "d": "pk_dk",
    "t": "st_hi", "S": "st", "s": "st_dk", "Y": "buckle",
    "w": "roll_hi", "R": "roll", "r": "roll_sh", "M": "map", "m": "map_sh", "x": "ribbon",
}

def _rle(spec: str) -> str:
    """'.3 K h10 tSs' -> '...Khhhhhhhhhh' + 'tSs': a char with a count, or a literal run."""
    out = []
    for tok in spec.split():
        if len(tok) > 1 and tok[1:].isdigit():
            out.append(tok[0] * int(tok[1:]))
        else:
            out.append(tok)
    return "".join(out)


# 60 x 56, hand-drawn. Bedroll strapped on top with its coiled end showing; the two straps run
# down the lid to buckles; front pocket with a flap and snap; side pocket on the right holding
# a rolled trail map tied with a ribbon; shoulder strap looping out on the left.
_BEDROLL = [          # columns 0..41
    ".13 K29",
    ".11 K2 w6 S3 w15 S3 w2",
    ".10 K w2 R6 tSs R15 tSs R2",
    ".9 K w R8 tSs R15 tSs R2",
    ".9 K w R8 tSs R15 tSs R2",
    ".9 K R4 r4 R tSs R4 r6 R5 tSs R2",
    ".9 K R9 tSs R15 tSs R2",
    ".9 K R2 r5 R2 tSs R8 r5 R2 tSs R2",
    ".9 K R9 SSs R15 SSs R2",
    ".9 K r R8 SSs R15 SSs R2",
    ".10 K r2 R6 SSs R15 SSs r2",
    ".11 K2 r6 SSs r15 SSs r2",
    ".9 K10 SSs K15 SSs K2",
]
_COIL = [             # columns 42..49: the rolled end of the bedroll
    "K.......", "wwKK....", "RRrrK...", "RrrrrK..", "RrKKrrK.", "RrKrKrK.", "RrKrKrK.",
    "RrrKKrK.", "RrrrrrK.", "RrrrrK..", "rrrrK...", "rrKK....", "KKKKKKK.",
]
_MAP_TOP = [".........."] * 7 + [".....KKK.."] + ["....KMMmK."] * 5      # columns 50..59
_LID = "K h B12 tSs B15 tSs B11 b K"
_BODY = ". K h B6 K h B25 b d K B5 b d K ."
_MID = {              # columns 5..52, rows 13..55
    13: ".3 K h10 SSs h15 SSs h9 K .3",
    14: ".2 K h6 B5 tSs B15 tSs B9 b K .2",
    15: ". K h4 B8 tSs B15 tSs B10 b K .",
    16: _LID,
    17: "K h B12 tSs B7 w B7 tSs B11 b K",          # a small mountain patch sewn on the lid
    18: "K h B12 tSs B6 w3 B6 tSs B11 b K",
    19: "K h B12 tSs B5 w h w3 B5 tSs B11 b K",
    20: "K h B12 tSs B4 w h2 w h w2 B4 tSs B11 b K",
    21: _LID,
    22: "K h B2 b8 B2 tSs B2 b11 B2 tSs B2 b7 B2 b K",
    23: "K B13 tSs B15 tSs B11 b K",
    24: "K B13 tSs B15 tSs B11 b K",
    25: "K b B12 tSs B15 tSs B10 b2 K",
    26: "K b B12 YYY B15 YYY B10 b2 K",
    27: "K b2 B11 YKY B15 YKY B9 b3 K",
    28: ". K13 YYY K15 YYY K12 .",
    29: ". K h B11 tSs B15 tSs B9 b d K .",
    30: ". K h B11 tSs B15 tSs B9 b d K .",
    31: ". K h B11 tSs B15 tSs B9 b d K .",
    32: ". K h B11 SSs B15 SSs B9 b d K .",
    33: ". K h B11 K3 B15 K3 B9 b d K .",
    34: ". K h B7 K28 B6 b d K .",
    35: ". K h B6 K h28 K B5 b d K .",
    36: ". K h B6 K B28 K B5 b d K .",
    37: ". K h B6 K B28 K B5 b d K .",
    38: ". K h B6 K B26 b2 K B5 b d K .",
    39: ". K h B6 K B25 b3 K B5 b d K .",
    40: ". K h B6 K3 b24 K3 B5 b d K .",
    41: ". K h B6 K B2 K3 b8 Y2 b8 K3 B2 K B5 b d K .",
    42: ". K h B6 K B5 K8 Y2 K8 B5 K B5 b d K .",
    43: _BODY, 44: _BODY, 45: _BODY, 46: _BODY, 47: _BODY, 48: _BODY, 49: _BODY,
    50: ". K h B7 K b25 d K B6 b d K .",
    51: ". K h B8 K26 B7 b d K .",
    52: ". K h B40 b2 d K .",
    53: ". K B b41 d2 K .",
    54: ".2 K2 d40 K2 .2",
    55: ".4 K40 .4",
}
_STRAP = {17: "...KK ", 18: "..KsS ", 19: ".KsSK ", 42: ".KsSK ", 43: "..KsSS", 44: "...KKK",
          **{y: "KsSK. " for y in range(20, 42)}}                         # columns 0..5; space keeps
_POCKET = {29: "..KMMmK.", 30: "KKKKKKK.", 31: "hhhhhhbK", 32: "hBBBBbdK", 33: "hBBBBbdK", 34: "dddddddK",
           **{y: "hBBBBbdK" for y in range(35, 46)},
           46: "BBBBbbdK", 47: "bbbbbddK", 48: "KKKKKKK."}                 # columns 52..59


def _pack() -> list[str]:
    rows = [_rle(_BEDROLL[y]) + _COIL[y] + _MAP_TOP[y] for y in range(13)]
    for y in range(13, 56):
        tail = ".KxxxK." if y in (20, 21) else ".KMMmK." if y < 29 else "......."
        mid = _MID[y]
        if 36 <= y <= 48 and mid.startswith(". K h B6 "):
            mid = "K h B7 " + mid[len(". K h B6 "):]          # the body bows out a pixel through the middle
        row = list("....." + _rle(mid) + tail)
        for x, ch in enumerate(_STRAP.get(y, "")):
            if ch != " ":
                row[x] = ch
        for x, ch in enumerate(_POCKET.get(y, "")):
            row[52 + x] = ch
        rows.append("".join(row))
    bad = [(y, len(r)) for y, r in enumerate(rows) if len(r) != 60]
    assert not bad, bad
    return rows


PACK = _pack()


RIM_TUFTS = [            # light blades poking up over the far rim of the patch
    ["..c...c", "c.c.c.c", "c.ccc.c", ".ccccc."],
    [".c..c..", ".c.cc.c", "cc.cc.c", ".ccccc."],
    ["c...c", "c.c.c", "ccccc"],
]
FRONT_TUFTS = [          # dark blades in front of the near rim
    ["....f....", "f...f...f", "f..ff..f.", ".f.ff.ff.", ".fffffff.", "..fffff.."],
    ["..f...f..", "..f..ff.f", "f.ff.f.ff", "ff.fff.f.", ".fffffff."],
    ["f..f.", "f.ff.", "fff.f", ".ffff"],
]
FLOWERS = ((66, 70), (80, 84), (93, 62), (156, 66), (168, 80), (150, 88), (74, 58), (176, 70))


def field() -> Canvas:
    c = Canvas(W, H, ROLES)
    c.rect(0, 0, W, H, "bg")
    rng = random.Random(41)
    for _ in range(46):                                # the field stays flat and dark: only short grass marks
        x, y = rng.randrange(W), rng.randrange(4, H - 4)
        role = "bg_hi" if rng.random() < 0.5 else "bg_dk"
        for dx, dy in ((0, 0), (0, -1), (-1, -2), (2, 0), (2, -1), (3, -2)):
            c.put((x + dx) % W, y + dy, role)
    return c


def stamp(c, rows, x0, y0, key, flip=False):
    for dy, row in enumerate(rows):
        row = row[::-1] if flip else row
        for dx, ch in enumerate(row):
            if ch != ".":
                c.put(x0 + dx, y0 + dy, key[ch])


def platform() -> Canvas:
    pw, ph = PLATFORM["w"], PLATFORM["h"]
    c = Canvas(pw, ph, ROLES)
    xs, ys = grid(pw, ph)
    cx, cy, rx, ry = PATCH["cx"] - OX, PATCH["cy"] - OY, PATCH["rx"], PATCH["ry"]
    rag = tile_noise(pw, ph, 9, 3) * 0.16 - 0.08       # ragged rim instead of a clean ellipse
    d = ((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2 + rag
    chk = checker(pw, ph)

    # glow spilling onto the dark field, then the patch: brightest in the middle
    c.paint((d < 1.22) & chk, "bg_hi")
    c.paint((d < 1.1), "bg_hi")
    c.paint(d < 1.0, "g_md")
    c.paint((d < 0.86) & chk, "g")
    c.paint(d < 0.74, "g")
    c.paint((d < 0.5) & chk, "g_hi")
    c.paint(d < 0.36, "g_hi")
    # a shaded lower lip, so the patch reads as a low mound
    lip = (d < 1.0) & (d > 0.8) & (ys > cy + 6)
    c.paint(lip & chk, "g_dk")

    rng = random.Random(9)
    # texture: short blade ticks across the patch
    for _ in range(120):
        x, y = rng.randrange(pw), rng.randrange(ph)
        if d[y, x] < 0.9:
            role = "g_md" if d[y, x] < 0.6 else "g_dk"
            c.put(x, y, role)
            if y > 0:
                c.put(x + rng.choice((-1, 0, 1)), y - 1, role)
    for fx, fy in FLOWERS:
        x, y = fx - OX, fy - OY
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            c.put(x + dx, y + dy, "fl_w")
        c.put(x, y, "fl_y")

    # far rim: lighter tufts poking up into the dark
    for i, t in enumerate(np.linspace(np.pi * 1.06, np.pi * 1.94, 13)):
        rows = RIM_TUFTS[i % len(RIM_TUFTS)]
        x = int(cx + np.cos(t) * rx * 0.97) - len(rows[0]) // 2 + rng.randint(-2, 2)
        y = int(cy + np.sin(t) * ry * 0.97) - len(rows) + 2
        stamp(c, rows, x, y, {"c": "g_md" if i % 2 else "g"}, flip=bool(i % 2))

    # shadow under the pack, then the pack itself
    sx, sy = PACK_X + 29 - OX, PACK_Y + 55 - OY
    sd = ((xs - sx) / 34) ** 2 + ((ys - sy) / 6) ** 2
    c.paint((sd < 1.0) & chk, "g_dk")
    c.paint(sd < 0.7, "g_dk")
    stamp(c, PACK, PACK_X - OX, PACK_Y - OY, KEY)
    for dx, rows, role in ((4, RIM_TUFTS[2], "g_md"), (24, RIM_TUFTS[0], "g"), (45, RIM_TUFTS[1], "g_md"), (56, RIM_TUFTS[2], "g")):
        stamp(c, rows, PACK_X + dx - OX, PACK_Y + 57 - len(rows) - OY, {"c": role})   # blades in front of its base

    # near rim: dark blades in front
    for i, t in enumerate(np.linspace(np.pi * 0.08, np.pi * 0.92, 12)):
        rows = FRONT_TUFTS[i % len(FRONT_TUFTS)]
        x = int(cx + np.cos(t) * rx * 0.98) - len(rows[0]) // 2 + rng.randint(-2, 2)
        y = int(cy + np.sin(t) * ry * 0.98) - len(rows) + 3
        stamp(c, rows, x, y, {"f": "blade" if i % 3 else "bg_dk"}, flip=bool(i % 2))
    return c


def build(variant: str) -> Variant:
    pal = PALETTES[variant]
    v = Variant()
    v.layers.append(Layer(f"{variant}/00-field.png", field().to_rgba(pal), 0, 1, 0))
    v.platform = platform().to_rgba(pal)
    v.platform_file = f"{variant}/platform.png"
    return v
