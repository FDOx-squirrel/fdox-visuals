"""S6 — CITATION.cff schema diagram ("the minimum CFF").

Unlike MD.cff (FDOx's own schema), CITATION.cff is the external, standard
Citation File Format (cff-version 1.2.0) — fdo-squirrel doesn't define it,
it only reads a subset of it. Built from
`fdo-squirrel/crosswalks/crosswalk.fdo-metadata.yaml` (which fields are
mapped at all) cross-checked against
`fdo-squirrel/crosswalks/citation_crosswalk_engine.py`'s
`_normalize_citation()` (which of those mapped fields actually reach the
RDF output). The two don't fully agree — see PRIMER.md A1 for the
finding: 14 of the 22 fields the crosswalk YAML maps are silently dropped
before any RDF is emitted, because `_normalize_citation()` only forwards
a fixed allow-list.

One class box, not two (first version split "forwarded" and "not
forwarded" into two separately-titled `CITATION_cff` boxes — confusing,
read as two copies of the same class rather than one class with a
per-field status; see PRIMER.md A1 Befund 13). Fields are grouped the way
a person reading a CITATION.cff would group them (identity, people,
provenance/links, licensing, repository), same as any other class
diagram; the RDF status is a per-field `[not in RDF]` tag, the same
bracket convention MD.cff's diagram already uses for `[required]`, not a
second box. Author/Identifier satellites sit next to the three rows that
actually reference them (authors, contributors, identifiers — grouped
adjacently for exactly this reason), so the connecting lines are short
and don't cross each other.

Produces:
  img/fdox-citation-cff-schema.svg / .png (transparent)

Runnable standalone: `python py/step_citation_cff_schema.py`
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

ACCENT = "#0E9488"
TINT = "#E6F6F4"

BOX_W = 520
FIELD_H = 30
HEADER_H = 46
PAD_V = 14
ROW_GAP = 34
COL_GAP = 420

# (field text, forwarded-to-RDF?)
FIELDS = [
    ("string title", False),
    ("string abstract", True),
    ("string type", False),
    ("string version", False),
    ("string date-released", False),
    ("string cff-version", False),
    ("list<Author> authors", True),
    ("list<Author> contributors", False),
    ("list<Identifier> identifiers", True),
    ("string doi", False),
    ("string url", True),
    ("string repository", True),
    ("string repository-code", True),
    ("string repository-artifact", False),
    ("string license", True),
    ("string license-url", False),
    ("string[] keywords", True),
    ("string commit", False),
    ("string contact", False),
    ("string message", False),
    ("list preferred-citation", False),
    ("list references", False),
]

# indices (0-based) into FIELDS, for connecting lines to satellites
IDX_AUTHORS = 6
IDX_CONTRIBUTORS = 7
IDX_IDENTIFIERS = 8

SATELLITES = [
    ("Author", ["string given-names", "string family-names", "string orcid"]),
    ("Identifier", ["string type", "string value"]),
]


def _render_box(x: float, y: float, w: float, title: str, fields: list[str], accent: str, tint: str) -> tuple[str, float]:
    header_h = HEADER_H
    h = header_h + len(fields) * FIELD_H + 2 * PAD_V
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{tint}" stroke="{accent}" stroke-width="3"/>'
    out += (
        f'<text x="{x+w/2}" y="{y+30}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="26" fill="{INK}">{esc(title)}</text>'
    )
    out += f'<line x1="{x}" y1="{y+header_h}" x2="{x+w}" y2="{y+header_h}" stroke="{accent}" stroke-width="2.5"/>'
    fy = y + header_h + 22
    for f in fields:
        out += (
            f'<text x="{x+16}" y="{fy}" text-anchor="start" font-family="Fira Sans" '
            f'font-weight="400" font-size="18" fill="{INK}">+ {esc(f)}</text>'
        )
        fy += FIELD_H
    return out, h


def _field_row_y(box_top: float, idx: int) -> float:
    """Absolute y of field row `idx`'s text baseline, matching _render_box's own layout math."""
    return box_top + HEADER_H + 22 + idx * FIELD_H


def _build_svg() -> tuple[str, float, float]:
    pad = 50

    # centre class box height (computed once so satellites can be placed
    # relative to it before we render anything)
    center_h = HEADER_H + len(FIELDS) * FIELD_H + 2 * PAD_V
    center_x = pad
    center_y = pad

    right_x = center_x + BOX_W + COL_GAP

    # satellite y-positions: Author sits centred between the authors and
    # contributors rows (rows 6 and 7); Identifier sits level with the
    # identifiers row (row 8) - all three are adjacent in FIELDS, so both
    # satellites land close to the same, small stretch of the centre box.
    author_target_y = (
        _field_row_y(center_y, IDX_AUTHORS) + _field_row_y(center_y, IDX_CONTRIBUTORS)
    ) / 2 - FIELD_H / 2
    ident_target_y = _field_row_y(center_y, IDX_IDENTIFIERS) - FIELD_H / 2

    sat_heights = [HEADER_H + len(f) * FIELD_H + 2 * PAD_V for _, f in SATELLITES]
    author_y = author_target_y - sat_heights[0] / 2
    ident_y = ident_target_y - sat_heights[1] / 2
    # keep Identifier comfortably below Author (min gap), since their
    # target rows are close together but the boxes themselves are taller
    min_gap = 24
    if ident_y < author_y + sat_heights[0] + min_gap:
        ident_y = author_y + sat_heights[0] + min_gap
    sat_y = {"Author": author_y, "Identifier": ident_y}

    content_bottom = max(center_y + center_h, ident_y + sat_heights[1])
    footnote_h = 90
    W = right_x + BOX_W + pad
    H = content_bottom + footnote_h

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    parts.append(font_face_css())

    # connecting lines, drawn first (under the boxes)
    lines = []

    def _line(from_y: float, sat_title: str, sat_h: float):
        ty = sat_y[sat_title] + sat_h / 2
        lines.append(
            f'<line x1="{center_x+BOX_W}" y1="{from_y}" x2="{right_x}" y2="{ty}" '
            f'stroke="{MUTED}" stroke-width="2.5"/>'
        )

    _line(_field_row_y(center_y, IDX_AUTHORS) - 6, "Author", sat_heights[0])
    _line(_field_row_y(center_y, IDX_CONTRIBUTORS) - 6, "Author", sat_heights[0])
    _line(_field_row_y(center_y, IDX_IDENTIFIERS) - 6, "Identifier", sat_heights[1])
    parts += lines

    center_labels = [
        f"{txt}" + ("" if fwd else " [not in RDF]\u00b9") for txt, fwd in FIELDS
    ]
    center_svg, _ = _render_box(center_x, center_y, BOX_W, "CITATION_cff", center_labels, ACCENT, TINT)
    # override colour per-field: forwarded rows stay ink, dropped rows go muted.
    # _render_box always uses INK, so re-render field text on top in the
    # right colour instead of re-deriving the geometry twice.
    field_overlay = ""
    fy = center_y + HEADER_H + 22
    for (txt, fwd), label in zip(FIELDS, center_labels):
        if not fwd:
            field_overlay += (
                f'<rect x="{center_x+1.5}" y="{fy-22}" width="{BOX_W-3}" height="{FIELD_H}" fill="{TINT}"/>'
                f'<text x="{center_x+16}" y="{fy}" text-anchor="start" font-family="Fira Sans" '
                f'font-weight="400" font-size="18" fill="{MUTED}">+ {esc(label)}</text>'
            )
        fy += FIELD_H
    parts.append(center_svg)
    parts.append(field_overlay)

    for title, fields in SATELLITES:
        box_svg, _ = _render_box(right_x, sat_y[title], BOX_W, title, fields, ACCENT, TINT)
        parts.append(box_svg)

    footnote_y = content_bottom + 46
    parts.append(
        f'<text x="{pad}" y="{footnote_y}" text-anchor="start" font-family="Fira Sans" '
        f'font-weight="400" font-size="19" fill="{MUTED}">\u00b9 fdo-squirrel/crosswalks/citation_crosswalk_engine.py: '
        f'_normalize_citation() only forwards a fixed allow-list before</text>'
    )
    parts.append(
        f'<text x="{pad}" y="{footnote_y+28}" text-anchor="start" font-family="Fira Sans" '
        f'font-weight="400" font-size="19" fill="{MUTED}">the crosswalk rules run \u2014 these fields are mapped in the YAML but never reach RDF today.</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts), W, H


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []

    svg_text, w, h = _build_svg()
    svg_path = IMG_DIR / "fdox-citation-cff-schema.svg"
    svg_path.write_text(svg_text, encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    render_svg_to_png(svg_path, png_path, int(w * 1.7), int(h * 1.7))
    final_w, final_h = trim_transparent_border(png_path, margin_px=10)
    log.append(
        f"wrote {svg_path.relative_to(IMG_DIR.parent)} + .png "
        f"({final_w}x{final_h}, transparent, <=10px border)"
    )
    return log


if __name__ == "__main__":
    for line in run():
        print(line)
