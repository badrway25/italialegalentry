# W2-B — the login «Il varco» and the entrance pages · accessibility + performance check (one pass, V5.5)

Italy Legal Entry™ · design V5 · V5.4 plan §1.13, §1.9 (the engage), §2.6, §3.1 items 8–11, §3.4 item 2 · V5.5 delivery
mode · label **w2-b-a11y-perf** · 11 October 2026, 10:10–11:40 · branch `v54-w2-b` at `9772c53` (the code is `61c4771`'s;
`d5a9e65`, the senior review, landed during this check and changes no code) against its merge base, design-v5 `3c288d6` ·
lane 7, `127.0.0.1:8787` on `ile_v5_l7` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`): the dev server
for accessibility, the lane's compressed twin (the 8782 shape) for performance. I built nothing and changed nothing in the
family's code; this file is the only thing I wrote in the worktree. One pass: accessibility on the real pages in French and
in Arabic, performance against the family's own merge base and against W1-0's manifest.

## Verdict — SHIP_AFTER_FIXES

**No P0.** The entrance is accessible where it was measured: axe-core finds nothing on 32 page × state × language cells;
244 keyboard stops on the entrance's own parts, every one `:focus-visible`, wholly in view and uncovered, the ring at
3.70 : 1 or more; 180 text boxes read on pixels, none under 4.5 : 1, the night stage's small text at 9.44 : 1 or more;
reduced motion is a true still through every gesture, the engage included; forced colours keep fields, ring, key and
routes in both themes; nothing overflows at 320 px or at 400 %; text spacing breaks nothing; the 429 is the same page,
in the request's language. Performance holds against W1-0's V4 set in every cell — LCP 220–320 ms earlier, the
first-render task 46–85 ms where V4's was 384–485 — and the stage's life is clean: the arrival holds no task over 50 ms,
every one of its animations composites, the engage costs nothing over the merge base's busy key, and after it three idle
seconds hold no style, layout, paint, frame or timer. CLS ≤ 0.023, all of it the navigation's.

Four things to fix or record before shipping — two of them the senior review's own (M3, M4), confirmed here:

- **A1 (= REVIEW M3)** — the sign-up's «Nom et prénom» has no `autocomplete="name"`: a WCAG 2.2 AA failure (1.3.5) on a
  page this family draws, one line in the form class it already edits;
- **P1** — the login's CSS is **47 628 B gzip on the wire against its §2.6 ceiling of 45 694 B** (+1 934 B; +4 119 B over
  the merge base): take the second copy of the key mask out (≈ 220 B), then the merge step records the ceiling (≤ 2 KB,
  §2.6 item 5) on this check's measurements, as DL54-44 did for the home;
- **P2** — on French phones the LCP element is **the stage's 3 % grain** (9 loads of 9 at 412 px), which acceptance L9
  names as what LCP must not be (M7): draw the grain as a mask, or not on the band;
- **C1 (= REVIEW M4)** — the production `collectstatic` stops on this family's raw entry (the steward's shared fix).

Four minors follow (targets under SP-8's floors, the visually hidden allauth placeholders, a heavier style pass on the Tab
into the password, and a guard for the fix pass).

## Findings

| # | Severity | Finding (measured) | Fix |
|---|---|---|---|
| A1 | major | **The sign-up's name field has no input purpose** (WCAG 2.2 AA, 1.3.5): `<input type="text" name="full_name" maxlength="160" required id="id_full_name">` — the e-mail says `email`, both passwords `new-password`, the name nothing. V4's (W1-C's check listed it under «Others»), but the sign-up is now this family's page and `accounts.forms.SignupForm.__init__` is in its slice. The same finding as REVIEW M3 | `self.fields["full_name"].widget.attrs["autocomplete"] = "name"` in `SignupForm.__init__`, beside the placeholder removal; one assertion in `apps/accounts/tests/test_login_form_w2_b.py` |
| P1 | major | **The login's CSS is over its §2.6 ceiling.** On the wire (WhiteNoise gzip, hashed URLs, the twin): `main.css` 42 613 + `accounts/entrance.css` 5 015 = **47 628 B** against the Wave-1 ceiling **45 694 B** (DL54-44: «login 45 694 B … nothing is lowered while Wave 1 is open») — **+1 934 B**; against the merge base 43 509 B, +4 119 B (if Wave 1 counts as closed, §2.6 item 3 makes 43 509 B the ceiling). The entrance sheet's 5.0 KB gzip is the door as drawn (`_door.css`, 1.19 KB alone), the stage's paints (`_varco.css`, 0.73 KB) and the places, states, passes and form (3.54 KB); `main.css` +86 B (the door's token block). Effect, n = 9 per cell and arm: FCP +28 to +44 ms and LCP +68 to +124 ms against the merge base (p ≤ 0.007), the first-render task unchanged (−8 to −0.3 ms); against W1-0, LCP 220–320 ms earlier and the first-render task a fifth of V4's or less — §2.6 item 5's two conditions met. The implementer's 48 206 B (2 512 B over) was weighed locally; the figure here is what the twin serves | (1) The key on the primary repeats `loader.css`'s mask as a second data URI (`entrance.css` §5.3, `--key-mask`): one token in `v5/tokens.css` (the steward's block), read by both — ≈ 220 B gzip off the sheet. (2) The merge step records the login's page-type ceiling in DL54 on these measurements — the one ≤ 2 KB raise of §2.6 item 5, which covers the rest (≈ 1.7 KB) — as DL54-44 did for the home. Nothing else to trim without trimming the stage (the session-message block is ≈ 207 B and needed) |
| P2 | major | **On French phones the LCP element is the stage's grain** (`.varco__stage::before { background-image: url(grain.svg) }`, 3 % multiply): `div.varco__stage …` with `/static/img/grain.….svg` as the LCP entry in **9 of 9 loads at 412 × 823**, 32 303 px² against the assurance paragraph's 31 820 px², painted ~64 ms after it in the load inspected (grain.svg is fetched once the sheet is applied). Arabic: the assurance paragraph (9 of 9). At 1440 the grain is no candidate (a 246 B file over a large area: Chrome's low-entropy rule, most likely) and the LCP is the door's photograph (18 of 18). V4 and the merge base: text. Acceptance L9: «LCP element = the door, not the grain (M7)» — the very regression M7 recorded | Take the grain out of LCP candidacy: draw it as a mask over a flat layer (a mask image is never an LCP candidate) — or, if a 3 % grain on a 120 px band is not wanted, `content: none` for `.varco__stage::before` below 64rem. The French phone LCP then becomes the assurance paragraph (~60 ms earlier); re-measure |
| C1 | major — shared (the steward's) | **The production `collectstatic` stops on this family's raw entry:** with `CompressedManifestStaticFilesStorage` into a scratch root, `SuspiciousFileOperation: The joined path (…\static\css\v5\_door.css) is located outside of the base path` — `apps/accounts/static/accounts/entrance.css` imports `../../../../static/css/v5/_door.css` (and `_varco.css`). With the two raw entries left out (`--ignore "accounts?entrance.css" --ignore "portal?console.css"`) it passes and the built bundle is collected and hashed. The same defect as design-v5's console entry (DL54-44 item 4): no 8782 window and no deployment until it is fixed; the preview is unaffected. The same finding as REVIEW M4 and the implementer's (DL54-59 item 16) | The steward's one correction for both entries — a build-only entry outside `static/`, or static-namespace imports resolved in `scripts/build_css.mjs` — and a test that runs `collectstatic` under the production storage into a temporary root |
| A2 | minor | **Four small targets under SP-8's floors** (24 px everywhere, 44 px under a coarse pointer; effective hit boxes; WCAG 2.5.8 itself holds for all four by its inline and spacing exceptions): the assurance's «Lire la Privacy Policy» — a link alone in its paragraph — **140 × 20 px** at a fine pointer (fr), 21–24 px under a finger; the invitation's inline link («enregistrer», «vous connecter», «التسجيل») 22 px fine, 23–27 px under a finger; the help line's address **18 px** at a fine pointer (fr; 22 ar) — plan §1.13 asks «the help link, with a 44 px target», built for coarse pointers only; the second factor's «Annuler» in Arabic («يلغي», allauth's word) **28 px wide** under a finger | `.varco__assurance-more a`: the aside link's device (`::after`, `inset: -2px 0`; under `(pointer: coarse)` grown into the air above it); the invitation's link: the help line's 44 px band under `(pointer: coarse)`; the help line's band at every pointer (24 px fine) or the `(pointer: coarse)` condition dropped; `.varco .form__actions .btn--link { min-inline-size: var(--hit-primary); }` under a coarse pointer |
| A3 | minor | **allauth's placeholders stay in the markup on the reset form («Adresse e-mail») and the code field («Code»)**: the sheet makes them transparent, but they reach assistive technology — the code field says «Code» twice. The same as REVIEW m4 and the implementer's «what is left» 3 | `ACCOUNT_FORMS["reset_password"]` / `["reset_password_from_key"]` without placeholders; `MFA_FORMS["authenticate"]` with `inputmode="numeric"` — a second setting, the steward's nod |
| P3 | minor | **The Tab from the address into the password restyles the whole stage.** Desktop, CPU × 4: the Tab's Event Timing is 48–88 ms (merge base 24–48), and in 5 of 18 loads one task of 54–68 ms, 47–60 of them style — a task over 50 ms the base never shows (0 of 18). Blink's invalidation tracking: **206 elements recalculated in the Tab, 128 with the stage's classes held still**; the extra pass is the stage's whole subtree (82 elements against 4), because its state is an inherited custom property on the stage's root (`.varco__stage.is-frame { --door-frame: 1 }`, `.is-held { --door-steps: 1 }`), which every descendant inherits. The click into the address costs the same way (48–88 ms against 32–72). Inside the 200 ms INP budget | Write the lights where they are drawn — `.varco__stage.is-frame .door-stage__frame { opacity: 1 }`, `.varco__stage.is-held .door-stage__step { opacity: var(--step-lit) }` — keeping `--door-frame` / `--door-steps` as `_door.css`'s API for consumers that set them above the stage; re-read the Tab (expected ≈ 130 elements) |
| F1 | minor — for the fix pass | **REVIEW M1's `<picture>` changes the LCP image.** The photograph is the desktop LCP (18 of 18) and the page preloads `doorway-arch-400.webp` with `fetchpriority="high"` (`entrance.html:47`). If the `<picture>` lands and the preload stays as it is, a phone or a DPR-2 screen fetches the 400 px file **and** the chosen source, both competing with the CSS on a slow link. Likewise REVIEW m2 (the arrival lighting each route) adds animations to a window that is clean today, and REVIEW m3 (no assurance where it is not translated) would make the grain the phone LCP in Arabic too | With M1: the preload takes `imagesrcset` / `imagesizes` matching the `<picture>` (or goes, the `<img>` keeping `fetchpriority`), so one file is fetched; re-measure LCP and CLS on the twin. With m2: transform and opacity only, once, and the arrival window re-read for tasks over 50 ms and `compositeFailed`. Fix P2 before m3 |

## Accessibility — what was run and what it read

Dev shape, lane 7, headless Chromium (Playwright 1.63, `HeadlessChrome/153`), this role's own persistent profiles, one
browser at a time. Pages behind a sign-in: the second factor's page, reached through a session minted on `ile_v5_l7` for the
implementer's throwaway account (unusable password) with allauth's own `perform_login` — no password used, typed or stored —
re-minted once when allauth's 15-minute pending sign-in expired, and revoked at the end (4 session rows deleted).

| Check | Cells | Result |
|---|---|---|
| Names, roles, outline (Chromium's tree through CDP); axe-core 4.13.0, WCAG 2.0–2.2 A / AA + best practice | 32: the login at rest, with field errors and refused × fr, ar × 1440 × 900, 390 × 844; the login in it, en; sign-up, reset, reset sent, verification sent, inactive account, bad confirmation link, bad reset key, the second factor's code, the 429 — fr at 1440, ar at 390 | **0 violations in 32 cells.** 0 control without a name; 0 broken `aria-describedby` / `-labelledby` / `-controls` / `for`; 0 focusable inside `aria-hidden`; 0 duplicate id; one `h1` a page. The door and the floor `aria-hidden`, the help line exposed. Refused: the summary (`role="alert"`, `tabindex="-1"`) takes the focus, both fields described by it («Le formulaire contient des erreurs. L’adresse e-mail ou le mot de passe sont incorrects.»), neither marked invalid, the title «Erreur — Connexion». Arabic: the French assurance carries `lang="fr"`; the Latin runs left unmarked are the chrome's and the footer's, an e-mail address and the page name «Privacy Policy». axe's «incomplete» (colour on the header and the night stage) was read on pixels instead |
| Keyboard, real Tab and Shift+Tab | 20 walks: the login fr, ar at 1440 × 900, 1024 × 768, 390 × 844, 360 × 640; refused fr 1440, ar 390; sign-up, reset, verification sent, the code, the 429 at fr 1440 and ar 390 | 628 stops, **244 on the entrance's own parts: every one `:focus-visible`, wholly in view, nothing over it** (the password's eye sits inside its own plate, by design). The ring found on pixels around every stop, on all four sides (one link at the viewport's lower edge: its bottom side outside the capture): `#1d8a93` on paper 3.70 : 1, on the eye's white seat 4.11, `#7fd1d8` on night 9.83–10.44. Skip link → Enter → Tab lands on the form's first stop (L6) on every page and in both languages — the invitation's link on the sign-in and the sign-up, the field on the reset and the code, the way back on a page that is not a form; on the sign-in the order then runs: the address, the password, its eye, the reset link, the action, the assurance's link, the help address. From the keyboard the stage answers at 0 ms (`is-ways`, `is-frame`; the band answers with its frame) |
| Contrast on pixels (DPR 2, the p5 glyph method, first line of each box, transitions frozen) | 180 boxes on 14 cells: the login at rest, typed, refused and with field errors (fr, ar; 1440, 390), verification sent, sign-up, the code, the 429 | **0 under 4.5 : 1.** Weakest: the primary's label 5.29 (hover 6.32); links 5.67–5.69 (hover 7.67); eyebrow, invitation and assurance 5.98–6.46; labels and title 14.62; typed text 16.23; the refusal 9.36 / 14.80; a field's error 9.26; on night, the help line and its address 9.44–10.4. No rule of the system holds entrance text to 7 : 1 (the hero's CL-6 and the state words do); the night stage's small text is above 7 : 1 anyway, and on paper the text under 16 px is 5.29–6.46 (AA). Non-text: a field's edge 3.37 against the page, 3.74 against its plate; the error edge 7.55; the eye 6.32; the primary's fill 4.77 against the page |
| Reduced motion (Playwright's emulated media) | fr, ar 1440; fr 390: load, then five pointer gestures — the address, a valid address, the password, a typed password, the submit (POST answered 204) — each sampled every 50 ms for 900 ms | **A true still**: 0 running animations through every gesture; two captures 150 ms apart identical (0 px); every still equal to the motion's end state (0 px). No arrival. The engage: `is-engaged` and `aria-busy`, nothing turns; at 10 s the form is given back. With motion the same gestures play the ways' pass (480 + 120 ms), the frame's rise (480 ms) and the two key turns (480 / 320 ms) — finite, transform and opacity |
| Forced colours, light and dark | fr 1440, ar 390 | Fields keep a 1 px `CanvasText` edge, the ring is 2 px `Highlight`, the primary's key is `ButtonText` on `ButtonFace` (21 : 1, both themes), the routes are `CanvasText` hairlines, the lights and the frame are not drawn, the door stays an image with `CanvasText` lines and `Canvas`-edged steps. Captures looked at |
| No script | fr 1440, ar 390 | The whole form and the stage at rest; the show / hide control is not drawn (it would do nothing) |
| Reflow 1.4.10 | 320 × 640 (phone) and 320 × 256 @ 4 (400 % of 1280 × 1024): login, sign-up, reset, verification sent, the code — fr, ar; 360 × 640 in four languages | 0 px of horizontal overflow (the one «offender» is the honeypot parked off-screen), 0 text cut, 0 text over text; the primary's label inside its plate; the label row's link clear of the label. The submit's lower edge at 360 × 640: 613 px fr, 562 ar, 585 it / en (L5) |
| Text spacing 1.4.12 | login and sign-up, fr, ar, 1440 and 320 | Clean: no overflow, nothing cut or overlapping, the primary's label inside its plate |
| Targets (effective hit boxes: `elementFromPoint` along both centre lines) | 20 cells: five pages × fr, ar × 1440 (fine) and 390 (coarse asserted) | Fields 52 px, the primary 52, the eye 44 × 44, the reset link 24 / 44 under a finger, the way back 24+ / 44, the help address 44 under a finger. Below SP-8: A2 |
| The show / hide control | fr 390 | A finger's press hands the focus back to the field with its caret where it was (3, 3), `type="text"`, `aria-pressed="true"`; Space from the keyboard keeps the focus on the control, `aria-pressed="false"`; the name never changes («Afficher le mot de passe») |

## Performance — against the merge base and W1-0's manifest

**Protocol.** The lane's compressed twin on 8787 — the plan's 8782 shape (DEBUG off, `CompressedManifestStaticFilesStorage`,
hashed URLs, gzip on the wire, its own `STATIC_ROOT`; settings outside the repository, copied from the W2-D check's) on the
lane's port and database; the two raw entries left out of `collectstatic` (C1). The branch served from its worktree, the
merge base from a plain export of `3c288d6`, each from its own collected root. W1-0's protocol P and analysis, imported
read-only (`analyse.py` on `an_pfr.py`, `capture.py`'s `cls_of` and `bytes_summary`): profile A (150 ms RTT, 1.6 / 0.75
Mbps), CPU × 4, cold loads, fresh profile, a click on the address field at 5 s, then a Tab. **n = 9 per cell and arm, in
alternating blocks (branch 5, base 5, branch 4, base 4)**; medians with min–max; arm differences tested by permutation
within the cell. The machine was 21–28 % busy during loads (the branch's blocks a little busier: a bias against it). A
lane's screen for regressions, not the Performance Lead's PASS on 8782 (which C1 prevents today); W1-0's milliseconds come
from another port and database and are compared only for direction.

| Cell (median of 9) | LCP branch · base · W1-0 | FCP | First-render task | Longest load task | TBT | CLS (max) | INP proxy (max) | LCP element branch · base |
|---|---|---|---|---|---|---|---|---|
| fr · 1440 | **1 400** (1 384–1 512) · 1 332 · 1 720 | 1 200 · 1 164 | 79.0 · 87.4 · 397 | 94.7 · 90.2 | 70 · 43 | 0.016 (0.023) · 0.016 (0.037) | 64 (88) · 40 (56) | the door's photograph 9 / 9 · V4's doorway 9 / 9 |
| fr · 412 @ 1.75 | **1 488** (1 400–1 684) · 1 364 · 1 708 | 1 188 · 1 160 | 46.5 · 46.8 · 384 | 98.0 · 78.7 | 65 · 30 | 0 · 0 | 48 (56) · 40 (48) | **the stage's grain 9 / 9** · the invitation 9 / 9 |
| ar · 1440 | **1 632** (1 608–1 776) · 1 512 · 1 872 | 1 376 · 1 332 | 84.6 · 87.0 · 485 | 118.0 · 114.6 | 128 · 114 | 0.013 (0.018) · 0.014 (0.032) | 64 (88) · 48 (72) | the door's photograph 9 / 9 · V4's doorway 9 / 9 |
| ar · 412 @ 1.75 | **1 576** (1 472–1 780) · 1 500 · 1 872 | 1 356 · 1 316 | 46.2 · 47.2 · 483 | 127.9 · 98.5 | 117 · 55 | 0 · 0 | 56 (64) · 40 (64) | the assurance paragraph 9 / 9 · the help line 9 / 9 |

- **Branch − merge base:** LCP +68 / +124 / +120 / +76 ms (p ≤ 0.007), FCP +28 to +44 ms (p ≤ 0.001), the first-render
  task −8.4 to −0.3 ms (not significant), the longest load task +3 to +29 ms (style and layout of the stage's DOM and
  rules; +19 and +29 on phones), TBT +14 to +62 ms, the INP proxy +8 to +24 ms (p ≤ 0.023). Tasks over 50 ms per load are as many as on
  the base (medians 4 · 3 · 4 · 3 against 4 · 3 · 5 · 4). At 1440 the door's photograph finishes ≈ 30 ms later behind
  5.7 KB more CSS and JS on the slow link, and FCP is ≈ 40 ms later: the bytes of P1, measured.
- **Against W1-0 (§2.6's reference):** LCP 220–320 ms earlier in all four cells, the first-render task 46–85 ms where V4's
  was 384–485 — the «no worse» tolerances (+50 ms LCP, +30 ms first-render task) are not approached. LCP ≤ 2.5 s
  everywhere; CLS ≤ 0.05 on this flagship in every load (0.023 at most).
- **CLS sources at 1440:** every load-time shift on the branch is the navigation (`nav.main-nav.is-enhanced`, 17 shifts in
  18 loads); the entrance's own sources on the merge base (the V4 sheet's centring, 5 shifts; its door) are gone. 0 on
  phones.

**Bytes and requests, as served (fr; encoded = on the wire)**

| | W1-0 (V4) | Merge base | **Branch** | Budget (§2.6) |
|---|---|---|---|---|
| CSS before `load` | 37 502 in 2 | 43 509 in 2 (`main` 42 527, entrance 982) | **47 628 in 2** (`main` 42 613, entrance 5 015) | ceiling 45 694 — **P1** |
| JS before `load` | 34 488 in 6 | 37 897 in 5 | 39 615 in 6 (`entrance.js` 1 663) | ≤ 45 KB a public page: met |
| CSS + JS requests before `load` | 8 | 7 | 8 | ≤ the before set's: met |
| Fonts | 217 732 in 5 · ar 484 456 in 11 | 20 956 in 2 · ar 53 184 in 3 | 20 956 in 2 · ar 53 184 in 3 | ≤ 25 KB · ≤ 56 KB: met |
| Images before `load`, 1440 | 45 078 in 4 | 49 748 in 4 | 158 783 in 8 | — |

The door's photograph is V4's file (42 494 B); `grain.svg` (246 B) replaces V4's `key.svg` (307 B). The four navigation
photographs (≈ 109 KB, W2-C1's) start 420–565 ms after the LCP in both arms; they count «before `load`» on the branch only
because its `load` lands ≈ 20 ms later.

**The stage's life**

- **The arrival** (18 of 18 desktop loads): starts 452–736 ms after the LCP entry (medians 493 fr, 521 ar), lasts
  2 421–2 434 ms (L7: ≤ 3.4 s), holds **0 tasks over 50 ms** (main thread 57–59 ms per second); all of the stage's
  animations composite (13 of 13 in the load inspected) — the only non-composited animations in either arm are the field's
  four 120 ms border-colour transitions (W1-C's). Never on the band, never under reduced motion, cut by any focus.
- **At rest:** after the arrival, three idle seconds traced — 0 style recalculations, 0 layouts, 0 paints, 0 animation
  frames, 0 timers, 0 running animations, 0 `will-change` (fr and ar at 1440, ar at 390, and with the address focused).
  Nothing loops.
- **The engage** (n = 16 per arm, the POST answered 204): the submit's Event Timing 48 ms median (max 72) against the merge
  base's 52 (max 88); `aria-busy` set 3.6–4.6 ms after the click, in its own task (L8); the 1.5 s after the submit hold
  6 tasks over 50 ms in 5 loads of 16 in each arm; `loader.js` (1 502 B) is fetched on the first submit in both.
- **The click and the Tab** into the form: within the 200 ms INP budget, heavier than the base's — P3.

## Seen, not this family's

- **The skip link's ring on phones is 1.68 : 1** (`#7fd1d8` on the paper header) — on the home and the contact page too, so
  it is the base template's; the link itself is a navy pill that appears only on focus, which is the indicator. Not a
  failure.
- **W2-C1** — under reduced motion the navbar's panels run an 80 ms `display` transition at load (discrete, invisible); the
  navigation is the only source of layout shift at 1440 (≤ 0.023 a load); its photographs start ≈ 20 ms before `load` here
  (after the LCP).
- **W1-C** — the field's four border-colour transitions are the page's only non-composited animations (120 ms); the
  sign-up's two eyes share one name («Afficher le mot de passe»), each tied to its field by `aria-controls` — clear in
  context, could name the confirmation's.

## Method, limits, not done

- Own headless Chromium, own persistent profiles under `C:/tmp/ile_v5_council/.profiles/w2-b-a11y-perf/` (removed after each
  context; none left), one browser at a time, no pytest. Every browser start waited on the benchmark lock: never present,
  never created by this role. No run ended on «Target crashed». Never 8780, 8782, 8887 (the senior reviewer's server, which
  worked beside this check), 9222 or 9223.
- Servers on 8787, each stopped after its series: the dev server (accessibility; restarted twice to clear allauth's
  in-memory rate-limit counters after the refused and 429 series), the compressed twin (performance, branch and merge base
  in turn), the dev server again for the style diagnostic. The twin's static roots and the merge base's export lived in
  this role's scratch folder and were removed. Writes to `ile_v5_l7`: the session rows (minted, then revoked) and what the
  product records for twelve refused sign-ins and six reset requests on addresses no account has (audit events); allauth's
  rate-limit counters live in the server's memory.
- Three instrument faults found and corrected before any figure was used: the first contrast pass read two links half-way
  through a colour transition (made by the measurement itself) — re-read with transitions frozen; the first engage run
  used a selector the merge base does not have — re-run with the contract's `form.form button[type=submit]`; the code
  page's first reflow cells were redirected to the sign-in when the pending session expired — re-run on a fresh one.
- Not done: Safari, Firefox, a real phone, a screen reader with a person, a password manager; L8's next-page delay against
  the reduced-motion baseline was not re-measured (the implementer's: 7.2 ms against 5.0); Blink's invalidation tracking
  slows the engine, so P3 uses its element counts, not its milliseconds; the timing figures are a lane's screen, not 8782's
  PASS (C1); emulated phones; HTTP/1.1 only.

## Evidence and tools

`C:/tmp/ile_v5_council/evidence/v54/w2-b/a11y-perf/` — `s1_structure.json` (and `s1/` captures), `s2_keyboard.json`,
`s3_contrast.json` (first pass, superseded) and `s3_contrast_v2.json`, `s4_modes.json` and `s4/` (reduced-motion pairs,
forced-colours and no-script captures), `s5_reflow_targets.json` and `s5/`, `s7_429.json` and `s7/`, `s8_misc.json` and
`s8/`, `s9_tabstyle.json`, `perf/P/runs.jsonl` (72 traced loads, one trace kept per cell and arm), `perf/E/runs.jsonl`
(32 engage loads), `perf/summary-P.json`, `perf/summary-E.json`. Tools, outside every repository:
`C:/tmp/ile_v5_council/.work/w2-b/w2-b-a11y-perf/` (`rig.py`, `s1_structure.py` … `s9_tabstyle.py`, `perf_trace.py`,
`perf_compare.py`, `twin/settings_8787_twin.py`, `twin/collect.sh`, the start and stop scripts, `mint.py` / `revoke.py`).
