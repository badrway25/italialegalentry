# W2-B · Login «Il varco» and the entrance pages — implementation notes

The family's implementer (label w2-b-impl-1). Append-only: each step adds a dated section. Heavy evidence (captures,
films, traces) under `C:/tmp/ile_v5_council/evidence/v54/w2-b/` (E/ below), outside every repository; scratch tools under
`C:/tmp/ile_v5_council/.work/w2-b/w2-b-impl-1/`. Lane 7: dev server 8787 on `ile_v5_l7`, `ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`; pytest on `test_ile_v5_l7`. Branch `v54-w2-b` from `design-v5` (`8246a7f`); plan
`docs/design-v5/V5_4_EXECUTION_PLAN.md` §1.13, §1.9, §3.4 item 2, under V5.5 delivery mode (implement → review once →
fix → ship). One headless Chromium at a time (Playwright's headless shell, Chromium 153, its own profile); never 8780,
never the owner's Chrome. The second factor's page and the re-authentication page were reached through sessions minted
on `ile_v5_l7` for a throwaway account with an unusable password (`mint.py`, outside the repository:
`Client.force_login`, and allauth's own `perform_login` for the sign-in that waits for its code) — no password used,
typed or stored. That account, `w2b-probe@example.test`, stays in the lane's clone for the form's step.

---

## Step 1 of 2 — the stage (9 October 2026)

The owner: «concept good; the left side too static». The stage is now a place with depth that answers the person, and
it is silent when nobody acts. The form's panel is still V4's: its design is step 2.

### What was done — the commits, oldest first

| Commit | What |
|---|---|
| `7bba19d` | `static/css/v5/_door.css` (new, a `_` partial the entrance imports): **the owner's door stage as drawn** — the vector parts in one SVG in stage units (`264 64 368 456`), the photograph an `<img>` in a box of the arch's shape, the key the verbatim `key.svg` as an HTML layer on the loader's primitive (`.sig__l` / `.sig__turn`), and two pre-painted lights the stage can take, its frame and its steps (`--door-frame`, `--door-steps`). `direction: ltr`: never mirrored. Its literals are the block §4.3 appended to `static/css/v5/tokens.css` |
| `ea030a5` | `templates/allauth/layouts/entrance.html` draws the stage in full; `apps/accounts/static/accounts/entrance.css` (rewritten; the block is `.varco`) places the niche, the floor and every state; `static/js/src/entrance.js` (new) writes the states as classes; `templates/allauth/elements/form__entrance.html` (new, **outside the slice** — see «For the merge») names the stage on the sign-in's forms; `components.css` §27 loses the entrance's narrow container |
| `41d295a` | Bundles rebuilt (CSS; JS from a clean `dist`) |
| `2088a14` | The scene and the help line stay in sight on a page longer than the screen (the signup); an address being typed is read at the typing pause; the arrival waits for a largest-contentful-paint entry and the photograph's decode |
| `cdcc9e7` | `tests/frontend/test_entrance_w2_b.py`, `tests/i18n/test_rtl_browser_entrance.py`; a pass class that stayed on the stage for good, found by the submit test (passes are now counted per light) |
| `f777e02` | Every part of the entrance has its place before it is parsed: grid lines and a reserved band row, never `order` (layout shift 0.446 → 0 at CPU ×4) |
| `ffc4ede` | The element that takes the focus asks for its own state, with its pass (leaving the e-mail field for the password's show / hide control wrote the frame without a pass: seen in the Arabic run) |
| `d053d19` | Three alias tokens removed; `docs/design/DESIGN_SYSTEM_2026.md` names the entrance, its six keyframes and its module |
| `b28eaab` | The night of the stage's place is painted by the page's own box, so a paint that comes before the stage shows the niche's ground and not the light page turning dark; every part names its grid cell in full. **In Arabic the room kept for the password's show / hide control is on the control's side** (the placeholder and the typed password ran under it at 390 px, on V4 as on V5) |
| `d78ae32` | **The stage's paints are a page-only partial**, `static/css/v5/_varco.css` (new, **outside the slice**): `main.css` no longer carries the login's picture (−524 B gzip on every page of the site) |
| this one | DL54-39 and these notes |

### The stage as built (plan §1.13 → where it lives)

- **Depth, drawn** (`entrance.css` places, `_varco.css` paints). A night niche behind the page's light wall: the wall's
  thickness as two stone rings at the seam (`--varco-reveal`, 10 px) and the shadow the wall casts into the niche; the
  door on a threshold; **four ways in the audience accents** rising from the lower edge and converging on the threshold
  (the vanishing point is 41 stage units inside the door); a low warm pool at the steps' foot (12 % at rest); the 3 %
  grain; the help line under a hairline. This is also the no-JS state and the reduced-motion rest.
- **The stage answers the person** (`entrance.js` writes classes on `[data-varco-stage]`; the sheet draws them):

  | The person | The state | What is lit | The way to it |
  |---|---|---|---|
  | focuses the e-mail field | `is-ways` | the four ways | one pass, `--motion-slow` + `--motion-fast` (600 ms): a light runs up each way, the lit way is drawn behind it, the bead goes out at the threshold |
  | has typed a valid address | `is-held` | the threshold's line, the pool, the three steps | opacity, `--motion-standard`; the steps `--motion-stagger` apart |
  | focuses the password (or its show / hide control), or has typed one | `is-frame` | the door's frame, in the key's gold | one pass, `--motion-slow` (480 ms): the light rises from the threshold along the arch |
  | submits the sign-in | `.is-engaged` (the loader's) | the key turns once and holds | `sig-turn`, `--motion-slow`, `--ease-turn` — `loader.js` through `data-loader-host="varco-door"` |

  A state is a function of the form, never a memory: clearing the address or leaving the form gives back the state of
  what is left, in 200 ms, without travel. A pass is asked only by a pointer's focus; from the keyboard the states are
  there at once (`html[data-input="key"]`, tier 0); under reduced motion every state appears at its end.
- **The arrival, once**: the four lights travel into the threshold one after the other (`--motion-route-light` each,
  `--motion-route-stagger` apart: 2.4 s), after the door has been painted; any focus, input or submit cuts it. Never
  on a refused sign-in's page (it loads at rest, with the still of the kept address), never on a page reached from
  another entrance page, never from history, never on the band, never under reduced motion.
- **Below 64rem** the stage is a band above the form — the door and the help line: 121 px at 390, 141 px from 48rem,
  72 px under 44rem of height; the frame answers for all three states, and the key turns on submit.
- **Motion rules held by tests**: nothing loops (every animation `1` iteration, on duration tokens); only `transform`
  and `opacity` move; every pass keyframe has a `from` only and ends on the element's own state; the lights are
  contained (`contain: strict` / `layout paint`) and no text sits on one; no `will-change`; the script writes classes
  only (no style, no `animate()`, no frame loop, no string).
- **RTL**: the page mirrors (the stage at the reading edge, the help line at its start), the drawing does not — door,
  key and ways are `direction: ltr`, Persona's way on the left in every language. **Forced colours**: the hairlines in
  `CanvasText`, no light layer, the steps with a `Canvas` edge. **No JS**: the complete rest.
- **Before the stage is parsed** (a slow browser paints in between: at CPU ×4 the first paint came before the form's
  submit and the stage's door had been parsed in six loads of six in one sitting, in one of six in another — it depends
  on what else the machine is doing): the form is at its place, and the stage's place is already the night
  (`E/step1/measures/stage-not-yet-parsed-before/` and `-after/`).
- **The same layout** serves the signup, the password reset (form, sent, bad key, done), the e-mail verification (sent,
  bad link), the inactive account, the second factor and the re-authentication: each checked (`E/step1/pages`). The
  states run wherever a page has an e-mail or a password field; the key turns on the login and on the second factor's
  code only.
- **Three sheets**: `entrance.css` (the app sheet: the page's grid, the parts' places, the states, the passes, the form
  as it was), `v5/_door.css` (the door stage, to be shared with the home's hero and the console), `v5/_varco.css` (the
  stage's gradients, page-only). The token block holds the door's four literals and five colours.

Decisions met during the build are **DL54-39** (thirteen items: the three lights, «600 ms» on the tokens, the typing
pause, the arrival's conditions, `form__entrance.html`, no words of a long wait, the source order with the placement
and the ground, the promoter's line, the block's name, the door stage's structure, the sticky set, the Arabic password
correction, the paints' partial).

### Measures (lane 7, the dev server; Chromium headless; `E/step1/`; re-run on `d78ae32`)

- **Captures looked at**: `rest/` — fr, ar, it, en × 1920, 1440, 1366, 1024, 390, 360 × 640: 24 pages, 0 px of
  horizontal overflow, 0 console or CSP issue; `stills/` (20: reduced motion, no JS, forced colours, each at rest and
  with states); `states/` (14); `films/` (the arrival, the two passes and the key's turn, frame by frame, with contact
  sheets; the key in Arabic); `pages/` (the other entrance pages; 320–430 px in fr and ar, and 768 and 1023 px: 0
  overflow); `before/` (6).
- **L7 — the scripted person** (`measures/l7-*.json` and captures; fr and ar at CPU ×1, fr at ×4). The LCP element is
  the door's photograph (236 ms ar, 512 ms fr on the server's first answer; 560 ms at ×4); the arrival starts 37–38 ms
  after that entry (153 ms at ×4), lasts 2.4 s, and the click on the e-mail field at 2.0 s cuts it. Then:
  `is-ways is-passing-ways` at 2.04 s → `is-ways` at 2.65 s; the address typed from 3.6 s is valid at ≈ 4.8 s and
  `is-held` is written at 5.27–5.29 s (5.42 at ×4), after the pause; the password clicked at 7.0 s →
  `is-frame is-passing-frame` → `is-frame` at 7.50 s. **At t = 10 s three person-driven states are visible**
  (`l7-fr-t10.0-three-states.png`, `l7-ar-…`), and `document.getAnimations()` is empty at 3.2 s, 6.0 s, 8.1 s and 10 s.
  Layout shift 0 and no long task at ×1; at ×4 two long tasks of 86 and 96 ms, during the load, before the arrival.
- **L8 — the engage delays nothing** (`measures.json`, n = 8 each, the POST answered at the network): submit → the next
  document's time origin 7.2 ms with motion, 5.0 ms under reduced motion; → its first contentful paint 43.6 ms against
  37.3 ms. Under one frame.
- **L9 — on the compositor** (`trace-fr-cpu1.json`, `trace-fr-cpu4.json`, `layers-fr.json`): 28 animations and
  transitions of the stage over the scripted run, **0 `compositeFailed`** at ×1 and ×4; the ways' lights are strips of at
  most 488 × 16 px; the only text on a layer of its own is the pinned letterhead. No long task overlaps or follows the
  arrival's start (`longtasks_arrival_ab.json`, six loads at ×4 with motion against six under reduced motion: one to
  three long tasks per load in both, 136 ms against 153 ms in total at the median, the longest 130 ms; L9's
  comparison with R3B's first-render task, 398–485 ms on the twin, is the performance check's).
- **L10 — the stage moves no text** (`measures.json`, device scale 2): 0 changed pixels in the form's panel
  (2 659 536 px) and in the help line across paused frames of the arrival and of both passes.
- **Layout shift at CPU ×4, cache off** (`cls.json`, five loads each, fr and ar at 1440, 1024, 390, 360): 0 at 390 and
  360; from 64rem at most 0.029, and the form's box is the same with and without the stage in the document (held by a
  test, eight cases). The sources are not the stage's, with one exception: in one load of forty (ar 1024) the help
  line's own block moved 40 px as its paragraph arrived (0.0017). What moves is the public navigation (≤ 0.02) and
  **the V4 sheet**: it is centred in its panel, and painted before it is whole — 350 px tall, up to the e-mail field,
  of 518 — it moves up by half of what arrives (`sheet-shift-why-fr-1440.txt`,
  `first-paint-before-the-form-is-parsed-fr-1024.txt`). `order_ab_n24-run1.txt` and `order_ab_n24.json` serve the same
  document as built and with the stage first in the source, CPU ×4: over two runs of 24 loads × 4 cases the sheet
  moved in 57 loads of 192 as built and in 57 of 192 with the stage first, 0.005–0.05 each time. The source order is
  not the cause; the centring is, and it was there before this step.
- **L6 — the order**: after the skip link the stops are the signup link, `#id_login`, `#id_password`, its show / hide
  control, the reset link, the submit, then the help line's address (`probe2.json`). A refused sign-in loads with
  `is-still is-ways is-held`, the focus on `#form-errors`, the address kept, the password empty, no arrival.
- **Phones**: at 360 × 640 the submit's lower edge is at 574 px in French, 528 in Arabic, 550 in Italian and English —
  in the first viewport. The page is shorter than before at 390 (1 838 px against 1 854) and at 360 × 640 (1 817 against
  1 894): the band pushes nothing down.
- **The password in Arabic** (`measures/password-field-before/`, `-after/`): the field is `direction: ltr`, its control
  at the left; the room kept was at the right (16 px / 176 px of padding, left / right). Now 176 / 16: placeholder and
  typed password at the field's start, clear of the control at 390, 768 and 1440; French unchanged.
- **Weights (gzip −9)**: `dist/main.css` 43 933 → **44 047 B** (+114: the token block); `dist/accounts/entrance.css`
  1 208 → **4 157 B** (the door as drawn ≈ 1.2 KB, the paints ≈ 0.7 KB, the places, states and passes); `dist/entrance.js`
  1 664 B (3 613 raw), **one more JS request** before `load` on the entrance pages (6 against 5; CSS 2 = before). It
  imports the shared chunk `shell.js` already loads on every page (71 896 B, unchanged; its hashed name changes with
  the new entry). Against the Wave-1 ceilings of plan §2.6: the home 46 867 of 47 306, an interior page 44 047 of
  44 486, the dashboard 49 670 of 49 860 — and **the login 48 204 of 45 694: 2 510 B over** (see «What is left», 4).

### Tests

On `d78ae32` (the last code commit), `test_ile_v5_l7`, one pytest at a time:

- **Not in a browser** — `pytest -m "not browser" apps/accounts tests/frontend tests/security tests/i18n`: **1775
  passed, 6 failed, 2 xfailed** (16 min). The six failures are `tests/frontend/test_state_chips_carry_a_register.py` on
  `templates/dev/designpreview/{_family,_row,_strip,index}.html` — the preview hub's `dp-state` chips, W1-P's: neither
  the test nor those templates nor `apps/core/chips.py` differ from design-v5 `8246a7f`. The allauth flows
  (`apps/accounts`), `test_layout.py`, `tests/security`, the catalogues and the locked texts,
  `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_design_docs`, `test_v5_tokens`,
  `test_loader_rules` and `test_rtl_static` are in the 1775.
- **In Chromium** (`-m browser`, 0 skipped) — `tests/frontend/test_entrance_w2_b.py` and
  `tests/i18n/test_rtl_browser_entrance.py`: **43 passed** (15 on the sources, 28 in the browser);
  `tests/i18n/test_rtl_browser.py`, `tests/frontend/test_loader_w1_d.py` and `tests/frontend/test_layout.py`: **45
  passed**.
- Two of the new tests were held against their defect: the password test fails in Arabic at its three widths when the
  `[dir="rtl"]` rule is taken out of the built sheet; the band's full-width assertion is the 242 px sheet an auto-placed
  part produced at 390 px, seen in the pixel comparison before `b28eaab` was committed.
- Not run: the full suite (V5.5). Not written: the 429 test (step 2, with the page).

### For the merge (the steward)

- **Two paths outside the slice**, both new. `scripts/check_ownership.py w2-b design-v5` → **FAIL** until the manifest
  names them.
  - `templates/allauth/elements/form__entrance.html`: the engage needs `data-loader-host` on the sign-in's `<form>`,
    which allauth's `form` element writes; allauth looks for `form__entrance.html` before `form.html` on this layout, so
    the attribute is added for the entrance alone and `form.html` (W3-F2's manage pages) is untouched. A test holds the
    two elements equal but for that attribute.
  - `static/css/v5/_varco.css`: DL54-15's bust rule («moves page-specific rules into page partials»), applied to the
    stage's gradients — as tokens they put three page types over their ceilings (DL54-39 item 13).
- **Slices used**: `tokens.css` — one named block appended at the end (§4.3; W2-D appends its hero block at the same
  place: keep both); `components.css` — one rule of §27 deleted (`.account-page--entrance`); `DECISION_LOG_V54.md` —
  DL54-39, to renumber if another family's entries land first.
- **DS 2026, beyond the letter of the slice** («the prose of the entrance»), each needed by `test_design_docs`: the row
  of `entrance.css` in §2.1; `doorway.html`'s consumers and example in §10 (the entrance no longer includes it); a dated
  paragraph in §12 naming the six keyframes; the row of `entrance.js` in §16. The weight of `v5/tokens.css` in §2 was
  rewritten by `scripts/regen_design_inventory.py --write` (41.6 → 43.9 KB), not by hand.
- The bundles are committed as built here; the chunk names follow this worktree.

### What is left

For step 2 of this family (the form):
1. The form «la lastra» of plan §1.13 — hierarchy, fields, the reset link's slot, the flat CTA with its key (L14), the
   four unhappy states and the error page's title (L4), `templates/429.html` and **its test** (L12; not written: the
   page does not exist yet), the project `account/login.html` (it can extend allauth's own template rather than restate
   it), the skip link's target, `lang` on the Latin runs of the Arabic page.
2. **The sheet's place must not depend on its height.** It is the one real source of layout shift left on the entrance
   (three loads of ten at CPU ×4, up to 0.05 against a budget of 0.05 on a flagship), and a taller form will move
   further. Three ways, in the order I would try them: place the sheet from the top of its panel (a fixed offset; the
   title then stands at the same height on every entrance page); or keep the centring and show the sheet only once it
   is whole (`:has()` on a last-child sentinel); or hold the first paint (`<link rel="expect" blocking="render">`),
   which this headless shell does not implement (`relList.supports('expect')` is false) and so could not be measured
   here.
3. **Placeholders**: at 360 px the password's placeholder is cut short by the room kept for the control («Mot de pas»,
   `rest/rest-fr-360.png`); the plan's removal of the placeholders ends it.

Not done, and why:
4. **The login's CSS is over its ceiling** (48 204 B gzip of 45 694; +3 063 B on design-v5, of which 114 in `main.css`).
   It is the stage itself: the door as drawn, the niche's paints, the states and the passes. DL54-15 lets the CD raise a
   page type's ceiling once by ≤ 2 KB after the Performance Lead's measure on 8782: that leaves ≈ 0.5 KB to find, and
   step 2 replaces the V4 form rules (≈ 0.8 KB of the sheet). Not trimmed here: for the performance check and the CD.
5. **The words of a long wait** (`word`, `slow`, `retry` of the loader's host): no live string exists in any catalogue
   for «Ouverture…», «C'est plus long que d'habitude.» or «Réessayer» (CDV §17's proposal; O32 of the owner's copy
   packet, B1), and Arabic is never written by us. The stage engages without them: the state is carried by the
   submit's `aria-busy` and its key, and with no «Réessayer» on offer the form is given back at 10 s. One include in
   the layout the day the strings exist.
6. **The photograph at a device scale of 2**: the one live file is 400 px wide; from 64rem the arch is drawn 200–360 px
   wide, so it is soft on a dense screen. The door-master derivatives (`static/brand/v5/`, W2-D) are not on design-v5
   yet: a `srcset` on the stage's `<img>` when they are.
7. **The promoter's line is not repeated in the stage** (the plan lists it among what is kept): the entrance keeps the
   public letterhead, whose utility bar prints the line above the same column (DL54-39 item 8). For the review to
   confirm or overrule.

Not verified:
8. Chromium only, headless. No Safari, no Firefox; where `largest-contentful-paint` is not reported the arrival waits
   for the load instead — that branch was read, not run. `_varco.css` needs `color-mix()`, as six sheets of the
   cascade already do.
9. Nobody watched the motion at speed: the films are paused frames, and the traces say what ran and where.
10. The full suite was not run (V5.5). The before / after on the owner's preview and the budgets' PASS on 8782 are the
    performance check's.

For other families:
11. **W1-C** — the cascade's own rule for the password's room (`v4/buttons.css`, `padding-inline-end` on a field that
    is `direction: ltr` in Arabic) serves every password field outside the entrance (the account's password pages): the
    same defect, not looked at here.
12. **W2-D / W2-E** — `templates/components/doorway.html` has one consumer left, the home's hero; once W2-D's own door
    lands, the component and the doorway rules of `v4/hero.css` have none.
13. **W2-C1** — without JS at 390 px the public navigation is laid out open above every page's content (the entrance's
    form starts about 1 400 px down: `stills/still-nojs-fr-390.png`); at CPU ×4 the navigation is the source of shifts
    of up to 0.02 on this page.
14. Under forced colours at 390 px, a focus re-rasters the arch's top outline with a different anti-aliasing in two
    runs of three (65 px, a channel delta of 71 at most, nothing a person sees; the frame's light is `display: none`
    there). Noted because the pixel comparison of the stills reports it.

---

## Step 2 of 2 — the form (9–10 October 2026)

The family's second implementer (label w2-b-impl-2), same lane and same rules as above: dev server 8787 on
`ile_v5_l7`, pytest on `test_ile_v5_l7`, one headless Chromium and one pytest at a time, the benchmark lock checked
before every browser series and every build, no run ended on «Target crashed». Scratch tools under
`C:/tmp/ile_v5_council/.work/w2-b/w2-b-impl-2/`, evidence under `E/step2/` (`rest/`, `states/`, `pages/`, `stills/`,
`measures/`). The pages behind a sign-in were reached with sessions minted on the lane's clone for three throwaway
accounts with unusable passwords (`mint.py`: `Client.force_login`, and allauth's own `perform_login` for the sign-in
that waits for its code and for the one whose address is not verified; `mint_keys.py` builds the two signed links
allauth e-mails) — no password used, typed or stored. The owner: «the form too simple».

### The core components were not on design-v5 — what this branch did, and what is still to do

This step builds on the core components' fields «la lastra» (W1-C). **The tag `v54/w1-c` did not reach design-v5
during this step.** It was looked for every two minutes from 21:50 on 9 October until the two hours the step allows
had passed (23:52: the watch ended at its limit, without the tag), and again before these notes were closed
(01:51 on 10 October): design-v5 had moved to `887c8aa` — W2-D's hero merged and tagged `v54/w2-d` between
01:38 and 01:51 — still without this tag, and `v54-w1-c` was at `61cf067`: W1-C's review landed at 22:45
(SHIP_AFTER_FIXES), its accessibility and performance check at 01:41 (SHIP_AFTER_FIXES, the report only), its fix
pass not yet. When the step began `git merge design-v5` was a no-op (`8246a7f`), and on design-v5 alone the form can
be neither measured nor tested (run on the branch before the merge, `b342dce`, 11 of the form's browser tests fail
for want of `v5/field.css` and `v5/buttons.css`). So:

- the form was first built and measured on a **throwaway merge** of this branch with `v54-w1-c`, under the scratch
  directory (W1-C's own method for the loader family);
- at the end of the two hours **`v54-w1-c` was merged into this branch as reviewed** (`7e867e4`, before its fix
  pass): `75c1ba1`. That is a merge of a sibling family's branch, not of design-v5 — a decision of this step, taken
  because every later step of this family (the review, the checks) needs a branch that draws and tests what will
  ship. The branch without the core components is `b342dce`.
- **Still to do, by whoever syncs next: `git merge design-v5` once it carries `v54/w1-c`.** W1-C's fixes then arrive
  on top of `75c1ba1`. What will meet there:
  - `templates/components/form_field.html` — W1-C's review asks for the two changes this branch already made in
    that file: the help as a `<div>` (its M1) and the show / hide control as a glyph in a 44 px seat (its M2). When
    W1-C's fix has made the glyph the system's control, this branch's own copy of it goes: the `reveal` argument,
    `templates/allauth/elements/fields__entrance.html`, the `.form-field__toggle--glyph` /
    `.form-field__control--glyph` rules and the help-list rule of `entrance.css`, and the two test lines that name
    them. The label row's aside stays.
  - `static/js/src/shell.js` §3 — W1-C's M2 «swaps the glyph and no longer writes `textContent`»: keep this
    branch's kept caret (`setSelectionRange` after the type change) and the keyboard's press that leaves the focus
    on the control.
  - W1-C's M3 gives every public form's action 52 px and the large pads (`body:not(.console) .form__actions .btn`,
    (0,3,1)): it beats this sheet's `.varco .form__actions .btn--primary` with the same values, and loses to the
    sign-in's holder rule (0,4,1) — but check the second factor's and the new password's «Annuler», a link button
    in the actions row, against it.
  - `docs/design-v5/DECISION_LOG_V54.md` — on this branch this family's entries are **DL54-52** (the stage, written
    as DL54-39 in step 1: read «DL54-39» in the step-1 section above as DL54-52) and **DL54-53** (the form), after
    W1-C's DL54-39 … DL54-51. **These numbers do not survive the merges**: design-v5 has since given DL54-39 …
    DL54-44 to W2-D's and the steward's entries, so W1-C's thirteen and this family's two are numbered again when
    the branches meet. The two entries are «W2-B: the stage of «Il varco» as built» and «W2-B: the form of «Il
    varco» as built»; this family's code cites only numbers design-v5 already holds (DL54-07, -08, -13, -15) and
    none of those that move (`6e66f88`); its notes and the two entries' own lines cite them. `DESIGN_SYSTEM_2026.md`
    §2's table is W1-C's (regenerate the figures); §2.1's row of `entrance.css` and §10's `form_field.html` are this
    family's prose.
  - design-v5 itself has moved since this branch last met it (`8246a7f` → `887c8aa` when these notes were closed:
    W2-D's hero). Step 1 expected it: W2-D appends its token block to `static/css/v5/tokens.css` where the door's
    block is — keep both; `main.css` then changes for every page, so the login's weight is to weigh again.
  - The throwaway worktree and its branch (`…/w2-b-impl-2/trial`, `v54-w2-b-trial`) were deleted at the end of the
    step.

### What was done — the commits, oldest first

| Commit | What |
|---|---|
| `49f00b8` | `accounts.forms.LoginForm` — allauth's form with its presentation only — wired by `ACCOUNT_FORMS["login"]`; the project's `SignupForm` writes no placeholder |
| `7107948` | the templates: the layout's hierarchy (eyebrow, the error said first in the title, the way back); `templates/account/login.html` (new: extends allauth's own, adds the assurance); `templates/429.html` (new); `form_field.html` (the label row's slot, the help as a `<div>`, the glyph control) and `templates/allauth/elements/fields__entrance.html` (new, **outside the slice**); `static/js/src/shell.js` §3 (**outside the slice**: the caret kept) |
| `94eab9c` | `apps/accounts/static/accounts/entrance.css` §5 — the form on the paper |
| `97ade8f` | the tests: `apps/accounts/tests/test_login_form_w2_b.py`, `tests/frontend/test_429_w2_b.py`, `tests/frontend/test_entrance_form_w2_b.py`, the form in `tests/i18n/test_rtl_browser_entrance.py` |
| `b342dce` | interim notes (replaced by this section) |
| `75c1ba1` | **merge of `v54-w1-c` (`7e867e4`)** — see above; conflicts: `entrance.css` (this branch's), DS 2026 (§2's table W1-C's, the entrance's row ours), DL54 (W1-C's 39 … 51 kept, ours → 52), the bundles rebuilt |
| `b820837` | the sheet names no control: W1-C's guard («entrance.css draws no control», DL54-44) holds on the merged tree |
| `c6c8f56` | the glyph control has one name and no tooltip twin (`title` removed); two browser tests — the control's name, state and kept caret; the page without script |
| `c2984a6` | **no part of the form's column waits for a later one**: the eyebrow's row has its line's height before its words are parsed, the label row's link has the label's own line in Arabic too — with the test that takes the later parts away; a refusal's summary stands on the form's rhythm |
| `6e66f88` | two comments cite W1-C's decision by its name — the number they used, DL54-44, names another decision on design-v5 now (comments only: the bundle is byte for byte the same) |
| this one | DS 2026 (the entrance's row and its weight, `form_field.html`'s contract), DL54-53, these notes |

### The form as built (plan §1.13 → where it lives)

- **A column on the paper, hung from the top of its panel** (`entrance.css` §5). No card: 25rem, centred in the 7 / 12
  panel, on the page's own ground (no light painted on it). From 64rem its distance from the letterhead is
  `clamp(3rem, 14vh − 1rem, 12rem)`: the title stands at the same height on every entrance page — level with the
  top of the arch — and the column no longer moves while the page loads (step 1's item 2: the V4 sheet was centred
  on its own height).
- **One hierarchy on every entrance page**, written by `templates/allauth/layouts/entrance.html`: the eyebrow
  «Espace réservé» with the registry's key (`ile-key` — not `ile-steps` as the plan wrote: DL54-53 item 2), ONE title
  (28 / 36, 36 / 44 from 48rem, balanced), the page's sentence at 17 / 28, the fields, ONE primary action, then what
  is quiet. A page that is not a form ends with the way back to the sign-in («Se connecter»), for a person who is
  not signed in. When a form comes back with errors the document's title says so first («Erreur — Connexion · …»).
- **The fields are the system's «la lastra»** (52 px, the label above at 14 / 20, typed text 16 px, the one ring with
  its halo and the 2 px rule, an error by its doubled edge, its mark and its words). This sheet draws no control
  (W1-C's guard). It adds:
  - **the label row's slot** — the sign-in's «Mot de passe oublié ?» at the end of the password's label row. It is
    allauth's own help text (its message, its catalogue: `account/password_reset_help_text.html` is **not** written —
    DL54-53 item 4); `LoginForm` marks the field `help_beside_label`, `form_field.html` writes the help as the
    `form-field__aside` **after the control** (from the keyboard: the address, the password, its control, the link,
    the action) and the sheet places it in the label's row with a grid; 24 px target, 44 px under a finger, grown
    upward so that it never lies over the field below;
  - **the show / hide control as a glyph** (`reveal="glyph"`, on every entrance form through
    `fields__entrance.html`): the registry's eye in a 44 px target inside the plate's end, ONE name that does not
    change («Afficher le mot de passe», the live string) and `aria-pressed` as the one channel; the glyph swaps at
    once; a pointer's press hands the focus back to the field **with its caret where it was**, a press from the
    keyboard leaves the focus on the control; the reserve is the plate's own height, on the control's side in
    Arabic too. A shown password has room for 36 characters at 1440, 28 at 360, 23 at 320 (the words took the
    plate: 12 at 360). Without script the control is not drawn;
  - no placeholder: the sign-in's and the signup's fields have none in their markup; the other entrance forms are
    allauth's classes and keep the attribute — the sheet does not draw it; no required mark where every field of
    the form is required (the inputs keep `required`); a one-time code in tabular figures, left to right.
- **The primary** — the system's flat primary (no gradient, no light, no shadow: L14), the column's width, 52 px,
  label 16 / 24 at 500. **On the forms that complete a sign-in** (the login, the second factor's code: the ones that
  name the stage) **it holds the key**: at rest, the very key the loader turns — the same mask, the same 18 px box,
  the middle of the same 52 px end pad; on submit that pseudo-element turns once and dims while the stage's key
  turns, and the label does not move by a pixel. Every other entrance primary gets its key only while it waits.
- **The assurance** (the sign-in only, `templates/account/login.html`): under the action, after a hairline, the
  locked FAQ answer on data protection — its question as a heading set as a label, the answer verbatim at 15 / 24,
  the FAQ's own link after it. Read from the locked registry behind the Phase-3 gate, as the home quotes the FAQ;
  French, marked `lang="fr"`, on a page that is not French.
- **The sign-in's page extends allauth's own** (`{% extends "account/login.html" %}` from the project's template of
  the same name): the view, the form, the field names, the CSRF token, the redirect field and the passkey and code
  blocks are `block.super`; no message of allauth is restated.
- **`accounts.forms.LoginForm`** (`ACCOUNT_FORMS["login"]`) — presentation only: no placeholder,
  `inputmode="email"`, `autocapitalize="none"`, `spellcheck="false"`, `dir="ltr"`; `autocomplete` stays allauth's
  (`email`, `current-password`). It overrides no method of the sign-in (a test holds it member by member). After a
  refusal that names no field its bound field puts the summary's id first in each field's `aria-describedby`;
  neither field is marked invalid.

### Every unhappy state, drawn (`E/step2/states`, `E/step2/pages`)

| State | What the person sees — live strings only |
|---|---|
| wrong address or password | the same page: the summary (the system's error notice: the double rule, the mark, «Le formulaire contient des erreurs.» and allauth's one sentence for both causes) takes the focus; both fields described by it, no red edge; the address kept, the password empty; the stage at the still of the kept address, no arrival; the title «Erreur — Connexion» |
| a field's own error (an empty field) | the summary with a link to each field; the field's doubled garnet edge, its message with the drawn mark, under the field |
| too many failed attempts (5 in 5 minutes) | allauth says it **in the form** — the summary — and the reset link is in the password's row; the right password is refused too |
| too many requests (allauth's 429: the reset, the signup, a sign-in posted too often, a verification asked again) | `templates/429.html` on «Il varco», in the request's language: «Trop de requêtes», the product's one sentence (nothing was lost, a few minutes), the way back to the sign-in; no countdown, never which limit. A signed-in person gets the product's error page |
| address not verified | allauth sends the verification again and shows «Vérifiez votre adresse e-mail»; its session message stands **in the form's column** (it was a band across the page, above the stage); the way back |
| the second factor's code | title, sentence, «Code», the primary that holds the key (the stage's key turns on its submit), «Annuler» under it; a wrong code is the field's own error |
| reset asked | «Réinitialisation du mot de passe» and allauth's sentence — the same for every address — and the way back |
| a reset link or a confirmation link that has expired | the title, allauth's sentence with its own link; the confirmation's page also has the way back |
| a new password | two plates with the glyph control; the rules as a list inside the first field's help (they were raw HTML outside it); «Annuler» under the primary |
| account inactive · signup closed | the title, the sentence, the way back |

### Measures (lane 7, the dev server; headless Chromium 153; on the merged branch, the final tree; `E/step2/measures/`)

Every capture and every figure below was taken again after the last change to the sheet (`c2984a6`: the eyebrow's
row, the label row's line in Arabic).

- **Looked at**: `rest/` — fr, ar, it, en × 1920, 1440, 1366, 1024, 768, 390, 360, 320: 32 pages, 0 px of horizontal
  overflow, 0 console or CSP issue; `states/` (fr and ar, 1440 and 390: focus, typed, the password shown, hover, busy,
  refused, field errors; the same at device scale 2; the keyboard's stops one by one); `pages/` (every other
  entrance page in French at 1440 and in Arabic at 390, the 429, the session message at 1440, 1024, 768 and 390,
  the two signed links' pages, the re-authentication); `stills/` (reduced motion, forced colours, no script).
- **L1 / L2 / L5 / L11** (`measures.json`, four languages × five sizes): typed text 16 px in every cell; fields and
  the primary 52 px; the show / hide control 44 × 44; the reset link's target 24 px, 44 px under a finger, in the
  four languages; the password's room 330 px at 1440 (36 characters of the field's own type), 288 at 390 (31), 258 at
  360 (28), 218 at 320 (23); the action's lower edge at 360 × 640: 613 px in French, 585 in Italian and English,
  562 in Arabic; overflow 0 in the twenty cells. Contrast on the paper: title and labels 14.62 : 1, the sentence, the
  eyebrow and the assurance 6.46, links 5.69, the field's edge 3.37 (3.74 on its plate), the control's glyph 7.17,
  the primary's label and key 5.29.
- **L3**: no `placeholder` on the two fields; `autocomplete` `email` / `current-password`; the contract classes kept.
- **L4** (a refused sign-in, read in the page): the focus on `#form-errors`; title «Erreur — Connexion · Italy
  Legal Entry™»; `aria-describedby` `form-errors` on the address and `form-errors id_password_helptext` on the
  password; `aria-invalid` on neither; the address kept, the password empty; the stage `is-ways is-held`, 0
  animations.
- **L6**: after the skip link the stops are the invitation's signup link, the address, the password, «Afficher le
  mot de passe», the reset link, the action, the assurance's link, then the help line's address.
- **L8 / L14** (the POST answered 204 at the network): at rest `box-shadow: none`, `background-image: none`, the key
  7.66 × 18 px at 22.17 px from the inline end, opacity 1; under the pointer the fill one step darker; busy —
  `aria-busy`, the same box, `sig-turn` once in 320 ms, opacity 0.8, **label shift 0.0 px**, the focus kept, the
  stage engaged, one POST for two presses. French and Arabic.
- **Layout shift at CPU ×4, cache off** (`cls.json`, five loads each, fr and ar at 1440, 1024, 390, 360 — forty
  loads): 0 in thirty-seven; 0.0113 once at 1024 in Arabic (the public navigation, `NAV.main-nav`), 0.0006 once at 390
  (the letterhead's end, `DIV.site-header__end`), 0.0007 once at 360 (the stage's help line: centred beside the door,
  it takes its second line when the address is parsed) — **nothing of the form moves** (step 1: the V4 sheet, up to
  0.05). The run before the last change to the sheet had the navigation at up to 0.0198 (1440, French): these figures
  move with the machine's load. The form's box is the same with and without the stage in the document, eight cases.
- **No part of the column waits for a later one.** That earlier run named the eyebrow's key once, at 390: 3 px, for a
  score of 0.0000 — a paint had come between the key and its words, and the row was the key's height until they
  arrived. Taking the later parts away one by one (`parse_probe.py`: four languages, 1440 and 390) found that row
  and, in Arabic only, the label's row — 2 px taller once its link arrived, under a password already drawn. Both hold
  their height now (the eyebrow's row has its line's height; the link has the label's own line in every language):
  the probe reads no move in its twenty-four cases, a test holds it, and at rest the captures are the earlier ones
  pixel for pixel in French, Italian and English (24 of 24) — in Arabic the page is 2 px shorter from the password's
  label down (8 of 8, as intended).
- **axe-core 4.13** (WCAG 2.x A / AA and 2.2 AA; `axe.json`: eleven pages and states, French at 1440 and Arabic at
  390, 22 cells): 0 violation in 20 cells; in the two cells of the login's field errors, `listitem` × 2 — the
  system's field error is `<ul role="alert">`, whose role takes the list away from its items (see «For other
  families»). «Incomplete» (to judge by eye): text on the night stage and in the letterhead, none in the form.
- **Weights (gzip −9)**: `dist/accounts/entrance.css` 4 157 → **5 151 B** (the V4 form rules out, the form in);
  `dist/main.css` 43 055 B (W1-C's 42 939 + this family's token block); `dist/shell.js` 1 120 B, `dist/entrance.js`
  1 664 B (unchanged). **The login's CSS: 48 206 B of 45 694 — 2 512 B over**, as after step 1 (2 510): the form
  costs what the core components gave back. Still for the performance check and the CD (DL54-15: one raise of
  ≤ 2 KB; ≈ 0.5 KB would remain to find — the stage's paints and the key's mask, which is `loader.css`'s, written
  twice, are the candidates).

### Tests

On the final tree, `test_ile_v5_l7`, one pytest at a time and never beside a browser series of this lane. The two
long runs are on `c2984a6`, the last commit that changes what the page does; `6e66f88` after it changes two comments
(the bundle is byte for byte the same), and the source and document tests were run again on it and on these notes:

- **In Chromium** (`-m browser`, 0 skipped) — `tests/frontend/test_entrance_form_w2_b.py`,
  `tests/frontend/test_entrance_w2_b.py`, `tests/i18n/test_rtl_browser_entrance.py`, `tests/i18n/test_rtl_browser.py`,
  `tests/frontend/test_loader_w1_d.py`, `tests/frontend/test_browser_w1_c.py`, `tests/frontend/test_layout.py`:
  **119 passed** (14 min 56 s).
- **Not in a browser** — `pytest -m "not browser" apps/accounts tests/frontend tests/security tests/i18n
  tests/test_regen_design_inventory.py`: **1967 passed, 2 xfailed, 0 failed** (17 min 33 s). In it: the allauth
  flows (`apps/accounts`, with `test_login_form_w2_b.py`), the entrance's slice of `test_layout.py`, the 429 test,
  `tests/security`, the catalogues' audit and the locked texts, `test_css_bundle_is_current`,
  `test_frontend_bundle_is_current`, `test_design_docs`, the tokens, the loader's rules, `test_rtl_static`, W1-C's
  guards and its lint. The six failures step 1 reported in `test_state_chips_carry_a_register.py` (W1-P's preview
  chips) are gone with W1-C's branch.
- **New in this step**: `apps/accounts/tests/test_login_form_w2_b.py` (14: the form overrides no method of the
  sign-in, its fields and widgets, the page in the four languages, a refusal, a field's error, the limit on failed
  attempts, CSRF, an address not verified, the second factor's step, the reset's one answer for every address);
  `tests/frontend/test_429_w2_b.py` (7); `tests/frontend/test_entrance_form_w2_b.py` (22 on the sources and
  through the test client, 33 in the browser: L1, L2, L4, L5, L6, L8, L11, L14, the title's height, the
  targets, the show / hide control, the page without script, the places, the session message, forced colours); one
  fixture and one test in `tests/i18n/test_rtl_browser_entrance.py` (the form mirrors, its key does not).
- **Held against their defect**: the test of the places fails on the sheet as it was — in French on the eyebrow's
  row, in Arabic on the label's row — and passes on the corrected one (`c2984a6`); step 1's keyboard test refused the
  first draft of the label's row, the link before the password in the Tab order: the link is written after the
  control since; W1-C's guard («entrance.css draws no control») refused the sheet's first selectors on the merged
  tree (`b820837`).
- **After the last commit and these notes** — the bundles' two tests, the form's and the stage's source tests, W1-C's
  guards and lint, the tokens, `test_design_docs`, `test_rtl_static`, `test_documentation`, the inventory's check,
  `tests/security/test_confidential_material.py`: **GATE-PENDING**.
- Not run: the full suite (V5.5).

### For the merge (the steward)

- **`collectstatic` under the production storage stops on this family's raw entry — to settle at this merge, with
  the console's.** `apps/accounts/static/accounts/entrance.css` imports its two partials as step 1 wrote them,
  `@import url("../../../../static/css/v5/_door.css")` and `…/_varco.css`: the way
  `apps/portal/static/portal/console.css` imports `_loader-light.css` (W1-D) — the open item of design-v5's own
  DL54-44 (the steward's, item 4; W2-D's check, F2), read while these notes were being closed. The raw entry is
  collected beside its bundle, and `CompressedManifestStaticFilesStorage` follows the import out of `STATIC_ROOT`:
  `SuspiciousFileOperation`. Run here on this branch, with the production storage into a scratch root: it stops on
  `accounts/entrance.css` first; with the two raw entries left out (`--ignore "accounts?entrance.css" --ignore
  "portal?console.css"`) it passes, and the built `css/dist/accounts/entrance.css` and the two partials are collected
  and hashed. Nothing a person sees depends on it — the templates load the bundle; the lane, the preview and the
  tests use the plain storage — but no deployment passes that command. **Not corrected here**: both ways out are
  outside this family's hands — (a) the correction design-v5 already owes the console's entry, made for this one
  too, and for `hero.css` the day it imports `_door.css`: a build-only entry outside `static/`, or the imports
  written in the static namespace (`../css/v5/_door.css`) with a resolver for `@import` in
  `scripts/build_css.mjs`'s plugin, as it has one for `url()`; (b) the two partials moved beside their importer
  (`apps/accounts/static/accounts/_door.css`, `_varco.css`: a sibling import is one path in both trees), which ends
  the shared door plan §1.17 asks for.
- **The sync with design-v5** once it carries `v54/w1-c`: see the first section.
- **The door arrives with this family** (`static/css/v5/_door.css`, step 1). design-v5's DL54-44 item 2 keeps two
  things for the merge that brings it: `hero.css` imports it and drops its own copy (see the line above first: that
  import is of the same kind), and `v4/hero.css` — which W2-D shrank to the entrance's door — leaves `main.css`: the
  entrance stopped including `templates/components/doorway.html` in step 1, and with the home's own door that
  component and those rules have no consumer left.
- **`scripts/check_ownership.py`**, on the final tree. `w2-b design-v5` → **FAIL, 87 paths outside**: W1-C's own
  paths are in this branch until W1-C is on design-v5 (the rest: 11 inside, 9 slice, 15 generated). `w2-b v54-w1-c` —
  this family's own 27 paths, both steps — → **11 inside, 8 slice, 4 generated, 4 outside: FAIL** until the manifest
  names the four:
  - step 1's two: `templates/allauth/elements/form__entrance.html`, `static/css/v5/_varco.css`;
  - `templates/allauth/elements/fields__entrance.html` (new) — the one argument `reveal="glyph"` on the entrance's
    fields; it leaves with W1-C's M2 if the glyph becomes the system's control;
  - `static/js/src/shell.js` §3 (W2-C1's file) — the caret kept, the keyboard's press, one channel on the glyph
    control: plan §1.13's micro-interactions live in that section.
- **Slices used beyond their letter**, each small:
  - `templates/components/form_field.html` («the reset slot»): also the help as a `<div>` and the glyph control —
    both asked by W1-C's own review (M1, M2);
  - `apps/accounts/forms.py` («the LoginForm subclass»): also four lines in the project's `SignupForm` — its
    placeholders, handed to this family by W1-C's review;
  - `config/settings/base.py`: one key in the one setting.
- `templates/account/password_reset_help_text.html` of the manifest is **not created** (DL54-53 item 4).
- The bundles are committed as built here; the chunk names follow this worktree.

### Copy packet for the owner (B1 — nothing below was added to the pages)

Microcopy the form would use and that has no live string. French drafts for the owner and counsel; the translators
write the three other languages (never us, in Arabic).

1. **A Caps Lock hint** under the password, said once, politely — «Verr. Maj est activée.»
2. **A session-ended line** on the sign-in when the eight-hour session has ended and the person is sent back —
   «Votre session a expiré. Connectez-vous pour reprendre là où vous en étiez.»
3. **The words of a long wait** on the sign-in (O32; step 1's item 5): «Ouverture…» at 1 s, «C'est plus long que
   d'habitude.» at 10 s, «Réessayer».
4. **The second factor's hint** — «6 chiffres, affichés par votre application d’authentification» — and the way to a
   recovery code — «Utiliser un code de récupération» (allauth's page only says «Veuillez saisir un code
   d'authentification :»; the same field takes both codes).
5. **The way forward after too many failed attempts** — allauth's sentence stops at «Veuillez réessayer
   ultérieurement.»; a second one could name the reset: «Vous pouvez aussi réinitialiser votre mot de passe.»
6. **A line for a verification asked too often** (3 in 10 minutes: today the 429 page) — «Un nouveau message pourra
   être envoyé dans quelques minutes.»
7. **allauth's own strings, live today, for one reading** (not ours to rewrite): «Mauvais jeton d'identification»
   as the title of an expired reset link; «Courriel» as a label beside «adresse e-mail» in the sentences; straight
   apostrophes («n'avez», «l'e-mail») beside the product's typographic ones. In Arabic (B2, the Moroccan reader):
   allauth says «يلغي» («he cancels») for «Annuler» on the second factor's and the new password's pages, addresses
   the person in the singular («لديك») where the product uses the plural of respect («تحتاجون»), and labels the
   code «شفرة».
8. **The assurance under the action** (CDV O44, «yes»): the locked FAQ answer is shown as built — for the owner to
   see, not to write.

### What is left

Not done, and why:
1. **The production `collectstatic` stops on this family's raw entry** — «For the merge», first line. It is step 1's
   two imports, found only at the end of this step, in design-v5's log; it blocks a deployment, not the preview.
2. **The sync with design-v5 and W1-C's fixes** (first section): the tag did not land in this step's time, so the
   step's first instruction — wait for `v54/w1-c`, then `git merge design-v5` — is met only by the merge of W1-C's
   reviewed branch. Whoever takes the next step: look for the tag first.
3. **The second factor's code keeps allauth's widget**: its numeric keyboard (`inputmode="numeric"`) and the removal
   of its placeholder in the markup are `MFA_FORMS` — a second setting, outside this family's slice (one setting);
   the same for the reset's and the new password's placeholders (`ACCOUNT_FORMS["reset_password"]`, `[…_from_key]`:
   two more subclasses of allauth's forms). The sheet does not draw those placeholders; assistive technology still
   reads them. For the review to decide.
4. **The skip link still targets `main`**: `templates/base.html` is not this family's. The first content of `main`
   is the form's eyebrow and title (step 1's source order), so the next stop after it is in the form (L6).
5. **The login's CSS is 2 512 B over its ceiling** (see the weights).
6. **Words** — the copy packet above; and the long wait's words (step 1's item 5).
7. Step 1's items 6 (the photograph at a device scale of 2, when W2-D's derivatives land) and 7 (the promoter's
   line) stand. And **the stage's help line** still takes its place again when its second line — the address — is
   parsed: it is centred beside the door in the band, and stands on the foot of the stage from 64rem (0.0007 once in
   the last forty loads at CPU ×4; named once among the sources of the run before, at 1024 in Arabic). Two ways,
   neither taken here: anchor its first line (it moves the line on the widths where it is one line — a choice of the
   stage's look), or draw the line only once it is whole (`.varco__colophon:not(:has(+ .varco__scene))
   { visibility: hidden; }`: «its next sibling has begun»). For the review.

Not verified:
8. Chromium only, headless. No Safari, no Firefox, no real phone, no screen reader, no password manager filling
   the two fields (the attributes are the ones they read: `autocomplete`, the field names, `type`). `:has()` and
   subgrid carry the label row's place and the session message's place: where they are not understood the link
   stands under the control and the message stays a band above the stage — read in the sheet, not run.
9. The full suite was not run (V5.5). The budgets on 8782 and the before / after on the owner's preview are the
   performance check's.

For other families:
10. **W1-C / the accessibility owner — a field's error list is `<ul role="alert">`** (`form_field.html`,
   `tests/frontend/test_design_docs.py:948`, `docs/ACCESSIBILITY.md` §6): the role takes the list semantics away
   and axe reports `listitem` (serious) on every form with a field error; the summary already announces. Seen on
   the login's field errors; not changed here (a pinned contract of the system). W1-C's accessibility check,
   committed while these notes were being closed (`61cf067`: its major A2), names the same line and its fix — it
   comes with W1-C's fix pass.
11. **W1-C / W3-F2 — the show / hide control drawn as its words** (the account pages) still says its state twice
    (`aria-pressed` and the swapped words): `shell.js` keeps that for the words face only.
12. **W1-A** — `static/css/v5/base.css` still holds `:lang(ar) .entrance .form-field__help { line-height: 1.5rem; }`:
    `.entrance` left the layout in step 1 and the help line it served is now the label row's aside; the rule matches
    nothing.
13. **W2-C1** — at CPU ×4 the public navigation is still the source of the page's layout shifts (≤ 0.02).
14. **W1-A — `docs/ACCESSIBILITY.md`** (its file, not edited here): gap **G-10** (2.5.8: «Mot de passe oublié ?»,
    17 px high at 2 px from the password field) is closed on the entrance by the label's row — the link's target is
    24 px, 44 px under a finger, and never lies over a field (measured in the four languages; a test holds it): the
    gap's row, §9's sentence and the checklist's row 2.5.8 are to rewrite there. The same document's §6 still shows
    the help as `<p class="form-field__help">`: it is a `<div>` now (W1-C's M1 asks the same of the system).
15. **The e-mails allauth sends from the lane's clone sign «example.com»** (the Sites framework's default name on
    this clone; the console backend printed them, none was sent): to check on the production site's row before
    go-live — not design.

## Step 2, resumed — the sync with design-v5 (11 October 2026)

The step was cut twice by usage limits; on resuming, 50 commits were on the branch and three files (these notes, the
decision log's entry, the design system's rows) were uncommitted — they were the step's closing notes and were
committed as they stood (`w2-b step 2: the notes, …`). The tag `v54/w1-c` was on design-v5: **`git merge design-v5`**
was done before anything else (`f392589`). What the merge changed in this family's work:

1. **The show / hide control is now the system's** (W1-C's fix pass, M2 / A10: the glyph in `v5/field.css` §5, one
   name in a `visually-hidden` span, `aria-pressed` the one channel). The entrance's own face is gone: the
   `reveal="glyph"` argument of `form_field.html`, `templates/allauth/elements/fields__entrance.html` (deleted: allauth
   falls back on `fields.html`) and `entrance.css`'s glyph rules (the 44 px target, its RTL reserve, its forced-colours
   line) — the system draws all of it. Kept from this family: `shell.js` §3's caret (a pointer's press hands the focus
   back to the field with its selection; a keyboard press keeps the focus on the control — design-v5's version always
   moved the focus to the field, which this family's test refuses); and **without script the entrance does not draw
   the control** (`html.no-js .varco [data-password-toggle]`, in `entrance.css`): a button that does nothing.
   «What is left» items 3 (the glyph until the system's) and 11 (the words face) are closed by this.
2. **The field's errors** take W1-C's wrapper (`<div role="alert"><ul class="form-field__error-list">`): «What is
   left» item 10 is closed. The label row's aside (the reset slot) stays, unchanged.
3. **`tokens.css`** keeps both named blocks: §4.2 the hero (W2-D), §4.3 the door stage (this family).
4. **The decision log**: design-v5 renumbered W1-C's entries DL54-45 … 57, so this family's are **DL54-58** (the
   stage) and **DL54-59** (the form); the references inside them follow (W1-C's «entrance draws no field» is DL54-50).
   DL54-59 item 13 says the glyph is now the system's.
5. **DS 2026**: `form_field.html`'s contract loses `reveal`, gains `__error-list`; `doorway.html` is «used in: no
   page» (the home and the entrance both draw the stage themselves) — the component and `v4/hero.css` (still in
   `main.css`) wait for their removal (the steward's, DL54-44 item 2). The §2 weights are the steward's script's.
6. **Bundles** rebuilt (`npm run build`); two chunks no bundle references any more removed.

### Measures (lane 7, 8787; headless Chromium; `evidence/v54/w2-b/step2-resume/`)

The sign-in, fr and ar, at 1440 × 900 and 390 × 844: at rest, the password shown (the toggle pressed), and refused
(wrong credentials). Looked at: one title, one primary, the reset link quiet at the label row's end, the glyph in
its seat at the plate's end (left in Arabic, the password typed left to right), the refusal's summary first and
focused, the address kept and the password emptied, the stage lit as before. 0 px horizontal overflow, 0 console
errors, 0 failed requests on all twelve.

### Tests (targeted; V5.5 — not the full suite)

- `apps/accounts/tests`, `tests/security`, `tests/frontend/test_429_w2_b.py`, `test_layout.py`,
  `test_css_bundle_is_current.py`, `test_frontend_bundle_is_current.py`, `test_design_docs.py`,
  `test_components_w1_c.py` (not browser): **332 passed, 1 failed** on the first run — W1-C's
  `test_the_password_control_is_a_glyph…` reads the button's class exactly; `js-only` on it was taken off (the
  entrance's sheet hides it instead) → **78 passed** on the re-run of the files concerned.
- `tests/frontend/test_entrance_form_w2_b.py`, `apps/accounts/tests/test_login_form_w2_b.py`,
  `tests/frontend/test_429_w2_b.py` (browser included): **76 passed**.
- `tests/i18n/test_rtl_browser.py`, `test_rtl_browser_entrance.py`, `tests/frontend/test_loader_w1_d.py`,
  `test_layout.py`, `test_components_w1_c.py` (browser included): **121 passed**. No crashed run.

### For the merge (updates the step's list)

- `scripts/check_ownership.py w2-b design-v5` → **11 inside, 8 slice, 16 generated, 3 outside: FAIL** until the
  manifest names the three: `static/css/v5/_varco.css` (step 1), `templates/allauth/elements/form__entrance.html`
  (step 1), `static/js/src/shell.js` §3 (the kept caret and the keyboard's press). `fields__entrance.html` is gone.
- Still open: the production `collectstatic` and the raw entry's `@import` (first item of the step's list; design-v5
  has not settled the console's either).
- **For W1-C**: the system's show / hide control is drawn without script too (it does nothing then); the entrance
  hides it under `html.no-js`; the system could do the same in `v5/field.css`.

---

## Review fixes (11 October 2026)

The family's fix pass (label w2-b-fix), on the senior review (`REVIEW.md`, SHIP_AFTER_FIXES: no P0, M1–M4, m1–m5) and the
accessibility + performance check (`A11Y_PERF.md`, SHIP_AFTER_FIXES: A1, P1, P2, C1 major; A2, A3, P3, F1 minor) —
implement, review once, fix, ship (V5.5). Same lane: dev server 8787 on `ile_v5_l7` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`), the compressed twin on the same port for the performance A/B, pytest on
`test_ile_v5_l7`; one headless Chromium and one pytest at a time, the benchmark lock checked before every browser series
and the build (never present), no run ended on «Target crashed». Tools under `C:/tmp/ile_v5_council/.work/w2-b/w2-b-fix/`,
evidence under `C:/tmp/ile_v5_council/evidence/v54/w2-b/fix/` (F/ below). Branch `v54-w2-b` from `c3d870b`; design-v5 had
not moved when the pass began (`3c288d6`) and is at `1c001e6` at its end (W3-A merged): the merge meets it.

### Finding → change → evidence

| # | Finding | Change | Evidence |
|---|---|---|---|
| M1 · F1 | The stage's photograph soft at a device scale of 2 (V4's single 400 px file over 550–724 device px) | `templates/allauth/layouts/entrance.html`: the home's `<picture class="door-stage__photo">` — the `static/brand/v5` AVIF (400–1200) and WebP (400–960) sources, the same registration — with a `sizes` that is the photo box (320 / 368 of `--door-w`), each `clamp()` of the sheet cut at its bounds into plain lengths (nine lines); the preload is the AVIF source with the same sizes, character for character. `_door.css` draws the `<picture>` as it drew the span (the same box, radius, clip, shadow; the `img` at .5 and saturate .8). | F/smoke: 1440 @1 → `400.avif`; 1440 @2 → `576.avif` (box 275.5 px: 551 device px covered); 1920 @2 → `800.avif` (box 361.7); 1366 @2 → `576.avif`; 390 @3 → `400.avif`; **one photograph fetched in each**; `zoom-photo-dpr2-after-1to1.png` against the review's `dpr/zoom-photo-dpr2.png` (the inscription, the capitals and the statues are drawn, not smeared). Twin: see «Performance» |
| M2 | A shown password outside the sign-in kept the browser's spelling and the keyboard's corrections | `static/js/src/shell.js` §3: when a `[data-password-toggle]` is wired, its field gets `spellcheck = false`, `autocapitalize="none"`, `autocorrect="off"` — every revealable password of the site at once | F/smoke `secrets signup`: `id_password1`, `id_password2` → `false · none · off`; the browser test reads the three on the sign-in, the sign-up's two and the new password's two, before and after the press |
| M3 · A1 | The sign-up's «Nom et prénom» had no input purpose (WCAG 1.3.5) | `accounts.forms.SignupForm.__init__`: `autocomplete="name"` | F/smoke: `id_full_name` → `name`; test |
| M4 · C1 | The production `collectstatic` stops on the raw entry | **Not changed here** — the steward's one correction for this entry and the console's (see «For the merge») | the twin's collect without the ignore: SuspiciousFileOperation, as before (F/perf `collect-c1-probe.log`) |
| P1 | The login's CSS over its §2.6 ceiling (47 628 B on the wire) | The key's mask written once: `--key-mask` in this family's block of `v5/tokens.css`, read by `v5/loader.css`'s busy key and by the entrance's primary at rest (`loader.css` loses its declaration; W1-D's rule test reads the token) | gzip −9 of the bundles: `main.css` 42 550 → 42 542 B, `accounts/entrance.css` 5 003 → 4 861 B (≈ −220 B for the mask, the fixes below the rest): **−150 B**; on the wire 47 628 → **47 477 B** («Performance») |
| P2 | On French phones the LCP element was the stage's 3 % grain | The grain (`.varco__stage::before`) only from 64rem: the band keeps the arch only (§1.13) | dev server: at 390 @3 and 412 the pseudo-element is `none` and `grain.svg` is not fetched; the French phone LCP is the assurance's paragraph, the Arabic phone's the door's photograph. Twin: see «Performance» |
| P3 | The Tab into the password restyled the whole stage (inherited switches on the stage's root) | `entrance.css` §4: each of `_door.css`'s switches set on the layer it lights — `.is-frame .door-stage__frame { --door-frame: 1 }`, `.is-held .door-stage__step { --door-steps: 1 }` (leaves, or nearly: the frame's four parts) — never on the stage's root; `_door.css` keeps drawing the lights from them (a first form wrote the steps' opacity from `_door.css`'s `--step-lit` / `--step-n`: the design documents' token guard refuses an app sheet that reads a partial's internals) | the check's own diagnostic re-run (F/`s9_tabstyle.json`, CPU ×4, Blink's invalidation tracking): **136 elements for the Tab (fr and ar), 127 with the stage's classes held still** — 206 before; the stage's share 10 elements (the frame and its four parts, the steps), 82 before; style 34.8 ms against 36.0 held still (the first form, the opacity written on the layers: 131 — `s9_tabstyle-first-form.json`) |
| m1 | From 64rem a band of light wall between the niche and the night footer | `.page-entrance .site-footer { margin-block-start: 0 }` from 64rem, as the home's last chapter meets the footer | F/smoke `full-*-1440.png`: the stage ends where the footer begins (932 = 932 fr; 901 = 901 it, en, ar); test at 1440 and 1024 |
| m2 | The arrival read as four sparks | `.is-arriving .varco__way-lit`: `varco-draw` + `varco-glint` on the light's own clock — each way lit behind its light, given back as it arrives | F/smoke `arrival-fr-1440-*.png` (Persona's way lit at 0.35 s, three at 0.9 s, the fourth from 1.5 s; nothing at 2.7 s, 0 animations). Twin: the arrival window, see «Performance» |
| m3 | The assurance's French answer on the it, en and ar sign-in | `templates/account/login.html`: the question and the answer only where the registry holds the page's language; the FAQ's own link in every language | F/smoke `login it/en/ar`: the link alone («Leggi la Privacy Policy», «Read the Privacy Policy», «قراءة Privacy Policy»); French unchanged |
| m4 · A3 | allauth's placeholders in the reset, new-password and code fields; the code on the text keyboard | `accounts.forms.ResetPasswordForm`, `ResetPasswordKeyForm` (`ACCOUNT_FORMS`), `AuthenticateForm` (**`MFA_FORMS`, a second setting — for the steward's agreement**): no placeholder, `inputmode="numeric"` on the code | tests: each overrides its constructor only; the pages write no placeholder; the code says `numeric` and `one-time-code` |
| m5 | The address said `email` | `LOGIN_PRESENTATION`: `autocomplete="username"` (supersedes L3's «email»: DL54-59 item 19) | F/smoke: `username` in the four languages; test |
| A2 | Four small targets under SP-8's floors | the help line's address: the 44 px band at every pointer; the assurance's link: the reset link's device; the invitation's link: the 44 px band under a finger; a link under the action: 44 px wide under a finger, its words at the column's start | F/smoke: help 44 px at a fine pointer (fr, it, en, ar), assurance 28 / 48, invitation 44 under a finger; tests (the targets at 1440 and 390; «يلغي» on the new password's page in Arabic) |

### Commits

| Commit | What |
|---|---|
| `533d1cf` | the forms: the sign-up's name `name` (M3, A1), the address `username` (m5), allauth's reset, new-password and second-factor forms with their presentation only (m4, A3; `MFA_FORMS`) |
| `011f7f1` | the page: the photograph's `<picture>` and its preload (M1, F1), a shown password never spelled nor corrected (M2), the assurance by language (m3); the JS bundles rebuilt from a clean `dist` |
| `f2f52d2` | the sheet: the grain on the niche only (P2), one key token (P1), the switches on the layers (P3), the niche meets the footer (m1), the arrival's lit ways (m2), the small targets (A2); the tests; the CSS bundles; DS 2026's entrance prose |
| this one | DL54-59's «Fix pass» (items 17–27) and these notes |

### Decisions met on the way

DL54-59, «Fix pass», items 17–27 (appended to the family's own entry: design-v5 numbers past DL54-59 now). Three of them
change something the plan or a test had written down: L3's `email` becomes `username` (item 19); the assurance quotes the
locked answer only in the language the registry holds (item 20); `MFA_FORMS` is a second setting in `base.py` (item 21).

### Performance (the twin, A/B)

The check's protocol P (its own scripts, copied read-only) on lane 7's compressed twin — 8787, DEBUG off,
`CompressedManifestStaticFilesStorage`, its own `STATIC_ROOT`, the two raw entries left out of `collectstatic` (C1) — the
fix (the worktree) against the code before the fix pass (`c3d870b`, a plain export): profile A (150 ms RTT, 1.6 / 0.75
Mbps), CPU ×4, cold loads, fresh profile, a click on the address at 5 s, then a Tab. **n = 10 per cell and arm**: a first
round in blocks of 3 + 2 runs, a second in five one-run blocks alternating the arms (the fix re-collected from the final
sheet). The machine was 31–45 % busy, the fix's blocks the busier (medians 40–45 % against 31–36 %): a bias against the
fix. Differences tested by permutation within the cell (F/perf/`summary-AB.json`, `P/runs.jsonl`, one trace per cell and
arm kept).

| Cell (median of 10) | LCP before → fix (ms) | LCP element before → fix | FCP | First-render task | CLS (max) |
|---|---|---|---|---|---|
| fr · 1440 | 1 462 → 1 452 (−10, p 0.45) | the photograph → the photograph, 10 / 10 | 1 206 → 1 194 | 85.2 → 97.6 (+12.4, p 0.10) | 0.0234 → 0.0234 |
| fr · 412 @ 1.75 | 1 600 → 1 488 (−112, p 0.17) | **the grain → the assurance's paragraph**, 10 / 10 | 1 202 → 1 170 (−32, p 0.08) | 48.4 → 49.5 | 0 → 0 |
| ar · 1440 | 1 642 → 1 672 (+30, p 0.61) | the photograph → the photograph, 10 / 10 | 1 376 → 1 366 (−10, p 0.03) | 94.8 → 95.2 | 0.0183 → 0.0183 |
| ar · 412 @ 1.75 | 1 694 → 1 696 (+2, p 0.74) | the assurance's paragraph → **the door's photograph**, 10 / 10 | 1 374 → 1 352 (−22, p 0.04) | 52.4 → 57.9 | 0 → 0 |

- **LCP** ≤ 2.5 s in every cell; the LCP element is the door or text in every load, never the grain (L9). No timing is
  worse with significance; FCP is earlier in Arabic (p ≤ 0.04). The first-render task at fr · 1440 (+12.4 ms, p 0.10)
  is inside §2.6's tolerance (+30 ms), on the busier blocks.
- **CLS**: every load-time shift in both arms is the public navigation's (`nav.main-nav.is-enhanced`, W2-C1's: 0.0088
  to 0.0234 a load); none is the entrance's — the `<picture>` has its box before its file. ≤ 0.05 (a flagship) in every
  load.
- **The arrival** (20 desktop loads per arm): 2.43 s, **0 tasks over 50 ms** in its window in either arm (the longest
  39.9 ms, against 24.6), the main thread 79–86 ms per second against 60–64 (16 animations instead of 8, and the busier
  blocks); nothing running after it.
- **compositeFailed**: 8 per desktop load and 4 per phone load in both arms, identical — the navigation panels'
  `display` transitions (W2-C1's) and the field's border-colour transitions (W1-C's, as the check found); none of the
  stage's: the arrival's lit ways composite.
- **Bytes before `load`** (fr, on the wire): CSS **47 628 → 47 477 B** (`main.css` 42 605, `entrance.css` 4 872);
  images at 1440 158 783 → 149 707 B (the 400 px AVIF, 33 418 B, for V4's 400 px WebP, 42 494 B); on phones 49 687 B in
  4 requests → 40 365 B in 3 (no grain). At 1440 × 900 @ 2 the photograph is the 576 px AVIF (47 115 B), at 1920 @ 2 the
  800 px (61 586 B): the price of a sharp door on a dense screen, one file each.

### Tests

Targeted (V5.5: not the full suite), `test_ile_v5_l7`, one pytest at a time and never beside another of this lane's:

- **Not in a browser** — the family's three files, W1-D's rule test, the 429, the bundles' two tests, the tokens:
  **665 passed**. Then `apps/accounts`, `tests/security`, `test_design_docs.py`, `test_components_w1_c.py`,
  `test_layout.py`, `tests/i18n`, `test_check_ownership.py`: **597 passed, 1 failed** — the design documents' token guard
  (`test_conforming_app_stylesheets_use_only_design_tokens`) refused the first form of P3, which read `_door.css`'s
  `--step-lit` / `--step-n` from the app sheet; P3 now sets the door's own switches on the layers, and the guard, the
  stage's, the form's, the bundles', the loader's and W1-C's source tests: **129 passed**. The forms' file after its four
  lines were wrapped for `ruff check`: **18 passed**.
- **In Chromium** (0 skipped) — `test_entrance_w2_b.py`, `test_entrance_form_w2_b.py`, `test_rtl_browser_entrance.py`
  (whole files): **104 passed, 1 failed** — the new sizes test read the chosen file's width from `naturalWidth`, which an
  image from a `srcset` reports density-corrected (the box's); it reads the candidate's width from its name now: **1
  passed**. `test_loader_w1_d.py` and `test_browser_w1_c.py`: **38 passed**. `tests/i18n/test_rtl_browser.py`: **23
  passed**. No run crashed.
- `ruff check .`: nothing from this pass (the six findings left are other families' files: `apps/accounts/apps.py`'s
  import order, `scripts/gen_loader_light.py`).
- **New or changed in this pass**: `apps/accounts/tests/test_login_form_w2_b.py` — `username`, the code's keyboard and no
  placeholder, the reset's form, the sign-up's name, the three presentation-only subclasses (parametrised);
  `tests/frontend/test_entrance_w2_b.py` — the `<picture>` and its preload character for character, the sizes against
  the box at twelve windows and the file chosen at a device scale of 2 with one fetch, the switches on the layers, the
  arrival's lit ways, the grain on the niche only (sources and the band), the niche meeting the footer;
  `tests/frontend/test_entrance_form_w2_b.py` — the one key token, the assurance by language, no placeholder on the reset,
  the small targets at a fine pointer and under a finger, the three attributes on every revealable password (the
  sign-in, the sign-up, the new password) and «Annuler» under a finger in Arabic; `tests/i18n/test_rtl_browser_entrance.py`
  — the Arabic assurance is the link alone; W1-D's `test_loader_rules.py` — the busy key reads the token.

### For the merge (updates the step's list)

- **`scripts/check_ownership.py w2-b`** → **13 inside, 8 slice, 17 generated, 5 outside: FAIL** until the manifest names the five:
  `static/css/v5/_varco.css`, `templates/allauth/elements/form__entrance.html`, `static/js/src/shell.js` §3 (the steps'),
  and, new in this pass, `static/css/v5/loader.css` and `tests/frontend/test_loader_rules.py` (P1, W1-D's files).
- **Paths outside the slice, new in this pass:** `static/css/v5/loader.css` (one declaration removed: the busy key reads
  the token) and `tests/frontend/test_loader_rules.py` (one assertion reads the token) — W1-D's two files, for P1. Still
  from the steps: `static/css/v5/_varco.css`, `templates/allauth/elements/form__entrance.html`, `static/js/src/shell.js`
  §3 (now also M2).
- **Slices used beyond their letter:** `config/settings/base.py` — `ACCOUNT_FORMS` gains two keys, and **`MFA_FORMS`
  is a second setting**, written for the steward's agreement (declining it is one line: the code keeps its placeholder,
  which the sheet does not draw); `apps/accounts/forms.py` — beyond the LoginForm subclass, the sign-up's name and three
  presentation-only subclasses; `static/css/v5/tokens.css` — the door's block gains `--key-mask`.
- **The production `collectstatic` (REVIEW M4, the check's C1) is still the deployment's blocker**, unchanged here: the
  raw entry `apps/accounts/static/accounts/entrance.css` imports `../../../../static/css/v5/_door.css`, `_varco.css`
  and draws `url("../../../../static/img/grain.svg")`, paths of the source tree that leave `STATIC_ROOT` once the entry is
  collected. The one correction for this entry and the console's: the imports and the grain's `url()` written in the
  static namespace (`../css/v5/_door.css`, `../img/grain.svg`), and in `scripts/build_css.mjs` an `onResolve` for the
  `import-rule` kind that finds the static path in `static/` or an app's `static/` (the plugin's `url-token` branch
  already resolves `url()` by static path) — or the raw entries built from outside `static/`. Then `collectstatic` under
  `CompressedManifestStaticFilesStorage` passes without `--ignore`.
- **The login's CSS ceiling:** 47 477 B on the wire against the Wave-1 ceiling of 45 694 B — 1 783 B over (1 934 before
  this pass): under §2.6 item 5's one raise of ≤ 2 KB, which the merge step records in DL54 on these measurements and the
  check's (LCP and the first-render task against W1-0's set are the check's: 220–320 ms earlier, 46–85 ms against
  384–485). Nothing else to take out without taking out the stage.
- The JS bundles were rebuilt from a clean `dist`: `chunks/chunk-HQRD43CN.js`, which design-v5's own build left and no
  bundle referenced, is gone; the steward rebuilds from clean after the merge anyway.
- DS 2026 §2's weights: `scripts/regen_design_inventory.py` reads two stale figures on this branch — `v5/tokens.css`
  (58.6 → 61.8 KB: the door block's key, and what the earlier merges left) and `v5/loader.css` (11.7 → 11.5 KB). Not
  written here: the table is regenerated after the merge, on design-v5's tree.
- design-v5 moved during this pass (W3-A, `1c001e6`): `DECISION_LOG_V54.md` (this family's two entries are numbered
  again), `tokens.css` (keep the blocks), DS 2026 and the bundles meet there.

### What is left

- The production `collectstatic` (above) — the steward's.
- `MFA_FORMS` — the steward's agreement.
- The re-authentication's two forms (`ACCOUNT_FORMS["reauthenticate"]`, `MFA_FORMS["reauthenticate"]`) still write
  allauth's placeholder, which the sheet does not draw — the same one-line subclass, not asked by the review.
- Not verified: Safari, Firefox, a real phone, a screen reader, a password manager filling `username`; a vendor's
  spelling service (headless Chromium has none: M2 was read from the attributes, as the review read the defect).

---

## Merge step — the steward's note on numbering (11 October 2026; label w2-b-merge)

W3-A's fifteen entries and the record of their merge reached design-v5 first as DL54-58 … DL54-73, so at the family's
merge its two entries became **DL54-74** (the stage) and **DL54-75** (the form) — add 16 —, content unchanged but for
their cross-references and their numbering sentences (the pre-merge sync, `041e056`). The steward's own record of the
merge is **DL54-76**.

How to read the numbers written before the merge:
- **This file.** The stage's entry is «DL54-39» in step 1 (with its items 8 and 13), «DL54-52» in step 2 and «DL54-58»
  in the resumed step: read **DL54-74**. The form's entry is «DL54-53» in step 2 (items 2 and 4) and «DL54-59» from the
  resumed step on (items 13 and 19, the fix pass's 17–27): read **DL54-75**. Not the family's: «W1-C's DL54-39 …
  DL54-51» in step 2 (W1-C's entries as the branch numbered them; DL54-45 … DL54-57 on design-v5); the «DL54-44» of
  `b820837` and `6e66f88` in step 2's commit table (W1-C's guard as the branch then numbered it: DL54-50); every other
  «DL54-44» — design-v5's own, the steward's record of the w2-d merge (its items 2 and 4).
- **`REVIEW.md`** and **`A11Y_PERF.md`**: «DL54-59 item 16» (the raw entry and the production storage) is **DL54-75
  item 16**; every «DL54-44» is design-v5's, unchanged.
- The code and DS 2026 cite none of the moved numbers (DL54-05 … DL54-15 and DL54-37 only): nothing else follows.

What shipped, the tag and what is left: `SHIPPED.md`, beside this file (on design-v5).
