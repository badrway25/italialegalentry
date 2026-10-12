# W2-D shipped — 10 October 2026

**The final hero in the real home page — E2's flow on the desktop, E3's composition on phones, a light that can be
sent again — and the home made coherent around it.** Tag **`v54/w2-d`** (design-v5 `d6ce32d`); the owner's preview on
http://127.0.0.1:8780 serves it (v5-live checked out at the tag, 8780 restarted at 01:46 and verified). Steward's
merge, label `w2-d-merge`, under `DESIGN_V5_MERGE_LOCK` from 00:57 to 01:51. Reviewed once and fixed (V5.5):
`REVIEW.md` and `A11Y_PERF.md` are both SHIP_AFTER_FIXES with no P0; the four majors and every minor that is this
area's were closed in the fix pass (`NOTES.md` §9), which no reviewer has read again.

## What shipped

- **The hero, in the real templates, on real data and the live locked copy** (`templates/pages/home/_hero.html`,
  `apps/pages/static/pages/css/hero.css`, `static/js/src/hero.js`; `/fr/`, `/ar/`, `/it/`, `/en/`).
  - **Desktop — E2's flow.** The statement, then one path: a bronze inlay on the light wall from MAROC through the
    stations of the pilot sequence, across the stone reveal, gold in the night niche, to the owner's door, with the
    last station inscribed at its threshold. The four entrances hang from the path, each with its photograph, its
    word and its sentence readable at rest. From 1536 px the wall stands on the page's column — the logo's edge.
  - **Phones — E3's composition.** The statement, the night band with the whole door beside the rail of stations,
    the four tiles on one spine: four of four tiles in the first screen from 360 × 640 up; the four sentences one
    swipe lower, in the register.
  - **The first movement**, once per session (about 3.55 s on the desktop, 2.75 s on a phone): the four named in
    colour, the light from MAROC to the door, the arch, the steps, the golden key turning once, the door opening as
    light and staying ajar. Nothing loops; at rest nothing moves.
  - **The owner's door stage is as drawn** — arch, photograph, golden key, three steps — never replaced and never
    mirrored: the Arabic page mirrors everything but the door, the key and the marks. The steps are plainly coloured;
    no dashed line is left.
  - **Black and white → colour, here only**: the four photographs rest in black and white and take colour with the
    light, under the hand, the keyboard and a finger.
  - **The repeatable flow.** Under a mouse the light runs from the shore to the door each time the hand comes on an
    entrance (about 1.3 s); a focused entrance shows its state at once and sends the same light; under a finger a tap
    shows its press and sends its light, and a scroll that starts on a tile shows nothing (the press waits 100 ms, or
    the lift); on a screen that does not hover the light also runs once each time the hero comes back into view, and
    the key's halo rests softly lit. A real button over the golden key — «Rejouer l’animation de la porte», named in
    the four languages — replays the whole sequence with Enter, Space, a click or a tap.
  - **Reduced motion is a still**: the settled hero with the door ajar from the first paint, no replay button, no
    animation. Without script the page is whole and the door closed, as drawn. Under forced colours nothing lights.
  - **With gate G3 closed** (the interim variant) the hero draws the path, the four and the door without a station;
    on phones the door stands on the spine's axis and the four tiles stay in the first screen.
- **The home around the hero** — the chapters plan §3.4 item 6 gave W2-E, built here under V5.5. Every chapter is one
  object on the V5 tokens: a band on its ground, a head at the reading edge (the mark's three steps, the title, the
  lead), a body. No running head and no ordinal. The Morocco → Italy model is said once, by the hero's path: the
  pilot chapter is a statement with one link, the jurisdiction bar is off the home, the route between two shores is
  gone. A prescribed sentence the hero shows is not printed again under it. The register of the four entrances has no
  index and no glyph, and is not drawn where the hero already carries the four sentences. «Il gradino» carries the
  anti-fraud warning; the reserved area is a row on the night with the mark's key. The news chapter is drawn once an
  article is live, in either gate state. French spacing (no-break spaces beside high punctuation) for team-authored
  strings only — a prescribed text is handed back byte for byte.
- **What left**: `static/css/v2/routes.css` and `static/css/v2/voyage.css` (deleted, with their imports), the hero's
  rules of `static/css/v4/hero.css` (23.3 → 4.4 KB: what remains draws the entrance page's door), the home's separate
  script `apps/pages/static/pages/js/home.js` (one request fewer), two unused partials.
- **Measured by the area's one accessibility + performance check** (`A11Y_PERF.md`; the lane's compressed twin, profile
  A, CPU × 4, n = 9 per cell, against the W1-0 before set): 0 axe violations and no WCAG 2.2 AA failure found on the
  home, fr and ar; LCP 1 600–1 728 ms for 2 064–2 356 ms; the longest load task 124–154 ms for 710–938 ms;
  CLS ≤ 0.038; 0 animations and 0 `will-change` at rest. These are the check's figures on the state it read
  (`a649654`), before the fix pass; they were not measured again at the merge.

## The merge

- The branch already stood on design-v5's head (`8246a7f`): `git merge design-v5` had nothing to bring, no conflict.
- **Ownership.** `scripts/check_ownership.py w2-d design-v5` listed 30 paths outside the slice. Each was read in the
  diff, found to be what the notes declare, and written under w2-d in `OWNERSHIP_V54.json` (`25c981a`), as a slice
  wherever another family holds the file; two existing slices say what was written. After it: 25 inside, 122 slice,
  16 generated — PASS. Nothing was reverted.
- **Bundles.** Rebuilt from a clean `static/js/dist` on the branch: byte for byte the committed ones. On design-v5
  after the merge the three shared chunks take that worktree's names (`098cd29`); compared file by file, the code is
  the branch's but for those names.
- **The capture report** was regenerated on the new home (`343236a`; lane 5, one headless Chromium, the run complete):
  the same 43 captures, none failing a condition, **969 icons laid out** for 842, 0 empty; 16 captures differ, all
  the home's and only in that count. DS 2026 §13 follows, by `scripts/regen_design_inventory.py`, which answers
  «current» on design-v5 after the merge and the rebuild.
- **DL54-44** (`1a21feb`, the steward's entry): the manifest assignment; the merge before W2-B; and **the home's CSS
  weight, said plainly** — 57 820 B gzip in three render-blocking sheets (`main.css` 43 169, `pages.css` 4 083,
  `hero.css` 10 568), which is **10 514 B over plan §2.6's Wave-1 ceiling for the home** (47 306 B). §2.6 item 5 («a
  family over its ceiling does not merge») was not applied: V5.5's performance rule, on the check's measurement
  above. The ceiling from here is `main.css`'s own plus the two page sheets as they weigh, 59 137 B. `main.css` itself
  is 764 B lighter than at `v54/w1-d`, so every other page type has that much more room.
- design-v5 `f43ca53` (no-ff; `8246a7f` + `1a21feb`). Steward's files (`d6ce32d`, the tag): `live_status.json` — the
  family row, state `v5`, and the first surface key, **`home`: `v5`**, with the tag; `CHANGELOG_V54.md` — the new
  entry first.

## Where to see it — http://127.0.0.1:8780

- **`/__design-v5/`** opens the real `/fr/` under the strip; the strip now lists the home under «Superfici V5».
  `/fr/`, `/ar/`, `/it/` and `/en/` directly for the page alone.
- **The first movement** plays once per browser session: open the home in a new window, or press the button over the
  golden key, which replays it. Then move the pointer over one of the four entrances, or Tab to it: the light runs to
  the door again, every time.
- **The phone**: the strip's phone frame (390 px), or a narrow window — the night band with the door and the rail,
  the four tiles, and the register of the four sentences under the hero.
- **Under the hero**, scrolling: the brand chapter (orientation), the pathways, the pilot's statement on the night,
  the four questions, «il gradino», the promoter and the partners, the reserved row. No news chapter today: no article
  is published in the preview's database.
- **`/ar/`**: mirrored, the door, the key and the marks as drawn; the French runs read left to right.
- `/__design-v5/index/` lists the family as passed, with its review (`/__design-v5/decisioni/w2-d/REVIEW.md`).

Checked on 8780 after the restart, by request only (no browser on the owner's server): `/fr/`, `/ar/`, `/it/`, `/en/`,
`/__design-v5/`, the index, the served review, `/fr/actualites/`, `/fr/attention-aux-fraudes/` and the two logins
answer 200, an unknown address 404. The four homes carry the Phase 3 hero, one `h1` each, the replay button named in
their language, six chapter heads, the plate and the register; the Arabic page is `dir="rtl"`. The three sheets, the
home's script and the two chunks it imports, the door's photograph, a plate, the grain and the sprite are served
with the built sizes. No external address and no inline style in the page; the Content-Security-Policy header is
the product's. The strip names `v54/w2-d`. The server log holds no traceback and no 500; no database connection was
left open. No page was opened in a browser on 8780. What a person sees there was looked at on the lane, on the same
tree: this merge's capture run — the first screen in French and Arabic at 1440 and 390 px, the chapters in French
at both widths — after the review, the check and the fix pass. At 1440 px the capture of the settled hero is byte
for byte the reduced-motion capture; the 390 px captures caught the first movement in flight.

## Tests (lane 5, `test_ile_v5_l5`; one pytest at a time; every run completed, none crashed)

On the branch with the steward's commits (`1a21feb` — the tree that was merged):

- Not in a browser — **1 361 passed, 0 failed, 0 skipped** (55 browser tests deselected; 21 min 14 s on a busy
  machine): `apps/pages`, all of `tests/i18n` (the locked texts, the catalogues' integrity, the pages' integrity in
  Arabic, routing, the RTL rules, the documentation), `tests/security`, `tests/frontend/test_design_docs.py`, the two
  bundle-currency files, the V5 tokens and the token rules, the script motion gate, the icons, the French typography,
  the inventory and ownership tools.
- In a browser (Chromium, one at a time) — **32 passed, 0 skipped** (4 min 12 s): `apps/pages/tests/test_browser.py`
  28 — the hero's geometry, the interim phone hero, a finger on the tiles, the door's `sizes`, the home under the hero
  as one system, the banner, the phone page — and `tests/frontend/test_browser_w1_b.py` 4.
- On design-v5 after the merge and the rebuild (`098cd29`): **948 passed** — bundle currency, the design documents,
  the tokens, the motion gate, the icons, the typography, the two tools, the locked texts, the catalogues, the home's
  tests, the pages' static and service tests.
- The fix pass's own runs on the last code (`NOTES.md` §9.5) stand beside these: the other browser modules that open
  the home, 86 passed. The full suite is the integration checkpoint's (V5.5); it was not run here.

## Not done

- **The door's shared sheet.** `static/css/v5/_door.css` is W2-B's and is not on design-v5: the hero's sheet holds the
  stage's rules, and `v4/hero.css` is shrunk, not deleted. When W2-B lands, `hero.css` imports `_door.css` and drops
  its copy.
- **The home's CSS is 10.5 KB over the plan's ceiling** (above; DL54-44). Nothing pins any CSS ceiling:
  `tests/frontend/test_css_budget.py` does not exist.
- **To say to the owner in words** (the review's row 5): when the first movement settles, the four photographs go back
  to black and white and only the door stays lit. If «→ colour» is expected to stay, it is one keyframe — a forward
  correction. The changelog's entry says it.
- **No picture under the hero**: after it come five screens of type (the review's reason for 3.5 and not 4 on the
  lower page). The frames are the imagery pass's, under O54 / O55; so are plate cuts at the ratios really drawn, a
  1 600 px derivative of the door and a WebP above 960 px.
- **RH-4 on phones is not met**: 10.3 screens at 390 × 844 and 11.2 at 360 × 800, where the rule says 9.5 (13.6
  before). The one lever left removes content a person reads on a phone; it was not taken.
- **Below 1536 px, two things remain in the wall**: in a tall window (1440 × 950 and taller) the fourth word takes
  two lines; and with a classic scrollbar drawn at 1440 × 900 one sentence takes a sixth line and the description's
  first line falls under the fold (DL54-43 item 3).
- **Accepted, in writing**: on phones the replay button takes the keyboard focus after the four tiles although it
  stands above them (`docs/ACCESSIBILITY.md` §3). **Not done**: the layers' weight while the movement plays (about
  10.9 MB at 1440 × 900, released at the settle; no dropped frame was traced to it).
- **The fix pass was not reviewed again** (V5.5: review once); its measures are the implementer's own.
- **In a prescribed text a line can still end on an opening guillemet** (seen in this merge's capture at 1440 px:
  the warning's «voies rapides»). The no-break space is written for team-authored strings only; in locked copy it
  is the owner's and counsel's decision (plan §1.19, B1 item 8).
- **Not measured or not run**: a real phone (touch was synthesised), a screen reader with a person, WebKit and
  Firefox; the Performance Lead's PASS on 8782; plan §1.17's parity check against the re-held prototype; the full
  suite.
- **Unchanged**: the echoes that are in the copy itself (the owner's packet B1), the order of the chapters (the back
  office's), and the dead code left on purpose with its owners (`NOTES.md` §8.8).
- **Not this area's, open on design-v5:**
  - **`collectstatic` fails under the production storage** (`SuspiciousFileOperation`: `portal/console.css` imports
    `v5/_loader-light.css` by a path that leaves `STATIC_ROOT` — W1-D's console entry). Run again at this merge, into
    a scratch root: it still fails. No 8782 window and no deployment is possible until it is corrected.
  - Six cases of `test_state_chips_carry_a_register` fail at the tag, on four of the preview's own templates
    (`_family.html`, `_row.html`, `_strip.html`, `index.html`) — the same six as at `v54/w1-d`; the test, the
    templates and the chips registry are untouched by this merge.
  - W2-C1's: the navigation's photographs are requested before `load`; its box shifts while the header is parsed; at
    1024 × 768 with a classic scrollbar the letterhead's four doors wrap onto a second row. W1-C's: a `.btn`'s focus
    ring on the night.

Evidence of the merge: `C:/tmp/ile_v5_council/evidence/v54/w2-d/merge/` (the state before, the ownership check before
and after, the capture run and its comparison, the build on design-v5, the three test runs, the `collectstatic` run,
the requests to 8780).
