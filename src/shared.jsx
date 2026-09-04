import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, useReducedMotion } from "motion/react";
import { CONTACT } from "./data/index.js";
import { EXP_VISIBLE_DEFAULT } from "./data/professional.js";
import { CAN_PLAY_WEBM } from "./lib/media.js";

export const TITLE_AMBIENCE_RATE = 0.45;
export const TITLE_AMBIENCE_CROSSFADE_WALL_S = 1.75;
export const EASE_OUT = [0.22, 1, 0.36, 1];

const MOTION_TAGS = {
  div: motion.div,
  section: motion.section,
  article: motion.article,
  li: motion.li,
};

export function Reveal({ children, className = "", as = "div", delay = 0, ...rest }) {
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

export function MascotSprite({ starter, loop, className, alt }) {
  const reduce = useReducedMotion();
  const [failed, setFailed] = useState(false);
  const [imgSrc, setImgSrc] = useState(null);
  const [videoSrc, setVideoSrc] = useState(null);

  useEffect(() => {
    let cancelled = false;
    starter
      .loadImg()
      .then((mod) => {
        if (!cancelled) setImgSrc(mod.default);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [starter]);

  useEffect(() => {
    if (reduce || !CAN_PLAY_WEBM) return undefined;
    let cancelled = false;
    const loader = loop === "hi" ? starter.loadHi : starter.loadIdle;
    loader()
      .then((mod) => {
        if (!cancelled) setVideoSrc(mod.default);
      })
      .catch(() => {
        if (!cancelled) setFailed(true);
      });
    return () => {
      cancelled = true;
    };
  }, [starter, loop, reduce]);

  if (!imgSrc) {
    return <span className={className} role="img" aria-label={alt} />;
  }

  if (reduce || !videoSrc || failed || !CAN_PLAY_WEBM) {
    return <img className={className} src={imgSrc} alt={alt} loading="lazy" />;
  }

  return (
    <video
      className={className}
      src={videoSrc}
      poster={imgSrc}
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

export function PageHero({ starter }) {
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

export function Contact() {
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

export function ExpRow({ job, delay }) {
  const [expanded, setExpanded] = useState(false);
  const hidden = job.points.length > EXP_VISIBLE_DEFAULT;
  const visiblePoints = expanded ? job.points : job.points.slice(0, EXP_VISIBLE_DEFAULT);

  return (
    <Reveal className="exp-row" as="li" delay={delay}>
      <div className="exp-head">
        <div>
          <div className="exp-org">{job.org}</div>
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

export function RouteFallback() {
  return (
    <div className="route-fallback" aria-busy="true" aria-live="polite">
      Loading…
    </div>
  );
}
