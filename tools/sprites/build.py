"""Build a character sprite sheet: python tools/sprites/build.py resumon [more slugs]"""
import importlib, json, os, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
FR = 64
GREY, LAKE = (128, 128, 136), (56, 120, 168)


def clean(img):
    """Hard alpha, 15-bit colour snap, drop orphan pixels (no 8-neighbour)."""
    a = np.array(img)
    a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    a[..., :3] = (a[..., :3] // 8) * 8
    a[a[..., 3] == 0] = 0
    op = a[..., 3] > 0
    pad = np.pad(op, 1)
    n = sum(pad[1 + dy:1 + dy + FR, 1 + dx:1 + dx + FR].astype(int)
            for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dx, dy))
    a[op & (n == 0)] = 0
    return Image.fromarray(a, "RGBA")


def on_bg(img, bg, scale=4):
    base = Image.new("RGBA", img.size, (*bg, 255))
    base.alpha_composite(img)
    return base.convert("RGB").resize((img.width * scale, img.height * scale), Image.NEAREST)


def build(slug):
    os.chdir(ROOT)  # characters reference repo-relative asset paths
    mod = importlib.import_module(f"characters.{slug}")
    cols = max(len(f) for _, _, _, f in mod.ANIMS)
    sheet = Image.new("RGBA", (cols * FR, len(mod.ANIMS) * FR))
    meta = {"frame": {"w": FR, "h": FR}, "anchor": {"x": 32, "y": 60}, "animations": {}}
    gifs = {}
    for row, (name, loop, nxt, frames) in enumerate(mod.ANIMS):
        imgs = []
        for i, (pose, ms) in enumerate(frames):
            f = clean(mod.render(pose))
            sheet.paste(f, (i * FR, row * FR))
            imgs.append(f)
        entry = {"row": row, "loop": loop}
        if nxt:
            entry["next"] = nxt
        entry["frames"] = [{"ms": ms} for _, ms in frames]
        meta["animations"][name] = entry
        gifs[name] = (imgs, [ms for _, ms in frames])
    out = ROOT / "src/assets/sprites" / slug
    out.mkdir(parents=True, exist_ok=True)
    sheet.save(out / "sheet.png")
    (out / "sheet.json").write_text(json.dumps(meta, indent=2) + "\n")

    rev = ROOT / "generated/review/sprites" / slug
    rev.mkdir(parents=True, exist_ok=True)
    strips = [on_bg(sheet, GREY), on_bg(sheet, LAKE)]
    contact = Image.new("RGB", (strips[0].width, strips[0].height * 2))
    contact.paste(strips[0], (0, 0)); contact.paste(strips[1], (0, strips[0].height))
    contact.save(rev / "contact-sheet@4x.png")
    for name, (imgs, durs) in gifs.items():
        fr = [on_bg(i, LAKE) for i in imgs]
        fr[0].save(rev / f"{name}@4x.gif", save_all=True, append_images=fr[1:], duration=durs, loop=0, disposal=2)
    print(f"built {slug}: " + ", ".join(f"{n}={len(f)}f/{sum(m for _, m in f)}ms" for n, _, _, f in mod.ANIMS))


if __name__ == "__main__":
    for s in sys.argv[1:] or ["resumon"]:
        build(s)
