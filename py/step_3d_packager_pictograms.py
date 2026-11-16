"""S19 -- Pictograms for the six steps of fdo-3d-packager.

fdo-3d-packager (FDOx-squirrel, MIT) runs six steps, as its CLI names them:

  1 fetch      Sketchfab API / local files
  2 convert    Blender -> OBJ + textures
  3 nexus      multiresolution build
  4 mdcff      MD.cff + CITATION.cff
  5 bundle     3DHOP viewer + ZIP
  6 build_fdo  -> fdo-squirrel

Same badge as the pictograms of the fdo-git-packager steps (circle, line icon, number tag), but with a
*solid* outline: this tool exists and is released, the git-packager is a skeleton (dashed). Transparent
PNG, at most 10 px border, like the other pictograms.

Runnable standalone: `python py/step_3d_packager_pictograms.py`
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visuals_utils import (  # noqa: E402
    FDO_ACCENT,
    IMG_DIR,
    STEPS,
    ensure_dirs,
    font_face_css,
    img_path,
    render_svg_to_png,
    trim_transparent_border,
)

TINT = STEPS[0]["tint"]
BADGE_R = 150
TAG_SIZE = 132
TAG_OFFSET = 26
ICON_SCALE = 4
SW = 6

# (number, slug, name as in the CLI)
PACKAGER_STEPS = [
    ("1", "fetch", "fetch"),
    ("2", "convert", "convert"),
    ("3", "nexus", "nexus"),
    ("4", "mdcff", "mdcff"),
    ("5", "bundle", "bundle"),
    ("6", "build-fdo", "build_fdo"),
]


def _line(x1, y1, x2, y2, c) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{SW}" stroke-linecap="round"/>'


def _poly(points: str, c) -> str:
    return (f'<polyline points="{points}" fill="none" stroke="{c}" stroke-width="{SW}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>')


def _icon_fetch(c: str) -> str:
    """An arrow into a tray: a download."""
    return _line(0, -54, 0, 14, c) + _poly("-26,-12 0,16 26,-12", c) + _poly("-50,18 -50,52 50,52 50,18", c)


def _icon_convert(c: str) -> str:
    """Two opposite arrows: one format becomes another."""
    return (_line(-52, -22, 48, -22, c) + _poly("24,-46 50,-22 24,2", c)
            + _line(52, 24, -48, 24, c) + _poly("-24,0 -50,24 -24,48", c))


def _icon_nexus(c: str) -> str:
    """Three layers: the levels of detail of a multiresolution model."""
    return (
        f'<polygon points="0,-52 54,-26 0,0 -54,-26" fill="none" stroke="{c}" stroke-width="{SW}" stroke-linejoin="round"/>'
        + _poly("-54,-2 0,24 54,-2", c)
        + _poly("-54,20 0,46 54,20", c)
    )


def _icon_mdcff(c: str) -> str:
    """A file with key: value lines: the metadata file."""
    return (
        f'<path d="M -40,-58 L 14,-58 L 40,-32 L 40,58 L -40,58 Z" fill="none" stroke="{c}" '
        f'stroke-width="{SW}" stroke-linejoin="round"/>'
        + _poly("14,-58 14,-32 40,-32", c)
        + "".join(_line(-24, y, -10, y, c) + _line(2, y, 24, y, c) for y in (-8, 12, 32))
    )


def _icon_bundle(c: str) -> str:
    """An isometric box: the packaged object."""
    return (
        f'<polygon points="0,-62 54,-31 54,31 0,62 -54,31 -54,-31" fill="none" stroke="{c}" '
        f'stroke-width="{SW}" stroke-linejoin="round"/>'
        + _poly("-54,-31 0,0 54,-31", c) + _line(0, 0, 0, 62, c)
    )


def _icon_build(c: str) -> str:
    """A database cylinder: where the FDO ends up."""
    return (
        f'<ellipse cx="0" cy="-42" rx="48" ry="16" fill="none" stroke="{c}" stroke-width="{SW}"/>'
        + _line(-48, -42, -48, 42, c) + _line(48, -42, 48, 42, c)
        + f'<path d="M -48,0 A 48,16 0 0 0 48,0" fill="none" stroke="{c}" stroke-width="{SW}"/>'
        + f'<path d="M -48,42 A 48,16 0 0 0 48,42" fill="none" stroke="{c}" stroke-width="{SW}"/>'
    )


_ICONS = [_icon_fetch, _icon_convert, _icon_nexus, _icon_mdcff, _icon_bundle, _icon_build]


def badge_group(idx: int, cx: float = 0, cy: float = 0, scale: float = 1.0) -> str:
    """One step badge as an SVG group, to draw it inside other graphics (radius BADGE_R * scale)."""
    tag = -BADGE_R - TAG_OFFSET
    num = PACKAGER_STEPS[idx][0]
    return (
        f'<g transform="translate({cx},{cy}) scale({scale})">'
        f'<circle cx="0" cy="0" r="{BADGE_R}" fill="{TINT}" stroke="{FDO_ACCENT}" stroke-width="7"/>'
        f'<g>{_ICONS[idx](FDO_ACCENT)}</g>'
        f'<rect x="{tag}" y="{tag}" width="{TAG_SIZE}" height="{TAG_SIZE}" rx="26" fill="{FDO_ACCENT}"/>'
        f'<text x="{tag + TAG_SIZE / 2}" y="{tag + TAG_SIZE / 2 + 40}" text-anchor="middle" font-family="Fira Sans" '
        f'font-weight="700" font-size="104" fill="white">{num}</text></g>'
    )


def _badge_svg(idx: int) -> tuple[str, int]:
    pad = 15
    left = top = -(BADGE_R + TAG_OFFSET) - pad
    right = bottom = BADGE_R + pad
    vb = right - left
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{vb}" height="{vb}" viewBox="{left} {top} {vb} {vb}">',
        font_face_css(),
        badge_group(idx),
        "</svg>",
    ]
    return "\n".join(p), vb


def run(strict: bool = False) -> list[str]:
    ensure_dirs()
    log: list[str] = []
    for i, (num, slug, _) in enumerate(PACKAGER_STEPS):
        svg_text, vb = _badge_svg(i)
        svg_path = img_path(f"fdox-3d-packager-step-{num}-{slug}.svg")
        svg_path.write_text(svg_text, encoding="utf-8")
        png_path = svg_path.with_suffix(".png")
        render_svg_to_png(svg_path, png_path, vb * ICON_SCALE, vb * ICON_SCALE)
        fw, fh = trim_transparent_border(png_path, margin_px=10)
        log.append(f"wrote {svg_path.relative_to(IMG_DIR.parent).as_posix()} + .png ({fw}x{fh}, transparent, <=10px border)")
    return log


if __name__ == "__main__":
    for line in run():
        print(line)
