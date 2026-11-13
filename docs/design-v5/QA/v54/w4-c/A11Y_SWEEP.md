# W4-C — Accessibility critical checks: the sweep (w4-c-impl-1, 16 October 2026)

Plan §3.6 item 3 (W4-C), §1.6 (focus), §2.5, WCAG 2.2 AA; the owner's V5.9 §15 («accessibility critical checks») and
V5.10 (the release gates). Tree: `v54-w4-c` = design-v5 at `v54/w4-b` (`dd61b21`: Wave 3 + W4-B's motion audit) plus
this area's fixes (NOTES.md §1). Lane 4: the dev server 8784 from `C:/tmp/ile_wt/v54-w4-c` on `ile_v5_l4`
(`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag). Signed-in pages through sessions
minted with `Client.force_login` on `ile_v5_l4` by a scratch script outside every repository (no password used, typed or
stored; revoked at the end). Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-c/a11y/` (one JSON record and one still per
page × cell); tools: `C:/tmp/ile_v5_council/.work/w4-c/w4-c-impl-1/`.

## What was checked, and how

**Every page type** of `docs/design-v5/live_status.json` «surfaces» (75 keys), by the preview's own registry
(`apps/designpreview/live.py`: each page type by its URL name, a detail page by the census's example), plus what the
preview has no persona for: the organisations' bridge for each organisation account (a company's declaration, an
institution, a university — two lane-only accounts made for this sweep and deleted at the end —, an authorised actor),
the staff's pages (the help desk's queue and its dispatch, the selection's workspace, the operator's «Espace réservé»,
the closed Forum console's 503), the error pages (the 403 and the 410 on their real paths; the 400, the 404 and the 500 through
the DEBUG-only `/_errors/` routes, since a missing path under DEBUG answers Django's technical page), the home with its menu open and a
step of the questionnaire (reached by «Commencer»). **101 pages**, each in **fr and ar** at **1440 × 900** (fine
pointer) and **390 × 844** (touch, mobile), = 404 page views per pass. The personas: the person with a case
(`qa-doc-person`, EE167596D4), the person whose terms are pending (`qa-person`), the person without one
(`qa-fresh-person`), the company (`qa-company`), the bridges (`seed-company`, the institution, the university,
`seed-actor`), the staff (`demo-professionnel`, `demo-operateur`, `demo-acteur-autorise`).

| Pass | Viewports | What it reads |
|---|---|---|
| **desk / phone** | 1440 × 900 · 390 × 844 | **the accessibility tree** (CDP `Accessibility.getFullAXTree`: headings, landmarks, every link / button / image named); **structure** (one h1, one main, banner, contentinfo, the navigations named, no heading level skipped, no image without `alt`, no field without a label); **axe-core 4.13.0** (already on disk, `C:/tmp/ile_v5_council/.work/w1-0-before/axe/`, never installed) — WCAG 2.0–2.2 A/AA and best-practice tags; **the keyboard walk** — real Tab presses from the load: Tab 1 = the skip link (visible? Enter → the focus in `main`?), then round the whole page and its wrap until a stop repeats; at every stop: a visible indicator (W1-0's signature method: outline, shadow, borders, background, colour, decoration of the element or a relative changed), the ring's contrast against what surrounds it (the outline colour composed on the ground behind it), **2.4.11** (the element sampled at 21 points: none entirely under a fixed or sticky layer), the focus never on an element the eye cannot see; **text contrast** — axe on every cell, and the text measured on the rendered pixels (each run against the page drawn again with every glyph transparent) for `main`, the chrome and the foot in French; **non-text contrast** — every field's and drawn checkbox's boundary (border or fill against the ground, ≥ 3 : 1), every icon-only control's glyph; **1.4.12** — the WCAG text-spacing values adopted as a constructed sheet (line height 1.5, letter spacing 0.12 em, word spacing 0.16 em, paragraphs 2 em): the text newly clipped, the text boxes newly overlapping, the page's overflow; **Arabic** text under 14 px; CSP reports and console errors |
| **forced** | 1440 × 900 · 390 × 844, forced colours emulated | the keyboard walk's indicator under the forced palette (the shadow rings vanish there); every element carrying a current / selected / pressed / checked state against a peer without it (outline, borders, decoration, weight, the pseudo-elements, a system-colour background): the state still distinguishable; W3-D's O2 (the rail's current entry) |
| **reflow** | 320 × 256 (= 1280 × 1024 at 400 %) | horizontal overflow (a 2-D scroll, tables apart), clipped text, overlapping text, the share of the viewport the fixed and sticky layers take; a still of the viewport and of the full page |
| **overlays** | 1440 · 390 | every distinct opener on the page — the overlay system's (`data-overlay-open`), popovers, the portico's doors, the disclosure menus, the rail's fold, a tooltip: focus it, Enter → open? focus moved in? (a modal keeps it after a Tab) → Esc → closed? the focus back on its opener and visible? A tooltip: shown on focus, Esc hides it and the focus stays (1.4.13). The shared chrome's openers are probed on the first page of each shell that draws them |
| **errors** | 1440 · 390 | the main forms submitted empty (login, sign-up, password reset, contact, the questionnaire's resume, the company's need, the help desk's request, the upload): the summary announced (`role="alert"`), every invalid field `aria-invalid` and described by its error, where the focus lands |
| **lang** | 1440, ar | WCAG 3.1.2: runs of Latin-script words on the Arabic pages whose nearest `lang` is «ar» |
| **tips** | 1440 | the tooltips under the keyboard: the targa on the home, the rail's entries with the rail folded (Tab to the control → the shared `.tooltip` shows its name → Esc hides it, the focus stays) |

**Cross-engine: not run.** Playwright's WebKit and Firefox binaries are not on this machine (only Chromium under
`%LOCALAPPDATA%/ms-playwright`), and none was downloaded (the standing rule). Every result below is Chromium's
(headless shell 1243). W2-A's O10, W3-C's and W3-D's m6 (the drawer and the sheet, `::details-content`) stay open for
a machine with those engines; Safari and a real device were never available locally. No screen reader was run by a
person: names, roles, states and live regions are read from the accessibility tree and the DOM.

**Reading the harness.** Patterns the probes flag by construction and that are not defects were checked once on a
still and filtered (each named in the findings): the register row's separator point, clipped by design at a line's
start (`_registers.css`); the rail's account name and the phone bar's page title cut with an ellipsis (the rail's word,
the drawer and the page's own h1 carry the whole name); a list row scrolled out of the rail's scrollport; the portico's
current door, marked under forced colours by the architrave in Highlight (a sibling element the state probe does not
read); the skip link read mid-slide; the honeypot field (`aria-hidden`, `tabindex="-1"`); a 4xx / 5xx page's own
status line in the console.

## Verdict

**No WCAG 2.2 AA failure on any page type, in French or in Arabic, at 1440 or at 390 — after the review fixes.** As
first written this line was not true: the sweep's probes do not test 1.3.5 (axe does not flag a missing
`autocomplete`), and «Ma situation» declared no input purpose for the person's date of birth (`bday`) and country of
residence (`country-name`) — every situation page, fr and ar, every width. The senior review found it (REVIEW M1,
confirmed by A11Y_PERF A2) and it is fixed in its owner's file (`apps/accounts/profile_forms.py`, `0858927`): the
review's read of the input purposes on its 396 views at 1366 and 360 found no other form without them. The verdict
covers the 101 pages of the census
(every surface key, the bridges, the staff's pages, the error pages, the open menu and a questionnaire step), each read
by the six passes above: 404 page views per pass (desk + phone: the tree, axe, the keyboard walk, contrast, 1.4.12;
forced colours at both widths; 400 % in both languages; every overlay opener; the forms' errors; Arabic's language of
parts). One robustness defect was fixed in its owner's file (F1), and the Dépôt's zone, drawn late with its keyboard
ring by a dynamic import, was fixed with the performance pass's layout shift (P1) — whose one regression, a silent
picker when `depot.js` does not arrive (REVIEW M2, A11Y_PERF A1), is fixed too (`a3613b3`: the browser's own control,
its file's name with it, until the module is there; A11Y_PERF a1's stale polite line on the way); the policies'
English names carry `lang="en"` where they stand alone (REVIEW m2, `8bd1f1c`). The rest is by design or someone
else's, each said below. The release gate «accessibility critical checks» (V5.9 §15): **PASS** on this tree after
the review fixes (NOTES.md «Review fixes»), Chromium only (limits above).

What the counts say, all page views together:
- **Structure and names.** One h1 on every page; one `main`; a banner and a content-info on every page that draws the
  chrome (the 400 and the 500 are self-sufficient pages, drawn without it on purpose — W3-F2); every navigation named;
  no heading level skipped; axe: **0 violations** of its WCAG 2.0–2.2 A/AA rules and **0** of its best-practice rules
  on the 404 views; the accessibility tree: no unnamed link, button or image; no field without a label (the honeypot is
  `aria-hidden` with `tabindex="-1"`, as `core/forms.py` writes it). axe's «incomplete» items were read: the contrast
  ones are the text on photographs and gradients — measured on the pixels instead (below) —, `aria-valid-attr-value`
  is axe's own uncertainty about `aria-controls` on a closed `aria-haspopup` opener (every target id is in the page),
  and `aria-hidden-focus` is the page behind the open phone sheet, made `aria-hidden` while the overlay system traps the
  focus in the sheet (the walk's 17 stops all stay in it — the W2-A rule: `aria-hidden`, never `inert`).
- **Keyboard.** The walk is the whole page's tab order — every control of the page's primary task reached in order,
  and its own interactions taken from the keyboard (its overlays opened and closed, its form submitted: below). Every
  Tab stop of every page view shows a visible indicator (W1-0's signature method); no stop is
  entirely hidden under a fixed or sticky layer (**2.4.11**: 0 of all stops); no focus lands on an element the eye
  cannot see (the Dépôt's file input is shown focused by its drop zone); the skip link is the first stop, slides into
  view and lands the focus in `main` (the questionnaire's step and the open menu move the focus themselves: the walk
  starts from there); every focus ring with a solid ground holds **≥ 3 : 1** against it — 10 066 rings measured on 11 444 stops, the lowest **3.44 : 1** (`--focus-ring` #1d8a93 on the stone ground #ecebe6); the skip link's own ring is not counted: the dark pill it draws on appearing is its indicator.
- **Overlays.** 19 distinct openers probed in fr and ar at their widths — the portico's doors, the phone sheet, the
  targa's and the rail's tooltips, the rail's fold and language, the console drawer and the account popover on the
  phone, the signed-in letterhead's account menu, the case file's state dialog and its row menus, the help desk's
  closing dialog, the register's state filter (a sheet on the phone), the piece drawer: each **opens, moves the focus
  in** (a dialog to its safe answer, a drawer to its first entry or its title, a menu to its first item; a disclosure
  keeps it on its button, as its pattern does), **closes on Esc and gives the focus back to its opener, visibly**; a
  trapped panel keeps the focus after a Tab; **the tooltips** (the visible twin of an icon-only control's name) show at
  once under the keyboard's focus — the targa at 1440, the rail's entries with the rail folded, fr and ar — and Esc
  hides them with the focus left where it was (1.4.13; `tips/tips-*.json`), while a control whose words are on screen
  (the rail unfolded) shows none, by design; axe inside every open panel: 0 violations. The shared chrome's openers were probed on the first page of each
  shell and are the same on every other page of it.
- **Contrast.** Text: axe 0 failures; on the pixels (French, 1440: `main`, the chrome and the foot; 390: the phone
  bars) the lowest ratio is **5.19 : 1** («Italy», the green of the lock-up's word, on the paper). Non-text: every field's
  and drawn checkbox's boundary ≥ 3 : 1 against its ground; every icon-only control's glyph ≥ 3 : 1.
- **Forced colours** (emulated): every stop keeps an indicator at both widths (W3-D's O2 is fixed — the rail's current
  entry is the underlined word and the Highlight disc, no outline at rest); every current / selected / pressed /
  checked state differs from its peers (the portico's current door by the architrave in Highlight, seen on the stills).
- **400 %** (320 × 256): 0 px of horizontal overflow on every page in both languages; no text clipped but by design
  (below); the fixed and sticky layers take at most **0.28** of the short viewport (the console's bottom bar or the case
  file's action bar, 61–72 px; the public letterhead, sticky, 57 px; the console's top bar scrolls away); the open menu covers the viewport and scrolls.
- **1.4.12.** With the WCAG spacing values, no text newly clipped or overlapping and no overflow but the by-design
  patterns below (and the rail's list, which scrolls under its pinned foot).
- **Errors announced.** Every main form submitted empty answers with its summary (`role="alert"`, the focus on it),
  every invalid field `aria-invalid` and described by its error (`aria-describedby` → the words), in fr and ar at both
  widths; the Dépôt (the upload) answers in place through its live regions with the focus on the field; the questionnaire's
  resume form was the one exception — fixed (F1). **Live regions**: the loader — every waiting control carries
  `aria-busy` (L2, `loader.js`), and the status line of an L1 host is `role="status"` `aria-live="polite"`, present
  empty before the wait and written at 1 s and 10 s (`components/loader.html`; drawn where a page gives it words — the
  login's stage gives none, so its wait is said by the busy control alone, with nothing on screen to announce); the
  toasts are the messages region, `role="status"` `aria-live="polite"` with `role="alert"` on an error (`base.html`;
  server-rendered after a round trip — no script toast exists); the Dépôt's two regions (polite, assertive for a
  refusal); the questionnaire's position (`aria-live`); the register's search count (`role="status"`).
- **Language of parts (Arabic).** The French and Italian runs of the chrome and the authored copy carry their `lang`;
  what the pass finds is either a proper name — the Forum's «Vénétie–Maroc» inside its Arabic label, Italian glossary
  terms quoted in the FAQ («Visto d’ingresso», «Decreto flussi»), a pathway's title quoted in «Formation»'s link — or
  records whose language the page cannot know (people's names, a company's needs, the help desk's messages, the Academy's
  courses, file names: the seed data is French). Exempt under 3.1.2 (proper names, words of indeterminate language);
  the records' language is said by `dir="auto"` where they are drawn. **The policies' English names** («Privacy
  Policy», «Cookie Policy») were unmarked in both footers and the Forum's links (REVIEW m2 — NOTES §4 had answered
  W3-F2's A4 «already fixed», true only of the error pages): they carry `lang="en"` wherever they stand alone
  (`8bd1f1c`); inside a translated sentence («Lire la Privacy Policy», «قراءة Privacy Policy») they are the document's
  proper name, the exception docs/ACCESSIBILITY.md now writes (3.1.2, G-08).

## The matrix — page type × check

One row per page of the census (its persona in brackets). **PASS** = the check passes in all four cells (fr and ar,
1440 and 390; the forced pass at both widths; the 400 % pass in both languages). **overlays**: `PASS (n)` = n distinct
openers probed on this page; `PASS (shell's)` = the page's openers are its shell's, probed on the first page of that
shell (the home's portico and targa, the console's rail, drawer and account menu); `n/a` = none. **skip**: `n/a` where
the page itself moves the focus (the open menu, a questionnaire step). The columns: **structure** (one h1, one main,
landmarks, named navigations, heading order, axe's structural rules) · **names** (axe's name rules, the AX tree, field
labels) · **keyboard** (an indicator at every stop, no focus on something unseen) · **2.4.11** (no stop entirely under a
fixed or sticky layer) · **skip** (first stop, visible, lands in main) · **overlays** (opens, focus in, Esc closes,
focus back) · **contrast** (axe + pixels) · **nontext** (field boundaries, icon glyphs, ring vs ground ≥ 3 : 1) ·
**forced** (indicator and states under forced colours) · **reflow** (400 %: no 2-D scroll, nothing clipped) ·
**spacing** (1.4.12) · **targets** (axe `target-size`, 2.5.8) · **csp** (no CSP report, no console error but a 4xx / 5xx
page's own status line). The records behind each cell: `evidence/v54/w4-c/a11y/<pass>/<page>-<lang>-<w>x<h>.json`
(and `-recheck` where a page was measured again after the probe's correction or after F1).

| Page type (persona) | structure | names | keyboard | 2.4.11 | skip | overlays | contrast | nontext | forced | reflow | spacing | targets | csp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| home (—) | PASS | PASS | PASS | PASS | PASS | PASS (8) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| login (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| signup (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| password-reset (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| password-reset-done (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| email-verification-sent (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| pathways (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| companies (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| institutions (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| universities (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| forum (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| project (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| pilot (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| agami (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| network (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| antifraud (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| orientation (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| orientation-resume (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| pathway-detail (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| diplomas (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| training (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| living (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| living-topic (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| news (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| faq (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| glossary (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| glossary-term (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| partners (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| contact (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| contact-form (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| company-needs (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| institution-proposal (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| university-proposal (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| enquiry-done (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| forum-register (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| privacy (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| cookies (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| notices (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| terms (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| disclaimer (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:dashboard (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (10) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:cases (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:case (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (4) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:documents (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (6) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:documents-app (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:document-requirement (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:document-upload (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:situation (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:requests (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:journey (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:deadlines (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:messages (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:academy (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:academy-course (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:profile (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (2) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:account-email (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:account-password (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:account-mfa (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:account-delete (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-doc-person:logout (qa-doc-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:dashboard (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:case (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (12) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:documents (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (2) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:document-upload (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:situation (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:requests (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:request-detail (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:journey (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:deadlines (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:messages (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:helpdesk (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:helpdesk-detail (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (4) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:helpdesk-new (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:academy-mine (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:academy-enrolment (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-person:profile (qa-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-fresh-person:dashboard (qa-fresh-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-fresh-person:documents (qa-fresh-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-fresh-person:situation (qa-fresh-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-fresh-person:profile (qa-fresh-person) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-company:company (qa-company) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-company:company-profile (qa-company) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-company:company-needs-list (qa-company) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-company:company-need-form (qa-company) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-company:company-analysis (qa-company) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| qa-company:profile (qa-company) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| orientation-step (—) | PASS | PASS | PASS | PASS | n/a (the page moves the focus) | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| error-404 (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| error-400 (—) | PASS | PASS | PASS | PASS | PASS | n/a | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| error-500 (—) | PASS | PASS | PASS | PASS | PASS | n/a | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| navbar-open (—) | PASS | PASS | PASS | PASS | n/a (the page moves the focus) | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| error-410 (—) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| seed-company:org-bridge (seed-company) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| w4c-institution:org-bridge (w4c-institution) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| w4c-university:org-bridge (w4c-university) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| seed-actor:org-bridge (seed-actor) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| helpdesk-queue (demo-professionnel) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| console-unavailable (demo-professionnel) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| helpdesk-dispatch (demo-operateur) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| selection-workspace (demo-acteur-autorise) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| operator-dashboard (demo-operateur) | PASS | PASS | PASS | PASS | PASS | PASS (shell's) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

## Findings

### Fixed (in its owner's file)

| # | Page type · check | What | Fix | Re-check (the same probes) |
|---|---|---|---|---|
| **F1** | orientation-resume · errors announced | The questionnaire's resume form was the one main form whose answer to an invalid submit left the focus on `<body>`: its error was a bare line (`role="alert"` present at load, which a screen reader is not bound to announce after a reload), with no summary and no link to the field — every other form uses the shared summary that `main.js`'s `initFormErrorFocus` focuses after the round trip (WCAG 3.3.1 / 4.1.3 as the project applies them) | `templates/orientation/resume.html` (W3-F1's slice): `components/form_errors.html` in place of the bare line — the summary (`role="alert"`, `tabindex="-1"`, «Le formulaire contient des erreurs.» / «يحتوي النموذج على أخطاء.»), the field's error linked; the field keeps its own inline error and `aria-describedby` (commit `8239d71`) | fr and ar, 1440 and 390: the focus on the summary, its ring visible; 2 alerts (the summary and the field's line), the field `aria-invalid` and described; the page's desk and phone passes unchanged (one h1, 0 axe, every stop indicated, 0 CSP); stills `evidence/v54/w4-c/a11y/errors/orientation-resume-*-recheck.png`; `apps/orientation/tests` + `tests/frontend/test_orientation_w3_f1.py` green (NOTES.md §5) |
| **P1** | document-upload, document-requirement · the performance pass's CLS (PERF.md) | Not an accessibility failure, but it moves the Dépôt's keyboard ring: the zone's enhanced drawing — and its focus ring, `html[data-input="key"] … :focus-within` — waited for `depot.js` (`[data-enhanced]`), so the zone shrank under the fields after it once the module arrived (CLS 0.042–0.071 on the upload page) | `apps/portal/static/portal/v5/_depot.css` (W3-C): keyed on `html.js` (set before the first paint by `head.js`); the waiting frame on `data-sending`, which only the script writes (commit `3ca0b0c`) | the two pages, fr and ar, 1440 and 390, every pass again (`*-recheck`): every stop indicated (the file input shown focused by its zone's ring), 0 axe, forced colours and 400 % unchanged, the empty submit still answered in place with the focus on the field; CLS 0.000 on the twin at n = 9 |
| **M1** (REVIEW; A11Y_PERF A2) | situation (qa-doc-person, qa-person, qa-fresh-person) · 1.3.5 identify input purpose | The form asked for two facts about the person whose purposes WCAG lists and declared neither: the date of birth (`bday`) and the country of residence (`country-name`) — missed by this sweep, whose probes do not test 1.3.5 | `apps/accounts/profile_forms.py` (`SituationForm`; W3-F2's slice is the profile form's, a delegated path): `DateInput(attrs={"type": "date", "autocomplete": "bday"})` and `TextInput(attrs={"autocomplete": "country-name"})`; the nationality has no HTML token (commit `0858927`) | the test beside W3-F2's profile test reads both inputs on `/fr/` and `/ar/espace-reserve/ma-situation/` (red before); the fix pass's smoke, fr and ar, 1440 and 390: `bday` and `country-name` on the inputs, 0 axe, 0 overflow |
| **M2** (REVIEW; A11Y_PERF A1) | document-upload, document-requirement · the core upload task without its module | P1's one regression: `html.js` says a script ran, not that `depot.js` arrived — with the module lost, a chosen file showed nothing (the input transparent over the frame, no row, no name) | `apps/portal/static/portal/v5/_depot.css` (W3-C): until `[data-enhanced]`, a chosen file (`:valid`, the field is required) shows the browser's own control in the frame, its name with it, the frame's words unpainted in their box — no shift; `static/js/src/depot.js`: a file chosen while the module was on its way is taken up when it arrives, and a new choice or a send empties both live regions (A11Y_PERF a1); paid in the page sheet (commit `a3613b3`) | four browser tests (the module aborted, fr 1440 and ar 390; the module held then released; a1), each red before; 20 lane cells blocked and normal, fr and ar, 1440, 390 and forced colours: the zone 76 → 76 / 96 → 96 px, 0 overflow, 0 CSP; CLS 0.000 on the compressed build (NOTES «Review fixes») |
| **m2** (REVIEW) | every page · 3.1.2 language of parts | «Privacy Policy» and «Cookie Policy» unmarked in the public and console footers and the Forum's links | `lang="en"` on the standalone names (W2-C1's footer, W3-A's console footer, W3-F2's join form, W3-F1's privacy note; commit `8bd1f1c`); the embedded runs read as the document's proper name (docs/ACCESSIBILITY.md) | the smoke: every standalone name `lang="en"` on 24 views, fr and ar; the footer, Forum and community tests green |

### Seen, and by design (filtered from the matrix, each checked once on a still)

| Pattern | Occurrences | Why it is not a defect |
|---|---|---|
| The register row's line of facts: a part's leading «·» clipped at a line's start (1.4.12, 400 %) | 45 · 113 | `_registers.css` «the point stands BETWEEN two parts»: each part opens with its point pulled into the gap before it, and the line's box clips the point that would open a line; the words are never clipped (stills `look/needs-spacing-fr-1440.png`) |
| The rail's account name cut with an ellipsis (1.4.12) | 28 | the rail's word beside it shows the name whole on hover and focus (console.js), the drawer wraps it on a second line (`_shell.css` «a name the rail cuts is shown whole by the word beside it»), the profile and «Mon compte» carry it |
| The phone bar's title cut with an ellipsis (1.4.12, 400 %) | 6 · 10 | it echoes the page's own h1 and the trail, which say it whole |
| A rail row overlapping the rail's foot under 1.4.12 | 20 | the row is inside the list's scrollport (`.rail__scroll`, `overflow-y: auto` between the pinned head and foot) and scrolls into view with the focus; the probe's first version read geometry, not the clip (corrected and re-checked) |
| Two skip links overlapping (400 %) | 88 | both sit off-screen, one above the other, until one takes the focus |
| The Arabic phone bar's two-line labels (400 %) | 2 | their line boxes overlap by ≤ 5 px with Vazirmatn's metrics; the glyphs stay apart (still `look`-checked, `reflow/helpdesk-queue-ar-320x256.png`) |
| The portico's current door «not distinguishable» under forced colours | 42 | it is marked by the architrave, a sibling element in `Highlight` with `forced-color-adjust: none` (`chrome.css` §forced colours) — the state probe compares the button's own subtree only (stills: the line under «Institutions») |
| The open phone sheet covering the 400 % viewport | 2 | a modal sheet: it is the screen while it is open, its list scrolls, «Fermer» first |
| No banner / content-info on the 400 and the 500 | 8 | self-sufficient pages (`errors/standalone.html`), drawn without the chrome so that they render when the session or the database cannot be read (W3-F2) |
| A disclosure keeps the focus on its button when it opens | — | the portico's doors and the rail's language are disclosures (WAI-ARIA disclosure pattern); the menus, dialogs, drawers and sheets move it in |

### Observations (not failures; for their owners)

- **«Formation» marks two portico doors `aria-current`** («Personnes» and «Universités & Formation»: the page belongs to
  both); the architrave can sit under one only, so under forced colours one of the two current doors shows no mark.
  Programmatically both are current (1.3.1 holds). For W2-C1 / the steward: one current door per page, if the IA wants it.
- **«Réinitialisation du mot de passe»** titles both the reset page and its «e-mail sent» answer (2.4.2 holds: both are
  about the reset). allauth's copy; not changed.
- **Records in French on the Arabic pages** (the seed data: names, needs, messages, courses, file names, the checklist's
  notes) carry no `lang`: their language is not known to the page (`dir="auto"` is how they are drawn). Where a
  record's language IS known — the ruleset's notes are written in French — a `lang="fr"` on the row would let a
  screen reader switch voice. For W3-C / W3-E, when the content plumbing carries a language.
- **A focused link flush with the viewport's bottom edge loses the bottom 4 px of its ring** (W3-F2 O2, W4-B O1): three
  sides and the halo stay, not a 2.4.7 / 2.4.11 failure. `scroll-padding-block-end` on the root fixes it but adds to
  `main.css`, whose ceiling no merge raises: **for W4-D**, paid by the dead legacy tokens of its sweep (NOTES.md §4).

### For W4-A (its classes of defect — not touched here)

None found failing: at 320 × 256 no page overflows; every 2.5.8 target ≥ 24 px (axe `target-size`: 0); the Arabic
stills looked at here (the phone bar, the open menu, the resume form, forced colours) read right to left. The one tight spot is the Arabic phone bar's two-line labels
at 320 px (line boxes 5 px into each other, glyphs apart) — W4-A's phone chrome, if it wants more air.
