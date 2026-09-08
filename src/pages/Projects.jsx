import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { STARTERS, PROJECTS, CONTACT, groupTech } from "../data/index.js";
import { PageHero, Reveal, Contact } from "../shared.jsx";

const AUTO_MS = 3500;

function useProjectShot(project) {
  const [shot, setShot] = useState(null);

  useEffect(() => {
    if (!project?.loadScreenshot) {
      setShot(null);
      return undefined;
    }
    let cancelled = false;
    project
      .loadScreenshot()
      .then((mod) => {
        if (!cancelled) setShot(mod.default);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [project]);

  return shot;
}

function AppCarousel({
  projects,
  index,
  onIndexChange,
  autoplay,
  onArrowNav,
}) {
  const reduce = useReducedMotion();
  const [dir, setDir] = useState(0);
  const [hoverPause, setHoverPause] = useState(false);
  const touchX = useRef(null);
  const rootRef = useRef(null);
  const count = projects.length;
  const current = projects[index] ?? null;
  const shot = useProjectShot(current);
  const shouldAuto = autoplay && !reduce && !hoverPause && count > 1;

  const go = useCallback(
    (next, direction, { fromArrow = false } = {}) => {
      if (count < 2) return;
      const nextIndex = ((next % count) + count) % count;
      setDir(direction);
      onIndexChange(nextIndex);
      if (fromArrow) onArrowNav?.();
    },
    [count, onIndexChange, onArrowNav]
  );

  const prev = useCallback(() => go(index - 1, -1, { fromArrow: true }), [go, index]);
  const next = useCallback(() => go(index + 1, 1, { fromArrow: true }), [go, index]);

  useEffect(() => {
    if (!shouldAuto) return undefined;
    const id = setInterval(() => {
      setDir(1);
      onIndexChange((index + 1) % count);
    }, AUTO_MS);
    return () => clearInterval(id);
  }, [shouldAuto, count, index, onIndexChange]);

  if (!current) return null;

  const slide = reduce
    ? { initial: false, animate: { opacity: 1 }, exit: { opacity: 0 } }
    : {
        initial: { opacity: 0, x: dir >= 0 ? 36 : -36 },
        animate: { opacity: 1, x: 0 },
        exit: { opacity: 0, x: dir >= 0 ? -36 : 36 },
      };

  return (
    <div
      ref={rootRef}
      id="app-carousel"
      className="app-carousel"
      role="region"
      aria-roledescription="carousel"
      aria-label="App screenshots"
      tabIndex={0}
      onMouseEnter={() => setHoverPause(true)}
      onMouseLeave={() => setHoverPause(false)}
      onFocus={() => setHoverPause(true)}
      onBlur={(e) => {
        if (!e.currentTarget.contains(e.relatedTarget)) setHoverPause(false);
      }}
      onKeyDown={(e) => {
        if (count < 2) return;
        if (e.key === "ArrowLeft") {
          e.preventDefault();
          prev();
        }
        if (e.key === "ArrowRight") {
          e.preventDefault();
          next();
        }
      }}
      onTouchStart={(e) => {
        touchX.current = e.changedTouches[0]?.clientX ?? null;
      }}
      onTouchEnd={(e) => {
        if (touchX.current == null) return;
        const dx = (e.changedTouches[0]?.clientX ?? touchX.current) - touchX.current;
        touchX.current = null;
        if (Math.abs(dx) < 40) return;
        if (dx > 0) prev();
        else next();
      }}
    >
      <div className="app-carousel-stage">
        <AnimatePresence mode="wait" custom={dir}>
          <motion.div
            key={current.name}
            className="app-carousel-slide"
            initial={slide.initial}
            animate={slide.animate}
            exit={slide.exit}
            transition={{ duration: reduce ? 0 : 0.28, ease: "easeOut" }}
          >
            {shot ? (
              <img
                className="app-carousel-shot"
                src={shot}
                alt={`Screenshot of ${current.name}`}
                width={1280}
                height={800}
              />
            ) : (
              <div className="app-carousel-placeholder" aria-hidden="true" />
            )}
          </motion.div>
        </AnimatePresence>

        {count > 1 ? (
          <>
            <button type="button" className="app-carousel-nav prev" onClick={prev} aria-label="Previous app">
              <ChevronLeft size={22} strokeWidth={2.4} aria-hidden="true" />
            </button>
            <button type="button" className="app-carousel-nav next" onClick={next} aria-label="Next app">
              <ChevronRight size={22} strokeWidth={2.4} aria-hidden="true" />
            </button>
          </>
        ) : null}
      </div>

      <div className="app-carousel-meta">
        <div className="app-carousel-copy">
          <h3 className="app-carousel-name">{current.name}</h3>
          <p className="app-carousel-what">{current.what}</p>
        </div>
        <div className="app-carousel-links">
          <a
            className="app-carousel-link"
            href={current.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            Link →
          </a>
          {current.moreLinks?.map((link) => (
            <a
              key={link.url}
              className="app-carousel-link app-carousel-link-alt"
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              {link.label} →
            </a>
          ))}
        </div>
      </div>

      {count > 1 ? (
        <div className="app-carousel-dots" role="tablist" aria-label="Choose app">
          {projects.map((p, i) => (
            <button
              key={p.name}
              type="button"
              role="tab"
              className="app-carousel-dot"
              aria-selected={i === index}
              aria-label={p.name}
              onClick={() => go(i, i > index ? 1 : -1)}
            />
          ))}
        </div>
      ) : null}
    </div>
  );
}

function ProjectCard({ p, delay, active, onSelectShot }) {
  const hasShot = typeof p.loadScreenshot === "function";

  return (
    <Reveal
      className={`proj-card ignite${hasShot ? " proj-card-shot" : ""}${active ? " is-active" : ""}`}
      as="article"
      preset="spark"
      delay={delay}
      onClick={hasShot ? () => onSelectShot?.(p) : undefined}
    >
      <h3 className="proj-name">{p.name}</h3>
      <p className="proj-what">{p.what}</p>
      <p className="proj-problem">{p.problem}</p>
      <p className="proj-outcome">{p.outcome}</p>
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
        {p.builtWith?.length ? (
          <div className="proj-tech-group">
            <span className="proj-tech-label">Built with</span>
            <ul className="chips">
              {p.builtWith.map((t) => (
                <li className="chip chip-ai" key={t}>{t}</li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>
      <div className="proj-links">
        {hasShot ? (
          <button
            type="button"
            className="proj-show-shot"
            aria-pressed={active}
            onClick={(e) => {
              e.stopPropagation();
              onSelectShot?.(p);
            }}
          >
            Show shot
          </button>
        ) : null}
        <a
          href={p.url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
        >
          Link →
        </a>
        {p.moreLinks?.map((link) => (
          <a
            key={link.url}
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
          >
            {link.label} →
          </a>
        ))}
      </div>
    </Reveal>
  );
}

export default function Projects() {
  const starter = STARTERS[1];
  const [mascotLoop, setMascotLoop] = useState("hi");
  const [carouselIndex, setCarouselIndex] = useState(0);
  const [autoplay, setAutoplay] = useState(true);
  const hiTimer = useRef(null);

  useEffect(() => {
    const t = setTimeout(() => setMascotLoop("idle"), 2000);
    return () => {
      clearTimeout(t);
      if (hiTimer.current) clearTimeout(hiTimer.current);
    };
  }, []);

  const featured = useMemo(() => PROJECTS.find((p) => p.featured), []);
  const rest = useMemo(() => PROJECTS.filter((p) => p !== featured), [featured]);
  const carouselProjects = useMemo(
    () => rest.filter((p) => typeof p.loadScreenshot === "function"),
    [rest]
  );

  const activeName = carouselProjects[carouselIndex]?.name;

  const selectFromCard = useCallback(
    (project) => {
      const i = carouselProjects.findIndex((p) => p.name === project.name);
      if (i < 0) return;
      setCarouselIndex(i);
      setAutoplay(false);
      document.getElementById("app-carousel")?.scrollIntoView({ behavior: "smooth", block: "center" });
    },
    [carouselProjects]
  );

  const resumeAutoplay = useCallback(() => setAutoplay(true), []);

  const onMascotActivate = useCallback(() => {
    setMascotLoop("hi");
    if (hiTimer.current) clearTimeout(hiTimer.current);
    hiTimer.current = setTimeout(() => setMascotLoop("idle"), 1200);
  }, []);

  return (
    <main className="page theme-fire">
      <PageHero
        starter={starter}
        variant="workbench"
        mascotLoop={mascotLoop}
        mascotHref={CONTACT.github}
        mascotTarget="_blank"
        mascotRel="noopener noreferrer"
        mascotLabel={`Open ${starter.name}'s GitHub`}
        onMascotActivate={onMascotActivate}
        speech={{
          name: starter.name.toUpperCase(),
          text: "Tap me to visit my GitHub!",
          hint: true,
          key: "hint-github",
        }}
      />
      <div className="wrap">
        {featured ? (
          <Reveal className="block" as="section" preset="spark">
            <h2 className="block-h">Featured build</h2>
            <div className="proj-featured-wrap">
              <ProjectCard p={featured} delay={0} />
            </div>
          </Reveal>
        ) : null}

        <Reveal className="block" as="section" preset="spark">
          <h2 className="block-h">Caught apps</h2>
          <p className="block-sub">Things I build after hours. Grab one off the shelf.</p>

          {carouselProjects.length ? (
            <AppCarousel
              projects={carouselProjects}
              index={carouselIndex}
              onIndexChange={setCarouselIndex}
              autoplay={autoplay}
              onArrowNav={resumeAutoplay}
            />
          ) : null}

          <div className="proj-grid">
            {rest.map((p, i) => (
              <ProjectCard
                p={p}
                key={p.name}
                delay={i * 0.06}
                active={p.name === activeName}
                onSelectShot={selectFromCard}
              />
            ))}
          </div>
        </Reveal>
      </div>
      <Contact variant="projects" />
    </main>
  );
}
