"""Helpers shared by the i18n test-suite (``tests/i18n``)."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

LANGS = ("it", "fr", "en", "ar")
TRANSLATED = ("it", "en", "ar")


def region(html: str, tag: str) -> str:
    """The first ``<tag>…</tag>`` region of a page (``header``, ``footer``, ``main``, ``nav``)."""
    match = re.search(rf"<{tag}\b.*?</{tag}>", html, re.S)
    return match.group(0) if match else ""


def text_nodes(html: str) -> list[str]:
    """Visible text nodes of an HTML fragment, in document order (SVG, scripts and styles dropped)."""
    html = re.sub(r"<(svg|script|style)\b.*?</\1>", "", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    return [node.strip() for node in re.sub(r"<[^>]+>", "\n", html).split("\n") if node.strip()]


def html_tag(html: str) -> str:
    match = re.search(r"<html\b[^>]*>", html)
    return match.group(0) if match else ""


@pytest.fixture(scope="session")
def audit():
    """The ``scripts/i18n_audit.py`` module (PO parser, source scanner, locked-text index)."""
    import i18n_audit

    return i18n_audit


@pytest.fixture(scope="session")
def catalogues(audit):
    """``{lang: {(msgctxt, msgid): Entry}}`` for the three translated catalogues."""
    return {
        lang: {
            (entry.msgctxt, entry.msgid): entry
            for entry in audit.parse_po(audit.po_path(lang))
            if not entry.obsolete and not entry.is_header
        }
        for lang in TRANSLATED
    }


# ---------------------------------------------------------------------------------------------
# Language-aware page reader (whole-site guards, tests/i18n/test_page_integrity.py)
# ---------------------------------------------------------------------------------------------
_VOID_TAGS = frozenset(
    {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
)
#: Attributes read aloud or shown to the visitor: they must be in the language of their element.
_READABLE_ATTRIBUTES = ("aria-label", "title", "placeholder", "alt")


class _PageWalker(HTMLParser):
    """Collect the visible strings of a page together with the language that applies to each of them."""

    def __init__(self, page_lang: str) -> None:
        super().__init__(convert_charrefs=True)
        self.page_lang = page_lang
        self.stack: list[tuple[str, str]] = []
        self.hidden = 0
        self.strings: list[tuple[str, str, str]] = []  # (effective language, kind, text)

    def _language(self) -> str:
        for _tag, lang in reversed(self.stack):
            if lang:
                return lang
        return self.page_lang

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag in ("script", "style", "svg"):
            self.hidden += 1
        lang = (attributes.get("lang") or "").split("-")[0]
        if tag not in _VOID_TAGS:
            self.stack.append((tag, lang))
        if self.hidden:
            return
        effective = lang or self._language()
        for name in _READABLE_ATTRIBUTES:
            if attributes.get(name):
                self.strings.append((effective, f"@{name}", attributes[name].strip()))
        if tag == "input" and attributes.get("type") in ("submit", "button") and attributes.get("value"):
            self.strings.append((effective, "@value", attributes["value"].strip()))
        if tag == "meta" and attributes.get("name") == "description":
            self.strings.append((effective, "@description", (attributes.get("content") or "").strip()))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in _VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg") and self.hidden:
            self.hidden -= 1
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        text = " ".join(data.split())
        if text and not self.hidden:
            self.strings.append((self._language(), self.stack[-1][0] if self.stack else "#root", text))


def visible_strings(html: str, page_lang: str) -> list[tuple[str, str, str]]:
    """
    ``[(language, kind, text), …]`` for every text node and human-readable attribute of a page, where
    ``language`` is the ``lang`` that applies to the string (nearest ancestor, else the page language)
    and ``kind`` is the parent tag or ``@attribute``. SVG, scripts and styles are skipped.
    """
    walker = _PageWalker(page_lang)
    walker.feed(html)
    walker.close()
    return walker.strings


# ---------------------------------------------------------------------------------------------
# « Language of parts » reader (WCAG 3.1.2) — tests/i18n/test_page_integrity.py
# ---------------------------------------------------------------------------------------------
class _PartsWalker(_PageWalker):
    """Same walk as ``_PageWalker``, but every string also carries the CSS classes of its ancestors."""

    def __init__(self, page_lang: str) -> None:
        super().__init__(page_lang)
        self.classes: list[tuple[str, tuple[str, ...]]] = []
        self.located: list[tuple[str, str, str, tuple[str, ...]]] = []  # (language, kind, text, ancestor classes)

    def _chain(self) -> tuple[str, ...]:
        return tuple(name for _tag, names in self.classes for name in names)

    def handle_starttag(self, tag, attrs):
        before = len(self.strings)
        names = tuple((dict(attrs).get("class") or "").split())
        if tag not in _VOID_TAGS:
            self.classes.append((tag, names))
        super().handle_starttag(tag, attrs)
        chain = self._chain() if tag not in _VOID_TAGS else (*self._chain(), *names)
        self.located += [(*item, chain) for item in self.strings[before:]]

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        for index in range(len(self.classes) - 1, -1, -1):
            if self.classes[index][0] == tag:
                del self.classes[index:]
                break

    def handle_data(self, data):
        before = len(self.strings)
        super().handle_data(data)
        self.located += [(*item, self._chain()) for item in self.strings[before:]]


def located_strings(html: str, page_lang: str) -> list[tuple[str, str, str, tuple[str, ...]]]:
    """``visible_strings`` plus, for each string, the CSS classes of the elements that contain it."""
    walker = _PartsWalker(page_lang)
    walker.feed(html)
    walker.close()
    return walker.located
