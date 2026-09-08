import { Tv, BookOpen, Clapperboard, Gamepad2, Flag, Mountain } from "lucide-react";

export const PERSONAL = {
  intro:
    "Off the clock, I run on recommendations nobody asked for. Here's the party.",
  badges: [
    { Icon: Tv, h: "Anime & Manga", p: "Always a few series behind, and at peace with it." },
    { Icon: BookOpen, h: "Comics", p: "Long boxes, single issues, and strong opinions about runs." },
    { Icon: Clapperboard, h: "Movies", p: "Ask me for a recommendation. I have several ready." },
    { Icon: Gamepad2, h: "Games", p: "Cozy sims to boss rushes. The backlog never really ends." },
    { Icon: Flag, h: "Golf", p: "Losing golf balls on purpose, apparently." },
    { Icon: Mountain, h: "Colorado Trails", p: "The best debugging happens above tree line." },
  ],
  facts: [
    "First-time dad.",
    "Used to dance competitively on an urban choreography team.",
    "Amateur woodworker.",
    "Favorite book no one's heard of: If Nobody Speaks of Remarkable Things.",
  ],
};

export const RECOMMENDATIONS = [
  {
    kind: "Games",
    items: [
      { name: "Batman Arkham series", blurb: "Still the gold standard for feeling like the Bat." },
      { name: "Diablo 2", blurb: "Loot loops that ruined every other ARPG for me." },
      { name: "Stardew Valley", blurb: "The cozy reset button. One more day turns into midnight." },
    ],
  },
  {
    kind: "Movies / shows",
    items: [
      { name: "Sinister", blurb: "Proper unsettling. The kind that sticks after the credits." },
      { name: "Parks & Rec", blurb: "Comfort TV with actual heart. Treat yo'self rewatch fuel." },
      { name: "The Gentlemen", blurb: "Both the show and movie are great. Stylish chaos never looks so good." },
      { name: "Abbott Elementary", blurb: "Warm, sharp, and somehow never cynical." },
      { name: "The Bear", blurb: "Kitchen stress as prestige drama. Anxiety optional, flavor required." },
      { name: "Peaky Blinders", blurb: "Fits, smoke, and family drama with a soundtrack." },
    ],
  },
  {
    kind: "Anime / manga",
    items: [
      { name: "Your Name", blurb: "Beautiful, aching, and worth every rewatch." },
      {
        name: "Dandadan",
        blurb: "Make it past the first few episodes or chapters. I promise.",
      },
      { name: "Versus", blurb: "Wild premise, wilder fights. Currently chewing through it." },
      { name: "Tsuyoshi", blurb: "Underdog sports manga with ridiculous momentum." },
      { name: "Kagurabachi", blurb: "Blade revenge done clean and sharp." },
    ],
  },
  {
    kind: "Trails",
    items: [
      {
        name: "Hidden Falls",
        blurb: "Wild Basin in RMNP. Short approach, big payoff, icy in winter.",
      },
      {
        name: "Emerald Lake",
        blurb: "Classic Bear Lake corridor hike. Crowded for a reason.",
      },
      {
        name: "South Valley Park",
        blurb: "Jeffco open space near Littleton. Red rocks without the I-70 scramble.",
      },
      {
        name: "Lost Lake",
        blurb: "Hessie Trail near Nederland. Alpine lake day trip that earns the drive.",
      },
    ],
  },
];

// Flat pool for Vibeon's speech-bubble picks.
export const RECS = RECOMMENDATIONS.flatMap((group) =>
  group.items.map((item) => ({
    kind: group.kind.split(" / ")[0].toLowerCase().replace(/s$/, ""),
    text: `${item.name}. ${item.blurb}`,
  }))
);
