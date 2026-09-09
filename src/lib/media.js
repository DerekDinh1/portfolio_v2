/**
 * Title-screen media loaders.
 * Mascot loops use animated WebP with real alpha (see starters.js / MascotSprite).
 * Magenta-keyed MOV/WebM are intentionally unused — Safari paints their matte pink.
 */

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
