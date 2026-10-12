# UX_PLATFORM.md — Senior UX panel, PLATFORM (V5 escalation)

Council V5 «premium escalation» · 27 September 2026 · read-only phase.
Panel scope: Dashboard UX · Document Workspace UX · Case / Fascicolo · Company / B2B · Academy · Forum ·
Notifications · Search / Command · Form UX · Accessibility.

What this panel touched and did not touch:
- Nothing under `C:/tmp/italylegalentry` was modified. This file is the only one written.
- No browser was driven, no form was submitted, and no password was typed.
- Nothing was fetched from Pexels or 21st.dev by this panel (§11).

---

## 0. Verdict in twelve lines

1. **The platform is not premium because it is two products sharing one frame.** Only **5** authenticated templates
   speak the V4 console language: dashboard, documents, case detail, «Ma situation» and the company dashboard.
   - **About 32 more** still render the V2 editorial register (`folio`, `register`, `entry`, `portal-section`). These
     include the piece detail, the assessment result, every Academy page, the whole Forum governance module,
     selection, the helpdesk lists and the need detail.
   - Five more (requests, messages, deadlines, pathways, request detail) are V2/V3 lists.
   - One click below the dashboard, the person falls from a 2026 console into a 2024 document (§2 D1).
2. **The journey is fractured by the data, not only by the design.** On the same case `EE167596D4`, four screens
   disagree:
   - the dashboard says the next action is «Compléter le questionnaire d'orientation»;
   - the documents page says «Remplacer la pièce»;
   - the case page says «Aucune pièce n'est encore demandée»;
   - the documents page counts «3 pièces demandées».

   The dashboard's one primary button also leads out of the console into the **public** shell (`/orientation/`
   extends `base.html`). None of this is a paint problem (§2 D3, §6).
3. **The V4 specification was built at about half.** These were designed and never shipped:
   - the V4 Chip (glyph per register, full border) and the Badge counter;
   - the bell and notification panel, and search in the context bar;
   - Toast, Skeleton, Tooltip and Switch;
   - the Upload flagship and the document preview drawer;
   - the staff CommandMenu;
   - the sliding segmented thumb and the rail's travelling indicator.

   What is live is the frame of V4 with the V3 content inside it.
4. **Status is illegible.** Every chip is the same grey pill carrying the V3 «vidimazione» gutter rule. On a pill,
   the phase gauge (a shortened rule) reads as a rendering glitch: the tick on «Brouillon», the dashed stub on
   «À remplacer». The gauge is deliberate (`static/css/v3/chip.css` §4) and fails anyway. The rule «no colour ever
   means approved» is right; the execution needs a different shape (§5).
5. **The HealthStrip lies by metaphor.** It is two-thirds filled in dark ink while the caption says «0 sur 3
   validées» (§3.3).
6. **Rows do not align.** Each `doc-row` is its own grid with an `auto` action column. «Consulter» and «Remplacer la
   pièce» give different widths, so the state column drifts from row to row (`before_documents_1440.png`, third
   row). The register has no column headers (§3.3).
7. **A new person's dashboard is mostly grey prose.** Four of seven panels are one sentence each (échéances,
   communications, academy, and the tail of mon compte). The doctrine «one hairline and one sentence, never a dashed
   box» is honest, but it produces a dead screen and contradicts DS V4 §8.30, which specified a real EmptyState
   (§3.2).
8. **Pages have no continuity, and actions give no feedback.** There is no loading cue, no skeleton and no toast.
   - The icons pop in late because the sprite is external.
   - When the vertical scrollbar appears, the context bar's end items jump about 15 px (fp+0250 → fp+1200).
   - «Enregistrer et recalculer» recomputes the person's legal orientation and never says what changed (§3.12).
9. **The shell is a competent navy SaaS rail with no identity moment.** The brand appears only as a 40 px tile. The
   rail is **icon-only by default below 1440 px** (most laptops), so icons carry the meaning for occasional,
   multilingual users. The account menu is anonymous: no name, role, organisation or space switcher (§3.1).
10. **The accessibility foundations are the best part; do not trade them away.** Native `<dialog>`, `aria-current`,
    logical properties, live counts on search, words beside every bar, a non-chromatic state channel and
    reduced-motion branches are all in place. The gaps are real but local (§3.13).
11. **V5 for the platform = finish V4, then escalate three signatures.** The signatures are «la soglia» journey
    rail, the Piece Ledger (status that reads) and the Dépôt (upload as the flagship interaction). Continuity wraps
    them: the thread, busy keys, toasts and a unified next-action engine. **No React island is needed anywhere on the
    platform:** every pattern here is route A or B; route C = 0.
12. **Priority order:**
    - P0 — coherence and truth: one next action, one list of what is asked, CTAs that stay in the console, chips
      that read.
    - P1 — the flagship interactions: upload, preview, piece ledger, notifications.
    - P2 — migrating the 32 V2 templates onto the V5 kit, the command surfaces, the identity moments.

Scores below are my judgment of «world-class 2026 platform» quality, not compliance (10 = Linear / Mercury / Stripe
grade for its domain):

| Surface | Today | Main reason | V5 target |
|---|---|---|---|
| App shell (rail, bar, bottom bar, drawer, account) | 5 | competent but anonymous; icon-only by default; no bell or search | 8 |
| Person dashboard | 4 | the next action is disconnected from its CTA; empty prose; truth conflicts | 8 |
| Document workspace («Mes pièces») | 5 | best V4 page, but rows misalign, chips are illegible, and upload is a bare input on another page | 9 |
| Case / fascicolo | 4 | two «où en est…» panels; contradictory checklist; an admin `<select>` for state change | 8 |
| «Ma situation» (wizard) | 5 | good bones; counter says 7 while 8 questions show; browser-locale date; no «what changed» | 8 |
| Company / B2B | 5 | a proper table, but identical chips and repeated buttons; the «Vérifiée» seal is questionable | 8 |
| Academy | 3 | a V2 serif island inside the console | 7 |
| Forum governance | 1 | placeholder rendered in the PUBLIC shell under `/espace-reserve/` | 7 (once opened) |
| Guichet numérique | 2 | captured unstyled (fixed after capture, not re-verified); V2 register lists | 7 |
| Notifications | 0 | absent from the UI, although the model exists | 7 |
| Search / command | 1 | only the in-page filter on «Mes pièces» | 7 |
| Loading & feedback | 2 | nothing covers a wait; no outcome feedback | 8 |
| Accessibility (foundations) | 7 | strong semantics; local gaps | 9 |

---

## 1. Evidence base

### 1.1 Captures read (16 PNGs, one at a time, platform only)

All are from `C:/tmp/ile_v5_council/captures/`, listed in `council/CAPTURES_AND_REFERENCES.md` §4, and were
captured on 26 Sept on port 8771 by the capture role.

| # | File | What I took from it |
|---|---|---|
| 1 | `before_dashboard_1440.png` | Shell and ContextHeader; the next-action panel without its CTA; the Dossier facts; the JourneyRail; the HealthStrip; the compact rows |
| 2 | `before_dashboard_1440_full.png` | The whole dashboard: the deposits list («non analysé»), three empty panels, «Mon compte» with «· Entreprise», the untranslated footer «Privacy Policy» |
| 3 | `before_dashboard_390.png` | Top bar; «Continuer» detached above its card; bottom bar with hyphenated two-line labels |
| 4 | `before_documents_1440.png` | Register: filters with register dots, search, rows whose columns drift, the ≡ row menu, the footnote |
| 5 | `before_documents_390.png` | Mobile register: horizontal filter scroller; the first piece is below the fold |
| 6 | `before_case_1440.png` | Case: vertical journey, the «Où en est votre demande» timeline, a repeated next action |
| 7 | `before_case_1440_full.png` | «Ce qui est demandé: aucune pièce» (the contradiction), «Qui intervient», the «Faire évoluer l'état» admin form |
| 8 | `before_situation_1440.png` | Wizard: stepper with 8 questions, counter «0 … sur 7», foot «1 / 8», date field `mm/dd/yyyy` on a FR page |
| 9 | `before_entreprise_1440.png` | Company ContextHeader; the «Vérifiée» chip with the seal cut; the next action versus the «Ouvrir le besoin» CTA |
| 10 | `before_entreprise_1440_full.png` | Needs table: four different states drawn as four identical grey chips, and four identical «Ouvrir le besoin» buttons |
| 11 | `before_formation_1440.png` | Academy: serif, a numbered register, indented differently from the console; «Mes formations» sub-entry without a glyph |
| 12 | `before_forum-permanent_1440.png` | Forum permanent: public header and footer under a reserved URL; an amber notice |
| 13 | `before_loading-dashboard_1440_fp+0250ms.png` | Rail without icons; empty workspace; no cue |
| 14 | `before_loading-dashboard_1440_fp+1200ms.png` | Complete page; the scrollbar has appeared and the context bar's end items moved about 15 px |
| 15 | `before_dashboard-accountmenu_1440.png` | Account menu: four links, no identity header |
| 16 | `before_console-drawer_390.png` | Phone drawer: the best-looking mobile surface (icon rows, groups, language) |

Not re-read because of the 16-image budget:
- **The Guichet captures.** The capture role diagnosed them as unstyled (missing `portal/console.css`). Commit
  `c9a58d8` («helpdesk: keep the console shell's stylesheets») landed **after** the captures, so the Guichet's
  current appearance is **unverified** by this panel.
- **The case at 390 and the collapsed rail.**
- **The Arabic console:** no AR console capture exists.

### 1.2 Code and documents read

**Templates**
- `templates/portal/{base_portal,dashboard,situation}.html`
- `templates/partials/portal_chrome.html`
- `templates/portal/partials/{rail_nav,next_action}.html`
- `templates/cases/detail.html`
- `templates/components/{document_row,health_strip,journey_rail,empty_state,account_menu}.html`
- `templates/documents/{upload,requirement_detail}.html`
- `templates/companies/dashboard.html`
- `templates/academy/{base_academy,catalogue}.html`
- `templates/helpdesk/base_helpdesk.html`
- `templates/forum/governance/{base_governance,unavailable}.html`
- `templates/selection/workspace.html`
- a class census of every platform template

**CSS**
- `apps/portal/static/portal/console.css`: rail, bottom bar
- `static/css/v4/workspace.css`: doc-row, chips, panel sections
- `static/css/v3/chip.css`: registers, gauge, seal
- `static/css/tokens.css`: chrome tokens
- `static/css/base.css`: scroll padding
- `apps/academy/static/academy/academy.css`

**JS:** `static/js/src/{console,motion}.js`

**Python**
- `apps/cases/services.py`: `next_action`
- `apps/cases/views.py`: checklist source
- `apps/portal/views.py`: situation counter
- `apps/accounts/models.py`: `PROFILE_FIELDS`
- `apps/core/templatetags/ile_core.py`: `svg_icon` points to the external sprite
- `apps/documents/views.py`: download is audited and throttled
- `apps/companies/services.py`: CTA labels
- `apps/notifications/models.py`: `Notification` with a read state

**Project docs**
- `docs/design-v4/CREATIVE_DIRECTION.md` §1–3.9
- `docs/design-v4/DESIGN_SYSTEM_V4.md` §7–8
- `docs/source-of-truth/CONFLICT_REGISTER.md` CR-03 / CR-04
- `docs/ACCESSIBILITY.md` G-08

**Council docs** (read so that this panel builds on them instead of duplicating them)
- `21st_platform-domains.md`, `21st_nav-shell.md`, `21st_forms-docs.md`: matrices and selected patterns
- `21st_primitives.md`: chips, notification center
- `MOTION.md` §0, §5.5–5.9, §6.3, §6.7
- `IMAGERY.md` §3.19
- `COLOUR.md` §5
- `ICON_SEMANTIC_MAP.md`: row menu, missing glyphs
- `CAPTURES_AND_REFERENCES.md`

The project memory warns that visual defects are often deliberate («three of three obvious repairs were wrong»).
Every critique below that touches a documented decision names that decision and says whether V5 should **keep**,
**re-express** or **reverse** it. Reversals are owner decisions (§9).

---

## 2. Cross-cutting diagnosis — the eight structural reasons

### D1 · Two design languages inside one shell (the main cause)

Class census per template: V2 register classes (`folio`, `register`, `entry`, `portal-section`, `t-folio`) versus
V4 classes (`panel panel--`, `ctx`, `ws-head`, `doc-row`, `table`).

**V4 (5 templates)**
- `portal/dashboard.html`
- `portal/documents.html`
- `cases/detail.html`
- `portal/situation.html`
- `companies/dashboard.html`

**V2 register (about 32 templates)**
- `documents/requirement_detail.html`
- `cases/assessment.html`, `cases/index.html`
- all `academy/*`
- all `forum/governance/*`
- all `selection/*`
- `helpdesk/{requests,queue,detail,dispatch}.html`
- `companies/{need_detail,analysis,needs,profile,profile_form,need_form}.html`

**V2/V3 lists (5 templates)**
- `portal/{requests,messages,deadlines,pathways,request_detail}.html` (`portal-list`, `account-table`,
  `portal-result`)

The two most important depth pages are V2: the **piece detail**, where you upload, and the **assessment result**,
where you learn your pathway. The pages that feel «premium» are the summaries; the pages where the work happens are
not. No V5 visual escalation will read as premium until the depth pages share the kit.

→ **Move:** a migration plan by component family (§4), not by page.
- Every V2 register instance maps to one of five V5 families: DocumentRow/Collection, Table, Timeline, Register-row
  V5, Panel/Facts.
- Templates change class hooks only.
- The domain markup stays: words, legal caveats, `lang`, sources.

### D2 · The V4 spec shipped at about half

| DS V4 §8 component | Status in code (27 Sept) |
|---|---|
| #3 Chip (glyph per register + full 1 px border in register style) | **not built.** The V3 gutter rule sits inside a pill; chip templates carry no glyph |
| #4 Badge (numeric counter) | not built |
| #15 Tooltip | only the rail's own tip |
| #16/17 Popover / Menu | built for the doc-row menu (native popover, placed by JS) |
| #19 Drawer (preview) | not built |
| #20 Toast | not built; Django messages stay page notices |
| #26 Upload (flagship) | not built: a bare `ClearableFileInput` on the V2 piece page |
| #30 EmptyState V4 | contradicted by the dashboard doctrine (`<p class="empty">`) |
| #31 Skeleton | not built |
| #34 Search in the context bar / #35 CommandMenu | not built |
| §3.9 bell + notifications panel | not built, although the `Notification` model with its read state exists |
| §3.9 travelling rail indicator, §8.14 sliding segmented thumb | not built (static `aria-current` styling) |
| §3.6.1 compact case bar on scroll | **built** (`console.js` §2c, `data-ctx-bar`) |

→ **Move:** the V5 platform kit (§4) is mostly «build what V4 already decided, with V5 craft». That is lower risk and
faster than inventing new shapes.

### D3 · The journey is fractured by the model

- **Next action vs pieces.** `cases.services.next_action()` reads only `case.checklist` (`open_items`). The document
  requirements (the «pièces» of `documents.requirements`) are not an input.
  - This dossier has an empty checklist and one piece «À remplacer».
  - So the dashboard shows the fallback «Compléter le questionnaire d'orientation», while `/mes-documents/` shows
    «Remplacer la pièce» as its primary.
  - The person has two «next actions».
- **Two lists of «what is asked».** For the same reference `EE167596D4`, with the same word «pièce»:
  - `cases/detail.html` «Ce qui est demandé» renders `case.checklist` and says «Aucune pièce n'est encore
    demandée…»;
  - `/mes-documents/` renders the requirements and says «3 pièces demandées».

  On a legal-trust platform this is a P0 defect.
- **The primary CTA leaves the console.** «Continuer» → `orientation:start` → `templates/orientation/start.html`,
  which does `{% extends "base.html" %}`. The rail, the context bar and the bottom bar vanish, and the person is back
  on the public site in the middle of their own case.
- **Two questionnaires, unexplained.** The rail says «Ma situation»: an 8-question profile form in the console
  (`PROFILE_FIELDS`). The next action says «questionnaire d'orientation»: a different, ruleset-driven wizard in the
  public shell. Nothing tells the person how the two relate.

→ **Moves:** §6 (the unified next-action model and orientation inside the console). These need a product and
engineering decision, not CSS.

### D4 · Empty-state doctrine → a dead first-run dashboard

For a new person, the most common visitor, the dashboard ends in four panels of one grey sentence each.

The doctrine comes from the `dashboard.html` comment: «An empty region is one hairline and one sentence … never a
dashed box with a centred icon, and never a zero». It was a reaction to the V2 dashboard's dashed boxes. It is right
about honesty and wrong about composition: **empty panels should not be drawn at the size of full ones.**

→ **Move:** collapse empties.
- A region with no data yields its space to regions that have data.
- It becomes one line in a «Rien pour l'instant» strip.
- The EmptyState component (DS #30) is kept for **whole-page** empties («no case yet»), where it carries the one
  action (§3.2).

### D5 · States do not read

- **Chips.** Brouillon, Transmis au projet, En cours d'examen and Pris en charge are the same grey pill at the same
  weight (`before_entreprise_1440_full.png`). The only difference is the style and length of a 3–4 px gutter, which
  is below the threshold of a glance.
- **The phase gauge.** `data-stage` (rule length = phase) draws a short tick at the top of the pill. Three of three
  observers would file it as a bug.
- **The HealthStrip.** It fills two-thirds in `--ink-2` for «Déposé» while the caption says «0 sur 3 validées».
  Proportional width encodes how many pieces sit in each state, but a filled bar is universally read as progress.
  The metaphor defeats the legal law it was built to serve.
- **«1 en attente».** It is drawn in `--pending-700` and counts the piece **the person** must replace, yet «en
  attente» reads as «waiting for someone else». The counts wording is locked copy (flagged, §9).

→ **Move:** Chip V5 and the Piece Ledger (§5).

### D6 · Collections that do not align

- **Per-row grids.** `.doc-row { grid-template-columns: 4fr 1.5fr 2fr 1.5fr 1fr auto 40px }` is computed per row.
  The `auto` action column differs between «Consulter» and «Remplacer la pièce», so every `fr` track shifts. In the
  capture, the state column starts at x≈625 on rows 1–2 and at x≈651 on row 3.
- **No column headers.** The «—» in the due column is an unexplained dash floating mid-row. On the compact dashboard
  rows it sits alone at the far end.
- **Repeated buttons.** «Ouvrir le besoin» appears four times and «Remplacer la pièce» twice. That is visual noise,
  where the row itself should be the target.

→ **Move:** CSS subgrid collections with one header row (§3.3).

### D7 · No continuity, no feedback

- **Navigation.** On slow 4G + CPU ×4 the old page holds, then the new one paints in pieces. At fp+250 ms the
  workspace is empty and the rail has no glyphs: `svg_icon` points `<use>` at the external `static/img/icons.svg`,
  which is fetched after the CSS. There is no thread and no cue.
- **Layout.** `html` has no `scrollbar-gutter`. When content grows past the viewport, the scrollbar takes 15 px and
  the context bar's end items shift (fp+0250 vs fp+1200). This is a small horizontal CLS contribution on every
  console page.
- **Actions.** Every POST is followed by a redirect and a full page.
  - No toast.
  - No «this row changed» cue.
  - No «ce qui a changé» after «Enregistrer et recalculer». That button re-runs the orientation engine on the
    person's facts: it is the most consequential click in the product, and it looks like a save.

→ **Move:** adopt `MOTION.md` §6 (the thread «la soglia», L2 busy key, L3 region skeleton) and §5.9 (the cause bar
on the changed row). Add toasts, an outcome diff and `scrollbar-gutter: stable` (§3.12).

### D8 · An anonymous shell

- **Identity.** The rail is navy SaaS with a mesh at 55 %. The brand is a 40 px tile and a serif wordmark. Nothing in
  the console says «Italy ↔ Morocco, a regular path through a door».
- **Anonymity.** The account menu shows `get_short_name` («Personne», or the handle «qa-company») and four links. It
  has no identity header, no role, no organisation and no space switcher (person / company / staff).
- **Default rail state.** The rail is collapsed below 90rem (1440 px), so on 1280–1439 px laptops the platform is
  icon-only. Several of those icons are double-booked (`ICON_SEMANTIC_MAP.md` §2: `list` = «Mes demandes»,
  `handshake` = «Guichet»).

→ **Move:** a labelled rail, the travelling indicator, an identity header in the account menu, and the journey rail
as the console's signature object (§3.1, §3.2).

---

## 3. Surface by surface

Each surface follows the same format: **Critique** (severe, sourced) · **What a top 2026 platform does** · **Concrete
moves** (numbered, with owner files) · **Component families** · **Priority**.

Where the move is a pattern already curated by the 21st.dev curators, the candidate id is cited from their document
(`#nnnnn`, with the source doc in brackets). This panel made **no new 21st.dev calls** (§11).

### 3.1 App shell — rail, context bar, bottom bar, drawer, account menu, footer

**Critique**

- **Icon-only by default on laptops.** At 1280–1439 px the rail is 64 px wide and every entry is a glyph behind a
  400 ms tooltip (`console.css` L216–231: labels at opacity 0 below 90rem). This is a platform used occasionally, in
  four languages, by people under legal stress. Linear's icon-only rail works for daily power users; here it is
  cognitive load.
- **The indicator does not travel.** The active entry is a static lighter plate plus a 3 px bar. DS §3.9 specified a
  travelling indicator with `SPRING_SNAPPY`, and `console.js` explains it was dropped because «a page is a full
  navigation». `MOTION.md` §5.6 has since given the right answer: move on click and stay until `pagehide`.
- **Groups carry little.** «ACADEMY» is a group title over a single entry named «Academy», and «PARCOURS» over three.
  Titles are uppercase eyebrows at `--on-dark-3`, which reads as a SaaS template.
- **The context bar holds only a breadcrumb and utilities.** V4 §3.9 promised, at the end of the bar, a search field
  for persons, a CommandMenu for staff and a bell with a real badge. None exists.
- **The account menu is anonymous** (`before_dashboard-accountmenu_1440.png`).
  - It has no identity header (name, e-mail, account type, organisation) and no space switcher: a person who is also
    a company referent cannot see which space they are in.
  - The summary shows `user.get_short_name`, which for the QA company is the handle «qa-company».
- **Bottom bar labels wrap on purpose** (`hyphens: auto`, «Communica-tions», «Tableau de / bord»). It is
  deliberate and still reads cramped. A 2026 bottom bar uses short labels, and the nav model has no short label
  today.
- **Drawer:** good. It is the best mobile surface (native `<dialog>`, focus to the current entry, language, «Site
  public»).
- **Footer:** «Privacy Policy» is English on every locale. This is the documented residual G-08
  (`docs/ACCESSIBILITY.md`), but the console footer (`base_portal.html`) does not carry the `lang="en"` that G-08
  prescribes: WCAG 3.1.2.

**What a top 2026 platform does**

- A **labelled rail**: icon plus a short label always visible (the Material 3 / Arc pattern), or open by default
  wherever width allows.
- One **quiet indicator** that moves where you go.
- A **context bar** that carries the page's identity when scrolled, a global «go to», and a notification centre with
  real counts.
- An **account menu** that starts with who you are and which space you are in.
- **Continuity** between pages: the chrome never flickers, and a thread shows that something is coming.

**Concrete moves**

1. **Open the rail by default from 80rem (1280 px), not 90rem.** Below 80rem, use a **labelled compact rail** (72–80 px,
   glyph plus an 11/14 label under it, two lines max, `short_label`) instead of glyph-only. The persisted choice still
   wins. File: `console.css` L18–22, L216–231. Needs `portal.services.navigation` to supply `short_label`, and a copy
   review (§9).
2. **Travelling indicator** (`MOTION.md` §5.6): one `rail__indicator` element translated by `SPRING_SNAPPY` to the
   clicked item, staying until `pagehide`. The static `aria-current` style remains the no-JS truth. Route B (Motion is
   already a dependency). File: `console.js` §1.
3. **Group titles** keep only real semantics: *Parcours* · *Dossier* · *Échanges*. The single-item «Academy» group
   becomes a plain entry after a separator. Titles move to sentence case 12/16 500 at `--on-dark-2`, closer to Linear
   than to the uppercase SaaS eyebrow (copy review §92 is already pending).
4. **Context bar, end zone** (V4 §3.9, finally built):
   - **(a) bell** with a real unread count as Badge (DS #4) → notification panel (§3.10);
   - **(b) «Aller à…»** IconButton + `Ctrl/⌘ K` for everyone, limited to the account's own destinations (§3.11);
   - **(c) account menu** with an identity header;
   - **(d) language** stays segmented.

   Scrolled: the page title and state chip condense into the bar (`#23562` in [nav-shell]; CSS scroll-driven where
   supported, the existing IntersectionObserver elsewhere).
5. **Account menu V5** (`#393` anatomy in [nav-shell]):
   - header: initials Glyph 32, full name (`dir="auto"`), e-mail, **account type + organisation**;
   - if the account holds several roles, a «Changer d'espace» group (Personne · Entreprise · Staff): links, not a
     toggle;
   - then Profil · Sécurité · Préférences de notification (the `NotificationPreference` model exists), a separator,
     and «Se déconnecter».
   - No avatar photos.
6. **Bottom bar:** short labels (`Accueil · Dossier · Pièces · Messages · Menu`, subject to copy review), one line,
   `hyphens` removed. The badge on «Messages» and «Pièces» uses real counts only.
7. **Footer:** add `lang="en"` on «Privacy Policy» in `base_portal.html` (G-08 residual). One attribute.
8. **Identity moment (the one place the brand speaks in the console):**
   - the rail tile gets the **golden key** at rest, gold only on navy (`#c39a2b` = 5.80:1 per [nav-shell]); this is a
     brand-asset question for the owner;
   - the navigation thread «la soglia» plus the lock sweep on the tile during page loads (`MOTION.md` §6.3 S).

   That is enough identity. No arch in the workspace, which respects V4 pillar 2 («niente porta nel cruscotto»).
9. **`scrollbar-gutter: stable`** on `html.console` / `body.console` removes the ~15 px shift of the context bar when
   the scrollbar appears (D7). Measure CLS before and after.
10. **Shell icons render with the first paint.** Either inline the ~12 rail and bar symbols as an in-document
    `<svg><symbol>` block rendered by the server (markup, not script or style, so CSP-safe; roughly 2 KB gz), or
    `<link rel="preload">` the sprite. Preload does not reliably feed an external `<use>` reference in every engine,
    so **measure**. Today the rail paints without glyphs (fp+250).

**Component families:** NavigationRail (labelled / compact / drawer), RailIndicator, ContextBar (+ condensed title),
Bell + NotificationPanel, AccountMenu V5, BottomBar, Thread «la soglia», Footer.
**Priority:** moves 1, 7, 9 and 10 → P0 (cheap; they fix comprehension and CLS). Moves 2–6 → P1. Move 8 → P1,
behind an owner decision.

### 3.2 Person dashboard

**Critique**

- **The next action has no button of its own.** The primary sits in the ContextHeader (a V4 decision: «The action is
  the context header's (CD §3.4.1): one PRIMARY per screen»).
  - Desktop: the label is about 900 px from its button.
  - Phone (`before_dashboard_390.png`): «Continuer» sits above the card that explains it, and the card is not
    clickable.
  - The one-primary rule is right; its placement breaks proximity.
- **«Responsable» means two things on one screen.** In the next action it is the step owner («La personne»); in the
  Dossier panel it is the case's assigned professional («Professionnel»).
- **The Dossier panel repeats the header** (state chip, then objective / responsible). The five-notch meter only
  appears when checklist data exists, so on a first run the panel is three facts in a 460 px box.
- **The JourneyRail is the right object, drawn thin.** It shows seven labels and a ring, «Vous êtes ici», and a
  MAROC/ITALIE eyebrow. It does not say what the current step means, what it needs, or who else acts. The `detail`
  field in its contract is not rendered in the horizontal variant.
- **«Mes documents» mixes two ideas.** The pieces (requirements) and the «Derniers dépôts» (files) sit in one panel.
  The files end in «non analysé», raw scan-status jargon beside a file name.
- **Four empty panels** (D4): échéances, communications, academy, and «Mon compte», which duplicates the account menu
  and says «· Entreprise» on a person dashboard. The QA fixture carries `account_type=company` plus the PERSON role
  (`portal.services` L1297/L1302); verify with a clean person before judging.
- **Hierarchy:** every panel is the same L1 white card with the same 17/24 title. The eye has nowhere to land after
  the next action.

**What a top 2026 platform does**

A «home» of this kind (Mercury, Stripe Atlas, Deel onboarding, GOV.UK «your application») answers three questions
in this order:
1. **Now** — one task, the button inside it, and why it matters.
2. **Where I am** — the path, with the current stage expanded.
3. **What happened** — a short activity feed, never empty after creation because the system's own events count.

Everything else is a shortcut. Empty modules disappear instead of apologising.

**Concrete moves**

1. **«Maintenant» panel (L2, 8 columns).** It holds eyebrow, title (the action) and detail, plus the **primary
   button inside the panel**, plus the ResponsibilityBar and due date. It is still the one PRIMARY on the screen. The
   ContextHeader keeps identity (greeting, reference, chip, «depuis le») and a quiet «Voir le dossier» link. Applies
   to dashboard, case and company.
   - This reverses the placement, not the rule. Owner/ECD decision §9.
   - On the phone, the panel is the first thing under the header, and its button is full width.
2. **Rename the case-level «Responsable»** to «Intervenant» (or «Suivi par»). Copy review; the word already exists in
   «Qui intervient sur ce dossier».
3. **JourneyRail «la soglia» as the dashboard signature** (`#24528` + `#28384` in [platform-domains]; the
   frontier-as-arch idea there is subject to the V4 «no door in the dashboard» rule, owner decision §9).
   - Draw the travelled segment once (`MOTION.md` §7.4, already prototyped).
   - Under the current node, a **«Cette étape»** disclosure shows the step's `detail`, the actor and what it waits
     on. Real data only; if absent, nothing.
   - Keep the vertical rail for the phone.
4. **One «À faire» list replaces «Mes documents» + «Mes échéances»** when either has data.
   - Content: the pieces the person must act on and the dated deadlines, merged and sorted by urgency (overdue →
     soon → dated → open).
   - Each row carries its action button (subgrid row, §3.3).
   - Pieces awaiting a third party go into a quiet «En attente d'un tiers (n)» line. No zeros.
5. **One «Activité» feed replaces the empty «Communications», the «Derniers dépôts» list and the dead space.**
   - Data: the case timeline the case page already reads from the audit trail (`cases/views.py` L142) — Dossier
     ouvert, Intervenant assigné, dépôts, messages.
   - Grouped by day with absolute dates (`#28340` in [platform-domains]).
   - Never empty once a case exists, and every event is real.
   - Scan status becomes words: «Analyse en cours» / «Fichier vérifié», per the chip registry.
6. **«Raccourcis» row** (at most 4, `#28284` in [platform-domains]): Déposer une pièce · Écrire au Guichet · Mettre à
   jour ma situation · Academy. Each is a whole-row link with a verb.
7. **«Mon compte» leaves the dashboard.** It is already the account menu (§3.1 move 5); «Dernière connexion» moves
   into the account menu header as a security cue.
8. **No-case state:** the full EmptyState (DS #30, the V5 skin in §4). It carries the orientation image, the one
   exception `IMAGERY.md` §3.19 proposes, and the one action «Commencer», which stays in the console (§6).
9. **Panel hierarchy.**
   - L2 «Maintenant» is the only raised panel.
   - «À faire» is an L1 sheet.
   - «Activité» is flat (L0 on the canvas, hairline spine).
   - Raising only what matters is how Linear and Mercury read as expensive without decoration.

**Component families:** ContextHeader, NowPanel (next action + CTA + ResponsibilityBar), JourneyRail (3 densities),
TaskList (subgrid rows), ActivityFeed (Timeline by day), Shortcuts, EmptyState V5.
**Priority:** moves 1, 2, 4 and 5 → P0 (comprehension); 3 → P1 (signature); 6, 7, 9 → P1; 8 → P1.

### 3.3 Document workspace — «Mes pièces», piece detail, upload, preview

**Critique**

- **Alignment** (D6): each row has its own tracks, so the columns drift and there are no headers.
- **Chips all look alike:** grey pill + gutter; «À remplacer» barely differs from «Déposé».
- **The HealthStrip reads as progress** (D5).
- **The ≡ row menu uses the hamburger glyph**, which reads as navigation. The menu also duplicates «Consulter»
  (`#28828` discipline in [forms-docs]; `ICON_SEMANTIC_MAP.md` → `ellipsis-vertical`).
- **Filters.** The pill row lists all seven states with counts, most at 0 («Manquant 0 · En examen 0 · Valide 0 ·
  Non valide 0 · Expiré 0»). Five of eight options select nothing. On the phone, the row scrolls sideways with a
  partial label («En exam»).
- **Upload, the platform's central act, is its least designed screen.**
  - «Remplacer la pièce» navigates to `requirement_detail.html`, a **V2 folio page**.
  - The form there is a bare file input with «Déposer». There is no dropzone, no progress, no client-side type or size
    check mirroring the server's, and no preview of what you chose.
  - The antivirus fact («non analysé») and the review fact arrive later as V2 text.
- **No preview.** «Consulter» is a full navigation to a V2 page (DS #19 drawer not built).
- **Title mismatch:** «Mes pièces» versus the rail and the breadcrumb «Mes documents». The page title is locked; the
  rail label is not.

**What a top 2026 platform does**

Document workspaces (Deel, Rippling, Carta, Stripe Identity, GOV.UK «upload your evidence») share six traits:
- the collection is **grouped by who must act**, not by an enum;
- a row is one line of truth: what, status (word + glyph), due, one action;
- preview happens **in place**, in a side sheet;
- upload is **drag, check, progress, confirm** without leaving the list;
- the verdict of the system (scanned) and of the human (reviewed) are shown as two separate facts;
- a filter never offers an empty result.

**Concrete moves**

1. **Group by responsibility** (`#28857` + `#29345` in [forms-docs] C17):
   - «À vous de fournir (n)» — open by default;
   - «En attente d'un tiers (n)»;
   - «Déposées, en attente d'examen (n)»;
   - «Examinées (n)».

   Each group header shows glyph, title and count (tabular). Empty groups are not drawn. This replaces most of the
   need for filters.
2. **Filters show only non-zero states.**
   - «Tous» plus the states with a count > 0; the others fold into «Autres états» (a `<details>` popover).
   - Sliding thumb `#23552` (route B), as V4 §8.14 specified.
   - State stays in `?état=`.
   - On the phone, the segmented control wraps. It never scrolls sideways with clipped labels.
3. **Subgrid collection.**
   - `.doc-collection { display: grid; grid-template-columns: minmax(0,4fr) minmax(0,1.5fr) minmax(0,2fr)
     minmax(9ch,1.5fr) minmax(0,1fr) max-content 40px }`.
   - `.doc-row { grid-column: 1 / -1; display: grid; grid-template-columns: subgrid }`.
   - Every row then shares the widest action and the columns align. Subgrid is Baseline 2023. Fallback: a fixed
     `18ch` action column.
   - Add **one header row** (`aria-hidden="true"`, 12/16 600 `--ink-3`: Pièce · État · Responsable · Échéance) and a
     visually-hidden prefix on each zone for assistive technology («État : », «Échéance : »). This keeps list
     semantics, which V4 chose over a `<table>` for the person's collection.
   - The «—» becomes the words «Sans échéance» in `--ink-3` on the register. On compact rows the zone is omitted.
4. **The whole row is the target of «Consulter».**
   - Its title becomes a link spanning the row (`::after` stretched link; the button and menu stay above it with
     `position: relative; z-index`).
   - The explicit button remains only for **the person's act** (Déposer / Remplacer, PRIMARY-small with gradient) and
     for the Terms gate.
   - The menu keeps only what is not on the row: Télécharger, Historique des dépôts.
5. **Preview drawer** (DS #19; `#23558` behaviours in [nav-shell]; C12 in [forms-docs]).
   - A native `<dialog>` at the inline end, 420 px (full-screen sheet ≤ 640 px).
   - Content: the piece page's `<article>` fetched as a fragment (`connect-src 'self'`).
   - Loading: `MOTION.md` §6.7 B (L3 skeleton + door 24).
   - Footer: the person's primary action, which opens the Dépôt inside the drawer.
   - The URL updates with `history.pushState` to the piece URL, so a reload or a shared link lands on the full page.
6. **«Dépôt» — the upload flagship** (C9 in [forms-docs]: `#25108` baseline, `#17767` dropzone idea, `#27137`
   behaviour, `#28271` lifecycle; `MOTION.md` §5.9).
   - A no-JS native input is the baseline; the dropzone keeps the real input inside it.
   - Client guards mirror the server (PDF / JPEG / PNG, 10 Mo).
   - A real `<progress>` via XHR upload events, showing bytes and an estimate.
   - Row lifecycle: «En file» · «Envoi — 1,4 Mo sur 3,2 Mo» · «Vérification du fichier» · «Déposée — version n»
     (neutral) · «Refusée : raison» / «Envoi interrompu» + Réessayer.
   - **The review verdict never appears here:** filed ≠ examined.
   - Success: a tick drawn in 320 ms, a toast «Pièce déposée — version 2», and the row's cause bar (`MOTION.md` §5.9).
   - Security note for engineering: the XHR must use the same CSRF and multipart endpoint, with no new route unless
     reviewed. Throttling (`UPLOAD_THROTTLE`) must surface as a human message, not a 429 page.
7. **The Piece Ledger replaces the proportional HealthStrip** (§5.3). For n ≤ 24, show one pip per piece, in group
   order, each carrying its register glyph shape. The caption stays the locked sentence, with «validées» visually
   first.
8. **Title coherence:** the rail entry becomes «Mes pièces» (the page title is locked; the nav label is not), or the
   breadcrumb explains «Mes documents › Pièces du dossier». Copy review.
9. **Personal files** (`documents/upload.html`, «a file that answers NO requirement») stay a secondary path, listed
   under the groups as «Mes fichiers personnels». The same Dépôt component, and never promoted.

**Component families:** DocumentCollection (subgrid), DocumentRow V5, GroupHeader, SegmentedControl (thumb), Search,
PreviewDrawer, Dépôt (dropzone + file rows + progress), PieceLedger, Chip V5, Toast, RowMenu (Popover).
**Priority:** moves 3, 4 and 7 → P0 (legibility and truth); 1, 2, 5, 6 → P1 (6 is the single most visible «premium»
move on the platform); 8, 9 → P2.

### 3.4 Case / fascicolo

**Critique**

- **Truth conflict** (D3): «Ce qui est demandé: aucune pièce» while `/mes-documents/` lists three for this case.
- **Two «où en est…» panels.** «Où en est ce dossier» (the journey, main column) and «Où en est votre demande» (the
  timeline, inspector) answer the same question in two vocabularies.
- **The order buries the action.** Journey (7 rows) → next action → what is asked → who → state form. The next
  action is at y≈660 on desktop; on the phone it is after the full vertical journey.
- **Repetition:** the next action, communications and échéances repeat the dashboard, with the same empty sentences.
- **«Faire évoluer l'état du dossier» is an admin form** (`<select>` «Nouvel état» + a free-text reason +
  «Enregistrer l'état»).
  - The template comment labels it Staff; it rendered for `qa-doc-person` because `transitions_available()` returned
    entries. Verify whether the person may transition, e.g. to submit or withdraw.
  - If the person may, a `<select>` of states is the wrong UI. If not, it is a permission bug. Either way, flag it.
- **No section navigation** on a long page. There is a sticky compact bar (good), but no local index.

**What a top 2026 platform does**

A case file in 2026 (Clio, Ironclad, the Legalesign / DocuSign agreement view, GOV.UK case pages) is a **workspace
with an inspector**.
- Main column: what is asked, and the one action.
- Inspector: facts, timeline and people.
- State changes are **intent buttons** («Soumettre mon dossier», «Retirer ma demande») with a confirmation dialog
  that states the consequence, never a state-machine dropdown.
- A **context index** lets you jump between sections, and the header condenses on scroll.

**Concrete moves**

1. **Order: Maintenant → Ce qui est demandé → Parcours → Qui intervient.**
   - The next-action panel is first, with its CTA (§3.2 move 1).
   - «Ce qui est demandé» is **one list**: the case checklist items **and** the document requirements, grouped as in
     §3.3 with the Piece Ledger. This needs the model decision in §6.
   - The journey comes after, as a compact rail with the current step expanded.
2. **Merge the two «où en est».** The main column keeps «Parcours» (the 7 steps, the where). The inspector becomes
   «Suivi» (the timeline of events, the what happened), with the last node lit once (`MOTION.md`). The titles stop
   echoing each other.
3. **Context index** (≥ 80rem):
   - a slim sticky list in the inspector's head: Maintenant · Pièces · Parcours · Intervenants · Suivi · Messages;
   - `aria-current="location"`; the marker glides (`#29954` tree rail + `#21517` ticks in [nav-shell], route B);
   - on the phone, `<details>` or anchors under the compact bar.
4. **State transitions as intent buttons.**
   - Each permitted transition from `transitions_available()` renders as its own button with a verb label
     (engineering supplies labels per transition).
   - Suspension-type transitions open a `<dialog>` with the required reason (textarea with a counter, `#29430` in
     [forms-docs]) and the consequence sentence.
   - Staff-only transitions live in a staff drawer, not in the person's page.
   - Destructive transitions use the DESTRUCTIVE button (DS #1).
5. **Remove repetition.** Communications and échéances appear on the case only when they have case data. Otherwise
   one line in the inspector.
6. **Sticky compact bar** (built): add the Piece Ledger micro-version (pips) and the one primary. Keep it `aria-hidden`
   as today; the header is the accessible source.

**Component families:** ContextHeader + CompactCtxBar, NowPanel, RequirementList (unified, grouped), PieceLedger,
JourneyRail (compact), Inspector (Timeline «Suivi», facts, intervenants with Glyph), ContextIndex, TransitionActions
+ ConfirmDialog.
**Priority:** move 1 (with §6) → P0; 4 → P0 if the person does see the form, P1 otherwise; 2, 3 → P1; 5, 6 → P2.

### 3.5 «Ma situation» and Form UX

**Critique**

- **The counter contradicts the stepper.**
  - The stepper and the panels show **8** questions («1 / 8» in the foot).
  - The counter says «0 question(s) renseignée(s) sur **7**» (`total = len(PROFILE_FIELDS)` = 7; the 8th, «titre
    reconnu», is shown but «the rules do not read [it] yet», per the view comment).
  - It is honest in code and confusing on screen.
- **The date of birth renders `mm/dd/yyyy` on a French page.** Native `<input type="date">` formats by browser UI
  locale, not page `lang`. For a FR/IT/AR audience on phones this is a known failure pattern; GOV.UK abandoned native
  date inputs for exactly this reason.
- **Two submit semantics on step 1.** «Continuer» (primary) sits beside «Enregistrer et recalculer» (secondary), so
  the person does not know whether «Continuer» saves.
- **No review step** before recalculation, and **no outcome** after it (D7).
- **Layout.** The question card floats with about 300 px of dead canvas at its inline end, and the explanatory notes
  (the recalculation notice, the counter's caveat) are 13 px grey paragraphs the eye skips.
- **Good and to keep:** «Ce que nous ne demandons pas», the per-question «why», OptionCards, the sticky foot, the
  no-JS fallback, and the refusal of a «profile strength» meter.

**What a top 2026 platform does**

One question at a time with visible reasons and an explicit review («Vérifiez vos réponses»). Dates as day / month /
year fields. Autosave (or a clearly separated save), and after submission a **result delta**: «Votre orientation a
changé : 1 parcours possible → 2».

**Concrete moves**

1. **Counter coherence.**
   - Either count over 8 and mark question 8 in the stepper with the qualifier «non utilisée par les règles pour
     l'instant» (an `--ink-3` badge),
   - or keep 7 and show the 8th after the others as «Question complémentaire».

   Words: copy review. Code: the view supplies `answered` and `total` consistently.
2. **DateField:** three labelled inputs (Jour · Mois · Année, `inputmode="numeric"`, `autocomplete="bday-day|month|year"`)
   in the page's reading order, each field's value in LTR digits (also in AR). Server-side validation into one
   `date`, with one error summary entry. This is a standard Django `MultiWidget`.
3. **Foot logic.**
   - Questions 1–7: «Précédent» (SECONDARY) · «Continuer» (PRIMARY); «Enregistrer maintenant» becomes a LINK-level
     action in the foot's start zone.
   - Last question: «Vérifier mes réponses» → a **review panel** (definition list with «Modifier» links per answer)
     → «Enregistrer et recalculer» (PRIMARY, busy key L2 while the engine runs).
4. **Outcome diff after save.**
   - The page returns with a notice listing, in words, what the recalculation changed: pathways added or removed,
     requirements added, or «aucun changement».
   - The content comes from comparing the previous and new assessment (the history is kept: «Les résultats
     précédents sont conservés»).
   - This is the single most reassuring feedback the platform can give. It needs an engineering presenter; no
     invented data.
5. **Notes promoted to UI.**
   - The recalculation notice becomes an L0 Notice with an `info` glyph (15/24) above the stage.
   - The counter caveat stays small under the stepper.
6. **Composition.** On ≥ 80rem, the stage uses 7 columns and the inline-end 3 columns hold «Pourquoi cette question»
   (the field's help moves there, larger), so the empty canvas becomes explanation.
7. **Form kit across the platform** (C1–C16 in [forms-docs]):
   - Input state model `#28301` (hint / invalid / warning; valid only when the server confirms);
   - native Select styled `#31494`;
   - Textarea with counter `#29430` + `field-sizing: content`;
   - Consent rows `#24975` / `#661`;
   - ErrorSummary `#29338`, focused on load, with «Erreur : » prefixed to `<title>`;
   - submit pending = L2 key (`MOTION.md` §6.7 C, label stays visible, `aria-disabled`).

**Component families:** Wizard (Stepper, stage, foot), OptionCard, DateField, ReviewPanel, OutcomeDiff notice,
ErrorSummary, Field / Select / Textarea, BusyButton.
**Priority:** moves 1 and 2 → P0 (trust + correctness); 3, 4 → P1; 5, 6, 7 → P1/P2.

### 3.6 Company / B2B workspace

Constraint that shapes everything here: **CR-03 / CR-04** — no list of persons, no candidate cards, no people search,
no count of matching people. The B2B workspace turns around **needs**, never people. V5 must not import the
«talent pipeline» aesthetics of 21st.dev B2B dashboards.

**Critique**

- **All states look the same:** four identical grey chips (D5).
- **Buttons repeat:** four identical «Ouvrir le besoin» buttons; the row should be the target.
- **The CTA contradicts the next action.** The next action says «Transmettez le besoin «…» au projet»; the header
  button says «Ouvrir le besoin» (`companies/services.py` L506/L510). The person clicks «Ouvrir» to do «Transmettre».
- **The «Vérifiée» chip wears `chip--seal`** (cut corner, double rule, bronze): the template adds `chip--seal` when
  `is_verified`.
  - CD V4 §3.8 says the opposite: «Vérifiée (registro conforme — un fatto, non un sigillo d'autorità)».
  - The seal register means «issued by an authority»; the project team is not an authority.
  - A legal-semantics question for the owner (§9); the visual consequence is a misleading gold tag.
- **The account label is the handle** («qa-company»), not the referent's name and the company.
- **«Mon entreprise» panel:** the legal sentence about verification runs as body text inside the facts. It is a
  caveat and should read as one.
- **Good:** a real `<table>` with caption, scope, sticky head and cards below 64rem. The best table in the product.

**What a top 2026 platform does**

For a B2B client of a regulated intermediary (Deel for employers, Remote, Stripe Connect onboarding):
- **the lifecycle of each request is visible at a glance**: stage columns or a stage meter per row;
- the next step names the verb it will perform;
- verification is shown as a checked fact with its date and scope, not as a medal.

**Concrete moves**

1. **Needs overview strip** above the table: four counts by state (Brouillon · Transmis au projet · En cours
   d'examen · Pris en charge), each a filter link with its Chip V5 glyph. These are counts of **needs**, the only
   numbers allowed (`#22187` footer idea in [platform-domains]).
2. **Row = target.**
   - The need title becomes a stretched link.
   - The trailing column shows the **next verb only when the company must act** («Compléter», «Transmettre») as
     PRIMARY-small; otherwise a chevron.
   - Removes four identical buttons.
3. **CTA label = the verb.**
   - The header CTA says what the destination completes: «Relire et transmettre» for the transmit case.
   - Transmission itself stays on the need page, behind a confirm dialog that restates what is shared and with
     whom (the legal sentence).
   - Copy + `services.py` label change.
4. **Chip V5 per state** (§5): Brouillon = nullo-ish outline; Transmis = neutro + `send`; En cours d'examen = attesa
   + `glasses` (per `ICON_SEMANTIC_MAP.md`); Pris en charge = neutro + actor Glyph. Distinguishable at a glance, no
   verdict colour.
5. **Verification.**
   - «Vérifiée» becomes the **conforme** register chip with a `badge-check` glyph and a date («Vérifiée le
     12.09.2026»).
   - No seal cut, unless the owner rules that the project's verification is an act of authority (it should not be).
6. **Account identity:** the summary shows the referent's name plus the company short name; the handle never shows.
7. **Need detail** (`companies/need_detail.html`, V2) migrates to the case-file composition: header with state and
   one action, main column (the need's facts and profiles as the company declared them), inspector (Suivi timeline,
   the authorised actor with Glyph).

**Component families:** ContextHeader (company), StateOverview (counts as filters), Table V5 (stretched-link rows,
sticky head, cards < 64rem), Chip V5, ConfirmDialog, Inspector.
**Priority:** 3 and 5 → P0 (truth / legal semantics); 1, 2, 4 → P1; 6 → P1; 7 → P2.

### 3.7 Academy

**Critique**

- **A V2 island.** Newsreader serif titles, a «01 CATALOGUE» folio, numbered register rows with underlined serif
  links, `academy.css` («never a pill … never a card … radius ≤ 2px»).
  - The only console page with typographic character, and the only one that contradicts V4 pillar 3 («serif … mai»
    on the platform).
  - The user moves from Plex console to serif catalogue within the same shell.
- **The domain filter is words on a hairline**, wrapping to two lines at 1440.
- **Indentation differs** from every other console page: an extra left padding on the header block.
- **The rail's «Mes formations» sub-entry** appears without a glyph when on Academy: an ad-hoc second level.
- **The course meta line** «… · enseigné en Italiano» mixes languages. If the endonym is deliberate, it needs
  `lang="it"` and a FR gloss.
- **No imagery, no progress.** Allowed progress is modules counted in words, per REQ-EDU-05.

**What a top 2026 platform does**

A learning catalogue (Coursera for Business, Maven, the gov.uk learning platform) shows:
- courses as **scannable tiles or rows with a cover**, format chips (durée · modalité · langue) and the provider;
- «Mon suivi» as **continue-where-you-left-off**, with a module counter;
- course detail as a lesson list with a state per lesson.

**Concrete moves**

1. **Migrate to the console language** (Plex, V5 kit).
   - Keep the **register idea** as the ECD's «Register-row V5»: mono ordinal, Plex 17/24 600 title, one-line gloss,
     format chips (Durée 10 h · À distance · 3 modules · Italien), provider with Glyph, trailing chevron.
   - This keeps the identity move (the numbered register) and loses the editorial break.
2. **Filters:** SegmentedControl (wrap) or a native `<select>` below 480, with counts.
3. **«Mon suivi» first when enrolled:** one row per enrolment (`#28524` anatomy minus avatars in
   [platform-domains]) — status word, «Prochain module», notched module meter (modules as notches, words beside,
   never %).
4. **Course covers:** an owner decision. `IMAGERY.md` §3.6 assigns one image to Formation/Academy at the section
   level. Per-course covers need a CMS field and editorial sourcing. Until then, a course tile uses its domain glyph
   in a 40 px disc, never a stock photo.
5. **Rail:** «Mes formations» becomes a real entry with a glyph inside the Academy group, or an in-page tab. No
   glyph-less sub-entries.
6. **The Academy caveat** (`.note`, CR-14 / REQ-EDU-05) stays on every route, restyled as the V5 Notice (info glyph),
   at the end, as today.

**Component families:** Register-row V5, Chip (format), SegmentedControl, EnrolmentRow + module meter, LessonList,
Notice.
**Priority:** P2 overall (it works). Move 1 is the most visible coherence gain after the documents.

### 3.8 Forum governance («Forum permanent»)

**Critique**

- `/fr/espace-reserve/forum-permanent/` renders `forum/governance/unavailable.html`, which **extends `base.html`**.
  The person, inside the console, suddenly sees the public utility bar, the mega-menu, a serif H1 and the four-column
  institutional footer.
  - The 503 comment says it answers «to everyone, including a signed-in member»; it also covers the case where the
    reserved area's kill switch is off.
  - The shell jump is the defect, not the message.
- The module's live templates (commissions, tables, proposals, projects, participation, annual report) are **all V2
  register** (29 register instances in `commission_detail.html` alone). When the gate opens, it will open onto
  the oldest language in the product.

**What a top 2026 platform does**

Governance tools (Loomio, Decidim 0.28, GitHub Discussions) present **proposals in state lanes** with counts. Each
item shows its sponsors, its state as a word, and its timeline. Participation is shown as structured activity, not
as a feed.

**Concrete moves**

1. **Unavailable inside the console** when the portal itself is on: `unavailable.html` extends `portal/base_portal.html`
   if `portal_enabled`; `base.html` only when the reserved area is off.
   - The body becomes EmptyState V5, variant «en préparation»: glyph, the existing sentence, «Consulter la page
     publique du Forum» as SECONDARY.
2. **State lanes without drag** (`#29494` + `#1400` in [platform-domains]):
   - proposals in columns by `ProposalStatus` (Déposée · En examen · Décidées), with the count in each head;
   - entries are Register-row V5;
   - stacked sections with anchors below 64rem;
   - projects by `ProjectStatus`, milestones via the Timeline.
3. **The engagement caveat** (base_governance) as a persistent V5 Notice at the top of every module page. It is
   legal, keep it verbatim.

**Component families:** EmptyState V5 («en préparation»), StateLanes, Register-row V5, Timeline, Notice.
**Priority:** move 1 → P0 (a shell breach, with a one-line template condition); 2, 3 → P2 (the gate is closed).

### 3.9 Guichet numérique (helpdesk)

**Critique** (from templates; the post-fix appearance was not re-captured)

- It was rendered **unstyled** at capture time (the missing `console.css`), fixed by `c9a58d8` with a regression test
  (`tests/frontend/test_console_shell_stylesheets.py`).
  - **20 templates** override `block extra_head`. The fix pattern (`{{ block.super }}`) must be verified on each
    (`CAPTURES_AND_REFERENCES.md` §2 asked for it). Academy and companies already use `{{ block.super }}`, per their
    comments.
- Lists (`requests.html`, `queue.html`) are V2 register. The detail is V2 with a thread.
- There is no triage before the form, so every question becomes a ticket, even the ones the FAQ and glossary answer.
- The rail glyph is `handshake`, which is also used for the authorised actor. `ICON_SEMANTIC_MAP.md` proposes
  `concierge-bell`.

**What a top 2026 platform does**

Help centres (Intercom, Stripe support, GOV.UK «contact» flows) **deflect before they collect**: two or three
questions route to written answers, and «still need help?» opens a prefilled request. Threads show who answered, in
which role, and when. No SLA promise unless it is real.

**Concrete moves**

1. **Triage first** (`#26714` in [platform-domains]):
   - two choice questions (sujet · étape du parcours) → matching FAQ and glossary entries;
   - «Toujours besoin d'aide ?» opens the form carrying both answers.
2. **Request form:** topic as radio chips, textarea with counter, busy submit, and a confirmation page with the
   request reference and what happens next (`#24438`).
3. **Thread rows** (`#28568`): role label («Vous», «Professionnel mandaté», «Équipe du projet»), absolute date,
   «transmis / lu» only where the data exists.
4. **Requests list** grouped by date (`#29936`), each with a state Chip V5 and an unread dot bound to real data.
5. **Staff queue** (`queue.html`, `dispatch.html`): Table V5 with the C14 filter bar and C15 sortable headers (from
   [forms-docs]).

**Component families:** TriageStepper, OptionCard / radio chips, Textarea, BusyButton, ThreadRow, Table V5 +
FilterBar, Chip V5.
**Priority:** verification of the 20 `extra_head` overrides → P0 (one test); moves 1–4 → P1; move 5 → P2.

### 3.10 Notifications and communications

**Critique**

- **There is no notification surface.** `apps/notifications` holds a `Notification` model (a read state bound to its
  message, `read_at`), a `NotificationPreference` model, deadlines and an email outbox. The UI shows only
  «Communications», a V2 `portal-list`.
- Nothing in the chrome tells a person that something happened since the last visit.
- Mark-as-read is a separate POST (`communications/<uuid>/lu/`, `message_read`). This is good: reading via GET has no
  side effect, which also makes prefetch safe (§3.12).

**What a top 2026 platform does**

A **bell with a real unread count** opens a panel with tabs «Non lues · Toutes», items grouped by day, each item
linking to its object, «Tout marquer comme lu». A **preferences** page lists per-channel switches. A counter never
animates for fun and never says «99+» for a small product.

**Concrete moves**

1. **Bell + NotificationPanel** in the context bar (`#27135` doctrine + `#28432` tabs in [primitives]):
   - Popover (DS #16), L3, 360 px; bottom sheet ≤ 640 px.
   - Items: event glyph, one-line text, the object (dossier / pièce / besoin), absolute time.
   - Opening the panel **does not** mark anything as read. «Marquer comme lu» is a POST per item or for all.
   - Count on page load only (server-rendered badge). No polling in V5.
2. **Badge** (DS #4): 18 px, tabular, the width reserved in `ch` (the `.chip__n` rule already exists), real counts
   only, `aria-label` «3 notifications non lues».
3. **Communications page → Inbox V5:** list grouped by day, unread weight + dot (not colour alone), thread detail with
   ThreadRow; the mark-as-read POST stays.
4. **Preferences:** Switch rows (`#25090` + `#26523` in [forms-docs] C7) on `NotificationPreference`. The state word
   is always visible («Activé / Désactivé»).
5. **Toasts** (DS #20) for Django messages after POST-redirect-GET: bottom inline-end, 360 px, 6 s with pause on
   hover and focus, `role="status"`. **Legal outcomes stay in-page notices**, as DS #20 says.

**Component families:** Bell, Badge, NotificationPanel (Popover / Sheet), InboxList, ThreadRow, Switch rows, Toast.
**Priority:** moves 1, 2, 5 → P1; 3, 4 → P2.

### 3.11 Search and command

**Critique**

- The only search is the in-page title filter on «Mes pièces» (`console.js` §2). It is good: accent-folded, a live
  count after 400 ms, nothing sent.
- There is no way to jump to a dossier, a request or a message by reference. Staff have no command surface at all.

**Hard constraint.** CR-03 / CR-04 and `selection/workspace.html`: «there is nothing to search, because the workspace
holds mandates, not people … A list of people is the thing this product refuses to build.»
- The nav-shell curator's staff CommandMenu lists a «Personnes» result type (`21st_nav-shell.md` §3, `#27378`).
- **This panel objects:** no person search for authorised actors or companies, ever.
- For back-office staff, a person lookup exists only if the permission model already grants it (the Django admin
  does). Even then it should live in the back-office, not in the console palette. Owner / DPO decision (§9).

**Concrete moves**

1. **«Aller à…» for every account** (`#23522` behaviour in [platform-domains] «Quick actions» P2, `#27378` anatomy
   minus people):
   - a native `<dialog>` with a combobox;
   - sources: the account's own destinations (rail entries, own dossiers by reference, own pieces, own requests, own
     needs), served by a same-origin endpoint that reuses each view's queryset (out of scope → 404);
   - `Ctrl/⌘ K`, and `/` outside fields only, both listed in a «Raccourcis clavier» dialog and disable-able (WCAG
     2.1.4);
   - dynamic import on first use, under 4 KB.
2. **Staff CommandMenu:** the same component plus staff destinations (queues, dossiers by reference, requests).
   **No «Personnes» type** (see above).
3. **Register search pattern everywhere a list exceeds about 12 rows** (the helpdesk queue, needs, the forum):
   reuse `data-doc-search` generalised as `data-list-search`.

**Component families:** CommandDialog (combobox + listbox, ARIA 1.2), ListSearch, KeyboardShortcutsDialog.
**Priority:** P1 («Aller à…»), P2 (staff menu, shortcuts dialog).

### 3.12 Loading, pending, feedback — cross-cutting

**Critique:** D7. The platform is server-rendered, so its loading states are:
- **(a) navigation waits:** up to 3.8 s first paint uncompressed and 2.3 s gzip on slow 4G + CPU ×4;
- **(b) POST waits:** upload, recalculation, transition;
- **(c) the few in-page fetches V5 will add:** preview, «Aller à…», notifications.

None has a visual answer today. Also: the icons pop in (§3.1 move 10) and the scrollbar shift (§3.1 move 9).

**Concrete moves**

Align with `MOTION.md`, which already specifies and measured these.

1. **Navigation:** the thread «la soglia» plus the lock sweep on the rail tile (S level), from 400 ms after a
   same-origin click. **The console keeps the thread alone, without View Transitions**, as `MOTION.md` §5.5
   recommends after measuring +90 ms LCP. This panel agrees: a person working a case wants the next page, not a
   transition.
2. **Speculation Rules for the console** (not measured; this panel adds the exclusions `MOTION.md` does not list):
   - `moderate` eagerness `prefetch` (not prerender) on rail and bottom-bar links, delivered by the
     `Speculation-Rules` HTTP header pointing to a same-origin JSON (CSP `script-src 'self'` forbids inline rules).
   - **Exclude:** every `…/telecharger/` and signed download route. They are **audited** (`record(action="documents.downloaded")`)
     and **throttled** (120/h): a prefetch would forge audit entries and burn quota.
   - Also exclude logout, the back-office, every `?next=` and every POST-backed URL.
   - Portal views are `never_cache`; verify that Chrome uses the prefetched response for `no-store` documents before
     counting on any gain.
   - Optionally skip side effects on `Sec-Purpose: prefetch`.
   - Gate: measure LCP / INP with and without.
3. **POST waits:** busy key L2 in the submit button (`MOTION.md` §6.7 C, label kept, `aria-disabled`, ≥ 480 ms once
   shown); for upload, the real `<progress>` (§3.3 move 6).
4. **Region waits** (preview, palette, notifications): L3 skeleton at final dimensions (CLS 0), static for 1 s, then
   the single light; `aria-busy`; one announcement («Ouverture du document…») only if the wait exceeds 1 s; at 10 s,
   stop and say so (`MOTION.md` §6.6).
5. **Outcome feedback:** toasts (§3.10 move 5); the **cause bar** on the changed row (`MOTION.md` §5.9); the **outcome
   diff** after recalculation (§3.5 move 4); a chip word crossfade with one `aria-live` per register.
6. **First paint of the console:** inline shell symbols (§3.1 move 10); `scrollbar-gutter: stable`. Keep
   «arrive complete» (`MOTION.md` law 2.2): no entrance that hides painted content (gate E removed `ws-in` for exactly
   that reason).

**Component families:** Thread, BusyButton (L2 key), RegionSkeleton (L3), Toast, CauseBar, OutcomeDiff, Speculation
config (not a component).
**Priority:** 3, 5, 6 → P0/P1 (cheap, high perceived quality); 1 → P1; 2 → P2 (after measurement); 4 → with the
features that need it.

### 3.13 Accessibility (WCAG 2.2 AA, keyboard, reduced motion, RTL)

**Strengths to keep (verified in code)**
- native `<dialog>` for the drawer, with focus to the current entry and focus return;
- rail keyboard model (arrows, Home/End) on both rails;
- `aria-current` on nav and journey;
- HealthStrip bars `aria-hidden` with the words beside them;
- a live, debounced count on search;
- logical properties throughout, with physical sides only where RTL requires them (the rail tip);
- a non-chromatic state channel (rule style);
- reduced-motion branches (`withMotion`);
- labels kept accessible at `opacity: 0` in the collapsed rail;
- mark-as-read by POST.

**Gaps**

1. **2.4.11 Focus Not Obscured (Minimum).**
   - Top: `html { scroll-padding-block-start: var(--chrome-block-size) }` uses the **public** chrome size (96–104 px).
     With the console bar (56) plus the compact case bar (56) = 112 px, a focused control can land under the bars.
   - Bottom: there is **no `scroll-padding-block-end`** for the 56 px bottom bar, which also appears for desktop users
     zoomed to 400 % (reflow).
   - → Console tokens: `--console-chrome-top` (56, or 112 with `.has-ctx-bar`) and `--console-chrome-bottom`
     (56 + safe area), consumed by `scroll-padding` on `body.console`. Verify with keyboard at 320 CSS px.
2. **1.3.1 / 1.4.1 state perception.** Registers are distinguished by a 3–4 px rule style (solid / dashed / double /
   dotted) and length. It is compliant (the words carry meaning), but low-vision users cannot tell the register at a
   glance → the glyph per register (§5) is also an accessibility gain.
3. **3.3.x Dates.** The native date input follows the browser locale, not the page `lang` → DateField (§3.5 move 2).
4. **3.1.2 Language of parts.** «Privacy Policy» without `lang="en"` in the console footer (§3.1 move 7);
   «Italiano» in the Academy meta if deliberate (§3.7).
5. **Cognitive (2.4.6 and COGA guidance).** Icon-only navigation by default under 1440 px (§3.1 move 1); two
   «Responsable» meanings (§3.2 move 2); two «où en est» panels (§3.4 move 2); the 7 vs 8 counter (§3.5 move 1).
6. **HealthStrip segments** carry `title` tooltips: unreachable by keyboard and touch. If segments become filters (V4
   intent), they must be links; otherwise drop the `title`. The Piece Ledger (§5.3) removes the issue.
7. **Target size 2.5.8:** the row menu (40 px with a 44 px hit) passes. Recheck the Piece Ledger pips if they become
   interactive: they must not be.
8. **RTL:** not visually verified by this panel (no AR console capture exists).
   - Code review shows logical properties and flip classes (`icon--flip-rtl`), plus physical sides where deliberate.
   - V5 additions that need an RTL check:
     - the travelling indicator (inline end);
     - the preview drawer (from the inline end = left in AR);
     - the DateField order (Arabic reading order with LTR digits);
     - the Piece Ledger order (start to end);
     - toasts (bottom inline end = bottom-left in AR).
   - **An AR console capture pass is a gate requirement for V5**, not an afterthought.
9. **Reduced motion:** every V5 move above has a still state (`MOTION.md` §9). The thread under reduced motion is
   static at full width, 55 % opacity.

**Priority:** 1, 3, 4 → P0; 2, 5 → with the moves they belong to; 8 → gate requirement.

---

## 4. The V5 platform kit — component families

Routes:
- **A** — Django template + CSS + a small vanilla ES module;
- **B** — the same plus Motion (already a dependency, via `static/js/src/motion.js`);
- **C** — React island: **none proposed**;
- **D** — rejected.

The «Built?» column states the 27 Sept code state.

| Family | Members | Route | Pattern sources | Built? | Priority |
|---|---|---|---|---|---|
| **Shell** | NavigationRail (labelled / compact / drawer), RailIndicator, ContextBar (+ condensed title), BottomBar (short labels), AccountMenu V5, Footer | A (+B indicator) | V4 §3.9; `#29334` `#21517` `#14941` `#23562` `#393` [nav-shell] | partly (rail, bar, drawer, bottom bar) | P0 / P1 |
| **Headers** | ContextHeader (person / case / company), CompactCtxBar, WorkspaceHead, ContextIndex | A (+B index marker) | DS §8.33; `#29954` [nav-shell] | ctx + compact bar built; index no | P1 |
| **Status** | Chip V5 (word + glyph + register border + stage micro-meter), Badge (counter), Seal chip (authority only), UrgencyTag (due) | A | DS §8.3–5 re-expressed (§5); `#17207` [primitives] | no (V3 chip live) | **P0** |
| **Measures** | PieceLedger (pips), Meter (notches), module meter | A | §5.3; DS «misuratore» | meter yes; ledger no | **P0** |
| **Journey** | JourneyRail «la soglia» (dashboard / case / public densities), StepDetail disclosure, Timeline «Suivi» (by day), ActivityFeed | A (+draw once) | `#24528` `#28384` `#28295` `#28340` [platform-domains]; `MOTION.md` §7.4 | rail + timeline built (thin) | P1 |
| **Now** | NowPanel (next action + CTA + ResponsibilityBar + due), Shortcuts | A | `#8698` `#28284` [platform-domains] | panel built without CTA | **P0** |
| **Collections** | DocumentCollection (subgrid) + DocumentRow V5 + GroupHeader + DocumentCard, TaskList, Table V5 (sortable, stretched rows, cards < 64rem), StateLanes, Register-row V5, InboxList | A | `#28857` `#29345` `#28828` `#28496` `#22187` `#29494` `#19793` `#23561` [forms-docs, platform-domains] | doc-row + table built (unaligned) | P0 (alignment) / P1 |
| **Documents** | Dépôt (dropzone + file rows + progress + retry), PreviewDrawer, VersionsList | A (+B height spring) | C9 C12 [forms-docs] (`#25108` `#17767` `#27137` `#28271` `#23558`) | no | **P1 flagship** |
| **Forms** | Field (state model), Select, Textarea (+counter), DateField (3 parts), OptionCard, Wizard (stepper / stage / foot), ReviewPanel, ErrorSummary, Switch row, ConsentRow, TransitionActions + ConfirmDialog | A | C1–C16 [forms-docs] | partly (OptionCard, wizard, error summary V2 skin) | P0 (date, counter) / P1 |
| **Overlays** | Popover menu, Dialog, Drawer, Sheet (≤ 640), Tooltip | A (+B sheet spring) | DS §8.15–19; `#23548` [primitives] | popover + drawer-dialog built | P1 |
| **Feedback & loading** | Thread «la soglia», BusyButton (L2 key), RegionSkeleton (L3), Toast, CauseBar, OutcomeDiff notice, Notice V5 | A (WAAPI, no Motion) | `MOTION.md` §6; DS §8.20 | no | P0 / P1 |
| **Empty** | EmptyState V5 (vuoto · ricerca · pagina · accesso · rete · in preparazione), EmptyLine (inline) | A | DS §8.30; [primitives] empty-state family | component exists (V2 skin); doctrine conflict | P1 |
| **Notifications** | Bell, NotificationPanel, Preferences (switch rows) | A | `#27135` `#28432` [primitives]; `#25090` `#26523` [forms-docs] | no | P1 |
| **Command** | CommandDialog «Aller à…» (all accounts), staff CommandMenu (no people), ListSearch, ShortcutsDialog | A | `#23522` `#27378` (minus people) | ListSearch only (documents) | P1 / P2 |
| **Identity** | Key at rest on the rail tile, lock sweep during navigation | A | `MOTION.md` §6; BRAND_ASSETS | no | P1 (owner) |

**Rejected on the platform (D):**
- KPI tiles and charts of the person's «progress» (legal: no percentage, no score);
- candidate pipelines, people boards, talent counts (CR-03 / CR-04);
- drag-to-reorder kanban for forum proposals (state is not the user's to drag);
- avatar photos (DS #6: glyphs only);
- confetti or celebratory success motion (nothing is «approved»);
- AI chat assistant surfaces (no such function exists; inventing one is forbidden);
- theme / dark-mode toggles in the account menu (not in scope; the console chrome is already night);
- full-screen route loaders (`MOTION.md` rule: never full-screen);
- infinite scroll (registers are finite; pagination or grouping).

---

## 5. Status that reads — Chip V5, Seal, Piece Ledger

The legal law is untouched: **no colour ever means «approved»**. `conforme` is ink without chroma. Colour says only
«someone must act» (`--pending-700`), «refused / invalid» (`--err-700`), or «issued by an authority» (`--seal-600`).
The register comes from Python (`apps/core/chips.py`, `data-register`), never from a template.

### 5.1 Chip V5 (re-expresses DS V4 §8.3, which was never built)

- **Shape:** pill, `radius-full`, 24 px (20 in dense registers), padding-inline 8 / 10.
- **Structure:** `[glyph 14] word`, and `[· qualifier]` when there is one. The word is Plex 13/20 500 `--ink`, never
  coloured.
- **Register → glyph + border style** (glyph from `ICON_SEMANTIC_MAP.md` where it exists; the border is a full 1 px
  of the mark colour):

| Register | Mark | Border | Glyph (examples) | Meaning |
|---|---|---|---|---|
| neutro | `--ink-2` | solid | per state (`send` Transmis, `document` Déposé) | a fact, nobody late |
| attesa | `--ink-2` | dashed | `glasses` (en examen), `clock` | someone else is working on it |
| azione | `--pending-700` | solid, 1.5 px | `arrow-up-right` / `refresh-cw` (À remplacer) / `upload` (Manquant) | **you** must act |
| conforme | `--ink` | solid + a closing hairline under the body (V3 idea kept) | `check` | recorded as compliant, never «approved» |
| rifiuto | `--err-700` | double | `x-circle` | refused / invalid, with a reason |
| nullo | `--hairline-strong` | dotted, no body | `minus` | void / expired / withdrawn |
| unmapped | `--hairline-strong` | dotted | none | a bug made visible (V3 rule kept) |

- **The phase gauge moves inside.** The V3 «rule length = phase» becomes a **3-notch micro-meter** after the word (3 ×
  4 px dots, filled = phase), `aria-hidden`, with the phase in words in a visually-hidden span. The external gutter
  and its tick are retired: they are what reads as a glitch.
- **Status change:** the word and glyph crossfade 120 / 200; the border changes at once; one `aria-live` per register
  (DS §7 #10, `MOTION.md` §5.9).
- **Contrast:** marks against the paper follow `COLOUR.md` §5; its `verify_out.md` holds 363 pairs with 0 below the
  minimum. The glyph at 1.5 px effective stroke follows the `.chip__g` compensation (stroke-width 2.6 on the 24 grid,
  `chip.css` §5).

### 5.2 Seal

The seal (cut corner, double rule, bronze, `shield` glyph) is reserved to **acts of an authority**: visas, permits,
recognitions, when recorded. It is **not** used for «Vérifiée» (the project team's verification of a company). This
realigns the template with CD V4 §3.8; owner confirmation in §9.

### 5.3 Piece Ledger (replaces the proportional HealthStrip where n ≤ 24)

- **One pip per requested piece:** 12 × 12, radius 3, gap 4, in the order of the groups (À vous → Tiers → En examen →
  Examinées). Each pip's **shape** follows its register:
  - azione = solid square `--pending-700`
  - attesa = dashed outline
  - neutro = solid `--ink-2`
  - conforme = ink square with an inner check notch
  - rifiuto = square with a diagonal
  - nullo = dotted outline
- **Caption:** the locked sentence («3 pièces demandées · 0 sur 3 validées · 1 en attente»).
- **Visual first line** «À vous : 1», derived from the same counts. It is a count, not a judgment; copy review §9.
- **Why it is better:**
  - it is **discrete and verifiable** («one square per piece» can be counted on screen, which is the V4 principle
    «4 sur 11 is verifiable, a bar is not»);
  - it cannot be read as a progress bar;
  - the person's own pieces are first and distinct.
- **n > 24:** fall back to the proportional strip, but draw **only conforme as fill** and every other state as a
  hatched or outlined segment, so the filled part equals validated only.
- `aria-hidden`; the words carry the meaning.
- Animation: pips appear with the page (no stagger entrance, per law 2.2). On a state change, the one pip crossfades.

---

## 6. The journey — one thread from «Maintenant» to «Arrivée»

**The problem, restated.** Three engines speak to the person:
1. `cases.services.next_action()` over the checklist;
2. the documents register over requirements;
3. the orientation engine over the questionnaire.

The first ignores the other two. Result: contradictory «next actions», a case page saying nothing is asked, and a
primary CTA that exits the console.

**UX requirement for engineering** (a product decision, not CSS; stated as the behaviour the interface needs):

1. **One next action, computed over all open obligations of the person.** Precedence, extending the current
   `next_action` docstring:
   - blocking outcome;
   - overdue item (checklist **or** requirement);
   - due item;
   - open item the person must act on (a requirement «Manquant / À remplacer» counts here);
   - orientation not done;
   - state fallback.

   The same presenter feeds the dashboard NowPanel, the case NowPanel and the documents primary, so they can never
   disagree.
2. **One «Ce qui est demandé».** The case page lists checklist items **and** requirements for that case in one grouped
   list (§3.3 grouping), or the checklist panel explicitly links the requirements («3 pièces demandées pour ce
   dossier → Voir les pièces») instead of saying «aucune pièce».
   - Minimum P0 fix: the empty-state sentence must not say «Aucune pièce n'est encore demandée» when the requirements
     register has rows for the case.
3. **The orientation questionnaire runs inside the console for signed-in people.** `orientation/*.html` choose
   `portal/base_portal.html` when `request.user.is_authenticated` (a base-template variable). The public wizard stays
   public for visitors.
4. **Explain the two question flows.**
   - «Ma situation» = the facts the rules read (profile).
   - «Questionnaire d'orientation» = the pathway question flow.
   - Each page's lead names the other in one sentence, and the NowPanel names the one it sends you to.
   - Longer term (owner / product), merge them if the rules allow.
5. **JourneyRail step ↔ screen.** Each of the seven locked steps names, in its disclosure, the screen where the work
   of that step happens (Ma situation, Mon parcours, Mes pièces, …). This uses existing routes only; no step is linked
   when its screen does not exist yet.

**Where the V5 journey becomes a signature** (per [platform-domains] «La soglia» and `MOTION.md` §7):
- The same rail in three densities (public parcours, dashboard, case).
- The travelled line is drawn once per load and crosses the MA→IT frontier to the person's step.
- The current step is ringed (no pulse) and expanded.
- **Actors per step only when signed data exists** (`MOTION.md` §7: no presenter supplies them today; do not invent).

---

## 7. Priorities

**P0 — coherence and truth** (before any visual escalation is judged)
1. Unified next action, the case/documents contradiction and the orientation-in-console decision (§6). Engineering +
   product.
2. Chip V5 + Piece Ledger (§5); subgrid alignment + header row on `doc-collection` (§3.3 moves 3, 4, 7).
3. The NowPanel holds its primary; «Responsable» vs «Intervenant» (§3.2 moves 1, 2).
4. Situation counter coherence + DateField (§3.5 moves 1, 2).
5. Forum «unavailable» inside the console when the portal is on (§3.8 move 1); verify the 20 `extra_head` overrides
   (§3.9).
6. «Vérifiée» without the seal; the company CTA names its verb (§3.6 moves 3, 5).
7. Shell cheap wins: open rail from 80rem / labelled compact rail, `scrollbar-gutter: stable`, inline shell icons,
   `lang="en"` on Privacy Policy, console scroll-padding top and bottom (§3.1 moves 1, 7, 9, 10; §3.13 gap 1).
8. Person-facing state transitions as intent buttons, if the person does see that form (§3.4 move 4).

**P1 — the flagship interactions and continuity**
- Dépôt upload and the preview drawer (§3.3 moves 5, 6);
- document grouping and non-zero filters (§3.3 moves 1, 2);
- bell, badge and toasts (§3.10);
- busy key, cause bar, outcome diff and thread (§3.12);
- the journey rail signature (§3.2 move 3, §6);
- «À faire» and «Activité» on the dashboard (§3.2 moves 4, 5);
- account menu V5 and the travelling indicator (§3.1);
- «Aller à…» (§3.11);
- case merge and context index (§3.4 moves 2, 3);
- company overview and row targets (§3.6 moves 1, 2, 4);
- Guichet triage and threads (§3.9).

**P2 — migration and depth**
- Migrate the ~32 V2 templates by family:
  - piece detail and assessment first;
  - then need detail, requests / messages / deadlines / pathways;
  - Academy, helpdesk staff, selection;
  - Forum governance when its gate opens.
- Staff CommandMenu (no people), shortcuts dialog, notification preferences, Academy «Mon suivi», course covers
  (owner).

**Gates for every item:**
- the budget stays binding: LCP ≤ 2.5 s, CLS ≤ 0.10, INP ≤ 200 ms on slow 4G + CPU ×4, no avoidable long task
  > 50 ms;
- WCAG 2.2 AA with keyboard;
- an AR/RTL capture;
- a reduced-motion capture;
- the memory rule «re-measure after every change» on every page a shared sheet touches.

---

## 8. Owner decisions needed

1. **NowPanel owns the primary** (dashboard, case, company) instead of the ContextHeader. The one-primary rule is kept
   (§3.2 move 1).
2. **Empty-state doctrine:** collapse empty regions into one line and reserve EmptyState V5 for whole-page empties.
   This reconciles the dashboard comment with DS §8.30 (§2 D4).
3. **Chip V5:** retire the V3 external gutter and gauge, and move the phase into a 3-notch micro-meter (§5.1).
4. **«Vérifiée»** is not a seal (§5.2): the project's verification is not an authority act.
5. **Unified next action and the single list of «ce qui est demandé»** (§6): a product / engineering decision.
6. **The orientation questionnaire inside the console** for signed-in people, and how «Ma situation» and the
   orientation questionnaire relate (§6).
7. **Rail default:** open from 1280 px, or a labelled compact rail below; short labels for the bottom bar (copy
   review) (§3.1).
8. **Key glyph on the rail tile and the lock sweep** during navigation. This is a brand-asset use; the mark moving
   departs from «il marchio è fermo» (`MOTION.md` D1) (§3.1 move 8).
9. **Academy moves off serif** into the console language (§3.7). This reverses the V2 exception V4 left in place.
10. **Course covers** (a CMS field and sourcing) versus glyph tiles (§3.7 move 4).
11. **No «Personnes» type in any console command surface** (CR-03 / CR-04). Any staff person lookup stays in the
    back-office (§3.11).
12. **Copy review items:**
    - «Intervenant» for the case-level responsible;
    - «À vous : n» over the locked counts;
    - the counter wording for question 8;
    - the company CTA verbs;
    - the rail «Mes pièces» versus the page title;
    - group titles in sentence case.
13. **Speculation Rules on the console** (exclusions in §3.12 move 2), only after measurement.

---

## 9. Positions on conflicts inside the council

| Topic | Other council position | This panel |
|---|---|---|
| Photographs on the dashboard | [platform-domains] proposes «Console with a window»: a photo band in the dashboard header (`#19068`). `IMAGERY.md` §3.19 and `COLOUR.md` say «no photographs on operational screens» | **Side with IMAGERY / COLOUR.** The console's image richness comes from the person's real objects (document preview, the Piece Ledger), the journey rail, material and motion. Allowed exceptions: the no-case EmptyState (orientation image, as IMAGERY proposes) and Academy section / course imagery if the owner funds covers. A decorative photo band above the next action competes with the one thing the page must say. |
| Page transitions in the console | nav-shell curation: View Transitions everywhere | **Side with `MOTION.md` §5.5:** the thread alone in the console (measured +90 ms LCP with VT). |
| Staff command palette with «Personnes» | [nav-shell] `#27378` filters include Personnes | **Object** (CR-03 / CR-04, `selection/workspace.html`). |
| Arch at the MA→IT frontier on the dashboard rail | [platform-domains] «La soglia» draws the arch where the line crosses | V4 pillar 2 forbids the door in the dashboard. **Owner decision.** This panel's preference: a **small arch glyph** at the frontier node, 16 px (a glyph, not the full arch drawing). The identity gain is real and the dashboard needs one. |
| EmptyState | DS §8.30 dashed box + glyph 48 vs the dashboard doctrine «one sentence» | **Both, by scope:** one line for regions, the full component for pages (§2 D4). |

---

## 10. Surface → files → families (hand-off index)

| Surface | Main files | Families |
|---|---|---|
| Shell | `templates/partials/portal_chrome.html`, `templates/portal/partials/rail_nav.html`, `templates/components/account_menu.html`, `templates/portal/base_portal.html`, `apps/portal/static/portal/console.css`, `static/js/src/console.js`, `apps/portal/services.py` (navigation, short labels) | Shell, Identity, Notifications, Command |
| Dashboard | `templates/portal/dashboard.html`, `static/css/v4/workspace.css` (ws-grid, panel, journey, dates / threads), `apps/portal/services.py` | Headers, Now, Journey, Collections (TaskList), Feedback, Empty |
| Documents | `templates/portal/documents.html`, `templates/documents/partials/register.html`, `templates/components/{document_row,health_strip}.html`, `templates/documents/{requirement_detail,upload}.html`, `workspace.css` (doc-*), `console.js` §2–2b | Collections, Documents, Status, Measures, Overlays |
| Case | `templates/cases/detail.html`, `templates/cases/assessment.html`, `templates/components/{journey_rail,case_timeline}.html`, `apps/cases/services.py` (`next_action`, `transitions_available`) | Headers, Now, Journey, Collections, Forms (TransitionActions) |
| Situation / forms | `templates/portal/situation.html`, `templates/components/{wizard_stepper,option_cards,form_field,form_errors}.html`, `static/js/src/situation.js`, `apps/portal/views.py` L190–194 | Forms, Feedback |
| Company | `templates/companies/*.html`, `templates/companies/partials/*.html`, `apps/companies/services.py` L450–525 | Headers, Collections (Table), Status |
| Academy | `templates/academy/*.html`, `apps/academy/static/academy/academy.css` | Collections (Register-row V5), Measures |
| Forum | `templates/forum/governance/*.html` | Empty, Collections (StateLanes), Journey (Timeline) |
| Guichet | `templates/helpdesk/*.html` | Forms (Triage), Collections (Inbox / Thread), Table |
| Status system | `static/css/v3/chip.css`, `apps/core/chips.py`, `static/img/icons.svg` | Status |

---

## 11. What I could not do, and why

- **Captures.** 16 PNGs were read, within the budget. I did **not** read:
  - the Guichet captures: the capture role's diagnosis, and fixed by `c9a58d8` after capture;
  - the case / documents / company captures at 390 (only the dashboard and documents at 390 were read);
  - the collapsed rail;
  - any Arabic console: none exists.

  The Guichet's post-fix look, the platform in RTL, and the case on the phone are therefore **unverified** here.
- **No browser.** I did not open the running servers: `CAPTURES_AND_REFERENCES.md` reserves the QA Chrome to the
  capture role, and `MOTION.md` §0 records that a shared tab was disturbed once. Every claim about behaviour comes
  from code or from the 16 captures. The x-offsets quoted (state column 625 vs 651; the 15 px bar shift) are read from
  the PNGs by eye, not measured by the DOM.
- **No 21st.dev calls.** The three curations already cover every platform family with retrieved code
  (`21st_platform-domains.md`: 13 `get_component`; `21st_nav-shell.md`: 23; `21st_forms-docs.md`: 130 candidates
  checked). This panel cites their ids rather than re-querying. `generate` / `iterate_generation` were **not** called.
- **No Pexels calls.** Imagery positions defer to `IMAGERY.md`.
- **Not measured.**
  - The CLS / LCP / INP effect of any proposal: `scrollbar-gutter`, inline symbols, the thread, Speculation Rules,
    subgrid.
  - Whether Chrome serves prefetched `never_cache` portal documents.

  Each is gated in §7.
- **Data caveats.**
  - The `qa-doc-person` fixture carries `account_type=company` plus the PERSON role («· Entreprise» on the person
    dashboard), and it saw the «Faire évoluer l'état» form. Both need a clean person fixture before they are filed
    as product defects.
  - Whether the orientation questionnaire and «Ma situation» ask overlapping questions was **not** established: the
    orientation questions are ruleset data in the database, which this panel did not query.
- **Not re-verified.** Contrast figures for Chip V5 marks rely on `COLOUR.md` (`verify_out.md`: 363 pairs, 0 below
  minimum). The new pip shapes need their own non-text contrast check (3:1) once drawn.
