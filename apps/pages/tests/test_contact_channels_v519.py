"""
V5.19 — the owner-confirmed public telephone channels (lane v519-k; directive V5_19 §15).

The Numero Verde 800 642 015 (tel:800642015) and WhatsApp, stored once in the site's settings (core.models.SiteSettings,
core.contact) and rendered on the contact page, the footer and the phone's sheet, in four languages. Arabic keeps the
digit groups in their order: every number is isolated left to right (<bdi dir="ltr">). No template writes a number; a
blank setting withdraws its channel.

V5.20 (option B, applied while the owner's answer is awaited): the owner-confirmed WhatsApp number is configured outside
the repository (V5.19/V5.20) — the back office holds it, the environment's ILE_WHATSAPP_NUMBER gives its default — for
it is a personal identifier no tracked file may hold (tests/security/test_confidential_material.py, the private sentinel
table). These tests draw the channel with Ofcom's fictional +44 7700 900123 (tests/conftest.py, ``whatsapp_channel``) to
prove the grouping, the wa.me rule, the accessible names and the Arabic order; with nothing configured the channel is
absent everywhere; and the owner-confirmed number itself is checked wherever it is configured (the last test: SKIPPED,
with its reason, only where ILE_WHATSAPP_NUMBER is unset).

Test-update note (V5.20 rule): the expectations that spelt the owner's number conflict with that rule; the behaviour now
read — the number from the environment and the back office — is implemented on purpose (core.contact.
default_whatsapp_number, migration core 0003); every invariant is kept, on the fictional number, and the
absent-everywhere, the configured-number and the migration checks are added.
"""

from __future__ import annotations

import html as html_lib
import os
import re
from importlib import import_module
from pathlib import Path

import pytest
from django.apps import apps
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.utils import translation

from core import contact
from core.models import SiteSettings
from pages.tests.conftest import LANGS
from tests.conftest import FICTIONAL_WHATSAPP_NUMBER, whatsapp_link_set_aside

ROOT = Path(__file__).resolve().parents[3]

FREEPHONE_LABEL = "800 642 015"
#: the fictional channel (tests/conftest.py) as core.contact draws it: the digits; the grouping (a country other than
#: Italy: its code, then groups of three); the wa.me link (the digits alone); the telephone link
WHATSAPP_DIGITS = "+447700900123"
WHATSAPP_LABEL = "+44 770 090 0123"
WHATSAPP_URL = "https://wa.me/447700900123"
WHATSAPP_TEL = "tel:+447700900123"

#: names the owner-confirmed WhatsApp number (V5.20, option B): the server's environment file, the local untracked .env
#: or the shell — never a tracked file
WHATSAPP_VARIABLE = "ILE_WHATSAPP_NUMBER"

#: the accessible names, as each language says them (directive §8); ``{number}`` is the WhatsApp channel's grouping
NAMES = {
    "fr": ("Appeler le numéro vert 800 642 015", "Contacter Italy Legal Entry sur WhatsApp au {number}"),
    "it": ("Chiamare il numero verde 800 642 015", "Contattare Italy Legal Entry su WhatsApp al {number}"),
    "en": ("Call the freephone number 800 642 015", "Contact Italy Legal Entry on WhatsApp at {number}"),
    "ar": (
        "الاتصال بالرقم المجاني 800 642 015",
        "التواصل مع Italy Legal Entry عبر WhatsApp على الرقم {number}",
    ),
}

#: the placeholders that once stood for a site number (V5.19 §4) — never on a public page
OBSOLETE = ("+39 0000 000000", "0000000000", "tel:0000", "wa.me/0")

#: public pages every language serves on the seeded data, whatever the gates say
ALWAYS_SERVED = ("", "contact/", "le-projet/", "agami/")


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


def _footer(html: str) -> str:
    return html.split('<footer class="site-footer', 1)[1].split("</footer>", 1)[0]


def _sheet(html: str) -> str:
    return html.split('id="nav-sheet"', 1)[1].split("</dialog>", 1)[0]


def _links(fragment: str) -> dict[str, str]:
    """href → accessible name (aria-label) of every link of a fragment."""
    return {
        html_lib.unescape(href): html_lib.unescape(label)
        for href, label in re.findall(r'<a [^>]*href="([^"]+)"[^>]*aria-label="([^"]+)"', fragment)
    }


def _names(lang: str, whatsapp_label: str = WHATSAPP_LABEL) -> tuple[str, str]:
    freephone_name, whatsapp_name = NAMES[lang]
    return freephone_name, whatsapp_name.format(number=whatsapp_label)


def _desk_rows(main: str) -> list[str]:
    """RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D,
    «lo sportello»): the contact page's channels are the desk's rows — the address's, then each voice the settings
    hold."""
    desk = main.split('<ul class="sportello__lista"', 1)[1].split("</ul>", 1)[0]
    return re.findall(r'<li class="sportello-canale sportello-canale--([a-z]+)">', desk)


@pytest.fixture
def no_whatsapp_channel(db, settings):
    """Nothing configured: ILE_WHATSAPP_NUMBER blank (the settings' value) and the back office's number blank."""
    settings.ILE = {**settings.ILE, "WHATSAPP_NUMBER": ""}
    row = SiteSettings.load()
    row.whatsapp_number = ""
    row.save()
    return row


# ---- the canonical values ------------------------------------------------------------------------------------------
def test_the_canonical_channels(whatsapp_channel):
    channels = contact.public_channels(SiteSettings.load())
    freephone, whatsapp = channels["freephone"], channels["whatsapp"]
    assert (freephone.digits, freephone.label, freephone.tel_url, freephone.url) == (
        "800642015",
        FREEPHONE_LABEL,
        "tel:800642015",
        "tel:800642015",
    )
    assert (whatsapp.digits, whatsapp.label, whatsapp.tel_url, whatsapp.url) == (
        WHATSAPP_DIGITS,
        WHATSAPP_LABEL,
        WHATSAPP_TEL,
        WHATSAPP_URL,
    )
    assert whatsapp == whatsapp_channel
    # the wa.me link: the digits alone — no space, plus, bracket or punctuation (§7)
    assert re.fullmatch(r"https://wa\.me/\d+", whatsapp.url)
    # the settings' value (a new row's default, the fallback before migrations) draws the same channels
    assert contact.public_channels() == channels


def test_an_italian_mobile_reads_plus_39_then_three_three_four():
    """The owner's grouping of an Italian mobile (V5.19: «+39», then 3-3-4), on digits no numbering plan assigns."""
    assert contact.international_label("+390000000000") == "+39 000 000 0000"
    assert contact.whatsapp("+39 000 000 0000").url == "https://wa.me/390000000000"


@pytest.mark.parametrize("typed", ["800 642 015", "800-642-015", "800.642.015", "800642015"])
def test_a_number_typed_with_separators_is_the_same_channel(typed):
    assert contact.freephone(typed) == contact.freephone("800642015")


@pytest.mark.parametrize("typed", ["+44 7700 900123", "+44 7700-900123", "+44.7700.900.123", "+447700900123"])
def test_whatsapp_typed_with_spaces_opens_the_same_link(typed):
    assert contact.whatsapp(typed).url == WHATSAPP_URL


@pytest.mark.parametrize("bad", ["80064", "00447700900123 x", "abc"])
def test_the_back_office_refuses_a_malformed_number(bad):
    with pytest.raises(ValidationError):
        contact.validate_national_number(bad)
    with pytest.raises(ValidationError):
        contact.validate_international_number(bad)


@pytest.mark.parametrize("configured", [FICTIONAL_WHATSAPP_NUMBER, ""], ids=["configured", "blank"])
def test_the_settings_hold_the_configured_numbers(db, settings, configured):
    """
    A new settings row holds the Numero Verde and the environment's WhatsApp number (V5.20: settings.ILE, read from
    ILE_WHATSAPP_NUMBER — the default's only source); blank, the row holds none and the channel is withdrawn.
    """
    settings.ILE = {**settings.ILE, "WHATSAPP_NUMBER": configured}
    SiteSettings.objects.all().delete()
    settings_row = SiteSettings.load()
    assert settings_row.freephone_number == "800642015"
    assert settings_row.whatsapp_number == configured
    assert contact.public_channels(settings_row) == contact.public_channels()
    assert (contact.public_channels(settings_row)["whatsapp"] is None) is (not configured)


def test_no_whatsapp_number_is_written_in_the_settings_or_the_migration():
    """
    V5.20 (option B): the settings read ILE_WHATSAPP_NUMBER with a blank default, and migration core 0003 names the
    default's function — neither writes an international number or a wa.me link (the private sentinel table checks
    the owner's own number in every tracked file, tests/security/test_confidential_material.py).
    """
    read = django_settings.ILE["WHATSAPP_NUMBER"] == os.environ.get(WHATSAPP_VARIABLE, "")
    assert read, "settings.ILE['WHATSAPP_NUMBER'] is not the environment's ILE_WHATSAPP_NUMBER (blank when unset)"
    for relative in ("config/settings/base.py", "apps/core/migrations/0003_public_telephone_channels.py"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert not re.search(r"\+\d[\d ()./-]{7,}\d", text), relative
        assert not re.search(r"wa\.me/\d", text), relative


def test_the_migration_copies_the_environments_number_into_a_blank_row(db, settings):
    """Migration core 0003's data step: the environment's number into a row that holds none — never over the back
    office's."""
    step = import_module("core.migrations.0003_public_telephone_channels").set_the_confirmed_numbers
    settings_row = SiteSettings.load()
    settings_row.whatsapp_number = ""
    settings_row.save()
    settings.ILE = {**settings.ILE, "WHATSAPP_NUMBER": ""}
    step(apps, None)
    settings_row.refresh_from_db()
    assert settings_row.whatsapp_number == ""
    settings.ILE = {**settings.ILE, "WHATSAPP_NUMBER": FICTIONAL_WHATSAPP_NUMBER}
    step(apps, None)
    settings_row.refresh_from_db()
    assert settings_row.whatsapp_number == FICTIONAL_WHATSAPP_NUMBER
    settings_row.whatsapp_number = "+44 7700 900456"  # another of Ofcom's fictional numbers, typed in the back office
    settings_row.save()
    step(apps, None)
    settings_row.refresh_from_db()
    assert settings_row.whatsapp_number == "+44 7700 900456"


def test_no_template_writes_a_number():
    """§3: the numbers live in the settings — a template reads site.channels, never a literal: not the Numero Verde, no
    wa.me link, no international telephone link, no international number in any grouping (V5.20: the WhatsApp number
    is configured outside the repository, so the shapes are general — they cover the owner's number and any other)."""
    shapes = ("800642015", "800 642 015", "wa.me/", "tel:+")
    international = re.compile(r"\+\d[\d\s\u00a0.()/-]{7,}\d")
    offenders = [
        str(path.relative_to(ROOT))
        for path in (ROOT / "templates").rglob("*")
        if path.is_file() and path.suffix in (".html", ".txt")
        for text in (path.read_text(encoding="utf-8"),)
        if any(shape in text for shape in shapes) or international.search(text)
    ]
    assert offenders == []


def test_the_guards_set_aside_the_configured_whatsapp_link_only_as_a_link(whatsapp_channel):
    """tests/conftest.py's helper: the configured channel's wa.me URL as a link, and nothing else — not as a source,
    not another wa.me number; nothing configured, nothing is set aside."""
    page_html = (
        f'<a class="canale__link" href="{WHATSAPP_URL}" aria-label="x">x</a>'
        f'<img src="{WHATSAPP_URL}" alt=""><a href="https://wa.me/440000000000">y</a>'
    )
    checked = whatsapp_link_set_aside(page_html)
    assert re.findall(r'(?:src|href)="(https?://[^"]+)"', checked) == [WHATSAPP_URL, "https://wa.me/440000000000"]
    assert 'href="#whatsapp"' in checked
    settings_row = SiteSettings.load()
    settings_row.whatsapp_number = ""
    settings_row.save()
    assert whatsapp_link_set_aside(page_html) == page_html


# ---- the public surfaces, in four languages --------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_the_contact_page_draws_both_channels(page, seeded, whatsapp_channel, lang):
    response, html = page(f"/{lang}/contact/")
    assert response.status_code == 200
    main = _main(html)
    freephone_name, whatsapp_name = _names(lang)
    links = _links(main)
    assert links["tel:800642015"] == freephone_name
    assert links[WHATSAPP_URL] == whatsapp_name
    # the visible numbers, isolated left to right, the same in every language
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # the desk's links carry the number as the site's phone isolate (the footer's and the sheet's own markup)
    link = (
        '<a class="sportello-canale__link" href="{href}" aria-label="{name}">'
        '<bdi class="phone" dir="ltr">{label}</bdi></a>'
    )
    assert link.format(href="tel:800642015", name=freephone_name, label=FREEPHONE_LABEL) in html_lib.unescape(main)
    assert link.format(href=WHATSAPP_URL, name=whatsapp_name, label=WHATSAPP_LABEL) in html_lib.unescape(main)
    # WhatsApp is drawn as its channel (its glyph and its word), the Numero Verde as a telephone
    assert re.search(r'sportello-canale--voce">.*?#icon-phone"', main, re.S)
    assert re.search(r'sportello-canale--whatsapp">.*?#icon-message-circle".*?>WhatsApp<', main, re.S)
    # one board, never repeated on the page, named for both channels — V5.22 (SECTION_SYSTEM_V2 §3.12 C1 + C2 + C3;
    # strict rule V5.20): the telephones and the form are one channel board, its heading «Par téléphone, WhatsApp ou
    # formulaire», which still names only the channels the settings hold (the same rule, in the board's words)
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D,
    # «lo sportello»): the board is the desk «Canaux de contact» beside the form's own seat — its rows name only the
    # channels the settings hold, the address first, each once on the page
    assert main.count('href="tel:800642015"') == 1 and main.count(WHATSAPP_URL) == 1
    assert _desk_rows(main) == ["email", "voce", "whatsapp"]
    with translation.override(lang):
        assert translation.gettext("Canaux de contact") in main.split('id="contact-channels-title"', 1)[1][:200]


@pytest.mark.parametrize("lang", LANGS)
def test_the_footer_and_the_sheet_draw_both_channels(page, seeded, whatsapp_channel, lang):
    _response, html = page(f"/{lang}/")
    freephone_name, whatsapp_name = _names(lang)
    for fragment in (_footer(html), _sheet(html)):
        links = _links(fragment)
        assert links["tel:800642015"] == freephone_name
        assert links[WHATSAPP_URL] == whatsapp_name
        assert f'<bdi class="phone" dir="ltr">{FREEPHONE_LABEL}</bdi>' in fragment
    assert f'<bdi class="phone" dir="ltr">{html_lib.escape(WHATSAPP_LABEL)}</bdi>' in _footer(html)


@pytest.mark.usefixtures("faq_case_open")  # V5.20: the FAQ opened for its case (pages/tests/conftest.py), never skipped
@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("path", ["", "contact/", "le-projet/", "agami/", "faq/"])
def test_no_obsolete_number_on_a_public_page(page, seeded, whatsapp_channel, lang, path):
    response, html = page(f"/{lang}/{path}")
    assert response.status_code == 200, (lang, path, response.status_code)
    for value in OBSOLETE:
        assert value not in html, (path, value)
    # every tel: link is one of the configured channels'; every wa.me link the configured one
    assert set(re.findall(r'href="tel:([^"]*)"', html)) <= {"800642015", WHATSAPP_DIGITS}
    assert set(re.findall(r'href="(https://wa\.me/[^"]*)"', html)) <= {WHATSAPP_URL}


def test_arabic_keeps_the_digit_groups_in_order(page, seeded, whatsapp_channel):
    """In the Arabic page every visible number is inside an LTR isolate, its groups in the owner's order."""
    _response, html = page("/ar/contact/")
    assert 'dir="rtl"' in html.split("<body", 1)[0]
    shown = re.findall(r'<bdi class="[^"]*phone[^"]*" dir="ltr">([^<]+)</bdi>', html)
    assert html_lib.unescape(shown[0]) in (FREEPHONE_LABEL, WHATSAPP_LABEL)
    assert {html_lib.unescape(s) for s in shown} == {FREEPHONE_LABEL, WHATSAPP_LABEL}
    # no number outside an isolate in the visible text of the channels
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # the contact desk's links are held to the same rule as the footer's and the sheet's
    channel = r'<a class="(?:canale__link|sportello-canale__link|site-footer__channel|nav-sheet__channel)".*?</a>'
    assert len(re.findall(r'<a class="sportello-canale__link"', html)) == 2
    for fragment in re.findall(channel, html, re.S):
        bare = re.sub(r"<bdi[^>]*>[^<]*</bdi>", "", re.sub(r'aria-label="[^"]*"', "", fragment))
        assert not re.search(r"\d{3}", re.sub(r"<[^>]+>", " ", bare).replace("#", " ")), fragment


def test_a_blank_setting_withdraws_its_channel(page, seeded, whatsapp_channel):
    _response, html = page("/fr/contact/")
    assert WHATSAPP_URL in _main(html) and WHATSAPP_URL in _footer(html)
    settings_row = SiteSettings.load()
    settings_row.whatsapp_number = ""  # the back office's blank wins over the environment's default
    settings_row.save()
    _response, html = page("/fr/contact/")
    assert "wa.me" not in html and "WhatsApp" not in _footer(html)
    assert 'href="tel:800642015"' in _main(html)
    settings_row.freephone_number = ""
    settings_row.save()
    _response, html = page("/fr/contact/")
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # with both voices blank the desk is the address's row alone
    assert "tel:" not in html and _desk_rows(_main(html)) == ["email"]


@pytest.mark.parametrize("lang", LANGS)
def test_with_nothing_configured_the_whatsapp_channel_is_absent_everywhere(page, seeded, no_whatsapp_channel, lang):
    """
    V5.20 (option B): ILE_WHATSAPP_NUMBER unset and the back office's number blank — a fresh clone, CI, a server before
    the owner configures it. No surface draws or names the channel: no wa.me link, no international telephone link, no
    glyph, no word «WhatsApp»; the contact page's chapter is the telephone's alone. Never skipped: every page below is
    served in every language.
    """
    for path in ALWAYS_SERVED:
        response, html = page(f"/{lang}/{path}")
        assert response.status_code == 200, (lang, path, response.status_code)
        assert "wa.me" not in html and "tel:+" not in html, (lang, path)
        assert "#icon-message-circle" not in html and "canale--whatsapp" not in html, (lang, path)
        assert "WhatsApp" not in html, (lang, path)
        # the Numero Verde stays: the footer and the phone's sheet
        assert 'href="tel:800642015"' in _footer(html) and 'href="tel:800642015"' in _sheet(html), (lang, path)
    _response, html = page(f"/{lang}/contact/")
    main = _main(html)
    assert main.count('href="tel:800642015"') == 1
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # the desk's rows are the address's and the Numero Verde's — WhatsApp is not named (the board's rule, by its rows)
    assert _desk_rows(main) == ["email", "voce"]


# ---- the owner-confirmed number, where it is configured ------------------------------------------------------------
def test_the_configured_whatsapp_number_is_the_one_the_contact_page_links(page, seeded):
    """
    V5.20 (option B): the owner-confirmed WhatsApp number is never written in the repository; it is configured in the
    environment (ILE_WHATSAPP_NUMBER: the server's environment file, the local untracked .env, the shell). Where it is,
    a new settings row takes it, and the contact page links exactly https://wa.me/<its digits> and shows them in the
    owner's grouping («+39», then 3-3-4: V5.19), in French and in Arabic, with the channel's accessible name.

    Modelled on tests/security/test_confidential_material.py's private-table test: SKIPPED, with the reason in the run
    summary, only where the variable is unset (CI, a fresh clone), so a green run never reads as «the owner's number
    was checked»; a value that is set but is not an international number FAILS. No message prints the number.
    """
    configured = os.environ.get(WHATSAPP_VARIABLE, "").strip()
    if not configured:
        pytest.skip(
            f"{WHATSAPP_VARIABLE} is not set: the owner-confirmed WhatsApp number is checked only where it is "
            "configured (the server's environment file or the local .env, outside the repository — V5.20, option B)"
        )
    digits = contact.canonical(configured)
    assert re.fullmatch(r"\+\d{8,15}", digits), f"{WHATSAPP_VARIABLE} is set but is not an international number"
    read = django_settings.ILE["WHATSAPP_NUMBER"] == os.environ[WHATSAPP_VARIABLE]
    assert read, "settings.ILE['WHATSAPP_NUMBER'] is not the environment's ILE_WHATSAPP_NUMBER"
    if digits.startswith("+39"):
        national = digits[3:]
        assert len(national) == 10, f"{WHATSAPP_VARIABLE}: an Italian mobile has ten digits after +39"
        label = f"+39 {national[:3]} {national[3:6]} {national[6:]}"
    else:
        label = contact.international_label(digits)
    url = f"https://wa.me/{digits[1:]}"
    SiteSettings.objects.all().delete()  # the row the page makes takes the environment's number
    for lang in ("fr", "ar"):
        response, html = page(f"/{lang}/contact/")
        assert response.status_code == 200
        main = _main(html)
        linked = set(re.findall(r'href="(https://wa\.me/[^"]*)"', html)) == {url}
        assert linked, f"/{lang}/contact/ does not link exactly the configured https://wa.me/<digits>"
        once = main.count(f'href="{url}"') == 1
        assert once, f"/{lang}/contact/: the configured WhatsApp link is not drawn once in the page's body"
        # the left-to-right isolate around the grouped number, whatever its class (V5.32 restyled the desk's rows)
        isolate = r'<bdi\b[^>]*\bdir="ltr"[^>]*>' + re.escape(html_lib.escape(label)) + r"</bdi>"
        grouped = re.search(isolate, main) is not None
        assert grouped, f"/{lang}/contact/: the number is not shown in the owner's grouping, left to right"
        named = _links(main).get(url) == _names(lang, label)[1]
        assert named, f"/{lang}/contact/: the WhatsApp link's accessible name is not the channel's"
    stored = SiteSettings.load().whatsapp_number == os.environ[WHATSAPP_VARIABLE]
    assert stored, "the new settings row does not hold the environment's number"
