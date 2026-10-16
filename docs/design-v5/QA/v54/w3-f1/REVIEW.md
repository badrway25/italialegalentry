# W3-F1 · The doors, the project pages and orientation — senior review (one pass)

Reviewer label `w3-f1-review` (built nothing). V5.5 delivery mode: one review, then fix, then ship. Branch `v54-w3-f1`
at `f9af825` (step 1 + step 2 and their notes). Looked at on the reviewer's own server from this worktree
(127.0.0.1:8887, `ile_v5_l7`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag),
headless Chromium with its own profile (`.profiles/w3-f1-review/`), one browser and one pytest at a time; no run ended
on a crash; the server is stopped. One authenticated check — «Ma situation», which lost `v4/wizard.css` to this area —
through sessions minted with `Client.force_login` (no password used, typed or stored), revoked at the end. Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w3-f1/review/` (`fr/`, `ar/` full pages by width, `wizard/`, `panel/`,
`situation/`, `metrics_*.json`, `action_positions.json`, `wordbreaks.json`).

**Looked at:** the seven doors — /parcours/ (+ two sheets), /entreprises/, /institutions/, /universites-et-formation/,
/forum/ (+ /forum/inscription/), /le-projet/, /projet-pilote/ — and orientation (/orientation/, a step, a refused
answer, the pre-evaluation, /orientation/reprendre/), /diplomes-et-titres/, /formation/, /attention-aux-fraudes/,
/agami/, /reseau/, /contact/; the home and the open portico panel as the reference. fr and ar × 1440 × 900,
1366 × 768, 390 × 844, 360 × 800 (144 full pages), + 1280 and 1024 for the doors and the advice pages (48), + a
mid-word-break sweep (18 pages × 9 widths from 320 to 1440 × fr, ar). The questionnaire driven end to end in fr and
ar, by mouse and by keyboard. `tests/compliance` once on `test_ile_v5_l7`: **59 passed**. Every `data-locked`
element of the 32 pages compared with the registry: 10 / 10 identical; 53 locked keys of the area's families found
verbatim on its pages.

## Verdict: **SHIP_AFTER_FIXES**

**The question — the same premium product as the hero and «Il portico», or V4 pages inside a V5 frame?** Not V4 any
more. The side columns, the sticky section bars, the CTA bands, the card grids and the growth-curve illustration are
gone, and every page speaks one grammar: the entrance at the reading edge, chapters with the home's section device,
registers on hairlines, «la linea» for real sequences, the stone for the one action. Type, colour, corners
(4 · 6 · full) and icons (≤ 5 in a body) are the system's; Arabic mirrors correctly; nothing overflows from 320 to
1440; the compliance texts are byte-identical. It reads as a calm, credible institutional site.

It does not yet read as the *same premium product*. The step down from the hero and the portico is sharp: open
«Personnes» and the panel shows a warm photograph with the audience's disc; click through and the page's lead is a
dark slab with three grey blocks — «la porta» — the same slab on four doors, told apart by a 20 px glyph and a 3 px
line. Below it, the 17 pages carry no image at all and four doors run 2 to 6 screens with nothing drawn. And the one
action is never in the first viewport of a door (only /universites-et-formation/ at desktop widths), nor on the
questionnaire's own start page. All of it is fixable now with what the repository holds: five majors, then polish.

No P0: no broken page, no wrong direction, nothing unusable, no data or security problem.

## The gate, checked on the real pages

| Gate item | Result |
|---|---|
| D26 slots | one inset a page (the page's notice or the anti-fraud callout); one action (one primary; the Forum and the pilot keep one secondary); «who can help me» from live text («Besoin d'aide ? Écrivez-nous :» + the address) on the doors, the sheets and the advice pages; the authority's host beside its link (slot built — no authority in the data has a URL yet); caption + credit under every photograph (no photograph is drawn) |
| Headings verbatim | the locked titles verbatim; chapter heads are existing catalogue strings (translated in ar); the reader's questions proposed for B1, not written |
| RH-3 — a picture or a drawn figure every second screen of a door | **not met** on /parcours/ (2.25 / 4.01 screens at 1440 / 390), /entreprises/ (3.47 / 4.20), /forum/ (3.97 / 6.04) and /le-projet/ on phones (2.74) — the builder's measure, confirmed by eye → M2 |
| RH-6 — the page as a chain of questions | yes on every page (what is this space → which ways → how → where else, who can help) |
| One action a page | yes — but where it sits: M1, M4 (`action_positions.json`) |
| Imagery O54 / O55; no frame from the panel or the hero entrance of the same audience; none twice | met, trivially: no photograph on any page of the area. The only audience frames in the repository are the panel's and the hero's (`static/img/portico/`, `static/img/photos/hero/`), so the builder's reading is right; what stands in for them is the problem (M1) |
| ≤ 3 corners a screen | 4 · 6 · full on every page and width, fr and ar |
| ≤ 6 icons in the editorial body | 5 at most (/reseau/'s actors), 0–4 elsewhere, identity marks apart |
| The wizard | one act («Continuer», 52 px, first in the DOM); typed text 16 px everywhere (the resume field and the companies' fields 52 px high); plates 58 px around 24 px controls; a refusal said in words + a mark + doubled edges, `aria-invalid`, `aria-describedby`, `role="alert"` — never colour alone; keyboard: start → the focus on the question, Tab → «Pourquoi cette question ?» → the first choice, arrows choose, Enter submits, the next question takes the focus, the ring on the plate; reduced motion 0 s. **But** the percentage stays → M3 |
| Compliance | byte-identical (above); the programme's first item split on its own «—» (CD law 8) |
| Health | 0 horizontal overflow, 0 CSP report, 0 console error, 0 response ≥ 400 in the lane's log, on every load |
| RTL | a true mirror — heads at the reading edge, stations 01 → 08 right to left, registers in RTL order, the stair unmirrored; one collision → m2 |
| Performance (V5.5: real regressions only) | nothing to fix — no image request, text LCP, nothing moves at load; two page types over their Wave-1 CSS ceiling by 0.5 and 1.0 KB gzip (the Forum, orientation), recorded by the builder for the steward |

## Blocking

None.

## Major — fix before the merge

**M1 · «la porta» reads as a missing picture, and a door's first screen does nothing.** On /parcours/, /entreprises/,
/institutions/ and /universites-et-formation/ the entrance's end seat is a 4:3 night slab (≈ 400 × 300 at 1440; a
120–144 px strip on phones) holding three flat blocks and a 36 px disc. Under the open portico panel — the same card
with a real photograph — it reads as that card with its image failed. Its three steps are «il gradino»'s sign (CD §1.3
signature 6, the anti-fraud component) and the hero's stair: drawn here, they say nothing about the audience.
Meanwhile the door's one action sits at 1.8 / 2.2 / 3.3 / 3.7 screens on /parcours/ (1440 / 1366 / 390 / 360) and at
3.6–5.1 on /entreprises/, where the settled landing rule is «primary within 560 px at 360 × 800» and the door card
carries the space's first tasks (CD §10). **Fix (one direction):** the plate keeps its night, its disc and its accent
rule and carries the door's way in instead of the stair — the page's one action moved up into it (persons: the
questionnaire's action card; institutions and universities: their prescribed button and its one sentence) and, on
/entreprises/, the jump to «Recueil des besoins» (the form's submit stays the one action). The stair leaves. A curated,
captioned frame still takes the seat the day it exists (D26); the way in then moves under the lead.

**M2 · RH-3 is a gate of this family and fails on four doors; it is deferred, neither met nor waived.** Fix with what
the copy already gives. On /parcours/, draw «Comment ça marche» on «la linea» — the locked text split verbatim on its
own «→» (CD law 8; CD §20 / D-U4 give the home this rendering of the same locked text), four stations beside the
action's reason — instead of a run-on paragraph with arrows. On /entreprises/ the stretch is the 14-field form, a task rather than reading: set the six short
single-line fields two-up from 64rem (≈ 300 px shorter) and record the form region as outside RH-3 in DL54. On /forum/
(prescribed prose, no Forum frame in the repository) and /le-projet/ on phones, write the CD's waiver into DL54 with
the condition that lifts it (curated, captioned frames, §1.16), so that the gate says what it is.

**M3 · The questionnaire still shows a percentage** — «Question 1 · 0 %», «Question 2 · 35 %», «Question 3 · 65 %»
(Arabic: «% 0 · السؤال 1»). FM12 (DESIGN_SYSTEM_V5 §11, CD §20, RED_TEAM B4 «resolved»): «Question n sur N» in words,
no %, tested. On an adaptive questionnaire the figure jumps, and it opens at 0. **Fix:** show the words the bar
already speaks — «Question {{ n }} sur {{ m }} au maximum», in the catalogue in it / en / ar — drop the visible %, keep
the quiet line, and add FM12's test (no «%» in a rendered step).

**M4 · The questionnaire's start page hides «Commencer».** The hero's primary leads to /orientation/, where
«Commencer» is under the first viewport at every width: its top at 1 152 px at 1440 × 900, 1 200 at 1366 × 768,
1 512 at 390 × 844, 1 644 at 360 × 800 — after the lead, the three stations and the notice. **Fix:** from 64rem the
action card takes the entrance's end seat (empty on this page); on phones the action follows the lead, «À lire avant
de commencer» kept before it in reading order (as the card's note or just above it), the three stations after it.

**M5 · «ACCOMPAGNEMENT» breaks mid-word on /projet-pilote/ at 1280 and 1366** («ACCOMPAGNEMEN / T», fr and ar): eight
stations a row from 80rem leave ≈ 125 px for a 13 px tracked capital word (`wordbreaks.json` — the only mid-word break
of the area from 320 to 1440). **Fix:** eight a row from 90rem, four a row below it (or let the label hyphenate under
its `lang="fr"`).

## Minor — polish

- **m1** The Forum's programme puts «15h00» in the numeral column of its first row and 02–08 under it: the list seems
  to start at 02. CD §20: a time column only when every row has a time — number 01–08 and keep the first row's locked
  words whole («15h00 — Accueil et enregistrement»).
- **m2** The Arabic door card: the stair and the disc collide at the inline start (the stair's own `direction: ltr`
  resolves its `inset-inline-end` to the right, where its comment wants the other end). Moot if M1 removes the stair.
- **m3** The Forum's index at ≤ 390: two links share a line with no separator («QU'EST-CE QUE LE FORUM  OBJECTIFS») and
  read as one; one link a row, as on desktop.
- **m4** «Destinataires» on /institutions/: fragments of the locked sentence stand as register rows with mixed initials
  («Régions» · «organismes publics» · «Chambres de Commerce» …) and read as typos in a list. Show the verbatim sentence
  (visually hidden today) as the body; keep registers for real lists.
- **m5** A questionnaire step at 1440 × 900 and 1366 × 768: on question 1 «Continuer» falls under the fold (top at
  920 px), because the page's title and its sentence repeat above every question. Compress the step's head (the
  sentence once, on the start page).
- **m6** French on Arabic pages without `lang="fr"` (WCAG 3.1.2): on /ar/forum/ the eyebrow «Espace permanent de
  dialogue et de coopération» and the h1 «FORUM PERMANENT VÉNÉTIE–MAROC»; on /ar/agami/ the h2 «Qui est derrière Italy
  Legal Entry ?» (a locked FAQ question; `title_lang` is not passed to the chapter head).
- **m7** Arabic: a French lead of seven to eleven lines is end-aligned in the entrance (ragged on the left —
  /ar/parcours/ 7 lines at 1440, 11 at 390; /ar/projet-pilote/). Keep end alignment for heads; a French lead longer
  than two lines keeps its own start, as the bodies do. The home does the same (W2-D's): one rule for both, through the
  steward.
- **m8** (chrome — hand on to W2-C1 / W2-C2) The portico marks two places current: «Institutions» and «Forum
  Vénétie–Maroc» on /forum/ (yet only the Forum on /forum/inscription/), «Personnes» and «Universités & Formation» on
  /formation/ — `cms_nav._mark_current` makes a door current whenever one of its children matches.

## What holds — keep it through the fixes

- One grammar for the whole interior, and no V4 left on these pages (side columns, sticky bars, CTA bands, card grids,
  the two-glyph metadata rows).
- The pilot's eight stations on «la linea» instead of a growth curve ending on a gold node: honest, and one diagram
  language with the home.
- The Arabic composition (the heads, the stations, the registers, the quotation's rule on the French quotation's own
  side, the forms' fields and labels).
- The questionnaire's plates, its refusal and its keyboard model; typed text at 16 px on every form.
- «Ma situation» after `v4/wizard.css` became `v5/_wizard.css`: 4 · 8 · full, one primary at rest, the date field at
  16 px, no overflow, fr and ar × 1440 and 390.
- The compliance texts, byte for byte; the anti-fraud callout and the pilot's notice said in words, never by colour.

## Other areas, seen on the way

- «Ma situation» (W3-E's markup, W3-D's script): the save button is rendered `btn--primary` and `situation.js` turns it
  secondary after load, so the desktop's first second shows two primaries and the slab's transition animates the
  change. Render it secondary on the server (or hold the transition until the script is ready).
- The portico's double current marker (m8).

## Runs

| Run | Result |
|---|---|
| `tests/compliance -m "not browser"` on `test_ile_v5_l7` | 59 passed (151 s) |
| Captures: 18 pages × fr, ar × 1440, 1366, 390, 360; 12 pages × fr, ar × 1280, 1024 (`capture.py`) | 192 loads: 0 overflow, 0 CSP, 0 console error |
| Mid-word breaks: 18 pages × fr, ar × 1440, 1366, 1280, 1024, 768, 430, 390, 360, 320 (`wordbreak.py`) | one word: «ACCOMPAGNEMENT» on /projet-pilote/ at 1280 and 1366 (M5) |
| The questionnaire, fr and ar: start, step, refusal, steps, the pre-evaluation × 1440, 390, 360; a keyboard-only walk | as in the gate table; M3, M4, m5 |
| The one action's position: 10 pages × 1440, 1366, 390, 360 (`action_positions.json`) | M1, M4 |
| Locked texts: the `data-locked` elements and the registry's keys against the rendered pages | 10 / 10 identical; 53 keys verbatim |
| «Ma situation», fr and ar × 1440, 390 (a minted session, revoked: 3 sessions deleted) | 4 · 8 · full, one primary, 16 px, 0 overflow |

The scratch scripts are in `C:/tmp/ile_v5_council/.work/w3-f1/w3-f1-review/`.
