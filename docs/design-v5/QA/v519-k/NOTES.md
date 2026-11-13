# Lane K (v519-k-build) — V5.19 contact information, owner-confirmed

> V5.20 (lane v520-wa, 30 October 2026): every form of the owner-confirmed WhatsApp number in this note now reads
> «the owner-confirmed WhatsApp number (configured outside the repository, V5.19/V5.20)» — the number is configured
> in the environment and the back office, never in a tracked file (`docs/design-v5/QA/v520/wa/NOTES.md`).

- 29 October 2026. Worktree `C:/tmp/ile_wt/v519-k`, branch `v519-k` from `design-v5` `238dc1c`.
- Directive `C:/tmp/ile_v5_council/directives/V5_19_CONTACT_INFORMATION_OWNER_CONFIRMED.md` (part of the V5.18 final
  stabilisation). The owner's direct order: the footer (lane D's) and the contact page (lane C's) are touched as small
  recorded slices, in the established premium system — no redesign, no alternative concept.

**CONTACT INFORMATION UPDATED / Numero Verde: 800 642 015 / WhatsApp: the owner-confirmed WhatsApp number (configured outside the repository, V5.19/V5.20) / https://wa.me/ followed by its digits**

## 1. Canonical configuration (§3)

The existing singleton `core.models.SiteSettings` (the one that already holds the public e-mail) gains two fields,
editable in the back office under «Contatti e versione»:

| field | value | validator |
|---|---|---|
| `freephone_number` | `800642015` | `core.contact.validate_national_number` (6–11 digits) |
| `whatsapp_number` | the owner-confirmed WhatsApp number (configured outside the repository, V5.19/V5.20) | `core.contact.validate_international_number` (`+` and 8–15 digits) |

- Defaults and the before-migrations fallback: `settings.ILE["FREEPHONE_NUMBER"]`, `settings.ILE["WHATSAPP_NUMBER"]`
  (`config/settings/base.py`); the model's defaults read them.
- Migration `core/0003_public_telephone_channels`: AddField (the defaults write the confirmed values into the existing
  row) + a data step that sets them on a row holding none.
- One helper, `apps/core/contact.py`: `public_channels()` → `{"freephone", "whatsapp"}`, each a `Channel(digits,
  label, tel_url, url)` — 800642015 / «800 642 015» / `tel:800642015`; for WhatsApp the owner-confirmed WhatsApp
  number (configured outside the repository, V5.19/V5.20): `+39…` / «+39 3xx xxx xxxx» / `tel:+39…` /
  `https://wa.me/39…`. Separators typed in the back office are dropped; a blank value
  withdraws the channel (nothing is drawn, never an empty link).
- The context processor `core.context_processors.site` exposes it as `site.channels`. **No template writes a number**
  (a test reads every template for the digit shapes).

## 2. Surfaces (§5, §11, §12)

| Surface | What | Files |
|---|---|---|
| Contact page | a new chapter «Par téléphone et WhatsApp» between «Par e-mail» and the form: two plates in the head's own disc idiom — Numero Verde (`phone`, «Numéro vert», the number, «Appeler») and WhatsApp (`message-circle`, «WhatsApp», the number, «Écrire sur WhatsApp»); one link per plate (≥ 114 px tall), two columns from 40rem, stacked below | `templates/pages/contact.html` (slice), `templates/pages/partials/_canali.html` (new), `apps/pages/static/pages/css/_canali.css` (new) + one import line in `interior.css` |
| Footer | under the e-mail: «Numéro vert 800 642 015» and «WhatsApp» with the owner-confirmed WhatsApp number (configured outside the repository, V5.19/V5.20), each with its glyph; 44 px under a finger | `templates/partials/footer.html` (slice), `static/css/v5/chrome.css` (slice after the colophon block) |
| Phone sheet (below 80rem) | the contact action: two 44 px plates first in the pinned night foot — the number dials, «WhatsApp» opens the app | `templates/partials/main_nav.html` (slice), `chrome.css` (same slice; forced-colours line) |
| Structured data | the existing `Organization` node gains `telephone: "800 642 015"`; no ContactPoint, no new type (WhatsApp has no schema.org property) | `apps/pages/services.py` (`home_jsonld`) |

Not added, by judgement (§5 «do not repeat both numbers excessively»): the desktop mega menu (it has no contact block;
the footer is on every page and the contact page is one link away), the error pages and the FAQ's «aiuto» line (they
point to the contact page and keep the address), the AGAMI identity plate (the promoter's own identity), the e-mails
(their texts name only the address), the console foot. The WhatsApp `tel:` link is exposed by the helper (`tel_url`)
but not drawn: the owner's channel is WhatsApp, not a second voice line.

Accessible names (§8), translated in the catalogue (fr source; it/en/ar): «Appeler le numéro vert 800 642 015» /
«Chiamare il numero verde …» / «Call the freephone number …» / «الاتصال بالرقم المجاني …»; «Contacter Italy Legal
Entry sur WhatsApp au …» / «Contattare Italy Legal Entry su WhatsApp al …» / «Contact Italy Legal
Entry on WhatsApp at …» / «التواصل مع Italy Legal Entry عبر واتساب على الرقم …». Each name contains the visible label.
Every visible number is `<bdi class="phone" dir="ltr">` (base.css `.phone` isolates it on an Arabic page) and
`white-space: nowrap`.

New msgids (13, added with `scripts/i18n_audit.py --sync`, translated, `--compile`; 3 666 msgids, 100 % in every
language; Arabic in the catalogue's register: verbal nouns for actions, «الرقم المجاني» for the Numero Verde,
«واتساب» in sentences, the visible brand word «WhatsApp» in Latin): «Par téléphone et WhatsApp», «Numéro vert»,
«Appeler», «Écrire sur WhatsApp», «Nous contacter» (the sheet's group name), the two accessible names, and the six
Italian back-office strings (field names, help texts, validator messages; fr/en/ar translated).

## 3. Icons (§10)

Lucide has no brand marks. A WhatsApp glyph was **not** used: Meta's WhatsApp brand guidelines ask for the glyph
unaltered (its shape and colours), which the ILE treatment (a 1.5 px stroke in `currentColor`) would alter, and a CC0
copy (Simple Icons) licenses the drawing, not the trademark. The channel is drawn with Lucide `message-circle`
(1.48.0, ISC, from the vendored package; 12 % tone in the bubble) beside its word «WhatsApp». Recorded in
`docs/design-v5/ICON_LICENSES.md` (77 donors, the §3 log line); registry `apps/core/icons.py` (chrome sprite, group
«Contatti e pagine pubbliche»; CHAPTER `telephone` → `phone` for the anchor `contact-voice-title`); sprite rebuilt
(`icons.svg` 17 039 → 17 464 B, ceiling 31 049); `tests/frontend/test_icons.py` 125 → 126 symbols. The Numero Verde
keeps the ILE `phone` drawing. Never `ile-steps`.

## 4. Audit (§4, §14) — what was retained and why

Searched: every number shape (`+39`, `0000 000000`, `0000000000`, `\d{3} \d{3}`), `tel:`, `wa.me`, `whatsapp`,
`telephone`/`téléphone`/`telefono`, schema.org, across templates (all languages are catalogue strings), apps, seeds,
`cms.locked_content`, e-mail templates, static JS, docs. **No official contact number was published before**: the
contact page said «no phone number is invented», and its test forbade any `tel:`. Retained:

| Where | Value | Why |
|---|---|---|
| `apps/companies/management/commands/companies_demo.py` | `+39 0000 000000` | the fictional preview company's referent phone (§14: a preview organisation, never the site's number) |
| test fixtures (`accounts`, `enquiries`, `forum`, `portal` tests) | `+212600000000`, `+39 041 123456`, `+39 0425 000000`, `+39 049 0000000`, `+39 000 000`, `+39 333 000 11 22` | personal/company profile test data; unrelated assertions |
| `docs/deployment/*` | `0000…0000` | SHA placeholders, not phone numbers |
| `docs/design-v5/QA/v54/w4-a/NOTES.md` | `+39 0000 000000` | historical QA note about the demo company |
| `cms.locked_content` | «Téléphone» | form field labels; no prescribed text carries a contact line (nothing to report) |
| `apps/integrations/openapi.py` | e-mail only | the API's metadata contact; not a public page |

Tests changed (not weakened): `apps/pages/tests/test_institutional.py` — the contact page's «no tel:» now asserts the
two confirmed links and that the only numbers on the page are the two labels; `apps/pages/tests/test_seo.py` — the
Organization's `telephone` is «800 642 015», and `contactPoint` joins the absent list.

## 5. Tests (§15)

- New `apps/pages/tests/test_contact_channels_v519.py`: canonical digits/labels/URLs; separators; validators; the
  settings row; no template writes a number; contact page, footer and sheet in fr/it/en/ar (exact hrefs, translated
  accessible names, isolated numbers, WhatsApp drawn with its glyph and word); no obsolete number and no other
  tel:/wa.me link on five public pages × four languages; Arabic digit order (every number inside an LTR isolate,
  nothing numeric outside it in the channel links); a blank setting withdraws its channel; JSON-LD.
- New `tests/frontend/test_browser_contact_channels_v519.py` (Playwright, touch, 390 and 360, fr and ar): every
  channel link ≥ 44 × 44, its number on one line, computed direction ltr, first digit drawn left of the last.
- Results on the merged tree (design-v5 5f92e4d + this lane), lane DB `test_ile_v5_l9_b`: the targeted set
  (pages contact/institutional/SEO, icons, bundles, layout, interior, forms budget, nav sheet, design docs, tokens,
  motion budget, tests/i18n, migration drift, apps/core) — 741 passed after one fix (the Arabic chrome's proper-noun
  list now names «WhatsApp», `tests/i18n/test_ui_translations.py`); the browser test — 4 passed (headless, under
  the Chromium lock). Failures seen in `tests/frontend` that are NOT this lane's (they fail identically on
  design-v5 without it): login invitation, account pages' frame («conto»), journey rail, 400/500 standalone, o14
  lint, brand-colour literals, `_platform.css` gradients, the persona switch (`caplog` when run with
  `-p no:logging`).
- main.css: design-v5 after the v518 merge measured 33 455 B gzip (over test_forms_v515_b's 33 448 line); with the
  channels 33 579 B — the line now reads lane A's V5.15 ceiling, 33 600 (as test_motion_v512_a_w2 does).

## 6. Headed review (Chromium, lock `v519-k-build`, 18:56–19:05)

Lane server 8789 (`ile_v5_l9`). Contact page, footer and sheet at 1440, 768, 390, 360 in fr and ar (shots kept outside
the repository: `C:/tmp/ile_v5_council/.work/v519-k/shots/`). Measured: plates 401 × 121 (1440), 328 × 114 (768), 350
× 116 (390), 320 × 116 (360); footer links 44 px tall under touch (24 px under a fine pointer, as every colophon link);
sheet plates 171–182 × 44; every number on one line, `direction: ltr`, groups in order in Arabic. One correction
found and made: base.css `ul[role="list"]` (0,1,1) took the footer list's margin — the rule now has two classes.

## 7. Merge

The v518 steward merge had already landed in `design-v5` (`5f92e4d`, DL54-175) when this lane finished: `design-v5`
was merged INTO `v519-k` (merge commit on the branch; conflicts only in the four catalogues — both sides appended,
the union kept and recompiled — and the compiled bundles, rebuilt). `v519-k` is therefore a fast-forward of
`design-v5`; moving `design-v5` itself, and recording the ownership of the slices (`footer.html`, `main_nav.html`,
`contact.html`, `chrome.css`, `icons.py`, the catalogues), is the steward's step.
