import { useLayoutEffect, useRef } from "react";

const NATIVE_W = 240;
const NATIVE_H = 160;
const MAX_VH = 0.62;

// Art-bible display rule: an integer number of device pixels per art pixel,
// with the 240x160 scene at most 62vh tall. Writes the CSS size of one art
// pixel to --px on the returned ref's element.
export function computePixelScale(cssWidth) {
  const dpr = window.devicePixelRatio || 1;
  const byWidth = Math.floor((cssWidth * dpr) / NATIVE_W);
  const byHeight = Math.floor((window.innerHeight * MAX_VH * dpr) / NATIVE_H);
  return Math.max(1, Math.min(byWidth, byHeight)) / dpr;
}

export default function usePixelScale() {
  const ref = useRef(null);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return undefined;

    const apply = () => {
      el.style.setProperty("--px", `${computePixelScale(el.clientWidth)}px`);
    };
    apply();

    const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(apply) : null;
    ro?.observe(el);
    window.addEventListener("resize", apply);

    // Browser zoom / moving between displays changes devicePixelRatio.
    let mql = null;
    const watchDpr = () => {
      mql?.removeEventListener("change", onDpr);
      mql = window.matchMedia(`(resolution: ${window.devicePixelRatio || 1}dppx)`);
      mql.addEventListener("change", onDpr);
    };
    function onDpr() {
      apply();
      watchDpr();
    }
    watchDpr();

    return () => {
      ro?.disconnect();
      window.removeEventListener("resize", apply);
      mql?.removeEventListener("change", onDpr);
    };
  }, []);

  return ref;
}
