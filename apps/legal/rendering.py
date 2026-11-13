"""
The body of a legal document as blocks for the template — escaped text, never raw HTML from the database.

The grammar is the one the back office's help text gives (``## `` a section heading, a blank line between
paragraphs), plus what the privacy and cookie information need: ``### `` a sub-heading and ``- `` list items.
An open field «[DA COMPLETARE — …]» becomes ``<mark class="legal-open-field">`` so the owner sees what is missing;
it reaches a page only where open fields are allowed (the preview), since production never shows such a text.
The mark carries the marker's class (V5.16: ``data-open-field-class`` = production-config, owner-confirmation or
legal-review), and the marker's own words name it.
"""

from __future__ import annotations

from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe

from legal.models import OPEN_FIELD_CLASSES, OPEN_FIELD_RE, open_field_class


def _inline(text: str) -> SafeString:
    out: list[str] = []
    last = 0
    for match in OPEN_FIELD_RE.finditer(text):
        out.append(escape(text[last : match.start()]))
        slug = OPEN_FIELD_CLASSES.get(open_field_class(match.group(0)), "unclassified")  # V5.16: the class
        out.append(f'<mark class="legal-open-field" data-open-field data-open-field-class="{slug}">')
        out.append(f"{escape(match.group(0))}</mark>")
        last = match.end()
    out.append(escape(text[last:]))
    return mark_safe("".join(out))  # noqa: S308 - every piece above is escaped


def blocks(body: str) -> list[dict]:
    """[{"kind": "h2"|"h3"|"p"|"ul", "html": SafeString} | {"kind": "ul", "items": [SafeString]}]."""
    out: list[dict] = []
    for raw in body.replace("\r\n", "\n").split("\n\n"):
        block = raw.strip()
        if not block:
            continue
        if block.startswith("### "):
            out.append({"kind": "h3", "html": _inline(block[4:].strip())})
        elif block.startswith("## "):
            out.append({"kind": "h2", "html": _inline(block[3:].strip())})
        elif all(line.lstrip().startswith("- ") for line in block.splitlines()):
            items = [_inline(line.lstrip()[2:].strip()) for line in block.splitlines()]
            out.append({"kind": "ul", "items": items})
        else:
            out.append({"kind": "p", "html": _inline(" ".join(line.strip() for line in block.splitlines()))})
    return out
