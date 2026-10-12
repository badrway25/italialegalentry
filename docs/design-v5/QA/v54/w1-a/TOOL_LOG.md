# W1-A · tool log

Every call of the design tools made by the family, in order (plan §5.1 step 2: «The calls are logged»). Label of the
caller in brackets. Times are Rome, 5 October 2026.

## UI-UX-Pro-Max (skill 2.13.0, local search over its CSV knowledge base; nothing leaves the machine)

Used as plan §5.4 says: on the family's *current* implementation, to rank weaknesses and pick the strongest fix — never on
abstract alternatives. Its own design-system output proposes a palette and a typeface (Atkinson Hyperlegible, a Google
Fonts `@import`): neither is taken — the family's faces and colours are the council's decisions (§1.1, §1.2), and a
hotlinked font is forbidden by the CSP and by the standing rules. What is taken is the guideline layer, read against
the measured audit below.

| # | Time | Call | Returned (top result) | Used for |
|---|---|---|---|---|
| 1 | 07:15 | `search.py "government legal service institutional" --design-system -p "Italy Legal Entry"` [w1-a-impl-1] | style «Accessible & Ethical» (government, legal compliance): 16 px+ text, visible focus, 44 × 44 targets, reduced motion; anti-patterns «ornate design», «AI purple/pink gradients» | confirms the direction of §1.2 (no violet: «En examen» leaves the wisteria) and §1.6; palette and font proposals not taken (see above) |
| 2 | 07:16 | `search.py "input font size zoom mobile" --domain ux -n 3` | «Readable Font Size: minimum 16px body text on mobile» (High); «Font Size Scale: consistent modular scale» | weakness W3 below (fields at 15 px) → typed text 16 px at every width |
| 3 | 07:16 | `search.py "line length measure readability" --domain ux -n 3` | «Line Length: 65–75 characters» · «Line Height 1.5–1.75» · «Heading Line Balance» | measures in rem (36 rem ≈ 70 characters at 17 px; TR C1) |
| 4 | 07:16 | `search.py "focus ring visible keyboard" --domain ux -n 3` | «Focus States: a visible ring on every control» (High) · «Focus Not Obscured (Minimum), WCAG 2.2 AA: scroll-padding» | the one focus system (§1.6); `scroll-padding-block-start` kept in V1 base.css |
| 5 | 07:16 | `search.py "color not only status indicator" --domain ux -n 3` | «Color Only: use icons/text in addition to colour» (High) | the eight registers keep word + mark + edge style (C3) + pattern (C4) |
| 6 | 07:16 | `search.py "touch target size spacing" --domain ux -n 3` | «Target Size (Minimum) WCAG 2.2 AA: 24 CSS px» · «44pt iOS / 48dp Android» · «8 px between targets» | the control tokens of §1.8 (24 fine / 44 coarse and primaries); `--hit-min` kept at 44 for the V4 controls until W1-C |
| 7 | 07:16 | `search.py "font weight hierarchy" --domain typography -n 3` | single-family systems (Outfit, Plus Jakarta Sans): weight as the hierarchy | confirms one family + weight as the axis (500 acts, 400 reads, 600 titles); the faces themselves not taken |
| 8 | 07:16 | `search.py "border radius consistency" --domain style -n 3` | **0 results** — no database match | retried once (#9) |
| 9 | 07:17 | `search.py "corner radius" --domain ux -n 3` | **0 results** — no database match | stated as such; the corner scale rests on the plan's evidence (BX §4.2, TS §24), not on this tool |
| 10 | 07:17 | `search.py "shadow elevation depth" --domain ux -n 3` | one VisionOS result (glass and z-offset) | not applicable to the web product; not used |
| 11 | 07:17 | `search.py "font loading swap layout shift" --domain ux -n 3` | «Font Loading: reserve space with a similar fallback; font-display swap» · «Content Jumping» (High) | the metric-matched fallbacks (Windows, Arial for Apple, Roboto for Android, the wordmark, ILE Mono) |

**The audit it ranks** — measured, not opined: computed styles of every visible text node and painted box on lane 3
(8783), the current product at `v54/base`, fr and ar, 1440 × 900 and 390 × 844 (`evidence/v54/w1-a/before-lane/audit.json`,
tool `evidence/v54/w1-a/tools/audit_pages.py`). Ranked by reach × severity:

| # | Weakness (current product) | Measure | The fix built in W1-A |
|---|---|---|---|
| W1 | Font payload | home 306 KB fr / 519 KB ar; login and dashboard 219 KB fr / 488 KB ar; 4 families on the home (Newsreader, IBM Plex Sans, Segoe UI for «ع», IBM Plex Mono) | type «Una voce»: five files, two to three per page |
| W2 | Console text too small | dashboard: 57 % of text nodes under 14 px, 12 nodes at 11 px; documents: 65 % under 14 px, one node at 9.36 px | the eyebrow and count at 12; the console one step up below 48 rem or under a coarse pointer; never under 12 px Latin, 14 px Arabic |
| W3 | Typed text at 15 px | login `login`, `password`; the documents search | typed text 16 px at every width |
| W4 | Too many sizes, line-heights off the 4 px line | home: 11 distinct sizes (11 … 75.84 px), 20 line-heights off 4 px; login: 11 off; dashboard: 18 off | eight public sizes; line-heights on the 4 px line in the tokens |
| W5 | Corners | 10 / 14 / 20 / full on the home's first screen; dashboard 10 / 14 / 6 / full | «Lo spigolo» 2 · 4 · 6 · 8 · 12 · full on the existing names (the per-screen fold is counted on the boards) |
| W6 | Shadows | 4 distinct shadow values in the dashboard's first viewport, one a 6 px laguna ring used as a shadow | five levels in the night's colour; the glow retired; SH-8's caps checked on the boards |
| W7 | Focus | three ring styles on one page (navy two-tone in V1, laguna + halo in V2–V4, button-specific) | one focus system: 2 px laguna ring, halo on text fields only |

**The re-audit after the fixes** (plan §5.4: «at the start and again after the fixes»), the same script on the same
pages and on seventeen more (`E/after-2/`, `E/after-3/`, `E/after-sweep/`, `E/after-6/`):

| # | Status after step 1 | Measure |
|---|---|---|
| W1 | fixed | fonts 20 956 B on a Latin public page, 23 644 B in the Latin console, 53 184 / 55 872 B on Arabic pages — inside 25 / 32 / 56 KB |
| W2 | fixed for the type system; two seats left to their families | 0 Latin text nodes under 12 px on the dashboard, the documents and the case file at 1440 (V4: 12 at 11 px); the phone console's bottom bar at 12 px in Latin; its Arabic labels and the lock-up's ™ (brand drawing) remain |
| W3 | fixed | typed text 16 px on the login, the signup, the contact form, the documents search |
| W4 | the tokens fixed; the page sheets' own literals remain | home 10 sizes at 1440 (V4: 11); the forum page 15 (its own sheet, W3-F) |
| W5 | the scale fixed; the per-screen fold pending | 2 · 4 · 6 · 8 · 12 · full only; four values on the home's first screen and the console screens — folded on the boards and in the three-screen comparison (step 2) |
| W6 | the levels fixed; the caps are the console families' | dashboard 4, case file 5 shadow values in view (unchanged count, V5 levels) |
| W7 | fixed globally; component rules left to their families | one ring (laguna-550, 2 px at 2 px), the halo only on text fields; the buttons' and fields' own focus rules are W1-C's |

## 21st.dev

Not used. The brief (§1, «How it enters») records it: W1-A has no component — tokens, faces and type roles are not
React components — so there is nothing to search, shortlist or get. No `search`, `get_component`, `generate`,
`iterate`, `bookmark`, `submit`, `edit` or `delete` call was made.

## The Emil principles

Plan §5.4: the flagged skills are not invoked; their written rules in MOTION_SYSTEM and EMIL_SKILL_INTEGRATION apply,
as the review checklist. For a foundation family the items that bear are hierarchy, spacing and typography (the type
roles, the weights that act / read / title, tracking by size), and — for the motion tokens W1-A declares and W1-D uses —
timing (no duration changed), the one key-turn curve (`--ease-turn`), the reduced-motion state (the zeroing restated in
v5/tokens.css, `--motion-reduced` 80 ms). Origin, interruption, press and the tooltip group belong to W1-C, W1-D and W2-A.

## Step 2 — tests and docs (5 October 2026, w1-a-impl-2)

No design tool was called: the step retargets tests and writes documentation, and no surface changed. No UI-UX-Pro-Max
search (its audit and re-audit are step 1's, above), no 21st.dev call (W1-A has no component), no skill invoked. The
figures written into DS 2026 §5 were computed from the cascade by the family's own test module
(`tests/frontend/test_v5_tokens.py`), through a scratch generator outside the repository.

## Step 3 — finishing for shipping (5 October 2026, resumed 8 October; w1-a-impl-1)

No design tool was called: V5.5 delivery mode (implement → one review → fix → ship) — the step merged design-v5, closed
G-15, measured the CSS bytes and ran «no page worse» on the 316 pairs, then the targeted suites. The two corrections of
`v5/base.css` (`9512bea`) came from the sweep's own counts, not from a tool. No UI-UX-Pro-Max search, no 21st.dev call
(W1-A has no component), no skill invoked. The record is `NOTES.md`.
