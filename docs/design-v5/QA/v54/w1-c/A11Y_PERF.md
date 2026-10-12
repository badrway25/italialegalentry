# W1-C — core components · accessibility + performance check (one pass, V5.5)

Italy Legal Entry™ · design V5 · V5.4 plan §1.2, §1.4, §1.6, §1.8, §2.6, §3.3 item 7 · V5.5 delivery mode · label
**w1-c-a11y-perf** · 9–10 October 2026 · branch `v54-w1-c` at `04f43e9` (the code under test; `7e867e4` adds the senior
review's report and no code) against its merge base, design-v5 `8246a7f` · lane 8, `127.0.0.1:8788` on `ile_v5_l8`
(`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`; the preview routes on for the chip board only).
I built nothing. One pass: accessibility on the real pages in French and in Arabic, performance against the family's
own merge base and against W1-0's manifest.

## Verdict — SHIP_AFTER_FIXES

No P0. The family is accessible where it was measured: 2 430 keyboard stops on its parts, each `:focus-visible`, the
ring on pixels at 3.44 : 1 or more against its ground wherever nothing covers it; no text of the family under 4.5 : 1
on 1 757 boxes read on pixels, every state word at 7 : 1 or more («nullo» 5.38 by design), every mark at 3.28 : 1 or
more; the tabs and the disclosure keep the WAI-ARIA model in both reading directions; reduced motion is a still;
forced colours keep every kind and every state; under a coarse pointer every control of the family but one is hit in
44 px, and 25 controls a finger could miss on the merge base no longer are.

Four things are to fix before shipping — each a few lines in the family's own files:

- **A1** — a link-style button no longer wraps in a console panel head: the person's dashboard overflows by 51 px at
  320 px where the merge base overflowed by 9;
- **A2** — the field component writes its errors as `<ul role="alert">`, which takes the list away from its items: axe
  fails on every console form that shows an error;
- **A3** — the text link with its arrow is hit in 24–40 px under a coarse pointer where the plan asks 44, and the
  family made eight of them smaller;
- **P1** — one selector of the card sheet makes **every page of the site** recalculate all its styles a second time
  when the parse ends: style time + 25 %, 0.6 to 1.0 more task over 50 ms a load at CPU × 4.

A1, A3 and P1 were tried on the lane with the fix in place (§ Findings); A2 is one template line. Seven one-line items
follow (A4 … A10).

Performance otherwise holds: bytes inside the Wave-1 allowance with 1.2 KB or more to spare on every page type, the
same LCP element in every cell, CLS 0.034 at most, the first-render task, the longest task and LCP equal to the merge
base's (the plan's two tolerances are not touched), nothing of the family running at rest. With P1's selector changed
the long tasks are the merge base's again (5.6 = 5.6 a load).

## What was measured

Everything on lane 8, headless Chromium (Playwright 1.63, `HeadlessChrome/153`), one browser at a time, this label's
own profiles, seven sessions minted with `Client.force_login` (no password used, typed or stored) and revoked at the
end. The benchmark lock was never present; no run ended on «Target crashed».

| Series | What | Size |
|---|---|---|
| Sweep 320 × 640 (fine pointer) | overflow and its offenders, clipped text, targets, hit boxes | 168 cells (91 page types, fr + ar) · the same on the merge base |
| Sweep 390 × 844 (emulated phone, `pointer: coarse` asserted in every cell) | overflow, every target's **effective** hit box (`elementFromPoint` along its two centre lines) | 168 cells · the same on the merge base |
| Sweep 1440 × 900 | targets, axe-core 4.13.0 (WCAG 2.0–2.2 A / AA), layout shifts, the page's requests | 168 cells · the same on the merge base |
| Keyboard walks, real Tab and Shift+Tab | at each stop: `:focus-visible`, the ring found on pixels on its four sides and its contrast, what lies over the focused box | 316 walks, 10 480 stops, 3 449 outside the chrome, 2 430 on the family's parts (47 page types, the showcase, the chip board, 4 error states; fr + ar, 1440 and 390, both directions) |
| Contrast on pixels (DPR 2) | the first line of every label, help, error, value, placeholder, button, tab, row, chip word, tag, notice, card text; rest, hover, press; edges and marks | 1 422 + 200 + 135 text boxes, 910 edges and marks (70 + 24 page × language cells, the chip board) |
| Components | tabs and disclosure with real keys (fr, ar); names, roles and references on 54 page × state × language cells; axe on 40 state cells (errors shown, a row open, a tab chosen) | — |
| Reduced motion, forced colours | emulated media: seven gestures, two captures 150 ms apart; the boards and nine product pages for the eye | fr + ar |
| WCAG 1.4.12 text spacing | the four overrides through a constructed style sheet, before and after | 11 pages, fr + ar, 1440 and 320 |
| The chip board (preview routes) | the eight registers × stone, sheet, night × fr, ar: words, marks, 320 px, forced colours | 1 page |
| Traces, profile A (150 ms, 1.6 Mbps, CPU × 4), W1-0's analysis | branch and merge base in alternating blocks, same port, data and sessions | 135 + 99 loads on 19 cells; 24 + 24 matched loads with the whole load broken down; then three arms — branch, branch with P1's fix, merge base — 24 matched loads each |
| Why styles are recalculated | Blink's invalidation tracking and selector statistics on both arms; the bundle rewritten in flight (as is / the rule removed / the selector fixed); every box of the pages that use the rule, before and after | both arms at CPU × 1 and × 4 (64 loads); 45 loads through the rewrite; 92 pages scanned; 15 page × width cells for the boxes |
| Main thread at rest | style recalculations, layouts and running animations in three idle seconds | 22 cells, both arms |

## Accessibility

### Keyboard — fr and ar, 1440 and 390, forwards and backwards

- **Every stop of the family shows `:focus-visible` and the one ring.** 2 430 stops on the family's parts; the ring was
  found on pixels on every one that nothing covers (below). The only stops without the system's ring are the calendar
  button inside a date field, reached with Shift+Tab (six fields): the browser's own black ring shows there (A9).
- **Tabs** (the showcase; no product page uses them yet): arrows move selection and focus together and wrap, **reversed
  in Arabic**; Home, End; Tab goes into the panel and Shift+Tab comes back; roving `tabindex`, `aria-selected`,
  `aria-controls` and `aria-labelledby` resolve; the indicator stands under the selected label within 1 px in both
  directions; a key's change is static (0 running animations, `html[data-input="key"]`), a pointer's travels.
- **Disclosure** (FAQ and showcase): Enter and Space open and close, a link to a row opens it, in both languages.
- **Forms**: after an empty submit the focus is on the summary (`#form-errors`); each link of the summary reaches its
  field; a date field takes its three inner stops and lets the walk go on.

### The ring, on pixels (plan §1.6)

| Ring | Ground beyond it | Stops | Contrast |
|---|---|---|---|
| `#1d8a93` | `#ecebe6` (band) | 32 | **3.44** |
| `#1d8a93` | `#efeeeb` · `#f0eeea` | 80 | 3.54 · 3.55 |
| `#1d8a93` | `#f4f3f0` (stone) | 2 158 | 3.70 |
| `#1d8a93` | `#fdf2f1` (error wash) · `#f3f5f8` (information wash) | 87 | 3.72 … 3.76 |
| `#1d8a93` | `#fbfaf8` (sheet) | 524 | 3.94 |
| `#1d8a93` | `#ffffff` | 74 | 4.11 |
| `#7fd1d8` | night (`#0f2547` … `#0b1a33`) | 73 | 8.73 … 9.95 |

3 030 rings measured outside the chrome (2 333 on the family's parts; two more on a tinted row at 4.5), none under
3 : 1 against the ground beyond it. On the 479 stops of a public text field the two pixels that touch the ring are its
own halo: **2.58 : 1** on stone (359), 2.71 on the entrance sheet (119), 1.67 for the one field on night (ruling R1).

### Focus not obscured (WCAG 2.4.11)

No part of the family hides a focus, and the site header hides none (W2-C1's scroll padding holds in both directions).
Three bars of other families do — all three the same on the merge base (walked there too): the console's fixed bottom
bar at phone width (O1), the pathway page's sticky section bar (O2), the wizard's sticky foot (O3).

### Names and roles

- 312 controls on 54 cells: **0 without a name, 0 dangling `aria-describedby` / `aria-controls` / `aria-labelledby`**;
  30 invalid controls, each with `aria-invalid` and a description; required fields carry `required` and the page says
  what the asterisk means; 50 chips: the mark `aria-hidden`, the word present, never focusable; notices `status`,
  errors `alert`. The show / hide control of a password says its state twice (A10).
- **axe, 168 cells at 1440:** 3 nodes, none the family's and all three on the merge base too — the Forum
  registration's eyebrow (1.36 : 1, fr and ar) and one paragraph of the pre-evaluation (O4). The login's
  `target-size` node of the merge base is gone.
- **axe on states:** the public forms with their errors, the FAQ with a row open: clean. **The console forms with their
  errors: `listitem` (serious)** — A2.

### Contrast on pixels

Text (first line of each box, DPR 2; weakest pair of each kind, 1440 and 390):

| Part | Weakest pair | Ratio |
|---|---|---|
| label · legend | `#15222a` on `#f4f3f0` (console label `#4a5a62` on `#fbfaf8`: 6.87) | 14.62 |
| help · placeholder · required mark · error | `#4a5a62` on stone · `#55646b` on white · `#932039` · `#830a2c` | 6.46 · 6.14 · 7.55 · 9.26 |
| primary: rest · hover · press | white on `#12777f` · `#0f6a72` · `#0b555c` | 5.29 · 6.32 · 8.51 |
| ghost · link button: rest · hover | `#0f6a72` · `#0b555c` on stone | 5.69 · 7.67 |
| disabled (exempt) | `#55646b` on `#e3e2dd` | 4.73 |
| in the hero (under 16 px: 7 : 1 asked, CL-6) | paper plate `#15222a` on `#fbfaf8`; secondary `#eef1f6` on `#16304f` | 15.56 · 11.82 (hover 13.59 · 10.08) |
| tab: rest · selected | `#4a5a62` · `#15222a` on stone | 6.46 · 14.62 |
| tag · show / hide control | `#15222a` on white · `#0f6a72` on white | 16.23 · 6.32 |
| notice title · body | `#434f5c` on `#f3f5f8` (information) · `#830a2c` on `#fdf2f1` (error) | 7.66 · 9.36 |
| card eyebrow, meta · text · title | `#55646b` on `#fbfaf8` · `#4a5a62` on stone · `#15222a` | 5.88 · 6.46 · 14.62 |
| text link with arrow | `#0f6a72` on `#ecebe6`; on night `#7fd1d8` | 5.29 · 9.93 |

1 757 boxes, **0 under 4.5 : 1** (3 : 1 for 24 px and more). The state words, where the system asks 7 : 1 (the council's
COLOUR; «nullo» is AA by design), on the chip board:

| Register | conforme | esame | neutro | attesa | azione | rifiuto | blocco | nullo |
|---|---|---|---|---|---|---|---|---|
| word on stone, sheet | 13.59 | 8.71 | 7.23 | 7.25 | 7.18 | 8.79 | 11.34 | 5.38 |
| word on night | 11.82 | 7.06 | 7.03 | 7.03 | 7.03 | 7.06 | 7.80 | 7.06 |
| mark on its body (paper · night) | 13.59 · 11.82 | 3.77 · 3.94 | 5.09 · 5.00 | 3.42 · 3.61 | 5.12 · 5.12 | 7.17 · 6.81 | 8.71 · 8.13 | 3.28 · 3.44 |

Edges and marks (3 : 1): the hairline of a field, a checkbox and a secondary button, `#7a868b` — 3.37 on stone, 3.59 on
the sheet, 3.74 against a white fill; the invalid edge `#932039` 7.55; a primary's fill against its ground 4.43 at
least; a checked radio's edge 7.67; the notices' marks from 3.63 (warning) to 13.59 (success). The tick of a checked
box: 3.07 (ruling R2).

### Reduced motion, forced colours

- **Reduced motion is a still.** Every duration token is 0 ms and every transition of the family computes to 0 s; on
  seven gestures (a tab chosen by pointer, a primary held down, a field focused, a box ticked, a row opened, an arrow
  button and a card under the pointer) nothing runs in the same task, two captures 150 ms apart are identical and the
  first equals the last. One exception, in Arabic: A4.
- **Forced colours are usable.** Buttons keep their hierarchy by their borders (primary a second line, danger dashed,
  ghost and link in `LinkText`), fields a border (2 px when invalid), the native select and checkbox come back, chips
  keep mark, word and the style of their edge on the three grounds, notices their rule (dashed, double), the tab
  indicator and every ring are `Highlight`. One loss: A5.

### 320 px (WCAG 1.4.10) and text spacing (1.4.12)

- **320 px, 168 cells:** overflow on 3 cells, 7 on the merge base. Four got right (the file control of the upload and of
  a requirement, 28 px over at the base, fr and ar); the wizard's foot is as it was (O3); **one got worse — A1**.
  Clipped text 224 = 224, targets under 24 px 12 = 12 (the wizard's own 20 px radios).
- **Text spacing, 44 cells:** at 1440 no overflow and no clipped text appears; one chip's word stands 6 px out of its
  pill on «Mes pièces» (the row's state column is as wide as the word: W3-C's). At 320 with the spacing on top, the two
  `nowrap` buttons of the console's panel heads run 40 and 58 px over (A1's root, and O5).

### Targets

- **Fine pointer (1440 and 320):** every target of the family is 24 px or more (629 targets a sweep): boxed buttons
  36 / 44 / 52, link buttons and text links 24, tags 24–25, checkboxes 24, the show / hide control 44 with its halo.
- **Coarse pointer (390), effective hit boxes:** buttons, small buttons and link buttons 44; fields 44 or more;
  checkboxes 44 × 44 (24 on the merge base); the file control 44 (28); tags 45; tabs 44–45 × 57 or more; rows 56–80;
  the show / hide control 44. Against the merge base 25 controls came up to 44: 18 checkboxes, 4 file controls,
  2 radios, 1 field. **The text link with its arrow: 24–40 px — A3.**

## Performance

### Bytes (plan §2.6), as each page really requests them

CSS and JS of every request of the 1440 sweep, weighed as the twin serves them (hashed `url()`s, gzip 9):

| Page type | W1-0 before | Ceiling (+ 8 KB) | Merge base | **Branch** | Headroom |
|---|---|---|---|---|---|
| home | 39 114 | 47 306 | 46 832 | **45 840** | 1 466 |
| door page · interior page · public form · FAQ | 36 294 | 44 486 | 44 012 | **43 020** | 1 466 |
| login | 37 502 | 45 694 | 45 220 | **44 002** | 1 692 |
| dashboard · case file | 41 668 | 49 860 | 49 635 | **48 643** | 1 217 |
| «Mes pièces» | 42 839 | 51 031 | 50 806 | **49 815** | 1 216 |
| company dashboard | 42 541 | 50 733 | 50 508 | **49 516** | 1 217 |

`dist/main.css` 44 012 → **43 020 B** (ceiling 46 080). The console rows are 249 B above the implementer's table: the
page sheets grew with the loader family, which that table did not count; the ceilings hold. Script: `main.js` 4 537 →
5 566 B gzip (+ 1 029, served unminified, comments included); a public page 37 728 B, the home 40 106 B, against 45 KB;
requests before `load` are W1-0's or fewer. P1's fix adds 66 B raw to the bundle.

### Branch against its merge base — 19 cells, alternating blocks, CPU × 4, 5 to 8 loads a cell and arm

| | Merge base (mean) | Branch | Difference, stratified by cell and block |
|---|---|---|---|
| first-render task | 76.1 ms | 75.8 ms | −0.3 ms, p = 0.86 · by cell: median −2.0, from −23.5 to +6.3 (the plan's tolerance: +30) |
| longest load task | 151.2 ms | 155.0 ms | +3.8 ms, p = 0.37 · by cell: median −1.4, from −38.3 to +29.3 |
| LCP (lane) | 2 529 ms | 2 546 ms | +17 ms, p = 0.23 · by cell: median +4, from −172 to +140 (tolerance +50; one cell's own spread is ± 150) |
| LCP element | — | — | the same in all 19 cells |
| CLS, largest load | 0.036 | 0.034 | medians 0.000 in both arms |
| INP proxy (h1 or field click, Tab, checkbox) | 45.0 ms | 47.7 ms | +2.7 ms, p = 0.06 · 96 ms at most |
| tasks over 50 ms in a load | — | — | **+0.7 a load (+13.5 %), p < 0.001** |
| blocking time over the load (ms beyond 50 a task) | 231 ms | 267 ms | **+36 ms (+15.5 %), p < 0.001** |

The first paint is the merge base's; the load after it is heavier. The next section says where, why, and what one
selector does to it.

### The extra work after the first paint: one selector (P1)

**Where.** Six cells traced again with the whole load broken down by kind of work, the arms alternating, 24 matched
loads each — and a second time as a three-arm run. Style is the kind of work that moves:

| Profile A, CPU × 4 · means of 24 matched loads | Merge base | Branch | **Branch + P1's fix** | Branch − base | Fix − base |
|---|---|---|---|---|---|
| style self time, first run | 198.0 ms | 248.1 ms | — | **+50.1 (+25.3 %), p = 0.001**, 20 of 24 pairs | — |
| style self time, three-arm run | 186.7 ms | 233.4 ms | **197.1 ms** | **+46.7 (+25.0 %), p < 0.001** | +10.4 (+5.6 %), p = 0.10 |
| tasks over 50 ms a load | 5.6 | 6.2 (6.7 in the first run, p = 0.010) | **5.6** | +0.6, p = 0.07 | 0.0 |
| … of which led by style, over the 24 loads | 25 | 39 | **27** | | |
| all main-thread task time | 1 113 ms | 1 233 ms | **1 160 ms** | +120 (+10.8 %), p = 0.006 | +47 (+4.2 %), p = 0.085 |
| blocking time (ms beyond 50 a task) | 227 ms | 276 ms | 259 ms | +49 (+21.8 %), p = 0.007 | +32 (+14.3 %), p = 0.017 |
| layout self time | 220.9 ms | 234.9 ms | 236.5 ms | +14.0, p = 0.13 | +15.6 (+7.1 %), p = 0.025 |
| first-render task · longest task | 82.1 · 158.0 | 84.5 · 153.8 | 86.7 · 164.7 | p = 0.54 · 0.55 | p = 0.21 · 0.21 |
| LCP | 2 516 ms | 2 550 ms | 2 512 ms | +35, p = 0.16 | −4, p = 0.88 |

By page, style self time base → branch → fix: home 367 → 425 → **365**; login 158 → 174 → **160**; contact form 139 →
176 → 151; dashboard 166 → 215 → 189 (fr), 182 → 236 → 191 (ar); «Mes pièces» 108 → 174 → 126. The LCP element is the
same in the three arms in all six cells.

**Why.** `static/css/v5/card.css` l. 116, new with this family:

```css
.card > :where(section, div):only-child > * { margin-block: 0; }
```

A universal subject under a structural pseudo-class. Blink keeps one invalidation set per pseudo-class for the whole
sheet, and with `*` as the subject the set of `:only-child` is «the whole subtree». So every time the parser closes a
parent whose last element is already styled — `<body>` at the end of every page, then `.container`, `.portal__main`,
`.ws-grid`, a list — that element's **whole subtree is recalculated again**, whether or not the page holds a card.
Blink's invalidation tracking says it in so many words: «pseudo only-child» scheduled on `BODY`, then «Related style
rule», subtree. Such subtree marks: 2 to 13 in every load of the branch (20 loads) — **none on the merge base**
(10 loads). Selector matching itself costs the same in both arms (≈ 7 ms).

| Elements recalculated in one load, CPU × 4 | login | contact form | dashboard | «Mes pièces» | home |
|---|---|---|---|---|---|
| merge base (mean of 2) | 930 | 916 | 880 | 592 | 2 493 |
| branch (mean of 2) | 1 175 | 1 021 | 1 281 | 798 | 3 236 |
| of which the recalculation at the end of the parse | 256 | 267 | 415 | 219 | 752 |
| branch, the selector fixed in flight (median of 3) | 940 | 944 | 999 | 621 | 2 506 |
| subtree marks: as is → the rule removed → the selector fixed | 6 → 0 → 0 | 2 → 0 → 0 | 13 → 0 → 0 | 8 → 0 → 0 | 12 → 0 → 0 |

(What remains is on the two pages that gained the chips' marks: 32 and 23 more elements than on the merge base, each
mark with the tree its `<use>` draws.) On this desktop at CPU × 1 with no throttling the document is parsed before the sheet is
applied and the two arms recalculate the same elements (login 957 and 963, home 2 488 and 2 482): the redo only exists
when a page is styled while it arrives, which is every real load — and, coming after the first paint, it is why the
first render and LCP do not see it.

**After the load** the same rule answers every change of an only child. One empty element added beside an only child,
then removed, the bundle as is → the selector fixed: 297 → 6 elements recalculated on the dashboard (its workspace),
87 → 6 on the contact form (the footer), 215 → 66 on the home (the hero; the 66 are its own running animation).

**What remains with the fix, against the merge base:** style +10 ms (p = 0.10), most of it on the three cells that
gained the chips' marks; layout +16 ms (+7 %, p = 0.025) — some 26 ms of 1 113 at CPU × 4. No long task is added (5.6 =
5.6); the ones already there are a little longer for it (blocking time +32 ms). That is the price of the marks and of
the new field, not a regression to chase; the steward's run on 8782 under the lock has the last word on §2.6.

No other selector of the family has this shape. Two older ones have (`.notice:not(:has(.notice__icon)) > *`,
`[data-seat].is-seating > *`): both stop at their own component and both are on the merge base. A change of input
modality (`html[data-input]`) recalculates 15 to 84 elements in 0.3 to 2.1 ms: the six «key» rules are bounded.

### Against W1-0's manifest (24 traced cells; what does not depend on the server)

- **LCP element:** the same in 23 cells. In «Mon parcours» with results, Arabic, 1440 the largest text is now a list
  item where it was a paragraph — **on the merge base too** (3 loads of 3): the fonts' doing, before this family.
- **CLS:** 0.000 median in every cell, 0.034 at most (the login at 1440): under the flagship ceiling of 0.05.
- Milliseconds are not compared with the manifest: the lane serves uncompressed files with DEBUG on; W1-0 measured the
  compressed twin.

### Nothing loops

In three idle seconds, on 22 cells: 0 style recalculations, 0 layouts, 0 running animations — with a text field
focused too — on every page but the home, whose four endless `route-current` animations (181 recalculations) are the
V4 hero's and identical on the merge base. `initTabs`' ResizeObserver settles: the showcase is at 0.

## Findings — the family's (fix list)

### Major — before shipping

**A1 · A link-style button no longer wraps in a console panel head: the dashboard overflows at 320 px.** Person
dashboard with a saved pre-evaluation, French, 320 px (WCAG 1.4.10): the page is 371 px wide — «Voir le détail de la
pré-évaluation» is one 226 px line beside its title; on the merge base the same link wrapped (125 px, two lines) and
the page was 329 px. `v4/workspace.css` says `.panel__head .btn { white-space: nowrap }` (for «Nouveau besoin»); V3's
link button undid it, `v5/buttons.css` does not. *Fix:* `.btn.btn--link, .btn.btn--text { white-space: normal; }` in
`v5/buttons.css`. Tried: 51 → **0 px** (the base's 9 px go too), no button box moves at 1440 on six pages, one moves
at 390 (the same link, now on two lines).

**A2 · A field's errors are a list without a list** (`templates/components/form_field.html` l. 26, older than the
family and the family's file): `<ul class="form-field__errors" role="alert"><li>…` — the role takes the list
semantics away and axe fails `listitem` (serious; WCAG 1.3.1) on every form the component draws once it shows an
error: «Nouvelle demande» (2 nodes), «Nouveau besoin» (1), fr and ar, 1440 and 390; the showcase (5). The public
enquiry forms, whose partial has no such role, are clean. *Fix:* take the role off the list — drop it (the summary is
the alert and takes the focus on every form walked; each field stays wired by `aria-invalid` and `aria-describedby`),
or, to keep an alert by field, carry it on a wrapping `<div>` — and update the two assertions that pin it,
`tests/frontend/test_design_docs.py:948` and `:959`. Same line in three templates of other families: O6.

**A3 · The text link with its arrow is not hit in 44 px under a coarse pointer** (plan §1.4 SP-8, §1.8; WCAG 2.5.8's
24 px holds). `.link-arrow` is drawn by `v5/buttons.css` and is the one target of the family the coarse rules forgot:
71 of 76 on the sweep are hit in 24–40 px (69 on the merge base, in 28–33) — the home's «Voir l'Espace Personnes»,
«Toutes les actualités» … at 28–29. The family's own setting made eight smaller: the second actions of «Formation»
57 → 40 and 29 → 24 (fr), 65 → 25 and 33 → 25 (ar), the «Attention aux fraudes» link of four pages 29–33 → 25 in
Arabic. *Fix:* the tag's device — under `(pointer: coarse)`, `.link-arrow { position: relative; }` and a `::after`
with `inset-inline: 0; inset-block: calc(50% - var(--hit-primary) / 2)`. Tried: 29 → 45 px on the home, 24 → 44 on
«Formation», no box moves, no page height changes.

**P1 · One selector makes every page recalculate all its styles a second time** (`static/css/v5/card.css` l. 116;
measures and mechanism in § Performance). Style time +25 % over a load and 0.6 to 1.0 more task over 50 ms at CPU × 4,
on every page of the site, with or without a card; after the load, every change of an only child recalculates its whole
subtree. *Fix:* name the children — the same specificity, so nothing else in the cascade moves:

```css
.card > :where(section, div):only-child > :where(.card__eyebrow, .card__title, .card__text, .card__meta, .notice) {
  margin-block: 0;
}
```

(or give the wrapper a class and drop the structural test); update `tests/frontend/test_chips_cards_w1_c.py:291`,
which pins the old selector; rebuild the bundle. Tried three ways: in flight on five pages (the table above: subtree
marks → 0, elements recalculated back to the merge base's plus the chips' marks); on the geometry — the rule has three
producers on 92 pages scanned, the two phases of «Formation» and the showcase's sample, and with the fix **0 of 511
boxes move on «Formation»** (fr, ar; 1440, 390, 320) and 0 of 2 093 on the showcase, where removing the rule instead
moves up to 146 (the notice inside the first phase needs it); and as the third arm of the A/B (the branch exported
with that one selector changed): style 233 → 197 ms, tasks over 50 ms 6.2 → 5.6, the merge base's. A guard worth one
test: no universal subject (`> *`, ` *`) after a structural pseudo-class in an ancestor compound.

### Minor — one line each, in this pass

- **A4 · Reduced motion, Arabic: the arrow still leans.** `[dir="rtl"] .btn--arrow:hover .icon` (0,4,0) outranks the
  reduced-motion reset (0,3,0): 3 px at once under the pointer, in Arabic only. Add the two RTL selectors to the reset
  of `v5/buttons.css` (tried: `-3px` → `none`).
- **A5 · Forced colours: the error's mark is an empty ring** — the stroke and the point are gradients, which are not
  painted there; beside the words it reads as a radio button. In `v5/field.css`'s forced-colours block:
  `forced-color-adjust: none` and `CanvasText` for the mark's border and its two gradients (tried: the mark is back).
- **A6 · The halo reaches an invalid checkbox** (`:is(input, select, textarea)[aria-invalid="true"]:focus-visible`):
  plan §1.6 keeps it for text fields. Leave the box its ring alone (tried).
- **A7 · The tab list has no name.** `components/tabs.html` gives `role="tablist"` neither `aria-label` nor
  `aria-labelledby`; add a `label` to the contract before a product page uses the component.
- **A8 · A link in the meta line of a card that opens sits under the stretched title link** (no producer today):
  `.card--link .card__meta > :any-link { position: relative; z-index: 1; }`.
- **A9 · The calendar button of a date field keeps the browser's ring** (visible, black; not the system's):
  `::-webkit-calendar-picker-indicator:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 2px; }`. Optional.
- **A10 · The show / hide control of a password says its state twice**: its label and `aria-pressed` both flip
  («Masquer le mot de passe», pressed). One channel, whatever form the reviewer's M2 takes: a constant name with
  `aria-pressed`, or a name that changes and no `aria-pressed`.

## Rulings on the open points

- **R1 · The ring between two bands of its own halo (the implementer's point 1, the reviewer's m9): not a failure.**
  WCAG 1.4.11 measures the indicator against what is adjacent to *it*; a colour of the component that does not
  interfere «is subsumed into the color closest in brightness» (Understanding 1.4.11) — the halo is closer to the
  ground than to the ring. Against the ground the ring is 3.70 (stone), 3.94 (sheet); the field's own edge and foot
  rule are 4.11 on the plate. The plan's «both neighbouring colours» are those. If the ring is to hold 3 : 1 against
  every pixel that touches it, laguna-600 on text fields (3.33 on the halo) or a halo at α ≤ 0.16 does it: optional,
  through the steward (`v5/tokens.css`).
- **R2 · The tick (the reviewer's m1): measured on pixels, `#15222a` on `#12777f`, 3.07 : 1** — over 3 : 1 by a hair for
  the one sign of a checkbox's state. Take the reviewer's rule (white: 5.29).
- **R3 · The password's rules (the reviewer's M1):** the element `aria-describedby` names must hold the list — the
  `<div>` the reviewer asks for does; keep the id on it.
- **The console's fields without a halo** (the implementer's point 2): the ring is 3.70 – 3.94 on both sides; fine.

## Seen on the way — not this family's (each the same on the merge base)

- **O1 · W3-A — the console's bottom bar hides the focus at phone width, and at 400 % zoom** (WCAG 2.4.11): 15
  controls wholly covered and 6 by half on seven console pages when tabbing forwards at 390 (a field of «Nouveau
  besoin», «Remplacer la pièce», a date field …). `scroll-padding-block-end` for the bar's height where it is fixed.
- **O2 · W3-F1 — the pathway page's sticky section bar covers the first link of its sticky side column** («Tous les
  parcours réguliers») at 1440, and two tags at 390 reached backwards.
- **O3 · W3-D — the wizard:** its sticky foot covers the first field at 390 and runs 8–18 px over at 320; its own
  radios are 20 px (40 × 41 under a coarse pointer).
- **O4 · the pre-evaluation page, «03 Vérification»:** `.section--verso > .t-prose` is ink on navy, **1.06 : 1** (V1's
  `.t-prose { color: var(--ink) }` on a verso section) — unreadable; one line for the page's family.
- **O5 · W3-B —** `.panel__head` neither wraps nor lets its button wrap: with text spacing at 320, «Nouveau besoin»
  and «Voir mes documents» run 58 and 40 px over.
- **O6 —** the `role="alert"` list of A2 is also in `components/option_cards.html`, `portal/situation.html` (W3-D) and
  `news/_newsletter.html`.
- Others: the sign-up's name field has no `autocomplete`; the Forum registration's eyebrow (1.36 : 1); the diplomas'
  timeline lays its tags over each other at 1440; the showcase's sample table overflows below 463 px and its
  account-menu sample has no name (dev page).

## Instrument notes and limits

- A full-page capture drops the emulated phone's `pointer: coarse`: every measure here is taken before any capture.
- Contrast is the third pass of the tool: the first two read some boxes off their place (a sticky column, a page whose
  content arrives after a scroll, a section revealed while it was read) and are replaced; a box is now read again
  until two readings 90 ms apart agree.
- The first walks stopped at a date field's second inner stop; the four pages that hold one were walked again whole.
- A focus read in the same task as the key can be mid-way: the skip link slides in (visible 150 ms later), and a date
  field entered backwards scrolls smoothly (`html:has(:focus-visible)` is false on the calendar button).
- Traces: the lane's dev server, no lock held, the machine 32 – 60 % busy with other lanes; the arms are compared
  with each other only, matched by cell and round, by a permutation test (stratified, or sign-flip on the pairs).
  Emulated phones, Chromium only. The merge base is a plain export of `8246a7f`, the fix arm an export of `04f43e9`
  with the one selector changed in the sheet and in the bundle; both served on the same port, data and sessions.
- Invalidation tracking slows the engine: its counts are used, never its milliseconds. The in-flight rewrite answers
  the bundle from the driver, so both of its arms get the sheet sooner than a real load does; it is used for counts
  and geometry, and the three-arm run for time.

## Evidence

`C:/tmp/ile_v5_council/evidence/v54/w1-c/a11y-perf/` — `runs/` (every record: `reflow320`, `touch390`, `desk1440`
and their `-base` and `-board` twins, `walk-*`, `contrast-*`, `components-*`, `axe-states`, `spacing`, `fixsim`,
`idle-*`, `traces-*` with `-p5` and `-p10`, `selstats-*`, `invtrack-*`, `fixperf-*`), `walk-clips/` (the flagged
stops), `captures/` (`fc`, `rm`, `board`, `spacing`, `fixsim`), `bytes.json`, `*-summary.json` (`p5`, `p10`, sweeps,
walks, contrast, traces), `tools/` (the probes as run).
