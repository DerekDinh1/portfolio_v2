"""Validate a sheet against the art-bible sprite contract: python tools/sprites/validate.py resumon"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def check(slug):
    d = ROOT / "src/assets/sprites" / slug
    meta = json.loads((d / "sheet.json").read_text())
    a = np.array(Image.open(d / "sheet.png").convert("RGBA"))
    fw, fh = meta["frame"]["w"], meta["frame"]["h"]
    assert (fw, fh) == (64, 64), "frame must be 64x64"
    assert meta["anchor"] == {"x": 32, "y": 60}, "anchor"
    anims = meta["animations"]
    cols = max(len(v["frames"]) for v in anims.values())
    assert a.shape[:2] == (len(anims) * fh, cols * fw), f"sheet {a.shape[:2]} vs json {(len(anims)*fh, cols*fw)}"
    assert set(np.unique(a[..., 3])) <= {0, 255}, "alpha must be 0/255"
    op = a[a[..., 3] == 255][:, :3]
    assert (op % 8 == 0).all(), "channels must be multiples of 8"
    ncol = len(np.unique(op, axis=0))
    assert ncol <= 24, f"{ncol} colours"
    for name, v in anims.items():
        for c in range(cols):
            cell = a[v["row"] * fh:(v["row"] + 1) * fh, c * fw:(c + 1) * fw, 3] > 0
            if c >= len(v["frames"]):
                assert not cell.any(), f"{name}[{c}] should be empty"
                continue
            ys, xs = np.where(cell)
            assert len(ys), f"{name}[{c}] empty"
            # the resting pose keeps a 2px margin; a hop may use the top two rows
            top = 2 if name == "idle" else 0
            assert xs.min() >= 2 and ys.min() >= top and xs.max() <= 61 and ys.max() <= 61, \
                f"{name}[{c}] margin: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}"
    for c in range(len(anims["idle"]["frames"])):
        ys = np.where(a[anims["idle"]["row"] * fh:(anims["idle"]["row"] + 1) * fh, c * fw:(c + 1) * fw, 3] > 0)[0]
        assert ys.max() == 60, f"idle[{c}] feet at y={ys.max()}, expected 60"
    print(f"OK {slug}: sheet {a.shape[1]}x{a.shape[0]}, {ncol} colours, "
          + ", ".join(f"{n}={len(v['frames'])}f" for n, v in anims.items()))


if __name__ == "__main__":
    for s in sys.argv[1:] or ["resumon"]:
        check(s)
