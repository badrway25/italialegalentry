"""
Constants of the orientation platform.

* ``DISCLAIMER_VERSION`` — version stamp stored with every result. It identifies the wording of the
  disclaimer shown to the person (the locked ``p3.persons.how_it_works`` sentence + the informational
  banner). Bump it whenever that wording changes (new official transmission), never silently.
* ``PATHWAY_KEYS`` — the eight pathway keys come from the locked registry (``p3.persons.pathways``);
  ``NEEDS_INDIVIDUAL_ANALYSIS`` is the only additional outcome family.
"""

from __future__ import annotations

from cms import locked_content

DISCLAIMER_VERSION = "2026-09-17.1"
DISCLAIMER_KEY = "orientation.disclaimer"
# Logical disclaimer key → locked registry key. The text itself is NEVER stored: it is rendered
# through {% locked %} at display time.
DISCLAIMER_LOCKED_KEYS: dict[str, str] = {DISCLAIMER_KEY: "p3.persons.how_it_works"}

NEEDS_INDIVIDUAL_ANALYSIS = "needs_individual_analysis"


def locked_pathway_keys() -> tuple[str, ...]:
    entries, _lang = locked_content.get("p3.persons.pathways", "fr")
    return tuple(entry["key"] for entry in entries)


PATHWAY_KEYS: tuple[str, ...] = locked_pathway_keys()
OUTCOME_PATHWAY_KEYS: tuple[str, ...] = (*PATHWAY_KEYS, NEEDS_INDIVIDUAL_ANALYSIS)

ANONYMOUS_SESSION_TTL_DAYS = 30
RESUME_TOKEN_LENGTH = 64  # hex characters (32 random bytes)
MAX_SESSIONS_PER_BROWSER = 10

THROTTLE_SCOPE_START = "orientation_start"
THROTTLE_START_LIMIT = 20
THROTTLE_START_WINDOW_SECONDS = 600
THROTTLE_SCOPE_RESUME = "orientation_resume"
THROTTLE_RESUME_LIMIT = 10
THROTTLE_RESUME_WINDOW_SECONDS = 600

# Django session key holding the list of orientation session ids created by this browser.
BROWSER_SESSION_KEY = "orientation_sessions"
# Django session key holding the resume token revealed exactly once on the result page.
REVEAL_TOKEN_KEY = "orientation_reveal_token"  # noqa: S105 - not a secret value, a session key name

# Guard for the integrity validation: maximum number of answer paths explored.
MAX_VALIDATION_PATHS = 5000
