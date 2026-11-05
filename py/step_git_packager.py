"""S11 -- fdo-git-packager: how a pinned GitHub commit becomes an FDOx.

`fdo-git-packager` (FDOx-squirrel, MIT) exists today only as an *S1 skeleton*:
five step stubs (fetch, inspect, mdcff, bundle, build_fdo) that all answer
"nothing to do". Its PRIMER fixes the design -- a mandatory commit SHA, the
working tree without .git packaged flat into one ZIP, fdo-squirrel as the
engine -- and these graphics follow that design, not an invented one. The
ArcheoFOSS 2026 abstract adds CoMET-RS (metadata extraction); that wiring is
not in the skeleton yet, so it is drawn as planned.

Every graphic therefore says *planned* in the picture: dashed outlines mean
"not implemented yet", solid ones "exists today".

The example is a real repository, as in chublets-visuals' S18: the SPARQLing
Unicorn QGIS plugin (github.com/sparqlunicorn/sparqlunicornGoesGIS), read on
2026-11-05 at tag v0.17.4 = commit ba8af4cd0e3f95b862bd7562f0315b058124ab34
(master HEAD a519707 is 7 commits later). Facts used, all checked against the
repository or CoMET-RS's real output (chublets-software/comet-metadata-
extraction, examples/unicorn, tag v0.4.3-chublets.2):
  tags v0.17.2 736ec92, v0.17.3 4a5ab67, v0.17.4 ba8af4c (2025-12-17), in that
  order; master HEAD a519707 (2026-03-11); 690 files in the working tree, none
  of them in a directory the packager strips; CITATION.cff says version 0.17.2
  with 15 DOI entries; CoMET-RS flags "version 0.17.2 differs from release tag
  0.17.4".

Produces (all new, none replaces an existing graphic):
  img/fdox-git-packager-four-steps.svg/.png       banner, transparent (A4)
  img/fdox-git-packager-step-<n>-<slug>.svg/.png  four badges, transparent
  img/fdox-talk-git-packager-step<n>-<slug>.svg/.png  four 7:4 slides, white (S8)
  img/fdox-talk-git-packager-actions.svg/.png     GitHub Actions swimlane, white

One brand colour on purpose (S7 precedent), so none of this is mistaken for the
four-colour FDOx pattern of S2, whose steps 1-4 mean something else.

Runnable standalone: `python py/step_git_packager.py`
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
    img_path,
    INK,
    MUTED,
    STEPS,
    arrow_line,
    arrow_marker,
    ensure_dirs,
    esc,
    font_face_css,
    render_svg_to_png,
    trim_transparent_border,
    wrap_text,
)

TINT = STEPS[0]["tint"]  # #E6ECF1, the light tint that belongs to FDO_ACCENT
CODE_BG = "#F5F7FA"

REPO_URL = "https://github.com/sparqlunicorn/sparqlunicornGoesGIS"
PIN_SHA = "ba8af4cd0e3f95b862bd7562f0315b058124ab34"
PIN_SHA7 = PIN_SHA[:7]
FOOTER = "fdo-git-packager · S1 skeleton, no step implemented yet"

# --------------------------------------------------------------- the steps --

# Four steps, mapped onto the five skeleton steps: Package = mdcff + bundle.
BANNER_STEPS = [
    {"num": "1", "slug": "pin", "title": ["Pin", "the Commit"],
     "desc": "fetch: --repo + --ref, a commit SHA and never a branch HEAD"},
    {"num": "2", "slug": "inspect", "title": ["Inspect", "& Extract"],
     "desc": "inspect: the repository’s own CITATION.cff, plus CoMET-RS"},
    {"num": "3", "slug": "package", "title": ["Package", "as fdo:SoftwareFDO"],
     "desc": "mdcff + bundle: MD.cff and one ZIP, schema-validated"},
    {"num": "4", "slug": "build", "title": ["Build", "& Publish"],
     "desc": "build_fdo: fdo-squirrel; then Zenodo DOI and registry"},
]

# ------------------------------------------------------------------- icons --


def _icon_pin(color: str) -> str:
    """A release tag (price-tag shape): the thing that pins a snapshot."""
    sw = 6
    return (
        f'<polygon points="-58,-32 18,-32 60,0 18,32 -58,32" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linejoin="round"/>'
        f'<circle cx="-34" cy="0" r="9" fill="{color}"/>'
        f'<line x1="-10" y1="0" x2="24" y2="0" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
    )


def _icon_inspect(color: str) -> str:
    """A file with a folded corner and text lines."""
    sw = 6
    return (
        f'<path d="M -40,-58 L 14,-58 L 40,-32 L 40,58 L -40,58 Z" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linejoin="round"/>'
        f'<path d="M 14,-58 L 14,-32 L 40,-32" fill="none" stroke="{color}" stroke-width="{sw}" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
        + "".join(
            f'<line x1="-22" y1="{y}" x2="22" y2="{y}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
            for y in (-8, 12, 32)
        )
    )


def _icon_package(color: str) -> str:
    """An isometric box: the packaged object."""
    sw = 6
    return (
        f'<polygon points="0,-62 54,-31 54,31 0,62 -54,31 -54,-31" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linejoin="round"/>'
        f'<polyline points="-54,-31 0,0 54,-31" fill="none" stroke="{color}" stroke-width="{sw}" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
        f'<line x1="0" y1="0" x2="0" y2="62" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
    )


def _icon_build(color: str) -> str:
    """A database cylinder: the registry the FDO ends up in."""
    sw = 6
    return (
        f'<ellipse cx="0" cy="-42" rx="48" ry="16" fill="none" stroke="{color}" stroke-width="{sw}"/>'
        f'<line x1="-48" y1="-42" x2="-48" y2="42" stroke="{color}" stroke-width="{sw}"/>'
        f'<line x1="48" y1="-42" x2="48" y2="42" stroke="{color}" stroke-width="{sw}"/>'
        f'<path d="M -48,0 A 48,16 0 0 0 48,0" fill="none" stroke="{color}" stroke-width="{sw}"/>'
        f'<path d="M -48,42 A 48,16 0 0 0 48,42" fill="none" stroke="{color}" stroke-width="{sw}"/>'
    )


_ICONS = [_icon_pin, _icon_inspect, _icon_package, _icon_build]

# ------------------------------------------------------------------- badge --

BADGE_R = 150
TAG_SIZE = 132
TAG_OFFSET = 26


def _badge(cx: float, cy: float, idx: int) -> str:
    """Dashed circle = planned. The number tag stays solid so it reads."""
    tag_x = cx - BADGE_R - TAG_OFFSET
    tag_y = cy - BADGE_R - TAG_OFFSET
    out = (
        f'<circle cx="{cx}" cy="{cy}" r="{BADGE_R}" fill="{TINT}" stroke="{FDO_ACCENT}" '
        f'stroke-width="7" stroke-dasharray="26 16" stroke-linecap="round"/>'
    )
    out += f'<g transform="translate({cx},{cy})">{_ICONS[idx](FDO_ACCENT)}</g>'
    out += f'<rect x="{tag_x}" y="{tag_y}" width="{TAG_SIZE}" height="{TAG_SIZE}" rx="26" fill="{FDO_ACCENT}"/>'
    out += (
        f'<text x="{tag_x + TAG_SIZE/2}" y="{tag_y + TAG_SIZE/2 + 40}" text-anchor="middle" '
        f'font-family="Fira Sans" font-weight="700" font-size="104" fill="white">{BANNER_STEPS[idx]["num"]}</text>'
    )
    return out


def _build_badge_svg(idx: int) -> tuple[str, int]:
    pad = 15
    left = -(BADGE_R + TAG_OFFSET) - pad
    top = -(BADGE_R + TAG_OFFSET) - pad
    right = BADGE_R + pad
    bottom = BADGE_R + pad
    vb_w, vb_h = right - left, bottom - top
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{vb_w}" height="{vb_h}" '
        f'viewBox="{left} {top} {vb_w} {vb_h}">',
        font_face_css(),
        _badge(0, 0, idx),
        "</svg>",
    ]
    return "\n".join(p), vb_w


# ------------------------------------------------------------------ banner --

W = 3840
MARGIN_X = 260
COL_W = (W - 2 * MARGIN_X) / 4
CENTERS = [MARGIN_X + COL_W * (i + 0.5) for i in range(4)]

TOP_MARGIN = 130
BADGE_CY = TOP_MARGIN + BADGE_R + TAG_OFFSET
TITLE_Y0 = BADGE_CY + BADGE_R + 150
DESC_Y0 = TITLE_Y0 + 80 * 2 + 46
BOTTOM_MARGIN = 130

# Same ceiling reasoning as step_pattern.py: content in the low single-digit
# megapixels (PRIMER A4: ~2-6 MP), far below Google Slides' 25 MP insert limit.
OVERSAMPLE = 1.4
ICON_SCALE = 4


def _build_banner_svg(desc_lines: list[list[str]]) -> tuple[str, int]:
    max_lines = max(len(x) for x in desc_lines)
    content_bottom = DESC_Y0 + (max_lines - 1) * 54 + 34
    footer_y = content_bottom + 120
    h = int(footer_y + BOTTOM_MARGIN)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">']
    p.append(font_face_css())

    # dashed connectors with an open chevron -- the flow is planned, not built
    for i in range(3):
        x1 = CENTERS[i] + BADGE_R + 14
        x2 = CENTERS[i + 1] - BADGE_R - 14
        p.append(
            f'<line x1="{x1}" y1="{BADGE_CY}" x2="{x2 - 34}" y2="{BADGE_CY}" stroke="{FDO_ACCENT_SOFT}" '
            f'stroke-width="10" stroke-dasharray="30 20"/>'
        )
        p.append(
            f'<path d="M {x2-46},{BADGE_CY-26} L {x2-10},{BADGE_CY} L {x2-46},{BADGE_CY+26}" fill="none" '
            f'stroke="{FDO_ACCENT_LIGHT}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>'
        )

    for i, (cx, step) in enumerate(zip(CENTERS, BANNER_STEPS)):
        p.append(_badge(cx, BADGE_CY, i))
        for j, line in enumerate(step["title"]):
            p.append(
                f'<text x="{cx}" y="{TITLE_Y0 + j*80}" text-anchor="middle" font-family="Fira Sans" '
                f'font-weight="700" font-size="60" fill="{INK}">{esc(line)}</text>'
            )
        for j, line in enumerate(desc_lines[i]):
            p.append(
                f'<text x="{cx}" y="{DESC_Y0 + j*54}" text-anchor="middle" font-family="Fira Sans" '
                f'font-weight="400" font-size="38" fill="{MUTED}">{esc(line)}</text>'
            )

    p.append(
        f'<text x="{W/2}" y="{footer_y}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="40" fill="{FDO_ACCENT_LIGHT}">{esc(FOOTER)}</text>'
    )
    p.append("</svg>")
    return "\n".join(p), h


# ----------------------------------------------------------- slide helpers --

SW, SH = 1750, 1000
SLIDE_OVERSAMPLE = 2


def _t(x: float, y: float, s: str, size: float, weight: int = 400, fill: str = INK, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Fira Sans" font-weight="{weight}" '
        f'font-size="{size}" fill="{fill}">{esc(s)}</text>'
    )


def _slide_open() -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">',
        f'<rect x="0" y="0" width="{SW}" height="{SH}" fill="white"/>',
        font_face_css(),
        arrow_marker("arrow", MUTED),
    ]


def _heading(idx: int, title: str, sub: str) -> str:
    """Badge top-left (S8 position and scale) with the step's name next to it."""
    return (
        f'<g transform="translate(175,165) scale(0.56)">{_badge(0, 0, idx)}</g>'
        + _t(310, 150, title, 58, 700, FDO_ACCENT)
        + _t(310, 202, sub, 30, 400, MUTED)
    )


def _box(x: float, y: float, w: float, h: float, rows: list, dashed: bool = False, fill: str = "white",
         stroke: str = FDO_ACCENT, center: bool = False, pad: float = 22) -> str:
    """A rounded box with rows of text.

    A row is (text, size, weight, colour) or (text, size, weight, colour, indent);
    (None, gap_px) is a spacer. Line height is 1.38 x size.
    """
    dash = ' stroke-dasharray="14 9"' if dashed else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3.5"{dash}/>'

    def height_of(r):
        return r[1] if r[0] is None else r[1] * 1.38

    total = sum(height_of(r) for r in rows)
    cy = y + (h - total) / 2 if center else y + pad
    for r in rows:
        if r[0] is None:
            cy += r[1]
            continue
        text, size, weight, color = r[:4]
        indent = r[4] if len(r) > 4 else 0
        cy_base = cy + size * 1.0
        if center:
            out += _t(x + w / 2, cy_base, text, size, weight, color, "middle")
        else:
            out += _t(x + pad + indent, cy_base, text, size, weight, color)
        cy += size * 1.38
    return out


def _legend_and_note(note: str) -> str:
    ly = 880
    out = (
        f'<rect x="60" y="{ly}" width="62" height="34" rx="9" fill="white" stroke="{FDO_ACCENT}" stroke-width="3.5"/>'
        + _t(140, ly + 25, "exists today", 22, 400, INK)
        + f'<rect x="330" y="{ly}" width="62" height="34" rx="9" fill="white" stroke="{FDO_ACCENT}" '
        f'stroke-width="3.5" stroke-dasharray="14 9"/>'
        + _t(410, ly + 25, "planned – fdo-git-packager is an S1 skeleton, no step is implemented yet", 22, 400, INK)
    )
    out += _t(60, 950, note, 19, 400, MUTED)
    return out


def _slide_close(p: list[str]) -> str:
    p.append("</svg>")
    return "\n".join(p)


def _arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return arrow_line(x1, y1, x2, y2, width=3.5)


# ------------------------------------------------------------ slide 1: fetch --


def _build_slide_fetch() -> str:
    p = _slide_open()
    p.append(_heading(0, "fetch", "Pin the commit"))

    # the history of the real example repository, with the pin on v0.17.4
    ly = 400
    p.append(f'<line x1="110" y1="{ly}" x2="1640" y2="{ly}" stroke="{MUTED}" stroke-width="4"/>')
    nodes = [
        (260, "v0.17.2", "736ec92", False),
        (560, "v0.17.3", "4a5ab67", False),
        (860, "v0.17.4", f"{PIN_SHA7} · 2025-12-17", True),
        (1460, "master HEAD", "a519707 · 2026-03-11", False),
    ]
    for x, name, sub, pinned in nodes:
        if pinned:
            p.append(f'<circle cx="{x}" cy="{ly}" r="26" fill="{FDO_ACCENT}"/>')
        else:
            p.append(f'<circle cx="{x}" cy="{ly}" r="17" fill="white" stroke="{MUTED}" stroke-width="5"/>')
        p.append(_t(x, ly + 66, name, 26, 700, FDO_ACCENT if pinned else INK, "middle"))
        p.append(_t(x, ly + 96, sub, 20, 400, MUTED, "middle"))
    p.append(_t(1160, ly - 22, "7 commits later", 20, 400, MUTED, "middle"))
    p.append(_t(1460, ly + 126, "not used: no branch-HEAD fallback", 19, 400, MUTED, "middle"))
    p.append(
        f'<rect x="800" y="{ly-96}" width="120" height="40" rx="10" fill="{FDO_ACCENT}"/>'
        + _t(860, ly - 67, "--ref", 24, 700, "white", "middle")
        + f'<line x1="860" y1="{ly-56}" x2="860" y2="{ly-30}" stroke="{FDO_ACCENT}" stroke-width="4"/>'
    )

    # command -> result
    p.append(_box(
        60, 590, 830, 250,
        [
            ("python main.py --only fetch", 23, 400, INK),
            ("--repo https://github.com/sparqlunicorn/sparqlunicornGoesGIS", 23, 400, INK, 26),
            (f"--ref {PIN_SHA}", 23, 400, INK, 26),
            (None, 12),
            ("--ref is mandatory: without it, fetch stops", 19, 400, MUTED),
            ("instead of falling back to the branch HEAD.", 19, 400, MUTED),
        ],
        dashed=True, fill=CODE_BG,
    ))
    p.append(_arrow(898, 715, 982, 715))
    p.append(_box(
        990, 590, 700, 250,
        [
            (f"data/raw/sparqlunicornGoesGIS-{PIN_SHA7}/", 24, 700, INK),
            (None, 10),
            ("690 files: the working tree, without .git", 21, 400, MUTED),
            ("source_info.json: GitHub API metadata", 21, 400, MUTED),
            ("(description, licence, language)", 21, 400, MUTED),
            (None, 10),
            ("the only step that uses the network", 21, 700, FDO_ACCENT),
        ],
        dashed=True,
    ))
    p.append(_legend_and_note(
        "Example: SPARQLing Unicorn QGIS plugin, github.com/sparqlunicorn/sparqlunicornGoesGIS, read on 2026-11-05."))
    return _slide_close(p)


# --------------------------------------------------------- slide 2: inspect --


def _build_slide_inspect() -> str:
    p = _slide_open()
    p.append(_heading(1, "inspect", "Read what the repository already says"))

    p.append(_box(
        60, 320, 520, 330,
        [
            ("CITATION.cff", 27, 700, INK),
            ("in the repository at " + PIN_SHA7, 19, 400, MUTED),
            (None, 12),
            ("title: SPARQLing Unicorn QGIS Plugin", 21, 400, INK),
            ("version: 0.17.2", 21, 700, FDO_ACCENT),
            ("doi: 10.5281/zenodo.3786814", 21, 400, INK),
            ("authors: Florian Thiery, Timo Homburg", 21, 400, INK),
            ("identifiers: 15 DOIs, newest for 0.17.2", 21, 400, INK),
        ],
    ))
    p.append(_box(
        660, 320, 400, 150,
        [("inspect", 28, 700, INK), ("offline, reads only data/raw/", 19, 400, MUTED),
         ("the repository’s own CITATION.cff wins", 19, 400, MUTED)],
        dashed=True, center=True,
    ))
    p.append(_box(
        660, 500, 400, 150,
        [("+ CoMET-RS", 28, 700, INK), ("metadata with source", 19, 400, MUTED), ("and confidence", 19, 400, MUTED)],
        dashed=True, center=True,
    ))
    p.append(_arrow(588, 395, 652, 395))
    p.append(_arrow(588, 575, 652, 575))
    p.append(_arrow(1068, 395, 1132, 395))
    p.append(_arrow(1068, 575, 1132, 575))

    p.append(_box(
        1140, 320, 550, 330,
        [
            ("Proposal for mdcff, and open points", 24, 700, INK),
            (None, 10),
            ("licence: GNU General Public License v2.0", 21, 400, INK),
            (None, 12),
            ("For review:", 21, 700, FDO_ACCENT),
            ("• version 0.17.2 differs from release tag 0.17.4", 19.5, 400, INK, 6),
            ("• several DOIs, not linked to versions", 19.5, 400, INK, 6),
            ("• authors need reconciliation to an item", 19.5, 400, INK, 6),
        ],
        dashed=True,
    ))
    p.append(_t(60, 745, "The repository’s own CITATION.cff lags behind its latest release:", 25, 700, INK))
    p.append(_t(60, 782, "pinning a commit and reviewing the proposal makes that visible before anything is published.",
                25, 400, MUTED))
    p.append(_legend_and_note(
        "CoMET-RS output of 2–3 Nov 2026 (chublets-software/comet-metadata-extraction, examples/unicorn, "
        "tag v0.4.3-chublets.2); CITATION.cff read at tag v0.17.4."))
    return _slide_close(p)


# -------------------------------------------------------- slide 3: package --


def _build_slide_package() -> str:
    p = _slide_open()
    p.append(_heading(2, "mdcff + bundle", "One ZIP, the working tree flat at its root"))

    inputs = [
        ("CITATION.cff of the repository", "kept as it is, not rewritten", False),
        ("inspect proposal", "title, creator, licence", True),
        ("--title  --creator  --licence", "command-line overrides always win", True),
    ]
    ys = [310, 450, 590]
    for (title, sub, dashed), y in zip(inputs, ys):
        p.append(_box(60, y, 440, 118, [(title, 22, 700, INK), (sub, 19, 400, MUTED)], dashed=dashed, center=True))
    for y_in, y_out in zip([369, 509, 649], [450, 505, 560]):
        p.append(_arrow(508, y_in, 592, y_out))

    p.append(_box(
        600, 360, 300, 290,
        [("mdcff", 29, 700, INK), (None, 6), ("writes MD.cff", 20, 400, MUTED),
         ("fdo_type: fdo:SoftwareFDO", 19.5, 400, MUTED), (None, 6), ("validated against", 19.5, 400, MUTED),
         ("MD.cff-schema.yaml", 19.5, 400, MUTED)],
        dashed=True, center=True,
    ))
    p.append(_arrow(908, 505, 1002, 505))
    p.append(_t(955, 484, "bundle", 21, 700, FDO_ACCENT, "middle"))

    p.append(_box(
        1010, 300, 680, 440,
        [
            ("sparqlunicornGoesGIS.zip", 27, 700, INK),
            ("dist/<slug>.zip, working tree flat at the root", 19.5, 400, MUTED),
            (None, 14),
            ("MD.cff  (new)", 22, 700, FDO_ACCENT),
            ("CITATION.cff  (the repository’s own)", 22, 400, INK),
            ("LICENSE · README.md · RELEASE_NOTES.md", 22, 400, INK),
            ("sparql_unicorn.py · metadata.txt", 22, 400, INK),
            ("docs/ · test/ · util/ · tabs/ · …", 22, 400, INK),
            (None, 14),
            ("690 files from the working tree, plus MD.cff", 20, 700, INK),
            (None, 14),
            ("Flat on purpose: fdo-squirrel’s role rules", 19.5, 400, MUTED),
            ("match paths from the ZIP root, so no repo/ folder.", 19.5, 400, MUTED),
        ],
        dashed=True,
    ))
    p.append(_legend_and_note(
        "Working tree of sparqlunicorn/sparqlunicornGoesGIS at v0.17.4; layout and rules from fdo-git-packager PRIMER A2/A4."))
    return _slide_close(p)


# ---------------------------------------------------------- slide 4: build --


def _build_slide_build() -> str:
    p = _slide_open()
    p.append(_heading(3, "build_fdo", "Let fdo-squirrel make the FDO, then publish"))

    bw, bh, gap, x0, y0 = 225, 130, 36, 110, 380
    xs = [x0 + i * (bw + gap) for i in range(6)]
    boxes = [
        ("dist/<slug>.zip", "from bundle", True, False),
        ("build_fdo", "local fdo-squirrel", True, False),
        ("fdo-metadata.ttl", "proof it works", True, True),
        ("Zenodo deposit", "API upload → DOI", True, False),
        ("FDOx Registry", "DCAT, SHACL gate", False, False),
        ("N4O KG", "harvest", False, False),
    ]
    for x, (title, sub, dashed, filled) in zip(xs, boxes):
        if filled:
            p.append(
                f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="14" fill="{FDO_ACCENT}" stroke="{FDO_ACCENT}" '
                f'stroke-width="3.5" stroke-dasharray="14 9"/>'
                + _t(x + bw / 2, y0 + 62, title, 23, 700, "white", "middle")
                + _t(x + bw / 2, y0 + 94, sub, 19, 400, TINT, "middle")
            )
        else:
            p.append(_box(x, y0, bw, bh, [(title, 24, 700, INK), (sub, 19, 400, MUTED)], dashed=dashed, center=True))
    for i in range(5):
        p.append(_arrow(xs[i] + bw + 6, y0 + bh / 2, xs[i + 1] - 6, y0 + bh / 2))

    # two groups: what fdo-git-packager does itself, and what happens outside it
    gy = 330
    inner_x1, inner_x2 = xs[0], xs[2] + bw
    outer_x1, outer_x2 = xs[3], xs[5] + bw
    for xa, xb, label in ((inner_x1, inner_x2, "inside fdo-git-packager (step S6)"),
                          (outer_x1, outer_x2, "outside this repository, later")):
        p.append(f'<line x1="{xa}" y1="{gy}" x2="{xb}" y2="{gy}" stroke="{MUTED}" stroke-width="3"/>')
        p.append(_t(xa, gy - 14, label, 21, 700, MUTED))
    divider_x = (xs[2] + bw + xs[3]) / 2
    p.append(f'<line x1="{divider_x}" y1="300" x2="{divider_x}" y2="540" stroke="{MUTED}" stroke-width="2.5" '
             f'stroke-dasharray="6 8"/>')

    p.append(_box(
        110, 590, 700, 250,
        [
            ("SPARQLing Unicorn today", 25, 700, INK),
            (None, 10),
            ("CITATION.cff lists 15 DOIs", 22, 400, INK),
            ("newest snapshot: v0.17.2, 10.5281/zenodo.14874994", 22, 400, INK),
            ("release tag v0.17.4: no DOI listed", 22, 400, INK),
        ],
    ))
    p.append(_box(
        940, 590, 700, 250,
        [
            ("The pinned commit as an FDOx", 25, 700, INK),
            (None, 10),
            (f"commit {PIN_SHA7} of release v0.17.4", 22, 400, INK),
            ("MD.cff + CITATION.cff + working tree", 22, 400, INK),
            ("fdo-metadata.ttl as proof", 22, 400, INK),
            ("one deposit, one DOI of its own", 22, 700, FDO_ACCENT),
        ],
        dashed=True,
    ))
    p.append(_t(60, 950,
                "Zenodo’s GitHub integration archives only the source code of a release, so the FDOx ZIP goes "
                "up through the Zenodo API.", 19, 400, MUTED))
    # legend only (the note line above is this slide's footnote)
    ly = 880
    p.append(
        f'<rect x="60" y="{ly}" width="62" height="34" rx="9" fill="white" stroke="{FDO_ACCENT}" stroke-width="3.5"/>'
        + _t(140, ly + 25, "exists today", 22, 400, INK)
        + f'<rect x="330" y="{ly}" width="62" height="34" rx="9" fill="white" stroke="{FDO_ACCENT}" '
        f'stroke-width="3.5" stroke-dasharray="14 9"/>'
        + _t(410, ly + 25, "planned – fdo-git-packager is an S1 skeleton, no step is implemented yet", 22, 400, INK)
    )
    return _slide_close(p)


# -------------------------------------------------- slide 5: Actions lanes --

LANE_X0, LANE_X1 = 30, 1720
LANE_LABEL_X = 48
LANE_TOP0, LANE_H, LANE_GAP = 70, 180, 14
COL_X0, BOX_W, COL_GAP = 260, 215, 30
BOX_H = 110
LANE_TINT = "#F5F7FA"

# (lane title, lane subtitle)
_LANES = [
    ("GitHub", "repository"),
    ("GitHub Actions", "workflow: planned"),
    ("Zenodo", "deposit"),
    ("FDOx Registry", "→ N4O KG"),
]

# (lane, col, title, subline, step tag or None, exists_today)
_NODES = [
    (0, 0, "Publish release", "tag + commit SHA", None, True),
    (1, 0, "fetch", "--repo + --ref SHA", "1", False),
    (1, 1, "inspect", "CITATION.cff, CoMET-RS", "2", False),
    (1, 2, "mdcff", "MD.cff, validated", "3", False),
    (1, 3, "bundle", "flat ZIP", "3", False),
    (1, 4, "build_fdo", "→ fdo-squirrel", "4", False),
    (2, 4, "Zenodo deposit", "API upload → DOI", "4", False),
    (3, 4, "registry entry", "DOI + bundle link", "4", False),
    (3, 5, "N4O KG", "harvest", None, True),
]
_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)]


def _box_rect(lane: int, col: int) -> tuple[float, float, float, float]:
    x = COL_X0 + col * (BOX_W + COL_GAP)
    y = LANE_TOP0 + lane * (LANE_H + LANE_GAP) + (LANE_H - BOX_H) / 2
    return x, y, BOX_W, BOX_H


def _node_svg(node: tuple) -> str:
    lane, col, title, sub, tag, exists = node
    x, y, w, h = _box_rect(lane, col)
    dash = "" if exists else ' stroke-dasharray="14 9"'
    out = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="white" stroke="{FDO_ACCENT}" '
        f'stroke-width="3.5"{dash}/>'
        + _t(x + w / 2, y + h / 2 - 2, title, 25, 700, INK, "middle")
        + _t(x + w / 2, y + h / 2 + 28, sub, 18, 400, MUTED, "middle")
    )
    if tag:
        tx, ty = x - 14, y - 14
        out += (
            f'<rect x="{tx}" y="{ty}" width="40" height="40" rx="9" fill="{FDO_ACCENT}"/>'
            f'<text x="{tx + 20}" y="{ty + 29}" text-anchor="middle" font-family="Fira Sans" '
            f'font-weight="700" font-size="26" fill="white">{tag}</text>'
        )
    return out


def _edge_svg(a: tuple, b: tuple) -> str:
    ax, ay, aw, ah = _box_rect(a[0], a[1])
    bx, by, bw, bh = _box_rect(b[0], b[1])
    gap = 8
    if a[0] == b[0]:  # same lane: left to right
        return arrow_line(ax + aw + gap, ay + ah / 2, bx - gap, by + bh / 2, width=3)
    return arrow_line(ax + aw / 2, ay + ah + gap, bx + bw / 2, by - gap, width=3)


def _build_actions_svg() -> str:
    p = _slide_open()
    for i, (title, sub) in enumerate(_LANES):
        top = LANE_TOP0 + i * (LANE_H + LANE_GAP)
        fill = TINT if i == 1 else LANE_TINT
        p.append(f'<rect x="{LANE_X0}" y="{top}" width="{LANE_X1 - LANE_X0}" height="{LANE_H}" rx="16" fill="{fill}"/>')
        p.append(_t(LANE_LABEL_X, top + LANE_H / 2 - 4, title, 25, 700, INK))
        p.append(_t(LANE_LABEL_X, top + LANE_H / 2 + 26, sub, 20, 400, MUTED))

    for a, b in _EDGES:
        p.append(_edge_svg(_NODES[a], _NODES[b]))
    # what travels down from build_fdo to the deposit
    bx, by, bw, bh = _box_rect(1, 4)
    p.append(_t(bx + bw / 2 + 14, by + bh + 38, "ZIP + fdo-metadata.ttl", 18, 400, MUTED))
    for node in _NODES:
        p.append(_node_svg(node))

    ly = 880
    p.append(
        f'<rect x="{LANE_X0 + 4}" y="{ly}" width="62" height="34" rx="9" fill="white" '
        f'stroke="{FDO_ACCENT}" stroke-width="3.5"/>'
        + _t(LANE_X0 + 84, ly + 25, "exists today", 22, 400, INK)
        + f'<rect x="{LANE_X0 + 300}" y="{ly}" width="62" height="34" rx="9" fill="white" '
        f'stroke="{FDO_ACCENT}" stroke-width="3.5" stroke-dasharray="14 9"/>'
        + _t(LANE_X0 + 380, ly + 25, "planned – fdo-git-packager is an S1 skeleton, no step is implemented yet",
             22, 400, INK)
    )
    p.append(_t(LANE_X0 + 4, ly + 70,
                "Zenodo’s GitHub integration archives only the source code of a release, not its assets "
                "– hence the upload through the Zenodo API.", 20, 400, MUTED))
    return _slide_close(p)


# --------------------------------------------------------------------- run --

SLIDES = [
    ("fdox-talk-git-packager-step1-fetch", _build_slide_fetch),
    ("fdox-talk-git-packager-step2-inspect", _build_slide_inspect),
    ("fdox-talk-git-packager-step3-package", _build_slide_package),
    ("fdox-talk-git-packager-step4-build", _build_slide_build),
    ("fdox-talk-git-packager-actions", _build_actions_svg),
]


def _to_rgb(png_path: Path) -> None:
    from PIL import Image  # lazy, same reasoning as visuals_utils

    with Image.open(png_path) as im:  # S8 convention: opaque slide, RGB not RGBA
        rgb = im.convert("RGB")
    rgb.save(png_path)


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []
    warnings: list[str] = []

    desc_lines = [wrap_text(s["desc"]) for s in BANNER_STEPS]
    for s, lines in zip(BANNER_STEPS, desc_lines):
        if len(lines) > 3:
            warnings.append(f'description for step {s["num"]} wraps to {len(lines)} lines (design assumes <=3)')

    svg_text, h = _build_banner_svg(desc_lines)
    svg_path = img_path("fdox-git-packager-four-steps.svg")
    svg_path.write_text(svg_text, encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    render_svg_to_png(svg_path, png_path, int(W * OVERSAMPLE), int(h * OVERSAMPLE))
    fw, fh = trim_transparent_border(png_path, margin_px=10)
    log.append(f"wrote {svg_path.relative_to(IMG_DIR.parent).as_posix()} + .png ({fw}x{fh}, transparent, <=10px border)")

    for i, step in enumerate(BANNER_STEPS):
        svg_text, vb = _build_badge_svg(i)
        svg_path = img_path(f"fdox-git-packager-step-{step['num']}-{step['slug']}.svg")
        svg_path.write_text(svg_text, encoding="utf-8")
        png_path = svg_path.with_suffix(".png")
        render_svg_to_png(svg_path, png_path, int(vb * ICON_SCALE), int(vb * ICON_SCALE))
        fw, fh = trim_transparent_border(png_path, margin_px=10)
        log.append(f"wrote {svg_path.relative_to(IMG_DIR.parent).as_posix()} + .png ({fw}x{fh}, transparent, <=10px border)")

    for name, build_fn in SLIDES:
        svg_path = img_path(f"{name}.svg")
        svg_path.write_text(build_fn(), encoding="utf-8")
        png_path = svg_path.with_suffix(".png")
        render_svg_to_png(svg_path, png_path, SW * SLIDE_OVERSAMPLE, SH * SLIDE_OVERSAMPLE)
        _to_rgb(png_path)
        log.append(f"wrote {svg_path.relative_to(IMG_DIR.parent).as_posix()} + .png ({SW*SLIDE_OVERSAMPLE}x{SH*SLIDE_OVERSAMPLE}, white background)")

    if warnings:
        for w in warnings:
            log.append(f"WARNING: {w}")
        if strict:
            raise RuntimeError(f"{len(warnings)} warning(s) in step 'git-packager' (--strict)")

    return log


if __name__ == "__main__":
    for line in run():
        print(line)
