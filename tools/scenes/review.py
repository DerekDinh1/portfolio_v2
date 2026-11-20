"""Review artefacts: 4x composites with layout overlays, tiling test, animated GIF."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from common import H, W, Variant

TEXT_BOX = (0, 112, 240, 48)
INFO_PANEL = (12, 16, 104, 34)
CREATURE = (144, 16, 64, 64)  # 64x64 sprite, feet at (176, 80)


def _over(dst: Image.Image, src: np.ndarray, x=0, y=0):
    dst.alpha_composite(Image.fromarray(np.ascontiguousarray(src), "RGBA"), (x, y))


def render(v: Variant, platform: dict, t: float = 0.0, width: int = W, origin: int = 0) -> Image.Image:
    """Compose the layers at time t (seconds). `width` > 240 lays layers out wider (tiling test)."""
    img = Image.new("RGBA", (width, H), (0, 0, 0, 255))
    for L in v.layers:
        fi = int(t * L.fps) % L.frames if L.frames > 1 else 0
        fr = L.frame(fi)
        off = int(np.floor(L.drift * t)) % L.w
        cols = (np.arange(width) + origin - off) % L.w
        _over(img, fr[:, cols])
    return img


def _overlay(img4: Image.Image):
    ov = Image.new("RGBA", img4.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    s = 4
    x, y, w, h = TEXT_BOX
    d.rectangle([x * s, y * s, (x + w) * s - 1, (y + h) * s - 1], fill=(255, 0, 255, 90), outline=(255, 0, 255, 200))
    x, y, w, h = INFO_PANEL
    d.rectangle([x * s, y * s, (x + w) * s - 1, (y + h) * s - 1], fill=(0, 255, 255, 70), outline=(0, 255, 255, 220))
    x, y, w, h = CREATURE
    d.rectangle([x * s, y * s, (x + w) * s - 1, (y + h) * s - 1], outline=(255, 255, 0, 200))
    img4.alpha_composite(ov)


def composite(v: Variant, platform: dict, t: float = 0.0, overlay=True) -> Image.Image:
    img = render(v, platform, t)
    _over(img, v.platform, platform["cx"] - platform["w"] // 2, platform["cy"] - platform["h"] // 2)
    img4 = img.resize((W * 4, H * 4), Image.NEAREST)
    if overlay:
        _overlay(img4)
    return img4


def tiling(v: Variant) -> Image.Image:
    """Two copies side by side (480 wide, native scale). Layers of width 480 tile at 480."""
    return render(v, {}, 0.0, width=480)


def wide(v: Variant, platform: dict) -> Image.Image:
    """480x112 crop at 2x (safe area = first 240 columns); platform at its contract position."""
    img = render(v, platform, 0.0, width=480)
    _over(img, v.platform, platform["cx"] - platform["w"] // 2, platform["cy"] - platform["h"] // 2)
    return img.crop((0, 0, 480, 112)).resize((960, 224), Image.NEAREST).convert("RGB")


def gif(v: Variant, platform: dict, path: Path, seconds=5, fps=8):
    frames = []
    for i in range(seconds * fps):
        im = composite(v, platform, i / fps, overlay=False).convert("RGB")
        frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=64))
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=1000 // fps, loop=0, disposal=1)


def write_all(name: str, variants: dict[str, Variant], platform: dict, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    for vn, v in variants.items():
        composite(v, platform).convert("RGB").save(out / f"{vn}@4x.png")
        tiling(v).convert("RGB").save(out / f"{vn}-tiling.png")
        wide(v, platform).save(out / f"{vn}-wide@2x.png")
        gif(v, platform, out / f"{vn}.gif")
