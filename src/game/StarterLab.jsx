import { useCallback, useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { STARTERS } from "../data/index.js";
import SceneBackdrop from "./SceneBackdrop.jsx";
import SpriteSheet from "./SpriteSheet.jsx";
import usePixelScale from "./usePixelScale.js";
import { TextBox } from "./BattleHero.jsx";
import "./game.css";

const capsuleUrls = import.meta.glob("../assets/sprites/capsules/*.png", {
  eager: true,
  import: "default",
  query: "?url",
});

// Scene coordinates (art pixels) matching tools/scenes/habitats/lab.py.
const SLOTS = [84, 120, 156]; // capsule centres on the table
const CAPSULE_TOP = 63;
const TRAINER_FEET_Y = 67; // just behind the table
const CAPSULE_MOUTH_Y = 69; // where the creature bursts out
const STAGE = { x: 120, y: 100 }; // centre stage: where the creature lands, feet here
const WALK_MS = 420;
const WOBBLE = [1, 0, 2, 0, 1, 0, 2]; // capsule strip frames before it opens
const WOBBLE_MS = 90;

function prefersReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

const px = (n) => `calc(var(--px) * ${n})`;

// Starter select as a lab scene: the professor stands behind a table of three typed
// capsules. Picking one walks him over and opens it; the creature pops out of the capsule
// to centre stage while the lab behind it blurs, with a yes/no prompt. The text-box menu
// offers the same choices as the capsules.
export default function StarterLab() {
  const rootRef = usePixelScale();
  const trainerRef = useRef(null);
  const creatureRef = useRef(null);
  const menuRef = useRef(null);
  const timers = useRef([]);
  const [picked, setPicked] = useState(null);
  const [phase, setPhase] = useState("idle"); // idle | walking | opening | shown
  const [trainerX, setTrainerX] = useState(SLOTS[1]);
  const [capFrame, setCapFrame] = useState(0);
  const [msgKey, setMsgKey] = useState(0);

  const later = (fn, ms) => timers.current.push(window.setTimeout(fn, ms));
  useEffect(() => {
    const pending = timers.current;
    return () => pending.forEach((t) => window.clearTimeout(t));
  }, []);

  const choose = useCallback(
    (i) => {
      if (phase === "walking" || phase === "opening") return;
      setPicked(i);
      setMsgKey((k) => k + 1);
      if (prefersReducedMotion()) {
        setTrainerX(SLOTS[i]);
        setCapFrame(3);
        setPhase("shown");
        return;
      }
      const walk = SLOTS[i] === trainerX ? 0 : WALK_MS;
      setCapFrame(0);
      setPhase("walking");
      if (walk) trainerRef.current?.play(SLOTS[i] < trainerX ? "walk-left" : "walk-right");
      setTrainerX(SLOTS[i]);
      later(() => {
        setPhase("opening");
        trainerRef.current?.play("interact");
        WOBBLE.forEach((f, n) => later(() => setCapFrame(f), n * WOBBLE_MS));
        later(() => {
          setCapFrame(3);
          setPhase("shown");
          setMsgKey((k) => k + 1);
        }, WOBBLE.length * WOBBLE_MS);
      }, walk);
    },
    [phase, trainerX]
  );

  const reset = () => {
    setPicked(null);
    setCapFrame(0);
    setPhase("idle");
    setMsgKey((k) => k + 1);
  };

  // New menu, new starting point for keyboard users.
  useEffect(() => {
    if (phase === "shown") {
      creatureRef.current?.play("greet");
      menuRef.current?.querySelector(".bh-menu-item")?.focus({ preventScroll: true });
    }
  }, [phase]);

  const starter = picked === null ? null : STARTERS[picked];
  const busy = phase === "walking" || phase === "opening";
  const message =
    phase === "shown"
      ? `${starter.name.toUpperCase()}, the ${starter.type} type! ${starter.blurb} Go with ${starter.name.toUpperCase()}?`
      : busy
        ? `PROF. DINH reaches for the ${starter.type} capsule...`
        : "Three capsules rest on the table. Which one will you open?";

  return (
    <section ref={rootRef} className={`bh lab${starter ? ` theme-${starter.theme}` : ""}`}>
      <h1 className="bh-sr">Choose a starter</h1>
      <div className="bh-scene">
        <div className={`lab-stage${phase === "shown" ? " is-showcase" : ""}`}>
        <SceneBackdrop habitat="lab" />
        <div className="bh-safe">
          <div
            className="lab-trainer"
            aria-hidden="true"
            style={{ left: px(trainerX - 8), top: px(TRAINER_FEET_Y - 31) }}
          >
            <SpriteSheet ref={trainerRef} slug="trainer" />
          </div>
          {STARTERS.map((s, i) => {
            const mine = picked === i;
            const frame = mine ? capFrame : 0;
            return (
              <button
                key={s.slug}
                type="button"
                className={`lab-capsule${mine && phase === "shown" ? " is-open" : ""}`}
                style={{ left: px(SLOTS[i] - 16), top: px(CAPSULE_TOP - 8) }}
                onClick={() => choose(i)}
                disabled={busy || phase === "shown"}
                aria-pressed={mine}
                aria-label={`${s.type} capsule`}
              >
                <span className="lab-capsule-art" aria-hidden="true">
                  <img
                    src={capsuleUrls[`../assets/sprites/capsules/${s.theme}.png`]}
                    alt=""
                    draggable={false}
                    style={{ transform: `translateX(${px(-frame * 16)})` }}
                  />
                </span>
              </button>
            );
          })}
        </div>
        </div>
        {phase === "shown" && starter?.battle ? (
          <div className="bh-safe lab-showcase">
            <div
              key={starter.slug}
              className="lab-creature"
              role="img"
              aria-label={`${starter.name}, the ${starter.type}-type starter`}
              style={{
                left: px(STAGE.x - 32),
                top: px(STAGE.y - 60),
                "--fx": px(SLOTS[picked] - STAGE.x),
                "--fy": px(CAPSULE_MOUTH_Y - STAGE.y),
              }}
            >
              <span className="lab-shadow" aria-hidden="true" />
              <SpriteSheet ref={creatureRef} slug={starter.battle.sprite} />
            </div>
          </div>
        ) : null}
      </div>

      <TextBox text={message} msgKey={msgKey}>
        <div className="bh-menu" ref={menuRef} role="group" aria-label="Starter menu">
          {phase === "shown" ? (
            <>
              <Link className="bh-menu-item" to={`/${starter.slug}`} aria-label={`Yes, go with ${starter.name}`}>
                <span className="bh-cursor" aria-hidden="true">▶</span>
                YES
              </Link>
              <button type="button" className="bh-menu-item" onClick={reset} aria-label="No, put it back">
                <span className="bh-cursor" aria-hidden="true">▶</span>
                NO
              </button>
            </>
          ) : (
            STARTERS.map((s, i) => (
              <button
                key={s.slug}
                type="button"
                className="bh-menu-item"
                onClick={() => choose(i)}
                disabled={busy}
                aria-label={`Open the ${s.type} capsule`}
              >
                <span className="bh-cursor" aria-hidden="true">▶</span>
                {s.type.toUpperCase()}
              </button>
            ))
          )}
        </div>
      </TextBox>
    </section>
  );
}
