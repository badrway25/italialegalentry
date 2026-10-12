"""
Every `.state` chip in the templates carries a `data-register`, and every register is one of six.

Phase 1b of the status chip (24 September 2026) converted 63 sites on 32 templates. The stylesheet
paints a chip without a register with a DOTTED rule — «unmapped», visible — which is the right
thing to do at runtime and the wrong thing to discover in production. This test finds the site in
CI instead: a `.state`, `.chip` or `.badge` written into a template must either carry a literal
`data-register="…"` with one of the six words, or compute one with `chip_register` /
`badge_register` on the same tag.

The check is on the SOURCE, tag by tag, because the templates render behind sessions and
fixtures that no single test can set up for all thirty-two of them.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from core import chips  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"

#: An opening tag whose class list contains one of the chip classes as a whole word.
CHIP_TAG = re.compile(
    r"<(?:span|a|button|p|div)\b[^>]*\bclass=\"[^\"]*\b(?:state|chip|badge)\b[^\"]*\"[^>]*>",
    re.IGNORECASE,
)
#: Classes that contain the word but are not chips.
NOT_A_CHIP = re.compile(r"\b(?:empty-state|desk-state|state-of|badge-list)\b")
LITERAL = re.compile(r'\bdata-register="(?P<word>[a-z]+)"')
COMPUTED = re.compile(r'\bdata-register="\{\{[^}]*\|(?:chip_register|badge_register)[^}]*\}\}"')
CONDITIONAL = re.compile(r"\{% if register %\} data-register=\"\{\{ register \}\}\"")
#: allauth's badge chooses its register with template tags inside the attribute:
#: data-register="{% if … %}conforme{% elif … %}azione{% else %}neutro{% endif %}". Every bare
#: word left once the tags are stripped must be a register.
TEMPLATED = re.compile(r'\bdata-register="(?P<body>[^"]*\{%[^"]*)"')
TAG = re.compile(r"\{%.*?%\}")


def chip_tags() -> list[tuple[str, str]]:
    found = []
    for path in sorted(TEMPLATES.rglob("*.html")):
        if path.relative_to(TEMPLATES).parts[0] == "dev":
            continue  # the dev-only showcase and preview write registers by hand to display them, including «none»
        text = path.read_text(encoding="utf-8")
        for match in CHIP_TAG.finditer(text):
            tag = match.group(0)
            if NOT_A_CHIP.search(tag):
                continue
            found.append((str(path.relative_to(ROOT)).replace("\\", "/"), tag))
    return found


TAGS = chip_tags()


def test_the_scan_sees_the_converted_sites():
    """A regex that matches nothing would pass every other test here for the wrong reason."""
    assert len(TAGS) >= 60, len(TAGS)


@pytest.mark.parametrize(("path", "tag"), TAGS, ids=[f"{p}:{i}" for i, (p, _) in enumerate(TAGS)])
def test_every_chip_tag_carries_a_register(path, tag):
    literal = LITERAL.search(tag)
    if literal:
        assert literal.group("word") in chips.REGISTERS, f"{path}: {literal.group('word')!r} is not a register"
        return
    templated = TEMPLATED.search(tag)
    if templated:
        words = TAG.sub(" ", templated.group("body")).split()
        assert words, f"{path}: templated data-register resolves to nothing"
        for word in words:
            assert word in chips.REGISTERS, f"{path}: {word!r} is not a register"
        return
    assert COMPUTED.search(tag) or CONDITIONAL.search(tag), f"{path}: chip without data-register — {tag[:120]}"


def test_computed_registers_name_a_known_producer():
    """`chip_register:'x.Y'` with a producer chips.py does not know returns "" — silently unmapped."""
    named = re.compile(r"chip_register:'([a-zA-Z_.]+)'")
    for path, tag in TAGS:
        for producer in named.findall(tag):
            assert producer in chips.REGISTER, f"{path}: unknown producer {producer!r}"
