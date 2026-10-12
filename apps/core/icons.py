"""
The ILE icon registry — one concept, one glyph (design V5: V5.4 plan §1.7; the research map
ICON_SEMANTIC_MAP.md on the design-research-v5 branch, «IC» below; decision log DL54).

Pure Python, no Django import: ``scripts/build_icons.py`` and the tests read this module as well as the
templates do.

What it holds
  SYMBOLS        every symbol of ``static/img/icons.svg`` — built from ``static/icons/src/<id>.svg`` by
                 ``scripts/build_icons.py`` — with its tier, its size floor and the origin of its geometry
                 (``docs/design-v5/ICON_LICENSES.md``). The sprite holds these and nothing else.
  MIN_SIZE       symbol → the smallest size in px at which it may render: the floor measured on the built
                 sprite (the sub-pixel space a 0.5 px closing adds at DPR 1 ≤ 10 %, the method of IC §11.1;
                 evidence/v54/w1-b/impl-1/measure/metrics.md), or the review's floor where that is stricter
                 (institution, university, factory, languages, house; handshake 24 since the senior review of
                 9 October 2026 — a seat below that redraws it first).
  FLIP_RTL       the closed list of symbols that mirror in Arabic. Direction mirrors, meaning does not: the
                 ``svg_icon`` tag adds ``icon--flip-rtl`` to these and to no other.
  TWINS          the groups whose members read alike at 16 px: never two members in one list, menu, row or
                 notice set.
  CHECK_BEARING  the four symbols that draw a check, and the only places each may appear.
  SHARED         the reviewed exceptions to «one glyph, one concept»: one symbol under two keys that are one
                 concept seen from two places.
  the concept maps — AUDIENCE, ACTOR, NAV, COMPANY_NAV, CARD, PATHWAY, LIVING, JOURNEY, STATUS, NOTICE, DUE,
                 ALERT: a concept reaches a template through ``concept(domain, key)`` (the ``concept``
                 filter, the ``actor_glyph`` filter), never as a literal.
  LEGACY         the V4-only ids that producers outside the icon family still emit until their owners sweep
                 them (a dashboard card, the living catalogue, the pathways' defaults): resolved here to a V5
                 symbol, never drawn as such.

The tiers (plan §1.7): identity — drawn from the mark, never toned, never mirrored; concept — audiences,
actors, domains, phases, may carry the 12 % tone; utility — actions, direction, feedback, monoline, never
toned; status — «i cerchi», outline = open, filled = settled, painted by their chip.
"""

from __future__ import annotations

from dataclasses import dataclass

SPRITE = "img/icons.svg"
#: The ceiling of the built sprite, raw bytes (plan §2.6 «Sprite»).
SPRITE_MAX_BYTES = 32 * 1024

IDENTITY, CONCEPT, UTILITY, STATUS_TIER = "identity", "concept", "utility", "status"
TIERS = (IDENTITY, STATUS_TIER, CONCEPT, UTILITY)

#: The size classes of the svg_icon tag → px (plan §1.7, «Sizes and stroke»).
SIZE_CLASSES: dict[str, int] = {
    "icon--xs": 14,
    "icon--sm": 16,
    "icon--md": 20,
    "icon--lg": 24,
    "icon--xl": 32,
    "icon--hero": 48,
}

LUCIDE_VERSION = "1.48.0"


@dataclass(frozen=True)
class Symbol:
    tier: str
    floor: int
    #: The Lucide icon whose geometry it draws (lucide-static 1.48.0, ISC; ICON_LICENSES.md), or "" for an
    #: ILE drawing — the project's own.
    donor: str = ""
    #: Words for the sheet and the documentation: what it stands for.
    meaning: str = ""


def _ile(tier: str, floor: int, meaning: str) -> Symbol:
    return Symbol(tier, floor, "", meaning)


def _lucide(tier: str, floor: int, meaning: str, donor: str = "") -> Symbol:
    return Symbol(tier, floor, donor or "=", meaning)


_I, _S, _C, _U = IDENTITY, STATUS_TIER, CONCEPT, UTILITY

#: Every symbol of the sprite. The order is the sheet's and the sprite's.
SYMBOLS: dict[str, Symbol] = {
    # ---- identity: the mark's own grammar ----------------------------------------------------------------
    "ile-arch": _ile(_I, 16, "the arrival, threshold B of the journey; the favicon"),
    "ile-key": _ile(_I, 14, "Espace réservé: access, sign in"),
    "ile-steps": _ile(_I, 14, "Mon parcours, the journey"),
    "ile-mark": _ile(_I, 20, "Équipe du projet, as an actor or a sender"),
    # ---- status: «i cerchi» --------------------------------------------------------------------------------
    "st-attesa": _ile(_S, 14, "attesa: missing, pending, draft"),
    "st-attesa-replace": _ile(_S, 14, "attesa: to replace"),
    "st-neutro": _ile(_S, 14, "neutro: filed, transmitted, closed"),
    "st-esame": _ile(_S, 14, "esame: in review, in progress"),
    "st-conforme": _ile(_S, 14, "conforme: valid, done — a plain disc, no glyph"),
    "st-azione": _ile(_S, 14, "azione: expired, review required"),
    "st-rifiuto": _ile(_S, 14, "rifiuto: not valid, rejected"),
    "st-nullo": _ile(_S, 14, "nullo: withdrawn, not applicable"),
    # ---- concept: the four audiences, the actors ---------------------------------------------------------
    "person": _ile(_C, 14, "Persona: the person, «vous»"),
    "building": _ile(_C, 14, "Impresa: the company, «Mon entreprise»"),
    "institution": _ile(_C, 16, "Istituzione: the institutions"),
    "university": _ile(_C, 16, "Università – Formazione: the training body"),
    "briefcase": _ile(_C, 14, "the appointed professional"),
    "stamp": _lucide(_C, 16, "the competent authority; threshold A of the journey"),
    "badge-dot": _ile(_C, 14, "the authorised actor (an accreditation, no check)"),
    "badge-check": _lucide(_C, 14, "the seal: an act of an authority only"),
    "circle-user-round": _lucide(_C, 14, "my account, the profile"),
    # ---- concept: the platform's domains ------------------------------------------------------------------
    "layout-dashboard": _lucide(_C, 16, "Tableau de bord"),
    "compass": _ile(_C, 14, "Ma situation, the orientation"),
    "signpost": _lucide(_C, 14, "Voies régulières; journey step 2"),
    "folder": _lucide(_C, 14, "Mes dossiers, the case file (Fascicolo)"),
    "document": _ile(_C, 14, "Mes pièces: the documents, a piece"),
    "send": _lucide(_C, 14, "Mes demandes: requests sent to the Guichet"),
    "calendar-clock": _lucide(_C, 14, "Mes échéances: the deadlines"),
    "mail": _ile(_C, 14, "Communications: the messages"),
    "concierge-bell": _lucide(_C, 20, "Guichet numérique: the help desk"),
    "inbox": _lucide(_C, 14, "requests entrusted to me (a professional's queue)"),
    "book-open": _lucide(_C, 14, "Academy; the training phase"),
    "list-ordered": _lucide(_C, 14, "selection processes: stages, in order"),
    "wrench": _lucide(_C, 20, "Mes besoins: a company's needs"),
    "map": _lucide(_C, 14, "Analyse territoriale"),
    "handshake": _ile(_C, 24, "Forum Vénétie–Maroc: the cooperation (the two cuffs merge at 20 px: review m3)"),
    "calendar-range": _lucide(_C, 20, "Forum: an edition"),
    "table": _lucide(_C, 14, "Forum: a working table"),
    "file-plus": _lucide(_C, 14, "Forum: a proposal"),
    "sprout": _lucide(_C, 14, "Vivre en Italie; journey step 7"),
    "settings": _ile(_C, 20, "administration, the back-office"),
    "bell": _lucide(_U, 14, "notifications"),
    "shield": _lucide(_C, 14, "Sécurité du compte"),
    "award": _lucide(_C, 14, "Diplômes et titres"),
    # ---- concept: the journey ------------------------------------------------------------------------------
    "scroll-text": _lucide(_C, 16, "journey step 4: procedures with the competent authorities"),
    "clipboard-list": _lucide(_C, 16, "journey step 5: preparing the departure"),
    "building-2": _lucide(_C, 16, "Services publics; journey step 6"),
    # ---- concept: selection and the regular pathways --------------------------------------------------------
    "pen-line": _lucide(_C, 14, "identity disclosure: the person's consent"),
    "factory": _lucide(_C, 16, "pathway: salaried work"),
    "id-card": _lucide(_C, 16, "pathway: the EU Blue Card"),
    "users": _lucide(_C, 14, "pathway: family reunification"),
    "store": _lucide(_C, 14, "pathway: self-employment"),
    "flask-conical": _lucide(_C, 14, "pathway: scientific research"),
    "split": _lucide(_C, 14, "pathway: the other regular routes"),
    # ---- concept: living in Italy ---------------------------------------------------------------------------
    "languages": _lucide(_C, 16, "the Italian language; the language control"),
    "house": _ile(_C, 16, "housing (Logement)"),
    "heart-pulse": _lucide(_C, 16, "health"),
    "stethoscope": _lucide(_C, 14, "the national health service (SSN)"),
    "school": _lucide(_C, 16, "school"),
    "vote": _lucide(_C, 14, "civic education — its own page only"),
    "scale": _lucide(_C, 16, "rights and duties"),
    "hard-hat": _lucide(_C, 16, "safety at work"),
    "receipt": _lucide(_C, 16, "basic taxation"),
    # ---- concept: contact and public specifics --------------------------------------------------------------
    "at-sign": _lucide(_C, 14, "an e-mail address"),
    "phone": _ile(_C, 20, "a phone number"),
    "map-pin": _ile(_C, 16, "an address, a place"),
    "shield-alert": _lucide(_C, 14, "Attention aux fraudes: the anti-fraud entry"),
    "megaphone": _lucide(_C, 14, "an institutional notice"),
    "book-a": _lucide(_C, 14, "the glossary"),
    "circle-help": _lucide(_C, 14, "the questions (FAQ)"),
    "newspaper": _lucide(_C, 20, "the news"),
    "hash": _lucide(_C, 14, "a reference number"),
    "history": _lucide(_C, 16, "what happened, in order: versions, the rules version, the case's history"),
    "quote": _ile(_C, 14, "a quotation, a testimony"),
    # ---- utility: actions, direction, feedback (monoline, never toned) --------------------------------------
    "upload": _lucide(_U, 14, "Déposer: upload a piece"),
    "refresh-cw": _lucide(_U, 14, "Remplacer: replace a piece"),
    "download": _ile(_U, 14, "Télécharger: download"),
    "eye": _lucide(_U, 16, "Consulter, show the password"),
    "eye-off": _lucide(_U, 16, "hide the password"),
    "trash-2": _lucide(_U, 14, "Supprimer: delete"),
    "plus": _ile(_U, 14, "Ajouter: add"),
    "minus": _ile(_U, 14, "Retirer: remove"),
    "pencil": _lucide(_U, 14, "Modifier: edit"),
    "copy": _lucide(_U, 14, "Copier: copy"),
    "mail-open": _lucide(_U, 14, "Marquer comme lu: mark as read"),
    "list-filter": _lucide(_U, 14, "Filtrer: filter"),
    "arrow-down-up": _lucide(_U, 14, "Trier: sort"),
    "printer": _lucide(_U, 14, "Imprimer: print"),
    "search": _ile(_U, 14, "Rechercher, Aller à…"),
    "arrow": _ile(_U, 14, "forward: a primary action, a whole-row target"),
    "arrow-start": _ile(_U, 14, "back, previous"),
    "arrow-up-right": _ile(_U, 14, "an external link (an authority's site)"),
    "chevron": _ile(_U, 14, "a disclosure: it turns 180°"),
    "chevron-end": _ile(_U, 14, "a forward disclosure, the breadcrumb separator"),
    "close": _ile(_U, 14, "Fermer: close"),
    "check": _ile(_U, 14, "the person's own act: a chosen option, a ticked box"),
    "menu": _ile(_U, 14, "the menu"),
    "ellipsis-vertical": _lucide(_U, 14, "a row's or a piece's actions"),
    "panel-left-close": _lucide(_U, 14, "collapse or expand the rail"),
    "logout": _ile(_U, 14, "Se déconnecter: sign out"),
    "lock": _ile(_U, 14, "blocked (the blocco register)"),
    # ---- utility: notices and time -----------------------------------------------------------------------
    "info": _ile(_U, 14, "notice: information"),
    "warning": _ile(_U, 14, "notice: warning"),
    "circle-alert": _lucide(_U, 14, "notice: error"),
    "clock": _ile(_U, 14, "notice: pending; a due date that is soon"),
    "circle-pause": _lucide(_U, 14, "notice: unavailable"),
    "circle-check": _lucide(_U, 14, "the person's own account act, done (an allauth success)"),
    "calendar": _ile(_U, 16, "a date; a due date that is upcoming"),
    "alarm-clock": _lucide(_U, 20, "a due date that is overdue (10.9 % sub-pixel space at 16 px, measured)"),
    "empty": _ile(_U, 16, "nothing here yet: the neutral mark of an empty state whose space has no glyph of its own"),
}

# A Lucide donor's name is its symbol's id (the map's own rule: the id says what it draws).
SYMBOLS = {name: Symbol(s.tier, s.floor, name, s.meaning) if s.donor == "=" else s for name, s in SYMBOLS.items()}

#: The groups of the sheet and of DS 2026 §13 (Italian, like the document), in the sprite's order.
GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Identità — dal marchio", ("ile-arch", "ile-key", "ile-steps", "ile-mark")),
    (
        "Stati — «i cerchi»",
        ("st-attesa", "st-attesa-replace", "st-neutro", "st-esame", "st-conforme", "st-azione", "st-rifiuto",
         "st-nullo"),
    ),
    (
        "Pubblici e soggetti",
        ("person", "building", "institution", "university", "briefcase", "stamp", "badge-dot", "badge-check",
         "circle-user-round"),
    ),
    (
        "Domini della piattaforma",
        ("layout-dashboard", "compass", "signpost", "folder", "document", "send", "calendar-clock", "mail",
         "concierge-bell", "inbox", "book-open", "list-ordered", "wrench", "map", "handshake", "calendar-range",
         "table", "file-plus", "sprout", "settings", "bell", "shield", "award"),
    ),
    ("Il percorso", ("scroll-text", "clipboard-list", "building-2")),
    ("Selezione e vie regolari", ("pen-line", "factory", "id-card", "users", "store", "flask-conical", "split")),
    (
        "Vivere in Italia",
        ("languages", "house", "heart-pulse", "stethoscope", "school", "vote", "scale", "hard-hat", "receipt"),
    ),
    (
        "Contatti e pagine pubbliche",
        ("at-sign", "phone", "map-pin", "shield-alert", "megaphone", "book-a", "circle-help", "newspaper", "hash",
         "history", "quote"),
    ),
    (
        "Azioni e direzione",
        ("upload", "refresh-cw", "download", "eye", "eye-off", "trash-2", "plus", "minus", "pencil", "copy",
         "mail-open", "list-filter", "arrow-down-up", "printer", "search", "arrow", "arrow-start", "arrow-up-right",
         "chevron", "chevron-end", "close", "check", "menu", "ellipsis-vertical", "panel-left-close", "logout", "lock"),
    ),
    (
        "Avvisi e tempo",
        ("info", "warning", "circle-alert", "clock", "circle-pause", "circle-check", "calendar", "alarm-clock",
         "empty"),
    ),
)

#: symbol → its size floor in px.
MIN_SIZE: dict[str, int] = {name: symbol.floor for name, symbol in SYMBOLS.items()}

#: The closed flip list (plan §1.7 «RTL»; IC §7). `milestone` left the sprite (a twin of `signpost`), so it
#: left the list. Never mirrored: everything else — the identity tier (`ile-steps` included, Q8), every status
#: mark, every audience glyph, `arrow-up-right`, `history`, `refresh-cw`, `list-ordered`, `split`.
FLIP_RTL: frozenset[str] = frozenset(
    {"arrow", "arrow-start", "chevron-end", "logout", "send", "signpost", "panel-left-close"}
)

#: Groups whose members read alike at 16 px (similarity ≥ 0.75, IC §11.6; re-measured on the built sprite, 8 Oct
#: 2026, C:/tmp/ile_v5_council/evidence/v54/w1-b/impl-1/measure/metrics.md): never two members in one list, menu,
#: row or notice set. The circle family is ONE group now that `info` and `clock` are drawn at the donors' radius
#: (rule 12, one live area): info / circle-alert 0.94, circle-alert / clock 0.89, circle-help / info 0.84, and
#: `compass` / circle-pause 0.76 — the «i» and the «!» differ by which end carries the dot, which is the convention
#: every reader knows; a notice therefore never rests on its glyph (IC §3.7, the family rule).
TWINS: tuple[frozenset[str], ...] = (
    frozenset({"st-conforme", "st-azione", "st-rifiuto"}),
    frozenset({"info", "clock", "circle-alert", "circle-help", "circle-pause", "circle-check", "compass"}),
    frozenset({"badge-check", "badge-dot"}),
    frozenset({"pen-line", "pencil"}),
    frozenset({"building-2", "school"}),
    frozenset({"shield", "shield-alert"}),
)

#: The symbols that draw a check, and the only places each may appear (IC §2, «the check rule»): never in a
#: chip, a journey node or station, the ledger, a rail, an actor disc or a filter chip.
CHECK_BEARING: dict[str, str] = {
    "check": "the person's own interface act: a chosen option card, a ticked box",
    "circle-check": "the person's own account act, done: an allauth success alert",
    "badge-check": "the seal: an act of an authority, never the project's own",
    "vote": "the civic-education topic, on its own page",
}

# ---- the concept maps ------------------------------------------------------------------------------------

#: The four audiences (the entrances, the hero's legend, the network page): Persona ≠ Impresa ≠ Istituzione
#: ≠ Università.
AUDIENCE: dict[str, str] = {
    "person": "person",
    "company": "building",
    "institution": "institution",
    "university": "university",
}

#: Who acts — cases.ResponsibleActor, companies.ActorRole and cases.AssignmentRole (IC §3.4). One glyph per
#: actor, on the row, never a check. `operator` has none: the dashed disc.
ACTOR: dict[str, str] = {
    "person": "person",
    "company": "building",
    "authority": "stamp",
    "professional": "briefcase",
    "training_body": "university",
    "authorised_actor": "badge-dot",
    "project_team": "ile-mark",
}

#: The person's console rail, its bottom bar and its drawer (IC §5): portal.services.NAV_GLYPHS IS this map
#: (review fix M1, 9 October 2026) — the journey is the mark's steps, a case its folder, the help desk its
#: bell, the Academy its book; `briefcase`, `handshake`, `university` and `calendar` mean in the rail what they
#: mean everywhere else, so they are not in it. A key is added here first (tests/frontend/test_icons.py).
NAV: dict[str, str] = {
    "dashboard": "layout-dashboard",
    "situation": "compass",
    "pathways": "ile-steps",
    "cases": "folder",
    "requests": "send",
    "documents": "document",
    "deadlines": "calendar-clock",
    "messages": "mail",
    "helpdesk": "concierge-bell",
    "academy": "book-open",
    "selection": "list-ordered",
    "company": "building",
    "helpdesk-queue": "inbox",
    # the dispatch desk, an operator's register: a row of the rail on every page since the console shell builds
    # one rail per space (W3-A, plan §1.18 D06) — `settings` is the back-office's glyph and has no other seat
    "helpdesk-dispatch": "settings",
    # «Communications d’identité», a person's own panel: a row of the rail for the account somebody has asked
    # (W3-A) — `pen-line` is this registry's glyph for that consent, and has no other seat in a rail
    "disclosures": "pen-line",
}

#: The company workspace's rail, bottom bar and drawer: companies.services.navigation draws each entry from
#: this map (review fix M1) — the needs are a wrench, the analysis a map.
COMPANY_NAV: dict[str, str] = {
    "dashboard": "layout-dashboard",
    "needs": "wrench",
    "profile": "building",
    "analysis": "map",
    "messages": "mail",
}

#: The dashboard's cards, by the keys of portal.services' card builders — and the glyph of each card's empty
#: page (the domain's concept glyph, IC §3.7).
CARD: dict[str, str] = {
    "requests": "send",
    "orientation": "compass",
    "documents": "document",
    "deadlines": "calendar-clock",
    "messages": "mail",
    "organisation": "building",
}

#: The eight regular pathways, by their key (IC §3.5): once per page — the detail's eyebrow, the register rows.
PATHWAY: dict[str, str] = {
    "salaried_work": "factory",
    "skilled_work_eu_blue_card": "id-card",
    "training_in_origin_country": "book-open",
    "study_and_training_in_italy": "university",
    "family_reunification": "users",
    "self_employment_entrepreneurship": "store",
    "scientific_research": "flask-conical",
    "other_regular_routes": "split",
}

#: The ten topics of «Vivre en Italie», by slug (IC §3.6): on the topic's own page only — the index of the
#: ten is typographic (ten glyphs on one public page, and `building-2` / `school` are twins).
LIVING: dict[str, str] = {
    "langue-italienne": "languages",
    "logement": "house",
    "sante": "heart-pulse",
    "service-sanitaire-national": "stethoscope",
    "ecole": "school",
    "education-civique": "vote",
    "droits-et-devoirs": "scale",
    "securite-au-travail": "hard-hat",
    "fiscalite-de-base": "receipt",
    "services-publics": "building-2",
}

#: The journey: the seven steps of portal.services.JOURNEY_STEPS by status, and the two thresholds (IC §3.3).
#: A threshold and a station never share a label.
JOURNEY: dict[str, str] = {
    "draft": "compass",
    "oriented": "signpost",
    "training": "book-open",
    "threshold_a": "stamp",
    "admin_process": "scroll-text",
    "pre_departure": "clipboard-list",
    "threshold_b": "ile-arch",
    "entered": "building-2",
    "post_entry": "sprout",
}

#: «i cerchi»: a chip's register → its mark (IC §2). The chips (W1-C) read it; a template never chooses one.
STATUS: dict[str, str] = {
    "attesa": "st-attesa",
    "neutro": "st-neutro",
    "esame": "st-esame",
    "conforme": "st-conforme",
    "azione": "st-azione",
    "rifiuto": "st-rifiuto",
    "blocco": "lock",
    "nullo": "st-nullo",
    "seal": "badge-check",
}

#: The mark of an empty state whose space has no glyph of its own (review fix M3; IC §3.7 «Empty page»: «one
#: glyph that says which space is empty»). components/empty_state.html draws it when its caller passes none:
#: an empty PAGE passes its domain's concept glyph (the FAQ `circle-help`, the glossary `book-a`, the news
#: `newspaper`, the Forum `handshake`, «Vivre en Italie» `sprout`, a console list its own); a REGION under its
#: own heading, and a page whose domain the registry does not draw (the partners: IC keeps «Réseau» a word),
#: draw this one. Never `document` by default: that is «Mes pièces».
EMPTY_STATE = "empty"

#: A notice's kind → its mark (IC §3.7). A notice never rests on its glyph: the title names the kind.
NOTICE: dict[str, str] = {
    "info": "info",
    "warning": "warning",
    "error": "circle-alert",
    "pending": "clock",
    "unavailable": "circle-pause",
    "institutional": "megaphone",
    "success": "circle-check",
}

#: A due date's urgency → its mark. No urgency is a plain date and draws the date's own mark, `calendar`: the
#: rows of one list then carry a glyph each or none (a glyph column is all or nothing), never some.
DUE: dict[str, str] = {
    "": "calendar",
    "upcoming": "calendar",
    "soon": "clock",
    "overdue": "alarm-clock",
}

#: An allauth message's level → its mark (fixes V4's «always info»; `circle-check` only for the person's own
#: account acts — signed in, e-mail confirmed, password changed).
ALERT: dict[str, str] = {
    "debug": "info",
    "info": "info",
    "success": "circle-check",
    "warning": "warning",
    "error": "circle-alert",
}

DOMAINS: dict[str, dict[str, str]] = {
    "audience": AUDIENCE,
    "actor": ACTOR,
    "nav": NAV,
    "company_nav": COMPANY_NAV,
    "card": CARD,
    "pathway": PATHWAY,
    "living": LIVING,
    "journey": JOURNEY,
    "status": STATUS,
    "notice": NOTICE,
    "due": DUE,
    "alert": ALERT,
}

#: The domains rendered as ONE list, menu or row set: TWINS may not meet inside one of them.
LIST_DOMAINS: tuple[str, ...] = ("audience", "actor", "nav", "company_nav", "card", "pathway", "journey")

#: The reviewed exception register (IC §6): one symbol under two concept keys that are one concept.
SHARED: dict[str, str] = {
    "person": "the audience Persona, the person as an actor, «vous»: one person",
    "building": "the audience Impresa, the company as an actor, «Mon entreprise», «Mon organisation»: one company",
    "university": "the audience Università, the training body, the study pathway: study (Q9 — no backpack)",
    "book-open": "Academy, the training phase, the training pathway: training before the departure",
    "stamp": "the competent authority and threshold A: the authority's act",
    "signpost": "Voies régulières and journey step 2: the possible pathways",
    "building-2": "Services publics and journey step 6: the first formalities, with public services",
    "compass": "Ma situation, the orientation card and journey step 1: where the person stands",
    "sprout": "Vivre en Italie and journey step 7: life after the arrival",
    "document": "Mes pièces, a piece, the dashboard's documents card: the pieces",
    "send": "Mes demandes in the rail and on the dashboard: one domain",
    "calendar-clock": "Mes échéances in the rail and on the dashboard: one domain",
    "mail": "Communications in both rails and on the dashboard: one domain",
    "layout-dashboard": "the person's and the company's dashboards: one place, the dashboard",
    "info": "the information notice and the debug / info alert levels: one kind",
    "warning": "the warning notice and the warning alert level: one kind",
    "circle-alert": "the error notice and the error alert level: one kind",
    "circle-check": "the success notice and the success alert level: the person's own act, done",
    "calendar": "a date with no urgency and an upcoming due date: a date",
    "clock": "the pending notice and a due date that is soon: both are a wait (IC §11.2)",
}

#: V4-only ids still emitted by producers outside the icon family, each resolved to the V5 symbol of its
#: remaining use. The ``svg_icon`` tag resolves them, so a page's markup carries the V5 id; the sprite also
#: holds each one as an alias symbol drawing the target's geometry (plan §2.3), so a producer's literal id
#: still draws and the producers' own tests still find it. A template never writes one
#: (tests/frontend/test_icons.py), nor does the dev showcase's list; each leaves with its last producer:
#:   home  — living.catalogue («Logement») and the rows seeded from it; the admin's own example («ex. home»).
#:           It draws a house, as it always did (IC §4: `home` renamed `house`) — the rails, which used it
#:           for the dashboard, draw `layout-dashboard` from NAV since the review fix M1.
#:   list  — portal.services._requests_card (`icon="list"`, W3-B's dashboard presenters; the portal's
#:           compliance test reads that literal against the sprite). The card itself draws CARD's `send`.
#:   globe — living.catalogue («Langue italienne») and pathways.services.DEFAULT_ICONS (the EU Blue Card),
#:           with the rows seeded from them; both pages draw the registry's symbol by key or slug first.
#: `user` and `key` left on 9 October 2026 (the fix pass after the review): no producer emitted them any
#: more — the rails are NAV's, the navbar's plate writes `ile-key`, the showcase's list names symbols.
LEGACY: dict[str, str] = {
    "home": "house",
    "list": "send",
    "globe": "languages",
}


class UnknownIcon(ValueError):
    """A name that is neither a symbol of the sprite nor a registered V4 alias, or a key a domain lacks."""


def resolve(name: str) -> str:
    """The sprite symbol a name draws: the symbol itself, or the V5 symbol of a V4-only id."""
    name = str(name or "")
    if name in SYMBOLS:
        return name
    if name in LEGACY:
        return LEGACY[name]
    raise UnknownIcon(f"no icon called {name!r} (apps/core/icons.py)")


def concept(domain: str, key: object) -> str:
    """The symbol of `key` in a concept domain (AUDIENCE, ACTOR, NAV, …) — the registry's, never a literal."""
    try:
        mapping = DOMAINS[domain]
    except KeyError:
        raise UnknownIcon(f"no icon domain called {domain!r}") from None
    try:
        return mapping[str(key if key is not None else "")]
    except KeyError:
        raise UnknownIcon(f"the icon domain {domain!r} has no key {key!r}") from None


def floor_violation(symbol: str, css_class: str) -> int | None:
    """The size a size class asks for when it is below the symbol's floor, else None."""
    sizes = [SIZE_CLASSES[c] for c in str(css_class or "").split() if c in SIZE_CLASSES]
    if sizes and min(sizes) < MIN_SIZE[symbol]:
        return min(sizes)
    return None
