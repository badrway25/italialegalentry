"""
V5.24 §2–§3, §23, §30 (2 Nov 2026) — no visible stock credit anywhere on the product: the production-facing
«Pexels-visible-label check» of the final gate (FINAL_DELIVERY_V2.md §3.2 D7, lane v524-px).

The owner's words: «NO visible “Pexels”, “Photo by …”, “Source: Pexels”, “Pexels.com” under imagery in the public site
or platform, wherever the licence permits attribution-free use; provenance stays INTERNAL. An asset that legally
requires visible attribution is replaced, never hidden.» Every photograph the product serves is Pexels License (no
attribution required) or the owner's; the retired Unsplash library renders nowhere; no CC BY asset exists
(evidence/v524/IMAGERY_ATTRIBUTION.md §2–§3) — so the credit leaves `components/photo.html` and the author stays in
`static/img/v5/<family>/PROVENANCE.json` (`pages.imagery.record`, held by tests/compliance/test_imagery_v512.py).

Four checks, each a production surface: the template SOURCES (no stock word outside a template comment); the RENDERED
public site in every language, the gates open, with the five legal pages and the error pages; the RENDERED signed-in
pages of the preview's personas and of an institution's and a university's organisation space, in French and Arabic;
the slot REGISTRY (no `credit` on a rendering; licence, author and page still recorded for every slot).

What the test must NOT catch (IMAGERY_ATTRIBUTION F5): the footer's copyright line «© 2026 AGAMI …» and the glossary
term pages' legal-source field «Source» / «المصدر» are not image credits — the patterns below are the stock vocabulary
only, never a bare «Source:» or «©». A curated plate (`cms.MediaAsset`) keeps its caption apparatus and draws a byline
only when its licence demands it (`MediaAsset.attribution_required`, CC BY): that byline names a person, never a stock
platform, and is outside these patterns by construction.
"""

from __future__ import annotations

import html as html_module
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse
from django.utils import translation

from core.public_routes import all_routes, ungated_paths
from pages import imagery

pytestmark = [pytest.mark.compliance]

ROOT = Path(settings.BASE_DIR)
LANGS = [code for code, _ in settings.LANGUAGES]

#: the stock vocabulary in a template source (a template comment is not a surface)
SOURCE_WORDS = ("Pexels", "Unsplash", "Photo by", "pexels.com", "unsplash.com", "foto__credit", "creditText")
#: the stock vocabulary in a page's VISIBLE text
VISIBLE = (
    re.compile(r"\bPexels\b"),
    re.compile(r"\bUnsplash\b"),
    re.compile(r"\bPhoto by\b"),
    re.compile(r"(?:Photo|Foto|صورة)\s*[: ]\s*.{0,80}/\s*(?:Pexels|Unsplash)", re.S),
    re.compile(r"pexels\.com|unsplash\.com", re.I),
)
STOCK = re.compile(r"pexels|unsplash|photo by", re.I)
ATTRIBUTE = re.compile(r'\b(?:alt|title|aria-label|content)="([^"]*)"')
SLOT_FIGURE = re.compile(r"<figure\b[^>]*\bdata-slot=[^>]*>(.*?)</figure>", re.S)
JSON_LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
TEMPLATE_COMMENT = re.compile(r"{%\s*comment\b.*?%}.*?{%\s*endcomment\s*%}|{#.*?#}", re.S)
#: the gates whose routes MUST render here (the registry's ungated paths, Phase 3 open, the five legal texts published);
#: the other gates need a live edition or article (the Forum, the news, the partners, the virtual forum) and stay closed
#: in a seeded database — their pages are checked when they happen to answer 200
OPEN_GATES = ("", "phase3_public", "legal_pages")


def visible_text(page: str) -> str:
    """The text a visitor can read: comments, scripts, styles, templates and noscript blocks stripped, then every tag,
    then the entities resolved (as ``cms.forbidden.scan`` reads a page)."""
    page = re.sub(r"<!--.*?-->", " ", page, flags=re.S)
    page = re.sub(r"<(script|style|template|noscript)\b.*?</\1>", " ", page, flags=re.S | re.I)
    return html_module.unescape(re.sub(r"<[^>]+>", " ", page))


def assert_clean(where: str, page: str) -> None:
    text = visible_text(page)
    for pattern in VISIBLE:
        hit = pattern.search(text)
        assert hit is None, (where, pattern.pattern, text[max(0, hit.start() - 60) : hit.end() + 60] if hit else "")
    for body in SLOT_FIGURE.findall(page):
        assert "<figcaption" not in body, (where, "a stock frame (figure[data-slot]) carries a caption")
    for value in ATTRIBUTE.findall(page):
        assert not STOCK.search(value), (where, "an attribute names a stock source", value[:120])
    for script in JSON_LD.findall(page):
        assert not STOCK.search(script), (where, "a JSON-LD block names a stock source")


# ---- 1. the sources -------------------------------------------------------------------------------------------------
def _product_templates():
    dev = ROOT / "templates" / "dev"
    for folder in (ROOT / "templates", *sorted(ROOT.glob("apps/*/templates"))):
        for path in sorted(folder.rglob("*.html")):
            if dev in path.parents:
                continue  # the development specimen boards (never mounted in production) keep their data sheets
            yield path


def test_no_product_template_names_a_stock_source_outside_a_comment():
    offenders = []
    for path in _product_templates():
        source = TEMPLATE_COMMENT.sub("", path.read_bytes().decode("utf-8"))
        offenders += [(str(path.relative_to(ROOT)), word) for word in SOURCE_WORDS if word in source]
    assert not offenders, offenders


def test_the_photo_component_draws_no_caption_and_no_hidden_credit():
    """D1: the frame is the <picture> alone — no <figcaption>, no data-credit / data-author (nothing reads it; a name
    lives in one place, SECTION_SYSTEM_V2 §8); `data-slot` is the pointer to the internal record."""
    source = (ROOT / "templates" / "components" / "photo.html").read_bytes().decode("utf-8")
    markup = source.split("{% endcomment %}", 1)[1]
    assert "<figcaption" not in markup and "credit" not in markup and "author" not in markup
    assert 'data-slot="{{ p.slot.key }}"' in markup


# ---- 2. the rendered public site ------------------------------------------------------------------------------------
@pytest.mark.django_db
def test_no_public_page_shows_a_stock_credit_in_any_language(client, seeded, phase3_open, legal_published):
    from core import views as core_views

    walked = 0
    factory = RequestFactory()
    for lang in LANGS:
        for route in all_routes():
            response = client.get(f"/{lang}/{route.path}")
            if route.requires_gate in OPEN_GATES:
                assert response.status_code == 200, (lang, route.path, response.status_code)
            elif response.status_code != 200:
                continue
            assert_clean(f"/{lang}/{route.path}", response.content.decode("utf-8"))
            walked += 1
        # the error pages, drawn by core.views: the 404 through the site, the 429 and the 500 through their views
        not_found = client.get(f"/{lang}/page-inexistante-v524/")
        assert not_found.status_code == 404
        assert_clean(f"/{lang}/ 404", not_found.content.decode("utf-8"))
        with translation.override(lang):
            request = factory.get(f"/{lang}/")
            for status, view in ((429, core_views.error_429), (500, core_views.error_500)):
                response = view(request)
                assert response.status_code == status
                assert_clean(f"/{lang}/ {status}", response.content.decode("utf-8"))
    # every ungated route in every language, plus the Phase 3 and legal routes: the walk is not a no-op
    assert walked >= len(LANGS) * (len(ungated_paths()) + 1), walked


# ---- 3. the rendered platform ---------------------------------------------------------------------------------------
ORGANISATION_PAGES = (
    "portal:dashboard",
    "portal:organisation",
    "portal:requests",
    "portal:messages",
    "portal:documents",
    "portal:deadlines",
    "accounts:profile",
)


@pytest.mark.django_db
def test_no_signed_in_page_shows_a_stock_credit(client, seeded, django_user_model):
    """The preview's four personas (as tests/frontend/test_design_preview.py's `accounts` builds them: no usable
    password, signed in with force_login) over designpreview.live.PERSONA_PAGES, and an institution's and a
    university's organisation space (role + organisation + OWNER membership, through the models the acceptance seed
    uses), in French and Arabic. A page a fresh account cannot reach (another persona's case file, a closed module)
    answers something other than 200 and is skipped; the walk must still render the dashboards."""
    from designpreview import live

    from accounts import roles
    from accounts.models import Membership, MembershipRole, Organisation
    from core import clock

    def account(key: str, role: str):
        user = django_user_model.objects.create_user(
            email=f"{key}@example.test", password=None, full_name=key, terms_accepted_at=clock.now()
        )
        roles.assign_role(user, role)
        return user

    personas = {key: account(key, roles.PERSON) for key in ("qa-doc-person", "qa-person", "qa-fresh-person")}
    personas["qa-company"] = account("qa-company", roles.COMPANY)
    for kind, role in (("institution", roles.INSTITUTION), ("university", roles.UNIVERSITY)):
        user = account(f"qa-{kind}", role)
        organisation = Organisation.objects.create(
            name=f"Organizzazione di prova ({kind})", kind=kind, country="Italia", city="Rovigo"
        )
        Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
        personas[f"qa-{kind}"] = user

    rendered = 0
    dashboards = set()
    for key, user in personas.items():
        client.force_login(user)
        for lang in ("fr", "ar"):
            if key in live.PERSONA_PAGES:
                targets = [(page.slug, live.url_of(page, lang)) for page in live.PERSONA_PAGES[key]]
            else:
                with translation.override(lang):
                    targets = [(name.split(":", 1)[1], reverse(name)) for name in ORGANISATION_PAGES]
            for slug, url in targets:
                if not url:
                    continue
                response = client.get(url)
                if response.status_code != 200:
                    continue
                assert_clean(f"{key} /{lang}/ {slug}", response.content.decode("utf-8"))
                rendered += 1
                if slug == "dashboard":
                    dashboards.add((key, lang))
        client.logout()
    assert rendered >= 30, rendered
    expected = {(key, lang) for key in ("qa-doc-person", "qa-institution", "qa-university") for lang in ("fr", "ar")}
    assert expected <= dashboards, dashboards


# ---- 4. the registry ------------------------------------------------------------------------------------------------
def test_the_registry_renders_no_credit_and_keeps_every_record():
    """D2: a rendering carries no `credit`; the internal invariant — licence, author, Pexels page per slot — stays with
    test_imagery_v512.py::test_every_slot_is_licensed_and_its_author_recorded and is restated here for the gate."""
    assert not hasattr(imagery.picture("companies.hero"), "credit")
    for slot in imagery.SLOTS:
        rec = imagery.record(slot)
        assert rec["license"].startswith("Pexels License"), slot.key
        assert rec["photographer"].strip() and rec["page"].startswith("https://www.pexels.com/photo/"), slot.key
