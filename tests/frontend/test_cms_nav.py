"""cms_nav template tags: menu tree from CMS rows or the static fallback, gates, brand tags."""

from __future__ import annotations

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
    assert "data-nav-item" in html
    assert 'aria-controls="nav-main-' in html
    assert 'class="main-nav__sublink" href="/fr/privacy-policy/" aria-current="page"' in html
    assert "Ouvrir le sous-menu « Projet »" in html
