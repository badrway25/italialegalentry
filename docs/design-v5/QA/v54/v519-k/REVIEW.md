# V5.19 contact information: review of branch v519-k (label v519-k-review)

> V5.20 redaction (lane v520-wa, 30 October 2026): byte for byte the review of 29 October 2026, apart from this note
> and its three sentences that quoted the WhatsApp number, which now read «the owner-confirmed WhatsApp number (configured
> outside the repository, V5.19/V5.20)» (`docs/design-v5/QA/v520/wa/NOTES.md`).

- Reviewed on 29 October 2026, 21:48 to 22:56. Branch `v519-k` at `e4b5ff7`, worktree `C:/tmp/ile_wt/v519-k`.
- Directive: `C:/tmp/ile_v5_council/directives/V5_19_CONTACT_INFORMATION_OWNER_CONFIRMED.md`.
- `design-v5` is at `900372a`, which is the v518 steward merge's record. `v519-k` contains it, so merging the branch into `design-v5` is a fast-forward. The v518 steward merge (5f92e4d and 900372a) had already landed before this lane merged.
- I made no change to the branch. Every finding below is minor and none blocks the merge.

## Verdict: APPROVE

## Point-by-point check against V5.19

| Point | Check | Result |
|---|---|---|
| §3 one canonical location | The values live in the existing `core.models.SiteSettings` singleton (`freephone_number`, `whatsapp_number`). Their defaults come from `settings.ILE`. `core.contact.public_channels()` reads them and the context processor exposes them as `site.channels`. I grepped every template: none contains a number. The test `test_no_template_writes_a_number` guards this. | OK |
| §2 and §7 exact values | Rendered HTML, fr/it/en/ar: the Numero Verde link is `tel:800642015` with the label «800 642 015». The WhatsApp link is `https://wa.me/` followed by the digits of the owner-confirmed WhatsApp number (configured outside the repository, V5.19/V5.20), with no `+`, space or punctuation, and the label in the owner's grouping («+39», then 3-3-4). The WhatsApp `tel:` link is exposed but not drawn, which is a reasonable choice. | OK |
| §4 and §14 only official values replaced | Before this change the site published no official number. `+39 0000 000000` in `companies_demo.py` belongs to the fictional preview company and was kept. Test fixtures, legal sources and archived notes were not touched. No locked or prescribed text contains a contact line. | OK |
| §5 placement, no excessive repetition | The channels appear in the contact-page chapter, the footer and the phone menu sheet below 80rem. The mega menu, the error pages and the e-mails were left out deliberately, and the reasons are recorded. The contact page's `<main>` shows each link exactly once (tested). | OK |
| §6 and §10 icons | The Numero Verde uses the ILE `phone` icon. WhatsApp uses Lucide `message-circle` (ISC) beside the word «WhatsApp», so it is never drawn as a plain number. No brand glyph was used: Meta's guidelines require the glyph unaltered, and a CC0 copy carries no trademark licence. Both points are recorded in `ICON_LICENSES.md` (77 donors, log line). The registry and DESIGN_SYSTEM icon counts are updated. The `ile-steps` icon is not used. | OK |
| §8 accessible names | `aria-label` reads «Appeler le numéro vert 800 642 015» and «Contacter Italy Legal Entry sur WhatsApp au …» (the owner-confirmed WhatsApp number (configured outside the repository, V5.19/V5.20)), with the it/en/ar versions as §8 gives them. Every catalogue is at 100 %. See m-1 for the Arabic case. | OK, see m-1 |
| §9 and §12 Arabic order | Rendered DOM: every number is `<bdi class="phone" dir="ltr">`. Headed Chromium (below) gave computed `direction: ltr` and showed the first digit drawn left of the last on every surface. Screenshots: `shots/contact-ar-360.png`, `shots/sheet-ar-390.png`, `shots/footer-view-ar-360.png`. | OK |
| §11 contact page | Two cards in the page header's disc style, one link each (114 to 123 px tall). Tokens only, logical properties, reduced-motion and forced-colours rules. Hierarchy: kind, then the number, then the action. The design is coherent with the e-mail and form chapters and is not overdecorated (`shots/contact-fr-1440.png`). | OK |
| §12 tap targets and wrapping | Headed Chromium, touch, at 390 and 360 in fr and ar. Contact-page cards measure 320 to 350 × 114 to 122. Footer links measure 190 to 228 × 44. Sheet buttons measure 156 to 171 × 44. Every number sits on one line, and no page scrolls horizontally. At 1440 with a fine pointer the footer links are 24 px tall, the same as every other footer link. | OK |
| §13 structured data | The existing Organization node gains `"telephone": "800 642 015"`. No ContactPoint or other new type was added (tested). The JSON parses, and the graph still holds only Organization and WebSite. | OK |
| §15 tests | The new `apps/pages/tests/test_contact_channels_v519.py` covers canonical values, separators, validators, the settings row, the no-template-literal guard, three surfaces in four languages, obsolete numbers on public pages, Arabic order, blank-withdraws-channel and JSON-LD. The new browser test covers 44 px targets, one-line numbers and LTR order. `test_institutional` replaced its old «no `tel:`» check with stricter positive checks: only the two labels may appear as numbers on the page. See m-3. | OK |

## Test results (review run, lane l9, `test_ile_v5_l9`)

The run covered `test_contact_channels_v519`, `test_institutional`, `test_seo`, `test_icons`, `test_layout`, `test_forms_v515_b`, `test_interior_w3_f1`, `test_nav_sheet_w2_c2`, `test_motion_v512_a_w2`, `tests/i18n/test_ui_translations` and `apps/core`, excluding browser tests. Result: **340 passed, 4 skipped, 0 failed** in 12 min 17 s. The 4 skips are `/xx/faq/`, which is gated (404) on this database.

## Headed Chromium (lock `v519-k-review`, 22:53 to 22:55, lane server 8789)

The probe data is in `probe.json`, and the screenshots are in `shots/`: contact page, footer and sheet in ar and fr at 390 and 360, plus 1440. The footer element screenshots show the sticky header over the first line; that comes from the capture method, so I retook them as viewport shots (`footer-view-*`). The probe script is at `C:/tmp/ile_v5_council/.work/v519-k-review/shots.py`. Playwright's bundled chromium-1243 is not installed, so the run used chromium-1234 through `executable_path`.

## Findings (all minor)

- **m-1 (Arabic label in name).** The Arabic accessible name says «واتساب», but the visible word is «WhatsApp» in Latin script. On the sheet's button the visible text is only «WhatsApp», so the name does not contain the visible label (WCAG 2.5.3). Commit 66172e5 already treats «WhatsApp» as a proper noun in the Arabic interface. Suggested fix: write «عبر WhatsApp» in the Arabic msgstr of «Contacter Italy Legal Entry sur WhatsApp au {{ number }}», recompile, and update `NAMES["ar"]` in the test. I did not apply it because it is the translator's register decision.
- **m-2 (example numbers in the back office).** The admin help texts and validator messages in `models.py`, migration 0003 and the four catalogues quote 800 642 015 and the owner-confirmed WhatsApp number (configured outside the repository, V5.19/V5.20) as examples. These are not public surfaces and do not break §3. If a number ever changes, though, those examples will be out of date. A neutral example (e.g. «800 000 000») would avoid that. Optional.
- **m-3 (budget ceiling raised).** `tests/frontend/test_forms_v515_b.py` raises the `main.css` gzip ceiling from 33 448 to 33 600: +124 B for this lane. `design-v5` was already at 33 455 B after the v518 merge. The new value is lane A's recorded V5.15 ceiling and the change is documented, so I accept it. The steward should be aware that a ratchet was loosened.
- **m-4 (migration data step).** `AddField` already writes the defaults into the existing row, so the `RunPython` step only covers a row that is blank, which cannot happen after AddField. It is harmless.
- **m-5 (sheet button).** The sheet's Numero Verde button shows only the number, without the words «Numéro vert». Its accessible name carries the full meaning, and the width at 360 px justifies the choice. No action needed.

## Merge note

`v519-k` is a fast-forward of `design-v5` (900372a). Moving `design-v5` and recording ownership of the slices (lane D's `footer.html` and `main_nav.html`, lane C's `contact.html`, plus `chrome.css`, `icons.py` and the catalogues, all under DECISIONS §10.0) is the steward's step.
