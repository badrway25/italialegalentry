"""
The form system of V5.12 W2 (lane B; DECISIONS §5): one field partial, its anatomy and states, the inline check's
messages, the choice cards, the date and number components, the combobox's hook, the country list, the page-only
assets and their budgets.
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from django import forms
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.utils import translation

from core import countries, icons
from core.templatetags import ile_forms

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"


class DemoForm(forms.Form):
    email = forms.EmailField(label="Adresse e-mail", help_text="Aide")
    phone = forms.CharField(label="Téléphone", required=False, widget=forms.TextInput(attrs={"type": "tel"}))
    message = forms.CharField(label="Message", max_length=200, widget=forms.Textarea)
    country = forms.ChoiceField(label="Pays", choices=[("", "—"), *countries.choices("fr")], required=False)
    kind = forms.ChoiceField(label="Type", choices=[("a", "A"), ("b", "B")], widget=forms.RadioSelect)
    langs = forms.MultipleChoiceField(
        label="Langues", choices=[("fr", "FR"), ("it", "IT")], widget=forms.CheckboxSelectMultiple, required=False
    )
    born = forms.DateField(label="Date", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    years = forms.IntegerField(label="Années", min_value=0, max_value=60, required=False)
    reference = forms.CharField(label="Référence", required=False, widget=forms.TextInput(attrs={"readonly": True}))
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation", widget=forms.PasswordInput)
    consent = forms.BooleanField(label="J’accepte")


def _render(form, name, **extra):
    request = RequestFactory().get("/")
    with translation.override("fr"):
        return render_to_string("components/form_field.html", {"field": form[name], "request": request, **extra})


def test_no_asterisk_the_optional_minority_is_marked_and_required_controls_keep_required():
    form = DemoForm()
    email = _render(form, "email")
    phone = _render(form, "phone")
    assert "*" not in re.sub(r"<[^>]+>", "", email), "a required field carries no asterisk (DECISIONS §5.3)"
    assert "form-field__required" not in email and 'class="form-field__optional"' not in email
    assert " required" in email and "form-field--required" in email
    assert '<span class="form-field__optional">facultatif</span>' in phone and "form-field--optional" in phone
    consent = _render(form, "consent")
    assert "facultatif" not in consent and "*" not in re.sub(r"<[^>]+>", "", consent)
    for path in (ROOT / "templates").rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if "dev" in path.relative_to(ROOT / "templates").parts or path.name == "depot.html":
            continue
        assert "Les champs marqués d’un astérisque" not in text, path
        assert 'class="form-field__required"' not in text, path


def test_the_field_anatomy_label_control_slots_help_and_one_live_message_row():
    form = DemoForm(data={"email": "invalide"})
    form.is_valid()
    html = _render(form, "email")
    assert html.index('class="form-field__label"') < html.index("<input") < html.index('class="form-field__help"')
    assert 'class="form-field__control form-field__control--glyph"' in html and "#icon-at-sign" in html
    assert '<span class="form-field__status" aria-hidden="true"><svg' in html and "#icon-circle-alert" in html
    assert html.count('aria-live="polite"') == 1 and 'class="form-field__msg"' in html
    assert '<div class="form-field__errors" id="id_email_error"><ul class="form-field__error-list">' in html
    assert 'aria-describedby="id_email_helptext id_email_error"' in html and 'aria-invalid="true"' in html
    pristine = _render(DemoForm(), "email")
    assert "aria-invalid" not in pristine and "form-field__errors" not in pristine
    assert 'class="form-field__msg"' in pristine, "the row is always there, so the inline check writes into it"
    assert '#icon-phone' in _render(DemoForm(), "phone")
    readonly = _render(DemoForm(), "reference")
    assert "form-field--readonly" in readonly and "#icon-lock" in readonly


def test_the_inline_check_reads_the_servers_own_messages():
    with translation.override("fr"):
        html = _render(DemoForm(), "email")
        message = _render(DemoForm(), "message")
        years = _render(DemoForm(), "years")
    assert 'data-msg-required="Ce champ est obligatoire."' in html
    assert "data-msg-type=" in html and "valide" in html.split("data-msg-type=", 1)[1].split('"', 2)[1]
    assert 'data-msg-max="' in message and "{n}" in message and "200" in message
    assert 'data-count-of="id_message" data-max="200"' in message and "data-msg-near=" in message
    assert 'data-msg-low="' in years and 'data-msg-high="' in years
    password2 = _render(DemoForm(), "password2")
    assert 'data-match="id_password1"' in password2 and "data-msg-matched=" in password2 and "data-msg-caps=" in password2
    assert "data-match" not in _render(DemoForm(), "password1")


def test_choice_cards_are_the_one_choice_component():
    form = DemoForm(data={})
    form.is_valid()
    radios = _render(form, "kind")
    assert re.search(r"<fieldset class=\"choices[^>]*data-field data-choices", radios)
    assert 'class="choices choices--error form-field--error"' in radios and "data-choices" in radios
    assert radios.count('class="choice"') == 2 and radios.count("#icon-check") == 2
    assert 'id="id_kind_error"' in radios and 'aria-describedby="' in radios
    boxes = _render(DemoForm(), "langs")
    assert 'class="choices__hint" id="id_langs_hint"' in boxes and "facultatif" in boxes
    alias = (ROOT / "templates" / "components" / "option_cards.html").read_text(encoding="utf-8")
    assert 'include "components/choice_cards.html"' in alias, "OptionCard is an alias of the choice cards"
    step = (ROOT / "templates" / "orientation" / "_step.html").read_text(encoding="utf-8")
    assert 'class="choice wizard__choice"' in step and 'class="choice__mark"' in step, "the questionnaire draws choice cards"
    wizard = (ROOT / "apps" / "orientation" / "static" / "orientation" / "wizard.css").read_text(encoding="utf-8")
    assert '@import url("../css/v5/_choice.css");' in wizard


def test_the_signup_offers_the_audiences_as_cards_with_their_glyphs():
    from accounts.forms import SignupForm

    with translation.override("fr"):
        form = SignupForm()
        html = _render(form, "account_type")
    assert isinstance(form.fields["account_type"].widget, forms.RadioSelect)
    for glyph in ("person", "building", "institution", "university", "briefcase"):
        assert f"#icon-{glyph}" in html, glyph
    assert "choices--glyphs" in html and html.count('class="choice"') == 5


def test_date_number_and_long_select_components():
    date = _render(DemoForm(), "born")
    assert "data-date" in date and 'type="date"' in date, "without the script the native date input is used"
    assert 'data-label-day="Jour"' in date and 'data-label-month="Mois"' in date and 'data-label-year="Année"' in date
    number = _render(DemoForm(), "years")
    assert "data-number" in number and number.count("data-step=") == 2 and number.count(" hidden>") == 2
    assert 'min="0"' in number and 'max="60"' in number
    country = _render(DemoForm(), "country")
    assert "data-combobox" in country and "<select" in country, "a select of more than 15 options is enhanced"
    assert "data-combobox" not in _render(DemoForm(), "kind")


def test_one_announcement_channel_no_alert_inside_the_live_row():
    """Review W2 (minor): the row is aria-live and held a role=alert error — said twice. The row is the only channel."""
    form = DemoForm(data={"email": "invalide"})
    form.is_valid()
    html = _render(form, "email")
    row = re.search(r'<div class="form-field__msg" aria-live="polite" data-field-msg>.*?</div></div>', html, re.S)
    assert row and "form-field__errors" in row.group(0) and 'role="alert"' not in row.group(0)
    for rel in ("components/_field_msg.html", "allauth/elements/field.html"):
        text = (ROOT / "templates" / rel).read_text(encoding="utf-8")
        assert '<div class="form-field__errors" id=' in text and 'role="alert">' not in text, rel
    source = (STATIC / "js" / "src" / "fieldcheck.js").read_text(encoding="utf-8")
    assert "[role=alert]" not in source and '"alert"' not in source
    # a fragment fetched by script: its inert module script is documented, and the host's hook is there
    assert 'document.addEventListener("fields:load"' in source
    assert "fields:load" in (STATIC / "js" / "dist" / "fieldcheck.js").read_text(encoding="utf-8")

def test_the_assets_come_once_per_response_and_only_with_a_field():
    request = RequestFactory().get("/")
    tpl = Template("{% load ile_forms %}{% form_assets %}{% form_assets %}")
    html = tpl.render(Context({"request": request}))
    assert html.count("css/dist/core/forms.css") == 1 and html.count("js/dist/fieldcheck.js") == 1
    assert 'type="module"' in html
    page = Template("{% load ile_forms %}{% for f in form %}{% include 'components/form_field.html' with field=f %}{% endfor %}")
    with translation.override("fr"):
        rendered = page.render(Context({"form": DemoForm(), "request": RequestFactory().get("/")}))
    assert rendered.count("fieldcheck.js") == 1


def test_budgets_form_js_and_the_page_only_sheet():
    js = sum(len(gzip.compress((STATIC / "js" / "dist" / n).read_bytes(), 9)) for n in ("fieldcheck.js", "combobox.js"))
    assert js <= 6 * 1024, f"form-page JS {js} B gzip > 6 KB (DECISIONS «Lane B» acceptance 8)"
    sheet = len(gzip.compress((STATIC / "css" / "dist" / "core" / "forms.css").read_bytes(), 9))
    assert sheet <= 6 * 1024, f"the form sheet {sheet} B gzip > 6 KB"
    main = (STATIC / "css" / "main.css").read_text(encoding="utf-8")
    assert "_form.css" not in main and "forms.css" not in main, "the form system is page-only"
    source = (STATIC / "js" / "src" / "fieldcheck.js").read_text(encoding="utf-8")
    assert "innerHTML" not in source and "eval(" not in source and "style." not in source


def test_motion_m10_m14_and_reduced_motion():
    css = (STATIC / "css" / "v5" / "_form.css").read_text(encoding="utf-8")
    assert "grid-template-rows: 0fr" in css and "grid-template-rows: 1fr" in css and "160ms" in css
    choice = (STATIC / "css" / "v5" / "_choice.css").read_text(encoding="utf-8")
    assert "transform: scale(0.8)" in choice and "transform: scale(1)" in choice and '@import url("_choice.css");' in css
    assert not re.search(r"@keyframes|animation\s*:", choice)
    assert "prefers-reduced-motion: reduce" in css and 'html[data-input="key"]' in css
    assert not re.search(r"@keyframes|animation\s*:", css), "nothing loops, shakes or pulses"
    assert not re.search(r"(?<![\w-])(margin|padding)-(left|right)\s*:|(?<![\w-])(left|right)\s*:", css)


def test_countries_are_cldr_in_four_languages_and_match_free_text():
    assert len(countries.COUNTRIES) >= 240 and countries.CLDR_VERSION
    assert {"MA", "IT", "FR", "TN", "SN"} <= countries.CODES and "EU" not in countries.CODES
    assert countries.name("MA", "fr") == "Maroc" and countries.name("MA", "it") == "Marocco"
    assert countries.name("MA", "ar") == "المغرب" and countries.name("MA", "en") == "Morocco"
    assert countries.match("maroc") == "MA" and countries.match("Côte d’Ivoire") == "CI" and countries.match("المغرب") == "MA"
    assert countries.match("ma") == "MA" and countries.match("Atlantide") == ""
    names = [n for _c, n in countries.choices("fr")]
    assert names.index("Albanie") < names.index("Algérie") < names.index("Égypte") < names.index("Zimbabwe")
    licence = (ROOT / "apps" / "core" / "LICENSE-CLDR.txt").read_text(encoding="utf-8")
    assert "UNICODE LICENSE V3" in licence and "Unicode-3.0" in licence


@pytest.mark.django_db
def test_the_person_profile_stores_iso_codes_for_the_rules():
    from accounts.profile_forms import SituationForm

    form = SituationForm(data={"nationality": "MA", "country_of_residence": "TN"})
    assert form.is_valid(), form.errors
    assert form.cleaned_data["nationality"] == "MA" and form.cleaned_data["country_of_residence"] == "TN"
    assert not SituationForm(data={"nationality": "Atlantide"}).is_valid()


def test_the_icon_registry_draws_every_glyph_the_form_system_names():
    for name in ("at-sign", "phone", "lock", "circle-alert", "warning", "check", "minus", "plus"):
        assert icons.SPRITE_OF[name] == icons.SPRITE, f"{name}: a form glyph is the chrome sprite's"
    assert ile_forms.LEADING_GLYPHS == {"email": "at-sign", "tel": "phone"}
