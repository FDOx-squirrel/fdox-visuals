"""S9 -- Talk purpose slides: the four-outcome pattern, one slide each.

Companion to S7's purpose *banner* (all four outcomes side by side, at a
glance) the same way S8 is to S2: one full 7:4 slide per outcome,
substantiated with real data (the live FDOx Registry, CIIC 81's real TTL,
a real SPARQL query and its real result graph) instead of S7's abstract
icon+description. Built for the FAIR 3D Heritage Conference talk (Mainz,
2026-09-14/16), Part 5.

Produces (white background, see S8 docstring for why that differs from
the transparent-icon convention elsewhere in this repo):
  img/fdox-talk-purpose1-fair-citable.png
  img/fdox-talk-purpose2-semantically-queryable.png
  img/fdox-talk-purpose3-interoperable.png
  img/fdox-talk-purpose4-integrable.png

Deliberately screenshot-free (Flo, 2026-09-09: "eher eine eigene Grafik...
den Reviewern gerecht wird" -- after S8-style Sketchfab/registry crops
were tried for two of these and felt like a step backwards here): every
one of the four is hand-drawn SVG from real values, nothing composited.

Runnable standalone: `python py/step_talk_purpose.py`
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals_utils import (  # noqa: E402
    FDO_ACCENT,
    FDO_ACCENT_LIGHT,
    IMG_DIR,
    INK,
    MUTED,
    arrow_line,
    arrow_marker,
    ensure_dirs,
    esc,
    font_face_css,
    measure_content_margins,
    render_svg_to_png,
)

TINT = "#E6ECF1"
ACCENT = FDO_ACCENT
ACCENT_LIGHT = FDO_ACCENT_LIGHT

W, H = 1750, 1000
OVERSAMPLE = 2

ICON_CX = 150


def _badge_gradient_defs() -> str:
    return (
        '<defs><linearGradient id="talkPurposeGrad" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{ACCENT_LIGHT}"/><stop offset="100%" stop-color="{ACCENT}"/>'
        "</linearGradient></defs>"
    )


def _badge_icon_1(cy: float, scale: float) -> str:
    """FAIR & Citable -- same certificate glyph as S7's purpose-1 icon,
    reproduced at this module's own scale/tag convention (S7's own
    `_icon_document` is tuned for `ICON_S = ICON_R/78`; re-deriving it
    inline keeps this module self-contained since the corner tag here
    sits top-left, not top-right as in S7's banner badges).
    """
    return (
        '<path d="M -43.6 -53.8 h 64.1 l 23.1 23.1 v 84.6 h -87.2 z" fill="none" stroke="#FFFFFF" '
        'stroke-width="6.4" stroke-linejoin="round"/>'
        '<path d="M 20.5 -53.8 v 23.1 h 23.1 z" fill="#FFFFFF" opacity="0.85"/>'
        '<line x1="-28.2" y1="-20.5" x2="25.6" y2="-20.5" stroke="#FFFFFF" stroke-width="5.1" stroke-linecap="round"/>'
        '<line x1="-28.2" y1="-5.1" x2="25.6" y2="-5.1" stroke="#FFFFFF" stroke-width="5.1" stroke-linecap="round"/>'
        '<path d="M -28.2 12.8 l 11.5 11.5 l 21.8 -21.8" fill="none" stroke="#FFFFFF" stroke-width="6.4" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def _badge_icon_2() -> str:
    """Semantically Queryable -- RDF triple glyph, same shape as S7's."""
    return (
        '<line x1="0" y1="-59" x2="-59" y2="41" stroke="#FFFFFF" stroke-width="5.1"/>'
        '<line x1="0" y1="-59" x2="59" y2="41" stroke="#FFFFFF" stroke-width="5.1"/>'
        '<line x1="-59" y1="41" x2="59" y2="41" stroke="#FFFFFF" stroke-width="5.1" '
        'stroke-dasharray="2 7" stroke-linecap="round"/>'
        '<circle cx="0" cy="-59" r="14.1" fill="#FFFFFF"/><circle cx="-59" cy="41" r="14.1" fill="#FFFFFF"/>'
        '<circle cx="59" cy="41" r="14.1" fill="#FFFFFF"/>'
    )


def _badge_icon_3() -> str:
    """Interoperable -- four-spoke hub glyph, same shape as S7's."""
    return (
        '<line x1="0" y1="0" x2="0" y2="-66.7" stroke="#FFFFFF" stroke-width="5.1"/>'
        '<line x1="0" y1="0" x2="66.7" y2="0" stroke="#FFFFFF" stroke-width="5.1"/>'
        '<line x1="0" y1="0" x2="0" y2="66.7" stroke="#FFFFFF" stroke-width="5.1"/>'
        '<line x1="0" y1="0" x2="-66.7" y2="0" stroke="#FFFFFF" stroke-width="5.1"/>'
        '<circle cx="0" cy="-66.7" r="11.5" fill="#FFFFFF"/><circle cx="66.7" cy="0" r="11.5" fill="#FFFFFF"/>'
        '<circle cx="0" cy="66.7" r="11.5" fill="#FFFFFF"/><circle cx="-66.7" cy="0" r="11.5" fill="#FFFFFF"/>'
        '<circle cx="0" cy="0" r="15.4" fill="#FFFFFF"/>'
    )


def _badge_icon_4() -> str:
    """Integrable -- three linked clusters glyph, same shape as S7's."""
    clusters = [(-51.3, -35.9), (53.8, -25.6), (-7.7, 56.4)]
    out = ""
    for a, b in ((0, 1), (1, 2), (2, 0)):
        (x1, y1), (x2, y2) = clusters[a], clusters[b]
        out += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFFFFF" stroke-width="4.5"/>'
    for x, y in clusters:
        out += f'<circle cx="{x}" cy="{y}" r="20.5" fill="none" stroke="#FFFFFF" stroke-width="4.5"/>'
        out += f'<circle cx="{x}" cy="{y}" r="6.4" fill="#FFFFFF"/>'
    return out


_BADGE_ICONS = [
    lambda: _badge_icon_1(0, 1),
    _badge_icon_2,
    _badge_icon_3,
    _badge_icon_4,
]


def _icon_svg(num: int, cy: float, scale: float = 0.6) -> str:
    """Corner badge: gradient circle + glyph + numbered tag, top-left,
    same visual language as S7's banner badges (PRIMER S7) but laid out
    for a single corner rather than a row of four.
    """
    out = f'<g transform="translate({ICON_CX},{cy}) scale({scale})">'
    out += '<circle cx="0" cy="0" r="100" fill="url(#talkPurposeGrad)"/>'
    out += '<circle cx="0" cy="0" r="100" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.35"/>'
    out += _BADGE_ICONS[num - 1]()
    out += f'<circle cx="72" cy="-72" r="30" fill="#FFFFFF" stroke="{ACCENT}" stroke-width="3.5"/>'
    out += (f'<text x="72" y="-62" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
            f'font-size="29" fill="{ACCENT}">{num}</text></g>')
    return out


def _icon_exclude_box(cy: float, scale: float) -> tuple[int, int, int, int]:
    r = 100 * scale * OVERSAMPLE
    cx_px, cy_px = ICON_CX * OVERSAMPLE, cy * OVERSAMPLE
    return (int(cx_px - r), int(cy_px - r * 1.4), int(cx_px + r * 1.4), int(cy_px + r))


def _svg_open() -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>',
        font_face_css(),
        arrow_marker("arrow", ACCENT_LIGHT),
        _badge_gradient_defs(),
    ]


# -------------------------------------------------------------- Purpose 1 --
# CIIC 81's real CITATION.cff-derived values as a citation card, plus a
# chip row for four of the other seven real, DOI-cited registry sources,
# plus the real licence distribution from the registry's own filter.
_OTHER_SOURCES = [
    ("Lago di Anterselva cairn", "zenodo.18732892"),
    ("Cologne Heinzelm\u00e4nnchen", "zenodo.18740523"),
    ("Kassel Beuys stele", "zenodo.18742693"),
    ("GEARS/1", "zenodo.18369865"),
]
_LICENCES = [("CC-BY-4.0", 3, 3), ("CC-BY-SA-4.0", 2, 3), ("CC-BY-NC-SA-4.0", 1, 3)]


def _build_purpose1(hshift: int, vshift: int) -> str:
    p = _svg_open()
    p.append(_icon_svg(1, 145, 0.62))
    p.append(f'<g transform="translate({hshift},{vshift})">')

    card_x, card_y, card_w, card_h = 60, 260, 900, 430
    p.append(f'<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="16" fill="{TINT}" '
              f'stroke="{ACCENT}" stroke-width="3"/>')
    p.append(f'<text x="{card_x+40}" y="{card_y+52}" font-family="Fira Sans" font-weight="700" font-size="26" '
              f'fill="{ACCENT}">CITATION.cff \u2014 CIIC 81 (real)</text>')
    fields = [
        ("title", "CO074-148---- (Ogham Stone, UCC Stone Corridor)"),
        ("doi", "10.5281/zenodo.18724635"),
        ("authors", "Distel, Anne-Karoline \u00b7 Thiery, Florian"),
        ("publisher", "Research Squirrel Engineers Network (wd:Q73901970)"),
        ("license", "CC-BY-NC-SA-4.0"),
        ("date-released", "2024-06-05"),
    ]
    fy = card_y + 92
    for label, val in fields:
        p.append(f'<text x="{card_x+40}" y="{fy}" font-family="Fira Sans" font-weight="700" font-size="20" '
                  f'fill="{INK}">{esc(label)}</text>')
        p.append(f'<text x="{card_x+225}" y="{fy}" font-family="Fira Sans" font-weight="400" font-size="20" '
                  f'fill="{MUTED}">{esc(val)}</text>')
        fy += 53

    p.append(f'<text x="{card_x}" y="{card_y+card_h+50}" font-family="Fira Sans" font-weight="700" font-size="24" '
              f'fill="{ACCENT}">+ 7 more real, DOI-cited sources in the registry</text>')
    chip_y = card_y + card_h + 78
    chip_w, chip_h, chip_gap = 210, 78, 14
    chip_x = card_x
    for name, doi in _OTHER_SOURCES:
        p.append(f'<rect x="{chip_x}" y="{chip_y}" width="{chip_w}" height="{chip_h}" rx="10" fill="white" '
                  f'stroke="{ACCENT_LIGHT}" stroke-width="2.5"/>')
        p.append(f'<text x="{chip_x+14}" y="{chip_y+32}" font-family="Fira Sans" font-weight="700" font-size="16" '
                  f'fill="{INK}">{esc(name)}</text>')
        p.append(f'<text x="{chip_x+14}" y="{chip_y+56}" font-family="Fira Sans" font-weight="400" font-size="15" '
                  f'fill="{MUTED}">{esc(doi)}</text>')
        chip_x += chip_w + chip_gap
    sum_w = 300
    p.append(f'<rect x="{chip_x}" y="{chip_y}" width="{sum_w}" height="{chip_h}" rx="10" fill="{ACCENT}"/>')
    p.append(f'<text x="{chip_x+sum_w/2}" y="{chip_y+32}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="700" font-size="16" fill="white">+ 3 more</text>')
    p.append(f'<text x="{chip_x+sum_w/2}" y="{chip_y+56}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="400" font-size="14" fill="{TINT}">incl. 2 software FDOs</text>')

    badge_x, badge_y, badge_r = 1290, 350, 190
    p.append(f'<circle cx="{badge_x}" cy="{badge_y}" r="{badge_r}" fill="{TINT}" stroke="{ACCENT}" stroke-width="3"/>')
    p.append(f'<text x="{badge_x}" y="{badge_y-58}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
              f'font-size="86" fill="{ACCENT}">8</text>')
    p.append(f'<text x="{badge_x}" y="{badge_y+4}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
              f'font-size="26" fill="{INK}">real sources</text>')
    p.append(f'<text x="{badge_x}" y="{badge_y+40}" text-anchor="middle" font-family="Fira Sans" font-weight="400" '
              f'font-size="21" fill="{MUTED}">each with a Zenodo DOI</text>')
    p.append(f'<text x="{badge_x}" y="{badge_y+74}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
              f'font-size="21" fill="{ACCENT}">Release 2026-09-03</text>')

    lic_x, lic_y0 = 990, 601
    p.append(f'<text x="{lic_x}" y="{lic_y0-26}" font-family="Fira Sans" font-weight="700" font-size="24" '
              f'fill="{ACCENT}">Licences \u2014 6 filtered 3D objects, real counts</text>')
    for i, (lic, count, maxc) in enumerate(_LICENCES):
        ly = lic_y0 + i * 55
        p.append(f'<text x="{lic_x}" y="{ly+18}" font-family="Fira Sans" font-weight="700" font-size="19" '
                  f'fill="{INK}">{esc(lic)}</text>')
        bx, bar_w = lic_x + 250, 340
        p.append(f'<rect x="{bx}" y="{ly+2}" width="{bar_w}" height="24" rx="7" fill="{TINT}" '
                  f'stroke="{ACCENT_LIGHT}" stroke-width="1.5"/>')
        p.append(f'<rect x="{bx}" y="{ly+2}" width="{bar_w*count/maxc}" height="24" rx="7" fill="{ACCENT}"/>')
        p.append(f'<text x="{bx+bar_w+20}" y="{ly+21}" font-family="Fira Sans" font-weight="700" font-size="21" '
                  f'fill="{ACCENT}">{count}\u00d7</text>')

    p.append("</g></svg>")
    return "\n".join(p)


# -------------------------------------------------------------- Purpose 2 --
# A real SPARQL query (Query 3, fdo-squirrel-registry/sparql.html), hand-
# drawn as code, feeding a real connected result graph -- FDOx Registry
# (the real dcat:Catalog) at the root, four real FDOs as children, each
# with two of its real model-file distributions as grandchildren.
_QUERY_LINES = [
    (0, [("SELECT ", True), ("?title ?path ?mediaType ?bytes ?role", False)]),
    (0, [("WHERE {", True)]),
    (40, [("?fdo dct:title ?title ;", False)]),
    (95, [("dcat:distribution ?distribution .", False)]),
    (40, [("?distribution fdo:role \u201cmodel\u201d ;", False)]),
    (95, [("fdo:path ?path ;", False)]),
    (95, [("crm:P2_has_type ?concept .", False)]),
    (40, [("?concept skos:prefLabel ?role .", False)]),
    (40, [("OPTIONAL ", True), ("{ ?distribution dcat:mediaType ?mediaType }", False)]),
    (40, [("OPTIONAL ", True), ("{ ?distribution dcat:byteSize ?bytes }", False)]),
    (0, [("}", False)]),
    (0, [("ORDER BY DESC", True), ("(?bytes)", False)]),
]
_QUERY_FDOS = [
    ("CO074-148----", [("model.obj", "430 MB"), ("model.nxs", "173 MB")]),
    ("CHUIS/1", [("CHUIS_1.ply", "91 MB"), ("CHUIS_1.nxs", "74 MB")]),
    ("GEARS/1", [("GEARS_1.ply", "49 MB"), ("...gaers1.glb", "31 MB")]),
    ("Freshford: St Lachtain's Well", [("model.nxs", "7 MB"), ("model.obj", "1 MB")]),
]
_QUERY_NAME_LINES = {
    "CO074-148----": ["CO074-148----"],
    "CHUIS/1": ["CHUIS/1"],
    "GEARS/1": ["GEARS/1"],
    "Freshford: St Lachtain's Well": ["Freshford:", "St Lachtain's Well"],
}
CODE_BG, CODE_TEXT, CODE_KEYWORD = "#161B2E", "#D8DEE9", "#6FC3E8"


def _build_purpose2(hshift: int, vshift: int) -> str:
    p = _svg_open()
    p.append(_icon_svg(2, 110, 0.5))
    p.append(f'<g transform="translate({hshift},{vshift})">')

    q_x, q_y, q_w = 260, 55, 1430
    line_h = 33
    q_h = len(_QUERY_LINES) * line_h + 50
    p.append(f'<rect x="{q_x}" y="{q_y}" width="{q_w}" height="{q_h}" rx="14" fill="{CODE_BG}"/>')
    for i, (indent, segs) in enumerate(_QUERY_LINES):
        ty = q_y + 40 + i * line_h
        tx = q_x + 34 + indent
        seg_parts = []
        for text, is_kw in segs:
            color = CODE_KEYWORD if is_kw else CODE_TEXT
            weight = 700 if is_kw else 400
            seg_parts.append(f'<tspan font-weight="{weight}" fill="{color}">{esc(text)}</tspan>')
        p.append(f'<text x="{tx}" y="{ty}" font-family="Fira Sans" font-size="23">{"".join(seg_parts)}</text>')
    p.append(f'<text x="{q_x}" y="{q_y+q_h+32}" font-family="Fira Sans" font-weight="400" font-size="19" '
              f'fill="{MUTED}">Query 3, fdo-squirrel-registry/sparql.html \u2014 real, live, 1.3s over 7,882 triples</text>')

    tree_top = q_y + q_h + 70
    root_w, root_h = 480, 80
    root_x, root_cx = (W - root_w) / 2, W / 2
    p.append(f'<rect x="{root_x}" y="{tree_top}" width="{root_w}" height="{root_h}" rx="14" fill="{ACCENT}"/>')
    p.append(f'<text x="{root_cx}" y="{tree_top+34}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
              f'font-size="22" fill="white">FDOx Registry (dcat:Catalog)</text>')
    p.append(f'<text x="{root_cx}" y="{tree_top+58}" text-anchor="middle" font-family="Fira Sans" font-weight="400" '
              f'font-size="16" fill="{TINT}">all ?fdo results are dcat:Dataset members here</text>')

    n = len(_QUERY_FDOS)
    slot_w = W / n
    fdo_y, fdo_h = tree_top + root_h + 55, 70
    file_y, file_h = fdo_y + fdo_h + 45, 66
    for i, (name, files) in enumerate(_QUERY_FDOS):
        slot_x = i * slot_w
        fdo_w = slot_w - 30
        fdo_x = slot_x + 15
        fdo_cx = fdo_x + fdo_w / 2
        p.append(f'<line x1="{root_cx}" y1="{tree_top+root_h}" x2="{fdo_cx}" y2="{fdo_y}" stroke="{ACCENT_LIGHT}" '
                  f'stroke-width="2.2" marker-end="url(#arrow)" opacity="0.75"/>')
        p.append(f'<rect x="{fdo_x}" y="{fdo_y}" width="{fdo_w}" height="{fdo_h}" rx="10" fill="{ACCENT_LIGHT}"/>')
        lines = _QUERY_NAME_LINES[name]
        line_gap = 21 if len(lines) > 1 else 26
        start_y = fdo_y + fdo_h / 2 - (len(lines) - 1) * line_gap / 2 + 6
        for j, line in enumerate(lines):
            p.append(f'<text x="{fdo_cx}" y="{start_y+j*line_gap}" text-anchor="middle" font-family="Fira Sans" '
                      f'font-weight="700" font-size="17" fill="white">{esc(line)}</text>')
        p.append(f'<text x="{fdo_cx}" y="{fdo_y+fdo_h-6}" text-anchor="middle" font-family="Fira Sans" font-weight="400" '
                  f'font-size="13" fill="{TINT}">dcat:Dataset</text>')

        file_w = (fdo_w - 14) / 2
        for k, (path, size) in enumerate(files):
            fx = fdo_x + k * (file_w + 14)
            fcx = fx + file_w / 2
            p.append(f'<line x1="{fdo_cx}" y1="{fdo_y+fdo_h}" x2="{fcx}" y2="{file_y}" stroke="{ACCENT_LIGHT}" '
                      f'stroke-width="2" marker-end="url(#arrow)" opacity="0.6"/>')
            p.append(f'<rect x="{fx}" y="{file_y}" width="{file_w}" height="{file_h}" rx="8" fill="{TINT}" '
                      f'stroke="{ACCENT_LIGHT}" stroke-width="1.8"/>')
            path_size = 14 if len(path) <= 20 else 13.5
            p.append(f'<text x="{fcx}" y="{file_y+26}" text-anchor="middle" font-family="Fira Sans" '
                      f'font-weight="700" font-size="{path_size}" fill="{INK}">{esc(path)}</text>')
            p.append(f'<text x="{fcx}" y="{file_y+48}" text-anchor="middle" font-family="Fira Sans" '
                      f'font-weight="400" font-size="13" fill="{MUTED}">{esc(size)}</text>')

    p.append("</g></svg>")
    return "\n".join(p)


# -------------------------------------------------------------- Purpose 3 --
# Six real registry objects converging on three real hubs (OpenStreetMap,
# Wikidata, SquirrelBase), directed edges labelled with the real predicate
# where confirmed from the TTL (dct:spatial / dct:subject); SquirrelBase
# carries the real item id instead, since that triple's own predicate
# isn't confirmed from the TTL (S9 -- do not assert it).
_INTEROP_FDOS = [
    ("CO074-148---- (CIIC 81)", "OSM node/11071361392", [("osm", "dct:spatial"), ("wd", "dct:subject/type")]),
    ("GEARS/1", "OSM node/11966441102", [("osm", "dct:spatial")]),
    ("Steinm\u00e4nnchen / Antholzer See", "OSM relation/14599988", [("osm", "dct:spatial"), ("sb", "Q60")]),
    ("Beuys-Stele B 1036", "OSM node/3647679932", [("osm", "dct:spatial"), ("sb", "Q56")]),
    ("CHUIS/1", "OSM node/11966430251", [("osm", "dct:spatial")]),
    ("Freshford: St Lachtain's Well", "wd:Q121840779", [("wd", "dct:subject")]),
]
_INTEROP_HUBS = {"osm": (190, "OpenStreetMap"), "wd": (500, "Wikidata"), "sb": (810, "SquirrelBase")}


def _edge_label(x1, y1, x2, y2, frac, text, font_size=19, color=ACCENT):
    import math
    lx = x1 + (x2 - x1) * frac
    ly = y1 + (y2 - y1) * frac
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle > 90:
        angle -= 180
    if angle < -90:
        angle += 180
    tw = len(text) * font_size * 0.60 + 20
    th = font_size + 14
    return (
        f'<g transform="translate({lx:.1f},{ly:.1f}) rotate({angle:.1f})">'
        f'<rect x="{-tw/2:.1f}" y="{-th/2:.1f}" width="{tw:.1f}" height="{th:.1f}" rx="6" fill="white" '
        f'stroke="{color}" stroke-width="1.3" opacity="0.95"/>'
        f'<text x="0" y="{font_size*0.36:.1f}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
        f'font-size="{font_size}" fill="{color}">{esc(text)}</text></g>'
    )


def _build_purpose3(hshift: int, vshift: int) -> str:
    p = _svg_open()
    p.append(_icon_svg(3, 120, 0.55))
    p.append(f'<g transform="translate({hshift},{vshift})">')

    p.append(f'<text x="80" y="215" font-family="Fira Sans" font-weight="700" font-size="24" fill="{MUTED}">'
              f'6 real registry objects</text>')
    p.append(f'<text x="1500" y="45" text-anchor="middle" font-family="Fira Sans" font-weight="700" font-size="24" '
              f'fill="{ACCENT}">three real, shared hubs</text>')

    fdo_x, fdo_w, fdo_h = 80, 500, 90
    row_top0, row_gap = 250, 128
    fdo_pts = []
    for i, (name, ident, edges) in enumerate(_INTEROP_FDOS):
        ry = row_top0 + i * row_gap
        fdo_pts.append((fdo_x + fdo_w, ry + fdo_h / 2, edges))
        p.append(f'<rect x="{fdo_x}" y="{ry}" width="{fdo_w}" height="{fdo_h}" rx="12" fill="{TINT}" '
                  f'stroke="{ACCENT}" stroke-width="2.5"/>')
        p.append(f'<text x="{fdo_x+20}" y="{ry+36}" font-family="Fira Sans" font-weight="700" font-size="19" '
                  f'fill="{INK}">{esc(name)}</text>')
        p.append(f'<text x="{fdo_x+20}" y="{ry+65}" font-family="Fira Sans" font-weight="400" font-size="17" '
                  f'fill="{MUTED}">{esc(ident)}</text>')

    hub_x, hub_r = 1500, 115
    hub_counts = {"osm": 0, "wd": 0, "sb": 0}
    for _, _, edges in _INTEROP_FDOS:
        for hub_key, _ in edges:
            hub_counts[hub_key] += 1

    for x, y, edges in fdo_pts:
        for ei, (hub_key, label) in enumerate(edges):
            hy = _INTEROP_HUBS[hub_key][0]
            hx2 = hub_x - hub_r - 8
            p.append(arrow_line(x, y, hx2, hy, color=ACCENT_LIGHT, width=2))
            p.append(_edge_label(x, y, hx2, hy, 0.22 + ei * 0.22, label))

    for hub_key, (hy, hname) in _INTEROP_HUBS.items():
        p.append(f'<circle cx="{hub_x}" cy="{hy}" r="{hub_r}" fill="{ACCENT}"/>')
        p.append(f'<text x="{hub_x}" y="{hy-4}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
                  f'font-size="22" fill="white">{esc(hname)}</text>')
        p.append(f'<text x="{hub_x}" y="{hy+24}" text-anchor="middle" font-family="Fira Sans" font-weight="400" '
                  f'font-size="18" fill="{TINT}">{hub_counts[hub_key]} real links</text>')

    p.append("</g></svg>")
    return "\n".join(p)


# -------------------------------------------------------------- Purpose 4 --
# An abstract DCAT-catalogue graphic (no screenshot -- Flo, 2026-09-09)
# with the registry's five real machine-readable exits, plus the real
# 8-record dcat:Catalog structure, all orthogonal connectors.
_CATALOG_RECORDS = [
    "CO074-148---- (CIIC 81)", "CHUIS/1", "GEARS/1", "Beuys-Stele B 1036",
    "Steinm\u00e4nnchen / Antholzer See", "Freshford: St Lachtain's Well",
    "o3d-epidoc-extractor", "ogham-analysis",
]
_EXITS = ["bundle\n(Turtle)", "index\n(JSON)", "CRM\ncrosswalk", "SPARQL", "quality\nreport"]


def _build_purpose4(hshift: int, vshift: int) -> str:
    p = _svg_open()
    p.append(_icon_svg(4, 130, 0.6))
    p.append(f'<g transform="translate({hshift},{vshift})">')

    cyl_cx, cyl_top, cyl_rx, cyl_ry, cyl_h = 380, 70, 115, 30, 150
    p.append(f'<rect x="{cyl_cx-cyl_rx}" y="{cyl_top}" width="{cyl_rx*2}" height="{cyl_h}" fill="{ACCENT}"/>')
    p.append(f'<ellipse cx="{cyl_cx}" cy="{cyl_top+cyl_h}" rx="{cyl_rx}" ry="{cyl_ry}" fill="{ACCENT_LIGHT}"/>')
    p.append(f'<ellipse cx="{cyl_cx}" cy="{cyl_top}" rx="{cyl_rx}" ry="{cyl_ry}" fill="{ACCENT}" stroke="{TINT}" '
              f'stroke-width="2"/>')
    p.append(f'<text x="{cyl_cx}" y="{cyl_top+cyl_h/2+8}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="700" font-size="30" fill="white">DCAT</text>')
    p.append(f'<text x="{cyl_cx}" y="{cyl_top+cyl_h+cyl_ry+40}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="700" font-size="22" fill="{INK}">FDOx Registry</text>')
    p.append(f'<text x="{cyl_cx}" y="{cyl_top+cyl_h+cyl_ry+66}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="400" font-size="17" fill="{MUTED}">Release 2026-09-03 \u00b7 7,793 triples</text>')

    ex_x0, ex_y, ex_gap, ex_w, ex_h = 660, 130, 210, 175, 90
    ex_cy = ex_y + ex_h / 2
    cyl_anchor_x, cyl_anchor_y = cyl_cx + cyl_rx, cyl_top + cyl_h / 2
    p.append(f'<line x1="{cyl_anchor_x}" y1="{cyl_anchor_y}" x2="{cyl_anchor_x+30}" y2="{cyl_anchor_y}" '
              f'stroke="{ACCENT_LIGHT}" stroke-width="2.5"/>')
    p.append(f'<line x1="{cyl_anchor_x+30}" y1="{cyl_anchor_y}" x2="{cyl_anchor_x+30}" y2="{ex_cy}" '
              f'stroke="{ACCENT_LIGHT}" stroke-width="2.5"/>')
    last_ex_cx = ex_x0 + (len(_EXITS) - 1) * ex_gap + ex_w / 2
    p.append(f'<line x1="{cyl_anchor_x+30}" y1="{ex_cy}" x2="{last_ex_cx}" y2="{ex_cy}" stroke="{ACCENT_LIGHT}" '
              f'stroke-width="2.5"/>')
    for i, label in enumerate(_EXITS):
        ex_x = ex_x0 + i * ex_gap
        p.append(f'<rect x="{ex_x}" y="{ex_y}" width="{ex_w}" height="{ex_h}" rx="12" fill="{TINT}" '
                  f'stroke="{ACCENT}" stroke-width="2.2"/>')
        lines = label.split("\n")
        start_y = ex_cy - (len(lines) - 1) * 13 + 7
        for j, line in enumerate(lines):
            p.append(f'<text x="{ex_x+ex_w/2}" y="{start_y+j*26}" text-anchor="middle" font-family="Fira Sans" '
                      f'font-weight="700" font-size="18" fill="{ACCENT}">{esc(line)}</text>')
    p.append(f'<text x="{ex_x0}" y="{ex_y+ex_h+34}" font-family="Fira Sans" font-weight="400" font-size="18" '
              f'fill="{MUTED}">5 real, machine-readable exits \u2014 not just N4O-specific</text>')

    col_xs = [80, 500, 920, 1340]
    rec_w, rec_h = 360, 110
    row_ys = [560, 730]
    row1_cxs = [x + rec_w / 2 for x in col_xs]
    bus_y1, bus_y2, trunk_x = 515, 700, 890  # trunk sits in the real 860-920 gap between row-1 boxes

    cat_x, cat_y, cat_w, cat_h = 725, 380, 300, 90
    p.append(f'<rect x="{cat_x}" y="{cat_y}" width="{cat_w}" height="{cat_h}" rx="14" fill="{ACCENT}"/>')
    p.append(f'<text x="{cat_x+cat_w/2}" y="{cat_y+38}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="700" font-size="23" fill="white">dcat:Catalog</text>')
    p.append(f'<text x="{cat_x+cat_w/2}" y="{cat_y+65}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="400" font-size="17" fill="{TINT}">FDOx Registry \u2014 7,793 triples</text>')
    cat_cx = cat_x + cat_w / 2

    p.append(f'<line x1="{cat_cx}" y1="{cat_y+cat_h}" x2="{cat_cx}" y2="{bus_y1}" stroke="{ACCENT_LIGHT}" '
              f'stroke-width="2" opacity="0.8"/>')
    p.append(f'<line x1="{min(row1_cxs+[cat_cx])}" y1="{bus_y1}" x2="{max(row1_cxs+[cat_cx])}" y2="{bus_y1}" '
              f'stroke="{ACCENT_LIGHT}" stroke-width="2" opacity="0.8"/>')
    for cx in row1_cxs:
        p.append(arrow_line(cx, bus_y1, cx, row_ys[0], color=ACCENT_LIGHT, width=2))

    p.append(f'<line x1="{cat_cx}" y1="{bus_y1}" x2="{trunk_x}" y2="{bus_y1}" stroke="{ACCENT_LIGHT}" '
              f'stroke-width="2" opacity="0.8"/>')
    p.append(f'<line x1="{trunk_x}" y1="{bus_y1}" x2="{trunk_x}" y2="{bus_y2}" stroke="{ACCENT_LIGHT}" '
              f'stroke-width="2" opacity="0.8"/>')
    p.append(f'<line x1="{min(row1_cxs+[trunk_x])}" y1="{bus_y2}" x2="{max(row1_cxs+[trunk_x])}" y2="{bus_y2}" '
              f'stroke="{ACCENT_LIGHT}" stroke-width="2" opacity="0.8"/>')
    for cx in row1_cxs:
        p.append(arrow_line(cx, bus_y2, cx, row_ys[1], color=ACCENT_LIGHT, width=2))

    for i, name in enumerate(_CATALOG_RECORDS):
        col, row = i % 4, i // 4
        rx, ry = col_xs[col], row_ys[row]
        p.append(f'<rect x="{rx}" y="{ry}" width="{rec_w}" height="{rec_h}" rx="10" fill="{TINT}" '
                  f'stroke="{ACCENT}" stroke-width="2"/>')
        p.append(f'<text x="{rx+18}" y="{ry+38}" font-family="Fira Sans" font-weight="700" font-size="18" '
                  f'fill="{INK}">{esc(name)}</text>')
        p.append(f'<text x="{rx+18}" y="{ry+68}" font-family="Fira Sans" font-weight="400" font-size="16" '
                  f'fill="{MUTED}">dcat:CatalogRecord \u2192 dcat:Dataset</text>')

    p.append("</g></svg>")
    return "\n".join(p)


# ------------------------------------------------------------------------

def _render_balanced(name: str, build_fn, badge_num: int, badge_cy: float, badge_scale: float) -> tuple[int, int]:
    """Same two-pass discipline as S8's _render_balanced -- see that
    module's docstring."""
    svg_path = IMG_DIR / f"{name}.svg"
    png_path = svg_path.with_suffix(".png")

    svg_path.write_text(build_fn(0, 0), encoding="utf-8")
    render_svg_to_png(svg_path, png_path, W * OVERSAMPLE, H * OVERSAMPLE)

    exclude = _icon_exclude_box(badge_cy, badge_scale)
    left, right, top, bottom = measure_content_margins(png_path, exclude)
    hshift = round(((right - left) / 2) / OVERSAMPLE)
    vshift = round(((bottom - top) / 2) / OVERSAMPLE)

    svg_path.write_text(build_fn(hshift, vshift), encoding="utf-8")
    render_svg_to_png(svg_path, png_path, W * OVERSAMPLE, H * OVERSAMPLE)

    from PIL import Image
    with Image.open(png_path) as im:
        return im.size


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []

    jobs = [
        ("fdox-talk-purpose1-fair-citable", _build_purpose1, 1, 145, 0.62),
        ("fdox-talk-purpose2-semantically-queryable", _build_purpose2, 2, 110, 0.5),
        ("fdox-talk-purpose3-interoperable", _build_purpose3, 3, 120, 0.55),
        ("fdox-talk-purpose4-integrable", _build_purpose4, 4, 130, 0.6),
    ]
    for name, build_fn, num, cy, scale in jobs:
        w, h = _render_balanced(name, build_fn, num, cy, scale)
        log.append(f"wrote img/{name}.svg + .png ({w}x{h}, white background)")

    return log


if __name__ == "__main__":
    for line in run():
        print(line)
