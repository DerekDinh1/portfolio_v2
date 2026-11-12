"""Resumon front sprite: the original mascot design redrawn as a 64x64 GBA-style sprite.

The pose, proportions and props come from `src/assets/mascots/resumon.png` (traced to
a 56px-tall grid as a guide), then every row was redrawn by hand in a fixed
15-colour palette with clean outlines and hard-edged tones.

Each row is "y x0 x1 runs"; a run is a palette glyph plus a count ("T5" = five
pixels). The width is checked against x0..x1, so a miscounted row fails loudly.
Groups are stacked back to front and moved in whole pixels to animate.

    tools/.venv/bin/python tools/sprites/resumon_hand.py
"""
import json
import pathlib
import re

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "src/assets/sprites/resumon"
REVIEW = ROOT / "generated/review/sprites/resumon"
SIZE = 64

PALETTE = {
    "K": (24, 40, 72),      # outline, eyes
    "D": (16, 96, 128),     # teal, deepest (nostrils, moustache)
    "t": (40, 152, 176),    # teal shadow
    "T": (80, 208, 216),    # teal
    "U": (168, 240, 240),   # teal highlight
    "C": (240, 248, 240),   # pale underside
    "c": (176, 224, 224),   # underside shadow
    "N": (40, 96, 160),     # navy (tail, tie, collar)
    "n": (24, 64, 120),     # navy shadow
    "M": (72, 136, 200),    # navy highlight
    "G": (152, 160, 184),   # clipboard
    "g": (104, 112, 144),   # clipboard shadow, clip
    "W": (248, 248, 248),   # eye shine
    "P": (248, 200, 176),   # blush
    "V": (56, 184, 72),     # check mark
}


def rows(spec):
    out = []
    for line in spec.strip().splitlines():
        y, x0, x1, runs = re.match(r"\s*(\d+)\s+(\d+)\s+(\d+)\s+(.*)", line).groups()
        pix = "".join(tok[0] * int(tok[1:] or 1) for tok in runs.split())
        assert len(pix) == int(x1) - int(x0) + 1, f"row y={y}: {len(pix)} px for x {x0}..{x1}: {runs}"
        out.append((int(y), int(x0), pix))
    return out


HEAD = rows("""
5 29 30 K2
6 27 31 K T t2 K
7 26 31 K T2 t2 K
8 25 31 K U T2 t2 K
9 24 31 K U T3 t2 K
10 20 31 K4 U T4 t2 K
11 18 32 K2 U3 T7 t K2
12 17 34 K U4 T10 t K2
13 16 35 K U5 T11 t2 K
14 15 36 K U6 T11 t3 K
15 14 36 K U6 T12 t3 K
16 13 37 K T2 U4 T14 t3 K
17 13 38 K U T19 t4 K
18 12 38 K U T20 t4 K
19 12 38 K T K T11 K3 T8 t K
20 12 38 K K W K T9 K W2 K2 T7 t K
21 12 39 K K W K T9 K W2 K2 T7 t2 K
22 12 39 K4 T9 K5 T7 t2 K
23 12 38 K4 T9 K3 W K T7 t K
24 12 38 K3 T2 D T2 D T5 K3 T8 t K
25 11 38 K T4 D6 T7 P3 T5 t K
26 10 38 K T3 K D3 K2 D4 K T3 P4 T5 t K
27 10 38 K C4 K3 C2 K4 C2 T2 P4 T5 t K
28 10 38 K C21 T5 t K
29 11 38 K C20 c T4 t K
30 13 37 K C18 c2 T2 t K
31 14 35 K2 C13 c4 t K2
32 16 33 K2 c3 C6 c4 K3
33 19 31 K2 c7 K4
22 40 42 K3
23 39 43 T U T t K
24 39 42 T2 t K
25 39 42 T t K2
26 39 43 U T2 t K
27 39 42 T2 t K
28 39 41 t K2
29 39 40 K2
22 10 11 K2
23 9 11 K U T
24 9 11 K T t
25 9 10 K2
""")
EYES_HALF = rows("""
19 13 37 T25
20 13 37 T25
21 13 15 K3
21 25 29 K5
""")
EYES_SHUT = rows("""
19 13 37 T25
20 13 37 T25
21 13 37 T25
22 13 15 K3
22 16 24 T9
22 25 29 K5
23 13 37 T25
24 13 37 T4 D T2 D T17
""")

BOARD = rows("""
36 15 18 K4
37 11 21 K11
38 11 21 K G3 g3 G3 K
39 11 21 K G9 K
40 11 21 K G C7 G K
41 11 21 K G C7 G K
42 11 21 K G C g5 C G K
43 11 21 K G C7 G K
44 11 21 K G C g4 C2 G K
45 11 21 K G C7 g K
46 11 21 K g9 K
47 11 21 K11
""")
CHECK = rows("""
41 18 19 V2
42 17 18 V2
43 13 14 V2
43 16 17 V2
44 14 16 V3
45 15 15 V
""")
HAND_L = rows("""
42 10 13 K4
43 9 13 K U T2 K
44 9 13 K T t2 K
45 10 13 K4
""")

BODY = rows("""
34 19 32 K n N4 M N3 n2 K2
35 18 33 K2 N4 K N2 K N3 n K2
36 19 34 K9 U T4 t K
37 22 34 N2 K C3 T5 t K
38 22 35 N2 n C3 T6 t K
39 22 35 M N n C c T7 t K
40 22 35 n2 K T9 t K
41 22 36 K U T10 t2 K
42 22 36 K T11 t2 K
42 19 21 K3
43 19 36 K U T12 t3 K
44 19 36 K T13 t3 K
45 19 36 K t7 T5 t4 K
46 20 36 K6 t T6 t3 K
47 22 37 K2 c2 C2 T6 t3 K
48 15 38 K T c12 T6 t3 K
49 15 38 K T C13 T5 t3 K
50 15 38 K T2 C12 T5 t3 K
51 15 38 K T2 C11 T6 t3 K
52 15 38 K T3 C9 c T6 t3 K
53 15 38 K T4 C6 c2 T7 t3 K
54 15 38 K t T4 c6 T7 t4 K
55 15 37 K t7 c3 t T6 t4 K
56 16 37 K t7 K5 T4 t4 K
57 15 23 K2 t6 K
57 28 37 K t T4 t3 K
58 15 23 K T2 t5 K
58 29 37 K T5 t2 K
59 15 23 K9
59 28 36 K T3 t4 K
60 29 35 K7
""")
STALK = rows("""
47 39 42 K4
48 38 42 t T3 t
49 38 43 t T3 t2
50 38 43 t6
51 38 43 t6
52 39 44 K6
""")
FLUKE = rows("""
36 47 47 K
37 45 47 K N K
38 44 47 K M N K
39 43 47 K M N2 K
40 43 48 K M N2 n K
41 42 48 K M N3 n K
42 42 48 K M N3 n K
43 42 48 K N4 n K
44 41 48 K M N4 n K
45 41 47 K N4 n K
46 42 50 K N3 n K4
47 42 52 K N5 n2 K3
48 43 53 K N7 n2 K
49 44 53 N6 n3 K
50 44 52 K n6 K2
51 45 50 K6
""")


def stamp(im, layer, dx=0, dy=0):
    for y, x0, pix in layer:
        for i, ch in enumerate(pix):
            x, yy = x0 + i + dx, y + dy
            if 0 <= x < SIZE and 0 <= yy < SIZE:
                im.putpixel((x, yy), PALETTE[ch] + (255,))


def frame(bob=0, tail=0, eyes="open", lift=0, check=False, flash=False, hop=0):
    """bob: head down px. tail: fluke up(-)/down(+) px. lift: clipboard up px. hop: whole sprite up px."""
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    stamp(im, BOARD, dy=-lift - hop)
    if flash:
        stamp(im, [(y, 13, "W" * 7) for y in range(40, 46)], dy=-lift - hop)
    elif check:
        stamp(im, CHECK, dy=-lift - hop)
    stamp(im, BODY, dy=-hop)
    stamp(im, HAND_L, dy=-lift - hop)
    stamp(im, STALK, dy=-hop)
    stamp(im, FLUKE, dy=tail - hop)
    stamp(im, HEAD, dy=bob - hop)
    if eyes == "half":
        stamp(im, EYES_HALF, dy=bob - hop)
    elif eyes == "shut":
        stamp(im, EYES_SHUT, dy=bob - hop)
    return im


I = lambda ms, **kw: (frame(**kw), ms)
ANIMS = {
    "idle": [
        I(240), I(200, tail=-1), I(200, bob=1, tail=-1), I(240, bob=1, tail=-2), I(200, bob=1, tail=-1),
        I(200, tail=-1), I(240), I(200, tail=1), I(70, eyes="half", tail=1), I(90, eyes="shut", tail=1),
        I(70, eyes="half"), I(240),
    ],
    "greet": [
        I(70, bob=1), I(80, bob=2, eyes="half"), I(50, hop=1, tail=-1), I(50, hop=2, tail=-2), I(60, hop=3, tail=-1),
        I(70, hop=4, tail=1), I(60, hop=3, tail=1), I(50, hop=2), I(50, hop=1), I(70, bob=2, eyes="shut", tail=-1),
        I(70, bob=1, eyes="half", tail=-2), I(80, tail=-1), I(80, tail=1), I(100),
    ],
    "action": [
        I(80, bob=1), I(70, lift=1), I(70, lift=2), I(80, lift=3, tail=-1), I(90, lift=3, eyes="half", tail=-1),
        I(60, lift=3, flash=True), I(110, lift=3, check=True, eyes="shut"), I(110, lift=3, check=True, eyes="shut", bob=1),
        I(110, lift=3, check=True), I(90, lift=3, check=True, tail=1), I(80, lift=2, check=True, tail=1),
        I(70, lift=1, check=True), I(80, check=True), I(100, check=True),
    ],
}


def main():
    cols = max(len(v) for v in ANIMS.values())
    sheet = Image.new("RGBA", (SIZE * cols, SIZE * len(ANIMS)), (0, 0, 0, 0))
    manifest = {"frame": {"w": SIZE, "h": SIZE}, "anchor": {"x": 32, "y": 60}, "animations": {}}
    for r, (name, frames) in enumerate(ANIMS.items()):
        for c, (im, _) in enumerate(frames):
            sheet.paste(im, (c * SIZE, r * SIZE))
        anim = {"row": r, "loop": name == "idle", "frames": [{"ms": ms} for _, ms in frames]}
        if name != "idle":
            anim["next"] = "idle"
        manifest["animations"][name] = anim
    used = {px for px in sheet.get_flattened_data() if px[3]}
    assert len(used) <= 15, f"{len(used)} colours"
    OUT.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT / "sheet.png")
    (OUT / "sheet.json").write_text(json.dumps(manifest, indent=2) + "\n")

    REVIEW.mkdir(parents=True, exist_ok=True)
    ref = Image.open(ROOT / "src/assets/mascots/resumon.png").convert("RGBA")
    ref.thumbnail((SIZE * 6, SIZE * 6))
    key = Image.new("RGBA", (SIZE * 6 * 3, SIZE * 6), (56, 136, 208, 255))
    key.paste((200, 176, 120, 255), (SIZE * 6, 0, SIZE * 12, SIZE * 6))
    key.paste((232, 232, 232, 255), (SIZE * 12, 0, SIZE * 18, SIZE * 6))
    big = frame().resize((SIZE * 6, SIZE * 6), Image.NEAREST)
    key.alpha_composite(big, (0, 0))
    key.alpha_composite(big, (SIZE * 6, 0))
    key.alpha_composite(ref, (SIZE * 12 + (SIZE * 6 - ref.width) // 2, (SIZE * 6 - ref.height) // 2))
    key.save(REVIEW / "hand-key@6x.png")
    print(f"OK resumon (hand): sheet {sheet.width}x{sheet.height}, {len(used)} colours, "
          + ", ".join(f"{k}={len(v)}f/{sum(ms for _, ms in v)}ms" for k, v in ANIMS.items()))


if __name__ == "__main__":
    main()
