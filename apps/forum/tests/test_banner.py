"""Homepage banner partial (document §2.2) — provided to the pages app, gated by forum_banner."""

from __future__ import annotations

import datetime as dt

import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory
from freezegun import freeze_time

from cms import locked_content
from core import flags
from core.context_processors import site
from forum import services
from forum.tests.conftest import ROME

pytestmark = pytest.mark.django_db


def _render(context):
    request = RequestFactory().get("/fr/")
    ctx = {"banner": context, **site(request)}
    return render_to_string("forum/partials/home_banner.html", ctx, request=request)


def test_banner_context_visible_before_2_october(event):
    with freeze_time(dt.datetime(2026, 9, 25, 12, 0, tzinfo=ROME)):
        flags.invalidate()
        ctx = services.banner_context()
    assert ctx["visible"] is True
    assert ctx["title"] == locked_content.text("p2.home.banner.title", "fr")
    assert ctx["meta"] == "Rovigo | 2 octobre 2026 | 15h00–18h00"
    assert ctx["button"] == "DÉCOUVREZ LE FORUM"
    assert ctx["url"] == "/fr/forum/"
    html = _render(ctx)
    assert 'data-banner="forum"' in html
    assert "DÉCOUVREZ LE FORUM" in html and 'href="/fr/forum/"' in html
    assert "« Institutions, entreprises, universités et professionnels" in html


def test_banner_hidden_after_2_october(event):
    with freeze_time(dt.datetime(2026, 10, 3, 0, 1, tzinfo=ROME)):
        flags.invalidate()
        ctx = services.banner_context()
    assert ctx["visible"] is False
    assert _render(ctx).strip() == ""


def test_banner_hidden_when_permanent(permanent_event):
    with freeze_time(dt.datetime(2026, 9, 25, 12, 0, tzinfo=ROME)):
        flags.invalidate()
        assert services.banner_context()["visible"] is False


def test_banner_hidden_without_event(db):
    with freeze_time(dt.datetime(2026, 9, 25, 12, 0, tzinfo=ROME)):
        flags.invalidate()
        assert services.banner_context()["visible"] is False
