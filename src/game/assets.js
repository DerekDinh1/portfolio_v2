// Asset lookup for the battle-scene runtime. Globs resolve to {} when the
// folders do not exist yet, so missing art degrades to placeholders.
const spriteMeta = import.meta.glob("../assets/sprites/*/sheet.json", {
  eager: true,
  import: "default",
});
const spriteUrls = import.meta.glob("../assets/sprites/*/sheet.png", {
  eager: true,
  import: "default",
  query: "?url",
});
const sceneMeta = import.meta.glob("../assets/scenes/*/*.json", {
  eager: true,
  import: "default",
});
const sceneUrls = import.meta.glob("../assets/scenes/**/*.png", {
  eager: true,
  import: "default",
  query: "?url",
});

export function getSprite(slug) {
  const meta = spriteMeta[`../assets/sprites/${slug}/sheet.json`];
  const url = spriteUrls[`../assets/sprites/${slug}/sheet.png`];
  return meta && url && meta.animations?.idle?.frames?.length ? { meta, url } : null;
}

export function getScene(habitat) {
  const prefix = `../assets/scenes/${habitat}/`;
  const keys = Object.keys(sceneMeta).filter((k) => k.startsWith(prefix));
  if (!keys.length) return null;
  const key = keys.find((k) => k.endsWith("/scene.json")) || keys[0];
  const meta = sceneMeta[key];
  if (!meta?.variants) return null;
  return { meta, url: (file) => (file ? sceneUrls[`${prefix}${file}`] : undefined) };
}
