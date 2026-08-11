import { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  NavLink,
} from "react-router-dom";
import "./index.css";

import resumon from "./assets/mascots/resumon.jpg";
import buildasaur from "./assets/mascots/buildasaur.jpg";
import vibeon from "./assets/mascots/vibeon.jpg";
import titleBg from "./assets/title-bg.jpg";
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
  return (
    <section className={`hero theme-${starter.theme}`}>
      <div className="hero-copy">
        <span className="dex">{starter.dex} · {starter.type} type</span>
        <h1 className="hero-name">{starter.name}</h1>
        <p className="hero-tagline">{starter.tagline}</p>
      </div>
      <div className="hero-art">
        <div className="hero-orb" />
        <img src={starter.img} alt={`${starter.name}, the ${starter.type}-type starter`} />
      </div>
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
function TitleScreen({ onStart }) {
  return (
    <section
      className="title-screen"
      style={{ backgroundImage: `url(${titleBg})` }}
    >
      <div className="title-inner">
        <p className="title-region">Colorado Region</p>
        <h1 className="title-name">DEREK DINH</h1>
        <button className="title-press" onClick={onStart}>Press Start</button>
      </div>
    </section>
  );
}

function StarterSelect() {
  const [revealed, setRevealed] = useState({});
  const reveal = (slug) => setRevealed((r) => ({ ...r, [slug]: true }));

  return (
    <section className="select-stage">
      <h1 className="select-title">Choose a starter</h1>
      <p className="select-sub">Tap a Poké Ball to see who's inside. You can catch all three.</p>
      <div className="starter-grid">
        {STARTERS.map((s) => {
          const open = revealed[s.slug];
          return (
            <div key={s.slug} className={`starter-card ${open ? `theme-${s.theme} open` : "closed"}`}>
              {open ? (
                <>
                  <div className="starter-orb" />
                  <img className="starter-img" src={s.img} alt={s.name} />
                  <span className="starter-dex">{s.dex} · {s.type}</span>
                  <h2 className="starter-name">{s.name}</h2>
                  <p className="starter-blurb">{s.blurb}</p>
                  <Link to={`/${s.slug}`} className="starter-cta">Choose {s.name} →</Link>
                </>
              ) : (
                <button className="pokeball-btn" onClick={() => reveal(s.slug)} aria-label={`Open the ${s.slug} Poké Ball`}>
                  <span className="pokeball" aria-hidden="true" />
                  <span className="pokeball-hint">{s.slug.charAt(0).toUpperCase() + s.slug.slice(1)}</span>
                </button>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}

function Home() {
  const [scene, setScene] = useState("title"); // title | intro | select
  const [step, setStep] = useState(0);
  const last = step >= INTRO.length - 1;

  if (scene === "title") {
    return (
      <main className="home">
        <TitleScreen onStart={() => setScene("intro")} />
      </main>
    );
  }

  return (
    <main className="home">
      {scene === "intro" ? (
        <section className="intro-stage">
          <div className="dialogue">
            <span className="nameplate">PROF. DINH</span>
            <p className="dialogue-text">{INTRO[step]}</p>
            <span className="cursor" aria-hidden="true">▼</span>
            <div className="dialogue-controls">
              <button className="btn btn-ghost" onClick={() => setScene("select")}>Skip intro</button>
              {last ? (
                <button className="btn btn-red" onClick={() => setScene("select")}>Choose a starter</button>
              ) : (
                <button className="btn btn-dark" onClick={() => setStep((s) => s + 1)}>Next</button>
              )}
            </div>
          </div>
          <ol className="progress" aria-hidden="true">
            {INTRO.map((_, i) => (
              <li key={i} className={i <= step ? "done" : ""} />
            ))}
          </ol>
        </section>
      ) : (
        <StarterSelect />
      )}
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
          {STATS.map((s) => (
            <div className="stat" key={s.l}>
              <div className="stat-n">{s.n}</div>
              <div className="stat-l">{s.l}</div>
            </div>
          ))}
        </section>

        <section className="block">
          <h2 className="block-h">What I'm focused on</h2>
          <ul className="notable">
            {FOCUS.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>
        </section>

        <section className="block">
          <h2 className="block-h">Experience</h2>
          <ul className="exp">
            {EXPERIENCE.map((e) => (
              <li className="exp-row" key={e.org}>
                <div className="exp-head">
                  <div>
                    <div className="exp-org">{e.org}</div>
                    <div className="exp-role">{e.role}</div>
                  </div>
                  <span className="exp-when">{e.when}</span>
                </div>
                <ul className="exp-points">
                  {e.points.map((p, i) => (
                    <li key={i}>{p}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </section>

        <section className="block">
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
        </section>

        <section className="block">
          <h2 className="block-h">Education</h2>
          <div className="edu">
            <div className="edu-head">
              <div className="edu-school">{EDUCATION.school}</div>
              <span className="exp-when">{EDUCATION.year}</span>
            </div>
            <div className="edu-degree">{EDUCATION.degree}</div>
            <div className="edu-minors">{EDUCATION.minors}</div>
          </div>
        </section>
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
        <section className="block">
          <h2 className="block-h">Caught apps</h2>
          <p className="block-sub">Things I build after hours. Grab one off the shelf.</p>
          <div className="proj-grid">
            {PROJECTS.map((p) => (
              <article className="proj-card" key={p.name}>
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
              </article>
            ))}
          </div>
        </section>
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
        <section className="block">
          <p className="fun-intro">{PERSONAL.intro}</p>
          <div className="badges">
            {PERSONAL.badges.map((b) => {
              const Icon = b.Icon;
              return (
                <div className="badge" key={b.h}>
                  <span className="badge-icon" aria-hidden="true"><Icon size={28} strokeWidth={2} /></span>
                  <h3>{b.h}</h3>
                  <p>{b.p}</p>
                </div>
              );
            })}
          </div>
        </section>

        <section className="block">
          <h2 className="block-h">A few true things</h2>
          <ul className="notable">
            {PERSONAL.facts.map((f, i) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </section>
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
function App() {
  return (
    <div className="app">
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/professional" element={<Professional />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/personal" element={<Personal />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
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
