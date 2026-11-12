"""Write a 4x horizontal strip PNG per animation (GIFs only show frame 1 in viewers): python tools/sprites/strip.py resumon"""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LAKE = (56, 120, 168, 255)


def strips(slug, scale=4):
    d = ROOT / "src/assets/sprites" / slug
    meta = json.loads((d / "sheet.json").read_text())
    sheet = Image.open(d / "sheet.png").convert("RGBA")
    out = ROOT / "generated/review/sprites" / slug
    for name, a in meta["animations"].items():
        n = len(a["frames"])
        strip = Image.new("RGBA", (64 * n, 64), LAKE)
        for i in range(n):
            strip.alpha_composite(sheet.crop((i * 64, a["row"] * 64, i * 64 + 64, a["row"] * 64 + 64)), (i * 64, 0))
        strip.convert("RGB").resize((64 * n * scale, 64 * scale), Image.NEAREST).save(out / f"{name}-strip@4x.png")


if __name__ == "__main__":
    for s in sys.argv[1:] or ["resumon"]:
        strips(s)
