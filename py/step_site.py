"""S14: the GitHub Pages site (docs/), generated from img/<category>/.

One overview page and one page per category (figure-pages-site layout, FDOx
blue). Run last: it reads the finished PNGs and SVGs. docs/ is generated and
committed; nothing in it is edited by hand.

Strict mode: a graphic without a caption, or a caption without a graphic,
raises. The SVG copies get their font path rewritten so that they render with
Fira Sans from docs/assets/fonts when opened from the site.
"""

from __future__ import annotations

import shutil
import struct
from html import escape
from pathlib import Path

from site_kit import ASSETS, DOCS, page, write_assets
from site_meta import CAPTIONS, CREDIT_BASE, DRAFT_CATEGORIES, DRAFT_NOTICE, LABELS, SHORT
from visuals_utils import CATEGORIES, IMG_DIR

VIS = DOCS / "visuals"
VIS_IMG = VIS / "img"


def _png_size(path: Path) -> tuple[int, int]:
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    return struct.unpack(">II", head[16:24])


def _collect() -> list[dict]:
    cats = []
    for cat in CATEGORIES:
        slug = cat["slug"]
        on_disk = sorted(p.stem for p in (IMG_DIR / slug).glob("*.svg"))
        listed = [stem for stem, _, _ in CAPTIONS[slug]]
        if sorted(listed) != on_disk:
            raise ValueError(
                f"{slug}: captions and graphics differ; "
                f"missing caption: {sorted(set(on_disk) - set(listed))}, "
                f"no graphic: {sorted(set(listed) - set(on_disk))}")
        figs = []
        for i, (stem, caption, source) in enumerate(CAPTIONS[slug], 1):
            png = IMG_DIR / slug / f"{stem}.png"
            w, h = _png_size(png)
            figs.append({"stem": stem, "label": f"{LABELS[slug]}.{i}", "caption": caption,
                         "source": source, "w": w, "h": h, "slug": slug})
        cats.append({**cat, "short": SHORT[slug], "figs": figs, "draft": slug in DRAFT_CATEGORIES})
    return cats


def _copy_images(cats: list[dict]) -> None:
    if VIS_IMG.exists():
        shutil.rmtree(VIS_IMG)
    VIS_IMG.mkdir(parents=True)
    for cat in cats:
        for f in cat["figs"]:
            src = IMG_DIR / f["slug"]
            shutil.copyfile(src / f"{f['stem']}.png", VIS_IMG / f"{f['stem']}.png")
            svg = (src / f"{f['stem']}.svg").read_text(encoding="utf-8")
            svg = svg.replace("../../fonts/", "../../assets/fonts/")
            (VIS_IMG / f"{f['stem']}.svg").write_text(svg, encoding="utf-8")


def _figure_card(f: dict, draft: bool) -> str:
    cap = escape(f["caption"])
    credit = CREDIT_BASE + (" " + escape(f["source"]) if f["source"] else "")
    badge = f'<div class="badge">{DRAFT_NOTICE}</div>' if draft else ""
    return (
        f'<section class="card" id="{f["stem"]}">{badge}'
        f'<img class="fig" src="img/{f["stem"]}.png" width="{f["w"]}" height="{f["h"]}" loading="lazy" '
        f'alt="{cap}">'
        f'<div class="cap"><span class="n">{f["label"]}</span><span class="t">{cap}</span>'
        f'<button class="copy" type="button" data-copy="{cap}">Copy</button></div>'
        f'<div class="credit">{credit}</div>'
        f'<div class="dl"><a href="img/{f["stem"]}.png" download>PNG ({f["w"]}×{f["h"]})</a>'
        f'<a href="img/{f["stem"]}.svg" download>SVG</a></div></section>'
    )


def _category_page(cat: dict, cats: list[dict]) -> str:
    notice = ""
    if cat["draft"]:
        notice = (f'<blockquote class="note"><b>{DRAFT_NOTICE}.</b> These graphics are drafts for the '
                  'ArcheoFOSS 2026 talk. Dashed outlines mark what is planned, solid outlines what exists.</blockquote>')
    body = (f'<h1>{escape(cat["title"])}</h1><p class="lead">{escape(cat["desc"])}</p>{notice}'
            + "".join(_figure_card(f, cat["draft"]) for f in cat["figs"]))
    return page(cat["title"], body, cats, cat["slug"], 1)


def _index_page(cats: list[dict]) -> str:
    n = sum(len(c["figs"]) for c in cats)
    tiles = []
    for c in cats:
        first = c["figs"][0]
        badge = f'<div class="badge">{DRAFT_NOTICE}</div>' if c["draft"] else ""
        tiles.append(
            f'<section class="card"><a class="tile" href="visuals/{c["slug"]}.html">{badge}'
            f'<img src="visuals/img/{first["stem"]}.png" loading="lazy" alt="">'
            f'<div class="ct">{escape(c["title"])}</div><div class="cd">{escape(c["desc"])}</div>'
            f'<div class="cc">{len(c["figs"])} graphics</div></a></section>')
    body = (
        "<h1>FDOx graphics</h1>"
        f'<p class="lead">{n} graphics for talks, posters and papers of the FDOx-squirrel family, '
        "sorted by topic. Each comes as PNG and SVG with a caption you can copy.</p>"
        f'<blockquote class="note"><b>{DRAFT_NOTICE}.</b> The sets on fdo-git-packager, the federated knowledge '
        "graph ecosystem and the Ogham graph pictures are drafts and carry a notice on every card.</blockquote>"
        f'<div class="grid">{"".join(tiles)}</div>'
        '<article class="prose"><p>The graphics are generated by pure-Python scripts, see the '
        '<a href="https://github.com/FDOx-squirrel/fdox-visuals">repository</a>. Transparent PNGs are meant for '
        "slides and posters, white 7:4 PNGs are complete talk slides.</p></article>")
    return page("FDOx graphics", body, cats, "index", 0)


def run(strict: bool = False) -> list[str]:
    cats = _collect()
    write_assets()
    _copy_images(cats)
    VIS.mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(_index_page(cats), encoding="utf-8")
    log = ["wrote docs/index.html"]
    for c in cats:
        (VIS / f"{c['slug']}.html").write_text(_category_page(c, cats), encoding="utf-8")
        log.append(f"wrote docs/visuals/{c['slug']}.html ({len(c['figs'])} graphics)")
    log.append(f"copied {sum(len(c['figs']) for c in cats)} PNG + SVG pairs to docs/visuals/img/")
    return log


if __name__ == "__main__":
    for line in run():
        print(line)
