# W1-C · core components — implementation notes

The family's implementer (label w1-c-impl-1), under V5.5 delivery mode (implement → review once → fix → ship).
Append-only: each step adds a dated section. Heavy evidence (captures, probes, logs) is outside every repository,
under `C:/tmp/ile_v5_council/evidence/v54/w1-c/impl-1/` (E/ below); the tools are under
`C:/tmp/ile_v5_council/.work/w1-c/w1-c-impl-1/tools/` (T/).

Lane 8: dev server 8788 on `ile_v5_l8` from this worktree (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
`--noreload`, no preview routes); pytest on `test_ile_v5_l8`; headless Chromium with the lane's own profile
(`C:/tmp/ile_v5_council/.profiles/w1-c-impl-1/`), one browser and one pytest at a time; never 8780, never Chrome
9222 / 9223. Signed-in pages used seven sessions minted with `Client.force_login` (`T/mint_sessions_l8.py`; no
password used, typed or stored), revoked at the end of the step. Every browser series and every build went
through `servers/lock_gate.py` first; the lock was never present. No run ended on «Target crashed».

---

## Step 1 — buttons, fields «la lastra», notices, tabs and the disclosure (9 October 2026)

Part 2 of the family (chips, cards, the O14 lint, the specimen boards) is the next step and is not in this one.

### What was done

**Four sheets in `static/css/v5/`, imported after `v5/base.css` in the plan's order** (buttons, field, notice,
tabs; `v5/loader.css` and `v5/chrome.css` follow). What they replace left the cascade with them: `components.css`
§1, §4, §14, §15 and §20's field rules (57 679 → 43 593 B), `v3/buttons.css` (deleted), `v4/buttons.css` (deleted —
see the hand-over below), the notice block of `v4/shell.css`, and the V4 input of the entrance sheet.

1. **Buttons** (`v5/buttons.css`). The slab on V3's property API, kept whole (`--btn-fill`, `-ink`, `-edge` and
   their `-hover` / `-press` states, `--btn-box-h`, `--btn-pad`, `--btn-pad-end`). Every primary is flat — no
   gradient, no light, no shadow (the only `box-shadow` in the sheet is `none`); the hero's signature CTA is not
   drawn here. Secondary on paper, soft, ghost in the accent, danger outlined, icon 40 px with a 44 px hit area.
   36 / 44 / 52 px from the control tokens, 44 px under a coarse pointer. Link-style and quiet variants. States:
   rest, hover (only under `(hover: hover)`, never on a disabled or busy button), `:focus-visible` (the one ring,
   nothing added), pressed — one gesture, the press fill and 1 px down at 0 ms, back on `--spring-snappy`, nothing
   under reduced motion — `:disabled` / `[aria-disabled="true"]` / `.is-disabled` by colour and cursor, never by
   opacity. On night the primary is the paper plate (DS V5 §10.1). A wrapped Latin label stays centred on an
   Arabic page. Borders carry the hierarchy in forced colours. `.is-busy` is not drawn by this sheet.
2. **Fields «la lastra»** (`v5/field.css`). Label above (14/20, 8 px), help and errors 13/20 wired by the ids
   Django writes in `aria-describedby`; the control is a plate — paper, a 1 px hairline at 3 : 1, radius 4, no
   shadow, 44 px in the console and 52 px on public pages (`body:not(.console) { --field-h: var(--control-lg) }`),
   typed text 16 px — at specificity (0,1,0), so a component that draws its own control keeps it. The select's
   chevron is drawn from the icon ink (with its RTL twin); the file control's button is 36 px, 44 px under a
   coarse pointer; the password keeps room for its show / hide control on the side where an LTR password ends,
   on Arabic pages too. Focus: the one ring, the foundation's halo on public pages, and a 2 px rule drawn along
   the foot with `transform` from the reading edge. Invalid is never colour alone: the edge doubles, each
   message carries a drawn mark, and the words. Checkbox, radio and switch are the native controls drawn from
   tokens at 24 px, hit in 44 px under a coarse pointer. `templates/components/form_field.html`: the required
   mark is tied to its label by a no-break space.
3. **Notices** (`v5/notice.css`). One shape; the kind is said three times without colour — the mark, the title,
   the style of the inline-start rule (solid, dashed for a warning, double for an error). A done thing is ink,
   never green with a check (O14); pending is lapis, a warning amber, institutional a hairline frame.
4. **Tabs and the disclosure** (`v5/tabs.css`, `initTabs` and `initAccordions` in `static/js/main.js`). WAI-ARIA
   tabs: automatic activation, roving tabindex, Home / End, arrows that wrap and follow the reading direction,
   Alt / Ctrl / Meta + arrow left to the browser. One indicator, moved with `transform` alone from custom
   properties `initTabs` measures (`--spring-snappy` on public pages, `--ease-layout` in the console); only a
   pointer's choice travels, the panel arriving 12 px from the side of the travel. Nothing is written to
   `localStorage` (A11Y G-21 closed). The accordion draws its own chevron for every producer, `.accordion__panel`
   is `.accordion__body` (G-19 closed), and a link to a row opens it (`/faq/#key`).
5. **Tier 0.** With `html[data-input="key"]` (W1-D's flag) every transition of the family lasts 0 s.

### Commits (branch `v54-w1-c`, on design-v5 `8246a7f`)

| Commit | What |
|---|---|
| `80f49f4` | the four sheets, the legacy deletions, `dist/main.css` |
| `c72de90` | the entrance draws no field of its own (login, signup, reset take «la lastra») |
| `1deb012` | `initTabs`, `initAccordions`, `templates/components/tabs.html` |
| `cb8e4fe` | the family's tests; `test_state_chips_carry_a_register.py` skips `templates/dev/**` |
| `8130aff` | tier 0 — the family's rules for a change asked from the keyboard |
| `df48d7f` | DS 2026, A11Y §13 (G-19, G-21), the decision log |
| `ae25efa` | two family tests hold on both sides of the loader family's merge |
| `1e6f1df` | the slab keeps `--btn-pad-end`, where the loader's key is centred (found by a trial merge) |
| `0be55b0` | the slab reads no V4 lighting (found by the same trial) |
| `bf9e03a` | `components.css` keeps its §3 until the chips move (the icon family's test reads up to it) |
| `6498889` | `v4/workspace.css` left as it was — the earlier edit changed no pixel |
| `8606a4b` | merge of design-v5 with the icon family (W1-B) |
| `68c637e` | the required mark tied to its label |
| `1ac68e2` | merge of design-v5 with the loader family (W1-D) |
| `d16fcb5` | the V4 busy block goes — the loader family's hand-over |
| this commit | these notes; DL54-50 names the hand-over's three outside paths |

The decision log's entries are **DL54-45 … DL54-51**. They were DL54-26 … 32 before the first merge, 37 … 43
between the two and 39 … 51 until the merge of 11 October, which gave W2-D's entries DL54-39 … 44 their place (+6;
the earlier commit messages and the review reports' first wording carry the old numbers); nothing outside the log cites them.

### «No page worse» — every page type, fr + ar, 1440 × 900 + 390 × 844

W1-0's tools (`capture.py`, `health.js`), copied unchanged and pointed at lane 8: 79 page types × fr, ar × two
viewports = 316 cells, one fresh headless profile per cell, axe and the real-Tab focus walk. The 404 is reached
through `/_errors/404/` (the lane runs with DEBUG on). Every sweep: 316 / 316 answered their expected status.

| Sweep | Tree | Overflow | Clipped text | Focus missing | Overlapping targets | axe contrast failures | axe violation nodes | Targets under 24 px | CSP | Page errors |
|---|---|---|---|---|---|---|---|---|---|---|
| W1-0 «before» | `v54/base` | 0 | 108 | 0 | 32 | 4 | 8 | 376 | 0 | 0 |
| `E/base` | design-v5 `a906d6d`, before this family | 0 | 108 | 0 | 36 | 4 | 6 | 218 | 0 | 0 |
| `E/a5` | this family alone (the sheets of `80f49f4`) | 0 | 108 | 0 | 36 | 4 | 4 | 218 | 0 | 0 |
| `E/a8` | + the icon family (`8606a4b`) | 0 | 106 | 0 | 36 | 4 | 4 | 218 | 0 | 0 |
| `E/a10` | **final: + the loader family and the hand-over (`d16fcb5`)** | 0 | 106 | 0 | 36 | 4 | 4 | 218 | 0 | 0 |

No cell is worse than the W1-0 set, nor than the lane's own base, on overflow, clipped text or focus, in any of
the three sweeps of this family. What moved, and why:

- **axe 6 → 4 nodes**: the login's reset link no longer fails `target-size` (fr, both widths). The four that
  remain are the Forum registration's eyebrow (`.forum-hero__eyebrow`, 1.36 : 1) — the forum's, before and after.
- **Clipped text 108 → 106** came with the icon family (two rail labels).
- **Overlapping targets 32 → 36** is the lane base's figure, from families merged before this one (the wizard's
  sticky action bar over the first question at 390 px, the open navbar, the helpdesk queue).
- axe «incomplete» (to check by hand, not failures): 1 863 → 1 762 with this family alone — the primaries no
  longer carry a gradient, so axe can read them; six new ones are the two selects whose chevron is a drawn
  background (`#case-status`, `#id_account_type`: ink on paper, the same pair as every field).
- «Across layers» overlaps moved in three cells (5 → 0, 5 → 0, 0 → 5): the console's fixed bottom bar lies over
  whichever control is at the fold in a full-page capture.

Smaller re-probes after each late change, each compared leaf by leaf with the sweep before it: 56 cells after
the tier-0 rules (`E/a6`, 0 leaves moved) and 64 cells after the template change (`E/a9`, 0 leaves moved).

**Computed styles and boxes** (`T/probe_styles.py`, 320 cells: the 316 and the showcase; every `.btn`, control,
checkbox, notice, tab and accordion row with its box and 35 properties; `T/diff_styles.py`):

- base → this family (`E/a3/styles-diff.txt`): the changes are the intended ones — the primary flat (the
  background image gone), radius 6 → 4, the secondary on the sheet surface, the ghost in the accent, the large
  button's label 17 → 15 px, checkbox and radio drawn, public fields 52 px, the fieldset frames gone, the notices
  re-registered. Scroll width grew in 0 cells.
- the padding API (`E/a7/styles-diff-p0-p1.txt`): only the arrow buttons' end padding (20 → 16 px, 16 → 12 px
  on the small one); no size, position or document height changed.
- the lighting (`p1 → p2`) and the required mark (`p3 → p4`): no size or position changed.

**Looked at**, fr and ar, 1440 and 390 (`E/a4/pages`, `E/a5`, `E/a8`, `E/a10` captures; `E/a4/states`): the contact
and company forms at rest and after an empty submit, login and signup, the account pages, the company's need
form, the upload and the document requirement, the helpdesk form, the orientation wizard, «Ma situation», the
FAQ with a row open, the Forum's closed registration, the anti-fraud callout, the success notice after an
enquiry, the company dashboard, the showcase's button, field, notice and tabs boards; hover, press, focus,
disabled, reduced motion and the coarse pointer as states.

### Weight

`dist/main.css`, gzip 9: design-v5 `8246a7f` 43 933 B → this branch **43 821 B** (−112 B; raw 240 301 →
239 820 B), under the 45 KB ceiling (46 080 B) by 2 259 B. On the wire (W1-A's method: the hashed `url()`s,
`T/css_bytes_w1c.py` → `E/css_bytes.json`): 44 012 → 43 899 B. `dist/accounts/entrance.css`, gzip: 1 208 → 982 B.

| Page type | W1-0 before | design-v5 `8246a7f` | This branch | Ceiling (+ 8 KB) | Headroom |
|---|---|---|---|---|---|
| home | 39 114 | 46 832 | 46 719 | 47 306 | 587 |
| door page, interior page | 36 294 | 44 012 | 43 899 | 44 486 | 587 |
| login | 37 502 | 45 220 | 44 881 | 45 694 | 813 |
| dashboard, case file | 41 668 | 49 386 | 49 273 | 49 860 | 587 |
| «Mes pièces» | 42 839 | 50 557 | 50 444 | 51 031 | 587 |

**The Wave-1 allowance is nearly spent: 587 B per page type.** This family gives 113 B back; part 2 (chips,
cards) has to delete at least what it adds. `static/js/main.js` 15 163 → 18 104 B (gzip 4 537 → 5 566 B),
served as it is; the page budget is 45 KB gzip of script in all.

### Tests

On the final tree (`d16fcb5`), with the lane's database:

- `tests/frontend/test_components_w1_c.py` — 29, on the sources. `tests/frontend/test_browser_w1_c.py` — 11,
  Chromium on the live server.
- Targeted, no browser: 1 528 passed, 2 xfailed (both older than this family: the legacy token shim, the
  showcase's captions), 17 deselected (`E/suites/final-targeted-nonbrowser.txt`) — the chips registry,
  `test_state_chips_carry_a_register`, `test_layout`, `apps/accounts`, the V5 and V4 tokens, the bundles, the
  design documents, the RTL guard, the icons, the loader's rules, the preview and the showcase.
- Browser, one module set at a time: 45 passed (this family's, the loader's, its reduced-motion module) and 57
  passed (`test_rtl_browser`, `test_rtl_browser_nav`, the header, «Il portico», `test_browser`, the icon
  family's) — `E/suites/final-browser-1.txt`, `final-browser-2.txt`.
- `scripts/regen_design_inventory.py`: current. `ruff check` on the family's test files: clean.

Not run: the full suite (V5.5: targeted tests only) and the design preview's browser tests (W1-P's).

One test of another family was repaired on the way: `test_state_chips_carry_a_register` had six failures on
design-v5 since the preview landed (its `dp-state` labels read as chips); the scan now skips `templates/dev/**`.

### The two merges, and the loader family's hand-over

design-v5 moved twice during the step; both times it was merged in and the whole measure taken again.

1. **`8606a4b`, the icon family.** `components.css`: §1 gone (this family) and §2's header the icon family's;
   the decision log renumbered; DS 2026 §2 by row. `components.css` §3 «Badges & tags» — a comment, no rule — had
   left with §1 in the first commit; it is back until the chips move, because that family's
   `test_icons.py` reads §2 «up to "   3. Badges"» (`bf9e03a`).
2. **`1ac68e2`, the loader family, then `d16fcb5`, its hand-over.** W1-D's notes («Handed to — W1-C») and the
   steward's shipped note: V4's busy rule repainted every waiting button as the primary, and its keyframes
   looped. Both were tried first on a throwaway merge of the two branches, which found two things this family
   had to change in its own sheet before any merge: the slab had dropped `--btn-pad-end`, in which the loader's
   key is centred (`1e6f1df`), and it still read V4's `--btn-lighting` (`0be55b0`). After the real merge:
   - `v4/buttons.css` is deleted with its import; the RTL guard's one known entry goes with it;
   - `KEYLESS` in `static/js/src/shell.js` names the three padless variants the sheets draw (V3's `--tertiary`
     and `--inline` have no producer in any template and are not drawn);
   - one assertion of `test_loader_w1_d.py` reads the V5 link, which has no `::after`.

   A waiting button now keeps its own surface and ink — primary, secondary, ghost, danger, the paper plate on
   night — with the key at 80 % of that ink in the end padding: 7.2 px from the last glyph, 5.2 px in a small
   button, 9.2 px in a large one, 5.2 px from an arrow's box (`E/trial-w1d/busy-*.json`, `busy-sheet-fr.png`;
   the final tree: `E/a10/busy/`).

The JS bundles in this branch were rebuilt from a clean `dist` on lane 8 and carry this worktree's chunk names
(`chunk-4CTWE25X`, `chunk-SASCRBJY`); the steward's rebuild after the merge gives them design-v5's again.

### Ownership — six paths outside the slice, each justified (DL54-50)

`scripts/check_ownership.py w1-c design-v5`: 11 inside, 5 slice, 13 generated, **6 outside**, for the merge step
to write into the manifest:

| Path | Whose | What, and why |
|---|---|---|
| `apps/accounts/static/accounts/entrance.css` | W2-B | 37 lines deleted: the V4 input at (0,5,1) overrode «la lastra» (W1-A review m-1, m-9; the Arabic login overflowed at 390 px) |
| `static/css/v4/shell.css` | W2-C1 | the notice's type block, which that file's own header gave to this family |
| `docs/ACCESSIBILITY.md` | W1-A | §13, the rows of G-19 and G-21, closed (a test holds the two documents to the same status) |
| `static/js/src/shell.js` | W1-D | `KEYLESS`, one constant — the hand-over |
| `tests/frontend/test_loader_w1_d.py` | W1-D | one assertion — the hand-over |
| `tests/i18n/test_rtl_static.py` | W1-A | `KNOWN_UNMIRRORED` emptied — the hand-over |

In the slice but worth the steward's eye: `static/css/main.css` holds two deleted imports and four added ones
(the plan's order); `docs/design/DESIGN_SYSTEM_2026.md` outside §10 (the §2 rows of the sheets this family adds,
empties or deletes, §2.1's entrance row, one sentence of §5.1, §16's two rows, §21's two, two sentences of the
motion section on `btn-busy`).

### Open points for the review

1. **The ring beside its halo on public text fields: 2.59 : 1.** The one focus system gives a text field the
   2 px ring (laguna-550) at a 2 px offset **and** a 5 px halo at α 0.3 (plan §1.6); the halo is painted under
   and around the ring. Measured on the company form: ring against the page ground 3.70 : 1, against the field's
   fill 4.11 : 1, **against the halo band on both of its sides 2.59 : 1**; halo against the ground 1.43 : 1. The
   icon family's keyboard walk had already listed three textareas for it («the ring under 3 : 1 … W1-C's field
   ring»). Until this family the legacy field rules hid the halo on most fields; W1-A's review asked that it
   reach them (m-9), and it now does, on every public text field. Whether a ring that is 3.70 : 1 on the ground
   but separated from it by its own halo meets 1.4.11 is a judgement this step does not make. The ways out,
   none taken: leave it (the halo is part of the indicator); a lighter halo (α ≤ 0.16 gives 3 : 1, and a halo
   at 1.2 : 1 on the ground — W1-A's token); a ring one step darker on text fields (laguna-600: 3.33 : 1 against
   the α 0.3 halo, 4.76 on the ground — one token of `v5/tokens.css` and one line here).
2. **The console's fields have no halo.** `.console__workspace :is(a, button, input, select, textarea, …)`
   (`v4/workspace.css`, the console family's) keeps V4's 2 px companion in the ground's colour on every control:
   ring 3.70 : 1 with the ground on both sides. That is the safer of the two constructions; it is not the
   plan's letter. Left to the console families, with point 1.
3. **The icon-only button's busy face** (DS V5 §10.1: the key replaces the glyph) is not drawn: no template
   uses `.btn--icon`, so `KEYLESS` keeps one waiting with `aria-busy` and no key.
4. **The same plain space before the required mark** is in three templates of other families
   (`templates/allauth/elements/field.html`, `templates/enquiries/partials/form_field.html`,
   `templates/news/_newsletter.html`): `&nbsp;` there too.

### Left — for part 2, and for other families

- **Part 2 of this family:** chips and cards on V5 (`components.css` §3 and §13, `v3/chip.css`; the icon family
  notes that `.chip__g { stroke-width: 2.6 }` now reads as px and that the documents' filter chips keep V4
  marks), the O14 lint test (it does not exist yet), the specimen boards (none was built in this step: the
  showcase at `/_design/` carries the buttons, the form, the notice and the tabs).
- **`templates/components/form_field.html`** changed by one character twice (the no-break space); the reset slot
  is W2-B's. `templates/components/notice.html` is untouched.
- **The accordion's glyph**: the templates still write a `plus` icon in the summary, which the sheet hides in
  favour of its drawn chevron (DL54-48; the icon family's DL54-29 item 2 expected the map's chevron — it is
  drawn, not taken from the sprite, so the FAQ's own producer needs no change). The dead `<svg>` can leave the
  two templates when their families pass.
- **`--hit-min`** is no longer read by a button; nine readers remain in other families' sheets (`v4/shell.css`,
  `v4/workspace.css` × 2, `console.css` × 4, `dev/designpreview.css` × 2), so the alias stays.
- **The legacy shim** (`static/css/_legacy-tokens.css`, 142 names): 1 274 → 1 077 readings; 27 more names have
  no reader left, 36 in all — `--btn-bg` and its four siblings, `--notice-bg / -fg / -border`, the old notices'
  `--color-<state>-*`, `--font-size-button`, `--tracking-button`, `--text-placeholder`, `--icon-size`. Its
  ceiling test is W1-A's and was not lowered.
- **Seen on the way, older than this family, not touched:** the account pages' links box floats over the title
  on every signed-in public account page (in the W1-0 set too; W2-A / W3-F2); the wizard's sticky action bar
  covers the first question at 390 px until the page scrolls (W3-D); the Forum registration's eyebrow at
  1.36 : 1; a required consent label of the account deletion page breaks before its last word (the account
  page's measure).
- **The lane server keeps its templates** (`--noreload` and the cached loader): a template change needs a
  restart before it is measured. Every sweep above ran on a server started after the last template change it
  measures.

### Where the evidence is

`E/PAGE_TYPES.json` (79 types) · `E/base`, `E/a5`, `E/a8`, `E/a10` (the four full sweeps: `runs/captures-s0.jsonl`,
`captures/<type>/<lang>/`) · `E/a6`, `E/a9` (re-probes) · `E/a3`, `E/a7` (style probes and their diffs, the
focus ring's figures in `a7/ring`, the busy face before and after in `a7/busy-*`) · `E/a4/states`, `E/a4/pages`
(hover, press, focus, disabled, reduced motion, coarse pointer; pages at rest) · `E/trial-w1d` (the busy key on
the V5 slab) · `E/suites` (every test run's output) · `E/css_bytes.json`.

---

## Step 2 — the status chip «i cerchi», the tag, cards by purpose, the O14 lint (9 October 2026)

The family's second implementer (label w1-c-impl-2), same lane and same rules as above. Evidence under
`C:/tmp/ile_v5_council/evidence/v54/w1-c/impl-2/` (E2/ below), tools under
`C:/tmp/ile_v5_council/.work/w1-c/w1-c-impl-2/tools/` (T2/), browser profiles under
`C:/tmp/ile_v5_council/.profiles/w1-c-impl-2/`. The lane server ran with the preview routes only for the captures
of the chip board. Seven sessions minted with `Client.force_login` (`T2/mint_sessions_l8.py`), revoked at the end.
The benchmark lock was never present; no run ended on «Target crashed». design-v5 did not move during the step
(`8246a7f`): no merge.

### What was done

**The registry** — `apps/core/chips.py`: the eight registers of plan §1.2 (conforme, esame, neutro, attesa, azione,
rifiuto, blocco, nullo) for 21 producers and 103 members; 16 members moved, by one rule (`in_review`,
`under_review`, `assigned`, `in_progress` → esame; `blocked` → blocco) and four rows of their own (a verification
and a scan that are `pending` → esame; `not_required`, `not_configured` → nullo). «En examen» is lapis. The mark
comes from the icon registry (`icons.STATUS`); «À remplacer» keeps the register of «Manquant» and has its own mark.
The legacy badge kinds are translated once: `warning` → attesa, `pending` → esame, and two new ones for the
deadlines, `soon` → attesa and `overdue` → azione (DL54-52).

**One producer** — `{% chip member "app.Enum" %}word{% endchip %}` (a block tag of the built-in library) renders
`templates/components/chip.html`: register, mark, word, and the three notches of a case status. 76 calls in 42
product templates — 72 of the 81 sites that wrote the element by hand, and the two badge partials; the other nine
sites were terms, not states, and are a `.tag` (no register, no mark). No template writes a chip by hand any
more, so none can be drawn without its mark (DL54-53).

**The sheets** — `static/css/v5/chip.css` (24 px by construction, 20 dense, 28 large; the mark on the first
line; a long word wraps, a chip in a table cell does not; the edge's style as the third voice; no pointer, no
hover, no focus; the tag) and `static/css/v5/card.css` (the record card on level 1, the action card on level 2,
the summary strip; no stat card, no board; one radius). They replace `static/css/v3/chip.css` (deleted),
`components.css` §3 and §13 and the pill block of `v4/workspace.css`; the health strip and the filters' legend of
«Mes pièces» read the chip's tokens and draw its marks (DL54-54, DL54-55).

**The O14 lint** — `tests/frontend/test_o14_lint.py`: HTML as a tree, CSS (sources and bundles), JavaScript and the
Python producers; 30 planted cases caught, 16 clean ones left alone. Its first finding: the V1 stepper's check on
a done step (`components.css` §16) — removed (DL54-56).

**The boards** — the chip board `/__design-v5/specimens/chips/` (preview routes): eight registers and the second
mark of attesa × stone, sheet, night × French and Arabic, the three sizes in both scripts, the long word, the
table cell, the gauge, the unknown value, the tag, the three cards in both directions. The showcase `/_design/`
draws the same through the tag, and the wrapped card.

### Commits (branch `v54-w1-c`; design-v5 is `8246a7f`)

| Commit | What |
|---|---|
| `63741a5` | the eight registers; each register draws its mark from the icon registry |
| `60e377f` | the chip has one producer — the `{% chip %}` pair — and every site goes through it; nine tags |
| `fbb79b6` | `v5/chip.css`, `v5/card.css`; the legacy rules they replace leave the cascade; `dist/` |
| `afb2206` | the O14 lint as a test; the stepper's check removed |
| `3b340c6` | the chip board and the showcase |
| `a8a6698` | DS 2026 and A11Y say what the tree does |
| `1ae4eb0` | three console fields take the field's corner (4 px) |
| `80eb464` | three corrections the browser tests found — the tag's 44 px, a chip in a narrow cell, the summary at 390 |
| `7fed91f` | the showcase's sample checklist draws its two states through the tag |
| `22da9fa` | `tests/frontend/test_browser_chips_w1_c.py` |
| `cc35b8b` | three corrections the final sweep found on the pages that draw a card (below) |
| this commit | these notes; DL54-52 … DL54-57 |

### «No page worse» — 91 page types, fr + ar, 1440 × 900 + 390 × 844

The same tools as step 1 (`capture.py`, `health.js`: one fresh headless profile per cell, axe, the real-Tab focus
walk), with one probe added to every cell (`T2/probes.js`: each chip and tag of the page — register, symbol,
box, lines, mark, font, contrast — and the corners and planes of the first viewport). **The set is wider than
W1-0's**: its 79 types and 12 more that draw a chip or a tag and are not in it — two bridges (an authorised
actor's, a professional's), a company's need, an academy plan, the selection's disclosures, a second case file,
its pre-evaluation, a second «Mes pièces» and requirement, a professional's case file and helpdesk request, a
second cases index. 91 × 2 × 2 = **364 cells**; every one answered its expected status.

- Before: step 1's final sweep `E/a10` for the 79 (tree `d16fcb5`, this step's base) and `E2/b0` for the 12,
  captured on the same base before any change.
- After: `E2/f1`, the 364 cells on `22da9fa`; then `E2/f3`, the 20 cells of the five page types that draw a card,
  on `cc35b8b` — the only pages the last commit can reach (an HTTP read of the 91 types: `class="card"` on
  «Formation», the three doors with a related list, and the pilot). `E2/final` is the two together.

| | Overflow | Clipped text | Focus missing | Overlapping targets | axe contrast failures | axe violation nodes | Targets under 24 px | CSP | Page errors |
|---|---|---|---|---|---|---|---|---|---|
| before (364 cells) | 0 | 149 | 0 | 37 | 6 | 6 | 302 | 0 | 0 |
| **after** (`E2/final`) | 0 | 149 | 0 | 37 | 6 | 6 | 302 | 0 | 0 |
| W1-0 «before», its 316 cells | 0 | 108 | 0 | 32 | 4 | 8 | 376 | 0 | 0 |
| after, the same 316 | 0 | 106 | 0 | 36 | 4 | 4 | 218 | 0 | 0 |

**No cell is worse** on overflow, clipped text or focus, against the lane's base and against W1-0's set
(`E2/final/compare-vs-before.json`, `compare-vs-w1-0.json`), and no other health figure moved in any cell, leaf
by leaf (`T2/cells_diff.py`), but two that are not failures: axe's «incomplete» contrast count in four cells
(± 1 to 3) and, in one cell, the «across layers» overlaps of the console's fixed bottom bar with whatever is at
the fold of a full-page capture (5 → 10: the page is 24 px taller).

**What the sweep found, and was fixed** (`cc35b8b`): on `E2/f1` «Formation» had two targets under 24 px in each
cell where it had none — the cards' second actions, 20 px tall on the new 13/20 meta line. Looking at the
captures of the five card pages showed two more: the entries of the related lists had lost the room under their
text (the next hairline 8 px under it), and the two phases of «Formation», which wrap their content in a
section, had their eyebrow, title, text and link sitting on each other. Fixed in `v5/card.css`, re-captured
(`E2/f3`): no health figure moved on the 20 cells.

**Heights.** 42 cells changed height on `E2/f1`, none by an overflow: the five card pages (the cards are V5's:
their titles are 20 px where the old ones were 13); a ± 1 to 3 px on rows whose chip is now 24 px; and seven
console cells at 390 that grew by 20 to 32 px because a V5 chip is wider than V3's (the mark, 13 px, and the
gauge) and a row wraps where it did not — the person's dashboard header in French (the date goes under the
reference), the same header with the terms pending in Arabic, an academy enrolment in both languages (a
module's «suivi» goes under its title), the first entry of a company's needs, a second case file in Arabic, and
the helpdesk's «Vérification professionnelle requise», the one chip of the set on two lines (253 × 44). Each
was looked at; nothing is cut and nothing overflows.

### The chips, measured

- **In the browser** (`E2/final/chips-report.json`): 384 chips and 68 tags over the 364 cells, on 29 page types
  (tags on 5), 23 seats. Registers met: neutro 100, attesa 96, conforme 68, azione 56, nullo 32, esame 24,
  rifiuto 8 — no blocco on the lane's data. Every chip has a known register and that register's mark (72 dashed
  rings and 24 «À remplacer» rings for attesa); every tag has neither. 383 chips are on one line and 24 px tall,
  none off by a quarter pixel; one wraps. Every mark is 16 × 16, on the centre of the first line (0 px off in
  all 384), 4 px inside the reading edge — the right in Arabic. Text 13 px, 14 px on the console at phone width
  and on every Arabic page (the tokens' floors), no tracking, no capitals. Contrast on the chip's own body:
  words 5.38 : 1 at the least, marks 3.28 : 1.
- **In process, the whole site** (`T2/site_chips.py`, the Django test client signed in as each of seven personas
  and as a visitor, inside a rolled-back transaction; `E2/final/site-chips-fr.json`, `-ar.json`): 788 pages in
  French and 789 in Arabic, 729 of them answered 200; 72 hold a chip and 85 a tag; **192 chips and 350 tags, 0
  without a register, a mark or a word, 0 elements still written the old way** (`state`, `state--*`,
  `badge--*`). 30 of the 44 templates that call the chip or hold a tag were drawn by a page of the walk.
- **The 14 the lane cannot reach** — the community's three (404 on the lane), the permanent forum's nine (503),
  the selection process and its partial (no process for a persona) — were drawn by their apps' own tests with
  the same judge attached to the test client (`T2/chip_watch.py`, a scratch pytest plugin): see «Tests».
- **By construction**: `test_state_chips_carry_a_register.py` reads every call of the tag (its producer or its
  register must be known) and renders every member of every producer through it.
- **Looked at**, fr and ar, 1440 and 390: the dashboards, «Mes pièces» and its legend, the case files, a
  company's dashboard and needs, the helpdesk lists and a request, the academy, the pathway's and the diplomas'
  terms, «Formation», the related lists, the chip board and the showcase (`E2/f1/captures`, `E2/f3/captures`,
  `E2/final-look`).

### Corners and planes (first viewport of each cell)

- This family's components draw three radii: 4 (buttons, fields, notices), 8 (cards) and the pill (chips, tags).
- 47 of the 364 cells show more than three, and in each the fourth is another family's: the 6 px of the
  console's rail rows and tile (24 signed-in cells at 1440 are 4 · 6 · 8 · pill), of the header's targa and of
  the menu toggle, and the 12 px of the entrance's sheet, of the doorway's legend and of the wizard's question.
  With the three console fields folded to 4 px (`1ae4eb0`), a phone console screen holds 4 · 8 · pill. The
  wizard's own input is still 6 px («Ma situation»).
- Planes: no signed-in cell has more than two shadow values in its first viewport, and none has more than one
  plane of level 2 or above.

### Weight

`dist/main.css` on the wire (W1-A's method, `T2/css_bytes_w1c.py` → `E2/css_bytes.json`): design-v5 44 012 B →
step 1 43 899 B → **43 020 B** (−992 B against design-v5), under the 45 KB ceiling (46 080 B) by 3 060 B.
`v5/chip.css` 6.4 KB and `v5/card.css` 7.5 KB of source; `v3/chip.css`, `components.css` §3 and §13 and the V4
pill block are gone.

| Page type | W1-0 before | design-v5 `8246a7f` | This branch | Ceiling (+ 8 KB) | Headroom |
|---|---|---|---|---|---|
| home | 39 114 | 46 832 | 45 840 | 47 306 | 1 466 |
| door page, interior page | 36 294 | 44 012 | 43 020 | 44 486 | 1 466 |
| login | 37 502 | 45 220 | 44 002 | 45 694 | 1 692 |
| dashboard, case file | 41 668 | 49 386 | 48 394 | 49 860 | 1 466 |
| «Mes pièces» | 42 839 | 50 557 | 49 566 | 51 031 | 1 465 |

The family as a whole gives 992 B back to the Wave-1 allowance (587 B of headroom per page type after step 1,
1 466 B now). No script was added or changed in this step.

### Tests

On the final tree, with the lane's test database, one pytest at a time:

- **This step's own:** `test_chips_registry.py` 30, `test_state_chips_carry_a_register.py` 118,
  `test_o14_lint.py` 53, `test_chips_cards_w1_c.py` 17 — on the sources; `test_browser_chips_w1_c.py` 13 —
  Chromium on the live server (the eight registers and their marks, night, 20 / 24 / 28 px in French and in
  Arabic, the long word and the table cell, the gauge and the unknown value, forced colours, the tag's 44 px,
  the filters' legend, the cards' levels and radius, the wrapped card, the entry's room, the summary strip at
  1440 and 390).
- **Targeted, no browser** — every module of `tests/frontend` and `tests/i18n` that opens no browser:
  1 392 passed, 2 xfailed (both xfails are older than this family: the legacy token shim, the showcase's captions). It
  holds `test_layout.py` (29, its form slice among them), `test_components_w1_c.py` (29), the V5 and V4 tokens,
  `test_css_bundle_is_current`, `test_design_docs`, the icons, the loader's rules, the RTL guard, the locked
  texts, the catalogues and the page integrity of the four languages.
- **`apps/accounts` and `apps/core`:** 81 passed. **The ten apps whose templates changed** (portal, documents,
  cases, companies, helpdesk, academy, forum, selection, community, pathways): 1 168 passed, 3 skipped (the
  cases' intake, for want of a rule in force on the test data — older). These two runs are on `22da9fa`; the
  commit after it changes the card sheet, the showcase, two test modules and the design document, none of which
  they read.
- **Browser, one module set at a time:** 51 passed (`tests/i18n/test_rtl_browser.py` 23 — the forms among
  them —, this family's two modules 11 + 13, the icon family's 4) and 378 passed (`test_browser`, the loader's
  module and its reduced-motion one, `test_rtl_browser_nav`, the header at the narrowest viewport, «Il
  portico», the design preview).
- **The watch on the forum's, the community's and the selection's own tests** (`-p chip_watch`): 343 passed;
  451 responses, 449 of them HTML, 70 with a chip; 187 chips judged as the sweep judges them — 0 without a
  register, a mark or a word, 0 elements written the old way — and each of the 14 templates the lane cannot
  reach drawn at least once (`E2/final/chip-watch-forum-community-selection.json`).
- **Beside them, because console templates changed:** `tests/test_phase_console.py`, `tests/compliance`,
  `tests/security`, `tests/backoffice` and the two script tests (`test_regen_design_inventory`,
  `test_check_ownership`): 244 passed.
- `scripts/regen_design_inventory.py`: current. `ruff check` on the step's Python: clean.

Not run: the full suite (V5.5: targeted tests only).

### Ownership — 60 paths outside the slice (`scripts/check_ownership.py w1-c design-v5`), DL54-50 and DL54-57

The six of step 1, and 54 of this step: 46 templates (41 that call the chip, the two that now hold tags only,
the filters' legend, `components/card.html`, the showcase), `apps/core/templatetags/ile_core.py`,
`static/css/v4/workspace.css`, `apps/documents/static/documents/documents.css`, `static/css/base.css`,
`static/css/v5/base.css`, `tests/frontend/test_icons.py`, `apps/core/dev.py` and the new
`static/css/dev/specimen-chips.css` (in no family's slice: the steward assigns it). One more the script cannot
see, the file being shared: the stepper's check removed from `components.css` §16 (W3-D's). In every template only
the chip or tag element changed. The merge step records them in the manifest.

### Open points for the review

1. **`warning` → attesa and `pending` → esame** change the colour of badges the portal's services emit by kind:
   «Bientôt» is amber (plan §1.2: soon = attesa) and a request «in progress» is lapis. «En retard» is still
   `error` — drawn as a refusal — until W3-C changes the producer to `overdue` (plan §3.5 gives it the deadline
   kinds; F13). A scan that failed, which `SCAN_BADGES` calls `warning`, is amber on the bridge's cards where
   the registry says azione for `documents.ScanStatus.error` (DL54-52).
2. **A V5 chip is wider than V3's** — a row wraps at 390 where it did not in seven cells (above). The one a
   person meets first is the dashboard's header in French: the reference, the chip with its gauge (118 px) and
   the date no longer share a line, and the date goes under the reference. The header is W3-B's to recompose.
3. **A chip on two lines keeps the pill's radius** (22 px ends on a 44 px box), so that a screen does not gain a
   fourth corner; it reads as a lozenge. One case on the lane (the helpdesk list at 390, in French).
4. **The action card and the summary strip have no product consumer yet** — the showcase and the board draw
   them; the dashboards are W3-B's. The record card is drawn by five page types.
5. **Not drawn, having no producer:** the seal chip (an authority's act), `chip--indicative`, the filter chip
   (a control: the staff filter bars are W3-E's), the count pill and the deadline's text styles of DS V5 §10.2
   (W3-C's registers), the chip's change choreography (nothing changes a chip in place without a page load yet).
6. **`badge` stays as a class** on the chips the two badge partials draw — a hook with no rule of its own.

### Left — for other families

- **W3-C:** `present_deadline` → `soon` / `overdue`; `SCAN_BADGES` through the registry; the document rows of
  «Mes pièces» do not share their columns (the third row's chip stands 27 px to the right of the two above —
  it did before).
- **W3-B:** the six-card bridge of the accounts that are neither a person nor a company (the grid §1.15 retires);
  the first consumers of the action card and of the summary strip; the context header at 390.
- **W3-A:** the rail's 6 px rows and tile. **W2-C1 / W2-B:** the targa's and the toggle's 6 px, the entrance
  sheet's and the doorway legend's 12 px.
- **W3-D:** the wizard's own input (6 px) and question panel (12 px). The V1 stepper lost its check: a done
  step is its filled disc with its number. No product template includes `components/stepper.html` today (the
  showcase does); the journey family draws the done step when it redraws the journey.
- **W3-F1:** the pathway's «Termes utiles» list (its first row's two tags stand 4 px apart in height, and the
  list touches the box under it — both older than this step); the two phases of «Formation» now take the
  card's flow, the page needs no rule of its own for it.
- **The buttons' and the fields' specimen boards** (`templates/dev/designpreview/specimens/{buttons,fields}.html`,
  plan §3.3 item 7) are not built: the showcase at `/_design/` carries both sets and step 1's captures of their
  states are in `E/a4/states`. Only the chip board exists.
- **The lane's data draws no blocco chip** and 14 templates are out of its reach (above): a staging data set
  with a blocked checklist item, an open community and a selection process would put them in a sweep.

### Where the evidence is

`E2/PAGE_TYPES.json` (91 types) · `E2/b0` (the 12 extra types before any change; the site map and the HTML crawl
before) · `E2/before-all` (the before set of the 364 cells) · `E2/f1` (the 364-cell sweep), `E2/f2`, `E2/f3`
(the card pages re-captured), `E2/final` (the merged set, both comparisons, the chip report, the two in-process
walks, the watch reports) · `E2/c1`, `E2/c2`, `E2/final-look` (the board, the showcase, pages at rest) · `E2/p1`
(the pilot of the probe) · `E2/css_bytes.json` · the test runs' output in
`C:/tmp/ile_v5_council/.work/w1-c/w1-c-impl-2/logs/`.

## Review fixes (label w1-c-fix, 11 October 2026)

After `REVIEW.md` (w1-c-review, SHIP_AFTER_FIXES) and `A11Y_PERF.md` (w1-c-a11y-perf, SHIP_AFTER_FIXES). The earlier
fix pass was cut by the usage limit and left nothing on disk (tree clean at `61cf067`). design-v5 had moved 73
commits: merged first (`4965b27`; conflicts in `main.css`, DL54, DS 2026 §2, one test, the bundles — resolved as the
commit says; W1-C's decision-log entries are now **DL54-45 … 57**, W2-D's DL54-39 … 44 keep their numbers,
`08d7bb3` updates the citations). The fixes are `73e20bc`; the browser test that pinned the old 44 px action
follows in the notes' commit.

### Finding → change → evidence

| Finding | Change | Evidence (lane 8788, `E3` = `C:/tmp/ile_v5_council/evidence/v54/w1-c/fix/`) |
|---|---|---|
| **M1** · R3 — the password rules are raw HTML, the focus rule leaves its field | `form_field.html`: the help is a `<div class="form-field__help">` with the same id; `field.css`: a help list has no margin, a 1.25 em indent, 4 px between items | sign-up and password change, fr + ar, 1440 + 390: the four rules are `li` inside the help (13 px fr, 14 px ar), no stray list in any `.form-field`; `signup-focus-fr-390.png`: the 2 px rule on the control's foot, the rules under it |
| **M2** · A10 — the show / hide sentence eats the plate; the state said twice | the control is `eye` / `eye-off` (sprite, through `svg_icon`) in a seat of `--field-h − 8px` (44 public, 36 console; hit 52 / 44), a constant visually-hidden name, `aria-pressed` the one channel, the glyph swapped by the sheet; the password's end padding is `--field-h` (RTL twin); `shell.js` §3 no longer writes `textContent` | the password's room **130 → 240 px at 390** (216 on the password change), **204 → 330 px at 1440**; the seat 44 × 44 on every page; `login-shown-ar-390.png` (pressed, `eye-off`, the typed text LTR beside the control) |
| **M3** — a public form's action at 44 px under 52 px fields, never the column on a phone | `buttons.css`: `body:not(.console) :is(.form__actions, .form-actions) > .btn` (boxed) takes `--control-lg` and `--btn-pad-lg`; below 48 rem the primary is block. The profile's `.form-actions` is reached | contact 187 × 52 at 1440, **350 × 52 at 390**; profile 124 × 52 → 350 × 52; password change 221 / 284 × 52; login unchanged (398 / 308 × 52) |
| **M4** · m2 — a chip stretched into a bar on phone lists | `chip.css`: `inline-size: fit-content`; `border-radius: calc(var(--chip-box, var(--chip-h)) / 2)` | dashboard at 390: the widest chip **119 px** (was 296), fr; 104 ar; «Mes pièces» 116; `dashboard-fr-390.png` |
| **A1** — a link button no longer wraps in a panel head (320 px overflow) | `.btn.btn--link, .btn.btn--text { white-space: normal; }` | 0 overflow on all 44 smoke cells; the 320 px cell is the a11y check's (tried there: 51 → 0) |
| **A2** — `<ul role="alert">` loses its list semantics (axe `listitem`) | the alert is a wrapping `<div class="form-field__errors" id="…_error" role="alert">`, the list `ul.form-field__error-list` inside; `docs/ACCESSIBILITY.md` §6 and `test_design_docs` follow | no `ul[role=alert]` on any smoke cell; the rendering test asserts the markup |
| **A3** — `.link-arrow` hit in 24–40 px under a finger | `(pointer: coarse)`: `.link-arrow { position: relative }` and a `::after` with `inset-block: min(0px, calc(50% − var(--hit-primary) / 2))` | test pins it; the home's chapters already did the same in `pages.css` (W2-D) |
| **P1** — `.card > :where(section, div):only-child > *` makes every page recalculate twice | the children are named (`.card__eyebrow, .card__title, .card__text, .card__meta, .notice`), same specificity; a guard in `test_chips_cards_w1_c.py` refuses a universal subject after a structural pseudo-class in every v5 sheet | the a11y check's three-arm run measured this exact selector (style 233 → 197 ms, tasks over 50 ms back to the base's) |
| A4 | the two RTL arrow selectors join the reduced-motion reset | `buttons.css` §7 |
| A5 | forced colours: the error mark `forced-color-adjust: none`, `CanvasText` border and gradients | `field.css` §8 |
| A6 | the halo rule on an invalid control excludes checkbox and radio | `field.css` §4 |
| A7 | `components/tabs.html` takes `label` → `aria-label` on the tab list | the contract line |
| A8 | `.card--link .card__meta > :any-link { position: relative; z-index: 1; }` | `card.css` |
| A9 | `::-webkit-calendar-picker-indicator:focus-visible` takes the system's ring | `field.css` |
| m1 · R2 | `input:is([type="checkbox"], [type="radio"]):checked { color: var(--text-on-accent) }` — the tick white, 5.29 : 1 | `field.css` §6 |
| m4 | the placeholder's ink at zero specificity (`:where(input, textarea)::placeholder`) | `field.css` §3 |
| m5 | a notice's title and body capped at `--measure-body` | `notice.css` |
| m6 | the disclosure's row and answer on the section's edge (no 4 px inset); a focused tab's 2 px corner | `faq-fr-1440.png`: the questions at the heading's x |
| m7 | a question written as a heading takes the row's type (`font: inherit`), keeps its role | `faq-fr-1440.png`: nine rows, one type |
| m8 | `.meta-row` label `nowrap`, the colon joined by a no-break space | `card.css` |

Smoke: `E3/smoke.json` and 44 captures — login, sign-up (rest, focus, empty submit), login with the password
shown, contact, FAQ, dashboard, «Mes pièces», profile, password change; fr + ar; 1440 × 900 and 390 × 844 with
`pointer: coarse`. Every cell 200, 0 overflow, 0 CSP violations, 0 console errors. Looked at: the sign-up at 1440
and 390 (focus), the login shown in Arabic at 390, the dashboard at 390, the FAQ at 1440. One browser at a time;
the session minted with `Client.force_login` and revoked; the lane server stopped.

### Not fixed here, and why

- **m3** (5 px between two buttons on «Supprimer mon compte», «Demande transmise», the upload) — the three page
  templates are other families': handed below.
- **m6, the first tab's 12 px inset** — `initTabs` measures the label from its padding; moving the padding moves the
  indicator. No product page uses the tabs yet; left for the first consumer.
- **m9 / R1** — ruled not a failure; laguna-600 for a text field's ring is a token change through the steward.
- **m10** (a showcase row for the soft and icon buttons, radio, switch, disabled / read-only / warning fields) and
  the showcase's tab list `label` (A7) — `templates/dev/showcase.html` is outside the slice; one row for the next
  family that edits it.
- **m11** (the gauge's notches as bars) — optional, taste; kept as built.

### Paths outside the slice (for the merge step's manifest)

- `static/js/src/shell.js` — section 3 only (the show / hide control): the `textContent` write removed and the
  comment updated; W2-C1's file. Without it the click would replace the glyphs with text (M2, A10).
- `docs/ACCESSIBILITY.md` — §6, the form contract's markup and its two rows (help `<div>`, alert wrapper): the doc
  quotes what the component writes (A2, M1).
- `tests/frontend/test_design_docs.py` — the one assertion of the field's markup, outside the section-count slice.
- `scripts/check_ownership.py w1-c design-v5` after the fixes: 25 inside, 7 slice, 17 generated, 60 outside — the
  DL54-50 / DL54-57 paths still differing from design-v5, plus the two above.

### Handed to

- **W3-B / W2-A** (`templates/accounts/delete_request.html`, the upload) and **W3-F1** («Demande transmise»): m3, the
  inline white space between two buttons — wrap the pair in `.form__actions` / a flex row.
- **W2-A / W3-F2**: on «Supprimer mon compte» at 1440 the account links box covers the end of the warning notice's
  first line (review, «seen on the way»).
- **W3-A**: O1, the console's fixed bottom bar hides the focus at phone width (`scroll-padding-block-end`).
- **W3-F1**: O2 (the pathway page's sticky bar over its side column), the anti-fraud callout's measure, «Pour aller
  plus loin» 6 px under the FAQ's last row, O4 (`.section--verso > .t-prose` 1.06 : 1 on the pre-evaluation).
- **W3-D**: O3 (the wizard's sticky foot, its 20 px radios), O6 (`role="alert"` on a list in
  `components/option_cards.html`, `portal/situation.html`; `news/_newsletter.html` to its owner).
- **W3-B**: O5 (`.panel__head` does not wrap under text spacing), the dashboards' equal sheets.
- **W3-C**: `SCAN_BADGES` beside the registry, «En retard» drawn as a refusal, the third row's chip off its column.
- **W3-E**: «Mes formations»' bare capitals, the hand-written console labels.
- **W2-B**: the placeholders that repeat their labels; the sign-up's name field without `autocomplete`.

### Tests (one pytest at a time, `test_ile_v5_l8`)

- `tests/frontend/test_layout.py`, `apps/accounts`, `test_chips_registry`, `test_state_chips_carry_a_register`,
  `test_o14_lint`, `test_v5_tokens`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`,
  `test_design_docs`, `test_components_w1_c`, `test_chips_cards_w1_c`, `test_template_comments_do_not_leak`:
  **938 passed** (the one red was a bundle mtime after a stash, content unchanged; rebuilt, green).
- `tests/i18n/test_rtl_browser.py -k form`: 2 passed. `test_browser_w1_c.py` + `test_browser_chips_w1_c.py`:
  24 passed after the primary's expected height on the public form went 44 → 52 (M3).
- New: `test_the_password_control_is_a_glyph_with_one_channel_and_the_help_can_hold_a_list`, the P1 guard, the
  M3 / A1 / A3 assertions. The full suite is the integration checkpoint's.
