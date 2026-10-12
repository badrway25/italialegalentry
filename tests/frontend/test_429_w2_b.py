"""
«Too many requests», as allauth answers them (V5.4 plan §1.13; acceptance L12; W2-B, step 2).

allauth's rate limits answer 429 with the template named ``429.html``. The product had none of that name — only
``errors/429.html``, which its own views render — so allauth fell back on a page of its own: English, unstyled,
«429 Too Many Requests». ``templates/429.html`` is that template:

* a person who is not signed in was at the entrance — the page is «Il varco», in the request's language, with the
  product's own words (one title, one sentence), the way back to the sign-in, and no arrival of the stage;
* a signed-in person met the limit on an account page — the product's own error page, with its recovery navigation;
* the status stays 429, the limits stay allauth's (``ACCOUNT_RATE_LIMITS``), and nothing says which limit was met.

The limits are reached through the real views, never by calling the template.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "429.html"

pytestmark = pytest.mark.django_db

#: allauth's own fallback page, word for word (allauth.core.internal.ratelimit.handler429).
FALLBACK = ("429 Too Many Requests", "You have sent too many requests. Please try again later.")
TITLE = "Trop de requêtes"
SENTENCE = (
    "Vous avez atteint la limite d’envois autorisée. Merci de réessayer dans quelques minutes ; "
    "rien n’a été perdu de votre côté."
)


def _throttled_reset(client, lang: str):
    """The password reset is limited to three requests an hour for one address: the fourth is refused."""
    assert settings.ACCOUNT_RATE_LIMITS["reset_password"] == "5/h/ip,3/h/key"
    path = f"/{lang}/compte/password/reset/"
    for _ in range(3):
        assert client.post(path, {"email": "someone@example.test"}).status_code == 302
    return client.post(path, {"email": "someone@example.test"})


@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_a_throttled_entrance_request_is_answered_on_the_stage_in_the_request_s_language(client, seeded, lang):
    response = _throttled_reset(client, lang)
    html = response.content.decode()
    assert response.status_code == 429
    for words in FALLBACK:
        assert words not in html, "allauth's English fallback page"
    with translation.override(lang):
        title, sentence = gettext(TITLE), gettext(SENTENCE)
    if lang != "fr":
        assert title != TITLE and sentence != SENTENCE, f"{lang}: the catalogue holds the page's words"
    direction = "rtl" if lang == "ar" else "ltr"
    assert f'<html lang="{lang}" dir="{direction}"' in html
    assert re.search(rf"<title>\s*{re.escape(title)}\s*·", html), "the document's title is the page's"
    # «Il varco»: the stage, one title, one sentence, the way back to the sign-in — and nothing else to do
    assert html.count("data-varco-stage") == 1 and 'class="account-page account-page--entrance varco"' in html
    focus = html.split('class="varco__focus"', 1)[1].split("data-varco-stage", 1)[0]
    assert re.findall(r"<h1[^>]*>\s*(.*?)\s*</h1>", focus, re.S) == [title] and html.count("<h1") == 1
    assert sentence.replace("’", "&#x27;") in focus or sentence in focus
    assert focus.count("<form") == 0 and focus.count("<button") == 0, "no form, no countdown, no retry button"
    way = focus.split('class="varco__back"', 1)[1].split("</p>", 1)[0]
    assert f'href="/{lang}/compte/login/"' in way
    assert 'class="error-page' not in html, "not the generic error page: the person was at the entrance"
    assert "someone@example.test" not in html and "3" not in re.sub(r"<[^>]+>", "", focus), "which limit, never"


def test_a_signed_in_person_gets_the_product_s_error_page(client, seeded, person_user):
    """The password page takes five posts a minute from one account (allauth counts what is sent, not what is read)."""
    assert settings.ACCOUNT_RATE_LIMITS["change_password"] == "5/m/user"
    client.force_login(person_user)
    path, refused = "/fr/compte/password/change/", {"oldpassword": "not-it", "password1": "n", "password2": "n"}
    responses = [client.post(path, refused) for _ in range(6)]
    statuses = [response.status_code for response in responses]
    assert statuses[:5] == [200] * 5 and statuses[5] == 429, statuses
    assert client.get(path).status_code == 200, "reading the page is never refused"
    html = responses[5].content.decode()
    for words in FALLBACK:
        assert words not in html
    assert 'class="container error-page"' in html and 'class="error-page__code"' in html
    assert "data-varco-stage" not in html, "a signed-in person is not sent back to the entrance"
    assert re.search(rf'<h1 id="error-title" class="error-page__title">{TITLE}</h1>', html)
    assert html.count("<h1") == 1 and "data-history-back" in html, "the error page's recovery navigation"


def test_the_template_is_one_page_with_two_parents_and_no_words_of_its_own():
    source = TEMPLATE.read_bytes().decode("utf-8")
    assert "\r" not in source
    body = re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", source, flags=re.S)
    assert body.startswith(
        '{% extends request.user.is_authenticated|yesno:"errors/429.html,allauth/layouts/entrance.html" %}'
    )
    assert "{% if request.user.is_authenticated %}{{ block.super }}{% else %}" in body, "the error page's own content"
    # its two messages are the error page's, word for word: no new copy
    error_page = (ROOT / "templates" / "errors" / "429.html").read_bytes().decode("utf-8")
    messages = re.findall(r'\{% translate "([^"]+)" %\}', body)
    assert sorted(set(messages)) == sorted({TITLE, SENTENCE}), messages
    for message in messages:
        assert f'{{% translate "{message}" %}}' in error_page, message
    assert not re.search(r"\sstyle=|<style|<script", body), "no inline style, no script"


def test_the_product_s_own_429_is_unchanged(client, seeded):
    """The views of the product render errors/429.html themselves (core.views.error_429): still the error page."""
    from django.test import RequestFactory

    from core.views import error_429

    request = RequestFactory().get("/fr/")
    request.session = client.session
    from django.contrib.auth.models import AnonymousUser

    request.user = AnonymousUser()
    response = error_429(request)
    html = response.content.decode()
    assert response.status_code == 429 and 'class="container error-page"' in html and "data-varco-stage" not in html
