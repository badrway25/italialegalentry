# W3-C · Document workspace and status — accessibility + performance check (one pass)

Label `w3-c-a11y-perf`, 12 October 2026 — the family's one accessibility/performance check (V5.5: implement → review
once → fix → ship). Built nothing, changed nothing in the family's code. Checked branch `v54-w3-c` at `b62c10b` (step 1
+ step 2, W2-A's overlay system merged in), merge base with `design-v5` `361b03d` (design-v5's head `abbabda` adds only
docs). The senior review (`REVIEW.md`, committed as `5b5f40a` while this check ran) was read after the measures; nothing
here repeats its findings except its M1, re-read on the keyboard path and counted once (finding 1).

**Lane.** Lane 9, port 8789. Accessibility on the dev server from `C:/tmp/ile_wt/v54-w3-c` (`ile_v5_l9`,
`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag). Performance on the same port: the
merge base (an export of `361b03d` in this role's scratch folder) and the worktree, each as a **compressed twin** — the
plan's 8782 shape: DEBUG off, `CompressedManifestStaticFilesStorage`, hashed URLs, gzip on the wire, `collectstatic` into
a scratch root per tree (settings outside every repository: W3-B's check's file, re-pointed at lane 9) — served in turn.
Signed-in pages through sessions minted with `Client.force_login` on `ile_v5_l9` (no password used, typed or stored),
revoked at the end. Personas of the lane clone: `qa-person` (seven pieces in seven states, the Conditions not accepted:
the rows say «Bloqué»), `qa-doc-person` (a piece to replace, two filed — W1-0's «documents» persona), `w3c-depot` (the
implementer's lane persona: two open pieces with «Déposer la pièce», three deadlines), `seed-company` (no file). **No
write to any piece**: the Dépôt's server answers were fulfilled inside the browser (Playwright's route), so no request
reached the server; the only writes on the clone are the four minted sessions (deleted at the end), the accounts'
`last_login` and one `auth.login` audit event each. Headless Playwright Chromium (the venv's), its own profile under
`C:/tmp/ile_v5_council/.profiles/w3-c-a11y-perf/`; one browser and no pytest at a time; every series waited on
`PERFORMANCE_BENCHMARK_LOCK` (never present; never created). **No run crashed.** Never 8780, 8782, 9222 or 9223.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-c/a11y-perf/` — `desk/`, `phone/` (keyboard walk, pixel contrast,
hit areas, accessibility tree, axe — one JSON + PNG per page), `drawer/`, `sheet/`, `depot/`, `reflow/`, `spacing/`,
`reduce/`, `forced/`, `look/`, `rest.json`, `swap.json`, `search_status.json`, `weigh.json`, `twin/` (the BASE / HEAD runs
and traces, `summary.json`). Probes: `C:/tmp/ile_v5_council/.work/w3-c/w3-c-a11y-perf/` (W3-B's probes adapted; W1-0's
`trace.py`, `analyse.py`, `health.js` byte-identical).

## Verdict — SHIP_AFTER_FIXES

0 blocking · 1 major · 3 minor. The major is the senior review's M1, confirmed here for a keyboard user (after a swap,
closing the drawer leaves the focus off-screen or on the wrong row) and carried with its fix; the three minors are this
check's own and small, all in W3-C's files: the register strip's runs lose most of their focus ring to the strip's clip,
«Télécharger» and the gate's link are under the plan's 44 px for a finger, and a refused file is not tied to its field.
Otherwise **no WCAG 2.2 AA failure** on the area's nine page states, fr and ar (1440, 1024, 390 touch, 320; reduced
motion, forced colours, text spacing): axe 0 on 64 runs; 872 keyboard stops named and `:focus-visible`, none hidden by a
fixed layer or by the drawer beside the list; 1 755 text runs at AA or more against the worst pixel, the status words at
7.17 : 1 or more; the drawer and the filter's sheet keep their contracts (the focus in and back, the trap where modal,
Esc, «Fermer» 44 px); the Dépôt's answers land in place and are said. **No performance regression:** the shared CSS goes
down (−1 273 B), the register's page-only sheets add 5 044 B — allowed by the owner's V5.8 ruling with a twin check —
and the twin (W1-0's protocol, n = 9 a cell, the merge base against the head, interleaved) shows LCP no worse
(−112 … +28 ms), the first-render task lower in every cell, CLS ≤ 0.0011, the drawer's cold open p90 112–120 ms
(≤ 200), nothing looping at rest; against V4, LCP 188–384 ms earlier.

## What was measured

9 page states × fr / ar (the two languages of every row below):

| Key | Account | Page | What it shows |
|---|---|---|---|
| R1 | `qa-person` | `/{lang}/espace-reserve/mes-documents/` | «Mes pièces»: seven pieces in seven states, the Conditions gate («Bloqué» on three rows, «Consulter» as the strip's act), the files table |
| R2 | `qa-doc-person` | `/documents/` | W1-0's «documents» flagship URL: a piece to replace («Remplacer la pièce»), two filed |
| R3 | `w3c-depot` | `/{lang}/espace-reserve/mes-documents/` | two open pieces with «Déposer la pièce» on the row and in the strip, dates (soon / none) |
| R4 | `seed-company` | `/{lang}/espace-reserve/mes-documents/` | the company account without a file: the register's one sentence |
| P1 | `qa-doc-person` | `/documents/requirements/70d79bd5…/` | the piece in the order of need, the Dépôt open (replace), a deposit with «Télécharger» |
| P2 | `qa-person` | `/documents/requirements/b643c62c…/` | a refused piece, the Conditions gate in place of the Dépôt |
| U1 | `qa-doc-person` | `/documents/upload/` | the loose road (file, type, description, organisation) |
| U2 | `qa-person` | `/documents/upload/` | the gate page (403 by design, IP S7) |
| D1 | `w3c-depot` | `/{lang}/espace-reserve/mes-echeances/` | the deadline register, F13 (overdue azione, soon attesa, calm) |

Passes: 1440 × 900 (fine pointer) and 390 × 844 (phone emulation, touch) — keyboard walk with the ring read on pixels,
pixel contrast, hit areas, the accessibility tree, axe-core 4.13.0 (W1-0's copy) on `wcag2a/2aa/21a/21aa/22aa` and
`best-practice`, W1-0's `health.js`; the preview drawer opened from the keyboard at 1440, 1024 (beside the list) and 390
(the sheet); the filter's sheet at 390 and 320; the Dépôt's answers at 1440 and 390; 320 × 640 reflow; WCAG 1.4.12 text
spacing at 1440 and 390; reduced motion (`emulateMedia`) and forced colours (Chromium's emulation) at 1440 and 390; a
5-second window at rest on every page, with the drawer and the sheet left open. **142 recorded page loads in the JSON
passes (+ 26 rest windows and the probes): 0 CSP reports, 0 console errors** — the gate page's own 403 status line apart,
as W1-0 counts the 410 page's.

How the probes read pixels (W3-B's, unchanged). The keyboard walk clips every stop focused, then the same clip at the
same scroll with nothing focused: the indicator is the pixels that changed (ring fill = changed pixels in a 6 px band round
the box ÷ a 2 px perimeter; change contrast = the median ratio between each changed pixel's two colours). Contrast: every
text run of `<main>` (or of the open overlay) fully in view and under no fixed layer — its computed colour, with its
opacity chain, against the pixels under it, the page re-drawn with every glyph transparent: the dominant pixel, and the
worst pixel covering ≥ 5 % of the run. Hit areas: `elementFromPoint` probed outward from each target's centre (a
stretched link's `::after` counts — the row is the target).

## Accessibility

| Check | Result |
|---|---|
| axe 2.0–2.2 A/AA | **0 violations** on 64 runs — the 36 page loads at 1440 and 390, the drawer open (12), the filter's sheet open (8), the Dépôt after each answer (8); best-practice 0. «Incomplete» only where axe cannot decide: W3-A's rail words on night, the phone bar's `aria-controls` to the closed menu, and the filter control's `aria-controls` to its closed sheet (`aria-haspopup`, the overlay system's) |
| Keyboard, fr and ar | skip links → rail (the bar on phones) → the search → the three runs → the strip's act (`aria-describedby` = the next piece) → the filter (its entries in `STATE_ORDER`, `aria-current` on the chosen one; one 44 px control in the card layout) → each row's title (the row is the link), then its act where the reader acts (`aria-describedby` = its piece) → the files table's links → the foot's links → footer. The piece: its state, the Dépôt (the field, the date, «Déposer»), «Télécharger» (described by its version), «Retour au registre». **872 stops** at 1440 and 390: every one named, every one `:focus-visible`, every ring measured on pixels |
| Focus visible | laguna-550, 2 px at 2 px — change contrast **3.94–4.11 : 1** on paper and white, **3.44** on the segmented track (Arabic, the floor), 3.74–3.84 in French; the Dépôt's zone takes its field's ring (3.94). Ring fill ≥ 0.9 of a 2 px perimeter on every stop of the area **except the register strip's three runs**, whose ring the strip's `overflow: clip` cuts — finding 2 (the probe's other low readings are artefacts: a two-line title's ring wraps both lines,
`look/R1-fr-390-0-focus.png`, and the skip links are read in the middle of their entrance) |
| Focus not obscured (2.4.11) | **0 stops** hidden or partly covered by the sticky bar (desktop) or the bottom bar (phones). **The drawer beside the list** (1440 and 1024, fr and ar): every focusable control of the register focused in turn — 19 on `qa-person`, 13 on `w3c-depot` — **0 under the drawer**, and the backward walk from the drawer's title through the register met none either |
| Contrast on pixels | **1 755 text runs, 0 below AA** — also against the worst pixel (the pages, the open drawer, the open sheet; the Dépôt after each answer: 0 of 313). **State words ≥ 7.17 : 1** on all 106 («Bloqué» is the floor; chip words, «En retard» / «Bientôt», the drawer's head): COLOUR §10's AAA rule holds. Text under 16 px between 4.5 and 7 : 1 is W1-A's tokens as designed — white on the primary 5.29 (15 px; 4.99 once on a phone while the primary's label sat at 0.96 opacity), the segmented track's words and counts 5.14 (13–14 px), laguna-700 links 5.93–6.05, text-2 6.87; none is a state word or a notice title |
| Names, roles, structure | 0 nameless controls (CDP accessibility tree); one h1 a page; the register a region named by its h2 («Pièces du dossier E46E03B461»), the runs a navigation named by the same heading, the groups h3 with their count as text; the ledger's marks `aria-hidden`; the date's word in a visually hidden «Échéance»; **2.5.3 holds on every stop of the area** (the only name that differs from its words is W3-A's rail brand, by a dash) |
| Arabic | mirrored grid, the drawer on the left (x 0), arrows and chevrons flipped; French record titles isolated (`lang="fr" dir="ltr"`, the drawer's head too), a reviewer's reason `dir="auto"` on the reading edge; **no Arabic text under 14 px** (the type system's floor) on 18 Arabic loads |
| The preview drawer | **desktop** (1440, 1024): opened from the keyboard, the focus goes to its title (`tabindex="-1"`, visible ring); non-modal — no `aria-modal`, the page usable, Tab goes on to the footer, Shift+Tab back into the register; Esc returns the focus to the row's title and the register's URL. **Phone** (390): a modal sheet by script — `aria-modal="true"`, 30 Tabs stay inside (Fermer → its links → Fermer), Esc returns to the row. «Fermer» 44 × 44 and named in both; axe 0; 0 text under AA inside (17–20 runs at 390, 14–19 at 1440 and 1024). The swap, read on the keyboard path (`swap.json`, 1440, fr and ar): Enter on the first row, the focus back in the list on the sixth row, Enter (the drawer swaps, `replaceState`, the focus stays in the list — correct), then a close: **Esc from the list** brings the register's URL back but the page jumps from scrollY 1 028 / 1 043 to 0 and the focus stays on the sixth row, now 1 060 px below the viewport; **«Fermer»** sends the focus to the first row opened, not to the piece shown — the review's M1, confirmed for a keyboard user (finding 1) |
| The filter's sheet | 390 and 320, fr and ar: Enter on «Filtrer par état» opens it with the focus on the current entry (`aria-current`), `aria-modal="true"`, labelled «Filtrer par état»; 20 presses stay inside; every entry and «Fermer» 44 px; Esc returns the focus to the control; contrast floor 5.53 |
| The Dépôt | the native input covers the zone (opacity 0), named by its label «Fichier», described by the formats; **the client guards send nothing** (0 POST seen by the route), say the reason in the assertive region and put the focus back on the field; **a past date**: `aria-invalid="true"`, the error in the field's description, said, the focus on the date; **the server's refusal** (simulated) lands on the file's row, is said, the focus back on the field; **the throttle** as a notice, said politely, «Déposer» kept. One gap: a refused file is not tied to its field — finding 4 |
| Reduced motion — a real still | **0 animations** at load, at 1 s, after hovers, after two Tabs (16 loads, 1440 and 390); every transition of the area computes to 0 s (rows, links, runs, the strip, buttons, the filter, chips, the zone); the drawer opened and closed from the keyboard: `translate: none`, no transform, `transition-duration: 0s`, no L3 seat — nothing runs at 16 ms or after 900 ms; the filter's sheet the same. With motion: 0 running animations at rest on every page |
| Forced colours | the strip keeps a 1 px CanvasText edge (no shadow), the to-act group its 3 px rule, the rows their hairlines, the chips their 1 px edge — dashed for the attesa states, so the shape still speaks; the current filter entry outlined in Highlight; the ledger's marks in the link colour; the drawer and the sheet a 1 px edge; the zone dashed; the ring in Highlight (change contrast 11.3–15.1 : 1). The runs' ring is cut the same way (finding 2) |
| Reflow 320 × 640 | 0 overflow on 18 / 18 pages; the only clipped text is W3-A's phone bar title (its ellipsis on the piece's page; the h1 carries the whole title) |
| Text spacing (1.4.12) | 0 overflow at 1440 and 390; nothing of the area clipped — the only ellipsis is W3-A's rail account name, which the spacing pushes past its box |
| Targets | fine pointer: every target ≥ 24 px or spaced. Coarse pointer (390 touch): **the row is the target** — 45 of 45 probe points on every card open the piece (the title's link stretched over the row); the filter's control and entries, «Fermer», the drawer's and the sheet's controls, the Dépôt's zone (≥ 56 px) and «Déposer» 44 px or more; the foot's links carry an invisible 44 px band — **except «Télécharger» and the gate's inline link** (finding 3) |
| Status messages (4.1.3) | the register's search says «Pièces affichées : n» in its status region once the typing pauses — «Pièces affichées : 1 / 7» («المستندات المعروضة: 1 / 7»), then «… 0 / 7» with «Aucune pièce ne correspond à cette recherche.» —, and the groups it empties are hidden with their rows (`search_status.json`, fr and ar) |
| Against W1-0's «before» set | no count rose on the area's page types (documents, documents-portal, document-upload, the gate, the requirement, deadlines): overflow 0, axe contrast failures 0, focus missing 0, CSP 0, console errors 0 |

## Performance

**Weight** (`gzip -9` of the committed bundles, the stewards' method; `weigh.json`):

| | W1-0 «before» (V4, 8782) | merge base `361b03d` | `v54-w3-c` `b62c10b` | W3-C's delta |
|---|---|---|---|---|
| `dist/main.css` (every page) | 36 294 | 42 152 | **40 876** | −1 276 |
| `dist/portal/console.css` | — | 6 809 | 6 809 | 0 |
| `dist/portal/portal.css` | — | 1 932 | 1 935 | +3 |
| **the shared console sheets** (main + console + portal; the deadlines page) | 41 668 | 50 893 | **49 620** | **−1 273** — 1 307 B under the ceiling of 50 927 B (DL54-87 item 3) |
| `dist/documents/documents.css` (page-only: the five documents pages, the showcase) | — (V4's page sheets: 6 545 with portal + console) | 1 172 | 5 418 | +4 246 |
| `dist/core/overlay-panels.css` (W2-A's page-only sheet, now linked by the two register pages) | — | — | 2 071 | +2 071 |
| **the register** («Mes pièces», `/documents/`) | 42 839 | 52 065 | **57 109** | **+5 044**, all in page-only sheets |
| the piece, the upload page, the gate page | 42 839 | 52 065 | 55 038 | +2 973, page-only |
| JS before `load` (`/documents/` on the twin, on the wire) | 36 706 · 8 requests | 46 620 · 9 | 49 121 · 10 | +2 501: `console.js` +142, `piece-drawer.js` 2 358 (imported where the register draws the drawer) |
| JS after `load`, on demand | — | — | the Dépôt's chunk 3 577 (+ `depot.js` 100), W2-A's overlay extras 1 600 | new, the register and the piece only |

§2.6 and the owner's V5.8, read on this: the shared bundles ratchet down (−1 273 B, `main.css` under its 45 KB cap);
everything the family added is page-only — the register, the piece, the Dépôt and the drawer's own rules in the documents
sheet, the panels' anatomy in W2-A's sheet as its CONTRACT §1 requires — and the definitive ruling (12 Oct, 02:15) allows
a page type's total to grow that way, for what the surface draws, «only with a performance sanity check (no meaningful
LCP / first-render regression on the lane twin)». **That check passes** (below). Each module is under the 4 KB of §2.6's
module row. For the steward: the register page type records **57 109 B** and the piece/upload/gate type **55 038 B** at
this merge (their first page-type totals with these sheets), and they ratchet down from there; the review's m7 (the
ledger marks drawn twice) is a deletion from the documents sheet when the family consolidates.

**On the wire** (the twin, `/documents/`, before `load`): CSS 5 requests / 57 166 B (BASE 4 / 52 128), JS 10 / 49 121 B
(BASE 9 / 46 620) — `piece-drawer.js` starts just before `load`, the Dépôt's chunk and W2-A's overlay extras after it
(JS in all 12 / 54 298 B); fonts 3 / 23 644 B in French, 55 872 B in Arabic (unchanged; the caps 32 KB and 56 KB hold).
CSS + JS requests before `load`: **15**, BASE 13, V4 12 — §2.6's request row was already one over at the merge base; W3-C
adds the panels' sheet and the drawer's module. No time is lost to it (the twin below: `load` itself fires 25–77 ms
earlier than at BASE), so it is recorded here for the steward, not raised as a finding.

**Before / after on the lane twin** — W1-0's `trace.py`, byte-identical (profile A: 150 ms RTT, 1.6 / 0.75 Mbps, CPU ×4,
cache off, a fresh profile per load, the h1 click + Tab after the rest), W1-0's «documents» cells (`/documents/`,
`qa-doc-person`), the merge base and the head served in turn in blocks BASE · HEAD · HEAD · BASE, one discarded warm-up
per cell after each server start; **n = 9 a cell and tree**, 72 traced loads, 0 failed, 0 trace loss; medians [range]:

| Cell | LCP BASE → HEAD (ms) | first-render task | longest task | tasks > 50 ms | TBT | CLS max BASE / HEAD | LCP element BASE → HEAD |
|---|---|---|---|---|---|---|---|
| fr 1440 | 1 260 [1 224–1 308] → **1 168** [1 124–1 328] | 42.7 → **35.3** | 101 → 108 | 4 → 3 | 77 → 42 | 0.0013 / 0.0010 | `p.doc-page__lead` → `p.ws-head__lead` |
| fr 412 | 1 232 [1 128–1 396] → **1 216** [1 116–1 296] | 40.0 → **29.1** | 143 → 109 | 4 → 5 | 156 → 111 | 0 / 0 | `p.doc-page__lead` → `h2.ws-case__title` |
| ar 1440 | 1 460 [1 320–1 588] → **1 348** [1 332–1 488] | 50.4 → **40.9** | 145 → 125 | 5 → 3 | 121 → 90 | 0.0045 / 0.0011 | `p.doc-page__lead` → `p.ws-head__lead` |
| ar 412 | 1 456 [1 320–1 576] → **1 484** [1 400–1 552] | 46.2 → **36.3** | 151 → 132 | 5 → 4 | 208 → 127 | 0 / 0 | `p.doc-page__lead` → the next piece's title (`span`, text) |

LCP −112 … +28 ms (PFR's resolution for «no worse» is +50 ms); the first-render task lower in all four cells (−7 … −11 ms;
the resolution is +30); the longest task lower in three, +7 ms in one; TBT lower in all four; the heaviest load task of the
72 is BASE's (218 ms; HEAD's 182). No long task class is new: both trees show the same ones — the parse (≈ 230 ms), the
style and layout as the sheets and the fonts land (≈ 1.0–1.3 s), the shell's scripts. The LCP element stays a text block
of the first render (the page head's lead, the register's heading or the next piece's title), never an image or a late
fragment. Machine: busy 24–31 % before a load, 33–40 % during (other lanes' tests); the blocks interleave, so the noise
falls on both trees.

**Against the W1-0 «before» set** (V4 on 8782, the same protocol and cells; medians): LCP **1 168 / 1 216 / 1 348 /
1 484 ms** against V4's 1 552 / 1 564 / 1 692 / 1 672 (fr 1440, fr 412, ar 1440, ar 412) — **188–384 ms earlier**, under
2.5 s everywhere; the first-render task 29–41 ms where V4's was 324–435; the longest task 108–132 ms where V4's was
324–435; tasks over 50 ms 3–5 (V4 3–5); CLS ≤ 0.0011 on 36 loads (V4 up to 0.0142). The flagship's CLS budget (≤ 0.05)
holds with a wide margin.

**The preview drawer's cold open** (plan §1.14's INP rule: the heaviest page — «Mes pièces» of `qa-person`, seven pieces,
in Arabic first —, n = 9, CPU ×4, p90 ≤ 200 ms): the head twin, the same protocol, the first row's title clicked (a tap on
the phone) 5 s after a cold load; the Event Timing duration of the press (input delay + handlers + the next paint):

| Cell | n | p50 (ms) | p90 (ms) | max |
|---|---|---|---|---|
| ar 1440 (beside the list) | 9 | 96 | **112** | 112 |
| ar 412 (the sheet, a tap) | 9 | 104 | **120** | 128 |
| fr 1440 (beside the list) | 9 | 96 | **112** | 144 |
| fr 412 (the sheet, a tap) | 9 | 96 | **112** | 120 |

**p90 112–120 ms**, under the 200 ms of O7 in every cell — the head is written into its slots at 0 ms and the
register's re-layout waits for the drawer's first frame (DL54-103), so the press pays neither. After the press the
longest main-thread task is 78–177 ms (median 111: the piece's fragment seated, the register laid out beside the drawer) —
after the press's own paint, so the press does not wait for it; the merge base answered the same press with a page load
(LCP ≈ 1.2–1.5 s on this profile). CLS over the whole load and the open: ≤ 0.0005 — the workspace makes room under the
person's own act (within 500 ms of the input), and nothing shifts when the fragment lands. The same loads give «Mes
pièces» itself (no W1-0 trace exists for this page type): LCP 1 236–1 432 ms (medians), the first-render task 32–38 ms,
the longest load task 99–155 ms.

**At rest** (`rest.json`, the lane, 5 pages × fr / ar × 1440 / 390, a 5 s window 3 s after load, and again with the drawer
open — beside the list and as a sheet — and with the filter's sheet open): 0 `requestAnimationFrame`, 0 timers, 0 style
recalculations, 0 layouts, ≤ 11 ms of task time, 0 running animations in all 26 windows — **nothing loops**.

## Findings

**1 · major · W3-C (the senior review's M1, confirmed for a keyboard user — one finding, counted once) — After a swap,
closing the drawer loses the keyboard's place.** At 1440, fr and ar (`swap.json`): Enter on the first row opens the
drawer; the focus back in the list on the sixth row and Enter swap it (correct: `replaceState`, the focus stays in the
list). Then **Esc from the list** returns the register's URL but the page jumps from scrollY 1 028 (1 043 in Arabic) to
0 while the focus stays on the sixth row — 1 060 px below the viewport, so nothing on screen shows where the focus is
(WCAG 2.4.7 in practice, 2.4.3); **«Fermer»** sends the focus to the first row opened, not to the piece shown (2.4.3).
*Fix:* the review's M1 — on `overlay:close` focus the current opener (the shown piece's row) and bring it into view
after the history's restoration (or hold `history.scrollRestoration = "manual"` while the drawer owns its entry), with a
keyboard browser test: swap → Esc / «Fermer» → the focus on the shown piece's row, inside the viewport.

**2 · minor · W3-C — The register strip's runs lose most of their focus ring.** `.reg` clips its children
(`apps/portal/static/portal/v5/_workspace.css` §3, `overflow: clip`) and the three runs sit flush with its edges, so the
system's ring — 2 px at a 2 px offset (plan §1.6) — falls outside the clip box: on «À faire» only the inline-end edge is
drawn (ring fill 0.27–0.29 of a 2 px perimeter at 1440, fr and ar), on the two other runs the inline edges only
(0.53–0.68); 0.53–0.83 at 390; the same cut in forced colours (`look/R1-fr-1440-0-focus.png`, `-1-focus.png`;
`desk/R1-*.json`, `R2-*`, `R3-*`). The indicator stays visible (change contrast 4.11 : 1; 15.1 in forced colours), so
WCAG 2.4.7 holds; the system's focus rule does not, on the register's first three stops after the search. *Fix:* draw
the run's ring inside the strip — `a.reg-run:focus-visible { outline-offset: -4px; }` (the rail's inset ring is the
precedent) — and let the documents browser test read a run's ring as it reads the rows'.

**3 · minor · W3-C — Two targets under the plan's 44 px for a finger.** At 390 × 844 (touch): «Télécharger» in the
piece's deposits (the piece's page and the drawer's body) has a 77 × 20 px hit area in French and **30 × 22 px** in
Arabic («تنزيل»); the gate's «Lire les Conditions d’utilisation» (the gated piece, the gate page, a gated piece's drawer)
is 25 px tall in Arabic and wraps inline in French (`phone/P1-*.json`, `P2-*`, `U2-*`). WCAG 2.5.8 holds (spacing; the
gate's link is inline in its sentence); SP-8 («44 px … every target under a coarse pointer») does not — and the foot's
links already carry the band (`_workspace.css` §7, `.doc-aside a::before`). *Fix:* the same invisible 44 px band on
`.doc-version__get a` under `(pointer: coarse)` (`position: relative`; a `::before` with `inset-block: calc(50% -
var(--hit-primary) / 2)`), in `_depot.css`'s coarse block; the gate's link may take it too, or keep the inline exception.

**4 · minor · W3-C — A refused file is not tied to its field.** After a client guard's refusal (format, size, empty) or
the server's refusal of the file, `static/js/src/depot.js` `refuse()` writes the sentence on the file's row and says it
once in the assertive region, and the focus returns to the field — but the field keeps `aria-describedby` = the formats
only and gets no `aria-invalid` (`depot/*.json`: `guard_type.field.file`, `server_refused.field.file`), while the date's
error does both (`fieldError()`: `aria-invalid="true"` and the error in its description, W1-C's grammar). A screen-reader
user who leaves the field and comes back hears «Fichier, PDF, JPEG ou PNG — 10 Mo maximum» and no reason. WCAG 3.3.1 is
met by the visible sentence and the announcement; the field is simply not marked in error as every other field is.
*Fix:* in `refuse()`, `aria-invalid="true"` on the input and the refusal's id added to its description (give
`[data-depot-refusal]` an id in `templates/documents/partials/depot.html`, e.g. `{{ field.auto_id }}_refusal`); both
undone in `clear()` and on a new choice; a line in the Dépôt's browser test.

Said, not findings: the assertive region keeps the last refusal's words after a later answer (visually hidden, never
re-read by itself); the gate page answers 403 by design (its console line is that status); the drawer's title shows a
ring when it receives the focus (a heading, the panel's point of orientation, as W2-A's contract asks).

## Not W3-C's (seen on the area's pages, owned elsewhere)

- **W3-A (the shell):** the skip links' ring is read mid-entrance (their 120 ms slide starts above the viewport); the
  rail's and the bottom bar's current item show no change on focus in forced colours (their inset Highlight outline is
  already there — the W1-0 set found the same); the phone bar's title and the rail's account name are the only clipped
  text of the reflow and text-spacing passes (the page's h1 carries the whole title); axe's incompletes on the rail's
  night words and on `#console-menu`'s `aria-controls`.
- **W2-A (the overlay system):** axe leaves the filter control's `aria-controls` to its closed sheet «incomplete» with
  `aria-haspopup` (not a violation); the swap's focus has a system half (the review's M1 carry-over).

## For the merge step

- Accessibility: finding 1 is the review's M1 (one fix for both); findings 2–4 are small and in W3-C's own files
  (`_workspace.css`, `_depot.css`, `depot.js`, `depot.html`). With the review's majors fixed, the family's browser tests
  are the re-check — no second pass needed.
- Performance: no regression to fix. Record the register page type at **57 109 B** and the piece/upload/gate type at
  **55 038 B** (page-only sheets included; the shared console sheets **49 620 B**, the ceiling's new low point), and the
  register's CSS + JS requests before `load` at 15 (V4 12, the merge base 13) — the panels' sheet and the drawer's module;
  importing `piece-drawer.js` after `load` (or on the first press) would take one back without changing what the person
  meets, if the steward wants the row met.
- The twin's settings, the BASE export and both static roots stay in this role's scratch folder (outside every
  repository); the minted sessions were revoked and the lane's dev server stopped at the end.

## Limits (honest)

Chromium only (Playwright's headless build); phones emulated (touch + a coarse pointer), no real device, no Safari or
Firefox: the WebKit / Firefox smoke of the overlay system (O10) has not run anywhere yet (no binaries on this machine,
W2-A's notes) — the drawer and the sheet go to Wave 4's cross-engine pass with it. No screen reader was run by a person: names, descriptions, live regions and the focus were read
from the DOM and the accessibility tree. The twin is the lane's (HTTP/1.1 runserver, `ile_v5_l9`), not 8782; its
comparison with W1-0's V4 figures shares the protocol, the data shape and the reference date, not the machine's load
(other lanes' tests ran throughout — the blocks interleave so that the noise falls on both trees). The Dépôt's server
answers were simulated in the browser (the server's own sentences were tested by the family's suites); no deposit was
written.
