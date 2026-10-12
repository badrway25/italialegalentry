# W1-D · Accessibility + performance check — A11Y_PERF

Label `w1-d-a11y-perf`, 9 October 2026, one pass (V5.5: implement → review once → fix → ship). Built nothing. Reviewed the
family's branch `v54-w1-d` at `21b6b00` (merge base with `design-v5` `474ced9`) as served by lane 7 — the dev server on
`127.0.0.1:8787` from `C:/tmp/ile_wt/v54-w1-d` on `ile_v5_l7`, `ILE_REFERENCE_DATE=2026-10-03`; the served `dist/main.css`
is byte-identical to the worktree's (md5 `f7385aae…`). Signed-in pages through sessions minted by `Client.force_login` on
`ile_v5_l7` by a scratch script outside every repository (`.work/w1-d/w1-d-a11y-perf/mint_sessions_a11y.py`; no password
used, typed or stored; the rows are revoked at the end of this pass). Browsers: headless Playwright Chromium 1.63, one
fresh persistent profile per case under `C:/tmp/ile_v5_council/.profiles/w1-d-a11y-perf/`; the setting emulated with
`reduced_motion="reduce"` and `forced_colors="active"`, never the `html.rm` flag. The baseline's own tools were reused
where a number is compared with the «before» set: `health.js` (overflow, targets, the focus walk's indicator rule) and
axe-core 4.13.0 with the WCAG 2.x A/AA tags. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w1-d/a11y-perf/`
(`console/<case>/record.json` + PNGs, `login/<case>/`, `buttons/`, `l1_host/`, `perf/perf.json`, `bytes.json`); the
probes under `C:/tmp/ile_v5_council/.work/w1-d/w1-d-a11y-perf/`.

## Verdict — SHIP_AFTER_FIXES

0 blocking · 2 major · 4 minor · observations for other families. Nothing a person cannot do; no performance regression
against the baseline (bytes inside §2.6, no long task introduced, every LCP element unchanged, CLS 0, nothing loops).
The two majors are one-line CSS corrections in W1-D's own sheet (`static/css/v5/loader.css`): the busy key's dim face
sits under 3 : 1 on the primary button, and on a link-styled submit the key is drawn over the label's last glyphs.

## Findings

| # | Severity | What | Where | Fix |
|---|---|---|---|---|
| 1 | **major** | The busy key's dim face reads **2.69 : 1** against the primary button (white at 55 % over `#12777f`, measured on pixels in fr, ar, 390 and the keyboard/pointer cases; 2.72 computed). It is the one visual indicator of the busy state (the label does not change, the cursor is not available to a keyboard user), so WCAG 1.4.11 asks 3 : 1. Under forced colours it reads 4.81 : 1 (ButtonText at 55 % on ButtonFace). | `v5/loader.css` §3, `.btn.is-busy::after { opacity: 0.55 }` and `.busy-key { opacity: 0.55 }` | `opacity: 0.65` → 3.18 : 1 on `#12777f`, 3.66 : 1 on `#0f6a72` (the lit face stays 1); 0.62 is the floor. Keep the dim → lit distinction, it survives at 0.65. |
| 2 | **major** | On a **link-styled submit** (`.btn--link`, `--btn-pad: 0`) the key is drawn 8 px from the inline end — over the label: the whole key box (372.8–380.4 px) lies inside the text run (the label ends at 387.4 px; padding-inline-end 0px), so the 7.7 px key covers the glyphs 8–15.7 px from the label's end. `templates/portal/messages.html:31` ships one («Marquer comme lue», `btn btn--link btn--sm`, `type="submit"`) for every unread communication. Picture `l1_host/btn_link_busy.png`. Transient (until the answer replaces the page) but on a slow link it is the legible state of the control. | `v5/loader.css` §3 | For `.btn--link.is-busy::after, .btn--inline.is-busy::after` place the key *after* the label without touching layout: `inset-inline-end: calc(-1 * (var(--s-2) + var(--key-size) * 40 / 94))` (the button's box is the text, overflow is visible, 0 px of shift). Alternatively `content: none` for link buttons and rely on `aria-busy` + the guard. |
| 3 | minor | **Focus is lost when «Réessayer» is pressed**: `retryFrom()` → `quiet()` sets `retry.hidden = true` while it is the focused element, so focus falls to `<body>` (measured: `active: body` after Enter on the control). The retry is reachable (Shift+Tab from the submit, one stop) and ringed (W1-A's ring, `l1_host/retry_focus.png`), 103.75 × 36 px. No product path reaches it yet (the login's engage is W2-B's wiring), so minor; it is W1-D's primitive. | `static/js/src/loader.js` `retryFrom()` | Before `quiet(host)`: focus the form's submit control (`form.querySelector('button[type="submit"]')?.focus()`), which is where the person is invited to go. |
| 4 | minor | The forced-colours rule `.sig__room, .sig__face--ink { display: none }` does not reach the ink layer: `.sig__turn > svg { display: block }` (0,1,1) beats it (0,1,0). Measured `ink_display: block` under `forced_colors: active` on both seats; harmless today because the ink's rest is `opacity: 0` and `_loader-light.css` sets `animation: none` there (the forced-colours still is pixel-identical at t0 and t400, and the picture keeps the mark's own colours, `console/rail_fr_1440_forced/tile_rest.png`). | `v5/loader.css` §5 | `.sig__turn > .sig__face--ink { display: none }` in the forced-colours block (or `:where()` the svg rule). |
| 5 | minor | **L2 inherits V4's busy fill flip.** `v4/buttons.css:105` still sets `--btn-fill: var(--accent); --btn-ink: var(--min-3); --btn-lighting: var(--grad-primary)` on every `.btn.is-busy`, so a secondary, danger or link button repaints as the primary gradient while busy (sweep: «Enregistrer et recalculer» `btn--secondary`, «Confirmer la suppression» `btn--danger` → white on the teal gradient; the link button in `l1_host/btn_link_busy.png` becomes a solid slab). Contrast stays fine (5.29–6.32 : 1); the semantic change (a danger action turning primary) and the surprise are the issue. The busy face per variant is W1-C's gate (§3.3 item 7). | `v4/buttons.css` §BUSY (W1-C) — or neutralised in `v5/loader.css` | W1-C decides the busy face per variant; the quick neutralisation is `.btn.is-busy { --btn-fill: initial; --btn-ink: initial; --btn-lighting: initial; --btn-edge: initial }` in `v5/loader.css` so the button keeps its own colours and only the key changes. |
| 6 | minor | **A submit control with no busy face**: the account menu's logout (`button.account-menu__link`, not a `.btn`, 222 × 36) receives `is-busy` + `aria-busy` from `shell.js` on every console page but nothing draws (no key, no `cursor: progress`): assistive technology hears busy, the eye sees nothing. Navigates at once in practice. The control is W2-A's. | `templates/partials/account_menu*` (W2-A); `v5/loader.css` | Either make the item a `.btn--link` (then finding 2's rule applies) or let `shell.js` set the face only on `.btn` / `[data-busy-face]` controls. |

**Observations (not counted; for the senior reviewer and the owning families):**

- **Keyboard-initiated submits play the 320 ms turn.** `head.js` writes `html[data-input="key"]` on Enter, and plan §1.5's tier 0 reads «every keyboard-initiated change · 0 ms»; DL54-20 item 5 argues a submit is an activation and leaves the ruling to the reviewer. Accessibility impact nil (one 320 ms turn of a 7.7 × 18 px glyph; 0 s under the setting). The one-line rule, if the reviewer wants the letter of §1.5: `html[data-input="key"] .btn.is-busy::after { animation-duration: 0ms }`.
- **The console dashboard already animates at load** without the release: `rail-draw-y` × 6 (900 ms) on the journey steps and `strip-fill` × 2 (320 ms) on the health strip (named in `.work/…/exp_running2.py`'s log; all finite, all on zeroed tokens). MS §3.2 / §2.6 say «0 animations at load on console pages, except the entrance release»; these are V4's and W3-B's / W3-D's, not W1-D's — the release adds exactly its three.
- **The hero's `route-current` 28 s `infinite` loop** (`v4/hero.css:327`) is pre-existing V4 under `no-preference` only (not drawn under the setting, confirmed by the probes); «nothing loops» (§1.5) is W2-D's to settle. The removed universal block exposed nothing: at rest under the setting 0 animations run on every page probed (the implementer's 221 loads; mine on the console, the login and the home).
- **The Wave-1 CSS allowance is almost spent**: with W1-A's foundation the home sits at 46 743 B gz of its 47 306 ceiling and the dashboard at 49 546 of 49 860 (W1-D's share +1 224 in `main.css`, +249 in `console.css`). The next family lands over unless it deletes legacy rules first (§2.6 item 5).
- `head.js` grew from 198 to 919 B gz (the modality flag) — a synchronous head script, still trivial; `main.js` +338 B gz (the guard).
- The two «under 24 px» targets on the console («Accueil» 43 × 20, «Site public» 62 × 20) are the baseline's own (2 before, 2 after).

**Cross-reference with the senior review** (`REVIEW.md`, `9902b5b`, read after my series ran on `21b6b00`): its M1 — a
form whose answer is a file («Exporter mes données (JSON)», `/fr/compte/profil/`) keeps `is-busy`, `aria-busy="true"` and
`aria-disabled="true"` for ever — is an accessibility defect as well (4.1.3: a state announced that never ends; assistive
technology reports the control unavailable, and Playwright refused the second click on the same ground). My sweep gave the
class in place and never exercised a file answer, so it is not counted twice here; the opt-out it proposes
(`data-loader="none"` honoured by `shell.js`) also settles finding 6's class — a control that never receives an in-page
answer should carry no busy face — and should be fixed in the same step as findings 1 and 2. Its m3 is finding 5; its m2
is the second observation above; its m5 (`aria-disabled` where nothing refuses) is consistent with what I measured on the
login, where the guard does refuse.

## Accessibility — what was measured

### The entrance release (console first page) — fr and ar, rail and bar seats, reduced motion, forced colours, 320 px, 200 %

Each case is a fresh minted session (the first console page consumes the release); the second load of the same page is
the control (no host, the `<img>` back). «rest vs `<img>`» compares the layered mark's rest tile with the one-file mark on
the next page at the same seat (device scale 2). The Arabic rest tile is pixel-equal to the French one at the bar seat and
within 10/255 at the rail seat, and 175/255 away from its own mirror image: the mark is served unmirrored
(`host_dir: ltr` under `html[dir=rtl]`). The lit frame (seek to 360 ms) differs from the rest in 182 px of 10 816, all
inside the doorway (`tile_lit_360.png`). The release host is `aria-hidden`; the brand link's name is unchanged
(`link "Italy Legal Entry™ — Espace réservé"` / `"… — الفضاء الخاص"`, aria snapshot).

| case | persona | viewport | mode | release host (visible/in DOM · size) | host animations at load | running at 2.6 s / looping | CLS | LCP element | long tasks ms | overflow px | targets / under 24 px | axe violations | Tab stops / missing ring | rest vs `<img>` (max Δ / px > 8) | console errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bar_ar_390 | qa-doc-person | 390x844 touch @2 | - | 1/2 · 20 px | 3 (3 running) | 1 / 0 | 0.0 | p.panel__title | 0 | 0 | 17 / 0 (before 17 / 1) | 0 (before 0) | 16 / 0 | 32 / 2 | 0 |
| bar_ar_390_forced | qa-doc-person | 390x844 touch @2 | forced | 1/2 · 20 px | 0 (0 running) | 0 / 0 | 0.0 | p.panel__title | 0 | 0 | 17 / 0 (before 17 / 1) | 0 (before 0) | - / - | 32 / 2 | 0 |
| bar_fr_390 | qa-doc-person | 390x844 touch @2 | - | 1/2 · 20 px | 3 (3 running) | 4 / 0 | 0.0 | p.panel__title | 0 | 0 | 17 / 0 (before 17 / 0) | 0 (before 0) | 16 / 0 | 32 / 2 | 0 |
| bar_fr_390_reduce | qa-doc-person | 390x844 touch @2 | reduce | 1/2 · 20 px | 3 (0 running) | 0 / 0 | 0.0 | p.panel__title | 0 | 0 | 17 / 0 (before 17 / 0) | 0 (before 0) | - / - | 32 / 2 | 0 |
| documents_first_fr_1440 | qa-doc-person | 1440x900 @2 | - | 1/2 · 24 px | 3 (3 running) | 0 / 0 | 0.0 | p.doc-page__lead | [62] | 0 | 39 / 2 (before 39 / 2) | 0 (before 0) | - / - | 8 / 0 | 0 |
| rail_ar_1440 | qa-doc-person | 1440x900 @2 | - | 1/2 · 24 px | 3 (3 running) | 0 / 0 | 0.0 | h1.ctx__title | 0 | 0 | 28 / 2 (before 28 / 3) | 0 (before 0) | 30 / 0 | 8 / 0 | 0 |
| rail_fr_1440 | qa-doc-person | 1440x900 @2 | - | 1/2 · 24 px | 3 (3 running) | 0 / 0 | 0.0 | p.empty | 0 | 0 | 28 / 2 (before 28 / 2) | 0 (before 0) | 30 / 0 | 8 / 0 | 0 |
| rail_fr_1440_company | qa-company | 1440x900 @2 | - | 1/2 · 24 px | 3 (3 running) | 0 / 0 | 0.0 | p.panel__title | 0 | 0 | 25 / 2 (before 25 / 2) | 0 (before 0) | - / - | 8 / 0 | 0 |
| rail_fr_1440_forced | qa-doc-person | 1440x900 @2 | forced | 1/2 · 24 px | 0 (0 running) | 0 / 0 | 0.0 | p.empty | 0 | 0 | 28 / 2 (before 28 / 2) | 0 (before 0) | 12 / 0 | 8 / 0 | 0 |
| rail_fr_1440_person_terms | qa-person | 1440x900 @2 | - | 1/2 · 24 px | 3 (3 running) | 6 / 0 | 0.0 | p.panel__title | 0 | 0 | 28 / 2 (before 28 / 2) | 0 (before 0) | - / - | 8 / 0 | 0 |
| rail_fr_1440_reduce | qa-doc-person | 1440x900 @2 | reduce | 1/2 · 24 px | 3 (0 running) | 0 / 0 | 0.0 | p.empty | 0 | 0 | 28 / 2 (before 28 / 2) | 0 (before 0) | - / - | 8 / 0 | 0 |
| reflow_ar_320 | qa-doc-person | 320x568 touch @1 | - | 1/2 · 20 px | 3 (3 running) | 4 / 0 | 0.0 | p.panel__title | 0 | 0 | 17 / 0 (before 17 / 1) | 0 (before 0) | - / - | 12 / 2 | 0 |
| reflow_fr_320 | qa-doc-person | 320x568 touch @1 | - | 1/2 · 20 px | 3 (3 running) | 1 / 0 | 0.0 | p.panel__title | 0 | 0 | 17 / 0 (before 17 / 0) | 0 (before 0) | - / - | 12 / 2 | 0 |
| zoom200_fr_720x450 | qa-doc-person | 720x450 @2 | - | 1/2 · 20 px | 3 (3 running) | 0 / 0 | 0.0 | p.panel__title | 0 | 0 | 17 / 0 (before 28 / 2) | 0 (before 0) | - / - | 32 / 2 | 0 |

Reduced motion is a real still: under the setting the three animations exist at 0 s and are `finished` at load; the tile at
t = 0 and at t = 1000 ms differ in 0 px (`still_t0_vs_t1000`), and equal the `<img>`. Forced colours: the room is
`display: none` (no light can show), no animation runs, the tile keeps the brand's colours (picture), t0 = t400 in 0 px.
The keyboard walk (real Tab presses, `focusPrep` / `focusCheck` of the baseline) found **0 missing and 0 weak indicators
on 134 stops** (fr 1440: 30, ar 1440: 30, fr 390: 16, ar 390: 16, forced fr 1440: 12), the rail's brand link ringed with the
layered mark inside it (`focus_brand_1.png`); the «obscured» column of the records lists only stops read while the page was
still scrolling to them (every entry is `offscreen`, none covered by another element). 320 px: no horizontal overflow in fr
or ar; the bar seat carries the release at 20 px. The 200 % proxy (720 × 450 @ 2): no overflow, the bar seat.

### L2 — the busy key on the login's CTA, on a real activation

Keyboard (Tab to the CTA, Enter), pointer and tap, fr and ar, reduced motion, forced colours, 390 and 720 × 450 @ 2. The
page is kept by a `preventDefault()` on `window`'s `submit` (the implementer's method: nothing reaches the server, the form
is submitted empty, no credential is typed); the state is read in the activation's own task and at 150 / 400 / 700 ms;
contrast on the pixels of the control at device scale 3 (key = the pixels of the key box that differ from the ground;
label = the brightest fifth of the label's pixels).

| case | viewport | mode | activation | first read | `aria-disabled` at 400 ms | focus still on the control at 700 ms | `::after` animation | key box (inline end), overlap with the label | button rect Δ / label rect Δ | key vs ground | label vs ground | ground RGB | submits (prevented before mine) | loader.js fetched on submit | Event Timing | long tasks | console errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ar_1440_forced_key | 1440x900 | forced | keyboard (24 Tabs) | 54 ms: busy true, class yes | true | True | sig-turn 0.32s ×1 op 0.55 | 7.66×18 @ 8 px, overlap 0.00 | [0.0, 0.0, 0, 0] / [0.0, 0.0, 0.0, 0] | 4.81 | 21.0 | [255, 255, 255] | [False, True] | True | [('keydown', 16), ('keyup', 16), ('keydown', 16)] | 0 | 0 |
| ar_1440_key | 1440x900 | - | keyboard (24 Tabs) | 60 ms: busy true, class yes | true | True | sig-turn 0.32s ×1 op 0.55 | 7.66×18 @ 8 px, overlap 0.00 | [0.0, 0.0, 0, 0] / [0.0, 0.0, 0.0, 0] | 2.69 | 5.29 | [18, 119, 127] | [False, True] | True | [('keydown', 24), ('keyup', 32), ('keydown', 16)] | 0 | 0 |
| fr_1440_forced_key | 1440x900 | forced | keyboard (24 Tabs) | 114 ms: busy true, class yes | true | True | sig-turn 0.32s ×1 op 0.55 | 7.66×18 @ 8 px, overlap 0.00 | [0.0, 0.0, 0, 0] / [0.0, 0.0, 0.0, 0] | 4.81 | 21.0 | [255, 255, 255] | [False, True] | True | [('keydown', 16), ('keyup', 16), ('keydown', 24)] | 0 | 0 |
| fr_1440_key | 1440x900 | - | keyboard (24 Tabs) | 82 ms: busy true, class yes | true | True | sig-turn 0.32s ×1 op 0.55 | 7.66×18 @ 8 px, overlap 0.00 | [0.0, 0.0, 0, 0] / [0.0, 0.0, 0.0, 0] | 2.69 | 5.29 | [18, 119, 127] | [False, True] | True | [('keydown', 16), ('keydown', 32), ('keyup', 32)] | 0 | 0 |
| fr_1440_ptr | 1440x900 | - | pointer | 137 ms: busy true, class yes | true | True | sig-turn 0.32s ×1 op 0.55 | 7.66×18 @ 8 px, overlap 0.00 | [0.0, 0.0, 0, 0] / [0.0, 0.0, 0.0, 0] | 2.69 | 5.29 | [18, 119, 127] | [False, True] | True | [('pointerover', 40), ('pointerenter', 40), ('pointerenter', 40)] | 0 | 0 |
| fr_1440_reduce_key | 1440x900 | reduce | keyboard (24 Tabs) | 58 ms: busy true, class yes | true | True | sig-turn 0s ×1 op 0.55 | 7.66×18 @ 8 px, overlap 0.00 | [0.0, 0.0, 0, 0] / [0.0, 0.0, 0.0, 0] | 2.69 | 5.29 | [18, 119, 127] | [False, True] | True | [('keydown', 32), ('keyup', 32), ('keydown', 16)] | 0 | 0 |
| fr_390_tap | 390x844 touch | - | pointer | 119 ms: busy true, class yes | true | True | sig-turn 0.32s ×1 op 0.55 | 7.66×18 @ 8 px, overlap 0.00 | [0, 0, 0, 0] / [0.0, 0.0, 0.0, 0] | 2.69 | 5.29 | [18, 119, 127] | [False, True] | True | [('pointerover', 24), ('pointerenter', 24), ('pointerenter', 24)] | 0 | 0 |
| fr_720x450_zoom_key | 720x450 | - | keyboard (10 Tabs) | 19 ms: busy true, class yes | true | True | sig-turn 0.32s ×1 op 0.55 | 7.66×18 @ 8 px, overlap 0.00 | [0, 0, 0, 0] / [0.0, 0.0, 0.0, 0] | 2.69 | 5.29 | [18, 119, 127] | [False, True] | True | [('keyup', 24), ('keydown', 16), ('keyup', 16)] | 0 | 0 |

Every case: busy face and `aria-busy` in the activation's task, `aria-disabled` by 400 ms, focus kept on the control, the
label and the button's box unmoved (0 px), the second activation refused by `main.js`'s guard (the second `submit` event
arrives already prevented), `loader.js` fetched on the first submit and never before, no long task, no console error; the
turn is 0 s under the setting (the key still, dim). In Arabic the key sits at the inline end (left) with the label unmoved
(`login/ar_1440_key/btn_busy_700.png`). Finding 1 is the key's 2.69 : 1.

### L2 — propagation: every visible submit control of 23 pages, given `.is-busy` in place

| page | control | classes | busy face drawn | label end → key gap px | overlap px | size shift / label shift px | fill changed / ink changed | method / data-single-submit |
|---|---|---|---|---|---|---|---|---|
| login_fr | button.btn.btn--primary <Connexion> | btn btn--primary | yes | 157.77 | 0 | no / 0 | no / no | post / yes |
| login_ar | button.btn.btn--primary <تسجيل الدخول> | btn btn--primary | yes | 147.78 | 0 | no / 0 | no / no | post / yes |
| signup_fr | button.btn.btn--primary <Création de compte> | btn btn--primary | yes | 121.52 | 0 | no / 0 | no / no | post / yes |
| password_reset_fr | button.btn.btn--primary <Réinitialiser mon mot de passe> | btn btn--primary | yes | 79.34 | 0 | no / 0 | no / no | post / yes |
| orientation_fr | button.btn.btn--primary.btn--large <Commencer> | btn btn--primary btn--large | yes | 25 | 0 | no / 0 | no / no | post / no |
| messages_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| messages_ar | button.account-menu__link <تسجيل الخروج> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| situation_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| situation_fr | button.btn.btn--secondary <Enregistrer et recalculer> | btn btn--secondary | yes | 21 | 0 | no / 0 | yes / yes | post / no |
| document_upload_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| document_upload_fr | button.btn.btn--primary <Déposer> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / no |
| documents_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| password_change_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| password_change_fr | button.btn.btn--primary <Modifier le mot de passe> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / yes |
| account_delete_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| account_delete_fr | button.btn.btn--danger <Confirmer la suppression> | btn btn--danger | yes | 21 | 0 | no / 0 | yes / yes | post / no |
| logout_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| logout_fr | button.btn.btn--primary <Se déconnecter> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / yes |
| profile_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| profile_fr | button.btn.btn--primary <Enregistrer> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / no |
| profile_fr | button.btn.btn--secondary <Exporter mes données (JSON)> | btn btn--secondary | yes | 21 | 0 | no / 0 | yes / yes | post / no |
| email_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| email_fr | button.btn.btn--primary <Rendre principale> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / yes |
| email_fr | button.btn.btn--secondary <Renvoyer le message de vérifica | btn btn--secondary | yes | 21 | 0 | no / 0 | yes / yes | post / yes |
| email_fr | button.btn.btn--danger <Enlever> | btn btn--danger | yes | 21 | 0 | no / 0 | yes / yes | post / yes |
| email_fr | button.btn.btn--primary <Ajouter un e-mail> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / yes |
| mfa_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| case_file_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| case_file_fr | button.btn.btn--secondary <Enregistrer l’état> | btn btn--secondary | yes | 21 | 0 | no / 0 | yes / yes | post / no |
| helpdesk_new_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| helpdesk_new_fr | button.btn.btn--primary <Enregistrer ma demande> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / no |
| helpdesk_detail_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| helpdesk_detail_fr | button.btn.btn--primary <Enregistrer> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / no |
| helpdesk_detail_fr | button.btn.btn--secondary <Clore définitivement> | btn btn--secondary | yes | 21 | 0 | no / 0 | yes / yes | post / no |
| company_need_form_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |
| company_need_form_fr | button.btn.btn--primary <Créer le besoin> | btn btn--primary | yes | 21 | 0 | no / 0 | no / no | post / no |
| company_profile_fr | button.account-menu__link <Se déconnecter> | account-menu__link | **no** | - | 0 | no / 0 | no / no | post / no |

37 visible controls: every `.btn` draws the key inside its own padding (label gap 21–158 px, 0 px of overlap, 0 size or
label shift); the one control without a face is the account menu's logout (finding 6); the fill flip on secondary/danger
is finding 5. The `btn--link` geometry (finding 2) was measured on a `btn btn--link btn--sm` submit built in-page from
`messages.html`'s markup, because the probing personas had no unread communication.

### L1 — the primitive, in-page on a console page (the words, the retry, the status line)

Host built from `components/loader.html`'s rendered markup with `word`, `slow`, `retry`, engaged through the real path
(`shell.js` → `loader.js` on Enter): at 120 ms `is-engaged` with one `sig-turn` 480 ms running and the control busy; at
1.2 s `is-worded` and the `role="status" aria-live="polite"` line reads the word (the line is server-rendered empty, so the
live region exists before it speaks); `slow()` adds the sentence and shows «Réessayer»; the retry puts host, form and
control at rest and a second engage is accepted. The status line is `--text-2` at 13 px: 6.46 : 1 on `--p-carta-50`
(7.17 on white; 9.94 for its night twin) — the system's own table demands 4.5 for this role (DS 2026 §6 row «testo
secondario»). Finding 3 is the focus loss on the retry.

## Performance — what was measured

Protocol: 127.0.0.1:8787 dev server (DEBUG, unhashed static, no compression): absolute ms are not the 8782 baseline's; the comparison is with vs without the release on the same lane, interleaved cold contexts, CPU x4 via CDP, n per arm. Comparison with the baseline is by **element identity, counts and deltas**, never by absolute
milliseconds (the baseline ran on the compressed twin 8782, slow 4G + CPU ×4; this lane is the dev server on localhost, CPU
×4 only). n = 5 cold persistent contexts per arm, interleaved, under the quiet-machine lock
(`C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK`, created only when absent, role and time inside, deleted in `finally`).

### Bytes (gzip −9 of the committed bundles, design-v5 → HEAD)

| file | design-v5 raw / gz | HEAD raw / gz | Δ gz |
|---|---|---|---|
| static/css/dist/main.css | 238800 / 42699 | 243332 / 43923 | +1224 |
| static/css/dist/portal/console.css | 12692 / 2687 | 13807 / 2936 | +249 |
| static/js/dist/chunks/chunk-4CTWE25X.js | — / — | 71896 / 26670 | +26670 |
| static/js/dist/chunks/chunk-5T5FIULM.js | 387 / 272 | — / — | -272 |
| static/js/dist/chunks/chunk-UCR2EZQS.js | 70084 / 26130 | — / — | -26130 |
| static/js/dist/chunks/chunk-VR2J32YB.js | 206 / 158 | — / — | -158 |
| static/js/dist/console.js | 4320 / 1681 | 4279 / 1675 | -6 |
| static/js/dist/home.js | 4270 / 1676 | 4190 / 1650 | -26 |
| static/js/dist/loader.js | — / — | 2717 / 1193 | +1193 |
| static/js/dist/motion.js | 332 / 235 | 476 / 299 | +64 |
| static/js/dist/shell.js | 3390 / 1486 | 3476 / 1555 | +69 |
| static/js/dist/situation.js | 2520 / 1196 | 2412 / 1139 | -57 |
| static/js/head.js | 233 / 198 | 1736 / 919 | +721 |
| static/js/main.js | 22622 / 6244 | 23591 / 6582 | +338 |

Per page type against §2.6's Wave-1 ceilings (baseline total + 8 192 B): home `main.css` 43 923 + `pages.css` 2 820 =
**46 743 ≤ 47 306**; door / interior 43 923 ≤ 44 486; login 43 923 + 1 208 = 45 131 ≤ 45 694; dashboard and case file
43 923 + 2 936 + 2 687 = **49 546 ≤ 49 860**; «Mes pièces» 43 923 + 6 545 = 50 468 ≤ 51 031; `main.css` 43.9 KB ≤ 45 KB.
JS: `loader.js` 1 193 B gz (≤ 4 KB, loaded on the first submit only); the home's scripts 37 376 B gz in all (≤ 45 KB;
baseline 36 892 on the wire), the console's 37 401; three chunks became one (+110 B gz, two requests fewer).

### The console's first page, CPU ×4 — with the release vs without

| arm | release host at load | animations running at load | running / looping at 3 s | load ms | LCP element @ ms | CLS | long tasks ms (whole load) | long tasks after `load` |
|---|---|---|---|---|---|---|---|---|
| with | 2 | 9 | 0 / 0 | 2469 | p.empty @ 2244 | 0.0018 | [131, 62, 105, 91, 57] | [57] |
| with | 2 | 11 | 0 / 0 | 1518 | p.empty @ 1412 | 0.0 | [65, 64] | 0 |
| with | 2 | 11 | 0 / 0 | 1157 | p.empty @ 1080 | 0.0014 | [214] | 0 |
| with | 2 | 11 | 0 / 0 | 1191 | p.empty @ 1084 | 0.0 | [54, 51] | 0 |
| with | 2 | 11 | 0 / 0 | 1178 | p.empty @ 1084 | 0.0 | [59] | 0 |
| without | 0 | 8 | 0 / 0 | 1195 | p.empty @ 1112 | 0.0 | 0 | 0 |
| without | 0 | 6 | 0 / 0 | 1708 | p.empty @ 1440 | 0.0 | [54, 67] | 0 |
| without | 0 | 8 | 0 / 0 | 1269 | p.empty @ 1156 | 0.0011 | 0 | 0 |
| without | 0 | 8 | 0 / 0 | 1280 | p.empty @ 1180 | 0.0 | 0 | 0 |
| without | 0 | 8 | 0 / 0 | 1034 | p.empty @ 964 | 0.0 | [167] | 0 |

| arm | n | long tasks per load (median) | long-task ms per load (median) | longest task ms, median (min–max) | LCP ms (median) | LCP element | CLS max | load ms (median) | running at 3 s / looping |
|---|---|---|---|---|---|---|---|---|---|
| with | 5 | 2 | 129 | 65 (54–214) | 1084 | ['p.empty'] | 0.0018 | 1191 | [0, 0, 0, 0, 0] / [0, 0, 0, 0, 0] |
| without | 5 | 0 | 0 | 0 (0–167) | 1156 | ['p.empty'] | 0.0011 | 1269 | [0, 0, 0, 0, 0] / [0, 0, 0, 0, 0] |

Reading. The LCP element is `p.empty` in all ten loads; CLS ≤ 0.0018 (the shifts named are the console bar's actions and
the context action, not the mark's seat); 0 animations running and 0 looping at 3 s in both arms; `load` and LCP medians
are *lower* with the release (one `<img>` request fewer). Long tasks: no task after `load` except one of 57 ms in the first,
cold load of the series; during the load phase the release arm shows one or two tasks of 51–65 ms where the plain page
shows none in three of five loads (its own first-render task sits just under the 50 ms threshold at CPU ×4 on this lane;
the outliers 131–214 ms and 167 ms fall on both sides). The first-render task is therefore no worse within §2.6's ±30 ms
resolution, and nothing a person would meet; the implementer's trace series (`NOTES.md` step 2: +131 ms of busy main
thread inside a ±230 spread, 36 compositor frames in both arms, `compositeFailed` 0) says the same with finer tools.

### The home and the login, CPU ×4 (LCP element, CLS, long tasks, loops, requests)

| cell | LCP element @ ms | CLS | long tasks ms | running / looping at 3 s | CSS / JS requests before `load` | scripts |
|---|---|---|---|---|---|---|
| home_fr_1440-0 | image.doorway__img @ 788 | 0.0213 | [103, 116, 63, 88, 127] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| home_fr_1440-1 | image.doorway__img @ 904 | 0.0243 | [136, 65, 67, 88] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| home_fr_1440-2 | image.doorway__img @ 712 | 0.0 | [50] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| home_ar_1440-0 | image.doorway__img @ 1112 | 0.0155 | [51, 113, 161, 65, 56, 76] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| home_ar_1440-1 | image.doorway__img @ 700 | 0.0028 | [176, 67, 65, 59] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| home_ar_1440-2 | image.doorway__img @ 1356 | 0.0051 | [151, 51] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| home_fr_412-0 | p.hero__body @ 988 | 0.0 | [117, 71, 55] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| home_fr_412-1 | p.hero__body @ 604 | 0.0 | [113, 50] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| home_fr_412-2 | p.hero__body @ 648 | 0.0 | [68] | 5 / 4 | 3 / 6 | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js |
| login_fr_1440-0 | image.doorway__img @ 704 | 0.0159 | 0 | 0 / 0 | 2 / 4 | head.js, main.js, shell.js, chunk-4CTWE25X.js |
| login_fr_1440-1 | image.doorway__img @ 484 | 0.0 | 0 | 0 / 0 | 2 / 4 | head.js, main.js, shell.js, chunk-4CTWE25X.js |
| login_fr_1440-2 | image.doorway__img @ 404 | 0.0017 | 0 | 0 / 0 | 2 / 4 | head.js, main.js, shell.js, chunk-4CTWE25X.js |
| login_ar_412-0 | p.entrance__help @ 500 | 0.0 | 0 | 0 / 0 | 2 / 4 | head.js, main.js, shell.js, chunk-4CTWE25X.js |
| login_ar_412-1 | p.entrance__help @ 516 | 0.0 | [54] | 0 / 0 | 2 / 4 | head.js, main.js, shell.js, chunk-4CTWE25X.js |
| login_ar_412-2 | p.entrance__help @ 464 | 0.0 | [50, 50] | 0 / 0 | 2 / 4 | head.js, main.js, shell.js, chunk-4CTWE25X.js |

### Requests at load (unthrottled)

| page | release | before `load` by kind | all requests by kind | scripts | sheets |
|---|---|---|---|---|---|
| home | 0 | {'font': 2, 'css': 3, 'js': 6, 'img': 3, 'other': 1} | {'font': 2, 'css': 3, 'js': 6, 'img': 3, 'other': 1} | head.js, main.js, shell.js, home.js, home.js, chunk-4CTWE25X.js | main.css, pages.css, grain.svg |
| login | 0 | {'font': 2, 'css': 2, 'js': 4, 'img': 3, 'other': 1} | {'font': 2, 'css': 2, 'js': 4, 'img': 3, 'other': 1} | head.js, main.js, shell.js, chunk-4CTWE25X.js | main.css, entrance.css |
| dashboard-release | 2 | {'font': 2, 'css': 4, 'js': 6, 'img': 1, 'other': 1} | {'font': 2, 'css': 4, 'js': 6, 'img': 1, 'other': 1} | head.js, rail-pref.js, main.js, shell.js, console.js, chunk-4CTWE25X.js | main.css, console.css, portal.css, v5-ile-mono-400.woff2 |
| documents | 0 | {'font': 2, 'css': 5, 'js': 6, 'img': 1, 'other': 1} | {'font': 2, 'css': 5, 'js': 6, 'img': 1, 'other': 1} | head.js, rail-pref.js, main.js, shell.js, console.js, chunk-4CTWE25X.js | main.css, portal.css, console.css, documents.css, v5-ile-mono-400.woff2 |

Reading: no `loader.js` before a submit on any page; `_loader-light.css` is inlined in `console.css` (no extra sheet
request; the console's CSS requests equal the baseline's 3); the home's script requests are 6 against the baseline's 8
(one shared chunk instead of three); every LCP element is the baseline's (`image.doorway__img` on the home at 1440, the
hero's body on the phone, `p.empty` / `h1.ctx__title` / `p.panel__title` on the dashboard, `p.doc-page__lead` on the
documents page); CLS 0 on every console load with the release (the seat is a fixed 40 × 40 tile and the `<img>` → layers
swap is server-side); 0 animations running and 0 looping at 3 s on every page.

## Honest limits

- Chromium headless only (no Safari, no Firefox, no real device); phones emulated; the 200 % zoom is a 720 × 450 @ 2 proxy.
- No person watched the motion at speed (plan §1.5); the frames here are deterministic seeks (360 ms, 1100 ms).
- The dev server is not the compressed twin: absolute LCP / long-task milliseconds are not comparable to the «before» set;
  the comparison made is with vs without the release on the same lane, element identities, counts and bytes.
- The L1 host and the link-button geometry were measured on markup built in-page (the product has no login engage yet —
  W2-B — and the personas had no unread communication); the CSS and the module are the product's.
- The sweep's `anim / dur / opacity` columns in `buttons/summary.json` were read after the class was removed (a probe
  slip); the animation values that count are the login series' (`sig-turn 0.32s × 1`, opacity 0.55).

## What this pass wrote and removed

Evidence and scratch only, outside every repository; this file in the worktree. Sessions: 38 minted (30 qa-doc-person,
4 qa-person, 4 qa-company); 17 rows revoked by `mint_sessions_a11y.py revoke` (the 16 keys still in the cookie file and
the one unused row of the minting window) and the cookie file removed; the ~21 rows whose first console page the cases
consumed were popped from the file before the pass started recording them, their values are nowhere readable (the browser
profiles that held them are deleted), and their rows lapse with `SESSION_COOKIE_AGE` by ≈ 17:35 on 9 October. Nothing
else was written on `ile_v5_l7` beyond what a page load writes.
