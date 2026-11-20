"""Traced base: BOX-downscale a reference still, classify pixels into materials, re-ramp onto a fixed palette."""
import numpy as np
from PIL import Image

# material ids
TEAL, CREAM, NAVY, GREY, LINE, NONE = 1, 2, 3, 4, 5, 0


def downscale(path, height):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    w = round(im.width * height / im.height)
    a = np.asarray(im).astype(float)
    a[..., :3] *= a[..., 3:4] / 255  # premultiply: no dark fringes
    s = np.asarray(Image.fromarray(a.astype("uint8"), "RGBA").resize((w, height), Image.BOX)).astype(float)
    al = s[..., 3]
    rgb = np.where(al[..., None] > 0, s[..., :3] * 255 / np.maximum(al[..., None], 1), 0).clip(0, 255)
    return rgb, al >= 128


def classify(rgb, mask):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(-1), rgb.min(-1)
    m = np.zeros(mask.shape, np.uint8)
    m[mask] = TEAL
    lum = .3 * r + .59 * g + .11 * b
    m[mask & (r > 190)] = CREAM
    m[mask & (mx - mn < 50) & (mx > 90) & (lum <= 205)] = GREY
    m[mask & (b > g + 25) & (g < 140) & (b > 120) & (r < 110)] = NAVY
    m[mask & (mx < 115)] = LINE
    return m


def majority(m, mask, passes=1):
    """Replace isolated material speckle by the neighbourhood majority (LINE is left alone)."""
    h, w = m.shape
    for _ in range(passes):
        pad = np.pad(m, 1)
        out = m.copy()
        for y in range(h):
            for x in range(w):
                if not mask[y, x] or m[y, x] == LINE:
                    continue
                win = pad[y:y + 3, x:x + 3].ravel()
                win = win[(win != NONE) & (win != LINE)]
                if len(win) < 5:
                    continue
                vals, cnt = np.unique(win, return_counts=True)
                best = vals[cnt.argmax()]
                if cnt.max() >= 5 and best != m[y, x] and (win == m[y, x]).sum() <= 2:
                    out[y, x] = best
        m = out
    return m


def inpaint(m, hole, mask):
    """Fill `hole` pixels with the most common non-LINE material of their neighbours (grows inward)."""
    m = m.copy()
    hole = hole.copy()
    h, w = m.shape
    while hole.any():
        pad = np.pad(m, 1)
        changed = False
        for y, x in zip(*np.where(hole)):
            win = pad[y:y + 3, x:x + 3].ravel()
            win = win[(win != NONE) & (win != LINE) & (win != GREY)]
            win = win[win > 0]
            if len(win):
                m[y, x] = np.bincount(win).argmax()
                hole[y, x] = False
                changed = True
        if not changed:
            break
    return m


def keymap(path, height, ramps, dark, thr, size=64, feet=60, grey_box=None):
    """Traced base placed on a size x size canvas (feet at row feet-1, centred).

    ramps: {material: (hi, base, sh)} palette keys; dark: {material: key}; thr: {material: (hi_min, sh_max)} on luma.
    Returns (K object array of palette keys / None, M material array)."""
    rgb, mask = downscale(path, height)
    m = classify(rgb, mask)
    m = majority(m, mask)
    lum = .3 * rgb[..., 0] + .59 * rgb[..., 1] + .11 * rgb[..., 2]
    tone = np.ones(m.shape, np.uint8)  # 0 hi, 1 base, 2 sh
    for mat, (hi_min, sh_max) in thr.items():
        sel = m == mat
        tone[sel & (lum >= hi_min)] = 0
        tone[sel & (lum <= sh_max)] = 2
    # tone speckle filter: pixel differing from all same-material neighbours takes the neighbourhood mode
    pad_t, pad_m = np.pad(tone, 1, constant_values=1), np.pad(m, 1)
    t2 = tone.copy()
    for y, x in zip(*np.where(mask)):
        if m[y, x] in ramps:
            wm = pad_m[y:y + 3, x:x + 3].ravel() == m[y, x]
            wt = pad_t[y:y + 3, x:x + 3].ravel()[wm]
            if (wt == tone[y, x]).sum() <= 2 and len(wt) >= 6:
                t2[y, x] = np.bincount(wt).argmax()
    h, w = m.shape
    ox, oy = (size - w) // 2, feet - h
    K = np.full((size, size), None, object)
    M = np.zeros((size, size), np.uint8)
    for y in range(h):
        for x in range(w):
            if not mask[y, x]:
                continue
            mat = m[y, x]
            t_here = t2[y, x]
            if mat == GREY and grey_box and not (grey_box[0] <= x + ox <= grey_box[2] and grey_box[1] <= y + oy <= grey_box[3]):
                mat, t_here = TEAL, 0  # pale highlight misread as grey outside the clipboard
            if mat == LINE:
                win = pad_m[y:y + 3, x:x + 3].ravel()
                win = win[(win > 0) & (win != LINE)]
                mat = np.bincount(win).argmax() if len(win) else TEAL
                key = dark[mat]
            else:
                key = ramps[mat][t_here] if mat in ramps else dark.get(mat, ramps[TEAL][1])
            K[y + oy, x + ox] = key
            M[y + oy, x + ox] = mat
    return K, M
