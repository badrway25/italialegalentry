"""
The design-system showcase: it must exist for a developer and not exist for anyone else.

The page at ``/_design/`` renders every component of the system on one screen. It is a development
tool, and a development tool that reaches production is a liability: it names internal paths, it
prints the palette, and it is the one page nobody reviews for wording. So the guarantee tested
here is not "the page looks right" — it is "the page is absent when DEBUG is off, and truthful
when DEBUG is on".

Three of these tests guard a duplication that CSP forces on us. ``style-src 'self'`` blocks inline
``style=""`` attributes, and no CSS feature turns an attribute value into a custom-property name,
so each swatch needs its own rule in ``static/css/dev/showcase.css``. A token added to the palette
without a rule would paint a blank square. The page warns about it at runtime; these tests fail
about it in CI, which is the half that works when nobody is looking.
"""

from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

import pytest
from django.test import override_settings
from django.urls import clear_url_caches

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from cms.forbidden import scan  # noqa: E402
from core import dev  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SHOWCASE_CSS = ROOT / "static" / "css" / "dev" / "showcase.css"
TOKENS_CSS = ROOT / "static" / "css" / "v2" / "tokens.css"

ALL_COLOUR_TOKENS = [name for _, _, names in dev.COLOUR_GROUPS for name in names]


@pytest.fixture
def debug_urlconf():
    """
    Re-import the root URLconf with DEBUG on, so the showcase route is actually registered.

    ``config/urls.py`` decides at import time whether ``/_design/`` exists. The test settings run
    with DEBUG off — which is what `test_absent_without_debug` relies on — so a test that wants to
    *render* the page has to rebuild the URLconf. The fixture puts it back afterwards; without the
    restore, every later test in the process would resolve URLs against a DEBUG urlconf.
    """
    import config.urls

    with override_settings(DEBUG=True):
        clear_url_caches()
        importlib.reload(config.urls)
        yield
    clear_url_caches()
    importlib.reload(config.urls)


# --------------------------------------------------------------------------- absence


def test_absent_without_debug():
    """
    With DEBUG off the route is not registered at all — not a view that refuses, no view.

    Asserted on the URL resolver rather than through the test client: a client request for a
    missing page renders the 404 template, which reads the CMS, which needs a database. The claim
    here is about the URLconf, and it should not need one.
    """
    from django.urls import Resolver404, resolve

    with pytest.raises(Resolver404):
        resolve("/_design/")


@pytest.mark.django_db
def test_answers_404_without_debug(client):
    """And end to end, the way a visitor would meet it."""
    assert client.get("/_design/").status_code == 404


def test_view_refuses_even_if_someone_wires_it_up(rf):
    """
    Belt and braces: the view checks DEBUG itself.

    The URLconf guard is the real protection, but a URLconf is a file and files get edited. If
    somebody moves this path out of the `if settings.DEBUG:` block, the view still answers 404.
    """
    from django.http import Http404

    with pytest.raises(Http404):
        dev.design_showcase(rf.get("/_design/"))


# --------------------------------------------------------------------------- truthfulness


@pytest.mark.django_db
def test_renders_every_family_of_component(client, debug_urlconf):
    response = client.get("/_design/")
    assert response.status_code == 200
    html = response.content.decode()

    # One representative marker per component family. If an include silently stops rendering —
    # a renamed contract key, a moved partial — one of these goes to zero.
    for marker, minimum in (
        ("data-swatch=", len(ALL_COLOUR_TOKENS)),
        ("data-type=", len(dev.TYPE_SCALE)),
        ('class="badge', len(dev.BADGE_KINDS)),
        ('class="notice notice--', len(dev.NOTICE_KINDS)),
        ('class="btn ', 10),
        ("form-field", 10),
        ("<dialog", 2),
        ("account-table", 1),
        ("tabs__tab", len(dev.DEMO_TABS)),
        ("accordion__item", len(dev.DEMO_ACCORDION)),
        ("timeline__item", len(dev.DEMO_TIMELINE)),
        ("stepper__item", len(dev.DEMO_STEPS)),
        ("pagination__link", 2),
        ("card__title", 3),
        ("empty-state", 1),
        ('class="ds__icon"', len(dev.ICONS)),
    ):
        assert html.count(marker) >= minimum, f"{marker!r} appears {html.count(marker)}× (expected ≥ {minimum})"


@pytest.mark.django_db
def test_carries_no_forbidden_wording(client, debug_urlconf):
    """
    The showcase is the one page where demo copy is written freehand.

    It is not public, so the compliance suite never walks it — which is exactly why it is the
    easiest place for a forbidden formulation to be typed back in by accident and then copied
    somewhere that *is* public.
    """
    html = client.get("/_design/").content.decode()
    violations = scan(html)
    assert not violations, "; ".join(f"{v.label}: {v.excerpt}" for v in violations)


@pytest.mark.django_db
def test_uses_no_inline_style_attribute(client, debug_urlconf):
    """CSP is `style-src 'self'`: an inline style attribute is blocked, so it would be dead code."""
    html = client.get("/_design/").content.decode()
    assert not re.search(r"<[^>]+\sstyle=", html), "an inline style attribute cannot survive the CSP"


@pytest.mark.django_db
def test_no_element_id_appears_twice(client, debug_urlconf):
    """
    Rendering the same form twice on one page is how duplicate ids get made.

    ``<label for="id_email">`` binds to the FIRST element with that id, so the second copy of a
    form loses every label: no caption click, nothing announced. Chrome reported five unlabelled
    controls on this page before `auto_id` separated the two forms, and the same trap waits for
    any page that shows a form beside a preview of itself.
    """
    html = client.get("/_design/").content.decode()
    ids = re.findall(r'\sid="([^"]+)"', html)
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    assert not duplicates, "ids used more than once: " + ", ".join(duplicates)


@pytest.mark.django_db
def test_the_page_reports_no_uncovered_token(client, debug_urlconf):
    """The runtime self-check must be quiet: a visible warning means a swatch is blank."""
    html = client.get("/_design/").content.decode()
    assert "Jetons sans carré de couleur" not in html


# --------------------------------------------------------------------------- the duplication


def test_every_colour_token_has_a_swatch_rule():
    covered = dev.covered_swatches()
    missing = [name for name in ALL_COLOUR_TOKENS if name.removeprefix("--") not in covered]
    assert not missing, (
        "no [data-swatch] rule in static/css/dev/showcase.css for: "
        + ", ".join(missing)
        + " — the showcase would paint an empty square"
    )


def test_every_named_token_exists_in_the_palette():
    """A renamed or retired token must not survive as a caption under a transparent square."""
    tokens = dev.read_tokens()
    assert tokens, "static/css/v2/tokens.css parsed to nothing"
    named = [
        *ALL_COLOUR_TOKENS,
        *(token for token, _, _ in dev.TYPE_SCALE),
        *(token for token, _ in dev.MOTION),
    ]
    missing = [name for name in named if name not in tokens]
    assert not missing, "core.dev names tokens that tokens.css no longer declares: " + ", ".join(missing)


def test_no_swatch_rule_is_orphaned():
    """The other direction: a rule left behind after a token is retired is dead CSS."""
    declared = set(dev.read_tokens())
    orphans = sorted(slug for slug in dev.covered_swatches() if f"--{slug}" not in declared)
    assert not orphans, "static/css/dev/showcase.css paints tokens that no longer exist: " + ", ".join(orphans)
