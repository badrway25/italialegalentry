# W1-A · Foundation — the brief

**Executive Creative Director (label w1-a-brief) · 5 October 2026.** Plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.3
item 4, run through the loop of §5.1; DL54 binds where it differs from an older rule. Branch `v54-w1-a` from `v54/base`
(`f11d131`); merge tag `v54/w1-a`, checkpoint `v54/w1-a-pre-propagation` (DL54-01). Nothing here is an option: it is
what we build. P/ = `C:/tmp/ile_v5_council/proof/`, E/ = `C:/tmp/ile_v5_council/evidence/v54/`.

## 1. The direction

- **Type «Una voce»** (§1.1). Host Grotesk variable 400–700 for everything, preloaded; Host italic 400 on use, for titles
  of acts cited in sources only; «ILE Wordmark» (Newsreader 600, 11 code points) for every rendering of the name; «ILE
  Mono» (the Plex Mono 400 subset, renamed for the RFN) for references, hashes and rule versions; Vazirmatn 400–700 for
  every Arabic role. Public sizes 64 · 36 · 28 · 20 · 17 · 15 · 13 · 12: display `clamp` 40 → 64 at 500, −0.026 em at 64;
  titles 600, with tracking that stops at 20 px; reading 400; leading on the 4 px line. Console `--u-*`, eyebrow and count
  at 12, one step up below 48 rem or under a coarse pointer (16 · 15 · 14 · 13 · 12). 500 acts, 400 reads, 600 titles;
  measures 36 rem at 17 px, 29 rem at 15; typed text 16 px at every width; never under 12 px Latin or 14 px Arabic; Arabic
  titles 600 without ×1.15, leading 1.35–1.4, body 1.75, console 1.7. TY-2, TY-3, CDV law 2's serif clause and HET §0
  item 9 are retired (DL54-10). Neither the A-bis test nor the French-spacing filter is ours (W2-E); locked copy is never
  altered.
- **Colour** (§1.2). «En examen» in lapis `#5278c1` (C1): the nine wisteria primitives go, no violet is left. C2 the
  information notice on the slate wash · C3 attesa dashed and nullo dotted at step 600 · C4 the hatch at α 0.78 · C5 the
  night marks re-solved · C6 kept as a rule · C7 the glass at 0.94 · C8 «argento» `#d9dee6` for Istituzione, kept only if
  design and taste read it as a hue on night beside the other three (else the nearest hue that passes that reading and the
  separation check; the hero's set wins) · C9 literals become named tokens. Registers: conforme ink, a plain disc with no
  glyph · esame lapis · neutro slate · attesa amber · azione terracotta · rifiuto garnet, struck · blocco graphite, `lock` ·
  nullo ash. O14 VALIDE in ink, no check anywhere · O57 no tricolour filet · O19 Persona on sand · brand colours declared
  once, in `v2/tokens.css` · «soon» amber, «overdue» terracotta, never red, never without its glyph.
- **Corners «Lo spigolo»** (§1.3, DL54-14). 2 · 4 · 6 · 8 · 12 · full on the existing names: `xs` insets · `sm` buttons,
  fields, tooltip, the hero's plates · `md` the targa, menu rows, the segmented track · `lg` cards, panels, popovers · `xl`
  dialogs, drawers, sheets · `full` chips, counts, indicators — never a button or a card. Concentric nesting; 21 : 9 bands
  at 0; the arch the only large curve; **at most three distinct radii on a screen at rest** — a fourth folds into a role
  already on it.
- **Spacing and shadow** (§1.4). SP-1–SP-8, RH-1–RH-8, SH-1–SH-9 binding: the 4 px scale, groups ≥ 2.5 × apart, one
  padding per component; five shadow levels in `rgba(7, 18, 38, α)`, hairlines before boxes, no glow, glass on the two
  sticky bars only (blur 12, α 0.94), every primary flat; the lit arris on night plates only (DL54-13).
- **Focus** (§1.6). `:focus-visible` only: a 2 px `--focus-ring` (laguna-550) at a 2 px offset on the element's radius ·
  laguna-400 on night · two-tone on photographs · the 5 px halo on text fields only · `Highlight` in forced colours ·
  never animated · ≥ 3 : 1 against both neighbours on every ground. The 200 ms drawn rule belongs to the field (W1-C).
- **Tokens others apply.** Control heights (§1.8): `--control-sm` 36 · `-md` 44 · `-lg` 52 · `-icon` 40 / 44; hit floors 24
  fine, 44 coarse and for primaries — W1-C applies them. Motion (§1.5): the tokens enter `v5/tokens.css` as decided (no
  duration changed; `--motion-reduced` 80 ms and `--ease-turn` added; the reduced-motion zeroing with them); the rule's
  use, the universal block's deletion and their tests are W1-D's.
- **How it enters** (§2.1, §2.3). In place, alias-first: `main.css` imports `v5/fonts, tokens, aliases, base` after
  `v4/*`; a regression is fixed in `v5/aliases.css`, never in a template. Until its own family passes, a page is «V4 +
  fondation», never shown or reported as V5; Wave 1 sends the owner no report (§6). 21st.dev is not used: no component.

## 2. Slice, pages, work

**Slice** (`OWNERSHIP_V54.json` → `w1-a`; `scripts/check_ownership.py w1-a v54/base` before every hand-over):
`static/css/main.css`; `static/css/v5/{fonts,tokens,aliases,base}.css`; `static/fonts/v5-*`; `static/fonts/licenses/**`
(each family's OFL text, IBM's notice kept for ILE Mono); `templates/base.html` (head, preloads); `scripts/build_css.mjs`
(the `_` rule); `templates/dev/designpreview/specimens/{type,colour,corners}.html`; the W1-A row of the deletion map
(`fonts.css` and the V4 woff2; what `v5/aliases.css` re-declares in V1 `tokens.css`, `v2/tokens.css` — brand colours kept —
and `v4/tokens.css`; the adopted names of `_legacy-tokens.css`; V1 `base.css`'s type roles, links, digits and focus); the
W1-A rows of §2.7 and new `tests/**/test_*_w1_a.py`; DS 2026 §2 (prose), §5–§8, §12, §17; `docs/design-v5/FONTS_V5.md`;
this folder; DL54, append-only.
**Pages**: all of them, re-valued at once — the 79 entries of the W1-0 set (`E/w1-0/before/PAGE_TYPES.json`: 31 public
pages and the open navbar, 11 account, 4 error, 29 console, 3 staff), fr and ar; the boards at
`/__design-v5/specimens/{type,colour,corners}/` on 8783.
**Work**: audit (≤ 20 %: UI-UX-Pro-Max on today's type, colour and corners in the product; the Emil checklist) → fonts,
tokens, base, the three boards → self-scores ≥ 4 → council on the boards → checkpoint tag → propagation (`main.css`) →
«no page worse» on every page, re-measured → the steward's merge. LF bytes; real templates, live copy only.

## 3. The boards that are scored (§3.1 item 6)

| Board | What it shows — real faces, live copy (French verbatim, Arabic as served), CSP-clean | Signature for the swap test |
|---|---|---|
| `type` | each face in its role; the eight public sizes with leading and tracking; the console scale and its step up; weights by role; both measures; a 16 px typed field; ILE Mono on a reference as the product prints it; the Vazirmatn roles; the 64 px display line on stills at 1440 and 390 | the wordmark beside Host; ILE Mono in its one seat |
| `colour` | the eight registers on paper, white and night, with edges and marks; hatch; notices; the four audience accents side by side on night (C8); glass over the night hero; the focus ring on every ground; the contrast table | «I cerchi · Il registro»: ink, lapis, notte — no violet |
| `corners` | the six roles on their elements; concentric nesting; the owner's arch beside a 21 : 9 band (photographs from the product's own set, O54 / O55); the five shadow levels; hairline against box; the lit arris on a night plate beside a flat primary; control heights and paddings; the radii count | «Lo spigolo»: few corners, the arch alone large |

The corner comparison (§1.3): the home's first screen, «Mes pièces» and the login, in the adopted scale and in «Lo
spigolo», radii counted, recorded in this folder — an internal check, not an option.

## 4. Acceptance — the gate (§3.1, §3.3 item 4)

| Item | Target |
|---|---|
| Six scales | on each of visual, premium, originality, UX, mobile, coherence, the **lowest** chair ≥ 4 — boards at the standard set, phones emulated |
| Taste | 0 F on the eighteen, portrait A «no», ≤ 1 P\*, the swap test on every still with its signature named, brochure ≤ 2 / 11, TS §21.2 with no «No» on Q1, Q4, Q9, Q10 and ≤ 2 «Partly» |
| Contrast | ≥ 400 pairs on the effective cascade (`test_v5_tokens.py`), 0 below their minimum — PC §6.3's 23 answered by C3, C4, C5, C7 or barred by C6's rule: C3 3.13–3.96, C4 3.04, C7 «Italy» 4.61 on night; C5 0 of 28 night pairs under 0.05; C8 read as a hue |
| Type | ≤ 8 public sizes; nothing under 12 px Latin or 14 px Arabic; typed text 16 px; console text under 14 px ≤ 33 % with the step up |
| CLS | font swap ≤ 0.01 (Windows and Android fallbacks; Apple's before the milestone); ≤ 0.10 every page, ≤ 0.05 flagships (DL54-04) |
| Fonts | per page ≤ 25 KB Latin public · ≤ 32 KB console · ≤ 56 KB Arabic (today 218–304 KB and 484–525 KB); preloads ≤ 2 Latin, ≤ 3 Arabic; `FONTS_V5.md` with sources, commands and hashes |
| CSS, Wave 1 | page-type total ≤ before + 8 KB gzip: home 47 306 · door 44 486 · interior 44 486 · login 45 694 · dashboard 49 860 · «Mes pièces» 51 031 · case file 49 860 B; `dist/main.css` ≤ 45 KB (today 36 294 B) |
| Coherence | off-token radii 0; ≤ 3 radii a screen, by script on every capture; gaps on the scale ≥ 95 % public, ≥ 90 % console; ≤ 4 shadow values a viewport; SH-8's caps |
| Accessibility | PASS: keyboard fr and ar, axe, contrast, forced colours, reduced motion by `emulateMedia`, 400 % reflow, 1.4.12, SP-8 targets, focus never obscured |
| Performance | PASS on 8782 by the Performance Lead under the lock, n ≥ 9 interleaved: LCP ≤ 2.5 s; per before cell LCP ≤ +50 ms and first-render task ≤ +30 ms (24 cells, n = 9, `E/w1-0/before/runs/traces.jsonl`); CSS + JS requests ≤ before |
| Health, tests | 0 CSP, 0 console errors, 0 overflow 320–1920 px; §2.7's W1-A row green — `-m "not browser"` in full, the seven browser files, showcase, shim — at 0 skips. The 27 failures and 2 skips of `v54/base` are not ours: merge design-v5 when its clock fix lands |

## 5. «No page worse than before» — blocking

Every page type of the W1-0 set × fr, ar × 1440 × 900, 390 × 844 = **316 pairs**. By eye the design chair marks each
better / same / worse; **one «worse» blocks the merge** until it is fixed in the aliases. Automated: `compare.py` (in
`E/w1-0/before/tools/`) on an after-set taken with the same `capture.py` and `health.js` on 8782, switched to this worktree
by the Performance Lead (`ile_v5_perf`, 3 October): overflow, clipped text, overlapping targets, axe contrast failures,
missing focus indicators, CSP violations and console errors may not rise in any cell; CLS by ≤ 0.001. Before, from the
raw records (`runs/captures-s{0,1,2}.jsonl`, 277 cells): overflow 0 · clipped text 72 · overlapping targets 32 (80 across
a fixed layer) · contrast failures 4, one element — the forum-register eyebrow, `#d3d2cc` on `#f4f3f0`, 1.36 : 1, W3-F1's
sheet · target-size 4, the login's reset link (W2-B) · focus missing 0 · CSP 0 · console errors 0 beyond the pages' own
403 / 404 / 410 / 503 · CLS ≤ 0.0296.
**Open, for the steward — it blocks the check, not the build.** The capture series stopped at 04:43 after 559 and 557 of
636 captures per shard: academy-enrolment, the four company pages, org-bridge and the three staff pages have none,
academy-mine one of its four cells — 39 pairs. `MANIFEST.json` (03:45) predates 976 captures: it holds 34 of the 316
cells, its README's totals (9 clipped, 4 overlapping, 0 contrast) describe that partial state, and `compare.py` skips a
cell it cannot find. The set is completed and the manifest rebuilt (`build_manifest.py`) before the check runs.

## 6. References (§3.1 item 5) — side by side with the boards, at 1440 and 390

| Reference | The reference for | Not taken |
|---|---|---|
| **GOV.UK** — the home, the visa guide, the task list | legibility as the floor: one sans doing all the work, reading at 19 px; a state is a word — the finished task in «black text with no background colour», O14's precedent and conforme's ink; a focus that is never lost; flat primaries | the crown, the typeface, the blue, the square corner — the State's clothes; display at 700 |
| **Collège de France** | institutional colour and restraint: warm paper `rgb(245, 244, 239)` and warm ink `rgb(61, 56, 52)`, never black; one corner (5 px), no shadow; numbers set as type — the agenda's date blocks | its serif voice (retired under B); text on a façade (O54) |
| **Mercury** | premium carried by a grotesque alone: display at weight 480, body 16 / 1.5 — B's display line; night grounds that are not black, `rgb(23, 23, 33)`; hairline panels, no shadow; 4 and 12 carrying most corners | glass buttons, centred headlines, the rendered landscape, pill navigation |

Captures in `P/research/benchmarks/external/`: `public-digital-service/gov-uk`, `gov-uk-task-list`, `gov-uk-skilled-worker`;
`premium-institutional/college-de-france`; `fintech/mercury`. The side-by-sides go to `E/w1-a/refs/`.

## 7. The council, and the lane

**Council** (§3.3 item 4): the Typography Director (lead) → design → taste → accessibility → performance → the Creative
Director. Chairs calibrated by W1-K (no gate before W1-K has passed), none scoring what it built; on every scale the lowest
chair, never a mean; three rounds at most. §3.1 wants two chairs a scale and names UX on UX and mobile: the UX lead sits
for those two scales — if none is seated, the Typography Director takes UX and design takes mobile, and the scorecard
says so. Not a flagship: no blind ranking.
**Lane** (`E/LANES.json`, lane 3): 8783 on `ile_v5_l3`, `DB_CONN_MAX_AGE=0`, `ILE_REFERENCE_DATE=2026-10-03`,
`--noreload`, stopped when done; pytest on `test_ile_v5_l3` — `TEST_DATABASE_URL=…/ile_v5_l3`, as the lane's `.env` has
it (Django adds `test_`; a URL naming `test_ile_v5_l3` would test on `test_test_ile_v5_l3`); sessions by `force_login` on
`ile_v5_l3` from a scratch script outside every repository; a headless profile under
`C:/tmp/ile_v5_council/.profiles/w1-a-<label>/`, never 8780, never Chrome 9222 / 9223; `lock_gate.py` before every browser
series, build, full suite or measurement. Evidence in `E/w1-a/`; the scorecard, the chairs' files, the CD decision and
the report in this folder.
