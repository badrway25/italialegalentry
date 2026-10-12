"""
Signals emitted by the accounts domain so that other apps can react without accounts importing them
(documents purges the user's private files, community could scrub a participant profile, ...).

``user_anonymised`` — sent *inside* the anonymisation transaction with ``user`` (already scrubbed)
and ``user_id``. Receivers must be idempotent and must never re-introduce personal data.

The entrance release (design V5, V5.4 plan §1.9; DL54-07; W1-D). The loader «Lume» is one movement split
by the navigation: on the login's submit the key turns and holds; on the first console page after a
*successful* sign-in the lit doorway plays once, on the rail's mark. The page cannot know on its own that
it is that page, so Django's ``user_logged_in`` — sent by allauth's sign-in, by ``Client.force_login`` and
by the preview's persona switch alike — leaves a flag in the new session (``mark_entrance_release``), and
the first console page consumes it, once, through ``{% entrance_release %}`` (accounts.templatetags.entrance
→ ``consume_entrance_release``). A refused sign-in never sends the signal, so the light says «it is open»
only when it is (RTD-M6); a page reloaded or revisited finds the flag gone. The receiver is connected in
``AccountsConfig.ready`` with a ``dispatch_uid``, as the audit trail connects its own.
"""

from django.dispatch import Signal

user_anonymised = Signal()

#: The session key of the entrance release: present between a successful sign-in and the first console page.
ENTRANCE_RELEASE_KEY = "ile.entrance_release"


def mark_entrance_release(sender, request, user, **kwargs) -> None:
    """``user_logged_in`` receiver: the next console page this session renders plays the entrance release."""
    session = getattr(request, "session", None)
    if session is not None:
        session[ENTRANCE_RELEASE_KEY] = True


def consume_entrance_release(request) -> bool:
    """True once per sign-in: the flag is removed as it is read, so the release never plays twice."""
    session = getattr(request, "session", None)
    if session is None:
        return False
    return bool(session.pop(ENTRANCE_RELEASE_KEY, False))
