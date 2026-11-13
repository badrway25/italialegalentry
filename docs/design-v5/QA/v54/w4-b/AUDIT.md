# W4-B — Motion audit (read-only pass, before any change)

16 October 2026 · w4-b-impl-1 · design-v5 at `8ab5b89` (integration checkpoint 3; Wave 3 merged except W3-E) ·
plan §3.6 item 2, §1.5, §2.6 «Motion», K17.

*Corrected after the review and the accessibility check (w4-b-fix, the same day): four lines this pass marked
compliant were not — marked ✗ (§11) below, each with its fix in §11.*

**How it was measured.** The lane (8788, `ile_v5_l8`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
`--noreload`), one headless Chromium, a fresh context per load. An instrument injected before the page's own scripts
(scratch, never shipped) records every CSS transition and CSS animation (`document.getAnimations()` polled each frame,
plus `transitionrun` / `animationstart`) and every Web Animations call (`Element.prototype.animate` wrapped), with its
target, duration, delay, easing and properties, phase by phase: the load, then each gesture of the plan. 1440 × 900 and
390 × 844 (touch), the setting on and off (`emulateMedia`, never the preview's flag), French everywhere and Arabic for
the home, the login, the dashboard and «Ma situation» — 68 loads, 0 console errors (the 404 page's own 404 apart), 0
CSP reports, at rest after every load **0 running animations and 0 `will-change`**. Sessions minted with
`Client.force_login` on the lane's clone (no password); a fresh session per console load, so the entrance release is
seen where it plays. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-b/audit-base/` (one JSON + captures per load),
`extra-base/` (the skip link, the panel's Esc, a dialog), `rail-r10/` (the rail's frames at CPU × 4). The static read
covers every `transition` / `animation` / `@keyframes` of `static/css/**` and `apps/*/static/**` (249 declarations,
`.work/w4-b/w4-b-impl-1/css_motion.txt`) and every motion call of `static/js/src/**` and `static/js/main.js`.

Tiers (plan §1.5): 0 static (every keyboard-initiated change) · 1 micro ≤ 120 ms · 2 state ≤ 320 in / ≤ 200 out, a
sequence ≤ 600 · 3 signature (L1, the filed mark, the journey light) · 4 one immersive public moment ≤ 5 s. A
reduced-motion still = one opacity ≤ 80 ms and no transform, or nothing.

## 1. Every public page — the chrome («Il portico», the sheet) and the shared controls

| What moves | When | Tier | Duration · easing (tokens) | Reduced motion | Verdict |
|---|---|---|---|---|---|
| L'architrave (the one indicator) | load: first placement, no travel (`is-jump`), an opacity fade; pointer: travels between doors | 1 | fade `--motion-fast` linear · travel `--spring-snappy` (470 ms twin) | `transition: none` (nothing) | ✓ one indicator per page (MS-O3); **from the keyboard its 120 ms fade still plays (F4)** |
| A door's panel (≥ 64rem) | pointer intent / click | 2 | in `--motion-standard` `--ease-enter` from −8 px; out `--motion-fast` `--ease-exit`; entries staggered 30 ms (≤ 350 ms) on the first pointer opening | one opacity of `--motion-reduced` | ✓ ceilings; keyboard opening instant (`is-instant`); **✗ the exit's curve: `--ease-exit`, where MS-O2 has a small surface leave on `--ease-enter` (§11, F9)** |
| The panel closed by **Esc** / Tab out | keyboard | must be 0 | runs the 120 ms exit and the chevron's 200 ms turn (measured, `extra-base/portico-esc-fr-1440`) | nothing | **✗ tier 0 (F4)** |
| The door's chevron | open / close | 1–2 | `--motion-standard` `--ease-layout` | zeroed token (nothing) | **✗ not zeroed from the keyboard (F4)** |
| The photograph of a door panel (≥ 80rem) | panel open / switch | 2 | `--motion-standard` `--ease-enter` cross-fade | 80 ms opacity | ✓ |
| The phone sheet («Menu», < 80rem) | tap | 2 | 320 ms in (`--motion-emphasized`, `--ease-enter`, body and foot translate 12 px), scrim with it; out `--motion-standard` | one 80 ms opacity, scrim too | ✓ (measured 320 ms; 80 ms opacity under the setting) |
| The sheet's doors (`<details>` chevron) | tap | 1–2 | `--motion-standard` `--ease-layout` | nothing | ✓ |
| The sheet closed by Esc | keyboard | 0 | 0 ms (`html[data-input="key"] .overlay`) | — | ✓ |
| **The skip link** | Tab (keyboard only) | must be 0 | slides 120 ms (`--duration-fast` → `--motion-fast`, V1 `base.css`) | nothing | **✗ tier 0 (F5)** |
| Links, buttons, fields, cards, chips | hover, press, focus | 1 | colours `--motion-fast` `--ease-enter`; the press at 0 ms released on `--spring-snappy`; the field's focus draw `--field-draw` | tokens zeroed (nothing) | ✓; from the keyboard 0 ms for buttons, fields, tabs and accordions (W1-C's `html[data-input="key"]` rules); **✗ links had no such rule: the console bar's trail ran its 120 ms colour fade from Tab (§11, F8)** |
| Tooltips | hover after the 400 ms wait | 1 | `--motion-fast` opacity; the group warms 400 ms | 0 ms | ✓ MS-O5 |
| `[data-reveal]` (shell.js, Motion's `inView` + `animate` + `stagger`) | scroll into view | — | 320 ms from 12 px, 40 ms stagger, literal values | settled at once | **no element on any page** (templates, CMS content in `ile_v5` and `ile_v5_l8`, the DOM of every page type): dead code that hides text when it runs — **K17 (F1)** |
| `.reveal` (components.css §29 + main.js `initReveal`) | scroll into view | — | `--duration-reveal` (0 ms in the shim) | visible | no element on any page (`components/hero.html`, the only carrier, is included by no template) — **K17 (F1)** |
| Smooth scroll to an anchor | a pointer's anchor click | — | the browser's | `scroll-behavior: auto` (base.css); from the keyboard `auto` (chrome.css) | ✓ |

## 2. The home (`/fr/`, `/ar/`)

| What moves | When | Tier | Duration · easing | Reduced motion | Verdict |
|---|---|---|---|---|---|
| The hero's discovery (E2 desktop / E3 phone): the four named, the path, the arch, the steps, the key's turn, the door ajar | once per session, after the LCP, the door decoded, the hero in view and an idle slot + `--motion-wait` | 4 | one WAAPI clock through `motion.js`'s `play()`: **3 575 ms at 1440 (fr and ar), 2 770 ms at 390**; transform and opacity only | the settled still at once, no replay button | ✓ ≤ 5 s; 0 animation and 0 `will-change` at rest |
| The repeatable flow | hover (fine pointer) / touch on an origin, focus from the keyboard | 4 (short) | ≈ 1 750 ms measured, transform and opacity; the hand's states are CSS at `--motion-fast` / `--motion-standard` | nothing (the CSS states land at once) | ✓ |
| The replay (button over the golden key) | click / Enter / Space | 4 | 3 850 ms (the door closes in 240 ms, then the discovery) | no button | ✓ ≤ 5 s |
| CTA-B «Soglia» | hover / press | 1 | `--motion-fast`, `--motion-standard` on hover | zeroed | ✓ |
| The chapters under the hero | — | — | nothing moves at load or on scroll; the rows' arrows 120 ms on hover | zeroed | ✓ |
| The dismissible notice | click | 0 | none | — | ✓ |

## 3. Door pages, the project, the interior (FAQ, legal, content), errors, the orientation questionnaire

| What moves | When | Tier | Duration · easing | Reduced motion | Verdict |
|---|---|---|---|---|---|
| The chrome of §1 | — | — | — | — | as §1 (F4, F5) |
| The accordion's chevron (FAQ, glossary) | click | 1–2 | `--motion-standard` `--ease-enter` | nothing; 0 ms from the keyboard | ✓ |
| The orientation choices, the help toggle | click | 1 | `--motion-fast` / `--motion-standard` | nothing; 0 ms from the keyboard | ✓ (nothing at load, measured) |
| The 404 / 410 / 403 pages | — | — | nothing | — | ✓ |

## 4. The entrance — «Il varco» (login, sign-up, reset, verification, MFA)

| What moves | When | Tier | Duration · easing | Reduced motion | Verdict |
|---|---|---|---|---|---|
| The arrival: four lights travel into the threshold | once, from outside the entrance, after the door's paint, ≥ 64rem only | 3 | `--motion-route-light` 1 200 ms each, `--motion-route-stagger` 400 ms: **2 408 ms** measured | nothing | ✓ never on the band, a refused sign-in, from history |
| A pass of light (the ways / the frame) | a pointer's focus on the e-mail / the password | 2 | `--motion-slow` 480 ms + `--motion-fast` out | nothing (no pass asked under the gate) | ✓ public lines only use `--motion-slow` |
| The stage's states (pool, threshold, steps, frame) | focus, a valid address | 2 | `--motion-standard` `--ease-sine`, the steps staggered by `--motion-stagger` | zeroed; from the keyboard 0 ms | ✓ |
| L1 engage: the key turns once and holds (the sign-in's submit) | submit | 3 | `sig-turn` `--motion-slow` `--ease-turn`, once | the turned key, still | ✓ nothing loops |
| L2 the busy key of a `.btn` | submit (every form) | 1 | `sig-turn` `--motion-emphasized` `--ease-turn`, then holds; lit at `--motion-fast` | still | ✓ |

## 5. The console shell (every console page)

| What moves | When | Tier | Duration · easing | Reduced motion | Verdict |
|---|---|---|---|---|---|
| **The entrance release** (`lume-light-o`, `lume-light-t`, `lume-ink-o` on the rail's mark) | the first console page after a successful sign-in, once per session | 3 | `--motion-door` 1 600 ms, phase-aligned keyframes | the animations run at 0 ms (the token zeroed): the still | ✓ **the only motion at load on every console page** (dashboard, «Mon parcours», company, «Mes pièces», «Ma situation», the case file: nothing else, fr and ar, 1440 and 390) |
| **The rail's fold** (`body` `padding-inline-start`, the rail's `inline-size`) | the rail control (pointer or keyboard) | 2 | `--motion-standard` `--ease-layout` | zeroed | **✗ R10 and the properties law (F3)**: layout properties; at CPU × 4 the fold runs at 8 frames in 260 ms with gaps of 67–117 ms (n = 5), and `contain: layout` does not save it (9.5 frames, gaps 50–117 ms) |
| The phone drawer («Menu») | tap | 2 | translate 320 ms `--ease-enter`, scrim with it; out `--motion-standard` `--ease-layout` | one 80 ms opacity | ✓; Esc from the keyboard 0 ms |
| The rail's tips, the account popover | hover / focus / click | 1–2 | the overlay system's | 80 ms opacity | ✓ |
| Rail rows, the bottom bar | hover / press | 1 | colours `--motion-fast` `--ease-exit` | zeroed | ✓ the current page is drawn, never travelled to; **✗ the curve: `--ease-exit` into and out of the hover, where MS-O1 / MS-O2 want `--ease-enter` (§11, F9)** |
| `html:has(.console-drawer[open])` (W3-D's O3) | — | — | — | — | **gone with W2-A** (`e5fa845`); measured in NOTES (O3) |

## 6. «Ma situation»

| What moves | When | Tier | Duration · easing | Reduced motion | Verdict |
|---|---|---|---|---|---|
| The question's change («Continuer», «Précédent», the Stepper's links, the hash) | click / tap; **the keyboard too (§11, F6)** | 2 | **through the Motion library** (`animate`): the leaving question's opacity 120 ms, then the arriving one's opacity 200 ms and 16 px in the reading direction (`x`, a JS frame loop, not WAAPI); the `easing:` option is Motion One's name, ignored by Motion 13 (its default ease-out ran); inline styles committed and scrubbed after | nothing (the question swaps at once) | ✓ ceilings (320 ms sequence) — **the library leaves (F2)**; at load nothing moves (the submit's role colour is applied under `transition: none`); **✗ Enter or Space ran the same 120 + 200 ms (tier 0; §11, F6); a return within the leaving fade left no question drawn and the focus on `body` (§11, F7)** |
| The Stepper's current node, a filled node | the change / an answer | 0–1 | `.wstep__link { transition: none }` | — | ✓ |

## 7. «Mes pièces», a piece, the upload (documents)

| What moves | When | Tier | Duration · easing | Reduced motion | Verdict |
|---|---|---|---|---|---|
| The preview drawer (beside the list; a sheet on a phone) | a row's title or act | 2 | translate `--motion-emphasized` `--ease-enter` (320 ms) | one 80 ms opacity | ✓ |
| L3 «seat»: the piece's parts on their first arrival | asynchronous fragment only | 3 | `sig-seat` `--motion-standard` from 4 px, `--motion-stagger` | nothing | ✓ never a server-rendered region |
| The filter's bottom sheet (phone) | tap | 2 | `--spring-sheet` twin (550 ms clock; 92 % of the travel at 275 ms), scrim `--motion-standard` | 80 ms opacity | ✓ the plan's spring twin (§1.5 tokens; DS 2026 §12) |
| The alert dialog (a loose file's deletion) | its «Supprimer» | 2 | the overlay system's dialog (.96 → 1, `--motion-emphasized`) | 80 ms opacity | ✓ by the system (no loose file in the lane's data; the overlay board's tests cover it) |
| The filed mark (the Dépôt) | a filing | 3 | `stroke-dashoffset` `--motion-standard`, the dot `--motion-fast` after | still | ✓ ≤ 240 ms |
| Hover on rows | pointer | 1 | colour, at once | — | ✓ |

## 8. The other console pages (dashboard, registers, «Mon parcours», the case file, the company, the Academy, the help desk, selection)

Nothing moves at load but the entrance release (§5); the journey runs no script and no animation (W3-D); hovers are
colours at `--motion-fast`. `v4/workspace.css` still declares two load animations of V4 (`notch-fill`, `strip-fill`,
behind `prefers-reduced-motion: no-preference`) on `.meter__notch--on` and `.health__segment`: **no page draws either
class** (0 such animations in the 68 loads); the file leaves the cascade with W3-E (in review) — not touched here.

## 9. Script motion outside `static/js/src/` and the gate

| Where | What | Verdict |
|---|---|---|
| `static/js/main.js` `initReveal` | `.reveal` on scroll; reads the media query itself | **dead + K17 (F1)** |
| `static/js/main.js` `initCounters` | count-up with `requestAnimationFrame`, outside the gate; reads the media query itself | **dead (no `[data-counter]` anywhere) — W1-D's hand-off (F1)** |
| `static/js/main.js` `initFormErrorFocus` | smooth `scrollIntoView` unless the setting | ✓ the setting honoured (the preview's flag is not the state, plan §1.5) |
| `apps/orientation/static/orientation/wizard.js` | no motion | ✓ |
| `static/js/src/**` | every `.animate(` and frame wait through `motion.js` (`play`, `nextFrame`, `afterPaint`, `tween`, `settled`) — `test_script_motion_gate` green — **except** the Motion library's own calls from `shell.js` and `situation.js` (`animate`, `inView`, `stagger`), which the gate only wraps from outside | **F2** |

## 10. Findings — what this area fixes

| # | Finding | Rule | Fix (the owner family's file) |
|---|---|---|---|
| F1 | `[data-reveal]` (shell.js, Motion) and `.reveal` (components.css §29, main.js `initReveal`) hide text until a script reveals it; `initCounters` animates outside the gate; none has a target on any page | K17; plan §2.3 deletion map; W1-D's hand-off | delete shell.js's reveal, components.css §29 (with `.counter`), `initReveal` and `initCounters`, their DS 2026 §16 rows and §12 sentence |
| F2 | the Motion library (`motion` 13.4.1, a 26.5 KB gzip chunk on **every** page type) is still imported by `shell.js` (the reveal) and `situation.js` (the question's change); the home's script is 51 249 B gzip against §2.6's 45 KB | plan §1.5 «Engine», §2.3, §2.6; DL54-101 item 4 | `situation.js` on `play()` (WAAPI through the gate) with the same clock; `motion.js` without the re-exports; `npm uninstall motion --package-lock-only`; the bundle test rewritten; the dist rebuilt |
| F3 | the rail's fold animates `padding-inline-start` and `inline-size` | §1.5 R10 («ships instant unless `contain: layout` brings it to 60 fps at CPU × 4»: it does not); the properties law | the two transitions leave `_shell.css` (W3-A); the fold is instant |
| F4 | the portico's panel, chevron, door word and architrave keep their transitions from the keyboard (Esc, Tab out, the arrows' indicator fade) | tier 0 (R-07; head.js's rule «each family writes its one rule») | one `html[data-input="key"]` rule in `chrome.css` (W2-C1) |
| F5 | the skip link slides 120 ms on Tab — it is only ever reached from the keyboard | tier 0 | its transition leaves V1 `base.css` |

Everything else meets its tier, its tokens and its still (as this pass measured it — §11 lists what it missed): one indicator per page (the architrave on public pages; the
console draws its current page and moves no indicator); nothing at load in the console but the entrance release;
under the setting every overlay is one opacity of 80 ms and every other motion is gone; nothing loops; at rest 0
animations and 0 `will-change`.

## 11. What this audit missed — found by the review and the accessibility check, fixed after them

The senior review (`REVIEW.md` m1–m4) and the accessibility / performance check (`A11Y_PERF.md` findings 1–3) measured
four things this pass had marked compliant. Each is fixed (w4-b-fix, 16 October 2026; `NOTES.md` «Review fixes»).

| # | Finding | Rule | Fix |
|---|---|---|---|
| F6 | «Ma situation»'s question change asked from the keyboard (Enter on «Continuer», Space on «Précédent», Enter on a Stepper link) ran the pointer's 120 + 200 ms, and the focused question's ring showed ≈ 320 ms after the key — §6 listed the change for «click / tap» only | tier 0 (R-07) | `situation.js` creates no animation under `html[data-input="key"]`: the question swaps in the key's own task, the focus and its ring on it |
| F7 | A change asked within the leaving fade («Continuer» then «Précédent» 40 ms later; the Stepper's Q3 then Q1) left no question drawn and the focus on `body`: the first change's late step hid the question the second had shown | the pattern «wizard»: one question, always | each change takes a turn and a late step whose turn has passed does nothing; a change asked in flight lands the earlier one (its animations cancelled, no inline opacity) and plays its own arrival only |
| F8 | Plain links had no keyboard rule: the console bar's trail ran the links' 120 ms colour fade when Tab focused it — §1 credited W1-C's rules, which cover buttons, fields, tabs and accordions | tier 0 | `html[data-input="key"] a { transition-duration: 0ms; }` in `v5/base.css` |
| F9 | `--ease-exit` outside its one role in ten declarations — the portico's pointer exit (it held near-full opacity for its first ~40 ms), the menu items' and the close control's hover colours, the rail's rows, tools and foot, the phone bar: the superseded council table's curve | MS-O1 / MS-O2 | `--ease-enter` in each; the two hover rules that only switched the curve back lose that clause |

With these, every keyboard-initiated change measured on the lane is static — the hero's origin light on a key focus
apart, by W2-D's documented decision (`A11Y_PERF.md` O4) —, and no sheet names `--ease-exit` but the token files: no
object crosses the view today.
