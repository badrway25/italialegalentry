"""
No URL pattern and no setting exposes PRIVATE_MEDIA_ROOT — under the production settings as well as the test ones.

Private documents (identity documents, contracts, diplomas) leave the server through one exit only:
``documents.views._serve``, after ``documents.policies`` and ``services.delivery_block`` have said yes (proven by
apps/documents/tests/test_download.py, test_signed_links.py and tests/security/test_authorization_audit.py). That
exit is worth nothing if the same file can also be fetched another way, so this module checks the other ways:

* no URL pattern serves files from disk (``django.views.static.serve``) out of the private root — in production
  no such pattern exists at all, which is also why the reverse proxy, not Django, serves public media;
* the private root overlaps none of the directories something publishes: MEDIA_ROOT (nginx's /media/ alias),
  STATIC_ROOT (WhiteNoise indexes it at start-up), STATICFILES_DIRS (collectstatic copies them into STATIC_ROOT);
* the private storage has no URL at all;
* an empty PRIVATE_MEDIA_ROOT means the default directory, never the current one (it used to mean «.», and the
  documents then landed in the root of the checkout).

The web server's own configuration cannot be tested here; tests/deployment/test_runbook_matches_the_code.py holds
the runbook's nginx block to «no alias, no root, for the private directory».
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import URLResolver, get_resolver

ROOT = Path(__file__).resolve().parents[2]

#: Run in a child process under any settings module: the URL patterns that serve files from disk, the directories
#: that are published, the private root, and whether the private storage would hand out a URL.
PROBE = r"""
import json, django
django.setup()
from pathlib import Path
from django.conf import settings
from django.urls import URLResolver, get_resolver

def walk(patterns, prefix=""):
    for entry in patterns:
        if isinstance(entry, URLResolver):
            yield from walk(entry.url_patterns, prefix + str(entry.pattern))
        else:
            yield prefix + str(entry.pattern), entry.callback, entry.default_args

serving = [
    {"route": route, "document_root": str(args.get("document_root", ""))}
    for route, callback, args in walk(get_resolver().url_patterns)
    if getattr(callback, "__module__", "") == "django.views.static" and callback.__name__ == "serve"
]
from documents.storage import PrivateFileSystemStorage, private_root, private_storage
try:
    try:
        storage = private_storage()
    except OSError:
        # private_storage() creates its root, and the runbook's root exists only on the server: where it cannot be
        # created, the same class at the same root answers the question asked here — does it hand out a URL?
        storage = PrivateFileSystemStorage(location=str(private_root()), base_url=None)
    storage.url("1/x.pdf")
    url = "a URL was produced"
except Exception as exc:
    url = type(exc).__name__
served = {"MEDIA_ROOT": str(settings.MEDIA_ROOT), "STATIC_ROOT": str(settings.STATIC_ROOT)}
served.update({f"STATICFILES_DIRS[{i}]": str(d[1] if isinstance(d, (tuple, list)) else d) for i, d in enumerate(settings.STATICFILES_DIRS)})
if getattr(settings, "WHITENOISE_ROOT", None):
    served["WHITENOISE_ROOT"] = str(settings.WHITENOISE_ROOT)
print(json.dumps({
    "debug": settings.DEBUG,
    "serving": serving,
    "served": served,
    "private": str(Path(settings.PRIVATE_MEDIA_ROOT).resolve()),
    "url": url,
}))
"""

PRODUCTION = {
    "DJANGO_SETTINGS_MODULE": "config.settings.prod",
    "DJANGO_SECRET_KEY": "K" + "aB3xY7zQ9wE2rT5yU8iO1pA4sD6fG0hJ-kL_mN3bV5cX7zQ9wE2rT5yU8iO1pA4s",
    "DJANGO_ALLOWED_HOSTS": "example.com",
    "DJANGO_CSRF_TRUSTED_ORIGINS": "https://example.com",
    "DATABASE_URL": "postgres://ile:ile-dev-password@127.0.0.1:5439/ile",
    "IP_HASH_SALT": "Zq3vN8rT1yW6uI0oP5aS9dF2gH7jK4lX-cV_bN1mQ8wE3rT6",
    "BACKOFFICE_MFA_ENFORCED": "1",
    "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
    # No default under the production settings: the production template's values.
    "SECURE_HSTS_INCLUDE_SUBDOMAINS": "0",
    "SECURE_HSTS_PRELOAD": "0",
}


def _probe(**environment) -> dict:
    env = {**os.environ, **environment}
    env.pop("ILE_ALLOW_INSECURE_PROD", None)
    run = subprocess.run(
        [sys.executable, "-c", PROBE],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        check=False,
    )
    assert run.returncode == 0, run.stderr[-2000:]
    return json.loads(run.stdout.strip().splitlines()[-1])


def _overlap(a: str, b: str) -> bool:
    first, second = Path(a).resolve(), Path(b).resolve()
    return first == second or first in second.parents or second in first.parents


def _assert_private_is_never_served(report: dict) -> None:
    for name, directory in report["served"].items():
        assert not _overlap(report["private"], directory), f"PRIVATE_MEDIA_ROOT overlaps {name} ({directory})"
    for pattern in report["serving"]:
        assert not _overlap(report["private"], pattern["document_root"]), f"{pattern['route']} serves the private root"
    assert report["url"] == "ImproperlyConfigured", report["url"]


@pytest.mark.parametrize(
    "layout",
    [{}, {"MEDIA_ROOT": "/var/lib/italylegalentry/media", "PRIVATE_MEDIA_ROOT": "/var/lib/italylegalentry/private"}],
    ids=["defaults", "runbook-layout"],
)
def test_under_the_production_settings_nothing_serves_the_private_root(layout):
    report = _probe(**PRODUCTION, **layout)
    assert report["debug"] is False
    # In production Django serves no file from disk at all: public media is the reverse proxy's /media/ alias,
    # static files are WhiteNoise's, private documents are documents.views._serve's.
    assert report["serving"] == [], report["serving"]
    _assert_private_is_never_served(report)


def test_a_private_root_this_machine_cannot_create_still_has_no_url(tmp_path):
    """
    The runbook's directories exist only on the server, created there with their owner. On a CI runner /var/lib is not
    writable (GitHub's Linux runner answered PermissionError where Windows had quietly created C:\\var\\lib), so the
    probe asks the storage its question — does it hand out a URL? — whether or not the root can be created here.
    """
    blocker = tmp_path / "a-file"
    blocker.write_text("not a directory", encoding="utf-8")
    report = _probe(**PRODUCTION, MEDIA_ROOT=str(tmp_path / "media"), PRIVATE_MEDIA_ROOT=str(blocker / "private"))
    _assert_private_is_never_served(report)


def test_under_the_development_settings_the_media_route_is_not_the_private_root():
    """DEBUG mounts static(MEDIA_URL, document_root=MEDIA_ROOT); that pattern must not reach the private root either."""
    report = _probe(
        DJANGO_SETTINGS_MODULE="config.settings.dev", ILE_READ_ENV_FILE="0", DJANGO_DEBUG="1", ILE_DESIGN_PREVIEW="0"
    )
    assert report["debug"] is True
    assert [p["document_root"] for p in report["serving"]] == [report["served"]["MEDIA_ROOT"]], report["serving"]
    _assert_private_is_never_served(report)


def test_an_empty_private_media_root_means_the_default_directory_not_the_current_one():
    report = _probe(
        DJANGO_SETTINGS_MODULE="config.settings.dev",
        ILE_READ_ENV_FILE="0",
        DJANGO_DEBUG="1",
        ILE_DESIGN_PREVIEW="0",
        PRIVATE_MEDIA_ROOT="",
    )
    assert report["private"] == str((ROOT / "private_media").resolve()), report["private"]


def test_in_this_process_no_pattern_serves_files_and_the_private_storage_has_no_url():
    """The same statements in-process, under the test settings (DEBUG off, like production)."""

    def walk(patterns):
        for entry in patterns:
            if isinstance(entry, URLResolver):
                yield from walk(entry.url_patterns)
            else:
                yield entry.callback

    assert settings.DEBUG is False
    assert not [
        cb for cb in walk(get_resolver().url_patterns) if getattr(cb, "__module__", "") == "django.views.static"
    ]
    from documents.storage import PrivateFileSystemStorage

    with pytest.raises(ImproperlyConfigured):
        PrivateFileSystemStorage(location=str(settings.PRIVATE_MEDIA_ROOT)).url("1/x.pdf")
