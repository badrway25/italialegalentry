"""
Local conftest: re-exports the project-wide fixtures of ``tests/conftest.py`` so the FAQ suite can
run standalone (``pytest apps/faq``) with the same ``seeded`` / ``phase3_open`` / ``superuser`` …
fixtures used by the compliance suite.
"""

from tests.conftest import (  # noqa: F401
    _clear_caches,
    before_phase3,
    client_ar,
    client_fr,
    legal_published,
    person_user,
    phase3_open,
    seeded,
    set_flag,
    staff_user,
    superuser,
    url,
    user_factory,
)
