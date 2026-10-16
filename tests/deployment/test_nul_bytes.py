"""
A NUL byte in a request — its path, its query string, a form field, its session cookie — is answered with the project's
own 400 page: no 500, no traceback, no ERROR line in the log (gate 2's N-4, carried by gates 3 and 4 as N-G; the DevOps
lane's second pass, item 2, docs/design-v5/QA/v54/devops/NOTES.md).

PostgreSQL refuses a NUL in text, and psycopg raises DataError before the query leaves (in a jsonb value: «unsupported
Unicode escape sequence»). Measured on 16 October 2026, before cms.middleware.NulByteMiddleware, each vector below ended
in a 500 and an ERROR line with its traceback — one per request, for anyone:

* the path, `/fr/nothing%00here/`: the page's 404 rendered, then cms.middleware.LegacyURLMiddleware looked the path up
  among the redirects (lookup_redirect);
* the query string, `/fr/actualites/?categorie=%00`: the view, news.services.category_by_slug;
* a form field a view reads without a form: a case file's transition with a NUL in its reason (cases.views.transition →
  audit.services.record, jsonb) — here the stand-in view of tests/deployment/nul_urls.py, which looks the field up;
* the session cookie, `sessionid="\\000…"`: Python's cookie parser decodes the octal escape, the session lookup fails.

The guard answers nothing else. Its first version read the body of every POST in front of everything (the review of the
second pass, REVIEW_2 M1 and m1): the public webhook, csrf_exempt, could no longer read its raw body after a multipart
POST — a 500 and an ERROR line for anyone, no NUL needed — and a body Django refuses to parse (more fields than
DATA_UPLOAD_MAX_NUMBER_FIELDS) became a 400 with TooManyFieldsSent's ERROR line where CSRF had answered 403. The form
fields are now read where CsrfViewMiddleware reads them, for the views it protects, and a body that cannot be parsed is
left to the next reader. And the 400 leaves through the middlewares that write the site's security headers (REVIEW_2 m2).
"""

from __future__ import annotations

import logging
from urllib.parse import urlencode

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings

from cms.middleware import LegacyURLMiddleware

pytestmark = [pytest.mark.django_db, pytest.mark.security]

URLCONF = "tests.deployment.nul_urls"
STAND_IN = "/__nul__/lookup/"
RAW_BODY = "/__nul__/raw/"
#: The public webhook: no API key, csrf_exempt, and it reads its raw body (integrations.views.inbound_webhook).
WEBHOOK = "/api/v1/webhooks/anything/"
GUARD = "cms.middleware.NulByteMiddleware"

#: What Django's technical pages print and the product's pages never do.
LEAKS = ("Traceback", "Request Method", "Exception Value", "SECRET_KEY", "DataError", "INSTALLED_APPS", "\x00")

#: The headers the site puts on every page it draws: Django's SecurityMiddleware, XFrameOptionsMiddleware, django-csp,
#: core.middleware.ExtraSecurityHeadersMiddleware.
SECURITY_HEADERS = (
    "Content-Security-Policy",
    "X-Frame-Options",
    "Permissions-Policy",
    "Cross-Origin-Resource-Policy",
    "X-Permitted-Cross-Domain-Policies",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Cross-Origin-Opener-Policy",
)
#: The middlewares that write them on the way out, listed above the guard so that its 400 passes through them.
HEADER_WRITERS = (
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
    "core.middleware.BackofficeCSPMiddleware",
    "core.middleware.ExtraSecurityHeadersMiddleware",
)


@pytest.fixture
def client_():
    return Client(raise_request_exception=False)


def assert_quiet(caplog) -> None:
    loud = [(r.levelname, r.name, r.getMessage()) for r in caplog.records if r.levelno >= logging.ERROR or r.exc_info]
    assert not loud, f"an ERROR line or a traceback in the log: {loud}"


def assert_clean_400(response, caplog) -> str:
    html = response.content.decode("utf-8")
    assert response.status_code == 400, response.status_code
    assert 'class="container error-page"' in html, "not the project's own 400 page"
    for leak in LEAKS:
        assert leak not in html, f"the 400 page leaks {leak!r}"
    assert_quiet(caplog)
    return html


def too_many_fields() -> dict[str, str]:
    """More fields than Django parses (DATA_UPLOAD_MAX_NUMBER_FIELDS): request.POST raises TooManyFieldsSent, which
    Django logs at ERROR with its traceback — whoever reads the form first meets it."""
    return {f"f{i}": "x" for i in range(settings.DATA_UPLOAD_MAX_NUMBER_FIELDS + 50)}


@pytest.mark.parametrize(
    "path",
    ["/fr/nothing%00here/", "/fr/%00/", "/%00", "/fr/actualites/a%00b/", "/static/js/dist/loader.js%00"],
)
def test_a_nul_byte_in_the_path_is_a_clean_400(client_, caplog, path):
    caplog.set_level(logging.WARNING)
    assert_clean_400(client_.get(path), caplog)


@pytest.mark.parametrize("query", ["categorie=%00", "categorie=a%00b", "%00=x", "page=1&q=%00"])
def test_a_nul_byte_in_the_query_string_is_a_clean_400(client_, caplog, query):
    caplog.set_level(logging.WARNING)
    assert_clean_400(client_.get(f"/fr/actualites/?{query}"), caplog)


@override_settings(ROOT_URLCONF=URLCONF)
def test_a_nul_byte_in_a_form_field_is_a_clean_400(client_, caplog):
    caplog.set_level(logging.WARNING)
    assert_clean_400(client_.post(STAND_IN, {"old_path": "/a\x00b/"}), caplog)
    assert_clean_400(client_.post(STAND_IN, {"old\x00path": "x"}), caplog)
    # multipart: the text fields are read, as a form sends them beside a file
    upload = SimpleUploadedFile("piece.pdf", b"%PDF-1.4 ...", content_type="application/pdf")
    assert_clean_400(client_.post(STAND_IN, {"old_path": "/a\x00b/", "file": upload}), caplog)


def test_a_nul_byte_in_the_sign_in_form_is_a_clean_400(client_, caplog):
    """A public form: Django's field would refuse the value with a message; the request never reaches it."""
    caplog.set_level(logging.WARNING)
    response = client_.post("/fr/compte/login/", {"login": "a\x00b@example.test", "password": "irrelevant"})
    assert_clean_400(response, caplog)


def test_a_nul_byte_in_the_session_cookie_is_a_clean_400(caplog):
    caplog.set_level(logging.WARNING)
    client = Client(raise_request_exception=False, HTTP_COOKIE=f'{settings.SESSION_COOKIE_NAME}="\\000abcdefgh"')
    assert_clean_400(client.get("/fr/"), caplog)


def test_the_400_page_speaks_the_language_of_the_path(client_, caplog):
    html = assert_clean_400(client_.get("/ar/nothing%00here/"), caplog)
    assert 'lang="ar"' in html and 'dir="rtl"' in html


@override_settings(ROOT_URLCONF=URLCONF)
def test_a_file_holding_nul_bytes_is_never_refused(client_):
    """A document's bytes hold NUL by nature: the guard reads the form's text fields, never request.FILES."""
    upload = SimpleUploadedFile("scan.png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00", content_type="image/png")
    response = client_.post(STAND_IN, {"old_path": "/plain/", "file": upload})
    assert response.status_code == 200, response.status_code
    assert response.content == b"looked up; files received: 1"


def test_a_request_without_a_nul_byte_is_untouched(client_):
    assert client_.get("/fr/").status_code == 200
    # `%2500` is the text «%00», three characters: nothing for PostgreSQL to refuse
    assert client_.get("/fr/actualites/?q=%2500").status_code == 200
    # the sign-in form answers its own way (a 200 with the form's message), not with the 400
    assert client_.post("/fr/compte/login/", {"login": "nobody@example.test", "password": "x"}).status_code == 200


def test_the_public_webhook_still_reads_its_body_after_a_multipart_post(client_, caplog):
    """
    REVIEW_2 M1: the guard parsed every POST's form, and Django parses a multipart body from the request's stream, after
    which the raw body cannot be read — the webhook answered 500 with RawPostDataException's traceback, for anyone, no
    NUL needed. Legitimate senders post JSON, which is never parsed as a form: what answers here is the webhook (an
    unknown system: 401), as before the guard.
    """
    caplog.set_level(logging.WARNING)
    response = client_.post(WEBHOOK, {"event": "ping"})  # the test client's default: multipart/form-data
    assert response.status_code == 401, response.status_code
    assert response.json()["error"]["code"] == "unknown_system"
    assert_quiet(caplog)


def test_a_webhook_body_of_more_fields_than_django_parses_is_still_the_webhook_s(client_, caplog):
    """REVIEW_2 m1: the guard's parse raised TooManyFieldsSent — a 400 and an ERROR line with its traceback, for anyone."""
    caplog.set_level(logging.WARNING)
    body = urlencode(too_many_fields())
    response = client_.post(WEBHOOK, body, content_type="application/x-www-form-urlencoded")
    assert response.status_code == 401, response.status_code
    assert_quiet(caplog)


@override_settings(ROOT_URLCONF=URLCONF)
def test_a_csrf_exempt_view_keeps_its_raw_body_nul_or_not(client_, caplog):
    """
    The form is read where CsrfViewMiddleware reads it, for the views it protects: a csrf_exempt view reads its body
    itself — the integrations API — and a NUL there is its own to answer, as before the guard (no such view stores a
    posted field today).
    """
    caplog.set_level(logging.WARNING)
    response = client_.post(RAW_BODY, {"note": "a\x00b"})
    assert response.status_code == 200, response.status_code
    assert response.content.startswith(b"read its body: "), response.content[:80]
    assert_quiet(caplog)


@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
def test_a_body_django_will_not_parse_is_answered_as_without_the_guard(caplog, encoding):
    """
    More fields than Django parses, posted to the public sign-in without a CSRF cookie: CsrfViewMiddleware refuses the
    request (403) before it reads anything, as it did before the guard. A guard that parsed the form first answered 400
    with TooManyFieldsSent's ERROR line and traceback, for anyone (REVIEW_2 m1's cause, on every protected form): a body
    that cannot be parsed is left to the next reader, which answers it as before.
    """
    caplog.set_level(logging.WARNING)
    client = Client(raise_request_exception=False, enforce_csrf_checks=True)
    if encoding == "multipart":
        response = client.post("/fr/compte/login/", too_many_fields())
    else:
        body = urlencode(too_many_fields())
        response = client.post("/fr/compte/login/", body, content_type="application/x-www-form-urlencoded")
    assert response.status_code == 403, response.status_code
    assert_quiet(caplog)


@override_settings(ROOT_URLCONF=URLCONF)
def test_the_400_carries_the_security_headers_of_every_page(client_, caplog):
    """
    REVIEW_2 m2: the guard answers before the views, and its 400 had only SecurityMiddleware's headers — no CSP, no
    X-Frame-Options, no Permissions-Policy — because the middlewares that write them sat below it. Listed above it, they
    put on its page the same headers, with the same values, as on any page.
    """
    caplog.set_level(logging.WARNING)
    page = client_.get("/fr/")
    assert page.status_code == 200, page.status_code
    expected = {name: page.get(name) for name in SECURITY_HEADERS}
    assert all(expected.values()), f"a page of the site lacks one of SECURITY_HEADERS: {expected}"
    cookie = Client(raise_request_exception=False, HTTP_COOKIE=f'{settings.SESSION_COOKIE_NAME}="\\000abcdefgh"')
    for vector, response in (
        ("path", client_.get("/fr/nothing%00here/")),
        ("query string", client_.get("/fr/actualites/?categorie=%00")),
        ("session cookie", cookie.get("/fr/")),
        ("form field", client_.post(STAND_IN, {"old_path": "/a\x00b/"})),
    ):
        assert_clean_400(response, caplog)
        answered = {name: response.get(name) for name in SECURITY_HEADERS}
        assert answered == expected, f"the 400 answering a NUL in the {vector} lacks the site's headers: {answered}"


def test_the_redirect_lookup_never_sends_a_nul_byte_to_the_database(django_assert_num_queries):
    """The second layer, should the guard ever be moved or removed: the lookup that broke first answers «no redirect»."""
    with django_assert_num_queries(0):
        assert LegacyURLMiddleware.lookup_redirect("/fr/nothing\x00here/") is None


def test_the_guard_stands_before_everything_that_reads_a_value():
    chain = settings.MIDDLEWARE
    guard = chain.index(GUARD)
    for before in ("core.middleware.RequestIDMiddleware", "django.middleware.locale.LocaleMiddleware"):
        assert chain.index(before) < guard, f"{before} must run first: the page carries its id and its language"
    writers = [chain.index(name) for name in HEADER_WRITERS]
    assert writers == sorted(writers), "the header writers keep their order (BackofficeCSP after django-csp)"
    assert chain.index("core.middleware.TextGZipMiddleware") < writers[0], "django-csp stays below the gzip layer"
    assert writers[-1] < guard, "the security headers are written on the guard's 400 too: their writers stand above it"
    for after in (
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "allauth.account.middleware.AccountMiddleware",
        "accounts.middleware.BackofficeMFAMiddleware",
        "cms.middleware.LegacyURLMiddleware",
    ):
        assert guard < chain.index(after), f"{after} reads the request's values: the guard must run before it"
