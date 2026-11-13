"""Water habitat: open ocean off a small beach, clear to the horizon (day + night).

The mountain range and tree ridge drawn here are still used by the fire and grass habitats.

Cel-lit, rounded, high-key landscape: key light from the top-left (sun by day, moon by night).
Everything is drawn into role-indexed canvases; day and night share all geometry.
"""
from __future__ import annotations

import math
import random

import numpy as np

from common import (H, W, Canvas, Layer, RoleSet, Variant, banded, checker, grid,
                    open_profile, periodic_profile, tile_noise)

NAME = "water"
WATER_Y = 58           # first lake row
MOON = (128, 26, 7)    # cx, cy, r (night)
WIDE = W * 2
PLATFORM = dict(file="platform.png", w=96, h=24, cx=176, cy=80)

ROLES = RoleSet([
    "sky0", "sky1", "sky2", "sky3", "sky4", "hz",
    "c_hi", "c_lit", "c_base", "c_sh",
    "pk_far", "pk_far_sh", "pk_hi", "pk_lit", "pk_base", "pk_sh", "pk_dk",
    "snow_hi", "snow", "snow_sh",
    "r_hi", "r_lit", "r_base", "r_dk",
    "w0", "w1", "w2", "w3", "w4", "wv", "hl", "foam", "spark2", "refR", "refP", "dock_shadow",
    "sand_hi", "sand", "sand_sh", "sand_wet", "pebble", "cshadow",
    "g_hi", "g_lit", "g_base", "g_sh", "bk",
    "t_hi", "t_lit", "t_base", "t_dk", "tr_lit", "tr_dk",
    "d_hi", "d_lit", "d_sh", "d_dk",
    "moon", "moon_sh", "glow", "mp", "mp2", "star1", "star2",
])

DAY = dict(
    sky0="#2878E8", sky1="#3C90F0", sky2="#58A8F8", sky3="#78C0F8", sky4="#98D4FC", hz="#C4EAFC",
    c_hi="#FFFFFF", c_lit="#EEF8FF", c_base="#C4DAF8", c_sh="#98B0E8",
    pk_far="#A8C0F0", pk_far_sh="#8CA4E0",
    pk_hi="#C0D0FF", pk_lit="#88A0E8", pk_base="#6C84D4", pk_sh="#5060B8", pk_dk="#3C46A0",
    snow_hi="#FFFFFF", snow="#DCE6F8", snow_sh="#98ACE8",
    r_hi="#60C494", r_lit="#3CA480", r_base="#2C8070", r_dk="#1C5C68",
    w0="#78D0F4", w1="#5CB8F0", w2="#44A0E4", w3="#3088D4", w4="#2470C0",
    wv="#A4E4FC", hl="#FFFFFF", foam="#FFFFFF", spark2="#C8F0FC", refR="#2C84B4", refP="#5C94D4", dock_shadow="#1C60A4",
    sand_hi="#FCEAB0", sand="#F0C878", sand_sh="#C89870", sand_wet="#A07868", pebble="#886C70",
    cshadow="#D8A470",
    g_hi="#B8E858", g_lit="#78C840", g_base="#48A038", g_sh="#2C7040", bk="#7C5848",
    t_hi="#98E060", t_lit="#58C048", t_base="#34983C", t_dk="#1C6040", tr_lit="#A87050", tr_dk="#6C4048",
    d_hi="#E8C890", d_lit="#C09868", d_sh="#8C6860", d_dk="#503C48",
    moon="#F8F4D0", moon_sh="#C8C8E0", glow="#3C58A0", mp="#F8F4D0", mp2="#C8F0FC",
    star1="#FFFFFF", star2="#C8F0FC",
)

NIGHT = dict(
    sky0="#04082C", sky1="#0C1448", sky2="#14225C", sky3="#1C3470", sky4="#284882", hz="#3A68A0",
    c_hi="#A8C8F8", c_lit="#6080C0", c_base="#40529C", c_sh="#28387C",
    pk_far="#2C4C8C", pk_far_sh="#24407C",
    pk_hi="#98B8F8", pk_lit="#4468B4", pk_base="#34549C", pk_sh="#24367C", pk_dk="#182460",
    snow_hi="#E0ECFF", snow="#A4BCF4", snow_sh="#5068B4",
    r_hi="#48A0A0", r_lit="#2C7478", r_base="#1C5064", r_dk="#102C48",
    w0="#3274AC", w1="#2A64A0", w2="#225494", w3="#1A4484", w4="#143474",
    wv="#4C9CC8", hl="#98E0EC", foam="#78C8DC", spark2="#78C8DC", refR="#0C2854", refP="#1C3C80", dock_shadow="#0C2048",
    sand_hi="#B0B8E8", sand="#7C84BC", sand_sh="#545CA0", sand_wet="#343C7C", pebble="#282C68",
    cshadow="#6068A4",
    g_hi="#60C0A8", g_lit="#3C8C6C", g_base="#2C6C5C", g_sh="#1C4848", bk="#302850",
    t_hi="#60D0B0", t_lit="#349474", t_base="#206C5C", t_dk="#124444", tr_lit="#705C98", tr_dk="#3C3064",
    d_hi="#A098C8", d_lit="#706898", d_sh="#4C4478", d_dk="#2C2450",
    moon="#F8F4D0", moon_sh="#C8C8E0", glow="#3C58A0", mp="#F8F4D0", mp2="#B0F0F8",
    star1="#F8F4D0", star2="#B0F0F8",
)
PALETTES = {"day": DAY, "night": NIGHT}


def cv(h=H, w=W) -> Canvas:
    return Canvas(w, h, ROLES)


# ----------------------------------------------------------------------- cel helpers
CUTS = (0.30, 0.62, 0.90)


def tone(s, roles):
    for role, cut in zip(roles, CUTS):
        if s < cut:
            return role
    return roles[3]


def lobe(c: Canvas, cx, cy, r, roles, under=True, clip_y=None, only=None):
    """Round lobe with 4 hard-edged cel tones, light from the top-left."""
    for y in range(cy - r, cy + r + 1):
        if clip_y is not None and y > clip_y:
            continue
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 > r * r + r:
                continue
            if only is not None and not only[y, x]:
                continue
            u, v = (x - cx) / r, (y - cy) / r
            s = (u + 1) / 2 * 0.5 + (v + 1) / 2 * 0.55
            role = roles[3] if (under and y >= cy + r - 1 and r >= 3) else tone(s, roles)
            c.put(x, y, role)


def dome(c: Canvas, cx, y_bot, hw, th, roles):
    """Rounded conifer tier: domed top, flat dark underside. Returns nothing."""
    for r in range(th):
        y = y_bot - th + 1 + r
        ratio = (r + 0.5) / th
        half = max(1, int(round(hw * math.sqrt(max(0.0, 1 - (1 - ratio) ** 2)))))
        for x in range(cx - half, cx + half + 1):
            u = (x - cx) / hw
            v = r / max(1, th - 1)
            s = (u + 1) / 2 * 0.55 + v * 0.6
            if r == th - 1:
                role = roles[3]
            elif r == th - 2:
                role = roles[2] if tone(s, roles) in (roles[0], roles[1]) else tone(s, roles)
            else:
                role = tone(s, roles)
            c.put(x, y, role)


TREE = ["t_hi", "t_lit", "t_base", "t_dk"]


def conifer(c: Canvas, cx, base, tiers, shadow_mask=None):
    """Stacked rounded tiers (top -> bottom as (half_width, height)); base = ground y."""
    hw_b = tiers[-1][0]
    if shadow_mask is not None:  # contact shadow, thrown to the right
        for dy in (-1, 0, 1):
            half = hw_b + 2 - abs(dy) * 2
            for x in range(cx - half + 3, cx + half + 4):
                y = base + dy
                if 0 <= y < c.h and 0 <= x < c.w and shadow_mask[y, x]:
                    c.put(x, y, "g_sh")
    trunk_top = base - 3
    for y in range(trunk_top, base + 1):
        c.put(cx - 1, y, "tr_lit")
        c.put(cx, y, "tr_lit")
        c.put(cx + 1, y, "tr_dk")
    y_bot = base - 2
    layout = []
    for hw, th in reversed(tiers):
        layout.append((hw, th, y_bot))
        y_bot = y_bot - th + 5
    for hw, th, yb in layout:  # bottom tier first, upper tiers overlap in front
        dome(c, cx, yb, hw, th, TREE)


def clump(c: Canvas, cx, base, lobes, shadow_mask=None):
    """Round leafy clump built from overlapping lobes [(dx, dy, r)]."""
    rmax = max(abs(dx) + r for dx, _, r in lobes)
    if shadow_mask is not None:
        for dy in (-1, 0, 1):
            for x in range(cx - rmax + 3, cx + rmax + 4 - abs(dy) * 2):
                y = base + dy
                if 0 <= y < c.h and 0 <= x < c.w and shadow_mask[y, x]:
                    c.put(x, y, "g_sh")
    for dx, dy, r in lobes:
        lobe(c, cx + dx, base - r + dy, r, TREE)


# ------------------------------------------------------------------------------ sky
def sky(night: bool) -> Canvas:
    sw = WIDE if night else W  # night is 480 wide so the moon is not repeated
    c = cv(H, sw)
    banded(c, [0, 11, 22, 33, 44, 52], ["sky0", "sky1", "sky2", "sky3", "sky4", "hz"])
    if night:
        mx, my, r = MOON
        xs, ys = grid(sw)
        d2 = (xs - mx) ** 2 + (ys - my) ** 2
        c.paint(d2 <= (r + 3) ** 2 + (r + 3), "glow")
        ring = (d2 > (r + 3) ** 2 + (r + 3)) & (d2 <= (r + 6) ** 2 + (r + 6)) & checker(sw, parity=0)
        c.paint(ring, "glow")
        m = d2 <= r * r + r
        c.paint(m, "moon")
        lit = (xs - (mx - 2)) ** 2 + (ys - (my - 2)) ** 2 <= r * r + r
        c.paint(m & ~lit, "moon_sh")
        for (dx, dy, n) in [(-2, 2, 2), (2, -3, 2), (3, 1, 1), (-3, -2, 1)]:
            for k in range(n):
                c.put(mx + dx + k, my + dy, "moon_sh")
            if n == 2:
                c.put(mx + dx, my + dy + 1, "moon_sh")
    return c


STARS_PLUS = [(30, 10), (92, 6), (178, 14), (208, 30), (60, 38)]
STARS_DOT = [(14, 22), (46, 8), (74, 24), (104, 14), (150, 8), (164, 30), (196, 6), (226, 16), (122, 46),
             (40, 44), (84, 6), (136, 38), (170, 20), (204, 40), (8, 8), (236, 30), (66, 14), (158, 44),
             (20, 32), (54, 20), (112, 8), (140, 22), (188, 22), (218, 40), (30, 4), (98, 28), (182, 36),
             (200, 14), (72, 42), (156, 16)]


def stars() -> Canvas:
    """Four frames stacked: plus-stars pulse, dots dim and flicker out of phase."""
    c = cv(H * 4)
    for f in range(4):
        oy = f * H
        for i, (x, y) in enumerate(STARS_PLUS):
            st = (f + i) % 4
            c.put(x, y + oy, "star1")
            if st == 0:
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    c.put(x + dx, y + dy + oy, "star2")
        for i, (x, y) in enumerate(STARS_DOT):
            st = (f + i) % 4
            if i % 3 == 0 and st == 0:
                continue  # blink off
            c.put(x, y + oy, "star2" if st == 2 else "star1")
    return c


# ---------------------------------------------------------------------------- clouds
SMALL = [(-7, 3), (0, 5), (8, 3)]
MEDIUM = [(-12, 4), (-4, 7), (5, 6), (13, 4)]
LARGE = [(-18, 5), (-9, 8), (1, 10), (12, 7), (21, 5)]
CLOUDS = [(60, 38, LARGE), (152, 15, SMALL), (236, 42, MEDIUM), (340, 30, LARGE), (420, 14, SMALL)]


def clouds() -> Canvas:
    c = cv(H, WIDE)
    roles = ["c_hi", "c_lit", "c_base", "c_sh"]
    for cx, base, lobes in CLOUDS:
        before = c.a.copy()
        for dx, r in lobes:
            lobe(c, cx + dx, base - r + 1, r, roles, under=False, clip_y=base)
        m = (c.a != before) | ((c.a != 0) & (before != 0) & (c.a != before))
        m = c.a != 0
        # flat shaded underside: bottom two rows of the cloud
        below2 = np.zeros_like(m)
        below2[:-2] = m[2:]
        local = np.zeros_like(m)
        local[base - 12:base + 1, cx - 30:cx + 31] = True
        c.paint(m & ~below2 & local, "c_sh")
    return c


HORIZON = [(34, [(-16, 2), (-9, 4), (-1, 5), (8, 3), (15, 2)]), (118, [(-7, 2), (0, 3), (7, 2)]),
           (212, [(-12, 3), (-4, 4), (5, 6), (14, 4), (22, 2)]), (300, [(-8, 2), (0, 4), (9, 3)]),
           (392, [(-18, 2), (-10, 3), (-2, 5), (7, 4), (15, 2)]), (458, [(-6, 2), (2, 3)])]


def horizon_clouds() -> Canvas:
    """Low cloud banks sitting on the sea horizon, so the skyline is not one bare line."""
    c = cv(H, WIDE)
    roles = ["c_hi", "c_lit", "c_base", "c_sh"]
    for cx, lobes in HORIZON:
        for dx, r in lobes:
            lobe(c, cx + dx, WATER_Y - r, r, roles, under=False, clip_y=WATER_Y - 1)
    m = c.a != 0
    c.paint(m & (grid(WIDE)[1] == WATER_Y - 1), "c_sh")           # flat base against the water
    return c


# ----------------------------------------------------------------------------- peaks
FAR_RANGE = [(0, 50), (20, 42), (46, 46), (70, 40), (96, 45), (120, 40), (160, 44), (200, 44),
             (220, 40), (240, 50), (260, 44), (290, 40), (320, 46), (350, 38), (380, 45), (410, 41),
             (440, 46), (480, 50)]
# Hand-placed ridgeline (x, top y), periodic over 480: uneven summits, shoulders, saddles and
# notches, like a real range. Nothing tall between x=140 and x=200, where the creature stands.
RIDGELINE = [
    (0, 44), (6, 40), (11, 41), (16, 33), (19, 34), (23, 30), (27, 33), (31, 31), (36, 38), (40, 36),
    (45, 27), (49, 24), (52, 20), (55, 22), (58, 21), (63, 27), (67, 26), (72, 33), (76, 31), (80, 24),
    (84, 19), (87, 14), (90, 13), (93, 16), (96, 15), (100, 21), (104, 20), (108, 27), (113, 29),
    (117, 35), (121, 33), (126, 39), (131, 38), (137, 44), (145, 46), (152, 43), (160, 47), (170, 45),
    (180, 48), (190, 44), (197, 46), (203, 39), (208, 35), (212, 30), (215, 31), (219, 24), (223, 17),
    (226, 13), (229, 15), (232, 14), (236, 20), (240, 24), (244, 23), (249, 30), (254, 27), (259, 24),
    (263, 26), (268, 33), (274, 37), (280, 35), (286, 41), (292, 38), (297, 34), (301, 36), (306, 42),
    (312, 40), (318, 33), (324, 27), (329, 22), (334, 18), (338, 16), (341, 18), (345, 17), (350, 24),
    (355, 28), (360, 27), (366, 34), (371, 31), (376, 35), (382, 40), (388, 37), (394, 33), (400, 30),
    (405, 26), (410, 28), (414, 25), (419, 31), (425, 36), (431, 34), (437, 40), (443, 43), (450, 41),
    (458, 45), (466, 42), (473, 45), (480, 44)]
SNOWLINE = 30
FOOT = 58          # first row below the range


def _jag(rng, n, lo, hi, run=(2, 4)):
    """Stepped offsets: hold a value for a few pixels, then move by at most one."""
    out, v = [], rng.randint(lo, hi)
    while len(out) < n:
        out += [v] * rng.randint(*run)
        v = min(hi, max(lo, v + rng.choice((-1, 0, 1))))
    return out[:n]


def peaks(ridgeline=None, far_range=None, snowline=SNOWLINE, canvas=None, names=None) -> Canvas:
    """The mountain range. Other habitats reuse it with their own ridgeline and role names
    (`names` maps this module's role names to theirs); snowline=0 leaves the rock bare."""
    ridgeline = ridgeline or RIDGELINE
    far_range = far_range or FAR_RANGE

    def R(name):
        return (names or {}).get(name, name)

    w = WIDE
    c = canvas if canvas is not None else cv(H, w)
    xs, ys = grid(w)
    # far range: two tones, quantised into chunky 3px blocks
    top = periodic_profile(far_range, w)
    top = (top // 2) * 2
    top = top[(np.arange(w) // 3) * 3 + 1]
    body = ys >= top[None, :]
    rising = (np.roll(top, -1) - np.roll(top, 1) <= 0)[None, :]
    c.paint(body & rising, R("pk_far"))
    c.paint(body & ~rising, R("pk_far_sh"))

    # main range. Work on three copies of the ridgeline so spur and valley lines can cross the seam.
    ext = np.tile(periodic_profile(ridgeline, w), 3)
    n = 3 * w
    summits = []
    for x in range(8, n - 8):
        if ext[x] <= 38 and ext[x] == ext[x - 7:x + 8].min() and ext[x - 1] > ext[x]:
            if not summits or x - summits[-1] >= 8:
                summits.append(x)
    valleys = [a + int(np.argmax(ext[a:b + 1])) for a, b in zip(summits, summits[1:])]

    def line(x0, seed, lo, hi):
        """A wandering line falling from (x0, ext[x0]): a slope plus a stepped wobble."""
        rng = random.Random(seed + x0 % w)
        k = rng.uniform(lo, hi)
        wob = _jag(rng, H, -1, 1, run=(2, 5))
        y0 = ext[x0]
        return [x0 if y < y0 else x0 + int((y - y0) * k) + wob[y - y0] for y in range(H)]

    spurs = [line(sx, 1000, 0.10, 0.55) for sx in summits]
    vals = [line(vx, 2000, -0.15, 0.25) for vx in valleys]

    M = np.zeros((H, w), bool)
    lit = np.zeros((H, w), bool)
    crest = np.zeros((H, w), bool)    # the sunlit edge of each spur
    for y in range(FOOT):
        bounds = []
        for j in range(len(vals)):
            v = vals[j][y]
            if bounds:
                v = max(v, bounds[-1] + 2)
            bounds.append(v)
        for x in range(w):
            X = x + w
            if y < ext[X]:
                continue
            M[y, x] = True
            i = 0
            while i < len(bounds) and X > bounds[i]:
                i += 1
            i = min(i, len(summits) - 1)
            sp = spurs[i][y]
            lo = bounds[i - 1] + 1 if i > 0 else -10 ** 6
            hi = bounds[i] - 1 if i < len(bounds) else 10 ** 6
            sp = min(max(sp, lo), hi)
            lit[y, x] = X <= sp
            crest[y, x] = X == sp and y - ext[summits[i]] < 14
    tp = ext[w:2 * w]
    c.paint(M & lit, R("pk_lit"))
    c.paint(M & ~lit, R("pk_sh"))
    left_edge = np.zeros_like(M)
    left_edge[:, 1:] = ~M[:, :-1]
    top_edge = ys == tp[None, :]
    hi_mask = M & lit & (left_edge | top_edge | crest)
    c.paint(hi_mask, R("pk_hi"))

    # rock strata: short strokes that run with the slope, darker on the lit faces and darkest in shadow
    rng = random.Random(7)
    for _ in range(260):
        x, y = rng.randrange(w), rng.randint(16, 48)
        if not M[y, x] or y < tp[x] + 3:
            continue
        ln, steep = rng.randint(2, 5), rng.random() < 0.5
        on_lit = bool(lit[y, x])
        for t in range(ln):
            xx = (x - t if on_lit else x + t) % w
            yy = y + (t if steep else t // 2)
            if yy < FOOT and M[yy, xx] and lit[yy, xx] == on_lit and not hi_mask[yy, xx]:
                c.put(xx, yy, R("pk_base") if on_lit else R("pk_dk"))

    if snowline:
        # snow: everything above a ragged snowline, with streaks running down the gullies
        jag = _jag(random.Random(11), w, -2, 3, run=(2, 5))
        snow = np.zeros_like(M)
        for x in range(w):
            snow[:max(0, snowline + jag[x]), x] = True
        for _ in range(34):
            x = rng.randrange(w)
            if tp[x] >= snowline:
                continue
            y0, extra = snowline + jag[x], rng.randint(2, 6)
            for xx in (x, x + 1)[:rng.randint(1, 2)]:
                snow[y0:y0 + extra, xx % w] = True
        snow &= M
        below = np.zeros_like(M)
        below[:-2] = ~snow[2:]            # the bottom two rows of the snow read a tone darker
        c.paint(snow & lit, R("snow_hi"))
        c.paint(snow & lit & below & ~top_edge, R("snow"))
        c.paint(snow & ~lit, R("snow_sh"))
        for _ in range(40):               # bare rock showing through
            x, y = rng.randrange(w), rng.randint(14, snowline)
            if snow[y, x] and y >= tp[x] + 3:
                for xx in (x, x + 1)[:rng.randint(1, 2)]:
                    if snow[y, xx % w]:
                        c.put(xx % w, y, R("pk_lit") if lit[y, xx % w] else R("pk_dk"))

    # mist at the foot of the range: flat band with a one-row dither
    m = c.a != 0
    row = ys == 49
    c.paint(m & (ys >= 50), R("pk_far"))
    c.paint(m & row & checker(w, parity=0), R("pk_far"))
    return c


# ----------------------------------------------------------------------------- ridge
RIDGE = ["r_hi", "r_lit", "r_base", "r_dk"]


def ridge() -> tuple[Canvas, np.ndarray]:
    """Row of rounded treetop lobes (not a sawtooth)."""
    c = cv()
    xs, ys = grid()
    rng = random.Random(7)
    c.paint(ys >= 54, "r_base")
    x = 8
    lobes = []
    while x < 232:
        calm = 138 <= x <= 218
        r = rng.randint(3, 4) if calm else rng.randint(4, 6)
        lobes.append((x, 53 - r + 1 + rng.randint(0, 1), r))
        x += rng.randint(r + 1, r + 3)
    for cx, cy, r in lobes:
        lobe(c, cx, cy, r, RIDGE, under=False)
    c.paint(ys >= 56, "r_dk")
    c.paint((ys == 55) & checker(parity=0) & (c.a != 0), "r_dk")
    return c, c.a != 0


# ----------------------------------------------------------------------------- water
SPARKS = [(30, 64), (96, 68), (122, 99), (58, 100), (250, 66), (318, 76), (398, 88), (296, 98),
          (440, 67), (204, 101), (370, 62)]
BANDS = ["w0", "w1", "w2", "w3", "w4"]
BAND_EDGES = [WATER_Y, 66, 76, 88, 100]
LADDER = ["wv"] + BANDS + ["dock_shadow"]     # light to dark; a band's neighbours are one step either way
WATER_FRAMES = 16
TRI = (0, 1, 2, 1, 0, -1, -2, -1)
# wavelengths that divide the 480px layer, so every swell tiles; each travels exactly one
# wavelength per loop, so long swells near the shore move faster than the short far ones
LAMBDAS = [8, 10, 12, 15, 16, 20, 24, 30, 32, 40, 48, 60]


def _moon_path():
    rng = random.Random(23)
    cx = MOON[0]
    out = []
    for y in range(59, 108, 2):
        hw = 3 + int((y - WATER_Y) * 0.34)
        ln = 2 + (y - WATER_Y) // 7 + rng.randint(0, 2)
        for _ in range(2):
            x = cx + rng.randint(-hw, hw) - ln // 2
            near = abs(x + ln // 2 - cx) < hw * 0.55
            out.append((x, y, ln, "mp" if near else "mp2"))
    return out


class Swell:
    """One travelling wave line: two sine swells added together, both moving the same way.

    `height(f)` is the wave shape per column at frame f, in -1..1. The second swell has a
    different length and speed, so the line keeps changing shape as it slides along.
    """

    def __init__(self, rng, la, lb, w=WIDE):
        self.x = np.arange(w)
        self.la, self.lb = la, lb
        self.pa, self.pb = rng.random() * math.tau, rng.random() * math.tau
        self.kb = rng.choice((1, 2))

    def height(self, f):
        t = f / WATER_FRAMES
        return (0.65 * np.sin(math.tau * (self.x / self.la - t) + self.pa)
                + 0.35 * np.sin(math.tau * (self.x / self.lb - self.kb * t) + self.pb))


def _swell_rows():
    """Wave lines from the far shore to the beach: short, low and close together far away."""
    rng = random.Random(41)
    rows = []
    y, i = 60, 0
    tiers = ("light", "deep", "tone", "light", "tone", "deep")
    while y <= 106:
        depth = (y - WATER_Y) / 49
        k = min(int(depth * 6) + rng.randint(0, 2), 8)
        sw = Swell(rng, LAMBDAS[k], LAMBDAS[max(0, min(len(LAMBDAS) - 1, k + rng.choice((-2, -1, 1, 2))))])
        tier = tiers[i % len(tiers)]
        if depth < 0.16 and tier == "deep":
            tier = "tone"
        rows.append(dict(y=y, sw=sw, amp=0.7 + 1.7 * depth, tier=tier, bright=rng.random() < 0.6,
                         cover={"light": 0.46, "tone": 0.5, "deep": 0.4}[tier] + 0.08 * (1 - depth),
                         noise=tile_noise(WIDE, 1, (16, 24, 40)[min(2, int(depth * 3))], 90 + i)[0],
                         sag=np.rint(2 * tile_noise(WIDE, 1, 40, 130 + i)[0] - 1).astype(int),
                         ex=rng.random() * math.tau, el=LAMBDAS[min(len(LAMBDAS) - 1, k + 3)],
                         minrun=2 if depth < 0.2 else 3))
        y += 2 + int(round(depth * 1.6))
        i += 1
    return rows


def _runs(on, minrun):
    """Drop lit runs shorter than `minrun` (periodic)."""
    w = len(on)
    out = on.copy()
    start = next((i for i in range(w) if not on[i]), None)
    if start is None:
        return out
    i = 0
    while i < w:
        x = (start + i) % w
        if on[x]:
            j = i
            while j < w and on[(start + j) % w]:
                j += 1
            if j - i < minrun:
                out[(start + np.arange(i, j)) % w] = False
            i = j
        else:
            i += 1
    return out


def water(ridge_mask: np.ndarray, peak_mask: np.ndarray) -> Canvas:
    w = WIDE
    frames = WATER_FRAMES
    out = cv(H * frames, w)
    xs, ys = grid(w)
    cols = np.arange(w)
    calm = (cols % 240 >= 118) & (cols % 240 <= 232)       # behind the creature: no white glints
    rm = np.tile(ridge_mask, (1, 2))
    ladder = np.array([ROLES[r] for r in LADDER])
    refR, refP, wv, hl = ROLES["refR"], ROLES["refP"], ROLES["wv"], ROLES["hl"]
    rng = random.Random(7)
    # the lines between water tones are travelling swells too, taller toward the shore
    edge_sw = [None] + [(Swell(rng, la, lb), amp) for la, lb, amp in
                        [(12, 20, 1.0), (16, 30, 1.3), (24, 40, 1.7), (32, 48, 2.1)]]
    gap_r, gap_p = Swell(rng, 12, 20), Swell(rng, 16, 24)   # reflections ripple instead of sitting in level stripes
    rows = _swell_rows()
    # one envelope threshold per row, taken over the whole loop, so coverage stays steady frame to frame
    for r in rows:
        env = np.stack([r["noise"] + 0.22 * np.sin(math.tau * (cols / r["el"] - f / frames) + r["ex"])
                        + 0.18 * r["sw"].height(f) for f in range(frames)])
        r["env"], r["cut"] = env, np.quantile(env, 1 - r["cover"])
    for f in range(frames):
        fr = cv(H, w)
        band = np.zeros((H, w), int)
        for b in range(1, len(BANDS)):
            sw, amp = edge_sw[b]
            band += ys >= (BAND_EDGES[b] - np.rint(amp * sw.height(f)).astype(int))[None, :]
        water_px = ys >= WATER_Y
        fr.a[water_px] = ladder[band + 1][water_px]
        # reflections: ridge (dark teal), then compressed peaks (violet)
        gr = np.rint(1.3 * gap_r.height(f)).astype(int)
        gp = np.rint(1.3 * gap_p.height(f)).astype(int)
        for y in range(WATER_Y, WATER_Y + 12):
            sel = rm[WATER_Y - 1 - (y - WATER_Y)] & ((y + gr) % 4 != 3)
            if y >= WATER_Y + 7:
                sel &= (y + gr) % 2 == 0
            fr.a[y, sel] = refR
        for y in range(66, 82):
            src = 46 - 2 * (y - 66)
            sel = peak_mask[src] & ((y + gp) % 3 != 2) & (fr.a[y] != refR)
            fr.a[y, sel] = refP
        # wave lines
        for r in rows:
            h = r["sw"].height(f)
            yy = r["y"] + r["sag"] - np.rint(r["amp"] * h).astype(int)
            on = _runs(r["env"][f] > r["cut"], r["minrun"])
            x = cols[on]
            y = yy[on]
            bi = band[y, x] + 1                       # ladder index of the water tone at each pixel
            if r["tier"] == "deep":                   # trough: one tone darker; over a reflection it shows as plain water
                plain = fr.a[y, x] == ladder[bi]
                fr.a[y, x] = np.where(plain, ladder[np.minimum(bi + 1, len(ladder) - 1)], ladder[bi])
            elif r["tier"] == "tone":                 # low swell: one tone lighter
                fr.a[y, x] = ladder[bi - 1]
            else:                                     # crest: pale line, white on the tops, shaded face beneath
                top = (h[on] > 0.45) & r["bright"] & ~calm[on]
                fr.a[y, x] = np.where(top, hl, wv)
                if r["amp"] >= 1.0:
                    face = h[on] > -0.1
                    fx, fy = x[face], y[face] + 1
                    under = fr.a[fy, fx]
                    fr.a[fy, fx] = np.where(np.isin(under, (wv, hl)), under,
                                            ladder[np.minimum(band[fy, fx] + 2, len(ladder) - 1)])
        for i, (sx, sy) in enumerate(SPARKS):
            st = (f // 2 + i) % 4
            if st == 1:
                fr.put(sx, sy, "hl")
            elif st == 2:
                fr.put(sx, sy, "hl")
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    fr.put(sx + dx, sy + dy, "spark2")
            elif st == 3:
                fr.put(sx, sy, "spark2")
        out.a[f * H:(f + 1) * H] = fr.a
    return out


def moonpath() -> Canvas:
    """Night only: glitter under the moon, 480 wide so it is not repeated. Longer glints are shallow arcs."""
    c = cv(H * 8, WIDE)
    for f in range(8):
        for x, y, ln, role in _moon_path():
            s = TRI[f]
            if ln >= 4:
                c.hline(x + s + 1, x + s + ln - 2, y + f * H, role)
                c.put(x + s, y + 1 + f * H, role)
                c.put(x + s + ln - 1, y + 1 + f * H, role)
            else:
                c.hline(x + s, x + s + ln - 1, y + f * H, role)
    return c


# ----------------------------------------------------------------------------- shore
def shore() -> Canvas:
    w = WIDE
    c = cv(H, w)
    xs, ys = grid(w)
    s_top = periodic_profile([(0, 106), (30, 105), (70, 107), (110, 106), (150, 105), (190, 107), (240, 106),
                              (270, 105), (310, 107), (350, 106), (390, 105), (430, 107), (480, 106)], w)
    land = open_profile([(4, 104), (10, 96), (18, 91), (40, 87), (60, 88), (68, 90), (76, 95),
                         (84, 99), (92, 103), (98, 106)], w)
    # dock cast shadow on the water: deck strip, thrown right/down; posts add short diagonal strokes
    for x in range(70, 114):
        c.put(x, 95, "dock_shadow")
        if x % 2 == 0:
            c.put(x, 96, "dock_shadow")
    for px in (70, 82, 94, 106):
        for k in range(6):
            c.put(px + 2 + k, 100 + k // 2 + 1, "dock_shadow")
    # knoll: grass with lit top and shadowed bank; right slope faces away from the light
    m = (ys >= land[None, :]) & (ys < s_top[None, :])
    for x in range(4, 100):
        if land[x] >= 10_000:
            continue
        lit_face = (min(land[x + 3], 200) - land[x - 3] <= 0) if land[x + 3] < 10_000 else False
        for y in range(int(land[x]), int(s_top[x])):
            d = y - land[x]
            b = s_top[x] - 1 - y
            if b == 0:
                role = "bk"
            elif b <= 3:
                role = "g_sh"
            elif b == 4:
                role = "g_sh" if (x + y) % 2 == 0 else "g_base"
            elif lit_face:
                role = "g_hi" if d < 2 else "g_lit" if d < 7 else "g_base"
            else:
                role = "g_lit" if d < 1 else "g_base" if d < 5 else "g_sh"
            c.put(x, y, role)
    rng = random.Random(5)
    for _ in range(9):  # grass tufts on the lit face
        x = rng.randint(12, 58)
        y = int(land[x]) + rng.randint(3, 6)
        if y < s_top[x] - 6:
            for dx, dy in ((0, 0), (2, 0), (1, 1)):
                c.put(x + dx, y + dy, "g_hi")
    # beach strip: sand, wet line, broken white foam line
    for x in range(w):
        t = int(s_top[x])
        c.a[t:, x] = ROLES["sand"]
        c.put(x, t, "sand_wet")
        c.put(x, t + 1, "sand_wet" if x % 2 == 0 else "sand")
        c.a[t + 2:t + 4, x] = ROLES["sand"]
        c.a[t + 4:t + 8, x] = ROLES["sand"]
        c.a[t + 8:, x] = ROLES["sand_sh"]
    for x in range(w):
        t = int(s_top[x])
        if (x // 3 + (x // 24)) % 3 != 0:
            c.put(x, t - 1, "foam")
        if (x % 11) in (2, 3, 4):
            c.put(x, t - 2, "foam")
    for y in (110, 113):
        for x in list(range(8, 232, 17)) + list(range(250, 470, 19)):
            xx = x + (y * 3) % 7
            c.hline(xx, xx + 3, y, "sand_hi")
    # foam where the water meets the knoll's sloping ends
    dil = m | np.roll(m, 1, axis=1) | np.roll(m, -1, axis=1) | np.roll(m, -1, axis=0)
    foam = dil & ~m & (ys >= 93) & (ys < s_top[None, :] - 1) & (((xs <= 20) | ((xs >= 70) & (xs <= 100))))
    foam &= ((xs + ys) % 3 != 0)
    c.paint(foam, "foam")
    for x, y in [(20, 109), (44, 110), (52, 108), (86, 109), (112, 110), (150, 110), (206, 109)]:
        c.put(x, y, "pebble"); c.put(x + 1, y, "pebble"); c.put(x, y - 1, "sand_hi")
        if x < 100:
            c.put(x + 1, y + 1, "pebble")
    # quiet far half (x 240-479): two small cel-lit rocks, sparse reeds, one lone small pine
    for rx in (290, 424):
        t = int(s_top[rx])
        for (x0, x1, yy, role) in [(rx, rx + 3, t - 3, "sand_hi"), (rx - 1, rx + 4, t - 2, "sand"),
                                   (rx - 1, rx + 4, t - 1, "sand_sh"), (rx, rx + 4, t, "pebble")]:
            c.hline(x0, x1, yy, role)
    for rx, rh in [(262, 5), (265, 4), (268, 6), (338, 4), (341, 5), (401, 5), (404, 4), (407, 6), (456, 4), (459, 5)]:
        t = int(s_top[rx])
        for k in range(rh):
            c.put(rx + (k // 3), t - 3 - k, "g_hi" if k == rh - 1 else "g_lit" if k > 1 else "g_base")
    pcx = 366
    t = int(s_top[pcx])
    mound = np.zeros((H, w), bool)
    mound[t - 3:t + 1, pcx - 5:pcx + 6] = True
    c.hline(pcx - 4, pcx + 4, t - 2, "g_lit")
    c.hline(pcx - 5, pcx + 5, t - 1, "g_base")
    c.hline(pcx - 5, pcx + 5, t, "g_sh")
    conifer(c, pcx, t - 2, [(3, 7), (5, 8)])
    # knoll trees, back to front: stacked rounded conifers and two leafy clumps
    conifer(c, 40, int(land[40]) + 3, [(4, 9), (6, 10), (8, 10), (10, 10)], m)
    conifer(c, 55, int(land[55]) + 3, [(3, 8), (5, 9), (7, 9)], m)
    conifer(c, 24, int(land[24]) + 3, [(3, 8), (5, 9), (7, 9)], m)
    conifer(c, 12, int(land[12]) + 3, [(3, 8), (5, 8)], m)
    clump(c, 64, int(land[64]) + 2, [(-3, 0, 4), (2, -1, 5), (5, 1, 3)], m)
    clump(c, 8, int(land[8]) + 3, [(-1, 0, 3), (3, 1, 3)], m)
    # weathered dock: deck 90-93, posts, tall mooring post
    for px in (70, 82, 94, 106):
        for y in range(94, 102):
            c.put(px, y, "d_lit")
            c.put(px + 1, y, "d_dk")
        c.put(px, 94, "d_sh")
        c.put(px - 1, 102, "foam"); c.put(px + 2, 102, "foam"); c.put(px, 102, "foam"); c.put(px + 1, 102, "foam")
    c.rect(106, 85, 2, 9, "d_dk")
    c.put(106, 85, "d_hi"); c.put(106, 86, "d_lit"); c.put(107, 85, "d_lit")
    for y in range(87, 94):
        c.put(106, y, "d_lit")
    x = 66
    plank = 0
    lens = [7, 9, 6, 8, 7, 9]
    while x <= 108:
        ln = lens[plank % len(lens)]
        x1 = min(108, x + ln - 1)
        role = "d_hi" if plank % 2 == 0 else "d_lit"
        for yy in (90, 91):
            c.hline(x, x1, yy, role)
        if plank == 3:  # a missing board
            for yy in (90, 91):
                c.hline(x + 2, x1 - 3, yy, "dock_shadow")
        if x1 + 1 <= 108:
            c.put(x1 + 1, 90, "d_sh"); c.put(x1 + 1, 91, "d_sh")
        x = x1 + 2
        plank += 1
    c.hline(66, 108, 92, "d_lit")
    c.hline(66, 108, 93, "d_sh")
    for x in (74, 86, 99):
        c.put(x, 92, "d_sh")
    return c


# --------------------------------------------------------------------------- platform
def platform() -> Canvas:
    pw, ph = 96, 24
    c = cv(ph, pw)
    cx, cy = 47.5, 11.5
    xs, ys = grid(pw, ph)

    def ell(a, b, ox=0.0, oy=0.0):
        return ((xs - cx - ox) / a) ** 2 + ((ys - cy - oy) / b) ** 2 <= 1.0

    out, ring_in, wet_in, rim_in = ell(48, 12), ell(46, 10.4), ell(45, 9.4), ell(42.2, 7.6)
    theta = np.arctan2((ys - cy) * 48 / 12, xs - cx)
    seg = ((theta + math.pi) / (2 * math.pi) * 24).astype(int) % 3 != 0
    c.paint(out & ~ring_in & seg, "foam")                 # foam ring, broken
    c.paint((wet_in & ~ring_in) | (ring_in & ~wet_in), "sand_wet")
    upper_left = ((xs - cx) / 48 + (ys - cy) / 12) < 0.0
    c.paint(wet_in & ~rim_in, "sand_sh")                # darker edge lower-right
    c.paint(wet_in & ~rim_in & upper_left, "sand_hi")   # lighter rim top-left
    c.paint(rim_in, "sand")
    c.paint(rim_in & ~ell(42.2, 7.6, -2.5, -1.4), "sand_sh")
    c.paint(rim_in & ell(41, 6.8, 2.0, 1.4) & ~ell(41, 6.8, 0, 0) & upper_left, "sand_hi")
    # soft contact shadow where the creature stands (about 30x6, flat)
    sh = ((xs - 47.5) / 15.5) ** 2 + ((ys - 12.0) / 3.2) ** 2 <= 1.0
    c.paint(sh & rim_in, "cshadow")
    # tufts and pebbles at the edge (only where they land on sand)
    for x, y in [(9, 11), (10, 10), (11, 11), (83, 13), (84, 12), (85, 13), (31, 6), (32, 5), (33, 6), (60, 17), (61, 18)]:
        if rim_in[y, x]:
            c.put(x, y, "g_lit")
    for x, y in [(10, 10), (84, 12), (32, 5)]:
        if rim_in[y, x]:
            c.put(x, y, "g_hi")
    for x, y in [(20, 16), (72, 7), (45, 18), (70, 16), (24, 7)]:
        if rim_in[y, x]:
            c.put(x, y, "pebble"); c.put(x + 1, y, "pebble"); c.put(x, y - 1, "sand_hi")
    return c


# -------------------------------------------------------------------------------- build
def build(variant: str) -> Variant:
    night = variant == "night"
    pal = PALETTES[variant]
    v = Variant()
    none = np.zeros((H, W), bool)          # open sea: no far shore or range to reflect

    def add(file, canvas, drift=0, frames=1, fps=0):
        v.layers.append(Layer(f"{variant}/{file}", canvas.to_rgba(pal), drift, frames, fps))

    add("00-sky.png", sky(night))
    if night:
        add("05-stars.png", stars(), frames=4, fps=3)
    add("10-clouds.png", clouds(), drift=-2)
    add("15-horizon.png", horizon_clouds())
    add("30-water.png", water(none, np.zeros((H, WIDE), bool)), frames=WATER_FRAMES, fps=8)
    if night:
        add("35-moonpath.png", moonpath(), frames=8, fps=8)
    add("40-shore.png", shore())
    v.platform = platform().to_rgba(pal)
    v.platform_file = f"{variant}/platform.png"
    return v
