"""
Signals emitted by the accounts domain so that other apps can react without accounts importing them
(documents purges the user's private files, community could scrub a participant profile, ...).

``user_anonymised`` — sent *inside* the anonymisation transaction with ``user`` (already scrubbed)
and ``user_id``. Receivers must be idempotent and must never re-introduce personal data.
"""

from django.dispatch import Signal

user_anonymised = Signal()
