"""
No third party's e-mail address may sit in the repository.

The read-only audit of the current site captured a third party's personal data, and the captures
were first committed verbatim, in six files, as evidence. The personal-data finding about the
current site is recorded in the private register.

The finding belongs in the audit; the data do not belong in a repository that may be shared.
This test keeps the distinction after the redaction, and catches the next capture that forgets it.

Every check here is by SHAPE, never by value. A guard that stores the secret in order to find the
secret is not a guard: the first version of this file searched for the value it protects as a
literal, which made the file match itself the moment it was committed, and left that value in the
repository it was supposed to be clearing.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

#: Top-level domains reserved by RFC 2606 / RFC 6761: an address under one cannot reach a person.
RESERVED_TLDS = (".test", ".invalid", ".example", ".localhost")

#: Addresses the project owns, or that belong to the systems it audits. Everything else is somebody's.
ALLOWED_DOMAINS = (
    "agamieuromed.org",  # the single public destination of every form
    "example.com",  # RFC 2606
    "example.org",
    "legalitalentry.it",  # named in the audit as *not* activated; guarded by its own rule
    "azienda.it",  # the placeholder inside the current site's own company form, captured verbatim
)

ADDRESS = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")

#: A run of hex long enough to be a digest rather than a colour or an identifier.
LONG_HEX = re.compile(r"\b[0-9a-f]{32,}\b")

#: Binary and vendored paths where a match would be noise rather than a leak.
SKIP_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".ico", ".woff", ".woff2", ".pdf", ".mo", ".po")
SKIP_PREFIXES = ("locale/", "static/vendor/", "docs/audit/current-site/screenshots/")

CAPTURES = ROOT / "docs" / "audit" / "current-site" / "raw"


def _tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True, encoding="utf-8"
    )
    return [line for line in out.stdout.splitlines() if line]


@pytest.fixture(scope="module")
def tracked() -> list[str]:
    files = _tracked_files()
    assert len(files) > 200, "git ls-files returned too little to be the repository"
    return files


def test_no_third_party_email_address_is_committed(tracked):
    offenders: list[str] = []
    for name in tracked:
        if name.endswith(SKIP_SUFFIXES) or name.startswith(SKIP_PREFIXES):
            continue
        path = ROOT / name
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in ADDRESS.finditer(text):
            domain = match.group(1).lower().rstrip(".")
            if domain.endswith(RESERVED_TLDS) or domain.endswith(ALLOWED_DOMAINS):
                continue
            offenders.append(f"{name}: {match.group(0)}")
    assert not offenders, "third-party e-mail addresses are committed:\n" + "\n".join(sorted(set(offenders))[:20])


def test_the_captured_wordpress_user_record_carries_no_identifier():
    """
    What the capture may contain is defined positively: redaction markers, and nothing else.

    No address, no digest, no author-archive slug. Stating it this way means the test never has to
    name the value it is protecting, and it catches a *different* identifier appearing tomorrow.
    """
    capture = CAPTURES / "wp_json_users.json"
    assert capture.exists(), "the audit evidence was deleted rather than redacted"
    text = capture.read_text(encoding="utf-8")

    assert "REDATTO" in text, "the capture is no longer redacted"
    assert not LONG_HEX.search(text), "a long hex digest is in the capture"
    assert "@" not in text, "an e-mail address is in the capture"
    assert not re.search(r"/author/(?!\[REDATTO)", text), "an author archive slug is not redacted"


def test_no_digest_sits_in_the_audit_captures():
    """
    A digest is a privacy problem only where it is a digest OF something personal.

    `apps/cms/locked_content.sha256.json` is full of 64-hex values and must stay that way: they are
    content-integrity hashes of this project's own prescribed texts, and the project computed them.
    The audit captures are the opposite — whatever they hold was computed by somebody else, from
    somebody's data — so the rule is scoped to that directory instead of applied repository-wide.
    """
    offenders: list[str] = []
    for path in sorted(CAPTURES.rglob("*")):
        if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in LONG_HEX.finditer(text):
            offenders.append(f"{path.relative_to(ROOT).as_posix()}: {match.group(0)[:16]}…")
    assert not offenders, "hex digests in the audit captures:\n" + "\n".join(offenders[:20])


def test_the_audit_still_reports_the_exposure():
    """Redaction must not have quietly deleted the finding it protects."""
    report = (ROOT / "docs" / "CURRENT_SITE_AUDIT.md").read_text(encoding="utf-8")
    assert "/wp-json/wp/v2/users" in report
    assert "REDATTO" in report
