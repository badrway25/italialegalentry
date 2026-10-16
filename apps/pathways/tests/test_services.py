import datetime as dt

import pytest
from django.conf import settings
from django.test import RequestFactory
from django.utils import translation
from freezegun import freeze_time

from cms import locked_content
from cms.models import PublicationStatus, TranslationStatus
from core import flags
from pathways import services
from pathways.models import (
    GENERIC_AUTHORITY_NAMES,
    PATHWAY_KEYS,
    Pathway,
    PathwayDocument,
    PathwayStep,
    PathwayStepTranslation,
    PathwayWarning,
)
from pathways.seeds import GENERIC_STEPS_FR, seed_pathways

pytestmark = pytest.mark.django_db


# ---- seed -----------------------------------------------------------------------------------


def test_seed_creates_eight_scheduled_pathways_with_skeleton(pathways_seeded):
    rows = Pathway.objects.ordered()
    assert [p.key for p in rows] == list(PATHWAY_KEYS)
    assert [p.order for p in rows] == list(range(1, 9))
    for p in rows:
        assert p.status == PublicationStatus.SCHEDULED
        assert p.publish_at == settings.ILE["PHASE3_DATE"]  # midnight Europe/Rome, 2 Oct 2026
        assert p.locked is True
        assert p.icon
        assert p.eligibility_context_fr == ""  # nothing invented
        assert list(p.steps.values_list("title_fr", flat=True)) == list(GENERIC_STEPS_FR)
        assert p.steps.filter(pending_legal_review=False).count() == 0
        assert p.documents.count() == 0
        assert p.warnings.count() == 0


def test_seed_authorities_are_generic_names_without_urls(pathways_seeded):
    for p in Pathway.objects.all():
        assert p.authorities, p.key
        for item in p.authorities:
            assert item["name"] in GENERIC_AUTHORITY_NAMES, item
            assert item["url"] == ""
    assert any(
        a["name"] == "Sportello Unico per l’Immigrazione" for a in Pathway.objects.get(key="salaried_work").authorities
    )
    assert all(
        a["name"] != "Sportello Unico per l’Immigrazione"
        for a in Pathway.objects.get(key="training_in_origin_country").authorities
    )


def test_seed_is_idempotent_and_respects_editorial_changes(pathways_seeded):
    p = Pathway.objects.get(key="salaried_work")
    p.icon = "custom-icon"
    p.eligibility_context_fr = "Texte éditorial vérifié."
    p.status = PublicationStatus.PUBLISHED
    p.authorities = [{"name": "Questura", "url": "https://example.invalid/"}]
    p.save()
    p.steps.filter(order=5).delete()
    before_versions = dict(Pathway.objects.values_list("key", "version"))

    result = seed_pathways()
    assert "0 pathway(s) created" in result
    assert "0 skeleton step(s) created" in result

    p.refresh_from_db()
    assert p.icon == "custom-icon"
    assert p.eligibility_context_fr == "Texte éditorial vérifié."
    assert p.status == PublicationStatus.PUBLISHED
    assert p.authorities == [{"name": "Questura", "url": "https://example.invalid/"}]
    assert p.steps.count() == 4  # an editor's deletion is not undone
    assert dict(Pathway.objects.values_list("key", "version")) == before_versions
    assert Pathway.objects.count() == 8


def test_seed_recreates_skeleton_only_when_no_step_exists(pathways_seeded):
    p = Pathway.objects.get(key="scientific_research")
    p.steps.all().delete()
    seed_pathways()
    assert p.steps.count() == len(GENERIC_STEPS_FR)


def test_seed_realigns_drifted_order(pathways_seeded):
    a = Pathway.objects.get(key="salaried_work")
    b = Pathway.objects.get(key="skilled_work_eu_blue_card")
    a.order, b.order = 100, 101
    a.save(update_fields=["order"])
    b.save(update_fields=["order"])
    result = seed_pathways()
    assert "2 order(s) realigned" in result
    a.refresh_from_db()
    b.refresh_from_db()
    assert (a.order, b.order) == (1, 2)


# ---- index entries --------------------------------------------------------------------------


def test_index_entries_always_eight_in_locked_order_even_without_rows():
    entries = services.index_entries()
    assert [e.key for e in entries] == list(PATHWAY_KEYS)
    locked = locked_content.get("p3.persons.pathways", "fr")[0]
    for entry, prescribed in zip(entries, locked, strict=True):
        assert entry.title == prescribed["title"]
        assert entry.description == prescribed["description"]
        assert entry.url == ""
        assert entry.is_live is False
        assert entry.icon  # default icon


def test_index_entries_link_only_live_pathways(pathways_seeded, set_flag):
    # A pathway page answers 200 only when it is live AND the Phase 3 gate is open (flag + date):
    # the index links it only then (core.links.public_url — never link to a 404).
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    with freeze_time("2026-10-03 12:00:00"), translation.override("fr"):
        flags.invalidate()
        entries = services.index_entries()
        assert all(e.is_live for e in entries)
        assert entries[0].url == "/fr/parcours/salaried_work/"
    with freeze_time("2026-09-20 12:00:00"):
        flags.invalidate()
        entries = services.index_entries()
        assert not any(e.is_live for e in entries)
        assert all(e.url == "" for e in entries)


# ---- glossary association -------------------------------------------------------------------


def test_glossary_links_only_reference_locked_terms():
    known = {t["key"] for t in locked_content.get("p3.glossary.terms", "fr")[0]}
    for key in PATHWAY_KEYS:
        links = services.glossary_links(key)
        slugs = [link["slug"] for link in links]
        assert set(slugs) <= known
        assert slugs[:3] == list(services.GENERAL_GLOSSARY_TERMS)
        assert len(slugs) == len(set(slugs))
        for link in links:
            # "" while the glossary app is not routed yet (safe_url), else its permalink
            assert link["url"] == "" or link["url"].endswith(f"/{link['slug']}/")
    for key, extra in services.GLOSSARY_TERMS_BY_PATHWAY.items():
        assert key in PATHWAY_KEYS
        assert set(extra) <= known


def test_family_reunification_links_its_own_term():
    slugs = [link["slug"] for link in services.glossary_links("family_reunification")]
    assert "ricongiungimento_familiare" in slugs
    assert "carta_blu_ue" not in slugs


# ---- public rendering rules -----------------------------------------------------------------


def _pathway():
    return Pathway.objects.create(key="salaried_work", order=1, status=PublicationStatus.PUBLISHED)


def test_pending_step_exposes_heading_only():
    p = _pathway()
    PathwayStep.objects.create(
        pathway=p, order=2, title_fr="Préparer", text_fr="Détail non vérifié", pending_legal_review=True
    )
    PathwayStep.objects.create(
        pathway=p, order=1, title_fr="S’orienter", text_fr="Détail vérifié", pending_legal_review=False
    )
    steps = services.public_steps(p, "fr")
    assert [s.order for s in steps] == [1, 2]
    assert steps[0].body == "Détail vérifié"
    assert steps[1].heading == "Préparer"
    assert steps[1].body == ""
    assert steps[1].pending is True


def test_published_translation_is_used_and_draft_ignored():
    p = _pathway()
    step = PathwayStep.objects.create(
        pathway=p, order=1, title_fr="S’orienter", text_fr="Texte FR", pending_legal_review=False
    )
    PathwayStepTranslation.objects.create(
        master=step, language="it", title="Orientarsi", text="Testo IT", status=TranslationStatus.DRAFT
    )
    items = services.public_steps(p, "it")
    assert items[0].heading == "S’orienter"
    assert items[0].lang == "fr"
    tr = step.translations.get(language="it")
    tr.status = TranslationStatus.PUBLISHED
    tr.save()
    items = services.public_steps(Pathway.objects.get(pk=p.pk), "it")
    assert items[0].heading == "Orientarsi"
    assert items[0].body == "Testo IT"
    assert items[0].lang == "it"


def test_pending_documents_and_warnings():
    p = _pathway()
    PathwayDocument.objects.create(pathway=p, order=1, label_fr="Passeport", note_fr="note", pending_legal_review=True)
    PathwayWarning.objects.create(pathway=p, order=1, text_fr="Avertissement non vérifié", pending_legal_review=True)
    PathwayWarning.objects.create(pathway=p, order=2, text_fr="Avertissement vérifié", pending_legal_review=False)
    docs = services.public_documents(p, "fr")
    assert docs[0].heading == "Passeport" and docs[0].body == ""
    warnings = services.public_warnings(p, "fr")
    assert [w.body for w in warnings] == ["Avertissement vérifié"]


def test_authorities_drop_insecure_urls_and_blank_names():
    p = _pathway()
    p.authorities = [
        {"name": "Questura", "url": "http://insecure.invalid/"},
        {"name": " ", "url": ""},
        {"name": "Prefettura", "url": "https://example.invalid/", "lang": "it"},
        "garbage",
    ]
    # `lang` tells the template which language the name is written in (I18N-08): an editor may set it,
    # otherwise the content source language applies.
    # `host`: where a link leads, shown beside it (design V5.4 D26: an authority link's host made visible).
    assert services.authorities(p) == [
        {"name": "Questura", "url": "", "lang": "fr", "host": ""},
        {"name": "Prefettura", "url": "https://example.invalid/", "lang": "it", "host": "example.invalid"},
    ]


def test_detail_context_shape():
    p = _pathway()
    with translation.override("fr"):
        ctx = services.detail_context(p)
    assert ctx.title == "Travail salarié"
    assert [s["id"] for s in ctx.sections] == [
        "apercu",
        "etapes",
        "documentation",
        "autorites",
        "avertissements",
        "ressources",
        "orientation",
    ]
    assert ctx.is_training_in_origin_country is False
    assert ctx.eligibility == ""


def test_diploma_steps_are_headings_only_and_pending():
    steps = services.diploma_steps()
    assert len(steps) == 5
    assert all(s["pending"] for s in steps)
    assert [s["id"] for s in steps] == ["documentation", "traductions", "legalisation", "declaration", "procedures"]
    assert steps[2]["glossary"][0]["slug"] == "legalizzazione_apostille"


# ---- gate / preview -------------------------------------------------------------------------


def test_can_preview_requires_staff_and_flag(staff_user, person_user):
    rf = RequestFactory()
    anon = rf.get("/fr/parcours/?preview=1")
    anon.user = type("Anon", (), {"is_authenticated": False, "is_staff": False})()
    assert services.can_preview(anon) is False
    req = rf.get("/fr/parcours/?preview=1")
    req.user = person_user
    assert services.can_preview(req) is False
    req.user = staff_user
    assert services.can_preview(req) is True
    req2 = rf.get("/fr/parcours/")
    req2.user = staff_user
    assert services.can_preview(req2) is False


def test_gated_pages_visible(before_phase3, staff_user):
    rf = RequestFactory()
    req = rf.get("/fr/parcours/")
    req.user = staff_user
    assert services.gated_pages_visible(req) == (False, False)
    req = rf.get("/fr/parcours/?preview=1")
    req.user = staff_user
    assert services.gated_pages_visible(req) == (True, True)


def test_related_links_return_own_urls_and_empty_for_missing_apps(set_flag):
    with translation.override("fr"):
        closed = services.related_links()
    assert closed["index"] == "/fr/parcours/"
    assert closed["training"] == "" and closed["diplomas"] == "", "gated pages are never linked while closed"
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    with freeze_time("2026-10-03 12:00:00"), translation.override("fr"):
        flags.invalidate()
        links = services.related_links()
    assert links["index"] == "/fr/parcours/"
    assert links["training"] == "/fr/formation/"
    assert links["diplomas"] == "/fr/diplomes-et-titres/"
    for name in ("orientation", "living", "antifraud", "faq", "glossary"):
        assert isinstance(links[name], str)
