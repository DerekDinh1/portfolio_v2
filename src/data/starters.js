export const STARTERS = [
  {
    slug: "professional",
    name: "Resumon",
    dex: "No. 001",
    type: "Water",
    theme: "water",
    loadImg: () => import("../assets/mascots/resumon.webp"),
    loadBackdrop: (night) =>
      night
        ? import("../assets/habitats/water-night.jpg")
        : import("../assets/habitats/water-day.jpg"),
    tagline: "9+ year IT professional. Non-generative human just trying to be friends with AI before it takes over the world.",
    blurb: "Experience, automation, and integrations.",
    // Battle-scene hero data (see src/game/BattleHero.jsx).
    battle: {
      habitat: "water",
      sprite: "resumon",
      level: 9, // 9+ years in IT
      bar: {
        label: "EXP",
        value: 67, // 9 years 8 months in IT (since Mar 2017): two-thirds of the way to Lv 10
        text: "Over 9 years of IT experience, on the way to 10",
      },
      status: {
        tag: "OPEN",
        text: "Open to senior IT, automation and AI ops roles",
      },
      message: "RESUMON is on duty. Where to?",
      greetMessage: "RESUMON waves its clipboard. Want the résumé?",
    },
  },
  {
    slug: "projects",
    name: "Buildasaur",
    dex: "No. 002",
    type: "Fire",
    theme: "fire",
    loadImg: () => import("../assets/mascots/buildasaur.webp"),
    loadBackdrop: (night) =>
      night
        ? import("../assets/habitats/fire-night.jpg")
        : import("../assets/habitats/fire-day.jpg"),
    tagline: "Small apps I build after hours.",
    blurb: "Projects, straight from GitHub.",
    // Battle-scene hero data. Level and the LIVE bar are counted from PROJECTS on the page.
    battle: {
      habitat: "fire",
      sprite: "buildasaur",
      status: {
        tag: "WIP",
        text: "Always building something after hours",
      },
      message: "BUILDASAUR fired up the forge. What'll it be?",
      greetMessage: "BUILDASAUR waves its wrench. Want to see the code?",
    },
  },
  {
    slug: "personal",
    name: "Vibeon",
    dex: "No. 003",
    type: "Grass",
    theme: "grass",
    loadImg: () => import("../assets/mascots/vibeon.webp"),
    loadBackdrop: (night) =>
      night
        ? import("../assets/habitats/grass-night.jpg")
        : import("../assets/habitats/grass-day.jpg"),
    tagline: "Anime, golf, games, and Colorado trails.",
    blurb: "The person behind the tickets.",
  },
];
