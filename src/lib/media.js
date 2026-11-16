/** Title-screen media. */
import dayPoster from "../assets/title-bg.webp";
import nightPoster from "../assets/title-bg-night.webp";

// Plain URLs: nothing is fetched until a poster is put on screen.
export const TITLE_POSTERS = { day: dayPoster, night: nightPoster };

export function loadTitleVideos() {
  return Promise.all([
    import("../assets/title-bg-day.mp4"),
    import("../assets/title-bg-night.mp4"),
  ]).then(([day, night]) => ({
    day: day.default,
    night: night.default,
  }));
}
