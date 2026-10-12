"""
The interface is really translated: navigation, skip link, footer, the « form unavailable » notice, error
pages and plural sentences are asserted in Italian, English and Arabic on rendered pages — and no French
interface string leaks into the Arabic navigation.
"""

from __future__ import annotations

import gettext as gettext_module
import re

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.utils import translation

from core import views as core_views

from .conftest import TRANSLATED, region, text_nodes

pytestmark = pytest.mark.django_db

EXPECTED = {
    "it": {
        "skip": "Vai al contenuto principale",
        "nav_label": "Navigazione principale",
        "menu_button": "Menu",
        "nav": [
            "Persone",
            "Imprese",
            "Progetto",
            "Il proprio percorso",
            "Fabbisogni professionali",
            "Rete",
            "Contatti",
        ],
        "forum": "Forum Vénétie–Maroc",
        "footer_headings": ["Informazioni legali", "Navigazione", "Il progetto"],
        "footer_links": ["Note legali", "Privacy Policy", "Cookie Policy", "Condizioni di utilizzo", "Avvertenze"],
        "home": "Pagina iniziale",
        "language_label": "Scegli la lingua",
        "form_unavailable": "Modulo temporaneamente non disponibile.",
        "legal_blocked": "Pagina in corso di preparazione.",
        "errors": {
            400: "Richiesta non valida",
            403: "Accesso non autorizzato",
            404: "Pagina non trovata",
            429: "Troppe richieste",
            500: "Errore tecnico",
        },
        "back_home": "Torna alla pagina iniziale",
    },
    "en": {
        "skip": "Skip to main content",
        "nav_label": "Main navigation",
        "menu_button": "Menu",
        "nav": ["Individuals", "Enterprises", "Project", "Your pathway", "Professional needs", "Network", "Contact"],
        "forum": "Forum Vénétie–Maroc",
        "footer_headings": ["Legal information", "Navigation", "The project"],
        "footer_links": ["Legal notice", "Privacy Policy", "Cookie Policy", "Terms of use", "Disclaimer"],
        "home": "Home",
        "language_label": "Choose language",
        "form_unavailable": "Form temporarily unavailable.",
        "legal_blocked": "Page under preparation.",
        "errors": {
            400: "Invalid request",
            403: "Access not authorised",
            404: "Page not found",
            429: "Too many requests",
            500: "Technical error",
        },
        "back_home": "Back to the home page",
    },
    "ar": {
        "skip": "الانتقال إلى المحتوى الرئيسي",
        "nav_label": "التنقل الرئيسي",
        "menu_button": "القائمة",
        "nav": ["الأفراد", "الشركات", "المشروع", "مساركم", "الاحتياجات المهنية", "الشبكة", "اتصل بنا"],
        "forum": "منتدى Vénétie–Maroc",
        "footer_headings": ["المعلومات القانونية", "التنقل", "المشروع"],
        "footer_links": ["الإشعارات القانونية", "Privacy Policy", "Cookie Policy", "شروط الاستخدام", "تنبيه"],
        "home": "الرئيسية",
        "language_label": "اختيار اللغة",
        "form_unavailable": "النموذج غير متاح مؤقتًا.",
        "legal_blocked": "الصفحة قيد الإعداد.",
        "errors": {
            400: "طلب غير صالح",
            403: "دخول غير مرخَّص",
            404: "الصفحة غير موجودة",
            429: "عدد كبير جدًا من الطلبات",
            500: "خطأ تقني",
        },
        "back_home": "العودة إلى الصفحة الرئيسية",
    },
}

#: French interface strings that must never be visible in the Arabic header / footer.
FRENCH_UI = [
    "Personnes",
    "Entreprises",
    "Projet",
    "Votre parcours",
    "Besoins professionnels",
    "Réseau",
    "Contact",
    "Accueil",
    "Menu",
    "Voir l’espace",
    "Ouvrir le sous-menu",
    "Navigation",
    "Informations légales",
    "Mentions légales",
    "Conditions d’utilisation",
    "Avertissement",
    "Le projet",
    "promoteur du projet",
    "Langue",
    "Aller au contenu principal",
]

#: Latin-script text allowed inside the Arabic header and footer: proper nouns, the trademark, the two
#: policy names kept in the original, the e-mail address, language endonyms and codes, the version label
#: (an editorial SiteSettings value). Anything else in Latin script is an untranslated string.
ARABIC_LATIN_ALLOWED = re.compile(
    # «Italy», «Legal», «Entry» on their own: the official lock-up sets the trademark's three words in
    # the three colours of the flag, one span each (v2/shell.css .lock__w1 / .lock__w3).
    r"Italy Legal Entry(?:™)?|Italy|Legal|Entry|AGAMI — Dialogo Giuridico Interculturale APS|AGAMI|Vénétie–Maroc|Privacy Policy|"
    r"Cookie Policy|contact@agamieuromed\.org|Italiano|Français|English|\b(?:it|fr|en|ar)\b|v\d+\.\d+\.\d+ — Fase \d"
)
_LATIN_WORD = re.compile(r"[A-Za-zÀ-ÿ]{2,}")


@pytest.mark.parametrize("lang", TRANSLATED)
def test_skip_link_header_and_navigation_are_translated(client, seeded, lang):
    html = client.get(f"/{lang}/").content.decode()
    expected = EXPECTED[lang]
    assert f'<a class="skip-link" href="#main-content">{expected["skip"]}</a>' in html
    header = region(html, "header")
    assert f'aria-label="{expected["nav_label"]}"' in header
    nodes = text_nodes(header)
    assert expected["menu_button"] in nodes
    for label in [*expected["nav"], expected["forum"]]:
        assert label in nodes, (lang, label)


@pytest.mark.parametrize("lang", TRANSLATED)
def test_footer_headings_and_legal_links_are_translated(client, seeded, lang):
    footer = region(client.get(f"/{lang}/").content.decode(), "footer")
    expected = EXPECTED[lang]
    headings = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<h2\b[^>]*>.*?</h2>", footer, re.S)]
    assert headings == expected["footer_headings"]
    nodes = text_nodes(footer)
    for label in [*expected["footer_links"], expected["home"]]:
        assert label in nodes, (lang, label)
    # The two policy names are kept in the original in every language, and they are links, not gettext.
    assert '">Privacy Policy</a>' in footer and '">Cookie Policy</a>' in footer


@pytest.mark.parametrize("lang", TRANSLATED)
def test_language_switcher_is_labelled_in_the_page_language(client, seeded, lang):
    html = client.get(f"/{lang}/").content.decode()
    assert f'aria-label="{EXPECTED[lang]["language_label"]}"' in html


@pytest.mark.parametrize("lang", TRANSLATED)
def test_form_unavailable_notice_is_translated_on_every_public_form(before_the_forum, client, seeded, lang):
    # The Forum form shows the notice only while registration is open, i.e. before the event ended
    # (2 Oct 2026, 18:00 Rome): the clock is frozen in the run-up to the Forum, not read for real.
    for path in ("entreprises/recueil-des-besoins/", "contact/formulaire/", "forum/inscription/"):
        html = client.get(f"/{lang}/{path}").content.decode()
        assert 'data-gate="forms-closed"' in html, (lang, path)
        assert EXPECTED[lang]["form_unavailable"] in html, (lang, path)
        assert "Formulaire temporairement indisponible." not in html, (lang, path)
        assert 'href="mailto:contact@agamieuromed.org"' in html


@pytest.mark.parametrize("lang", TRANSLATED)
def test_blocked_legal_page_notice_is_translated_and_shows_no_legal_text(client, seeded, lang):
    html = client.get(f"/{lang}/privacy-policy/").content.decode()
    main = region(html, "main")
    assert 'data-gate="legal-blocked"' in main
    assert EXPECTED[lang]["legal_blocked"] in main
    assert "Page en cours de préparation." not in main
    assert max(len(node) for node in text_nodes(main)) < 400, "no legal text may be rendered while G1 is closed"


@pytest.mark.parametrize("lang", TRANSLATED)
def test_not_found_page_is_translated(client, seeded, lang):
    response = client.get(f"/{lang}/cette-page-n-existe-pas/")
    assert response.status_code == 404
    main = region(response.content.decode(), "main")
    assert re.search(rf"<h1\b[^>]*>{re.escape(EXPECTED[lang]['errors'][404])}</h1>", main)
    assert EXPECTED[lang]["back_home"] in main
    assert "Page introuvable" not in main


@pytest.mark.parametrize("lang", TRANSLATED)
@pytest.mark.parametrize("status", [400, 403, 429, 500])
def test_error_pages_are_translated(seeded, lang, status):
    request = RequestFactory().get(f"/{lang}/")
    request.user = AnonymousUser()
    view = getattr(core_views, f"error_{status}")
    with translation.override(lang):
        response = view(request)
    html = response.content.decode()
    assert response.status_code == status
    assert f'<html lang="{lang}" dir="{"rtl" if lang == "ar" else "ltr"}"' in html
    assert len(re.findall(r"<h1\b", html)) == 1
    assert re.search(rf"<h1\b[^>]*>{re.escape(EXPECTED[lang]['errors'][status])}</h1>", html), (lang, status)


def test_no_french_interface_string_leaks_into_the_arabic_header_and_footer(client, seeded):
    html = client.get("/ar/").content.decode()
    for part in ("header", "footer"):
        nodes = text_nodes(region(html, part))
        assert nodes, part
        for french in FRENCH_UI:
            assert french not in nodes, (part, french)
            assert not any(node.startswith(french + " ") for node in nodes), (part, french)


def test_latin_text_in_the_arabic_chrome_is_limited_to_proper_nouns(client, seeded, audit):
    """Every Latin-script node of the Arabic header/footer is a proper noun or a documented keep-source text."""
    html = client.get("/ar/").content.decode()
    # The institutional bar ends where the header begins (since design V4 it carries no <details>).
    utility = re.search(r'<div class="utility-bar.*?(?=<header\b)', html, re.S).group(0)
    leaks = []
    for fragment in (utility, region(html, "header"), region(html, "footer")):
        for node in text_nodes(fragment):
            if node in audit.KEEP_SOURCE:
                continue  # locked-derived wording: never translated by the team (change requested to its owner)
            if _LATIN_WORD.search(ARABIC_LATIN_ALLOWED.sub("", node)):
                leaks.append(node)
    assert leaks == []


def test_arabic_navigation_attributes_are_translated(client, seeded):
    header = region(client.get("/ar/").content.decode(), "header")
    for value in re.findall(r'aria-label="([^"]*)"', header):
        assert not _LATIN_WORD.search(ARABIC_LATIN_ALLOWED.sub("", value)), value


@pytest.mark.parametrize("lang", TRANSLATED)
def test_plural_sentence_is_rendered_through_the_template_tag(client, seeded, phase3_open, audit, catalogues, lang):
    """{% blocktranslate count %} on the FAQ search picks the plural form of the page language."""
    response = client.get(f"/{lang}/faq/", {"q": "Italy"})
    assert response.status_code == 200
    count = len(response.context["entries"])
    assert count >= 2, "the seeded locked FAQ mentions the project several times"
    entry = catalogues[lang][(None, "%(counter)s résultat pour « %(q)s »")]
    # The index comes from the project's own Plural-Forms header: Django's Italian catalogue declares three
    # forms, ours two — Django keeps one plural rule per catalogue, so ours must win for our messages.
    header = audit.header_fields(audit.parse_po(audit.po_path(lang)))["Plural-Forms"]
    index = gettext_module.c2py(header.split("plural=", 1)[1].rstrip(";"))(count)
    expected = entry.msgstr[index] % {"counter": count, "q": "Italy"}
    heading = re.search(r'<h2 id="faq-results-title">(.*?)</h2>', response.content.decode(), re.S).group(1)
    assert heading.strip() == expected
    assert "résultat" not in heading


# ---------------------------------------------------------------------------------------------
# E-mails sent to a visitor are written in the language of the request that queued them
# ---------------------------------------------------------------------------------------------
_VISITOR_EMAILS = {
    "enquiries_acknowledgement": {"kind_label": "—", "submitted_at": None},
    "forum_registration_ack": {
        "registration": {"first_name": "Test"},
        "event_title": "Forum Vénétie–Maroc",
        "event_meta": "",
        "category_label": "—",
        "contact_email": "contact@agamieuromed.org",
    },
    "newsletter_confirm": {
        "confirm_url": "http://testserver/x/",
        "unsubscribe_url": "http://testserver/y/",
        "contact_email": "contact@agamieuromed.org",
    },
}


@pytest.mark.parametrize("lang", TRANSLATED)
@pytest.mark.parametrize("template", sorted(_VISITOR_EMAILS))
def test_visitor_emails_are_rendered_in_the_language_of_the_request(catalogues, template, lang):
    from django.utils import timezone

    from notifications.services import queue_email

    context = dict(_VISITOR_EMAILS[template])
    if "submitted_at" in context:
        context["submitted_at"] = timezone.now()
    with translation.override(lang):
        item = queue_email(to_email="visitor@example.test", subject="x", template=template, context=context)
    lines = [line.strip() for line in item.body_text.splitlines() if line.strip()]
    assert len(lines) >= 5, item.body_text
    french = {e.msgid for e in catalogues[lang].values() if len(e.msgid) > 3 and e.msgstr[0] != e.msgid}
    assert [line for line in lines if line in french] == []
    assert not any(line.startswith(("Bonjour", "Votre demande", "Nous accusons")) for line in lines), lines
    if lang == "ar":
        latin_only = [
            line
            for line in lines
            if not re.search(r"[\u0600-\u06FF]", line)
            and _LATIN_WORD.search(re.sub(r"https?://\S+", "", ARABIC_LATIN_ALLOWED.sub("", line)))
        ]
        assert latin_only == [], latin_only
