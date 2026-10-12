"""
"Ma situation" — the page where a person tells the platform about their circumstances.

What is being defended:

* the page belongs to the person and to nobody else (deny by default, like every reserved page);
* a question is asked only when something reads the answer, and the page says what;
* saving re-runs the rules, so the orientation is dynamic rather than a photograph taken once;
* "I do not know yet" is preserved as a distinct answer from "no", because a rule that cannot tell
  them apart will fire on an absence of information.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.utils import timezone

from accounts.models import EducationLevel, PersonProfile

pytestmark = pytest.mark.django_db

SITUATION = "/fr/espace-reserve/ma-situation/"
LOGIN = "/fr/compte/login/"


@pytest.fixture
def signed_in(client, alice, seeded):
    client.force_login(alice)
    return client


def post(client, **overrides):
    data = {
        "date_of_birth": "",
        "nationality": "",
        "country_of_residence": "",
        "education_level": "",
        "years_of_experience": "",
        "languages": [],
        "has_job_offer": "",
        "has_qualification_recognition": "",
    }
    data.update(overrides)
    return client.post(SITUATION, data)


class TestAccess:
    def test_an_anonymous_visitor_is_sent_to_the_login_page(self, client, seeded):
        response = client.get(SITUATION)
        assert response.status_code == 302
        assert LOGIN in response["Location"]

    def test_the_page_is_never_indexed_and_never_cached(self, signed_in):
        response = signed_in.get(SITUATION)
        assert response.status_code == 200
        assert "noindex" in response["X-Robots-Tag"].lower()
        assert "no-store" in response["Cache-Control"]

    def test_a_person_sees_their_own_answers_and_only_their_own(self, client, alice, bob, seeded):
        PersonProfile.objects.update_or_create(user=bob, defaults={"nationality": "BOB-NATIONALITY-UNIQUE"})
        client.force_login(alice)
        body = client.get(SITUATION).content.decode()
        assert "BOB-NATIONALITY-UNIQUE" not in body


class TestTheQuestionsExplainThemselves:
    def test_every_question_says_what_it_is_used_for(self, signed_in):
        from accounts.profile_forms import SituationForm

        for name, field in SituationForm().fields.items():
            assert str(field.help_text).strip(), f"{name} asks for personal data without saying why"

    def test_the_page_states_what_it_does_not_ask_for(self, signed_in):
        body = signed_in.get(SITUATION).content.decode()
        assert "passeport" in body.lower()
        assert "reconnaît aucun" in body or "reconnaît aucune" in body

    def test_no_field_is_required(self, signed_in):
        from accounts.profile_forms import SituationForm

        assert not any(field.required for field in SituationForm().fields.values())

    def test_an_empty_submission_is_accepted(self, signed_in):
        assert post(signed_in).status_code == 302


class TestSaving:
    def test_answers_are_recorded(self, signed_in, alice):
        post(
            signed_in,
            nationality="MA",
            country_of_residence="MA",
            education_level=EducationLevel.HIGHER,
            years_of_experience="7",
            languages=["ar", "fr"],
            has_job_offer="yes",
        )
        profile = PersonProfile.objects.get(user=alice)
        assert profile.nationality == "MA"
        assert profile.education_level == EducationLevel.HIGHER
        assert profile.years_of_experience == 7
        assert profile.languages == ["ar", "fr"]
        assert profile.has_job_offer is True

    def test_i_do_not_know_yet_is_not_the_same_answer_as_no(self, signed_in, alice):
        post(signed_in, has_job_offer="no")
        assert PersonProfile.objects.get(user=alice).has_job_offer is False
        post(signed_in, has_job_offer="")
        assert PersonProfile.objects.get(user=alice).has_job_offer is None

    def test_a_future_date_of_birth_is_refused(self, signed_in, alice):
        # Tomorrow in Rome, the calendar the form checks (``timezone.localdate``): the host's
        # ``date.today()`` is still yesterday at 00:30 in Rome on a UTC host, and «tomorrow» was today.
        future = (timezone.localdate() + dt.timedelta(days=1)).isoformat()
        response = post(signed_in, date_of_birth=future)
        assert response.status_code == 200
        assert PersonProfile.objects.get(user=alice).date_of_birth is None

    def test_saving_is_audited_by_field_name_and_never_by_value(self, signed_in, alice):
        from audit.models import AuditEvent

        post(signed_in, nationality="SECRET-VALUE-UNIQUE")
        event = AuditEvent.objects.filter(action="account.situation_updated").latest("created_at")
        assert "nationality" in event.metadata["fields"]
        assert "SECRET-VALUE-UNIQUE" not in str(event.metadata)

    def test_an_unchanged_submission_records_no_audit_event(self, signed_in, alice):
        from audit.models import AuditEvent

        post(signed_in, nationality="MA")
        before = AuditEvent.objects.filter(action="account.situation_updated").count()
        post(signed_in, nationality="MA")
        assert AuditEvent.objects.filter(action="account.situation_updated").count() == before


class TestTheAnswersReachTheRuleEngine:
    def test_the_declared_facts_are_the_ones_a_rule_may_read(self, signed_in, alice):
        from rules.engine import ALLOWED_FIELDS
        from rules.facts import facts_for

        post(
            signed_in,
            date_of_birth="1994-03-15",
            nationality="MA",
            country_of_residence="MA",
            education_level=EducationLevel.HIGHER,
            years_of_experience="7",
            languages=["ar", "fr"],
            has_job_offer="yes",
        )
        alice.refresh_from_db()
        facts = facts_for(person=alice)
        assert facts["nationality"] == "MA"
        assert facts["residence_country"] == "MA"
        assert facts["languages"] == ["ar", "fr"]
        assert facts["has_job_offer"] is True
        assert isinstance(facts["age"], int)
        for key in facts:
            assert key.split(".", 1)[0] in ALLOWED_FIELDS, f"{key} is not a fact a rule may read"

    def test_the_date_of_birth_itself_never_reaches_a_rule(self, signed_in, alice):
        """A rule reads an age. Holding the date in the fact set would copy it into every snapshot."""
        from rules.facts import facts_for

        post(signed_in, date_of_birth="1994-03-15")
        alice.refresh_from_db()
        facts = facts_for(person=alice)
        assert "date_of_birth" not in facts
        assert "1994-03-15" not in str(facts)


class TestCompleteness:
    def test_the_counter_counts_answers_and_nothing_else(self, alice):
        profile = PersonProfile.objects.create(user=alice)
        assert profile.completeness == 0
        profile.nationality = "MA"
        profile.has_job_offer = False
        profile.save()
        assert profile.completeness == 2, "answering 'no' is an answer"

    def test_a_complete_profile_says_so(self, alice):
        profile = PersonProfile.objects.create(
            user=alice,
            date_of_birth=dt.date(1994, 3, 15),
            nationality="MA",
            country_of_residence="MA",
            education_level=EducationLevel.HIGHER,
            years_of_experience=7,
            languages=["fr"],
            has_job_offer=True,
        )
        assert profile.is_complete is True


class TestTheExportIncludesEverything:
    def test_the_personal_data_export_carries_the_situation(self, signed_in, alice):
        from accounts.services import export_user_data

        post(signed_in, nationality="MA", languages=["fr"], has_job_offer="no")
        alice.refresh_from_db()
        exported = export_user_data(alice)["profile"]
        assert exported["nationality"] == "MA"
        assert exported["languages"] == ["fr"]
        assert exported["has_job_offer"] is False

    def test_deleting_the_account_removes_the_situation(self, signed_in, alice):
        from accounts.services import anonymise_user

        post(signed_in, nationality="MA")
        anonymise_user(alice, reason="test")
        assert not PersonProfile.objects.filter(user=alice).exists()
