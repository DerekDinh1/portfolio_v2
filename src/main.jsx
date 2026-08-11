import { StrictMode, useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  NavLink,
  useLocation,
} from "react-router-dom";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import "./index.css";

import resumon from "./assets/mascots/resumon.jpg";
import buildasaur from "./assets/mascots/buildasaur.jpg";
import vibeon from "./assets/mascots/vibeon.jpg";
import titleBg from "./assets/title-bg.jpg";
import cloudA from "./assets/layers/cloud-a.png";
import cloudB from "./assets/layers/cloud-b.png";
import grassLayer from "./assets/layers/grass.png";
import treeSprite from "./assets/layers/tree.png";
import { Tv, BookOpen, Clapperboard, Gamepad2, Flag, Mountain, Menu, X } from "lucide-react";

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
      "Built a Console AI agent into our Slack help channel that handles about 79% of requests through automated resolutions and escalations.",
      "Stood up agentic AI models across departments using Console, ChatGPT, and Claude.",
      "Ran technology integration and migration during an acquisition, coordinating across teams to keep things running.",
    ],
  },
  {
    org: "Valtech (formerly Kin+Carta)",
    role: "Senior IT Support Specialist",
    when: "Jun 2023 to Feb 2025",
    points: [
      "Delivered IT initiatives tied to company goals and hit 100% of targeted deliverables.",
      "Put security and operational practices in place through risk assessments, maintenance, and end-user education.",
      "Mentored junior support staff and pushed knowledge sharing across the team.",
    ],
  },
  {
    org: "Handshake",
    role: "IT Support Engineer",
    when: "Apr 2022 to May 2023",
    points: [
      "Cut ticket resolution times by 60% and raised documentation accuracy by 70%.",
      "Designed automated Okta workflows that improved efficiency and user experience by 50%.",
      "Managed 300+ Apple endpoints with Jamf Pro at a 95% uptime rate.",
    ],
  },
  {
    org: "Red Canary",
    role: "IT Support Admin",
    when: "Apr 2021 to Apr 2022",
    points: [
      "Led an A3/lean process-improvement team that made end-user onboarding 90% better.",
      "Built Zendesk and Slack workflows that improved response times by 30%.",
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
  { name: "Between Us", tagline: "A two-player card game.", tech: ["HTML", "JS"], url: "https://derekdinh1.github.io/betweenus/" },
  { name: "Laminar Focus", tagline: "A focus coach for deep-work sessions.", tech: ["JavaScript"], url: "https://laminarfocus.com" },
  { name: "Dayview", tagline: "A daily brief with live weather.", tech: ["JavaScript"], url: "https://derekdinh1.github.io/dayview/" },
  { name: "Auction War Room", tagline: "A fantasy football draft tracker.", tech: ["JavaScript"], url: "https://derekdinh1.github.io/auction-war-room/" },
  { name: "TradesXP", tagline: "A trading journal for building discipline.", tech: ["JavaScript"], url: "https://tradesxp.com" },
];

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
  const close = () => setOpen(false);
  return (
    <header className="nav">
      <div className="nav-inner">
        <Link to="/" className="wordmark" onClick={close}>DEREK DINH</Link>
        <button
          className="nav-toggle"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
          onClick={() => setOpen((o) => !o)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
        <nav className={`nav-links ${open ? "open" : ""}`} aria-label="Primary">
          <NavLink to="/professional" onClick={close} className={({ isActive }) => (isActive ? "on" : "")}>Professional</NavLink>
          <NavLink to="/projects" onClick={close} className={({ isActive }) => (isActive ? "on" : "")}>Projects</NavLink>
          <NavLink to="/personal" onClick={close} className={({ isActive }) => (isActive ? "on" : "")}>Personal</NavLink>
          <a className="btn btn-red" href={CONTACT.linkedin} target="_blank" rel="noopener noreferrer" onClick={close}>Get in touch</a>
        </nav>
      </div>
    </header>
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
        <div className="hero-orb" />
        <img className="hero-mascot" src={starter.img} alt={`${starter.name}, the ${starter.type}-type starter`} />
      </motion.div>
    </section>
  );
}

function Contact() {
  return (
    <footer className="contact">
      <h2>Get in touch</h2>
      <p>Recruiters, collaborators, or anyone with a movie recommendation. Find me here.</p>
      <div className="contact-links">
        <a className="btn btn-red" href={CONTACT.linkedin} target="_blank" rel="noopener noreferrer">LinkedIn</a>
        <a className="btn btn-ghost" href={CONTACT.github} target="_blank" rel="noopener noreferrer">GitHub</a>
      </div>
      <Link to="/" className="back-lab">← Back to the lab</Link>
    </footer>
  );
}

/* ------------------------------------------------------------------ */
/* HOME (title screen -> intro dialogue -> starter select)             */
/* ------------------------------------------------------------------ */
function TitleScreen({ onStart, exiting }) {
  const reduce = useReducedMotion();
  return (
    <section
      className={`title-screen${exiting ? " exiting" : ""}${reduce ? " reduced" : ""}`}
      style={{ backgroundImage: `url(${titleBg})` }}
    >
      <div className="title-parallax" aria-hidden="true">
        <img className="title-cloud c1" src={cloudA} alt="" />
        <img className="title-cloud c2" src={cloudB} alt="" />
        <img className="title-cloud c3" src={cloudA} alt="" />
        <img className="title-tree t1" src={treeSprite} alt="" />
        <img className="title-tree t2" src={treeSprite} alt="" />
        <img className="title-tree t3" src={treeSprite} alt="" />
        <img className="title-grass g1" src={grassLayer} alt="" />
        <img className="title-grass g2" src={grassLayer} alt="" />
      </div>
      <div className="title-inner">
        <p className="title-region">Colorado Region</p>
        <h1 className="title-name">DEREK DINH</h1>
        <button className="title-press btn-pop" onClick={onStart} disabled={exiting}>
          Press Start
        </button>
      </div>
      {exiting ? <div className="title-flash" aria-hidden="true" /> : null}
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
    }, 1280);
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
              {open ? (
                <>
                  <div className="starter-orb" />
                  <img className="starter-img" src={s.img} alt={s.name} />
                  <span className="starter-dex">{s.dex} · {s.type}</span>
                  <h2 className="starter-name">{s.name}</h2>
                  <p className="starter-blurb">{s.blurb}</p>
                  <Link to={`/${s.slug}`} className="starter-cta">Choose {s.name} →</Link>
                </>
              ) : popping ? (
                <div className="starter-popout" aria-live="polite">
                  <span className="pokeball pokeball-fade" aria-hidden="true" />
                  <span className="pokeball-burst" aria-hidden="true" />
                  <img className="starter-emerge" src={s.img} alt={s.name} />
                </div>
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
                <span className="next-arrow bounce" aria-hidden="true">▼</span>
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
  const [exitingTitle, setExitingTitle] = useState(false);
  const reduce = useReducedMotion();

  const startFromTitle = () => {
    if (exitingTitle) return;
    if (reduce) {
      setScene("intro");
      return;
    }
    setExitingTitle(true);
    window.setTimeout(() => setScene("intro"), 520);
  };

  return (
    <main className="home">
      <AnimatePresence mode="wait">
        {scene === "title" ? (
          <motion.div
            key="title"
            initial={false}
            exit={reduce ? { opacity: 0 } : { opacity: 0 }}
            transition={{ duration: reduce ? 0.15 : 0.35 }}
          >
            <TitleScreen onStart={startFromTitle} exiting={exitingTitle} />
          </motion.div>
        ) : scene === "intro" ? (
          <motion.div
            key="intro"
            initial={reduce ? { opacity: 0 } : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, y: -8 }}
            transition={{ duration: reduce ? 0.2 : 0.4, ease: EASE_OUT }}
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
            initial={reduce ? { opacity: 0 } : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: reduce ? 0.2 : 0.45, ease: EASE_OUT }}
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
                <ul className="chips">
                  {p.tech.map((t) => (
                    <li className="chip" key={t}>{t}</li>
                  ))}
                </ul>
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
    <div className="app">
      <Nav />
      <AnimatedRoutes />
    </div>
  );
}

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
