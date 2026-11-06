# SECTION SYSTEM V2 — composition library, page-by-page section map, icon treatment V2, motion density V2

V5.22 · the Director's decisions (label `v522-director`) · 30 October 2026 · baseline design-v5 `fdd6e34` (local tag
`v520/gate`, served by the preview `http://127.0.0.1:8780`).

**Binding inputs.** `directives/V5_22_EDITORIAL_PATTERN_SECTION_COMPOSITION_REMEDIATION.md` (the owner's rejection of 30 Oct),
the standing constraints of V5.12–V5.21, the earlier Director's `DECISIONS.md` (V5.12), and the five audits of this phase:
`AUDIT_home.md`, `AUDIT_pages1.md`, `AUDIT_pages2.md`, `RESEARCH.md`, `ICONS.md` (all in `evidence/v522/`).

**Status.** These decisions are final. They are internal: the owner never sees this library as a catalogue (§5, §29).
He sees the pages. Implementation starts with lane S (§9). Only §11 goes to the owner.

---

## 0. The decision in one screen

1. **The diagnosis is settled.** The audits measured it in headed Chromium, and the Director re-checked the disputed
   sections in a headed pass of his own (`evidence/v522/director/`, 15 captures). Below every approved header, every page
   falls back into one device: `.chapter` (`static/css/v5/_pagina.css` §3) and its home twin (`apps/pages/static/pages/css/pages.css:53-213`).
   It is a sticky 4/12 head holding a 24 px glyph and a 28 px title, beside an 8/12 body of one to three blocks of text.
   Then come 64 px of paper, a hairline, and the same again. Content covers 5–42 % of each band. 67–100 % of the motion
   below the fold is the `rise.js` translateY + opacity. 27 of the 30 interior body sections, and every home section
   below the hero, would survive a Word export.
2. **The cure is composition.** Renaming classes cures nothing (§2). Each section is re-composed from **one pattern of
   an eleven-pattern library** (A–L without G, §2). The pattern is chosen for that section's content. Each pattern has
   its own motion signature on one shared timing language. **No two adjacent sections share a signature** (§5).
3. **The chapter device leaves the 15 pages' bodies.** It stays only where a document is the right form: the legal and
   privacy pages, and the CMS reading templates. The bare 24 px mark above a title is retired everywhere. Icons either
   become part of the composition (Icon Treatment V2, §4) or are not drawn.
4. **The approved headers stay.** The exceptions are deliberate and listed in §9.8:
   - Réseau's static actor ring becomes the page's interactive map;
   - the Vivre head is absorbed by its own panorama;
   - the Forum's night head gains its drawing;
   - the two form pages (Recueil des besoins, Proposer une collaboration) and the glossary term page gain the compact
     frontispiece they lack.

   Every other header keeps its composition. Its folio seal becomes the page's T1 seal (§4).
5. **Imagery below the fold, never repeated.** Lane M sources **seven new licensed frames** (Pexels, with full
   provenance) and makes **four re-crops** of existing frames. Every major page then has at least one visual moment
   below its header: a photograph, an integrated drawing, or a material ground (§8).
6. **Everything stays inside the rules.** The rules: locked copy re-composed at render, never retyped; legal notices
   always visible; `main.css` never above 32 718 B gzip -9; new CSS only in page-only sheets with recorded ceilings;
   no new npm dependency; WCAG 2.2 AA; reduced motion as a designed still; RTL mirrored by logical properties.
7. **Lanes:** S (foundation: library + Icon Treatment V2 + Motion Density V2) first, M (imagery) in parallel from day 1,
   then H (homepage), P1 (journeys and spaces) and P2 (system, trust and reading) in parallel. S-close follows. Merge
   order: S → M → H → P1 → P2 → S-close (§9).
8. **One owner question** (§11): the AGAMI page points to a legal notice that is unpublished under Q2.

### 0.1 Rulings where the audits diverged

| Section | Proposals | Ruling | Why |
|---|---|---|---|
| Home `he__body` hand-off | home: F (the route continues) · research: K (a raised plate overlapping the hero's foot) | **F**: the route continues; no plate | The hero's first screen and its fold peek are approved. The hero's own line, continued, joins the hero to the process with no new box. |
| Home orientation | home: F · research: A + K «product glimpse» (CSS questionnaire cards) · icons: T1 + passage | **F**, with station 1 = the T1 `ile-orienta` seal | The owner-approved cut of the locked sentence exists (D-U4, `pathways.services.how_it_works`). A drawn skeleton of a questionnaire reads as a loading state. |
| Home pathways | home: L (tabs + stage) · research: E (grouped catalogue) | **L** | The home needs one state surface. The full catalogue lives on /parcours/ (B). |
| Home trust | home: K (four plates, all visible) · research: L (question deck) | **K** | These are transparency statements. A deck would hide three of the four «Non.». |
| Home anti-fraud + interior callouts | home: ink K plate · icons and pages2: amber register, `shield-alert` seal | **One component, «la protezione»**: ink, the `ile-scudo` T1 seal standing on the plate's top rule, the same on every page | One locked text gets one rendering. The home's prescription forbids an alarm register. Amber stays for status notices (things pending or not authorised). |
| Home ecosystem | home: A with an arched frame · research: A with a bleeding photo · icons: T1 `ile-rete` | **A, arched frame**, no extra seal | The brand's arch, used as the frame, is the icon integrated into the composition (§6). A seal beside it would be a second device. |
| Home entrances (phones) | home: J · research: — | **J, phones only** | It turns 822 px of stacked text into one tactile band, and differs from the hero's 2 × 2 grid above. The four plates are equal; the hero above shows all four at once. |
| Le projet | pages1: K + C + D + E (a lead tile) · research: C (one figure, three states) + L + D | **C** (one figure, three states), then **D** (a new frame), then **E «le porte»** (equal doors) | One figure tells the system, so there is no second actor ring next to Réseau's. PX02 forbids a lead tile among the four audiences. |
| Pilot sequence | pages1: F · research: J (a pinned horizontal track) | **F** | The eight stations read as one image. The mandatory notice must follow at once. Pinning traps keyboard and wheel users. |
| Parcours register | pages1: B (route board) · research: E + View Transition | **B, as lanes** | It gives the movement grammar of §13. Nothing leaves the layout, so no View Transition is needed. |
| Réseau | pages1: a map in the body, names off the head · research: head nodes as controls, panel in the body | **H integrated in the head**: the ring's nodes become the controls; the panel docks in the head's reading column | A panel below the head would change off-screen at 1440 × 900. The system is drawn once and operated once. |
| Institutions «Destinataires» | pages1: H (words under the seats) · research: A (architectural statement) | **H-lite «l'emiciclo»**: glyph-only seats, the sentence whole, linked by hover and focus | RH-5 («one thing once»): words under the seats would print the locked sentence twice. |
| Contact «Une demande précise ?» | pages2: H «trois portes» · research: router | **E «le porte»** joined by a drawn hub line | Three audience doors are a router, not a map. |
| FAQ | pages2: L master–detail · research: L sticky category rail | **L master–detail** | There is one category today. The rail returns automatically when there are several. |
| Closing «Pour aller plus loin» bands | pages1: «Approdo V2» on night | **«l'approdo» on stone** | A night band above the night footer makes a night–paper–night sandwich (the 80 px footer margin). Stone avoids it. |
| Folio seals in the heads | icons: a T1 arch at 64 px in the text column | **A small T1 (32 in 56 × 68) in the folio's place**; the label's drawn rule becomes its sill | The headers are approved: refine the seal, never recompose the header. |
| Chrome gold (menus, mobile sheet) | icons: remove it | **Not in V5.22** | The navbar and the mega menus are preserved (§24). Recorded in §9.8. |
| Text masks («Non.», glossary terms) | audits: mask the words on entry | **Never** | Text never waits. Masks act on images, plates and rules. A user-initiated panel change may mask its incoming content for ≤ 320 ms. |
| Scroll-linked entrances | research: `view()` everywhere | **One-shot entrances are time-based** (IntersectionObserver trigger, fill `backwards`). Scroll-linked only for scrubbed progress and parallax | `rise.js` round 2 found that a scroll-linked one-shot «finished off-screen». V5.20 requires finished animations to clean up. |
| Same-document View Transitions in sections | pages2 (FAQ answer swap) | **Not used** | Lume owns the View Transition names (`ile-mark`). A clip-path swap does the job. |

---

## 1. The rules every section obeys

1. **Composition first.** A section is re-composed by changing its partial and its pattern, never by renaming a class (§2).
2. **The Word/PDF test (§21) is a merge gate.** A V2 section must carry at least two of the following:
   - an integrated drawing or image;
   - its signature motion;
   - a state or an interaction;
   - layered material or depth;
   - a spatial structure that carries meaning (route, ring, lanes, plates).

   A section that would export to Word unchanged does not merge.
3. **Text never waits.** No word is hidden or held for a scroll entrance. On entry a text block may move ≤ 8 px or scale
   ≥ 0.985, with opacity 1 from the first frame. Lines, marks, images, plates and light carry the motion. A panel that
   changes because the reader asked (tab, map, disclosure) may bring its content in by a clip-path or a ≤ 12 px slide
   in ≤ 320 ms. From the keyboard it changes in 0 ms.
4. **One signature per section; adjacent sections differ.** Section heads share one small punctuation: the 48 px label
   rule or the head rule draws once. It is never a section's signature.
5. **Rhythm.** Every page has three heights:
   - a **strip** (≤ 0.2 viewport);
   - **bands** (0.5–0.8);
   - one **moment** (≥ 1 viewport: the page's immersive, interactive or sticky section), placed second or third below
     the header.

   Never two text-only sections in a row. A picture or a drawn figure appears at least every second screen. There is
   one brand wash (`--grad-brand`) per page, and one night band per page below the header (the home excepted: hero
   niche, pilot panorama, reserved row). Two grounds of the same kind never touch.
6. **Locked copy is re-composed, never reworded.** Splits happen at render, from the registry, on the text's own
   separators (`.`, `:`, `;`, `→`, `,`). The element's `textContent` stays byte-identical
   (`locked_content.sha256.json`; no six-word run retyped, `apps/pages/tests/test_prescribed_fragments.py`).
   A locked sentence and its parts are never printed twice (RH-5). On it/en/ar a French locked run stays French
   (`lang="fr"`). It stands in its own box, aligned to its own start, hanging from the page's reading edge. That box is
   a deliberate quotation plate, never a misaligned paragraph.
7. **Legally required notices are always visible, never collapsed:**
   - the anti-fraud text;
   - the pilot's status notice;
   - the how-it-works caveat;
   - «Qui décide ?»;
   - the Formation notice;
   - the «Nature» meta rows;
   - «Définition à caractère informatif.»;
   - the orientation card's caution;
   - the G2 notice when forms are closed;
   - the privacy link where data are collected;
   - the trademark line.

   Progressive disclosure is allowed only for non-mandatory detail: FAQ answers, the home's pathway descriptions,
   definitions behind glossary chips.
8. **Both gate states.** Every home composition renders G3 open (prescribed content) and G3 closed (interim content)
   with the same pattern. Nothing composed depends on a `p3.*` text while G3 is closed.
9. **No metric band (G).** The project has no verified public metric. Numerals are station markers inside F and I,
   never counters.
10. **The references are principles, not models.** agamieuromed.org gives a full-bleed visual break every three
    sections, varied section heights and router bands. studiobadrane.com gives depth on hover and a separate entrance
    per content type. Nothing is copied (RESEARCH §2, R1–R10).

---

## 2. Composition library V2

Eleven patterns, each with an internal name the code uses. **G (metric band) is not used** (§1.9).

### 2.0 What every pattern shares

- **Section shell.** `<section class="sez sez--<pattern>" data-sec="<pattern>" aria-labelledby="…">` with a ground
  modifier: `paper`, `stone`, `brand`, `night`, `photo`.
- **Head roles.** Partial `templates/components/sezioni/_testa.html` with `role`:
  - **statement**: title `--t-title` 36/44 at 600, full measure, the lead beside or under it;
  - **process**: title `--t-band` 28/36, the lead as the route's caption;
  - **router**: title `--t-band`, short, at the reading edge or centred over doors;
  - **panel**: folio label in ILE Mono `--t-folio` with its 48 px rule that draws.

  No head carries a 24 px glyph. When a section has a theme seal it is a T1 integrated in the composition (§4), never
  stacked above the title. No head is `position: sticky` except the C and I patterns' own sticky columns.
- **Trigger contract** (lane S, `static/js/src/rise.js` → «the section runtime»):
  - At load, a `[data-sec]` section that starts below 92 % of the viewport gets `data-sec-state="wait"`. When 25 % of
    it is visible it gets `data-sec-state="in"`, once.
  - A section already in view at load never waits: it is drawn at rest.
  - Under reduced motion, `html.rm`, keyboard input, without IntersectionObserver or without script, no state is
    ever written. The section stands as its designed still.
  - Entrance keyframes are keyed to `[data-sec-state="in"]` with fill `backwards`, so a finished entrance leaves
    `document.getAnimations()` (V5.20).
- **Scroll-linked motion** (`animation-timeline: view()` / `scroll()`) is used only for scrubbed progress (C, I, the D
  drift and widening, the J rail rule). It sits inside `@supports`, `(prefers-reduced-motion: no-preference)` and
  `:root:not(.rm)`, and it reverses with the scroll by nature.
- **Interactive modules** live in `static/js/src/sezioni/<name>.js`. That subfolder is not an esbuild entry, so each
  module is a split chunk.
  - `rise.js` loads a module through `import()` only when `[data-sec-js~="<name>"]` is in the page.
  - Each module stays ≤ 1.5 KB gzip, adds no scroll listener, and disconnects every observer when done.
  - No template gets a new `<script>` and `templates/base.html` is untouched: `rise.js` keeps its name and its
    `reveal_sheet` block.
- **CSS** lives in page-only partials: `static/css/v5/_sezioni.css` (the shell, grounds, head roles, plates),
  `_sigillo.css` (icons V2) and one `_sec-<pattern>.css` each.
  - The family entry sheets that use a pattern import its partial. **None goes into `main.css`.**
  - The motion vocabulary (§5) lives in `static/css/v5/_reveal.css` → `core/reveal.css`, which every public page already loads.
  - Distances are `--sez-*` custom properties declared in `_sezioni.css`. **No new duration or easing token**: the
    `tokens.css` set is enough, and `test_rm_flag_parity.py` stays untouched.
- **Data.** A pattern partial takes plain data built by the page's service or view, plus the S helpers for locked
  copy:
  - `apps/cms/locked_split.py` cuts by sentence, colon, semicolon, arrow or first clause. It returns `None` unless the
    parts rebuild the source character for character; the caller then renders the text whole.
  - The filters `locked_spans` and `emphasize` wrap exact substrings in spans and return the text unchanged when
    absent.
  - Every split carries an equality test.
- **No-JS.** Every pattern renders complete without script: lists stay lists, panels are all shown, disclosures are
  native `<details>`. A module only upgrades. Print shows the final state and every panel.

### A · «la campata» — architectural split

- **Use when** one strong image and one identity or statement belong together. Never for a list.
- **Anatomy:**
  - media 7/12 (or 5/12), bleeding to the viewport edge on its side;
  - text 5/12 (or 7/12);
  - a 1 px connector from the image edge into the text column;
  - optional: an arched frame (the brand doorway's geometry) with a sill line under it;
  - optional: a detail crop overlapping by `--s-8`.
- **Responsive:**
  - ≥ 80 rem: 7/5 split, image bleeding;
  - 64–80 rem: 6/6;
  - 48–64 rem: image above at 3:2 (or 4:3), text below at the 36 rem measure;
  - < 48 rem: the image full width first, then the text;
  - at 360: the arch flattens to a segmental arch (radius 1.5 × width) so the frame keeps its height.
- **RTL:** sides swap through logical grid areas, the mask origin follows `[dir]`, and photographs never mirror.
- **Motion signature: MASK.** A clip-path opens from the outer edge, or the arch silhouette widens to the frame. 900 ms,
  `--ease-enter`. The frame settles from `--reveal-zoom` (1.06) to 1 over 1 080 ms. The connector then draws (scaleX,
  `--motion-draw`, `--ease-sine`). The text never moves.
- **Interaction:** the action is a button or a link row. On a fine pointer, hovering the image's link lifts the
  connector light.
- **A11y:** `<figure>` with its credit `<figcaption>`, the text in a `<div>` with its own heading level, one action.
- **Still** (reduced motion): the framed image in colour, the connector drawn.
- **Slots:** one body frame per instance (3:2, 4:3, or 4:5 on the wide side), lazy.
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/sezioni/campata.html` (`media_slot`, `side`, `frame="arch"\|"plain"`, `detail_slot`, `head`, `body`, `action`) |
  | CSS | `_sec-campata.css` ≤ 1.2 KB gzip |
  | JS | none |
- **Variant «la boussole»** (the shared closing «Orientation» band):
  - 5/12: a drawn compass, the `ile-orienta` geometry at display scale (200 px), hairline rings, the north tip in
    gold (the page's arrival gold);
  - 7/12: the action card, borderless on the brand wash: title 28, text, primary button, the help line as a side
    annotation;
  - signature **SEMANTIC TURN**: on entry the needle settles once from −25° to point at the button (480 ms,
    `--spring-soft`); hovering or focusing the button turns it 4° further;
  - still: the needle at rest, pointing at the button.
- **21st provenance:**
  - Split Content Section · 28310 · `21st.dev/@felipemenezes098/components/content-06`: headline beside a media frame
    that reveals;
  - Editorial Collage Hero · 19074 · `21st.dev/@felipemenezes098/components/hero-04`: two overlapping frames as
    layering;
  - SVG Clip Mask · 31436 · `21st.dev/@educalvolpz/components/svg-clip-mask`: an image seen through a shaped mask (the
    ILE arch);
  - refused: stats and avatar rows (28168), coloured twin panels (29418), the mask's morph loop.
- **Used on:** home S7; Projet pilote PP-2 («due porte»); Entreprises EN-4; AGAMI AG-1; Fraudes AF1+2; Forum FO1;
  «la boussole» on Parcours sheets, Formation and Diplômes.

### B · «il tracciato» — interactive journey (route board)

- **Use when** several routes or stations are chosen or explored. The stations have destinations of their own.
- **Anatomy:**
  - an origin node at the reading edge;
  - a trunk;
  - lanes (one per family or phase), each with a head (a folio label, optionally a frame);
  - station cards (numeral, title, one line, arrow);
  - a selection control (native radios or links);
  - the light that travels a lane.
- **Responsive:**
  - ≥ 64 rem: lanes as horizontal rows from the trunk, cards in a row, the frame at the lane head;
  - 48–64 rem: the lane head on top, cards two-up;
  - < 48 rem: the trunk down the reading edge, each lane a block (a 21:9 frame strip, cards stacked), the selection
    as a sticky segmented bar under the letterhead (`scroll-padding-top` set so focus is never obscured, WCAG 2.4.11).
- **RTL:** the trunk on the right, lanes run right to left; a French card is its own LTR box at its own start.
- **Motion signature: PATH PROGRESSION.**
  - On entry the trunk and lanes draw from the origin (900 ms, lanes 120 ms apart).
  - On selection the light travels the chosen lane once (a dash of the same path, `--motion-route-light` 1 200 ms,
    `--ease-sine`). The lane's frame develops from black and white to colour (`--motion-slow`). The lane's cards go to
    `--text-1`; the others go to `--text-2`, never to an opacity.
  - Nothing leaves the layout.
- **Interaction:** native radio group (arrow keys, focus visible on the chip). Hovering or focusing a card lights its
  lane segment. Cards are links.
- **A11y:** `fieldset` + `legend`, `ol` per lane, count line `aria-live="polite"` (as today).
- **Still:** every lane drawn, all frames in colour, the selection instant.
- **Slots:** optional, one frame per lane head (3:2, narrow 21:9 strip; treatment `select`: black and white at rest,
  colour when its lane is chosen, hovered or focused).
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/sezioni/tracciato.html` (`origin`, `lanes[{key, label, frame_slot, stations[]}]`, `control`) |
  | CSS | `_sec-tracciato.css` ≤ 1.4 KB gzip; the selection read by `:has(:checked)` (no JS) |
  | JS | none |
- **21st provenance:**
  - Wizard Steps · 23576 · `21st.dev/@ddoemonn/components/wizard-steps`: the panel or light comes from the side of
    travel; keyboard on the rail;
  - Growth Story Timeline · 28273 · `21st.dev/@shadcnspace/components/timeline-01`: the route fills as one advances;
  - refused: check marks, completion, percentages (O14: nothing ticks a step for anyone).
- **Used on:** Parcours PA-1, Parcours PA-2 (station links), Universités U1.

### C · «il racconto» — sticky story

- **Use when** a short run of statements explains one system and a single figure can act it out. Not for long prose.
- **Anatomy:**
  - a sticky figure column (5/12 from 64 rem, at the inline start), on a night plate;
  - a text column (7/12) of steps, each with its own heading and a 2 px progress bar on its reading edge;
  - the figure has one state per step (layers drawn or lit).
- **Responsive:**
  - ≥ 64 rem: pinned at `--header-h-scrolled + 24 px`;
  - < 64 rem: not pinned; the figure drawn once above the steps at full width (about 240 px), showing its final
    state; each step keeps its bar;
  - the section is exactly as tall as its text: no artificial scroll length.
- **RTL:** the figure on the right, its drawing mirrored, the text LTR blocks hanging from the right edge.
- **Motion signature: LAYERING.**
  - The step in the middle band of the viewport is active (IntersectionObserver, `rootMargin: -45% 0px -45% 0px`). It
    writes `data-step` on the figure.
  - The figure's layers draw or light per state: 480 ms, routes 900 ms.
  - The active step's text is `--text-1`, the others `--text-2`.
  - Each step's bar fills on `view()`.
- **Interaction:** scrolling only, nothing to operate. The reading order is unchanged.
- **A11y:** the figure is `aria-hidden` (the words carry the content), each step a `<section>` with its `<h2>`.
- **Still:** the figure in its final drawing, all steps at `--text-1`.
- **Slots:** none (drawn).
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/sezioni/racconto.html` (`figure` (an inline SVG partial with `data-state` layers), `steps[{id, heading, body(spans)}]`) |
  | CSS | `_sec-racconto.css` ≤ 1.2 KB gzip |
  | JS | `sezioni/racconto.js` ≤ 0.9 KB gzip |
- **21st provenance:**
  - Scroll Reveal Content A · 19203 · `21st.dev/@abui/components/scroll-reveal-content-a`: per-step bar and figure
    change at thresholds;
  - Services Stack · 33309 · `21st.dev/@ivarunchaudhary/components/services-stack`: a sticky figure whose drawing acts
    out the active step;
  - refused: the 300 vh scroll trap, 50 % opacity on inactive text, looping drawings, card scale-out.
- **Used on:** Le projet (En bref · Pourquoi · Qui porte).

### D · «il panorama» — immersive image panel

- **Use when** one photograph carries the section's meaning, or the page needs its full-bleed break.
- **Anatomy:** the frame starts at the container width with the card radius. It widens to full bleed with radius 0 as
  it enters. Optionally a statement on a solid plate (`--plate-night-photo` or paper; never glass, SH-5). The credit
  sits in a corner.
- **Responsive:**
  - ≥ 64 rem: 21:9 (or the panel ratio), 60–82 vh;
  - 48–64 rem: 16:9;
  - < 48 rem: 4:5, drift off, the statement plate under the image, overlapping it by 40 px.
- **RTL:** the plate on the reading edge; photographs never mirror.
- **Motion signature: WIDENING + DRIFT.**
  - `clip-path: inset(0 var(--pan-inset) round var(--pan-r))` goes to 0/0 over `animation-range: entry 10% cover 35%`
    (scroll-linked).
  - The image drifts through M22 (`[data-parallax]`, scale 1.12, ±3 %, from 48 rem).
  - Variant «develop in sequence» (home pilot): two halves develop from black and white to colour on offset ranges,
    and a seam line draws.
- **Interaction:** none, or the plate's one link.
- **A11y:** `<figure>` + credit. The statement is real text on an AA plate (`--scrim-photo-aa`).
- **Still:** full bleed, colour, no drift.
- **Slots:** one 21:9 + 4:5 band frame (role `band`, lazy, ≤ 60 KB at 1 920 w), or a diptych of 2:3 panels.
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/sezioni/panorama.html` (`slot` or `pair`, `plate`, `ratio`) |
  | CSS | `.panorama` in `static/css/v5/_photo.css` (+ ≤ 0.7 KB gzip) |
  | JS | none |
- **Lane S also fixes the M22 specificity defect** (`_reveal.css` M22 0,3,1 is beaten by M2 0,3,2). A band then
  drifts instead of masking like every other photograph.
- **21st provenance:**
  - Scroll Reveal Image · 24466 · `21st.dev/@unlumen/components/scroll-reveal-image`: the frame widens to full bleed,
    radius to 0;
  - Parallax Image · 20023 · `21st.dev/@pulkitxm/components/parallax-image`: the image drifts against its frame;
  - refused: blur on scroll (2544), zoom tunnels (5967), scroll-jacking, video.
- **Used on:** home S4 (pilot, develop variant); Le projet (after the story); Entreprises EN-2; Vivre V1.

### E · «il mosaico» — dynamic feature grid

- **Use when** the destinations or features have a real hierarchy (a lead tile), or as the equal doors and compact
  routers below. Never an equal 3 × 1 grid of icon cards: that is the rejected pattern.
- **Anatomy (hierarchical):** `grid-template-areas` per breakpoint. A lead tile spans 2 × 2 (a live diagram or a
  frame). Compact tiles hold a T2 glyph in its tile with title and one line. The foot cell holds a link or a help line.
- **Variant «le porte»** (unranked, PX02): equal door plates with arched tops on stone, night door faces, T2a audience
  discs with audience-accent rings (accents on night only).
  - On hover or focus a door widens (`flex-grow` 1 → 1.25, `--ease-layout` 320 ms, ≥ 64 rem), its threshold lights
    and its arrow line extends.
  - Every word stays visible at rest: nothing hides behind the hover.
- **Variant «il rimando»** (the reading pages' foot): three compact link tiles on stone.
- **Responsive:**
  - ≥ 80 rem: as drawn;
  - 64–80 rem: the lead tile 2 × 1;
  - 48–64 rem: two columns;
  - < 48 rem: one column, tiles ≥ 64 px tall, doors stacked at full width.
- **RTL:** areas mirror; arrows follow `FLIP_RTL`.
- **Motion signature: STAGGER.** On entry the tiles' threshold rules draw and their glyph tiles light in turn
  (`--motion-stagger` 60 ms, ≤ 6 steps).
  - Depth on hover: a pre-painted `--shadow-2` layer fades in (SH-4: a shadow never animates), with a 2 px lift and
    the glyph's 2 px directional shift.
  - The M21 spotlight is in `--accent-mark` at 10 % on paper.
- **Interaction:** whole-tile links, ≥ 44 px targets, focus equals hover.
- **A11y:** `<ul>` of `<li>`, each tile one `<a>` whose name is its title. A «stretched link» keeps the accessible
  name short.
- **Still:** tiles at rest, rules drawn.
- **Slots:** optional, one lead frame (develop) or one live diagram.
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/sezioni/mosaico.html` (`variant="grid"\|"porte"\|"rimando"`, `tiles[{href, glyph, title, line, weight}]`, `foot`) |
  | CSS | `_sec-mosaico.css` ≤ 1.2 KB gzip |
  | JS | none |
- **21st provenance:**
  - Bento Grid Hero · 26904 · `21st.dev/@ln-dev7/components/bento-02`: one wide lead tile and compact tiles;
  - Animated Features Bento with Live Diagrams · 36110 · `21st.dev/@kedhareswer/components/ink-orbit-features`: a tile
    holding a live diagram;
  - Hover Expand Gallery · 27010 · `21st.dev/@kedhareswer/components/hover-expand-gallery`: equal plates where the
    focused one grows (for «le porte»);
  - refused: equal grids as a default, magnification (10470), neon edges (6014), stat tiles, rotated labels,
    hover-only content.
- **Used on:**
  - «le porte»: Le projet LP-4, Contact C4;
  - «il rimando»: FAQ Q2, Glossaire G3, Vivre V2;
  - grid: Formation F2, Diplômes D3, Parcours PA-3, Glossaire G2 («il lessico»: term cards).

### F · «la linea V2» — visual process

- **Use when** a real sequence of stations explains a procedure. It is never a progress tracker: no current station,
  no tick.
- **Anatomy:** the passage drawing evolved (`templates/components/stepper.html` + `static/css/v5/_journey-passage.css`),
  not a second invention. Each large station has:
  - a numeral in ILE Mono at `--t-title` 36 (`--t-band` 28 under 48 rem);
  - a T2 tile (24 in 48) or, for the origin, the section's T1 seal;
  - the label at `--t-entry` 20/28 (locked capitals as written at `--t-ui`, tracked);
  - optional: one line of text.

  Straight segments are CSS-drawn between grid cells. A **curved or measured** connector between real boxes is an SVG
  overlay drawn by `sezioni/flow.js` (ResizeObserver, logical positions, so Arabic mirrors by itself). The caveat or
  status plate stands as the route's terminal plate, at body size.
- **Responsive:**
  - ≥ 80 rem: all stations on one row (up to 8, a gently stepped line);
  - 48–80 rem: rows of four joined by a «carriage return» segment, so row 2 still reads in the reading direction;
  - < 48 rem: down the reading edge, the tile on the line, the label beside it.
- **RTL:** stations run right to left; locked French labels are LTR runs centred under their tiles.
- **Motion signature: LINE DRAW.**
  - On entry the route draws segment by segment (`--motion-draw` per segment group, `--ease-sine`).
  - Each tile's strokes draw when the line reaches it (480 ms).
  - Labels go from `--text-2` to `--text-1`; stations light 120 ms apart.
  - The call at the route's end takes the arrival light last (gold, the page's one arrival).
  - Hovering or focusing the end call sends one light along the whole route (`:has()` + `--light`).
- **Interaction:** the end call. Where a station has its own destination (only in B) it is a link.
- **A11y:**
  - an `<ol>`;
  - for a locked sentence cut into stations, the whole sentence is present once (`visually-hidden`) and the drawn
    fragments are `aria-hidden`, as /parcours/ does today (`templates/pathways/index.html:82-90`);
  - the arrows stay as hidden text.
- **Still:** the route drawn, every station lit, the arrival lit.
- **Slots:** none.
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/stepper.html` V2 (`size="large"`, `origin_seal`, `terminal`, `end_action`) |
  | CSS | `_journey-passage.css` (+ ≤ 1.2 KB gzip) |
  | JS | `sezioni/flow.js` ≤ 1.3 KB gzip, only where the connector is measured |
- **21st provenance:**
  - Klyv Animated Beam · 38286 · `21st.dev/@klyv-ui/components/klyv-animated-beam`: a connector between real boxes,
    re-measured, the light as a dash of the same path;
  - How It Works · 19861 · `21st.dev/@chamaac/components/how-it-works`: zig-zag stations on one curve;
  - refused: infinite pulses, rotated pinned cards, handwritten numerals.
- **Used on:** home S2; Projet pilote PP-1; Entreprises EN-1 (measured); Diplômes D1.

### H · «la mappa» — interactive actor map

- **Use when** actors and their relations are the content. Never as decoration of a list.
- **Anatomy:**
  - a hub (photo, mark or caption);
  - actor nodes on a ring (T2a discs with labels) and spokes;
  - a panel showing the selected actor's sentence and link, docked where the eye already is (beside or under the
    ring);
  - a highlight ring that glides to the selected node.
- **Responsive:**
  - ≥ 64 rem: the ring beside the panel;
  - < 64 rem: the ring above the panel, nodes ≥ 44 px targets;
  - < 48 rem: when the ring is under 300 px wide, the nodes become a horizontal tab rail of glyph chips above the
    panel (all reachable, no hidden actor).
- **RTL:** the ring mirrors (clockwise becomes counter-clockwise).
- **Motion signature: RELATIONAL DRAW + GLIDE.**
  - On selection the spoke and the two neighbour links draw (`--motion-emphasized` 320 ms).
  - The highlight glides around the ring (rotate about the ring centre, `--spring-soft`).
  - The panel's content crosses in by clip-path from the node's side (≤ 320 ms).
  - On entry the nodes settle from 0.92 to 1, 60 ms apart (`--spring-soft`).
- **Interaction:** tablist (or radio group) with roving tabindex. Arrows rotate the selection; Home and End work;
  Escape returns to the hub. The panel's link is the action. Hover previews on a fine pointer only; a click or Enter
  commits.
- **A11y:**
  - the panels are `role="tabpanel"` and all stay in the DOM;
  - panels stack in one grid cell (`grid-area: 1 / 1`; hidden ones `visibility: hidden`), so the panel's height is
    the tallest panel's and no selection shifts the layout (CLS 0);
  - with `html.no-js` all entries are listed;
  - the nodes are anchors to their entries, so `:target` shows one without the module.
- **Still:** the ring drawn, the hub caption shown, the selection instant.
- **Slots:** the hub photograph when the page already owns one (Réseau's `network.table`).
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/sezioni/mappa.html` (`hub`, `nodes[{key, glyph, accent, label, panel}]`, `layout="ring"\|"arc"`) |
  | CSS | `_sec-mappa.css` ≤ 1.4 KB gzip |
  | JS | `sezioni/mappa.js` ≤ 1.5 KB gzip |
- **Variant «l'emiciclo»** (CSS only, words once):
  - the nodes are glyph-only seats on an assembly arc (`aria-hidden`);
  - the locked sentence stands whole beside them, its enumerated items as spans (`split_enumeration` at render);
  - hovering a seat or a phrase, or `:focus-within` on the phrase's link, lights both (`:has([data-seat="n"]:hover)`);
  - no module, no tab stops added;
  - motion: the arc draws, the seats stagger.
- **21st provenance:**
  - Nodes · 40282 · `21st.dev/@abhishek-mallick/components/nodes` and Relay Hub Diagram · 40264 ·
    `21st.dev/@hello_54e122be/components/relay`: the route from the hub to the pointed or focused actor lights;
  - Fluid Hover Highlight · 39507 · `21st.dev/@educalvolpz/components/fluid-hover-highlight`: a highlight that glides
    instead of blinking;
  - refused: orbits, energy levels, isometric 3D.
- **Used on:** Réseau (in the head); Forum FO2b; Parcours sheet PS-2 (arc); Institutions IN-1 («l'emiciclo»).

### I · «il filo» — timeline / progression with a sticky rail

- **Use when** the content is a real progression read in order (steps of a sheet, two times, eight clauses), and the
  reader benefits from knowing where they are.
- **Anatomy:**
  - a vertical route with milestones: numeral 36, T2 tile 40 on the line, heading 20;
  - optional: a sticky companion (the page rail «Sommaire», or a sticky text column);
  - optional: a horizontal crossing between two times at ≥ 64 rem.
- **Responsive:**
  - ≥ 64 rem: the rail at the inline start (3/12) or the sticky column (5/12);
  - < 64 rem: no sticky part; the «Sommaire» stays in the head (as today), the route down the reading edge.
- **RTL:** the route and rail on the right.
- **Motion signature: SCROLL PROGRESSION.**
  - The line's `scaleY` is bound to `view()` (M16, extended): the route advances as it is read.
  - A milestone's node lights when the line reaches it.
  - The rail's fill uses a scroll timeline, and its current item takes `aria-current="location"` (`sezioni/spia.js`).
- **Interaction:** the rail's anchors.
- **A11y:** `<ol>`; the rail is `<nav aria-label>`; `aria-current` is announced only on focus, never on scroll.
- **Still:** the route fully drawn, every node lit.
- **Slots:** optional, one frame per station (Formation: two, developing as the line leaves and arrives).
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/sezioni/filo.html` (`milestones[]`, `rail`, `crossing`) |
  | CSS | `_sec-filo.css` ≤ 1.0 KB gzip |
  | JS | `sezioni/spia.js` ≤ 1.0 KB gzip, only with a rail |
- **21st provenance:**
  - Timeline · 857 · `21st.dev/@manuarora700/components/timeline`: a sticky label column beside the content while a
    beam follows the scroll;
  - Scroll animated timeline · 35029 · `21st.dev/@ibrandify/components/scroll-timeline`: the line draws as it is read;
  - refused: Lenis and GSAP (26930).
- **Used on:** Parcours sheets PS-1; Formation F1 («la traversata»); Forum FO2a.

### J · «il passaggio» — controlled horizontal scroll (phones only)

- **Use** only where a stacked list would cost more than a screen and the items are equal. Today that is one place:
  the home's four entrances below 640 px. No pinned or scroll-jacked horizontal track anywhere.
- **Anatomy:** a native `scroll-snap-type: x mandatory` row of equal plates, each 78 % of the column wide, with an
  18 % peek of the next. The row scrolls inside itself (page overflow 0). Under it, a slim position rule bound to the
  rail's own scroll (`animation-timeline: scroll(self inline)`). No arrows, no dots, no autoplay, no loop.
- **RTL:** the row starts at the right edge; French plates stay LTR inside.
- **Motion signature: DIRECTIONAL SLIDE.** Native snap. On first entry each plate's arch outline draws (480 ms,
  60 ms apart). The plate in view is at `--text-1`; the peeking plate's text is at `--text-2`.
- **Interaction:** swipe; Tab moves plate to plate (`scrollIntoView({inline: "nearest"})` on focus, no JS needed
  beyond the browser's own focus scrolling). The pressed plate lights its arch's top edge.
- **A11y:** an `<ol>` with four `<li>`. Each plate is one link with all its locked text visible.
- **Still:** snap stays (it is not animation); no draw.
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/entrances.html` (`rail=True`) |
  | CSS | `_sec-passaggio.css` ≤ 0.6 KB gzip |
  | JS | none |
- **21st provenance:**
  - Horizontal Depth Fade · 18439 · `21st.dev/@unlumen/components/horizontal-depth-fade`: the item in view in full
    ink, neighbours muted;
  - Horizontal Feature Reveal · 26062 · `21st.dev/@hyperiux/components/horizontal-feature-reveal`: a fallback that
    simply stacks;
  - refused: pinning and scrubbing, blur, GSAP.

### K · «lo strato» — layered material section

- **Use when** the content is a set of statements, an action or a notice that must feel institutional and physical:
  plates on a ground.
- **Anatomy:**
  - a ground: stone `--surface-area`, a graded photograph under a veil, or night `--surface-night` + `--mesh-dark` +
    the static grain `static/img/grain.svg` at 3–4 %;
  - one to five raised plates: `--surface-raised` at `--radius-md`, a 1 px `--line-rhythm` edge, a pre-painted shadow
    layer;
  - drawn architectural marks: sill lines, corner brackets as formwork marks, the page motif returning low as a
    bookend.

  At most one raised surface (`--shadow-2`) per first screen (the V5.20 rule). The other plates sit at `--shadow-1`.
- **Variants:**
  - **«la protezione»**: the anti-fraud plate everywhere. Its 3 px ink top rule is the sill of the `ile-scudo` T1 seal
    (the small seat: 32 in 56 × 68, as the head folios) at the reading edge. The locked title in its own capitals, then the locked body in three levels:
    - sentence 1 at `--t-entry` 600;
    - sentences 2–3 at `--t-body`;
    - sentence 4 at `--t-body` 600 behind a 1 px rule.

    All are spans of one `<p data-locked>`. Ink only, never red or amber. The link «Lire la page…» is a secondary
    button.
  - **«l'approdo»**: the closing «Pour aller plus loin» band. On stone. Weighted tiles:
    - the Forum tile is typographic on a night face (Q4);
    - the others are raised paper with a T2 or T2a glyph;
    - the page motif is drawn low in `--line-structure` at 30 % as a bookend.
  - **«la targa»**: one contact or identity plate on night (the address as a large type element).
  - **«la scheda»**: the glossary term page's definition plate.
- **Responsive:**
  - ≥ 64 rem: plates in a 2 × 2 or 1 + 2 arrangement;
  - < 64 rem: one column;
  - the ground photograph switches 21:9 → 4:5.
- **RTL:** plates mirror; the rule and seal at the right edge; each French run LTR inside its plate.
- **Motion signature: DEPTH.**
  - Plates settle from scale 0.985 to 1 while their pre-painted shadow layer goes from 0 to 1 (480 ms, 60 ms apart).
  - The photographic ground drifts by at most 24 px against the scroll (scroll-linked).
  - On a night or stone band, one light sweep crosses once as it enters (`--motion-route-light`, `--ease-sine`).
  - «la protezione»: the top rule draws from the reading edge (900 ms), then the seal draws (§4.7), then sentence 1
    goes from `--text-2` to `--text-1` (480 ms).
  - Nothing shakes, pulses or loops.
- **Interaction:** plates that open something are links (the question's heading carries the stretched link). The
  M21 lit edge under a fine pointer is the K «spotlight», in `--accent-mark` on paper and oro only on the night door
  plate.
- **A11y:** plates are `<article>` with a heading; notices keep their roles; legal texts are always fully visible.
- **Still:** the plates at rest, rules and seals drawn, no drift.
- **Slots:** optional, one ground frame (21:9 + 4:5, role `band`, desaturated in the file, never a CSS grayscale
  outside the hero).
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partials | `templates/components/sezioni/strato.html` (`ground`, `plates[]`, `variant`), `sezioni/protezione.html`, `sezioni/approdo.html` |
  | CSS | `_sec-strato.css` ≤ 1.6 KB gzip |
  | JS | none |
- **21st provenance:**
  - Spotlight · 35180 · `21st.dev/@kevingirelli/components/spotlight`: a lit edge under the pointer;
  - Corner Frame · 35211 · `21st.dev/@kevingirelli/components/corner-frame`: corner brackets as formwork marks;
  - Ocean grain · 24379 · `21st.dev/@hazelgrace3026/components/ocean-grain`: static grain;
  - refused: animated grain, glow, glass on paper.
- **Used on:**
  - home S5 + S6 (the integrity band);
  - «la protezione» on Parcours, the sheets, Formation and Diplômes;
  - «l'approdo» on Projet pilote, Entreprises, Institutions, Réseau and AGAMI;
  - «la targa» on AGAMI AG-3;
  - «la scheda» on the glossary term page;
  - Forum FO3;
  - the compact frontispiece of the two form pages (a K head, §3.5).

### L · «l'indice» — interactive content reveal

- **Use when** a set is better read one item at a time, and every item stays in the DOM.
- **Three forms:**
  1. **Tabs and master–detail** (≥ 64 rem): an index at the inline start (rows with a 20 px glyph and the title;
     a 2 px marker), the stage or answer plate beside it (a T2 tile 64 with a 32 px glyph, the title at 28, the text
     at 20/28, its links). The first item is selected; the order is the locked order, never a ranking. The URL hash
     follows the item where permalinks exist (FAQ).
  2. **Exclusive disclosure** (< 64 rem, or for definitions in place): native `<details name="…">`, all closed at
     first, one open at a time, `interpolate-size` open 200 ms and close 120 ms (M6).
  3. **Scroll-spy rail**: a sticky index whose indicator plate glides to the part in view (`sezioni/spia.js`).
- **RTL:** the index on the right; arrow keys follow the visual order.
- **Motion signature: GLIDE.**
  - The marker or indicator glides (`--spring-soft`).
  - The stage content enters by clip-path from the index side (320 ms, `--ease-enter`), and the stage glyph's strokes
    draw (480 ms).
  - On entry the index rows go from `--text-3` to `--text-1`, 60 ms apart.
- **Interaction:** the full ARIA tabs pattern (`role="tablist"`, `aria-orientation="vertical"`, roving tabindex,
  Arrows/Home/End, Enter/Space). `aria-expanded` on disclosures.
- **A11y:** the keyboard path never animates (`html[data-input="key"]`); no content behind hover only; print shows
  every panel.
- **Still:** an instant panel swap.
- **Contract:**

  | Piece | Value |
  |---|---|
  | Partial | `templates/components/sezioni/indice.html` (`form="tabs"\|"explorer"\|"disclosure"\|"rail"`, `items[]`) |
  | CSS | `_sec-indice.css` ≤ 1.4 KB gzip; the panel engine stays `tabs.css` (already in `main.css`), so no second tab system |
  | JS | `sezioni/indice.js` ≤ 1.3 KB gzip (tabs and master–detail, hash sync); `sezioni/spia.js` for the rail |
- **21st provenance:**
  - Feature List Showcase · 27506 · `21st.dev/@felipemenezes098/components/feature-01`: select, then reveal;
  - Scroll Spy · 23554 · `21st.dev/@ddoemonn/components/scroll-spy`: a gliding indicator;
  - Rectangular Text Reveal · 26076 · `21st.dev/@hyperiux/components/rectangular-text-reveal`, for heads: a plate or
    rule sweeping beside a heading, never the letters;
  - refused: autoplay, hover-only content, «helpful?» buttons.
- **Used on:** home S3 (tabs); FAQ Q1 (explorer); Glossaire G1 (rail); the sheets' PS-4 (definitions in place);
  Diplômes D1 (station disclosures at ≥ 64 rem); AGAMI AG-2 (one disclosure).

### 2.1 Library → pages (where each pattern lives)

| Pattern | Home | Interior pages |
|---|---|---|
| A campata | S7 | PP-2, EN-4, AG-1, AF1+2, FO1; «la boussole»: PS-5, F3, D4 |
| B tracciato | — | PA-1, PA-2, U1 |
| C racconto | — | Le projet |
| D panorama | S4 | Le projet, EN-2, Vivre V1 |
| E mosaico | — | LP-4, C4 (porte); Q2, G3, V2 (rimando); F2, D3, PA-3, G2 (grid) |
| F linea V2 | S2 (+ H0 route) | PP-1, EN-1, D1 |
| H mappa | — | Réseau (head), FO2b, PS-2; IN-1 (emiciclo) |
| I filo | — | PS-1, F1, FO2a |
| J passaggio | S1 (phones) | — |
| K strato | S5 + S6, S8 (refined) | protezione ×4, approdo ×5, AG-3, term page, FO3, form heads |
| L indice | S3 | Q1, G1, PS-4, D1, AG-2 |

---

## 3. Page-by-page section map

How to read an entry: **ID · section** — *where*: URL · template:line · root CSS block — *now* (fr 1440 unless stated):
what the visitor sees, and the evidence capture (paths under `evidence/v522/`) — **decision** — then composition,
imagery, motion, interaction, icon, typography, density, locked copy, RTL. «KEEP» means the composition stays;
refinements are named.

### 3.1 Homepage `/xx/` — `templates/pages/home.html`, `templates/pages/home/_*.html`; sheets `pages/css/pages.css` + `hero.css`; script `home.js` · lane H

**After V2** (grounds, signatures):

| Order | Section | Ground | Signature |
|---|---|---|---|
| 0 | hero | paper wall + night niche | its own (approved) |
| 1 | H0 route | paper → brand fade | LINE DRAW (route) |
| 2 | S2 orientation | brand wash | LINE DRAW + station light |
| 3 | S3 pathways | paper | GLIDE (state) |
| 4 | S4 pilot | night, full bleed (the moment) | WIDENING + DEVELOP |
| 5 | S5 + S6 integrity | stone over the new masonry ground | DEPTH |
| 6 | S7 ecosystem | paper | MASK (arch) |
| 7 | S8 reserved | night, joined to the footer | SEMANTIC TURN |

(S1 is phones only: J, DIRECTIONAL SLIDE.) The H0 and S2 signatures are two halves of one line language (the route
continues); every other neighbour pair differs. Scores target ≥ 4.5 composition and coherence, ≥ 4 on the rest
(§10).

- **Hero · KEEP.** Its first screen is approved: door, path, plates, Q1's visible H1. Untouched except its foot.
- **H0 · the hand-off `he__body` → F «la soglia» (the route continues).** *Where:* `_hero.html:124` `p.he__body`,
  `hero.css:1133-1165` (a 56 px foot). *Now:* a lone 4-line 27 px paragraph on paper, 56 px of paper, then a hard cut
  to the teal band. The hero's bronze route ends at the door. Evidence: `director/d_fr_1440_home_handoff.jpg`,
  `home/s1_fr_1440_01_handoff.jpg`.
  - *Composition.* The statement stays the hero's last row; the peek stays. A 2 px route line in the hero's own route
    ink (`--he-bronze`, `--he-gold-line` once lit) starts at the statement's first line on the reading edge and runs
    down beside it into the orientation band, where it becomes S2's route. The ground fades from paper to
    `--grad-brand` over the statement's last 96 px (no cut). The 56 px foot is gone.
  - *Motion.* The line draws once as it enters (scaleY, `--motion-draw`, `--ease-sine`). Still: drawn.
  - *Icon.* None.
  - *Density.* Unchanged.
  - *RTL.* The line on the right edge. The French run gets one alignment: LTR start, in its own box hanging from the
    RTL edge. This applies the `pages.css:26-31` rule instead of `hero.css:208`'s end alignment.
  - *Build.* `hero.css` ≤ +0.5 KB gzip, no JS.
- **S1 · «Quatre accès à l'écosystème» (phones < 640 px) → J «il passaggio».** *Where:* `_entrances.html:14-21`,
  `components/entrances.html:22-63`, `pages.css:335-460`; hidden ≥ 640 px by `hero.css:643/995` (deliberate, UX-1).
  *Now:* 822 px of capitals questions, sentences and calls on hairlines, one screen after the hero's four tiles.
  Evidence: `director/d_fr_390_home-entrances.jpg`.
  - *Composition.* Four equal door plates in a snap rail. Each plate holds:
    - an arched top seat with its T2a audience disc (32 in 56; audience accent on the night seat);
    - the prescribed question;
    - the sentence;
    - the call (12 locked strings, as written).
  - *Size.* About 430 px instead of 822.
  - *Motion and interaction.* As J.
  - *Locked.* `p3.entrances.*`.
- **S2 · «Comment fonctionne l'orientation» → F «la linea V2, la discesa».** *Where:* `_orientation.html:15-30`
  (`p.home-orientation__how`, `data-locked="p3.persons.how_it_works"`), `pages.css:462-497`. *Now:* a pale teal band;
  a 24 px compass, title and lead on the left; on the right a 5-line paragraph with three «→» and a button; coverage
  18 %; only the head moves. Evidence: `director/d_fr_1440_home-orientation.jpg`, `home/s2_crops/fr_orientation_1024.png`.
  - *Composition.* The title at `--t-band` and the lead above the route. The locked sentence is cut by
    `pathways.services.how_it_works()` (D-U4, the cut that returns `None` unless it rebuilds the sentence):
    - the lead «Comment ça marche :» is the route's caption;
    - four stations with labels at 20/28;
    - the caveat «Aucun résultat…» as the route's terminal line at 17/28, always visible;
    - the call «Commencer le questionnaire d'orientation» at the route's end.
  - *Responsive.* ≥ 48 rem: 4 across; below: down the reading edge.
  - *Ground.* `--grad-brand` with the three arches of the brand's portico geometry drawn at 6 % ink (aria-hidden).
  - *Icon.*
    - Station 1 is the T1 `ile-orienta` seal (40 in 72 × 88; 56 × 68 below 64 rem), the route's origin. The 24 px
      compass above the title is gone.
    - Stations 2–4 are T2 tiles: `info` (an informative pre-assessment, never a check), `presentation`, `stamp`.
  - *Motion.* F's line draw. The CTA takes the page's arrival gold last. Hover or focus on the CTA sends the light
    along the route.
  - *Gate closed.* The neutral four steps on the same route, plus the editorial note.
  - *RTL.* The route runs right to left; French labels are centred LTR runs.
  - *Build.* `pages.css` + `_journey-passage.css`; no JS.
- **S3 · «Les parcours réguliers» → L «l'indice» (tabs).** *Where:* `_pathways.html:16-44`,
  `components/pathway_list.html:6-15`, `pages.css:499-662`. *Now:* the title and lead on the left over 400 px of empty
  column; eight rows in two columns under gold rules; at 390, 1 435 px of text; in ar the French rows read right
  column first. Evidence: `director/d_fr_1440_home-pathways.jpg`, `director/d_ar_1440_home-pathways.jpg`,
  `director/d_fr_390_home-pathways.jpg`.
  - *Composition.*
    - The title and lead above two panes.
    - ≥ 48 rem: an index (4/12; 6/12 at 768) of eight rows, each a 20 px PATHWAY glyph and the title. A stage (8/12)
      shows the selected pathway: a T2 tile 64 with its 32 px glyph, the title at 28/36, the description at 20/28 and
      «Voir le parcours».
    - < 48 rem: eight disclosure rows (button, glyph, title), all closed at first, one open at a time.
    - The foot link «Voir l'Espace Personnes» stays.
  - *Gate closed.* The four neutral families as a static index (no stage, no destination) + the existing note.
  - *Icon.* The PATHWAY map (`apps/core/icons.py:431-440`). Ink at rest; the selected row's glyph and its 2 px marker
    in `--accent-text`. The gold rules retire.
  - *Motion.* L's glide.
  - *Density.* About 45 words visible instead of 156; all eight descriptions stay in the DOM.
  - *RTL.* One index removes the reversed two-column order.
  - *Build.* `_sec-indice.css` via `pages.css`; `sezioni/indice.js` (the only section chunk on the home).
- **S4 · «PROJET PILOTE VÉNÉTIE–MAROC» → D «il panorama, lo stesso gesto» (develop variant).** *Where:*
  `_pilot.html:19-35`, `pages.css:664-720`, slots `home.pilot.cedar` / `home.pilot.marble`. *Now:* a 584 px night band;
  a 28 px title, a 2-line lead and a link over 200 px of empty night; two 243 × 304 photographs that mask and develop.
  Evidence: `home/s1_fr_1440_04_pilot.png`.
  - *Composition.*
    - A full-bleed night panel, about 82 vh from 64 rem.
    - The cedar panel at the reading edge and the marble panel at the far edge, each about 30 % wide and full height
      (new 2:3 re-crops, §8).
    - In the seam, the locked title at `--t-display` (40 → 64), then the lead and the link.
    - Phones: two stacked 3:2 bands with a horizontal seam between them, the statement under the second.
  - *Lead.* The lead is team copy (`content.py:74`) promising a sequence the band does not draw. The team rewrites its
    own lead to announce what the panel shows, with professional it/en/ar. `p3.pilot.sequence` stays on the pilot page
    and in the hero («said once»).
  - *Motion.* The cedar develops first (`entry 10%` → `cover 40%`), then the marble (`cover 25%` → `55%`), through the
    existing `reveal-colour` mechanism. A gold seam line (the en dash made visible, an identity gold) draws top to
    bottom. Still: colour, the seam drawn.
  - *Interaction.* On a fine pointer, hovering a half lowers its inner veil (a pre-painted layer's opacity).
  - *Icon.* None.
  - *Credits.* Visible.
- **S5 + S6 · «Ce que fait la plateforme, et ce qu'elle ne fait pas» + «ATTENTION AUX FRAUDES» → K «lo strato, la banda
  dell'integrità».** *Where:* `_trust.html:21-58`, `pages.css:722-795`; `_antifraud.html:14-28`, `pages.css:797-882`.
  *Now:* trust is the title on the left over 550 px of empty column and four Q&A in one column that never move.
  Anti-fraud is a white plate with a 24 px shield and a 10-line paragraph, with no motion at all. Evidence:
  `director/d_fr_1440_home-trust.jpg`, `director/d_fr_1440_home-antifraud.jpg`, `director/d_fr_390_home-trust.jpg`.
  - *Composition.*
    - One band, the two sections' anchors kept. Ground: the new masonry frame `home.integrity.stone` (§8) under a
      60 % stone veil, its credit in the corner.
    - The trust title at `--t-title` 36 and the lead above a 2 × 2 grid of plates at `--shadow-1`. Each plate holds:
      the question (17/24, 600, the plate's stretched link to its FAQ anchor `/xx/faq/#faq_visas`,
      `#faq_recruitment_agency`, `#faq_preassessment_guarantee`, `#faq_diplomas`; all four exist, verified 30 Oct);
      «Non.» as the large keyword (`--t-title`, 500, ink: the answer's own first sentence cut on its full stop at
      render, `textContent` identical, equality test); the rest of the answer (17/28), fully visible.
    - «Toutes les questions fréquentes» becomes a secondary button.
    - Under the grid stands «la protezione» at `--shadow-2` (the band's one raised surface). The adjacent-sibling rule
      `.home-trust + .home-antifraud` keeps the back office free to reorder: apart, each stands on its own.
    - Phones: one column, «Non.» at `--t-band` 28, about 820 px for the four plates.
  - *Gate closed.* The interim two lists become two plates («Ce que fait la plateforme» / «Ce qu'elle ne fait pas»);
    no keyword; the disclaimer link.
  - *Motion.* K's depth and the ground drift. «Non.» is painted from the first frame: a 2 px accent rule under it
    draws as its plate settles. Anti-fraud follows «la protezione».
  - *Icon.* Trust plates carry none, and never ✓ or ✗ (O14). The anti-fraud plate carries `ile-scudo` T1 on its top
    rule.
  - *RTL.* The grid mirrors; each plate's French text is LTR from its own start.
  - *Build.* `_sec-strato.css` via `pages.css`; no JS.
- **S7 · «Un écosystème institutionnel» → A «la campata, il colophon».** *Where:* `_ecosystem.html:19-53`,
  `pages.css:1011-1094`, slot `home.ecosystem`. *Now:* a 24 px arch mark above the title, a 6-line promoter answer, a
  464 × 309 photograph. Evidence: `director/d_fr_1440_home-antifraud.jpg` (lower half), `home/s1_fr_1440_07_ecosystem.png`.
  - *Composition.*
    - The title above the split.
    - The photograph on 7/12 at the reading edge: a new 4:3 re-crop with its lanyard redaction kept, under an arched
      top on a sill line.
    - 5/12 colophon: the label «Promoteur» (ILE Mono folio); the AGAMI name from `settings.ILE["PROMOTER"]` at
      `--t-title`; the `faq_who` answer at 17/28 with «depuis 2011» and «Italie–Maroc» as ink keywords (the `emphasize`
      filter, emphasis only); the link as a secondary button.
    - No partner slot (G6).
  - *Motion.* A's arch mask (the photograph appears through the arch silhouette widening to the frame, 900 ms), the
    1.04 → 1 settle, then the arch outline draws. Black and white rests only in the hero, and the pilot owns develop.
  - *Icon.* The 24 px `ile-arch` mark is gone; the arch is the frame.
  - *RTL.* The photograph on the right, the colophon LTR in its own box.
- **S8 · «ESPACE RÉSERVÉ» → KEEP (refined).** *Where:* `_reserved.html:13-24`, `pages.css:1096-1169`. *Now:* a slim
  night row with a 24 px gold key, the title, one sentence and «CONNEXION».
  - *Refinement.* The key becomes the T5 `ile-accesso` (32 in a 56 × 68 night arch seat, the identity gold). It turns
    90° on hover and focus of «CONNEXION» (`--ease-turn`, 320 ms; no rotation under reduced motion).
  - The row joins the footer with the night's 1 px rule. The page-only rule
    `.page-home .site-footer { margin-block-start: 0 }` lives in `pages.css`; `chrome.css` and `footer.html` are
    untouched.

### 3.2 Le projet `/xx/le-projet/` — `templates/pages/project.html`; sheet `pages/css/interior.css` · lane P2

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | night |
| moment | C (story) | paper + night figure plate |
| break | D (panorama) | full bleed |
| band | E «le porte» | stone |
| strip | foot | paper |

Evidence: `director/d_fr_1440_projet_chapters.jpg`, `director/d_fr_1440_projet_spaces.jpg`, `pages1/le-projet_fr_390.jpg`.

- **LP-0 · head «l'ingresso», arch composition → KEEP** (`project.html:14-17`, `_fronte.css`, `fronte/_arco.html`;
  Q1's H1).
- **LP-1 + LP-2 + LP-3 · «En bref» / «POURQUOI ITALY LEGAL ENTRY» / «Qui porte le projet» → C «il racconto, il
  sistema in tre stati».** *Where:* `project.html:19-51`, `.chapter` ×3 (`_pagina.css` §3). *Now:* three
  title-left/text-right bands (269 / 381 / 317 px), a 101-word paragraph, rise only (100 % translateY + opacity).
  - *Composition.* One wrapper `[data-sec=racconto]`: three `<section>` steps, each with its `<h2>` and its locked text
    (`p3.hero.body`; `p2.forum.why.title/body`; the `faq_who` answer and the promoter link), and one sticky figure.
  - *The figure* (a night plate, drawn, aria-hidden): the brand doorway enlarged, the five actors as T2a nodes in
    their audience accents (person sand, company blue, institution silver, university green; professionals in
    on-night ink), and their spokes. Its states:
    1. the whole system drawn;
    2. «Pourquoi», by sentence (the three sentences as spans of one `<p data-locked>`, cut on their full stops): the
       grey broken paths of the improvised channels → the regular route drawing through the door → the arch lighting;
    3. the promoter: the doorway's sill (its foundation) lights under the arch. The image says that the promoter
       carries the project; it is not an authority.
  - *Motion.* C's layering. *Interaction.* Scroll only.
  - *Icon.* The T2a nodes on the figure; no T1 (the arch is the brand drawing).
  - *Density.* No word removed or reordered.
  - *Phones.* The figure drawn once above the steps.
- **LP-3b · the visual break → D «il panorama».** A new frame `project.volumes` (§8: bound law volumes, spines in
  raking light, titles unreadable) after the story. Full bleed 21:9 from 64 rem, 4:5 on phones; widening + drift; the
  credit visible; no text on it. It carries the «legality» thesis of the Pourquoi.
- **LP-4 · «Les espaces de l'écosystème» → E «le porte».** *Where:* `project.html:53-71`, `.registro.spazi`
  (`_compose.css` §4). *Now:* four equal white cards whose 22 px discs do not answer hover. Evidence:
  `icons_shots/s2_fr_1440_projet_spazi_hover.png`.
  - *Composition.*
    - Four equal night door plates on stone, each a whole link: a T2a disc 40 in 64 with the audience-accent ring,
      the space name at 20/28 600, and «Espace …» with its arrow line.
    - The actor sentences stay on Réseau only (the cross-page repetition, pages1 §5.3). The foot strip carries the
      three secondary links (questionnaire, Réseau, Forum).
  - *LP-5 «La marque».* The trademark line (`p1.trademark.*`) is folded into the foot strip as its quiet last line,
    always visible.
  - *Motion.* E's stagger; the doors widen on hover and focus.

### 3.3 Projet pilote `/xx/projet-pilote/` — `templates/ecosystem/pilot.html` (+ `ecosystem/partials/pilot_flow.html`); sheet `ecosystem/ecosystem.css` · lane P1

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | night |
| moment | F route + status plate | paper |
| band | A two doors | stone |
| strip | «l'approdo» | stone, after a paper gap |

Evidence: `pages1/frame_projet-pilote_sequence_entering.jpg`, `pages1/p1_projet-pilote_sequence_fr_768.jpg`.

- **PP-0 · head «two territories» diptych → KEEP** (`pilot.html:15-18`; `p3.pilot.title/body`).
- **PP-1 · «La séquence du projet pilote» + the mandatory notice → F «il tracciato pilota».** *Where:*
  `pilot.html:20-34`, `pilot_flow.html:14-17` → `pages/partials/_linea.html` → `components/stepper.html`. *Now:* 12 px
  rings, 13 px numerals and 13–15 px labels across the column, reading like a table header. The notice is 575 px wide
  with the right half empty.
  - *Composition.*
    - The T1 `ile-pilota` seal beside the title; its sill line becomes the sequence line.
    - Eight stations: an ILE Mono numeral at 36, a T2 tile with its concept glyph, the locked capitals label.
    - ≥ 80 rem: one gently stepped row. 48–80 rem: 4 + 4 with a carriage-return segment. < 48 rem: down the reading
      edge.
    - The notice is the route's terminal **status plate** directly under it: the «attesa» register (dashed edge),
      full text, never collapsible.
  - *Glyphs* (lane S records them in `icons.PILOT_STATION`; never `ile-steps`, never a check, never a twin of a
    PATHWAY glyph, never a glyph that suggests candidate selection):
    1. `briefcase-business`;
    2. a competence-profile glyph chosen and vendored by S;
    3. `presentation`;
    4. `list-checks`;
    5. `stamp`;
    6. `ile-arch` (the page's one gold arrival node);
    7. an accompaniment glyph chosen by S;
    8. a follow-up glyph chosen by S.
  - *Motion.* F's line draw; lit stations in `--accent-mark`. *Interaction.* Hover or focus brings a label to full ink.
  - *Locked.* `p3.pilot.sequence` (8 labels, order fixed). The notice is factual UI wording and stays visible right
    after the diagram.
- **PP-2 · «Participer à la construction du projet» → A «due porte».** *Where:* `pilot.html:36-54`,
  `.card.card--action` (`_interior.css`). *Now:* a head beside one white card with two stacked buttons.
  - *Composition.* Two door plates:
    - Entreprises: night face, company-blue ring, its half of the team sentence (split at its own full stop, a team
      string), the locked primary;
    - Institutions: paper face, its half, the locked secondary.

    The help line runs under both.
  - *Motion.* **LIGHT**: on entry the two thresholds light (480 ms, the primary first); hover and focus raise them.
    The text is static.
- **PP-3 · «Pour aller plus loin» → K «l'approdo»** (the Forum tile typographic, Q4; the mission motif as bookend;
  one light sweep).

### 3.4 Parcours `/xx/parcours/` — `templates/pathways/index.html`; sheet `pathways/pathways.css` · lane P1

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| moment | B (route board) | paper |
| band | B (how it works) | brand |
| band | E grid | paper |
| band | «la protezione» | stone |

Evidence: `director/d_fr_1440_parcours_register.jpg`, `pages1/frame_parcours_filter_work.jpg`,
`pages1/p1_parcours_register_ar_360.jpg`.

- **PA-0 · head «route» → KEEP.** The folio becomes the T1 `ile-percorso` seat at the spine's top; the spine and its
  gold arrival node stay.
- **PA-1 · «Les parcours réguliers» → B «il tracciato delle famiglie».** *Where:* `index.html:36-74`,
  `fieldset.famiglie` + `ol.registro.pathway-register--numbered` (`_pathways.css:224-346`). *Now:* a sticky head with a
  24 px signpost over empty column; five pill chips; eight numbered rows in two columns. The filter hides rows
  (`display: none`). 2.39 screens at 360. In ar the reading edge splits.
  - *Composition.*
    - The origin node is the questionnaire (a T2 tile `compass` with its secondary link; the primary stays in the
      head).
    - A trunk and four lanes: Travail (01, 02, 06), Études et formation (03, 04, 07), Famille (05), Autres voies (08).
      The prescribed order shows in the numerals.
    - Each lane head: the existing family label (team string) + its new family frame (§8; 3:2, 21:9 strip on phones;
      black and white at rest, developing when the lane is chosen).
    - Station cards: the numeral, a PATHWAY T2 tile 20 in 40, the locked title and description, the arrow; each card a
      link.
    - The existing radios choose a lane: nothing leaves the layout; the count line still announces.
  - *Motion.* B's path progression. *Interaction.* The radio group; hover or focus on a card lights its lane.
  - *Icon.* The 24 px signpost leaves.
  - *RTL.* A card mirrors as a whole: numeral and French text share one reading edge.
  - *Locked.* `p3.persons.pathways` (8, order fixed).
- **PA-2 · «Comment ça marche» + its caveat → B (station links) on the brand wash.** *Where:* `index.html:76-96`,
  `ol.linea.linea--across` (`_pathways.css:98-114`).
  - *Composition.*
    - Four step plates: an ILE Mono numeral at 36, a T2 tile 40 (`compass`, `info`, `presentation`, `stamp`), and the
      fragment at 20/28.
    - Station 1 is a link to the questionnaire (`links.orientation`) and station 3 a link to /formation/; 2 and 4 stay
      text.
    - The caveat stands as the route's terminal plate at body size with the T4 info mark (not small print).
    - The whole locked sentence stays present once, visually hidden.
  - *Motion.* **STAGGER** of the four plates as they enter (60 ms), their tiles' threshold rules drawing; the route
    light only on hover or focus (it travels to the station under the hand). It differs from PA-1.
- **PA-3 · «Dans l'Espace Personnes» → E grid + «la protezione».** *Where:* `index.html:98-108`,
  `pathways/_space_links.html`, `pathways/_antifraud_callout.html`.
  - *Grid.* Five destinations with T2 tiles: `presentation` (Formation, the wide tile), `award` (Diplômes), `sprout`
    (Vivre), `circle-help` (FAQ), `book-a` (Glossaire). The help line is the grid's foot. The `ile-key` mark leaves
    (CHAPTER_OF `space-links-title` → none).
  - *Then* «la protezione» as its own K band (`p3.antifraud.*`).

### 3.5 Pathway sheets `/xx/parcours/<slug>/` (eight sheets) — `templates/pathways/detail.html` · lane P1

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| moment | I timeline + rail | paper |
| band | H «chi decide» | night |
| band | «la protezione» | stone |
| strip | L terms | paper |
| band | «la boussole» | brand |

The sheets are type-led by decision (DECISIONS §6). Their imagery is drawn: the timeline, the authority arc, the
compass. Evidence: `pages1/salaried_work_fr_1440.jpg`, `pages1/salaried_work_fr_390.jpg`, `pages1/salaried_work_ar_390.jpg`.

- **PS-0 · head (folio «Parcours régulier n/8», locked title and description, nature line, «Sommaire») → KEEP.** From
  64 rem the «Sommaire» becomes PS-1's sticky rail.
- **PS-1 · «Étapes» → I «il filo» + the page rail.** *Where:* `detail.html:71-80`, `section#etapes`. *Now:* 12 px rings
  and 17 px grey labels; ink density 0.05.
  - *Composition.* Five milestones (the CMS seed headings, `pending_legal_review`, nothing invented): an ILE Mono
    numeral at 36, a T2 tile 40, the heading at 20/28. The tiles: `compass`, `files`, `stamp`, `list-checks`,
    `ile-arch`.
  - *Rail.* ≥ 64 rem: the rail at the inline start tracks Étapes → Autorités → Avertissements → Ressources →
    Orientation with `aria-current="location"` and a scroll-timeline fill (`sezioni/spia.js`).
  - No durations, no states, no ticks.
- **PS-2 · «Autorités et acteurs compétents» → H «chi decide» (arc) on night.** *Where:* `detail.html:102-116`.
  - *Composition.* Four authority plates on an arc, each with a building glyph (T2a, neutral ink) and its Italian name
    (`lang="it"`). ILE is drawn **outside** the arc as a dotted node, captioned by the existing lead («… n'intervient
    pas auprès des autorités et ne délivre aucune autorisation»), kept whole and visible. The map itself says that ILE
    is not an authority.
  - *Motion.* The arc draws, the plates stagger; the ILE node never lights.
  - *Interaction.* A pointer light only: the plates have no URL and take no focus.
- **PS-3 · «Avertissements» → K «la protezione»** (+ the editors' warnings, when present, as plates under it).
- **PS-4 · «Ressources» → L (definitions in place) + a compact row.** *Where:* `detail.html:133-151`, `.termes`. Each
  Italian term chip is a `<details name="termini">` that opens its locked definition (`p3.glossary.terms`, its `lang`
  kept, «Voir dans le glossaire» inside). The space links become a compact row with their glyphs.
- **PS-5 · «Orientation» → A «la boussole»** (`pathways/_orientation_action.html`; the card's caution «Les décisions
  relèvent des autorités compétentes» stays).

### 3.6 Entreprises `/xx/entreprises/` — `templates/ecosystem/companies.html`; sheet `ecosystem/ecosystem.css` · lane P1

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| band | F process | paper |
| break | D panorama | full bleed |
| band | the form (preserved) | stone |
| band | A split | paper |
| strip | «l'approdo» | stone |

Evidence: `pages1/frame_entreprises_pullquote_entering.jpg`, `pages1/probe_entreprises_band_viewport.jpg`.

- **EN-0 · head «economic» → KEEP;** the folio becomes the T1 `ile-impresa`.
- **EN-1 · «Trois temps, une même démarche» → F, measured connector.** *Where:* `companies.html:34-47`,
  `blockquote.citazione--pull` (`_spaces.css:309-324`) + linea (3).
  - *Composition.*
    - The locked quote (`p1.companies.quote`) opens the band full width at `--t-title` 36/44, its rule drawn.
    - The head's rising line continues down into the band: three wide stage panels hung on one measured curve
      (`sezioni/flow.js`). Each panel: a T2 tile 40, the moment's label at 20/28, its text at 17/28.
    - Glyphs: `briefcase-business`, a construction or collaboration glyph chosen by S (not `users`, which is the family
      pathway's), `presentation`.
    - The moments are team strings (`company_moments`, CONTENT_PENDING_LEGAL_REVIEW): no procedure, delay or outcome
      added.
  - *Motion.* **PATH PROGRESSION** along the curve. The quote's rule is a line draw. The panels get no translate
    beyond 8 px.
- **EN-2 · the 21:9 band (greenhouse tunnels at dusk) → D «il panorama».** `companies.html:49`, slot
  `companies.territory`. Lane S fixes M22 so it drifts; the band widens to full bleed. It is the page's only drifting
  image.
- **EN-3 · «Recueil des besoins», the form → KEEP** (preserved, V5.22 §24; the sticky side panel stays).
- **EN-4 · «Ce que la plateforme fait, et ne fait pas» → A split of one locked answer.** *Where:* `companies.html:71-82`,
  `components/notice.html`.
  - The question becomes the band's title at 28.
  - The `faq_recruitment_agency` answer is cut at its own colon into two columns inside one `<p data-faq>` (spans,
    `textContent` identical). A vertical rule between them draws (scaleY).
  - No marks: no slash-circle and no tick, since they read as verdicts. The FAQ link is an arrow row.
  - The notice's shield painted `--brand-navy` leaves (tokens rule).
- **EN-5 · «Pour aller plus loin» → K «l'approdo».** The skyline returns low as the bookend; the pilot tile carries a
  miniature of the eight-station route (aria-hidden; E's «live diagram» principle).
- **EN-H · head of `/xx/entreprises/recueil-des-besoins/` → K «compact frontispiece».** *Where:*
  `templates/enquiries/company_needs.html:16-20`, plain `header.page-header` (`_pagina.css` §2). *Now:* a paper header,
  45 % of the first screen empty. Evidence: `pages1/recueil_fr_1440.jpg`.
  - The economic band in `_ingresso.html compact=True` (built by S; P1 wires it in the header block only): paper tone,
    the skyline and rising line at the far side, the T1 `ile-impresa` folio, the locked title and intro.
  - At most 50 vh at 1440 and one screen at 390: the formwork still starts in the first screen at 1440. The page links
    `pages/css/fronte.css` (+1 request, recorded).
  - The form is untouched.

### 3.7 Institutions `/xx/institutions/` — `templates/ecosystem/institutions.html` · lane P1

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| moment | H «l'emiciclo» | photo + night veil |
| strip | «l'approdo» | stone |

Evidence: `pages1/frame_institutions_chamber_developing.jpg`, `pages1/p1_institutions_destinataires_fr_768.jpg`.

- **IN-0 · head «civic» → KEEP;** the folio becomes the T1 `ile-istituzione`.
- **IN-1 · «Destinataires» → H «l'emiciclo».** *Where:* `institutions.html:26-37`, `p.destinataires__statement`
  (`_compose.css` §1, `_spaces.css:253-267`), slot `institutions.chamber`. *Now:* «Destinataires» twice (the chapter
  title and the sentence's first word); a 28 px sentence beside a 324 × 216 photograph.
  - *Composition.*
    - The chamber photograph as the layered ground (its develop kept), a night veil on its lower half.
    - Six glyph seats (T2a 32 in 48, the institution silver ring on night) on an assembly arc drawn over the
      photograph (aria-hidden): `map`, a commune building, `landmark`, `briefcase` (chambers), a labour-body glyph
      chosen by S (not `users`), `globe`.
    - The locked `p3.institutions.recipients` sentence whole at `--t-band` 28/36 on the plate under the arc. Its items
      are spans (`split_enumeration` at render), and «Destinataires :» stays the sentence's own head.
    - A visually hidden `<h2>` («Destinataires», team) keeps the outline. The visible duplicate is gone.
    - The help line and the link-arrow «Proposez une collaboration institutionnelle» follow (the primary stays in the
      head).
  - *Motion.* The arc draws, the seats stagger, the photograph develops.
  - *Interaction.* Hovering a seat or a phrase lights both (CSS `:has`, no JS, words once: RH-5).
- **IN-2 · «Pour aller plus loin» → K «l'approdo»** (the civic colonnade bookend).
- **IN-H · head of `/xx/collaboration/institutions/` → K «compact frontispiece»** (`templates/enquiries/collaboration_proposal.html:14-28`).
  - The civic band, compact, on paper; the T1 `ile-istituzione` folio.
  - The locked recipients sentence becomes a side annotation beside a small six-seat hemicycle drawing (aria-hidden).
  - The formwork stays in the first screen. Evidence: `pages1/collab-inst_fr_1440.jpg`.

### 3.8 Universités et formation `/xx/universites-et-formation/` — `templates/ecosystem/universities.html` · lane P1

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| moment | B «la filiera» with its destination frame | paper |

Evidence: `pages2/universites_fr_1440.jpg`, `pages2/m_universites_hover_fr_1440.jpg`, `pages2/p1_universites_fr_768.jpg`.

- **U0 · head → KEEP;** the folio's `school` becomes the T1 `ile-sapere` (this also fixes `school` vs `university`).
- **U1 · «Pour aller plus loin» (campus photo + two tiles) → B «la filiera di formazione».** *Where:*
  `universities.html:34-49`, `.scambio__inner` (`_spaces.css:269-306`), `.approdo`.
  - *Composition.* A route crosses the section from the reading edge. Three station plates, each a team kicker
    (professionally translated) and the locked title and one-line description:
    - «Avant le départ»: «Formation dans le pays d'origine» → `/parcours/training_in_origin_country/`, plus a second
      link to `/formation/#avant-le-depart`;
    - «En Italie»: «Études et formation en Italie» → `/parcours/study_and_training_in_italy/`, with «Recherche
      scientifique» branching off;
    - «Après l'arrivée»: «FORMATION APRÈS L'ARRIVÉE» → `/formation/#apres-l-arrivee`.
  - *Destination.* The campus frame, re-cropped to hands and folder with no redaction (§8), stands at the route's end
    as the destination panel (6/12), overlapping the last plate by 48 px. The help line is the route's footnote.
  - *Icon.* T2 tiles 40: `earth`, `university` (`flask-conical` on the branch), `presentation`. The route ends on an
    `ile-arch` node (the page's arrival gold).
  - *Motion.* Path progression. The destination frame develops (`bw-scroll`) as the route arrives.
  - *Interaction.* Hover or focus on a plate lights the route up to it.

### 3.9 Formation `/xx/formation/` — `templates/pathways/training.html` · lane P1

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| moment | I «la traversata» | paper |
| band | E grid | paper |
| band | «la protezione» | stone |
| band | «la boussole» | brand |

Evidence: `pages2/formation_fr_1440.jpg`, `pages2/m_formation_develop_fr_1440.jpg`, `pages2/p1_formation_fr_768.jpg`.

- **F0 · head → KEEP;** the folio becomes the T1 `ile-formazione`. The «Nature» meta row stays.
- **F1 · «Premier temps / Second temps» → I «la traversata».** *Where:* `training.html:25-57`,
  `ol.linea.linea--phases` (`_journey-passage.css:29-226`).
  - *Composition (≥ 64 rem).*
    - Two columns joined by one horizontal crossing line from an `earth` node (origin country) to an `ile-arch` node
      (Italy, the arrival gold).
    - Each column holds its kicker, title, text and link, with its frame under the line: station 1 the new
      `training.before` (§8), station 2 the existing `training.after` (microscopes).
    - Station 1's notice («… aucune attestation n'a valeur d'approbation administrative.») is a side annotation
      docked to its frame's edge, always visible.
    - The locked `p3.training_after.body` stays whole; its first sentence is set larger in place (emphasis, not a
      cut). Station 1's text is CONTENT_PENDING_LEGAL_REVIEW wording: untouched.
  - *< 64 rem.* The line down the reading edge, each frame at 3:2 after its text, the notice inline. The 34 rem
    measure applies from 48 rem (the 768 overlong line is fixed).
  - *Motion.* The crossing line draws (scroll-linked). Frame 1 develops as the line leaves it, frame 2 as it arrives.
    The annotation slides ≤ 8 px from the reading edge.
- **F2 · «Dans l'Espace Personnes» → E grid** (Diplômes as the wide tile); the `ile-key` mark leaves.
- **F2b · the anti-fraud callout → K «la protezione»** (its own band).
- **F3 · «Orientation» → A «la boussole».**

### 3.10 Diplômes et titres `/xx/diplomes-et-titres/` — `templates/pathways/diplomas.html` · lane P1

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| moment | F process + C sticky aside | paper |
| band | «la protezione» | stone |
| band | E grid | paper |
| band | «la boussole» | brand |

Evidence: `pages2/diplomes_fr_1440.jpg`, `pages2/p1_diplomes_fr_1024.jpg`, `pages2/p1_diplomes_ar_1024.jpg`.

- **D0 · head → KEEP;** the folio becomes a typographic label: there is no custom mark for diplomas, and a Lucide disc
  in the folio's seat would be the old device.
- **D1 + D2 · «Les démarches, étape par étape» + «Qui décide ?» → F «le dossier, pièce par pièce» + a C sticky
  aside.** *Where:* `diplomas.html:34-64`, `ol.linea.diploma-steps`, `DIPLOMA_STEPS` (all pending,
  `apps/pathways/services.py:398-421`). *Now:* five grey labels; 7 % coverage at 1440; 70 % empty at 1024.
  - *Composition.*
    - Five large stations (columns 1–8): a numeral at 36 in an outlined node, the label at 20/28, the T2 glyphs
      `files`, `languages`, `badge-check`, `file-badge`, `stamp`.
    - Stations 3–5 carry a detail plate holding the locked definition of their term (`p3.glossary.terms`, verbatim)
      and a link to the term page. Stations 1–2 carry none: nothing is invented.
    - From 64 rem each station with a plate is an `aria-expanded` button, one open at a time, the first open at load.
      On phones all are open (L, disclosure form).
    - The dashed «pending» node ring and a quiet caption in the meta-row voice keep the status explicit, never by
      colour alone.
    - «Qui décide ?» becomes the sticky aside (columns 9–12 from 64 rem): a raised stone plate, a 48 px `stamp` tile,
      the h2, and the statement at 20/28 as an emphasised legal statement (team wording with legal weight, verbatim).
      On phones it closes the process inline.
  - *Motion.* The line draws down, 120 ms a station. Each plate opens by a clip-path from its node's side. The aside's
    shadow layer goes from 0 to 1 while it is pinned. The stamp presses once (1.04 → 1, 200 ms, `--ease-turn`) the
    first time the plate pins: semantic, never repeated.
- **D2's callout → K «la protezione».**
- **D3 → E grid** (Formation as the wide tile; `ile-key` leaves). **D4 → A «la boussole».**

### 3.11 Réseau `/xx/reseau/` — `templates/pages/network.html`; sheet `pages/css/interior.css` · lane P2

| Rhythm | Section | Ground |
|---|---|---|
| moment | the head as H | night |
| strip | «l'approdo» | stone |

Evidence: `director/d_fr_1440_reseau_head.jpg`, `director/d_fr_1440_reseau_actors.jpg`, `pages1/p1_reseau_actors_ar_360.jpg`.

- **RE-0 + RE-1 + RE-2 · head ring + «En bref» + «Les acteurs de l'écosystème» → H «la mappa» in the head.** *Where:*
  `network.html:13-44`, `fronte/_rete.html` (`_fronte.css:993`), `ul.registro--glyph.actor-list`
  (`_institutional.css:7-25`). *Now:* the strongest icon composition on the site, a night ring of five actors around
  the shared-table photograph, is static. Below it, the same five actors are told again as five hairline rows, and
  the «En bref» sentence is a separate chapter.
  - *Composition.*
    - At rest the ring looks exactly as today.
    - Its five nodes become the map's controls: anchors in the HTML layer over the drawing, upgraded to tabs. The
      ring's lines and circles stay SVG, aria-hidden.
    - The **panel docks in the head's reading column** under the lead (≥ 64 rem) or under the ring (phones). Its hub
      state is the «En bref» sentence (`p3.hero.body`, moved from RE-1, the ring's caption). Selecting an actor shows
      that actor's sentence (NETWORK_ACTORS, team strings), its space link and its glyph (T2a 40 in 64).
    - Escape, or the hub photograph, returns to the hub state.
    - The folio's `users` glyph leaves: the ring is the page's T1.
    - The gate logic is unchanged. Under each G3 state the hub caption renders exactly what RE-1 rendered, so
      `apps/pages/tests/test_prescribed_fragments.py::test_no_phase3_fragment_is_public_while_gate_closed` still holds
      for `reseau/`.
  - *No-JS.* The five entries listed under the hub caption.
  - *Motion and interaction.* As H. The LCP photograph at the hub is untouched: the module is a dynamic chunk after load.
  - *RTL.* The ring mirrors.
  - *Build.* `fronte/_rete.html` (P2) + `_sec-mappa.css` via `interior.css` + `sezioni/mappa.js`.
- **RE-3 · «Pour aller plus loin» (Forum, Le promoteur; partners only under G6) → K «l'approdo»** (the network nodes
  as bookend).

### 3.12 Contact `/xx/contact/` — `templates/pages/contact.html`; sheets `pages/css/interior.css` (`_canali.css`) · lane P2

The contact architecture is preserved (V5.19, V5.21 option B):
- the channels, their URLs from SiteSettings / `ILE_WHATSAPP_NUMBER` (never in a tracked file);
- the accessible names, `<bdi dir="ltr">`, the ≥ 44 px targets;
- a blank WhatsApp number is never announced.

Only the composition changes.

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| band | E channel board | stone |
| band | E «le porte» | paper with night doors |

Evidence: `pages2/contact_fr_1440.jpg`, `pages2/m_contact_hover_fr_1440.jpg`, `pages2/p1_contact_fr_1024.jpg`.

- **C0 · head «la carta» → KEEP.** The folio's `map-pin` becomes a typographic label. C1's sentence («Tous les
  formulaires du site sont acheminés vers cette adresse.») becomes the caption of the head's address, so the address
  is said once in the body.
- **C1 + C2 + C3 · «Par e-mail» / «Par téléphone et WhatsApp» / «Par le formulaire de contact» → E «il centralino»
  (one section).** *Where:* `contact.html:22-56`, `pages/partials/_canali.html`, `_canali.css`.
  - *Composition.* One channel board with three plates on the existing plate idiom:
    - the Numéro vert (wide; `phone` in its 48 px disc);
    - WhatsApp (its own glyph and the word «WhatsApp», never a second ordinary number);
    - the contact form (`message-square-text`; the plate is the link «Ouvrir le formulaire de contact»; with G2 closed
      the G2 notice stands in the same plate, in the pending register).

    The heading «Par téléphone, WhatsApp ou formulaire» (team copy, professional translation; it names only the
    channels the settings hold) sits in the board's first row.
  - *Privacy.* **C5 «Vos données»** attaches as the board's legal foot line, at the same visibility.
  - *Motion.* E's stagger: the discs' rings draw. The existing fill response becomes **hover = focus**: the disc fills
    lagoon on `:focus-visible` too.
  - *Icon.* The three bare 24 px marks leave, which removes the phone duplicate at 390.
- **C4 · «Une demande précise ?» → E «le porte», joined by a drawn hub line.** *Where:* `contact.html:58-71`, labels
  `apps/pages/services.py:988-998`.
  - Three night door plates (`.porta` idiom), each with its T2a audience disc (`building`, `institution`,
    `university`; audience-accent rings, never one gold) and its existing dedicated-form label.
  - A hub line carrying the h2 draws through the three doors (LINE DRAW; it differs from the board's stagger).
  - Hover and focus draw the door's accent foot rule (scaleX 0.18 → 1).

### 3.13 FAQ `/xx/faq/` — `templates/faq/index.html` + `faq/_item.html`; sheet `cms/lettura.css` · lane P2

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| moment | L explorer | paper |
| strip | E «il rimando» | stone |

Evidence: `pages2/faq_fr_1440.jpg`, `pages2/m_faq_open_fr_1440.jpg`, `pages2/spot_faq_it_1440.jpg`.

- **Q0 · head with the search plate → KEEP.**
- **Q1 · «Général» → L explorer (master–detail).** *Where:* `faq/index.html:66-79`, `details.accordion__item.faq-item`.
  *Now:* «Général» alone in a 400 px sticky column beside nine questions.
  - *Composition (≥ 64 rem).*
    - The nine locked questions as a list (5/12); the active one carries a reading-edge rule that draws.
    - An answer plate (7/12, sticky under the letterhead) holds the answer at 20/28, its links as chips, the date and
      the permalink, and the T1 `ile-domande` small seal in its corner.
    - The first question is active at load; the hash follows (the existing permalinks and the home's trust links keep
      working).
    - «Général» becomes a small eyebrow while it is the only category.
    - The fraud question (`faq_guaranteed_visa_offer`) carries an ink reading-edge rule and the `ile-scudo` T2 mark.
  - *Phones and no-JS.* Native `<details name="faq">`, one open at a time.
  - *Motion.* L's glide; the answer crosses in by clip-path (≤ 320 ms; keyboard 0 ms).
  - *Locked.* `p3.faq.items`.
- **Q2 · «Pour aller plus loin» → E «il rimando»:**
  - Glossaire (`book-a`);
  - Attention aux fraudes (`ile-scudo` small, ink);
  - Contact (`message-square-text`, the help question as its label).

### 3.14 Glossaire `/xx/glossaire/` + the term page `/xx/glossaire/<term>/` — `templates/glossary/{index,_entry,term}.html` · lane P2

| Rhythm (index) | Section | Ground |
|---|---|---|
| head | KEEP | paper |
| band | L rail + E «il lessico» | paper |
| strip | E «il rimando» | stone |

| Rhythm (term page) | Section | Ground |
|---|---|---|
| head + plate | compact band + K «la scheda» | paper |
| strip | the chip rows | paper |

Evidence: `pages2/glossaire_fr_1440.jpg`, `pages2/m_glossaire_scroll_fr_1440.jpg`, `pages2/glossaire-terme_fr_1440.jpg`.

- **G0 · head with the search plate → KEEP.**
- **G1 · the A–Z band → L scroll-spy rail.**
  - An indicator plate glides between the letters as the register scrolls; the active letter takes `--accent-text`
    (200 ms). This uses `sezioni/spia.js`.
  - `aria-current="true"` on the letter in view, announced only on focus.
  - **Defect fixed:** the letter heads leave the sticky side column, so the A–Z band no longer covers half a letter.
- **G2 · the register → E «il lessico».**
  - Ten term cards in two columns (three from 80 rem) under large letters set in the flow (`--t-display`, 500,
    `--text-3`).
  - Each card holds:
    - the Italian term at `--t-band` 28 (`lang="it"`; the card's heading and link);
    - the locked definition at 17/28;
    - «Où le rencontrer» chips (team label): the pathways that use the term, from live data
      (`GLOSSARY_TERMS_BY_PATHWAY`, `apps/pathways/services.py:80-89`, inverted in the glossary view), each labelled
      with its locked pathway title.
  - *Motion.* **STAGGER**: each card's reading-edge rule draws by column and the chips catch the light. No text is
    masked.
- **G3 → E «il rimando»** (`circle-help`, `signpost`, `ile-scudo` small).
- **T0 + T1 · the term page → the compact `learning` band + K «la scheda».**
  - The page takes the frontispiece band in its compact form (it links `pages/css/fronte.css`, +1 request recorded)
    with the T1 `ile-lessico` folio.
  - A raised definition plate holds the Italian term at `--t-display`, then the locked definition set as a dictionary
    entry. A drawn rule separates them; no character is added.
  - A large outlined initial behind the plate (aria-hidden).
  - The source and verification facts as a side annotation; «Définition à caractère informatif.» stays visible.
  - «Termes liés» and «Où le rencontrer» as two chip rows; the back link as a secondary button.
  - *Motion.* **DEPTH** (the plate settles over its shadow layer) + hairlines drawn to the related chips.

### 3.15 Vivre en Italie `/xx/vivre-en-italie/` — `templates/living/index.html` · lane P2

| Rhythm | Section | Ground |
|---|---|---|
| head as moment | D panorama | full bleed |
| band | E «pour s'installer» | paper |

Evidence: `pages2/vivre_fr_1440.jpg`, `pages2/vivre_fr_390.jpg`.

- **V0 + V1 · the head (locked title, 53-word locked lead) + the 21:9 street band → D «il panorama».** *Where:*
  `living/index.html:20-25`, `fronte-wrap[data-fronte=territory]`, slot `living.street` (the LCP). *Now:* the right
  half of the head empty; the page's only image is still; 1.7 viewports in all.
  - *Composition.*
    - The h1 stays in its band. The street frame follows it full bleed (21:9, then 16:9 from 64 rem, 4:5 at 390),
      outside the `fronte-wrap`, so the change lives in `templates/living/index.html` and the page sheets (P2) and
      in `.panorama` (S). No `_fronte.css` rule changes; a `.fronte__wide` rule left unused goes in S-close.
    - The locked lead sits on an opaque paper plate (no glass, SH-5) overlapping the image's lower third from 64 rem,
      with the T1 `ile-vivere` seal beside the title.
  - *Motion* (allowed on an LCP: no mask, no opacity). Controlled scale 1.04 → 1 over 1 200 ms after the first paint;
    the M22 drift from 48 rem; one light sweep as it leaves the viewport.
- **V2 · (missing) the page's close → E «pour s'installer», built only from what exists.**
  - «FORMATION APRÈS L'ARRIVÉE» (locked title) → `/formation/#apres-l-arrivee`.
  - Two locked glossary terms, «Permesso di soggiorno» and «Codice fiscale», as term tiles with their locked
    definitions → their term pages.
  - The FAQ.

  Q8 holds: no theme card, no «coming soon». Reviewed themes take this place automatically through the existing
  publication model.

### 3.16 Forum `/xx/forum/` — `templates/forum/index.html` → `forum/partials/{hero,presentation,cta_row}.html`; sheet `forum/forum.css` · lane P2

Q4: no stock photograph as the Forum, no invented content. Q5: no archive photograph. The Forum's imagery is drawn.

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP + drawing | night |
| band | A typographic split | paper |
| band | I | paper |
| moment | H | night plate |
| band | K actions | stone |

Evidence: `pages2/forum_fr_1440.jpg`, `pages2/m_forum_spread_rise_fr_1440.jpg`, `pages2/p1_forum_fr_360.jpg`.

- **FO0 · night head → KEEP + its drawing.** The T1 `ile-forum` (a cavea facing the speaker's arch) drawn at display
  scale on the band's far side, once (`fronte-draw`), with the night threshold light (the page's arrival gold). The
  page without photographs then has its image.
- **FO1 · «QUI SOMMES-NOUS» + «POURQUOI ITALY LEGAL ENTRY» → A, typographic.** *Where:* `presentation.html:14-25`,
  `.forum-pair` (`_forum.css:378-422`).
  - Left 6/12: the opening clause (up to its first comma, cut at render with an equality test) at `--t-band` 28/36,
    the rest at 17/28.
  - Right 5/12: the paragraph's last sentence set in place as the emphasised statement (`--t-band`, a 2 px accent rule
    at its reading edge). It is never duplicated as a pull-quote.
  - A hairline divider draws top to bottom as part of the head's sequence (the section is in view at load), and one
    light passes across the statement.
- **FO2a · «QU'EST-CE QUE LE FORUM» + «OBJECTIFS» → I «dal dialogo ai progetti».** *Where:* `presentation.html:27-45`,
  `.forum-spread` (`_forum.css:425-470`).
  - Left 5/12, sticky: «what» and its three paragraphs.
  - Right 7/12: «OBJECTIFS» as a vertical line of eight clause-stations. They are the one locked sentence cut on its own
    « ; » in order, with its punctuation kept. Reading the stations top to bottom reads the sentence (words once).
  - The arrival node, the last clause, carries the `ile-forum` T2 mark and takes the gold light once.
  - *Motion.* Scroll progression.
- **FO2b · «À QUI S'ADRESSE-T-IL» → H on a night plate (the moment).**
  - The nine actors of the locked sentence are its own spans placed on a ring around the Forum hub, clockwise in
    sentence order (counter-clockwise in ar), punctuation kept in `--text-on-night-2`.
  - The four that name an ILE audience carry its T2a glyph (20 in 40). There are no links inside the locked sentence.
  - *Motion.* Spokes draw from the hub; nodes settle 0.92 → 1, 60 ms apart.
  - *Phones.* A vertical constellation (the hub on top, the nodes in two columns).
- **FO3 · «Participer et collaborer» → K on stone** (from night: this removes the night–paper–night sandwich, RH-8).
  *Where:* `cta_row.html:14-38`.
  - Two raised action plates, each with its audience disc: `building` (company accent) for the pilot interest,
    `institution` for the collaboration.
  - The locked labels are the title-buttons; the help line is the foot.
  - A faint `ile-forum` drawing behind.
  - *Motion.* Depth.

### 3.17 AGAMI `/xx/agami/` — `templates/pages/agami.html` · lane P2

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | paper, colonnade |
| band | A identity | paper |
| band | K «la targa» | night plate |
| strip | «l'approdo» | stone |

Q5: no photograph. Evidence: `pages1/agami_fr_1440.jpg`, `pages1/agami_ar_1440.jpg`.

- **AG-0 · head «civic», name composition → KEEP.**
- **AG-1 + AG-2 · «Le promoteur du projet» + «Qui est derrière Italy Legal Entry ?» → A «la targa d'identità» + one
  disclosure.**
  - Inline start: a drawn architectural plate (the head's colonnade motif cropped at section scale on a sill;
    aria-hidden, no words).
  - Inline end: `p2.forum.who.body` whole at 20/28, with «depuis 2011» and «Italie–Maroc» emphasised in place.
  - AG-2's near-identical `faq_who` becomes a disclosure row under it, closed by default; both locked texts stay
    unchanged and in the DOM.
  - *Motion.* The plate is revealed from the reading edge (MASK, 900 ms) and the colonnade line draws.
- **AG-3 · «Identification et contact» → K «la targa».**
  - The address as the action at 28 px, with its at-sign T2 disc (the contact page's idiom).
  - The identification sentence as a side annotation, **pending §11**: it points to an unpublished legal notice.
- **AG-4 → K «l'approdo»** (the colonnade bookend).

### 3.18 Attention aux fraudes `/xx/attention-aux-fraudes/` — `templates/pages/antifraud.html` · lane P2

| Rhythm | Section | Ground |
|---|---|---|
| head | KEEP | the notice panel |
| band | A split | paper |

Evidence: `pages2/fraudes_fr_1440.jpg`.

- **AF0 · head with the locked notice as its panel → KEEP;** the folio's `shield-alert` becomes the T1 `ile-scudo`.
- **AF1 + AF2 · «Signaler une offre suspecte» + «S'informer sur les voies régulières» → A «segnalare · informarsi».**
  - Left 5/12: the report plate. The sentence leads; the address is the plate's action (a 48 px at-sign disc, the
    address at 22 px), with an ink reading-edge rule that draws.
  - Right 7/12: three route tiles:
    - `circle-help` with the locked question `faq_guaranteed_visa_offer`;
    - `signpost` («Espace Personnes : les parcours réguliers»);
    - `book-a`.
  - **No authority, police, embassy or portal link is added** (the template's legal comment).

### 3.19 Academy — its public entry `/xx/compte/login/` · lane S (one rule)

The Academy has no public page by design. It stays hidden while no course is published (DECISIONS §8). Q7 forbids a
promise of a capability that is not live. No public Academy page is created. The public surfaces of the training theme
are /formation/ and /universites-et-formation/.

The entry «Il varco» (form, door stage, Lume) is preserved. **The one change:** the eyebrow key, a 14 px brand-gold
glyph on paper at 2.37:1 (`apps/accounts/static/accounts/entrance.css:276`), becomes a T5 key at 20 px in `--text-1`.
No gold glyph on paper (§4.4).

---

## 4. Icon Treatment V2

### 4.1 Rules

1. An icon is drawn at the scale of its composition. It belongs to the section's architecture (it starts a route,
   holds a light, frames an image, stands on a sill) or it is not drawn. **No glyph is stacked above a title.**
2. One container per meaning:

   | Container | Meaning | Tier |
   |---|---|---|
   | arch seat | a theme | T1 |
   | arch seat | the brand | T5 |
   | tile | a concept | T2 |
   | disc | an actor | T2a |
   | ring | a status | T4 |
   | bare | a utility | T3 |

3. Colour comes from the context. Gold comes from a budget (§4.5).
4. Motion only where it explains: **draw** (a theme arrives), **light** (a theme answers its action), **lead** (a route
   leaves the theme), **turn** (the key unlocks, the needle settles, a disclosure opens). Icons never fade-and-rise,
   loop, bounce or float.
5. Hover equals keyboard focus. Reduced motion, `html.rm` and keyboard input see the final state at once.

### 4.2 Tiers

| Tier | Role | Glyph in container (1440 / 1024 / 390) | Stroke | Interaction | Motion | Limit |
|---|---|---|---|---|---|---|
| **T1 seal** | a page's or a section's theme | body: custom mark 40 / 36 / 32 in an arch seat 72 × 88 / 64 × 78 / 56 × 68; the small seat (head folios, «la protezione»): 32 in 56 × 68 at every width | 2 px (40–48), 1.75 px (32–36) | the threshold light answers the section's primary action (`--light` 0 → 1 on `:hover`/`:focus-visible` via `:has()`) | draw once: arch, then mark, then route line | ≤ 1 per viewport, ≤ 3 per page (head included) |
| **T2 tile** | a concept in a station, tile, plate or index | 24 in 48 / 24 in 48 / 22 in 44; index rows 20; stage 32 in 64 | 1.5 px (≤ 24), 1.75 px (32) | the tile's threshold rule runs 40 % → 100 % and the glyph shifts 2 px along the reading direction, on hover and focus alike | none on scroll (its section carries the entrance) | ≤ 6 per group; a register of named entities is all or nothing (§4.10) |
| **T2a disc** | an actor (person, company, institution, university, professional) | 20 in 44 (maps); 40 in 64 (doors, panels) | 1.5 px | the ring thickens 1 → 2 px; its link line lights | link lines draw on entry or selection | — |
| **T3 utility** | arrows, chevrons, close, search, eye, external | 16; 20 in buttons | 1.5 px (the hero's 1.8 / 2.25 px recorded as its display weight, the one exception) | 3 px directional shift (mirrored); the disclosure turns 180° | none | — |
| **T4 status ring** | a state («i cerchi»), notices | 14–16 in chips; 20 in notices | 1.5 px | none | on a state change only: 240 ms, `--ease-enter` | never gold |
| **T5 identity** | the key, the arch, the mark | 16 (header plate, unchanged); 20 (login eyebrow); 32 (reserved row) | 1.5 px; 2 px at 32 | the key turns 90° on hover and focus of its own action | Lume unchanged | gold budget |

### 4.3 Containers

- **Arch seat** (T1, T5): `templates/components/sezioni/sigillo.html` + `static/css/v5/_sigillo.css` (page-only).
  - *Shape.* A rectangle whose top is a full semicircle (radius = width / 2), standing on a **sill line** that runs
    12 px past each side. The sill is mandatory: it keeps the arch from reading as a headstone. The 56 px floor holds.
  - *Face.* Paper: `linear-gradient(180deg, var(--surface-raised), var(--surface-sheet))`. Night:
    `linear-gradient(180deg, var(--surface-night-sheet), var(--surface-night))`.
  - *Edge.* 1 px `--line-rhythm` (paper) or `--line-night-soft` (night), with a 1 px inner highlight at the crown.
  - *Threshold light.* A radial gradient at the sill. Paper: `--accent-mark` 10 % → 22 % with `--light: 1`. Night: oro
    14 % → 28 %, the one gold use for T1.
  - *Integration.* The sill continues as the section's route line, or as the head label's rule (folios).
- **Tile** (T2): 48 px square at `--radius-md` (the «three corners a screen» rule: 4 · 6 · full). A **threshold rule
  at the foot** in the context accent runs to 100 % when its owner is active, and continues as the card's own bottom
  rule.
- **Disc** (T2a): full radius with a 1 px ring. On night the ring takes the **audience accent** (`--aud-persona`,
  `--aud-impresa`, `--aud-istituzione`, `--aud-universita`; professionals take `--accent-night`). On paper the ring is
  `--line-structure`: audience colours are allowed on night and over photographs only.
- **Ring** (T4): unchanged. **Bare** (T3).

### 4.4 Colour by context (tokens only)

| Context | Glyph | Container face / edge | Accent (interactive, threshold, route) | Gold |
|---|---|---|---|---|
| Paper | `--text-1` | `--surface-raised` / `--line-rhythm` | `--accent-mark` (lines), `--accent-text` (active glyph) | never on a glyph |
| Brand wash | `--text-1` | `--surface-raised` at 80 % | `--accent-mark` | the page's one arrival node only |
| Night | `--text-on-night-1` | `--surface-night-sheet` / `--line-night-soft` | `--accent-night`; audience accents on actor discs and doors | identity (the key), a T1 threshold light, the arrival node |
| Over a photograph | `--text-on-night-1` | `--plate-night-photo` | `--accent-night` | no |
| Status | `--tone-*-mark` / `--tone-*-text` | `--tone-*-bg` | — | never |

Never a brand colour on an icon (`tokens.css:190`): the Entreprises notice's `--brand-navy` shield leaves.

### 4.5 The gold budget (page bodies)

**At most 2 gold elements per viewport at rest in a page body; 0 added by hover.** Gold in a body means one of four
things only:

1. identity (the key);
2. **one arrival per page** (a route's end node, or the T1 threshold light on night);
3. the home pilot's seam (the hero's light continued);
4. the hero's own route continuing into H0.

**What changes in the bodies:**

| Today | V2 | File |
|---|---|---|
| The pointer spotlight in oro-300 on paper cards and links | `--accent-mark` at 10 %; oro only on the night door plate | `_reveal.css` M21 |
| Gold rules drawn under pathway and programme rows | retired with the registers; route nodes in `--accent-mark`, the end node gold | `_reveal.css` M20 |
| Bare marks and folio discs | T1 / T2 / T2a per §4.2 | partials |

The **chrome is not touched in V5.22.** Its gold (menu hover, lunetta halo, mobile sheet door disc and channel glyphs)
belongs to the preserved navbar family (§24) and is recorded in §9.8. The heads keep their approved light and motif
nodes.

### 4.6 Stroke

- The ILE hand stays: non-scaling stroke, square caps, miter joins, `currentColor`, Lucide geometry as donor.
- Weights: 1.5 px for 14–24 px, 1.75 px for 32–36 px, 2 px for 40–48 px.
- **Custom marks are drawn on a 48-unit grid with 2 px lines.** Every negative space is at least 3 units at 48. A
  24-grid Lucide glyph is never scaled up to 40 px.
- One weight per tier per screen.

### 4.7 Motion and interaction (exact values)

| Motion | Applies to | Values | Off when |
|---|---|---|---|
| Draw | T1 arch, mark, route line; T2a link lines | `pathLength="1"`, `stroke-dashoffset` 1 → 0. Arch: `--motion-draw`, `--ease-sine`. Mark: `--motion-slow`, delayed 300 ms. Route: `--motion-draw`, delayed 600 ms. The mark's 12–18 % tone fades in last over `--motion-standard`. Once, on the section trigger (head folios: in the head's own sequence at load) | reduced motion, `html.rm`, keyboard, print: drawn at rest |
| Light response | the T1 threshold; the T2 threshold rule | `--light` 0 → 1 over `--motion-emphasized`, `--ease-enter`, driven by `:has()` on the section's primary action (`:hover`, `:focus-visible`) | reduced motion: an instant step; forced colours: none |
| Route progression | a T1 sill feeding a route | the line leaves the sill; stations light in order (120 ms each) | as above |
| Directional shift | T2 glyphs in links; T3 arrows | T2 2 px, T3 3 px; `--motion-standard`, `--ease-enter`; mirrored | keyboard: 0 ms |
| Semantic turn | the key (T5); the `ile-orienta` needle; disclosures | key −90° about its bow, `--motion-emphasized`, `--ease-turn`, back on leave; needle −25° → rest once after its draw (`--motion-slow`, `--spring-soft`); chevron 180° | reduced motion: no rotation |
| Status draw | T4 | 240 ms, `--ease-enter`, on a state change only | reduced motion |

**Removed:** `reveal-mark` on icons (`_reveal.css:214-242`, opacity + 8 px). S keeps it alive only on the
not-yet-migrated pages until S-close.

### 4.8 Integration into compositions

| Integration | What it is | Patterns |
|---|---|---|
| Arch + route | the T1 at the route's origin; its sill becomes the route | F, B, I (home S2, PP-1, PA-0 spine) |
| Card head with threshold | the T2 tile's foot rule = the card's bottom rule | E, L |
| Actor ring | T2a discs on a ring around a hub; spokes light on selection | H |
| Layered light | a T1 on night with its threshold light spilling onto the band | K, D (Forum head, reserved row) |
| Sequence | numerals mark stations of a real sequence; T2 tiles name the phases | F, I |
| Frame | the brand arch used as an image's frame | A (home S7) |
| Sill | a T1 standing on a plate's rule | K «la protezione» |

### 4.9 Custom ILE marks to draw (13)

Common construction:
- **Grid and anchor.** A 48-unit grid with a 4–44 live area, anchored on the brand doorway: `ile-arch`'s outer arch
  and inner opening on the sill, at 2× its 24-unit coordinates.
- **Fill.** The only fill is the doorway's 12–18 % tone.
- **Detail.** At most three inner details; legible at 32 px; no letters (except the glossary's Latin «A»).
- **Delivery.** Inline SVG in their T1 use: one partial per mark, each stroke `pathLength="1"`, about 600 B each.
  A T2-size copy goes into the page-only sprite `static/img/icons-marks.svg` (≤ 16 KiB). `icons.svg` and
  `icons-domain.svg` stay untouched.
- **RTL.** Marks never mirror, except a drawn route arrow inside a mark.

| # | Id | Concept and use | Brief | Purposeful motion |
|---|---|---|---|---|
| 1 | `ile-orienta` | orientation: home S2 station 1; «la boussole» (display scale) | the doorway, and inside its toned opening a two-headed compass needle at 45°, its north tip touching the crown | draw, then the needle settles from −25° |
| 2 | `ile-percorso` | the regular pathways: the Parcours head folio | three treads rising from the sill's start corner into the inner opening of an outer arch drawn as its arc only | treads draw one after another (3 × 120 ms) |
| 3 | `ile-impresa` | companies: the Entreprises head; the Recueil compact head | a three-tooth sawtooth roof over a façade whose central bay is the toned arch opening, on the sill | draw; the opening's tone deepens 12 → 24 % on the CTA's hover and focus |
| 4 | `ile-istituzione` | institutions: the Institutions head; the Collaboration compact head | a low 30° pediment over four columns, the central intercolumn the toned arch opening, on a stylobate line | pediment first, then the columns (60 ms apart) |
| 5 | `ile-sapere` | universities: the Universités head | an open book whose gutter rises into a small toned arch | the pages draw outward from the gutter |
| 6 | `ile-formazione` | training, before and after: the Formation head | two arches on one sill (a smaller one for before departure, the full doorway for after arrival) joined by a route line with a node between them | the line draws from the first arch to the second; the node lights |
| 7 | `ile-forum` | the Forum Vénétie–Maroc: the Forum head (display scale), FO2a arrival, FO3 drawing | a cavea (three concentric half-arcs) facing a small arch on the sill; replaces the cliché handshake in heads | tiers draw outer to inner; then the light at the arch |
| 8 | `ile-pilota` | the pilot project: PP-1 | two arches facing each other across one sill (a Venetian ogee and a horseshoe), joined by one route arc above the sill; no flags, no letters | the arc draws from the first arch to the second; never mirrored |
| 9 | `ile-scudo` | protection: «la protezione» everywhere, the Fraudes head, the FAQ fraud question, the «rimando» tiles | a shield outline whose inner field is the key's keyhole (bow ring + short shaft); ink only | the keyhole tone deepens on the link's hover and focus; no shake, no pulse |
| 10 | `ile-accesso` | access: the home reserved row | the key standing in the doorway's opening, its bit toward the sill (Lume's first frame at icon scale) | turns 90° on hover and focus of «CONNEXION» |
| 11 | `ile-domande` | the FAQ answer plate | the doorway whose inner opening continues into a question-mark hook; the dot sits on the sill | draw; the dot last |
| 12 | `ile-lessico` | the glossary term page's folio | a page outline whose top-start corner holds a small arch with a Latin «A» | draw |
| 13 | `ile-vivere` | living in Italy: the Vivre head plate | a low roofline of three pitched houses, the central door the toned arch opening, a two-leaf sprout at its sill | the roofline draws, then the sprout rises 2 units |

**Deliberately not custom:**
- the contact channels (Lucide's at-sign, phone and message glyphs read at once);
- the Academy (its `book-open` belongs to the console);
- statuses, utilities and the four audience glyphs (already ILE or Lucide, governed by the registry).

`ile-rete` and `ile-missione` from ICONS §5 are not drawn: their places are taken by the Réseau ring and Le projet's
story figure.

### 4.10 Registry, a11y, RTL, guards

- **Registry** (`apps/core/icons.py`, lane S):
  - `MARKS` maps concept → mark id, tier and floor (32);
  - `CHAPTER` / `CHAPTER_OF` stay as the concept registry, and `chapter_mark` renders nothing in V2 heads;
  - `space-links-title` → none (the `ile-key` misuse ends);
  - the Universités folio becomes `ile-sapere` (the `school` slip ends);
  - the Réseau folio's `users` leaves;
  - `PILOT_STATION` and the pending choices of §3.3, §3.6 and §3.7 are recorded here.
- **A11y.** T1, T2 and T2a are decorative (`aria-hidden`); the words beside them carry the concept. A T1 never stands
  in for a heading.
  - Glyph against its face: ≥ 4.5:1.
  - A meaningful container edge: ≥ 3:1, or the container is decorative.
- **Parity.** Every hover response is also the `:focus-visible` response. The contact discs get theirs: today the
  disc fills on hover only.
- **Forced colours.** Arch edges in `CanvasText`, no light layers.
- **Print.** Drawn at rest.
- **Guard updates (V5.20 strict rule, each citing V5.22 §6, §7, §13).** Each keeps an invariant of equal or greater
  strength:
  - `tests/frontend/test_chapter_marks.py`: a head draws its concept as a T1 seal or not at all; never `ile-steps`;
    never two concepts in one head.
  - `tests/frontend/test_motion_v512_a_w2.py` (the `reveal-mark` cases): icons never fade-and-rise.
  - `tests/frontend/test_interior_w3_f1.py:284` (≤ 6 body icons) keeps:
    - one primary per page;
    - every body icon a registered concept, one concept once per section;
    - never `ile-steps`;
    - a register of named entities (the PATHWAY index, the pilot's eight stations, the Forum's nine actors) all or
      nothing, recorded in DESIGN_SYSTEM_V5 §13.
  - **New guards:** the body gold budget per viewport; hover/focus parity; the marks' floors and their sprite ceiling
    (`tests/frontend/test_icons.py`).

---

## 5. Motion Density V2

### 5.1 The vocabulary: one timing language, many verbs

| Verb | Mechanism | Tokens | Signature of | Reduced-motion still |
|---|---|---|---|---|
| **LINE DRAW** | `stroke-dashoffset` on `pathLength=1`, or `scaleX`/`scaleY` on a rule from the reading edge | `--motion-draw` 900 ms, `--ease-sine` | F, the head rules, C4 hub line, EN-4 rule, AF rule | drawn |
| **MASK REVEAL** | `clip-path: inset()` from the reading or outer edge; arch silhouette widening; panel swap ≤ 320 ms | `--motion-draw` / `--motion-emphasized`, `--ease-enter` | A, L stage, AG-1 plate, D1 plates | open |
| **COLOUR TRANSITION** | black and white → colour (`filter`, images only); text `--text-3` → `--text-1` | `--motion-slow` 480 ms; `--motion-standard` 200 ms | the pilot develop, B lane frames, F1 frames, U1 destination | colour, full ink |
| **DIRECTIONAL SLIDE** | `translate` on the inline axis, logical, ≤ 8 px on entry, ≤ 12 px on state; native snap | `--motion-slow`, `--ease-enter` | J; F1 annotation | at rest |
| **STAGGER** | 60 ms steps, capped at 6, on rules, glyph tiles and light | `--motion-stagger` | E, PA-2, C board, G2 | all lit |
| **DEPTH** | a pre-painted shadow layer's opacity 0 → 1 + scale 0.985 → 1 or a 2 px lift (SH-4: a shadow never animates) | `--motion-slow`, `--ease-enter` | K, term plate, FO3, the D1 sticky aside | at rest |
| **LIGHT** | a radial or linear light swept once, or `--light` 0 → 1 on `:has()`; M21 spotlight | `--motion-route-light` 1 200 ms / `--motion-emphasized`, `--ease-sine` | PP-2, K sweeps, T1 thresholds | the final light |
| **PATH PROGRESSION** | a lane or route lit by a dash of its own path; scroll-linked `scaleY` where scrubbed | `--motion-route-light`, `--ease-sine`; `view()` | B, EN-1, U1 | drawn, lit |
| **LAYERING** | figure layers per state; two planes at two rates (the ground drift ≤ 24 px, M22 ±3 %) | `--motion-slow`; `view()` | C, the D drift, the K ground | final layer, no drift |
| **CONTROLLED SCALE** | 1.06 → 1 under a mask (`--reveal-zoom`); 1.04 → 1 on an LCP after paint; 0.92 → 1 node settle; stamp press 1.04 → 1 | 1 080 ms / 1 200 ms / `--spring-soft` / 200 ms | A, Vivre V1, H nodes, D2 stamp | 1 |
| **SEMANTIC TURN** | key −90°, needle settle, chevron 180° | `--ease-turn`, `--spring-soft` | S8, «la boussole», disclosures | no rotation |

**No new duration or easing token.** The `tokens.css` set is enough. Distances live in `_sezioni.css` (`--sez-slide`
8 px, `--sez-drift` 24 px).

**translateY + opacity** (`rise.js`, `reveal-mark`) is never a section's motion again. It survives only on rows inside
plain lists that no V2 pattern composes (the legal pages, the CMS reading templates, published news). S-close removes
it from the 15 pages.

### 5.2 The per-page motion map (adjacent sections differ)

| Page | Sequence of signatures below the header |
|---|---|
| Home | LINE (H0 + S2 route) → GLIDE (S3) → WIDENING + DEVELOP (S4) → DEPTH (S5 + S6) → MASK (S7) → TURN (S8); phones: SLIDE (S1) between the hero and S2 |
| Le projet | LAYERING (story) → WIDENING + DRIFT (panorama) → STAGGER (doors) |
| Projet pilote | LINE (route) → LIGHT (doors) → LIGHT sweep + depth («l'approdo», different ground, different scale) |
| Parcours | PATH (lanes) → STAGGER (how it works) → STAGGER on another ground (grid) → DEPTH (protezione) |
| Pathway sheet | SCROLL PROGRESSION (filo) → RELATIONAL DRAW (arc) → DEPTH (protezione) → MASK/height (terms) → TURN (boussole) |
| Entreprises | PATH (process) → WIDENING + DRIFT (band) → none (form) → LINE (split rule) → LIGHT sweep (approdo) |
| Institutions | RELATIONAL DRAW + DEVELOP (emiciclo) → LIGHT sweep (approdo) |
| Universités | PATH + DEVELOP (filiera) |
| Formation | LINE + DEVELOP (traversata) → STAGGER (grid) → DEPTH (protezione) → TURN (boussole) |
| Diplômes | LINE + MASK + DEPTH (process + aside) → DEPTH on stone (protezione) → STAGGER (grid) → TURN (boussole) |
| Réseau | GLIDE + RELATIONAL DRAW (head map) → LIGHT sweep (approdo) |
| Contact | STAGGER (board) → LINE (doors' hub) |
| FAQ | GLIDE + MASK (explorer) → STAGGER (rimando) |
| Glossaire | GLIDE (rail) + STAGGER (lessico) → STAGGER on stone (rimando); term page: DEPTH + LINE |
| Vivre | SCALE + DRIFT + LIGHT (panorama) → STAGGER (tiles) |
| Forum | LINE + LIGHT (pair) → SCROLL PROGRESSION (objectives) → RELATIONAL DRAW + SETTLE (audience) → DEPTH (actions) |
| AGAMI | MASK (identity) → LIGHT (targa) → LIGHT sweep (approdo) |
| Fraudes | LINE + STAGGER (split) |

### 5.3 Density and budget per page

- **Per view:** ≤ 1 moving control, ≤ 1 tier-2 surface entrance and ≤ 1 tier-3 sequence (draw or stagger) at a time
  (DECISIONS §2 rule 5, kept).
- **Per section:** one signature entrance, once. Per page: 3–6 signature entrances. Nothing loops, shakes or pulses.
- **Runtime:**
  - 0 animations and 0 `will-change` at rest;
  - finished entrances use fill `backwards` and leave `getAnimations()`;
  - no scroll listener, no rAF loop (a finite one inside a module is allowed);
  - observers disconnected after use;
  - compositor-only properties: `transform`, `translate`, `scale`, `opacity`, `clip-path`, `filter` on images,
    `stroke-dashoffset`.
- **Performance gates** (measured on the compressed twin 8782 per V5.4 plan §2.6: slow 4G + CPU × 4, n ≥ 9):
  - **LCP ≤ 2.5 s mobile** on every page type, fr and ar;
  - **CLS ≤ 0.1** on every page (≤ 0.05 on the home and the landings): panels stack in one grid cell; images carry
    width and height; nothing animates layout;
  - **INP ≤ 200 ms** on every interaction (tabs, map, filter, explorer, disclosures, doors);
  - no long task beyond the first render.

---

## 6. Depth & material · typography · text density

### 6.1 Depth and material: institutional, never neon SaaS

- **Grounds.**
  - Paper `--surface-page` / `--surface-sheet`; stone `--surface-area`; the brand wash `--grad-brand` (one per page).
  - Night `--surface-night` with `--mesh-dark` and the static grain (`static/img/grain.svg`, 3–4 %, never animated).
  - Graded photographs under `--scrim-photo-aa` / `--plate-night-photo`.
  - Two equal grounds never touch. A night band is never directly above the night footer (stone or paper sits
    between, or the band joins the footer by a page-only rule, as on the home).
- **Planes** (SH-1): 0 canvas · 1 sheet · 2 raised · 3 popover/panel · 4 modal.
  - **One raised surface per first screen.**
  - Shadows are `rgba(7, 18, 38, α)`: never black, never coloured, never luminous.
  - **A shadow never animates.** A change of plane is a pre-painted layer's opacity (SH-4).
  - Rows never carry shadows (SH-2).
- **Light.** Radial lights at ≤ 22 % (`--accent-mark`, paper) or ≤ 28 % (oro, night, arrival only). One sweep per
  band, once.
- **Architectural geometry.** The brand doorway (arch, opening, sill), route lines, corner brackets as formwork marks,
  and page motifs as low bookends at ≤ 30 % `--line-structure`.
- **Forbidden:**
  - glass outside the two sticky bars (SH-5);
  - blur on content; glow; neon edges; purple or AI gradients; animated gradients or grain;
  - 3D tilt; drop shadows on text;
  - more than three corner radii per screen (4 · 6 · full; the arch's crown is «full»).

### 6.2 Typography: compositional, never a magazine

- **The public scale stays eight sizes:** 64 display · 36 title · 28 band · 20 entry/lead · 17 body · 15 ui ·
  13 small · 12 caption. No ninth size. No serif (`--f-serif` is the sans for Latin, the V5.15 decision). Arabic
  follows the Vazirmatn rules: titles 600 at 1.4, body at 1.75, never under 14 px.
- **Devices** (§19):
  - **Large keyword**: a locked text's own word set at `--t-title` or `--t-display` through a span («Non.», «2011»
    emphasis).
  - **Side annotation**: 13–15 px beside a frame or plate at `--measure-small` (the Formation notice, the term page's
    sources, the AGAMI identification line, the help lines).
  - **Step marker**: ILE Mono numerals at `--t-title` (36), tabular lining, in stations (F, I, B).
  - **Emphasised legal or product statement**: 20/28 at 600, or 28/36, with a 2 px rule («Qui décide ?», FO1's last
    sentence).
  - **Pull-out concept**: emphasis in place, never a duplicated quote (RH-5).
  - **Caption next to an image**: the credit stays the `figcaption`; a caption sentence sits beside the frame, not
    under it, where the composition asks.
- **Head roles** as in §2.0. A display line appears at most once below a page's header (the pilot seam title, the term
  page's term, the glossary letters).
- **Capitals.** Locked capitals stay as written. Tracking applies only to locked capital strings and the ILE Mono
  folio. No capitals are added.
- **Measures:** body and lead 36 rem; a statement at display sizes ≤ 30 em.
- **French locked runs inside it/en/ar:** their own box, their own start (§1.6).

### 6.3 Text density

- **No running prose block over 6 lines at 1440 (12 at 390)** inside a V2 section without a structural device:
  summary + detail, a step split on its own separators, side information, in-place emphasis, or a sticky companion.
- **Exception:** a locked legal notice kept whole. It then gets typographic levels through spans: the anti-fraud body,
  the Forum's «what», Formation's 71-word body.
- Disclosure is allowed only for non-mandatory detail (§1.7).
- Nothing authoritative is shortened. A team string may be shortened or rewritten only by its owner, with
  professional it/en/ar.

---

## 7. Budgets

### 7.1 CSS (gzip -9; measured on `fdd6e34`, 30 Oct)

| Sheet (dist) | Today | V2 ceiling | Note |
|---|---|---|---|
| `main.css` | 32 718 | **32 718** (ratchet: never up; S-close lowers it to the measure if a dead rule leaves) | no V2 rule; no new token |
| `core/reveal.css` | 2 379 | 6 144 (existing) | the motion vocabulary V2 (S) |
| `core/portico.css` | 2 993 | 3 000 (existing) | untouched |
| `pages/css/fronte.css` | 5 508 | 6 144 (existing) | S's folio T1 change paid by the removed folio disc rules |
| `pages/css/hero.css` | 10 711 | 11 264 (first recorded) | H0 only |
| `pages/css/pages.css` (home) | 4 269 | 12 288 | H |
| `pages/css/interior.css` | 3 687 | 11 264 | P2 |
| `ecosystem/ecosystem.css` | 4 976 | 11 264 | P1 |
| `pathways/pathways.css` | 5 126 | 11 264 | P1 |
| `cms/lettura.css` | 4 110 | 9 216 | P2 |
| `forum/forum.css` | 3 380 | 8 192 | P2 |
| `core/glyph.css` | 1 571 | 2 048 (existing) | untouched (forms preserved) |

**Per page type, all sheets the page links, desktop (portico included):**

| Page type | Today | Ceiling |
|---|---|---|
| Home | 53 070 | ≤ 61 440 |
| Landings, interior and pathways pages | 47 285 – 48 724 | ≤ 56 320 |
| Reading pages and the Forum | ≈ 47 700 | ≤ 54 272 |

S-close ratchets every per-sheet and per-page ceiling to its measure after the last merge.
`tests/frontend/test_frontispiece_v515_c.py`'s blanket 6 KB for four sheets becomes these recorded per-sheet ceilings
plus the per-page totals. That is a stronger invariant: page-only, each sheet capped, each page capped, ratchet-down.
The change cites V5.22's «page-only sheets with their own recorded budgets».

### 7.2 JavaScript (gzip)

| Item | Ceiling |
|---|---|
| `rise.js` (the section runtime) | ≤ 1 536 (873 today) |
| `sezioni/indice.js`, `mappa.js` | ≤ 1 536 each |
| `sezioni/flow.js`, `spia.js`, `racconto.js` | ≤ 1 331 / 1 024 / 922 |
| Section chunks per page | ≤ 2, ≤ 3 072 together |
| `home.js` | ≤ 8 192 (7 357 today) |
| `shell.js` | ≤ 4 700 (unchanged, untouched) |
| A public page, all JS | ≤ 45 KB (plan §2.6) |

**Requests before `load`:** unchanged on every page type, except +1 CSS (`fronte.css`) on the two form pages and the
glossary term page (recorded). Section chunks are dynamic imports and are counted separately (≤ 2).

### 7.3 Images

| Kind | Ceiling (largest served AVIF) | Notes |
|---|---|---|
| Body frame | ≤ 45 KB | |
| 21:9 band or panorama | ≤ 60 KB at 1 920 w | |
| 2:3 pilot panel | ≤ 60 KB at 1 600 w | |
| Family frame (B) | ≤ 30 KB at 720 w | |
| Ground (K) | ≤ 60 KB (21:9 at 1 920 w), ≤ 40 KB (4:5 at 800 w) | |
| LCP images | unchanged (≤ 60 KB) | |

- Every new frame is lazy with `decoding="async"`, explicit width and height, and an exact `sizes`.
- **No new eager image anywhere.**
- A page's full-scroll image weight at 390 DPR 2 may rise by at most 250 KB over `fdd6e34` (measured per page by
  lane M).
- No video (R55 stands).

---

## 8. Imagery plan (lane M)

**Pipeline.**
- Pexels only; originals outside the repository; self-hosted derivatives through `tools/build_derivatives.py` (AVIF +
  WebP at 480/800/1200/1600 (+1920 for 21:9), the one V5 grade).
- `static/img/v5/<family>/PROVENANCE.json` rows: pexels id, page, licence, original size and sha256, crops,
  redactions, treatment. No person's name is copied into any other document.
- `docs/IMAGE_LICENSES.md` §3 and `docs/design-v5/ASSET_USAGE_MATRIX.md` rows; slots in `apps/pages/imagery.py`.

**Rules.**
- **One frame, one slot, site-wide** (`tests/compliance/test_imagery_v512.py`).
- Nobody identifiable (O55): hands, backs and out-of-focus figures only.
- **No arch, step, vault, door or gridded window as the subject** (O54, `docs/IMAGE_LICENSES.md:100`).
- No cliché: passport, plane, luggage, handshake, gavel, call centre, visa counter, flag.
- No readable text or brand: blur-redact, as recorded.
- Stock is never documentary: alt texts say what is shown, never a place or an event.
- Q4 and Q5 hold.
- Every frame passes the AUM §6 full-resolution check before it ships.

**Treatments.**
- Black and white rests only in the hero, plus the `select` treatment (black and white at rest, colour on its
  lane's state, hover or focus: the Parcours family frames, «meaningful interaction», V5.12 §9).
- The home stone ground is desaturated in the file, never by a CSS grayscale.
- `apps/pages/tests/test_home.py::test_black_and_white_rests_only_in_the_hero` gets the new home slot in its set
  (lane H, citing V5.22 §14). The invariant stays: black and white rests only in the hero, and every frame under it is
  revealed by lane A's one mechanism.

### 8.1 New frames (7)

| Slot (family / slug) | Page · section | Subject brief | Crops | Treatment | Ceiling |
|---|---|---|---|---|---|
| `home.integrity.stone` (`accueil` / `pierre-appareillee`) | Home S5 + S6 ground | dressed stone masonry (travertine or ashlar courses) in raking light, close and frontal; **no opening of any kind** in frame | 21:9 (≥ 64 rem), 4:5 | desaturated −35 % in the file, under a 60 % stone veil; alt `""` (decorative), credit visible | 60 / 40 KB |
| `project.volumes` (`projet` / `codici-rilegati`) | Le projet, D panorama | bound volumes of law reports on shelves, spines in raking light, titles unreadable (redacted where legible), nobody; a different scale and subject from the Universités reading room | 21:9, 4:5 | colour, cool grade | 60 / 45 KB |
| `pathways.family.work` (`personnes` / `entrepot-allee-rayonnages`) | Parcours PA-1, lane «Travail» | a logistics warehouse aisle with high racking in perspective, empty or with one out-of-focus figure | 3:2, narrow 21:9 | `select` | 30 KB |
| `pathways.family.study` (`personnes` / `cahier-lexique-mains`) | Parcours PA-1, lane «Études et formation» | hands writing vocabulary cards beside a bilingual dictionary on a desk; no readable words | 3:2, narrow 21:9 | `select` | 30 KB |
| `pathways.family.family` (`personnes` / `table-dressee-mains`) | Parcours PA-1, lane «Famille» | a set family table seen from above, hands passing a dish; no faces | 3:2, narrow 21:9 | `select` | 30 KB |
| `pathways.family.other` (`personnes` / `vignes-brume-aube`) | Parcours PA-1, lane «Autres voies» | vine rows in morning mist (seasonal work); distinct from the Entreprises greenhouses at dusk | 3:2, narrow 21:9 | `select` | 30 KB |
| `training.before` (`formation` / `banc-electrique-mains`) | Formation F1, station 1 | hands wiring terminal blocks on an electrical training panel; no face, brand or readable text; distinct from the welding head and the companies' calliper | 4:5, narrow 3:2 | `develop` (`bw-scroll`, allowed for /formation/'s two times) | 45 KB |

### 8.2 Re-crops (same sources, same slots, new derivatives)

| Slot | New crops | Why |
|---|---|---|
| `home.pilot.cedar` (Pexels 30563520) / `home.pilot.marble` (6713855) | 2:3 full-height panels (cedar 2 023 × 3 035 of 4 547 × 3 035; marble 2 667 × 4 000 of 6 000 × 4 000), narrow 3:2; new `sizes` | the D panel |
| `home.ecosystem` (33543226) | 4:3 (6 869 × 5 152), narrow 3:2; the lanyard redaction kept | the A arched frame |
| `universities.exchange` (31367507) | a 3:2 re-crop of hands and folder only, **no redaction needed** | the blurred covers read as censored objects at 768 (`pages2/p1_universites_fr_768.jpg`) |

### 8.3 What each major page carries below its header after V2

| Page | Visual moments below the header |
|---|---|
| Home | pilot panorama, stone ground, ecosystem frame; drawn route and seals |
| Le projet | story figure, law volumes |
| Projet pilote | drawn route, approdo miniature |
| Parcours | four family frames, drawn lanes |
| Pathway sheets | drawn timeline and arc |
| Entreprises | drawn process, panorama band |
| Institutions | hemicycle map |
| Universités | route + campus destination |
| Formation | two frames on the crossing |
| Diplômes | drawn process |
| Réseau | the head map |
| Contact | channel board and doors |
| FAQ, Glossaire | drawn seals and plates (type-led) |
| Vivre | street panorama |
| Forum | three drawings (Q4) |
| AGAMI | drawn colonnade plate (Q5) |
| Fraudes | type-led split |

No frame repeats anywhere.

---

## 9. Implementation lanes

### 9.1 Lane S — Section System V2 foundation + Icon Treatment V2 + Motion Density V2 (first)

**Scope.**
1. **Section runtime.** `rise.js` gets the trigger contract (§2.0) and the dynamic loader of `sezioni/*`. Its
   chapter SINGLES stay only for not-yet-migrated pages until S-close.
2. **Motion vocabulary V2** in `_reveal.css` (§5.1): the verbs' keyframes and trigger selectors; `reveal-mark`
   retired from V2 icons; **the M22 specificity fix**; M21 spotlight to `--accent-mark` on paper.
3. **The library.**
   - CSS: `_sezioni.css`, `_sigillo.css`, `_sec-{campata,tracciato,racconto,mosaico,mappa,filo,passaggio,strato,indice}.css`,
     `.panorama` in `_photo.css`, the passage V2 in `_journey-passage.css`.
   - Partials `templates/components/sezioni/{_testa,sigillo,campata,tracciato,racconto,panorama,mosaico,mappa,filo,strato,protezione,approdo,indice,boussole}.html`,
     `components/stepper.html` V2, `components/photo.html` (the `select` treatment, panorama hooks), `pages/partials/_linea.html`.
   - JS modules `static/js/src/sezioni/{indice,mappa,flow,spia,racconto}.js`.
4. **Icon Treatment V2.**
   - The registry: `MARKS`, `PILOT_STATION` and the glyph choices pending in §3.
   - 13 custom marks: inline partials + `static/img/icons-marks.svg`; vendored Lucide additions; `docs/design-v5/ICON_LICENSES.md`,
     `ICON_SEMANTIC_MAP.md`.
   - `_chapter_head.html` / `_section_header.html` (the bare mark retired; `_testa.html`).
   - **The folio → T1 seal** in `_ingresso.html` + `_fronte.css`, with `fronte.css` held ≤ 6 144 B.
   - **`compact=True`** for the form pages' and the term page's frontispiece.
   - The login eyebrow key (`entrance.css`, one rule).
5. **Locked-copy helpers.** `apps/cms/locked_split.py` + the filters `locked_spans` and `emphasize`, with equality tests.
6. **Guards and budgets** (§4.10, §7): the cited updates of `test_chapter_marks.py`, `test_motion_v512_a_w2.py`,
   `test_interior_w3_f1.py`, `test_frontispiece_v515_c.py`; new guards (gold budget, parity, reduced-motion stills,
   no-JS order, fill `backwards`, per-sheet and per-page ceilings); the four `main.css` ceilings untouched.
7. **Docs.** `docs/design-v5/COMPONENT_PROVENANCE.md` rows (from §2's provenance); DESIGN_SYSTEM_V5 §13 (icon tiers,
   the register exemption) and the motion vocabulary V2.

**Proof.** Browser fixtures under `tests/frontend/`, one per pattern: render it at the 8 widths in fr and ar,
reduced motion, keyboard, no-JS. These are fixtures, not a hub page: the library is never shown to the owner as a
catalogue. On the real pages S lands the T1 folio seals, the motion vocabulary and the M22 fix. «Icon Treatment V2»
and «Motion Density V2» become visible in the preview.

### 9.2 Lane M — imagery (in parallel with S from day 1)

**Scope.** §8: seven new frames and four re-crops; slots, derivatives, provenance, licences, asset matrix,
professional alt texts (FR msgids + it/en/ar in S-close's catalogue pass); the one-frame-one-slot and AUM guards
extended; the per-page image-weight report.

**Feeds.** H (the stone, pilot panels, ecosystem 4:3), P1 (families, `training.before`, campus re-crop), P2
(`project.volumes`).

### 9.3 Lane H — Homepage Composition V2

**Scope.** §3.1: H0, S1–S8, both gate states; the pilot lead rewritten by the team; the home footer junction rule.

### 9.4 Lane P1 — Page Composition V2: journeys and spaces

**Scope.** §3.3–§3.10: Projet pilote, Parcours (+ `index_interim.html` kept coherent), the eight pathway sheets,
Entreprises (+ the Recueil header), Institutions (+ the Collaboration header), Universités, Formation, Diplômes.

### 9.5 Lane P2 — Page Composition V2: system, trust and reading

**Scope.** §3.2 and §3.11–§3.18: Le projet, Réseau, Contact, FAQ, Glossaire + the term page, Vivre, Forum, AGAMI,
Fraudes.

### 9.6 S-close (after P2)

**Scope.**
- Dead-rule removal across `_pagina.css`, `_compose.css`, `_interior.css`, `_reveal.css`, `pages.css`, `_spaces.css`,
  `_pathways.css`, measured by Chromium coverage (the V5.20 method);
- every ceiling ratcheted to the measure;
- the single catalogue pass (`makemessages` / `compilemessages`; professional it/en/ar for every new team string;
  Arabic reviewed for RTL; locked text never translated);
- the final docs.

### 9.7 File ownership (no two lanes edit the same file)

| Files | Owner | Others |
|---|---|---|
| `static/js/src/rise.js`, `static/js/src/sezioni/**`; `static/css/v5/_reveal.css`, `_sezioni.css`, `_sigillo.css`, `_sec-*.css`, `_photo.css`, `_journey-passage.css`, `_pagina.css`, `_interior.css`, `_compose.css`, `_porta.css`, `_fronte.css`; `templates/components/sezioni/**`, `components/stepper.html`, `components/photo.html`, `pages/partials/_linea.html`, `_ingresso.html`, `_chapter_head.html`, `_section_header.html`; `apps/core/icons.py`, the sprites, `static/icons/src/**`, `scripts/build_icons.py`, `static/img/icons-marks.svg`; `apps/cms/locked_split.py` + its filters; `apps/accounts/static/accounts/entrance.css` (one rule); the shared guard tests; `COMPONENT_PROVENANCE.md`, `ICON_*.md`, `DESIGN_SYSTEM_V5.md` | **S** | H, P1 and P2 consume classes, partials and data attributes; any change goes to S in notes. Page-specific overrides go in their own family partials |
| `apps/pages/imagery.py`, `static/img/v5/**`, `tools/build_derivatives.py`, `docs/IMAGE_LICENSES.md`, `docs/design-v5/ASSET_USAGE_MATRIX.md`, `tests/compliance/test_imagery_v512.py` | **M** | others reference slot keys only |
| `templates/pages/home.html`, `templates/pages/home/**` (in `home/_hero.html`, the foot `he__body` only), `components/entrances.html`, `components/pathway_list.html` (other callers unchanged), `apps/pages/static/pages/css/pages.css`, `hero.css`, `static/js/src/home.js`, `apps/pages/services.py`, `apps/pages/content.py`, `apps/pages/tests/test_home.py` | **H** | P2 reads `content.py` (NETWORK_ACTORS) and `services.py` without editing them. If P2 needs data there, it builds it in `apps/pages/views.py` (its own file) |
| `templates/ecosystem/**`, `apps/ecosystem/**` (incl. `_spaces.css`, `ecosystem.css`), `templates/pathways/**`, `apps/pathways/**` (incl. `_pathways.css`, `pathways.css`, `services.py`), the header blocks only of `templates/enquiries/company_needs.html` and `collaboration_proposal.html`, their tests | **P1** | H imports `pathways.services.how_it_works` read-only; P2 imports `GLOSSARY_TERMS_BY_PATHWAY` read-only |
| `templates/pages/{project,network,contact,agami,antifraud,institutional_base}.html`, `templates/pages/partials/_canali.html`, `templates/pages/partials/fronte/_rete.html`, `fronte/_contatto_azione.html` (the address caption), `apps/pages/views.py`, `apps/pages/static/pages/css/{interior.css,_institutional.css,_canali.css}`, `templates/faq/**`, `templates/glossary/**`, `templates/living/**`, `apps/faq/**`, `apps/glossary/**`, `apps/living/**`, `apps/cms/static/cms/lettura.css`, `static/css/v5/_lettura.css`, `templates/forum/**`, `apps/forum/static/**`, their tests (incl. `apps/pages/tests/test_institutional.py`, `test_contact_channels_v519.py`, which must not weaken) | **P2** | — |
| `locale/**` | **S-close** | the lanes list new msgids in their notes |
| `docs/design-v5/DECISION_LOG_V54.md`, `OWNERSHIP_V54.json`, `live_status.json`, `CHANGELOG_V54.md` | the steward | — |

**Merge order: S → M → H → P1 → P2 → S-close.**
- H, P1 and P2 build in parallel against S's documented contracts, in their own worktrees, and rebase on each merge.
- Each lane runs its tests on its **own `TEST_DATABASE_URL`**.
- One Chromium per lock slot (`C:/tmp/ile_locks/CHROMIUM_LOCK_A`/`_B`, ≤ 25 min per session).
- Merges go through `DESIGN_V5_MERGE_LOCK`.
- **S never removes a legacy behaviour a not-yet-migrated page still uses; S-close does.**
- **Shared test modules.** A test module that covers both home and interior pages (`apps/pages/tests/test_services.py`,
  `test_templates_static.py`, `test_browser.py`, `test_review2.py`) belongs to the first lane in the merge order that
  changes it (H). P2 puts its new assertions in a module of its own (`apps/pages/tests/test_interior_v522.py`) and
  sends any needed change to an H-owned module through H's notes. Every lane adds its new browser checks in new
  modules named `test_*_v522_<lane>.py`, so two lanes never edit one test file.

### 9.8 Preserved families: NOT touched

**Untouched:**
- The navbar, the mega menus, the mobile sheet and the footer: `partials/header.html`, `main_nav.html`, the portico
  partials, `chrome.css`, `_portico.css`, `nav.js`, `shell.js`, `footer.html`.
- Lume: `lume.css`, `loader.css`, `motion.css`, `head.js`, `lume/*`.
- The premium forms: `components/form_*`, `_form.css`, `_formwork.css`, `_glyph.css`, `_choice.css`, `_steps.css`,
  `fieldcheck.js`, `steps.js`, `combobox.js`, the form bodies.
- The contact channels' architecture (SiteSettings / `ILE_WHATSAPP_NUMBER`, links, accessible names, `bdi`).
- The privacy and cookie pages and their links.
- Terminology (catalogue labels).
- Security and accessibility behaviour.
- The Institution/University role-aware platform: `templates/portal/**`, `apps/portal/**`.
- The home hero's first screen.
- `templates/base.html`, `tokens.css`, `main.css`.

**The named exceptions, each inside a section in scope:**
1. `entrance.css`: the login eyebrow key (S).
2. The two form pages' **header blocks** (P1).
3. `_canali.html` placed inside the channel board, channels unchanged (P2).
4. The home's footer junction, by a page-only rule in `pages.css` (H).
5. The folio seals in `_ingresso.html` / `_fronte.css` (S).
6. Réseau's head ring made interactive (P2).
7. The Vivre head absorbed by its panorama (P2).
8. The Forum head's drawing (P2).

**Recorded, not done in V5.22** (for after acceptance):
- the chrome's gold (mega-menu hover, lunetta halo, mobile sheet gold door disc and channel glyphs);
- the Forum `handshake` at 20 px in the mobile sheet, below its 24 px floor;
- the form tiles' gold top light (`_glyph.css`);
- the «attesa» notice glyph at 3.63:1;
- the FAQ category's it/en/ar names (back-office content);
- the Lume pre-warm veil at 1–2/255 (deliberate, `lume.css:78-95`).

### 9.9 Acceptance per lane (every item is a merge gate)

1. **Scores.** The six §26 dimensions (composition, motion, imagery, interaction, institutional quality, coherence)
   reach ≥ 4 on every page the lane owns (targets in §10), self-scored at 1440 and 390 in fr and ar, then verified by
   the one senior reviewer. For lane S: no page scores lower on any dimension after S than before.
2. **Headed Chromium** at 1440, 1280, 1024, 768, 430, 390, 375 and 360, in fr, it, en and ar:
   - rhythm, image crops, motion, no horizontal overflow, text density, icons, interaction, RTL;
   - reduced motion emulated: every section shows its designed still;
   - keyboard only: every control reachable, focus visible and never obscured (2.4.7, 2.4.11), no animation;
   - no-JS: complete content in reading order.
3. **WCAG 2.2 AA:**
   - axe at 0 serious or critical;
   - contrast 1.4.3 and 1.4.11;
   - target size 2.5.8, with ILE's 44 px for primary targets;
   - name, role and value for tabs, maps and disclosures (4.1.2);
   - no information behind hover only.
4. **Locked copy and legal notices.** Locked copy is byte-identical (`locked_content.sha256.json`, the six-word guard,
   the split equality tests). Every legally required notice is visible (§1.7). Both G3 states render.
5. **The Word/PDF test fails** for every V2 section (§1.2).
6. **Budgets** (§7) measured and recorded; LCP, CLS and INP within §5.3 on 8782.
7. **The V5.20 final gate on the integrated tree:** FAILURES 0, BLOCKING LINT 0, UNEXPECTED SKIPS 0, P0/P1 0. A test
   changes only under the strict rule, citing V5.22.
8. **Preview labels.**

   | Lane | Visible in preview |
   |---|---|
   | S | «Section System V2 · Icon Treatment V2 · Motion Density V2» |
   | H | «Homepage Composition V2» |
   | P1, P2 | «Page Composition V2» |

   Shown at `http://127.0.0.1:8780/__design-v5/`.

---

## 10. Score targets (§26; 1–5, 3 = clean but editorial or static)

Today's scores are the audits'. Each target is the lane's acceptance bar.

| Page | Comp. | Motion | Imagery | Interaction | Institutional | Coherence |
|---|---|---|---|---|---|---|
| Home (fr; ar) | 2.5 → **4.5** | 2.5 → **4** | 2.5 → **4** | 2 → **4** | 3.5 → **4.5** | 3 / 2.5 → **4.5** |
| Le projet | 2.5 → 4 | 2 → 4 | 2.5 → 4 | 2 → 4 | 3.5 → 4.5 | 3.5 → 4.5 |
| Projet pilote | 2.5 → 4 | 2.5 → 4 | 2.5 → 4 | 2 → 4 | 3.5 → 4.5 | 3.5 → 4.5 |
| Parcours | 3 → 4.5 | 2.5 → 4 | 2.5 → 4.5 | 3 → 4.5 | 3.5 → 4.5 | 3.5 → 4.5 |
| Pathway sheet | 2 → 4 | 2 → 4 | 1.5 → 4 (drawn) | 2 → 4 | 3.5 → 4.5 | 3.5 → 4.5 |
| Entreprises | 3.5 → 4.5 | 3 → 4 | 3.5 → 4.5 | 3.5 → 4 | 4 → 4.5 | 3.5 → 4.5 |
| Recueil / Collaboration heads | 2.5 → 4 | 2.5 → 4 | 1.5 → 4 (drawn) | n/a (the form) | 3.5 → 4.5 | 2.5 → 4.5 |
| Institutions | 3 → 4 | 3 → 4 | 3.5 → 4 | 2.5 → 4 | 3.5 → 4.5 | 3.5 → 4.5 |
| Universités | 2.5 → 4 | 2.5 → 4 | 3.5 → 4 | 2 → 4 | 3.5 → 4.5 | 4 → 4.5 |
| Formation | 3 → 4 | 3 → 4 | 3.5 → 4.5 | 2 → 4 | 3.5 → 4.5 | 4 → 4.5 |
| Diplômes | 2 → 4 | 2.5 → 4 | 3 → 4 | 2 → 4 | 3.5 → 4.5 | 4 → 4.5 |
| Réseau | 2.5 → 4.5 | 2 → 4 | 2.5 → 4 | 2 → 4.5 | 3.5 → 4.5 | 3 → 4.5 |
| Contact | 2.5 → 4 | 2.5 → 4 | 3 → 4 | 3 → 4.5 | 3.5 → 4.5 | 4 → 4.5 |
| FAQ | 3 → 4 | 3 → 4 | 2 → 4 (drawn) | 3.5 → 4.5 | 3.5 → 4.5 | 4 → 4.5 |
| Glossaire (+ term page) | 2.5 → 4 | 2.5 → 4 | 2 → 4 (drawn) | 3 → 4 | 3.5 → 4.5 | 3.5 → 4.5 |
| Vivre en Italie | 2.5 → 4 | 2.5 → 4 | 4 → 4.5 | 1 → 4 | 3.5 → 4.5 | 3.5 → 4.5 |
| Forum | 2.5 → 4 | 2 → 4 | 1.5 → 4 (drawn, Q4) | 2 → 4 | 3.5 → 4.5 | 3.5 → 4.5 |
| AGAMI | 2 → 4 | 2 → 4 | 2 → 4 (drawn, Q5) | 1.5 → 4 | 3 → 4.5 | 3 → 4.5 |
| Attention aux fraudes | 3 → 4 | 2.5 → 4 | 2 → 4 (type-led) | 2 → 4 | 4 → 4.5 | 4 → 4.5 |
| Academy entry (login) | preserved; eyebrow key only | | | | | |

---

## 11. Owner question (the only one)

**AGAMI page, «Identification et contact» (`templates/pages/agami.html:44-55`).** The page sends visitors to the site's
«Mentions légales» for the association's identification data. That notice stays unpublished under Q2. The legal
question concerns identifying the site's publisher: until the legal notice is published, should this page carry the
association's public identification data itself (name, legal form, registered seat, registry and tax numbers, as the
association already publishes them)? Or should the reference be withdrawn? The composition (§3.17, AG-3) is built
either way. Only the side annotation's content waits for the answer.

---


### 11.1 The owner's answer (30 October 2026, 21:15 — binding; full text in the orchestrator's directives as V5.23)

**Q9 — Decision: A.** The AGAMI page shows the association's verified public institutional identification directly, as a compact, elegant identification block integrated into the page (strong typographic hierarchy, appropriate institutional iconography, refined spacing, subtle interaction only if useful, the existing premium visual language) — never a legal-disclaimer dump, and never a link to an unpublished «Mentions légales» merely to identify the association. Only these verified public data, no other identifier:

| Field | Value |
|---|---|
| Name | AGAMI – Dialogo Giuridico Interculturale APS |
| Legal form | Associazione di Promozione Sociale (APS) / Ente del Terzo Settore |
| Tax code | 91036640240 |
| RUNTS | Repertorio n. 149809 |
| Registration | Decreto Regione Veneto n. 11118 del 17/09/2025 |
| Registered office | Via Sandrigo n. 29, 36061 Bassano del Grappa (VI), Italy |
| Operational office | Viale Giuseppe Mazzini 142, 00195 Roma, Italy |
| Official contact | contact@agamieuromed.org |
| Official website | agamieuromed.org |

When the full legal notices are published, the block may link to them for further information, but it must remain independently understandable. Lane P2 builds it in §3.17 from one canonical source (the existing prescribed identity strings byte for byte where they already exist; the missing fields — e.g. the registration decree — added once, never duplicated across templates).

## 12. Evidence

- **The Director's verification pass:** headed Chromium (build chromium-1234), lock slot A 19:56–19:57:47 (released),
  15 captures in `evidence/v522/director/`:
  - `d_fr_1440_home_handoff`, `d_fr_1440_home-orientation`, `-pathways`, `-trust`, `-antifraud`, `-ecosystem`;
  - `d_fr_1440_reseau_head`, `d_fr_1440_reseau_actors`;
  - `d_fr_1440_projet_chapters`, `d_fr_1440_projet_spaces`;
  - `d_fr_1440_parcours_register`;
  - `d_ar_1440_home-pathways`;
  - `d_fr_390_home-entrances`, `d_fr_390_home-pathways`, `d_fr_390_home-trust`.

  The FAQ anchors `faq_visas`, `faq_recruitment_agency`, `faq_preassessment_guarantee`, `faq_diplomas`,
  `faq_guaranteed_visa_offer` and `faq_who` all exist on `/fr/faq/`. Script and measures:
  `.work/v522-audit/director/verify.py`, `verify_measures.json`.
- **The bundle sizes of §7** were measured on the built dist of `fdd6e34` (gzip -9).
- **The audits** (`evidence/v522/`): `AUDIT_home.md` (+ `home/`), `AUDIT_pages1.md` (+ `pages1/`), `AUDIT_pages2.md`
  (+ `pages2/`), `RESEARCH.md` (+ `research_shots/`), `ICONS.md` (+ `icons_shots/`).
