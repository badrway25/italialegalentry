"""
The locked-copy cuts of V5.22 (SECTION_SYSTEM_V2 §1 rule 6, §2.0 «Data»; lane S): a prescribed text set in several
levels is sliced on its own separators, and the slices rebuild it character for character — or there is no cut and the
text stands whole. Every cut a V2 section uses on a real locked text is asserted here against the registry itself.
"""

from __future__ import annotations

import html
import re

import pytest
from django.template import Context, Template

from cms import locked_content, locked_split


def _text_content(markup: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", str(markup)))


def test_a_sentence_cut_keeps_every_character_and_its_full_stop():
    text = "Une phrase. Une autre ? Et la troisième !"
    parts = locked_split.sentences(text)
    assert parts == ("Une phrase. ", "Une autre ? ", "Et la troisième !")
    assert "".join(parts) == text


def test_one_sentence_is_not_cut():
    assert locked_split.sentences("Une seule phrase.") is None
    assert locked_split.first_clause("Sans virgule") is None
    assert locked_split.split("Sans deux-points", ":") is None


def test_the_separator_stays_with_the_part_it_closes():
    assert locked_split.split("Destinataires : Régions, Communes", ":") == ("Destinataires : ", "Régions, Communes")
    assert locked_split.split("a ; b ; c", ";") == ("a ; ", "b ; ", "c")
    assert locked_split.split("A → B → C", "→") == ("A →", " B →", " C")
    assert locked_split.first_clause("Qui sommes-nous, et pourquoi.") == ("Qui sommes-nous, ", "et pourquoi.")
    with pytest.raises(ValueError):
        locked_split.split("x", "|")


@pytest.mark.parametrize(
    "key, mode, count",
    [
        ("p3.antifraud.body", "sentence", 4),  # «la protezione»: sentence 1 larger, 2–3 body, 4 behind a rule
        ("p3.institutions.recipients", ":", 2),  # «l'emiciclo»: «Destinataires :» stays the sentence's own head
        ("p3.persons.how_it_works", ":", 2),  # the route's caption, then its stations
    ],
)
def test_the_cuts_of_the_v2_sections_rebuild_the_locked_texts(key, mode, count):
    text, _lang = locked_content.get(key, "fr")
    parts = locked_split.cut(text, mode)
    assert parts is not None and len(parts) == count, (key, parts)
    assert "".join(parts) == text
    assert _text_content(locked_split.spans(parts)) == text


def test_the_filters_wrap_and_never_retype():
    text, _lang = locked_content.get("p3.antifraud.body", "fr")
    out = Template('{% load locked_split %}{{ t|locked_spans:"sentence" }}').render(Context({"t": text}))
    assert out.count('<span class="ls ls-') == 4 and _text_content(out) == text
    template = Template('{% load locked_split %}{{ t|locked_spans:"sentence" }}')
    whole = template.render(Context({"t": "Une <seule> phrase."}))
    assert whole == "Une &lt;seule&gt; phrase.", "no cut: the text whole, escaped"


def test_emphasis_is_in_place_and_an_absent_keyword_changes_nothing():
    text = "L’association AGAMI œuvre depuis 2011 entre l’Italie et le Maroc (Italie–Maroc)."
    out = locked_split.emphasize(text, ["depuis 2011", "Italie–Maroc", "absent"])
    assert out.count('class="em-keyword"') == 2 and _text_content(out) == text
    template = Template('{% load locked_split %}{{ t|emphasize:"depuis 2011|nulle part" }}')
    rendered = template.render(Context({"t": text}))
    assert _text_content(rendered) == text and rendered.count("em-keyword") == 1
    assert locked_split.emphasize("<b>", ["x"]) == "&lt;b&gt;"


def test_the_arabic_pilot_title_isolates_its_french_name_and_keeps_its_bytes():
    """The owner's FINAL CLOSURE PASS of 12 Nov 2026: the prescribed Arabic rendering «المشروع التجريبي
    Vénétie–Maroc» is never reworded — its French proper name is isolated at render as ONE left-to-right unit
    (<bdi dir="ltr">), so the dash is never reordered by the Arabic around it; the textContent is the locked text,
    byte for byte. No lang on the bdi: the heading would turn left to right as a whole (v5/base.css's
    prescribed-French rule)."""
    text, lang = locked_content.get("p3.pilot.title", "ar")
    assert lang == "ar", lang
    assert text.startswith("المشروع التجريبي ") and "Vénétie–Maroc" in text
    template = Template('{% load locked_split %}{{ t|isolate_ltr:"Vénétie–Maroc|VÉNÉTIE–MAROC" }}')
    rendered = template.render(Context({"t": text}))
    assert rendered.count('<bdi class="em-keyword" dir="ltr">Vénétie–Maroc</bdi>') == 1, rendered
    assert _text_content(rendered) == text and _text_content(rendered).encode() == text.encode()
    assert "<span" not in rendered, "the Arabic phrase itself is not wrapped: it keeps the title's direction"
    assert locked_split.emphasize("<b>", ["x"], ltr=True) == "&lt;b&gt;"
