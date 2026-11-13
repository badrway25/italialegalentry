"""
The phase console: what each gate controls, and what changes when it moves.

The back-office already showed seven booleans. A boolean is not an instruction — an administrator
looking at «Contenuti Fase 3 pubblici: no» cannot tell what is hidden, what would appear, what has to
be true first, or whether the answer is "no" because somebody decided so or because a date has not
arrived. Every one of those questions was answered by reading the source, which means in practice
they were answered by asking a developer.

So each gate is described here as DATA: the flag behind it, the pages it opens, the condition it
depends on, and the reason it exists. The console renders that description; it does not compute it.

This module deliberately holds no logic of its own. ``core.gates`` decides; this says what the
decision means. If the two ever disagree, the test suite fails rather than the administrator being
misled — ``tests/test_phase_console.py`` asserts that every gate in ``gates.snapshot()`` has an entry
here and that no entry names a flag that does not exist.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from django.utils.translation import gettext_lazy as _


@dataclass(frozen=True)
class GateDescription:
    """One gate, described for the person who has to decide whether to open it."""

    key: str
    label: object
    flag: str
    opens: object
    depends_on: tuple[str, ...] = ()
    reason: object = ""
    reversible: bool = True
    routes: tuple[str, ...] = field(default_factory=tuple)


#: Every gate ``core.gates.snapshot()`` reports, in the order an administrator meets them.
#: The order is the project's own chronology: legal pages first, because everything else waits on
#: them, then the forms they unlock, then the phase and the Forum.
GATES: tuple[GateDescription, ...] = (
    GateDescription(
        key="legal_pages_available",
        label=_("Pagine legali ufficiali (IT)"),
        flag="",
        opens=_(
            "Privacy policy, condizioni d'uso, cookie policy, note legali e informativa candidati "
            "nella loro versione italiana ufficiale."
        ),
        reason=_(
            "Non è un interruttore: è vero quando i cinque documenti legali sono pubblicati. "
            "Finché non lo sono, nessun form pubblico può raccogliere dati personali, perché la "
            "persona non avrebbe l'informativa che la legge le deve."
        ),
        reversible=False,
    ),
    GateDescription(
        key="public_forms_enabled",
        label=_("Form pubblici attivi"),
        # There is no "open the forms" flag, and that is the point: the gate follows the legal pages.
        # ``forms_override_without_legal`` forces it open, is named DANGER in its own note, and every
        # change to it is audited — it exists for the QA environment, not for a launch decision.
        flag="forms_override_without_legal",
        opens=_(
            "Contatto, proposta di collaborazione, fabbisogni d'impresa, iscrizione al Forum, "
            "registrazione di un account."
        ),
        depends_on=("legal_pages_available",),
        reason=_(
            "Un form raccoglie dati personali. Aprirlo prima delle pagine legali significa "
            "raccoglierli senza informativa, che è esattamente ciò che il gate impedisce."
        ),
        routes=("enquiries:contact", "enquiries:collaboration", "accounts:signup"),
    ),
    GateDescription(
        key="phase3_public",
        label=_("Contenuti Fase 3 pubblici"),
        flag="phase3_public",
        opens=_(
            "Spazio Persone, elenco dei percorsi, questionario di orientamento, pagina Progetto "
            "pilota, FAQ, glossario, Vivere in Italia."
        ),
        reason=_(
            "La Fase 3 è prevista dopo il 2 ottobre 2026. Il gate esiste perché la data possa "
            "cambiare senza che nessuno debba toccare il codice, e perché il contenuto possa essere "
            "preparato e riletto prima di essere visibile."
        ),
    ),
    GateDescription(
        key="forum_banner_visible",
        label=_("Banner Forum in homepage"),
        flag="forum_banner",
        opens=_("La fascia di annuncio dell'evento del 2 ottobre 2026 in testa alla homepage."),
        reason=_(
            "Si spegne da sé il 2 ottobre tramite la finestra di attivazione. Un banner che annuncia "
            "un evento già avvenuto è il difetto più visibile che un sito istituzionale possa avere."
        ),
    ),
    GateDescription(
        key="forum_permanent_mode",
        label=_("Forum in modalità permanente"),
        flag="forum_permanent_mode",
        opens=_(
            "La pagina Forum passa da «evento» a «Forum Permanente Vénétie–Maroc»: esiti "
            "dell'edizione, prossime tappe, risorse pubbliche, relazione annuale."
        ),
        reason=_(
            "Il convegno e l'infrastruttura permanente sono due prodotti con lo stesso nome. "
            "La transizione è una decisione editoriale, non tecnica, e va presa dopo l'evento."
        ),
    ),
    GateDescription(
        key="virtual_forum_enabled",
        label=_("Forum Virtuale (area autenticata)"),
        flag="virtual_forum",
        opens=_(
            "Lo spazio di cooperazione riservato: commissioni, tavoli, proposte, progetti, "
            "monitoraggio e relazione annuale."
        ),
        depends_on=("legal_pages_available",),
        reason=_(
            "Chiuso fino a dopo il 30 ottobre 2026. È uno spazio in cui organizzazioni pubblicano "
            "documenti e proposte: aprirlo prima che esistano le regole di partecipazione "
            "significherebbe chiedere a qualcuno di fidarsi senza dirgli di che cosa."
        ),
    ),
    GateDescription(
        key="newsletter_enabled",
        label=_("Newsletter"),
        flag="newsletter",
        opens=_("Il modulo di iscrizione alla newsletter e l'invio."),
        depends_on=("legal_pages_available",),
        reason=_(
            "Richiede un consenso specifico e revocabile, quindi richiede il testo del consenso, "
            "quindi richiede le pagine legali."
        ),
    ),
)

GATES_BY_KEY: dict[str, GateDescription] = {gate.key: gate for gate in GATES}


def console_rows() -> list[dict]:
    """
    The console, assembled from the live gate states and the descriptions above.

    ``blocked_by`` is the useful column: a gate whose dependency is closed cannot be opened by
    flipping its own flag, and an administrator who does not know that will flip it, see no change,
    and conclude the system is broken.
    """
    from core import gates

    snapshot = gates.snapshot()
    rows = []
    for gate in GATES:
        blocked_by = [
            GATES_BY_KEY[name].label
            for name in gate.depends_on
            if name in GATES_BY_KEY and not snapshot.get(name, False)
        ]
        rows.append(
            {
                "key": gate.key,
                "label": gate.label,
                "open": bool(snapshot.get(gate.key, False)),
                "flag": gate.flag,
                "opens": gate.opens,
                "reason": gate.reason,
                "reversible": gate.reversible,
                "blocked_by": blocked_by,
                "depends_on": gate.depends_on,
            }
        )
    return rows
