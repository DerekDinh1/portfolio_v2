import { useEffect, useRef, useState } from "react";
import { useIsNight } from "../shared.jsx";
import { getScene } from "./assets.js";

const PLACEHOLDER = { water: "#3890D8", fire: "#E86830", grass: "#58A848" };

// True while the element is on screen and the tab is visible.
function useRunning(ref) {
  const [running, setRunning] = useState(true);
  useEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    let visible = true;
    const sync = () => setRunning(visible && !document.hidden);
    const io =
      typeof IntersectionObserver !== "undefined"
        ? new IntersectionObserver(([entry]) => {
            visible = entry.isIntersecting;
            sync();
          })
        : null;
    io?.observe(el);
    document.addEventListener("visibilitychange", sync);
    return () => {
      io?.disconnect();
      document.removeEventListener("visibilitychange", sync);
    };
  }, [ref]);
  return running;
}

function layerStyle(layer, url) {
  const frames = layer.frames || 1;
  const drift = layer.drift || 0;
  const names = [];
  const durations = [];
  const timings = [];
  if (drift) {
    names.push("bh-drift");
    durations.push(`${layer.w / Math.abs(drift)}s`);
    timings.push(`steps(${layer.w})`);
  }
  if (frames > 1) {
    names.push("bh-frames");
    durations.push(`${frames / (layer.fps || 4)}s`);
    timings.push(`steps(${frames})`);
  }
  return {
    backgroundImage: `url(${url})`,
    "--lw": layer.w,
    "--lf": frames,
    "--dx": `calc(var(--px) * ${layer.w * Math.sign(drift)})`,
    ...(names.length
      ? {
          animationName: names.join(", "),
          animationDuration: durations.join(", "),
          animationTimingFunction: timings.join(", "),
          animationIterationCount: "infinite",
        }
      : null),
  };
}

// Renders a habitat per the art-bible Scene contract.
// Props: habitat ("water" | "fire" | "grass" | ...), className.
// Layers fill the full-bleed band (the nearest positioned ancestor); the
// platform sits inside a centred 240-art-pixel safe area. Missing scene data
// or images degrade to a flat, labelled placeholder band.
export default function SceneBackdrop({ habitat, className = "" }) {
  const night = useIsNight();
  const ref = useRef(null);
  const running = useRunning(ref);
  const scene = getScene(habitat);

  if (!scene) {
    return (
      <div
        ref={ref}
        className={`bh-backdrop bh-backdrop--missing ${className}`}
        style={{ backgroundColor: PLACEHOLDER[habitat] || "#98A8C8" }}
        aria-hidden="true"
      >
        <span className="bh-backdrop-label">PLACEHOLDER SCENE: {habitat}</span>
      </div>
    );
  }

  const { meta, url } = scene;
  const day = meta.variants.day;
  const variant = night && meta.variants.night ? meta.variants.night : day;
  const layers = (variant.layers?.length ? variant.layers : day?.layers) || [];
  const platform = meta.platform;
  const platformUrl = url(variant.platform || platform?.file);

  return (
    <div ref={ref} className={`bh-backdrop ${running ? "" : "is-paused"} ${className}`} aria-hidden="true">
      {layers.map((layer) => {
        const src = url(layer.file);
        return src ? (
          <div
            key={`${night}-${layer.file}`}
            className="bh-layer"
            style={layerStyle(layer, src)}
          />
        ) : null;
      })}
      {platform && platformUrl ? (
        <div className="bh-safe">
          <img
            className="bh-platform"
            src={platformUrl}
            alt=""
            draggable={false}
            style={{
              left: `calc(var(--px) * ${platform.cx - platform.w / 2})`,
              top: `calc(var(--px) * ${platform.cy - platform.h / 2})`,
              width: `calc(var(--px) * ${platform.w})`,
              height: `calc(var(--px) * ${platform.h})`,
            }}
          />
        </div>
      ) : null}
    </div>
  );
}
