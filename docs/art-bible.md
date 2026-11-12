# Art bible: GBA-era overhaul

The contract every asset and component follows. If a rule here blocks you, report it; do not work around it.

## Look

Original art in the style of a 2004 handheld monster RPG (the user's reference is Pokémon Emerald). Style only: **no** Nintendo/Game Freak sprites, tiles, UI rips, fonts, names, logos or audio, and nothing traced from them. Creatures, scenes and UI are our own designs.

## Pixel rules (all shipped art)

- Native scene is **240×160**. Art is authored at native size, 1 art pixel = 1 file pixel.
- Colour is 15-bit: every R, G, B value is a multiple of 8. Alpha is 0 or 255 only.
- No anti-aliasing, blur, soft gradients or sub-pixel anything. Gradients are 3–6 flat bands; a 1px checker dither row between bands is allowed.
- Cel lighting: 4 flat tones per main material (highlight, light, base, shadow) with hard edges between them, hue-shifted: shadows lean blue/violet, highlights lean yellow. One key light from the top-left (the sun by day, the moon by night). Use it to build form: a core shadow on the side away from the light, cast shadows where one part overlaps another (head on torso, arm on belly, prop on body, tree on ground), a thin rim light on the shadow-side edge, and small specular highlights on wet or shiny surfaces. Everything standing on the ground gets a contact shadow.
- Sprites carry a 1px outline in a dark shade of the local colour (never pure black; darkest allowed is `#181820`).
- No isolated single pixels ("orphans") unless they are deliberate highlights.
- Sprites: at most 24 colours plus transparent. A scene variant (all its layers): at most 64 colours.
- PNG only, no JPEG. Files are small; do not add compression tooling.

## Display rules (runtime)

- Scale is an integer number of **device** pixels per art pixel: `scale = floor(cssWidth * devicePixelRatio / 240) / devicePixelRatio`, capped so the scene is at most 62vh tall. Always `image-rendering: pixelated`.
- One CSS variable, `--px`, holds the CSS size of one art pixel. Every game-UI dimension is `calc(var(--px) * n)`.
- Animation is stepped (held frames), never tweened. Scroll/drift moves in whole art pixels.
- `prefers-reduced-motion`: show frame 0, no drift, no typewriter.

## Battle-scene hero (240×160 safe area)

Full-bleed band; background layers repeat horizontally, and the 240-wide safe area is centred in it.

| Region | Native rect (x, y, w, h) | Content |
| --- | --- | --- |
| Backdrop | 0, 0, 240, 112 | Habitat layers |
| Platform | centred at (176, 80), about 96×24 | Oval terrain patch the creature stands on |
| Creature | 64×64, feet at (176, 80) | Front sprite, faces slightly left |
| Info panel | 12, 16, 104, 34 | Name, type badge, level, one stat bar, status tag |
| Text box | 0, 112, 240, 48 | Message line(s) left, 2×2 menu right |

Keep points of interest above y=112; the text box covers everything below.

## Sprite contract

Path: `src/assets/sprites/<slug>/sheet.png` and `sheet.json` (slug: `resumon`, `buildasaur`, `vibeon`).

- Frames are 64×64. Feet baseline at y=60, body centred on x=32, 2px clear margin on all sides. Hop frames may rise into the top margin.
- Sprites are hand-authored as pixel grids (see `tools/sprites/resumon_hand.py`, `tools/sprites/trainer.py`), not generated from shapes or downscaled art.
- One row per animation, frames left to right. Unused cells are fully transparent.
- Frames are still stepped (no tweening at runtime), but motion is drawn with enough in-betweens to read as smooth: parts move 1px per frame, with ease-in and ease-out spacing, overlap and follow-through (the tail and fins lag the body by a frame or two).

```json
{
  "frame": { "w": 64, "h": 64 },
  "anchor": { "x": 32, "y": 60 },
  "animations": {
    "idle":   { "row": 0, "loop": true,  "frames": [{ "ms": 480 }, { "ms": 480 }] },
    "greet":  { "row": 1, "loop": false, "next": "idle", "frames": [{ "ms": 90 }] },
    "action": { "row": 2, "loop": false, "next": "idle", "frames": [{ "ms": 110 }] }
  }
}
```

- `idle`: 12–16 frames, 2.4–3.6s loop. Breathing as a 1px bob with a chest swell, a 3-frame blink (half, closed, half), and a secondary motion that eases through its arc (tail, fin, flame).
- `greet`: 14–18 frames. Anticipation squash, hop with a proper arc, a full wave cycle, landing squash and settle.
- `action`: 14–18 frames. The creature uses its prop, with anticipation and a settle back to the idle pose.

### Characters (identities are fixed; redraw, do not redesign)

- **Resumon** (water, `/professional`): the original mascot, unchanged in design: a teal axolotl-shark pup standing upright in a 3/4 view facing left. Dorsal fin on the head, frilled gill-fins at the cheeks, pale muzzle and belly, peach blush, navy collar and tie, a grey clipboard held in both paws, navy shark tail. Calm and dutiful. Action: lifts the clipboard and ticks it. (No water drop above the head: removed at the user's request.)
- **Buildasaur** (fire, `/projects`): orange dino, yellow belly, flame crest and flame tail tip, tool belt with pouch, steel wrench in the right hand, open grin. Eager. Action: spins the wrench.
- **Vibeon** (grass, `/personal`): mint fox, cream chest and tail tip, dark green paws and ear tips, headphones round the neck, small controller charm. Sits. Relaxed. Action: puts the headphones on and nods.

Reference stills (old style, for identity only): `src/assets/mascots/*.png`.

## Scene contract

Path: `src/assets/scenes/<habitat>/` (habitat: `water`, `fire`, `grass`, later `title`, `lab`).

- Every layer PNG is 160px tall per frame and 240 or 480px wide, and tiles seamlessly left-to-right.
- Animated layers stack frames vertically (file height = 160 × frames).
- `drift` is horizontal scroll in art pixels per second (negative moves left). 0 for static layers.
- Layers are listed back to front. `day` and `night` variants share geometry; night is a palette re-ramp plus extras (stars, glow).

```json
{
  "size": { "w": 240, "h": 160 },
  "platform": { "file": "platform.png", "w": 96, "h": 24, "cx": 176, "cy": 80 },
  "variants": {
    "day":   { "layers": [ { "file": "day/00-sky.png", "w": 240, "drift": 0 },
                           { "file": "day/10-clouds.png", "w": 480, "drift": -2 },
                           { "file": "day/30-water.png", "w": 240, "frames": 8, "fps": 8, "drift": 0 } ],
               "platform": "day/platform.png" },
    "night": { "layers": [], "platform": "night/platform.png" }
  }
}
```

### Landscape conventions

Borrow the conventions of GBA-era monster-RPG landscapes; do not copy or trace any specific scene, tile or sprite from those games.

- High-key, saturated palette: clean sky blues, vivid greens, warm sand. Nothing muddy or grey by day.
- Simple, readable masses over fine detail. Each element is one bold shape with 3–4 cel tones and a dark base line.
- Trees are rounded, bushy clumps built from overlapping lobes, lit top-left with a dark underside, not thin realistic spikes. Conifers are stacked rounded tiers.
- Clouds are puffy stacks of round lobes with a flat, shaded underside.
- Mountains are stepped, chunky forms with a clear lit face and shadow face and ledge lines, not smooth triangles.
- Water is drawn with a repeating wave motif (short curved crests in rows that shift each frame) and sparkle clusters, with a white foam line where it meets land.
- Ground under the creature is an oval platform with a lighter rim, texture tufts or pebbles at the edge, and a contact shadow.
- A soft band of lighter colour at the horizon separates sky from land (atmospheric perspective in flat bands).

### Habitats

- **water**: alpine lake under Colorado front-range peaks; pine shoreline left, weathered dock, banded water with moving highlight rows. Platform: wet-sand oval with a ripple ring. Night: moon, twinkling stars, moon path on the water.
- **fire**: forge clearing; anvil, workbench, ember glow, drifting sparks. Platform: scorched packed earth.
- **grass**: forest trail at the foothills; ferns, dappled light, drifting leaves, fireflies at night. Platform: mossy turf.

## Game UI

- Font: `var(--pixel)` (Silkscreen, already loaded). Text sits on the art-pixel grid.
- Panels are our own design: cream fill `#F8F8E8`, 1px inner line `#B8B8A0`, 2px outer frame `#404858`, 1px drop edge. Night uses `#283048` fill with `#98A8C8` lines.
- Type colours: water `#3890D8`, fire `#E86830`, grass `#58A848`.
- Starter select (later phase) uses three original typed capsules, one per starter in its type colour. Not a red-and-white ball, and not called a Poké Ball.

## Review artefacts

Write previews for the director to `generated/review/<kind>/<name>/` (git-ignored): a 4× nearest-neighbour contact sheet PNG and, where useful, a 4× GIF per animation.
