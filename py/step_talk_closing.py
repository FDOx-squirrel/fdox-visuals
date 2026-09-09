"""S10 -- Closing slide ("All in All -- Best Documentation Practice").

The eight step/purpose badges from S2/S7, arranged as a ring (alternating
step -> purpose -> step -> purpose, so neighbours are cause -> effect)
around S3's FDO sphere -- the slide itself is a small knowledge graph,
not a table describing one. Two variants:

  A: the ring + the sphere only.
  B: the same ring + sphere, plus three real external hubs (Wikidata,
     OpenStreetMap, NFDI4Objects) wired to the ring nodes they actually
     connect to in the rest of the family (Part 4/5 of the talk) -- makes
     "this joins the real Linked Open Data cloud" concrete rather than
     asserted.

Produces (white background, no header/footer/title -- same A4-departure
rationale as S8/S9: single image on a slide, not a composited banner):
  img/fdox-talk-closing-a-sphere.svg / .png
  img/fdox-talk-closing-b-hubs.svg / .png

Runnable standalone: `python py/step_talk_closing.py`
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals_utils import (  # noqa: E402
    FDO_ACCENT,
    FDO_ACCENT_LIGHT,
    IMG_DIR,
    INK,
    STEPS,
    ensure_dirs,
    esc,
    font_face_css,
    render_svg_to_png,
)
from step_pattern import BADGE_R, _node_icon  # noqa: E402 -- exact same step glyphs as S2
from step_fdo_meta import ACCENT_STROKE, INNER_R, OUTER_R, RING_FILL  # noqa: E402 -- exact same sphere as S3
from step_purpose import PROPERTIES  # noqa: E402 -- titles, same source as S7

CONNECTOR = "#A9B3C4"

W, H = 1750, 1000
OVERSAMPLE = 2

# Purpose titles reused from S7's own PROPERTIES; two are abbreviated here
# purely for space around an eight-node ring (S7's banner has a whole
# column per item, this has ~150px of arc) -- same wording, shorter.
_PURPOSE_TITLE_OVERRIDE = {"semantically-queryable": "Sem. Queryable"}

# Step titles are two-line in S2 ("FDO"/"Encapsulation" etc, see
# visuals_utils.STEPS) -- abbreviated to one short line each here for the
# same space reason as the purpose titles above.
_STEP_TITLE_OVERRIDE = {
    "fdo-encapsulation": "Encapsulation",
    "semantic-paradata-modelling": "Semantic Metadata",
    "linking-community-hubs": "Linking to Hubs",
    "federated-kg-integration": "Federated KG",
}


def _purpose_title(idx: int) -> str:
    item = PROPERTIES[idx]
    return _PURPOSE_TITLE_OVERRIDE.get(item["id"], item["title"])


def _purpose_icon_glyph(idx: int) -> str:
    """The four S7 glyphs (_icon_document/_icon_triples/_icon_hub/
    _icon_network), reproduced at this module's own (much smaller) scale
    rather than imported: S7's four functions are hard-coded to
    `ICON_S = ICON_R/78`, a module constant, not a parameter, so importing
    them here would still need S7's own ICON_R=100 -- more than triple
    this ring's node radius. Documented rather than silently duplicated
    (see PRIMER S9's identical note); a future `ICON_S`-as-parameter
    refactor of step_purpose.py would let this become a real import.
    """
    if idx == 0:
        x0, y0, w, h, fold = -13, -16, 26, 32, 7
        return (f'<path d="M {x0} {y0} h {w-fold} l {fold} {fold} v {h-fold} h -{w} z" fill="none" stroke="#FFFFFF" '
                f'stroke-width="2" stroke-linejoin="round"/>'
                f'<line x1="{x0+5}" y1="{y0+10}" x2="{x0+w-5}" y2="{y0+10}" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round"/>'
                f'<line x1="{x0+5}" y1="{y0+15}" x2="{x0+w-5}" y2="{y0+15}" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round"/>'
                f'<path d="M {x0+5} {y0+20} l 3.5 3.5 l 7 -7" fill="none" stroke="#FFFFFF" stroke-width="2" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    if idx == 1:
        pts = [(0, -18), (-18, 12), (18, 12)]
        out = ('<line x1="0" y1="-18" x2="-18" y2="12" stroke="#FFFFFF" stroke-width="1.6"/>'
               '<line x1="0" y1="-18" x2="18" y2="12" stroke="#FFFFFF" stroke-width="1.6"/>'
               '<line x1="-18" y1="12" x2="18" y2="12" stroke="#FFFFFF" stroke-width="1.6" stroke-dasharray="1 3" stroke-linecap="round"/>')
        out += "".join(f'<circle cx="{x}" cy="{y}" r="4.3" fill="#FFFFFF"/>' for x, y in pts)
        return out
    if idx == 2:
        pts = [(0, -20), (20, 0), (0, 20), (-20, 0)]
        out = "".join(f'<line x1="0" y1="0" x2="{x}" y2="{y}" stroke="#FFFFFF" stroke-width="1.6"/>' for x, y in pts)
        out += "".join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#FFFFFF"/>' for x, y in pts)
        out += '<circle cx="0" cy="0" r="4.7" fill="#FFFFFF"/>'
        return out
    clusters = [(-15, -11), (16, -8), (-2, 17)]
    out = ""
    for a, b in ((0, 1), (1, 2), (2, 0)):
        (x1, y1), (x2, y2) = clusters[a], clusters[b]
        out += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFFFFF" stroke-width="1.4"/>'
    for x, y in clusters:
        out += f'<circle cx="{x}" cy="{y}" r="6.2" fill="none" stroke="#FFFFFF" stroke-width="1.4"/>'
        out += f'<circle cx="{x}" cy="{y}" r="2" fill="#FFFFFF"/>'
    return out


def _svg_open() -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>',
        font_face_css(),
        '<defs><linearGradient id="talkClosingPurposeGrad" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{FDO_ACCENT_LIGHT}"/><stop offset="100%" stop-color="{FDO_ACCENT}"/>'
        "</linearGradient></defs>",
    ]


def _ring_positions(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    angles = [-90, -45, 0, 45, 90, 135, 180, 225]
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in angles]


_ANGLES = [-90, -45, 0, 45, 90, 135, 180, 225]


def _sphere(cx: float, cy: float, outer_r: float) -> list[str]:
    scale = outer_r / OUTER_R
    inner_r = INNER_R * scale
    p = [f'<circle cx="{cx}" cy="{cy}" r="{outer_r:.1f}" fill="{RING_FILL}" stroke="{FDO_ACCENT}" stroke-width="5"/>']
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{inner_r:.1f}" fill="{FDO_ACCENT}" stroke="{ACCENT_STROKE}" stroke-width="5"/>')
    fs = 22 if outer_r < 90 else 26
    p.append(f'<text x="{cx}" y="{cy-fs*0.3:.1f}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
              f'font-size="{fs}" fill="white" letter-spacing="2">I0I0</text>')
    p.append(f'<text x="{cx}" y="{cy+fs:.1f}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
              f'font-size="{fs}" fill="white" letter-spacing="2">0I0I</text>')
    return p


def _ring(cx: float, cy: float, r: float, node_r: float) -> tuple[list[str], list[tuple[float, float]]]:
    pts = _ring_positions(cx, cy, r)
    parts = []
    for i in range(8):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 8]
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{CONNECTOR}" stroke-width="2.5"/>')
    for x, y in pts:
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{CONNECTOR}" stroke-width="1.6" opacity="0.55"/>')

    step_i = purpose_i = 0
    for i, (x, y) in enumerate(pts):
        if i % 2 == 0:
            step = STEPS[step_i]; step_i += 1
            color, tint = step["color"], step["tint"]
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r}" fill="{tint}" stroke="{color}" stroke-width="4"/>')
            parts.append(f'<g transform="translate({x:.1f},{y:.1f}) scale({node_r/BADGE_R})">{_node_icon(step_i-1, color)}</g>')
            title = _STEP_TITLE_OVERRIDE[step["id"]]
        else:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r}" fill="url(#talkClosingPurposeGrad)"/>')
            parts.append(f'<g transform="translate({x:.1f},{y:.1f}) scale({node_r/72})">{_purpose_icon_glyph(purpose_i)}</g>')
            title = _purpose_title(purpose_i)
            purpose_i += 1

        a = _ANGLES[i]
        rad = math.radians(a)
        lx = x + math.cos(rad) * (node_r + 26)
        ly = y + math.sin(rad) * (node_r + 26)
        if abs(math.cos(rad)) < 0.3:
            anchor = "middle"
        elif math.cos(rad) > 0:
            anchor = "start"
        else:
            anchor = "end"
        dy = 8 if math.sin(rad) > 0.3 else (-4 if math.sin(rad) < -0.3 else 6)
        parts.append(f'<text x="{lx:.1f}" y="{ly+dy:.1f}" text-anchor="{anchor}" font-family="Fira Sans" '
                      f'font-weight="700" font-size="21" fill="{INK}">{esc(title)}</text>')
    return parts, pts


def _build_variant_a() -> str:
    p = _svg_open()
    cx, cy, r = 875, 512, 335
    ring_parts, _ = _ring(cx, cy, r, 72)
    p += ring_parts
    p += _sphere(cx, cy, 118)
    p.append("</svg>")
    return "\n".join(p)


def _build_variant_b() -> str:
    p = _svg_open()
    cx, cy, r = 1015, 512, 330
    ring_parts, pts = _ring(cx, cy, r, 72)
    p += ring_parts
    p += _sphere(cx, cy, 118)

    # real external hubs, wired to the ring node each one actually connects
    # to elsewhere in the talk (Part 4/5): OpenStreetMap/Wikidata via
    # dct:spatial/dct:subject (Folie C/G), NFDI4Objects via the registry
    # harvest (Folie D).
    hub_r = 58
    hubs = [
        ("OpenStreetMap", 200, 860, 4),   # -> step 3, Linking to Hubs
        ("Wikidata", 150, 545, 5),        # -> purpose 3, Interoperable
        ("NFDI4Objects", 200, 290, 7),    # -> purpose 4, Integrable
    ]
    for name, hx, hy, target_idx in hubs:
        tx, ty = pts[target_idx]
        p.append(f'<line x1="{hx}" y1="{hy}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{FDO_ACCENT_LIGHT}" '
                  f'stroke-width="2.5" stroke-dasharray="2 8" stroke-linecap="round"/>')
    for name, hx, hy, _ in hubs:
        p.append(f'<circle cx="{hx}" cy="{hy}" r="{hub_r}" fill="{FDO_ACCENT}"/>')
        p.append(f'<text x="{hx}" y="{hy-hub_r-16}" text-anchor="middle" font-family="Fira Sans" font-weight="700" '
                  f'font-size="21" fill="{INK}">{esc(name)}</text>')

    p.append("</svg>")
    return "\n".join(p)


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []

    for name, build_fn in [
        ("fdox-talk-closing-a-sphere", _build_variant_a),
        ("fdox-talk-closing-b-hubs", _build_variant_b),
    ]:
        svg_path = IMG_DIR / f"{name}.svg"
        svg_path.write_text(build_fn(), encoding="utf-8")
        png_path = svg_path.with_suffix(".png")
        render_svg_to_png(svg_path, png_path, W * OVERSAMPLE, H * OVERSAMPLE)
        from PIL import Image
        with Image.open(png_path) as im:
            w, h = im.size
        log.append(f"wrote img/{name}.svg + .png ({w}x{h}, white background)")

    return log


if __name__ == "__main__":
    for line in run():
        print(line)
