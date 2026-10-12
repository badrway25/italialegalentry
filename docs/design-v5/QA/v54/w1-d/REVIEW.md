# W1-D · Motion foundation and the loader «Lume» — senior review

Reviewer label `w1-d-review` (built nothing). One pass, design + UX + taste together, against the owner's bar («credible
alongside excellent international digital products») and the settled direction — plan §1.5, §1.9, §3.3 item 6; DL54-05,
-07, -08, -09, -20, -21; V5.5 delivery mode (implement → review once → fix → ship). Branch `v54-w1-d` at `21b6b00`
(design-v5 `474ced9` merged in). Looked at on my own server, 8887, from `C:/tmp/ile_wt/v54-w1-d` on `ile_v5_l7`
(`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, the preview on for the specimen board), headless Chromium through
Playwright with profiles under `C:/tmp/ile_v5_council/.profiles/w1-d-review/`, signed-in pages through sessions minted with
`Client.force_login` by a scratch script outside every repository (no password used, typed or stored; one fresh session per
release capture, since the first console page consumes it; all revoked at the end). Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w1-d/review/` (`review.json`, the strips, the viewports); the probe
`C:/tmp/ile_v5_council/.work/w1-d/w1-d-review/probe_review.py`. The implementer's notes (`NOTES.md`, both steps) were read
first and their numbers were not re-derived where my own series confirmed them.

## Verdict — SHIP_AFTER_FIXES

0 blocking · 1 major · 5 minor. The loader is unmistakably ILE: it *is* the mark, drawn in layers that rasterise as the
one-file mark at rest, and the only thing that moves is the key's turn and the light inside the door — nothing cracks open,
the planes, the door and the steps never move, nothing loops, nothing is mirrored, and it costs nothing a person can feel
(the release is three compositor animations started at the first paint, no script, CLS 0; the busy key is one turn in the
click's own frame, label shift 0 px). Reduced motion is a real state, built once in the tokens and read through one gate.
The one thing that must change before shipping is a regression the «every form of the site» hook brings: a form whose
answer is a file keeps its busy face for ever.

## What I looked at

| Series | Where | Widths | Result |
|---|---|---|---|
| A · the release | the first console page after a sign-in (`/fr/espace-reserve/`, `/ar/…`), person and company | 1440 · 1366 (rail, 24 px) · 390 · 360 (bar, 20 px); device scale 1, 3, 4 | plays once per session on the visible seat; frames seeked at 0 · 80 · 200 · 360 · 700 · 1000 · 1200 · 1300 · 1400 · 1599 ms; the second page carries the `<img>`; CLS 0 in every case; the rest state is 0 px different from the `<img>` at 1×, 2× and 3× |
| A · real time | the same page, three fresh sessions | 1440 ×1, 1440 ×2, 390 ×2 | the release's three animations run from ≈ 100 ms and nothing runs at 2.3 s; light opacity 0 / scale 0.08, ink 0 at rest |
| A · the states | reduced motion (emulated setting), forced colours | 1440 ×4, 390 ×3 | 0 px change across the phase: the still is the verbatim mark |
| B · L2 on the login | a real submit of the empty form (allauth answers the page again; no credential typed), then the busy face applied to the same button for the frames | fr / ar · 1440 · 1366 · 390 · 360; pointer and keyboard; reduced motion; forced colours | `is-busy` + `aria-busy` in the submit's task, the focus where it was; the key 7.66 × 18 px at 55 % of the button's ink, inside the inline-end padding (left end in Arabic), `sig-turn 0.32 s × 1` on `--ease-turn` (0 s under the setting); label shift 0 px, box delta 0, label raster 0 of 16 236 device px changed; every answer lands at rest with its field errors |
| C · a form whose answer is a file | `/fr/compte/profil/` → «Exporter mes données (JSON)» | 1440 ×2 | the file downloads and the button stays busy — the major below |
| D · the specimen board | `/__design-v5/specimens/loader/` | 1440 · 390 · reduce · forced colours | 200, 33 hosts, 20 / 14 animations at load and **0 after 2.6 s**, 80 paused frames (32 under forced colours), no horizontal overflow, 0 console errors |
| E · reduced motion | home, login, dashboard, documents | 1440 | 0 running animations, 0 elements or pseudo-elements with a non-zero transition or animation duration; the tokens read 0 ms, `--motion-wait` 400 and `--motion-reduced` 80 kept |
| static | the branch | — | 564 targeted tests pass (`test_loader_rules`, `test_script_motion_gate`, `test_rm_flag_parity`, `test_v5_tokens`, both bundle-currency tests, `test_loader_w1_d` without the browser marks); `gen_loader_light.py --check` current; LF bytes on every changed text file; `check_ownership.py w1-d design-v5`: the 10 paths outside the slice are exactly the extras the notes declare; CSP `img-src 'self' data:` admits the key mask; 0 console errors across 547 requests, 0 tracebacks |

## Findings

### Major

**M1 — A form whose answer does not replace the page keeps its busy face for ever.** `shell.js` now sets the busy face on
*every* form of the site and `loader.js` adds `aria-disabled`; nothing ever rests a control whose answer is not a new page.
Measured on `/fr/compte/profil/`: «Exporter mes données (JSON)» downloads `italy-legal-entry-donnees-20261003.json` and
2.5 s later the button reads `btn btn--secondary is-busy`, `aria-busy="true"`, `aria-disabled="true"`, `cursor: progress`,
the key dim at 55 % — and V4's busy rule has turned the secondary button into a teal primary (`c_export_after_2500ms.png`).
A second press still downloads (nothing is refused), but the face never resets until the page is reloaded; Playwright
itself refused the second click («element is not enabled»), which is what assistive technology will say too. Before W1-D
`shell.js` touched only `form[data-single-submit]`, so this form was untouched: a regression of the propagation. It is the
only such form today (`apps/accounts/views.py::export_data`, `require_POST`, `Content-Disposition: attachment`); the
documents' downloads are links.
*Fix (small):* an opt-out the submit hook honours — e.g. `data-loader="none"` on the form: `shell.js` sets nothing and does
not import the loader, `main.js`'s guard is unaffected; the attribute on the export form in `templates/accounts/profile.html`
(a justified extra path for the steward, like the others, or the owning family's one-line edit); the rule written where the
hook is documented (`loader.js` header, DS 2026 §16, the loader's §10 entry): «a form whose answer does not replace the page
— a file, a new window — opts out». A line in `test_loader_rules.py` that every form posting to a view answering with an
attachment carries it would keep the next one honest.

### Minor

**m1 — At the served size the release is a whisper at 1×.** Between t = 0 and 360 ms the lit change is a 6 × 8 CSS-px
region inside the rail's 24 px mark (44 of the 52 × 52 crop's pixels change by more than 24/255; mean |Δ| 1.9/255 over the
crop) and 4 × 7 px in the bar's 20 px mark (`a_fr_1440_x1_strip.png`, `a_fr_390_x1_strip.png`). At 3× and 4× the sequence
is exactly the designed one and reads beautifully — the light from the bow, the room lit with the key in ink, the hold, the
withdrawal into the eye, the gold key back on navy (`a_fr_1440_x4_strip.png`, `a_fr_390_x3_strip.png`) — and the plan's three
measured conditions pass at the seat (the implementer's ΔE00 series, re-read on my own frames). Nothing to change in the
build: the seat is the plan's, and the fallback conditions did not fire. It is the honest limit for the owner's report: on a
1× desktop a person will not notice the release unless told where to look; the signature becomes legible when W2-B wires the
engage on the login's stage at 160 px (the key's turn, then this release on arrival). The report should say so in words and
the preview's index should name the seat («sulla prima pagina della console, nel marchio della rail») beside its sign-in state.

**m2 — The release does not play alone at the entrance.** On the dashboard, from the first paint, `rail-draw` ×4
(900 ms, `.journey__step::before`) and `strip-fill` (320 ms, `.health__segment`) run beside the release's three animations
(`review.json` → `ART.*.names_early`): V4's console entrance animations, which the plan's own rule retires («the console has
no entrance and no stagger at load», MS §3.2) and which put three sequences on screen at once (T-3 allows one tier-3 *or*
tier-4). Not W1-D's files — W3-B (the dashboard's strip) and W3-D (the journey rail); a row for the steward's deletion map so
the entrance is the release alone when those families land.

**m3 — V4's busy rule still shapes every busy button.** `static/css/v4/buttons.css:105–134` sets `--btn-fill: var(--accent)`,
`--btn-ink: var(--min-3)` and the primary gradient on `.btn.is-busy`, so a secondary or ghost button becomes a primary while
it waits (the export button above; the board's «secondario · occupato»), against V5's flat, rank-by-surface hierarchy
(DL54-13); and it keeps the dead `btn-busy 1200ms linear infinite` keyframes — overridden by `v5/loader.css`, but the only
`infinite` left in the cascade. W1-C's file: when `v5/buttons.css` lands, drop the fill/ink override (a busy button keeps its
own surface; the key takes its ink, which `v5/loader.css` already expects with `var(--btn-ink, var(--accent))`) and delete
the keyframes.

**m4 — Under reduced motion the release leaves no trace.** The first console page shows the verbatim mark, 0 px different
from the `<img>` (`a_rm_fr_1440_x4_strip.png`), exactly as §1.9 asks («the end state, without travel») and as A11Y §7 now
says. L2 keeps a designed still (the dim key, present on the control); the release has none, so a person who asked for
reduced motion never sees the signature at all. Plan-compatible polish, for the CD to take or leave: under the setting (and
`html.rm`) `[data-lume="release"]` could hold the *lit* picture — light at scale 1, key in ink — for that one page, once per
sign-in by the same flag, no travel, the next page showing the mark. The trade-off is a lit mark that stays for the page's
visit, a statement the no-preference person never sees; if kept as built, nothing to do.

**m5 — `aria-disabled` on controls that nothing refuses.** `loader.js::busy()` sets `aria-disabled="true"` on every
submitted control; only `form[data-single-submit]` (allauth's forms) actually refuses the second submit. On the other forms the
attribute announces a refusal that does not exist — moot while the page is replaced within ≈ 110 ms, visible in M1's case.
With M1's opt-out in place this is consistent again; otherwise set `aria-disabled` only where `main.js`'s guard holds.

## Reviewed, no action

- **The key's turn.** `rotateY` 0 → 360° about the shaft on `--ease-turn`, with a little perspective: at 160 ms the key is
  edge-on, then the verbatim key — a turn, not a flip; the mirror image passes between 90° and 270° as DL54-08 says, and the
  host is `direction: ltr` in Arabic (the rail's mark unmirrored in the RTL console, `a_ar_1440_x4_viewport_t360.png`).
- **The keyboard submit plays the same turn** (DL54-20 item 5): an activation, not a navigation key; the focus stays in the
  field it was in (`kbd_fr_1440_x3`: `focused: false`, `is-busy` set). Agreed; no `html[data-input="key"]` rule needed.
- **The light stays inside the door** at every seat and scale I shot; the muddy tone is gone on the way out after `dd20d3f`
  (the 1200–1300 ms frames show a shrinking cream disc, not a grey blend).
- **No hang at 0 ms, one gate, no event waits**: read in `motion.js` / `loader.js`, held by the static tests; `main.js` (V1)
  still asks the media query itself for the reveal and the counters — W4-B's slice, as the notes say.
- **Performance**: nothing to add to the implementer's trace; my real-time runs show 0 running animations at 2.3 s, CLS 0,
  `loader.js` fetched on the first submit only; `main.css` +1.2 KB gzip, inside the Wave-1 allowance.
- **The board** is a dev artefact and reads clearly at 1440 and 390; 0 console errors.
- **Ownership**: the ten paths outside the slice are the declared extras (`apps/accounts/apps.py`, the templatetag pair,
  `static/css/dev/loader-board.css`, `static/css/main.css` one import, `static/css/v5/tokens.css` the reduced-motion block,
  `static/js/src/{console,shell,situation}.js`, `tests/frontend/test_design_preview.py`); the merge step writes them in.

## Honest limits of this review

Chromium only (no Safari or Firefox locally). The release's frames are deterministic seeks every 40–360 ms of animation
time; the real-time clock was sampled at 100 ms on three loads, not recorded at 60 fps. No person watched the motion at
speed. The login's submit was measured with the form empty; the busy face's frames come from the same button with the class
applied, since the empty submit is answered in ≈ 110 ms. L3 has no product container yet, so the seat was judged on the board
only. The second run of the company case reused a session whose release the first run had consumed — my pool, not the
product; the first run's company case passed like the others.
