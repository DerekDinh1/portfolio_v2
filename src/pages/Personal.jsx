import { STARTERS, PERSONAL } from "../data/index.js";
import { PageHero, Reveal, Contact } from "../shared.jsx";

export default function Personal() {
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
