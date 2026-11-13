"""Forum test fixtures. Everything runs on the ``ile_forum`` test database (see TEST_DATABASE_URL)."""

from __future__ import annotations

import datetime as dt
import time

import pytest
from django.conf import settings
from django.utils import timezone

from cms.models import PublicationStatus
from core import flags
from core.forms import HONEYPOT_FIELD, TIMESTAMP_FIELD
from forum import services
from forum.models import ForumEvent, ForumMode, ModeOverride, RegistrationCategory
from forum.seeds import ROVIGO_SLUG, seed_forum_event
from tests.conftest import (  # noqa: F401 — shared project fixtures (tests/conftest.py)
    _clear_caches,
    after_midnight_in_rome,
    before_phase3,
    before_the_forum,
    client_ar,
    client_fr,
    legal_published,
    person_user,
    phase3_open,
    seeded,
    set_flag,
    staff_user,
    superuser,
    url,
    user_factory,
)

ROME = settings.ROME
EVENT_END_ROME = dt.datetime(2026, 10, 2, 18, 0, tzinfo=ROME)


@pytest.fixture
def event(db) -> ForumEvent:
    """The seeded Rovigo edition (programme, speaker functions, placeholder partners)."""
    seed_forum_event()
    return ForumEvent.objects.get(slug=ROVIGO_SLUG)


@pytest.fixture
def permanent_event(event) -> ForumEvent:
    event.mode_override = ModeOverride.PERMANENT
    event.save()
    assert event.effective_mode() == ForumMode.PERMANENT
    return event


@pytest.fixture
def forms_open(legal_published):  # noqa: F811 — shared fixture injected by name
    """Gate G2 open through the official mechanism (legal pages published with test-only text)."""
    flags.invalidate()
    return True


@pytest.fixture
def registration_payload():
    def _payload(**overrides):
        data = {
            "first_name": "Amina",
            "last_name": "Test",
            "organisation": "Chambre test",
            "role": "Responsable",
            "email": "amina@example.test",
            "phone": "+39 000 000",
            "country": "Maroc",
            "category": RegistrationCategory.INSTITUTION,
            "sector_of_interest": "Formation",
            "consent": "on",
            HONEYPOT_FIELD: "",
            TIMESTAMP_FIELD: str(int(time.time()) - 30),
        }
        data.update(overrides)
        return data

    return _payload


@pytest.fixture
def published():
    def _mark(obj):
        obj.status = PublicationStatus.PUBLISHED
        obj.save()
        return obj

    return _mark


@pytest.fixture
def speaker_names_flag(set_flag):  # noqa: F811 — shared fixture injected by name
    def _enable(enabled: bool = True):
        set_flag(services.SPEAKER_NAMES_FLAG, enabled)
        flags.invalidate()

    return _enable


# =================================================================================================
# Forum Permanent — governance fixtures
# =================================================================================================
# The public Forum above is a PAGE; everything below belongs to the authenticated governance module
# (docs/platform/FORUM_GOVERNANCE.md). The fixtures build real rows through the real services, so a
# test that passes here is evidence the service path works, not merely that the model accepts a dict.
from types import SimpleNamespace  # noqa: E402

from forum import governance_services as gservices  # noqa: E402
from forum.governance import (  # noqa: E402
    Commission,
    ForumEdition,
    ForumProfile,
    ForumRole,
    MandateRole,
    ParticipantCategory,
)
from forum.governance_seeds import EDITION_KEY, seed_forum_governance  # noqa: E402

#: «Today» in the platform's calendar — Rome's, as the models read it (``timezone.localdate``) —
#: never the host's ``date.today()``, which is another date around midnight on a host that is not
#: on Rome time (a UTC CI runner, a laptop abroad).
TODAY = timezone.localdate


@pytest.fixture
def governance_open(set_flag, legal_published):  # noqa: F811 — shared fixture injected by name
    """Open gate G11 — its flag, and the legal pages it depends on (W4-D part 2, F-3). Every governance test that
    touches a ROUTE needs this, and says so."""
    set_flag(gservices.GOVERNANCE_FLAG, True)
    flags.invalidate()
    return True


@pytest.fixture
def governance_edition(db) -> ForumEdition:
    """The Rovigo 2026 edition and its five commissions, created by the real seed."""
    seed_forum_governance()
    return ForumEdition.objects.get(key=EDITION_KEY)


@pytest.fixture
def commission(governance_edition) -> Commission:
    return Commission.objects.filter(edition=governance_edition).order_by("order").first()


@pytest.fixture
def other_commission(governance_edition) -> Commission:
    return Commission.objects.filter(edition=governance_edition).order_by("order")[1]


@pytest.fixture
def forum_actor(db, django_user_model, governance_edition):
    """
    Build an account + participation profile (+ optional dated mandate) in one call.

    The mandate window is always explicit, because every interesting question in this module is a
    question about dates: a member whose mandate ran out yesterday must read nothing today.
    """

    def _make(
        email: str,
        *,
        role: str = ForumRole.PARTICIPANT,
        organisation_label: str = "",
        category: str = ParticipantCategory.INSTITUTION,
        interests: str = "",
        commission=None,
        mandate_role: str = MandateRole.MEMBER,
        valid_from=None,
        valid_until=None,
        active: bool = True,
    ):
        user = django_user_model.objects.create_user(email=email, password="Str0ng-Passw0rd-2026!")
        profile = ForumProfile.objects.create(
            user=user,
            edition=governance_edition,
            role=role,
            organisation_label=organisation_label or email.split("@")[0].replace(".", " ").title(),
            category=category,
            declared_interests=interests,
            is_active=active,
        )
        mandate = None
        if commission is not None:
            mandate = gservices.grant_mandate(
                commission,
                profile,
                role=mandate_role,
                valid_from=valid_from or TODAY() - dt.timedelta(days=30),
                valid_until=valid_until,
            )
        return SimpleNamespace(user=user, profile=profile, mandate=mandate)

    return _make


@pytest.fixture
def member(forum_actor, commission):
    return forum_actor("membre@example.test", organisation_label="Chambre de commerce test", commission=commission)


@pytest.fixture
def referent(forum_actor, commission):
    return forum_actor(
        "referent@example.test",
        organisation_label="Université test",
        category=ParticipantCategory.UNIVERSITY,
        commission=commission,
        mandate_role=MandateRole.REFERENT,
    )


@pytest.fixture
def secretariat(forum_actor):
    return forum_actor(
        "secretariat@example.test", role=ForumRole.SECRETARIAT, organisation_label="Secrétariat du Forum"
    )


@pytest.fixture
def observer(forum_actor, commission):
    return forum_actor(
        "observateur@example.test",
        role=ForumRole.OBSERVER,
        organisation_label="Institution observatrice",
        commission=commission,
        mandate_role=MandateRole.OBSERVER,
    )


@pytest.fixture
def lapsed_member(forum_actor, commission):
    """A mandate that ended yesterday. It must grant nothing at all, from today."""
    return forum_actor(
        "echu@example.test",
        organisation_label="Organisation au mandat échu",
        commission=commission,
        valid_from=TODAY() - dt.timedelta(days=200),
        valid_until=TODAY() - dt.timedelta(days=1),
    )


@pytest.fixture
def outsider(db, django_user_model):
    """An authenticated account with no Forum profile whatsoever."""
    return django_user_model.objects.create_user(email="dehors@example.test", password="Str0ng-Passw0rd-2026!")
