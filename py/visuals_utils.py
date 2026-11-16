"""fdox-visuals: shared constants and render helpers.

No step imports rdflib/matplotlib/pandas — this stays light on purpose so
`python main.py --list` and `--dry-run` are instant.
"""

from __future__ import annotations

import base64
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONTS_DIR = ROOT / "fonts"
IMG_DIR = ROOT / "img"

FONT_REGULAR = FONTS_DIR / "FiraSans-Regular.ttf"
FONT_BOLD = FONTS_DIR / "FiraSans-Bold.ttf"
FONT_FAMILY = "Fira Sans"

# Every generated SVG lives in img/<category>/ (one level below img/), so the
# relative path back to fonts/ is always the same. If a step ever writes its
# SVG somewhere else, this constant has to move with it.
_FONT_REL_PREFIX = "../../fonts"

# Topic folders under img/. The order is the order of the site (S14), and the
# order of the navigation. A graphic belongs to the category with the longest
# prefix its file stem starts with.
CATEGORIES = [
    {"slug": "pattern", "group": "Concept", "title": "The four-step pattern and its outcomes",
     "desc": "The two banners: the four FDO steps and the four outcomes of FDOx.",
     "prefixes": ["fdox-four-step-pattern", "fdox-purpose-pattern"]},
    {"slug": "pictograms", "group": "Concept", "title": "Pictograms: steps and outcomes",
     "desc": "The eight pictograms as single files: the four steps and the four outcomes.",
     "prefixes": ["fdox-step-", "fdox-purpose-"]},
    {"slug": "schemas", "group": "Concept", "title": "Schemas, architecture and bundle views",
     "desc": "The MD.cff and CITATION.cff schemas, the fdo-squirrel architecture, the three views of a bundle (RDF, RO-Crate, landing page) and the FDO meta graphic.",
     "prefixes": ["fdox-md-cff-schema", "fdox-citation-cff-schema", "fdox-fdo-squirrel-architecture",
                  "fdox-bundle-three-views",
                  "fdox-fair-digital-object-meta-graphic", "fdox-fdo-sphere"]},
    {"slug": "sphere", "group": "Concept", "title": "The FDO sphere and the community hubs",
     "desc": "The eight pictograms around the FDO sphere, with and without the community hubs.", "prefixes": ["fdox-sphere-"]},
    {"slug": "steps", "group": "3D models", "title": "The four steps in practice",
     "desc": "One graphic per FDOx step with real values of CIIC 81: packaging with fdo-3d-packager (RDF and RO-Crate via fdo-squirrel), modelling, linking, federation.",
     "prefixes": ["fdox-steps-"]},
    {"slug": "outcomes", "group": "3D models", "title": "The four outcomes in practice",
     "desc": "One graphic per outcome: FAIR and citable, semantically queryable, interoperable, integrable.",
     "prefixes": ["fdox-outcomes-"]},
    {"slug": "3d-packager-pictograms", "group": "3D models", "title": "Pictograms: fdo-3d-packager",
     "desc": "The six pictograms of the fdo-3d-packager steps: fetch, convert, nexus, mdcff, bundle, build_fdo.",
     "prefixes": ["fdox-3d-packager-step-"]},
    {"slug": "git-packager", "group": "Software", "title": "fdo-git-packager: software as FDO",
     "desc": "Concept graphics for packaging a Git repository as an FDO (the tool is a skeleton, nothing here is implemented yet).",
     "prefixes": ["fdox-git-packager-"]},
    {"slug": "git-packager-pictograms", "group": "Software", "title": "Pictograms: fdo-git-packager",
     "desc": "The four pictograms of the fdo-git-packager steps: pin, inspect, package, build.",
     "prefixes": ["fdox-git-packager-step-"]},
    {"slug": "story", "group": "3D and software", "title": "From the FKGE to FDOx",
     "desc": "Graphics that lead from the federated knowledge graph ecosystem to FDOx, for 3D models and software.",
     "prefixes": ["fdox-story-"]},
    {"slug": "federation", "group": "3D and software", "title": "Federated knowledge graph ecosystem",
     "desc": "Finished 3D and software FDOs in the registry and the N4O collection.",
     "prefixes": ["fdox-federation-"]},
    {"slug": "ogham-graph", "group": "3D and software", "title": "Ogham graph pictures",
     "desc": "Graph pictures of Ogham stones, their 3D FDOs and the software that uses them.",
     "prefixes": ["fdox-ogham-graph-"]},
]


def category_of(stem: str) -> str:
    """Folder slug (under img/) for a graphic's file stem: the longest matching prefix wins."""
    best, best_len = None, -1
    for cat in CATEGORIES:
        for pre in cat["prefixes"]:
            if stem.startswith(pre) and len(pre) > best_len:
                best, best_len = cat["slug"], len(pre)
    if best is None:
        raise KeyError(f"no category for graphic {stem!r}; add its prefix to CATEGORIES")
    return best


def img_path(filename: str) -> Path:
    """Output path of a graphic: img/<category>/<filename>; creates the folder."""
    folder = IMG_DIR / category_of(Path(filename).stem)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / filename

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
FDO_TINT = STEPS[0]["tint"]  # #E6ECF1 — page tint of the site (S14)

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


def write_tight_graphic(svg_text: str, svg_path: Path, png_path: Path, scale: float = 2.0, margin_px: int = 10) -> tuple[int, int]:
    """Write a graphic that has no background and no empty canvas.

    The SVG is first drawn on its design canvas and rasterised once; the alpha
    channel tells where the content really is. The SVG's own width, height and
    viewBox are then rewritten to that content box plus `margin_px`, so the SVG
    and the PNG are cropped the same way (like the schemas), and the PNG is
    rendered again from the cropped SVG. Returns the PNG size.
    """
    import re

    from PIL import Image  # lazy, as in trim_transparent_border

    svg_path.write_text(svg_text, encoding="utf-8")
    m = re.search(r'<svg [^>]*viewBox="([-\d. ]+)"[^>]*>', svg_text)
    if m is None:
        raise ValueError("write_tight_graphic: no viewBox in the SVG")
    vx, vy, vw, vh = (float(v) for v in m.group(1).split())
    render_svg_to_png(svg_path, png_path, int(vw * scale), int(vh * scale))
    bbox = Image.open(png_path).convert("RGBA").split()[-1].getbbox()
    if bbox is None:
        return Image.open(png_path).size
    pad = margin_px / scale
    x0 = round(vx + bbox[0] / scale - pad, 2)
    y0 = round(vy + bbox[1] / scale - pad, 2)
    x1 = round(vx + bbox[2] / scale + pad, 2)
    y1 = round(vy + bbox[3] / scale + pad, 2)
    w, h = round(x1 - x0, 2), round(y1 - y0, 2)
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{x0} {y0} {w} {h}">'
    svg_path.write_text(svg_text.replace(m.group(0), head, 1), encoding="utf-8")
    render_svg_to_png(svg_path, png_path, int(round(w * scale)), int(round(h * scale)))
    return trim_transparent_border(png_path, margin_px=margin_px)


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


# Third-party logos used in the graphics (img/source/NOTICE.md says whose they
# are and under which terms). Each is looked up as img/source/<stem>.svg, then
# .png; fewer than all of them is fine, a text pill stands in for a missing one.
LOGOS = {
    "ro-crate": {"stem": "ro-crate-logo", "credit": "RO-Crate logo: RO-Crate Community, CC BY 4.0"},
    "rdf": {"stem": "rdf-logo", "credit": "RDF logo: Bill Schwappacher / W3C, CC BY 4.0"},
}
RO_CRATE_LOGO_CREDIT = LOGOS["ro-crate"]["credit"]


def logo_path(key: str) -> Path | None:
    stem = LOGOS[key]["stem"]
    for ext in (".svg", ".png"):
        candidate = IMG_DIR / "source" / (stem + ext)
        if candidate.exists():
            return candidate
    return None


def logo_credits() -> str:
    """The credit line for the logos that are actually present."""
    return "  ·  ".join(LOGOS[k]["credit"] for k in LOGOS if logo_path(k) is not None)


def _svg_ratio(head: str) -> float:
    m = re.search(r'viewBox\s*=\s*"([-\d.eE]+)[ ,]+([-\d.eE]+)[ ,]+([-\d.eE]+)[ ,]+([-\d.eE]+)"', head)
    if m and float(m.group(4)) > 0:
        return float(m.group(3)) / float(m.group(4))
    # no viewBox: fall back to the width and height attributes of the root element
    root = re.search(r"<svg\b[^>]*>", head)
    if root:
        wm = re.search(r'\bwidth\s*=\s*"([\d.]+)', root.group(0))
        hm = re.search(r'\bheight\s*=\s*"([\d.]+)', root.group(0))
        if wm and hm and float(hm.group(1)) > 0:
            return float(wm.group(1)) / float(hm.group(1))
    return 1.0


def logo(key: str, x: float, y: float, max_w: float, max_h: float) -> str:
    """The logo as an <image> with an embedded data: URI, fitted into the
    given box and centred in it; empty string if no logo file exists."""
    path = logo_path(key)
    if path is None:
        return ""
    raw = path.read_bytes()
    if path.suffix.lower() == ".png":
        mime = "image/png"
        # IHDR: width and height are big-endian 32-bit ints at bytes 16-24
        pw, ph = struct.unpack(">II", raw[16:24])
        ratio = pw / ph if ph else 1.0
    else:
        mime = "image/svg+xml"
        ratio = _svg_ratio(raw[:2000].decode("utf-8", errors="ignore"))
    w, h = max_w, max_w / ratio
    if h > max_h:
        w, h = max_h * ratio, max_h
    ix, iy = x + (max_w - w) / 2, y + (max_h - h) / 2
    uri = f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")
    return f'<image x="{ix:.1f}" y="{iy:.1f}" width="{w:.1f}" height="{h:.1f}" xlink:href="{uri}"/>'


def ro_crate_logo_path() -> Path | None:
    return logo_path("ro-crate")


def ro_crate_logo(x: float, y: float, max_w: float, max_h: float) -> str:
    return logo("ro-crate", x, y, max_w, max_h)


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
