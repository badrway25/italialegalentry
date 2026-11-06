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
  the concept maps — AUDIENCE, ACTOR, NAV, COMPANY_NAV, CARD, PATHWAY, LIVING, JOURNEY, CHAPTER, STATUS, NOTICE,
                 DUE, ALERT: a concept reaches a template through ``concept(domain, key)`` (the ``concept``
                 filter, the ``actor_glyph`` filter, the ``chapter_mark`` tag), never as a literal.
  CHAPTER_OF     a section's anchor → its CHAPTER concept: the mark a chapter head draws, or none (V5.12 §7).
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
#: The second sprite (V5.12 §7, DECISIONS §4 «Sprite split», W2 — lane B): the domain concepts — the platform's
#: domains, the journey, the pathways, living in Italy, the Forum, the public pages' own subjects. `icons.svg` keeps
#: what every page's chrome draws (identity, status, audiences and actors, utility, notices), so a public page whose
#: sections name no domain concept fetches one sprite, and each file stays under its ceiling as the system grows.
SPRITE_DOMAIN = "img/icons-domain.svg"
#: The third sprite (V5.22, SECTION_SYSTEM_V2 §4.9, lane S): the page-only sprite of the V2 sections — the T2-size
#: copies
#: of the thirteen ILE marks (their T1 drawing is inline: templates/components/sezioni/marks/, built from
#: static/icons/marks/ on the 48-unit grid) and the Lucide glyphs V5.22 vendored for the sections' stations, seats and
#: tiles. icons.svg and icons-domain.svg stay untouched; only a page that draws a V2 section fetches this one.
SPRITE_MARKS = "img/icons-marks.svg"
SPRITES: tuple[str, ...] = (SPRITE, SPRITE_DOMAIN, SPRITE_MARKS)
#: The ceiling of each built sprite, raw bytes (plan §2.6 «Sprite»; DECISIONS §4: each under 32 KiB).
SPRITE_MAX_BYTES = 32 * 1024
#: The chrome sprite only ratchets down (DECISIONS §4: «below today's 31 049 B»).
CHROME_SPRITE_MAX_BYTES = 31_049
#: The marks sprite's own ceiling (V5.22 §4.9: «≤ 16 KiB»).
MARKS_SPRITE_MAX_BYTES = 16 * 1024

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
    # V5.12 W2 (lane B, DECISIONS §4): the operator is no longer the dashed disc — a person with the tool of a role
    "user-cog": _lucide(_C, 16, "the operator at work: the dispatch desk"),
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
    # V5.12 §7 (W1, lane B): the needs are the skills a job asks for, never a repair — `wrench` left the sprite.
    # Floor 20, the seat of the wrench it replaces (the rail draws 20 px); not re-measured below that.
    "briefcase-business": _lucide(_C, 20, "Mes besoins: a company's needs in skills and trades"),
    "map": _lucide(_C, 14, "Analyse territoriale"),
    "handshake": _ile(_C, 24, "Forum Vénétie–Maroc: the cooperation (the two cuffs merge at 20 px: review m3)"),
    "calendar-range": _lucide(_C, 20, "Forum: an edition"),
    "table": _lucide(_C, 14, "Forum: a working table"),
    "file-plus": _lucide(_C, 14, "Forum: a proposal"),
    "sprout": _lucide(_C, 14, "Vivre en Italie; journey step 7"),
    "settings": _ile(_C, 20, "administration, the back-office"),
    "bell": _lucide(_U, 14, "notifications"),
    "shield": _lucide(_C, 14, "Sécurité du compte"),
    "shield-check": _lucide(_C, 14, "a protection that is active: two-step verification on"),
    "award": _lucide(_C, 14, "Diplômes et titres"),
    # ---- concept: the V5.12 W2 symbols (lane B, DECISIONS §4 «Symbols to vendor») ---------------------------
    "presentation": _lucide(_C, 14, "training: a training body, the training phase, «Formation avant le départ»"),
    "list-checks": _lucide(_C, 14, "the steps to take: «Étapes», the next steps of a result"),
    "file-search": _lucide(_C, 14, "a review: a piece or a file to verify (the action; the status is st-azione)"),
    "book-text": _lucide(_C, 14, "a legal source: the texts, the official resources"),
    "earth": _lucide(_C, 16, "the country of origin: the stages before the departure"),
    "files": _lucide(_C, 16, "the documentation a pathway requires (the set, never one piece)"),
    "messages-square": _lucide(_C, 16, "Forum: the discussions"),
    "message-square-text": _lucide(_C, 14, "a written message: the contact form"),
    "mic": _lucide(_C, 14, "Forum: the speakers"),
    "mail-plus": _lucide(_C, 14, "the newsletter: subscribe to the news"),
    # V5.15 W3 (lane B, round 1): the ILE's own drawings for the forms' key concepts — the doorway of the mark in each
    "ile-referent": _ile(
        _C, 20, "the company and its referent: a person beside the doorway (the needs form's first step)"
    ),
    "ile-need": _ile(_C, 20, "a need in skills: the post opening on the doorway (the needs form's second step)"),
    "ile-review": _ile(_C, 20, "the review before sending: the sheet under the lens (a form's last step)"),
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
    "message-circle": _lucide(_C, 14, "WhatsApp: the messaging channel (V5.19; Lucide draws no brand mark)"),
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
    # ---- V5.22 (SECTION_SYSTEM_V2 §4.9, lane S): the thirteen ILE marks — here their T2-size copy (the 48-unit drawing
    # at half size, the sprite's 1.5 px line); their T1 drawing is inline, in its arch seat (MARK, below) -------------
    "ile-orienta": _ile(_C, 20, "orientation: the doorway and its compass needle (home S2, «la boussole»)"),
    "ile-percorso": _ile(_C, 20, "the regular pathways: three treads rising into the doorway (the Parcours folio)"),
    "ile-impresa": _ile(_C, 20, "companies: a sawtooth roof over the doorway's bay (the Entreprises folio)"),
    "ile-istituzione": _ile(_C, 20, "institutions: a pediment over four columns, the arch between them (the folio)"),
    "ile-sapere": _ile(_C, 20, "universities: an open book before the arch that rises from its gutter (the folio)"),
    "ile-formazione": _ile(_C, 20, "training, before and after: two arches on one sill joined by a route (the folio)"),
    "ile-forum": _ile(_C, 20, "the Forum Vénétie–Maroc: a cavea facing the speaker's arch (the Forum head)"),
    "ile-pilota": _ile(_C, 20, "the pilot project: Morocco's horseshoe and Veneto's ogee joined by one route"),
    "ile-scudo": _ile(_C, 16, "protection: a shield whose field is the key's keyhole («la protezione», the frauds)"),
    # the key's mark is the T5 identity in its seat (MARK, below); its sprite copy is a concept glyph of the V2
    # sections,
    # never the chrome's — the identity tier of this sprite registry is the chrome's own (icons.svg)
    "ile-accesso": _ile(_C, 20, "access: the key standing in the doorway (the reserved row: it turns on «CONNEXION»)"),
    "ile-domande": _ile(_C, 20, "the questions: the doorway's opening becomes a question mark (the FAQ answer)"),
    "ile-lessico": _ile(_C, 20, "the glossary: a page with an arched Latin initial (the term page's folio)"),
    "ile-vivere": _ile(_C, 20, "living in Italy: three roofs, the doorway, a sprout (the Vivre plate)"),
    # ---- V5.22 (§3, lane S): the Lucide glyphs the V2 sections' stations, seats and tiles need -----------------------
    "layers": _lucide(_C, 20, "the pilot's station 2: the profiles and competences a need is made of (never a person)"),
    "hand-helping": _lucide(_C, 20, "the pilot's station 7: the accompaniment after the arrival"),
    "calendar-sync": _lucide(_C, 20, "the pilot's station 8: the follow-up, over time"),
    "waypoints": _lucide(_C, 20, "the companies' second moment: the pathways built with the competent actors"),
    "map-pinned": _lucide(_C, 20, "the institutions' hemicycle: the communes, a place on the territory"),
    "landmark": _lucide(_C, 20, "a public body; a competent authority's seat (the hemicycle, a sheet's authority arc)"),
    "file-badge": _lucide(_C, 20, "the diplomas' station 4: the declaration of value (an act of an authority)"),
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
         "circle-user-round", "user-cog"),
    ),
    (
        "Domini della piattaforma",
        ("layout-dashboard", "compass", "signpost", "folder", "document", "send", "calendar-clock", "mail",
         "concierge-bell", "inbox", "book-open", "list-ordered", "briefcase-business", "map", "handshake",
         "calendar-range", "table", "file-plus", "sprout", "settings", "bell", "shield", "shield-check", "award"),
    ),
    (
        "Concetti V5.12",
        ("presentation", "list-checks", "file-search", "book-text", "earth", "files", "messages-square",
         "message-square-text", "mic", "mail-plus"),
    ),
    ("Moduli — disegni ILE (V5.15)", ("ile-referent", "ile-need", "ile-review")),
    ("Il percorso", ("scroll-text", "clipboard-list", "building-2")),
    ("Selezione e vie regolari", ("pen-line", "factory", "id-card", "users", "store", "flask-conical", "split")),
    (
        "Vivere in Italia",
        ("languages", "house", "heart-pulse", "stethoscope", "school", "vote", "scale", "hard-hat", "receipt"),
    ),
    (
        "Contatti e pagine pubbliche",
        ("at-sign", "phone", "message-circle", "map-pin", "shield-alert", "megaphone", "book-a", "circle-help",
         "newspaper", "hash", "history", "quote"),
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
    (
        "Marchi ILE V5.22 — copie T2 (il disegno T1 è in linea, nel suo seggio ad arco)",
        ("ile-orienta", "ile-percorso", "ile-impresa", "ile-istituzione", "ile-sapere", "ile-formazione", "ile-forum",
         "ile-pilota", "ile-scudo", "ile-accesso", "ile-domande", "ile-lessico", "ile-vivere"),
    ),
    (
        "Concetti V5.22 — stazioni, seggi, tessere",
        ("layers", "hand-helping", "calendar-sync", "waypoints", "map-pinned", "landmark", "file-badge"),
    ),
)

#: The symbols of the domain sprite (SPRITE_DOMAIN); every other symbol is the chrome sprite's. The chrome keeps
#: what the header, the footer, the account menu, the rails' frame, the notices, the chips and the forms draw on every
#: page: identity, status, the audiences and actors, the utility glyphs, the notices, the contact glyphs of the footer,
#: the anti-fraud entry and the Forum's door of the navigation, the account's security.
DOMAIN_SYMBOLS: frozenset[str] = frozenset({
    # the platform's domains (the console rails, the dashboard's cards)
    "layout-dashboard", "compass", "signpost", "folder", "document", "send", "calendar-clock", "mail", "concierge-bell",
    "inbox", "book-open", "list-ordered", "briefcase-business", "map", "calendar-range", "table", "file-plus",
    "sprout", "settings", "award",
    # the journey, selection and the regular pathways, living in Italy
    "scroll-text", "clipboard-list", "building-2", "pen-line", "factory", "id-card", "users", "store",
    "flask-conical", "split", "languages", "house", "heart-pulse", "stethoscope", "school", "vote", "scale",
    "hard-hat", "receipt",
    # the public pages' own subjects
    "book-a", "circle-help", "newspaper", "hash", "history", "quote",
    # the V5.12 concepts, all but the account's security; the operator's desk in the rail
    "user-cog", "presentation", "list-checks", "file-search", "book-text", "earth", "files", "messages-square",
    "message-square-text", "mic", "mail-plus",
    # V5.15 W3: the forms' ILE drawings (the steps' tiles)
    "ile-referent", "ile-need", "ile-review",
})

#: The symbols of the marks sprite (SPRITE_MARKS, V5.22 §4.9): the thirteen marks' T2 copies and the glyphs V5.22
#: vendored — the two V5.12 sprites stay untouched.
MARKS_SYMBOLS: frozenset[str] = frozenset({
    "ile-orienta", "ile-percorso", "ile-impresa", "ile-istituzione", "ile-sapere", "ile-formazione", "ile-forum",
    "ile-pilota", "ile-scudo", "ile-accesso", "ile-domande", "ile-lessico", "ile-vivere",
    "layers", "hand-helping", "calendar-sync", "waypoints", "map-pinned", "landmark", "file-badge",
})

#: symbol → the sprite file that holds it (static path); a V4 alias lives in its target's sprite.
SPRITE_OF: dict[str, str] = {
    name: SPRITE_MARKS if name in MARKS_SYMBOLS else SPRITE_DOMAIN if name in DOMAIN_SYMBOLS else SPRITE
    for name in SYMBOLS
}

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
    frozenset({"shield", "shield-alert", "shield-check"}),
    # V5.12 W2 (by drawing, not measured): three lines with a mark at their start; two speech bubbles; a sheet, a
    # stack of sheets and a sheet under a lens
    frozenset({"list-ordered", "list-checks"}),
    frozenset({"messages-square", "message-square-text"}),
    frozenset({"document", "files", "file-search"}),
    # one case outline: the professional and the company's needs (V5.12 W1 — by drawing, not measured)
    frozenset({"briefcase", "briefcase-business"}),
    # V5.22 (by drawing, not measured): a pin and a pin over its ground; two classical fronts — never side by side
    frozenset({"map-pin", "map-pinned"}),
    frozenset({"institution", "landmark"}),
)

#: The symbols that draw a check, and the only places each may appear (IC §2, «the check rule»): never in a
#: chip, a journey node or station, the ledger, a rail, an actor disc or a filter chip.
CHECK_BEARING: dict[str, str] = {
    "check": "the person's own interface act: a chosen option card, a ticked box, the language the person chose",
    "circle-check": "the person's own account act, done: an allauth success alert",
    "badge-check": "the seal: an act of an authority, never the project's own",
    "vote": "the civic-education topic, on its own page",
    "list-checks": "a chapter head «Étapes» / next steps: steps to read, never a state, a chip or a rail",
    "shield-check": "the account's security overview: a protection the person has turned on (two-step verification)",
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
#: actor, on the row, never a check. `operator` is not a responsible actor (it has none: the dashed disc); its desk,
#: the dispatch, draws `user-cog` in the rail (NAV). Since V5.12 W2 the training body draws `presentation`: the
#: university's own glyph is the university's alone (DECISIONS §4).
ACTOR: dict[str, str] = {
    "person": "person",
    "company": "building",
    "authority": "stamp",
    "professional": "briefcase",
    "training_body": "presentation",
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
    # one rail per space (W3-A, plan §1.18 D06) — the operator at work, `user-cog` (V5.12 W2, DECISIONS §4: it was
    # the back-office's `settings`, a cog that said «configuration»)
    "helpdesk-dispatch": "user-cog",
    # «Communications d’identité», a person's own panel: a row of the rail for the account somebody has asked
    # (W3-A) — `pen-line` is this registry's glyph for that consent, and has no other seat in a rail
    "disclosures": "pen-line",
}

#: The company workspace's rail, bottom bar and drawer: companies.services.navigation draws each entry from
#: this map (review fix M1) — the needs are the business case (V5.12 §7: a wrench read «repair»), the analysis a map.
COMPANY_NAV: dict[str, str] = {
    "dashboard": "layout-dashboard",
    "needs": "briefcase-business",
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
    "training_in_origin_country": "presentation",
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
    "training": "presentation",
    "threshold_a": "stamp",
    "admin_process": "scroll-text",
    "pre_departure": "clipboard-list",
    "threshold_b": "ile-arch",
    "entered": "building-2",
    "post_entry": "sprout",
}

#: The chapter mark (V5.12 §7, W1 — lane B): the glyph a section head draws above its title says the section's
#: CONCEPT, or the head draws none. Until V5.12 every head drew `ile-steps`, the journey's own mark, above 83 unrelated
#: titles («Par e-mail», «Documentation», «Avertissements», the Forum's programme…): that stair now belongs to «Mon
#: parcours» alone (NAV["pathways"]; tests/frontend/test_icons.py). An editorial section («En bref», «Pourquoi»,
#: «Pour aller plus loin») and a section whose concept the sprite does not draw yet carry no glyph: the title is the
#: device. Never twice on one page for two concepts, never the audience a door already shows in its own entrance.
#: Keys are concepts; CHAPTER_OF says which anchors draw them. W2 (V5.12, DECISIONS §4) vendored the symbols the W1
#: map waited for: «Étapes» `list-checks`, «Ressources» / «Sources officielles» `book-text`, the contact form
#: `message-square-text`, the speakers `mic`, the discussions `messages-square`, training `presentation`, the
#: newsletter `mail-plus`, and «Documentation généralement requise» the set of pieces, `files`.
CHAPTER: dict[str, str] = {
    "orientation": "compass",
    "pathways": "signpost",
    "authorities": "stamp",
    "documents": "files",
    "training": "presentation",
    "steps": "list-checks",
    "legal-sources": "book-text",
    "contact-form": "message-square-text",
    "newsletter": "mail-plus",
    "forum-speakers": "mic",
    "forum-discussions": "messages-square",
    "email": "at-sign",
    "telephone": "phone",
    "news": "newspaper",
    "faq": "circle-help",
    "forum-agenda": "calendar-range",
    "forum-rooms": "table",
    "company-needs": "briefcase-business",
    "institutions": "institution",
    "companies": "building",
    "universities": "university",
    "professionals": "briefcase",
    "italy": "ile-arch",
}

#: A section's anchor (the id of its title, which the chapter partials receive as ``title_id``) → its CHAPTER
#: concept. An anchor that is not here draws no mark. One anchor names one kind of section wherever it appears
#: («orientation-chapter-title» closes every pathway sheet), so the map stays short.
CHAPTER_OF: dict[str, str] = {
    # the home, under the frozen hero
    "home-orientation-title": "orientation",
    "home-pathways-title": "pathways",
    "home-news-title": "news",
    "home-ecosystem-title": "italy",
    # orientation and the regular pathways
    "how-title": "orientation",
    "pathway-title": "pathways",
    "pathways-title": "pathways",
    "antifraud-more-title": "pathways",
    "training-title": "training",
    "orientation-chapter-title": "orientation",
    "documentation-title": "documents",
    "etapes-title": "steps",
    "diploma-steps-title": "steps",
    "checklist-title": "steps",
    "ressources-title": "legal-sources",
    "sheet-sources-title": "legal-sources",
    "autorites-title": "authorities",
    "diploma-who-title": "authorities",
    # «Dans l'Espace Personnes» drew `ile-key` (the reserved area's key) above a list of public pages: V5.22 §4.10 ends
    # the misuse — the anchor says no concept, and its head draws nothing
    # contact, the promoter, the news
    "contact-email-title": "email",
    "contact-voice-title": "telephone",
    "agami-contact-title": "email",
    "newsletter-title": "newsletter",
    "contact-form-title": "contact-form",
    "related-title": "news",
    # the companies' needs form, on their door and on its own page
    "formulaire-header": "company-needs",
    "company-needs-form-title": "company-needs",
    # the Forum and its community
    "forum-next-events-title": "forum-agenda",
    "forum-programme-title": "forum-agenda",
    "agenda-heading": "forum-agenda",
    "rooms-heading": "forum-rooms",
    "discussions-heading": "forum-discussions",
    "forum-speakers-title": "forum-speakers",
    # the partners' groups, by kind (partners.PartnerKind): the audience a group is
    "partners-group-institution": "institutions",
    "partners-group-company": "companies",
    "partners-group-university": "universities",
    "partners-group-professional": "professionals",
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
    "chapter": CHAPTER,
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
    "building": "the audience Impresa, the company as an actor, «Mon entreprise», «Mon organisation», the partners' "
    "group of companies: one company",
    "institution": "the audience Istituzione and the partners' group of institutions: the institutions",
    "university": "the audience Università, the study pathway, the partners' group of universities: study at a "
    "university (Q9 — no backpack; the training body draws `presentation` since V5.12 W2)",
    "briefcase": "the appointed professional and the partners' group of professionals: the professional",
    "briefcase-business": "«Mes besoins» in the company's rail and the needs form's chapter: the company's needs",
    "presentation": "the training body, the training phase of the journey, the training pathway, the chapter "
    "«Formation avant le départ»: training before the departure (V5.12 W2; `book-open` is the Academy's alone)",
    "list-checks": "the chapters «Étapes» of a pathway sheet and of the diplomas page, a result's next steps: "
    "the steps",
    "book-text": "a pathway's «Ressources» and a living sheet's «Sources officielles»: the legal sources",
    "stamp": "the competent authority, threshold A and the chapters «Autorités» / «Qui décide ?»: the authority's act",
    "signpost": "Voies régulières, journey step 2 and the chapters that lead to them: the possible pathways",
    "ile-arch": "threshold B of the journey and the home's institutional ecosystem: Italy, the arrival",
    "building-2": "Services publics and journey step 6: the first formalities, with public services",
    "compass": "Ma situation, the orientation card, journey step 1 and the orientation chapters: where the person "
    "stands",
    "sprout": "Vivre en Italie and journey step 7: life after the arrival",
    "document": "Mes documents, a piece, the dashboard's documents card: the pieces",
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
    # V5.22 §3 (the Director's seats and stations, recorded by lane S)
    "earth": "the country of origin (the stages before the departure) and the partner countries' institutions of the "
    "institutions' hemicycle: the other shore",
    "hard-hat": "safety at work (its living topic) and the labour bodies of the institutions' hemicycle: work",
    "map": "the territorial analysis and the regions of the institutions' hemicycle: the territory",
    "landmark": "a public body of the institutions' hemicycle and a competent authority's seat on a sheet's arc: a "
    "public institution's building",
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


# ---- V5.22 — Icon Treatment V2 (SECTION_SYSTEM_V2 §4, lane S) ----------------------------------------------------


@dataclass(frozen=True)
class Mark:
    """A custom ILE mark (§4.9): drawn on the 48-unit grid (static/icons/marks/<id>.svg), inline at its T1 size in an
    arch seat (templates/components/sezioni/marks/_<id>.html, generated by scripts/build_icons.py), and as a T2-size
    copy in the marks sprite (SYMBOLS[id], SPRITE_MARKS)."""

    id: str
    tier: str  # "T1" a theme (in its arch seat); "T5" the identity (the key)
    #: the smallest size of its inline drawing in px — the small seat's 32 (§4.2); its sprite copy's floor is SYMBOLS'
    floor: int
    #: its purposeful motion, beyond the draw (§4.7, §4.9): the template and the sheet name the moving part
    motion: str = ""


#: concept → its mark (§4.9, §4.10 «MARKS maps concept → mark id, tier and floor (32)»).
MARKS: dict[str, Mark] = {
    "orientation": Mark("ile-orienta", "T1", 32, "the needle settles once from −25° after its draw"),
    "pathways": Mark("ile-percorso", "T1", 32, "the three treads draw one after another (3 × 120 ms)"),
    "companies": Mark("ile-impresa", "T1", 32, "the opening's tone deepens on the call's hover and focus"),
    "institutions": Mark("ile-istituzione", "T1", 32, "the pediment first, then the columns 60 ms apart"),
    "universities": Mark("ile-sapere", "T1", 32, "the pages draw outward from the gutter"),
    "training": Mark("ile-formazione", "T1", 32, "the route draws from the first arch to the second; the node lights"),
    "forum": Mark("ile-forum", "T1", 32, "the tiers draw outer to inner, then the light at the arch"),
    "pilot": Mark("ile-pilota", "T1", 32, "the route draws from Morocco's arch to Veneto's; never mirrored"),
    "protection": Mark("ile-scudo", "T1", 32, "the keyhole's tone deepens on the link's hover and focus"),
    "access": Mark("ile-accesso", "T5", 32, "the key turns 90° on its action's hover and focus"),
    "faq": Mark("ile-domande", "T1", 32, "the dot last"),
    "glossary": Mark("ile-lessico", "T1", 32, ""),
    "living": Mark("ile-vivere", "T1", 32, "the roofline draws, then the sprout rises 2 units"),
}
#: mark id → its Mark.
MARK: dict[str, Mark] = {mark.id: mark for mark in MARKS.values()}

#: The head folios (§0.1 «Folio seals in the heads», §3): the concept glyph a page head passes as its folio's `glyph`
#: → the T1 mark its small seat draws in the folio's place. A glyph not here (the contact's `map-pin`, the network's
#: `users` — the ring is that page's T1 —, the diplomas' `award`, the promoter's `scale`) leaves a typographic folio:
#: a Lucide disc in the folio's seat would be the old device.
FOLIO: dict[str, str] = {
    "compass": "ile-percorso",  # Parcours (PA-0): the seat at the spine's top
    "signpost": "ile-percorso",  # a pathway sheet: «Parcours régulier n/8»
    "factory": "ile-impresa",  # Entreprises (EN-0)
    "institution": "ile-istituzione",  # Institutions (IN-0)
    "school": "ile-sapere",  # Universités (U0): the `school` slip ends
    "presentation": "ile-formazione",  # Formation (F0)
    "shield-alert": "ile-scudo",  # Attention aux fraudes (AF0)
}

#: The pilot's eight stations (§3.3 PP-1), in the locked order of p3.pilot.sequence: never `ile-steps`, never a check,
#: never a twin of a PATHWAY glyph, never a glyph that suggests a selection of candidates. Station 6, the arrival
#: (`ile-arch`), is the page's one gold node. Lane S's choices: 2 `layers` (the profiles and competences a need is made
#: of — no person, no ranking), 7 `hand-helping` (the accompaniment), 8 `calendar-sync` (the follow-up over time).
#: Station 4, «Préparation avant le départ»: §3.3 names `list-checks`, but that glyph draws two ticks (CHECK_BEARING:
#: «never a state, a chip or a rail») and the same list says «never a check» (O14). The registry's own glyph for the
#: concept stands there instead: `clipboard-list`, the journey's «preparing the departure» (DOMAINS journey).
PILOT_STATION: tuple[str, ...] = (
    "briefcase-business", "layers", "presentation", "clipboard-list",
    "stamp", "ile-arch", "hand-helping", "calendar-sync",
)
#: The companies' three moments (§3.6 EN-1): the needs, the pathways built with the competent actors (`waypoints`, lane
#: S's choice — never `users`, the family pathway's), the training.
COMPANY_MOMENT: tuple[str, ...] = ("briefcase-business", "waypoints", "presentation")
#: The six seats of the institutions' hemicycle (§3.7 IN-1), in the order of p3.institutions.recipients: the regions,
#: the communes (`map-pinned`, lane S), the public bodies, the chambers of commerce, the labour bodies (`hard-hat`, lane
#: S — never `users`), the diplomatic and consular representations and the partner countries' institutions (`earth`;
#: `globe` is a V4 alias of `languages`).
RECIPIENT_SEAT: tuple[str, ...] = ("map", "map-pinned", "landmark", "briefcase", "hard-hat", "earth")
#: A competent authority on a pathway sheet's arc (§3.5 PS-2), each the same building, neutral ink.
AUTHORITY_SEAT = "landmark"
#: A pathway sheet's five milestones (§3.5 PS-1) and the diplomas' five stations (§3.10 D1). Milestone 4,
#: «Préparation», takes `clipboard-list` for §3.5's `list-checks`, for the reason given at PILOT_STATION (O14). The
#: diplomas' third station keeps `badge-check`: the seal, an authority's act (CHECK_BEARING), and the one check a
#: sequence may hold.
SHEET_STEP: tuple[str, ...] = ("compass", "files", "stamp", "clipboard-list", "ile-arch")
DIPLOMA_STEP: tuple[str, ...] = ("files", "languages", "badge-check", "file-badge", "stamp")
#: «Comment ça marche» (§3.1 S2 — station 1 drawn as the T1 `ile-orienta` seal there —, §3.4 PA-2): the four stations.
HOW_STEP: tuple[str, ...] = ("compass", "info", "presentation", "stamp")


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


def chapter_glyph(key: object) -> str:
    """
    The mark of a chapter head: ``key`` is the section's anchor (its title's id) or a CHAPTER concept itself (for a
    head whose anchor is built at render time, an FAQ group); "" when the section says no concept — the head then
    draws no glyph. Never `ile-steps`: that is the journey's (NAV["pathways"]).
    """
    key = str(key or "")
    return CHAPTER.get(CHAPTER_OF.get(key, key), "")


def floor_violation(symbol: str, css_class: str) -> int | None:
    """The size a size class asks for when it is below the symbol's floor, else None."""
    sizes = [SIZE_CLASSES[c] for c in str(css_class or "").split() if c in SIZE_CLASSES]
    if sizes and min(sizes) < MIN_SIZE[symbol]:
        return min(sizes)
    return None
