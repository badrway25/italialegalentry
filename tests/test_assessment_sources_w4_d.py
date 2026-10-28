"""
The questionnaire's assessment keeps the pathway's own sources (W4-D part 2, A1).

``cases.intake._sources_of`` read ``pathways.models.PathwaySource`` with ``order_by("order", "id")``
and ``source.title_fr`` / ``source.reference`` — fields the model never had (it has ``title``,
``url``, ``publisher``, ``retrieved_at``, ``note``). The ``FieldError`` was caught by an
``except Exception`` that only logged, so every assessment lost the pathway's sources and the log
filled with one traceback per completed questionnaire (found by the database bridge's rebuild).

The fix reads the model's own fields in the model's own order (``Meta.ordering`` = pathway, id —
the back office's inline lists them so). The public pathway pages never show these rows (the
model: «never published, traceability only»); the person's own assessment does, after the
sources of the rules in force, as ``_sources_of``'s docstring has said since the rule engine: an
outcome with no rule in force still shows no source. The assessment page's empty sentence
(«… parce qu'aucune règle en vigueur ne s'y applique») and the dashboard's note («ne s'appuie sur
aucune règle actuellement en vigueur … aucune source ne lui est donc rattachée») both rest on that
equivalence, so a no-rule outcome keeps showing them.
"""

from __future__ import annotations

import datetime as dt
import logging

import pytest

from cases.intake import reassess
from cases.models import CaseFile, ResponsibleActor
from cases.tests.test_intake import run_questionnaire
from pathways.models import Pathway, PathwaySource
from rules import services as rule_services
from rules.models import LegalRule, LegalSource, ReviewStatus, RuleEffect

pytestmark = pytest.mark.django_db

PATHWAY = "salaried_work"  # the pathway the seeded questionnaire reaches with its first options


@pytest.fixture
def person(django_user_model):
    from accounts import roles

    roles.ensure_roles()
    user = django_user_model.objects.create_user(email="sources-w4d@example.test", password="x")
    roles.assign_role(user, roles.PERSON)
    return user


@pytest.fixture
def pathway_sources(seeded):
    """Two primary sources an editor recorded on the pathway, in the order the back office lists them."""
    pathway = Pathway.objects.get(key=PATHWAY)
    first = PathwaySource.objects.create(
        pathway=pathway,
        title="Portale Integrazione Migranti — Lavoro subordinato",
        url="https://www.integrazionemigranti.gov.it/example",
        publisher="Ministero del Lavoro e delle Politiche Sociali",
        retrieved_at=dt.date(2026, 9, 30),
        note="note interne — jamais affichée",
    )
    second = PathwaySource.objects.create(pathway=pathway, title="Decreto flussi 2026 — scheda")
    return [first, second]


def _rule_in_force(django_user_model, *, condition=None) -> LegalRule:
    """A rule on the pathway, walked to ACTIVE through the whole chain by someone else than its author."""
    author = django_user_model.objects.create_user(email="sources-author@example.test", password="x")
    reviewer = django_user_model.objects.create_user(email="sources-reviewer@example.test", password="x")
    source = LegalSource.objects.create(
        key="w4d-tui-22",
        title_fr="Travail salarié",
        reference="D.Lgs. 286/1998, art. 22",
        authority="Repubblica Italiana",
        url="https://www.normattiva.it/example",
        consulted_on=dt.date(2026, 9, 21),
        consulted_by="Referente giuridico",
    )
    rule = LegalRule.objects.create(
        rule_id="R-W4D-SOURCES",
        version=1,
        pathway=PATHWAY,
        condition=condition if condition is not None else {},
        effect=RuleEffect.MISSING_REQUIREMENT,
        message_key="rules.w4d.sources",
        message_fr="Un employeur identifié en Italie.",
        requirement_fr="Proposition de contrat d’un employeur établi en Italie.",
        responsible_actor=ResponsibleActor.COMPANY,
        valid_from=dt.date(2026, 1, 1),
        created_by=author,
    )
    rule.sources.add(source)
    for target in (ReviewStatus.SOURCE_VERIFIED, ReviewStatus.LEGAL_REVIEW, ReviewStatus.APPROVED, ReviewStatus.ACTIVE):
        rule_services.transition(rule, target, actor=reviewer)
    return rule


def _intake_errors(caplog) -> list[logging.LogRecord]:
    return [r for r in caplog.records if r.name == "ile.cases" and r.levelno >= logging.ERROR]


# ---------------------------------------------------------------------------------------------
# No assessment logs a swallowed error any more
# ---------------------------------------------------------------------------------------------
def test_completing_the_questionnaire_logs_no_swallowed_error(person, pathway_sources, caplog):
    """Red before the fix: «pathway sources unavailable for salaried_work» with a FieldError, on every run."""
    caplog.set_level(logging.ERROR, logger="ile.cases")
    run_questionnaire(person)
    assert CaseFile.objects.filter(person=person).exists()
    errors = _intake_errors(caplog)
    assert not errors, [f"{r.getMessage()} — {r.exc_info[1]!r}" if r.exc_info else r.getMessage() for r in errors]


# ---------------------------------------------------------------------------------------------
# ALLOW: an outcome from rules in force carries the pathway's sources after the rules'
# ---------------------------------------------------------------------------------------------
def test_an_outcome_from_rules_in_force_carries_the_pathways_sources(
    person, pathway_sources, django_user_model, caplog
):
    caplog.set_level(logging.ERROR, logger="ile.cases")
    _rule_in_force(django_user_model)
    run_questionnaire(person)
    assessment = CaseFile.objects.get(person=person).assessments.latest("assessed_at")

    assert [a["rule_id"] for a in assessment.applied_rules] == ["R-W4D-SOURCES"]
    titles = [s["title"] for s in assessment.sources]
    assert titles == [
        "Travail salarié",  # the rule's own source first
        "Portale Integrazione Migranti — Lavoro subordinato",  # then the pathway's, in the model's order
        "Decreto flussi 2026 — scheda",
    ], titles
    first = assessment.sources[1]
    assert first["url"] == "https://www.integrazionemigranti.gov.it/example"
    assert first["authority"] == "Ministero del Lavoro e delle Politiche Sociali"
    assert first["consulted_on"] == "2026-09-30"
    # A pathway source carries no precise provision: no reference is made up for it.
    assert first["reference"] == ""
    # The editor's internal note never leaves the back office, nor who recorded the row.
    assert "note interne" not in repr(assessment.sources)
    assert not any("added_by" in s or "note" in s for s in assessment.sources)
    second = assessment.sources[2]
    assert (second["url"], second["authority"], second["consulted_on"]) == ("", "", "")
    assert not _intake_errors(caplog)


def test_the_assessment_page_shows_the_pathways_sources(person, pathway_sources, django_user_model, client):
    _rule_in_force(django_user_model)
    run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    assessment = case.assessments.latest("assessed_at")

    client.force_login(person)
    response = client.get(f"/fr/espace-reserve/dossiers/{case.reference}/pre-evaluation/{assessment.pk}/")
    assert response.status_code == 200
    html = response.content.decode()
    listed = html[html.index('<ol class="sources">') : html.index("</ol>", html.index('<ol class="sources">'))]
    assert (
        listed.index("Travail salarié")
        < listed.index("Portale Integrazione Migranti")
        < listed.index("Decreto flussi 2026")
    )
    assert 'href="https://www.integrazionemigranti.gov.it/example"' in listed
    assert "consultée le 2026-09-30" in listed
    assert "note interne" not in html


def test_a_reassessment_keeps_the_pathways_sources(person, pathway_sources, django_user_model):
    """The second path that records an assessment cites the same sources as the first."""
    from accounts.services import get_or_create_profile

    _rule_in_force(django_user_model, condition={"field": "has_job_offer", "op": "is_false"})
    profile = get_or_create_profile(person)
    profile.has_job_offer = False
    profile.save()
    run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    first = case.assessments.latest("assessed_at")
    assert [s["title"] for s in first.sources][1:] == [
        "Portale Integrazione Migranti — Lavoro subordinato",
        "Decreto flussi 2026 — scheda",
    ]

    # A second rule enters into force: the findings move, so a new assessment is recorded.
    second_source = LegalSource.objects.create(
        key="w4d-second",
        title_fr="Second texte",
        reference="D.P.R. 394/1999, art. 30",
        authority="Repubblica Italiana",
        url="https://www.normattiva.it/example-2",
        consulted_on=dt.date(2026, 9, 22),
        consulted_by="Referente giuridico",
    )
    reviewer = django_user_model.objects.get(email="sources-reviewer@example.test")
    author = django_user_model.objects.get(email="sources-author@example.test")
    rule = LegalRule.objects.create(
        rule_id="R-W4D-SECOND",
        version=1,
        pathway=PATHWAY,
        condition={},
        effect=RuleEffect.WARNING,
        message_key="rules.w4d.second",
        message_fr="Un second point.",
        valid_from=dt.date(2026, 1, 1),
        created_by=author,
    )
    rule.sources.add(second_source)
    for target in (ReviewStatus.SOURCE_VERIFIED, ReviewStatus.LEGAL_REVIEW, ReviewStatus.APPROVED, ReviewStatus.ACTIVE):
        rule_services.transition(rule, target, actor=reviewer)

    later = reassess(case)
    assert later is not None and later.pk != first.pk
    titles = [s["title"] for s in later.sources]
    assert titles[-2:] == ["Portale Integrazione Migranti — Lavoro subordinato", "Decreto flussi 2026 — scheda"], titles
    assert {"Travail salarié", "Second texte"} <= set(titles[:-2])


# ---------------------------------------------------------------------------------------------
# DENY: an outcome with no rule in force still shows no source, on both screens
# ---------------------------------------------------------------------------------------------
def test_an_outcome_with_no_rule_in_force_still_shows_no_source(person, pathway_sources, client):
    run_questionnaire(person)
    case = CaseFile.objects.get(person=person)
    assessment = case.assessments.latest("assessed_at")
    assert assessment.applied_rules == []
    assert assessment.sources == [], assessment.sources

    client.force_login(person)
    page = client.get(f"/fr/espace-reserve/dossiers/{case.reference}/pre-evaluation/{assessment.pk}/").content.decode()
    assert "Aucune source n’est rattachée à ce résultat, parce qu’aucune règle en vigueur ne s’y applique." in page
    assert "Portale Integrazione Migranti" not in page
    dashboard = client.get("/fr/espace-reserve/").content.decode()
    assert "ne s’appuie sur aucune règle actuellement en vigueur dans la plateforme" in dashboard
    assert "Portale Integrazione Migranti" not in dashboard
