"""S5 — MD.cff schema class diagram.

No generator for this existed anywhere in the FDOx-squirrel family (see
PRIMER.md A1) — built fresh from fdo-squirrel-spec's actual
`data/raw/MD.cff-schema.yaml` (checked 2026-09-08), not from the earlier
hand-made diagram, which had drifted from the schema on several concrete
points (see PRIMER.md A1 for the list).

Produces:
  img/fdox-md-cff-schema.svg / .png (transparent)

Runnable standalone: `python py/step_md_cff_schema.py`
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals_utils import (  # noqa: E402
    IMG_DIR,
    INK,
    MUTED,
    ensure_dirs,
    esc,
    font_face_css,
    render_svg_to_png,
    trim_transparent_border,
)

ACCENT = "#0E9488"   # Step-2 teal: this whole diagram IS "semantic metadata modelling"
TINT = "#E6F6F4"
CENTER_ACCENT = "#004473"
CENTER_TINT = "#E6ECF1"

BOX_W = 430
FIELD_H = 30
HEADER_H = 46
PAD_V = 14
COL_GAP = 620
ROW_GAP = 34

# (title, stereotype-or-None, [field strings], cardinality-label, dashed?)
LEFT = [
    ("Keywords", None, ["string label [required]", "iri id"], "0..*", False),
    ("License", None, ["string label [required]", "iri id"], "0..1", False),
    ("Publishers", None, ["string label [required]", "iri id"], "1..*", False),
    ("Creators", None, ["string label [required]", "iri id"], "0..*", False),
    ("Contributors", None, ["string label [required]", "iri id"], "0..*", False),
    ("Identifiers", None, ["string scheme [required]", "string value [required]", "string label"], "0..*", False),
    ("FDO_Class_Vocab", "enum", ["Software : fdo:SoftwareFDO", "Analysis : fdo:AnalysisFDO", "3D Data : fdo:3DDataFDO"], "1", True),
]

RIGHT = [
    ("Spatial", None, ["string label [required]", "iri id", "string wkt", "string bounding_box", "float lon", "float lat"], "0..1", False),
    ("Temporal", None, ["string label [required]", "iri id", "integer start", "integer end", "integer[2] range"], "0..1", False),
    ("HeritageObject", None, ["object object_type", "object monument", "object material", "string context", "string documentation_purpose", "string overall_condition", "string conservation_urgency"], "0..1", False),
    ("Technique", None, ["object acquisition", "string|object processing", "string[] programming_languages", "object repository"], "0..1", False),
    ("RelatedResources", None, ["string relation [required]", "object target [required]", "string note"], "0..*", False),
    ("Distributions", None, ["string id [required]", "string label [required]", "string media_type", "object checksum"], "0..*", False),
]

CENTER_FIELDS = [
    "string md_cff_version [required]",
    "string fdo_type [required]",
    "iri id [required]",
    "string title [required]",
    "string description [required]",
    "string version",
    "date date_created",
    "date date_released",
    "date[] date_modified",
    "string[] funding",
]


def _render_box(x: float, y: float, w: float, title: str, stereotype: str | None, fields: list[str], accent: str, tint: str) -> tuple[str, float]:
    header_h = HEADER_H + (26 if stereotype else 0)
    h = header_h + len(fields) * FIELD_H + 2 * PAD_V
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{tint}" stroke="{accent}" stroke-width="3"/>'
    if stereotype:
        out += (
            f'<text x="{x+w/2}" y="{y+24}" text-anchor="middle" font-family="Fira Sans" '
            f'font-weight="400" font-size="20" fill="{accent}">\u00ab{stereotype}\u00bb</text>'
        )
        out += (
            f'<text x="{x+w/2}" y="{y+50}" text-anchor="middle" font-family="Fira Sans" '
            f'font-weight="700" font-size="26" fill="{INK}">{esc(title)}</text>'
        )
    else:
        out += (
            f'<text x="{x+w/2}" y="{y+30}" text-anchor="middle" font-family="Fira Sans" '
            f'font-weight="700" font-size="26" fill="{INK}">{esc(title)}</text>'
        )
    out += f'<line x1="{x}" y1="{y+header_h}" x2="{x+w}" y2="{y+header_h}" stroke="{accent}" stroke-width="2.5"/>'
    fy = y + header_h + 24
    for f in fields:
        out += (
            f'<text x="{x+16}" y="{fy}" text-anchor="start" font-family="Fira Sans" '
            f'font-weight="400" font-size="19" fill="{INK}">+ {esc(f)}</text>'
        )
        fy += FIELD_H
    return out, h


def _build_svg() -> tuple[str, float, float]:
    left_heights = [HEADER_H + (26 if s else 0) + len(f) * FIELD_H + 2 * PAD_V for _, s, f, _, _ in LEFT]
    right_heights = [HEADER_H + (26 if s else 0) + len(f) * FIELD_H + 2 * PAD_V for _, s, f, _, _ in RIGHT]

    left_total = sum(left_heights) + (len(LEFT) - 1) * ROW_GAP
    right_total = sum(right_heights) + (len(RIGHT) - 1) * ROW_GAP
    content_h = max(left_total, right_total)

    center_h = HEADER_H + len(CENTER_FIELDS) * FIELD_H + 2 * PAD_V
    center_w = 480

    pad = 50
    left_x = pad
    right_x = left_x + BOX_W + COL_GAP
    W = right_x + BOX_W + pad
    H = content_h + 2 * pad

    center_x = left_x + BOX_W + (COL_GAP - center_w) / 2
    center_y = pad + content_h / 2 - center_h / 2

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    parts.append(font_face_css())

    # left column
    ly = pad
    left_positions = []
    for (title, stereotype, fields, card, dashed), h in zip(LEFT, left_heights):
        box_svg, hh = _render_box(left_x, ly, BOX_W, title, stereotype, fields, ACCENT, TINT)
        parts.append(box_svg)
        left_positions.append((ly, hh, card, dashed))
        ly += hh + ROW_GAP

    # right column
    ry = pad
    right_positions = []
    for (title, stereotype, fields, card, dashed), h in zip(RIGHT, right_heights):
        box_svg, hh = _render_box(right_x, ry, BOX_W, title, stereotype, fields, ACCENT, TINT)
        parts.append(box_svg)
        right_positions.append((ry, hh, card, dashed))
        ry += hh + ROW_GAP

    # center box (drawn after columns' connecting lines so it sits on top visually? draw lines first)
    lines_svg = []
    for ly0, hh, card, dashed in left_positions:
        y_mid = ly0 + hh / 2
        x1 = left_x + BOX_W
        x2 = center_x
        dash = ' stroke-dasharray="10 8"' if dashed else ""
        lines_svg.append(
            f'<line x1="{x1}" y1="{y_mid}" x2="{x2}" y2="{center_y+center_h/2}" '
            f'stroke="{MUTED}" stroke-width="2.5"{dash}/>'
        )
        lines_svg.append(
            f'<text x="{x1+22}" y="{y_mid-10}" text-anchor="start" font-family="Fira Sans" '
            f'font-weight="400" font-size="18" fill="{MUTED}">{card}</text>'
        )
    for ry0, hh, card, dashed in right_positions:
        y_mid = ry0 + hh / 2
        x1 = right_x
        x2 = center_x + center_w
        dash = ' stroke-dasharray="10 8"' if dashed else ""
        lines_svg.append(
            f'<line x1="{center_x+center_w}" y1="{center_y+center_h/2}" x2="{x1}" y2="{y_mid}" '
            f'stroke="{MUTED}" stroke-width="2.5"{dash}/>'
        )
        lines_svg.append(
            f'<text x="{x1-22}" y="{y_mid-10}" text-anchor="end" font-family="Fira Sans" '
            f'font-weight="400" font-size="18" fill="{MUTED}">{card}</text>'
        )
    parts = parts[:2] + lines_svg + parts[2:]

    center_svg, _ = _render_box(center_x, center_y, center_w, "MD_cff", None, CENTER_FIELDS, CENTER_ACCENT, CENTER_TINT)
    parts.append(center_svg)

    parts.append("</svg>")
    return "\n".join(parts), W, H


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []

    svg_text, w, h = _build_svg()
    svg_path = IMG_DIR / "fdox-md-cff-schema.svg"
    svg_path.write_text(svg_text, encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    render_svg_to_png(svg_path, png_path, int(w * 1.6), int(h * 1.6))
    final_w, final_h = trim_transparent_border(png_path, margin_px=10)
    log.append(
        f"wrote {svg_path.relative_to(IMG_DIR.parent)} + .png "
        f"({final_w}x{final_h}, transparent, <=10px border)"
    )
    return log


if __name__ == "__main__":
    for line in run():
        print(line)
