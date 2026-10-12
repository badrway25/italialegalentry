# W3-A · the console shell — senior review (one pass)

Reviewer label `w3-a-review` (built nothing). V5.5 delivery mode: one review, then fix, then ship. Branch `v54-w3-a`
at `9383df1` (step 1 + step 2 and their notes). Looked at on the reviewer's own server from this worktree
(127.0.0.1:8886, `ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03`, `--noreload`), headless Chromium with its own profile,
one browser at a time, sessions minted with `Client.force_login` (no password used) and revoked at the end. No run
ended on a crash. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-a/review/` (`desk/`, `desk-states/`, `phone/`,
`release/`, `review2/`, `review3/`, each with its `report.json`).

Looked at: 13 page types of seven accounts (a person with a file, a person without one, a company in both spaces,
the administrator, an operator, a professional) × fr / ar × 1440 × 900, 1366 × 657, 390 × 844, 360 × 800 (104
captures); 30 desk states (compact, tips, the language list, the keyboard walk, forced colours, reduced motion, 1920,
1280 × 800, 1024, it / en at 1366 × 657); the phone drawer opened from the keyboard in fr and ar, a staff drawer at
360, the band at 820; the loader's release on the rail's mark.

## Verdict: **SHIP_AFTER_FIXES**

The shell is at the bar. It reads as an institutional workspace, not a dashboard kit: one night rail with a quiet
three-level hierarchy (the space under the name · the section word · glyph + word on one axis), «il lume» as the
single, unmistakable "you are here", a pinned foot that says who you are, and a page frame with one start edge and
one header. Arabic is a true mirror (rail, tips, drawer, foot, chevrons). The phone chrome is the rail laid flat and
it works: one «Menu», four entries at most, the drawer carries the whole rail and its foot.

No P0. One major item — what a staff member meets at the space's home — must be settled before the console ships;
the rest is polish.

## The gate, checked on the real pages

| Gate item | Result |
|---|---|
| Same rail keys across a space | yes — one rail per space on every page looked at; one current entry per rail copy, everywhere |
| Rail foot visible at 1366 × 657 | yes for every account, fr / ar / it / en; a person's whole rail fits without scrolling |
| Long rails (staff, 11–13 entries) at 1366 × 657 | the list scrolls by 61–198 px under a pinned foot; the current page stays in view |
| Compact mode | 64 px, the glyph column does not move; the word stands beyond the edge on hover / focus (on the correct side in ar); the choice is kept; reduced motion: 0 ms |
| Bottom bar ≤ 4 (+ «Menu») | 1–4 on every account; 3 for staff at 390 / 360 |
| Phone chrome ≤ 120 px | 114 (fr), 103 (ar), 109 on the case file with its action bar, 100 for a one-line bar, 112 in the band |
| «Menu» in three keys | Tab, Tab, Enter → «Menu» (a button by script); Enter opens the drawer with the focus on the current page; Esc closes it and the focus returns to «Menu» |
| Health | 0 horizontal overflow, 0 console errors, 0 CSP messages, one h1, on all 164 page loads |
| Animations at load from the shell | none; the only motion is the loader's release on the mark (W1-D) and the pages' own draws |
| Skip links | both visible on focus (229 × 52 and 269 × 52, above everything) |

**Where am I · what is the one thing to do · what is next — first viewport**
- *Person* (1440, 1366 × 657, 390): yes — the lit rail entry, the title with the file reference and state,
  «Votre prochaine action» with one primary button («Continuer»), the journey with «Vous êtes ici».
- *Company*: yes — «Tableau de bord» lit, the company's name as the title, «Ouvrir le besoin» as the one act, the
  next action said in a sentence.
- *Staff on their own registers* (dispatch, the professional's queue, the territorial analysis): yes — the page lit
  under «Mon rôle», the title says the task, the act sits on the row.
- *Staff at the space's home*: **no** — M1.

## Findings

### Major

**M1 — A staff member's home is a person's dashboard.** The administrator (and every role account) reaches, from
the mark and the phone top bar's tile, «ESPACE RÉSERVÉ» with «Votre prochaine action — Commencer le questionnaire»
as the primary act and «Mes documents · 3 pièces demandées» below (`desk/admin-dash-fr-1366x657.png`,
`desk-states/compact-admin-fr-1366x657.png`). The rail puts the role's registers first, but the page tells the
staff member to fill in an applicant's questionnaire: «what is the one thing to do» is answered wrong for every
staff account. *Fix (shell side, team decision):* for an account that holds a role register, `shell_space` gives the
space's url — the mark, the phone tile — to the first entry of «Mon rôle»; the person dashboard stays one key away
under «Parcours». W3-B gives staff a home of their own later; until then they do not land on a person's.

### Minor

**m1 — A scrolling rail is cut dead under the foot.** When the list scrolls (staff at 1366 × 657, open and
compact; a professional in ar) the last visible row is sliced through its glyph and word at the foot's edge, with no
cue that more follows (`desk/operator-dispatch-fr-1366x657.png`, `desk/pro-queue-ar-1366x657.png`,
`desk-states/compact-admin-fr-1366x657.png`). *Fix:* a scroll edge at the list's block end — the
`background-attachment: local` pair of night gradients (CSS only, no script, no motion), visible only while
something is under it.

**m2 — In Arabic the French name above the title is off the reading edge.** The dashboard's context line
(«Personne de test QA») hugs the left of a right-anchored box: 130 px off the title's edge at 1366, floating
mid-line at 360 (`desk/person-dash-ar-1366x657.png`, `phone/person-dash-ar-360x800.png`). The frame already solves
this for `.page-header__title` / `__lead` with `inline-size: fit-content`; extend that rule to the context header's
name line, or W3-B does it in its own sheet.

**m3 — The identity carriers disagree on the empty dashboards.** For a person without a file, a company in
«Espace réservé» and staff, the rail lights «Tableau de bord», the breadcrumb ends on «Espace réservé» and the h1
reads «ESPACE RÉSERVÉ» in capitals (a locked string, as written), while the dashboard with a file says «Tableau de
bord» in sentence case. The h1 is W3-B's template; the shell's part is the breadcrumb — on a space's first page it
could end on the page, as it does everywhere else.

**m4 — Open dependencies of the gate, not defects of this build.** The notification centre (popover / phone sheet)
and the console's account popover wait for the overlay system (W2-A); «Aller à…» for staff has no control in the
product; the labelled 80 px compact rail waits for copy (B1). Land them with W2-A / B1; do not hold this merge.

**m5 — Weight.** The console page type's CSS stands 1 445 B gzip over the Wave-1 ceiling (DL54-52). The shell adds
no image, font, request or load animation: not a real regression. The Performance Lead measures first render on 8782
at the integration checkpoint; the CD takes the one raise or names what goes.

**m6 — Polish.** The rail's control draws the same glyph open and compact (the state lives only in
`aria-expanded`); a mirrored twin for the compact state would read better at a glance. French bottom-bar labels
stand on two lines on most phones until the short labels are signed (B1) — legible and never broken inside a word,
but busier than the Arabic bar.

Checked and dropped: the band's account trigger reads «Personne ▾» — that is the QA account's first name
(`get_short_name`), not a defect.

## What not to change

The night rail and its foot, «il lume», the one-axis glyph column, the context bar as the page's level, «Menu»
once, the drawer's foot, the phone action bar on the case file. They are the screen's identity carriers and they
pass the swap test.
