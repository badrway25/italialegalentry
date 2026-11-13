# V5.29 — senior visual review of PUB2 (label v529-pub2-review, 7 Nov 2026)

Branch `v524-pub2` at `78af131f` (worktree C:/tmp/ile_wt/v524-pub2), served on 8789 (database lane l5). Headed `chromium-1234`
under `CHROMIUM_LOCK_A` (01:03, released after the run); headless probes without a slot. Server stopped at the end.
Stills, `review.json`: this folder. Scripts: `.work/v529-pub2-review/`.

**VERDICT: PASS — 0 blockers.**

## What was checked
- FAQ, Glossaire, term (`carta_blu_ue`), Fraudes, AGAMI, Contact, Réseau at 1440 / 1024 / 390 fr; FAQ, Glossaire, AGAMI, Fraudes,
  Contact, Réseau at 1440 / 390 ar; reduced motion on the FAQ (fr 390, ar 1440).
- 36 cells: overflow 0, console errors 0, pure-black text 0, axe (wcag2a/2aa/21aa, 1440 fr + ar, 390 ar) 0 violations.
- FAQ: 9 glyphs, 0 repeats; search «visa» 2 answers each with its glyph; empty search 9 register links (fr, ar);
  1440 click → `#faq_decreto_flussi`, row 500 in the accent ink, one panel shown; keyboard ArrowDown/End/Home move selection with a
  solid 1.6 px ring; 390 open → answer shown, close → height 0, Enter opens with focus ring and no `faq-svela` reveal (only the
  tile's own state transition runs); permalink `#faq_visas` lands in view at 390.
- Contact doors: a full-page still caught them before their scroll reveal; scrolled into view they match design-v5 (`doors_*`).
- Tests: targeted static set 949 passed, 1 skipped (WhatsApp unset, option B), 1 failed = design-v5's
  `test_icons::…thinner_hand…` (SYS `.sez-tile--lg`, file identical to design-v5); `test_typography_v2` Arabic browser test
  2 passed with `DJANGO_ALLOW_ASYNC_UNSAFE` (as the other lanes run it). Lane browser modules (`test_pages_browser_v524_pub2.py`,
  `test_pages_browser_v522_p2.py`): 70 passed, 1 failed = the CARRIED `test_the_forum_ring_turns_round_its_hub_and_mirrors_in_arabic`
  (V5.29 orchestrator note 21:25: PUB2's steward item).
- Locked copy: `tests/compliance/test_locked_content.py` green. Channels: `test_contact_channels_v519.py` green; two channel plates
  drawn on /fr/contact/ (values never read or printed).
- Budgets (gzip -9, dist): main.css 32 714 ≤ 32 716; faq.css 2 207 (re-recorded, V5.29); lessico 2 324; interior 7 986;
  agami 1 778; frodi 1 199; rete 1 761; forum 7 865 ≤ 8 192; projet 2 222 (re-recorded).
- Preserved families: Navbar, Lume, contact board, privacy link, forms, footer — unchanged in every cell.

## V5.29 §23
1. Raw CSS grids left? **No** on these pages: glossary cards, FAQ explorer, Fraudes split and AGAMI registers are materials on stone.
2. Pure/heavy black dominant? **No**: 0 pure-black text nodes; navy ink, secondary text in warm slate.
3. Headings relying on bold? **No**: headings and FAQ questions at 500; the only ≥ 700 is AGAMI's inline emphasis in its body.
4. Backgrounds intentionally designed? **Yes**: stone grounds, the drawn head fields, paper before the footer.
5. Cards/materials sophisticated? **Yes**: layered plates, accent rules, tiles; nothing generic.
6. FAQ a 2026 premium product? **Yes**: subject glyph index, master–detail, state-ink, quiet reveal, empty search showing the whole register.
7. Icons semantic and integrated? **Yes**: nine distinct FAQ glyphs in SYS's tile; repeats found are link arrows only.
8. protezione__campo discreet? **Not in these pages** (0 occurrences); the Fraudes «Votre protection» panel is the page's subject.
9. Institutions Italy–Morocco? **Not this stream.**
10. Less editorial than before? **Yes**.

## Minor (not blocking; for the steward or post-acceptance)
- PUB2's Arabic contract still open (orchestrator note 21:25, the steward's job before recording): French FAQ questions/answers,
  the Fraudes body and glossary definitions on /ar/ without the C-SUBST caption (ARABIC_BURNDOWN PUB2 rows); the Forum ring RTL test.
- Lane database l5 is stale: 0 FAQ category translations (ile_v5 has 3), so /ar/faq/ shows «Général» `lang="fr"`; 8780 shows «عام».
  Data, not code — refresh l5 from ile_v5.
- FAQ 1440: «…agence de recrutement ?» leaves the «?» alone on a line (normal space before «?»; locked copy, so a CSS/nbsp
  fix only if allowed).
- Fraudes head: the H1 in capitals with an empty left field above it — unchanged from design-v5, out of this lane's table.
- `templates/components/sezioni/indice.html` (library file) touched: two class attributes, explorer form only — record in the ownership manifest.

## The verdict as the workflow returned it to the steward, verbatim

```json
{"review": [{"page":"FAQ (fr/ar, 1440/1024/390, search, empty, open/close, keyboard, reduced motion)","composition":5,"motion":4,"imagery":4,"interaction":5,"institutional":5,"coherence":5,"note":"PASS. Nine distinct glyphs, no repeats, in every cell. Ink changes by state, questions at 500, solid focus ring. Search shows answers with glyphs; an empty search shows all 9 register links. Opening on a phone reveals the answer and closes back to height 0. A keyboard open runs only the tile's own state transition, with no reveal. 0 overflow, 0 console errors, axe 0."},{"page":"Glossaire + term (carta_blu_ue)","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":5,"coherence":5,"note":"PASS. Stone ground, layered term cards with accent rules and outlined initials, letter rail, paper band before the footer. The term page's band and chips read well. Arabic 390 is correct RTL. axe 0."},{"page":"Fraudes","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":5,"coherence":5,"note":"PASS. Stone ground, a report plate with the shield, three routes as tiles. The 'Votre protection' panel is the page's subject, not protezione__campo. The French body on /ar/ without its caption is an open AR contract item for the steward."},{"page":"AGAMI","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":5,"coherence":5,"note":"PASS. Colonnade signature, registers on the night plate with tiles, labels in the label role (Readex Pro in ar). The only weight of 700 or more is inline emphasis in the body."},{"page":"Contact","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":5,"coherence":5,"note":"PASS. Channel board unchanged, both channel plates drawn (values never read), privacy link kept. Scrolled into view the doors match design-v5. The clipped doors in the full-page still were their state before the scroll reveal."},{"page":"Réseau","composition":5,"motion":4,"imagery":5,"interaction":4,"institutional":5,"coherence":5,"note":"PASS. The map composition is intact and mirrors correctly in ar. Labels are in the label role, so the Arabic glyphs no longer fall back to a system face. 0 overflow, axe 0."}],
 "minors": [{"severity":"minor","where":"/ar/faq/, /ar/attention-aux-fraudes/, /ar/glossaire/ + term pages, /ar/forum/ (tests/i18n/arabic_allowlist.py ARABIC_BURNDOWN PUB2 rows; tests/frontend/test_pages_browser_v522_p2.py::test_the_forum_ring_turns_round_its_hub_and_mirrors_in_arabic)","detail":"PUB2's Arabic contract is still open. French FAQ questions and answers, the Fraudes body and the glossary definitions appear on /ar/ without the C-SUBST caption. The carried Forum-ring RTL test still fails ('ar' ring offsets not mirrored, 192 > 2). Both predate this lane: they came in with the AR merge and are assigned to the PUB2 merge steward by the orchestrator note of 6 Nov 21:25.","fix":"Before recording, the merge steward burns the PUB2 ARABIC_BURNDOWN rows to 0 (entry_for through locked_content.get, plus locked_caption on the FAQ, Fraudes and glossary) and turns the Forum-ring RTL test green."},{"severity":"minor","where":"lane database ile_v5_l5 (/ar/faq/ category heading)","detail":"The lane database is stale: it holds 0 FAQCategoryTranslation rows where ile_v5 holds 3, so /ar/faq/ shows 'Général' with lang=fr while the 8780 preview shows 'عام'. This is data, not code; the template logic is unchanged.","fix":"Refresh ile_v5_l5 from ile_v5 before the steward's checks."},{"severity":"minor","where":"/fr/faq/ explorer at 1440 (row 2)","detail":"In '…agence de recrutement ?' the question mark wraps onto its own line, because the locked copy has a normal space before '?'.","fix":"Post-acceptance candidate: a narrow no-break space applied at render time, only if allowed for locked copy. Otherwise leave it."},{"severity":"minor","where":"templates/components/sezioni/indice.html","detail":"This library file (S/LIB family) was changed by PUB2: two class attributes, explorer form only.","fix":"The steward records the slice in the ownership manifest."},{"severity":"minor","where":"tests/frontend/test_icons.py::test_no_sheet_draws_a_glyph_with_a_thinner_hand_than_the_icon_rule","detail":"This test fails on design-v5 itself, from SYS's .sez-tile--lg stroke 1.25. _sezioni.css and test_icons.py are byte-identical to design-v5 31f5ceff, so PUB2 did not cause it.","fix":"SYS or CLOSING resolves it. Not this lane."}]}
```

No fix round (PASS, 0 blockers). The steward's merge (DL54-195) answered the minors on the merged tree: PUB2's
ARABIC_BURNDOWN rows 26 → 0 (the FAQ questions, the glossary chips, the Forum programme and roles, the trademark
words by sub-key; the FAQ answers, the Fraudes body and the definitions captioned), the Forum ring mirrored
(fr [0, 255, 391 …], ar [0, −255, −391 …] at 1440; the carried test green), ile_v5_l5 refreshed from ile_v5
(3 = 3 category rows), indice.html recorded as v524-pub2's slice; the «?» wrap and test_icons stay carried.
