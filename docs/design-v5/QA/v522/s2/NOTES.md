# V5.22 lane S follow-up — the four red guards, P2's merge conditions, lane H's requests (label v522-s2-build)

Branch `v522-s2` from design-v5 `269cf39` (worktree `C:/tmp/ile_wt/v522-s2`). Binding: the owner's V5.22
(`V5_22_EDITORIAL_PATTERN_SECTION_COMPOSITION_REMEDIATION.md`), V5.23, SECTION_SYSTEM_V2 §9.7–§9.9 and §10, the
V5.12–V5.21 standing rules and V5.20's strict test rule. Scope (the orchestrator's task, «lane S follow-up»):

1. the FOUR red guards on design-v5 (DL54-182 item 10 a–c, DL54-183 the tag guard), fixed at the root in the product,
   the guards kept as strong;
2. lane P2's merge conditions on lane S's modules (P2's QA_ROUND3 MC-1…MC-3: `indice.js`, `spia.js`, `mappa.js`), with
   the assertions P2 wrote for them proved;
3. lane H's requests to lane S (H's QA_ROUND3, NOTES §12.5): the index glyph that shrank, «la protezione»'s title on an
   Arabic page, the photo credit's French space, and the first keyboard input's INP at its root — the library's
   `[data-input]` / `:is()` rules and the ONE rule of the preserved `static/css/v5/motion.css`.

- Database lane l3 (`test_ile_v5_l3`; the browser sessions `test_ile_v5_l3b`), one pytest per database at a time.
- Lane server 8783 (dev settings, `ile_v5_l3`, reference date 2026-10-03, G3 open); scratch dev servers outside every
  repository — 8791 the base (`git archive 269cf39`), 8794 lane H alone (its final head `4afed99` merged with `269cf39`
  by `git merge-tree`; `c17146f`, its round-3 head, for the first counts), 8792 lane H with this branch (`4afed99` merged
  with this branch's tree) —; three compressed twins for the INP measurement, 8788 (the base), 8789 (lane H + this
  branch) and 8790 (lane H alone), DEBUG off, `CompressedManifestStaticFilesStorage`, their own `STATIC_ROOT`, as 8782 is
  built. All stopped at the end.
- Headed chromium-1234 for every visual check; the test suites headless as designed; every Chromium session inside a
  lock slot (`C:/tmp/ile_locks/CHROMIUM_LOCK_A`/`_B`), each under 25 minutes and released.
- Scripts and raw data: `C:/tmp/ile_v5_council/.work/v522-s2/` (`tools/`, `data/`, `logs/`, `twin/`); evidence:
  `C:/tmp/ile_v5_council/evidence/v522/s2/`.

## 0. In one screen

| Item | State on design-v5 `269cf39` | On this branch |
|---|---|---|
| (a) `test_every_horizontal_shift_has_its_rtl_twin` | red: the route board's light had no RTL twin — in Arabic it glowed at 37–67 % of every rail at rest and ran the wrong way | green: the light waits beyond the rail's start and runs to its end right to left (`sez-run-rtl`) |
| (b) `test_l3_attaches_only_to_fragment_containers` | red: the hemicycle wrote Lume's L3 attribute `data-seat` on its seats (and P1's producer on the sentence's phrases) | green: the pattern's own `data-seggio` on both sides; no element of any page carries `data-seat` |
| (c) `test_data_register_is_written_by_the_partial_and_by_two_legends_only` | red: the library's register marker was the chip's attribute, written by hand in 8 library templates and 8 of P1's | green: the library's own `data-registro`; the chip's `data-register` is again the chip partial's and the two legends' alone |
| (d) `test_a_tag_is_a_term_and_carries_neither_a_register_nor_a_mark` | red since P1's recomposition (5 tags under a floor of 9) | green: updated under the strict rule to the exact remaining set, and the terms' new form (disclosures) held to the same invariant |
| MC-1 (`indice.js`) | a phone's permalink landed on a folded answer; a same-document hash was not followed | applied: the named answer open at arrival on a phone, `hashchange` selects or opens its answer; proved on the library's explorer and by P2's own assertions on P2's tree |
| MC-2 (`spia.js`) | the rail lit the wrong letter where parts share a row | applied (normalised to LF): a row is one stop, a followed link current at once; proved on a grid fixture and by P2's glossary assertion |
| MC-3 (`mappa.js`) | a phone's chosen actor stayed below the screen | applied: the chosen entry comes into view; proved on the library's map |
| H m3 (index glyph) | squeezed to 15.5 px by a wrapped title | `flex: none`: 20 px at every width |
| H m5 («la protezione», ar) | the French title at the right, its French body flush left | one reading-measure column; the title carries its own language: one left-to-right box per element, one start |
| H m7 (credit) | «Foto : …», «Photo : …» on it/en | the space before the colon in French only (a no-break one) |
| H M2 (INP, the first key) | the flip of `html[data-input]` restyled 853 of 1 180 elements on the base home, 1 138 of 1 396 on lane H's home, 774 of 1 024 on Parcours (the whole document) | 525 of 1 396 on lane H's home with this branch, 379 on Parcours; the first Tab and the first pointer after the keyboard measured on compressed twins against the base (§3.5) |

## 1. The four red guards

### (a) The route board's light, right to left — `static/css/v5/_sec-tracciato.css`

**Cause.** `.tracciato__linea::after` (the lane's light, 30 % of the rail, `translate: -110% 0`) had as its only RTL rule
`scale: -1 1`, which mirrors a symmetric gradient and moves nothing. Right to left an over-constrained absolute box
stands at the inline start — the rail's right end —, so `-110 %` left it at 37–67 % of the rail at rest (the glow the
reviewer captured), and the run `sez-run` (−110 % → 360 %) travelled left to right, against the reading.

**Fix.** `[dir="rtl"] .tracciato__linea::after { translate: 110% 0; }` (the box waits beyond the rail's start) and, in
the lit lane's container query, `:root[dir="rtl"]… { animation-name: sez-run-rtl; }` with
`@keyframes sez-run-rtl { from { translate: 110% 0; } to { translate: -360% 0; } }` — the root's own `[dir]`, as lane P1
found its page twin had to be. 1 418 / 1 434 B gzip -9.

**Proof.** The guard green; `test_the_route_board_s_light_waits_beyond_the_rail_s_start_and_runs_in_the_page_s_direction`
(the light's box outside the rail at rest in both directions, the run `sez-run` / `sez-run-rtl`); headed on
/parcours/ fr and ar at 1440 and 390 (§7). Lane P1's page-level twin in `_index.css` (`.percorsi-tracciato`) is now
the library's own and can go (request 8.2).

### (b) The hemicycle's own attribute — `components/sezioni/mappa.html`, `_sec-emiciclo.css`

**Cause.** «L'emiciclo» paired its seats and the locked sentence's phrases through `data-seat`, Lume's L3 attribute,
reserved for the fragment containers `loader.js` seats (`[data-seat].is-seating`; DS 2026 §12, W1-D: «no
server-rendered region seats»). SECTION_SYSTEM_V2 §2 H names the pairing `:has([data-seat="n"]:hover)` as its example;
the steward's record names the fix: «an attribute of the pattern's own (`_sec-emiciclo.css` and the contract with it)».

**Fix.** `data-seggio` (the pattern's vocabulary: `.emiciclo__seggio`) — on the seats (the partial), in the contract
(the sentence's items as `<span data-seggio="n">`), in the sheet's six pairs. The contract's producer is lane P1's
`apps/ecosystem/services.py::recipients_sentence` (one f-string) and P1's `_institutions.css` reads it twice: both
carried here so that the page never breaks (§4, P1's slices). P1's test `test_pages_v522_p1.py` held the old attribute
name twice: updated under the strict rule (§6.2), stronger (no element of the section carries `data-seat`).

**Proof.** The L3 guard green; `test_the_hemicycle_pairs_its_seats_and_phrases_through_its_own_attribute` (six seats and
six phrases carry `data-seggio`, none `data-seat`; a phrase under the hand lights its seat and a seat its phrase);
/fr/ and /ar/institutions/ headed (§7).

### (c) The library's register marker — 8 library templates, 8 of P1's, the three readers

**Cause.** Lane S's NOTES §8 asked every composing lane to mark a register of named entities (§4.10: drawn all or none,
one register for the ≤ 6 body icons) with `data-register` — the chip's attribute, which by construction only
`components/chip.html` and the two legends write («a chip is never drawn without its mark»). The chip guard was red on
the library's templates, and every page sheet's `[data-register]` rules (tokens.css's forced-colours re-pointing of the
chip's tokens) matched the library's lists too.

**Fix.** The library's own `data-registro` (`.registro` is already the codebase's name for a register list): the eight
library templates (`approdo`, `filo`, `flusso`, `indice` ×2, `mappa` ×3, `mosaico`, `tracciato`, `stepper`), the eight
of lane P1 that wrote the marker by S's request (`ecosystem/partials/approdo`, `ecosystem/universities`,
`pathways/_tracciato`, `pathways/detail` ×3, `diplomas`, `index`, `index_interim`, `training`; one attribute token each,
no visible change — §4), and its three readers, each keeping its invariant (§6.2): the O14 lint (an element carrying
either attribute is a status context; two planted cases added for the library's marker, one CSS case), the interior and
the orientation guards (a register is `[data-registro]`, a chip's register mark read as before). DESIGN_SYSTEM_V5 §14.2
names the marker. Lane P2's branch writes the old marker in three templates and reads it in three test lines: request
8.3, with its patch.

### (d) The tag guard — `tests/frontend/test_state_chips_carry_a_register.py`

**Cause.** None in the product: lane P1 turned the pathway sheet's and the diplomas' Italian terms from tags into the
native disclosures of their locked definitions (SECTION_SYSTEM_V2 §3.5 PS-4, §3.10 D1 — approved), so five tags remain
under the guard's floor of nine.

**Update (V5.20 strict rule, cited in the test).** The floor became the exact set of the remaining tags (the community
room ×1, the company need ×2, the helpdesk message ×2: one tag more or less fails — stronger), and the terms keep the
invariant in their new form: a term's disclosure carries no register (the chip's or the library's) and its word no mark,
the chevron being the disclosure's own control beside the word. This is lane P1's request 2 (DL54-183 item 10).

## 2. Lane P2's merge conditions on lane S's modules (QA_ROUND3 MC-1…MC-3)

The three request patches (`evidence/v522/p2/imp2/requests/`), applied with `git apply --whitespace=error`: `indice.js.patch`
and `mappa.js.patch` as written, `spia.js.patch` after normalising its CRLF to LF (m5; the base `spia.js.orig` is
byte-identical to design-v5's). The built chunks: indice 1 238 / 1 536, mappa 1 037 / 1 536, spia 806 / 1 024 B gzip;
`rise.js` 1 325 / 1 536; the three stale chunks removed.

- **MC-1** — `sezioni/indice.js`: a phone opens the answer its address names at arrival (the others folded); a same-document
  `hashchange` (a link to another answer, the address bar) selects it (≥ 64 rem) or opens it and brings its heading under
  the letterhead (< 64 rem), at once from the keyboard and under reduced motion.
- **MC-2** — `sezioni/spia.js`: parts that share a row cross the band together, so they are one stop, marked from its first
  (`aria-current`, the others `data-spia-con`); a followed link is current at once and stays so through the scroll it
  started; the last part lit only while no part holds the band.
- **MC-3** — `sezioni/mappa.js`: a chosen node whose entry stands below the screen brings it into view.

**Proved on this branch** on the library's own fixtures (the explorer, a scroll-spy over a three-column grid, the map;
`test_sezioni_browser_v522_s2.py`, 6 cases), each case red on the base tree and green here (§6.3). **Proved with P2's
own assertions** on a scratch tree outside the repository — this branch merged with `v522-p2` (`f32fa07`, P2's branch
with design-v5 `269cf39` merged in) by `git merge-tree`, P2's half (`p2_with_lane_s.patch`: the phone's first paint,
W1-C's same-document step restored, the permalink test tightened, the spy test) applied, the dist rebuilt —:
`test_pages_browser_v522_p2.py` and W1-C's `test_a_link_to_an_faq_row_opens_it`, **38 passed, 2 failed**. The two
failures are the Forum half of P2's new spy test, and they are its count, not the product: the test expects
`len(seen) == 5`, while in the test database the event is before its date, so the sommaire holds seven links
(`#forum-programme` and `#forum-registration` join the five) — and all seven lit (the assertion's own message lists
them). Its glossary half (every letter followed lights itself, 1440 / 1280 / 1024, fr and ar) passed. Request 8.3:
compare with the sommaire's own link count.

## 3. Lane H's requests

### 3.1 The index glyph — `_sec-indice.css`
`.indice__glifo { flex: none; }`: the glyph is a flex item of the row and shrank to 15.5 px when its title wrapped at
1024–1280 px. `test_an_index_glyph_keeps_its_twenty_pixels_whatever_its_title_wraps_to` (20 px at 1024, 1280 and 1440,
fr and ar, a wrapped title present). With it, H's request 4: the rows' ranks are filed under the row's class
(`.indice__riga:nth-child(n)`, not a bare `:nth-child` tried against every element).

### 3.2 «La protezione»'s French title on an Arabic page — `components/sezioni/protezione.html`, `_sec-strato.css`
The title was a `<span lang="fr">` inside an h2 of the page's direction: the box right to left, its run at the right,
while the French body ran in a 46 rem left-to-right box. Now the h2 carries its own language (`locked_text`, its
`locked_lang` when it falls back — the body's own way; the text byte for byte the locked title), and the plate's
in-flow parts share one reading-measure column (`grid-template-columns: minmax(0, 46rem)` on the plate, in place of the
body's own `max-inline-size`): two left-to-right boxes hung from the same reading edge, one start (§1 rule 6). French,
Italian and English pages: unchanged in position (the same 46 rem column). `test_the_protection_s_title_carries_its_own_language`,
`test_the_protection_s_french_title_is_one_left_to_right_box_on_the_body_s_edge`; headed on the home (lane H + this
branch), Parcours, Formation and Diplômes (§7). One plate, every page that shows it.

### 3.3 The photo credit — `components/photo.html`, `pages/partials/_ingresso.html`
`{% translate "Photo" %}{% if credit_lang == "fr" %}&nbsp;:{% else %}:{% endif %}`: «Photo : …» (no-break, the French
rule of `pages_typo`), «Foto: …», «Photo: …», «صورة: …». No msgid changes. The Forum hero's and the pathway sheet's
captions are whole French runs (`lang="fr"`): their French spacing is right as it is.

### 3.4 The first keyboard input's INP — the library's rules and the one rule of `motion.css`

**Diagnosis** (`tools/inval.py`: Chromium's invalidation tracking and `UpdateLayoutTree.elementCount` around the first
Tab, then around the first pointer after it; `data/inval*.json`). The flip of `html[data-input]` restyles every element
its rules' subjects name. Two rules made Blink give up and restyle the WHOLE document (`allDescendantsMightBeInvalid`):
the preserved `[data-input="key"] .accordion__item::details-content` (Blink cannot scope an invalidation that ends on
that pseudo-element) and the library's `html[data-input="key"] .mosaico *` (a universal subject). Then the library's
tag and class features: the stroke verb's `:is(path, circle, line, polyline)` (every SVG shape of the page) and
`:is(.sez-tile .icon, …)` (every icon). What-if drops on /fr/parcours/ (1 024 elements): 774 restyled at the first Tab;
774 with `.mosaico *` dropped (the accordion rule alone still forced the whole document); 326 with both dropped; 246 with
the tag and icon rules dropped too; 2 with every `[data-input]` rule dropped.

**Changes.**
- `static/css/v5/motion.css` — the one INP rule. `[data-input="key"] .accordion__item::details-content { transition-duration:
  0ms; }` is gone; the keyboard's condition stands on the accordion's own interpolation rule:
  `html:not([data-input="key"]) .accordion { interpolate-size: allow-keywords; }`. From the keyboard the height is not
  interpolable, so the answer opens and closes at once; a pointer still sees it move. `main.css` 32 716 B gzip -9 (−2;
  the ratchet held). Every faithful «custom property read by `::details-content`» form measured +6 to +9 B on
  `main.css` (zeroing `--motion-fast` / `--motion-standard` on the item or the accordion, in every order and place) —
  over the ratchet — so the byte-neutral form was chosen. Its one residue: on a close from the keyboard the discrete
  `content-visibility` flip keeps its 120 ms (`--motion-fast`) as it does for a pointer — invisible (the height is 0 and
  clipped). Recorded for the Director (§9).
- `_sec-mosaico.css` — `html[data-input="key"] .mosaico *` → `.mosaico__soglia` and `.mosaico__tessera` (what moves there;
  the tiles' glyphs, discs, frames and links have their own rules).
- `_reveal.css` — the stroke verb without its tag branch: the dash properties are inherited, so a carrier (an svg, a g, a
  span round a mark — lane P2's drawings) holds them and runs the draw and its shapes follow; a shape that carries the verb
  itself (the home's drawings, the fixtures) draws as before. −23 B on `core/reveal.css`.
- `_sezioni.css` — `html[data-input="key"] :is(.sez-tile .icon, .sez-disc, .sg-g--key)` → three class-led selectors setting
  `--sez-t: 0s`, which the tile's glyph and rule, the disc and the key read in their transitions: the first key restyles
  the tiles, discs and keys, never every icon (H's request 2).
- `_sec-indice.css` — the ranks under the row's class (H's request 4, §3.1).
- Not done, measured: H's request 3 (`_sigillo.css`'s `:is(.sez, .ingresso, [data-sigillo-scope]):has(…)` as three selectors)
  costs 7 B on `fronte.css`, which has 3 B of headroom (6 141 / 6 144) — left for S-close, its cost now spread over far
  fewer restyled elements; the `img` subjects of `_photo.css`'s select grade and `_sec-campata.css`'s settle stay (their
  class-led forms cost 3 and 15 B on the home, which has 7 B left under its ceiling with lane H's final head — 61 433 /
  61 440 —, one without the other changes nothing, the tag staying in the flip's set, and they reach the photographs only).

**Elements restyled at the flip** (`inval5_*.json` for the home — lane H's final head `4afed99`, alone and with this
branch, against the base; `inval4_*.json` / `inval_*.json` for the other pages; headed, unthrottled, 1440 × 900 and
412 × 823; the largest recalc of the interaction, then its time):

| Page | Base `269cf39` | Lane H alone (`4afed99`) | Lane H + this branch |
|---|---|---|---|
| home fr, desk · Tab / pointer | 853 / 853 (18.3 ms) | 1 138 / 1 138 (18.4 ms) | **525 / 522** (16.7 ms) |
| home ar, desk · Tab / pointer | 904 / 904 (20.8 ms) | 1 195 / 1 195 (41.0 ms) | **542 / 539** (29.0 ms) |
| home fr, phone | 820 | 1 025 | **498** |
| home ar, phone | 879 | 1 066 | **507** |
| /fr/parcours/ (this branch alone) | 774 | — | **379** |
| /fr/institutions/ | 462 | — | **170** |
| /fr/entreprises/ | 612 | — | **248** |

The remaining 500-odd on the home are what the modality really changes there (the sections' verbs, which stop for the
keyboard, and their contents); the whole-document restyle is gone on every page.

### 3.5 The INP, measured on compressed twins — the base, lane H alone, lane H with this branch

The Performance Lead's rig as lane H's reviewer used it (`tools/inp_twins.py`): network A (150 ms, 1.6 Mbit/s down,
750 kbit/s up), CPU × 4, PHONE 412 × 823 @1.75 (mobile, touch) and DESK 1440 × 900, cold loads (a fresh context each,
the cache disabled), the trees interleaved, the order rotating each round. Per load, after a 2.5 s rest: the first Tab
(`html[data-input]` absent → «key»; its interaction's longest Event Timing entry) and the first pointer input after the
keyboard (a click on the desk, a tap on the phone, on the page's h1 — what it costs is the flip back to «pointer» and the
frame after it). Twins, DEBUG off and compressed (`CompressedManifestStaticFilesStorage`, their own `STATIC_ROOT`):
8788 the base (`269cf39`, design-v5's home), 8789 **lane H's final head `4afed99` + this branch** (a `git merge-tree`
of the two, built), 8790 lane H alone (`4afed99` merged with `269cf39`, built). Every load answered 200 and ended in the
«pointer» modality. The machine was shared with lanes H and P2 (their browsers, servers and pytest runs) and this lane's
own non-browser suite, so only the paired, interleaved figures mean anything.

*A first series is void and discarded:* Git Bash rewrote the rig's path argument (`/` → `C:/Program Files/Git/`), so it
timed a 404 page on every tree. The rig now refuses a rewritten path and any answer but 200; the series below are the
real pages (each file records its path).

**Home, n = 5, three trees** (`data/inp_home_n5_three_trees.json`; ms, median · p75):

| Cell | First Tab — base | lane H alone | **lane H + S2** | Δ vs base | Pointer after the keyboard — base | lane H alone | **lane H + S2** | Δ vs base |
|---|---|---|---|---|---|---|---|---|
| desk fr | 256 · 264 | 360 · 400 | **248 · 248** | −8 · −16 | 552 · 576 | 440 · 496 | **408 · 424** | −144 · −152 |
| desk ar | 264 · 344 | 400 · 648 | **280 · 288** | +16 · −56 | 480 · 496 | 456 · 480 | **432 · 496** | −48 · 0 |
| phone fr | 208 · 208 | 216 · 224 | **184 · 184** | −24 · −24 | 160 · 176 | 160 · 168 | **152 · 184** | −8 · +8 |
| phone ar | 208 · 264 | 240 · 240 | **208 · 264** | 0 · 0 | 176 · 216 | 264 · 304 | **128 · 160** | −48 · −56 |

Lane H alone takes the first Tab on the desktop 104 ms (fr) and 136 ms (ar) over the base — the reviewer's M2; with this
branch the first Tab is back at the base (−8 and +16 ms) and every cell, desktop and phone, French and Arabic, is within
20 ms of the base or under it, the first pointer input after the keyboard included. LCP medians 1.8–2.5 s, CLS ≤ 0.02 on
every tree. The element counts of §3.4 are the deterministic measure behind it.

**Home, every series pooled** — the three-tree series above, a second base/lane series (n = 5, desktop and phone,
`data/inp_home_b.json`) and a third on the desktop (n = 5, `data/inp_home_c.json`): n = 15 a cell on the desktop, 10 on
the phone; ms, median · p75, the lane's shift against the base (Δ median, Δ p75, and the Hodges–Lehmann estimate — the
median of every lane − base pair, the robust shift for samples this noisy):

| Cell | First Tab — base | **lane H + S2** | Δ med · Δ p75 · HL | Pointer after the keyboard — base | **lane H + S2** | Δ med · Δ p75 · HL |
|---|---|---|---|---|---|---|
| desk fr (n 15) | 216 · 256 | **208 · 248** | −8 · −8 · 0 | 392 · 464 | **312 · 408** | −80 · −56 · −72 |
| desk ar (n 15) | 224 · 248 | **240 · 288** | +16 · +40 · +8 | 440 · 496 | **392 · 456** | −48 · −40 · −48 |
| phone fr (n 10) | 180 · 208 | **156 · 184** | −24 · −24 · −12 | 148 · 176 | **132 · 184** | −16 · +8 · −8 |
| phone ar (n 10) | 184 · 208 | **196 · 216** | +12 · +8 · 0 | 172 · 216 | **144 · 248** | −28 · +32 · −8 |

Against the target (within 20 ms of the base): every median and every Hodges–Lehmann shift is in, desktop and phone,
French and Arabic, the first pointer input after the keyboard at or below the base everywhere; two p75 are over (the
Arabic desktop's first Tab +40 ms, the Arabic phone's pointer +32 ms), in the two noisiest cells — one series' base
median moved 72 ms from the next on the same tree, so this rig resolves about ±30 ms at p75. Lane H alone, in the same
rounds, was +144 ms (fr) and +176 ms (ar) on the desktop's first Tab.

**Where the first Tab's time goes** (`tools/tabtrace.py`, `data/tabtrace_desk_fr.json`: the rig's conditions, a Chromium
trace around the Tab, desk fr, n = 4 a tree, medians): the Tab's processing is almost all of it (input delay 6 ms,
presentation ≤ 7 ms) — the focus navigation brings style up to date inside the keydown, so the flip's restyle is paid
there. Style: base 127 ms (1 063 elements), lane H alone 174 ms (1 295), lane H + this branch 137 ms (710); layout
5.7 / 11.8 / 12.8 ms. What remains above the base on lane H's home is its own composition (layout +7 ms; more style per
element: the elements the modality really changes — the verbs that stop, their drawings and masks) and two preserved
rules outside lane S's files that the flip still sends to every link and every field: `base.css`
`html[data-input="key"] a { transition-duration: 0ms; }` (every `<a>` of the page) and `main.css`'s
`html[data-input="key"] :is(.form-field :is(input, select, textarea), …)` (request 8.6). The library's last tag subject,
`img` (`_photo.css`'s select grade, `_sec-campata.css`'s settle), stays for S-close (§8.5): its two class-led forms cost
18 B on a home that has 7 B left.

**Parcours, n = 5, two trees** (`data/inp_parcours_b.json`; the route board, the library's busiest page outside the
home — lane H's sheet is not on it, so the lane twin is this branch's library alone; median · p75):

| Cell | First Tab — base | lane | Δ med | Pointer after the keyboard — base | lane | Δ med |
|---|---|---|---|---|---|---|
| desk fr | 160 · 168 | 136 · 144 | −24 | 120 · 152 | 104 · 112 | −16 |
| desk ar | 160 · 176 | 112 · 144 | −48 | 128 · 128 | 88 · 120 | −40 |
| phone fr | 136 · 136 | 80 · 88 | −56 | 104 · 112 | 88 · 88 | −16 |
| phone ar | 128 · 144 | 80 · 80 | −48 | 120 · 120 | 80 · 88 | −40 |

LCP medians 2.2–2.7 s on every tree (network A), CLS ≤ 0.023.

## 4. Files

**Lane S's own (§9.7):** `static/css/v5/_sec-tracciato.css`, `_sec-emiciclo.css`, `_sec-indice.css`, `_sec-mosaico.css`,
`_sec-strato.css`, `_sezioni.css`, `_reveal.css`; `static/js/src/sezioni/indice.js`, `mappa.js`, `spia.js`;
`templates/components/sezioni/{approdo,filo,flusso,indice,mappa,mosaico,protezione,tracciato}.html`,
`components/stepper.html`, `components/photo.html`, `pages/partials/_ingresso.html`; the shared guards
`tests/frontend/test_state_chips_carry_a_register.py`, `test_o14_lint.py`, `test_interior_w3_f1.py`,
`test_orientation_w3_f1.py`, `test_motion_v512_a_w2.py`; the new `tests/frontend/test_sezioni_v522_s2.py` and
`test_sezioni_browser_v522_s2.py`; `docs/design-v5/DESIGN_SYSTEM_V5.md` §14; these notes; the dist they build.

**The one preserved-family rule:** `static/css/v5/motion.css` §5 (the disclosure's height), as the task allows.

**Lane P1's files, carried because the root fix is a contract of lane S that P1's markup and producer instance (no
visible change; for the steward's ownership rows as this family's slices):** `apps/ecosystem/services.py` (one f-string
and its docstring), `apps/ecosystem/static/ecosystem/_institutions.css` (two selectors), the eight templates of (c) (one
attribute token each), `tests/frontend/test_pages_v522_p1.py` (two assertions, §6.2), and their dists
(`ecosystem/institutions.css`, …).

## 5. Budgets (gzip -9)

Measured on this branch against the base `269cf39` (the base's files from a `git archive` of it, outside the repository;
the per-page sums by `tools/pagetotal.py`, the rule of `test_frontispiece_v515_c.py::test_each_page_type_stays_inside_its_total`).

**`main.css` 32 716 B** (−2; the ratchet 32 718 B). `motion.css`'s one rule is the only change in it.

**The library's partials, each minified alone** (`test_sezioni_v522_s.py`'s method and ceilings):

| Partial | Base | Branch | Δ | Ceiling |
|---|---|---|---|---|
| `_sec-tracciato.css` | 1 395 | 1 418 | +23 (the RTL twin and its run) | 1 434 |
| `_sec-indice.css` | 1 400 | 1 404 | +4 | 1 434 |
| `_sec-strato.css` | 1 422 | 1 423 | +1 | 1 638 |
| `_sec-mosaico.css` | 1 200 | 1 203 | +3 | 1 229 |
| `_sec-emiciclo.css` | 661 | 661 | 0 | 716 |
| `_sezioni.css` | 2 434 | 2 444 | +10 | — (in the page sheets) |
| `_reveal.css` (= `core/reveal.css`) | 3 549 | 3 526 | −23 | 6 144 |

**The built sheets:** `core/sezioni.css` (the fixtures' bundle) 11 254 → 11 308; the page sheets that bundle the library
— `ecosystem/pilot.css` 9 487 → 9 508 (ceiling 9 728), `companies.css` 8 682 → 8 701 (9 216), `institutions.css`
8 365 → 8 381 (9 216), `universities.css` 7 614 → 7 630 (8 448), `pathways/index.css` 10 099 → 10 117 (10 240),
`sheet.css` 9 676 → 9 701 (10 240), `training.css` 8 759 → 8 788 (9 728), `diplomas.css` 8 866 → 8 895 (9 728).

**Every sheet a page links, summed:**

| Page (type, ceiling) | Base | Branch | Δ |
|---|---|---|---|
| `/fr/` (home, 61 440) — design-v5's home | 54 703 | 54 678 | −25 |
| `/fr/` — **lane H's home (`4afed99`) + this branch** (a scratch merge) | 61 436 (H alone) | **61 433** | −3 |
| `/fr/entreprises/` (landing, 56 320) | 54 083 | 54 077 | −6 |
| `/fr/contact/` (interior, 56 320) | 49 549 | 49 524 | −25 |
| `/fr/parcours/` (pathways, 56 320) | 55 500 | 55 493 | −7 |
| `/fr/faq/` (reading, 54 272) | 49 511 | 49 486 | −25 |
| `/fr/forum/` (forum, 54 272) | 42 640 | 42 615 | −25 |
| `/fr/institutions/` | 53 766 | 53 757 | −9 |
| `/fr/projet-pilote/` | 54 888 | 54 884 | −4 |
| `/fr/universites-et-formation/` | 53 015 | 53 006 | −9 |
| `/fr/formation/` | 54 160 | 54 164 | +4 |
| `/fr/diplomes-et-titres/` | 54 267 | 54 271 | +4 |

**JavaScript:** `rise.js` 1 327 → 1 325 (1 536); P2's merge conditions grow three modules, inside their ceilings —
`indice` 1 088 → 1 238 (1 536), `mappa` 901 → 1 037 (1 536), `spia` 577 → 806 (1 024). The three superseded chunks
are removed from the dist (`git rm`), the build reproducible (two builds, every dist file's hash equal).

## 6. Tests

**6.1 New.** `tests/frontend/test_sezioni_v522_s2.py` (30, on the sources): every rule of the library that reads the
modality filed under the library's own classes — no universal subject, no rule ending on `::details-content`, no SVG
tag, no bare `.icon` (one case per library sheet); the stroke verb without a tag branch; the tile's `--sez-t`; the
hemicycle's `data-seggio` and the register's `data-registro` in their templates and sheet; the route board's RTL twin
and run; the credit's colon by language (rendered in four); «la protezione»'s title in its own language (rendered in
four, byte for byte the locked title); the glyph's `flex: none` and the rows' ranks. `tests/frontend/test_sezioni_browser_v522_s2.py`
(16, Chromium, the library's fixtures and real pages): MC-1 (the explorer's permalink on a phone, `hashchange`, W1-C's
same-document step), MC-2 (a grid's row is one stop, a followed link current at once), MC-3 (the map's chosen entry into
view at 768 × 560), the route board's light at rest and its run in both directions, the hemicycle's pairing, the glyph's
20 px, «la protezione»'s one edge in Arabic, the credit, the keyboard's tier 0 on tiles, discs and keys, a stroke carrier
drawing its shapes, the disclosure at once from the keyboard and moving for a pointer.

**6.2 Updated under V5.20's strict rule** (the reason cited in each test, every invariant the same or stronger):
`test_state_chips_carry_a_register.py` (the tag guard, §1 d), `test_o14_lint.py` (a register context is `data-register`
or `data-registro`; planted cases for the new marker), `test_interior_w3_f1.py` and `test_orientation_w3_f1.py` (the
register reader reads both markers), `test_pages_v522_p1.py` (the hemicycle's six phrases and seats pair through
`data-seggio`, none carries `data-seat` — stronger), `test_motion_v512_a_w2.py` (the disclosure's keyboard condition on
the accordion; no `[data-input]` rule ends on the pseudo-element). Nothing loosened, no timeout raised, no skip.

**6.3 Red on the base.** The two new modules on a tree of `269cf39` with them copied in: 15 of the 30 source cases
fail there (the modality's subjects, the stroke branch, the attributes, the twin, the credit, the title, the glyph) and
13 of the 16 browser cases; the three that pass on both are equivalence guards (the stroke drawing, the tile's tier 0,
the pointer's disclosure still moving).

**6.4 Runs on this branch** (database lane l3; the browser sessions `test_ile_v5_l3b`, one at a time, each inside a lock
slot):
- non-browser — `tests/frontend`, `tests/compliance`, the confidential-material guard with the private table
  (`ILE_CONFIDENTIAL_SENTINELS`, read in process), `test_html_compression`, `test_nul_bytes`, `test_env_example_is_complete`,
  `test_check_ownership`, `tests/i18n`, `apps/pages`, `apps/pathways`, `apps/ecosystem`, `apps/glossary`, `apps/cms`:
  **4 093 passed**, 1 skipped (the configured WhatsApp number's own check: `ILE_WHATSAPP_NUMBER` unset, as bound), 2 xfailed (the two standing debts: the showcase's captions, the legacy token shim), the browser cases deselected (run below) — 1 h 01 on a shared machine;
- browser — lane S's modules (`test_sezioni_browser_v522_s`, `…_s2`, `test_seal_heads_browser_v522_s`,
  `test_browser_v515_c`, `test_reduced_motion_w1_d`, `test_browser`): **70 passed**; lane P1's pages
  (`test_pages_browser_v522_p1`, `apps/ecosystem` `test_browser`, `test_browser_w3_f1`, `test_orientation_browser_w3_f1`,
  `test_journey_browser_w3_d`): **89 passed**; the shared modules (`apps/pages` `test_browser`, `test_browser_w1_c`,
  `test_motion_browser_w4_b`, `tests/i18n/test_rtl_browser`, `test_mobile_rtl_w4_a`, `test_content_pages_browser_w3_f2`,
  `test_browser_chips_w1_c`, `test_service_pages_browser_w3_f2`, `test_imagery_v522_m`, the browser halves of
  `test_motion_v512_a_w2` and `test_forms_v515_b`): **162 passed** (their 59 source cases deselected here, run in the non-browser set);
- P2's own assertions on the scratch merge: 38 passed, 2 failed — the Forum spy test's count (§2, request 8.3);
- `manage.py check`, `makemigrations --check`, `ruff check .`: clean; `npm run build` twice, every dist file's hash
  equal.

## 7. Headed checks

Chromium 1234, headed, motion allowed (`tools/headed.py`, `tools/seal_check.py`; `evidence/v522/s2/headed_s2.json`,
`seal_check.json` and 40 captures `s2_*.png`): the lane server 8783 for this branch's pages, 8792 for lane H's home
with this branch.

- **Parcours** fr and ar, 1440 and 390: at rest no light inside a rail (0 of 4), the chosen lane's run `sez-run` in
  French and `sez-run-rtl` in Arabic; «la protezione» in Arabic: the title and the body on one edge (572 / 572 px at
  1440, 44 / 44 at 390), the seal on the plate's reading edge.
- **Institutions** fr and ar, 1440 and 390: no element carries `data-seat`; six seats and six phrases carry
  `data-seggio`; a phrase lights its seat (1440); two `data-registro`, no bare `data-register`.
- **Home, lane H + this branch**, fr and ar, 1440, 1280, 1024: the eight index glyphs 20 px wide; «la protezione» in
  Arabic: the title and the body on one edge at every width (572, 420, 217 and, at 390, 40 px); its seal where lane H
  set it, over the plate's rule, the same box and ink as on lane H alone (`seal_check.json`).
- **Formation, Diplômes et titres** fr and ar, 1440: the title and the body on one edge (572 / 572 in Arabic, 116 /
  116 in French).
- **The credit**, Universités et formation and Entreprises, four languages: «Photo : …» (no-break) in French,
  «Foto: …», «Photo: …», «صورة: …».
- **FAQ** fr and ar, 1440: from a pointer the answer's height moves (57 → 236 → 249 px at 40 and 640 ms); from the
  keyboard it is there at once (233 px at 40 ms, the same at 640 ms).
- No horizontal overflow and no console error on any page checked.

## 8. Requests to other lanes, the steward and the Director

**8.1 The steward (this branch's merge).**
- Ownership: the family `v522-s2`. `scripts/check_ownership.py`'s `FAMILY_ID` does not admit it yet (`v5[0-9]{2}-[hms]`
  takes one letter): from V5.22 on, `v5(?:2[2-9]|[3-9][0-9])-s[2-9]`, as `-p1` was admitted at P1's merge, with
  `OUTSIDE_THE_WAVES` and `tests/test_check_ownership.py`'s cases (the steward's files). Its whole files (the two new test
  modules, these notes), its slices in lane S's files and the one rule of `motion.css`, and **lane P1's slices** listed
  in §4 (`apps/ecosystem/services.py`, `_institutions.css`, the eight templates, `test_pages_v522_p1.py`, their dists).
- Order: this branch carries P2's merge conditions MC-1…MC-3 (lane S's half); P2's merge needs this branch first (or with
  it), and P2's half (`p2_with_lane_s.patch`) with it, as P2's QA_ROUND3 asks.
- The catalogue: +0 −0 (no string added, none removed; the credit's colon is markup, the protection's title the locked
  text).

**8.2 Lane P1.**
- `_index.css`: the route board's light twin `[dir="rtl"] .percorsi-tracciato .tracciato__linea::after` and its
  `sez-run-rtl` are now the library's own (`_sec-tracciato.css`): they can go (identical values, harmless meanwhile).
- The first key's cost on P1's own sheets (the same class of rule as §3.4, P1's files): `_pilot.css`
  `html[data-input="key"] .pilota-rotta__percorso ol > li::after` and the `[data-sec-state="wait"] .linea-v2 > ol > li…`
  rules (subjects `li` and `span`: every list item and span of the page), `_universities.css`
  `.filiera__meta .foto > picture > img` (every image), `_index.css` `.come .sez-tile .icon` and `_training.css`
  `.traversata__nodo .icon` (every icon): class-led forms, for the pilot page above all (333 elements restyled at its
  first Tab once the whole-document rules are gone).

**8.3 Lane P2** (and its merge's steward).
- Rename the library's register marker in P2's own files: `templates/forum/partials/presentation.html`,
  `templates/pages/partials/fronte/_rete_pannelli.html`, `templates/pages/partials/projet/_figura.html` (one attribute
  token each) and the three test lines that read it (`apps/forum/tests/test_forum_v522.py:70`,
  `apps/pages/tests/test_interior_v522.py:56`, `:127`). Patch: `evidence/v522/s2/requests/p2_data_registro.patch`
  (against `v522-p2` `f32fa07`). Without it the chip guard (c) goes red again at P2's merge.
- MC-2's new spy test (`test_pages_browser_v522_p2.py::test_the_spy_lights_each_letter_followed_and_each_section_read`,
  from `p2_with_lane_s.patch`): its Forum half asserts `len(seen) == 5`; in the test database the event is before its
  date and the sommaire holds seven links, all seven lit. Compare with the sommaire's own link count
  (`page.locator('.forum-localnav a').count()`), not 5.
- `_projet.css` `html[data-input="key"] :is(.projet-racconto *, …)`: a universal subject (the whole document at the
  first key, §3.4) — name the elements that move.
- The stroke verb on a carrier (the Forum's ring, the fraud shield, AGAMI's colonnade, the project's door): unchanged for
  P2 — the carrier's dash is inherited by its shapes (`test_a_stroke_carrier_passes_its_draw_to_the_shapes_inside`).

**8.4 Lane H.** Nothing is needed for this branch: the home's own drawings carry the verb on their shapes; the home's
total with this branch is 61 437 / 61 440 B gzip -9 against `c17146f` (§5; H's final fix round `4afed99`: see §5).
The INP measure of H's §9.9 item 6 is §3.5.

**8.5 S-close.** `_sigillo.css`'s `:is(.sez, .ingresso, [data-sigillo-scope]):has(…)` as three selectors (H's request 3:
7 B over `fronte.css`'s headroom); the `img` subjects of `_photo.css` and `_sec-campata.css` (3 + 15 B on the home);
`_reveal.css`'s other `:is()` subjects (the legacy reveal-mark list, the spotlight's keyboard list, `settle`/`depth`, the
light, the seal's shapes) — class-led selectors, measured against the home's ceiling; the two orphan chunks
`chunk-ESW3PKTX.js` and `chunk-RNCDCP3M.js` (unreferenced since v512-a W2, still in the dist).

**8.6 The Director.** SECTION_SYSTEM_V2 §2 H writes the hemicycle's pairing as `:has([data-seat="n"]:hover)`; the
attribute is Lume's L3 one (DS 2026 §12), so the pattern uses `data-seggio` — the example to amend. §3.4's one residue:
the disclosure's `content-visibility` flip keeps its 120 ms on a keyboard close (invisible), the price of `main.css`'s
ratchet. And the first key's last broad subjects are in preserved families this follow-up may not touch (§3.5):
`static/css/v5/base.css` `html[data-input="key"] a { transition-duration: 0ms; }` restyles every link of a page at the
first key, and `main.css`'s field rule `html[data-input="key"] :is(.form-field :is(input, select, textarea), .input, …)`
every field — class-led or `:focus-visible`-scoped forms, measured against `main.css`'s ratchet, for a preserved-family
pass.

## 9. Not done, deviations

- H's request 3 (`_sigillo.css`) and the two `img` subjects: measured, not done (bytes; §3.4, §8.5).
- The campata's settle cancelled by the shell (H's request 2 of §11.5) and the `sez-arch` `from` (request 1 of §11.5):
  outside this follow-up's brief (§12.5's items 1–5 are), unchanged.
- The keyboard's condition for the accordion sits on its interpolation rule, not «a custom property read by
  `::details-content`» (§3.4: every such form is over `main.css`'s ratchet).
- Lane P1's files carry this branch's contract renames (§4): the steward records them as this family's slices.
- The lock slots: at 15:09 the end of one of this lane's sessions released both slots (its helper released every slot
  carrying the lane's label) while the lane's INP session still ran in the other; the slot was taken again at 15:10
  and every later session held its slot under its own label (`tools/with_lock2.sh`). No other lane's slot was touched.
