"""S15 -- The story: from the federated KG ecosystem to FDOx, for 3D models and software.

Four 7:4 talk slides (white, S8 convention) that tie the 3D story of "From
Smartphone 3D to Federated Knowledge Graphs" to the software story of the
ArcheoFOSS 2026 talk:

  fdox-talk-story-fkge-map              the FKGE (FDO-driven / LOD-driven) with the four FDOx steps as the bridge
  fdox-talk-story-two-roads-unicorn     two roads, one bundle: CIIC 81 (3D) and the SPARQLing Unicorn plugin (software, planned)
  fdox-talk-story-two-roads-extractor   two roads, one bundle: CIIC 81 (3D) and the Ogham 3D EpiDoc Extractor (software, finished)
  fdox-talk-story-squilly-graph         a drawn nut-and-string graph next to the real registry graph

Sources, all read on 2026-11-05:
  * FKGE columns and terms: the author's FKGE diagram (Thiery & Noback, CC BY 4.0),
    simplified; NFDI4Objects KG as in the N4O tree slide.
  * fdo-3d-packager v1.0.0 steps and fdo-squirrel stages: the author's talk slides 20 and 28.
  * fdo-git-packager: S1 skeleton (steps fetch, inspect, mdcff, bundle, build_fdo), see S11;
    SPARQLing Unicorn tag v0.17.4 = ba8af4c (S11).
  * Registry 253aee9 (release 2026-09-03), dist/registry-index.json:
      CO074-148---- (CIIC 81): 3DDataFDO, DOI 10.5281/zenodo.18724635, 50 files, CC-BY-NC-SA-4.0,
        roles auxiliary 25, data 10, documentation 9, model 4, metadata 2.
      Ogham 3D EpiDoc Extractor: SoftwareFDO, DOI 10.5281/zenodo.18369125, 254 files, MIT,
        roles software 222, script 30, documentation 2.
  * Squilly graph, right half: the S13 registry graph (facts as documented in step_ogham_graph.py).

Nothing here says that fdo-git-packager built the extractor FDO: how it was packaged is not
recorded in the repositories read, so the packager lane is drawn dashed (planned).

Runnable standalone: `python py/step_story.py`
"""

from __future__ import annotations

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
    img_path,
    render_svg_to_png,
)
from step_federation import (  # noqa: E402
    H,
    OVERSAMPLE,
    TINT,
    W,
    _arrow,
    _box,
    _close,
    _glyph_hub,
    _glyph_stack,
    _glyph_triple,
    _heading,
    _legend,
    _open,
    _t,
    _tag,
    _to_rgb,
)

# ------------------------------------------------------- slide 1: FKGE map --


def _pill(x, y, w, text, dashed=False) -> str:
    dash = ' stroke-dasharray="10 7"' if dashed else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="20" fill="white" stroke="{FDO_ACCENT}" stroke-width="3"{dash}/>'
        + _t(x + w / 2, y + 27, text, 19, 400, INK, "middle")
    )


def _step_chip(x, y, step) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="46" height="46" rx="10" fill="{step["color"]}"/>'
        + _t(x + 23, y + 33, step["num"], 28, 700, "white", "middle")
    )


def _build_fkge_map() -> str:
    p = _open()
    p.append(_heading(_glyph_hub(), "From the federated KG ecosystem to FDOx", "Two ways into the graph, one bridge for 3D models and software"))

    # research object on top
    p.append(_box(520, 250, 710, 70, [("A research object: a stone, a 3D model, a piece of software", 22, 700, INK)], center=True))
    p.append(_arrow(520, 285, 395, 345))
    p.append(_arrow(1230, 285, 1355, 345))

    # the two drivers
    for x, title, rows in (
        (50, "FAIR-Digital-Object-driven", ["Measurement", "Analysis & Visualisation", "Conclusion"]),
        (1370, "Linked-Open-Data-driven", ["Capture & Documentation", "Analysis & Enrichment", "Conclusion"]),
    ):
        p.append(_t(x + 165, 372, title, 21, 700, FDO_ACCENT, "middle"))
        for i, r in enumerate(rows):
            p.append(_box(x, 392 + i * 84, 330, 62, [(r, 21, 400, INK)], center=True, fill=TINT))
            if i < 2:
                p.append(_arrow(x + 165, 454 + i * 84, x + 165, 476 + i * 84))

    # the federated knowledge graph in the middle
    cx, cy = 875, 520
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="400" ry="190" fill="{TINT}" stroke="{FDO_ACCENT}" stroke-width="4"/>')
    p.append(_t(cx, cy - 120, "Federated Knowledge Graph", 28, 700, FDO_ACCENT, "middle"))
    hubs = [("Wikidata", -230, -10), ("Wikibase", 230, -10), ("LOD Cloud", 0, 30), ("NFDI4Objects KG", -150, 100), ("OpenStreetMap", 150, 100)]
    for name, dx, dy in hubs:
        for name2, dx2, dy2 in hubs:
            if name < name2:
                p.append(f'<line x1="{cx+dx}" y1="{cy+dy}" x2="{cx+dx2}" y2="{cy+dy2}" stroke="{FDO_ACCENT_SOFT}" stroke-width="2.5" opacity="0.7"/>')
    for name, dx, dy in hubs:
        p.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="17" fill="{FDO_ACCENT}"/>')
        p.append(_t(cx + dx, cy + dy + 42, name, 19, 700, INK, "middle"))
    p.append(_arrow(380, 520, 468, 520))
    p.append(_arrow(1370, 520, 1282, 520))

    # the bridge: four steps
    p.append(f'<rect x="440" y="735" width="870" height="120" rx="16" fill="white" stroke="{FDO_ACCENT}" stroke-width="4"/>')
    p.append(_t(875, 770, "FDOx: the same four steps for every object", 22, 700, INK, "middle"))
    xs = [460, 690, 890, 1085]
    labels = ["Encapsulation", "Modelling", "Linking", "Integration"]
    for step, x, lab in zip(STEPS, xs, labels):
        p.append(_step_chip(x, 790, step))
        p.append(_t(x + 58, 822, lab, 21, 400, INK))
    p.append(_arrow(875, 733, 875, 712))
    # drivers feed the bridge
    p.append(f'<polyline points="215,622 215,795 432,795" fill="none" stroke="{MUTED}" stroke-width="3.5" marker-end="url(#arrow)"/>')
    p.append(f'<polyline points="1535,622 1535,795 1318,795" fill="none" stroke="{MUTED}" stroke-width="3.5" marker-end="url(#arrow)"/>')
    p.append(_pill(50, 690, 330, "3D · Software · Data · Image"))
    p.append(_pill(1370, 690, 330, "3D · Software · Data · Geodata"))

    p.append(_t(60, 950, "Simplified from the FKGE diagram of Thiery & Noback (CC BY 4.0). The four steps are the FDOx four-step pattern.", 19, 400, MUTED))
    return _close(p)


# --------------------------------------------------- slides 2, 3: two roads --

CIIC = dict(
    tag="3D", title="CO074-148---- (CIIC 81)",
    lines=["3DDataFDO · CC-BY-NC-SA-4.0", "DOI 10.5281/zenodo.18724635", "50 files: model 4, data 10, documentation 9,", "auxiliary 25, metadata 2"])


def _lane(y, source, packager, packager_dashed, result, result_dashed) -> str:
    out = ""
    out += _box(50, y, 330, 170, source["rows"], center=True, dashed=source.get("dashed", False))
    out += _box(440, y, 330, 170, packager["rows"], center=True, dashed=packager_dashed)
    out += _box(1180, y, 340, 170, result["rows"], center=True, dashed=result_dashed)
    out += _tag(1192, y + 12, result["tag"], result_dashed)
    out += _arrow(384, y + 85, 434, y + 85)
    out += _arrow(774, y + 85, 828, y + 85)
    out += _arrow(1124, y + 85, 1174, y + 85)
    return out


def _build_two_roads(variant: str) -> str:
    p = _open()
    p.append(_heading(_glyph_stack(), "Two roads, one bundle", "A 3D model and a piece of software end up as the same kind of FDO"))
    p.append(_t(50, 276, "3D model", 22, 700, FDO_ACCENT))
    p.append(_t(50, 506, "Software", 22, 700, FDO_ACCENT))

    y1, y2 = 290, 520
    p.append(_lane(
        y1,
        dict(rows=[("CIIC 81 / UCC 4", 23, 700, INK), (None, 6), ("Sketchfab model of an", 19, 400, MUTED), ("Ogham stone, Cork", 19, 400, MUTED)]),
        dict(rows=[("fdo-3d-packager v1.0.0", 22, 700, INK), (None, 6), ("fetch · convert · nexus", 19, 400, MUTED), ("mdcff · bundle · build_fdo", 19, 400, MUTED)]),
        False,
        dict(tag="3D", rows=[(None, 30), ("CO074-148----", 23, 700, INK), ("DOI 10.5281/zenodo.18724635", 18, 400, MUTED), ("50 files · CC-BY-NC-SA-4.0", 18, 400, MUTED)]),
        False))
    if variant == "unicorn":
        src = dict(rows=[("SPARQLing Unicorn", 23, 700, INK), (None, 6), ("GitHub, tag v0.17.4", 19, 400, MUTED), ("commit ba8af4c", 19, 400, MUTED)])
        pack = dict(rows=[("fdo-git-packager", 22, 700, INK), (None, 6), ("S1 skeleton, no step built:", 19, 400, MUTED), ("fetch · inspect · mdcff · bundle · build_fdo", 16, 400, MUTED)])
        res = dict(tag="SW", rows=[(None, 30), ("SoftwareFDO", 23, 700, INK), ("not built yet", 19, 400, MUTED), ("planned", 19, 400, MUTED)])
        res_dashed = True
        diff_roles = "software files are the code, scripts and documentation"
        foot = "SPARQLing Unicorn QGIS plugin, tag v0.17.4 = ba8af4c (read 2026-11-05); fdo-git-packager is an S1 skeleton."
    else:
        src = dict(rows=[("o3d-epidoc-extractor", 23, 700, INK), (None, 6), ("Ogham in 3D project", 19, 400, MUTED), ("LOD extractor for TEI/EpiDoc", 17, 400, MUTED)])
        pack = dict(rows=[("fdo-git-packager", 22, 700, INK), (None, 6), ("planned for the next ones;", 19, 400, MUTED), ("how this one was packaged", 17, 400, MUTED), ("is not recorded here", 17, 400, MUTED)])
        res = dict(tag="SW", rows=[(None, 30), ("Ogham 3D EpiDoc Extractor", 21, 700, INK), ("DOI 10.5281/zenodo.18369125", 18, 400, MUTED), ("254 files · MIT", 18, 400, MUTED)])
        res_dashed = False
        diff_roles = "software 222, script 30, documentation 2"
        foot = "Registry 253aee9 (release 2026-09-03), registry-index.json; fdo-git-packager is an S1 skeleton."
    p.append(_lane(y2, src, pack, True, res, res_dashed))

    # the shared fdo-squirrel box between the lanes
    p.append(_box(830, 290, 290, 400, [
        ("fdo-squirrel", 26, 700, FDO_ACCENT),
        (None, 10),
        ("MD.cff + CITATION.cff", 19, 400, INK),
        (None, 6),
        ("metadata ingest", 19, 400, MUTED),
        ("schema validation", 19, 400, MUTED),
        ("crosswalk to DCAT", 19, 400, MUTED),
        ("and CIDOC CRM", 19, 400, MUTED),
        ("bundle finalisation", 19, 400, MUTED),
        (None, 12),
        ("one engine for both", 19, 700, INK),
    ], center=True, fill=TINT))

    # shared target
    p.append(_box(1560, 290, 150, 400, [
        ("Zenodo", 21, 700, INK), ("DOI", 18, 400, MUTED), (None, 8),
        ("FDOx", 21, 700, INK), ("Registry", 21, 700, INK), (None, 8),
        ("N4O KG", 21, 700, INK), ("(onboarding open)", 15, 400, MUTED),
    ], center=True))
    p.append(_arrow(1524, 375, 1554, 375))
    p.append(_arrow(1524, 605, 1554, 605))

    p.append(_box(50, 720, 1650, 130, [
        ("What differs, what does not", 23, 700, INK),
        (f"Differs: the type tag (3DDataFDO or SoftwareFDO) and the roles of the files (model and textures; {diff_roles}).", 20, 400, MUTED),
        ("Does not differ: the MD.cff schema, fdo-squirrel, the DOI, the registry record and the way both are queried.", 20, 400, MUTED),
    ]))
    p.append(_legend(foot, "planned or not built yet"))
    return _close(p)


# ------------------------------------------------------ slide 4: Squilly graph --

# the drawn nut-and-string graph: (x, y, rx, ry) per nut, deterministic
NUTS = [(110, 420, 30, 24), (240, 330, 26, 21), (360, 410, 32, 26), (200, 520, 24, 20), (330, 560, 28, 23),
        (450, 500, 25, 21), (150, 640, 26, 21), (290, 700, 31, 25), (430, 650, 24, 20), (500, 360, 22, 18),
        (90, 540, 20, 17)]
STRINGS = [(0, 1), (1, 2), (0, 3), (2, 4), (3, 4), (2, 5), (4, 5), (3, 6), (4, 7), (6, 7), (5, 8), (7, 8), (2, 9), (5, 9), (0, 10), (10, 3)]


def _squilly_graph() -> str:
    out = ""
    for a, b in STRINGS:
        xa, ya = NUTS[a][:2]
        xb, yb = NUTS[b][:2]
        mx, my = (xa + xb) / 2, (ya + yb) / 2 + (8 if (a + b) % 2 else -8)  # a slight sag, like string
        out += f'<path d="M {xa},{ya} Q {mx},{my} {xb},{yb}" fill="none" stroke="{MUTED}" stroke-width="2.5" opacity="0.8"/>'
    for x, y, rx, ry in NUTS:
        out += (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{TINT}" stroke="{FDO_ACCENT_SOFT}" stroke-width="3.5" transform="rotate(-18 {x} {y})"/>'
                f'<ellipse cx="{x-rx*0.3:.1f}" cy="{y-ry*0.3:.1f}" rx="{rx*0.28:.1f}" ry="{ry*0.2:.1f}" fill="white" opacity="0.8" transform="rotate(-18 {x} {y})"/>')
    return out


def _real_graph() -> str:
    """Compact version of the S13 registry graph (facts: see step_ogham_graph.py)."""
    pos = {
        "E": (1010, 330), "A": (1010, 540), "G": (1290, 290), "C": (1510, 330),
        "H": (1600, 500), "An": (1590, 690), "B": (1150, 780), "F": (1420, 800),
        "q": (1260, 450), "o": (860, 440), "t": (1150, 210), "ag": (1400, 640),
    }
    pos = {k: (x, round(325 + (y - 210) * 0.77)) for k, (x, y) in pos.items()}
    fdos = {"E": ("Extractor", "SW"), "A": ("Analysis", "SW"), "G": ("GEARS/1", "3D"), "C": ("CIIC 81", "3D"),
            "H": ("CHUIS/1", "3D"), "An": ("Antholzer See", "3D"), "B": ("Beuys-Stele", "3D"), "F": ("Freshford", "3D")}
    edges = [("E", "q", FDO_ACCENT, ""), ("A", "q", FDO_ACCENT, ""), ("G", "q", FDO_ACCENT, ""), ("C", "q", FDO_ACCENT, ""),
             ("E", "o", FDO_ACCENT_LIGHT, "3 7"), ("A", "o", FDO_ACCENT_LIGHT, "3 7"),
             ("E", "t", MUTED, ""), ("G", "t", MUTED, ""),
             ("C", "ag", MUTED, ""), ("H", "ag", MUTED, ""), ("An", "ag", MUTED, ""), ("B", "ag", MUTED, ""),
             ("H", "q", MUTED, "10 8")]
    out = ""
    for a, b, col, dash in edges:
        d = f' stroke-dasharray="{dash}" stroke-linecap="round"' if dash else ""
        out += f'<line x1="{pos[a][0]}" y1="{pos[a][1]}" x2="{pos[b][0]}" y2="{pos[b][1]}" stroke="{col}" stroke-width="3.5"{d}/>'
    for k, (name, kind) in fdos.items():
        x, y = pos[k]
        fill = FDO_ACCENT if kind == "3D" else "white"
        ink = "white" if kind == "3D" else INK
        out += (f'<rect x="{x-80}" y="{y-26}" width="160" height="52" rx="12" fill="{fill}" stroke="{FDO_ACCENT}" stroke-width="4"/>'
                + _t(x, y + 7, name, 18, 700, ink, "middle"))
    x, y = pos["q"]
    out += f'<rect x="{x-105}" y="{y-30}" width="210" height="60" rx="30" fill="{TINT}" stroke="{FDO_ACCENT_SOFT}" stroke-width="3.5"/>'
    out += _t(x, y - 2, "wd:Q2016147", 19, 700, INK, "middle") + _t(x, y + 20, "Inscribed Ogham stone", 14, 400, MUTED, "middle")
    x, y = pos["o"]
    out += f'<ellipse cx="{x}" cy="{y}" rx="80" ry="34" fill="white" stroke="{FDO_ACCENT_LIGHT}" stroke-width="3" stroke-dasharray="3 6" stroke-linecap="round"/>'
    out += _t(x, y - 2, "OSM relation", 14, 400, MUTED, "middle") + _t(x, y + 18, "62273", 17, 700, INK, "middle")
    x, y = pos["t"]
    out += f'<ellipse cx="{x}" cy="{y}" rx="80" ry="30" fill="white" stroke="{MUTED}" stroke-width="3"/>' + _t(x, y + 6, "Thiery (ORCID)", 16, 700, INK, "middle")
    x, y = pos["ag"]
    out += f'<ellipse cx="{x}" cy="{y}" rx="92" ry="30" fill="white" stroke="{MUTED}" stroke-width="3" stroke-dasharray="12 8"/>' + _t(x, y + 6, "Thiery (agent)", 16, 700, INK, "middle")
    return out


def _build_squilly() -> str:
    p = _open()
    p.append(_heading(_glyph_triple(), "From Squilly’s nut-and-string graph to a real one", "Eight FDOs, the concepts and people that connect them: real triples of the registry"))
    p.append(_t(300, 275, "The sketch: nuts and string", 24, 700, FDO_ACCENT, "middle"))
    p.append(_squilly_graph())
    p.append(_t(300, 780, "“FAIR Digital Objects”", 20, 400, MUTED, "middle"))
    p.append(_t(300, 806, "a picture of what we want", 18, 400, MUTED, "middle"))
    p.append(_arrow(580, 520, 770, 520))
    p.append(_t(675, 490, "becomes", 20, 400, MUTED, "middle"))
    p.append(_t(1235, 275, "The registry today: 3D models and software", 24, 700, FDO_ACCENT, "middle"))
    p.append(_real_graph())
    p.append(_legend(
        "Registry 253aee9 (release 2026-09-03), dist/fdo-registry.ttl, 7,793 triples; graph facts as on the Ogham graph slide. "
        "Freshford shares nothing with the others. The sketch is drawn, not data.",
        "free text, or an agent the registry minted"))
    return _close(p)


# --------------------------------------------------------------------- run --

SLIDES = [
    ("fdox-talk-story-fkge-map", _build_fkge_map),
    ("fdox-talk-story-two-roads-unicorn", lambda: _build_two_roads("unicorn")),
    ("fdox-talk-story-two-roads-extractor", lambda: _build_two_roads("extractor")),
    ("fdox-talk-story-squilly-graph", _build_squilly),
]


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []
    for name, build_fn in SLIDES:
        svg_path = img_path(f"{name}.svg")
        svg_path.write_text(build_fn(), encoding="utf-8")
        png_path = svg_path.with_suffix(".png")
        render_svg_to_png(svg_path, png_path, W * OVERSAMPLE, H * OVERSAMPLE)
        _to_rgb(png_path)
        log.append(f"wrote {svg_path.relative_to(IMG_DIR.parent).as_posix()} + .png ({W*OVERSAMPLE}x{H*OVERSAMPLE}, white background)")
    return log


if __name__ == "__main__":
    for line in run():
        print(line)
