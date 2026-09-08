"""S4 — fdo-squirrel architecture diagram.

Redraws FDOx-squirrel/fdo-squirrel's `architecture.mermaid` in the
fdox-visuals house style, and brings it up to date with the actual
current `main.py` pipeline (see PRIMER.md A1 for the three stages the
original diagram is missing: schema validation, the Mermaid/JPG overview
step, and bundle finalisation).

"Role classification" and "Crosswalk & Mapping Rules" are drawn side by
side, not stacked, because that's what they actually are in main.py:
two independent branches that both start from an input (Role
classification straight from the ZIP's Data/Software/Models, Crosswalk
from the schema-validated MD.cff) and both feed the same two downstream
things (fdo-metadata.ttl, Provenance tracking). A single-file column
forces an order onto two things that don't have one, and worse, forces
whichever one *isn't* adjacent to Provenance to route straight through
the other box to reach it (found and fixed 2026-09-08 — see PRIMER.md A1
Befund 10/12).

Produces:
  img/fdox-fdo-squirrel-architecture.svg / .png (transparent)

Runnable standalone: `python py/step_architecture.py`
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

# Panel accents reuse the four-step-pattern family: input = Step-1 blue,
# process = Step-2 teal, output = Step-4 violet (skipping Step-3's amber,
# which is reserved for "linking to community hubs" elsewhere).
INPUT_ACCENT, INPUT_TINT = "#004473", "#E6ECF1"
PROCESS_ACCENT, PROCESS_TINT = "#0E9488", "#E6F6F4"
OUTPUT_ACCENT, OUTPUT_TINT = "#8034C9", "#F3E9FC"

BOX_W = 460
PROCESS_BOX_W = 760
ROW_H = 108
GAP = 26
FORK_GAP = 30
PANEL_PAD = 40
PANEL_GAP = 140
PANEL_TOP = 90     # y of every panel rect's top edge
TOP_INSET = 150    # panel_top -> first row's vertical centre (clears the title text)
BOTTOM_PAD = 40    # last row's bottom -> panel bottom

# --- process rows, top to bottom. Row 2 is a fork: two boxes side by
# side instead of one, see module docstring. ---
ROW_INGEST, ROW_VALIDATE, ROW_FORK, ROW_PROVENANCE, ROW_OVERVIEW, ROW_BUNDLE = range(6)

SINGLE_ROWS = {
    ROW_INGEST: "Metadata ingest",
    ROW_VALIDATE: "Schema validation",
    ROW_PROVENANCE: "Provenance tracking",
    ROW_OVERVIEW: "Overview diagram\nMermaid \u2192 JPG",
    ROW_BUNDLE: "Bundle finalisation",
}
FORK_LEFT = "Role classification\nZIP \u2192 Distribution"   # fed directly by Data/Software/Models
FORK_RIGHT = "Crosswalk &\nMapping Rules"                    # fed by Schema validation

N_ROWS = 6

# --- input column: (label, target process row) ---
INPUT_BOXES = [
    ("MD.cff\nDescriptive Metadata", ROW_INGEST),
    ("CITATION.cff\nCitation Metadata", ROW_INGEST),
    ("Data / Software / Models", ROW_FORK),
]

# --- output column: (label, source process row) ---
OUTPUT_BOXES = [
    ("fdo-metadata.ttl\nDCAT + FDO + CIDOC CRM /\nCRMdig + GeoSPARQL", ROW_FORK),
    ("rdf_modelling_report\nJSON / HTML", ROW_PROVENANCE),
    ("fdo_overview\nMermaid + JPG", ROW_OVERVIEW),
    ("<slug>-fdo-bundle.zip\nself-contained, republishable", ROW_BUNDLE),
]


def row_y(i: float) -> float:
    """Absolute y-centre of process row i."""
    return PANEL_TOP + TOP_INSET + i * (ROW_H + GAP)


def _wrap_lines(text: str) -> list[str]:
    return text.split("\n")


def _box(x: float, y: float, w: float, h: float, fill: str, stroke: str, lines: list[str]) -> str:
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3.5"/>'
    n = len(lines)
    line_h = 34
    start_y = y + h / 2 - (n - 1) * line_h / 2 + 10
    for i, line in enumerate(lines):
        weight = 700 if i == 0 else 400
        out += (
            f'<text x="{x+w/2}" y="{start_y+i*line_h}" text-anchor="middle" font-family="Fira Sans" '
            f'font-weight="{weight}" font-size="27" fill="{INK}">{esc(line)}</text>'
        )
    return out


def _arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="3" '
        f'marker-end="url(#arrow)"/>'
    )


def _elbow_arrow(points: list[tuple[float, float]]) -> str:
    """Orthogonal multi-segment connector, for a route that would
    otherwise cut diagonally through an unrelated box in between.
    """
    pts = " ".join(f"{x},{y}" for x, y in points)
    return (
        f'<polyline points="{pts}" fill="none" stroke="{MUTED}" stroke-width="3" '
        f'stroke-linejoin="round" marker-end="url(#arrow)"/>'
    )


def _build_svg() -> tuple[str, float, float]:
    last_bottom = row_y(N_ROWS - 1) + ROW_H / 2
    panel_h = (last_bottom - PANEL_TOP) + BOTTOM_PAD

    input_x = PANEL_PAD
    process_x = input_x + BOX_W + PANEL_GAP
    output_x = process_x + PROCESS_BOX_W + PANEL_GAP

    W = output_x + BOX_W + PANEL_PAD
    H = PANEL_TOP + panel_h + PANEL_PAD

    fork_w = (PROCESS_BOX_W - FORK_GAP) / 2
    fork_left_x = process_x
    fork_right_x = process_x + fork_w + FORK_GAP
    cx = process_x + PROCESS_BOX_W / 2  # centre of the full-width rows

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    parts.append(font_face_css())
    parts.append(
        '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
    )

    def panel(x, title, accent, tint):
        panel_w = (PROCESS_BOX_W if x == process_x else BOX_W) + 2 * PANEL_PAD
        parts.append(
            f'<rect x="{x-PANEL_PAD}" y="{PANEL_TOP}" width="{panel_w}" '
            f'height="{panel_h}" rx="22" fill="{tint}" stroke="{accent}" stroke-width="3"/>'
        )
        parts.append(
            f'<text x="{x-PANEL_PAD+panel_w/2}" y="{PANEL_TOP+48}" text-anchor="middle" '
            f'font-family="Fira Sans" font-weight="700" font-size="34" fill="{accent}">{title}</text>'
        )

    panel(input_x, "FDO ZIP Package", INPUT_ACCENT, INPUT_TINT)
    panel(process_x, "fdo-squirrel", PROCESS_ACCENT, PROCESS_TINT)
    panel(output_x, "Derived Outputs", OUTPUT_ACCENT, OUTPUT_TINT)

    # single-width process boxes
    for i, label in SINGLE_ROWS.items():
        y = row_y(i) - ROW_H / 2
        parts.append(_box(process_x, y, PROCESS_BOX_W, ROW_H, "white", PROCESS_ACCENT, _wrap_lines(label)))

    # fork boxes
    fork_y = row_y(ROW_FORK) - ROW_H / 2
    parts.append(_box(fork_left_x, fork_y, fork_w, ROW_H, "white", PROCESS_ACCENT, _wrap_lines(FORK_LEFT)))
    parts.append(_box(fork_right_x, fork_y, fork_w, ROW_H, "white", PROCESS_ACCENT, _wrap_lines(FORK_RIGHT)))

    # input boxes
    for i, (label, target) in enumerate(INPUT_BOXES):
        y = row_y(target) - ROW_H / 2
        if i == 1:  # CITATION.cff sits just below MD.cff, both -> ingest
            y += ROW_H + GAP
        parts.append(_box(input_x, y, BOX_W, ROW_H, "white", INPUT_ACCENT, _wrap_lines(label)))

    # output boxes
    for label, source in OUTPUT_BOXES:
        y = row_y(source) - ROW_H / 2
        parts.append(_box(output_x, y, BOX_W, ROW_H, "white", OUTPUT_ACCENT, _wrap_lines(label)))

    # --- edges: input -> process ---
    md_y = row_y(ROW_INGEST)
    cff_y = md_y + ROW_H + GAP
    ingest_y = row_y(ROW_INGEST)
    parts.append(_arrow(input_x + BOX_W, md_y, process_x, ingest_y - 14))
    parts.append(_arrow(input_x + BOX_W, cff_y, process_x, ingest_y + 14))
    # Data/Software/Models -> Role classification (fork LEFT box, so this
    # is a direct, unobstructed horizontal line, same as before)
    parts.append(_arrow(input_x + BOX_W, row_y(ROW_FORK), fork_left_x, row_y(ROW_FORK)))

    # --- ingest -> validation -> Crosswalk (fork RIGHT box) ---
    parts.append(_arrow(cx, row_y(ROW_INGEST) + ROW_H / 2, cx, row_y(ROW_VALIDATE) - ROW_H / 2))
    crosswalk_cx = fork_right_x + fork_w / 2
    parts.append(_arrow(crosswalk_cx, row_y(ROW_VALIDATE) + ROW_H / 2, crosswalk_cx, fork_y))

    # --- fork -> Provenance: both halves drop straight down, landing at
    # two different x-offsets on Provenance's top edge - a clean two-
    # pronged convergence, not a diagonal through either box. ---
    roleclass_cx = fork_left_x + fork_w / 2
    prov_top = row_y(ROW_PROVENANCE) - ROW_H / 2
    fork_bottom = fork_y + ROW_H
    parts.append(_arrow(roleclass_cx, fork_bottom, cx - 60, prov_top))
    parts.append(_arrow(crosswalk_cx, fork_bottom, cx + 60, prov_top))

    # --- fork -> fdo-metadata.ttl: Crosswalk (right half) exits directly
    # right. Role classification (left half) can't do the same without
    # crossing Crosswalk, so it's routed up and over, through the empty
    # gap between Schema validation and the fork row - open space, not
    # through any box. ---
    ttl_y = row_y(OUTPUT_BOXES[0][1])
    parts.append(_arrow(fork_right_x + fork_w, row_y(ROW_FORK) - 14, output_x, ttl_y - 14))
    over_y = row_y(ROW_VALIDATE) + ROW_H / 2 + GAP / 2
    parts.append(_elbow_arrow([
        (roleclass_cx, fork_y),
        (roleclass_cx, over_y),
        (output_x - 60, over_y),
        (output_x - 60, ttl_y + 14),
        (output_x, ttl_y + 14),
    ]))

    # --- process tail (provenance -> overview -> bundle), full width ---
    for a, b in [(ROW_PROVENANCE, ROW_OVERVIEW), (ROW_OVERVIEW, ROW_BUNDLE)]:
        ya = row_y(a) + ROW_H / 2
        yb = row_y(b) - ROW_H / 2
        parts.append(_arrow(cx, ya, cx, yb))

    # --- provenance/overview/bundle -> their outputs ---
    for src, y_out in [
        (ROW_PROVENANCE, row_y(OUTPUT_BOXES[1][1])),
        (ROW_OVERVIEW, row_y(OUTPUT_BOXES[2][1])),
        (ROW_BUNDLE, row_y(OUTPUT_BOXES[3][1])),
    ]:
        parts.append(_arrow(process_x + PROCESS_BOX_W, row_y(src), output_x, y_out))

    parts.append("</svg>")
    return "\n".join(parts), W, H


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []

    svg_text, w, h = _build_svg()
    svg_path = IMG_DIR / "fdox-fdo-squirrel-architecture.svg"
    svg_path.write_text(svg_text, encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    render_svg_to_png(svg_path, png_path, int(w * 1.8), int(h * 1.8))
    final_w, final_h = trim_transparent_border(png_path, margin_px=10)
    log.append(
        f"wrote {svg_path.relative_to(IMG_DIR.parent)} + .png "
        f"({final_w}x{final_h}, transparent, <=10px border)"
    )
    return log


if __name__ == "__main__":
    for line in run():
        print(line)
