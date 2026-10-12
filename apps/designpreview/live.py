"""
What the live V5 product shows around the real pages — the strip of ``/__design-v5/`` and the
index one click away (V5.4 plan §4.1). DEVELOPMENT ONLY.

The preview stopped being a catalogue of options on 4 October 2026 (the owner's directive V5.4,
«EXECUTION MODE»): ``/__design-v5/`` opens the real ``/fr/`` page of this very server — the current
best V5 — full window, in one same-origin frame, under a slim strip that sits outside the page.
The catalogue moved, as it was, to ``/__design-v5/research/`` (designpreview.services).

Six things live here and nowhere else:

1. **The pages** (``PUBLIC_PAGES``, ``PERSONA_PAGES``, ``STATE_PAGES``, ``STATE_KEYS``,
   ``OUTSIDE``): every page type of W1-0's census — the before set of V5.4,
   ``C:/tmp/ile_v5_council/evidence/v54/w1-0/before/PAGE_TYPES.json``, 79 types — one row each, by
   its URL name, so that a path that changes in a later wave changes here by itself; a detail page
   by the census's own example; with the languages it is reviewed in: fr and ar everywhere, it and
   en as well for the home and the login (§4.1). A page's **surface key is its census id**: the
   steward marks a page type «v5», and every page of that type follows — the five legal texts share
   one template and one key, and so do the institutions' and the universities' proposal forms. The
   four types only a role account reaches stand apart (``OUTSIDE``): the preview has no persona for
   those roles (review W1-P M2).
2. **The state of a surface** (``live_status()``, ``state_of()``): «V5 — council-passed» only where
   the steward's ``live_status.json`` says so for that surface's key; «V4 + fondation» everywhere
   else, and everywhere when the file is absent or unreadable. The preview only reads the file —
   the steward alone writes it (``docs/design-v5/OWNERSHIP_V54.json``, ``steward_only``) — and
   never claims a pass the steward has not written.
3. **What the strip says about the build** (``identity()``): the tag this worktree is checked out
   at — on 8780, the v5-live tag — its commit and its date, read from git once per process (8780
   is restarted after every checkout).
4. **«Changed since the last report»** (``changelog()``): the first three entries of the steward's
   ``docs/design-v5/CHANGELOG_V54.md``, opened on demand.
5. **The page a frame may hold** (``page_param()``): a path of this site under a language prefix,
   or under ``/documents/`` (the documents app is mounted without one: its language is the language
   cookie's) — never another origin, never a scheme, never a dot segment, never the preview itself.
6. **The V4 control** (``v4_origin()``): the same URLs on 8771 (main, phase 3) — never on this
   server, which serves V5.

**The schema of ``live_status.json``** (``ile-live-status-v54/1``) — what the steward writes and
the preview reads::

    {
      "schema": "ile-live-status-v54/1",
      "updated": "2026-10-06",
      "families": [
        {"key": "w1-a", "title": "…", "state": "v5" | "v4-fondation",
         "scores": {"visual": 4, "premium": 4, "originality": 4, "ux": 4, "mobile": 4, "coherence": 4},
         "decision": "w1-a/CD_DECISION.md", "tag": "v54/w1-a", "date": "2026-10-06"}
      ],
      "surfaces": {"home": "v4-fondation", "login": "v5", "dashboard-person": "v5", …}
    }

``surfaces`` is keyed by the census ids (``surface_keys()``; the index lists them for the steward);
a value is a state, or an object with a ``state``. ``decision`` is relative to
``docs/design-v5/QA/v54/`` and is served as text by the preview (``/__design-v5/decisioni/<path>``).
Anything malformed reads as «V4 + fondation».
"""

from __future__ import annotations

import datetime
import functools
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlencode, urlsplit

from django.conf import settings
from django.urls import NoReverseMatch, reverse
from django.utils import translation

from designpreview import access

# ---------------------------------------------------------------------------------------------
# Languages and states
# ---------------------------------------------------------------------------------------------

LANGS_ALL: tuple[str, ...] = ("fr", "ar", "it", "en")
LANGS_PRIMARY: tuple[str, ...] = ("fr", "ar")
#: The languages named in Italian, the preview's language: the tooltips, and the words a screen
#: reader hears after a link that shows only «fr» or «ar» (review W1-P, accessibility m6, m7).
LANG_NAMES = {"fr": "Francese", "ar": "Arabo", "it": "Italiano", "en": "Inglese"}

STATE_V5 = "v5"
STATE_V4 = "v4-fondation"
#: The two states, in the plan's words (§4.1): a surface is one or the other.
STATE_LABELS = {STATE_V5: "V5 — council-passed", STATE_V4: "V4 + fondation"}

#: The frames the strip offers: the window itself, and a phone of 390 CSS pixels.
FRAMES = ("desktop", "phone")

# ---------------------------------------------------------------------------------------------
# The pages — W1-0's census, one row per page type
# ---------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Page:
    slug: str  #: the row's own name, unique in its list: its anchor in the index (``#p-<slug>``)
    title: str
    url_name: str
    kwargs: tuple[tuple[str, str], ...] = ()
    langs: tuple[str, ...] = LANGS_PRIMARY
    group: str = ""  #: the heading it stands under in the index (public pages)
    key: str = ""  #: its surface key: W1-0's census id of its page type («» = the slug)
    query: str = ""  #: the query string of the census's example (``k=contact``)
    note: str = ""  #: what the page is, where its title does not say it (a 403, a closed module)
    path: str = ""  #: a path under the language prefix, for a state that has no URL name (the 404)

    @property
    def surface(self) -> str:
        return self.key or self.slug


_ACCOUNT = "Ingresso e account"
_DOORS = "Gli accessi"
_PROJECT = "Il progetto"
_PATHS = "Percorsi e orientamento"
_INFO = "Vivere in Italia, notizie, comunità"
_FORMS = "Contatti e moduli"
_LEGAL = "Testi legali"

#: Every public page type, in the order the index lists them.
PUBLIC_PAGES: tuple[Page, ...] = (
    Page("home", "La home", "pages:home", langs=LANGS_ALL, group=_ACCOUNT, key="home"),
    Page("login", "L’accesso «Il varco»", "account_login", langs=LANGS_ALL, group=_ACCOUNT, key="login"),
    Page("signup", "La registrazione", "account_signup", group=_ACCOUNT, key="signup"),
    Page("password-reset", "La password dimenticata", "account_reset_password", group=_ACCOUNT, key="password-reset"),
    Page(
        "password-reset-done",
        "La password dimenticata — e-mail inviata",
        "account_reset_password_done",
        group=_ACCOUNT,
        key="password-reset-done",
    ),
    Page(
        "email-verification-sent",
        "La verifica dell’indirizzo — e-mail inviata",
        "account_email_verification_sent",
        group=_ACCOUNT,
        key="email-verification-sent",
    ),
    Page("pathways", "Persone — i percorsi", "pathways:index", group=_DOORS, key="door-persons"),
    Page("companies", "Imprese", "ecosystem:companies", group=_DOORS, key="door-companies"),
    Page("institutions", "Istituzioni", "ecosystem:institutions", group=_DOORS, key="door-institutions"),
    Page("universities", "Università e formazione", "ecosystem:universities", group=_DOORS, key="door-universities"),
    Page("forum", "Il Forum", "forum:index", group=_DOORS, key="door-forum"),
    Page("project", "Il progetto", "pages:project", group=_PROJECT, key="project"),
    Page("pilot", "Il progetto pilota", "ecosystem:pilot", group=_PROJECT, key="project-pilot"),
    Page("agami", "AGAMI", "pages:agami", group=_PROJECT, key="project-agami"),
    Page("network", "La rete", "pages:network", group=_PROJECT, key="project-network"),
    Page("antifraud", "Attenzione alle frodi", "pages:antifraud", group=_PROJECT, key="antifraud"),
    Page("orientation", "Il questionario di orientamento", "orientation:start", group=_PATHS, key="orientation-start"),
    Page(
        "orientation-resume",
        "Il questionario — riprendere con un codice",
        "orientation:resume",
        group=_PATHS,
        key="orientation-resume",
    ),
    Page(
        "pathway-detail",
        "Un percorso — il lavoro subordinato",
        "pathways:detail",
        (("key", "salaried_work"),),
        group=_PATHS,
        key="pathway-detail",
    ),
    Page("diplomas", "Diplomi e titoli", "pathways:diplomas", group=_PATHS, key="diplomas"),
    Page("training", "La formazione", "pathways:training", group=_PATHS, key="training"),
    Page("living", "Vivere in Italia", "living:index", group=_INFO, key="living-index"),
    Page(
        "living-topic",
        "Vivere in Italia — l’alloggio",
        "living:topic",
        (("slug", "logement"),),
        group=_INFO,
        key="living-topic",
    ),
    Page("news", "Le notizie", "news:index", group=_INFO, key="news-index"),
    Page("faq", "Le domande frequenti", "faq:index", group=_INFO, key="faq"),
    Page("glossary", "Il glossario", "glossary:index", group=_INFO, key="glossary-index"),
    Page(
        "glossary-term",
        "Il glossario — il permesso di soggiorno",
        "glossary:term",
        (("slug", "permesso_di_soggiorno"),),
        group=_INFO,
        key="glossary-term",
    ),
    Page("partners", "I partner", "partners:index", group=_INFO, key="partners"),
    # Not in the census: every path of the virtual forum answers 404 while its module is closed.
    Page(
        "community",
        "Il forum virtuale",
        "community:index",
        group=_INFO,
        note="404 finché il forum virtuale è chiuso (in sviluppo: la pagina tecnica di Django)",
    ),
    Page("contact", "Contatti", "pages:contact", group=_FORMS, key="contact"),
    Page("contact-form", "Il modulo di contatto", "enquiries:contact", group=_FORMS, key="contact-form"),
    Page(
        "company-needs",
        "Il modulo dei bisogni dell’impresa",
        "enquiries:company_needs",
        group=_FORMS,
        key="enquiry-company-needs",
    ),
    Page(
        "institution-proposal",
        "Il modulo delle istituzioni",
        "enquiries:institution_proposal",
        group=_FORMS,
        key="enquiry-collaboration",
    ),
    Page(
        "university-proposal",
        "Il modulo delle università",
        "enquiries:university_proposal",
        group=_FORMS,
        key="enquiry-collaboration",
    ),
    Page("enquiry-done", "La domanda trasmessa", "enquiries:done", group=_FORMS, key="enquiry-done", query="k=contact"),
    Page("forum-register", "L’iscrizione al Forum", "forum:register", group=_FORMS, key="forum-register"),
    Page("privacy", "Privacy", "legal:privacy", group=_LEGAL, key="legal-document"),
    Page("cookies", "Cookie", "legal:cookies", group=_LEGAL, key="legal-document"),
    Page("notices", "Note legali", "legal:notices", group=_LEGAL, key="legal-document"),
    Page("terms", "Condizioni d’uso", "legal:terms", group=_LEGAL, key="legal-document"),
    Page("disclaimer", "Avvertenze", "legal:disclaimer", group=_LEGAL, key="legal-document"),
)

# The census's examples of the detail pages, on the preview's database and its clones (ile_v5 and
# ile_v5_l3 … l9 are template copies of one another: the same rows, the same ids).
_REQUIREMENT = "70d79bd5-9917-468f-abaf-6ec44669abb4"
_TICKET = "4262f0d4-1396-4f63-a690-a2b8e9c27ad4"
_ENROLMENT = "32589170-cc35-4fda-984f-edabf4d3f30f"

#: The pages of each persona (designpreview.personas.PERSONAS), in fr and ar — each page type under
#: the persona the census captured it with. Named as the product names them, in French.
PERSONA_PAGES: dict[str, tuple[Page, ...]] = {
    "qa-doc-person": (
        Page("dashboard", "Tableau de bord", "portal:dashboard", key="dashboard-person"),
        Page("cases", "Mes dossiers", "cases:index", key="cases-index"),
        Page("case", "Le dossier EE167596D4", "cases:detail", (("reference", "EE167596D4"),), key="case-file"),
        Page("documents", "Mes pièces", "portal:documents", key="documents-portal"),
        Page("documents-app", "Mes pièces — /documents/", "documents:index", key="documents"),
        Page(
            "document-requirement",
            "Pièce demandée",
            "documents:requirement",
            (("pk", _REQUIREMENT),),
            key="document-requirement",
        ),
        Page("document-upload", "Déposer un fichier", "documents:upload", key="document-upload"),
        Page("situation", "Ma situation", "portal:situation", key="situation"),
        Page("requests", "Mes demandes", "portal:requests", key="requests"),
        Page("journey", "Mon parcours", "portal:pathways", key="journey", note="senza pre-valutazione: lo stato vuoto"),
        Page("deadlines", "Mes échéances", "portal:deadlines", key="deadlines"),
        Page("messages", "Communications", "portal:messages", key="messages"),
        Page("academy", "Academy — le catalogue", "academy:catalogue", key="academy-catalogue"),
        Page(
            "academy-course",
            "Academy — le cours Italien A1",
            "academy:course",
            (("slug", "italien-a1"),),
            key="academy-course",
        ),
        Page("profile", "Profil", "accounts:profile", key="account-profile"),
        Page("account-email", "Adresses e-mail", "account_email", key="account-email"),
        Page("account-password", "Mot de passe", "account_change_password", key="account-password-change"),
        Page("account-mfa", "Sécurité du compte", "mfa_index", key="account-mfa"),
        Page("account-delete", "Supprimer mon compte", "accounts:delete_request", key="account-delete"),
        Page("logout", "Se déconnecter", "account_logout", key="logout-confirm", note="la pagina di conferma"),
    ),
    "qa-person": (
        Page(
            "dashboard",
            "Tableau de bord",
            "portal:dashboard",
            key="dashboard-person-terms-pending",
            note="condizioni non accettate",
        ),
        Page("case", "Le dossier E46E03B461", "cases:detail", (("reference", "E46E03B461"),), key="case-file"),
        Page("documents", "Mes pièces", "portal:documents", key="documents-portal"),
        Page(
            "document-upload",
            "Déposer un fichier",
            "documents:upload",
            key="document-upload-terms-required",
            note="403 per questa persona: le condizioni non sono accettate",
        ),
        Page("situation", "Ma situation", "portal:situation", key="situation"),
        Page("requests", "Mes demandes", "portal:requests", key="requests"),
        Page(
            "request-detail",
            "Mes demandes — une demande",
            "portal:request_detail",
            (("kind", "contact"), ("pk", "1")),
            key="request-detail",
        ),
        Page("journey", "Mon parcours", "portal:pathways", key="journey-results", note="con una pre-valutazione"),
        Page("deadlines", "Mes échéances", "portal:deadlines", key="deadlines"),
        Page("messages", "Communications", "portal:messages", key="messages"),
        Page("helpdesk", "Guichet numérique", "helpdesk:requests", key="helpdesk"),
        Page(
            "helpdesk-detail",
            "Guichet numérique — une demande",
            "helpdesk:detail",
            (("uuid", _TICKET),),
            key="helpdesk-detail",
        ),
        Page("helpdesk-new", "Guichet numérique — ouvrir une demande", "helpdesk:open", key="helpdesk-new"),
        Page("academy-mine", "Mes formations", "academy:mine", key="academy-mine"),
        Page(
            "academy-enrolment",
            "Mes formations — un suivi",
            "academy:enrolment",
            (("uuid", _ENROLMENT),),
            key="academy-enrolment",
        ),
        Page("profile", "Profil", "accounts:profile", key="account-profile"),
    ),
    "qa-fresh-person": (
        Page(
            "dashboard",
            "Tableau de bord",
            "portal:dashboard",
            key="dashboard-person-empty",
            note="senza fascicolo: gli stati vuoti",
        ),
        Page("documents", "Mes pièces", "portal:documents", key="documents-portal"),
        Page("situation", "Ma situation", "portal:situation", key="situation"),
        Page("profile", "Profil", "accounts:profile", key="account-profile"),
    ),
    "qa-company": (
        Page("company", "Espace entreprise", "companies:dashboard", key="company-dashboard"),
        Page("company-profile", "Mon entreprise", "companies:profile", key="company-profile"),
        Page("company-needs-list", "Mes besoins", "companies:needs", key="company-needs"),
        Page("company-need-form", "Nouveau besoin", "companies:need_create", key="company-need-form"),
        Page(
            "org-bridge", "Espace réservé", "portal:dashboard", key="org-bridge", note="il ponte delle organizzazioni"
        ),
        Page(
            "company-analysis",
            "Analyse territoriale",
            "companies:analysis",
            key="error-403",
            note="403 per questa impresa: la pagina d’errore",
        ),
        Page("profile", "Profil", "accounts:profile", key="account-profile"),
    ),
}

#: The census's states that have an address, which the strip names like a page: the census's
#: example of a 404, and a step of the questionnaire — its address carries the anonymous session,
#: so the strip matches it as a pattern (``_patterns``).
STATE_PAGES: tuple[Page, ...] = (
    Page("error-404", "La pagina 404", "", key="error-404", path="/page-inexistante/"),
    Page(
        "orientation-step",
        "Il questionario — un passo",
        "orientation:step",
        (("session_id", "00000000-0000-0000-0000-000000000000"),),
        key="orientation-step",
    ),
)

#: The census's states the index names under «Stati senza credenziali» (plan §4.5): the home with
#: its menu open, a step of the questionnaire (the answer to «Commencer»), the 404, the 410 of an
#: old WordPress address, the 403 (qa-company's «Analyse territoriale»).
STATE_KEYS: tuple[str, ...] = ("navbar-open", "orientation-step", "error-404", "error-410", "error-403")

#: The census's page types that no persona of the preview reaches: each needs a role account (the
#: census's demo-* accounts), and the preview offers none — «fuori dall’anteprima».
OUTSIDE: tuple[tuple[str, str, str], ...] = (
    ("helpdesk-queue", "La coda del Guichet numérique", "un professionista"),
    ("helpdesk-dispatch", "La designazione dei professionisti", "un operatore"),
    ("selection-workspace", "Lo spazio della selezione", "un attore autorizzato"),
    ("console-unavailable", "Il Forum permanente, chiuso (503)", "un professionista"),
)


def url_of(page: Page, lang: str) -> str:
    """The real URL of ``page`` in ``lang`` — with the census's query string — or "" if its name no longer resolves."""
    if page.path:
        return f"/{lang}{page.path}"
    with translation.override(lang):
        try:
            url = reverse(page.url_name, kwargs=dict(page.kwargs) or None)
        except NoReverseMatch:
            return ""
    return f"{url}?{page.query}" if page.query else url


def public_url(slug: str, lang: str) -> str:
    """The URL of the public page ``slug`` in ``lang`` — or "" if there is no such page."""
    page = next((page for page in PUBLIC_PAGES if page.slug == slug), None)
    return url_of(page, lang) if page else ""


def persona_urls(key: str) -> set[str]:
    """Every URL of the persona ``key``'s own pages, in every language they are listed in."""
    return {url for page in PERSONA_PAGES.get(key, ()) for lang in page.langs if (url := url_of(page, lang))}


def surface_keys() -> list[str]:
    """Every key ``live_status.json`` may name under ``surfaces``: W1-0's census ids, in the index's order."""
    keys: list[str] = []
    pages = [*PUBLIC_PAGES, *(page for pages in PERSONA_PAGES.values() for page in pages), *STATE_PAGES]
    for key in [page.surface for page in pages] + list(STATE_KEYS):
        if key not in keys:
            keys.append(key)
    return keys


# ---------------------------------------------------------------------------------------------
# live_status.json — read only
# ---------------------------------------------------------------------------------------------

SCALES = ("visual", "premium", "originality", "ux", "mobile", "coherence")
SCALE_LABELS = {
    "visual": "visivo",
    "premium": "premium",
    "originality": "originalità",
    "ux": "UX",
    "mobile": "telefono",
    "coherence": "coerenza",
}


def _default_live_status_path() -> Path:
    return Path(settings.BASE_DIR) / "docs" / "design-v5" / "live_status.json"


def _state(value) -> str:
    if isinstance(value, dict):
        value = value.get("state")
    return STATE_V5 if value == STATE_V5 else STATE_V4


def day(value) -> datetime.date | None:
    """
    An ISO date the steward or git wrote («2026-10-05»), as a date the templates print in words
    («5 ottobre 2026», the ISO value kept in ``datetime``) — or None, and the words are the value as
    written (review W1-P, UX r2 n8; CD condition C9).
    """
    try:
        return datetime.date.fromisoformat(str(value or "")[:10])
    except ValueError:
        return None


def live_status() -> dict:
    """
    The steward's ``live_status.json``, read now — template-ready and defensive: an absent file is
    said to be absent, an unreadable one to be unreadable, and either way every surface is
    «V4 + fondation». Nothing is remembered from one request to the next.
    """
    path = Path(getattr(settings, "ILE_DESIGN_PREVIEW_LIVE_STATUS", "") or _default_live_status_path())
    status = {"path": path.as_posix(), "present": False, "error": "", "updated": "", "families": [], "surfaces": {}}
    try:
        data = json.loads(path.read_bytes().decode("utf-8"))
    except FileNotFoundError:
        return status
    except (OSError, UnicodeDecodeError, ValueError):
        return {**status, "present": True, "error": "illeggibile"}
    if not isinstance(data, dict):
        return {**status, "present": True, "error": "non è un oggetto JSON"}
    families = []
    for raw in data.get("families") or []:
        if not isinstance(raw, dict) or not raw.get("key"):
            continue
        scores = raw.get("scores") if isinstance(raw.get("scores"), dict) else {}
        state = _state(raw.get("state"))
        families.append(
            {
                "key": str(raw.get("key")),
                "title": str(raw.get("title") or ""),
                "state": state,
                "label": STATE_LABELS[state],
                "scores": [
                    {"scale": scale, "label": SCALE_LABELS[scale], "value": scores.get(scale)}
                    for scale in SCALES
                    if isinstance(scores.get(scale), (int, float)) and not isinstance(scores.get(scale), bool)
                ],
                "decision": str(raw.get("decision") or ""),
                "tag": str(raw.get("tag") or ""),
                "date": str(raw.get("date") or ""),
                "day": day(raw.get("date")),
            }
        )
    surfaces = data.get("surfaces") if isinstance(data.get("surfaces"), dict) else {}
    return {
        **status,
        "present": True,
        "updated": str(data.get("updated") or ""),
        "updated_day": day(data.get("updated")),
        "families": families,
        "surfaces": {str(key): _state(value) for key, value in surfaces.items()},
    }


def state_of(key: str, status: dict) -> str:
    return status["surfaces"].get(key, STATE_V4)


#: The states of plan §4.5 that a later family builds, with the families that build them: the engage
#: on the login (the loader's L1, on the login's stage), the release after «Entrer» (the loader's
#: receiver and the rail's mark), the stage's answers while the sign-in is filled. The index says
#: «in arrivo» beside each until every family it names is "v5" in live_status.json: it shows the
#: owner what works today, never a promise worded as a fact (review W1-P, UX r2 n4; CD condition C2).
COMING: dict[str, tuple[tuple[str, str], ...]] = {
    "engage": (("w1-d", "W1-D (il caricatore «Lume»)"), ("w2-b", "W2-B (l’accesso «Il varco»)")),
    "release": (("w1-d", "W1-D (il caricatore «Lume»)"),),
    "stage": (("w2-b", "W2-B (l’accesso «Il varco»)"),),
}


def coming(status: dict) -> dict[str, str]:
    """Per state of ``COMING``: the «in arrivo» note while a family it needs has not passed, "" once all have."""
    passed = {family["key"] for family in status["families"] if family["state"] == STATE_V5}
    notes = {}
    for state, families in COMING.items():
        waiting = [name for key, name in families if key not in passed]
        notes[state] = f"— in arrivo con {' e '.join(waiting)}: oggi la pagina non lo mostra ancora." if waiting else ""
    return notes


# ---------------------------------------------------------------------------------------------
# The build and the changelog
# ---------------------------------------------------------------------------------------------


def _git(*args: str) -> str:
    """One git question about this worktree, answered in at most five seconds — or ""."""
    git = shutil.which("git")
    if not git:
        return ""
    try:
        # A fixed argument list: nothing of a request reaches it.
        result = subprocess.run(  # noqa: S603
            [git, "-C", str(settings.BASE_DIR), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


@functools.lru_cache(maxsize=1)
def identity() -> dict:
    """
    The tag this worktree is checked out at (v5-live's, on 8780), its commit and its date — or the
    branch, when no tag points at the commit. Asked once per process: 8780 is restarted after every
    checkout, so the answer cannot go stale while it is shown.
    """
    tag = _git("describe", "--tags", "--exact-match", "HEAD")
    commit, _, date = _git("log", "-1", "--format=%h%x09%cs").partition("\t")
    branch = "" if tag else _git("rev-parse", "--abbrev-ref", "HEAD")
    return {"tag": tag, "branch": "" if branch == "HEAD" else branch, "commit": commit, "date": date}


def _default_changelog_path() -> Path:
    return Path(settings.BASE_DIR) / "docs" / "design-v5" / "CHANGELOG_V54.md"


_ENTRY = re.compile(r"^\s*[-*]\s+(.+?)\s*$")


def changelog(limit: int = 3) -> dict:
    """
    The first ``limit`` entries of the steward's changelog: its first list items, newest first as
    the steward writes them. Absent, it says so.
    """
    path = Path(getattr(settings, "ILE_DESIGN_PREVIEW_CHANGELOG", "") or _default_changelog_path())
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return {"path": path.as_posix(), "present": False, "lines": []}
    lines = []
    for line in text.splitlines():
        match = _ENTRY.match(line)
        if match:
            lines.append(match.group(1).replace("**", "").replace("`", ""))
            if len(lines) == limit:
                break
    return {"path": path.as_posix(), "present": True, "lines": lines}


# ---------------------------------------------------------------------------------------------
# The page a frame holds
# ---------------------------------------------------------------------------------------------

_LANG_PREFIX = re.compile(r"^/(it|fr|en|ar)/")
#: What a frame may hold: a page under a language prefix, or one of the documents app, which is
#: mounted without a prefix (config/urls.py) and speaks the language cookie's language.
_PAGE_PREFIX = re.compile(r"^/(?:it|fr|en|ar|documents)/")
_UNSAFE = re.compile(r"[\\\s\x00-\x1f\x7f]")
#: The same rule, for the script that follows the frame (the strip's data block).
FOLLOW = _PAGE_PREFIX.pattern


def _clean_path(path: str) -> bool:
    """
    No dot segment, no empty segment and nothing unsafe — in the path as written and as a browser
    reads it: the URL standard takes ``%2e%2e`` for ``..``, so the path is percent-decoded and
    looked at again until it stops changing (review W1-P, security m3: ``/fr/../__design-v5/…``
    framed a research comp under the live strip).
    """
    for _ in range(4):
        if _UNSAFE.search(path):
            return False
        segments = path.split("/")[1:]
        if segments and segments[-1] == "":
            segments = segments[:-1]
        if any(segment in ("", ".", "..") for segment in segments):
            return False
        decoded = unquote(path)
        if decoded == path:
            return True
        path = decoded
    return False


def page_param(raw: str) -> str:
    """
    A path of this site under a language prefix or under ``/documents/``, with its query string —
    or "" for anything else: another origin, a scheme, a protocol-relative URL, a backslash, a
    control character, a dot segment or an empty one, encoded or not, the preview itself. What a
    frame holds comes from here and from nowhere else.
    """
    if not raw or len(raw) > 512 or _UNSAFE.search(raw) or raw.startswith("//"):
        return ""
    parts = urlsplit(raw)
    if parts.scheme or parts.netloc or not _PAGE_PREFIX.match(parts.path) or not _clean_path(parts.path):
        return ""
    return parts.path + (f"?{parts.query}" if parts.query else "")


def is_neutral(page: str) -> bool:
    """A page without a language prefix (the documents app): its language is the language cookie's."""
    return not _LANG_PREFIX.match(page)


def lang_of(page: str) -> str:
    match = _LANG_PREFIX.match(page)
    return match.group(1) if match else "fr"


def in_lang(page: str, lang: str) -> str:
    """The same page in another language: the site's paths are the same under every prefix."""
    return _LANG_PREFIX.sub(f"/{lang}/", page, count=1)


def reserved(page: str) -> bool:
    """A page that needs a session: the reserved area and the documents app."""
    return is_neutral(page) or bool(re.match(r"^/(it|fr|en|ar)/espace-reserve/", page))


def signin_paths() -> list[str]:
    """The sign-in's address in every language it is reviewed in («Il varco»: fr, ar, it, en)."""
    login = next(page for page in PUBLIC_PAGES if page.slug == "login")
    return [url for lang in login.langs if (url := url_of(login, lang))]


def way_in(page: str, persona: str) -> tuple[bool, str]:
    """
    Signed out, the product's own way in ends on the sign-in's password form, which the preview never
    asks for (review W1-P, UX r2 n2; CD condition C4). Whether the strip says «Per entrare senza
    password: «Personas»» beside the state — nobody is inside, and the frame holds the sign-in or a
    reserved page, which sends a visitor there — and the page an «Entrer» then opens: the sign-in's
    ``next``, or the reserved page itself. The switch honours it only when it is that persona's own
    page (``views._next``); "" opens the persona's first page.
    """
    path, _, query = page.partition("?")
    at_signin = path in signin_paths()
    if at_signin:
        target = page_param(parse_qs(query).get("next", [""])[0])
    elif reserved(page) and not persona:
        target = page
    else:
        target = ""
    return (not persona and (at_signin or reserved(page))), target


def landing_url(page: str = "", frame: str = "desktop", lang: str = "") -> str:
    """
    The landing framing ``page``. ``lang`` is carried only for a page without a language prefix: the
    landing then sets the language cookie, so that the documents app answers in that language.
    """
    query = {}
    if page:
        query["page"] = page
    if frame != "desktop":
        query["frame"] = frame
    if page and lang in LANGS_ALL and is_neutral(page):
        query["lang"] = lang
    base = reverse("designpreview:landing")
    return f"{base}?{urlencode(query, safe='/')}" if query else base


# ---------------------------------------------------------------------------------------------
# The V4 control
# ---------------------------------------------------------------------------------------------

_LOCAL_ORIGIN = re.compile(r"^http://(127\.0\.0\.1|localhost):(\d{2,5})$")


def v4_origin() -> str:
    """
    The V4 control's origin (8771 unless the environment says otherwise) — or "" if the setting
    names anything but a loopback origin on another port than this server's: V4 is never compared
    on the server that serves V5.
    """
    origin = str(getattr(settings, "ILE_DESIGN_PREVIEW_V4_ORIGIN", "") or "")
    match = _LOCAL_ORIGIN.match(origin)
    if not match or int(match.group(2)) == access.own_port():
        return ""
    return origin


# ---------------------------------------------------------------------------------------------
# What the templates draw
# ---------------------------------------------------------------------------------------------


def _ordered_pages(persona: str) -> list[Page]:
    """
    Every page the strip may name, the active persona's first: a URL several page types share — the
    reserved area's first page is four of them, one per persona — is named as the persona inside
    sees it.
    """
    own = list(PERSONA_PAGES.get(persona, ()))
    others = [page for key, pages in PERSONA_PAGES.items() if key != persona for page in pages]
    return [*own, *PUBLIC_PAGES, *STATE_PAGES, *others]


_REGEX_SPECIAL = re.compile(r"([.^$*+?()\[\]{}|\\])")


def _pattern(path: str, values: list[str]) -> str:
    """
    The address of a detail page as a regular expression that Python and the browser read alike:
    every segment that is one of the page's ids becomes any segment; the rest stays as written.
    """
    segments = [r"[^/]+" if segment in values else _REGEX_SPECIAL.sub(r"\\\1", segment) for segment in path.split("/")]
    return "^" + "/".join(segments) + "$"


def _known(status: dict, persona: str = "") -> tuple[dict[str, list], list[list[str]]]:
    """
    Every known page in every language it is reviewed in — path → [its state, its languages, its
    title] — and, for the pages whose address carries an id (a case, a request, a course, a step of
    the questionnaire), the pattern of that address: [regular expression, state, title]. Any case of
    a page type the steward has marked then says so, not only the census's example.
    """
    known: dict[str, list] = {}
    patterns: list[list[str]] = []
    for page in _ordered_pages(persona):
        state = state_of(page.surface, status)
        for lang in page.langs:
            url = url_of(page, lang)
            if not url:
                continue
            path = url.split("?", 1)[0]
            known.setdefault(path, [state, " ".join(page.langs), page.title])
            if page.kwargs:
                regex = _pattern(path, [value for _name, value in page.kwargs])
                if all(regex != seen[0] for seen in patterns):
                    patterns.append([regex, state, page.title])
    return known, patterns


def _entry(known: dict[str, list], patterns: list[list[str]], path: str) -> list | None:
    """What the strip knows of ``path``: [state, languages, title], from the pages or from a pattern."""
    if path in known:
        return known[path]
    for regex, state, title in patterns:
        if re.match(regex, path):
            return [state, " ".join(LANGS_PRIMARY), title]
    return None


def quick_surfaces(status: dict, lang: str, frame: str, active: str = "") -> dict:
    """
    The council-passed surfaces in ``lang`` — the strip's «Superfici V5» menu (review W1-P M5: one
    menu, never a row of links that outgrows the strip): the public pages, then each persona's, with
    whether that persona is the one inside (a plain link) or not (a POST to the switch that opens it).
    """
    from designpreview import personas

    public: list[dict] = []
    for page in PUBLIC_PAGES:
        if state_of(page.surface, status) != STATE_V5:
            continue
        code = lang if lang in page.langs else page.langs[0]
        url = url_of(page, code)
        if url and all(item["url"] != url for item in public):
            public.append({"title": page.title, "url": url, "lang": code, "landing": landing_url(url, frame, code)})
    allowed = personas.allow_list()
    groups: list[dict] = []
    for persona in personas.PERSONAS.values():
        pages = []
        for page in PERSONA_PAGES.get(persona.key, ()):
            if state_of(page.surface, status) != STATE_V5:
                continue
            code = lang if lang in page.langs else page.langs[0]
            url = url_of(page, code)
            if url:
                pages.append({"title": page.title, "url": url, "lang": code, "landing": landing_url(url, frame, code)})
        if pages:
            groups.append(
                {
                    "key": persona.key,
                    "name": persona.name,
                    "inside": persona.key == active,
                    "allowed": persona.key in allowed,
                    "pages": pages,
                }
            )
    return {"public": public, "personas": groups, "count": len(public) + sum(len(group["pages"]) for group in groups)}


def strip(request, page: str, frame: str, status: dict | None = None, lang: str = "") -> dict:
    """
    The strip above the frame: the build, the state of the page, its languages, the frames, the
    council-passed surfaces, the personas. ``lang`` is the language of a page without a language
    prefix (the documents app), which the landing was asked for or the language cookie holds.
    """
    from designpreview import personas

    status = status if status is not None else live_status()
    active = personas.current(request)
    known, patterns = _known(status, active)
    neutral = is_neutral(page)
    lang = (lang if lang in LANGS_ALL else "fr") if neutral else lang_of(page)
    entry = _entry(known, patterns, page.split("?", 1)[0])
    state = entry[0] if entry else STATE_V4
    offered = entry[1].split() if entry else list(LANGS_PRIMARY)
    allowed = personas.allow_list()
    database = personas.database_name()
    build = identity()
    hint, target = way_in(page, active)
    return {
        "page": page,
        "page_title": entry[2] if entry else "",
        "frame": frame,
        "lang": lang,
        "state": state,
        "state_label": STATE_LABELS[state],
        "langs": [
            {
                "code": code,
                "name": LANG_NAMES[code],
                "url": landing_url(page, frame, code) if neutral else landing_url(in_lang(page, code), frame),
                "current": code == lang,
            }
            for code in offered
        ],
        "frames": [
            {
                "code": "desktop",
                "label": "Desktop",
                "url": landing_url(page, "desktop", lang),
                "current": frame == "desktop",
            },
            {
                "code": "phone",
                "label": "Telefono 390",
                "url": landing_url(page, "phone", lang),
                "current": frame == "phone",
            },
        ],
        "identity": {**build, "day": day(build.get("date"))},
        "changelog": changelog(),
        "hint": hint,
        "next": target,
        "quick": quick_surfaces(status, lang, frame, active),
        "personas": [
            {
                "key": persona.key,
                "name": persona.name,
                "note": persona.note,
                "opens": PERSONA_PAGES[persona.key][0].title if PERSONA_PAGES.get(persona.key) else "",
                "allowed": persona.key in allowed,
                "inside": persona.key == active,
            }
            for persona in personas.PERSONAS.values()
        ],
        "persona": personas.PERSONAS[active].name if active in personas.PERSONAS else active,
        "persona_key": active,
        "database": database,
        "database_allowed": personas.database_allowed(database),
        "map": {
            "pages": known,
            "patterns": patterns,
            "labels": STATE_LABELS,
            "fallback": STATE_V4,
            "follow": FOLLOW,
            "persona": active,
            "landing": reverse("designpreview:landing"),
            "archive": reverse("designpreview:hub"),
            "signin": signin_paths(),
        },
    }


def public_rows(status: dict) -> list[dict]:
    """The index's public pages: per page its state and, per language, its URL, its frames and its V4 twin."""
    origin = v4_origin()
    rows = []
    for page in PUBLIC_PAGES:
        urls = [(lang, url_of(page, lang)) for lang in page.langs]
        urls = [(lang, url) for lang, url in urls if url]
        if not urls:
            continue
        state = state_of(page.surface, status)
        rows.append(
            {
                "slug": page.slug,
                "key": page.surface,
                "title": page.title,
                "note": page.note,
                "group": page.group,
                "state": state,
                "label": STATE_LABELS[state],
                "urls": [
                    {
                        "lang": lang,
                        "name": LANG_NAMES[lang],
                        "url": url,
                        "landing": landing_url(url, lang=lang),
                        "desktop": landing_url(url, "desktop", lang),
                        "phone": landing_url(url, "phone", lang),
                        "v4": f"{origin}{url}" if origin else "",
                    }
                    for lang, url in urls
                ],
            }
        )
    return rows


def persona_cards(request, status: dict) -> list[dict]:
    """
    The four persona cards: per page, per language, its URL and the landing framing it. The index
    draws a page of the persona inside as a link, and a page of any other persona as a POST to the
    switch that enters that persona and opens that page (review W1-P M3) — a link would meet the
    login, or another persona's view of the address.
    """
    from designpreview import personas

    allowed = personas.allow_list()
    active = personas.current(request)
    cards = []
    for persona in personas.PERSONAS.values():
        pages = []
        for page in PERSONA_PAGES.get(persona.key, ()):
            state = state_of(page.surface, status)
            urls = [(lang, url_of(page, lang)) for lang in page.langs]
            pages.append(
                {
                    "slug": page.slug,
                    "key": page.surface,
                    "title": page.title,
                    "note": page.note,
                    "state": state,
                    "label": STATE_LABELS[state],
                    "urls": [
                        {"lang": lang, "name": LANG_NAMES[lang], "url": url, "landing": landing_url(url, lang=lang)}
                        for lang, url in urls
                        if url
                    ],
                }
            )
        cards.append(
            {
                "key": persona.key,
                "name": persona.name,
                "note": persona.note,
                "case": persona.case,
                "opens": pages[0]["title"] if pages else "",
                "allowed": persona.key in allowed,
                "active": persona.key == active,
                "pages": pages,
            }
        )
    return cards


# ---------------------------------------------------------------------------------------------
# The foundation's specimen boards, and the states reachable without credentials
# ---------------------------------------------------------------------------------------------

#: The boards the foundation families are scored on (templates/dev/designpreview/specimens/README.md):
#: (name, what it shows, the family that writes it).
SPECIMEN_BOARDS: tuple[tuple[str, str, str], ...] = (
    ("type", "Il campione tipografico", "W1-A"),
    ("colour", "La tavola dei registri di colore", "W1-A"),
    ("corners", "La tavola degli angoli e delle ombre", "W1-A"),
    ("icons", "Il foglio delle icone", "W1-B"),
    ("loader", "Le sequenze del caricatore", "W1-D"),
    ("chips", "La tavola dei chip", "W1-C"),
    ("buttons", "La serie dei bottoni", "W1-C"),
    ("fields", "La serie dei campi", "W1-C"),
    ("overlays", "Il sistema degli overlay", "W2-A"),
)


def specimen_boards() -> list[dict]:
    """Each board with its link when its template exists — looked up now, so a board is linked the moment it lands."""
    from django.template import TemplateDoesNotExist, loader

    boards = []
    for name, title, family in SPECIMEN_BOARDS:
        try:
            loader.get_template(f"dev/designpreview/specimens/{name}.html")
        except TemplateDoesNotExist:
            url = ""
        else:
            url = reverse("designpreview:specimen", kwargs={"board": name})
        boards.append({"name": name, "title": title, "family": family, "url": url})
    return boards


#: The error pages the DEBUG URLconf serves (config/urls.py) — beside the preview's own 429.
DEBUG_ERROR_PAGES: tuple[str, ...] = ("400", "403", "404", "500")
