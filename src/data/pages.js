// Browser-tab titles per route. Shared by the app (document.title on navigation) and by
// scripts/postbuild.mjs, which writes one HTML file per route so direct links answer 200.
export const SITE_TITLE = "Derek Dinh";

export const PAGE_TITLES = {
  "/": SITE_TITLE,
  "/professional": `Professional · ${SITE_TITLE}`,
  "/projects": `Projects · ${SITE_TITLE}`,
  "/personal": `Personal · ${SITE_TITLE}`,
};

export const NOT_FOUND_TITLE = `Page not found · ${SITE_TITLE}`;

export function titleFor(pathname) {
  const key = pathname.length > 1 ? pathname.replace(/\/+$/, "") : pathname;
  return PAGE_TITLES[key] ?? NOT_FOUND_TITLE;
}
