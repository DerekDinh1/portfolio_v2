"""The three starter capsules: an original pill-shaped canister with metal caps and a glass
core tinted by type, each with its own emblem. One 64x24 strip per type, four 16x24 frames:
closed, lid nudged left, lid nudged right and lifting, open. Only the lid moves, at the seam.

    tools/.venv/bin/python tools/sprites/capsules.py
"""
import pathlib

from PIL import Image
from tone import grade, grade_all

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "src/assets/sprites/capsules"
REVIEW = ROOT / "generated/review/sprites/capsules"
W, H = 16, 24

METAL = {"K": (40, 48, 72), "h": (232, 240, 248), "g": (168, 176, 200), "m": (104, 112, 144), "W": (248, 248, 248),
         "Y": (248, 240, 152)}
TYPES = {
    "water": dict(a=(152, 216, 248), A=(56, 144, 216), b=(32, 96, 168), emblem=["eeee", "e..e", "e..e", "eeee"]),  # bubble
    "fire": dict(a=(248, 200, 120), A=(232, 104, 48), b=(168, 56, 32), emblem=["..e.", ".ee.", "eeee", "eeee"]),   # flame
    "grass": dict(a=(176, 232, 136), A=(88, 168, 72), b=(48, 112, 64), emblem=["..ee", ".eee", "eee.", "e..."]),   # leaf
}

METAL = grade_all(METAL)
TYPES = {k: {n: (grade(v) if isinstance(v, tuple) else v) for n, v in t.items()} for k, t in TYPES.items()}

LID = [                      # the metal cap, four rows above the seam
    ".....KKKKKK.....",
    "....KhhhhhgK....",
    "...KhWhhhhggK...",
    "...KggggggmmK...",
]
SEAM_Y = 8                   # the rim line where the lid meets the glass
BODY = [
    "...KKKKKKKKKK...",    # rim
    "...KaAAAAAAbK...",
    "...KaAAAAAAbK...",
    "...KaAAAAAAbK...",
    "...KaAAAAAAbK...",
    "...KaAAAAAAbK...",
    "...KaAAAAAAbK...",
    "...KaAAAAAAbK...",
    "...KbbbbbbbbK...",
    "...KKKKKKKKKK...",
    "...KggggggmmK...",
    "...KhhhhhhgmK...",
    "....KggggmmK....",
    ".....KKKKKK.....",
]
# Light between the rim and the lifted lid. PEEK is the sliver shown mid-wobble.
PEEK = ["....YYYYYYYY...."]
BURST = [
    "..Y...KKKKKKKK..",    # underside of the lifted lid
    "...Y..YWWY..Y...",
    "....YYWWWWYY....",
    "....YWWWWWWY....",
]


def frame(kind, lid_dx=0, lid_dy=0, light=()):
    """lid_dx/lid_dy move the lid only; `light` rows sit directly above the rim."""
    spec = TYPES[kind]
    pal = {**METAL, "a": spec["a"], "A": spec["A"], "b": spec["b"], "e": METAL["W"]}
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def put(grid, y0, dx=0):
        for j, row in enumerate(grid):
            for x, ch in enumerate(row):
                if ch != "." and 0 <= x + dx < W and 0 <= y0 + j < H:
                    im.putpixel((x + dx, y0 + j), pal[ch] + (255,))

    body = [list(r) for r in BODY]
    for j, er in enumerate(spec["emblem"]):                 # emblem sits low in the glass
        for i, ch in enumerate(er):
            if ch == "e":
                body[3 + j][6 + i] = "e"
    put(["".join(r) for r in body], SEAM_Y)
    put(light, SEAM_Y - len(light))
    put(LID, SEAM_Y - len(LID) + lid_dy, lid_dx)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    review = Image.new("RGBA", (W * 4 * 8, H * 3 * 8), (208, 160, 104, 255))
    for r, kind in enumerate(TYPES):
        strip = Image.new("RGBA", (W * 4, H), (0, 0, 0, 0))
        frames = (frame(kind), frame(kind, lid_dx=-1), frame(kind, lid_dx=1, lid_dy=-1, light=PEEK),
                  frame(kind, lid_dx=2, lid_dy=-4, light=BURST))
        for i, im in enumerate(frames):
            strip.paste(im, (i * W, 0))
        used = {px for px in strip.get_flattened_data() if px[3]}
        assert len(used) <= 15, f"{kind}: {len(used)} colours"
        strip.save(OUT / f"{kind}.png")
        review.alpha_composite(strip.resize((W * 32, H * 8), Image.NEAREST), (0, r * H * 8))
        print(f"OK capsule {kind}: {strip.width}x{strip.height}, {len(used)} colours")
    review.save(REVIEW / "capsules@8x.png")


if __name__ == "__main__":
    main()
