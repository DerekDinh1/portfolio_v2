"""Shared helpers for the battle-scene generators.

Everything draws into *role-indexed* canvases (uint8 ids, 0 = transparent) and is
turned into RGBA only at the end through a palette (role name -> hex).  That keeps
day and night geometry identical: night is just a different palette plus extras.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 240, 160


# --------------------------------------------------------------------------- colour
def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def q15(c):
    """Snap to the 15-bit grid (multiples of 8)."""
    return tuple(int(v) & 0xF8 for v in c)


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def ramp3(base_hex: str):
    """(highlight, base, shadow): shadows lean violet, highlights lean yellow."""
    b = hex_rgb(base_hex)
    hi = mix(mix(b, (255, 244, 170), 0.28), (255, 255, 255), 0.10)
    sh = mix(mix(b, (70, 60, 130), 0.34), (0, 0, 0), 0.10)
    return tuple("#%02X%02X%02X" % q15(c) for c in (hi, b, sh))


class RoleSet:
    def __init__(self, names):
        self.names = list(names)
        self._ids = {n: i + 1 for i, n in enumerate(self.names)}

    def __getitem__(self, name):
        return self._ids[name]


# --------------------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w: int, h: int, roles: RoleSet):
        self.w, self.h, self.roles = w, h, roles
        self.a = np.zeros((h, w), np.uint8)

    def put(self, x, y, role):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = self.roles[role]

    def hline(self, x0, x1, y, role):
        """Inclusive run."""
        for x in range(x0, x1 + 1):
            self.put(x, y, role)

    def rect(self, x, y, w, h, role):
        for yy in range(y, y + h):
            self.hline(x, x + w - 1, yy, role)

    def paint(self, mask, role):
        self.a[mask] = self.roles[role]

    def mask(self, *roles):
        return np.isin(self.a, [self.roles[r] for r in roles])

    def copy_from(self, other: "Canvas"):
        self.a = other.a.copy()

    def to_rgba(self, palette: dict[str, str]) -> np.ndarray:
        lut = np.zeros((256, 4), np.uint8)
        for name in self.roles.names:
            lut[self.roles[name]] = (*q15(hex_rgb(palette[name])), 255)
        return lut[self.a]


def grid(w=W, h=H):
    ys, xs = np.mgrid[0:h, 0:w]
    return xs, ys


# --------------------------------------------------------------------------- shapes
def periodic_profile(verts, w=W) -> np.ndarray:
    """Integer top-edge heights from (x, y) vertices, periodic over w.

    Linear interpolation then rounding gives natural stepped slopes (runs of equal y).
    """
    pts = sorted(verts)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    out = np.zeros(w, np.int32)
    for x in range(w):
        out[x] = math.floor(np.interp(x, xs, ys, period=w) + 0.5)
    return out


def open_profile(verts, w=W, empty=10_000) -> np.ndarray:
    """Like periodic_profile but only defined between the first and last vertex."""
    pts = sorted(verts)
    out = np.full(w, empty, np.int32)
    for x in range(pts[0][0], pts[-1][0] + 1):
        out[x] = math.floor(np.interp(x, [p[0] for p in pts], [p[1] for p in pts]) + 0.5)
    return out


def disc(cx, cy, r, w=W, h=H):
    xs, ys = grid(w, h)
    return (xs - cx) ** 2 + (ys - cy) ** 2 <= r * r + r


def checker(w=W, h=H, parity=0):
    xs, ys = grid(w, h)
    return ((xs + ys) % 2) == parity


def banded(cv: Canvas, edges, roles, dither=True):
    """Flat horizontal bands. edges = start rows; the last band runs to the bottom.

    A single checker row above each boundary is the only dither used.
    """
    xs, ys = grid(cv.w, cv.h)
    for i, role in enumerate(roles):
        y0 = edges[i]
        y1 = edges[i + 1] if i + 1 < len(edges) else cv.h
        cv.a[y0:y1, :] = cv.roles[role]
    if dither:
        for i in range(len(roles) - 1):
            b = edges[i + 1]
            row = (xs[b - 1] + (b - 1)) % 2 == 0
            cv.a[b - 1, row] = cv.roles[roles[i + 1]]


def tile_noise(w, h, cell, seed) -> np.ndarray:
    """Seamlessly tileable value noise in [0,1) (periodic lattice, smoothstep).

    Used to *choose where* clusters go, never as visible texture.
    """
    rng = np.random.default_rng(seed)
    gw, gh = max(1, w // cell), max(1, h // cell)
    lat = rng.random((gh, gw))
    xs = (np.arange(w) / cell)
    ys = (np.arange(h) / cell)
    x0 = np.floor(xs).astype(int) % gw
    y0 = np.floor(ys).astype(int) % gh
    x1, y1 = (x0 + 1) % gw, (y0 + 1) % gh
    fx = xs - np.floor(xs)
    fy = ys - np.floor(ys)
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    top = lat[np.ix_(y0, x0)] * (1 - fx) + lat[np.ix_(y0, x1)] * fx
    bot = lat[np.ix_(y1, x0)] * (1 - fx) + lat[np.ix_(y1, x1)] * fx
    return top * (1 - fy)[:, None] + bot * fy[:, None]


# --------------------------------------------------------------------------- checks
def seam_report(rgba: np.ndarray, frame_h: int = H):
    """Tile-seam continuity per frame.

    Returns (worst_seam_mismatch, worst_interior_mismatch): the number of rows whose pixel
    differs between the wrap pair (last col, first col) vs. between interior neighbours.
    A seam is fine if it is no more broken than the art is anywhere else.
    """
    worst_seam = worst_inner = 0
    for f in range(rgba.shape[0] // frame_h):
        fr = rgba[f * frame_h:(f + 1) * frame_h].astype(int)
        diff = (fr[:, 1:] != fr[:, :-1]).any(axis=2).sum(axis=0)
        seam = int((fr[:, 0] != fr[:, -1]).any(axis=1).sum())
        worst_seam = max(worst_seam, seam)
        worst_inner = max(worst_inner, int(diff.max()))
    return worst_seam, worst_inner


def colour_set(arrs) -> set:
    cols = set()
    for a in arrs:
        flat = a.reshape(-1, 4)
        vis = flat[flat[:, 3] == 255][:, :3]
        cols |= {tuple(int(v) for v in c) for c in np.unique(vis, axis=0)}
    return cols


def save_png(rgba: np.ndarray, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(path, optimize=True)


# --------------------------------------------------------------------------- scene model
@dataclass
class Layer:
    file: str            # path relative to the variant folder root, e.g. "day/00-sky.png"
    rgba: np.ndarray     # (160 * frames, w, 4)
    drift: int = 0
    frames: int = 1
    fps: int = 0

    @property
    def w(self):
        return self.rgba.shape[1]

    def frame(self, i: int) -> np.ndarray:
        i %= self.frames
        return self.rgba[i * H:(i + 1) * H]


@dataclass
class Variant:
    layers: list[Layer] = field(default_factory=list)
    platform: np.ndarray | None = None
    platform_file: str = ""
