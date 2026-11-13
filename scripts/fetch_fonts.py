"""
Self-host the type system — run once, commit the result.

Two sources, one convention on disk (``{slug}-{weight}-{style}-{subset}.woff2`` under
``static/fonts/``) and one generated stylesheet, ``static/css/fonts.css``, with ``@font-face``
rules (``font-display: swap`` + ``unicode-range``) pointing at the LOCAL files only:

* the Google Fonts CSS API, for the families that only exist there as subset woff2
  (Newsreader, Noto Naskh Arabic, IBM Plex Sans Arabic) — ``FAMILIES`` below;
* the ``@fontsource`` npm packages, for the families design V4 added
  (docs/design-v4/DESIGN_SYSTEM_V4.md §4.1: IBM Plex Sans and IBM Plex Mono replace Fira Sans and
  Fira Mono, so that the Latin interface and the Arabic interface — IBM Plex Sans Arabic, already
  vendored — are one superfamily). Fontsource ships the same OFL fonts, already split into the same
  ``unicode-range`` subsets; ``--from-fontsource`` copies the needed files out of ``node_modules``
  under our file names — ``FONTSOURCE`` below.

The runtime site never contacts fonts.googleapis.com / fonts.gstatic.com (CSP is self-only and
the compliance scanner rejects those hosts). This script is the only place those hosts appear.

Licences — every family here is SIL Open Font License 1.1, which permits self-hosting and
redistribution with the licence text (see docs/IMAGE_LICENSES.md for the recorded attributions):

  Newsreader            Production Type    OFL 1.1
  IBM Plex Sans         IBM Corp.          OFL 1.1  (via @fontsource/ibm-plex-sans, design V4)
  IBM Plex Mono         IBM Corp.          OFL 1.1  (via @fontsource/ibm-plex-mono, design V4)
  Noto Naskh Arabic     Google             OFL 1.1
  IBM Plex Sans Arabic  IBM Corp.          OFL 1.1

Usage (from the project root)::

    .venv/Scripts/python scripts/fetch_fonts.py                   # Google families + fontsource + fonts.css
    .venv/Scripts/python scripts/fetch_fonts.py --from-fontsource # copy the fontsource files + fonts.css
    .venv/Scripts/python scripts/fetch_fonts.py --css-only        # rewrite fonts.css from files on disk
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "static" / "fonts"
CSS_FILE = ROOT / "static" / "css" / "fonts.css"
NODE_MODULES = ROOT / "node_modules"

# A modern Chrome UA makes the API answer with woff2 + unicode-range subsets.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
CSS_API = "https://fonts.googleapis.com/css2"

# family → (slug, axis spec). Weights are deliberately restrained (institutional voice).
FAMILIES: dict[str, tuple[str, str]] = {
    # Latin display. The opsz axis is the reason this family was chosen: the display plate and the
    # lead are different drawings (AD-A §3.2). V4 keeps it for the public H1s, section titles, the
    # hero lead and the wordmark — and nowhere on an operational screen (DESIGN_SYSTEM_V4.md §4.2).
    "Newsreader": ("newsreader", "ital,opsz,wght@0,6..72,200..800;1,6..72,200..800"),
    # Arabic display + prose. A true Naskh is the register Moroccan administrative documents use and
    # the correct counterpart to a Latin serif (AD-A §3.2).
    "Noto Naskh Arabic": ("noto-naskh-arabic", "wght@400..700"),
    # Arabic interface face: since V4 the Arabic half of the Plex superfamily.
    "IBM Plex Sans Arabic": ("ibm-plex-sans-arabic", "wght@400;500;600"),
}
SUBSETS = ("latin", "latin-ext", "arabic")

# family → (slug, npm package, faces as (weight, style)). Latin interface + reference codes.
FONTSOURCE: dict[str, tuple[str, str, tuple[tuple[str, str], ...]]] = {
    "IBM Plex Sans": (
        "ibm-plex-sans",
        "@fontsource/ibm-plex-sans",
        (("400", "normal"), ("400", "italic"), ("500", "normal"), ("600", "normal")),
    ),
    "IBM Plex Mono": ("ibm-plex-mono", "@fontsource/ibm-plex-mono", (("400", "normal"),)),
}
FONTSOURCE_SUBSETS = ("latin", "latin-ext")

# The unicode ranges the Google Fonts API assigns to each subset — identical for every family, so
# a face copied from fontsource (which uses the same split) or rebuilt from disk gets the right one.
SUBSET_RANGES: dict[str, str] = {
    "latin": (
        "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, "
        "U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
    ),
    "latin-ext": (
        "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, "
        "U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF"
    ),
    "arabic": (
        "U+0600-06FF, U+0750-077F, U+0870-088E, U+0890-0891, U+0897-08E1, U+08E3-08FF, U+200C-200E, "
        "U+2010-2011, U+204F, U+2E41, U+FB50-FDFF, U+FE70-FE74, U+FE76-FEFC, U+102E0-102FB, U+10E60-10E7E, "
        "U+10EC2-10EC4, U+10EFC-10EFF, U+1EE00-1EE03, U+1EE05-1EE1F, U+1EE21-1EE22, U+1EE24, U+1EE27, "
        "U+1EE29-1EE32, U+1EE34-1EE37, U+1EE39, U+1EE3B, U+1EE42, U+1EE47, U+1EE49, U+1EE4B, U+1EE4D-1EE4F, "
        "U+1EE51-1EE52, U+1EE54, U+1EE57, U+1EE59, U+1EE5B, U+1EE5D, U+1EE5F, U+1EE61-1EE62, U+1EE64, "
        "U+1EE67-1EE6A, U+1EE6C-1EE72, U+1EE74-1EE77, U+1EE79-1EE7C, U+1EE7E, U+1EE80-1EE89, U+1EE8B-1EE9B, "
        "U+1EEA1-1EEA3, U+1EEA5-1EEA9, U+1EEAB-1EEBB, U+1EEF0-1EEF1"
    ),
}

_BLOCK = re.compile(r"/\*\s*(?P<subset>[a-z-]+)\s*\*/\s*@font-face\s*{(?P<body>.*?)}", re.S)
_PROP = re.compile(r"(?P<key>[a-z-]+)\s*:\s*(?P<value>[^;]+);")
_URL = re.compile(r"url\((?P<url>[^)]+)\)")
_FILENAME = re.compile(
    r"(?P<slug>[a-z-]+?)-(?P<weight>\d+(?:-\d+)?)-(?P<style>normal|italic)-(?P<subset>[a-z-]+)\.woff2$"
)


@dataclass(frozen=True)
class Face:
    family: str
    slug: str
    style: str
    weight: str
    subset: str
    unicode_range: str
    remote_url: str = ""

    @property
    def filename(self) -> str:
        # A variable face answers with a weight RANGE ("200 800"); flatten it to a stable filename.
        weight = self.weight.replace(" ", "-") if " " in self.weight else self.weight
        return f"{self.slug}-{weight}-{self.style}-{self.subset}.woff2"


def _slugs() -> dict[str, str]:
    """slug → family, over both sources."""
    slugs = {slug: family for family, (slug, _axis) in FAMILIES.items()}
    slugs.update({slug: family for family, (slug, _pkg, _faces) in FONTSOURCE.items()})
    return slugs


def _curl(url: str, *, out: Path | None = None) -> bytes:
    cmd = ["curl", "-sSL", "--fail", "-A", USER_AGENT, url]
    if out is not None:
        cmd += ["-o", str(out)]
    result = subprocess.run(cmd, check=True, capture_output=True)  # noqa: S603 - fixed binary, controlled args
    return result.stdout


def fetch_css(family: str, axis: str) -> str:
    query = f"{CSS_API}?family={family.replace(' ', '+')}:{axis}&display=swap"
    return _curl(query).decode("utf-8")


def parse_faces(css: str, family: str, slug: str) -> list[Face]:
    faces: list[Face] = []
    for match in _BLOCK.finditer(css):
        subset = match.group("subset")
        if subset not in SUBSETS:
            continue
        props = {m.group("key"): m.group("value").strip() for m in _PROP.finditer(match.group("body"))}
        url_match = _URL.search(props.get("src", ""))
        if not url_match:
            continue
        faces.append(
            Face(
                family=family,
                slug=slug,
                style=props.get("font-style", "normal"),
                weight=props.get("font-weight", "400"),
                subset=subset,
                unicode_range=props.get("unicode-range", ""),
                remote_url=url_match.group("url").strip("'\""),
            )
        )
    return faces


def download(faces: list[Face]) -> None:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    for face in faces:
        target = FONT_DIR / face.filename
        if target.exists() and target.stat().st_size > 0:
            print(f"  = {face.filename} (cached)")
            continue
        _curl(face.remote_url, out=target)
        print(f"  + {face.filename} ({target.stat().st_size // 1024} KB)")


def copy_from_fontsource() -> list[Face]:
    """Copy the fontsource faces out of node_modules under our file names.

    Fontsource names its files ``{slug}-{subset}-{weight}-{style}.woff2``; ours put the subset
    last, which is what ``_FILENAME`` and the preload lines in ``templates/base.html`` expect.
    """
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    faces: list[Face] = []
    for family, (slug, package, wanted) in FONTSOURCE.items():
        files = NODE_MODULES / package / "files"
        if not files.is_dir():
            raise SystemExit(f"{package} is not installed: run `npm install` first (it is a devDependency)")
        print(f"{family} ({package}):")
        for weight, style in wanted:
            for subset in FONTSOURCE_SUBSETS:
                source = files / f"{slug}-{subset}-{weight}-{style}.woff2"
                if not source.exists():
                    raise SystemExit(f"{package} ships no {source.name}")
                face = Face(
                    family=family,
                    slug=slug,
                    style=style,
                    weight=weight,
                    subset=subset,
                    unicode_range=SUBSET_RANGES[subset],
                )
                target = FONT_DIR / face.filename
                if target.exists() and target.read_bytes() == source.read_bytes():
                    print(f"  = {face.filename} (identical)")
                else:
                    shutil.copyfile(source, target)
                    print(f"  + {face.filename} ({target.stat().st_size // 1024} KB)")
                faces.append(face)
    return faces


def write_css(faces: list[Face]) -> None:
    lines = [
        "/* ============================================================================",
        "   Self-hosted fonts (SIL OFL 1.1 for every family).",
        "   Generated by scripts/fetch_fonts.py — do not edit by hand.",
        "   Sources: Google Fonts CSS API subsets (Newsreader, Noto Naskh Arabic, IBM Plex Sans",
        "   Arabic) and the @fontsource packages (IBM Plex Sans, IBM Plex Mono — design V4).",
        "   Subsets: latin, latin-ext, arabic. font-display: swap. No external requests.",
        "   ========================================================================== */",
        "",
    ]

    def sort_key(face: Face) -> tuple:
        # A variable face declares a weight RANGE ("200 800"); sort on its lower bound.
        return (face.family, face.style, int(face.weight.split()[0]), face.subset)

    for face in sorted(faces, key=sort_key):
        lines += [
            f"/* {face.family} — {face.style} {face.weight} — {face.subset} */",
            "@font-face {",
            f'  font-family: "{face.family}";',
            f"  font-style: {face.style};",
            f"  font-weight: {face.weight};",
            "  font-display: swap;",
            f'  src: url("../fonts/{face.filename}") format("woff2");',
        ]
        if face.unicode_range:
            lines.append(f"  unicode-range: {face.unicode_range};")
        lines += ["}", ""]
    CSS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {CSS_FILE.relative_to(ROOT)} ({len(faces)} faces)")


def faces_from_disk() -> list[Face]:
    """Rebuild the face list from the files on disk (used by --css-only and after a fontsource
    copy). Unicode ranges are re-read from the existing fonts.css when present, else taken from
    the subset table."""
    ranges: dict[str, str] = {}
    if CSS_FILE.exists():
        current = CSS_FILE.read_text(encoding="utf-8")
        for block in re.finditer(r"@font-face\s*{(.*?)}", current, re.S):
            body = block.group(1)
            src = re.search(r'url\("\.\./fonts/([^"]+)"\)', body)
            rng = re.search(r"unicode-range:\s*([^;]+);", body)
            if src and rng:
                ranges[src.group(1)] = rng.group(1).strip()
    faces = []
    slugs = _slugs()
    for path in sorted(FONT_DIR.glob("*.woff2")):
        m = _FILENAME.match(path.name)
        if not m or m.group("slug") not in slugs:
            continue
        faces.append(
            Face(
                family=slugs[m.group("slug")],
                slug=m.group("slug"),
                style=m.group("style"),
                # a variable face was flattened to "200-800" on disk; declare it as the range
                weight=m.group("weight").replace("-", " "),
                subset=m.group("subset"),
                unicode_range=ranges.get(path.name) or SUBSET_RANGES.get(m.group("subset"), ""),
            )
        )
    return faces


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--css-only", action="store_true", help="only rewrite fonts.css from the files on disk")
    parser.add_argument(
        "--from-fontsource",
        action="store_true",
        help="copy the @fontsource families out of node_modules, then rewrite fonts.css from disk",
    )
    args = parser.parse_args(argv)

    if args.css_only:
        write_css(faces_from_disk())
        return 0
    if args.from_fontsource:
        copy_from_fontsource()
        write_css(faces_from_disk())
        return 0

    all_faces: list[Face] = []
    for family, (slug, axis) in FAMILIES.items():
        print(f"{family}:")
        css = fetch_css(family, axis)
        faces = parse_faces(css, family, slug)
        if not faces:
            print("  ! no matching @font-face blocks returned — check the user agent / network", file=sys.stderr)
            return 1
        download(faces)
        all_faces.extend(faces)
    all_faces.extend(copy_from_fontsource())
    write_css(all_faces)
    total = sum((FONT_DIR / f.filename).stat().st_size for f in all_faces)
    print(f"{len(all_faces)} files, {total // 1024} KB total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
