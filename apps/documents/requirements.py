"""
The seven states of a required document, and the rule each word carries.

Two different questions are answered in this project by two different vocabularies, and keeping
them apart is the whole point of this module:

* **What does the scanner say about this FILE?** — ``documents.models.ScanStatus``:
  NOT_CONFIGURED · PENDING · CLEAN · INFECTED · ERROR. This is a technical fact about bytes on a
  disk. It is shown, honestly, where a technical fact belongs: next to the file.
* **What does this mean for MY FILE?** — ``documents.models.RequirementState``:
  MANQUANT · DÉPOSÉ · EN EXAMEN · VALIDE · NON VALIDE · EXPIRÉ · À REMPLACER. This is what the
  person came to find out, and it is the only thing the register column shows.

"Analysé — sain" in the column where someone looks for their own status answers a question nobody
asked. That was the defect. A scan result feeds the derivation below; it never *is* the answer.

No state here means "approved". VALIDE says: the piece received is the piece that was asked for.
The platform approves nobody, and no state of a document says anything at all about a person's
entitlement to enter, work or study (CONFLICT_REGISTER CR-11).
"""

from __future__ import annotations

import datetime as dt

from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from core import clock
from documents.models import RequirementState, ScanStatus, VersionDecision

#: A piece whose validity ends within this many days is already "à remplacer": telling somebody the
#: day it expires is not a warning, it is a notification of a problem they can no longer prevent.
REPLACE_WINDOW_DAYS = 30

#: Rank used to sort a register. Missing and expiring first, art direction A §13.3.
STATE_ORDER: dict[str, int] = {
    RequirementState.EXPIRED: 0,
    RequirementState.INVALID: 1,
    RequirementState.MISSING: 2,
    RequirementState.TO_REPLACE: 3,
    RequirementState.IN_REVIEW: 4,
    RequirementState.FILED: 5,
    RequirementState.VALID: 6,
}

#: The CSS modifier of ``.state`` in static/css/register.css. The stylesheet already carries all
#: seven; this map exists so a template never builds a class name out of a database value.
STATE_CSS: dict[str, str] = {
    RequirementState.MISSING: "missing",
    RequirementState.FILED: "filed",
    RequirementState.IN_REVIEW: "review",
    RequirementState.VALID: "valid",
    RequirementState.INVALID: "invalid",
    RequirementState.EXPIRED: "expired",
    RequirementState.TO_REPLACE: "replace",
}

#: The RULE each word carries. A state word with no rule is a colour with extra steps: the reader
#: must be able to learn, from the page, what the word means and what follows from it.
STATE_RULES: dict[str, object] = {
    RequirementState.MISSING: _("Rien n’a encore été déposé pour cette pièce."),
    RequirementState.FILED: _("Le fichier est arrivé. Il n’a pas encore été examiné par une personne."),
    RequirementState.IN_REVIEW: _("Un intervenant du dossier examine la pièce déposée."),
    RequirementState.VALID: _("La pièce reçue correspond à ce qui était demandé. Ceci n’est pas une décision."),
    RequirementState.INVALID: _(
        "La pièce déposée n’a pas été retenue. Le motif est indiqué ; il faut en déposer une autre."
    ),
    RequirementState.EXPIRED: _("La validité de la pièce est dépassée. Une pièce en cours de validité est nécessaire."),
    RequirementState.TO_REPLACE: _(
        "La pièce doit être remplacée : sa validité se termine, ou un remplacement a été demandé."
    ),
}

#: What the antivirus integration point can honestly say (REQ-DOC-03). Never "sain" when nothing
#: has run; never "en attente" when nothing is coming.
SCAN_RULES: dict[str, object] = {
    ScanStatus.NOT_CONFIGURED: _(
        "Aucun antivirus n’est déployé sur cette installation : le fichier n’a pas été analysé."
    ),
    ScanStatus.PENDING: _("Le fichier attend son analyse."),
    ScanStatus.CLEAN: _("L’antivirus a analysé ce fichier et n’a rien signalé."),
    ScanStatus.INFECTED: _("L’antivirus a signalé ce fichier. Il a été supprimé du stockage."),
    ScanStatus.ERROR: _("L’analyse a échoué. Le résultat est inconnu : il n’est pas présumé sain."),
}

#: The same five states as ONE WORD, for the state chip.
#:
#: `ScanStatus.choices` carries the field's verbose labels, and one of them is a whole sentence —
#: "Aucune analyse antivirus n’est configurée". The dashboard put that sentence in `.entry__actor`,
#: a slot the design draws on a single line and the stylesheet sets `white-space: nowrap`; at 320px
#: it ran 128px past the card and gave the whole page a horizontal scrollbar. The same mistake was
#: made once before with an organisation's full name, and `templates/academy/catalogue.html` records
#: the resolution taken then: the slot is for a short label, so the long text moves — the CSS does
#: not bend.
#:
#: Nothing is softened by shortening it. "non analysé" says exactly what "aucune analyse n’est
#: configurée" says, and the full sentence is still `SCAN_RULES`, shown on the document register
#: where a reader is deciding whether to trust a file.
SCAN_CHIPS: dict[str, object] = {
    ScanStatus.NOT_CONFIGURED: _("non analysé"),
    ScanStatus.PENDING: _("en attente"),
    ScanStatus.CLEAN: _("sain"),
    ScanStatus.INFECTED: _("bloqué"),
    ScanStatus.ERROR: _("échec d’analyse"),
}

#: The widest the chip may be before it stops fitting the slot at 320px. Measured, not guessed:
#: the slot is 186px there and the folio face sets roughly 11px per uppercase character.
SCAN_CHIP_MAX_CHARS = 18


#: Why a stored file cannot be HANDED OVER to the account reading the page, when it cannot.
#:
#: This is a third vocabulary, and it is deliberately not mixed with the other two. A file may be
#: perfectly readable to a reviewer under ``documents.policies`` and still not be deliverable to
#: them: ``documents.views._serve`` refuses an unscanned file to anybody but its depositor, because
#: handing an unverified file to a third party is the one thing the antivirus hook exists to
#: prevent, and it must not become optional merely because no scanner is installed.
#:
#: The interface must say that, and say WHOSE problem it is. Drawing a "Télécharger" link that
#: answers 403 is a worse failure than drawing none: it makes the reader think they did something
#: wrong.
DELIVERY_RULES: dict[str, object] = {
    "file_gone": _("Le fichier n’est plus conservé : il a été purgé ou supprimé."),
    "infected": _("Le fichier a été signalé par l’antivirus et supprimé du stockage."),
    "unscanned": _(
        "Aucun antivirus n’est déployé sur cette installation : le fichier n’est remis qu’à la "
        "personne qui l’a déposé. Un administrateur doit le contrôler avant toute autre remise."
    ),
}


def delivery_rule(code: str) -> object:
    return DELIVERY_RULES.get(code, "")


def state_label(state: str) -> object:
    return dict(RequirementState.choices).get(state, state)


def state_css(state: str) -> str:
    return STATE_CSS.get(state, "missing")


def state_rule(state: str) -> object:
    return STATE_RULES.get(state, "")


def scan_rule(status: str) -> object:
    return SCAN_RULES.get(status, "")


def scan_chip(status: str) -> object:
    """The one-word form, for the state chip. See SCAN_CHIPS."""
    return SCAN_CHIPS.get(status, status)


def derive_state(requirement, version, *, today: dt.date | None = None) -> str:
    """
    The single derivation of a requirement's state. Read by the interface on every render, so an
    expiry becomes true the day it happens and not the day a cron job next runs.

    Precedence, worst first, because a person must see the thing that blocks them:

    1. no version at all, or the file is gone (purged, deleted, blocked by the scanner) → MANQUANT
       — except after a refusal, which stays NON VALIDE so the motive survives the deletion;
    2. the scanner signalled the file, or a reviewer refused it → NON VALIDE;
    3. the piece's own validity has passed → EXPIRÉ;
    4. a replacement was asked for, or the validity ends within thirty days → À REMPLACER;
    5. a reviewer accepted it → VALIDE;
    6. a reviewer has it in hand → EN EXAMEN;
    7. otherwise the file is simply there → DÉPOSÉ.

    The scan status feeds step 2 and NOTHING else: a file that no scanner has looked at is not
    "pending" to a person, it is *deposited*. Saying otherwise would make the antivirus a gate the
    deployment does not actually have.
    """
    today = today or clock.today()
    if version is None:
        return RequirementState.MISSING

    document = version.document
    refused = version.decision == VersionDecision.REFUSED
    infected = document is not None and document.is_infected

    if infected or refused:
        return RequirementState.INVALID
    if document is None or document.deleted_at is not None or not document.has_file:
        # The file no longer exists and no reviewer refused it: the requirement is unmet again.
        return RequirementState.MISSING
    if version.expires_on and version.expires_on < today:
        return RequirementState.EXPIRED
    if requirement.replacement_requested_at is not None:
        return RequirementState.TO_REPLACE
    if version.expires_on and version.expires_on <= today + dt.timedelta(days=REPLACE_WINDOW_DAYS):
        return RequirementState.TO_REPLACE
    if version.decision == VersionDecision.ACCEPTED:
        return RequirementState.VALID
    if version.decision == VersionDecision.IN_REVIEW:
        return RequirementState.IN_REVIEW
    return RequirementState.FILED


def state_reason(requirement, version, state: str) -> str:
    """The sentence that explains THIS row's state — the motive of a refusal, the expiry date."""
    if version is None:
        return ""
    if state == RequirementState.INVALID:
        if version.document is not None and version.document.is_infected:
            return str(_("Le fichier a été signalé par l’antivirus et supprimé."))
        return version.decision_note
    if state == RequirementState.TO_REPLACE and requirement.replacement_requested_at is not None:
        return requirement.replacement_reason
    return ""


def sort_key(requirement) -> tuple:
    """Missing and expiring rows first, then by due date, then by the declared order."""
    state = requirement.display_state
    due = requirement.due_date or dt.date.max
    return (STATE_ORDER.get(state, 9), due, requirement.order, str(requirement.title))


def counts(requirements) -> dict[str, int]:
    """
    Honest counts, never a percentage meter: "3 pièces sur 7 validées" is verifiable, "62 %" is not.
    """
    rows = list(requirements)
    per_state = dict.fromkeys(RequirementState.values, 0)
    for row in rows:
        per_state[row.display_state] = per_state.get(row.display_state, 0) + 1
    return {
        "total": len(rows),
        "per_state": per_state,
        "valid": per_state[RequirementState.VALID],
        "open": sum(
            per_state[value]
            for value in (
                RequirementState.MISSING,
                RequirementState.INVALID,
                RequirementState.EXPIRED,
                RequirementState.TO_REPLACE,
            )
        ),
        "missing": per_state[RequirementState.MISSING],
        "expired": per_state[RequirementState.EXPIRED],
    }


# ---- Urgency, health, the actor's glyph (design V4, CREATIVE_DIRECTION.md §3.5.4) ---------------------
#: How near a due date is, as a word the row can carry beside the date — never a colour alone.
URGENCY_SOON_DAYS = 14
URGENCY_UPCOMING_DAYS = 45


def due_urgency(due_date, *, overdue: bool = False, today=None) -> str:
    """'overdue' · 'soon' (≤ 14 days) · 'upcoming' (≤ 45 days) · '' (nothing to say)."""
    if due_date is None:
        return ""
    if overdue:
        return "overdue"
    today = today or clock.today()
    days = (due_date - today).days
    if days < 0:
        return "overdue"
    if days <= URGENCY_SOON_DAYS:
        return "soon"
    if days <= URGENCY_UPCOMING_DAYS:
        return "upcoming"
    return ""


def health(state: str, version, *, today=None) -> str:
    """The row's health, when the data exists: the piece's own expiry, or that it is being reviewed."""
    if state == RequirementState.IN_REVIEW:
        return str(_("en révision"))
    expires_on = getattr(version, "expires_on", None) if version is not None else None
    if expires_on is not None:
        today = today or clock.today()
        days = (expires_on - today).days
        if days < 0:
            return str(_("pièce expirée"))
        if days <= 90:
            return str(ngettext("expire dans %(n)d jour", "expire dans %(n)d jours", days) % {"n": days})
    return ""


#: The glyph of the actor answerable for a piece (static/img/icons.svg) — beside the actor's name,
#: never instead of it; an unknown actor gets the dashed disc the stylesheet draws for no glyph.
ACTOR_GLYPHS: dict[str, str] = {
    "person": "person",
    "company": "building",
    "authority": "shield",
    "professional": "briefcase",
    "training_body": "university",
    # The company's needs (companies.models.ActorRole): the authorised actor and the project team.
    "authorised_actor": "handshake",
    "project_team": "institution",
}
