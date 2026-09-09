import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, useReducedMotion, useScroll, useTransform } from "motion/react";
import { CONTACT, CONTACT_BLURB, STATS } from "./data/index.js";
import { EXP_VISIBLE_DEFAULT } from "./data/professional.js";

export const TITLE_AMBIENCE_RATE = 0.45;
export const TITLE_AMBIENCE_CROSSFADE_WALL_S = 1.75;
export const EASE_OUT = [0.22, 1, 0.36, 1];

const MOTION_TAGS = {
  div: motion.div,
  section: motion.section,
  article: motion.article,
  li: motion.li,
};

// Per-habitat motion presets: flow (water), spark (fire), sway (grass).
// Undefined preset keeps the original Reveal feel.
const REVEAL_PRESETS = {
  flow: { duration: 0.7, ease: [0.33, 1, 0.68, 1], y: 10 },
  spark: { duration: 0.32, ease: "easeOut", y: 14, scale: [0.96, 1] },
  sway: { duration: 0.55, ease: EASE_OUT, y: 12, rotate: [-2, 0] },
};

export function Reveal({ children, className = "", as = "div", delay = 0, preset, ...rest }) {
  const reduce = useReducedMotion();
  const Tag = MOTION_TAGS[as] || motion.div;
  const p = preset ? REVEAL_PRESETS[preset] : null;
  const duration = p ? p.duration : 0.45;
  const ease = p ? p.ease : EASE_OUT;
  const y = p ? p.y : 18;

  const initial = reduce
    ? false
    : {
        opacity: 0,
        y,
        ...(p?.scale ? { scale: p.scale[0] } : null),
        ...(p?.rotate ? { rotate: p.rotate[0] } : null),
      };
  const whileInView = reduce
    ? undefined
    : {
        opacity: 1,
        y: 0,
        ...(p?.scale ? { scale: p.scale[1] } : null),
        ...(p?.rotate ? { rotate: p.rotate[1] } : null),
      };

  return (
    <Tag
      className={className}
      initial={initial}
      whileInView={whileInView}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: reduce ? 0 : duration, delay: reduce ? 0 : delay, ease }}
      {...rest}
    >
      {children}
    </Tag>
  );
}

// Tracks html[data-time] so components outside main.jsx's TimeProvider
// (e.g. habitat backdrops) can react to day/night without a circular import.
function useIsNight() {
  const [night, setNight] = useState(
    () => typeof document !== "undefined" && document.documentElement.dataset.time === "night"
  );
  useEffect(() => {
    if (typeof document === "undefined") return undefined;
    const el = document.documentElement;
    const obs = new MutationObserver(() => setNight(el.dataset.time === "night"));
    obs.observe(el, { attributes: true, attributeFilter: ["data-time"] });
    return () => obs.disconnect();
  }, []);
  return night;
}

export function SeamlessAmbienceVideo({ src, poster, className, active }) {
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
    if (!a || !b || !src) return undefined;

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

  if (!src) return null;

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

// loop: "idle" | "hi" | "sleep" (sleep falls back to idle if the starter has no sleep asset)
// Animated WebP loops (true alpha). Magenta-keyed MOV/WebM are not used — Safari
// paints their matte as a solid pink square, and the WebMs are opaque pink too.
export function MascotSprite({ starter, loop = "idle", className, alt, playOnce = false, onEnded }) {
  const reduce = useReducedMotion();
  const [failed, setFailed] = useState(false);
  const [stillSrc, setStillSrc] = useState(null);
  const [animSrc, setAnimSrc] = useState(null);

  const hasSleepAsset = !!starter.loadSleep;
  const effectiveLoop = loop === "sleep" && !hasSleepAsset ? "idle" : loop;

  useEffect(() => {
    let cancelled = false;
    starter
      .loadImg()
      .then((mod) => {
        if (!cancelled) setStillSrc(mod.default);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [starter]);

  useEffect(() => {
    setFailed(false);
    setAnimSrc(null);
    if (reduce) return undefined;

    let cancelled = false;
    const animLoader =
      effectiveLoop === "hi" ? starter.loadHi : effectiveLoop === "sleep" ? starter.loadSleep : starter.loadIdle;

    if (!animLoader) {
      setFailed(true);
      return undefined;
    }

    animLoader()
      .then((mod) => {
        if (cancelled) return;
        if (!mod?.default) {
          setFailed(true);
          return;
        }
        setAnimSrc(mod.default);
      })
      .catch(() => {
        if (!cancelled) setFailed(true);
      });

    return () => {
      cancelled = true;
    };
  }, [starter, effectiveLoop, reduce]);

  useEffect(() => {
    if (!playOnce || !animSrc || reduce || failed) return undefined;
    const t = window.setTimeout(() => {
      if (typeof onEnded === "function") onEnded();
    }, 5200);
    return () => window.clearTimeout(t);
  }, [playOnce, animSrc, reduce, failed, onEnded]);

  if (!stillSrc) {
    return <span className={className} role="img" aria-label={alt} />;
  }

  const src = !reduce && !failed && animSrc ? animSrc : stillSrc;

  return (
    <img
      className={className}
      src={src}
      alt={alt}
      loading="eager"
      decoding="async"
      fetchPriority="high"
      onError={() => setFailed(true)}
    />
  );
}

function HeroSpeech({ speech, reduce }) {
  if (!speech?.text && !speech?.kind) return null;
  const hint = Boolean(speech.hint);
  const typing = Boolean(speech.caret);
  return (
    <motion.div
      className={`hero-speech${hint ? " hero-speech-hint" : ""}`}
      role="status"
      aria-live={typing ? "off" : "polite"}
      aria-atomic="true"
      initial={reduce ? false : { opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: reduce ? 0 : 0.35, ease: EASE_OUT }}
      key={speech.key || speech.kind || "speech"}
    >
      {speech.name ? <span className="hero-speech-name">{speech.name}</span> : null}
      <p className="hero-speech-text">
        {speech.kind ? <span className="rec-kind">{speech.kind}</span> : null}
        {speech.text}
        {typing ? <span className="type-caret" aria-hidden="true">▌</span> : null}
      </p>
    </motion.div>
  );
}

// variant: "dossier" (Professional) | "workbench" (Projects) | "card" (Personal)
export function PageHero({
  starter,
  variant = "dossier",
  mascotLoop = "idle",
  mascotBehavior,
  onMascotActivate,
  mascotHref,
  mascotDownload = false,
  mascotTarget,
  mascotRel,
  mascotLabel,
  speech,
  children,
}) {
  const reduce = useReducedMotion();
  const isNight = useIsNight();
  const [backdropSrc, setBackdropSrc] = useState(null);

  useEffect(() => {
    if (!starter.loadBackdrop) {
      setBackdropSrc(null);
      return undefined;
    }
    let cancelled = false;
    starter
      .loadBackdrop(isNight)
      .then((mod) => {
        if (cancelled) return;
        setBackdropSrc(typeof mod === "string" ? mod : (mod?.default ?? null));
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [starter, isNight]);

  const mascotAlt = `${starter.name}, the ${starter.type}-type starter`;
  const actionLabel = mascotLabel || `Tap ${starter.name}`;
  const mascot = (
    <MascotSprite starter={starter} loop={mascotLoop} className="hero-mascot" alt={mascotAlt} />
  );

  let mascotNode = mascot;
  if (mascotHref) {
    mascotNode = (
      <a
        className="hero-mascot-btn"
        href={mascotHref}
        download={mascotDownload || undefined}
        target={mascotTarget}
        rel={mascotRel}
        aria-label={actionLabel}
        onClick={onMascotActivate}
      >
        {mascot}
      </a>
    );
  } else if (typeof onMascotActivate === "function") {
    mascotNode = (
      <button type="button" className="hero-mascot-btn" onClick={onMascotActivate} aria-label={actionLabel}>
        {mascot}
      </button>
    );
  }

  return (
    <section
      className={`hero hero--${variant} theme-${starter.theme}`}
      data-behavior={mascotBehavior || undefined}
    >
      {backdropSrc ? (
        <div className="hero-backdrop" aria-hidden="true">
          <img src={backdropSrc} alt="" />
        </div>
      ) : null}
      <div className="hero-inner">
        <motion.div
          className="hero-copy"
          initial={reduce ? false : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: reduce ? 0 : 0.5, ease: EASE_OUT }}
        >
          <span className="dex">{starter.dex} · {starter.type} type</span>
          <h1 className="hero-name">{starter.name}</h1>
          <p className="hero-tagline">{starter.tagline}</p>
          {children}
        </motion.div>
        <motion.div
          className="hero-art"
          initial={reduce ? false : { opacity: 0, scale: 0.92 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: reduce ? 0 : 0.55, delay: reduce ? 0 : 0.08, ease: EASE_OUT }}
        >
          <div className="hero-mascot-stage">
            <HeroSpeech speech={speech} reduce={reduce} />
            {mascotNode}
          </div>
        </motion.div>
      </div>
    </section>
  );
}

export function Contact({ variant }) {
  const navigate = useNavigate();
  const blurb =
    (variant && CONTACT_BLURB[variant]) ||
    "Recruiters, collaborators, or anyone with a movie recommendation. Find me here.";
  return (
    <footer className="contact">
      <h2>Get in touch</h2>
      <p>{blurb}</p>
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

export function ExpRow({ job, delay, latest = false, preset }) {
  const [expanded, setExpanded] = useState(false);
  const hidden = job.points.length > EXP_VISIBLE_DEFAULT;
  const visiblePoints = expanded ? job.points : job.points.slice(0, EXP_VISIBLE_DEFAULT);

  return (
    <Reveal className="exp-row" as="li" delay={delay} preset={preset}>
      <div className="exp-head">
        <div>
          <div className="exp-org">
            {job.org}
            {job.stamp ? <span className="exp-latest">{job.stamp}</span> : latest ? <span className="exp-latest">Latest</span> : null}
          </div>
          <div className="exp-role">{job.role}</div>
        </div>
        <span className="exp-when">{job.when}</span>
      </div>
      <ul className="exp-points">
        {visiblePoints.map((p, j) => (
          <li key={j}>{p}</li>
        ))}
      </ul>
      {hidden ? (
        <button
          type="button"
          className="exp-more"
          aria-expanded={expanded}
          onClick={() => setExpanded((v) => !v)}
        >
          {expanded ? "Show less" : `Show more (${job.points.length - EXP_VISIBLE_DEFAULT})`}
        </button>
      ) : null}
    </Reveal>
  );
}

// Prefer an explicit bar % when the label is not a parseable number ("Agentic", "Channels").
function statBarWidth(stat) {
  if (typeof stat.bar === "number") return Math.min(100, Math.max(4, stat.bar));
  const str = String(stat.n);
  const num = parseFloat(str.replace(/[^0-9.]/g, ""));
  if (!Number.isFinite(num)) return 50;
  if (str.includes("%")) return Math.min(100, Math.max(4, num));
  if (num < 100) return Math.min(100, Math.max(4, num * 10));
  return 85;
}

export function StatBars({ stats = STATS, delay = 0 }) {
  const reduce = useReducedMotion();
  return (
    <div className="stat-bars">
      {stats.map((s, i) => (
        <Reveal className="stat-bar-row" key={s.l} delay={delay + i * 0.06}>
          <div className="stat-bar-head">
            <span className="stat-bar-n">{s.n}</span>
            <span className="stat-bar-l">{s.l}</span>
          </div>
          <div className="stat-bar-track">
            <motion.div
              className="stat-bar-fill"
              initial={reduce ? false : { width: "0%" }}
              whileInView={{ width: `${statBarWidth(s)}%` }}
              viewport={{ once: true, amount: 0.4 }}
              transition={{ duration: reduce ? 0 : 0.7, delay: reduce ? 0 : i * 0.08, ease: EASE_OUT }}
            />
          </div>
        </Reveal>
      ))}
    </div>
  );
}

// Wraps an experience list with a left rail whose fill tracks scroll progress
// through the section, giving the timeline a sense of depth as you read down it.
export function ExpRail({ children, className = "exp" }) {
  const ref = useRef(null);
  const reduce = useReducedMotion();
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start 0.85", "end 0.4"],
  });
  const height = useTransform(scrollYProgress, [0, 1], ["0%", "100%"]);

  return (
    <div className="exp-rail" ref={ref}>
      {!reduce ? (
        <div className="exp-rail-track" aria-hidden="true">
          <motion.div className="exp-rail-fill" style={{ height }} />
        </div>
      ) : null}
      <ul className={className}>{children}</ul>
    </div>
  );
}

export function RouteFallback() {
  return (
    <div className="route-fallback" aria-busy="true" aria-live="polite">
      Loading…
    </div>
  );
}
