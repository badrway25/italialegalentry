"""cms_nav template tags: menu tree from CMS rows or the static fallback, gates, brand tags."""

from __future__ import annotations

import re

import pytest
from django.template import Context, Template
from django.test import RequestFactory
from django.utils import translation

from cms.models import MenuItem, MenuLocation
from cms.templatetags import cms_nav

pytestmark = pytest.mark.django_db


def _labels(items):
    return [i.label for i in items]


def test_fallback_main_menu_hides_gated_and_unresolvable_items(seeded, before_phase3):
    items = cms_nav.build_menu(MenuLocation.MAIN, lang="fr")
    labels = _labels(items)
    assert "Institutions" not in labels  # gated by phase3_public
    assert "Universités & Formation" not in labels
    assert "Actualités" not in labels
    for item in items:
        assert item.url or item.children, item
        for child in item.children:
            assert child.url


def test_fallback_main_menu_after_phase3_only_lists_resolvable_routes(seeded, phase3_open):
    items = cms_nav.build_menu(MenuLocation.MAIN, lang="fr")
    for item in items:
        assert item.url or item.children
        for child in item.children:
            assert child.url.startswith("/fr/")


def test_rows_override_fallback_and_respect_visibility_flags_and_gates(seeded, set_flag):
    parent = MenuItem.objects.create(
        location=MenuLocation.MAIN,
        order=1,
        label_fr="Projet",
        label_it="Progetto",
        label_en="Project",
        url_name="pages:home",
    )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        parent=parent,
        order=1,
        label_fr="Privacy",
        label_it="Privacy",
        label_en="Privacy",
        url_name="legal:privacy",
    )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        parent=parent,
        order=2,
        label_fr="Caché",
        label_it="Nascosto",
        label_en="Hidden",
        url_name="legal:cookies",
        is_visible=False,
    )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        parent=parent,
        order=3,
        label_fr="Flag",
        label_it="Flag",
        label_en="Flag",
        url_name="legal:terms",
        requires_flag="virtual_forum",
    )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        parent=parent,
        order=4,
        label_fr="Gate",
        label_it="Gate",
        label_en="Gate",
        url_name="legal:notices",
        requires_gate="phase3_public",
    )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        parent=parent,
        order=5,
        label_fr="Inconnu",
        label_it="Ignoto",
        label_en="Unknown",
        url_name="nope:missing",
    )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        order=2,
        label_fr="Externe",
        label_it="Esterno",
        label_en="External",
        url="/fr/avvertenze/",
        open_in_new_tab=True,
    )

    items = cms_nav.build_menu(MenuLocation.MAIN, lang="it", path="/it/privacy-policy/")
    assert _labels(items) == ["Progetto", "Esterno"]
    assert _labels(items[0].children) == ["Privacy"]
    assert items[0].children[0].is_current is True
    assert items[0].is_current is True
    assert items[1].new_tab is True and items[1].url == "/fr/avvertenze/"

    set_flag("virtual_forum", True)
    items = cms_nav.build_menu(MenuLocation.MAIN, lang="fr")
    assert _labels(items[0].children) == ["Privacy", "Flag"]


def test_home_is_current_only_on_exact_path(seeded):
    MenuItem.objects.create(
        location=MenuLocation.MAIN, order=1, label_fr="Accueil", label_it="Home", label_en="Home", url_name="pages:home"
    )
    items = cms_nav.build_menu(MenuLocation.MAIN, lang="fr", path="/fr/privacy-policy/")
    assert items[0].is_current is False
    items = cms_nav.build_menu(MenuLocation.MAIN, lang="fr", path="/fr/")
    assert items[0].is_current is True


def test_footer_menu_fallback_and_rows(seeded):
    items = cms_nav.build_menu(MenuLocation.FOOTER_1, lang="fr")
    assert all(i.url for i in items)
    MenuItem.objects.create(
        location=MenuLocation.FOOTER_1,
        order=1,
        label_fr="Privacy",
        label_it="Privacy",
        label_en="Privacy",
        url_name="legal:privacy",
    )
    items = cms_nav.build_menu(MenuLocation.FOOTER_1, lang="fr")
    assert _labels(items) == ["Privacy"]


def test_gate_open_mapping(seeded, set_flag):
    assert cms_nav.gate_open("") is True
    assert cms_nav.gate_open("phase3_public") is False
    assert cms_nav.gate_open("public_forms") is False
    assert cms_nav.gate_open("unknown_flag_name") is False
    set_flag("unknown_flag_name", True)
    assert cms_nav.gate_open("unknown_flag_name") is True


def test_brand_tags_use_locked_registry():
    tpl = Template('{% load cms_nav %}{% brand %}|{% brand "x" %}|{% brand_words %}')
    with translation.override("fr"):
        out = tpl.render(Context({}))
    assert '<span class="brand__wordmark" translate="no" dir="ltr" lang="en">Italy Legal Entry™</span>' in out
    assert '<span class="x" translate="no" dir="ltr" lang="en">Italy Legal Entry™</span>' in out
    assert out.endswith("marque déposée")
    with translation.override("it"):
        assert Template("{% load cms_nav %}{% brand_words %}").render(Context({})) == "marchio depositato"
    with translation.override("ar"):
        assert Template("{% load cms_nav %}{% brand_words %}").render(Context({})) == ""
    assert "®" not in out


def test_site_context_rebinds_dict_when_shadowed(seeded):
    from django.contrib.sites.models import Site

    request = RequestFactory().get("/fr/")
    tpl = Template("{% load cms_nav %}{% site_context as site %}{{ site.project_name }}|{{ site.dir }}")
    with translation.override("fr"):
        out = tpl.render(Context({"request": request, "site": Site(domain="example.com", name="x")}))
    assert out == "Italy Legal Entry™|ltr"
    with translation.override("ar"):
        out = tpl.render(Context({"request": request, "site": {"project_name": "kept", "dir": "rtl"}}))
    assert out == "kept|rtl"


def test_main_menu_tag_renders_in_template(client, seeded):
    parent = MenuItem.objects.create(
        location=MenuLocation.MAIN,
        order=1,
        label_fr="Projet",
        label_it="Progetto",
        label_en="Project",
        url_name="pages:home",
    )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        parent=parent,
        order=1,
        label_fr="Privacy",
        label_it="Privacy",
        label_en="Privacy",
        url_name="legal:privacy",
    )
    html = client.get("/fr/privacy-policy/").content.decode()
    # the drawer (below 80rem): a link and a chevron toggle per section
    assert "data-nav-item" in html
    assert 'aria-controls="nav-main-' in html
    assert 'class="main-nav__sublink" href="/fr/privacy-policy/" aria-current="page"' in html
    assert "Ouvrir le sous-menu « Projet »" in html
    # «Il portico» (design V5, W2-C1): the same tree as disclosure buttons with their panels in the letterhead
    assert f'aria-controls="nav-main-{parent.id}-portico" data-portico-door aria-current="true"' in html
    assert f'id="nav-main-{parent.id}-portico" data-portico-panel' in html
    assert 'class="portico__link" href="/fr/privacy-policy/" aria-current="page"' in html


def test_portico_gives_every_door_its_panel_from_live_content(seeded, legal_published, phase3_open):
    """«Il portico» (V5.4 plan §1.12): a section leading to an audience's space is a door, drawn with the door
    card's locked gloss, its audience glyph and its photograph; a door without CMS children carries the door card's
    two live task links; the anti-fraud page is the panel's foot, not an entry; a second line exists only where a
    short live sentence does, whole; the hairline stands before the first item after the doors."""
    items = {item.label: item for item in cms_nav.build_menu(MenuLocation.MAIN, lang="fr")}
    doors = [item for item in items.values() if item.audience]
    assert [door.audience for door in doors] == ["person", "company", "institution", "university"]
    for door in doors:
        assert door.is_section and door.children and door.icon, door.label
        assert door.photo["src"].endswith("-640.webp") and " 960w" in door.photo["srcset"], door.label
        assert door.photo["width"] == 640 and door.photo["height"] == 800
        assert door.gloss and door.gloss_lang == "", door.label  # the locked gloss, in the page's language
        for child in door.children:
            assert child.url_name != cms_nav._FOOT_ROUTE
            assert len(child.description) <= cms_nav._SECOND_LINE_MAX
    assert items["Personnes"].foot_url.endswith("/attention-aux-fraudes/")
    assert [bool(c.description) for c in items["Personnes"].children] == [True, False, True, False, True, True]
    assert [c.url_name for c in items["Institutions"].children] == ["enquiries:institution_proposal", "forum:index"]
    assert [c.label for c in items["Universités & Formation"].children] == [
        "Proposer un partenariat",
        "Formation : avant le départ et après l’arrivée",
    ]
    forum, project = items["Forum Vénétie–Maroc"], items["Projet"]
    assert forum.after_doors is True and not forum.is_section and not forum.audience
    assert project.is_section and not project.photo and not project.audience
    assert project.gloss == "Le projet, son promoteur et son réseau." and project.gloss_lang == ""
    assert [c.label for c in project.children] == ["Italy Legal Entry", "AGAMI", "Réseau", "Actualités", "Contact"]
    # the pages' own standfirsts, where one is short enough (AGAMI's first sentence is longer than the limit)
    assert [bool(c.description) for c in project.children] == [True, False, True, True, True]
    assert project.children[4].description == "Une adresse unique pour toutes les demandes relatives au projet."


def test_portico_glosses_and_second_lines_carry_their_language(seeded, legal_published, phase3_open):
    """On an Arabic page a prescribed French gloss says lang="fr" (and is drawn LTR in its run), a translated
    gloss is in the page's language and says nothing, and a second line is shown only in the page's own language —
    a panel never mixes a French line into an Arabic list."""
    arabic = re.compile(r"[\u0600-\u06ff]")
    items = {item.audience or item.url_name: item for item in cms_nav.build_menu(MenuLocation.MAIN, lang="ar")}
    assert items["person"].gloss and items["person"].gloss_lang == "fr"
    assert arabic.search(items["pages:project"].gloss) and items["pages:project"].gloss_lang == ""
    lines = [c.description for item in items.values() for c in item.children if c.description]
    assert lines and all(arabic.search(line) for line in lines), lines
    # a description written in the back-office is French: it is the gloss on the French page only
    parent = MenuItem.objects.create(
        location=MenuLocation.MAIN,
        order=1,
        label_fr="Projet",
        label_it="Progetto",
        label_en="Project",
        label_ar="المشروع",
        url_name="pages:project",
        description_fr="Une phrase écrite dans le back-office.",
    )
    MenuItem.objects.create(
        location=MenuLocation.MAIN,
        parent=parent,
        order=1,
        label_fr="Contact",
        label_it="Contatto",
        label_en="Contact",
        label_ar="اتصل",
        url_name="pages:contact",
        description_fr="Écrire à l’équipe.",
    )
    fr = cms_nav.build_menu(MenuLocation.MAIN, lang="fr")[0]
    assert fr.gloss == "Une phrase écrite dans le back-office." and fr.gloss_lang == ""
    assert fr.children[0].description == "Écrire à l’équipe."
    ar = cms_nav.build_menu(MenuLocation.MAIN, lang="ar")[0]
    assert ar.gloss == "Une phrase écrite dans le back-office." and ar.gloss_lang == "fr"
    # the French back-office line never reaches the Arabic list; the destination's own live Arabic sentence does
    # (the contact page's lead, in _SECOND_LINES), as the plan's precedence says: description_<lang>, then the live line
    assert ar.children[0].description != "Écrire à l’équipe." and arabic.search(ar.children[0].description)
