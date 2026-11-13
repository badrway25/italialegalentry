# MOBILE UX — V5 council, Mobile UX Specialist

> **Erratum — ECD red-team revision, 27 Sept 2026 (`final/RED_TEAM.md` M18).** «Nothing modified» below holds for the repository's files only: this lane added seven session rows to the local `ile_qa` database (disclosed in §1 and §10 of this report). Deleting or keeping them is the owner's decision, phase 0 of `final/IMPLEMENTATION_PLAN.md` (O66).

**Role:** independent Mobile UX Specialist, requested by the product owner · **Date:** 27 September 2026 · **Repository:** `C:/tmp/italylegalentry`, `main` @ `c9a58d8`, read only — **nothing under the repository was modified**. Everything this lane produced is under `C:/tmp/ile_v5_council/` (this file, `council/mobile/`, `scratch/mobile/`).

**The question.** The owner did not accept the Mobile score of 3, nor a permanent exception for a hero taller than 130 % of the viewport at 360 and 375 px. This report measures the hero, the fold, the calls to action, the doorway composition, the navbar, the menu, the density and the scroll length on the public home and the key platform screens, then proposes two complete solutions, with target heights at 360×800, 375×812, 390×844 and 412×915, and recommends one.

---

## 0. The answer on one screen

**The owner is right, and the exception is not needed.** Measured today on the served pages:

| Hero, share of the viewport | 360×800 | 375×812 | 390×844 | 412×915 |
|---|---|---|---|---|
| 8770, interim (phase 3 closed), fr | **142.4 %** | **136.3 %** | 129.3 % | 119.2 % |
| 8771, phase 3 open, fr | **138.4 %** | 128.9 % | 124.1 % | 114.4 % |
| 8771, ar | **137.0 %** | **131.5 %** | 126.5 % | 115.4 % |
| 8771, it | **139.4 %** | 128.9 % | 124.1 % | 114.4 % |

These are percentages of the full nominal viewport, the way the gate reviewers measured. On a real phone, where the browser's own bars take 128–215 px of those heights, the same hero fills **157–176 %** of what is visible (§1.3). The CD's own target was **≤ 110 % at 390** (`CREATIVE_DIRECTION.md` §3.1, item 1). The hero misses it at all four widths, 412 included (114.4 % and 119.2 %).

There are three causes, all measured:

1. **A V1 rule leaks into the V4 hero.** `static/css/components.css:1171` gives `.hero` `padding-block: clamp(48px, 8vw, 96px)` and a hairline. `v4/hero.css` never resets it. On a phone that is **48 + 48 = 96 px of empty navy**. The door starts 72 px below the header (48 from this rule plus 24 from `.hero__inner`), not the 24 px the round-3 notes assumed. The same rule adds 61 + 61 px at 768 and 96 + 96 px at 1440. No V4 document or comment mentions it, so it is almost certainly unintended. At desktop it is now part of the approved composition, and whoever removes it there must re-measure.
2. **The phone hero carries six blocks** where the first screen can hold four: door, title, lead, two actions, a 7-line body paragraph (196 px at 390, 224 at 360) and the 2×2 legend (122 px, 154 at 360). The body and the legend together are **30–34 % of the hero**. The legend also repeats section 01 («Quatre accès», 1 450 px), which directly follows the hero.
3. **Nothing in the layout is sized against the viewport height.** The phone hero is a stack of fixed pixels (`min-block-size: 0` below 48rem), so a shorter screen can only overflow.

**Recommendation: Solution A, «Una schermata»** (§3). On a phone the hero becomes exactly one small viewport (`100svh`), minus a 32 px peek of the next chapter. The door takes whatever height the copy leaves, between 136 and 300 px, which is **+35 % over today's 223 px** at every nominal viewport. The copy is eyebrow, title, lead and two actions, sitting low where the thumb reaches. The body paragraph and the four-access legend move into section 01, whose rows already show the gloss the CD asked for. Measured with the prototype stylesheet injected into the live pages:

| Solution A, measured | 360×800 | 375×812 | 390×844 | 412×915 |
|---|---|---|---|---|
| Hero height (below the 57 px header) | **711 px** | **723 px** | **755 px** | **826 px** |
| Hero / viewport | 88.9 % | 89.0 % | 89.5 % | 90.3 % |
| Hero bottom / viewport | **96.0 %** | **96.1 %** | **96.2 %** | **96.5 %** |
| Door (w × h), phase 3 | 242 × 300 | 242 × 300 | 242 × 300 | 242 × 300 |
| Door (w × h), interim fr | 166 × 206 | 176 × 218 | 215 × 266 | 242 × 300 |
| Primary action, bottom edge (phase 3 / interim) | 688 / 688 | 700 / 700 | 732 / 732 | 803 / 803 |

The same numbers hold in fr, it, en and ar, on 8770 and 8771. **The primary action is fully visible in all 40 measured cases**: 5 page and language variants, each at the 4 nominal viewports and the 4 estimated small ones. The secondary action is visible in 39 of 40. The exception is interim fr at 375×629, where it is 28 px under the fold.

**Alternative: Solution B, «Soglia affiancata»** (§4). The door stands beside the title at 128 px wide, and the legend stays in the hero. The hero is 537 px (phase 3), which is **63.6–67.1 %** of the nominal viewport, and the next section shows 206–321 px in the first screen. It is denser and faster to act on, but the door loses 49 % of its area, and the interim title has to drop to 28 px on 6 lines. I use B's composition for the **inner landing pages**, for **phone landscape** and for the **login band**, not for the home.

**Also measured, and fixable without a waiver:**
- **Phone landscape:** the hero is 244–332 % of the height and there is no CTA in the first screen (§5).
- **Wordmark:** hidden at every width ≤ 368 px, 360 included, although it fits there with 47 px to spare (§6.1).
- **Home scroll length:** 13.1 screens at 390. The first 3 screens are the hero and section 01, which present the same four audiences twice. An empty news block adds 480 px (§7).
- **Audience landing:** `/fr/parcours/` shows its first CTA at 2 745 px (3.25 screens). The Forum shows its first at 4 242 px (§8).
- **Platform:**
  - Persistent chrome is 174 px on the case file (21.8 % of 800).
  - The bottom-bar labels are 11 px, and three of five wrap onto two lines at every width.
  - The first input of «Ma situation» sits at 772 px at 360×800, under the sticky action bar (§9).

---

## 1. Method, and what it can and cannot prove

### 1.1 What was looked at

Fourteen images were read with the Read tool, the maximum allowed. They were read one at a time, the 390-wide captures first:
- `before_home-8771_390`, `before_home-8770_390`, `before_drawer-8771_390`
- `before_dashboard_390`, `before_case_390`, `before_documents_390`, `before_situation_390`, `before_entreprise_390`
- `before_console-drawer_390`, `before_login-8771_390`, `before_parcours-8771_390`, `before_forum-8771_390`
- Two composites I built: `council/mobile/sheet_home8771_390_full.png` (the 11 080 px home in six columns, with red ticks every 844 px) and `council/mobile/sheet_now_A_B.png` (today / A / B / A interim at 375×629 / A in Arabic at 360 / the A-L variant).

Templates and CSS read:
- `templates/pages/home/_hero.html`, `templates/components/doorway.html`, `templates/partials/portal_chrome.html`
- `static/css/v4/hero.css`, `static/css/v4/tokens.css`, `static/css/components.css` (the `.hero` rule), `static/css/v2/shell.css` (the lock-up breakpoints), `static/css/main.css` (import order)
- `docs/design-v2/BRAND_ASSETS.md` §2, `docs/design-v4/CREATIVE_DIRECTION.md` §3.1 and §4.5, `docs/design-v4/README.md` (gate A rounds 2–7)
- The council's `CAPTURES_AND_REFERENCES.md`, `21st_nav-shell.md`, `21st_hero-public.md`, `IMAGERY.md`, `MOTION.md` and `TYPOGRAPHY.md`

### 1.2 How it was measured

- **A separate browser.** I used a separate headless Chrome 153 on port **9355** with its own profile, `scratch/chrome-profile-mobile/`. The QA Chrome on 9222, and the motion lane's Chrome on 9333, were never contacted.
- **Client.** The project's `scripts/cdp.py`, imported read-only with `PYTHONDONTWRITEBYTECODE=1`, so no `__pycache__` was written into the repository.
- **Emulation.** `Emulation.setDeviceMetricsOverride` with `mobile: true`, DPR 2 and touch emulation. The pages were served by 8770 (`ile`, interim) and 8771 (`ile_qa`, phase 3 open), with the cache disabled.
- **Platform sessions.** They were minted server-side in `ile_qa` with the same method as `scripts/qa_chrome_signin.py`. No password was typed, no form was submitted, and the cookie went only to the isolated browser. Side effect: seven session rows were added to `ile_qa`'s session table.
- **The prototypes are CSS only.** Each was injected after load as a `<style>` element, with `Page.setBypassCSP` switched on in that browser only. Nothing was served differently, and nothing was written anywhere but `scratch/mobile/`.
- **What moves.** A and B move two blocks out of the hero (the body paragraph, and in A the legend). The prototype hides them; the real change is a template change (§3.3).
- **Scripts and logs:**
  - `m1_public.py` → `log_m1_public.json` (public, 4 widths)
  - `m3_platform.py` → `log_m3_platform.json` (platform, 4 widths)
  - `m5_nav.py` (header and drawer)
  - `m6_proto.py` → `log_m6_proto.json` (today / A / B)
  - `m7_proto.py` (A2 and A-L variants)
  - `m9`–`m12` (final A with the lever and the centred door → `log_m12_a_v5.json`)
  - `m13_edges.py` (320 px and landscape)
  - `m11_situation.py` (preamble of «Ma situation»)
  - `m8_lockup.py` (wordmark)

### 1.3 Nominal and «small» viewports

The four viewports the owner named are DevTools device sizes: the whole screen, in CSS px. On a real phone the browser's bars take part of that height. `100svh` is exactly the visible height with those bars shown, which is why Solution A uses it. I measured every proposal twice: at the nominal size, and at an **estimated small viewport** with the bars shown:

| Nominal | Estimated small viewport | Basis of the estimate |
|---|---|---|
| 360×800 | **360×672** | Chrome Android: 24 status + 56 URL bar + 48 three-button navigation |
| 375×812 | **375×629** | iPhone 12/13 mini, Safari with the bottom toolbar expanded |
| 390×844 | **390×664** | iPhone 12–15, Safari with the bottom toolbar expanded |
| 412×915 | **412×787** | Chrome Android: 24 + 56 + 48 |

**These four heights are estimates of typical browser chrome, not device measurements.** They must be checked on at least one iPhone and one Android phone before any claim is signed (§11).

### 1.4 21st.dev

The two relevant catalogues had already been curated by the council (`21st_nav-shell.md`, `21st_hero-public.md`). This lane made **2 `search` calls** («mobile full screen hero…», «sticky bottom action bar mobile…») and **1 `get_component`** (#26796 «Hero 12»). **`generate` and `iterate_generation` were not called.** How each pattern is classified is in §3.6, §6 and §9.

---

## 2. Today, measured

### 2.1 Where the 1 047 px of the hero go (8771, fr, 390×844)

| Block | px | Note |
|---|---|---|
| V1 `.hero` padding, top | 48 | `components.css:1171`, never reset by V4 |
| `.hero__inner` padding, top | 24 | |
| Door (SVG, cropped viewBox 368 × 456) | 223 | 180 px wide: arch, photograph, navy inner arch, key, three steps |
| Gap | 20 | |
| Title, 2 lines at 44 px | 85 + 24 | |
| Lead, 2 lines | 56 + 16 | |
| Actions (8 + 44 + 12 + 44 + 24) | 132 | primary 561–605, secondary 617–661 |
| **Body paragraph, 7 lines** | **196** | 224 at 360 (8 lines) |
| Gap | 20 | |
| **Legend 2×2** | **122** | 154 at 360: rows 44 / 56 / 56 / 76 |
| `.hero__inner` padding, bottom | 32 | |
| V1 `.hero` padding, bottom | 48 | |
| **Total** | **1 047** | 124.1 % of 844 |

### 2.2 Findings on the public home

| # | Finding | Evidence |
|---|---|---|
| M1 | **Leaked V1 padding**: 96 px on phones (48 + 48), 122.9 at 768 (61.44 × 2), 192 at 1440 (96 × 2, inside the border-box `min-block-size`). | `.hero` computed `padding-top: 48px` at 390; `96px` at 1440 (`m2_herobox.py`, `m14_desk.py`) |
| M2 | **Six blocks in the phone hero.** The body and the legend are 318–378 px, 30–34 % of it. The legend is a key without its diagram: on phones the routes are not drawn (`.is-compact .doorway__routes { display: none }`), so four coloured nodes point at nothing. | §2.1; `hero.css` «Responsive» block |
| M3 | **The door is small and far away.** It is 180 × 223, only 21 % of the hero, and starts 72 px under the header. The CD asked for 220 px wide (§4.5). It is also the only image on every public phone page. | captures `before_home-*_390`, §2.1 |
| M4 | **The legend wraps at 360.** «Universités & Formation» takes 3 lines (76 px). The Italian cell takes 96 px. The CD's «gloss always visible» (§4.5) is not delivered: the gloss is visually hidden at every width. | `legendRows` in `log_m1_public.json` |
| M5 | **The CTA on the interim home (8770).** Primary at 733–777, secondary at 789–833 at 360×800: the secondary is outside even the nominal 800. On every estimated small viewport except 412 both are outside. On 8771 the primary (561–605) is inside every fold. | `log_m6_proto.json` («current») |
| M6 | **Share of what is actually visible** (hero height / estimated small viewport): 157.7–166.5 % (8771 fr), 164.3–176.0 % (8770 fr) at 360/375/390; 133.0–138.6 % at 412. | same, «small» rows |
| M7 | **The navbar is fine at 57 px** (6.2–7.1 % of the viewport, sticky, Menu 44 px). But **the wordmark is hidden at ≤ 368 px**: `v2/shell.css:187` hides `.lock__text` below 23rem, a breakpoint written for 320 px. At 360 the complete lock-up measures 227 px and fits with 47 px to spare before the Menu button, with no horizontal scroll. | `m5_nav.py`, `m8_lockup.py` |
| M8 | **The public drawer puts utility before navigation.** The promoter line, «Espace réservé» and the language control come first; navigation starts at y 278, after 221 px of utility. Rows are 52 px tall, text only: no glyph, no description, no primary action (the orientation questionnaire). Sub-menus are split rows (link 268 + chevron 52), which is correct for access. The console drawer (`before_console-drawer_390`: groups, glyph rows, language and «Site public» at the foot) is the model to follow. | `before_drawer-8771_390`, `m5_nav.py` |
| M9 | **Scroll length**: 11 080 px = **13.1 screens** at 390×844 (8771); 7 728 = 9.2 (8770); 11 518 = 14.4 at 360×800. **The four audiences are presented twice in the first 3 screens**: the hero legend (901–1 023) and the section 01 cards (1 104–2 554, 1 450 px). One of them appears a third time as the hero's secondary action («Espace entreprises»). An empty «Actualités» section takes 480 px («Aucune actualité publiée pour le moment»). The footer takes 1 306 px. | `log_m1_public.json` (`secs`), contact sheet |
| M10 | **Phone landscape is broken today.** At 667×375 the hero is 243.5 % of the height (phase 3) and 269.9 % (interim). At 844×390 it is 303.8 % and 331.8 %, and there is **no CTA in the first screen** in any of the four cases. | `m13_edges.py` |
| M11 | **320 px** (the oldest iPhone SE): 208–215 % and no CTA in the first screen. | `m13_edges.py` |

---

## 3. Solution A — «Una schermata» (recommended)

### 3.1 The idea

On a phone the first screen is the portico. The owner's door, at up to 300 px, stands in the navy, with the locked title, the lead and the two actions under it, low in the screen where the thumb is. The hero ends where the visible screen ends, less 32 px through which the cream edge of chapter 01 and its gold hairline show: the page never looks finished, and no animated scroll cue is needed. Nothing is clipped. The hero's height is a **minimum**, so at 200 % text size (WCAG 1.4.4 and 1.4.10) it grows instead of cutting.

It keeps and strengthens the brand grammar. `BRAND_ASSETS.md` §2 allows a mobile composition of its own («ritaglio, viewBox, quantità di elementi»). The arch, the photograph, the key and the three steps are all kept, and larger. It is the CD's own phone order (§4.5: the door alone, then the title), with the height problem solved.

### 3.2 The stylesheet (prototype, measured)

The prototype is `council/mobile/solution_a_una_schermata.css`. It applies below 48rem and only affects the hero:

```css
.hero { padding-block: 0; border-block-end: 0;                       /* the V1 leak, closed */
        min-block-size: calc(100vh  - 57px - 2rem);
        min-block-size: calc(100svh - 57px - 2rem); }                  /* one small viewport, minus a 32px peek */
.hero__inner { display: flex; flex-direction: column; padding-block: var(--s-4) var(--s-6); gap: var(--s-5); }
.hero__stage .doorway { order: -1; flex: 1 1 0; margin-block: auto; align-self: center;
        min-block-size: clamp(8.5rem, 22svh, 10.5rem);                 /* 136–168px, follows the small viewport */
        max-block-size: 18.75rem;                                      /* 300px */
        inline-size: auto; max-inline-size: 100%; aspect-ratio: 368 / 456; }
.hero__copy { flex: none; }
.hero__body, .doorway-legend { display: none; }                        /* prototype only: they MOVE (§3.3) */
@media (max-height: 43.75rem) { [data-hero-variant="interim"] .hero__title { font-size: 2rem; } }
```

For production:
- Replace `57px` with a token (`calc(var(--header-h) + 1px)` once the phone header token is confirmed at 56 + 1).
- Replace `2rem` with `--hero-peek`.
- The flex column is deliberate. The door is `flex: 1 1 0` with a floor and a ceiling, so it absorbs whatever the copy leaves in any language, with no per-locale constants and no JavaScript.

### 3.3 What moves (template, not CSS)

- **The body paragraph** (`d.body`, the ecosystem description) leaves the phone hero. It becomes the lead of section 01 («L'écosystème — Quatre accès»), or of the ecosystem section, whichever the content owner prefers. It is moved, not cut: the text is prescribed copy.
- **The legend**: on phones, section 01 becomes the four-access list with the legend's grammar. Each row has a route-colour node, a glyph, the word, **the gloss visible**, and an arrow, with the whole row as the target (≥ 64 px). That list replaces today's four 360 px cards. It delivers the CD §4.5 promise that the V4 hero never kept on phones (gloss always visible), and it removes the duplication in M9.
- The hero legend stays in the markup from 48rem up, where the routes are drawn. `home.js` must tolerate a legend that is not rendered below 48rem. The prototype could not test this (it injects after `home.js` has run), so it is an implementation check.

### 3.4 Numbers (targets, all measured on the prototype)

**At the nominal viewports.** The hero's height is below the 57 px header; the bottom edges are measured from the top of the page.

| | 360×800 | 375×812 | 390×844 | 412×915 |
|---|---|---|---|---|
| **Target hero height** | **711** | **723** | **755** | **826** |
| Hero bottom (= viewport − 32) | 768 (96.0 %) | 780 (96.1 %) | 812 (96.2 %) | 883 (96.5 %) |
| Door, phase 3 (fr/it/en/ar) | 242 × 300 | 242 × 300 | 242 × 300 | 242 × 300 |
| Door, interim fr / it | 166 × 206 / 144 × 178 | 176 × 218 | 215 × 266 / 230 × 285 | 242 × 300 |
| Primary bottom | 688 | 700 | 732 | 803 |
| Secondary bottom | 744 | 756 | 788 | 859 |
| Today's hero, for comparison (8770 / 8771) | 1 139 / 1 107 | 1 107 / 1 047 | 1 091 / 1 047 | 1 091 / 1 047 |
| Saved | −428 / −396 | −384 / −324 | −336 / −292 | −265 / −221 |

**At the estimated small viewports** (browser bars shown):

| | 360×672 | 375×629 | 390×664 | 412×787 |
|---|---|---|---|---|
| Hero bottom, phase 3 (fr/it/en/ar) | 640 (95.2 %) | 597 (94.9 %) | 632 (95.2 %) | 755 (95.9 %) |
| Door, phase 3 fr / ar | 195 × 242 / 179 × 221 | 160 × 199 / 144 × 178 | 189 × 234 / 172 × 213 | 242 × 300 |
| Primary / secondary bottom, phase 3 | 560 / 616 | 517 / 573 | 552 / 608 | 675 / 731 |
| Hero bottom, interim fr (with the 2rem lever) | 690 (102.7 %) | 681 (108.3 %) | 673 (101.4 %) | 755 (95.9 %) |
| Primary / secondary bottom, interim fr | 610 / 666 | 601 / **657 (out by 28)** | 593 / 649 | 675 / 731 |

Two further checks:
- **Interim** carries the 5-line title plus an eyebrow that wraps to two lines. That is why it needs the `max-height` lever. Without the lever, the primary is still visible everywhere (bottom 612–630) and the hero reaches 104–111 % on the short screens. Interim ar and it with the lever: 95–103 %, both actions visible.
- **320×568:** phase 3 is 98.9 % with both actions visible. Interim is 119.5 % with the primary at 599 (out by 31). This is the one case where the interim title would need the typography lane's help, for example the Source Serif 4 setting in `TYPOGRAPHY.md`.

### 3.5 What A costs and risks

- **LCP**: nothing new is requested. The LCP element (the door photograph, `doorway-arch-400.webp`, 400 × 533, 42 KB) is drawn larger:
  - At DPR 2 the arch shows about 420 × 562 device px, which is 1.05× the file (fine).
  - At DPR 3 it shows about 631 × 843 device px, **1.58× the file**. Softness may be acceptable under the 0.5 opacity and the veil, but it must be judged on a DPR 3 phone. If it looks soft, use a 600-wide arch strip, preferably AVIF (inside `<image>`, no `srcset`). That is about +25–45 KB, roughly +0.15–0.25 s on slow 4G against 1.42–1.82 s measured after `ac92427`, so still inside the 2.5 s budget. Re-measure before committing.
- **CLS**: `svh` does not change when the bars slide, so no shift from that. **Never use `dvh` here.** The door's size is fixed by the first layout, with no JavaScript. A font swap that changes the copy's height is absorbed by the door, which then moves by a few pixels. With the metric-matched fallbacks proposed in `TYPOGRAPHY.md` §9.4 this should stay near 0, but it was not measured under throttling.
- **INP / long tasks**: nothing is added.
- **Motion**: none added. The ambient current is not drawn on phones today (routes hidden), and the existing scroll-linked drift of the photograph stays. An optional «door settles as you scroll» (`animation-timeline: view()`, `transform`/`opacity` only, inside `@supports` and `prefers-reduced-motion: no-preference`) is handed to the Motion lane. It is not needed for the height.
- **RTL**: measured in `ar`; the title aligns to the end, the door is not mirrored (as today), and the actions keep the arrow flip.
- **Reduced motion, forced colours, no-JS**: this is layout only, so they should be unaffected. The prototype was not measured under those three modes.
- **The CD's signature** is needed on one point: the legend leaves the phone hero, for section 01. That point is also the one that finally delivers «gloss always visible» (§4.5).

### 3.6 Patterns

- **21st #26796 «Hero 12»** (code read): the copy and CTA are anchored to the bottom of an image hero. **Class A** for that principle, done in CSS. **Class D** for its motion (a `filter: blur` reveal, and text at opacity 0 until JavaScript runs, which `MOTION.md` rule 11 forbids) and for its fixed `min-h-[560px]`, which ignores the viewport.
- Hero curation **#2061 «Smooth Scroll Hero»**: only for the optional scroll-linked settle, **class B** (Motion) or CSS scroll-timeline, owned by the Motion lane.
- **No React island.**

---

## 4. Solution B — «Soglia affiancata» (the alternative)

### 4.1 The idea

An editorial cover: the door (128 px wide) stands at the inline end beside the title, with lead and actions full width under them, and the four-access legend kept in the hero, 2×2, without the 16 px route trait. The hero sizes to its content and the next chapter enters the first screen. The body paragraph leaves the hero, as in A.

### 4.2 The stylesheet (prototype, measured)

The prototype is `council/mobile/solution_b_soglia_affiancata.css`, below 48rem. It is a grid with areas `"eyebrow door" "title door" "lead lead" "actions actions" "legend legend"`, columns `1fr 8rem`, `.hero__copy { display: contents }`, and the interim title at 1.75rem (28 px).

### 4.3 Numbers (measured)

| | 360×800 | 375×812 | 390×844 | 412×915 |
|---|---|---|---|---|
| **Target hero height, phase 3** (fr/it/en) | **537** | **537** | **537** | **537** |
| Hero / viewport | 67.1 % | 66.1 % | 63.6 % | 58.7 % |
| Next section visible in the first screen | 206 px | 218 px | 250 px | 321 px |
| Hero, ar | 537 | 525 | 525 | 525 |
| Hero, interim fr (title 28 px, 6 lines) | 627 | 627 | 611 | 611 |
| Door | 128 × 159 | 128 × 159 | 128 × 159 | 128 × 159 |
| Primary / secondary bottom, phase 3 | 372 / 428 | 372 / 428 | 372 / 428 | 372 / 428 |
| Legend rows at 360 (today 44/56/56/76) | 44 / 44 / 44 / 56 | | | |

On the estimated small viewports the phase 3 hero is 68.2–85.4 % of the height (bottom edge 75.5–94.4 %). Interim is 77.6–99.7 % (bottom edge up to 108.7 % at 375×629). Both actions are visible everywhere. At 320×568 the interim title runs to **9 lines**: B does not work for interim at 320. In landscape at 667×375, B is the only composition that puts the primary inside the screen (bottom 344 phase 3, 375 interim).

### 4.4 What B costs

- The door's area drops by 49 % (128 × 159 against 180 × 223 today, and against 242 × 300 in A): less image in the first screen, which works against «image-rich».
- It needs **a CD signature**: CD §4.5 says the door comes first and alone.
- It needs **a typography decision**: the interim title drops from 36 to 28 px.
- The legend on phones stays a key without its diagram (M2).

---

## 5. A and B side by side, and the recommendation

| Criterion | Today | **A «Una schermata»** | B «Soglia affiancata» |
|---|---|---|---|
| Hero, 360×800 (phase 3 / interim) | 138 % / 142 % | **89 % / 89 %** (bottom 96 %) | 67 % / 78 % |
| Hero, 375×812 | 129 % / 136 % | **89 % / 89 %** | 66 % / 77 % |
| Hero, 390×844 | 124 % / 129 % | **89.5 % / 89.5 %** | 64 % / 72 % |
| Hero, 412×915 | 114 % / 119 % | **90 % / 90 %** | 59 % / 67 % |
| Primary / secondary visible, 40 measured cases (5 variants × 8 viewports) | 37 / 28 (the 3 primary misses: interim fr at 360×672, 375×629, 390×664) | **40 / 39** | 40 / 40 |
| Door on screen (phase 3, 390×844) | 180 × 223 | **242 × 300 (+81 % area)** | 128 × 159 (−49 %) |
| First-screen premium feel | image small, text-heavy | **image-led, calm, one decision** | editorial, dense |
| Presentations of the four audiences in the first 3 screens | 2 (legend + section 01), plus one audience again as the secondary action | 1 (section 01, at the fold) | 2 (legend + section 01) |
| Brand composition (arch, photograph, key, steps) | kept | kept, larger | kept, smaller |
| CD signatures needed | the waiver (refused) | legend → section 01 on phones | door beside title; interim title 28 px |
| Engineering | — | CSS + moving two blocks in the template | CSS + moving the body |
| Risks | — | DPR 3 sharpness (§3.5); `home.js` without a legend below 48rem | smaller LCP image; 320 px interim |

**Recommendation: A for the home.** It is the only option that shrinks the hero while enlarging the image, which is what the owner is asking for (premium, image-rich, memorable), and it makes the waiver unnecessary at every width. Take B's composition where A is the wrong tool:
- **phone landscape**: `@media (orientation: landscape) and (max-height: 30rem)`, at every width, because 844×390 is above 48rem, so A's rules do not reach it. Door beside the copy, height `min(100svh − header − 2rem, 300px)`. This rule was not measured at 844×390. B's grid at 667×375 measured 117.6 % of the height for phase 3 and 125.9 % for interim, with the primary inside (bottom 344 and 375 px);
- **inner landing pages** (§8);
- **the login band**, which already works this way.

A variant, **A-L** (A with the 2×2 legend kept under the actions), was measured too. It fills the nominal viewports exactly for phase 3, but on the estimated small viewports the interim hero reaches 101.5–124.8 % of the height (bottom edge 108.8–133.9 %), so it is not recommended.

---

## 6. Navbar and menu (public)

### 6.1 Keep the wordmark at 360

Change `@media (max-width: 23rem) { .lock__text { display: none } }` in `v2/shell.css` to **`21.5rem`** (344 px). Measured at 360: lock-up 20–247, Menu button 294–340, no horizontal scroll. The wordmark then disappears only below 344 px (320 px devices), where it truly does not fit. This keeps the brand name on the most common Android width; the wordmark font itself is untouched.

### 6.2 Header

Keep it sticky at 57 px (≤ 7.1 % of the viewport). On phones, no compaction and no utility row. Hide-on-scroll-down is **not** recommended: the Menu button is the only way to the navigation, and the header is small.

### 6.3 Drawer, re-ordered like the console drawer

- **Order.** The four audiences first, each as a 64 px row with glyph, word and a one-line description. Then Forum, Actualités and Projet (52 px). Then **one primary action** («Découvrir le questionnaire d'orientation»). At the foot: «Espace réservé», the language grid and the promoter line.
- **Where navigation starts.** At y ≈ 73 instead of 278. The whole drawer fits in 743 px at 360×800 without scrolling.
- **Sub-menus.** Keep the split row (link + 52 px chevron). Use the idea of #22313 from the nav curation, **class A**: the tapped row stays in place as a breadcrumb and its children indent under it. Leave out its per-character animation, which breaks Arabic joining (class D).
- **Focus and scroll mechanics.** From #23558 (`inert` on siblings, focus return, Escape, `overscroll-behavior: contain`), **class A** in the existing `main.js`.
- **No new motion** beyond the existing drawer slide.

---

## 7. The rest of the home on a phone: scroll length

**Targets** at 390×844. The hero figure is measured on the prototype; the other section figures are **estimates of the proposed change**, not prototypes.

| Section (8771) | Today | Target | How |
|---|---|---|---|
| Hero | 1 047 | **755** (measured) | Solution A |
| 01 Quatre accès | 1 450 | ≈ 850 | four 96 px rows with gloss plus the moved body paragraph, instead of four 360 px cards |
| 02 Orientation | 550 | 550 | keep |
| 03 Les parcours réguliers (8 rows) | 1 583 | ≈ 900 | two-line rows of 64 px, the detail in `<details>` |
| Pilote Vénétie–Maroc (voyage) | 1 013 | 1 013 | signature, keep (journey prototype in `MOTION.md`) |
| 04 Transparence / FAQ | 1 508 | ≈ 850 | questions as `<details>`, the legend strip kept |
| Anti-fraud | 907 | 907 | compliance text, not shortened |
| 05 Actualités | 480 | **0 when empty** | do not render an empty news block on the home |
| 06 Écosystème | 840 | 840 (+ imagery) | `IMAGERY.md` below the fold |
| Espace réservé | 290 | 290 | |
| Footer | 1 306 | ≈ 700 | link groups as `<details>` on phones; legal links always visible |
| **Page** | **11 080 (13.1 screens)** | **≈ 7 800 (≈ 9.2 screens)**, ≤ 9.5 with the V5 imagery | −30 % |

Interim (8770): 7 728 px (9.2 screens) → ≈ 5 500 px (≈ 6.5 screens), using the same levers on its sections (banner 267, entrances 1 250, orientation 843, pathways 950, trust 1 337, ecosystem 729, footer 1 156).

---

## 8. Inner public pages

- **`/fr/parcours/` (Espace Personnes).** At 390:
  - The H1 is 32 px on 3 lines.
  - The serif lead runs 10 lines in grey.
  - The **first CTA is at 2 745 px (3.25 screens)**, 2 796 at 360.

  Target: **first primary action at ≤ 600 px at 390×844 and ≤ 560 px at 360×800**, inside every estimated small viewport. How: B's «soglia» band (eyebrow, title, the first sentence of the lead, «Commencer le questionnaire d'orientation», and an arch-window image per `IMAGERY.md`), with the rest of the compliance lead directly under it and unchanged.
- **Forum (`/fr/forum/`).**
  - The breadcrumb takes 60 px.
  - The navy band is 430 px with the date and place (good).
  - The **first CTA is at 4 242 px**.
  - The sticky local nav cuts «POURQUOI ITALY LEGAL E» without a fade.

  Target: «Manifestez votre intérêt» inside the navy band (≤ 560 px at 360×800). The breadcrumb on phones becomes a single 36 px back link. The local nav gets `--mask-fade-end` (already a V4 token, mirrored in RTL).
- **Login.** The 120 px band with the small arch and the help card already works on the phone (`before_login-8771_390`). Keep it: it is B's grammar at its smallest.

---

## 9. Platform screens

### 9.1 Measured (DPR 2, touch; qa-doc-person and qa-company on 8771)

| Screen | H1 (top–bottom) | Primary action (viewport px) | First field | Page length, screens (360 / 375 / 390 / 412) |
|---|---|---|---|---|
| Dashboard | 109–141 | «Continuer» 197–241 | — | 3.9 / 3.8 / 3.6 / 3.3 |
| Case file EE167596D4 | 101–133 | «Continuer» in the fixed bar: 692–736 / 704–748 / 736–780 / 807–851 | — | 3.6 / 3.5 / 3.4 / 3.1 |
| Mes pièces | 97–129 | «Remplacer la pièce» 233–277 | search 601 | 3.5 / 3.3 / 3.1 / 2.9 |
| Ma situation | 81–113 | «Continuer» in the sticky foot: 686–730 / 703–747 / 735–779 / 780–824 | **772 / 756 / 684 / 684** | 2.2 / 2.0 / 1.8 / 1.7 |
| Guichet numérique | 113–149 | «Ouvrir une demande» 529–573 | — | 1.6 / 1.5 / 1.5 / 1.3 |
| Academy | 141–177 | none (a catalogue) | — | 3.9 / 3.8 / 3.5 / 3.2 |
| Entreprise (qa-company) | 101–133 | «Ouvrir le besoin» 217–261 | — | 3.7 / 3.6 / 3.3 / 3.1 |

Fixed chrome:
- The console bar is 57 px and the bottom bar 56 px on every screen.
- The case file adds a 61 px action bar: **174 px of persistent chrome, 21.8 % of 800 and 20.6 % of 844**.
- The bottom-bar labels are **11 px**. «Tableau de bord», «Mes documents» and «Communications» take **two lines (26 px) at every width, 412 included**, and the captures show «Communica-tions» hyphenated.
- **The top-left ≡ and the bottom-bar «Menu» both open `#console-drawer`** (`portal_chrome.html:33` and `:53`).

No horizontal overflow on any screen.

### 9.2 Recommendations and targets

1. **Persistent chrome ≤ 15 % of the viewport (≤ 120 px at 360×800).** When a page action bar is present (case file, wizard), it takes the bottom bar's place (with `env(safe-area-inset-bottom)`): 57 + 61 = **118 px**, against 174 today. The pattern is **class A**; there is no 21st component for it. The two sticky-bar searches returned floating action buttons, **class D**: the council already rejects a floating CTA over content.
2. **Bottom bar: one line, ≥ 12 px.** Shorter labels are a copy decision for the owner and CD, already open in the V4 README, for example «Accueil · Dossiers · Pièces · Messages · Menu». Target: label height 16 px. Pattern #27897 «Mobile Navigation Tabs» (nav curation, icon + label always visible), **class A**. Remove the duplicate ≡ in the top bar on phones: the bottom «Menu» is in the thumb zone, and the tile top-left becomes the way back to the dashboard.
3. **Ma situation: first input at ≤ 520 px at 360×800 and ≤ 480 at 390×844** (today 772 and 684). At 360 the input sits under the sticky foot, whose top is at 671. The measured preamble at 360:
   - title and lead 160;
   - margins 24 + 16;
   - the recalculation note 89, plus 16 + 16;
   - the form's 48 px top margin;
   - the progress rail at 181 (eight dots plus a 3-line count sentence).

   Levers:
   - move the note into a `<details>` «Comment ces informations sont utilisées» under the form (−121);
   - take the form margin from 48 to 16 (−32);
   - turn the rail into one line «Question 1 sur 8» plus the dots (≈ 64, −117).

   The «sur 7» / «1 / 8» mismatch is already an open owner decision.
4. **Case file:** the vertical 7-step stepper is ≈ 480 px, the whole first screen. On phones, show a current-step card (≈ 200 px: «Étape 1 sur 7 · Maroc · Votre situation et votre objectif · Vous êtes ici») plus «Voir les 7 étapes» in `<details>`. Target: the first file section starts within the first screen at 390×844.
5. **Dashboard:** the «Dossier» card is a vertical definition list of 225 px. Make it a 2-column key/value grid (≈ 120 px). Target: «Mon parcours» starts above the bottom bar at 390×844 (today its title is at ≈ 765 and the bar starts at 788).
6. **Entreprise:** put «Ouvrir le besoin» inside the «Votre prochaine action» card that explains it. Today the button comes first and its context 180 px later. The page keeps one primary.
7. **Mes pièces:** the bar says «Mes documents» and the H1 says «Mes pièces». Align the names (copy decision).
8. **Loading on the phone.** A skeleton for asynchronous lists, following the timing rules of #23557 already selected in the nav curation (class A). No full-screen loader: the budget allows none.

---

## 10. Acceptance tests for «Mobile ≥ 4»

These are written so a gate reviewer can run them. Each is measurable with the scripts in `scratch/mobile/`.

1. **Public home hero bottom ≤ 100 % of the viewport** at 360×800, 375×812, 390×844 and 412×915, in fr, it, en and ar, on the interim and phase-3 homes. On the estimated small viewports (360×672, 375×629, 390×664, 412×787): ≤ 100 % in phase 3, ≤ 110 % in interim.
2. **The primary action is fully visible** (bottom ≤ viewport) in every case of test 1. The secondary is visible at every nominal viewport.
3. **The door keeps arch, photograph, key and three steps**, and is never smaller than 136 px tall at a nominal viewport.
4. **Every public landing page** (home, the four audience pages, Forum) shows its primary action in the first 560 px at 360×800.
5. **Landscape phones** (667×375 and 844×390): the primary action is inside the first screen.
6. **Persistent chrome** on platform screens ≤ 120 px at 360×800. Bottom-bar labels on one line, ≥ 12 px.
7. **The first form input on «Ma situation»** sits above the sticky action bar at 360×800.
8. **Home length** ≤ 9.5 screens at 390×844 (phase 3) and ≤ 7 (interim).
9. **Measured after the change, not assumed:**
   - no horizontal scroll from 320 to 430 px;
   - touch targets ≥ 44 px (the project's rule), and never below 24 px (WCAG 2.5.8);
   - CLS ≤ 0.10 and LCP ≤ 2.5 s on slow 4G + CPU ×4;
   - the same checks under reduced motion, in forced colours and without JavaScript.

---

## 11. What was not done, and why

- **No real device.** The small-viewport heights (§1.3) are estimates of typical browser chrome. An iPhone (Safari, bottom toolbar) and an Android phone (Chrome, 3-button navigation) must confirm both the A and B numbers, and the DPR 3 sharpness of the door in A.
- **The prototypes are CSS injected after load.** They hide the blocks that the real change moves. Not tested:
  - the template move itself;
  - `home.js` with no rendered legend below 48rem;
  - the no-JavaScript first frame;
  - forced colours;
  - reduced motion;
  - the phone landscape rule at 844×390 (above 48rem, so the prototype did not reach it).
- **LCP, CLS and INP were not re-measured** for A or B under throttling: the images and scripts are unchanged, but the door is drawn larger.
- **Section targets outside the hero (§7) are estimates**, not prototypes.
- **Image reads.** All 14 allowed reads were used: 12 captures plus 2 composites. Screenshots of the other prototype states exist in `scratch/mobile/proto/shot_*.png` but were not viewed. Their numbers come from the DOM, not from looking at them.
- **Loading filmstrips at 390** (`before_loading-*_390_*`) were not viewed, for the same reason. Mobile loading is covered only by the principles in §9.2.8 and by `MOTION.md`.
- **The tablet (768×1024) hero is 114 % of the height**, partly because of M1. It is outside this lane and flagged for the desktop and tablet review.
- **Side effects outside the council folder:** 7 session rows in the local `ile_qa` database (the same method the capture role used), and a headless Chrome process on port 9355, stopped at the end of this lane.

**Decisions this report needs from the owner and CD:**
- adopt A (or B) and sign its CD point;
- the 2rem interim-title lever on short screens (with the typography lane);
- the wordmark breakpoint 23rem → 21.5rem;
- the bottom-bar labels;
- hiding the «Actualités» section when it is empty;
- where the hero's body paragraph goes (section 01 or the ecosystem section).

---

## Appendix — files

| Path | What |
|---|---|
| `council/MOBILE_UX.md` | this report |
| `council/mobile/solution_a_una_schermata.css` | Solution A prototype (recommended), as measured |
| `council/mobile/solution_b_soglia_affiancata.css` | Solution B prototype, as measured |
| `council/mobile/sheet_now_A_B.png` | today / A / B / A interim at 375×629 / A in Arabic at 360 / A-L, as rendered |
| `council/mobile/sheet_home8771_390_full.png` | the whole 8771 home at 390, six columns, a tick every 844 px |
| `scratch/mobile/mcdp.py` | CDP helper pinned to the isolated Chrome on 9355 |
| `scratch/mobile/m1_public.py`, `log_m1_public.json` | public pages at four widths |
| `scratch/mobile/m3_platform.py`, `m3_platform_mint.py`, `log_m3_platform.json` | platform screens at four widths (server-side session, no password) |
| `scratch/mobile/m5_nav.py`, `m8_lockup.py` | header, drawer, wordmark |
| `scratch/mobile/m6_proto.py` … `m13_edges.py`, `log_m6_proto.json`, `log_m7_proto.json`, `log_m9_afinal.json`, `log_m10_alever.json`, `log_m12_a_v5.json`, `log_m13_edges.json` | prototype measurements |
| `scratch/mobile/m11_situation.py` | «Ma situation» and case-file layout breakdown at 360 |
| `scratch/mobile/proto/*.css`, `proto/shot_*.png` | every prototype variant and its screenshots |
