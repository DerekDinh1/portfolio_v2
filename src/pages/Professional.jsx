import { useEffect, useRef, useState } from "react";
import {
  STARTERS,
  PROFESSIONAL_THROUGLINE,
  FOCUS,
  EXPERIENCE,
  EARLIER_EXPERIENCE,
  SKILLS,
  EDUCATION,
  RESUME_PDF,
} from "../data/index.js";
import { PageHero, Reveal, Contact, ExpRow, ExpRail, StatBars } from "../shared.jsx";

export default function Professional() {
  const starter = STARTERS[0];
  const [mascotLoop, setMascotLoop] = useState("idle");
  const expSectionRef = useRef(null);
  const greetTimerRef = useRef(null);

  useEffect(() => {
    const el = expSectionRef.current;
    if (!el || typeof IntersectionObserver === "undefined") return undefined;

    let greeted = false;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !greeted) {
          greeted = true;
          setMascotLoop("hi");
          greetTimerRef.current = setTimeout(() => setMascotLoop("idle"), 1400);
        }
      },
      { threshold: 0.35 }
    );
    observer.observe(el);
    return () => {
      observer.disconnect();
      if (greetTimerRef.current) clearTimeout(greetTimerRef.current);
    };
  }, []);

  const onMascotActivate = () => {
    setMascotLoop("hi");
    if (greetTimerRef.current) clearTimeout(greetTimerRef.current);
    greetTimerRef.current = setTimeout(() => setMascotLoop("idle"), 1200);
  };

  return (
    <main className="page theme-water">
      <PageHero
        starter={starter}
        variant="dossier"
        mascotLoop={mascotLoop}
        mascotHref={RESUME_PDF}
        mascotDownload
        mascotLabel={`Download résumé from ${starter.name}`}
        onMascotActivate={onMascotActivate}
        speech={{
          name: starter.name.toUpperCase(),
          text: "Tap me to download my résumé!",
          hint: true,
          key: "hint-resume",
        }}
      >
        <div className="hero-cta-row">
          <span className="availability-chip">
            <span className="availability-dot" aria-hidden="true" />
            Open to senior IT · automation · AI ops
          </span>
        </div>
      </PageHero>
      <div className="wrap">
        <Reveal className="career-throughline" as="section" preset="flow">
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

        <Reveal className="block" as="section" preset="flow">
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

        <Reveal className="block" as="section" preset="flow">
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
      <Contact variant="professional" />
    </main>
  );
}
