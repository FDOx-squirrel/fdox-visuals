"""S12 -- Finished 3D and software FDOs in the federated KG ecosystem.

Three 7:4 talk slides (white, S8 convention) for the ArcheoFOSS 2026 talk
("From Fragmented Objects to Federated Knowledge"): what happens to the
*finished* FDOs, 3D and software alike, once they leave the packagers.

  img/fdox-talk-federation-path.svg/.png             FDO -> Zenodo -> Registry -> N4O KG -> ecosystem
  img/fdox-talk-federation-catalogue.svg/.png        one catalogue, two kinds of FDO (real table)
  img/fdox-talk-federation-shared-concepts.svg/.png  what the graph links, and what it does not (real query)

Nothing here is invented. Values come from the repositories as read on
2026-11-05 (shallow clones, `FDOx-squirrel/fdo-squirrel-registry` at
253aee9 = release 2026-09-03; `FDOx-squirrel/fdox-squirrel-n4o-collection`
at 882a5f7 = 2026-09-04):
  * registry-index.json: 8 FDOs in the catalogue (6 x 3DDataFDO, 2 x
    SoftwareFDO), 599 files, titles, licences, file counts; `dist/fdo-registry.ttl`
    has 7,793 triples. A ninth pinned record ("Heinz Eau") has no
    fdo-metadata.ttl in its package and is not in the catalogue.
  * metadata/crm_bridge.ttl: fdo:3DDataFDO subClassOf crmdig:D1_Digital_Object,
    fdo:SoftwareFDO subClassOf crmdig:D14_Software.
  * the registry's own `shared-concepts` query (queries.yaml), run with
    rdflib on dist/fdo-registry.ttl: wd:Q22731 is the dct:subject of 6 FDOs,
    wd:Q2016147 of 4 (Ogham 3D EpiDoc Extractor, Ogham Analysis, GEARS/1,
    CO074-148----). CHUIS/1 carries "Ogham Stone" only as free text.
    Beuys-Stele and Freshford share no Wikidata concept with another FDO.
    OSM relation 62273 is the dct:spatial of both software FDOs.
  * N4O collection: VoID in dist/metadata.ttl counts 5 x 3DDataFDO and
    2 x SoftwareFDO (the bundle of 2026-09-04, older than the registry's
    8-FDO release). VZG's manual onboarding and the real collection URI are
    still open in that repository's README (status 2026-09-04), so the KG
    step is drawn dashed.

Solid outline = exists and was checked; dashed = pending or planned.
`jupyter-nb-lod` is the second software repository named in the abstract;
it is not in the registry yet, so it is drawn dashed.

One brand colour (S7/S11 precedent).

Runnable standalone: `python py/step_federation.py`
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
    arrow_line,
    arrow_marker,
    ensure_dirs,
    esc,
    font_face_css,
    render_svg_to_png,
)

TINT = STEPS[0]["tint"]
CODE_BG = "#F5F7FA"
W, H = 1750, 1000
OVERSAMPLE = 2

# (record id, title as in the registry, type, licence, files)
FDOS = [
    ("18369126", "Ogham 3D EpiDoc Extractor", "SW", "MIT", 254),
    ("18369157", "Ogham Analysis", "SW", "MIT", 117),
    ("18369866", "GEARS/1", "3D", "CC-BY-SA-4.0", 7),
    ("22675886", "CO074-148---- (CIIC 81)", "3D", "CC-BY-NC-SA-4.0", 50),
    ("18744583", "CHUIS/1", "3D", "CC-BY-SA-4.0", 10),
    ("18732893", "Steinmännchen / Antholzer See", "3D", "CC-BY-4.0", 64),
    ("18742694", "Beuys-Stele B 1036 (Kassel)", "3D", "CC-BY-4.0", 47),
    ("22676380", "Freshford: St Lachtain’s Well", "3D", "CC-BY-4.0", 50),
]
# which FDOs have which Wikidata concept as dct:subject (real query result)
Q2016147 = {"18369126", "18369157", "18369866", "22675886"}
Q22731 = {"18369126", "18369157", "18369866", "22675886", "18744583", "18732893"}

# ------------------------------------------------------------------ helpers --


def _t(x, y, s, size, weight=400, fill=INK, anchor="start") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Fira Sans" font-weight="{weight}" '
        f'font-size="{size}" fill="{fill}">{esc(s)}</text>'
    )


def _open() -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>',
        font_face_css(),
        arrow_marker("arrow", MUTED),
    ]


def _glyph_hub() -> str:
    c = FDO_ACCENT
    out = "".join(
        f'<line x1="0" y1="0" x2="{x}" y2="{y}" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
        for x, y in ((0, -56), (54, 30), (-54, 30))
    )
    out += "".join(f'<circle cx="{x}" cy="{y}" r="13" fill="{c}"/>' for x, y in ((0, -56), (54, 30), (-54, 30)))
    return out + f'<circle cx="0" cy="0" r="17" fill="white" stroke="{c}" stroke-width="6"/>'


def _glyph_stack() -> str:
    c = FDO_ACCENT
    out = ""
    for dy in (-34, 0, 34):
        out += f'<rect x="-52" y="{dy-14}" width="104" height="28" rx="8" fill="white" stroke="{c}" stroke-width="6"/>'
        out += f'<circle cx="-34" cy="{dy}" r="5" fill="{c}"/>'
    return out


def _glyph_triple() -> str:
    c = FDO_ACCENT
    return (
        f'<line x1="0" y1="-52" x2="-52" y2="38" stroke="{c}" stroke-width="6"/>'
        f'<line x1="0" y1="-52" x2="52" y2="38" stroke="{c}" stroke-width="6"/>'
        f'<line x1="-52" y1="38" x2="52" y2="38" stroke="{c}" stroke-width="6" stroke-dasharray="3 10" stroke-linecap="round"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="14" fill="{c}"/>' for x, y in ((0, -52), (-52, 38), (52, 38)))
    )


def _heading(glyph: str, title: str, sub: str) -> str:
    """Badge top-left (S8 position and scale), no number: these are not steps."""
    return (
        f'<g transform="translate(175,165) scale(0.56)">'
        f'<circle cx="0" cy="0" r="150" fill="{TINT}" stroke="{FDO_ACCENT}" stroke-width="7"/>'
        f'<g transform="scale(1.05)">{glyph}</g></g>'
        + _t(310, 150, title, 58, 700, FDO_ACCENT)
        + _t(310, 202, sub, 30, 400, MUTED)
    )


def _box(x, y, w, h, rows, dashed=False, fill="white", stroke=FDO_ACCENT, center=False, pad=22) -> str:
    dash = ' stroke-dasharray="14 9"' if dashed else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3.5"{dash}/>'

    def hh(r):
        return r[1] if r[0] is None else r[1] * 1.38

    cy = y + (h - sum(hh(r) for r in rows)) / 2 if center else y + pad
    for r in rows:
        if r[0] is None:
            cy += r[1]
            continue
        text, size, weight, color = r[:4]
        indent = r[4] if len(r) > 4 else 0
        if center:
            out += _t(x + w / 2, cy + size, text, size, weight, color, "middle")
        else:
            out += _t(x + pad + indent, cy + size, text, size, weight, color)
        cy += size * 1.38
    return out


def _tag(x, y, kind: str, dashed=False) -> str:
    """Small type tag: 3D or SW (software)."""
    d = ' stroke-dasharray="6 4"' if dashed else ""
    return (
        f'<rect x="{x}" y="{y}" width="48" height="30" rx="8" fill="{FDO_ACCENT if kind == "3D" else "white"}" '
        f'stroke="{FDO_ACCENT}" stroke-width="3"{d}/>'
        + _t(x + 24, y + 22, kind, 18, 700, "white" if kind == "3D" else FDO_ACCENT, "middle")
    )


def _legend(note: str, extra: str = "") -> str:
    ly = 880
    return (
        f'<rect x="60" y="{ly}" width="62" height="34" rx="9" fill="white" stroke="{FDO_ACCENT}" stroke-width="3.5"/>'
        + _t(140, ly + 25, "exists, checked in the repositories", 22)
        + f'<rect x="560" y="{ly}" width="62" height="34" rx="9" fill="white" stroke="{FDO_ACCENT}" '
        f'stroke-width="3.5" stroke-dasharray="14 9"/>'
        + _t(640, ly + 25, extra or "pending or planned", 22)
        + _t(60, 950, note, 19, 400, MUTED)
    )


def _close(p: list[str]) -> str:
    p.append("</svg>")
    return "\n".join(p)


def _arrow(x1, y1, x2, y2) -> str:
    return arrow_line(x1, y1, x2, y2, width=3.5)


# ---------------------------------------------------------- slide 1: path --


def _build_path() -> str:
    p = _open()
    p.append(_heading(_glyph_hub(), "From packaged FDOs to the federated KG", "3D models and software take the same road"))

    # column 1: the finished FDOs
    p.append(_box(50, 300, 400, 540, [("Finished FDOs", 25, 700, INK)], pad=18))
    y = 358
    for kind, title, dashed in (
        ("3D", "CO074-148---- (CIIC 81)", False),
        ("3D", "GEARS/1 · CHUIS/1", False),
        ("3D", "Beuys-Stele · Antholzer See", False),
        ("3D", "Freshford: St Lachtain’s Well", False),
        ("SW", "Ogham 3D EpiDoc Extractor", False),
        ("SW", "Ogham Analysis", False),
        ("SW", "jupyter-nb-lod", True),
    ):
        p.append(_box(70, y, 360, 52, [], dashed=dashed))
        p.append(_tag(80, y + 11, kind, dashed))
        p.append(_t(138, y + 34, title, 20, 400, INK))
        y += 56
    p.append(_t(70, 785, "6 × 3D, 2 × SW in the registry;", 17, 400, MUTED))
    p.append(_t(70, 807, "jupyter-nb-lod: via fdo-git-packager, planned", 17, 400, MUTED))

    cols = [
        (500, "Zenodo", ["one record per FDO,", "version DOI, bundle ZIP", "with fdo-metadata.ttl"], False),
        (778, "FDOx Registry", ["harvests the ZIPs,", "DCAT + CIDOC CRM,", "SHACL gate: 7,793 triples"], False),
        (1056, "N4O collection", ["fdox-squirrel-n4o-collection", "→ n4o-kg-profile", "VZG onboarding: open"], True),
    ]
    for x, title, lines, dashed in cols:
        rows = [(title, 27, 700, INK), (None, 8)] + [(ln, 17.5 if len(ln) > 24 else 20, 400, MUTED) for ln in lines]
        p.append(_box(x, 400, 250, 250, rows, dashed=dashed, center=True))
    p.append(_arrow(458, 525, 492, 525))
    p.append(_arrow(756, 525, 770, 525))
    p.append(_arrow(1034, 525, 1048, 525))

    # column 5: the ecosystem
    p.append(_box(1360, 300, 340, 520, [("Federated KG ecosystem", 25, 700, INK)], pad=18, dashed=True))
    eco = [
        ("NFDI4Objects KG", "collection via VZG", True),
        ("Wikidata", "dct:subject: Q2016147 …", False),
        ("OpenStreetMap", "dct:spatial: relation 62273", False),
        ("SquirrelBase", "Q56, Q60 on two 3D FDOs", False),
        ("CIDOC CRM / CRMdig", "D1 Digital Object, D14 Software", False),
    ]
    y = 350
    for title, sub, dashed in eco:
        p.append(_box(1378, y, 304, 78, [(title, 22, 700, INK), (sub, 17, 400, MUTED)], dashed=dashed, center=True))
        y += 92
    p.append(_arrow(1316, 525, 1352, 525))


    p.append(_t(500, 715, "Both kinds of FDO pass the same gates:", 21, 700, INK))
    p.append(_t(500, 745, "the registry reads a 3DDataFDO and a SoftwareFDO with one pipeline;", 20, 400, INK))
    p.append(_t(500, 773, "the KG only ever sees the registry’s CRM-anchored bundle.", 20, 400, INK))
    p.append(_legend(
        "Read 2026-11-05: fdo-squirrel-registry 253aee9 (release 2026-09-03), fdox-squirrel-n4o-collection 882a5f7 "
        "(README status 2026-09-04).",
        "pending or planned (N4O onboarding by VZG, jupyter-nb-lod)"))
    return _close(p)


# ---------------------------------------------------- slide 2: catalogue --


def _build_catalogue() -> str:
    p = _open()
    p.append(_heading(_glyph_stack(), "One catalogue, two kinds of FDO", "The registry’s own overview query lists them side by side"))

    x0, y0, rh = 60, 300, 56
    cols = [("Type", 60), ("FDO", 130), ("Licence", 590), ("Files", 880)]
    p.append(f'<rect x="{x0}" y="{y0-44}" width="900" height="44" fill="{TINT}"/>')
    for name, dx in cols:
        p.append(_t(x0 + dx - 50 + 20, y0 - 14, name, 20, 700, FDO_ACCENT, "end" if name == "Files" else "start"))
    y = y0
    for _, title, kind, lic, files in FDOS:
        p.append(f'<line x1="{x0}" y1="{y+rh}" x2="{x0+900}" y2="{y+rh}" stroke="#D9DEE6" stroke-width="2"/>')
        p.append(_tag(x0 + 20, y + 13, kind))
        p.append(_t(x0 + 100, y + 36, title, 23, 400, INK))
        p.append(_t(x0 + 560, y + 36, lic, 22, 400, MUTED))
        p.append(_t(x0 + 880, y + 36, str(files), 22, 400, MUTED, "end"))
        y += rh
    p.append(_t(x0, y + 36, "8 FDOs · 599 files · 7,793 triples · release 2026-09-03", 22, 700, FDO_ACCENT))

    # right: the same two classes in CIDOC CRM
    p.append(_box(1010, 255, 690, 190, [
        ("fdo:3DDataFDO", 25, 700, INK),
        ("rdfs:subClassOf crmdig:D1_Digital_Object", 20, 400, MUTED),
        (None, 14),
        ("fdo:SoftwareFDO", 25, 700, INK),
        ("rdfs:subClassOf crmdig:D14_Software", 20, 400, MUTED),
    ]))
    p.append(_box(1010, 475, 690, 220, [
        ("Same query, same shape", 25, 700, INK),
        (None, 8),
        ("Every row is a dcat:Dataset with a licence and", 20, 400, MUTED),
        ("distributions, whatever it describes. A model of a", 20, 400, MUTED),
        ("stone and the code that extracts its inscription", 20, 400, MUTED),
        ("are found, filtered and counted the same way.", 20, 400, MUTED),
    ]))
    p.append(_legend(
        "Registry query “Every FDO with its type, licence and file count” (queries.yaml); values from registry-index.json. "
        "A ninth pinned record has no fdo-metadata.ttl."))
    return _close(p)


# ------------------------------------------------ slide 3: shared concepts --


def _build_shared() -> str:
    p = _open()
    p.append(_heading(_glyph_triple(), "What the graph links, and what it does not", "Registry query: Wikidata concepts that more than one FDO points at"))

    rx, rw, rh, gap, y0 = 60, 600, 54, 8, 270
    pos = {}
    for i, (rid, title, kind, _, _) in enumerate(FDOS):
        y = y0 + i * (rh + gap)
        pos[rid] = (rx + rw, y + rh / 2)
        p.append(_box(rx, y, rw, rh, []))
        p.append(_tag(rx + 12, y + 12, kind))
        p.append(_t(rx + 74, y + 35, title, 22, 400, INK))

    hubs = [
        ("18369126", "wd:Q2016147", "4 FDOs", Q2016147, 800, 370, FDO_ACCENT),
        ("18369157", "wd:Q22731", "6 FDOs", Q22731, 800, 640, FDO_ACCENT_SOFT),
    ]
    hub_pos = {}
    for _, name, count, members, hx, hy, col in hubs:
        hub_pos[name] = (hx, hy)
    # edges first, nodes on top
    for _, name, count, members, hx, hy, col in hubs:
        for rid, (ex, ey) in pos.items():
            if rid in members:
                p.append(f'<line x1="{ex}" y1="{ey}" x2="{hx}" y2="{hy}" stroke="{col}" stroke-width="3.5"/>')
    for _, name, count, members, hx, hy, col in hubs:
        p.append(f'<rect x="{hx}" y="{hy-42}" width="260" height="84" rx="14" fill="{TINT}" stroke="{col}" stroke-width="4"/>')
        p.append(_t(hx + 130, hy - 4, name, 25, 700, INK, "middle"))
        p.append(_t(hx + 130, hy + 26, count, 20, 400, MUTED, "middle"))
    p.append(_t(930, 308, "“Ogham stone”", 20, 400, MUTED, "middle"))
    p.append(_t(930, 708, "label in the bundle: “Stone”", 20, 400, MUTED, "middle"))

    # CHUIS/1: free text only, dashed edge to a literal
    cy = y0 + 4 * (rh + gap) + rh / 2
    p.append(f'<line x1="{rx+rw}" y1="{cy}" x2="1090" y2="{cy+4}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 8"/>')
    p.append(_box(1090, cy - 24, 200, 52, [("“Ogham Stone”", 20, 400, MUTED)], dashed=True, stroke=MUTED, center=True))

    p.append(_box(1330, 255, 370, 200, [
        ("What this shows", 24, 700, INK),
        (None, 6),
        ("3D models and software share", 19, 400, MUTED),
        ("concepts, so a query from one", 19, 400, MUTED),
        ("finds the other: the extractor,", 19, 400, MUTED),
        ("the analysis and two stones.", 19, 400, MUTED),
    ]))
    p.append(_box(1330, 490, 370, 240, [
        ("What it does not", 24, 700, FDO_ACCENT),
        (None, 6),
        ("CHUIS/1 says “Ogham Stone” as text", 19, 400, MUTED),
        ("only and is missing from Q2016147.", 19, 400, MUTED),
        ("The Beuys stele and the Freshford", 19, 400, MUTED),
        ("well share no concept with another", 19, 400, MUTED),
        ("FDO. The query makes that visible.", 19, 400, MUTED),
    ], dashed=True))
    p.append(_t(60, 790, "Also shared: both software FDOs carry OSM relation 62273 as dct:spatial.", 21, 400, INK))
    p.append(_legend(
        "Registry query “Wikidata concepts that more than one FDO points at” (queries.yaml, shared-concepts), run on "
        "dist/fdo-registry.ttl (7,793 triples), 2026-11-05.",
        "free text, no concept IRI"))
    return _close(p)


# --------------------------------------------------------------------- run --

SLIDES = [
    ("fdox-talk-federation-path", _build_path),
    ("fdox-talk-federation-catalogue", _build_catalogue),
    ("fdox-talk-federation-shared-concepts", _build_shared),
]


def _to_rgb(png_path: Path) -> None:
    from PIL import Image  # lazy, same reasoning as visuals_utils

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
