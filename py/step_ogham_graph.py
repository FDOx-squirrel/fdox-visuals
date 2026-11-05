"""S13 -- Real graph pictures: Ogham stones, their 3D FDOs and the software that works on them.

Three 7:4 talk slides (white, S8 convention) that draw *actual triples* of the
FDOx Registry as node-link graphs, not as boxes-and-arrows concept art:

  img/fdox-talk-ogham-graph-cluster.svg/.png    the Ogham cluster: 3 x 3DDataFDO + 2 x SoftwareFDO, shared concept, places, people
  img/fdox-talk-ogham-graph-object.svg/.png     CIIC 81 (3D FDO) and the o3d-epidoc-extractor (SoftwareFDO), one hop each
  img/fdox-talk-ogham-graph-registry.svg/.png   all eight FDOs of the registry as one graph, with the Wikidata hubs

Source of every node and edge: `dist/fdo-registry.ttl` of
`FDOx-squirrel/fdo-squirrel-registry` at 253aee9 (release 2026-09-03, 7,793
triples), read with rdflib on 2026-11-05, plus `registry-index.json` for file
counts and sizes. Predicates drawn: dct:subject / dct:type (Wikidata concepts),
dct:creator, dct:spatial, dct:license, dct:publisher, codemeta:codeRepository.
Checked values:
  * wd:Q2016147 is dct:subject and dct:type of Ogham 3D EpiDoc Extractor,
    Ogham Analysis, GEARS/1 and CO074-148---- (CIIC 81); label in the bundle
    "Inscribed Ogham stone". wd:Q22731 (label "Stone") is dct:subject of six.
  * CHUIS/1 carries "Ogham Stone" as free text only, no concept IRI.
  * Creators: Florian Thiery appears as the ORCID node 0000-0002-3246-3531
    (Extractor, GEARS/1) and as the registry-minted agent 8e916ce55425de21
    (CHUIS/1, CO074-148----, Steinmaennchen, Beuys-Stele); the registry does not
    merge by name (quality report). Timo Homburg: ORCID 0000-0002-9499-5840 on the
    Extractor. Anne-Karoline Distel: agent 1ef85dc7cadee6db on CO074-148----.
    Sophie C. Schmidt: ORCID 0000-0003-4696-2101 on Ogham Analysis.
  * Places: OSM relation 62273 (both software FDOs), OSM node 11071361392
    (CO074-148----, labelled "CO074-148----"), OSM node 11966441102 (GEARS/1).
  * Other concept IRIs on the objects: wd:Q24041450 (Cork Public Museum, GEARS/1),
    wd:Q5382396 (EpiDoc) and wd:Q18692990 (Linked Open Data) on the Extractor,
    wd:Q121592049 on CO074-148---- (no label in the bundle, none invented here).
  * CO074-148----: 50 files, 673 MB, CC-BY-NC-SA-4.0, provenance "KIRI Engine".
    Extractor: 254 files, 53 MB, MIT, v1.1, codeRepository
    linkedopenogham.github.io/o3d-epidoc-extractor/.
  * Wikidata itself was not reachable from the sandbox, so only the labels the
    bundle carries are shown; nothing about the Wikidata items is added.

There is NO triple in the registry in which a software FDO states that it
*uses* a particular 3D FDO. The software and the objects meet through the
shared concept, the shared context and the same publisher. The second slide
therefore draws that link dashed and says so.

Solid = in the registry today; dashed = not modelled yet.

Runnable standalone: `python py/step_ogham_graph.py`
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals_utils import (  # noqa: E402
    FDO_ACCENT,
    FDO_ACCENT_LIGHT,
    FDO_ACCENT_SOFT,
    IMG_DIR,
    INK,
    MUTED,
    STEPS,
    ensure_dirs,
    esc,
    render_svg_to_png,
)
from step_federation import (  # noqa: E402
    H,
    OVERSAMPLE,
    W,
    _close,
    _glyph_hub,
    _glyph_triple,
    _heading,
    _open,
    _t,
)

TINT = STEPS[0]["tint"]
CODE_BG = "#F5F7FA"
HALO = "#D9DEE6"

# ------------------------------------------------------------------- nodes --
# kind: fdo3d | fdosw | concept | place | person | literal | info
# a node is (kind, x, y, w, h, [(text, size, weight)], dashed)


def N(kind, x, y, w, h, lines, dashed=False):
    return dict(kind=kind, x=x, y=y, w=w, h=h, lines=lines, dashed=dashed)


def _clip(n: dict, tx: float, ty: float) -> tuple[float, float]:
    """Point where the line from the node centre to (tx, ty) leaves the node."""
    dx, dy = tx - n["x"], ty - n["y"]
    if dx == 0 and dy == 0:
        return n["x"], n["y"]
    hw, hh = n["w"] / 2 + 3, n["h"] / 2 + 3
    if n["kind"] in ("place", "person"):
        k = 1 / math.sqrt((dx / hw) ** 2 + (dy / hh) ** 2)
    else:
        k = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
    return n["x"] + dx * k, n["y"] + dy * k


def _node_svg(n: dict) -> str:
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    left, top = x - w / 2, y - h / 2
    k = n["kind"]
    dash = ' stroke-dasharray="12 8"' if n["dashed"] else ""
    ink = INK
    if k == "fdo3d":
        shape = f'<rect x="{left}" y="{top}" width="{w}" height="{h}" rx="14" fill="{FDO_ACCENT}" stroke="{FDO_ACCENT}" stroke-width="4"{dash}/>'
        ink = "white"
    elif k == "fdosw":
        shape = f'<rect x="{left}" y="{top}" width="{w}" height="{h}" rx="14" fill="white" stroke="{FDO_ACCENT}" stroke-width="4.5"{dash}/>'
    elif k == "concept":
        shape = f'<rect x="{left}" y="{top}" width="{w}" height="{h}" rx="{h/2}" fill="{TINT}" stroke="{FDO_ACCENT_SOFT}" stroke-width="3.5"{dash}/>'
    elif k == "place":
        shape = f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="white" stroke="{FDO_ACCENT_LIGHT}" stroke-width="3" stroke-dasharray="3 6" stroke-linecap="round"/>'
    elif k == "person":
        shape = f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="white" stroke="{MUTED}" stroke-width="3"{dash}/>'
    elif k == "literal":
        shape = f'<rect x="{left}" y="{top}" width="{w}" height="{h}" rx="10" fill="white" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 7"/>'
    else:  # info
        shape = f'<rect x="{left}" y="{top}" width="{w}" height="{h}" rx="10" fill="{CODE_BG}" stroke="{HALO}" stroke-width="2.5"{dash}/>'
    total = sum(s * 1.3 for _, s, _ in n["lines"])
    cy = y - total / 2
    txt = ""
    for text, size, weight in n["lines"]:
        color = ink if weight >= 700 or ink == "white" else MUTED
        if ink != "white" and weight < 700:
            color = MUTED
        txt += _t(x, cy + size * 0.95, text, size, weight, color if ink != "white" else ("white" if weight >= 700 else "#D6E2EC"), "middle")
        cy += size * 1.3
    return shape + txt


# ------------------------------------------------------------------- edges --
STYLE = {
    "subject": dict(color=FDO_ACCENT, width=4.5, dash=""),
    "creator": dict(color=MUTED, width=3, dash=""),
    "spatial": dict(color=FDO_ACCENT_LIGHT, width=3, dash="3 7"),
    "meta": dict(color="#9AA3B5", width=2.5, dash=""),
    "planned": dict(color=FDO_ACCENT, width=4, dash="14 9"),
    "text": dict(color=MUTED, width=3, dash="10 8"),
}


def _edge_svg(nodes: dict, a: str, b: str, style: str, label: str = "", arrow: bool = True, bend: float = 0, lpos: float = 0.5) -> str:
    na, nb = nodes[a], nodes[b]
    st = STYLE[style]
    mx, my = (na["x"] + nb["x"]) / 2, (na["y"] + nb["y"]) / 2
    # optional quadratic bend, perpendicular to the straight line
    dx, dy = nb["x"] - na["x"], nb["y"] - na["y"]
    ln = math.hypot(dx, dy) or 1
    cx, cy = mx - dy / ln * bend, my + dx / ln * bend
    x1, y1 = _clip(na, cx, cy)
    x2, y2 = _clip(nb, cx, cy)
    dash = f' stroke-dasharray="{st["dash"]}" stroke-linecap="round"' if st["dash"] else ""
    if bend:
        d = f"M {x1:.1f},{y1:.1f} Q {cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}"
    else:
        d = f"M {x1:.1f},{y1:.1f} L {x2:.1f},{y2:.1f}"
    out = f'<path d="{d}" fill="none" stroke="{st["color"]}" stroke-width="{st["width"]}"{dash}/>'
    if arrow:
        ang = math.atan2(y2 - (cy if bend else y1), x2 - (cx if bend else x1))
        s = 13
        p1 = (x2 - s * math.cos(ang - 0.45), y2 - s * math.sin(ang - 0.45))
        p2 = (x2 - s * math.cos(ang + 0.45), y2 - s * math.sin(ang + 0.45))
        out += f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{st["color"]}"/>'
    if label:
        t = lpos
        if bend:
            lx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2
            ly = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2
        else:
            lx, ly = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        tw = len(label) * 8.2 + 12
        out += f'<rect x="{lx - tw/2:.1f}" y="{ly - 12:.1f}" width="{tw:.1f}" height="22" rx="6" fill="white" opacity="0.92"/>'
        out += _t(round(lx, 1), round(ly + 5, 1), label, 15, 400, st["color"] if style != "meta" else MUTED, "middle")
    return out


def _graph(nodes: dict, edges: list) -> str:
    out = "".join(_edge_svg(nodes, *e[:3], **(e[3] if len(e) > 3 else {})) for e in edges)
    return out + "".join(_node_svg(n) for n in nodes.values())


def _fdo(kind, x, y, title, sub, w=250):
    return N(kind, x, y, w, 72, [(title, 21, 700), (sub, 15, 400)])


def _legend(items_note: str, y: int = 905) -> str:
    """Node-kind and edge-style legend, one row, plus the source note."""
    out = ""
    x = 60
    for kind, label in (("fdo3d", "3D FDO"), ("fdosw", "Software FDO"), ("concept", "Wikidata concept"), ("place", "place"), ("person", "person")):
        n = N(kind, x + 22, y, 44, 26, [])
        out += _node_svg(n) + _t(x + 54, y + 7, label, 18, 400, INK)
        x += 54 + len(label) * 9.5 + 34
    out += _t(60, 958, items_note, 18, 400, MUTED)
    return out


# ------------------------------------------------------- slide 1: cluster --


def _build_cluster() -> str:
    p = _open()
    p.append(_heading(_glyph_hub(), "Ogham in the graph", "Stones, 3D models and software: real triples of the FDOx Registry"))

    n = {
        "hub": N("concept", 875, 500, 250, 76, [("wd:Q2016147", 22, 700), ("Inscribed Ogham stone", 16, 400)]),
        "E": _fdo("fdosw", 480, 340, "Ogham 3D EpiDoc Extractor", "SoftwareFDO · MIT", 310),
        "A": _fdo("fdosw", 480, 660, "Ogham Analysis", "SoftwareFDO · MIT"),
        "G": _fdo("fdo3d", 1270, 340, "GEARS/1", "3DDataFDO · Cork Public Museum"),
        "C": _fdo("fdo3d", 1270, 660, "CO074-148---- (CIIC 81)", "3DDataFDO · UCC Stone Corridor", 290),
        "H": _fdo("fdo3d", 875, 800, "CHUIS/1", "3DDataFDO · Cork Public Museum"),
        "T": N("person", 875, 300, 190, 54, [("Thiery, F.", 18, 700), ("ORCID", 14, 400)]),
        "Ho": N("person", 175, 290, 170, 54, [("Homburg, T.", 18, 700), ("ORCID", 14, 400)]),
        "S": N("person", 175, 720, 170, 54, [("Schmidt, S. C.", 18, 700), ("ORCID", 14, 400)]),
        "Ta": N("person", 1150, 850, 190, 54, [("Thiery, F.", 18, 700), ("registry agent", 14, 400)], dashed=True),
        "D": N("person", 1600, 730, 170, 54, [("Distel, A.-K.", 18, 700), ("registry agent", 14, 400)]),
        "p62": N("place", 205, 500, 190, 62, [("OSM relation", 15, 400), ("62273", 17, 700)]),
        "pG": N("place", 1560, 270, 190, 62, [("OSM node", 15, 400), ("11966441102", 17, 700)]),
        "pC": N("place", 1560, 540, 190, 62, [("OSM node", 15, 400), ("11071361392", 17, 700)]),
        "Q24": N("concept", 1560, 400, 190, 56, [("wd:Q24041450", 17, 700), ("Cork Public Museum", 14, 400)]),
        "lit": N("literal", 640, 800, 200, 50, [("“Ogham Stone”", 18, 400)]),
    }
    edges = [
        ("E", "hub", "subject"),
        ("A", "hub", "subject"),
        ("G", "hub", "subject"),
        ("C", "hub", "subject"),
        ("H", "hub", "text", dict(label="text only, no IRI")),
        ("H", "lit", "text", dict(arrow=False)),
        ("E", "T", "creator"),
        ("G", "T", "creator"),
        ("E", "Ho", "creator"),
        ("A", "S", "creator"),
        ("C", "D", "creator"),
        ("C", "Ta", "creator"),
        ("H", "Ta", "creator"),
        ("E", "p62", "spatial"),
        ("A", "p62", "spatial"),
        ("G", "pG", "spatial"),
        ("C", "pC", "spatial"),
        ("G", "Q24", "subject"),
    ]
    p.append(_graph(n, edges))
    # predicate legend under the title
    p.append(_t(360, 250, "dct:subject", 18, 700, FDO_ACCENT) + f'<line x1="478" y1="243" x2="530" y2="243" stroke="{FDO_ACCENT}" stroke-width="4.5"/>')
    p.append(_t(570, 250, "dct:creator", 18, 700, MUTED) + f'<line x1="684" y1="243" x2="736" y2="243" stroke="{MUTED}" stroke-width="3"/>')
    p.append(_t(776, 250, "dct:spatial", 18, 700, FDO_ACCENT_LIGHT) + f'<line x1="890" y1="243" x2="945" y2="243" stroke="{FDO_ACCENT_LIGHT}" stroke-width="3" stroke-dasharray="3 7" stroke-linecap="round"/>')
    p.append(_box_note(60, 778, 470, 96, ["All five: dct:publisher wd:Q73901970 and one", "fdo:context, “Ogham Stones in the Wild and", "in Museums in Ireland”."]))
    p.append(_legend("Registry 253aee9, release 2026-09-03 (dist/fdo-registry.ttl). Dashed = free text or a second node for the same person; CHUIS/1 is missing from Q2016147."))
    return _close(p)


def _box_note(x, y, w, h, lines) -> str:
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{CODE_BG}" stroke="{HALO}" stroke-width="2.5"/>'
    for i, ln in enumerate(lines):
        out += _t(x + 18, y + 30 + i * 25, ln, 18, 400, INK if i == 0 else MUTED)
    return out


# ------------------------------------------------------- slide 2: object --


def _build_object() -> str:
    p = _open()
    p.append(_heading(_glyph_triple(), "One Ogham stone, its 3D FDO and the software", "One hop around each FDO; the link between them is the open point"))

    n = {
        "C": N("fdo3d", 480, 520, 300, 100, [("CO074-148----", 25, 700), ("CIIC 81 · 3DDataFDO", 17, 400), ("subClassOf crmdig:D1_Digital_Object", 15, 400)]),
        "E": N("fdosw", 1270, 520, 330, 100, [("Ogham 3D EpiDoc Extractor", 22, 700), ("SoftwareFDO · v1.1", 17, 400), ("subClassOf crmdig:D14_Software", 15, 400)]),
        "hub": N("concept", 875, 520, 220, 76, [("wd:Q2016147", 22, 700), ("Inscribed Ogham stone", 15, 400)]),
        # around the 3D FDO
        "pC": N("place", 150, 400, 200, 66, [("OSM node", 15, 400), ("11071361392", 17, 700)]),
        "Q121": N("concept", 150, 640, 220, 52, [("wd:Q121592049", 17, 700)]),
        "Di": N("person", 330, 290, 180, 54, [("Distel, A.-K.", 18, 700), ("registry agent", 14, 400)]),
        "Ta": N("person", 560, 270, 180, 54, [("Thiery, F.", 18, 700), ("registry agent", 14, 400)]),
        "lC": N("info", 150, 770, 230, 56, [("CC-BY-NC-SA-4.0", 17, 700)]),
        "fC": N("info", 400, 790, 240, 70, [("50 files · 673 MB", 18, 700), ("model/obj, KIRI Engine", 14, 400)]),
        # around the software
        "Th": N("person", 1060, 270, 180, 54, [("Thiery, F.", 18, 700), ("ORCID", 14, 400)]),
        "Ho": N("person", 1310, 270, 180, 54, [("Homburg, T.", 18, 700), ("ORCID", 14, 400)]),
        "p62": N("place", 1590, 400, 200, 66, [("OSM relation", 15, 400), ("62273", 17, 700)]),
        "Ep": N("concept", 1590, 520, 200, 52, [("wd:Q5382396", 17, 700), ("EpiDoc", 14, 400)]),
        "LO": N("concept", 1590, 625, 200, 52, [("wd:Q18692990", 17, 700), ("Linked Open Data", 14, 400)]),
        "lE": N("info", 1090, 790, 120, 52, [("MIT", 17, 700)]),
        "fE": N("info", 1300, 790, 240, 70, [("254 files · 53 MB", 18, 700), ("codeRepository: GitHub Pages", 14, 400)]),
    }
    edges = [
        ("C", "hub", "subject", dict(label="dct:type")),
        ("E", "hub", "subject", dict(label="dct:type")),
        ("C", "pC", "spatial", dict(label="dct:spatial")),
        ("C", "Q121", "subject", dict(label="dct:subject")),
        ("C", "Di", "creator"),
        ("C", "Ta", "creator"),
        ("C", "lC", "meta", dict(label="dct:license")),
        ("C", "fC", "meta", dict(label="dcat:distribution")),
        ("E", "Th", "creator"),
        ("E", "Ho", "creator"),
        ("E", "p62", "spatial"),
        ("E", "Ep", "subject"),
        ("E", "LO", "subject"),
        ("E", "lE", "meta"),
        ("E", "fE", "meta"),
        # the explicit link that does not exist yet, arching over the shared concept
        ("E", "C", "planned", dict(label="uses: not modelled yet", bend=-190, lpos=0.5)),
    ]
    p.append(_graph(n, edges))
    p.append(_box_note(560, 765, 450, 106, ["What the registry knows today:", "both FDOs are typed with the same concept,", "share fdo:context and publisher. That software", "works on that kind of object is not an edge."]))
    p.append(_legend("Registry 253aee9 (dist/fdo-registry.ttl, registry-index.json). Dashed arc = proposal (e.g. prov:used), not part of the data."))
    return _close(p)


# ----------------------------------------------------- slide 3: registry --


def _build_registry() -> str:
    p = _open()
    p.append(_heading(_glyph_hub(), "The whole registry as one graph", "Eight FDOs, the concepts and people that connect them, and the ones that do not"))

    fdo = lambda kind, x, y, t, s="": N(kind, x, y, 215, 60, [(t, 18, 700), (s, 14, 400)] if s else [(t, 18, 700)])
    n = {
        "E": N("fdosw", 330, 350, 250, 60, [("Ogham 3D EpiDoc Extractor", 17, 700), ("SoftwareFDO", 14, 400)]),
        "A": fdo("fdosw", 330, 570, "Ogham Analysis", "SoftwareFDO"),
        "G": fdo("fdo3d", 720, 260, "GEARS/1", "3DDataFDO"),
        "C": fdo("fdo3d", 1060, 260, "CO074-148----", "3DDataFDO"),
        "H": fdo("fdo3d", 1490, 400, "CHUIS/1", "3DDataFDO"),
        "An": fdo("fdo3d", 1490, 640, "Antholzer See", "3DDataFDO"),
        "B": fdo("fdo3d", 700, 800, "Beuys-Stele B 1036", "3DDataFDO"),
        "F": fdo("fdo3d", 1130, 800, "Freshford well", "3DDataFDO"),
        "q20": N("concept", 875, 480, 290, 76, [("wd:Q2016147", 22, 700), ("Inscribed Ogham stone · 4 FDOs", 15, 400)]),
        "tO": N("person", 470, 250, 190, 54, [("Thiery, F.", 18, 700), ("ORCID · 2 FDOs", 14, 400)]),
        "tA": N("person", 1235, 565, 220, 58, [("Thiery, F.", 18, 700), ("registry agent · 4 FDOs", 14, 400)], dashed=True),
        "osm": N("place", 110, 460, 170, 62, [("OSM relation", 14, 400), ("62273 · 2 FDOs", 16, 700)]),
    }
    edges = [
        ("E", "q20", "subject", dict(arrow=False)), ("A", "q20", "subject", dict(arrow=False)),
        ("G", "q20", "subject", dict(arrow=False)), ("C", "q20", "subject", dict(arrow=False)),
        ("H", "q20", "text", dict(arrow=False, label="text only", lpos=0.8)),
        ("E", "tO", "creator", dict(arrow=False)), ("G", "tO", "creator", dict(arrow=False)),
        ("C", "tA", "creator", dict(arrow=False)), ("H", "tA", "creator", dict(arrow=False)),
        ("An", "tA", "creator", dict(arrow=False)), ("B", "tA", "creator", dict(arrow=False)),
        ("E", "osm", "spatial", dict(arrow=False)), ("A", "osm", "spatial", dict(arrow=False)),
    ]
    p.append(_graph(n, edges))
    p.append(_box_note(60, 690, 330, 150, ["Not connected to the rest:", "Freshford well. It shares no", "concept, place or person with", "another FDO (publisher only)."]))
    p.append(_box_note(1330, 690, 380, 150, ["One person, two nodes:", "Thiery as ORCID and as a", "registry-minted agent. The registry", "never merges on a name."]))
    p.append(_legend("Registry 253aee9, dist/fdo-registry.ttl (7,793 triples). wd:Q22731 (“Stone”, 6 FDOs) is left out for legibility; all eight share dct:publisher wd:Q73901970."))
    return _close(p)


SLIDES = [
    ("fdox-talk-ogham-graph-cluster", _build_cluster),
    ("fdox-talk-ogham-graph-object", _build_object),
    ("fdox-talk-ogham-graph-registry", _build_registry),
]


def _to_rgb(png_path: Path) -> None:
    from PIL import Image

    with Image.open(png_path) as im:
        rgb = im.convert("RGB")
    rgb.save(png_path)


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []
    for name, build_fn in SLIDES:
        svg_path = IMG_DIR / f"{name}.svg"
        svg_path.write_text(build_fn(), encoding="utf-8")
        png_path = svg_path.with_suffix(".png")
        render_svg_to_png(svg_path, png_path, W * OVERSAMPLE, H * OVERSAMPLE)
        _to_rgb(png_path)
        log.append(f"wrote img/{name}.svg + .png ({W*OVERSAMPLE}x{H*OVERSAMPLE}, white background)")
    return log


if __name__ == "__main__":
    for line in run():
        print(line)
