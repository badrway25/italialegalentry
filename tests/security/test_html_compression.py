"""
HTML compression (Gate A, 26/09/2026 — approved by the product owner): core.middleware.TextGZipMiddleware.

What must hold:
- a rendered page is gzip-encoded when the client accepts it, with `Vary: Accept-Encoding`;
- it is not when the client does not ask for it;
- binary responses (a private document, an image) are never compressed on the fly;
- the middleware sits below WhiteNoise, so static files — already precompressed by
  collectstatic — never reach it (no double compression);
- the BREACH mitigation of Django's GZipMiddleware (random padding) is the one in use.
"""

from __future__ import annotations

import gzip

from django.conf import settings
from django.http import HttpResponse
from django.test import RequestFactory

from core.middleware import TextGZipMiddleware


def test_a_rendered_page_is_gzipped_when_the_client_accepts_it(client, seeded):
    response = client.get("/fr/", HTTP_ACCEPT_ENCODING="gzip, deflate, br")
    assert response.status_code == 200
    assert response["Content-Encoding"] == "gzip"
    assert "Accept-Encoding" in response["Vary"]
    html = gzip.decompress(response.content).decode("utf-8")
    assert "<!DOCTYPE html>" in html


def test_a_page_is_plain_when_the_client_does_not_ask(client, seeded):
    response = client.get("/fr/")
    assert response.status_code == 200
    assert not response.has_header("Content-Encoding")


def test_binary_content_is_never_compressed_on_the_fly():
    factory = RequestFactory()
    request = factory.get("/", HTTP_ACCEPT_ENCODING="gzip")
    for content_type in ("application/pdf", "image/jpeg", "image/webp", "application/octet-stream"):
        response = HttpResponse(b"%PDF" + b"x" * 5000, content_type=content_type)
        out = TextGZipMiddleware(lambda r: response).process_response(request, response)
        assert not out.has_header("Content-Encoding"), content_type


def test_text_content_is_compressed_with_the_breach_padding():
    factory = RequestFactory()
    request = factory.get("/", HTTP_ACCEPT_ENCODING="gzip")
    body = ("<p>" + "x" * 4000 + "</p>").encode()
    sizes = set()
    for _ in range(8):
        response = HttpResponse(body, content_type="text/html; charset=utf-8")
        out = TextGZipMiddleware(lambda r: response).process_response(request, response)
        assert out["Content-Encoding"] == "gzip"
        assert gzip.decompress(out.content) == body
        sizes.add(len(out.content))
    # Django pads each body with up to 100 random bytes: eight identical bodies, several lengths.
    assert TextGZipMiddleware.max_random_bytes >= 100
    assert len(sizes) > 1, "no random padding: the BREACH mitigation is not in use"


def test_the_middleware_sits_below_whitenoise_and_above_the_body_writers():
    stack = settings.MIDDLEWARE
    gzip_at = stack.index("core.middleware.TextGZipMiddleware")
    assert stack.index("whitenoise.middleware.WhiteNoiseMiddleware") < gzip_at
    for later in ("csp.middleware.CSPMiddleware", "django.middleware.csrf.CsrfViewMiddleware"):
        assert stack.index(later) > gzip_at, later
    assert "django.middleware.gzip.GZipMiddleware" not in stack, "two gzip layers would compress twice"
