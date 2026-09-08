import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "motion/react";
import { STARTERS, PERSONAL, RECS, RECOMMENDATIONS } from "../data/index.js";
import { PageHero, Reveal, Contact } from "../shared.jsx";

function shuffleIndices(length, avoidFirst = null) {
  const indices = Array.from({ length }, (_, i) => i);
  for (let i = indices.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [indices[i], indices[j]] = [indices[j], indices[i]];
  }
  if (
    avoidFirst != null &&
    indices.length > 1 &&
    indices[0] === avoidFirst
  ) {
    const swapWith = 1 + Math.floor(Math.random() * (indices.length - 1));
    [indices[0], indices[swapWith]] = [indices[swapWith], indices[0]];
  }
  return indices;
}

export default function Personal() {
  const starter = STARTERS[2];
  const reduce = useReducedMotion();
  const [recIndex, setRecIndex] = useState(null);
  const [typed, setTyped] = useState("");
  const [mascotLoop, setMascotLoop] = useState("idle");
  const typeTimer = useRef(null);
  const mascotTimer = useRef(null);
  const deckRef = useRef([]);

  useEffect(() => {
    return () => {
      if (typeTimer.current) clearInterval(typeTimer.current);
      if (mascotTimer.current) clearTimeout(mascotTimer.current);
    };
  }, []);

  const nextRecIndex = () => {
    if (deckRef.current.length === 0) {
      deckRef.current = shuffleIndices(RECS.length, recIndex);
    }
    return deckRef.current.shift();
  };

  const giveRec = () => {
    const idx = nextRecIndex();
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
  const speech = currentRec
    ? {
        name: starter.name.toUpperCase(),
        kind: currentRec.kind,
        text: typed,
        caret: typed.length < currentRec.text.length,
        key: `rec-${recIndex}`,
      }
    : {
        name: starter.name.toUpperCase(),
        text: "Tap me for a recommendation!",
        hint: true,
        key: "hint-rec",
      };

  return (
    <main className="page theme-grass">
      <PageHero
        starter={starter}
        variant="card"
        mascotLoop={mascotLoop}
        onMascotActivate={onMascotActivate}
        mascotLabel={`Ask ${starter.name} for a recommendation`}
        speech={speech}
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
          <h2 className="block-h">Recommendations</h2>
          <p className="block-sub">
            Stuff I'd actually hand you. Tap {starter.name} above for a random pick.
          </p>
          <div className="rec-groups">
            {RECOMMENDATIONS.map((group, gi) => (
              <Reveal className="rec-group" key={group.kind} delay={gi * 0.05} preset="sway">
                <h3 className="rec-group-h">{group.kind}</h3>
                <ul className="rec-list">
                  {group.items.map((item) => (
                    <li key={item.name}>
                      <span className="rec-item-name">{item.name}</span>
                      <span className="rec-item-blurb">{item.blurb}</span>
                    </li>
                  ))}
                </ul>
              </Reveal>
            ))}
          </div>
        </Reveal>
      </div>
      <Contact variant="personal" />
    </main>
  );
}
