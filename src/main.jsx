import {
  StrictMode,
  createContext,
  lazy,
  Suspense,
  useCallback,
  useContext,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";
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
import { Menu, X } from "lucide-react";
import "./index.css";

import {
  CONTACT,
  STARTERS,
  INTRO,
  TITLE_ROLE,
  TITLE_PROOF,
} from "./data/index.js";
import { loadTitlePosters, loadTitleVideos } from "./lib/media.js";
import {
  EASE_OUT,
  SeamlessAmbienceVideo,
  RouteFallback,
} from "./shared.jsx";

const Professional = lazy(() => import("./pages/Professional.jsx"));
const Projects = lazy(() => import("./pages/Projects.jsx"));
const Personal = lazy(() => import("./pages/Personal.jsx"));
const NotFound = lazy(() => import("./pages/NotFound.jsx"));

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

function getFocusableElements(container) {
  return Array.from(
    container.querySelectorAll(
      'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
    )
  ).filter((el) => el.offsetParent !== null || el === document.activeElement);
}

function Nav() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const menuId = useId();
  const toggleRef = useRef(null);
  const menuRef = useRef(null);

  const close = useCallback(() => {
    setOpen(false);
    requestAnimationFrame(() => toggleRef.current?.focus());
  }, []);

  const goTitle = (e) => {
    e.preventDefault();
    close();
    navigate("/", { state: { screen: "title", t: Date.now() } });
  };

  useEffect(() => {
    if (!open) return undefined;

    const onKeyDown = (e) => {
      if (e.key === "Escape") {
        e.preventDefault();
        close();
        return;
      }
      if (e.key !== "Tab" || !menuRef.current) return;

      const focusable = getFocusableElements(menuRef.current);
      if (focusable.length === 0) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    document.addEventListener("keydown", onKeyDown);
    const firstLink = menuRef.current?.querySelector("a[href], button:not([disabled])");
    firstLink?.focus();

    return () => document.removeEventListener("keydown", onKeyDown);
  }, [open, close]);

  return (
    <header className="nav">
      <div className="nav-frame">
        <div className="nav-plate nav-plate-head">
          <Link to="/" className="wordmark" onClick={goTitle}>DEREK DINH</Link>
        </div>
        <div className="nav-plate nav-plate-body">
          <div className="nav-lead">
            <button
              ref={toggleRef}
              className="nav-toggle"
              type="button"
              aria-label={open ? "Close menu" : "Open menu"}
              aria-expanded={open}
              aria-controls={menuId}
              onClick={() => setOpen((o) => !o)}
            >
              {open ? <X size={20} /> : <Menu size={20} />}
            </button>
            <DayNightToggle />
          </div>
          <nav
            ref={menuRef}
            id={menuId}
            className={`nav-links ${open ? "open" : ""}`}
            aria-label="Primary"
          >
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

function TitleScreen({ onStart, onSkipIntro }) {
  const reduce = useReducedMotion();
  const { mode } = useTime();
  const night = mode === "night";
  const [posters, setPosters] = useState(null);
  const [videos, setVideos] = useState(null);

  useEffect(() => {
    let cancelled = false;
    loadTitlePosters()
      .then((loaded) => {
        if (!cancelled) setPosters(loaded);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (reduce) return undefined;
    let cancelled = false;
    loadTitleVideos()
      .then((loaded) => {
        if (!cancelled) setVideos(loaded);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [reduce]);

  return (
    <section
      className={`title-screen${reduce ? " reduced" : ""}${night ? " is-night" : " is-day"}`}
    >
      <div className="title-bg-stack" aria-hidden="true">
        {posters ? (
          <>
            <div
              className="title-bg title-bg-still title-bg-day"
              style={{ backgroundImage: `url(${posters.day})` }}
            />
            <div
              className="title-bg title-bg-still title-bg-night"
              style={{ backgroundImage: `url(${posters.night})` }}
            />
          </>
        ) : null}
        {!reduce && videos && posters ? (
          <>
            <SeamlessAmbienceVideo
              className="title-bg-day"
              src={videos.day}
              poster={posters.day}
              active={!night}
            />
            <SeamlessAmbienceVideo
              className="title-bg-night"
              src={videos.night}
              poster={posters.night}
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
        <p className="title-role">{TITLE_ROLE}</p>
        <div className="title-proof" aria-label={`${TITLE_PROOF.n} ${TITLE_PROOF.l}`}>
          <span className="title-proof-n">{TITLE_PROOF.n}</span>
          <span className="title-proof-l">{TITLE_PROOF.l}</span>
        </div>
        <div className="title-actions">
          <button className="title-press btn-pop" onClick={onStart}>
            Press Start
          </button>
          <button type="button" className="title-skip btn-pop" onClick={onSkipIntro}>
            Skip intro — choose a starter
          </button>
        </div>
      </div>
    </section>
  );
}

const STARTER_CHOOSE_MS = 520;

function StarterSelect() {
  const [choosing, setChoosing] = useState(null);
  const reduce = useReducedMotion();
  const navigate = useNavigate();
  const timers = useRef([]);

  useEffect(() => {
    STARTERS.forEach((s) => {
      s.loadImg().then((mod) => {
        const img = new Image();
        img.src = mod.default;
      });
    });
    const pending = timers.current;
    return () => {
      pending.forEach(clearTimeout);
    };
  }, []);

  const choose = (slug) => {
    if (choosing) return;
    if (reduce) {
      navigate(`/${slug}`);
      return;
    }
    setChoosing(slug);
    const t = setTimeout(() => navigate(`/${slug}`), STARTER_CHOOSE_MS);
    timers.current.push(t);
  };

  return (
    <section className="select-stage">
      <h1 className="select-title">Choose a starter</h1>
      <p className="select-sub">One tap sends you there. You can catch all three.</p>
      <div className="starter-grid">
        {STARTERS.map((s) => {
          const active = choosing === s.slug;
          const locked = choosing && !active;
          return (
            <div
              key={s.slug}
              className={`starter-card theme-${s.theme} closed${
                active ? " choosing" : ""
              }${locked ? " locked" : ""}`}
            >
              <button
                type="button"
                className={`pokeball-btn${active ? " wobbling" : ""}`}
                onClick={() => choose(s.slug)}
                disabled={!!choosing}
                aria-label={`Choose ${s.name}, the ${s.type}-type starter`}
              >
                <span className="pokeball" aria-hidden="true" />
                {active ? <span className="pokeball-burst" aria-hidden="true" /> : null}
                <span className="pokeball-hint">{s.name}</span>
                <span className="pokeball-blurb">{s.blurb}</span>
              </button>
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
            <button type="button" className="btn btn-ghost btn-pop intro-skip" onClick={onSkip}>
              Skip to starters
            </button>
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
  const [scene, setScene] = useState("title");
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
            <TitleScreen
              onStart={() => setScene("intro")}
              onSkipIntro={() => setScene("select")}
            />
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
        <Suspense fallback={<RouteFallback />}>
          <Routes location={location}>
            <Route path="/" element={<Home />} />
            <Route path="/professional" element={<Professional />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/personal" element={<Personal />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
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
