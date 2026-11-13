"""
No back-office form and no list filter names another account to an account that may not read accounts (finding F-8,
review F8R-3).

The accounts screens are closed to role:staff, role:content_editor, role:moderator and role:operator — but
``User.__str__`` is the e-mail address, and a foreign key to the user model renders its choices from the whole user
table. The editorial forms (banners, the home hero, the Forum's pages, «Vivre en Italie», news, partners) listed every
account's address — persons included — on their add page; an autocomplete rendered the address of whichever account
its initial value named (``faq/faqitem/add/?author=<pk>``); a crafted POST set any account as a row's author or
reviewer, or moved a forum membership to another account, and the page then printed that account's address; the news
list's «dernier éditeur» filter listed every account. Each DENY below failed before the fix: for an account that may
not open the accounts screen, every account field of a form is read-only (``core.admin_base.frozen_account_fields``) —
it shows the account the row already names and nothing else — and a filter over an account lists only the accounts the
screen's own rows name. The ALLOW tests hold that the workflow still sets these fields (the author on creation, the
reviewer by the review action) and that the administration, which reads accounts, still chooses them.

Accounts are this module's own, created with a test-only password and signed in through minted sessions
(``Client.force_login``); ``roles.ensure_roles()`` gives the roles their model permissions as the production seed does.
"""

from __future__ import annotations

import warnings

import pytest
from django import forms
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from accounts import roles

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Local-Only-F8R3-2026!"
BO = "/backoffice/"

#: The roles that open editorial or moderation screens and may not open the accounts screen.
NO_ACCOUNTS = {
    "staff": roles.STAFF,
    "content_editor": roles.CONTENT_EDITOR,
    "moderator": roles.MODERATOR,
    "operator": roles.OPERATOR,
    "legal_editor": roles.LEGAL_EDITOR,
    "legal_approver": roles.LEGAL_APPROVER,
}

#: Add pages each role may open whose account fields were a plain select of every account (the review's inventory).
SELECT_SCREENS = [
    ("staff", "cms/sitebanner"),
    ("staff", "cms/homehero"),
    ("staff", "forum/forumevent"),
    ("staff", "forum/forumdocument"),
    ("staff", "living/livingtopic"),
    ("staff", "living/livingsheet"),
    ("staff", "news/article"),
    ("staff", "partners/partner"),
    ("staff", "portal/portalnotice"),
    ("content_editor", "cms/sitebanner"),
    ("content_editor", "cms/homehero"),
    ("content_editor", "living/livingsheet"),
    ("content_editor", "news/article"),
    ("content_editor", "partners/partner"),
    ("content_editor", "faq/faqitem"),
    ("content_editor", "glossary/term"),
]


@pytest.fixture
def cast(django_user_model):
    roles.ensure_roles()

    def make(key, role=None, **extra):
        user = django_user_model.objects.create_user(email=f"f8r3.{key}@example.test", password=PASSWORD, **extra)
        if role:
            roles.assign_role(user, role)
        return user

    people = {key: make(key, role, is_staff=True) for key, role in NO_ACCOUNTS.items()}
    people["administrator"] = make("administrator", roles.ADMINISTRATOR, is_staff=True)
    people["person"] = make("person", roles.PERSON)
    people["other_person"] = make("other.person", roles.PERSON)
    people["superuser"] = django_user_model.objects.create_superuser(email="f8r3.super@example.test", password=PASSWORD)
    return people


def _others(cast, who) -> list[str]:
    """The addresses ``who`` may not read: every account of the cast but its own."""
    return [user.email for key, user in cast.items() if key != who]


def _leaked(page: str, cast, who) -> list[str]:
    return [email for email in _others(cast, who) if email in page]


def _request(user):
    request = RequestFactory().get(BO)
    request.user = user
    request.session = {}
    return request


def _account_choice_fields(form_class) -> list[str]:
    user_model = get_user_model()
    return [
        name
        for name, field in form_class.base_fields.items()
        if isinstance(field, forms.ModelChoiceField) and field.queryset.model is user_model and not field.disabled
    ]


# =================================================================================================
# DENY — a form or a filter answers no account an account may not read
# =================================================================================================
class TestTheForms:
    @pytest.mark.parametrize("who,screen", SELECT_SCREENS, ids=[f"{w}-{s}" for w, s in SELECT_SCREENS])
    def test_an_add_page_lists_no_other_account(self, client, cast, who, screen):
        client.force_login(cast[who])
        response = client.get(f"{BO}{screen}/add/")
        assert response.status_code == 200, (screen, response.status_code)
        leaked = _leaked(response.content.decode("utf-8"), cast, who)
        assert not leaked, f"F8R-3: {who} reads {leaked} on {screen}"

    @pytest.mark.parametrize("who", ["staff", "content_editor"])
    @pytest.mark.parametrize("screen", ["faq/faqitem", "cms/sitebanner", "glossary/term"])
    def test_an_initial_value_names_no_account(self, client, cast, who, screen):
        client.force_login(cast[who])
        target = cast["other_person"]
        response = client.get(f"{BO}{screen}/add/", {"author": target.pk, "reviewer": target.pk})
        assert response.status_code == 200
        assert target.email not in response.content.decode("utf-8"), (
            f"F8R-3: an id answered with its address on {screen}"
        )

    def test_a_crafted_post_names_no_other_account_as_author_or_reviewer(self, client, cast):
        from cms.models import SiteBanner

        client.force_login(cast["staff"])
        target = cast["other_person"]
        response = client.post(
            f"{BO}cms/sitebanner/add/",
            {"key": "f8r3-banner", "status": "draft", "author": target.pk, "reviewer": target.pk, "requires_flag": "x"},
        )
        assert response.status_code == 302, response.content[:2000]
        banner = SiteBanner.objects.get(key="f8r3-banner")
        assert banner.author == cast["staff"] and banner.reviewer is None, "F8R-3: a POST named another account"
        page = client.get(f"{BO}cms/sitebanner/{banner.pk}/change/").content.decode("utf-8")
        assert target.email not in page

    def test_a_moderator_moves_no_membership_to_another_account(self, client, cast):
        from community.models import Membership

        membership = Membership.objects.create(user=cast["person"], category="company")
        client.force_login(cast["moderator"])
        page = client.get(f"{BO}community/membership/{membership.pk}/change/")
        assert page.status_code == 200
        assert cast["other_person"].email not in page.content.decode("utf-8")
        client.post(
            f"{BO}community/membership/{membership.pk}/change/",
            {"user": cast["other_person"].pk, "category": "company", "status": membership.status},
        )
        membership.refresh_from_db()
        assert membership.user == cast["person"], "F8R-3: a moderator handed a membership to another account"

    @pytest.mark.parametrize("who", list(NO_ACCOUNTS))
    def test_no_form_of_the_registry_offers_a_choice_of_accounts(self, cast, who):
        """Every add and change form (and every inline) a role may open: no field chooses among accounts."""
        request = _request(cast[who])
        offending = []
        for model, model_admin in admin.site._registry.items():
            for change in (False, True):
                allowed = (
                    model_admin.has_change_permission(request) if change else model_admin.has_add_permission(request)
                )
                if not allowed:
                    continue
                with warnings.catch_warnings():  # a URLField's Django 6.0 notice, unrelated to what is checked
                    warnings.simplefilter("ignore", DeprecationWarning)
                    fields = flatten_fieldsets(model_admin.get_fieldsets(request, None))
                    form_class = model_admin.get_form(request, None, change=change, fields=fields)
                    offending += [(model._meta.label, name) for name in _account_choice_fields(form_class)]
                    for inline in model_admin.get_inline_instances(request, None):
                        inline_fields = flatten_fieldsets(inline.get_fieldsets(request, None))
                        formset = inline.get_formset(request, None, fields=inline_fields)
                        offending += [(inline.model._meta.label, n) for n in _account_choice_fields(formset.form)]
        assert not offending, f"F8R-3: {who} chooses among accounts on {sorted(set(offending))}"


class TestTheFilters:
    def test_the_news_editor_filter_lists_only_the_editors_of_the_list(self, client, cast):
        from news.models import Article, NewsCategory

        category = NewsCategory.objects.create(slug="f8r3-category", name_fr="Catégorie F8R3")
        Article.objects.create(
            slug="f8r3", category=category, title_fr="F8R3", summary_fr="s", body_fr="b", editor=cast["staff"]
        )
        client.force_login(cast["content_editor"])
        response = client.get(f"{BO}news/article/")
        assert response.status_code == 200
        page = response.content.decode("utf-8")
        assert cast["staff"].email in page, "the article's editor is the list's own column and filter"
        leaked = [email for email in _others(cast, "content_editor") if email in page and email != cast["staff"].email]
        assert not leaked, f"F8R-3: the editor filter lists {leaked}"


# =================================================================================================
# ALLOW — the workflow still sets the fields; the administration still chooses them
# =================================================================================================
class TestTheWorkflowStillSetsThem:
    def test_the_author_is_the_account_that_creates_the_row(self, client, cast):
        from cms.models import SiteBanner

        client.force_login(cast["content_editor"])
        client.post(f"{BO}cms/sitebanner/add/", {"key": "f8r3-own", "status": "draft", "requires_flag": "x"})
        assert SiteBanner.objects.get(key="f8r3-own").author == cast["content_editor"]

    def test_the_review_action_records_the_reviewer(self, client, cast):
        from living.models import LegalReviewStatus, LivingSheet, LivingTopic

        topic = LivingTopic.objects.create(slug="f8r3-topic", name_fr="Thème F8R3")
        sheet = LivingSheet.objects.create(topic=topic, slug="f8r3-sheet", title_fr="Fiche F8R3", body_fr="Corps.")
        client.force_login(cast["content_editor"])
        client.post(
            f"{BO}living/livingsheet/",
            {"action": "action_mark_reviewed", "_selected_action": [str(sheet.pk)], "index": "0"},
        )
        sheet.refresh_from_db()
        assert sheet.legal_review == LegalReviewStatus.REVIEWED and sheet.reviewer == cast["content_editor"]

    @pytest.mark.parametrize("who", ["administrator", "superuser"])
    def test_an_account_that_reads_accounts_still_chooses_them(self, client, cast, who):
        client.force_login(cast[who])
        page = client.get(f"{BO}cms/sitebanner/add/").content.decode("utf-8")
        assert 'name="author"' in page and 'name="reviewer"' in page
        request = _request(cast[who])
        model_admin = admin.site._registry[get_user_model()]
        assert model_admin.has_view_permission(request)
