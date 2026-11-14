"""Buildasaur front sprite: the original mascot design redrawn as a 64x64 GBA-style sprite.

The pose, proportions and props come from `src/assets/mascots/buildasaur.png` (traced
to a 56px-tall grid as a guide), then every row was redrawn by hand in a fixed
12-colour palette with clean outlines and hard-edged tones.

Each row is "y x0 pixels": one glyph per pixel, "." for transparent. Groups are
stacked back to front and moved in whole pixels to animate.

    tools/.venv/bin/python tools/sprites/buildasaur_hand.py
"""
import json
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "src/assets/sprites/buildasaur"
REVIEW = ROOT / "generated/review/sprites/buildasaur"
SIZE = 64
DY = 2  # rows below are numbered from the trace grid; the feet land on y=60

PALETTE = {
    "K": (72, 24, 16),      # outline, pupil
    "O": (248, 136, 32),    # orange
    "o": (216, 88, 16),     # orange shadow, spikes, belt
    "R": (168, 48, 16),     # deep shadow, far limbs, iris
    "L": (248, 184, 88),    # orange highlight, cheek
    "Y": (248, 232, 128),   # belly, flame core, claws
    "y": (232, 184, 80),    # belly shadow
    "M": (112, 24, 32),     # mouth
    "T": (240, 120, 120),   # tongue
    "W": (248, 248, 248),   # teeth, eye shine
    "G": (184, 192, 208),   # wrench
    "g": (112, 120, 144),   # wrench shadow, buckle
}


def rows(spec):
    out = []
    for line in spec.strip().splitlines():
        y, x0, pix = line.split()
        out.append((int(y), int(x0), pix))
    return out


HEAD = rows("""
3 32 KK
4 30 KKoK
5 28 KKooK
6 27 KoOooK.KKK
7 26 KoOLoooKKoooK
8 25 KoOLYoooooOooK
9 24 KoOLYYLooOLYOooK
10 24 KoLYYYYYLOLYYLoK..KKK
11 21 KKKKoLYYYYLOoKKKKoK.KooK
12 18 KKKLLLKOLYYYLKKKLLLLKKKoooK
13 16 KKLLLLOOOOLYLOOOOOOOOOOOOKooK
14 15 KLLOOOOOOOOLLOOOOOOOOOOOOOKooK
15 14 KLOOOOOOOOOOOOOOOOOKKKKOOOOOKoK
16 13 KLOOOOOOOOOOOOOOOOOKWWKKKOOOOKoKK
17 13 KLOOOOOOOOOOOOOOOOKKWWKKWKOOOOKoooK
18 12 KOOOKOOOKOOOOOOOOOOKKKKKKWKOoOOKooooK
19 12 KOOOKOOOKOOOOOOOOOOKKKKKKWKOOoOKoooRK
20 12 KOOOOOOOOOOOOOOOOOOKKRRRKWKoOOOKoRRK
21 13 KOOOOOOOOOOOOOOOOOOKRRRWKOOoOOKRK
22 13 KooooOOOOOOOOOOOOOOOKKKKOOOOOOKoKK
23 14 KoooooOOOOOOOOOOOOKKOOLLLOOOKoooK
24 15 KKoooooooooooooKKWWKLLLLLOOKooooK
25 17 KKKKooooooKKKWWMWKLLLLLOOKRRRK
26 18 KWWKKKKKKWWMWWMMYYLLLYOKRRK
27 19 KWMWWWMWWWMWMMYYYYYYYOKK
28 20 KMMWMMMWMMMMMYYYYYYOKK
29 20 KMMTTTTTTTTMYYYYYooKoK
30 21 KMTTTTTTTTYYYYooKKooK
31 22 KYYTTTTTYYYYoooKKKKK
32 23 KKyYYYYYKKK
33 25 KKKKKK
""")
# Crest flicker: the inner flame tongues swap sides.
CREST_B = rows("""
7 29 o
8 29 o
8 31 Y
9 27 o
9 31 Y
9 34 o
9 36 Y
""")
EYES_HALF = rows("""
15 33 OOOO
16 32 OOOOOO
17 31 OOOOOOOO
18 31 KKKKKKKK
""")
EYES_SHUT = rows("""
15 33 OOOO
16 32 OOOOOO
17 31 OOOOOOOO
18 31 OOOOOOOO
19 31 KOOOOOOK
20 31 OKKKKKKO
21 32 OOOOOO
22 33 OOOO
""")

BODY = rows("""
32 34 oooK
33 24 KOOOOOOOOOOOOoK
34 24 KOOYYYYYYOOOOoKKKK
35 24 KyYYYYYYYOOOOooKooK
36 24 KyYYYYYKKKOOOOooKoK
37 24 KyyYYKKOOOOOOOOoKKK
38 24 KyYYKOOOOLOOOOoooK
39 24 KyYYKOOOOOOOOoKooK
40 24 KyyYKOOKOKOooKoooK
41 24 KyYYYKOKOKoKKKKKKK
42 23 KKKyYYKKKKKKKYYYYYYK
43 23 KooKKKooGGooKYYYgYYK
44 23 KRRoooooGGoRKyyyyyyK
45 23 KKKRRRRRggRKKKKKKKKK
46 23 KRRKKKKKKKKYKOOOOOoK
47 22 KRRRyYYYYYYYYKOOOOooK
48 21 KRoRRyYYYYYYYYKooooooK
49 20 KRooRRRyYYYYYYKOKKKKKKoo
50 20 KRRRRRRRyYYYYYKOOLOOoooo
51 20 KRRRRRRRRRyYYYKOLOOOoooo
52 21 KRRRRRRRRRKKKKOOOOoooooK
53 22 KRRRRRRRRK...KOOOOoooooK
54 22 KRRRRRRRK....KOOOOOooooK
55 20 KKRRRRRRRRK...KOOOOOOOoooK
56 19 KYYKYYKRRRRK..KYYoYYoYYOOooK
57 20 KK.KK.KKKK...KYYKYYKYYOoooK
58 34 KK.KK.KKKKKK
""")

# Near arm and the wrench it holds.
ARM = rows("""
28 13 KKK
29 10 K..KGK
30 9 KK..KGGK
31 9 KWK.KGGK
32 9 KGGKWGGK
33 9 KgGGGGGK
34 10 KggGGGK
35 12 KKGGKKKK..KK
36 13 KGgKOOOKKRRK
37 14 KgKOOORRRRK
38 13 KOOOKRRRRRoK
39 13 KOOoKRRRRooK
40 13 KOOoKRRoooK
41 14 KoooGgKKKK
42 15 KKKGgK
43 17 KGGGK
44 17 KG.gK
45 17 KgggK
46 18 KKK
""")
SPARK = rows("""
22 11 W
23 11 W
24 9 WWYWW
25 11 W
26 11 W
23 13 Y
25 9 Y
""")

TAIL = rows("""
33 52 KK
34 52 KOK
35 52 KOOK
36 52 KOOYK
37 52 KoOYK
38 50 KKoOOYK
39 49 KoooOOOYK
40 50 KooOOOYK
41 42 KK..K..KooOOOOYK
42 43 oKKoKKoooOOOOYK
43 43 oooooooooOOOOYK
44 43 oooooOOOOOOOYK
45 43 ooooOOoOOOOOYK
46 43 ooooOOOOoOYYK
47 43 ooooOoOOOYYK
48 43 oooOOOOYYYK
49 43 ooOOOYYYYK
50 44 oOYYYYKK
51 44 oyYKKK
52 45 KK
""")
FLAMES = [
    rows("""
26 52 o
27 52 oo
28 52 oOo
29 51 oOLOo
30 50 oOLYLo
31 50 oOLYYOo
32 50 oOOLYOo
33 50 ooOO
34 50 .oO
35 51 o
"""),
    rows("""
27 54 o
28 53 oo
29 52 oOLo
30 51 oOLLOo
31 50 oOLYYOo
32 50 oOLYYLo
33 50 oOOO
34 50 ooO
35 51 o
"""),
    rows("""
25 53 o
27 53 o
28 52 oOo
29 52 oLOo
30 51 oOYLOo
31 51 oLYYOo
32 50 oOOYLOo
33 50 .oOO
34 50 ooO
35 50 o
"""),
]


def stamp(im, layer, dx=0, dy=0):
    for y, x0, pix in layer:
        for i, ch in enumerate(pix):
            x, yy = x0 + i + dx, y + dy + DY
            if ch != "." and 0 <= x < SIZE and 0 <= yy < SIZE:
                im.putpixel((x, yy), PALETTE[ch] + (255,))


def frame(bob=0, flame=0, crest=0, eyes="open", lift=0, hop=0, spark=False):
    """bob: head down px. flame: tail flame frame. lift: wrench arm up px. hop: whole sprite up px."""
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    stamp(im, FLAMES[flame], dy=-hop)
    stamp(im, TAIL, dy=-hop)
    stamp(im, BODY, dy=-hop)
    stamp(im, HEAD, dy=bob - hop)
    if crest:
        stamp(im, CREST_B, dy=bob - hop)
    if eyes == "half":
        stamp(im, EYES_HALF, dy=bob - hop)
    elif eyes == "shut":
        stamp(im, EYES_SHUT, dy=bob - hop)
    stamp(im, ARM, dy=-lift - hop)
    if spark:
        stamp(im, SPARK, dy=-lift - hop)
    return im


I = lambda ms, **kw: (frame(**kw), ms)
ANIMS = {
    "idle": [
        I(180), I(180, flame=1, crest=1), I(180, flame=2, bob=1), I(180, flame=1, bob=1, crest=1),
        I(180, bob=1), I(180, flame=1, crest=1), I(180, flame=2), I(180, flame=1, crest=1),
        I(70, eyes="half"), I(90, eyes="shut", flame=1), I(70, eyes="half", flame=2, crest=1), I(180, flame=1),
    ],
    "greet": [
        I(70, bob=1), I(80, bob=1, eyes="half", flame=1), I(50, hop=1, lift=1, flame=2), I(50, hop=2, lift=2, crest=1),
        I(60, hop=3, lift=3, flame=1), I(70, hop=4, lift=2, flame=2), I(60, hop=3, lift=3, crest=1), I(50, hop=2, lift=2, flame=1),
        I(50, hop=1, lift=1, flame=2), I(70, bob=1, eyes="shut"), I(70, bob=1, eyes="half", flame=1, crest=1),
        I(80, lift=1, flame=2), I(80, flame=1), I(100),
    ],
    "action": [
        I(80, bob=1), I(70, lift=1, flame=1), I(70, lift=2, flame=2, crest=1), I(80, lift=3, flame=1),
        I(90, lift=3, eyes="half", flame=2), I(60, lift=1, bob=1, crest=1), I(60, lift=0, bob=1, spark=True, eyes="shut"),
        I(110, lift=0, bob=1, spark=True, eyes="shut", flame=1), I(90, lift=1, flame=2), I(90, lift=2, flame=1, crest=1),
        I(80, lift=1, flame=2), I(70, bob=1, flame=1), I(80, crest=1), I(100),
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
    ref = Image.open(ROOT / "src/assets/mascots/buildasaur.png").convert("RGBA")
    ref.thumbnail((SIZE * 6, SIZE * 6))
    key = Image.new("RGBA", (SIZE * 6 * 3, SIZE * 6), (96, 152, 96, 255))
    key.paste((200, 176, 120, 255), (SIZE * 6, 0, SIZE * 12, SIZE * 6))
    key.paste((232, 232, 232, 255), (SIZE * 12, 0, SIZE * 18, SIZE * 6))
    big = frame().resize((SIZE * 6, SIZE * 6), Image.NEAREST)
    key.alpha_composite(big, (0, 0))
    key.alpha_composite(big, (SIZE * 6, 0))
    key.alpha_composite(ref, (SIZE * 12 + (SIZE * 6 - ref.width) // 2, (SIZE * 6 - ref.height) // 2))
    key.save(REVIEW / "hand-key@6x.png")
    print(f"OK buildasaur (hand): sheet {sheet.width}x{sheet.height}, {len(used)} colours, "
          + ", ".join(f"{k}={len(v)}f/{sum(ms for _, ms in v)}ms" for k, v in ANIMS.items()))


if __name__ == "__main__":
    main()
