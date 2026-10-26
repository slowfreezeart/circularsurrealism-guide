#!/usr/bin/env python3
"""Static builder for the article hub (guide.circularsurrealism.com).

Usage:  python build.py            # sync drafts, build into docs/
        python build.py --no-sync  # build only from content/

Output goes to docs/ so GitHub Pages can serve "main branch, /docs folder".
Nothing here publishes or pushes anything.
"""
import html, json, re, shutil, sys
from pathlib import Path

import markdown
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
ASSETS_SRC = ROOT / "assets-src"
STATIC = ROOT / "static"
OUT = ROOT / "docs"
DRAFTS = ROOT.parent / "marketing" / "articles" / "polished"
VISUALS = ROOT.parent / "visuals"

cfg = json.loads((ROOT / "config.json").read_text())
HUB = cfg["hub_url"].rstrip("/")
warnings = []


def sync():
    if not DRAFTS.is_dir():
        return
    for md in DRAFTS.glob("*.md"):
        if md.name.lower() == "readme.md":
            continue
        shutil.copy2(md, CONTENT / md.name)
        for ref in set(re.findall(r"visuals/([\w.-]+\.png)", md.read_text())):
            src = VISUALS / ref
            if src.exists():
                shutil.copy2(src, ASSETS_SRC / ref)
            else:
                warnings.append(f"{md.name}: image visuals/{ref} not found")


def parse(path):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta, body = yaml.safe_load(m.group(1)), m.group(2)
    meta["body_md"] = body
    return meta


IMG_CACHE = {}


def image(name):
    """Make webp (1600w + 900w) and return (path, w, h, srcset)."""
    if name in IMG_CACHE:
        return IMG_CACHE[name]
    src = ASSETS_SRC / name
    if not src.exists():
        warnings.append(f"missing image {name}")
        IMG_CACHE[name] = None
        return None
    stem = Path(name).stem
    (OUT / "assets" / "img").mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    out = {}
    for w in (900, 1600):
        c = im.copy()
        c.thumbnail((w, 10000), Image.LANCZOS)
        p = OUT / "assets" / "img" / f"{stem}-{w}.webp"
        c.save(p, "WEBP", quality=80, method=6)
        out[w] = (f"/assets/img/{stem}-{w}.webp", c.size)
    r = (out[1600][0], out[1600][1][0], out[1600][1][1],
         f"{out[900][0]} 900w, {out[1600][0]} {out[1600][1][0]}w")
    IMG_CACHE[name] = r
    return r


def og_image(name, slug):
    src = ASSETS_SRC / name
    if not src.exists():
        return None
    (OUT / "assets" / "og").mkdir(parents=True, exist_ok=True)
    W, H = 1200, 630
    canvas = Image.new("RGB", (W, H), (13, 11, 8))
    im = Image.open(src).convert("RGB")
    im.thumbnail((W - 60, H - 60), Image.LANCZOS)
    canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    p = OUT / "assets" / "og" / f"{slug}.jpg"
    canvas.save(p, "JPEG", quality=85, optimize=True)
    return f"{HUB}/assets/og/{slug}.jpg"


def fill_placeholders(s, where):
    s = s.replace("{{HUB_URL}}/", "/").replace("{{HUB_URL}}", "/")
    for key, val in cfg["links"].items():
        tok = "{{" + key + "}}"
        if tok in s:
            if val:
                s = s.replace(tok, val)
            else:
                warnings.append(f"{where}: {tok} not set in config.json (left as placeholder)")
    return s


FOUNDING_TOKEN = "{{FOUNDING_PRICE_LINE}}"


def founding_line(md_text, where):
    """Replace the {{FOUNDING_PRICE_LINE}} token (at most one per article) from config, or drop it."""
    n = md_text.count(FOUNDING_TOKEN)
    if n > 1:
        warnings.append(f"{where}: {FOUNDING_TOKEN} appears {n} times; only the first is used")
    fp = cfg.get("founding_price", {})
    line = ""
    if fp.get("enabled"):
        line = '<p class="founding">' + html.escape(fp["template"].format(price=fp["price"], limit=fp["limit"])) + "</p>"
        if not fp.get("limit_confirmed_by_user"):
            warnings.append(f"{where}: founding-price line is ON but the limit ({fp['limit']}) is not confirmed by the user")
    md_text = md_text.replace(FOUNDING_TOKEN, line, 1)
    return re.sub(r"^\{\{FOUNDING_PRICE_LINE\}\}\s*$", "", md_text, flags=re.M)


def render_body(md_text, where):
    md_text = founding_line(md_text, where)
    md_text = re.sub(r"^- \[ \] ", "- \u2610 ", md_text, flags=re.M)
    md_text = fill_placeholders(md_text, where)
    h = markdown.markdown(md_text, extensions=["fenced_code", "tables", "toc", "attr_list", "sane_lists"],
                          extension_configs={"toc": {"permalink": False}})
    first = [True]

    def fig(m):
        alt, src = html.unescape(m.group(1)), m.group(2)
        name = src.split("/")[-1]
        r = image(name) if src.startswith("visuals/") else None
        if not r:
            return m.group(0)
        path, w, hh, srcset = r
        lazy = "" if first[0] else ' loading="lazy"'
        first[0] = False
        return (f'<figure><img src="{path}" srcset="{srcset}" sizes="(max-width: 820px) 100vw, 820px" '
                f'width="{w}" height="{hh}" alt="{html.escape(alt)}" decoding="async"{lazy}>'
                f'<figcaption>{html.escape(alt)}</figcaption></figure>')

    h = re.sub(r'<p><img alt="([^"]*)" src="([^"]+)" ?/?></p>', fig, h)
    # external links open normally; mark outbound
    h = re.sub(r'<a href="(https?://(?!guide\.circularsurrealism\.com)[^"]+)"', r'<a href="\1" rel="noopener"', h)
    # code blocks become prompt cards
    h = h.replace("<pre><code>", '<div class="prompt"><span class="prompt-label">Prompt</span><button class="copy" type="button">Copy</button><pre><code>').replace("</code></pre>", "</code></pre></div>")
    return h


def head(title, desc, canonical, og_img, og_type="website", extra=""):
    e = html.escape
    og = f'<meta property="og:image" content="{e(og_img)}">\n<meta name="twitter:image" content="{e(og_img)}">' if og_img else ""
    return f"""<!doctype html>
<html lang="{cfg['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{e(cfg['site_name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(canonical)}">
{og}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="theme-color" content="#0d0b08">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/"><span class="seal" aria-hidden="true"></span><span>Circular Surrealism <em>Build Notes</em></span></a>
<nav><a href="/">Articles</a><a href="{cfg['art_site_url']}" rel="noopener">The site</a></nav>
</div></header>
"""


FOOT = f"""<footer class="site-footer"><div class="wrap">
<p class="credit"><strong>Built with Grok.</strong> The case-study site, <a href="{cfg['art_site_url']}" rel="noopener">circularsurrealism.com</a>, was built with Grok Build by xAI. These articles and the guides are independent and are not made, endorsed or sponsored by xAI.</p>
<p class="small">&copy; Slowfreeze · Circular Surrealism</p>
</div></footer>
<script src="/site.js" defer></script>
</body></html>
"""


def check_meta(a):
    if len(a["description"]) > 155:
        warnings.append(f"{a['slug']}: description is {len(a['description'])} chars (>155)")
    if len(a["title"]) > 65:
        warnings.append(f"{a['slug']}: title is {len(a['title'])} chars (Google may truncate)")
    want = f"{{{{HUB_URL}}}}/{a['slug']}/"
    if a.get("canonical") != want:
        warnings.append(f"{a['slug']}: canonical in front matter is {a.get('canonical')!r}, expected {want!r}")


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for f in STATIC.iterdir():
        shutil.copy2(f, OUT / f.name)
    (OUT / "CNAME").write_text(HUB.split("//", 1)[1] + "\n")
    (OUT / ".nojekyll").write_text("")

    arts = {p.stem: parse(p) for p in CONTENT.glob("*.md") if p.name.lower() != "readme.md"}
    order = [s for s in cfg["article_order"] if s in arts] + sorted(s for s in arts if s not in cfg["article_order"])
    cards = []
    for slug in order:
        a = arts[slug]
        assert a["slug"] == slug, f"slug mismatch in {slug}.md"
        check_meta(a)
        canonical = f"{HUB}/{slug}/"
        og = og_image(Path(a["og_image"]).name, slug) if a.get("og_image") else None
        body = render_body(a["body_md"], slug)
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["h1"][:110],
              "description": a["description"], "mainEntityOfPage": canonical,
              "author": {"@type": "Person", "name": cfg["author"], "url": cfg["art_site_url"]},
              "publisher": {"@type": "Organization", "name": "Circular Surrealism", "url": cfg["art_site_url"]}}
        if og:
            ld["image"] = og
        extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
        page = head(a["title"], a["description"], canonical, og, "article", extra)
        page += f"""<main id="main" class="wrap article">
<p class="eyebrow"><a href="/">Build Notes</a> · Case study: circularsurrealism.com</p>
<h1>{html.escape(a['h1'])}</h1>
<p class="dek">{html.escape(a['description'])}</p>
<div class="prose">
{body}
</div>
</main>
""" + FOOT
        d = OUT / slug
        d.mkdir()
        (d / "index.html").write_text(page)
        thumb = image(Path(a["og_image"]).name) if a.get("og_image") else None
        img = f'<img src="{thumb[0].replace("-1600", "-900")}" alt="" width="{thumb[1]}" height="{thumb[2]}" loading="lazy" decoding="async">' if thumb else ""
        cards.append(f'<li class="card"><a href="/{slug}/">{img}<div><h2>{html.escape(a["h1"])}</h2><p>{html.escape(a["description"])}</p><span class="more">Read the article →</span></div></a></li>')

    idx_desc = cfg["site_tagline"][:155]
    page = head("Build a High-End Website with AI — Build Notes", idx_desc, f"{HUB}/",
                og_image(Path(arts[order[0]]["og_image"]).name, "home") if order else None)
    page += f"""<main id="main" class="wrap home">
<section class="intro">
<p class="eyebrow">Free articles</p>
<h1>Build a high-end website with AI</h1>
<p class="dek">{html.escape(cfg['site_tagline'])}</p>
<p>Every number here comes from the real build: the chat history, the code, or the author's own article. Nothing is invented, and load times were never measured, so you will not find "X seconds faster" claims.</p>
</section>
<ul class="cards">
{''.join(cards)}
</ul>
</main>
""" + FOOT
    (OUT / "index.html").write_text(fill_placeholders(page, "index"))

    nf = head("Page not found — Build Notes", "This page does not exist.", f"{HUB}/404.html", None)
    nf = nf.replace("<head>", '<head>\n<meta name="robots" content="noindex">')
    nf += '<main id="main" class="wrap home"><h1>Not here.</h1><p class="dek">This page does not exist. <a href="/">Back to the articles</a>.</p></main>' + FOOT
    (OUT / "404.html").write_text(nf)

    urls = [f"{HUB}/"] + [f"{HUB}/{s}/" for s in order]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    (OUT / "sitemap.xml").write_text(sm)
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {HUB}/sitemap.xml\n")

    left = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", "".join(p.read_text() for p in OUT.rglob("*.html")))))
    needs = sorted(set(re.findall(r"\[NEEDS FACT[^\]]*\]", "".join(a["body_md"] for a in arts.values()))))
    print(f"Built {len(order)} articles into {OUT}")
    print("Placeholders left in HTML:", ", ".join(left) or "none")
    print("NEEDS FACT markers:", ", ".join(needs) or "none")
    for w in sorted(set(warnings)):
        print("WARN", w)


if __name__ == "__main__":
    if "--no-sync" not in sys.argv:
        sync()
    build()
