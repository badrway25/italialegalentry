"""
Reviewer tests — prescribed wording must never be hand-copied *in part*.

The builder's checks compare whole prescribed sentences. The review rule is stricter: any run of
six consecutive words of a prescribed French text found outside ``cms.locked_content`` is a
violation, and no run of six words that belongs to a Phase 3 text only may be public while gate G3
is closed (editorial copy, meta description and social tags included).
"""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

import pytest

from cms import locked_content

pytestmark = pytest.mark.compliance

ROOT = Path(__file__).resolve().parents[3]
APP_DIR = ROOT / "apps" / "pages"
TEMPLATE_DIR = ROOT / "templates" / "pages"
RUN = 6
_WORD = re.compile(r"[0-9a-zà-öø-ÿœ]+(?:[-'][0-9a-zà-öø-ÿœ]+)*")


def _words(text: str) -> list[str]:
    return _WORD.findall(text.lower().replace("’", "'"))


def _runs(text: str) -> set[str]:
    words = _words(text)
    return {" ".join(words[i : i + RUN]) for i in range(len(words) - RUN + 1)}


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for name, item in value.items():
            if name != "key":  # technical identifiers are not prescribed wording
                yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def _prescribed_runs(prefixes: tuple[str, ...]) -> dict[str, str]:
    runs: dict[str, str] = {}
    for key, value in locked_content.LOCKED_TEXTS["fr"].items():
        if key.startswith(prefixes):
            for text in _strings(value):
                for run in _runs(text):
                    runs.setdefault(run, key)
    return runs


def _sources() -> list[Path]:
    files = [p for p in APP_DIR.rglob("*") if p.suffix in {".py", ".js", ".css"}]
    files = [p for p in files if "tests" not in p.parts and "migrations" not in p.parts]
    return sorted(files + list(TEMPLATE_DIR.rglob("*.html")))


def test_sources_are_found():
    names = {p.name for p in _sources()}
    assert {"content.py", "services.py", "home.html", "contact.html", "pages.css"} <= names


@pytest.mark.parametrize("path", _sources(), ids=lambda p: p.relative_to(ROOT).as_posix())
def test_no_six_word_fragment_of_a_prescribed_text_in_the_sources(path):
    prescribed = _prescribed_runs(("p1.", "p2.", "p3.", "legal."))
    found = {run: prescribed[run] for run in _runs(path.read_text(encoding="utf-8")) if run in prescribed}
    assert found == {}, f"{path.name}: prescribed wording must come from the locked registry: {found}"


def _public_text(html: str) -> str:
    """Everything a visitor or a crawler reads: <main> text, <title>, meta descriptions, social tags."""
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    main = re.sub(r"<(script|style)\b.*?</\1>", " ", main, flags=re.S)
    head = " ".join(re.findall(r'<meta [^>]*content="([^"]*)"', html) + re.findall(r"<title>(.*?)</title>", html, re.S))
    return html_lib.unescape(re.sub(r"<[^>]+>", " ", main) + " " + head)


@pytest.mark.django_db
@pytest.mark.parametrize("path", ["", "le-projet/", "agami/", "reseau/", "contact/"])
def test_no_phase3_fragment_is_public_while_gate_closed(client, seeded, path):
    already_public = _prescribed_runs(("p1.", "p2."))
    phase3_only = {run: key for run, key in _prescribed_runs(("p3.",)).items() if run not in already_public}
    response = client.get(f"/fr/{path}")
    assert response.status_code == 200
    leaked = {run: phase3_only[run] for run in _runs(_public_text(response.content.decode())) if run in phase3_only}
    assert leaked == {}, f"/fr/{path}: Phase 3 wording published before the gate: {leaked}"


@pytest.mark.django_db
def test_phase3_fragment_detector_sees_the_open_homepage(client, seeded, phase3_open):
    """Guard against a blind detector: once the gate is open the same scan must find Phase 3 wording."""
    phase3 = _prescribed_runs(("p3.",))
    html = client.get("/fr/").content.decode()
    assert any(run in phase3 for run in _runs(_public_text(html)))
