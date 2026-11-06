"""
V5.12 lane D, wave W2 — the organisation space, the empty-state wall, the console's foot, the footer's legal links and
the account pages' words (docs/design-v5/QA/v512/d-w2/NOTES.md; Director's decisions §8, §9, §12 Q2/Q7, §13).

* Q7 an institution, a university, a training body has its OWN space: «Espace Institutions» / «Espace Universités et
  Formation» at the rail's head, a rail with no person's module, a dashboard composed for the organisation (its identity,
  its registers with rows only, the project's public pages it works with), «Mon organisation»; the person's pages send
  it back. No CTA for a closed capability.
* D-08 / D-22 a company's «Espace réservé» has no person's module either, its dashboard an ungrouped first row.
* §8 the Academy is a page of the rail only while a course is published (or the account holds an enrolment).
* D-20 a bridge register is drawn only with rows: no heading over «… apparaîtront ici».
* D-16 the console's foot names the promoter and says, in the locked words, that ILE is not an authority.
* Q2 / V5.14 §13 the footer links only the legal pages that are published; D-24 the fraud link says the glossary's word.
* D-11 the account pages speak the glossary: «Créer un compte», «Se connecter», «Adresse e-mail» — never «Sign Up»,
  «الاشتراك», «Courriel».
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
from django.template import Context, Template
from django.test import RequestFactory
from django.urls import reverse
from django.utils import translation

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps"))
sys.path.insert(0, str(ROOT / "scripts"))

from accounts import roles  # noqa: E402
from accounts.models import AccountType, Membership, MembershipRole, Organisation  # noqa: E402

LANGS = ("fr", "it", "en", "ar")
SPACE = {
    "institution": {
        "fr": "Espace Institutions",
        "it": "Area Istituzioni",
        "en": "Institutions Area",
        "ar": "فضاء المؤسسات",
    },
    "university": {
        "fr": "Espace Universités et Formation",
        "it": "Area Università e Formazione",
        "en": "Universities and Training Area",
        "ar": "فضاء الجامعات والتكوين",
    },
}
PERSON_KEYS = {"situation", "pathways", "cases", "documents", "helpdesk", "academy", "disclosures"}


def _organisation_account(user_factory, kind: str, email: str):
    role = {"institution": roles.INSTITUTION, "university": roles.UNIVERSITY}[kind]
    user = user_factory(email, role=role, full_name=f"Ufficio {kind}", account_type=kind)
    organisation = Organisation.objects.create(
        name=f"Comune di prova {kind}", kind=kind, country="Italia", city="Rovigo"
    )
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    return user


@pytest.fixture
def institution(user_factory):
    return _organisation_account(user_factory, "institution", "d-w2.institution@example.test")


@pytest.fixture
def university(user_factory):
    return _organisation_account(user_factory, "university", "d-w2.university@example.test")


@pytest.fixture
def company_user(user_factory):
    # typed «person» by default, as the preview's company account is: the role names it
    return user_factory("d-w2.company@example.test", role=roles.COMPANY, full_name="Giulia Ferrante")


def _rail(html: str) -> list[str]:
    return re.findall(r'data-rail-item data-rail-tip data-key="([^"]+)"', html)


# ---- Q7: the organisation's own space ----------------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("kind", ["institution", "university"])
@pytest.mark.parametrize("lang", LANGS)
def test_an_organisation_has_its_own_space_and_rail(client, seeded, user_factory, kind, lang):
    user = _organisation_account(user_factory, kind, f"d-w2.{kind}.{lang}@example.test")
    client.force_login(user)
    with translation.override(lang):
        html = client.get(reverse("portal:dashboard")).content.decode()
    assert re.findall(r"data-rail-space>([^<]+)<", html)[:1] == [SPACE[kind][lang]]
    keys = _rail(html)
    assert set(keys) >= {"dashboard", "organisation", "requests", "messages"}, keys
    assert not set(keys) & PERSON_KEYS, "no person's module in an organisation's rail"
    assert "Comune di prova" in html, "the organisation's own name heads its dashboard"


@pytest.mark.django_db
def test_the_organisation_space_has_its_own_key_for_the_loader(institution):
    from portal import services

    nav = services.navigation(institution, "dashboard")
    assert nav[0]["space"]["key"] == services.SPACE_ORGANISATION, "the console's first page of the space lights once"
    assert services.organisation_audience(institution) == "institution"


@pytest.mark.django_db
def test_the_dates_are_a_page_of_the_rail_only_once_the_team_set_one(institution):
    import datetime as dt

    from portal import services
    from portal.models import Deadline

    assert "deadlines" not in {entry["key"] for entry in services.navigation(institution)}
    Deadline.objects.create(owner=institution, title="Riunione", due_on=dt.date(2026, 11, 3))
    assert "deadlines" in {entry["key"] for entry in services.navigation(institution)}


@pytest.mark.django_db
@pytest.mark.parametrize("route", ["portal:situation", "portal:pathways", "cases:index"])
def test_the_person_s_pages_send_an_organisation_back_to_its_dashboard(client, seeded, institution, route):
    client.force_login(institution)
    response = client.get(reverse(route))
    assert response.status_code == 302 and response["Location"] == reverse("portal:dashboard")


@pytest.mark.django_db
def test_an_organisation_s_documents_are_on_its_organisation_page(client, seeded, institution):
    client.force_login(institution)
    response = client.get(reverse("portal:documents"))
    assert response.status_code == 302 and response["Location"] == reverse("portal:organisation")


@pytest.mark.django_db
def test_the_organisation_dashboard_is_composed_for_the_organisation(client, seeded, institution):
    client.force_login(institution)
    with translation.override("fr"):
        html = client.get(reverse("portal:dashboard")).content.decode()
    assert "Italy Legal Entry promeut des modèles de coopération institutionnelle" in html, "the locked §3.4 lead"
    assert "Accédez à votre espace personnel" not in html, "never the person's «espace personnel»"
    for words in ("Commencer l’orientation", "Date de naissance", "apparaîtront ici", "Mon parcours"):
        assert words not in html, words
    assert 'data-card="organisation"' in html and "Responsable" in html, "the identity sheet and the account's role"
    assert "Aucune action ne vous est demandée pour l’instant." in html, "nothing under way: one calm sentence"


@pytest.mark.django_db
def test_no_collaboration_cta_while_the_public_form_is_closed(client, seeded, institution, university):
    from core import gates

    assert not gates.public_forms_enabled().open
    for account, button in ((institution, "PROPOSEZ UNE COLLABORATION"), (university, "COLLABOREZ AVEC NOUS")):
        client.force_login(account)
        with translation.override("fr"):
            html = client.get(reverse("portal:dashboard")).content.decode()
        assert button not in html, "no CTA for a capability that is closed (Q7)"


@pytest.mark.django_db
def test_the_collaboration_cta_appears_with_the_open_form(client, seeded, legal_published, university):
    client.force_login(university)
    with translation.override("fr"):
        html = client.get(reverse("portal:dashboard")).content.decode()
    assert "COLLABOREZ AVEC NOUS" in html
    assert reverse("enquiries:university_proposal") in html


@pytest.mark.django_db
def test_a_register_with_rows_is_drawn_and_an_empty_one_is_not(client, seeded, university):
    from portal import services

    services.send_message(recipient=university, subject="Incontro di coordinamento", body="Testo.")
    client.force_login(university)
    with translation.override("fr"):
        html = client.get(reverse("portal:dashboard")).content.decode()
    assert 'data-card="messages"' in html and "Incontro di coordinamento" in html
    assert 'data-card="requests"' not in html and 'data-card="deadlines"' not in html
    assert "Aucune action ne vous est demandée" not in html


@pytest.mark.django_db
def test_the_project_s_pages_are_offered_only_while_public(institution):
    from core.links import public_url
    from portal import services

    rows = services.organisation_references("institution")
    assert rows, "the institution's own public space at least"
    for row in rows:
        assert row["url"], row
    assert all(row["url"] for row in rows)
    forum = public_url("forum:index")
    assert (forum in {row["url"] for row in rows}) == bool(forum), "the Forum only with a live edition"


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_my_organisation_shows_the_identity_sheet(client, seeded, university, lang):
    client.force_login(university)
    with translation.override(lang):
        response = client.get(reverse("portal:organisation"))
    html = response.content.decode()
    assert response.status_code == 200
    assert "Comune di prova university" in html and "Rovigo" in html
    assert re.search(r'aria-current="page" data-rail-item data-rail-tip data-key="organisation"', html), (
        "the rail lights it"
    )


@pytest.mark.django_db
def test_my_organisation_is_not_a_person_s_page(client, seeded, user_factory):
    person = user_factory("d-w2.person@example.test", role=roles.PERSON, account_type=AccountType.PERSON)
    client.force_login(person)
    response = client.get(reverse("portal:organisation"))
    assert response.status_code == 302 and response["Location"] == reverse("portal:dashboard")


# ---- D-08 / D-22: a company's «Espace réservé» ----------------------------------------------------------------------------
@pytest.mark.django_db
def test_a_company_s_reserved_area_has_no_person_s_module(client, seeded, company_user):
    from portal import services

    nav = services.navigation(company_user)
    keys = {entry["key"] for entry in nav}
    assert not keys & {"situation", "pathways", "cases"}, keys
    dashboard = next(entry for entry in nav if entry["key"] == "dashboard")
    assert dashboard["group"] == dashboard["space"]["label"], "the dashboard is the space's ungrouped first row"
    client.force_login(company_user)
    for route in ("portal:situation", "portal:pathways", "cases:index"):
        response = client.get(reverse(route))
        assert response.status_code == 302, route
    html = client.get(reverse("portal:dashboard")).content.decode()
    assert "Commencer l’orientation" not in html, "a company is never asked to start the person's questionnaire"
    assert "db-now" not in html, "no NowPanel: the bridge"


@pytest.mark.django_db
def test_the_bridge_draws_no_empty_wall(client, seeded, company_user):
    client.force_login(company_user)
    with translation.override("fr"):
        html = client.get(reverse("portal:dashboard")).content.decode()
    assert "apparaîtront ici" not in html, "no heading over «… apparaîtront ici» (D-20)"
    assert "Aucune action ne vous est demandée pour l’instant." in html


# ---- D-20 on the person's side column (the W2 review's major) --------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_a_person_s_side_column_draws_no_empty_wall(client, seeded, user_factory, lang):
    person = user_factory(f"d-w2.person.{lang}@example.test", full_name="Amina Prova")
    client.force_login(person)
    with translation.override(lang):
        html = client.get(reverse("portal:dashboard")).content.decode()
        calm = translation.gettext("Aucune échéance ni communication pour l’instant.")
    assert 'class="db-dates"' not in html and 'class="db-messages"' not in html, "no head over nothing"
    assert "apparaîtront ici" not in html
    assert calm in html and (lang == "fr" or calm != "Aucune échéance ni communication pour l’instant.")


@pytest.mark.django_db
def test_a_person_s_register_with_rows_is_drawn_and_the_other_is_not(client, seeded, user_factory):
    import datetime as dt

    from core import clock
    from portal.models import Deadline

    person = user_factory("d-w2.person.dated@example.test", full_name="Amina Prova")
    Deadline.objects.create(owner=person, title="Visite médicale", due_on=clock.today() + dt.timedelta(days=40))
    client.force_login(person)
    with translation.override("fr"):
        html = client.get(reverse("portal:dashboard")).content.decode()
    assert "Visite médicale" in html
    assert 'class="db-messages"' not in html and "Aucune échéance ni communication" not in html


@pytest.mark.django_db
def test_a_person_s_unreadable_register_says_so(client, seeded, user_factory, monkeypatch):
    from portal import services

    def broken(_user):
        raise LookupError("a sibling app changed shape")

    monkeypatch.setattr(services, "_dashboard_messages", broken)
    person = user_factory("d-w2.person.broken@example.test", full_name="Amina Prova")
    client.force_login(person)
    with translation.override("fr"):
        html = client.get(reverse("portal:dashboard")).content.decode()
    messages = html.split('class="db-messages"', 1)[1].split("</section>", 1)[0]
    assert "momentanément indisponible" in messages, "an honest «indisponible», never «… apparaîtront ici»"
    assert "Aucune échéance ni communication" not in html


# ---- the organisation's country and trail (the W2 review's minors) -------------------------------------------------------
COUNTRY = {"fr": "Italie", "it": "Italia", "en": "Italy", "ar": "إيطاليا"}


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_identity_sheet_names_the_country_in_the_reader_s_language(client, seeded, university, lang):
    pytest.importorskip("core.countries")
    client.force_login(university)
    with translation.override(lang):
        html = client.get(reverse("portal:organisation")).content.decode()
    assert COUNTRY[lang] in html
    if lang in {"fr", "ar"}:
        assert '<dd dir="auto">Italia</dd>' not in html, "never the raw stored word"


def test_an_unknown_country_is_shown_as_stored():
    from portal.services import country_label

    assert country_label("") == ""
    assert country_label("Atlantide") == "Atlantide"


@pytest.mark.django_db
@pytest.mark.parametrize("kind", ["institution", "university"])
def test_the_trail_starts_with_the_space_s_name(client, seeded, user_factory, kind):
    user = _organisation_account(user_factory, kind, f"d-w2.trail.{kind}@example.test")
    client.force_login(user)
    with translation.override("fr"):
        html = client.get(reverse("portal:organisation")).content.decode()
    trail = html.split('class="breadcrumbs', 1)[1].split("</nav>", 1)[0]
    assert SPACE[kind]["fr"] in trail and "Espace réservé" not in trail


# ---- §8: the Academy, only with a course ------------------------------------------------------------------------------
@pytest.mark.django_db
def test_the_academy_is_a_page_of_the_rail_only_with_a_published_course(user_factory):
    from academy.models import Course, CourseStatus
    from portal import services

    person = user_factory("d-w2.academy@example.test", role=roles.PERSON, account_type=AccountType.PERSON)
    Course.objects.update(status=CourseStatus.DRAFT)
    assert "academy" not in {entry["key"] for entry in services.navigation(person)}
    assert not services.academy_open(person)


@pytest.mark.django_db
def test_the_academy_is_a_page_of_the_rail_with_a_published_course(user_factory, academy_courses):
    from portal import services

    person = user_factory("d-w2.academy2@example.test", role=roles.PERSON, account_type=AccountType.PERSON)
    assert services.academy_open(person)
    assert [entry["key"] for entry in services.navigation(person)][-1] == "academy"


@pytest.fixture
def academy_courses(db, settings):
    from django.core.management import call_command

    settings.ILE_SEED_DEMONSTRATION_DATA = True
    call_command("seed_all", "--only", "academy", verbosity=0)


# ---- D-16: the console's foot -------------------------------------------------------------------------------------------
LOCKED_STATEMENT = (
    "Italy Legal Entry ne délivre pas de visas, de permis de séjour ni d’autorisations : ces décisions relèvent "
    "exclusivement des autorités compétentes."
)


def _render(source: str, lang: str = "fr") -> str:
    from core.context_processors import site as site_context

    request = RequestFactory().get("/")
    with translation.override(lang):
        context = Context({**site_context(request), "request": request})
        return Template(source).render(context)


def test_the_locked_statement_is_the_first_sentence_of_the_locked_text():
    from cms import locked_content
    from portal.templatetags.console_foot import first_sentence

    whole = locked_content.get("p3.persons.intro", "fr")[0]
    assert first_sentence(whole) == LOCKED_STATEMENT
    assert whole.startswith(first_sentence(whole)), "cut from the locked text, never retyped"


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_console_foot_names_the_promoter_and_says_ilE_is_not_an_authority(lang):
    html = _render('{% include "portal/partials/console_foot.html" %}', lang)
    assert "AGAMI — Dialogo Giuridico Interculturale APS" in html
    assert LOCKED_STATEMENT in html
    if lang != "fr":
        assert 'lang="fr"' in html, "the French fallback is marked as French"
    assert "privacy-policy" not in html, "no link to an unpublished legal page"


@pytest.mark.django_db
def test_the_console_foot_links_the_published_privacy_notice(legal_published):
    html = _render('{% include "portal/partials/console_foot.html" %}')
    assert reverse("legal:privacy") in html and reverse("legal:cookies") in html


# ---- Q2 / V5.14 §13: the footer's legal links ------------------------------------------------------------------------------
@pytest.mark.django_db
def test_the_footer_links_no_unpublished_legal_page(client, seeded):
    html = client.get(reverse("pages:home")).content.decode()
    footer = html.split('id="site-footer"', 1)[1]
    for name in ("legal:notices", "legal:privacy", "legal:cookies", "legal:terms", "legal:disclaimer"):
        assert f'href="{reverse(name)}"' not in footer, name
    assert "Informations légales" not in footer, "the column leaves with its links"
    assert "site-footer__inner--three" in footer


@pytest.mark.django_db
def test_the_footer_links_each_published_legal_page(client, seeded, legal_published):
    footer = client.get(reverse("pages:home")).content.decode().split('id="site-footer"', 1)[1]
    for name in ("legal:notices", "legal:privacy", "legal:cookies", "legal:terms", "legal:disclaimer"):
        assert f'href="{reverse(name)}"' in footer, name
    assert "site-footer__inner--three" not in footer


@pytest.mark.django_db
def test_a_single_published_page_is_linked_alone(superuser):
    from legal import services
    from legal.templatetags.legal_links import legal_links

    assert legal_links() == [], "nothing published yet: the answer is cached per kind"
    doc = services.get_document("cookies")
    doc.body_it = "Testo di prova."
    doc.source_reference = "Fonte di prova"
    doc.save()
    services.publish(doc, superuser)  # the saved signal drops the cached answers
    assert [row["kind"] for row in legal_links()] == ["cookies"]


FRAUD = {"fr": "Attention aux fraudes", "it": "Attenzione alle frodi", "en": "Beware of fraud", "ar": "احذروا الاحتيال"}


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_footer_s_fraud_link_says_the_glossary_s_word(client, seeded, phase3_open, lang):
    with translation.override(lang):
        url = reverse("pages:home")
    footer = client.get(url).content.decode().split('id="site-footer"', 1)[1]
    link = footer.split('class="site-footer__antifraud"', 1)[1].split("</a>", 1)[0]
    assert FRAUD[lang] in link and "ATTENTION AUX FRAUDES" not in link


# ---- D-11: the account pages' words -----------------------------------------------------------------------------------------
ENTRANCE = {
    "fr": ("Créer un compte", "Adresse e-mail", ("Courriel", "Création de compte")),
    "it": ("Crea un account", "Indirizzo e-mail", ("La tua password", "Cambia la tua")),
    "en": ("Create an account", "E-mail address", ("Sign Up", "sign up")),
    "ar": ("إنشاء حساب", "البريد الإلكتروني", ("الاشتراك",)),
}


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_entrance_speaks_the_glossary(client, seeded, legal_published, lang):
    create, email, never = ENTRANCE[lang]
    with translation.override(lang):
        login, signup = reverse("account_login"), reverse("account_signup")
    for url, words in ((login, (email,)), (signup, (create, email))):
        html = client.get(url).content.decode()
        main = html.split("<main", 1)[1].split("</main>", 1)[0]
        for word in words:
            assert word in main, (url, word)
        for word in never:
            assert word not in main, (url, word)


def test_every_allauth_term_is_translated_in_the_four_catalogues():
    from i18n_audit import parse_po, po_path

    from accounts.allauth_terms import ALLAUTH_TERMS

    for lang in LANGS:
        entries = {e.msgid: e for e in parse_po(po_path(lang)) if not e.obsolete}
        for msgid in ALLAUTH_TERMS:
            entry = entries.get(msgid)
            assert entry is not None and entry.msgstr.get(0), (lang, msgid)
            if lang == "fr":
                assert entry.msgstr[0] != msgid or msgid in {"Password"}, (
                    "French words, never allauth's English",
                    msgid,
                )
