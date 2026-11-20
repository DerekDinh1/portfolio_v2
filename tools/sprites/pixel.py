"""Pixel-exact drawing helpers shared by every character module (no anti-aliasing anywhere)."""
import numpy as np
from PIL import Image, ImageDraw

W = H = 64
_YS, _XS = np.mgrid[0:H, 0:W]


def ell(cx, cy, rx, ry):
    return ((_XS + .5 - cx) / rx) ** 2 + ((_YS + .5 - cy) / ry) ** 2 <= 1


def rect(x0, y0, x1, y1):
    return (_XS >= x0) & (_XS <= x1) & (_YS >= y0) & (_YS <= y1)


def poly(pts):
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.array(im) > 0


def capsule(x0, y0, x1, y1, r):
    dx, dy = x1 - x0, y1 - y0
    L = dx * dx + dy * dy or 1
    t = np.clip(((_XS + .5 - x0) * dx + (_YS + .5 - y0) * dy) / L, 0, 1)
    return (_XS + .5 - (x0 + t * dx)) ** 2 + (_YS + .5 - (y0 + t * dy)) ** 2 <= r * r


def taper(x0, y0, x1, y1, r0, r1):
    """Capsule whose radius changes linearly from r0 (at p0) to r1 (at p1): a bent limb is a chain of these."""
    dx, dy = x1 - x0, y1 - y0
    L = dx * dx + dy * dy or 1
    t = np.clip(((_XS + .5 - x0) * dx + (_YS + .5 - y0) * dy) / L, 0, 1)
    r = r0 + (r1 - r0) * t
    return (_XS + .5 - (x0 + t * dx)) ** 2 + (_YS + .5 - (y0 + t * dy)) ** 2 <= r * r


def pix(pts):
    m = np.zeros((H, W), bool)
    for x, y in pts:
        if 0 <= x < W and 0 <= y < H:
            m[int(y), int(x)] = True
    return m


def shift(m, dx, dy):
    return np.roll(m, (int(dy), int(dx)), (0, 1))


def dilate(m):
    return m | shift(m, 1, 0) | shift(m, -1, 0) | shift(m, 0, 1) | shift(m, 0, -1)


class Canvas:
    """Canvas of palette keys (object array, None = transparent); colours resolved in to_image()."""

    def __init__(self, K=None):
        self.px = np.full((H, W), None, object) if K is None else K.copy()

    def fill(self, mask, key):
        self.px[mask] = key

    def part(self, mask, base, hi=None, sh=None, rim=None, clip=None, hl=1, sd=2):
        """Paint a part: optional 1px rim, base, top-left highlight band, bottom-right shadow band."""
        if rim is not None:
            self.fill(dilate(mask), rim)
        lit = mask & ~shift(mask, hl, hl)
        dark = mask & ~shift(mask, -sd, -sd)
        k = mask if clip is None else mask & clip
        self.fill(k, base)
        if hi is not None:
            self.fill(lit & k & ~dark, hi)
        if sh is not None:
            self.fill(dark & k, sh)

    def paste(self, K, dx=0, dy=0, where=None):
        ys, xs = np.where(K != None)  # noqa: E711 (elementwise on object array)
        for y, x in zip(ys, xs):
            if where is not None and not where[y, x]:
                continue
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W:
                self.px[ny, nx] = K[y, x]

    def to_image(self, pal):
        a = np.zeros((H, W, 4), np.uint8)
        for y, x in zip(*np.where(self.px != None)):  # noqa: E711
            a[y, x] = (*pal[self.px[y, x]], 255)
        return Image.fromarray(a, "RGBA")


def crouch(img, start, k):
    """Delete k pixel rows from `start` down and shift everything above them down by k (squash / tucked legs)."""
    a = np.array(img)
    if k > 0:
        out = np.zeros_like(a)
        out[k:start + k] = a[:start]
        out[start + k:] = a[start + k:]
        a = out
    return Image.fromarray(a, "RGBA")


def lift(img, hop):
    return Image.fromarray(np.roll(np.array(img), -int(hop), 0), "RGBA") if hop else img


def reoutline(K, dark_of, rows=None):
    """Any non-outline pixel left with a transparent 4-neighbour becomes an outline pixel in the dark of its colour."""
    op = K != None  # noqa: E711
    edge = op & ~(shift(op, 1, 0) & shift(op, -1, 0) & shift(op, 0, 1) & shift(op, 0, -1))
    out = K.copy()
    for y, x in zip(*np.where(edge)):
        if rows and not rows[0] <= y <= rows[1]:
            continue
        d = dark_of(K[y, x])
        if d:
            out[y, x] = d
    return out


# ---- cel lighting: 4 flat tones per material, key light from the top-left ----
TONES = ("hi", "lt", "bs", "sh")


def split_key(k):
    if k is None or "_" not in k:
        return None, None
    fam, tone = k.rsplit("_", 1)
    return (fam, TONES.index(tone)) if tone in TONES else (None, None)


def flatten(K):
    """Collapse every toned key to its family's light tone (the traced base only supplies material)."""
    out = K.copy()
    for y, x in zip(*np.where(K != None)):  # noqa: E711
        fam, t = split_key(K[y, x])
        if fam:
            out[y, x] = f"{fam}_lt"
    return out


def bands(geo, th=2, sx=3, sy=3, bx=3, by=2):
    """Hard-edged tone map: 0 highlight (top-left rim), 1 light, 2 base, 3 core shadow (bottom-right crescent)."""
    sh = geo & ~shift(geo, -sx, -sy)
    bs = geo & ~shift(geo, -(sx + bx), -(sy + by)) & ~sh
    hi = geo & ~shift(geo, th, th) & ~sh & ~bs
    t = np.full(geo.shape, -1, int)
    t[geo] = 1
    t[hi], t[bs], t[sh] = 0, 2, 3
    return t


def apply_bands(px, geo, t=None, rim_light=False, soften=(), **kw):
    t = bands(geo, **kw) if t is None else t
    interior_edge = geo & ~shift(geo, -1, 0)  # right-most column of each row
    for y, x in zip(*np.where(geo)):
        fam, _ = split_key(px[y, x])
        if fam:
            tone = t[y, x]
            if rim_light and interior_edge[y, x] and tone == 3 and t[y, max(0, x - 1)] == 3:
                tone = 2  # thin rim light on the shadow-side edge
            if fam in soften and tone > 1:
                tone -= 1  # pale materials keep a lighter shade
            px[y, x] = f"{fam}_{TONES[tone]}"


def cast(px, caster, dx, dy, steps=2):
    """Cast shadow of `caster` (bool mask incl. outline) onto what is already drawn: step tones darker."""
    m = shift(caster, dx, dy) & ~caster
    for y, x in zip(*np.where(m)):
        fam, t = split_key(px[y, x])
        if fam:
            px[y, x] = f"{fam}_{TONES[min(3, t + steps)]}"


def solid(c, mask, fam, rim, **kw):
    """Draw a part: 1px rim, light-tone fill, then cel bands from its own silhouette."""
    if rim:
        c.fill(dilate(mask), rim)
    c.fill(mask, f"{fam}_lt")
    apply_bands(c.px, mask, **kw)
    return dilate(mask) if rim else mask
