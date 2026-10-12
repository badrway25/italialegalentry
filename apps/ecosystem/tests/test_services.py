"""Service layer: gates, presentation cuts of prescribed sentences, photography, navigation."""

from __future__ import annotations

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from cms import locked_content
from cms.models import MediaAsset, TranslationStatus
from ecosystem import services
from ecosystem.models import EcosystemSpace, EcosystemSpaceTranslation, SpaceKey

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------------
# Registry of pages and gates
# ---------------------------------------------------------------------------------------------
def test_url_contract_and_paths():
    from django.urls import reverse

    assert reverse("ecosystem:companies") == "/fr/entreprises/"
    assert reverse("ecosystem:institutions") == "/fr/institutions/"
    assert reverse("ecosystem:universities") == "/fr/universites-et-formation/"
    assert reverse("ecosystem:pilot") == "/fr/projet-pilote/"
    assert services.ungated_paths() == ["entreprises/"]
    assert services.gated_paths() == ["institutions/", "universites-et-formation/", "projet-pilote/"]


def test_public_routes_are_registered_with_their_gate():
    from core.public_routes import all_routes

    routes = {r.path: r for r in all_routes() if r.app == "ecosystem"}
    assert routes["entreprises/"].requires_gate == ""
    for path in services.gated_paths():
        assert routes[path].requires_gate == "phase3_public"
    assert len(routes) == 4


def test_companies_gate_never_depends_on_phase3(seeded, before_phase3):
    assert services.gate_open(SpaceKey.COMPANIES) is True
    for key in (SpaceKey.INSTITUTIONS, SpaceKey.UNIVERSITIES, SpaceKey.PILOT):
        assert services.gate_open(key) is False


def test_gated_spaces_open_with_phase3(seeded, phase3_open):
    assert all(services.gate_open(key) for key in SpaceKey.values)


def test_preview_requires_staff_and_explicit_parameter(staff_user, person_user):
    factory = RequestFactory()

    def visible(user, query=""):
        request = factory.get(f"/fr/institutions/{query}")
        request.user = user
        return services.page_visible(request, SpaceKey.INSTITUTIONS)

    assert visible(AnonymousUser(), "?preview=1") == (False, False)
    assert visible(person_user, "?preview=1") == (False, False)
    assert visible(staff_user) == (False, False)
    assert visible(staff_user, "?preview=1") == (True, True)


# ---------------------------------------------------------------------------------------------
# Presentation cuts never alter a word
# ---------------------------------------------------------------------------------------------
@pytest.mark.compliance
@pytest.mark.parametrize("key", ["p3.institutions.recipients", "p3.universities.intro"])
def test_split_enumeration_keeps_every_word_in_order(key):
    cut = services.enumeration(key, "fr")
    original = locked_content.text(key, "fr")
    assert cut.source.text == original, "the authoritative sentence is carried untouched"
    rebuilt = services.words(cut.label) + [w for item in cut.items for w in services.words(item)]
    assert rebuilt == services.words(original)
    rebuilt_from_label_items = [w for item in cut.label_items for w in services.words(item)]
    assert rebuilt_from_label_items == services.words(cut.label)
    for item in cut.items + cut.label_items:
        assert item in original, "each list item is a verbatim fragment of the prescribed sentence"
        assert "," not in item and ";" not in item


def test_split_enumeration_shapes():
    recipients = services.enumeration("p3.institutions.recipients", "fr")
    assert recipients.label == "Destinataires"
    assert len(recipients.items) == 6
    universities = services.enumeration("p3.universities.intro", "it")
    assert universities.source.lang_attr == "fr", "French fallback is tagged on non-French pages"
    assert universities.label_items == (
        "Universités",
        "organismes de formation",
        "instituts et centres de recherche",
    )
    assert len(universities.items) == 7


def test_split_enumeration_without_colon():
    source = services.LockedText("x", "alpha, beta ; gamma.", "fr", "")
    cut = services.split_enumeration(source)
    assert (cut.label, cut.label_items, cut.items) == ("", (), ("alpha", "beta", "gamma"))


def test_locked_text_refuses_list_keys():
    with pytest.raises(TypeError):
        services.locked_text("p3.pilot.sequence", "fr")


# ---------------------------------------------------------------------------------------------
# Editorial layer
# ---------------------------------------------------------------------------------------------
def test_editorial_note_uses_only_published_translations():
    space = EcosystemSpace.objects.create(key=SpaceKey.COMPANIES, intro_note_fr="Note en français.")
    assert services.editorial_note(None, "fr") is None
    assert services.editorial_note(space, "fr") == services.Note("Note en français.", "")
    row = EcosystemSpaceTranslation.objects.create(
        master=space, language="it", intro_note="Nota in italiano.", status=TranslationStatus.DRAFT
    )
    space = services.get_space(SpaceKey.COMPANIES, preview=True)
    assert services.editorial_note(space, "it") == services.Note("Note en français.", "fr")
    row.status = TranslationStatus.PUBLISHED
    row.save()
    space = services.get_space(SpaceKey.COMPANIES, preview=True)
    assert services.editorial_note(space, "it") == services.Note("Nota in italiano.", "")
    space.intro_note_fr = ""
    assert services.editorial_note(space, "en") is None


def test_get_space_only_returns_live_rows_unless_previewing():
    EcosystemSpace.objects.create(key=SpaceKey.COMPANIES)  # draft
    assert services.get_space(SpaceKey.COMPANIES) is None
    assert services.get_space(SpaceKey.COMPANIES, preview=True) is not None


def _curate(asset):
    """
    Give an asset the caption apparatus a curated photograph carries.

    ``photo_for`` refuses an asset that cannot fill it (art direction A §6.2), so a test of the
    IMAGE PIPELINE has to hand it a publishable asset — otherwise it is testing the refusal, which
    tests/compliance/test_figure_caption.py already does.
    """
    import datetime as dt

    asset.caption_place = "Rovigo"
    asset.caption_date = dt.date(2026, 10, 2)
    asset.caption_fr = "Séance de travail."
    asset.credit = "AGAMI"
    asset.save()
    return asset


def test_photo_uses_responsive_static_derivatives_for_curated_assets(seeded):
    space = services.get_space(SpaceKey.COMPANIES)
    _curate(space.hero_image)
    space.refresh_from_db()
    photo = services.photo_for(space, "fr")
    assert photo.src == "/static/img/photos/equipe-entreprise-1440.jpg"
    assert photo.share_image == photo.src
    assert [part.split(" ")[1] for part in photo.webp_srcset.split(", ")] == ["480w", "960w", "1440w", "1920w"]
    assert all(part.startswith("/static/img/photos/equipe-entreprise-") for part in photo.webp_srcset.split(", "))
    assert (photo.width, photo.height) == (1440, 960)
    assert photo.alt and photo.alt_lang == ""
    assert services.photo_for(space, "ar").alt_lang == "fr"


def test_photo_falls_back_to_the_stored_file_and_respects_decorative_assets():
    asset = _curate(
        MediaAsset.objects.create(
            title="Téléversée",
            file="media/2026/09/x.jpg",
            alt_fr="Alt",
            alt_it="Testo alternativo",
            width=800,
            height=600,
        )
    )
    space = EcosystemSpace.objects.create(key=SpaceKey.PILOT, hero_image=asset)
    photo = services.photo_for(space, "it")
    assert (photo.src, photo.webp_srcset, photo.width, photo.height) == ("/media/media/2026/09/x.jpg", "", 800, 600)
    assert (photo.alt, photo.alt_lang) == ("Testo alternativo", "")
    asset.is_decorative = True
    asset.save()
    assert services.photo_for(space, "it").alt == ""
    assert services.photo_for(None, "fr") is None
    space.hero_image = None
    assert services.photo_for(space, "fr") is None


def test_every_space_has_a_photo_slot_in_the_manifest():
    for spec in services.SPACES.values():
        assert services.manifest_entry_for_slot(spec.photo_slot) is not None, spec.photo_slot
    assert services.manifest_entry_for_slot("does-not-exist") is None


# ---------------------------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------------------------
def test_local_nav_before_and_after_phase3(seeded, set_flag):
    sections = [("formulaire", "Recueil des besoins")]
    items = services.local_nav(SpaceKey.COMPANIES, sections)
    assert [i["url"] for i in items] == ["/fr/entreprises/"]
    assert items[0]["current"] is True
    # ``lang`` carries the language of the label when a prescribed text is served in fallback, so an
    # Arabic page can mark a French section name. Added in Stage 2; this expectation lagged behind it.
    assert items[0]["children"] == [
        {"label": "Recueil des besoins", "url": "#formulaire", "current": False, "lang": ""}
    ]
    preview = services.local_nav(SpaceKey.PILOT, [], preview=True)
    assert [i["url"] for i in preview] == [
        "/fr/entreprises/",
        "/fr/institutions/?preview=1",
        "/fr/universites-et-formation/?preview=1",
        "/fr/projet-pilote/?preview=1",
    ]


def test_related_links_never_point_to_closed_phase3_routes(seeded, before_phase3):
    links = services.related_links()
    assert links["forum"] == "/fr/forum/"
    assert links["company_needs"] == "/fr/entreprises/recueil-des-besoins/"
    for name in ("pilot", "institutions", "universities", "training", "faq"):
        assert links[name] == "", name


def test_related_links_after_phase3(seeded, phase3_open):
    links = services.related_links()
    assert links["pilot"] == "/fr/projet-pilote/"
    assert links["training"] == "/fr/formation/"
    assert links["pathways"] == "/fr/parcours/"
    assert links["partners"] == "/fr/partenaires/"
    assert links["faq"] == "/fr/faq/"


def test_safe_reverse_returns_empty_string_for_missing_routes():
    assert services.safe_reverse("nowhere:missing") == ""


# ---------------------------------------------------------------------------------------------
# Transparency block and pilot flow
# ---------------------------------------------------------------------------------------------
def test_recruitment_guarantee_is_phase3_content(seeded, before_phase3):
    assert services.recruitment_guarantee("fr") is None


def test_recruitment_guarantee_is_the_prescribed_faq_entry(seeded, phase3_open):
    entry = next(e for e in locked_content.get("p3.faq.items", "fr")[0] if e["key"] == services.RECRUITMENT_FAQ_KEY)
    guarantee = services.recruitment_guarantee("en")
    assert (guarantee.question, guarantee.answer) == (entry["question"], entry["answer"])
    assert guarantee.lang_attr == "fr"
    assert guarantee.faq_url == "/fr/faq/#faq_recruitment_agency"


def test_pilot_flow_numbers_and_languages():
    flow = services.pilot_flow("it")
    assert [s.number for s in flow.steps] == ["01", "02", "03", "04", "05", "06", "07", "08"]
    assert [s.label for s in flow.steps] == locked_content.get("p3.pilot.sequence", "fr")[0]
    assert all(s.locked for s in flow.steps)
    assert (flow.lang_attr, flow.locked_count) == ("fr", 8)
    assert services.pilot_flow("fr").lang_attr == ""


def test_company_moments_are_three_neutral_steps():
    moments = services.company_moments()
    assert len(moments) == 3
    text = " ".join(f"{m['label']} {m['text']}" for m in moments).lower()
    for token in ("matching", "sélection", "candidat", "classement", "recrut", "garanti"):
        assert token not in text
