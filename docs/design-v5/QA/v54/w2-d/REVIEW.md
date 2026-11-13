# W2-D — the final hero in the real home, and the home around it · senior review (one pass, V5.5)

Italy Legal Entry™ · design V5 · V5.4 plan §1.17, §3.4 items 4 and 6 · DL54-05, 07, 10, 11, 39, 40, 41 · V5.5 delivery mode ·
label **w2-d-review** · 9 October 2026, 20:10–21:55 · branch `v54-w2-d`, the code at `a649654` (the two commits after it are the
accessibility + performance report, no code), worktree `C:/tmp/ile_wt/v54-w2-d`, on my own server **127.0.0.1:8885**
(`ile_v5_l5`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`). I built nothing and wrote nothing but this
file. One pass, design + UX + taste together, against the owner's bar («credible alongside excellent international digital
products») and the settled direction. Accessibility and performance have their own check (`A11Y_PERF.md`): not repeated.

## Verdict — SHIP_AFTER_FIXES

No P0: no broken page, no wrong direction, nothing unusable, no data or security problem (0 console message, 0 CSP
violation, 0 failed request, 0 layout shift in every recording; the 20 links of `main` answer 200 in fr and ar).

The hero is the best screen the product has. At laptop widths and on phones it is the owner's brief built for real: one
path from MAROC to the door, four entrances readable at rest, black-and-white that takes colour with the light, steps that
are plainly coloured, a key that turns and a door that stays ajar — premium, and neither editorial, SaaS nor generic.
Four things are below the bar and are fixed before it ships: on wide screens the hero leaves the page's column (M1); on a
phone a scroll that starts on a tile fires its press and its light (M2); with gate G3 closed the phone hero has an empty
band and loses its entrances to the fold (M3); on a phone the movement can be seen again only through a control nothing
points to (M4). None needs a new direction: M1 and M3 are sheet work, M2 and M4 a few lines each.

## What I looked at

- **The real pages, fr and ar, 1440 × 900 · 1366 × 768 · 390 × 844 · 360 × 800** (it and en at 1440 and 390, it at 360): the
  settled hero at all eight; the first movement of a fresh session recorded in real time at six of them (CDP screencast,
  the hero's class changes on the page's clock: fr at the four, ar at 1440 and 390), with every screen of the page as a
  visitor scrolls it; at 1440, fr and ar, the hand on each origin, the keyboard from the top of the document, the replay;
  in fr a press during the replay, the navigation's panel over the hero, reduced motion, no script.
- **Phones under a finger** (touch synthesised through CDP in headless Chromium — not a real phone): a finger held on a
  tile, a real tap while the next page takes 0.9 s to answer, a flick that starts on a tile, a tap on the key, back.
- **Other windows**: 35 sizes from 320 × 568 to 1920 × 1200 (`sweep-fr.json`), the windows a laptop really leaves a page
  (1366 × 640, 1440 × 760, 1536 × 730, 1920 × 940, 1280 × 600, 1093 × 614), 2560 × 1440, an iPad lying down as a touch screen.
- **The interim page** (gate G3 closed): the same worktree served with `phase3_public` read as closed **in my server's
  process only** — no write to the lane's database — fr and ar at 1440, 390 and 360, fr at 1366 and seven more sizes.
- The owner's references: E2 at 1440 and 1920, E3 at 390 (`proof/research/hero/he/concepts/`), `HERO_FINAL_BRIEF.md`; the
  family's notes and DL54-39 … 41 — read after looking, to tell a decision from a defect.
- Evidence: `C:/tmp/ile_v5_council/evidence/v54/w2-d/review-1/` (Phase 3), `review-2x/` (details at DPR 2),
  `review-interim/`; the rigs in `C:/tmp/ile_v5_council/.work/w2-d/w2-d-review/`. One browser at a time, own profiles
  (removed), every series behind the benchmark lock (never present); never 8780, 9222, 9223. No run crashed.

## The owner's hero brief, item by item (the real home, under «Il portico»)

| # | The brief | Verdict | What the page does |
|---|---|---|---|
| 1 | E2's narrative and flow, desktop | **Met** at 1280–1536; the composition slips above ≈ 1600 px (M1) | Statement → one path: MAROC, four live stations, across the reveal, gold in the night, the door → four origins hung by one stem each. The first movement is 3.56 s, once a session, ≈ 0.45 s after the door has painted: the four named in colour → their stems → the light MAROC → door → arch → steps → key → the door ajar → settle. 4 / 4 origins whole in the first screen from 1280 × 720 to 1920 × 1200 and in real windows (1366 × 640, 1440 × 760, 1536 × 730, 1920 × 940) |
| 2 | E3's composition, mobile | **Met** (Phase 3); not with the gate closed (M3) | Statement → night band (six-station rail beside the whole door) → 2 × 2 tiles on one spine: 4 / 4 tiles in the first screen at 360 × 640, 360 × 800, 375 × 667, 375 × 812, 390 × 664, 390 × 844, 412 × 915, 430 × 932. The door gives way first on short screens, as briefed |
| 3 | E2's repeatable light flow, mobile | **Partly met** (M2, M4) | A press on a tile lights its route — spine, floor line, steps, the chip in colour — every time: under a held finger the light travels to the door (≈ 0.7 s); on a tap it is a lit state of ≈ 0.3 s before the page changes. A tap on the key replays the whole movement (2.75 s) — and nothing on a touch screen says so. The same press also fires when the finger only starts a scroll |
| 4 | Morocco → Italy | **Met** | Desktop: MAROC (the one filled node) → the door, «ENTRÉE EN ITALIE» inscribed under its steps; the light only ever runs that way. Phone: clearer still, the rail reads MAROC … ENTRÉE EN ITALIE beside the door. Arabic: right to left, المغرب first. The origin is the quietest thing on the line (m5) |
| 5 | Black-and-white → colour | **Met as decided** (DL54-12) | Black-and-white at full range at rest — crisp, never dimmed; colour under the hand in 200 ms, at once under focus and press, and once in the first movement. **To say to the owner in words:** when the movement settles the four go back to black-and-white and only the door stays lit; if «→ colour» is expected to stay, it is one keyframe (the colour's release), a forward correction |
| 6 | Cleaner route lines, fewer dashes | **Met** | 0 dashed or dotted stroke, 0 dash array, 0 repeating gradient among the hero's computed styles (1440, 390). The desktop draws one 3 px path and four stems; the phone one rail and one spine |
| 7 | Coloured, reactive lower steps | **Met** | At rest three laguna treads with the door's warm spill — plainly coloured; gold bottom → top in the movement; lit again under hand, focus and touch, with the door's band at full |
| 8 | The rotating key and the unlock | **Met** | The key turns once about its shaft (0.8 s; edge-on twice, a glint on the bow as its face returns) over a warm halo, then a band of light opens at the leaf's edge and falls on the steps; the door rests ajar. It reads as an unlock without a trick. Reduced motion: the ajar still from the first paint; no script: the stage closed, as drawn |
| 9 | Four entrances legible at rest | **Met** | Desktop: photograph, word 17 / 600 with its arrow, sentence 15 / 22 (14 / 20 at 1366) in 3–5 lines. Phone: chip, word 16 px, arrow; the sentences one swipe lower, in the register. One ragged row at 1440 × 900 (m2) |
| 10 | Premium — not editorial, not SaaS, not generic | **Met** at laptop widths and on phones; **not above ≈ 1600 px** (M1) | A grotesque promise, a bronze inlay, a night niche, the owner's door: no card idiom, no serif sentence, no gradient decoration. Beside E2 at 1440 the product is the cleaner page (no ticks, no collector, no arrow chips) |

For the record, by my eye: the desktop hero at 1366–1536 and the Phase 3 phone hero 4 / 5 and above on visual quality,
premium, originality and UX; the desktop hero at 1920 3.5 until M1; the interim phone hero 3; the page under the hero
coherence 4, premium 3.5.

## The home around the hero

- **One object, repeated**: a band on its ground, a head on the reading edge (the steps' mark, title 28 / 600, lead), a body
  from the fifth column; hairlines, one plate («il gradino»), two night grounds, one brand band. Five sizes of type; a title
  is never smaller than what it titles; on phones nothing a person reads is under 16 px. 6.06 screens at 1440 × 900, 7.01 at
  1366 × 768, 10.3 at 390 × 844, 11.2 at 360 × 800. The Arabic page mirrors; the door, the key and the marks do not.
- **Hand and keyboard**: a pathway's row, the forward links, the two buttons and the night links all answer, with the right
  ring on each ground; the heads stay in sight while their body scrolls from 75 rem.
- **Judgement**: coherent with the hero and with itself, sober, well set — and typographic only. After the richest screen of
  the product come five screens of type on one layout, with no picture and no figure (the family says so, DL54-41 item 11).
  It does not block shipping; it is why the lower page is 3.5 and not 4, and the first thing the imagery pass should change.

## Findings

**Blocking — none.**

| # | Severity | Finding (seen and measured) | Fix |
|---|---|---|---|
| M1 | major | **On wide screens the hero leaves the page's column.** The hero's text starts 32 px from the window at every width up to 1920 (422 at 2560); the chrome, the navigation's panels and every chapter stand on the container: 135 px at 1366, 100 at 1440, 148 at 1536, 160 at 1680, **280 at 1920**, 600 at 2560. At 1920 × 1080 the promise starts 248 px left of the logo above it and of the chapter under it; the description at the hero's foot (x = 32) and the first chapter's head (x = 280) stand in one screen; the plates (240 px) are narrower than their columns (277 px) and the sentences run past them; an open panel leaves cut pieces of the promise at its side (1440: «Le», «de», «Décou»). The niche ends on a grey shadow above the description, where E2 — the owner's reference — stood it on the hero's bottom edge and started the wall on the logo's edge (x = 300 at 1920). At 1280–1440 the wall needs the page (DL54-40 item 5: 196 px columns, 4 · 5 · 5 · 3 lines): accepted there | `hero.css`, the ≥ 80 rem block: from the width where four columns of ≥ 190 px fit between the container's inner edge and the niche (≈ 96 rem: 193 px at 1536, 195 at 1680, 221 at 1920 — today's 1440 line counts or better) `--pad-start` is that edge (`--container`, `--grid-margin`), not `--page-pad`; the niche keeps the far edge of the window. Plates as wide as their columns, or the text capped to the plate. The hinge at every desktop width: the description on the page's column — DL54-39 item 1's own forward correction (chapter 01's statement, `test_home.py` retargeted), the niche then standing on the hero's bottom edge as in E2 |
| M2 | major | **On a phone, a scroll that starts on a tile fires the tile's press and the light.** `hero.js` sets `is-pressed` and calls `flow()` in `pointerdown`: in a flick starting on a tile the page's own clock reads `pointerdown` → `is-pressed`, `is-flowing` (+ 5 … 17 ms) → `pointercancel` (+ 53 ms when the finger moves at once, + 80 ms after a 40 ms rest); the recording shows the pressed ground, the chip in colour and a bead on the spine for four to seven frames, then the fade (`review-1/fr-390x844-scrollflash-40ms.png`). The four tiles are the bottom fifth of the first screen — where a thumb starts the scroll. The browser's own delay of `:active` under a finger exists to prevent exactly this | `hero.js`, the origins' `pointerdown`, for `touch` and `pen` only: arm the press and the flow ≈ 80–100 ms after the finger lands, or at `pointerup`; disarm on `pointercancel`. The mouse and the keyboard as they are. A11Y_PERF's F3 (the handler's cost) is met by the same change |
| M3 | major — the interim page (gate G3 closed, «what the site shows today» by the family's notes; the lane and the hub have it open) | **With the gate closed the phone hero is not at the bar.** No station may be drawn, and the band keeps the rail: the left half of the night is empty but for an L-shaped gold line (`review-interim/fr-390x844-settled.png`). The statement is ≈ 90 px taller (eyebrow, title, lead), so the tiles leave the first screen on the windows a phone really has: 2 / 4 at 360 × 800 and 390 × 664, **0 / 4 at 360 × 640** (Phase 3: 4 / 4 at all three). Eyebrow, lead and description say one thing three times. The interim desktop holds (4 / 4 at 1024 × 768 … 1920 × 1080), with its lead at 15 px under a 52 px title | `hero.css`, `[data-hero-variant="interim"]` under 64 rem: no rail where there is no station — the door centred in the band on the spine's axis, the floor line and the spine kept; the band sized by the height as the Phase 3 short-height rule does, and the lead not drawn on phones (the description says it one swipe lower), until 4 / 4 tiles stand in the first screen at 360 × 640, 390 × 664 and 360 × 800. Desktop: the lead at the reading size |
| M4 | major | **On a phone the movement can be seen again only through a control nothing points to.** The replay is a transparent, empty 44 × 71 px button over the key: on a touch screen it has no sign at rest (the halo is the fine pointer's, the ring the keyboard's; no glyph, no tap highlight). A tap on a tile gives ≈ 0.3 s of lit route before the page changes; the travelling light needs a finger held 0.7 s — a hold a phone's own link menu is likely to interrupt (not tried on a real phone). The owner asked for a *repeatable* flow on mobile by name | Under `(hover: none)`: the key's halo — the hero's own layer, the sign a mouse gets on hover — softly lit at rest, so the key reads as the one live object; and the hand's short flow (≈ 1 s, no key turn) run once each time the hero comes back into view after having left it. Never under reduced motion; the full replay stays on the key |
| m1 | minor | **A stray glint beside the inscription on the desktop.** In every flow (first movement, replay, hand, focus) the door station's light — an 18 px gold glow — appears at the start of the label's box, ≈ 90 px left of «ENTRÉE EN ITALIE», under the lowest step, on nothing (1440 × 900: x ≈ 1004, y ≈ 821; `review-1/crop-hover1-800-steps.png`). On phones it sits on the rail's last node, as meant | `hero.css`, ≥ 64 rem: no `.he-station__lit` on the door's station, or seat it centred behind the inscription |
| m2 | minor | **At 1440 × 900 and 1280 the fourth word takes two lines** («Universités &» / «Formation →», a fraction of a pixel too long for its 196 px column) and its sentence starts 24 px under the other three; the row is level at 1366 and from 1536 | Let the glued arrow hang in the gutter (the word alone fits), so the four sentences share a line at every desktop width |
| m3 | minor | **Arabic page: the arrow of a French run points back into it.** «DÉCOUVREZ VOTRE PARCOURS ←» in the hero's call and in the phone register, «← Travail salarié» in the pathway rows: the glyph is flipped by the page's direction inside a run that reads left to right (`review-1/crop-ar-1440-call.png`) | An arrow inside a `dir="ltr"` run of an RTL page keeps its own direction (`[dir="rtl"] [dir="ltr"] .icon--flip-rtl`), or stands on the run's far side |
| m4 | minor — before go-live | **The home announces an empty chapter**: «Actualités — Aucune actualité publiée pour le moment.» (0 articles in the lane's database, as in `ile_v5` and `ile`). Right as an empty state on the news page; on the home it is a chapter about nothing | Do not draw the news chapter on the home while it has no article (the icon family's browser test then reads the disc on the news page), or publish the first article before the home ships |
| m5 | minor (taste) | **The origin is under-marked.** MAROC is set exactly as the four intermediate stations (13 px, 600) while the destination has gold, 700 and the door | Give MAROC the weight of a terminus (700, or the path's bronze) — no new element |
| m6 | minor — the imagery pass, not this family | **No picture and no figure under the hero** (DL54-41 item 11), on five screens of type | When O54 / O55 allow: one frame for the pilot's night band and one for orientation; the chapters are built to take them |

Also seen by the accessibility check, and I agree as UX: its **F5** (on a desktop the eight pathway rows do not look like
links at rest — rest their arrow at .6) and **F8** (a touch screen in the desktop layout never shows the four calls, and
their row stays reserved and empty — show them under `hover: none`).

Seen and accepted: at 1280 × 600 (a 1080p laptop at 150 %) one sentence loses its last line to the fold; at 1093 × 614 (the
compact layout in a short window) the fourth row stands under it. From 1536 the plates are narrower than their columns
(192 in 222, 208 in 227, 240 in 277): the derivatives are the imagery pass's, the alignment is M1's.

## What is right, and should not move in the fix pass

The door stage as the owner drew it, and its ajar rest; the key's turn and its pace; colour that follows light; the one path
and its four stems; the light's body under the hand; the replay on the key and its guards (a second press lands the still;
after a fast sweep of the hand or an interrupted replay the hero is pixel-identical to its rest); the phone band with its
rail; the chapters' one object, their grounds and their type; the Arabic mirroring with the door, the key and the marks
unmirrored; reduced motion as a real still; the page without script.

## Limits

Chromium only (no WebKit or Firefox here); no real phone — touch was synthesised, and the first-screen counts are emulated
viewports (360 × 640 and 390 × 664 stand for a phone with its bars); no screen reader; no performance measure (the check's
own). The lane's data: 0 news articles, 2 partners. Tests: only the two bundle-currency modules (8 passed) — the lane's
test database was left to the check running beside me. The hub on 8780 untouched; my server stopped at the end.
