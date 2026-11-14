# Sprite pipeline

Rebuild everything (sheet.png, sheet.json, review contact sheet, GIFs, strips) and validate:

    tools/.venv/bin/python tools/sprites/build.py resumon && tools/.venv/bin/python tools/sprites/strip.py resumon && tools/.venv/bin/python tools/sprites/validate.py resumon

Method (no Blender): traced base plus hand-stamped details.
- `base.py`: BOX-downscales the reference still (`REF`, `HEIGHT` per character), classifies pixels into materials, keeps only the material (light tone) from the trace and cleans speckle; `pixel.py` then cel-lights it (4 tones per material, top-left key light, cast shadows).
- `characters/<slug>.py`: palette, ramps, the erase/stamp edits on the base, part-wise `render(pose)` and `ANIMS`. Add `buildasaur.py` / `vibeon.py` the same way (own REF, HEIGHT, regions).
- `pixel.py`: masks, 3-tone parts with rim, crouch/hop, re-outline.
- `build.py` (sheet, JSON, review), `strip.py` (4x strip PNG per animation), `validate.py` (art-bible contract).
