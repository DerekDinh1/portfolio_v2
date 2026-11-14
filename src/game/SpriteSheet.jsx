import { useEffect, useImperativeHandle, useMemo, useRef, useState } from "react";
import { getSprite } from "./assets.js";

// Plays a sprite sheet per the art-bible Sprite contract. Frames advance by
// mutating a transform on one <img>, so React never re-renders per frame.
// Props: slug (string), label (placeholder caption), className, ref.
// ref API: { play(name) } plays a non-looping animation, then its `next`.
export default function SpriteSheet({ slug, className = "", ref }) {
  const sprite = useMemo(() => getSprite(slug), [slug]);
  const rootRef = useRef(null);
  const imgRef = useRef(null);
  const engine = useRef(null);
  const [dims, setDims] = useState(null);
  const [failed, setFailed] = useState(false);

  useImperativeHandle(ref, () => ({ play: (name) => engine.current?.play(name) }), []);

  // Safari fires `load` for a cached sheet before this effect runs, so read the
  // image here instead of clearing the size and waiting for an event that already happened.
  useEffect(() => {
    const img = imgRef.current;
    setFailed(Boolean(img?.complete && !img.naturalWidth));
    setDims(img?.complete && img.naturalWidth ? { w: img.naturalWidth, h: img.naturalHeight } : null);
  }, [slug]);

  useEffect(() => {
    const root = rootRef.current;
    const img = imgRef.current;
    if (!sprite || !root || !img) return undefined;
    const { animations, frame } = sprite.meta;
    const fw = frame?.w || 64;
    const fh = frame?.h || 64;
    const s = { anim: "idle", frame: 0 };
    let timer = 0;
    let onScreen = true;
    const reduceMql = window.matchMedia("(prefers-reduced-motion: reduce)");

    const canRun = () => onScreen && !document.hidden && !reduceMql.matches;

    // An animation may list `order`: the sheet column for each step, so frames can repeat.
    const steps = (a) => (a.order ? a.order.length : a.frames.length);
    const column = (a) => (a.order ? a.order[s.frame] : s.frame);

    const draw = () => {
      const a = animations[s.anim];
      img.style.transform = `translate(calc(var(--px) * ${-column(a) * fw}), calc(var(--px) * ${-a.row * fh}))`;
    };

    const tick = () => {
      window.clearTimeout(timer);
      timer = 0;
      draw();
      const a = animations[s.anim];
      if (!canRun() || (a.loop && steps(a) < 2)) return;
      timer = window.setTimeout(advance, (a.frames[column(a)] || a.frames[0]).ms);
    };

    function advance() {
      const a = animations[s.anim];
      if (s.frame + 1 < steps(a)) {
        s.frame += 1;
      } else if (a.loop) {
        s.frame = 0;
      } else {
        s.anim = animations[a.next] ? a.next : "idle";
        s.frame = 0;
      }
      tick();
    }

    const syncMotion = () => {
      if (reduceMql.matches) {
        s.anim = "idle";
        s.frame = 0;
      }
      tick();
    };

    engine.current = {
      play(name) {
        if (reduceMql.matches || !animations[name]) return;
        s.anim = name;
        s.frame = 0;
        tick();
      },
    };

    const io =
      typeof IntersectionObserver !== "undefined"
        ? new IntersectionObserver(([entry]) => {
            onScreen = entry.isIntersecting;
            tick();
          })
        : null;
    io?.observe(root);
    document.addEventListener("visibilitychange", tick);
    reduceMql.addEventListener("change", syncMotion);
    syncMotion();

    return () => {
      window.clearTimeout(timer);
      io?.disconnect();
      document.removeEventListener("visibilitychange", tick);
      reduceMql.removeEventListener("change", syncMotion);
      engine.current = null;
    };
  }, [sprite, dims]);

  if (!sprite || failed) {
    return (
      <span className={`sprite sprite--missing ${className}`} role="img" aria-label={`Sprite missing: ${slug}`}>
        <span className="sprite-missing-label">NO SPRITE {slug}</span>
      </span>
    );
  }

  return (
    <span ref={rootRef} className={`sprite ${className}`} aria-hidden="true">
      <img
        ref={imgRef}
        className="sprite-sheet"
        src={sprite.url}
        alt=""
        draggable={false}
        style={
          dims
            ? { width: `calc(var(--px) * ${dims.w})`, height: `calc(var(--px) * ${dims.h})` }
            : { visibility: "hidden" }
        }
        onLoad={(e) => setDims({ w: e.currentTarget.naturalWidth, h: e.currentTarget.naturalHeight })}
        onError={() => setFailed(true)}
      />
    </span>
  );
}
