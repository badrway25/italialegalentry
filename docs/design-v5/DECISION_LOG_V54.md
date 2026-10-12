# DECISION LOG V5.4 — DL54

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» (the owner's directive of 4 October 2026, 20:20) · created by W1-0,
the steward, on 4 October 2026 · plan: `docs/design-v5/V5_4_EXECUTION_PLAN.md` (committed `889c6b1`).

**What it is.** V5.4's own decision log. The plan's header defines it — «DL54 `docs/design-v5/DECISION_LOG_V54.md` —
V5.4's own decision log, created by W1-0 with the entries of §8.3; where DL54 and an R/ rule disagree, DL54 binds the
reviewers» — and §8.3 lists what it receives before W1-A. Entry DL54-01 is the orchestrator's correction to the plan's ref
names; DL54-02 … DL54-16 are §8.3's fifteen entries, in §8.3's order.

**How it is kept.**
- **Append-only.** A later decision is a new entry at the end. No entry is edited in place: a reversal or a correction is
  a new entry that names the one it replaces («supersedes DL54-nn»).
- **Who writes.** The Creative Director, inside a family, for a question met during the build (plan §5.2: one entry, with
  its reason and its evidence) and for a trigger that fires (plan §1, head: the measured condition and the chair who
  verified it); the steward, for the infrastructure. Entries reach design-v5 through the steward's merge: every family
  holds an append-only slice of this file in `docs/design-v5/OWNERSHIP_V54.json`.
- **Form.** `DL54-nn · date · title`, then **Decision**, **Why** where the source does not already say it, and
  **Source** — the plan section(s), the red-team finding, the directive line.
- **Abbreviations** as in the plan's header: V54 l.N = line N of `C:/tmp/ile_v5_council/directives/V5_4_EXECUTION_MODE.md`;
  RTD-… / RTE-… = the design and engineering red teams (plan §8.1, §8.2); TS, LS, HF, HET, CDV, BA as the plan defines
  them.

| # | Date | Decision | Source |
|---|---|---|---|
| DL54-01 | 4 Oct 2026 | Ref names: branches `v54-<family>`; tags `v54/<family>`, `v54/<family>-pre-propagation`, `v54/base` | orchestrator's correction to §2.2 and §5.1 step 9 |
| DL54-02 | 4 Oct 2026 | The generic-AI test has eighteen symptoms | §8.3 item 1 |
| DL54-03 | 4 Oct 2026 | Six scales everywhere, N17 and L13 included | §8.3 item 2 |
| DL54-04 | 4 Oct 2026 | CLS: ≤ 0.10 every page, ≤ 0.05 flagships, font swap ≤ 0.01; 0.01 elsewhere a target | §8.3 item 3 |
| DL54-05 | 4 Oct 2026 | `--ease-turn` = `cubic-bezier(0.77, 0, 0.175, 1)` | §8.3 item 4 |
| DL54-06 | 4 Oct 2026 | The hero's three files | §8.3 item 5 |
| DL54-07 | 4 Oct 2026 | BA §1 amended: the mark moves «once, at the entrance, across the page load» | §8.3 item 6 |
| DL54-08 | 4 Oct 2026 | «Never mirrors» = never held, drawn or served mirrored | §8.3 item 7 |
| DL54-09 | 4 Oct 2026 | M10's letter yields to V54 l.19; its reasons hold | §8.3 item 8 |
| DL54-10 | 4 Oct 2026 | TY-2, TY-3, CDV law 2's serif clause, HET §0 item 9 retired under type B | §8.3 item 9 |
| DL54-11 | 4 Oct 2026 | The hero's door rests ajar, with its revert | §8.3 item 10 |
| DL54-12 | 4 Oct 2026 | Black-and-white → colour in the home hero only | §8.3 item 11 |
| DL54-13 | 4 Oct 2026 | The lit arris on night plates only; every primary but CTA-B flat | §8.3 item 12 |
| DL54-14 | 4 Oct 2026 | At most three distinct radii on a screen | §8.3 item 13 |
| DL54-15 | 4 Oct 2026 | The `_`-partial rule, the app-sheet token rule, the CSS ratchet and its bust rule | §8.3 item 14 |
| DL54-16 | 4 Oct 2026 | The gate of §3.1, the calibration (W1-K), the reference list | §8.3 item 15 |
| DL54-17 | 5 Oct 2026 | W1-P: a form's answer inside the preview's frame is framed under the narrow condition, and a framed page drops `upgrade-insecure-requests` — supersedes §4.4's «GET or HEAD» | §4.4, §4.6; review W1-P security M1, UX B1 |
| DL54-18 | 5 Oct 2026 | W1-P: the persona switch refuses any role but a person's or a company's, and any direct permission — stricter than §4.4's letter | §4.1, §4.4; review W1-P security m4 |
| DL54-19 | 5 Oct 2026 | W1-P: the preview's build decisions, ratified by the CD — Italian working strings with the plan's proper names verbatim; one gate for every route; the states in the app; the CD decisions served; the documents follow `main.css`'s layers; the steward's two files in `docs/design-v5/` | §4.1, §4.4, §4.5; W1-P implementation notes §6; CD decision W1-P |
| DL54-20 | 9 Oct 2026 | W2-C1: Home / End move the open panel like the arrows | §1.12 item 6; NAVIGATION §4.8 |
| DL54-21 | 9 Oct 2026 | W2-C1: the plain panel's gloss keeps its language — the catalogue, never a re-read translation | §1.12 change 2; §2.5 |
| DL54-22 | 9 Oct 2026 | W2-C1: one height = the content's honest height; the lede is one block; a short list closes with a hairline | §1.12 change 1 (LA-7); review M3 |
| DL54-23 | 9 Oct 2026 | W2-C1: the letterhead's fit is measured — compact 80–90rem, end zone compact below 100rem, label and name from 100rem, the bar wraps under pressure | §1.11; §1.12 item 9; review M1, M2; a11y/perf 1 |
| DL54-24 | 9 Oct 2026 | W2-C1: the lock-up's name on phones from 329 px; the mark alone only at ≤ 20.5rem | §1.12; review M4 |
| DL54-25 | 9 Oct 2026 | W2-C1: the keyboard focus jumps (`html:has(:focus-visible) { scroll-behavior: auto }`), in chrome.css; the one height is measured off the scrolled switch | §1.12 item 5; a11y/perf 2, 4 |
| DL54-26 | 8 Oct 2026 | W1-B: the stroke table is drawn with non-scaling strokes — 1.5 px from 14 to 24 px, 1.67 at 32, 2 at 48, from one `.icon` rule | §1.7 «Sizes and stroke»; IC §0 rule 3, §6; W1-B build |
| DL54-27 | 8 Oct 2026 | W1-B: the five V4 alias symbols stay in the sprite, resolved by the tag, until their producers are swept | §2.3 «Icons»; §2.2 (W3-A's rail); W1-B build |
| DL54-28 | 8 Oct 2026 | W1-B: the review's redraw candidates adopted on the built sprite (Q11, Q13), judged on the icon sheet at 1× and 2×; the chip board re-judges the marks | §1.7 Q7, Q8, Q11, Q13; IC §1, §2, §3.1, §3.2 |
| DL54-29 | 8 Oct 2026 | W1-B: the family re-maps meanings; the secondary links' arrows, the accordion's `plus` and the rails' ids are their page and component families' | §1.7 «Rules»; §2.2 serialized table; §3.3 item 5 («the rail is W3-A's») |
| DL54-30 | 8 Oct 2026 | W1-B: five paths written outside the family's slice, each justified — the actor map, the sm glyph disc, the pages' icon-list test, the board's sheet, the registry filters | §2.2 (the manifest: the steward assigns); §3.3 item 5 |
| DL54-31 | 9 Oct 2026 | W1-B: numbering — the family's entries DL54-26 … 30 were DL54-20 … 24 on its branch; its review, its a11y report and its notes of 8–9 October cite the old numbers | DL54 «How it is kept»; DL54-19's closing line |
| DL54-32 | 9 Oct 2026 | W1-B: the rails draw the registry's maps, written by the icon family in delivery mode (supersedes DL54-29 item 3); `user` and `key` leave, `home` is a house again (amends DL54-27) | review M1; V5.5; §1.7; §2.3 «Icons» |
| DL54-33 | 9 Oct 2026 | W1-B: an empty state says which space is empty — the domain's glyph, or the neutral mark `empty`; never `document` by default; its glyph is the one hand's 1.5 px | review M2, M3; IC §3.7; V5.5 |
| DL54-34 | 9 Oct 2026 | W1-B: under forced colours an icon inherits its ink and paints no ground — two `!important` in `components.css` §2; the other sheets' forced icon colours yield to it | W2-C1 a11y/perf 7; §2.5; §3.1 |
| DL54-35 | 9 Oct 2026 | W1-B: the review's minors — a glyph on its eyebrow's line (`.icon--inline`), the row menu's solid dots, `handshake` at 24 px, the audiences' measured floors stand | review m1, m3; a11y m1, m2, n1, n5 |
| DL54-36 | 9 Oct 2026 | W1-B: the fix pass's paths outside the slice — the two rail producers, the showcase's list, one declaration of `components.css` §23, one function of `test_rtl_static.py`, one assertion of `test_design_preview.py` (adds to DL54-30) | §2.2 (the manifest: the steward assigns); V5.5 |
| DL54-37 | 8 Oct 2026 | W1-D: the loader «Lume» as built — the release served once by the first console page, L2 drawn on every busy button, L3's seat; the tokens it moves on | §1.9, §1.5; W1-D notes |
| DL54-38 | 8 Oct 2026 | W1-D: every V5 duration lands at 0 ms under reduced motion, the three signature durations included | §1.5; W1-D step 1 (`e62805e`) |
| DL54-39 | 8 Oct 2026 | W2-D, the hero's port: the decisions met during the build (the description as the hero's last row and the fold's peek; the stations in the Phase 3 variant only; `v4/hero.css` shrunk; the repeatable flow; the photographs paired by order; the chevron; logical properties in the stage) | §1.17, §3.4 item 4; DL54-06, -08, -11, -12; the V5.5 directive |
| DL54-40 | 9 Oct 2026 | W2-D, the review fix: the prototype's measured defects (design, taste, UX and motion, sitting 2 round 2) closed in the product — the wall takes the page (columns ≤ 5 lines at 1440 × 900, ≤ 4 from 1536) and the door stands on the niche's floor; the register under the hero not drawn where the hero carries the four sentences; the keyboard's share of the repeatable flow and a real replay control over the key; the hero's own turn curve (supersedes DL54-05 for the hero's key); the door's rest .9 with the band brightest at the gap (DL54-11's revert updated); C-6 d by three levers; every French run end-aligned on the Arabic page; two port defects closed (the composition's height, the stations' list under the product's reset) | plan §1.17; the V5.5 directive; QA/hero-final/*_s2r2.md; QA/v54/w2-d/NOTES.md §7 |
| DL54-41 | 9 Oct 2026 | W2-D, the home around the hero: every chapter under the hero one object (a band, a head at the reading edge with the sprite's `ile-steps` as its mark, a body) on the V5 tokens; no running head, no ordinal; the Morocco → Italy model said once, by the hero's path (the pilot chapter a statement, the jurisdiction bar off the home, `v2/voyage.css` and `v2/routes.css` deleted); a prescribed sentence the hero shows not printed again; the register under the hero without index or glyph; «il gradino», the reserved row on the night; French spacing for team-authored strings only; at the merge, the glyphs of the icon system and the hero's script through the one motion gate | V5.5; §1.1, §1.4, §1.5, §1.7, §1.18 D24, §2.3, §3.4 items 4 and 6; DL54-12, DL54-33, DL54-40; DS V5 PX02, PX04, PX08, PX13; UX_PUBLIC §2.1, §2.3 |
| DL54-42 | 9 Oct 2026 | W2-D, the senior review's fix pass: from 96 rem the hero's wall stands on the page's column — the container's content edge — with the niche capped by the wall and the plate as wide as its column (amends DL54-40 item 5); on the desktop the description on the page's column and the niche on the composition's bottom edge (DL54-39 item 1's forward correction, the paragraph still inside the hero); a finger's press waits 100 ms or the lift; the interim variant's phone band without a rail, its door on the spine's axis; where nothing hovers the key's halo at rest and the hand's light on each return into view; the home draws its news chapter once an article is live (supersedes DL54-41 item 7's empty row on the home); the home's page-type CSS ceiling left to the merge step, with its measurement | V5.5; `QA/v54/w2-d/REVIEW.md`, `A11Y_PERF.md`; §1.17, §2.6; DL54-11, DL54-12, DL54-33, DL54-39, DL54-40, DL54-41 |
| DL54-43 | 10 Oct 2026 | W2-D, the fix pass, the wall under a classic scrollbar: the smallest column of the wall's cap is 12 rem (supersedes DL54-42 item 1's 11.75 rem and its line of the door's `sizes`) — the cap is read in `vw` and the grid in `%`, and with a scrollbar drawn the fourth word took two lines where the niche is capped; what was seen with the scrollbar drawn and left | V5.5; `QA/v54/w2-d/REVIEW.md` m2; DL54-42 |
| DL54-44 | 10 Oct 2026 | Steward, the w2-d merge: the home's chapters assigned to w2-d in the manifest (V5.5 folded W2-E's chapters into the area: thirty paths, slices wherever another family holds the file); the area merged before W2-B (`_door.css` is not on design-v5: `hero.css` holds the stage's rules until it lands); the home's page-type CSS recorded as measured — 57 820 B gzip in three sheets, 10 514 B over §2.6's Wave-1 ceiling, §2.6 item 5 not applied under V5.5's performance rule, on the check's evidence; the ceiling from here 59 137 B (`main.css`'s ceiling + the two page sheets as they weigh); `collectstatic` under the production storage still fails (W1-D's console entry) | V5.5; §2.2, §2.6, §3.4 items 4 and 6; DL54-41, DL54-42 item 9; `QA/v54/w2-d/A11Y_PERF.md` F1, F2 |
| DL54-45 | 9 Oct 2026 | W1-C: the field's 2 px focus rule is drawn by the field's own column, with transform; the plate is (0,1,0), 52 px on public pages | §1.6; §1.8; §1.13; §1.5 (properties) |
| DL54-46 | 9 Oct 2026 | W1-C: checkbox and radio are the native controls, drawn at 24 px with a 44 px hit area under a coarse pointer; the switch is `role="switch"` | §1.4 SP-8; §1.8; DS V5 §10.3 |
| DL54-47 | 9 Oct 2026 | W1-C: a notice says its kind three times without colour — the mark, the title, the STYLE of its rule (solid · dashed · double); a done thing is ink | §1.2 (O14); DS V5 §10.8 |
| DL54-48 | 9 Oct 2026 | W1-C: tabs — one indicator on transform, a constant weight, nothing remembered (G-21 closed); the disclosure draws its own chevron, `__panel` is `__body` (G-19 closed), a link opens its row | §1.5 MS-O3; §1.15; CDV §15 |
| DL54-49 | 9 Oct 2026 | W1-C: buttons — one press gesture, no shadow at all, the ghost in the accent, `text-wrap-style` and not `text-wrap`; the V4 busy face stays in `v4/buttons.css` for the loader family | §1.4 SH-9; §1.5; §1.9; §3.3 item 7 |
| DL54-50 | 9 Oct 2026 | W1-C: the entrance draws no field of its own; the paths written outside the family's slice, each justified — four of its own, three with the loader's hand-over; the console keeps its own focus rule | §2.2 (the manifest: the steward assigns); W1-A review m-1, m-9 |
| DL54-51 | 9 Oct 2026 | W1-C: tier 0 — the family's rules for a change asked from the keyboard, written before the flag exists | §1.5 (tiers; R-07); §2.3 (`head.js`, W1-D) |
| DL54-52 | 9 Oct 2026 | W1-C: eight registers — «esame» and «blocco» enter by one rule; the badge kinds read as the notices do | W1-C step 2; `QA/v54/w1-c/NOTES.md` |
| DL54-53 | 9 Oct 2026 | W1-C: the chip has one producer — the `{% chip %}` pair; a term is a tag | W1-C step 2; `QA/v54/w1-c/NOTES.md` |
| DL54-54 | 9 Oct 2026 | W1-C: `v5/chip.css` — 24 px by construction, the mark on the first line, the edge as a voice | W1-C step 2; `QA/v54/w1-c/NOTES.md` |
| DL54-55 | 9 Oct 2026 | W1-C: cards by purpose — a record, an action, a summary; no stat grid, no board | W1-C step 2; `QA/v54/w1-c/NOTES.md` |
| DL54-56 | 9 Oct 2026 | W1-C: the O14 lint is a test, in four languages — and its first finding | W1-C step 2; `QA/v54/w1-c/NOTES.md` |
| DL54-57 | 9 Oct 2026 | W1-C: the paths the chips and the cards wrote outside the slice | W1-C step 2; `QA/v54/w1-c/NOTES.md` |
| DL54-58 | 9 Oct 2026 | W3-A: one builder for every rail, two spaces — `shell_navigation(user, space, active)`; a role's registers come first; the other space is named at the rail's head; four entries at most reach the bottom bar | §1.18 D06; §3.5 item 3; the platform audit's S-4 |
| DL54-59 | 9 Oct 2026 | W3-A: level 1 is the line under the name, not a plate; who the account is stands at the foot — the roles first, then the account type | §1.18 D06; §1.7; the audit's S-1 |
| DL54-60 | 9 Oct 2026 | W3-A: the rail is open from 80rem and remembered; compact is 64 px and glyph-only until its short labels are signed | §1.18 D06; §1.8; B1 |
| DL54-61 | 9 Oct 2026 | W3-A: the foot — the profile link, a lone sign-out, the rail's control, the language by its own name, «Site public» in its two words; one row in the four languages; no account popover yet | §1.18 D06; D21; §3.5 item 3; WCAG 1.4.12 |
| DL54-62 | 9 Oct 2026 | W3-A: «il lume» is the lit paper disc, no edge bar; the word of a lone glyph stands beyond the rail's edge and leaves on Esc wherever the focus is | §1.18 D06; §1.11 (Tooltip); WCAG 1.4.13 |
| DL54-63 | 9 Oct 2026 | W3-A: «Communications d’identité» is a page of the rail for the account somebody has asked — the ten stay ten; «Changer d'espace» is not drawn, the way is named by the space it leads to | §1.18 D06; B1 |
| DL54-64 | 9 Oct 2026 | W3-A: one page header by the frame's own rules; a console button takes the control's corner (6 → 4) from the frame; two native skip links | §3.5 item 3; §1.3; the audit's S-2 |
| DL54-65 | 9 Oct 2026 | W3-A: seven paths written outside the family's slice, each justified; the legacy rules deleted from `portal.css`; the console page type stands 571 B gzip over its Wave-1 ceiling | §2.2; §2.6; DL54-15 |
| DL54-66 | 9 Oct 2026 | W3-A: below 64rem the rail is laid flat — the top bar is its head, the bottom bar its pages, the drawer the whole of it; the two bars are the rail's night; «il lume» on the bar is the lit disc | §1.18 D06; §3.5 item 3; §3.1 item 7; O13 |
| DL54-67 | 9 Oct 2026 | W3-A: the phone's measures — a top bar of 48 px (56 in the band), a bottom bar as tall as its words, 114 px of chrome (120 at most); the top bar leaves a short or very narrow viewport | §1.18 D06 (S-3); WCAG 1.4.10 |
| DL54-68 | 9 Oct 2026 | W3-A: the bar's words are the live labels, whole — one line or two runs, three entries where four do not hold; the company space's bar capped and completed by the shell; no short label | §1.18 D06; §1.1; D21; B1 |
| DL54-69 | 9 Oct 2026 | W3-A: one «Menu», a link that script turns into a button and that shows the drawer without script; the drawer keeps today's `<dialog>` and holds the rail's own foot | §1.18 D06 (O63, S-2); D21; CD V5 §8 |
| DL54-70 | 9 Oct 2026 | W3-A: a page's action bar takes the four entries' place and «Menu» keeps its end (the case file: 109 px for 174); the questionnaire's foot is part of its page below 64rem | §1.18 D06; O63; the audit's S-3 |
| DL54-71 | 9 Oct 2026 | W3-A, step 2: two paths outside the slice, the foundation's two patches for V4's bar retired, one inventory figure regenerated; the console page type stands 1 445 B gzip over its Wave-1 ceiling | §2.2; §2.6; DL54-15; DL54-65 |
| DL54-72 | 11 Oct 2026 | W3-A, the fix pass: a space starts where its rail does (a role's account at its first register); a space's first page ends its trail on itself; the list's scroll edge is two named tokens; the footer's and the menu's targets | REVIEW M1, m1, m3; A11Y_PERF M1, m1, m4; §2.2 |
| DL54-73 | 11 Oct 2026 | Steward, the w3-a merge: the family's fifteen entries renumbered DL54-58 … DL54-72 (add 19); the eleven paths outside the slice assigned to w3-a in the manifest, two slices named as written; the console page types' CSS ceiling recorded as measured (50 007 B in the three sheets every console page loads, 1 923 B over the end of Wave 1); the area merged before W2-A; the rail foot's disc drawn through the registry's concept filter for W1-C's O14 lint | §2.2; §2.6 items 3 and 5; §3.2; DL54-15; DL54-44; DL54-56; V5.5 |
| DL54-74 | 9 Oct 2026 | W2-B: the stage of «Il varco» as built — three lights that are a function of the form, the passes on the tokens, the address read at the typing pause, the arrival for a person who arrives, the sign-in's forms name the stage (`form__entrance.html`), no words of a long wait yet, every part placed and its ground painted before it is parsed, the password's room on its control's side in Arabic, the stage's paints in a page-only partial (`_varco.css`) | §1.13, §1.9, §1.5; DL54-15; W2-B notes |
| DL54-75 | 10 Oct 2026 | W2-B: the form of «Il varco» as built — a column on the paper hung from the top of its panel, one hierarchy on every entrance page (the eyebrow's key is `ile-key`), the sign-in's page extends allauth's own, no `password_reset_help_text.html` (allauth's link, placed by the slot), `LoginForm` with its presentation only, the primary that holds the loader's key, one 429 template with two parents, the locked assurance, the session message in the form's column, the glyph control until it is the system's, no part of the column waits for a later one, the core components through their family's branch, the raw entry and the production storage (handed to the merge); **fix pass 11 Oct** (items 17–27: the photograph's v5 set, a shown password never spelled, `username`, the assurance where it is translated, allauth's forms without placeholders and `MFA_FORMS`, the grain on the niche only, one key token, the lights where they are drawn, the niche meets the footer, the arrival's lit ways, the small targets) | §1.13 (L1–L6, L8, L11, L12, L14); §1.7; §2.2; §2.3; CDV §18; W1-C's review M1–M3 |
| DL54-76 | 11 Oct 2026 | Steward, the w2-b merge: the family's two entries renumbered DL54-74 and DL54-75 (add 16); the five paths outside the slice assigned to w2-b in the manifest, three slices named as written; `MFA_FORMS` agreed; the login page type's CSS ceiling recorded as measured (47 392 B in its two sheets, 3 949 B over the end of Wave 1); `main.css` +79 B on every page type, the console page types' ceiling 50 086 B; `collectstatic` still refused, now on two raw entries; DL54-44 item 2's two forward corrections left, with the reason | §2.2; §2.3; §2.6 items 3 and 5; DL54-15; DL54-44; DL54-73; DL54-74; DL54-75; V5.5 |
| DL54-77 | 11 Oct 2026 | Steward, the static pipeline: every @import and url() of a source sheet written in the collected tree, `build_css.mjs` resolving and refusing through Django's own mapping, the guard `test_static_pipeline.py` (a real `collectstatic` under the manifest storage); CI's Lint step closed (W1-D's six findings, formatting only); the non-browser checkpoint on a fresh clone — 4 482 passed, 0 failed; two paths and one slice assigned to the steward | §2.2; §2.3; DL54-44; DL54-73; DL54-76; V5.5 |
| DL54-78 | 11 Oct 2026 | W3-B: the person's dashboard — the DOM's order (h1 → NowPanel → journey); the NowPanel the one raised plane with the one primary, four variants chosen by the system and an overdue date taking it over; cards by purpose; one thing once; what folds; the account's line until W2-A's popover; the journey placed, still at load | §3.5 item 4; §1.15; §1.4 SH-8; §3.1 item 7; DL54-55 |
| DL54-79 | 11 Oct 2026 | W3-B: T1 — one next action over the file's checklist items and pieces, on the precedence it had; a piece read through the documents app's authorisation (`reader`); the case views pass the reader | §1.18 Track T; IMPLEMENTATION_PLAN §2 T1 |
| DL54-80 | 11 Oct 2026 | W3-B: «il registro» on the dashboard — by who holds the piece, the colour the group's, the shape the state's; the group words the catalogue's until B1 | §1.18 D15; O62 |
| DL54-81 | 11 Oct 2026 | W3-B: the door in the console's one empty state — the doorway component as drawn | §2.3; §3.1 item 7 |
| DL54-82 | 11 Oct 2026 | W3-B: five paths outside the slice, each justified; the legacy rules deleted; the console page types' CSS +1 305 B gzip, reported | §2.2; §2.6; DL54-15; DL54-73 |
| DL54-83 | 11 Oct 2026 | W3-B, step 2: the company's dashboard in the person's grammar — the NowPanel (one partial) says the company's one next action with its one primary; «il registro» of the needs by who holds them; the NowPanel's need drawn there only; the legal name once | §3.5 item 4; §1.15; §3.1 item 7; DL54-78; DL54-80 |
| DL54-84 | 11 Oct 2026 | W3-B, step 2: the bridge of the accounts that are not a person — no NowPanel (no next action of their own), its registers as flat sections, an empty region one line, the pre-assessment once | §3.5 item 4; §1.15; DL54-55 |
| DL54-85 | 11 Oct 2026 | W3-B, step 2: four paths outside the slice, each justified; the facts, the workspace grid, the needs table and the six cards deleted; Panel, ContextHeader and HealthStrip stay with their consumers; the console page types 51 308 → 50 768 B, 761 B over the ceiling — reported | §2.1; §2.2; §2.3; §2.6; DL54-73; DL54-82 |
| DL54-86 | 11 Oct 2026 | W3-B, the fix pass: no button promises an act its page cannot do («Consulter» and the register's own note while the Conditions gate blocks the filing; DL54-78's «Accepter les Conditions» superseded); a record's own words keep their direction (`dir="auto"`); the company's NowPanel carries the need page's own act («Transmettre au projet», when the account may submit); the minors kept honest in place; the console's empty state spans the main column again | REVIEW M1–M3, m1–m11; A11Y_PERF findings 1–4, 6; DL54-78; DL54-83 … DL54-85 |
| DL54-87 | 11 Oct 2026 | Steward, the w3-b merge: the family's nine entries renumbered DL54-78 … DL54-86 (add 4); the nine paths outside the slice assigned to w3-b in the manifest, three slices named as written; the console page types' CSS ceiling raised once, by 841 B, under §2.6 item 5 on the area's twin measure (50 927 B in the three sheets); `main.css` −651 B on every page type, no ceiling lowered; the door's component included again (the NowPanel), its paint still `v4/hero.css`; the capture report unchanged | §2.2; §2.3; §2.6 items 3 and 5; DL54-15; DL54-44; DL54-73; DL54-76; DL54-82; DL54-85; DL54-86; V5.5 |
| DL54-88 | 11 Oct 2026 | W2-A: the overlay system as built — one sheet (`v5/overlays.css`), one module (`overlay.js`), five components, the board; `.overlay` and `data-overlay`; body and foot by template; a menu as a sheet stays a menu; the side chosen before the opening; the warm group in CSS; the gutter kept; the link as the no-script opener | §1.14; §1.5 MS-O2, O4–O6; §2.3; the contract |
| DL54-89 | 11 Oct 2026 | W2-A: the INP rule fired — a modal kind opens with `show()`, `aria-modal`, `closedby` and one shared scrim, the trap in script (`showModal()` an opt-in); `html:has(:focus-visible)` (DL54-25) becomes `html[data-input="key"]`; W3-A's `html:has(.console-drawer[open])` leaves with the console drawer | §1.14 (the INP rule, O6, O7); §1.12 item 5; DL54-25; DL54-69 |
| DL54-90 | 11 Oct 2026 | W2-A, step 1: the paths written outside the slice — the board and its dev sheet, one row of the preview's index, one rule of `chrome.css`, the DS 2026 figures the change moved | §2.2; V5.5; V5.7; DL54-37 |
| DL54-91 | 11 Oct 2026 | W2-A, step 2: every overlay of a console page on the system — the drawer a modal drawer of the trap with its own measures; the account popover with V4's details face kept for the letterhead; the row menu; the disclosures owned by `overlay.js` (an open one takes the Esc before its panel), `main.js`'s dropdowns a fallback, `initDialogs` gone; the rail's word on the one top-layer tip (`data-tip-label`, `data-tip-beyond`, `overlay:tip`; keyboard focus); no script, at once; the notification centre handed over | §1.14 (the propagation, O11, the INP rule); §3.4 item 1; §3.5 item 3; DL54-69; DL54-89 |
| DL54-92 | 11 Oct 2026 | W2-A, step 2: the paths written outside the slice — W3-A's shell sheet, its console.js rail word and its three test files, `v4/shell.css`, the showcase and its demo, `test_static_assets.py`'s pin, ACCESSIBILITY.md's overlay rows, DS 2026's sentences that follow the markup | §2.2; DL54-73 item 4; DL54-90 |
| DL54-93 | 11 Oct 2026 | W2-A, the fix pass: a menu shown as a phone sheet stands over the one scrim, which holds the whole press, headed by its name (supersedes DL54-88 item 3); the page behind a trapped panel `aria-hidden`, never `inert` (amends DL54-89); the focus brought into its panel's view; the layer tip follows a scroll; the rarer parts in `overlay/extras.js` behind a dynamic import no console page makes, the module budget and the console page types' ceilings left to the merge step; the account trigger's name; four paths outside the slice | REVIEW M1, m3, m4; A11Y_PERF M1–M4, m1; §1.14; §2.6; DL54-88; DL54-89 |
| DL54-94 | 11 Oct 2026 | W2-A, the budget fix: design-v5 merged (W2-A's entries DL54-88 … DL54-93); what no product page draws — the dialog and the alert, the bottom sheet and its grip, the head / body / foot of the components, a native modal's backdrop, the control's own CSS tooltip — page-only in `v5/_overlay-panels.css`, its own entry `css/dist/core/overlay-panels.css`, linked by the pages that draw it; the shared sheet written once; 77 dead selectors deleted from the shared bundles, each proved by a grep of design-v5 and the four in-flight trees; the console drawer's copied declarations gone; every page type under its V5.8 ceiling (the console page types 50 893 of 50 927 B); the module's 6 466 B recorded; supersedes DL54-93 item 5's request | the owner's V5.8; V5_5 addendum 11 Oct 19:40; §2.3; §2.6 items 3 and 5; DL54-73; DL54-76; DL54-87; DL54-93 |
| DL54-95 | 12 Oct 2026 | Steward, the w2-a merge: nothing to renumber (design-v5 had not moved since the budget fix's sync: W2-A's entries stay DL54-88 … DL54-94); the 24 paths outside the slice assigned to w2-a in the manifest, five slices named as written; the shared CSS gate of V5.8 passed on the ceilings as recorded (plan §2.6 item 3) — the console page types 50 927 → 50 893 B, every public page type +272 B and under its ceiling, none raised, none recorded anew, none lowered — with the strict reading named for the orchestrator; the page-only sheet and its rule; the overlay module's 6 466 B recorded against §2.6's 4 KB; DS 2026 §2's one stale figure regenerated; the capture report unchanged | the owner's V5.8; V5_5 addendum 11 Oct 19:40; §2.2; §2.3; §2.6 items 3 and 5; DL54-73; DL54-76; DL54-87; DL54-88 … DL54-94 |
| DL54-96 | 11 Oct 2026 | W3-F2, step 1: the content and legal pages as built — one page partial and one entry for every content page; the interior's grammar value for value; the glossary a visible register with a sticky letter index; the empty page without a dashed box; D26 as layout slots with live words; the legal page's pinned markup; a fallback `lang` on its text; a prescribed text in `<title>` and `<meta>` as text; five paths outside the slice; the interior page type 1 379 B over its Wave-1 ceiling, measured | §3.5 item 2; §1.18 D26; §2.3; §2.6; DL54-15; DL54-33; DL54-47; V5.5 |
| DL54-97 | 11 Oct 2026 | W3-F2, step 2: the error and account pages as built — one quiet page for every status in the interior's grammar; 400 and 500 self-sufficient (no database, no context processor, a bare fallback); the account pages in one frame on the public shell; allauth's elements keep their class names; the deletion behind its own page; no page of sessions, the CSRF page left for B1; the paths outside the slice; the service page type under its Wave-1 ceiling | §3.5 item 2; §1.3; §1.4; §1.8; §1.18 D26; §2.1; §2.3; DL54-15; V5.5 |
| DL54-98 | 12 Oct 2026 | W3-F2, the fix pass: the door at rest on the error pages (the key out of the lock), in a page sheet of their own; every Latin head of an Arabic page on its cell's reading edge, a head's paragraph a box the width of its words; the refused newsletter on the system's summary; the profile's input purposes; the official Italian text left to right; three paths outside the slice; the page types' weights for the merge | §3.5 item 2; §1.4 SP-8; §1.16; §1.18 D26; §2.3; §2.6; CD §0, §1.4 law 5, §20; DS V5 PX21; V5.5; V5.8 |
| DL54-99 | 12 Oct 2026 | Steward, the w3-f2 merge: the family's three entries renumbered DL54-96 … DL54-98 (add 19); the ten paths outside the slice assigned to w3-f2 in the manifest, DS 2026's slice named as written; the shared CSS gate of V5.8 passed with the shared payload lighter on every page type (`main.css` 42 152 → 41 464 B, −688 B; the console page types 50 893 → 50 205 B); the interior, login and home ceilings lowered to the measured totals (§2.6 item 3: 41 464, 46 325, 56 115 B), the console page types' kept; the content, account and error page types recorded with their page-only sheets (45 520, 43 890, 45 093 B), §2.6 item 5 not applied and said; DS 2026 §2's two stale figures regenerated; the capture report regenerated (12 captures of the area changed) | the owner's V5.8; V5_5 addendum 11 Oct 19:40; V5.5; §2.2; §2.3; §2.6 items 3 and 5; DL54-44; DL54-73; DL54-76; DL54-87; DL54-95; DL54-96 … DL54-98 |

---

## DL54-01 · 4 October 2026 · Correction to §2.2 and §5.1 step 9: D/F ref conflict

**Decision.** The V5.4 refs are named as follows, everywhere — the ownership manifest, the scripts, the briefs, the
reports:
- **a family's branch** is `v54-<family>` (for example `v54-w1-a`), in the worktree `C:/tmp/ile_wt/v54-<family>`;
- **its merge tag** is `v54/<family>` (for example `v54/w1-a`), the tag v5-live checks out;
- **its checkpoint tag**, before a propagation step, is `v54/<family>-pre-propagation` (for example
  `v54/w1-a-pre-propagation`);
- **the base tag** is `v54/base`: design-v5 at the end of W1-0. The wave tags keep the plan's names (`v54/wave-2`,
  `v54/wave-3`, `v54/wave-4`).

These names replace the plan's in §2.2 («One branch per family: `v54/<family>`»; «a checkpoint commit + tag
`v54/<family>/pre-propagation`») and in §5.1 step 9 (the same tag). The workflow names of §3 were already `v54-<family>`.

**Why.** git stores a ref as a path. The merge tag `refs/tags/v54/w1-a` would have to be a file while
`refs/tags/v54/w1-a/pre-propagation` needs the same name to be a directory: a directory/file («D/F») conflict, which git
refuses. And a branch named like a tag makes every short name ambiguous, so `git checkout v54/w1-a` in v5-live could take
the branch instead of the tag. Reproduced with git 2.51 in a scratch repository: `fatal: cannot lock ref
'refs/tags/v54/w1-a/pre-propagation': 'refs/tags/v54/w1-a' exists`, and `warning: refname 'v54/w1-a' is ambiguous`; the
corrected names create and resolve without a warning (`C:/tmp/ile_v5_council/evidence/v54/w1-0-repo/e1_ref_naming_demo.txt`).

**Source.** The orchestrator's correction to the plan, binding, given with the W1-0 brief (4 October 2026); plan §2.2
(«Branches, worktrees, the live preview, reversibility»), §5.1 step 9, §3 (workflow names).

## DL54-02 · 4 October 2026 · The generic-AI test has eighteen symptoms

**Decision.** Taste's generic-AI test has **eighteen** symptoms, those of TS §19.2 — in the gate (0 F on the eighteen,
portrait A answered «no»), in the council's reading (TS §19 with its three portraits) and on every scorecard. A «17
symptoms» anywhere earlier reads as eighteen.

**Source.** Plan §8.3 item 1; §3.1 item 4; §5.1 step 6; RTD-M1 and RTD-m9 (§8.1).

## DL54-03 · 4 October 2026 · Six scales everywhere

**Decision.** Every gate and every scorecard scores the same **six** scales — visual, premium, originality, UX, mobile,
coherence — each with its one instrument (§3.1 item 2), passing only when the lowest chair's score is ≥ 4 on each (§3.1
item 3). Family acceptance lists that counted their scales differently are read with these six: N17 (the navbar) and L13
(the login) included.

**Source.** Plan §8.3 item 2; §3.1 items 1–3; §5.1 (the scorecard); RTD-B1, RTD-m9 (§8.1).

## DL54-04 · 4 October 2026 · CLS

**Decision.** CLS ≤ 0.10 on every page; **≤ 0.05 on flagship pages** (HF §0 item 11, extended to every flagship); the
font swap ≤ 0.01 with matched fallbacks; 0.01 elsewhere is a target, not a gate. Measured on the compressed twin 8782
under §2.6's protocol.

**Source.** Plan §8.3 item 3; §2.6 (the budget table); §1.17 (hero CLS ≤ 0.05); RTD-m9 (§8.1).

## DL54-05 · 4 October 2026 · `--ease-turn`

**Decision.** `--ease-turn` = `cubic-bezier(0.77, 0, 0.175, 1)` is the one key-turn curve of the loader, the login and
the hero. It replaces LS's `--sig-turn` (LS §9) and gate-0's `--ease-turn-in` / `--ease-turn-out`, and takes the
`--ease-*` name the hero-final build already uses (HF §9.1).

**Source.** Plan §8.3 item 4; §1.5 («Added»); §1.17 («One curve, one place per file, one CLS»); RTD-m9 (§8.1).

## DL54-06 · 4 October 2026 · The hero's files

**Decision.** The ported hero lives in three files: `templates/pages/home/_hero.html`;
`apps/pages/static/pages/css/hero.css`, a page entry (HF §14's `static/css/v5/hero.css` would have had to enter `main.css`,
which §2.3 forbids for page-only CSS); and `static/js/src/hero.js`, imported by the home entry.

**Source.** Plan §8.3 item 5; §1.17; §2.3 («Page-only CSS»); §3.4 item 4 (W2-D's slice); RTD-m9 (§8.1).

## DL54-07 · 4 October 2026 · BA §1 amended: the mark moves once, at the entrance, across the page load

**Decision.** `docs/design-v2/BRAND_ASSETS.md` §1 — the mark «se si muove, si muove una volta, all'ingresso» — is amended
to: the mark moves **«once, at the entrance, across the page load»**. Engage and release are one movement, split by the
navigation and played once per sign-in: on submit the key turns once and holds, with no light; the lit doorway plays on
the arriving console page, once per session, only after a successful sign-in, never over painted content. It is the only
other context. W1-D adds a one-line pointer to this entry in BA §1.

**Source.** Plan §8.3 item 6; §1.9 items 2–3; V54 l.19; RTD-M6 (§8.1).

## DL54-08 · 4 October 2026 · «The tricolour mark never mirrors»

**Decision.** «The tricolour mark never mirrors» means: never **held, drawn or served** mirrored. The key turns 0 → 360°
about its shaft and passes its mirror image between 90° and 270° — the turning the owner asked for — and ends on the
verbatim key (HF §9.1: 0 px difference). The mark stays `direction: ltr`. The loader and hero reports say so in words.

**Source.** Plan §8.3 item 7; §1.9 item 4; §1.17; §1.19 (class A); V54 l.9, l.19; RTD-m7 (§8.1).

## DL54-09 · 4 October 2026 · M10's letter yields to V54 l.19; its reasons hold

**Decision.** The letter of M10 — the gate-0 red team's fix «L1 = the key's half-turns and the frame light only»
(`docs/design-v5/RED_TEAM.md` M10, adopted by CDV) — yields to V54 l.19 (the loader: door, key, rotation or opening,
light). Its reasons hold absolutely: the tricolour planes, the door and the steps never move; nothing cracks open; the
light says «it is open» only when it is — nothing of L1 plays on the `OUTCOME_BEARING` list, which keeps L2 and L3.

**Source.** Plan §8.3 item 8; §1.9 items 2 and 4; V54 l.19; RTD-M6 (§8.1).

## DL54-10 · 4 October 2026 · Rules retired under type B

**Decision.** While type «Una voce» (B) is the system, TY-2 (the serif's scope), TY-3 (the display as a serif sentence),
CDV law 2's serif clause and HET §0 item 9 («one serif line (the promise)») are **retired**: no reviewer applies them.
They return, with A-bis's scope, if W2-E's blind test switches the system to A-bis.

**Source.** Plan §8.3 item 9; §1.1 («Rules retired while B is the system»); §3.4 item 6 (the A-bis test); RTD-M2 (§8.1).

## DL54-11 · 4 October 2026 · The hero's door rests ajar

**Decision.** Once the first movement has played, the hero's door **stays ajar**: a warm band ≤ 14 % of the leaf at its
opening edge, with a spill on the steps. The first paint and the no-JS page show the stage closed, as the owner drew it;
under reduced motion the ajar still shows from the first paint. Taken under V54 l.9 and said in words in the hero report,
with its revert: the band's and the spill's rest opacity 0.8 → 0 gives the closed rest (a forward correction), and the
tag `v54/w2-d` reverts the port whole.

**Why.** An opening that closes again «reads as a refusal» (HF §9.2); the aperture is light from inside, not a passage,
and promises nothing.

**Source.** Plan §8.3 item 10; §1.17; §1.19 (class A); V54 l.9; RTD-M7, option (b) (§8.1).

## DL54-12 · 4 October 2026 · Black-and-white → colour, in the home hero only

**Decision.** Only in the home hero do the four audience photographs rest in black-and-white, at full tonal range, and
take colour under the hand and once in the first movement. Everywhere else — the navbar panel included — an audience
photograph rests in colour, in the V5 grade. A wider use needs its own taste test on that page at ≤ 1 P\*, with GROUP_4
#20029 named as the catalogue comparison.

**Source.** Plan §8.3 item 11; §1.16; §1.12; V54 l.9; RTD-M3 (§8.1).

## DL54-13 · 4 October 2026 · The lit arris has one seat; every primary but CTA-B is flat

**Decision.** The lit arris appears only on **night plates** — the hero's plates, the targa on night, the login stage's
plate — where the light has a cause; paper surfaces (fields, overlays, panels, cards) carry a hairline only. Primaries are
flat (SH-9): no inner light, no glow, no arris, the login's included. The one material treatment on the site is CTA-B
«Soglia», on the hero's primary only, once per page.

**Source.** Plan §8.3 item 12; §1.4 (SH-9 and the lit arris); §1.10; RTD-M8, RTD-m1 (§8.1).

## DL54-14 · 4 October 2026 · At most three distinct radii on a screen

**Decision.** On the corner scale «Lo spigolo» (2 · 4 · 6 · 8 · 12 · full), **at most three distinct radii** on any screen
at rest — `full` included; the arch and the 0 px photographic bands excluded; an open overlay may add its own one. Counted
by script on every capture, under the coherence scale.

**Source.** Plan §8.3 item 13; §1.3; §3.1 item 2 (coherence); RTD-M8, RTD-m12 (§8.1).

## DL54-15 · 4 October 2026 · The `_`-partial rule, the app-sheet token rule, the CSS ratchet and its bust rule

**Decision.**
- **The `_`-partial rule.** A `_`-prefixed sheet is a partial: `scripts/build_css.mjs` skips it as an entry wherever it
  is, and the entries that draw it import it. Page-only CSS (`static/css/v5/_*.css`) and console-only CSS
  (`apps/portal/static/portal/v5/_*.css`) never enter `main.css`; `test_design_docs.py:612` becomes «every non-partial
  sheet is imported by `main.css`; every partial by at least one entry».
- **The app-sheet token rule.** App sheets keep `test_design_docs.py:937`'s rule — no gradient, no `rgba(`, no hex; tokens
  only. The hero's and the door's literal colours and gradients become tokens in `v5/tokens.css`.
- **The ratchet.** W1-0 records each page type's CSS (the home, a door page, an interior page, the login, the dashboard,
  «Mes pièces», the case file). In Wave 1 each page type's total CSS ≤ its baseline + 8 KB gzip, and `dist/main.css` ≤
  45 KB gzip at every merge. From the first Wave-2 merge each page type's ceiling — its measured total at the end of Wave 1
  — never rises, and the steward lowers it whenever a merge lands more than 1 KB below. At the milestone `dist/main.css`
  ≤ 36 KB gzip.
- **The bust rule.** A family over its ceiling does not merge. It first deletes the legacy rules its components supersede
  (§2.3), then moves page-specific rules into page partials; if it is still over, the Performance Lead measures LCP and the
  first-render task with the fonts on 8782 (n ≥ 9), and only if both pass may the CD raise that page type's ceiling once,
  by ≤ 2 KB, recorded in this log. Never above 45 KB for `main.css`.

**Source.** Plan §8.3 item 14; §2.3; §2.6 («The CSS budget — measured, then ratcheted»); §2.7; RTE-B1 (§8.2).

## DL54-16 · 4 October 2026 · The gate of §3.1, the calibration (W1-K), the reference list

**Decision.** A family is shown, merged or propagated only under §3.1: the anchored scale (4 = at the owner's bar,
«credible alongside excellent international digital products», V5.1 §96); one instrument per scale, scored by at least
two chairs; on every scale the **lowest** chair's score ≥ 4, never a mean — the CD may refuse a pass and never grants one
over a score below 4; taste at 0 F on the eighteen symptoms and ≤ 1 P\*, with the swap and brochure tests, and for the
flagships a blind ranking against V4 and two named references; accessibility PASS; performance PASS on 8782 with its
protocol; the motion evidence; health; the tests and the ownership check. Only chairs calibrated by W1-K score a gate:
each lands the three surfaces the owner has already judged below 4 on visual, premium and originality. Each family names
three real products from §3.1 item 5's list and shows side-by-side captures at 1440 and 390; a family may add a reference,
never replace one.

**Source.** Plan §8.3 item 15; §3.1 items 1–12; §3.3 item 2 (W1-K); RTD-B1, RTD-M1 (§8.1).

## DL54-17 · 5 October 2026 · W1-P: a form's answer is framed under the narrow condition; a framed page drops `upgrade-insecure-requests`

**Decision.** In the preview process only (DEBUG and `ILE_DESIGN_PREVIEW=1`), `designpreview.frames.PreviewFrameMiddleware`
relaxes a real page's answer for the preview's own frame when it answers **GET, HEAD or POST** — POST being a form
submitted inside the frame — under exactly the condition §4.4 already set: a loopback caller with no proxy header, this
process's own `Host`, `Sec-Fetch-Dest: iframe`, `Sec-Fetch-Site: same-origin`, outside `/backoffice/` and `/__design-v5/`.
A relaxed answer's policy changes in two directives and nothing else: `frame-ancestors 'self'` (with `X-Frame-Options:
SAMEORIGIN`), and no `upgrade-insecure-requests`. The landing and the index drop `upgrade-insecure-requests` too
(`csp_replace` with `None`). The read-only rule of a persona session still refuses a persona's write before any view, and
its refusal is what the frame shows. The global policy (`config/settings/base.py`) is unchanged and keeps both directives.
This supersedes §4.4's «It applies only when all hold: … GET or HEAD», and generalises the deviation the W1-P notes
recorded for the read-only refusal (notes §6 item 2; security review D1).

**Why.** Measured by the council's UX and security reviewers (docs/design-v5/QA/v54/w1-p/ux.md B1, security.md M1): on
the preview's plain-http loopback server, `upgrade-insecure-requests` made Chromium upgrade the frame's redirect hops to
https — a reserved page's redirect to the sign-in, a form's redirect after it is answered — and refuse them under
`frame-src 'self'` / `form-action 'self'`; and a form's answer was never framed at all (`frame-ancestors 'none'`). The
owner saw a blank frame in every natural flow — the sign-in, its error, the product's own sign-out, every public form —
and §4.6's «0 CSP violations» failed. The browser failed closed, so nothing was exposed; the security reviewer accepted
relaxing a POST answer under the same condition because `Sec-Fetch-Site` cannot be forged by web content,
`frame-ancestors 'self'` still demands that every ancestor be this origin, a refused caller stays strict, and a persona's
writes are refused first. A page that can never be framed (the back-office, the preview's own pages, another site) now
shows the stage's message instead of a blank frame.

**Source.** Plan §4.4 («Frames»), §4.6 («0 CSP violations»); review W1-P (5 October 2026): security M1 (the constraints
and the tests), UX B1 (the measured failures and the option). Code: `apps/designpreview/frames.py` (`FRAMED_METHODS`,
`RELAXED`), `apps/designpreview/views.py` (`NO_UPGRADE`); tests:
`test_a_real_page_is_framed_by_this_origin_only_when_every_condition_holds`,
`test_a_relaxed_policy_differs_from_the_strict_one_in_two_directives_and_nothing_else`,
`test_a_redirect_and_a_form_s_answer_render_in_the_frame_without_a_policy_violation`,
`test_the_product_s_own_sign_out_in_the_frame_ends_on_the_home_and_the_strip_follows`. Numbered on W1-P's branch: if
another family's entries reach design-v5 first, the steward renumbers this entry at the merge, its content unchanged.

## DL54-18 · 5 October 2026 · W1-P: no privileged persona — a person's or a company's role, nothing else

**Decision.** The persona switch (`POST /__design-v5/accedi/<persona>/`) refuses, with 403 and no session, an
allow-listed account that holds any group but `role:person` or `role:company`, or any permission of its own — beside the
refusals §4.4 lists (staff, superuser, unknown or inactive accounts, a database outside the list). The log line says
`refused (privileged)`, with the persona key and never the e-mail.

**Why.** In this codebase a privilege is a group, independent of `is_staff` (`apps/accounts/roles.py`): an operator
handles case files and the help desk, an authorised actor acts on cases for someone else, a moderator, a legal editor or
approver, a content editor. Were an allow-listed QA account ever given one of those roles on a preview database, «Entrer»
would open that privileged session without a password. §4.1's «a staff persona is never offered» is read as «no
privileged session, ever» — stricter than §4.4's letter, which names only `is_staff` and `is_superuser`. Today the four
accounts hold `role:person` (two), `role:company` (one) and no group (one).

**Source.** Plan §4.1 («A staff persona is never offered»), §4.4 («Refused: is_staff or is_superuser accounts»); review
W1-P security m4. Code: `apps/designpreview/personas.py` (`PERSONA_ROLES`); test:
`test_the_switch_never_opens_a_privileged_session_whatever_the_role`. Numbered on W1-P's branch, as DL54-17.

## DL54-19 · 5 October 2026 · W1-P: the preview's build decisions, ratified by the Creative Director

**Decision.** For the preview (`apps/designpreview`, W1-P), the CD ratifies the decisions the engineer met during the
build (implementation notes §6, items 1 and 3–8; item 2 became DL54-17):
1. **The strip and the index speak Italian,** as the preview always has.
   - The plan's proper names stay verbatim: «V5 — council-passed», «V4 + fondation», «Personas», «Entrer», «Sortir»,
     and the persona names.
   - §4.1's working strings read:
     - «Italy Legal Entry™ — V5, la migliore di oggi» (current best);
     - «Novità» → «Cambiato dall’ultimo rapporto» (changed since the last report);
     - «Indice» (index);
     - «Apri a parte» (open the page alone; the full sentence is its tooltip).
2. **One gate for every preview route, not only for the persona switch.** A request passes only from loopback, with no
   proxy header and with this process's own `Host`.
   - The proxy headers are sixteen: the plan's five, and eleven that tunnels and forwards add.
   - `ile` is refused beside `ile_qa`.
   - This is stricter than §4.4's letter.
3. **Some states live in the app,** at `/__design-v5/stati/<code>/`: those the product's DEBUG error routes cannot show
   in the product's own words. `config/urls.py` has no owner in the manifest.
   - 429 today;
   - 404 by the CD's condition C1 (W1-P CD decision).
4. **The status board's link to a CD decision is served** as text, `.md` only, at `/__design-v5/decisioni/<path>`,
   through the proof resolver's guards.
5. **Every standalone preview document loads the font and token layers that `static/css/main.css` imports,** never the
   bundle. The bundle's `iframe { display: none }` would hide the frames. So the preview follows W1-A without an edit.
6. **`live_status.json` and `CHANGELOG_V54.md` live in `docs/design-v5/`** of the checkout the server serves, and only
   the steward writes them.
   - The surface keys are W1-0's census ids.
   - A lane may point the two settings at scratch copies.

**Why.** Each keeps the plan's intent and closes a gap its letter left; item 2 is stricter. The council's four lenses
(UX, security, accessibility, performance; W1-P rounds 1 and 2) reviewed them, and none objected. The security review
endorsed items 2 and 4 by name (its D2 and D3).

**Source.** Plan §4.1, §4.4, §4.5, §4.6. `docs/design-v5/QA/v54/w1-p/IMPLEMENTATION_NOTES.md`: §6, and «Review fixes —
round 1», «For the steward». `docs/design-v5/QA/v54/w1-p/security.md` and `security_r2.md`: D2 and D3.
`docs/design-v5/QA/v54/w1-p/CD_DECISION.md`: §3. Numbered on W1-P's branch, like DL54-17: if another family's entries
reach design-v5 first, the steward renumbers it at the merge, with its content unchanged.

## DL54-20 · 9 October 2026 · W2-C1: Home / End with a panel open move the open panel

**Decision.** In «Il portico», Home and End on the bar behave as the arrows do (plan §1.12 item 6, NAVIGATION §4.8):
the focus goes to the first / last item and an open panel follows it — it opens under a door, and leaves with the
focus when the item is Forum. The first build left the panel open under another item.

**Why.** One rule for the four keys that move along the bar; a panel open under an item that is not its door is a
state the model does not have.

**Source.** Plan §1.12 item 6; NAVIGATION §4.8; `static/js/src/nav.js` (the `Home` / `End` branch); met during the
build, 8 October 2026 (NOTES.md «Decisions met during the build»).

## DL54-21 · 9 October 2026 · W2-C1: the plain panel's gloss keeps its language

**Decision.** The gloss of a plain panel («Projet») that comes from the fallback structure is a gettext source: the
panel asks the catalogues for it (`page_services.ui`) and marks `lang` only when the catalogue has no translation.
It never re-reads an already translated string as French.

**Why.** The first build drew the Arabic «Projet» gloss LTR with `lang="fr"`: the string was translated and then
treated as a French fallback. A gloss is in the page's language whenever the catalogue has it (plan §2.5).

**Source.** Plan §1.12 change 2 (the locked gloss), §2.5 (i18n); `apps/cms/templatetags/cms_nav.py` (`_portico`);
`tests/frontend/test_cms_nav.py::test_portico_glosses_and_second_lines_carry_their_language`.

## DL54-22 · 9 October 2026 · W2-C1: the one height is the content's honest height; the lede is one block; a short list closes

**Decision.** The four door panels share one height (LA-7), and that height is the tallest door's honest content
height (Personnes: six entries, four with a second line): no row is compacted below 48 px and no line is clamped
to reach it. In every panel the lede is one block — the gloss, then «Voir l'espace» directly under it (as the comp
kept the link at the end of the sentence) — so the paper below reads as the grid's air, never as a missing column.
A door panel whose own content ends more than 24 px above the shared height is marked `.portico--short` by
`nav.js` at the measure, and its last entry closes with a hairline, so a short list ends instead of trailing off;
the full panel's list is closed by the foot's hairline. The second lines remain live sentences only (B1 item 1
stays the owner's).

**Why.** The review's M3 measured three panels of 1240 × 570 with two rows and the link pinned 340–460 px under
the gloss; the comp had the link with the sentence. The composition fix is inside the plan; the content fix is not
ours to write.

**Source.** Plan §1.12 change 1 (N3, LA-7) and change 3 (whole lines, never written by us); REVIEW.md M3;
`static/css/v5/chrome.css` §5; `static/js/src/nav.js` (`heights`).

## DL54-23 · 9 October 2026 · W2-C1: the letterhead's fit is measured, not assumed

**Decision.** The six-item letterhead stays at 80rem (plan §1.12 item 7) and fits its content column at every width,
measured in fr · it · en · ar, signed out and signed in (`test_the_letterhead_holds_its_column_at_every_desktop_width`):
- **80–90rem** (the `lg` column, 1096 px; the six French items beside the full lock-up need 1178): the letterhead
  is compact — the lock-up at 32/17 (the scrolled state's size), 16 px gaps, the doors without their chevrons as
  between 64 and 80rem; the row then needs fr 1029 · en 1028 · it 1002 · ar 914 (measured, E/fix/).
- **Below 100rem** the end zone is compact: the targa is the key alone (32 × 32, its name in the tooltip and the
  accessible name); signed in, the seat is the person glyph alone on the same plate (the name visually hidden, no
  chevron). The label's threshold moves from 90rem to **100rem**, the measured one (§1.11: «shown wherever it
  fits»): at 90–100rem the column is 1240 px and the French row leaves 59 px, less than the plate's 140.
- **From 100rem** the plate carries its word and the seat its name, at most 6rem, then an ellipsis.
- **Under pressure** — WCAG 1.4.12 text spacing, a long back-office label — `.main-nav__list` wraps and the
  letterhead grows by one row; the panels hang from the inner's foot and follow. It never clips (plan §1.12 item 9).

**Why.** The review's M1 (80–83 px past the column from 1280 to 1599 in French, the signed-in seat overflowing
Arabic too) and M2 (scrollWidth 1600 at 1440 under text spacing); the a11y/perf check's finding 1. The reviewer's
option (a) kept the six items from 80rem; its padding-8 variant left French 1.4 px of slack, too little for
Italian and English to be safe, so the chevrons leave the band instead, as they already leave 64–80rem.

**Source.** Plan §1.11 (the label «wherever the four languages fit»), §1.12 items 7 and 9; REVIEW.md M1, M2;
A11Y_PERF.md 1; `static/css/v5/chrome.css` §3, §4, §6; DS 2026 §7.2, §11.1, §11.3.

## DL54-24 · 9 October 2026 · W2-C1: the lock-up's name on phones from 329 px

**Decision.** The lock-up's name is hidden only at ≤ 20.5rem (328 px), where the name (227.5 px at the brand's
14 px words) and the icon-only «Menu» (44 px) cannot share the 280 px of content of a 320 px screen; from 329 px
the name is on screen — on every 340-, 360-, 375- and 390-class phone. Below 48rem the letterhead's gap is 12 px
and «Menu» has 8 px of padding (84 px with its word, 44 without); the word stays screen-reader only at ≤ 23rem.

**Why.** The review's M4: V4's `max-width: 23rem` rule hid the name at 360 px, the most common Android width. The
arithmetic also showed a latent overflow at 369–383 px (the name, 24 px and the 92 px button exceeded the column),
which the same row fixes. The brand's 14 px words are kept; 320 keeps the mark alone.

**Source.** REVIEW.md M4; BRAND_ASSETS §1 (the lock-up scales as one unit); `static/css/v5/chrome.css` §1, §3, §7;
`tests/frontend/test_header_fits_the_narrowest_viewport.py::test_the_name_and_the_menu_button_share_the_phone_row`.

## DL54-25 · 9 October 2026 · W2-C1: the keyboard focus jumps; the one height is measured off the scrolled switch

**Decision.** `html:has(:focus-visible) { scroll-behavior: auto; }` lives in `static/css/v5/chrome.css` §3 as the
navigation's rule (plan §1.12 item 5, «no smooth scroll on Tab»): while the focus is a keyboard focus the page
jumps to the next stop; a pointer's anchor click keeps `base.css`'s smooth scroll (a click gives no
`:focus-visible`); the wheel is never smooth-scrolled. The letterhead's own stops (the lock-up, the six items, the
end zone) carry `scroll-margin-block-start: -80px`, the negative of the page's scroll padding: a focus inside the
sticky bar — a door, Shift+Tab from the page — no longer scrolls the page to the top (measured: 300 px stays 300 px,
fr and ar; the instant jump made visible what the smooth scroll had hidden, and `test_the_keyboard_model_of_the_portico`'s
«↑ never scrolls» had passed on timing). The panels' entries keep the padding: they hang below the bar (2.4.11 holds,
`test_focus_is_not_obscured_by_the_sticky_letterhead`). And `nav.js` measures the four panels' one height only when
the inner's width, the bar or the fonts change — the 64 ↔ 56 switch re-reads the lead and re-places the architrave
only.

**Why.** The a11y/perf check's findings 4 (a stop below the fold arrived after > 900 ms of smooth scroll) and 2
(57–125 ms of long task on every wheel crossing at CPU ×4, of which the relayout was 54–107 ms and the class
toggle 25–31). The rule is the navigation's own item, so it sits in the navigation's sheet rather than in
`base.css` through the steward; it is global in effect and is noted here for that reason.

**Source.** Plan §1.12 item 5; A11Y_PERF.md 2 and 4; `static/css/v5/chrome.css` §3; `static/js/src/nav.js`
(`lead`, `heights`, `layout`).

## DL54-26 · 8 October 2026 · W1-B: the stroke table is drawn with non-scaling strokes

**Decision.** Every stroked shape of a symbol is merged into one `<path vector-effect="non-scaling-stroke">` by
`scripts/build_icons.py`, and the sprite carries no stroke-width, cap or join of its own. The `.icon` rule
(`components.css` §2) draws every symbol at **1.5 px** — in CSS px, at 14, 16, 20 and 24 px alike — with square caps
and miter joins; `.icon--xl` sets 1.67 px and `.icon--hero` 2 px, the plan's optical step-up. The six size classes
are `--icon-xs … --icon-hero`.

**Why.** The plan's table gives the stroke per size in grid units (2.57 / 2.25 / 1.8 / 1.5 / 1.25 / 1) so that the
effective stroke is 1.5 px; the product sizes `.icon` from dozens of component rules without a size class (the rail,
the utility bar, the account menu, the glyph discs, the notices), and a unit stroke would give each of them its own
weight — the «two hands in one component» the review measured (IC §11.4). A non-scaling stroke makes the table hold by
construction wherever a glyph is drawn. Cost, stated: a `stroke-width` written for the old scaling sprite now reads as
px — `.empty-state__icon` 1.25 (W3-E's §23: 2.1 px before, 1.25 px now, to be set to 1.5) and `.chip__g` 2.6 in
`v3/chip.css` (W1-C's, unrendered today) — named in the §2 comment and in W1-B's notes.

**Source.** Plan §1.7 («Sizes and stroke», «Square caps, miter joins, currentColor only»); IC §0 rule 3, §6 («CSS»);
`docs/design-v5/QA/v54/w1-b/NOTES.md`.

## DL54-27 · 8 October 2026 · W1-B: the five V4 alias symbols stay in the sprite until their producers are swept

**Decision.** `user`, `home`, `list`, `globe` and `key` are alias symbols of the built sprite, each drawing the
geometry of the V5 symbol of its remaining use (`person`, `layout-dashboard`, `send`, `languages`, `ile-key`:
`apps/core/icons.py` `LEGACY`). The `svg_icon` tag resolves an alias, so a page's markup carries the V5 id; a template
never writes one (`tests/frontend/test_icons.py`). They leave with their last producer.

**Why.** Plan §2.3 asks for them. The producers that still emit them are other families' serialized files — the console
rail's `NAV_GLYPHS` and the company rail (W3-A), the dashboard cards' `icon=` (W3-B), `living.catalogue` and the
pathways' `DEFAULT_ICONS` (W3-F) — and their own compliance tests read the sprite's ids. Cost: 1 786 B raw; the sprite
is 31 969 B, under the 32 KB ceiling (DS §12 #7).

**Source.** Plan §2.3 («Icons»), §2.2 (the serialized table), §3.3 item 5 («the rail's re-mapping is W3-A's»).

## DL54-28 · 8 October 2026 · W1-B: the review's redraw candidates adopted on the built sprite

**Decision.** The sprite draws the review's candidates (IC §1, §2, §3.1, §3.2): `building-b` (two bars, the annex
without dots), `document-b` (two lines), `info-b` (the dot clear of the stem), `warning` with the larger triangle,
`st-attesa` with eight dashes, `st-azione-b` and `st-rifiuto-b` with the 3-unit signs, `ile-key-b` with the teeth 4.5
units apart; the 22 pictorial V4 drawings re-proportioned to the 21.5-unit live area (Q11). Settled by the plan and
kept: the gate-0 nested arch for `ile-arch`, floor 16 (Q7); `ile-steps` never mirrors (Q8); `shield`, no
`fingerprint` (Q10); `award` (Q12); `university` shared by the study pathway, no `backpack` (Q9). Judged on the icon
sheet (`/__design-v5/specimens/icons/`) at 1× and 2×, fr and ar, and on the raster measurement
(`C:/tmp/ile_v5_council/evidence/v54/w1-b/impl-1/measure/`); the chip board (W1-C) re-judges the marks in their chips.

**Why.** The plan settled Q7–Q13 for the build (§1.7 «Settled questions»); Q13's «judged on the chip board at 1× and
2×» needs W1-C's chips, which do not exist yet — the marks are judged here as marks, and W1-C looks again.

**Source.** Plan §1.7; IC §1 (the key's teeth), §2 (the two candidates), §3.1 (`building-b`), §3.2 (`document-b`),
§3.7 (`info-b`), §11.4.

## DL54-29 · 8 October 2026 · W1-B: the family re-maps meanings; density and the rails are their page and component families'

**Decision.** W1-B re-mapped every call site whose glyph said the wrong thing, and left three things to their owners,
named here so that nobody reads them as forgotten:
1. **The secondary links' arrows** (`link-arrow`, ≈ 45 sites; `entry__arrow`, `page-links__arrow`) stay. The map's «80 →
   ≈ 30 calls» is the six-icon ceiling of the public editorial body (§1.7 «Rules»), which W2-E (the home) and W3-F1 /
   W3-F2 (the public interior) deliver when they recompose those pages; an arrow is one concept (forward), so no meaning
   is wrong meanwhile.
2. **The accordion keeps `plus`** (it turns 45° to a cross on open); the map's `chevron` turning 180° needs the rule of
   `components.css` §15, W1-C's, which rebuilds the accordion.
3. **The rails' ids** — `portal.services.NAV_GLYPHS` (`check` for the selection processes, `handshake` for the Guichet,
   `map-pin` for the journey, `university` for the Academy, `briefcase` for the cases), the company rail — are W3-A's;
   the registry's `NAV` and `COMPANY_NAV` maps are written for it, and the aliases (DL54-27) keep the rail drawing.

**Why.** The ownership manifest and §2.2's serialized table; V5.5 ships what is wrong first.

**Source.** Plan §1.7 («Rules»), §2.2, §3.3 item 5; `OWNERSHIP_V54.json` (w1-b: «the svg_icon call sites, for the
re-mapping only»).

## DL54-30 · 8 October 2026 · W1-B: five paths written outside the family's slice, each justified

**Decision.** For the steward to write into the manifest at the merge (plan §2.2: «a path nobody owns … the steward
adds the assignment»):
1. `apps/documents/requirements.py` — `ACTOR_GLYPHS = dict(icons.ACTOR)`: the authority's disc was `shield` (now the
   account-security symbol), the authorised actor `handshake` (now the Forum), the project team `institution`; the
   actor glyph is the one place the four audiences and the actors meet, and IC §6 makes every map import from the
   registry. One line, tested equal.
2. `static/css/v4/workspace.css` line 377 — the sm glyph disc draws a 16 px glyph, not 14: `stamp`, `institution` and
   `university` are clean from 16 px (plan §1.7 «Audiences», IC §3.1).
3. `apps/pages/tests/test_templates_static.py` — `AVAILABLE_ICONS` read from the sprite instead of a V4 literal list.
4. `static/css/dev/specimen-icons.css` — the icon board's own sheet (a board may not carry a `<style>`; the folder's
   README names no sheet).
5. `apps/core/templatetags/ile_core.py` beyond «the svg_icon tag»: the `concept` and `actor_glyph` filters and the
   `icon_registry` tag — the registry's way into the templates (plan §1.7: a concept «reaches templates only through
   the registry»).

**Source.** Plan §1.7, §2.2, §3.3 item 5; IC §3.1, §6; `scripts/check_ownership.py w1-b` (run before the merge, the
five paths listed as OUTSIDE).

## DL54-31 · 9 October 2026 · W1-B: numbering — DL54-26 … 30 were DL54-20 … 24 on the family's branch

**Decision.** W1-B's five entries of 8 October are DL54-26 … DL54-30. They were written and cited as DL54-20 … DL54-24
on the family's branch; W2-C1's six entries reached design-v5 first and hold DL54-20 … 25, so the merge of 9 October
renumbered W1-B's — content unchanged but for the one cross-reference inside DL54-29 (the aliases' entry is DL54-27).
`docs/design-v5/QA/v54/w1-b/REVIEW.md`, `A11Y_PERF.md` and the notes of 8–9 October in `NOTES.md` were written before
the merge and cite the old numbers: there, DL54-20 / 21 / 22 / 23 / 24 read DL54-26 / 27 / 28 / 29 / 30.

**Source.** DL54 «How it is kept» (append-only); the closing line of DL54-19 («if another family's entries reach
design-v5 first, the steward renumbers it at the merge, with its content unchanged»); the merge `7b7fcbd`.

## DL54-32 · 9 October 2026 · W1-B: the rails draw the registry's maps, written by the icon family; `user` and `key` leave

**Decision.** Supersedes DL54-29 item 3 and amends DL54-27.
1. `portal.services.NAV_GLYPHS` is `icons.NAV` and `companies.services.navigation` draws `icons.COMPANY_NAV`: the
   console rail, its bottom bar and its drawer say the V5 meanings — the journey `ile-steps`, a case `folder`, the
   requests `send`, the deadlines `calendar-clock`, the help desk `concierge-bell`, the Academy `book-open`, the
   selection processes `list-ordered`, a professional's queue `inbox`; the company's needs `wrench`, the analysis `map`.
   `handshake`, `briefcase`, `map-pin`, `university`, `calendar` and `check` keep in the rail the one meaning they have
   everywhere else, so the rails no longer draw them. W1-B writes the two producers; W3-A keeps the rail's composition,
   its collapse control and the rows the modules append without a glyph (`NOTES.md`, «Handed to»).
2. The aliases, checked one by one against who still emits them: `home` stays for `living.catalogue` («Logement») and
   its rows, and resolves to `house` — the V4 drawing, renamed (IC §4) — now that the rails draw the dashboard from
   `NAV`; `list` stays for `portal.services._requests_card` (W3-B); `globe` stays for `living.catalogue` and
   `pathways.services.DEFAULT_ICONS`; **`user` and `key` leave the registry and the sprite**: no producer emitted them
   (the navbar's plate writes `ile-key` since the merge), and the dev showcase's list, the last place that named the
   five, names symbols only. The sprite is 110 symbols + 3 aliases, 31 049 B raw.

**Why.** The senior review's M1, measured on its 204 captures: `handshake` rendered 136 times and every one meant the
help desk, `briefcase` 208 times and never the professional, the mortarboard twice with two meanings on «Mes pièces»;
below 90rem the rail is glyph-only, so those drawings were the whole signifier. V5.5 ships the product: the
platform-shell family has not started, and a product that says V4 meanings with V5 drawings does not ship. An alias
nobody emits is not kept «just in case»: it is a second name for a glyph, the thing the registry exists to prevent.

**Source.** `docs/design-v5/QA/v54/w1-b/REVIEW.md` M1; V5.5 (implement → review once → fix → ship); plan §1.7, §2.3
(«Icons»); IC §4, §5; `tests/frontend/test_icons.py` (`test_the_rails_emit_the_registrys_symbol_for_every_entry`, the
alias set), `tests/frontend/test_browser_w1_b.py`; evidence `C:/tmp/ile_v5_council/evidence/v54/w1-b/fix/`.

## DL54-33 · 9 October 2026 · W1-B: an empty state says which space is empty — the neutral mark `empty`

**Decision.**
1. `components/empty_state.html` draws the glyph its caller passes, and `empty` when the caller passes none: a frame
   drawn in dashes — four mitred corners and one dash a side, an ILE drawing, utility tier, floor 16 px (measured),
   the closest symbol 0.51 alike at 16 px. Never `document` by default: that glyph is «Mes pièces».
2. Which glyph: an empty PAGE passes its domain's concept glyph — the FAQ `circle-help`, the glossary `book-a`, the
   news `newspaper` (the home's block and the index), the Forum `handshake`, «Vivre en Italie» `sprout`, a console
   list its own (`CARD`, `calendar-clock`, `mail`, `send`, `compass`). A REGION under its own heading — the four
   sections of a pathway page, a topic's sheets, the profile's organisations — and a page whose domain the registry
   does not draw (the partners: IC keeps `handshake` for the Forum only and «Réseau» a word) draw the neutral mark.
   IC §3.7 gave an empty region no icon at all: the neutral mark replaces that blank, because the component is one
   composition — a glyph in its disc, a title, a sentence — on every page that uses it, and W3-E redraws it.
3. `components.css` §23 no longer writes a `stroke-width` on `.empty-state__icon`: the glyph is drawn by the `.icon`
   rule, 1.5 px like every other (it read 1.25 px since DL54-26's non-scaling strokes).

**Why.** The review's M2 and M3: `document` meant «nothing here yet» on ten public pages, and the empty states were the
only glyphs of their page drawn with a thinner hand. One glyph, one concept — in both directions.

**Source.** `REVIEW.md` M2, M3; IC §3.7 («Empty page: the domain's concept glyph — one glyph that says which space is
empty»); `apps/core/icons.py` (`EMPTY_STATE`); the measurement
`C:/tmp/ile_v5_council/evidence/v54/w1-b/fix/measure/metrics.md`; `tests/frontend/test_icons.py`.

## DL54-34 · 9 October 2026 · W1-B: under forced colours an icon inherits its ink and paints no ground

**Decision.** `components.css` §2 ends with `@media (forced-colors: active) { .icon { color: inherit !important;
background: none !important; } }`. Under forced colours an icon is the ink of the text beside it — `CanvasText` in
running text, `LinkText` in a link, `ButtonText` in a button, `HighlightText` on a selection — whatever rule coloured
it, and it paints no ground of its own. The three forced icon colours other sheets already wrote (`v4/hero.css`: the
legend's glyphs; `v5/chrome.css`: the plate's key and the account glyph, the door's chevron) yield to it: the glyph
takes its control's own system colour, which is the pair the system guarantees.

**Why.** A browser gives `<svg>` `forced-color-adjust: preserve-parent-color`, which follows the palette only while
the svg's own `color` is inherited; a component that colours its glyph kept its authored hex. Measured on 26 cells
(13 pages, a light and a dark forced palette, the bundle of the merge): 140 of 502 icons were not a system colour and
20 stood under 3 : 1 on their ground — the home's navy arrows at 1.38 : 1 on a dark canvas, the footer's night ink at
1.75 : 1 on a light one. `forced-color-adjust: auto` on the icon was tried and is worse (300 of 384 lose the palette);
`color: CanvasText` without `!important` loses to every component rule of two classes and paints a link's glyph in a
colour its ground is not paired with. With the rule: 502 icons, 0 outside the palette, 0 off their text's colour, 0
under 3 : 1. The ground goes because the empty state's disc is painted on the svg itself and would stay light under
an ink turned white.

**Source.** `docs/design-v5/QA/v54/w2-c1/A11Y_PERF.md` finding 7 («icon system (W1-B)») and W2-C1's notes («handed»);
plan §2.5, §3.1; `tests/frontend/test_browser_w1_b.py`, `tests/frontend/test_icons.py`; evidence
`C:/tmp/ile_v5_council/evidence/v54/w1-b/fix/forced/` (`before/`, `product/`, `crops/`).

## DL54-35 · 9 October 2026 · W1-B: the review's minors — the eyebrow's glyph, the row menu's dots, the handshake's floor

**Decision.**
1. **A glyph set in a line of text sits on that line** (`.icon--inline`, `components.css` §2): the reset draws every
   svg as a block, so the living topic's glyph stood alone above its title and the pathway page's above its eyebrow.
   Both sit in the eyebrow now (IC §3.6: «a topic's glyph appears on its own page (the eyebrow)»), 16 px, on the line.
   `.icon--heading`, which had no rule, is gone.
2. **`ellipsis-vertical` draws three 1-unit squares**: the 1.5 px stroke then makes a solid dot of 2.1–2.8 px at every
   size. The donor's three points were 1.5 px squares on half pixels — the a11y probe read them as not painted.
3. **`handshake` has a floor of 24 px** (was 20): its two cuffs merge at 20 px. No seat draws it smaller — the rails
   no longer draw it, the Forum's empty states draw 24 px; a 20 px seat redraws it first.
4. **The audiences' floors stand as measured** — `person` and `building` 14, `institution` and `university` 16 — and
   the `glyph--sm` disc draws 16 px (DL54-30 item 2). Plan §1.7's «never below 20 px … in chrome discs the glyph is
   drawn at 24 px» was written before the redraws and the measurement; the senior review judged the four at 16 px in
   the actor discs and the hero's legend, always beside their words, and passed them.
5. `DUE[""]` draws `calendar` on a plain due date by design (a glyph column is all or nothing); its comment says so.
6. The icon board: its ten-column table is a named, focusable region; its journey line wraps instead of scrolling;
   its labels are 12 px; it shows the empty state's row. Four strings it wrapped in `{% translate %}` were not the
   product's (no msgid, so the catalogue test failed and no translation existed): two became the product's own words
   («Processus assignés», «Parcours réguliers»), the two thresholds' captions the board's Italian chrome.

**Source.** `REVIEW.md` m1, m3; `A11Y_PERF.md` m1, m2, n1, n5; IC §3.1, §3.6, §3.7; plan §1.1 (the 12 px floor), §1.7.

## DL54-36 · 9 October 2026 · W1-B: the fix pass's paths outside the slice (adds to DL54-30)

**Decision.** For the steward to write into the manifest at the merge, with DL54-30's five:
1. `apps/portal/services.py` — `NAV_GLYPHS = dict(icons.NAV)` and the import: W3-A's slice («NAV_GLYPHS → the
   registry»), written here by DL54-32. Nothing else of the file is touched (the cards' `icon=` stay W3-B's).
2. `apps/companies/services.py` — `navigation` draws `icons.COMPANY_NAV[key]` (the four literals leave, the import):
   nobody's in the manifest; DL54-32.
3. `apps/core/dev.py` — the showcase's `ICONS` list names symbols only (five names, one of them a duplicate):
   nobody's in the manifest; DL54-32 item 2.
4. `static/css/components.css` §23 — one declaration removed (`.empty-state__icon { stroke-width: 1.25 }`): W3-E's
   section, DL54-33 item 3. The file is in W1-B's slice for §2 only.
5. `tests/i18n/test_rtl_static.py` — one function, `test_previous_page_icon_points_backwards_in_both_directions`
   (W1-A's file): RTL-07's guard pinned the V4 mechanism — the forward arrow turned by `.pagination__icon-prev` — and
   had failed since the family gave «Précédent» its own back arrow, `arrow-start`, on 8 October; nobody had run
   `tests/i18n` on the branch. The guard follows the mechanism (the symbol, the flip list, the tag's class, the rule of
   `base.css`), its intent unchanged. The two dead `.pagination__icon-prev` rules of `components.css` §22 stay W3-F's.
6. `tests/frontend/test_design_preview.py` — one assertion of
   `test_the_index_lists_the_foundation_s_specimen_boards` (W1-P's file): the index links a board the moment its
   template exists, so «Il foglio delle icone» is a link since the family wrote its board; the test said «non ancora».
7. `tests/frontend/test_browser_w1_b.py` — new, the family's own per-family browser file (`tests/**/test_*_w1_b.py`,
   already in the slice); named here because it signs in with `Client.force_login`, as the other browser files do.

**Source.** Plan §2.2 («a path nobody owns … the steward adds the assignment»; the serialized table for
`apps/portal/services.py`); V5.5; `scripts/check_ownership.py w1-b design-v5` (9 paths OUTSIDE: DL54-30's four files
and items 1–3, 5 and 6 above).

## DL54-37 · 8 October 2026 · W1-D: the loader «Lume» as built

**Decision.** Built by W1-D on plan §1.9, with these choices met during the build (plan §5.2: one entry, its reason,
its evidence):

1. **The release is served, not scripted.** `user_logged_in` — allauth's sign-in, `Client.force_login`, the preview's
   persona switch — leaves a flag in the session (`accounts.signals.mark_entrance_release`); the first console page
   consumes it once (`{% entrance_release %}`, `accounts.templatetags.entrance`) and renders the rail's mark — below
   64rem the top bar's — as `components/loader.html` with `release=True`; the lit doorway is a CSS animation of the
   console-only generated sheet `v5/_loader-light.css` that starts at the first paint, across the page load, with or
   without script, and never over painted content. A refused sign-in never sends the signal. Every later page carries
   the `<img>`; the drawer always does.
2. **One phase, `--motion-door`** (1600 ms): the light grows from the key's eye at full opacity from a disc the size
   of the bow (the 80 ms ramp happens over the bow alone, which is the fix of the muddy grey-beige of LS §6 before any
   measurement), is full at 360 ms, holds lit to 1000 ms (≥ 600 ms, §1.9 condition 1), fades back by 1400; the key
   reads in ink from 80 to 1300 ms. The rest state of both layers is declared in `v5/loader.css`; under reduced motion
   the token is 0 ms and `fill-mode: both` lands the mark on the still. No `will-change`: the layers are composited on
   their own (the trace in the family's notes).
3. **L2 is drawn by CSS on every busy button, with no markup**: `.btn.is-busy::after` carries `key.svg` as a mask in
   the button's own ink, inside the inline-end padding (0 px of label shift, nothing laid out again); `shell.js` sets
   the class in the submit's own task on every form of the site and imports `loader.js` then, never before. The plan's
   «260 ms» turn is `--motion-emphasized` (320 ms): no duration is added (§1.5). The key holds dim (55 %) and lights
   on an in-page answer. `main.js`'s double-submit guard sets `aria-disabled`, never `disabled`: the focus stays.
4. **L3's «40 ms apart» is `--motion-stagger`** (60 ms): the one stagger token, rather than a typed number; the rows
   rise 4 px in `--motion-standard`; the seat plays on a container's first arrival only (`data-seated`), never on a
   server-rendered region. No product region fetches asynchronously today: the seat ships as the primitive and the
   board, and the Wave-3 families attach it to their containers.
5. **The engage's 480 ms is `--motion-slow`**, on `--ease-turn`, 0 → 360° in one turn. A submit from the keyboard
   plays the same turn: R-07 («the keyboard never animates», tier 0) governs the changes a navigation key asks for —
   a focus that moves, a tab that changes — and a submit is an activation whose feedback is the same whoever asked;
   the reviewer may rule otherwise, in which case `html[data-input="key"]` gets the one zeroing rule.
6. **The words of a long wait belong to the including template.** `components/loader.html` carries no string: the
   1 s word, the 10 s sentence and «Réessayer» are passed in (`word`, `slow`, `retry`) by W2-B's login with its own
   translations; W1-D adds no catalogue entry. The release's seat has no words.
7. **The mark in layers rasterises as the one-file mark**: the base and the key are two full-size SVGs from one origin
   (the layer formula of `.sig__l` keeps mark units for a stage's key box); the bow is a ring of the mark's own radii,
   so the light shows through the eye and the gold key is the verbatim key over the navy door.

**Why.** V54 l.19 (door, key, rotation or opening, light), with M10's reasons kept (DL54-09) and the light only after a
successful sign-in (RTD-M6). Items 3 and 4 keep §1.5's «no duration added»; item 1 keeps the release out of script so
that it needs no frame and no event; item 6 keeps the locked-copy and no-text-in-JS rules.

**Source.** Plan §1.5, §1.9, §2.3, §3.3 item 6; LS §3.2, §5.2, §6; RTD-M6, RTE-m6, RTD-m2;
`docs/design-v5/QA/v54/w1-d/NOTES.md` step 2. Written on W1-D's branch as DL54-20; renumbered DL54-26 on 9 October
2026 when design-v5 was merged into the branch (W2-C1's DL54-20 … DL54-25 had reached design-v5 first), and
DL54-37 by the steward at the family's own merge the same day (W1-B's DL54-26 … DL54-36 had reached design-v5
first) — content unchanged both times. The family's review and accessibility reports of 9 October
(`QA/v54/w1-d/REVIEW.md`, `A11Y_PERF.md`) and the notes before that date cite this entry as «DL54-20» and the next
one as «DL54-21»; the notes of the fix pass («Review fixes») cite them as «DL54-26» and «DL54-27».

**Addendum, 9 October 2026 (W1-D, the review-once of V5.5 on its own filmstrips).** Item 2's exit is changed: the light no longer
fades back by opacity over the navy door — the 4× filmstrip of the rail seat (8 October, `step2/release`) showed the same
grey-beige on the way out that LS §6 named on the way in (83 % of the doorway's interior in the blend at 1200–1280 ms). The
light now **withdraws into the key's eye** on `--ease-sine` from 1000 to 1400 ms (the lit disc shrinks back to the bow's size) and
goes out over the bow alone in the last 80 ms, as it came; the key reads in ink from 40 ms (the moment the light is under it)
to 1360 ms. One phase, the same three animations, the same tokens; `scripts/gen_loader_light.py` is the record, the generated
sheet and the console bundle were rebuilt, and the measures before and after are in the family's notes (step 2).

**Second addendum, 9 October 2026 (W1-D, the fix pass after the review-once and the accessibility check; V5.5).** Six
corrections to the hook, the state machine and the sheet; none to the motion.

(a) **No wait is for ever** (review M1). A control whose answer did not replace the page — the account's «Exporter mes
données (JSON)» — kept `is-busy`, `aria-busy` and `aria-disabled` until the page was reloaded. Now a form whose answer is a
file says so with `data-loader="none"` and never waits: `shell.js` sets nothing and imports nothing, and
`test_loader_rules` holds that every form posting to a view that answers with an attachment carries it; a form that opens
elsewhere or closes a dialog is read from its own markup. Every other wait is a **lease**: `SLOW_AFTER` — 10 s, the moment
«Réessayer» is offered — plus the time the form's files need at 16 KiB/s, at whose end the form is at rest and can be sent
again, unless a host is offering «Réessayer», which leaves the choice to the person. A submit cancelled by a listener that
runs after the hook (an answer given in the page) is at rest in the next task; a page back from the back/forward cache is at
rest (`pageshow`, in `loader.js`, `shell.js` and `main.js`). No event tells a script that an answer was a download or a 204:
hence the declaration for the case that is known and the lease for every one that is not.

(b) Only a `.btn` waits — the account menu's logout, a plain button, no longer declares an `aria-busy` nothing draws — and
`aria-disabled` is set only where `main.js` really refuses the second submit (`data-single-submit`). When nothing waits and
no host is named, the module is not loaded.

(c) Item 3's dim face is **80 %** of the button's ink, not 55 %. Measured on the pixels of real activations — pointer,
keyboard, tap; French and Arabic; 1440 and 390 — it reads 4.0 : 1 on the teal every busy button has today (2.7 before),
3.6 at its weakest pixel (WCAG 1.4.11: the key is the one visual indicator of the state). The accessibility check proposed
65 %: 3.2 on that teal, but 2.9 on the ghost's own ink and ground, for the day a busy button keeps its own surface (W1-C);
80 % keeps every variant's own pair at 3.9 or more.

(d) The key sits **in the middle of the inline-end padding**, whatever the size — the slab's own padding expression —
instead of a fixed 8 px from the edge: on a small button it stood 1.2 px from the label's last glyph, 0.3 px in Arabic; it
now stands 5 and 3 px away (7 in a button, 9 in a large one).

(e) **Where the key has no place there is no key** (the accessibility check's second major). A link-styled button
(tertiary, link, text, inline) and an icon-only one have no padding, and the key was drawn over the label's last glyphs —
measured on «Marquer comme lue»; «Supprimer» in the documents' table, a `.btn--text`, is the same case. The first correction, the key after the label and outside the
box, was withdrawn before it was merged: the box of such a button ends where its neighbour or its container's edge begins,
and under V4's busy rule the link becomes a slab while a key outside it is drawn on the page's ground in the slab's ink.
`shell.js` gives those variants no class — so neither the key nor the slab — and `aria-busy`: they wait as they are. The
list (`KEYLESS`) is read by `test_loader_rules` against the sheets, so a new variant without padding cannot be forgotten.
This is the design system's own table: DS V5 §10.1 gives the LINK button no loading face («—»), and the ICON button a key
that replaces its glyph — a face W1-C draws with its buttons; until then an icon-only submit, of which the product has
none, waits like a link.

(f) «Réessayer» hands the focus to the form's submit control before it hides; under forced colours the ink layer is hidden
by `.sig__turn > .sig__face--ink`, which beats the layer rule.

Left to their owners. V4's busy rule (`v4/buttons.css`: a busy secondary, danger or ghost button repainted as the primary)
is W1-C's to retire with its sheet: neutralising it from `v5/loader.css` with `--btn-fill: initial` would also strip the
variant's own fill (`v3/buttons.css` reads `var(--btn-fill, transparent)` and the busy rule's specificity beats the
variant's), so it is not done here. Under reduced motion the release keeps the plan's letter — the end state without
travel, i.e. the verbatim mark — rather than a lit still; the trade-off is recorded in the review (m4) for the Creative
Director.

## DL54-38 · 8 October 2026 · W1-D: every V5 duration lands at 0 ms under reduced motion

**Decision.** `static/css/v5/tokens.css` zeroes, under `prefers-reduced-motion: reduce` and under its twin `html.rm`,
every duration it declares — `--motion-key`, `--motion-door`, `--motion-luce` and the two staggers included, which
W1-A's §12 note had kept «because a 0 ms loop spins on itself». Nothing in V5 loops (plan §1.5 «Nothing loops»), and a
one-shot at 0 ms lands on its still, which is the designed state. `--motion-wait` (a threshold) and `--motion-reduced`
(the one 80 ms opacity, MS-O4) keep their values.

**Source.** Plan §1.5 «Reduced motion, built as a state»; RTE-M2; W1-D step 1 (`e62805e`), `test_v5_tokens.py`,
`test_rm_flag_parity.py`; `docs/ACCESSIBILITY.md` §7. Written on W1-D's branch as DL54-21; renumbered DL54-27 on
9 October 2026, then DL54-38 at the family's own merge the same day, with DL54-37 (its Source paragraph tells
why), content unchanged.

## DL54-39 · 8 October 2026 · W2-D, the hero's port: the decisions met during the build

**Decisions** (the family's, under V5.5 — implement, review once, fix, ship; the hero-final CD decision's conditions
C-1, C-3, C-4, C-6 a + b, C-7 and C-8 carried as the proof's round-2 fixes; C-9 the port itself).

1. **The hero's description is the hero's last row and the fold's peek.** `p3.hero.body` stays inside the hero
   (`apps/pages/tests/test_home.py` asks it there) as `.he__body` under the composition, and `--peek` is sized so that its
   first line shows whole at the fold (48 · 40 · 32 px); chapter 01's folio follows it. The brief's «eyebrow at the fold»
   (HF §3.6) becomes «the description at the fold»; W2-E may move the paragraph into chapter 01's head (the prototype's
   `.he-next__statement`) and retarget the test — a forward correction, no revert needed.
2. **The stations are drawn only in the Phase 3 variant.** They are the locked pilot sequence (`p3.pilot.sequence`, items
   2–6, after the origin's shore «Maroc» from the catalogue), which gate G3 forbids while closed; the interim variant draws
   the path, the four origins and the door, with its editorial eyebrow, title (as the promise) and lead.
3. **`v4/hero.css` is shrunk, not deleted.** `components/doorway.html` still draws the entrance page's door from its paint;
   the file keeps only that paint (its hero rules are gone) and leaves `main.css` with W2-B's `static/css/v5/_door.css`
   (plan §2.3's row «v4/hero.css — W2-D» is done for the hero; the file's last consumer deletes it).
4. **The repeatable flow** (the owner's V5.5 directive: «a REPEATABLE interaction flow»). The discovery plays once per
   session (CD R6); on the settled hero a hover with a fine pointer or a touch on an origin runs the light along the one
   path to the door again, every time (`static/js/src/hero.js`): the shore's glint, the inlay's light, the gold run, the
   arch light, the steps' twins — ≈ 1.3 s, transform and opacity only, cancelled where it stands when the hand leaves;
   never from the keyboard (its states are instant, D7), never under reduced motion or forced colours; the key does not
   turn under the hand (D8).
5. **The four photographs pair with the four entrances by order** (`pages.content.ENTRANCES`: person, company, institution,
   university ↔ lectrice-bibliothèque-dos, chai-cuve-chêne, table-en-séance, paillasse-deux-étudiantes), through
   `{% cycle %}` in the partial — `apps/pages/services.py` is not W2-D's — and a test holds the pairing.
6. **The secondary's glyph** is the sprite's `compass` (the proof's `ile-steps` glyph is not in the product's sprite; W1-B
   may give the entrance its glyph).
7. **The stage's layers use logical properties.** The stage is `direction: ltr`, so `inset-inline-start` IS the drawing's
   left; the static RTL guard needs no allow-list, and the aperture's shift carries an identical `[dir="rtl"]` twin.

**Source.** Plan §1.17, §2.3, §3.4 item 4; DL54-06, DL54-08, DL54-11, DL54-12; HERO_FINAL.md «Review fixes — round 2»;
QA/hero-final/CD_DECISION.md §5–§6; the owner's V5.5 directive (5 October 2026, 14:32).

Numbered DL54-17 on the family's branch, DL54-20 at the first merge of design-v5 into `v54-w2-d` on 9 October 2026 (W1-P's DL54-17 … DL54-19 had reached design-v5 first), DL54-26 at the second merge of that day (W2-C1's DL54-20 … DL54-25 had reached it first), and DL54-39 at the third, in
the evening (W1-B's DL54-26 … DL54-36 and W1-D's DL54-37 and DL54-38 had reached it first), with the family's two other
entries — DL54-40, the review fix, was DL54-27 that afternoon; DL54-41, the home around the hero, was written as DL54-28;
their contents unchanged.

## DL54-40 · 9 October 2026 · W2-D, the review fix: the prototype's measured defects closed in the product

**Decisions** (the family's, under V5.5 — implement, review once, fix, ship; each on a reviewer's measured finding of
5 October — `QA/hero-final/design_s2r2.md`, `taste_s2r2.md`, `ux_s2r2.md`, `motion_s2r2.md` — re-measured in the product
on 9 October: `QA/v54/w2-d/NOTES.md` §7).

1. **The register under the hero is not drawn where the hero carries the four sentences.** On the desktop (≥ 64 rem) and on
   the tablets whose tiles draw the sentence (≥ 40 rem wide and ≥ 30.0625 rem tall), the four origins give word, sentence and
   call at rest, and the chapter under the hero (`templates/pages/home/_entrances.html`: the same four, the same sentences, the
   same links) repeats the hero's question (UX-1, design M-6; RH-5 «the audiences once», RH-6 «each block raises a new
   question»). The rule lives in the hero's own sheet, as `.he + .home-entrances` (and through the banner), so it holds only
   under the hero and only while the hero is on the page; the markup stays (the list is the page's structure; the home's tests
   still count four piers). On phones, short heights and landscape — where the tiles carry words only — the register stays:
   it is the page's one copy of the four sentences, and it reads at 16 px (RE-4, UX MOB-1), again from the hero's sheet. Nothing
   locked is rewritten, only not repeated. W2-E gives the chapter its next answer (the proof: the Forum's date, the places, the
   partners) and may move these two rules into the chapter's own sheet.
2. **The keyboard's share of the repeatable flow, and a real replay control.** Focus on an origin runs its light along the
   one path (its states stay instant: CSS, `html.he-keys`); a blur fades the light where it stands, as a pointer leaving does.
   A `<button type="button" class="he-replay">` stands over the golden key, inside the door box and outside the stage — the
   stage, the reveal and the halo carry `aria-hidden`, the niche no longer does, so the control is reachable by assistive
   technology —, named by the catalogue («Rejouer l’animation de la porte», with its Italian, English and Arabic translations:
   a new interface string, `locale/**`, a path the manifest has no owner for), symmetric about the key's centre so that it is
   the same box from either edge in Arabic, ≥ 44 px on the smallest phone stage, the night focus ring of the one focus system.
   Enter, Space, a click or a tap replay the whole sequence from the closed door: the three lights of the ajar door fade in
   240 ms, then the discovery plays again. `hero.js` shows the button only on a page that moves (`has-replay`); under
   reduced motion and forced colours it is not drawn. The key answers the hand and the focus before it turns — its halo lit
   softly (`:hover` under a fine pointer, `:focus-visible`): the pointer's sign that it is a control, the ring being the
   keyboard's. The door itself never becomes a control (a clickable door over «ENTRÉE EN ITALIE» would read «click to enter
   Italy», UX round 2): the key is the one object a visitor expects to turn.
3. **The hero's own turn curve** — `--he-ease-turn: cubic-bezier(0.45, 0.05, 0.55, 0.95)` in the hero's token block, 800 ms
   on the desktop and 640 on a phone — so that the half-turn (90° → 270°) lasts 250 / 200 ms, 15 / 12 frames at 60 Hz
   (motion M-B: on `--ease-turn` it took ≈ 80 ms, «a flick»). A warm halo behind the key while it turns and a glint across
   the bow as its face returns are the turn's light response; they stay inside the stage. **This supersedes DL54-05's «hero»
   for the hero's key only**: the loader and the login keep `--ease-turn`. An interruption still lands the key forward, now at
   the turn's own pace instead of a 340° whip in 120 ms (motion m-4). The desktop's door opens as the key lands; the four's lift
   waits for the key's halo to go (no frame changes more than 10 % of the screen by luma: D4's curtain); END 3.55 s at 1440
   and 2.75 s at 390 (D3).
4. **The door's rest is .9, and the band is brightest at the gap.** The settled band, spill and bloom rest at .9 (DL54-11:
   the revert is now «the 0.9s to 0», in `hero.css` and in `hero.js`'s last keyframes); the band's paint falls off across its
   own width from the leaf's opening edge toward the leaf, no flat core, its inner edge softened (taste m-1, motion m-3); the
   bloom α .45 at the edge, stronger on phones; the phone's band at 16 % of the leaf (D9's cap) — the phone's door beat
   (motion M-C) measured ≥ 4 % of the screen by luma for ≥ 600 ms at 390 and 360 after the fix (3.7 / 3.3 % peaks, never ≥ 4,
   before it).
5. **The wall takes the page; the columns are as wide as the door leaves them** (design M-2, M-3; taste M-B; the CD's
   C-6 c). The proof started the wall on a 1320 px container's edge (60 px at 1440, 300 px at 1920). The product's chrome
   («Il portico», merged on 9 October) and its chapters stand on another column — the container's 40 px margin: 100 px at
   1440, 280 px at 1920 —, so that edge aligned with nothing. The wall now starts at the page's pad (32 px) at every desktop
   width — the hero is the page's one full-bleed band, the niche bleeding at the far side —, ends 16 px before the reveal
   (24), and the stage box stands on the reveal and on the page's edge (`--niche-pad` 28 → 0: the arch keeps its own 24
   stage units of night on either side, ≈ 35 px at 1440). Past `--wall-max` (75 rem: four columns of ≈ 282 px) the leftover
   goes to the start side (2560 × 1440: 422 px). Measured, fr = ar: columns 196 px at 1440 × 900 with 192 px plates (177 in
   the proof) and 4 · 5 · 5 · 3 lines (5 · 5 · 6 · 4); 222 px at 1536 × 864, 3 · 4 · 4 · 3; 245 px at 1680 × 960,
   3 · 4 · 4 · 3; 277 px at 1920 × 1080, 3 · 4 · 4 · 2; 195 px at 1366 × 768, 4 · 5 · 5 · 3; 170 px at 1280 × 800,
   5 · 5 · 6 · 4 (5 · 6 · 7 · 4). C-6 c is met as the CD wrote it (≤ 5 lines at ≥ 1440) and no column is over four lines
   from 1536. **Four lines at 1440 × 900 are out of the geometry's reach**: in the product's face at 15 px Entreprises needs
   233 px and Institutions 236 px for four lines — 992 px of columns and gutters — and the whole wall is 879 px there with
   the niche pad at 0; the type is not shrunk for it (design M-3: «by width, not by a smaller size»). Plates: the 1 : 1 ≤
   192 px (its 384 file at DPR 2: C2); a 4 : 5 plate ≤ 208 px from 1680 × 940 (a 1080p window) and ≤ 240 px from
   1800 × 1060, where four-line columns leave it the height; ≥ 160 px at ≤ 800 px tall (192 from 1536 wide, 176 at ≤ 736);
   the 3 : 2 plate only below 1536 wide at ≤ 736 tall (design M-2, IM-10). The cell is on the 4 px scale: plate → text 12,
   word → sentence 4, sentence → call 8 (4 at ≤ 800 px tall, a step of the scale); the stems ≥ 24 px (A3). The stations'
   distribution is the figure's own — Maroc at the path's start, three nodes over the gutters, the fifth before the reveal —
   and is recorded here as SP-1's exception (design M-1).
6. **C-6 d by the three levers left** (design M-5, taste M-C a): the inlay one step deeper (`--he-bronze` #8f5f1f → #7a4f16,
   ≈ 6.5 : 1 on carta-50, its arris α .7), the five wall labels at 600, the plates' base grade at `contrast(1)` (the chips keep
   1.12). The stepper idiom (rings on a line) is kept: the stations are the pilot's live sequence and the owner's figure.
7. **One edge per column on the Arabic page** (design M-4): every French run (`lang="fr" dir="ltr"`) ends on its column's
   start edge — the promise, the desktop's sentences and calls, the phone's and the compact desktop's station labels
   `text-align: end`; the wide desktop's three inner station labels centred over their nodes, as on the French page, and the
   fifth start-aligned, on its node's side; the door's inscription centred under the stage; on the desktop the description
   too ends on that edge (its box hugs it and is narrower than a wide wall: left-aligned, the paragraph started mid-wall at
   1920), while on phones and tablets, where its box is the page's width and it runs to eight lines, it keeps its own
   alignment. The product's base sheet starts every French run of an Arabic page at (0,2,1); the hero's rules sit above it. An Arabic station name is never under 14 px (the tokens' Arabic floor):
   «المغرب» at 14 px where the Latin labels are 12 (≤ 1366 wide, the landscape plinth). Measured at 1440: the promise, the
   primary, the first plate, the Arabic word and its French sentence share the wall's start edge (x = 1408); on phones every
   rail label's lines end 10 px from the rail's node, as «المغرب» does.
8. **The travelling light has a body** (motion M-A): on the wall a 16 × 12 px bead with a comet's tail — a warm band ±14 px
   about the inlay, brightest at the head and gone 30 rem behind it (`--he-tail` under its mask: no cut at the leading edge, as
   the first pass's two ellipses had) — and the inlay held lit behind the head until the doorway has taken the light (a wipe,
   as the night's, instead of a glide back to bronze in ≈ 280 ms); the stems' light a 10 px amber column with a bright core
   (a pale wipe on a light wall was not seen); the stations' glints 21 px, filled gold; the night's gold run with a 14 px
   glow; on phones the rail's and the floor's beads with a 14 px glow in 20 px clips. The light takes ≈ 930 ms from the shore
   to the door on any wall (≈ 700 ms under the hand), so the clock keeps its length where the wall takes the page. Measured
   frame to frame (ΔE00 > 6, 150 ms pairs; NOTES §7.5): 0.33–0.48 % of the screen in every pair of the travel at 1440 × 900
   (the proof: 0.13 % at most), 0.41–0.60 % at 1920 × 1080, 0.31 % and more down the phone's rail at 390 (D4's «no hole»
   floor is 0.3 %), 0.46 % and more at 360; no pair under 0.3 % at any size. The seat's target of 0.5–1 % in every pair
   would need a glow tall enough to wash the station labels 12 px above the path; not pursued (V5.5: fix what is real, do
   not chase the instrument).
9. **The phone tile** (UX MOB-1, m-1, m-2; design m-5; taste m-4): the word 16 px at every width, the chip 52 px under 376 px
   so «& Formation» keeps its line; the arrow's own row ends at the word's box, not at the tile's far edge (the text column keeps
   its basis 0 beside the chip and aligns its items to the start — a shrink-to-fit basis made the long labels wrap under the
   chip) — the three seats' inline arrow does not fit: at 360 the tile's text column is 90 px, and «Entreprises →» needs 98 px,
   «& Formation →» 106; the stations keep 13 px on the short phones; in landscape the tiles are 52 px with 8 px gaps so that the promise
   stands 16 px under the letterhead with the door where it was, and the plinth keeps its two lines of three at 12 px (the
   Latin floor). Below 48 rem a tile that carries the sentence (the small tablets) sets it at 16 px (RE-4).
10. **The halo's box ends above «ENTRÉE EN ITALIE»** (motion m-1) and its reach is .64 → .5 of the stage's height, a little
    brighter: the label is never promoted into a moving layer, and the rim fades out above it.
11. **The door stands on the niche's floor, and the composition keeps the hero's height** (taste M-A; a port defect). Since
    the description became the hero's last row (DL54-39 item 1) the grid's `min-block-size` was met by that row and the
    composition's own tracks shrank to their content: the niche ended 8 px under the stage and the description rose 20–40 px
    into the first screen. An empty item spanning the composition's tracks (`.he::after`) carries the height again — a
    subgrid's own minimum does not reach its parent's tracks —, and the fold's peek is the designed one (64 · 56 · 48 · 48 ·
    40 · 40 · 32 px from 1920 × 1080 to 1280 × 720: the description's first line whole). With the height back, the proof's
    centred stage left 56–134 px of empty wall under the columns and 20–40 px over the promise (taste M-A, larger now that
    the columns are shorter). The stage stands instead 16 px above the niche's floor (`--door-floor`) and the height left
    over is headroom above the arch: the path stays on the springing by construction (0.0–0.1 px) and the statement and the
    four move down with it — 52 px of air over the promise at 1440 × 900 (28), 102 at 1920 × 1080 (78), 44 at 1536 × 864
    (25); under the columns 56 px at 1440 × 900, 42 at 1680 × 960, 63 at 1920 × 1080, 45–51 at 1280–1366, 74 at 1536 × 864
    and 65 at 1280 × 720 (the seat's 48 ± 4 px at every size is not reached: the columns' heights step with the line counts
    and the plates' tiers). The compact
    desktop gives its leftover to the statement's row too: the path, the door hung on it and the four rows stand on the
    hero's foot, as in the proof; the floor is the stage box's own margin, so the door keeps its 16 px there too (3 px at
    1279 × 900 before). The stage is not replaced, not resized and not mirrored: it stands lower in its niche.
    And the hero has a foot: 56 px of its own ground under the description (32 px on phones), which had ended 0–14 px above
    the next chapter's change of ground. Under forced colours the niche's edge is an outline, not a border: the stage box
    fills the niche, and a border's 2 px pushed it 1 px past the page's edge.
12. **The stations' list is not reset by the product** (a port defect, found by a structural parity probe: every element of
    the hero, class by class, proof against product). `static/css/base.css` resets `ol[role="list"]` to a start padding of 0
    at (0,1,1), over the hero's `.he-stations` at (0,1,0): on phones the rail's six nodes and their labels stood 16 px off
    the rail — its line through the labels' first letters — and on the compact desktop Maroc's disc stood off the path's
    corner, since the port and through two smokes. The list's six rule heads carry the hero's class (0,2,0); a browser test
    holds the nodes on the rail (`apps/pages/tests/test_browser.py::test_the_hero_holds_its_geometry`).
13. **Not done, by decision**: the shadow ledger (design M-1, taste m-3: ≤ 4 values — a refactor of the plates', the CTA's and
    the treads' edges into borders, not a fix); the re-cut of the black-and-white derivatives to one tonal map (design M-2:
    the Image Art Director's, O54 / O55); CTA-B's radius (W1-C's button system); the promise's weight (taste m-8: W1-A's type
    decision); the travel's 0.5 % in every 150 ms pair (item 8).
14. **The door is told its width, and a short window keeps the tablets' door** (found at the end of the step, on a number
    the smokes had carried since the port: at 1366 × 768 the 400 px file drawn 409 px wide). The door's `sizes` — the hero's
    centre and the page's LCP image — gave the width at the *bottom* of each range of windows, so above it the browser was
    told less than the truth and took a file too small: `door-1`, 15 of 55 windows — the 576 px file stretched 15 % at
    1920 × 1200 and on a 2560 × 1440 screen, the 400 px file 6 % at 1440 × 799 and 2 % at 1366 × 768, 8 % on a phone lying
    down (34vh said 133 px, the door is 144). `sizes` now follows `hero.css` rule for rule and says the widest the
    photograph is drawn: on the desktop the photograph is the hero's height less the door's two pads, × 320 / 456 — one
    line per regime of the pads, in `vh`, with the smallest peek of its range; 41.4375 rem at the hero's 64 rem ceiling; the
    niche's 40vw in the compact band; below 64 rem `--arch-w`, the cascade read from its last rule to its first, without
    `min()` or `max()`. The preload's `imagesizes` is the same string (C-9; `test_home.py` holds the two equal). `door-2`,
    102 windows — the 55 and the edges of every rule: none under-told, none stretched at density 1; told within 2 % of
    drawn except where the niche's width caps the door in a tall narrow window (+ 18 % at 1280 × 1024: one candidate
    heavier at most, never a stretch). Above density 1 the browser's own rule may take a file a little short of the
    device's pixels; the one window where no file is large enough is 1728 × 1117 at density 2 (1 229 px needed, the largest
    AVIF is 1 200): a larger derivative is the imagery pass's. Under 64 rem the short-phone rule (`--arch-w: 39vw` below
    700 px of height) passed the tablets' 17 rem in a window wider than 698 px — at 960 × 600 (a small tablet lying down,
    a narrowed desktop window) the door was 374 px wide and its stage 89 % of the window's height: it is
    `min(39vw, 17rem)`, 272 px and 65 % (`short-1`, `short-2`, LOOKED AT).
    `apps/pages/tests/test_browser.py::test_the_door_photograph_is_told_its_width` holds the sheet and the attribute together
    at eight windows.

**Source.** `QA/hero-final/{design,taste,ux,motion}_s2r2.md` (5 October 2026); the owner's V5.5 directive; plan §1.17,
§2.2 (the serialized files), §3.4 item 4; DL54-05, DL54-08, DL54-11, DL54-12; the measures in `QA/v54/w2-d/NOTES.md` §7 and
`C:/tmp/ile_v5_council/evidence/v54/w2-d/` (geom-0 … geom-18, motion-1 … motion-9, keyboard-1 … keyboard-3, smoke-3 … smoke-7, fc-1, page-1, states-1, cls-1,
interim-1, door-1, door-2, short-1, short-2).

## DL54-41 · 9 October 2026 · W2-D, the home around the hero: the chapters as one object, each thing said once

**Decisions** (the family's, under V5.5 — implement, review once, fix, ship. V5.5 gives the area «the final hero in the
real home page and the home made coherent around it»: the chapters under the hero, plan §3.4 item 6, are built here with
the hero, by the same implementer; the A-bis blind test and the council of that item are superseded by V5.5. Measured on
the lane, `QA/v54/w2-d/NOTES.md` §8. Items 2, 3, 6, 7 and 12 say what stands after the merge of design-v5 of 9 October,
evening — W1-B's icon system and W1-D's motion reached design-v5 while the step was being built: `NOTES.md` §8.4.)

1. **Every chapter under the hero is the same object** (`apps/pages/static/pages/css/pages.css`, on the V5 tokens): a band
   on its ground, a head at the reading edge, a body. From 75 rem the head takes four columns of twelve and stays in sight
   while its body scrolls (`position: sticky`, no script); below, the head stands above the body. 48 · 64 · 96 px around a
   chapter (SP-5), 32 px from head to body, hairlines before boxes (SH-2). Titles 28/36 at 600, leads 20/28, a row's
   title 17/24 at 600 over 15/24 (16/24 below 64 rem: RE-4), labels 13/20 — the eight public sizes, and **a title is never
   smaller than what it titles** (the pathways' titles were 13 px over 15 px descriptions and the trust chapter's
   questions 13 px over 17 px answers: the legacy `h4` size, UX D3). Below 75 rem the chapters stand on the page's own pad, the edge the hero's wall starts on
   (16 px on phones, 32 px on tablets); from 75 rem on the chrome's column. The footer follows the last chapter directly
   on this page (its 80 px margin doubled the chapter's own closing space).
2. **One section device, no running head, no ordinal** (PX04, amended). The head opens on the mark's three steps: the
   sprite's identity glyph `ile-steps` — the stair profile, never mirrored (W1-B; plan §1.7 Q8) — in ink, through
   `{% svg_icon %}` in `templates/pages/partials/_section_header.html`. PX04 sets the micro-mark at 14 px beside its
   eyebrow; with no eyebrow it opens the head alone, in the icon scale's 24 px box (a drawing of 18 × 12 px), and the
   box is pulled by the symbol's own margins so that the drawing — not its box — stands on the reading edge, 16 px
   above the title. (Built first, while the sprite had no `ile-steps`, as three stacked strokes drawn inline: the
   drawing the red team's m1 had retired as a near-twin of `menu` and `list-filter`. It left at the merge: one hand,
   one stroke table, one forced-colours rule — DL54-26, DL54-34.) PX04's sentence-case eyebrow is **not drawn**: five of the
   seven running heads repeated the title under them or the link at the chapter's foot («Orientation» over «Comment
   fonctionne l'orientation», «L'écosystème» over «Quatre accès à l'écosystème», «Espace Personnes» over «Voir l'Espace
   Personnes», «Informations» over «Actualités», «Promoteur et partenaires» over the two bays' own labels), and two
   eyebrows on a page of seven chapters are not a system. The folio's ordinals 01–06 go (numbers in front of chapters,
   of the four entrances and of the eight pathways told the reader nothing: UX §2.1); numerals stay on the one real
   sequence, the four neutral steps of the orientation while gate G3 is closed.
3. **The Morocco → Italy model is said once, by the hero's path.** It was drawn three times on one page: the hero's
   path (the origin's shore, five stations of the prescribed pilot sequence, the door), the pilot chapter's «route
   between two shores» (design V2: the same sequence, eight stations between «Maroc» and «Vénétie», on a line drawn with
   the scroll — and broken at every desktop width: UX D4, D5) and the trust chapter's jurisdiction bar
   (four stretches «from the country of origin to the Italian territory», its own caption calling them «the model's
   steps»).
   - **The pilot chapter is a statement** on the night ground: the prescribed title, the section's sentence, one link.
     It prints no station: the first, seventh and eighth steps of the prescribed sequence, which the hero's path does
     not carry, are on the pilot's own page, where the whole sequence is the page's diagram (R-P3-013). Its revert: the
     template (`build_pilot` still hands it `d.steps`).
   - **The jurisdiction bar is not drawn on the home.** What it says in a drawing the chapter says in words four times
     («relèvent exclusivement des autorités compétentes», «Chaque décision appartient aux autorités» …). The component,
     its rules and its data stay (`components/jurisdiction.html`, `register.css`, `pages.services.jurisdiction_segments`):
     its revert is one include line.
   - `static/css/v2/voyage.css` and `static/css/v2/routes.css` leave `main.css` and the tree (home-only sheets with no
     consumer left: plan §2.1 «delete what you supersede»; the deletion map gave `voyage.css` to W3-D with the journey
     it expected to rebuild from it — its last consumer was this chapter); `static/js/src/home.js` loses the route's
     scroll-drawn line. `dist/main.css` 43 258 → 41 963 B gzip (42.2 → 41.0 KB); the home's CSS in all 0.1 KB less
     (before the evening's merge; with W1-B's and W1-D's sheets the merged `dist/main.css` is 43 186 B, 747 B under
     design-v5's own 43 933 B).
4. **One thing once, in the composition too** (`pages.services._say_once`). While gate G3 is closed — what the site shows
   today — the hero's description is the first of the two Phase 1 fragments, and the trust chapter listed the same
   sentence again under «what the platform does». The chapter now keeps its other statement; an editor who gives the
   hero another description gets the whole list back. No text is changed, and the order of the sections stays the back
   office's (the master brief's §21 order is kept: the RH-6 chain reads promise · doors · path → where to start → which
   ways → where it is tried → what it does and does not → the warning → the news → who stands behind it → the reserved
   door).
5. **The register under the hero is the legend's continuation** (DL54-40 item 1 kept: not drawn where the hero carries
   word, sentence and call). On phones it is the page's one copy of the four sentences: one frame, four rows (two bays
   from 48 rem) — the prescribed title, the sentence at 16 px, the call with its arrow beside the words; **no ordinal
   and no landform glyph** (PX02: the four are never ranked). Its lead, which names the four a third time between the
   hero's four and the register's, is not drawn under the hero.
6. **The grounds are the composition**: the page's paper; the one BRAND chapter (`--grad-brand`), the orientation — the
   question «where do I start?» beside its action, the prescribed sentence set whole as the chapter's statement (its
   arrows are its own: splitting it into a stepper would restyle a locked text, the owner's and counsel's call); the
   stone under **«il gradino»**, the anti-fraud warning on a plate of its own (PX08: a raised sheet, an ink rule at the
   reading edge — ink, not a status colour —, the prescribed paragraph whole at 36 rem; its sign is the registry's glyph
   of this warning, `shield-alert` (W1-B), the one the footer, the navigation's panels and the anti-fraud page put
   beside it); the night for the pilot's statement and for **the reserved row**, which the footer continues (PX13:
   the key of the mark — the sprite's `ile-key` in the key's gold, on the reading edge, level with the label it
   signs —, not a padlock; one quiet button; a row, never a chapter). Two night grounds on the home is the ceiling (`test_browser.py`).
7. **The trust chapter** is four questions and their answers in one column at the reading measure (UPu HO-3). A question
   stands on its own line and wraps as it comes: a balanced wrap broke the prescribed questions inside their verb–pronoun
   inversion («reconnaît- / elle») at every width. **The news** are rows of a register; while nothing is published the
   chapter says so in one row — the empty state's glyph in its disc (DL54-33: the news' `newspaper`; one composition
   on every page that uses it, and W1-B's browser test reads the home's disc), the sentence, what will stand here;
   no dashed frame and nothing centred (only the component's V4 box is undone by the chapter's sheet, until W3-E
   redraws the component). **The ecosystem** is two bays under one lintel, each named once by its own label.
8. **The Arabic page** mirrors the chapter (the head at the reading edge). A French run in a head or in the reserved
   row — a prescribed title with no official Arabic version, an editor's heading — ends on that edge, under the mark
   (DL54-40 item 7's rule: one edge per column); a French reading block in a body keeps its own alignment, in a box that
   stands on the reading edge. The trust chapter's texts carry their own `lang` (the article did, and turned the whole
   block left to right).
9. **French spacing for team-authored strings only** (plan §1.1; D24): the filter `typo`
   (`apps/pages/templatetags/pages_typo.py`) writes a no-break space, U+00A0, before `: ; ! ? »` and after `«` in the
   editorial strings of the chapters — a line started with « : la séquence… » and a link ended on a lone guillemet on
   phones. A prescribed text never passes through it: the templates apply it to editorial variables only, and the
   filter hands back untouched any string that is a prescribed text or carries six words of one in a row (the 275
   strings of the registry: 0 changed). The U+2011 of HO-6 (inversions) is not written: no team-authored string holds
   one, and the prescribed questions are not this filter's.
10. **Black and white stays the hero's** (DL54-12): the chapters ship no photograph today and their sheet declares no
    `filter`; `test_home.py` and `test_browser.py` hold it.
11. **Not done, by decision or for want of a decision that is not the family's**:
    - **No photograph and no drawn figure under the hero** (RH «a picture at least every second screen» is not met:
      the hero, then four screens of type at 1440). The frames are the Image Art Director's under O54 / O55 (plan §1.16;
      D24's diptych); the chapters are built to take them.
    - **RH-4 on phones**: 10.3 screens at 390 × 844 (13.6 before; the rule says 9.5), 11.2 at 360 × 800; 6.1 at
      1440 × 900 (7.4 before), 7.0 at 1366 × 768. The footer is 1.3 of the phone's screens. The one lever left —
      hiding the eight pathways' prescribed descriptions on phones (≈ 0.7 screen) — removes content a person in Morocco
      reads on a phone: not taken.
    - **Echoes that are in the copy itself** (the owner's packet B1): the editorial heading «Comment fonctionne
      l'orientation» above the prescribed sentence that opens «Comment ça marche : …»; while the gate is closed, the trust
      chapter's two column titles under a heading that says both; the pathway «Formation dans le pays d'origine» and
      the station of the same words (two prescribed texts); while the gate is closed, on phones, the register's neutral
      titles under the tiles' same words; the hero's primary and the orientation chapter's primary, two labels for one
      destination (UPu HO-10).
    - The order of the chapters (UX §3.0 proposed trust third): the back office's, and the master brief's.
12. **The hero's script passes through the one motion gate** (W1-D; plan §1.5 «Reduced motion, built as a state»).
    `static/js/src/hero.js` read the reduced-motion query itself and called `element.animate()` and
    `requestAnimationFrame` directly: it was written before the gate reached its branch, and W1-D's two source tests
    met it at the evening's merge. It now imports `motion.js` (its one import) and asks `reducedMotion()` — the
    person's setting or the preview's `html.rm` —, animates through `play()` and waits on a frame through
    `nextFrame()` and `afterPaint()`. Nothing of the movement changes: the discovery's 36 animations (29 on a phone),
    the hand's 13, the replay's 39 are identical call for call — target, keyframes, options —, in the same two frames
    on one start time, 3 582 ms from the class flip to the settled still before and after at 1440 × 900 (`gate-1`).
    What changes is the preview's reduced-motion flag: the discovery played under it, over zeroed tokens; the hero
    rests on its still there now.

**Source.** The owner's V5.5 directive (5 October 2026, 14:32); plan §1.1 (French spacing), §1.3, §1.4 (SP-1 … SP-8,
RH-1 … RH-8, SH-2), §1.5 (the motion gate), §1.7 (the icon system; Q8), §1.16, §1.18 D24, §2.1, §2.3 (the deletion
map), §3.4 items 4 and 6;
DL54-12, DL54-14, DL54-26, DL54-32 … DL54-34 (W1-B), DL54-38 (W1-D), DL54-39, DL54-40; `RED_TEAM.md` m1;
`ICON_SEMANTIC_MAP.md` §1 (`ile-steps`: «the section-header micro-mark»); `DESIGN_SYSTEM_V5.md` §11 (PX02, PX04, PX05, PX08, PX13, PX17, PX18); `council/UX_PUBLIC.md` §2.1, §2.3, §2.4
(D2 … D5), §3.4, §3.8; `UIUX_PRO_MAX_AUDITS_public.md` §2 (HO-1 … HO-10); `QA/hero-final/ux_s2r2.md` (UX-1);
`docs/REQUIREMENTS_MATRIX.md` R-ARC-006, R-P3-013; the measures in `QA/v54/w2-d/NOTES.md` §8 and
`C:/tmp/ile_v5_council/evidence/v54/w2-d/` (page-2-before, page-3 … page-9, page-7-tablets, interim-2 … interim-4, states-2,
states-3, sample-news-1, fc-2, banner-1; after the merge: page-10 … page-15, page-14-tablets, interim-5, states-4,
states-5, fc-3, rm-1, sample-news-2, others-1, gate-1).

## DL54-42 · 9 October 2026 · W2-D, the senior review's fix pass: the hero on the page's column, a finger's press that waits

**Decisions** (the family's, under V5.5 — implement, review once, fix, ship; each on a finding of the senior review or of
the accessibility + performance check of 9 October 2026 — `QA/v54/w2-d/REVIEW.md` M1 … M4, m1 … m6, `A11Y_PERF.md`
F1 … F10 — re-measured on the lane after the fix: `QA/v54/w2-d/NOTES.md` «Review fixes». Every number is the
implementer's own measurement, headless Chromium, the lane's server.)

1. **From 96 rem the wall stands on the page's column** (M1; amends DL54-40 item 5, which stands below 96 rem). Up to
   1535 px the wall needs the page: at 1440 × 900 its four columns are 195.8 px with the wall at the page's pad, and
   Institutions takes five lines from 195 px. From 1536 px four such columns fit between the container's content edge
   and the niche, so the wall starts THERE — where the letterhead's logo, the navigation's panels and every chapter
   start — and the niche keeps the far edge of the window. Measured, fr (ar mirrored at 1536 and 1920): the logo, the
   promise, the first plate, MAROC, the description and the first chapter's title start on one x — 148 px at
   1536 × 864, 120 at 1600 × 900, 160 at 1680 × 1050, 280 at 1920 × 1080 and × 940, 600 at 2560 × 1440, 1 040 at
   3440 × 1440 (the promise stood 32 px from the window at each of them up to 1920, and 422 at 2560). Columns 192.8 px at
   1536 × 864, 210 at 1600 × 900, 200 at 1680 × 1050, 221.2 at 1920 × 940, 214.7 at 1920 × 1080, 237.6 at
   2560 × 1440; sentences 4 · 5 · 5 · 3 lines — 1440 × 900's own count — everywhere but 2560 (3 · 4 · 4 · 3). Below
   96 rem nothing moves: 1440 × 900, 1366 × 768 and 1280 × 800 are as the review saw them, to the tenth of a pixel.
   - **The niche gives way to the wall, never the wall to the niche.** `--niche-max` is `min(44vw, 100vw − the edge −
     the wall's end − four columns of --col-min and their gutters)`: `--col-min` 11.75 rem where the sentences are
     14 px, 12.5 rem where they are 15 px (five lines of Institutions at 15 px need 195 px; the edge is read in `vw` and
     the grid in `%`, so a classic scrollbar takes 2 px of a column: the minimum keeps that margin). A tall, narrow
     window therefore draws a smaller door with more night above it: at 1536 × 960 the stage is 556 px for 587 px by
     the height alone (columns 188 px); at 1680 × 1050 640 for 659. At 1536 × 864 the door is the one the review saw
     (522 px). The sentences are 14 px at 1536–1599 px, where the container is still 1 320 px, and in every window at
     most 864 px tall; 15 px elsewhere.
   - **The columns are never wider than the largest plate** (15 rem: the 480 px cuts at density 2, C2). On a screen
     wider than that the night takes the leftover and the door stays centred in it (3440 × 1440: columns 240 px, the
     niche 1 352 px).
   - **The door's `sizes`** follow (DL54-40 item 14): one line for the cap between 1536 and 1599 px in a window at
     least 952 px tall (told 484 px for 483.5 drawn at 1536 × 960 and × 1050, where the height's lines told 516 and
     580); from 1600 px the same cap can draw the door up to 9 % narrower than the height's line tells (1728 × 1117:
     told 627, drawn 577) — told more, never less, and the same file taken.
2. **The plate is as wide as its column and as tall as the height leaves** (M1: «plates as wide as their columns»).
   From 96 rem a plate's width is its column's and its height is what the hero leaves under the path for a five-line
   column, its call and `--row-air` of wall (2 rem; 1.25 rem in a window at most 800 px tall), between 3 : 2 and 4 : 5
   of its width — one expression (`--plate-fit`), no tier by height: 192.8 × 189.5 px at 1536 × 864, 192.8 × 155.3
   at 1536 × 730, 210 × 192.5 at 1600 × 900, 200 × 250 (4 : 5) at 1680 × 1050, 221.2 × 217 at 1920 × 940,
   214.7 × 268.4 (4 : 5) at 1920 × 1080, 237.6 × 297 at 2560 × 1440. The row therefore fits by construction — at
   1920 × 940 the five-line columns under the 208 × 260 plate of the old tier would have passed the hero's height by
   about 19 px (computed from the sheet's values, not captured). Its file is the 4 : 5 cut (the 3 : 2 one in a window at most 736 px tall), **covered** by the box: a crop of
   an approved cut, never more of the photograph than the cut shows (O54); `object-position` holds each photograph on
   its subject. The 1 : 1 cut is no longer drawn from 96 rem. **For the imagery pass:** cuts at the ratios the box
   really takes (≈ 1 : 1 at 1536 × 864 and 1920 × 940, 5 : 4 at 1536 × 730) would replace the cover.
3. **On the desktop the description stands on the page's column, and the niche on the composition's bottom edge**
   (M1; DL54-39 item 1's forward correction). The paragraph starts where the chapters under it start — the page's pad
   below 75 rem, the container's content edge from there: 92 px at 1280, 135 at 1366, 100 at 1440, 148 at 1536, 280
   at 1920, the logo's x at each — on the page's paper. It **stays inside the hero's section** (the data contract and
   `test_home.py` are unchanged: the retarget the review expected was not needed) and is placed by the hero's own grid,
   on a line `body-start`: a French paragraph on the Arabic page is `direction: ltr`, and paddings in its own direction
   put it at the wrong edge (found by measuring the Arabic page). The wall's light and the grain are the
   composition's (`.he-ground`, which spans its tracks), not the description's row; the niche clips its own shadows —
   the «grey shadow» under it was the door photograph's drop shadow falling a hundred pixels onto that row.
4. **A finger's press waits** (M2; F3). On an origin, a touch or a pen arms the press state and the light 100 ms after
   it lands, or at once when it lifts sooner; `pointercancel` drops them where they stand; a tap keeps them 700 ms
   after the lift, while the next page answers. The mouse and the keyboard are as they were. Measured on the page's
   clock (touch synthesised through the DevTools protocol, not a real phone), Phase 3 and interim: a flick that starts
   on a tile — `pointercancel` 19–33 ms after `pointerdown` when the finger moves at once, 49–66 ms after a 40 ms
   rest — changes no class at all (the reviewed script set `is-pressed` and `is-flowing` until the cancel: REVIEW M2);
   a finger that rests 140 ms before it scrolls still shows them for 53–64 ms (the press was armed: the browser's own
   `:active` does the same); a tap of 60 ms shows its press and its light from the lift, and the page it opens
   follows. The handler reads before it writes (`flow()`, then the class): at CPU × 4 on the dev server a tap's
   slowest event is 104 ms (96–120, n = 7) for 112 ms (88–160) with the reviewed script, and `pointerdown` itself is
   under the 16 ms the API reports in 7 of 7 (it was 64–88 ms).
5. **The interim variant's phone band has no rail** (M3; gate G3 closed — what the site shows today). No station may be
   drawn, so no rail: the door stands in the middle of the band, on the spine's axis — the spine rises from the four
   tiles into its threshold —, on a floor line from pad to pad; the band's light and the doorway's halo are centred
   with it; the first movement is the spine, the steps, the key and the door (1.94 s; 2.75 s with the rail). The lead
   is not drawn below 64 rem (the eyebrow has said it, the description says it one swipe lower). On phones the door is
   sized by the window's height (`100svh` less what the letterhead, the statement and the tiles take), never above
   Phase 3's width at that height: 4 / 4 tiles in the first screen at 360 × 640 (the lowest at 619 px; 0 / 4 before),
   390 × 664 (647; 2 / 4), 375 × 667 (648; 2 / 4), 360 × 701 and × 720, 360 × 800 (731; 2 / 4), 390 × 844 (fr and
   ar), 412 × 915. On the desktop the lead is read at the reading size (17 / 28, one line from 1280 px: it was 15 px on
   two), which makes the statement 12 px shorter: at 1440 × 900 the composition is the hero's height again (755 px
   for 767) and the description's first line is whole at the fold; and without a stations' row the statement's row
   carries the path's whole height, so the door stands on its floor in a tall window too (16 px at 1920 × 1080,
   where it hung 54 px above it).
6. **Where nothing hovers, the key shows it is live and the light comes back by itself** (M4). Under `(hover: none)`
   the key's halo rests at .45 on the settled hero of a page that moves — the hero's own layer, the sign a mouse gets
   under the hand at .6 —, and the hand's short light (the flow of DL54-39 item 4: ≈ 1.4 s on a phone, the key does
   not turn) runs once each time the hero comes back into view after having left it (the niche out of sight, then
   60 % of it in sight). Never under reduced motion or forced colours, never with a mouse; the whole sequence stays
   on the key. In the desktop layout such a screen also draws the four calls at rest (F8).
7. **The minors.** No light of its own on the door's station on the desktop (m1: sized as a node's glint, it stood on
   nothing 90 px before the inscription; the discovery is 35 animations for 36, the hand's flow 12 for 13). The last
   word's line may run into the 16 px before the reveal, so «Universités & Formation» keeps its arrow on its own
   line and the four sentences share one at 1440 × 900 and 1536; at 1280–1312 px the words are 15 px over their
   14 px sentences, which gives the same at 1280 × 800 (m2; a hanging arrow out of flow was tried and left: it could
   stand on the stone). On the Arabic page an arrow in a left-to-right run points the way the run reads — the hero's
   calls, the register's, and a pathway's row, which is laid left to right as a whole when its title stands in French
   (m3). MAROC at 700, in the labels' ink (m5: the path's bronze is under 7 : 1 at 13 px). A pathway's arrow rests at
   .6 where a hand hovers (F5); the register's call may take two lines (F6: text-only 200 % no longer pushes the
   phone page past its edge — 0 px at 390 for 66; the 21 px left at 360 are the footer's). The stations' row has its
   height before its list is parsed (F9, Phase 3 only). The name in the `h1` is marked `lang="en"` on every page, as
   the header's lock-up marks it (F10).
8. **The home draws its news chapter once an article is live** (m4; supersedes DL54-41 item 7's «while nothing is
   published the chapter says so in one row» on the home). With gate G3 open the home announced an empty chapter
   between the warning and the promoter. `pages.services.build_news` hands the chapter over only with an article, in
   either gate state (it already did so with the gate closed). The news' own page keeps its empty state, and DL54-33's
   composition — the news' glyph in its disc — is read there by the icon family's browser test
   (`tests/frontend/test_browser_w1_b.py`, one assertion moved from the home to `/fr/actualites/`). The partial keeps
   its empty row and the sheet its rules: the revert is the builder's condition.
9. **The home's page-type CSS ceiling is the merge step's to record** (F1; plan §2.6 item 5 lets the CD raise a
   ceiling by 2 KB only, and `tests/frontend/test_css_budget.py` of §2.7 does not exist). The measurement after this
   pass, gzip of the built sheets: `main.css` 43 169 B, `pages.css` 4 083 B, `hero.css` 10 571 B (F4: 14 KB) —
   57 823 B in all, 719 B more than the reviewed state (57 104 B; 57 180 B on the wire in the check's twin, 9 874 B
   over §2.6's ceiling of baseline + 8 KB). Each sheet is inside its own budget; the excess is the hero's sheet, which
   §1.17 makes a page entry. The hero's script chunk is 7 119 B gzip (F4: 7 KB = 7 168 B), with the gate's
   `durationToken()` instead of a local twin.
10. **Not done.** F4 — the niche-sized layers while the movement plays (no dropped frame, no long task: not needed to
    ship). F7 — on phones the replay button takes the focus after the four tiles although it stands above them:
    accepted and stated in `docs/ACCESSIBILITY.md` §3 (meaning and operation are kept; `reading-flow` later). m6 — no
    picture under the hero: the imagery pass, under O54 / O55. Not this family's: F2 (`collectstatic` under the
    production storage, W1-D's console entry), the navigation's photographs before `load`, its box shifting while the
    header is parsed and its drawer's opening time (W2-C1), a `.btn`'s focus ring on the night (W1-C), the footer's
    21 px under a text-only enlargement.

**Source.** The owner's V5.5 directive; `QA/v54/w2-d/REVIEW.md` and `A11Y_PERF.md` (9 October 2026); plan §1.17, §2.2,
§2.6; DL54-11, DL54-12, DL54-33, DL54-39, DL54-40, DL54-41; the measures in `QA/v54/w2-d/NOTES.md` «Review fixes» and
`C:/tmp/ile_v5_council/evidence/v54/w2-d/` (fix-0-before, fix-0-before-interim, fix-final, fix-final-interim,
fix-final-forced, fix-final-rm, fix-6-odd, fix-door-1, fix-door-2, fix-tap-timing, fix-m3-before, fix-m3-after,
fix-hover-1).

---

## DL54-43 · 10 October 2026 · W2-D, the fix pass: the wall's smallest column under a classic scrollbar

**Decisions** (the family's, in the same fix pass as DL54-42, before its merge; **supersedes two figures of DL54-42
item 1** — `--col-min` where the sentences are 14 px, and the line of the door's `sizes` — and nothing else of it. Every
number is the implementer's own measurement on the lane; «with a scrollbar» is headless Chromium started without its
`--hide-scrollbars` default, which draws the classic 15 px bar a desktop on Windows draws.)

1. **The smallest column of the wall's cap is 12 rem where the sentences are 14 px** (it was 11.75 rem; 12.5 rem where
   they are 15 px stands). «Universités & Formation →» measures 203.5 px with its arrow, and its line may run into the
   16 px before the reveal (DL54-42 item 7): it needs 187.5 px of column. The cap is read in `vw` and the hero's grid
   in `%` — a custom property that sizes the stage cannot be a percentage —, so under a scrollbar each column is
   narrower than the cap intends: 1.9 px under a 15 px bar, 2.1 px under a 17 px one. With 11.75 rem the capped columns
   were 188 px without a scrollbar — 0.5 px to spare — and 186.1 px with one: at 1536 × 960 the fourth word took two
   lines again and its sentence started 24 px under the other three (the review's m2, reproduced with the bar drawn).
   With 12 rem they are 192 px, and 190.1 px under the 15 px bar: the four words on one line and 4 · 5 · 5 · 3 lines at
   1536 × 960, 1536 × 1050 and 1599 × 1000, fr and ar at 1536 × 960, with and without the bar.
   - **What it costs.** Where the cap binds — between 1536 and 1599 px, in a tall window: at 1536 px from about 890 px
     of height (the door is the height's at 1536 × 880, the cap's at 1536 × 895) — the niche is 16 px narrower: at
     1536 × 960 the stage is 540 px (556 with 11.75 rem; 587 by the height alone), the plates 192 × 198.9 px. Nothing else moves: 1536 × 864 and × 730, and every cell from 1600 px, are to the tenth of a
     pixel what DL54-42 records.
2. **The door's `sizes` follow** (supersedes DL54-42 item 1's third sub-point): between 1536 and 1599 px, in a window
   at least 896 px tall, `calc(43.5vw - 198px)` — told 470 px for 469.6 drawn at 1536 × 896, × 960 and × 1050, 497 for
   497.0 at 1599 × 1000. At 1599 px the cap binds from about 933 px of height only (497 for 495.4 at 1599 × 931):
   between the two the line tells up to 5.5 % more (1599 × 896: 497 for 470.9 — the same 576 px file). Told more,
   never less; from 1600 px as DL54-42 says.
3. **Seen with the scrollbar drawn, and left as it is.**
   - From 96 rem the hero stays on the page's column: the logo, the promise, the first plate, MAROC, the description
     and the first chapter's title share one x under the bar too — 140.5 px at 1536, 112.5 at 1600, 152.5 at 1680,
     272.5 at 1920, 592.5 at 2560 (fr; ar at 1536 and 1920) —, the sentences keep 4 · 5 · 5 · 3 lines (198.1 px columns
     at 1680 × 1050, where the cap's 12.5 rem binds).
   - Below 96 rem the wall is the one the review accepted, measured without a bar. With one, at 1440 × 900 the columns
     are 192.1 px and Institutions takes six lines for five (it needs 195 px at 15 px): the composition is 13.5 px
     taller, the four links still whole in the first screen (the lowest at 857.5 of 900), the description's first
     line under the fold; at 1280 × 720 Personnes takes five lines for four, in the same row. Not changed here: the
     lever is the sentences' size at 1440, which is the reviewed design.
   - At 1024 × 768 the letterhead's four doors wrap onto a second row under the bar (the header is 64 px taller; the
     hero under it holds, its fourth row ending on the fold): the bar is W2-C1's — for the steward.

**Why.** The review's measurements, the family's and the browser tests are taken in headless Chromium, which draws no
scrollbar; a desktop on Windows draws one, and the hero's new cap was the one place of this pass where 2 px decided a
line. The browser test now holds the 192 px minimum at 1536 × 960 (`apps/pages/tests/test_browser.py`).

**Source.** DL54-42 items 1 and 7; `QA/v54/w2-d/REVIEW.md` m2; the measures in `QA/v54/w2-d/NOTES.md` «Review fixes»
and `C:/tmp/ile_v5_council/evidence/v54/w2-d/` (fix-final/scrollbar.json and its captures, fix-6-odd, fix-door-3).

## DL54-44 · 10 October 2026 · Steward, the w2-d merge: the home's chapters assigned to w2-d, the merge before W2-B, the home's CSS ceiling as measured

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w2-d` into design-v5 on 10 October 2026 —
what the family's own entries hand to the merge step: DL54-41, DL54-42 item 9; `QA/v54/w2-d/NOTES.md` §7.8, §8.8, §9.6).

1. **The home's chapters are this area's in the manifest.** The owner's V5.5 directive made «the final hero in the real
   home page and the home made coherent around it» one area, so the chapters plan §3.4 item 6 gave W2-E were built on
   `v54-w2-d`. The thirty paths `scripts/check_ownership.py w2-d design-v5` listed as outside the slice were read in the
   diff, found to be what the notes declare, and written under w2-d in `OWNERSHIP_V54.json` (`25c981a`) — slices wherever
   another family holds the file: the nine chapter partials, the chapter head and the register of the four entrances
   (only the home includes either), the two deleted partials, the home's part of `pages.css` (the interior part byte
   for byte but for three removals of home-only rules), `_say_once()` and `build_news()`'s condition, the locked-key map
   of two sections, the French-spacing filter, `v2/routes.css` and `v2/voyage.css` deleted with their last consumer, one
   interface string in the four catalogues, one row of `docs/ACCESSIBILITY.md` §3, one assertion of W1-B's browser test.
   The check after it: 25 inside, 122 slice, 16 generated — PASS (before: 30 outside). W2-E stays in the manifest as the
   plan's family, with no branch; its A-bis blind test is superseded by V5.5 and was not run (DL54-41).
2. **The area merged before W2-B**, which plan §3.4 item 4 and the manifest's `merges_after` put first. The reason for
   that order was `static/css/v5/_door.css` (W2-B creates it; plan §1.17 has `hero.css` import it). The file is not on
   design-v5, and the port did not wait for it: the stage's rules stand in `hero.css`, scoped to `.he`, and
   `static/css/v4/hero.css` is shrunk to the entrance's door, not deleted (DL54-39 item 3). The two areas are
   independent as built, and V5.5 runs independent areas in parallel. What is left for the merge that brings
   `_door.css`: `hero.css` imports it and drops its copy — a forward correction —, and `v4/hero.css` leaves `main.css`
   with its last consumer.
3. **The home's page-type CSS ceiling is recorded as measured.** On the bundles rebuilt from a clean dist at the merge,
   gzip −9: `dist/main.css` 43 169 B, `dist/pages/css/pages.css` 4 083 B, `dist/pages/css/hero.css` 10 568 B — **57 820 B
   in three render-blocking sheets**. Plan §2.6's Wave-1 ceiling for the home is 47 306 B (the W1-0 baseline, 39 114 B,
   + 8 KB): **the home is 10 514 B over it.** Only the page sheets grew: `main.css` is 764 B lighter than at `v54/w1-d`
   (43 933 B: `v2/routes.css`, `v2/voyage.css` and the V4 hero's rules left it, the hero's token block entered it),
   `pages.css` is 1 263 B heavier (2 820 B: the chapters on the V5 tokens), and `hero.css` is new — a page entry by plan
   §1.17, never in `main.css`.
   - **§2.6 item 5 was not applied to this merge, and that is said here rather than passed over.** Its letter is «a
     family over its ceiling does not merge», with one raise of at most 2 KB by the Creative Director after a
     measurement on 8782. The owner's V5.5 directive overrides the V5.4 process where the two conflict, and its
     performance rule is «fix only real regressions, serious blocks, important long tasks, evident LCP/CLS problems. If
     performance is good and does not block UX: ship». The area's one accessibility + performance check
     (`QA/v54/w2-d/A11Y_PERF.md`, F1) measured the effect of the heavier CSS in production shape — the lane's compressed
     twin, profile A (150 ms RTT, 1.6 / 0.75 Mbps), CPU × 4, n = 9 cold loads per cell, against the W1-0 before set —
     and found none to the worse: LCP 1 600–1 728 ms for 2 064–2 356 ms (464–628 ms earlier), the longest load task
     124–154 ms for 710–938 ms, CLS ≤ 0.038; it asked for this record, not for code. The Creative Director raised
     nothing; no measurement was made on 8782, which cannot be rebuilt today (item 4).
   - **What holds from here.** The home's page-type ceiling is `main.css`'s ceiling plus the home's two page sheets as
     they weigh at this merge: 44 486 B + 14 651 B = **59 137 B**; the home stands 1 317 B under it. `main.css` keeps on
     the home the ceiling it has on every page type — 44 486 B while Wave 1 is open (W1-C has not merged: the «measured
     total at the end of Wave 1» that §2.6 item 3 ratchets from does not exist yet), never above 45 KB — and the home's
     ceiling follows it, with the same 14 651 B, when Wave 1 closes. It does not rise otherwise: a merge that would land
     over it comes back to this log first. The other page types' Wave-1 ceilings stand (interior 44 486 B, login
     45 694 B, dashboard 49 860 B) and nothing is lowered while Wave 1 is open; this merge leaves each of them 764 B
     more room (interior 43 169 B, login 44 377 B, dashboard 48 792 B). The per-sheet budgets DL54-42 item 9 names are
     met and stand: `hero.css` 10 568 B of 14 KB, the hero's script chunk 7 119 B of 7 KB (7 168 B). Nothing pins any of
     these figures: `tests/frontend/test_css_budget.py` (plan §2.7) does not exist.
4. **Seen at the merge, not this area's, and open on design-v5** (`A11Y_PERF.md` F2, run again at the merge with the
   check's twin settings into a scratch root): `collectstatic` fails under the production storage with
   `SuspiciousFileOperation` — `apps/portal/static/portal/console.css` imports `v5/_loader-light.css` by a path that
   leaves `STATIC_ROOT` (W1-D's console entry). No 8782 window and no deployment is possible until it is corrected;
   nothing of it was touched here.

**Why.** A ceiling that is exceeded and not written down is a ceiling nobody holds. The plan's own remedy does not
reach this case — 2 KB, on a measurement that cannot be made today — and the directive that lets the area ship asks
that only real regressions stop it: the record says which rule gave way, on what evidence, and what number the next
merge is held to.

**Source.** The owner's V5.5 directive (5 October 2026, 14:32: «PERFORMANCE», «SHIP THE PRODUCT»); plan §1.17, §2.2
(the manifest: the steward assigns), §2.6 items 2, 3 and 5, §3.4 items 4 and 6; DL54-39 item 3, DL54-41, DL54-42
item 9; `QA/v54/w2-d/A11Y_PERF.md` F1, F2 and §3; `QA/v54/w1-d/SHIPPED.md` «Bytes» (the ceilings and the weights at
`v54/w1-d`); the weights measured on `v54-w2-d` at `343236a`, after `npm run build` from a clean `static/js/dist`.

## DL54-45 · 9 October 2026 · W1-C: the field's focus rule is drawn by the field, with transform; the plate stays light

**Decision.** «La lastra» (`static/css/v5/field.css`):
- **The 2 px rule of §1.6** is the `::after` of `.form-field`, not a background of the control: the field is a
  column (`display: flex; flex-direction: column`), the help and the errors take `order: 2`, the rule takes
  `order: 1` and a `-2px` margin, so it lies on the control's foot whatever the template that wrote the field. It
  draws with `transform: scaleX(0 → 1)` from the reading edge (`transform-origin` has its `[dir="rtl"]` twin) in
  `--field-draw`, which is `--motion-standard` and becomes `0ms` under `html[data-input="key"]` — the
  input-modality flag of `static/js/head.js` (W1-D): until that merge every focus draws in 200 ms, afterwards a
  keyboard focus draws nothing (tier 0). Under reduced motion the token is 0 ms.
- **Specificity is the contract.** The plate is `.form-field :where(…)` — (0,1,0) — and a control no component
  has drawn takes a zero-specificity base (`:where(input:not(…), select, textarea)`: height, inset, hairline,
  corner, paper). Every component that draws its own control keeps it: the wizard's fields, the documents'
  search, the console's table select. A stray `<select>` keeps its native arrow: the drawn chevron and
  `appearance: none` go together, on `.form-field select` only.
- **52 px on public pages** is `body:not(.console) { --field-h: var(--control-lg); }`: a context re-points the
  component token, no template changes (plan §1.8). The inline inset follows the height —
  `(--field-h − 20 px) / 2`: 12 px at 44, 16 px at 52.
- **An error is three things beside the colour:** the edge doubles (1 → 2 px, a static inset), each message carries
  a mark drawn in its own ink (a ring, its stroke, its point: two gradients and a border — nothing a screen reader
  hears), and the words. The V4 left bar and the indent of `.form-field--error`, and the tinted box of the consent
  row, are gone: a form keeps one left edge.
- **A group is not a box:** `fieldset.form__group` (the class the templates write; V1 styled `.form__fieldset`
  only, so the browser's own grooved frame showed) has no border; two groups stand 64 px apart (48 on phones),
  2.6 × the 24 px between two fields (SP-2).

**Why.** A background-size transition would have drawn the same rule with four declarations, on every producer,
without a column — and animated a property that is neither `transform` nor `opacity` (plan §1.5, «Properties»).
The column costs `display: flex` on `.form-field`; on the 316 cells of the sweep no page overflows and no
focus indicator is missing (QA/v54/w1-c/NOTES.md). The W1-A review asked for the two folds this entry makes
(m-1: fields at 4 px; m-9: the halo reaches the fields).

**Source.** Plan §1.4 (SP-2, SP-3, SH-9), §1.5, §1.6, §1.8, §1.13; DS V5 §10.3; `static/css/v5/field.css`;
`tests/frontend/test_components_w1_c.py`, `tests/frontend/test_browser_w1_c.py`; QA/v54/w1-c/NOTES.md.

## DL54-46 · 9 October 2026 · W1-C: checkbox, radio and switch are the native controls, drawn at 24 px

**Decision.** `input[type="checkbox"]` and `input[type="radio"]` are drawn on the element itself
(`appearance: none`, at zero specificity): a **24 px** box — DS V5 §10.3 drew 20 — with the structural hairline,
4 px corners (a radio is round), the primary's fill when checked, and the person's own mark as its `::before`
(a `clip-path` check in the label ink; a dot for the radio) scaling in over 120 ms. Under a coarse pointer an
`::after` extends the hit area to 44 px. A switch is the same checkbox with `role="switch"`: a 44 × 24 track, the
thumb at the inline end when on (its travel has its RTL twin). In forced colours the system's own controls come
back (`appearance: auto`).

**Why.** 24 px is the floor of every target (SP-8) and the size the product already had (the consent checkbox had
been raised from 20 to 24 for WCAG 2.5.8); a 20 px box would have put every checkbox and radio back under it. No
markup changes: every producer of a checkbox (Django's widgets, the newsletter, the selection workspace, the
orientation wizard) gets the same drawing, and a component that hides its input (the option card) is untouched.
The check is the person's own act — never a status (O14).

**Source.** Plan §1.4 (SP-8), §1.8; DS V5 §10.3; `static/css/v5/field.css` §6.

## DL54-47 · 9 October 2026 · W1-C: a notice says its kind three times without colour

**Decision.** `static/css/v5/notice.css`: the register's wash, a 3 px rule at the reading edge, the mark, the title
in the register's word colour, the body in ink — and the **style of the rule** as the third non-colour channel,
in the vocabulary the chips already use: **solid** for a fact (information on the slate wash, «en examen» in
lapis, a done thing in ink), **dashed** for a warning (the broken edge of «attesa», amber at step 600), **double**
for an error (the two lines of «rifiuto», garnet). `notice--success` and `alert--success` are the conforme tone —
paper and ink, never green: no colour ever means «approved» (O14). `notice--warn`, which two console templates
write and no sheet defined (it fell back to the information colours), is the warning. The institutional notice
keeps a hairline frame, the navy mark and a gold rule. No shadow, corners on the two outer ends only, 15/24.
The component's three properties are `--notice-wash`, `--notice-word`, `--notice-rule` — not `--notice-bg` /
`-fg` / `-border`, which are names of the legacy shim.

**Why.** Every notice has words; a session message (`.alert`) has nothing else — no mark, no title — so the rule's
style is what tells a warning from an error when the colours are gone (forced colours keep it).

**Source.** Plan §1.2 (the registers, O14, O57), §1.4 (SH-2); DS V5 §10.8; `static/css/v5/notice.css`.

## DL54-48 · 9 October 2026 · W1-C: tabs keep one indicator and no memory; the disclosure draws its own mark

**Decision.**
- **One indicator** (MS-O3): `.tabs__list::after`, a 1 px box moved under the selected label with
  `transform: translate() scaleX()`. `initTabs` measures the label in physical pixels from the list's top left
  corner — the same measure in both directions — and writes `--tabs-x / -y / -w / -dir` on the widget; the sheet
  does the rest (`--spring-snappy` on public pages, `--ease-layout` in the console). It travels for a pointer's
  choice only (`event.detail > 0` sets `.is-travelling`): from the keyboard, at load, from a link and on a resize
  it is where it is (tier 0). The arriving panel comes 12 px from the side the indicator travelled from
  (`@starting-style`, the same 200 ms); nothing under reduced motion. Until the script has measured, the selected
  tab draws its own line in place.
- **No bold sizer:** the selected tab keeps the control weight (500) and takes the ink; the indicator is the
  non-colour mark. A weight change needed a hidden twin of every label to hold the width (CDV §15).
- **Nothing is remembered:** the `remember` option, which wrote the choice to `localStorage` and never read it
  (G-21), is removed from the template and the script — `main.js` no longer uses `localStorage` (plan §1.15).
- **Keys:** ← / → (reversed when the list reads right to left), Home, End, never with Alt / Ctrl / Meta (Alt + ← is
  the browser's «back»); automatic activation; Tab enters the panel.
- **The disclosure** (`.accordion`): the mark is a chevron drawn on every `summary`, turning when open — the FAQ's
  rows had none, the component's had a plus that turned into a cross; the inline glyph of
  `components/accordion.html` is hidden rather than removed (the template is not in this family's slice).
  `.accordion__panel`, the name the FAQ's markup gives the answer, is the same box as `.accordion__body` (G-19
  closed). A link to a row (`/faq/#key`, «Lien direct vers cette question») opens it: `initAccordions`.

**Source.** Plan §1.5 (MS-O3, tiers, «Properties»), §1.15; CDV §15; `static/css/v5/tabs.css`;
`static/js/main.js` (`initTabs`, `initAccordions`); DS 2026 §10 (`tabs.html`, `accordion.html`), §16, §21;
`docs/ACCESSIBILITY.md` §13 (G-19, G-21).

## DL54-49 · 9 October 2026 · W1-C: buttons — one press, no shadow, and the busy face left to the loader

**Decision.** `static/css/v5/buttons.css` replaces `components.css` §1, `v3/buttons.css` and the material of
`v4/buttons.css`, and keeps the V3 property API (`--btn-fill`, `--btn-ink`, `--btn-edge`, their `-hover` and
`-press` states, `--btn-box-h`, `--btn-pad`, `--btn-pad-end`).
- **Flat means no shadow either.** DS V5 §10.1 gave the primary `--shadow-1`; SH-9, the shadow budget (SH-8) and
  the login's L14 («no `box-shadow`, no inset, no gradient») read together leave none: the only `box-shadow` in the
  sheet is `none`.
- **One press gesture:** the press fill and `translate: 0 1px` at 0 ms, released on `--spring-snappy`; a link
  button does not travel; under reduced motion colour only. Hover sits behind `(hover: hover)`, the arrow's lean
  behind `(hover: hover) and (pointer: fine)`.
- **The ghost is the quiet action in the accent** (DS V5): V3's grey label read as text.
- **`text-wrap-style: balance`, not `text-wrap`:** the shorthand resets `text-wrap-mode`, and a button inside a
  cell that says `white-space: nowrap` wrapped (the company dashboard's «Ouvrir le besoin», found by the style
  probe).
- **`.btn--lg` keeps the 15/20 label** of every button (V4 set 17 px): the public scale has eight sizes and 16 px
  is not one of them; the entrance sets its own CTA.
- **Disabled** by colour and by cursor, never by opacity, and never while busy
  (`:where(:not(.is-busy))`).
- **The busy face is not drawn here: it is the loader's, and V4's is gone.** While this family was alone on
  its branch V4's three-notch meter stayed as the only block of `v4/buttons.css` — it was the only busy face
  there was. W1-D's notes hand the block to this family («with `v5/buttons.css`: drop the override, delete the
  dead keyframes»: it repainted every waiting button as the primary), and the loader reached design-v5 the
  same day. In the commit after that merge: the file, its import, the RTL guard's one known entry, DS 2026's
  row and its two sentences on `btn-busy` are gone; `KEYLESS` in `static/js/src/shell.js` names the three
  padless variants the sheets draw (`.btn--link`, `.btn--text`, `.btn--icon` — V3's `--tertiary` and
  `--inline` have no producer and are not drawn; `test_loader_rules.py` reads the list off the sheets); and
  the loader's browser test reads the V5 link, which underlines with `text-decoration` and has no `::after`.
  A waiting button now keeps its own variant's surface and ink, with the key at 80 % of that ink in the end
  padding (measured: 7.2 px from the last glyph, 5.2 px in a small button, 9.2 px in a large one, 5.2 px from
  an arrow's box). Not done: the busy face of an icon-only button (DS V5 §10.1, «the key replaces the
  glyph») — no template draws a `.btn--icon` today, so `KEYLESS` keeps it waiting without a key.
- **The padding is V3's expression, whole** — `padding-inline: var(--btn-pad, …) var(--btn-pad-end,
  var(--btn-pad, …))`; `.btn--arrow` shortens the end by 4 px (the glyph's optical margin, never a negative
  margin on the glyph); a padless variant writes `--btn-pad: 0`. A trial merge with the loader family's branch
  found why it matters: its busy key is centred in that end padding and its tests pin the expression and read
  the padless variants off the sheets (`tests/frontend/test_loader_rules.py`). The first slab of this family
  had `padding: 4px var(--btn-pad)`: two of that family's tests failed on the merged tree and the key stood
  2 px closer to an arrow. No box moved when the expression came back (320 cells, before and after).
- **`--btn-lighting` is not read.** It is V4's name and only V4's busy block wrote it; that block now paints
  its own `background-image`, the slab says `background-image: none`, and deleting the block leaves no
  reference to a property declared nowhere (`tests/frontend/test_css_tokens_exist.py` would have failed).
- **`--hit-min`** is no longer read by a button (`--hit-primary` is); nine readers remain in other families'
  sheets (`v4/shell.css`, `v4/workspace.css` × 2, `console.css` × 4, `dev/designpreview.css` × 2), so the alias in
  `v5/aliases.css` stays until they move.
- **A wrapped Latin label stays centred on an Arabic page.** `base.css` isolates a French, Italian or English
  span left to right on an Arabic page and aligns it to its own start — right for a paragraph, wrong for the
  label of a centred slab: «MANIFESTEZ VOTRE INTÉRÊT POUR LE PROJET» hung on the left of the company form's
  button at 390 px (it did before this family too). One rule in the sheet,
  `[dir="rtl"] .btn:not(.btn--link, .btn--text) > :is([lang="fr"], [lang="it"], [lang="en"])`, re-centres it; a
  link-style button keeps its start.

**Source.** Plan §1.4 (SH-8, SH-9), §1.5, §1.8, §1.9, §1.13 (L14), §3.3 item 7; DL54-13; DS V5 §10.1;
`static/css/v5/buttons.css`; `tests/frontend/test_components_w1_c.py`.

## DL54-50 · 9 October 2026 · W1-C: the entrance draws no field of its own; the paths outside the slice

**Decision.** Four paths outside W1-C's slice of `docs/design-v5/OWNERSHIP_V54.json` were written, for the merge
step to record:
1. `apps/accounts/static/accounts/entrance.css` (W2-B's) — the V4 input of the entrance pages (44 px, radius
   `md`, its own ring, the password's padding) is deleted, 37 lines: at (0,5,1) it overrode «la lastra» and left
   the login with fields at 6 px beside a button at 4 px, without the halo. The login's fields are now the
   system's — 52 px, 4 px corners, the one ring, the halo and the rule — as plan §1.8 and §1.13 decide; the rest
   of the sheet (the stage, the sheet, the 52 px action) is untouched and stays W2-B's to redraw.
2. `static/css/v4/shell.css` — the three-selector rule that set the notice in the interface face: that file's own
   header gave it to W1-C.
3. `docs/ACCESSIBILITY.md` §13 — the rows of G-19 and G-21, closed (`tests/frontend/test_design_docs.py` holds
   the two documents to the same status).
4. `docs/design/DESIGN_SYSTEM_2026.md` outside §10 — the prose of §2's rows for the sheets this family adds,
   empties or deletes, the list of component properties, the entrance sheet's row in §2.1 (its fields), one
   sentence of §5.1 that cited `v3/buttons.css`, the rows of `initTabs` and `initAccordions` in §16 and of
   G-19 / G-21 in §21; the figures are `scripts/regen_design_inventory.py`'s.
Also in the slice but worth saying: `tests/frontend/test_state_chips_carry_a_register.py` skips every
development-only template (`templates/dev/**`), not only the showcase — it was red on design-v5 since the preview
landed (six `dp-state` labels of `templates/dev/designpreview/` read as chips).

**`static/css/v4/workspace.css` is left as it was.** A first pass took two selectors out of the workspace's focus
rule (`.console__workspace .form-field input…`, `… select`) to let the halo of §1.6 reach the console's fields.
It could not: the rule's first selector — `.console__workspace :is(a, button, input, select, textarea, summary,
[tabindex]):focus-visible`, (0,2,1) — names the text controls too and still beats the foundation's halo
(0,1,1), so the edit changed no pixel and only wrote in another family's file. It is undone. Measured on the
company's «Nouveau besoin»: a console field's focus is the ring, 3.70 : 1 on the workspace ground, and V4's
2 px companion in the ground's colour — no halo; a public field's is the ring and the 5 px halo. The console's
blanket rule is the console family's to keep or to retire (W3-A, W3-E); see the open point in
QA/v54/w1-c/NOTES.md on the ring beside its halo before the halo is carried there.

**Three more with the loader family's hand-over** (DL54-49, the busy face; `scripts/check_ownership.py w1-c`
lists six paths outside the slice in all — these three, and items 1 to 3 above):
5. `static/js/src/shell.js` (W1-D's section 4) — one constant: `KEYLESS` names the three padless variants the
   sheets draw. `tests/frontend/test_loader_rules.py` reads the list off the sheets and fails on any other.
6. `tests/frontend/test_loader_w1_d.py` (W1-D's) — one assertion, on the `::after` of a link-styled button:
   V3 drew the link's rule there, the V5 link has none.
7. `tests/i18n/test_rtl_static.py` (W1-A's) — `KNOWN_UNMIRRORED` is empty: its one entry was the V4 busy
   notches, and the test fails when a fixed entry stays on the list.

**Why.** Each is a rule or a sentence about this family's components living in a file another family owns; left
there, the component would have been half replaced (the W1-A review's m-1 and m-9 name the first), or a test
of another family would have stayed red on the tree that holds both (the last three).

**Source.** Plan §2.2 (the manifest; «a file not in the manifest has no writer until the steward assigns it»),
§2.3; W1-A REVIEW.md m-1, m-9; `scripts/check_ownership.py w1-c`.

## DL54-51 · 9 October 2026 · W1-C: tier 0 — the family's rules for a change asked from the keyboard

**Decision.** Plan §1.5 makes every keyboard-initiated change static (tier 0, 0 ms), and the input-modality flag
`html[data-input]` of `static/js/head.js` is the loader family's (W1-D: «each family writes its one rule,
`html[data-input="key"] <its selector> { transition-duration: 0ms; }`»). This family's rules were written on a
branch where the flag did not exist yet:
- `v5/buttons.css`: `html[data-input="key"] .btn` — the press, its way back on the spring and the fill.
- `v5/field.css`: `html[data-input="key"] .form-field { --field-draw: 0ms; }` (the 2 px rule, DL54-45's first
  item) and one rule for the plate's edge, `.input`, `.search-form__input`, the show / hide control, the checkbox
  and the radio with their tick.
- `v5/tabs.css`: the tab's label and the disclosure's mark. The indicator and the arriving panel need no rule:
  they travel only under `.is-travelling`, which `initTabs` sets for a pointer's choice alone
  (`event.detail > 0`).

**Why then.** Before W1-D's merge the rules matched nothing — no element carried the attribute — so they changed
no page: the 56 cells re-probed on the build that held them were equal, leaf by leaf, to the 316-cell sweep taken
without them (QA/v54/w1-c/NOTES.md). The loader reached design-v5 the same day and this branch holds both: the
family is at tier 0 with the real flag. `tests/frontend/test_browser_w1_c.py` sets the attribute itself and
reads every transition of the family at 0 s, so it held on both sides of that merge.

**Source.** Plan §1.5 (tiers, R-07), §1.6; `static/js/head.js` (W1-D); `static/css/v5/{buttons,field,tabs}.css`;
`tests/frontend/test_components_w1_c.py`, `tests/frontend/test_browser_w1_c.py`.

## DL54-52 · 9 October 2026 · W1-C: eight registers — «esame» and «blocco» enter by one rule; the badge kinds read as the notices do

**Decision.** `apps/core/chips.py` holds the eight registers of plan §1.2, in the plan's order — conforme, esame,
neutro, attesa, azione, rifiuto, blocco, nullo — for its 21 producers and 103 members. Sixteen members moved:
- **One rule, whatever the producer:** a member named `in_review`, `under_review`, `assigned` or `in_progress` is
  **esame** — somebody other than the reader has it in hand (nine members: the document «En examen», a need under
  review or taken in charge, a proposal under review, a ticket assigned or in review, a checklist item, a
  milestone and an enrolment under way);
  a member named `blocked` is **blocco** — a dependency, heavy and calm, never an alarm (three: a checklist item, a
  milestone, a piece of evidence; they were attesa). `tests/frontend/test_chips_registry.py` holds the rule both
  ways: no such member outside its register, and no other member inside it except the two rows below.
- **By their own rows:** a verification and a scan that are `pending` are esame (the team is checking the declared
  elements; the scanner has the file) — elsewhere `pending` stays a thing due (attesa); `not_required` and
  `not_configured` are nullo: nothing was asked, nothing was analysed, nothing is coming (they were neutro).
- **A stage is a position, not a piece in somebody's hands:** `selection.SelectionStage`'s three `…_review` stages
  stay neutro and `cases.CaseStatus.review_required` stays azione. The rule names members, not words that contain
  «review».
- **The mark is the register's**, from the icon registry (`icons.STATUS`, «i cerchi», W1-B): `chips.mark_for`. One
  member keeps its register and has a mark of its own — `documents.RequirementState.to_replace` draws
  `st-attesa-replace`, the ring with two arrows that tells «À remplacer» from «Manquant» at 16 px
  (ICON_SEMANTIC_MAP §2). V3's `GLYPH` table (the mask glyphs of «la vidimazione») is gone with its sheet.
- **The legacy `kind` of `components/badge.html`** is translated once (`KIND_REGISTER`): `warning` is **attesa**
  (it was azione) and `pending` is **esame** (it was attesa) — the readings the notices of the same names have
  since DL54-47 (the broken amber edge; «en examen» in lapis). Two kinds are added for the plan's deadlines:
  `soon` → attesa, `overdue` → azione. Red never means lateness.
- **A value the module does not know gets no register:** the chip is drawn on the neutral tone with the neutral
  mark and a dotted edge — visible — and the tag logs a warning; the registry test keeps it out of the product.

**Not done here.** `apps/portal/services.py::present_deadline` still gives «En retard» the kind `error` (platform
map F13): plan §3.5 gives «the deadline kinds in `apps/portal/services.py`» to the document workspace (W3-C). The
two kinds wait for it. Until then «Bientôt», which the service calls `warning`, is already amber — half of F13 —
and «En retard» is still drawn as a refusal. The same file's `SCAN_BADGES` translates a scan's state into legacy
kinds for the bridge's cards (`clean` → `success`, `error` → `warning`), beside the registry's own row for
`documents.ScanStatus` (`clean` → neutro, `error` → azione): two tables for one enum. With `warning` read as
attesa, a scan that failed is amber on those cards where the registry says azione; the template can call
`{% chip d.scan_status "documents.ScanStatus" %}` once the service hands the member over.

**Why.** Plan §1.2 names eight registers and «En examen» in lapis; the six-register table of V3 had put every
«somebody has it» on the neutral slate and every «blocked» on amber, beside the things that are merely due.

**Source.** Plan §1.2 (the eight registers, «Deadlines», O14); ICON_SEMANTIC_MAP §2; DL54-47; `apps/core/chips.py`,
`apps/core/icons.py` (`STATUS`); `tests/frontend/test_chips_registry.py`.

## DL54-53 · 9 October 2026 · W1-C: the chip has one producer — the `{% chip %}` pair; a term is a tag

**Decision.**
- **One producer.** `{% chip member "app.Enum" %}word{% endchip %}` — or `register="…"` where a state has no enum —
  is a block tag of the built-in library (`apps/core/templatetags/ile_core.py`, Django's `simple_block_tag`) that
  renders `templates/components/chip.html`: the `span.chip` with its `data-register`, the register's mark
  (`svg.icon.chip__g`, hidden from assistive technology: the word says the state), the word in `span.chip__w`, and
  for a case status the three notches of its phase. The word stays the template's own content — a translated
  display value or a `{% translate %}` — which is why the producer is a block and not an include with a `label`.
- **Every site goes through it:** 76 calls in 42 product templates — 72 of the 81 sites that wrote the element
  by hand (the other nine are tags, below) and the two badge partials, `components/badge.html` and
  `allauth/elements/badge.html`; the showcase and the chip board too.
  `tests/frontend/test_state_chips_carry_a_register.py` fails on a chip written by hand, on a call that names an
  unknown producer or register, and renders every member of every producer through the tag. So a chip is never
  drawn without its mark (O17), and never by colour alone.
- **Gone:** the `chip_stage` filter (the tag computes the phase), the `state`, `state--word` and `badge--kind`
  classes on the element, `chip--seal` on the company dashboard — the project's «Vérifiée» is conforme, ink and
  the plain disc, never a seal (O18). `chip--indicative` and the seal chip are not drawn: neither has a producer.
- **A term is not a state.** Nine sites that drew a chip for a term or a category are a `.tag` — paper, a hairline,
  no register and no mark: the glossary terms under a pathway and under the diplomas page (2 + 2), the level of a
  skill in a company's need (2), the kind of a helpdesk message («Question», «Réponse») and its «note interne»,
  a room's «En évidence».
  A tag that is a link is hit in 44 px under a coarse pointer, the pill itself staying 24 px.
- **What a person chooses is not a chip:** a filter is a control of its own family and carries no check either;
  the filters' legend of «Mes pièces» draws the register's mark in place of the 10 px dot
  (`documents/partials/register.html`, the `chip_mark` filter) — at 14 px with the gap taken back, so an entry is
  as wide as it was and the search field stays on its row at 1440.
- **The health strip reads the chip's tokens** (`v4/workspace.css`, `.health__segment[data-register]`): its V4
  rules knew six registers, so a segment of esame or blocco would have been painted with nothing.

**Why.** Plan §1.2 and §3.3: each register with its mark from the sprite and never colour alone. Written by
hand at 81 sites the mark would have been 81 promises; with one producer it is one fact, and the next register
or the next mark is one edit.

**Source.** Plan §1.2, §1.8, §3.3 item 7; O14, O17, O18; `apps/core/templatetags/ile_core.py` (`chip`,
`chip_register`, `chip_mark`, `badge_register`); `templates/components/chip.html`;
`tests/frontend/test_state_chips_carry_a_register.py`.

## DL54-54 · 9 October 2026 · W1-C: `v5/chip.css` — 24 px by construction, the mark on the first line, the edge as a voice

**Decision.** `static/css/v5/chip.css` replaces `static/css/v3/chip.css` (deleted), the badge rules of
`components.css` §3 and the pill block of `v4/workspace.css`.
- **The height is built, not set:** the line (20 px), 1 px of block padding and the 1 px edge make 24; the dense
  chip is an 18 px line and the edge, 20; the large one 20 + 6 + 2, 28. It is a `min-block-size`: a long label
  wraps — it is never cut — and its 16 px mark (14 in the dense chip) stays centred on the first line, 3 px from
  the edge, concentric with the end cap. Arabic takes the same boxes at its 14 px floor.
- **In a table cell a chip is one line** and is not held to the cell's width: the column takes the chip.
- **The state is said three times without colour:** the word, the mark, and the style of the edge — solid, dashed
  for a thing due, dotted for one that carries nothing (the tokens of `v5/tokens.css` §4.1, W1-A's). Colour is the
  fourth voice. The sheet reads five names (`--chip-bg`, `-edge`, `-edge-style`, `-mark`, `-text`) and writes no
  colour of its own, so paper, white, night and forced colours are the tokens' business.
- **No small capitals, no tracking** (V3's stamp), and **not a control:** no pointer, no hover, no focus.
- **The gauge** of a case status: three 6 px notches after the word, as many filled as phases reached; decoration,
  hidden from assistive technology.

**Source.** Plan §1.2, §1.3, §1.8, §2.3; DS V5 §4.1, §10.2; `static/css/v5/chip.css`;
`tests/frontend/test_chips_cards_w1_c.py`, `tests/frontend/test_browser_chips_w1_c.py`.

## DL54-55 · 9 October 2026 · W1-C: cards by purpose — a record, an action, a summary; no stat grid, no board

**Decision.** `static/css/v5/card.css` replaces `components.css` §13 and draws three things, named by what they
are for:
- **The record card** `.card` — a thing that exists and can be opened: the sheet surface, the card's hairline and
  8 px corner, shadow level 1. With `.card--link` the title's link covers the card — one destination, one tab
  stop. Hover darkens the edge and underlines the title; no shadow moves and nothing lifts (SH-4).
  `.card--flat` is the same record without a box, under a hairline, for a list on paper.
- **The action card** `.card--action` — the one thing to do next: the raised surface, no edge, shadow level 2, and
  one primary (`.card__action`). One raised plane a screen (SH-8).
- **The summary strip** `dl.summary` — a few facts of a file in one bordered strip, cells divided by hairlines,
  words and figures at text size (17 px). It wraps by full rows (four cells: one row at 1440, two by two at 390).
- **Three things the final sweep added**, on the five page types that draw a card today (the two phases of
  «Formation», the related lists of the three doors and of the pilot): an entry of a list has the same room
  under its last line as over its first (20 px) — those lists keep an 8 px row gap and the next hairline sat on
  the text; a link alone in the meta line — the card's second action — is a 24 px target on a line that stays
  13/20 (it had dropped to 20 px: two targets under the floor on «Formation»); and a card whose content is
  wrapped in **one** labelled `<section>` keeps the card's flow — the 12 px between its parts, the meta line at
  the foot — so the second actions of two cards in a row stand on one line.
- **No stat-card grid and no rearrangeable board** are drawn and no class offers one (plan §1.15: the system
  orders by priority; disclosures fold what is secondary). A summary's figure is never set as a numeral.
- **At most three radii a screen** (DL54-14): the card's 8, the 4 of buttons and fields, and the pill. Three
  console fields that `v4/workspace.css` draws itself kept V4's 6 px — the search of «Mes pièces», the
  checklist's select, the case file's state form — and take `--field-radius`.
- `.meta-row`, the tail of §13, is carried into the sheet on V5 tokens.

**Not done here.** The action card and the summary strip have no product consumer yet — they are drawn on the
showcase and on the chip board; the dashboards are W3-B's. The six-card «bridge» of the accounts that are neither
a person nor a company (`templates/portal/partials/card.html`, `portal.css`, pinned by the portal's tests) is a
card grid of the kind §1.15 retires: it is W3-B's page, and is left as it stands. The console's rail keeps a
6 px corner on its rows and its tile (W3-A's): a console screen at 1440 shows 4 · 6 · 8 and the pill in its first
viewport until the shell is redrawn.

**Source.** Plan §1.3, §1.4 (SH-1 … SH-9), §1.15; DL54-14; DS V5 §8, §10.5; `static/css/v5/card.css`;
`templates/components/card.html`; `tests/frontend/test_chips_cards_w1_c.py`.

## DL54-56 · 9 October 2026 · W1-C: the O14 lint is a test, in four languages — and its first finding

**Decision.** `tests/frontend/test_o14_lint.py` is the lint of plan §1.2 («completed so it also catches JavaScript
cases»), run on the product at every test run:
- **HTML** — every product template read as a tree: inside a status context (a chip, anything that carries
  `data-register`, a badge, a filter's entry, the health strip, a journey or timeline node, a stepper, a rail, the
  ledger, an actor's disc) no check-bearing symbol of the sprite is drawn at any depth and no check character is
  written; a symbol named by a variable must come from a registry map, and the maps are held to hold no check.
- **CSS** — every sheet and every bundle: no check character in a `content`; a rule that paints a settled state or
  a status context draws no tick, as an image, a clip or a rotated border.
- **JavaScript** — no script names a check-bearing symbol or writes a check character.
- **Python** — no producer writes one into the page.
It catches its 30 planted cases and leaves its 16 clean ones alone: the check stays the mark of the person's own
act (`icons.CHECK_BEARING`: a chosen option, a ticked box, an account confirmation) and of nothing else.

**Its first finding** was in the cascade: the V1 stepper wrote a check (U+2713) as the `content` of a done step's
marker (`components.css` §16). The rule is deleted — a done step is its filled disc with its number. No product
template includes `components/stepper.html` today (the showcase does). §16 is the journey family's (W3-D): one
rule, removed because the lint this family owes cannot be green beside it.

**Source.** Plan §1.2 («Standing rulings», O14; the research's decision log A5); `tests/frontend/test_o14_lint.py`;
`apps/core/icons.py` (`CHECK_BEARING`).

## DL54-57 · 9 October 2026 · W1-C: the paths the chips and the cards wrote outside the slice

**Decision.** `scripts/check_ownership.py w1-c design-v5` lists 60 paths outside W1-C's slice: the six of DL54-50
and 54 of this step, for the merge step to record.
1. **46 templates** — 41 of the 42 product templates that call the chip (DL54-53; `components/badge.html` is
   in the slice): academy 5, accounts 1, allauth 1, cases 2, community 3, companies 6, components
   `case_timeline.html` and `document_row.html`, documents 1, forum governance 9, helpdesk 3, pathways 2,
   portal 2, selection 4; the two that now hold tags only (`pathways/detail.html`, `pathways/diplomas.html`); the
   filters' legend `templates/documents/partials/register.html`; `templates/components/card.html` (its comment:
   the record card); `templates/dev/showcase.html`. In each, only the chip (or tag) element changed: the words,
   the order and every other element are as they were. The task's «Propagation: every template that uses them».
2. `apps/core/templatetags/ile_core.py` — the `chip` block tag and the three filters; `chip_stage` removed.
3. `static/css/v4/workspace.css` — the pill block removed; the health strip and the filters' dot re-pointed to the
   chip's tokens; three fields at the field's radius (DL54-55).
4. `apps/documents/static/documents/documents.css` — two selectors, `.state` → `.chip`.
5. `static/css/base.css`, `static/css/v5/base.css` — dead selectors of the old chip (`.state`; `.chip__q`,
   `.chip__n`) removed from two lists.
6. `tests/frontend/test_icons.py` — one marker: the end of §2 was found by the heading «3. Badges», which is gone.
7. `apps/core/dev.py`, `static/css/dev/specimen-chips.css` (new, in no slice) — the showcase's demo register and
   the chip board's sheet, development only.
8. `docs/ACCESSIBILITY.md` — already listed by DL54-50; this step moved where G-14 lives (the chip's sheet).
And one the script cannot see, because the file is shared: `static/css/components.css` **§16** — the stepper's
check (DL54-56); the section is W3-D's.

**Why.** A component with one producer changes every site that drew it by hand, and the rules it replaces lived
in five sheets. Left in place, the old chip would have been drawn beside the new one.

**Source.** Plan §2.2, §2.3; `scripts/check_ownership.py w1-c design-v5`; DL54-50.


## DL54-58 · 9 October 2026 · W3-A: one builder for every rail, two spaces

**Decision.** A **space** is a set of pages that share ONE rail: «Espace réservé», which every account has, and «Espace
entreprise», the company workspace. A page belongs to a space by its route; nothing about it is stored.
`portal.services.shell_navigation(user, space, active)` builds every rail, and every producer of a console page asks it —
the portal's own views through `navigation()`, the Academy, the help desk, the selection workspace and the company
workspace (whose own entries stay `companies.services.navigation`'s: the module decides what a company, a prospect and a
project reader may be offered). In the rail:

- the registers a **role** owns come first, under «Mon rôle» — a professional's queue, an actor's processes, the
  dispatch desk of an operator or an administrator (`helpdesk-dispatch`, which was reachable from the help desk's pages
  only) — then the ten destinations, unchanged, in their three sections;
- the account's **other space** is an entry of kind `space`: the rail draws it at its head, named as that space names
  itself, and never among the pages;
- **four entries at most** reach the phone's bottom bar, for every role (`NAV_BOTTOM_MAX`, `_bottom_keys`): the
  dashboard, the pieces, the communications, then the surface the role owns — or the cases.

**Why.** Measured on the lane before the build, on 29 page types and ten accounts: every account saw **four or five
different key sets** depending on the URL (the Academy, the help desk and the selection workspace each added or dropped
rows on their own pages); a company and the administrator had **five** flagged bottom entries; the help desk's pages
carried one label twice for a professional and marked two entries current. After: **two key sets per account — its two
spaces**; four bottom entries at most; no label twice; never two entries current.

**Left.** The Forum permanent still appends its five rows on its own pages (its gate is closed: 503) — its family's, when
it opens. The company rail's «Communications» leads to the page of «Espace réservé», as the module defines it.

**Source.** Plan §1.18 D06 («One rail per account type (`shell_navigation(user, space)`)», «The bottom bar holds ≤ 4
entries + Menu»); §3.5 item 3 (gate); the platform audit's S-4. Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w3-a/nav/{before-v4,after-services}.json`; `tests/frontend/test_console_shell_w3_a.py`.

## DL54-59 · 9 October 2026 · W3-A: level 1 is a line under the name; who the account is stands at the foot

**Decision.** The rail's three levels are told apart by their form. **Level 1, the space,** is not a plate of its own: it
is the line under «ITALY LEGAL ENTRY™» at the rail's head (the brand link leads to the space's first page), and, for an
account with two spaces, one row beneath it — the way to the other. **Level 2** is a word on the text axis; a rule
without the word where the word would only repeat its one entry («Academy») or the space's name. **Level 3** is the
page: glyph + word.

**Who the account is** — Persona ≠ Impresa ≠ Istituzione ≠ Università — is said once, at the foot, beside the account's
name: the registry's glyph and the role's own label. The project team first; then the account's **roles** (institution,
university, training body, authorised actor, professional, person, company); then the account **type**, for an account
that holds no role yet.

**Why.** A separate plate for the space cost a row of 44 px, which is what kept a person's rail from holding at
1366 × 657 (S-1). The roles come before the type because a privilege is a group here and the type defaults to «person»:
a company's representative, a professional and an operator are all created with it — and the QA persona «personne avec
dossier» is typed `company` while holding the person's role: it is a person.

**Source.** Plan §1.18 D06 («Tre livelli»); §1.7 (the four audiences' glyphs); the audit's S-1. `shell_space`,
`_AUDIENCES` in `apps/portal/services.py`.

## DL54-60 · 9 October 2026 · W3-A: open from 80rem and remembered; compact is glyph-only until its short labels are signed

**Decision.** From 80rem the rail is **open** (248 px) by default — at 1280, 1366, 1440 and 1920 nobody meets a rail of
icons alone; the person's choice is kept (`localStorage`, `ile.rail`) and written on `<body>` before the first frame
(`rail-pref.js`), and without script the rail is open. Between 64rem and 80rem the default is the **compact** rail:
**64 px, glyphs alone on the same axis as when the rail is open**, each with its word beside it on hover and on focus.
One density step: under 760 px of height with a fine pointer the rows are 40 px.

**Why not the labelled compact rail** (DS V5 SC01: 80 px, a 12/16 label under each glyph)? The ten labels do not fit
72 px — «Communications», «Tableau de bord», «Guichet numérique» would be broken or cut, as the phone's bottom bar shows —
so the labelled rail needs **short labels**, which are new copy (B1) and unsigned. `--rail-w-compact: 80px` stays in the
foundation for that day; the shell's own measure is `--rail-compact: 64px`.

**Source.** Plan §1.18 D06; §1.8 (rows 44; 40 under 760 px of height on a fine pointer); DS V5 SC01; B1.
`tests/frontend/test_console_shell_browser_w3_a.py` (the default by width, the stored choice, CLS < 0.01).

## DL54-61 · 9 October 2026 · W3-A: the foot

**Decision.** The foot is pinned; the list scrolls between the head and the foot. It holds, in two rows: **the account**
— its glyph on a night disc, its name and who it is — as a link to the profile, and **«Se déconnecter»**, a lone glyph
that posts the sign-out form; then **the rail's control**, **the language** — the current one by its own name; the four
open ABOVE the control, in a column on the text axis — and **«Site public»**, in its two words.

- **No account popover.** The plan gives the console «its use of the account popover», which belongs to the overlay
  system (W2-A, not shipped): until then the three things a popover would hold are in the foot itself. The V4 account
  menu stays in the phone's top bar.
- **One row in the four languages.** Measured: French and Arabic fitted with 0 px to spare and Italian was 8 px over —
  the chevron of «Italiano» lay on «Sito pubblico». «Site public» lost its arrow (the drawer draws it without one), the
  paddings came closer, the language's name is never squeezed: 15 px to spare in Italian, the longest pair. Under the
  user's own text spacing (WCAG 1.4.12) the last word goes under the row, never over its neighbour.
- A name the rail has to cut is shown whole by the account's word (DL54-62), which says who the account is too.

**Measured.** At 1366 × 657 the open rail of a person holds whole in French, Italian, English and Arabic — ten pages,
three section words, the head and the foot, 518 px of list in 518 — and the foot's five controls are in view; in French
and Arabic likewise at 1280 × 800, at 1920 × 1080 and, compact, at 1024 × 768. A longer rail (a role's registers, a
second space) scrolls under the pinned foot and its last page is reached.

**Source.** Plan §1.18 D06 («Site public at the rail's foot», «a pinned rail foot»); D21 («Languages by their own
names»); §3.5 item 3 (gate: the foot visible at 1366 × 657); the audit's S-1.

## DL54-62 · 9 October 2026 · W3-A: «il lume» is the lit disc; the word of a lone glyph stands beyond the rail's edge

**Decision.**
- **«Il lume»** marks the current page: its glyph on a **lit paper disc** — the material of the tile that carries the
  mark at the rail's head, where the loader's light is released — on the row's night plate, the word at the title's
  weight. Once per rail copy. **No bar at the edge**: D06's fallback is not used. D06 asked for a taste check of the
  disc's kinship with a well-known active indicator (a tonal pill behind the icon): the disc is not a tone of the
  surface but the one paper element of a night rail, it is a circle of the glyph discs' own measure (32 px), and the
  selection does not rest on it alone — the row's plate and the word's weight say it too; under forced colours the row
  keeps an outline and the disc the system's highlight.
- **The word of a glyph that stands alone** (the compact rail's entries, sign-out, the rail's control; a name the open
  rail had to cut) is one element, `.rail__tip`, on the control's own line and **beyond the rail's edge**. Laid beside
  the control, inside the rail, it covered the next control of the foot for as long as the pointer rested on it — and
  the pointer may rest on it (WCAG 1.4.13, hoverable). It wraps inside its box, stays whole in the viewport, waits
  400 ms under the pointer and not at all under the keyboard, and leaves on Esc **wherever the focus is**.

**Source.** Plan §1.18 D06; §1.11 (Tooltip); §3.1 item 7 (the identity carriers); WCAG 1.4.13.
`tests/frontend/test_console_shell_browser_w3_a.py`.

## DL54-63 · 9 October 2026 · W3-A: «Communications d’identité» keeps a place; «Changer d'espace» is not drawn

**Decision.**
- **«Communications d’identité»** — the panel where a person decides whether a company may know who they are — is a
  page of the rail, the last of «Échanges», with the registry's glyph for that consent (`pen-line`), **for the account
  somebody has asked** (`selection.services.has_disclosures`) and for nobody else. The ten destinations stay ten for
  everybody; the keys depend on the account, never on the page.
- **«Changer d'espace»** (D06's words for a multi-space account) is not drawn: the string is in no catalogue, and new
  copy is B1. The way to the other space is named by the space it leads to — «Espace entreprise», «Espace réservé» —
  in words the pages already carry, in the four languages. The label waits for the copy review.

**Why.** The selection module listed the panel in a rail of its own, drawn on its own pages only: an actor reached it
from the workspace, and a person — the one who decides — by no link at all. Under one builder that row is either lost or
given a place; a consent that can be withdrawn at any moment has to stay within reach of the person who gave it.

**Source.** Plan §1.18 D06 («The ten destinations are kept», «The rail's destinations, URLs and permissions are
unchanged»); B1. `_identity_panel` in `apps/portal/services.py`; `apps/core/icons.py` NAV.

## DL54-64 · 9 October 2026 · W3-A: the page frame

**Decision.**
- **One start edge** for everything a page draws — 32 px from the rail (16 px below 48rem), in a column of 1320 px at
  most — and one rhythm: 32 px under the bar, the page header, 32 px, the content.
- **One page header, by the frame's own rules**, whatever markup a page's family still carries (`page_header.html`,
  the ContextHeader `.ctx`, `.ws-head`, the documents pages' titles): the title at the console's title size (28 / 36,
  600), its line of context at the body's, the page's one primary action at the reading end of the title's row. The
  level is the breadcrumb, in the bar. The families redraw their headers inside this frame; the frame does not wait for
  them.
- A title or a lead written in another language than the page hugs its words, so it stays on the reading edge
  (`fit-content`, bounded by the frame).
- **«Lo spigolo».** The shell draws 4 px and full; a page's panels 8. A console **button** takes V5's corner for a
  control, 4 px, from the frame (`.console .btn`) where the V4 button sheet still gives it 6 — the plan's fold
  («usually 6 → 4»), once for every page. Measured on 48 page rows: 45 draw three corners or fewer (12 drew four and
  one five). The three left are their families': the documents pages' search field (6, W3-C) and the wizard's panel
  and field on «Ma situation» (12 and 6, W3-F1).
- **Two native skip links** follow «Aller au contenu principal»: the rail from 64rem, «Menu» below it — three keys to
  the navigation on a phone (S-2), no script.
- **Nothing of the shell animates at load**; the rail's width moves on the person's own act only.

**Source.** Plan §3.5 item 3; §1.3 («Where a screen would show a fourth value…»); DL54-14; the audit's S-2.

## DL54-65 · 9 October 2026 · W3-A: paths outside the slice, the legacy rules deleted, the CSS weight

**Seven paths outside the family's slice** (`check_ownership.py w3-a`), each for one reason:

| Path | Owner | What, and why |
|---|---|---|
| `apps/academy/views.py`, `apps/helpdesk/views.py`, `apps/selection/services.py`, `apps/companies/views.py` | none | each module's rail producer now asks `shell_navigation` — the one builder is the family's own gate («the same rail keys on every URL of a space»); `selection.services` also gains `has_disclosures` (DL54-63) |
| `apps/core/icons.py` | W1-B | `NAV` gains `helpdesk-dispatch` → `settings` and `disclosures` → `pen-line`: «a key added to the rail is added to the registry first» |
| `tests/frontend/test_icons.py` | W1-B | the stand-in account that walks every entry of the rail is handed the identity panel's row, as it is handed every role's register |
| `apps/portal/static/portal/portal.css` | W3-B («the bridge part») | four blocks the shell supersedes are deleted — the V1 platform bar, the platform footer, a no-JS guard of the public header, the reserved area's own title size (below) |

Four sentences of DS 2026 outside «the console shell's prose» were corrected so that the document stays true — where
`language_segmented.html` and `account_menu.html` are used in the console (§10, §11.3).

**The legacy rules.** The bust rule's first remedy (DL54-15): a family deletes the legacy rules its components
supersede. Every property of the four blocks is re-declared by `v5/_shell.css`; proved on the lane — the computed styles
and the boxes of the bar, its children, the footer, the page header and the workspace on 11 page types × fr / ar ×
1440 / 1024 / 390 are identical before and after.

**The weight.** `dist/portal/console.css` 13 807 → 22 461 B (2 936 → 4 235 B gzip); `dist/portal/portal.css` 12 311 →
10 243 B (2 687 → 2 263). The console page type's CSS (`main.css` + `portal.css` + `console.css`) stands at **50 431 B
gzip — 49 556 before the family (+875), and 571 B over the Wave-1 ceiling of 49 860** that W1-D's check recorded. The
shell has no row in the deletion map (V4's console sheet was the entry it replaces), so nothing else of its own is left
to delete; the phone chrome's patches in `v5/base.css` leave with the phone redraw (step 2). Under V5.5 («fix only real
regressions») it is reported, not hidden: the Performance check measures the console's first render on 8782, and the
steward records the ceiling.

**Source.** Plan §2.2; §2.6; DL54-15; `OWNERSHIP_V54.json`.

## DL54-66 · 9 October 2026 · W3-A: below 64rem the rail is laid flat — its head on top, its pages at the bottom, the whole of it in the drawer

**Decision.** Below 64rem the rail is not drawn at the reading edge: it is laid flat, in three pieces, in the same
night. **The top bar is the rail's head** — the mark on its paper tile (the way to the space's first page), the level
of the page as a title, the account. **The bottom bar is the rail's pages** — four entries at most and «Menu».
**The drawer holds the whole rail** and the rail's own foot. The two bars are the rail's night (`--rail-bg`), without
glass, without a shadow and without an edge: the night stops where the paper starts. **«Il lume»** on the bar is the
rail's lit paper disc — the current page's glyph in ink on a 32 px disc of paper, its word in the night's first ink —
and never a bar at the edge; the word's weight does not change, so a word never changes lines when its page becomes
the current one.

**Why.** The gate-0 comp drew a night top bar and a white bottom bar whose current entry was a tint of the accent
under a 2 px bar at the bar's top edge. That bottom bar rested on short labels («Accueil · Dossier · Pièces ·
Messages»), which are unsigned copy (B1), and on the edge indicator that DL54-62 gave up for the rail. A white bar of
five tinted glyphs is also what every product draws: on a phone the console had no carrier of its own at rest (plan
§3.1 item 7 names «il lume» in the rail). The owner's ruling O13 keeps «the same night chrome» over a lighter paper:
laid flat, the rail brings its night, its tile and its disc with it, and the phone's screen passes the swap test by
the same signature as the desktop's.

**The account.** The top bar keeps the menu of design V4 (`account_menu.html`, the overlay family's) until the
account popover exists: on a phone it is its glyph alone on the night disc of the rail's foot, 44 px to the finger —
its name stays its accessible name, and the name is drawn in the drawer's foot; from 48rem the name stands beside the
glyph. There is no «≡» in the top bar: «Menu» stands once, in the thumb's zone.

**The band from 48rem to 64rem** (a tablet upright, a phone on its side, a narrow window) keeps the same three
pieces — the glyph-only compact rail has no hover under a finger. There is room for the rail's own row: the glyph on
its disc beside its word, in a bar of 56 px. The current entry has no plate there: a label that wraps leaves its seat
wider than its words, and a plate would draw that.

**Source.** Plan §1.18 D06; §3.5 item 3 (gate); §3.1 item 7; CD V5 §8 («Phone»); O13; DL54-62.
`apps/portal/static/portal/v5/_shell.css` §5; `templates/partials/portal_chrome.html`. Captures:
`C:/tmp/ile_v5_council/evidence/v54/w3-a/step2/` (`before/`, `final-look/`, `final-states/`).

## DL54-67 · 9 October 2026 · W3-A: the phone's measures — 120 px of chrome at most, and less where the screen is short

**Decision.** The top bar is **48 px** below 48rem and 56 px in the band. The bottom bar is as tall as its tallest
entry: 52 px when every label holds on one line, **66 px** with a label on two (55 and 72 px in Arabic, whose labels
are 14 / 17). The chrome that stays on screen is therefore **114 px in French, Italian and English and 103 px in
Arabic** on every measured account from 360 to 430 px — 120 px at most (the gate; the audit's S-3). Where the viewport
is short (under 30rem of height: a phone on its side) or very narrow (under 22.5rem: a 320 px phone, a window at
400 %) the top bar is the page's first line and **leaves with the page**: the bottom bar alone stays; and in a short
viewport the drawer's foot is not pinned either. **On paper** there is no rail, no bar and no drawer, and the page
gives back at once the room it kept for them: a fixed bar is printed again on every sheet.

**Why 48 and not the comp's 57.** The words of the bar are the live labels (DL54-68): two of a person's four take two
lines in French, and two lines of 12 / 14 under a 32 px disc make 66 px. 57 + 66 would be 123. The top bar gives the
9 px: it carries the tile (32), a title on one line (20) and one 44 px target, which 48 px hold.

**Measured** (lane 8786, Chromium, phone emulation; ten QA accounts × fr / it / en / ar × 320, 360, 375, 390, 412 and
430 px = 312 drawings): chrome 114 px at most (V4: 113 with broken and clipped words; 174 on the case file; 177 on
«Ma situation»); four entries at most; every label on one line or two; 7.7 px at least between the words of two
entries; every seat at least 51 px wide and 52 px high; no word outside its seat or outside the screen. The only
horizontal overflow met is a page's own, on 11 of the 312 drawings: a person's dashboard whose pre-assessment panel
holds a link that does not wrap (W3-B's — 9 px at 320 in French, as before the step; 6–33 px in Italian up to 375;
26–60 px in English at every width) and the company dashboard's «needs» panel head at 320 in Italian (4 px).

**Source.** Plan §1.18 D06 (S-3); §3.5 item 3; WCAG 1.4.10. `_shell.css` §1 (`--bar-top`, `--bottom-clear`), §5;
`evidence/v54/w3-a/step2/final-matrix/report.json`.

## DL54-68 · 9 October 2026 · W3-A: the bar's words are the live labels, whole — one line or two runs, three entries where four do not hold

**Decision.** No label of the bar is shortened and none is new: the words are the rail's own («Tableau de bord»,
«Mes dossiers», «Mes documents», «Communications», a role's register by its full name). They are 12 / 14 in Latin —
the floor of the scale — and 14 / 17 in Arabic. Three rules make them hold:

- **A label stands on one line or on its two runs, never on three, and is never cut.** The builder splits it
  (`portal.services._bar_lines`: at the space that leaves the shorter longest run — «Tableau» · «de bord»,
  «Demandes qui me» · «sont confiées», «Communications» · «(2)»), and the bar breaks a label between its runs and
  nowhere else. A stylesheet can size a seat to a label's longest word or to its whole line, never to its two
  balanced lines: left to wrap by itself, a register's name took three or four lines in a seat that two would have
  filled.
- **A bar whose words do not hold on one line of a phone draws them on their two runs at once**
  (`_bar_stacks`, an estimate for the row of a 360 px phone): each seat then asks the row for its longer run and no
  more. An Arabic bar and a bar of two entries keep their line. The air of an entry (6 px on each side, inside its
  target) gives way before a word does, and two entries' words are never closer than 6 px.
- **Three entries where four do not hold** (`_bottom_yield`; `yields` on the entry that leaves): below 22.5rem for
  every bar — the cases leave a person's bar (the dashboard opens on the case), the pieces a company account's, the
  company's sheet the company space's; below 30rem for a bar that carries a role's register — with four entries its
  words stood 4 px apart from 360 to 430 px and a professional's needed a third line in English. The entry stays in
  the drawer, one press further.

**What it is not.** V4 hyphenated inside words («Communica-tions», «Mes docu-ments») and clipped what did not fit; the
comp wrote short labels. Short labels are copy (B1): the day they are signed the bar can draw one line for every
role, and these three rules have nothing left to do.

**The company space's bar is the shell's** as its cap is: the module's flags are capped at four and the rail's
remaining pages complete the bar while there is room — a project reader without a company had one entry and «Menu»,
and the page one was on («Analyse territoriale») was not among them.

**Source.** Plan §1.18 D06 («The bottom bar holds ≤ 4 entries + Menu»); §1.1 (never under 12 px); D21 (never under
14 px in Arabic); B1. `apps/portal/services.py` (`_bar_lines`, `_bar_stacks`, `_bottom_yield`, `_company_rail`);
`evidence/v54/w3-a/step2/labels.json` (every label's width, on one line and by its longest word).

## DL54-69 · 9 October 2026 · W3-A: one «Menu», a link that script turns into a button; the drawer holds the rail's own foot

**Decision.**
- **«Menu» stands once**, at the reading end of the bottom bar, and is reached in three keys (the second skip link).
  It is a link to the drawer (`href="#console-drawer"`): `console.js` turns it into the button of a modal drawer —
  the role, Enter and Space, `aria-expanded`, the focus on the page one is on, Esc, a press on the scrim, the focus
  returned, nothing added to the address. **Without script the link stays a link and still leads somewhere**: the
  stylesheet shows the drawer it points at (`html.no-js .console-drawer:target`) and the close control
  (`href="#main-content"`) leads back to the page. V4's «Menu» was a button that opened nothing without script, and
  only the bar's four entries were within reach.
- **The drawer keeps today's mechanism** — a native `<dialog>` opened with `showModal()`; its move onto the overlay
  system comes with that family. What changes is what it holds: the rail's own foot, from the same partial
  (`rail_nav.html`, `part="foot"`), instead of V4's segmented language track. Who the account is (→ the profile),
  **sign-out as a row with its word** (a finger finds no hover, and the rail's lone glyph relies on one), the language
  by its own name — the four open above it, as in the rail — and «Site public». The rail's own control is not drawn:
  nothing folds in a drawer. Esc puts the language's list away before it puts the drawer away.
- A window widened past 64rem puts the drawer away. While it is open the page behind the scrim does not scroll. A
  long name — an e-mail address — goes on a second line in the drawer's foot, never under an ellipsis: the rail
  shows a name it had to cut whole in the word beside its control, and a drawer has no such word.

**Source.** Plan §1.18 D06 (O63, S-2); §3.5 item 3; D21; CD V5 §8 («the console drawer kept as built»);
WCAG 2.1.1, 4.1.2. `templates/partials/portal_chrome.html`, `templates/portal/partials/rail_nav.html`,
`static/js/src/console.js` §3.

## DL54-70 · 9 October 2026 · W3-A: a page's action bar takes the four entries' place; the questionnaire's foot is part of its page

**Decision.**
- **The action bar is a contract of the shell** (O63): a page that keeps ONE act within the thumb's reach on a phone
  declares its bar — `data-console-action`; the case file's own bar (`data-file-action-bar`) is its first holder, read
  as it is. The bar stands where the four entries stood, on the page's own glass, and «Menu» keeps the same end of
  the same row: the bar leaves it a seat of 64 px. **48 + 61 = 109 px of chrome** on the case file, where the page's
  bar stood over the bottom bar (174 px). The four entries are one press further, in the drawer.
- **A bar that holds several controls is not an action bar.** The questionnaire's foot on «Ma situation»
  («Précédent», its count, «Continuer», «Enregistrer et recalculer») was sticky over the bottom bar — 177 px of chrome
  while its form was on screen — and five controls do not hold beside «Menu» (measured at 360 px: 306 px of controls
  for 280). Below 64rem it closes its form where the form ends, and its controls wrap rather than squeeze. Its family
  redraws the questionnaire; the page's one act is then a candidate for the action bar.

Both are written in the shell's sheet against the pages' existing hooks, with `:has()`: no template of another family
is touched. The day a family renames a hook, `test_console_shell_w3_a.py` says so.

**Source.** Plan §1.18 D06 («actions sit at the band's end or in the phone action bar»); O63; CD V5 §8; the audit's
S-3. `_shell.css` §5; `tests/frontend/test_console_phone_browser_w3_a.py`.

## DL54-71 · 9 October 2026 · W3-A, step 2: two paths outside the slice, the foundation's two patches retired, the CSS weight

| Path | Owner | What, and why |
|---|---|---|
| `static/css/v5/base.css` | W1-A | its two patches for V4's phone bar are deleted — the 12 px size of the bottom bar's labels and the 14 px title with its 8 px gap. Their own comments say so: «the bar's geometry is the console shell's (W3-A), which retires these two lines when it redraws the bar». The rules were written `:root body …` to beat the console's sheet: left in place they would have beaten the new bar too |
| `tests/frontend/test_browser_w1_b.py` | W1-B | one filter of `test_the_rail_the_bottom_bar_and_the_drawer_draw_the_registrys_symbols`: «Menu» is a link now (`#console-drawer`), so the bar's entries are the links to a page |

**One sentence and one figure of DS 2026 outside «the console shell's prose».** The row of `v5/base.css` in §2
named the two patches «until W3-A redraws the bar»: it now says they left. Its weight (9.5 → 7.9 KB, 20 % off: the
weights test allows 10) and §16's total of `static/js` (17.3 → 17.5 KB, step 1's) were rewritten by the steward's own
script, `scripts/regen_design_inventory.py --write` — computed, not typed; the steward's run after the merge finds
nothing left to change. The sentences of §10, §11.3 and §16 that say where the language control and the drawer's
script live follow the markup (the language control is included by `rail_nav.html`'s foot now).

**The weight.** `dist/portal/console.css` 22 461 → 29 207 B (4 235 → 5 167 B gzip); `dist/main.css` −58 B gzip (the
two patches). The console page type's CSS stands at **51 305 B gzip — +874 for step 2, 1 445 B over the Wave-1
ceiling of 49 860**; `dist/console.js` 1 938 → 2 037 B gzip. No image, no font, no new request; nothing animates at
load. No sheet outside the shell's still styles the console's chrome, so the bust rule's first remedy (DL54-15) has
nothing left to delete: the excess stands under the 2 KB the rule lets the CD grant once, after the Performance
Lead's measure on 8782 — which this step did not take. Under V5.5 it is reported, not hidden.

**Numbering.** Written on the family's branch as DL54-52, after step 1's DL54-39 … DL54-46 and step 2's DL54-47 …
DL54-51. W2-D's and W1-C's entries reached design-v5 first as DL54-39 … DL54-57, so the steward's merge of
11 October 2026 renumbered the family's fifteen entries DL54-58 … DL54-72 — content unchanged but for their
cross-references (DL54-73).

**Source.** Plan §2.2; §2.6; DL54-15; DL54-65.


## DL54-72 · 11 October 2026 · W3-A, the fix pass: a space starts where its rail does; a space's first page ends its trail on itself; the list's scroll edge is two named tokens

The decisions met while closing the family's one review (`QA/v54/w3-a/REVIEW.md`) and its accessibility and
performance check (`A11Y_PERF.md`). No variant was built and none is proposed.

1. **«Espace réservé» starts where its rail does** (REVIEW M1). `portal.services.shell_space` gives the space's
   `url` — the rail's mark, the phone's tile, the drawer's mark, the way back from «Espace entreprise» — to the
   first entry of «Mon rôle» for an account that holds a role's register (the dispatch desk for an operator or an
   administrator, the queue for a professional, the assigned processes for an authorised actor; a superuser is
   offered every register and starts at the rail's first, «Processus assignés»), and to the dashboard for every
   other account. One rule for the rail and its start (`_role_surfaces`), computed from the roles the caller has
   already read: no query is added. The person's dashboard stays one key away, under «Parcours»; W3-B gives staff
   a home of their own later. Not changed here, and said: the sign-in lands operators and administrators on the
   dashboard (`accounts.adapters`, whose order has no row for them), and the account menu's «Espace réservé» and
   the breadcrumbs' «Espace réservé» still lead to the dashboard on every producer.
2. **A space's first page ends its trail on itself** (REVIEW m3). «Espace réservé › Tableau de bord» and «Espace
   entreprise › Tableau de bord» — the word the rail lights — instead of a trail that ended on the space's name;
   the space's name is no link to the page one is on (`_render` of `portal.views` and `companies.views`: a root
   whose address is the request's is drawn as a word). The phone's top bar says the page. The h1 «ESPACE RÉSERVÉ»
   of the empty dashboards is W3-B's locked copy, as written.
3. **The list's scroll edge is two images named in `tokens.css`** (REVIEW m1). The review asked for the
   `background-attachment: local` pair; an app sheet draws no gradient (`tests/frontend/test_design_docs.py`, the
   rule W2-D's hero block follows), so the two images are tokens of the «console chrome» group —
   `--rail-scroll-edge` (transparent → the night's sheet, 24 px, fixed to the box's end) and `--rail-scroll-cover`
   (the rail's own night, 24 px solid under 16 px of fade, travelling with the list's end) — and `_shell.css` reads
   them. They are written into W1-A's group, beside `--rail-bg`, rather than in a block appended at the file's end:
   design-v5 appended W2-D's block there, and two blocks at the end of one file conflict at every merge. The band
   is lighter, not darker: the night's own shadow colour on notte-900 is 1.07 : 1 and says nothing; the sheet's
   is the rail's plate (1.30 : 1) and keeps every word of the rail at 4.72 : 1 or more. Under forced colours the
   browser draws neither image.
4. **Targets** (A11Y M1, m1). The console footer's three legal pages are 24 px tall at least, 44 × 44 under a
   coarse pointer (the footer grows by 24 px at 390, by 48 where its links wrap); the account menu's rows in the
   phone's top bar are 44 px under a coarse pointer — V4's menu stays until W2-A's popover replaces it.
5. **Two lines rather than an ellipsis** (A11Y m4). In the band (48–64rem) the account's name beside its glyph wraps
   instead of losing its end under a person's own text spacing. At 390 and 320 the check's «ellipsis» was the
   name's visually hidden box — below 48rem the glyph stands alone and the name is the trigger's word for a
   reader, with or without the spacing: nothing changed there.

**Paths outside the slice** (add to DL54-65 and DL54-71): `apps/portal/views.py` (no owner — its `_render` and the
dashboard's crumb, for item 2) and `static/css/v5/tokens.css` (W1-A — the two tokens of item 3, in the «console
chrome» group); `apps/companies/views.py` is already step 1's. **The weight:** the console page type's CSS +153 B
gzip (`dist/portal/console.css` 5 167 → 5 292, `dist/main.css` +28), 51 458 B on the family's base — 1 598 B over
the Wave-1 ceiling of 49 860 (DL54-71); on today's design-v5 the check's 50 479 B becomes about 50 632 (+772).
No image, font, request or animation is added.

**Numbering.** Written on the family's branch as DL54-53; renumbered DL54-72 by the steward at the family's merge
on 11 October 2026 — W2-D's and W1-C's entries hold DL54-39 … DL54-57 on design-v5 (DL54-73).

**Source.** REVIEW.md M1, m1, m3; A11Y_PERF.md M1, m1, m4; plan §2.2 (the serialized shared files, tokens.css);
DL54-65; DL54-71.


## DL54-73 · 11 October 2026 · Steward, the w3-a merge: the family's entries renumbered, the eleven paths assigned, the console page types' CSS ceiling as measured, the merge before W2-A

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w3-a` into design-v5 on 11 October 2026 —
what the family's own entries hand to the merge step: DL54-65, DL54-71, DL54-72; `QA/v54/w3-a/NOTES.md` «Review
fixes» and «What is left, and whose»).

1. **Numbering.** W2-D's entries with the record of its merge, and W1-C's thirteen, reached design-v5 first as
   DL54-39 … DL54-57, so the family's fifteen entries, written as DL54-39 … DL54-53 on its branch, are **DL54-58 …
   DL54-72** — the same order, add 19 —, content unchanged but for their cross-references and their two «Numbering»
   paragraphs (the pre-merge sync, `4394387`). The index gains the row of the fix pass's entry, which the branch had
   not written. The citations in code and in DS 2026 follow the new numbers (`dd74dac`: `_shell.css`,
   `portal_chrome.html`, the shell's two test files, §11.6); the family's notes, review and accessibility report keep
   the numbers they were written with, and the notes' closing section says how to read them — the «DL54-44» of
   `A11Y_PERF.md` and of the notes' «Review fixes» is design-v5's own, the record of the w2-d merge.
2. **The eleven paths outside the slice are this area's in the manifest.** `scripts/check_ownership.py w3-a
   design-v5` listed them; each was read in the diff, found to be what the family declares and written under w3-a as
   a slice (`5290459`) — DL54-65: the four rail producers that now ask the one builder (`apps/academy/views.py`,
   `apps/helpdesk/views.py`, `apps/selection/services.py`, `apps/companies/views.py`), the two keys of the icon
   registry (`apps/core/icons.py`) with the stand-in of W1-B's walk (`tests/frontend/test_icons.py`), the platform
   shell's legacy blocks deleted from `apps/portal/static/portal/portal.css` (W3-B's bridge part untouched); DL54-71:
   W1-A's two retired patches in `static/css/v5/base.css`, one filter of `tests/frontend/test_browser_w1_b.py`;
   DL54-72: the first page's crumb in `apps/portal/views.py`, the two scroll-edge tokens in the «console chrome»
   group of `static/css/v5/tokens.css`. The slices of `apps/portal/services.py` (the shell's builder, as written: the
   spaces, the audiences, the rails, where a space starts, the bottom bar) and of DS 2026 (§11.6 and the sentences of
   §2, §2.1, §10, §11.3 and §16 that follow the markup) are named as written. The check after it: 12 inside, 15
   slice, 17 generated, and the manifest itself, the one steward-only path (before: 11 outside).
3. **The console page types' CSS ceiling is recorded as measured.** On the bundles rebuilt from a clean dist at the
   merge, gzip −9: `dist/main.css` 42 452 B, `dist/portal/console.css` 5 292 B, `dist/portal/portal.css` 2 263 B —
   **50 007 B in the three sheets every console page loads** (the dashboard's total; «Mes pièces» adds
   `documents.css`, 1 172 B, unchanged by the area). At `v54/w1-c` — the last Wave-1 merge, so the «measured total at
   the end of Wave 1» from which plan §2.6 item 3 and DL54-15 ratchet — the same three sheets weighed 48 084 B
   (42 461 + 2 936 + 2 687): **the merge adds 1 923 B** (`console.css` +2 356, `portal.css` −424, `main.css` −9) and
   lands 147 B over the dashboard's Wave-1 allowance of 49 860 B. `dist/console.js` 1 676 → 2 038 B.
   - **§2.6 item 5 was not applied to this merge, as for the home (DL54-44 item 3), and that is said here rather than
     passed over.** The family took the bust rule's first remedy — the platform shell's legacy blocks left
     `portal.css` (DL54-65) and W1-A's two patches left `main.css` (DL54-71): no sheet outside the shell still styles
     the console's chrome, so nothing of its own is left to delete. The Performance Lead's measure on 8782 was not
     made: the compressed twin cannot be rebuilt while `collectstatic` refuses the console's raw entry (DL54-44 item
     4, still open on 10–11 October per the area's check). The area's accessibility + performance check
     (`QA/v54/w3-a/A11Y_PERF.md`, m3 and «Performance») measured the effect in production shape — the lane's
     compressed twin, profile A (150 ms RTT, 1.6 / 0.75 Mbps), CPU × 4, n = 9 cold loads per cell, against the W1-0
     before set — and found none to the worse: LCP 240–370 ms earlier on every traced cell (the dashboard, «Mes
     documents», the journey; fr and ar; 1440 and 412), the first-render task 30–65 ms where it was 258–500, the
     longest load task lower everywhere, CLS ≤ 0.0005; against the merge base on the same twin, the longest task
     within ± 35 ms and LCP inside the two series' spreads. The owner's V5.5 rule — «fix only real regressions,
     serious blocks, important long tasks, evident LCP/CLS problems. If performance is good and does not block UX:
     ship» — lets the area ship; the Creative Director raised nothing.
   - **What holds from here.** The console page types' ceiling is the three sheets as they weigh at this merge,
     **50 007 B**, plus a page's own sheet as it weighs at this merge. It does not rise: a Wave-3 family that adds to
     the console's sheets first deletes the legacy rules its components supersede, and a merge that would land over
     it comes back to this log first. `dist/main.css` stands 3 628 B under its 45 KB ceiling (46 080 B); the home's
     ceiling follows `main.css`'s, as DL54-44 item 3 says. Nothing pins these figures:
     `tests/frontend/test_css_budget.py` (plan §2.7) does not exist.
4. **The area merged before W2-A**, which plan §3.2 (W2-A → W3-A) and the manifest's `after` put first. The overlay
   system is not on design-v5 — W2-A has no branch — and the shell did not wait for it: the phone's top bar keeps
   V4's account menu (its rows 44 px under a finger), the drawer keeps today's `<dialog>`, and the notification
   centre and the console's account popover are not drawn (DL54-61, DL54-69; REVIEW m4). What W2-A's merge picks
   up, as a forward correction: the drawer onto the overlay system, the account popover, the notification centre
   (`apps/portal/static/portal/v5/_notifications.css`, which the manifest gives w3-a — the overlay family writes it
   with the shell's hand-over, through the steward).
5. **The account's disc at the rail's foot is drawn through the registry's `concept` filter.** The merge brought
   W1-C's O14 lint (`tests/frontend/test_o14_lint.py`, DL54-56): inside a status context — a rail is one — a symbol
   named by a variable must come from a registry map, visibly. The foot drew `{% svg_icon space.who_icon %}`, a glyph
   the producer already took from `icons.AUDIENCE` / `ACTOR` but that the lint cannot trace, and the lint failed on
   the merged tree — the targeted run's one red. Both areas are kept (`56be416`): `portal.services._AUDIENCES` and
   `_audience()` carry the registry's concept (domain, key), `shell_space()` adds `who_domain` and `who_key` beside
   `who_icon`, and the template draws `space.who_key|concept:"actor"` or `|concept:"audience"` — the filter the
   lint reads and `test_the_registry_keeps_the_check_out_of_every_status_map` guards. The symbol drawn is the same
   for every account; the lint is unchanged.

**Why.** Fifteen entries under numbers other families already hold would make every citation ambiguous; eleven paths
nobody holds would have no writer for the next family; and a ceiling that is exceeded and not written down is a
ceiling nobody holds. The plan's own remedy for the weight cannot be applied today, and the directive that lets the
area ship asks that only real regressions stop it: the record says which rule gave way, on what evidence, and what
number the next merge is held to. A lint that the merge turns red is a conflict like any other: resolved by keeping
both areas' work — the lint as written, the shell drawing the same symbol through the registry.

**Source.** The owner's V5.5 directive (5 October 2026, 14:32: «PERFORMANCE», «SHIP THE PRODUCT»); plan §2.2 (the
manifest: the steward assigns; the serialized shared files), §2.6 items 3 and 5, §3.2; DL54-15; DL54-44 items 3
and 4; DL54-56 (the O14 lint); DL54-65, DL54-71, DL54-72; `QA/v54/w3-a/REVIEW.md` m4, m5; `QA/v54/w3-a/A11Y_PERF.md` m3 and «Performance»;
the weights measured on `v54-w3-a` after the pre-merge sync and `npm run build` from a clean `static/js/dist` and
`static/css/dist`, and on design-v5 at `3c288d6` (the static tree of `v54/w1-c`, `e0a5004`, unchanged since).

## DL54-74 · 9 October 2026 · W2-B: the stage of «Il varco» as built

**Decision.** Built by W2-B (step 1, the stage) on plan §1.13 and §1.9, with these choices met during the build (plan
§5.2: one entry, its reason, its evidence):

1. **Three lights, from the floor to the door, each a function of the form.** The e-mail field's focus lights the four
   ways (`is-ways`); a valid address holds the threshold — its line, the pool at the steps' foot, the three steps
   (`is-held`); the password's focus, or a typed password, lights the door's frame (`is-frame`); on the sign-in's submit
   the stage's key turns once and holds. The plan's «the routes hold lit» is the second state: it is drawn as the light
   reaching the threshold, so that the scripted person of L7 leaves three states that can be told apart in a capture at
   t = 10 s. A state is what the form holds and where the person is — never a memory: clearing the address or leaving
   the form gives back the state of what is left, in `--motion-standard`, without travel.
2. **The plan's «600 ms» is a sequence on the tokens.** A pass is `--motion-slow` (480 ms: the lights run in, the ways
   are drawn behind them, the frame's light rises) and, for the ways, `--motion-fast` (120 ms: the beads go out where
   they arrive). No duration is added (§1.5), as W1-D read «260 ms» and «480 ms» (DL54-37 items 3, 5). The steps take
   the light `--motion-stagger` apart. Every pass has a `from` keyframe only and ends on the element's own state: no
   fill stays in effect, and `document.getAnimations()` is empty once it has ended.
3. **An address being typed is read at the person's pause** (`--motion-wait`, a threshold): «a@b» is valid and «a@b.»
   is not, and a light that followed the field's validity on every keystroke went on at «…@e», off at «…@example.»
   and on again 60 ms later (lane 7, the scripted person of L7, before this rule). A cleared field and a field that is
   left answer at once.
4. **The arrival is said to a person who arrives.** Once, after a largest-contentful-paint entry and the photograph's
   decode, from 64rem: never on a refused sign-in's page (the plan), and never on a page reached from another entrance
   page — after the key has turned, the second factor's page does not greet again — nor from history, nor under
   reduced motion. Its four lights are `--motion-route-light` each, `--motion-route-stagger` apart: 2.4 s.
5. **The sign-in's forms name the stage through the layout's own form element.** allauth looks for
   `allauth/elements/form__entrance.html` before `form.html` on the entrance layout: that element is the product's form
   plus `data-loader-host` on the forms that complete a sign-in — the login, and the second factor's code
   (`mfa/authenticate`), whose submit is the one the console answers: for an account with a second factor the engage
   and the release (DL54-07) are one movement only if that submit turns the key. A project `account/login.html` that
   restates allauth's template was not written for this: the catalogue audit refuses a msgid the project does not own
   («Sign In» is allauth's), and the form's step can extend allauth's own template instead of copying it.
6. **No words of a long wait yet.** `word`, `slow` and `retry` (DL54-37 item 6) have no live string: «Ouverture…»,
   «C'est plus long que d'habitude.» and «Réessayer» are CDV §17's proposal, O32 of the owner's copy packet (B1), and
   Arabic is never written by us. The host engages without them; with no «Réessayer» on offer the lease gives the form
   back at 10 s (DL54-37, second addendum, a). The day the three strings exist they are one include in the layout.
7. **In the source the focus precedes the stage, and every part is placed** (L6, m9): after the skip link the next stop
   is in the form, and the help line's address follows the form's action. The sheet places the two on grid lines and
   holds the stage's place before the stage is parsed — its column from 64rem, the band's row below — because a slow
   browser paints in between: left to the order of the source (`order: -1`) the form was drawn in the stage's column
   and moved when the stage arrived, 0.446 of layout shift at CPU ×4 (0 at ×1); placed, 0. For the same reason the help
   line is written before the scene and the door before the floor that hangs from it, and the night of the stage's
   place is painted by the page's own box (`.varco::before`, in the stage's cell): in that paint the place is already
   the niche's night, not the page's light ground turning dark a frame later. Every part names its cell in full,
   column and row — a part left to auto-placement steps aside from that ground into a column of its own.
8. **The promoter's line stays in the letterhead.** The comp's foot line stood in for a focused letterhead; the product
   keeps the public letterhead on the entrance, whose utility bar carries the line in the same column. Printing it
   twice on one screen would be a repetition, not a signature. The colophon is the help line.
9. **The block is `.varco`.** V1's `.entrance` — the four entrances of `components.css` §12, W2-E's to delete — was
   reaching the layout's section: a background on `:focus-within`, with its transition, every time a field took the
   focus. §27's `.account-page--entrance` (the narrow container) is deleted with it.
10. **The door stage in `_door.css`.** The vector parts are the stage as drawn; the photograph is an `<img>` in a box of
    the arch's shape (it can take the door-master derivatives' `srcset` when `static/brand/v5/` reaches design-v5 with
    W2-D: the 400 px file is soft at a device scale of 2); the key is `key.svg` shape for shape, gold bow and navy eye,
    on the loader's `.sig__l` / `.sig__turn`; the stage is `direction: ltr` and so is the scene — the ways are part of
    the drawing, Persona on its left in every language. The door's two lights are switched by `--door-frame` and
    `--door-steps`. From 64rem the door is 15.5–26rem wide (the photograph is never upscaled at 1×).
11. **On a long page the set stays in sight** (the signup): the scene and the help line are sticky under the pinned
    letterhead, and the niche's shadows have fixed depths.
12. **One correction to the V4 form ahead of its step**: in Arabic the room kept for the password's show / hide control
    is on the control's side. The field stays `direction: ltr` there (`base.css`: a password is typed left to right)
    while the control sits at the field's end, the left; `padding-inline-end` alone kept the room on the right, and the
    placeholder and the typed password ran under «إظهار كلمة المرور» — at 390 px the placeholder at once and a typed
    password from its fourth character, on V4 as on V5. The entrance's sheet now keeps the room on the input's own
    start side under `[dir="rtl"]`. The same rule of `v4/buttons.css` serves the password fields of the other layouts
    and is W1-C's.
13. **The stage's paints are a page-only partial, `static/css/v5/_varco.css`** — a second path outside the slice. Its
    gradients (the niche's shadows, the wall's reveal, the threshold, the pool, the ways and their light) were first
    written as paint tokens in the family's block of `v5/tokens.css`, because an app sheet may write no gradient: there
    they rode in `main.css` on every page of the site — 579 B gzip, measured — and put the home, an interior page and
    the dashboard over their ceilings for the login's picture. DL54-15's bust rule («moves page-specific rules into
    page partials») is applied instead: the block keeps the door's four literals and five colours; the partial, which
    the entrance imports after `_door.css`, composes the gradients from them with `color-mix(in srgb, … N%,
    transparent)` for an alpha. `main.css` is 114 B gzip above design-v5 instead of 638; the stage's pixels are the
    same to one level in 255 (two in under 0.1 % of them).

**Why.** V54 l.18 («left: route lights, doorway, richer motion, depth») and V5.5 («more motion and light on the left»),
inside the plan's laws: nothing loops, only transform and opacity move, the keyboard never animates, reduced motion is a
state, and the light never says more than the form does.

**Source.** Plan §1.5, §1.9, §1.13 (L6, L7, L8, L10, L11), §2.3, §2.5, §2.6, §3.4 item 2; DL54-07, DL54-08, DL54-13,
DL54-15, DL54-37; `docs/design-v5/QA/v54/w2-b/NOTES.md` step 1, with the measures. Written on W2-B's branch as DL54-39, renumbered DL54-52 when the core components' entries (DL54-39 … DL54-51)
reached the branch first, and DL54-58 when design-v5 renumbered those entries DL54-45 … DL54-57 (the w1-c merge), and DL54-74 at the w2-b merge, where
the console shell's entries and their merge (DL54-58 … DL54-73) were on design-v5 first.

## DL54-75 · 10 October 2026 · W2-B: the form of «Il varco» as built

**Decision.** Built by W2-B (step 2, the form) on plan §1.13, on the core components' fields «la lastra» (W1-C), with
these choices met during the build (plan §5.2: one entry, its reason, its evidence):

1. **The form is a column on the paper, hung from the top of its panel.** No card (CDV §18: «no floating SaaS card»):
   one column of 25rem on the page's own ground, centred in the 7 / 12 panel. From 64rem its distance from the
   letterhead is `clamp(3rem, 14vh − 1rem, 12rem)` — a function of the screen, never of the form's height — so the
   title stands at the same height on every entrance page, level with the top of the arch beside it, and a browser
   that paints before the whole column is parsed draws every line where it stays. The V4 sheet was centred on its own
   height and was the one source of layout shift left on the page (step 1: up to 0.05 at CPU ×4); the form gives none
   now, and what still moves on the page is the public navigation's (≤ 0.02) and, in one load of forty, the stage's
   help line (0.0007: it is centred beside the door, and takes its second line). The same rule holds inside the column:
   **no part waits for a later one to know its place.** The eyebrow's row has its line's height before its words are
   parsed (its key is written first: in one load of forty a paint came between the two, and the key stood 3 px
   higher), and the label row's link has the label's own type and line in every language (in Arabic its taller line
   made the row 2 px taller when it arrived, under a control already drawn). A test takes the later parts away, one
   by one, and asks the others where they stand.
2. **One hierarchy on every entrance page, written by the layout.** The eyebrow, ONE title (28 / 36, 36 / 44 from
   48rem), the page's sentence at 17 / 28, the fields, ONE primary action, then what is quiet. The eyebrow is
   «Espace réservé» with **`ile-key`**, not `ile-steps` as §1.13 wrote: the icon registry (W1-B, built after the plan:
   one concept, one glyph) gives the key to «Espace réservé» and the steps to the journey, and the letterhead's plate
   («la targa») says the same words with the same key. A page that is not a form — «a message has been sent», a link
   that has expired, an inactive account, too many requests — ends with the way back to the sign-in («Se connecter»,
   a string of the product), for a person who is not signed in; a form never carries it.
3. **The sign-in's page extends allauth's own template.** `templates/account/login.html` is `{% extends
   "account/login.html" %}` — Django resolves the same name in the next template directory — and its content is
   `block.super`: the view, the form, the field names, the CSRF token, the redirect field and the passkey and code
   blocks are allauth's at the installed version, never a copy; its words stay messages of allauth's catalogue (the
   project's catalogue audit refuses a message the project does not own — DL54-74 item 5).
   What the page adds is the assurance (item 9).
4. **`account/password_reset_help_text.html` is not written.** The plan put the reset link in the label's row through
   that override «plus a `form_field.html` slot». allauth already renders exactly that link when the template is
   absent — its own message («Forgot your password?»), from its own catalogue, in the four languages — and a project
   template could only restate a message the project does not own. The slot alone moves it: `LoginForm` marks the
   password field `help_beside_label`, and `form_field.html` writes that field's help as the `form-field__aside`,
   under the help's own id (the field is still described by it).
5. **The link is written after the control and placed in the label's row.** In the source the order is the address,
   the password, its show / hide control, the reset link, the action — the keyboard's order: a person who types the
   address and presses Tab reaches the password, never a link. The sheet places the aside at the end of the label's
   row (the field becomes a grid, `:has(> .form-field__aside)`); where `:has()` is not understood the link stands
   under the control, as a help text does.
6. **`LoginForm` is allauth's form with its presentation only** (`ACCOUNT_FORMS["login"]`). It overrides no method of
   the sign-in — a test holds that, member by member. Its constructor changes what the two widgets say: no
   placeholder (LG-3), `inputmode="email"`, `autocapitalize="none"`, `spellcheck="false"`, `dir="ltr"`;
   `autocomplete` stays allauth's (`email`, `current-password`). After a refusal that names no field — «the address
   or the password» — its bound field (`RefusalBoundField`, Django 5.2's `bound_field_class`) puts the error
   summary's id first in each field's `aria-describedby`, before the ids Django writes; neither field is marked
   invalid, so neither carries the error's edge (L4). The project's own `SignupForm` drops its placeholders too (the
   core components' review handed them to this family); the other entrance forms are allauth's classes — the reset,
   a new password, the second factor's code — and keep the attribute in their markup: on the entrance the sheet does
   not draw it. Removing it there, and giving the code its numeric keyboard, is `ACCOUNT_FORMS` / `MFA_FORMS` again —
   a second setting, outside this family's slice (one setting): left to the review.
7. **«The button holds the key» is said by the forms that complete a sign-in.** On the login and on the second
   factor's code — the forms that name the stage (`data-loader-host`) — the primary carries, at rest, the very key
   the loader turns when it is busy: the same mask, the same 18 px box, the middle of the same end pad (a test holds
   the two sheets to one mask). Its two pads are the plate's own height (52 px), so the label stays centred on the
   plate. On submit `loader.css` turns that pseudo-element once and dims it: the label does not move by a pixel (L8),
   and the wait begins with the key the person was looking at. Every other entrance primary is the system's large
   primary, and gets its key only while it waits. Flat in every state (L14): the fill, its edge and the press are
   `v5/buttons.css`'s; this sheet writes no background, no shadow, no gradient on it.
8. **Too many requests is one template with two parents.** `templates/429.html` extends the entrance layout for a
   person who is not signed in — the limits of the sign-in, the signup, the reset and the verification e-mail are
   reached at the entrance — and the product's error page (`errors/429.html`, through `block.super`) for a signed-in
   one, who met the limit on an account page. Its two sentences are that error page's, word for word. The limit on
   failed sign-ins is not a 429: allauth says it in the form, and the reset link is in the password's row.
9. **The assurance is the FAQ's locked answer, quoted as the home quotes the FAQ.** Under the action, after a
   hairline: the question as a heading set as a label, the answer verbatim (15 / 24), then the FAQ's own link —
   after the locked text, never inside it. It is read from the locked registry behind the Phase-3 gate
   (`gates.phase3_public`), with `lang` when the registry holds it in French only (`pages.services.faq_entry` does
   the same for the home's quotes); it does not read the FAQ row's publication state. CDV listed it for the owner
   (O44, «yes»); plan §1.13 lists it in the hierarchy.
10. **A session message belongs to the form's column.** `templates/base.html` writes the messages before the
    entrance, as a band across the page: the stage then began under it and the two panels no longer met the
    letterhead. With `:has()` and subgrid the page's `<main>` becomes the grid whose lines the entrance takes: the
    stage keeps the reading edge for the page's whole height and the message stands above the eyebrow, hung where the
    form hangs; below 64rem — the band, the message, the form. Without them the message stays a band above, as
    before. The base template is not this family's and is untouched.
11. **When a form comes back with errors the document's title says so first** («Erreur — Connexion · …»: L4), on
    every entrance form, with the product's own word. The refusal's summary keeps the system's notice; its list of
    fields, empty when the refusal names none, takes no room on the entrance and is not announced as a list of
    nothing (`:not(:has(li))`).
12. **A mark that says nothing is not drawn.** When every field of a form is required the asterisks carry no
    information: the sheet draws none (`.form:not(:has(.form-field:not(.form-field--required)))`); the inputs keep
    `required`, and a form with one optional field keeps all its marks.
13. **The show / hide control is a glyph on the entrance, until it is the system's.** Plan §1.13: «one channel
    (`aria-pressed` + the existing live label string); the glyph swaps at once; the caret is kept». The control's
    words («Afficher le mot de passe», 162–176 px inside the plate) left twelve characters to a password at 360 px
    (LG-2), and no shorter live string exists. `form_field.html` takes an argument, `reveal="glyph"` — the
    registry's `eye` / `eye-off` in a 44 px target, the live string as its one name, `aria-pressed` its one
    channel, the reserve the plate's own height with its RTL twin — which the entrance asks for on every one of its
    forms (`allauth/elements/fields__entrance.html`); `shell.js` §3 keeps the caret (a pointer's press hands the
    focus back to the field with its selection; pressed from the keyboard the control keeps the focus) and swaps no
    words on the glyph control. The core components' review, the same evening, asked the same control of the system
    (its M2): when W1-C's fix has drawn it in `v5/field.css`, the argument, the element and this sheet's two rules
    go, and the kept caret stays. **Done at the w1-c merge (11 October):** the system's glyph (`v5/field.css` §5) is
    the control on every page; `reveal`, `fields__entrance.html` and the sheet's rules are gone; `shell.js` §3 keeps
    the caret; without script the entrance does not draw the control (it would do nothing; `entrance.css`).
14. **This sheet draws no control.** W1-C's guard (DL54-50, `test_components_w1_c.py`: no rule of `entrance.css` on a
    field's input, select or textarea) is kept, and the form's own test holds it too: what the entrance adds to a
    control is said of the form (the caret's colour, inherited; no placeholder drawn), of the field's parts (the
    control of a field with an aside is «what is neither the label, nor the aside, nor the errors»), or of what a
    control is for (a one-time code, found by its `autocomplete`).
15. **The core components came through their family's branch.** `v54/w1-c` was not on design-v5 when the step began
    nor two hours later (W1-C: SHIP_AFTER_FIXES, its fix pass ahead); on design-v5 alone the form can be neither
    measured nor tested. The form was built on a throwaway merge with `v54-w1-c`, and at the two hours the reviewed
    branch (`7e867e4`) was merged into this one (`75c1ba1`) so that the family's next steps look at what will ship.
    design-v5 is merged again once it carries the tag; the notes list what meets there.
16. **The raw entry and the production storage: found, and handed to the merge.** `collectstatic` under
    `CompressedManifestStaticFilesStorage` stops on `apps/accounts/static/accounts/entrance.css`: step 1's two imports
    of its partials (`../../../../static/css/v5/_door.css`, `_varco.css`) leave `STATIC_ROOT` once the raw entry is
    collected beside its bundle — the defect design-v5 records for the console's entry (the steward's entry on the
    w2-d merge, item 4), found there at the end of this step and run here on this branch (it passes with the two raw
    entries left out). It is not corrected in this family: the correction is either the build's (a build-only entry,
    or imports written in the static namespace with a resolver in `scripts/build_css.mjs` — the steward's file, and
    the one correction that also lets `hero.css` import the door) or the end of the shared door (the partials moved
    beside their importer). Nothing a person sees depends on it; a deployment does.

**Why.** V54 l.18 («form: custom premium fields, focus states, micro-interactions, hierarchy, refined surfaces,
stronger CTA») and V5.5 («a more premium form; better inputs, focus, CTA and states»), inside the plan's laws: paper
carries a hairline and no light, every primary is flat, the form's motion is the system's, and the page says nothing
the product does not already say — live strings only.

**Source.** Plan §1.4, §1.6, §1.7, §1.8, §1.13 (L1–L6, L8, L11, L12, L14), §2.2, §2.5; CDV §18; DL54-13, DL54-50,
DL54-74; the core components' review (`docs/design-v5/QA/v54/w1-c/REVIEW.md`, M1–M3);
`docs/design-v5/QA/v54/w2-b/NOTES.md` step 2, with the measures. Written on W2-B's branch as DL54-53, renumbered
DL54-59 when the branch met the w1-c merge, and DL54-75 at the w2-b merge (the console shell's DL54-58 … DL54-73 first).

**Fix pass (11 October 2026).** After the senior review (`QA/v54/w2-b/REVIEW.md`) and the accessibility + performance
check (`QA/v54/w2-b/A11Y_PERF.md`), both SHIP_AFTER_FIXES, by the family's fix pass (label w2-b-fix), with these choices
met on the way (finding, change and evidence in the notes, «Review fixes»):

17. **The stage's photograph is the home's set** (REVIEW M1, the check's F1): `<picture class="door-stage__photo">` with
    the `static/brand/v5` AVIF (400–1200 px) and WebP (400–960 px) sources — the same registration as V4's single 400 px
    file, which was stretched 1.4–1.8× on a dense screen. Its `sizes` says the photo box, 320 / 368 of `--door-w`, the
    WIDEST it is drawn in each range: each `clamp()` of the sheet is cut where its middle term meets a bound and written
    as plain lengths in media conditions, as the home writes its own (`calc()` only: `clamp()` inside `sizes` is not
    assumed of every engine). The preload is that AVIF source, character for character, so one file is fetched: 400 at
    1×, 576 at 2× on a laptop, 800 on a large desktop at 2×, 400 on any phone. A browser test holds the sizes to the box
    across all nine lines.
18. **A shown password is still a secret** (REVIEW M2): when the system's show / hide control is wired, `shell.js` §3
    tells the field it can show `spellcheck = false`, `autocapitalize="none"`, `autocorrect="off"` — every revealable
    password of the site, the sign-up's and the new password's included, at once; without script there is no reveal.
19. **The sign-in's address says `username`** (REVIEW m5) — allauth writes `email`. It is the sign-in's identifier:
    password managers and a phone's suggestion bar key a saved credential on `username`, and `email` can offer the
    person's contact card instead. Both are input purposes of WCAG 1.3.5. This supersedes acceptance L3's «`email`»
    (`surfaces.md` §2.4), whose point was the right purpose and no placeholder; the password stays `current-password`.
20. **The assurance's locked answer only where the registry holds the page's language** (REVIEW m3): a French
    paragraph under the action of an Italian, English or Arabic page read as a missing translation exactly where it is
    meant to build trust. There the page keeps the FAQ's own link alone, in its language; the paragraph comes with the
    translation, by itself. The home's quotes keep the product's locked-text fallback (another page, another purpose).
21. **allauth's other entrance forms change their presentation only** (REVIEW m4, the check's A3):
    `accounts.forms.ResetPasswordForm` and `ResetPasswordKeyForm` under the same setting (`ACCOUNT_FORMS`) write no
    placeholder; `AuthenticateForm` under **`MFA_FORMS` — a second setting in `config/settings/base.py`, written for the
    steward's agreement at the merge** — writes none either and gives the code the digits' keyboard: both codes it takes
    are digits (the authenticator's six, allauth's recovery codes eight, 65.19.4). Declining it is one line: the code
    keeps its «Code» placeholder, which the sheet does not draw.
22. **The grain is the niche's only** (the check's P2): on a phone's band its 246 B file was the page's largest
    contentful paint (9 loads of 9 in French), which acceptance L9 names as what LCP must not be. From 64rem the grain is
    unchanged (no LCP candidate there: a small file over a large area); the band keeps the arch only, as §1.13 says.
23. **The key's mask is one token** (the check's P1): `--key-mask` in this family's block of `v5/tokens.css`, read by
    `v5/loader.css`'s busy key and by the entrance's primary at rest — one key, written once (−220 B gzip on the login's
    sheet). `loader.css` loses its declaration and W1-D's rule test reads the token: two paths outside the slice, for
    the merge step to write into the manifest. The login's CSS is then 47 477 B on the wire (−151 B), 1 783 B over its
    Wave-1 ceiling (45 694 B): the merge step records the page type's ceiling on these measurements and the check's — the
    one raise of ≤ 2 KB of §2.6 item 5.
24. **Each of the door's switches is set on the layer it lights** (the check's P3): `--door-frame` on
    `.is-frame .door-stage__frame`, `--door-steps` on `.is-held .door-stage__step` — no longer on the stage's root,
    where every element of the stage inherited them: the Tab into the password restyled 206 elements, 136 now (127 with
    the stage's classes held still), in no more style time than with them held. `_door.css` keeps drawing the
    lights from its switches (each step's opacity, the order, the stagger), and an app sheet reads none of its
    internals (the design documents' token guard).
25. **From 64rem the niche meets the footer** (REVIEW m1): one night, as the home's last chapter meets it; the footer's
    80 px of air stays below 64rem, where the form's paper is above it.
26. **The arrival lights each way behind its light** (REVIEW m2): the lit way drawn from the night as the light runs and
    given back as it arrives (`varco-draw` and `varco-glint` on the light's own clock: same tokens, same 2.4 s, once).
    Four beads on grey hairlines read as sparks to a person who has not acted yet; the lit way is the light the e-mail
    field will call. Transform and opacity only, on the layers the focus pass already moves.
27. **The small targets around the form** (the check's A2): the help line's address takes its 44 px band at every
    pointer (§1.13: «the help link, with a 44 px target»), the assurance's link the reset link's device (24 px, 44 under a
    finger), the invitation's link the 44 px band under a finger, and a link under the action («Annuler», 28 px in
    allauth's Arabic) is 44 px wide under a finger with its words at the column's start.

What the fix pass does not do: the production `collectstatic` on the raw entry (DL54-75 item 16; REVIEW M4, the check's
C1) is the steward's one correction for this entry and the console's — unchanged here, and still the deployment's
blocker.

## DL54-76 · 11 October 2026 · Steward, the w2-b merge: the family's entries renumbered, the five paths assigned, `MFA_FORMS` agreed, the login page type's CSS ceiling as measured, every page type's 79 B, the door's two forward corrections left

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w2-b` into design-v5 on 11 October 2026 —
what the family's own entries hand to the merge step: DL54-74 items 5 and 13, DL54-75 items 16, 21 and 23;
`QA/v54/w2-b/NOTES.md` «For the merge», in its four versions).

1. **Numbering.** W3-A's fifteen entries and the record of their merge reached design-v5 first as DL54-58 … DL54-73,
   so the family's two entries — the stage, written DL54-39 on its branch, then DL54-52 and DL54-58; the form, DL54-53,
   then DL54-59 — are **DL54-74** and **DL54-75** (add 16), content unchanged but for their cross-references and their
   numbering sentences (the pre-merge sync, `041e056`). The index keeps design-v5's rows, then the family's two. The
   code and DS 2026 cite none of the moved numbers; the family's notes, review and accessibility report keep the
   numbers they were written with, and the notes' closing section says how to read them (`d7d0499`).
2. **The five paths outside the slice are this area's in the manifest** (`dcf3269`). `scripts/check_ownership.py w2-b
   design-v5` listed them; each was read in the diff and found to be what the family declares:
   `static/css/v5/_varco.css` (whole: the stage's gradients as a page-only partial that `entrance.css` imports after
   `_door.css`, DL54-74 item 13); `templates/allauth/elements/form__entrance.html` (whole: allauth's `form` element on
   the entrance layout — `form.html`'s markup plus `data-loader-host` on the sign-in's forms, DL54-74 item 5);
   `static/js/src/shell.js` §3 (a slice: the kept caret, the keyboard's press, a revealable password never spelled nor
   corrected — DL54-75 items 13 and 18; the file stays W2-C1's); `static/css/v5/loader.css` §3 and
   `tests/frontend/test_loader_rules.py` (slices: the busy key reads the one token `--key-mask`, DL54-75 item 23; the
   files stay W1-D's). Three slices are named as written: `apps/accounts/forms.py` (allauth's entrance forms with their
   presentation only, and the sign-up's presentation), `config/settings/base.py` (item 3), DS 2026 (the entrance's prose
   and its four rows in §2.1, §10, §12 and §16). The check after it: 15 inside, 11 slice, 17 generated, and the two
   steward-only paths the steward writes itself — the manifest, and the capture report regenerated on the new login
   (`2bac1bc`: the same 43 captures, two more icons on each of the login's thirteen; DS 2026 §13 follows) — (before:
   5 outside).
3. **`MFA_FORMS` is agreed** — a second setting, where plan §2.2's serialized table gave the family one
   («`config/settings/base.py` | W2-B only (one setting: `ACCOUNT_FORMS`)»). `accounts.forms.AuthenticateForm` is
   allauth's second-factor form with its constructor only — no placeholder, `inputmode="numeric"` (both codes the field
   takes are digits) —, held by `apps/accounts/tests/test_login_form_w2_b.py`; authentication, validation and the rate
   limit stay allauth's. Declining it was one line, and the code would have kept a placeholder that the sheet does not
   draw and that assistive technology reads. The re-authentication's two forms (`ACCOUNT_FORMS["reauthenticate"]`,
   `MFA_FORMS["reauthenticate"]`) still write allauth's placeholder: the same one-line subclass, not asked by the review
   — left for the next pass on the entrance.
4. **The login page type's CSS ceiling is recorded as measured.** On the bundles rebuilt from a clean dist at the merge,
   gzip −9: `dist/main.css` 42 531 B, `dist/accounts/entrance.css` 4 861 B — **47 392 B in the two sheets every entrance
   page loads**. At `v54/w1-c`, the end of Wave 1 from which plan §2.6 item 3 ratchets (DL54-73 item 3), the same two
   sheets weighed 43 443 B (42 461 + 982): **the merge adds 3 949 B**, and lands 1 698 B over the login's Wave-1
   allowance of 45 694 B (DL54-44 item 3). `dist/entrance.js` is new (1 663 B gzip: one more script request, on the
   entrance pages only); `dist/shell.js` 1 033 → 1 131 B, on every page.
   - **§2.6 item 5 is not what is applied, and that is said here rather than passed over.** The family asked for its
     one raise of at most 2 KB, measured against the Wave-1 allowance (1 783 B over on the wire, `NOTES.md` «Review
     fixes»); measured against the end-of-Wave-1 total — the ceiling item 3 names — the merge adds more than 2 KB, and
     the Performance Lead's measure on 8782 was not made (item 6: the compressed twin cannot be rebuilt while
     `collectstatic` refuses the raw entries). The family took the bust rule's remedies first: `components.css` §27's
     entrance rule deleted, the V4 form rules replaced by the system's fields, the stage's paints moved into the
     page-only partial `_varco.css` (as tokens they weighed 579 B on every page), the grain on the niche only, the key's
     mask written once (−150 B). The area's accessibility + performance check (`QA/v54/w2-b/A11Y_PERF.md` «Performance»:
     the lane's compressed twin, profile A, CPU × 4, n = 9 cold loads per cell, against the W1-0 before set) found
     nothing to the worse — LCP 220–320 ms earlier in all four cells, the first-render task 46–85 ms where V4's was
     384–485, LCP ≤ 2.5 s, CLS ≤ 0.023 and all of it the navigation's —, and the fix pass's A/B (n = 10 per cell and
     arm) found no timing worse with significance. As for the home (DL54-44 item 3) and the console (DL54-73 item 3),
     the owner's V5.5 rule lets the area ship; the Creative Director raised nothing.
   - **What holds from here.** The login page type's ceiling is its two sheets as they weigh at this merge,
     **47 392 B**. It does not rise: a merge that would land over it comes back to this log first. `dist/main.css`
     stands 3 549 B under its 45 KB ceiling (46 080 B). Nothing pins these figures: `tests/frontend/test_css_budget.py`
     (plan §2.7) does not exist.
5. **Every page type carries 79 B more, and the console's ceiling moves with them.** `dist/main.css` is 79 B heavier
   than design-v5's (42 452 → 42 531 B): the door stage's named block in `v5/tokens.css` (plan §2.2 «W2-B the door
   stage's»; §2.3: a page partial's literal colours are tokens) — its four door colours and five light colours — and the
   key's mask, which left `v5/loader.css` for that block (one copy where there were two). Every page loads `main.css`:
   an interior page 42 452 → 42 531 B, the home 57 103 → 57 182 B (1 955 B under its ceiling of 59 137 B, DL54-44 item
   3), the console page types 50 007 → **50 086 B** — 79 B over the ceiling DL54-73 item 3 recorded this morning, which
   asks that a merge landing over it come back to this log first. The block is the plan's own, and nothing else of this
   area reaches a console page: **the console page types' ceiling is 50 086 B from here**, and it does not rise
   otherwise.
6. **`collectstatic` under the production storage still fails, now on two raw entries** — W1-D's console entry (DL54-44
   item 4) and this area's (DL54-75 item 16; `REVIEW.md` M4; `A11Y_PERF.md` C1):
   `apps/accounts/static/accounts/entrance.css` imports `../../../../static/css/v5/_door.css` and `…/_varco.css` and
   draws `url("../../../../static/img/grain.svg")`, paths of the source tree that leave `STATIC_ROOT` once the raw entry
   is collected beside its bundle (`SuspiciousFileOperation`). Not corrected at this merge: the one correction for both
   entries — the imports and the `url()` written in the static namespace with an `import-rule` resolver in
   `scripts/build_css.mjs`, or the raw entries kept out of `collectstatic` — touches the build script and the console's
   entry, neither this area's, and no page depends on it: the templates, the preview, the lanes and the tests load the
   bundles through the plain storage. It is a deployment blocker for design-v5 as a whole, open since DL54-44, to be
   settled before the integration milestone (plan §2.9).
7. **DL54-44 item 2's two forward corrections are left, with the reason.** That entry kept two things «for the merge that
   brings `_door.css`» — this one. (a) `apps/pages/static/pages/css/hero.css` importing `_door.css` and dropping its
   copy of the stage: that import is of item 6's kind — a third raw entry the production storage would refuse — and the
   hero draws the stage with its own markup in stage units, scoped to `.he`; a forward correction for the hero's family
   once the static-namespace import exists. (b) `static/css/v4/hero.css` leaving `main.css` «with its last consumer»:
   on the entrance `_door.css` restates every declaration that reaches the stage's parts but three — the door group's
   `pointer-events` (its `svg` already has it), the steps' transform box and origin, the arch's dash offset (inert
   without a dash) —, but the home's key still carries the class `doorway__key`, to which the sheet gives a transform
   box and origin, and `tests/frontend/test_v5_tokens.py` names the sheet. It leaves `main.css` (≈ 0.6 KB gzip on its
   own, on every page) in one measured pass on both pages — the entrance at rest and in its states, the home's key
   turning, fr and ar — with `templates/components/doorway.html` (included by no page since this merge, DS 2026 §10)
   and its section; the deletion map gives the file to W2-D, and the pass lands through the steward.

**Why.** Two entries under numbers W3-A already holds would make every citation ambiguous; five paths nobody holds would
have no writer for the next family; a second setting nobody agreed to is a setting nobody holds; and a ceiling that is
exceeded and not written down is a ceiling nobody holds — the console's included, which this merge moves by the plan's
own token block. Deleting a sheet that still reaches two flagship pages, or adding a raw entry the production storage
refuses, is not a merge step's work: the record says what is left, why, and who takes it.

**Source.** The owner's V5.5 directive (5 October 2026, 14:32: «PERFORMANCE», «SHIP THE PRODUCT»); plan §2.2 (the
manifest: the steward assigns; the serialized shared files), §2.3 («Page-only CSS»; the deletion map), §2.6 items 3 and
5, §2.9; DL54-15; DL54-44 items 2, 3 and 4; DL54-73 item 3; DL54-74 items 5 and 13; DL54-75 items 13, 16, 18, 21 and
23; `QA/v54/w2-b/REVIEW.md` M4; `QA/v54/w2-b/A11Y_PERF.md` P1, C1 and «Performance»; `QA/v54/w2-b/NOTES.md` «For the
merge» (step 1, step 2, the resumed step, the fix pass); the weights measured on `v54-w2-b` after the pre-merge sync and
`npm run build` from a clean `static/js/dist` and `static/css/dist`, against design-v5 at `1c001e6` and at `3c288d6`
(the static tree of `v54/w1-c`).

## DL54-77 · 11 October 2026 · Steward, the static pipeline: imports written in the collected tree, the guard, CI's lint, the fresh-clone checkpoint

**Decisions** (the steward's, for the infrastructure: the branch `v54-steward-static`, merged into design-v5 as `7d4ce79`
on 11 October 2026 after W2-B's merge, so one merge covered every raw entry; the evidence is in
`C:/tmp/ile_v5_council/evidence/v54/steward-static/`, `NOTES.md` and `VERIFY.md`).

1. **The failure.** `collectstatic` under base.py's `CompressedManifestStaticFilesStorage` stopped with
   `SuspiciousFileOperation`: a raw source sheet collected beside the bundles (`portal/console.css`, then
   `accounts/entrance.css`) imported a partial by its source-tree path («../../../../static/css/v5/…»), which climbs
   above `STATIC_ROOT` once collected. dev.py and test.py use `StaticFilesStorage` and esbuild resolved the source path,
   so nothing local noticed; DL54-44, DL54-73 and DL54-76 recorded it as open.
2. **The convention** (DS 2026 §2, beside the `_` partial rule; `scripts/build_css.mjs`'s header; `console.css`'s
   import list): every `@import` and `url()` in a source sheet is written as it resolves in the collected tree —
   `static/<p>` → `<p>`, `apps/<app>/static/<p>` → `<p>` — relative to the sheet's own collected path: «../css/v5/_x.css»
   from `accounts/entrance.css` or `portal/console.css`, «../../css/v5/_x.css» from `pages/css/hero.css`.
   `build_css.mjs` resolves through the mapping Django's finders use (`static/` first, then each app's `static/`) and
   refuses a path that climbs out of that tree or is absolute, naming the sheet and the line, so `npm run build` stops
   before CI does. The production storage is unchanged; the alternative — keeping raw sources out of what the storage
   post-processes — would have changed it and needed an exclusion list.
3. **Applied.** `console.css`: one line (W1-D's `_loader-light.css`). `entrance.css`: three (`_door.css`, `_varco.css`
   and the grain image). A comment states the rule without a url token, because the manifest storage reads comments
   too. Every `css/dist` bundle rebuilds byte for byte; `static/js/dist` differs only by the chunk names a worktree's
   path gives, so design-v5's names are kept.
4. **The guard:** `tests/frontend/test_static_pipeline.py`, in the non-browser suite — every reference of every source
   sheet lands on exactly one file of the collected tree (Django's own `HashedFilesMixin.patterns`, comments included),
   a self-test of the refusal, and a real `collectstatic` on base settings into `tmp_path` that must exit 0 and hash
   every bundle. Counter-checked: with the old line restored, both fail, the second with the real
   `SuspiciousFileOperation`.
5. **CI's Lint step.** ruff's six findings on design-v5 (W1-D's: `apps/accounts/apps.py` I001;
   `scripts/gen_loader_light.py` E501 ×3, S105, B905) ended the hosted job before its tests ran. Closed as formatting
   only: ruff's safe import order; strings split by implicit concatenation; a `noqa` on S105 (a CSS custom property's
   name, a false positive); `strict=False` on the zip. `gen_loader_light.py --check`: the sheet is unchanged.
6. **The non-browser integration checkpoint**, on a fresh clone of `0b7f457` (no `.env`, no `node_modules`, ci.yml's
   environment): `check`, `makemigrations --check`, ruff and the bundle touch exit 0; `pytest -m "not browser"`:
   **4 482 passed, 0 failed**, 3 skipped (`cases/test_intake`: no legal rule is in force), 2 xfailed (declared debts),
   312 deselected, in 56 min 40 s; `collectstatic` under the manifest storage from the clone: exit 0, 570 files copied,
   1 314 post-processed, every `css/dist` and `js/dist` file hashed.
7. **The manifest** (this entry's commit): `tests/frontend/test_static_pipeline.py` and `.github/workflows/ci.yml` are
   the steward's; `scripts/build_css.mjs` gains a steward slice (the collected-tree resolution and its refusal) and
   stays W1-A's. The import lines of `console.css` and `entrance.css`, the lines pinned in `test_console_shell_w3_a.py`,
   `test_loader_rules.py` and `test_entrance_w2_b.py`, and the formatting of `gen_loader_light.py` and
   `apps/accounts/apps.py` were edited on their owners' behalf; the files stay theirs.
8. **Left, with the reason.** ci.yml's comment gave ~3 200 tests in ~40 minutes; it now gives the rehearsal's figures
   (the job's ceiling stays 90 minutes). The `--durations` table shows ~1.79e9 s for tests that freeze time during
   their setup — pytest 9 starts its timer in `_pytest.timing`, which freezegun's default ignore list does not cover;
   one line in the conftest (`freezegun.configure(extend_ignore_list=["_pytest.timing"])`) would fix the figure, which
   misleads and breaks nothing: left to the test infrastructure. The hero's import of `_door.css` (DL54-44 item 2,
   DL54-76 item 7) is now possible under the convention and stays with the door pass.

**Why.** No deployment passes a `collectstatic` that fails, and a hosted job whose lint step fails never runs the tests:
design-v5 had both, invisible locally because development and tests use another storage. One convention that the
bundler and Django read the same way — checked by the build, by a test and by the real command — keeps the shared
partials shared without changing production's storage.

**Source.** The owner's V5.5 directive (5 October 2026, 14:32: «SHIP THE PRODUCT»; full regression at integration
checkpoints); plan §2.2 (the steward's serialized files and infrastructure), §2.3 (the `_` partial rule); DL54-44 item 4;
DL54-73; DL54-76 items 6 and 7; `C:/tmp/ile_v5_council/evidence/v54/steward-static/` (`NOTES.md`, `VERIFY.md`, the
rehearsal's logs, `junit.xml` and `staticfiles.json`).

## DL54-78 · 11 October 2026 · W3-B: the person's dashboard — the order, the NowPanel's four variants and the takeover, one raised plane, cards by purpose

**Decision.**
- **The order is the DOM's** (plan §3.5 item 4: h1 → NowPanel → journey): the page header — who and which file, the
  reference in ILE Mono, the state and since when, no action —; the NowPanel; «Mon parcours»; the file's facts
  (beside the NowPanel from 64rem by grid placement — the journey carries no control, so the focus still goes
  NowPanel → file); the pieces; the dates and the communications; what folds; the account's line.
- **The NowPanel is the screen's one raised plane** — W1-C's action card — and holds the screen's ONE primary: the
  act itself, on the obligation's own page, in the register's words («Déposer la pièce», «Remplacer la pièce»;
  «Accepter les Conditions», labelled «Accepter les Conditions d’utilisation», where the conditions gate blocks the
  filing — the register row's own resolution). **Four variants, chosen by the system** (`portal.services.now_panel`,
  never by the person, never remembered): «à vous» · «en attente d'un tiers» (no primary; «Cette étape ne dépend pas
  de vous.»; a quiet «Consulter» for a piece) · «rien à faire» («Aucune action ne vous est demandée pour
  l’instant.») · «pas encore de dossier» («Le questionnaire d’orientation», «Commencer le questionnaire»). **An
  overdue date of the account takes the panel over** — unless the next action is already overdue or a blocking
  outcome stops the path — and is drawn there only.
- **Cards by purpose** (DL54-55): the action card for the NowPanel, the summary strip for the file's facts (its
  objective, its progress, who intervenes). Everything else is flat under hairlines. No stat card, no grid of equal
  cards, no board.
- **One thing once.** The NowPanel's piece is not drawn again in the list (`data-piece`, tested); the reference is
  drawn once (the header) and the way to the file once — «Votre dossier», at the file's head; the rail's «Mes
  dossiers» leads to the list — the comp's D-1 and D-4. «Navigation rapide» is not drawn (D-3: it repeated the
  rail).
- **What folds** is W1-C's native disclosure, its default picked by the server from the data and never remembered:
  the Academy open when there is an enrolment; «Derniers dépôts» and the pre-assessment's sources closed.
- **The account stays one quiet line at the foot** — e-mail, account type, last sign-in; Profil, Sécurité du compte
  and, for staff, Back-office — until the console's account popover (W2-A) holds them: from 64rem the rail's foot
  carries the profile and sign-out only, and nothing else in the console leads to the security settings or to the
  back-office. The gate-0 comp moved it into the account menu; that menu does not exist on the desktop yet.
- **The journey is W3-D's, placed and not redrawn**, with one scoped rule: on the dashboard the rail is drawn still at
  load (plan §1.18 D16: «in V5.4 the rail is drawn still at load»; MS §3.2) — V4's line drew itself, six
  animations at every visit. Redundant, and harmless, the day W3-D redraws the rail.
- **The pre-assessment's outcome at the console's scale** (20 / 28 on its 3 px state rule): the V2 display made it
  the largest word of the page, above the page's own title.

**Measured** (lane 8786, `ile_v5_l6`, four personas × fr / ar × 1920 × 1080, 1440 × 900, 1366 × 657, 1024 × 768,
390 × 844): one primary in the first viewport wherever the person has an act, with its piece and its date when the
piece has one; no piece drawn twice; one raised plane and two shadow values (the NowPanel's, the journey node's
halo — W3-D's); corners 4 · 8 · full; no animation at load; no horizontal overflow; 0 console errors, 0 CSP
reports. At 390 px 0–9 % of the characters are under 14 px (the gate: 35 %).

**Source.** Plan §3.5 item 4 (gate), §1.15, §1.4 SH-2 / SH-8, §3.1 item 7; DL54-55; the platform map's F4–F7 and
the comp's D-1, D-3, D-4, D-6; `QA/v54/w3-b/NOTES.md`; `tests/frontend/test_dashboard_w3_b.py`,
`tests/frontend/test_dashboard_browser_w3_b.py`.

## DL54-79 · 11 October 2026 · W3-B: T1 — one next action over the file's open obligations, on the precedence it had; a piece named only to an account that may read it

**Decision.** `cases.services.next_action(case, *, reader=None)` computes ONE next action over every open obligation
of the file — its open checklist items AND the pieces it still waits for (`documents.models.OPEN_STATES`) — on the
precedence the function already had: a blocking outcome (which now leads to its page, `cases:assessment`), the
review rung, an overdue obligation, the nearest date (on a tie a checklist item before a piece, the order before
T1), the person's own open obligation, else the first of anybody's (IMPLEMENTATION_PLAN §2 T1: «open item the person
must act on»), the questionnaire for a draft file, nothing. A piece that satisfies a checklist item stands for it:
one obligation, drawn once. The action says what it is about — `kind`, `piece_id`, `due_date`, `state`, the `lang` of
its own words. **Pieces are read through the documents app's own authorisation, at query time**
(`DocumentRequirement.objects.readable_by(reader)`); with no reader, only the access class every reader of the case
may read (CASE): a title kept to the person and the administration never reaches a caller that did not say who is
looking. The case views pass the reader (`apps/cases/views.py`, two lines): the dashboard and the case name the same
piece.

**Not changed.** No rung moved; no legal rule, permission, state logic or visibility changed. A checklist item still
has no URL of its own — it is worked from the case file, which the dashboard's NowPanel links with «Continuer». The
documents page's own primary (`documents.presenters.primary_action`, the first piece the person can file in the
register's order) is W3-C's: it should read `next_action(case, reader=user)` when its kind is a piece — left to W3-C.

**Why.** On the QA data the dashboard named an authority's checklist item («Identifier les interlocuteurs et les
autorités compétents…», no date, no act) while the person had three pieces of their own to replace, the first due
on 05.11.2026; another draft file named the questionnaire while its diploma was «À remplacer».

**Source.** Plan §1.18 «Track T» (T1–T3 by unifying presenters on the existing precedence; no rule changes);
IMPLEMENTATION_PLAN §2 T1; `tests/frontend/test_dashboard_w3_b.py` (one test per rung).

## DL54-80 · 11 October 2026 · W3-B: «il registro» on the dashboard — the colour is the group, the shape is the state; the group words are the catalogue's

**Decision.** The dashboard draws the file's pieces by who holds them (O62): **to act** (an open piece the person
answers for), **in hand** (filed, in review, or asked of another actor), **settled** (valid) — each a 16 px mark of its
state, the chip's own (`chip_mark`), coloured by its group's ledger token (`--ledger-to-act`, `--ledger-in-hand`,
`--ledger-settled`, W1-A's), never by `data-register` (W1-C keeps that attribute to the chip and its two legends).
The group's word and its count are the text; the marks are decoration over them. **The words are catalogue strings
in the four languages** — «À faire» and «En cours» (the checklist's own states, `cases.ChecklistStatus`), «Valide»
(`RequirementState.VALID`) — until B1 signs «À vous · En cours · Réglées» (plan §1.18 D15: «The group words stay as
existing catalogue strings until B1 signs»). The list under the ledger names every piece the person must act on,
each with its act, then the pieces in somebody else's hands with who holds them, five rows at most («et n autres
pièces»).

**Source.** Plan §1.18 D15; O62; DL54-53; `apps/portal/services.py` `_dashboard_pieces`.

## DL54-81 · 11 October 2026 · W3-B: the door in the console's one empty state

**Decision.** «Pas encore de dossier» draws the owner's door with the doorway component exactly as it is
(`templates/components/doorway.html` inside `<svg viewBox="264 64 368 456">`, prefix `db-door` — the entrance's
compact crop), at the NowPanel's end and above the words on a phone; aria-hidden imagery; never mirrored (the
component's own `direction: ltr`); nothing animates it. Its paint is v4/hero.css's until W2-B's `_door.css` takes
the stage as drawn, which then serves this seat too. One request more on that page only: the 42 KB arch strip.

**Why.** Plan §2.3 («the console entry for the one empty state that shows the door») and §3.1 item 7 (the identity
carriers of a console screen: «the door in its one empty state»). The comp composed no empty state (D-6).

**Source.** Plan §2.3, §3.1 item 7; BA §2; `DESIGN_SYSTEM_2026.md` §10 `doorway.html`, §11.7.

## DL54-82 · 11 October 2026 · W3-B: paths outside the slice, the legacy rules deleted, the CSS weight

**Paths outside the family's slice** (`scripts/check_ownership.py w3-b design-v5`), each for one reason, for the merge
step to record:

| Path | Owner | What, and why |
|---|---|---|
| `apps/cases/views.py` | none | the two calls of `next_action` pass `reader=request.user` (DL54-79): the case page names the piece the reader may read, the same as the dashboard's |
| `apps/portal/tests/test_views.py`, `test_services.py`, `test_review.py` | none | the dashboard's tests that pinned V4's markup (`threads__row`, `dates__row`, `portal-account__identity`, `class="empty"`) and the hidden grid (`dashboard_context(person)["cards"]`) retargeted to the V5 markup and to `bridge_cards`: the intents kept — an empty region prints one line and no figure, real rows are listed, the e-mail is printed once, the orientation is presented once |
| `tests/frontend/test_console_shell_w3_a.py` | W3-A | console.css's import list: the light sheet, the shell, then each Wave-3 family's `_` partial from the app's static folder — the test said «each family adds its partial's import» and pinned two lines |

**Inside shared files, beyond the slice's words:** `static/css/v4/workspace.css` — besides its Panel / facts /
HealthStrip rules (`.panel__more`, the meter's facts row, `.health--compact`), the person dashboard's own rules that
no section names (its regions' grid placements, the latest deposits, the account panel) and the two dashboard-only
variants nobody calls any more: the DocumentRow's `--compact` with `.doc-collection--bare` (W3-C's section) and the
journey's dashboard wrapper `.ws-journey` (W3-D's section) — every selector removed matches no template;
`apps/portal/static/portal/portal.css` — the old account panel (two blocks, unused); `DESIGN_SYSTEM_2026.md` — §11.7
and §2.1's console row (the dashboard's prose), and three §10 entries kept true: `document_row.html` and
`health_strip.html` no longer cite the dashboard (their `compact` said uncalled — W3-C's prose), `doorway.html` cites
it (W2-D's prose).

**The weight.** The bust rule's first remedy (DL54-15) taken: the legacy rules the dashboard supersedes are deleted —
`dist/main.css` −270 B gzip, `dist/portal/portal.css` −68 B; the partial adds `dist/portal/console.css` +1 643 B
(5 292 → 6 935). The console page types' three sheets weigh **51 246 B gzip — +1 305 B over the base of this
branch** (49 941 B, the committed bundles of `1c001e6`, `gzip -9`), about 1.2 KB over the ceiling DL54-73 recorded
(50 007 B in the steward's measure). What the dashboard still draws with V4's rules (Panel, facts, HealthStrip,
ContextHeader) stays: the case file (W3-E), the company dashboard (W3-B's step 2), «Ma situation» and the documents
pages (W3-C) draw them. Under V5.5 («fix only real regressions … if performance is good and does not block UX:
ship») it is reported here, not hidden; the merge step records the ceiling.

**Source.** Plan §2.2, §2.6; DL54-15; DL54-73 item 3; `OWNERSHIP_V54.json`.

## DL54-83 · 11 October 2026 · W3-B, step 2: the company's dashboard — the person's grammar, the company's one next action on the NowPanel, «il registro» of the needs, each need once

**Decision.**
- **The same grammar as the person's dashboard** (DL54-78), not a second system: the page header without an action
  — «Entreprise», the legal name as the h1 (its own direction, its box on the page's reading edge), the verification
  as a word with its register (a fact the project checked about the legal entity, never an approval of anyone),
  sector, place —; **the NowPanel**, the screen's one raised plane, from the one partial both dashboards include
  (`templates/portal/partials/now_panel.html`); the company's identity in W1-C's summary strip beside it from 64rem;
  the needs; the communications, flat. No stat card, no grid of equal cards, no person anywhere on the screen.
- **The NowPanel says the company's one next action** — `companies.services.next_action`, unchanged, composed by
  `portal.services.company_now_panel`: «à vous» when the act is the company's (declare the company, complete or
  transmit a need, express the first one) with its ONE primary in the presenter's own words («Déclarer mon
  entreprise», «Compléter le besoin», «Ouvrir le besoin», «Créer un besoin»); «en attente d'un tiers» while the
  project team verifies the company or examines the needs («Cette étape ne dépend pas de vous.», no primary); «rien
  à faire». The need the act is about — found as the need whose page the act opens — lends its state chip and is
  drawn there and only there (`data-need`; the person's rule for a piece, DL54-78 «one thing once»). The company's
  next action has no date: none is drawn (the data holds none). The owner's door stays the person's one empty state
  (DL54-81): the company without a company has the declaration on its NowPanel.
- **«Il registro» of the needs** (O62, DL54-80): by who holds them — to act (the company's drafts), in hand
  (transmitted, under review, taken over, on hold: the project's or an actor's), closed (closed, withdrawn) — each a
  16 px mark of its state coloured by its group; the group words are the catalogue's: «À faire» and «En cours», as on
  the person's dashboard, and «Clos», the need's own state. Then the needs in that order, five at most: a draft with
  its act («Ouvrir le besoin», a secondary button described by the need's title), the others with who answers for
  them (the named live party, or «aucun intervenant désigné» on the dashed disc) — one destination, one stop: a
  draft's way to its page is its act, another need's is its title; «Tous mes besoins» leads to the register;
  «Nouveau besoin» stands under the list, offered while the project verifies the company too (a need can be
  prepared before), unless creating is already the NowPanel's primary. The header's «n besoins en cours» is gone: it
  counted the drafts as «en cours» while the ledger's «En cours» does not, and the ledger counts them all.
- **One thing once**: the legal name is the h1 and is not repeated in the identity strip (immatriculation in ILE Mono,
  the referent); a record's own words carry `dir="auto"` on an inline isolate, so a Latin name on an Arabic page
  stays on the reading edge.

**Not built, and said:** a date on the company's NowPanel (no data), «Formation liée» (no data links a training to a
company — CREATIVE_DIRECTION.md §3.8.4, unchanged). **Not changed:** `companies.services` (no rule, no state, no
permission); the view adds one call (`apps/companies/views.py`, DL54-85).

**Source.** Plan §3.5 item 4, §1.15, §3.1 item 7; DL54-55, DL54-78, DL54-80, DL54-81; `QA/v54/w3-b/NOTES.md` «Step
2/2»; `tests/frontend/test_dashboard_w3_b.py`, `tests/frontend/test_dashboard_browser_w3_b.py`.

## DL54-84 · 11 October 2026 · W3-B, step 2: the bridge — no NowPanel, its registers in the person's grammar

**Decision.** The accounts that are not a person — an institution, a university, a professional, a company account
without the person's role — have no case file and no next action of their own until their workspaces exist (P1 of
the requirement matrix). Their dashboard draws **no NowPanel**: a «rien à faire» there would be a claim the system
cannot make (an authorised actor's work is in «Processus assignés», the rail's first page for that account), and an
invented priority would be worse. Their registers (`portal.services.bridge_cards`, unchanged, built for them only:
F9) become flat sections in the person's grammar (`templates/portal/partials/card.html`), and the system still
orders priority: the main column first says what is due and what came in — the dates (an overdue one said by its
chip, in azione as on the person's page: terracotta, never the red of a refusal — plan §1.2; the card presenter maps
the deadlines page's «error» to «overdue», the page itself keeps its register for W3-C), the communications — then
what the account sent and filed; the organisation it belongs to stands beside, from
64rem, as the file's facts do on a person's page (on one column it comes last). Each section: the domain's glyph, the
word, a state worth saying as a chip («1 en retard», «1 non lue»), the one link to its whole page, then its latest
rows with their date, kind and state chip (`components/badge.html` is the chip). An empty region is one line; the
empty «titles» of V4's dashed boxes are not drawn. The pre-assessment is the person's section (the orientation
register gives way to it: never drawn twice) and the account's quiet line closes the page as it closes the person's.
The six equal cards with their numerals, V4's grid and its rules are gone.

**Why.** Plan §1.15 — «the system orders priority … a region the account cannot use is not rendered; an empty region
is one line»; DL54-55 — no stat grid, no board; the gate's «no stat-card» and «≤ 1 raised panel». The value: an
institution reads first what is due and what came back — a deadline overdue in its chip, an unread message —, then
what it sent, with the organisation it belongs to beside, instead of six boxes of equal weight, four of them empty.

**Source.** Plan §3.5 item 4 («the institution / university bridge»), §1.15; DL54-55, DL54-78;
`tests/frontend/test_dashboard_w3_b.py` (the bridge's three tests), `tests/frontend/test_dashboard_browser_w3_b.py`.

## DL54-85 · 11 October 2026 · W3-B, step 2: paths outside the slice, the legacy rules deleted, the CSS weight — the ceiling not reached, and why

**Paths outside the family's slice** (`scripts/check_ownership.py w3-b design-v5`), added by this step, for the merge
step to record (the five of step 1 are DL54-82's):

| Path | Owner | What, and why |
|---|---|---|
| `apps/companies/views.py` | W3-A (a slice: `_render`, the last crumb) | `dashboard()` adds one call, `portal_services.company_dashboard(company, needs, next_action)`: the NowPanel and the needs' ledger are the console's dashboard presenters (W3-B's slice of `apps/portal/services.py`), over the company app's own answers |
| `templates/portal/partials/now_panel.html` | none (new) | the NowPanel, extracted from the person's dashboard so that the company's draws the same component: one markup for the one raised plane |
| `templates/portal/partials/card.html` | none named (W3-E holds «the console templates no other family names») | the bridge's register — the dashboard's own partial, included by `templates/portal/dashboard.html` only — redrawn from V4's counted card to a flat section |
| `tests/frontend/test_chips_cards_w1_c.py` | W1-C | `test_no_stat_card_grid_on_a_persons_or_a_companys_screen` pinned the bridge's `<div class="portal-cards">` behind its guard; retargeted to the redrawn bridge, the intent kept — no counted box on a person's or a company's screen, the bridge never a person's |
| `apps/portal/tests/test_views.py` (again) | none | the `_card` helper reads a bridge register by its `data-card`, as before |

**Inside shared files, beyond the slice's words:** `static/css/v4/workspace.css` — besides the facts (the slice's
«facts»: their last consumer was the company's identity panel), the company dashboard's own section, the 12-column
workspace grid and its spans (the case file neutralises them inside its own grid), the lone next step, the bridge's
assessment panel and every rule of the needs table (`companies/partials/need_table.html` is drawn by no page now; the
dev-only showcase still includes it); `apps/portal/static/portal/portal.css` — the slice's «bridge part», the card grid
and its cards; `DESIGN_SYSTEM_2026.md` — §11.7 «I cruscotti» (the company's dashboard and the bridge), §2.1's console
row, §10's `doorway.html` entry (its consumer is the NowPanel partial now: W2-D's prose kept true), and §2's row of
`v4/workspace.css`: its sentence follows the sheet, and its weight was rewritten by
`scripts/regen_design_inventory.py --write` (52.2 → 45.7 KB, the one stale figure it found) so that
`test_documented_file_weights_are_roughly_true` holds on the branch — the steward's regeneration after the merge
finds it current.

**Panel, ContextHeader and HealthStrip stay** — the rest of this family's rows of the deletion map (plan §2.3) still
have consumers outside it: the case file (`templates/cases/detail.html`: Panel, ContextHeader, the meter, the
HealthStrip — W3-E), «Ma situation» (Panel, the workspace head — W3-E), «Mes pièces» and the register partial (Panel,
the workspace head, the HealthStrip — W3-C). Deleting them here would break those pages («no page worse than
before», plan §2.1); they leave with their last consumer (§2.1: «its last named consumer deletes the file»).

**The weight** (gzip −9 the steward's way, Python's `gzip.compress(…, 9)`, DL54-73): the console page types' three
sheets **51 308 → 50 768 B** with this step — `dist/main.css` 42 178 → 41 802 (−376), `dist/portal/portal.css`
2 195 → 1 954 (−241), `dist/portal/console.css` 6 935 → 7 012 (+77: the company's and the bridge's few rules, after a
consolidation of the partial). **The ceiling of DL54-73, 50 007 B, is not reached: 761 B over**, where step 1 left it
1 301 B over. Measured by deletion, the rows that cannot leave yet weigh 624 B (Panel 175, ContextHeader and the
workspace head 166, HealthStrip 181, the meter 102; the facts, 38, did leave) and the case file's own section 866 B:
W3-C's and W3-E's redraws bring the console page types under the ceiling. What was weighed and refused: moving the
dashboard's partial into a page sheet of the three dashboards (the thirty other console page types would drop to
≈ 49 050 B, the dashboards would rise to ≈ 51 400 B, and a session that opens the dashboard — every session — would
load ≈ 640 B more in all, the partial losing the shell's gzip dictionary); cutting the dashboards' own rules (the
partial is 1.7 KB for three page types). Under V5.5 («fix only real regressions … if performance is good and does
not block UX: ship»; the lane's smoke — LCP 168–288 ms on the company's and the bridge's pages, 388–464 ms on the
person's, CLS 0 — is in the notes) it is reported here, not hidden; the merge step records it, as DL54-73 asks of a
merge that would land over the ceiling.

**Source.** Plan §2.1, §2.2, §2.3 (the deletion map), §2.6; DL54-15; DL54-73 item 3; DL54-82; `OWNERSHIP_V54.json`;
`QA/v54/w3-b/NOTES.md` «Step 2/2».

## DL54-86 · 11 October 2026 · W3-B, the fix pass: no button promises an act its page cannot do; a record's own words keep their direction; the company's NowPanel carries the need page's own act

**Decision.**
- **The Conditions gate (the review's M1; the check's WCAG 2.5.3 finding).** While the gate blocks a piece's filing,
  the NowPanel's one primary is «Consulter» on the piece's own page — which states the gate and links the terms — and
  its note carries the register's own words, «Acceptation des Conditions d'utilisation requise.»; the dashboard's rows
  already said «Consulter» for the same block. «Accepter les Conditions» led to the public terms page, which has
  nothing to accept until the acceptance flow exists (G1), and its accessible name in Arabic did not contain its
  visible words: the button and its `aria_label` are gone, and the partial no longer takes an `aria_label` — the
  visible words are the name. DL54-78's «Accepter les Conditions … where the conditions gate blocks the filing» is
  superseded. The register row's own «Accepter les Conditions» (`components/document_row.html`) is W3-C's, carried
  over with the same resolution.
- **A record's own words keep their direction** (M2; the check's finding 1). What the data holds no language for — a
  date the team wrote and its source note on the NowPanel's takeover, a date's title, a message's subject, a file's
  name, the pre-assessment's rationale, an organisation's name — is drawn in its own direction (`dir="auto"`), as the
  bridge's register already did; the partial writes `dir` whenever the presenter sets it (`words.dir`), and a title or
  text so isolated hugs its box on the panel's reading edge (the `[lang]` rule extended to `[dir]`). The takeover's
  note stands under the deadlines page's «Origine :» (m8). The NowPanel's region is named by whose move it is and by the
  obligation (`aria-labelledby="db-now-eyebrow db-now-title"`; the check's finding 6).
- **The company's transmit act (m4 — the team's decision, one direction).** When the company's next action is to
  transmit a complete draft and the account may submit it (`can(user, "submit", need)`, the company app's own policy),
  the NowPanel's primary is the need page's own act — its POST form to `companies:need_submit` and its words,
  «Transmettre au projet» — with the need in view (its title in the h2, its state, its reference in ILE Mono), and
  «Ouvrir le besoin» stays beside it as the quiet secondary for a last reading. One verb, one click, the same server
  checks; the link is never relabelled as the act. An account that may not submit keeps the link, as before.
- **Kept honest in place** (the minors, no new copy): «rien à faire» names the file's most recent live assignment
  (m2); a piece the person filed, or in review, names no party in the slot for who holds it (m3); when the overdue
  date the NowPanel took over is the only one, «Mes échéances» is not drawn (m1); the company account without a company
  has its communications beside the NowPanel (m9); the bridge heads its main column with one quiet link to where the
  account's work lives, in the rail's words — «Espace entreprise», «Processus assignés»… — and none for an institution or
  a university (m10). French spacing (W2-D's `typo`) on the NowPanel's title and text (m5); the progress figures tied
  by no-break spaces (m11); the «Responsable» disc and its word held together (m7); under a finger a list link's words
  centred in its 44 px and an empty line's link 44 px too (m6; the check's finding 3); the needs' end track a fixed
  measure, so a late font no longer resizes the shared columns (the check's finding 4). The console's empty state
  spans the main column again (`.portal__main .empty-state`, restored in `portal.css`: M3 — four pages of other
  families had been made worse by the bridge's clean-up).

**Not done, and why.** The person's register keeps its `auto` end columns: a fixed end track there would narrow the
pieces' titles at 1024–1440 for one shift in seven cold loads on the dev server (0 on the production-shaped twin, where
the font is preloaded). A case's suspension reason in its notice stays unisolated: the notice component (W1-C's) has
no direction parameter.

**The weight.** `gzip -9` of the committed bundles: `dist/portal/console.css` 7 012 → 7 072 B (+60), `dist/portal/portal.css`
1 954 → 1 975 B (+21, the restored rule); the console page types 50 768 → 50 849 B — 842 B over DL54-73's ceiling,
inside §2.6 item 5's once-only raise (≤ 2 KB) the merge step records (DL54-85); JS unchanged.

**Paths.** `apps/companies/views.py` (DL54-85's) passes `user=request.user` to `company_dashboard` — one argument; no
new path outside the slice.

**Source.** `QA/v54/w3-b/REVIEW.md` (M1–M3, m1–m11), `QA/v54/w3-b/A11Y_PERF.md` (findings 1–4, 6); `QA/v54/w3-b/NOTES.md`
«Review fixes»; DL54-78, DL54-83 … DL54-85; `tests/frontend/test_dashboard_w3_b.py`,
`tests/frontend/test_dashboard_browser_w3_b.py`.

## DL54-87 · 11 October 2026 · Steward, the w3-b merge: the family's entries renumbered, the nine paths assigned, the console page types' ceiling raised once as measured, the door's component included again

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w3-b` into design-v5 on 11 October 2026 —
what the family's own entries hand to the merge step: DL54-82, DL54-85, DL54-86; `QA/v54/w3-b/NOTES.md` «What is left,
and whose» (steps 1 and 2) and «Handed over»; `QA/v54/w3-b/A11Y_PERF.md` finding 7).

1. **Numbering.** W2-B's two entries, the record of their merge and the static pipeline reached design-v5 first as
   DL54-74 … DL54-77, so the family's nine entries, written as DL54-74 … DL54-82 on its branch, are **DL54-78 …
   DL54-86** — the same order, add 4 —, content unchanged but for their cross-references (the pre-merge sync,
   `3c24d67`). The index gains the row of the fix pass's entry (DL54-86), which the branch had not written. The code
   and DS 2026 cite none of the moved numbers; the family's notes, review and accessibility report keep the numbers
   they were written with, and the notes' closing section says how to read them (`6bcb460`).
2. **The nine paths outside the slice are this area's in the manifest** (`046879f`). `scripts/check_ownership.py w3-b
   design-v5` listed them; each was read in the diff and found to be what the family declares — DL54-82:
   `apps/cases/views.py` (the two calls of `next_action` pass the reader, T1), `apps/portal/tests/test_views.py`,
   `test_services.py` and `test_review.py` (the dashboard's tests retargeted to the V5 markup and to `bridge_cards`,
   their intents kept), one test of `tests/frontend/test_console_shell_w3_a.py` (each Wave-3 family's partial after the
   shell; the file stays W3-A's); DL54-85: `apps/companies/views.py` (`dashboard()`'s one call to
   `portal.services.company_dashboard`; the file stays W3-A's), `templates/portal/partials/now_panel.html` and
   `card.html` (whole: the NowPanel, included by the two dashboards; the bridge's register, by the person's dashboard
   only), one test of `tests/frontend/test_chips_cards_w1_c.py` (the file stays W1-C's). Three slices are named as
   written: `static/css/v4/workspace.css` (the deletions beyond «Panel, HealthStrip, facts, ContextHeader» — among them
   DocumentRow's `--compact` from W3-C's section and `.ws-journey` from W3-D's, every selector matching no template),
   `apps/portal/static/portal/portal.css` (the bridge part, the old account panel, the restored
   `.portal__main .empty-state`), DS 2026 (§11.7 and the sentences of §2, §2.1 and §10 that follow the markup). The
   check after it: 10 inside, 14 slice, 18 generated, and the manifest itself, the one steward-only path (before: 9
   outside).
3. **The console page types' ceiling is raised once, by 841 B, as measured — §2.6 item 5, applied and said.** On the
   bundles rebuilt from a clean dist at the merge, gzip −9: `dist/main.css` 41 880 B, `dist/portal/console.css`
   7 072 B, `dist/portal/portal.css` 1 975 B — **50 927 B in the three sheets every console page loads**, 841 B over the
   ceiling of 50 086 B (DL54-73 item 3, DL54-76 item 5); the company's dashboard adds `companies.css` (873 B: 51 800 B),
   «Mes pièces» `documents.css` (1 172 B: 52 099 B), both unchanged by the area. Against design-v5 the merge moves
   `console.css` +1 780 B (the dashboards' partial), `portal.css` −288 B and `main.css` −651 B (the legacy rules
   deleted). Item 5's conditions, one by one: the family first deleted the legacy rules its components supersede — the
   dashboards' V4 rules, the facts, the 12-column workspace grid, the needs table, the bridge's cards (the bust rule's
   first remedy, DL54-15); it weighed moving the dashboards' partial into a page sheet and refused it on its measure —
   the dashboards would carry ≈ 51 400 B and every session, which opens on a dashboard, ≈ 640 B more (DL54-85); and LCP
   and the first render were measured no worse — not by the Performance Lead on 8782, which was not made, but by the
   area's check on the lane's compressed twin with W1-0's protocol and `trace.py` (profile A, CPU × 4, n = 9 cold loads
   a cell): `dashboard-person` LCP 252–300 ms earlier than V4 in all four cells (fr and ar, 1440 and 412; ≤ 2.5 s),
   the first-render task 39–57 ms where V4's was 370–500, CLS 0 on 36 loads; against the merge base on the lane
   (n = 7 a cell, interleaved), no consistent regression and the longest task lower in 5 of 7 cells
   (`QA/v54/w3-b/A11Y_PERF.md` «Performance», finding 7). The raise is under 2 KB and the console page types' first
   under item 5 (DL54-73 item 3 recorded a ceiling as measured without applying it; DL54-76 item 5 moved it by the
   plan's own token block). The family asked for it (DL54-85, DL54-86) and the check found its conditions met; the
   owner's V5.5 rule lets the area ship.
   - **What holds from here.** The console page types' ceiling is **50 927 B** in the three sheets, plus a page's own
     sheet as it weighs at this merge. The once-only raise is spent: it does not rise again — a family that adds to
     the console's sheets first deletes, and a merge that would land over it comes back to this log first. What the
     family measured by deletion and left with its consumers — Panel 175 B, ContextHeader and the workspace head
     166 B, HealthStrip 181 B, the meter 102 B (624 B), and the case file's own V4 section 866 B — leaves with W3-C's
     and W3-E's redraws, and the steward lowers the ceiling when a merge lands more than 1 KB under it (§2.6 item 3).
   - **No ceiling is lowered.** `main.css`'s −651 B reaches every page type, and none lands more than 1 KB under its
     ceiling: an interior page 42 531 → 41 880 B, the login 47 392 → 46 741 B (DL54-76 item 4), the home 57 182 →
     56 531 B. The home's ceiling, read from DL54-44 item 3's own rule — `main.css`'s measured total at the end of
     Wave 1 (42 461 B at `v54/w1-c`, DL54-73 item 3) plus the home's two page sheets (14 651 B), with DL54-76 item 5's
     79 B — is **57 191 B**, not the Wave-1 figure of 59 137 B that DL54-76 item 5 cites; the home stands 660 B under
     it. `dist/main.css` stands 4 200 B under its 45 KB ceiling (46 080 B). Nothing pins these figures:
     `tests/frontend/test_css_budget.py` (plan §2.7) does not exist.
4. **The door's component is included again — by the NowPanel — and its paint is still `v4/hero.css`.** W2-B's merge
   left `templates/components/doorway.html` included by no page (DS 2026 §10; DL54-76 item 7 (b)); this one brings
   `templates/portal/partials/now_panel.html`, whose «pas encore de dossier» is the console's one empty state that
   shows the door (DL54-81). DS 2026 §10's «Usato in» was merged at the sync to say both: the NowPanel is the one
   template that includes the component; the home and the entrance draw the stage with their own markup. The door on
   the dashboard is painted by `v4/hero.css`'s `.doorway__*` rules in `main.css` — `static/css/v5/_door.css` paints
   the same classes on the entrance only, imported by `accounts/entrance.css`. So DL54-76 item 7 (b)'s pass —
   `v4/hero.css` out of `main.css` with the component — has a third page to measure, the person's dashboard without a
   file, and first gives the console the door's paint (the import of `../css/v5/_door.css` in `console.css`'s list,
   through the steward, weighed against the ceiling of item 3). Left to that pass, with this consumer named.
5. **The capture report is unchanged.** Plan §2.2 step 3 regenerates `docs/qa/design/capture-report.json` whenever
   pages, icons or the chrome change; `capture.py` captures the home, the privacy page, the login and the 404, none of
   which this merge changes (`main.css` loses rules no captured page draws). `scripts/regen_design_inventory.py` finds
   the inventory tables current on the merged tree.

**Why.** Nine entries under numbers W2-B and the static pipeline already hold would make every citation ambiguous; nine
paths nobody holds would have no writer for the next family; a ceiling exceeded and not written down is a ceiling
nobody holds — and the raise item 5 allows once is worth recording with the evidence it rests on, so that the next
merge knows it is spent. A component that a page includes again needs its paint named before the sheet that paints it
is retired.

**Source.** The owner's V5.5 directive (5 October 2026, 14:32: «PERFORMANCE», «SHIP THE PRODUCT»); plan §2.2 (the
manifest: the steward assigns; the serialized shared files; merge step 3), §2.3 (the deletion map), §2.6 items 3 and 5;
DL54-15; DL54-44 item 3; DL54-73 item 3; DL54-76 items 4, 5 and 7; DL54-81, DL54-82, DL54-85, DL54-86;
`QA/v54/w3-b/A11Y_PERF.md` «Performance» and finding 7; `QA/v54/w3-b/NOTES.md` «What is left, and whose» and «Handed
over»; the weights measured on `v54-w3-b` after the pre-merge sync and `npm run build` from a clean `static/js/dist`
and `static/css/dist`, against design-v5 at `38f78d4`.

## DL54-88 · 11 October 2026 · W2-A: the overlay system as built — one sheet, one module, five components, a board

**Decision.** The overlay system of plan §1.14 is one stylesheet (`static/css/v5/overlays.css`, in `main.css` after
`v5/tabs.css`), one module (`static/js/src/overlay.js`, an entry of its own that `console.js` and — W2-C2 —
`shell.js` import) and five components (`templates/components/{dialog,drawer,popover,tooltip,sheet}.html`), on the
contract written first (`QA/v54/w2-a/CONTRACT.md`). The decisions met while building it:

1. **One block, five families.** Every panel is `.overlay` with a family modifier (`--dialog`, `--alert`, `--drawer`,
   `--sheet`, `--popover`) and `data-overlay="<family>"` as the script's hook (DS 2026 §2: hooks are `data-*`, classes
   style); the tooltip is `[data-tip]`'s own `::after` and the shared `.tooltip`. `.sheet` was not available (the
   living page's article carries it) and `.dialog` was V2's.
2. **A template-side caller gives the body and the foot by template** (`body_template`, `actions_template`, included
   with `overlay_part`): a Django include wraps nothing, and the account popover, the console drawer and the filter
   sheet are drawn by templates, not by views.
3. **A menu as a sheet stays a menu** (≤ 40rem): non-modal, no scrim — a popover's backdrop lets every press through
   (the platform's rule), and a dim layer that does not take the press would only look modal.
4. **The side of a menu is chosen before it opens** (below unless the room is above), from sizes read at idle on
   inert clones, so its 4 px drop goes away from its trigger on the first opening too; the anchor is bound by script
   (`anchor-name`), read in the panel's own direction (`position-area: self-block-end span-self-inline-start`: the
   viewport's direction is the root's, and the board's Arabic cell sits in an Italian page); without anchor
   positioning `overlay.js` places it with the same flip and clamp and follows the scroll.
5. **The tooltip's warm group is CSS** (`@property --tip-warm`, a 0 ms transition with the wait as its delay): O9's
   «0 B of script for the warm window»; Esc and the press are script (`data-tip-off`). A control whose panel is open
   names nothing (`[aria-expanded="true"]`). Esc puts the tips away and takes the key from nobody.
6. **The scroll lock keeps the scrollbar's gutter** (`html[data-overlay-lock="gutter"]`, `scrollbar-gutter: stable`)
   only where the page had a scrollbar: a permanent gutter would move every short page.
7. **The no-script path is the link**: an opener is `<a href="#id" data-overlay-open>` (`:target` shows the panel;
   «Fermer» is a link back), which the module makes a button — W3-A's «Menu» precedent (DL54-69).
8. **The board** `templates/dev/designpreview/specimens/overlays.html` shows every family open in French and in
   Arabic with live strings (the account deletion as an alertdialog, the need's withdrawal as a dialog with a field,
   the rail's pages, a detail beside the list with its history entry, the languages, the account and row menus, a
   tooltip group and the top-layer tip); the browser tests run on it, rendered by Django through their module's URL.

**Source.** Plan §1.14 (O1–O11), §1.5 (MS-O2, MS-O4, MS-O5, MS-O6), §2.3; the contract; DS 2026 §2, §7.2, §10, §12,
§16; `tests/frontend/test_overlays.py`, `test_overlays_browser_w2_a.py`, `tests/i18n/test_rtl_browser_overlays.py`.

## DL54-89 · 11 October 2026 · W2-A: the INP rule fired — a modal kind opens with show() over one scrim, the trap in script; and html:has(:focus-visible) goes

**Decision.**
1. **The modal kinds (dialog, alert, modal drawer, sheet) open with `show()`**, `aria-modal="true"` and
   `closedby="closerequest"` (Esc and a phone's Back reach a dialog `showModal()` did not open), over ONE shared
   `.overlay-scrim` (made at idle; drawn like a `::backdrop`, on the topmost panel's clocks), with the trap in script —
   Tab and Shift+Tab wrap inside the panel, a focus that lands outside is brought back —, Esc, the focus return and
   the scroll lock as for any modal. `data-overlay-modal="native"` keeps `showModal()` for a light page. Plan §1.14's
   rule, item 3: «If p90 stays > 200 ms, the dialog opens with show() + the shared scrim + a script focus trap …
   proved by keyboard browser tests. Never inert on main alone» — nothing is made `inert` but a leaving panel.
2. **`html:has(:focus-visible) { scroll-behavior: auto; }` (DL54-25) is `html[data-input="key"] { scroll-behavior:
   auto; }`** — the same behaviour (a keyboard focus jumps, a pointer's anchor click stays smooth), read from
   head.js's input flag, set in the key's own capture before the focus moves.
3. **W3-A's `html:has(.console-drawer[open])`** leaves with the console drawer when W2-A's propagation moves it onto
   the system (its lock is `html[data-overlay-lock]`, set by the module): until then every `[open]` on a console page
   — a dialog, a `<details>` — re-styles ≈ 700 elements.

**Why — measured** (lane 8783, Chromium 153 headless, 412 × 823 @1.75, touch, CPU × 4, cold, the panel injected and
the real `dist/overlay.js` imported; `C:/tmp/ile_v5_council/evidence/v54/w2-a/inp/`):
- elements re-styled by a cold opening, traced: `showModal()` 860 on the Arabic «Mes documents», 1 024 on the
  phase-3 home — inertness is a style flag every element inherits; the trapped open 184 / 234;
- `html:has(:focus-visible)` re-styled the whole document on every focus change, so on every press of a link or a
  button anywhere: 3 758 → 181 elements for the same trapped opening once it was removed (style 213 → 34 ms);
- an insertion under the body in the tap re-evaluated the page's `:has()` rules (≈ 720 elements): the scrim is made
  at idle;
- INP (n = 9): the trapped open p90 80 ms on «Mes documents» (W3-A's rule removed, as the propagation will) and
  72 ms on the home; `showModal()` 200 / 168 ms; closes p90 ≤ 80 / 56 ms.

**What the trap gives up, and what holds it.** A non-modal dialog is not in the top layer: the panel stands at
`--z-modal` (the module stacks trapped panels and puts the scrim right under the topmost), so it must sit at the
body's level — no transformed or z-indexed ancestor, which every component's place (the end of the page) respects.
Assistive technology reads `aria-modal`; the pointer meets the scrim; the keyboard meets the trap. The browser tests
prove Esc, the return, the wrap, the focus brought back, the scrim's press, the still page, and the native opt-in.

**Source.** Plan §1.14 (the INP rule, O6, O7), §1.12 item 5; DL54-25 (superseded in its rule, not its intent);
DL54-69; INP_QUIET.md §0, §5; `QA/v54/w2-a/NOTES.md` «INP».

## DL54-90 · 11 October 2026 · W2-A, step 1: the paths written outside the family's slice, each justified

**Decision.** The manifest's merge step writes these into w2-a's slice or names their owner's consent:
- `templates/dev/designpreview/specimens/overlays.html` and `static/css/dev/overlay-board.css` — the family's
  specimen board and its dev-only sheet (W1-D's precedent, DL54-37: a board may not carry a `<style>`; the sheet
  stays out of `main.css`, `test_the_dev_stylesheet_stays_out_of_the_production_cascade`);
- `apps/designpreview/live.py` — one row of `SPECIMEN_BOARDS`, so the preview's index links the board (V5.7: what is
  built is visible);
- `static/css/v5/chrome.css` — one rule (DL54-89 item 2);
- `docs/design/DESIGN_SYSTEM_2026.md` — besides the family's prose (its slice), the figures its own change moved,
  regenerated by `scripts/regen_design_inventory.py --write` (§2 weights and numbering, components.css 18 sections,
  §10 42 files, §16's total) — the steward's regeneration gives the same numbers;
- `static/js/main.js` — inside the family's slice (`initDialogs`): it also closes on the overlay system's «Fermer»
  (`data-overlay-close`) a dialog it opened, on the pages that do not load `overlay.js` yet (the design showcase).

**Source.** Plan §2.2 (the manifest: the steward assigns); V5.5; V5.7; DL54-37, DL54-89.

## DL54-91 · 11 October 2026 · W2-A, step 2: every overlay of a console page on the system

**Decision.** The propagation of plan §1.14, in its order — the console drawer → popovers and menus → modal and
alertdialog → the tooltip group —, on every console page: `console.js` imports `overlay.js` and keeps no overlay of its
own. The decisions met while doing it:

1. **The console drawer is a modal drawer of the system, by the trap** (DL54-89), not `showModal()`: `overlay overlay--drawer`,
   `data-overlay="drawer"`, `data-overlay-edge="start"` on W3-A's `<dialog>`; «Menu» its link opener (`data-overlay-open`,
   still a link without script), the close control the system's «Fermer». W3-A's measures and night stay the drawer's —
   320 px / 88vw over the system's phone rule (a modal drawer full width at ≤ 40rem), the night, the safe areas, the
   `--drawer-radius`, the dark shadow — written on the panel itself, never under `[open]`, so that the «Slide» out keeps
   them (B1). The lock is `html[data-overlay-lock]`: W3-A's `html:has(.console-drawer[open])`, which re-styled ≈ 700
   elements at every `[open]` of a console page, its `::backdrop` and its two keyframes leave (DL54-89 item 3). A window
   widened past 64rem puts the drawer away, the focus to the rail.
2. **The account popover has two faces, one set of rows** (`account_menu.html`). `popover=True` — the console's top bar —
   is a real `<button popovertarget>` and `components/popover.html`, a group named «Mon compte»; the default stays design
   V4's `<details>`, because the letterhead's seat and drawer still draw it and wiring the public popover is W2-C2's (it
   adds `overlay.js` to `shell.js`). `components.css` §8 is deleted (the deletion map); what the details face still
   needs of it — the list hanging from its summary, the rows' flex — went into `v4/shell.css`'s last block, which leaves
   with that face; the trigger's base serves both faces from `v5/overlays.css` §9.
3. **The row menu is the system's popover**, named by the piece's title, opened by «⋮» named by the top-layer tooltip
   (`data-tip="layer"`: the row may sit in a clipping sheet); `v4/workspace.css`'s row popover and `console.js`'s
   placement leave.
4. **`overlay.js` owns the disclosures that are still a `<details data-dropdown>`** (the rail's language): one open at a
   time, `aria-expanded`, Esc, a press outside, the focus leaving — and an open one takes the Esc before the panel it
   stands in, the key's default prevented so no close request reaches the dialog (DL54-69: the language's list goes
   before the drawer). It marks each `data-dropdown="overlay"`; **`main.js`'s `initDropdowns` is a fallback** that leaves
   the marked ones alone — read at the event, since `overlay.js` loads after `main.js` — for the pages that do not load
   the system yet (the letterhead, until W2-C2). **`initDialogs` is gone** with its last caller: the showcase opens its
   dialogs through the system.
5. **The tooltip group: the rail's word is the system's one top-layer tip** (O11 in the product). Three generic hooks
   carry what the rail needs: `data-tip-label` (the words where a control's name is its own content), `data-tip-beyond`
   (beyond the rail's edge, never over the foot's next control; in Arabic on the rail's left), and a cancelable
   `overlay:tip` by which the rail refuses the tip while a word is beside its glyph. A control names nothing while the
   *overlay* it opens is open — not while any `aria-expanded` is true (the rail's own control, whose state is the rail's,
   keeps its word). The word shows on the keyboard's focus (`:focus-visible`), as every tip of the system: W3-A's showed
   on any focus, so a programmatic focus after a pointer's press brought one; W3-A's test reaches the compact rail's page
   by its arrows. `.rail__tip` and sixty lines of its timers leave.
6. **Without script a panel appears and leaves at once** (`html.no-js .overlay { transition: none }`, plan §1.14's
   fallback row): the system's 200 ms way out kept W3-A's drawer on screen after its close link was followed.
7. **The notification centre is not built**: the communications it would list exist (`portal.Message`, the unread count
   of «Communications»), but plan §3.5 item 3 asks its content as an asynchronous fragment, and no view returns one —
   new backend work, which the brief says not to invent. Handed over (`QA/v54/w2-a/NOTES.md`, «Handed to»).

**Why.** One system: a console page had three overlay mechanisms (W3-A's `showModal()` drawer, V4's details menu, a
native popover placed by hand) and two tooltips; the plan asks one, and the INP rule asks the trap (the drawer's open
p90 168 ms, close 128 ms, on the Arabic «Mes documents» at CPU × 4 — `NOTES.md` «Step 2 — measures»). Every behaviour
W3-A's tests pin is kept; the tests follow the mechanism where they named it (`:modal`, a keyframe's name, V4's list).

**Source.** Plan §1.14 (the propagation's order, O1–O11, the INP rule), §3.4 item 1, §3.5 item 3, §2.3 (the deletion map);
DL54-69; DL54-73 item 4; DL54-89; `QA/v54/w2-a/CONTRACT.md` §6; `tests/frontend/test_overlays.py`,
`test_overlays_console_w2_a.py`, `test_overlays_console_browser_w2_a.py`.

## DL54-92 · 11 October 2026 · W2-A, step 2: the paths written outside the family's slice, each justified

**Decision.** The manifest's merge step writes these into w2-a's slice or names their owner's consent:
- `apps/portal/static/portal/v5/_shell.css` (W3-A's) — the drawer's rules on the system (its shape off `[open]`, the
  `:has()` lock, the `::backdrop` and the keyframes deleted, the forced-colours edge on the new selector, a guard for a
  no-script link from 64rem), the account's rows (the coarse rule of V4's links deleted), `.rail__tip` deleted — W3-A
  handed the drawer, the popover and the word over (DL54-73 item 4);
- `static/js/src/console.js` — besides the drawer code (the slice): the import of `overlay.js`, the row menu's placement
  deleted, the rail's word moved onto the system's tip (§1's «rail words», W3-A's);
- `templates/partials/portal_chrome.html` — besides the drawer element (the slice): «Menu»'s `data-overlay-open` and the
  top bar's account include (`popover=True`, plan §3.5 item 3: «the console's use of the account popover»);
- `tests/frontend/test_console_shell_w3_a.py`, `test_console_shell_browser_w3_a.py`, `test_console_phone_browser_w3_a.py`
  (W3-A's) — their pins of the old mechanism (`:modal`, the keyframes, V4's list, `.rail__tip`), every behaviour kept;
- `static/css/v4/shell.css` (W2-C1's; its own header names W2-A for its last block) — what the details face needed of
  `components.css` §8;
- `templates/dev/showcase.html`, `apps/core/dev.py` — the showcase's two dialogs on the system (`initDialogs`' last caller);
- `tests/frontend/test_static_assets.py` — main.js's `showModal` pin, now overlay.js's;
- `docs/ACCESSIBILITY.md` — §3's rows of the dropdowns, the popovers and the dialog family, §4.3's dialog, one row of
  the tests' table;
- `docs/design/DESIGN_SYSTEM_2026.md` — besides the family's prose: §2's rows of `components.css`, `v4/shell.css`,
  `v4/workspace.css`, §10's `document_row.html` clause on its menu, §11.6's sentences on the word and «Menu», §16's
  rows of `main.js` and its paragraph on `console.js`; the figures regenerated by `scripts/regen_design_inventory.py`.

**Source.** Plan §2.2 (the manifest: the steward assigns); DL54-73 item 4; DL54-90.

## DL54-93 · 11 October 2026 · W2-A, the fix pass: a menu sheet stands over the one scrim; the trapped page leaves the accessibility tree; the focus in its panel's view; the rarer parts on demand

**Decisions** (the fix pass of the family's one review, `QA/v54/w2-a/REVIEW.md`, and of its accessibility and performance
check, `QA/v54/w2-a/A11Y_PERF.md`; what was done and measured is the notes' «Review fixes»).

1. **A menu shown as a phone sheet stands over the one scrim — supersedes DL54-88 item 3** (REVIEW M1). At ≤ 40rem the
   popover's sheet draws the shared `.overlay-scrim` under it: opacity only, on the sheet's clocks, and no trap, no scroll
   lock, no `aria-hidden` — it stays a menu (Esc, the focus leaving, a choice). The scrim holds the whole press,
   pointerdown to click (`data-held`, let go on the click, on a cancel, or after a second): the platform light-dismisses
   the menu on the way up, before the click, and that click still lands on the scrim, so the page is never reached —
   the reviewer's taps had focused the register's search field and followed a filter link, fr and ar. The press moves no
   focus (mousedown's default is prevented); the close gives it back where CONTRACT §4 says. The sheet is headed by its
   group name — the `label` of `components/popover.html`, the piece's title or «Mon compte», live strings — as
   `.overlay__caption`, in the small secondary ink, `aria-hidden` (the group's name already says it), drawn only as a
   phone sheet. DL54-88 item 3 refused a scrim because a popover's own `::backdrop` lets every press through and a dim
   layer that does not take the press would only look modal; it did not weigh the system's own scrim, a real element
   that takes the press.
2. **The page behind a trapped panel leaves the accessibility tree — amends DL54-89's «what the trap gives up»**
   (A11Y_PERF M2). DL54-89 assumed «Assistive technology reads `aria-modal`»; Chromium prunes nothing for it (357 nodes
   kept with the console drawer open, against `showModal()`'s 107). While a trapped panel is open every element beside
   its way up to the body is `aria-hidden="true"` — written once the focus is in, taken back before it comes out, so the
   focus never stands in a hidden subtree; an element hidden by its own markup is left as it is —, never `inert`, a
   style flag every element inherits (DL54-89's measure). No rule of the project selects `aria-hidden`
   (`tests/frontend/test_overlays.py` guards it), so nothing is re-styled. Measured: the tree as `showModal()`'s — the
   dialog and its «Menu» alone, 107 nodes —, the page whole again on close, the focus back on «Menu».
3. **A focus the module moves comes into its panel's view** (A11Y_PERF M1, WCAG 2.4.7): still `preventScroll` for the
   page, then `scrollIntoView({ block: "nearest", inline: "nearest" })` when the target stands in an open panel — fixed,
   over a locked page: only the panel's own list can move. «Academy», every rail's last page, is whole in the staff
   account's drawer at 390 × 844, 844 × 390 and, in Arabic, 320 × 568, by tap and by key; Shift+Tab's wrap lands in
   view; the page stays at 0.
4. **The layer tip follows a scroll** (A11Y_PERF M3): re-placed while its control keeps the keyboard's focus or the
   pointer and its middle is its own on screen (`elementFromPoint`), put away otherwise. The compact rail's words: every
   item of the staff account's scrolling list, fr and ar, and the person's.
5. **The rarer parts are a chunk of their own, imported on demand** (A11Y_PERF M4). The grip of a sheet, Back, the
   placement without anchor positioning, a dialog's scrolling body made a stop (A11Y_PERF m1: `tabindex="0"` while it
   overflows with nothing to focus — what Chromium and Firefox do and Safari does not) and a native modal's backdrop
   press live in `static/js/src/overlay/extras.js`. `overlay.js` imports it at idle where a page draws one of them, at
   once where the engine has no anchor positioning, and hands it what the parts need (`install(core)`: the file imports
   nothing); no console page fetches it. Weights (gzip −9 without a name, the bundles rebuilt from a clean dist): the
   core chunk every console page loads **6 491 B** (6 472 B before, the five fixes now inside it), the on-demand chunk
   **1 600 B**; `dist/main.css` 44 523 B (+57 B: the head line, the held scrim, the scrolling body's ring);
   `dist/portal/console.css` 5 061 B unchanged. The module stays over plan §2.6's 4 KB, and the three sheets every
   console page loads weigh 51 847 B — 1 906 B over the branch base's 49 941 B (A11Y_PERF M4: +1 849 B), 1 840 B over
   DL54-73's recorded 50 007 B: **the merge step records the module budget and the page types' ceilings here**, as
   DL54-44, DL54-73 and DL54-76 did, with A11Y_PERF's timings (LCP
   +34 ms pooled over the eight console cells, every cell within the before set's resolution; the first-render task
   +3 ms).
6. **The account trigger's name** (REVIEW m3): «‹short name› — Mon compte» — the words it shows first (WCAG 2.5.3), then
   what it opens; two live strings and the em dash the console's tiles already use.
7. **Left, as the review asked.** The drawer's cold open on the INP edge (REVIEW m1): no change to ship — Wave 4's
   measure on a quiet machine and a real mid-range Android decides; if its p90 still exceeds 200 ms, plan §1.14's INP
   item 1 lays the closed drawer out at idle. O10, the WebKit and Firefox smoke (REVIEW m2): Wave 4's cross-engine
   pass, before W2-C2 ships the public phone sheet on the same module.
8. **Paths outside the slice** (the manifest's merge step writes them): `static/js/src/overlay/extras.js` — the
   module's rarer parts (the slice names `static/js/src/overlay.js`); `static/css/components.css` — one selector, V2's
   `.dialog[open]`, deleted from the universal reduced-motion block, which is W1-D's slice: §21's leftover (w2-a's
   slice names §8 and §21), deleted at the review's request (REVIEW m4), the block's other guard untouched;
   `templates/dev/designpreview/specimens/overlays.html` (DL54-90) — the board's account popovers named «Mon compte»;
   `tests/frontend/test_console_shell_w3_a.py` (DL54-92) — its pin on the trigger allows the name. Generated:
   `static/js/dist/chunks/extras-*.js`.

**Source.** `QA/v54/w2-a/REVIEW.md` M1, m1–m4; `QA/v54/w2-a/A11Y_PERF.md` M1–M4, m1; plan §1.14 (the INP rule, O10), §2.6;
DL54-44; DL54-73 item 3; DL54-76; DL54-88 item 3; DL54-89; DL54-90; `QA/v54/w2-a/NOTES.md` «Review fixes»; `QA/v54/w2-a/CONTRACT.md`
§1–§4, §6, §7; `tests/frontend/test_overlays.py`, `test_overlays_console_browser_w2_a.py`, `test_overlays_browser_w2_a.py`.

## DL54-94 · 11 October 2026 · W2-A, the budget fix: the panels with a head are page-only; the shared sheet written once; dead rules deleted, each proved; every page type under its ceiling; the module's figure recorded

**Decisions** (the shared-CSS gate stopped the w2-a merge on 11 October at 20:49 — `QA/v54/w2-a/NOTES.md` «Steward»;
the owner's V5.8: the shared ceilings are hard, a surface's own CSS goes into page-only sheets, reuse and delete first,
no quality cut; what was done and measured is the notes' «Budget fix»).

1. **design-v5 merged into the branch first** (77 commits: W2-B's login, the static pipeline, W3-B's dashboards).
   design-v5's numbers stay (DL54-74 … DL54-87); W2-A's six entries follow as DL54-88 … DL54-93 (add 14), their
   cross-references moved with them — but DL54-93 item 5's «as DL54-44, DL54-73 and DL54-76 did», which names
   design-v5's own DL54-76 (the steward's record of the w2-b merge); DS 2026's five hunks as the steward's guide resolves
   them; the bundles rebuilt from a clean dist. Weighed the stewards' way (`gzip.compress(data, 9)`): `main.css`
   44 022 B, the console page types 52 840 B — 1 913 B over their 50 927 B.
2. **What no product page draws is page-only.** The dialog and the alert dialog, the bottom sheet and its grip, the head
   / body / foot anatomy of `dialog.html`, `sheet.html` and `drawer.html` (with a drawer beside the list's phone sheet),
   a native modal's `::backdrop`, and the control's own CSS tooltip with its warm group (`@property --tip-warm`) leave
   `v5/overlays.css` for the partial `static/css/v5/_overlay-panels.css`, carried by an entry of its own,
   `apps/core/static/core/overlay-panels.css` → `css/dist/core/overlay-panels.css` (2 071 B gzip), its import written in
   the collected tree (DS 2026 §2). `core` because the overlay system is no app's and `core` is the app of the
   cross-cutting interface (chips, icons, the template tags): an app sheet is an entry `scripts/build_css.mjs` builds
   without a change to it. Linked today by the overlay board and the design showcase only. **The rule** (CONTRACT §1):
   a page that draws a dialog, an alert dialog, a bottom sheet, a drawer of `components/drawer.html`, a native modal or a
   CSS tooltip links it in its `extra_head` — W3-E's staff dialogs, W3-F2's danger confirmation, W3-C's preview drawer
   and filter sheet, W2-C2's phone sheet if it is the sheet family; `test_overlays.py` refuses a template that draws one
   without the link. The partial comes after `main.css`, so it says reduced motion, forced colours, paper and tier 0
   again after its families. The orchestrator's list named the dialog, the sheet and the backdrop; the CSS tooltip goes
   by the same rule — the product's words are the top-layer tip (`data-tip="layer"`), which stays shared — and is worth
   409 B on every page (put back into today's `main.css`; the panels 708 B more, `gzip.compress(data, 9)`). Seen: the
   board's computed styles, every element and every pseudo-element that draws, in eleven
   states (the alert, the dialog with a field, both drawers, the sheet, the phone sheets, the menu, the CSS tip on focus),
   identical to the merged single bundle's (`evidence/v54/w2-a/budget/cmp_board.json`).
3. **The shared sheet is written once per declaration** (`v5/overlays.css` 31.6 → 22.3 KB of source): the popover and
   the dialog leave on the panel's own clocks instead of a copy of them; `--overlay-scrim-in` and `--overlay-drag` move
   where they are read (the native backdrop, a sheet's grip); the phone popover's two rules are one, without the
   declarations its panel already has; the top-layer tip's box is one rule; `.tooltip::backdrop` leaves (the platform's
   popover backdrop is transparent and takes no press); tier 0 is one list.
4. **Dead rules deleted from the shared bundles.** A selector is dead when it names at least one class, id or attribute
   outside `:not()` and none of its classes, ids or attributes appears in any template, Python, JS, JSON or SVG file of
   design-v5, of this branch and of the in-flight trees `v54-w3-c`, `v54-w3-d`, `v54-w3-f1`, `v54-w3-f2` (tracked and
   untracked), nor in the installed Django forms and allauth packages, nor as a prefix or suffix a template, Python or JS
   builds a class from (`x--{{ v }}`, `f"x--{v}"`, `` `x--${v}` ``, `"x--" + v`); a rule goes when every selector of its
   list is dead. 77 selectors (65 whole rules, 12 out of a list; 59 names) in eight sheets — `components.css` §12's entrance leftovers, `_legacy-tokens.css`'s seven
   `.text-*`, `base.css`'s unused roles, `layout.css`'s zones, columns and utilities, `register.css`'s verso plate and
   archive caption, `v5/base.css`'s `.on-image` focus and `.t-entry`, `v5/field.css`'s `.form__intro`, `portal.css`'s
   `.portal__aside`; each with its grep in `evidence/v54/w2-a/budget/dead_rules_proof.json`. Left: `.section--inverse`
   and `.container--narrow`, which `v54-w3-f1` deletes in its own merge (no conflict made for it), and `.section--d`,
   the one consumer of `--rank-d-block`, which DS 2026 §3 documents as used.
5. **The console drawer's copied declarations go** (`v5/_shell.css`, DL54-92's path): its place, its flex column, its
   box and its start corners are the system drawer's (`.overlay--drawer[data-overlay-edge="start"]`); its measures, its
   night and the `display` that outweighs `.console-drawer { display: none }` stay (−34 B on `console.css`).
6. **Every page type under its ceiling** (gzip −9, the bundles rebuilt from a clean dist): an interior page 42 152 B
   (ceiling 42 540), the login 47 013 (47 392), the home 56 803 (57 191), the console page types 50 893 (50 927), «Mes
   pièces» 52 065 (52 099), the company's dashboard 51 766 (51 800) — design-v5 41 880 · 46 741 · 56 531 · 50 927 ·
   52 099 · 51 800. On the product's pages nothing that is drawn changed: the computed style of every element, in the
   drawer, the account popover (sheet and anchored), the row menu (anchored and sheet), the rail's word, at rest and on
   six public pages, equals the merged bundle's but for custom properties no rule of those pages reads (`--tip-warm`,
   `--overlay-drag`, `--overlay-scrim-in`), a menu body's flex and overscroll (no box moved), and the invisible touch
   ring of «⋮» (W3-C's `.doc-row__more::after`, 2 px around the 44 px button under a coarse pointer), which the CSS
   tip's rules hid by accident — on every phone (`[data-tip]::after` at ≤ 40rem), elsewhere while its menu was open —
   and which now gives the 48 px target W3-C wrote
   (`evidence/v54/w2-a/budget/cmp_styles.json`; the home's and the login's other differences are their own animations,
   the same in a control run with identical bundles).
7. **The module's figure is recorded** (not a V5.8 ceiling): the core chunk every console page loads is 6 466 B gzip
   against plan §2.6's 4 KB, the rarer parts 1 600 B on demand. The dialog's and the sheet's own code in the core is at
   most ≈ 300 B (measured by stubbing it out) and is synchronous behaviour — the alert's safe answer, the guard of
   unsaved input against the scrim, a drawer beside the list opened as a sheet on a phone — that a lazy chunk would lose
   for an interaction made before it arrives: it stays. The rest is what a console page uses.
8. **Supersedes DL54-93 item 5's request** («the merge step records … the page types' ceilings»): V5.8 forbids a raise,
   and no page type needs one.
9. **Paths outside the slice** (the manifest's merge step writes them): `static/css/v5/_overlay-panels.css` (new, the
   system's page-only partial; the slice names `v5/overlays.css`), `apps/core/static/core/overlay-panels.css` (new, its
   entry); the dead rules' sheets — `static/css/_legacy-tokens.css`, `static/css/base.css`, `static/css/layout.css`,
   `static/css/register.css`, `static/css/components.css` (§12, W2-E's row of the deletion map), `static/css/v5/base.css`
   (W1-A), `static/css/v5/field.css` (W1-C), `apps/portal/static/portal/portal.css` (W3-A); `apps/portal/static/portal/
   v5/_shell.css` (DL54-92); `templates/dev/showcase.html` (DL54-92) and `templates/dev/designpreview/specimens/
   overlays.html` (DL54-90), which link the entry; `static/css/v5/chrome.css` and `docs/ACCESSIBILITY.md`, one DL number
   each; `tests/frontend/test_loader_rules.py` (W1-D's), whose anchor on the console drawer's opening tag step 2's
   classes had broken (`<dialog class="console-drawer overlay overlay--drawer"`): read on its first class now, the
   assertion unchanged. Generated: `static/css/dist/core/overlay-panels.css`.

**Source.** The owner's V5.8 (`C:/tmp/ile_v5_council/directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`) and the V5_5
addendum of 11 October 19:40; plan §2.3 (page-only CSS, the deletion map), §2.6 items 3 and 5; DL54-73; DL54-76;
DL54-87; DL54-93; `QA/v54/w2-a/NOTES.md` «Steward» and «Budget fix»; `evidence/v54/w2-a/merge/budget_gate.log`;
`QA/v54/w2-a/CONTRACT.md` §1, §7; `tests/frontend/test_overlays.py`.

## DL54-95 · 12 October 2026 · Steward, the w2-a merge: nothing to renumber, the 24 paths assigned, the shared CSS gate passed on the ceilings as recorded, the module's figure recorded

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w2-a` into design-v5 on 12 October 2026 —
what the family's own entries hand to the merge step: DL54-90, DL54-92, DL54-93, DL54-94; `QA/v54/w2-a/NOTES.md`
«Steward» (the stop of 11 October, 20:41–20:48) and «Budget fix» §6 «For the merge»).

1. **Nothing to renumber.** design-v5 stood at `1c03e3b` — the commit the budget fix had merged into the branch
   (`9c8571d`) — so `git merge design-v5` found the branch up to date. W2-A's seven entries keep the numbers the budget
   fix gave them, **DL54-88 … DL54-94** (DL54-94 item 1; the notes' «Budget fix» §1 says how to read the numbers
   written before it); this entry is DL54-95.
2. **The 24 paths outside the slice are this area's in the manifest** (`5418565`). `scripts/check_ownership.py w2-a
   1c03e3b` listed exactly the paths the family declares; each was read in the diff and found to be what it declares.
   Whole files, the system's own and new: `static/css/v5/_overlay-panels.css` and its entry
   `apps/core/static/core/overlay-panels.css` (DL54-94 item 2), `static/js/src/overlay/extras.js` (DL54-93 item 8),
   the overlay board `templates/dev/designpreview/specimens/overlays.html` and its sheet `static/css/dev/overlay-board.css`
   (DL54-90). Slices: the board's row of `apps/designpreview/live.py`; the showcase's demo (`apps/core/dev.py`) and its
   «Surcouches» section with the page-only sheet's link (`templates/dev/showcase.html`); W3-A's
   `apps/portal/static/portal/v5/_shell.css` (the drawer and the rail's word on the system) and its three test files,
   retargeted with their intents kept; W1-D's `tests/frontend/test_loader_rules.py` (one anchor);
   `tests/frontend/test_static_assets.py` (no `showModal` in `main.js`); `static/css/v4/shell.css` (the details face's
   position that `components.css` §8 held); `static/css/v5/chrome.css` (`html[data-input="key"]`, DL54-89);
   `docs/ACCESSIBILITY.md`'s rows; the dead rules deleted from `_legacy-tokens.css`, `base.css`, `layout.css`,
   `register.css`, `v5/base.css`, `v5/field.css` and `portal.css` (DL54-94 item 4). Five slices are named as written:
   `templates/partials/portal_chrome.html` (the drawer and the top bar's account popover), `static/js/src/console.js`
   (the drawer, the row menu's placement, the rail's word on the system's tip), `static/css/components.css` (§8 and §21;
   §12's dead entrance leftovers and V2's `.dialog[open]`), `static/css/main.css` (the system's import line) and
   DS 2026 (the prose as it follows the system). The check after it: 22 inside, 28 slice, 23 generated, and the
   manifest itself, the one steward-only path (before: 24 outside); `--validate`: coherent, 25 families, 538 entries.
3. **The shared CSS gate (the owner's V5.8) passes on the ceilings as recorded.** On the bundles rebuilt from a clean
   `static/css/dist` and `static/js/dist` (byte-identical to the family's committed bundles), `gzip.compress(data, 9)`:

   | Page type | design-v5 `1c03e3b` | merged | change | ceiling |
   |---|---|---|---|---|
   | console page types (`main` + `console` + `portal`) | 50 927 | 50 893 | −34 | 50 927 (DL54-87 item 3) |
   | «Mes pièces» (+ `documents.css`) | 52 099 | 52 065 | −34 | 52 099 |
   | the company's dashboard (+ `companies.css`) | 51 800 | 51 766 | −34 | 51 800 |
   | an interior page (`main.css`) | 41 880 | 42 152 | +272 | 42 540 (DL54-73 item 3 + DL54-76 item 5) |
   | the login (+ `entrance.css`) | 46 741 | 47 013 | +272 | 47 392 (DL54-76 item 4) |
   | the home (+ `hero.css`, `pages.css`) | 56 531 | 56 803 | +272 | 57 191 (DL54-87 item 3) |

   `dist/main.css` 41 880 → 42 152 B (the overlay system's shared sheet, less 77 dead selectors), `portal/console.css`
   7 072 → 6 809 B, `portal/portal.css` 1 975 → 1 932 B; new and fetched only where it is linked,
   `core/overlay-panels.css` 2 071 B. **No page type is over its ceiling; none is raised, none recorded anew; none is
   lowered** (none lands more than 1 KB under it, §2.6 item 3). The console page types — the owner's named concern — are
   34 B lighter than before the merge. The ceilings read are the page types' as the log records them — plan §2.6 item 3's
   «measured total at the end of Wave 1», with item 5's one raise per page type —, the reading of the stop of 11 October
   and the target the budget fix met. **Named for the orchestrator, not decided here:** the orchestrator's note on V5.8
   writes the shared ceilings as «`main.css` as it stands at `v54/w3-b`»; read as that sheet's weight there (41 880 B),
   this merge is 272 B over it on every public page type, which draws nothing of the overlay system today (the
   letterhead keeps the account's details face until W2-C2). The lever, if that reading is the one meant: the
   console-only parts of `v5/overlays.css` (the drawer, the popover, the layer tip) into `console.css` — the console
   page types unchanged, the public page types lighter — until W2-C2 brings the popover to the letterhead.
4. **The page-only sheet and its rule.** `css/dist/core/overlay-panels.css` is linked today by the overlay board and
   the design showcase only. CONTRACT §1 binds every family that adopts a dialog, an alert dialog, a bottom sheet, a
   drawer of `components/drawer.html`, a native modal or the CSS face of `components/tooltip.html` to link it in its
   `extra_head` — W3-E (the staff consequence dialogs), W3-F2 (a danger confirmation as a dialog), W3-C (the preview
   drawer and the filter sheet), W2-C2 (its phone sheet, if it is the sheet family);
   `test_overlays.py::test_the_panels_are_page_only_and_linked_by_the_pages_that_draw_them` refuses a template that
   draws one without the link. The in-flight trees still carry W3-A's console drawer in `portal_chrome.html`: their
   merges meet W2-A's version (the slice above).
5. **The module's figure is recorded, not met.** Plan §2.6's JS row gives the overlay module ≤ 4 KB gzip; the core
   chunk every console page loads (`chunks/chunk-4PT2QVVC.js`) is **6 466 B**, the rarer parts 1 600 B on demand
   (`chunks/extras-*.js`, fetched by no console page), `dist/console.js` 2 038 → 1 505 B; on every page the runtime
   helpers' chunk (394 B) is new and the motion library's chunk 253 B lighter. Not a V5.8 ceiling; the family's measure
   and its reason for not moving more into a lazy chunk are DL54-94 item 7. Left to the orchestrator, with REVIEW m1
   (the drawer's cold open on the INP edge) and m2 (O10, the WebKit and Firefox smoke), handed to Wave 4.
6. **The inventory and the capture report.** `scripts/regen_design_inventory.py` found one stale figure — DS 2026 §2's
   weight of `layout.css`, written by hand as 7.5 KB, 7 784 B after the deletions — and wrote 7.6 KB on the branch
   before the targeted tests (`1c6e39b`), so that the tree tested is the tree that lands. The capture report is
   unchanged: `capture.py` captures the home, the privacy page, the login and the 404, which draw nothing of the
   overlay system; what changed for them in `main.css` is the system's rules, which match none of their elements, and
   selectors proved to match no file (DL54-94 item 4); the family's computed-style comparison found nothing drawn
   changed on the home and the login (DL54-94 item 6).

**Why.** Entries already numbered after design-v5's need no move; paths nobody holds would have no writer for the next
family; a gate read one way at the stop and another at the merge would move the target after the family met it — and a
reading the steward cannot settle is worth naming with its lever, so that the orchestrator rules on it once.

**Source.** The owner's V5.8 (`C:/tmp/ile_v5_council/directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`, and the
orchestrator's reading below it) and the V5_5 addendum of 11 October 19:40; plan §2.2 (the manifest: the steward
assigns; merge step 3), §2.3, §2.6 items 3 and 5 and its JS row; DL54-73 item 3; DL54-76 items 4 and 5; DL54-87 items 3
and 5; DL54-88 … DL54-94; `QA/v54/w2-a/NOTES.md` «Steward» and «Budget fix»; the weights in
`evidence/v54/w2-a/merge/budget_gate_final.log` and `js_weights_final.log`; the ownership checks in
`evidence/v54/w2-a/merge/ownership_before.log` and `ownership_after.log`.

## DL54-96 · 11 October 2026 · W3-F2, step 1: the content and legal pages as built — «la lettura»

**Decision.** Built by W3-F2 (step 1: the content and legal pages) on plan §3.5 item 2 and §1.18 D26, with these choices
met during the build (plan §5.2: one entry, its reason, its evidence):

1. **One page partial, one entry.** The area's rules are `static/css/v5/_lettura.css`, imported by one page sheet,
   `apps/cms/static/cms/lettura.css` (the `cms` app: the content's own), which every page of the area loads after
   `main.css` — not one entry per app: the FAQ, the glossary, the news, «Vivre en Italie», the partners, the Forum
   Virtuel, the enquiry forms, the legal pages and the consents are read one after the other, and one cached sheet
   serves them all. The re-drawings of main.css's components (the trail, the page header, the search, the pagination,
   the empty state) are scoped by the body class `lettura`; the import is written in the collected tree (DS 2026 §2).
2. **The interior's grammar, value for value.** Trail, head, chapters with one section device (`ile-steps` + the title,
   4 | 8 and sticky from 75rem), the register, the quiet foot — the home's chapters (W2-D) and the doors' (W3-F1, read
   on its branch, not imported: it is not on design-v5), under the same class names, so that one partial can later
   import the other's common part. The FAQ's and the glossary's search sits in the head's end seat (7 | 5 from 64rem).
3. **The glossary is a visible register, not the disclosure.** A definition is a line or two: folding it would double
   the reader's work for nothing, and PX25 draws an index and a register. One band for every letter (groups 40 px
   apart, the letter the group's head), the letter index a band that sticks under the letterhead from 48rem (PX25; a
   phone keeps it as a block of its own: on one row from 48rem, several on a phone). The FAQ keeps the system's
   disclosure (v5/tabs.css), its keyboard model the native one.
4. **The empty page draws no dashed box.** On V5 a broken edge is the register of «attesa», what is due; an empty list
   owes nothing. Under `.lettura` the empty state is DS V5 §10.8's page empty state: the domain's glyph on its 40 px
   disc (W1-B's floors kept), the title at 20/28, one sentence, one action, at the reading edge on a hairline.
5. **D26 as layout slots, the headings verbatim.** The verification line only where a date exists; one inset (a sheet's
   general-information sentence on the institutional notice's paper, a legal page's courtesy translation or pending
   notice, the companies' prescribed quote); one action (the page's one primary — no page of the area needs the raised
   action card); an authority's host beside each official source (`{{ url|host }}`); a caption and a credit under an
   article's photograph; «who can help me» in live words only — «Vous n’avez pas trouvé de réponse ? Contactez-nous»
   (the FAQ's), «Besoin d’aide ? Écrivez-nous :» (the account pages' and the login's) with the one address on the
   legal pages and the sheets. The question headings and the slot's own wording are proposed in the family's NOTES for
   B1 item 7, not written.
6. **The legal page keeps the markup the i18n tests pin** (`<article class="container legal-page" lang="it">`,
   `<p class="legal-page__meta" lang="…">`, `data-gate="legal-blocked"`): one column at the reading edge, not a band.
7. **A fallback `lang` stands on the text that holds the fallback, not on its container**, so the interface's words
   inside keep the page's language and a French body on an Arabic page reads left to right with its punctuation in
   place (a prose block in another language takes `direction: ltr` as a whole).
8. **A prescribed text goes into `<title>` and into a `<meta>` attribute as text.** On the Forum Virtuel's non-French
   pages the `locked` tag's `<span lang>` ended the description's attribute and the prescribed text spilled above the
   letterhead (older than this family; fixed, tested).
9. **The paths outside the slice** (for the merge step to write into the manifest): `static/css/v5/_lettura.css`,
   `apps/cms/static/cms/lettura.css` (its dist output generated), `apps/cms/templatetags/lettura.py` (`host`,
   `locked_title`), `apps/living/catalogue.py` (W1-B's hand-over: the seed's glyphs are the registry's LIVING map),
   DS 2026 §2 (the two figures `regen_design_inventory.py --write` computes for the deleted sections, and the row's
   prose).
10. **The interior page type stands over its Wave-1 ceiling.** `dist/main.css` −322 B gzip (components.css §20, §28 and
    §22's dead rules deleted); `dist/cms/lettura.css` 3 724 B gzip on the content pages: an interior page 45 865 B,
    1 379 B over 44 486 B. The bust rule's steps 1 and 2 are done; the LCP A/B on the lane (slow 4G, CPU ×4, the sheet
    served uncompressed — an upper bound) adds 44–104 ms, every LCP ≤ 2.1 s, CLS ≤ 0.001, no task over 114 ms. Left to
    the merge step's record under V5.5's performance rule, as DL54-44, -73 and -76 did.

**Source.** Plan §3.5 item 2, §1.18 D26, §1.3, §1.4, §1.7, §1.16, §2.3, §2.6; DESIGN_SYSTEM_V5 PX17, PX18, PX24 … PX26,
§10.8; DL54-15, DL54-33, DL54-47; the owner's V5.5 directive; `QA/v54/w3-f2/NOTES.md` (step 1).

## DL54-97 · 11 October 2026 · W3-F2, step 2: the error and account pages as built — «le pagine di servizio»

**Decision.** Built by W3-F2 (step 2: the 400 / 403 / 404 / 410 / 429 / 500 errors, the profile and the account's
management pages) on plan §3.5 item 2, with these choices met during the build (plan §5.2: one entry, its reason, its
evidence):

1. **One quiet page for every status, in the interior's grammar.** What happened (the status as the head's label —
   «Erreur 404», the document title's words, decorative —, the title and the sentence verbatim), what to do (one
   primary, the home; the way back with script), the way on (the recovery navigation as a quiet chapter: a label, not a
   title), «who can help me» in the account pages' live words. The V4 numeral at 7rem and the at-sign button are gone;
   the one forward arrow stays on the primary — the action that goes on —, the way back has none. The 403 offers the
   sign-in as its primary to a person who is not signed in (its sentence asks for it); a signed-in person gets the home
   and the way back.
2. **400 and 500 are self-sufficient.** `core.views` renders them without the request — no context processor, no
   database, no session —, as Django's own `bad_request` and `server_error` do: a request that could not be read or a
   failed server may have taken any of these with it, and a 500 that queries the database inside a broken transaction
   fails twice. The frame is `templates/errors/standalone.html` (the letterhead's lock-up on paper, no menu, no switch
   of language, main.css and the page sheet, head.js and main.js for the back link); the public address and the
   project's name come from settings. If even the template fails (a lost manifest entry), the view answers a bare page
   of the same catalogue words, naming nothing. 403, 404, 410 and 429 stay in the public shell: they answer a visit,
   and the site's navigation is the way on. W2-B's root `templates/429.html` keeps the page's content for a signed-in
   person, untouched.
3. **The account pages stay on the public shell, in one frame.** They sat in neither the console (W3-A) nor the
   entrance (W2-B): the console needs `portal_nav` from producers that allauth's views are not, and the plan lists them
   with the public interior. One frame (`allauth/layouts/base.html` → `manage.html`) now holds the profile, allauth's
   management pages and the deletion request: the trail (Accueil › Espace réservé › Mon compte › the section, read
   from the address — allauth's views give none), the account's sections in the chapter head's seat from 64rem (a band
   above the page below), the page in the body's eight columns. It replaces two lists and two drawings — the profile's,
   which floated over its title under the header menu's class names (W1-C's «seen on the way»), and allauth's side list.
   The way to the reserved area and the sign-out stay the letterhead's account menu; «Mes documents» moved to the
   person's data.
4. **allauth's elements keep their class names; the page draws them.** `account-page__title`, `account-page__text`,
   `account-panel` are drawn under `.conto`, and the product's two pages use the same names — one drawing for both. The
   entrance's elements are not touched; one management variant only: `button__manage.html`, so that a page has one
   primary («Rendre principale» beside «Ajouter un e-mail», «Générer de nouveaux codes» beside «Télécharger les
   codes» become secondaries).
5. **The danger action keeps today's confirmation.** W2-A's tag is not on design-v5, so the deletion stays behind its
   own page: the profile's danger button (the garnet outline) leads to it; the password and the mandatory box confirm;
   «Annuler» first, the destructive answer last. allauth's own confirmations (an address's removal, the authenticator's
   deactivation, new recovery codes) are allauth's. With W2-A's overlay, the deletion's confirmation can become its
   alertdialog — a change of `accounts/delete_request.html` and the profile's button only.
6. **Not built:** a page of sessions — `allauth.usersessions` is not installed (no page exists); the CSRF failure
   (`templates/403_csrf.html`) — no live sentence fits a form whose token expired, and the generic 403's («vous n’avez
   pas les droits…») would mislead: a new sentence is B1 copy.
7. **The paths outside the slice** (for the merge step to write into the manifest): `static/css/v5/_servizio.css`,
   `apps/cms/static/cms/servizio.css` (its dist output generated), `apps/core/views.py` (`error_400`, `error_500`: the
   self-sufficient render), `templates/errors/standalone.html` and the error partials are inside the slice's globs;
   DS 2026 §2 (the figures `regen_design_inventory.py --write` computes for components.css, the row's prose, the two
   page sheets' rows) and §10 (the entries citing the rewritten templates).
8. **The weight.** `dist/main.css` 42 141 → 41 814 B gzip (components.css §26 whole; §27's frame, card and panels);
   `dist/cms/servizio.css` 2 353 B gzip on the service pages only: an error or account page 44 167 B, under the
   interior ceiling (44 486 B).

**Source.** Plan §3.5 item 2, §1.3, §1.4, §1.8, §1.18 D26, §2.1, §2.3; DL54-15; the owner's V5.5 directive;
`QA/v54/w3-f2/NOTES.md` (step 2).

## DL54-98 · 12 October 2026 · W3-F2, the fix pass: the door at rest, the Latin heads of the Arabic pages, the refused newsletter

**Decision.** The fix pass on the family's one review and its accessibility / performance check (V5.5:
`QA/v54/w3-f2/REVIEW.md`, `A11Y_PERF.md`), with these choices met on the way (plan §5.2):

1. **The error pages seat the door at rest** (CD §0 item 2, brand act 1 «La porta … error pages (static)», §1.4 law 5,
   §20; DS V5 PX21; the review's M1). `templates/errors/_door.html` draws the entrance's stage — the arch, the owner's
   photograph as served (`static/brand/v5`), the solid navy inner door, the three steps, the outline — with the key OUT
   of the lock: the verbatim key set down on its side on the top step (its box the stage's key box, moved to x 429.333,
   y 414.467 and turned 90°: bow at the door's right, bit down). No light — no glow at the keyhole, no lit frame, no lit
   steps —, nothing moves, never mirrored (the stage stays `direction: ltr`); decorative, static files only, so the 400
   and the 500 stay self-sufficient. Compact (5rem) above the label below 64rem; from 64rem in the head's end seat, one
   grid row with what happened and what to do (`.error-page__body`, one block, so that nothing in it stretches), its
   threshold on the actions' line when the words are the taller; the arch, not its box, on the edge; no shadow on paper.
2. **The door's paint loads where the door is.** W2-B's `static/css/v5/_door.css` is imported by a page sheet of the
   error pages, `apps/cms/static/cms/errori.css` (the door stage, the service pages' partial, the door's seat), which the
   two error frames load instead of `cms/servizio.css`: the account pages keep their sheet without the door (V5.8: a
   surface's CSS where it is used; `dist/cms/servizio.css` gains only the fix pass's account rules). Not
   `components/doorway.html`: its paint is `v4/hero.css` in `main.css`, which is to leave it.
3. **One rule for the Latin heads of an Arabic page** (the review's M2 and m8). A heading — a page's or a chapter's
   title, a glossary's Italian term, a FAQ's French question, a register's title (the Forum Virtuel's rooms) — ends on
   its cell's reading edge (`text-align: end`, the run keeping its `ltr`); a head's paragraph (a lead, an eyebrow, a
   chapter's lead, a topic's introduction) is a box the width of its words pushed onto the reading edge
   (`inline-size: fit-content; margin-inline-start: auto`): one line ends there as a heading does, a longer text reads
   from its own start as a body does; bodies keep their own start. W3-F1's review m7 asks the same of the doors: the
   steward shares the rule.
4. **A refused form lands on the system's summary** (the review's M3, A1): the newsletter opens with
   `components/form_errors.html`, as the enquiry forms and the deletion do; its consent's `label_lang` (`apps/news/forms.py`)
   keeps the French label marked in the summary.
5. **Found on the way and fixed:** the official Italian legal text read right to left on the Arabic page (its `lang`
   is the article's; the rules keep a foreign text `ltr` by the element's own attribute) — now left to right from its
   own start, and the courtesy translation's box stands as a French quote's.
6. **The paths outside the slice** (for the manifest): `apps/cms/static/cms/errori.css` (an app entry, plan §2.3; its
   `dist` output generated), `apps/accounts/profile_forms.py` (A2: the input purposes, three widgets),
   `apps/news/forms.py` (one line, item 4) — beside step 1's and step 2's seven.
7. **The weight** (gzip -9): `main.css` and the console bundles untouched by the fix pass (the shared payload does not
   grow); `cms/lettura.css` 3 718 → 4 056 B, `cms/servizio.css` 2 340 → 2 426 B, `cms/errori.css` 3 619 B (the error
   pages load it instead of servizio.css). On the review's merged tree (main.css 41 155 B): a content page 45 211 B (725
   over the Wave-1 interior figure), an error page 44 774 B (288 over), an account page 43 581 B (under) — the page-only
   sheets are where V5.8 wants this CSS; the merge records the page types as DL54-44, -73 and -76 did.

**Source.** Plan §3.5 item 2, §1.4 SP-8, §1.16, §1.18 D26, §2.3, §2.6; CREATIVE_DIRECTION_V5 §0, §1.4, §20; DS V5 PX21;
the owner's V5.5 and V5.8; `QA/v54/w3-f2/REVIEW.md`, `A11Y_PERF.md`, `NOTES.md` («Review fixes»).

## DL54-99 · 12 October 2026 · Steward, the w3-f2 merge: the family's three entries renumbered, the ten paths assigned, the shared CSS gate passed with the shared payload 688 B lighter on every page type, three ceilings lowered, the three page types recorded

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w3-f2` into design-v5 on 12 October 2026 —
what the family's own entries and notes hand to the merge step: DL54-96, DL54-97, DL54-98; `QA/v54/w3-f2/NOTES.md`
«For the merge (the steward)»; `QA/v54/w3-f2/A11Y_PERF.md` P1).

1. **The numbering.** design-v5 stood at `abbabda` (W2-A's shipped note): the static pipeline's record, W3-B's and
   W2-A's entries and the records of their merges had taken DL54-77 … DL54-95, so the pre-merge sync (`f4f344e`) gave
   the family's three entries **DL54-96 … DL54-98** (add 19; their headings and index rows only — no entry cites
   another of the three, and the code and DS 2026 cite none of the moved numbers); the notes' closing section says how
   to read the numbers written before (`95102da`). This entry is DL54-99.
2. **Four conflicts, both areas' work kept.** `static/css/components.css`: W3-F2's §20 (to `v5/_lettura.css`) and
   W2-A's §21 (to `v5/overlays.css`) are both gone — the merged sheet is design-v5's plus exactly the family's diff and
   the branch's plus exactly W2-A's. DS 2026: §2's components row carries both families' clauses; `doorway.html`'s
   «Usato in» names W3-B's NowPanel and W3-F2's error pages (the error pages draw the door with their own markup,
   painted by `v5/_door.css` through `cms/errori.css`). The decision log: design-v5's entries, then the family's.
   `dist/main.css`: rebuilt from a clean dist (`bb8af88`); the JS byte for byte design-v5's but for the shared chunks'
   names, which follow the worktree — the family changed no script.
3. **The ten paths outside the slice are this area's in the manifest** (`0e290e9`). `scripts/check_ownership.py w3-f2
   abbabda` listed exactly the paths the family declares (step 1's and step 2's seven and the fix pass's three); each
   was read in the diff and found to be what it declares. Whole files: the page partials `static/css/v5/_lettura.css`
   and `_servizio.css` and their entries `apps/cms/static/cms/{lettura,servizio,errori}.css` (plan §2.3; one glob,
   W3-D keeping its import-line slice), `apps/cms/templatetags/lettura.py` (`host`, D26, and `locked_title`). Slices of
   files no family held: `apps/core/views.py` (`error_400` / `error_500`, the self-sufficient page and its bare
   fallback), `apps/living/catalogue.py` (the seed's glyphs from `core.icons.LIVING`, W1-B's hand-over),
   `apps/accounts/profile_forms.py` (the profile's input purposes, WCAG 1.3.5, no logic) and `apps/news/forms.py` (the
   consent's `label_lang` in the refused newsletter's summary). DS 2026's slice is named as written (§10's entries and
   §10.1's rows, §2's components row, §2.1's three page-sheet rows). The check after it: 57 inside, 8 slice,
   3 generated, and the manifest itself, the one steward-only path (before: 10 outside); `--validate`: coherent,
   25 families, 546 entries.
4. **The shared CSS gate (the owner's V5.8) passes: the shared payload falls on every page type.** On the bundles
   rebuilt from a clean `static/css/dist` and `static/js/dist`, `gzip.compress(data, 9)`:

   | Page type | design-v5 `abbabda` | merged | change | ceiling before → after |
   |---|---|---|---|---|
   | console page types (`main` + `console` + `portal`) | 50 893 | 50 205 | −688 | 50 927 (DL54-87 item 3), kept |
   | «Mes pièces» (+ `documents.css`) | 52 065 | 51 377 | −688 | 52 099, kept |
   | the company's dashboard (+ `companies.css`) | 51 766 | 51 078 | −688 | 51 800, kept |
   | an interior page (`main.css`) | 42 152 | 41 464 | −688 | 42 540 → **41 464** |
   | the login (+ `entrance.css`) | 47 013 | 46 325 | −688 | 47 392 → **46 325** |
   | the home (+ `hero.css`, `pages.css`) | 56 803 | 56 115 | −688 | 57 191 → **56 115** |

   `dist/main.css` 42 152 → 41 464 B: the rows of `components.css` §20, §26, §27 (the account pages' frame, card and
   panels) and §28 leave the shared sheet for the area's page-only sheets and the pagination's dead rule is deleted
   (DL54-96, DL54-97, DL54-98); `console.css`, `portal.css` and every page sheet but the area's three are byte for byte
   unchanged. `main.css` also lands under the other reading DL54-95 item 3 named for the orchestrator (the sheet as it
   stood at `v54/w3-b`, 41 880 B): 416 B under it, so the 272 B that W2-A's merge stood over it on the public page types
   are gone and `main.css` is under its ceiling on either reading.
5. **Three ceilings lowered, as plan §2.6 item 3 says («the steward lowers a ceiling whenever a merge lands more than
   1 KB below it»).** An interior page lands 1 076 B under its ceiling, the login 1 067 B, the home 1 076 B: each
   ceiling is lowered to the total measured at this merge (the ratchet's reading: a ceiling is a measured total, item
   3's first sentence) — **41 464 B**, **46 325 B**, **56 115 B**. The console page types land 722 B under theirs and keep
   them (50 927 B; «Mes pièces» 52 099 B, the company's dashboard 51 800 B). `dist/main.css` stands 4 616 B under its
   45 KB ceiling (46 080 B). Under V5.8 the shared ceilings are hard: no merge raises them; a merge that would grow the
   shared payload is sent back.
6. **The area's three page types are recorded as measured — page-only sheets, where V5.8 puts a surface's own CSS.**
   The content and legal pages load `main.css` + `cms/lettura.css` (4 056 B): **45 520 B**; the account pages
   `main.css` + `cms/servizio.css` (2 426 B): **43 890 B**; the error pages `main.css` + `cms/errori.css` (3 629 B, which
   imports `v5/_door.css` and `v5/_servizio.css`): **45 093 B**. Before the merge these pages loaded `main.css` alone
   (42 152 B): +3 368, +1 738 and +2 941 B on their own pages, while every other page type is 688 B lighter; against the
   Wave-1 interior figure (44 486 B, DL54-44 item 3) +1 034, −596 and +607 B. Their ceilings are read as the home's
   is (DL54-44 item 3): the interior page's ceiling plus the page's own sheet as it weighs at this merge — 45 520,
   43 890 and 45 093 B — and they do not rise; a family that adds to one of the three sheets first deletes. The cost was
   measured by the area's one accessibility + performance check on the lane's compressed twin (`A11Y_PERF.md` P1, n = 10
   per cell and tree): LCP pooled +38.5 ms on the content cells and +44.7 ms on the service cells, both inside PFR's
   +50 ms resolution with intervals spanning 0; the first-render task no worse anywhere; CSS + JS requests before `load`
   7, the «before» set's 7; the LCP element text everywhere. Under the owner's V5.5 performance rule that is no
   regression to fix. That timing precedes the fix pass, which seated the door at rest on the error pages: its
   photograph (33–47 KB) is sized in its box from the first frame (no layout shift, the family's measure) but was not
   timed on the twin — an error page is the rarest page type, and this is said, not measured. **§2.6 item 5 is not applied to these three page types, and that is said here rather than passed
   over** (as DL54-44 item 3 said it for the home): before this merge they were interior pages under 42 540 B, and with
   their own sheets the content pages stand 2 980 B over that figure, the error pages 2 553 B and the account pages
   1 350 B — more than item 5's once-only raise of 2 KB for the first two. The owner's V5.8, the later word, writes the
   remedy item 5 names as the rule — a surface's own CSS in a page-only sheet loaded only where it is used, the shared
   payload the hard gate — and V5.5 ships what performs; the family deleted what it replaced first (`main.css` −688 B
   on every page). **The lever, if one is ever wanted:** REVIEW m11 — the interior grammar restated in
   `_lettura.css`, `_servizio.css` and W3-F1's `_interior.css` extracted once W3-F1 is on design-v5 (≈ 0.4 KB out of
   `lettura.css`, the check's estimate).
7. **The inventory and the capture report.** `scripts/regen_design_inventory.py` found two stale figures after the sync
   — DS 2026 §2's components.css 34.6 KB and 17 sections — and wrote 28.0 KB and 14 on the branch before the targeted
   tests (`bd96a2e`). The capture report is regenerated (`ef98cad`) — `docs/qa/design/capture.py`
   on lane 4 (DEBUG off, `--insecure`, one headless Chromium, exit 0): 43 captures, every one as expected; 12 differ,
   all of them the area's — the privacy page lays out one icon more (the legal pages' trail) and the 404 one fewer
   (the error page redrawn) — and the icons' total is unchanged, so §13 needs no rewrite.
8. **The tests.** On the branch after the sync, the bundles and the figures (`bd96a2e`), `TEST_DATABASE_URL=…/test_ile_v5_l4`,
   one pytest at a time: the area's targeted set without the browser — `tests/i18n`, `tests/compliance`,
   `tests/security`, the error pages in four languages with the 429 (the family's two unit files,
   `test_429_w2_b.py`, `apps/cms`), `apps/accounts` and the content apps (enquiries, faq, glossary, news, living,
   partners, community; consents and legal hold no test), `test_layout.py`, `test_design_docs.py`, the two
   bundle-current tests, `test_static_pipeline.py`, `test_o14_lint.py`, `test_state_chips_carry_a_register.py`, and
   what the merge touched besides (W2-A's `test_overlays.py`, `test_loader_rules.py`, `test_icons.py`, the comments'
   leak test, the ownership and inventory scripts' tests) — **1 390 passed** in 22 min, no skip; the browser set —
   `tests/i18n`'s four RTL files and the family's two — **60 passed** in 8 min, no skip, no crash. `ruff check`
   clean. The full suite is the integration checkpoint's (V5.5).

**Why.** Entries renumbered after design-v5's keep the log's one order; paths nobody holds would have no writer for the
next family; the gate is read on the shared payload as V5.8 writes it, and a ceiling the merge has left more than
1 KB behind is lowered so that the next family meets the weight the product has, not the one it had.

**Source.** The owner's V5.8 (`C:/tmp/ile_v5_council/directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`, and the
orchestrator's reading below it) and the V5_5 addendum of 11 October 19:40; plan §2.2 (the manifest; merge step 3),
§2.3, §2.6 items 3 and 5; DL54-44 item 3; DL54-73 item 3; DL54-76 items 4 and 5; DL54-87 item 3; DL54-95 item 3;
DL54-96 … DL54-98; `QA/v54/w3-f2/NOTES.md` «For the merge (the steward)» and «Merge step»; `QA/v54/w3-f2/A11Y_PERF.md`
P1; the weights in `evidence/v54/w3-f2/merge/budget_gate.log`; the ownership checks in
`evidence/v54/w3-f2/merge/ownership_before.log` and `ownership_after_wt.log`.
