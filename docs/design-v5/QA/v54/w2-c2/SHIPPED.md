# W2-C2 shipped — 12 October 2026

**The navbar, part 2 — the phone sheet, the targa's account popover, the panel on `overlay.js`.** Tag **`v54/w2-c2`**
(design-v5 `f0bd452`, the status commit, as for the earlier families); merge commit `28d3916`. The owner's
preview on http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at 05:45 and
verified. Steward's merge, label `w2-c2-merge`, under `DESIGN_V5_MERGE_LOCK` from 04:11:57. Reviewed once and fixed
(V5.5): `REVIEW.md` and `A11Y_PERF.md` are both SHIP_AFTER_FIXES with no P0; the fix pass (`NOTES.md`, «Review fixes»;
DL54-101) closed the review's two majors (the French letterhead on two rows at 1024; the tablet sheet without its
foot), the check's two majors (a tap on the menu sheet's scrim reaching the phone sheet; the foot's menu ring at
1.75 : 1), recorded its third (the public pages' script, with its A/B), fixed six of the review's seven minors and the
check's minor, and routed the review's m1 (the scrim beside a classic scrollbar's gutter) to W2-A. No reviewer has
read the fix pass again.

## What shipped

- **The phone and tablet sheet** (below 80rem; `templates/partials/main_nav.html` «sheet», `static/css/v5/chrome.css`
  §7, `static/js/src/nav.js` `initSheet`): the overlay system's modal drawer, at the body's level after the letterhead,
  opened by «Menu» (a link to it: without script the sheet shows in place). Its head takes the letterhead's row — the
  lock-up and «Fermer», which takes the first focus; «Menu» and «Fermer» are one width per language below 48rem. Then
  the Fase 3 order: the four languages by their own names → the four doors as 64 px rows on night discs, each
  unfolding in place (an exclusive `<details name>`: the locked gloss in the lede's voice, the entries with their live
  second lines, «Voir l'espace»; the current section's door open) → Forum · Projet → the FAQ's search (when that page
  is public) → the primary → the anti-fraud line → the foot pinned on night: «la targa» at 44 px (signed in, the
  account popover's trigger) and the promoter. Below 48rem it takes the screen «Quiet» (an opacity, the body and the
  foot rising 12 px; 320 / 200 ms); from 48rem the side sheet slides in from the inline end — from the left in
  Arabic — with its own 24 px margin and ends on the same night foot. The system holds the trap, the one scrim, Esc,
  «Fermer», the focus back on «Menu», the scroll lock without a shift and the page out of the accessibility tree; a
  window widened past 80rem puts the sheet away. Under 30rem of height the sheet scrolls as one under a sticky head.
- **The signed-in targa's account popover** (`templates/partials/header.html`): `components/account_menu.html` with
  `popover`, in the targa's seat (the person glyph alone below 100rem, the name beside it from there) and in the
  sheet's foot — hung on the trigger's inline end, the focus on its first row, ↓ ↑ Home End, Esc and the focus back,
  closed when the focus leaves or a row is chosen; at ≤ 40rem a bottom sheet over the one scrim whose tap reaches
  nothing beneath (the held scrim in `overlay.js`). Its rows keep the paper's ring (#1d8a93, 4.11 : 1) from the night
  foot too.
- **The key alone** is named by the system's one top-layer tooltip, refused from 100rem where the plate says its word;
  **no hole when the flags are off** (a bare end zone, not drawn from 80rem).
- **The letterhead holds one row at 1024 px** in every language, under a finger and beside a classic scrollbar: the
  compact lock-up from 64rem (French 42.8 px to spare under a finger).
- **`overlay.js` on every public page** (`shell.js` imports it; one chunk with the console's). Any opening of the
  system puts a pinned door panel away (WebKit's press focuses nothing).
- **What left**: the V4 drawer (markup, script, rules), `v4/shell.css` (the file), the account menu's `<details>` face,
  `main.js`'s `initDropdowns`, V4's segmented language track and its rules — W2-A's hand-overs, as its comments asked.
- **Not built — item 3, the desktop panel on `overlay.js`**: the portico panel keeps W2-C1's adapter (its own scrim,
  dismissal and focus) until W2-A's contract has a disclosure primitive (`NOTES.md` «For W2-A» item 1); the switch is
  a small change in `initPortico`, W2-C2's follow-up. The panel looks and behaves as W2-C1 shipped it.

## The merge

- **The sync** (`63b5860`): design-v5 at `3780a7c` — 31 commits since the branch's last sync (W3-F2's content, legal,
  error and account pages, its steward's merge, status and shipped note, the confidential-material docs commit) —
  merged into the branch. Two conflicts, both areas' work kept: the decision log (design-v5's entries, then the
  family's) and `dist/main.css` (rebuilt). `components.css` and DS 2026 merged on their own, each design-v5's plus
  exactly the family's diff. Nothing of W3-F2's draws what this family removed (every account-menu caller passes
  `popover=True`, every language-control caller `lang_names`; the self-sufficient error letterhead includes neither the
  header nor the nav).
- **Numbering**: the family's entries are **DL54-100** and **DL54-101** (written DL54-96 and DL54-97; the notes' closing
  section, «Merge step», gives the mapping); the steward's record of the merge is **DL54-102**.
- **Ownership**: `scripts/check_ownership.py w2-c2 3780a7c` listed the 17 paths outside the slice the family declares;
  each was read in the diff and written under w2-c2 with its reason (`2960180`), six slices named as written
  (`chrome.css`, `nav.js`, `header.html`, `components.css`, `test_design_docs.py`, DS 2026); three more came from the
  merge's own runs (below). After it: 6 inside, 29 slice, 19 generated, and the two steward-only paths the steward
  wrote (the manifest, the capture report); `--validate`: coherent, 25 families, 566 entries.
- **Bundles**: rebuilt from a clean `static/css/dist` and `static/js/dist` in the sync, and again on design-v5 after the
  merge (`35acc4c`): every CSS bundle byte for byte the tested one; the JS the branch's code byte for byte, three shared
  chunks named after design-v5's worktree.
- **Bytes — the owner's V5.8 gate** (gzip −9, design-v5 before → merged; DL54-102 items 4–5): every page type
  **435 B lighter**, every page-only sheet unchanged, and every ceiling lowered to the merged weight under the
  orchestrator's definitive ruling:

  | Page type | design-v5 `3780a7c` | merged | new ceiling |
  |---|---|---|---|
  | an interior page (`main.css`) | 41 464 | **41 029** | 41 029 |
  | console page types (`main` + `console` + `portal`) | 50 205 | **49 770** | 49 770 (was 50 927) |
  | «Mes pièces» (+ `documents.css`) | 51 377 | **50 942** | 50 942 |
  | the company's dashboard (+ `companies.css`) | 51 078 | **50 643** | 50 643 |
  | the login (+ `entrance.css`) | 46 325 | **45 890** | 45 890 |
  | the home (+ `hero.css`, `pages.css`) | 56 115 | **55 680** | 55 680 |
  | a content page (+ `cms/lettura.css`) | 45 520 | **45 085** | 45 085 |
  | an account page (+ `cms/servizio.css`) | 43 890 | **43 455** | 43 455 |
  | an error page (+ `cms/errori.css`) | 45 093 | **44 658** | 44 658 |

  JS: the overlay core (6 476 B gzip) is now on every public page — the home's script 51 156 B against plan §2.6's
  45 KB, one more request before `load`, no measured cost on the twin (DL54-101 item 4) — recorded, until W4-B removes
  the Motion library's 26.6 KB chunk.
- **The capture report** regenerated on lane 8 (DEBUG off, one headless Chromium, exit 0; `4577ed4`): 43 captures, all
  as expected; 29 differ, all the sheet — the menu open fills the screen from the top (844 / 844 px at 390 × 844,
  768 / 768 at 1024 × 768), without script the letterhead holds its row and sticks (57 / 65 px); DS 2026 §13's icon
  total regenerated with it (995 → 865, `3921d29`).
- **Three pins of what the family removed**, found by the merge's runs and fixed (`0ac4c43`, `a52dddf`): `main.js`'s
  new header line tripped the «no import» guard of `test_static_assets.py`, which also pinned the deleted dropdown
  fallback (now read in `overlay.js`); `test_components_w1_c.py` read the deleted `v4/shell.css`; and
  `test_page_integrity.py` read the English «Close» of the sheet's «Fermer» as the helpdesk's French «Close» (une demande
  close) on every English page — a homograph the guard now leaves out. None of these files was in the family's runs.
- **Tests** (`TEST_DATABASE_URL=…/test_ile_v5_l8`, one pytest and one browser at a time, no run crashed; V5.5:
  targeted, not the full suite). On the branch: the named non-browser set with the family's, W3-F2's and the scripts'
  unit files **1 235 passed** (+1 failed, fixed: the first pin); widened to every other non-browser file of
  `tests/frontend` and `tests/i18n`, **727 passed** (+5 failed: three the family's, fixed; two design-v5's own); after
  the fixes every touched file green (39 + 30 + 24 + 160 + 46). Browser (headless Chromium): **239 passed** — the
  family's and W2-C1's navigation, the 320 px header, `test_browser.py`, the Arabic navigation (58); W2-A's overlay
  files, the Arabic overlays and W3-A's console files (107, +1 failed: design-v5's own); `test_rtl_browser` and
  W3-F2's two browser files (39); W1-D's loader and reduced motion and W1-B's icons (35, +3 failed: design-v5's own).
  On design-v5 after the merge and the rebuild: **394 passed** (the bundles, the design docs, the static pipeline, the
  ownership and inventory scripts, `test_overlays`, `test_nav_sheet_w2_c2`, `test_static_assets`,
  `test_components_w1_c`, `test_layout`, `test_cms_nav`, `tests/security` with the sentinel test) and **42 passed** in
  the browser on the renamed chunks (the family's two files, W2-A's console overlays). `ruff check .` clean;
  `makemigrations --check`: no changes. Logs: `C:/tmp/ile_v5_council/evidence/v54/w2-c2/merge/`.
- `live_status.json`: the family row w2-c2 (state v5, its review as the decision, the tag) and the census state
  **`navbar-open`** as V5 — both halves of «the home with its menu open» are now V5 (W2-C1's panel at 1440, this
  family's sheet at 390). `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all 200, no traceback, after the restart)

- http://127.0.0.1:8780/fr/ · http://127.0.0.1:8780/ar/ · http://127.0.0.1:8780/__design-v5/ — the strip names
  `v54/w2-c2`; the index lists the family as passed, with its review
  (http://127.0.0.1:8780/__design-v5/decisioni/w2-c2/REVIEW.md), and «navbar-open» as V5.
- **The sheet** — in the strip's phone frame, or a window under 1280 px: http://127.0.0.1:8780/fr/ and
  http://127.0.0.1:8780/ar/ — «Menu» opens it (on a phone «Quiet» over the screen; from 768 px the side sheet, from the
  left in Arabic); a door page, its door already open in the sheet: http://127.0.0.1:8780/fr/parcours/ ; the FAQ, with
  the sheet's search: http://127.0.0.1:8780/fr/faq/ ; http://127.0.0.1:8780/fr/le-projet/ ; the login under the same
  letterhead: http://127.0.0.1:8780/fr/compte/login/ (and each under `/ar/`). A 1024 px window: the letterhead on one row.
- **The account popover** — `/__design-v5/` → «Personas» → «Entrer» (e.g. «Personne, conditions non acceptées»,
  qa-person; no password; the preview's sessions are read-only), then http://127.0.0.1:8780/fr/ : the targa is the
  account's trigger (its name beside the glyph from 1600 px); in the phone frame the sheet's foot holds it and the menu
  opens as a bottom sheet over the scrim. «Sortir» after. **Reduced motion** and **forced colours**: the system's
  settings.

Checked after the restart at 05:45, by request only (no browser on the owner's server;
`C:/tmp/ile_v5_council/evidence/v54/w2-c2/merge/verify_8780.log`): 29 checks, 0 failures — `/fr/`, `/ar/`, `/it/`,
`/en/` with the sheet (`#nav-sheet`, the system's drawer, «Menu» its link) and no V4 drawer nor `<details>` account menu;
the preview, its index and the review; the door page, the project, the FAQ and the login in fr and ar; `shell.js`,
the four chunks it imports and `main.css`; through the preview's own persona switch (qa-person; «Sortir» after), `/fr/`,
`/ar/` and the door pages with the letterhead's two account popovers (the targa's and the sheet's foot's), and the
console (`/fr/espace-reserve/`, `/ar/espace-reserve/`) with its own popover and drawer and no sheet. The server's log
(`.work/servers/srv8780.log`) holds no traceback and no 5xx.

## Not done

- **Item 3 — the desktop portico panel on `overlay.js`** (plan §1.12 item 6, §3.4 item 5's gate): waits for W2-A's
  disclosure primitive (`NOTES.md` «For W2-A» item 1); `nav.js` closes the panel on any opening of the system until
  then. W2-C2's follow-up, a small change in `initPortico`.
- **For W2-A** (`NOTES.md` «For W2-A»): the disclosure primitive (1); main.js's fallback traces in CONTRACT §6,
  `wireDisclosure`'s marking and `overlays.css` §9's summary-only declarations (2); the core chunk on public pages (3);
  the scrim and an inline-end drawer beside a classic scrollbar's gutter, a 15–17 px undimmed strip (REVIEW m1; 4); the
  held scrim in `overlay.js`, W2-A's to own from this merge (5).
- **design-v5's own failures, handed over** (DL54-102 item 10; each reproduced on design-v5 before the merge):
  W3-A's `test_menu_is_reached_in_three_keys_and_opens_a_drawer_that_holds_the_whole_rail` — **a press on the scrim
  after a keyboard reopen leaves the console drawer open**, 2 runs of 3 alone on either tree (W2-A's intermittent
  defect, seen once at its merge; on a phone, a tap on the scrim that does nothing — for W2-A first);
  `test_the_chip_is_drawn_by_one_sheet` (W3-F2's `_lettura.css` styles the chip; W3-F2 with W1-C);
  `test_no_animate_or_frame_loop_outside_the_gate` (`overlay/extras.js` calls `requestAnimationFrame`; W2-A with
  W1-D); three of `test_loader_w1_d.py` (the submit guard's `aria-disabled`, and the logout probe's
  `account-menu__link`, a class no page carries any more; W1-D with W2-A).
- **The public pages' script over plan §2.6** (the home 51 156 B, +1 request): recorded (DL54-101 item 4, DL54-102
  item 6), until W4-B removes the Motion library.
- **For W4-D**: `_legacy-tokens.css`'s `--nav-drawer-top` has no consumer since the drawer left (DS 2026 §3.18 and
  §17, `test_css_tokens_exist.py`'s `RUNTIME_PROPERTIES`).
- **The in-flight trees**: `v54-w3-c`, `v54-w3-d` and `v54-w3-f1` still carry the V4 drawer in the shared chrome files
  they did not edit (their merges take design-v5's); `v54-w3-c` edits `templates/dev/showcase.html` and `v54-w3-f1`
  `static/css/main.css`, both rewritten here — their stewards meet this version.
- **N18** («richer than Fase 3»: the comp beside the build) stays the navbar review's, for W2-C1 and W2-C2 together.
- **Not checked at the merge**: no browser on 8780 (by rule); WebKit, Firefox, a real phone and a screen reader were
  never run (REVIEW m2's WebKit press reproduced by dispatched clicks); the Performance Lead's twin 8782 was not
  measured for this merge.
- **The full suite** was not run (V5.5: the integration checkpoint runs it).
