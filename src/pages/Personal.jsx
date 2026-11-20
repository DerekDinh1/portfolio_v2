import { useRef, useState } from "react";
import { STARTERS, PERSONAL, RECS, RECOMMENDATIONS, CONTACT } from "../data/index.js";
import { Reveal, Contact } from "../shared.jsx";
import BattleHero from "../game/BattleHero.jsx";

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

// Phones only show the first few picks per group; the rest sit behind a toggle
// so the list doesn't run for screens. Wider layouts always show everything.
const REC_PREVIEW = 3;

function RecGroup({ group, delay }) {
  const [expanded, setExpanded] = useState(false);
  const extra = group.items.length - REC_PREVIEW;
  return (
    <Reveal className={`rec-group${expanded ? " expanded" : ""}`} delay={delay} preset="sway">
      <h3 className="rec-group-h">{group.kind}</h3>
      <ul className="rec-list">
        {group.items.map((item, i) => (
          <li key={item.name} className={i >= REC_PREVIEW ? "rec-extra" : undefined}>
            <span className="rec-item-name">{item.name}</span>
            <span className="rec-item-blurb">{item.blurb}</span>
          </li>
        ))}
      </ul>
      {extra > 0 ? (
        <button
          type="button"
          className="exp-more rec-more"
          aria-expanded={expanded}
          onClick={() => setExpanded((v) => !v)}
        >
          {expanded ? "Show less" : `Show more (${extra})`}
        </button>
      ) : null}
    </Reveal>
  );
}

export default function Personal() {
  const starter = STARTERS[2];
  const { battle } = starter;
  const [seen, setSeen] = useState(0);
  const lastRef = useRef(null);
  const deckRef = useRef([]);
  const seenRef = useRef(new Set());

  // Deal picks from a shuffled deck so nothing repeats until every pick has come up.
  const nextPick = () => {
    if (deckRef.current.length === 0) {
      deckRef.current = shuffleIndices(RECS.length, lastRef.current);
    }
    const idx = deckRef.current.shift();
    lastRef.current = idx;
    seenRef.current.add(idx);
    setSeen(seenRef.current.size);
    const rec = RECS[idx];
    return `${rec.kind.toUpperCase()} PICK: ${rec.text}`;
  };

  const menu = [
    { key: "pick", label: "PICK", ariaLabel: "Get a random recommendation", play: "action", onSelect: nextPick },
    { key: "hobbies", label: "HOBBIES", scrollTo: "hobbies" },
    { key: "recs", label: "RECS", ariaLabel: "All recommendations", scrollTo: "recs" },
    { key: "contact", label: "CONTACT", ariaLabel: "Contact on LinkedIn (opens in a new tab)", href: CONTACT.linkedin, newTab: true },
  ];

  return (
    <main className="page theme-grass">
      <BattleHero
        starter={starter}
        habitat={battle.habitat}
        sprite={battle.sprite}
        level={RECS.length}
        bar={{
          label: "EXP",
          value: Math.round((seen / RECS.length) * 100),
          text: `${seen} of ${RECS.length} picks seen this visit`,
        }}
        status={battle.status}
        message={battle.message}
        greetMessage={battle.greetMessage}
        onTap={nextPick}
        menu={menu}
      />
      <div className="wrap">
        <Reveal className="block" as="section" preset="sway" id="hobbies">
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

        <Reveal className="block" as="section" preset="sway" id="recs">
          <h2 className="block-h">Recommendations</h2>
          <p className="block-sub">
            Stuff I'd actually hand you. Tap {starter.name} above for a random pick.
          </p>
          <div className="rec-groups">
            {RECOMMENDATIONS.map((group, gi) => (
              <RecGroup group={group} key={group.kind} delay={gi * 0.05} />
            ))}
          </div>
        </Reveal>
      </div>
      <Contact variant="personal" />
    </main>
  );
}
