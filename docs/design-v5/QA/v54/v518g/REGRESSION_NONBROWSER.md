# V5.18 — full regression, non-browser half (fresh clone)

Label: `v518-reg-nonbrowser` · 29 Oct 2026 · read-only (nothing in the repository or in the worktree was changed)

## Setup

- **Clone:** `git clone --no-local --branch design-v5 C:/tmp/italylegalentry C:/tmp/ile_v5_council/.work/v518-reg-nonbrowser/clone`
- **HEAD:** `900372aaf3f62c9f6509f46366be8e02229b74de`. This is `v518/stabilisation`, the same commit as the merge's head. The tree is clean, LF throughout (`.gitattributes eol=lf`), and has no `.env`.
- **Environment:** CI-style, following `.github/workflows/ci.yml`.
  - Variables: `PYTHONIOENCODING=utf-8`, `PYTHONDONTWRITEBYTECODE=1`, `DATABASE_URL=…/ile`, the CI placeholders for `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.
  - Unset: `DJANGO_SETTINGS_MODULE` and `ILE_CONFIDENTIAL_SENTINELS`.
  - Port 5439 (the local compose database) instead of the CI service's 5432.
- **Database lane:** l3, `TEST_DATABASE_URL=postgres://ile:…@127.0.0.1:5439/ile_v5_l3`, which gives `test_ile_v5_l3`. It was idle before the start. Only one pytest ran on it at a time.
- **Python:** `C:/tmp/italylegalentry/.venv` (ruff 0.16.8 = the pin in requirements/dev.txt).
- **Bundles:** `find static/js/dist static/css/dist -type f -exec touch {} +`, as CI does.
- **Command:** `python -m pytest -m "not browser" -p no:randomly --create-db --durations=15 -q -rfE`

## CI steps

| Step | Result |
|---|---|
| `manage.py check` | **pass**: no issues (0 silenced) |
| `makemigrations --check --dry-run` | **pass**: no changes detected |
| `ruff check .` | **FAIL**: 69 errors (see below) |
| pytest, not browser | **22 failed, 6333 passed, 4 skipped, 2 xfailed, 635 deselected** (6361 collected) in 4945 s (1 h 22 min) |

## Flake or defect

- **Rerun alone:** all 22 failures were rerun alone (`rerun.log`). **22 failed again. 0 flakes.**
- **Same tests in the design-v5 worktree** (`C:/tmp/ile_wt/design-v5`, same HEAD, which has its `.env`): **22 failed** (`rerun_worktree.log`). Neither the clone nor the missing `.env` explains them.
- **Same tests on the pre-V5.18 base `v515/d`** (238dc1c1, a temporary worktree of the clone, removed afterwards): **20 failed, 2 passed** (`rerun_base.log`).
  - **2 failures are new in V5.18.**
  - **20 were already red on design-v5 before the stabilisation.**

## A. New in V5.18 (2): one cause, candidate defect (performance-budget ratchet)

| Test | file:line |
|---|---|
| `tests/frontend/test_forms_v515_b.py::test_budgets` | test_forms_v515_b.py:173 |
| `tests/frontend/test_forms_v515_b.py::test_the_empty_state_brings_its_sheet_once_and_main_css_does_not_rise` | test_forms_v515_b.py:271 |

`static/css/dist/main.css` grew from 33 448 B to **33 455 B** gzip -9, which is 7 B over the ratchet. Raw, it went from 172 584 B to 172 725 B. The whole growth comes from lane A's `a9ad225d` (v518-a-fix):

- `static/css/v5/chrome.css:654`: the P11 rule, `.nav-sheet .lang-seg__list--names .lang-seg__link { min-block-size/min-inline-size: var(--hit-primary) … }` (the 44 px target).
- `static/css/v5/tokens.css:513`: the P8 change, `--utility-h: 0px` plus its comment.

The rules themselves are correct and wanted (WCAG target size and P8). The ratchet `<= 33_448` belongs to lane B, and no exception was recorded for it in V5.18. There are two possible fixes:
- Lane A trims the 7 B, for example by shortening the comment that tokens.css added inside `html.rm`, which is in the bundle.
- Lane A records the +7 B as a V5.18 exception, and the ratchet in both tests is re-seated at 33 455 with that note.

The guard must not be dropped.

## B. Already red before V5.18 (20)

### B1. Stale tests: the product changed on purpose and the test did not follow (15)

| # | Test(s) | file:line | What changed (where, by whom) |
|---|---|---|---|
| 1–3 | `apps/faq/tests/test_views.py::test_search_without_result_shows_empty_state`, `apps/glossary/tests/test_views.py::test_search_without_result_shows_empty_state`, `apps/forum/tests/test_forum_registration.py::test_registration_page_without_event` | faq/tests/test_views.py:135, glossary/tests/test_views.py:145, forum/tests/test_forum_registration.py:194 | The empty state is now `class="empty-state empty-state--tile"` (`templates/components/empty_state.html:9`, lane B v515-b `9211d5fc`). The tests look for the exact attribute `class="empty-state"`. The empty state does render. |
| 4–6 | `tests/frontend/test_login_invitation_w4_d.py::test_the_invitation_is_back_once_the_sign_up_opens[fr\|ar]`, `::test_the_forms_override_reopens_the_invitation_as_it_reopens_the_sign_up` | test_login_invitation_w4_d.py:49, :58 | allauth's invitation was re-translated into the glossary's words: «Vous n’avez pas encore de compte ? Créer un compte» and «ليس لديكم حساب بعد؟ إنشاء حساب» (`locale/fr/LC_MESSAGES/django.po:15537`, `locale/ar/LC_MESSAGES/django.po:15425`; V5.12 lane D W2, `d6d5c6e5`). The gate still works. With the sign-up open, the paragraph is drawn with its link to `/fr/compte/signup/` (probe). With it closed, the paragraph is withheld, and `test_no_invitation_to_a_closed_sign_up` passes. Only the `INVITATION` needles are stale. |
| 7–12 | `tests/frontend/test_service_pages_w3_f2.py::test_every_account_page_stands_in_one_frame[…]` × 6 (profil, suppression, email, password/change, 2fa, logout) | test_service_pages_w3_f2.py:275 | Since V5.12 W2 (lane B), a signed-in account whose reserved area is open draws its account pages in the console frame, `allauth/layouts/_console.html`. The switch is `templates/allauth/layouts/manage.html:1` `{% extends request\|account_frame %}`, which calls `apps/core/templatetags/ile_core.py:358` and then `accounts.shell.frame`. The public frame `class="container conto"` (`allauth/layouts/base.html:27`) is no longer what `person_user` sees. The response carries `console.js` and `shell.js`. |
| 13–14 | `tests/frontend/test_service_pages_w3_f2.py::test_the_situation_s_personal_facts_say_what_they_are_for[fr\|ar]` | test_service_pages_w3_f2.py:440 (helper), :445 | «Ma situation»'s country of residence is now the CLDR `<select … autocomplete="country">` (`apps/accounts/profile_forms.py:191-195`, `751be04c`, DECISIONS §5.7). The test still expects `<input type="text" autocomplete="country-name">`. The profile test in the same file (`test_the_profile_s_personal_fields_say_what_they_are_for`) was already updated to the select and passes. |
| 15 | `tests/frontend/test_journey_w3_d.py::test_one_rail_drawing_and_one_passage_drawing_never_a_third` | test_journey_w3_d.py:586 | `static/css/v5/_compose.css:199`, `.training-phases > .training-phase > .linea__text { max-inline-size: none; }`, is a layout modifier of the passage (lane C v515-c-improve2, `a7884261`), not a redrawing. The test's `modifiers` set does not list `static/css/v5/_compose.css`. This is an ownership crossing: lane D's guard over lane C's sheet. |

### B2. Candidate defects (5)

| # | Test(s) | file:line | Diagnosis |
|---|---|---|---|
| 16–18 | `tests/frontend/test_service_pages_w3_f2.py::test_400_and_500_render_without_the_database_or_a_context_processor[400\|500]`, `tests/frontend/test_mobile_rtl_w4_a.py::test_the_500_keeps_its_semicolon_with_its_words` | test_service_pages_w3_f2.py:136, test_mobile_rtl_w4_a.py:285 | **The 400 and 500 pages query the database again.** See the chain below. |
| 19 | `tests/frontend/test_o14_lint.py::test_the_one_check_of_the_templates_is_the_persons_own_choice` | test_o14_lint.py:368 | `templates/partials/header.html:51` draws `{% svg_icon "check" "icon lang-menu__check" %}` on the active language (lane A v515-a W3, `cb252091`). The sprite's `check` is admitted only on the chosen option card. The integrated review already listed this as red on design-v5, with «lane A must either seat it in the lint's list or replace the glyph». It is still unresolved, so it stays a candidate defect until lane A rules. |
| 20 | `tests/frontend/test_v5_tokens.py::test_the_brand_colours_are_declared_once_and_no_literal_colour_leaves_the_token_sheets` | test_v5_tokens.py:932 | `static/css/v5/_fronte.css` (lane C v515-c-build, `fb4542a1`) has **27 literal colours** where tokens should be used. 21 are `#000` in mask gradients (lines 64, 65, 69, 70, 232, 233, …). The rest are `rgba(7, 18, 38, …)` shadows and `--fronte-grid: rgba(214, 226, 228, 0.07)` (lines 516, 560, 567, …). V5 rule: a literal colour lives only in `v5/tokens.css`. The V5.18 findings T1/T2 cover other `_fronte.css` tests (css_tokens_exist, rtl_static), not this one. Fix: token the shadow and grid colours. Mask alpha can use a token, or the guard can be extended for masks with a recorded reason. Do not weaken the guard. |

The DB-query chain for rows 16–18:
1. `templates/errors/_way_on.html:13` calls `{% safe_url 'forum:index' %}`.
2. That runs `apps/core/links.py:67` `public_url`, then `path_is_open` (:56), then `gate_is_open` (:41).
3. `apps/core/gates.py:109` `forum_public()` calls `apps/forum/services.py:79` `current_event()`, which is a query.

This gate came in with V5.12 lane C (`e677099a` and `832a1083`, «/forum/ behind its own gate»).

`apps/core/views.py:82-98` (`_self_sufficient`) promises that the 400 and the 500 draw with «no context processor, no database, no session». What happens instead:
- Under the test's DB block, rendering raises, and the view falls back to `_bare()`. That page has no `error-page__title` and no typo filter, so the semicolon's no-break space is gone.
- In production, `forum_public` catches only `DatabaseError`, so a lost database degrades to the full page with Forum omitted. A DB that hangs would still block the error page.

Fix: in `_way_on.html`, do not resolve a DB-backed gate on the self-sufficient pages. One option is to pass `forum_url` from settings or the context. The other is to skip that entry when there is no request.

## C. Lint (CI step «Lint»): candidate defect, pre-existing

`ruff check .` on HEAD: **69 errors**.

By rule:

| Rule | Count |
|---|---|
| E501 | 44 |
| C408 | 19 |
| UP031 | 3 |
| E741 | 1 |
| UP033 | 1 |
| C416 | 1 |

By file:

| File | Errors |
|---|---|
| `tools/build_derivatives.py` | 39 |
| `apps/pages/imagery.py` | 8 |
| `apps/pages/tests/test_home.py` | 3 |
| `apps/companies/forms.py` | 3 |
| `scripts/gen_loader_light.py` | 2 |
| `apps/enquiries/forms.py` | 2 |
| `apps/ecosystem/tests/test_gated_pages.py` | 2 |
| `apps/core/templatetags/ile_forms.py` | 2 |
| `tests/frontend/test_forms_v515_b.py:104`, `scripts/check_ownership.py`, `apps/portal/tests/test_views.py`, `apps/pathways/tests/test_views.py`, `apps/pages/views.py`, `apps/pages/templatetags/pages_imagery.py`, `apps/core/icons.py`, `apps/accounts/forms.py` | 1 each |

The full list is in `.work/v518-reg-nonbrowser/ruff_head.txt`.

How the count got here:

| Ref | Errors |
|---|---|
| `origin/main` (2b16eb3a) | 0 |
| merge-base c50d086 | 12 |
| `v515/a` | 3 |
| `v515/c` | 58 |
| `v515/b` | 68 |
| `v515/d` | 69 |
| HEAD | 69 |

V5.18 added none: the finding set is identical to `v515/d`'s. CI on a push of design-v5 would stop at the Lint step, before pytest.

## Counts

- **Collected:** 6361 non-browser tests.
- **Outcome:** 6333 passed, 22 failed, 4 skipped, 2 xfailed.
- **Flakes:** 0.
- **Failures by origin:**

| | New in V5.18 | Already red before V5.18 | Total |
|---|---|---|---|
| Candidate defect | 2 (the budget ratchet) | 5 | 7 |
| Stale test | 0 | 15 | 15 |
| **Total** | **2** | **20** | **22** |

- **Other CI steps:**
  - CI Lint red: 69 ruff errors, pre-existing.
  - Django check and migrations green.

## Files (all in C:/tmp/ile_v5_council/.work/v518-reg-nonbrowser/)

`pytest_full.log` (the full run), `failed.txt`, `rerun.log` (alone), `rerun_worktree.log` (design-v5 worktree), `rerun_base.log` (v515/d), `ruff_head.txt`, `env.sh` (the environment used), `clone/` (left as cloned; `git status` clean).
