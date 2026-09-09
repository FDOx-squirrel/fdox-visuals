"""S3 — FAIR Digital Object meta-graphic.

Recolours the classic "Data / Metadata / PID" nested-circle diagram into
the FDOx house palette. Composition (title left, nested circles right,
three leader lines) matches the original reference image; colour and
typography follow this repo's conventions instead.

Produces:
  img/fdox-fair-digital-object-meta-graphic.svg / .png (transparent)
  img/fdox-fdo-sphere.svg / .png (transparent) -- the nested-circle glyph
    alone, no title/leader-lines/labels, for use as a standalone FDO symbol
    (Flo, 2026-09-10: "die FDOx Kugel... als alleinige Symbolgrafik")

Runnable standalone: `python py/step_fdo_meta.py`
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals_utils import (  # noqa: E402
    FDO_ACCENT,
    IMG_DIR,
    INK,
    MUTED,
    ensure_dirs,
    font_face_css,
    render_svg_to_png,
    trim_transparent_border,
)


def _shade(hex_color: str, factor: float) -> str:
    """Darken (factor<1) or lighten-toward-white (factor>1, capped) a hex colour."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r, g, b = (min(255, max(0, int(c * factor))) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def _tint(hex_color: str, white_ratio: float) -> str:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    mix = lambda c: int(c * (1 - white_ratio) + 255 * white_ratio)
    return f"#{mix(r):02X}{mix(g):02X}{mix(b):02X}"


ACCENT = FDO_ACCENT              # #004473 — the original FAIR Digital Object blue
ACCENT_STROKE = _shade(ACCENT, 0.7)
RING_FILL = _tint(ACCENT, 0.65)

W, H = 1600, 1000
CX, CY = 1080, 430
OUTER_R = 320
INNER_R = 175

# See step_pattern.py's OVERSAMPLE comment: kept modest so the trimmed
# content stays well under Google Slides' 25-megapixel insert limit.
OVERSAMPLE = 2.5


def _build_svg() -> str:
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    p.append(font_face_css())

    p.append(f'<circle cx="{CX}" cy="{CY}" r="{OUTER_R}" fill="{RING_FILL}" stroke="{ACCENT}" stroke-width="6"/>')
    p.append(f'<circle cx="{CX}" cy="{CY}" r="{INNER_R}" fill="{ACCENT}" stroke="{ACCENT_STROKE}" stroke-width="6"/>')

    p.append(
        f'<text x="{CX}" y="{CY-14}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="70" fill="white" letter-spacing="4">I0I0</text>'
    )
    p.append(
        f'<text x="{CX}" y="{CY+70}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="70" fill="white" letter-spacing="4">0I0I</text>'
    )

    p.append(
        f'<text x="90" y="{CY+22}" text-anchor="start" font-family="Fira Sans" '
        f'font-weight="700" font-size="64" fill="{INK}">FAIR Digital Object</text>'
    )

    labels = [
        {"text": "Data", "y": 610, "dir": (-0.447, 0.894), "radius": 90},          # inside the inner disk
        {"text": "Metadata", "y": 700, "dir": (-0.678, 0.735), "radius": 250},     # inside the ring band
        {"text": "PID", "y": 790, "dir": (-0.6, 0.8), "radius": OUTER_R},          # exactly on the outer edge
    ]
    label_x, elbow_x, h_start_x = 210, 560, 420
    for lbl in labels:
        tx = CX + lbl["dir"][0] * lbl["radius"]
        ty = CY + lbl["dir"][1] * lbl["radius"]
        y = lbl["y"]
        p.append(
            f'<text x="{label_x}" y="{y}" text-anchor="start" font-family="Fira Sans" '
            f'font-weight="400" font-size="44" fill="{INK}">{lbl["text"]}</text>'
        )
        p.append(
            f'<polyline points="{h_start_x},{y-14} {elbow_x},{y-14} {tx:.1f},{ty:.1f}" '
            f'fill="none" stroke="{MUTED}" stroke-width="3.5"/>'
        )

    p.append("</svg>")
    return "\n".join(p)


def _build_sphere_svg() -> str:
    """Just the nested-circle glyph -- no title, no Data/Metadata/PID
    leader lines -- reusing the exact same geometry/colours as
    `_build_svg()`'s circles (A3: one source, not a second set of
    radii/colours hand-copied alongside it).
    """
    pad = 20
    size = OUTER_R * 2 + pad * 2
    c = OUTER_R + pad
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">']
    p.append(font_face_css())
    p.append(f'<circle cx="{c}" cy="{c}" r="{OUTER_R}" fill="{RING_FILL}" stroke="{ACCENT}" stroke-width="6"/>')
    p.append(f'<circle cx="{c}" cy="{c}" r="{INNER_R}" fill="{ACCENT}" stroke="{ACCENT_STROKE}" stroke-width="6"/>')
    p.append(
        f'<text x="{c}" y="{c-14}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="70" fill="white" letter-spacing="4">I0I0</text>'
    )
    p.append(
        f'<text x="{c}" y="{c+70}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="70" fill="white" letter-spacing="4">0I0I</text>'
    )
    p.append("</svg>")
    return "\n".join(p), size


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []

    svg_text = _build_svg()
    svg_path = IMG_DIR / "fdox-fair-digital-object-meta-graphic.svg"
    svg_path.write_text(svg_text, encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    render_svg_to_png(svg_path, png_path, int(W * OVERSAMPLE), int(H * OVERSAMPLE))
    final_w, final_h = trim_transparent_border(png_path, margin_px=10)
    log.append(
        f"wrote {svg_path.relative_to(IMG_DIR.parent)} + .png "
        f"({final_w}x{final_h}, transparent, <=10px border, accent {ACCENT})"
    )

    sphere_svg, sphere_size = _build_sphere_svg()
    svg_path = IMG_DIR / "fdox-fdo-sphere.svg"
    svg_path.write_text(sphere_svg, encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    render_svg_to_png(svg_path, png_path, int(sphere_size * OVERSAMPLE), int(sphere_size * OVERSAMPLE))
    final_w, final_h = trim_transparent_border(png_path, margin_px=10)
    log.append(
        f"wrote {svg_path.relative_to(IMG_DIR.parent)} + .png "
        f"({final_w}x{final_h}, transparent, <=10px border, accent {ACCENT})"
    )

    return log


if __name__ == "__main__":
    for line in run():
        print(line)
