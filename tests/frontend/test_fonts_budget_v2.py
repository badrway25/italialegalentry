"""
Typography V2 — the font budget (v524-t; TYPOGRAPHY_V2 §4.6–§4.7; FINAL_DELIVERY_V2 R4 g, §3.1).

The shipped set and each file under its ceiling; Readex Pro in Vazirmatn's place, with its licence; the record
(docs/design-v5/FONTS_V5.md) in step with the files — the bytes and hashes are held by
tests/frontend/test_v5_tokens.py::test_fonts_v5_md_records_every_shipped_face_with_its_bytes_and_hash; the per-page
fetched bytes by the two browser tests (tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded,
tests/i18n/test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded). Every ceiling is UNDER the figure of
the previous system (set 77 240 B; a Latin public page 20 956–30 916 B; an Arabic one 53 184–63 144 B): a ceiling is
never raised (V5.20; FINAL_DELIVERY_V2 R4 — CLOSING ratchets each to its measure).
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "static" / "fonts"
FONTS_CSS = ROOT / "static" / "css" / "v5" / "fonts.css"
FONTS_DOC = ROOT / "docs" / "design-v5" / "FONTS_V5.md"

pytestmark = pytest.mark.compliance

#: Per-file ceilings (TYPOGRAPHY_V2 §4.7): variable sans ≤ 22 KB, italic ≤ 15 KB, Arabic ≤ 18 KB, the two mono files
#: ≤ 10 KB together, the wordmark ≤ 2 KB; the set ≤ 62 000 B (61 140 measured).
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet): the values below recorded at their measure on v524-closing — only down.
FILE_CEILINGS = {
    "v5-host-grotesk-var-400-700.woff2": 19_208,
    "v5-host-grotesk-400-italic.woff2": 14_096,
    "v5-readex-pro-var-400-700-arabic.woff2": 16_128,
    "v5-ile-wordmark-600.woff2": 1_748,
}
MONO_FILES = ("v5-ile-mono-400.woff2", "v5-ile-mono-400-ext.woff2")
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet): the values below recorded at their measure on v524-closing — only down.
SET_CEILING = 61_140
#: Per-page encoded bytes the browser fetches: Latin public, Latin console, Arabic public, Arabic console — the
#: TYPOGRAPHY_V2 §4.7 letters 22 000 · 24 000 · 38 000 · 40 000. CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet —
#: the review's minor): measured in Chromium on v524-closing (headless; the woff2 resources' encoded bytes, as the two
#: browser tests read them; /fr/ /fr/parcours/ /fr/faq/ /fr/entreprises/ /fr/collaboration/institutions/
#: /fr/glossaire/ and their Arabic twins, a person's /espace-reserve/ in both) and recorded at the measure, only down:
#: a public page fetches Host Grotesk and the wordmark, an Arabic one Readex Pro too, a console page the mono as well.
PAGE_CEILINGS = {"latin_public": 20_956, "latin_console": 23_644, "arabic_public": 37_084, "arabic_console": 39_772}


def test_the_page_ceilings_stand_under_the_letters_of_typography_v2():
    assert PAGE_CEILINGS["latin_public"] <= 22_000 and PAGE_CEILINGS["latin_console"] <= 24_000
    assert PAGE_CEILINGS["arabic_public"] <= 38_000 and PAGE_CEILINGS["arabic_console"] <= 40_000


def test_the_shipped_set_is_six_files_under_62_kb_and_each_file_under_its_ceiling():
    files = {p.name: p.stat().st_size for p in FONTS.glob("*.woff2")}
    assert set(files) == set(FILE_CEILINGS) | set(MONO_FILES), sorted(files)
    for name, ceiling in FILE_CEILINGS.items():
        assert files[name] <= ceiling, (name, files[name], ceiling)
    assert sum(files[name] for name in MONO_FILES) <= 9_960
    assert sum(files.values()) <= SET_CEILING, sum(files.values())


def test_readex_pro_replaced_vazirmatn_with_its_licence():
    """TYPOGRAPHY_V2 §3 (the companion measured against Host Grotesk: content area 1.25 em, tooth 88 %, alef 106 %,
    half the bytes); the OFL text travels with the file; its Reserved Font Name is never used; no Vazirmatn file,
    licence, face or stack is left in the product's sources."""
    assert not list(FONTS.glob("*vazirmatn*")) and not (FONTS / "licenses" / "OFL-Vazirmatn.txt").exists()
    licences = {p.name for p in (FONTS / "licenses").glob("*.txt")}
    assert licences == {"OFL-HostGrotesk.txt", "OFL-Newsreader.txt", "OFL-IBMPlexMono.txt", "OFL-ReadexPro.txt"}
    text = (FONTS / "licenses" / "OFL-ReadexPro.txt").read_bytes()
    assert b"\r" not in text, "LF line ends"
    text = text.decode("utf-8")
    assert "The Readex Pro Project Authors" in text and "SIL OPEN FONT LICENSE Version 1.1" in text
    assert "RevReading Lexend" in text, "the Reserved Font Name is declared in the licence and never used by the file"
    css = re.sub(r"/\*.*?\*/", "", FONTS_CSS.read_text(encoding="utf-8"), flags=re.S)
    face = re.search(r'@font-face\s*\{[^}]*font-family:\s*"Readex Pro";[^}]*\}', css)
    assert face, "no Readex Pro face"
    assert "font-weight: 400 700" in face.group(0) and "font-display: swap" in face.group(0)
    assert 'url("../../fonts/v5-readex-pro-var-400-700-arabic.woff2")' in face.group(0)
    assert "U+0020, U+00A0, U+0600-06FF" in face.group(0), "the file's own spaces, then the Arabic blocks"
    assert "Vazirmatn" not in css
    for source in (
        ROOT / "static" / "css" / "v5" / "tokens.css",
        ROOT / "templates" / "base.html",
        ROOT / "templates" / "errors" / "standalone.html",
    ):
        assert "azirmatn" not in re.sub(
            r"/\*.*?\*/|\{% comment %\}.*?\{% endcomment %\}", "", source.read_text(encoding="utf-8"), flags=re.S
        ), source


#: WOFF2's known-table index (the specification's table of 63 tags; 63 = an arbitrary tag follows).
_WOFF2_TAGS = (
    "cmap head hhea hmtx maxp name OS/2 post cvt  fpgm glyf loca prep CFF  VORG EBDT EBLC gasp hdmx kern LTSH PCLT VDMX "
    "vhea vmtx BASE GDEF GPOS GSUB EBSC JSTF MATH CBDT CBLC COLR CPAL SVG  sbix acnt avar bdat bloc bsln cvar fdsc feat "
    "fmtx fvar gvar hsty just lcar mort morx opbd prop trak Zapf Silf Glat Gloc Feat Sill"
)
_WOFF2_KNOWN = [
    _WOFF2_TAGS[i : i + 5].rstrip() if i + 5 <= len(_WOFF2_TAGS) else _WOFF2_TAGS[i:] for i in range(0, 63 * 5, 5)
]


def _woff2_tables(data: bytes) -> tuple[str, int, list[str]]:
    """(flavor, numTables, table tags) of a WOFF2 file, read from its header and table directory — no decompression:
    the directory's tags, flags and Base128 lengths precede the brotli stream."""
    assert data[:4] == b"wOF2", "not a WOFF2 file"
    flavor = {"00010000": "TrueType", "4f54544f": "CFF"}.get(data[4:8].hex(), data[4:8].hex())
    num_tables = int.from_bytes(data[12:14], "big")
    offset = 48

    def base128() -> int:
        nonlocal offset
        value = 0
        for _ in range(5):
            byte = data[offset]
            offset += 1
            value = (value << 7) | (byte & 0x7F)
            if not byte & 0x80:
                return value
        raise AssertionError("UIntBase128 longer than five bytes")

    tags = []
    for _ in range(num_tables):
        flags = data[offset]
        offset += 1
        index = flags & 0x3F
        if index == 63:
            tag = data[offset : offset + 4].decode("latin-1")
            offset += 4
        else:
            tag = _WOFF2_KNOWN[index]
        transform = (flags >> 6) & 3
        base128()  # origLength
        if (tag in ("glyf", "loca") and transform == 0) or (tag not in ("glyf", "loca") and transform != 0):
            base128()  # transformLength
        tags.append(tag.rstrip())
    return flavor, num_tables, tags


def test_the_woff2_is_a_variable_shaped_unhinted_subset():
    """What the file's own directory says (the project's test venv carries neither fontTools nor brotli, so the cmap,
    name and axis facts — the Arabic blocks and the two spaces only, never the digits or the Latin; «Readex Pro»,
    1.205; wght 400–700 — are the build tool's guards, `build_v5_fonts.py` READEX, pinned here by the file's SHA-256 that
    FONTS_V5 §1 records and test_v5_tokens.py checks): a TrueType-flavoured WOFF2 with the variation table (fvar: one
    file for 400–700), the shaping tables (GSUB for init/medi/fina/rlig, GPOS for mark/mkmk), the cmap, the name — and
    no hinting program (fpgm, prep, cvt: `hinting = False`)."""
    data = (FONTS / "v5-readex-pro-var-400-700-arabic.woff2").read_bytes()
    flavor, num_tables, tags = _woff2_tables(data)
    assert flavor == "TrueType" and num_tables == len(tags), (flavor, num_tables, len(tags))
    for required in ("fvar", "gvar", "GSUB", "GPOS", "GDEF", "cmap", "name", "glyf", "loca", "OS/2", "hhea", "hmtx"):
        assert required in tags, (required, tags)
    for hinting in ("fpgm", "prep", "cvt"):
        assert hinting not in tags, (hinting, tags)
    assert "STAT" in tags or "fvar" in tags
    digest = hashlib.sha256(data).hexdigest()
    assert digest in FONTS_DOC.read_text(encoding="utf-8"), "the file is not the one FONTS_V5 §1 records"
    # the same directory facts for the Latin variable face: one build discipline for both scripts
    _flavor, _n, host = _woff2_tables((FONTS / "v5-host-grotesk-var-400-700.woff2").read_bytes())
    assert "fvar" in host and "fpgm" not in host


def test_fonts_v5_md_states_the_ceilings_and_the_metric_fallback_of_readex_pro():
    """The record names the new face, the ceilings of §4.7 and the recomputed ILE Arabic Fallback; the SHA-256 of the
    Readex Pro file in §1 is the file's (the full table is test_v5_tokens.py's)."""
    doc = FONTS_DOC.read_text(encoding="utf-8")
    assert "Readex Pro" in doc and "OFL-ReadexPro.txt" in doc
    digest = hashlib.sha256((FONTS / "v5-readex-pro-var-400-700-arabic.woff2").read_bytes()).hexdigest()
    assert digest in doc
    for figure in ("62 000", "22 000", "24 000", "38 000", "40 000"):
        assert figure in doc, figure
    css = FONTS_CSS.read_text(encoding="utf-8")
    fallback = re.search(
        r'font-family: "ILE Arabic Fallback";[^}]*size-adjust: ([0-9.]+)%;[^}]*ascent-override: ([0-9.]+)%;[^}]*descent-override: ([0-9.]+)%',
        css,
    )
    assert fallback
    for value in fallback.groups():
        assert f"{value} %" in doc or f"{value}%" in doc, value
