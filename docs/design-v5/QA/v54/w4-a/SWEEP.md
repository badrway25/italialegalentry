# W4-A — the mobile + RTL sweep: before the fixes, and after

16 October 2026 · implementer `w4-a-impl-1` · branch `v54-w4-a` from design-v5 `a833403` (tag `v54/wave-4`) · plan §3.6 item 1,
§1.12, SP-8, N13 / N14 / N19, §2.5 (RTL), §2.6 · lane 8786 on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`, DEBUG on).

## What was swept, and how

- **Every surface** of `docs/design-v5/live_status.json`, by the preview's own registry (`apps/designpreview/live.py`:
  `PUBLIC_PAGES`, `PERSONA_PAGES`, `STATE_PAGES` resolved by URL name), plus what the preview has no persona for: the
  organisations' bridge for each organisation account type (a company — `seed-company`; an institution and a university —
  two accounts created **on the lane clone only**, `w4a-institution`, `w4a-university`; a professional actor — `seed-actor`),
  the staff pages through the role accounts (`helpdesk-queue`, `console-unavailable` — `demo-professionnel`;
  `helpdesk-dispatch` and the operator's dashboard — `demo-operateur`; `selection-workspace` — `demo-acteur-autorise`),
  the 410, the public menu open, the overlay states (the console drawer, the documents' filter sheet, the console's and the
  public header's account menus), the product's 400 / 404 / 500 (`/_errors/<n>/` — under DEBUG a path that resolves to
  nothing draws Django's technical page, not the product's: the census's `/page-inexistante/` and the closed virtual forum
  were that page on the lane, and left the matrix), and the dev-only design showcase. **106 page states × fr, ar.**
- Sessions minted with `Client.force_login` against `ile_v5_l6` by a scratch script outside every repository (no password
  used, typed or stored). Headless Chromium (Playwright 1.63), one browser, its own profile
  (`C:/tmp/ile_v5_council/.profiles/w4-a-impl-1-<mode>/`).
- **Viewports:** 360 × 800, 375 × 812, 390 × 844, 412 × 915, 430 × 932 (portrait), 844 × 390 and 932 × 430 (landscape),
  390 × 640 (short), each a fresh load, captured; 320 × 640 for the overflow probe; all under a **coarse pointer**
  (`is_mobile` + `has_touch`: overlay scrollbars, `pointer: coarse`, no hover). A second pass at 390 × 844 under a **fine
  pointer** (a desktop window narrowed: classic scrollbar, the 24 px floor). A third, in Arabic at 360 / 390 / 412: the
  **overflow probes** (D21 / O86) — a long Arabic word, mixed Latin and Arabic with Arabic-Indic and Western digits, a
  reference and a phone number appended to every heading, label, control, cell, chip and title of the page; and the same
  values set as the whole text of the slots that hold what people write (an e-mail, a file name, a company's name, a
  subject).
- **The probe** (`probe.js`, per load): the page and every element against the viewport (`scrollWidth` = `clientWidth`, and
  no box sticking out unless inside a scroller); the chrome that stays on screen at rest and at four scroll depths (every
  fixed or stuck sticky element, their union); the first object (the visible `h1`, else the first heading; and the page's
  one primary) against the band the chrome leaves; every target measured by `elementFromPoint` — its real hit extent
  through its middle, so a target's own `::before` / `::after` area counts and a neighbour's does not (44 × 44 under a
  coarse pointer, 24 × 24 under a fine one; a link inside a sentence is WCAG 2.5.8's inline exception and is counted
  apart); in Arabic, every icon of the closed flip list (`apps/core/icons.py` `FLIP_RTL`) and every other icon (flipped
  exactly when it should be, by the transform chain), the lock-up (`direction: ltr`, the mark before the name), text arrows
  in a right-to-left run, references and phone numbers outside an isolate, and text aligned left.
- **Looked at:** every capture, as one contact sheet per page × language (the eight captures at 0.6, each labelled with the
  probe's flags) — 212 sheets, one line each in the review log; details at 2× where a sheet raised a doubt.
- Evidence (outside the repository): `C:/tmp/ile_v5_council/evidence/v54/w4-a/before/` — `coarse/`, `fine/`, `stress/`
  (`results.jsonl`, the captures, `_sheets/`), `aggregate_coarse.json`; the scripts in
  `C:/tmp/ile_v5_council/.work/w4-a/w4-a-impl-1/` (`sweep.py`, `probe.js`, `sheets.py`, `aggregate.py`, `userdata_probe.py`,
  the review log `visual_before.md`).

## What holds everywhere (no defect)

- **The phone chrome ≤ 120 px** on every page and viewport: 114 px at most (the console's top bar 48 + the bottom bar's
  two-line labels 66, French, 360); the public letterhead 57; landscape 103 at most (the glossary's A–Z index under the bar,
  of 390); the short height 114. No sticky head eats a landscape screen (the console's top bar leaves with the page below
  480 px of height), no action bar is trapped, every sheet and drawer scrolls where it is taller than the screen.
- **No horizontal overflow** on any product page from 320 to 430 px, nor in landscape (1 818 probed loads; the dev-only
  showcase apart, D13). Every box that passes the edge lives inside a scroller drawn as one (the Academy's and the needs'
  state filters, the documents' table region) or is a register row's first point, clipped by design (`_registers.css`).
- **The first object** — the title, or the one primary — in the first screen on every page at every portrait width and on
  the short height; in landscape too, except D12.
- **The mirrors:** the overlay contract's edges (the console drawer from the inline start; the public sheet full screen on a
  phone, from the inline end from 48rem; the bottom sheets from the bottom; the account menu a bottom sheet on a phone, a
  popover at the inline end beyond), every «next» arrow and chevron of the flip list mirrored in Arabic and none other; the
  French calls on the Arabic home keep their own direction and their arrow (`pages.css`, the review's m3).
- **What never mirrors:** the lock-up (`direction: ltr`, the mark first), the console's mark and the rail's, the door stage
  on the home, the login, the error pages and the NowPanel, the steps glyph (Q8), references (`.reg-ref`, `.ws-case__ref`,
  `.t-ref`: isolates), dates; the native date field reads left to right. One exception: D8.

## The defects found

Severity: **major** — a WCAG 2.2 AA failure, a mirror the plan forbids, a broken order; **minor** — the plan's stricter
rules (SP-8's 44 px under a finger and 24 px floor, RE-4) where WCAG 2.5.8 still holds by size or spacing, robustness,
typography; **record** — not this area's to change.

| id | severity | what | where (page states) | owning file (family) | decision |
|---|---|---|---|---|---|
| D1 | minor | the public footer's links are 24 px boxes on a 32 px pitch under a finger (the legal list, the site list, the e-mail; the anti-fraud plate 38–40 px) — SP-8 asks 44 | every public page and every page with the public chrome, every width, fr + ar | `static/css/v5/chrome.css` §8 (W2-C1) — shared `main.css` | fix: under a coarse pointer each link a 44 px row, the list's gap folded in; paid by deletions in `main.css` |
| D2 | minor | the «aiuto» help line's e-mail link: 24 px under a finger outside the reading pages (its 44 px area is scoped to `.lettura`) | the door pages, the project and interior pages, the companies' form (`ecosystem-form__destination`) | `static/css/v5/_pagina.css` (W3-F1) — page-only | fix: the trail's hit area for `.aiuto a` in the shared page partial, once (out of `_lettura.css`'s list) |
| D3 | minor | the legal pages' pending notice: its e-mail link is a 20 px box — under the 24 px floor and the 44 px | privacy, cookies, notes, terms, disclaimer — fine and coarse | `static/css/v5/_lettura.css` (W3-F2) — page-only | fix: 24 px box, 44 px under a finger |
| D4 | minor | orientation's «Vous avez un code de reprise ? …»: a stand-alone link on two lines of 20 px line boxes | orientation start, fr + ar, every width | `apps/orientation/static/orientation/wizard.css` (W3-F1) — page-only | fix: one box (inline-block), 44 px under a finger |
| D5 | minor | the stand-alone forward links on one or two lines of 22 px: «linea»'s «Voir le parcours …» / «Découvrir « Vivre en Italie »», and the companies form's privacy link (its 44 px area scoped to `.lettura`) | training; companies | `static/css/v5/_journey-passage.css` (W3-D); `_lettura.css` (W3-F2) | fix: one box, 24 px at least, 44 px under a finger |
| D6 | minor | forum registration closed: «Retour à la page du Forum» a 20 px box | forum-register, fine and coarse | `apps/forum/static/forum/forum.css` (W3-F1) — page-only | fix: 24 px box, 44 px under a finger |
| D7 | minor | the documents' foot links («Déposer un fichier hors exigence», «Registre complet», «Retour au registre des pièces») and the version's «Télécharger»: 20 px boxes under a fine pointer; under a finger the foot links' 44 px bands overlap when they stack (360, 375: 32 px) | «Mes pièces» (both routes), a requirement, the loose upload, the Conditions gate | `apps/portal/static/portal/v5/_workspace.css`, `_depot.css` (W3-C) — page-only | fix: 24 px boxes; the foot's rows 24 px apart under a finger |
| D8 | **major** | the company profile's contact line: the phone number is not isolated — on the Arabic page its digit groups run right to left («000000 0000 39+») | qa-company's «Mon entreprise», ar, every width | `templates/companies/profile.html` (W3-E) | fix: the e-mail and the phone each in a left-to-right isolate |
| D9 | minor | «Ma situation»'s Stepper, eight equal columns: 41 px at 360, 43 at 375 (36 at 320) — under 44 | «Ma situation» for the three persons, fr + ar | `apps/portal/static/portal/v5/_journey-stepper.css` (W3-D) — page-only | fix: below 23rem the row takes the page's gutters (45 px at 360) |
| D10 | minor | the dashboards' account block: «Profil» is 32 px wide under a finger | every dashboard and bridge below 64rem | `apps/portal/static/portal/v5/_dashboard.css` (W3-B) — the console bundle | fix: 44 px wide; paid by dead console rules |
| D11 | minor | a short forward link: «الشبكة» (the project page's «Le réseau», Arabic) 41.5 px wide under a finger | project, ar | `static/css/v5/_pagina.css` (W3-F1) — page-only | fix: the chapter's links widened about their middle, as the trail's |
| D12 | minor | the error pages with the chrome, on a phone on its side (844 × 390, 932 × 430): the door above the label puts the title at the screen's foot, half out | 403, 404, 410, the reserved area's 503 | `apps/cms/static/cms/errori.css` (W3-F2) — page-only | fix: on a short landscape screen the door takes the end seat (the 64rem layout), the title rises |
| D13 | dev | the design showcase `/_design/` is 126–304 px wider than the screen at every phone width (in Arabic the page's start is cut) | `/_design/`, fr + ar | `templates/dev/showcase.html`, `static/css/dev/showcase.css` (no owner: the steward's slice) | fix if cheap |
| D14 | record | locked French copy breaks before its «:» or after its «« (an ordinary space inside the locked string): a line starts with «: langue italienne» or ends on «vous «» | antifraud (360, 375); «Vivre en Italie» (landscape) | locked copy — B1 item 8 (the owner's and counsel's) | record: the typography filter never touches locked copy (`pages_typo.py`) |
| D15 | minor | team-authored catalogue strings break the same way: the FAQ's search hint («« / diplôme »», «» .»), the 500's «; vous pouvez réessayer» | faq (360, 375); 500 (360), fr | `templates/faq/index.html`, `templates/errors/500.html` (W3-F2) | fix: the `typo` filter (W2-D's) on those strings |
| D16 | minor | the console phone bar's title: a record's own title in another language (a French course title on an Arabic page, no `lang`) is cut at its START — the reader sees its end | qa-person's enrolment, ar, every width | `apps/portal/static/portal/v5/_shell.css` (W3-A) — the console bundle | fix: the title takes its direction from its own first letter (`unicode-bidi: plaintext`): cut at its own end, W3-A's rule for every title, with or without a `lang` |
| D17 | — | (withdrawn) «Ma situation»'s «1 / 8» drawn «8 / 1» in Arabic: two numbers around a slash in a right-to-left paragraph read 1 first — the Arabic reading order, as «الخطوة 1 من 7» beside it | — | — | not a defect |
| D18 | minor | the overflow probe: a company name with an unbreakable word longer than the column (34 Arabic letters) widens the company dashboard by 32 px at 360 — the head's words are a flex item that will not shrink below its longest word | qa-company's dashboard, ar (stress) | `apps/portal/static/portal/v5/_frame.css` (W3-B / W3-E) — the console bundle | fix: the head's words may shrink, the title wraps anywhere |
| D19 | minor | the Forum's gallery: a native `<video controls>` on an Arabic page takes the page's direction — media controls never mirror (no video on the lane: not captured) | the Forum's permanent sections | `apps/forum/static/forum/forum.css` (W3-F1) — page-only | fix: the video left to right |
| D20 | minor | at 320 (≤ 20.5rem) the lock-up is the mark alone, a 38 px wide link — and the sheet's head's | every public page and the open menu, 320 | `static/css/v5/chrome.css` §1, §7 (W2-C1) — shared `main.css` | fix: 44 px wide under a finger |
| D21 | minor | (W3-D's hand-off) «la linea»'s station words are 15 px on a phone — RE-4 / SP-7 ask a phone's reading text one step up (W3-D's own line, dropped to keep the door pages identical) | the companies' and the orientation's passages, diplomas, training, every portrait width | `static/css/v5/_journey-passage.css` (W3-D) — page-only | fix: W3-D's line restored, below 64rem |

The probe's other flags, read and set aside: the register rows' first point clipped by design; a text «cut» that is a link's
own hit area counted in its `scrollWidth` (the trail, «Gérer», the error pages' links, «Télécharger») or a table's visually
hidden head (the dispatch, the Academy course); the glossary's terms at 39 px in landscape, their 44 px area cut by the
sticky A–Z index at that scroll position; the synthetic overflow probes that widen a page only through fixed interface
strings (a label, a button, a heading that never holds a person's words: no real string comes near) — the slots that hold
what people write (a request's subject, a ticket, the e-mail address, a file's name, the organisation, the profile's
facts) hold the long e-mail, the long file name, the long word and the mixed run without overflow, D18 apart.

## The table — page × width × language

`·` none · `—` not run. Columns: the eight captured viewports and 320 under a finger, then the fine-pointer pass at 390 and the
Arabic overflow probes.

| page | lang | 360 | 375 | 390 | 412 | 430 | 844×390 | 932×430 | 390×640 | 320 | fine 390 | stress ar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| home | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| home | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| login | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| login | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| signup | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| signup | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| password-reset | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| password-reset | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| password-reset-done | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| password-reset-done | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| email-verification-sent | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| email-verification-sent | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| pathways | ar | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · | · |
| pathways | fr | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · |  |
| companies | ar | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D5 | D1 D2 D5 | D1 D2 D21 D5 | D1 D2 D20 D21 D5 | D5 | · |
| companies | fr | D1 D2 D21 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D5 | D1 D2 D5 | D1 D2 D21 D5 | D1 D2 D20 D21 | D5 |  |
| institutions | ar | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · | · |
| institutions | fr | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · |  |
| universities | ar | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · | · |
| universities | fr | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · |  |
| forum | ar | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · | · |
| forum | fr | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · |  |
| project | ar | D1 D11 | D1 D11 | D1 D11 | D1 D11 | D1 D11 | D1 D11 | D1 D11 | D1 D11 | D1 D11 D20 | · | · |
| project | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| pilot | ar | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · | · |
| pilot | fr | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · |  |
| agami | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| agami | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| network | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| network | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| antifraud | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| antifraud | fr | D1 D14 | D1 D14 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| orientation | ar | D1 D21 D4 | D1 D21 D4 | D1 D21 D4 | D1 D21 D4 | D1 D21 D4 | D1 D4 | D1 D4 | D1 D21 D4 | D1 D20 D21 D4 | · | · |
| orientation | fr | D1 D21 D4 | D1 D21 D4 | D1 D21 D4 | D1 D21 D4 | D1 D21 D4 | D1 D4 | D1 D4 | D1 D21 D4 | D1 D20 D21 D4 | D4 |  |
| orientation-resume | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| orientation-resume | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| pathway-detail | ar | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · | · |
| pathway-detail | fr | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 | D1 D2 D20 | · |  |
| diplomas | ar | D1 D2 D21 | D1 D2 D21 | D1 D2 D21 | D1 D2 D21 | D1 D2 D21 | D1 D2 | D1 D2 | D1 D2 D21 | D1 D2 D20 D21 | · | · |
| diplomas | fr | D1 D2 D21 | D1 D2 D21 | D1 D2 D21 | D1 D2 D21 | D1 D2 D21 | D1 D2 | D1 D2 | D1 D2 D21 | D1 D2 D20 D21 | · |  |
| training | ar | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D5 | D1 D2 D5 | D1 D2 D21 D5 | D1 D2 D20 D21 D5 | D5 | · |
| training | fr | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D21 D5 | D1 D2 D5 | D1 D2 D5 | D1 D2 D21 D5 | D1 D2 D20 D21 D5 | D5 |  |
| living | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| living | fr | D1 | D1 | D1 | D1 | D1 | D1 D14 | D1 D14 | D1 | D1 D20 | · |  |
| living-topic | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| living-topic | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| news | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| news | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| faq | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| faq | fr | D1 D15 | D1 D15 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| glossary | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| glossary | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| glossary-term | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| glossary-term | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| partners | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| partners | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| contact | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| contact | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| contact-form | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| contact-form | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| company-needs | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| company-needs | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| institution-proposal | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| institution-proposal | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| university-proposal | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| university-proposal | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| enquiry-done | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| enquiry-done | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| forum-register | ar | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D20 D6 | · | · |
| forum-register | fr | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D6 | D1 D20 D6 | D6 |  |
| privacy | ar | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 | D1 D3 | D1 D3 | D1 D20 D3 | · | · |
| privacy | fr | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D20 D3 | D3 |  |
| cookies | ar | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 | D1 D3 | D1 D3 | D1 D20 D3 | · | · |
| cookies | fr | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D20 D3 | D3 |  |
| notices | ar | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D20 D3 | · | · |
| notices | fr | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D20 D3 | D3 |  |
| terms | ar | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D20 D3 | · | · |
| terms | fr | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D20 D3 | D3 |  |
| disclaimer | ar | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D20 D3 | · | · |
| disclaimer | fr | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D3 | D1 D20 D3 | D3 |  |
| qa-doc-person:dashboard | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:dashboard | fr | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | · |  |
| qa-doc-person:cases | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:cases | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:case | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:case | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:documents | ar | · | · | · | · | · | · | · | · | · | D7 | · |
| qa-doc-person:documents | fr | D7 | D7 | · | · | · | · | · | · | D7 | D7 |  |
| qa-doc-person:documents-app | ar | · | · | · | · | · | · | · | · | · | D7 | · |
| qa-doc-person:documents-app | fr | · | · | · | · | · | · | · | · | · | D7 |  |
| qa-doc-person:document-requirement | ar | · | · | · | · | · | · | · | · | · | D7 | · |
| qa-doc-person:document-requirement | fr | · | · | · | · | · | · | · | · | · | D7 |  |
| qa-doc-person:document-upload | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:document-upload | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:situation | ar | D9 | · | · | · | · | · | · | · | D9 | · | · |
| qa-doc-person:situation | fr | D9 | D9 | · | · | · | · | · | · | D9 | · |  |
| qa-doc-person:requests | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:requests | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:journey | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:journey | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:deadlines | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:deadlines | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:messages | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:messages | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:academy | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:academy | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:academy-course | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:academy-course | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:profile | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-doc-person:profile | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| qa-doc-person:account-email | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-doc-person:account-email | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| qa-doc-person:account-password | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-doc-person:account-password | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| qa-doc-person:account-mfa | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-doc-person:account-mfa | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| qa-doc-person:account-delete | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-doc-person:account-delete | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| qa-doc-person:logout | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-doc-person:logout | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| qa-person:dashboard | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:dashboard | fr | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | · |  |
| qa-person:case | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:case | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:documents | ar | · | · | · | · | · | · | · | · | · | D7 | · |
| qa-person:documents | fr | · | · | · | · | · | · | · | · | · | D7 |  |
| qa-person:document-upload | ar | · | · | · | · | · | · | · | · | · | D7 | · |
| qa-person:document-upload | fr | · | · | · | · | · | · | · | · | · | D7 |  |
| qa-person:situation | ar | D9 | · | · | · | · | · | · | · | D9 | · | · |
| qa-person:situation | fr | D9 | D9 | · | · | · | · | · | · | D9 | · |  |
| qa-person:requests | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:requests | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:request-detail | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:request-detail | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:journey | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:journey | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:deadlines | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:deadlines | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:messages | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:messages | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:helpdesk | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:helpdesk | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:helpdesk-detail | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:helpdesk-detail | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:helpdesk-new | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:helpdesk-new | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:academy-mine | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:academy-mine | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:academy-enrolment | ar | D16 | D16 | D16 | D16 | D16 | D16 | D16 | D16 | D16 | · | · |
| qa-person:academy-enrolment | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:profile | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-person:profile | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| qa-fresh-person:dashboard | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-fresh-person:dashboard | fr | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | · |  |
| qa-fresh-person:documents | ar | · | · | · | · | · | · | · | · | · | D7 | · |
| qa-fresh-person:documents | fr | D7 | D7 | · | · | · | · | · | · | D7 | D7 |  |
| qa-fresh-person:situation | ar | D9 | · | · | · | · | · | · | · | D9 | · | · |
| qa-fresh-person:situation | fr | D9 | D9 | · | · | · | · | · | · | D9 | · |  |
| qa-fresh-person:profile | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-fresh-person:profile | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| qa-company:company | ar | · | · | · | · | · | · | · | · | · | · | D18 |
| qa-company:company | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company-profile | ar | D8 | D8 | D8 | D8 | D8 | D8 | D8 | D8 | D8 | D8 | · |
| qa-company:company-profile | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company-needs-list | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-company:company-needs-list | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company-need-form | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-company:company-need-form | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company-analysis | ar | D1 | D1 | D1 | D1 | D1 | D1 D12 | D1 | D1 | D1 D20 | · | · |
| qa-company:company-analysis | fr | D1 | D1 | D1 | D1 | D1 | D1 D12 | D1 | D1 | D1 D20 | · |  |
| qa-company:profile | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| qa-company:profile | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| error-404 | ar | D1 | D1 | D1 | D1 | D1 | D1 D12 | D1 | D1 | D1 D20 | · | · |
| error-404 | fr | D1 | D1 | D1 | D1 | D1 | D1 D12 | D1 | D1 | D1 D20 | · |  |
| orientation-step | ar | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · | · |
| orientation-step | fr | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 | D1 D20 | · |  |
| navbar-open | ar | · | · | · | · | · | · | · | · | D20 | · | · |
| navbar-open | fr | · | · | · | · | · | · | · | · | D20 | · |  |
| error-410 | ar | D1 | D1 | D1 | D1 | D1 | D1 D12 | D1 | D1 | D1 D20 | · | · |
| error-410 | fr | D1 | D1 | D1 | D1 | D1 | D1 D12 | D1 | D1 | D1 D20 | · |  |
| seed-company:org-bridge | ar | · | · | · | · | · | · | · | · | · | · | · |
| seed-company:org-bridge | fr | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | · |  |
| w4a-institution:org-bridge | ar | · | · | · | · | · | · | · | · | · | · | · |
| w4a-institution:org-bridge | fr | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | · |  |
| w4a-university:org-bridge | ar | · | · | · | · | · | · | · | · | · | · | · |
| w4a-university:org-bridge | fr | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | · |  |
| seed-actor:org-bridge | ar | · | · | · | · | · | · | · | · | · | · | · |
| seed-actor:org-bridge | fr | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | · |  |
| helpdesk-queue | ar | · | · | · | · | · | · | · | · | · | · | · |
| helpdesk-queue | fr | · | · | · | · | · | · | · | · | · | · |  |
| console-unavailable | ar | D1 | D1 | D1 | D1 | D1 | D1 D12 | D1 | D1 | D1 D20 | · | · |
| console-unavailable | fr | D1 | D1 | D1 | D1 | D1 | D1 D12 | D1 D12 | D1 | D1 D20 | · |  |
| helpdesk-dispatch | ar | · | · | · | · | · | · | · | · | · | · | · |
| helpdesk-dispatch | fr | · | · | · | · | · | · | · | · | · | · |  |
| selection-workspace | ar | · | · | · | · | · | · | · | · | · | · | · |
| selection-workspace | fr | · | · | · | · | · | · | · | · | · | · |  |
| operator-dashboard | ar | · | · | · | · | · | · | · | · | · | · | · |
| operator-dashboard | fr | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | D10 | · |  |
| showcase | ar | D13 | D13 | D13 | D13 | D13 | D13 | D13 | D13 | D13 | D13 | · |
| showcase | fr | D13 | D13 | D13 | D13 | D13 | D13 | D13 | D13 | D13 | D13 |  |
| error-400 | ar | · | · | · | · | · | · | · | · | D20 | · | · |
| error-400 | fr | · | · | · | · | · | · | · | · | D20 | · |  |
| error-500 | ar | · | · | · | · | · | · | · | · | D20 | · | · |
| error-500 | fr | D15 | · | · | · | · | · | · | · | D20 | · |  |
| console-drawer | ar | · | · | · | · | · | · | · | · | · | — | · |
| console-drawer | fr | · | · | · | · | · | · | · | · | · | — |  |
| documents-filter-sheet | ar | · | · | · | · | · | · | · | · | · | — | · |
| documents-filter-sheet | fr | · | · | · | · | · | · | · | · | · | — |  |
| console-account-menu | ar | · | · | · | · | · | · | · | · | · | — | · |
| console-account-menu | fr | · | · | · | · | · | · | · | · | · | — |  |
| public-account-menu | ar | · | · | · | · | · | · | · | · | · | — | · |
| public-account-menu | fr | · | · | · | · | · | · | · | · | · | — |  |

## After the fixes — the same sweep, again

16 October 2026, on the fixed tree (the commits `f557a61` … `e4f54f3`; the 500's sentence re-swept after its own fix,
`2a5592f`), the lane restarted (with `--noreload` the template loader keeps what it first read) and the browser
profiles' caches emptied: the same 106 page states, the same matrix and the same probe (`E/after/`) — 1 818 page loads
probed under a finger and the 74 overlay states, 202 under a mouse, 303 overflow probes in Arabic —, and every capture
looked at again: 212 contact sheets, one line each (S/`visual_after.md`). That look found two defects the first one had
missed (D22, D23 below), both in W3-E's registers; once they were fixed, the 25 page states that link the registers'
sheet were swept again on the same matrix (`E/after2/`) and their 50 sheets looked at. The table at the end is the
after sweep with those 25 pages' rows replaced by the re-sweep's.

**Cleared**, each where the table above placed it:

- D1, D2, D3, D4, D5, D6, D7, D10, D11, D20 — no target under 44 × 44 under a finger on a product page, none under the
  24 px floor under a mouse: the small targets under a finger 16 464 → 410, under a mouse 44 → 14, and what is left is
  the dev showcase's own (its table of contents, its sample breadcrumbs, buttons, table links and account menu) but for
  two product cases set out below;
- D8 — no phone number or reference outside an isolate: the company's phone reads «+39 …» left to right on the Arabic
  page;
- D9 — the Stepper's eight columns are 44 px from 360 (the three persons, fr and ar);
- D12 — the first object in the first screen on every page and viewport, landscape included (9 page states → 0);
- D13 — the showcase fits every width (126–304 px too wide → 0), its start no longer cut in Arabic;
- D15 — the FAQ's hint and the 500's sentence keep their guillemets and their «;» with their words at 360 and 375;
- D16 — the Arabic phone bar's French course title starts with its first word, the ellipsis at its end;
- D18 — the company dashboard holds the 34-letter name; the overflow probes widen 18 page states instead of 45, each
  through a fixed interface string only (a label, a button, a heading no person writes), never a slot that holds a
  person's words;
- D19 — held by a test (no video on the lane);
- D21 — the station words at 17 px below 64rem on the four pages that draw them, 15 px on a desktop.

**Found by the after look — present before too** (the same rows in the before captures; the first look missed them,
and the table above is left as it was written):

| id | severity | what | where (page states) | owning file (family) | decision |
|---|---|---|---|---|---|
| D22 | minor | a register meta row's part in the other direction than its row — a reference (`.reg-ref`) or a date, left to right on an Arabic page, a name in its own script (`dir="auto"`) — hangs its point and its pull on its own start, which is the row's end: a «·» closes the line («· A13BD5582C» on the help desk, «طلب اتصال  contact-2 ·» in «Mes demandes»), or two points meet before the next part (the staff queue's «5CFFEA1CD6 ⁚ في هذه الحالة …») — the registers' own rule puts the point between two parts, never at a line's end | qa-person's help desk and «Mes demandes», the Academy's plans, the help desk's staff queue — ar, every width | `apps/portal/static/portal/v5/_registers.css` (W3-E) — page-only (the registers' sheet) | fix: such a part lays its point and its pull on the row's side (`flex-direction: row-reverse`, the pull on its own end) |
| D23 | minor | «Mon parcours»: a saved result's French title, two lines on a phone, stands at the Arabic page's far edge — W3-E's head rule (its review's minor 6: a title in the other direction than the page ends on the reading edge, wrapped or not) reads `:dir()`, and this title's `lang` turns it through main.css, not a `dir` | qa-person's «Mon parcours», ar, every portrait width | `apps/portal/static/portal/v5/_registers.css` (W3-E) | fix: the title joins that rule (`:dir(rtl) .reg-result__title:is([lang="fr"], [lang="it"], [lang="en"])`) |
| D24 | dev · record | the dev showcase on the Arabic page: its French copy carries no `lang`, so its stops stand at the left and a swatch's hex reads «ecebe6#» | `/_design/`, ar | `templates/dev/showcase.html` (no owner) | record: a dev page, not changed |

Measured on the lane before and after the fix (S/`d22.py`, `E/d22-before/`, `E/d22-after/`: each part's point box
against its words' own range; fr and ar, 390 and 1440, eight register pages): 24 rows with a point on the wrong side →
0; the title's two lines 184 and 124 px short of the Arabic reading edge → 0 and 0; the French pages unchanged.

From the hand-offs (`NOTES.md` §3), W4-B's O1 was measured and fixed on the same lane: Tab through every public page
state of the sweep, fr and ar, at 390 and 360 — 86 focus rings of 2 480 stops cut by the screen's bottom edge → 0
(`E/o1-before/`, `E/o1-final/`). After that last change to the shared sheet (`main.css`: the scroll padding's foot, and
D11's inline inset written as its block one), the fourteen page states that draw an arrow link were probed again on the
whole matrix (`E/after3/`, 252 + 28 loads): identical to the after sweep on every measure.

**What remains** — by design, recorded, or not this area's:

- D14 (record): the locked French copy's breaks beside «:» and inside «« »» (B1 item 8) — the anti-fraud page at 360 / 375,
  «Vivre en Italie» in landscape;
- the 429's «;» (the 500's sentence, D15): never reached on the lane, and W2-B's test holds its exact words — left as
  written;
- «Ma situation»'s Stepper at 320: 40 px a column (the gutters are spent; 44 from 360);
- the glossary's terms at 39 px in landscape at one scroll position, their 44 px area under the sticky A–Z index;
- the probe's flags that are the design: a register row's first point, clipped; a link's own hit area counted as «cut»;
- the showcase's own samples under 44 px (D24's page; a dev tool, not a product surface);
- real devices, WebKit and Firefox — W4-C's (O10).

### The table after the fixes

`·` none · `—` not run · the same columns as above · `(D9)` the Stepper at 320, 40 px a column (what remains) ·
`dev` the showcase's own samples (no overflow: D13 cleared) · D14 recorded, unchanged.

| page | lang | 360 | 375 | 390 | 412 | 430 | 844×390 | 932×430 | 390×640 | 320 | fine 390 | stress ar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| home | ar | · | · | · | · | · | · | · | · | · | · | · |
| home | fr | · | · | · | · | · | · | · | · | · | · |  |
| login | ar | · | · | · | · | · | · | · | · | · | · | · |
| login | fr | · | · | · | · | · | · | · | · | · | · |  |
| signup | ar | · | · | · | · | · | · | · | · | · | · | · |
| signup | fr | · | · | · | · | · | · | · | · | · | · |  |
| password-reset | ar | · | · | · | · | · | · | · | · | · | · | · |
| password-reset | fr | · | · | · | · | · | · | · | · | · | · |  |
| password-reset-done | ar | · | · | · | · | · | · | · | · | · | · | · |
| password-reset-done | fr | · | · | · | · | · | · | · | · | · | · |  |
| email-verification-sent | ar | · | · | · | · | · | · | · | · | · | · | · |
| email-verification-sent | fr | · | · | · | · | · | · | · | · | · | · |  |
| pathways | ar | · | · | · | · | · | · | · | · | · | · | · |
| pathways | fr | · | · | · | · | · | · | · | · | · | · |  |
| companies | ar | · | · | · | · | · | · | · | · | · | · | · |
| companies | fr | · | · | · | · | · | · | · | · | · | · |  |
| institutions | ar | · | · | · | · | · | · | · | · | · | · | · |
| institutions | fr | · | · | · | · | · | · | · | · | · | · |  |
| universities | ar | · | · | · | · | · | · | · | · | · | · | · |
| universities | fr | · | · | · | · | · | · | · | · | · | · |  |
| forum | ar | · | · | · | · | · | · | · | · | · | · | · |
| forum | fr | · | · | · | · | · | · | · | · | · | · |  |
| project | ar | · | · | · | · | · | · | · | · | · | · | · |
| project | fr | · | · | · | · | · | · | · | · | · | · |  |
| pilot | ar | · | · | · | · | · | · | · | · | · | · | · |
| pilot | fr | · | · | · | · | · | · | · | · | · | · |  |
| agami | ar | · | · | · | · | · | · | · | · | · | · | · |
| agami | fr | · | · | · | · | · | · | · | · | · | · |  |
| network | ar | · | · | · | · | · | · | · | · | · | · | · |
| network | fr | · | · | · | · | · | · | · | · | · | · |  |
| antifraud | ar | · | · | · | · | · | · | · | · | · | · | · |
| antifraud | fr | D14 | D14 | · | · | · | · | · | · | · | · |  |
| orientation | ar | · | · | · | · | · | · | · | · | · | · | · |
| orientation | fr | · | · | · | · | · | · | · | · | · | · |  |
| orientation-resume | ar | · | · | · | · | · | · | · | · | · | · | · |
| orientation-resume | fr | · | · | · | · | · | · | · | · | · | · |  |
| pathway-detail | ar | · | · | · | · | · | · | · | · | · | · | · |
| pathway-detail | fr | · | · | · | · | · | · | · | · | · | · |  |
| diplomas | ar | · | · | · | · | · | · | · | · | · | · | · |
| diplomas | fr | · | · | · | · | · | · | · | · | · | · |  |
| training | ar | · | · | · | · | · | · | · | · | · | · | · |
| training | fr | · | · | · | · | · | · | · | · | · | · |  |
| living | ar | · | · | · | · | · | · | · | · | · | · | · |
| living | fr | · | · | · | · | · | D14 | D14 | · | · | · |  |
| living-topic | ar | · | · | · | · | · | · | · | · | · | · | · |
| living-topic | fr | · | · | · | · | · | · | · | · | · | · |  |
| news | ar | · | · | · | · | · | · | · | · | · | · | · |
| news | fr | · | · | · | · | · | · | · | · | · | · |  |
| faq | ar | · | · | · | · | · | · | · | · | · | · | · |
| faq | fr | · | · | · | · | · | · | · | · | · | · |  |
| glossary | ar | · | · | · | · | · | · | · | · | · | · | · |
| glossary | fr | · | · | · | · | · | · | · | · | · | · |  |
| glossary-term | ar | · | · | · | · | · | · | · | · | · | · | · |
| glossary-term | fr | · | · | · | · | · | · | · | · | · | · |  |
| partners | ar | · | · | · | · | · | · | · | · | · | · | · |
| partners | fr | · | · | · | · | · | · | · | · | · | · |  |
| contact | ar | · | · | · | · | · | · | · | · | · | · | · |
| contact | fr | · | · | · | · | · | · | · | · | · | · |  |
| contact-form | ar | · | · | · | · | · | · | · | · | · | · | · |
| contact-form | fr | · | · | · | · | · | · | · | · | · | · |  |
| company-needs | ar | · | · | · | · | · | · | · | · | · | · | · |
| company-needs | fr | · | · | · | · | · | · | · | · | · | · |  |
| institution-proposal | ar | · | · | · | · | · | · | · | · | · | · | · |
| institution-proposal | fr | · | · | · | · | · | · | · | · | · | · |  |
| university-proposal | ar | · | · | · | · | · | · | · | · | · | · | · |
| university-proposal | fr | · | · | · | · | · | · | · | · | · | · |  |
| enquiry-done | ar | · | · | · | · | · | · | · | · | · | · | · |
| enquiry-done | fr | · | · | · | · | · | · | · | · | · | · |  |
| forum-register | ar | · | · | · | · | · | · | · | · | · | · | · |
| forum-register | fr | · | · | · | · | · | · | · | · | · | · |  |
| privacy | ar | · | · | · | · | · | · | · | · | · | · | · |
| privacy | fr | · | · | · | · | · | · | · | · | · | · |  |
| cookies | ar | · | · | · | · | · | · | · | · | · | · | · |
| cookies | fr | · | · | · | · | · | · | · | · | · | · |  |
| notices | ar | · | · | · | · | · | · | · | · | · | · | · |
| notices | fr | · | · | · | · | · | · | · | · | · | · |  |
| terms | ar | · | · | · | · | · | · | · | · | · | · | · |
| terms | fr | · | · | · | · | · | · | · | · | · | · |  |
| disclaimer | ar | · | · | · | · | · | · | · | · | · | · | · |
| disclaimer | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:dashboard | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:dashboard | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:cases | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:cases | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:case | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:case | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:documents | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:documents | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:documents-app | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:documents-app | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:document-requirement | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:document-requirement | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:document-upload | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:document-upload | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:situation | ar | · | · | · | · | · | · | · | · | (D9) | · | · |
| qa-doc-person:situation | fr | · | · | · | · | · | · | · | · | (D9) | · |  |
| qa-doc-person:requests | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:requests | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:journey | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:journey | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:deadlines | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:deadlines | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:messages | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:messages | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:academy | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:academy | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:academy-course | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:academy-course | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:profile | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:profile | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:account-email | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:account-email | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:account-password | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:account-password | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:account-mfa | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:account-mfa | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:account-delete | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:account-delete | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-doc-person:logout | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-doc-person:logout | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:dashboard | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:dashboard | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:case | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:case | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:documents | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:documents | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:document-upload | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:document-upload | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:situation | ar | · | · | · | · | · | · | · | · | (D9) | · | · |
| qa-person:situation | fr | · | · | · | · | · | · | · | · | (D9) | · |  |
| qa-person:requests | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:requests | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:request-detail | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:request-detail | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:journey | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:journey | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:deadlines | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:deadlines | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:messages | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:messages | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:helpdesk | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:helpdesk | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:helpdesk-detail | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:helpdesk-detail | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:helpdesk-new | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:helpdesk-new | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:academy-mine | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:academy-mine | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:academy-enrolment | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:academy-enrolment | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-person:profile | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-person:profile | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-fresh-person:dashboard | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-fresh-person:dashboard | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-fresh-person:documents | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-fresh-person:documents | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-fresh-person:situation | ar | · | · | · | · | · | · | · | · | (D9) | · | · |
| qa-fresh-person:situation | fr | · | · | · | · | · | · | · | · | (D9) | · |  |
| qa-fresh-person:profile | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-fresh-person:profile | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-company:company | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company-profile | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-company:company-profile | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company-needs-list | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-company:company-needs-list | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company-need-form | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-company:company-need-form | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:company-analysis | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-company:company-analysis | fr | · | · | · | · | · | · | · | · | · | · |  |
| qa-company:profile | ar | · | · | · | · | · | · | · | · | · | · | · |
| qa-company:profile | fr | · | · | · | · | · | · | · | · | · | · |  |
| error-404 | ar | · | · | · | · | · | · | · | · | · | · | · |
| error-404 | fr | · | · | · | · | · | · | · | · | · | · |  |
| orientation-step | ar | · | · | · | · | · | · | · | · | · | · | · |
| orientation-step | fr | · | · | · | · | · | · | · | · | · | · |  |
| navbar-open | ar | · | · | · | · | · | · | · | · | · | · | · |
| navbar-open | fr | · | · | · | · | · | · | · | · | · | · |  |
| error-410 | ar | · | · | · | · | · | · | · | · | · | · | · |
| error-410 | fr | · | · | · | · | · | · | · | · | · | · |  |
| seed-company:org-bridge | ar | · | · | · | · | · | · | · | · | · | · | · |
| seed-company:org-bridge | fr | · | · | · | · | · | · | · | · | · | · |  |
| w4a-institution:org-bridge | ar | · | · | · | · | · | · | · | · | · | · | · |
| w4a-institution:org-bridge | fr | · | · | · | · | · | · | · | · | · | · |  |
| w4a-university:org-bridge | ar | · | · | · | · | · | · | · | · | · | · | · |
| w4a-university:org-bridge | fr | · | · | · | · | · | · | · | · | · | · |  |
| seed-actor:org-bridge | ar | · | · | · | · | · | · | · | · | · | · | · |
| seed-actor:org-bridge | fr | · | · | · | · | · | · | · | · | · | · |  |
| helpdesk-queue | ar | · | · | · | · | · | · | · | · | · | · | · |
| helpdesk-queue | fr | · | · | · | · | · | · | · | · | · | · |  |
| console-unavailable | ar | · | · | · | · | · | · | · | · | · | · | · |
| console-unavailable | fr | · | · | · | · | · | · | · | · | · | · |  |
| helpdesk-dispatch | ar | · | · | · | · | · | · | · | · | · | · | · |
| helpdesk-dispatch | fr | · | · | · | · | · | · | · | · | · | · |  |
| selection-workspace | ar | · | · | · | · | · | · | · | · | · | · | · |
| selection-workspace | fr | · | · | · | · | · | · | · | · | · | · |  |
| operator-dashboard | ar | · | · | · | · | · | · | · | · | · | · | · |
| operator-dashboard | fr | · | · | · | · | · | · | · | · | · | · |  |
| showcase | ar | dev | dev | dev | dev | dev | dev | dev | dev | dev | dev | · |
| showcase | fr | dev | dev | dev | dev | dev | dev | dev | dev | dev | dev |  |
| error-400 | ar | · | · | · | · | · | · | · | · | · | · | · |
| error-400 | fr | · | · | · | · | · | · | · | · | · | · |  |
| error-500 | ar | · | · | · | · | · | · | · | · | · | · | · |
| error-500 | fr | · | · | · | · | · | · | · | · | · | · |  |
| console-drawer | ar | · | · | · | · | · | · | · | · | · | · | · |
| console-drawer | fr | · | · | · | · | · | · | · | · | · | · |  |
| documents-filter-sheet | ar | · | · | · | · | · | · | · | · | · | · | · |
| documents-filter-sheet | fr | · | · | · | · | · | · | · | · | · | · |  |
| console-account-menu | ar | · | · | · | · | · | · | · | · | · | · | · |
| console-account-menu | fr | · | · | · | · | · | · | · | · | · | · |  |
| public-account-menu | ar | · | · | · | · | · | · | · | · | · | · | · |
| public-account-menu | fr | · | · | · | · | · | · | · | · | · | · |  |
