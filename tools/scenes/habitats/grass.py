"""Grass habitat: an alpine meadow under a snow-capped Colorado range, with a winding trail.

Shares the lake habitat's roles, sky, clouds, tree ridge and mountain drawing; the lake rows
become a meadow whose wind lines travel the same way the lake's wave lines do.
"""
from __future__ import annotations

import math
import random

import numpy as np

from common import H, W, Canvas, Layer, Variant, grid, periodic_profile, sky_ramp, tile_noise
from habitats import water as base
from habitats.water import ROLES, TREE, Swell, _runs, conifer, dome, lobe

NAME = "grass"
FIELD_Y = 58           # first meadow row
WIDE = W * 2
FRAMES = 32            # one long, slow wind loop
PLATFORM = dict(file="platform.png", w=96, h=24, cx=176, cy=80)

# The lake palette with the water and beach roles re-inked as grass and a putting green.
DAY = {**base.DAY,
       "w0": "#B8E870", "w1": "#98D858", "w2": "#78C848", "w3": "#58B040", "w4": "#409838",
       "wv": "#D8F890", "hl": "#F8F8E0", "spark2": "#F8E060", "dock_shadow": "#2C7838",
       "sand": "#90D858", "sand_hi": "#C0F078", "sand_sh": "#58A840", "sand_wet": "#388838",
       "foam": "#D8F890", "cshadow": "#4CA03C", "pebble": "#F8F8E0"}
NIGHT = {**base.NIGHT,
         "w0": "#2C7868", "w1": "#246860", "w2": "#1C5858", "w3": "#184850", "w4": "#103C48",
         "wv": "#48A088", "hl": "#B0F0E0", "spark2": "#F0E890", "dock_shadow": "#0C2C3C",
         "sand": "#2C7060", "sand_hi": "#48A080", "sand_sh": "#1C5050", "sand_wet": "#103840",
         "foam": "#48A088", "cshadow": "#184848", "pebble": "#B0F0E0"}
PALETTES = {"day": sky_ramp(DAY), "night": sky_ramp(NIGHT)}

# Hand-placed ridgeline (x, top y), periodic over 480. Each mountain is a different size and shape:
# low foothills, one broad massif with its summit at x=128 (in the gap between the info panel and
# the creature), a pair of narrow spires, a wide rounded dome, and a tall thin horn.
RIDGE = [
    (0, 44), (8, 42), (15, 43), (22, 39), (28, 36), (33, 38), (40, 42), (48, 41), (55, 44), (62, 42),
    (68, 38), (74, 36), (79, 37), (84, 31), (88, 29), (92, 27), (96, 29), (100, 26), (105, 22), (110,
    20), (114, 16), (118, 15), (122, 11), (125, 10), (128, 9), (131, 11), (134, 15), (137, 14), (140,
    20), (143, 26), (146, 30), (150, 37), (155, 41), (162, 44), (170, 42), (178, 45), (186, 43), (194,
    45), (200, 40), (205, 33), (209, 26), (212, 22), (214, 20), (216, 23), (219, 24), (222, 19), (224,
    16), (226, 15), (228, 18), (231, 25), (234, 31), (238, 36), (244, 40), (250, 38), (256, 34), (262,
    31), (268, 28), (274, 27), (280, 25), (286, 24), (290, 23), (295, 25), (300, 24), (306, 27), (312,
    30), (318, 34), (324, 38), (330, 41), (338, 43), (346, 40), (352, 42), (360, 44), (368, 41), (376,
    43), (382, 38), (387, 31), (391, 25), (395, 19), (399, 14), (402, 12), (404, 11), (406, 14), (409,
    19), (412, 23), (416, 27), (420, 29), (425, 30), (430, 34), (436, 39), (442, 42), (450, 40), (458,
    44), (466, 42), (474, 45), (480, 44)]


def cv(h=H, w=W) -> Canvas:
    return Canvas(w, h, ROLES)


# ------------------------------------------------------------------------------ meadow
BANDS = ["w0", "w1", "w2", "w3", "w4"]
EDGES = [FIELD_Y, 63, 72, 84, 98]
LADDER = ["wv"] + BANDS + ["dock_shadow"]      # sunlit to shaded
FLOWERS = [(22, 70), (44, 92), (70, 66), (118, 74), (132, 96), (232, 70), (226, 99), (250, 84),
           (274, 67), (296, 95), (322, 72), (372, 80), (398, 64), (416, 92), (440, 74), (462, 98),
           (12, 100), (58, 80), (112, 62), (308, 62), (424, 104), (474, 66), (148, 66), (210, 88)]
# Wildflower patches in the near meadow: loose groups, the way they grow in drifts.
PATCHES = [(16, 90), (22, 95), (28, 89), (120, 99), (127, 95), (114, 96), (62, 86), (68, 91),
           (230, 95), (236, 90), (262, 92), (268, 97), (257, 99), (310, 88), (316, 93), (305, 94),
           (384, 96), (390, 91), (378, 99), (446, 90), (452, 95), (440, 97), (474, 88), (4, 96),
           (200, 98), (207, 95), (150, 98), (158, 96)]
# The trail winds from the near bank up to the tree line: (centre x, y). It widens with
# perspective and carries on across the foreground bank.
TRAILS = [[(98, 58), (95, 62), (88, 66), (85, 71), (90, 77), (99, 83), (103, 90), (97, 98), (84, 106), (68, 116), (52, 130), (40, 160)],
          [(352, 58), (356, 63), (364, 67), (367, 73), (360, 79), (349, 86), (345, 94), (352, 102), (368, 110), (388, 120), (404, 132), (416, 160)]]


def trail_masks():
    """(dirt, edge, rut, worn) masks for the winding trails over one 480-wide frame."""
    cols = np.arange(WIDE)
    dirt, edge, rut, worn = (np.zeros((H, WIDE), bool) for _ in range(4))
    for pts in TRAILS:
        py, px = [p[1] for p in pts], [p[0] for p in pts]
        for y in range(pts[0][1], H):
            cx = float(np.interp(y, py, px))
            half = 1.0 + (y - FIELD_Y) * 0.14                       # 2px at the trees, about 16px at the bank
            off = cols - cx
            row = np.abs(off) <= half
            dirt[y] |= row
            edge[y] |= row & (np.abs(off) > half - (1.0 if half < 4 else 1.6))      # darker lips under the grass
            if half >= 3.5:
                for side in (-0.42, 0.42):                           # two worn ruts, broken so they are not ruled lines
                    rut[y] |= (np.abs(off - side * half) < 0.6) & ((y + int(cx)) % 5 != 0)
                worn[y] |= (np.abs(off) < half * 0.16) & ((y * 3 + int(cx)) % 4 != 0)
    return dirt, edge & dirt, rut & dirt, worn & dirt


# Lone trees dotted over the meadow, smaller with distance, as on the title screen's hills.
# Round trees: (x, ground y, r). Pines: (x, ground y, tiers top to bottom as (half width, height)).
ROUNDS = [(34, 74, 4), (118, 66, 3), (233, 71, 3), (300, 75, 4), (420, 66, 3), (186, 62, 2), (372, 63, 2)]
PINES_FAR = [(14, 67, [(2, 4), (3, 5)]), (56, 65, [(2, 4), (3, 5)]), (246, 64, [(1, 3), (2, 4)]),
             (276, 69, [(2, 4), (3, 5), (4, 5)]), (330, 64, [(1, 3), (2, 4)]), (396, 73, [(2, 4), (3, 5), (4, 6)]),
             (458, 68, [(2, 4), (3, 5)]), (140, 62, [(1, 3), (2, 4)])]


def _trees(ground: Canvas):
    """Draw the meadow trees into the ground canvas; returns the mask they cover."""
    before = ground.a.copy()
    for x, y, r in ROUNDS:
        for dx in range(-r, r + 3):                     # contact shadow, thrown right
            ground.put(x + dx + 1, y, "dock_shadow")
            if abs(dx) < r:
                ground.put(x + dx + 2, y + 1, "dock_shadow")
        for yy in range(y - 2, y + 1):
            ground.put(x, yy, "tr_lit")
            ground.put(x + 1, yy, "tr_dk")
        lobe(ground, x - r + 1, y - r - 1, r - 1 if r > 2 else r, TREE, under=False)
        lobe(ground, x + r - 1, y - r - 1, r - 1 if r > 2 else r, TREE, under=False)
        lobe(ground, x, y - 2 * r, r, TREE, under=False)
        lobe(ground, x, y - r - 2, r, TREE)
    for x, y, tiers in PINES_FAR:
        hw = tiers[-1][0]
        for dx in range(-hw + 1, hw + 3):
            ground.put(x + dx + 1, y, "dock_shadow")
        ground.put(x, y - 1, "tr_dk")
        ground.put(x, y, "tr_dk")
        yb = y - 1
        for hw, th in reversed(tiers):                  # bottom tier first
            dome(ground, x, yb, hw, th, TREE)
            yb -= th - 2
    return ground.a != before


def _tufts():
    """Grass tufts from the tree line to the bank: (x, base y, height). Bigger and sparser up close."""
    rng = random.Random(23)
    out = []
    y = FIELD_Y + 2
    while y < 126:
        depth = min(1.0, (y - FIELD_Y) / 50)
        h = 2 + int(round(depth * 3))
        gap = 4 + int(round(depth * 5))
        x = rng.randint(0, gap)
        while x < WIDE:
            out.append((x, y + rng.randint(0, 1), h + rng.choice((-1, 0, 0, 1))))
            x += gap + rng.randint(-1, 2)
        y += 2 + int(round(depth * 2))
    return out


def gust(x, y, f):
    """Wind strength 0..1 at a point. The gusts run right to left, like the clouds, and only a
    little faster: each crosses 40-60 art pixels in the whole loop."""
    t = f / FRAMES
    a = math.sin(math.tau * (x / 60 + t) + y * 0.11)
    b = math.sin(math.tau * (x / 40 + t) + y * 0.23)
    return 0.5 + 0.5 * (0.7 * a + 0.3 * b)


def meadow() -> Canvas:
    c = cv(H * FRAMES, WIDE)
    xs, ys = grid(WIDE)
    rng = random.Random(29)
    # the ground: flat tones whose edges are ragged with grass, not ruled bands
    rag = [np.array([rng.choice((0, 0, 1, 1, 2)) for _ in range(WIDE)]) for _ in BANDS]
    band = np.zeros((H, WIDE), np.int32)
    for b in range(1, len(BANDS)):
        band += ys >= (EDGES[b] - rag[b])[None, :]
    ground = cv(H, WIDE)
    for b, role in enumerate(BANDS):
        ground.a[(band == b) & (ys >= FIELD_Y)] = ROLES[role]
    dirt, edge, rut, worn = trail_masks()
    ground.a[dirt] = ROLES["d_lit"]
    ground.a[worn] = ROLES["d_hi"]
    ground.a[rut] = ROLES["d_sh"]
    ground.a[edge] = ROLES["d_sh"]
    ground.a[dirt & ~edge & (((xs * 7 + ys * 13) % 37) == 0)] = ROLES["d_dk"]      # scattered pebbles
    trees = _trees(ground)
    tufts = [t for t in _tufts() if not dirt[min(H - 1, t[1]), t[0] % WIDE]
             and not trees[min(H - 1, t[1]), t[0] % WIDE] and not trees[max(0, t[1] - 2), t[0] % WIDE]]
    blooms = [(x, y) for x, y in FLOWERS + PATCHES
              if not dirt[y, x % WIDE] and not trees[y - 3:y + 1, (x - 1) % WIDE:(x + 2) % WIDE].any()]

    for f in range(FRAMES):
        oy = f * H
        c.a[oy:oy + H] = ground.a
        for x, y, h in tufts:                       # each blade leans left as a gust passes over it
            g = gust(x, y, f)
            lean = 0 if g < 0.38 else 1 if g < 0.72 else 2
            here = BANDS[band[min(H - 1, y), x]]
            k = LADDER.index(here)
            dark, tip = LADDER[min(k + 1, len(LADDER) - 1)], LADDER[k - 1]
            for blade, (bx, bh) in enumerate(((x, h), (x + 2, h - 1), (x - 2, h - 1))):
                for j in range(bh):
                    shift = 0 if j < bh - lean else -(j - (bh - lean) + 1)   # only the top of the blade bends
                    role = tip if j == bh - 1 else dark if blade == 0 else here
                    if j == bh - 1 and lean == 2 and h >= 4:
                        role = "wv"                                          # pale underside flashing in a strong gust
                    c.put((bx + shift) % WIDE, y - j + oy, role)
        for j, (x, y) in enumerate(blooms):         # wildflowers bob with the same gusts
            g = gust(x, y, f)
            dx = 0 if g < 0.5 else -1
            c.put(x, y + oy, "dock_shadow")
            if y < 78:                              # far off: a dot of colour on a stem
                c.put(x + dx, y - 1 + oy, ("hl", "spark2", "fl")[j % 3])
                if g > 0.8:
                    c.put(x + dx - 1, y - 1 + oy, "wv")
            elif j % 3 == 2:                        # near: an orange bloom with a lit petal
                c.put(x, y - 1 + oy, "dock_shadow")
                for ax, ay in ((0, -2), (1, -2), (0, -3), (1, -3)):
                    c.put(x + dx + ax, y + ay + oy, "fl")
                c.put(x + dx, y - 3 + oy, "spark2")
            else:                                   # near: a daisy, four petals round a yellow eye
                c.put(x, y - 1 + oy, "dock_shadow")
                for ax, ay in ((-1, -3), (1, -3), (0, -2), (0, -4)):
                    c.put(x + dx + ax, y + ay + oy, "hl")
                c.put(x + dx, y - 3 + oy, "spark2")
    return c


# -------------------------------------------------------------------------------- shore
BANK = [(0, 104), (26, 100), (60, 103), (96, 107), (140, 109), (190, 110), (240, 107), (280, 103),
        (320, 105), (370, 109), (430, 110)]
PINES = [(8, [(3, 8), (5, 9), (7, 9), (9, 10)]), (24, [(3, 8), (5, 9), (7, 9)]), (40, [(3, 7), (5, 8)]),
         (224, [(3, 7), (5, 8)]), (236, [(3, 8), (5, 9), (7, 9)]),
         (262, [(3, 8), (5, 9)]), (278, [(3, 7), (4, 8)]), (446, [(3, 7), (5, 8)]), (460, [(3, 8), (5, 9), (7, 9), (9, 10)]),
         (474, [(3, 8), (5, 9), (7, 9)])]
BOULDERS = [(118, 4), (125, 3), (202, 4), (332, 4), (339, 3), (410, 3)]
BANK_BLOOMS = [56, 61, 104, 136, 142, 150, 168, 176, 190, 214, 300, 308, 318, 360, 366, 392, 428, 434]
ROCK = ["pk_hi", "pk_lit", "pk_base", "pk_sh"]
SIGN = ["KKKKKKKKKKKKK.",
        "KHHHHHHHHHHHKK",
        "KLLLLLKLLLLLLK",
        "KLKKKKKKLLLLKK",
        "KLLLLLKLLLLLK.",
        "KSSSSSSSSSSSK.",
        "KKKKKKKKKKKKK.",
        ".....KLS......",
        ".....KLS......",
        ".....KLS......",
        ".....KLS......",
        ".....KLS......"]


def shore() -> Canvas:
    c = cv(H, WIDE)
    xs, ys = grid(WIDE)
    prof = periodic_profile(BANK, WIDE)
    rng = random.Random(5)
    blade = np.array([rng.choice((0, 0, 1, 1, 2, 3)) for _ in range(WIDE)])    # ragged grass edge
    top = prof - blade
    d = ys - top[xs]
    ground = d >= 0
    n = tile_noise(WIDE, 64, 16, 31)[(ys - 96) % 64, xs]
    c.paint(ground, "g_base")
    c.paint(ground & (n > 0.6), "g_lit")
    c.paint(ground & (n < 0.34), "g_sh")
    c.paint(ground & (d <= 1), "g_lit")
    c.paint(ground & (d == 0), "g_hi")
    c.paint(ground & (ys >= 150), "g_sh")
    dirt, edge, rut, worn = trail_masks()             # the trail carries on across the bank
    c.paint(ground & dirt, "d_lit")
    c.paint(ground & worn, "d_hi")
    c.paint(ground & (rut | edge), "d_sh")
    for x, r in BOULDERS:                         # granite boulders half-sunk in the grass
        lobe(c, x, int(prof[x]) + 1, r, ROCK, clip_y=int(prof[x]) + 3)
    key = {"K": "d_dk", "H": "d_hi", "L": "d_lit", "S": "d_sh"}
    for j, row in enumerate(SIGN):                # trail sign beside the path
        for i, ch in enumerate(row):
            if ch != ".":
                c.put(66 + i, 93 + j, key[ch])
    for j, x in enumerate(BANK_BLOOMS):           # wildflowers along the top of the bank
        if dirt[int(prof[x]), x]:
            continue
        y = int(prof[x]) - 1
        c.put(x, y + 1, "g_sh")
        c.put(x, y, "g_sh")
        if j % 3 == 2:
            for ax, ay in ((0, -1), (1, -1), (0, -2), (1, -2)):
                c.put(x + ax, y + ay, "fl")
            c.put(x, y - 2, "spark2")
        else:
            for ax, ay in ((-1, -2), (1, -2), (0, -1), (0, -3)):
                c.put(x + ax, y + ay, "hl")
            c.put(x, y - 2, "spark2")
    for x, tiers in PINES:
        conifer(c, x, int(prof[x]) + 3, tiers)
    return c


# -------------------------------------------------------------------------------- build
def build(variant: str) -> Variant:
    night = variant == "night"
    pal = PALETTES[variant]
    v = Variant()

    def add(file, canvas, drift=0, frames=1, fps=0):
        v.layers.append(Layer(f"{variant}/{file}", canvas.to_rgba(pal), drift, frames, fps))

    add("00-sky.png", base.sky(night))
    if night:
        add("05-stars.png", base.stars(), frames=4, fps=3)
    add("10-clouds.png", base.clouds(), drift=-2)
    add("12-cumulus.png", base.cumulus(base=52), drift=-1)
    add("20-peaks.png", base.peaks(ridgeline=RIDGE, snowline=27))
    add("25-ridge.png", base.ridge()[0])
    add("30-meadow.png", meadow(), frames=FRAMES, fps=2)
    add("40-shore.png", shore())
    v.platform = base.platform().to_rgba(pal)     # the lake's island, re-inked as a putting green
    v.platform_file = f"{variant}/platform.png"
    return v
