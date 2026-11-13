"""
Forbidden public formulations (Implementation document §1.1–§1.3, §3.1, §3.9 and master brief §8).

``scan(text)`` returns the list of violations found in a rendered public page. The compliance
test-suite renders every public route in every language and asserts an empty result.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Exact phrases that must never appear on a public page (case-insensitive unless noted).
FORBIDDEN_PHRASES: tuple[str, ...] = (
    "Recruit in Morocco",
    "Find Qualified Profiles",
    "matching with Italian enterprises",
    "regulated enterprise matching",
    "Enterprise Area — Submit a Recruitment Request",
    "Submit a Recruitment Request",
    "positions or requested profiles",
    "Registered trademark",
    "Marque enregistrée",
    "Marchio registrato",
    "Cross the doorway to Italy",
    "A doorway, not a shortcut",
    "Digital Pathways to Italy",
    "Explore Italian Opportunities",
)

# Whole-word patterns (regex, case-insensitive).
FORBIDDEN_PATTERNS: tuple[tuple[str, str], ...] = (
    ("MATCHING", r"\bmatching\b"),
    ("@legalitalentry.it e-mail address", r"[A-Za-z0-9._%+-]+@legalitalentry\.it\b"),
    ("Google Analytics / gtag", r"google-analytics\.com|googletagmanager\.com|\bgtag\("),
    ("Meta Pixel", r"connect\.facebook\.net|\bfbq\("),
    ("Hotjar", r"hotjar\.com"),
    ("TikTok Pixel", r"analytics\.tiktok\.com"),
    ("Hostinger Reach", r"cdn-reach\.hostinger\.com"),
    ("Google Fonts hotlink", r"fonts\.googleapis\.com|fonts\.gstatic\.com"),
    ("Unsplash hotlink", r"images\.unsplash\.com"),
    ("Pexels hotlink", r"images\.pexels\.com"),
)

# Characters forbidden everywhere on public pages.
FORBIDDEN_CHARACTERS: tuple[tuple[str, str], ...] = (("® (registered mark)", "®"),)


@dataclass(frozen=True)
class Violation:
    label: str
    excerpt: str


def scan(text: str) -> list[Violation]:
    violations: list[Violation] = []
    lowered = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        idx = lowered.find(phrase.lower())
        if idx >= 0:
            violations.append(Violation(phrase, text[max(0, idx - 40) : idx + len(phrase) + 40]))
    for label, pattern in FORBIDDEN_PATTERNS:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            violations.append(Violation(label, text[max(0, m.start() - 40) : m.end() + 40]))
    for label, char in FORBIDDEN_CHARACTERS:
        idx = text.find(char)
        if idx >= 0:
            violations.append(Violation(label, text[max(0, idx - 40) : idx + 40]))
    return violations
