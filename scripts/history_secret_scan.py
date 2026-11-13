"""
Secret / PII scan over EVERY blob that has ever existed in the repository.

`git ls-files` sees the working tree. `git rev-list --objects --all` sees history, including blobs
whose path was deleted, renamed, or rewritten. Only the second answers "is this repository safe to
publish".

Reports one row per (blob, pattern, match). Binary blobs are reported by type and size only -- a
PNG cannot be grepped for an address, and a scanner that claims it did is lying.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\tmp\italylegalentry")

RESERVED_TLDS = (".test", ".invalid", ".example", ".localhost")
ALLOWED_DOMAINS = (
    "agamieuromed.org",
    "example.com",
    "example.org",
    "legalitalentry.it",
    "legalitalentry.com",
    "azienda.it",
    "sentry.io",
    "anthropic.com",
    "w3.org",
    "djangoproject.com",
    "python.org",
    "github.com",
    "mozilla.org",
    "googleapis.com",
    "gstatic.com",
    "jsdelivr.net",
    "unpkg.com",
    "cloudflare.com",
    "schema.org",
    "gnu.org",
    "postgresql.org",
    "docker.com",
    "openstreetmap.org",
    "europa.eu",
    "gazzettaufficiale.it",
    "normattiva.it",
    "esteri.it",
    "interno.it",
    "lavoro.gov.it",
    "miur.it",
    "mise.gov.it",
    "wordpress.org",
    "gravatar.com",
    "litespeedtech.com",
    "hostinger.com",
    "dadapro.com",
)

PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "third-party e-mail address"),
    ("phone_intl", re.compile(r"(?<![\w.])\+\d{1,3}[\s.\-]?\(?\d{1,4}\)?(?:[\s.\-]?\d{2,4}){2,4}(?![\w.])"), "international telephone number"),
    ("phone_ma", re.compile(r"(?<![\w.])0[567]\d{8}(?![\w.])"), "Moroccan national-format mobile"),
    ("aws_key", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"), "AWS access key id"),
    ("private_key", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY"), "private key block"),
    ("gh_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"), "GitHub token"),
    ("slack_token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"), "Slack token"),
    ("google_key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), "Google API key"),
    ("stripe_key", re.compile(r"\b[sr]k_(live|test)_[0-9A-Za-z]{16,}\b"), "Stripe key"),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"), "JSON Web Token"),
    ("secret_assign", re.compile(
        r"(?i)\b(secret_key|api_key|apikey|access_token|auth_token|client_secret|password|passwd|pwd|token)\b"
        r"\s*[:=]\s*[\x27\"][^\x27\"\n]{8,}[\x27\"]"), "assigned credential literal"),
    ("db_url_pw", re.compile(r"\b(?:postgres|postgresql|mysql|mongodb|redis|amqp)(?:\+\w+)?://[^\s:/@]+:[^\s:/@]+@"), "connection URL carrying a password"),
    ("hex64", re.compile(r"\b[0-9a-f]{64}\b"), "64-hex value (digest)"),
    ("id_document", re.compile(r"(?i)\b(carte\s+nationale\s+d|CNIE|passeport\s+n|passaporto\s+n|numero\s+di\s+passaporto)\b"), "identity-document reference"),
    ("codice_fiscale", re.compile(r"(?<![A-Z0-9])[A-Z]{6}\d{2}[A-EHLMPR-T]\d{2}[A-Z]\d{3}[A-Z](?![A-Z0-9])"), "Italian codice fiscale shape"),
    ("iban", re.compile(r"\b(?:IT|FR|MA|DE|ES|BE|NL)\d{2}[A-Z0-9]{11,28}\b"), "IBAN shape"),
]

AUDIT_CAPTURE = ("docs/audit/current-site/raw/", "docs/audit/current-site/screenshots/")
SELF_REFERENTIAL_PREFIXES = ("scripts/",)
SELF_REFERENTIAL_EXACT = (
    "tests/compliance/test_no_personal_data_in_repository.py",
    "apps/cms/forbidden.py",
)

TEXT_SUFFIXES = {
    ".py", ".html", ".css", ".js", ".md", ".po", ".txt", ".json", ".yml", ".yaml",
    ".toml", ".cfg", ".ini", ".headers", ".xml", ".svg", ".sh", ".example", ".gitignore",
    ".gitattributes", "", ".lock", ".csv", ".dockerfile",
}


def all_blobs() -> dict:
    out = defaultdict(set)
    proc = subprocess.run(
        ["git", "rev-list", "--objects", "--all"], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=True,
    )
    for line in proc.stdout.splitlines():
        sha, _, path = line.partition(" ")
        if path:
            out[sha].add(path)
    return out


def is_allowed_email(value: str) -> bool:
    domain = value.rsplit("@", 1)[1].lower().rstrip(".")
    return domain.endswith(RESERVED_TLDS) or domain.endswith(ALLOWED_DOMAINS)


def main() -> int:
    blobs = all_blobs()
    sizes = {}
    proc = subprocess.run(
        ["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
        cwd=ROOT, input="\n".join(blobs) + "\n",
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[1] == "blob":
            sizes[parts[0]] = int(parts[2])

    findings, binaries = [], []
    scanned = skipped = 0

    for sha, paths in blobs.items():
        if sha not in sizes:
            continue
        sample = sorted(paths)[0]
        suffix = Path(sample).suffix.lower()
        raw = subprocess.run(["git", "cat-file", "-p", sha], cwd=ROOT, capture_output=True, check=False).stdout
        if raw is None:
            continue
        if b"\x00" in raw[:8192] or suffix not in TEXT_SUFFIXES:
            binaries.append({"sha": sha, "paths": sorted(paths), "bytes": sizes[sha], "suffix": suffix})
            skipped += 1
            continue

        text = raw.decode("utf-8", errors="replace")
        scanned += 1
        self_ref = any(
            p in SELF_REFERENTIAL_EXACT or p.startswith(SELF_REFERENTIAL_PREFIXES) for p in paths
        )
        is_capture = any(p.startswith(AUDIT_CAPTURE) for p in paths)

        for name, pattern, label in PATTERNS:
            for m in pattern.finditer(text):
                value = m.group(0)
                if name == "email" and is_allowed_email(value):
                    continue
                findings.append({
                    "sha": sha,
                    "paths": sorted(paths),
                    "pattern": name,
                    "label": label,
                    "value": value[:120],
                    "line": text.count("\n", 0, m.start()) + 1,
                    "self_referential": self_ref,
                    "is_audit_capture": is_capture,
                })

    report = {
        "blobs_total": len(blobs),
        "blobs_text_scanned": scanned,
        "blobs_binary_not_scanned": skipped,
        "findings": findings,
        "binaries": binaries,
    }
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("history_scan.json")
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")

    by_pattern = defaultdict(int)
    for f in findings:
        by_pattern[f["pattern"]] += 1
    print(f"blobs: {len(blobs)}   text scanned: {scanned}   binary (not grep-able): {skipped}")
    print(f"findings: {len(findings)}")
    for name, count in sorted(by_pattern.items(), key=lambda kv: -kv[1]):
        print(f"  {name:16s} {count}")
    print(f"report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
