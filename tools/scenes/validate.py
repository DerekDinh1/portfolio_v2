"""Validate a generated scene folder against the art-bible Scene contract.

Usage: python tools/scenes/validate.py [habitat ...]   (default: every folder in src/assets/scenes)
Exit code 1 on any failure.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from common import H, colour_set, seam_report

ROOT = Path(__file__).resolve().parents[2]
SCENES = ROOT / "src" / "assets" / "scenes"
MAX_COLOURS = 64


def check_scene(folder: Path) -> list[str]:
    errs: list[str] = []
    ok = lambda cond, msg: errs.append(msg) if not cond else None  # noqa: E731
    spec = json.loads((folder / "scene.json").read_text())
    ok(spec["size"] == {"w": 240, "h": 160}, "size must be 240x160")
    pf = spec["platform"]
    listed = {pf["file"]}
    ptop = Image.open(folder / pf["file"]).convert("RGBA")
    ok(ptop.size == (pf["w"], pf["h"]), f"{pf['file']} size {ptop.size} != platform {pf['w']}x{pf['h']}")
    report = []
    for vname, var in spec["variants"].items():
        arrs = []
        listed.add(var["platform"])
        plat = np.array(Image.open(folder / var["platform"]).convert("RGBA"))
        ok(plat.shape[:2] == (pf["h"], pf["w"]), f"{var['platform']} wrong size {plat.shape[:2]}")
        arrs.append(plat)
        for L in var["layers"]:
            listed.add(L["file"])
            p = folder / L["file"]
            if not p.exists():
                errs.append(f"missing file {L['file']}")
                continue
            im = np.array(Image.open(p).convert("RGBA"))
            frames = L.get("frames", 1)
            ok(im.shape[0] == H * frames, f"{L['file']}: height {im.shape[0]} != 160*{frames}")
            ok(im.shape[1] in (240, 480), f"{L['file']}: width {im.shape[1]} not 240/480")
            ok(im.shape[1] == L["w"], f"{L['file']}: width {im.shape[1]} != json w {L['w']}")
            ok(isinstance(L.get("drift"), int), f"{L['file']}: drift must be an int")
            if frames > 1:
                ok(L.get("fps", 0) > 0, f"{L['file']}: animated layer needs fps")
            ok(set(np.unique(im[..., 3])) <= {0, 255}, f"{L['file']}: alpha not 0/255")
            vis = im[im[..., 3] == 255][:, :3]
            ok(bool((vis % 8 == 0).all()), f"{L['file']}: channels not multiples of 8")
            seam, inner = seam_report(im)
            ok(seam <= inner, f"{L['file']}: seam mismatch {seam} rows > interior max {inner}")
            report.append(f"    {L['file']:<22} {im.shape[1]}x{im.shape[0]:<4} seam={seam:<3} (interior max {inner})")
            arrs.append(im)
        ok(set(np.unique(plat[..., 3])) <= {0, 255}, f"{var['platform']}: alpha not 0/255")
        pv = plat[plat[..., 3] == 255][:, :3]
        ok(bool((pv % 8 == 0).all()), f"{var['platform']}: channels not multiples of 8")
        n = len(colour_set(arrs))
        ok(n <= MAX_COLOURS, f"variant {vname}: {n} colours > {MAX_COLOURS}")
        report.append(f"  {vname}: {len(var['layers'])} layers, {n} colours")
    on_disk = {str(p.relative_to(folder)) for p in folder.rglob("*.png")}
    ok(on_disk == listed, f"files on disk != scene.json: extra={sorted(on_disk - listed)} missing={sorted(listed - on_disk)}")
    print(f"[{folder.name}]")
    print("\n".join(report))
    return errs


def main(argv: list[str]) -> int:
    names = argv or sorted(p.parent.name for p in SCENES.glob("*/scene.json"))
    bad = 0
    for n in names:
        errs = check_scene(SCENES / n)
        for e in errs:
            print(f"  FAIL {e}")
        print(f"  {'FAIL' if errs else 'OK'}: {n}")
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
