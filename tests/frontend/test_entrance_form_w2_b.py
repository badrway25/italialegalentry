"""
The entrance «Il varco» — the form (V5.4 plan §1.13; acceptance L1–L6, L8, L11, L14; W2-B, step 2).

On the sources and with Django's client (fast, offline):
* ONE hierarchy on every entrance page: the eyebrow with the key and the words of the letterhead's plate, one title,
  at most one primary action; a page that is not a form leads back to the sign-in, a form never does;
* the sign-in's page extends allauth's own template — the view, the fields, the CSRF token and the redirect field
  are allauth's, at the installed version — and restates none of its messages;
* the assurance under the action is the locked answer of the FAQ on data protection, verbatim, with the FAQ's own
  link after it; it waits for Phase 3, and it is marked French on a page that is not;
* the «forgotten password» link is allauth's own help text, written AFTER the control (the keyboard goes from the
  address to the password) and placed in the label's row by the sheet; it keeps the help's id;
* the sheet: the form is a column on the paper, not a card, hung from the top of its panel and never centred on its
  own height; the primary that completes a sign-in holds, at rest, the very key the loader turns — the same mask;
  the sheet adds no motion of its own to the form.

In Chromium (``-m browser``):
* L1 — typed text is 16 px in every field of the entrance, fr and ar, at every width;
* L2 — fields and the primary are 52 px, every target of the form is at least 24 px (44 px under a finger, without
  lying over the field below), and a password shown at 360 px has room for 20 characters, 16 at 320;
* L5 — the action is in the first viewport at 360 × 640 in the four languages;
* L6 — from the keyboard: the address, the password, its show / hide control, the reset link, the action;
* the title stands at the same height on every entrance page; the column is not a card; nothing overflows from 320
  to 430 px;
* L14 — the primary computes flat, and holds the key at rest only where a sign-in completes; on submit the key the
  person was looking at turns, in the same box, and the label does not move (L8);
* L4 — a refused sign-in's page: the focus on the summary, both fields described by it, no red edge, no list of
  nothing; a field's own error is its edge, its mark and its words;
* a session message stands in the form's column, and the stage still meets the letterhead.
The stage is tests/frontend/test_entrance_w2_b.py; the allauth flows are apps/accounts/tests/test_login_form_w2_b.py;
the Arabic page is tests/i18n/test_rtl_browser_entrance.py.
"""

from __future__ import annotations

import html as html_lib
import os
import re
from pathlib import Path

import pytest
from allauth.account.models import EmailAddress
from django.conf import settings
from django.test import Client
from django.utils import translation
from django.utils.translation import gettext

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

ROOT = Path(__file__).resolve().parents[2]
LAYOUT = ROOT / "templates" / "allauth" / "layouts" / "entrance.html"
LOGIN_PAGE = ROOT / "templates" / "account" / "login.html"
FIELD = ROOT / "templates" / "components" / "form_field.html"
SHEET = ROOT / "apps" / "accounts" / "static" / "accounts" / "entrance.css"
LOADER = ROOT / "static" / "css" / "v5" / "loader.css"
TOKENS = ROOT / "static" / "css" / "v5" / "tokens.css"
SHELL = ROOT / "static" / "js" / "src" / "shell.js"

PASSWORD = "Str0ng-Passw0rd-2026!"
#: Entrance pages an anonymous visitor reaches, and whether the page is a form (the signup: its form, or the
#: message of a closed registration — the gate of the public forms decides, so the page itself says which).
PAGES = {
    "login": ("/{lang}/compte/login/", True),
    "signup": ("/{lang}/compte/signup/", None),
    "reset": ("/{lang}/compte/password/reset/", True),
    "reset-done": ("/{lang}/compte/password/reset/done/", False),
    "verification-sent": ("/{lang}/compte/confirm-email/", False),
    "inactive": ("/{lang}/compte/inactive/", False),
    "bad-confirmation": ("/{lang}/compte/confirm-email/not-a-key/", False),
}
SUBMIT = ".varco .form__actions .btn--primary"


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)


def _body(template: Path) -> str:
    return re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", _read(template), flags=re.S)


def _rules(css: str) -> list[tuple[str, str]]:
    return [(" ".join(selector.split()), body) for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)]


def _focus(html: str) -> str:
    """The form's panel of an entrance page."""
    return html.split('class="varco__focus"', 1)[1].split("data-varco-stage", 1)[0]


def _text(fragment: str) -> str:
    return " ".join(html_lib.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


# ----------------------------------------------------------------------------------------- the hierarchy


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar", "it", "en"])
def test_every_entrance_page_has_one_hierarchy(client, seeded, lang):
    with translation.override(lang):
        place = gettext("Espace réservé")
        back = gettext("Se connecter")
    for name, (path, is_form) in PAGES.items():
        html = client.get(path.format(lang=lang)).content.decode()
        focus = _focus(html)
        if is_form is None:
            is_form = 'id="id_password1"' in focus
        sheet = focus.split('class="account-page__main varco__sheet">', 1)[1]
        # the eyebrow first: the key of the letterhead's plate, and its words
        eyebrow = re.match(r'\s*<p class="varco__eyebrow">(.*?)</p>', sheet, re.S)
        assert eyebrow, (name, lang, sheet[:200])
        assert "#icon-ile-key" in eyebrow.group(1) and 'aria-hidden="true"' in eyebrow.group(1), (name, lang)
        assert _text(eyebrow.group(1)) == place, (name, lang)
        # then ONE title, and at most one primary action
        assert focus.count("<h1") == 1 and html.count("<h1") == 1, (name, lang)
        assert focus.index("varco__eyebrow") < focus.index("<h1"), (name, lang)
        assert focus.count("btn btn--primary") == (1 if is_form else 0), (name, lang, focus.count("btn btn--primary"))
        # a page that is not a form leads back to the sign-in; a form never does
        way = re.search(r'<p class="varco__back">(.*?)</p>', focus, re.S)
        assert bool(way) is (not is_form), (name, lang)
        if way:
            assert f'href="/{lang}/compte/login/"' in way.group(1) and _text(way.group(1)) == back, (name, lang)
            assert focus.rindex("varco__back") > focus.index("</h1>"), "the way back comes last"
        assert not re.search(r"\sstyle=|<style", focus), (name, lang)


@pytest.mark.django_db
def test_a_signed_in_person_is_not_shown_the_way_to_the_sign_in(client, seeded, person_user):
    client.force_login(person_user)
    html = client.get("/fr/compte/password/reset/done/").content.decode()
    assert "data-varco-stage" in html and 'class="varco__back"' not in html


@pytest.mark.django_db
def test_the_title_of_the_document_says_an_error_first(client, seeded):
    rest = client.get("/fr/compte/password/reset/").content.decode()
    assert re.search(r"<title>\s*Réinitialisation du mot de passe\s*·", rest)
    refused = client.post("/fr/compte/password/reset/", {"email": "not-an-address"}).content.decode()
    assert re.search(r"<title>\s*Erreur — \s*Réinitialisation du mot de passe\s*·", refused), "every entrance form, not the login alone"
    layout = _body(LAYOUT)
    assert '{% block page_title %}{% if form.errors %}{% translate "Erreur" %} — {% endif %}{% block head_title %}' in layout


def test_the_layout_adds_no_message_of_its_own():
    """The eyebrow, the error's word and the way back are strings the product already says elsewhere."""
    messages = set(re.findall(r'\{% translate "([^"]+)" %\}', _body(LAYOUT)))
    assert messages == {
        "Espace réservé — accès au compte",
        "Erreur",
        "Espace réservé",
        "Se connecter",
        "Besoin d’aide ? Écrivez-nous :",
    }, messages
    for message, elsewhere in (("Espace réservé", "templates/portal/unavailable.html"), ("Se connecter", "templates/errors/403.html"), ("Erreur", "templates/errors/base_error.html")):
        assert f'{{% translate "{message}" %}}' in _read(ROOT / elsewhere), message


# ----------------------------------------------------------------------------------------- the sign-in's page


def test_the_sign_in_page_extends_allauth_s_own_template_and_restates_none_of_its_messages():
    body = _body(LOGIN_PAGE)
    assert body.lstrip().startswith('{% extends "account/login.html" %}'), "the same name, in the next template directory"
    assert body.count("{{ block.super }}") == 1 and "{% block content %}{{ block.super }}" in body
    assert re.findall(r"\{% block (\w+) %\}", body) == ["content"], "nothing of allauth's page is replaced"
    for tag in ("<form", "<input", "csrf_token", "{% element", "redirect_field"):
        assert tag not in body, f"{tag}: the form is allauth's, never a copy"
    assert re.findall(r'\{% (?:translate|trans|blocktranslate|blocktrans)\b[^%]*%\}', body) == ['{% translate "Lire la Privacy Policy" %}']
    assert '{% translate "Lire la Privacy Policy" %}' not in _body(LAYOUT)
    assert "Lire la Privacy Policy" in _read(ROOT / "apps" / "faq" / "services.py"), "the FAQ's own link, in the catalogue"


@pytest.mark.django_db
def test_the_sign_in_is_still_allauth_s_form_with_its_redirect(client, seeded):
    html = client.get("/fr/compte/login/?next=/fr/espace-reserve/mes-pieces/").content.decode()
    form = _focus(html).split('<form class="form"', 1)[1].split("</form>", 1)[0]
    assert 'method="post" action="/fr/compte/login/"' in form.split(">", 1)[0]
    assert form.count('name="csrfmiddlewaretoken"') == 1
    assert re.search(r'<input type="hidden" name="next" value="/fr/espace-reserve/mes-pieces/"', form), "the redirect field"
    assert re.findall(r'<input\b[^>]*\bname="(\w+)"', form) == ["csrfmiddlewaretoken", "login", "password", "next"]
    assert re.findall(r'<button\b[^>]*type="submit"', form).__len__() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_assurance_is_the_locked_answer_verbatim(client, seeded, phase3_open, lang):
    from cms import locked_content

    entries, effective = locked_content.get("p3.faq.items", lang)
    entry = next(item for item in entries if item["key"] == "faq_data_protection")
    html = client.get(f"/{lang}/compte/login/").content.decode()
    focus = _focus(html)
    block = re.search(r'<div class="varco__assurance" data-faq="faq_data_protection">(.*?)</div>', focus, re.S)
    assert block, "the assurance is on the sign-in's page once the FAQ is public"
    assert focus.index("varco__assurance") > focus.index("</form>"), "under the action"
    with translation.override(lang):
        more = gettext("Lire la Privacy Policy")
    link = re.search(r'<p class="varco__assurance-more"><a href="([^"]+)">(.*?)</a></p>', block.group(1))
    assert link and link.group(1) == f"/{lang}/privacy-policy/" and html_lib.unescape(link.group(2)) == more, "the link, in every language"
    if effective == lang:
        question = re.search(r'<h2 class="varco__assurance-q">(.*?)</h2>', block.group(1), re.S)
        answer = re.search(r'<p class="varco__assurance-a">(.*?)</p>', block.group(1), re.S)
        assert question and html_lib.unescape(question.group(1)) == entry["question"], "the question, verbatim, as a heading"
        assert answer and html_lib.unescape(answer.group(1)) == entry["answer"], "the answer, verbatim"
        assert "<a" not in answer.group(1), "the link stands after the locked answer, never inside it"
        assert block.group(1).index("varco__assurance-a") < block.group(1).index("varco__assurance-more")
    else:
        # French until a translation is published: a French paragraph under the action of an Arabic page reads as a
        # missing translation where it is meant to build trust (review m3) — the link alone, in the page's language
        assert lang == "ar" and effective == "fr"
        assert "varco__assurance-q" not in block.group(1) and "varco__assurance-a" not in block.group(1)
        assert entry["answer"] not in html_lib.unescape(html) and 'lang="fr"' not in block.group(1)
    assert html.count("<h1") == 1


@pytest.mark.django_db
def test_the_assurance_waits_for_phase_3_and_stays_on_the_sign_in(client, seeded, before_phase3):
    assert "varco__assurance" not in client.get("/fr/compte/login/").content.decode(), "Phase-3 content, gated as the FAQ"


@pytest.mark.django_db
def test_no_other_entrance_page_carries_the_assurance(client, seeded, phase3_open):
    for name, (path, _is_form) in PAGES.items():
        html = client.get(path.format(lang="fr")).content.decode()
        assert ("varco__assurance" in html) is (name == "login"), name


# ----------------------------------------------------------------------------------------- the fields' slot


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar", "it", "en"])
def test_the_reset_link_is_allauth_s_help_written_after_the_control(client, seeded, lang):
    html = client.get(f"/{lang}/compte/login/").content.decode()
    field = html.split('id="wrap_id_password"', 1)[1].split('<div class="form__actions">', 1)[0]
    aside = re.search(r'<span class="form-field__aside" id="id_password_helptext">(.*?)</span>', field, re.S)
    assert aside, "the password's help is the label row's aside, under the help's own id"
    with translation.override(lang):
        words = gettext("Forgot your password?")  # allauth's message, from allauth's catalogue
    assert re.fullmatch(rf'<a href="/{lang}/compte/password/reset/">{re.escape(html_lib.escape(words, quote=False))}</a>', aside.group(1).strip()) or (
        _text(aside.group(1)) == words and f'href="/{lang}/compte/password/reset/"' in aside.group(1)
    ), aside.group(1)
    if lang != "en":
        assert words != "Forgot your password?", f"{lang}: allauth's catalogue holds the link's words"
    assert "form-field__help" not in field, "…and no help line is left under the field"
    # the order of the source is the order of the keyboard: the control, its show / hide control, then the link
    assert field.index('id="id_password"') < field.index("data-password-toggle") < field.index("form-field__aside")
    assert 'aria-describedby="id_password_helptext"' in field, "the field is still described by it"
    assert html.index('id="id_login"') < html.index('id="id_password"') < html.index("form-field__aside") < html.index('type="submit"')


@pytest.mark.django_db
def test_a_help_that_is_a_list_stays_inside_its_help(client, seeded, legal_published):
    """The rules of a new password are a <ul>: written inside a <p> it closed the paragraph, the id was left on an empty
    element and the list outside the help's style (the signup, once its gate is open: the legal pages published)."""
    html = client.get("/fr/compte/signup/").content.decode()
    assert 'id="id_password1"' in html, "the registration is open in this test"
    assert re.search(r'<div class="form-field__help" id="id_password1_helptext"><ul>.*?</ul></div>', html, re.S)
    assert not re.search(r"<p[^>]*>\s*<ul", html)
    assert 'placeholder="' not in _focus(html), "the signup's labels are above its fields: no placeholder"
    assert "form-field__aside" not in html, "only a form that asks for it has a help beside its label"


def test_the_slot_and_the_help_in_the_component():
    body = _body(FIELD)
    assert (
        '{% if help %}<div class="form-field__help" id="{{ field.auto_id }}_helptext">{{ help }}</div>'
        '{% elif field.help_text and field.field.help_beside_label %}<span class="form-field__aside" id="{{ field.auto_id }}_helptext">{{ field.help_text }}</span>'
        '{% elif field.help_text %}<div class="form-field__help" id="{{ field.auto_id }}_helptext">{{ field.help_text }}</div>{% endif %}'
    ) in body
    assert "<p class=\"form-field__help\"" not in body
    control = body.index('<div class="form-field__control form-field__control--password')
    assert control < body.index("form-field__aside") < body.index("form-field__errors"), "after the control, before the errors"


# ----------------------------------------------------------------------------------------- the sheet


def test_the_form_is_a_column_on_the_paper_hung_from_the_top_of_its_panel():
    sheet = _css(SHEET)
    rules = _rules(sheet)
    column = [body for selector, body in rules if selector == ".varco__sheet"]
    assert column and all(not re.search(r"background|border|box-shadow|padding", body) for body in column), "not a card"
    assert any("max-inline-size: 25rem;" in body for body in column)
    focus = [body for selector, body in rules if selector == ".varco__focus"]
    assert focus and "background-color: var(--surface-page);" in focus[0] and "align-content: start;" in focus[0]
    assert not any("align-content: center" in body for body in focus), "never centred on its own height"
    assert any("padding-block: clamp(var(--s-12), 14vh - 1rem, 12rem) var(--s-16);" in body for body in focus), (
        "from 64rem the distance from the letterhead is the screen's, never the form's"
    )
    assert "background-image" not in "".join(focus), "the paper is flat: no light is painted on it"
    for retired in ("--min-", "--ink", "--hairline", "--light-focus", "--radius-xl", "--shadow-2", ".account-page__aside"):
        assert retired not in sheet, f"{retired}: a V4 name of the old sheet"


def test_the_primary_is_the_system_s_flat_primary_and_holds_the_loader_s_key():
    sheet, loader = _css(SHEET), _css(LOADER)
    rules = _rules(sheet)
    primary = next(body for selector, body in rules if selector == ".varco .form__actions .btn--primary")
    for declaration in ("--btn-box-h: var(--control-lg);", "--btn-pad: var(--btn-pad-lg);", "justify-self: stretch;", "font-size: var(--t-field);"):
        assert declaration in primary, declaration
    holder = next(body for selector, body in rules if selector == ".varco form[data-loader-host] .form__actions .btn--primary")
    for declaration in ("--btn-pad: var(--control-lg);", "--btn-pad-end: var(--control-lg);"):
        assert declaration in holder, f"{declaration} the label centred on the plate, the end pad the key's seat"
    for body in (primary, holder):
        assert not re.search(r"background|box-shadow|border|gradient|filter", body), "the fill, the edge and the press are the system's"
    key_rule = ".varco form[data-loader-host] .form__actions .btn--primary::after"
    key = next(body for selector, body in rules if selector == key_rule)
    # the very mask the loader turns — one key at rest and busy — written ONCE: the token of v5/tokens.css, read by
    # both sheets (the performance check's P1: the entrance's sheet carried a second copy, ≈ 220 B gzip)
    tokens = _css(TOKENS)
    declared = re.findall(r'--key-mask: (url\("data:image/svg\+xml,[^"]+"\));', tokens)
    assert len(declared) == 1 and "viewBox='10 11 40 94'" in declared[0], "key.svg cropped symmetric about its shaft"
    for name, css in (("entrance.css", sheet), ("loader.css", loader)):
        assert "--key-mask:" not in css and "data:image/svg+xml" not in css, f"{name} writes the key's mask a second time"
    busy = next(body for selector, body in _rules(loader) if selector == ".btn.is-busy::after")
    for shared in (
        "inset-block-start: 50%;",
        "inline-size: var(--key-inline);",
        "block-size: var(--key-size);",
        "translate: 0 -50%;",
        "background: currentColor;",
        "mask: var(--key-mask) center / contain no-repeat;",
    ):
        assert shared in key and shared in busy, f"the key at rest and the busy key part: {shared}"
    assert "inset-inline-end: calc((var(--btn-pad-end) - var(--key-inline)) / 2);" in key, "the middle of the end pad"
    assert "--key-size: 18px;" in holder and "--key-inline: calc(var(--key-size) * 40 / 94);" in holder
    assert "--key-size: 18px;" in next(body for selector, body in _rules(loader) if ".btn.is-busy" in selector and "::after" not in selector)
    assert not re.search(r"animation|opacity|transition", key), "its turn and its dim face are the loader's alone"
    forced = sheet.split("@media (forced-colors: active)", 1)[1]
    assert re.search(re.escape(key_rule) + r" \{\s*forced-color-adjust: none;\s*background: ButtonText;", " ".join(forced.split()))


def test_the_form_s_rules_move_nothing_and_read_tokens():
    """What moves on the form is the system's (the field's rule, the press, the key): this sheet adds no transition
    and no animation to it, and — as for the stage — no literal colour and no gradient."""
    sheet = _css(SHEET)
    form = sheet.split(".varco__focus {", 1)[1].split("@media (min-width: 48rem)", 1)[0]
    assert not re.search(r"(?<![\w-])(?:animation|transition)\s*:", form)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|gradient\(", form)
    assert not re.search(r"(?<![\w-])(?:left|right|margin-left|margin-right|padding-left|padding-right)\s*:", form), "logical properties"
    assert ".varco .form ::placeholder { color: transparent; }" in " ".join(form.split())
    # the sheet draws no control (W1-C: «the entrance draws no field of its own»): no rule names a field's input,
    # select or textarea — what it adds is said of the form, of the field's parts, or of what a control is for (a
    # password's control, a one-time code)
    assert not re.search(r"\.form-field[^{]*(input|select|textarea)[^{]*\{", sheet), "entrance.css draws no control"
    for declaration in ("min-block-size: var(--field-h)", "border-radius: var(--field-radius)", "background-color: var(--field-bg)"):
        assert declaration not in sheet, f"the plate is the system's: {declaration}"
    assert ".varco .form:not(:has(.form-field:not(.form-field--required))) .form-field__required { display: none; }" in " ".join(form.split())
    assert "@supports (grid-template-rows: subgrid)" in form and ".page-entrance main:has(> .messages)" in form


# ---------------------------------------------------------------------------------------------- in Chromium


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


def _page(browser, width=1440, height=900, touch=False, motion="no-preference", forced="none", scale=1):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        device_scale_factor=scale,
        reduced_motion=motion,
        forced_colors=forced,
        has_touch=touch,
        is_mobile=touch,
    )
    return context, context.new_page()


def _eventually(page, check, timeout=5.0):
    import time

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if check():
            return True
        page.wait_for_timeout(50)
    return bool(check())


BOX = "(sel) => { const b = document.querySelector(sel).getBoundingClientRect(); return {x: b.x, y: b.y, w: b.width, h: b.height, right: b.right, bottom: b.bottom}; }"


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("size", [(1440, 900), (390, 844), (360, 640)])
def test_typed_text_is_16_px_and_the_controls_are_52(browser, live_server, seeded, lang, size):
    """L1, L2: 16 px in every field at every width (under 16 px a phone's browser enlarges the page on focus); the
    fields and the primary at the public control's height."""
    width, height = size
    context, page = _page(browser, width, height, touch=width < 600)
    try:
        for path in ("login", "password/reset"):
            page.goto(f"{live_server.url}/{lang}/compte/{path}/", wait_until="networkidle")
            fields = page.evaluate(
                """() => [...document.querySelectorAll('.varco .form-field :is(input:not([type=checkbox]), select, textarea)')].map((el) => {
                     const cs = getComputedStyle(el); return {id: el.id, size: cs.fontSize, h: el.getBoundingClientRect().height,
                             written: el.hasAttribute('placeholder'), placeholder: getComputedStyle(el, '::placeholder').color}; })"""
            )
            assert fields, path
            for field in fields:
                assert field["size"] == "16px", (lang, width, field)
                assert field["h"] == 52, (lang, width, field)
                # no placeholder at all: the label is above the field (the sign-in's form, and the reset's since the
                # review's m4 — accounts.forms.ResetPasswordForm)
                assert not field["written"], f"{path}: a placeholder reads the label a second time: {field}"
            submit = page.evaluate(BOX, SUBMIT)
            sheet = page.evaluate(BOX, ".varco__sheet")
            assert submit["h"] == 52 and abs(submit["w"] - sheet["w"]) < 0.5, "one primary, the column's width"
            assert page.evaluate(f"getComputedStyle(document.querySelector('{SUBMIT}')).fontSize") == "16px"
            assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar", "it", "en"])
def test_the_action_is_in_the_first_viewport_of_a_small_phone(browser, live_server, seeded, legal_published, lang):
    """L5: 360 × 640, the four languages (the invitation is three lines in French, two elsewhere). The sign-up is open
    (the legal pages published): the invitation is drawn only then since W4-D part 2 (F-4), and it is the tallest case."""
    context, page = _page(browser, 360, 640, touch=True)
    try:
        page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
        page.evaluate("async () => { await document.fonts.ready }")
        submit = page.evaluate(BOX, SUBMIT)
        assert submit["bottom"] <= 640, f"{lang}: the action ends at {submit['bottom']:.0f} px"
        assert page.evaluate("scrollY") == 0
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width", [320, 360, 430])
def test_nothing_overflows_and_a_shown_password_has_its_room(browser, live_server, seeded, lang, width):
    """L2, L11: from 320 to 430 px nothing overflows; the password's plate keeps room for 20 characters at 360 px and
    16 at 320 — the control beside it is a glyph, not a sentence — and what is typed is never set under the control."""
    context, page = _page(browser, width, 760, touch=True)
    try:
        page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
        page.evaluate("async () => { await document.fonts.ready }")
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
        room = page.evaluate(
            """(n) => { const input = document.getElementById('id_password'); const toggle = document.querySelector('[data-password-toggle]');
                 const cs = getComputedStyle(input), i = input.getBoundingClientRect(), t = toggle.getBoundingClientRect();
                 const text = [i.left + parseFloat(cs.borderLeftWidth) + parseFloat(cs.paddingLeft), i.right - parseFloat(cs.borderRightWidth) - parseFloat(cs.paddingRight)];
                 const ctx = document.createElement('canvas').getContext('2d'); ctx.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
                 return {text, toggle: [t.left, t.right, t.width, t.height], sample: ctx.measureText('Abcdefghij0123456789'.slice(0, n)).width, display: getComputedStyle(toggle).display}; }""",
            16 if width == 320 else 20,
        )
        (text_left, text_right), (toggle_left, toggle_right, toggle_w, toggle_h) = room["text"], room["toggle"]
        assert room["display"] != "none" and toggle_w >= 44 and toggle_h >= 44, f"the control is a 44 px target: {room['toggle']}"
        assert text_right <= toggle_left + 0.5 or text_left >= toggle_right - 0.5, "what is typed is never under the control"
        assert text_right - text_left >= room["sample"], f"{width} px: {text_right - text_left:.0f} px for a sample of {room['sample']:.0f} px"
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_title_stands_at_one_height_and_the_column_is_not_a_card(browser, live_server, seeded):
    """The form hangs from the top of its panel: the title is at the same height on a long page and on a short one, and
    the column carries no surface of its own."""
    context, page = _page(browser)
    try:
        tops = {}
        for name in ("login", "reset", "reset-done", "inactive"):
            page.goto(live_server.url + PAGES[name][0].format(lang="fr"), wait_until="networkidle")
            page.evaluate("async () => { await document.fonts.ready }")
            tops[name] = round(page.evaluate(BOX, ".varco .account-page__title")["y"], 1)
            look = page.evaluate(
                """() => { const cs = getComputedStyle(document.querySelector('.varco__sheet'));
                     return [cs.backgroundColor, cs.borderTopWidth, cs.boxShadow, cs.borderRadius, cs.paddingTop]; }"""
            )
            assert look == ["rgba(0, 0, 0, 0)", "0px", "none", "0px", "0px"], (name, look)
            sheet, focus = page.evaluate(BOX, ".varco__sheet"), page.evaluate(BOX, ".varco__focus")
            assert sheet["w"] == 400 and abs((sheet["x"] - focus["x"]) - (focus["right"] - sheet["right"])) < 1, "25rem, centred in its panel"
        assert len(set(tops.values())) == 1, f"the title moved with the page's length: {tops}"
        # level with the top of the arch beside it, within one line of the title
        arch = page.evaluate(BOX, "#varco-door")["y"]
        assert abs(tops["login"] - arch) <= 44, (tops["login"], arch)
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_from_the_keyboard_the_address_is_followed_by_the_password(browser, live_server, seeded):
    """L6, and the order inside the form: the address, the password, its show / hide control, the reset link — which
    stands in the label's row, above the field — and the action. Every stop shows the one ring."""
    context, page = _page(browser)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        page.wait_for_timeout(2800)  # the arrival has been said
        page.focus("body")
        stops = []
        for _ in range(80):
            page.keyboard.press("Tab")
            stop = page.evaluate(
                """() => { const el = document.activeElement; const cs = getComputedStyle(el);
                     return {inForm: Boolean(el.closest('.varco .form')), id: el.id, toggle: el.hasAttribute('data-password-toggle'), href: el.getAttribute('href'),
                             submit: el.matches('button[type=submit]'), ring: [cs.outlineStyle, cs.outlineWidth], halo: cs.boxShadow}; }"""
            )
            if stop["inForm"]:
                stops.append(stop)
            if stop["submit"]:
                break
        kinds = ["login" if s["id"] == "id_login" else "password" if s["id"] == "id_password" else "toggle" if s["toggle"] else "reset" if s["href"] else "submit" for s in stops]
        assert kinds == ["login", "password", "toggle", "reset", "submit"], kinds
        assert stops[3]["href"] == "/fr/compte/password/reset/"
        for stop, kind in zip(stops, kinds):
            assert stop["ring"] == ["solid", "2px"], f"{kind}: no ring from the keyboard ({stop['ring']})"
        assert stops[0]["halo"] != "none" and stops[1]["halo"] != "none", "a text field adds the halo"
        # in the label's row: the link stands above the password's plate, at the row's end
        link, field, label = page.evaluate(BOX, ".form-field__aside a"), page.evaluate(BOX, "#id_password"), page.evaluate(BOX, "label[for=id_password]")
        assert link["bottom"] <= field["y"] and abs(link["right"] - field["right"]) < 1 and abs((link["y"] + link["h"] / 2) - (label["y"] + label["h"] / 2)) <= 2, (link, field, label)
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("touch", [False, True])
def test_every_target_of_the_form_has_its_size(browser, live_server, seeded, phase3_open, legal_published, touch):
    """L2 / SP-8: 24 px is the floor; 44 px for the form's controls, and for every target under a finger — where the
    reset link's target grows upward, into the air between the two fields, and never lies over the password. The
    small links around the form (the check's A2): the help line's address is 44 px at every pointer (plan §1.13), the
    assurance's link 24 px and 44 under a finger, the invitation's link 44 under a finger — each a band around its
    line, the line itself unmoved. The sign-up is open (the legal pages published): the invitation is drawn only then since
    W4-D part 2 (F-4, tests/frontend/test_login_invitation_w4_d.py)."""
    context, page = _page(browser, 390 if touch else 1440, 844 if touch else 900, touch=touch)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        hits = page.evaluate(
            """() => Object.fromEntries([['help', '.varco__help a', '::before'], ['assurance', '.varco__assurance-more a', '::after'], ['invitation', '.varco .account-page__text a', '::before']].map(([name, sel, part]) => {
                 const el = document.querySelector(sel); const b = el.getBoundingClientRect(); const hit = getComputedStyle(el, part);
                 const top = hit.content === 'none' ? b.top : Math.min(b.top, b.top + parseFloat(hit.top)), bottom = hit.content === 'none' ? b.bottom : Math.max(b.bottom, b.bottom - parseFloat(hit.bottom));
                 return [name, {height: bottom - top, line: b.height, width: b.width}]; }))"""
        )
        assert hits["help"]["height"] >= 44 - 0.5, f"the help link, with a 44 px target (plan §1.13): {hits['help']}"
        assert hits["assurance"]["height"] >= (44 if touch else 24) - 0.5, hits["assurance"]
        assert hits["invitation"]["height"] >= (44 if touch else 0) - 0.5, hits["invitation"]
        sizes = page.evaluate(
            """() => { const r = (el) => el.getBoundingClientRect(); const link = document.querySelector('.form-field__aside a'); const hit = getComputedStyle(link, '::after');
                 const l = r(link); const top = l.top + parseFloat(hit.top), bottom = l.bottom - parseFloat(hit.bottom);
                 return {coarse: matchMedia('(pointer: coarse)').matches, login: r(document.getElementById('id_login')).height, password: r(document.getElementById('id_password')).height,
                         toggle: [r(document.querySelector('[data-password-toggle]')).width, r(document.querySelector('[data-password-toggle]')).height],
                         submit: r(document.querySelector('.varco .form__actions .btn--primary')).height, link: [top, bottom], field: r(document.getElementById('id_password')).top,
                         above: r(document.getElementById('id_login')).bottom, signup: r(document.querySelector('.varco .account-page__text a')).height}; }"""
        )
        assert sizes["coarse"] is touch
        assert sizes["login"] >= 44 and sizes["password"] >= 44 and sizes["submit"] >= 44 and min(sizes["toggle"]) >= 44, sizes
        top, bottom = sizes["link"]
        assert bottom - top >= (44 if touch else 24) - 0.5, f"the reset link's target is {bottom - top:.0f} px"
        assert bottom <= sizes["field"] + 0.5 and top >= sizes["above"] - 0.5, f"it lies over a field: {sizes}"
    finally:
        context.close()


TOGGLE = """() => { const t = document.querySelector('[data-password-toggle]'); const i = document.getElementById('id_password');
  const shown = (sel) => { const el = t.querySelector(sel); return el ? getComputedStyle(el).display !== 'none' : null; };
  return {type: i.type, pressed: t.getAttribute('aria-pressed'), name: t.getAttribute('aria-label') || t.textContent.trim(), focus: document.activeElement === t ? 'control' : document.activeElement === i ? 'field' : 'elsewhere',
          caret: [i.selectionStart, i.selectionEnd], value: i.value, eye: shown('.form-field__toggle-show'), eyeOff: shown('.form-field__toggle-hide'), words: [...t.childNodes].filter((n) => n.nodeType === 3 || (n.nodeType === 1 && !n.matches('.visually-hidden, svg'))).map((n) => n.textContent.trim()).join('')}; }"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_the_show_hide_control_is_one_name_one_state_and_keeps_the_caret(browser, live_server, seeded):
    """Plan §1.13: one channel — `aria-pressed`, under a name that does not change (the live string) — the glyph swaps
    at once, and the caret is kept: a pointer's press hands the focus back to the field where the person was typing;
    pressed from the keyboard, the control keeps the focus and can be pressed again."""
    context, page = _page(browser)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        rest = page.evaluate(TOGGLE)
        assert rest["type"] == "password" and rest["pressed"] == "false" and rest["name"] == "Afficher le mot de passe", rest
        assert rest["eye"] is True and rest["eyeOff"] is False and rest["words"] == "", "a glyph, not a sentence"
        page.click("#id_password")
        page.keyboard.type("abcdef")
        for _ in range(3):
            page.keyboard.press("ArrowLeft")
        box = page.locator("[data-password-toggle]").bounding_box()
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        shown = page.evaluate(TOGGLE)
        assert shown["type"] == "text" and shown["pressed"] == "true", shown
        assert shown["name"] == rest["name"], "the name does not change: the state is `aria-pressed` alone"
        assert shown["eye"] is False and shown["eyeOff"] is True, "the glyph swaps"
        assert shown["focus"] == "field" and shown["caret"] == [3, 3], f"the caret is kept: {shown}"
        page.keyboard.type("X")
        assert page.evaluate(TOGGLE)["value"] == "abcXdef", "the person goes on typing where they were"
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        hidden = page.evaluate(TOGGLE)
        assert hidden["type"] == "password" and hidden["pressed"] == "false" and hidden["caret"] == [4, 4] and hidden["focus"] == "field", hidden
        # from the keyboard: the control keeps the focus, and a second press hides the password again
        page.keyboard.press("Tab")
        assert page.evaluate(TOGGLE)["focus"] == "control"
        page.keyboard.press("Space")
        pressed = page.evaluate(TOGGLE)
        assert pressed["type"] == "text" and pressed["pressed"] == "true" and pressed["focus"] == "control", pressed
        page.keyboard.press("Enter")
        again = page.evaluate(TOGGLE)
        assert again["type"] == "password" and again["pressed"] == "false" and again["focus"] == "control" and again["value"] == "abcXdef", again
        assert page.url.endswith("/fr/compte/login/") and page.locator("#form-errors").count() == 0, "the control never submits the form"
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_without_script_the_control_is_not_drawn_and_the_form_is_whole(browser, live_server, seeded):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    try:
        page = context.new_page()
        page.goto(live_server.url + "/fr/compte/login/", wait_until="load")
        assert page.locator("[data-password-toggle]").evaluate("(el) => getComputedStyle(el).display") == "none"
        assert page.locator(SUBMIT).is_visible() and page.locator("#id_login").is_visible() and page.locator(".form-field__aside a").is_visible()
    finally:
        context.close()


PLACES = """() => { const r = (sel) => { const el = document.querySelector(sel); if (!el) return null; const b = el.getBoundingClientRect(); return [Math.round(b.top * 10) / 10, Math.round(b.height * 10) / 10]; };
  return {key: r('.varco__eyebrow-key'), title: r('.varco .account-page__title'), address: r('#id_login'), label: r('label[for=id_password]'), password: r('#id_password'), action: r('.varco .form__actions .btn--primary')}; }"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("size", [(1440, 900), (390, 844)])
def test_no_part_of_the_column_waits_for_a_later_one_to_know_its_place(browser, live_server, seeded, lang, size):
    """A browser that paints before the whole column is parsed draws it without what has not arrived yet, and a part
    that is drawn must not move when the next one comes. Read by taking the later parts away, last first — the
    password's link (written after its control), the show / hide control, the eyebrow's words (written after its
    key) — and asking the others where they stand. Held against two defects: in Arabic the link's taller line made
    the label's row 2 px taller when it arrived; the eyebrow's row was its key's height until its words came."""
    context, page = _page(browser, *size)
    try:
        page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
        whole = page.evaluate(PLACES)
        assert all(whole.values()), whole
        for later in (".form-field__aside", "[data-password-toggle]", ".varco__eyebrow span"):
            page.evaluate("(sel) => document.querySelector(sel).remove()", later)
            assert page.evaluate(PLACES) == whole, f"{lang} {size}: the column moves when {later} arrives"
    finally:
        context.close()


KEY = """(sel) => { const b = document.querySelector(sel); const cs = getComputedStyle(b), k = getComputedStyle(b, '::after');
  const range = document.createRange(); range.selectNodeContents(b); const label = range.getBoundingClientRect(); const box = b.getBoundingClientRect();
  return {shadow: cs.boxShadow, image: cs.backgroundImage, fill: cs.backgroundColor, ink: cs.color, busy: b.getAttribute('aria-busy'), classes: b.className,
          key: {content: k.content, mask: k.maskImage || k.webkitMaskImage, w: parseFloat(k.width), h: parseFloat(k.height), end: parseFloat(k.insetInlineEnd), ground: k.backgroundColor,
                opacity: k.opacity, animation: k.animationName, iterations: k.animationIterationCount},
          label: [Math.round(label.left * 10) / 10, Math.round(label.width * 10) / 10], box: [box.left, box.width, box.height], focused: document.activeElement === b}; }"""


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_primary_is_flat_and_the_key_it_holds_is_the_key_that_turns(browser, live_server, seeded, lang):
    """L14, L8: no shadow, no image; at rest the key in the label's ink, in the middle of the end pad; on submit the
    same pseudo-element turns once and dims — the same box, to the pixel — and the label has not moved."""
    context, page = _page(browser)
    posts = []

    def answer(route):
        if route.request.method != "POST":
            return route.continue_()
        posts.append(route.request.url)
        return route.fulfill(status=204, body="")

    try:
        page.route("**/*", answer)
        page.goto(f"{live_server.url}/{lang}/compte/login/", wait_until="networkidle")
        page.evaluate("async () => { await document.fonts.ready }")
        rest = page.evaluate(KEY, SUBMIT)
        assert rest["shadow"] == "none" and rest["image"] == "none", "flat: no shadow, no inset, no gradient"
        key = rest["key"]
        assert key["content"] == '""' and "data:image/svg+xml" in key["mask"], "the primary holds the key at rest"
        assert key["h"] == 18 and 7 < key["w"] < 8.5 and key["ground"] == rest["ink"] and key["opacity"] == "1", key
        assert abs(key["end"] - (52 - key["w"]) / 2) < 0.6, f"the middle of the 52 px end pad: {key}"
        assert key["animation"] == "none"
        box_left, box_width, _ = rest["box"]
        label_left, label_width = rest["label"]
        assert abs((label_left + label_width / 2) - (box_left + box_width / 2)) < 1, "the label is centred on the plate"

        page.fill("#id_login", "prenom.nom@example.com")
        page.fill("#id_password", "not-a-password")
        page.locator(SUBMIT).click(no_wait_after=True)  # the answer is not a page: no navigation will end
        assert _eventually(page, lambda: page.evaluate(KEY, SUBMIT)["busy"] == "true")
        busy = page.evaluate(KEY, SUBMIT)
        assert "is-busy" in busy["classes"] and busy["focused"], "the busy face, and the focus kept"
        assert busy["key"]["animation"] == "sig-turn" and busy["key"]["iterations"] == "1" and busy["key"]["opacity"] == "0.8", busy["key"]
        for name in ("w", "h", "end", "mask", "ground"):
            assert busy["key"][name] == key[name], f"the busy key is not the key at rest: {name} {key[name]} → {busy['key'][name]}"
        assert busy["label"] == rest["label"] and busy["box"] == rest["box"], "nothing is laid out again: the label has not moved"
        page.wait_for_timeout(400)  # the press has been released on the slab's own transition
        held = page.evaluate(KEY, SUBMIT)
        assert held["shadow"] == "none" and held["image"] == "none" and held["fill"] == rest["fill"], "it waits on its own surface"
        assert held["label"] == rest["label"] and held["key"]["end"] == key["end"], "…and still nothing has moved"
        page.locator(SUBMIT).click(force=True, no_wait_after=True)
        page.wait_for_timeout(300)
        assert len(posts) == 1, "a second press is refused while the first waits"

        # the key at rest is the sign-in's: another entrance form's primary holds none, and its busy key is the loader's
        page.goto(f"{live_server.url}/{lang}/compte/password/reset/", wait_until="networkidle")
        other = page.evaluate(KEY, SUBMIT)
        assert other["key"]["content"] == "none" and other["shadow"] == "none" and other["image"] == "none", other["key"]
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_refused_sign_in_is_said_once_and_no_field_is_blamed(browser, live_server, seeded):
    """L4: the summary takes the focus at load, both fields are described by it, neither carries the error's edge, and
    the summary's list of fields — empty: the refusal names none — takes no room; a second refusal says it again."""
    context, page = _page(browser)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        rest_edge = page.evaluate("getComputedStyle(document.getElementById('id_login')).borderTopColor")
        for attempt in range(2):
            page.fill("#id_login", "personne.inconnue@example.com")
            page.fill("#id_password", f"not-a-password-{attempt}")
            with page.expect_navigation(wait_until="load"):
                page.locator("#id_password").press("Enter")
            assert _eventually(page, lambda: page.evaluate("document.activeElement.id") == "form-errors"), "the summary takes the focus"
            state = page.evaluate(
                """() => { const s = document.getElementById('form-errors'); const list = s.querySelector('.form-errors__list');
                     const f = (id) => { const el = document.getElementById(id); const cs = getComputedStyle(el); return {described: el.getAttribute('aria-describedby'), invalid: el.getAttribute('aria-invalid'), edge: cs.borderTopColor, shadow: cs.boxShadow, value: el.value}; };
                     const last = s.querySelector('.notice__body > p:last-of-type');
                     return {title: document.title, role: s.getAttribute('role'), list: list ? getComputedStyle(list).display : null, items: list ? list.children.length : 0,
                             gap: s.getBoundingClientRect().bottom - last.getBoundingClientRect().bottom, login: f('id_login'), password: f('id_password'),
                             ring: getComputedStyle(s).outlineStyle}; }"""
            )
            assert state["title"].startswith("Erreur — Connexion"), state["title"]
            assert state["role"] == "alert" and state["ring"] == "solid"
            assert state["items"] == 0 and state["list"] == "none", "a list of nothing takes no room and is not announced"
            assert state["gap"] <= 17, f"the summary ends {state['gap']:.0f} px under its sentence"
            assert state["login"]["described"] == "form-errors" and state["password"]["described"].split()[0] == "form-errors"
            for field in (state["login"], state["password"]):
                assert field["invalid"] is None and field["edge"] == rest_edge and field["shadow"] == "none", "no field is blamed"
            assert state["login"]["value"] == "personne.inconnue@example.com" and state["password"]["value"] == ""
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_field_s_own_error_is_its_edge_its_mark_and_its_words(browser, live_server, seeded):
    """Never by colour alone: the edge doubles, the message carries a drawn mark, and the words say it."""
    context, page = _page(browser)
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        rest = page.evaluate("(() => { const cs = getComputedStyle(document.getElementById('id_login')); return [cs.borderTopColor, cs.boxShadow]; })()")
        with page.expect_navigation(wait_until="load"):
            page.locator(SUBMIT).click()
        state = page.evaluate(
            """() => ['id_login', 'id_password'].map((id) => { const el = document.getElementById(id); const cs = getComputedStyle(el);
                 const message = document.getElementById(id + '_error'); const item = message.querySelector('li'); const mark = getComputedStyle(item, '::before');
                 return {invalid: el.getAttribute('aria-invalid'), described: el.getAttribute('aria-describedby'), edge: cs.borderTopColor, shadow: cs.boxShadow,
                         words: item.textContent.trim(), mark: [mark.content, mark.width, mark.borderTopStyle], under: message.getBoundingClientRect().top >= el.getBoundingClientRect().bottom}; })"""
        )
        for field in state:
            assert field["invalid"] == "true" and field["described"].endswith("_error"), field
            assert field["edge"] != rest[0] and field["shadow"] != rest[1] and "inset" in field["shadow"], "the edge doubles"
            assert field["words"] and field["mark"][0] == '""' and field["mark"][1] == "16px" and field["mark"][2] == "solid", field
            assert field["under"], "the message stands under its field"
        assert page.evaluate("document.querySelectorAll('#form-errors .form-errors__list a').length") == 2
        # the reset link keeps its place in the label's row, above the field in error
        link, field = page.evaluate(BOX, ".form-field__aside a"), page.evaluate(BOX, "#id_password")
        assert link["bottom"] <= field["y"]
    finally:
        context.close()


@pytest.fixture
def unverified_session(user_factory):
    """A sign-in of an account whose address is not verified, through allauth's real view: it sends the verification
    again and says so in a session message. Returns the session's key, to hand to a browser."""
    user = user_factory("message-varco@example.test", password=PASSWORD)
    EmailAddress.objects.create(user=user, email=user.email, verified=False, primary=True)

    def sign_in(lang="fr"):
        client = Client()
        response = client.post(f"/{lang}/compte/login/", {"login": user.email, "password": PASSWORD})
        assert response.status_code == 302 and response["Location"].endswith("/compte/confirm-email/"), response
        return client.cookies[settings.SESSION_COOKIE_NAME].value

    return sign_in


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("size", [(1440, 900), (390, 844)])
def test_a_session_message_stands_in_the_form_s_column(browser, live_server, seeded, unverified_session, size):
    """templates/base.html writes the message before the entrance, as a band across the page: the stage then began under
    it. It stands in the form's column — above the eyebrow, hung where the form hangs — and the stage still meets the
    letterhead; below 64rem: the band, the message, the form."""
    width, height = size
    context, page = _page(browser, width, height, touch=width < 600)
    try:
        context.add_cookies([{"name": settings.SESSION_COOKIE_NAME, "value": unverified_session(), "url": live_server.url}])
        page.goto(live_server.url + "/fr/compte/confirm-email/", wait_until="networkidle")
        boxes = {name: page.evaluate(BOX, sel) for name, sel in (("message", "main > .messages"), ("stage", "[data-varco-stage]"), ("focus", ".varco__focus"), ("sheet", ".varco__sheet"), ("eyebrow", ".varco__eyebrow"), ("main", "main"))}
        assert "message-varco@example.test" in page.inner_text("main > .messages")
        message, stage, sheet = boxes["message"], boxes["stage"], boxes["sheet"]
        assert abs(message["x"] - sheet["x"]) < 1 and abs(message["w"] - sheet["w"]) < 1, "the column's own measure"
        assert message["bottom"] <= boxes["eyebrow"]["y"], "above the eyebrow"
        assert abs(stage["y"] - boxes["main"]["y"]) < 1, "the stage meets the letterhead: no band of the page above it"
        if width >= 1024:
            assert stage["right"] <= message["x"] and abs(stage["bottom"] - boxes["main"]["bottom"]) < 1, "the stage keeps the reading edge for the page's height"
            assert stage["h"] >= height - 97, "one screen of the niche, as on a page without a message"
        else:
            assert stage["bottom"] <= message["y"], "the band, the message, the form"
        assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
        # the message is said once: the next page of the entrance has none, and its title is back at its height
        page.goto(live_server.url + "/fr/compte/confirm-email/", wait_until="networkidle")
        assert page.locator("main > .messages").count() == 0
    finally:
        context.close()


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_under_forced_colours_the_form_keeps_its_signs(browser, live_server, seeded):
    context, page = _page(browser, forced="active")
    try:
        page.goto(live_server.url + "/fr/compte/login/", wait_until="networkidle")
        signs = page.evaluate(
            """() => { const b = document.querySelector('.varco .form__actions .btn--primary'); const k = getComputedStyle(b, '::after');
                 const t = document.querySelector('[data-password-toggle]'); const i = document.getElementById('id_login');
                 return {key: [k.content, k.forcedColorAdjust, k.backgroundColor], button: getComputedStyle(b).borderTopStyle, toggle: getComputedStyle(t).borderTopStyle,
                         field: getComputedStyle(i).borderTopStyle, ink: getComputedStyle(b).color}; }"""
        )
        assert signs["key"][0] == '""' and signs["key"][1] == "none" and signs["key"][2] == signs["ink"], f"the key in the button's forced ink: {signs}"
        assert signs["button"] == "solid" and signs["toggle"] == "solid" and signs["field"] == "solid", "edges carry the form"
    finally:
        context.close()


def _reset_key_path(user, lang: str) -> str:
    """The link allauth e-mails for a password reset (its own token generator, its own encoding of the user)."""
    from allauth.account.forms import default_token_generator
    from allauth.account.utils import user_pk_to_url_str

    return f"/{lang}/compte/password/reset/key/{user_pk_to_url_str(user)}-{default_token_generator.make_token(user)}/"


SECRETS = """() => [...document.querySelectorAll('[data-password-toggle]')].map((t) => { const i = document.getElementById(t.getAttribute('aria-controls'));
  return {id: i.id, type: i.type, spellcheck: i.spellcheck, autocapitalize: i.getAttribute('autocapitalize'), autocorrect: i.getAttribute('autocorrect'),
          placeholder: i.hasAttribute('placeholder')}; })"""


def test_the_show_hide_control_tells_every_field_it_can_show_not_to_spell_or_correct():
    """Review M2, on the source: the control's section of shell.js tells the field it shows, once, when it is wired."""
    section = _read(SHELL).split("/* 3.", 1)[1].split("/* 4.", 1)[0]
    code = re.sub(r"/\*.*?\*/", "", section, flags=re.S)
    wired = code.split('button.addEventListener("click"', 1)[0]
    for line in ("input.spellcheck = false;", 'input.setAttribute("autocapitalize", "none");', 'input.setAttribute("autocorrect", "off");'):
        assert line in wired, f"{line} — before the first press, for every revealable password"


@pytest.mark.browser
@pytest.mark.django_db(transaction=True)
def test_a_password_the_control_can_show_is_never_spelled_nor_corrected(browser, live_server, seeded, legal_published, user_factory):
    """Review M2: shown, a password is a text field — spell-checked by a vendor's service where the browser has one,
    capitalised and corrected by a phone's keyboard. Every password the system's control can show says no to the
    three, before and after the press: the sign-in's, the sign-up's two, the new password's two. The new password's
    fields write no placeholder (m4), and the link under its action is a 44 px target under a finger with its words at
    the column's start — allauth's Arabic «يلغي» is 28 px (the check's A2)."""
    user = user_factory("reset-varco@example.test", password=PASSWORD)
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    for path, count, touch in (("/fr/compte/login/", 1, False), ("/fr/compte/signup/", 2, False), (_reset_key_path(user, "ar"), 2, True)):
        context, page = _page(browser, 390 if touch else 1440, 844 if touch else 900, touch=touch)
        try:
            page.goto(live_server.url + path, wait_until="networkidle")
            fields = page.evaluate(SECRETS)
            assert len(fields) == count, (path, fields)
            for field in fields:
                assert field["spellcheck"] is False and field["autocapitalize"] == "none" and field["autocorrect"] == "off", (path, field)
            page.locator("[data-password-toggle]").first.click()
            shown = page.evaluate(SECRETS)[0]
            assert shown["type"] == "text" and shown["spellcheck"] is False and shown["autocapitalize"] == "none", (path, shown)
            if "/key/" in page.url:
                assert all(not field["placeholder"] for field in fields), f"the new password's labels are above its fields: {fields}"
                cancel = page.evaluate(
                    """() => { const b = document.querySelector('.varco .form__actions .btn--link'); const r = b.getBoundingClientRect();
                         const range = document.createRange(); range.selectNodeContents(b); const words = range.getBoundingClientRect();
                         return {w: r.width, h: r.height, right: r.right, wordsRight: words.right, dir: getComputedStyle(b).direction}; }"""
                )
                assert cancel["w"] >= 44 - 0.5 and cancel["h"] >= 44 - 0.5, f"«Annuler» under a finger: {cancel}"
                assert cancel["dir"] == "rtl" and abs(cancel["right"] - cancel["wordsRight"]) < 1, f"its words at the column's start: {cancel}"
        finally:
            context.close()
