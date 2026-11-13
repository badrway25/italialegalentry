"""
V5.15 W3, lane B — the premium form system on the V5.15 bar (DECISIONS §5.10–5.15, §15 «Premium Forms + Icon Visual
System»): the formwork (panel, sticky side), the multi-step forms (the company's need: four steps and a review; the
public «Recueil des besoins»: three, the prescribed order and the locked consent and button unchanged; the sign-up:
two), the new password's live checklist, the drop zone of a file field, the receipt after a request, the glyph tile,
the document rows (the file, its size, its download) and the filters without a zero, the empty state's surface.

Behaviour is held here; the look is reviewed in headed Chromium (docs/design-v5/QA/v515/b/NOTES.md).
"""

from __future__ import annotations

import gzip
import os
import re
from pathlib import Path

import pytest
from django import forms
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.utils import translation

from accounts.forms import SignupForm
from companies.forms import CompanyNeedForm
from core.templatetags import ile_forms
from enquiries.forms import CompanyNeedsForm
from enquiries.models import CompanyNeedsRequest

# the browser tests drive Playwright's sync API beside the live server's database (as the other browser modules do)
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
gz = lambda path: len(gzip.compress(path.read_bytes(), 9))  # noqa: E731


def _names(steps):
    return [[bound.name for bound in step["fields"]] for step in steps]


# ---- the steps -----------------------------------------------------------------------------------------------
@pytest.mark.django_db
def test_the_public_needs_form_has_three_steps_in_the_prescribed_order():
    with translation.override("fr"):
        steps = ile_forms.form_steps(CompanyNeedsForm())
    assert [s["key"] for s in steps] == ["entreprise", "besoin", "envoi"]
    flat = [name for names in _names(steps) for name in names]
    assert flat == [*CompanyNeedsRequest.DATA_FIELDS, "consent"], "the 14 prescribed fields keep their order, then the consent"
    assert len(flat) == len(set(flat)) and "website_url" not in flat
    assert [s["n"] for s in steps] == [1, 2, 3] and all(s["glyph"] for s in steps)


@pytest.mark.django_db
def test_the_company_need_has_four_steps_and_a_review_and_loses_no_field():
    form = CompanyNeedForm()
    steps = ile_forms.form_steps(form)
    assert len(steps) == 5 and steps[-1]["fields"] == [] and form.steps_review
    flat = [name for names in _names(steps) for name in names]
    assert sorted(flat) == sorted(b.name for b in form.visible_fields()), "every visible field is in one step"
    assert "mandatory_skills" in _names(steps)[1] and "start_from" in _names(steps)[3]


def test_the_signup_asks_who_first_then_the_identity():
    steps = ile_forms.form_steps(SignupForm())
    assert _names(steps)[0] == ["account_type"]
    assert _names(steps)[1][:2] == ["full_name", "email"] and _names(steps)[1][-1] == "accept_terms"
    assert "website_url" not in [n for names in _names(steps) for n in names]


def test_a_form_without_steps_has_none_and_unnamed_fields_join_the_last_step():
    class Plain(forms.Form):
        a = forms.CharField()

    assert ile_forms.form_steps(Plain()) == []

    class Partial(forms.Form):
        a = forms.CharField()
        b = forms.CharField()
        steps = (("one", "Un", "", ("a",)), ("two", "Deux", "", ()))

    assert _names(ile_forms.form_steps(Partial())) == [["a"], ["b"]]


@pytest.mark.django_db
def test_a_step_with_an_error_is_marked_for_the_script():
    form = CompanyNeedsForm(data={"company_name": ""})
    form.is_valid()
    steps = ile_forms.form_steps(form)
    assert steps[0]["errors"] is True


@pytest.mark.django_db
def test_the_public_needs_page_is_the_formwork_in_steps_and_works_without_script(client, seeded, legal_published):
    response = client.get("/fr/entreprises/recueil-des-besoins/")
    html = response.content.decode()
    assert response.status_code == 200
    form = re.search(r'<form[^>]+id="formulaire-recueil-des-besoins"[^>]*>', html).group(0)
    assert "data-steps" in form and "data-steps-review-on" in form
    for key in ("next", "back", "edit", "position"):
        assert f"data-msg-{key}=" in form
    assert "data-msg-empty" not in form and "Non renseigné" not in html, "an empty answer is a dash, a missing one an error"
    # all the steps and all the fields are in the page: without script the form is the same form
    assert list(re.findall(r'<fieldset class="form-step" id="etape-([a-z]+)"', html)) == ["entreprise", "besoin", "envoi"]
    for name in CompanyNeedsRequest.DATA_FIELDS:
        assert f'name="{name}"' in html
    assert ' hidden' not in re.search(r'<fieldset class="form-step" id="etape-besoin"[^>]*>', html).group(0)
    # the rail is a table of contents without script; the side says what happens after; the review has its seat
    assert html.count('class="steps-rail__link" href="#etape-') == 3
    assert "formwork__side" in html and "data-steps-review" in html
    assert "formwork__panel" in html and html.count("form-step__count") == 3
    # the locked button is the form's own, after the steps
    assert html.index('id="etape-envoi"') < html.index('class="form__actions"')


@pytest.mark.django_db
def test_the_signup_page_is_in_two_steps_with_the_live_password_checklist(client, seeded, legal_published):
    html = client.get("/fr/compte/signup/").content.decode()
    form = re.search(r'<form[^>]+data-steps[^>]*>', html)
    assert form, "the sign-up form says its steps"
    assert re.findall(r'id="etape-([a-z]+)"', html) == ["profil", "identite"]
    assert html.index('id="etape-profil"') < html.index('name="account_type"') < html.index('id="etape-identite"')
    rules = re.findall(r'<li class="pw-rule" data-rule="([^"]*)"', html)
    assert rules == ["min:12", "notnumeric"], "the checklist holds the rules the browser verifies"
    note = re.search(r'<p class="pw-rules__note">([^<]+)</p>', html)
    assert note and "mot de passe" in note.group(1).lower(), "the server's own rules: one quiet sentence, no mark"
    assert 'data-pw-rules="id_password1"' in html and "data-pw-summary" in html and 'aria-live="polite"' in html
    assert 'data-pw-rules="id_password2"' not in html, "the confirmation has no checklist"


@pytest.mark.django_db
def test_the_password_rules_are_the_validators_own_words():
    rules = ile_forms.password_rules(SignupForm()["password1"])
    assert [r["rule"] for r in rules if r["rule"]] == ["min:12", "notnumeric"]
    assert all(r["text"] for r in rules)
    assert ile_forms.password_rules(SignupForm()["password2"]) == []


# ---- the script ----------------------------------------------------------------------------------------------
def test_the_steps_module_is_fetched_only_where_a_steps_form_is_and_draws_no_tick():
    fieldcheck = (STATIC / "js" / "src" / "fieldcheck.js").read_text(encoding="utf-8")
    steps = (STATIC / "js" / "src" / "steps.js").read_text(encoding="utf-8")
    assert 'querySelector("form[data-steps]")) import("./steps.js")' in fieldcheck
    assert "validate" in fieldcheck and "data-pw-rules" in fieldcheck
    for source in (steps, fieldcheck):
        assert "innerHTML" not in source and "eval(" not in source and ".style." not in source
    assert '"check"' not in steps and "circle-check" not in steps, "a done step keeps its number (O14)"
    assert "history.replaceState" in steps and "etape" in steps, "the address keeps the step"
    assert "stopImmediatePropagation" in steps, "Enter on a step that is not the last moves on, never sends"
    # F1: the one motion gate (test_script_motion_gate): reducedMotion() and play() from motion.js, cut from the keyboard
    assert 'still()' in steps and 'import { play, reducedMotion } from "./motion.js";' in steps and "reducedMotion()" in steps
    assert 'data-input") === "key"' in steps


def test_budgets():
    """The unit is the KiB (6 × 1024 B, gzip -9). A steps form loads fieldcheck.js + steps.js; the review is fetched
    when the last step is reached; combobox.js is §5.7's own ≤ 3 KB enhancement, fetched only where a long select is."""
    dist = STATIC / "js" / "dist"
    assert gz(dist / "fieldcheck.js") + gz(dist / "steps.js") <= 6 * 1024, "form-page JS ≤ 6 KiB gzip at load"
    assert gz(dist / "fieldcheck.js") + gz(dist / "steps.js") + gz(dist / "steps-review.js") <= 6 * 1024 + 1024
    assert gz(dist / "combobox.js") <= 3 * 1024
    steps = (STATIC / "js" / "src" / "steps.js").read_text(encoding="utf-8")
    assert 'import("./steps-review.js")' in steps, "the review is fetched on reaching the last step"
    assert gz(STATIC / "css" / "dist" / "core" / "forms.css") <= 6 * 1024
    assert gz(STATIC / "css" / "dist" / "core" / "glyph.css") <= 2 * 1024
    assert gz(STATIC / "css" / "dist" / "core" / "steps.css") <= 3 * 1024, "the steps' own sheet (round 2)"
    assert gz(STATIC / "css" / "dist" / "core" / "receipt.css") <= 2 * 1024
    assert gz(STATIC / "css" / "dist" / "orientation" / "wizard.css") <= 6 * 1024
    main = (STATIC / "css" / "main.css").read_text(encoding="utf-8")
    assert "_steps.css" not in main and "_steps.css" not in (STATIC / "css" / "v5" / "_form.css").read_text(encoding="utf-8")
    assert "_formwork.css" not in main and "_glyph.css" not in main and "_receipt.css" not in main
    # design-v5's main.css after the v515-a and v515-c merges (lane A's recorded V5.15 exception); lane B adds nothing
    # V5.19 (lane v519-k, the owner's order): + 124 B for the telephone channels of the footer and the phone's sheet;
    # design-v5 after the v518 merge was already 33 455 B — the ceiling is lane A's V5.15 exception (test_motion_v512_a_w2)
    # V5.18 green suite (the v518g merge, DL54-179; V5.8: a shared bundle ratchets down): group N's dead shared CSS
    # left it at 33 530 B with lane K's channels — the ratchet is re-seated at that measure
    # V5.20: ratchet restored by dead-rule removal (v520-css, 30 October 2026: the declarations a later layer of the
    # same context re-declares and the custom properties nothing reads left the token layers; the shim shrank) — 33 530
    # → 32 657 B → 32 105 B (CLOSING, V5.29 09:41 item 2: the headroom under the hard 32 716), the measure
    assert gz(STATIC / "css" / "dist" / "main.css") <= 32_105


def test_the_new_sheets_are_logical_and_honour_reduced_motion():
    for name in ("_formwork.css", "_steps.css", "_glyph.css", "_receipt.css"):
        css = (STATIC / "css" / "v5" / name).read_text(encoding="utf-8")
        assert not re.search(r"(?<![\w-])(margin|padding)-(left|right)\s*:|(?<![\w-])(left|right)\s*:", css), name
        assert "html.rm" in css or name == "_steps.css", f"{name}: the site's reduced-motion switch"
        assert not re.search(r"#[0-9a-fA-F]{3,8}\b", css), f"{name}: tokens only"
        assert "forced-colors: active" in css
    assert "prefers-reduced-motion: reduce" in (STATIC / "css" / "v5" / "_glyph.css").read_text(encoding="utf-8")
    receipt = (STATIC / "css" / "v5" / "_receipt.css").read_text(encoding="utf-8")
    assert "html.rm .receipt__ring" in receipt and "prefers-reduced-motion: reduce" in receipt


# ---- the components ------------------------------------------------------------------------------------------
def test_a_file_field_is_a_drop_zone_over_the_native_input():
    class Upload(forms.Form):
        piece = forms.FileField(label="Pièce")

    with translation.override("fr"):
        html = render_to_string("components/form_field.html", {"field": Upload()["piece"], "request": RequestFactory().get("/")})
    assert 'class="dropzone" data-filezone' in html and 'type="file"' in html and "data-file-name" in html
    assert html.index("data-filezone") < html.index('type="file"') < html.index("glyph-tile")


def test_the_receipt_says_filed_never_approved(client, db):
    html = client.get("/fr/demande-transmise/").content.decode()
    assert 'class="receipt"' in html and "receipt__ring" in html and "receipt__dot" in html
    assert 'role="status"' in html and "css/dist/core/receipt.css" in html and "css/dist/core/forms.css" not in html
    # what happens next: the request's own states, the first reached (round 1, DECISIONS §5.15)
    assert len(re.findall(r'class="receipt__stop[ "]', html)) == 3 and 'class="receipt__stop is-reached" aria-current="step"' in html
    # the receipt's own words (the v515-b merge: lane A's language popover ticks the current language with #icon-check)
    receipt = html[html.index("<main"):html.index("</main>")]
    assert "#icon-check" not in receipt and "circle-check" not in receipt


def test_the_document_row_says_its_size_never_its_name_and_stays_one_link():
    row = {
        "id": 7, "title": "Passeport", "words": {}, "mandatory": True, "version_count": 2, "health": "",
        "state": "submitted", "state_label": "Déposée", "state_reason": "", "action_blocked": False,
        "responsible": "Vous", "responsible_note": "", "responsible_glyph": "person", "due_date": None,
        "urgency": "", "due_word": "", "act": None, "detail_url": "/x/",
        "current": {"file_name": "passeport.pdf", "size": 245_760, "download_url": "/dl/abc/"},
    }
    with translation.override("fr"):
        html = render_to_string("components/document_row.html", {"row": row})
    assert re.search(r"240[,.]0\s*(Ko|Kio|KB|KiB)", html)
    assert "passeport.pdf" not in html, "the register is not a file browser"
    assert "/dl/abc/" not in html and 'class="doc-row__act"' not in html, "a quiet row offers no second control"


def test_a_filter_without_a_piece_is_folded_into_all():
    block = {"counts": {"total": 3}, "filters": [
        {"value": "missing", "label": "Manquante", "count": 3, "register": "attesa"},
        {"value": "invalid", "label": "Refusée", "count": 0, "register": "rifiuto"},
    ]}
    with translation.override("fr"):
        html = render_to_string("documents/partials/state_filter.html", {
            "block": block, "register": {"state_filter": ""}, "request": RequestFactory().get("/fr/pieces/")})
    assert "Manquante" in html and "Refusée" not in html and "Tous" in html


def test_the_glyph_tile_and_the_choice_cards_and_the_empty_state():
    choice = (STATIC / "css" / "v5" / "_choice.css").read_text(encoding="utf-8")
    assert '@import url("_glyph.css");' in choice
    cards = (ROOT / "templates" / "components" / "choice_cards.html").read_text(encoding="utf-8")
    assert 'class="choice__disc glyph-tile"' in cards
    glyph = (STATIC / "css" / "v5" / "_glyph.css").read_text(encoding="utf-8")
    for size in ("--sm", "--lg", "--xl", "--solid", "--warm", "--night"):
        assert f".glyph-tile{size}" in glyph
    assert "--identity-key" in glyph, "the ILE light on the tile's upper edge"
    # the empty state: the REAL lg tile on a muted surface, from a page-only sheet the component brings (round 1)
    partial = (ROOT / "templates" / "components" / "empty_state.html").read_text(encoding="utf-8")
    assert '{% glyph_assets %}<div class="empty-state empty-state--tile"' in partial
    assert '<span class="glyph-tile glyph-tile--xl" aria-hidden="true">{% svg_icon icon|default:"empty" "icon empty-state__icon" %}</span>' in partial
    # F1: the opening statement — no surface, the doorway arch on the rhythm line, the light run once (still under rm)
    empty = glyph.split("/* ---- the empty state")[1]
    assert ".empty-state.empty-state--tile {" in empty and "background: none;" in empty and "dashed" not in glyph
    assert "border: 1px solid var(--line-rhythm);" in empty and "html.rm .empty-state--tile > .glyph-tile::after { animation: none; }" in empty
    assert '@import url("../css/v5/_glyph.css");' in (ROOT / "apps" / "core" / "static" / "core" / "glyph.css").read_text(encoding="utf-8")


def test_the_empty_state_brings_its_sheet_once_and_main_css_does_not_rise():
    request = RequestFactory().get("/")
    with translation.override("fr"):
        twice = render_to_string("components/empty_state.html", {"title": "Rien", "request": request})
        twice += render_to_string("components/empty_state.html", {"title": "Rien", "request": request})
    assert twice.count("css/dist/core/glyph.css") == 1
    on_a_form_page = RequestFactory().get("/")
    on_a_form_page._ile_form_assets = True
    with translation.override("fr"):
        html = render_to_string("components/empty_state.html", {"title": "Rien", "request": on_a_form_page})
    assert "glyph.css" not in html, "core/forms.css already carries the tile"
    components = (STATIC / "css" / "components.css").read_text(encoding="utf-8")
    assert "glyph-tile" not in components and "empty-state--tile" not in components
    # the ratchet: design-v5's main.css at the lane's base was 31 345 B (python gzip -9), 33 448 B after the v515-a
    # and v515-c merges (the v515-b merge: identical to design-v5's); lane B adds nothing to it
    # V5.19 (lane v519-k, the owner's order): + 124 B for the telephone channels of the footer and the phone's sheet;
    # design-v5 after the v518 merge was already 33 455 B — the ceiling is lane A's V5.15 exception (test_motion_v512_a_w2)
    # V5.18 green suite (the v518g merge, DL54-179; V5.8: a shared bundle ratchets down): 33 530 B, the measure
    # V5.20: ratchet restored by dead-rule removal (v520-css, 30 October 2026: the declarations a later layer of the
    # same context re-declares and the custom properties nothing reads left the token layers; the shim shrank) — 33 530
    # → 32 657 B → 32 105 B (CLOSING, V5.29 09:41 item 2: the headroom under the hard 32 716), the measure
    assert gz(STATIC / "css" / "dist" / "main.css") <= 32_105


# ---- round 1 (v515-b-improve1) -----------------------------------------------------------------------------------
def test_ui_lang_marks_only_a_word_without_its_translation():
    with translation.override("ar"):
        assert ile_forms.ui_lang("Vos données") == "", "translated: the Arabic words are Arabic"
        assert ile_forms.ui_lang("Un mot que le catalogue ne connaît pas (test)") == ' lang="fr"'
        assert ile_forms.msg_lang("back", "Précédent") == ""
        assert ile_forms.msg_lang("x", "Un mot que le catalogue ne connaît pas (test)") == ' data-msg-x-lang="fr"'
    with translation.override("fr"):
        assert ile_forms.ui_lang("Un mot que le catalogue ne connaît pas (test)") == ""


@pytest.mark.django_db
def test_the_steps_reuse_the_translated_words_and_mark_the_minority_per_step():
    with translation.override("fr"):
        need = {step["key"]: step for step in ile_forms.form_steps(CompanyNeedForm())}
        public = {step["key"]: step for step in ile_forms.form_steps(CompanyNeedsForm())}
    assert str(need["poste"]["label"]) == "Le poste et son territoire" and str(need["competences"]["label"]) == "Compétences attendues"
    with translation.override("en"):
        assert str(ile_forms.form_steps(CompanyNeedForm())[0]["label"]) == "The position and its territory"
    # «Le besoin»: one required field among eight — the required one is tagged, the optional ones are not
    assert public["besoin"]["minority"] == "required" and public["entreprise"]["minority"] == ""
    msgs = (ROOT / "templates" / "components" / "_steps_msgs.html").read_text(encoding="utf-8")
    assert "{% translate 'Précédent' %}" in msgs and '{% script_word "data-msg-position" "Étape %(n)s sur %(total)s" %}' in msgs
    assert "Non renseigné" not in msgs and "'Retour'" not in msgs


@pytest.mark.django_db
def test_the_needs_step_tags_its_required_field_not_its_optional_ones(client, seeded, legal_published):
    html = client.get("/fr/entreprises/recueil-des-besoins/").content.decode()
    besoin = html[html.index('id="etape-besoin"'):html.index('id="etape-envoi"')]
    assert besoin.count("form-field__required") == 1 and 'class="form-field__optional"' not in besoin
    entreprise = html[html.index('id="etape-entreprise"'):html.index('id="etape-besoin"')]
    assert "form-field__required" not in entreprise
    # the privacy link and its shield are said once — beside the consent, not again in the side
    side = html[html.index('<aside class="formwork__side"'):]
    side = side[:side.index("</aside>")]
    assert "Privacy" not in side and "#icon-shield" not in side and html.count("form-step__privacy") == 1
    # the ILE drawings head the steps
    for symbol in ("ile-referent", "ile-need", "ile-review"):
        assert f"#icon-{symbol}" in html


def test_the_script_never_keeps_a_value_and_opens_no_step_past_an_empty_one():
    steps = (STATIC / "js" / "src" / "steps.js").read_text(encoding="utf-8")
    review = (STATIC / "js" / "src" / "steps-review.js").read_text(encoding="utf-8")
    assert "sessionStorage" not in steps + review and "localStorage" not in steps + review, "no personal datum stored"
    assert "api.validate(steps[at], true)" in steps, "a deep link opens no step past the first one still empty"
    assert 'head.setAttribute("aria-hidden", "true")' in steps and "link.tabIndex = -1" in steps
    assert "msgRequired" in review and "is-missing" in review, "a required empty answer is an error with its way back"
    assert "Lang`]" in steps, "a word still in French says its language"


def test_the_console_need_s_actions_are_one_row_cancel_then_the_primary():
    template = (ROOT / "templates" / "companies" / "need_form.html").read_text(encoding="utf-8")
    actions = template[template.index('<div class="form__actions">'):]
    assert actions.index("form__cancel") < actions.index('type="submit"'), "Annuler, then the one primary at the end"
    css = (STATIC / "css" / "v5" / "_steps.css").read_text(encoding="utf-8")
    assert "[data-steps-last] > .form__actions { display: flex; flex-wrap: wrap;" in css
    assert "> .steps-nav__back { margin-inline-end: auto; }" in css


# ---- round 2 (v515-b-improve2) -----------------------------------------------------------------------------------
def test_a_script_word_with_a_placeholder_is_the_catalogue_s_and_says_its_language():
    """{% translate %} escapes «%» before its lookup: «Étape %(n)s sur %(total)s» rendered its French source in every
    language while gettext() said «translated». {% script_word %} asks gettext() for the value and the language."""
    with translation.override("ar"):
        word = ile_forms.script_word("data-msg-position", "Étape %(n)s sur %(total)s")
        assert "الخطوة" in word and "-lang" not in word, word
        unknown = ile_forms.script_word("data-msg", "%(n)s mots que le catalogue ne connaît pas (test).")
        assert unknown.endswith(' data-msg-lang="fr"')
    with translation.override("fr"):
        assert ile_forms.script_word("data-msg-position", "Étape %(n)s sur %(total)s") == ' data-msg-position="Étape %(n)s sur %(total)s"'
    fields = (ROOT / "templates" / "components" / "form_field.html").read_text(encoding="utf-8")
    msgs = (ROOT / "templates" / "components" / "_steps_msgs.html").read_text(encoding="utf-8")
    for source in (fields, msgs):
        assert not re.search(r"\{% translate '[^']*%\(", source), "a word with a placeholder goes through script_word"
    js = (STATIC / "js" / "src" / "fieldcheck.js").read_text(encoding="utf-8")
    assert "summary.dataset.msgLang" in js and "msgNearLang" in js
    assert "msgCountLang" in (STATIC / "js" / "src" / "combobox.js").read_text(encoding="utf-8")


@pytest.mark.django_db
def test_the_arabic_needs_page_says_the_position_in_arabic_and_marks_no_translated_container(client, seeded, legal_published):
    html = client.get("/ar/entreprises/recueil-des-besoins/").content.decode()
    form = re.search(r'<form[^>]+id="formulaire-recueil-des-besoins"[^>]*>', html).group(0)
    assert re.search(r'data-msg-position="الخطوة', form) and "data-msg-position-lang" not in form
    nav = re.search(r'<nav class="steps-rail"[^>]*>', html).group(0)
    assert "lang=" not in nav and 'aria-labelledby="steps-rail-name"' in nav, "no lang on a container of translated labels"
    aside = re.search(r'<aside class="formwork__side[^"]*"[^>]*>', html).group(0)
    assert "lang=" not in aside and 'aria-labelledby="formwork-side-name"' in aside
    assert re.search(r'<span id="steps-rail-name" hidden( lang="fr")?>', html)


@pytest.mark.django_db
def test_the_short_fields_pair_by_meaning_and_the_details_gather_under_a_sub_head(client, seeded, legal_published):
    with translation.override("fr"):
        steps = {step["key"]: step for step in ile_forms.form_steps(CompanyNeedsForm())}
    rows = [[b.name for b in row] for row in steps["entreprise"]["rows"]]
    assert ["sector", "headquarters"] in rows and ["email", "phone"] in rows
    besoin = steps["besoin"]
    assert [[b.name for b in row] for row in besoin["rows"]] == [["profiles_needed"]]
    assert str(besoin["more_label"]) == "Précisions facultatives"
    # F1: like pairs with like — the two pairs of text areas; the single lines stand alone
    assert [[b.name for b in row] for row in besoin["more"]] == [
        ["indicative_headcount"], ["qualifications_required", "experience_required"],
        ["language_requirements", "training_needs"], ["indicative_timeline"], ["notes"]]
    # never reordered: rows + details read back the prescribed order
    flat = [b.name for step in steps.values() for row in step["rows"] + step["more"] for b in row]
    assert flat == [*CompanyNeedsRequest.DATA_FIELDS, "consent"]
    html = client.get("/fr/entreprises/recueil-des-besoins/").content.decode()
    assert html.count('class="form-step__pair"') == 4 and 'class="form-step__more" role="group"' in html
    assert html.count("css/dist/core/steps.css") == 1, "the steps' own sheet, once"


def test_the_composition_is_one_measure_and_the_console_side_is_paper():
    formwork = (STATIC / "css" / "v5" / "_formwork.css").read_text(encoding="utf-8")
    steps = (STATIC / "css" / "v5" / "_steps.css").read_text(encoding="utf-8")
    # V5.29 («layout & brand refinement» §1, the owner's 6 Nov 2026): the formwork is the shell's width (--form-wide,
    # v5/tokens.css — the letterhead's and the content's one system, never a width of its own), its measure 60rem
    # (46rem left the wider paper half empty) and its fields on two columns from 36rem, a line field one cell — the
    # same one measure, held where the steps' rule, the fields, the review and the actions end
    assert "--measure: 60rem" in formwork and "> :not(.steps-head) { max-inline-size: var(--measure); }" in formwork
    assert "max-inline-size: var(--form-wide);" in formwork and "71rem" not in formwork, "one horizontal system"
    assert ".formwork :is(.form-step__body, .form-step__pair) { grid-template-columns: repeat(2, minmax(0, 1fr)); }" in formwork
    assert ".formwork .form-step__body > .form-field--text { grid-column: 1; }" in formwork, "a line field is never stretched"
    assert "max-inline-size: 30rem" not in formwork, "one measure per step (no ragged edge)"
    assert ".formwork__side:not(:has(.formwork__notes)) { display: none; }" in formwork, "no empty night band"
    assert ".formwork--console .formwork__side { border-radius: var(--radius-xl); background: var(--surface-sheet);" in steps
    assert ".formwork .steps-head { margin: calc(-1 * var(--pad))" in steps and "\n.steps-head { margin: 0 0 var(--s-6); }" in steps, \
        "the night strip only inside a formwork (--pad); the sign-up's rail on the sheet"
    assert '.steps-rail__link[aria-disabled="true"] { color: GrayText; }' in steps


def test_the_glyph_light_runs_from_the_reading_corner_and_the_referent_stands_in_the_doorway():
    css = (STATIC / "css" / "v5" / "_glyph.css").read_text(encoding="utf-8")
    assert "transform: scaleX(0.55);" in css and "transition: transform 320ms" in css
    assert ".form-step:focus-within > .form-step__legend .glyph-tile::after { transform: scaleX(1); }" in css
    assert "inset 0 0 0 1px var(--line-structure)" not in css.split(".glyph-tile::after")[0], "a seal, not an outlined box"
    referent = (STATIC / "icons" / "src" / "ile-referent.svg").read_text(encoding="utf-8")
    assert 'fill-opacity=".18"' in referent and "a7 7 0 0 1 14 0" in referent


# ---- in Chromium (``-m browser``) ----------------------------------------------------------------------------
@pytest.fixture(scope="module")
def browser():
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as p:
        try:
            instance = p.chromium.launch()
        except Exception as exc:  # pragma: no cover - browser not installed
            pytest.skip(f"Chromium not available: {exc}")
        yield instance
        instance.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang,width", [("fr", 1440), ("ar", 390)])
def test_the_needs_form_is_asked_step_by_step_and_reviewed(browser, live_server, seeded, legal_published, lang, width):
    """One step at a time; «Continuer» checks the step in the server's words and stays; a filled step moves on and the
    address says it; the last step opens on the review and brings back the locked button with «Retour»."""
    context = browser.new_context(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    try:
        page.goto(f"{live_server.url}/{lang}/entreprises/recueil-des-besoins/", wait_until="networkidle")
        visible = "() => [...document.querySelectorAll('.form-step')].filter(s => !s.hidden).map(s => s.dataset.step)"
        assert page.evaluate(visible) == ["entreprise"]
        assert not page.locator(".form__actions button[type=submit]").is_visible(), "the locked button waits for the last step"
        page.locator(".steps-nav__next").click()
        assert page.evaluate(visible) == ["entreprise"] and page.locator(".form-field--error").count() >= 5
        assert page.evaluate("document.activeElement.id") == "id_company_name"
        for name, value in (("company_name", "Officine (synthétique)"), ("sector", "Métallurgie"), ("headquarters", "Valfiorita"),
                            ("contact_name_and_role", "RH"), ("email", "rh@example.test")):
            page.fill(f"#id_{name}", value)
        page.locator(".steps-nav__next").click()
        assert page.evaluate(visible) == ["besoin"] and "etape=besoin" in page.url
        page.fill("#id_profiles_needed", "Soudeurs")
        page.locator(".steps-nav__next").click()
        assert page.evaluate(visible) == ["envoi"]
        review = page.locator(".form-review__part")
        # the review is drawn by steps-review.js, fetched on reaching the last step: wait for its first part (the
        # v515-b merge: on the merged tree the module could land after an immediate count, at ar 390)
        review.first.wait_for(state="attached", timeout=5000)
        assert review.count() == 2 and "Officine (synthétique)" in review.first.inner_text()
        assert page.locator(".form__actions button[type=submit]").is_visible()
        assert page.locator(".form__actions .steps-nav__back").count() == 1
        page.locator(".form-review__edit").first.click()
        assert page.evaluate(visible) == ["entreprise"]
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        assert errors == []
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_tabbing_through_a_step_says_nothing_and_continuer_still_names_every_empty_field(
    browser, live_server, seeded, legal_published, lang
):
    """V5.32 correction round, the integration review's P2-9: a keyboard tabbing through the first step's empty fields,
    before typing anything, turns nothing red and no live row speaks; «Continuer» still checks the step in the
    server's words — every empty required field named, and only those, the focus on the first — as before."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    said = """() => {
      const step = document.querySelector(".form-step[data-step='entreprise']");
      const id = (w) => w.querySelector('input:not([type=hidden]), select, textarea').id;
      return {errors: [...step.querySelectorAll('.form-field--error')].map(id),
              required: [...step.querySelectorAll('[data-field].form-field--required')].map(id),
              invalid: step.querySelectorAll('[aria-invalid="true"]').length,
              spoken: [...step.querySelectorAll('[data-field-msg]')].map((r) => r.textContent.trim()).filter(Boolean)};
    }"""
    try:
        page.goto(f"{live_server.url}/{lang}/entreprises/recueil-des-besoins/", wait_until="networkidle")
        page.focus("#id_company_name")
        for _ in range(40):
            page.keyboard.press("Tab")
            if page.evaluate("() => document.activeElement.classList.contains('steps-nav__next')"):
                break
        else:  # pragma: no cover - «Continuer» is reached from the keyboard
            pytest.fail("«Continuer» never reached by the keyboard")
        before = page.evaluate(said)
        assert len(before["required"]) >= 5 and before["errors"] == [], before
        assert before["invalid"] == 0 and before["spoken"] == [], before
        page.keyboard.press("Enter")
        after = page.evaluate(said)
        assert after["errors"] == after["required"], "«Continuer» names every empty required field, and only those"
        assert after["invalid"] == len(after["required"]) and len(after["spoken"]) == len(after["required"]), after
        assert page.evaluate("document.activeElement.id") == "id_company_name"
        assert errors == []
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_new_password_checklist_follows_the_typing(browser, live_server, seeded, legal_published):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    try:
        page.goto(f"{live_server.url}/fr/compte/signup/", wait_until="networkidle")
        page.locator(".choice").first.click()
        page.locator(".steps-nav__next").click()
        met = "() => [...document.querySelectorAll('.pw-rule')].map(r => r.dataset.met || '')"
        page.fill("#id_password1", "12345678")
        assert page.evaluate(met).count("1") == 0
        page.fill("#id_password1", "Une-longue-phrase-2026")
        assert page.evaluate(met).count("1") == 2
        page.wait_for_function("() => document.querySelector('[data-pw-summary]').textContent.includes('2')")
        assert page.evaluate("document.querySelectorAll('#icon-check, .pw-rule use').length") == 0, "no tick (O14)"
    finally:
        context.close()
