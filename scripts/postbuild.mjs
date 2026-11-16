// Runs after `vite build`. GitHub Pages serves /professional from professional.html, so
// writing one copy of the app shell per route makes direct links answer 200 (not the 404
// fallback) and gives each one its own <title> before any script runs. 404.html stays the
// fallback for every other path.
import { readFileSync, writeFileSync } from "node:fs";
import { NOT_FOUND_TITLE, PAGE_TITLES, SITE_TITLE } from "../src/data/pages.js";

const dist = new URL("../dist/", import.meta.url);
const shell = readFileSync(new URL("index.html", dist), "utf8");
const tag = `<title>${SITE_TITLE}</title>`;
if (shell.split(tag).length !== 2) {
  throw new Error(`postbuild: expected exactly one ${tag} in dist/index.html`);
}
const withTitle = (title) => shell.replace(tag, `<title>${title}</title>`);

for (const [route, title] of Object.entries(PAGE_TITLES)) {
  if (route === "/") continue;
  writeFileSync(new URL(`${route.slice(1)}.html`, dist), withTitle(title));
}
writeFileSync(new URL("404.html", dist), withTitle(NOT_FOUND_TITLE));
