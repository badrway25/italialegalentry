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
#: RESTATED under V5.20 for the owner's FINAL HOMEPAGE ART-DIRECTION + TYPOGRAPHY PASS of 11 Nov 2026: the owner's
#: decision gives the home's statements an institutional serif, so the shipped set gains ONE face, «ILE Serif» (Source
#: Serif 4 400, opsz 48, renamed; docs/design-v5/FONTS_V5.md §1). The six files above, every per-file ceiling and the
#: six-file SET_CEILING stay as they were; the seventh file is held apart, at its measure (18 732 B), only down; it is
#: licensed (OFL-SourceSerif4.txt), read only under .page-home, never preloaded and Readex Pro on an Arabic run
#: (test_the_home_serif_is_the_seventh_file_licensed_home_only_never_preloaded below).
HOME_SERIF = "v5-ile-serif-400.woff2"
HOME_SERIF_CEILING = 18_732
#: Per-page encoded bytes the browser fetches: Latin public, Latin console, Arabic public, Arabic console — the
#: TYPOGRAPHY_V2 §4.7 letters 22 000 · 24 000 · 38 000 · 40 000. CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet —
#: the review's minor): measured in Chromium on v524-closing (headless; the woff2 resources' encoded bytes, as the two
#: browser tests read them; /fr/ /fr/parcours/ /fr/faq/ /fr/entreprises/ /fr/collaboration/institutions/
#: /fr/glossaire/ and their Arabic twins, a person's /espace-reserve/ in both) and recorded at the measure, only down:
#: a public page fetches Host Grotesk and the wordmark, an Arabic one Readex Pro too, a console page the mono as well.
PAGE_CEILINGS = {"latin_public": 20_956, "latin_console": 23_644, "arabic_public": 37_084, "arabic_console": 39_772}
#: RESTATED under V5.20 for the owner's FINAL HOMEPAGE ART-DIRECTION + TYPOGRAPHY PASS of 11 Nov 2026: the Latin HOME
#: alone draws the serif, so it has its own ceiling at its measure — the Latin public page's two files plus the serif
#: (19 208 + 1 748 + 18 732); PAGE_CEILINGS above, every other page's, unchanged (test_browser.py holds both)
HOME_LATIN_CEILING = 39_688


#: RESTATED under V5.20 for the owner's FINAL CLOSURE PASS of 12 Nov 2026: the font budget is ROUTE-AWARE
#: (docs/design-v5/FONTS_V5.md §1 bis, «Route-aware font budget (owner, 12 Nov 2026)») — two separate invariants and never
#: one sum: the SHARED set (the six files every route may fetch) under SET_CEILING with each per-file ceiling unchanged, and
#: the serif a declared HOMEPAGE-ONLY addition under its own file ceiling. Per route: the Latin home (fr, it, en) at its
#: measure, every other Latin public page at the shared figure and no serif, every Arabic page never the serif.
SHARED_FILES = (*FILE_CEILINGS, *MONO_FILES)
HOME_ONLY_FILES = {HOME_SERIF: HOME_SERIF_CEILING}
ROUTE_CEILINGS = {
    "home_latin": HOME_LATIN_CEILING,   # /fr/ /it/ /en/ — the shared files a public page draws, plus the serif
    "latin_public": PAGE_CEILINGS["latin_public"],   # every other Latin public page: never the serif
    "arabic_public": PAGE_CEILINGS["arabic_public"],   # every Arabic page, the home included: never the serif
}


def test_the_font_budget_is_route_aware_never_one_sum():
    """RESTATED under V5.20 for the owner's FINAL CLOSURE PASS of 12 Nov 2026 (stronger: the route-aware budget made
    explicit): the shared set's ceiling and every per-file ceiling are the CLOSING figures, unchanged; the serif is the one
    home-only file, under its own ceiling; no ceiling of the shared set, of a page or of the record covers the shared set and
    the serif together (the former «61 140 + 18 732» sum is gone from FONTS_V5.md); the home's route ceiling is exactly the
    Latin page's plus the serif's file, and no other route's ceiling moved."""
    assert SET_CEILING == 61_140 and FILE_CEILINGS == {
        "v5-host-grotesk-var-400-700.woff2": 19_208,
        "v5-host-grotesk-400-italic.woff2": 14_096,
        "v5-readex-pro-var-400-700-arabic.woff2": 16_128,
        "v5-ile-wordmark-600.woff2": 1_748,
    }
    assert HOME_ONLY_FILES == {"v5-ile-serif-400.woff2": 18_732} and HOME_SERIF not in SHARED_FILES
    assert PAGE_CEILINGS == {"latin_public": 20_956, "latin_console": 23_644, "arabic_public": 37_084, "arabic_console": 39_772}
    assert ROUTE_CEILINGS["home_latin"] == 39_688 == ROUTE_CEILINGS["latin_public"] + HOME_SERIF_CEILING
    assert max(ROUTE_CEILINGS.values()) < SET_CEILING, "a route fetches a part of the set, never the whole"
    combined = SET_CEILING + HOME_SERIF_CEILING
    doc = FONTS_DOC.read_text(encoding="utf-8")
    assert f"{combined:,}".replace(",", " ") not in doc and str(combined) not in doc, "no sum of the shared set and the serif"
    section = doc[doc.index("## 1 bis. Route-aware font budget (owner, 12 Nov 2026)") : doc.index("## 2. ")]
    for figure in ("61 140", "18 732", "39 688", "20 956", "37 084"):
        assert figure in section, figure
    for words in ("HOMEPAGE-ONLY", "its own owner decision", "never normalised"):
        assert words in section, words


def test_the_page_ceilings_stand_under_the_letters_of_typography_v2():
    assert PAGE_CEILINGS["latin_public"] <= 22_000 and PAGE_CEILINGS["latin_console"] <= 24_000
    assert PAGE_CEILINGS["arabic_public"] <= 38_000 and PAGE_CEILINGS["arabic_console"] <= 40_000
    # RESTATED (V5.31 art pass, above): the home's own ceiling is exactly the Latin page's plus the serif's file ceiling
    assert HOME_LATIN_CEILING == PAGE_CEILINGS["latin_public"] + HOME_SERIF_CEILING


def test_the_shipped_set_is_six_files_under_62_kb_and_each_file_under_its_ceiling():
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE ART-DIRECTION + TYPOGRAPHY PASS of 11 Nov 2026: the disk
    # holds the six files AND the home's serif — exactly those seven; the six keep every ceiling and SET_CEILING; the
    # serif has its own ceiling at its measure (HOME_SERIF above)
    files = {p.name: p.stat().st_size for p in FONTS.glob("*.woff2")}
    six = set(FILE_CEILINGS) | set(MONO_FILES)
    assert set(files) == six | {HOME_SERIF}, sorted(files)
    for name, ceiling in FILE_CEILINGS.items():
        assert files[name] <= ceiling, (name, files[name], ceiling)
    assert sum(files[name] for name in MONO_FILES) <= 9_960
    assert sum(files[name] for name in six) <= SET_CEILING, sum(files[name] for name in six)
    assert files[HOME_SERIF] <= HOME_SERIF_CEILING, (HOME_SERIF, files[HOME_SERIF], HOME_SERIF_CEILING)


def _uncommented(path: Path) -> str:
    return re.sub(r"/\*.*?\*/|\{% comment %\}.*?\{% endcomment %\}|\{#.*?#\}", "", path.read_text(encoding="utf-8"), flags=re.S)


def test_the_home_serif_is_the_seventh_file_licensed_home_only_never_preloaded():
    """RESTATED under V5.20 for the owner's FINAL HOMEPAGE ART-DIRECTION + TYPOGRAPHY PASS of 11 Nov 2026 (the seventh
    file's conditions): its OFL text travels with it and its Reserved Font Name «Source» is not the family's; one
    @font-face (400, swap, the Latin range); the role token is consumed by a rule whose every selector is under
    .page-home, and by no other rule of any source sheet; no template preloads it; on an Arabic run the role is Readex
    Pro and a Latin run inside it takes the serif back; FONTS_V5.md records its bytes and hash."""
    text = (FONTS / "licenses" / "OFL-SourceSerif4.txt").read_bytes()
    assert b"\r" not in text, "LF line ends"
    text = text.decode("utf-8")
    assert "Adobe" in text and "SIL OPEN FONT LICENSE Version 1.1" in text and "Reserved Font Name 'Source'" in text
    css = re.sub(r"/\*.*?\*/", "", FONTS_CSS.read_text(encoding="utf-8"), flags=re.S)
    faces = re.findall(r'@font-face\s*\{[^}]*font-family:\s*"ILE Serif";[^}]*\}', css)
    assert len(faces) == 1, faces
    face = faces[0]
    assert f'url("../../fonts/{HOME_SERIF}")' in face and "font-weight: 400;" in face and "font-display: swap" in face
    assert "unicode-range: U+0000-00FF" in face and "U+0600" not in face, "Latin only"
    assert 'font-family: "Source' not in css, "the Reserved Font Name is never a family"
    tokens = _uncommented(ROOT / "static" / "css" / "v5" / "tokens.css")
    assert re.search(r'--f-inst-lat:\s*"ILE Serif", Georgia, serif;', tokens)
    assert re.search(r":root:lang\(ar\), :lang\(ar\) \{[^}]*--f-display-inst: var\(--f-sans-ar\);", tokens), "Readex Pro in Arabic"
    assert re.search(r'\[lang="en"\]\) \{[^}]*--f-display-inst: var\(--f-inst-lat\);', tokens), "a Latin run takes it back"
    consumers = {}
    sheets = [p for p in (ROOT / "static" / "css").rglob("*.css") if "dist" not in p.parts]
    sheets += list((ROOT / "apps").glob("*/static/**/*.css"))
    for sheet in sheets:
        source = _uncommented(sheet)
        for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", source):
            if re.search(r"var\(--f-(?:display-inst|inst-lat)\)|ILE Serif", body) and not selector.strip().startswith(("@font-face", ":root", ":where(:root", "body")):
                consumers.setdefault(sheet.relative_to(ROOT).as_posix(), []).append(selector.strip())
    assert set(consumers) == {"static/css/v5/_home-a.css"}, consumers
    for selector in consumers["static/css/v5/_home-a.css"]:
        parts = [part.strip() for part in re.split(r",(?![^(]*\))", selector)]
        assert all(part.startswith(".page-home ") for part in parts), selector
    for template in (ROOT / "templates").rglob("*.html"):
        assert "ile-serif" not in template.read_text(encoding="utf-8"), f"{template}: the serif is never preloaded"
    # RESTATED under V5.20 for the owner's FINAL CLOSURE PASS of 12 Nov 2026 (stronger: the route-aware budget, held in
    # what the browser loads too): of the built bundles only main.css declares the face and the role (fonts.css, tokens.css:
    # every var() of the role there is the value of a role token), and only the home's pages.css consumes it
    dist = ROOT / "static" / "css" / "dist"
    carriers = {
        p.relative_to(dist).as_posix()
        for p in dist.rglob("*.css")
        if re.search(r"ILE Serif|--f-display-inst|--f-inst-lat", p.read_text(encoding="utf-8"))
    }
    assert carriers == {"main.css", "pages/css/pages.css"}, carriers
    main = (dist / "main.css").read_text(encoding="utf-8")
    uses = re.findall(r"([\w-]+):\s*var\(--f-(?:display-inst|inst-lat)\)", main)
    assert uses and set(uses) == {"--f-display-inst"}, uses
    doc = FONTS_DOC.read_text(encoding="utf-8")
    data = (FONTS / HOME_SERIF).read_bytes()
    assert hashlib.sha256(data).hexdigest() in doc and f"{len(data):,}".replace(",", " ") in doc
    assert "OFL-SourceSerif4.txt" in doc


def test_readex_pro_replaced_vazirmatn_with_its_licence():
    """TYPOGRAPHY_V2 §3 (the companion measured against Host Grotesk: content area 1.25 em, tooth 88 %, alef 106 %,
    half the bytes); the OFL text travels with the file; its Reserved Font Name is never used; no Vazirmatn file,
    licence, face or stack is left in the product's sources."""
    assert not list(FONTS.glob("*vazirmatn*")) and not (FONTS / "licenses" / "OFL-Vazirmatn.txt").exists()
    licences = {p.name for p in (FONTS / "licenses").glob("*.txt")}
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE ART-DIRECTION + TYPOGRAPHY PASS of 11 Nov 2026: the home's
    # serif adds its own OFL text — the set of licences is exact, one per family, and still no Vazirmatn
    assert licences == {"OFL-HostGrotesk.txt", "OFL-Newsreader.txt", "OFL-IBMPlexMono.txt", "OFL-ReadexPro.txt", "OFL-SourceSerif4.txt"}
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
