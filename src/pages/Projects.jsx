import { STARTERS, PROJECTS, groupTech } from "../data/index.js";
import { PageHero, Reveal, Contact } from "../shared.jsx";

export default function Projects() {
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
            ))}
          </div>
        </Reveal>
      </div>
      <Contact />
    </main>
  );
}
