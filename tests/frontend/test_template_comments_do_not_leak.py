"""
No template ships its own commentary into the page.

Django's `{# … #}` is a SINGLE-LINE comment. Spanning it over several lines does not raise, does
not warn, and does not comment anything out: the `{#` is rendered as text, and so is every line
after it until the closing `#}`. The result is developer prose inside the `<head>` of a public
page, or above the warning on a legal pre-assessment.

Both of those happened in this project, a day apart, and neither was noticed by reading the
template — the mistake looks exactly like a comment. The first was found by opening the site in a
real Chrome window and reading the rendered source; the second by grepping for the same shape
immediately afterwards.

`{% comment %}` has no such trap, which is why it is the only form allowed over more than one line.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SHORT_COMMENT = re.compile(r"\{#")


def _templates() -> list[Path]:
    found = list((ROOT / "templates").rglob("*.html"))
    found += list((ROOT / "apps").rglob("templates/**/*.html"))
    assert len(found) > 50, f"only {len(found)} templates found; the glob is wrong"
    return found


def test_no_short_comment_spans_more_than_one_line():
    offenders: list[str] = []
    for path in _templates():
        text = path.read_text(encoding="utf-8")
        for match in SHORT_COMMENT.finditer(text):
            end_of_line = text.find("\n", match.start())
            segment = text[match.start() : end_of_line if end_of_line != -1 else len(text)]
            if "#}" not in segment:
                line = text.count("\n", 0, match.start()) + 1
                offenders.append(f"{path.relative_to(ROOT).as_posix()}:{line}")
    assert not offenders, (
        "`{# #}` opened and not closed on the same line — its text WILL render into the page. "
        "Use `{% comment %}`:\n  " + "\n  ".join(offenders)
    )


def test_the_rendered_head_of_the_home_page_carries_no_commentary(client, db):
    """
    The belt to the braces above: the shape check reads files, this one reads the OUTPUT.

    A different mistake — a comment inside a `{% verbatim %}`, an HTML comment holding notes — would
    slip past the regex and still reach the reader.
    """
    from django.urls import reverse

    html = client.get(reverse("pages:home")).content.decode()
    body_of_head = html[: html.find("</head>")]

    for giveaway in ("{#", "#}", "TODO", "FIXME", "XXX:"):
        assert giveaway not in body_of_head, f"{giveaway!r} reached the rendered head"

    # Prose that belongs in a code comment, recognisable because a page never addresses the reader
    # about its own implementation.
    for phrase in ("so Chrome stops", "the reader", "this project", "which is why"):
        assert phrase.lower() not in body_of_head.lower(), f"commentary in the head: {phrase!r}"
