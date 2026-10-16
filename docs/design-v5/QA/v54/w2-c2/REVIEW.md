# W2-C2 · The navbar, part 2 — the senior review (design + UX + taste, one pass)

Reviewer label `w2-c2-review`, V5.5 delivery mode (implement → review once → fix → ship). Nothing was built by this
reviewer. Reviewed: branch `v54-w2-c2` at `549428e` (clean worktree), on the reviewer's own server `127.0.0.1:8888` run
from `C:/tmp/ile_wt/v54-w2-c2` on `ile_v5_l8` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`), headless
Chromium 153 (one browser at a time, closed after each run), the signed-in header through a session minted with
`Client.force_login` (no password). Pages: `/fr/` and `/ar/` at 360 · 390 · 412 (touch) · 768 (touch) · 1024 · 1279 ·
1366 · 1440 · 1680, signed out and in; `/fr/compte/login/`, `/ar/faq/`, `/ar/parcours/`, `/fr/le-projet/`, a phone in
landscape (844 × 390), an iPad in landscape (1024 × 768, touch), a desktop window with a classic scrollbar (1024–1279).
The builder's `NOTES.md` and DL54-96 were read first. Evidence (captures, probes, INP series) under
`C:/tmp/ile_v5_council/evidence/v54/w2-c2/review/` (E/ below); scripts under
`C:/tmp/ile_v5_council/.work/w2-c2/w2-c2-review/`.

## Verdict — SHIP_AFTER_FIXES

No P0: no page is broken, every direction is right, nothing is unusable, no data or security problem. The phone sheet and
the account popover are at the bar. Two majors, both cheap, must go before the merge: the French letterhead breaks onto
two rows in the 1024–1279 band on an iPad in landscape and in a Windows-sized desktop window, and the tablet sheet
(48–80rem) has lost its pinned foot — no «Espace réservé», no account entry, a third of the panel blank. Then seven
minors.

## The judgement against the bar

**The phone sheet is the owner's Fase 3 drawer, developed — and it is premium.** Against the comp at 390
(`proof/shots/home/phase3-menu-390.png`) the order and the anatomy are the same: the languages first, the four doors on
discs, the hairline, Forum with its glyph and Projet without one (as in the comp), the search, the primary, the
anti-fraud line, the targa and the promoter in a pinned foot. The build adds what the comp only promised: the doors
unfold in place (an exclusive `<details name>`, the current section's door open on an interior page) with the door's
locked gloss, its entries with whole second lines and «Voir l'espace» — the desktop panel's content, without the
photograph that N8 keeps off phones; the discs turn night; the foot sits on the institutional bar's night with the gold
key at 44 px. The head line is the letterhead's own row, so the lock-up does not move when the sheet opens. At 360 the
words of «Menu» and «Fermer» give way to the glyph and nothing reflows. In Arabic everything mirrors as it should
(discs and labels at the right, chevrons at the left, the primary's arrow turned), and the phone's rise has no sideways
travel. It is one product with the hero and «Il portico»: the entries, «Voir l'espace», the anti-fraud foot and the disc
are literally the bar panel's drawing (`.portico__*`, one rule set for both places), the night is the institutional
bar's, the key is the hero's. Credible beside the references at 360–412. (E/shots/390-fr-1-open.png, 390-fr-2-door1.png,
390-ar-1-open.png, 360-ar-2-door1.png, 412-ar-3-scroll1.png.)

**The signed-in targa's popover is quiet, correct and keyboard-complete.** One plate in the letterhead (the person glyph
alone below 100rem, 32 px on a fine pointer, 44 under a finger), named «‹name› — Mon compte»; the menu hangs from the
trigger's inline end (its right edge on the trigger's in French, its left edge in Arabic), four rows and a rule, no
motion beyond the system's 4 px drop. Enter opens it with the focus on the first row (ring visible), ↓ ↑ wrap, Home /
End, Esc closes and gives the focus back to the trigger, Tab out of the last row closes it, Shift+Tab back to the trigger
keeps it, a second press on the trigger closes it, a press outside closes it, a door's pinned panel closes when it opens.
In the phone sheet's foot it becomes a bottom sheet over the one scrim, headed «Mon compte»; Esc closes the menu alone
and the sheet stays. (E/probe-targa-1440-fr-in.json, -ar-in.json; shots/targa-1440-fr-in-2-open-kb.png,
390-fr-in-5-account.png, 1440-ar-in-4-account.png.)

**Through overlay.js — for the sheet and the popover, entirely.** The sheet is the system's drawer: `show()` +
`aria-modal`, the focus on «Fermer» in the tap's task (0 animations on the first frame of a keyboard open), the trap
(17 stops at 390, Tab and Shift+Tab wrap, nothing outside reachable), the rest of the page `aria-hidden`, Esc / «Fermer» / the
scrim / a link close it, the focus back on «Menu», the page held without moving (scrollY unchanged, the wheel on the page
does nothing), a close request — the Android Back gesture's path — closes it through the same module, no history entry,
a window widened past 80rem puts it away with the focus on the lock-up, bfcache brings the page back clean. The
desktop portico panel is still on W2-C1's adapter (m2): accepted for now, the contract has no primitive for it.

**Motion.** Below 48rem «Quiet» exactly: opacity in 320 ms with the body and the foot rising 12 px, out in 200 ms, the
leaving panel inert; from 48rem «Slide» from the inline end, out by the same edge, mirrored in Arabic; a close at 70 ms
and a reopen continue from the pose (O1); reduced motion is one 80 ms opacity with no transform in any frame, at 390 and
768. (E/probe-motion-*.json.)

## Findings

### Blocking — none

### Major

**M1 — In the 1024–1279 band the French letterhead breaks onto two rows on an iPad in landscape and in a Windows-sized
desktop window.** The band's row needs 945 px in French under a coarse pointer (the targa and the signed-in trigger grow
to 44 px) and 933 px under a fine one; the column is 944 px at 1024, and 929 px when the window draws a classic scrollbar
(Windows Chrome / Edge, a mouse on macOS). Result at 1024: «Personnes Entreprises Institutions» on one row,
«Universités & Formation» under it, a 129 px sticky letterhead — the default French home on an iPad in landscape,
signed out and signed in, and in a 1024 px window (a 1280 px laptop screen at 125 %) on Windows. Even on a fine pointer
with no scrollbar the spare is 11 px, against N11's «≥ 24 px spare at 1024 px in the longest language». English is at
8 px (coarse) and 5 px (scrollbar); Italian and Arabic hold. The bar was drawn by W2-C1 and the coarse 44 px widths
predate this step, but the 1024–1279 band is this family's brief and the navbar ships as one.
Evidence: E/probe-wrap.json, probe-wrap-touch.json, probe-wrap-in.json; shots/ipad-1024-fr.png,
gutter-1024-fr-0-before.png. **Fix:** in the 64–80rem band draw the lock-up at the compact 32/17 the 80–90rem band already
uses (≈ 45 px back), or trim the doors' padding and the row's gaps; then measure ≥ 24 px spare at 1024 under a coarse
pointer and with a 17 px classic scrollbar, fr · en · it · ar, signed out and in, and add the coarse case to the band's
browser test.

**M2 — The tablet sheet (48–80rem) has no pinned foot: no reserved-area entrance inside the open menu, and the panel
ends in blank paper.** `chrome.css` §7 hides `.nav-sheet__foot` from 48rem on the reasoning that «the letterhead keeps
its lock-up, la targa and the promoter» — but the targa sits at the inline end, exactly where the side sheet arrives,
so while the menu is open it is under the sheet and `aria-hidden` (measured at 768: the targa at x 580–624, the sheet
at 348–768; mirrored in Arabic). On an iPad in portrait the person who opens «Menu» to sign in finds no «Espace
réservé», signed in no account entry; and the sheet stops on the anti-fraud line with 283 px of empty paper below it at
768 × 1024, 438–470 px at 1024–1279 where it carries only Forum · Projet · the languages · the search. Plan §1.12 item 8
(and this review's brief) name «the phone and tablet sheet … the targa and the promoter sit in the pinned foot».
Evidence: E/probe-sheet-geometry.json; shots/768-fr-touch-2-sheet.png, 768-ar-touch-3-sheet-door1.png,
1024-fr-2-sheet.png, 1279-ar-in-2-sheet.png. **Fix:** keep the night foot from 48 to 80rem (hide only the head's
duplicate lock-up there), so every sheet ends the same way: «la targa» at 44 px or the account popover's trigger, and
the promoter; re-check the trap's stops and the 44 px targets at 768 and 1024.

### Minor

**m1 — With a classic scrollbar the scrim and the side sheet stop at the gutter: an undimmed 15–17 px strip runs down
the window's edge.** The scroll lock keeps the gutter (`scrollbar-gutter: stable`, nothing moves sideways — verified),
but neither the scrim (`inset: 0`) nor the inline-end sheet reaches into it; in Arabic, where the sheet is on the left,
the bright strip stands beside the dimmed page (E/shots/gutter-1024-ar-1-open.png, gutter-1024-fr-1-open.png). The scrim
and the lock are W2-A's and every trapped modal shows it; route to W2-A: let the scrim cover the gutter (e.g. a
`100vw` inline size) and let an inline-end drawer meet the window's edge.

**m2 — The desktop portico panel is still on W2-C1's adapter, not overlay.js (plan §1.12 item 6, §3.4 item 5's gate).**
Accepted as a deferral: the contract opens kinds (dialog, alert, drawer, sheet, popover) and its popover family would
top-layer, place and key the panel, breaking N1, the portico's keyboard model and the photographs' cross-fade —
verified in `overlay.js`. One user-facing gap follows from it: the adapter closes a pinned panel on focusout, Esc or its
scrim, and a press on «Menu» or on the targa in Safari and on an iPad does not move the focus, so a pinned panel would
stay open under the sheet or beside the popover (not reproducible in Chromium, where it closes — E/probe-interplay.json;
WebKit not run). **Fix now, in nav.js:** close the open panel on any `overlay:open` the system dispatches; track W2-A's
disclosure primitive and this family's switch so the gate item is not lost.

**m3 — The tablet sheet uses the page's 40 px grid margin inside a 420 px panel.** Its column is 339 px, narrower than
the phone's 350, and the primary «Découvrir le questionnaire d'orientation» breaks onto two lines at 768
(E/shots/768-fr-touch-2-sheet.png). Give the side sheet its own padding (24 px) from 48rem.

**m4 — Unfolded on the phone, the door's gloss reads as one more grey second line.** The desktop panel sets the gloss as
the lede (20 px, ink); the sheet sets it at 13 px in `text-2` — exactly the size and ink of the entries' second lines
just below it (computed at 390; E/shots/390-fr-2-door1.png). Give it the lede's voice (a step up, in ink) so the unfolded door reads as the door card
opened.

**m5 — «Menu» and «Fermer» are not the same width, so the head's button jumps when the sheet opens.** 84 → 95 px in
French (its leading edge moves 11 px), 87 → 77 px in Arabic, and during the 320 ms cross-fade both outlines show
(E/shots/390-fr-1a-opening-60ms.png). One width for both words per language (the longer one's), so only the word and the
glyph change.

**m6 — Signed in, the targa's trigger sits 2 px high in Arabic.** `.account-menu` is a block whose line box takes
Vazirmatn's 32 px strut (36 px tall), so the trigger's middle is at 62 against the row's 64 at every width from 48rem.
`.targa-seat .account-menu { display: flex; }` centres it (verified 62 → 64; E/probe-seat-offset.json); the sheet's foot
has the same wrapper.

**m7 — The chrome's links flash Android's default tap highlight.** Only `.btn` sets `-webkit-tap-highlight-color:
transparent`; «Menu», «Fermer», the door rows, the entries, the languages and the targa show the browser's tint on a tap
(seen in the 60 ms frame of the opening). Set it on the chrome's interactive elements.

## What was checked and holds

| Item | Result |
|---|---|
| N8 photographs | the sheet draws none; on a phone none of the four portico photographs is requested — after `load`, idle, the sheet opened and every door unfolded, fr and ar (the six requests are the hero's own) |
| N9 cold open, CPU × 4, 390 × 844, n = 9 | open p90 fr 152 ms (median 136), ar 160 ms (median 128); close p90 fr 144, ar 192 — all ≤ 200 ms (E/inp-fr-ar-n9.json; the machine at ≈ 24 % CPU) |
| N13 targa | seated in both states; 32 px on a fine pointer, 44 under a finger; the key alone named (`aria-label` + the layer tip on hover after 400 ms and at once on the keyboard's focus, Esc hides it without moving the focus); the word and no tip from 100rem (1680); flag off: the builder's test green |
| N14 targets | none under 44 px in the sheet under a finger at 360 · 390 · 412 · 768, fr and ar, every door unfolded; «Italiano»'s ring whole inside the body's clip in both directions; an unfolded door adds no glyph |
| N19 Arabic | the architrave under the open door; the account menu on the trigger's inline end (left edges equal); the side sheet comes and goes by the left; the phone's rise vertical |
| O2–O8 | exit by the entry edge, inert while leaving; state and focus at t = 0; reduced motion opacity-only 80 ms; Esc everywhere, focus back on «Menu» / the trigger; CLS 0; no horizontal scroll at any width |
| Back | a close request (`requestClose()`, the Android Back gesture's path) closes the sheet through overlay.js with the focus back; opening pushes no history entry |
| No script | «Menu» shows the sheet in place (`:target`), the doors unfold natively, «Fermer» puts it away |
| WCAG 1.4.12 | under the spacing sheet nothing in the sheet is clipped or pushed out, 390 |
| Forced colours | the discs become glyphs, the lines `CanvasText`, the pinned foot keeps its line |
| Health | 0 console errors, 0 CSP violations on every capture; the login, the FAQ, a door page and a phone in landscape draw the same sheet |

## Measures

- **Shared CSS (V5.8)**, gzip −9: `main.css` 42 152 → 41 565 B (−587 on every page type), `portal/console.css` 6 809 →
  6 809, `core/overlay-panels.css` 2 071 → 2 071 — the shared payload goes down.
- **JS on the home**: 51 136 B gzip (the overlay core's 6 466 B now on every public page, as plan §2.3 puts `overlay.js`
  in `shell.js`) against §2.6's 45 KB public-page line, which the home already passed at 45 584 B — recorded, not a
  finding: LCP 308 ms (390) / 272 ms (1440) on the lane, CLS 0.

## Tests run (lane 8, one pytest and one browser at a time)

`tests/frontend/test_nav_sheet_w2_c2.py` — 10 passed; `tests/frontend/test_browser_w2_c2.py` +
`tests/i18n/test_rtl_browser_w2_c2.py` — 15 passed, no crashed run. `scripts/check_ownership.py w2-c2 361b03d`: 16 paths
outside the slice, each justified in `NOTES.md` (the drawer's deletion, W2-A's hand-overs) — for the merge step to write
into the manifest.

## Not covered

WebKit and Firefox (O10) were not run — no engine is installed here; the sheet's `<summary>` rows drawn as grids,
`<details name>`, `closedby` and Safari's focus-on-press behaviour (m2) are the points to watch at the integration
checkpoint.
