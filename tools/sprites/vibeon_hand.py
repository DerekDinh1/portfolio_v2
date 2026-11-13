"""Vibeon front sprite: the original mascot design redrawn as a 64x64 GBA-style sprite.

The pose, proportions and props come from `src/assets/mascots/vibeon.png` (traced to a
57px-tall grid as a guide), then every row was redrawn by hand in a fixed 15-colour
palette with clean outlines and hard-edged tones.

Each row is "y x0 runs"; a run is a palette glyph plus a count ("G5" = five pixels,
"." = transparent). Groups are stacked back to front and moved in whole pixels to animate.

    tools/.venv/bin/python tools/sprites/vibeon_hand.py
"""
import json
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "src/assets/sprites/vibeon"
REVIEW = ROOT / "generated/review/sprites/vibeon"
SIZE = 64
DY = 1  # rows below are numbered from the trace grid; the feet land on y=60

PALETTE = {
    "K": (24, 56, 64),      # outline, pupils
    "G": (144, 216, 168),   # mint fur
    "g": (96, 184, 136),    # fur shadow
    "D": (32, 152, 128),    # teal: ear rims, paws, iris, headphone
    "d": (16, 104, 96),     # deep teal: ear backs, soles
    "E": (72, 200, 176),    # light teal: iris glow, headphone cup
    "C": (248, 240, 216),   # cream fur
    "c": (216, 208, 176),   # cream shadow
    "W": (248, 248, 248),   # eye shine, tufts, golf ball, controller
    "P": (248, 184, 168),   # blush
    "T": (240, 112, 112),   # tongue
    "R": (224, 56, 48),     # flag, mouth, controller button
    "H": (48, 48, 72),      # headphone cup
    "h": (112, 112, 144),   # headphone rim
    "Y": (176, 216, 72),    # pendant, putting green
}


def rows(spec):
    out = []
    for line in spec.strip().splitlines():
        y, x0, *runs = line.split()
        out.append((int(y), int(x0), "".join(tok[0] * int(tok[1:] or 1) for tok in runs)))
    return out


# Both eyes share one construction: shine top-left, pupil fading into a teal iris, lighter
# glow and a glint along the bottom.
HEAD = rows("""
3 18 K2
4 17 K d2 K .25 K2
5 17 K d3 K2 .21 K2 d2 K
6 16 K d6 K .19 K d5 K
7 16 K d C2 d4 K .17 K d6 K
8 16 K d C3 d3 g K .4 K .9 K2 d3 c3 d2 K
9 15 K d C4 d2 g2 K .3 K G K . K .5 K G2 d2 c4 d2 K
10 15 K D C5 d g3 K . K G3 K G K .3 K G4 d c5 d K
11 15 K G C5 g5 K G7 K3 G5 c C4 d2 K
12 15 K G C6 g3 G16 c C4 c d K
13 16 K G C5 g2 G16 C3 c3 g d K
14 16 K G W3 C2 G17 C5 c2 g K
15 17 K G W2 C G18 W2 C2 c g3 K
16 17 K G2 W G20 W C2 c g2 K
17 16 K G8 C2 G7 C2 G9 g2 K
18 16 K G5 K4 G10 K4 G5 g2 K
19 16 K G4 K W2 K3 G8 K W2 K3 G4 g2 K
20 15 K G3 g G K W2 K3 G8 K W2 K3 G g G2 g2 K
21 15 K G2 g G2 K2 d3 K G8 K2 d3 K G2 g G2 g2 K
22 15 K G5 K d4 K G8 K d4 K G5 g2 K
23 14 K G6 K D4 K G3 K2 G3 K D4 K G5 g2 K
24 13 K G7 K E2 D W K C8 K E2 D W K G6 g2 K
25 14 K G2 C5 K4 C K C2 K2 C2 K C K4 C2 G4 g2 K
26 14 K C P3 C9 K2 R2 K2 C9 P3 G g2 K
27 13 K C2 P3 C9 K R4 K C9 P3 C G g2 K
28 14 K2 C12 K T4 K C13 g K2
29 15 K2 c2 C10 K T2 K C12 c2 K2
30 17 K2 c2 C9 K2 C11 c2 K2
31 19 K2 c2 C18 c2 K2
32 21 K3 c2 K3 c3 K4 c2 K5
33 24 K2 .3 K3 .4 K2
""")
EYES_HALF = rows("""
18 22 G4 .10 G4
19 21 G6 .8 G6
20 21 G6 .8 G6
21 21 K6 .8 K6
""")
# Happy closed eyes: two little arcs.
EYES_SHUT = rows("""
18 22 G4 .10 G4
19 21 G6 .8 G6
20 21 G6 .8 G6
21 21 G6 .8 G6
22 21 K G4 K .8 K G4 K
23 21 G K4 G .8 G K4 G
24 21 G6 .8 G6
25 22 C4 .10 C4
""")

BODY = rows("""
32 22 K4 .9 K4
33 21 K h H3 K C7 K E4 K
34 20 K W h H4 K K5 K H E W2 E2 K
35 20 K h H5 K E5 K H E5 K
36 19 K K h H5 K D5 K H E2 D3 K G3 K
37 18 K C2 K H4 K C K5 K H D5 K G4 K
38 18 K C3 K4 C8 K D4 K G5 K
39 17 K C9 K3 C5 K4 G7 K
40 18 K C7 K W3 K C6 Y g G7 K
41 18 K C7 K Y3 K C4 K5 G7 K
42 17 K C9 K3 C4 K W K W R W K G5 K
43 18 K G2 C13 K W2 K W2 K G6 K
44 18 K G3 C13 K2 C K2 G7 K
45 17 K G5 C14 G10 K
46 16 K G7 c C11 G12 K
47 15 K G8 c C10 G13 K
48 14 K G7 K G3 c2 C4 c2 G3 K G10 K
49 13 K G8 K G5 K c2 K G5 K G10 K
50 13 K K5 G3 K g5 K c2 K g5 K G10 K
51 13 K D5 K G2 K g5 K c2 K g5 K G4 K5 G K
52 12 K D d E d E d D K G K D5 K c2 K D5 K G3 K D5 K
53 12 K D d5 D K . K D4 d K c2 K D4 d K g2 K D d E d E d D K
54 12 K D d E3 d D K . K D4 d K c2 K D4 d K g2 K D d5 D K
55 12 K D d E3 d D K . K D4 d K c2 K D4 d K K2 K D d E3 d D K
56 12 K D d5 D K . K D K D K D K K2 K D K D K D K .2 K D d E3 d D K
57 13 K D5 K .2 K D K D K D K .2 K D K D K D K .2 K D d5 D K
58 14 K5 .4 K5 .4 K5 .4 K D5 K
59 42 K5
""")

TAIL = rows("""
29 53 K2
30 52 K C2 K
31 52 K C3 K
32 51 K C5 K
33 50 K C6 K
34 49 K C8 K
35 48 K C8 W K
36 46 K2 G2 C7 W K
37 45 K G4 C7 W c K
38 45 G6 C G2 C2 W2 c K
39 45 G9 C G W2 c2 K
40 45 G11 W c2 K
41 45 G11 c3 K
42 45 G4 g G6 c3 K
43 45 G11 c2 K
44 45 G5 g G5 c2 K
45 45 G10 g c2 K
46 45 G9 g2 c K
47 46 G8 g2 c K
48 46 G7 g3 K
49 47 G5 g3 K
50 48 G4 g3 K
51 48 G3 g3 K
52 49 G2 g3 K
53 49 g4 K
54 49 g3 K
55 49 g2 K
56 49 g K
57 48 K2
""")

# Golf flag, ball and a scrap of putting green.
PROPS = rows("""
41 9 K3
42 9 K R2 K2
43 9 K R4 K
44 9 K R2 K2
45 9 K3
46 9 K
47 9 K
48 9 K
49 9 K
50 9 K
51 9 K
52 9 K
53 5 K3 . K
54 4 K W3 K K
55 4 K W c W K K
56 5 K3 . K
57 3 K Y8 K
58 4 K8
""")
NOTE = rows("""
12 54 E2
13 54 E . E
14 54 E . E
15 54 E
16 52 E3
17 52 E3
""")


def stamp(im, layer, dx=0, dy=0):
    for y, x0, pix in layer:
        for i, ch in enumerate(pix):
            x, yy = x0 + i + dx, y + dy + DY
            if ch != "." and 0 <= x < SIZE and 0 <= yy < SIZE:
                im.putpixel((x, yy), PALETTE[ch] + (255,))


def frame(bob=0, tail=0, eyes="open", hop=0, note=None):
    """bob: head down px. tail: tail sideways px. hop: creature up px. note: music note rise px."""
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    stamp(im, PROPS)
    stamp(im, TAIL, dx=tail, dy=-hop)
    stamp(im, BODY, dy=-hop)
    stamp(im, HEAD, dy=bob - hop)
    if eyes == "half":
        stamp(im, EYES_HALF, dy=bob - hop)
    elif eyes == "shut":
        stamp(im, EYES_SHUT, dy=bob - hop)
    if note is not None:
        stamp(im, NOTE, dy=-note - hop)
    return im


I = lambda ms, **kw: (frame(**kw), ms)
ANIMS = {
    "idle": [
        I(220), I(200, tail=1), I(200, bob=1, tail=1), I(220, bob=1), I(200, bob=1, tail=-1), I(200, tail=-1),
        I(220), I(200, tail=1), I(70, eyes="half", tail=1), I(90, eyes="shut"), I(70, eyes="half"), I(220),
    ],
    "greet": [
        I(70, bob=1), I(70, bob=1, eyes="half", tail=1), I(50, hop=1, tail=-1, eyes="shut"), I(50, hop=2, tail=1, eyes="shut"),
        I(60, hop=3, tail=-1, eyes="shut"), I(70, hop=4, tail=1, eyes="shut"), I(60, hop=3, tail=-1, eyes="shut"),
        I(50, hop=2, tail=1, eyes="shut"), I(50, hop=1, tail=-1, eyes="shut"), I(70, bob=1, eyes="shut", tail=1),
        I(70, bob=1, eyes="half", tail=-1), I(80, tail=1), I(80, tail=-1), I(100),
    ],
    "action": [
        I(80, bob=1), I(80, bob=1, eyes="half"), I(80, note=0, tail=1), I(80, note=1, bob=1, tail=1),
        I(80, note=2, eyes="shut", tail=-1), I(80, note=3, eyes="shut", bob=1, tail=-1), I(80, note=4, eyes="shut", tail=1),
        I(80, note=5, eyes="shut", bob=1, tail=1), I(80, note=6, tail=-1), I(80, bob=1, tail=-1), I(80, tail=1),
        I(80, bob=1), I(80), I(100),
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
    ref = Image.open(ROOT / "src/assets/mascots/vibeon.png").convert("RGBA")
    ref.thumbnail((SIZE * 6, SIZE * 6))
    key = Image.new("RGBA", (SIZE * 6 * 3, SIZE * 6), (120, 176, 232, 255))
    key.paste((200, 176, 120, 255), (SIZE * 6, 0, SIZE * 12, SIZE * 6))
    key.paste((232, 232, 232, 255), (SIZE * 12, 0, SIZE * 18, SIZE * 6))
    big = frame().resize((SIZE * 6, SIZE * 6), Image.NEAREST)
    key.alpha_composite(big, (0, 0))
    key.alpha_composite(big, (SIZE * 6, 0))
    key.alpha_composite(ref, (SIZE * 12 + (SIZE * 6 - ref.width) // 2, (SIZE * 6 - ref.height) // 2))
    key.save(REVIEW / "hand-key@6x.png")
    print(f"OK vibeon (hand): sheet {sheet.width}x{sheet.height}, {len(used)} colours, "
          + ", ".join(f"{k}={len(v)}f/{sum(ms for _, ms in v)}ms" for k, v in ANIMS.items()))


if __name__ == "__main__":
    main()
