"""S6 — CITATION.cff schema diagram ("the minimum CFF").

Unlike MD.cff (FDOx's own schema), CITATION.cff is the external, standard
Citation File Format (cff-version 1.2.0) — fdo-squirrel doesn't define it,
it only reads a subset of it. Built from
`fdo-squirrel/crosswalks/crosswalk.fdo-metadata.yaml` (which fields are
mapped at all) cross-checked against
`fdo-squirrel/crosswalks/citation_crosswalk_engine.py`'s
`_normalize_citation()` (which of those mapped fields actually reach the
RDF output). The two don't fully agree — see PRIMER.md A1 for the finding
this surfaced: 14 of the 22 fields the crosswalk YAML maps are silently
dropped before any RDF is emitted, because `_normalize_citation()` only
forwards a fixed allow-list. Both groups are drawn, visually distinguished,
rather than only drawing the ones that "work".

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
DROPPED_ACCENT = "#8A93A6"   # muted grey-blue: mapped in YAML, never reaches RDF
DROPPED_TINT = "#EEF0F3"

BOX_W = 460
FIELD_H = 28
HEADER_H = 44
PAD_V = 14
ROW_GAP = 34
COL_GAP = 560

FORWARDED = [
    "string abstract",
    "string url",
    "string repository-code",
    "string repository",
    "string license",
    "string[] keywords",
    "list<Identifier> identifiers",
    "list<Author> authors",
]

NOT_FORWARDED = [
    "string cff-version",
    "string message",
    "string title",
    "string type",
    "string version",
    "string date-released",
    "string doi",
    "string repository-artifact",
    "string license-url",
    "string commit",
    "string contact",
    "list<Author> contributors",
    "list preferred-citation",
    "list references",
]

SATELLITES = [
    ("Author", ["string given-names", "string family-names", "string orcid"]),
    ("Identifier", ["string type", "string value"]),
]


def _render_box(x: float, y: float, w: float, title: str, fields: list[str], accent: str, tint: str,
                 field_color: str | None = None, dashed: bool = False, subtitle: str | None = None) -> tuple[str, float]:
    extra = 22 if subtitle else 0
    header_h = HEADER_H + extra
    h = header_h + len(fields) * FIELD_H + 2 * PAD_V
    dash = ' stroke-dasharray="10 7"' if dashed else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{tint}" stroke="{accent}" stroke-width="3"{dash}/>'
    out += (
        f'<text x="{x+w/2}" y="{y+30}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="25" fill="{INK}">{esc(title)}</text>'
    )
    if subtitle:
        out += (
            f'<text x="{x+w/2}" y="{y+50}" text-anchor="middle" font-family="Fira Sans" '
            f'font-weight="400" font-size="16" fill="{accent}">{esc(subtitle)}</text>'
        )
    out += f'<line x1="{x}" y1="{y+header_h}" x2="{x+w}" y2="{y+header_h}" stroke="{accent}" stroke-width="2.5"{dash}/>'
    fy = y + header_h + 22
    fc = field_color or INK
    for f in fields:
        out += (
            f'<text x="{x+16}" y="{fy}" text-anchor="start" font-family="Fira Sans" '
            f'font-weight="400" font-size="18" fill="{fc}">+ {esc(f)}</text>'
        )
        fy += FIELD_H
    return out, h


def _build_svg() -> tuple[str, float, float]:
    pad = 50
    center_x = pad + BOX_W + COL_GAP / 2 - BOX_W / 2

    # center: two stacked boxes (forwarded, then not-forwarded)
    fwd_svg, fwd_h = _render_box(
        center_x, pad, BOX_W, "CITATION_cff", FORWARDED, ACCENT, TINT,
        subtitle="forwarded to RDF",
    )
    gap_between = 34
    dropped_svg, dropped_h = _render_box(
        center_x, pad + fwd_h + gap_between, BOX_W, "CITATION_cff", NOT_FORWARDED,
        DROPPED_ACCENT, DROPPED_TINT, field_color=MUTED, dashed=True,
        subtitle="mapped in crosswalk.fdo-metadata.yaml, not forwarded \u00b9",
    )
    center_total_h = fwd_h + gap_between + dropped_h

    # right column: satellites, vertically centred on the combined centre block
    sat_heights = [HEADER_H + len(f) * FIELD_H + 2 * PAD_V for _, f in SATELLITES]
    sat_total = sum(sat_heights) + (len(SATELLITES) - 1) * ROW_GAP
    right_x = center_x + BOX_W + COL_GAP
    sat_y0 = pad + center_total_h / 2 - sat_total / 2

    W = right_x + BOX_W + pad
    footnote_h = 90
    H = pad + max(center_total_h, sat_total) + footnote_h

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    parts.append(font_face_css())

    # connecting lines: authors/contributors/identifiers -> satellites
    lines = []
    sy = sat_y0
    sat_positions = []
    for (title, fields), hh in zip(SATELLITES, sat_heights):
        sat_positions.append((title, sy, hh))
        sy += hh + ROW_GAP

    def _line_to_sat(sat_title, from_x, from_y, dashed=False):
        for title, sy0, hh in sat_positions:
            if title == sat_title:
                dash = ' stroke-dasharray="10 7"' if dashed else ""
                lines.append(
                    f'<line x1="{from_x}" y1="{from_y}" x2="{right_x}" y2="{sy0+hh/2}" '
                    f'stroke="{MUTED}" stroke-width="2.5"{dash}/>'
                )

    # locate the y of "identifiers" and "authors" rows in the forwarded box,
    # and "contributors" in the not-forwarded box, for connecting lines
    def _field_y(box_top, subtitle_present, idx):
        header_h = HEADER_H + (22 if subtitle_present else 0)
        return box_top + header_h + 22 + idx * FIELD_H - 6

    idents_i = FORWARDED.index("list<Identifier> identifiers")
    authors_i = FORWARDED.index("list<Author> authors")
    contrib_i = NOT_FORWARDED.index("list<Author> contributors")

    _line_to_sat("Identifier", center_x + BOX_W, _field_y(pad, True, idents_i))
    _line_to_sat("Author", center_x + BOX_W, _field_y(pad, True, authors_i))
    _line_to_sat("Author", center_x + BOX_W, _field_y(pad + fwd_h + gap_between, True, contrib_i), dashed=True)

    parts += lines

    parts.append(fwd_svg)
    parts.append(dropped_svg)

    for (title, fields), (_, sy0, hh) in zip(SATELLITES, sat_positions):
        box_svg, _ = _render_box(right_x, sy0, BOX_W, title, fields, ACCENT, TINT)
        parts.append(box_svg)

    footnote_y = pad + max(center_total_h, sat_total) + 46
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
