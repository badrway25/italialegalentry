# W2-C2 · The navbar, part 2 — accessibility + performance check (V5.5, one pass)

Role: the family's accessibility + performance check (label `w2-c2-a11y-perf`; built nothing, changed nothing in the
family's code). Reviewed: branch `v54-w2-c2` at `549428e` (clean); the base of every comparison is its merge base,
design-v5 at the W2-A merge (`361b03d`). Lane 8: the dev server on 8788 from `C:/tmp/ile_wt/v54-w2-c2` on `ile_v5_l8`
(`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`) for the accessibility series; for the timings a
compressed twin of 8782's shape (DEBUG off, `CompressedManifestStaticFilesStorage`, hashed and gzipped static, its own
`STATIC_ROOT`, the same clone and date) on **8798** — a port outside the lanes, so that neither the lane's dev server nor
the family reviewer's (8888) was ever replaced by it — serving the head and the base (`git archive 361b03d` into a scratch
folder outside every repository) in turn. Headless Playwright Chromium (the venv's 1.63, HeadlessChrome 153.0.8010.12),
one fresh profile per context under `C:/tmp/ile_v5_council/.profiles/w2-c2-a11y-perf/`, removed at close; reduced motion
and forced colours by emulation; axe-core 4.13.0. One browser and no pytest at a time; every series waited on
`PERFORMANCE_BENCHMARK_LOCK` (never present; never created by this role); no run crashed. Never 8780, 8782, 9222 or
9223. The signed-in header through one session minted with `Client.force_login` on `ile_v5_l8` (`qa-person`; no password
used, typed or stored), revoked at the end (`revoked: 1 session rows deleted on ile_v5_l8`); 269 evidence and scratch files
scanned: the session value is in none. Base tree, static roots and profiles deleted at the end; the lane server and the
twin stopped. 12 October 2026, 01:52 → 03:02. The model that did this check is Claude Opus 5.5.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w2-c2/a11y-perf/` (E/ below) — `s1/` (keyboard and states, 10 cells, JSON +
PNG; `zorder.json`), `s23/` (the key alone's tip, the account popover, `scrimtap.json`), `s4/` (contrast on pixels, rings,
`menu_tokens.json`), `s5/` (reduced motion, forced colours, reflow, text spacing, targets, axe, the accessibility tree),
`s11/` (at rest, no script), `s12_portico.json` (the desktop panel's keyboard model), `perf/` (216 traced loads: `ab-head/`,
`ab-base/`, `summary-ab.json`), `weigh_revs.json`, `js_per_page.json`. Probes: `C:/tmp/ile_v5_council/.work/w2-c2/w2-c2-a11y-perf/`.

## 1. Verdict: SHIP_AFTER_FIXES

No P0. The phone and tablet sheet and the account popover are keyboard-complete in both directions, every text passes
contrast on pixels (everything under 16 px at 7.17 : 1 or more), focus is visible on every stop and never obscured,
reduced motion is a real still, forced colours hold, 320 px and 400 % reflow, no target under 44 px under a finger, axe
finds nothing, the shared CSS got lighter on every page type, the LCP element is unchanged, CLS stays under 0.03 and
nothing loops. Two behaviours must be fixed before the merge — both in the new composition of the account menu inside
the sheet's night foot — and the public pages' script weight must be fixed or recorded; one minor.

| # | Severity | Finding | Where | Fix | Acceptance |
|---|---|---|---|---|---|
| M1 | **major** | **On a touch screen, a tap on the account menu's scrim inside the open phone sheet reaches the sheet underneath.** Signed in at 390 × 844 (touch), fr and ar: the sheet open, its foot's account menu open as a bottom sheet over the scrim; a tap on the dimmed sheet closes the menu — and then the row under the finger receives the tap: over «Institutions» the door unfolds and takes the focus; over «Forum Vénétie–Maroc» the page navigates to the Forum; over «English» the site switches to English. With a mouse the scrim takes the whole press (nothing reached, the focus back on the trigger), as the system promises (W2-A's REVIEW M1: «the page is never reached»). **Cause** (event log in E/s23/scrimtap.json): the platform light-dismisses the menu at `pointerdown`; `settle()` → `syncScrim()` then re-stacks the one scrim from z 51 (over the nav sheet, z 50) to z 49 (under it, for the still-open trapped sheet); a touch's compatibility `mousedown` / `mouseup` / `click` are hit-tested after `touchend`, so they land on the row. `data-held` keeps the scrim's `pointer-events`, not its place in the stack. Only this family's composition — a menu sheet over a trapped drawer — reaches the case on a product page (the console's menu sheet has no trapped panel under it; the sheet's own scrim beside the side sheet at 768 is fine, E/s1). | `static/js/src/overlay.js` (`makeScrim()` / `syncScrim()`; W2-A's module) | Keep the scrim stacked where it was while it is `data-held` — re-stack at the release (the click or the 1 s timer) — or cancel the press's compatibility events (`preventDefault()` on the scrim's `touchend` when the press dismissed a popover). Either is a few lines; the path is outside W2-C2's slice (plan §2.2: a justified extra path, or W2-A's hand-over). | Signed in, 390 × 844 touch, fr and ar: sheet open → foot's menu open → tap the scrim over a door, over Forum and over a language: the menu closes; the door stays folded, the URL and the language unchanged, the focus on the foot's trigger, the sheet still open and modal. A browser test with `page.touchscreen.tap`. |
| M2 | **major** | **WCAG 1.4.11 / plan §1.6 (the ring ≥ 3 : 1 on every ground): the account menu opened from the sheet's night foot draws its focus ring at 1.75 : 1.** `.nav-sheet__foot` is `.on-inverse`, which re-points `--focus-ring` to the night ring (#7fd1d8) and the icon tokens to their night values (#b9c5d6); the menu is a white panel in the top layer but inherits both from its DOM ancestor. Its focused rows draw the light ring on white — 1.75 : 1 on both sides (fr and ar, E/s4/s4.json `rings.signed-*-390`, E/s4/menu_tokens.json) — and its row glyphs are washed out (≈ 1.8 : 1, decorative). The letterhead seat's menu (1440) and the console's draw the paper ring (#1d8a93, 4.11 : 1) and #4a5a62 glyphs. If the review's M2 brings the foot back from 48 to 80rem, the side sheet's menu inherits the same tokens. | `static/css/v5/chrome.css` §7 (with `on-inverse` on `.nav-sheet__foot` in `partials/main_nav.html`) | Give the menu panel its paper tokens back, e.g. `.nav-sheet__foot .overlay { --focus-ring: var(--p-laguna-550); --focus-halo: rgba(29, 138, 147, 0.3); --icon-default: var(--text-2); --icon-muted: var(--text-3); --icon-strong: var(--text-1); --icon-interactive: var(--accent-mark); }` (`:root`'s values) — or keep `on-inverse` on the targa / trigger and the promoter and off the popover's ancestor. | Signed in at 390 (and at 768 if the foot returns there), fr and ar: the foot's menu open, each row focused in turn: outline colour #1d8a93, ≥ 3 : 1 against the row and the panel; glyphs #4a5a62. |
| M3 | **major** (fix or record; no measured cost) | **The public pages' script is beyond plan §2.6.** `shell.js` now imports `overlay.js` (as plan §2.3 says), so the overlay chunk (6 466 B gzip; the module budget is 4 KB, the figure the steward recorded at the W2-A merge, DL54-94 / 95) is on every public page: the home 45 581 → **51 136 B** gzip, past the «public page ≤ 45 KB» line (46 080 B) by 5 056 B; a door page 38 006 → 43 559, the login 39 683 → 45 235 (still under). Requests before `load` +1 script on every public page (the home 3 + 8 → 3 + 9, a door page 1 + 6 → 1 + 7, against the before set's 2 + 8 and 1 + 6: the request ratchet of §2.6 is now over by this family's one request). The console pages are 913 B lighter (one chunk for both). **Measured cost: none** — the A/B in §3: LCP pooled 1 524 → 1 472 ms, every cell within +50 ms (the Arabic home at 1440 +18 ms at n = 18), first-render task, longest task and TBT equal or lower, CLS unchanged. | `static/js/src/shell.js` (the static `import` of `overlay.js`) | Either load the overlay chunk off the critical path on public pages — a dynamic `import()` at idle after `load`, and at once on the first `pointerdown` / `focus` of «Menu» or the account trigger (the no-script `:target` sheet covers the gap) — which takes the request and the 5.5 KB off the path before `load`; or have the merge step record the public pages' JS figures in DL54 with these timings, as DL54-94 / 95 recorded the module's. | The home ≤ 46 080 B gzip and 3 + 8 requests before `load` — or a DL54 entry naming the figures and this A/B. |
| m1 | minor | **At 320 × 256 (400 % of 1280 × 1024) the pinned foot and the head leave the menu one row.** The head 56 px + the night foot 120 px (fr) / 128 px (ar) leave the sheet's body 80 / 72 px of 256. Not a 1.4.10 failure — one-dimensional scrolling, no overflow, every stop whole when focused (E/s5/reflow.json) — but at 400 % the menu reads through a slot. | `chrome.css` §7 | Unpin the foot on a short viewport (e.g. `@media (max-height: 30rem)`: the foot scrolls at the end of the body), as the console drawer already does below 30rem of height. | 320 × 256, fr and ar: the body ≥ 50 % of the viewport; the targa / trigger reachable at the end of the scroll. |

**Not findings, explained.** (a) axe's incompletes: `aria-hidden-focus` on the page behind the open sheet is the overlay
system's trapped modal by design (the page `aria-hidden`, never `inert` — W2-A's INP rule; the scripted trap holds: no
stop outside the sheet in any cycle); `color-contrast` incompletes are answered by the pixel probe; `aria-valid-attr-value`
is axe's «needs review» for `aria-controls` on a closed panel (the target exists). (b) The ring samples at 2.71 / 2.82 are
the ring meeting the 1 px row hairline or the search field's own halo (the field ring ruled not a failure in W1-C's R1);
against the sheet's white the ring is 4.11 : 1. (c) The «clipped» records at 360 under the spacing sheet are the visually
hidden «Fermer» (screen-reader-only at ≤ 23rem, by design). (d) A press outside the letterhead's popover on desktop
reaches the element under it — the platform's light dismiss on a non-modal popover, as everywhere; M1 differs because a
menu shown as a sheet promises that its scrim takes the press. (e) The sheet's cold open costs about 70 ms more than V4's
drawer (p90 128–160 against 48–80 ms) — the dialog, the trap, the page's `aria-hidden` and the first layout of a larger
panel — and holds N9's 200 ms (§3). (f) The desktop portico panel's switch to `overlay.js` (item 3) is not built; the
panel is W2-C1's, re-checked here for the keyboard only (§2), unchanged.

**Read after the measures — the senior review (`REVIEW.md`, `15d2a12`).** No overlap with M1 / M2 above (the review does
not exercise a touch on the menu sheet's scrim nor the menu's ring colour in the foot). Its M2 (the tablet sheet's
missing foot) is consistent with what this check measured at 768 (the sheet's cycle has no targa; the letterhead's targa
lies under the sheet) — and its fix makes M2 above apply at tablet widths too. Its N9 figures (lane, p90 152 / 160 ms)
agree with this check's twin figures. On the script weight the review records the figure and calls it not a finding; this
check flags it because its brief counts bytes beyond §2.6 as a regression to flag, with the measured nil cost said in the
same row.

## 2. Accessibility

**Names, roles, landmarks** (the accessibility tree through CDP, 390 × 844, fr and ar; E/s5/ax.json). Closed: «Menu» is a
`button` (the overlay system upgrades the no-script link: `role="button"`, `aria-haspopup="dialog"`, `aria-controls="nav-sheet"`,
`aria-expanded` false → true), named «Menu» / «القائمة» at every width (the word screen-reader-only at ≤ 23rem). Open: only
the sheet is exposed — a `dialog` named «Menu», `modal` true (124 of 615 nodes kept in fr, 126 of 648 in ar; the banner,
the bars, `main`, the footer and the scrim are `aria-hidden` while it is open and given back at the close, E/s1 →
`open_state.hiddenSiblings` / `after_esc`). Inside: «Fermer» a `button`; «Choisir la langue» a `navigation` of four links
named in their own language (`lang` / `hreflang` / `dir`, the current one `aria-current`); the five doors as disclosure
triangles named by their door with the right `expanded` state (the current section's open); the entries as links with
their live second line as the description (`aria-describedby`); the FAQ's search a `search` landmark with a visible
label; the French gloss on an Arabic page a `lang="fr" dir="ltr"` run. Signed in: the account trigger is a `button`
(`popovertarget`) named «‹short name› — Mon compte» (the visible name first, 2.5.3), the panel a `group` named «Mon compte»
whose rows are links and the sign-out a submit button. The key alone is a link named «Espace réservé» / «الفضاء الخاص» at
every width; its layer tip is `aria-hidden` (the name stays on the control). axe-core 4.13.0, WCAG 2.0–2.2 A/AA, on the
open sheet (390 fr + ar, 768, 1024), the account popover (1440), the menu sheet in the sheet's foot (390) and the closed
pages (1440 fr, 390 ar): **0 violations** (E/s5/axe.json); the incompletes are explained in §1.

**Keyboard walk, fr and ar** (E/s1/s1-{fr,ar}-{390,360,768,1024,1279}.json, open-*.png, door-*.png). From the top: skip link →
lock-up → «Menu» on a phone (at 768 the languages and the targa come first, at 1024 / 1279 the bar's doors). Enter, Space
or a tap opens the sheet in the input's task; the focus lands on «Fermer» with its ring. A full Tab cycle stays inside the
sheet — 17 stops on a phone (the four languages, the five doors, Forum, the search field and its button, the primary,
the anti-fraud link, the targa, the lock-up, «Fermer»), 15 at 768, 9 in the band (languages, Forum, Projet, the search,
«Fermer») — and Shift+Tab from «Fermer» wraps to the last stop. Enter on a door unfolds it in place and folds the one that
was open (exclusive); Tab enters its entries. Esc closes from anywhere in it, «Fermer» (Enter) closes, a press on the
scrim beside the side sheet closes; each time the focus is back on «Menu», `aria-expanded` false, the page's
`aria-hidden` removed, `html[data-overlay-lock]` gone. The page scrolled to 400 px stays at 400 px through the open, the
close and a Space on «Menu»; no horizontal scroll at any width. A press on the letterhead while the sheet is open lands on
the scrim (z 49 over the letterhead's 20; E/s1/zorder.json). The side sheet stands at the inline end (fr 348–768, ar
0–420 at 768). The account popover (1440, 1280, 1920, 768 under a finger; fr and ar; E/s23/s3.json): Enter opens it with
the focus on «Espace réservé», ↓ ↑ walk the rows and wrap, Home / End, Esc closes and gives the focus back to the trigger
(`aria-expanded` back to false), Tab from the last row closes it and moves on, a press on a blank spot closes it; it hangs
on the trigger's inline end (its right edge on the trigger's in fr, its left edge in ar). Inside the phone sheet the menu
opens as a bottom sheet over the scrim with the focus on its first row; Esc closes the menu first (the focus back on the
foot's trigger, the sheet still modal), a second Esc closes the sheet (the focus back on «Menu»). M1 is the one break: a
touch on that scrim. The desktop portico after this step's `nav.js` changes (E/s12_portico.json; 1440 and 1024, fr and
ar): ↓ opens a door's panel and enters its first entry, ↑ returns to the door, → / ← follow the eye with the open panel
following, Esc closes with the focus on the door and the scrim gone, Enter toggles, Tab walks the panel, the focus leaving
the navigation closes it — W2-C1's model intact.

**Focus visible, never obscured.** Every stop of every cycle draws a 2 px solid ring (`tab_rings_missing` empty in all ten
cells) and every focused stop is whole on screen and uncovered (`tab_obscured` empty: the visible share inside the sheet's
scrolling body is 1.0 and no other element covers any of nine sample points) — the pinned foot never covers a focused row;
the body scrolls the next stop into view. On paper the ring is #1d8a93, 4.11 : 1 against the sheet's white on both sides;
on the night foot #7fd1d8, 9.93 : 1. The exception is M2 (1.75 : 1).

**Contrast on pixels** (299 visible texts, fr and ar: the sheet folded, every door unfolded, the bottom and the foot, the
side sheet, the band, the popover, the menu sheet, the tip; the computed ink against the mode colour of each text box's
screenshot; E/s4/s4.json). All text under 16 px measures **7.17 : 1** (the glosses and the second lines at 13 / 14 px, the
popover's caption) or more (the promoter at 12 px on night 9.94, its name 15.33, the targa's word 15.33, the tip 11.82, the
popover rows 16.23). The lowest texts: the primary in the sheet 5.29 : 1 (15 px, white on #12777f), «Voir l'espace» 6.32 : 1
(15 px), the language names 7.17 : 1 idle; the lock-up's words 5.41 / 6.03 are the logotype. Nothing under 4.5 : 1 (one
sample at 2.75 was a box straddling the foot's edge; the same link measures 6.32 everywhere else).

**Reduced motion is a real still** (every animation frame sampled; E/s5/rm.json). Under `prefers-reduced-motion: reduce` the
sheet opens and closes in one opacity of 66–68 ms (≤ 80 ms) with no translate and no transform at any frame — the phone's
12 px rise and the side sheet's slide are gone, fr and ar; the account popover and the menu sheet the same (66–67 ms, no
drop, no spring); the door chevron's turn is 0 ms (the tokens). Without it: «Quiet» on the phone (opacity 283 ms, the body
and the foot rising 12 px, out 183 ms), the side sheet sliding in from the inline end (fr from the right, ar from the left
— a drawer mirrors), the popover's 4 px drop (165 ms), the menu sheet's spring from the bottom. No animation runs once the
sheet has closed.

**Forced colours** (E/s5/fc-*.png, fc.json; judged by eye and computed): the sheet on the forced canvas, its text in
`CanvasText` and its links in `LinkText`; the side sheet keeps a 1 px `CanvasText` edge; the pinned foot loses its night
and keeps a `CanvasText` line above it; the popover and the menu sheet keep their borders; every focused stop has a
visible 2 px outline; the scrim's veil dims the page. Usable in fr and ar.

**Reflow and spacing** (E/s5/reflow.json, spacing.json). At 320 × 568, 320 × 256 and 844 × 390 (a phone on its side), fr and ar:
no horizontal overflow of the page, the sheet or its body; «Menu» 44 × 44 at 320 (its word screen-reader-only); every stop
whole when focused. At 320 × 256 the menu's body is 80 / 72 px: m1. Under WCAG 1.4.12's spacing (line-height 1.5, letters
0.12 em, words 0.16 em, paragraphs 2 em) at 360, 390, 768 and 1024: no clipped text, no text leaving its row, no
overflow; the letterhead wraps at 1024 instead of clipping.

**Targets** (every interactive element of the sheet with each door unfolded in turn; E/s5/targets.json). Under a finger at 360,
390, 412 and 768, fr and ar: **none under 44 px** — the languages 44 tall (44–62 wide), the doors 64, Forum and Projet 52,
the entries 48–134, «Voir l'espace» 44, the search field and its button 52, the primary 52, the anti-fraud link 44, the
targa and the account trigger 44 × the column, «Menu» / «Fermer» 44. On a fine pointer at 1024 and 1279: none under 24 px
(the languages 24 tall, as §1.11 sets). The popover's rows 36 on a fine pointer, 44 under a finger; the key alone 32 × 32
on a fine pointer (labelled 140 × 32 / 128 × 32 from 100rem), 44 × 44 under a finger.

**«La targa»'s key alone** (E/s23/s2.json): named «Espace réservé» at every width; below 100rem its word is drawn by the
system's top-layer tip — at once on the keyboard's focus, after the wait on hover — 6 px under the plate (106 × 28 fr, 94 × 28
ar); Esc puts it away while the focus stays on the plate; the pointer can move onto it without losing it; it leaves with the
pointer (WCAG 1.4.13). From 100rem the plate says its word and the tip is refused (1600, fr and ar).

**The no-script path** (E/s11/s11.json, nojs-*.png; JavaScript off, 390 fr + ar, 768 fr): «Menu» is a link to `#nav-sheet` and
the sheet shows in place (fixed, the full screen on a phone, at the inline end at 768), its stops in order with their
rings, the doors unfold natively, «Fermer» (a link to the letterhead) puts it away. No trap without the script, as designed.

## 3. Performance (lane 8; the budgets are judged on 8782 by the Performance Lead — these are the regressions to flag)

**CSS — the shared payload** (gzip −9 from the committed bundles of both commits, E/weigh_revs.json; the same on the wire
of the twin): every page type **−587 B** — an interior page 42 152 → 41 565, the home 56 803 → 56 216, the login 47 013 →
46 426, the console page types 50 893 → 50 306 (ceiling 50 927), «Mes pièces» 52 065 → 51 478. No page-only sheet grew;
the sheet is the drawer family drawn on the shared `.portico__*` rules. No CSS regression (V5.8 holds).

**JS** (static closures of each page's entries + `main.js` + `head.js`, gzip −9; E/js_per_page.json — the twin's bytes on the
wire are identical): the home 45 581 → 51 136 (+5 555), an interior page 38 006 → 43 559 (+5 553), the login 39 683 →
45 235 (+5 552), a console page 45 977 → 45 064 (−913). Module requests 6 → 7 on the home, 4 → 5 on an interior page,
unchanged on console pages. The overlay chunk 6 466 B (budget 4 KB, recorded), `nav` 3 529 → 3 133, `main.js` 5 408 →
4 872. M3.

**The A/B** — the head and the base on the same twin, interleaved by round (the order alternating), the W1-0 before set's
`measure()`: profile A (150 ms RTT, 1.6 / 0.75 Mbps), CPU × 4, cache off, a fresh profile per load, a tap / click on the h1,
Tab and «Menu» after 5 s of rest; n = 9 per cell and arm (18 for the one cell first at the resolution's edge); the machine
shared (CPU 5–54 % in the second before a load, median 19.5 % on the head's loads and 21.6 % on the base's). E/perf/summary-ab.json, 216 traces.

| Cell | LCP base → head (Δ) | LCP spreads base / head | FCP | First-render task | Longest load task (median; max b / h) | TBT | CLS max b / h | «Menu» open p90 b → h (max) |
|---|---|---|---|---|---|---|---|---|
| home fr 1440 | 1 504 → 1 468 (−36) | 1 368–1 600 / 1 328–1 584 | 1 192 → 1 172 | 72.6 → 70.9 | 125.5 → 107.3 (150 / 150) | 191.8 → 103.3 | 0.024 / 0.025 | — (the bar) |
| home fr 412 | 1 452 → 1 428 (−24) | 1 388–1 708 / 1 276–1 480 | 1 168 → 1 172 | 38.3 → 37.4 | 122.3 → 112.6 (177 / 133) | 102.5 → 120.2 | 0 / 0 | 72 → 128 (136) |
| home ar 1440 (n = 18) | 1 670 → 1 688 (+18) | 1 512–1 932 / 1 536–1 844 | 1 336 → 1 346 | 72.8 → 71.3 | 158.2 → 139.9 (264 / 165) | 316.3 → 263.6 | 0.019 / 0.018 | — (the bar) |
| home ar 412 | 1 732 → 1 660 (−72) | 1 508–1 828 / 1 484–1 868 | 1 348 → 1 328 | 42.2 → 40.7 | 163.6 → 152.9 (267 / 252) | 201.5 → 147.6 | 0 / 0 | 80 → 136 (176) |
| door page fr 412 | 1 028 → 980 (−48) | 1 000–1 212 / 952–1 148 | 924 → 900 | 78.5 → 40.9 | 84.4 → 70.5 (123 / 164) | 28.4 → 31.5 | 0 / 0 | 48 → 160 (160) |
| door page ar 412 | 1 264 → 1 152 (−112) | 1 188–1 368 / 1 116–1 280 | 1 088 → 1 060 | 55.0 → 45.7 | 150.4 → 129.2 (164 / 169) | 125.0 → 106.2 | 0 / 0 | 56 → 136 (144) |
| pooled medians | 1 524 → 1 472 | | 1 192 → 1 188 | 62.8 → 46.2 | 136.6 → 124.6 | 180.6 → 134.4 | | |

- **LCP and its element:** no cell worse than the plan's resolution (+50 ms); the element is the same on both arms in every
  load — the hero's photograph (`img`) on the home, `p.page-header__lead` on the door page. Against the W1-0 before set
  (8782 at `v54/base`, a quieter machine) the home's element changed from V4's `image.doorway__img` / `p.hero__body` to the
  hero port's `img` — W2-D's change, not this family's — and its LCP is lower (1 428–1 688 against 2 064–2 356 ms).
- **Long tasks:** none introduced. The longest load-phase task (to the first input, ≈ 5 s, so the idle work is in it: the
  overlay module's idle measures, the scrim made at idle, the portico's layout) is equal or lower on the head in every
  cell, and so is TBT except two small rises inside the spread (home fr 412 +18 ms, door fr 412 +3 ms). The first render
  holds the long task, as on the base.
- **CLS:** ≤ 0.025 on every load of both arms (flagship ≤ 0.05 holds); the sheet and the popover open with no shift.
- **The sheet's cold open (N9):** p90 128 / 160 ms (fr home / door page), 136 / 136 ms (ar), max 176 ms — under 200 ms at
  CPU × 4 on the compressed twin; V4's drawer was 48–80 ms (§1 «Not findings» (e)).
- **At rest, nothing loops** (E/s11/s11.json; the home and a door page, 390 and 1440, fr and ar; 3 s windows after load, with the
  sheet open, after its close, after the pointer crossed the bar): 0 rAF callbacks, 0 long tasks, 0 running animations,
  0 style recalculations, 0 layouts, ≈ 0.5 ms of task time per window.
- **Requests and bytes before `load`** (the twin, every load): the home 3 CSS + 9 JS (base 3 + 8), the door page 1 + 7 (base
  1 + 6); images unchanged; N8 holds — no portrait photograph requested on a phone (W2-C1's policy, unchanged; the review
  and the builder measured it with the sheet open and every door unfolded).

## 4. Protocol, instruments, caveats

- Accessibility series on the lane's dev server (DEBUG on, uncompressed): `s1_keyboard.py`, `probe_zorder.py`, `s23_targa.py`,
  `probe_scrimtap.py`, `probe_menu_tokens.py`, `probe_console_menu.py`, `s4_contrast.py`, `s5_modes.py` (rm · fc · reflow ·
  spacing · targets · axe · ax), `s12_portico.py`; helpers in `rig.py` (the stop facts: ring, visible share inside every
  clipping ancestor, nine-point coverage; the pixel ground = the mode colour of a screenshot of the text box). The text
  spacing and axe runs alone used a CSP-bypassing context (to inject the sheet and the library); every other context kept
  the CSP and reported **0 console errors, 0 page errors**; the lane's log shows 3 057 requests, 0 errors.
- Timings on the twin (8798): `ab.py` + the W1-0 tools (`tools/trace.py`, `analyse.py`, byte-identical to W2-A's copy but for
  the constants and one added cell, the door page), `summ_ab.py`; `s11_rest_nojs.py` against the twin's head. Lane timings
  are a regression screen; the budgets' PASS is the Performance Lead's on 8782 (§2.6, §2.8).
- Emulated phones, touch and media (`is_mobile`, `has_touch` → `pointer: coarse`, reduced motion, forced colours); no Safari,
  no Firefox (O10 is not covered here: no engine installed), no real device, no screen reader run (the tree through CDP).
- One instrument mistake corrected during the check: the first contrast pass measured texts inside closed `<details>` and
  sampled a ring's «inside» on a button's fill; the re-run filters unrendered content (`checkVisibility`) and samples the
  ring's true neighbours; only the re-run's figures are reported.
- Data writes: one session row on `ile_v5_l8`, deleted; `last_login` and an `auth.login` audit row from the mint, as every
  minted session. Nothing typed, no password used.

## 5. Tests

None of the suite run by this role (V5.5: the integration checkpoints run it; the family's targeted tests were green at
`549428e` for the builder and for the review — `test_nav_sheet_w2_c2` 10, `test_browser_w2_c2` + `test_rtl_browser_w2_c2`
15). Neither M1 nor M2 is covered by them: M1 wants a touch tap on the menu sheet's scrim inside the open sheet, M2 the
outline colour of a focused row of the foot's menu — both written as the acceptance in §1.
