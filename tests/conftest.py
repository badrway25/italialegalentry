"""
Shared pytest fixtures. Tests run against PostgreSQL (docker compose service ``db``).

Conventions for every agent:
* ``client_fr`` / ``client_ar`` — anonymous clients with the language prefix helper ``url(lang, path)``.
* ``staff_user`` / ``superuser`` / ``person_user`` — users with roles from ``accounts.roles``.
* ``legal_published`` — publishes the five legal pages with placeholder *test-only* Italian text so
  that gated forms can be exercised. Never use these strings outside tests.
* ``phase3_open`` — enables the Phase 3 gate (flag + frozen date after 2 Oct 2026).
* ``before_the_forum`` — freezes the clock in the run-up to the Rovigo Forum (banner up, registration
  open). A test about a dated state freezes the clock: on the real one it expires with the date.
* ``after_midnight_in_rome`` — freezes the clock at 00:30 Europe/Rome, when the UTC date is still
  yesterday's: what a page or a rule reads as «today» must be Rome's date, never the UTC one.
* ``whatsapp_link_set_aside(html)`` — a page as the «no external resource» guards read it: the configured
  WhatsApp channel's link set aside, nothing else (V5.19 §7; V5.20: the channel the site's settings hold).
* ``whatsapp_channel`` — the WhatsApp channel configured with Ofcom's fictional +44 7700 900123, where the site
  reads it (V5.20, option B: the owner-confirmed number is configured outside the repository, never in a test).
"""

from __future__ import annotations

import datetime as dt
import re
from zoneinfo import ZoneInfo

import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client

from accounts import roles
from core import flags
from core.models import FeatureFlag
from legal.models import LegalDocument, LegalKind, LegalStatus
from legal.services import invalidate as legal_invalidate

ROME = ZoneInfo("Europe/Rome")

#: A fixed moment of the run-up to the Rovigo Forum (2 October 2026, 15:00–18:00 Europe/Rome): the
#: homepage banner is up (``forum_banner`` runs until 2 Oct 00:00), registration is open (it closes
#: when the event ends) and Phase 3 has not begun. Every test whose subject is that state used to
#: read the real clock, and every one of them failed from 2 October 2026 on.
BEFORE_THE_FORUM = dt.datetime(2026, 9, 25, 11, 0, tzinfo=ROME)

#: Half past midnight in Rome is 22:30 the day before in UTC. For two hours every night (one in
#: winter) the two calendars disagree, and a date taken from a UTC datetime is yesterday's.
AFTER_MIDNIGHT_IN_ROME = dt.datetime(2026, 10, 5, 0, 30, tzinfo=ROME)

TEST_LEGAL_TEXT = "TESTO UFFICIALE DI PROVA — SOLO PER TEST AUTOMATICI. Paragrafo uno.\n\n## Sezione\n\nParagrafo due."


@pytest.fixture(autouse=True)
def _clear_caches():
    cache.clear()
    flags.invalidate()
    legal_invalidate()
    yield
    cache.clear()


@pytest.fixture
def url():
    def _url(lang: str, path: str = "") -> str:
        path = path.lstrip("/")
        return f"/{lang}/{path}"

    return _url


@pytest.fixture
def client_fr(client):
    return client


@pytest.fixture
def client_ar():
    return Client(HTTP_ACCEPT_LANGUAGE="ar")


@pytest.fixture
def user_factory(db):
    User = get_user_model()

    def _make(email: str, password: str = "Str0ng-Passw0rd-2026!", role: str | None = None, **extra):
        user = User.objects.create_user(email=email, password=password, **extra)
        if role:
            roles.assign_role(user, role)
        return user

    return _make


@pytest.fixture
def person_user(user_factory):
    return user_factory("person@example.test", role=roles.PERSON)


@pytest.fixture
def staff_user(user_factory):
    return user_factory("staff@example.test", role=roles.STAFF, is_staff=True)


@pytest.fixture
def superuser(db):
    return get_user_model().objects.create_superuser(email="admin@example.test", password="Str0ng-Passw0rd-2026!")


@pytest.fixture
def seeded(db):
    from django.core.management import call_command

    call_command("seed_all", verbosity=0)
    flags.invalidate()
    legal_invalidate()


@pytest.fixture
def legal_published(db, superuser):
    """Publish all five legal documents with TEST-ONLY text so gated forms open (never in prod)."""
    from legal.services import publish

    docs = []
    for kind in LegalKind.values:
        doc, _ = LegalDocument.objects.get_or_create(kind=kind)
        doc.title_it = f"Test {kind}"
        doc.body_it = TEST_LEGAL_TEXT
        doc.source_reference = "TEST FIXTURE — non è l’Allegato 1"
        doc.translations = {}  # V5.14: the seeded privacy/cookie translations (with open fields) go with the text
        doc.status = LegalStatus.DRAFT
        doc.save()
        docs.append(publish(doc, superuser))
    legal_invalidate()
    return docs


@pytest.fixture
def set_flag(db):
    def _set(key: str, enabled: bool = True, enabled_from=None, enabled_until=None):
        row, _ = FeatureFlag.objects.update_or_create(
            key=key, defaults={"enabled": enabled, "enabled_from": enabled_from, "enabled_until": enabled_until}
        )
        flags.invalidate()
        return row

    return _set


@pytest.fixture
def phase3_open(set_flag):
    from freezegun import freeze_time

    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    with freeze_time("2026-10-03 10:00:00"):
        flags.invalidate()
        yield


@pytest.fixture
def before_phase3(set_flag):
    from freezegun import freeze_time

    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    with freeze_time("2026-09-17 10:00:00"):
        flags.invalidate()
        yield


@pytest.fixture
def before_the_forum():
    """Freeze the clock at ``BEFORE_THE_FORUM`` for the whole test: banner up, registration open."""
    from freezegun import freeze_time

    with freeze_time(BEFORE_THE_FORUM):
        flags.invalidate()
        yield BEFORE_THE_FORUM


@pytest.fixture
def after_midnight_in_rome():
    """
    Freeze the clock at ``AFTER_MIDNIGHT_IN_ROME`` (5 Oct 2026, 00:30 Rome = 4 Oct, 22:30 UTC).

    Request it FIRST, before the fixtures that create rows, so that everything the test builds is
    dated at that moment rather than on the day the suite happens to run.
    """
    from freezegun import freeze_time

    with freeze_time(AFTER_MIDNIGHT_IN_ROME):
        flags.invalidate()
        yield AFTER_MIDNIGHT_IN_ROME


#: Ofcom's drama-reserved fictional UK mobile: the range 07700 900000–900999 is never assigned to a subscriber. The
#: WhatsApp channel of every test that draws one (V5.20, option B): the owner-confirmed number is configured outside
#: the repository (the environment's ILE_WHATSAPP_NUMBER, the back office) and no file of the repository writes it.
FICTIONAL_WHATSAPP_NUMBER = "+44 7700 900123"


@pytest.fixture
def whatsapp_channel(db, settings):
    """
    The WhatsApp channel, configured with FICTIONAL_WHATSAPP_NUMBER where the site reads it: the settings' value (the
    environment's ILE_WHATSAPP_NUMBER: the default of a new settings row, and the fallback before migrations) and the
    site's settings row (the back office) — whatever the machine's own environment holds. Returns core.contact's
    channel (digits, label, tel_url, url).
    """
    from core.contact import whatsapp
    from core.models import SiteSettings

    settings.ILE = {**settings.ILE, "WHATSAPP_NUMBER": FICTIONAL_WHATSAPP_NUMBER}
    row = SiteSettings.load()
    row.whatsapp_number = FICTIONAL_WHATSAPP_NUMBER
    row.save()
    return whatsapp(FICTIONAL_WHATSAPP_NUMBER)


def whatsapp_link_set_aside(html: str) -> str:
    """
    A page as the guards that forbid an external resource read it. V5.19 §7, the owner's order (DL54-176): the
    WhatsApp channel's own wa.me URL is the one outbound link a public page draws (the contact page, the footer and the
    phone's sheet). V5.20: the URL is the CONFIGURED channel's — the site's settings row, read as the context processor
    reads it (``core.contact.public_channels(SiteSettings.load())``), never a number written here; nothing configured,
    nothing is set aside. Only as a link: each ``<a href>`` to exactly that URL is set aside, so the same URL as a
    source, a srcset, a meta content or a form action, and every other external URL, still fail the guard — the rule
    of tests/compliance/test_public_pages.py since the v519-k merge, given to the apps' guards at the v518g merge.
    """
    from core.contact import public_channels
    from core.models import SiteSettings

    whatsapp = public_channels(SiteSettings.load())["whatsapp"]
    if not whatsapp:
        return html
    return re.sub(rf'(<a\b[^>]*?\bhref="){re.escape(whatsapp.url)}"', r'\g<1>#whatsapp"', html)
