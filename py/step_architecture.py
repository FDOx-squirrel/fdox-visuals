"""S4 — fdo-squirrel architecture diagram.

Redraws FDOx-squirrel/fdo-squirrel's `architecture.mermaid` in the
fdox-visuals house style, and brings it up to date with the actual
current `main.py` pipeline (see PRIMER.md A1 for the three stages the
original diagram is missing: schema validation, the Mermaid/JPG overview
step, and bundle finalisation).

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
PROCESS_BOX_W = 480
ROW_H = 108
GAP = 26
PANEL_PAD = 40
PANEL_GAP = 140

# --- process column (7 rows, top to bottom, matches main.py's real order) ---
PROCESS_ROWS = [
    "Metadata ingest",
    "Schema validation",
    "Crosswalk & Mapping Rules",
    "Role classification\nZIP \u2192 Distribution",
    "Provenance tracking",
    "Overview diagram\nMermaid \u2192 JPG",
    "Bundle finalisation",
]

# --- input column: (label, target process row index, own row slot) ---
INPUT_BOXES = [
    ("MD.cff\nDescriptive Metadata", 0),
    ("CITATION.cff\nCitation Metadata", 0),
    ("Data / Software / Models", 3),
]

# --- output column: (label, source process row index) ---
OUTPUT_BOXES = [
    ("fdo-metadata.ttl\nDCAT + FDO + CIDOC CRM /\nCRMdig + GeoSPARQL", 2.5),
    ("rdf_modelling_report\nJSON / HTML", 4),
    ("fdo_overview\nMermaid + JPG", 5),
    ("<slug>-fdo-bundle.zip\nself-contained, republishable", 6),
]

EDGES_TO_PROCESS = [
    (0, 0), (1, 0),  # MD.cff, CITATION.cff -> Metadata ingest
    (2, 3),          # Data/Software/Models -> Role classification
]
EDGES_PROCESS_CHAIN = [(0, 1), (1, 2)]  # ingest -> validation -> crosswalk
EDGES_TO_PROVENANCE = [(2, 4), (3, 4)]  # crosswalk & roles -> provenance
EDGES_PROCESS_TAIL = [(4, 5), (5, 6)]   # provenance -> overview -> bundle
EDGES_TO_OUTPUT = [(2, 0), (3, 0), (4, 1), (5, 2), (6, 3)]


def row_y(i: float) -> float:
    return PANEL_PAD + 70 + i * (ROW_H + GAP)


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


def _build_svg() -> tuple[str, float, float]:
    n_process = len(PROCESS_ROWS)
    process_top = row_y(0) - ROW_H / 2
    process_bottom = row_y(n_process - 1) + ROW_H / 2
    panel_h = process_bottom - process_top + 2 * PANEL_PAD

    input_x = PANEL_PAD
    process_x = input_x + BOX_W + PANEL_GAP
    output_x = process_x + PROCESS_BOX_W + PANEL_GAP

    W = output_x + BOX_W + PANEL_PAD
    H = panel_h + 140  # + panel title band

    panel_top = 90

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    parts.append(font_face_css())
    parts.append(
        '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
    )

    def panel(x, title, accent, tint):
        parts.append(
            f'<rect x="{x-PANEL_PAD}" y="{panel_top}" width="{BOX_W+2*PANEL_PAD if x!=process_x else PROCESS_BOX_W+2*PANEL_PAD}" '
            f'height="{panel_h}" rx="22" fill="{tint}" stroke="{accent}" stroke-width="3"/>'
        )
        panel_w = (PROCESS_BOX_W if x == process_x else BOX_W) + 2 * PANEL_PAD
        parts.append(
            f'<text x="{x-PANEL_PAD+panel_w/2}" y="{panel_top+48}" text-anchor="middle" '
            f'font-family="Fira Sans" font-weight="700" font-size="34" fill="{accent}">{title}</text>'
        )

    panel(input_x, "FDO ZIP Package", INPUT_ACCENT, INPUT_TINT)
    panel(process_x, "fdo-squirrel", PROCESS_ACCENT, PROCESS_TINT)
    panel(output_x, "Derived Outputs", OUTPUT_ACCENT, OUTPUT_TINT)

    yoff = panel_top + 40

    # process boxes
    for i, label in enumerate(PROCESS_ROWS):
        y = yoff + row_y(i) - ROW_H / 2
        parts.append(_box(process_x, y, PROCESS_BOX_W, ROW_H, "white", PROCESS_ACCENT, _wrap_lines(label)))

    # input boxes
    for i, (label, target) in enumerate(INPUT_BOXES):
        y = yoff + row_y(target if target != 3 else 3) - ROW_H / 2
        if i == 1:  # CITATION.cff sits just below MD.cff, both -> ingest
            y += ROW_H + GAP
        parts.append(_box(input_x, y, BOX_W, ROW_H, "white", INPUT_ACCENT, _wrap_lines(label)))

    # output boxes
    for label, source in OUTPUT_BOXES:
        y = yoff + row_y(source) - ROW_H / 2
        parts.append(_box(output_x, y, BOX_W, ROW_H, "white", OUTPUT_ACCENT, _wrap_lines(label)))

    # edges: input -> process
    md_y = yoff + row_y(0) - ROW_H / 2 + ROW_H / 2
    cff_y = md_y + ROW_H + GAP
    data_y = yoff + row_y(3)
    ingest_left = process_x
    ingest_y = yoff + row_y(0)
    roles_y = yoff + row_y(3)
    parts.append(_arrow(input_x + BOX_W, md_y, ingest_left, ingest_y - 14))
    parts.append(_arrow(input_x + BOX_W, cff_y, ingest_left, ingest_y + 14))
    parts.append(_arrow(input_x + BOX_W, data_y, ingest_left, roles_y))

    # process chain (ingest -> validation -> crosswalk), and provenance/tail
    chain = EDGES_PROCESS_CHAIN + EDGES_TO_PROVENANCE + EDGES_PROCESS_TAIL
    cx = process_x + PROCESS_BOX_W / 2
    for a, b in chain:
        ya = yoff + row_y(a) + ROW_H / 2
        yb = yoff + row_y(b) - ROW_H / 2
        xa = cx - 40 if (a, b) in EDGES_TO_PROVENANCE else cx
        xb = cx + 40 if (a, b) in EDGES_TO_PROVENANCE else cx
        parts.append(_arrow(xa, ya, xb, yb))

    # process -> output
    for src, out_i in EDGES_TO_OUTPUT:
        y_src = yoff + row_y(src)
        y_out = yoff + row_y(OUTPUT_BOXES[out_i][1])
        parts.append(_arrow(process_x + PROCESS_BOX_W, y_src, output_x, y_out))

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
