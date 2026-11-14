"""Grass habitat: an alpine meadow under a snow-capped Colorado range, with a winding trail.

Shares the lake habitat's roles, sky, clouds, tree ridge and mountain drawing; the lake rows
become a meadow whose wind lines travel the same way the lake's wave lines do.
"""
from __future__ import annotations

import math
import random

import numpy as np

from common import H, W, Canvas, Layer, Variant, grid, periodic_profile, tile_noise
from habitats import water as base
from habitats.water import ROLES, Swell, _runs, conifer, lobe

NAME = "grass"
FIELD_Y = 58           # first meadow row
WIDE = W * 2
FRAMES = 16            # wind loop; must match the Swell period
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
PALETTES = {"day": DAY, "night": NIGHT}

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
FLOWERS = [(22, 70), (44, 92), (70, 66), (96, 101), (118, 74), (132, 96), (232, 70), (226, 99), (250, 84),
           (274, 67), (296, 95), (322, 72), (350, 100), (372, 80), (398, 64), (416, 92), (440, 74), (462, 98),
           (12, 100), (58, 80), (104, 62), (308, 62), (384, 104), (474, 66)]
# The trail winds from the near bank up to the tree line: (centre x, y), widening as it nears.
TRAILS = [[(98, 58), (94, 62), (86, 66), (84, 71), (90, 77), (100, 83), (104, 90), (96, 98), (80, 106), (62, 116), (50, 128)],
          [(352, 58), (357, 63), (366, 67), (368, 73), (360, 79), (348, 86), (344, 94), (352, 102), (370, 110), (392, 120), (404, 130)]]


def _trail_mask():
    """(dirt, shaded edge) masks for the winding trails."""
    xs, ys = grid(WIDE)
    dirt = np.zeros((H, WIDE), bool)
    edge = np.zeros((H, WIDE), bool)
    for pts in TRAILS:
        py = [p[1] for p in pts]
        px = [p[0] for p in pts]
        for y in range(pts[0][1], min(H, pts[-1][1] + 1)):
            cx = float(np.interp(y, py, px))
            half = 0.6 + (y - FIELD_Y) * 0.085
            row = np.abs(np.arange(WIDE) - cx) <= half
            dirt[y] |= row
            edge[y] |= row & (np.arange(WIDE) - cx > half - 1.2)      # the side away from the light
    return dirt, edge


def meadow() -> Canvas:
    c = cv(H * FRAMES, WIDE)
    xs, ys = grid(WIDE)
    rng = random.Random(23)
    edge_sw = [Swell(rng, la, lb) for la, lb in ((12, 20), (16, 30), (24, 40), (32, 48))]
    lines = []
    y, i = FIELD_Y + 2, 0
    while y < 124:
        depth = min(1.0, (y - FIELD_Y) / 50)
        la = (8, 10, 12, 15, 16, 20, 24, 30)[min(7, int(depth * 6) + rng.randint(0, 2))]
        lines.append(dict(y=y, sw=Swell(rng, la, rng.choice((12, 16, 20, 24, 30, 40))), amp=0.6 + 1.5 * depth,
                          lit=i % 3 != 1, noise=tile_noise(WIDE, 1, (16, 24, 40)[min(2, int(depth * 3))], 40 + i)[0],
                          ex=rng.random() * math.tau, el=(24, 30, 40, 48, 60)[min(4, int(depth * 4) + 1)]))
        y += 2 + int(round(depth * 1.8))
        i += 1
    dirt, shade = _trail_mask()

    for f in range(FRAMES):
        oy = f * H
        t = f / FRAMES
        band = np.zeros((H, WIDE), np.int32)
        for b in range(1, len(BANDS)):          # rolling ground: the tone edges breathe with the wind
            edge = EDGES[b] - np.rint((0.8 + 0.4 * b) * edge_sw[b - 1].height(f)).astype(int)
            band += ys >= edge[None, :]
        for b, role in enumerate(BANDS):
            c.a[oy:oy + H][(band == b) & (ys >= FIELD_Y)] = ROLES[role]
        for ln in lines:                         # gusts: bent grass catches the light as each wave passes
            h = ln["sw"].height(f)
            env = ln["noise"] + 0.22 * np.sin(math.tau * (np.arange(WIDE) / ln["el"] - t) + ln["ex"]) + 0.18 * h
            on = _runs(env > np.quantile(ln["noise"], 0.58 if ln["lit"] else 0.66), 3)
            yy = ln["y"] - np.rint(ln["amp"] * h).astype(int)
            for x in np.nonzero(on)[0]:
                if not FIELD_Y < yy[x] < H:
                    continue
                k = LADDER.index(BANDS[band[yy[x], x]])
                c.put(x, yy[x] + oy, LADDER[k - 1] if ln["lit"] else LADDER[k + 1])
        fr = c.a[oy:oy + H]
        fr[dirt] = ROLES["d_lit"]
        fr[dirt & shade] = ROLES["d_sh"]
        fr[dirt & ~shade & (((xs * 3 + ys * 5) % 11) == 0)] = ROLES["d_hi"]     # pebbles on the path
        for j, (x, y) in enumerate(FLOWERS):     # wildflowers nod in turn
            st = (f // 2 + j) % 8
            c.put(x, y + oy - (1 if st == 0 else 0), "hl" if j % 2 else "spark2")
            c.put(x, y + 1 + oy, "dock_shadow")
            if st in (0, 1) and j % 3 == 0:
                c.put(x + 1, y + oy, "wv")
    return c


# -------------------------------------------------------------------------------- shore
BANK = [(0, 104), (26, 100), (60, 103), (96, 107), (140, 109), (190, 110), (240, 107), (280, 103),
        (320, 105), (370, 109), (430, 110)]
PINES = [(8, [(3, 8), (5, 9), (7, 9), (9, 10)]), (24, [(3, 8), (5, 9), (7, 9)]), (40, [(3, 7), (5, 8)]),
         (224, [(3, 7), (5, 8)]), (236, [(3, 8), (5, 9), (7, 9)]),
         (262, [(3, 8), (5, 9)]), (278, [(3, 7), (4, 8)]), (446, [(3, 7), (5, 8)]), (460, [(3, 8), (5, 9), (7, 9), (9, 10)]),
         (474, [(3, 8), (5, 9), (7, 9)])]
BOULDERS = [(118, 4), (125, 3), (202, 4), (332, 4), (339, 3), (410, 3)]
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
    for x, r in BOULDERS:                         # granite boulders half-sunk in the grass
        lobe(c, x, int(prof[x]) + 1, r, ROCK, clip_y=int(prof[x]) + 3)
    key = {"K": "d_dk", "H": "d_hi", "L": "d_lit", "S": "d_sh"}
    for j, row in enumerate(SIGN):                # trail sign beside the path
        for i, ch in enumerate(row):
            if ch != ".":
                c.put(66 + i, 93 + j, key[ch])
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
    add("20-peaks.png", base.peaks(ridgeline=RIDGE, snowline=27))
    add("25-ridge.png", base.ridge()[0])
    add("30-meadow.png", meadow(), frames=FRAMES, fps=8)
    add("40-shore.png", shore())
    v.platform = base.platform().to_rgba(pal)     # the lake's island, re-inked as a putting green
    v.platform_file = f"{variant}/platform.png"
    return v
