export const CAN_PLAY_WEBM =
  typeof document !== "undefined" &&
  document.createElement("video").canPlayType('video/webm; codecs="vp9"') !== "";

export const CAN_PLAY_HEVC =
  typeof document !== "undefined" &&
  document.createElement("video").canPlayType('video/mp4; codecs="hvc1"') !== "";

// Only VP9 WebM sprites have real alpha. Magenta-keyed HEVC .mov must not be
// shown as raw video; iOS falls back to the transparent PNG still instead.
export const CAN_PLAY_ALPHA_VIDEO = CAN_PLAY_WEBM;

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
