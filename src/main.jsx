import { StrictMode, createContext, useContext, useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  NavLink,
  useLocation,
  useNavigate,
} from "react-router-dom";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import "./index.css";

import resumon from "./assets/mascots/resumon.png";
import buildasaur from "./assets/mascots/buildasaur.png";
import vibeon from "./assets/mascots/vibeon.png";
import resumonHi from "./assets/mascots/resumon-hi.webm";
import resumonIdle from "./assets/mascots/resumon-idle.webm";
import buildasaurHi from "./assets/mascots/buildasaur-hi.webm";
import buildasaurIdle from "./assets/mascots/buildasaur-idle.webm";
import vibeonHi from "./assets/mascots/vibeon-hi.webm";
import vibeonIdle from "./assets/mascots/vibeon-idle.webm";
import titleBg from "./assets/title-bg.jpg";
import titleBgNight from "./assets/title-bg-night.jpg";
import titleBgDayVid from "./assets/title-bg-day.mp4";
import titleBgNightVid from "./assets/title-bg-night.mp4";
import { Tv, BookOpen, Clapperboard, Gamepad2, Flag, Mountain, Menu, X } from "lucide-react";

const TITLE_AMBIENCE_RATE = 0.45; // 55% slower than full speed
const TITLE_AMBIENCE_CROSSFADE_WALL_S = 1.75;
const CAN_PLAY_WEBM =
  typeof document !== "undefined" &&
  document.createElement("video").canPlayType('video/webm; codecs="vp9"') !== "";

/**
 * Seamless title ambience:
 * - Source clips use the original still as BOTH first and last frame (returns to start).
 * - ffmpeg self-crossfade + dual video buffers hide any residual seam.
 * - Play at 1× so motion stays smooth (no frame ticking from ultra-slow playback).
 */
function SeamlessAmbienceVideo({ src, poster, className, active }) {
  const aRef = useRef(null);
  const bRef = useRef(null);
  const [front, setFront] = useState("a");
  const fadingRef = useRef(false);
  const frontRef = useRef(front);
  frontRef.current = front;

  useEffect(() => {
    [aRef.current, bRef.current].forEach((v) => {
      if (!v) return;
      v.playbackRate = TITLE_AMBIENCE_RATE;
      v.defaultPlaybackRate = TITLE_AMBIENCE_RATE;
    });
  }, [src]);

  useEffect(() => {
    const a = aRef.current;
    const b = bRef.current;
    if (!a || !b) return undefined;

    const applyRate = (v) => {
      if (v.playbackRate !== TITLE_AMBIENCE_RATE) v.playbackRate = TITLE_AMBIENCE_RATE;
      v.defaultPlaybackRate = TITLE_AMBIENCE_RATE;
    };
    const mediaFade = TITLE_AMBIENCE_CROSSFADE_WALL_S * TITLE_AMBIENCE_RATE;

    if (!active) {
      a.pause();
      b.pause();
      fadingRef.current = false;
      return undefined;
    }

    const frontEl = frontRef.current === "a" ? a : b;
    const backEl = frontRef.current === "a" ? b : a;
    applyRate(frontEl);
    applyRate(backEl);
    backEl.pause();
    const play = frontEl.play();
    if (play && typeof play.catch === "function") play.catch(() => {});

    const onTimeUpdate = () => {
      if (fadingRef.current) return;
      const lead = frontRef.current === "a" ? a : b;
      const next = frontRef.current === "a" ? b : a;
      if (!Number.isFinite(lead.duration) || lead.duration < mediaFade + 0.35) {
        return;
      }
      if (lead.duration - lead.currentTime > mediaFade) return;

      fadingRef.current = true;
      applyRate(next);
      try {
        next.currentTime = 0;
      } catch {
        /* ignore */
      }
      const nextPlay = next.play();
      if (nextPlay && typeof nextPlay.catch === "function") nextPlay.catch(() => {});
      setFront((f) => (f === "a" ? "b" : "a"));
      window.setTimeout(() => {
        lead.pause();
        fadingRef.current = false;
      }, TITLE_AMBIENCE_CROSSFADE_WALL_S * 1000 + 80);
    };

    a.addEventListener("timeupdate", onTimeUpdate);
    b.addEventListener("timeupdate", onTimeUpdate);
    return () => {
      a.removeEventListener("timeupdate", onTimeUpdate);
      b.removeEventListener("timeupdate", onTimeUpdate);
    };
  }, [active, src]);

  return (
    <div className={`title-bg title-ambience ${className}`}>
      <video
        ref={aRef}
        className={`title-ambience-layer${front === "a" ? " is-front" : ""}`}
        src={src}
        poster={poster}
        muted
        playsInline
        preload={active ? "auto" : "metadata"}
      />
      <video
        ref={bRef}
        className={`title-ambience-layer${front === "b" ? " is-front" : ""}`}
        src={src}
        poster={poster}
        muted
        playsInline
        preload={active ? "auto" : "metadata"}
      />
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* CONTENT (real facts, sourced from Derek's resume)                   */
/* ------------------------------------------------------------------ */
const CONTACT = {
  linkedin: "https://www.linkedin.com/in/dinhderek",
  github: "https://github.com/DerekDinh1",
};

const STARTERS = [
  {
    slug: "professional",
    name: "Resumon",
    dex: "No. 001",
    type: "Water",
    theme: "water",
    img: resumon,
    hi: resumonHi,
    idle: resumonIdle,
    tagline: "9+ years across IT support, security, and systems. Lately, automation and agentic AI.",
    blurb: "Experience, automation, and integrations.",
  },
  {
    slug: "projects",
    name: "Buildasaur",
    dex: "No. 002",
    type: "Fire",
    theme: "fire",
    img: buildasaur,
    hi: buildasaurHi,
    idle: buildasaurIdle,
    tagline: "Small apps I build after hours.",
    blurb: "Projects, straight from GitHub.",
  },
  {
    slug: "personal",
    name: "Vibeon",
    dex: "No. 003",
    type: "Grass",
    theme: "grass",
    img: vibeon,
    hi: vibeonHi,
    idle: vibeonIdle,
    tagline: "Anime, golf, games, and Colorado trails.",
    blurb: "The person behind the tickets.",
  },
];

const INTRO = [
  "Hello there! Welcome to the world of Derek Dinh.",
  "For 9+ years I've kept IT running: fixing what breaks, automating what shouldn't be manual, and writing it all down.",
  "There's more to me than uptime and tickets. I build small apps, chase golf balls, and fall behind on good anime.",
  "This place splits into a few paths. Each one is a different side of me.",
  "Pick a Poké Ball to start. You can always come back for the others.",
];

const STATS = [
  { n: "9+ yrs", l: "in IT support, security, and systems" },
  { n: "79%", l: "of Slack support requests handled by an AI agent I built" },
  { n: "300+", l: "Apple endpoints managed at 95% uptime" },
  { n: "60%", l: "faster ticket resolution" },
];

const FOCUS = [
  "IT security, process, and systems management across fast-moving teams.",
  "Automation and agentic AI: building AI agents and workflows that take repetitive work off people's plates.",
  "Growth mentorship for junior team members.",
];

const EXPERIENCE = [
  {
    org: "Spring Health",
    role: "Senior IT Support Engineer",
    when: "Feb 2025 to Jul 2026",
    points: [
      "Architected a Console AI agent into our Slack help channel that freed over 79% of human resources through automated resolutions and escalations.",
      "Created, reviewed, and established agentic AI models across department platforms and company channels using Console, ChatGPT, and Claude.",
      "Revamped multiple SOPs to increase team efficiency, which unlocked further automation from those frameworks.",
      "Served as a senior escalation point for technical issues, partnering with stakeholders to keep resolution timely and service continuous.",
      "Managed technology integration and migration during acquisition efforts, coordinating across teams to minimize disruption.",
    ],
  },
  {
    org: "Valtech (formerly Kin+Carta)",
    role: "Senior IT Support Specialist",
    when: "Jun 2023 to Feb 2025",
    points: [
      "Developed and executed IT initiatives aligned with organizational objectives, achieving 100% completion of targeted deliverables.",
      "Implemented security and operational best practices through risk assessments, system maintenance, and end-user education.",
      "Mentored junior support staff and promoted knowledge sharing across the team.",
      "Performed system analysis, troubleshooting, and upgrades to improve performance, stability, and security.",
    ],
  },
  {
    org: "Handshake",
    role: "IT Support Engineer",
    when: "Apr 2022 to May 2023",
    points: [
      "Diagnosed, investigated, and resolved hardware, software, and network issues, reducing ticket resolution times by 60%.",
      "Maintained and enhanced technical documentation and knowledge base content, increasing documentation accuracy by 70%.",
      "Designed and implemented automated Okta workflows and system enhancements, improving operational efficiency and user experience by 50%.",
      "Supported and maintained Apple hardware across 300+ endpoints with Jamf Pro, hitting 95% uptime and streamlining device enrollment by 40%.",
    ],
  },
  {
    org: "Red Canary",
    role: "IT Support Admin",
    when: "Apr 2021 to Apr 2022",
    points: [
      "Led a process-improvement team for end-user onboarding and training with A3/lean methodology, resulting in a 90% better onboarding experience.",
      "Developed Zendesk and Slack workflows for help requests, improving response times by 30%.",
      "Promoted documentation maintenance for new systems, increasing knowledge management by 40%.",
    ],
  },
  {
    org: "FORM MarketX (formerly GoSpotCheck)",
    role: "IT Desktop Support Specialist",
    when: "Dec 2019 to Mar 2021",
    points: [
      "Developed, implemented, and maintained an asset-tracking system in Asana to improve hardware accountability.",
      "Improved employee onboarding, security practices, and equipment maintenance as the company scaled.",
      "Planned internal technical operations and communicated across teams so new hires were set up for success.",
      "Resolved user issues quickly while finding creative fixes for unique problems across teams and executives.",
    ],
  },
];

const SKILLS = [
  { h: "Support & Systems", items: ["Microsoft 365", "Google Workspace", "Entra ID / Azure AD", "Active Directory", "Okta", "Intune", "Jamf", "Kandji", "Windows & Mac endpoints", "VPN admin"] },
  { h: "Service Management", items: ["ServiceNow", "Zendesk", "FreshService", "Atlassian", "Incident management", "Root cause analysis", "SLA management", "SOC 2 compliance"] },
  { h: "AI, Automation & Integrations", items: ["Agentic AI", "Console AI", "Claude", "OpenAI (ChatGPT)", "Okta Workflows", "Zapier", "n8n", "API integrations", "Python", "JavaScript"] },
];

const EDUCATION = {
  school: "Colorado Technical University",
  year: "2018 to 2020",
  degree: "Bachelor's in Information Technology",
  minors: "Minors in Web Development and Project Management",
};

const PROJECTS = [
  {
    name: "UVoice",
    tagline:
      "Turn your writing voice into a prompt you can feed any AI. Built as a learning project: prompt generator, then AI skill, then AI agent.",
    tech: [
      "React",
      "TypeScript",
      "Vite",
      "Tailwind",
      "Zustand",
      "Zod",
      "Whisper",
      "Cursor",
      "Claude Code",
    ],
    url: "https://github.com/DerekDinh1/uvoice",
  },
  {
    name: "Between Us",
    tagline: "A card game for two.",
    tech: ["HTML", "JS", "Cursor", "Claude Code"],
    url: "https://derekdinh1.github.io/betweenus/",
  },
  {
    name: "Auction War Room",
    tagline: "Track your fantasy football auction draft as it happens.",
    tech: ["JavaScript", "Supabase", "Cursor", "Claude Code"],
    url: "https://derekdinh1.github.io/auction-war-room/",
  },
  {
    name: "Laminar Focus",
    tagline: "A little coach for getting into deep work.",
    tech: ["JavaScript", "Cloudflare", "Supabase", "Cursor", "Claude Code"],
    url: "https://laminarfocus.com",
  },
  {
    name: "Dayview",
    tagline: "Your day at a glance, with live weather.",
    tech: ["JavaScript", "Cursor", "Claude Code"],
    url: "https://derekdinh1.github.io/dayview/",
  },
  {
    name: "TradesXP",
    tagline: "A trading journal that helps you stay disciplined.",
    tech: ["JavaScript", "Cloudflare", "Supabase", "Cursor", "Claude Code"],
    url: "https://tradesxp.com",
  },
];

const TECH_KIND = {
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
  Cursor: "ai",
  "Claude Code": "ai",
};

const TECH_GROUP_ORDER = [
  { kind: "stack", label: "Stack" },
  { kind: "platform", label: "Platform" },
  { kind: "ai", label: "AI" },
];

function groupTech(tech) {
  const buckets = { stack: [], platform: [], ai: [] };
  for (const name of tech) {
    const kind = TECH_KIND[name] ?? "stack";
    buckets[kind].push(name);
  }
  return TECH_GROUP_ORDER.filter((g) => buckets[g.kind].length > 0).map((g) => ({
    ...g,
    items: buckets[g.kind],
  }));
}

const PERSONAL = {
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

/* ------------------------------------------------------------------ */
/* DAY / NIGHT                                                          */
/* ------------------------------------------------------------------ */
const TimeContext = createContext({ mode: "day", toggle: () => {} });

function readStoredTime() {
  try {
    const v = localStorage.getItem("dd-time");
    if (v === "day" || v === "night") return v;
  } catch {
    /* ignore */
  }
  return "day";
}

function TimeProvider({ children }) {
  const [mode, setMode] = useState(readStoredTime);

  useEffect(() => {
    document.documentElement.dataset.time = mode;
    try {
      localStorage.setItem("dd-time", mode);
    } catch {
      /* ignore */
    }
  }, [mode]);

  const toggle = () => setMode((m) => (m === "day" ? "night" : "day"));
  return (
    <TimeContext.Provider value={{ mode, toggle }}>
      {children}
    </TimeContext.Provider>
  );
}

function useTime() {
  return useContext(TimeContext);
}

function DayNightToggle() {
  const { mode, toggle } = useTime();
  const night = mode === "night";
  return (
    <button
      type="button"
      className={`time-toggle${night ? " night" : " day"}`}
      onClick={toggle}
      aria-label={night ? "Switch to day mode" : "Switch to night mode"}
      aria-pressed={night}
      title={night ? "Night — tap for day" : "Day — tap for night"}
    >
      <span className="time-track" aria-hidden="true">
        <span className="time-sky">
          <span className="time-star s1" />
          <span className="time-star s2" />
          <span className="time-star s3" />
        </span>
        <span className="time-knob">
          <span className="time-sun" />
          <span className="time-moon" />
        </span>
      </span>
      <span className="time-label">{night ? "NIGHT" : "DAY"}</span>
    </button>
  );
}

/* ------------------------------------------------------------------ */
/* MOTION HELPERS                                                       */
/* ------------------------------------------------------------------ */
const EASE_OUT = [0.22, 1, 0.36, 1];

const MOTION_TAGS = {
  div: motion.div,
  section: motion.section,
  article: motion.article,
  li: motion.li,
};

function Reveal({ children, className = "", as = "div", delay = 0, ...rest }) {
  const reduce = useReducedMotion();
  const Tag = MOTION_TAGS[as] || motion.div;
  return (
    <Tag
      className={className}
      initial={reduce ? false : { opacity: 0, y: 18 }}
      whileInView={reduce ? undefined : { opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: reduce ? 0 : 0.45, delay: reduce ? 0 : delay, ease: EASE_OUT }}
      {...rest}
    >
      {children}
    </Tag>
  );
}

/* ------------------------------------------------------------------ */
/* SHARED COMPONENTS                                                    */
/* ------------------------------------------------------------------ */
function Nav() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const close = () => setOpen(false);
  const goTitle = (e) => {
    e.preventDefault();
    close();
    navigate("/", { state: { screen: "title", t: Date.now() } });
  };
  return (
    <header className="nav">
      <div className="nav-frame">
        <div className="nav-plate nav-plate-head">
          <Link to="/" className="wordmark" onClick={goTitle}>DEREK DINH</Link>
        </div>
        <div className="nav-plate nav-plate-body">
          <div className="nav-lead">
            <button
              className="nav-toggle"
              aria-label={open ? "Close menu" : "Open menu"}
              aria-expanded={open}
              onClick={() => setOpen((o) => !o)}
            >
              {open ? <X size={20} /> : <Menu size={20} />}
            </button>
            <DayNightToggle />
          </div>
          <nav className={`nav-links ${open ? "open" : ""}`} aria-label="Primary">
            <NavLink to="/professional" onClick={close} className={({ isActive }) => `nav-item${isActive ? " on" : ""}`}>Professional</NavLink>
            <NavLink to="/projects" onClick={close} className={({ isActive }) => `nav-item${isActive ? " on" : ""}`}>Projects</NavLink>
            <NavLink to="/personal" onClick={close} className={({ isActive }) => `nav-item${isActive ? " on" : ""}`}>Personal</NavLink>
            <a className="btn btn-red nav-cta nav-cta-mobile" href={CONTACT.linkedin} target="_blank" rel="noopener noreferrer" onClick={close}>Get in touch</a>
          </nav>
          <div className="nav-end">
            <a className="btn btn-red nav-cta" href={CONTACT.linkedin} target="_blank" rel="noopener noreferrer">Get in touch</a>
          </div>
        </div>
      </div>
    </header>
  );
}

function MascotSprite({ starter, loop, className, alt }) {
  const reduce = useReducedMotion();
  const [failed, setFailed] = useState(false);
  const src = loop === "hi" ? starter.hi : starter.idle;
  if (reduce || !src || failed || !CAN_PLAY_WEBM) {
    return <img className={className} src={starter.img} alt={alt} />;
  }
  return (
    <video
      className={className}
      src={src}
      poster={starter.img}
      autoPlay
      loop
      muted
      playsInline
      aria-label={alt}
      onLoadedMetadata={(e) => {
        e.currentTarget.playbackRate = 1.25;
        e.currentTarget.defaultPlaybackRate = 1.25;
      }}
      onError={() => setFailed(true)}
    />
  );
}

function PageHero({ starter }) {
  const reduce = useReducedMotion();
  return (
    <section className={`hero theme-${starter.theme}`}>
      <motion.div
        className="hero-copy"
        initial={reduce ? false : { opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: reduce ? 0 : 0.5, ease: EASE_OUT }}
      >
        <span className="dex">{starter.dex} · {starter.type} type</span>
        <h1 className="hero-name">{starter.name}</h1>
        <p className="hero-tagline">{starter.tagline}</p>
      </motion.div>
      <motion.div
        className="hero-art"
        initial={reduce ? false : { opacity: 0, scale: 0.92 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: reduce ? 0 : 0.55, delay: reduce ? 0 : 0.08, ease: EASE_OUT }}
      >
        <MascotSprite
          starter={starter}
          loop="idle"
          className="hero-mascot"
          alt={`${starter.name}, the ${starter.type}-type starter`}
        />
      </motion.div>
    </section>
  );
}

function Contact() {
  const navigate = useNavigate();
  return (
    <footer className="contact">
      <h2>Get in touch</h2>
      <p>Recruiters, collaborators, or anyone with a movie recommendation. Find me here.</p>
      <div className="contact-links">
        <a className="btn btn-red" href={CONTACT.linkedin} target="_blank" rel="noopener noreferrer">LinkedIn</a>
        <a className="btn btn-ghost" href={CONTACT.github} target="_blank" rel="noopener noreferrer">GitHub</a>
      </div>
      <Link
        to="/"
        className="back-lab"
        onClick={(e) => {
          e.preventDefault();
          navigate("/", { state: { screen: "title", t: Date.now() } });
        }}
      >
        ← Back to the lab
      </Link>
    </footer>
  );
}

/* ------------------------------------------------------------------ */
/* HOME (title screen -> intro dialogue -> starter select)             */
/* ------------------------------------------------------------------ */
function TitleScreen({ onStart }) {
  const reduce = useReducedMotion();
  const { mode } = useTime();
  const night = mode === "night";

  return (
    <section
      className={`title-screen${reduce ? " reduced" : ""}${night ? " is-night" : " is-day"}`}
    >
      <div className="title-bg-stack" aria-hidden="true">
        <div
          className="title-bg title-bg-still title-bg-day"
          style={{ backgroundImage: `url(${titleBg})` }}
        />
        <div
          className="title-bg title-bg-still title-bg-night"
          style={{ backgroundImage: `url(${titleBgNight})` }}
        />
        {!reduce ? (
          <>
            <SeamlessAmbienceVideo
              className="title-bg-day"
              src={titleBgDayVid}
              poster={titleBg}
              active={!night}
            />
            <SeamlessAmbienceVideo
              className="title-bg-night"
              src={titleBgNightVid}
              poster={titleBgNight}
              active={night}
            />
          </>
        ) : null}
      </div>
      <div className="title-skyfx" aria-hidden="true">
        <div className="title-stars">
          {Array.from({ length: 18 }, (_, i) => (
            <span key={i} className={`title-star n${i + 1}`} />
          ))}
        </div>
      </div>
      <div className="title-inner">
        <p className="title-region">Colorado Region</p>
        <h1 className="title-name">DEREK DINH</h1>
        <button className="title-press btn-pop" onClick={onStart}>
          Press Start
        </button>
      </div>
    </section>
  );
}

function StarterSelect() {
  const [revealed, setRevealed] = useState({});
  const reduce = useReducedMotion();
  const timers = useRef([]);

  useEffect(() => {
    STARTERS.forEach((s) => {
      const img = new Image();
      img.src = s.img;
    });
    const pending = timers.current;
    return () => {
      pending.forEach(clearTimeout);
    };
  }, []);

  const reveal = (slug) => {
    if (revealed[slug]) return;
    if (reduce) {
      setRevealed((r) => ({ ...r, [slug]: true }));
      return;
    }
    setRevealed((r) => ({ ...r, [slug]: "opening" }));
    const t1 = setTimeout(() => {
      setRevealed((r) => ({ ...r, [slug]: "popping" }));
    }, 720);
    const t2 = setTimeout(() => {
      setRevealed((r) => ({ ...r, [slug]: true }));
    }, 1850);
    timers.current.push(t1, t2);
  };

  return (
    <section className="select-stage">
      <h1 className="select-title">Choose a starter</h1>
      <p className="select-sub">Tap a Poké Ball to see who's inside. You can catch all three.</p>
      <div className="starter-grid">
        {STARTERS.map((s) => {
          const state = revealed[s.slug];
          const opening = state === "opening";
          const popping = state === "popping";
          const open = state === true;
          return (
            <div
              key={s.slug}
              className={`starter-card ${
                open
                  ? `theme-${s.theme} open`
                  : opening || popping
                    ? `theme-${s.theme} ${opening ? "opening" : "popping"}`
                    : "closed"
              }`}
            >
              {open || popping ? (
                <>
                  <div className="starter-mascot-wrap">
                    {popping ? (
                      <>
                        <span className="pokeball pokeball-fade" aria-hidden="true" />
                        <span className="pokeball-burst" aria-hidden="true" />
                      </>
                    ) : null}
                    <MascotSprite
                      starter={s}
                      loop="hi"
                      className={`starter-img${popping || open ? " emerging" : ""}`}
                      alt={s.name}
                    />
                  </div>
                  <div
                    className={`starter-details${open ? " in" : " pending"}`}
                    aria-hidden={!open}
                  >
                    <span className="starter-dex">{s.dex} · {s.type}</span>
                    <h2 className="starter-name">{s.name}</h2>
                    <p className="starter-blurb">{s.blurb}</p>
                    <Link
                      to={`/${s.slug}`}
                      className="starter-cta"
                      tabIndex={open ? 0 : -1}
                    >
                      Choose {s.name} →
                    </Link>
                  </div>
                </>
              ) : (
                <button
                  className={`pokeball-btn${opening ? " wobbling" : ""}`}
                  onClick={() => reveal(s.slug)}
                  disabled={opening}
                  aria-label={`Open the ${s.slug} Poké Ball`}
                >
                  <span className="pokeball" aria-hidden="true" />
                  {opening ? <span className="pokeball-burst" aria-hidden="true" /> : null}
                  <span className="pokeball-hint">
                    {s.slug.charAt(0).toUpperCase() + s.slug.slice(1)}
                  </span>
                </button>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}

function IntroDialogue({ step, setStep, onSkip, onChoose }) {
  const line = INTRO[step];
  const last = step >= INTRO.length - 1;
  const reduce = useReducedMotion();
  const [typed, setTyped] = useState(reduce ? line : "");
  const [done, setDone] = useState(!!reduce);
  const [cardKey, setCardKey] = useState(0);
  const skipRef = useRef(false);
  const advancing = useRef(false);

  useEffect(() => {
    skipRef.current = false;
    advancing.current = false;
    if (reduce) {
      setTyped(line);
      setDone(true);
      return undefined;
    }
    setTyped("");
    setDone(false);
    let i = 0;
    const id = setInterval(() => {
      if (skipRef.current) {
        clearInterval(id);
        setTyped(line);
        setDone(true);
        return;
      }
      i += 1;
      setTyped(line.slice(0, i));
      if (i >= line.length) {
        clearInterval(id);
        setDone(true);
      }
    }, 28);
    return () => clearInterval(id);
  }, [line, step, reduce]);

  const advanceStep = () => {
    if (advancing.current) return;
    if (last) {
      onChoose();
      return;
    }
    advancing.current = true;
    if (reduce) {
      setStep((s) => s + 1);
      setCardKey((k) => k + 1);
      return;
    }
    // brief fade handled by AnimatePresence key change
    setStep((s) => s + 1);
    setCardKey((k) => k + 1);
  };

  const onNext = () => {
    if (!done) {
      skipRef.current = true;
      setTyped(line);
      setDone(true);
      return;
    }
    advanceStep();
  };

  return (
    <section className="intro-stage">
      <AnimatePresence mode="wait">
        <motion.div
          key={cardKey}
          className="dialogue"
          initial={reduce ? { opacity: 0 } : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={reduce ? { opacity: 0 } : { opacity: 0, y: -8 }}
          transition={{ duration: reduce ? 0.15 : 0.28, ease: EASE_OUT }}
        >
          <span className="nameplate">PROF. DINH</span>
          <p className="dialogue-text">
            {typed}
            {!done ? <span className="type-caret" aria-hidden="true">▌</span> : null}
          </p>
          {done ? <span className="cursor bounce" aria-hidden="true">▼</span> : null}
          <div className="dialogue-controls">
            <button className="btn btn-ghost btn-pop" onClick={onSkip}>Skip intro</button>
            {last && done ? (
              <button className="btn btn-red btn-pop" onClick={onChoose}>Choose a starter</button>
            ) : (
              <button className="btn btn-dark btn-pop" onClick={onNext}>
                Next
              </button>
            )}
          </div>
        </motion.div>
      </AnimatePresence>
      <ol className="progress" aria-hidden="true">
        {INTRO.map((_, i) => (
          <li key={i} className={i <= step ? "done" : ""} />
        ))}
      </ol>
    </section>
  );
}

function Home() {
  const [scene, setScene] = useState("title"); // title | intro | select
  const [step, setStep] = useState(0);
  const reduce = useReducedMotion();
  const location = useLocation();

  useEffect(() => {
    if (location.pathname !== "/") return;
    setScene("title");
    setStep(0);
  }, [location.pathname, location.state?.t]);

  return (
    <main className="home">
      <AnimatePresence mode="wait">
        {scene === "title" ? (
          <motion.div
            key="title"
            initial={false}
            exit={{ opacity: 0 }}
            transition={{ duration: reduce ? 0.12 : 0.55, ease: "easeInOut" }}
          >
            <TitleScreen onStart={() => setScene("intro")} />
          </motion.div>
        ) : scene === "intro" ? (
          <motion.div
            key="intro"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: reduce ? 0.12 : 0.55, ease: "easeInOut" }}
          >
            <IntroDialogue
              step={step}
              setStep={setStep}
              onSkip={() => setScene("select")}
              onChoose={() => setScene("select")}
            />
          </motion.div>
        ) : (
          <motion.div
            key="select"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: reduce ? 0.12 : 0.45, ease: "easeInOut" }}
          >
            <StarterSelect />
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}

/* ------------------------------------------------------------------ */
/* PROFESSIONAL (Resumon)                                              */
/* ------------------------------------------------------------------ */
function Professional() {
  const starter = STARTERS[0];
  return (
    <main className="page theme-water">
      <PageHero starter={starter} />
      <div className="wrap">
        <section className="stats">
          {STATS.map((s, i) => (
            <Reveal className="stat" key={s.l} delay={i * 0.06}>
              <div className="stat-n">{s.n}</div>
              <div className="stat-l">{s.l}</div>
            </Reveal>
          ))}
        </section>

        <Reveal className="block" as="section">
          <h2 className="block-h">What I'm focused on</h2>
          <ul className="notable">
            {FOCUS.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>
        </Reveal>

        <Reveal className="block" as="section">
          <h2 className="block-h">Experience</h2>
          <ul className="exp">
            {EXPERIENCE.map((e, i) => (
              <Reveal className="exp-row" as="li" key={e.org} delay={i * 0.05}>
                <div className="exp-head">
                  <div>
                    <div className="exp-org">{e.org}</div>
                    <div className="exp-role">{e.role}</div>
                  </div>
                  <span className="exp-when">{e.when}</span>
                </div>
                <ul className="exp-points">
                  {e.points.map((p, j) => (
                    <li key={j}>{p}</li>
                  ))}
                </ul>
              </Reveal>
            ))}
          </ul>
        </Reveal>

        <Reveal className="block" as="section">
          <h2 className="block-h">Skills</h2>
          <div className="skills">
            {SKILLS.map((g) => (
              <div className="skill-group" key={g.h}>
                <h3>{g.h}</h3>
                <ul className="chips">
                  {g.items.map((it) => (
                    <li className="chip" key={it}>{it}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </Reveal>

        <Reveal className="block" as="section">
          <h2 className="block-h">Education</h2>
          <div className="edu">
            <div className="edu-head">
              <div className="edu-school">{EDUCATION.school}</div>
              <span className="exp-when">{EDUCATION.year}</span>
            </div>
            <div className="edu-degree">{EDUCATION.degree}</div>
            <div className="edu-minors">{EDUCATION.minors}</div>
          </div>
        </Reveal>
      </div>
      <Contact />
    </main>
  );
}

/* ------------------------------------------------------------------ */
/* PROJECTS (Buildasaur)                                               */
/* ------------------------------------------------------------------ */
function Projects() {
  const starter = STARTERS[1];
  return (
    <main className="page theme-fire">
      <PageHero starter={starter} />
      <div className="wrap">
        <Reveal className="block" as="section">
          <h2 className="block-h">Caught apps</h2>
          <p className="block-sub">Things I build after hours. Grab one off the shelf.</p>
          <div className="proj-grid">
            {PROJECTS.map((p, i) => (
              <Reveal className="proj-card" as="article" key={p.name} delay={i * 0.06}>
                <h3 className="proj-name">{p.name}</h3>
                <p className="proj-tag">{p.tagline}</p>
                <div className="proj-tech">
                  {groupTech(p.tech).map((group) => (
                    <div className="proj-tech-group" key={group.kind}>
                      <span className="proj-tech-label">{group.label}</span>
                      <ul className="chips">
                        {group.items.map((t) => (
                          <li className={`chip chip-${group.kind}`} key={t}>{t}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
                <div className="proj-links">
                  <a href={p.url} target="_blank" rel="noopener noreferrer">Visit →</a>
                </div>
              </Reveal>
            ))}
          </div>
        </Reveal>
      </div>
      <Contact />
    </main>
  );
}

/* ------------------------------------------------------------------ */
/* PERSONAL (Vibeon)                                                   */
/* ------------------------------------------------------------------ */
function Personal() {
  const starter = STARTERS[2];
  return (
    <main className="page theme-grass">
      <PageHero starter={starter} />
      <div className="wrap">
        <Reveal className="block" as="section">
          <p className="fun-intro">{PERSONAL.intro}</p>
          <div className="badges">
            {PERSONAL.badges.map((b, i) => {
              const Icon = b.Icon;
              return (
                <Reveal className="badge" key={b.h} delay={i * 0.05}>
                  <span className="badge-icon" aria-hidden="true"><Icon size={28} strokeWidth={2} /></span>
                  <h3>{b.h}</h3>
                  <p>{b.p}</p>
                </Reveal>
              );
            })}
          </div>
        </Reveal>

        <Reveal className="block" as="section">
          <h2 className="block-h">A few true things</h2>
          <ul className="notable">
            {PERSONAL.facts.map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </Reveal>
      </div>
      <Contact />
    </main>
  );
}

function NotFound() {
  return (
    <main className="page">
      <div className="wrap notfound">
        <h1>A wild 404 appeared!</h1>
        <p>That path got away. Let's head back to the lab.</p>
        <Link className="btn btn-red" to="/">← Back to the lab</Link>
      </div>
    </main>
  );
}

/* ------------------------------------------------------------------ */
/* APP                                                                 */
/* ------------------------------------------------------------------ */
function AnimatedRoutes() {
  const location = useLocation();
  const reduce = useReducedMotion();
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        className="route-frame"
        initial={reduce ? { opacity: 0 } : { opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={reduce ? { opacity: 0 } : { opacity: 0, y: -8 }}
        transition={{ duration: reduce ? 0.15 : 0.32, ease: EASE_OUT }}
      >
        <Routes location={location}>
          <Route path="/" element={<Home />} />
          <Route path="/professional" element={<Professional />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/personal" element={<Personal />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  );
}

function App() {
  return (
    <TimeProvider>
      <div className="app">
        <Nav />
        <AnimatedRoutes />
      </div>
    </TimeProvider>
  );
}

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
