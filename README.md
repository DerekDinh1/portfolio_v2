# 🎮 Derek Dinh — Portfolio

[![Live site](https://img.shields.io/badge/live-derekdinh.com-e23b3b?style=flat-square)](https://derekdinh.com)
[![Built with Vite](https://img.shields.io/badge/built%20with-Vite-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vite.dev)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)

> *A personal portfolio dressed as a Pokémon-style adventure — choose a starter, explore the paths.*

## 🌟 Highlights

- **Choose a starter** — Resumon, Buildasaur, or Vibeon each lead into a different side of the story
- **Day / night mode** — a calm toggle that shifts the whole scene
- **Motion with restraint** — title ambience, mascot loops, and route transitions that respect `prefers-reduced-motion`
- **Mobile-first** — framed navbar, hamburger menu, and layouts that hold up at 375px
- **Static & fast** — Vite + React, deployed to GitHub Pages at [derekdinh.com](https://derekdinh.com)

## ℹ️ Overview

This site is Derek Dinh’s personal portfolio: an IT operator’s résumé, projects, and personal interests wrapped in a light Pokémon homage (original mascots and UI — no Nintendo assets).

You land on a title screen, step through a short intro, then pick a Poké Ball. Each starter opens a themed page:

| Starter | Path | Theme |
| --- | --- | --- |
| **Resumon** | `/professional` | Experience, automation, systems |
| **Buildasaur** | `/projects` | Side projects from GitHub |
| **Vibeon** | `/personal` | Anime, golf, games, Colorado trails |

Built with **Vite**, **React 19**, **react-router-dom**, and **Motion**, with styles and tokens living in `src/index.css`.

### ✍️ Author

I'm [Derek Dinh](https://github.com/DerekDinh1) — IT support and systems, lately automation and agentic AI. Find me on [LinkedIn](https://www.linkedin.com/in/dinhderek) or the live site at [derekdinh.com](https://derekdinh.com).

## 🚀 Usage

Clone, install, and run the Vite app:

```bash
npm install
npm run dev
```

Open the printed local URL (usually `http://localhost:5173`), press **Start**, and pick a starter.

Useful scripts:

| Command | What it does |
| --- | --- |
| `npm run dev` | Local development server |
| `npm run build` | Production build to `dist/` |
| `npm run preview` | Serve the production build locally |
| `npm run lint` | Run Oxlint |

## ⬇️ Installation

**Requirements:** Node.js 20+ (or a current LTS) and npm.

```bash
git clone https://github.com/DerekDinh1/portfolio_v2.git
cd portfolio_v2
npm install
```

No other runtime services are required — this is a static front-end.

## 💭 Feedback and Contributing

Spotted a bug, have a motion idea, or want to suggest a feature? Open an [issue](https://github.com/DerekDinh1/portfolio_v2/issues) on this repo.

PRs are welcome for polish, accessibility, and performance. Keep the Pokémon homage original (no Nintendo sprites, logos, or audio), and prefer small, focused changes.

## 📖 Further reading

README structure inspired by [banesullivan/README](https://github.com/banesullivan/README) — *How to write a good README*.
