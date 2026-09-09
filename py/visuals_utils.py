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
