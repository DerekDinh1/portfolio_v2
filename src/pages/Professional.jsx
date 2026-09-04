import {
  STARTERS,
  STATS,
  PROFESSIONAL_THROUGLINE,
  FOCUS,
  EXPERIENCE,
  SKILLS,
  EDUCATION,
} from "../data/index.js";
import { PageHero, Reveal, Contact, ExpRow } from "../shared.jsx";

export default function Professional() {
  const starter = STARTERS[0];
  return (
    <main className="page theme-water">
      <PageHero starter={starter} />
      <div className="wrap">
        <Reveal className="career-throughline" as="section">
          <p>{PROFESSIONAL_THROUGLINE}</p>
        </Reveal>

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
              <ExpRow job={e} key={e.org} delay={i * 0.05} />
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
