"""Fire habitat: a still lava lake that bubbles, under a smoking volcano, red-rock mesas and a basalt bank.

Same layout and lighting as the water habitat (horizon at row 58, key light top-left,
platform at 176,80). Day and night share all geometry; only the palette changes.
"""
from __future__ import annotations

import math
import random

import numpy as np

from common import (BAYER4, H, SKY_ROLES, W, Canvas, Layer, RoleSet, Variant, banded, checker, gradient, grid,
                    periodic_profile, sky_ramp, tile_noise)
from habitats.water import LARGE, MEDIUM, SMALL, STARS_DOT, STARS_PLUS, lobe
from habitats.water import peaks as range_layer

NAME = "fire"
LAVA_Y = 58            # first lava row
MOON = (34, 22, 7)     # cx, cy, r (night)
WIDE = W * 2
FRAMES = 16            # lava loop; must match the Swell period
PLATFORM = dict(file="platform.png", w=96, h=24, cx=176, cy=80)

ROLES = RoleSet([
    "sky0", "sky1", "sky2", "sky3", "sky4", "hz",
    "s_hi", "s_lit", "s_base", "s_sh",
    "v_far", "v_far_sh", "vk_hi", "vk_lit", "vk_base", "vk_sh", "vk_dk",
    "m_hi", "m_lit", "m_base", "m_dk", "m_band",
    "l0", "l1", "l2", "l3", "l4", "lw", "crust", "crust_hi", "crust_dk",
    "b_glow", "b_hi", "b_lit", "b_base", "b_sh", "b_dk",
    "a_hi", "a_lit", "a_dk",
    "sm0", "sm1", "sm2", "sm3", "sm4",
    "moon", "moon_sh", "glow", "star1", "star2",
])

DAY = dict(
    sky0="#3070D8", sky1="#5088E0", sky2="#78A0E0", sky3="#A8B4D8", sky4="#E0C0B0", hz="#F8D8A0",
    s_hi="#F8F0E8", s_lit="#D8C8C8", s_base="#A898A8", s_sh="#786880",
    v_far="#C0A0A0", v_far_sh="#A08890",
    vk_hi="#C89080", vk_lit="#A06868", vk_base="#805060", vk_sh="#603C58", vk_dk="#482C48",
    m_hi="#F8B870", m_lit="#E08850", m_base="#C06040", m_dk="#883838", m_band="#F0A060",
    l0="#F8E868", l1="#F8C040", l2="#F89828", l3="#F07018", l4="#D05018", lw="#F8F8C0",
    crust="#703040", crust_hi="#A85040", crust_dk="#482030",
    b_glow="#F09048", b_hi="#B098A0", b_lit="#887080", b_base="#605068", b_sh="#483858", b_dk="#302040",
    a_hi="#E0E8F0", a_lit="#9098B0", a_dk="#505870",
    moon="#F8F4D0", moon_sh="#C8C8E0", glow="#582848", star1="#FFFFFF", star2="#F8D8A0",
)

NIGHT = dict(
    sky0="#100820", sky1="#1C1030", sky2="#301838", sky3="#482038", sky4="#702838", hz="#A04030",
    s_hi="#B88080", s_lit="#805068", s_base="#583850", s_sh="#382038",
    v_far="#482848", v_far_sh="#381C38",
    vk_hi="#985858", vk_lit="#603048", vk_base="#482440", vk_sh="#301830", vk_dk="#201020",
    m_hi="#D07848", m_lit="#904040", m_base="#683040", m_dk="#401C30", m_band="#B05848",
    l0="#F8E868", l1="#F8B830", l2="#F08818", l3="#D86018", l4="#A83818", lw="#F8F8C0",
    crust="#501C28", crust_hi="#883028", crust_dk="#300C18",
    b_glow="#E07030", b_hi="#886078", b_lit="#583858", b_base="#402848", b_sh="#281838", b_dk="#180C20",
    a_hi="#B0B8D8", a_lit="#606490", a_dk="#303050",
    moon="#F8F4D0", moon_sh="#C8C8E0", glow="#582848", star1="#F8F4D0", star2="#F0A878",
)
PALETTES = {"day": sky_ramp(DAY), "night": sky_ramp(NIGHT)}
SMOKE = ["s_hi", "s_lit", "s_base", "s_sh"]


def cv(h=H, w=W) -> Canvas:
    return Canvas(w, h, ROLES)


# ------------------------------------------------------------------------------- sky
def sky(night: bool) -> Canvas:
    sw = WIDE if night else W  # night is 480 wide so the moon is not repeated
    c = cv(H, sw)
    gradient(c, 0, 56, SKY_ROLES, ease=0.9)        # one smooth blend, top to horizon
    if night:
        mx, my, r = MOON
        xs, ys = grid(sw)
        d2 = (xs - mx) ** 2 + (ys - my) ** 2
        fall = np.clip(1 - (np.sqrt(d2) - (r + 2)) / 11.0, 0, 1)      # soft halo, thinning out through a dither
        c.paint(fall > BAYER4[ys % 4, xs % 4], "glow")
        m = d2 <= r * r + r
        c.paint(m, "moon")
        c.paint(m & ~((xs - (mx - 2)) ** 2 + (ys - (my - 2)) ** 2 <= r * r + r), "moon_sh")
    return c


def stars() -> Canvas:
    """Four frames stacked: plus-stars pulse, dots dim and flicker out of phase."""
    c = cv(H * 4)
    for f in range(4):
        oy = f * H
        for i, (x, y) in enumerate(STARS_PLUS):
            c.put(x, y + oy, "star1")
            if (f + i) % 4 == 0:
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    c.put(x + dx, y + dy + oy, "star2")
        for i, (x, y) in enumerate(STARS_DOT):
            st = (f + i) % 4
            if y > 34 or (i % 3 == 0 and st == 0):
                continue  # none in the horizon glow; some blink off
            c.put(x, y + oy, "star2" if st == 2 else "star1")
    return c


def puffs(c: Canvas, items):
    """Round smoke puffs with a flat shaded underside."""
    for cx, base, lobes in items:
        for dx, r in lobes:
            lobe(c, cx + dx, base - r + 1, r, SMOKE, under=False, clip_y=base)
        m = c.a != 0
        below2 = np.zeros_like(m)
        below2[:-2] = m[2:]
        local = np.zeros_like(m)
        local[max(0, base - 12):base + 1, max(0, cx - 30):cx + 31] = True
        c.paint(m & ~below2 & local, "s_sh")


def clouds() -> Canvas:
    c = cv(H, WIDE)
    puffs(c, [(44, 41, MEDIUM), (206, 15, SMALL), (300, 37, LARGE), (446, 22, MEDIUM)])
    return c


# ---------------------------------------------------------------------------- volcano
FAR = [(0, 49), (22, 43), (40, 47), (66, 41), (90, 46), (150, 44), (186, 40), (214, 46), (240, 44),
       (268, 39), (296, 45), (330, 42), (360, 47), (420, 43), (452, 40), (470, 46), (480, 49)]
# Hand-placed ridgeline (x, top y), periodic over 480. Each mountain is a different size and shape:
# a small butte, one broad volcano with its crater at x=130 (in the gap between the info panel and
# the creature), low badlands, a narrow spire, and a lower, wider second volcano with its crater at x=375.
RIDGE = [
    (0, 45), (7, 43), (13, 44), (19, 40), (24, 41), (29, 35), (33, 32), (36, 30), (39, 31), (43, 36),
    (48, 40), (55, 43), (62, 41), (69, 44), (75, 40), (80, 36), (85, 34), (89, 30), (93, 29), (97, 25),
    (101, 24), (105, 20), (109, 21), (113, 17), (117, 18), (121, 14), (124, 13), (127, 16), (130, 17),
    (133, 15), (136, 13), (139, 15), (143, 19), (147, 18), (151, 23), (156, 25), (160, 30), (165, 31),
    (170, 36), (176, 40), (183, 43), (190, 41), (198, 45), (206, 43), (214, 45), (222, 42), (230, 44),
    (238, 40), (244, 35), (249, 29), (253, 24), (257, 20), (260, 18), (262, 17), (264, 19), (267, 25),
    (270, 29), (274, 34), (279, 38), (285, 42), (292, 44), (300, 42), (308, 45), (316, 43), (324, 45),
    (332, 41), (338, 38), (344, 36), (350, 31), (355, 29), (359, 25), (363, 22), (367, 20), (371, 23),
    (375, 24), (379, 21), (383, 20), (387, 23), (392, 27), (397, 29), (402, 34), (408, 36), (414, 40),
    (421, 43), (428, 41), (436, 44), (444, 42), (452, 45), (460, 43), (468, 45), (474, 44), (480, 45)]
CRATERS = [(125, 135), (368, 382)]
# Lava spills from each crater and wanders down the gullies.
STREAMS = [
    [(129, 18), (128, 22), (130, 26), (129, 30), (126, 34), (127, 38), (124, 42), (125, 46), (122, 50), (123, 57)],
    [(134, 16), (137, 20), (138, 24), (142, 27), (143, 31), (147, 34), (148, 38), (153, 42), (155, 47), (159, 51), (160, 57)],
    [(124, 14), (120, 19), (119, 23), (115, 27), (114, 31), (110, 35)],
    [(374, 25), (373, 29), (375, 33), (372, 38), (373, 43), (369, 48), (370, 57)],
    [(381, 22), (384, 27), (388, 30), (389, 35), (393, 39)],
]
# The smoke trails to the left, downwind, the same way the clouds drift.
PLUMES = [[(131, 11, 4), (127, 4, 5), (120, -3, 7), (109, -8, 9)], [(376, 19, 3), (372, 13, 4), (365, 6, 6)]]
ROCK = dict(pk_far="v_far", pk_far_sh="v_far_sh", pk_hi="vk_hi", pk_lit="vk_lit", pk_base="vk_base",
            pk_sh="vk_sh", pk_dk="vk_dk")


def peaks() -> Canvas:
    c = cv(H, WIDE)
    xs, ys = grid(WIDE)
    for plume in PLUMES:  # smoke behind the rim, lit orange where it leaves the crater
        for cx, cy, r in plume:
            lobe(c, cx, cy, r, SMOKE, under=False)
        cx, cy, r = plume[0]
        c.paint(c.mask("s_base", "s_sh") & (ys >= cy + r - 2) & (np.abs(xs - cx) <= r), "l3")
    # same spur-and-valley mountain drawing as the lake range, with bare rock instead of snow
    range_layer(ridgeline=RIDGE, far_range=FAR, snowline=0, canvas=c, names=ROCK)

    prof = periodic_profile(RIDGE, WIDE)
    for x0, x1 in CRATERS:                                        # molten rim
        for x in range(x0, x1 + 1):
            c.put(x, prof[x], "l0")
            c.put(x, prof[x] + 1, "l1")
            c.put(x, prof[x] + 2, "l3")
    for pts in STREAMS:
        top = pts[0][1]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            for y in range(y0, y1 + 1):
                x = round(x0 + (x1 - x0) * (y - y0) / max(1, y1 - y0))
                c.put(x, y, "l0" if y < top + 10 else "l1")
                c.put(x + 1, y, "l2" if y < top + 22 else "l3")
                if y > top + 12 and (x + y) % 3:
                    c.put(x - 1, y, "l3")
    return c


# ------------------------------------------------------------------------------- mesas
MESAS = [(0, 26, 52), (26, 56, 45), (56, 92, 53), (92, 104, 48), (104, 150, 54), (150, 196, 47), (196, 240, 52)]


def mesa() -> Canvas:
    c = cv()
    rng = random.Random(9)
    for x0, x1, top in MESAS:
        for x in range(x0, x1):
            t = top + (1 if x in (x0, x1 - 1) else 0)             # one-pixel bevel on each corner
            col = "m_lit" if x - x0 < 2 else "m_dk" if x1 - x <= 3 else "m_base"
            for y in range(t, LAVA_Y):
                role = col
                if y == t:
                    role = "m_hi"
                elif col != "m_dk" and (y - top) % 4 == 2:
                    role = "m_band"                               # strata
                c.put(x, y, role)
        for _ in range((x1 - x0) // 9):                           # short cracks down from the rim
            x = rng.randint(x0 + 3, x1 - 5)
            for y in range(top + 1, min(LAVA_Y, top + rng.randint(3, 6))):
                c.put(x, y, "m_dk")
    c.paint((c.a != 0) & (grid()[1] == LAVA_Y - 1), "m_dk")
    return c


# -------------------------------------------------------------------------------- lava
BANDS = ["l1", "l2", "l3", "l4"]
EDGES = [LAVA_Y, 64, 77, 95]
LADDER = ["l0"] + BANDS + ["crust"]        # hot to cool
PLATES = [(40, 70, 9, 2), (112, 66, 7, 1), (116, 88, 12, 2), (236, 73, 8, 2), (262, 67, 6, 1), (300, 90, 14, 3),
          (352, 78, 10, 2), (420, 70, 8, 2), (452, 96, 15, 3), (84, 99, 14, 3), (20, 86, 10, 2), (388, 100, 12, 3),
          (196, 100, 11, 2), (6, 62, 5, 1), (330, 63, 6, 1)]


def _plates():
    """Cooled crust plates: (mask, top rim, bottom rim, hot ring) over one frame."""
    xs, ys = grid(WIDE)
    jit = tile_noise(WIDE, 64, 8, 21)
    body = np.zeros((H, WIDE), bool)
    for cx, cy, hw, hh in PLATES:
        for dx in (-WIDE, 0, WIDE):
            e = ((xs - cx - dx) / hw) ** 2 + ((ys - cy) / (hh + 0.5)) ** 2
            body |= e + (jit[(ys - LAVA_Y) % 64, xs] - 0.5) * 0.7 <= 1.0
    up, down = np.roll(body, 1, 0), np.roll(body, -1, 0)
    ring = (up | down | np.roll(body, 1, 1) | np.roll(body, -1, 1)) & ~body
    return body, body & ~up, body & ~down, ring


def _heat():
    """Tone index 0..4 (hot to cool) per lava pixel: slow convection cells with glowing seams.

    Nothing travels. Plates of cooler lava sit between brighter seams, hotter toward the horizon haze.
    """
    xs, ys = grid(WIDE)
    row = np.clip(ys - LAVA_Y, 0, 63)
    stretch = (row * 1.6).astype(int) % 64                       # cells flatten with distance
    a = tile_noise(WIDE, 64, 16, 51)[stretch, xs]
    b = tile_noise(WIDE, 64, 8, 52)[(row * 2) % 64, xs]
    n = 0.7 * a + 0.3 * b
    depth = np.clip((ys - LAVA_Y) / 52.0, 0, 1)
    seam = np.abs(n - 0.5)                                         # near 0 on the lines between cells
    tone = np.full((H, WIDE), 2, np.int32)
    tone[n > 0.60] = 3
    tone[n > 0.74] = 4
    tone[seam < 0.045] = 1
    tone[seam < 0.016] = 0
    tone = np.clip(tone + (depth > 0.55).astype(int) - (depth < 0.12).astype(int), 0, 4)
    return tone, seam, n


# (x, y, size, phase): size 1 = small pop, 2 = medium, 3 = big blister. A few hug the rock slab
# the creature stands on (centre 176,80) and the near bank, where gas escapes along the edge.
BUBBLES = [(64, 80, 2, 0), (232, 92, 3, 5), (140, 100, 3, 9), (30, 70, 1, 3), (96, 72, 2, 11), (118, 90, 2, 7),
           (126, 80, 2, 13), (152, 95, 1, 2), (196, 96, 2, 6), (226, 80, 2, 10), (212, 66, 1, 14), (164, 64, 1, 8),
           (20, 96, 3, 12), (76, 104, 2, 4), (104, 62, 1, 1), (46, 62, 1, 15),
           (286, 76, 2, 3), (412, 86, 3, 11), (466, 74, 2, 7), (330, 98, 3, 1), (368, 68, 1, 13), (448, 102, 2, 5),
           (306, 64, 1, 9), (392, 104, 2, 15)]
EMBERS = [(40, 60, 0), (88, 59, 5), (150, 60, 10), (206, 59, 2), (232, 60, 13), (120, 59, 7),
          (270, 60, 4), (330, 59, 12), (396, 60, 8), (452, 59, 1)]


def _bubble(c: Canvas, x, y, size, st):
    """One bubble's life over the 16-frame loop: swell into a dome, burst, spatter, and a ring that fades."""
    r = size
    if st == 0:
        c.put(x, y, "lw")
    elif st == 1:
        c.hline(x - 1, x + 1, y, "l0")
        c.put(x, y - 1, "lw")
    elif st in (2, 3):                                             # full dome with a lit crown and a dark foot
        grow = 0 if st == 2 else 1
        w = r + grow
        for j in range(r + 1):
            half = max(0, w - j)
            c.hline(x - half, x + half, y - j, "l0")
        c.put(x - max(0, w - 1), y - 1, "lw")
        c.put(x, y - r, "lw")
        c.hline(x - w, x + w, y + 1, "l4")
    elif st == 4:                                                  # the skin splits
        for dx, dy in ((-r - 1, -1), (r + 1, -1), (0, -r - 1), (-r, -r), (r, -r)):
            c.put(x + dx, y + dy, "lw")
        c.hline(x - r, x + r, y, "l0")
    elif st == 5:                                                  # droplets fly out and up
        for dx, dy in ((-r - 2, -2), (r + 2, -2), (-1, -r - 3), (r + 1, -r - 2), (-r - 1, -r - 1)):
            c.put(x + dx, y + dy, "l0")
        c.hline(x - r, x + r, y, "l1")
    elif st == 6:                                                  # they fall back; a ring opens where it burst
        for dx, dy in ((-r - 3, 0), (r + 3, 0), (r + 2, -r)):
            c.put(x + dx, y + dy, "l1")
        c.hline(x - r - 1, x - r, y, "l0")
        c.hline(x + r, x + r + 1, y, "l0")
    elif st == 7:
        c.hline(x - r - 2, x - r - 1, y + 1, "l1")
        c.hline(x + r + 1, x + r + 2, y + 1, "l1")


def lava() -> Canvas:
    c = cv(H * FRAMES, WIDE)
    xs, ys = grid(WIDE)
    tone, seam, n = _heat()
    body, top, bottom, ring = _plates()
    ring_y, ring_x = np.nonzero(ring)
    lava_px = ys >= LAVA_Y
    ids = np.array([ROLES[r] for r in ("l0", "l1", "l2", "l3", "l4")], np.uint8)
    phase = (n * 16).astype(int)                                   # every seam pulses on its own beat

    for f in range(FRAMES):
        oy = f * H
        fr = c.a[oy:oy + H]
        t = tone.copy()
        glow = ((f + phase) % FRAMES) < 5                          # the seams brighten and dim in place
        t[(seam < 0.045) & ~glow & (t <= 1)] += 1
        t[(seam >= 0.045) & (seam < 0.07) & glow & (t == 2)] = 1
        fr[lava_px] = ids[np.clip(t, 0, 4)][lava_px]
        fr[body] = ROLES["crust"]
        fr[top] = ROLES["crust_hi"]
        fr[bottom] = ROLES["crust_dk"]
        hot = (ring_x + ring_y * 3 + f // 2) % 4 != 0              # the molten rim round each plate shimmers
        fr[ring_y[hot], ring_x[hot]] = ROLES["l0"]
        view = Canvas(WIDE, H, ROLES)
        view.a = fr
        for x, y, size, ph in BUBBLES:
            if not body[y, x]:
                _bubble(view, x, y, size, (f + ph) % FRAMES)
        for x, y, ph in EMBERS:                                    # sparks rise and drift left on the wind
            st = (f + ph) % FRAMES
            if st < 12:
                view.put(x - st // 2, y - st * 2, "lw" if st < 3 else "l0" if st < 7 else "l2" if st < 10 else "l3")
    return c


# ------------------------------------------------------------------------------- shore
BANK = [(0, 104), (30, 101), (62, 103), (86, 108), (120, 110), (160, 109), (200, 111), (240, 108),
        (270, 104), (300, 106), (340, 110), (400, 111), (440, 108)]
COLUMNS = [(0, 7, 90), (7, 6, 84), (13, 7, 88), (20, 6, 95), (26, 7, 92), (33, 6, 99), (39, 6, 103),
           (206, 6, 105), (212, 7, 99), (219, 6, 95), (225, 7, 90), (232, 8, 94),
           (252, 6, 101), (258, 7, 96), (265, 6, 99), (271, 7, 104),
           (436, 6, 103), (442, 7, 97), (449, 6, 92), (455, 7, 95), (462, 6, 90), (468, 6, 94), (474, 6, 98)]
CRACKS = [[(150, 125), (170, 131), (182, 140), (200, 146)], [(300, 119), (320, 127), (350, 131)],
          [(90, 136), (110, 143), (120, 153)], [(404, 132), (426, 138), (440, 150)], [(52, 120), (70, 124)]]
ANVIL = ["..HHHHHHHHHHHHH.",
         "HLLLLLLLLLLLLLD.",
         ".DLLLLLLLLLLLDD.",
         "...DDLLLLLDDD...",
         ".....LLLLD......",
         ".....LLLLD......",
         "....LLLLLLD.....",
         "...HLLLLLLLD....",
         "..LLLLLLLLLLD...",
         "..DDDDDDDDDDD..."]


def shore() -> Canvas:
    c = cv(H, WIDE)
    xs, ys = grid(WIDE)
    prof = periodic_profile(BANK, WIDE)
    d = ys - prof[xs]
    n = tile_noise(WIDE, 64, 16, 11)[(ys - 96) % 64, xs]
    ground = d >= 0
    c.paint(ground, "b_base")
    c.paint(ground & (n > 0.6), "b_lit")
    c.paint(ground & (n < 0.36), "b_sh")
    c.paint(ground & (ys >= 150) & ((n < 0.5) | checker(WIDE)), "b_sh")
    c.paint(ground & (ys >= 156), "b_dk")
    c.paint(ground & (d == 1), "b_hi")
    c.paint(ground & (d == 2) & checker(WIDE), "b_hi")
    c.paint(ground & (d == 0), "b_glow")                          # lip lit by the lava
    for pts in CRACKS:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            for x in range(x0, x1 + 1):
                y = round(y0 + (y1 - y0) * (x - x0) / max(1, x1 - x0))
                c.put(x, y, "l0" if x % 5 == 0 else "l3")
                c.put(x, y + 1, "b_dk")
    for x0, w, top in COLUMNS:                                    # basalt columns
        for x in range(x0, x0 + w):
            i = x - x0
            face = "b_dk" if i == 0 else "b_lit" if i <= w // 2 else "b_base" if i < w - 1 else "b_sh"
            for y in range(top, H):
                role = face
                if y == top:
                    role = "b_glow" if i else "b_dk"
                elif y == top + 1 and i:
                    role = "b_hi"
                elif i and (y + x0 * 3) % 9 == 0:
                    role = "b_sh"                                 # joints
                elif y >= 150:
                    role = "b_sh" if face != "b_dk" else "b_dk"
                c.put(x, y, role)
    key = {"H": "a_hi", "L": "a_lit", "D": "a_dk"}
    for j, row in enumerate(ANVIL):                               # the workbench: an anvil on the bank
        for i, ch in enumerate(row):
            if ch != ".":
                c.put(58 + i, 101 + j, key[ch])
    c.hline(59, 72, 111, "b_dk")
    return c


def platform() -> Canvas:
    pw, ph = 96, 24
    c = cv(ph, pw)
    cx, cy = 47.5, 11.5
    xs, ys = grid(pw, ph)

    def ell(a, b, ox=0.0, oy=0.0):
        return ((xs - cx - ox) / a) ** 2 + ((ys - cy - oy) / b) ** 2 <= 1.0

    out, ring_in, edge_in, top_in = ell(48, 12), ell(46, 10.4), ell(45, 9.4), ell(42.2, 7.6)
    theta = np.arctan2((ys - cy) * 48 / 12, xs - cx)
    seg = ((theta + math.pi) / (2 * math.pi) * 24).astype(int) % 3 != 0
    c.paint(out & ~ring_in & seg, "l0")                           # glowing seam, broken
    c.paint(ring_in & ~edge_in, "crust_dk")
    upper_left = ((xs - cx) / 48 + (ys - cy) / 12) < 0.0
    c.paint(edge_in & ~top_in, "b_sh")
    c.paint(edge_in & ~top_in & upper_left, "b_glow")
    c.paint(top_in, "b_lit")
    c.paint(top_in & ~ell(42.2, 7.6, -2.5, -1.4), "b_base")
    c.paint(top_in & ell(41, 6.8, 2.0, 1.4) & ~ell(41, 6.8, 0, 0) & upper_left, "b_hi")
    sh = ((xs - 47.5) / 15.5) ** 2 + ((ys - 12.0) / 3.2) ** 2 <= 1.0
    c.paint(sh & top_in, "b_base")
    for x, y, n in [(14, 10, 5), (66, 6, 6), (24, 15, 7), (70, 15, 5), (40, 5, 4)]:   # hairline cracks
        for k in range(n):
            if top_in[y + k // 3, x + k]:
                c.put(x + k, y + k // 3, "b_sh")
    return c


# -------------------------------------------------------------------------------- build
def build(variant: str) -> Variant:
    night = variant == "night"
    pal = PALETTES[variant]
    v = Variant()

    def add(file, canvas, drift=0, frames=1, fps=0):
        v.layers.append(Layer(f"{variant}/{file}", canvas.to_rgba(pal), drift, frames, fps))

    add("00-sky.png", sky(night))
    if night:
        add("05-stars.png", stars(), frames=4, fps=3)
    add("10-clouds.png", clouds(), drift=-2)
    add("20-peaks.png", peaks())
    add("25-mesa.png", mesa())
    add("30-lava.png", lava(), frames=FRAMES, fps=8)
    add("40-shore.png", shore())
    v.platform = platform().to_rgba(pal)
    v.platform_file = f"{variant}/platform.png"
    return v
