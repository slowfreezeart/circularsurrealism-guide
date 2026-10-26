# Article hub: guide.circularsurrealism.com (local, not published)

Static site for GitHub Pages. `python build.py` renders `content/*.md` into `docs/`.
It first syncs from `../marketing/articles/polished/` and `../visuals/` when those folders exist.

## Build and preview
```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
cd docs && python3 -m http.server 8765   # open http://localhost:8765
```
(On the box the venv lives at /workspace/course/.venv-hub.)

The build prints any placeholders left in the HTML, any `[NEEDS FACT]` markers, and descriptions over 155 chars.

## Config (`config.json`)
- `links.GUIDE_URL / QUICKSTART_URL / CHECKLIST_URL`: paste the Gumroad URLs, then rebuild. While they are empty, the literal `{{...}}` stays in the links.
- `hub_url`: canonical base, used for canonicals, OG URLs, the sitemap and `CNAME`.
- `article_order`: the order articles appear on the index.
- `founding_price`: the optional "Founding price $29 for the first 50 buyers." line.
  - Each article has one `{{FOUNDING_PRICE_LINE}}` token, placed right after the guide links. `enabled: true` renders it from `template`, `price` and `limit`. `enabled: false` removes it from every page. Rebuild after any change.
  - `limit` (50) is not confirmed by the user yet. The build warns while `limit_confirmed_by_user` is false. There is no refund wording anywhere.

## What docs/ contains
index, one `/<slug>/index.html` per article, 404, `CNAME`, `.nojekyll`, `robots.txt`, `sitemap.xml`, `style.css`, `site.js` (copy buttons on prompts), favicons and apple-touch icon (copied byte-for-byte from circularsurrealism.com), webp images (900/1600 px), and 1200x630 OG images.
Each page has a title, meta description, canonical, Open Graph and Twitter tags, and Article JSON-LD. No web fonts, analytics or third-party scripts.

## To go live (needs the user; not done)
1. A GitHub account or org and a repo, for example `circularsurrealism-guide`. Push this folder. In Settings → Pages, choose "Deploy from a branch", `main`, `/docs`.
2. DNS at the registrar (Namecheap): add a CNAME record for host `guide` pointing to `<github-username>.github.io`.
3. In GitHub Pages settings: custom domain `guide.circularsurrealism.com`, then tick "Enforce HTTPS" once the certificate is issued.
4. Optional: verify the domain in GitHub (Settings → Pages → verified domains), and add the property in Google Search Console with the sitemap.
