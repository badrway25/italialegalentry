"""
Phase 3 prescribed texts must not be public before the Phase 3 gate opens (document: « PHASE 3 —
Après le 2 octobre 2026 »; master brief §6/§31).

Found by browser QA (2026-09-20): the orientation result page printed the Phase 3 pathway description
and the « Comment ça marche » paragraph while the gate was closed. This test renders every page that
is reachable with the gate closed and looks for any Phase 3 locked fragment.
"""

import html as html_module
import re

import pytest
from django.conf import settings

from cms import locked_content
from core.public_routes import ungated_paths

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

MIN_FRAGMENT = 28  # shorter strings (single words, button labels shared with Phase 1/2) are ignored
# Phase 3 keys whose wording is ALSO prescribed for an earlier phase or is a bare proper noun.
ALLOWED_EARLY = {
    "p3.hero.title",  # the trademark itself
    "p3.reserved.button",  # « CONNEXION » — generic UI word
}


def _fragments() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []

    def walk(key, value):
        if isinstance(value, str):
            text = re.sub(r"\s+", " ", value).strip()
            if len(text) >= MIN_FRAGMENT:
                out.append((key, text))
        elif isinstance(value, list):
            for item in value:
                walk(key, item)
        elif isinstance(value, dict):
            for name, item in value.items():
                if name != "key":
                    walk(key, item)

    earlier = {
        re.sub(r"\s+", " ", t).strip()
        for k, v in locked_content.LOCKED_TEXTS["fr"].items()
        if k.startswith(("p1.", "p2."))
        for t in ([v] if isinstance(v, str) else [x for x in v if isinstance(x, str)] if isinstance(v, list) else [])
    }
    for key, value in locked_content.LOCKED_TEXTS["fr"].items():
        if key.startswith("p3.") and key not in ALLOWED_EARLY:
            walk(key, value)
    return [(k, t) for k, t in out if t not in earlier]


def _visible_text(markup: str) -> str:
    markup = re.sub(r"<script\b.*?</script>", " ", markup, flags=re.S | re.I)
    markup = re.sub(r"<[^>]+>", " ", markup)
    return re.sub(r"\s+", " ", html_module.unescape(markup))


def _leaks(markup: str) -> list[str]:
    text = _visible_text(markup)
    return [key for key, fragment in _fragments() if fragment in text]


def test_there_are_phase3_fragments_to_look_for():
    assert len(_fragments()) > 40


@pytest.mark.parametrize("lang", [code for code, _ in settings.LANGUAGES])
def test_open_pages_show_no_phase3_prescribed_text_while_the_gate_is_closed(client, seeded, lang):
    offenders = {}
    for path in ungated_paths():
        response = client.get(f"/{lang}/{path}")
        if response.status_code != 200:
            continue
        found = _leaks(response.content.decode())
        if found:
            offenders[f"/{lang}/{path}"] = sorted(set(found))
    assert not offenders, offenders


def test_orientation_result_shows_no_phase3_text_while_the_gate_is_closed(client, seeded):
    start = client.post("/fr/orientation/", follow=True)
    url = start.request["PATH_INFO"]
    for _ in range(8):
        page = client.get(url)
        if "/resultat/" in page.request["PATH_INFO"] or page.status_code != 200:
            break
        markup = page.content.decode()
        match = re.search(r'name="answer" value="([^"]+)"', markup)
        question = re.search(r'name="question_key" value="([^"]+)"', markup)
        if not match or not question:
            break
        payload = {"action": "answer", "answer": match.group(1), "question_key": question.group(1)}
        response = client.post(url, payload, follow=True)
        url = response.request["PATH_INFO"]
        if "/resultat/" in url:
            assert not _leaks(response.content.decode()), _leaks(response.content.decode())
            return
    pytest.fail(f"the wizard did not reach a result page (stopped at {url})")
