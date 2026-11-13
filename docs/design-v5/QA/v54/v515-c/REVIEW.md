# Lane C: finishing review F1 (v515f-c-qa1)

- **Branch:** v515-c @ `68597e8` (worktree C:/tmp/ile_wt/v515-c, clean). It contains design-v5 `7f2a02d` through the merge `e273e7c`.
- **Server:** lane server 127.0.0.1:8785, database lane l5 (`ile_v5_l5`), dev settings, ILE_DESIGN_PREVIEW=1, ILE_REFERENCE_DATE=2026-10-03. Stopped at the end of the review.
- **Browser:** headed Chromium (Playwright, headless=False), run through `C:/tmp/ile_v5_council/.work/v515f-c-qa1/rev.py`.
- **Chromium lock:** held from 10:57 to 11:11 on 29 Oct across three sessions (s1, interact, s2). Each session was under 22 minutes and released the lock when it ended. Lane D took the lock at 11:11.
- **Evidence:** `finish1/` holds `s1.json`, `s2.json`, `interact.json`, about 225 screenshots, and contact sheets in `finish1/sheets/`.

## Runs

| Run | Scope | Result |
|---|---|---|
| s1 | fr + ar × 1440/1280/1024/768/430/390/375/360 × 16 pages (256 loads; touch + mobile below 600) | 0 errors, 0 horizontal scroll, 0 elements beyond the viewport, 0 sub-24 px targets. The only text overlaps are with the decorative `.fronte__motif` (aria-hidden ground). No network-node clashes. Formation «Second temps»: no text under the frame at any width |
| s2 | it + en, same matrix (256 loads) | Same, 0 / 0 / 0 |
| interact, reduced motion | it 1440, en 390, ar 1280, ar 430, fr 375 × Parcours, Entreprises, Formation, Contact, Pilote | 0 running animations after load in all 25 cases. Head action inside the first screen in every case that has one (Parcours 375 bottom 842/844) |
| interact, keyboard | it/en/ar 1280: Tab from the top to the band's action on Parcours, Contact, Entreprises | Reached in 15 tabs. Skip link first. Focus ring solid 1.6 px teal on the action (screenshots `focus-*.png`); mirrored in ar |
| interact, in-page jump | Enter on «Recueil des besoins» | Scrolls to `#formulaire` (y 1896 / ar 1876). Focus stays on BODY (see m-4) |
| interact, real navigation | it/en home: hover/click the panel triggers, then click the Formation link in the header | Lands on `/it/formation/` and `/en/formation/` (`nav-*.png`, `menu-*.png`) |
| interact, Le projet titles | fr/it/en/ar 1280 | «POURQUOI ITALY LEGAL ENTRY» `chapter__title--caps` 24/32, +0.48 px tracking. Neighbours 28/36 at −0.56 px (ar 28/39.2, normal). On it/en/ar it carries `lang="fr"`. «بإيجاز» is not marked |
| interact, wheel walks | ar/en 1280: Formation, Le projet, Parcours, Institutions, scrolled by wheel | B/W frames reach full colour at mid-viewport (Formation's microscope frame, the Institutions chamber). No motif debris in the gutter |
| pytest, lane l5, `config.settings.test` | `test_frontispiece_v515_c.py` + `tests/i18n/test_page_integrity.py` (not browser) | **103 passed, 1 failed**: `test_latin_text_on_arabic_pages_carries_its_own_lang_attribute`. This is the known lane D msgid carry-over and matches the builder's account. (A first run had `.env`'s `DJANGO_SETTINGS_MODULE=dev` leak into it and showed a spurious second failure in the legal 404 test. That was my environment's fault, not the branch's. Under test settings it passes.) |

## Previous findings: verification

| Previous finding | Status | Evidence |
|---|---|---|
| **MAJOR**: round 3's headed inspection never ran (lock contention) | **FIXED** | The builder ran it (r3/, f1/), and this review re-ran the full headed matrix independently (512 loads in four languages plus the interaction probes). The results agree with the builder's f1.json load for load. |
| minor: `test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` fails (four lane C W2 msgids) | **NOT FIXED (lane D, correctly routed)** | Still 1 failed. NOTES F1 now names the test. It stays a merge blocker until D's catalogue pass. |
| minor: develop rule copied from lane A; head hairline missing on FAQ/Glossaire/Vivre (`.fronte-wrap`) | **NOT FIXED, and the route has changed** | Lane A has since been merged into design-v5 (`79769f6`) **without** adopting either one: `_reveal.css` at 79769f6 has no `.fronte-wrap` and no combined develop rule. The requests to lane A cannot be done any more as written. See m-2. |
| minor: `depot.html:78,82` and `terms_required.html:24` link `legal:terms` unconditionally (M-2 / m-12) | **NOT FIXED (lane D)** | Unchanged on v515-c (`{% safe_url 'legal:terms' %}`). |

Builder's two F1 fixes:
- **Arabic heads took the capitals layout: FIXED.** `data-words-first` is on Parcours, Entreprises, Diplômes and the pilot in all four languages. Institutions, Universités, Formation, Réseau and Contact are photo-first on ar phones, as on fr (`sheets/ar375a.png` vs `fr375a.png`). On the ar pages the caps class appears only on French-run titles.
- **Capitals section title: FIXED.** Measured above.

## Findings (this review)

No major.

**m-1 (minor), the head action leaves the first screen at tablet portrait and at 360, and the builder's account overstates this.** The account says the head action is «inside the first screen on Parcours, Entreprises and Contact in every case». The builder's own `f1/f1.json` and my sweep both show that it is not:
- Parcours: bottom 1255 / 900 at 768 in all four languages; 898 / 844 at 360 (fr, ar, it); 894 at en-360; 870 at it-375.
- Entreprises: 1175 / 900 at 768 (ar 1208).

At 768 (exactly 48 rem) the words-first rule does not apply (`max-width: 47.999rem`). The photo leads at about 380 px tall, so the h1 starts at about 740 and the action sits on the second screen (`f1/fr-768-parcours.png`). The visible list only promised 1440/1024/390, so this does not block the owner. It is still a gap at a common tablet width.

*Fix:* extend the `[data-words-first]` order/16:9 rules to `max-width: 63.999rem`, or cap the photo at 16:9 between 48 and 64 rem. At 360, trim the lead's block (`--t-body` → `--t-small` on the way text, or tighten the gaps) so the action clears 844. Correct the account in NOTES.

**m-2 (minor, merge), design-v5 has moved again and the lane no longer merges cleanly.** design-v5 HEAD is now `79769f6` (lane A merged). `git merge-tree HEAD 79769f6` reports **conflicts** in `apps/cms/templatetags/cms_nav.py` and `tests/frontend/test_cms_nav.py`: lane C's `_OWNER_SECTION` (one aria-current per page) collides with lane A's one-current-item rework. Lane A also brings its own `filter: grayscale(1)` rules (`_reveal.css` l.106, l.176), and it has not adopted lane C's combined zoom+colour rule.

*Fix:* lane C merges `79769f6`. In the conflict, keep a single source of «one current item» (A's, plus C's `_OWNER_SECTION` rows if A's rule does not already cover the pilot and Formation). Then re-run `test_cms_nav.py`, `test_browser_v515_c.py` (develop: grey before entry, colour at mid-viewport) and lane A's hairline test under the lock. Lane A has been merged, so the two lane A requests become **lane C's or the steward's**: the develop rule stays in `_photo.css` or moves into `_reveal.css` in the merge, and the hairline selector extends to `.fronte-wrap`. Update the NOTES request list to match.

**m-3 (minor, carry, lane D):** on Arabic pages, the locked French copy is a right-aligned title over a left-aligned lead and body. This shows on the Parcours head (`ar-375-parcours.png`), the Fraudes notice panel, the AGAMI body and the Entreprises quote. The h1 follows the page direction, while the paragraphs with `lang="fr"` set their own. It reads as two alignments in one block. This is the catalogue/dir question already with lane D; it is recorded here so it is not lost.

**m-4 (minor, a11y nicety):** the in-band jump «Recueil des besoins» → `#formulaire` scrolls correctly, but focus stays on `<body>`. A keyboard user's next Tab starts from the right place, but a screen reader announces nothing. *Fix (lane B owns the form):* give the form's heading `tabindex="-1"` and the anchor target, or let the browser's sequential-focus start point do the work and accept it as is.

## Scores (V5.15 §26)

| Family | Score | Why |
|---|---|---|
| Page Headers (system) | **4.5** | Re-measured in headed Chromium, 512 loads, four languages, eight widths: 0 horizontal scroll, 0 text/figure overlaps, the network names and the @ disc in place, focus visible. The page now decides the words-first layout, so the Arabic heads match their French pages. The 768/360 action fold (m-1) keeps it below 5. |
| Page-by-page art direction (§4) | **4** | Each composed head has its own idea (route spine, ring of actors, coordinate plate, arch, skyline, notice panel, colonnade, night pilot diptych) and is mirrored correctly in ar (`sheets/*1280*.png`). Contact still repeats its address in a centred second section, which is an accepted earlier choice but a little thin. |
| Imagery | **4** | B/W frames develop on entry (wheel walks, ar/en 1280). Credits are legible. The 1x srcset matches the drawn track. Re-verification after lane A's merge is pending (m-2). |
| Motion (lane C side) | **4** | Develop and rise run on wheel scroll. Under reduced motion, 0 running animations in 25 of 25 page states, and the frames are in colour and still. |
| Section design (§17) | **4** | Formation's split holds from 1440 to 360 with nothing under the frame. The Institutions «Destinataires» pull quote and frame are balanced. The Le projet rows are even. |
| Typography | **4** | The capitals title sits one step down and is tracked. The Arabic face sizes and line heights are correct. The mixed alignment of French runs on Arabic pages (m-3) is lane D's. |

**Minimum 4. No major.** Lane C clears the bar (≥ 4 per family, no major). Showing it to the owner depends only on the steward's merge conditions: the re-merge of design-v5 `79769f6` with the cms_nav conflict resolved and develop/hairline re-measured (m-2), D's four msgids, and D's legal_links fix.
