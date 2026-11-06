# V5.12 · lane A · wave W2 — the motion system (label v512-a-w2)

28 October 2026 · branch `v512-a-w2` from design-v5 `6251475` · worktree `C:/tmp/ile_wt/v512-a` · lane server 8783
(dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, database lane l3) · binding: V5.12 §4, §5, §6,
§18, §19 and the Director's DECISIONS §1 T4, §2 M1–M9 + M11–M13, §3 (rows marked A), §10 lane A, Waves W2.

W2 for lane A is exactly: **M1–M9, M11–M13, the notices, the accordions, the drawer/Dépôt regions (T4)**. Nothing of
W3 (M15–M18, the command palette, the mega-menu morph, the CTA arrow twin) is in this branch.

## What the owner sees, where

| Where | What | How to see it |
|---|---|---|
| Every public page with a head followed by a chapter (/institutions/, /entreprises/, /parcours/, /le-projet/, /faq/ …), fr · it · en · ar, 1440 and 390 | **M1** — at load, a stroke in the structure's ink draws along the hairline under the page head (900 ms, from the reading edge: right to left in Arabic) and settles into it. The rule itself never moves. | Load /fr/institutions/. Reduced motion: the rule alone, still. |
| Captioned photographs (`.figura`) and any figure/picture lane C marks `data-reveal="mask"` | **M2** — as the photograph enters, a mask opens from the reading edge and the frame settles 1.06 → 1. A photograph already in view at load is at rest at load (the LCP is never masked). | Scroll to a captioned photograph (e.g. /forum/, a pathway sheet with a figure); more as lane C's imagery lands. |
| Black-and-white photographs lane C marks `data-grade="bw"` / `"bw-scroll"` | **M3** — grey at rest, colour under a fine pointer or the focus (480 ms); `bw-scroll` (the home's pilot diptych, /formation/) colours as it enters. Under reduced motion: colour, still. | Arrives with lane C's markup (contract below). |
| Lists of rows, doors, pathways; chapter marks | **M4** — each row's glyph / a door's disc / a chapter's mark rises 8 px and comes in as it enters, the six first a step apart. | Scroll /fr/institutions/, /fr/parcours/. |
| The public passage «la linea» (/parcours/…, the door pages, the questionnaire) | **M5** — its rings come and the line from each to the next draws as it enters (down on a phone, along the row from 48rem, mirrored in Arabic); in a flow with a current step, on the page's first view in the session the steps behind fill one after another (120 ms each) and the current ring settles. | Scroll to «Comment ça marche» on a pathway page. |
| The dashboard's «Mon parcours» | **M5** — on the page's first view in the session the travelled stretches light one after the other from «Maroc» (120 ms each), then the «Vous êtes ici» node settles. A reload or a return: the still. | Persona «qa-person», open the dashboard (a fresh session or a new tab after closing the others). |
| FAQ (fr · ar) and every accordion | **M6** — the answer opens its height (200 ms) and closes (120 ms); the open question stands on a tinted plate; the chevron became a drawn plus that folds into a minus. From the keyboard and under reduced motion: at once. | /fr/faq/, /ar/faq/. The glossary has no disclosure (a list of terms): nothing to animate there. |
| Tabs (the component; today drawn by the showcase only) | **M7** — a pointer's choice morphs the panels' height (200 ms). | /dev showcase. |
| Every modal, drawer and sheet over the scrim | **M8** — the page behind blurs 0 → 4 px with the scrim, on the scrim's own clocks. (Below 40 rem the dialog already is a bottom sheet with its head and foot pinned — W2-A — unchanged.) | Open the account menu sheet on a phone, a dialog, a modal drawer. |
| Every page that shows a session message (after a form, a sign-in, a profile change …) | **M9** — each message has its kind's mark and «Fermer». A **success** appears as a toast at the foot of the screen (inline end; above the bottom bar on a console phone), rises in and leaves by itself after 6 s — held while the pointer is on it, while the focus is in it, while the tab is hidden. **Errors, warnings and information stay in the page until closed** (never timed away). In-page notices slide 8 px into place; their words are never faded. | Update the profile (success toast); any refused form (error, stays). |
| «Mes documents» — a piece's drawer | **T4** — a reading that takes more than 400 ms shows the head's busy key and, in the empty body, still placeholder shapes (no pulse); at 1 s «Chargement…» under the head (said once); all gone on arrival. A fast reading shows nothing. | DevTools → Slow 4G, open a piece. |
| «Mes documents» — after a filing | **M11** — the row whose state changed cross-fades its chip (240 ms) and lights its reading-edge rule a moment. | File a PDF on a missing piece from the drawer. |
| The Dépôt on a piece's own page | **T4** — a slow re-reading of the piece after a filing lights the Dépôt's submit key after 400 ms; the piece is `aria-busy` while it comes. | Slow network, file a PDF on /documents/requirements/…. |
| Console navigation (Chromium ≥ 126, pointer) | **M13** — the current row's night plate glides from the row left to the row reached (200 ms), its words cross-fading; on a phone, the bottom bar's current item. Not across a language switch; not from the keyboard. | Click «Mes documents» then «Tableau de bord» in the rail. |
| The dashboard's next action | **M12** — the arrow leans 3 px under a fine pointer: this was already the buttons' own `.btn--arrow`; nothing added. | Hover «Consulter». |

Not changed by this branch: the hero (frozen pending its owner — lane C's Q1 change), any locked copy, any template of
`templates/portal/**` (lane D's).

## What changed (files)

* `static/css/v5/_reveal.css` (new partial) + `apps/core/static/core/reveal.css` (new page-only entry →
  `static/css/dist/core/reveal.css`): M1, M2, M3, M4, M5 (public). Linked by `templates/base.html` in a new block
  `reveal_sheet` after main.css; `templates/portal/base_portal.html` empties the block.
* `apps/portal/static/portal/v5/_motion.css` (console partial): M13 (`rail-current`), M11 (`data-changed`), T4 (the
  drawer's word and its two still shapes). M5 for the console journey is the journey's page sheet
  (`apps/portal/static/portal/v5/_journey-rail.css` §8): the shared console bundle carries no journey rule (W3-D's guard).
* `static/css/v5/motion.css` (shared): §4 the notices' entry/exit (transitions from `@starting-style`: no keyframe
  carries a var()), §5 the disclosure's height.
* `static/css/v5/notice.css`: the session message's anatomy (mark, words, «Fermer» = `.btn--icon`), the toast region.
* `static/css/v5/tabs.css`: the accordion's open plate and drawn plus/minus; M7 the panel's `block-size` transition from
  `@starting-style` (`--tabs-from-h`).
* `static/css/v5/overlays.css`: M8 the scrim's `backdrop-filter: blur(4px)` on its clocks.
* `static/css/v5/tokens.css`: `--reveal-shift: 8px`, `--reveal-zoom: 1.06` (DECISIONS §2).
* `templates/base.html`: the two message regions (in-flow, toast) and the reveal sheet's block;
  `templates/components/session_notice.html` (new): one message.
* `templates/documents/partials/piece_drawer.html`: the region's status line (`data-region-word`, «Chargement…»). The file
  has no lane owner in §10.0 (W1 did the same for requirement_detail.html).
* JS: `static/js/src/notices.js` (new; fetched by shell.js only when a page carries messages), `static/js/src/lume/
  region.js` (new; T4, re-exported by loader.js), `piece-drawer.js` (the reading through `region()`, M11's marking),
  `depot.js` (the page refresh through `region()`), `shell.js` (the notices' import), `static/js/src/head/head.js`
  (`html.is-seen`, a page's first view in the session), `static/js/main.js` (M7's `--tabs-from-h`). Dist rebuilt with
  `npm run build` (no new package; `node_modules` junctioned); the stale chunk `chunk-GLNQJYWV.js` removed.
* Paid for (in part) by deletions in main.css — rules and names read by nothing: `register.css`'s `.sequence` (its last
  consumers left with W3-E), `base.css`'s `.t-title`, `.t-prose`, `.t-lead`, `.t-gloss`, `.list-reset`, `layout.css`'s
  `.section--d`, `.section__header--center`, `components.css`'s `.icon--inline`, `v5/base.css`'s `.btn--inline`,
  `notice.css`'s aliases `.notice--warn`, `.alert--pending`, three V5 tokens (`--accent-night-fade`, `--f-serif-lat`,
  `--passe-partout-night`) and four names of the legacy token shim (`--notice-bg` / `-fg`, `--measure-narrow`,
  `--z-below`: 79 → 75, `MAX_SHIM_TOKENS` lowered; DESIGN_SYSTEM_2026 §17 rows and census, §2's weight rows, §3's
  `--rank-d-block` now «riserva»). Every name a test or a document still cites was kept — deeper cuts (the shim's state
  pairs, `.t-plate`) turned the documentation guards red and were put back.
* Docs: `docs/design-v5/DECISION_LOG_V54.md` **DL54-165** (plan §1.5's still-at-load and W2-A's «never a blur»
  amended; the steward renumbers at merge if needed); `docs/design-v5/COMPONENT_PROVENANCE.md` nine rows (Mask Reveal
  39591, Reveal on hover 1816, Stepper-01 28546, Animated Roadmap 8113, Tabs 35021, Accordion-09 27711, Animated Dialog
  26905 + Sheet-02 25010, Toast 24297, Shapes Skeleton 29863).

## Decisions taken inside the brief (why)

* **The success toast at the foot, not at the top.** DECISIONS M9 says «from 8 px above». A notice that leaves by itself
  from the page's flow moves the whole page up (≈ 0.11 CLS at 1440 — over the 0.1 budget). So a success stands in a
  fixed region (no layout), at the foot where it covers neither the letterhead nor the console bar, and rises 8 px from
  its edge. In-flow notices (error, warning, information) do come from 8 px above, and stay.
* **The head's hairline is drawn OVER, never hidden.** The chapter's full-bleed rule stays at rest; a darker stroke
  draws over it and settles into it — nothing disappears if the sheet is late or motion is reduced.
* **Scroll reveals are scroll-linked** (`view()`, as DECISIONS §2 rule 2 requires), so their «900 ms» is a scroll range,
  not a clock; an element in view at load is at its end state.
* **M7's edge fades are not drawn**: the ILE tab list wraps at every width, so no tab is ever beyond an edge
  (adding them cost 275 B of main.css for nothing visible).
* **Glossary**: it has no disclosure; M6 is the FAQ's and every `accordion` component's.

## Budgets (gzip -9 on the built files)

| Asset | Before (6251475) | After | Limit |
|---|---|---|---|
| `static/css/dist/main.css` | 31 149 B | **31 288 B** (+139) | ≤ 31 414 (DECISIONS §10 lane A acceptance 12) |
| `static/css/dist/core/reveal.css` (public pages only, new) | — | **1 336 B** | page-only ≤ 6 KB |
| `static/css/dist/portal/console.css` (console only) | 7 759 B | 8 134 B (+375: M11, M13, T4) | its partial `_motion.css` ≤ 6 KB |
| `static/css/dist/portal/journey.css` (journey pages only) | 2 421 B | 2 734 B (+313: M5) | page-only |
| `static/js/dist/shell.js` | 4 368 B | **4 390 B** | ≤ 4 700 |
| `static/js/dist/notices.js` (only on a page with messages) | — | 718 B | ≤ 1.5 KB (LANE_A §3) |
| `static/js/head.js` (render-blocking; the test's gzip) | 916 B | 978 B | ≤ 1 000 |

**main.css rose by 139 B** (the notices' anatomy and toast region, the disclosure's height, plate and drawn mark, the
tabs' morph, the scrim's blur), inside DECISIONS' ceiling of 31 414 B and paid in part by the deletions above; every
other motion of this wave is in page-only sheets. If the steward holds the stricter «never above the wave's base»
reading, the next cut is the dead `.jurisdiction` rules of `register.css` (its component is kept by W2-E's note, so that
is a decision, not a deletion).

No animation library, no new npm dependency, no React. CLS: nothing in the flow is removed by a timer (the toast is
fixed); the reveals act on transform/opacity/clip-path/filter only.

## Measured on 8783 (Chromium 153 headless; `C:/tmp/ile_v5_council/.work/v512-a-w2/probe.py`, captures in `shots/`)

* M1 /institutions/: fr/ar × 1440/390 — at 350 ms `reveal-rule`, scaleX ≈ .33–.36; at 1.95 s opacity 0 (settled).
  Reduced motion: no animation, the rule alone.
* M6 /faq/: at 90 ms the item is mid-height (236 of 249 px at 1440 — the entrance curve is fast at its start), plate
  `#f2f4f3`, the upright bar at 6 % of its height; reduced motion: full height at once, minus drawn.
* M4 /parcours/: the door's disc and the chapter marks carry `reveal-mark` on `view()`; a mark below the fold is at
  opacity 0 until its row enters; above, at rest. Reduced motion: none.
* M5: the public passage's lines `reveal-down` (390, scaleY .85 / .57 / .24 down the list mid-scroll) and
  `reveal-across` (1440); the dashboard's journey first view: `m5-across` 0 s, 0.12 s … on the travelled stretches,
  `is-seen` false; reload: `is-seen` true, no animation. AR 390: `m5-down`.
* M9 (fr 1440, ar 390): the warning in the flow (static), the success fixed at the foot (1440: 416 px wide at the
  inline end, bottom 24 px; 390: full width above the bottom bar, mirrored in Arabic); «Fermer» shown once wired;
  hovered for 7.5 s the toast stays, then gone 6 s after the pointer left; the warning stays until «Fermer», the focus
  then on `#main-content`.
* M13: the current rail row's `view-transition-name` is `rail-current` (1440), the bottom item's (390).

## Tests (lane l3: `TEST_DATABASE_URL=…/test_ile_v5_l3`)

* New: `tests/frontend/test_motion_v512_a_w2.py` — 18 tests, 20 cases (16 static/client, 4 browser cases: the head's hairline and a
  question's height under no-preference and reduce; a success's 6 s held by the pointer, a warning that stays; the
  drawer's slow reading — nothing at 200 ms, key + aria-busy + still shapes + «Chargement…» at 1.2 s, nothing on arrival
  — and a filing that marks the changed row with `m11-chip` / `m11-rule`).
* Updated (stale by the change, no guard weakened — each now asserts the new rule as precisely as the old one):
  `test_components_w1_c.py` (the drawn plus/minus; the notice aliases gone; the tabs' one layout transition and the
  plus's `background-size` named), `test_overlays.py` (exactly one blur, the scrim's, on its clocks, none at rest),
  `test_journey_w3_d.py` (`.sequence` must be absent; `_reveal.css` named as the passage's motion seat; the rail's §8
  gated by no-preference / html.rm / html.is-seen, the drawing above still still), `test_design_docs.py` (the base
  template applies main.css and, on public pages, the reveal sheet — and §2 says so), `test_legacy_token_shim.py`
  (ceiling 79 → 75). DESIGN_SYSTEM_2026: §2, §3 (`--rank-d-block` riserva), §10 (`session_notice.html`, 40 files), §17,
  the weight rows.
* Runs (lane l3, fresh test database): `tests/frontend apps/accounts/tests apps/documents/tests -m "not browser"` —
  **2 575 passed, 5 failed, 2 xfailed** (the two standing markers). The 5 failures are **pre-existing and not this
  lane's**: they fail identically on design-v5 (`7bfbdd2`, run with the same database): `test_cms_nav::test_portico_gives_every_door_its_panel_from_live_content`,
  `test_nav_sheet_w2_c2::test_signed_in_the_targa_seat_and_the_sheets_foot_hold_the_account_popover`,
  `test_mobile_rtl_w4_a::test_the_500_keeps_its_semicolon_with_its_words`,
  `test_service_pages_w3_f2::test_400_and_500_render_without_the_database_or_a_context_processor[400|500]`.
  Browser (Chromium lock held): `test_motion_v512_a_w2`, `test_drawer_browser_w3_c`, `test_depot_browser_w3_c`,
  `test_journey_browser_w3_d`, `test_loader_w1_d`, `test_motion_browser_w4_b`, `test_overlays_browser_w2_a`,
  `test_overlays_console_browser_w2_a`, `test_reduced_motion_w1_d`, `test_lume_v512_a` — **143 passed**.
* Note: a reused `test_ile_v5_l3` failed 364 setups on `legal_legaldocument.seed_checksum` (a schema the reused database
  no longer matched); `--create-db` cleared it — nothing in this branch touches that model.
* The lane server's QA personas have no document rows, so the drawer's T4/M11 were verified by the browser test on
  W3-C's register fixture rather than on 8783.

## New translatable strings (for lane D)

None new. «Fermer» and «Chargement…» are existing msgids, reused (`templates/components/session_notice.html`,
`templates/documents/partials/piece_drawer.html`).

## Requests to other lanes

* **Lane C** — the photograph contract for M2/M3 (no markup of yours changed here): every `figure.figura` already
  reveals; `templates/components/photo.html` should put `data-reveal="mask"` on its `<figure>` (or `<picture>`) for a
  body image, and `data-grade="bw"` (hover/focus colour) or `data-grade="bw-scroll"` (colour as it enters: the home's
  pilot diptych, /formation/) on the figure for black-and-white frames; the img stays inside a `<picture>` so the frame
  can settle under its mask. Never on the LCP image of a landing page if it would be below the fold at load (it is not
  masked when in view at load anyway).
* **Lane D** — the dashboard and console templates are untouched; M5/M11/M13 key on existing classes
  (`.journey`, `.doc-row[data-state]`, `.rail__item[aria-current]`, `.console-bottom__item[aria-current]`). When
  institution/university get their own space key (Q7), their journey (if any) and first page light with no template
  change.
* **Steward** — DL54-165 renumbered DL54-166 in the fix after review (below); the reveal sheet's link lives in `base.html`'s new `reveal_sheet` block
  (any template overriding `extra_head` keeps it).

## Fixes after review (v512-a-fix-w2)

Base: design-v5 `4d9ada5` merged into the branch (the v514-p merge); the one conflict was the decision log.

| Finding | Severity | What was done |
|---|---|---|
| Console foot never included (`base_portal.html` `site_footer`) | major | The inline footer (with «Conditions d'utilisation» and «Avertissement» linked while unpublished) replaced by `{% include "portal/partials/console_foot.html" %}`, lane D's partial: promoter line, the locked «not an authority» sentence, published legal pages only. **The partial and its tags (`console_foot`, `legal_links`) live on `v512-d-w2`: merge lane D's W2 before, or together with, this branch** — on this branch alone every console page raises TemplateDoesNotExist. Verified on a scratch merge of this branch with `v512-d-w2` (below). |
| `ile.seen` stored visited paths (case-file references) | major | `static/js/src/head/head.js`: the key now holds at most two fixed surface tokens, `passage` («la linea») and `journey` («Mon parcours», not the descriptive spine) — never a path. Before the first paint each stored token sets `html.is-seen-passage` / `html.is-seen-journey`; a token is written once the page carrying that surface is parsed (DOMContentLoaded); an old value (paths) is dropped on read and overwritten. Behaviour change: the light plays on the first view of the surface in a session (was: of each path). Sheets: `static/css/v5/_reveal.css` (`.is-seen-passage`), `apps/portal/static/portal/v5/_journey-rail.css` (`.is-seen-journey`); dist rebuilt (`npm run build`). **Request to lane P**: add the row `ile.seen` to the category B list in `apps/legal/content/cookies/{it,fr,en,ar}.txt` — sessionStorage, the session, «which of the two animated journeys (public passage, personal journey) were already shown in this tab, so their animation plays once; values `passage` / `journey`, no identifier». |
| DL54-165 collides with v514-p's | minor | Lane A's entry renumbered **DL54-166** (table row and section) and every lane-A reference to it (CSS comments, DS 2026, tests). |
| `main.css` +148 B gzip over design-v5 (31 288 vs 31 140; cap 31 414); console bundle 7 759 → 8 134 B | minor | Not changed: steward's call per the finding. The `.jurisdiction` rules of `register.css` are not unused (`components/jurisdiction.html`, `pages/home/_trust.html`, `selection/partials/responsible.html`, `components/journey_rail.html`), so the cheap cut is not available; the alternative is moving M11/T4 rules into a page-only sheet. This fix adds 0 B to main.css and to console.css (the renamed selectors live in the page-only `reveal.css` 1 342 B and `journey.css` 2 737 B gzip). |
| COMPONENT_PROVENANCE rows of lanes B and C missing | minor | Added: Floating Label 23566, Combobox 34726, Calendar 34713, Icon Card Radio Group 28351 (lane B, URLs from DECISIONS §5), «gli approdi», the families chips, the image «develop» (lane C: families only, lane C recorded no component id). Lane B's W3 rows (Status Badge 521, Empty Background 18266, File List Item 28496, Table with Filters 22162) wait for W3. The Journey row says «once per journey per session». |

Not in the findings, left for later: lane B's request to drop the asterisk in `templates/documents/partials/depot.html`.

### Tests of the fix (lane l3, `TEST_DATABASE_URL=…/ile_v5_l3`, on a scratch merge of this branch with `v512-d-w2`)

* `-m "not browser"` over `test_motion_v512_a_w2`, `test_journey_w3_d`, `test_design_docs`, `test_components_w1_c`,
  `test_overlays`, `test_css_bundle_is_current`, `test_check_ownership`, `test_dashboard_w3_b`, `apps/portal/tests`:
  **515 passed**.
* With `v512-d-w2` at `9417e92`: `test_organisation_space_v512_d`, `test_motion_v512_a_w2` (new
  `test_the_console_footer_is_lane_ds_console_foot`), `test_journey_w3_d`, `test_css_bundle_is_current`,
  `test_check_ownership`, `apps/legal/tests`, plus a throwaway check that `/fr/espace-reserve/` as a signed-in person
  renders the console foot (promoter, the locked statement, no «Conditions d'utilisation» / «Avertissement»):
  **209 passed, 4 skipped** (D's `core.countries` waits for lane B), **1 failed pre-existing**:
  `test_privacy_cookie_v514::test_production_settings_force_open_fields_off` fails identically on design-v5 `4d9ada5`
  («prod settings did not load» in this environment).
* No browser run for the `ile.seen` change (the machine's one-Chromium budget); the static tests pin the source and the
  minified head, the selectors of both sheets and the dropped old value.

