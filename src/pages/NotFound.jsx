import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import SceneBackdrop from "../game/SceneBackdrop.jsx";
import usePixelScale from "../game/usePixelScale.js";
import { TextBox } from "../game/BattleHero.jsx";
import { SLOW } from "../game/timing.js";
import compassUrl from "../assets/sprites/lost/compass.png";
import "../game/game.css";

// Scene coordinates (art pixels) matching tools/scenes/habitats/lost.py.
const COMPASS = { x: 112, y: 93, size: 17, frames: 16 };
const SETTLED_FRAME = 6; // the needle comes to rest pointing down-right, at the menu
const SEARCH_MS = 4200 * SLOW;
const SPIN_MS = 2200 * SLOW;

const px = (n) => `calc(var(--px) * ${n})`;

function prefersReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

// 404 as a game screen: a pack left on a lit patch of grass, a compass that cannot settle
// while the trail map is checked, then the way back to the lab.
export default function NotFound() {
  const rootRef = usePixelScale();
  const [searching, setSearching] = useState(() => !prefersReducedMotion());

  useEffect(() => {
    if (!searching) return undefined;
    const id = window.setTimeout(() => setSearching(false), SEARCH_MS);
    return () => window.clearTimeout(id);
  }, [searching]);

  const message = searching
    ? "Page not found. Checking the trail map... Please wait."
    : "No trail leads here. Head back to the lab?";

  return (
    <main className="page theme-grass">
      <section ref={rootRef} className="bh lost">
        <h1 className="bh-sr">Page not found</h1>
        <div className="bh-scene">
          <SceneBackdrop habitat="lost" />
          <div className="bh-safe">
            <span
              className={`lost-compass${searching ? " is-spinning" : ""}`}
              aria-hidden="true"
              style={{ left: px(COMPASS.x), top: px(COMPASS.y) }}
            >
              <img
                src={compassUrl}
                alt=""
                draggable={false}
                style={
                  searching
                    ? { animationDuration: `${SPIN_MS}ms` }
                    : { transform: `translateX(${px(-SETTLED_FRAME * COMPASS.size)})` }
                }
              />
            </span>
          </div>
        </div>
        <TextBox text={message} msgKey={searching ? 0 : 1} note="Error 404: this path is not on the map.">
          <div className="bh-menu" role="group" aria-label="Lost menu">
            <Link className="bh-menu-item" to="/">
              <span className="bh-cursor" aria-hidden="true">▶</span>
              BACK TO LAB
            </Link>
          </div>
        </TextBox>
      </section>
      <div className="lost-foot">
        <p className="select-sub">Looks like you wandered off the trail. That path doesn't lead anywhere.</p>
        <Link className="btn btn-red" to="/">← Back to the lab</Link>
      </div>
    </main>
  );
}
