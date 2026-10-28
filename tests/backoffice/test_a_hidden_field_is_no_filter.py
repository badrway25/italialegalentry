"""
A field the back office hides from an account is no filter of the list either (finding F-8, review F8R-2).

sec-f8 took off the pages what a role may not read: a newsletter subscription's two bearer tokens (from everybody), a
mail's body (from a view grant on the outbox), a questionnaire's answers (from everybody but a superuser). But a
changelist prints its count, and Django lets the query string filter on any of the model's own fields
(``ModelAdmin.lookup_allowed`` refuses only lookups across relations): ``?confirm_token__startswith=<prefix>`` answered
1 or 0, so a subscriber's token was recoverable one character at a time, with no rate limit; ``?body_text__contains=``
read a mail's body for a view grant; ``?answers_snapshot__family=`` read the answers for the administrator. Each DENY
below failed before the fix. ``core.admin_base.BaseModelAdmin.hidden_fields`` now names, per account, the fields a
screen hides: a lookup over one is refused as Django refuses any lookup it does not allow (its 400), and the search
box never reads one. The ALLOW tests hold that an account that may read the field still filters on it, and that the
lists' own filters and searches still work.

Accounts are this module's own, created with a test-only password and signed in through minted sessions
(``Client.force_login``); ``roles.ensure_roles()`` gives the roles their model permissions as the production seed does.
"""

from __future__ import annotations

import pytest
from django.contrib import admin
from django.test import RequestFactory

from accounts import roles

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Local-Only-F8R2-2026!"
BO = "/backoffice/"
SUBSCRIPTIONS = f"{BO}consents/newslettersubscription/"
OUTBOX = f"{BO}notifications/emailoutbox/"
NOTIFICATIONS = f"{BO}notifications/notification/"
SESSIONS = f"{BO}orientation/orientationsession/"
RESULTS = f"{BO}orientation/orientationresult/"
ACCOUNTS = f"{BO}accounts/user/"
MARKER = "F8R2-HIDDEN-BODY-MARKER"
ANSWER = "F8R2-HIDDEN-ANSWER"


@pytest.fixture
def cast(django_user_model):
    roles.ensure_roles()

    def make(key, role=None, **extra):
        user = django_user_model.objects.create_user(email=f"f8r2.{key}@example.test", password=PASSWORD, **extra)
        if role:
            roles.assign_role(user, role)
        return user

    return {
        "staff": make("staff", roles.STAFF, is_staff=True),
        "administrator": make("administrator", roles.ADMINISTRATOR, is_staff=True),
        "person": make("person", roles.PERSON),
        "superuser": django_user_model.objects.create_superuser(email="f8r2.super@example.test", password=PASSWORD),
    }


@pytest.fixture
def subscription(cast):
    from consents.models import ConsentPurpose, NewsletterSubscription
    from consents.services import record_consent

    consent = record_consent(None, ConsentPurpose.NEWSLETTER, "f8r2.subscriber@example.test")
    return NewsletterSubscription.objects.create(email="f8r2.subscriber@example.test", consent=consent)


@pytest.fixture
def mail(cast):
    from notifications.models import EmailOutbox

    return EmailOutbox.objects.create(
        to_email="f8r2.subscriber@example.test",
        subject="F8R2 subject",
        body_text=f"Bonjour {MARKER}",
        body_html=f"<p>Bonjour {MARKER}</p>",
    )


@pytest.fixture
def result(cast):
    from orientation.models import OrientationResult, OrientationSession, Ruleset, SessionStatus
    from orientation.seeds import seed_ruleset_v1

    seed_ruleset_v1()
    ruleset = Ruleset.objects.get(version=1)
    session = OrientationSession.objects.create(
        ruleset=ruleset,
        user=cast["person"],
        status=SessionStatus.COMPLETED,
        state={"answers": {"family": ANSWER}, "history": []},
    )
    return OrientationResult.objects.create(
        session=session, outcome=ruleset.outcomes.first(), ruleset_version=1, answers_snapshot={"family": ANSWER}
    )


def _count(client, url: str, params: dict) -> int:
    response = client.get(url, params)
    assert response.status_code == 200, (url, params, response.status_code)
    return response.context["cl"].result_count


def _refused(client, url: str, params: dict) -> bool:
    """Django's answer to a lookup it does not allow: a 400 (DisallowedModelAdminLookup), never a count."""
    return client.get(url, params).status_code == 400


# =================================================================================================
# DENY — the hidden field answers nothing through the query string
# =================================================================================================
class TestTheSubscribersTokens:
    @pytest.mark.parametrize("who", ["staff", "administrator", "superuser"])
    def test_a_token_is_no_filter_for_anybody(self, client, cast, subscription, who):
        client.force_login(cast[who])
        token = subscription.confirm_token
        for params in (
            {"confirm_token": token},
            {"confirm_token__startswith": token[:1]},
            {"confirm_token__regex": "^."},
            {"unsubscribe_token__startswith": subscription.unsubscribe_token[:1]},
            {"unsubscribe_token__isnull": "False"},
        ):
            assert _refused(client, SUBSCRIPTIONS, params), f"F8R-2: {who} filtered the subscriptions by {params}"

    def test_the_search_box_does_not_read_a_token(self, client, cast, subscription):
        client.force_login(cast["administrator"])
        assert _count(client, SUBSCRIPTIONS, {"q": subscription.confirm_token}) == 0


class TestTheMailBodies:
    def test_a_body_is_no_filter_for_a_view_grant(self, client, cast, mail):
        client.force_login(cast["staff"])
        assert MARKER not in client.get(f"{OUTBOX}{mail.pk}/change/").content.decode("utf-8")
        for params in ({"body_text__contains": MARKER}, {"body_html__icontains": MARKER}, {"body_text__regex": "^B"}):
            assert _refused(client, OUTBOX, params), f"F8R-2: a view grant filtered the outbox by {params}"
        assert _count(client, OUTBOX, {"q": MARKER}) == 0, "the search box reads no body"

    def test_a_body_is_no_filter_across_a_notification(self, client, cast, mail):
        client.force_login(cast["staff"])
        assert _refused(client, NOTIFICATIONS, {"outbox__body_text__contains": MARKER})


class TestTheAnswers:
    def test_an_answer_is_no_filter_for_the_administrator(self, client, cast, result):
        client.force_login(cast["administrator"])
        assert ANSWER not in client.get(f"{RESULTS}{result.pk}/change/").content.decode("utf-8")
        for params in ({"answers_snapshot__family": ANSWER}, {"answers_snapshot__has_key": "family"}):
            assert _refused(client, RESULTS, params), f"F8R-2: the administrator filtered the results by {params}"
        assert _refused(client, SESSIONS, {"state__answers__family": ANSWER})
        assert _refused(client, RESULTS, {"session__state__answers__family": ANSWER})


class TestThePasswordHash:
    def test_the_administrator_filters_no_account_by_its_password(self, client, cast):
        """Django's own UserAdmin refuses it; held here because the accounts screen is the administrator's."""
        client.force_login(cast["administrator"])
        for params in ({"password__startswith": "pbkdf2"}, {"password__regex": "^p"}):
            assert _refused(client, ACCOUNTS, params), params


class TestEveryScreen:
    @pytest.mark.parametrize("who", ["staff", "administrator", "superuser"])
    def test_a_field_a_screen_hides_is_never_a_filter_nor_a_search_nor_a_column(self, cast, who):
        """Over the whole registry: whatever ``hidden_fields`` names for an account is refused as a lookup and appears
        in none of the list's filters, searches or columns."""
        request = RequestFactory().get(BO)
        request.user = cast[who]
        checked = 0
        for model_admin in admin.site._registry.values():
            hidden = getattr(model_admin, "hidden_fields", lambda _request: frozenset())(request)
            for name in hidden:
                checked += 1
                for lookup in (name, f"{name}__exact", f"{name}__startswith", f"{name}__regex"):
                    assert not model_admin.lookup_allowed(lookup, "x", request), (model_admin, lookup)
                searched = {f.lstrip("^=@").split("__", 1)[0] for f in model_admin.get_search_fields(request)}
                filtered = {
                    f if isinstance(f, str) else f[0] if isinstance(f, list | tuple) else f.parameter_name
                    for f in model_admin.get_list_filter(request)
                }
                assert name not in searched | filtered | set(model_admin.get_list_display(request)), (model_admin, name)
        assert checked >= (2 if who == "superuser" else 4)


# =================================================================================================
# ALLOW — an account that may read the field still filters on it; the lists' own filters still work
# =================================================================================================
class TestTheListsStillWork:
    def test_the_administration_still_filters_the_outbox_by_body(self, client, cast, mail):
        client.force_login(cast["administrator"])
        assert _count(client, OUTBOX, {"body_text__contains": MARKER}) == 1
        assert MARKER in client.get(f"{OUTBOX}{mail.pk}/change/").content.decode("utf-8")

    def test_a_superuser_still_filters_the_results_by_answer(self, client, cast, result):
        client.force_login(cast["superuser"])
        assert _count(client, RESULTS, {"answers_snapshot__family": ANSWER}) == 1

    def test_the_lists_own_filters_and_searches_still_answer(self, client, cast, subscription, mail, result):
        client.force_login(cast["staff"])
        assert _count(client, SUBSCRIPTIONS, {"q": "f8r2.subscriber"}) == 1
        assert _count(client, SUBSCRIPTIONS, {"language__exact": subscription.language}) == 1
        assert _count(client, OUTBOX, {"status__exact": mail.status}) == 1
        assert _count(client, OUTBOX, {"q": "F8R2 subject"}) == 1
        client.force_login(cast["administrator"])
        assert _count(client, RESULTS, {"ruleset_version__exact": "1"}) == 1
        assert _count(client, SESSIONS, {"status__exact": result.session.status}) == 1
