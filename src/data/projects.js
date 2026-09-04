export const PROJECTS = [
  {
    name: "UVoice",
    what: "A tool that turns your writing voice into a reusable AI prompt.",
    problem: "Writers who want the same tone across ChatGPT, Claude, and other models.",
    outcome: "Built end-to-end as a learning arc: prompt generator, then AI skill, then agent.",
    tech: ["React", "TypeScript", "Vite", "Tailwind", "Zustand", "Zod", "Whisper"],
    builtWith: ["Cursor", "Claude Code"],
    url: "https://github.com/DerekDinh1/uvoice",
    linkType: "source",
  },
  {
    name: "Between Us",
    what: "A two-player card game played in the browser.",
    problem: "Couples and close friends looking for a low-key way to connect.",
    outcome: "Shipped a complete game loop with no backend — just HTML, CSS, and JS.",
    tech: ["HTML", "JS"],
    builtWith: ["Cursor", "Claude Code"],
    url: "https://derekdinh1.github.io/betweenus/",
    linkType: "live",
  },
  {
    name: "Auction War Room",
    what: "A live fantasy football auction draft tracker.",
    problem: "Leagues running salary-cap drafts with no good real-time budget view.",
    outcome: "Persisted roster and spend data in Supabase so the board survives refreshes.",
    tech: ["JavaScript", "Supabase"],
    builtWith: ["Cursor", "Claude Code"],
    url: "https://derekdinh1.github.io/auction-war-room/",
    linkType: "live",
  },
  {
    name: "Laminar Focus",
    what: "A lightweight coach for getting into deep work.",
    problem: "Knowledge workers who lose momentum switching between tasks.",
    outcome: "Deployed on Cloudflare with session state in Supabase — my first edge + DB combo.",
    tech: ["JavaScript", "Cloudflare", "Supabase"],
    builtWith: ["Cursor", "Claude Code"],
    url: "https://laminarfocus.com",
    linkType: "live",
  },
  {
    name: "Dayview",
    what: "A single-page daily dashboard with live weather.",
    problem: "Anyone who opens five tabs every morning just to see what's ahead.",
    outcome: "Learned to pull live weather APIs without a backend — pure client-side.",
    tech: ["JavaScript"],
    builtWith: ["Cursor", "Claude Code"],
    url: "https://derekdinh1.github.io/dayview/",
    linkType: "live",
  },
  {
    name: "TradesXP",
    what: "A trading journal focused on discipline, not P&L bragging.",
    problem: "Retail traders who repeat the same mistakes because they never review entries.",
    outcome: "Shipped a production app on Cloudflare + Supabase with auth and persistent logs.",
    tech: ["JavaScript", "Cloudflare", "Supabase"],
    builtWith: ["Cursor", "Claude Code"],
    url: "https://tradesxp.com",
    linkType: "live",
  },
];

export const TECH_KIND = {
  HTML: "stack",
  JS: "stack",
  JavaScript: "stack",
  TypeScript: "stack",
  React: "stack",
  Vite: "stack",
  Tailwind: "stack",
  Zustand: "stack",
  Zod: "stack",
  Whisper: "stack",
  Supabase: "platform",
  Cloudflare: "platform",
};

export const TECH_GROUP_ORDER = [
  { kind: "stack", label: "Stack" },
  { kind: "platform", label: "Platform" },
];

export function groupTech(tech) {
  const buckets = { stack: [], platform: [] };
  for (const name of tech) {
    const kind = TECH_KIND[name] ?? "stack";
    if (buckets[kind]) buckets[kind].push(name);
  }
  return TECH_GROUP_ORDER.filter((g) => buckets[g.kind].length > 0).map((g) => ({
    ...g,
    items: buckets[g.kind],
  }));
}
