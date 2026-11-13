"""Models, database constraints, locked rows and idempotent seeds."""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from cms import locked_content
from cms.models import MediaAsset, PublicationStatus
from ecosystem import seeds
from ecosystem.models import (
    GATE_PHASE3,
    EcosystemSpace,
    EcosystemSpaceTranslation,
    PilotStep,
    SpaceKey,
    pilot_sequence,
    required_gate,
)

pytestmark = pytest.mark.django_db


def _asset(**extra) -> MediaAsset:
    data = {"title": "Photo test", "file": "library/photos/test.webp", "alt_fr": "Texte alternatif de test"}
    return MediaAsset.objects.create(**{**data, **extra})


# ---------------------------------------------------------------------------------------------
# EcosystemSpace
# ---------------------------------------------------------------------------------------------
def test_gate_is_a_property_of_the_page_not_an_editorial_choice():
    assert required_gate(SpaceKey.COMPANIES) == ""
    for key in (SpaceKey.INSTITUTIONS, SpaceKey.UNIVERSITIES, SpaceKey.PILOT):
        assert required_gate(key) == GATE_PHASE3
    # save() re-asserts the gate whatever was submitted…
    companies = EcosystemSpace.objects.create(key=SpaceKey.COMPANIES, requires_gate=GATE_PHASE3)
    assert companies.requires_gate == ""
    pilot = EcosystemSpace.objects.create(key=SpaceKey.PILOT, requires_gate="")
    assert pilot.requires_gate == GATE_PHASE3
    # …full_clean() refuses a wrong value…
    pilot.requires_gate = ""
    with pytest.raises(ValidationError):
        pilot.full_clean()
    # …and the database refuses a raw update that would ungate Phase 3 or gate Phase 1.
    with pytest.raises(IntegrityError), transaction.atomic():
        EcosystemSpace.objects.filter(pk=pilot.pk).update(requires_gate="")
    with pytest.raises(IntegrityError), transaction.atomic():
        EcosystemSpace.objects.filter(pk=companies.pk).update(requires_gate=GATE_PHASE3)


def test_space_key_is_unique_and_constrained():
    EcosystemSpace.objects.create(key=SpaceKey.COMPANIES)
    with pytest.raises(IntegrityError), transaction.atomic():
        EcosystemSpace.objects.create(key=SpaceKey.COMPANIES)
    with pytest.raises(IntegrityError), transaction.atomic():
        EcosystemSpace.objects.create(key="recruitment")


def test_editorial_note_rejects_forbidden_formulations():
    space = EcosystemSpace(key=SpaceKey.COMPANIES, intro_note_fr="Un service de matching pour les entreprises.")
    with pytest.raises(ValidationError) as excinfo:
        space.full_clean()
    assert "intro_note_fr" in excinfo.value.message_dict
    space.intro_note_fr = "Une note éditoriale sobre."
    space.full_clean()


def test_translation_rules():
    space = EcosystemSpace.objects.create(key=SpaceKey.COMPANIES, intro_note_fr="Note.")
    french = EcosystemSpaceTranslation(master=space, language="fr", intro_note="Note.")
    with pytest.raises(ValidationError):
        french.full_clean()
    EcosystemSpaceTranslation.objects.create(master=space, language="it", intro_note="Nota.")
    with pytest.raises(IntegrityError), transaction.atomic():
        EcosystemSpaceTranslation.objects.create(master=space, language="it", intro_note="Altra nota.")
    assert space.version >= 1 and str(space)


# ---------------------------------------------------------------------------------------------
# PilotStep
# ---------------------------------------------------------------------------------------------
def test_locked_step_always_carries_the_registry_wording_and_position():
    step = PilotStep.objects.create(order=1, locked_index=1, label_fr="RECRUTEMENT", is_locked=True)
    assert step.label_fr == pilot_sequence()[0] == "BESOINS DES ENTREPRISES"
    step.label_fr = "AUTRE LIBELLÉ"
    step.order = 5
    step.is_visible = False
    step.save()
    step.refresh_from_db()
    assert (step.label_fr, step.order, step.is_visible) == ("BESOINS DES ENTREPRISES", 1, True)
    assert str(step) == "01 — BESOINS DES ENTREPRISES"


def test_additions_never_enter_the_prescribed_sequence():
    with pytest.raises(ValidationError):
        PilotStep(order=3, label_fr="ÉTAPE AJOUTÉE").full_clean()
    with pytest.raises(IntegrityError), transaction.atomic():
        PilotStep.objects.create(order=3, label_fr="ÉTAPE AJOUTÉE")
    with pytest.raises(IntegrityError), transaction.atomic():
        PilotStep.objects.create(order=9, locked_index=9, label_fr="NEUVIÈME", is_locked=True)
    addition = PilotStep(order=9, label_fr="ÉVALUATION PARTAGÉE")
    addition.full_clean()
    addition.save()
    assert addition.is_visible is False, "an addition is hidden until an editor switches it on"
    assert list(PilotStep.objects.visible_additions()) == []


def test_addition_wording_goes_through_the_forbidden_scanner():
    with pytest.raises(ValidationError) as excinfo:
        PilotStep(order=9, label_fr="MATCHING").full_clean()
    assert "label_fr" in excinfo.value.message_dict


def test_only_registry_steps_can_be_locked():
    with pytest.raises(ValidationError):
        PilotStep(order=12, locked_index=12, label_fr="X", is_locked=True).full_clean()


# ---------------------------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------------------------
def test_seed_all_creates_the_four_spaces_and_eight_steps(seeded):
    spaces = {s.key: s for s in EcosystemSpace.objects.all()}
    assert set(spaces) == set(SpaceKey.values)
    assert spaces["companies"].status == PublicationStatus.PUBLISHED
    assert spaces["companies"].requires_gate == ""
    for key in ("institutions", "universities", "pilot"):
        assert spaces[key].status == PublicationStatus.SCHEDULED
        assert spaces[key].publish_at == seeds.PHASE3_PUBLISH_AT
        assert spaces[key].requires_gate == GATE_PHASE3
    assert all(space.hero_image_id for space in spaces.values()), "each space gets a sober photograph"
    assert [s.label_fr for s in PilotStep.objects.locked()] == locked_content.get("p3.pilot.sequence", "fr")[0]
    assert PilotStep.objects.count() == 8


def test_phase3_publish_date_is_2_october_2026_rome_time():
    assert seeds.PHASE3_PUBLISH_AT.astimezone(dt.UTC) == dt.datetime(2026, 10, 1, 22, 0, tzinfo=dt.UTC)


def test_seeds_are_idempotent_and_respect_editorial_changes(seeded):
    other = _asset(title="Choix éditorial")
    space = EcosystemSpace.objects.get(key="companies")
    space.hero_image = other
    space.intro_note_fr = "Note rédigée par l’équipe."
    space.order = 99
    space.save()
    EcosystemSpace.objects.filter(key="pilot").update(hero_image=None, version=4)  # image removed on purpose
    addition = PilotStep.objects.create(order=9, label_fr="ÉVALUATION PARTAGÉE", is_visible=True)

    assert seeds.seed_spaces().startswith("0 ecosystem space(s) created, 0 photograph(s) attached")
    assert seeds.seed_pilot_steps().startswith("0 prescribed pilot step(s) created, 0 re-synchronised")

    space.refresh_from_db()
    assert (space.hero_image, space.intro_note_fr, space.order) == (other, "Note rédigée par l’équipe.", 99)
    assert EcosystemSpace.objects.get(key="pilot").hero_image is None
    addition.refresh_from_db()
    assert addition.label_fr == "ÉVALUATION PARTAGÉE" and addition.is_visible
    assert EcosystemSpace.objects.count() == 4 and PilotStep.objects.count() == 9


def test_seed_attaches_a_photograph_that_arrived_later(db):
    assert "4 ecosystem space(s) created" in seeds.seed_spaces()  # media library still empty
    assert not EcosystemSpace.objects.exclude(hero_image=None).exists()
    from cms.seeds_media import seed as seed_media

    seed_media()
    assert "4 photograph(s) attached" in seeds.seed_spaces()
    assert not EcosystemSpace.objects.filter(hero_image=None).exists()


def test_seed_resynchronises_a_drifted_locked_step(seeded):
    # The database refuses to unlock or move a prescribed step…
    with pytest.raises(IntegrityError), transaction.atomic():
        PilotStep.objects.filter(locked_index=2).update(is_locked=False, order=20)
    # …and a raw change of its wording is repaired by the next seed run.
    PilotStep.objects.filter(locked_index=2).update(label_fr="TEXTE ALTÉRÉ")
    assert "1 re-synchronised" in seeds.seed_pilot_steps()
    step = PilotStep.objects.get(locked_index=2)
    assert (step.label_fr, step.is_locked, step.order) == ("PROFILS ET COMPÉTENCES", True, 2)
