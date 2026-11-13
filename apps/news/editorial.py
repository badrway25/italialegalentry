"""
Editorial plain-text markup and link-list validation shared by the CMS content apps
(news articles, "Vivre en Italie" sheets).

Editors never type HTML. The body is plain text where:

* paragraphs are separated by one or more blank lines;
* a line starting with ``## `` becomes an ``<h2>`` (``### `` → ``<h3>``);
* consecutive lines starting with ``- `` or ``* `` become a bulleted list.

``blocks()`` returns a list of ``(kind, payload)`` tuples that templates render with autoescape
on, so no editor input ever reaches the page unescaped. External links are only allowed as
plain anchors (``rel="noopener noreferrer"``) in the "sources" list — never as embedded
resources (CSP is self-only).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _

_BULLET = re.compile(r"^[-*]\s+")
_url_validator = URLValidator(schemes=["http", "https"])

MAX_LINK_LABEL = 160
MAX_LINKS = 20


@dataclass(frozen=True)
class Block:
    kind: str  # "h2" | "h3" | "p" | "ul"
    text: str = ""
    items: tuple[str, ...] = ()


def blocks(body: str) -> list[Block]:
    """Split editorial plain text into renderable blocks (see module docstring)."""
    out: list[Block] = []
    if not body:
        return out
    for raw in body.replace("\r\n", "\n").replace("\r", "\n").split("\n\n"):
        chunk = raw.strip()
        if not chunk:
            continue
        lines = [line.rstrip() for line in chunk.split("\n")]
        stripped = [line.strip() for line in lines if line.strip()]
        if not stripped:
            continue
        if len(stripped) == 1 and stripped[0].startswith("### "):
            out.append(Block("h3", stripped[0][4:].strip()))
        elif len(stripped) == 1 and stripped[0].startswith("## "):
            out.append(Block("h2", stripped[0][3:].strip()))
        elif all(_BULLET.match(line) for line in stripped):
            out.append(Block("ul", items=tuple(_BULLET.sub("", line).strip() for line in stripped)))
        else:
            out.append(Block("p", "\n".join(stripped)))
    return out


def plain_text(body: str, limit: int | None = None) -> str:
    """Flatten the markup to a single line (meta descriptions, search snippets)."""
    parts: list[str] = []
    for block in blocks(body):
        if block.kind == "ul":
            parts.extend(block.items)
        else:
            parts.append(block.text.replace("\n", " "))
    text = " ".join(p for p in parts if p).strip()
    if limit and len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def validate_link_list(value) -> None:
    """JSON list of ``{"label": str, "url": "https://…"}`` items (plain anchors only)."""
    if value in (None, ""):
        return
    if not isinstance(value, list):
        raise ValidationError(_("La liste de liens doit être un tableau JSON."))
    if len(value) > MAX_LINKS:
        raise ValidationError(_("Trop de liens (maximum %(max)d).") % {"max": MAX_LINKS})
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise ValidationError(_("Lien n°%(n)d : objet {label, url} attendu.") % {"n": index})
        label = item.get("label")
        url = item.get("url")
        if not isinstance(label, str) or not label.strip():
            raise ValidationError(_("Lien n°%(n)d : le libellé est obligatoire.") % {"n": index})
        if len(label) > MAX_LINK_LABEL:
            raise ValidationError(_("Lien n°%(n)d : libellé trop long.") % {"n": index})
        if not isinstance(url, str):
            raise ValidationError(_("Lien n°%(n)d : URL manquante.") % {"n": index})
        try:
            _url_validator(url.strip())
        except ValidationError as exc:
            raise ValidationError(_("Lien n°%(n)d : URL invalide (http/https uniquement).") % {"n": index}) from exc
        extra = set(item) - {"label", "url"}
        if extra:
            params = {"n": index, "keys": ", ".join(sorted(extra))}
            raise ValidationError(_("Lien n°%(n)d : clés non autorisées (%(keys)s).") % params)


def clean_link_list(value) -> list[dict[str, str]]:
    """Normalise a validated link list (strip whitespace, keep only label/url)."""
    validate_link_list(value)
    return [{"label": item["label"].strip(), "url": item["url"].strip()} for item in (value or [])]
