# ICON SEMANTIC MAP — Italy Legal Entry™ V5

> **Erratum — ECD red-team revision, 27 Sept 2026 (`final/RED_TEAM.md` M18).** On 26 Sept, 16:24–16:25, a Playwright MCP session wrote a `.playwright-mcp/` folder *inside the repository* (reported in `CAPTURES_AND_REFERENCES.md`); it held `ile-v5-icon-specimen.png`, which points to this lane's specimen run. The folder is gone, and the repository's tracked files are clean at `c9a58d8`; the «no file in the repository was touched» of limitation L1 should be read with that caveat. The process fix is O66.

Iconography Specialist · council V5 «premium escalation» · 26 September 2026 · read-only phase
(nothing under `C:/tmp/italylegalentry` was modified; every path below is a proposal).

Companion files, same folder:
`icons/icon_map_v5.json` (the registry, machine-readable) ·
`icons/ile-icons-v5-draft.svg` + `icons/specimen.html` (20 draft symbols on the V5 rules, rendered
at 14/16/20/24/48 px, square vs round terminals, paper vs navy — a specimen, not the sprite) ·
`icons/specimen-render.png` (the specimen as Chromium drew it, §6.1).

---

## 0. Verdict in six lines

1. The current sprite is **original, well-built and too small**: 36 symbols carry ~55 concepts.
   19 of the 32 live symbols stand for two or more unrelated things (§2). The cause is structural:
   four independent Python maps and 163 template calls pick from one sprite with **no registry**.
2. `person` and `user` are **byte-identical** symbols under two ids; `arrow` is **80 of 163 calls**
   (49 %): every CTA, link, pagination and entry carries the same glyph, which is the strongest
   «default look» signal on the site.
3. **Small sizes are under-weight**: `.icon` keeps `stroke-width: 1.5` in user units at every size,
   so a 16 px icon renders a **1.0 px** line and a 14 px glyph-disc icon a **0.875 px** line —
   below the 1.5 px the design system asks for (only `.chip__g` compensates, with 2.6). This alone
   makes the console glyphs read thin and «library-ish».
4. **One base**: keep the ILE sprite as *the product*, and adopt **Lucide (ISC)** as the single
   *donor geometry* for the glyphs the vocabulary lacks — same 24 grid, stroke-based, so the whole
   set takes the ILE treatment from one CSS rule: **1.5 px effective at every size, square caps,
   miter joins, 12 % tone on the concept tier**. Phosphor (MIT) is the semantic thesaurus the
   task provides — used as such — but it is a *filled* set on a 256 grid and cannot enter a stroke
   sprite without the «mixed sets» the design rules forbid (§4).
5. **Five bespoke glyphs stay ILE's own** and become the identity tier: the arch, the key, the three
   steps, the crossing, the mark (§6). They are the mark's own grammar at 24 px, never a library icon.
6. The map below gives **one glyph per concept** for ~150 concepts (§5), the fix for every
   collision (§7), the CSS/sprite/test contract (§8) and a migration in three phases (§9).

---

## 1. Inventory — what exists

| Item | Value | Source |
|---|---|---|
| Sprite | `static/img/icons.svg`, 36 `<symbol>`, 6.3 KB, `viewBox 0 0 24 24`, stroke inherited (`fill:none; stroke:currentcolor; stroke-width:1.5; round caps/joins` in `static/css/components.css:188`) | read |
| Tag | `{% svg_icon "name" "classes" "label" %}` → `<svg class><use href="/static/img/icons.svg#icon-name">` (`apps/core/templatetags/ile_core.py:86`); decorative by default, `role="img"+aria-label` when a label is given | read |
| Calls | **163** `svg_icon` calls in templates (+ `icon=`/`glyph=` include params) | grep |
| Python maps that choose an icon | `portal.services.NAV_GLYPHS` (rail, 13 keys) · `companies.services.navigation` (5) · `documents.requirements.ACTOR_GLYPHS` (7) · `pathways.services.DEFAULT_ICONS` (8) · `living.catalogue.INITIAL_TOPICS` (10) · `pages.content.ENTRANCES` (4) + `NETWORK_ACTORS` (5) · `portal.services` cards (6) · `core.chips.GLYPH` (5, **never rendered**) | read |
| Live / unused | 32 live; 4 unused: `phone`, `settings`, `quote`, `minus` | inventory §7 |
| Duplicates | `icon-person` ≡ `icon-user` (identical paths) | sprite |
| Inline SVG outside the sprite | the doorway (`components/doorway.html`, hero + login), the four route «landforms» (`pages/home/partials/_route_glyph.html`), the voyage route (`_pilot.html`) — all bespoke, all decorative | grep |
| Sizes in use | `--icon-xs 14 · sm 16 · md 20 · lg 24 · xl 32 · hero 48`; glyph discs 24/32/40 (`v4/tokens.css:206-215`) | read |
| Tests that constrain | every template literal must exist in the sprite (`test_static_assets.py:199`); sprite well-formed XML and every symbol `0 0 24 24` (`test_design_docs.py:980`); no `--` inside an XML comment (gap G-01) | read |
| Design rules | DS 2026 §13: one original set, 24 grid, no fill, **square terminals asked and never executed**, «max six icons per page», never an icon per row/card; V4 CD §3.9: icon rail, glyph discs for actors, chips with glyph + register; DS V4 §5 icon tokens; brand: arch + key + steps are the identity (`BRAND_ASSETS.md`) | read |

Call distribution (templates): `arrow` 80 · `info` 10 · `warning` 7 · `calendar` 7 · `mail` 6 · `shield` 5 ·
`clock` 5 · `menu` 4 · `lock` 4 · `close` 4 · `check` 4 · `user` 3 · `list` 3 · `document` 3 ·
`compass` 3 · `key` 2 · `home` 2 · `chevron-end` 2 · `chevron` 2 · one each `search`, `plus`,
`logout`, `download`, `arrow-up-right`.

---

## 2. Collisions — the same glyph for different concepts (today)

Condensed from the UI inventory (`UI_INVENTORY.md` §7 has every site). «Owner» = the concept that
keeps the glyph in V5; the others move (§7 gives each move).

| Symbol | Concepts it carries today | Owner in V5 | Movers |
|---|---|---|---|
| `person` | person actor · «Personnes» audience · «vous» · pathway *family reunification* | the person (audience = actor = you) | family → `users` |
| `user` | my account · «L'équipe du projet» sender | — (symbol retired: duplicate of `person`) | account → `circle-user-round`; project team → `ile-mark` |
| `building` | companies audience · company actor · «Mon entreprise» · company card · pathway *self-employment* · living «Services publics» | the company | self-employment → `store`; public services → `building-2` |
| `institution` | institutions audience · actor *project_team* · enumeration bullets · living «SSN» | the institution (audience) | project team → `ile-mark`; SSN → `hospital`; bullets → none |
| `university` | universities audience · actor *training_body* · rail «Academy» · pathway *study in Italy* · living «École» · bullets | university & training bodies (audience = actor) | Academy → `book-open`; study pathway → `backpack`; école → `school` |
| `briefcase` | actor *professional* · «Professionnels» · rail «Mes dossiers» · company «Mes besoins» · pathway *salaried work* · living «Fiscalité» | the professional | cases → `folder`; needs → `wrench`; salaried → `factory`; taxation → `receipt` |
| `check` | option selected · notice success · «marquer comme lue» · rail «Processus assignés» · bullets | the affirmation mark (VALIDE, selected, done) | success notice → `circle-check`; read → `mail-open`; selection → `list-checks`; bullets → none |
| `shield` | anti-fraud ×4 · actor *authority* · «guarantee» notice · living «Sécurité au travail» | — (symbol retired) | anti-fraud → `shield-alert`; authority → `stamp`; institutional notice → `megaphone`; work safety → `hard-hat` |
| `document` | rail «Mes documents» · doc-row disc · «Consulter» · news empty state · pathway bullets · «Version des règles» · living «Droits et devoirs» | the document / piece | consulter → `eye`; news → `newspaper`; rules version → `history`; rights & duties → `scale`; bullets → none |
| `globe` | pathway *EU Blue Card* · living «Langue italienne» | — (retired) | blue card → `id-card`; language → `languages` |
| `menu` | hamburger ×3 · **document row «more» menu** | navigation menu | row actions → `ellipsis-vertical` |
| `chevron-end` | sub-link bullet · rail collapse · rail fallback | forward disclosure | collapse → `panel-left-close`; bullets → none; fallback → registry error, not a glyph |
| `plus` | accordion expand · living «Santé» | add | expand → `chevron` (rotates); santé → `heart-pulse` |
| `search` | search field · pathway *scientific research* | the search control | research → `flask-conical` |
| `mail` | contact e-mail addresses · «Communications» · messages card/empty state | the message centre | e-mail address → `at-sign` |
| `key` | «Sécurité du compte» · «Référence» meta | — (retired: competes with the brand key) | security → `fingerprint`; reference → `hash` |
| `info` | info notice · **allauth alert at every level** · orientation note · «État» meta · FAQ link | the information notice | allauth → per level; état → status glyph; FAQ → `circle-help` |
| `map-pin` | rail «Mon parcours» · pathway *other routes* · pathway eyebrow default · «Analyse territoriale» | a place (address) | parcours → `ile-steps`; other routes → `route`; analysis → `map`; eyebrow → the pathway's own glyph |
| `home` | «Espace réservé» · rail «Tableau de bord» · company dashboard · living «Logement» | housing (`house`) | dashboard → `layout-dashboard`; reserved area → `ile-key` |
| `list` | «Mes demandes» · helpdesk queue · requests card · versions menu · glossary · index notice | — (retired) | requests → `send`; queue → `inbox`; versions → `history`; glossary → `book-a` |
| `handshake` | «Guichet numérique» · actor *authorised actor* · pathway *training in origin country* | the Forum (cooperation) | helpdesk → `concierge-bell`; authorised actor → `badge-check`; training → `book-open` |
| `compass` | «Ma situation» · orientation CTA · restart · antifraud «Espace Personnes» · living «Éducation civique» | orientation (situation = pre-orientation phase) | civic education → `vote`; «Espace Personnes» link → `person` |
| `warning` | notice warning/error · form error summary · **overdue** due date · pathway warnings | the warning notice | error → `circle-alert`; overdue → `alarm-clock` |
| `lock` | reserved-area access ×4 | BLOQUÉ (blocked) | reserved area → `ile-key` |

Minor: `calendar` (any date) is fine as «a date»; deadlines as a *domain* get `calendar-clock`.

---

## 3. Principles of the V5 map

- **P1 Bijection.** One concept → one symbol; one symbol → one concept. Enforced by a Python
  registry (`apps/core/icons.py`, §8.1) that every existing map imports from, and by a test (§8.5).
- **P2 Three tiers.** *Identity* (bespoke ILE: arch, key, steps, crossing, mark), *Concept*
  (audiences, actors, domains, navigation, phases, statuses — may carry the 12 % tone), *Utility*
  (actions, direction, feedback — monoline, never toned). A utility glyph may be typed literally in
  a template; a concept glyph reaches a template **only through the registry** (§8.5 test).
- **P3 The word carries the meaning; the glyph makes it recognisable at a glance.** Every glyph
  sits beside its word or gives its word to assistive technology (`.visually-hidden` / `aria-label`).
  Statuses remain words with a register (`core/chips.py`); the status glyph is an addition, not a
  replacement — and a neutro chip still carries none (badges.md §4.3) unless the owner decides
  otherwise (open question Q2).
- **P4 Families are allowed, twins are not.** Two glyphs may share a base (calendar, calendar-clock)
  only if the differing attribute is legible at 20 px; anything that needs 24 px to be told apart
  is a twin and one of the two goes.
- **P5 Direction mirrors, meaning does not.** The RTL flip list is closed and tested (§8.4).
- **P6 No glyph per row, no glyph per card, no bullets as icons.** Enumeration bullets
  (`ecosystem/partials/enumeration.html`), mega-menu sub-links and pathway lists return to
  typography. The DS 2026 «six per page» ceiling applies to the *editorial body* of public pages;
  the console chrome (rail, bottom bar, context bar) is exempt because the V4 direction made it an
  icon rail (open question Q1 records the conflict rather than hiding it).
- **P7 The arrow is a primary-CTA glyph.** `arrow` stays on `btn--primary` and on entry rows that
  are whole-row targets; `link-arrow` secondary links lose it (typographic «→» is already banned;
  the link is a link). Target: from 80 calls to ≈ 30.
- **P8 Nothing from the forbidden image vocabulary** becomes a glyph: no passport, luggage, plane,
  airport, queue, gate, barrier, border. Pre-departure is a checked clipboard, entry is the arch,
  the frontier is a crossing arc — never bars.

---

## 4. The base — one library, adapted to ILE

### 4.1 Candidates verified this session

| Set | Licence (verified) | Grid / format (verified on `folder`) | Verdict for ILE |
|---|---|---|---|
| **Lucide** | ISC (`lucide-icons/lucide/LICENSE`; Feather-derived icons MIT) | 24, **stroke** paths, `stroke-width 2`, round caps/joins on the root — caps/joins/width are *not* baked in | **Adopt as donor geometry.** Same grid as the ILE sprite (no rescale), stroke-based (the ILE CSS decides weight, caps, joins), ~1,600 glyphs covering every gap of §5, permissive licence with no runtime attribution. Under ILE treatment (1.5 px, square caps, miter, tone) the «shadcn/Linear» look disappears — that look *is* the 2 px round stroke. |
| Phosphor | MIT (`phosphor-icons/core/LICENSE`) | 256, **filled outlines** (`fill="currentColor"`), weight baked per file; duotone = a second path with `opacity="0.2"` | **Thesaurus only** (the task's dataset: 1,512 names + tags, no path data in the JSON). Cannot join a stroke sprite: `.icon { fill:none }` would hide it, and a filled/stroked mix is what DS 2026 §13 (R-DES-009) forbids. Its duotone grammar (a toned sub-shape) is what §4.3 adopts, in stroke form. |
| Iconoir | MIT | 24, stroke, `stroke-width 1.5` native, round caps | Runner-up. Closest native weight; slightly smaller «file-with-state» family; choosing it instead of Lucide is acceptable — **never both**. |
| Tabler | MIT | 24, stroke, `stroke-width 2`, round caps | Acceptable but the largest set (5,900) invites drift and reads «admin template»; not chosen. |
| Heroicons (outline) | MIT (not fetched this session) | 24, stroke, 1.5 | Too small a vocabulary (~300) for the concept tier; rejected as base. |
| Feather, Material Symbols, Font Awesome Free, Remix | not fetched this session | — | Rejected from knowledge: frozen (Feather), font/filled and a «Google» signature (Material), CC BY attribution + filled (FA), mixed line/fill (Remix). |
| 21st.dev | — | React components, not an icon library | Not a source for glyphs; **no 21st call was made for this deliverable, and no `generate`/`iterate_generation` call at any point.** |

### 4.2 The ILE treatment (what makes the set ILE's, whatever the donor)

| Rule | Value | Why |
|---|---|---|
| Grid | 24 × 24, live area 20 × 20 (2 px optical margin), key lines on the half-pixel for a 1.5 stroke | matches the existing 36 and the tests |
| Effective stroke | **1.5 px rendered at every size**: `stroke-width` per size class — 14 px → 2.57 · 16 → 2.25 · 20 → 1.8 · 24 → 1.5 · 32 → 1.25 (optical) · 48 → 1.0 | today 16 px renders 1.0 px and 14 px renders 0.875 px (§0.3) |
| Terminals | `stroke-linecap: square; stroke-linejoin: miter` (miter limit default 4 bevels anything sharper than ≈ 29°) | DS 2026 §13 asked for square terminals («rounded reads consumer»); the change is **one CSS rule** for the whole set because every path is stroked; dots drawn as `h.01`/`v.2` become 1.5 px squares, not nothing (never `butt`) |
| Corners | donors keep their 2 px rectangle radii in phase 2; bespoke glyphs are drawn with radius 1; a phase-3 pass may tighten donors to 1 | cost control — the caps/joins change already removes the «soft» look |
| Tone (duotone) | concept tier only: one extra sub-path inside the symbol, `fill="currentColor" fill-opacity=".12" stroke="none"` — the interior of the main shape (folder body, arch opening, book pages) | CSP-safe (no `<style>`, no `style=`, no hex — `currentColor` only), works through `<use>` because it is a presentation attribute on the cloned element, follows the icon's colour on paper and on navy; the tone is *never* on utility glyphs, so the two tiers are told apart by the eye |
| Colour | `currentcolor`; icons in the rail on navy use `--on-dark-2`, active `--on-dark`; on paper `--ink-2`; `--accent-2` is «the light» for the current/hover glyph (DS V4 §2) | unchanged |
| RTL | closed flip list (§8.4) via `.icon--flip-rtl` | unchanged mechanism |
| Forced colours | tone stays at 12 % of `CanvasText`; the register marks (rules) already survive `forced-colors` (chip.css) | verified rule exists for chips; the tone needs a visual check (limitation L4) |
| Motion | icons move only by `transform`/`opacity`: rail glyph −1 px on hover (exists), disclosure chevron rotates 180 (replaces the `plus` 45°), a status glyph on a chip *draws itself once* (`pathLength="1"`, 240 ms, `--ease-enter`) when the word changes; nothing loops; reduced motion → complete on first frame | the owner's «refined motion»; consistent with the V4 draw pattern (DS V4 §7 «draw») |

### 4.3 What the tone looks like in the sprite

```xml
<symbol id="icon-folder" viewBox="0 0 24 24">
  <!-- tone: concept tier only; currentColor at 12 %, never a hex -->
  <path fill="currentColor" fill-opacity=".12" stroke="none" d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>
  <path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>
</symbol>
```
(`icons/specimen.html` renders exactly this next to the untoned utility glyphs.)

---

## 5. THE MAP — one concept, one glyph

Columns: **Concept** · **Symbol id** (`icon-` prefix omitted) · **Geometry**: `ILE` = existing
ILE drawing kept (redrawn only by the CSS terminals), `ILE-new` = to draw, `Lucide <name>` = donor
path taken into the sprite under ILE rules · **Tier** I/C/U · **Tone** · **RTL** flip · **Replaces**.

### 5.1 Audiences and actors (the four doors, and who acts)

| Concept | Symbol | Geometry | Tier | Tone | RTL | Replaces / notes |
|---|---|---|---|---|---|---|
| **Persona** (audience) = the person actor = «vous» | `person` | ILE (head + shoulders) | C | yes | no | keeps; family reunification leaves |
| **Azienda / Impresa** (audience) = company actor = «Mon entreprise» | `building` | ILE | C | yes | no | keeps; self-employment, public services leave |
| **Istituzione** (audience) | `institution` | ILE (pediment + columns; Lucide `landmark` is the twin, not needed) | C | yes | no | keeps; project team, SSN leave |
| **Università e Formazione** (audience) = training-body actor | `university` | ILE (cap) | C | yes | no | keeps; Academy, école, study pathway leave |
| Professionista (actor, «Professionnels») | `briefcase` | ILE | C | yes | no | keeps; cases, needs, salaried work, taxation leave |
| Autorità competente (actor) | `stamp` | Lucide `stamp` | C | yes | no | the authority's act is a stamp (visa, nulla osta); replaces `shield` |
| **Attore autorizzato / acteur autorisé** (actor; also the phase «attore autorizzato») | `badge-check` | Lucide `badge-check` (scalloped seal + check) | C | yes | no | accreditation seal; replaces `handshake` |
| Équipe du projet (actor, message sender) | `ile-mark` | ILE-new: the mark mono at 24 (arch + key + steps) | I | no | no | the organisation's own avatar, as DS V4 #6 already lists («marchio ILE»); replaces `institution`/`user` |
| My account (summary, «Profil») | `circle-user-round` | Lucide | C | no | no | replaces `user` (symbol retired) |
| No actor / unknown | *(none)* | `glyph--none` dashed disc | — | — | — | exists; keep |

### 5.2 Platform domains and navigation (rail, bottom bar, account menu, context bar)

| Concept | Symbol | Geometry | Tier | Tone | RTL | Replaces |
|---|---|---|---|---|---|---|
| Tableau de bord (person and company) | `layout-dashboard` | Lucide | C | yes | no | `home` |
| **Ma situation** (orientation wizard) = orientation CTA = phase pre-orientamento | `compass` | ILE | C | yes | no | keeps |
| **Mon parcours** (the person's journey) = JourneyRail header = «Percorso» | `ile-steps` | ILE-new: three steps, unequal (6/11/16), the mark's own | I | no | no | `map-pin` |
| Voies régulières (public catalogue of pathways) | `signpost` | Lucide `signpost` | C | yes | **yes** | `map-pin` eyebrow default |
| **Mes dossiers / Fascicolo** (case files) | `folder` | Lucide `folder` (toned body) | C | yes | no | `briefcase` |
| **Mes pièces / Documenti** (the documents domain, a piece) | `document` | ILE | C | yes | no | keeps |
| Mes demandes (requests I sent to the guichet) | `send` | Lucide `send` | C | no | **yes** | `list` |
| Mes échéances (deadlines domain) | `calendar-clock` | Lucide | C | yes | no | `calendar` (which stays «a date») |
| **Communications / Messaggi** (message centre) | `mail` | ILE envelope | C | yes | no | keeps; e-mail *addresses* leave |
| **Guichet numérique / Helpdesk** (the digital counter) | `concierge-bell` | Lucide `concierge-bell` (dome on a plate) | C | yes | no | `handshake`; see Q3 (bell family) |
| Demandes qui me sont confiées (professional queue) | `inbox` | Lucide `inbox` | C | yes | no | `list` |
| **Academy** (courses) = phase formazione = pathway «formation dans le pays d'origine» = «Voir mes formations» | `book-open` | Lucide `book-open` (toned pages) | C | yes | no | `university`, `handshake` |
| Processus assignés / **Selezione** (selection processes of the authorised actor) | `list-checks` | Lucide | C | yes | no | `check` |
| Mes besoins (company needs in trades and skills) | `wrench` | Lucide | C | yes | no | `briefcase` |
| Analyse territoriale | `map` | Lucide `map` (folded map) | C | yes | no | `map-pin` |
| Mon organisation (institution / university accounts) | *the account type's audience glyph* | — | C | yes | no | `building` — data-driven, not a new symbol |
| **Forum Vénétie-Maroc** (cooperation forum, governance) | `handshake` | ILE | C | yes | no | keeps only this |
| Forum — édition | `calendar-range` | Lucide | C | no | no | new (forum has no glyphs today) |
| Forum — jalon / milestone | `milestone` | Lucide | C | no | **yes** | new |
| Forum — table de travail | `table` | Lucide | C | no | no | new |
| Forum — proposition | `file-plus` | Lucide | C | no | no | new |
| Forum — commission, projet | *(word only)* | — | — | — | — | no glyph: the twins `users-round`/`folder-kanban` would not pass P4 |
| Vivre en Italie (public section) = phase post-ingresso | `sprout` | Lucide | C | yes | no | new |
| Administration / back-office | `settings` | ILE gear (unused today) | C | no | no | new use |
| Notifications (context-bar bell, real badge) | `bell` | Lucide | U | no | no | new |
| Site public (link from the console) | *(text link)* | — | — | — | — | per CD §3.9 «come LINK» |
| Espace réservé / se connecter (access) | `ile-key` | ILE-new: the mark's key, vertical, ring + shank + two teeth | I | no | no | `lock` ×4 |
| Sécurité du compte (MFA, password) | `fingerprint` | Lucide | C | no | no | `key` |
| Se déconnecter | `logout` | ILE | U | no | **yes** | keeps |
| Langue | `languages` | Lucide (A/文) | U | no | no | new (the switcher is text today; optional) |
| Réduire / ouvrir la navigation (rail collapse) | `panel-left-close` | Lucide | U | no | **yes** | `chevron-end` |
| Menu (hamburger, public header, console bar, bottom bar) | `menu` | ILE | U | no | no | keeps; row menus leave |
| Menu de la pièce / row actions | `ellipsis-vertical` | Lucide | U | no | no | `menu` |
| Rechercher (field, command menu) | `search` | ILE | U | no | no | keeps; research pathway leaves |

### 5.3 Process phases — the public sequence, the seven journey steps, the eleven case states

The task names seven phases; the platform has seven locked journey steps (`portal.services.JOURNEY_STEPS`)
and eleven `CaseStatus` members. One glyph per phase; a step or a state that *is* that phase shares it.

| Phase (task) | Journey step (`JOURNEY_STEPS`) | `CaseStatus` | Symbol | Geometry | RTL | Note |
|---|---|---|---|---|---|---|
| **Pre-orientamento** | 1 «Votre situation et votre objectif» · 2 «Pré-évaluation et parcours possibles» | `draft`, `oriented`, `review_required` | `compass` | ILE | no | = «Ma situation» |
| **Formazione** | 3 «Préparation et formation avant le départ» | `training` | `book-open` | Lucide | no | = Academy |
| **Documentazione** (assembling the dossier) | — (runs across steps 2–4) | — | `document` | ILE | no | = the pieces; the *dossier* is `folder` |
| **Attore autorizzato** (selection under an authorised actor) | — | `selection` | `badge-check` | Lucide | no | = the actor |
| **Procedura** (with the competent authorities) | 4 «Procédures auprès des autorités compétentes» | `admin_process` | `scroll-text` | Lucide `scroll-text` | no | the administrative act; the *authority* is `stamp` |
| Preparazione alla partenza | 5 «Préparation du départ» | `pre_departure` | `clipboard-check` | Lucide | no | never luggage/plane (P8) |
| **Ingresso Italia** | 6 «Arrivée et premières démarches» | `entered` | `ile-arch` | ILE-new: the arch on its threshold line | no | **the brand's own moment**: you pass the door |
| **Post-ingresso** (accompagnamento e inclusione) | 7 «Accompagnement et inclusion» | `post_entry` | `sprout` | Lucide | no | = Vivre en Italie |
| Frontier MA → IT marker (JourneyRail) | between steps 3 and 4 | — | `ile-crossing` | ILE-new: two shores + one arc (the voyage route at 24 px) | **yes** | DS V4 #28 asks for «frontiera con glifo»: an arc, never bars |
| Sospeso | — | `suspended` | `circle-pause` | Lucide | no | register azione |
| Percorso concluso | — | `closed` | `archive` | Lucide | no | a fact, not a verdict (register neutro) |

Where phase glyphs appear: the public process/pilot sequence, «Prochaine étape» panels, timeline
events, the wizard's stepper header. The JourneyRail *nodes* stay dots (28 px, DS V4 #28); the
phase glyph sits in the descriptive (vertical) rail beside the label, 16 px.

### 5.4 Responsibility — who acts (ResponsibilityBar, glyph discs, checklist, evidence)

`cases.ResponsibleActor` and `documents.requirements.ACTOR_GLYPHS` become one table (registry §8.1):

| Actor | Symbol | Note |
|---|---|---|
| La persona / **vous** | `person` | = 5.1 |
| L'impresa / **the company** | `building` | = 5.1 |
| L'autorità competente | `stamp` | new |
| Il professionista incaricato | `briefcase` | keeps |
| L'ente di formazione | `university` | keeps (audience = actor) |
| Il soggetto autorizzato / **authorised actor** | `badge-check` | new |
| L'équipe del progetto / **institution running the platform** | `ile-mark` | new |
| unknown / none | dashed disc | exists |

«Institution» as a *responsible party* in the task's sense (the competent authority) is `stamp`; the
institution as an *audience* is `institution`. They are different concepts and get different glyphs.

### 5.5 Document statuses — eight words, eight marks (`documents.RequirementState` + «Bloqué»)

Chip glyphs render at 14 px (12 px dense) with `stroke: var(--chip-mark)`: a status glyph must be a
**mark**, not a pictogram (no file-with-arrow at 12 px). The register (gutter rule, dashed, closing
rule, struck, greyed) stays exactly as `chip.css` draws it; the mark is added in the `.chip__g` slot
that already exists in CSS and is rendered nowhere.

| Status (FR label) | Register (`chips.py`) | Symbol | Geometry | Reads as |
|---|---|---|---|---|
| **MANQUANT** | attesa | `circle-dashed` | ILE-new (dashed ring, same language as `glyph--none`) | an empty slot |
| **DÉPOSÉ** | neutro | `arrow-down-to-line` | Lucide | landed, filed |
| **EN EXAMEN** | neutro | `glasses` | Lucide `glasses` (two lenses + bridge) | someone is reading it — not `eye` (that is the view action) and not `search` (the control) |
| **VALIDE / VALIDÉ** | conforme | `check` | ILE | the affirmation mark; «conforme, never approved» — the word beside it says so |
| **NON VALIDE** | rifiuto | `ban` | Lucide `ban` (ring + slash) | not retained; distinct from `close` (the x control) |
| **EXPIRÉ** | azione | `hourglass` | Lucide | validity ran out |
| **À REMPLACER** | attesa | `refresh-cw` | Lucide | the same glyph as the *Remplacer* action — one concept |
| **BLOQUÉ** (`ChecklistStatus.blocked`, `EvidenceStatus.blocked`, doc-row «Bloqué» by the Conditions gate) | attesa | `lock` | ILE | held by a dependency, not refused; `lock` leaves the reserved-area links |

Neutro rule: per badges.md §4.3 a neutro chip carries no mark; DÉPOSÉ and EN EXAMEN therefore show
their glyph in legends, filters, timelines and the row identity, and *inside the chip* only if the
owner overrides the spec (Q2). `core.chips.GLYPH` (register → glyph) is replaced by
`documents.requirements.STATE_GLYPHS` (status → glyph); the five register marks it named
(`clock`, `warning`, `check`, `close`, `minus`) are retired as *register* glyphs.

### 5.6 Other status words (same mark family, per producer as in `chips.py`)

| Word (producer) | Symbol | Note |
|---|---|---|
| pending / en attente (checklist, evidence, scan, verification) | `clock` | ILE; «something is due, not late» |
| in progress / en cours | `circle-dot` | Lucide; not a spinner — a spinner promises motion the page does not make |
| done / completato / fourni / accepted / completed | `check` | affirmation |
| not applicable / sans objet / withdrawn / archived (nullo) | `slash` | Lucide `slash`; `minus` is freed for the *remove* action |
| rejected / infected (rifiuto) | `ban` | = NON VALIDE |
| suspended (case, process, project) | `circle-pause` | azione |
| needs clarification / professional review required / response available (ticket, azione) | `circle-alert` | «someone must act now» |
| information only (ticket) | `info` | |
| assigned / confiée à un professionnel | `briefcase` | the professional |
| closed / close (ticket, need, commission) | `archive` | a fact |
| verification approved (`chip--seal`) | `badge-check` | the one seal; same glyph as the accredited actor because it is the same act of accreditation |
| scan not configured | *(word only)* | honest absence: no glyph promises a scanner |

### 5.7 Selection and pathways (Selezione / percorso)

| Concept | Symbol | Geometry | Note |
|---|---|---|---|
| Selection process (domain, rail) | `list-checks` | Lucide | 5.2 |
| Stage — mandat confirmé | `badge-check` | | the actor's mandate |
| Stage — examen des compétences | `glasses` | | examination |
| Stage — vérification des justificatifs | `document` | | the pieces |
| Stage — examen par l'entreprise | `building` | | the company |
| Stage — processus clos | `archive` | | |
| Stage — suspendu | `circle-pause` | | |
| Identity disclosure (consent of the person) | `pen-line` | Lucide `pen-line` | the person signs; never a check on a person |
| Pathway — lavoro subordinato | `factory` | Lucide | |
| Pathway — Carta blu UE | `id-card` | Lucide | |
| Pathway — formazione nel paese d'origine | `book-open` | | = formazione |
| Pathway — studio e formazione in Italia | `backpack` | Lucide | |
| Pathway — ricongiungimento familiare | `users` | Lucide `users` | |
| Pathway — lavoro autonomo / imprenditoria | `store` | Lucide | |
| Pathway — ricerca scientifica | `flask-conical` | Lucide | |
| Pathway — altre vie regolari | `route` | Lucide | |

Pathway glyphs appear once per page (detail eyebrow, «Mon parcours» result) — never in the numbered
editorial list (P6).

### 5.8 Living-in-Italy topics (public), contact, public-site specifics

| Concept | Symbol | Geometry |
|---|---|---|
| Langue italienne | `languages` | Lucide |
| Logement | `house` | ILE `home` renamed `house`: housing only |
| Santé | `heart-pulse` | Lucide |
| Service sanitaire national (SSN) | `hospital` | Lucide |
| École | `school` | Lucide |
| Éducation civique | `vote` | Lucide |
| Droits et devoirs | `scale` | Lucide |
| Sécurité au travail | `hard-hat` | Lucide |
| Fiscalité de base | `receipt` | Lucide |
| Services publics | `building-2` | Lucide (check against `building` at 20 px — P4) |
| E-mail address (contact, footer, AGAMI) | `at-sign` | Lucide |
| Phone | `phone` | ILE (unused today) |
| Address / place | `map-pin` | ILE |
| Anti-fraud (panel, page, footer, callout) | `shield-alert` | Lucide |
| Institutional notice («guarantee», `kind="institutional"`) | `megaphone` | Lucide |
| Glossary | `book-a` | Lucide |
| FAQ | `circle-help` | Lucide |
| Actualités / news | `newspaper` | Lucide |
| Reference number («Référence» meta) | `hash` | Lucide |
| Rules version («Version des règles» meta) | `history` | Lucide (= versions) |
| Quote / testimony | `quote` | ILE (unused; keep for the forum) |

### 5.9 Actions and feedback (utility tier — monoline, never toned)

| Action | Symbol | Geometry | RTL | Note |
|---|---|---|---|---|
| **Déposer / upload** | `upload` | Lucide (tray + arrow up) | no | new; today the button is text-only, which is fine — the glyph is for the file field and the drop zone |
| **Remplacer / replace** | `refresh-cw` | Lucide | no | = À REMPLACER |
| **Télécharger / download** | `download` | ILE | no | keeps |
| **Consulter / aperçu / preview / afficher** | `eye` | Lucide | no | also «show password»; `eye-off` hides |
| **Supprimer / delete** | `trash-2` | Lucide | no | new |
| Versions / dépôts / history | `history` | Lucide | no | replaces `list` |
| Ajouter | `plus` | ILE | no | freed from the accordion |
| Retirer | `minus` | ILE | no | freed from chips |
| Modifier | `pencil` | Lucide | no | |
| Copier | `copy` | Lucide | no | |
| Marquer comme lue | `mail-open` | Lucide | no | replaces `check` |
| Filtrer | `list-filter` | Lucide | no | |
| Trier | `arrow-down-up` | Lucide | no | |
| Imprimer | `printer` | Lucide | no | optional |
| Suivant / continuer / CTA | `arrow` | ILE | **yes** | keeps, P7 halves its use |
| Précédent / retour | `arrow-start` | ILE-new (the same arrow, drawn pointing to reading start) | **yes** | pagination «prev» |
| Lien externe (authority sites) | `arrow-up-right` | ILE | no (DS rule) | keeps |
| Disclosure ▾ (select, account menu, accordion, mega-menu) | `chevron` | ILE | no | accordion rotates it 180° |
| Forward disclosure / breadcrumb separator | `chevron-end` | ILE | **yes** | keeps only these |
| Fermer | `close` | ILE | no | keeps |
| Info notice | `info` | ILE | no | keeps |
| Success notice | `circle-check` | Lucide | no | replaces bare `check` |
| Warning notice | `warning` | ILE triangle | no | keeps |
| Error notice / form error summary | `circle-alert` | Lucide | no | replaces `warning` |
| Pending notice | `clock` | ILE | no | keeps |
| Service unavailable (`form_unavailable`) | `circle-pause` | Lucide | no | replaces `clock` |
| Due date — upcoming | `calendar` | ILE | no | keeps |
| Due date — soon | `clock` | ILE | no | keeps |
| Due date — **overdue** | `alarm-clock` | Lucide | no | replaces `warning` |
| allauth alert | *per level*: `info` / `circle-check` / `warning` / `circle-alert` | — | — | fixes the «always info» defect |
| Empty state (any) | *(no icon)* | — | — | V4 rule: a hairline and a sentence; `.empty-state__icon` retires |

### 5.10 Retired symbols and new count

Retired: `user` (duplicate), `shield`, `globe`, `key` (generic), `list`; `home` renamed `house`;
`map-pin` stays (a place). Kept ILE drawings: 27. New bespoke: 7 (`ile-arch`, `ile-key`,
`ile-steps`, `ile-crossing`, `ile-mark`, `circle-dashed`, `arrow-start`). Donor glyphs: ≈ 62.
**Sprite ≈ 95 symbols, estimated 26–30 KB raw / ≈ 8 KB gzip** (donor paths average 200–300 B) —
one cached request, no LCP candidate, no CLS (every `.icon` has a fixed box).

---

## 6. The bespoke ILE glyphs — what stays hand-drawn, and why

These are the mark's grammar (`static/brand/original/logo-mark.svg`: two planes, an arched doorway,
a key, three steps) brought to the 24 grid. They are the identity tier: never replaced by a library
glyph, never toned (they are the tone of the whole set), never mirrored (except the crossing).

| Symbol | Drawing (24 grid, 1.5 stroke, square caps) | Used for | Draft in specimen |
|---|---|---|---|
| `ile-arch` | jambs at x 6 and 18 rising from y 19 to y 10.5, a semicircle r 6 closing them (apex y 4.5), and the threshold line x 3–21 at y 19; 12 % tone inside the opening (widened one unit each side after the render, §6.1) | **Ingresso Italia** phase; the brand tile in forced-colours; the login «entrance» at small sizes; the favicon (to be redone on the mark, BRAND_ASSETS §1) | yes |
| `ile-key` | ring r 3 at (12, 6.5), shank x 12 from y 9.5 to 20.5, two teeth to the end side at y 15 (3.5 long) and y 18.5 (2.5 long) — vertical, as it hangs in the door, not the diagonal «generic key» | **Espace réservé / access** (utility bar, drawer, home reserved panel, access point, login button) | yes |
| `ile-steps` | three horizontal lines of 6, 11 and 16 units at y 7, 12, 17 — the mark's 56/68/80 steps; unequal on purpose so it is never mistaken for `menu` (three equal) or `list` (dotted) | **Mon parcours / percorso**, the JourneyRail heading, the pilot sequence | yes |
| `ile-crossing` | two shore segments (x 3–7 and 17–21 at y 18) joined by one arc rising to y 10 — the `voyage_route` curve at 24 px; **mirrors in RTL** so Morocco stays at reading start | the **frontier MA → IT** marker of the JourneyRail (DS V4 #28), the pilot page | yes |
| `ile-mark` | the whole mark mono: arch + key + steps inside the 20 × 20 live area (planes omitted: at 24 px they close the shape into a badge) | **Équipe du projet** as an actor/sender avatar; never as a navigation glyph | yes |

### 6.1 Specimen render — what was verified (Chromium via Playwright, `icons/specimen-render.png`)

- The draft sprite is strict XML, 20 symbols, `viewBox 0 0 24 24` everywhere, no hex, no `<style>`,
  no `style=`, 4.5 KB. Served over HTTP and referenced through external `<use>` (the product's
  mechanism), **110 icon instances rendered, 0 empty** by the same `getBBox` gate that
  `docs/qa/design/capture.py` applies.
- One gate finding worth a rule: a dot drawn as a zero-length segment (`M12 5v.01`) draws with
  square caps but has a **zero bbox**, so the capture gate flags it. Rule for the build: dots are
  circles `r="1"` (Lucide's own convention), never zero-length paths. The existing ILE `warning`,
  `info` and `list` dots (`v.2`, `h.2`) pass because they have a length; keep them.
- Bespoke glyphs at 14 → 48 px: the key, the steps and the crossing read at every size; the arch
  was narrow at 14–16 px in the first render and has been widened one unit each side in the draft
  (jambs x 6/18, r 6, apex y 4.5 — the screenshot shows the first version); the mark is dense
  below 20 px — set its minimum at 20 (it is an avatar for 24/32 px discs, never a 14 px chip glyph).
- The eight status marks are legible at 14 px in a chip with the sketched register rules;
  `glasses` was the smallest of the eight and now has lens radius 3.75 in the draft (3.5 in the
  screenshot).
- Miter joins on the existing `handshake` and `arrow` paths produce no spikes (the default miter
  limit bevels the acute joins); the 12 % tone inside `folder` and `document` is visible on paper
  and on navy without reading as a fill.
- Comparison row (today's rule, round caps, 1.5 user units): the 14 and 16 px glyphs are visibly
  lighter than the 24 px ones — the under-weight finding of §0.3, seen.

Not bespoke any more: the four **landform** route glyphs (`_route_glyph.html`). DS V4 §9 retires
them in favour of actor glyphs; V5 confirms — at 20 px on navy a contour is a smudge, and the four
audiences already have glyphs that read at 14 px. The drawing stays in the repository history as
an ILE original; it does not enter the sprite.

The **favicon** (`static/img/favicon.svg`, three bars) predates the mark's recovery and is flagged
«da rifare sul marchio» by both design documents; V5 makes it `ile-arch` on navy, 32 px, and the
same file feeds the rail tile in forced-colours.

---

## 7. The fixes — every current site, where it goes

| Today (file : line or map) | Concept | V5 glyph |
|---|---|---|
| `portal.services.NAV_GLYPHS` | dashboard · situation · pathways · cases · requests · documents · deadlines · messages · helpdesk · academy · selection · company · helpdesk-queue | `layout-dashboard` · `compass` · `ile-steps` · `folder` · `send` · `document` · `calendar-clock` · `mail` · `concierge-bell` · `book-open` · `list-checks` · `building` · `inbox`; the `chevron-end` fallback becomes a registry error |
| `companies.services.navigation` | dashboard · needs · profile · analysis · messages | `layout-dashboard` · `wrench` · `building` · `map` · `mail` |
| `documents.requirements.ACTOR_GLYPHS` | person · company · authority · professional · training_body · authorised_actor · project_team | `person` · `building` · `stamp` · `briefcase` · `university` · `badge-check` · `ile-mark` |
| `pathways.services.DEFAULT_ICONS` | the 8 pathways | §5.7 |
| `living.catalogue.INITIAL_TOPICS` | the 10 topics | §5.8 |
| `pages.content.ENTRANCES` / `NETWORK_ACTORS` | 4 audiences + professionals | unchanged glyphs (`person`, `building`, `institution`, `university`, `briefcase`) — they were right |
| `portal.services` cards (requests, pathways, documents, deadlines, messages, organisation) | | `send` · `ile-steps` · `document` · `calendar-clock` · `mail` · audience glyph of the account |
| `core.chips.GLYPH` (unrendered) | register → glyph | **deleted**; `documents.requirements.STATE_GLYPHS` (status → glyph, §5.5) rendered in `.chip__g` |
| `components/account_menu.html:7,15` `user` | my account | `circle-user-round` |
| `components/account_menu.html:13` `home` | Espace réservé | `ile-key` |
| `components/account_menu.html:17` `key` | Sécurité du compte | `fingerprint` |
| `partials/utility_bar.html:23`, `header.html:33`, `pages/home/_reserved.html:10`, `portal/partials/access_point.html:20,23` `lock`/`home` | reserved area | `ile-key` |
| `components/document_row.html:20` `document` disc | row identity | keep `document` **or** the document *kind* if a kind field exists (Q4); never the status |
| `components/document_row.html:41` `warning` overdue | overdue | `alarm-clock` |
| `components/document_row.html:57` `menu` | row actions | `ellipsis-vertical` |
| `components/document_row.html:59` `document` «Consulter» | view | `eye` |
| `components/document_row.html:61` `list` «n dépôts» | versions | `history` |
| `components/document_row.html` state chip | status | `+ {% svg_icon row.state_glyph "chip__g" %}` from `STATE_GLYPHS` |
| `components/notice.html:7` | info / success / warning / error / pending | `info` / `circle-check` / `warning` / `circle-alert` / `clock` |
| `allauth/elements/alert.html:1` | always `info` | per `attrs.level` |
| `components/form_errors.html:6` `warning` | error summary | `circle-alert` |
| `components/form_unavailable.html:4` `clock` | unavailable | `circle-pause` |
| `components/option_cards.html:22` `check` | selected | keep `check` |
| `components/accordion.html:9` `plus` | expand | `chevron` (rotate 180°) |
| `components/pagination.html:6,8` `arrow` ×2 | prev / next | `arrow-start` / `arrow` |
| `partials/main_nav.html:24` `chevron-end` bullets | sub-links | none |
| `partials/portal_chrome.html:27` `chevron-end` | rail collapse | `panel-left-close` |
| `ecosystem/partials/enumeration.html:11` (`institution`, `university`, `check` bullets) | list bullets | none (typographic) |
| `ecosystem/companies.html:30` `mail`, `pages/contact.html:18`, `partials/footer.html:13`, `errors/base_error.html:19`, `pages/agami.html:41`, `pathways/index_interim.html:47` | e-mail address | `at-sign` |
| `ecosystem/companies.html:39` `shield` | institutional notice | `megaphone` |
| `pages/home/_antifraud.html:9`, `pages/antifraud.html:21`, `partials/footer.html:37`, `pathways/_antifraud_callout.html:7` `shield` | anti-fraud | `shield-alert` |
| `pages/antifraud.html:35-37` `info`/`compass`/`list` | FAQ · Espace Personnes · glossary | `circle-help` · `person` · `book-a` |
| `portal/pathways.html:36-39` `calendar`/`document`/`info`/`key` metas | date · rules version · state · reference | `calendar` · `history` · status glyph · `hash` |
| `portal/message_detail.html:14-16,28` | date · sender · read state · mark as read | `calendar` · `ile-mark` · `mail-open` (state) · `mail-open` (button) |
| `pages/home/_news.html:19` `document` empty state | news | none (empty states lose icons) |
| `portal/*.html` empty states (`calendar`, `mail`, `list`, `compass`) | | none |
| `pathways/detail.html:82` `document` bullets, `:102` `arrow-up-right`, `:114` `warning` | pieces list · authority site · warning | none · keep · keep |
| `living/index.html:21`, `living/topic.html:12` | topics | §5.8 |
| `cases/detail.html:47` `person` fallback «Vous» | the person | keep |
| `companies/dashboard.html:86` `building` | the company | keep |
| 45 `link-arrow` / `entry__arrow` sites | secondary links | typography only (P7); `btn--primary` keeps `arrow` |

---

## 8. Engineering contract (proposal — nothing applied)

### 8.1 Registry — `apps/core/icons.py`

```python
"""One concept, one glyph. Every map that chooses an icon reads from here; templates may type a
literal only from UTILITY. Tested: bijection, existence in the sprite, closed RTL list."""
TIER_IDENTITY = {"ile-arch", "ile-key", "ile-steps", "ile-crossing", "ile-mark"}
UTILITY = {"arrow", "arrow-start", "arrow-up-right", "chevron", "chevron-end", "menu", "close",
           "ellipsis-vertical", "search", "plus", "minus", "upload", "download", "refresh-cw", "eye",
           "eye-off", "trash-2", "history", "pencil", "copy", "mail-open", "list-filter",
           "arrow-down-up", "printer", "panel-left-close", "logout", "languages", "bell",
           "info", "circle-check", "warning", "circle-alert", "clock", "circle-pause",
           "calendar", "alarm-clock"}
CONCEPT = {  # concept key → symbol; keys are what the code says, symbols are what the sprite has
    "actor.person": "person", "actor.company": "building", "actor.authority": "stamp",
    "actor.professional": "briefcase", "actor.training_body": "university",
    "actor.authorised_actor": "badge-check", "actor.project_team": "ile-mark",
    "audience.institution": "institution", "audience.university": "university",
    "nav.dashboard": "layout-dashboard", "nav.situation": "compass", "nav.pathways": "ile-steps",
    "nav.cases": "folder", "nav.requests": "send", "nav.documents": "document",
    "nav.deadlines": "calendar-clock", "nav.messages": "mail", "nav.helpdesk": "concierge-bell",
    "nav.academy": "book-open", "nav.selection": "list-checks", "nav.company": "building",
    "nav.helpdesk_queue": "inbox", "nav.needs": "wrench", "nav.analysis": "map",
    "phase.pre_orientation": "compass", "phase.training": "book-open", "phase.documents": "document",
    "phase.authorised_actor": "badge-check", "phase.procedure": "scroll-text",
    "phase.pre_departure": "clipboard-check", "phase.entry": "ile-arch", "phase.post_entry": "sprout",
    "phase.frontier": "ile-crossing",
    "doc.missing": "circle-dashed", "doc.filed": "arrow-down-to-line", "doc.in_review": "glasses",
    "doc.valid": "check", "doc.invalid": "ban", "doc.expired": "hourglass",
    "doc.to_replace": "refresh-cw", "doc.blocked": "lock",
    # … pathways, living topics, forum, contact, public specifics as in §5 (full list: icons/icon_map_v5.json)
}
FLIP_RTL = {"arrow", "arrow-start", "chevron-end", "logout", "send", "signpost", "milestone",
            "panel-left-close", "ile-crossing"}
```
`NAV_GLYPHS`, `companies.services.navigation`, `ACTOR_GLYPHS`, `DEFAULT_ICONS`, `INITIAL_TOPICS`,
`ENTRANCES`, `NETWORK_ACTORS`, the portal cards and `STATE_GLYPHS` import their symbols from
`CONCEPT` — the maps keep their shape, they stop choosing.

### 8.2 Sprite build — `static/icons/src/*.svg` → `static/img/icons.svg`

- One file per symbol, already normalised (24 grid, no root attributes, no `stroke`/`fill` on paths
  except the tone path, no hex, no `<style>`, no `style=`, no `--` in comments).
- `scripts/build_icons.py` (new, stdlib only): concatenates into `<defs>`, validates with a strict
  XML parser, checks `viewBox`, forbids `#[0-9a-f]{3,6}`, `<style`, `style=`, and writes the DS §13
  list between `<!-- icon-list:start -->` / `end` — the same «dist is current» discipline as
  `tests/frontend/test_css_bundle_is_current.py`.
- Donor import: copy the Lucide path data of the named glyph into a `src` file **without** its root
  attributes (they carry the 2 px round look), add the tone path where the map says so. Keep
  `docs/design-v5/ICON_LICENSES.md`: Lucide ISC text + list of borrowed names (attribution is not
  required at runtime; the record is a project rule, like `IMAGE_LICENSES.md`).

### 8.3 CSS — `static/css/components.css` §2 (and `v3/chip.css` `.chip__g`)

```css
.icon { inline-size: var(--icon-md); block-size: var(--icon-md); flex: none; fill: none;
        stroke: currentcolor; stroke-width: 1.8;               /* 20 px → 1.5 px rendered */
        stroke-linecap: square; stroke-linejoin: miter; vertical-align: middle; }
.icon--xs { inline-size: var(--icon-xs); block-size: var(--icon-xs); stroke-width: 2.57; }
.icon--sm { inline-size: var(--icon-sm); block-size: var(--icon-sm); stroke-width: 2.25; }
.icon--lg { inline-size: var(--icon-lg); block-size: var(--icon-lg); stroke-width: 1.5; }
.icon--xl { inline-size: var(--icon-xl); block-size: var(--icon-xl); stroke-width: 1.25; }
.icon--hero { inline-size: var(--icon-hero); block-size: var(--icon-hero); stroke-width: 1; }
.glyph--sm .glyph__icon { stroke-width: 2.57; } .glyph__icon { stroke-width: 2.25; }
.glyph--lg .glyph__icon { stroke-width: 1.8; }
.chip__g { stroke-linecap: square; stroke-linejoin: miter; }   /* 2.6 stays: 1.52 px at 14 */
.rail__glyph { stroke-width: 1.8; } .console-bottom__item .icon { stroke-width: 1.8; }
```
(`--icon-size*` legacy tokens map to the V4 `--icon-*` ones; DS 2026 §17 already lists them as
«valore letterale, nessun token di destinazione».)

### 8.4 RTL — closed list

Mirrored with `.icon--flip-rtl`: `arrow`, `arrow-start`, `chevron-end`, `logout`, `send`,
`signpost`, `milestone`, `panel-left-close`, `ile-crossing`. Never mirrored: everything else,
including `arrow-up-right` (DS 2026 §13), `history`, `refresh-cw`, `ile-key`.

### 8.5 Tests to add (`tests/frontend/test_icons.py`)

1. `CONCEPT` values ∪ `UTILITY` ∪ `TIER_IDENTITY` == sprite ids (no orphan, no phantom).
2. No symbol appears under two concept keys unless listed in `SHARED` with a reason — the
   exception register, reviewed, not a loophole. The draft registry (`icons/icon_map_v5.json`,
   133 concept keys → 110 symbols) declares 21 such sharings, each the *same concept seen from two
   producers*: `person` audience/actor/you · `building` audience/actor/company review ·
   `university` audience/training body · `book-open` academy/phase/pathway · `refresh-cw`
   status/action · `badge-check` actor/phase/mandate/seal · `compass` situation/CTA/phase ·
   `document` domain/piece/phase/evidence review · `glasses` en examen/competence review ·
   `sprout` post-entry/living · `check` affirmation · `archive` closed-as-a-fact · `briefcase`
   professional/assigned · `languages` switcher/topic · `circle-pause` suspended/unavailable ·
   `ban` non valide/rejected · `clock` pending/soon · `circle-alert` needs action/error · `info`
   information · `history` versions/rules version · `calendar` date/upcoming.
3. Every `svg_icon "<literal>"` in templates ∈ `UTILITY` (concept glyphs travel through context).
4. Every symbol in `FLIP_RTL` is only ever rendered with `icon--flip-rtl`, and no other symbol is.
5. Sprite: strict XML, `viewBox 0 0 24 24`, no hex, no `<style`, no `style=`, ≤ 32 KB.
6. `STATE_GLYPHS.keys() == set(RequirementState) | {"blocked"}`; `ACTOR_GLYPHS.keys() == set(ResponsibleActor)`.
7. Build-is-current: rebuilding the sprite from `src/` changes nothing.

### 8.6 Accessibility and performance checklist

- Decorative beside text (`aria-hidden`, as today); icon-only controls keep `.visually-hidden` text
  (row menu, close, rail collapsed — the rail tooltip exists); `role="img"` + label when the glyph is
  the only carrier (none planned).
- Never colour alone: statuses keep word + register + mark; urgency keeps word + glyph.
- Forced colours: strokes follow `CanvasText`; tone at 12 % remains faint, acceptable (verify, L4).
- Hit areas unchanged (40 px IconButton + 44 hit).
- Sprite ≈ 8 KB gzip, cached, one request; no icon is an LCP candidate; fixed boxes → no CLS.
  Hero legend glyphs sit in the LCP viewport: if a sprite pop-in is measured on slow 4G, inline
  those four symbols in the hero template (Django include of `src/` files) — measure first.

---

## 9. Migration in three phases (estimate: 3–4 developer-days + ½ day design review)

| Phase | Scope | Risk |
|---|---|---|
| **1 — Contract (½ day)** | `core/icons.py` registry; CSS §8.3 (terminals + stroke per size); `STATE_GLYPHS` rendered in `.chip__g`; tests 1–7 (2–3 red until phase 2); allauth alert per level | CSS terminals change all 36 existing glyphs at once — check `handshake`, `phone`, `quote` joins in the specimen before commit («re-measure after every change») |
| **2 — Vocabulary (1½ days)** | `src/` folder + `build_icons.py`; 7 bespoke drawn from the specimen drafts; ≈ 62 donor imports with tone; sprite ≤ 32 KB; DS §13 list regenerated; `ICON_LICENSES.md` | Lucide names in §5 are from the current catalogue as known to me; the import script must fail loudly on a missing name (L2) |
| **3 — Sites (1–1½ days)** | §7 table, public first (nav, footer, contact, antifraud, ecosystem bullets), then console (rail, rows, chips, menus, account); remove `link-arrow` glyphs; favicon on the arch; screenshots at 14/16/20/24 on paper and navy in `docs/qa/design/capture.py` | «max six per page» and «no icon per row» tests, if any exist in `test_design_docs.py`, must be re-scoped to the editorial body (Q1) |

---

## 10. Open questions for the owner

- **Q1** The DS 2026 §13 ceiling («at most six icons per page», «never an icon per row») and the V4
  console (rail of 10–13 glyphs, glyph disc on every document row) contradict each other. V5
  proposes: ceiling on the editorial body of public pages; chrome exempt; rows carry a glyph only
  when it says something (status mark, actor) — the identity `document` disc on every row is
  decoration unless a document *kind* exists (Q4).
- **Q2** Neutro chips (DÉPOSÉ, EN EXAMEN) carry no mark per badges.md §4.3. Keep the spec (mark in
  legends and timelines only) or override for the eight document statuses?
- **Q3** «Guichet numérique» as `concierge-bell` is the most pertinent and memorable choice, but it
  shares the bell family with notifications (`bell`, context bar). The specimen shows both at 20 px;
  if the owner reads them as twins, the fallback is `messages-square` for the guichet.
- **Q4** Is there (or should there be) a document *kind* (identity, attestation, contract, photo,
  form) on `documents.requirements`? If yes, the row identity disc becomes pertinent
  (`id-card`-family avoided; use `file-badge`, `file-text`, `file-image`, `pen-line`); if no, keep
  one neutral `document`.
- **Q5** Accept ISC-licensed donor geometry inside the ILE sprite (with `ICON_LICENSES.md`), or
  commission the ≈ 62 missing glyphs as originals (≈ 3 designer-days more, same rules)?
- **Q6** The four landform route glyphs: retire from the home entrances (as DS V4 §9 says) — confirm.

## 11. What was not done, and why

- **L1** No file in the repository was touched (read-only phase); the sprite, CSS and registry are
  proposals with exact paths. The specimen SVG is a draft of 14 symbols, not the sprite.
- **L2** Lucide glyph names in §5 were not each verified against the live catalogue this session
  (only `folder` was fetched, to verify format and licence); names I am less sure of are
  `concierge-bell`, `book-a`, `arrow-down-to-line`, `panel-left-close`, `circle-user-round` — the
  build script must fail on a missing name, and the runner-up for each is in §5.
- **L3** UI-UX-Pro-Max `search.py --domain icons` covers only its 105 curated Phosphor entries:
  most concept queries (institution, university, helpdesk, forum, phases, statuses) returned
  nothing; the Phosphor upstream JSON (1,512 names + tags, no paths) was searched directly and used
  as a thesaurus. Results informed the choices; they did not decide them.
- **L4** No browser measurement of the proposed CSS (terminals, stroke per size, tone in forced
  colours) on the real pages: the specimen renders the rules in isolation; the «re-measure after
  every change» rule applies at phase 1.
- **L5** No 21st.dev search was made: icons are not a 21st component category, and the task's
  A/B/C/D classification is for UI patterns; every glyph here is class A (Django + CSS + sprite).
- **L6** The forum, helpdesk, selection and academy templates use no icons today except arrows;
  their entries in §5 are for the V5 shells that other specialists are designing.
