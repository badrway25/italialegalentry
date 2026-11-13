# W1-A · implementation notes

The family's frontend engineer with the typography director (label w1-a-impl-1). Append-only: each step adds a dated
section. Heavy evidence (captures, audits, logs) under `C:/tmp/ile_v5_council/evidence/v54/w1-a/` (E/ below), outside
every repository. Lane 3: dev server 8783 on `ile_v5_l3`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
`--noreload`; pytest on `test_ile_v5_l3`; signed-in pages through sessions minted by `Client.force_login` on
`ile_v5_l3` (`E/tools/mint_sessions_l3.py`, outside the repository; no password used, typed or stored). Every heavy step
went through `servers/lock_gate.py` first. The page is «V4 + fondation» everywhere until its own family passes (plan
§2.1): nothing below is reported to the owner as V5 (§6).

---

## Step 1 of 3 — fonts and tokens (5 October 2026)

### What was done

1. **Audit and curation** (plan §5.1 step 2; `TOOL_LOG.md`). The current product measured on lane 3 at `v54/base`
   (home, login, dashboard, documents; fr and ar; 1440 × 900 and 390 × 844; `E/before-lane/audit.json`), eleven
   UI-UX-Pro-Max calls read against it, seven weaknesses ranked (fonts 219–519 KB a page; 57–65 % of console text under
   14 px, one node at 9.36 px; typed text at 15 px; 11 sizes and 20 line-heights off the 4 px line on the home; 10 / 14 /
   20 / full corners; four shadow values in the dashboard's first viewport; three focus styles on one page). 21st.dev not
   used (no component). The Emil principles as the checklist, through MOTION_SYSTEM / EMIL_SKILL_INTEGRATION.
2. **The faces** (`static/fonts/v5-*`, `static/fonts/licenses/`, `docs/design-v5/FONTS_V5.md`). Five faces of type
   «Una voce» in six files, from the gate-0 foundation, built reproducibly by `E/tools/build_v5_fonts.py` (fontTools
   4.60.2, outside the product's requirements): Host Grotesk variable 400–700 and italic 400 (the name table's leftover
   «Light» corrected to «Regular»); «ILE Wordmark» (byte copy); «ILE Mono» (the Plex Mono subset renamed for the Reserved
   Font Name «Plex», IBM's copyright kept, name ID 10 says what changed) **split by unicode-range** into the reference
   core (digits, capitals, `# + , - . / : _`: 2 688 B) and the rest (7 272 B); Vazirmatn variable 400–700 (byte copy).
   The four OFL texts with LF line ends. The plan's «eight woff2» are the gate-0 set: Markazi Text and Source Serif 4 are
   not carried under §1.1.
3. **The cascade** (`static/css/main.css`): `v5/fonts.css`, `v5/tokens.css`, `v5/aliases.css`, `v5/base.css` imported
   after every V4 layer — v5 closes the cascade; `fonts.css` no longer opens it (V1's tokens do).
   - `v5/tokens.css`: the foundation's layers 1 → 3 without «PROOF ADDITION 0» (the brand colours stay declared once,
     in `v2/tokens.css`), with §1.1 (one family; eight public sizes 64 · 36 · 28 · 20 · 17 · 15 · 13 · 12, the display a
     `clamp` 40 → 64; weights 400 / 500 / 600; tracking that stops at 20 px; measures in rem; typed text 16 px; the
     console's eyebrow at 12 and its step up below 48 rem or under a coarse pointer; never under 14 px in Arabic), §1.2
     (lapis «En examen», the nine wisteria primitives gone; the slate information notice; attesa dashed and nullo dotted
     at step 600; the hatch at 0.78; the night marks of C5; the glass at 0.94; «argento» for Istituzione; Persona on
     sand; the C9 literals named), §1.3 («Lo spigolo» 2 · 4 · 6 · 8 · 12 · full on the existing names), §1.4 (five
     shadow levels in `rgba(7, 18, 38, α)`, the glow retired, primaries flat), §1.5 (`--motion-reduced` 80 ms,
     `--ease-turn`; the turn-in / turn-out pair gone; reduced-motion zeroing restated), §1.6 (the focus tokens), §1.8
     (the control heights). Every narrow-viewport and reduced-motion override of a name it declares is restated (a
     top-level `:root` here beats an earlier `:root` in a media query).
   - `v5/aliases.css`: DS V5 §13 — the V1 / V2 / V4 names on the V5 values (the paper, the ink, the night and the accent
     at the same hex; the audiences, the states, the materials and the families NOT the same, each line says so). One
     legacy name keeps its V4 meaning on purpose: `--hit-min` stays 44 px for the sixteen V4 controls that read it until
     W1-C retargets them (V5's floor is 24 px on a fine pointer).
   - `v5/base.css`: written for the last position, not copied (the proof's reset placed last would have flattened every
     heading): the weights and tracking of the type roles; **the name in «ILE Wordmark» wherever it is rendered** (the
     lock-up, the rail, the hero's name line, the footer's legal line, the `{% brand %}` classes — `:root`-lifted over
     the app sheets that load after `main.css`); **«ILE Mono» in its one seat** (the legacy sheets' footer labels, shore
     names, questionnaire count, journey / timeline dates and chip counters take the sans with tabular figures — the
     reason a public page downloads no mono); links in the accent; **the one focus system** (`:focus-visible` only, 2 px
     laguna-550 at 2 px on the element's radius, the halo on text fields only, `Highlight` in forced colours; the night
     contexts re-point the ring through the token); typed text 16 px (the one `!important`: `entrance.css` sets the login
     fields at (0,5,1) after `main.css`); Arabic titles 600 at 1.4 with no tracking, labels without capitals, emphasis by
     weight.
4. **The head** (`templates/base.html`): the per-script preload policy of §1.1 — Latin: Host Grotesk + the wordmark (2);
   Arabic: Vazirmatn + Host Grotesk + the wordmark (3).
5. **Deletion map, W1-A rows done in this step**: `static/css/fonts.css` and the 26 V4 woff2; V1 `base.css`'s links and
   focus (moved to `v5/base.css`); the eleven names V5 adopts from `_legacy-tokens.css` (`--radius-xs/sm/md`,
   `--control-height(-sm)`, the five `--focus-ring-*`, `--z-modal`) — ceilings lowered to 142 tokens / 1 515 usages.
   Left for the propagation step: the declarations of V1 `tokens.css`, `v2/tokens.css` (brand colours kept) and
   `v4/tokens.css` that `v5/aliases.css` re-declares, and V1 `base.css`'s type roles and digits (they now render the V5
   values through the aliases; deleting them needs `v5/base.css` to carry their margins first, measured page by page).
6. **The build**: `scripts/build_css.mjs` learns the `_` partial rule (DL54-15); `npm run build:css` rebuilt
   `static/css/dist/main.css`. `npm run build` also rewrites `static/js/dist/` with different chunk names in this
   worktree (esbuild resolves the `node_modules` junction to design-v5's tree): the JS sources are unchanged, so the JS
   bundles were restored to the committed ones and left to the steward's clean rebuild.
7. **Tests** (plan §2.7, W1-A rows): `tests/frontend/test_v5_tokens.py` (new; 470+ contrast pairs on the effective
   cascade, the C5 separation in four visions by Machado 2009 + OKLab, the faces, the scale, the corners, the shadows,
   the DS 2026 css blocks); `test_v4_tokens.py`, `test_static_assets.py` (:133–171, on the effective cascade),
   `test_design_docs.py` (fonts, cascade, focus), `test_layout.py`, `test_browser.py`, `test_rtl_browser.py` (fonts),
   `test_rtl_static.py` (recursive, with the LTR-stage allow-list), `test_css_bundle_is_current.py` (the `_` rule),
   `test_legacy_token_shim.py` (ceilings).
8. **Docs**: DS 2026 §2 (the V5 rows, regenerated weights), §5 (contrast on the effective cascade), §6 (type «Una voce»,
   with its css block), §7.5 (corners, shadows, controls, with their css block), §17 (the shim's countdown);
   `docs/design-v5/FONTS_V5.md`.

### What was measured (lane 3, unthrottled; E/after-1 … after-3)

- **Font bytes a page downloads** (from the requests the browser made; V4 from the W1-0 «before» set on 8782):

  | Page | V4 | W1-A | Budget |
  |---|---|---|---|
  | Latin public (home, login, door, FAQ) | 304 340 / 217 732 B | **20 956 B** (Host + the wordmark) | ≤ 25 KB |
  | Latin console (dashboard, documents, case file) | 217 732 B | **23 644 B** (+ the mono core) | ≤ 32 KB |
  | Arabic public | 484 456 – 525 044 B | **53 184 B** (Vazirmatn + Host + the wordmark) | ≤ 56 KB |
  | Arabic console | 484 456 B | **55 872 B** (+ the mono core) | ≤ 56 KB |

  Before the mono split the Arabic console downloaded 63 612 B (the whole 9.1 KB subset for one case reference): the
  split is what brings it under the budget. Font preloads: 2 on a Latin page, 3 on an Arabic one.
- **CSS**: `dist/main.css` 217 057 → 238 213 B raw; gzip 9 (whitenoise's level) 35 978 → **42 542 B** (+6.4 KB; the
  hashed copy on 8782 adds ≈ 300 B). Inside the Wave-1 allowance (each page type ≤ its baseline + 8 KB: home
  39 114 → ≈ 45.7 KB of 47 306; dashboard 41 668 → ≈ 48.2 KB of 49 860) and under the 45 KB ceiling of `main.css`. The
  headroom left for W1-B, W1-C and W1-D inside +8 KB is ≈ 1.6 KB: the remaining W1-A deletions (the re-declared V1 / V2
  / V4 token declarations) are what make room — measured in the propagation step.
- **Type** (computed styles of every visible text node): the home at 1440 carries 10 distinct sizes (V4: 11), the
  login 8, the dashboard 8 (V4: 9); text under 12 px on the dashboard at 1440: 0 nodes (V4: 12 at 11 px). Typed text:
  16 px on the login and the documents search (V4: 15).
- **Corners on the first screen** (painted boxes, by script): home 1440 — 6 · 8 · 12 · full (V4: 10 · 20 · full);
  login 1440 — 6 · 12 · full; dashboard 1440 — 4 · 6 · 8 · full (V4: 10 · 14 · full; 6 too at 390). The V4 composition
  reads the role names (buttons on `--radius-md`, the hero legend on `xl` …), so two screens show four values: the fold to
  three is counted on the boards and in the three-screen comparison (§1.3), and done in aliases or in the owning
  family's files.
- **Shadows in the first viewport**: dashboard 4 distinct values, case file 5 (V4: 4 / 5) — SH-8's caps are the console
  families' (W3-A, W3-B); W1-A only re-valued the levels.
- **Health**: 0 CSP violations and 0 console errors on every page audited, fr and ar, 1440 and 390 (home, login,
  dashboard, documents, case file, the persons' door, FAQ); 0 horizontal overflow (the one «overflow» flagged is Django's
  DEBUG 404 page on the lane, not the product's error page).
- **Looked at**: the home, the login, the dashboard and the documents in fr and ar at 1440 and 390, the persons' door and
  the FAQ — captures in `E/after-1/`, `E/after-2/`. The name in «ILE Wordmark» in the letterhead, the rail and the hero;
  Host Grotesk everywhere else; Vazirmatn on the Arabic pages with the Latin runs in Host; the chips on the V5 registers
  (amber dashed «Brouillon», «À remplacer»); the flat primaries (the hero's on night is the paper plate). Fixed after the
  first look: the Arabic hero's name line took the Arabic title leading (1.4) — the name is excluded from the Arabic rule;
  the footer's mono labels pulled 9.1 KB of mono onto every page — ILE Mono's one seat. After the sweep of seventeen
  more page types (project, forum, orientation, glossary, privacy, contact form, signup, profile, journey, deadlines,
  messages, helpdesk, academy, «Ma situation», the company dashboard, antifraud, a pathway; fr and ar, 1440 and 390;
  `E/after-sweep/`): the forum page downloaded 35 952 B of fonts for one italic note — the portico's three legacy
  italics are set roman (italics belong to the titles of acts cited in sources): 21 556 B; the home's door-card titles
  (capitals in the locked copy) and the pilot chapter's title, set in the serif at 400 / 300 by V4, read as form labels
  in Host at those weights — they take the title weight, the door titles the capitals' tracking (`E/after-4/`); the
  phone console's bottom-bar labels were a literal 11 px — 12 px in Latin on the bar's own 14 px line (at 12/16 the
  second line was clipped; `E/after-5/`, `E/after-6/`).
- **Swap CLS** (`E/tools/cls_swap.py`, the typography lane's method: every woff2 held 1.5 s, the layout shifts summed;
  Windows fallbacks; `E/cls-swap-1/cls_swap.json`): with the matched fallbacks 0.0000 – 0.0009 on the home (1440, 390),
  the login, the dashboard, the documents (1440, 390), the Arabic home (390) and the Arabic dashboard — all ≤ 0.01;
  with the overrides stripped («bare») up to 0.0200 (documents, 390): the fallbacks are load-bearing.

- **The seven browser files** (`-m browser -rs`: `apps/ecosystem`, `apps/pages`, `apps/portal`, `tests/frontend/test_browser.py`,
  `test_design_preview.py`, `test_header_fits_the_narrowest_viewport.py`, `tests/i18n/test_rtl_browser.py`), at
  `bb63683`, 11:22 → 11:33: **1 failed, 76 passed, 2 skipped** (`E/suites/s2_browser.log`, `.xml`). The failure was W1-A's
  own retargeted test (Chromium serialises the one-word family `Vazirmatn` without quotes) — fixed (`609b693`) and
  re-run green; the 320 px header, every RTL layout check, the pages' and the portal's browser tests passed on the V5
  faces. The **2 skips are `v54/base`'s** (the Forum banner's date gate, `apps/pages/tests/test_browser.py:84, :117`,
  W1-0's run: 77 passed, 2 skipped): the steward's merge runs at 0 skips once design-v5's clock fix lands.
- **Re-run after the fixes**, 11:35: the slice's file-based tests (`test_design_docs`, `test_css_bundle_is_current`,
  `test_v5_tokens`, `test_static_assets`, `test_design_showcase`, `test_legacy_token_shim`, `test_rtl_static`,
  `test_documentation`): **1 failed, 642 passed, 1 xfailed** — the one failure is the steward's path in
  `docs/ACCESSIBILITY.md` (above); `test_documentation.py::test_cited_paths_exist` passes once the RTL browser run has
  written `docs/qa/rtl/`.

### Questions met during the build — for the Creative Director to enter in DL54 (plan §5.2)

Each was decided at the implementer's level to keep the build moving, is reversible in one place, and is written here
with its reason and evidence for the CD to confirm or overturn (DL54 is the CD's to write):

1. **«ILE Mono» served in two files** (the reference core and the rest, complementary `unicode-range`s): the whole subset
   put the Arabic console at 63.6 KB of fonts against the 56 KB budget; with the core it is 55.9 KB. Evidence:
   `E/after-1/audit.json` vs `E/after-3/audit.json`; `docs/design-v5/FONTS_V5.md` §2.
2. **`--hit-min` keeps its V4 meaning (44 px)** in `v5/aliases.css` until W1-C retargets the sixteen V4 controls that read
   it; V5's 24 px floor would have shrunk them on narrow layouts.
3. **No italic on the portico**: the forum's note and the two banner quotes set roman (plan §1.1's rule; 14 KB saved on
   the forum page). Evidence: `E/after-sweep/` vs `E/after-forum/`.
4. **The home's V2 titles at the title weight** (the door cards — capitals in the locked copy, tracked +0.02 em — and the
   pilot chapter): at the serif's 300 / 400 in Host they read as labels. Evidence: `E/after-4/_crop-doors.png`.
5. **The phone console's bottom bar**: Latin labels at 12 px on the bar's own 14 px line (the 4 px line would clip the
   second line inside the fixed 56 px bar); the Arabic labels stay at V4's 11 px for W3-A, because at the 14 px floor
   the bar clips them. Evidence: `E/after-5/_bottombars.png`, `E/after-6/_bottombars.png`.
6. **Typed text 16 px with the one `!important`** of `v5/base.css`: the field rules of `components.css` (0,4,1) and of
   `entrance.css` (0,5,1, loaded after `main.css`) would otherwise keep 15 px on the login.
7. **Host Grotesk's name table corrected** («Light» → «Regular», the axis starts at 400) — the «check» plan §2.3 asked for,
   carried out as a correction since the family has no Reserved Font Name.
8. **The recursive RTL guard** exempts boxes centred from the physical centre (`inset: 50%` + −50 % on both axes: the same
   in both directions) and lists one known legacy defect with its owner (`.btn.is-busy::after`, W1-D) instead of fixing
   another family's sheet.
9. **The hero's name keeps one leading on every page** (1.0625): v4/hero.css's Arabic title leading, written for Arabic
   text, spread the Latin name on `/ar/`. Evidence: `E/after-8/_name-ar.png`.

### Suites (plan §2.7, row W1-A) — on lane 3 (`test_ile_v5_l3`), each behind the lock gate

- **`pytest -m "not browser"`, in full** (compliance and security included; `test_design_showcase.py` and
  `test_legacy_token_shim.py` inside it), at `2b0cffc`, 10:26 → 11:20: **28 failed, 3 841 passed, 3 skipped, 1 xfailed**
  (`E/suites/s1_not_browser.log`, `.xml`). Of the 28:
  - **25 are `v54/base`'s own**, reproduced by W1-0 at `889c6b1` before any family (`E/../w1-0-repo/h1_not_browser.log`):
    `tests/i18n/test_ui_translations.py` ×3, `apps/forum/tests/test_forum_page.py` ×3 and `test_forum_registration.py`
    ×12, `apps/pages/tests/test_home.py` ×6, `apps/pages/tests/test_models_admin_seeds.py` ×1 (the date gates; the
    brief: «not ours: merge design-v5 when its clock fix lands»). The base's two portal failures (a UTC-vs-Rome date
    window) passed in this run.
  - **1 was W1-A's and is fixed**: `test_design_docs.py::test_documented_file_weights_are_roughly_true` — v5/base.css grew
    after the last regeneration; regenerated (`bb63683`).
  - **1 is the steward's** (outside W1-A's slice): `test_design_docs.py::test_cited_paths_exist` — `docs/ACCESSIBILITY.md`
    §13 G-15 cites `static/css/fonts.css`, which W1-A removes by the plan; one path to change.
  - **1 is the worktree's state, not the code**: `tests/i18n/test_documentation.py::test_cited_paths_exist` —
    `docs/I18N_RTL.md` cites `docs/qa/rtl/`, the git-ignored folder the RTL browser suite writes its captures into; this
    fresh worktree had never run it. It passes after the browser run (below).


### Left, and for whom

- **W1-A, step 2**: the three scored boards (`templates/dev/designpreview/specimens/{type,colour,corners}.html`) — C8's
  check («argento» read as a hue on night beside the other three; on the V4 hero's legend it reads as near-white), the
  three-screen corner comparison with its radii count, the reference side-by-sides (GOV.UK, Collège de France, Mercury).
- **W1-A, step 3**: the rest of the deletion map (the re-declared V1 / V2 / V4 declarations, V1 `base.css`'s type roles
  and digits), the DS 2026 §5 table on V5 values, «no page worse» on the 316 pairs (after the steward completes the
  before-set), the swap CLS measurement (Windows and Android fallbacks) and the performance PASS on 8782 by the
  Performance Lead.
- **Steward**: `docs/ACCESSIBILITY.md` §13 G-15 cites `static/css/fonts.css`, which W1-A removes (plan §2.3): one path
  to change (to `static/css/v5/fonts.css`), outside W1-A's slice — `tests/frontend/test_design_docs.py::test_cited_paths_exist`
  fails until it is changed. Two other one-path corrections of the same cause were made in DS 2026, outside W1-A's
  sections (the documented-sources header, §21 G-15) — named in the commit.
- **W1-P**: `templates/dev/designpreview/{frame,compare}.html` link `css/fonts.css` (removed): the preview's bar loses
  its faces until they link `css/v5/fonts.css` (or nothing: `dist/main.css` carries them).
- **Unassigned**: `apps/core/dev.py` and `static/css/dev/showcase.css` (the `/_design/` swatches still describe the V2
  palette; `test_design_showcase.py` is green on it) — retargeting the showcase to the V5 palette needs those files;
  `scripts/fetch_fonts.py` generated the removed `fonts.css` and is now a dead tool.
- **W1-C**: `--hit-min` back to V5's meaning once the V4 controls read `--control-*` / `--hit-primary`; the field's
  200 ms drawn rule and its halo (the field rules of `components.css` and `entrance.css` still win over the global
  halo); the buttons' own focus halos (`v3/buttons.css`, `v4/buttons.css`).
- **W3-A**: the phone console's bottom bar — its Arabic labels stay at V4's 11 px: at 14 px (the Arabic floor) they wrap
  and the fixed 56 px bar clips them; the bar's geometry (height, label policy) is the console shell's.
- **W1-D**: the busy notches' RTL offset (`v4/buttons.css` `.btn.is-busy::after`, listed in
  `test_rtl_static.KNOWN_UNMIRRORED`), retired with the L2 key.
- Not computed (no font file on this machine): Apple's own system faces (SF, Helvetica, Geeza Pro) and the Android
  Arabic face — before the milestone (plan §7).

---

## Step 2 of 3 — tests and docs (5 October 2026, label w1-a-impl-2)

The family's frontend engineer with the typography director. Brief of the step: retarget or retire the V4 pins plan
§2.7 gives W1-A, write DS 2026 §2 (prose), §5–§8, §12, §17 and `docs/design-v5/FONTS_V5.md`, run the W1-A suites on
lane 3. No stylesheet, template or font changed in this step: every page renders as at `1cc2c15`, so no page was
re-captured (the boards, «no page worse» and the performance PASS are not this step's). Commits `1a15537` … `eba98a0`
(listed at the end of the section).

### What was done

1. **`tests/frontend/test_v5_tokens.py`** — the PLATFORM_COLORS checks D-doc-6 asks for are now all held: night
   separation, edges and patterns at 3 : 1, plates and glass over night (step 1) and **the tones on the selected and
   disabled surfaces** (new: every register's word, mark and broken edge on `--surface-selected` and
   `--surface-disabled`). C3's broken edges enter the pairs. **PC §6.3's 23 pairs** are each answered, by test: 3 hold
   now because a token changed (the link over the glass on night, C7, 5.39; Istituzione on the night plate over a white
   pixel, C8, 5.16; Persona on it, O19, 4.56); 20 are kept off every page by a written rule — C6 (over a photograph the
   plate is `--plate-night-photo` or a scrim, never `--plate-night`; the AA scrim carries `--text-on-night-1` alone;
   `--text-on-night-3` never meets a photograph), D-doc-2 (`--text-on-night-3` never on notte-700) and the disabled
   surface (it carries no state: nullo's mark and dotted edge would be 2.89 there) — and DS 2026 §5 lists each with its
   measured ratio; a ruled-out pair that came to hold would fail until moved. The brand / literal-colour /
   register-never-green rules of `test_v4_tokens.py:265, 275, 291` are extended to **every V5 sheet** — main.css's four,
   the page partials, the console partials — with the generated `_loader-light.css` allow-listed by name. **The console
   partials close the console entry** (plan §2.7: imported by it, never by main.css, last, and once there is one the
   entry keeps no rule of its own — vacuous today, a guard for W3-A). **SH-1**: V5 declares the five levels (1–4, their
   night twins with the same offsets, the door's) and no other shadow; `--shadow-5` is level 4. **DS 2026 §5's V5 table**
   and its stated count of pairs are recomputed from the cascade; **FONTS_V5.md's** table is held to the bytes and the
   SHA-256 of every shipped woff2 and to the opening of each licence's hash.
2. **`tests/frontend/test_v4_tokens.py`** — V4's six shadow roles retired into SH-1's five levels (above), with the
   contrast helpers no test used any more; what stays is true of the V4 sheets themselves (docstring).
3. **`tests/frontend/test_static_assets.py`** — the comment above the 29 V1 pairs said they were checked against
   `--paper #FAF7F0`; it now says they are read on the effective cascade (step 1 retargeted the reading).
4. **`tests/frontend/test_design_showcase.py`** (plan §2.7, «the V5 palette») — a named token must exist in the cascade
   every page loads and a swatch rule must paint one that does (not `v2/tokens.css` alone). The caption check is added as
   a **strict xfail** with its reason: `apps/core/dev.py` prints its captions from `v2/tokens.css`, and **14 of the 44
   captions** name a hex no page paints (V4's night, 8; V5's states and seal, 6). `apps/core/dev.py` and
   `static/css/dev/showcase.css` have no owner in `OWNERSHIP_V54.json`: the full retarget needs the steward's assignment
   (below). Strict, so the fix cannot pass unnoticed.
5. **`tests/frontend/test_css_tokens_exist.py`** — «kept, plus the `_` partial rule»: the sources are read, a partial
   included wherever it is, and never the `dist/` bundles (an output must not vouch for a name its sources lost).
6. **`tests/frontend/test_design_docs.py`** (W1-A's functions only) — `:612`: every non-partial sheet of `static/css` is
   a layer of main.css; every partial is reached from an entry (main.css, or an app entry: the page sheets, the console
   entry, directly or through what they import). `:500–512`: a component's CSS block may live in the cascade, in the
   design system's page and console partials, or in the app entries. `:1050`: the reserve labels read the design
   system's partials wherever they live; the app sheets' own rules stay out (question 12). Probed on the tree with an
   orphan partial and an orphan layer (both caught, by this test and by `test_css_bundle_is_current`) and with a partial
   imported by `pages.css` (accepted; the probe files were removed and the page sheet's mtime restored).
7. Re-verified, unchanged from step 1: `test_css_bundle_is_current.py` with the `_` rule of `scripts/build_css.mjs`;
   `tests/i18n/test_rtl_static.py` (recursive, Vazirmatn); `test_browser.py:211–220`; the fonts slices of
   `test_layout.py` and `test_rtl_browser.py`; the fonts, cascade-order and focus functions of `test_design_docs.py`;
   `test_legacy_token_shim.py`'s ceilings.
8. **DS 2026** — **§5** rewritten in two parts: 5.1 the effective cascade (how it is measured, the rules that follow, a
   75-row table every row of which the test recomputes, the ruled-out table with the rule of each pair); 5.2 the V1
   literal table, kept and labelled as the first layer's declarations — its two checkers are outside W1-A's functions
   (question 13). **§2** (prose): where page-only and console-only CSS live and the three tests that hold the rule.
   **§6.4**: the swap CLS measured on the product. **§7.5**: the one focus system of plan §1.6 in prose. **§7.6** (new):
   SP-1 … SP-8 and RH-1 … RH-8 as binding rules, with the spacing tokens in a css block the cascade test reads. **§8**: a
   V5 block — the name in ILE Wordmark, the rubric in ink since V2, the four filets, the folio, the entry, the plate and
   the note on their effective values, O57, the eight registers. **§12**: what the reduced-motion block zeroes and keeps,
   the five curves. **§17**: a row is the shim's declaration; the two names `static/css/v5/aliases.css` re-declares
   (`--radius-pill`, `--font-mono`); the eleven adopted names; the radii, controls and focus subsections (the empty focus
   table removed).
9. **`docs/design-v5/FONTS_V5.md`** — the swap CLS (§4) and §6, the tests that hold the file.
10. **For the steward** — `docs/design-v5/QA/v54/w1-a/STEWARD_PATCH_A11Y_G15.diff`: the one path of
    `docs/ACCESSIBILITY.md` G-15 that still names the removed `static/css/fonts.css` (A11Y §13 is outside W1-A's slice).
    Applied on the tree and tested — `test_design_docs.py` 40 passed — then reverted; the file is unchanged.

### What was measured (from the cascade; the files on disk)

- **Contrast on the effective cascade: 502 pairs held, 0 below their minimum** (466 at step 1; + C3's edges 10, + D-doc-6
  26). The weakest of each family: text `--text-3` 5.10 on the selection wash; a register's word 5.38 (nullo) and mark
  3.28 (nullo) on its body; the broken edges 3.14 – 3.96 (C3); the hatch 3.05 on the amber mark (C4), the dots 3.94, the
  cross 3.59; the night marks ≥ 3.05 on notte-700 (nullo), closest pair 0.052 in OKLab (neutro / rifiuto, protanopia) —
  0 of 28 under 0.05 in four visions (C5); «Italy» over the glass on night 4.62 (C7); the focus ring ≥ 3.41 on paper
  (the selection wash), 3.55 on the lapis body (C1); the marks on the selection wash ≥ 3.11 (nullo), on the disabled
  surface ≥ 3.05 (attesa).
- **PC §6.3: 23 → 3 answered by tokens, 20 ruled out** (the table above, DS 2026 §5).
- **The showcase**: 14 of 44 captions print a hex no page paints.
- **The family's file tests** after the last commit (`test_v5_tokens`, `test_v4_tokens`, `test_static_assets`,
  `test_legacy_token_shim`, `test_design_showcase`, `test_css_tokens_exist`, `test_css_bundle_is_current`,
  `test_design_docs`, `test_rtl_static`, `test_layout`, `tests/i18n/test_documentation.py`): see «Suites» below.

### Suites (plan §2.7, row W1-A) — on lane 3, each behind the lock gate

- **The seven browser files** (`-m browser -rs`: `apps/{ecosystem,pages,portal}/tests/test_browser.py`,
  `tests/frontend/test_browser.py`, `test_design_preview.py`, `test_header_fits_the_narrowest_viewport.py`,
  `tests/i18n/test_rtl_browser.py`), at `0442b1a` (the later commits change DS prose only), 12:34 → 12:50: **77 passed,
  2 skipped, 0 failed** (`E/suites/s4_browser.log`, `.xml`). The 2 skips are `v54/base`'s, the Forum banner's date gate
  (`apps/pages/tests/test_browser.py:84`, `:117`) — the «+ 2» of the brief, until design-v5 receives the clock fix
  (`evidence/v54/clock-fix/NOTE.md`: the two `pytest.skip` become assertions). Two lane-3 test databases, so that two
  runs never share one: the full suite on `test_ile_v5_l3` (`TEST_DATABASE_URL` naming `ile_v5_l3`, as the lane's `.env`
  and the family brief have it — Django adds `test_`), the browser run and the file tests on `test_test_ile_v5_l3` (the
  URL this step's task names, `…/test_ile_v5_l3`); the second is left in place for `--reuse-db`. The dev server 8783 was
  not started: no page changed in this step. The gate found the lock taken at 12:33 by a W1-P performance reviewer's 5-minute burst on 8791, and
  waited 75 s; the full suite below had started at 12:25:49 under an absent lock and was not stopped (another lane's
  full suite was running too).
- **The family's file tests on the final tree** (`test_v5_tokens`, `test_v4_tokens`, `test_static_assets`,
  `test_legacy_token_shim`, `test_design_showcase`, `test_css_tokens_exist`, `test_css_bundle_is_current`,
  `test_design_docs`, `test_rtl_static`, `test_layout`, `tests/i18n/test_documentation.py`), at `eba98a0`, 12:58 →
  13:01: **758 passed, 2 xfailed, 1 failed** (`E/suites/s5_family_files.log`, `.xml`). The failure is the steward's
  path (`test_design_docs.py::test_cited_paths_exist`, A11Y G-15; the patch above makes it pass). The xfails: the shim's
  finish line (`test_the_shim_is_gone`, since 21 September) and the showcase's captions (question 11).
- **`pytest -m "not browser"`, in full** (compliance and security included), at `585bd65` + the DS prose commits that
  followed while it ran: **26 failed, 3 869 passed, 3 skipped, 79 deselected, 2 xfailed**, 12:25:49 → 13:37:56
  (1 h 12 min: the machine carried another lane's full suite and, for 16 minutes, the browser run above;
  `E/suites/s3_not_browser.log`, `.xml`). The modules were collected at `585bd65`; the commits that followed while it
  ran change DS prose and one assertion of `test_v5_tokens.py`, re-run on the final tree in the line above. Of the 26:
  - **25 are `v54/base`'s own** — the same 25 as W1-0's base run and step 1's: `tests/i18n/test_ui_translations.py` ×3,
    `apps/forum/tests/test_forum_page.py` ×3, `test_forum_registration.py` ×12, `apps/pages/tests/test_home.py` ×6,
    `test_models_admin_seeds.py` ×1 (the date gates; the brief's «27 + 2» counts the base's two portal failures, which
    fail only between 00:00 and 02:00 in Rome: they passed);
  - **1 is the steward's path**: `tests/frontend/test_design_docs.py::test_cited_paths_exist` (A11Y G-15, patch above).
  The 3 skips are `apps/cases/tests/test_intake.py:133, :209, :238`, data-dependent and the base's own (W1-0's run has
  the same three); the 2 xfails are the shim's finish line and the showcase's captions (question 11). **Nothing W1-A
  wrote fails.**

### Questions met during the step — for the Creative Director to enter in DL54 (plan §5.2)

Numbered after step 1's nine. Each was decided at the implementer's level, is reversible in one place, and carries its
reason and evidence:

10. **The disabled surface carries no state.** PC §6.3's last pair — nullo's mark (and so its dotted edge) on
    `--surface-disabled`, 2.89 : 1 — is ruled off every page rather than answered by darkening cenere-600, which would
    move nullo's rung on the paper ladder and its separation from neutro. In `static/css/` the disabled surface is only
    the fill of the disabled button (`v3/buttons.css`) and of the V5 disabled-control tokens; no register is drawn on
    it. Evidence: `test_v5_tokens.py::test_the_23_pairs_of_pc_6_3_are_answered`, DS 2026 §5 (the ruled-out table).
11. **The showcase's caption check is a strict xfail**, not a green test on V2 values: `apps/core/dev.py` and
    `static/css/dev/showcase.css` have no owner, so the V5 palette cannot be shown on `/_design/` from W1-A's slice
    (plan §2.7 assigns the test to W1-A, the manifest gives it neither file). Evidence: the xfail's reason; 14 of 44.
12. **`test_design_docs.py:1050` reads the design system's partials, not the app sheets' own rules.** The plan's row
    says «read the console entry and the page sheets»; read literally, `--width-form` (consumed by `companies.css`) would
    stop being a «riserva» and turn the suite red on a §3 row no family owns, against the test's own contract («an app
    stylesheet may consume a reserve token»). The partials the console entry and the page sheets import are read, the
    entries' own rules are not. `:500–512` (component blocks) reads all of them: there more sources cannot mislead.
13. **DS 2026 §5's V1 table is kept and labelled, not converted.** Its two checkers
    (`test_contrast_table_matches_recomputed_ratios`, `test_contrast_table_covers_every_pair_locked_by_the_asset_tests`)
    are outside W1-A's functions of `test_design_docs.py`; the V5 table beside it is held by `test_v5_tokens.py`. The V1
    table leaves with the V1 declarations in the deletion step (step 3), and its checkers then need an owner or W1-A's
    slice widened by the steward.
14. **The console partials close the console entry structurally**: once `console.css` imports a V5 partial it may keep
    no rule of its own (CSS puts every `@import` first, so a rule left in the entry would beat the partials). This
    binds W3-A's file; the alternative — `@layer` — would be a second cascade mechanism the product does not use.

### Left, and for whom

- **Steward (at the merge)**: apply `docs/design-v5/QA/v54/w1-a/STEWARD_PATCH_A11Y_G15.diff` (A11Y §13 G-15 still names
  `static/css/fonts.css`; `test_design_docs.py::test_cited_paths_exist` fails until then — the one family-file failure of
  the suites above). **Assign `apps/core/dev.py` and `static/css/dev/showcase.css`** (to W1-A's step 3, or to W1-P with
  the preview) so the showcase reads the effective cascade and shows the V5 palette — the strict xfail then has to go.
  **DS 2026 §9** («Elevazione: nessuna», «Raggio: 0», two-tone focus rings) and **§1, principle 7** («anello di focus a
  due toni su ogni superficie») contradict §7.5 and are in no family's slice; W4-D's «DS 2026 final» or an
  assignment. The two checkers of question 13, for step 3.
- **W1-A, step 3** (not this step's brief): the three scored boards (`templates/dev/designpreview/specimens/{type,colour,
  corners}.html`) with C8's reading and the three-screen corner comparison — step 1's notes placed them in step 2, the
  workflow's step 2 is tests and docs; the rest of the deletion map (then DS §3, the V1 §5 table and their checkers); «no
  page worse» on the 316 pairs; the swap CLS with the Android fallback; the performance PASS on 8782 (Performance Lead).
- **W3-A**: the console partials rule above, when the first one arrives.
- **W1-D**: `_loader-light.css` is allow-listed by name for literal colours (`GENERATED_SHEETS` in `test_v5_tokens.py`);
  like every partial and app sheet, its keyframes are outside `test_design_docs.py`'s §12 keyframe scan, which reads the
  main.css cascade only — W1-D documents them in its prose of the loader.
- **W1-P**: `templates/dev/designpreview/compare.html` still links `css/fonts.css` (step 1's note stands).

### Commits of the step (on `v54-w1-a`, after `1cc2c15`)

`1a15537` DS 2026 §5 on the effective cascade, held by test_v5_tokens — D-doc-6, PC §6.3's 23 answered ·
`eb90f64` test_v4_tokens retires V4's six shadow roles into SH-1; the asset pairs say which values they read ·
`daf9165` the showcase's palette is the effective cascade; test_css_tokens_exist reads sources, partials included ·
`445f2c9` test_design_docs learns the partial rule · `585bd65` DS 2026 prose — §2, §7.5, §7.6, §8, §12, §17; FONTS_V5 §6 ·
`2ba433b` §6.4 the swap CLS, §5.2 · `364a3e9` §5's count of pairs is the test's · `0442b1a` §8 wording · `eba98a0` §17
wording · and the commit that carries these notes, the tool log's step-2 line and the steward's patch.

---

## Step 3 of 3 — finishing for shipping (5 October 2026, resumed 8 October, label w1-a-impl-1)

V5.5 delivery mode: only what shipping needs. The record of this step is **`docs/design-v5/QA/v54/w1-a/NOTES.md`** — the
merge of design-v5 (`a346e20`), A11Y G-15 (`047e2e2`), the CSS bytes per page type against the Wave-1 allowance (every
page type inside; `dist/main.css` 42 773 B gzip), «no page worse» on the 316 pairs with its two corrections (`9512bea`),
the targeted suites (759 passed, 2 xfailed; browser files: 62 passed, 0 skipped), what was looked at, and what is left and for
whom. The specimen boards and the deletion-map paperwork were not done, by (e) of the step's brief.
