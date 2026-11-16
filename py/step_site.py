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
from site_meta import CAPTIONS, CONCEPT_CATEGORIES, CONCEPT_NOTICE, CONCEPT_STEMS, CREDIT_BASE, LABELS, SHORT
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
                         "source": source, "w": w, "h": h, "slug": slug,
                         "concept": slug in CONCEPT_CATEGORIES or stem in CONCEPT_STEMS})
        cats.append({**cat, "short": SHORT[slug], "figs": figs, "concept": slug in CONCEPT_CATEGORIES})
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


def _figure_card(f: dict) -> str:
    cap = escape(f["caption"])
    credit = CREDIT_BASE + (" " + escape(f["source"]) if f["source"] else "")
    badge = f'<div class="badge">{CONCEPT_NOTICE}</div>' if f["concept"] else ""
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
    if cat["concept"]:
        notice = ('<blockquote class="note"><b>Concept.</b> fdo-git-packager is a skeleton; these graphics show the '
                  'planned design. Dashed outlines mark what is planned, solid outlines what exists.</blockquote>')
    body = (f'<h1>{escape(cat["title"])}</h1><p class="lead">{escape(cat["desc"])}</p>{notice}'
            + "".join(_figure_card(f) for f in cat["figs"]))
    return page(cat["title"], body, cats, cat["slug"], 1)


_GROUP_INTRO = {
    "Concept": "The pattern, its badges, and the schemas and architecture behind fdo-squirrel.",
    "Slides": "Worked examples with real data of CIIC 81 and the FDOx registry, as complete slides.",
    "Software FDOs": "Software as FDO: concept graphics for fdo-git-packager.",
    "Registry": "Finished 3D and software FDOs in the registry, drawn as graphs.",
}


def _index_page(cats: list[dict]) -> str:
    n = sum(len(c["figs"]) for c in cats)
    groups: dict[str, list[dict]] = {}
    for c in cats:
        groups.setdefault(c.get("group", "Visuals"), []).append(c)
    sections = []
    for g, members in groups.items():
        tiles = []
        for c in members:
            first = c["figs"][0]
            badge = f'<div class="badge">{CONCEPT_NOTICE}</div>' if c["concept"] else ""
            tiles.append(
                f'<section class="card"><a class="tile" href="visuals/{c["slug"]}.html">{badge}'
                f'<img src="visuals/img/{first["stem"]}.png" loading="lazy" alt="">'
                f'<div class="ct">{escape(c["title"])}</div><div class="cd">{escape(c["desc"])}</div>'
                f'<div class="cc">{len(c["figs"])} graphics</div></a></section>')
        sections.append(f'<h2>{escape(g)}</h2><p class="lead">{escape(_GROUP_INTRO.get(g, ""))}</p>'
                        f'<div class="grid">{"".join(tiles)}</div>')
    body = (
        "<h1>FDOx graphics</h1>"
        f'<p class="lead">An image pool of {n} graphics for presentations, posters and papers of the '
        "FDOx-squirrel family. Each comes as PNG and SVG with a caption and a credit line you can copy.</p>"
        '<blockquote class="note"><b>How to use them.</b> Transparent PNGs and SVGs (badges, schemas) go onto '
        "your own slides and posters; white 7:4 PNGs are complete slides. Where a graphic shows planned work it is "
        "tagged <b>Concept</b>; everything else is built from released tools and registry data, and its credit line "
        "names the release.</blockquote>"
        + "".join(sections)
        + '<article class="prose"><p>The graphics are generated by pure-Python scripts, see the '
        '<a href="https://github.com/FDOx-squirrel/fdox-visuals">repository</a>. Third-party logos carry their '
        "credit in the graphic.</p></article>")
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
