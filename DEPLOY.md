# Deploy to GitHub Pages

This site is a static Vite build deployed manually to the `gh-pages` branch (no GitHub Actions — OAuth can block CI deploys).

## Build

```bash
npm install
npm run build
```

The build script runs `vite build` and copies `dist/index.html` to `dist/404.html` so client-side routes work on GitHub Pages.

Preview locally:

```bash
npm run preview
```

## Push `dist/` to `gh-pages`

From the repo root, after a successful build:

```bash
cd dist
git init
git checkout -b gh-pages
git add -A
git commit -m "Deploy static site"
git remote add origin git@github.com:DerekDinh1/portfolio_v2.git
git push -f origin gh-pages
```

If the `gh-pages` branch already exists remotely, clone it elsewhere or use a worktree instead of re-initing `dist/`.

## Custom domain

`public/CNAME` contains `derekdinh.com`. Vite copies it into `dist/` on build — keep it in the repo so the domain survives redeploys.

## Checklist

- [ ] `npm run build` completes without errors
- [ ] `dist/404.html` exists (same as `index.html`)
- [ ] `dist/CNAME` is present
- [ ] Deep links (e.g. `/professional`) load after deploy
