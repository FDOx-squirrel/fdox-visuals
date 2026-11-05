"""Stylesheet, navigation and page skeleton of the GitHub Pages site (S14).

Single source of the look (figure-pages-site skill, accent changed to the FDOx
blue). Every page is static HTML, so the site needs no Jekyll build; docs/
carries a .nojekyll file. Colours come from visuals_utils, never from here.
"""

from __future__ import annotations

import shutil
from html import escape
from pathlib import Path

from visuals_utils import FDO_ACCENT, FONT_BOLD, FONT_REGULAR, ROOT, FDO_TINT

DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"

CSS = """\
@font-face { font-family: "Fira Sans"; src: url("fonts/FiraSans-Regular.ttf"); font-weight: 400; }
@font-face { font-family: "Fira Sans"; src: url("fonts/FiraSans-Bold.ttf"); font-weight: 700; }
:root { --bg: #f6f6f3; --card: #fff; --ink: #1f1f1d; --muted: #55544f; --rim: #d8d6ce;
        --accent: %(accent)s; --tint: %(tint)s; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%%; }
body { margin: 0; background: var(--bg); color: var(--ink);
       font: 400 17px/1.5 "Fira Sans", system-ui, sans-serif; }
a { color: var(--accent); }
header.site { background: var(--card); border-bottom: 1px solid var(--rim); }
header.site .in { max-width: 1040px; margin: 0 auto; padding: 14px 16px 10px; }
header.site .brand { font-weight: 700; font-size: 18px; color: var(--ink); text-decoration: none; }
nav .row { display: flex; flex-wrap: wrap; gap: 4px 16px; align-items: baseline; margin-top: 6px; font-size: 15px; }
nav .lab { font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted);
           min-width: 92px; font-variant: small-caps; }
nav a { color: var(--muted); text-decoration: none; }
nav a:hover { color: var(--accent); text-decoration: underline; }
nav a.on { color: var(--accent); font-weight: 700; }
main { max-width: 1040px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 28px; font-weight: 500; margin: 0 0 8px; }
p.lead { color: var(--muted); margin: 0 0 24px; }
section.card, article.prose { background: var(--card); border: 1px solid var(--rim); border-radius: 10px;
                              padding: 16px; margin-bottom: 24px; }
article.prose p { margin: 0; }
section.card img.fig { display: block; width: auto; height: auto; max-width: 100%%; max-height: 600px;
                       object-fit: contain; margin: 0 auto 12px; background: #fff; border: 1px solid var(--rim); }
.cap { display: flex; gap: 12px; align-items: baseline; }
.n { color: var(--accent); font-weight: 700; white-space: nowrap; }
.cap .t { font-size: 20px; font-weight: 500; flex: 1; }
button.copy { font: inherit; font-size: 14px; border: 1px solid var(--rim); background: var(--card);
              border-radius: 6px; padding: 2px 10px; cursor: pointer; color: var(--muted); }
button.copy:hover { border-color: var(--accent); color: var(--accent); }
.credit { font-size: 14px; color: var(--muted); margin-top: 6px; }
.dl { font-size: 14px; margin-top: 8px; }
.dl a { margin-right: 14px; }
.badge { display: inline-block; font-size: 13px; font-weight: 700; background: #fff7e0; color: #7a5200;
         border-left: 4px solid #d99a00; padding: 1px 8px; border-radius: 3px; margin-bottom: 8px; }
blockquote.note { margin: 0 0 24px; padding: 10px 14px; background: #fff7e0; border-left: 4px solid #d99a00;
                  border-radius: 4px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
.grid .card { margin: 0; padding: 12px; }
.grid a.tile { text-decoration: none; color: inherit; display: block; }
.grid img { display: block; width: 100%%; height: 190px; object-fit: contain; background: #fff;
            border: 1px solid var(--rim); border-radius: 6px; margin-bottom: 8px; }
.grid .ct { font-weight: 500; font-size: 18px; color: var(--accent); }
.grid .cd { font-size: 14px; color: var(--muted); }
.grid .cc { font-size: 13px; color: var(--muted); margin-top: 4px; }
footer { max-width: 1040px; margin: 0 auto; padding: 0 16px 32px; font-size: 14px; color: var(--muted); }
@media (max-width: 640px) { .grid { grid-template-columns: 1fr; } .cap { flex-wrap: wrap; }
  nav .lab { min-width: 0; width: 100%%; } h1 { font-size: 24px; } }
""" % {"accent": FDO_ACCENT, "tint": FDO_TINT}


def write_assets() -> None:
    """site.css and the vendored Fira Sans, written fresh on every run."""
    (ASSETS / "fonts").mkdir(parents=True, exist_ok=True)
    (ASSETS / "site.css").write_text(CSS, encoding="utf-8")
    for f in (FONT_REGULAR, FONT_BOLD):
        shutil.copyfile(f, ASSETS / "fonts" / f.name)
    shutil.copyfile(ROOT / "fonts" / "LICENSE-FiraSans.txt", ASSETS / "fonts" / "LICENSE-FiraSans.txt")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")


def nav(categories: list[dict], active: str, depth: int) -> str:
    """Two-row navigation. depth 0 = docs/index.html, 1 = docs/visuals/*.html."""
    up = "../" * depth
    def link(href: str, text: str, key: str) -> str:
        on = ' class="on"' if active == key else ""
        return f'<a href="{href}"{on}>{escape(text)}</a>'

    home = link(f"{up}index.html", "Overview", "index")
    links = " ".join(link(f"{up}visuals/{c['slug']}.html", c["short"], c["slug"]) for c in categories)
    return (f'<nav><div class="row"><span class="lab">Site</span>{home}</div>'
            f'<div class="row"><span class="lab">Visuals</span>{links}</div></nav>')


def page(title: str, body: str, categories: list[dict], active: str, depth: int) -> str:
    up = "../" * depth
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{escape(title)} · fdox-visuals</title>"
        f"<link rel=\"stylesheet\" href=\"{up}assets/site.css\"></head><body>"
        f"<header class=\"site\"><div class=\"in\"><a class=\"brand\" href=\"{up}index.html\">fdox-visuals</a>"
        f"{nav(categories, active, depth)}</div></header>"
        f"<main>{body}</main>"
        "<footer>Graphics and generator: <a href=\"https://github.com/FDOx-squirrel/fdox-visuals\">"
        "FDOx-squirrel/fdox-visuals</a>. Code under the MIT licence. Fira Sans: SIL Open Font Licence.</footer>"
        "<script>document.querySelectorAll('button.copy').forEach(function(b){b.addEventListener('click',function(){"
        "var t=b.getAttribute('data-copy');var d=function(){var o=b.textContent;b.textContent='Copied';"
        "setTimeout(function(){b.textContent=o;},1200);};"
        "if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(d,function(){});}"
        "});});</script></body></html>\n"
    )
