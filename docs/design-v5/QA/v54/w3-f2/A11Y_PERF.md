# W3-F2 · Accessibility + performance check — A11Y_PERF

Label `w3-f2-a11y-perf`, 11 October 2026, one pass (V5.5: implement → review once → fix → ship). Built nothing, changed
nothing in the family's code. Reviewed branch `v54-w3-f2` at `0e81923` (its code is `a420dad`'s: the later commit adds
`REVIEW.md` only), merge base `7d4ce79`, served by lane 4 from `C:/tmp/ile_wt/v54-w3-f2` on `ile_v5_l4`,
`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`: the dev server on 8784 for accessibility, then the
lane's compressed twin on 8784 for performance (the plan's 8782 shape: DEBUG off, `CompressedManifestStaticFilesStorage`,
hashed URLs, gzip on the wire, `collectstatic` of each tree into a scratch root; settings outside every repository).
Signed-in pages through sessions minted with `Client.force_login` on `ile_v5_l4` by a scratch script (no password used,
typed or stored; the five rows revoked at the end). The Forum Virtuel's flag was switched on, on `ile_v5_l4` only, for
its two pages and put back (row absent = the default; checked at the end). Headless Playwright Chromium
(HeadlessChrome 153), one browser and no pytest at a time; every browser start waited on `PERFORMANCE_BENCHMARK_LOCK`
(never present; this role never creates it). No run crashed. Never 8780, 8782, 9222 or 9223.

This is the role's second attempt: the first (21:24 – 22:46) ran every accessibility pass and most of the twin series,
then was cut (not crashed: its last record is a clean load). This pass continued from disk: the twin series completed
to n = 10 per cell and tree, the open items re-checked in one browser (`v2check`), the artefacts of the probes sorted
out, this report.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-f2/a11y-perf/` — `desk/` (1440 × 900, fine pointer), `phone/`
(390 × 844, touch), `reflow/` (320), `spacing/`, `reduce/`, `forced/`, `errors/` (forms sent empty), `interact/`,
`e429/`, `tophealth/`, `final_checks*.json`, `summary.json`, `twin/series/` (`runs.jsonl` — 160 traced loads,
`traces/`, `stats.json`), `v2check/` (`v2check.json` + crops). Probes: `C:/tmp/ile_v5_council/.work/w3-f2/w3-f2-a11y-perf/`.

Pages (35 states × fr, ar × 1440, 390 = 140): the FAQ (+ results, + none), the glossary (+ search) and a term, the
partners, the news (+ newsletter), «Vivre en Italie» and a topic, the Forum Virtuel and its join page, the three enquiry
forms and their answer, a legal page, the newsletter's confirmation and unsubscription; the 400, 403 (anonymous and
signed in), 404, 410, 429 and 500; the profile (person, company), the e-mail addresses (verified, unverified), the
password, the second factor and its activation, the deletion request and its answer, the sign-out's confirmation.

## Verdict — SHIP_AFTER_FIXES

0 blocking · 2 major · 3 minor. No P0. The area is keyboard-complete and screen-reader-sound in fr and ar: axe 0 on
140 page-states, every page one h1 and one main, nothing nameless, 4 492 Tab stops ringed and none under a sticky layer
(forwards on every page; backwards where the sticky parts are), 0 text under AA on pixels, reduced motion a real still,
forced colours usable, 0 overflow at 320 px and under text spacing. The two majors: a newsletter refusal nobody
perceives (the review's M3, confirmed with the accessibility facts) and the profile form's personal fields without an
input purpose (WCAG 1.3.5, older than this family, three lines). Performance: no real regression — JS unchanged, the
shared `main.css` 669 B lighter, the first-render task no worse on any cell, no long task added, LCP pooled inside
§2.6's +50 ms and a second under the budget, the LCP element text on every page, nothing loops; the content page type
stands over the interior CSS figure by its page-only sheet, for the merge's record.

## Findings

| # | Severity | What | Where | Fix |
|---|---|---|---|---|
| A1 | **major** | **A newsletter refusal is neither seen nor announced** (confirms REVIEW M3). Sent after the form's 3 s floor with a valid address and the consent unticked: the page returns to `/actualites/lettre-d-information/` at `scrollY` 0, focus on `body`, no summary. The error is tied to its field (`aria-invalid="true"` on the consent box, `aria-describedby` → «Le consentement est obligatoire pour envoyer la demande.») but stands at 980 px for a 900 px fold (fr 1440) and 1 050 px for 844 (ar 390), in a `role="alert"` that is there at load — screen readers do not announce it on a new page. 3.3.1 holds to the letter; in use a screen-reader or magnifier user does not learn that the subscription failed (`v2check/newsletter-refused-*.png`). | `templates/news/_newsletter.html` | REVIEW M3's fix: `{% include "components/form_errors.html" with form=newsletter_form %}` at the top of the form, so `main.js` `initFormErrorFocus` focuses and scrolls the summary as on the contact form and the deletion; keep the field's error. Test: an invalid POST renders `#form-errors` inside `#newsletter`. |
| A2 | **major** (older than V5; WCAG 2.2 AA 1.3.5) | **The profile form's personal fields carry no input purpose.** `full_name`, `phone` (typed `text`) and `country_of_residence` render without `autocomplete` on the person's and the company's profile, fr and ar — while the contact, needs, collaboration and newsletter forms, the e-mail page and the password page all carry theirs (`name`, `email`, `tel`, `organization`, `country-name`, `current-password` …). | `apps/accounts/profile_forms.py` `ProfileForm` (unchanged since design-v4; one justified path outside the slice), rendered by `templates/accounts/profile.html` | In `ProfileForm.__init__`, as `SignupForm` does (`forms.py:174`): `full_name` → `autocomplete="name"`; `phone` → `autocomplete="tel"`, `type="tel"`, `inputmode="tel"`; `country_of_residence` → `autocomplete="country-name"`; `preferred_language` → `autocomplete="language"` (optional). Test: the profile renders the three attributes. |
| A3 | minor | **SP-8's 44 px under a coarse pointer is not reached by seven kinds of link** (390, touch, fr and ar): the trail's links, 24 px tall on every page that carries a trail; the glossary register's term links (`dt a`), 24; the password page's «Mot de passe oublié ?», 130 × 17 (ar 22); the profile's «Gérer», 39 × 44 (ar «إدارة» 27 × 45) and «وثائقي» 39 wide; the FAQ answers' links, 40 in French (a 20 px line + 2 × 10); the FAQ permalink, 17 – 22; the consent's privacy link, two 20 px lines. Under a fine pointer, under SP-8's 24 px floor: the FAQ's help line link and the consent's privacy link, 20 px each (both stand alone in their paragraph). WCAG 2.5.8 passes everywhere (24 px, or its inline / spacing exception); the misses are the plan's. | `static/css/v5/_lettura.css` and `_servizio.css`, their `(pointer: coarse)` blocks | Add `.breadcrumbs__item a`, `.glossary-entry__term a`, `.faq-item__permalink`, `.form__privacy-link a` and the password field's help link to the `::after` extension; let it reach 44 from a 20 px line (`inset-block: -12px`) and widen short words (`inset-inline: min(0px, calc((100% - 44px) / 2))`). Fine pointer: `.aiuto a, .form__privacy-link a { display: inline-block; padding-block: 2px; }` (the trail's 24 px recipe). Re-measure the rows' gaps at 390 (no two extensions may overlap). |
| A4 | minor | **«Privacy Policy» is English without `lang="en"`** (3.1.2): hard-coded in the error pages' way-on list (400, 403, 404, 410, 500 — read in the Arabic or French voice) and the h1 of the legal page when no official version is loaded (on the lane: the Arabic page's h1 inherits `ar`). One may read the locked English name as the document's proper name, which 3.1.2 exempts; marking it costs nothing and spares a heading read in the wrong voice. The letterhead footer's «Privacy Policy» / «Cookie Policy» are the same (W2-C1's). E-mail addresses (no language) and the QA company's name (seed data) are exempt; every French or Italian run on the Arabic pages already carries its `lang` and an isolated `ltr`. | `templates/errors/_way_on.html` (l. 14); `templates/legal/document.html` (the title) | `<a … lang="en">Privacy Policy</a>` in the way-on list; on the legal page, `lang="en"` on the h1 when the title is that English name; hand the footer to its owner. |
| P1 | minor (to record at the merge) | **The content page type is over the §2.6 interior CSS figure while the shared payload falls.** gzip −9: `main.css` 42 531 → 41 862 B (−669 B on every page; V5.8's shared payload down — the review's clean merged build: 41 817 → 41 155, −662 B); `cms/lettura.css` 3 718 B on the 25 content templates, `cms/servizio.css` 2 340 B on the 4 service frames. A content page 42 531 → 45 580 B on the branch — 1 094 B over 44 486 B; 44 873 B on the merged tree (+387 B). A service page 44 202 B (43 495 merged), under. JS unchanged (5 requests, same files); requests before `load` 1 + 5 → 2 + 5 = 7, the before set's 7. Measured cost below (n = 10 / 10): LCP pooled +38.5 ms on the content cells, +44.7 ms on the service cells (inside the +50 ms resolution, both intervals spanning 0); the first-render task no worse anywhere. | merge step | Record it in the log as DL54-44, -73 and -76 did (§2.6 item 5 under V5.5's rule) with these figures, or take ≈ 0.4 KB out of `lettura.css` first (REVIEW m11: the interior grammar is restated in `_lettura.css`, `_servizio.css` and W3-F1's `_interior.css`). Not a code finding for the fix step. |

**Observations (not counted):**

- **O1 — the signed-in letterhead shifts at 1440, on both trees** (outside this area). The profile's CLS reached 0.1125
  in 1 of 10 BASE loads and 3 of 10 HEAD loads (p75 0.0234 → 0.1125; over §2.6's 0.10 for a page in those loads): the
  header's menu first lays out on two rows (427, 32, 819 × 128) and settles on one (455, 32, 829 × 64), the lock-up
  dropping 32 px and coming back, the account button moving. The same nodes, rectangles and scores (0.0573 + 0.0552)
  occur on `7d4ce79` — the letterhead's, not this family's markup. For W2-C1 / the W4 performance sweep: reserve the
  menu's one-row box before the fonts arrive (fallback metrics, or a fixed block size).
- **O2 — a ring cut by the viewport's bottom edge.** When the browser scrolls a focused element flush to the bottom
  edge, the ring's bottom 4 px fall outside the window (17 of 4 492 stops; the other three sides and the halo stay).
  Not obscured by content (2.4.11 passes); `scroll-padding-block-end: 8px` in the base sheet would keep it whole — the
  foundation's.
- **O3 — the field's ring against its halo is 2.58 : 1** (3.70 : 1 against the untouched ground): plan §1.6's ring +
  halo as W1-C's A11Y R1 ruled it; unchanged here.
- **O4 — REVIEW M2 is a layout matter only:** the Latin runs on the Arabic glossary, FAQ and Forum carry the right
  `lang` and `dir`, so a screen reader switches voice correctly; only their alignment is at fault.
- **O5 — probe artefacts dismissed with evidence:** textareas «without a name» (the probe skipped `<label>` for
  `textarea`; the accessibility tree names all of them); «hidden target centres» on two-line links (every line fragment
  hits its own link, scrolled into view); the skip link's «weak ring» in forced colours (read mid-slide; at rest it
  stands at 8 px with a 2 px `Highlight` ring); «no error» for the newsletter in the empty-post pass (the form's 3 s
  floor had dropped the post as a bot's — posted after the floor, the error is there: A1).

## Accessibility

**Names, roles, structure.** axe 4.13 (`wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`): 0 violations on 140
page-states; best practices 0; the 702 «incomplete» colour-contrast nodes settled on pixels below. Full accessibility
tree (CDP): every page one h1, no skipped level, one `main`, 0 nameless link, button, field or disclosure. The FAQ's
disclosures are native `<details>`; the password's show / hide control is a 44 × 44 button whose name stays and whose
`aria-pressed` turns `false` → `true`, focus staying on it. Page titles name the page; `html` `lang` / `dir` right on
every page (fr `ltr`, ar `rtl`). The 429 page: 38 stops, 0 weak ring, 0 contrast failure, axe 0, CSP 0.

**Keyboard and focus.** 4 492 Tab stops (fr, ar; 1440, 390), each `:focus-visible` with the 2 px laguna ring at 2 px
(fields add the 5 px halo; the account sections' links draw it inset), **0 stops under the sticky letterhead, the
glossary's letter band or the account sections** in the forward walk; the backward walk (Shift+Tab from the footer
to the skip link, glossary, FAQ, profile, «Vivre en Italie», fr and ar, 1440): 0 covered. The FAQ opens on Enter,
closes on Space, focus going into the open answer; the glossary's letter lands its heading clear of the sticky band (50 px
under it at 1440) and the next Tab is clear; the error page's way back returns to the page before. Ring contrast
3.70 : 1 on stone.

**Forms and errors.** Contact, company needs, collaboration, the deletion, e-mail, password and the forum's join page
sent empty: the system summary (`#form-errors`, `role="alert"`, `tabindex="-1"`) is focused on arrival, its links reach
existing field ids, every invalid field has `aria-invalid` and an `aria-describedby` that reads its message; the French
prescribed labels on the Arabic forms keep `lang="fr"` in the summary and on the labels. Typed text 16 px (the review's
measure). The newsletter: A1. Autocomplete: present on every public form and on the e-mail and password pages; missing
on the profile (A2).

**Contrast on pixels** (the text drawn, then its glyphs made transparent; the dominant ground under each box).
2 338 text boxes, **0 under AA** (4.5 : 1; 3 : 1 at 24 px and over); the lowest is the system's primary, white on
`#12777f` at 15 px, 5.29 : 1. Under 16 px between 4.5 and 7 : 1: the muted marginalia `#4a5a62` on stone (6.46), the
teal links `#0f6a72` (5.69), the primary (5.29) — where DS 2026 asks 4.5 : 1, not 7 : 1; no state word or chip on these
pages falls under 7 : 1.

**Reduced motion is a real still.** Under the setting: 0 animations at load, after 1 s, after a summary, a link, a
primary, a field and two Tabs, and at the end (140 page-states); every component transition 0 s; the only non-zero
ones are the letterhead's portico panels and photographs (80 ms opacity, W2-C1's). Without the setting: 0 running
animations and 0 `will-change` at rest (six pages, 3 s after load).

**Forced colours** (Chromium's emulation; captures in `forced/` and `v2check/`). The account sections' and the news
filter's current mark is drawn in `Highlight` (2 px, `forced-color-adjust: none`) at every width; the FAQ's chevron is
drawn by borders and stays; buttons framed, the danger button dashed; fields and notices framed (the warning's 3 px
edge dashed); the trail's current page is plain text among links; the skip link is a framed box with its ring once its
slide ends. Nothing else opts out.

**Reflow and spacing.** 320 px, fr and ar, 70 page-states: 0 horizontal overflow, 0 clipped text. WCAG 1.4.12's text
spacing at 1440 and 390: 0 overflow, 0 clipping.

**Targets.** Fine pointer: 0 targets under 24 px without an exception (78 inline or spaced: e-mail links in sentences,
the FAQ permalink, two standalone 20 px links — A3). Touch: A3. At the top of each page with the W1-0 tool: 0 under
24 px (the before set had 1 on the Arabic password, second-factor and deletion pages); the only overlapping pairs are the
show / hide buttons inside their password fields, as in the before set.

**Arabic.** 0 Arabic text under 14 px (70 Arabic page-states); French and Italian runs keep their `lang` and an
isolated `ltr`; the unmarked Latin in `main` is e-mail addresses, seed data and «Privacy Policy» (A4). Alignment:
REVIEW M2. CSP: 0 report on every load; console: 0 error but an error page's own status line.

## Performance

**Protocol.** The lane's compressed twin (above), BASE = `7d4ce79` exported to a scratch folder, HEAD = the worktree;
the W1-0 «before» set's own `trace.py`, byte-identical: profile A (150 ms RTT, 1.6 / 0.75 Mbps), CPU × 4, cache off, a
fresh browser profile per load, a click on the h1 and a Tab after 5 s. Nine interleaved blocks (BASE HEAD HEAD BASE
BASE HEAD | HEAD BASE HEAD), the twin restarted on each block's tree, one discarded warm-up per page and language per
block: **n = 10 per cell and tree**, 160 loads, 0 errors. Medians; Δ = HEAD − BASE with a bootstrap 95 % interval
(10 000 resamples). §2.6's resolution: +30 ms for the first-render task, +50 ms for LCP. The machine was shared (45 – 58 %
busy during loads, HEAD's blocks slightly busier).

| Cell | LCP ms BASE → HEAD (Δ, 95 %) | FCP Δ | First-render task | Longest task | CLS median · max | LCP element BASE → HEAD |
|---|---|---|---|---|---|---|
| FAQ fr 1440 | 1 190 → 1 198 (+8, −104 … +128) | +36 | 105 → 95 | 119 → 113 | 0.018 → 0.020 · 0.023 / 0.023 | lead → lead |
| FAQ ar 1440 | 1 360 → 1 438 (+78, −136 … +158) | +8 | 117 → 97 | 168 → 174 | 0.011 → 0.014 · 0.018 / 0.018 | lead → lead |
| FAQ fr 412 | 1 220 → 1 198 (−22, −120 … +162) | +22 | 45 → 51 | 99 → 105 | 0 · 0 | lead → lead |
| FAQ ar 412 | 1 376 → 1 466 (+90, −62 … +226) | +54 | 52 → 65 | 141 → 136 | 0 · 0 | lead → lead |
| 404 fr 1440 | 1 058 → 1 200 (+142, −72 … +194) | +32 | 93 → 100 | 122 → 113 | 0 → 0.013 · 0.022 / 0.023 | the code → the text |
| 404 ar 412 | 1 406 → 1 440 (+34, −180 … +200) | +20 | 55 → 61 | 141 → 167 | 0 · 0 | the text → the h1 |
| profile fr 1440 | 1 304 → 1 262 (−42, −166 … +58) | +16 | 116 → 117 | 170 → 136 | 0.016 → 0.022 · 0.113 / 0.113 (O1) | lead → the page's text |
| profile ar 412 | none recorded → 1 544 | +104 | 80 → 52 | 222 → 206 | 0 · 0 | none → the page's text |

- **Pooled LCP:** the four content cells +38.5 ms (−32 … +108), the service cells +44.7 ms (−71 … +110) — inside §2.6's
  +50 ms. Per cell every interval spans 0; the point estimates above +50 (404 fr 1440, FAQ ar 412 and 1440) go with the
  second render-blocking request and its 2.3 – 3.7 KB on throttled HTTP/1.1 (FCP +8 … +54 on those cells). Every HEAD
  LCP ≤ 1 760 ms (BASE's worst: 3 016), every median ≤ 1 544 ms — about a second under the 2.5 s budget.
- **Long tasks:** the first-render task Δ −28 … +14 ms (inside +30 on every cell); the longest load task lower on five
  cells, +5.6 on two and +25 on one (404 ar 412, inside its spread); tasks over 50 ms during load 4 – 6 on both trees;
  no interaction task over 50 ms. No task beyond those of the load is introduced.
- **LCP element:** text on every page of both trees; it moves from the V4 numeral to the sentence (the 404) and from the
  page header's lead to the account page's own sentence (the profile) — nothing later, nothing an image.
- **CLS:** unchanged by the area (≤ 0.023 outside the letterhead's shift, O1). These are not flagship pages.
- **Loops:** none — in the idle window (2.5 – 4.9 s) the traces carry no animation frame, timer, style or layout work
  on either tree; no running animation, no `will-change` at rest.
- **Bytes and requests:** P1. Against the W1-0 before set (V4): the FAQ page type had 1 sheet (36 294 B) and 6 scripts
  (34 488 B); HEAD has 2 sheets (45 580 B — of which 6.2 KB is V5's `main.css` growth already on the base, 3.0 KB this
  area's page sheet net of its deletions) and 5 scripts — 7 requests before `load` as before; fonts unchanged (Latin 2
  files, 20 956 B; Arabic 3, 53 184 B).

## State left

The lane's server stopped (8784 free); the five minted sessions revoked on `ile_v5_l4`, the secrets file and the
browser profile removed; the Forum Virtuel's flag in its default state (no row); no pytest run (this role changes no
module); no file of the family touched — this report is the one addition. Not done: a real screen reader (the tree,
axe and the interactions stand in), a dark forced-colours palette (every mark uses system colours), HTTP/2 (the
milestone's), the full-text legal page, a sheet and an article (no such content on the lane; the review judged them on
the builder's TEST captures).
