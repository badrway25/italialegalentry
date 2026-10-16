# W3-F1 · The doors, the project pages and orientation — accessibility + performance check (one pass)

Label `w3-f1-a11y-perf`, 11 October 2026: the area's one accessibility/performance check (V5.5: implement → review
once → fix → ship). This role built nothing and changed nothing in the area's code. Checked branch `v54-w3-f1` at
`f9af825` (steps 1 and 2 with their notes). `b33e5d7`, committed above it during the check, adds only the senior
review's `REVIEW.md`. Merge base with `design-v5`: `38f78d4`. design-v5 has since moved to `0a8299d`, the W3-B merge.

**Lane.** Lane 7, port 8787. The area's other roles had stopped it, and this role stopped it again at the end.
- **Accessibility:** the dev server from `C:/tmp/ile_wt/v54-w3-f1`, with `ile_v5_l7`, `ILE_REFERENCE_DATE=2026-10-03`,
  `DB_CONN_MAX_AGE=0`, `--noreload` and no preview flag.
- **Performance, same port:** the merge base (an export of `38f78d4` in this role's scratch folder) and the worktree,
  served in turn:
  - on the dev server, for the weights, the CLS sweep and the at-rest sweep;
  - as the compressed twin, for the traced loads. The twin has the plan's 8782 shape: DEBUG off,
    `CompressedManifestStaticFilesStorage`, hashed URLs, gzip on the wire, and `collectstatic` into a scratch root per
    tree. Its settings file lives outside every repository (W3-B's check's file, re-pointed to `ile_v5_l7`).
- **Signed-in page:** «Ma situation» was reached through one session minted with `Client.force_login` on `ile_v5_l7`
  (`qa-doc-person`). No password was used, typed or stored. The session was revoked at the end.
- **The questionnaire:** its states were reached by driving it. The check created 21 anonymous sessions on the lane
  clone, with no personal data. They were left in place, as W1-0's set left its own.
- **Browser:** headless Playwright Chromium (HeadlessChrome 153) with its own profile under
  `C:/tmp/ile_v5_council/.profiles/w3-f1-a11y-perf/`. One browser and no pytest ran at a time. Every series waited on
  `PERFORMANCE_BENCHMARK_LOCK`, which was never present and never created. **No run crashed.** Ports 8780, 8782, 9222
  and 9223 were never used.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-f1/a11y-perf/`:
- `desk/` and `phone/`: one JSON per state, with a still, holding the keyboard walk, the pixel contrast, the hit areas,
  the accessibility tree, axe, the language of parts and the heading outline;
- `reflow/`, `spacing/`, `reduce/`, `forced/`;
- `base-check/`: the merge base, for the targets and the home's rings;
- `extra.json` (the skip link, form controls, sticky heads, the coarse pointer, 200 % text), `backwalk.json`,
  `bidi.json`, `rest.json`, `cls-quick-base.json`;
- `bytes-head.json` and `bytes-base.json`;
- `twin/twin-ab/` and `twin/twin-abba/`: the runs, the first trace of each cell and tree, and `summary.json`;
- `variants-*.json`: untraced loads.

Probes: `C:/tmp/ile_v5_council/.work/w3-f1/w3-f1-a11y-perf/`. These are W3-B's check's probes, read and kept, pointed at
this area. Three in-page probes were added (language of parts, aria-hidden focusables, the DOM heading outline), plus
the questionnaire's flow.

## Verdict: SHIP_AFTER_FIXES

0 blocking · 1 major · 2 minor.

**The major** is the area's own and small. The interior's trail and its forward links are 20 px tall, where the merge
base drew them at 24–28 px. This is under SP-8's 24 px floor, which is part of the gate's Accessibility PASS (§3.1
item 8), on every page of the area. WCAG 2.5.8 still holds through its spacing exception. The fix is one rule in
`_interior.css`.

**Otherwise no WCAG 2.2 AA failure was introduced by the area.** This covers its 23 states in fr and ar, at 1440, at
390 (touch) and at 320, with reduced motion, forced colours, text spacing and 200 % text. The keyboard walk, focus
visibility, focus never obscured, pixel contrast, names and roles, reflow and reduced motion are all clean. Two
older gaps remain where French appears on Arabic pages:
- the Forum's eyebrow and h1 carry no `lang` (3.1.2);
- /ar/agami/'s French FAQ is tagged on its section but is drawn right to left.

**No performance regression.**
- **JS:** unchanged everywhere except the questionnaire's steps (+555 B, `wizard.js`).
- **CSS:** −2.0 KB on the home and −2.3 KB on the institutional pages. +2.0 KB and one more render-blocking request on
  the persons pages, which are now at the interior's ceiling. +1.7 KB on the orientation pages and +0.4 KB on the
  Forum, both over the ceiling (finding 3, to record).
- **On the production-shaped twin:**
  - LCP 1.18–1.81 s on every cell (≤ 2.5 s), always a text block or the home's image;
  - the first-render task within +14 ms of the merge base;
  - CLS ≤ 0.024, the portico's own shift, which the merge base shows too.
- **Nothing moves or loops at rest.**
- **The person door's slower LCP in the first traced series did not survive** tighter interleaving or untraced loads:
  1 108 ms at HEAD against 1 124 ms at the base, n = 12 each.

## What was measured

23 states × fr / ar:

| Key | Page | What it shows |
|---|---|---|
| PAR | `/parcours/` | the person door: the entrance with «la porta», the eight pathways as a register, «Comment ça marche» and the action, the anti-fraud callout |
| SAL | `/parcours/salaried_work/` | a pathway sheet: «Sommaire de la page» in the entrance, the steps on «la linea», four «en attente» blocks, «Termes utiles» |
| ENT | `/entreprises/` | the company door: the three moments, the needs form on the stone, the transparency notice |
| INS · UNI | `/institutions/` · `/universites-et-formation/` | the doors: the recipients as a register of words, the action card |
| FOR · FRG · FRD | `/forum/` · `inscription/` · `inscription/confirmation/` | the night entrance with its index, the sections as chapters (registrations closed) |
| PRJ · AGA · NET · CON · FRA | `/le-projet/` · `/agami/` · `/reseau/` · `/contact/` · `/attention-aux-fraudes/` | the institutional base |
| PIL | `/projet-pilote/` | the eight stations across the column |
| ORI · RSM | `/orientation/` · `/orientation/reprendre/` | the questionnaire's first page; the resume field |
| STEP · ERR · RESULT | a step reached by «Commencer» · the server's refusal · the pre-evaluation | driven through the questionnaire itself |
| DIP · TRA | `/diplomes-et-titres/` · `/formation/` | the advice pages |
| SIT | `/espace-reserve/ma-situation/` | «Ma situation»: `v4/wizard.css` → `v5/_wizard.css` (the area's CSS on W3-E's markup) |
| HOM | `/` | the home (W2-D's), whose `pages.css` this area split: checked for regression only |

**Passes:**
- 1440 × 900 with a fine pointer, and 390 × 844 with phone emulation and touch. Each covers the keyboard walk, pixel
  contrast, hit areas, the accessibility tree, axe-core 4.13.0 (W1-0's copy) on `wcag2a/2aa/21a/21aa/22aa` and
  `best-practice`, and W1-0's `health.js`.
- 320 × 640 reflow.
- WCAG 1.4.12 text spacing at 1440 and 390.
- Reduced motion (`emulateMedia`) and forced colours (Chromium's emulation) at 1440 and 390.
- Beside these:
  - a backward keyboard walk on six long pages;
  - a bidi probe on every Arabic state;
  - 200 % text at 1280;
  - the skip link, the form controls and the sticky chapter heads.

**414 recorded pass loads: 0 CSP reports, 0 console errors, every response 200.**

**How the probes read pixels.**
- **The keyboard walk** clips every stop while it is focused, then takes the same clip at the same scroll with nothing
  focused. The indicator is the pixels that changed. Ring fill is the changed pixels in a 6 px band round the box,
  divided by a 2 px perimeter. Change contrast is the median ratio between each changed pixel's two colours.
- **Contrast:** every text run of `<main>` that is fully in view and under no fixed layer. Its computed colour, with
  its opacity chain, is measured against the pixels under it, with the page re-drawn with every glyph transparent. The
  report uses the dominant pixel and the worst pixel that covers ≥ 5 % of the run.
- **Hit areas:** `elementFromPoint`, probed outward from each target's centre, so a pseudo-element's extension counts.

## Accessibility

| Check | Result |
|---|---|
| axe 2.0–2.2 A/AA | **0 violations** on 92 loads (1440 and 390); best-practice 0. «Incomplete»: color-contrast only, decided on pixels below. On «Ma situation» at 390 the console bar's `aria-controls` is incomplete too (W3-A's chrome) |
| Keyboard, fr and ar | Skip link → language bar → the portico → the trail → the index (where there is one) → the body in DOM order → the action → «who can help me» → footer. **3 062 stops** at 1440 and 390: every one `:focus-visible`, every one named in the accessibility tree |
| The questionnaire's keyboard model | «Commencer» puts the focus on the question (programmatic, out of the tab order, no ring by design). Tab then reaches «Pourquoi cette question ?», then the radio group (arrows choose), «Continuer», «Précédent». The browser's own refusal of an empty answer focuses the first choice with its message. The server's refusal puts the focus on the question again, with the message in `role="alert"` and the group `aria-describedby` it and `aria-invalid` |
| Focus visible | **Rings:**<br>• laguna-550, 2 px at a 2 px offset: change contrast 3.70–4.11 on the papers, 3.44 on the stone;<br>• laguna-400 on night (the Forum's entrance and the chrome): 9.66–10.69;<br>• text fields add the 5 px halo; the ring itself is the 3.44–3.73 figure.<br>**Ring fill** ≥ 0.6 of a 2 px perimeter on 3 041 / 3 062 stops. The 21 below:<br>• 12 stops that Tab scrolls flush with the viewport's bottom edge, so the ring's lower edge is cut while the control stays in view (O1);<br>• the questionnaire's radio ×8, whose ring is drawn on its plate: measured on the plate, fill 1.02–1.03 at 3.70 : 1, at 1440 and 390;<br>• one wrapped inline link, whose ring is drawn per line box |
| Focus not obscured (2.4.11) | **0 stops** under the sticky header, forward (3 062 stops) and backward (888 stops: six long pages × fr, ar × 1440, 390). The sticky chapter heads from 75rem (up to 8 a page) never cover a link or a control of the body: 8 scroll positions × 38 page loads. The skip link rests at top 8 px after its 120 ms entrance; Enter moves the focus to `main#main-content`; the next Tab reaches the trail |
| Contrast on pixels | **2 502 text runs, 0 below AA**, also against the worst pixel.<br>**State words and notice titles ≥ 7.66 : 1**, so COLOUR §10's AAA rule holds:<br>• «À lire avant de commencer», «Les inscriptions sont closes.» and the pre-evaluation's banner: 7.66;<br>• the anti-fraud titles, «Votre protection» and «Votre code de reprise»: 7.70;<br>• the refusal: 9.26;<br>• the «Termes utiles» tags: 16.2.<br>**Text under 16 px between 4.5 and 7 : 1** is W1-A's tokens as designed. None of it is a state word or a notice title, so no rule of the system asks 7 : 1 of it:<br>• text-2 at 13–15 px: 6.0–6.5;<br>• laguna-700 links: 5.2–6.3;<br>• white on the primary at 15 px: 5.29;<br>• text-3 metadata labels: 5.5.<br>No Latin text under 12 px, no Arabic under 14 px |
| Names, roles, structure | 0 nameless controls (CDP accessibility tree).<br>One h1 per state; the heading outline steps without a gap (DOM order).<br>One region per chapter, named by its h2; «Sommaire de la page» a named navigation; the anti-fraud callout a named complementary.<br>The progress bar is a `progressbar` named «Question n · p %», with `aria-valuetext`.<br>The door card is `aria-hidden` with nothing focusable inside; 0 aria-hidden focusables on any state |
| Language and direction (Arabic) | Prescribed French on the Arabic pages carries `lang="fr"`: heads, leads, register titles, the index, stations, the Italian terms (`lang="it"`).<br>The heads end on the reading edge; the stair does not mirror.<br>Two gaps, both older than the area (finding 2): the Forum's eyebrow and h1, and /ar/agami/'s FAQ section |
| Targets | **WCAG 2.5.8:** 0 targets under 24 px without the spacing or inline exception (3 022 targets).<br>**SP-8:** finding 1.<br>**Under a coarse pointer:** the plates are 58–82 px and the whole plate is the target (corners and bottom hit the label); the native control is 24 px; «Pourquoi cette question ?» 44; «Continuer» 52 (full width); fields 52; the action buttons 52 |
| Forms (the gate's 16 px) | Typed text **16 px** in every field of the area: the needs form's 14 fields and the resume field, 52 px high. `autocomplete` on the needs form's identity fields: organization, address-level2, name, email, tel. The honeypot is off-screen with `tabindex="-1"` |
| Reduced motion: a real still | **0 animations** at load and at 1 s, and 0 after the help toggle, a choice, hovers and two Tabs (92 loads, 1440 and 390). Every transition computes to 0 s: links, buttons, plates, the help chevron, chips. With motion on: nothing moves at load on the area's pages; at rest see Performance |
| Forced colours | The door card and its disc keep a 1 px CanvasText edge. The stations' rings and line are drawn in CanvasText. The progress keeps its track (GrayText, `forced-color-adjust: none`) and its fill (CanvasText). The chosen plate carries a 2 px Highlight outline (O5). Focus rings are drawn in Highlight, change contrast 11.3–15.1. **3 058 stops**, all `:focus-visible`; the stills are in `forced/*.png`. «Ma situation»'s rail current entry is W3-A's (O4) |
| Reflow 320 × 640 | 0 overflow, 0 clipped text, 46 / 46 |
| Text spacing (1.4.12) | 0 overflow and nothing clipped on the area's pages (92 loads). The only ellipsis is the rail's account name on «Ma situation» (W3-A's), which was clipped before the spacing too |
| 200 % text (1280, root size doubled) | 0 overflow on 38 page loads. The utility bar's identity line is clipped (W2-C1's, O3) |
| Against W1-0's «before» set (V4), the same `health.js` | Overflow 0, clipped 0, focus missing 0, CSP 0, console 0.<br>axe contrast failures 4 → 0: the Forum registration's eyebrow, fixed.<br>Targets under 24 px rose from 0 to 1–5 per page (finding 1).<br>«Overlapping targets» rose only because of where the walk stopped: the sticky header lies over content scrolled under it, not a collision |

## Performance

**Weight.** `gzip -9 -n` (GNU) of the committed bundles, the steward's method. The interior's ceiling is 44 486 B
(DL54-44: the Wave-1 ceiling for door and interior page types).

| Page type | W1-0 «before» (V4) | merge base `38f78d4` | `v54-w3-f1` | W3-F1's delta | vs 44 486 |
|---|---|---|---|---|---|
| persons: `/parcours/`, the sheets, `/diplomes-et-titres/`, `/formation/` | 36 294 · 1 sheet | 42 463 · 1 sheet | 44 464 · 2 sheets | **+2 001**, one CSS request more | 22 under |
| ecosystem: `/entreprises/`, `/institutions/`, `/universites-et-formation/`, `/projet-pilote/` | 38 226 | 44 395 | 44 362 | −33 | under |
| Forum: index, inscription, confirmation | 38 441 | 44 610 | 44 970 | +360 | **484 over** |
| institutional: `/le-projet/`, `/agami/`, `/reseau/`, `/contact/`, `/attention-aux-fraudes/` | 39 114 | 46 546 | 44 244 | **−2 302** | under (the base was 2 060 over) |
| orientation: first page, steps, pre-evaluation, `/reprendre/` | 37 626 | 43 795 | 45 513 | +1 718 | **1 027 over** |
| the home | 39 114 | 57 114 | 55 122 | −1 992 | its own 59 137: under |
| console: «Ma situation» | 41 668 | 50 018 | 49 954 | −64 | under DL54-87's 50 927 |
| `dist/main.css` | 36 294 | 42 463 | **41 203** | −1 260 | the 45 KB cap holds |
| JS | 6 scripts · 34 488 | 3 scripts · 7 618 | 3 scripts · 7 618 | **0**, except `wizard.js` 493 → 1 048 B (+555) on the questionnaire's steps and pre-evaluation | |

**On the wire (the twin):**
- **CSS requests before load:** the persons pages 1 → 2, the others unchanged.
- **CSS + JS requests before load** on the person door: 2 + 5 = 7, V4's count (1 + 6).
- **Fonts:** 2 requests / 20.9 KB in French (budget ≤ 25 KB) and 3 / 53.2 KB in Arabic (≤ 56 KB).
- **Images:** none above the fold. The door card is CSS and makes no image request.
- **After the merge:** design-v5's `main.css` is already 646 B lighter than this branch's base (W3-B). That brings the
  Forum to ≈ 44 324 (under) and orientation to ≈ 44 867 (≈ 381 over). The merge step's rebuild gives the figure.

**On the twin, BASE / HEAD, W1-0's protocol.** The twin's tools are W1-0's `trace.py`, byte-identical: profile A
(150 ms RTT, 1.6 / 0.75 Mbps), CPU ×4, cache off, a fresh profile per load, a click on the h1 and a Tab after the
rest. Each server start is followed by one discarded warm-up a cell. Series 1 ran blocks BASE·HEAD | HEAD·BASE, n = 8
a cell and tree. Medians with ranges:

| Cell | LCP BASE → HEAD (ms) | first-render task | longest load task | CLS max BASE / HEAD | LCP element BASE → HEAD |
|---|---|---|---|---|---|
| door-persons fr 1440 | 1158 [1044–1192] → 1294 [1056–1484] | 97 → 108 | 130 → 152 | 0.020 / 0.023 | `p.page-header__lead` → `p.ingresso__lead` |
| door-persons ar 412 | 1376 → 1410 | 50 → 59 | 161 → 208 | 0 / 0 | the same |
| pathway-detail fr 412 | 1246 → 1256 | 49 → 46 | 152 → 135 | 0 / 0 | the same |
| door-forum fr 1440 | 1298 → 1318 | 104 → 118 | 183 → 170 | 0.023 / 0.023 | `p.forum-lead` → `p.chapter__statement` (same text) |
| orientation-start fr 412 | 1234 → 1312 | 47 → 56 | 108 → 141 | 0 / 0 | `p.page-header__lead` → `p.ingresso__lead` |
| project fr 1440 | 1218 → 1200 | 105 → 96 | 131 → 106 | 0.023 / 0.023 | `p.page-section__text` (the same) |
| home fr 1440 | 1616 → 1656 | 70 → 36 | 129 → 142 | 0.023 / 0.022 | the doorway image |
| home ar 412 | 1842 → 1810 | 39 → 38 | 173 → 167 | 0 / 0 | the doorway image |

**Two cells passed the plan's «no worse» tolerance in series 1:** door-persons fr 1440 (+136 ms) and orientation-start
(+78 ms). All of HEAD's loads had run in the middle of the series, when the machine was busier (busy 52–67 % against
40–56 %). Both cells were measured again:
- **Series 2** ran ABBA in short blocks, n = 8 a cell and tree. Orientation-start came out −70 ms (1252 → 1182), the
  person door ar 412 +16 ms (1432 → 1448), the pathway sheet +2 ms, and the person door fr 1440 +66 ms
  (1166 → 1232).
- **Untraced ABBA**, without the profiler's overhead, n = 12 each, took the person door fr 1440 to BASE 1 124
  [1072–1244] against HEAD 1 108 [1064–1428]. FCP 982 / 974, the longest task 99 / 111, the layout time of the whole
  load 174 / 169 ms (CDP), style 149 / 149.
- **Feature checks:** neutralising `text-wrap`, the door card or the sticky heads changed nothing (`variants-*.json`).

**The person door's traced longest task** (161 → 208 ms at ar 412, CPU ×4, both series) stays well under V4's
370–900 ms tasks, and does not show untraced.

So: LCP ≤ 2.5 s on every cell. The first-render task is never worse than +14 ms. The LCP element is a text block or
the home's image, never worse. CLS ≤ 0.024 on every load of the twin, including the home (flagship, ≤ 0.05). The home
is 0.4–0.5 s earlier than V4 (W1-0: 2 064 / 2 328 ms), and its first-render task is 36–38 ms against V4's 710–914.

**At rest** (`rest.json`, the dev lane, 20 pages × fr, ar × 1440, 390): a 5 s window 3 s after load, with CPU ×4 for
the load.
- **The area's pages:** 0 `requestAnimationFrame`, 0 timers, 0 layouts and 0 style recalculations; ≤ 1.2 ms of task
  time; 0 running animations. **Nothing loops.**
- **The home** (W2-D's) does one layout and three style passes in the window, as at the merge base.
- **CLS on cold loads with CPU ×4:** 0 at 390, and 0–0.019 at 1440, every shift from `nav.main-nav` (O2). The
  merge base shows the same shift (`cls-quick-base.json`: 0–0.025).

## Findings

**1 · major · W3-F1 — The interior's trail and its forward links fell under SP-8's 24 px floor (merge base 28 px →
20 px).**

*The cause.* `static/css/v5/_interior.css` §1 sets `.interior .breadcrumbs` to 13/20. The chapter's link lines
(`.chapter__more`, `.chapter__links`) are 15/20.

*What the reader gets.*
- **The trail's links** («Accueil», «Le projet», «Espace Personnes», «Orientation», «FORUM PERMANENT VÉNÉTIE–MAROC») are
  20 px tall on every page of the area. They were 28 px at `38f78d4` (`base-check/`) and ≥ 24 px in W1-0's V4.
- **The forward links** (`.link-arrow`) are 20 px tall at 1440, where the base drew them at 24–28 px: «Tous les
  parcours réguliers», «Toutes les questions fréquentes», «Mentions légales», «Lire la Privacy Policy», «Voir les
  partenaires», «Questionnaire d'orientation», «En savoir plus sur le promoteur», «Le réseau».
- **Under a coarse pointer:**
  - the trail stays at 20 px;
  - PRJ's «Questionnaire d'orientation» answers on 28 px, because the next row's 44 px pseudo-target overlaps it (the
    links wrap 8 px apart);
  - the «Termes utiles» tags of a pathway sheet answer on 36 px (the diplomas page's tags on 45 px);
  - `/contact/`'s address link answers on 26–32 px.

*Why it matters.* WCAG 2.5.8 holds: the spacing exception covers every one, measured. But SP-8 says «24 px is the
floor of every target; 44 px … every target under a coarse pointer». It is one of §3.1 item 8's Accessibility PASS
checks. `health.js`'s under-24 count goes from 0 (V4 and the merge base) to 1–5 per page.

*Fix.* One rule in the slice, as `.sommaire__link` already does:
- give `.interior .breadcrumbs__item a` and the links of `.chapter__more` and `.chapter__links` `display: inline-flex;
  align-items: center; min-block-size: var(--hit-min)`;
- add a `@media (pointer: coarse)` rule that raises them, `.termes__list .tag` and `.contact-address__link` to
  `var(--hit-primary)`;
- under a coarse pointer, open `.chapter__links`' row gap to ≥ 24 px, so that the 44 px targets no longer overlap.

**2 · minor · W3-F1 (catalogue B2 for the first half) — French on two Arabic pages is not marked or not directed.**
1. **`/ar/forum/`** draws the eyebrow «Espace permanent de dialogue et de coopération» and the h1 «FORUM PERMANENT
   VÉNÉTIE–MAROC» with no `lang`. The same title appears as the trail's link on `/ar/forum/inscription/` and its
   confirmation. The Arabic catalogue holds the French on purpose (the owner's translators, B2), so a screen reader on
   the Arabic page reads it with the Arabic voice (WCAG 3.1.2). The h1 is the event's proper name; the eyebrow is not.
2. **`/ar/agami/`'s FAQ chapter** carries `lang="fr"` on its `<section>`, so 3.1.2 holds. But the interior's RTL rules
   (`_interior.css` §7) and `base.css`'s fallback key on the element's own attribute. The h2 «Qui est derrière Italy
   Legal Entry ?» and the answer are therefore drawn right to left: the «?» and the final «.» stand at the left end
   (`bidi.json`, 1440 and 390; the only such run on the 20 Arabic pages).

The senior review's m6 names both; this is the measured diagnosis. Both are older than the area: the merge base has
the same markup.

*Fix:*
- pass `title_lang=promoter_quote.lang` to `_chapter_head.html` in `pages/agami.html`, and put the `lang` on the answer's
  `<p>`, or let §7's selectors match `:lang(fr)`;
- for the Forum, emit `lang="fr"` when the active language is not French and the translation is the msgid itself (a
  small tag, or the view passing `permanent_title_lang`), until B2 brings the Arabic.

**3 · minor · the merge step — two page types over the interior's CSS ceiling.**
- **Orientation:** 1 027 B over (45 513).
- **The Forum:** 484 B over (44 970).
- **The persons pages** stand at the ceiling (22 B under) with one render-blocking request more (`pathways.css`).

V5.5 performance rule: the twin and the untraced series show no LCP or first-render effect on those page types. The
merge step records the figures in DL54, as DL54-81 asks, rather than trading pages against bytes.
- After the merge, W3-B's −646 B on `main.css` leaves orientation ≈ 381 B over and the Forum under.
- W3-F2's planned deletions (the legacy page header, breadcrumbs and local navigation still in `main.css` for its
  pages) bring both back under.

## Observations (no finding)

- **O1 · W2-C1 / `base.css`:** at desktop widths only `scroll-padding-block-start` is set. A control that Tab brings up
  from below lands flush with the viewport's bottom edge, and its ring's lower edge is cut. This happened on 12 of
  3 062 stops; the control itself is in view, so it is not a 2.4.11 failure. `scroll-padding-block-end: var(--s-4)`
  would keep the whole ring. W3-B's check saw the same (its O1).
- **O2 · W2-C1:** the portico's `nav.main-nav` widens about 0.5 s into a cold desktop load (the doors' JS state). CLS
  0.002–0.025 on the lane and on the twin, also at the merge base. That is under the 0.05 / 0.10 gates, over the 0.01
  target.
- **O3 · W2-C1:** at 200 % text the utility bar's identity line («— promoteur du projet») is clipped by its ancestor.
- **O4 · W3-A:** on «Ma situation», the rail's current entry shows no change on focus under forced colours (W3-B's
  finding 5). axe leaves the phone bar's `aria-controls` to the drawer «incomplete».
- **O5 · W3-F1:** under forced colours the chosen plate wears the focus ring's own sign, a 2 px Highlight outline;
  focus only moves it 2 px out (5 628 px change at 15.1 : 1, visible). For a radio group, focus and choice coincide.
  Once a multiple-choice question exists, a border for «chosen» (outline kept for focus) would tell them apart.
- **O6 · W3-F1:** `role="status"` sits on static content: the sheet's four «en attente» blocks and the static notices.
  A live region present at load announces nothing; `role="note"`, or no role, says what they are. Harmless.
- **O7 · W3-F1 (optional):** after the server's refusal, the focus returns to the question, and the message relies on
  `role="alert"` being announced at load. Focusing the message line (`tabindex="-1"`) would make the announcement
  certain.
- **O8 · method:** the traced loads carry W1-0's heavy categories (the V8 CPU profiler) under CPU ×4. Their absolute
  times are pessimistic: untraced, the person door paints its LCP at 1.11 s.
- **O9 · method:** the contrast probe's own hide / unhide re-runs the links' 120 ms colour transition, so some runs
  were measured at α 0.96–0.99. That is conservative; nothing on the pages fades.
- **Not measured:** Safari and real devices. Only HTTP/1.1 (the dev server). 8782 itself was not used: this was the
  lane's own twin.

## Clean-up

- The minted session was revoked: 1 row deleted on `ile_v5_l7`, and the secrets file removed.
- The lane server and the twin are stopped; 8787 is free.
- The merge-base export (with its copy of `.env`), the two twin static roots and the browser profile are removed.
- The evidence was scanned for cookie, CSRF and secret strings: 0 hits.
- The 21 anonymous questionnaire sessions stay on the lane clone.
- Nothing was written into the worktree but this file.
