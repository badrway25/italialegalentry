# V5.18 green suite, group C: the console family (label v518g-c)

**Branch:** `v518g-c`, from design-v5 `900372a` (tag `v518/stabilisation`).
**Scope:** the CONSOLE family of `REGRESSION_BROWSER.md`. That is 18 failures: `test_console_shell_browser_w3_a` ×13, `test_overlays_console_browser_w2_a` ×3, `test_journey_browser_w3_d` ×2.
**Database lane:** l6.
**Chromium:** headless, under `CHROMIUM_LOCK` from 23:04 to the end of the runs. No headed session was needed, because no visible change was made.

## Result

`pytest -m browser --create-db` on `test_console_shell_browser_w3_a.py`, `test_overlays_console_browser_w2_a.py` and `test_journey_browser_w3_d.py`: **63 passed, 0 failed**.

That count includes one new test (§2.1).

## 1. Candidate defect, fixed in the product

| Failure | Cause | Fix |
|---|---|---|
| `test_journey_browser_w3_d::test_mon_parcours_draws_the_dashboards_journey_at_its_head[level]`, `[card]` (:332, `rail["moving"] == ['empty-light']`) | In `static/css/v5/_glyph.css:140`, the empty-state tile's light ran `animation: empty-light 320ms … 160ms both`. Its keyframe has `from` only. With fill `both`, the finished one-shot stays in effect and stays listed by `document.getAnimations()`. That breaks the V5.18 rule «backwards, never both» (lane A, `portal/v5/_motion.css:176-179`, `_reveal.css:393`). | `both` → `backwards`. The resting frame is the element's own `transform: scaleX(1)`, so nothing visible changes. I rebuilt the bundles that carry the partial with `node scripts/build_css.mjs`; only `dist/core/glyph.css`, `dist/core/forms.css` and `dist/orientation/wizard.css` changed (+5 bytes each). Shared file: `_glyph.css` is a partial of page-only sheets, not `main.css`. |

## 2. Stale tests, updated to the approved behaviour with the same strength

None was deleted or loosened. Where a count stood for «the longest rail», the test now builds that rail rather than lowering the number.

### 2.1 The Academy row: DECISIONS §8, «hidden while 0 courses are published» (`portal.services.academy_open`)

- **Failures:**
  - `test_at_1366_by_657_…_holds_whole` `[fr]` `[ar]` (:138)
  - `test_a_longer_rail_scrolls_under_its_pinned_foot…` ×3 (:170)
  - `test_the_rail_is_open_from_80rem…` (:196)
  - `test_the_control_folds_the_rail…` (:223)
  - `test_the_identity_panel_is_drawn…` `[fr]` `[ar]` (:677)
  - `test_overlays_console_browser_w2_a::test_the_drawer_brings_the_focused_entry_into_its_view[390-844]` `[844-390]` (:281)
- **Cause:** these tests measure the person's longest rail: the ten (11 with a register or the identity panel), with Academy last. `seed_all` publishes no course when demonstration data is off, so the rail had nine.
- **Update:** a local fixture `academy_published` (`ILE_SEED_DEMONSTRATION_DATA=True`, then `seed_all --only academy`, asserting that a course is published). This is the same seeding as `tests/frontend/test_organisation_space_v512_d.py::academy_courses`. The geometry is again measured on the longest rail. The 1366 × 657 test also asserts that `academy` is the last key.
  - I added the same fixture to the foot test in four languages (`test_the_foot_s_last_row_holds…`). It was passing, but its message claims «the ten».
- **Added:** `test_while_no_course_is_published_a_person_s_rail_has_no_academy_row`. Without a published course, the rail is exactly the nine keys, in order, with no Academy row in the drawer, and it holds whole at 1366 × 657. Both sides of §8 are now asserted in the browser.

### 2.2 «— Espace Personnes»: V5.12 §11, Director's decisions §9 (`roles.AUDIENCE_SPACE_LABELS`)

- **Failure:** `test_il_lume_marks_the_current_page_once…` (:388).
- **Cause:** a person is told the name of their space, never the role word «Personne».
- **Update:** the compact account tip must end «— Espace Personnes».

### 2.3 The footer's legal line: D-16 (V5.12 lane D W2), V5.12 Q2 / V5.14 §13

`console_foot.html` draws only the published legal pages, so both tests now use `legal_published`.

- **`test_the_shell_draws_two_corners…` (:463, the TypeError):** the legal line is now present, so its edge is measured again.
- **`test_the_footer_s_legal_pages_are_targets…` (:816):** the count goes from 3 to **5**. That is privacy, cookies, terms and disclaimer, plus the contact address. The floors are unchanged: ≥ 24 px on a desktop and ≥ 44 × 44 under a finger, on every link.

### 2.4 The atrium head: V5.15 lane D, DECISIONS §15 lane D (`portal/v5/_platform.css` §1)

This failure was hidden behind the :463 TypeError.

- **Failure:** once the legal line was drawn, the same test stopped at «one start edge, 28 px title».
- **Measured on all five pages** (`page-header`, `ws-head`, `ws-head-empty`, `doc-page`, `academy`), with the same values on each:
  - the head is the atrium's sheet, with its left edge at 280;
  - the title sits at 313, which is 280 + 1 px hairline + `--s-8`;
  - the title size is 34.72 px with a 38.89 px line height: `clamp(1.75rem, 1.45rem + 0.8vw, 2.25rem)` at 1440, line 1.12;
  - the footer line and the breadcrumbs are at 280.
- **Update:** the test pins all of these exactly.
  - It asserts the `[data-atrium]` sheet: its edge at 280 and its inset of 33.
  - It asserts that the five pages share one edge and one size.
  - The workspace padding assertion is unchanged.

### 2.5 The company rail: Q7, «no person-oriented modules» (`PERSON_ONLY_PAGES`), and §8

- **Failure:** `test_an_account_with_two_spaces…` (:519).
- **Update:** the count of 10 becomes the exact key list `dashboard, requests, documents, deadlines, messages, helpdesk`. The other space is still asserted to be a way at the rail's head, not a page of the rail.

### 2.6 The organisation rail: Q7 (`portal.services._organisation_rail`)

- **Failures:** `test_an_institution_a_university_and_the_project_team_are_told_apart…` `[fr]` `[ar]` (:571).
- **Update:** «the ten» becomes the exact key list `dashboard, organisation, requests, messages` for the institution and for the university. «Mes échéances» appears only once the team has set a date. The test also asserts that the rail holds whole at 657 px (nothing clipped, nothing to scroll).

### 2.7 The page behind the drawer: the Lume veil, V5.15 lane A (`components/lume_veil.html`, included by `base.html`)

- **Failure:** `test_the_page_behind_the_drawer_leaves_the_accessibility_tree` (:334).
- **Cause:** the veil is a body-level child that is `aria-hidden="true"` in its own markup, and overlay.js leaves an element hidden by its own markup as it is.
- **Update:** before the drawer opens, the test records what hides itself: exactly the veil and the overlay scrim.
  - After closing, only the scrim, the tooltip and the veil may stay hidden.
  - A new assertion checks that the veil holds nothing reachable (no link, control or tabindex) and takes no pointer.
  - The open-state guard is unchanged: every other body child is hidden, and only the dialog and its «Menu» are read.

## 3. Rulings

None. Every failure in this scope was either a defect or a test made stale by a recorded decision.

## Outside this scope, seen while checking

`test_forms_v515_b::test_budgets`, `test_forms_v515_b::test_the_empty_state_brings_its_sheet_once_and_main_css_does_not_rise` and `test_journey_w3_d::test_one_rail_drawing_and_one_passage_drawing_never_a_third` fail identically with and without this branch. They are baseline failures listed in `REGRESSION_NONBROWSER.md` (:39, :40, item 15) and belong to the other groups.
