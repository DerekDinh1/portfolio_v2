import { useEffect, useRef } from "react";
import {
  STARTERS,
  PROFESSIONAL_THROUGLINE,
  FOCUS,
  EXPERIENCE,
  EARLIER_EXPERIENCE,
  SKILLS,
  EDUCATION,
  RESUME_PDF,
  CONTACT,
} from "../data/index.js";
import { Reveal, Contact, ExpRow, ExpRail, StatBars } from "../shared.jsx";
import BattleHero from "../game/BattleHero.jsx";

export default function Professional() {
  const starter = STARTERS[0];
  const { battle } = starter;
  const heroRef = useRef(null);
  const expSectionRef = useRef(null);

  const menu = [
    { key: "resume", label: "RÉSUMÉ", ariaLabel: "Download résumé", href: RESUME_PDF, download: true, play: "action" },
    { key: "experience", label: "EXPERIENCE", scrollTo: "experience" },
    { key: "skills", label: "SKILLS", scrollTo: "skills" },
    { key: "contact", label: "CONTACT", ariaLabel: "Contact on LinkedIn (opens in a new tab)", href: CONTACT.linkedin, newTab: true },
  ];

  // Greet once when the experience section first scrolls into view.
  useEffect(() => {
    const el = expSectionRef.current;
    if (!el || typeof IntersectionObserver === "undefined") return undefined;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          heroRef.current?.play("greet");
          observer.disconnect();
        }
      },
      { threshold: 0.35 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <main className="page theme-water">
      <BattleHero
        ref={heroRef}
        starter={starter}
        habitat={battle.habitat}
        sprite={battle.sprite}
        level={battle.level}
        bar={battle.bar}
        status={battle.status}
        message={battle.message}
        greetMessage={battle.greetMessage}
        menu={menu}
      />
      <div className="wrap">
        <Reveal className="career-throughline" as="section" preset="flow">
          <p className="career-tagline">{starter.tagline}</p>
          <p>{PROFESSIONAL_THROUGLINE}</p>
        </Reveal>

        <Reveal className="block" as="section" preset="flow">
          <h2 className="block-h">By the numbers</h2>
          <StatBars />
        </Reveal>

        <Reveal className="block" as="section" preset="flow">
          <h2 className="block-h">What I'm focused on</h2>
          <ul className="notable">
            {FOCUS.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>
        </Reveal>

        <Reveal className="block" as="section" preset="flow" id="experience">
          <div ref={expSectionRef}>
            <h2 className="block-h">Experience</h2>
            <ExpRail>
              {EXPERIENCE.map((e, i) => (
                <ExpRow job={e} key={e.org} delay={i * 0.05} latest={i === 0} preset="flow" />
              ))}
            </ExpRail>

            <h3 className="exp-earlier-h">Earlier experience</h3>
            <ul className="exp-earlier">
              {EARLIER_EXPERIENCE.map((e) => (
                <li key={e.org} className="exp-earlier-row">
                  <span className="exp-earlier-org">{e.org}</span>
                  <span className="exp-earlier-role">{e.role}</span>
                  <span className="exp-earlier-when">{e.when}</span>
                </li>
              ))}
            </ul>
          </div>
        </Reveal>

        <Reveal className="block" as="section" preset="flow" id="skills">
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

        <Reveal className="block" as="section" preset="flow">
          <h2 className="block-h">Education</h2>
          {EDUCATION.map((e) => (
            <div className="edu" key={e.school}>
              <div className="edu-head">
                <div className="edu-school">{e.school}</div>
                <span className="exp-when">{e.year}</span>
              </div>
              <div className="edu-degree">{e.degree}</div>
              {e.minors ? <div className="edu-minors">{e.minors}</div> : null}
            </div>
          ))}
        </Reveal>
      </div>
      <Contact variant="professional" />
    </main>
  );
}
