const CAN_PLAY_WEBM =
  typeof document !== "undefined" &&
  document.createElement("video").canPlayType('video/webm; codecs="vp9"') !== "";

/**
 * Apple WebKit (Safari, and all iOS browsers including Brave) may report WebM
 * as playable ("maybe") but does not composite VP9 alpha, which would show the
 * sprite's keyed-out backdrop as an opaque square. Never use animated WebM
 * sprites on WebKit; use the transparent PNG still instead.
 */
export function isAppleWebKit() {
  if (typeof navigator === "undefined") return false;
  const ua = navigator.userAgent || "";
  if (/iPhone|iPad|iPod/.test(ua)) return true;
  // iPadOS 13+ can report as MacIntel with touch
  if (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1) return true;
  // Safari / WebKit on Mac (Brave iOS also uses Apple vendor + WebKit)
  if (/Apple Computer/.test(navigator.vendor || "") && !/Edg\//.test(ua) && !/(Chrome|Chromium)\//.test(ua)) {
    return true;
  }
  return false;
}

export const CAN_PLAY_WEBM_ALPHA = CAN_PLAY_WEBM && !isAppleWebKit();

export function loadTitlePosters() {
  return Promise.all([
    import("../assets/title-bg.jpg"),
    import("../assets/title-bg-night.jpg"),
  ]).then(([day, night]) => ({
    day: day.default,
    night: night.default,
  }));
}

export function loadTitleVideos() {
  return Promise.all([
    import("../assets/title-bg-day.mp4"),
    import("../assets/title-bg-night.mp4"),
  ]).then(([day, night]) => ({
    day: day.default,
    night: night.default,
  }));
}
