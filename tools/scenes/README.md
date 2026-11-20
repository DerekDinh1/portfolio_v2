# Battle-scene generator

Rebuild every habitat (assets, review artefacts, then validation):

    tools/.venv/bin/python tools/scenes/build.py            # or: build.py water

Writes `src/assets/scenes/<habitat>/` (layer PNGs, platforms, `scene.json`) and
`generated/review/scenes/<habitat>/` (`day@4x.png`, `night@4x.png`, `*-tiling.png`, `*.gif`).
Validate alone: `tools/.venv/bin/python tools/scenes/validate.py [habitat]`.

## Layout

- `common.py`: palette ramps (`ramp3`, `q15`), role canvases, banded gradients, checker dither,
  stepped profiles, seamless value noise, seam/colour checks.
- `habitats/<name>.py`: one module per habitat with `NAME`, `PLATFORM`, `build(variant)`. Art is drawn
  into role-indexed canvases, so day/night share geometry and differ by palette (plus night extras).
- `habitats/__init__.py`: registry. To add `fire` or `grass`, copy the shape of `water.py`, import it here.
- `review.py`: composites with text-box / info-panel / creature overlays, tiling test, GIF.
- `validate.py`: checks the Scene contract in `docs/art-bible.md`.
