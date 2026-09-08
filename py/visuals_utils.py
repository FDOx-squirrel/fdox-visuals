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
    import cairosvg  # lazy: keeps --list/--dry-run free of the import

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=width,
        output_height=height,
    )


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
