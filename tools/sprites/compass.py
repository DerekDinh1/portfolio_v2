"""The 404 page's compass: a small framed dial whose needle cannot settle. One 272x17 strip,
sixteen 17x17 frames, the needle turning a sixteenth of a circle clockwise per frame.

    tools/.venv/bin/python tools/sprites/compass.py
"""
import math
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "src/assets/sprites/lost"
REVIEW = ROOT / "generated/review/sprites/lost"
S, FRAMES = 17, 16

PAL = {"K": (24, 32, 48), "g": (232, 240, 248), "m": (168, 176, 200), "W": (248, 248, 240),
       "n": (88, 96, 128), "r": (216, 56, 48), "t": (120, 136, 168)}

TILE = [                      # frame and dial; the needle is drawn on top
    "..KKKKKKKKKKKKK..",
    ".KggggggggggggmK.",
    "KggggnnnnnnnggmmK",
    "KgggnWWWnWWWnggmK",
    "KggnWWWWWWWWWngmK",
    "KgnWWWWWWWWWWWnmK",
    "KgnWWWWWWWWWWWnmK",
    "KgnWWWWWWWWWWWnmK",
    "KgnnWWWWWWWWWnnmK",
    "KgnWWWWWWWWWWWnmK",
    "KgnWWWWWWWWWWWnmK",
    "KgnWWWWWWWWWWWnmK",
    "KggnWWWWWWWWWnmmK",
    "KgggnWWWnWWWnmmmK",
    "KgmmmnnnnnnnmmmmK",
    ".KmmmmmmmmmmmmmK.",
    "..KKKKKKKKKKKKK..",
]


def needle(i):
    """Pixels of the needle for frame i: red toward the heading, grey behind, a pin in the middle."""
    a = i * 2 * math.pi / FRAMES
    dx, dy = math.sin(a), -math.cos(a)
    px = {}
    for step in range(1, 9):                       # grey tail, 3.5 long
        t = step * 0.45
        if t <= 3.6:
            px[(round(8 - dx * t), round(8 - dy * t))] = "t"
    for step in range(1, 12):                      # red point, 4.6 long
        t = step * 0.42
        px[(round(8 + dx * t), round(8 + dy * t))] = "r"
    px[(8, 8)] = "K"
    return px


def frame(i):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    for y, row in enumerate(TILE):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    for (x, y), ch in needle(i).items():
        im.putpixel((x, y), PAL[ch] + (255,))
    return im


def main():
    assert all(len(r) == S for r in TILE) and len(TILE) == S
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    strip = Image.new("RGBA", (S * FRAMES, S), (0, 0, 0, 0))
    for i in range(FRAMES):
        strip.alpha_composite(frame(i), (i * S, 0))
    strip.save(OUT / "compass.png")
    review = Image.new("RGBA", (S * 8 * 8, S * 2 * 8), (40, 88, 48, 255))
    for i in range(FRAMES):
        review.alpha_composite(frame(i).resize((S * 8, S * 8), Image.NEAREST), ((i % 8) * S * 8, (i // 8) * S * 8))
    review.save(REVIEW / "compass@8x.png")
    print("wrote", OUT / "compass.png")


if __name__ == "__main__":
    main()
