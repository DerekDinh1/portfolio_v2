export const STARTERS = [
  {
    slug: "professional",
    name: "Resumon",
    dex: "No. 001",
    type: "Water",
    theme: "water",
    loadImg: () => import("../assets/mascots/resumon.png"),
    loadHi: () => import("../assets/mascots/resumon-hi.webm"),
    loadIdle: () => import("../assets/mascots/resumon-idle.webm"),
    loadBackdrop: (night) =>
      night
        ? import("../assets/habitats/water-night.jpg")
        : import("../assets/habitats/water-day.jpg"),
    tagline: "9+ year IT professional. Non-generative human just trying to be friends with AI before it takes over the world.",
    blurb: "Experience, automation, and integrations.",
  },
  {
    slug: "projects",
    name: "Buildasaur",
    dex: "No. 002",
    type: "Fire",
    theme: "fire",
    loadImg: () => import("../assets/mascots/buildasaur.png"),
    loadHi: () => import("../assets/mascots/buildasaur-hi.webm"),
    loadIdle: () => import("../assets/mascots/buildasaur-idle.webm"),
    loadBackdrop: (night) =>
      night
        ? import("../assets/habitats/fire-night.jpg")
        : import("../assets/habitats/fire-day.jpg"),
    tagline: "Small apps I build after hours.",
    blurb: "Projects, straight from GitHub.",
  },
  {
    slug: "personal",
    name: "Vibeon",
    dex: "No. 003",
    type: "Grass",
    theme: "grass",
    loadImg: () => import("../assets/mascots/vibeon.png"),
    loadHi: () => import("../assets/mascots/vibeon-hi.webm"),
    loadIdle: () => import("../assets/mascots/vibeon-idle.webm"),
    loadBackdrop: (night) =>
      night
        ? import("../assets/habitats/grass-night.jpg")
        : import("../assets/habitats/grass-day.jpg"),
    tagline: "Anime, golf, games, and Colorado trails.",
    blurb: "The person behind the tickets.",
  },
];
