import { useEffect, useMemo, useState } from "react";
import { STARTERS, PROJECTS, groupTech } from "../data/index.js";
import { PageHero, Reveal, Contact } from "../shared.jsx";

const FILTERS = [
  { key: "all", label: "All" },
  { key: "live", label: "Live" },
  { key: "source", label: "Source" },
];

function ProjectCard({ p, delay, featured = false }) {
  const [shot, setShot] = useState(null);

  useEffect(() => {
    if (!p.loadScreenshot) {
      setShot(null);
      return undefined;
    }
    let cancelled = false;
    p.loadScreenshot()
      .then((mod) => {
        if (!cancelled) setShot(mod.default);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [p]);

  return (
    <Reveal
      className={`proj-card${featured ? " proj-featured" : ""} ignite`}
      as="article"
      preset="spark"
      delay={delay}
    >
      <span className={`proj-stamp proj-stamp-${p.status}`}>{p.status === "source" ? "SOURCE" : "LIVE"}</span>
      {shot ? (
        <img className="proj-screenshot" src={shot} alt="" width={800} height={500} loading="lazy" />
      ) : null}
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
        <a href={p.url} target="_blank" rel="noopener noreferrer">
          {p.linkType === "source" ? "Source" : "Live"} →
        </a>
      </div>
    </Reveal>
  );
}

export default function Projects() {
  const starter = STARTERS[1];
  const [mascotLoop, setMascotLoop] = useState("hi");
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    const t = setTimeout(() => setMascotLoop("idle"), 2000);
    return () => clearTimeout(t);
  }, []);

  const featured = useMemo(() => PROJECTS.find((p) => p.featured), []);
  const rest = useMemo(
    () =>
      PROJECTS.filter((p) => p !== featured).filter((p) => (filter === "all" ? true : p.status === filter)),
    [featured, filter]
  );

  return (
    <main className="page theme-fire">
      <PageHero starter={starter} variant="workbench" mascotLoop={mascotLoop} />
      <div className="wrap">
        {featured ? (
          <Reveal className="block" as="section" preset="spark">
            <h2 className="block-h">Featured build</h2>
            <ProjectCard p={featured} delay={0} featured />
          </Reveal>
        ) : null}

        <Reveal className="block" as="section" preset="spark">
          <h2 className="block-h">Caught apps</h2>
          <p className="block-sub">Things I build after hours. Grab one off the shelf.</p>
          <div className="proj-filter" role="group" aria-label="Filter projects">
            {FILTERS.map((f) => (
              <button
                key={f.key}
                type="button"
                className="proj-filter-btn"
                aria-pressed={filter === f.key}
                onClick={() => setFilter(f.key)}
              >
                {f.label}
              </button>
            ))}
          </div>
          <div className="proj-grid">
            {rest.map((p, i) => (
              <ProjectCard p={p} key={p.name} delay={i * 0.06} />
            ))}
          </div>
        </Reveal>
      </div>
      <Contact variant="projects" />
    </main>
  );
}
