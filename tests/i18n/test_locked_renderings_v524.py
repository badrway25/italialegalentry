"""
The Arabic rendering policy of the prescribed texts (V5.27 «ARABIC OWNER DECISION — FINAL»; FINAL_DELIVERY_V2.md R7′,
§3.8 (a)–(g); lane AR, label v524-ar) — ``cms.locked_renderings`` beside ``cms.locked_content``:

* the registry's French is untouched by the policy: every key in French is the registry's value, the checksums hold
  (``tests/compliance/test_locked_content.py`` keeps the byte-identity; here the seam is proved not to alter a French read);
* the policy is TOTAL: every text of the registry has exactly one class; every C-UI text has its Arabic rendering; every
  C-SUBST-FR text has its source route(s) and its page name; no rendering is machine-shaped (Arabic script, Western digits,
  Arabic punctuation, the brand's run followed by LRM);
* the seam: on ``/ar/`` a C-UI key answers its rendering with ``effective = "ar"``; a C-SUBST-FR key answers the French
  (``"fr"``) on its own route and the pointer line (``"ar"``) elsewhere; C-OFFICIAL and C-SUBST-IT keys answer the French;
  Italian and English keep today's behaviour; a sub-key addresses one text of a compound value; a compound value whose parts
  must stay French on this page stays French whole;
* the tag: the caption before a substantive block on its own page, the pointer off it, the brand isolated in a rendering;
* the cuts the compositions make on a rendering rebuild it (the route's four stations, the Forum's eight clauses and nine
  actors);
* Phase 3: an Arabic rendering of a Phase 3 text never shows before gate G3 (the leak guard of
  ``tests/compliance/test_phase3_texts_not_leaked.py``, extended to the renderings);
* the dev board lists every key with its class and status; the three counts of the report.
"""

from __future__ import annotations

import re

import pytest
from django.template import Context, Template
from django.urls import reverse
from django.utils import translation

from cms import locked_content, locked_renderings, locked_split

ARABIC = re.compile(r"[؀-ۿ]")
ARABIC_INDIC_DIGITS = re.compile(r"[٠-٩۰-۹]")
LATIN_WORD = re.compile(r"[A-Za-zÀ-ÿ]{2,}")
LRM = "‎"


@pytest.fixture(autouse=True)
def _outside_a_request():
    """Every test starts outside a request (the French stands for a substantive key) unless it pins a route."""
    locked_renderings.set_route_for_tests(None)
    yield
    locked_renderings.set_route_for_tests(None)


# ---------------------------------------------------------------------------------------------
# the policy is total and well formed
# ---------------------------------------------------------------------------------------------
def test_every_text_of_the_registry_has_exactly_one_class():
    unknown = [subkey for subkey, _french in locked_renderings.leaves() if locked_renderings.treatment(subkey) is None]
    assert unknown == []
    for pattern, kind in locked_renderings.TREATMENT.items():
        assert kind in locked_renderings.TREATMENTS, pattern
    # every pattern names a text that exists (no stale row in the policy).
    # RESTATED under V5.20 for the owner's directive of 10 Nov 2026 on the Arabic FAQ (DL54-211): a row may class ONE text by its
    # sub-key (the FAQ's five informational answers) — that text must exist too, and the row must change its class
    patterns = {locked_renderings.pattern(subkey) for subkey, _french in locked_renderings.leaves()}
    patterns |= {
        locked_renderings.pattern(subkey) for subkey, _french in locked_renderings.leaves() if "[" not in subkey
    }
    subkeys = {subkey for subkey, _french in locked_renderings.leaves()}
    for key, kind in locked_renderings.TREATMENT.items():
        assert key in patterns or key in subkeys or key in locked_content.keys(), key  # noqa: SIM118
        if key in subkeys and key not in patterns:
            assert kind != locked_renderings.TREATMENT.get(locked_renderings.pattern(key)), key


def test_every_c_ui_text_has_its_rendering_and_nothing_else_has_one():
    c_ui = {subkey for subkey, _french in locked_renderings.leaves() if locked_renderings.treatment(subkey) == "C-UI"}
    assert c_ui - set(locked_renderings.AR) == set(), "a compositional text without its provisional Arabic"
    assert set(locked_renderings.AR) - c_ui == set(), "a rendering of a text that is not compositional"


def test_the_renderings_are_professional_arabic_not_machine_shaped():
    for subkey, arabic in locked_renderings.AR.items():
        french = locked_content.get(subkey, "fr")[0]
        assert arabic.strip() == arabic and arabic, subkey
        assert ARABIC.search(arabic), subkey
        assert not ARABIC_INDIC_DIGITS.search(arabic), subkey
        assert arabic != french, subkey
        # a Latin run inside the Arabic (the brand, a proper name, an Italian term) is followed by LRM when a clause ends
        for match in re.finditer(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ –™’'.-]*[A-Za-z™]", arabic):
            following = arabic[match.end() : match.end() + 1]
            assert following in ("", LRM, " ", "»", ")", "؟", "،", "؛", ":", "."), (subkey, match.group(0))
        # Western digits of the French kept (dates, times) and the French's own numerals present
        for number in re.findall(r"\d+", french):
            if number not in ("15", "18", "00"):  # «15h00–18h00» is written «15:00 … 18:00»
                assert number in arabic, (subkey, number)
        # a question keeps its question mark, in Arabic
        if french.rstrip().endswith("?"):
            assert arabic.rstrip().endswith("؟"), subkey


def test_every_substantive_french_text_has_its_source_route_and_its_page_name():
    for subkey, _french in locked_renderings.leaves():
        if locked_renderings.treatment(subkey) != "C-SUBST-FR":
            continue
        assert locked_renderings.source_routes(subkey), subkey
        with translation.override("ar"):
            assert locked_renderings.page_name(subkey), subkey
            line = locked_renderings.pointer_line(subkey)
            name = locked_renderings.page_name(subkey)
        assert ARABIC.search(line) and "%(" not in line, (subkey, line)
        assert ARABIC.search(name) and name in line, (subkey, name)


def test_the_source_routes_resolve():
    kwargs = {"pathways:detail": {"key": "salaried_work"}, "glossary:term": {"slug": "nulla_osta"}}
    for routes in locked_renderings.SOURCE_ROUTES.values():
        for name in routes:
            assert reverse(name, kwargs=kwargs.get(name)), name


def test_the_counts_of_the_report():
    counts = locked_renderings.counts()
    leaves = locked_renderings.leaves()
    assert sum(counts.values()) == len(leaves) + len(locked_renderings.OFFICIAL_MSGIDS)
    assert counts["C-UI"] == len(locked_renderings.AR)
    # the register's figures, exactly (LOCKED_BLOCKS_REGISTER.md §2): a change of class is a decision and moves them.
    # RESTATED under V5.20 for the owner's directive of 10 Nov 2026 on the Arabic FAQ (DL54-211): five FAQ answers moved from
    # C-SUBST-FR to C-UI, the figures moved with them
    assert counts["C-UI"] == 144
    assert counts["C-SUBST-FR"] == 29  # 4 answers + 10 definitions + 8 descriptions + intro + 3 bodies + 3 consents
    assert counts["C-OFFICIAL"] == 17  # the trademark, the names, the 10 Italian terms, the Forum's titles, the address
    # the six legal courtesy keys, counted by their texts (titles, sections, paragraphs)
    legal_keys = {key for key in locked_content.keys() if locked_renderings.treatment(key) == "C-SUBST-IT"}  # noqa: SIM118
    assert len(legal_keys) == 6
    assert (
        counts["C-SUBST-IT"]
        == sum(1 for subkey, _ in leaves if subkey.split("[")[0].startswith(tuple(legal_keys)))
        == 59
    )


# ---------------------------------------------------------------------------------------------
# the registry's French is untouched; the seam
# ---------------------------------------------------------------------------------------------
def test_a_french_read_is_the_registry_whatever_the_policy_says():
    locked_renderings.set_route_for_tests("")
    for key in locked_content.keys():
        value, effective = locked_content.get(key, "fr")
        assert value == locked_content.LOCKED_TEXTS["fr"][key] and effective == "fr", key
    assert locked_content.checksums("fr") == {
        k: locked_content.checksum(v) for k, v in locked_content.LOCKED_TEXTS["fr"].items()
    }


@pytest.mark.parametrize("lang", ["it", "en"])
def test_italian_and_english_keep_todays_behaviour(lang):
    locked_renderings.set_route_for_tests("")
    for key in (
        "p3.hero.subtitle",
        "p3.antifraud.title",
        "p3.antifraud.body",
        "p3.faq.items",
        "p1.companies.form.fields",
    ):
        value, effective = locked_content.get(key, lang)
        assert value == locked_content.LOCKED_TEXTS["fr"][key] and effective == "fr", (lang, key)


def test_a_compositional_key_answers_its_rendering_on_arabic():
    for key in ("p3.hero.subtitle", "p3.antifraud.title", "p3.entrances.person.title", "p1.companies.form.button"):
        value, effective = locked_content.get(key, "ar")
        assert value == locked_renderings.AR[key] and effective == "ar", key
    text = locked_content.text("p3.reserved.title", "ar")
    assert text == locked_renderings.AR["p3.reserved.title"] and text.lang == "ar" and text.fallback_lang == ""


def test_a_substantive_key_answers_the_french_on_its_page_and_the_pointer_elsewhere():
    key = "p3.antifraud.body"
    french = locked_content.LOCKED_TEXTS["fr"][key]
    # outside a request: the French
    assert locked_content.get(key, "ar") == (french, "fr")
    locked_renderings.set_route_for_tests("pages:antifraud")
    assert locked_content.get(key, "ar") == (french, "fr")
    assert locked_renderings.is_hidden(key, "ar") is False
    locked_renderings.set_route_for_tests("pages:home")
    with translation.override("ar"):
        value, effective = locked_content.get(key, "ar")
        assert effective == "ar" and value == locked_renderings.pointer_line(key)
        assert "احذروا الاحتيال" in value and not LATIN_WORD.search(value)
    assert locked_renderings.is_hidden(key, "ar") is True
    # the French and the Italian pages are not concerned
    assert locked_content.get(key, "fr") == (french, "fr")
    assert locked_content.get(key, "it") == (french, "fr")


def test_an_official_name_and_a_legal_text_answer_the_french():
    locked_renderings.set_route_for_tests("pages:home")
    for key in ("p1.trademark.mark", "p2.forum.header.title", "p3.hero.title", "p1.email.public_contact"):
        assert locked_content.get(key, "ar") == (locked_content.LOCKED_TEXTS["fr"][key], "fr"), key
    for key in ("legal.privacy.fr_courtesy", "legal.courtesy_notice.fr"):
        assert locked_content.get(key, "ar") == (locked_content.LOCKED_TEXTS["fr"][key], "fr"), key


def test_a_sub_key_addresses_one_text_of_a_compound_value():
    french = locked_content.LOCKED_TEXTS["fr"]
    assert locked_content.get("p3.faq.items[0].question", "fr") == (french["p3.faq.items"][0]["question"], "fr")
    assert locked_content.get("p3.pilot.sequence[2]", "fr") == (french["p3.pilot.sequence"][2], "fr")
    assert locked_content.get("p3.persons.pathways[1].title", "ar") == (
        locked_renderings.AR["p3.persons.pathways[1].title"],
        "ar",
    )
    assert (
        locked_content.text("p1.companies.form.fields[0]", "ar") == locked_renderings.AR["p1.companies.form.fields[0]"]
    )
    locked_renderings.set_route_for_tests("pathways:detail")
    description = french["p3.persons.pathways"][0]["description"]
    assert locked_content.get("p3.persons.pathways[0].description", "ar") == (description, "fr")
    locked_renderings.set_route_for_tests("pathways:index")
    with translation.override("ar"):
        value, effective = locked_content.get("p3.persons.pathways[0].description", "ar")
    assert effective == "ar" and locked_renderings.AR["p3.persons.pathways[0].title"] in value
    for bad in (
        "p3.faq.items[99].question",
        "p3.faq.items[0].nothing",
        "p3.faq.items[x]",
        "p3.faq.items[0]]",
        "p9.nothing",
    ):
        with pytest.raises(locked_content.LockedContentMissing):
            locked_content.get(bad, "fr")


def test_a_compound_value_is_rebuilt_part_by_part_or_stays_french_whole():
    french = locked_content.LOCKED_TEXTS["fr"]
    # the pilot's sequence: eight compositional words → eight Arabic words
    value, effective = locked_content.get("p3.pilot.sequence", "ar")
    assert effective == "ar" and value == [locked_renderings.AR[f"p3.pilot.sequence[{i}]"] for i in range(8)]
    # the form's labels: fourteen
    value, effective = locked_content.get("p1.companies.form.fields", "ar")
    assert effective == "ar" and len(value) == 14 and all(ARABIC.search(label) for label in value)
    # the FAQ off its page: the questions in Arabic, the answers as pointer lines, the keys kept.
    # RESTATED under V5.20 for the owner's directive of 10 Nov 2026 on the Arabic FAQ (DL54-211): an informational answer reads
    # its rendering wherever it is quoted, a substantive one its pointer line — every answer held, not the first alone
    locked_renderings.set_route_for_tests("pages:home")
    with translation.override("ar"):
        value, effective = locked_content.get("p3.faq.items", "ar")
    assert effective == "ar" and [e["key"] for e in value] == [e["key"] for e in french["p3.faq.items"]]
    assert value[0]["question"] == locked_renderings.AR["p3.faq.items[0].question"]
    rendered = [i for i in range(len(value)) if locked_renderings.treatment(f"p3.faq.items[{i}].answer") == "C-UI"]
    assert rendered == [0, 2, 4, 6, 8], rendered
    for i, entry in enumerate(value):
        if i in rendered:
            assert entry["answer"] == locked_renderings.AR[f"p3.faq.items[{i}].answer"], i
        else:
            assert "الأسئلة الشائعة" in entry["answer"] and not LATIN_WORD.search(entry["answer"]), i
    # the FAQ on its own page: the substantive answers must stay French → the whole value stays French (the page
    # composes the parts)
    locked_renderings.set_route_for_tests("faq:index")
    assert locked_content.get("p3.faq.items", "ar") == (french["p3.faq.items"], "fr")
    # the glossary off its page: the Italian terms untouched, the definitions pointed; on its page: French whole
    locked_renderings.set_route_for_tests("pathways:detail")
    with translation.override("ar"):
        value, effective = locked_content.get("p3.glossary.terms", "ar")
    assert effective == "ar" and value[2]["term"] == french["p3.glossary.terms"][2]["term"]
    assert "مسرد المصطلحات" in value[2]["definition"]
    locked_renderings.set_route_for_tests("glossary:index")
    assert locked_content.get("p3.glossary.terms", "ar") == (french["p3.glossary.terms"], "fr")
    # the pathways' whole key, no longer deferred (V5.20: AR NOTES §4's contract «then DEFERRED_WHOLE loses its row»,
    # FINAL_DELIVERY_V2 §3.9 — every reader composes the parts by sub-key since CLOSING converted the home's): on the
    # home the titles read their provisional Arabic, the descriptions their pointer line, the identifiers untouched
    locked_renderings.set_route_for_tests("pages:home")
    assert not locked_renderings.DEFERRED_WHOLE
    with translation.override("ar"):
        value, effective = locked_content.get("p3.persons.pathways", "ar")
        pointer = locked_renderings.pointer_line("p3.persons.pathways[0].description")
    source = french["p3.persons.pathways"]
    assert effective == "ar" and len(value) == len(source) == 8
    assert all(v["key"] == s["key"] and v["title"] != s["title"] for v, s in zip(value, source, strict=True))
    assert value[0]["description"] == pointer and source[0]["description"] not in str(value)


def test_the_route_comes_from_the_request(client, seeded, phase3_open):
    """The seam reads the request's route: the anti-fraud page shows its own body in French (identified); the home shows
    the pointer line in its place."""
    own = client.get("/ar/attention-aux-fraudes/").content.decode()
    french = locked_content.LOCKED_TEXTS["fr"]["p3.antifraud.body"]
    assert french.split(".")[0] in own
    home = client.get("/ar/").content.decode()
    assert french.split(".")[0] not in home
    with translation.override("ar"):
        pointer = locked_renderings.pointer_line("p3.antifraud.body")
    assert pointer in home
    # outside a request, the French stands again
    assert locked_content.get("p3.antifraud.body", "ar") == (french, "fr")


# ---------------------------------------------------------------------------------------------
# the tag
# ---------------------------------------------------------------------------------------------
def _render(source: str, lang: str) -> str:
    with translation.override(lang):
        return Template(source).render(Context())


def test_the_tag_renders_a_compositional_text_in_arabic_without_a_language_attribute():
    html = _render('{% locked "p3.entrances.person.title" %}', "ar")
    assert html == locked_renderings.AR["p3.entrances.person.title"]
    html = _render('{% locked "p3.entrances.person.title" "h2" "x" %}', "ar")
    assert html == f'<h2 class="x">{locked_renderings.AR["p3.entrances.person.title"]}</h2>'
    assert _render('{% locked "p3.entrances.person.title" %}', "it").startswith('<span lang="fr">')


def test_the_tag_isolates_the_brand_inside_an_arabic_rendering():
    html = _render('{% locked "p3.hero.body" %}', "ar")
    assert '<bdi dir="ltr">Italy Legal Entry‎</bdi>' in html
    html = _render('{% locked "p2.forum.who.body" "p" %}', "ar")
    assert '<bdi dir="ltr">Italy Legal Entry™‎</bdi>' in html


def test_the_tag_captions_a_substantive_block_on_its_own_page_and_points_elsewhere():
    locked_renderings.set_route_for_tests("pages:antifraud")
    html = _render('{% locked "p3.antifraud.body" "p" "protezione__testo" %}', "ar")
    assert html.startswith('<p class="t-label locked-caption" data-locked-caption="p3.antifraud.body">')
    assert "النص المصدر بالفرنسية" in html and 'lang="fr"' in html
    assert locked_content.LOCKED_TEXTS["fr"]["p3.antifraud.body"][:40] in html
    # the inline form carries no caption, the French its language
    inline = _render('{% locked "p3.antifraud.body" %}', "ar")
    assert inline.startswith('<span lang="fr">') and "locked-caption" not in inline
    # the caption tag alone
    assert "locked-caption" in _render('{% locked_caption "p3.antifraud.body" %}', "ar")
    assert _render('{% locked_caption "p3.antifraud.title" %}', "ar") == ""
    assert _render('{% locked_caption "p3.antifraud.body" %}', "fr") == ""
    # off its page: the pointer, no caption, no French
    locked_renderings.set_route_for_tests("pages:home")
    html = _render('{% locked "p3.antifraud.body" "p" "protezione__testo" %}', "ar")
    assert "locked-caption" not in html and 'lang="fr"' not in html and not LATIN_WORD.search(html.split(">", 1)[1])
    assert _render('{% locked_is_hidden "p3.antifraud.body" %}', "ar") == "True"
    assert _render('{% locked_treatment "p3.antifraud.body" %}', "ar") == "C-SUBST-FR"
    assert _render('{% locked_treatment "p3.faq.items[0].question" %}', "ar") == "C-UI"


def test_a_french_or_italian_page_never_sees_a_caption():
    locked_renderings.set_route_for_tests("pages:antifraud")
    for lang in ("fr", "it", "en"):
        html = _render('{% locked "p3.antifraud.body" "p" %}', lang)
        assert "locked-caption" not in html
        assert locked_content.LOCKED_TEXTS["fr"]["p3.antifraud.body"][:40] in html


# ---------------------------------------------------------------------------------------------
# the cuts the compositions make on a rendering
# ---------------------------------------------------------------------------------------------
def test_the_route_sentence_cuts_into_its_four_stations_in_arabic():
    from pathways import services as pathways

    locked_renderings.set_route_for_tests("pages:home")
    cut = pathways.how_it_works("ar")
    assert cut is not None and len(cut.steps) == 4 and cut.lang == ""
    assert cut.text == locked_renderings.AR["p3.persons.how_it_works"]
    assert ARABIC.search(cut.caveat)


def test_the_forum_objectives_cut_into_eight_clauses_and_the_audience_into_nine_actors_in_arabic():
    from forum.templatetags import forum_v2

    objectives = locked_renderings.AR["p2.forum.objectives.body"]
    clauses = locked_split.split(objectives, ";")
    assert clauses is not None and len(clauses) == 8 and "".join(clauses) == objectives
    audience = locked_renderings.AR["p2.forum.audience.body"]
    actors = forum_v2.actors(audience)
    assert actors is not None and len(actors) == 9
    assert "".join(w + p for w, p in actors) == audience
    # the French cuts are untouched
    objectives_fr = locked_content.LOCKED_TEXTS["fr"]["p2.forum.objectives.body"]
    assert len(locked_split.split(objectives_fr, ";")) == 8
    assert locked_split.split("a ; b ; c", ";") == ("a ; ", "b ; ", "c")
    assert locked_split.split("أ؛ ب؛ ج", ";") == ("أ؛ ", "ب؛ ", "ج")


# ---------------------------------------------------------------------------------------------
# Phase 3 — a rendering never leaks before the gate (the leak guard, extended to the Arabic)
# ---------------------------------------------------------------------------------------------
#: shorter renderings (a three-word title such as «التكوين في بلد المنشأ») are ordinary phrases of the team's own copy too —
#: the French guard ignores fragments under 28 characters for the same reason (test_phase3_texts_not_leaked.MIN_FRAGMENT)
MIN_FRAGMENT = 28


def _phase3_renderings() -> list[tuple[str, str]]:
    out = []
    for subkey, arabic in locked_renderings.AR.items():
        if subkey.startswith("p3.") and len(arabic) >= MIN_FRAGMENT and subkey not in ("p3.reserved.button",):
            out.append((subkey, " ".join(arabic.split())))
    return out


def test_there_are_phase3_renderings_to_look_for():
    assert len(_phase3_renderings()) >= 20


def test_open_arabic_pages_show_no_phase3_rendering_while_the_gate_is_closed(client, seeded):
    from core.public_routes import ungated_paths

    offenders = {}
    for path in ungated_paths():
        response = client.get(f"/ar/{path}")
        if response.status_code != 200:
            continue
        text = " ".join(re.sub(r"<[^>]+>", " ", response.content.decode()).split())
        found = [subkey for subkey, arabic in _phase3_renderings() if arabic in text]
        if found:
            offenders[path] = found
    assert not offenders, offenders


# ---------------------------------------------------------------------------------------------
# the dev board
# ---------------------------------------------------------------------------------------------
def test_the_board_lists_every_key_with_its_class_and_status():
    rows = locked_renderings.board_rows()
    assert len(rows) == len(locked_renderings.leaves()) + len(locked_renderings.OFFICIAL_MSGIDS)
    by_key = {row["key"]: row for row in rows}
    assert by_key["p3.hero.subtitle"]["treatment"] == "C-UI"
    assert by_key["p3.hero.subtitle"]["status"] == locked_renderings.STATUS_PROVISIONAL
    assert by_key["p3.hero.subtitle"]["rendered"] is True
    # RESTATED under V5.20 for the owner's directive of 10 Nov 2026 on the Arabic FAQ (DL54-211): the first answer is
    # informational now — a rendering, no source page —, the second the substantive example the row held
    assert by_key["p3.faq.items[1].answer"]["treatment"] == "C-SUBST-FR"
    assert by_key["p3.faq.items[1].answer"]["routes"] == "faq:index"
    assert by_key["p3.faq.items[0].answer"]["treatment"] == "C-UI" and by_key["p3.faq.items[0].answer"]["rendered"]
    assert by_key["p3.faq.items[0].answer"]["routes"] == ""
    assert by_key["legal.privacy.fr_courtesy.title"]["treatment"] == "C-SUBST-IT"
    assert by_key["p1.trademark.mark"]["treatment"] == "C-OFFICIAL"
    assert all(row["status"] != "UNCLASSIFIED" for row in rows)


def test_the_register_fragment_renders_its_counts():
    """The fragment renders wherever the preview's URLs are mounted or not (v524-ar-fix B1: a hyphenated key in
    `locked_counts.C-UI` raised TemplateSyntaxError and a 500 on /__design-v5/index/)."""
    from django.template.loader import render_to_string

    html = render_to_string(
        "dev/designpreview/_locked_keys.html",
        {"locked_rows": locked_renderings.board_rows(), "locked_counts": locked_renderings.template_counts()},
    )
    for kind, figure in locked_renderings.counts().items():
        assert f"<strong>{kind}</strong>" in html
        assert f"({figure})" in html


def test_the_dev_board_index_carries_the_register(client, seeded, settings):
    settings.ILE_DESIGN_PREVIEW = True
    response = client.get("/__design-v5/index/")
    if response.status_code == 404:
        pytest.skip("the dev board is not served here (404: the preview app is off in this environment)")
    # any other status is a defect of the board (v524-ar-fix B1: a hyphenated key raised a 500 the old skip hid)
    assert response.status_code == 200, response.status_code
    html = response.content.decode()
    for kind, figure in locked_renderings.counts().items():
        assert f"<strong>{kind}</strong>" in html
        assert f"({figure})" in html
    assert 'id="testi-bloccati"' in html
    assert "p3.faq.items[0].answer" in html and "C-SUBST-FR" in html
    assert locked_renderings.STATUS_PROVISIONAL in html
