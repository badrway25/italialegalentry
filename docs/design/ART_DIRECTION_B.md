# ART DIRECTION B — Contemporary Legal Diplomacy

> **Documento incompleto.** L'agente che ha prodotto questa direzione ha restituito un testo
> troncato: il file comincia a metà di una frase, nella sezione sul comportamento bidirezionale.
> Le sezioni 1–16 non sono pervenute. È conservato così com'è, senza ricostruzioni, perché il
> materiale presente è reale e verificabile mentre una ricostruzione non lo sarebbe.
>
> La giuria lo ha valutato su ciò che era leggibile — i wireframe, la suite di test T1–T13, la
> lista di demolizione, la guardia contro l'impersonificazione istituzionale e i costi — e lo ha
> classificato terzo (318/400 contro 338 di A e 339,5 di C). Il giudice di prodotto ha annotato
> espressamente che quel punteggio riflette «materiale visibile forte e una metà illeggibile, non
> un giudizio che la metà mancante sia debole».
>
> **Da questa direzione è stato adottato l'elemento più importante dell'intero Design Council: la
> barra di giurisdizione.** Tutti e quattro i giudici l'hanno indicata indipendentemente come
> innesto obbligatorio. Vedere `ART_DIRECTION_DECISION.md`.

---

)` with `direction: ltr`, so `text-align: start` resolves to **left** and every fallback block flies to the opposite margin — the Forum hero's two lines begin 1136px apart, and the pathway rows put the number at x=1288 and the title at x=492 with ~760px of void between them, eight times.

The contract, stated as three rules:

1. A block **never** changes direction. `dir` and `unicode-bidi: isolate` are set on the inline `<bdi>` only. The block keeps the page direction and `text-align: start` → right.
2. Any element carrying a fallback `lang` gets `dir` from the **same** template tag, or neither. `{% locked %}` / `cms.translation.resolve()` emit both or nothing.
3. Inside a register row, an entrance row or a table cell, the number, the state chip, the jurisdiction mark and the arrow are pinned to the row's Arabic edges **regardless of the title's language**. The Latin title is an island inside the row, not a re-alignment of it.

Test change: `test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` must walk **text nodes**, not elements. The current version checks elements that already carry `lang`, which is why the nav string, the wizard `<legend>`, the three Forum-banner children and the utility bar all pass while being unmarked.

### 16.5 Direction of the graphic language

| device | RTL behaviour |
|---|---|
| rail | mirrors to the inline end (right) |
| apparatus | mirrors to the inline start (left) |
| hatch | 45° → **135°**, so the trame always reads forward |
| jurisdiction bar | segments run right → left; the legend mirrors with them |
| T3 attention rule | draws right → left |
| arrows | one component emits the correct glyph per direction. Inside an isolated Latin run the arrow belongs to the run and stays `→` — **stated, so that two directions on one page is a decision, not the accident it is today** |
| numerals | Western digits, tabular, wrapped by the isolation tag inside Arabic sentences |
| ™ © | wrapped by the same tag (today the FAQ lead renders `™Italy Legal Entry` and the footer strands a full stop at the left edge) |

### 16.6 The Arabic content gates

Three CI gates, each failing the build rather than filing a ticket:

- **Coverage:** `<main>` target-script share per route, with a per-route floor. Ordered by risk, not by sitemap: anti-fraud → FAQ → orientation → parcours → forum.
- **Prescribed ceiling:** §16.3.
- **Metrics:** §16.1 line-box assertion + Latin↔Arabic ink parity within 5%.

Until a page passes coverage, it is not served at `/ar/` as though it were Arabic: it carries an honest Arabic notice and a one-paragraph Arabic summary at the top. An empty slot is better art direction than a French paragraph in an RTL column.

### 16.7 The language control

Four inline items at 15px in the utility bar (§4.1), `FR · AR · IT · EN`, no dropdown. `dir` is set on the **label span only**, not on the row, so the Arabic option keeps the same column alignment as the other three instead of looking like a rendering fault.

---

## 17. Wireframes

### 17.1 Home, above the fold, 1440 × 900 (fr)

```
0     ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
      │ AGAMI — Dialogo Giuridico Interculturale APS · promoteur du projet                           │ 40  --field
      │                                                       FR · AR · IT · EN    ⌷ Espace réservé  │
40    ├──────────────────────────────────────────────────────────────────────────────────────────────┤
      │  ┌──┐                                                                                        │ 64  --paper-0
      │  │▌▬│  Italy Legal Entry™                Personnes  Entreprises  Institutions  Universités   │
      │  └──┘  Écosystème institutionnel · Vénétie–Maroc                              ☰ Sommaire     │
104   ╞══════════════════════════════════════════════════════════════════════════════════════════════╡ 2px --ink, 100vw
      │                                                                                              │
      │   ← 40 →│  RAIL 176  │32│      INSTRUMENT 896 (12 sub-cols)      │32│  APPARATUS 224  │← 40 →│
      │                                                                                              │
      │         VÉNÉTIE—MAROC                                                                        │ 96 pad
      │                        Un écosystème                                                         │
      │         Promu par      pour les parcours                              Pré-évaluations à      │  --field
      │         AGAMI —        réguliers vers l'Italie                        caractère informatif.  │  band
      │         Dialogo        ── 88/92 Newsreader 400, --on-field, cols 1–9  Ne se substituent pas  │  to 754
      │         Giuridico                                                     aux autorités          │
      │         Inter-         Orientation, formation avant le départ et      compétentes.           │
      │         culturale      accompagnement, avec les acteurs compétents.                          │
      │         APS            ── standfirst 22 italic, --on-field-muted, 1–7                        │
      │                                                                                              │
      │                        ┌───────────────────────────────┐  ┌──────────────────────────┐       │
      │                        │ Commencer l'orientation     → │  │  Espace entreprises   →  │       │
      │                        └───────────────────────────────┘  └──────────────────────────┘       │
      │                                                                                              │
      │         ▤ Italie       ▤▤▤▤▤▤▨▨▨▨▨▨▨▨▨▨▨▨▢▢▢▢▨▨▨▨▨▮▮▮▮▮▮▮▮▮▮▤▤▤▤▤▤▤▤▤▤  ← jurisdiction bar   │
      │         ▨ Maroc        01 Besoin  02 Compétences  03 Formation  04 Préparation               │
      │         ▢ Plateforme   05 Procédure régulière     06 Entrée et accompagnement                │
      │         ▮ Autorité                                                    Le modèle en détail →  │
754   ╞══════════════════════════════════════════════════════════════════════════════════════════════╡ 3px --on-field
      │                                                                                              │  --paper-0
      │         QUATRE ESPACES │  01  Personnes                                       ▨▤    →        │ 96px row
      │                        │      s'orienter vers une voie régulière et se préparer avant le     │
      │                        │  ────────────────────────────────────────────────────────────       │
900   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│  02  Entreprises                                     ▤     →  ─ ─ ─ │ FOLD
      │                        │      exprimer les besoins de votre entreprise en métiers et …       │
      │                        │  ────────────────────────────────────────────────────────────       │
      │                        │  03  Institutions                                    ▨▤    →        │
      │                        │  ────────────────────────────────────────────────────────────       │
      │                        │  04  Universités et organismes de formation          ▨▤    →        │
      └──────────────────────────────────────────────────────────────────────────────────────────────┘
```

What is above the fold that is not today: the four audiences (row 1 fully, row 2 beginning), the model as a diagram, the legal caveat, and an 88px statement instead of a 48px one beside a 484px stock photograph.

### 17.2 Home, above the fold, 390 × 844 (fr)

```
0    ┌────────────────────────────────────────────┐
     │ AGAMI APS · promoteur                      │  40  --field
     │              FR AR IT EN   ⌷ Espace réservé│
40   ├────────────────────────────────────────────┤
     │ ┌──┐                                       │  56  --paper-0
     │ │▌▬│ Italy Legal Entry™        ☰ Sommaire  │
     │ └──┘                                       │
96   ╞════════════════════════════════════════════╡  2px --ink, edge to edge
     │ VÉNÉTIE—MAROC                              │      --field band
     │                                            │      16px side margins
     │ Un écosystème                              │
     │ pour les parcours                          │  40/44 Newsreader 400
     │ réguliers vers l'Italie                    │  3 lines = 132px
     │                                            │
     │ Orientation, formation avant le départ     │  19/28 italic
     │ et accompagnement, avec les acteurs        │  --on-field-muted
     │ compétents.                                │
     │                                            │
     │ ┌────────────────────────────────────────┐ │  44px primary,
     │ │  Commencer l'orientation             → │ │  full width
     │ └────────────────────────────────────────┘ │
     │   Espace entreprises →                     │  44px text link
     │                                            │
     │ ▤▤▤▤▨▨▨▨▨▨▨▨▢▢▢▨▨▨▮▮▮▮▮▮▤▤▤▤▤▤             │  6px jurisdiction bar
     │ 01 Besoin · 02 Compétences · 03 Formation  │  14px reference,
     │ 04 Préparation · 05 Procédure · 06 Entrée  │  wraps to 3 lines
     │ ▤ Italie ▨ Maroc ▢ Plateforme ▮ Autorité   │
     │ Le modèle en détail →                      │
600  ╞════════════════════════════════════════════╡  3px --on-field
     │ QUATRE ESPACES                             │  Rubric, 24px pad
     ├────────────────────────────────────────────┤  1px clause, edge to edge
     │ 01  Personnes                        ▨▤  → │  88px row, whole row
     │     s'orienter vers une voie régulière     │  is the target
688  ├────────────────────────────────────────────┤
     │ 02  Entreprises                      ▤   → │
     │     exprimer les besoins de votre …        │
776  ├────────────────────────────────────────────┤
     │ 03  Institutions                     ▨▤  → │
844  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   FOLD
     │     construire des coopérations …          │
     ├────────────────────────────────────────────┤
     │ 04  Universités et organismes        ▨▤  → │
     ╞════════════════════════════════════════════╡
     │ ART. 02 · LE MODÈLE            ☰ Sommaire  │  44 sticky index bar
     └────────────────────────────────────────────┘  appears from y≈952
```

### 17.3 Person dashboard, 1440 × 900

```
0    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
     │ ▌▬ Italy Legal Entry™  Espace de travail          FR ▾   ✉ 2   Aide   qa-person ▾        │ 48 --field
     │                                                                        ← Site public     │
48   ╞══════════════════════════════════════════════════════════════════════════════════════════╡ 3px --ink
     │ DOSSIER ILE-2026-0043   ·   Amina B.   ·   Travail salarié — famille de parcours          │ 88 --paper-1
     ├──────────────────────────────────────────────────────────────────────────────────────────┤ 1px clause  STICKY
     │ ▮ ORIENTÉ      PHASE ▮▮▯▯▯▯▯ 2 / 7      RESPONSABLE — Équipe AGAMI / orientation          │
136  ╞══════════════════════════════════════════════════════════════════════════════════════════╡ 3px --ink
     │ PROCHAINE ACTION                                                    Échéance 14.10.2026  │ 132 --paper-2
     │ Téléversez votre attestation de formation.                                               │ 23px clause
     │ Responsable — Vous.           ┌──────────────────┐                                       │
     │                               │  Téléverser    → │       Pourquoi ? ▾                    │
     │                               └──────────────────┘                                       │
268  ├──────────────────────┬───────────────────────────────────────────┬──────────────────────┤
     │  RAIL 240            │   INSTRUMENT                              │  APPARATUS 224       │
     │                      │                                           │                      │
     │  MON DOSSIER         │ ═════════════════════════════════════════ │                      │
     │ ▌Vue d'ensemble      │ ART. 01   MON PARCOURS                    │                      │
     │  Ma checklist   ▮ 3  │                                           │                      │
     │  Mes pièces     ▮ 1  │ 01 ─┬  Compte créé              ▮ FAIT    │ 12.09.2026           │
     │  Mon parcours        │     │  ───────────────────────────────    │ Vous                 │
     │  Mes échéances   2   │ 02 ─┼  Orientation               ▮ EN COURS│ 20.09.2026          │
     │  Mes échanges  ✉ 2   │     │  ───────────────────────────────    │ Équipe AGAMI         │
     │  Historique          │ 03 ─┼╌ Formation avant le départ  ▮ À VENIR│ ⟶ MAROC             │
     │                      │     ╎  ───────────────────────────────    │ Organisme agréé      │
     │  MON COMPTE          │ 04 ─┼╌ Préparation                ▮ À VENIR│                     │
     │  Profil              │     │  ───────────────────────────────    │                      │
     │  Sécurité            │ 05 ─┼  Procédure régulière        ▮ À VENIR│ ⟶ ITALIE            │
     │  Consentements  ▮ 1  │     │                                     │ Autorité compétente  │
     │                      │ ═════════════════════════════════════════ │                      │
     │  ────────────        │ ART. 02   MA CHECKLIST                    │                      │
     │  Besoin d'aide ?     │                                           │                      │
     │  Ouvrir une demande →│ Élément            État      Responsable  Échéance      Action    │
     │                      │ ───────────────────────────────────────────────────────────────  │
     │                      │ Attestation form.  ▮MANQUANT  Vous        14.10.2026  Téléverser→│
     │                      │ Passeport          ▮VALIDE    Vous        02.03.2029  Voir      →│
     │                      │ Nulla osta         ▮SANS OBJET Autorité   —           —          │
     │                      │ ═════════════════════════════════════════ │                      │
     │                      │ ART. 03   MES ÉCHÉANCES                   │                      │
     │                      │ 14.10.2026  Attestation de formation    → │                      │
     │                      │ ─────────────────────────────────────────  │                     │
     │                      │ ART. 04   MES ÉCHANGES                    │                      │
     │                      │ 20.09.2026  Équipe AGAMI · Orientation  → │ non lu               │
     └──────────────────────┴───────────────────────────────────────────┴──────────────────────┘
     │ AGAMI APS · Ruleset v2.0.0 · Déclaration d'accessibilité · contact@agamieuromed.org      │ 48 --field
     └──────────────────────────────────────────────────────────────────────────────────────────┘
```

Zero tiles. Zero dashed boxes. Zero empty-state icons. Every region either carries data or carries one sentence naming who fills it.

---

## 18. Validation — what makes this direction survive contact with a sprint

Eleven tests. Each fails the build. They are the reason this document does not decay into the previous one within two months.

| # | assertion | kills |
|---|---|---|
| T1 | every section root declares `data-rank` and `data-sheet`; no two consecutive siblings share either | identical sections |
| T2 | exactly one `--t-instrument` element per page; `--field` ≤ 2 per page, never consecutive | flatness / navy everywhere |
| T3 | `grep box-shadow` returns only the two focus-ring declarations | elevation creep |
| T4 | `grep -E "border:\s*1px" ` matches only form controls and `dialog` | the return of the card |
| T5 | no rendered text block exceeds 70 characters per line at 1440 (10 routes) | 147-character definitions |
| T6 | every `<img>` inside `plate.html` has place + date + credit | stock photography |
| T7 | no literal `#` hex inside `static/img/` | two colour systems |
| T8 | every `--tracking-*` is 0 under `:lang(ar)`; no rule reachable under `:lang(ar)` sets a non-zero `letter-spacing` | broken Arabic ligatures |
| T9 | Arabic line-box: line N glyph bottom ≤ line N+1 glyph top, fully vocalised, every level | 12.2px overlap |
| T10 | `<main>` target-script share per route ≥ its floor; prescribed-French ceiling | a French site with an Arabic shell |
| T11 | with `java_script_enabled=False`, chrome ≤ 25% of viewport at 320/390/768/1024; no `.reveal`-style opacity gate exists | content that disappears without JS |
| T12 | every route declares an archetype; every `input[type=radio|checkbox]` ≥ 24px; every `aria-describedby` id resolves on every form in a bound-invalid state | improvised pages, broken forms |
| T13 | first 20 tab stops per archetype: focus ring ≥ 3:1 against **the surface it is drawn on** | the 1.38:1 skip link |

Plus one capture added to the standard visual matrix: **`forced-colors: active`**, at 1440, fr and ar.

---

## 19. Demolition list — delete before building

Do this first. It is faster than refactoring and it prevents the old system from leaking into the new one.

**Tokens** — the 12 unreferenced colour tokens; the entire bronze/accent family; `--radius-sm`, `--radius-md`, `--radius-pill`; `--shadow-hairline/-sm/-md/-lg`; `--font-mono` (declared, never loaded, so the "technical register" is currently Consolas on Windows and DejaVu on Linux); `--font-size-h4`, `--font-size-label`, `--font-size-button`, `--font-size-legal`, `--font-size-eyebrow`; `--container-max` as a universal.

**CSS** — `.site-header::before` and its `backdrop-filter`; `.reveal` and its 2.5s timeout and permanent `will-change`; `.counter`; every `.btn--ghost`, `.btn--upper`, `.btn--danger`; `.entrance` and its four illustration slots; `.pathway-pill`; `.empty-state__icon`; `.portal-card`; every `border-radius` and `box-shadow` on a photograph; `apps/forum/static/forum/forum.css` (fold into the system — it is the single most institution-facing page and it hard-codes `.78rem`/`.95rem`/`1.08` line-heights and a `font-weight: 700` that is not loaded); `apps/orientation/static/orientation/wizard.css` control styling.

**Templates** — `templates/portal/base_portal.html`'s `{% extends "base.html" %}`; the `page_header` block on every portal screen; the per-item mega-menu panels; `home-hero__fragment`; the four entrance illustrations; `templates/faq/_item.html`'s hand-rolled summary.

**JS** — `initCounters()`, `initReveal()`, `data-section-nav`; the `--nav-drawer-top` measurement.

**Assets** — the nine photographs that render on no page (4.83 MB), the duplicate `media/library/photos` copy (1.52 MB), `favicon.svg` (the temple), all six illustration SVGs, the two redundant copies of the variable Plex Sans shipped three times (153 KB).

**Content** — every uppercase string in the `.po` catalogues and the CMS; the second hero lead; the four boxed speaker titles with no names; the `Signaler vos besoins` / `Manifestez votre intérêt` / `Exprimer les besoins` triplicate labels for one destination; `og:title = "Italy Legal Entry™"` on every page.

---

## 20. Impersonation guard

AGAMI is a private association; Italy Legal Entry issues nothing. The design must make it impossible to imply otherwise by accident.

Forbidden without exception: the emblem of the Italian Republic, any stemma, regional or municipal coat of arms, any ministry, region, comune or chamber-of-commerce logo (partners appear only under signed written authorisation, and the partner component renders nothing without an `authorisation_ref` field); the EU emblem in any form, including a twelve-star ring, under the 2012/C 271/04 conditions — a bilateral Veneto–Morocco mobility project is precisely the context in which it would be read as endorsement; `#0066cc` and Titillium Web; the `.italia` three-band "ente di appartenenza" header lockup and the "Sito ufficiale" convention; ECL branding, its primary/secondary pair, and its Arial; SPID / CIE / pagoPA / AppIO buttons or lookalikes; "Amministrazione trasparente" section furniture; any `.gov.it` or `europa.eu` chrome cue; the words *officiel / ufficiale / official / رسمي* applied to the site anywhere in the chrome; flags, tricolours, and any red/white/green or red/green pairing in the jurisdiction system.

We borrow **structure, density, taxonomy and restraint**. We borrow nothing that identifies.

---

## 21. Risk, and what it costs

### 21.1 What could go wrong

**1 — Austerity read as unfinished.** This is the real risk. With no gradients, no shadows, no radius, no illustrations and possibly no photographs, a lazily executed page looks like an unstyled document rather than a designed one. *Mitigation:* the direction lives or dies on the **rail being visibly occupied and the rules being exactly right**. Acceptance test before any page ships: at 1440, screenshot the page, convert to greyscale, and check that the reader can identify the rank of every section from three metres away. If the page reads as one grey slab, the rank rules (§10.3) have not been applied. Additionally, the home must ship with at least one Tier A `--field` band and one jurisdiction bar from day one — those two objects carry the whole first impression.

**2 — Two navy bands per page becomes stripey on short pages.** A page with three sections and two full-bleed bands is a flag, not a document. *Mitigation:* the ceiling is two, but the **floor is one**; a page under four sections gets exactly one, and the second is spent only where there is a genuine institutional statement to make. Lint: `--field` bands ≤ ⌊sections / 3⌋.

**3 — The hatch fails in three places.** At 1px on a low-DPI screen it can moiré; in forced colours it disappears; in print it can fill in. *Mitigation:* it is **always** redundant with a text label (never load-bearing alone); the forced-colours fallback is specified (§5.8); the print stylesheet replaces it with a 4px dashed inline-start border. Test at 1×, 2×, forced-colours and print in the standard matrix.

**4 — Naskh against tight rows.** Noto Naskh Arabic's diagonal baseline and deep descenders fight the 72px register row. *Mitigation:* Arabic register rows have a 88px minimum and `--lead-clause: 1.55`; the line-box assertion (T9) catches regressions.

**5 — Newsreader at display sizes needs real kerning attention.** A high-contrast reading serif at 88px exposes bad pairs — `Vé`, `Ta`, `Ly`, and French/Italian accented capitals. *Mitigation:* the Instrument uses `opsz 72` (drawn for it), `font-feature-settings: 'kern' 1, 'liga' 1`, `text-wrap: balance`, and a manual review of the six home/hub Instrument strings in all four languages before ship. Budget half a day for it and expect two `<wbr>` insertions.

**6 — An empty rail.** If a template renders a section without an article number, the rail is 176px of nothing and the page looks broken. *Mitigation:* T1 already requires `data-rank`; add that the rail partial raises when it receives no number and no rubric.

**7 — The apparatus becomes a dumping ground.** Given a column for marginalia, writers will fill it. *Mitigation:* the apparatus holds **at most four entries** per article, each ≤ 3 lines; anything longer is a notice in the instrument track. Lint on the rendered node count.

**8 — The four-audience permanence depends on a backend change.** The design promises four audiences always; today two are gated out of both navigations. If `fallback_url_name` does not land, the design ships a promise the routing breaks. *Mitigation:* it is the first ticket in W4 and the compliance test is written before the CSS.

**9 — Losing what already works.** The repository contains six genuinely good things that a rebuild could casually destroy: the token discipline and per-token contrast annotations; the measured Latin↔Arabic ink parity; the logical-property RTL engineering with zero overflow on 50 measurements; `docs/IMAGE_LICENSES.md`; the object-level permission model in `apps/portal/services.py`; and the `core.public_routes` registry. *Mitigation:* all six are explicitly carried forward in this document, and the registry becomes the place the archetype assignment hangs.

### 21.2 What it costs

Developer-days, excluding design time and content work. Sequenced so each workstream unblocks the next.

| # | workstream | days | blocks |
|---|---|---|---|
| W0 | **Archetype layer** — 14 archetypes, one base template each, every route assigned, the declaring test | 4–5 | everything |
| W1 | Fonts + tokens + type scale + measure/leading; delete the dead tokens | 4–6 | W2, W3 |
| W2 | Grid: three tracks, sheet ladder, rail, apparatus, breakpoints, the six grid rules + lint | 8–10 | W3–W6 |
| W3 | Component rewrite — 29 numbered sections reduced to ~18; registers, notices, tables, buttons, form controls | 12–15 | W6 |
| W4 | Navigation — permanent four audiences + `fallback_url_name`, Sommaire sheet, rail nav, index bar, footer as site map, breadcrumb from the menu tree | 5–6 | |
| W5 | Graphic language — mark + lockups + favicon, hatch, jurisdiction bar, register, timeline, the outcome act + print stylesheet | 6–8 | |
| W6 | Platform — `shell_platform.html`, case header, next-action band, role-resolved navigation, tables, wizard fixes | 10–12 | |
| W7 | Arabic build — two faces, `:lang(ar)` tokens, `.prescribed` component, the isolation tag, the three CI gates | 6–8 | |
| W8 | Accessibility — focus-ring pair, forced-colours layer, no-JS chrome, drawer as `<dialog>`, live-region cleanup, target sizes, the 13 tests | 5–6 | |
| W9 | Imagery — ingest grade, manifest `object-position`, mandatory-caption template, delete unused assets | 3–4 | |
| | **Total** | **63–80 days** | |

**What can ship in stages.** W0+W1+W2 (16–21 days) already produces a page that is unrecognisable from today's: three tracks, a real type scale, the sheet ladder and no cards. W4 and W8 are independent and can run in parallel with W3. W5 is the highest visual return per day and should not be deferred to last — without the mark, the hatch and the jurisdiction bar, the intermediate build is austere without yet being distinctive, which is the worst place to show a client. W6 and W7 can follow the public launch; W9 depends on a commission that has its own lead time, and until that reportage exists **the site ships with zero photographs**, which this direction is designed to survive.

### 21.3 The one-sentence bet

This direction bets that a Region, a Chamber of Commerce and a consulate will find a page that looks like a well-set legal instrument more credible than a page that looks like a well-built website — and that the cost of being wrong is low, because everything here is rules, type and alignment, which are the cheapest things in a stylesheet to change and the hardest things in a design to fake.