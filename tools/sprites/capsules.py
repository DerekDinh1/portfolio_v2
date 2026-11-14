"""The three starter capsules: an original pill-shaped canister with metal caps and a glass
core tinted by type, each with its own emblem. One 64x24 strip per type, four 16x24 frames:
closed, tilted left, tilted right, open.

    tools/.venv/bin/python tools/sprites/capsules.py
"""
import pathlib

from PIL import Image

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

CLOSED = [
    "................",
    "................",
    ".....KKKKKK.....",
    "....KhhhhhgK....",
    "...KhWhhhhggK...",
    "...KggggggmmK...",
    "...KKKKKKKKKK...",
    "...KaAAAAAAbK...",
    "...KaWAAAAAbK...",
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
    "................",
    "................",
    "................",
    "................",
]
# Open: the cap swings up and to the right, and light pours out of the glass.
OPEN = [
    ".......KKKKKK...",
    "......KhhhhhgK..",
    ".....KhWhhhhggK.",
    ".....KggggggmmK.",
    "..Y...KKKKKKKK..",
    "...Y...Y....Y...",
    "....Y.YWY..Y....",
    "...KYWWWWWWYK...",
    "...KaYWWWWYbK...",
    "...KaAYWWYAbK...",
] + CLOSED[10:]


def frame(grid, kind, shear=0):
    spec = TYPES[kind]
    pal = {**METAL, "a": spec["a"], "A": spec["A"], "b": spec["b"], "e": METAL["W"]}
    rows = [list(r) for r in grid]
    for j, er in enumerate(spec["emblem"]):                 # emblem sits low in the glass
        for i, ch in enumerate(er):
            if ch == "e":
                rows[10 + j][6 + i] = "e"
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        dx = shear if y < 10 else 0                         # only the top half leans when it wobbles
        for x, ch in enumerate(row):
            if ch != "." and 0 <= x + dx < W:
                im.putpixel((x + dx, y), pal[ch] + (255,))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    review = Image.new("RGBA", (W * 4 * 8, H * 3 * 8), (208, 160, 104, 255))
    for r, kind in enumerate(TYPES):
        strip = Image.new("RGBA", (W * 4, H), (0, 0, 0, 0))
        for i, im in enumerate((frame(CLOSED, kind), frame(CLOSED, kind, -1), frame(CLOSED, kind, 1), frame(OPEN, kind))):
            strip.paste(im, (i * W, 0))
        used = {px for px in strip.get_flattened_data() if px[3]}
        assert len(used) <= 15, f"{kind}: {len(used)} colours"
        strip.save(OUT / f"{kind}.png")
        review.alpha_composite(strip.resize((W * 32, H * 8), Image.NEAREST), (0, r * H * 8))
        print(f"OK capsule {kind}: {strip.width}x{strip.height}, {len(used)} colours")
    review.save(REVIEW / "capsules@8x.png")


if __name__ == "__main__":
    main()
