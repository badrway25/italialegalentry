"""
The content pages on design V5 — «la lettura» (W3-F2; docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 2): what the
sources hold. The browser half is tests/frontend/test_content_pages_browser_w3_f2.py.

* every page of the area loads the one page sheet (static/css/dist/cms/lettura.css) and says `lettura` in its body
  class, so the partial's scoped rules reach it and nothing else;
* the partial is page-only CSS (DL54-15): imported by its entry, never by main.css, tokens only;
* the legacy rules the area retired are gone from main.css's sources (§2.3's deletion map, W3-F2's rows);
* the two template helpers: an authority link's host (D26) and a prescribed title tracked when it is in capitals;
* the review's fixes as the server renders them: a refused newsletter opens on the system's summary (M3), the news'
  filter only where it filters (m7), the legal pages' trail and their title's language (m3, A4), the newsletter's
  answers with a way on and «who can help me» (m4), a topic's glyph with its title (m10) — and the partial's rules for
  the Latin heads of the Arabic pages (M2, m8), the first legend of an enquiry form (m6) and the legal text's direction.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.template import Context, Template
from django.utils import translation

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"
PARTIAL = ROOT / "static" / "css" / "v5" / "_lettura.css"
ENTRY = ROOT / "apps" / "cms" / "static" / "cms" / "lettura.css"

#: Every page template of the area (the includes — `_item`, `_entry`, `_card`, `_newsletter`, partials — ride on them).
PAGES = [
    "faq/index.html",
    "glossary/index.html",
    "glossary/term.html",
    "partners/index.html",
    "news/index.html",
    "news/detail.html",
    "living/index.html",
    "living/topic.html",
    "living/sheet.html",
    "community/landing.html",
    "community/index.html",
    "community/calendar.html",
    "community/initiatives.html",
    "community/room.html",
    "community/discussion.html",
    "community/join.html",
    "community/post_edit.html",
    "community/report.html",
    "enquiries/contact.html",
    "enquiries/company_needs.html",
    "enquiries/collaboration_proposal.html",
    "enquiries/done.html",
    "legal/document.html",
    "consents/newsletter_confirm.html",
    "consents/newsletter_unsubscribe.html",
]


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


@pytest.mark.parametrize("name", PAGES)
def test_every_content_page_loads_the_one_page_sheet_and_carries_the_scope(name):
    source = _read(TEMPLATES / name)
    assert "{% static 'css/dist/cms/lettura.css' %}" in source, f"{name} does not load the content pages' sheet"
    body = re.search(r"{% block body_class %}(.*?){% endblock %}", source)
    assert body and "lettura" in body.group(1).split(), f"{name}: the body class does not say `lettura`"


def test_the_partial_is_page_only_css_imported_by_its_entry():
    entry = _read(ENTRY)
    assert '@import url("../css/v5/_lettura.css");' in entry, "the entry imports the partial from the collected tree"
    # W3-F1's budget pass: the components the public interior's pages share are drawn once, in the shared page,
    # imported before the partial (the review's m11; the owner's V5.8)
    assert re.findall(r'@import url\("([^"]+)"\);', entry) == ["../css/v5/_pagina.css", "../css/v5/_lettura.css"]
    assert "_lettura.css" not in _read(ROOT / "static" / "css" / "main.css"), "page-only CSS never enters main.css"
    assert (ROOT / "static" / "css" / "dist" / "cms" / "lettura.css").is_file(), "npm run build:css"


def test_the_partial_uses_tokens_only_and_logical_properties():
    css = re.sub(r"/\*.*?\*/", "", _read(PARTIAL), flags=re.S)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", css), "no literal colour"
    assert "rgba(" not in css and "rgb(" not in css and "gradient(" not in css
    # physical box properties are written as logical ones (RTL): the one exception is a logo's object-position
    physical = re.findall(r"(?<![\w-])(margin|padding|border)-(left|right|top|bottom)\s*:", css)
    assert physical == [], physical
    # every line-height on the 4 px line (RH-1): rem values are multiples of 0.25rem
    for value in re.findall(r"line-height:\s*([0-9.]+)rem", css):
        assert (float(value) * 16) % 4 == 0, value
    # every token the partial reads exists in the foundation's tokens or is declared by the partial itself
    tokens = _read(ROOT / "static" / "css" / "v5" / "tokens.css")
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", tokens + css))
    used = set(re.findall(r"var\((--[a-z0-9-]+)", css))
    assert used <= declared, sorted(used - declared)


def test_the_legacy_rules_the_area_retired_are_gone():
    components = _read(ROOT / "static" / "css" / "components.css")
    for selector in (
        ".search-form",
        ".az-index",
        ".faq-item__links",
        ".related-links__list",
        ".glossary-entry__term",
        ".legal-page",
        ".dev-placeholder",
        ".pagination__icon-prev",
    ):
        assert selector not in components, f"{selector} is still in components.css"
    for heading in ("   20. Forms", "   28. Legal page"):
        assert heading not in components
    # the pagination stays: the console's lists draw it
    assert ".pagination__link" in components


@pytest.mark.parametrize(
    ("url", "host"),
    [
        ("https://www.salute.gov.it/portale/temi/p2_4.jsp", "salute.gov.it"),
        ("http://Integrazionemigranti.gov.it/", "integrazionemigranti.gov.it"),
        ("https://portale.gov.it:8443/a?b=c", "portale.gov.it"),
        ("mailto:contact@agamieuromed.org", ""),
        ("javascript:alert(1)", ""),
        ("/fr/faq/", ""),
        ("", ""),
        (None, ""),
    ],
)
def test_an_authority_links_host_is_shown_or_nothing(url, host):
    rendered = Template("{% load lettura %}{{ url|host }}").render(Context({"url": url}))
    assert rendered == host


@pytest.mark.django_db
def test_a_prescribed_title_in_capitals_is_tracked_and_keeps_its_words():
    from cms import locked_content

    with translation.override("fr"):
        html = Template('{% load lettura %}{% locked_title "p3.news.title" %}').render(Context())
    words = locked_content.text("p3.news.title", "fr")
    assert words == words.upper()
    assert html == f'<h1 class="page-header__title page-header__title--caps">{words}</h1>'
    with translation.override("fr"):
        html = Template('{% load lettura %}{% locked_title "p1.companies.intro" %}').render(Context())
    assert "page-header__title--caps" not in html, "a sentence in lower case is not a capital run"


@pytest.mark.django_db
def test_a_prescribed_title_shown_in_french_on_another_page_says_so():
    from cms import locked_content

    with translation.override("ar"):
        html = Template('{% load lettura %}{% locked_title "p3.virtual_forum.title" %}').render(Context())
    value, effective = locked_content.get("p3.virtual_forum.title", "ar")
    if effective != "ar":
        assert f'lang="{effective}"' in html
    assert str(value) in html


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_prescribed_text_in_the_title_or_the_description_stays_text(
    client, seeded, phase3_open, legal_published, set_flag, lang
):
    """Where the Forum Virtuel's prescribed words fall back to French (the Arabic page), the `locked` tag wraps them in
    `<span lang>`: written into <title> or into the description's attribute, the markup ended the attribute and the
    words spilled onto the top of the page. They go in as text."""
    set_flag("virtual_forum", True)
    html = client.get(f"/{lang}/forum-virtuel/").content.decode()
    head = html.split("<body", 1)[0]
    assert "<span" not in head, "markup inside <title> or a <meta> attribute"
    description = re.search(r'<meta name="description" content="([^"]*)">', head)
    assert description and description.group(1).strip(), "the description is one attribute, whole"


# ---------------------------------------------------------------------------------------------- the review's fixes


def _main(html: str) -> str:
    return html.split("<main", 1)[1].split("</main>", 1)[0]


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_refused_newsletter_opens_on_the_system_s_summary(client, seeded, legal_published, set_flag, lang):
    """The review's M3, the accessibility check's A1: sent without the consent, the page the view renders again starts
    at its top — the summary inside #newsletter is what static/js/main.js focuses and scrolls to; the field keeps its
    own error; the consent's label keeps its `lang` in the summary where it is shown in French."""
    import time

    set_flag("newsletter", True)
    response = client.post(
        f"/{lang}/actualites/lettre-d-information/",
        {"email": "refus@example.test", "website_url": "", "form_started_at": str(int(time.time()) - 30)},
    )
    assert response.status_code == 200
    html = response.content.decode()
    newsletter = html.split('id="newsletter"', 1)[1].split("</section>", 1)[0]
    summary = re.search(
        r'<div class="notice notice--error form-errors" role="alert" tabindex="-1" id="form-errors">(.*?)</ul>',
        newsletter,
        re.S,
    )
    assert summary, "the summary, inside the newsletter's form"
    assert 'href="#id_consent"' in summary.group(1), "a link to the field in error"
    assert newsletter.index('id="form-errors"') < newsletter.index('name="email"'), "at the top of the form"
    assert 'aria-invalid="true"' in newsletter and 'id="id_consent_error"' in newsletter, "the field's own error"
    assert html.count('id="form-errors"') == 1 and 'class="form__errors"' not in newsletter
    from news.forms import NewsletterForm

    with translation.override(lang):
        form = NewsletterForm()
    if form.consent_is_fallback:
        assert f'<span lang="{form.consent_language}">' in summary.group(1)


@pytest.mark.django_db
def test_the_news_filter_is_drawn_only_where_it_filters(client, seeded, phase3_open):
    """The review's m7: over an empty news no filter; over a category's empty answer it stays (its way back)."""
    from news.models import NewsCategory

    main = _main(client.get("/fr/actualites/").content.decode())
    assert 'class="filter-bar"' not in main and 'class="empty-state' in main, "no filter over an empty news"
    category = NewsCategory.objects.first()
    if category is not None:
        main = _main(client.get(f"/fr/actualites/?categorie={category.slug}").content.decode())
        assert 'class="filter-bar"' in main, "a category's empty answer keeps the way back to every article"


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_legal_page_has_its_trail_and_says_its_title_s_language(client, seeded, lang):
    """The review's m3 (the trail) and the accessibility check's A4: «Privacy Policy» is the English name kept in every
    language — a run of its own in the h1, so the h1 keeps the page's direction and reading edge."""
    html = client.get(f"/{lang}/privacy-policy/").content.decode()
    crumbs = html.split('class="breadcrumbs container"', 1)[1].split("</nav>", 1)[0]
    assert 'aria-current="page"><span lang="en">Privacy Policy</span>' in crumbs
    assert '<h1 class="page-header__title"><span lang="en" dir="ltr">Privacy Policy</span></h1>' in _main(html)
    notices = client.get(f"/{lang}/note-legali/").content.decode()
    assert '<h1 class="page-header__title"><span' not in notices, "a title in the page's language is the h1's own"


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_official_legal_text_keeps_its_language_and_its_direction(client, seeded, legal_published, lang):
    html = _main(client.get(f"/{lang}/privacy-policy/").content.decode())
    title = re.search(r'<h1 class="page-header__title">(.*?)</h1>', html, re.S).group(1)
    assert title.startswith('<span lang="it" dir="ltr">') or (lang == "it" and "<span" in title), title
    css = re.sub(r"/\*.*?\*/", "", _read(PARTIAL), flags=re.S)
    assert re.search(r'\[dir="rtl"\] \.lettura \.legal-page\[lang="it"\] \.legal-page__body \{\s*direction: ltr;', css)
    assert re.search(r"\.lettura \.legal-page__meta \{\s*margin: var\(--s-6\) 0 0;", css), "the .verifica spacing"


@pytest.mark.django_db
def test_the_newsletter_s_answers_lead_on_and_say_who_can_help(client, seeded, legal_published, set_flag):
    """The review's m4: once confirmed (or unsubscribed) the page is not a dead end — the way home, one primary, and
    «who can help me», in live words."""
    import time

    from consents.models import NewsletterSubscription

    set_flag("newsletter", True)
    client.post(
        "/fr/actualites/lettre-d-information/",
        {
            "email": "answers@example.test",
            "consent": "on",
            "website_url": "",
            "form_started_at": str(int(time.time()) - 30),
        },
    )
    sub = NewsletterSubscription.objects.get(email="answers@example.test")
    client.post(f"/fr/consentements/newsletter/confirmer/{sub.confirm_token}/")
    for path in (
        f"/fr/consentements/newsletter/confirmer/{sub.confirm_token}/",
        f"/fr/consentements/newsletter/desinscription/{sub.unsubscribe_token}/",
    ):
        if "desinscription" in path:
            client.post(path)
        main = _main(client.get(path).content.decode())
        assert main.count("btn--primary") == 1 and 'href="/fr/"' in main and "Retour à l’accueil" in main, path
        assert '<p class="aiuto">' in main and "mailto:" in main, path


@pytest.mark.django_db
def test_a_topic_s_glyph_stands_with_its_title(client, seeded, phase3_open):
    """The review's m10: beside the eyebrow «Vivre en Italie» a house read as «home» for the section."""
    html = _main(client.get("/fr/vivre-en-italie/logement/").content.decode())
    h1 = re.search(r"<h1 class=\"page-header__title\">(.*?)</h1>", html, re.S).group(1)
    assert '<svg class="icon page-header__glyph" aria-hidden="true"' in h1
    eyebrow = re.search(r'<p class="page-header__eyebrow">(.*?)</p>', html, re.S).group(1)
    assert "<svg" not in eyebrow


def test_the_partial_holds_the_review_s_rules():
    css = re.sub(r"/\*.*?\*/", "", _read(PARTIAL), flags=re.S)
    # M2: every Latin head of an Arabic page ends on its cell's reading edge
    heads = re.search(
        r'\[dir="rtl"\] \.lettura :is\(\.glossary-entry__term, \.faq-item__question, \.registro__title\)'
        r':is\(\[lang="fr"\], \[lang="it"\]\) \{\s*text-align: end;',
        css,
    )
    assert heads, "the area's heads end on the reading edge"
    # m8: a head's paragraph stands on the reading edge as a box the width of its words, and reads from its own start
    lead = re.search(
        r'\.page-header, \.chapter__head\) :is\(p, div\.page-header__lead\):is\(\[lang="fr"\], \[lang="it"\]\) \{([^}]*)\}',
        css,
    )
    assert lead and "inline-size: fit-content;" in lead.group(1) and "margin-inline-start: auto;" in lead.group(1)
    # m1: the letter band is a row of equal cells, no letter left alone
    band = re.search(r"\.az-index__list \{([^}]*)\}", css).group(1)
    assert "grid-template-columns: repeat(auto-fill, minmax(var(--hit-primary), 1fr));" in band
    # m6: the first legend of an enquiry form under a chapter's title stays for assistive technology only
    legend = re.search(r"\.enquiry-form > \.form__group:first-of-type > \.form__legend \{([^}]*)\}", css).group(1)
    assert "clip-path: inset(50%);" in legend and "position: absolute;" in legend and "display: none" not in legend
    # m2: a register's title link carries the link's resting colour
    assert re.search(r"\.registro__title a \{\s*color: var\(--accent-text\);", css)
