"""
V5.12 lane D, wave W1 — terminology, the person's own words, the footer's phase, the Academy's demonstration gate and
the owner's acceptance labels (docs/design-v5/QA/v512/d-w1/NOTES.md; Director's decisions §8, §9).

* D-01 a person is never told that their role is «Personne / Persona / Person»: the rail's foot, the dashboard's account
  strip and the profile name the account by its space, «Espace Personnes» (accounts.roles.AUDIENCE_SPACE_LABELS); the
  account button shows the full name, never its first word; the profile's «Rôles» row is the back office's.
* D-07 the documents section has one name: «Mes documents / I miei documenti / My documents / وثائقي».
* D-14 the person reads «Vous» on their own next action, a step of the journey instead of «Brouillon», and nothing of
  the antivirus scan unless the file is blocked.
* D-17 the public footer says the project's phase, never a release number.
* D-18 the French catalogue holds no Italian text, whatever its length.
* D-06 the Academy's invented catalogue is demonstration data: never seeded where demonstration data is off.
* D-02 / D-03 the preview speaks the owner's acceptance language, and its data reads as a product's.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
from django.test import override_settings
from django.urls import reverse
from django.utils import translation

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps"))
sys.path.insert(0, str(ROOT / "scripts"))

from accounts import roles  # noqa: E402
from accounts.models import AccountType  # noqa: E402
from core import clock  # noqa: E402

LANGS = ("fr", "it", "en", "ar")
#: The binding glossary's space name (docs/I18N_RTL.md §5), per language.
SPACE_PERSON = {"fr": "Espace Personnes", "it": "Area Persone", "en": "Individuals Area", "ar": "فضاء الأفراد"}
#: The role word a person must never be shown as who they are.
ROLE_WORD = {"fr": "Personne", "it": "Persona", "en": "Person", "ar": "شخص"}
DOCUMENTS = {"fr": "Mes documents", "it": "I miei documenti", "en": "My documents", "ar": "وثائقي"}
PHASE_3 = {"fr": "Phase 3", "it": "Fase 3", "en": "Phase 3", "ar": "المرحلة 3"}


@pytest.fixture(autouse=True)
def _private_root(settings, tmp_path):
    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    settings.MEDIA_ROOT = tmp_path / "media"


@pytest.fixture
def person(user_factory):
    return user_factory(
        "d-w1.person@example.test",
        role=roles.PERSON,
        full_name="Samira El Amrani",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.fixture
def case(person):
    from cases.models import CasePurpose
    from cases.services import open_case

    return open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")


def _piece(case, code, *, actor="person"):
    from documents import services
    from documents.models import AccessClass

    return services.declare_requirement(
        case, code=code, title=f"Pièce {code}", responsible_actor=actor, access_class=AccessClass.CASE
    )


# ---- D-01: the space's name, never the role word ---------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_a_person_is_named_by_the_space_never_by_the_role_word(person, lang):
    from portal import services

    with translation.override(lang):
        plate = services.shell_space(person)
        assert plate["who"] == SPACE_PERSON[lang]
        assert roles.space_label(person) == SPACE_PERSON[lang]
        assert plate["who"] != str(roles.ROLE_LABELS[roles.PERSON])


@pytest.mark.django_db
def test_the_space_label_follows_the_role_then_the_type_and_the_team_first(user_factory):
    typed_company = user_factory("d-w1.typed@example.test", role=roles.PERSON, account_type="company")
    assert roles.space_label(typed_company) == "Espace Personnes", "a role says more than the type"
    assert roles.space_label(user_factory("d-w1.co@example.test", account_type="company")) == "Entreprise"
    assert roles.space_label(user_factory("d-w1.inst@example.test", account_type="institution")) == "Institution"
    operator = user_factory("d-w1.op@example.test", role=roles.OPERATOR)
    assert roles.audience_role(operator) == roles.STAFF and roles.space_label(operator) == "Équipe du projet"
    staff = user_factory("d-w1.staff@example.test", is_staff=True)
    assert roles.is_project_team(staff) and not roles.is_project_team(typed_company)
    assert roles.space_label(object()) == "Espace Personnes", "a stranger, without a query"


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_console_shows_the_space_and_the_full_name(client, seeded, person, lang):
    client.force_login(person)
    with translation.override(lang):
        url = reverse("portal:dashboard")
    html = client.get(url).content.decode()
    roles_shown = re.findall(r'<span class="rail__who-role">([^<]+)</span>', html)
    assert roles_shown and set(roles_shown) == {SPACE_PERSON[lang]}, roles_shown
    assert re.findall(r'<span class="account-menu__name">([^<]+)</span>', html) == ["Samira El Amrani"], (
        "the full name, never the first word only"
    )
    assert f"<span>{SPACE_PERSON[lang]}</span>" in html.split('class="db-account__who"', 1)[1].split("</p>", 1)[0], (
        "the dashboard's account strip names the space, never the account type («Entreprise» on a person)"
    )


MY_ACCOUNT = {"fr": "Mon compte", "it": "Il mio account", "en": "My account", "ar": "حسابي"}


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_an_account_without_a_name_is_my_account_never_its_e_mail_address(client, seeded, user_factory, lang):
    """Review fix W1: ``get_full_name`` falls back to the e-mail address; the account button and the rail say
    «Mon compte» instead."""
    nameless = user_factory(
        "d-w1.nameless@example.test",
        role=roles.PERSON,
        full_name="",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )
    client.force_login(nameless)
    with translation.override(lang):
        url = reverse("portal:dashboard")
    html = client.get(url).content.decode()
    assert re.findall(r'<span class="account-menu__name">([^<]+)</span>', html) == [MY_ACCOUNT[lang]]
    assert re.findall(r'<span class="rail__who-name" dir="auto">([^<]+)</span>', html) == [MY_ACCOUNT[lang]] * len(
        re.findall(r'class="rail__who-name"', html)
    )
    for part in html.split('class="account-menu__summary"')[1:] + html.split('class="rail__who"')[1:]:
        assert "d-w1.nameless@example.test" not in part.split("</button>", 1)[0].split("</a>", 1)[0]


@pytest.mark.django_db
def test_the_profile_keeps_the_roles_row_for_the_back_office_only(client, seeded, person, user_factory):
    client.force_login(person)
    response = client.get(reverse("accounts:profile"))
    assert response.context["roles"] == [] and response.context["space_label"] == "Espace Personnes"
    assert "<dt>Rôles</dt>" not in response.content.decode()
    operator = user_factory("d-w1.operator@example.test", role=roles.OPERATOR)
    client.force_login(operator)
    response = client.get(reverse("accounts:profile"))
    assert response.context["roles"] == ["Opérateur"], "the back office keeps its own vocabulary"


# ---- D-07: one name for the documents section ------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_documents_section_has_one_name_in_every_language(client, seeded, person, lang):
    client.force_login(person)
    with translation.override(lang):
        url = reverse("portal:documents")
    html = client.get(url).content.decode()
    titles = re.findall(r'<h1 class="ws-head__title">([^<]+)</h1>', html)
    assert titles == [DOCUMENTS[lang]], titles
    assert f"<title>{DOCUMENTS[lang]}" in html


def test_no_template_names_the_documents_section_mes_pieces():
    for path in ("templates/portal/documents.html", "templates/documents/index.html"):
        text = (ROOT / path).read_text(encoding="utf-8")
        assert '{% translate "Mes pièces" %}' not in text, path
    assert '_("Mes pièces")' not in (ROOT / "apps" / "documents" / "views.py").read_text(encoding="utf-8")


# ---- D-14: the person's own words ------------------------------------------------------------------------------------
@pytest.mark.django_db
def test_the_person_is_you_on_their_own_next_action_and_concerned_to_anybody_else(case, person):
    from cases.models import ResponsibleActor
    from cases.presenters import responsible_label
    from portal import services

    _piece(case, "passeport")
    now = services.dashboard_context(person)["now"]
    assert now["responsible"]["actor"] == ResponsibleActor.PERSON and now["responsible"]["label"] == "Vous"
    assert responsible_label(ResponsibleActor.PERSON, "La personne", own=False) == "La personne concernée"
    assert responsible_label(ResponsibleActor.AUTHORITY, "L’autorité compétente", own=True) == "L’autorité compétente"
    with translation.override("it"):
        assert responsible_label(ResponsibleActor.PERSON, "", own=True) == "Lei"
        assert responsible_label(ResponsibleActor.PERSON, "", own=False) == "La persona interessata"


@pytest.mark.django_db
def test_the_documents_register_says_you_to_the_person(case, person, user_factory):
    from documents.presenters import register_rows

    _piece(case, "passeport")
    rows = register_rows(person)
    assert [row["responsible"] for row in rows] == ["Vous"]


@pytest.mark.django_db
def test_a_draft_file_reads_as_its_step_of_the_journey(case, person, client, seeded):
    from cases.models import CaseStatus

    assert case.status == CaseStatus.DRAFT
    assert case.get_person_status_display() == "Étape 1 sur 7 — Votre situation et votre objectif"
    with translation.override("it"):
        assert case.get_person_status_display().startswith("Passaggio 1 di 7 — ")
    case.status = CaseStatus.ORIENTED
    assert case.get_person_status_display() == str(case.get_status_display()), "every other state keeps its label"
    case.status = CaseStatus.DRAFT
    client.force_login(person)
    html = client.get(reverse("portal:dashboard")).content.decode()
    head = html.split('<p class="ctx__meta">', 1)[1].split("</p>", 1)[0]
    assert "Étape 1 sur 7" in head and "Brouillon" not in head
    # V5.18 lane D: the chip holds the rank, the step's title stands beside it (one line on a phone, no word cut)
    assert case.get_person_status_parts() == ("Étape 1 sur 7", "Votre situation et votre objectif")
    chip = head.split('<span class="chip__w">', 1)[1].split("</span>", 1)[0]
    assert chip == "Étape 1 sur 7"
    assert '<span class="ctx__step">Votre situation et votre objectif</span>' in head
    rows = client.get(reverse("cases:index")).content.decode()
    assert '<span class="chip__w">Étape 1 sur 7</span>' in rows
    assert '<span class="reg-row__step">Votre situation et votre objectif</span>' in rows
    case.status = CaseStatus.ORIENTED
    assert case.get_person_status_parts() == (str(case.get_status_display()), "")


@pytest.mark.django_db
def test_the_scan_says_nothing_to_the_person_unless_the_file_is_blocked(person):
    from portal.services import _person_scan_word

    for status in ("not_configured", "pending", "clean", "error"):
        assert _person_scan_word(status) == "", status
    assert _person_scan_word("infected") == "Fichier bloqué"
    template = (ROOT / "templates" / "portal" / "dashboard.html").read_text(encoding="utf-8")
    assert '{% if document.state_label %}{% chip document.scan_status "documents.ScanStatus" %}' in template


# ---- D-17: the footer's phase ----------------------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
def test_the_footer_says_the_phase_never_the_release(client, seeded, phase3_open, lang):
    from django.conf import settings

    html = client.get(f"/{lang}/").content.decode()
    footer = html.split('class="site-footer__version"', 1)[1].split("</p>", 1)[0]
    assert footer.startswith(f">{PHASE_3[lang]}"), footer
    release = settings.ILE["VERSION_LABEL"].split()[0]
    assert release not in html.split('<footer class="site-footer', 1)[1], "no release number in the public footer"


def test_the_back_office_version_field_defaults_to_nothing():
    from core.models import SiteSettings

    assert SiteSettings._meta.get_field("version_label").default == ""


# ---- D-18: no Italian in the French catalogue ------------------------------------------------------------------------
def test_the_french_catalogue_translates_the_short_italian_labels():
    import i18n_audit as audit

    french = {entry.msgid: entry.msgstr.get(0) for entry in audit.parse_po(audit.po_path("fr")) if not entry.obsolete}
    assert french["Nessun titolo dichiarato"] == "Aucun titre déclaré"
    assert french["Istruzione secondaria"] == "Enseignement secondaire"
    assert french["Post-laurea"] == "Post-universitaire"
    assert audit.unnormalised_source_msgids(audit.parse_po(audit.po_path("fr"))) == []


def test_the_audit_catches_an_italian_label_of_any_length(tmp_path, monkeypatch):
    import i18n_audit as audit

    header = (
        'msgid ""\nmsgstr ""\n"Language: {lang}\\n"\n"Content-Type: text/plain; charset=UTF-8\\n"\n'
        '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n\n'
    )
    for lang in ("it", "fr"):
        target = tmp_path / "locale" / lang / "LC_MESSAGES"
        target.mkdir(parents=True)
        (target / "django.po").write_text(
            header.format(lang=lang) + 'msgid "Post-laurea"\nmsgstr "Post-laurea"\n\nmsgid "Menu"\nmsgstr "Menu"\n',
            encoding="utf-8",
        )
    monkeypatch.setattr(audit, "LOCALE_DIR", tmp_path / "locale")
    assert audit.unnormalised_source_msgids(audit.parse_po(audit.po_path("fr"))) == ["Post-laurea"], (
        "a two-word Italian label is caught; a word spelt the same in both languages («Menu») is not"
    )


# ---- D-06: the Academy's demonstration catalogue ---------------------------------------------------------------------
@pytest.mark.django_db
def test_the_academy_catalogue_is_not_seeded_where_demonstration_data_is_off():
    from academy.models import Course, TrainingProvider
    from academy.seeds import seed_catalogue

    with override_settings(ILE_SEED_DEMONSTRATION_DATA=False):
        assert "skipped" in seed_catalogue()
    assert not Course.objects.exists() and not TrainingProvider.objects.exists()
    with override_settings(ILE_SEED_DEMONSTRATION_DATA=True):
        seed_catalogue()
    assert Course.objects.published().count() == 7
    names = set(TrainingProvider.objects.values_list("name", flat=True))
    assert not any("(exemple)" in name for name in names), names


@pytest.mark.django_db
def test_production_settings_skip_the_academy_seed():
    """Acceptance 9: under the production switch, the seed is a dry run — nothing written."""
    from academy.models import Course
    from academy.seeds import seed_catalogue
    from core.seeds import demonstration_data_allowed

    prod = (ROOT / "config" / "settings" / "prod.py").read_text(encoding="utf-8")
    assert "\nILE_SEED_DEMONSTRATION_DATA = False\n" in prod
    with override_settings(ILE_SEED_DEMONSTRATION_DATA=False, DEBUG=False):
        assert demonstration_data_allowed() is False
        seed_catalogue()
    assert Course.objects.count() == 0


@pytest.mark.django_db
def test_the_data_step_unpublishes_the_seeded_courses_where_demonstration_data_is_off():
    import importlib

    from django.apps import apps as global_apps

    from academy.models import Course, CourseStatus
    from academy.seeds import COURSES, seed_catalogue

    step = importlib.import_module("academy.migrations.0002_unpublish_demonstration_catalogue")
    assert set(step.SEEDED_COURSES) == {spec["slug"] for spec in COURSES}, "the frozen slugs are the seed's"
    with override_settings(ILE_SEED_DEMONSTRATION_DATA=True):
        seed_catalogue()
        step.unpublish_where_not_allowed(global_apps, None)
    assert Course.objects.published().count() == 7, "where demonstration data is allowed, nothing changes"
    with override_settings(ILE_SEED_DEMONSTRATION_DATA=False):
        step.unpublish_where_not_allowed(global_apps, None)
    assert Course.objects.published().count() == 0
    assert Course.objects.filter(status=CourseStatus.DRAFT).count() == len(COURSES), "unpublished, never deleted"


# ---- D-02: the owner's acceptance labels -----------------------------------------------------------------------------
def test_the_preview_speaks_the_owner_s_acceptance_language():
    from designpreview import live, personas

    assert live.STATE_LABELS == {live.STATE_V5: "Approvata in revisione", live.STATE_V4: "Da rifinire"}
    keys = {
        "qa-doc-person",
        "qa-person",
        "qa-fresh-person",
        "qa-overdue-person",
        "qa-waiting-person",
        "qa-calm-person",
        "qa-company",
        "qa-institution",
        "qa-university",
    }
    assert set(personas.ACCEPTANCE) == keys, "the four of the code and the five of the acceptance launcher"
    for key, (label, note) in personas.ACCEPTANCE.items():
        # the label says what the access IS; «dati fittizi» and the key are the metadata line's
        for word in ("Personne", "qa-", "test", "demo", "prova", "fittizi", "council", "V4", "V5"):
            assert word not in label, (key, word)
        assert note and "ruolo" not in note, key
    launcher = personas.Persona(
        "qa-institution", "Institution — Comune di Valfiorita", "nota tecnica", "portal:dashboard"
    )
    assert personas.label_of(launcher) == "Istituzione — Comune di Valfiorita"
    assert personas.metadata(launcher) == "chiave qa-institution · dati fittizi"
    with_case = personas.PERSONAS["qa-doc-person"]
    assert personas.metadata(with_case) == "chiave qa-doc-person · fascicolo EE167596D4 · dati fittizi"


def test_the_preview_names_pages_by_their_product_title():
    from designpreview import live

    titles = [page.title for pages in live.PERSONA_PAGES.values() for page in pages] + [
        page.title for page in live.PUBLIC_PAGES
    ]
    assert not [title for title in titles if "Mes pièces" in title or "/documents/" in title or "«Il varco»" in title]
    outside = live.Page("documents", "Mes pièces", "portal:documents", key="documents-portal")
    assert live.title_of(outside) == "Mes documents", "a row declared outside the repository says the product's title"


def test_the_news_is_one_sentence_with_its_details_behind_a_disclosure():
    from designpreview import live

    entry = live.news_entry(
        "2026-10-28 · v54/rc-fix · Le correzioni del candidato al rilascio v2.0.0. La validazione aveva trovato due "
        "cancelli: ora corretti."
    )
    assert entry == {
        "summary": "Le correzioni del candidato al rilascio v2.0.0.",
        "detail": "La validazione aveva trovato due cancelli: ora corretti.",
        "meta": "2026-10-28 · v54/rc-fix",
    }
    template = (ROOT / "templates" / "dev" / "designpreview" / "_changelog.html").read_text(encoding="utf-8")
    assert "<details" in template and "entry.summary" in template and "entry.meta" in template


# ---- D-03: the preview's data reads as a product's -------------------------------------------------------------------
@pytest.mark.django_db
def test_the_preview_data_clean_renames_the_fixtures_and_is_idempotent(user_factory):
    from designpreview import preview_data

    from accounts.models import Organisation
    from enquiries.models import ContactRequest

    doc = user_factory("qa-doc-person@example.test", role=roles.PERSON, full_name="Personne de test QA")
    doc.account_type = "company"
    doc.save(update_fields=["account_type"])
    user_factory("qa-company@example.test", role=roles.COMPANY, full_name="qa-company")
    org = Organisation.objects.create(name="Comune di Valfiorita (organizzazione di prova)", kind="institution")
    demo = Organisation.objects.create(name="Demo — Cantiere Adriatico S.r.l. (entreprise fictive)", kind="company")
    from consents.services import record_consent

    fields = {"language": "it", "source_path": "/it/contact/formulaire/", "message": "Message de test red team."}
    fields["consent"] = record_consent(None, "contact", email="rt@example.test", language="it")
    first = ContactRequest.objects.create(
        name="RT", email="rt@example.test", subject=preview_data.RED_TEAM_SUBJECT, **fields
    )
    second = ContactRequest.objects.create(
        name="RT", email="rt@example.test", subject=preview_data.RED_TEAM_SUBJECT, **fields
    )

    dry = preview_data.clean(apply=False)
    assert dry.changes
    doc.refresh_from_db()
    assert doc.full_name == "Personne de test QA", "a dry run changes nothing"

    report = preview_data.clean(apply=True)
    assert report.changes
    doc.refresh_from_db()
    org.refresh_from_db()
    demo.refresh_from_db()
    assert (doc.full_name, doc.account_type) == ("Samira El Amrani", "person")
    assert org.name == "Comune di Valfiorita" and demo.name == "Cantiere Adriatico S.r.l."
    first.refresh_from_db()
    assert first.subject == preview_data.CONTACT_REQUEST["subject"] and "test" not in first.message
    assert not ContactRequest.objects.filter(pk=second.pk).exists()
    assert preview_data.clean(apply=True).changes == [], "a second run changes nothing"


@pytest.mark.django_db
def test_the_dry_run_counts_the_sample_file_restorations_it_does_not_write(person):
    """Review fix W1: the dry run reported 69 changes and --apply made 80 — the restorations were not counted."""
    from designpreview import preview_data

    from documents.models import PrivateDocument
    from documents.storage import private_storage

    doc = PrivateDocument.objects.create(
        owner=person,
        original_name="Passeport.pdf",
        stored_name="missing-sample.pdf",
        content_type="application/pdf",
        size=1,
        sha256="0" * 64,
    )
    path = f"{person.pk}/{doc.stored_name}"
    dry = preview_data.clean(apply=False)
    assert f"documents.PrivateDocument#{doc.pk} sample file restored" in dry.changes
    assert not private_storage().exists(path), "a dry run writes no file"
    report = preview_data.clean(apply=True)
    assert len(report.changes) == len(dry.changes), (dry.changes, report.changes)
    assert private_storage().exists(path)
    assert preview_data.clean(apply=False).changes == []


def test_a_marker_is_removed_and_the_rest_of_the_value_kept():
    from designpreview.preview_data import unmarked

    assert unmarked("Comune di Valfiorita (organizzazione di prova)") == "Comune di Valfiorita"
    assert unmarked("Demo — Agenzia per il lavoro autorizzata (fictive)") == "Agenzia per il lavoro autorizzata"
    assert unmarked("Rendez-vous au consulat (exemple)") == "Rendez-vous au consulat"
    assert unmarked("Studio Ponte Adriatico (données de test)") == "Studio Ponte Adriatico"
    assert unmarked("Comune di Valfiorita") == "Comune di Valfiorita"


@pytest.mark.django_db
def test_the_preview_data_command_refuses_a_database_that_is_not_a_preview_s():
    from designpreview.management.commands.preview_data_clean import Command
    from django.core.management.base import CommandError

    with override_settings(ILE_DESIGN_PREVIEW_ALLOWED_DATABASES=("ile_v5",)):
        with pytest.raises(CommandError, match="not a preview database"):
            Command().handle(apply=True)
