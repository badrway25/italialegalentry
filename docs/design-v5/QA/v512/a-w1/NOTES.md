# V5.12 · lane A · wave W1 — the loader «Lume» across every navigation (label v512-a-w1)

28 October 2026 · branch `v512-a-w1` from design-v5 `e047fae` · worktree `C:/tmp/ile_wt/v512-a` · lane server 8783
(dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, database lane l3) · binding: V5.12 §4, §5,
§18, §19 and the Director's DECISIONS C5, §1 T1–T3, §2 (tokens), §3 (rows Loader, Page transition), §10 lane A, Waves W1.

W1 for lane A is exactly: **T2 threshold + T1 View Transitions + the reduced-motion still + T3 the 40 px plate**, and
the C5 decision-log amendment. Nothing of W2/W3 (M1–M18, notices, accordions, drawer/depot regions, command palette) is
in this branch.

## What the owner sees, where

| Where | What | How to see it |
|---|---|---|
| Every public page (fr · it · en · ar, 1440 and 390) | **The threshold «la soglia»**: a link or a form that has not brought its page within 400 ms lights a 2 px gold line on the letterhead's rule (from the reading edge — right to left in Arabic — to 85 %, then held), the letterhead's mark turns its key once and holds, and at 1 s a legend «Chargement…» sits on the rule at the inline end (`role="status"`, said once). A fast page shows nothing. | DevTools → Network → «Slow 4G», click any header link. On the preview (fast local server) nothing shows, by design: no fake wait. |
| Every page change (Chromium ≥ 126, pointer) | **The page change**: the page cross-fades (120 ms out, 200 ms in, opacity only) and the brand mark is the one thing that travels between pages (`ile-mark`). Keyboard navigation: no transition. Language switch: the page fades, the mark does not travel (it never mirrors). | Click from the home to any page; fr → ar from the utility bar. |
| Sign-in → console | The door the key has just turned flies into the rail's tile (desktop) / the top bar's tile (phone), where the release lights. | Sign in (or the persona switch, which signs in the same way). |
| Console, first page of a session and first page of each further space (person ↔ company) | **The release on the 40 px plate**: the room's light in the mark AND the tile's whole paper plate takes a warm light with a halo on the night rail, 1.6 s, once per space per session. | Persona `qa-company` (Entreprise): the dashboard, then «Espace entreprise» — both light once; a reload does not. |
| Console navigation | The same threshold on the context bar (desktop: glass bar, gold line; phone: the night top bar, the night's light), the rail tile's key turns. | Slow network, click a rail entry. |
| A page reached after a slow navigation | Its mark plays the release's light alone, 600 ms. | Slow network, any link. |
| Reduced motion (OS setting) | **Branded feedback kept, nothing moves**: no View Transition; the threshold appears as its still — the line at 85 %, the key turned, the room lit in the mark (the ink key on light) — with one 80 ms fade, and the same word; the console release shows the lit still (room, ink key, plate) for 1.2 s, then one 80 ms fade. | Emulate `prefers-reduced-motion: reduce`. |

Never shown: downloads (`download`, `data-loader="none"`), a new tab/window, modifier/middle clicks, same-page anchors
(the skip link included), a form that opts out or engages its own host (the sign-in's door keeps its own engage), an
OUTCOME_BEARING form, the preview hub (`dp-page`: no threshold, no View Transition), error pages (their door stays still).

## What changed (files)

* `static/js/src/lume/threshold.js` (new, inlined into `shell.js`): when — the capture-phase click, the submit (from
  shell.js's own hook), the exclusions, `--motion-wait`, the word at 1 s, the 10 s lease, `pageshow`, `navigateerror`.
  Draws nothing. `OUTCOME_BEARING` is loader.js's list (a test holds the two equal).
* `static/js/src/shell.js`: imports and wires the threshold (shell.js runs on console pages too: base.html loads it
  under console.js).
* `static/js/head.js`: `pageswap` / `pagereveal` (skip from the keyboard, the hub, html.rm; `vt-lang` across a language
  switch) and the «slow» hand-off through sessionStorage (read once, within 5 s; storage refused → nothing).
* `static/css/v5/motion.css` (new, shared, last in `main.css`): T1, the letterhead's threshold, the arrival, the
  reduced-motion stills; keyframes `lume-out`, `lume-in`, `lume-line`, `lume-arrive`, `lume-fade`, `lume-still`.
* `apps/portal/static/portal/v5/_motion.css` (new console partial, imported last by `portal/console.css`): the tile's
  View Transition name per breakpoint, the context bar's threshold (day and night), the tile's key, the arrival.
* `static/css/v5/tokens.css`: `--lume-still: 1200ms` (a hold, kept under reduced motion), `--lume-line`,
  `--lume-line-night`, `--lume-line-to` (90deg; 270deg on `[dir="rtl"]`).
* `scripts/gen_loader_light.py` → `static/css/v5/_loader-light.css`: the plate's light (`lume-plate-o` on the
  release's phase, `::before` of the tile, halo on the night) and the reduced-motion lit still.
* `templates/partials/header.html`: the mark in layers (`components/loader.html`, `lock-sig`) laid exactly over the
  lock-up's `<img>` (measured: same box at 1440 and 390, fr and ar; the `<img>` hidden under it), and the band's
  status line. A back-office logo image has no layers: it neither turns nor travels.
* `templates/partials/portal_chrome.html`: both tiles carry the mark in layers on every console page (the drawer keeps
  its `<img>`), `release` from `{% entrance_release space.key %}`; the context bar's status line.
* `apps/accounts/signals.py` (`consume_space_release`, `LUME_SPACES_KEY`) and `apps/accounts/templatetags/entrance.py`:
  once per space per session; a new sign-in starts the list again.
* `templates/components/loader.html`: the comment — «never on a public page» revoked (C5).
* `templates/documents/requirement_detail.html`: the version's «Télécharger» link carries `data-loader="none"` (a file is
  not a page: nothing would end the threshold). One attribute; the file has no lane owner in §10.0.
* Budget paid by deletions: `static/css/_legacy-tokens.css` (56 names nothing reads: 138 → 82),
  `static/css/v4/tokens.css`, `v2/tokens.css`, `v5/aliases.css` (37 dead declarations), `base.css` `.t-secondary`,
  `layout.css` `.section--flush-top`. Docs kept true: `docs/design/DESIGN_SYSTEM_2026.md` §2 (the new layer, three
  weights), §12 (the six keyframes), §16 (head.js), §17 (the shim's rows and census), the shim's ceiling in
  `tests/frontend/test_legacy_token_shim.py`.
* `docs/design-v5/DECISION_LOG_V54.md`: **DL54-163** — DL54-07, MS-O3, K17 amended (C5); index row added. The steward
  renumbers at merge if needed.
* `docs/design-v5/COMPONENT_PROVENANCE.md` (new, lane A): rows Loader (21st 16834) and Page transition (21st 1033).
* Dist rebuilt with the repository's `npm run build` (no new package; `node_modules` junctioned from design-v5's).

## Budgets (measured, gzip -9 on the built files)

| Asset | Before (e047fae) | After | Limit |
|---|---|---|---|
| `static/css/dist/main.css` | 31 244 B | **31 233 B** (−11) | ≤ 31 414, no rise |
| `static/js/dist/shell.js` | 3 785 B | **4 359 B** | ≤ 4 700 |
| `static/css/dist/portal/console.css` (console pages only) | 7 116 B | 7 759 B (+643: the console's half of the threshold, the plate, the stills) | page-only, ≤ 6 KB each partial: `_motion.css` ≈ 0.6 KB gzip |
| JS chunks | 5 | 5 (no new request: the threshold is inlined into shell.js) | — |
| HTML per page | — | + the layered mark (≈ 1.4 KB raw, ≈ 0.5 KB gzip) in the letterhead; + one per console tile | — |

No animation library, no new npm dependency, no React. CLS: the layered mark is absolutely positioned over the `<img>`,
which keeps its box (no layout change); the line and the legend are absolutely positioned in the band.

## Measured on 8783 (Chromium 153 headless; scripts and captures in `C:/tmp/ile_v5_council/.work/v512-a-w1/`)

* Threshold, held answer (a 204 after 1.6 s, so the page stays and can be read): fr/ar × 1440/390, the console at
  1440 (fr) and 390 (ar): `is-departing`, line `lume-line` 0.9 s at `matrix(0.85, …)`, origin `0px` (fr) / the right
  edge (ar), key `sig-turn` 0.48 s, word «Chargement…» shown; after the 10 s lease: quiet. Reduced motion: `lume-fade`
  0.08 s, line at 0.85, light 1, ink 1, key 0 s. Keyboard: line and key 0 s. Fast (0.2 s): nothing. Error page (404):
  nothing. (`shots/probe204.json`, `shots/threshold-*.png`.)
* The arrival after a slow real navigation (2.8 s through a local slowing proxy): the next page has `lume-arrive`,
  `lume-arrive` on the light (reduced: `lume-still`).
* View Transitions (`pagereveal`): pointer home → FAQ: a transition; keyboard: none; reduced motion: none; fr → ar: a
  transition with `vt-lang` (the mark keeps no name), removed when it is over; login: the letterhead `none`, the door
  `ile-mark`; public → console: a transition, the rail's tile named at 1440, the top bar's at 390.
* Release: rail tile 40 px / bar tile 32 px; plate opacity .99 at 150 ms, 1 at 500, .9 at 900, 0 at 1 400; light 1 → 0.
  Second visit 0; the company space's first page 2 (rail + bar), its reload 0. Reduced: `lume-still` on light, ink and
  plate, opacity 1 until 1.2 s, 0 at 1.4 s.
* Boxes: the layered mark and the `<img>` coincide exactly (fr 1440 `[100, 45, 38, 38]`, ar 390 `[142.5, 9, 38, 38]`).

Note for whoever measures this again: Playwright (and raw CDP) cannot evaluate or capture a page whose navigation is
pending in this environment (the protocol waits for the commit, while the page's own script runs — checked with
beacons); hence the held-204 method and the arrival class.

## Tests (lane l3: `TEST_DATABASE_URL=…/test_ile_v5_l3`)

* New: `tests/frontend/test_lume_v512_a.py` — 17 (11 static/client, 6 browser).
* Updated (stale by the change, no guard weakened): `test_loader_rules.py` (motion.css in the loader's sheets; the
  allow-list admits the letterhead — C5; the seat test: the mark in layers on every console page, release only from
  the flags; the opt-out test reads the new hook order; the stills' `--motion-reduced` only inside reduced blocks),
  `test_loader_w1_d.py` (the second console page carries two layered marks and the drawer's `<img>`; the plate's
  phase; under reduced motion the release is the lit still), `test_reduced_motion_w1_d.py` (admits the loader's stills
  — `lume-still` / `lume-fade`, opacity only, exactly `--motion-reduced`), `test_v5_tokens.py` (`--lume-still` kept
  under the setting; a reduced-motion animation must have opacity-only keyframes), `test_documents_w3_c.py` (the
  download link's `data-loader="none"`), `test_legacy_token_shim.py` (ceiling 138 → 82).
* Runs: `tests/frontend apps/accounts/tests -m "not browser"` — **2 363 passed, 2 xfailed** (the two standing
  markers), 476 deselected; browser:
  `test_lume_v512_a.py`, `test_loader_w1_d.py`, `test_reduced_motion_w1_d.py` — **36 passed**.

## New translatable strings (for lane D)

| msgid (fr) | Where | Suggested (provisional, DECISIONS §1 T2) |
|---|---|---|
| `Chargement…` | `templates/partials/header.html`, `templates/partials/portal_chrome.html` (`data-lume-word`) | it «Caricamento…» · en «Loading…» · ar «جارٍ التحميل…» |

## Requests to other lanes

* **B** — `templates/community/discussion.html`: the attachment's «Télécharger» link (`{% url 'documents:download' … %}`)
  needs `data-loader="none"` (or `download`), as the version link now has: a file is not a page, and the threshold
  would show for its 10 s lease. The same for W3's `document_row.html` download action.
* **D** — the OUTCOME_BEARING forms (the situation's recalculation, the pre-assessment, an eligibility, a scan's
  verification) carry no `data-loader-action` today, so the threshold — and the arrival's light — play on them. Please
  tag those forms (`data-loader-action="recalculate-situation"` etc.: the list in `static/js/src/loader.js`).
  The release is per `space.key` of `portal.services.shell_space`: when the organisation rails (W2) give institution /
  university their own space key, their first page lights once by itself; no template change is needed.
* **Steward / orchestrator** — DL54-163 may need renumbering; `docs/design/DESIGN_SYSTEM_2026.md` §2/§12/§16/§17 were
  edited for this lane's sheets (no other lane's rows touched).

## Not done in W1 (by the wave plan)

M1–M9, M11–M13 (W2), M15–M18, the command palette, the mega-menu morph, the CTA arrow (W3); `loader.region()` for the
drawer and the depot (W2). The sign-in → console morph is built (names on the door and the tile) but could not be
driven end to end on 8783 (the QA accounts have no usable password); the persona switch's path was measured instead.

## Fixes after review (label v512-a-fix-w1, 28 October 2026)

Three minors from the W1 review; all fixed.

| Finding | Fix | Measured |
|---|---|---|
| `motion.css .lume-word`: at 1440 the «Chargement…» pill sat on the current door's underline («Projet»); at 390 in Arabic it covered the foot of the «القائمة» button | The legend now **hangs under the rule** (`inset-block-start: 100%`, `margin-block: var(--s-2) 0`) at the same inline end, rather than sitting across it (`translate: 0 50%` is gone). It touches no control and no indicator in the band, covers the page's first ~30 px at the inline end only for the length of a wait, and lets every click through (`pointer-events: none`). The console bar's legend inherits this: it hangs under the bar. | On 8783, `/…/le-projet/` with the threshold forced on: legend top 104 / band bottom 97 (fr 1440, fr 1024), 64 / 57 (ar 390, en 390). It intersects neither the current door nor the menu button (`C:/tmp/ile_v5_council/.work/v512-a-fix-w1/probe_word.py`, captures `shots/word_*.png`). The browser tests now assert `wordTop ≥ bandBottom` (fr 1440, ar 390, console 390) and that the legend stays on screen. |
| `templates/base.html`: no `<meta name="generator">`. After D's footer change the release number appeared nowhere | `<meta name="generator" content="Italy Legal Entry™ {{ site.version_label }}">` added after the description | Served: `Italy Legal Entry™ v2.0.0 — Fase 1`; test `test_every_page_names_its_release_in_the_head` |
| `static/js/head.js`: the render-blocking script had grown from 919 to 2 067 B gzip (4.9 KB raw) and was not minified | Its commented source moves to `static/js/src/head/head.js`. `scripts/build_frontend.mjs` minifies it with the existing esbuild step (no bundling, still a classic script, a one-line banner naming the source) into `static/js/head.js`, which base.html loads as before | **2 022 B raw / 924 B gzip** (was 4 882 / 2 059 B with this machine's `gzip -9`). Test `test_head_js_is_served_minified_from_its_source`: banner, no other comment, classic script, not older than its source, ≤ 1 000 B gzip. `test_lume_v512_a.py`'s static checks read the source. DS 2026 §16 row and ASSET_REGISTRY updated |

**Budget.** The legend's new placement cost +5 B gzip on `main.css`. Three more dead shim names paid for it:
`--tracking-tight`, `--tracking-button` and `--tracking-eyebrow`, which nothing reads (ceiling 82 → 79; DS 2026 §2,
§17 and two historical sentences now name the `--tracking-*` family). The empty `scaleX(0)` rest state of the band's
line also went, because the line is not drawn at rest (`opacity: 0`) and the keyframe starts from `scaleX(0)`.
`static/css/dist/main.css` **31 168 → 31 149 B gzip** (this machine's `gzip -9`; the same build measured 31 233 B in
the table above with the earlier tool). `regen_design_inventory.py --write` brought §2/§16 figures up to date.

**Tests (lane l3).** Non-browser: `test_lume_v512_a.py`, `test_legacy_token_shim.py`,
`test_frontend_bundle_is_current.py`, `test_script_motion_gate.py`, `test_layout.py`, `test_design_docs.py`,
`test_loader_rules.py`, `test_reduced_motion_w1_d.py`, `test_css_tokens_exist.py`, `test_v5_tokens.py`,
`tests/test_regen_design_inventory.py`: **731 passed, 1 xfailed** (the standing `test_the_shim_is_gone`). Browser (one
Chromium, under the machine's lock): `test_lume_v512_a.py` **6 passed**; `test_reduced_motion_w1_d.py::test_head_js_writes_the_input_modality`
and `test_motion_browser_w4_b.py`: **16 passed**.

**Still for lane D.** In Arabic the legend still reads «Chargement…» until the msgid gets its translation (see the
table above).
