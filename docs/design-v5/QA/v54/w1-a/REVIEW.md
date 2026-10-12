# W1-A · Senior review — design, UX and taste in one pass

**Reviewer** label `w1-a-review` (built nothing) · 8 October 2026, 19:50–20:20 · V5.5 delivery mode
(`C:/tmp/ile_v5_council/directives/V5_5_DELIVERY_MODE.md`: implement → review once → fix → ship; no council, no scoring
cycle) · the settled direction: plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §1.1, §1.2, §1.3, §1.4, §1.6, §1.8, §2.1–§2.3,
§3.3 item 4, and DL54 (`DECISION_LOG_V54.md`, DL54-10, -13, -14, -15) · the bar: «credible alongside excellent
international digital products» (plan §3.1 item 1; the W1-K anchors in `../w1-k/CALIBRATION.md` §1.1, §1.2).

**Reviewed:** branch `v54-w1-a` at `b90479b` (the implementer's shipping notes; `NOTES.md`, `IMPLEMENTATION_NOTES.md`),
served by my own dev server **8883** from `C:/tmp/ile_wt/v54-w1-a` on `ile_v5_l3` (`ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, the preview routes on for one check), signed-in pages through sessions minted with
`Client.force_login` by a scratch script outside every repository (no password used, typed or stored; revoked at the end),
headless Playwright under `C:/tmp/ile_v5_council/.profiles/w1-a-w1-a-review/`. Nothing in the repository changed but this
file. E/ = `C:/tmp/ile_v5_council/evidence/v54/w1-a/review/`.

## 1. Verdict — SHIP_AFTER_FIXES

**No page is worse than V4; the foundation is what the plan decided, executed cleanly; one owner-facing defect must be
fixed before the merge reaches v5-live.** Nothing blocking: no broken page, no wrong direction, no unusable state, no data
or security problem in 160 captures.

- **Blocking (P0): none.**
- **Major (must fix before shipping): 1** — the preview's hero/type frames and the compare page link `css/fonts.css`, which
  W1-A removed; they lose every web face and log a 404 on each load (§3, M-1).
- **Minor (polish, for the owning families or a one-line alias): 9** (§3).

**The question asked.** Does the V5 foundation make every page at least as good as V4 and visibly more premium?
*At least as good:* yes, on every pair I judged by eye (§4: 0 «worse», 10 «same», 7 «better») and on every automated count
(§5). *Visibly more premium:* modestly, where the foundation itself is the surface — the login and the forms (16 px typed
text, 4 px corners, flat primaries, one ring), the console's state registers (amber dashed «Brouillon» / «À remplacer»,
ink «Vérifiée», lapis «En examen», the slate notice), the fonts (one voice, 21–56 KB a page instead of 218–525 KB, CLS 0
in all 160 cells), the quieter hero (the paper-plate primary instead of the teal gradient). The composition is still V4's
on every page — «V4 + fondation», as the plan says it must be until a family passes (§2.1) — so the step from ≈ 3 to the bar
is the families' work, not this one's. The public pages trade the serif's editorial stature for one grotesque voice: at
1440 the H1 is 36 px where V4 stepped it to 52, which reads tidier and smaller (§3, m-3). I mark that «same», not worse.

## 2. What was looked at, and how

| | |
|---|---|
| Pages | 20 page types: home, navbar open, login, signup, door (persons), pathway detail, FAQ, legal document, 404, 403, person dashboard, «Mes pièces», a document requirement, journey (empty) and journey results, case file, company dashboard, helpdesk, plus the home and the login in a keyboard-focus state |
| Languages · widths | fr and ar · 1440 × 900, 1366 × 768, 390 × 844, 360 × 800 (phones emulated: mobile + touch, DPR 1) — **160 captures** (`E/after/<id>/<lang>/…-viewport.png` and full page; records `E/after/runs/captures-{desktop,phone}.jsonl`) |
| Before / after | the W1-0 «before» set at `v54/base` on 8782 (`evidence/v54/w1-0/before/captures/`) beside my captures, first viewport and full page, at 1440 and 390, fr and ar: 45 composites in `E/compare/` (`tools/compose.py`), judged by eye one pair at a time (§4) |
| Probes per capture | loaded faces; the first family that draws each visible text node; the size histogram; Latin text under 12 px and Arabic under 14 px; line-heights off the 4 px line; distinct radii and shadows among the painted boxes of the first viewport; control heights, typed-text size, radius and weight; horizontal overflow; ellipsised text; CLS (layout-shift observer from document start); CSP violations; console errors; every response ≥ 400; a 14-stop keyboard walk (outline, box-shadow, radius of each stop); axe-core 4.13 colour-contrast at 1440 and 390 |
| Extra probe | `E/extra/`: the public H1/H2/lead computed sizes on six page types at 1440 and 390; the login's field and primary in `:focus-visible` (fr 1440, fr and ar 390); the dashboard's rail focus walk on night |
| Tools | `C:/tmp/ile_v5_council/.work/w1-a/w1-a-review/tools/{capture_review,compose,probe_extra}.py` — the capture waits while `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` exists (one wait was logged: none before the series; the smoke tests of §6 queued behind the a11y/perf check's window AB1) |
| Not done, by V5.5 | no six-scale scoring, no taste portraits, no blind ranking (not a flagship); no performance measurement on 8782 (the Performance Lead's); the full suite (the integration checkpoint's) |

## 3. Findings — only what matters

### Major

**M-1 · The preview's frames link a stylesheet W1-A deleted: every hero / type frame and the compare page answer with a
404 and fall back to system faces.** `templates/dev/designpreview/frame.html:38` and `compare.html:30` link
`{% static 'css/fonts.css' %}`; W1-A removes `static/css/fonts.css` by the deletion map (plan §2.3). Those two documents
load the token layers (`css/tokens.css`, `v2/tokens.css`, `v4/tokens.css`) and `dev/designpreview.css`, **not**
`dist/main.css` (`views.py:29`: «standalone documents»), so nothing re-declares a face: the preview bar and the frames'
chrome draw in Georgia / Segoe, and the owner's 8780 would log a failed request on every frame once `v54/w1-a` is checked
out in v5-live. Confirmed on 8883: `GET /__design-v5/hero/?variant=he&lang=fr&phase=3` → 200, the document links
`/static/css/fonts.css` → **404**; `compare.html` carries the same link. The implementer flagged it for W1-P in step 1 and
step 2 («the preview's bar loses its faces»); it is still open at `b90479b`.
*Fix (two lines, W1-P's files — a justified extra path written into the manifest at the merge, or W1-P itself):* replace
the link with `css/v5/fonts.css`, and add `css/v5/tokens.css` and `css/v5/aliases.css` after `v4/tokens.css` so that
`--font-ui` / `--f-sans` / `--font-display` resolve to the served faces (Host Grotesk, the wordmark, Vazirmatn); then
load `/__design-v5/hero/…`, `/__design-v5/type/…` and `/__design-v5/compare/…` with 0 failed requests and the bar in Host.
`docs/ACCESSIBILITY.md` (G-15) is already the one extra path the merge step carries; this makes two.

### Minor

**m-1 · Buttons and fields render at 6 px, the decided role is 4 px; every console screen shows four radii.**
`v4/buttons.css:24` sets `.btn { border-radius: var(--radius-md) }` (6) and the legacy field rules read the same name; plan
§1.3 gives buttons, fields and tooltips `--radius-sm` (4) and `md` to the targa, menu rows and the segmented track. Measured
in the first viewport (records `probe.radiiViewport`): dashboard, «Mes pièces», case file, company dashboard, helpdesk — 4 · 6 ·
8 · full (four values; DL54-14: at most three); the login 6 · 12 · full with the card on `xl` (dialogs) instead of `lg`
(panels); the home 6 · 8 · 12 · full. The implementer measured and reported the same («the fold to three is counted on the
boards … done in aliases or in the owning family's files»); the boards were dropped by V5.5. By eye the 6 px is coherent and
sharper than V4's 10 / 14 / 20, so this is polish — but the fold is one line: W1-C's retarget of `v4/buttons.css` and the
field rules to `--btn-radius` / `--field-radius` (both already 4 in `v5/tokens.css`), or, if the steward lets W1-A carry it,
`.btn, .form-field__input { border-radius: var(--radius-sm) }` in `v5/base.css` folds the console to 4 · 8 · full.

**m-2 · The Arabic phone console's bottom-bar labels stay at V4's 11 px** (`span.console-bottom__label`, 5 per page, every
console page in Arabic at 390 and 360: records `arabicUnder14`), below the type system's own floor («never under 14 px in
Arabic», plan §1.1), while the Latin labels were lifted to 12 px on the bar's own line. Identical to V4, so not a
regression; the implementer's note is right that 14 px wraps and the fixed 56 px bar clips — the bar's geometry and label
policy are W3-A's. The accessibility check may weigh it higher; from the design chair it is a parity gap Arabic readers meet
on the console's only phone navigation.

**m-3 · The public H1 is a fixed 36 / 44 at every width.** V1 stepped `--t-title-size` 32 → 34 → 42 → 48 → 52 px up to
90 rem; the alias holds the eight-size scale's 36 (`E/extra/probe_extra.json`: `h1.page-header__title` 36 px at 1440 on the
door pages, the pathway, the FAQ, the glossary, the legal page). At 390 the H1 rose from 32 to 36 (better); at 1440 the door
pages' locked all-caps titles («VOTRE PARCOURS RÉGULIER VERS L'ITALIE», 36 px · 600 · +0.02 em) read heavier and smaller
than V4's 52 px serif caps — the first screen of a door page lost stature (`E/compare/door-persons-fr-1440x900.png`). This
is the settled scale (§1.1: titles 36), so «same», not worse. Polish for W3-F's composition of the public interior, or now
in `v5/base.css`: locked all-caps titles at `--w-display` (500), as the display line is — a capital run at 600 is what
makes it a label.

**m-4 · The page-header lead sits on a 33 px line.** `.page-header__lead` reads `--leading-relaxed` (1.65,
`_legacy-tokens.css:141`) at 20 px → 33 px, off the 4 px line on every public page header (RH-1); the lead's token is 28 px.
One alias (`--leading-relaxed: 1.6`) or the lead on `--t-lead-lh` in `v5/base.css`; W3-F otherwise.

**m-5 · Arabic navbar links at 13.5 px at 1366** (`a.main-nav__link`, the V4 header's narrow-desktop step; 7 links on the
Arabic home and the open navbar at 1366 only) — below the 14 px Arabic floor. V4's own rule; W2-C1 replaces the navbar.

**m-6 · The footnote marker on the documents pages is 9.36 / 10.08 px** (`span.note__marker` «1», the «one node at
9.36 px» of the family's own audit, still there at 390 and 1440 in French). A superscript index, not running text; polish:
`0.75em` on the marker.

**m-7 · Arabic font budget on two page types.** `document-requirement` and `dashboard-person-terms-pending` download
63 144 B in Arabic (ILE Mono's second file for a lowercase hash and a rule version) against the 56 KB budget — the
implementer's own measurement and remedy (move `a–f` and `v` into the mono core, ≈ +1 KB on every console page that prints a
reference). Not a regression (V4: 484–505 KB); the accessibility / performance check's call.

**m-8 · Shadows: four distinct values on the dashboard's first viewport, five on the case file** (records
`shadowsViewport`), re-valued to SH-1's levels but not folded to SH-8's console cap (one raised panel, two values). The
console families' (W3-A, W3-B); the levels and the night colour are right.

**m-9 · The field halo of §1.6 does not reach the fields yet.** On the login the focused field shows the 2 px laguna ring
at 2 px and its border turns laguna (`E/extra/login-field-focus-fr-1440.png`; outline `solid 2px rgb(29,138,147) off=2px`),
but the 5 px halo is overridden by the legacy field rules (components.css (0,4,1), entrance.css (0,5,1)) which paint V1's
2 px paper shadow instead. Visible, clean, WCAG-fine; the halo is W1-C's when it takes the field rules.

### Not findings — programme notes

- The Wave-1 CSS allowance leaves **1.7 KB gzip per page type** for W1-B, W1-C and W1-D (`NOTES.md` §(c)); the lever is the
  rest of W1-A's deletion map (the V1 / V2 / V4 declarations `v5/aliases.css` re-declares), left undone by V5.5 (e).
- The three specimen boards and the three-screen radii comparison were not built (V5.5 (e)); this review judged the real
  pages instead, which is what V5.5 asks.
- `scripts/check_ownership.py w1-a design-v5` → 55 inside, 10 slice, 1 generated, **1 outside** (`docs/ACCESSIBILITY.md`,
  the G-15 path), as the implementer recorded — the merge step's justified extra path. M-1 adds the two preview templates.

## 4. Pair by pair, by eye (before = W1-0 at `v54/base` · after = `b90479b`; 1440 and 390, fr and ar)

| Page | Mark | What the eye meets |
|---|---|---|
| Home (1440, 1366, 390, 360; fr, ar) | same → better | the name in the wordmark face (600) is heavier and more compact than V4's Newsreader 300; the primary is the paper plate on night (flat, calm) instead of the teal gradient; the four-entrance legend and the door stage untouched; section titles in Host 600 at 28 read tidier and smaller than the serif; the footer's name in the wordmark. 10 distinct sizes at 1440 (V4 11); CLS 0 |
| Navbar open (1440 mega-menu; 390 drawer; fr, ar) | same | identical structure; the panel's corners sharper; Host throughout; Vazirmatn in the Arabic panel with Latin runs in Host |
| Login (1440, 390; fr, ar) | **better** | the card at 12, fields and primary at 6, typed text 16 px, the flat laguna primary at 52 px, one ring on focus; the Arabic help link now 1 px clear of the field. The password placeholder / toggle overlap at 390 in Arabic is V4's own (identical before) — W1-C / W2-B |
| Signup (390, fr) | **better** | 16 px fields; the password rules in Host instead of the serif |
| Door: persons (1440, 390; fr, ar) | same | the caps title at 36 / 600 smaller than V4's 52 serif (m-3); the lead and the pathway list cleaner; the Arabic page's section titles in Vazirmatn 600 |
| Pathway detail (1440, 1366, 390; fr, ar) | same | the same page, one voice; the stepper's letter-by-letter column labels are V4's own (W3-D) |
| FAQ (1440, 390; fr, ar) | same (1440) · better (390) | questions at 20 / 600 read as titles; at 390 the H1 at 36 and the lead at 20 carry the page better than V4 |
| Legal document (1440; fr, ar) | same | the «page en préparation» notice now on the slate wash (C2) |
| 404 · 403 (1440, 390; fr, ar) | same → better | the big numeral in Host 600, flat buttons; Vazirmatn on the Arabic pages |
| Person dashboard (1440, 1366, 390; fr, ar) | same → better | «Brouillon» amber dashed with the hatch, «1 en attente» in amber, «Continuer» flat; the phone console one step up (16 / 15 / 14) with nothing clipped; the compact rail at 1366 as before |
| «Mes pièces» (1440, 390, 360; fr, ar) | same → better | the filter chips' marks on the registers (lapis «En examen»), the search at 16 px, the rows unchanged; the Arabic phone page more legible than V4 |
| Document requirement (1440, fr) | same | the reference in ILE Mono, «À remplacer» amber dashed |
| Journey, empty (1440, fr) · results (1440 fr, 390 ar) | same | the informative notice on the slate wash with its slate edge (C2) instead of V4's blue; the meta line in the sans with tabular figures |
| Case file (1440 fr, 390 ar) | same → better | the Arabic phone case file steps up and the station labels sit on the 4 px line; «مسودة» amber |
| Company dashboard (390, fr) | **better** | «Vérifiée» in ink (O14) instead of V4's amber; the bar title «Espace entreprise» whole (the implementer's fix) |
| Helpdesk (1440, ar) | same | the Arabic rail and queue in Vazirmatn; chips on the registers |

Zero «worse». The composition is V4's everywhere; the gain is in the material (faces, colour meaning, corners, flatness).

## 5. The numbers (160 cells)

- **Health:** 0 responses ≥ 400 beyond the error pages' own status · 0 console errors beyond them · 0 CSP violations ·
  0 status mismatches · 0 horizontal overflow at 1440 / 1366 / 390 / 360 · **CLS 0 in every cell** (observer from document
  start) · axe colour-contrast: **0 failures** on 40 cells (the forum eyebrow of the before set is not in this page set).
- **Faces drawn:** French — Host Grotesk 5 944 text nodes, ILE Wordmark 388, ILE Mono 76, Segoe UI 42 (the «ع» control,
  by design); Arabic — **Vazirmatn 4 812**, Host Grotesk 1 126 (Latin runs), ILE Wordmark 340, ILE Mono 76; **no system
  fallback draws Arabic**. Fonts per page: 2 preloads on Latin pages, 3 on Arabic ones.
- **Sizes:** the home 10 distinct at 1440 (the 11 px ™ of the lock-up and a 25.6 px legacy value are the two outside the
  eight); the FAQ 9; the dashboard 8. Latin under 12 px: only the lock-up's ™ (11 / 7.7 px, a brand drawing) and the
  footnote marker (m-6). Arabic under 14 px: the bottom-bar labels (m-2) and the 1366 navbar (m-5). Typed text 16 px on
  the login, the signup, the documents search.
- **Controls:** login primary 52 px, fields 44, the dense «show password» 36; console primaries 44, dense 36; the phone
  bottom bar 56. Weights 500 on what acts, 600 on titles, 400 on text.
- **Focus:** 14-stop walks on every standard capture — a ring on every stop (laguna-550 on paper, laguna-400 on the night
  rail and the skip link, 2 px at 2 px, the element's radius); the field's border turns laguna; the forced-colours rule is
  in the cascade (`v5/base.css`). Ellipsised text only at 1366 on console pages: the collapsed rail's hidden labels, as in
  V4 (the compact rail), not a clip.
- **Radii in the first viewport:** public pages 2–3 values; console pages 4 (m-1); the home 4.

## 6. Against the decisions — compliance

| Decision | Found | |
|---|---|---|
| §1.1 faces: Host 400–700 (preloaded), italic on use, ILE Wordmark for every name, ILE Mono in one seat, Vazirmatn | yes; the wordmark on the lock-up, the rail, the hero's name line, the footer; the mono on references only; no page draws a V4 face | ✓ |
| §1.1 scale: eight public sizes, 500 / 400 / 600 by role, tracking stops at 20, typed text 16, floors 12 / 14, Arabic 600 without ×1.15 | yes, with the two Arabic floor leftovers V4 owns (m-2, m-5) and the fixed 36 px H1 (m-3) | ✓ (noted) |
| §1.1 console step-up below 48 rem / coarse pointer | yes: 16 / 15 / 14 / 13 / 12 on every phone console capture, nothing clipped | ✓ |
| §1.2 colour: lapis «En examen», slate information notice, attesa dashed / nullo dotted at 600, hatch 0.78, glass 0.94, argento, O14 ink, no violet | yes on every chip and notice seen; no violet on any page; «Vérifiée» in ink | ✓ |
| §1.3 corners «Lo spigolo» 2 · 4 · 6 · 8 · 12 · full | the values, yes; the roles one step up on buttons / fields / the login card; four values on console screens | ✓ values · m-1 roles |
| §1.4 shadows: five levels in the night's colour, no glow, primaries flat, glass on the two bars only | yes: no gradient primary remains (`linear-gradient(a, a)`), no glow, the login's panel solid; the console's count not folded (m-8) | ✓ (m-8) |
| §1.6 focus: `:focus-visible` only, 2 px ring at 2 px on the radius, laguna-400 on night, halo on fields, Highlight in forced colours, never animated | yes except the field halo (m-9) | ✓ (m-9) |
| §1.8 control heights 36 / 44 / 52, hit 44 under a coarse pointer | yes where measured (login, console, home) | ✓ |
| §2.1 alias-first, in place; a regression fixed in the aliases, never in a template | yes: 67 files, no template but `base.html`'s head; the two sweep corrections in `v5/base.css` | ✓ |
| §2.3 deletion map (W1-A rows) | fonts.css and the 26 V4 woff2 gone; V1 links and focus moved; the shim's eleven names gone; the re-declared V1 / V2 / V4 declarations left (the CSS lever) | partial, recorded |
| «No page worse than before» | 0 worse by eye (§4); counts no worse (§5; the implementer's 316-pair sweep) | ✓ |

## 7. Smoke tests run by the reviewer

`tests/frontend/test_css_bundle_is_current.py`, `test_v5_tokens.py`, `test_legacy_token_shim.py` on
`test_ile_v5_l3`, behind the lock gate — queued behind the a11y / perf check's window AB1 (lock taken 20:07; the gate
timed out at 540 s and the run restarted once the lock lifted): **539 passed, 1 xfailed** (`test_the_shim_is_gone`, the
shim's deliberate marker) in 6.5 s, at `48c8a49` (`E/smoke.log`). The implementer's record stands as the suite evidence:
759 passed, 2 xfailed on the family's files; 62 browser tests at 0 skips (`NOTES.md`).

## 8. Evidence index

`E/after/` 160 captures + records · `E/compare/` 45 before / after composites · `E/extra/` the H1 and focus probes,
`probe_extra.json` · tools in `C:/tmp/ile_v5_council/.work/w1-a/w1-a-review/tools/`. Housekeeping: the three minted
sessions revoked and the secrets file removed at the end; the reviewer's server 8883 stopped; the browser profiles deleted.
