# V5.18 · green suite, group N (label v518g-n)

29 October 2026 · branch `v518g-n` from design-v5 `900372a` (`v518/stabilisation`), with design-v5 `fd7368e` (the v519-k
merge, DL54-176) merged in · worktree `C:/tmp/ile_wt/v518g-n` · tests on database lane l5 (`test_ile_v5_l5`),
`-m "not browser" -p no:randomly` · binding: V5.18, V5.12 §22 («technical tests remain green»), V5.8 (shared bundles
ratchet down) · source of the failures: `evidence/v518/REGRESSION_NONBROWSER.md` · decision: DL54-177 (provisional
number).

Scope: the 22 non-browser failures of the regression and the CI Lint step (`ruff check .`, 69 errors). There was no
visual redesign. No copy was changed and no msgid was added. No browser was opened: no visual fix needed checking.
The only colour value that changed is the two black shadows in `_fronte.css`, now the V5 shadow ink.

## Each failure

| # | Test(s) | Class | What was done | Decision cited |
|---|---|---|---|---|
| 1–2 | `test_forms_v515_b::test_budgets`, `::test_the_empty_state_brings_its_sheet_once_and_main_css_does_not_rise` | **defect fixed** | main.css was 7 B over 33 448. Dead shared CSS was removed, with no visible loss: `.section--process` (`static/css/layout.css`; retired from the home, `test_home` asserts it absent), `.hide-mobile` (no producer), and `.chapter--night`, `.section--verso` and `.plate--verso` from the two night-context `:is()` lists of `static/css/v5/tokens.css` (the verso left with its last page). The bundle went from 33 455 to **33 406 B** gzip -9. Lane A's P8 and P11 rules stay. After the v519-k merge it is 33 530 B, under lane K's recorded ceiling of 33 600. The ceiling was not touched. | V5.8 (ratchet down) |
| 3–5 | `test_service_pages_w3_f2::test_400_and_500_render_without_the_database_or_a_context_processor[400\|500]`, `test_mobile_rtl_w4_a::test_the_500_keeps_its_semicolon_with_its_words` | **defect fixed** | The way-on's Forum link read `gates.forum_public` → `current_event()`, which is a query. `core.links.without_database()` is a context variable: while it is set, a named gate is closed and is not read. `core.views._self_sufficient` renders the 400 and the 500 inside it. Every gate reads a table, so on those two pages a gated destination is left out. The rule «never a link to a 404» holds without the database. Production gains too: a database that hangs no longer blocks the error page. | W3-F2's contract (`_self_sufficient`'s docstring) |
| 6 | `test_o14_lint::test_the_one_check_of_the_templates_is_the_persons_own_choice` | **ruling** | The Director ruled under DECISIONS §15 lane A. The tick beside the active language in the letterhead's popover (`templates/partials/header.html`, v515-a cb252091) is the person's own choice in a menu (`aria-current="true"`). That is the option card's meaning, never a state. It is seated in the lint's list and in `apps/core/icons.py` `CHECK_BEARING["check"]`. The test also asserts that it is drawn exactly once, and only inside `{% if l.active %}`. | DECISIONS §15 lane A; o14 module docstring («the person's own interface act») |
| 7 | `test_v5_tokens::test_the_brand_colours_are_declared_once_and_no_literal_colour_leaves_the_token_sheets` | **defect fixed** | `static/css/v5/_fronte.css` had 27 literals. Each was replaced with a token value; the guard is unchanged:<br>• `rgba(7, 18, 38, α)` → `color-mix(in srgb, var(--p-notte-950) α%, transparent)` (same colour)<br>• `rgba(0, 0, 0, α)` → the same night ink (tokens.css: shadows are never black)<br>• mask stops `#000` → `var(--p-notte-950)` (a mask reads alpha only)<br>• `--fronte-grid` → `--line-night-soft` at 50 % (= .07)<br>• `--fronte-light` → `--p-oro-300` at 14 %<br>• the print `#000` → `--p-inchiostro-900`<br>No token was added to tokens.css, so main.css did not move. | V5 rule «a literal colour lives in v5/tokens.css» (plan §2.7) |
| 8–10 | `apps/faq/…::test_search_without_result_shows_empty_state`, `apps/glossary/…::test_search_without_result_shows_empty_state`, `apps/forum/…::test_registration_page_without_event` | **stale test updated** | The tests now assert the component's full opening tag `<div class="empty-state empty-state--tile" role="status">`, which is stronger than before: it includes the role. | V5.15 W3 lane B round 1 (DECISIONS §15 lane B; 9211d5fc) |
| 11–13 | `test_login_invitation_w4_d::test_the_invitation_is_back_once_the_sign_up_opens[fr\|ar]`, `::test_the_forms_override_reopens_the_invitation_as_it_reopens_the_sign_up` | **stale test updated** | The needles are now the catalogue's words: «Vous n’avez pas encore de compte ?» and «ليس لديكم حساب بعد؟». The old needles matched nothing, so `test_no_invitation_to_a_closed_sign_up` was passing vacuously. It tests again. | V5.12 lane D W2, DECISIONS §9 (d6d5c6e5, `accounts.allauth_terms`) |
| 14–19 | `test_service_pages_w3_f2::test_every_account_page_stands_in_one_frame[×6]` | **stale test updated** | Signed in with the reserved area open, the frame is the console's. The test asserts:<br>• `<div class="conto conto--console">` + servizio.css + `id="console-rail"`<br>• no public header and no public `container conto`<br>• the same section marking in `conto-nav`<br>• the page's own words as its one `<h1>` («Modifier le mot de passe» is allauth's title)<br>• the console trail's current crumb (`accounts.shell.console_context`) and «Espace réservé»<br>• one primary at most<br>The public frame stays covered by `test_account_shell_v512_b`. | V5.12 W2 lane B, DECISIONS «Lane B» acceptance 6; V5.18 P-2 |
| 20–21 | `test_service_pages_w3_f2::test_the_situation_s_personal_facts_say_what_they_are_for[fr\|ar]` | **stale test updated** | The country of residence is the CLDR `<select … autocomplete="country">`, and there is exactly one such control (no `<input>`). This matches the profile test in the same file. | DECISIONS §5.7 (751be04c) |
| 22 | `test_journey_w3_d::test_one_rail_drawing_and_one_passage_drawing_never_a_third` | **stale test updated** | `("passage", "static/css/v5/_compose.css")` is listed among the page modifiers. The rule is «Formation»'s two phases side by side, the text freed from the measure in its column. The test's «redraws the journey» check still runs over the sheet and passes. | DECISIONS §15 lane C (v515-c-improve2 a7884261) |

## ruff (CI «Lint»)

`ruff check .` went from 69 errors to **0**. Lane K's merge brought 6 more E501, which were also fixed.

- **Rules fixed:** C408 (`dict()` → literals, 19), C416, UP031 ×3 (percent → f-string), UP033 (`lru_cache(maxsize=None)` → `cache`), E741 (`l` → `left`).
- **E501:** fixed by wrapping lines and splitting string literals into adjacent literals (same value). The files touched were `ruff format`-ed, except `apps/core/icons.py`, which was wrapped by hand.
- **No value changed:**
  - `tools/build_derivatives.py`'s module literals and string constants were compared by AST before and after. The only difference is the `'  (budget %d)' % limit` → f-string.
  - The gettext msgids split across lines are the same strings.
  - `makemigrations --check`: no changes. `manage.py check`: clean.

## Shared files touched (kept minimal)

| File | Change |
|---|---|
| `apps/core/links.py` | `without_database()` plus two lines in `gate_is_open` |
| `apps/core/views.py` | the `with` around the self-sufficient render |
| `static/css/layout.css` | two dead rules removed |
| `static/css/v5/tokens.css` | three dead selectors removed from two lists |
| `apps/core/icons.py` | the `check` seat's description; one line wrapped |
| `static/css/dist/main.css`, `static/css/dist/pages/css/fronte.css` | rebuilt with `npm run build` |

Formatting only, in lane-owned files: `tools/build_derivatives.py`, `apps/pages/imagery.py`, `apps/companies/forms.py`, `apps/enquiries/forms.py`, `apps/accounts/forms.py`, `apps/core/templatetags/ile_forms.py`, `apps/pages/templatetags/pages_imagery.py`, `apps/pages/views.py`, `scripts/check_ownership.py`, `scripts/gen_loader_light.py`, lane K's `apps/core/{contact,context_processors,models}.py`, and five test files.

## Left for the steward

- **The main.css ceiling.** It stays lane K's 33 600. The measured value is 33 530 B. Lowering the ceiling to the measure, as V5.8 asks, is the steward's call once the parallel groups have merged, because their CSS lands on the same bundle.
- **`docs/design-v5/DESIGN_SYSTEM_V5.md:214`** still quotes the night list with `.chapter--night`. That is a historical V5 snippet and was left alone. In `docs/design/DESIGN_SYSTEM_2026.md`, the three places that named `.section--process` or `.hide-mobile` as living (§ grounds, §7) now say they are gone, citing DL54-177.

## Run

The full non-browser suite ran on lane l5 at the merged head. The result is in the commit that adds these notes
(`.work/v518g-n/pytest_full.log`).
