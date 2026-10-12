# ICON SEMANTIC MAP — final (V5)

**Italy Legal Entry™ · Executive Creative Director · 27 September 2026 · status PROPOSED — revised after the red team** (`RED_TEAM.md` B1, M2, m1, m2; the changes are marked **[RT]**). Built on `council/ICON_SEMANTIC_MAP.md` (registry draft `council/icons/icon_map_v5.json`, specimen `council/icons/specimen.html` + `specimen-render.png`) with the ECD amendments marked **[ECD]**. Nothing in the repository was modified.

---

## 0. The rules in eight lines

1. **One concept → one glyph; one glyph → one concept.** Enforced by a Python registry (`apps/core/icons.py`) that every map imports from, and by tests. Today 19 of 32 live symbols carry two or more unrelated concepts; `arrow` is 80 of 163 calls.
2. **One base, one hand.** The ILE sprite is the product; **Lucide (ISC)** is the single donor of geometry for missing glyphs; Phosphor is a thesaurus only; two libraries never mix.
3. **The ILE treatment**, whatever the donor: 24 grid, 20 × 20 live area; **1.5 px effective stroke at every size** (stroke-width 2.57 / 2.25 / 1.8 / 1.5 / 1.25 / 1.0 at 14 / 16 / 20 / 24 / 32 / 48 px); **square caps, miter joins**; `currentColor` only; dots drawn as `r = 1` circles, never zero-length paths.
4. **Three tiers.** *Identity* (drawn from the mark; never toned, never mirrored): `ile-arch`, `ile-key`, `ile-steps`, `ile-mark`. *Concept* (audiences, actors, domains, phases): may carry the **12 % tone** (a sub-path `fill="currentColor" fill-opacity=".12" stroke="none"`); reach templates only through the registry. *Utility* (actions, direction, feedback): monoline, never toned; may be typed literally in templates.
5. **Statuses are one family — «i cerchi»** [ECD]: outline = open, filled = settled; the chip mark is always the *register's* mark; the word carries the precise meaning.
6. **The word carries the meaning; the glyph makes it recognisable.** Every glyph sits beside its word or gives its name to assistive technology. Never a glyph per card or per row unless it says something (a status mark, an actor). No enumeration bullets as icons. The DS 2026 ceiling of six icons per page applies to the editorial body of public pages; the chrome is exempt.
7. **Direction mirrors, meaning does not.** A closed RTL flip list (§7).
8. **Nothing from the forbidden image vocabulary** becomes a glyph: no passport, luggage, plane, airport, queue, gate, barrier, border, flag.

---

## 1. Identity tier — the mark's own grammar

| Symbol | Drawing (24 grid, 1.5 stroke, square caps) | Used for | Never |
|---|---|---|---|
| `ile-arch` | jambs at x 6 and 18 from y 19 to 10.5, a semicircle r 6 (apex y 4.5), threshold line x 3–21 at y 19; 12 % tone inside the opening | **threshold B** (the arrival) — the only arch in the journey **[RT]**; the favicon; the rail tile in forced colours; the login at small sizes | a journey step (step 6 takes `building-2`) **[RT]**; a navigation glyph; a card decoration; a panel head |
| `ile-key` | ring r 3 at (12, 6.5), shank x 12 from 9.5 to 20.5, two teeth at y 15 (3.5 long) and 18.5 (2.5 long) — vertical, as it hangs in the door | **Espace réservé / access / se connecter** (utility bar, drawer, account menu, reserved band, login button) | security settings (that is `fingerprint`); a reference number (`hash`) |
| `ile-steps` | **[RT]** a stair profile — one polyline of three treads and three risers, from (3, 19) up to (21, 7): treads 6 units, risers 4 — the mark's steps seen from the side; the council's three stacked lines were a near-twin of `menu` and `list-filter` at 14–16 px | **Mon parcours**, the JourneyRail heading, the passage, the section-header micro-mark (14 px — the smallest icon size — in ink) | a list or a menu |
| `ile-mark` | the whole mark mono (arch + key + steps), minimum 20 px | **Équipe du projet** as an actor / message sender avatar | a 14 px chip glyph; navigation |
| ~~`ile-crossing`~~ | withdrawn **[ECD]** | — | the journey has two thresholds (`stamp`, `ile-arch`): a «crossing» at the jurisdiction switch would say «you crossed» when the visa procedure starts |

---

## 2. Statuses — «i cerchi» [ECD]

Replaces the council's pictographic picks (`glasses`, `hourglass`, `ban`, `arrow-down-to-line`, `circle-dot`, `slash`, `circle-dashed`) and `core.chips.GLYPH` (never rendered today). Drawn as ILE glyphs on a 16 px circle (14 px inside a 24 px chip, 16 px as ledger pips — **[RT]** raised from 12 px, M11); painted by the chip's `--chip-mark`, never by a template.

| Symbol | Drawing | Register | Shown for |
|---|---|---|---|
| `st-attesa` | dashed ring (the language of `glyph--none`) | attesa | MANQUANT · pending / en attente · draft · missing_requirement · assessment warning |
| `st-attesa-replace` | ring + two arrows (kin of the `refresh-cw` action — P4: distinguishable at 20 px) | attesa | À REMPLACER |
| `st-neutro` | ring + centre dot | neutro | DÉPOSÉ · filed · scan clean · transmitted · oriented … post_entry (case stages) · closed |
| `st-esame` | half-filled disc | esame | EN EXAMEN · in_review / under_review · assigned · in_progress · scan pending · verification pending |
| `st-conforme` | **[RT]** filled disc, **no glyph** — painted in ink by the chip (`conforme` has no chroma); the council's knocked-out check is withdrawn (B1), and the red team's horizontal bar is not used (it reads as «minus» / «no entry») | conforme | VALIDE · done / completed / accepted / fourni |
| `st-azione` | filled disc + clock hands | azione | EXPIRÉ · review_required · suspended · scan error · needs clarification · response available |
| `st-rifiuto` | filled disc + × | rifiuto | NON VALIDE · rejected · infected |
| `lock` (ILE, kept) | the existing padlock | blocco | BLOQUÉ (`ChecklistStatus.blocked`, `EvidenceStatus.blocked`) · assessment stop |
| `st-nullo` | slashed dotted ring | nullo | withdrawn · not applicable / sans objet · archived · not_required · scan not_configured |
| `badge-check` (Lucide) in the **seal** | navy disc, gold glyph | seal | acts of an authority only (verification approved by an authority); never the project's own «Vérifiée» |

Rules: **[RT] the check rule** — `check` and `circle-check` mark only the person's own interface acts (a ticked box, a chosen OptionCard, a selected filter chip, a field the server confirmed, an account confirmation such as «E-mail confirmé»), never a piece, a journey step, a case, an assessment or any state the platform produces; every chip carries its mark, neutro included (overrides `badges.md` §4.3); the doc-row Conditions gate (`action_blocked`) is a sentence + link, not a chip; `documents.requirements.STATE_GLYPHS` (state → mark) and the producers of `chips.py` import from the registry; marks draw themselves once (`pathLength`, 240 ms) when a state changes asynchronously; reduced motion: the new mark at once.

---

## 3. The map — one concept, one glyph

Columns: **Symbol** (`icon-` prefix omitted) · **Geometry** (`ILE` kept · `ILE-new` · `Lucide <name>` donor under ILE rules) · **Tier** I / C / U · **Tone** · **RTL** flip · **Replaces**.

### 3.1 Audiences and actors

| Concept | Symbol | Geometry | Tier | Tone | RTL | Replaces / note |
|---|---|---|---|---|---|---|
| **Persona** (audience) = the person actor = «vous» | `person` | ILE | C | yes | no | family reunification leaves → `users` |
| **Impresa** (audience) = company actor = «Mon entreprise» | `building` | ILE | C | yes | no | self-employment → `store`; public services → `building-2` |
| **Istituzione** (audience) | `institution` | ILE | C | yes | no | project team → `ile-mark`; SSN → `hospital` |
| **Università – Formazione** (audience) = training-body actor | `university` | ILE | C | yes | no | Academy → `book-open`; study pathway → `backpack`; school → `school` |
| Professional (actor, «Professionnels», «assigned») | `briefcase` | ILE | C | yes | no | cases → `folder`; needs → `wrench`; salaried work → `factory`; taxation → `receipt` |
| Competent authority (actor) = **threshold A** of the journey [ECD] | `stamp` | Lucide `stamp` | C | yes | no | replaces `shield`; the authority's act is a stamp |
| Authorised actor (actor and phase) | `badge-check` | Lucide | C | yes | no | replaces `handshake`; also the seal's glyph (the same act of accreditation) |
| Équipe du projet (actor, message sender) | `ile-mark` | ILE-new | I | no | no | replaces `institution` / `user` |
| My account (summary, Profil) | `circle-user-round` | Lucide | C | no | no | replaces `user` (retired: byte-identical duplicate of `person`) |
| No actor / unknown | dashed disc (`glyph--none`) | ILE | — | — | — | kept |

### 3.2 Platform domains and navigation (rail, bottom bar, account menu, context bar)

| Concept | Symbol | Geometry | Tier | Tone | RTL | Replaces |
|---|---|---|---|---|---|---|
| Tableau de bord (person, company) | `layout-dashboard` | Lucide | C | yes | no | `home` |
| **Ma situation** = orientation CTA = pre-orientation phase | `compass` | ILE | C | yes | no | keeps |
| **Mon parcours** = JourneyRail heading | `ile-steps` | ILE-new | I | no | no | `map-pin` |
| Voies régulières (public catalogue) | `signpost` | Lucide | C | yes | **yes** | `map-pin` eyebrow |
| **Mes dossiers / Fascicolo** | `folder` | Lucide (toned body) | C | yes | no | `briefcase` |
| **Mes pièces / Documents** (the domain, a piece) | `document` | ILE | C | yes | no | keeps |
| Mes demandes (requests sent to the Guichet) | `send` | Lucide | C | no | **yes** | `list` |
| Mes échéances (deadlines domain) | `calendar-clock` | Lucide | C | yes | no | `calendar` (stays «a date») |
| **Communications / Messages** | `mail` | ILE | C | yes | no | keeps; e-mail *addresses* → `at-sign` |
| **Guichet numérique** | `concierge-bell` | Lucide | C | yes | no | `handshake`; **[ECD]** confirmed after a 20 px side-by-side with `bell`; fallback `messages-square` |
| Demandes qui me sont confiées (professional queue) | `inbox` | Lucide | C | yes | no | `list` |
| **Academy** = training phase = «formation dans le pays d'origine» | `book-open` | Lucide (toned pages) | C | yes | no | `university`, `handshake` |
| Selection processes (authorised actor) | `list-checks` | Lucide | C | yes | no | `check` |
| Mes besoins (company needs) | `wrench` | Lucide | C | yes | no | `briefcase` |
| Analyse territoriale | `map` | Lucide | C | yes | no | `map-pin` |
| Mon organisation | the account type's audience glyph | — | C | yes | no | data-driven |
| **Forum Vénétie–Maroc** (cooperation, governance) | `handshake` | ILE | C | yes | no | keeps only this |
| Forum — edition | `calendar-range` | Lucide | C | no | no | new |
| Forum — milestone | `milestone` | Lucide | C | no | **yes** | new |
| Forum — working table | `table` | Lucide | C | no | no | new |
| Forum — proposal | `file-plus` | Lucide | C | no | no | new |
| Forum — commission, project | *(word only)* | — | — | — | — | twins would fail P4 |
| Vivre en Italie = post-entry phase | `sprout` | Lucide | C | yes | no | new |
| Administration / back-office | `settings` | ILE | C | no | no | new use of an unused symbol |
| Notifications (context bar) | `bell` | Lucide | U | no | no | new |
| Site public (from the console) | *(text link)* | — | — | — | — | — |
| **Espace réservé / se connecter** | `ile-key` | ILE-new | I | no | no | `lock` ×4 |
| Sécurité du compte | `fingerprint` | Lucide | C | no | no | `key` |
| Se déconnecter | `logout` | ILE | U | no | **yes** | keeps |
| Langue | `languages` | Lucide | U | no | no | optional (the control is text) |
| Rail collapse / expand | `panel-left-close` | Lucide | U | no | **yes** | `chevron-end` |
| Menu (hamburger) | `menu` | ILE | U | no | no | keeps; row menus leave |
| Row / piece actions | `ellipsis-vertical` | Lucide | U | no | no | `menu` |
| Rechercher / Aller à… | `search` | ILE | U | no | no | keeps; research pathway leaves |

### 3.3 The journey — seven steps, two thresholds [ECD]

| Journey step (`JOURNEY_STEPS`) | Phase | Symbol | Geometry | RTL |
|---|---|---|---|---|
| 1 «Votre situation et votre objectif» | pre-orientation | `compass` | ILE | no |
| 2 «Pré-évaluation et parcours possibles» **[RT]** | pre-orientation — the possible pathways | `signpost` (SHARED with «Voies régulières»: the same concept) | Lucide | **yes** |
| 3 «Préparation et formation avant le départ» | training | `book-open` | Lucide | no |
| — **threshold A** «les autorités compétentes» (between 3 and 4) | jurisdiction changes; the person has not moved | `stamp` | Lucide | no |
| 4 «Procédures auprès des autorités compétentes» | procedure | `scroll-text` | Lucide | no |
| 5 «Préparation du départ» **[RT]** | pre-departure | `clipboard-list` (no check anywhere on the journey) | Lucide | no (never luggage or a plane) |
| — **threshold B** «l'arrivée» (before 6) | the brand's own moment — the only arch in the journey | `ile-arch` | ILE-new | no |
| 6 «Arrivée et premières démarches» **[RT]** | entry — the first formalities, with public services | `building-2` (SHARED with «Services publics») | Lucide | no |
| 7 «Accompagnement et inclusion» | post-entry | `sprout` | Lucide | no |
| (documentation, across steps 2–4) | the pieces | `document` | ILE | no |
| (authorised actor, selection) | the actor | `badge-check` | Lucide | no |

Where they appear: the public passage (stations and thresholds, 20 px), the dashboard and case rails (16 px beside the label; the nodes stay dots — done nodes are filled ink dots, never a check **[RT]**), «Prochaine étape» / NowPanel eyebrows, timeline events, the questionnaire's stepper header. Case **states** (suspended, closed, review required) are chips with their register mark, not phase glyphs.

### 3.4 Responsibility — who acts

| Actor | Symbol |
|---|---|
| the person / «vous» | `person` |
| the company | `building` |
| the competent authority | `stamp` |
| the appointed professional | `briefcase` |
| the training body | `university` |
| the authorised actor | `badge-check` |
| the project team | `ile-mark` |
| unknown / none | dashed disc |

`cases.ResponsibleActor` and `documents.requirements.ACTOR_GLYPHS` become one table in the registry.

### 3.5 Selection and pathways

| Concept | Symbol | Geometry |
|---|---|---|
| Selection process (domain) | `list-checks` | Lucide |
| Selection stages (mandate confirmed, competence review, evidence check, company review, closed, suspended) | the **register mark** of the stage's state (§2) + the word | — |
| Identity disclosure (the person's consent) | `pen-line` | Lucide |
| Pathway — lavoro subordinato | `factory` | Lucide |
| Pathway — Carta blu UE | `id-card` | Lucide |
| Pathway — formazione nel paese d'origine | `book-open` | = training |
| Pathway — studio e formazione in Italia | `backpack` | Lucide |
| Pathway — ricongiungimento familiare | `users` | Lucide |
| Pathway — lavoro autonomo / imprenditoria | `store` | Lucide |
| Pathway — ricerca scientifica | `flask-conical` | Lucide |
| Pathway — altre vie regolari | `route` | Lucide (RTL: no — a route glyph has no reading direction here) |

Pathway glyphs appear once per page (the detail eyebrow, the «Mon parcours» result, the pathway register rows) — never in a numbered editorial list.

### 3.6 Living in Italy, contact, public specifics

| Concept | Symbol | Geometry |
|---|---|---|
| Langue italienne | `languages` | Lucide |
| Logement | `house` | ILE (`home` renamed: housing only) |
| Santé | `heart-pulse` | Lucide |
| Service sanitaire national (SSN) | `hospital` | Lucide |
| École | `school` | Lucide |
| Éducation civique | `vote` | Lucide |
| Droits et devoirs | `scale` | Lucide |
| Sécurité au travail | `hard-hat` | Lucide |
| Fiscalité de base | `receipt` | Lucide |
| Services publics | `building-2` | Lucide (checked against `building` at 20 px) |
| E-mail address | `at-sign` | Lucide |
| Phone | `phone` | ILE |
| Address / place | `map-pin` | ILE |
| Anti-fraud (link, footer entry) — the component itself is «il gradino» (the mark's steps drawing, not an icon) | `shield-alert` | Lucide |
| Institutional notice | `megaphone` | Lucide |
| Glossary | `book-a` | Lucide |
| FAQ | `circle-help` | Lucide |
| News | `newspaper` | Lucide |
| Reference number | `hash` | Lucide |
| Rules version / versions / history | `history` | Lucide |
| Quote / testimony | `quote` | ILE |

### 3.7 Actions and feedback (utility tier — monoline, never toned)

| Action | Symbol | Geometry | RTL |
|---|---|---|---|
| Déposer / upload (the dropzone, the file field) | `upload` | Lucide | no |
| Remplacer | `refresh-cw` | Lucide | no |
| Télécharger | `download` | ILE | no |
| Consulter / aperçu / show password | `eye` (hide: `eye-off`) | Lucide | no |
| Supprimer | `trash-2` | Lucide | no |
| Ajouter / Retirer | `plus` / `minus` | ILE | no |
| Modifier / Copier | `pencil` / `copy` | Lucide | no |
| Marquer comme lu | `mail-open` | Lucide | no |
| Filtrer / Trier / Imprimer | `list-filter` / `arrow-down-up` / `printer` | Lucide | no |
| Next / continue / forward CTA (primary and whole-row targets only) | `arrow` | ILE | **yes** |
| Previous / back | `arrow-start` | ILE-new | **yes** |
| External link (authority sites) | `arrow-up-right` | ILE | no (DS rule) |
| Disclosure (select, account menu, accordion, mega-menu) — rotates 180° | `chevron` | ILE | no |
| Forward disclosure, breadcrumb separator | `chevron-end` | ILE | **yes** |
| Fermer | `close` | ILE | no |
| Selected (option card) | `check` | ILE | no |
| Notices: info · warning · error · pending · unavailable (V5 has no «success» notice) | `info` · `warning` · `circle-alert` · `clock` · `circle-pause` | ILE / Lucide | no |
| Due dates: upcoming · soon · overdue | `calendar` · `clock` · `alarm-clock` | ILE / ILE / Lucide | no |
| allauth alert | per level (`info` / `circle-check` / `warning` / `circle-alert`) — `circle-check` only for the person's own account acts (signed in, e-mail confirmed, password changed) **[RT]** | — | fixes the «always info» defect |
| Empty **region** | *(no icon)* | — | — |
| Empty **page** [ECD] | the domain's concept glyph in a 40 px toned disc | — | one glyph that says which space is empty |

---

## 4. Retired symbols and the count

**Retired:** `user` (duplicate of `person`), `shield`, `globe`, `key` (generic), `list`; `home` renamed `house`; **[ECD]** `ile-crossing`, and the council's status pictograms (`glasses`, `hourglass`, `ban`, `arrow-down-to-line`, `circle-dot`, `slash`, `circle-dashed`), replaced by «i cerchi»; `archive` (states are register marks). The four landform route glyphs (`_route_glyph.html`) leave the product (DS V4 §9).

**Count [ECD, recomputed].** ILE drawings kept: **31** (36 − 5 retired; the council's «27» did not add up) · identity glyphs new: **4** · status marks new: **8** (+ `lock` reused) · `arrow-start`: **1** · Lucide donor geometries: **≈ 65** (§3) → **≈ 109 symbols**, estimated **≈ 30–34 KB raw / ≈ 9 KB gzip** (donor paths average 200–300 B). One cached request; fixed boxes (no CLS); no icon is an LCP candidate. The council's test ceiling (≤ 32 KB raw) may need 36 KB — measure the built sprite and set the ceiling from the measurement. In the console the ≈ 12 shell symbols are also rendered in the document so the rail paints with its glyphs.

---

## 5. Where every current site goes (summary; full list in `council/ICON_SEMANTIC_MAP.md` §7)

| Today | V5 |
|---|---|
| `portal.services.NAV_GLYPHS` (13 keys) | `layout-dashboard` · `compass` · `ile-steps` · `folder` · `send` · `document` · `calendar-clock` · `mail` · `concierge-bell` · `book-open` · `list-checks` · `building` · `inbox`; the `chevron-end` fallback becomes a registry error |
| `companies.services.navigation` | `layout-dashboard` · `wrench` · `building` · `map` · `mail` |
| `documents.requirements.ACTOR_GLYPHS` | `person` · `building` · `stamp` · `briefcase` · `university` · `badge-check` · `ile-mark` |
| `core.chips.GLYPH` (never rendered) | deleted; `STATE_GLYPHS` → «i cerchi», rendered in `.chip__g` |
| `lock` / `home` on reserved access (utility bar, header, home reserved band, access point, account menu) | `ile-key` |
| account menu `user` / `key` | `circle-user-round` / `fingerprint` |
| doc-row: `warning` overdue · `menu` more · `document` «Consulter» · `list` versions | `alarm-clock` · `ellipsis-vertical` · `eye` (the whole row is the target) · `history` |
| notices, form errors, form unavailable, allauth alert | per kind (§3.7) |
| accordion `plus` | `chevron` (rotates 180°) |
| pagination `arrow` ×2 | `arrow-start` / `arrow` |
| mega-menu `chevron-end` bullets · ecosystem enumeration bullets · pathway document bullets | none (typography) |
| e-mail addresses (`mail`) | `at-sign` |
| anti-fraud `shield` ×4 | «il gradino» component; `shield-alert` for the footer / link entry |
| `link-arrow` / `entry__arrow` secondary links (≈ 45 sites) | typography only; the arrow stays on primary CTAs and whole-row targets (80 → ≈ 30 calls) |
| favicon (three bars) | `ile-arch` on navy |

---

## 6. Engineering contract

- **Registry** `apps/core/icons.py`: `TIER_IDENTITY`, `UTILITY`, `CONCEPT` (concept key → symbol), `STATUS` (register → mark), `FLIP_RTL`, `SHARED` (the reviewed exception register: the same concept seen from two producers, e.g. `person` audience/actor/you, `book-open` academy/phase/pathway, `stamp` actor/threshold A, `badge-check` actor/seal, **[RT]** `signpost` voies régulières/journey step 2, `building-2` services publics/journey step 6; `ile-arch` is no longer shared: threshold B only). Every existing map (`NAV_GLYPHS`, `ACTOR_GLYPHS`, `DEFAULT_ICONS`, `INITIAL_TOPICS`, `ENTRANCES`, `NETWORK_ACTORS`, the portal cards, `STATE_GLYPHS`) imports from it.
- **Sprite build** `static/icons/src/*.svg` → `static/img/icons.svg` by `scripts/build_icons.py` (stdlib): strict XML, `viewBox 0 0 24 24`, no hex, no `<style`, no `style=`, no `--` inside comments; donor paths copied **without** their root attributes (which carry the 2 px round look); the tone path added where the map says so; the DS 2026 §13 icon list regenerated between markers; «build is current» test like the CSS bundle's; the import fails loudly on a Lucide name that does not exist (several names were not verified against the live catalogue: `concierge-bell`, `book-a`, `panel-left-close`, `circle-user-round`).
- **CSS** (`components.css` §2 → `v5/icons.css`): `.icon { fill: none; stroke: currentcolor; stroke-width: var(--icon-stroke-md); stroke-linecap: square; stroke-linejoin: miter; }` with one stroke-width per size class; `.chip__g` keeps its compensation with square caps; forced colours: strokes follow `CanvasText`, the 12 % tone stays faint (visual check needed).
- **Accessibility:** decorative beside text (`aria-hidden`); icon-only controls keep visually hidden text; `role="img"` + label only where a glyph is the sole carrier (none planned); never colour alone.

## 7. RTL — the closed flip list

Mirrored with `.icon--flip-rtl`: `arrow`, `arrow-start`, `chevron-end`, `logout`, `send`, `signpost`, `milestone`, `panel-left-close`. **Never mirrored:** everything else, including `arrow-up-right`, `history`, `refresh-cw`, `ile-key`, `ile-arch`, `ile-mark`, every status mark and every audience glyph.

## 8. Tests (`tests/frontend/test_icons.py`)

1. registry values == sprite ids (no orphan, no phantom); 2. no symbol under two concept keys unless listed in `SHARED` with its reason; 3. every template literal `svg_icon "…"` ∈ `UTILITY`; 4. `FLIP_RTL` symbols rendered only with `icon--flip-rtl`, and no other; 5. sprite strict XML, `viewBox`, no hex / `<style` / `style=`, size ceiling from the measured build; 6. `STATE_GLYPHS.keys() == set(RequirementState) | {"blocked"}` and every chip producer member maps to a register mark; `ACTOR_GLYPHS.keys() == set(ResponsibleActor)`; 7. build is current; 8. no `[data-register]` chip without its mark; **[RT]** 9. `STATUS["conforme"]` is not a check glyph, and no `check` / `circle-check` / `clipboard-check` symbol is rendered inside a chip, a journey node or station, or the ledger; 10. `ile-arch` is rendered only in the arch allow-list (CD §1.4 law 5).

## 9. Open questions for the owner

- **Q1** The DS 2026 ceiling («six icons per page», «never an icon per row») vs the V4 console (an icon rail; a glyph disc on every document row): V5 applies the ceiling to the editorial body of public pages; the chrome is exempt; rows carry a glyph only when it says something (a status mark, an actor) — the identity `document` disc on every row goes unless a document *kind* exists (Q4).
- **Q3** `concierge-bell` for the Guichet next to the notification `bell` — confirm after the side-by-side.
- **Q4** A document *kind* on requirements (identity, attestation, contract, photo, form) would make a per-row glyph meaningful (`file-text`, `file-image`, `pen-line`…); without it, one neutral `document`.
- **Q5** Accept ISC donor geometry in the ILE sprite (with `ICON_LICENSES.md`), or commission ≈ 65 originals (≈ 3 designer-days, same rules).
- **Q6** Retire the four landform route glyphs from the home (DS V4 §9) — confirmed by V5.
