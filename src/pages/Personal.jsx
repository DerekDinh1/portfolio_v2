import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "motion/react";
import { STARTERS, PERSONAL, RECS } from "../data/index.js";
import { PageHero, Reveal, Contact } from "../shared.jsx";

function pickRecIndex(exclude) {
  if (RECS.length <= 1) return 0;
  let next = Math.floor(Math.random() * RECS.length);
  while (next === exclude) next = Math.floor(Math.random() * RECS.length);
  return next;
}

export default function Personal() {
  const starter = STARTERS[2];
  const reduce = useReducedMotion();
  const [recIndex, setRecIndex] = useState(null);
  const [typed, setTyped] = useState("");
  const [mascotLoop, setMascotLoop] = useState("idle");
  const typeTimer = useRef(null);
  const mascotTimer = useRef(null);

  useEffect(() => {
    return () => {
      if (typeTimer.current) clearInterval(typeTimer.current);
      if (mascotTimer.current) clearTimeout(mascotTimer.current);
    };
  }, []);

  const giveRec = () => {
    const idx = pickRecIndex(recIndex);
    setRecIndex(idx);
    const line = RECS[idx].text;

    if (typeTimer.current) clearInterval(typeTimer.current);

    if (reduce) {
      setTyped(line);
      return;
    }

    setTyped("");
    let i = 0;
    typeTimer.current = setInterval(() => {
      i += 1;
      setTyped(line.slice(0, i));
      if (i >= line.length) clearInterval(typeTimer.current);
    }, 24);
  };

  const onMascotActivate = () => {
    giveRec();
    if (!reduce) {
      setMascotLoop("hi");
      if (mascotTimer.current) clearTimeout(mascotTimer.current);
      mascotTimer.current = setTimeout(() => setMascotLoop("idle"), 1200);
    }
  };

  const currentRec = recIndex !== null ? RECS[recIndex] : null;

  return (
    <main className="page theme-grass">
      <PageHero
        starter={starter}
        variant="card"
        mascotLoop={mascotLoop}
        onMascotActivate={onMascotActivate}
      >
        <div className="badge-case" aria-label="Badge case">
          {PERSONAL.badges.map((b) => {
            const Icon = b.Icon;
            return (
              <span className="badge-case-icon" key={b.h} title={b.h}>
                <Icon size={18} strokeWidth={2} />
              </span>
            );
          })}
        </div>
      </PageHero>
      <div className="wrap">
        <Reveal className="block" as="section" preset="sway">
          <p className="fun-intro">{PERSONAL.intro}</p>
          <div className="badges">
            {PERSONAL.badges.map((b, i) => {
              const Icon = b.Icon;
              return (
                <Reveal className="badge" key={b.h} delay={i * 0.05} preset="sway">
                  <span className="badge-icon" aria-hidden="true"><Icon size={28} strokeWidth={2} /></span>
                  <h3>{b.h}</h3>
                  <p>{b.p}</p>
                </Reveal>
              );
            })}
          </div>
        </Reveal>

        <Reveal className="block" as="section" preset="sway">
          <h2 className="block-h">A few true things</h2>
          <div className="dialogue dialogue-personal">
            <span className="nameplate">DEREK</span>
            <ul className="notable dialogue-facts">
              {PERSONAL.facts.map((f, i) => (
                <li key={i}>{f}</li>
              ))}
            </ul>
          </div>
        </Reveal>

        <Reveal className="block" as="section" preset="sway">
          <h2 className="block-h">Give me a rec</h2>
          <p className="block-sub">Tap the button, or tap {starter.name} above. One recommendation, no strings.</p>
          <div className="rec-box">
            <button type="button" className="btn btn-red btn-pop" onClick={giveRec}>
              Give me a rec
            </button>
            {currentRec ? (
              <p className="rec-text">
                <span className="rec-kind">{currentRec.kind}</span> {typed}
                {typed.length < currentRec.text.length ? (
                  <span className="type-caret" aria-hidden="true">▌</span>
                ) : null}
              </p>
            ) : null}
          </div>
        </Reveal>
      </div>
      <Contact variant="personal" />
    </main>
  );
}
