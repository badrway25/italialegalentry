# V5.18 full regression: browser half (label v518-reg-browser)

**Candidate:** design-v5 `900372aaf3f62c9f6509f46366be8e02229b74de`, which is tag `v518/stabilisation^{commit}`. The tag object is a248dc8.
**Clone:** `git clone --no-local --branch design-v5 C:/tmp/italylegalentry C:/tmp/ile_v5_council/.work/v518-reg-browser/clone`. HEAD was verified equal to the merge head. Nothing in the clone was changed: `git status` is empty.
**Environment (CI-style, from .github/workflows/ci.yml):**
- No `.env` in the clone.
- `DATABASE_URL` points at the local dev PostgreSQL on 127.0.0.1:5439, with the dev credentials of docker-compose.
- `TEST_DATABASE_URL=…/ile_v5_l4` (lane l4, test database `test_ile_v5_l4`).
- `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` take the CI placeholders. `DJANGO_SETTINGS_MODULE` is not set.
- `PYTHONIOENCODING=utf-8` and `PYTHONDONTWRITEBYTECODE=1`.
- Committed dist bundles were touched, as CI does.
- Shared `.venv`.

**Command:** `python -m pytest -m browser -p no:randomly --create-db -q --durations=15`
**Chromium lock:** held from 21:26:08 to the end. The time was rewritten into it about every 10 minutes and at each rerun. It is now released.

## Result

| Run | Passed | Failed | Skipped | Deselected | Time |
|---|---|---|---|---|---|
| Full browser suite, fresh clone | **594** | **41** | 0 | 6 361 | 3 990 s (1 h 06 min) |
| Each of the 41 rerun **alone** (one pytest process per node id, `--reuse-db`) | 0 | **41** | – | – | ~7 min |
| The same 41 on the **pre-merge design-v5 238dc1c1** (v515-d merged, before v518-a…d), same environment and DB lane | 0 | **41** | – | – | 316 s |

- **No flakes.** All 41 fail again when run alone, with the same assertion at the same line.
- **The stabilisation merge introduced no regression.** All 41 already fail, at the same line, on 238dc1c1.
- One test changed failure point. `test_content_pages_browser_w3_f2` failed at :301 on the baseline (shadows at rest on `/fr/faq/`: breadcrumbs container and the FAQ search). It now passes that check and stops at :323, the known corner set of DL54-173. The merge improved it.
- **Carry-overs DL54-174 now green.** `tests/frontend/test_dashboard_browser_w3_b.py` passes 29/29: the 18 c-rise cases, the 4 bridge-order cases and 390x844-fr. The w3-b test-ownership crossing no longer produces a failure.
  - m-6 (`test_design_docs`) is a non-browser test, so it is outside this half.
  - The other carry-over browser cases on the baseline list of 28111658 also pass now: the ten `test_service_pages_browser_w3_f2` cases and the dashboards' first-viewport and bridge tests.
- **Timing artefact.** `--durations` reports two `test_entrance_form_w2_b::test_every_target_of_the_form_has_its_size` setups at about 1.79e9 s. Those are wall-clock values from a mocked clock, not real durations; the whole run took 66 min. It is harmless.

## Classification of the 41

Legend:
- **Stale test:** the guard pins a state that a later, documented design decision replaced. The product behaves as designed.
- **Candidate defect:** the product breaks a rule that is still binding.
- **Ruling pending:** a design/guard conflict already handed to the Director, or one that needs the owning lane to confirm.

### A. Candidate defect (minor): 2 tests

| Test | file:line | Diagnosis |
|---|---|---|
| `test_journey_browser_w3_d.py::test_mon_parcours_draws_the_dashboards_journey_at_its_head[level]` and `[card]` | test :332 (`rail["moving"] == []`); product `static/css/v5/_glyph.css:140` | The empty-state tile's light `animation: empty-light 320ms … 160ms both` has a `from` keyframe only (:141). With `both`, the finished one-shot stays in effect and stays listed by `document.getAnimations()`, so the journey's settle guard reads `['empty-light']` as moving. This is the same cause lane A removed under the V5.18 rule «backwards, never both» (`apps/portal/static/portal/v5/_motion.css:176-179`, `_reveal.css:393`). Nothing loops and nothing visible is wrong; the guard is right under the V5.18 rule. Minimal fix: `both` → `backwards` on `_glyph.css:140`. Origin: 2a3de3e8 (v515-b F1). Owner: lane B. The integrated review's polish item 3 (`_conto-console.css:36`) is the same class. |

### B. Ruling pending: 5 tests

| Test | file:line | Diagnosis |
|---|---|---|
| `test_content_pages_browser_w3_f2.py::test_every_content_page_holds_the_grammar_in_both_directions` | :323 | The formwork pages' corner set (12/6/8/999/4/6.4 px, and 1 px at 390) on `/contact/formulaire/`, `/entreprises/recueil-des-besoins/` and `/collaboration/institutions/`, in fr and ar, at 1440 and 390. This is lane B's V5.15 formwork, **already left for the Director's ruling DL54-173** (INTEGRATED_REVIEW.md, «Tests»). It is unchanged by the merge apart from the improvement noted above. |
| `test_orientation_browser_w3_f1.py::test_no_overflow_three_corners_and_no_raised_shadow_at_rest[1440-900-fr/ar, 390-844-fr/ar]` (4) | :114 | `/{lang}/diplomes-et-titres/` has 2 radii and no overflow, but `raised: 1`: one first-screen element has a shadow with blur ≥ 40 px at rest. The W3-F1 guard forbids that. The V5.15 lane C page-head compositions use `--shadow-3` and `--shadow-4` (40 px blur) at rest by design: `_fronte.css:1262` (the head's notice panel), `_fronte.css:641` (search seat), `_compose.css:50` (the photographic band's frame). The exact element was not isolated, because nothing in the clone may change. Lane C should confirm it is one of those deliberate surfaces; if so, the guard is stale and the change goes to the Director, as in DL54-173. |

### C. Stale tests: 34 tests (product as designed; the guard predates a recorded decision)

| Test(s) | file:line | What the guard expects / what the product now does (decision) |
|---|---|---|
| `test_browser_chips_w1_c.py::test_the_cards_sit_on_their_levels_with_one_radius` | :398 | Expects «no shadow moves (SH-4)» on hover. A `.card--link` now lifts 3 px and takes `--shadow-3` under a fine pointer (`static/css/v5/_reveal.css:455-458`, «M15 · cards lift under the hand»). Source: V5.15 lane A motion language, cb252091/b9098210. |
| `test_browser_w1_c.py::test_a_public_field_is_la_lastra_and_its_focus_is_the_one_system` | :133 | Expects a 4 px field radius on `/fr/contact/formulaire/`. The formwork sets `--field-radius: var(--radius-md)`, which is 6 px (`static/css/v5/_formwork.css:28`). Source: V5.15 lane B Premium Forms (7788ca38); the same family as DL54-173. |
| `test_browser_w1_c.py::test_a_link_to_an_faq_row_opens_it` | :439 | Expects a rotating chevron (`::after` transform ≠ none). The mark is now a drawn plus/minus made of two background bars, with no transform (`static/css/v5/tabs.css:130-143`, Accordion-09). Source: V5.12 lane A W2 e2fe36ec. The permalink-opens-the-row part of the test passes. |
| `test_browser_w2_c2.py::test_the_sheet_opens_and_closes_on_the_overlay_system[fr]`, `[ar]` | :120 | Expects the sheet's head lock-up to match the header's. On the **home**, the header keeps only the mark (`apps/pages/static/pages/css/hero.css:182`, «one name on the screen … gives its words to the hero's H1 (Q1)»), so the bar is 44 px wide while the sheet's head shows the name. Source: 44252192 (v512-c-w2). The guard measures the home. |
| `test_header_fits_the_narrowest_viewport.py::test_the_name_and_the_menu_button_share_the_phone_row[fr]`, `[ar]` | :143 | Expects `.lock__text` shown from 329 px. On the home it is hidden at every width by the same Q1 rule (`hero.css:182`). The guard measures `/{lang}/` only. «Menu» past the column and the horizontal scroll both pass. |
| `test_rtl_browser.py::test_trademark_sign_stays_on_the_right_of_the_name_in_every_wordmark` | :459 | Expects ≥ 2 wordmarks on `/ar/`. Only the footer's is visible, because the header's is hidden by Q1 (`hero.css:182`). The visible one is correct (`ok: True`). |
| `test_console_shell_browser_w3_a.py` at 1366×657 `[fr]`, `[ar]` (:138); longer rail ×3 (:170); open from 80rem (:196); control folds (:223); identity panel `[fr]`, `[ar]` (:677) — **8** | :138 :170 :196 :223 :677 | Expects 10 rows for a person (11 for a professional, 11 with the identity panel). The Academy row is present only when at least one course is published or the account holds an enrolment (`apps/portal/services.py:924-942`, `:964-965`, DECISIONS §8 «hidden while 0 courses are published»). `seed_all` (tests/conftest.py:104) publishes none, so every count is one short. Source: d6d5c6e5 (V5.12 lane D W2). |
| `test_console_shell_browser_w3_a.py::test_il_lume_marks_the_current_page_once_per_rail_copy_and_a_lone_glyph_shows_its_word` | :388 | Expects the account tip to end «— Personne». It reads «Mon compte — Espace Personnes»: the space's word, never the role word (V5.12 §11; Director's decisions §9; `apps/portal/services.py`, the `_audience`/`roles.space_label` comment). |
| `test_console_shell_browser_w3_a.py::test_the_shell_draws_two_corners_no_shadow_at_rest_and_one_edge_for_every_page_header` | :463 (`TypeError … null.getBoundingClientRect`) | The script reads `.console__footer .portal-footer__legal`. That paragraph is drawn only when there are published legal links (`templates/portal/partials/console_foot.html:17`, `{% if console_legal %}`), and the test does not use `legal_published`. Source: d6d5c6e5, «the footer's published legal links». |
| `test_console_shell_browser_w3_a.py::test_the_footer_s_legal_pages_are_targets_and_a_skip_link_s_ring_stays_inside_its_box` | :816 | Expects 3 footer legal links. Only the contact address is drawn, because no legal document is published (the same rule as above). The one target present is 24 px tall, which meets the floor. |
| `test_console_shell_browser_w3_a.py::test_an_account_with_two_spaces_is_told_which_one_it_is_in_and_offered_the_other` | :519 | Expects 10 rows for a company's «Espace réservé». The rail has 6: `PERSON_ONLY_PAGES` (situation, pathways, cases) are removed for a company (`services.py:969-971`, Q7 «no person-oriented modules»), and Academy is absent (above). The head assertions just before (space, the way to «Espace entreprise», «Entreprise») pass. |
| `test_console_shell_browser_w3_a.py::test_an_institution_a_university_and_the_project_team_are_told_apart_at_the_foot[fr]`, `[ar]` | :571 | Expects «the ten» for an institution. Since Q7 an institution has its own organisation rail of 4 (`services.py:1049-1054`: dashboard, Mon organisation, Mes demandes, Mes échéances). Source: d6d5c6e5. |
| `test_overlays_console_browser_w2_a.py::test_the_drawer_brings_the_focused_entry_into_its_view[390-844]`, `[844-390]` | :281 | Expects «Academy» to be the rail's last page. Academy is absent with 0 published courses (above), so the focused entry is another one. |
| `test_overlays_console_browser_w2_a.py::test_the_page_behind_the_drawer_leaves_the_accessibility_tree` | :334 | After closing, the guard allows only `.overlay-scrim` and `.tooltip` to stay `aria-hidden` among `body`'s children. The Lume veil is a body-level child that is `aria-hidden="true"` by its own markup (`templates/components/lume_veil.html:23`, included at `templates/base.html:50`; V5.15 lane A cb252091). overlay.js leaves an element hidden by its own markup as it is (`static/js/src/overlay.js:573-598`). The open-state assertions (only the dialog and its «Menu» are read) pass. This is not an a11y defect. |
| `test_mobile_rtl_w4_a.py::test_every_stand_alone_link_answers_on_44px_under_a_finger_and_24_under_a_pointer[finger]`, `[pointer]` | :383 | The target list names `.aiuto a, .form__privacy-link a` on `/fr/entreprises/`, and the guard itself reports «nothing to measure: the page no longer draws it». The public company form left the door page for `/entreprises/recueil-des-besoins/` (V5.15 lane B formwork). The list must follow the page. |
| `test_mobile_rtl_w4_a.py::test_a_notices_address_answers_on_its_targets_while_the_legal_texts_are_awaited[finger]`, `[pointer]` | :383 | `.legal-page__pending .notice__body a` on `/ar/condizioni-di-utilizzo/` is no longer drawn. Unpublished legal pages changed form in C-W3 M-2 («legal 404 + links»). The list must follow the page. |
| `test_rtl_browser.py::test_every_arabic_public_page_fits_the_viewport[390]`, `[1440]` | :122 | `served >= 55` and 54 are served. Overflow and the one-h1 check (`problems == []`) come after this assertion. The floor predates the routes that now answer non-200 while their content is unpublished. This is the same class as `test_routing`'s ungated floor, which T3 already corrected to 23. The exact route was not isolated. |
| `test_rtl_browser_nav.py::test_the_architrave_and_the_entries_follow_the_doors_in_both_directions[ar]` (:75), `[fr]` (:77) | :75 :77 | W2-C1's «Il portico» geometry (N2: the entries column starts at the first door's inline start). V5.15 lane A replaced it with the floating mega panel: three zones, the content from the side travelled, each door at its own height (cb252091, b9098210). The architrave checks (N19) above it pass. |

The rows count 1+1+1+2+2+1+8+1+1+1+1+2+2+1+2+2+2+2 = 34. In total, A 2 + B 5 + C 34 = **41**.

## Notes

- **Ownership of the stale guards.** The guards come from the W1-C, W2-A, W2-C, W3-A, W3-F1, W4-A and RTL suites. Each was overtaken by a recorded V5.12 or V5.15 decision: Q1, Q7, DECISIONS §8, §11, the lane A motion and portico, the lane B formwork, and lane C's compositions. Under the binding rule («tests updated only to the new correct behaviour, never weakened»), each should be re-pointed, not loosened. Examples: measure the header on a non-home page; publish a course or use `legal_published` where the guard is about the rail or the footer; add the veil to the allow-list as a self-hidden element; follow the moved form. That work belongs to the owning lane at the next stabilisation step. Nothing was changed here.
- **What could not be isolated without changing anything:** the one element with a raised shadow on `/diplomes-et-titres/`, and the one non-200 Arabic route. The diagnoses above name the likely candidates.
- **Logs:**
  - Full run: `C:/tmp/ile_v5_council/.work/v518-reg-browser/run1.log`
  - Per-test reruns: `…/rerun/<n>.log`, summarised in `…/rerun_summary.txt`
  - Baseline run: `…/base_run.log` (baseline clone `…/base` at 238dc1c1)
  - Node ids: `…/failed_ids.txt`
  - Digest: `…/fails_digest.txt`
