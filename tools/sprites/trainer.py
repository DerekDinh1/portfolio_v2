"""Trainer (Derek) overworld sprite, hand-authored pixel by pixel.

GBA-era overworld conventions: 16x32 frames, the figure about 22px tall standing
on the bottom edge, 15 colours + transparent, three frames per walking direction.
Every glyph below is one pixel; edit the grids, then run:

    tools/.venv/bin/python tools/sprites/trainer.py
"""
import json
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "src/assets/sprites/trainer"
REVIEW = ROOT / "generated/review/sprites/trainer"

PALETTE = {
    ".": (0, 0, 0, 0),
    "K": (24, 24, 32, 255),     # outline
    "k": (48, 48, 64, 255),     # hair
    "h": (88, 96, 120, 255),    # hair highlight
    "S": (232, 176, 120, 255),  # skin
    "s": (192, 128, 80, 255),   # skin shadow
    "T": (48, 160, 160, 255),   # hoodie
    "t": (32, 112, 120, 255),   # hoodie shadow
    "U": (112, 208, 200, 255),  # hoodie highlight
    "W": (248, 248, 248, 255),  # tee, shoes, lens glint
    "w": (176, 184, 200, 255),  # white shadow, headphones
    "P": (64, 72, 104, 255),    # trousers
    "p": (40, 48, 72, 255),     # trousers shadow
    "B": (216, 96, 48, 255),    # backpack
    "b": (160, 64, 32, 255),    # backpack shadow
    "d": (16, 72, 88, 255),     # hoodie outline
}

W, H, TOP = 16, 32, 10  # figure rows start at y=10 and end on y=31

HEAD_F = [
    "....K..K..KK....",
    "...KhKKhKKkkK...",
    "..KkhkkhhkkkkK..",
    "..KkhhhkkkkkkK..",
    "..KkhkkkkkkkkK..",
    "..KkSkkSkkSSkK..",
    "..KSSSSSSSSSSK..",
    "..KSKKKSSKKKSK..",
    "..KSWKWKKWKWSK..",
    "..KsSSSSSSSSsK..",
    "...KsSSssSSsK...",
    "....KKssssKK....",
]

HEAD_F_BLINK = HEAD_F[:8] + ["..KSWsWKKWsWSK.."] + HEAD_F[9:]

BODY_F = [
    "...KwtWWWWtwK...",
    "..dTTBTWWTBTTd..",
    ".dTUTBTTTTBTTtd.",
    ".KSSdBTTTTBdSSK.",
    "..KKdtTTTTtdKK..",
]

LEGS_STAND = [
    "....KPPPPPPK....",
    "....KPPpPPpK....",
    "....KPPKKPpK....",
    "....KWWKKWwK....",
    "....KKK..KKK....",
]

LEGS_A = [
    "....KPPPPPPK....",
    "....KPPpPPpK....",
    "....KPPKKPpK....",
    "....KWWKKKKK....",
    "....KKKK........",
]

LEGS_B = [
    "....KPPPPPPK....",
    "....KPPpPPpK....",
    "....KPPKKPpK....",
    "....KKKKKWwK....",
    "........KKKK....",
]

HEAD_U = [
    "....K..K..KK....",
    "...KhKKhKKkkK...",
    "..KkhkkhhkkkkK..",
    "..KkhhhkkkkkkK..",
    "..KkhkkkkkkkkK..",
    "..KkkkkkkkkkkK..",
    "..KkkkkkkkkkkK..",
    "..KkkkkkkkkkkK..",
    "..KSkkkkkkkkSK..",
    "..KsSkkkkkkSsK..",
    "...KsSkkkkSsK...",
    "....KKssssKK....",
]
BODY_U = [
    "...KwtTTTTtwK...",
    "..dTTKKKKKKTTd..",
    ".dTUKBBBBBBKTtd.",
    ".KSSKBbBBBbKSSK.",
    "..KKKbbbbbbKKK..",
]

LEGS_U = [LEGS_STAND, LEGS_A, LEGS_B]

HEAD_L = [
    "....K..K..K.....",
    "...KhKKhKKkKK...",
    "..KkhkkhkkkkkK..",
    "..KkkhhkkkkkkK..",
    "..KkkkkkkkkkkK..",
    "..KSSkSkkkkkkK..",
    "..KSSSSkkkkkkK..",
    "..KKKKKKSkkkkK..",
    ".KSKWSSSSskkK...",
    "..KSSSSSSSsK....",
    "..KsSSSSSsK.....",
    "...KKsssKK......",
]

BODY_L = [
    "....KtTTTwKK....",
    "...dTTTTTTKBK...",
    "...dTUTTTTKBBK..",
    "...dTKSSKtKBbK..",
    "....KKKKTtKKK...",
]

LEGS_L_STAND = [
    "....KPPPPPK.....",
    "....KPPpPPK.....",
    "....KPPpPPK.....",
    "...KWWWKWWK.....",
    "...KKKKKKKK.....",
]

LEGS_L_A = [
    "....KPPPPPK.....",
    "....KPPpPPK.....",
    "...KPPKKPPK.....",
    "..KWWK..KWWK....",
    "..KKKK..KKKK....",
]

LEGS_L_B = [
    "....KPPPPPK.....",
    "....KPPpPPK.....",
    "....KPPpPPK.....",
    "....KWWWKK......",
    "....KKKKK.......",
]

WAVE_1 = HEAD_F[:10] + [
    "...KsSSssSSsKKK.",
    "....KKssssKKSSK.",
    "...KwtWWWWtwKTd.",
    "..dTTBTWWTBTTTd.",
    ".dTUTBTTTTBTTd..",
    ".KSSdBTTTTBTd...",
    "..KKdtTTTTtd....",
] + LEGS_STAND

WAVE_2 = HEAD_F[:10] + [
    "...KsSSssSSsK.KK",
    "....KKssssKKKSSK",
    "...KwtWWWWtwKTd.",
    "..dTTBTWWTBTTTd.",
    ".dTUTBTTTTBTTd..",
    ".KSSdBTTTTBTd...",
    "..KKdtTTTTtd....",
] + LEGS_STAND

FRAMES = {
    "down": [HEAD_F + BODY_F + LEGS_STAND, HEAD_F + BODY_F + LEGS_A, HEAD_F + BODY_F + LEGS_B,
             HEAD_F_BLINK + BODY_F + LEGS_STAND],
    "up": [HEAD_U + BODY_U + legs for legs in LEGS_U],
    "left": [HEAD_L + BODY_L + LEGS_L_STAND, HEAD_L + BODY_L + LEGS_L_A, HEAD_L + BODY_L + LEGS_L_B],
    "interact": [WAVE_1, WAVE_2],
}
FRAMES["right"] = [[row[::-1] for row in f] for f in FRAMES["left"]]
ROWS = ["down", "up", "left", "right", "interact"]


def draw(grid):
    assert len(grid) == H - TOP, f"{len(grid)} rows"
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        assert len(row) == W, f"row {y} is {len(row)} wide: {row!r}"
        for x, ch in enumerate(row):
            im.putpixel((x, TOP + y), PALETTE[ch])
    return im


def main():
    cols = max(len(FRAMES[r]) for r in ROWS)
    sheet = Image.new("RGBA", (W * cols, H * len(ROWS)), (0, 0, 0, 0))
    for r, name in enumerate(ROWS):
        for c, grid in enumerate(FRAMES[name]):
            sheet.paste(draw(grid), (c * W, r * H))
    OUT.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT / "sheet.png")

    walk = lambda row: {"row": row, "loop": True, "order": [1, 0, 2, 0], "frames": [{"ms": 130}] * 3}
    manifest = {
        "frame": {"w": W, "h": H},
        "anchor": {"x": 8, "y": 31},
        "animations": {
            "idle": {"row": 0, "loop": True, "order": [0, 0, 0, 3], "frames": [{"ms": 900}] * 3 + [{"ms": 120}]},
            "walk-down": walk(0), "walk-up": walk(1), "walk-left": walk(2), "walk-right": walk(3),
            "interact": {"row": 4, "loop": False, "next": "idle", "order": [0, 1, 0, 1, 0, 1],
                         "frames": [{"ms": 140}] * 2},
        },
    }
    (OUT / "sheet.json").write_text(json.dumps(manifest, indent=2) + "\n")

    used = {px for px in sheet.get_flattened_data() if px[3]}
    assert len(used) <= 15, f"{len(used)} colours"

    REVIEW.mkdir(parents=True, exist_ok=True)
    scale = 8
    review = Image.new("RGBA", (sheet.width, sheet.height * 2), (104, 184, 96, 255))
    review.paste((224, 216, 184, 255), (0, sheet.height, sheet.width, sheet.height * 2))
    review.alpha_composite(sheet, (0, 0))
    review.alpha_composite(sheet, (0, sheet.height))
    review.resize((review.width * scale, review.height * scale), Image.NEAREST).save(REVIEW / "contact-sheet@8x.png")
    print(f"OK trainer: sheet {sheet.width}x{sheet.height}, {len(used)} colours")


if __name__ == "__main__":
    main()
