"""fdox-visuals: shared constants and render helpers.

No step imports rdflib/matplotlib/pandas — this stays light on purpose so
`python main.py --list` and `--dry-run` are instant.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONTS_DIR = ROOT / "fonts"
IMG_DIR = ROOT / "img"

FONT_REGULAR = FONTS_DIR / "FiraSans-Regular.ttf"
FONT_BOLD = FONTS_DIR / "FiraSans-Bold.ttf"
FONT_FAMILY = "Fira Sans"

# Every generated SVG lives directly under img/, so the relative path back
# to fonts/ is always the same. If a step ever writes its SVG somewhere
# else, this constant has to move with it.
_FONT_REL_PREFIX = "../fonts"

INK = "#161B2E"
MUTED = "#5B6478"
BG = "#FFFFFF"

# The one family palette. Step 1's colour is the *original* FAIR Digital
# Object blue (#004473, sampled from the reference diagram) — every other
# graphic in this repo that needs "the FDOx blue" reads it from here rather
# than repeating the literal, so the family stays a single source of truth.
STEPS = [
    {
        "id": "fdo-encapsulation",
        "num": "1",
        "title": ["FDO", "Encapsulation"],
        "desc": "Persistent identifier, structured metadata & provenance",
        "color": "#004473",
        "tint": "#E6ECF1",
    },
    {
        "id": "semantic-paradata-modelling",
        "num": "2",
        "title": ["Semantic Metadata", "& Paradata Modelling"],
        "desc": "Acquisition, spatial anchoring & CIDOC CRM alignment",
        "color": "#0E9488",
        "tint": "#E6F6F4",
    },
    {
        "id": "linking-community-hubs",
        "num": "3",
        "title": ["Linking to", "Community Hubs"],
        "desc": "Cross-referenced with Wikidata & OpenStreetMap",
        "color": "#C2790C",
        "tint": "#FCF1E1",
    },
    {
        "id": "federated-kg-integration",
        "num": "4",
        "title": ["Federated Knowledge", "Graph Integration"],
        "desc": "RDF joins distributed research infrastructures",
        "color": "#8034C9",
        "tint": "#F3E9FC",
    },
]

FDO_ACCENT = STEPS[0]["color"]  # #004473 — reused by the FDO meta-graphic

# Two lightened tints of FDO_ACCENT, for graphics that use a single flat
# brand colour rather than the four-step rainbow above (S7 purpose banner:
# icon-circle gradient + connector chevrons). Derived once here rather than
# repeated as literals in the step module (A3: one palette, one source).
FDO_ACCENT_LIGHT = "#116099"
FDO_ACCENT_SOFT = "#4E8FBE"


def ensure_dirs() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)


def esc(text: str) -> str:
    """Escape the handful of characters that appear in our own copy text."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap_text(text: str, max_chars: int = 26) -> list[str]:
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def font_face_css() -> str:
    """@font-face block pointing at the two vendored weights.

    Vendored, not referenced (PRIMER A3): the repo carries its own copy of
    Fira Sans under fonts/, so a fresh clone renders identically without
    the font being installed on the machine that runs it.
    """
    return (
        "<style>"
        f'@font-face {{ font-family: "{FONT_FAMILY}"; '
        f'src: url("{_FONT_REL_PREFIX}/FiraSans-Regular.ttf"); font-weight: 400; }} '
        f'@font-face {{ font-family: "{FONT_FAMILY}"; '
        f'src: url("{_FONT_REL_PREFIX}/FiraSans-Bold.ttf"); font-weight: 700; }}'
        "</style>"
    )


def render_svg_to_png(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    """Rasterise via resvg (a single self-contained compiled wheel — no
    system libcairo/rsvg/ImageMagick needed, which is exactly what broke
    on Windows with the cairosvg-based first version of this repo: pip
    installs the Python package fine, but cairosvg still needs a system
    libcairo-2.dll that pip does not provide. resvg's wheel bundles the
    (Rust, statically-linked) renderer itself, so `pip install` is really
    the whole story.
    """
    import resvg_py  # lazy: keeps --list/--dry-run free of the import

    png_bytes = resvg_py.svg_to_bytes(
        svg_path=str(svg_path),
        width=width,
        height=height,
        font_files=[str(FONT_REGULAR), str(FONT_BOLD)],
        skip_system_fonts=True,  # always our vendored files, never a same-named system font
    )
    png_path.write_bytes(png_bytes)


def trim_transparent_border(png_path: Path, margin_px: int = 10) -> tuple[int, int]:
    """Crop a PNG to its non-transparent content, then pad back out to an
    exact, small, uniform transparent border.

    Works from the actual rendered alpha channel rather than a hand-
    computed design-unit margin — a wide title in one step's text can
    push the true content edge further out than the badge geometry alone
    would suggest (confirmed by inspecting the real render: the fourth
    step's title text extends past its own badge circle). Cropping pixels
    can't clip content the way guessing a margin in SVG coordinates could.

    Returns the final (width, height) for logging.
    """
    from PIL import Image  # lazy, same reasoning as render_svg_to_png

    im = Image.open(png_path).convert("RGBA")
    bbox = im.split()[-1].getbbox()  # bounding box of the alpha channel
    if bbox is None:
        return im.size  # fully transparent; nothing sensible to crop to
    cropped = im.crop(bbox)
    w, h = cropped.size
    out = Image.new("RGBA", (w + 2 * margin_px, h + 2 * margin_px), (0, 0, 0, 0))
    out.paste(cropped, (margin_px, margin_px))
    out.save(png_path)
    return out.size


def flatten_to_jpg(png_path: Path, jpg_path: Path, quality: int = 95) -> None:
    """Flatten a (possibly transparent) PNG onto white and save as JPEG.

    JPEG has no alpha channel; a plain `.convert("RGB")` would paint
    transparent pixels black instead of white, which is wrong for a
    graphic meant to sit on a white slide.
    """
    from PIL import Image  # lazy, same reasoning as above

    with Image.open(png_path) as im:
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        bg.save(jpg_path, "JPEG", quality=quality, subsampling=0)


# --- generic SVG line/box primitives -----------------------------------
# Added for S8/S9 (talk-process / talk-purpose slides), which compose
# flowchart-like diagrams rather than the badge grids S2/S7 draw. Pure
# string formatters, no heavy import, so they don't cost --list/--dry-run
# anything (A2 in spirit: keep this module light).


def arrow_marker(marker_id: str = "arrow", color: str = MUTED) -> str:
    """A `<marker>` definition for arrowheads; drop once per SVG, then
    reference filled lines with `marker-end="url(#{marker_id})"`.
    """
    return (
        f'<marker id="{marker_id}" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
    )


def arrow_line(x1: float, y1: float, x2: float, y2: float, color: str = MUTED,
               width: float = 4, marker_id: str = "arrow") -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{width}" marker-end="url(#{marker_id})"/>'
    )


def elbow_path(points: list[tuple[float, float]], color: str = MUTED,
               width: float = 4, marker_id: str = "arrow") -> str:
    """A multi-segment orthogonal/angled connector ending in an arrowhead."""
    pts = " ".join(f"{x},{y}" for x, y in points)
    return (
        f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linejoin="round" marker-end="url(#{marker_id})"/>'
    )


def label_box(x: float, y: float, w: float, h: float, lines: list[tuple[str, int, float]],
              fill: str = "white", stroke: str = INK, text_color: str = INK, radius: float = 14) -> str:
    """A rounded rectangle centred on (x + w/2, y + h/2) holding one or more
    text lines, each given as (text, font-weight, font-size), vertically
    centred as a block.
    """
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="3.5"/>'
    n = len(lines)
    line_h = 30
    start_y = y + h / 2 - (n - 1) * line_h / 2 + 8
    for i, (text, weight, size) in enumerate(lines):
        out += (
            f'<text x="{x + w/2}" y="{start_y + i*line_h}" text-anchor="middle" font-family="{FONT_FAMILY}" '
            f'font-weight="{weight}" font-size="{size}" fill="{text_color}">{esc(text)}</text>'
        )
    return out


def edge_label(x1: float, y1: float, x2: float, y2: float, frac: float, text: str,
               font_size: float = 20, color: str = INK) -> str:
    """A short bold label sitting directly on a line, rotated to match the
    line's angle, with a white buffer rect behind it so it stays legible
    where it crosses the line.
    """
    import math

    lx = x1 + (x2 - x1) * frac
    ly = y1 + (y2 - y1) * frac
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle > 90:
        angle -= 180
    if angle < -90:
        angle += 180
    text_w = len(text) * font_size * 0.60 + 20
    text_h = font_size + 14
    return (
        f'<g transform="translate({lx:.1f},{ly:.1f}) rotate({angle:.1f})">'
        f'<rect x="{-text_w/2:.1f}" y="{-text_h/2:.1f}" width="{text_w:.1f}" height="{text_h:.1f}" rx="6" '
        f'fill="white" stroke="{color}" stroke-width="1.3" opacity="0.95"/>'
        f'<text x="0" y="{font_size*0.36:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" '
        f'font-weight="700" font-size="{font_size}" fill="{color}">{esc(text)}</text></g>'
    )


def measure_content_margins(png_path: Path, exclude_box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Return (left, right, top, bottom) pixel margins of non-white content
    in an opaque PNG, ignoring a rectangular region (x0, y0, x1, y1) —
    used to blank out a fixed-position corner badge before measuring, so
    the *content* can be re-centred without ever moving the badge.

    PIL-only (no numpy): a difference-against-white image, blanked over
    the excluded box, then `Image.getbbox()`.
    """
    from PIL import Image, ImageChops

    im = Image.open(png_path).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    x0, y0, x1, y1 = exclude_box
    diff.paste(Image.new("RGB", (x1 - x0, y1 - y0), (0, 0, 0)), (x0, y0))
    bbox = diff.getbbox()
    w, h = im.size
    if bbox is None:
        return (0, 0, 0, 0)
    left, top, right, bottom = bbox
    return (left, w - right, top, h - bottom)


def paste_raster(base_png_path: Path, asset_path: Path, x: int, y: int, w: int, h: int,
                  scale: float, circular: bool = False) -> None:
    """Composite a source raster asset (a screenshot or photo under
    img/source/) onto an already-rendered PNG, at design-grid (x, y, w, h)
    scaled by the same `scale` factor the SVG was rasterised at.

    Used by S8's Sketchfab/registry screenshots and CIIC 81 photo -- real
    third-party assets that cannot be regenerated from a script (S8 Ziel),
    so they are shipped under img/source/ and composited rather than drawn.
    """
    from PIL import Image, ImageDraw

    base = Image.open(base_png_path).convert("RGB")
    px, py, pw, ph = (int(v * scale) for v in (x, y, w, h))
    src = Image.open(asset_path).convert("RGB").resize((pw, ph), Image.LANCZOS)
    if circular:
        mask = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, pw, ph), fill=255)
        base.paste(src, (px, py), mask)
    else:
        base.paste(src, (px, py))
    base.save(base_png_path)
