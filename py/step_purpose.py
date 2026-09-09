"""S7 — FDOx purpose banner ('What does FDOx do?').

Companion piece to S2's four-step *process* banner: where S2 names the
pipeline stages (Encapsulation -> ... -> Federation), this one names the
resulting *properties* of an FDOx-published artefact, in the same order
(each property is that stage's outcome). Single flat FDOx blue rather than
S2's four-colour rainbow, since this is one continuous claim about one
kind of object, not four distinct stages.

Produces:
  img/fdox-purpose-pattern.svg / .png   content-only banner, transparent,
                                         no header/footer (A4 convention)
  img/fdox-purpose-<n>-<slug>.svg / .png   one badge per property, transparent

Runnable standalone: `python py/step_purpose.py`
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
    ensure_dirs,
    esc,
    font_face_css,
    render_svg_to_png,
    trim_transparent_border,
    wrap_text,
)

PROPERTIES = [
    {
        "id": "fair-citable",
        "num": "1",
        "title": "FAIR & Citable",
        "desc": "Research artefacts with persistent identifiers & rich RDF/DCAT metadata",
    },
    {
        "id": "semantically-queryable",
        "num": "2",
        "title": "Semantically Queryable",
        "desc": "Entities as RDF triples, discoverable and queryable via SPARQL endpoints",
    },
    {
        "id": "interoperable",
        "num": "3",
        "title": "Interoperable",
        "desc": "Nodes connected to Community Hubs like NFDI4Objects (N4O)",
    },
    {
        "id": "integrable",
        "num": "4",
        "title": "Integrable",
        "desc": "Components of federated knowledge graph infrastructures",
    },
]

ICON_R = 100
TAG_R = 30
TAG_DX, TAG_DY = 72, 72  # tag centre offset from badge centre (top-right)
ICON_S = ICON_R / 78.0  # scale factor the four icon glyphs below are tuned at (R=78)

W = 2000
MARGIN_X = 30
COL_W = (W - 2 * MARGIN_X) / 4
CENTERS = [MARGIN_X + COL_W * (i + 0.5) for i in range(4)]

TOP_MARGIN = 60
ICON_CY = TOP_MARGIN + ICON_R + TAG_DY - ICON_R  # = TOP_MARGIN + TAG_DY, tag is the topmost point
TITLE_Y = ICON_CY + 162
DESC_Y0 = ICON_CY + 212
DESC_LH = 37
BOTTOM_MARGIN = 40

# render scale: authored in the W-wide design grid above, rasterised at
# OVERSAMPLE/ICON_SCALE x that grid, then trimmed to content (see
# trim_transparent_border). Tuned to land the banner and each icon in the
# same ~2-6 megapixel content range as every other graphic in this repo
# (A4: Google Slides recompresses well before its 25MP ceiling).
OVERSAMPLE = 2.5
ICON_SCALE = 5.6


def _icon_document(cx: float, cy: float) -> str:
    """FAIR & Citable: a certificate — page, ruled lines, checkmark."""
    x0, y0 = cx - 34 * ICON_S, cy - 42 * ICON_S
    w, h = 68 * ICON_S, 84 * ICON_S
    fold = 18 * ICON_S
    return (
        f'<path d="M {x0} {y0} h {w - fold} l {fold} {fold} v {h - fold} h -{w} z" '
        f'fill="none" stroke="#FFFFFF" stroke-width="{5 * ICON_S}" stroke-linejoin="round"/>'
        f'<path d="M {x0 + w - fold} {y0} v {fold} h {fold} z" fill="#FFFFFF" opacity="0.85"/>'
        f'<line x1="{x0 + 12 * ICON_S}" y1="{y0 + 26 * ICON_S}" x2="{x0 + w - 14 * ICON_S}" y2="{y0 + 26 * ICON_S}" '
        f'stroke="#FFFFFF" stroke-width="{4 * ICON_S}" stroke-linecap="round"/>'
        f'<line x1="{x0 + 12 * ICON_S}" y1="{y0 + 38 * ICON_S}" x2="{x0 + w - 14 * ICON_S}" y2="{y0 + 38 * ICON_S}" '
        f'stroke="#FFFFFF" stroke-width="{4 * ICON_S}" stroke-linecap="round"/>'
        f'<path d="M {x0 + 12 * ICON_S} {y0 + 52 * ICON_S} l {9 * ICON_S} {9 * ICON_S} l {17 * ICON_S} -{17 * ICON_S}" '
        f'fill="none" stroke="#FFFFFF" stroke-width="{5 * ICON_S}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def _icon_triples(cx: float, cy: float) -> str:
    """Semantically Queryable: an RDF triple — subject, predicate, object."""
    p_top = (cx, cy - 46 * ICON_S)
    p_left = (cx - 46 * ICON_S, cy + 32 * ICON_S)
    p_right = (cx + 46 * ICON_S, cy + 32 * ICON_S)
    r = 11 * ICON_S
    out = (
        f'<line x1="{p_top[0]}" y1="{p_top[1]}" x2="{p_left[0]}" y2="{p_left[1]}" stroke="#FFFFFF" stroke-width="{4 * ICON_S}"/>'
        f'<line x1="{p_top[0]}" y1="{p_top[1]}" x2="{p_right[0]}" y2="{p_right[1]}" stroke="#FFFFFF" stroke-width="{4 * ICON_S}"/>'
        f'<line x1="{p_left[0]}" y1="{p_left[1]}" x2="{p_right[0]}" y2="{p_right[1]}" stroke="#FFFFFF" '
        f'stroke-width="{4 * ICON_S}" stroke-dasharray="2 7" stroke-linecap="round"/>'
    )
    for x, y in (p_top, p_left, p_right):
        out += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF"/>'
    return out


def _icon_hub(cx: float, cy: float) -> str:
    """Interoperable: a hub with four spokes — Community Hub linkage."""
    r_out, r_in = 52 * ICON_S, 12 * ICON_S
    pts = [(cx, cy - r_out), (cx + r_out, cy), (cx, cy + r_out), (cx - r_out, cy)]
    out = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#FFFFFF" stroke-width="{4 * ICON_S}"/>' for x, y in pts
    )
    out += "".join(f'<circle cx="{x}" cy="{y}" r="{9 * ICON_S}" fill="#FFFFFF"/>' for x, y in pts)
    out += f'<circle cx="{cx}" cy="{cy}" r="{r_in}" fill="#FFFFFF"/>'
    return out


def _icon_network(cx: float, cy: float) -> str:
    """Integrable: three linked clusters — a network of networks."""
    clusters = [(cx - 40 * ICON_S, cy - 28 * ICON_S), (cx + 42 * ICON_S, cy - 20 * ICON_S), (cx - 6 * ICON_S, cy + 44 * ICON_S)]
    out = ""
    for a, b in ((0, 1), (1, 2), (2, 0)):
        (x1, y1), (x2, y2) = clusters[a], clusters[b]
        out += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFFFFF" stroke-width="{3.5 * ICON_S}"/>'
    for x, y in clusters:
        out += f'<circle cx="{x}" cy="{y}" r="{16 * ICON_S}" fill="none" stroke="#FFFFFF" stroke-width="{3.5 * ICON_S}"/>'
        out += f'<circle cx="{x}" cy="{y}" r="{5 * ICON_S}" fill="#FFFFFF"/>'
    return out


ICON_FNS = [_icon_document, _icon_triples, _icon_hub, _icon_network]


def _defs() -> str:
    return (
        "<defs>"
        f'<linearGradient id="purposeIconGrad" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{FDO_ACCENT_LIGHT}"/>'
        f'<stop offset="100%" stop-color="{FDO_ACCENT}"/>'
        "</linearGradient>"
        "</defs>"
    )


def _badge_markup(cx: float, cy: float, idx: int, item: dict) -> str:
    tag_x, tag_y = cx + TAG_DX, cy - TAG_DY
    out = f'<circle cx="{cx}" cy="{cy}" r="{ICON_R}" fill="url(#purposeIconGrad)"/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{ICON_R}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.35"/>'
    out += ICON_FNS[idx](cx, cy)
    out += f'<circle cx="{tag_x}" cy="{tag_y}" r="{TAG_R}" fill="#FFFFFF" stroke="{FDO_ACCENT}" stroke-width="3.5"/>'
    out += (
        f'<text x="{tag_x}" y="{tag_y + 10}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="29" fill="{FDO_ACCENT}">{item["num"]}</text>'
    )
    return out


def _arrow(x_center: float, y: float) -> str:
    out = ""
    for i, dx in enumerate((-16, 4)):
        x = x_center + dx
        opacity = 0.55 + 0.25 * i
        out += (
            f'<path d="M {x - 14} {y - 24} L {x + 14} {y} L {x - 14} {y + 24}" fill="none" '
            f'stroke="{FDO_ACCENT_SOFT}" stroke-width="7" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{opacity}"/>'
        )
    return out


def _build_content_svg(desc_lines_per_item: list[list[str]]) -> tuple[str, int]:
    max_desc_lines = max(len(x) for x in desc_lines_per_item)
    h = int(DESC_Y0 + (max_desc_lines - 1) * DESC_LH + 30 + BOTTOM_MARGIN)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">']
    p.append(font_face_css())
    p.append(_defs())

    gap_centers = [(CENTERS[i] + CENTERS[i + 1]) / 2 for i in range(3)]
    for gx in gap_centers:
        p.append(_arrow(gx, ICON_CY))

    for i, (cx, item) in enumerate(zip(CENTERS, PROPERTIES)):
        p.append(_badge_markup(cx, ICON_CY, i, item))
        p.append(
            f'<text x="{cx}" y="{TITLE_Y}" text-anchor="middle" font-family="Fira Sans" '
            f'font-weight="700" font-size="33" fill="{INK}">{esc(item["title"])}</text>'
        )
        for j, line in enumerate(desc_lines_per_item[i]):
            p.append(
                f'<text x="{cx}" y="{DESC_Y0 + j * DESC_LH}" text-anchor="middle" font-family="Fira Sans" '
                f'font-weight="400" font-size="25" fill="{MUTED}">{esc(line)}</text>'
            )
    p.append("</svg>")
    return "\n".join(p), h


def _build_icon_svg(idx: int, item: dict) -> tuple[str, int]:
    pad = 15
    left = -(ICON_R + TAG_DY) - pad  # tag pokes above/right of the icon circle
    top = -(ICON_R + TAG_DY) - pad
    right = ICON_R + TAG_DX + pad
    bottom = ICON_R + pad
    vb_w, vb_h = right - left, bottom - top
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{vb_w}" height="{vb_h}" '
        f'viewBox="{left} {top} {vb_w} {vb_h}">'
    ]
    p.append(font_face_css())
    p.append(_defs())
    p.append(_badge_markup(0, 0, idx, item))
    p.append("</svg>")
    return "\n".join(p), vb_w


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []
    warnings: list[str] = []

    desc_lines_per_item = [wrap_text(p["desc"]) for p in PROPERTIES]
    for item, lines in zip(PROPERTIES, desc_lines_per_item):
        if len(lines) > 3:
            warnings.append(f'description for "{item["id"]}" wraps to {len(lines)} lines (design assumes <=3)')

    svg_text, h = _build_content_svg(desc_lines_per_item)
    svg_path = IMG_DIR / "fdox-purpose-pattern.svg"
    svg_path.write_text(svg_text, encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    render_svg_to_png(svg_path, png_path, int(W * OVERSAMPLE), int(h * OVERSAMPLE))
    final_w, final_h = trim_transparent_border(png_path, margin_px=10)
    log.append(
        f"wrote {svg_path.relative_to(IMG_DIR.parent)} + .png "
        f"({final_w}x{final_h}, transparent, <=10px border)"
    )

    for i, item in enumerate(PROPERTIES):
        svg_text, vb = _build_icon_svg(i, item)
        svg_path = IMG_DIR / f"fdox-purpose-{item['num']}-{item['id']}.svg"
        svg_path.write_text(svg_text, encoding="utf-8")
        png_path = svg_path.with_suffix(".png")
        render_svg_to_png(svg_path, png_path, int(vb * ICON_SCALE), int(vb * ICON_SCALE))
        final_w, final_h = trim_transparent_border(png_path, margin_px=10)
        log.append(
            f"wrote {svg_path.relative_to(IMG_DIR.parent)} + .png "
            f"({final_w}x{final_h}, transparent, <=10px border)"
        )

    if warnings:
        for w in warnings:
            log.append(f"WARNING: {w}")
        if strict:
            raise RuntimeError(f"{len(warnings)} warning(s) in step 'purpose' (--strict)")

    return log


if __name__ == "__main__":
    for line in run():
        print(line)
