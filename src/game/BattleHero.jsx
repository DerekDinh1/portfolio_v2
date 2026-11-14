import { useCallback, useEffect, useImperativeHandle, useRef, useState } from "react";
import SceneBackdrop from "./SceneBackdrop.jsx";
import SpriteSheet from "./SpriteSheet.jsx";
import usePixelScale from "./usePixelScale.js";
import "./game.css";

const TYPE_MS = 28;
const SPRITE_W = 64;
const FEET = { x: 176, y: 80 };
const ANCHOR = { x: 32, y: 60 };

function prefersReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

// Typewriter text box. Only this component re-renders while typing. The live
// region is off while typing; the full message is exposed to screen readers
// once typing finishes.
export function TextBox({ text, msgKey, children }) {
  const [shown, setShown] = useState(() => (prefersReducedMotion() ? text.length : 0));
  const typing = shown < text.length;

  useEffect(() => {
    if (prefersReducedMotion()) {
      setShown(text.length);
      return undefined;
    }
    setShown(0);
    const id = window.setInterval(() => {
      setShown((n) => {
        if (n + 1 >= text.length) window.clearInterval(id);
        return n + 1;
      });
    }, TYPE_MS);
    return () => window.clearInterval(id);
  }, [text, msgKey]);

  return (
    <div className="bh-dock">
      <div className="bh-panel bh-textbox">
        <p className="bh-message" aria-live={typing ? "off" : "polite"} aria-atomic="true">
          <span aria-hidden="true">{text.slice(0, shown)}</span>
          {typing ? <span className="bh-caret" aria-hidden="true">▌</span> : null}
          <span className="bh-sr">{typing ? "" : text}</span>
        </p>
        {children}
      </div>
    </div>
  );
}

function scrollToId(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "start" });
}

// Battle-scene hero per the art-bible layout.
// Props:
//   starter        starter record (name, type, theme)
//   habitat        scene folder name ("water" | "fire" | "grass")
//   sprite         sprite slug under src/assets/sprites
//   level          number shown as "Lv n"
//   bar            { label, value (0-100), text }  accessible text for the stat bar
//   status         { tag, text }  short tag with accessible description
//   message        default text-box message
//   greetMessage   message shown when the creature is tapped
//   onTap          optional; called on tap, and a string it returns replaces greetMessage
//   menu           [{ key, label, ariaLabel?, href?, download?, newTab?, scrollTo?, play? }]
//                  href -> link; otherwise button. scrollTo = element id.
//                  play = sprite animation to run on activation.
//                  onSelect = called on activation; a string it returns is shown in the text box.
//   ref            { play(name) } plays a sprite animation (e.g. "greet")
export default function BattleHero({
  starter,
  habitat,
  sprite,
  level,
  bar,
  status,
  message,
  greetMessage,
  onTap,
  menu = [],
  ref,
}) {
  const rootRef = usePixelScale();
  const spriteRef = useRef(null);
  const menuRef = useRef(null);
  const [msg, setMsg] = useState({ text: message, key: 0 });

  useImperativeHandle(ref, () => ({ play: (name) => spriteRef.current?.play(name) }), []);

  const tap = () => {
    spriteRef.current?.play("greet");
    const text = onTap?.() || greetMessage;
    setMsg((m) => ({ text, key: m.key + 1 }));
  };

  const onMenuKey = useCallback((e) => {
    const delta = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 2, ArrowUp: -2 }[e.key];
    if (!delta) return;
    const items = [...menuRef.current.querySelectorAll(".bh-menu-item")];
    const i = items.indexOf(document.activeElement);
    if (i < 0) return;
    const next = items[i + delta];
    if (!next) return;
    e.preventDefault();
    next.focus();
  }, []);

  const type = starter.type.toUpperCase();
  const left = (FEET.x - ANCHOR.x) * 1;
  const top = FEET.y - ANCHOR.y;

  return (
    <section ref={rootRef} className={`bh theme-${starter.theme}`}>
      <div className="bh-scene">
        <SceneBackdrop habitat={habitat} />
        <div className="bh-safe">
          <button
            type="button"
            className="bh-creature"
            onClick={tap}
            aria-label={`${starter.name}, the ${starter.type}-type starter. Tap to say hi`}
            style={{
              left: `calc(var(--px) * ${left})`,
              top: `calc(var(--px) * ${top})`,
              width: `calc(var(--px) * ${SPRITE_W})`,
              height: `calc(var(--px) * ${SPRITE_W})`,
            }}
          >
            <SpriteSheet ref={spriteRef} slug={sprite} />
          </button>

          <div className={`bh-panel bh-info bh-type--${starter.theme}`}>
            <div className="bh-info-row">
              <h1 className="bh-name">{starter.name}</h1>
              <span className="bh-level">Lv {level}</span>
            </div>
            <div className="bh-info-row">
              <span className="bh-badge">{type}</span>
              {status ? (
                <span className="bh-status">
                  <span aria-hidden="true">{status.tag}</span>
                  <span className="bh-sr">{status.text}</span>
                </span>
              ) : null}
            </div>
            {bar ? (
              <div className="bh-stat">
                <span className="bh-stat-label" id="bh-stat-label">{bar.label}</span>
                <div
                  className="bh-bar"
                  role="meter"
                  aria-labelledby="bh-stat-label"
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-valuenow={bar.value}
                  aria-valuetext={bar.text}
                >
                  <div className="bh-bar-fill" style={{ width: `${bar.value}%` }} />
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </div>

      <TextBox text={msg.text} msgKey={msg.key}>
        <div className="bh-menu" ref={menuRef} onKeyDown={onMenuKey} role="group" aria-label={`${starter.name} menu`}>
          {menu.map((item) => {
            const onClick = () => {
              if (item.play) spriteRef.current?.play(item.play);
              if (item.scrollTo) scrollToId(item.scrollTo);
              const text = item.onSelect?.();
              if (text) setMsg((m) => ({ text, key: m.key + 1 }));
            };
            const content = (
              <>
                <span className="bh-cursor" aria-hidden="true">▶</span>
                {item.label}
              </>
            );
            return item.href ? (
              <a
                key={item.key}
                className="bh-menu-item"
                href={item.href}
                download={item.download || undefined}
                target={item.newTab ? "_blank" : undefined}
                rel={item.newTab ? "noopener noreferrer" : undefined}
                aria-label={item.ariaLabel}
                onClick={onClick}
              >
                {content}
              </a>
            ) : (
              <button key={item.key} type="button" className="bh-menu-item" aria-label={item.ariaLabel} onClick={onClick}>
                {content}
              </button>
            );
          })}
        </div>
      </TextBox>
    </section>
  );
}
