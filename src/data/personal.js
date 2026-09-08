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

// Draft placeholders for Give me a rec. Replace with Derek's real list before ship.
export const RECS = [
  { kind: "book", text: "If Nobody Speaks of Remarkable Things. Quiet, devastating, worth the reread." },
  { kind: "movie", text: "Paddington 2. Warm, funny, and somehow earnest without being soft." },
  { kind: "anime", text: "Frieren: Beyond Journey's End. Slow burn, and it sticks with you." },
  { kind: "game", text: "Slay the Spire. The run I still think about mid-workday." },
  { kind: "trail", text: "Herman Gulch. Steep enough to earn the view, short enough for a weekday." },
  { kind: "game", text: "Dave the Diver. Cozy on the surface, surprisingly deep underneath." },
];
