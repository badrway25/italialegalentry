# V5.29 — PUB1 senior visual review (label v529-pub1-review, 6 Nov 2026)

Branch `v524-pub1` @ `9695f0a2` (worktree C:/tmp/ile_wt/v524-pub1), lane server 8788 on `ile_v5_l4`. One headed run in
chromium-1234 under `CHROMIUM_LOCK_A`, released. Script: `.work/v529-pub1-review/review.py`. Measurements: `review.json`.
Stills: `<page>_<lang>_<w>_{top,full}.png`, `slices/`, `crop_*`. Lane server stopped. No page text, contact value or
private-table value is written here.

**Verdict: PASS. 0 blockers in this stream.**

## Coverage
Collaboration/Institutions fr 1440·1024·390, ar 1440·390, fr 1440 reduced motion; Institutions landing fr 1440·1024·390 and
ar 1440·390; Parcours fr 1440·1024·390 and ar 1440·390; Entreprises, Universités, Formation and the salaried_work sheet fr at
1440·1024·390. Keyboard: 25 Tabs on the collaboration page. axe (wcag2a/aa/21aa) on every fr 1440 page and on collab ar 390.

## Measured
- Horizontal overflow 0 and console errors 0 in all 28 cells. axe found 0 violations on 8 runs.
- Under reduced motion the collaboration page has 0 animations running. The two intesa drawings have `transform: none` in
  fr and ar, so the flags are not mirrored. In ar the placement mirrors: Italy sits at the right edge, still green→red, and
  Morocco sits bottom-left.
- Type: every h1/h2/h3 in main is weight 600 and colour rgb(21,34,42) (warm ink). 0 text elements are at 700 or above and
  0 text nodes are pure black.
- Keyboard: focus is visible on every stop (outline or focus ring). The order runs skip-link, nav, the form fields, consent,
  submit, then the footer.
- Budgets (gzip -9 of the committed dist): main.css 32 695 ≤ 32 716 (unchanged since 0ad88a42); institutions.css 9 149 and
  intesa.css 712; pathways index.css 10 664 and sheet.css 10 147 (each ≤ 11 264).
- Locked copy and contact channels: no `{% locked %}`, contact, footer or catalogue line is in the branch's template diff
  against 0ad88a42. The locked-checksum tests are part of the passing suites.

## Targeted tests
- Static: `test_pages_v522_p1.py`, `apps/ecosystem/tests`, `apps/pathways/tests`, `test_typography_v2.py`: 473 passed,
  2 failed. The failures are `test_the_form_pages_open_on_their_space_s_compact_band_and_keep_their_form` and
  `test_the_recipients_spans_rebuild_the_sentence`. Both are base reds already recorded by the builder: since AR's V5.27
  merge the Arabic recipients render as one rendering, not six spans.
- Browser: `test_pages_browser_v524_pub1.py` and `test_pages_browser_v522_p1.py`: 39 passed, 2 failed, both [ar].
  - `…recipients_as_one_annotation_beside_the_hemicycle[ar]` expects ltr French boxes. AR now renders Arabic (R7′), so this
    is the same base cause.
  - `…hold_their_width_at_every_size[ar]` finds a 2 px overflow on /ar/parcours/ at 768 under reduced motion. It comes from
    the French run in the head's lead (`.ingresso__lead > span[lang=fr]`). **It reproduces identically on a clean 0ad88a42
    served on a temporary port (removed): base, not PUB1.**
- These four reds belong to the AR/steward follow-up. A V5.20 amendment, or the lead's French-run fix, arrives with the next
  design-v5 merge. PUB1 does not touch them.

## V5.29 §23 — the ten questions
1. Raw CSS grids left? **No.** The Parcours board is a routed composition: family rows on one trunk, with a photograph per
   family. The «Comment ça marche» plates sit on the brand wash with their route. The démarche on stone has a curved route
   and staggered plates.
2. Pure or heavy black dominant? **No.** 0 pure-black text nodes; headings in warm ink 21/34/42; leads in 74/90/98.
3. Headings relying on bold? **No.** Everything is at 600 at most, and hierarchy comes from size, colour and spacing (0 text
   at 700 or above).
4. Backgrounds intentionally designed? **Yes.** Stone, brand wash, carta viva, pietra, the Institutions velatura and «l'intesa».
5. Cards and materials sophisticated? **Yes, restrained.** Niche tiles, the raccordi, plates ink and light. Shared plate
   treatment is SYS's.
6. FAQ a 2026 premium product? **Not this stream.**
7. Icons semantic and integrated? **Yes.** Each pathway has its own icon (briefcase, translate, building, handshake,
   cap, magnifier, person, pin). The four steps carry compass, info, board and stamp. A repeat is only the same pathway named
   twice.
8. protezione__campo discreet? **Not this stream (SYS).** On this branch it is still the base's large panel: 601 px tall at
   1440 and 898 at 390 on Parcours, Formation and the sheet. It becomes compact only when v529-sys merges. That dependency
   needs re-checking after the merge.
9. Institutions communicates Italy–Morocco elegantly? **Yes.** Italy's three soft fields hold the reading edge and
   Morocco's red field with its fine pentagram holds the far corner. It is low-opacity, cropped, aria-hidden and never over
   the words. It is correct in RTL and not mirrored. The same ground sits under the landing's «Pour aller plus loin». It is
   diplomatic, not a poster.
10. Less editorial than before? **Yes.** The numerals are in the sans and the kickers use the label role. The heads are image
    and text with a measured lead.

## Minor (post-acceptance candidates, not blocking)
- m1: at 1440 the pentagram's 1 px line crosses the head's temple line drawing (lower right, `crop_collab_fr_corner.png`):
  two line systems meet. Option: offset the star or clip it before the temple.
- m2: at 390 Italy's fields (opacity 0.16, about 60 px) are hardly perceptible, so on a phone the pairing reads mostly from
  the red corner. This was the builder's choice for 4.5:1 contrast and is acceptable.
- m3: in «Pour aller plus loin» the pilot card's title is in capitals beside the Forum card's sentence case. This is likely
  the locked copy. Note only.

## Scores (once; ≥ 4 expected)
collab-institutions 5·4·5·4·5·5 PASS · institutions 4·4·5·4·5·5 PASS · parcours 4·4·5·5·4·4 PASS · entreprises 4·4·5·4·5·4
PASS · universites 4·4·5·4·5·5 PASS · formation 4·4·5·4·4·4 PASS · sheet salaried_work 4·4·4·4·4·4 PASS
(composition · motion · imagery · interaction · institutional · coherence).

## The verdict as the workflow returned it to the steward, verbatim

```json
{"review": [{"page":"/fr|ar/collaboration/institutions/","composition":5,"motion":4,"imagery":5,"interaction":4,"institutional":5,"coherence":5,"note":"PASS. «L'intesa» is restrained, cropped and aria-hidden, with transform none on both flags; in ar the placement mirrors but the flags do not. 0 overflow, 0 console errors, axe 0 violations (fr 1440 and ar 390), 0 animations under reduced motion, focus visible on every stop."},{"page":"/fr|ar/institutions/","composition":4,"motion":4,"imagery":5,"interaction":4,"institutional":5,"coherence":5,"note":"PASS. The «Pour aller plus loin» band carries the intesa ground behind the tiles; the velatura and the hemicycle are kept. 0 overflow at 1440/1024/390 fr and 1440/390 ar; axe 0 violations."},{"page":"/fr|ar/parcours/","composition":4,"motion":4,"imagery":5,"interaction":5,"institutional":4,"coherence":4,"note":"PASS. The routed family board, the plates on the brand wash and the distinct semantic icons hold. protezione__campo is still the base's large panel (SYS's primitive, not PUB1's). The 2 px ar overflow at 768 also reproduces on base 0ad88a42."},{"page":"/fr/entreprises/","composition":4,"motion":4,"imagery":5,"interaction":4,"institutional":5,"coherence":4,"note":"PASS. The démarche on stone has a curved route and staggered plates; the form is preserved. Weights stay at 600 or below and there is no pure black."},{"page":"/fr/universites-et-formation/","composition":4,"motion":4,"imagery":5,"interaction":4,"institutional":5,"coherence":5,"note":"PASS. The filiera on the brand wash with its sfumatura, the campus frame kept, axe 0 violations."},{"page":"/fr/formation/","composition":4,"motion":4,"imagery":5,"interaction":4,"institutional":4,"coherence":4,"note":"PASS. The prescribed order holds (traversata → protezione → grid → boussole). The protezione panel is large, but it is SYS-owned."},{"page":"/fr/parcours/salaried_work/","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS. The étapes are on stone and the raccordo runs into the night arc. 0 overflow and 0 errors at all three widths."}],
 "minors": [{"severity":"minor","where":"/fr/collaboration/institutions/ head at 1440, lower right (evidence/v529/pub1/crop_collab_fr_corner.png)","detail":"The pentagram's 1 px line crosses the head's temple line drawing, so two line systems meet. It is decorative, low opacity and not over the text.","fix":"Post-acceptance candidate: offset the Moroccan star further into the corner, or clip it before the temple motif."},{"severity":"minor","where":"/xx/collaboration/institutions/ at 390","detail":"Italy's fields (opacity 0.16, about 60 px wide) are barely perceptible on a phone, so the pairing reads mostly from the red corner. This was a deliberate trade-off for 4.5:1 contrast.","fix":"Post-acceptance candidate: optionally widen the fields a little on a phone while keeping them clear of the text."},{"severity":"minor","where":"/fr/parcours/, /fr/formation/, the pathway sheets: protezione__campo","detail":"On this branch protezione__campo is still the base's large panel (601 px tall at 1440, 898 at 390). V5.29 §4 assigns it to SYS (v529-sys), not PUB1, so it is not a PUB1 blocker.","fix":"Re-check Q8 on these pages after v529-sys merges into design-v5."},{"severity":"minor","where":"tests: test_pages_v522_p1.py (2) and test_pages_browser_v522_p1.py [ar] (2)","detail":"Four reds come from the base, not PUB1. The two recipients-span tests and the ltr-annotation test fail because AR's R7′ renders Arabic. The 2 px overflow on /ar/parcours/ at 768 under reduced motion comes from the French run in .ingresso__lead and reproduced identically on a clean 0ad88a42 (temporary worktree, removed).","fix":"The AR/steward follow-up (the uncommitted design-v5 fix in progress, plus a V5.20 amendment citing R7′), arriving with the next design-v5 merge."}]}
```

No fix round (PASS, 0 blockers). The steward's merge (DL54-194) re-checked the minors on the merged tree: the
protection is SYS's compact band on PUB1's pages (216 px at 1440, 570 at 390, fr), the 768 px Arabic overflow
is gone with the Parcours intro set as a French block with its caption, the base's reds are recorded there.
