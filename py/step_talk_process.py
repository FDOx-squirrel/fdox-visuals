"""S8 -- Talk process slides: the four-step pattern, one slide each.

Companion to S2's four-step *banner* (all four steps side by side, at a
glance): this produces one full 7:4 slide per step, each substantiated
with real data from the FDOx-Squirrel family's own repos (CIIC 81's real
TTL, the live FDOx Registry, the real fdo-3d-packager/fdo-squirrel
pipeline) rather than the banner's abstract icon+description. Built for
the FAIR 3D Heritage Conference talk (Mainz, 2026-09-14/16), Part 5.

Produces (white background -- these are meant to be the single image on
a slide, not composited further, so A4's "transparent, no header/footer"
convention does not apply here; see PRIMER S8):
  img/fdox-talk-step1-fdo-encapsulation.png
  img/fdox-talk-step2-semantic-metadata.png
  img/fdox-talk-step3-linking-hubs.png
  img/fdox-talk-step4-federated-kg.png

Three of the four composite a real screenshot/photo under img/source/ --
Sketchfab, the FDOx Registry, and CIIC 81's preview render -- which is the
one case PRIMER A3/patch-zip-delivery's "generated files" rule carves out:
assets a script cannot itself produce (no browser, no camera) ship as
data and are composited, not regenerated. Step 2's slide is pure SVG.

Runnable standalone: `python py/step_talk_process.py`
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals_utils import (  # noqa: E402
    IMG_DIR,
    INK,
    MUTED,
    ROOT,
    STEPS,
    arrow_line,
    arrow_marker,
    edge_label,
    elbow_path,
    ensure_dirs,
    esc,
    font_face_css,
    label_box,
    measure_content_margins,
    paste_raster,
    render_svg_to_png,
)
from step_pattern import _node_icon  # noqa: E402  -- exact same badge glyphs as S2

SOURCE_DIR = IMG_DIR / "source"

W, H = 1750, 1000
OVERSAMPLE = 2

# icon badge: fixed top-left, never shifted -- every slide's content gets
# balanced around it, per S8 Nachtrag (see PRIMER).
ICON_CX, ICON_CY, ICON_R_DESIGN = 175, 165, 150  # r=150 is _node_icon's own badge radius


def _icon_svg(step_idx: int, scale: float, cx: float = ICON_CX, cy: float = ICON_CY) -> str:
    step = STEPS[step_idx]
    color, tint = step["color"], step["tint"]
    tag_size, tag_offset = 132, 26
    tag_x = -ICON_R_DESIGN - tag_offset
    tag_y = -ICON_R_DESIGN - tag_offset
    out = f'<g transform="translate({cx},{cy}) scale({scale})">'
    out += f'<circle cx="0" cy="0" r="{ICON_R_DESIGN}" fill="{tint}" stroke="{color}" stroke-width="7"/>'
    out += _node_icon(step_idx, color)
    out += f'<rect x="{tag_x}" y="{tag_y}" width="{tag_size}" height="{tag_size}" rx="26" fill="{color}"/>'
    out += (
        f'<text x="{tag_x + tag_size/2}" y="{tag_y + tag_size/2 + 36}" text-anchor="middle" '
        f'font-family="Fira Sans" font-weight="700" font-size="104" fill="white">{step["num"]}</text>'
    )
    out += "</g>"
    return out


def _icon_exclude_box(scale: float) -> tuple[int, int, int, int]:
    r = (ICON_R_DESIGN + 26) * scale * OVERSAMPLE
    cx, cy = ICON_CX * OVERSAMPLE, ICON_CY * OVERSAMPLE
    return (int(cx - r), int(cy - r), int(cx + r), int(cy + r))


def _svg_open(defs: str = "") -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>',
        font_face_css(),
        arrow_marker("arrow", MUTED),
        defs,
    ]


# ---------------------------------------------------------------- Step 1 --
# CIIC 81's real Sketchfab source -> fdo-3d-packager's real six-step CLI ->
# the FAIR Digital Object it produces (sphere-only crop of S3's meta-
# graphic -- no leader-line text, that graphic makes its own separate
# point about Data/Metadata/PID; here it's just "this is now an FDO").
_STEP1_PIPELINE = [
    ("fetch", "Sketchfab API / local files"),
    ("convert", "Blender \u2192 OBJ + textures"),
    ("nexus", "multiresolution build"),
    ("mdcff", "MD.cff + CITATION.cff"),
    ("bundle", "3DHOP viewer + ZIP"),
    ("build_fdo", "\u2192 fdo-squirrel"),
]


def _build_step1(hshift: int, vshift: int) -> str:
    accent = STEPS[0]["color"]
    photo_x, photo_y, photo_w, photo_h = 60, 300, 460, 350  # 1500:1141 Sketchfab screenshot
    col_w, gap_x = 220, 36
    col0_x = 620
    col1_x = col0_x + col_w + gap_x
    col2_x = col0_x + 2 * (col_w + gap_x)
    row_h = 140
    row1_y, row2_y = 340, 660
    meta_cx, meta_cy, meta_r = 1560, 630, 145

    p = _svg_open()
    p.append(_icon_svg(0, 0.56))
    p.append(f'<g transform="translate({hshift},{vshift})">')

    p.append(f'<rect x="{photo_x-6}" y="{photo_y-6}" width="{photo_w+12}" height="{photo_h+12}" rx="10" '
              f'fill="none" stroke="{accent}" stroke-width="4"/>')
    p.append(f'<rect x="{photo_x}" y="{photo_y}" width="{photo_w}" height="{photo_h}" fill="#EEEEEE"/>')
    p.append(f'<text x="{photo_x}" y="{photo_y+photo_h+34}" font-family="Fira Sans" font-weight="700" '
              f'font-size="22" fill="{INK}">Sketchfab</text>')
    p.append(f'<text x="{photo_x}" y="{photo_y+photo_h+60}" font-family="Fira Sans" font-weight="400" '
              f'font-size="20" fill="{MUTED}">Freshford: St Lachtain\u2019s Well \u00b7 by b-unicycling, via Sketchfab</text>')

    arrow_y = (row1_y + row2_y) / 2
    p.append(arrow_line(photo_x + photo_w + 15, arrow_y, col0_x - 15, arrow_y))

    p.append(f'<text x="{(col0_x+col2_x+col_w)/2}" y="{row1_y-90}" text-anchor="middle" '
              f'font-family="Fira Sans" font-weight="700" font-size="24" fill="{accent}">fdo-3d-packager v1.0.0</text>')

    cols = [col0_x, col1_x, col2_x]
    for i, (name, desc) in enumerate(_STEP1_PIPELINE[:3]):
        p.append(label_box(cols[i], row1_y - row_h/2, col_w, row_h,
                            [(name, 700, 26), (desc, 400, 18)], stroke=accent))
    for i, (name, desc) in enumerate(_STEP1_PIPELINE[3:5]):
        p.append(label_box(cols[i], row2_y - row_h/2, col_w, row_h,
                            [(name, 700, 26), (desc, 400, 18)], stroke=accent))
    name, desc = _STEP1_PIPELINE[5]
    p.append(label_box(col2_x, row2_y - row_h/2, col_w, row_h,
                        [(name, 700, 26), (desc, 400, 18)], fill=accent, stroke=accent, text_color="white"))

    p.append(arrow_line(col0_x + col_w, row1_y, col1_x, row1_y))
    p.append(arrow_line(col1_x + col_w, row1_y, col2_x, row1_y))
    p.append(elbow_path([(col2_x + col_w/2, row1_y + row_h/2), (col2_x + col_w/2, row1_y + row_h/2 + 35),
                          (col0_x + col_w/2, row2_y - row_h/2 - 35), (col0_x + col_w/2, row2_y - row_h/2)]))
    p.append(arrow_line(col0_x + col_w, row2_y, col1_x, row2_y))
    p.append(arrow_line(col1_x + col_w, row2_y, col2_x, row2_y))
    p.append(arrow_line(col2_x + col_w + 15, row2_y, meta_cx - meta_r - 15, row2_y))

    meta_scale = meta_r / 320
    p.append(f'<g transform="translate({meta_cx},{meta_cy}) scale({meta_scale})">'
              '<circle cx="0" cy="0" r="320" fill="#A5BDCE" stroke="#004473" stroke-width="6"/>'
              '<circle cx="0" cy="0" r="175" fill="#004473" stroke="#002F50" stroke-width="6"/>'
              '<text x="0" y="-14" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
              'font-size="70" fill="white" letter-spacing="4">I0I0</text>'
              '<text x="0" y="70" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
              'font-size="70" fill="white" letter-spacing="4">0I0I</text></g>')
    p.append(f'<text x="{meta_cx}" y="{meta_cy+meta_r+40}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="700" font-size="22" fill="{INK}">FDO bundle</text>')
    p.append(f'<text x="{meta_cx}" y="{meta_cy+meta_r+66}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="400" font-size="20" fill="{MUTED}">32 files \u00b7 deterministic</text>')

    p.append("</g></svg>")
    return "\n".join(p)


_STEP1_RASTER = dict(x=60, y=300, w=460, h=350, asset="talk-sketchfab-freshford.png", circular=False)


# ---------------------------------------------------------------- Step 2 --
# CIIC 81's real MD.cff/TTL values, each mapped to the actual CIDOC CRM
# class or property fdo-squirrel's crosswalk anchors it to. Pure SVG.
_STEP2_ROWS = [
    ("id", "10.5281/zenodo.18724635",
     "crm:E73_Information_Object", "crmdig:D1_Digital_Object (fdo:3DDataFDO)"),
    ("spatial", "OSM node/11071361392 (51.894, \u20138.492)",
     "crm:E53_Place", "CRMgeo SP5_Geometric_Place_Expression"),
    ("temporal", "Ogham stone inscriptions, 300\u2013699 CE",
     "P4_has_time-span \u2192 E52_Time-Span", "P82a_begin_of_the_begin / P82b_end_of_the_end"),
    ("object_type / material", "wd:Q2016147 Inscribed Ogham stone \u00b7 wd:Q22731 Stone",
     "P2_has_type \u2192 E55_Type", "via dct:type / dct:subject"),
    ("distributions", "32 files \u2014 model.obj, MD.cff, preview.png, \u2026",
     "crmdig:D9_Data_Object", "one per dcat:Distribution"),
]


def _build_step2(hshift: int, vshift: int) -> str:
    accent, tint = STEPS[1]["color"], STEPS[1]["tint"]
    left_x, left_w = 55, 585
    right_x, right_w = 1140, 555
    row_top0, row_h, row_gap = 235, 125, 20

    p = _svg_open()
    p.append(_icon_svg(1, 0.48, cy=120))
    p.append(f'<g transform="translate({hshift},{vshift})">')

    p.append(f'<text x="320" y="{row_top0-28}" font-family="Fira Sans" font-weight="700" font-size="24" '
              f'fill="{MUTED}">CIIC 81 \u2014 real MD.cff / TTL values</text>')
    p.append(f'<text x="{right_x}" y="{row_top0-28}" font-family="Fira Sans" font-weight="700" font-size="24" '
              f'fill="{accent}">CIDOC CRM anchor</text>')

    for i, (lfield, lval, rclass, rdetail) in enumerate(_STEP2_ROWS):
        top = row_top0 + i * (row_h + row_gap)
        p.append(f'<rect x="{left_x}" y="{top}" width="{left_w}" height="{row_h}" rx="12" fill="{tint}" '
                  f'stroke="{accent}" stroke-width="2.5"/>')
        p.append(f'<text x="{left_x+28}" y="{top+42}" font-family="Fira Sans" font-weight="700" font-size="23" '
                  f'fill="{INK}">{esc(lfield)}</text>')
        p.append(f'<text x="{left_x+28}" y="{top+76}" font-family="Fira Sans" font-weight="400" font-size="20" '
                  f'fill="{MUTED}">{esc(lval)}</text>')
        p.append(arrow_line(left_x + left_w + 15, top + row_h/2, right_x - 15, top + row_h/2, color=accent, width=3.5))
        p.append(f'<rect x="{right_x}" y="{top}" width="{right_w}" height="{row_h}" rx="12" fill="{accent}"/>')
        p.append(f'<text x="{right_x+28}" y="{top+42}" font-family="Fira Sans" font-weight="700" font-size="23" '
                  f'fill="white">{esc(rclass)}</text>')
        p.append(f'<text x="{right_x+28}" y="{top+76}" font-family="Fira Sans" font-weight="400" font-size="19" '
                  f'fill="{tint}">{esc(rdetail)}</text>')

    p.append("</g></svg>")
    return "\n".join(p)


# ---------------------------------------------------------------- Step 3 --
# CIIC 81's real photo, radiating out to the real external links found in
# its own TTL: Wikidata (all three), OpenStreetMap, ChronOntology, Sketchfab.
_STEP3_NODES = [
    ("Wikidata", "wd:Q2016147 \u2014 Inscribed Ogham stone"),
    ("Wikidata", "wd:Q22731 \u2014 Stone"),
    ("Wikidata", "wd:Q121592049 \u2014 UCC Stone Corridor"),
    ("OpenStreetMap", "node/11071361392"),
    ("ChronOntology", "period aChcHZdlBhkt \u2014 300\u2013699 CE"),
    ("Sketchfab", "Source: CIIC 81 / UCC 4"),
]


def _build_step3(hshift: int, vshift: int) -> str:
    accent = STEPS[2]["color"]
    photo_cx, photo_cy, photo_r = 560, 500, 210
    node_x = 990
    row_ys = [150, 290, 430, 570, 710, 850]

    p = _svg_open()
    p.append(_icon_svg(2, 0.56))
    p.append(f'<g transform="translate({hshift},{vshift})">')

    hub_anchor = (photo_cx + photo_r, photo_cy)
    for dy, name, detail in zip(row_ys, [n[0] for n in _STEP3_NODES], [n[1] for n in _STEP3_NODES]):
        p.append(f'<line x1="{hub_anchor[0]}" y1="{hub_anchor[1]}" x2="{node_x}" y2="{dy}" stroke="{accent}" '
                  f'stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>')

    p.append(f'<circle cx="{photo_cx}" cy="{photo_cy}" r="{photo_r}" fill="#EEEEEE"/>')
    p.append(f'<circle cx="{photo_cx}" cy="{photo_cy}" r="{photo_r+4}" fill="none" stroke="{accent}" stroke-width="5"/>')
    p.append(f'<text x="{photo_cx}" y="{photo_cy+photo_r+44}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="700" font-size="24" fill="{INK}">CIIC 81</text>')
    p.append(f'<text x="{photo_cx}" y="{photo_cy+photo_r+70}" text-anchor="middle" font-family="Fira Sans" '
              f'font-weight="400" font-size="19" fill="{MUTED}">10.5281/zenodo.18724635</text>')

    for dy, (name, detail) in zip(row_ys, _STEP3_NODES):
        p.append(f'<circle cx="{node_x}" cy="{dy}" r="12" fill="{accent}"/>')
        lx = node_x + 24
        p.append(f'<text x="{lx}" y="{dy-8}" font-family="Fira Sans" font-weight="700" font-size="23" '
                  f'fill="{INK}">{esc(name)}</text>')
        p.append(f'<text x="{lx}" y="{dy+18}" font-family="Fira Sans" font-weight="400" font-size="19" '
                  f'fill="{MUTED}">{esc(detail)}</text>')

    p.append("</g></svg>")
    return "\n".join(p)


# ---------------------------------------------------------------- Step 4 --
# The live FDOx Registry (real screenshot) -> FDOx joining the federated
# graph-of-graphs as one node in a 5-node mesh (same topology as S2's
# step-4 icon), NFDI4Objects highlighted as the real, named hub.
_MESH_NAMES = [
    ("NFDI4Objects", "Knowledge Graph"),
    ("Wikidata", None),
    ("Semantic Kompakkt", None),
    ("OpenStreetMap", None),
    ("FDOx", "n4o-collection"),
]
_MESH_LABEL_POS = ["above", "right", "right", "left", "above"]
_MESH_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 3)]


def _build_step4(hshift: int, vshift: int) -> str:
    accent = STEPS[3]["color"]
    shot_x, shot_y, shot_w, shot_h = 40, 245, 687, 680  # 1262:1249 registry screenshot

    cx, cy, r = 1300, 570, 175
    angles = [-90, -18, 54, 126, 198]
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in angles]
    node_r = 46

    p = _svg_open()
    p.append(_icon_svg(3, 0.5, cy=130))
    p.append(f'<g transform="translate({hshift},{vshift})">')

    p.append(f'<rect x="{shot_x}" y="{shot_y}" width="{shot_w}" height="{shot_h}" fill="#EEEEEE" '
              f'stroke="{MUTED}" stroke-width="2"/>')
    p.append(f'<text x="{shot_x}" y="{shot_y+shot_h+34}" font-family="Fira Sans" font-weight="700" '
              f'font-size="22" fill="{INK}">FDOx Registry</text>')
    p.append(f'<text x="{shot_x}" y="{shot_y+shot_h+60}" font-family="Fira Sans" font-weight="400" '
              f'font-size="20" fill="{MUTED}">Release 2026-09-03 \u2014 8 sources \u00b7 7,793 triples</text>')

    fx, fy = pts[4]
    ax1, ay1 = shot_x + shot_w + 15, (shot_y + shot_y + shot_h) / 2
    ax2, ay2 = fx - 55, fy + 38
    p.append(arrow_line(ax1, ay1, ax2, ay2, color=accent))
    p.append(edge_label(ax1, ay1, ax2, ay2, 0.42, "harvest & bundle", font_size=20, color=accent))

    for a, b in _MESH_EDGES:
        x1, y1 = pts[a]
        x2, y2 = pts[b]
        p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{accent}" '
                  f'stroke-width="3.5" stroke-linecap="round" opacity="0.55"/>')

    for i, (x, y) in enumerate(pts):
        name, sub = _MESH_NAMES[i]
        highlighted = i == 0
        fill = accent if highlighted else "white"
        text_color = "white" if highlighted else INK
        r_node = node_r + 10 if highlighted else node_r
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_node}" fill="{fill}" stroke="{accent}" stroke-width="4"/>')
        pos = _MESH_LABEL_POS[i]
        lines = [name] + ([sub] if sub else [])
        n = len(lines)
        if pos == "above":
            tx, ty, anchor = x, y - r_node - 20 - (n - 1) * 28, "middle"
        elif pos == "right":
            tx, ty, anchor = x + r_node + 18, y - (n - 1) * 13, "start"
        else:
            tx, ty, anchor = x - r_node - 18, y - (n - 1) * 13, "end"
        for j, line in enumerate(lines):
            weight = 700 if j == 0 else 400
            size = 24 if j == 0 else 19
            color = INK if j == 0 else MUTED
            p.append(f'<text x="{tx:.1f}" y="{ty+j*28:.1f}" text-anchor="{anchor}" font-family="Fira Sans" '
                      f'font-weight="{weight}" font-size="{size}" fill="{color}">{esc(line)}</text>')

    p.append("</g></svg>")
    return "\n".join(p)


_STEP4_RASTER = dict(x=40, y=245, w=687, h=680, asset="talk-registry-screenshot.png", circular=False)


# ------------------------------------------------------------------------

def _render_balanced(name: str, build_fn, icon_idx: int, icon_scale: float, icon_cy: float,
                      raster_specs: list[dict]) -> tuple[int, int]:
    """Two-pass render: build at (0,0), measure how far the true content
    (icon excluded) sits from centred, rebuild shifted by exactly that
    much. Measuring the actual rendered pixels rather than hand-picking a
    shift is the same discipline PRIMER already applies to trim_transparent_
    border (A1 finding 7) -- guessing a margin in design units misses
    content a wide title/photo can push further out than expected.
    """
    svg_path = IMG_DIR / f"{name}.svg"
    png_path = svg_path.with_suffix(".png")

    svg_path.write_text(build_fn(0, 0), encoding="utf-8")
    render_svg_to_png(svg_path, png_path, W * OVERSAMPLE, H * OVERSAMPLE)

    r_px = (150 + 26) * icon_scale * OVERSAMPLE  # badge radius + corner-tag offset, in rendered px
    cx_px, cy_px = ICON_CX * OVERSAMPLE, icon_cy * OVERSAMPLE
    exclude = (int(cx_px - r_px), int(cy_px - r_px), int(cx_px + r_px), int(cy_px + r_px))
    left, right, top, bottom = measure_content_margins(png_path, exclude)

    hshift = round(((right - left) / 2) / OVERSAMPLE)
    vshift = round(((bottom - top) / 2) / OVERSAMPLE)

    svg_path.write_text(build_fn(hshift, vshift), encoding="utf-8")
    render_svg_to_png(svg_path, png_path, W * OVERSAMPLE, H * OVERSAMPLE)

    for spec in raster_specs:
        paste_raster(
            png_path, SOURCE_DIR / spec["asset"],
            spec["x"] + hshift, spec["y"] + vshift, spec["w"], spec["h"],
            scale=OVERSAMPLE, circular=spec.get("circular", False),
        )

    from PIL import Image
    with Image.open(png_path) as im:
        return im.size


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []

    missing = [f for f in ("talk-sketchfab-freshford.png", "talk-registry-screenshot.png",
                            "talk-ciic81-preview.png") if not (SOURCE_DIR / f).exists()]
    if missing:
        msg = f"missing source asset(s) under img/source/: {', '.join(missing)}"
        if strict:
            raise RuntimeError(msg)
        log.append(f"WARNING: {msg}")

    jobs = [
        ("fdox-talk-step1-fdo-encapsulation", _build_step1, 0, 0.56, 165,
         [] if missing else [_STEP1_RASTER]),
        ("fdox-talk-step2-semantic-metadata", _build_step2, 1, 0.48, 120, []),
        ("fdox-talk-step3-linking-hubs", _build_step3, 2, 0.56, 165,
         [] if missing else [dict(x=560-210, y=500-210, w=420, h=420,
                                   asset="talk-ciic81-preview.png", circular=True)]),
        ("fdox-talk-step4-federated-kg", _build_step4, 3, 0.5, 130,
         [] if missing else [_STEP4_RASTER]),
    ]

    for name, build_fn, icon_idx, icon_scale, icon_cy, rasters in jobs:
        w, h = _render_balanced(name, build_fn, icon_idx, icon_scale, icon_cy, rasters)
        log.append(f"wrote img/{name}.svg + .png ({w}x{h}, white background)")

    return log


if __name__ == "__main__":
    for line in run():
        print(line)
