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

Once per space (V5.12 §4 «transitions into major platform contexts»; the Director's DECISIONS §1 T3). The release
plays again on the first page of each further space the session enters — the person's, the company's, the
organisation spaces as they come: ``consume_space_release`` keeps the spaces already lit in the session
(``LUME_SPACES_KEY``), and a new sign-in starts the list again with the space it lands in.
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

#: The session key of the spaces whose first page has already played the release in this session.
LUME_SPACES_KEY = "ile.lume_spaces"


def consume_space_release(request, space: str = "") -> bool:
    """
    True on the first console page after a successful sign-in, and on the first page of each further space of the
    session; False on every other page. ``space`` is the console's space key (``portal.services.SPACE_*``); without
    one only the sign-in's release counts. Nothing is written to the session on a page whose space is known.
    """
    session = getattr(request, "session", None)
    if session is None:
        return False
    entered = consume_entrance_release(request)
    if not space:
        return entered
    seen = [] if entered else list(session.get(LUME_SPACES_KEY, []))
    if space in seen:
        return False
    session[LUME_SPACES_KEY] = [*seen, space]
    return True
