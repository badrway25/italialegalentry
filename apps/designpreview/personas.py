"""
The persona switch — how the owner reaches the authenticated pages without a password (V5.4 plan
§4.4). DEVELOPMENT ONLY.

``POST /__design-v5/accedi/<persona>/`` signs this browser in as one of the preview database's QA
accounts; ``POST /__design-v5/esci/`` signs it out. No password is ever typed, sent or stored: the
session is minted by ``django.contrib.auth.login`` for an account the database already holds.

**Allowed only when all hold** — the views say 404 otherwise, 405 to anything but a POST, 403 to a
POST without its CSRF token:

* DEBUG and ``ILE_DESIGN_PREVIEW=1``; a loopback caller with no proxy header; this process's own
  ``Host`` (``designpreview.access``);
* the persona is a key of ``ILE_DESIGN_PREVIEW_PERSONAS`` (dev.py: the four QA accounts, by e-mail);
* the account exists, is active, and is neither staff nor superuser — a staff session is never
  minted, whatever the allow-list says;
* the account holds no role but a person's or a company's, and no permission of its own. In this
  codebase a privilege is a group, independent of ``is_staff`` — an operator handles case files, a
  moderator moderates (apps/accounts/roles.py) — and a session minted without a password never
  carries one (review W1-P, security m4; DL54-18, stricter than the letter of plan §4.4);
* the database is named in ``ILE_DESIGN_PREVIEW_ALLOWED_DATABASES`` (``ile_v5`` and the lane clones)
  and is not one of the V4 control's (``ile``, ``ile_qa``) — refused even if a setting names it.

**What the sign-in does.** ``auth.login(request, user, backend=ModelBackend)``: it sends
``user_logged_in``, so the audit trail records the sign-in and the entrance plays as after a real
one. One log line, carrying the persona key — never the e-mail (tests/security/test_log_privacy.py).
Whatever a request chose — its method, its path — reaches a log line escaped
(``designpreview.access.loggable``): a path cannot write a second, forged line (review W1-P,
security m2).

**Read-only.** A session opened here carries ``SESSION_KEY``. While it is set,
``PersonaReadOnlyMiddleware`` answers 403 to every unsafe method (POST, PUT, PATCH, DELETE …)
outside ``/__design-v5/``, except signing out and the language switch: a persona never drifts —
accepting the terms as ``qa-person`` would destroy that persona for everyone who looks after.
Flows that write are shown by the lanes on their own clones, and through the states (``?état=``).
The refusal is a few sentences in plain text that a frame of this origin may show
(designpreview.frames): what was not done, and the way back.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db import connections
from django.http import Http404, HttpResponse
from django.urls import Resolver404, resolve

from designpreview import access, frames

log = logging.getLogger("ile.designpreview")

#: The session flag that makes a session a persona's — and read-only.
SESSION_KEY = "ile_design_preview_persona"
#: The backend the switch signs in with — the first of AUTHENTICATION_BACKENDS (base.py).
BACKEND = "django.contrib.auth.backends.ModelBackend"
#: The V4 control's databases (8770 and 8772 on ``ile``, 8771 on ``ile_qa``): never, whatever a setting says.
V4_CONTROL_DATABASES = frozenset({"ile", "ile_qa"})
#: Where a persona session may still write: the preview's own routes (the switch itself).
PREVIEW_PREFIX = "/__design-v5/"
#: The views a persona session may still POST to: signing out, and the language switch.
WRITABLE_VIEWS = frozenset({"account_logout", "set_language"})
SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
#: The only roles a persona may hold (apps/accounts/roles.py: PERSON, COMPANY). Any other group is a
#: privilege, and a session minted without a password never carries one.
PERSONA_ROLES = frozenset({"role:person", "role:company"})


class Refused(Exception):
    """A persona the switch will not open here — said to the caller in plain words, logged without an e-mail."""

    def __init__(self, reason: str, sentence: str):
        super().__init__(reason)
        self.reason = reason
        self.sentence = sentence


@dataclass(frozen=True)
class Persona:
    key: str
    name: str  #: as the plan names it, in French — the product's language
    note: str  #: what the account is, in Italian — the preview's language
    home: str  #: the URL name of its first page
    case: str = ""  #: its case file, when it has one


#: The four QA accounts of the preview's database (plan §4.1), in the order the index shows them.
#: The e-mails are not here: they are the allow-list, in the preview block of dev.py.
PERSONAS: dict[str, Persona] = {
    persona.key: persona
    for persona in (
        Persona(
            "qa-doc-person",
            "Personne avec dossier",
            "Una persona con il suo fascicolo e le condizioni d’uso accettate.",
            "portal:dashboard",
            "EE167596D4",
        ),
        Persona(
            "qa-person",
            "Personne, conditions non acceptées",
            "Una persona con un fascicolo e le condizioni d’uso non ancora accettate: le pagine chiedono di "
            "accettare le condizioni.",
            "portal:dashboard",
            "E46E03B461",
        ),
        Persona(
            "qa-fresh-person",
            "Personne sans dossier",
            "Una persona appena registrata, senza fascicolo: ogni riquadro vuoto dice che cosa fare.",
            "portal:dashboard",
        ),
        Persona(
            "qa-company",
            "Entreprise — Cantiere Adriatico",
            "L’impresa Cantiere Adriatico S.r.l., con i suoi bisogni in stati diversi.",
            "companies:dashboard",
        ),
    )
}


def allow_list() -> dict[str, str]:
    """Persona key → e-mail, from the preview block of dev.py."""
    return dict(getattr(settings, "ILE_DESIGN_PREVIEW_PERSONAS", {}) or {})


def database_name(alias: str = "default") -> str:
    return str(connections[alias].settings_dict.get("NAME", "") or "")


def database_allowed(name: str) -> bool:
    allowed = set(getattr(settings, "ILE_DESIGN_PREVIEW_ALLOWED_DATABASES", ()) or ())
    return name in allowed and name not in V4_CONTROL_DATABASES


def current(request) -> str:
    """The persona key of this session, or ""."""
    session = getattr(request, "session", None)
    if session is None:
        return ""
    return str(session.get(SESSION_KEY, "") or "")


def enter(request, key: str) -> Persona:
    """Sign ``request`` in as the persona ``key``, or raise ``Http404`` (not a persona) / ``Refused``."""
    emails = allow_list()
    if key not in emails or key not in PERSONAS:
        raise Http404
    name = database_name()
    if not database_allowed(name):
        _refuse(
            key,
            "database",
            f"Persona rifiutata: questo server usa il database «{name}», che non è fra quelli dell’anteprima "
            "(soltanto il database dell’anteprima e le sue copie, ILE_DESIGN_PREVIEW_ALLOWED_DATABASES — mai "
            "ile_qa né ile, i database del controllo V4).",
        )
    user = get_user_model().objects.filter(email__iexact=emails[key]).first()
    if user is None or not user.is_active:
        _refuse(key, "unknown", f"Persona rifiutata: nessun account attivo per «{key}» su questo database.")
    if user.is_staff or user.is_superuser:
        _refuse(
            key,
            "staff",
            f"Persona rifiutata: l’account di «{key}» è dello staff, e l’anteprima non apre mai una sessione "
            "dello staff.",
        )
    roles = set(user.groups.values_list("name", flat=True))
    if not roles <= PERSONA_ROLES or user.user_permissions.exists():
        _refuse(
            key,
            "privileged",
            f"Persona rifiutata: l’account di «{key}» ha un ruolo o un permesso che una persona di prova non ha "
            "(un operatore, un moderatore, una redazione …), e l’anteprima non apre mai una sessione con "
            "privilegi.",
        )
    auth.login(request, user, backend=BACKEND)
    request.session[SESSION_KEY] = key
    log.info("Design preview: persona %s signed in (read-only session).", key)
    return PERSONAS[key]


def leave(request) -> str:
    """Sign this browser out, whoever it was; the persona key it had, or ""."""
    key = current(request)
    auth.logout(request)
    log.info("Design preview: persona %s signed out.", key or "-")
    return key


def _refuse(key: str, reason: str, sentence: str):
    log.warning("Design preview: persona %s refused (%s).", key, reason)
    raise Refused(reason, sentence)


def refusal(request, persona: str) -> HttpResponse:
    """The 403 a read-only persona meets: what was not done, and the way back, in plain words."""
    name = PERSONAS[persona].name if persona in PERSONAS else "la persona"
    text = (
        "Anteprima V5 — sola lettura.\n\n"
        f"Questa azione non è stata eseguita, e nulla è cambiato: «{name}» resta uguale per chi guarda dopo.\n\n"
        "Per tornare alla pagina: «Indietro» del browser. Per uscire dalla persona: «Sortir», nella barra in "
        "alto.\n"
    )
    response = HttpResponse(text, status=403, content_type="text/plain; charset=utf-8")
    response["Cache-Control"] = "no-store"
    response["X-Robots-Tag"] = "noindex, nofollow"
    # The frame's one predicate, method included: a framed POST shows the refusal, a framed PUT,
    # PATCH or DELETE keeps the normal policy (review W1-P, security m6).
    if frames.framed_by_this_origin(request):
        frames.relax(response)
    return response


def _view_name(request) -> str:
    try:
        return resolve(request.path_info).view_name
    except Resolver404:
        return ""


class PersonaReadOnlyMiddleware:
    """
    403 to every unsafe method of a persona session outside ``/__design-v5/``, signing out and the
    language switch excepted. Installed by the preview block of dev.py, at the end of the chain —
    after the session and the locale have been read, before any view.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method not in SAFE_METHODS and not request.path_info.startswith(PREVIEW_PREFIX):
            persona = current(request)
            if persona and _view_name(request) not in WRITABLE_VIEWS:
                log.info(
                    "Design preview: persona %s, %s %s refused (read-only).",
                    access.loggable(persona),
                    access.loggable(request.method),
                    access.loggable(request.path),
                )
                return refusal(request, persona)
        return self.get_response(request)
