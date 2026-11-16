"""S16 — "One bundle, three views".

One finished FDO bundle (the ZIP fdo-squirrel writes) is described three
ways, each generated from the same inputs:

  * fdo-metadata.ttl         the lossless RDF description (authoritative)
  * ro-crate-metadata.json   RO-Crate 1.2 with the FDOx profile, the
                             "Webby FDO" view (fdo-squirrel v1.1.0, S22)
  * fdo-landing-page.html    FAIR Signposting links for static hosting
                             (fdo-squirrel v1.1.0, S24)

Produces:
  img/schemas/fdox-bundle-three-views.svg / .png (transparent)

The RDF logo (card 1) and the RO-Crate logo (card 2) are used if
img/source/rdf-logo.svg|png and img/source/ro-crate-logo.svg|png exist (added
by hand, see PRIMER.md S16); a missing one is replaced by a text pill. Runnable standalone:
`python py/step_bundle_views.py`
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals_utils import (  # noqa: E402
    BG,
    FDO_ACCENT,
    FDO_TINT,
    IMG_DIR,
    INK,
    MUTED,
    STEPS,
    arrow_line,
    arrow_marker,
    ensure_dirs,
    esc,
    font_face_css,
    img_path,
    render_svg_to_png,
    LOGOS,
    logo,
    logo_credits,
    logo_path,
    trim_transparent_border,
)

TTL_ACCENT, TTL_TINT = STEPS[3]["color"], STEPS[3]["tint"]
CRATE_ACCENT = FDO_ACCENT
SIGNPOST_ACCENT, SIGNPOST_TINT = STEPS[1]["color"], STEPS[1]["tint"]

BOX_W = 460
CARD_W = 900
CARD_H = 200
CARD_GAP = 40
PANEL_PAD = 40
PANEL_GAP = 140
PANEL_TOP = 90
TOP_INSET = 90      # panel top -> first card top (clears the title)
BOTTOM_PAD = 40
CREDIT_H = 34       # extra room below the panels for the logo credit line

# (accent, tint, pill text, file name, line 2, line 3)
CARDS = [
    (TTL_ACCENT, TTL_TINT, "RDF", "fdo-metadata.ttl",
     "Lossless RDF description, authoritative",
     "DCAT · FDO · CIDOC CRM / CRMdig · GeoSPARQL"),
    (CRATE_ACCENT, FDO_TINT, "RO-Crate", "ro-crate-metadata.json",
     "RO-Crate 1.2 with the FDOx profile",
     "a generated view: the “Webby FDO”"),
    (SIGNPOST_ACCENT, SIGNPOST_TINT, "Signposting", "fdo-landing-page.html",
     "FAIR Signposting for static hosting",
     "cite-as · describedby · item · license · linkset"),
]

# which logo (key in visuals_utils.LOGOS) belongs on which card; None = text pill
LOGO_KEYS = ["rdf", "ro-crate", None]

BUNDLE_LINES = [
    ("<slug>-fdo-bundle.zip", 700, 30),
    ("self-contained, republishable", 400, 26),
    (None, 0, 0),
    ("data, models, viewer", 400, 26),
    ("MD.cff · CITATION.cff", 400, 26),
    ("FDOx.yaml · reports · diagrams", 400, 26),
]


def _text(x, y, s, size, weight, fill, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Fira Sans" '
        f'font-weight="{weight}" font-size="{size}" fill="{fill}">{esc(s)}</text>'
    )


def _build_svg() -> tuple[str, float, float]:
    n = len(CARDS)
    cards_h = n * CARD_H + (n - 1) * CARD_GAP
    panel_h = TOP_INSET + cards_h + BOTTOM_PAD
    left_x = PANEL_PAD
    right_x = left_x + BOX_W + 2 * PANEL_PAD + PANEL_GAP
    left_w = BOX_W + 2 * PANEL_PAD
    right_w = CARD_W + 2 * PANEL_PAD
    W = right_x + right_w + PANEL_PAD
    credits = logo_credits()
    has_logo = bool(credits)
    H = PANEL_TOP + panel_h + PANEL_PAD + (CREDIT_H if has_logo else 0)

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        font_face_css(),
        arrow_marker(),
    ]

    def panel(x, w, title, accent, tint):
        p.append(
            f'<rect x="{x}" y="{PANEL_TOP}" width="{w}" height="{panel_h}" rx="22" '
            f'fill="{tint}" stroke="{accent}" stroke-width="3"/>'
        )
        p.append(_text(x + w / 2, PANEL_TOP + 52, title, 34, 700, accent, "middle"))

    panel(left_x, left_w, "One bundle", FDO_ACCENT, FDO_TINT)
    panel(right_x, right_w, "Three views of the same FDO", MUTED, BG)

    # the bundle: one tall box
    bx, by = left_x + PANEL_PAD, PANEL_TOP + TOP_INSET
    bh = cards_h
    p.append(
        f'<rect x="{bx}" y="{by}" width="{BOX_W}" height="{bh}" rx="14" '
        f'fill="white" stroke="{FDO_ACCENT}" stroke-width="3.5"/>'
    )
    block_h = sum(40 if t is None else size + 22 for t, _, size in BUNDLE_LINES) - 22
    y = by + (bh - block_h) / 2 + BUNDLE_LINES[0][2] * 0.8
    for text, weight, size in BUNDLE_LINES:
        if text is None:
            y += 40
            continue
        p.append(_text(bx + BOX_W / 2, y, text, size, weight, INK, "middle"))
        y += size + 22

    # the three cards, with an arrow from the bundle to each
    for i, (accent, tint, pill, fname, line2, line3) in enumerate(CARDS):
        cx = right_x + PANEL_PAD
        cy = PANEL_TOP + TOP_INSET + i * (CARD_H + CARD_GAP)
        mid = cy + CARD_H / 2
        p.append(
            f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" rx="14" '
            f'fill="white" stroke="{accent}" stroke-width="3.5"/>'
        )
        # left zone: logo (RO-Crate card, if available) or a text pill
        zone_x, zone_w = cx + 30, 210
        card_logo = logo(LOGO_KEYS[i], zone_x, cy + 12, zone_w, CARD_H - 24) if LOGO_KEYS[i] else ""
        if card_logo:
            p.append(card_logo)
        else:
            p.append(
                f'<rect x="{zone_x}" y="{mid - 40}" width="{zone_w}" height="80" rx="40" fill="{accent}"/>'
            )
            p.append(_text(zone_x + zone_w / 2, mid + 11, pill, 31, 700, "white", "middle"))
        tx = cx + 280
        p.append(_text(tx, mid - 30, fname, 34, 700, INK))
        p.append(_text(tx, mid + 14, line2, 27, 400, INK))
        p.append(_text(tx, mid + 54, line3, 24, 400, MUTED))
        p.append(arrow_line(bx + BOX_W, mid, cx, mid))

    if has_logo:
        # CC BY 4.0 asks for attribution: say it in the picture itself
        p.append(
            _text(right_x + right_w, PANEL_TOP + panel_h + 30, credits, 18, 400, MUTED, "end")
        )

    p.append("</svg>")
    return "\n".join(p), W, H


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []
    svg_text, w, h = _build_svg()
    svg_path = img_path("fdox-bundle-three-views.svg")
    svg_path.write_text(svg_text, encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    render_svg_to_png(svg_path, png_path, int(w * 1.8), int(h * 1.8))
    final_w, final_h = trim_transparent_border(png_path, margin_px=10)
    log.append(
        f"wrote {svg_path.relative_to(IMG_DIR.parent)} + .png "
        f"({final_w}x{final_h}, transparent, <=10px border)"
    )
    for key in LOGOS:
        if logo_path(key) is None:
            log.append(
                f"note: img/source/{LOGOS[key]['stem']}.svg/.png not found, "
                "text pill instead of that logo"
            )
    return log


if __name__ == "__main__":
    for line in run():
        print(line)
