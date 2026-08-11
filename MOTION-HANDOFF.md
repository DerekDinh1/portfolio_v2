# Handoff: Motion, Animations & Transitions

Paste this whole file into Cursor as the opening prompt. It is self-contained.

## Context

This is Derek Dinh's personal portfolio: a **Pokémon-game homage** built with **Vite + React 19 + react-router-dom**. The static build is done, committed, and pushed to `DerekDinh1/portfolio_v2` (private). Your job is the **motion phase** only. Do not redesign layout, rewrite copy, or change content/data. Add animation on top of what exists.

**Architecture** (everything is in two files):
- `src/main.jsx` — all components, routes, and data constants in one file.
- `src/index.css` — the full design system (tokens, theme classes, component styles).

Run it: `npm install` then `npm run dev` (Vite, default port 5173).

## How the site flows

1. **Home** (`/`) is a client-side scene machine in the `Home` component (`src/main.jsx`), state var `scene` = `"title" | "intro" | "select"`:
   - `TitleScreen` — pixel landscape bg, "Colorado Region", "DEREK DINH", a **"Press Start"** button (`.title-press`). `onStart` moves to `intro`.
   - **Intro dialogue** (`.intro-stage`) — a Professor-Dinh nameplate (`.nameplate`), one line of `INTRO[step]` in `.dialogue-text`, a blinking `.cursor` (▼), and controls: Next / Skip intro / (on last line) Choose a starter. A `.progress` list of dots tracks `step`.
   - `StarterSelect` (`.select-stage`) — three `.starter-card`s. Each starts `.closed` as a `.pokeball-btn` (CSS-drawn `.pokeball` + `.pokeball-hint` label). Clicking calls `reveal(slug)`, flipping that card to `.open` `theme-{water|fire|grass}`, which swaps in the mascot img, dex line, name, blurb, and a `Choose {name} →` Link to the page.
2. **Pages** (`/professional` Resumon/water, `/projects` Buildasaur/fire, `/personal` Vibeon/grass) each render `PageHero` (`.hero` with `.hero-orb` + mascot `img`) then content `.block`s, then the `Contact` footer. Per-page accent comes from a `theme-water|fire|grass` class on `<main className="page ...">`.

Theme classes set `--accent`, `--accent-ink`, `--accent-soft` CSS custom properties — use those for any animated accents so each page's motion stays on-theme.

## What to build (in priority order)

Ship these one at a time and verify each in the browser before moving on.

1. **PRESS START blink + enter.** Make `.title-press` pulse/blink like an arcade prompt. On click, do a short screen-wipe or fade before switching to the intro scene (the classic Pokémon flash works well). Respect that the scene swap is a React state change, so animate the exit of the title and the enter of the intro.

2. **Typewriter dialogue.** In the intro, render `INTRO[step]` character-by-character instead of all at once. First click of "Next" while typing should **fast-forward to full line**; a second advances `step`. Keep the ▼ `.cursor` blinking only once the line finishes. Keep "Skip intro" instant.

3. **Poké Ball open animation.** When a `.starter-card` goes from `.closed` to `.open`, animate it: ball wobble (2-3 shakes), a flash/burst, then the mascot scales/fades in. Today the swap is instant via the `revealed` state object in `StarterSelect`. You'll likely need a short "opening" intermediate state per-card (e.g. `revealed[slug] = "opening" -> true`) so the wobble plays before the reveal. Reduce jank: preload mascot images.

4. **Route/page transitions.** Animate navigation between `/`, `/professional`, `/projects`, `/personal`. A tasteful cross-fade or slide keyed on `useLocation().pathname` (wrap `Routes` with `AnimatePresence` if you use Framer Motion). The `Choose {name} →` click should feel like the starter "leads you in."

5. **Scroll-in reveals on pages.** `.stat`, `.block`, `.exp-row`, `.proj-card`, `.badge` should fade/rise in as they enter the viewport (stagger the grids). Use IntersectionObserver or the library's in-view helper.

6. **Hero polish.** Gentle idle float on `.hero-orb` / mascot, and an entrance animation when a page mounts.

## Constraints (do not break these)

- **Accessibility:** gate every non-trivial animation behind `@media (prefers-reduced-motion: reduce)` — reduced motion should fall back to instant or simple fades. Keep focus states and `aria-*` intact (buttons already have labels).
- **Mobile:** the site is mobile-first and has a hamburger nav (`.nav-toggle` / `.nav-links.open`). Test all motion at 375px too; nothing should cause horizontal scroll or layout shift.
- **No content/data edits.** Leave `CONTACT`, `STARTERS`, `INTRO`, `STATS`, `EXPERIENCE`, `PROJECTS`, `PERSONAL`, etc. exactly as they are. **No personal email anywhere** (LinkedIn + GitHub only, by design). Interview Desk stays out.
- **No new heavy deps** beyond one animation library. **Framer Motion** (`motion`) is the recommended choice for React here; if you prefer CSS-only, that's fine too. Keep the bundle sane.
- **Legal:** all creatures/art are original AI-generated homage. Do not add any real Nintendo/Pokémon sprites, logos, sound, or fonts.
- Keep the two-file structure unless a component genuinely needs extracting; if you add files, keep imports clean.

## Definition of done

- All six items above work, on desktop and at 375px, with a clean `prefers-reduced-motion` fallback.
- `npm run build` succeeds with no new warnings; no console errors in dev.
- Commit in logical chunks (one feature per commit). This repo's convention ends commit messages with:
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` — drop that line if you're not running as Claude.

## Nice-to-haves (only if time allows)

- Sound toggle (muted by default) for a soft "select" blip on Poké Ball open.
- Per-project screenshot previews on `.proj-card` (was already parked as a to-do).
- A subtle animated pixel-parallax on the title-screen background.

## Not in scope

- Deploying to derekdinh.com (separate step).
- Cleaning the leftover Vite scaffold files (`src/App.jsx`, `src/App.css`, `src/assets/react.svg`, `src/assets/vite.svg`) — unused, safe to delete but not required.
