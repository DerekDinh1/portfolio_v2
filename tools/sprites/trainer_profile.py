"""Trainer (Derek) profile artwork: 64x64, hand-authored, same palette as the overworld sprite.

Each entry is (x offset, pixels); every glyph is one pixel. Rebuild with:

    tools/.venv/bin/python tools/sprites/trainer_profile.py
"""
import pathlib

from PIL import Image

from trainer import PALETTE

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "src/assets/sprites/trainer"
REVIEW = ROOT / "generated/review/sprites/trainer"

SIZE, LEFT, FEET = 64, 12, 60

ARM_L, ARM_R = "TTUTTT", "TTTTtt"
ROWS = [
    # hair
    (13, "K......K.....K"),
    (12, "KhK....KhK...KkK"),
    (11, "KhhkKKKhhhkKKkkkkK"),
    (10, "KhhkkkkhhhkkkkkkkkkK"),
    (10, "KhkkkkkhhkkkkkkkkkkK"),
    (10, "KkkkkkkkkkkkkkkkkkkK"),
    (10, "KkkkSkkkSSkkkSkkkkkK"),
    (10, "KkkSSSkSSSSkSSSSkkkK"),
    (10, "KkSSSSSSSSSSSSSSSSkK"),
    (10, "KkSSSSSSSSSSSSSSSSkK"),
    # glasses
    (9, "KKSKKKKKKSSSSKKKKKKSKK"),
    (8, "KsKSKWWWWKKKKKKWWWWKSKsK"),
    (8, "KsKSKWKKWKSSSSKWKKWKSKsK"),
    (8, "KsKSKWKKWKSSSSKWKKWKSKsK"),
    (9, "KKSKKKKKKSSSSKKKKKKSKK"),
    # lower face
    (10, "KSSSSSSSSssSSSSSSSSK"),
    (10, "KsSSSSSSSSSSSSSSSSsK"),
    (11, "KsSSSKSSSSSSKSSSsK"),
    (11, "KssSSSKKKKKKSSSssK"),
    (12, "KKssSSSSSSSSssKK"),
    (14, "KKKssssssKKK"),
    # neck and headphones
    (16, "KssssssK"),
    (13, "KwwKKssssKKwwK"),
    (10, "KKKwwKtWWWWWWtKwwKKK"),
    # shoulders
    (7, "KKTTTKKKTtWWWWWWtTKKKTTTKK"),
    (6, "KTUUTTTBBTTtWWWWtTTBBTTTTTtK"),
    (5, "KTUUTTTTBBTTTtWWtTTTBBTTTTTTtK"),
    (5, "KTUTTTTTBBTTTTddTTTTBBTTTTTTtK"),
    # arms and torso
    (4, "K" + ARM_L + "K" + "TBBTTTT" + "dd" + "TTTTBBT" + "K" + ARM_R + "K"),
    (4, "K" + ARM_L + "K" + "TBBTTTT" + "dd" + "TTTTBBT" + "K" + ARM_R + "K"),
    (4, "K" + ARM_L + "K" + "TBBTTTT" + "dd" + "TTTTBBt" + "K" + ARM_R + "K"),
    (4, "K" + ARM_L + "K" + "TTTTTTT" + "dd" + "TTTTTTt" + "K" + ARM_R + "K"),
    (4, "K" + ARM_L + "K" + "TTtttTT" + "dd" + "TTtttTt" + "K" + ARM_R + "K"),
    (4, "K" + "TTTTTT" + "K" + "TtTTTtT" + "dd" + "TtTTTtt" + "K" + "TTTttt" + "K"),
    (4, "K" + "tTTTTt" + "K" + "TtTTTtT" + "dd" + "TtTTTtt" + "K" + "tTTttt" + "K"),
    (4, "K" + "dddddd" + "K" + "TTTTTTT" + "dd" + "TTTTTtt" + "K" + "dddddd" + "K"),
    (4, "K" + "SSSSSs" + "K" + "dddddddddddddddd" + "K" + "SSSSss" + "K"),
    (4, "K" + "SSSSSs" + "K" + "PPPPPPPPPPPPPPPp" + "K" + "SSSSss" + "K"),
    (4, ".KKKKKK" + "K" + "PPPPPPPpPPPPPPPp" + "K" + "KKKKKK."),
    # legs
    (11, "K" + "PPPPPPPpPPPPPPPp" + "K"),
    (11, "K" + "PPPPPPPpPPPPPPPp" + "K"),
] + [(11, "K" + "PPPPPPp" + "KK" + "PPPPPPp" + "K")] * 10 + [
    (11, "K" + "PPPPPpp" + "KK" + "PPPPPpp" + "K"),
    (11, "K" + "ppppppp" + "KK" + "ppppppp" + "K"),
    # shoes
    (10, "K" + "WWWWWWWw" + "KK" + "WWWWWWWw" + "K"),
    (9, "K" + "WWWWWWWWw" + "KK" + "wWWWWWWWW" + "K"),
    (9, "K" + "wwwwwwwww" + "KK" + "wwwwwwwww" + "K"),
    (9, "K" * 22),
]


def main():
    top = FEET - len(ROWS) + 1
    assert top >= 0, f"{len(ROWS)} rows do not fit"
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for y, (off, row) in enumerate(ROWS):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((LEFT + off + x, top + y), PALETTE[ch])
    used = {px for px in im.get_flattened_data() if px[3]}
    assert len(used) <= 15, f"{len(used)} colours"
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / "profile.png")

    REVIEW.mkdir(parents=True, exist_ok=True)
    review = Image.new("RGBA", (SIZE * 2, SIZE), (104, 184, 96, 255))
    review.paste((224, 216, 184, 255), (SIZE, 0, SIZE * 2, SIZE))
    review.alpha_composite(im, (0, 0))
    review.alpha_composite(im, (SIZE, 0))
    review.resize((review.width * 6, review.height * 6), Image.NEAREST).save(REVIEW / "profile@6x.png")
    print(f"OK trainer profile: {len(ROWS)} rows, {len(used)} colours")


if __name__ == "__main__":
    main()
