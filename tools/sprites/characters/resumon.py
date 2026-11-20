"""Resumon: traced base (BOX-downscaled reference still) + hand-stamped details, cel-lit, animated by parts."""
import numpy as np
import base
from base import TEAL, CREAM, NAVY, GREY
from pixel import (Canvas, ell, rect, poly, pix, taper, crouch, lift, reoutline, flatten, apply_bands, cast, solid,
                   dilate, H, W)

SLUG = "resumon"
REF = "src/assets/mascots/resumon.png"  # repo-relative
HEIGHT = 54

C = dict(
    teal_hi=(168, 248, 232), teal_lt=(104, 224, 216), teal_bs=(64, 184, 208), teal_sh=(40, 128, 176), teal_d=(24, 64, 96),
    cream_hi=(248, 248, 232), cream_lt=(248, 240, 208), cream_bs=(224, 216, 200), cream_sh=(184, 184, 216),
    navy_hi=(96, 152, 216), navy_lt=(64, 112, 184), navy_bs=(40, 80, 152), navy_sh=(32, 56, 120), navy_d=(16, 32, 80),
    grey_hi=(216, 224, 240), grey_lt=(176, 184, 208), grey_bs=(136, 144, 176), grey_sh=(104, 112, 144), grey_d=(64, 72, 104),
    pink=(248, 160, 160), white=(248, 248, 248), green=(88, 200, 88),
)
RAMPS = {TEAL: ("teal_lt",) * 3, CREAM: ("cream_lt",) * 3, NAVY: ("navy_lt",) * 3, GREY: ("grey_lt",) * 3}
DARK = {TEAL: "teal_d", CREAM: "teal_d", NAVY: "navy_d", GREY: "grey_d"}
THR = {TEAL: (999, -1), CREAM: (999, -1), NAVY: (999, -1)}
_DARK_FAM = {"teal": "teal_d", "cream": "teal_d", "navy": "navy_d", "grey": "grey_d", "pink": "teal_d"}
T, TD = "teal", "teal_d"
CHECK = [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0), (5, -1), (6, -2)]
HEAD_ROWS = 32  # rows <= this belong to the head group
HOLD_S = (34, 39)  # near shoulder


def dark_of(k):
    return k if k.endswith("_d") else _DARK_FAM.get(k.rsplit("_", 1)[0])


def geo_of(px, fams=("teal", "cream", "navy", "grey")):
    m = np.zeros((H, W), bool)
    for y, x in zip(*np.where(px != None)):  # noqa: E711
        if px[y, x].split("_")[0] in fams and not px[y, x].endswith("_d"):
            m[y, x] = True
    return m


def opaque(px):
    return px != None  # noqa: E711


def _inpaint_dark(K, region):
    for _ in range(6):
        todo = [(y, x) for y, x in zip(*np.where(region)) if K[y, x] == TD]
        if not todo:
            break
        for y, x in todo:
            nb = [K[j, i] for j in range(y - 1, y + 2) for i in range(x - 1, x + 2)
                  if 0 <= j < H and 0 <= i < W and K[j, i] not in (None, TD)]
            if nb:
                K[y, x] = max(set(nb), key=nb.count)


def _build_base():
    K, _ = base.keymap(REF, HEIGHT, RAMPS, DARK, THR, grey_box=(12, 34, 24, 47))
    _inpaint_dark(K, rect(14, 18, 36, 29))
    for y, x in zip(*np.where(rect(29, 22, 36, 26))):
        if K[y, x] and K[y, x].startswith("cream"):
            K[y, x] = "teal_lt"
    K[rect(22, 5, 40, 11)] = None  # traced fin and drop: re-stamped fin only (no drop)
    K[rect(38, 19, 46, 31)] = None
    K[rect(8, 19, 12, 31)] = None
    K[rect(18, 32, 34, 36)] = None
    K[rect(10, 34, 37, 46)] = None  # collar, board, hand, traced arm: re-stamped
    K[rect(40, 30, 56, 52) & ~rect(40, 46, 43, 54)] = None  # fluke: redrawn per pose
    head = K.copy()
    head[HEAD_ROWS + 1:] = None
    head = reoutline(head, dark_of, rows=(0, 29))
    body = K.copy()
    body[:HEAD_ROWS + 1] = None
    # light the head: crown/brow top-left, core-shadow crescent right and under the jaw, rim light on the far edge
    apply_bands(head, geo_of(head), rim_light=True, soften=("cream",), th=3, sx=3, sy=3, bx=3, by=2)
    return head, body


HEAD, BODY = _build_base()
HEAD_SIL = opaque(HEAD)


def _torso(sw):
    c = Canvas()
    torso = poly([(19 - sw, 33), (33 + sw, 33), (34 + sw, 37), (35 + sw, 42), (36 + sw, 47), (36 + sw, 50),
                  (16 - sw, 50), (16 - sw, 47), (17 - sw, 42), (18 - sw, 37)])
    c.fill(dilate(torso), TD)
    c.fill(torso, "teal_lt")
    c.fill(ell(25, 48.5, 6.5 + sw * .5, 3.5 + sw * .5) & torso, "cream_lt")
    return c.px


def _lit_body(sw):
    c = Canvas()
    c.paste(_torso(sw))
    c.paste(BODY)
    geo = geo_of(c.px)
    apply_bands(c.px, geo, rim_light=True, soften=("cream",), th=2, sx=3, sy=2, bx=3, by=2)
    # belly: highlight patch on the lit side
    for y, x in zip(*np.where(geo)):
        if c.px[y, x] == "cream_lt" and x < 22 and y <= 50:
            c.px[y, x] = "cream_hi"
    return c.px


BODY_LIT = [_lit_body(0), _lit_body(1)]
BODY_SIL = [opaque(b) for b in BODY_LIT]


def slab(x0, y0, x1, y1, tilt):
    m = np.zeros((H, W), bool)
    for y in range(y0, y1 + 1):
        o = round(tilt * (y1 - y) / max(1, y1 - y0))
        m[y, x0 + o:x1 + o + 1] = True
    return m, (lambda y: round(tilt * (y1 - y) / max(1, y1 - y0)))


def board_masks(x0, y0, x1, y1, tilt):
    board, off = slab(x0, y0, x1, y1, tilt)
    mid = (x0 + x1) // 2 + off(y0)
    clip = rect(mid - 2, y0 - 2, mid + 2, y0 + 1)
    return board, clip, off, mid


def draw_board(c, x0, y0, x1, y1, tilt, tick, flash):
    board, clip, off, mid = board_masks(x0, y0, x1, y1, tilt)
    solid(c, board, "grey", "grey_d", th=1, sx=2, sy=2, bx=1, by=1)
    paper, _ = slab(x0 + 2, y0 + 3, x1 - 2, y1 - 2, tilt)
    c.fill(paper, "white" if flash else "cream_lt")
    if not flash:
        c.fill(paper & ~shift_m(paper, 1, 1), "cream_hi")  # top-left edge lit
        c.fill(paper & ~shift_m(paper, -1, -1), "cream_bs")  # lower-right edge in light shade
    py0 = y0 + 3
    nlines = 3 if y1 - y0 > 15 else 2
    for r in (1, 3, 5)[:nlines]:
        y = py0 + r
        o = off(y)
        c.fill(rect(x0 + 3 + o, y, x1 - 4 + o - (r == 5) * 3, y), "grey_d")
    solid(c, clip, "grey", "grey_d", th=1, sx=1, sy=1, bx=1, by=1)
    c.fill(rect(mid - 1, y0 - 1, mid + 1, y0 - 1), "grey_sh")
    c.fill(pix([(mid - 2, y0 - 2)]), "white")  # specular glint on the metal clip
    by = y1 - 4
    for i in range(min(tick, len(CHECK))):
        dx, dy = CHECK[i]
        x = x0 + 3 + dx + off(by + dy)
        c.fill(pix([(x, by + dy), (x, by + dy + 1), (x + 1, by + dy)]), "green")
    if tick:
        dx, dy = CHECK[min(tick, len(CHECK)) - 1]
        return x0 + 3 + dx + off(by + dy), by + dy
    return x0 + 3, by


def shift_m(m, dx, dy):
    return np.roll(m, (dy, dx), (0, 1))


def limb_mask(S, P, bend=2.5, fingers=True):
    """Short rounded arm: shoulder S, elbow bulge, paw at P with three finger bumps toward the direction of travel."""
    S, P = np.array(S, float), np.array(P, float)
    d = P - S
    n = np.array([-d[1], d[0]]) / (np.linalg.norm(d) or 1)
    if n[1] < 0:
        n = -n
    E = (S + P) / 2 + n * bend
    m = taper(*S, *E, 3.5, 3.1) | taper(*E, *P, 3.1, 2.7) | ell(P[0], P[1], 3.1, 3.0)
    f = P - E
    f = f / (np.linalg.norm(f) or 1)
    nn = np.array([-f[1], f[0]])
    gaps = []
    if fingers:
        for s in (-2.2, 0, 2.2):
            q = P + f * (3.4 - abs(s) * .3) + nn * s
            m |= ell(q[0], q[1], 1.4, 1.4)
        for s in (-1.1, 1.1):
            gaps.append(tuple(np.round(P + f * 3.9 + nn * s).astype(int)))
            gaps.append(tuple(np.round(P + f * 3.0 + nn * s).astype(int)))
    return m, gaps


def draw_arm(c, S, P, bend=2.5):
    m, gaps = limb_mask(S, P, bend)
    solid(c, m, "teal", TD, th=2, sx=2, sy=2, bx=2, by=1)
    for g in gaps:
        if 0 <= g[1] < H and 0 <= g[0] < W and m[g[1], g[0]]:
            c.px[g[1], g[0]] = "teal_sh"
    return m


def fin_parts(c, g):
    solid(c, poly([(25, 13), (26, 9), (29, 6), (30, 10), (32, 9), (34, 7), (35, 13)]), "teal", TD, th=2, sx=2, sy=2, bx=1, by=1)
    solid(c, poly([(15, 22 + g), (10, 21 + g), (12, 24 + g), (9, 26 + g), (12, 28 + g), (15, 28 + g)]), "teal", TD,
          th=1, sx=1, sy=2, bx=1, by=1)
    solid(c, poly([(36, 21 + g), (42, 18 + g), (40, 23 + g), (44, 25 + g), (40, 28 + g), (36, 29 + g)]), "teal", TD,
          th=1, sx=2, sy=2, bx=1, by=1)


def head_group(p):
    c = Canvas()
    fin_parts(c, p.get("gill", 0))
    c.paste(HEAD)
    lid = p.get("lid", 0)  # 0 open, 1 half, 2 closed
    for x0, w in ((27, 5), (15, 4)):
        if lid == 2:
            c.fill(rect(x0, 23, x0 + w - 1, 23), TD)
        elif lid == 1:
            c.fill(rect(x0, 22, x0 + w - 1, 25) | rect(x0 + 1, 22, x0 + w - 2, 26), TD)
            c.fill(rect(x0, 21, x0 + w - 1, 21), "teal_sh")
        else:
            c.fill(rect(x0, 21, x0 + w - 1, 25) | rect(x0 + 1, 20, x0 + w - 2, 26), TD)
            c.fill(rect(x0, 19, x0 + w - 1, 19), "teal_sh")  # upper-lid shadow
            c.fill(rect(x0 + 1, 21, x0 + 2, 22), "white")
            c.fill(pix([(x0 + w - 2, 25)]), "white")
    c.fill(rect(30, 27, 33, 28) | rect(12, 27, 14, 28), "pink")
    c.fill(rect(20, 29, 25, 29) | pix([(19, 28), (26, 28)]), TD)
    return c.px


def fluke(c, root, tip):
    """Forked crescent fluke; planted at the stem, mid follows `root`, the top lobe follows `tip` (it lags)."""
    u, l = tip, root
    pts = [(42, 52), (42, 47), (43 + l // 2, 41), (45 + u, 36), (47 + u, 34), (47 + u, 39), (48 + l // 2, 43),
           (51 + l // 2, 43), (54 + l // 2, 45), (53 + l // 2, 48), (49, 51)]
    m = poly(pts)
    solid(c, m, "navy", "navy_d", th=2, sx=2, sy=3, bx=1, by=1)
    return dilate(m)


def render(p):
    c = Canvas()
    b = p.get("bob", 0)
    sw = p.get("swell", 0)
    grow, lift_, tick = p.get("grow", 0), p.get("lift", 0), p.get("tick", 0)
    hop = p.get("hop", 0)

    fluke(c, p.get("tail", 0), p.get("tip", p.get("tail", 0)))
    cast(c.px, BODY_SIL[sw], 3, 1, 2)  # body onto the tail root
    c.paste(BODY_LIT[sw])

    # collar and tie (re-lit), then the head's cast shadow onto them and the upper torso
    solid(c, ell(26.5, 34 + b, 7.5, 2.5), "navy", "navy_d", th=1, sx=2, sy=1, bx=1, by=1)
    solid(c, poly([(23, 37 + b), (26, 37 + b), (27, 41 + b), (25, 44 + b), (23, 41 + b)]), "navy", "navy_d", th=1, sx=1, sy=1, bx=1, by=1)
    solid(c, rect(23, 35 + b, 26, 37 + b), "navy", "navy_d", th=1, sx=1, sy=1, bx=1, by=1)
    head_sil = np.roll(HEAD_SIL, (b, 0), (0, 1)) if b else HEAD_SIL
    cast(c.px, head_sil, 2, 3, 2)
    c.paste(head_group(p), dy=b)

    # clipboard (cast onto the belly first), left paw
    x0, x1 = 11 - grow, 24 + grow
    y0, y1 = 33 - lift_ - grow, 47 - lift_ + grow
    tilt = 2 if grow else 0
    board, clip, _, _ = board_masks(x0, y0 + b, x1, y1 + b, tilt)
    cast(c.px, dilate(board) | dilate(clip), 2, 2, 2)
    solid(c, ell(x0 - 1.5, y1 + b - 3.5, 3.4, 4.2), "teal", TD, th=2, sx=2, sy=2, bx=2, by=1)  # left forearm behind the board
    tip = draw_board(c, x0, y0 + b, x1, y1 + b, tilt, tick, p.get("flash", False))
    for q in ((x0 + 1.5, y1 + b - 6.5), (x0 + 2, y1 + b - 4), (x0 + 2, y1 + b - 1.5)):  # left-hand fingers over the board edge
        solid(c, ell(q[0], q[1], 1.6, 1.5), "teal", TD, th=1, sx=1, sy=1, bx=1, by=1)

    # near arm: hold -> pen -> wave, blended by 0..1 tracks
    hold = np.array([x1 + 1.0, y1 + b - 3.0])
    S = (HOLD_S[0], HOLD_S[1] + b)
    r = p.get("raise", 0)
    pen = p.get("pen", 0)
    if pen:
        target = np.array([tip[0] + 5.0, tip[1] - 4.0])
        P = hold + (target - hold) * pen
        pm, _ = limb_mask(S, P, 2.5)
        cast(c.px, dilate(pm), 1, 2, 1)
        for i in range(1, 5):
            c.px[int(P[1]) + i, int(P[0]) - i - 1] = "navy_d"
        draw_arm(c, S, P, 2.5)
    elif r:
        wv = p.get("wave", 1)
        target = np.array([44.0 + (wv - 1) * 2, 27.0 + b])
        P = hold + (target - hold) * r
        pm, _ = limb_mask(S, P, 2.5)
        cast(c.px, dilate(pm), 1, 2, 1)
        draw_arm(c, S, P, 2.5)
    else:
        pm, _ = limb_mask(S, hold, 2.5)
        cast(c.px, dilate(pm), 1, 2, 1)
        draw_arm(c, S, hold, 2.5)

    img = c.to_image(C)
    img = crouch(img, 50, p.get("crouch", 0))
    return lift(img, hop - 1)  # -1: the traced base's bottom outline row (59) lands on the y=60 baseline


# ---------------- animation tracks ----------------
def _idle():
    n = 14
    bob = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
    tail = [-1, -1, 0, 0, 1, 2, 2, 3, 3, 2, 2, 1, 0, 0]
    lid = [0] * 8 + [1, 2, 1] + [0] * 3
    frames = []
    for f in range(n):
        ms = 70 if lid[f] else 230
        frames.append((dict(bob=bob[f], swell=1 - bob[f], tail=tail[f], tip=tail[(f - 2) % n],
                            gill=bob[(f - 1) % n], lid=lid[f]), ms))
    return frames


def _greet():
    #      crouch hop raise wave ms
    rows = [(1, 0, 0, 1, 70), (2, 0, 0, 1, 70), (3, 0, 0, 1, 80), (1, 2, .35, 1, 50), (1, 4, .7, 1, 50),
            (2, 5, 1, 0, 50), (3, 6, 1, 1, 60), (3, 6, 1, 2, 60), (2, 5, 1, 1, 50), (1, 4, 1, 0, 50),
            (0, 2, 1, 1, 50), (2, 0, 1, 2, 70), (1, 0, 1, 1, 80), (0, 0, 1, 0, 100), (0, 0, .5, 1, 90), (0, 0, 0, 1, 120)]
    return [(dict(crouch=a, hop=h, raise_=r, wave=w, tail=[0, 0, 1, 1, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0][i],
                  tip=[0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0][i]), ms)
            for i, (a, h, r, w, ms) in enumerate(rows)]


def _action():
    #      grow lift crouch pen tick flash ms
    rows = [(0, 0, 0, 0, 0, 0, 90), (0, -1, 1, 0, 0, 0, 70), (0, -1, 1, 0, 0, 0, 70), (1, 0, 0, 0, 0, 0, 60),
            (2, 0, 0, 0, 0, 0, 60), (2, 0, 0, .33, 0, 0, 60), (2, 0, 0, .66, 0, 0, 50), (2, 0, 0, 1, 0, 0, 50),
            (2, 0, 0, 1, 2, 0, 60), (2, 0, 0, 1, 4, 0, 60), (2, 0, 0, 1, 7, 0, 60), (2, 0, 0, 1, 7, 1, 70),
            (2, 0, 0, .66, 7, 0, 160), (2, 0, 0, .33, 7, 0, 70), (1, 0, 0, 0, 7, 0, 70), (0, 0, 0, 0, 0, 0, 100)]
    return [(dict(grow=g, lift=l, crouch=cr, pen=pe, tick=t, flash=bool(fl)), ms) for g, l, cr, pe, t, fl, ms in rows]


def _fix(frames):
    out = []
    for pose, ms in frames:
        pose = dict(pose)
        if "raise_" in pose:
            pose["raise"] = pose.pop("raise_")
        out.append((pose, ms))
    return out


IDLE, GREET, ACTION = _idle(), _fix(_greet()), _action()
ANIMS = [("idle", True, None, IDLE), ("greet", False, "idle", GREET), ("action", False, "idle", ACTION)]
