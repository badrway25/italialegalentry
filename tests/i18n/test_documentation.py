"""
docs/I18N_RTL.md documents what exists: every cited path and test is real, the terminology table is the one
the catalogues apply, the cited screenshots are written by the browser suite, and the open defects (§9) match the
``xfail`` tests that keep those defects visible. No database needed.
"""

from __future__ import annotations

import re

import pytest

from .conftest import ROOT, TRANSLATED

pytestmark = pytest.mark.compliance

DOC = ROOT / "docs" / "I18N_RTL.md"
_DEFECT_ID = re.compile(r"\b(?:RTL|I18N)-\d{2}\b")


def _doc() -> str:
    return DOC.read_text(encoding="utf-8")


def _section(text: str, start: str, end: str | None = None) -> str:
    body = text.split(start, 1)[1]
    return body.split(end, 1)[0] if end else body


def _code_spans(text: str) -> list[str]:
    return re.findall(r"`([^`\n]+)`", re.sub(r"```.*?```", "", text, flags=re.S))


def test_document_has_the_required_sections():
    headings = re.findall(r"^## (\d+)\. (.+)$", _doc(), flags=re.M)
    assert [number for number, _title in headings] == [str(n) for n in range(1, 11)]
    titles = " | ".join(title for _number, title in headings)
    for needle in ("Architettura", "contenuti", "redazione", "sviluppo", "Glossario", "Plurali", "RTL", "Checklist"):
        assert needle in titles, needle


def test_cited_paths_exist():
    pattern = re.compile(r"^(?:templates|static|apps|tests|scripts|docs|config|locale)/[^\s*{}<>|]+$")
    cited = 0
    for span in _code_spans(_doc()):
        target = span.split("::", 1)[0]
        if target.startswith("docs/qa/") and target.endswith(".png"):
            continue  # git-ignored, absent from a fresh clone: test_cited_screenshots_are_produced_by_the_browser_suite
        if pattern.match(target) and "<" not in target:
            cited += 1
            assert (ROOT / target).exists(), f"docs/I18N_RTL.md cites a path that does not exist: {target}"
    assert cited >= 60, cited


def test_cited_tests_exist():
    cited = re.findall(r"`(tests/[a-z0-9_/]+\.py)::(test_[a-z0-9_]+)`", _doc())
    assert len(cited) >= 60, len(cited)
    for file_name, test_name in cited:
        source = (ROOT / file_name).read_text(encoding="utf-8")
        assert re.search(rf"^def {test_name}\(", source, flags=re.M), f"{file_name}::{test_name}"


def test_cited_screenshots_are_produced_by_the_browser_suite():
    """The PNG files are git-ignored (docs/qa/**/*.png): what is checked is that the suite writes those names."""
    from . import test_rtl_browser as browser_suite

    source = (ROOT / "tests" / "i18n" / "test_rtl_browser.py").read_text(encoding="utf-8")
    produced = {
        f"{page}-{lang}-{width}.png"
        for page in browser_suite.PAGES
        for lang in ("ar", "fr")
        for width in browser_suite.WIDTHS
    }
    produced |= set(re.findall(r'QA_DIR / "([a-z0-9-]+\.png)"', source))
    cited = set(re.findall(r"`(?:docs/qa/rtl/)?([a-z-]+-(?:ar|fr)-(?:390|1440)\.png)`", _doc()))
    assert cited, "the checklist cites its screenshots"
    assert cited <= produced, sorted(cited - produced)


def _glossary_rows() -> list[list[str]]:
    table = _section(_doc(), "## 5. Glossario terminologico", "\n---")
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in table.splitlines()
        if line.startswith("|") and not set(line) <= set("|- ")
    ]
    assert rows[0] == ["Français (source)", "Italiano", "English", "العربية"]
    return rows[1:]


def test_glossary_table_matches_the_catalogues(catalogues):
    rows = _glossary_rows()
    assert len(rows) >= 40, "the glossary documents about forty key interface terms"
    assert len({row[0] for row in rows}) == len(rows), "a French term is listed twice"
    for source, *expected in rows:
        for lang, value in zip(TRANSLATED, expected, strict=True):
            entry = catalogues[lang].get((None, source))
            assert entry is not None, f"« {source} » is not a msgid of locale/{lang}"
            assert entry.msgstr[0] == value, (lang, source, entry.msgstr[0], value)


def test_glossary_of_the_catalogue_tests_is_documented():
    from .test_catalogues import GLOSSARY

    documented = {row[0] for row in _glossary_rows()}
    assert set(GLOSSARY) <= documented, sorted(set(GLOSSARY) - documented)


def test_open_defects_match_the_xfail_tests():
    """§9 lists exactly the defects that an ``xfail`` test keeps visible (plus I18N-04, enforced by the audit)."""
    section = _section(_doc(), "## 9. Difetti aperti e limiti noti", "\nLimiti noti")
    documented = set(_DEFECT_ID.findall(section))
    in_tests: set[str] = set()
    for path in (ROOT / "tests" / "i18n").glob("test_*.py"):
        if path.name == "test_documentation.py":
            continue
        source = path.read_text(encoding="utf-8")
        for reason in re.findall(r"@pytest\.mark\.xfail\(\s*reason=\((.*?)\),\s*strict=", source, flags=re.S):
            ids = _DEFECT_ID.findall(reason)
            assert ids, f"{path.name}: an xfail reason must start with its defect id"
            in_tests.add(ids[0])
    # No xfail test is left when every defect of another owner has been fixed (second review, 20/09/2026).
    assert documented - {"I18N-04"} == in_tests, (sorted(documented - in_tests), sorted(in_tests - documented))
    for defect in sorted(documented):
        row = next(line for line in section.splitlines() if line.startswith(f"| {defect} |"))
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        assert len(cells) >= 6 and all(cells[:6]), f"{defect}: severity, defect, owner, fix and test are required"
        assert cells[1] in {"alta", "media", "bassa"}, defect


def test_the_xfail_reason_parser_reads_the_marker_layout_used_by_the_suite():
    """Guard of the guard: with no open defect left, prove the parser above still recognises a marker."""
    source = (
        '@pytest.mark.xfail(\n    reason=(\n        "RTL-42 (open, owner: design system): example "\n'
        '        "second line, see I18N-99."\n    ),\n    strict=False,\n)\ndef test_example():\n    pass\n'
    )
    reasons = re.findall(r"@pytest\.mark\.xfail\(\s*reason=\((.*?)\),\s*strict=", source, flags=re.S)
    assert len(reasons) == 1 and _DEFECT_ID.findall(reasons[0])[0] == "RTL-42"


def test_fixed_defects_are_documented_with_their_regression_test():
    fixed = _section(_doc(), "### 9.1 Difetti corretti", "\n---")
    rows = [line for line in fixed.splitlines() if _DEFECT_ID.match(line.lstrip("| "))]
    assert len(rows) >= 12
    for row in rows:
        cells = [cell.strip() for cell in row.strip().strip("|").split(" | ")]
        assert len(cells) == 3 and all(cells), row
        assert "`tests/i18n/" in cells[2], f"{cells[0][:8]}: a fixed defect names the test that protects the fix"
    open_section = _section(_doc(), "## 9. Difetti aperti e limiti noti", "\nLimiti noti")
    assert not set(_DEFECT_ID.findall(open_section)) & {_DEFECT_ID.match(r.lstrip("| ")).group(0) for r in rows}


def test_checklist_covers_the_required_items():
    checklist = _section(_doc(), "## 8. Checklist di verifica RTL", "## 9.")
    rows = [line for line in checklist.splitlines() if line.startswith("| ") and "`tests/" in line]
    assert len(rows) >= 16
    for item in (
        "Navigazione",
        "Drawer",
        "Breadcrumb",
        "Form",
        "Validazione",
        "Frecce",
        "Icone",
        "Accordion",
        "Card",
        "Tabelle",
        "Paginazione",
        "Modali",
        "Stepper",
        "Date",
        "Desktop 1440 / mobile 390",
    ):
        assert any(row.startswith(f"| {item}") for row in rows), item
