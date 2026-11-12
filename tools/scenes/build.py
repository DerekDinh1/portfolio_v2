"""Build battle-scene backdrops. Usage: python tools/scenes/build.py [habitat ...]"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import review  # noqa: E402
import validate  # noqa: E402
from common import save_png  # noqa: E402
from habitats import REGISTRY  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "src" / "assets" / "scenes"
REVIEW = ROOT / "generated" / "review" / "scenes"


def build(name: str):
    mod = REGISTRY[name]
    folder = OUT / name
    if folder.exists():
        shutil.rmtree(folder)
    variants = {vn: mod.build(vn) for vn in ("day", "night")}
    spec = {"size": {"w": 240, "h": 160}, "platform": mod.PLATFORM, "variants": {}}
    for vn, v in variants.items():
        layers = []
        for L in v.layers:
            save_png(L.rgba, folder / L.file)
            e = {"file": L.file, "w": L.w, "drift": L.drift}
            if L.frames > 1:
                e.update(frames=L.frames, fps=L.fps)
            layers.append(e)
        save_png(v.platform, folder / v.platform_file)
        spec["variants"][vn] = {"layers": layers, "platform": v.platform_file}
    save_png(variants["day"].platform, folder / mod.PLATFORM["file"])
    (folder / "scene.json").write_text(json.dumps(spec, indent=2) + "\n")
    review.write_all(name, variants, mod.PLATFORM, REVIEW / name)
    return validate.check_scene(folder)


if __name__ == "__main__":
    names = sys.argv[1:] or list(REGISTRY)
    failed = False
    for n in names:
        errs = build(n)
        for e in errs:
            print("  FAIL", e)
        failed |= bool(errs)
    sys.exit(1 if failed else 0)
