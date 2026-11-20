"""Shared colour grade for every sprite palette.

The sprites and scenes were authored a touch brighter than the title art, so each palette
is passed through one gentle per-channel gamma on the way out: mid-tones deepen and gain a
little saturation, white and the outlines barely move. Sprites take a lighter grade than
the scenes (tools/scenes/common.py, DEEPEN) so they still stand clear of the backdrop.
"""
GRADE = 1.10


def grade(c, g=GRADE):
    """(r, g, b[, a]) -> the same colour graded, snapped to the 15-bit grid (multiples of 8)."""
    rgb = tuple(min(248, int(round(255 * (v / 255) ** g / 8)) * 8) for v in c[:3])
    return rgb + tuple(c[3:])


def grade_all(pal):
    return {k: grade(v) for k, v in pal.items()}
