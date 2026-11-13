"""
What this module must never become.

The previous platform's help function was a third-party language model behind a button that offered
to answer «tout sur les visas proposés, les documents à fournir», with its API key as the whole of
the administration screen (previous-platform audit, part 2 §7, private register). The brief for this vertical
is one sentence: build the opposite, and let nothing here resemble it.

A rule that is only written in a document is a rule that comes back. These tests read the source of
the module and of its templates, so the prohibition survives whoever edits it next.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from helpdesk.models import TicketStatus

APP = Path(__file__).resolve().parent.parent
TEMPLATES = APP.parent.parent / "templates" / "helpdesk"


def _sources() -> list[tuple[Path, str]]:
    files = [p for p in APP.rglob("*.py") if "migrations" not in p.parts]
    files += list(APP.rglob("*.css"))
    files += list(TEMPLATES.rglob("*.html"))
    return [(p, p.read_text(encoding="utf-8")) for p in files]


def _sources_excluding_tests() -> list[tuple[Path, str]]:
    return [(p, text) for p, text in _sources() if "tests" not in p.parts]


# ---------------------------------------------------------------------------------------------
# No chatbot, no generated answer, no third-party model, no key
# ---------------------------------------------------------------------------------------------
#: Each pattern is a thing the previous platform actually had, or the name of the thing that would
#: bring it back. ``assistant`` is included because that is the exact word on the old button.
FORBIDDEN = {
    "chatbot": r"chat\s*bot|chatbot",
    "an assistant button": r"\bassistant\b",
    "a third-party model vendor": r"openai|anthropic|mistral|gemini|huggingface|deepseek",
    "a model API key": r"api[_\- ]?key|apikey|secret[_\- ]?key",
    "a prompt": r"\bprompt\b",
    "a completion or generated answer": r"completion|generated_answer|autoreply|auto_reply",
    "a language model": r"\bllm\b|language model|modèle de langage|intelligence artificielle",
}


@pytest.mark.parametrize(("label", "pattern"), sorted(FORBIDDEN.items()))
def test_the_module_contains_nothing_that_answers_by_itself(label, pattern):
    regex = re.compile(pattern, re.IGNORECASE)
    offenders = []
    for path, text in _sources_excluding_tests():
        # The module docstrings NAME the thing they forbid; a comment saying "no chatbot" is the
        # opposite of a chatbot. Only live code and rendered text are scanned.
        stripped = re.sub(r'""".*?"""', "", text, flags=re.DOTALL)
        stripped = re.sub(r"{%\s*comment\s*%}.*?{%\s*endcomment\s*%}", "", stripped, flags=re.DOTALL)
        stripped = re.sub(r"^\s*#.*$", "", stripped, flags=re.MULTILINE)
        stripped = re.sub(r"/\*.*?\*/", "", stripped, flags=re.DOTALL)
        if regex.search(stripped):
            offenders.append(str(path))
    assert offenders == [], f"{label} found in: {offenders}"


def test_the_module_never_imports_a_network_client():
    for path, text in _sources_excluding_tests():
        if path.suffix != ".py":
            continue
        assert not re.search(r"^\s*import\s+(requests|httpx|urllib|socket)\b", text, re.MULTILINE), path
        assert not re.search(r"^\s*from\s+(requests|httpx|urllib|socket)\b", text, re.MULTILINE), path


def test_no_setting_of_this_module_holds_a_secret():
    """The previous platform's single administrable setting was a model key. There is none here."""
    for path, text in _sources_excluding_tests():
        assert "getattr(settings, " not in text or "NOTIFICATIONS" in text or "DEBUG" in text, path


# ---------------------------------------------------------------------------------------------
# Nothing approves anybody, nothing promises anything
# ---------------------------------------------------------------------------------------------
#: Words a person would read as an administrative determination. ``éligible`` is absent from the
#: domain by decision (CONFLICT_REGISTER CR-11) and must stay absent from the interface.
APPROVAL_WORDS = (
    r"approuvé",
    r"approuvée",
    r"éligible",
    r"admissible",
    r"idoneo",
    r"ammissibile",
    r"vous avez droit",
    r"visa accordé",
    r"garantit un",
    r"nous garantissons",
)


@pytest.mark.parametrize("word", APPROVAL_WORDS)
def test_no_word_reads_as_an_approval(word):
    regex = re.compile(word, re.IGNORECASE)
    offenders = [str(path) for path, text in _sources_excluding_tests() if regex.search(text)]
    assert offenders == [], f"«{word}» found in: {offenders}"


def test_the_states_are_exactly_the_seven_of_the_blueprint():
    assert set(TicketStatus.values) == {
        "information_only",
        "needs_clarification",
        "professional_review_required",
        "assigned",
        "in_review",
        "response_available",
        "closed",
    }


# ---------------------------------------------------------------------------------------------
# No recruitment language, no age
# ---------------------------------------------------------------------------------------------
RECRUITMENT_WORDS = (
    r"recrutement",
    r"recruter",
    r"\bmatching\b",
    r"offre d.emploi",
    r"candidat",
    r"postuler",
    r"CV\b",
)


@pytest.mark.parametrize("word", RECRUITMENT_WORDS)
def test_no_recruitment_language(word):
    regex = re.compile(word, re.IGNORECASE)
    offenders = [str(path) for path, text in _sources_excluding_tests() if regex.search(text)]
    assert offenders == [], f"«{word}» found in: {offenders}"


def test_age_is_never_collected_or_shown():
    """Directive 2000/78/EC and D.lgs. 216/2003: age is never a criterion, so it is never a field."""
    for path, text in _sources_excluding_tests():
        assert not re.search(r"\bage\b|\bâge\b|date_of_birth|birth_date|tranche d.âge", text, re.IGNORECASE), path


# ---------------------------------------------------------------------------------------------
# The design discipline of art direction A
# ---------------------------------------------------------------------------------------------
FORBIDDEN_CSS = {
    "a box shadow on content": r"box-shadow\s*:\s*(?!none)",
    "a radius above 2px": r"border-radius\s*:\s*(?!0|2px|50%)",
    "a decorative gradient": r"linear-gradient|radial-gradient",
    "a hard-coded colour outside the tokens": r"#[0-9a-fA-F]{3,8}\b|rgba?\(",
}


@pytest.mark.parametrize(("label", "pattern"), sorted(FORBIDDEN_CSS.items()))
def test_the_stylesheet_stays_inside_the_design_system(label, pattern):
    css = (APP / "static" / "helpdesk" / "helpdesk.css").read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    assert not re.search(pattern, css), label


def test_the_templates_use_the_register_and_never_a_card():
    for path in TEMPLATES.rglob("*.html"):
        raw = path.read_text(encoding="utf-8")
        text = re.sub(r"{%\s*comment\s*%}.*?{%\s*endcomment\s*%}", "", raw, flags=re.DOTALL)
        assert 'class="card' not in text, path
        assert "empty_state.html" not in text, path
        assert "portal-card" not in text, path


def test_every_page_sits_on_the_platform_shell():
    for path in TEMPLATES.rglob("*.html"):
        if path.parent.name == "partials":
            # a fragment drawn inside a page (the closure's dialog, design V5 W3-E), never a page of its own
            continue
        text = path.read_text(encoding="utf-8")
        if path.name == "base_helpdesk.html":
            assert 'extends "portal/base_portal.html"' in text
        else:
            assert 'extends "helpdesk/base_helpdesk.html"' in text, path
