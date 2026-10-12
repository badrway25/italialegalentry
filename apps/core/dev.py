"""
Design-system showcase — DEVELOPMENT ONLY.

Why this exists, and why it is a module of its own
--------------------------------------------------
The visual rebase directive (§53) asks for one page where every surface can be looked at side by
side: the same button in its six variants, the six notices, the six badges, a field in its error
state, the modal, the drawer, the table, the empty state. Sixteen specifications describe those
surfaces; none of them could be *seen* in one place. ``.btn--primary`` alone is read by 62 buttons
in 54 templates, and verifying a change to it meant visiting a dozen pages, half of them behind a
session with a case file in the right state.

It is a SEPARATE MODULE, not a view inside ``core.views``, because ``config/urls.py`` imports it
only inside its ``if settings.DEBUG:`` block. With DEBUG off the module is never imported: the
page does not merely answer 404, its code is not in the process. ``design_showcase`` checks
``settings.DEBUG`` a second time anyway — a URLconf is a configuration file, and configuration
files get edited.

Two things here are deliberate and worth keeping:

1.  **The swatch values are read from ``static/css/v2/tokens.css``, not copied.** A showcase that
    re-declares the palette in Python is a second source of truth, and it drifts. This one parses
    the stylesheet on each request (dev only, one small file) so the hex printed under a swatch is
    the hex the browser paints.

2.  **The page checks its own coverage.** CSP is ``style-src 'self'``: no ``style=""`` attribute
    can carry a colour, so every swatch needs a rule in ``static/css/dev/showcase.css``. Without a
    check, adding a token to the palette would silently produce a blank square. ``uncovered``
    lists the tokens the stylesheet has no rule for, and the template prints them as a warning.
"""

from __future__ import annotations

import re
from datetime import UTC
from pathlib import Path

from django import forms
from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

TOKENS_CSS = Path(settings.BASE_DIR) / "static" / "css" / "v2" / "tokens.css"
SHOWCASE_CSS = Path(settings.BASE_DIR) / "static" / "css" / "dev" / "showcase.css"

_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
# Not anchored to the start of a line. tokens.css writes related tokens together —
# `--ok-700: …; --ok-100: …; --ok-300: …;` is one line — and an anchored pattern reads the first
# declaration of each line and silently drops the rest. It did: eight tokens showed a correct
# square with «—» printed underneath, because the square is painted by CSS resolving the variable
# and only the CAPTION came from this parser. tests/frontend/test_design_showcase.py caught it.
_DECL = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;{}]+);", re.IGNORECASE)
_SWATCH_RULE = re.compile(r'\[data-swatch="([a-z0-9-]+)"\]', re.IGNORECASE)

# Colour groups, in the order the design system introduces them. Names only: the values come from
# the stylesheet.
COLOUR_GROUPS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "Surfaces claires",
        "Quatre profondeurs sur papier, puis les encres et les filets.",
        (
            "--min-0",
            "--min-1",
            "--min-2",
            "--min-3",
            "--ink",
            "--ink-2",
            "--ink-3",
            "--hairline",
            "--hairline-strong",
        ),
    ),
    (
        "Surfaces sombres",
        "Les mêmes quatre profondeurs pour un chapitre de nuit.",
        ("--mid-0", "--mid-1", "--mid-2", "--mid-3", "--mid-4", "--on-dark", "--on-dark-2", "--on-dark-3"),
    ),
    (
        "Accent",
        "UN seul accent interactif : liens, action principale, anneau de focus. "
        "Deux luminosités, une pour le papier et une pour la nuit.",
        ("--accent", "--accent-hover", "--accent-dark", "--accent-ring", "--accent-wash"),
    ),
    (
        "Sémantique",
        "Le rouge est réservé à l'erreur. Le bronze est réservé aux sceaux.",
        (
            "--ok-700",
            "--ok-300",
            "--ok-100",
            "--err-700",
            "--err-100",
            "--pending-700",
            "--seal-600",
            "--seal-300",
            "--seal-100",
        ),
    ),
    (
        "Marque",
        "Le vert et le rouge vivent dans le marchio, et nulle part ailleurs.",
        ("--brand-green", "--brand-navy", "--brand-red", "--brand-gold"),
    ),
    (
        "Trajectoires et responsables",
        "Quatre routes, cinq porteurs de responsabilité.",
        (
            "--route-1",
            "--route-2",
            "--route-3",
            "--route-4",
            "--owner-person",
            "--owner-project",
            "--owner-training",
            "--owner-authority",
            "--owner-territory",
        ),
    ),
)

TYPE_SCALE: tuple[tuple[str, str, str], ...] = (
    ("--t-display", "Display", "Une fois par page, dans le chapitre d'ouverture."),
    ("--t-plate", "Plate", "Titre de page interne."),
    ("--t-title", "Title", "Titre de section."),
    ("--t-band", "Band", "Titre de bande."),
    ("--t-entry", "Entry", "Entrée de liste, titre de carte."),
    ("--t-lead", "Lead", "Chapeau."),
    ("--t-body", "Body", "Texte courant."),
    ("--t-ui", "UI", "Libellés d'interface, boutons."),
    ("--t-small", "Small", "Aide, mention."),
    ("--t-folio", "Folio", "Mono, coordonnées, numérotation."),
    ("--t-caption", "Caption", "Légende."),
)

MOTION: tuple[tuple[str, str], ...] = (
    ("--motion-instant", "Retour de pression, changement d'état sans déplacement."),
    ("--motion-fast", "Survol, ouverture d'un menu."),
    ("--motion-base", "Entrée d'un panneau, transition de section."),
    ("--motion-slow", "Tiroir, modale."),
    ("--motion-draw", "Le tracé immersif : un par page."),
    ("--motion-ambient", "L'objet vivant : un par page."),
)


# Demo payloads for the components whose contract is a list of dictionaries. They live here and
# not in the template because a template cannot build a dictionary, and the alternative — copying
# each component's markup into the showcase — is exactly how a showcase stops telling the truth.
DEMO_TABS = [
    {
        "id": "ds-tab-piece",
        "label": "Pièces",
        "body": mark_safe("<p>Le panneau actif est le premier. Les autres sont <code>hidden</code>.</p>"),
    },
    {
        "id": "ds-tab-suivi",
        "label": "Suivi",
        "body": mark_safe("<p>Sans JavaScript, les trois panneaux s'empilent avec leur titre.</p>"),
    },
    {
        "id": "ds-tab-notes",
        "label": "Notes",
        "body": mark_safe("<p>Flèches gauche et droite pour circuler, Début et Fin pour les extrémités.</p>"),
    },
]

DEMO_ACCORDION = [
    {
        "id": "ds-acc-1",
        "title": "Premier panneau, ouvert",
        "body": mark_safe(
            "<p>Construit sur <code>&lt;details&gt;</code> : clavier et lecteur d'écran sans JavaScript.</p>"
        ),
        "open": True,
    },
    {
        "id": "ds-acc-2",
        "title": "Deuxième panneau",
        "body": mark_safe("<p>Le marqueur natif est masqué ; le chevron est dessiné en CSS et pivote.</p>"),
    },
    {
        "id": "ds-acc-3",
        "title": "Troisième panneau",
        "body": mark_safe("<p>Le texte reste trouvable par la recherche du navigateur.</p>"),
    },
]

DEMO_STEPS = ["Profil", "Situation", "Objectif", "Résultat"]

# ---- Design V4, the console's components (gate B review, check 11) -----------------------
# Demo data shaped exactly like the presenters' output; the templates are the real ones.
DEMO_HEALTH = {
    "counts": {"total": 7, "valid": 1, "open": 4, "per_state": {}},
    "filters": [
        {"value": "missing", "label": "Manquant", "count": 1, "register": "attesa"},
        {"value": "filed", "label": "Déposé", "count": 1, "register": "neutro"},
        {"value": "in_review", "label": "En examen", "count": 1, "register": "esame"},
        {"value": "valid", "label": "Valide", "count": 1, "register": "conforme"},
        {"value": "invalid", "label": "Non valide", "count": 1, "register": "rifiuto"},
        {"value": "expired", "label": "Expiré", "count": 1, "register": "azione"},
        {"value": "to_replace", "label": "À remplacer", "count": 1, "register": "attesa"},
    ],
}
DEMO_DOC_ROW = {
    "id": "demo",
    "title": "Passeport en cours de validité",
    "state": "filed",
    "state_label": "Déposé",
    "state_css": "filed",
    "state_reason": "",
    "responsible": "La personne",
    "responsible_note": "",
    "responsible_glyph": "person",
    "due_date": None,
    "is_overdue": False,
    "urgency": "",
    "health": "",
    "mandatory": True,
    "current": None,
    "version_count": 1,
    "may_file": True,
    "action_blocked": False,
    "detail_url": "#console",
}


def _demo_journey() -> list[dict]:
    from portal.services import JOURNEY_STEPS

    first_italy = next((i for i, (_s, side, _l) in enumerate(JOURNEY_STEPS) if side == "italy"), None)
    return [
        {
            "label": label,
            "side": side,
            "is_current": index == 1,
            "frontier": index == first_italy,
            "detail": "",
            "actor": "",
            "state": "done" if index < 1 else "current" if index == 1 else "upcoming",
            "reached_at": None,
        }
        for index, (_status, side, label) in enumerate(JOURNEY_STEPS)
    ]


def _demo_needs() -> list:
    """Four needs in four states for companies/partials/need_table.html — objects, as the partial reads them."""
    from datetime import date
    from types import SimpleNamespace

    from companies.models import NeedStatus

    def need(reference, title, status, headcount, assignee=None):
        return SimpleNamespace(
            reference=reference,
            title=title,
            status=status,
            get_status_display=lambda status=status: str(NeedStatus(status).label),
            state_modifier="filed",
            territory=SimpleNamespace(label="Vénétie"),
            sector=SimpleNamespace(label="Bâtiment et travaux publics"),
            headcount=headcount,
            live_assignments=[SimpleNamespace(role="authorised_actor", display_name=assignee)] if assignee else [],
            updated_at=date(2026, 9, 21),
        )

    return [
        need("BD1F1C30DB", "Soudure d’assemblage sur charpente métallique", NeedStatus.DRAFT, 2),
        need("B06B9D3392", "Préparation de commandes en entrepôt", NeedStatus.SUBMITTED, 8),
        need("B0740869B4", "Conduite d’engins de chantier (voirie)", NeedStatus.UNDER_REVIEW, 4),
        need(
            "BF25965A42", "Maintenance des lignes d’embouteillage", NeedStatus.IN_PROGRESS, 3, "Agence de démonstration"
        ),
    ]


def _demo_case_timeline() -> list[dict]:
    from datetime import datetime

    when = datetime(2026, 9, 21, 10, 0, tzinfo=UTC)
    return [
        {"when": when, "title": "Dossier ouvert", "detail": "", "chip_label": "", "chip_register": "", "actor": "Vous"},
        {
            "when": when,
            "title": "Pré-évaluation enregistrée",
            "detail": "Parcours pertinent",
            "chip_label": "",
            "chip_register": "",
            "actor": "Vous",
        },
        {
            "when": when,
            "title": "Nouvel état",
            "detail": "",
            "chip_label": "Orientation terminée",
            "chip_register": "neutro",
            "actor": "Vous",
        },
    ]


class PasswordShowcaseForm(forms.Form):
    """One password field, for the show/hide control of components/form_field.html."""

    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"autocomplete": "off"}))


# The dialog contract says `body` and `actions` are safe HTML. Passing raw strings from the
# template would print the tags instead of rendering them — the escaping is doing its job, and the
# right place to opt out of it is here, over content this module wrote itself.
DEMO_DIALOG_BODY = mark_safe("<p>Le corps de la modale. Échap ferme ; le focus revient au bouton qui l'a ouverte.</p>")
DEMO_DIALOG_ACTIONS = mark_safe(
    '<button type="button" class="btn btn--secondary" data-overlay-close>Annuler</button>'
    '<button type="button" class="btn btn--primary" data-overlay-close>Confirmer</button>'
)
DEMO_DIALOG_LIGHT_BODY = mark_safe(
    "<p>Celle-ci se ferme aussi par un clic sur le fond. À réserver aux surcouches sans décision à prendre.</p>"
)

DEMO_BREADCRUMBS = [
    {"label": "Écosystème", "url": "#"},
    {"label": "Entreprises", "url": "#"},
    {"label": "Page courante", "url": ""},
]

DEMO_TIMELINE = [
    {"label": "Dépôt", "text": "La demande est enregistrée."},
    {"label": "Recevabilité", "text": "Contrôle des pièces."},
    {"label": "Instruction", "text": "Examen au fond."},
    {"label": "Décision", "text": "Notification au demandeur."},
]

DEMO_META = [
    {"label": "Date", "value": "3 octobre 2026", "icon": "calendar", "datetime": "2026-10-03"},
    {"label": "Lieu", "value": "Rovigo", "icon": "map-pin"},
    {"label": "Responsable", "value": "Autorité compétente", "icon": "institution"},
]

DEMO_TABLE = [
    {
        "title": "Demande n° 2026-0184",
        "kind": "Orientation",
        "date": "12.09.2026",
        "status": "Transmise",
        "badge": "info",
    },
    {
        "title": "Demande n° 2026-0177",
        "kind": "Formation",
        "date": "04.09.2026",
        "status": "En attente",
        "badge": "pending",
    },
    {
        "title": "Demande n° 2026-0166",
        "kind": "Document",
        "date": "28.08.2026",
        "status": "Validée",
        "badge": "success",
    },
    {
        "title": "Demande n° 2026-0154",
        "kind": "Document",
        "date": "19.08.2026",
        "status": "Incomplète",
        "badge": "error",
    },
]

BADGE_KINDS = ("neutral", "info", "success", "warning", "error", "pending", "primary")
NOTICE_KINDS = ("info", "success", "warning", "error", "pending", "institutional")
BUTTON_VARIANTS = ("primary", "secondary", "ghost", "link", "danger")
#: The showcase's icon list — symbols of the registry (apps/core/icons.py), never a V4 alias: `user` was a
#: duplicate of `person`, and `globe`, `key`, `home`, `list` are named by the symbol each one draws
#: (tests/frontend/test_icons.py). The whole sprite is on the icon board, /__design-v5/specimens/icons/.
ICONS = (
    "person",
    "building",
    "institution",
    "university",
    "briefcase",
    "arrow",
    "arrow-up-right",
    "check",
    "warning",
    "shield",
    "calendar",
    "clock",
    "document",
    "languages",
    "menu",
    "close",
    "chevron",
    "chevron-end",
    "plus",
    "minus",
    "search",
    "mail",
    "phone",
    "lock",
    "ile-key",
    "info",
    "map-pin",
    "download",
    "house",
    "logout",
    "settings",
    "quote",
    "send",
    "handshake",
    "compass",
)


class ShowcaseForm(forms.Form):
    """
    A form that exists to be *rendered*, never submitted — the showcase view is GET-only and the
    form has no action. It reproduces the conventions of the real public forms (``form-control``
    on every visible widget, the ``website_url`` honeypot, a mandatory consent checkbox) so that
    what the page shows is what the site does.
    """

    full_name = forms.CharField(
        label="Nom et prénom",
        max_length=120,
        help_text="Tel qu'il figure sur le document d'identité.",
    )
    email = forms.EmailField(label="Adresse électronique")
    profile = forms.ChoiceField(
        label="Vous écrivez en tant que",
        choices=[("", "—"), ("person", "Personne"), ("company", "Entreprise"), ("institution", "Institution")],
    )
    message = forms.CharField(label="Votre demande", widget=forms.Textarea(attrs={"rows": 4}))
    website_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )
    consent = forms.BooleanField(label="J'accepte que ces informations soient traitées pour répondre à ma demande.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in {"website_url", "consent"}:
                continue
            field.widget.attrs.setdefault("class", "form-control")


def read_tokens() -> dict[str, str]:
    try:
        css = TOKENS_CSS.read_text(encoding="utf-8")
    except OSError:  # pragma: no cover — the file is versioned
        return {}
    css = _COMMENT.sub(" ", css)
    tokens: dict[str, str] = {}
    # First declaration wins: the base `:root` value is what the showcase describes, not the
    # override a media query applies at one viewport.
    for name, value in _DECL.findall(css):
        tokens.setdefault(name, value.strip())
    return tokens


def covered_swatches() -> set[str]:
    try:
        css = SHOWCASE_CSS.read_text(encoding="utf-8")
    except OSError:  # pragma: no cover
        return set()
    return set(_SWATCH_RULE.findall(css))


def _swatch(name: str, tokens: dict[str, str]) -> dict[str, str]:
    return {"name": name, "slug": name.removeprefix("--"), "value": tokens.get(name, "—")}


def _situation_form():
    """The real «Ma situation» form, unbound: its radio and checkbox questions are the OptionCards."""
    from accounts.profile_forms import SituationForm

    return SituationForm()


@require_GET
@never_cache
def design_showcase(request):
    if not settings.DEBUG:
        raise Http404

    tokens = read_tokens()
    covered = covered_swatches()

    groups = [
        {"title": title, "note": note, "swatches": [_swatch(name, tokens) for name in names]}
        for title, note, names in COLOUR_GROUPS
    ]
    uncovered = sorted({s["name"] for g in groups for s in g["swatches"] if s["slug"] not in covered})

    # One bound form, deliberately invalid, so the error state is real: the messages under the
    # fields are Django's own, not a hand-written imitation of what an error looks like.
    #
    # `auto_id` is not decoration. Rendering the same form twice on one page gives both copies the
    # same element ids, and `<label for="id_email">` then points at the FIRST one: every field of
    # the second form loses its label, silently, for anyone using a screen reader or clicking a
    # caption. Chrome reported five unlabelled controls on this page and that is what they were.
    # A prefix would also separate the ids, but it renames the fields too, and then this data no
    # longer binds — the e-mail would come back merely «required» instead of malformed.
    invalid = ShowcaseForm(
        data={"full_name": "", "email": "pas-une-adresse", "profile": "", "message": ""},
        auto_id="id_err_%s",
    )
    invalid.is_valid()

    return render(
        request,
        "dev/showcase.html",
        {
            "noindex": True,
            "colour_groups": groups,
            "uncovered": uncovered,
            "type_scale": [
                {"slug": token.removeprefix("--t-"), "name": label, "note": note, "value": tokens.get(token, "—")}
                for token, label, note in TYPE_SCALE
            ],
            "motion": [{"name": token, "value": tokens.get(token, "—"), "note": note} for token, note in MOTION],
            "form": ShowcaseForm(),
            "invalid_form": invalid,
            "console_form": PasswordShowcaseForm(),
            "situation": _situation_form(),
            "answered_fields": set(),
            "journey": _demo_journey(),
            "health": DEMO_HEALTH,
            "doc_row": DEMO_DOC_ROW,
            "case_timeline": _demo_case_timeline(),
            "demo_needs": _demo_needs(),
            # A real ``Page``, not a dictionary that looks like one: the pagination component
            # reads ``has_previous``, ``has_next`` and ``paginator.num_pages``, and a stand-in
            # would let the component drift away from what the portal actually passes it.
            "page_obj": Paginator(range(47), 10).page(3),
            "tabs": DEMO_TABS,
            "accordion": DEMO_ACCORDION,
            "crumbs": DEMO_BREADCRUMBS,
            "timeline": DEMO_TIMELINE,
            "meta_items": DEMO_META,
            "rows": DEMO_TABLE,
            "steps": DEMO_STEPS,
            "dialog_body": DEMO_DIALOG_BODY,
            "dialog_actions": DEMO_DIALOG_ACTIONS,
            "dialog_light_body": DEMO_DIALOG_LIGHT_BODY,
            "badge_kinds": BADGE_KINDS,
            "notice_kinds": NOTICE_KINDS,
            "button_variants": BUTTON_VARIANTS,
            "icons": ICONS,
        },
    )
