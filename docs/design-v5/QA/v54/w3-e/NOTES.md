# W3-E — The case file and the secondary console pages — notes

Family W3-E of the V5.4 plan (`docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.5 item 7, §3.1 item 7, §1.2, §1.14; the
platform map `C:/tmp/ile_v5_council/.work/v54-plan/platform.md` §3), worked in the owner's delivery mode (V5.5:
implement → review once → fix → ship) under the V5.8 CSS budget (the shared bundles never rise). Branch `v54-w3-e`,
worktree `C:/tmp/ile_wt/v54-w3-e`, from design-v5 (`3d5351b`, after the DevOps readiness merge DL54-121). Evidence
outside every repository: `C:/tmp/ile_v5_council/evidence/v54/w3-e/` (E/ below). Decision log: DL54-130 … (numbered
after W3-D's entries, which merge first; renumbered by the steward at the merge).

Three steps: (1) the secondary pages of the person's space, (2) the organisations and the other spaces (companies,
Academy, the help desk, selection, the Forum's governance, the deletion map's last rows), (3) the case file — last,
after W3-D's journey (tag `v54/w3-d`).

## Step 1/3 — the secondary pages of the person's space (implementer w3-e-impl-1, 15 October 2026)

**Lane.** Lane 5: dev server 8785 from this worktree on `ile_v5_l5` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag), pytest on `test_ile_v5_l5`, one pytest and one headless Chromium of
mine at a time, its own profile (`C:/tmp/ile_v5_council/.profiles/w3-e-impl-1/`). Signed-in pages through sessions
minted with `Client.force_login` by a scratch script outside the repository (no password used, typed or stored); the
benchmark lock checked before every browser series. Never 8780, 8782, Chrome 9222 / 9223. No browser run ended on a
crash. With `--noreload` the cached template loader keeps the first template it read: the server is restarted after
every template change (one capture series was re-shot for that reason).

**Personas and data.** `qa-person` (a file, two pre-assessments — one completed, one in progress —, three contact
requests) and `qa-fresh-person` (nothing: every empty state). The QA clone holds no communication and no date for
anyone, so the lane carries five communications and six dates for `qa-person`, written by the earlier attempt's scratch
`seed.py` on `ile_v5_l5` only and tagged «[w3e]» in their free text (two unread, one linked to a date, one to a request,
one subject long enough to wrap; dates late, in four days, in eleven, far, done, cancelled) — data, never interface copy.
The 503 page was drawn by switching the lane clone's `reserved_area_enabled` off for one series and back on.

### What was built

- **One grammar for the person's registers** — «Mes échéances», «Communications», «Mes demandes», «Mon parcours» — and
  their records (the communication, the request), on what the platform families shipped:
  - **the head**: W3-A's workspace head (`.ws-head`) — the title and its line of context, **no eyebrow** repeating
    the level the breadcrumb already gives (C-4; W3-A's note); a record's own words as its title (a subject, a
    request), isolated in their direction, hugging their box on the reading edge (DL54-64's rule);
  - **the band**: the register's count under the head on the dashboard's ledger line (`.db-ledger`) — the figure at
    20/28 and 500, never a stat card — in the bridge's own live words («échéance(s) à venir», «%(n)d en retard»,
    «demande(s) transmise(s)», «pré-évaluation(s) enregistrée(s)»), each event counted once (a late date is not also
    «à venir»); «Communications» keeps its own sentence («%(n)s communication(s) non lue(s)» / «Toutes vos
    communications sont lues.»), the one live region of the page (`role="status"`);
  - **the rows**: the dashboard's row (`.db-task`: hairlines, 64 px at least, a subgrid) given the registers'
    columns — the words · the state as a chip · the date; a communication: its seal · its words · its act;
  - **the whole row as the way to its record** (requests, communications): the title's link stretched over the row
    (z 1), the row's own act above it (z 2) — **0 dead points in 180 probes** (fr / ar × 1440 / 390, E/probe_rows);
  - **the state as a chip**, never painted by hand: `components/badge.html` is no longer included by these pages
    (see «The status register»);
  - **the date** in the dashboard's grammar (`.db-due`): the glyph of its register (alarm-clock late, clock close by,
    the calendar), the date; **the distance in words is not drawn** — no live string says it (B1 item 4, below);
  - **«Non lue»** as a word, with the ink dot and the heavier weight (never a colour alone), as the dashboard says it;
  - sections under the dashboard's head (`.db-h2`) with their domain glyph («À venir» calendar-clock, «Terminées ou
    annulées» history; a request's «Suivi» history, «Données transmises» send, «Votre consentement» pen-line).
- **«la lettera»** (`portal/message_detail.html`): a communication drawn as the letter it is — the team's mark
  (`ile-mark`, the registry's glyph of «Équipe du projet, as an actor or a sender») on its toned disc as the letter's
  seal, «L'équipe du projet», «Reçue le» and the state in words; a hairline; the text at the reading size and measure
  (17 px, 36rem); the record it is about (`related_link`) as the dashboard's section link; the acts.
- **«Communications»**: the same seal on every row (20 px, at its floor, in a 32 px disc) — every communication here
  is the team's; the subject one step quieter once read; «Marquer comme lue» at the row's end (under the words on a
  phone), still `btn btn--link btn--sm` in `form.portal-list__form` (W1-D's hook, kept as a class without a rule —
  `test_a_link_styled_submit_waits_without_a_key` passes fr / ar).
- **«Mes demandes»**: the V4 table (`account-table`, four columns) is gone for rows: the subject, the kind and the
  reference in ILE Mono («contact-3», the ledger's hand), the state chip, the day it was sent. **The request**: its
  subject as the h1 and its kind under it; «Suivi» is W1-C's summary strip (the state chip, the date, the reference —
  said once); then what was transmitted and the consent, as facts on hairlines (the values hug their words in their own
  direction — a French name on an Arabic page stood at the far side).
- **«Mes échéances»**: the open dates first (the late ones lead, being the earliest), then «Terminées ou annulées»,
  the latest first; each row its title as the team wrote it, its kind, its description and «Origine», its state chip
  (late azione «En retard», near attesa «Bientôt», done conforme «Terminée», cancelled nullo «Annulée»; an open date
  further off has none — its date and its section say it), its date with its glyph.
- **«Mon parcours»**: the band, the notice of what a pre-assessment is worth (said once, `data-result-kind`), then each
  saved result a record on its hairline — the outcome's title in its own language, its facts on W1-C's metadata row
  (date, rules version, state, the reference in ILE Mono — said once: a questionnaire still open is titled by it), the
  informational next steps (their groups named in words at the console's small size, no longer V1's folio label in
  tracked capitals), the locked disclaimer with its version, the way to the whole result, «Recommencer l'orientation».
  **W3-D's journey block** (`journey-page`, the journey's conditional page sheet) is carried verbatim at the head of
  the page: inert on this branch (no `journey` in the context) until W3-D's merge brings `journey_for`.
- **The empty state is design V5's component** (`components.css` §23 — W3-E's section; DS V5 §10.8): the domain's
  glyph in its 40 px toned disc, the title at 20/28 and 600, one sentence, one action, on the reading edge under a
  hairline; under forced colours the disc keeps a 1 px outline (W1-B's hand-off); V4's dashed, centred box leaves
  `v4/workspace.css`. On the console it spans the main column (W3-B's `.portal__main .empty-state` kept: the hairline
  lines up with the lists'); the pages that compose it their own way keep doing so from their sheets.
- **«Ma situation»'s one act is the phone's action bar** (W3-A's and W3-F1's hand-off): at 390 × 844 «Continuer» stood
  behind the bottom bar, under the first viewport. Below 64rem the act group (`.wiz__act`, `data-console-action` — the
  shell's O63 contract, W3-A's `_shell.css`) is the bar where the four entries stood, «Menu» kept at the reading end:
  «Continuer» across it while stepping, the form's submit on the last question (situation.js gives the submit its role;
  without script the submit is the act). «Précédent» and the position stay in the page's foot; the save on the way waits
  for the last question (two acts do not hold beside «Menu»; the Stepper reaches the last question in one press).
  Above 64rem the foot's end is as it was. Chrome on the phone: 48 + 61 px. The rules are the guided form's (§5 of
  W3-F1's `v5/_wizard.css`, which W3-D's merge moves into the page's own sheet `portal/situation.css`), written away
  from W3-D's hunks; the template's head comment says the page as it is now (design V5, no more «sticky glass foot»).
- **The 503 page** (`portal/unavailable.html`, the reserved area switched off): a page of service in the error pages'
  grammar (W3-F2: `cms/errori.css`, `errors/_door.html`, `errors/_way_on.html` — nothing of its own): the door at rest
  with the key **out of the lock** says it before the words do; «Espace réservé» in the label's seat where an error page
  names its status; the page's own sentences; «Retour à l'accueil»; the way on and «who can help me». No new copy.

### The status register

- `core.chips` gains three producers (W1-C's file, a justified extra path): `enquiries.SubmissionStatus` (new neutro,
  in_progress esame, handled conforme, **archived nullo**), `forum.RegistrationStatus` (pending «Reçue» esame — the
  Forum's team confirms it —, confirmed conforme, **cancelled nullo**, attended conforme), `portal.DeadlineStatus`
  (open attesa, done conforme, **cancelled nullo**); their enums enter `test_chips_registry.PRODUCERS`. Before, an
  archived request and a cancelled date went out as `neutral` (neutro); nullo's own definition is «withdrawn, not
  applicable, archived: it carries nothing». A computed state is a literal register: late azione, near attesa.
- **Every `badge.html` include of the person's registers is a `{% chip %}` call** (messages: none — «Non lue» is a
  word). The last console includer is `portal/partials/card.html` (W3-B's bridge, whose presenters give it the legacy
  `kind`): it moves with the bridge pages in step 2. `test_state_chips_carry_a_register`, `test_chips_registry`,
  `test_o14_lint` green.

### Identity carriers and the swap test (plan §3.1 item 7)

The person's registers carry no journey rail and only the requests' and dates' chips; the communications and the letter
carry neither. What says ILE on each at rest, with the console's chrome taken away (E/swap/: the rail, the bars and the
footer hidden, a neutral frame and Arial put in their place — «ACME Workspace»):

| Screen | Carriers named | Swap test |
|---|---|---|
| «Communications» | the project's mark as every row's seal; the ink-dot «Non lue» grammar; the band's one counter | passes: the seals alone say whose space this is |
| the communication («la lettera») | the mark as the letter's seal at its head; the date in the ledger's figures; the L2 key on «Marquer comme lue»'s wait | passes (the seal) |
| «Mes échéances» | «i cerchi» (the azione clock-hands disc, the attesa dashed ring, the nullo slashed ring, the conforme ink disc); the date's glyph by register; the band | passes: the chips and the date glyphs are ILE's status language |
| «Mes demandes», the request | the chips; the references in ILE Mono; the summary strip | passes |
| «Mon parcours» | the journey «La soglia» (after W3-D's merge); the references in ILE Mono; the locked disclaimer | passes on the references and, after the merge, the journey |
| the 503 page | the owner's door stage, the key out of the lock | passes (the brand's door) |

The guichet and the help pages (`templates/helpdesk/**`) are step 2's: named and swap-tested there.

### Measures

- **Smoke** (E/s1, s2, s4, s5, s3 for the 503): every page × fr / ar × 1440, 1280, 390, 360 — 200 (503 for the
  switched-off area), **0 horizontal overflow, 0 CSP report, 0 console error** (the 503's one «error» is the browser
  logging the document's own status), one h1, ≤ 3 corners on every first viewport (full · 4 px · 8 px), no shadow, no
  uppercase label, no animation at load (the entrance release only, once after the sign-in, W1-D's).
- **Text under 14 px at 390**: 0 % on every page (the phone console's step up, W3-A's T4).
- **CSS (gzip -9, the stewards' way, `weigh_pages.py`), design-v5 `3d5351b` → this branch**: `main.css` 37 324 →
  **37 232** (−92 B on every page: V4's empty-state box out); `portal.css` 1 935 → **1 669** (the V4 item list, the
  message body and the orientation results, no other reader); `console.css` 7 941 → 7 953 (+12: «Ma situation»'s act
  rules, in `v5/_wizard.css`, which W3-D's merge carries out of the console bundle into the page's own sheet);
  **the console page types 47 200 → 46 854** (−346 B on every console page; 46 842 once W3-D's merge has moved the
  guided form out). The registers' own page sheet `portal/registers.css` (first sheet, recorded at its measured size):
  **1 624 B**, linked by the six pages that draw it — their page type 48 478 B.

### Copy packet (B1 item 4) — the words not drawn

No live string says a deadline's distance; the date is drawn alone (with its glyph and its chip):
1. «dans {n} jour(s)» / «aujourd'hui» / «demain» — a date within 14 days (U5/D11, plan §1.18 D17);
2. «en retard de {n} jour(s)» — a date past due. (The e-mail notifications carry «(dans {days} jour(s))» and
   «(dépassée de {days} jour(s))» inside their bodies, not as strings of their own.)
3. A heading over the pre-assessments of «Mon parcours» («Mes pré-évaluations») — the band introduces them meanwhile.

### Items handed to W3-E (grep «W3-E» in QA/v54/*/NOTES.md and */SHIPPED.md) — answers

| From | Item | Answer |
|---|---|---|
| W1-B NOTES l.164, l.317 | `.empty-state__icon { stroke-width: 1.25 }` now means 1.25 px | **done** — removed by W1-B's own fix (DL54-36); the redrawn component writes no stroke: the `.icon` rule's 1.5 px (`test_icons` holds it) |
| W1-B NOTES l.333, SHIPPED l.87 | under forced colours the empty state's disc is gone | **done** — the component draws a 1 px CanvasText outline round the disc there (no layout change) |
| W1-C NOTES l.496 | the filter chip — a control; the staff filter bars are W3-E's | **step 2** (the help desk's queue and dispatch, selection): the person's registers draw no filter |
| W1-C NOTES l.605 | «Mes formations»' bare capitals, the hand-written console labels | **step 2** (Academy) |
| W1-D NOTES l.469 | «Marquer comme lue» is a link-styled submit: it waits without a key | **kept as designed** — the button and its form's hook unchanged; the loader's browser test passes fr / ar |
| W2-A NOTES l.183, l.281, l.738, SHIPPED l.160 | the staff consequence dialogs on the modal (`components/dialog.html`, `kind="alert"`, with the page-only overlay sheet) | **step 3** (the case file's staff state changes, C-5) |
| W2-A NOTES l.279, SHIPPED l.160 | the notification centre: the endpoint (the portal's owner), the trigger and `_notifications.css` (W3-A's slice) | **not built** — it needs a new view returning the latest communications as an asynchronous fragment, authorised by `portal.policies` (backend work), then W3-A's trigger and sheet. `_notifications.css` does not exist. The messages page draws its rows in the grammar the centre will draw (seal, dot, word, date) |
| W2-D NOTES l.775 | the empty-state component's V4 box is undone for the home in `pages.css` until W3-E redraws it | **done** — the component is V5. The home's news row keeps its two-column composition from `pages.css`; its disc is now the component's 40 px (the spec, DS V5 §10.8) — it was V4's 48 px («as tall as the row's two lines»): W2-D's to resize in its own sheet if it wants the two lines matched. Same for the Forum's (`_forum.css`) |
| W3-A NOTES l.67, l.133 | `companies/profile_form.html` renders two h1; eyebrows that repeat the breadcrumb's level | eyebrows: **done** on the person's registers (none); `profile_form.html`: **step 2** |
| W3-A NOTES l.327 | the company dashboard's «needs» head overflows by 4 px at 320 in Italian | W3-B's dashboard; re-measured in step 2 with the company pages |
| W3-A NOTES l.328 | the case file's phone action bar is the shell's contract (`data-console-action` / `data-file-action-bar`) | **step 3** |
| W3-A NOTES l.463, SHIPPED l.149 | in «Espace entreprise» the mark leads to the company dashboard even for a project reader without a company | **step 2** (the companies module) |
| W3-B NOTES l.150, l.197, l.213, l.285, l.333, SHIPPED l.152, l.166 | Panel, ContextHeader and HealthStrip leave `v4/workspace.css` with their last consumers (the case file, «Ma situation»); the case file's own section (866 B) | **steps 2–3** (the deletion map's last rows, with the case file) |
| W3-B NOTES l.336 | `companies/partials/need_table.html` is drawn by no page | **step 2** decides |
| W3-B NOTES l.367 (M3) | `.portal__main .empty-state` restored; W3-C / W3-E retire it with their redraw | **kept, deliberately**: with the V5 component it spans the hairline across the main column, where every list's hairline runs; W3-B's two tests unchanged |
| W3-B NOTES l.410 | W3-C / W3-E's planned deletions bring the console back under its ceiling | done for this step's part (−358 B); the case file's in step 3 |
| W3-C NOTES l.51 | the deadlines page draws the chip through `badge.html` | **done** — `{% chip %}`: computed states as literal registers, closed ones by `portal.DeadlineStatus` |
| W3-C NOTES l.99 | the hatch stays on the case file | **step 3** |
| W3-C NOTES l.198, l.252, l.429, l.578, SHIPPED l.104, l.120 | the deadlines page's template and its eyebrow; the case file's band (`case_header.html`) and the HealthStrip's last consumer | the deadlines page: **done**; the band and the HealthStrip: **step 3** |
| W3-F1 NOTES l.231, l.298, l.341, SHIPPED l.115 | «Ma situation»'s one act as the phone's action bar | **done** — `data-console-action` on the act group: «Continuer» (the submit on the last question) is the bar, «Menu» kept; W3-A's phone test retargeted to the contract its own notes foresaw |
| W3-F1 NOTES l.304 | `.section--verso > .t-prose` 1.06 : 1 on the case's pre-evaluation (`cases/assessment.html`) | **step 3** |
| W3-F2 NOTES l.232, l.543, l.570, SHIPPED l.110, l.118 | the V5 empty state is W3-E's component to take | **done** (above) |
| W3-F2 NOTES l.330, l.468 | `.account-table` — the console's requests list reads it | the requests list no longer does; the rule stays for allauth's table element (`templates/allauth/elements/table.html`) and the showcase — W4-D's last row of §27 |

### Seen on the way — other areas'

- **One counter per event** (plan §1.18 D17: «one live region, a dot on the rail»): the rail still says
  «Communications (2)» beside the page's band — W3-A's `_person_rail` (a live string); the dot is the rail's to draw.
- On an Arabic page, the locked disclaimer of a pre-assessment falls back to its French text without a `lang`
  (`{% locked %}`, cms) — as before this step.

### Tests

Non-browser: `apps/cases`, `apps/companies`, `apps/academy`, `apps/helpdesk`, `apps/selection`, `apps/forum`,
`apps/notifications`, `tests/test_phase_console.py`, `tests/security` (the object-permission and authorisation audits
among them), `test_frontend_bundle_is_current`, `test_chips_cards_w1_c`, `test_documents_w3_c` — **988 passed, 3
skipped** (design-v5's own skips). Browser: `tests/i18n/test_rtl_browser.py` **23 passed**; W3-A's shell and phone
tests, W3-F1's orientation tests and `test_loader_rules` **147 passed** after the two retargets below;
`test_browser_w1_b.py` (the empty states of the public pages) 4 passed.
`apps/portal` (non-browser 330 passed with the frontend set below), `apps/portal/tests/test_browser.py`,
`tests/frontend/test_dashboard_browser_w3_b.py` (35 passed), `test_chips_registry`, `test_state_chips_carry_a_register`,
`test_o14_lint`, `test_icons`, `test_dashboard_w3_b`, `test_css_bundle_is_current`, `test_static_pipeline`,
`test_design_docs` — green. `tests/frontend/test_loader_w1_d.py` browser: 19 passed, the mark-as-read test fr / ar
among them; **3 failed that are design-v5's own** (the integration fix list: `test_a_wait_that_no_page_ends_is_a_lease`,
`test_without_the_state_machine_nothing_waits` — the submit guard's `aria-disabled` —, and
`test_a_submit_control_that_is_not_a_button_of_the_system_declares_no_state` — a logout check for a class no page
carries): none reads these pages. One app test retargeted: `test_requests_list_is_paginated` counts the rows' hook
(`data-request`) instead of V4's `<tr>` — its intent (ten a page, newest first) kept.

### Paths outside the slice (for the merge step's manifest)

`apps/core/chips.py` and `tests/frontend/test_chips_registry.py` (W1-C's: three producers and their enums);
`apps/portal/static/portal/registers.css` and `v5/_registers.css` (new: the registers' page-only sheet and its
partial); `apps/portal/static/portal/portal.css` (the V4 item list, the message body and the orientation results
deleted — no other reader — and one line saying where they went); `apps/portal/tests/test_views.py` (the pagination
test's row count); `apps/portal/static/portal/v5/_wizard.css` (W3-F1's: the act group's §5 rules, «Ma situation»'s
action bar); `tests/frontend/test_console_shell_w3_a.py` (the frame's first block may be the workspace head) and
`tests/frontend/test_console_phone_browser_w3_a.py` (the questionnaire's foot test rewritten to the action-bar contract,
its intent kept: one bar at the bottom, «Menu» at its end, ≤ 120 px of chrome, the foot in the page).
`docs/design/DESIGN_SYSTEM_2026.md` §10: the prose of `badge.html`, `empty_state.html` and `page_header.html`.

### At W3-D's merge (tag `v54/w3-d` absent when step 1 ended)

`git merge design-v5` once the tag is there — expected meeting points, each to keep both sides:
- `templates/portal/situation.html` — W3-D's page-only sheet link (`css/dist/portal/situation.css`, after the shell's two)
  beside this step's act group and head comment; `apps/portal/static/portal/v5/_wizard.css` — W3-D's version (the
  Stepper out) with this step's §5 act rules (W3-D's hunks are elsewhere: the head, §1, §2, §6's header); they then
  ride in `portal/situation.css`, out of the console bundle (−12 B there).
- `templates/portal/pathways.html` — W3-D's journey block is already here verbatim; the `extra_head` joins W3-D's
  conditional journey link and the registers' link (both already written here).
- `apps/portal/services.py` — `pathways_page`: W3-D's return (with `journey`) and this step's `results_count` line in
  the try block; `static/css/v4/workspace.css` — W3-D's deletions (the JourneyRail, the Timeline) and this step's
  (the EmptyState); its header comment is W3-D's to keep (this step did not touch it).
- `docs/design-v5/DECISION_LOG_V54.md` — W3-D's entries first, this family's renumbered after them.

### Left for steps 2 and 3, and for others

- **Step 2**: the bridge's `portal/partials/card.html` (the last console includer of `badge.html`: its presenters give
  the legacy `kind`) with the institution / university pages; the modules' console pages (Academy, the help desk,
  selection, the Forum's governance, the companies' pages beyond the dashboard) — their eyebrows that repeat the
  level, `page_header.html` on the console, the guichet's and the help pages' identity carriers and swap test; the
  deletion map's last rows (`v4/workspace.css` — the dates and threads lists, Panel, ContextHeader, HealthStrip, the
  case header —, `components.css` §23 is done); `portal-facts` and `portal__section-title`, still read by the modules.
- **Step 3**: the case file (the journey, the NowPanel, the checklist as register rows, the people, the feed; the staff
  consequence dialogs on the overlay system; the phone action bar; the pre-evaluation's O4).
- **W3-A**: «Communications (n)» in the rail beside the page's band (D17's «a dot on the rail»).
- **The notification centre**: a view returning the latest communications as a fragment (the portal's owner), then
  W3-A's trigger and `_notifications.css`.
- **B1 item 4**: the words above (a deadline's distance; a heading over the pre-assessments).
- **cms**: the locked disclaimer's French fallback on an Arabic page carries no `lang`.

## Step 2/3 — the organisations and the other spaces (implementer w3-e-impl-2, 15 October 2026)

**Lane.** The same lane 5: dev server 8785 from this worktree on `ile_v5_l5` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag; restarted after every template change), pytest on `test_ile_v5_l5`,
one pytest and one headless Chromium of mine at a time, its own profile (`C:/tmp/ile_v5_council/.profiles/w3-e-impl-2/`).
Signed-in pages through sessions minted with `Client.force_login` by a scratch script outside the repository (no password
used, typed or stored); the benchmark lock checked before every browser series (never present; `DESIGN_V5_MERGE_LOCK`
was — W3-D's merge in progress, not a browser lock). Never 8780, 8782, Chrome 9222 / 9223. No browser run ended on a crash.

**Personas and lane data.** The clone's own: `qa-person` (Academy: four enrolments and a plan; the help desk: five
requests), `qa-fresh-person`, `qa-company` (four needs), `seed-company` (no company: the declaration), `demo-professionnel`
(the help desk's queue), `demo-operateur` (the dispatch desk), `seed-actor` and `seed-person` (a selection process),
`qa-admin` (the analysis, the annual report). Two lane-only additions, on `ile_v5_l5` only, tagged «[w3e]» and removed at
the end of the step (scratch `seed_gov.py`, `seed_bridge.py`): the Forum permanent's flag `virtual_forum` opened for the
series and closed again (it was absent: G11 keeps the module shut), `qa-person` a participant of the Rovigo edition with a
live and a lapsed mandate, `qa-company` the commission's referent, a table, three proposals (a draft, one deposited, one
retained with its motivation), the project born of it with two milestones and a monitoring entry, the edition's report
assembled (a draft: the secretariat's and the administrator's to read); and the bridge's two accounts, an institution
(an overdue date, one in four days, one in seventeen, an unread and a read communication, its organisation) and a
university (its organisation only), unusable passwords — as W3-B's lane did.

### What was built

**One grammar for the console's secondary pages.** Step 1's registers' grammar — the workspace head (no eyebrow repeating
the level the breadcrumb gives, C-4), the band, the dashboard's row with the state as a chip and the whole row as the way
to its record — now draws the organisations' and the other spaces' pages too, with six devices added to the same partial
(`apps/portal/static/portal/v5/_registers.css` §9–§14) and one page-only sheet for all of them (`portal/registers.css`):
- **the clause** (`.reg-note`): what a record is not — never a decision, a title, a promise — at the foot of a page or
  under its section, one quiet paragraph after a hairline (V1's `.note` in its 34ch margin rail, redrawn);
- **a sequence of steps and the log** (`.reg-steps`, `--log`): a course's modules, a follow-up's modules with the one
  current step (`aria-current="step"`, its place in the accent's ink) and its act, a process's phases with the actor named
  on the current one, a need's history, a project's monitoring — each its place in ILE Mono (never a display numeral),
  its words, its state as a chip (V1's `.sequence` with its green rules and ordinals, redrawn);
- **the exchange** (`.reg-turns`): the help desk's turns, each headed by WHO speaks — a function, never a person's
  name: its actor's glyph through the registry's ACTOR map (the person, the appointed professional's briefcase, the
  project's mark), the function, the date, the turn's kind as a tag —, the text at the reading size and measure; the
  professional's own note on the area's ground with its word «note interne»;
- **the answerable party** (`.reg-party`): who answers for a stage, a need or a request — its actor's glyph (the
  authorised actor's `badge-dot` through the registry, never a literal), the label of its role, its name (an
  organisation's or a function's), its facts on one line (quality, authorisation in ILE Mono, jurisdiction, validity as a
  chip), the clause that the platform is not the intermediary; flat between two hairlines (V1's band on the process
  ground between a navy and a rubric rule, redrawn);
- **the form of an act** (`.reg-form`): its title (an `h2`/`h3`, no longer a paragraph in tracked capitals), its
  sentence, W1-C's fields and actions (`v5/field.css`); the forms of one page one after another, each opened by a
  hairline;
- **the filter** (`.reg-filter`): the register's counts as the way to narrow it — links on a hairline, the chosen one
  under the tabs' one indicator, `aria-current`, the count beside each word, a group with nothing in it a word;
  `?état=` / `?domaine=` in the URL, no script.
Plus a sub-heading (`.reg-sub`), a stack of blocks (`.reg-stack`), the reading text (`.reg-prose`, the letter's size and
measure), the head's second line and facts, and **the page's one column** (`.reg-page`: `minmax(0, 1fr)` — a table's
scroll region or a long reference overflows inside itself and never widens its siblings past a phone's edge; found on the
selection's process at 390, where the authorised actor's band and the clause ran under the frame's edge).

**The console's table on V5** (`portal.css`, its only consumers being these pages): the head in the console's small type
over a structure hairline, the rows on decorative hairlines, the row's head at the control's weight — no tracked
capitals, no navy rule, no display serif; on a phone the labelled pop-in in the head's type (no capitals in any
script) and every console table's scroll rules (moved there from `selection.css`; the phone's pop-in now releases the
wide table's floor inside `.scroll-x` too).

**The pages** (every word the catalogue's — no new copy; the V1 devices left with the redraw: the folio and its
ordinals, the register entries with their arrows, `.empty`, `.note`, `.gloss`, `.sequence`, `.outcome`, `.sources`, the
eyebrows «Plateforme», «Academy», «Mon suivi», «Sélection autorisée», «Forum permanent»):
- **the guichet** (`templates/helpdesk/**`): the person's requests and the professional's queue (the head with the
  page's one act «Ouvrir une demande», the band in the module's words, one row a request — its subject the way to it,
  its reference in ILE Mono, the file it is about, its state as a chip, the day it was opened); the request («État de la
  demande»: what follows and whether it depends on the person, the request's facts with the reference said once; the
  appointed professional and the mandate as the answerable party — an ended mandate kept, said by its word and the nullo
  chip; the exchange; one form an act); opening a request on W1-C's form; the dispatch desk's chrome (the nested double
  scroll region with two focus stops became one);
- **the Academy** (`templates/academy/**`): the catalogue (the domains as the register's filter; one row a course — its
  title in its own language, its summary, its body named first and its facts; «déjà inscrit» as a chip; «Où j'en suis»
  in W1-C's summary strip and the way to «Mes formations»), «Mes formations», the course (its one act at the head's
  reading end — enrolling, a POST — with its sentence; the facts; the description at the reading size; the modules in
  order), the follow-up (the attendance as a short document — its title, its reference in ILE Mono, its facts, its
  clause —; the one current module and its act; interrupt / resume), the plan (the gap table with its chips);
- **the selection** (`templates/selection/**`): the authorised actor as the answerable party on every screen where a
  stage is visible, the workspace (the band, one row a process), the process (its head with its phase as a chip, the
  mandate's facts, the phases, the actor's two acts as forms, the evidence, the identity's disclosure, the trail), the
  person's panel (each request waiting: its party, its facts, the decision's form, the clause; each decision with its
  consultations), the identity communicated;
- **the company's pages beyond its dashboard** (`templates/companies/**` but the dashboard): «Mes besoins en
  compétences» with **the register's counts as its filter (E-3)** — «Tous» and the dashboard's own groups À faire ·
  En cours · Clos (W3-B's `_company_needs` grouping, extracted as `_need_groups`, and `portal.services.needs_register`),
  each its count and the marks of its states, the chosen group's rows; the needs' rows on the dashboard's needs columns,
  the whole row the way to the need, who answers for it under the actor's glyph or, in words beside the dashed disc,
  nobody yet; the need (its head with its reference, state and since, and the company's acts on it — modify, transmit
  the one primary —; the pending notice before transmission; the verification's clause; the live assignments as
  answerable parties; the post as facts on hairlines; the skills; the history as the log; the withdrawal as a form);
  «Mon entreprise» (the identity as facts, the verification, the clause); the declaration and the forms — **one h1**
  (the declaration drew two, W3-A's finding); the analysis's chrome (a staff page). **The V1 company band** that every
  page repeated **left** (one identity per screen: the rail's space and the page's subject — S-5's «one rail» is W3-A's
  one rail per space) and `companies/partials/company_header.html` is deleted. **No bar chart (E-4)**: none was drawn —
  the analysis is a table of counts and stays one. The dashboard (W3-B's) links no module sheet any more;
- **the Forum permanent's governance** (`templates/forum/governance/**`): «Ma participation», the commissions, a
  commission, a table, the proposals, a proposal (its decision with its motivation; the cycle's act as a form), tabling
  one, the projects, a project, the annual report — rows, facts, tables, the log; the module's clause is the registers'
  clause; the closed module's 503 drawn as the reserved area's twin (the error pages' grammar, W3-F2: the door at rest
  with the key out of the lock, «Forum permanent» in the label's seat, «pas encore ouvert» — never «maintenance»);
- **the bridge** (`templates/portal/partials/card.html`, W3-B's partial; its presenters in `portal.services`): the
  registers' states as chips **through their producers** — a request's member, a scan's member (its chip word, as on the
  person's dashboard), a date's urgency as a literal register (azione late, attesa close by), the head's late dates azione
  and its unread count neutro; a communication not yet read says so with the ink dot, the weight and «Non lue», never a
  chip; a membership's role is a fact of the row's line. **`components/badge.html` is retired on console pages** — the
  dev showcase is its one includer. **«Mon organisation» draws the account's audience glyph** — an institution's
  `institution`, a university's `university`, a company's `building` (the registry's AUDIENCE map; it drew the company's
  building for every account). The bridge's regions were already W3-B's real data, without a stat tile or a serif numeral.
- **the e-mail notifications** (`templates/notifications/email/**`): plain text, no class name — nothing to change.
- **the staff and back-office pages**: the chrome only — the dispatch desk and the analysis on the same head, sections
  and console table; the Django admin untouched. Their working screens are design debt (below).

**Glyphs on the section heads** only where the registry names the section's concept and the symbol holds at the head's
16 px: `book-open` (the Academy), `inbox` (a professional's queue), `list-ordered` (the selection's processes and
phases), `pen-line` (the identity's disclosure), `file-plus` (a proposal), `map` (the analysis), `building` (the
company's identity), `history` (a trail: the exchange, a need's history, the monitoring, the decisions), `briefcase` (the
plans read under a mandate). `concierge-bell`, `wrench`, `settings` and `calendar-range` need 20 px and `handshake` 24:
those heads carry their words alone.

### The gate, measured

Lane 8785, every page of the area — 48 page types × fr / ar: the company (11, with the dashboard for the regression),
the Academy (9), the help desk (7), the selection (4), the Forum permanent (12), the bridge and the staff's dashboard
(4), the professional's request (1) —:
| Item | Result |
|---|---|
| The drawings | **192** — 48 page types × fr / ar × 1440 × 900 and 390 × 844 (phone emulation), each session's page signed in by its persona (E/m2/); every one 200 |
| Corners on the first viewport | **≤ 3** everywhere — full · 4 px · 8 px; the area's pages ≤ 2 (the chips' full, the buttons' and fields' 4); three only on the company's and the administrator's dashboards (W3-B's NowPanel, 8 px) |
| Raised panels · shadow values | **0 · 0** on every page of the area; 1 · 1 on the two dashboards (W3-B's NowPanel, its one value) |
| CSP reports · console errors | **0 · 0** |
| One h1 | on every page (the company's declaration drew two) |
| Eyebrows · `badge.html` · tracked capitals | **0 · 0 · 0** on the area's pages (W3-B's dashboard keeps its «Entreprise» eyebrow, below) |
| Animations running at load | **0** |
| Horizontal overflow 320 → 430 px | **0** on the 96 page × language pairs at 320 · 360 · 375 · 390 · 412 · 430, content clipped under the frame's edge counted too (E/sweep2/; the first sweep missed the selection's band running under the frame at 390 — clipped, not scrolled: the measure now counts it, the column was fixed) |
| Text under 14 px at 390 | **0 %** on every page of the area (the fields' help and the required note raised to the console's small size; W3-B's dashboard 3 %) |
| Forced colours · reduced motion | 21 drawings (E/fc1/: seven screen types × fr / ar at 1440 under forced colours and reduced motion, and at 390 under reduced motion): the filter's indicator in Highlight, the internal note outlined, every chip's edge and mark, every hairline; nothing moves at rest |
| Before | E/before/: the 39 page types at 1440 in French before the step — the V1 folios and ordinals, tracked capitals, the company band, the green sequences, the need's broken «Responsable» row, the governance shut |

### Identity carriers and the swap test (plan §3.1 item 7)

What says ILE on each screen type at rest, with the console's chrome taken away (E/swap2/: the rail, the bars and the
footer hidden, a neutral frame and Arial in their place — «ACME Workspace»):

| Screen | Carriers named | Swap test |
|---|---|---|
| the guichet — requests, queue | «i cerchi» (the requests' chips), the references in ILE Mono, the clause's voice | passes on the chips' marks |
| the guichet — a request | the exchange's seals: the actors' glyphs of the registry (the person, the appointed professional's briefcase, the project's mark), the chip and its mark, the references in ILE Mono | passes: the seals alone say whose exchange this is |
| the guichet — opening a request | the L2 key in the submit's wait (W1-D), W1-C's field with its drawn focus rule, the clause | weak at rest — a form; the key says ILE the moment it is sent |
| the selection — workspace, process, panel | the authorised actor's `badge-dot` (an accreditation, never a check), «i cerchi», the phases' places and the references in ILE Mono | passes |
| the company — needs | «il registro»: the ledger marks in the filter, coloured by the group (O62), the chips, the dashed disc of «aucun intervenant désigné», the references in ILE Mono | passes |
| the company — a need, «Mon entreprise», the forms | the answerable party's glyph, the chips, the log, the references | passes (the forms: as the guichet's) |
| the Academy | «déjà inscrit» in conforme's ink disc, the modules' places and the attendance's reference in ILE Mono | passes |
| the Forum permanent | the chips, the references in ILE Mono, the lapsed mandate's nullo | passes on the chips |
| the bridge | the audience glyph of «Mon organisation», the unread ink dot, the chips | passes |

### Measures — the CSS (gzip -9, mtime 0, the stewards' way; design-v5 `3d5351b` → this branch)

| Page type (the sheets it links) | step 1 `d912f9a` | step 2 | change |
|---|---:|---:|---:|
| **SHARED** `main.css` — every page | 37 232 | 37 232 | 0 |
| **SHARED** main + console + portal — every console page | 46 854 | **46 689** | **−165** |
| the company's dashboard (W3-B's: no module sheet now) | 47 727 | 46 689 | −1 038 |
| the bridge (institution, university) | 46 854 | 46 689 | −165 |
| the help desk (+ registers + helpdesk) | 47 729 | 49 544 | +1 815 |
| the Academy (+ registers + academy) | 47 472 | 49 474 | +2 002 |
| the selection (+ registers + selection) | 47 939 | 49 745 | +1 806 |
| a company page — the register, the identity, the forms, the analysis (+ registers) | 47 727 | 49 282 | +1 555 |
| a need's page (+ registers + companies) | 47 727 | 49 471 | +1 744 |
| the Forum permanent (+ registers) | 46 854 | 49 282 | +2 428 |
| the person's registers, step 1 (+ registers) | 48 478 | 49 282 | +804 |

From the branch's base (design-v5 `3d5351b`), both steps: `main.css` 37 324 → 37 232 (−92 on every page), the console page
types 47 200 → 46 689 (−511 on every console page).

Module sheets: `helpdesk.css` 875 → 262 B, `academy.css` 618 → 192, `selection.css` 1 085 → 463, `companies.css` 873 →
189 (linked by a need's page only); `portal.css` 1 669 → 1 504; `portal/registers.css` 1 624 → 2 593 (the six devices).
`main.css` unchanged (37 232 B): the V1 rules these pages no longer use are still read by other pages or are other
families' rows (below). **The shared bundles fall** (−177 B on every console page); the module pages pay the registers'
sheet — 2.5 KB, one sheet for the one grammar, cached once for ≈ 40 pages — instead of their V1 module sheets and V1
devices: +1.6 to +2.4 KB a page type, +804 B on step 1's registers (the new devices). Measured with
`weigh_area.py` (scratch, the stewards' gzip -9 / mtime 0), each page type with the sheets it links then and now.

### Tests

Non-browser, on the final tree: `apps/helpdesk`, `apps/academy`, `apps/selection`, `apps/companies`, `apps/forum`
(the governance's flag, access, lifecycle, privacy and report among them) — **488 passed**; `apps/portal`,
`tests/test_phase_console.py`, `test_design_docs`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`,
`test_static_pipeline`, `test_icons`, `test_state_chips_carry_a_register`, `test_chips_registry`, `test_o14_lint`,
`test_template_comments_do_not_leak`, `test_dashboard_w3_b`, `test_chips_cards_w1_c` — **587 passed**; `tests/security` (the
object-permission and authorisation audits), `apps/notifications`, `apps/cases` — **350 passed, 3 skipped** (design-v5's
own skips); `test_console_shell_w3_a`, `test_console_shell_stylesheets` — green. Browser: `tests/i18n/test_rtl_browser.py`
and `apps/portal/tests/test_browser.py` **31 passed**; `test_dashboard_browser_w3_b.py` (the bridge), W3-A's shell and
phone browser tests **91 passed**. One test file retargeted, intent kept: `apps/helpdesk/tests/test_views.py` — the
empty register is the console's one line (`db-empty`: who fills it and when, never a box or a glyph in a disc), the
register's rows (`db-tasks reg-rows`). `test_design_docs`' count of `page_header.html`'s other consumers follows the
redraw (DS 2026: «e almeno altri 8»).

### The items handed to step 2 — answers

| From | Item | Answer |
|---|---|---|
| step 1 | the bridge's `portal/partials/card.html`, the last console includer of `badge.html` | **done** — the states through their producers; `badge.html` retired on console pages |
| step 1, W3-A NOTES l.133 | the modules' eyebrows that repeat the level; `page_header.html` on the console | **done** — no eyebrow on any page of the area; no module page includes `page_header.html` any more |
| step 1, plan §3.1 item 7 | the guichet's and the help pages' identity carriers and swap test | **done** (the table above) |
| step 1, the deletion map | the last of `v4/workspace.css`; `portal-facts` and `portal__section-title` | `v4/workspace.css`: **every rule is still read** (the audit: 114 classes, none without a reader but two showcase samples) — the file goes with the case file (step 3). `portal-facts` stays: it is the console's facts list, which these pages draw on hairlines. `portal__section-title`, `portal-section` and the folio counter: read by `cases/assessment.html` only (step 3); four other portal rules deleted |
| W1-C NOTES l.496 | the filter chip — the staff filter bars are W3-E's | the console's filter is built (`.reg-filter`: the needs' groups, the Academy's domains); **the staff's filter bars are design debt** (the dispatch desk, the analysis) |
| W1-C NOTES l.605 | «Mes formations»' bare capitals | **done** — the folio heads and tracked capitals left every Academy page |
| W3-A NOTES l.67 | `companies/profile_form.html` renders two h1 | **done** — one head, one h1, in both modes |
| W3-A NOTES l.327 | the company dashboard's «needs» head overflows by 4 px at 320 in Italian | W3-B's dashboard; this step's sweep is fr / ar (0 there) — not re-measured in Italian |
| W3-A NOTES l.463 | in «Espace entreprise» the mark leads to the company dashboard for a project reader without a company | **not done** — the space's head (`shell_space`, W3-A's) and `companies.services.navigation` decide it; a project reader is staff (design debt above) |
| W3-B NOTES l.336 | `companies/partials/need_table.html` drawn by no page | **kept** — the dev showcase includes it; no product page does |
| platform.md §3 | the company: the V5 skin, E-3, S-5, E-4 | **done** — the skin; the counts as the needs register's filter; one identity per screen in the space's one rail; no chart |
| platform.md §3 | the institution and the university: real data only, no stat tiles, no serif numerals, never a region the account cannot use, distinct audience glyphs | the bridge's regions (W3-B's) hold; **the audience glyph is drawn** («Mon organisation»); the rail's person-file entries offered to these accounts are W3-A's (above) |

### Paths outside the slice (step 2, for the merge step's manifest)

- `apps/portal/static/portal/portal.css` (the console's `.data-table` on V5 and the scroll rules from `selection.css`;
  four dead rules and the V1 sequence's current step deleted — their consumers were these pages);
- `templates/portal/partials/card.html` (W3-B's partial, assigned at its merge: the states through their producers, the
  unread grammar, the organisation's glyph — the retirement of `badge.html` on console pages is W3-E's per §3.5 item 7);
- `apps/portal/services.py` beyond «its presenters for the secondary pages»: the bridge's card presenters (`CardItem`,
  `Card`, the five builders, `_organisation_glyph`) and W3-B's `_company_needs` split into `_need_groups` (output
  unchanged) for `needs_register`;
- `apps/companies/views.py` (`needs`: the register's filter, two lines — the view is the companies module's);
- `apps/helpdesk/tests/test_views.py` (two pins of art direction A retargeted, their intent kept: the empty register is
  one line, the register's rows).
Step 1's six paths stand (`portal/registers.css` and `v5/_registers.css` are this family's page sheet).

### Seen on the way — other areas'

- **W3-A (the rail)**: an institution, a university and a company account without the person's role get the person's
  file entries in «Espace réservé» — «Ma situation», «Mon parcours», «Mes dossiers» — regions they cannot use (the
  orientation is offered to persons and professionals only, `ORIENTATION_ACCOUNT_TYPES`; they hold no file). `_person_rail`
  could drop them for `ORGANISATION_ACCOUNT_TYPES` (the bottom bar's «cases» then yields to «requests»); the «ten» are
  pinned by W3-A's tests, so not here.
- **W3-A / the Forum module**: the governance pages' rail appends the module's five entries without glyphs (the current
  one an empty white disc) and on the module's pages only — `forum.governance_services.navigation` still extends the
  old `portal.services.navigation`; it wants `shell_navigation`, NAV keys and a place in the space (the module is shut in
  production, G11).
- **W3-B (the company dashboard)**: the `ctx__eyebrow` «Entreprise» in tracked capitals; `glyphs.needs` (`wrench`, floor
  20 px) drawn at the head's 16 px.
- **The modules' trails**: the Academy's pages have no «Espace réservé» level; the selection's level says «Sélection
  autorisée» and links to the authorised actor's workspace on the person's panel too (W3-A's note) — the views' crumbs.
- **W4-D / W3-D (V1 sheets)**: selectors no template draws any more after this step — `note__marker`, `folio__date`,
  `sequence__actor`, `sequence__crossing` (`register.css`), `t-entry`, `t-lead`, `t-muted`, `t-plate`, `t-title`,
  `t-secondary`, `list-reset`, `section--d`, `section--flush-top`, `section--process` (`layout.css`, `base.css`),
  `entrance__cta`, `entrance__icon`, `icon--accent`, `icon--inline` (`components.css`) — left to their rows (W3-D's
  sequence is being merged; the rest is W4-D's sweep).
- **W1-C (fields)**: on a phone the fields' help and the required note stay at the public 13 px; this family's pages raise
  them to the console's small size (14 px on a phone) from the registers' sheet — a console-wide rule would belong to
  `field.css` or the shell.
- `companies/partials/need_table.html` stays (W3-B: «W3-E decides»): no page draws it, the dev showcase includes it.

### Design debt — the staff and back-office pages (V5.4: «the chrome only», recorded)

The dispatch desk (an operator's table of requests waiting, each with its mandate form in a disclosure) and the
territorial analysis (counts by territory, sector and state) have the console's head, sections, table and clause; their
working screens are not redesigned — density, saved views and filters for staff (the platform map's §4: the only
audience for whom saved views and density pay), the staff's filter bars (W1-C's «filter chip — a control»), a home of
staff's own (W3-A's note). The Django admin keeps Django's chrome. The staff consequence dialogs on the modal are step 3's
(the case file's state changes, C-5).

### Left for step 3, and for others

- **Step 3**: the case file (the journey, the NowPanel, the checklist as register rows, the people, the feed; the staff
  consequence dialogs on the overlay system; the phone action bar; the pre-evaluation's O4) and the last of
  `v4/workspace.css` — its every rule is still read today (the case file's section, Panel, ContextHeader and the
  workspace head, HealthStrip, Glyph, the dates and threads lists, the JourneyRail's until W3-D's merge): the V5-named
  rules other pages still draw (`.ws-head`, `.ctx`, `.glyph`, …) move to a V5 sheet, the case file's go with its
  redraw, then the file and its `main.css` import line. `cases/assessment.html` is the last reader of `portal-section`,
  `portal__section-title` and the folio counter in `portal.css`.
- The words not drawn (B1 item 4) — step 1's list stands.

**The lane at the step's end.** The governance's data and the bridge's two accounts removed, the flag `virtual_forum`
closed again as it was (absent), the eleven sessions revoked, the lane server stopped; step 1's «[w3e]» communications
and dates for `qa-person` stay. To draw the governance or the bridge again on lane 5: `seed_gov.py add` and
`seed_bridge.py add` in `C:/tmp/ile_v5_council/.work/w3-e/w3-e-impl-2/` (and `remove` after), then `sessions.py mint`.

## Step 3/3 — the case file (implementer w3-e-impl-3, 15–16 October 2026)

**Before the step.** The tag `v54/w3-d` was on design-v5 (`fec37d3`): `git merge design-v5` at once (`7f7ca9a`) — both
areas kept where they met: «Mon parcours» (this family's head, band and records with W3-D's journey at the head and both
page-only links), the decision log (W3-D's DL54-122 … 129 first, this family's DL54-130 … 141 unchanged after them: no
renumbering), `v5/_wizard.css` (W3-D's guided form, this family's §5 act rules — they now ride in
`portal/situation.css`, out of the console bundle); the CSS bundles rebuilt from a clean dist.

**Lane.** Lane 5: dev server 8785 from this worktree on `ile_v5_l5` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag; restarted after every template change), pytest on `test_ile_v5_l5`,
one pytest and one headless Chromium of mine at a time, its own profile
(`C:/tmp/ile_v5_council/.profiles/w3-e-impl-3/`). Signed-in pages through sessions minted with `Client.force_login` by a
scratch script outside the repository (no password used, typed or stored): `qa-doc-person` (the reference case
`EE167596D4`), `demo-professionnel` (its assigned professional — the staff controls), `qa-person` (`E46E03B461`: five
lines, a pre-assessment, seven pieces, the Conditions gate), `seed-person` (`0FEEBAE3A9`, in SELECTION with its
authorised actor), `qa-admin`, `qa-fresh-person`. The benchmark lock was checked before every browser series (never
present; `DESIGN_V5_MERGE_LOCK` was held by `sec-f5-merge`, then by `intfix-merge` — merges, not a browser lock). For
the load check only, the tree before this step (`git archive` of `7f7ca9a` into the scratch folder) was served on a twin
port, 8796, then stopped and removed. Never 8780, 8782, Chrome 9222 / 9223. No browser run ended on a crash.

**Lane data.** The reference case holds three pieces and **no checklist line** on the clone: the step drew its checklist
with lane-only lines on `ile_v5_l5` (scratch `seed_case.py add`, tagged «[w3e]» in their words): five lines (in progress
and overdue with a source reference; blocked, the professional's, due soon, linked to the file's piece «Diplome ou titre
de formation»; pending, the authority's, with its note and source; done, the company's; not applicable), their status
changes by the person and the professional (the timeline; the interaction runs' changes on top, each put back), one
communication and two dates for `qa-doc-person`. Removed at the step's end (below).

### What was built

**The case file** (`templates/cases/detail.html`; plan §3.5 item 7; the platform map §3 «Case file») — composed, never a
new component family, on what the platform families shipped, in the order of a file's five questions (the DOM's order
too):
- **the head** — W3-A's ContextHeader: «Dossier» and the reference in ILE Mono, the objective, the state as a chip,
  «depuis le …». **No eyebrow** repeating the title (C-4). No action: the page's one primary is the NowPanel's.
- **1 · where am I** — W3-D's journey «La soglia», descriptive (the spine, each reached step dated), under its head.
- **2 · what next** — W3-B's NowPanel (the screen's ONE raised plane, its ONE primary) over the same one next action as
  the dashboard and the documents (T1; `portal.services.case_now_panel`): a checklist line has no page of its own, so
  its act — «Continuer» — leads to the line's row on this page (`#line-<pk>`, where its menu is); **a mandated reader**
  (professional, operator, administrator) is told the file's next step in nobody's voice — «Prochaine étape», whose it
  is in the facts, no primary, a piece still readable («Consulter») — where V4 told the professional «Votre prochaine
  action» for the person's act; no account date takes it over (the takeover is the dashboard's). **On a phone** the
  primary is the page's action bar (`data-file-action-bar`, the shell's O63 contract: where the bottom bar's entries
  stood, «Menu» kept at the reading end) and is not drawn a second time in the panel.
- **3 · what is asked** — «Ce qui est demandé»: **«Exigences», the checklist as the register's rows, never a table
  (C-3)** — the dashboard's row in four columns that line up (subgrid): the line in its own language, who answers for it
  (a fact every line states — the acceptance criterion — with the actor's glyph and the team's note), what the team
  wrote, the source in ILE Mono; the state as a chip; the date with its glyph and word while the line is open (F8: a
  settled line's date reads calm); the line's menu. The line one of the file's pieces satisfies
  (`DocumentRequirement.checklist_item`, readable by the reader) is the way to that piece (its title stretched over the
  row). Then **«Pièces du dossier»** — the dashboard's «il registro» (the pieces by whose move it is, each a mark of its
  state) and every piece the reader may read in the register's order (the register's own presenter and authorisation),
  the row the way to the piece, its act where the reader acts («Déposer» / «Remplacer la pièce»), «Bloqué» beside the
  chip where the Conditions gate stops the filing, who holds it otherwise; the NowPanel's piece is drawn there only. The
  V4 page had no pieces at all: for the reference case (three pieces, no line) it said «Aucune pièce n'est encore
  demandée» — untrue.
- **4 · who** — «Qui intervient sur ce dossier»: each live mandate as the registers' answerable party (the role's glyph
  through the registry — the project's mark for an operator —, the role and its organisation, the authorisation in ILE
  Mono, «valable jusqu'au …»), one hairline between two.
- **5 · what changed** — beside the file from 80rem, under it before: «Où en est votre demande» (W3-D's timeline, the
  owner's wording), «Ce qui vous a été indiqué» (the outcome at the console's scale, the rules version and date, the way
  to its detail, the earlier assessments), and **for the person only** their communications and dates (V4 showed a
  mandated reader its own inbox and dates on somebody else's file).
- two columns from 80rem (the file 2/3, what changed 1/3) with **no inner scroll** (W3-D's O1 — the inspector that
  scrolled inside itself with nothing focusable — is gone with the inspector); one column before.

**The state changes (C-5, C-6) — the row menu and the overlay system's alert dialog.** A line the reader may move (the
object policy, asked per line by the view; the POST asks again) offers its **row menu** — «⋮», a real button, W2-A's
popover, named «Actions» and described by the line (W-3: no two controls share a name and a description), the layer tip
— with one item, «Nouvel état de cette ligne», a link to the line's **alert dialog** (`components/dialog.html`,
`kind="alert"`, the 40 px disc of a consequence): the line in its own language with its state as a chip; **the
consequence named** («Seules les évolutions permises par l'état actuel sont proposées. Chaque changement est
enregistré.» — the dialog's description); the states the line may move to, each a radio and the chip of the state it
leads to — the current one is not offered, so a press never records a change that changes nothing; **«Annuler» the safe
default** (the focus at the opening, Esc presses it, the scrim never closes the dialog), then «Mettre à jour». **The
focus comes back** to the row's «⋮» (`static/js/src/console.js` §2f opens the dialog with the trigger as its opener —
the dialog first, then the menu's close: closed first, the menu gave the focus to «⋮», whose top-layer tip opened inside
the menu's own close and logged «Invalid to show a popover during another show operation»). After the POST the page
returns to the row (`#line-<pk>`, clear of the context bar), which takes the focus, and the page's status region says
«La ligne a été mise à jour.». **The file's state**: one act, «Nouvel état», opening the same dialog family — the moves
the domain permits this reader (`transitions_available`; the person keeps hers: suspend, close), none chosen in advance;
under the closure its consequence, said before the act («Un dossier clôturé ne se rouvre pas : on en ouvre un nouveau.»,
the domain's own sentence, tied to its radio); «Motif» with its rule as the field's help, tied to it (C-6: «La
suspension exige une motivation.», the domain's own words). No bulk edit (C-5: each change of a legal checklist is one
audited act with its author). Without script every item and opener is a link that shows its dialog in place (`:target`),
«Fermer» a link back to the row. The page links W2-A's page-only panels only where a dialog is drawn. **Presenter
changes only**: `portal.services.case_file / case_lines / case_pieces / case_now_panel` (reads), the view's context and
the line's redirect to its row; the permissions, the state machine, the audit trail and the object-permission checks
untouched.

**«Mes dossiers»** (`templates/cases/index.html`) and **the pre-assessment** (`templates/cases/assessment.html`) in the
registers' grammar: the workspace head without an eyebrow; the files as the dashboard's rows (the objective and the
reference in ILE Mono, «Dossier confié — …» for an entrusted file, the count in words, the late lines in the dates'
grammar, the state as a chip, since when; the whole row the way to the file; the mandate's clause once above them); the
pre-assessment's head says its file once on its line of facts (no V4 band — `case_header.html` is gone), the outcome at
the console's scale, its rules version, date and clause, the rules applied as the registers' sequence in their order of
application, the requirements found missing, the sources, **the replay on the page's own ground** (V1's night verso, on
which its text stood at 1.06 : 1 — W3-F1's O4 —, is gone), a divergence said as a warning; the demonstration notice
still before the outcome.

**«Ma situation» counts one total** (W3-D's m4): the counter under the Stepper says «0 question(s) renseignée(s) sur 8»
— the questions the page asks and the ones answered, as the Stepper's eight nodes and the foot's «1 / 8» — where it said
«sur 7» (the fields the rules read). Its two blocks lost three V4 panel classes their own sheet already drew.

### The sheets: v4/workspace.css leaves, the shared payload falls

- **`static/css/v4/workspace.css` leaves the cascade** (the deletion map's last row, «the file»). What other console
  pages still drew of it — the ContextHeader, the workspace head, the actor's glyph disc, the frame's focus ring — moves
  **with its values unchanged** to the console partial `apps/portal/static/portal/v5/_frame.css`, imported last by
  `console.css` (the shell's rules on the heads are the frame's own and more specific, its focus rules are the chrome's,
  the dashboards write none, and no `main.css` focus rule of equal weight reaches the frame — checked —: no tie changes
  hands). Everything else left with the V4 case file: Panel and its gradient edge, the meter and `notch-fill`, the
  ResponsibilityBar, the HealthStrip and `strip-fill` (**the case file moves nothing at load**: W3-D's hand-off closed),
  the dates and threads lists, the compact context bar and its script (`console.js` §2c), the V4 table, the
  intervenants, the state form, the phone's file bar. `components/health_strip.html` goes with its last consumer.
- **The case band and the shell's next action leave**: no page drew them any more — `portal/partials/case_header.html`
  and `next_action.html` are deleted, the shell's two blocks stay empty for the pages that still name them
  (`templates/portal/base_portal.html`), `portal.css` sheds their rules with the pre-assessment's V1 section rhythm,
  title and folio counter (1 504 → 1 045 B).
- **The V1 devices these pages were the last to draw leave `main.css`** (grep-proved on design-v5 and the in-flight
  branches — `v54-intfix`, `v54-sec-f7` —: every other user is a W3-E template already redrawn): the folio
  (`register.css`, `base.css`), the entry's ordinal and its responsible actor, the night verso (`layout.css`).
  `--rubric-on-navy`, `--t-numeral-size`, `--t-numeral-lh` lost their last consumer: reserves in DS 2026 §3.
- **The case file's own CSS** is one page-only sheet, `portal/case.css` (814 B: the two columns, the rows' columns, the
  dialogs' bodies, the phone bar), linked by the case file alone after the registers' sheet and before the journey's,
  which stays last (W3-D's order); W2-A's page-only panels where a dialog is drawn.

### Measures

**CSS (gzip -9, mtime 0; the stewards' `weigh_pages.py` — design-v5 `fec37d3` · this branch before the step `7f7ca9a` →
after):**

| Page type (the sheets it links) | design-v5 | before | after | step 3 |
|---|---:|---:|---:|---:|
| **SHARED** `main.css` — every page | 35 483 | 35 290 | **31 906** | **−3 384** |
| **SHARED** main + console + portal — every console page | 44 196 | 43 572 | **40 140** | **−3 432** |
| the case file, no dialog drawn (+ registers + case + journey) | 46 617 ¹ | 45 993 ¹ | **45 968** | −25 |
| the case file with its dialogs (+ W2-A's overlay panels) | — | — | **48 039** | ² |
| «Mes dossiers», the pre-assessment (shared alone → + registers) | 44 196 | 43 572 | **42 733** | −839 |
| a journey page — the dashboard, «Mon parcours» (+ journey) | 46 617 | 45 993 | 42 561 | −3 432 |
| «Ma situation» (+ situation) | 46 398 | 45 778 | 42 346 | −3 432 |
| the person's registers, the modules (+ registers) | — | 46 165 | 42 733 | −3 432 |
| «Mes pièces» — the register pages (+ documents + panels) | 51 764 | 51 140 | 47 708 | −3 432 |
| the home · the login · a content page | 49 844 · 40 344 · 39 584 | 49 651 · 40 151 · 39 391 | 46 267 · 36 767 · 36 007 | −3 384 |

¹ The case file was «a journey page» (shared + `portal/journey.css`). ² A page that draws a dialog links W2-A's
page-only panels (2 071 B) — the overlay system's rule, CONTRACT §1; the case file draws one where the reader may move a
line or the file (the person on her own lines, the assigned professional, an administrator). Recorded at the page type's
first own sheet. Sheets: `main.css` 31 906, `console.css` 7 189 (+411: `v5/_frame.css`, moved from main.css),
`portal.css` 1 045, `portal/case.css` 814 (new), `portal/registers.css` 2 593, `portal/journey.css` 2 421. **Both shared
bundles fall; every page type is lighter but the case file with its dialogs.**

**The load check** (V5.8 rule 2's performance sanity check; the lane, the tree before the step on the twin port 8796
against this branch on 8785, interleaved blocks BASE / HEAD, a fresh context with the cache disabled, CPU × 4, no
network throttling — the dev server's uncompressed files —, n = 5 after a warm-up, medians; `E/perf/loadcheck.json`):

| Cell | LCP | FCP | CLS max | longest task before LCP | elements |
|---|---|---|---|---|---|
| the person — fr 1440 | 604 → 536 ms | 360 → 404 | 0 → 0 | 249 → 0 | 834 → 1 111 |
| the person — fr 412 | 424 → 548 | 380 → 412 | 0 → 0 | 0 → 145 | 834 → 1 111 |
| the professional — ar 1440 | 508 → 516 | 364 → 384 | 0 → 0.0005 | 0 → 136 | 861 → 1 258 |

LCP signs mixed inside the machine's spread (W3-D measured its speed moving 2.2× between loads), FCP +20 to +44 ms
(three more stylesheets, uncompressed, on the dev server's HTTP/1.1), CLS ≈ 0, the LCP element the NowPanel's title (V4:
a panel's text): **no meaningful LCP or first-render regression.** The DOM grows with the rows' menus and the dialogs
laid out in advance (W2-A's INP rule: «each dialog is laid out in advance»): 1 258 elements for the professional, under
Lighthouse's 1 400.

**Smoke** (`E/s3/`, 56 loads, every capture looked at — through labelled contact sheets and full-size crops): the case
file for the person and the professional at 1440 · 1280 · 1100 · 390 · 360, fr and ar; `qa-person`'s and `seed-person`'s
files, the administrator's view, «Mes dossiers» (entrusted, empty, the person's), the pre-assessment, «Ma situation»,
«Mon parcours» and the dashboard at 1440 and 390, fr and ar — **all 200, 0 console error, 0 CSP report, 0 horizontal
overflow, one h1 each.** «Ma situation» captured again once the one total was served (`E/s3b/`, fr and ar at 1440 and
390: «0 question(s) renseignée(s) sur 8» under the eight nodes and «1 / 8»; 0 console error, 0 CSP report). Corners on
the case file: the NowPanel's 8, the controls' 4, the chips' and discs' full — three; one raised plane and its one
shadow value. Before: `E/before/` (the V4 composition: five panels, the eyebrow, the table with a select per row, the
inspector's inner scroll, the professional told «Votre prochaine action»).

**The interactions** (`E/i1/`, headless Chromium, fr 1440 and ar 390, with and without script): see DL54-143 — the menu
on Enter with the focus on its item, the alert dialog (described, `aria-modal`, the focus on «Annuler»), the trap over
ten Tabs, Esc and the focus back on «⋮», the scrim that never closes it, the POST on `#line-<pk>` with the focus on the
row and the status region's sentence, the file's dialog and its closure's consequence tied, the dialog in place without
script; 0 console errors, 0 duplicate ids (a duplicate id between the closure's radio and its hint was found by this run
and fixed).

### Identity carriers and the swap test (plan §3.1 item 7)

| Screen | Carriers named | Swap test (`E/swap3/`) |
|---|---|---|
| the case file (person, professional) | «La soglia» — the spine, threshold A's stamp and threshold B's arch, «Vous êtes ici»; «i cerchi» (every line's and piece's chip, the timeline's); «il registro» (the ledger's marks, coloured by the group); the references in ILE Mono (the file, the sources, the authorisation); the actors' glyphs; the NowPanel; the L2 key in a dialog's submit | passes on the journey and the chips |
| «Mes dossiers» | «i cerchi» (the file's phase chip with its gauge), the references in ILE Mono, the dates' azione grammar | passes on the chips |
| the pre-assessment | the outcome's state rule, the rules' places and ids in ILE Mono, the clause's voice | weak at rest — a reasoned document; the references and the chip in the head carry it |

### Tests

On `test_ile_v5_l5`, one pytest of mine at a time (a browser file its one headless Chromium; the benchmark lock checked
before each browser series; no run ended on a crash):

- **the domains the case file reads** — `apps/cases`, `apps/portal` (its browser file below),
  `tests/test_phase_console.py`, `tests/security` (the object-permission and authorisation audits): **465 passed, 3
  skipped**; after the last changes (the one total's test, the presenters' file trimmed) `apps/cases` and
  `test_situation.py` again, below.
- **the other secondary pages' apps** — `apps/companies`, `academy`, `helpdesk`, `selection`, `forum`, `notifications`:
  **664 passed**.
- **the frontend's and the languages' gates** (not in the browser) — the whole of `tests/frontend` with
  `tests/i18n/test_rtl_static.py` once the step's code stood: 650 passed and 18 failed, then 712 passed, 1 xfailed and 4
  failed — each corrected and re-run green (a pin retargeted with its intent, listed below; the console's import order:
  W3-B's partial right after the shell, `v5/_frame.css` last; a W3-C test's substring in a comment; three orphaned
  tokens recorded as DS 2026 reserves; the inventory regenerated) but design-v5's own comment red (fixed later, below).
  After the last changes, the gates the task names and every file the step touched —
  `test_template_comments_do_not_leak`, `test_journey_w3_d`, `test_design_docs`, `test_chips_registry`,
  `test_state_chips_carry_a_register`, `test_o14_lint`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`,
  `test_static_pipeline`, `test_dashboard_w3_b`, `test_depot_w3_c`, `test_documents_w3_c`, `test_overlays`,
  `test_icons`, `test_console_shell_w3_a`, `tests/i18n/test_rtl_static.py` and `test_catalogues.py`,
  `tests/test_regen_design_inventory.py`, `tests/test_check_ownership.py`, `apps/cases`,
  `apps/portal/tests/test_situation.py`: **874 passed, 3 skipped** (the three of `apps/cases/tests/test_intake.py` that
  need a rule in force — none is). (A full re-run of `tests/frontend` and `tests/i18n` was stopped at 18 %: on a machine
  shared with two other lanes' runs it moved at 0.4 test a second. Every string the step's templates draw is in the four
  compiled catalogues — checked.)
- **in the browser** — `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py`,
  `test_journey_browser_w3_d.py` and W3-A's two action-bar tests on a phone: **46 passed**;
  `test_overlays_console_browser_w2_a.py`, `test_console_shell_browser_w3_a.py`, `test_console_phone_browser_w3_a.py`,
  `test_dashboard_browser_w3_b.py`, `test_documents_browser_w3_c.py`: **131 passed, 1 failed** — W3-A's
  `test_menu_is_reached_in_three_keys_and_opens_a_drawer_that_holds_the_whole_rail`: the press on the scrim after a
  keyboard reopen leaves the drawer open — W2-A's intermittent defect, design-v5's own and handed over (DL54-102 item
  10: «2 runs of 3 alone on either tree»; W2-A's and W2-C2's SHIPPED notes); here it failed in the batch and in a re-run
  of its file (28 passed), and passed alone and after its four neighbours (7 passed). The drawer's code, the scrim and
  `overlay.js` are untouched by this step (`console.js` gains §2f, a click listener that acts on a line's menu item
  only, and loses §2c; the requests page the test opens draws nothing of the case file).
- Retargeted, intent kept: eight tests in six files (listed under «Paths outside the slice»), each pinning a rule that
  moved (W3-B's and W3-C's legacy rules now read on `v5/_frame.css`; `v4/workspace.css` gone; the register entry's kept
  classes; the RTL scanner's sheet list). Added: «Ma situation» counts one total
  (`apps/portal/tests/test_situation.py`).

### The items handed to W3-E for step 3 — answers

| From | Item | Answer |
|---|---|---|
| W2-A NOTES l.183, l.281, l.738, SHIPPED l.160 | the staff consequence dialogs on the modal (`components/dialog.html`, `kind="alert"`, the page-only panels) | **done** — the lines' and the file's alert dialogs (DL54-143); the panels linked only where a dialog is drawn |
| W3-A NOTES l.328 | the case file's phone action bar is the shell's contract | **done** — `data-file-action-bar`, the NowPanel's primary; W3-A's phone test passes |
| W3-B NOTES (Panel, ContextHeader, HealthStrip «leave v4/workspace.css with their last consumers»; the case file's section) | — | **done** — the file is gone; the ContextHeader moved to `v5/_frame.css` (the dashboards draw it) |
| W3-C NOTES l.99 | the hatch stays on the case file | **gone with the HealthStrip** — no hatch is drawn on the case file; the chips' dashed attesa edge says it |
| W3-C NOTES l.198, l.252, l.429, l.578 | the case file's band (`case_header.html`), the HealthStrip's last consumer | **done** — both deleted |
| W3-D NOTES «Handed to» | m4 — «Ma situation» counts three ways | **done** — one total (DL54-145) |
| W3-D NOTES «Handed to» | O1 — the inspector scrolls inside itself with nothing focusable | **gone** — the side column does not scroll inside itself |
| W3-D NOTES «For W3-E · W3-C» | the case file's HealthStrip still plays `strip-fill` at load | **gone** — nothing moves at load on the case file |
| W3-D NOTES «Handed to» | keep the three links W3-D wrote into W3-E's templates | **kept** — `portal/journey.css` in `cases/detail.html` (last) and `portal/pathways.html` (last), `portal/situation.css` in `portal/situation.html` |
| W3-F1 NOTES l.304 | `.section--verso > .t-prose` at 1.06 : 1 on the case's pre-assessment | **done** — the replay on the page's own ground; the verso's rules left `layout.css` |
| step 2 | the case file and the last of `v4/workspace.css`; `cases/assessment.html` the last reader of `portal-section`, `portal__section-title` and the folio counter | **done** — all deleted |

### Paths outside the slice (step 3, for the merge step's manifest)

`apps/cases/views.py` (the detail's context — presenter reads — and the line's redirect to its row; W3-B's two `reader=`
arguments kept); `apps/cases/presenters.py` (the dead `checklist_health` out; W3-D's two functions untouched);
`apps/portal/views.py` («Ma situation»'s one total); `apps/portal/static/portal/portal.css` (the case band's, the next
action's and the pre-assessment's dead rules); `apps/portal/static/portal/v5/_frame.css`, `case.css`, `v5/_case.css`
(new: the frame's console partial — its import line in `console.css` is this family's —, the case file's page-only
sheet); `static/js/src/console.js` (§2f, the row menu's dialog opener, in a second import line that keeps W2-A's and
W3-A's pinned one; §2c, the V4 compact bar's script, out); `templates/portal/base_portal.html` (W3-A's: the two blocks
empty); `templates/components/health_strip.html` (deleted) and `templates/dev/showcase.html` (its sample out; W3-D's
four-line comment a block comment); `apps/portal/tests/test_situation.py` (the one total's test, added);
`static/css/register.css`, `base.css`, `layout.css` (the V1 devices left without a reader — W4-D's sweep, done for these
rows); tests retargeted, intent kept: `tests/frontend/test_dashboard_w3_b.py` (W3-B's legacy rules read on
`_frame.css`), `test_depot_w3_c.py` (lateness on the legacy sheets; the register entry's kept classes),
`test_documents_w3_c.py` (the register's legacy rules; the runs' ring above the frame's ring), `test_journey_w3_d.py`,
`test_overlays.py` (W2-A's row popover), `tests/i18n/test_rtl_static.py` (the scanner's sheet list); DS 2026 (§2.1's
rows, §3's three reserves, §8.2's note, §10's glyph / form_field / page_header lines and health_strip's section, §11.10,
§12's note; §2's and §10's figures by `scripts/regen_design_inventory.py`). Steps 1 and 2's paths stand.

### Seen on the way — other areas'

- **design-v5's own red, fixed here**: `tests/frontend/test_template_comments_do_not_leak.py` failed on
  `templates/dev/showcase.html:21` — a `{# … #}` comment over four lines (W3-D's showcase link comment, on design-v5
  since the w3-d merge), whose text rendered into the showcase; it is a `{% comment %}` now, words unchanged (the file
  is already in this family's diff).
- **design-v5 moved** since `7f7ca9a` (the sec-f5 merge and its steward's DL54-130; `intfix-merge` held the merge lock
  at this step's end): this family's DL54-130 … 146 are renumbered at the merge, as step 2's notes said.
- **The dev showcase** draws the V4 case file's samples (the ContextHeader with its meter, the compact bar, the
  ResponsibilityBar, the V4 table, the intervenants, the file bar) and the company's V4 facts: their rules left with
  their pages (this step and W3-B's), the samples stand unstyled. The showcase's owner (the steward's to assign) retires
  them; `companies/partials/need_table.html` (no product page) with them.
- **sec-f7** (in flight): its NowPanel variant «suspended» says a suspended file's reason; the case file draws the
  reason as a notice under its head — when sec-f7 lands, one of the two goes (the dashboard's rule: drawn in the
  NowPanel only). Its narrower `transitions_available` feeds the file's dialog unchanged.
- **The administrator** reading a file is told «Vous y accédez au titre d'un mandat daté» — V4's sentence for every
  non-owner; an administrator holds no mandate. New words would be B1's.
- `companies/services.py`'s `next_action` docstring still names `portal/partials/next_action.html` (deleted): the
  companies module's line to update.

### Left, and for others

- **B1 item 4** — step 1's words not drawn stand (a deadline's distance; a heading over the pre-assessments); C-1
  («since your last visit», a stored `last_seen_at`) and C-2 (the timeline's own title) are the owner's (U8, U9): not
  drawn.
- **The showcase's owner** — the V4 samples above.
- **W2-A** — the drawer's scrim press after a keyboard reopen (DL54-102 item 10), seen again in this step's runs.
- **The merge step** — the paths outside the slice into the manifest (above, and steps 1 and 2's; `check_ownership.py
  w3-e design-v5` at this step's last code commit: 58 inside, 12 slice, 29 generated, 30 outside → FAIL until the
  manifest names them); this family's decision-log entries renumbered after design-v5's DL54-130; the JS bundles rebuilt
  on design-v5 (esbuild names the chunks after the worktree's path: this branch's names differ from design-v5's, the
  code does not).
- **The notification centre** — step 1's note stands (a view returning the latest communications as a fragment).

**The lane at the step's end.** The case file's lane-only data removed from `ile_v5_l5` (`seed_case.py remove`: the five
«[w3e]» lines, the sixteen timeline events their changes wrote — the seeding's and the interaction runs' —, the
communication and the two dates; the reference case `EE167596D4` back to its three pieces, no line, its state as found —
«Brouillon», no transition was ever submitted —, its trail back to its two events), the six sessions revoked and their
secrets file deleted, the lane server on 8785 stopped; step 1's «[w3e]» communications and dates for `qa-person` stay
(step 2's note). To draw the case file's lines again on lane 5: `seed_case.py add` in
`C:/tmp/ile_v5_council/.work/w3-e/w3-e-impl-3/` (and `remove` after), then `sessions.py mint`.

## Review fixes (implementer w3-e-fix, 16 October 2026)

The fix pass of the senior review (`REVIEW.md`, `6699bc7`: SHIP_AFTER_FIXES, four majors, eleven minors) and of the
accessibility/performance check (`A11Y_PERF.md`, `2fa57d0`: one major, five minors). V5.5: every major fixed, every
minor fixed or handed on with its reason (below). Decision log: **DL54-147** (renumbered at the merge with the rest of
the family's entries).

**Lane.** Lane 5: dev server 8785 from this worktree on `ile_v5_l5` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag; restarted after every template change), pytest on `test_ile_v5_l5`,
one pytest and one headless Chromium of mine at a time, its own profile (`C:/tmp/ile_v5_council/.profiles/w3-e-fix/`).
Sessions minted with `Client.force_login` (no password used, typed or stored): `qa-doc-person`, `demo-professionnel`,
`qa-admin`, `qa-person`, `seed-actor`, `qa-company`, `seed-person`. The benchmark lock was checked before every series
(never present). No browser run ended on a crash. Lane data: the reference case `EE167596D4` drawn with five lane-only
lines tagged «[w3ef]» (w3-e-impl-3's seed, retagged): the next action is then a checklist line, the case M2 is about.
Never 8780, 8782, Chrome 9222 / 9223. Scratch: `C:/tmp/ile_v5_council/.work/w3-e/w3-e-fix/`; evidence:
`C:/tmp/ile_v5_council/evidence/v54/w3-e/fix/` (`case1/`, `c5/`, `c5p/`, `pages1/`, `pages2/`, `align/`, `forced/`,
`interact/`, `post/`, `final/`, `final-disc/`).

### The majors

| Item | Fix | Measured |
|---|---|---|
| **M1 · LA-9** — the case file's first screen held no act | The journey is drawn in W3-D's **compact forms** (`descriptive` off): the level line where its column holds 56rem, else the card — the current step, its rank, «Vous êtes ici» — and the spine behind the disclosure, closed; its words «Où j'en suis» for the person, «Parcours» for a mandated reader (nobody's voice; both in the catalogue). The dated history is the feed's («Où en est votre demande»), beside it | the journey 460–521 → 162–166 px; the NowPanel's title y 762 → **464** and its primary y 895 → **657–701** at 1366 × 768 (within 768), 1280 × 800 and 1440 × 900 likewise; at 360 × 800 the title at y 428–484, the bar's top at 739: clear (`case1/`) |
| **M2** — the next line drawn twice; «Continuer» scrolled to the copy | `portal.services.case_file` draws the NowPanel's line **once**: `asked_lines` skips it in «Exigences» (the pieces' rule), the count «n sur m» stays the file's; `case_now_panel(…, line=…)` gives the panel what the row said — the team's note beside who answers, the source («Fondement», ILE Mono) — and the line's id on its wrapper (`<div class="file-now" id="line-<pk>" tabindex="-1">`: the POST and the dialog's «Fermer» return there). Its act is **the line's alert dialog** (`href="#line-<pk>-state" data-overlay-open`; «Nouvel état de cette ligne», no arrow: it goes nowhere): the person's primary and the phone's bar where the policy lets her move it; a mandated reader's quiet secondary where it lets them; nothing where it does not. W3-B's partial gains the `overlay` flag and the `source` fact (its one-primary pin kept: one `btn--primary` a branch) | the line once (`lineIds`: `line-21:file-now`); the dialog opens on Enter from the primary, the bar and the secondary — `alertdialog`, `aria-modal`, described by the line, the focus on «Annuler», Tab 10/10 inside, the scrim keeps it, Esc closes it and the focus is back on the opener, fr 1440 and ar 390 (`interact/`); the POST returns to the panel's wrapper while the line stays the next action, to its row in «Exigences» once settled, the focus there and «La ligne a été mise à jour.» (`post/`) |
| **M3** — the history said «Vous» to a mandated reader | `cases.presenters.timeline(case, reader=…)` (W3-D's presenter: a justified extra path): the person's acts are «Vous» for the person only, «La personne» (`ResponsibleActor.PERSON`) for anybody else; nobody is «Vous» without a reader. The view passes `request.user` | the professional and the administrator read «La personne», the person «Vous» (`case1/`); tests |
| **M4** — irreversible closures were one-press submits | The guichet's «Clore la demande» (the person and the appointed professional) and the selection's «Clore le processus» (the authorised actor) are **one act on the page that opens the overlay system's alert dialog** (`templates/helpdesk/partials/close_dialog.html`, `templates/selection/partials/conclude_dialog.html`): the consequence said before the act and as the dialog's description (the domain's own sentences: «Une demande close n'est pas rouverte : une nouvelle demande est ouverte.», «Un processus clos ne se rouvre pas.»), the reason inside — the selection's outcome as radios, **none chosen in advance** (the select preselected the first outcome of an irreversible act) —, «Annuler» `data-overlay-safe`, the act in the garnet outline (`btn--danger`). The pages link W2-A's page-only panels only where they draw one. One dialog body for the family's acts: `.reg-dialog` in the registers' sheet (the case file's `.file-dialog` grid moved there — the second family to draw a component consolidates) | the same contract on the three dialogs, fr 1440 and ar 390 (the phone's bottom sheet); without script the act shows the dialog in place (`:target`) (`interact/`) |

**The selection's evidence table** (a select and «Mettre à jour» on every row, the V4 pattern C-5 retired on the case
file): recorded as the staff's design debt, beside the dispatch desk (below) — the review's own alternative.

### The minors

| # | Item | Done |
|---|---|---|
| 1 | a wrapped line of facts left «·» at a line's end | Fixed: each part opens with its point in a box the gap's width, pulled into the gap; the first part of every line pulls its point out of the line's box, which clips it (`overflow-x: clip` — both inline edges, the same in both directions; the block axis visible). A state's chip in such a line stands in a span of its own (the selection's decisions), so no point is drawn in its edge and no sheet but the chip's paints `.chip` (W1-C's pin). Needs, Academy, «Mes dossiers», the queue: no line ends or opens on a point, fr and ar, 1440 and 390 (`pages1/`) |
| 2 | the case rows' «⋮» floated with the words on a phone | Fixed with the a11y check's finding 2: the trigger is the system's icon control (`inline-size: var(--btn-h-icon)`: 40 × 40, 44 × 44 for a finger) in a column of its own at the row's inline end below 48rem — the state and the date on the line under the words; x 330 on every row at 390, x 16 in Arabic (`case1/`) |
| 3 | the Academy's domain filter took five rows at 390 | Fixed: under 52rem the registers' filter is one row that scrolls along its hairline (the cut-off entry says there is more; focus brings an entry into view); the first course at y 278 at 390 (`pages1/`) |
| 4 | the pre-assessment's two sections ran at 1 130 px | Fixed: a section's sentence and its sources hold the reading measure (`.reg-sec > :is(.db-empty, .sources)`, 36rem): 576 px (`pages1/`) |
| 5 | the feed: «Ligne mise à jour» without its line; long chips on two lines | Fixed: a line's change names the line in its own words (the trail's `item`, the file's checklist; its language when it is not the page's, `dir="auto"`); from 80rem the date heads its event in the side column, which takes the column's width: «Phase gérée par un acteur autorisé» 44 → 24 px tall at 1280–1440, fr and ar (`c5/`, `pages2/`) |
| 6 | RTL: the note's «—» inside the isolate; a wrapped French h1 aligned left | Fixed: the dash outside the `dir="auto"` span; one rule for a title in the other direction than the page — its lines on the page's reading edge, wrapped or not (`:dir(rtl) …:dir(ltr) { text-align: end }` and its mirror: the head's title, a row's title, the feed's line): the guichet's wrapped French subject now stands right on an Arabic page, as the dates' titles (`align/`) |
| 7 | voice on a mandated reader's screen | Handed to **B1** (new words are the owner's) — added to the copy packet below |
| 8 | one counter per event | The rail's «Communications (2)» is W3-A's (handed on: «a dot on the rail», D17). The guichet's band («5 demandes en cours.») has no figureless string in the catalogue to draw the figure apart: **B1**, below |
| 9 | states off the chip grammar | Fixed: `academy.PlanStatus` has a producer (`core.chips`: draft attesa, active neutro, completed conforme, archived nullo — a justified extra path, as step 1's three) and «Mes formations» and the plan draw it as a chip. «Réponse disponible» in azione for the professional (a reader with nothing to do): the registry is per state — handed to **W1-C** (a per-audience register question) |
| 10 | swap test: two screens carried nothing at rest | Fixed: the guichet's opening form carries the person's own seal beside its promise (the seal that heads the person's turns in the exchange the request opens); the pre-assessment's outcome carries its journey phase's glyph («La soglia»'s «Pré-évaluation et parcours possibles» — the section's glyph on the dashboard and the case file), through the registry (`concept`) |
| 11 | at the merge: sec-f7's NowPanel draws a held file's reason | Prepared here, so the merge keeps one: the case file draws its suspension notice only when the NowPanel does not draw the reason (`now.variant != "suspended"`); `case_now_panel` reads sec-f7's variants by value (`HELD_NOW_VARIANTS`) — on the file's own page never the way to that page («Votre dossier»), the person's act (the questionnaire) for the person only, a mandated reader addressed as «Dossier». Before the merge `now_panel` never returns them and nothing changes; a test covers the held panel |

### The accessibility/performance check's findings

| # | Finding | Done |
|---|---|---|
| 1 | **major** — a draft need's head scrolled sideways at 320–375 (WCAG 1.4.10) | Fixed as advised: `.reg-head .ws-head__action { flex: 1 1 100%; min-inline-size: 0 }` below 48rem (the registers' page-only sheet): the head's acts are the line's width — 288 / 328 / 343 px at 320 / 360 / 375, both buttons stacked, fr and ar, 0 overflow (`pages1/`, `final/`) |
| 2 | the «⋮» drawn 22 px wide (the one axe violation) | Fixed: `inline-size: var(--btn-h-icon)` — 40 × 40 at 1440, 44 × 44 at 390 (`case1/`) |
| 3 | under forced colours a row link's ring lost its bottom edge | Fixed as advised: 6 px under a row's title in forced colours only; the bottom band drawn over the whole ring, needs and communications (`forced/`) |
| 4 | two landmarks with one name on the Academy plan | Fixed: the scroll region is named by the table's caption (`aria-labelledby="t-plan-gap"`) |
| 5 | «Voir le programme complet» 22 px tall on a phone | Fixed: the page's `db-link` (44 px for a finger): 44 px at 390 (`pages1/`) |
| 6 | budget letter: the case file links seven stylesheets | Recorded (nothing to ship): 7 + 9 requests before `load` on the case file, W3-E's share three (the registers', the case's, W2-A's panels where a dialog is drawn); the guichet's request and the selection's process now link the panels too where they draw the closure (one request). The one-sheet variant (one request less, 2.6 KB not reused from cache) is W4-C's call |

### Measures

**CSS** (gzip -9, mtime 0; the dist rebuilt — `npm run build:css`; this branch before the pass `2fa57d0` → after):
`main.css` 31 906 → **31 906 B**, `console.css` 7 189 → 7 189, `portal.css` 1 045 → 1 045 — **the shared bundles
unchanged** (main + console + portal 40 140 B on every console page). Page-only: `portal/registers.css` 2 593 → 2 875 B
(+282: the dialogs' one body, the separators, the filter's row, the alignment rule, the carriers, the head's acts on a
phone, the forced-colours room, the reading measure), `portal/case.css` 814 → 955 B (+141: the panel's wrapper, the
phone's row, the feed in the side column). Page types: the case file 45 968 → 46 391 B, **48 039 → 48 462 B** where it
draws its dialogs; the registers' pages 42 733 → 43 015; the guichet 42 995 → 43 277 B (45 348 B on an open request's
page, with W2-A's panels); the selection 43 196 → 43 478 B (45 549 on the actor's process page). Nothing moves at load
(no keyframe, transition or will-change added).

**Smoke** (`final/`, 98 loads — the case file for the person, the professional, the administrator, `qa-person`'s and
`seed-person`'s files; «Mes dossiers», the pre-assessment, the dashboard; the guichet (requests, a request for the person
and the professional, the queue, the opening form); the selection's process and decisions; the Academy (catalogue,
mine, the plan, a follow-up); the company's needs and a draft need; «Mes échéances», «Communications» — fr and ar at 1440
and 390, the draft need at 320 / 360 / 375): **all 200, 0 console error, 0 CSP report, 0 horizontal overflow, 0
duplicate id, one h1 each** (a duplicate id between the closures' sections and their dialogs' titles, found by the
first series, was fixed: the dialogs are `desk-close-dialog` and `conclude-dialog`). Every capture looked at.

### Tests

On `test_ile_v5_l5`, one pytest of mine at a time:
- **new**: `tests/frontend/test_case_file_w3_e.py` (the family's per-family file) — the compact journey and its order,
  the mandated reader's disclosure, the line drawn once with its source and its act on its dialog, the mandated reader's
  secondary, a line the reader may not move, the line's matching, the held file's panel (both readers), the reason drawn
  once, the history's voice and the line it names, the presenter without a reader, the guichet's closure dialog and its
  absence on a closed request, the selection's closure dialog (its own chain: the demonstration seed is off in tests),
  the plan's chip and region, and the sheets' fixes — **21 passed**;
- **retargeted, intent kept**: W3-D's `test_journey_w3_d.py` (the case file draws the compact rail; a file off the line
  says «here» nowhere — neither the card nor the list; the case file's timeline modifier allowed beside the partials:
  columns and alignment, no drawing) and `test_journey_browser_w3_d.py` (the case file's journey compact at 1440, opened
  the spine, the latest event lit); `apps/helpdesk/tests/test_compliance.py` (a fragment under `partials/` is not a
  page);
- five reds met on the way and fixed at their root: W3-B's one-primary pin (the overlay opener folded into the one
  `{% elif now.primary %}` branch), W1-C's one-sheet pin (`:not(.chip)` left the separators' selectors: the chip stands
  in a span of its own), the tokens' gate (the timeline modifier no longer reads W3-D's `--node`), the icons' literal
  gate (the outcome's glyph resolved through `concept` in a `with`), the helpdesk's shell test (above);
- **the final targeted set at the pass's last code** — the new file and W3-D's, the frontend and languages gates the
  pass touches (`test_chips_registry`, `test_chips_cards_w1_c`, `test_state_chips_carry_a_register`, `test_overlays`,
  `test_overlays_console_w2_a`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`,
  `test_template_comments_do_not_leak`, `test_dashboard_w3_b`, `test_o14_lint`, `test_design_docs`,
  `test_static_pipeline`, `test_console_shell_w3_a`, `test_icons`, `test_depot_w3_c`, `test_documents_w3_c`,
  `test_design_showcase`, `tests/i18n/test_rtl_static.py`, `test_catalogues.py`, `test_ui_translations.py`), the apps
  it touches (`apps/cases`, `apps/helpdesk`, `apps/selection`, `apps/academy`, `apps/portal` but its browser file) and
  `tests/security`: **1 523 passed, 3 skipped** (`apps/cases/tests/test_intake.py`: no rule in force), **1 xfailed**
  (the showcase's captions, design-v5's own strict marker);
- **in the browser**: `test_journey_browser_w3_d.py`, `apps/portal/tests/test_browser.py` and W3-A's case-file action
  bar test on a phone: **22 passed** (no crash).

### Paths outside the slice (the fix pass, for the merge step's manifest)

`apps/cases/presenters.py` (`timeline(case, reader=…)` and the line a change names — W3-D's presenter slice, M3);
`apps/cases/views.py` (the reader passed); `apps/core/chips.py` (`academy.PlanStatus`'s producer) with
`tests/frontend/test_chips_registry.py` (its enum); `templates/components/case_timeline.html` (**new**: W3-D's component —
the line's words with their language and `dir="auto"`, its contract); `templates/portal/partials/now_panel.html` (W3-B's
partial: the `overlay` opener in the one primary's branch and on the secondary, the `source` fact; listed «slice»);
`apps/helpdesk/tests/test_compliance.py` (**new**: a fragment is not a page); `tests/frontend/test_journey_w3_d.py` and
`tests/frontend/test_journey_browser_w3_d.py` (**new**) (retargeted, above). `check_ownership.py w3-e design-v5
--working-tree` at the pass's end: 63 inside, 13 slice, 29 generated, **33 outside** → FAIL until the manifest names
them (steps 1–3's thirty and these three). Inside the slice: `templates/{cases,helpdesk,selection,academy}/**` (the two
dialogs' partials are new), `apps/portal/services.py` (its presenters), the registers' and the case file's page-only
sheets with their dist, DS 2026 §11.10's prose, the decision log's DL54-147, the new test file.

### Handed on

- **B1 — the copy packet** (new words are the owner's), added to step 1's list: on a mandated reader's screen of the
  case file «Vous êtes ici» (the journey card), «Où en est votre demande» (the feed's title), «Ce qui vous a été
  indiqué» (the assessment's title), the assessment's empty sentence («… lorsque vous terminez le questionnaire»), the
  «Exigences» lead («… toutes ne vous incombent pas»), and «au titre d'un mandat daté» shown to an administrator who
  holds no mandate; the guichet's band as a figure — a string without the count («demande en cours» /
  «demandes en cours»), so the band draws its figure as the other registers do.
- **W3-A** — the rail's «Communications (n)» beside the band's count (D17: «a dot on the rail»).
- **W1-C** — the registry is per state, not per audience: «Réponse disponible» reads azione for the professional, who
  has nothing to do.
- **W3-D / W4-D** — the journey component's `descriptive` variant has no consumer now (its rules in
  `v5/_journey-rail.css`, the comments of `portal/journey.css`, `_journey-rail.css` and `journey_rail.html` still name
  the case file): keep it or sweep it.
- **The staff's design debt** (beside the dispatch desk, step 2's list): the selection's evidence table — a select and
  «Mettre à jour» a row — wants the row menu and the alert dialog the case file's lines have (C-5), when the staff's
  surface is next touched.
- **The merge step** — design-v5 has moved (sec-f5, intfix, sec-f7): sec-f7's held NowPanel meets this branch in
  `apps/portal/services.py` (`now_panel`, `_held_now`) — the case file reads its variants by value and draws the reason
  once (minor 11, prepared); the decision log's DL54-130 … 147 renumbered after design-v5's; the manifest's 33 paths;
  the JS bundles unchanged by this pass.

**The lane at the pass's end.** The lane-only «[w3ef]» data removed from `ile_v5_l5` (`seed_case.py remove`: the five
lines, their status events — the seed's and the pass's two POSTs —, the communication and the two dates; `EE167596D4`
back to its three pieces, no line, «Brouillon»), the seven sessions revoked and their secrets file deleted, the lane
server on 8785 stopped, no browser of this pass left running.

## At the merge (the steward, 16 October 2026)

The steward's merge step (`w3-e-merge`, under `C:/tmp/ile_locks/DESIGN_V5_MERGE_LOCK`, taken at 05:41:42 once the tag
`v54/w3-d` stood on design-v5) on lane 5: `TEST_DATABASE_URL=…/test_ile_v5_l5`, one pytest and one headless Chromium at
a time, no run crashed; no lane server started, no persona used on the lane. Nothing deployed, nothing pushed, no
production touched. Logs: `C:/tmp/ile_v5_council/evidence/v54/w3-e/merge/`.

- **The sync** (`dcf11a2`). design-v5 had moved from `fec37d3` to `11070b5`: 63 commits — the sec-f5 merge and its
  record DL54-130, integration checkpoint 3 (the intfix merge, its rebuild, DL54-131, the changelog line), the sec-f7
  merge and its record DL54-132, the private-root probe's test. Two conflicts: the decision log and `static/js/dist`
  (rebuilt). `apps/portal/services.py`, DS 2026 and the design showcase merged on their own and were read: sec-f7's held
  NowPanel (`held_case`, `now_panel`'s two held variants, `_held_now`) stands beside `case_now_panel`, which reads its
  variants (minor 11, prepared here); DS 2026 §11.7 (sec-f7) beside §11.10; the showcase's comment was the same fix on
  both sides. Where the two areas meet the steward wrote two lines (`398590e`): `_held_now`'s docstring named the case
  band this family deleted — it names the case file's page —, and `HELD_NOW_VARIANTS` reads sec-f7's constants.
- **The decision log's numbers.** design-v5 took DL54-130 … DL54-132 while this branch held DL54-130 … DL54-147, so the
  family's eighteen entries are **DL54-133 … DL54-150** on design-v5 (add 3 — headings, index rows and the
  cross-references between them; checked both ways). These notes, `REVIEW.md` and `A11Y_PERF.md` keep the numbers they
  were written with: read DL54-130 … DL54-147 above as DL54-133 … DL54-150 (step 1's DL54-130 … DL54-136 → DL54-133 …
  DL54-139; step 2's DL54-137 … DL54-141 → DL54-140 … DL54-144; step 3's DL54-142 … DL54-146 → DL54-145 … DL54-149; the
  fix pass's DL54-147 → DL54-150). The merge's record is DL54-151.
- **The semantic conflict the run found** (`ab0a79a`): sec-f7's `apps/cases/tests/test_transition_actors.py` read the
  case page's moves as V4's select options; this family's case file draws them as the radios of the file's state dialog.
  Ten cases of `test_the_case_page_offers_exactly_what_its_view_accepts` failed (the page «offered» nothing) and an
  absence check would have passed on nothing: both read the dialog's form now (`_moves_on_the_page`), the second with
  the closure asserted beside the absent move — intent kept, nothing weakened.
- **Ownership** (`c8859fc`, `6518c78`). The 33 paths outside the slice the notes declare (steps 1–3 and the fix pass),
  each read in the diff, assigned to w3-e with its reason and its owner: four whole-file entries (the five new sheets,
  `components/health_strip.html` retired) and 27 slices; then the merge's one retargeted test (a slice of sec-f7's
  file). Two slices named as written (`apps/portal/services.py`, DS 2026). `check_ownership.py w3-e design-v5`: 69
  inside, 41 slice, 32 generated, and the manifest itself, the one steward-only path (before: 33 outside); `--validate`:
  coherent, 29 families, 730 entries.
- **The bundles.** Both dist trees deleted and rebuilt from clean (`npm run build`): byte for byte the committed ones.
  The shared CSS gate (V5.8, `gzip -9`, mtime 0; `budget_gate_branch.log`): `main.css` 35 483 → **31 906 B** on every
  page, the console page types 44 196 → **40 140 B**; the page types that draw a dialog grow by W2-A's panels only where
  they draw one (the case file 46 617 → 48 462 B, an open request 45 071 → 45 348 B, the actor's process 45 281 → 45 549
  B), every other page type lighter; the JS unchanged in weight. DL54-151 records the table.
- **Tests on the merged branch**: non-browser (`-m "not browser"`, 16 min 17 s) — `apps/cases` (183), `apps/portal`
  (216), `apps/companies` (99), `apps/academy` (81), `apps/helpdesk` (94), `apps/selection` (86), `apps/forum` (213, the
  governance's among them), `apps/notifications` (95), `tests/test_phase_console.py` (8), `tests/security` (157: the
  object-permission and authorisation audits, the confidential-material guard among them), the chip registry and the
  state chips' register (34 + 147), `test_o14_lint` (53), `test_design_docs` (40), both bundle-current tests (5 + 3),
  `test_static_pipeline` (3, a real `collectstatic`), this family's file (21) and the files it retargeted or reads
  (W3-D's journey 41, W3-A's shell 58 + 2, W3-B's dashboard 60, W3-C's 28 + 41, W2-A's overlays 38 + 7, W1-C's chips 17,
  the icons 20, the showcase 12, the motion gate 6, the template comments 2, the RTL scanner 81), the checker's and the
  inventory's tests (57 + 6): **2 000 passed, 10 failed, 3 skipped, 1 xfailed** — the ten failures the one semantic
  conflict above, the skips `apps/cases/tests/test_intake.py`'s (no legal rule in force), the xfail the showcase's
  captions (design-v5's own strict marker). After the fix, sec-f7's file, this family's (with the held file's page
  rendered end to end, one test added: the reason once, in the NowPanel; no notice; never a way to the page itself;
  «Dossier» for a mandated reader) and W3-A's shell re-run: **162 passed**. In Chromium (16 min 54 s):
  `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py` and `test_rtl_browser_overlays.py`, W3-D's
  journey, W3-A's phone and shell, W3-B's dashboard, W2-A's console overlays, W3-C's documents and drawer — **199
  passed**, 0 skipped, no crash.
- **Checks**: `ruff check .` clean; `manage.py check`: no issue; `makemigrations --check --dry-run`: no changes;
  `regen_design_inventory.py`: current; `git diff --check` clean; no CR byte in a changed text file; no inline style or
  script, no external URL, no secret in the added lines.
