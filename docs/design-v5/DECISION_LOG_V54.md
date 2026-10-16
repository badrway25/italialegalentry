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
| DL54-100 | 12 Oct 2026 | W2-C2: the sheet below 80rem is the overlay system's modal drawer with its own head (the lock-up and «Fermer»), «Quiet» on a phone, the side sheet from 48rem mirrored in Arabic; the signed-in targa opens the system's account popover, the key alone named by the layer tip; W2-A's hand-overs taken (`initDropdowns`, the `<details>` face, `v4/shell.css`, V4's segmented track); the portico panel keeps W2-C1's adapter until the system has a disclosure primitive; no hole when the flags are off | §1.11; §1.12 items 6–8; §1.14; §3.4 item 5; DL54-88; DL54-89; DL54-94 |
| DL54-101 | 12 Oct 2026 | W2-C2, the fix pass: the letterhead compact from 64rem (N11: ≥ 24 px to spare at 1024, French 42.8 px under a finger); every sheet ends on its night foot (amends DL54-100 item 1), the side sheet's 24 px margin; the foot not `on-inverse`, its menu's paper ring; the held scrim in `overlay.js` (a path outside the slice); one width for «Menu» and «Fermer»; the gloss, the seat's flex, the tap tint, the short viewport, the portico closed by any opening; the public pages' script recorded with the A/B (§2.6 exceeded until W4-B removes the Motion library); the gutter routed to W2-A | REVIEW M1, M2, m1–m7; A11Y_PERF M1–M3, m1; §1.6; §1.12; §2.2; §2.3; §2.6; DL54-93; DL54-100 |
| DL54-102 | 12 Oct 2026 | Steward, the w2-c2 merge: the family's two entries renumbered DL54-100 and DL54-101 (add 4); the 17 paths outside the slice and three more found by the merge's runs assigned to w2-c2 in the manifest, six slices named as written; the shared CSS gate of V5.8 passed with the shared payload lighter on every page type (`main.css` 41 464 → 41 029 B, −435 B; the console page types 50 205 → 49 770 B); every ceiling lowered to the merged weight (the orchestrator's definitive ruling, 12 Oct 02:15), the console page types' 50 927 → 49 770 B; the public pages' script recorded again; the capture report regenerated (29 captures of the sheet changed) and DS 2026 §13 with it; three pins of what the family removed fixed (`main.js`'s header line and `test_static_assets`, `test_components_w1_c`, `test_page_integrity`'s homograph «Close»); design-v5's own failures handed over | the owner's V5.8 (the definitive ruling); V5.5; §2.2; §2.3; §2.6; DL54-87; DL54-94; DL54-95; DL54-99; DL54-100; DL54-101 |
| DL54-103 | 11 Oct 2026 | W3-F1, step 1: the public interior as built — one grammar (`static/css/v5/_interior.css`, three page partials): the entrance «l'ingresso», the door card drawn «la porta» where no audience frame is left for a door's lead (§1.16), the home's chapters, the register, «la linea», D26's slots as layout; no side column; the index in the entrance, never sticky; one primary a page; the interior's cards fold their 8 into the chrome's 6 (three corners a screen); the universities' breakdown removed (RH-5); the pilot-flow illustration retired | V5.5; §3.5 item 1; §1.18 D26; §1.4; §1.3; §1.7; §1.16; CDV §19; `QA/v54/w3-f1/NOTES.md` |
| DL54-104 | 11 Oct 2026 | W3-F1, step 1: the page sheets of the interior as plain import lists in the collected tree (two new: `pages/css/interior.css`, `pathways/pathways.css`; `pages.css` the home's alone), the legacy rules no page draws deleted, the page types' CSS as measured for the steward (door-persons and pathway-detail 943 B over the Wave-1 ceiling, one CSS request more), the paths outside the slice | V5.5; §2.2; §2.3; §2.6; DL54-15; DL54-77 |
| DL54-105 | 11 Oct 2026 | W3-F1, step 2: orientation, the advice pages and the wizard as built — «Diplômes et titres» and «Formation» on the interior's grammar (their sequences on «la linea», the side column and the CTA band gone, the closing register and the one action on the stone); the questionnaire on the core components (the progress as a quiet register, plates around native controls, ONE primary first, the error wired and said in words, the focus on the new question after each step); the fraud warning an amber notice said three times, its page's text byte-identical under a visible title | V5.5; §3.5 item 1; §1.18 D26; §1.3; §1.4; §1.7; DL54-51; DL54-70; DL54-103 |
| DL54-106 | 11 Oct 2026 | W3-F1, step 2: `v4/wizard.css` leaves main.css for the console partial `v5/_wizard.css` («Ma situation» at the console's three corners, one raised panel, no glow, no glass, its foot inside the page); the legacy layout rules no page draws deleted; the CSS as measured (`dist/main.css` 42 316 → 41 212 B gzip on every page type; the console page types 49 894 → 49 986, under their 50 086 ceiling; the orientation pages 43 659 → 45 533, 1 047 B over the interior's Wave-1 ceiling, recorded); the paths outside the slice | V5.5; §2.2; §2.3; §2.6; DL54-15; DL54-73; DL54-77; DL54-104 |
| DL54-107 | 11 Oct 2026 | W3-F1, the fix pass: «la porta» carries the door's way in (on /parcours/ the questionnaire's action card, on /institutions/ and /universites-et-formation/ the prescribed button — each the page's one primary —, on /entreprises/ «Recueil des besoins» as a secondary); RH-3 met on /parcours/ («Comment ça marche» on «la linea», the locked sentence cut on its own arrows and read back whole), the needs form recorded outside the cadence, /forum/ and /le-projet/ on a phone waived until curated, captioned frames exist; the questionnaire says its place in words (no percentage) and holds «Commencer» in its entrance; the pilot's eight stations in a row from 90rem; SP-8's 24 / 44 px targets; French on an Arabic page says so; the door card's CSS loads only on the doors (`v5/_porta.css`); the page types' CSS for the merge step to record | V5.5; V5.8; `QA/v54/w3-f1/REVIEW.md`, `A11Y_PERF.md`; §1.4 RH-3, SP-8; §1.16; §1.18 D26; DL54-103 … DL54-106 |
| DL54-108 | 12 Oct 2026 | W3-F1, the budget and consolidation pass: design-v5 at `v54/w3-f2` merged (this area's entries DL54-78 … DL54-82 → DL54-103 … DL54-107); one partial for the public interior's shared components, `static/css/v5/_pagina.css`, the first import of W3-F1's five page sheets and W3-F2's `cms/lettura.css` (the trail, the head, the chapters' device, the register's rows, D26's shared slots — drawn once; W3-F2's pages unchanged); the shared sheet sheds what the interior replaces (§9's and §10's re-drawn declarations, the orphan hero and local navigation, the verso and home plates, the zones' rail and margin, the sidebar layout; §18 to the home's sheet); a page sheet holds what its pages draw; `main.css` 41 464 → 39 111 B on every page; the persons page type recorded at its first page sheet (42 605 B), orientation 42 796 → 43 150 B, every other page type lighter; no LCP / first-render regression on the lane | V5.8 (the definitive ruling, 12 Oct 02:15); V5.5; W3-F2's review m11; DL54-99; `QA/v54/w3-f1/NOTES.md` «Budget and consolidation» |
| DL54-109 | 12 Oct 2026 | Steward, the w3-f1 merge: the family's six entries renumbered DL54-103 … DL54-108 (after W2-C2's DL54-100 … DL54-102); the 31 paths outside the slice assigned (21 whole files, 10 slices) and four slices named as written; the shared CSS gate passed — `dist/main.css` 41 029 → 38 683 B on every page, the console page types 49 770 → 48 556 B —; every ceiling lowered to the merged weight; the public interior's five page types recorded as measured (the persons pages' first page sheet, orientation, the ecosystem doors, the Forum, the institutional pages); one semantic conflict with W2-C2's phone sheet fixed in two of the family's tests; the capture report unchanged | V5.8 (definitive ruling, 12 Oct 02:15); V5.5; plan §2.2, §2.3, §2.6; DL54-102; DL54-103 … DL54-108 |
| DL54-110 | 11 Oct 2026 | W3-C: «Mes pièces» V5.2 — the register strip (the page's one raised plane, its one primary with its piece and its date), one partition in three groups by whose move it is, the row as the link (six zones, no row menu, no «Consulter»), the filter in STATE_ORDER and its sheet, the files tables, the piece in the order of need | §3.5 item 5; §1.2; §1.15; DL54-78 … DL54-80 |
| DL54-111 | 11 Oct 2026 | W3-C: F8 — the urgency ladder stops once a piece is filed; F13 — «En retard» `overdue` (azione), «Bientôt» `soon` (attesa) on the deadlines page | §1.2 «Deadlines»; the platform map F8, F13 |
| DL54-112 | 11 Oct 2026 | W3-C: the three page partials (`_workspace`, `_table`, `_depot`) imported by the documents page sheet, never by `main.css` nor the console entry; the piece's page in the order of need, V4's case band not drawn there | §2.3; DS 2026 §2 |
| DL54-113 | 11 Oct 2026 | W3-C: five paths outside the slice, each justified; the legacy register rules deleted from `main.css` (−1 332 B on every page); the documents page type's CSS as measured | §2.1; §2.2; §2.3; §2.6; DL54-15; DL54-73; DL54-85 |
| DL54-114 | 11 Oct 2026 | W3-C, step 2: the Dépôt — one markup for the two roads; the eleven answers of the server composed in place on a JSON road (`X-ILE-Depot`, always a 200) that changes no rule; client guards read from the server's limits; no new word | §3.5 item 5; IP S7; DOCUMENT_WORKSPACE §11 |
| DL54-115 | 11 Oct 2026 | W3-C, step 2: F13 on every page that draws a deadline register (the case file's checklist, dates and next step; the console's next action; the portal tables' late rows; the deadlines page's glyphs in the dashboard's grammar); `register.css`'s current-entry rules deleted, the rest still drawn by eight families; the shared payload flat (V5.8) | §1.2; §2.3; V5.8 |
| DL54-116 | 12 Oct 2026 | W3-C, step 2: the preview drawer and the filter's sheet on the overlay system — the drawer non-modal beside the list on desktop and a modal sheet on a phone, its head at 0 ms from the row, its body the piece's own article seated by L3, `?état=` kept and `replaceState` on swaps; the filter's one control a link to the system's bottom sheet, its entries one partial; the register pages link the page-only overlay sheet; W2-A's row-menu pins retargeted | §1.14; §1.15 item 3; §3.5 item 5; W2-A CONTRACT §1–§6 |
| DL54-117 | 12 Oct 2026 | W3-C, step 2: no state read through `:has()` — a row's and the Dépôt's keyboard focus from the input's modality (a focus in a row had re-styled the whole page, ≈ 650 elements a time on a phone), the register's re-layout after the drawer's first frame: the drawer's open and close p90 ≤ 184 ms at CPU × 4 (O7); `depot.js` brought back under the loader and motion rules | §1.14 O7; §1.5; DL54-89 |
| DL54-118 | 12 Oct 2026 | W3-C, step 2: the paths outside the slice; the shared payload 50 893 → 49 620 B (the console page types, 1 307 B under the ceiling), the documents pages' own sheet 1 172 → 5 418 B and W2-A's page-only overlay sheet (2 071 B) on the register pages | §2.2; §2.3; §2.6; V5.8; DL54-87 |
| DL54-119 | 12 Oct 2026 | W3-C, the fix pass: after a swap the drawer's close keeps the person's place (`history.scrollRestoration` manual while the drawer owns its entry; the focus on the shown piece's row — the native dialog had handed it to the first row opened); the open piece marked (`aria-current`, the selected state) and the press kept under the pointer across the re-layout; the strip's act steps down while the drawer shows its piece; one clock decides one deadline (`is_overdue` on `core.clock`); the caption, the files' list on a phone, the deletion's alert dialog, the loose answer, the size shown, the ledger marks consolidated, the runs' inset ring, «Télécharger»'s band, a refused file marks its field; shared CSS unchanged (49 620 B), documents.css 5 418 → 5 497 B | REVIEW M1–M3, m1–m7; A11Y_PERF 1–4; §1.14; §2.6; V5.8; DL54-116 |
| DL54-120 | 12 Oct 2026 | Steward, the w3-c merge: the family's ten entries renumbered DL54-110 … DL54-119 (after W3-F1's DL54-103 … DL54-109); the 18 paths outside the slice assigned (6 whole files in two globs, 12 slices) and four slices named as written; the shared CSS gate passed — `dist/main.css` 38 683 → 37 324 B on every page, the console page types 48 556 → 47 200 B —; every ceiling lowered to the merged weight; the documents pages' two page types recorded through their own sheet (the piece, upload and gate pages 52 697 B; the two register pages 54 768 B, with W2-A's overlay-panels sheet); DS 2026 §2's two stale figures regenerated; the capture report unchanged; design-v5's own motion-gate failure unchanged | V5.8 (definitive ruling, 12 Oct 02:15); V5.5; plan §2.2, §2.3, §2.6; DL54-102; DL54-109; DL54-110 … DL54-119 |
| DL54-121 | 12 Oct 2026 | Steward, the devops merge: production readiness (V5.9) on design-v5 — the runbook, the checklist, the rollback, `.env.example` and the production settings, nothing deployed; the family «devops» registered in the manifest outside the waves (30 paths, 18 whole, 12 slices; the checker accepts its id); the pre-merge sync closed F-6 through W3-F2's self-sufficient 400 page and documented the V5 families' new test variables; no tag, no push; the owner's thirteen open questions | V5.9 §3–§17; V5.8; DL54-01; DL54-77; plan §2.2; `QA/v54/devops/NOTES.md` |
| DL54-122 | 11 Oct 2026 | W3-D: a threshold is a place — a file in SELECTION stands on threshold A and on no step; `journey_for` gives each step its status, its state and the threshold it opens; the case file dates the threshold; SUSPENDED and CLOSED keep V4's first step until the trail is read | §3.5 item 6; §1.18 D16 (OJ2); JS §5.7, §7.3 |
| DL54-123 | 11 Oct 2026 | W3-D: one rail drawing for the console — the dashboard's journey, the case file's journey and timeline, «Ma situation»'s Stepper on one vocabulary; the level line from 56rem of the component (the research's 46rem measured too narrow); the card and its native disclosure under it; one marker a column (the glyph); A′, no beads; still at load; no `journey-rail.js` | §3.5 item 6; §1.18 D16; §1.5; JS §5.3, §5.5, §7.1, §7.2 |
| DL54-124 | 11 Oct 2026 | W3-D: one passage drawing for the public pages — «la linea» (W3-F1's grammar) homed in `_journey-passage.css` with `components/stepper.html`; the home's orientation steps drawn by it; the door pages after W3-F1's merge, the consolidation written down | §3.5 items 1 and 6; §1.18 D16; §2.3 |
| DL54-125 | 11 Oct 2026 | W3-D: a date on the rail in tabular figures in the sans (ILE Mono keeps its one seat); «Ma situation» moves nothing at load | §1.1; §1.5; `QA/v54/w1-d/NOTES.md` (situation.js) |
| DL54-126 | 11 Oct 2026 | W3-D: the paths outside the slice, each justified; the legacy rules deleted; the CSS as measured — the home page type lighter, the console page types over their ceiling, reported | §2.2; §2.3; §2.6; DL54-15; DL54-87 |
| DL54-127 | 12 Oct 2026 | W3-D, the fix pass: the rail leaves the shared console bundle for a page-only sheet (`portal/journey.css`, linked by the four pages that draw a journey — the console page types 51 530 → 49 614 B, 1 313 B under design-v5's 50 927); «Mon parcours» draws the journey at its head; a SUSPENDED or CLOSED file has no current item and «Vous êtes ici» nowhere — the case file dates what its trail reached; the timeline newest first; the consolidation with W3-F1 waits for its merge | REVIEW M1–M4, m1–m6; A11Y_PERF findings 1–3; V5.8; DL54-87; DL54-122 |
| DL54-128 | 12 Oct 2026 | W3-D, the integration pass: design-v5 merged at `v54/w3-f1`, then again after W3-C's merge and after the devops merge; one passage drawing — W3-F1's «la linea» homed in `_journey-passage.css` with `components/stepper.html` (the door pages and the home pixel-identical but for the rings' rim antialias); `components.css` §17, `timeline.html` and `_wizard.css`'s Stepper retired (grep-proved); «Ma situation»'s guided form out of the shared console bundle into its one page-only sheet; the rail drawing a vocabulary and two components so that each journey page loads only what it draws — the console page types 47 200 → 44 196 B against design-v5 after W3-C and the devops merge (`3d5351b`), every page type lighter; the design showcase links the journey's page sheets and, for the passage, the home's | REVIEW M4; NOTES «For W3-F1», «Integration pass»; the definitive CSS ruling (V5.8); DL54-87; DL54-109 |
| DL54-129 | 15 Oct 2026 | Steward, the w3-d merge: the family's seven entries kept as numbered (DL54-122 … DL54-128 — the branch held design-v5's head); the 19 paths outside the slice assigned (one whole file, 18 slices), the four new sheets whole files, seven slices named as written; the shared CSS gate passed — `dist/main.css` 37 324 → 35 483 B on every page, the console page types 47 200 → 44 196 B —; every ceiling lowered to the merged weight; the journey's two page types recorded through their own sheet (a journey page 46 617 B, «Ma situation» 46 398 B); no surface key (the journey is drawn inside other families' page types); the capture report unchanged; design-v5's own motion-gate failure unchanged | V5.8 (definitive ruling, 12 Oct 02:15); V5.5; plan §2.2, §2.3, §2.6; DL54-120; DL54-122 … DL54-128 |
| DL54-130 | 15 Oct 2026 | Steward, the sec-f5 merge: F-5 closed on design-v5 — `/backoffice/login/` signs no one in (staff sign in through allauth and its MFA stage) and an account that holds a second factor presents it in every session before the back office, the reserved area, `/documents/` or allauth's pages that manage the factor, whatever `BACKOFFICE_MFA_ENFORCED` says; the independent review (SHIP_AFTER_FIXES, nothing blocking) and its four minor findings fixed before the merge; the family «sec-f5» registered in the manifest outside the waves (21 entries, 4 whole, 17 slices; the checker accepts `sec-f<n>`); no tag, no push, nothing deployed | V5.9 §6, §14–§17; DL54-121 item 7.1; checklist A-13; plan §2.2; `QA/v54/sec-f5/NOTES.md`, `REVIEW.md` |
| DL54-131 | 16 Oct 2026 | Steward, integration checkpoint 3: the full suite on design-v5 after Wave 3's merges (W3-F1, W3-C, the DevOps readiness merge, W3-D; sec-f5 at the sync) — non-browser 5 058, then 5 108 passed (W3-D's three reds fixed, 954 passed around them), Chromium 507, then 519 passed, 0 errors —; the reds fixed at their root: the overlay's late settle (a console drawer reopened within one frame lost its trap and the scrim no longer closed it), the loader's guard left on for ever without loader.js, the overlay's own frame request outside motion.js's gate, SO_LINGER on Linux, a teardown deadlock in W3-C's drawer test, W3-D's showcase comment; DL54-112's «one importer» and `3093261`'s `@import` ban on the home's sheet superseded by what they protected; the review SHIP; the family «intfix» registered in the manifest outside the waves (12 entries, 1 whole, 11 slices; the checker accepts `intfix`); no stylesheet changed (the shared payload as DL54-129 left it); the tag `v54/checkpoint-3`; no push, nothing deployed | V5.5; V5.8 (definitive ruling); V5.9; DL54-77; DL54-102 item 10; DL54-112; DL54-128 item 4; plan §2.2; `QA/v54/intfix/NOTES.md`, `REVIEW.md` |
| DL54-132 | 16 Oct 2026 | Steward, the sec-f7 merge: F-7 closed on design-v5 — the lifecycle's «Chi può» column (`CASE_LIFECYCLE.md` §4, rule 2) declared as data beside the graph (`cases.models.TRANSITION_ACTORS`), enforced by `transition` whenever an actor is given and offered by `transitions_available` from the same rule, the object policy AND the column (the fix narrows; nobody's access widened); the administrator only where §4 names it, `BEYOND_SECTION_4`'s two departures pending the owner; the back office hands out no capacity; every move judged on the file's locked row, «chi ha sospeso» read from this suspension's own event, the platform's moves recorded as nobody's, CR-03 counting authorised actors' assignments only; Part B — a person whose latest file is suspended or closed is told so (`held_case`, the NowPanel's two held variants; DS 2026 §11.7: six variants); the review SHIP_AFTER_FIXES, its findings fixed before the merge; the family «sec-f7» registered in the manifest outside the waves (14 entries, 4 whole, 10 slices); 1 106 + 35 tests passed on the merged branch; no stylesheet changed (the shared payload as DL54-129 left it); the owner's questions Q1–Q12; no tag, no push, nothing deployed | V5.5; V5.9; `CASE_LIFECYCLE.md` §4; CR-03; DL54-121; DL54-130; plan §2.2; `QA/v54/sec-f7/NOTES.md`, `REVIEW.md` |
| DL54-133 | 15 Oct 2026 | W3-E: the person's registers on one grammar — the workspace head without an eyebrow, the band (the bridge's live words, each event counted once), the dashboard's row (`.db-task`) with the state as a chip, the whole row as the way to its record; the distance in words not drawn (B1 item 4) | §3.5 item 7; §1.2; the platform map §3; D17 |
| DL54-134 | 15 Oct 2026 | W3-E: three producers in the chip registry (`enquiries.SubmissionStatus`, `forum.RegistrationStatus`, `portal.DeadlineStatus`); an archived request and a cancelled date carry nothing (nullo); `badge.html` no longer included by the person's registers | §1.2; DL54-52; DL54-53 |
| DL54-135 | 15 Oct 2026 | W3-E: the empty state is design V5's component (`components.css` §23; DS V5 §10.8) — the 40 px toned disc, the 20/28 title, one sentence, one action, on a hairline, an outline under forced colours; V4's box out of `v4/workspace.css`; the console's spanning rule kept | §2.3 (W3-E's rows); DS V5 §10.8; DL54-33; DL54-34 |
| DL54-136 | 15 Oct 2026 | W3-E: «la lettera» — a communication drawn as the letter it is, the team's mark (`ile-mark`) as its seal, on the letter and on every row of «Communications»; the identity carriers of the screens with neither rail nor register named and swap-tested | §3.1 item 7; IC (`ile-mark`) |
| DL54-137 | 15 Oct 2026 | W3-E: the 503 page of the reserved area is a page of service in the error pages' grammar — the door at rest, the key out of the lock; no new copy | §3.5 items 2 and 7; DL54-97 |
| DL54-138 | 15 Oct 2026 | W3-E, step 1: six paths outside the slice, each justified; the registers' page-only sheet (1 624 B, first sheet as measured); the shared payload lower — `main.css` −92 B on every page, the console page types 47 200 → 46 854 B | §2.2; §2.3; §2.6; V5.8 «definitive ruling» |
| DL54-139 | 15 Oct 2026 | W3-E: «Ma situation»'s one act is the phone's action bar — «Continuer» (the submit on the last question) where the bottom bar's entries stood, «Menu» kept; «Précédent» and the position in the page's foot; the save on the way waits for the last question | §3.5 item 7; DL54-70; O63 |
| DL54-140 | 15 Oct 2026 | W3-E, step 2: the registers' grammar draws the organisations' and the other spaces' pages — the guichet, the Academy, the selection, the company's pages beyond its dashboard, the Forum permanent; six devices in the same partial (the clause, the steps and the log, the exchange, the answerable party, the form of an act, the filter) and one page-only sheet for all; the console's table on V5 | §3.5 item 7; §3.1 item 7; DL54-133; V5.8 |
| DL54-141 | 15 Oct 2026 | W3-E, step 2: the company — the needs register's counts are its filter (E-3: «Tous» and the dashboard's own groups, each its count and its marks, `?état=`); the V1 company band leaves every page (one identity per screen in the space's one rail, S-5); no chart (E-4); the declaration's two h1 become one | platform.md §3; §3.5 item 7; DL54-79 |
| DL54-142 | 15 Oct 2026 | W3-E, step 2: the bridge's states through their producers — `badge.html` retired on console pages; «Non lue» a word with its dot; a membership's role a fact; «Mon organisation» draws the account's audience glyph (an institution ≠ a university ≠ a company) | §1.2; platform.md §3; DL54-80; DL54-134 |
| DL54-143 | 15 Oct 2026 | W3-E, step 2: a section head carries a glyph only where the registry names its concept and the symbol holds at 16 px (`concierge-bell`, `wrench`, `settings`, `calendar-range` need 20, `handshake` 24); the Forum permanent's closed page in the error pages' grammar, «pas encore ouvert» | §1.7; IC floors; DL54-137 |
| DL54-144 | 15 Oct 2026 | W3-E, step 2: five paths outside the slice, each justified; the shared payload lower (the console page types 46 854 → 46 689 B, `main.css` flat); the registers' sheet 1 624 → 2 593 B on ≈ 40 pages, the module sheets 189–463 B; the staff and back-office pages' working screens recorded as design debt | §2.2; §2.3; §2.6; V5.8 «definitive ruling» |
| DL54-145 | 16 Oct 2026 | W3-E, step 3: the case file in design V5 — the five questions in order on what the platform families shipped (the head without an eyebrow, C-4; the journey; the NowPanel and its one primary, a line acted on in its row, a mandated reader told the next step in nobody's voice, the phone's action bar; «Ce qui est demandé» as the register's rows, C-3, then the file's pieces; who intervenes as answerable parties; what changed beside it) | §3.5 item 7; the platform map §3 «Case file»; DL54-81 … DL54-86; DL54-122 … DL54-128; DL54-140 |
| DL54-146 | 16 Oct 2026 | W3-E, step 3: the state changes through the row menu and the overlay system's alert dialog (C-5) — the consequence named, «Annuler» the safe default, the focus back on the row's «⋮»; the POST returns to the row; the file's state in the same dialog family, the closure's consequence and the suspension's rule said before the act (C-6); no bulk edit | §1.14; §3.5 item 7; the platform map C-5, C-6; W2-A CONTRACT §1–§6 |
| DL54-147 | 16 Oct 2026 | W3-E, step 3: v4/workspace.css leaves the cascade (the deletion map's last row, «the file») — what other console pages still drew of it moves unchanged to the console partial v5/_frame.css, imported last; the case band and the shell's next action leave; the V1 devices these pages were the last to draw leave main.css; three tokens become reserves | §2.3; §2.1 «Delete what you supersede»; V5.8 «definitive ruling» |
| DL54-148 | 16 Oct 2026 | W3-E, step 3: «Mes dossiers» and the case's pre-assessment in the registers' grammar; the pre-assessment's replay on the page's own ground (the night verso at 1.06 : 1 gone); «Ma situation» counts one total (W3-D's m4) | §3.5 item 7; DL54-140; W3-F1 NOTES l.304; W3-D NOTES «Handed to» |
| DL54-149 | 16 Oct 2026 | W3-E, step 3: the paths outside the slice; the CSS as measured — `main.css` 35 290 → 31 906 B on every page, the console page types 43 572 → 40 140 B; the case file 45 993 → 45 968 B, 48 039 B where it draws its dialogs (W2-A's page-only panels), recorded at its first own sheet; the load check | §2.2; §2.6; V5.8 «definitive ruling»; DL54-87 |
| DL54-150 | 16 Oct 2026 | W3-E, the fix pass: the case file's first screen holds the next act (the journey in W3-D's compact forms, the dated history the feed's); the NowPanel's line drawn once, its act its alert dialog; the history's «Vous» for the person only; the family's irreversible closures (the guichet ×2, the selection) on the alert dialog, one dialog body; the registers' minors and the a11y check's six; the held file's reason drawn once at the sec-f7 merge; the shared bundles unchanged | REVIEW M1–M4, minors 1–11; A11Y_PERF 1–6; §1.14; §3.5 item 7; LA-9; DL54-64; DL54-145; DL54-146 |
| DL54-151 | 16 Oct 2026 | Steward, the w3-e merge: the family's eighteen entries renumbered (DL54-133 … DL54-150, after design-v5's DL54-130 … DL54-132); the 33 paths outside the slice assigned (four whole-file entries, 27 slices) and the merge's one retargeted test (sec-f7's page test reads the case file's state dialog); two slices named as written; the shared CSS gate passed — `dist/main.css` 35 483 → 31 906 B on every page, the console page types 44 196 → 40 140 B —; every ceiling lowered to the merged weight; the area's page types recorded through their own sheets (a register page 43 015 B; the case file 46 391 B, 48 462 B where it draws its dialogs); nineteen surface keys v5; the capture report unchanged | V5.8 (definitive ruling, 12 Oct 02:15); V5.5; plan §2.2, §2.3, §2.6; DL54-129; DL54-132; DL54-133 … DL54-150 |
| DL54-152 | 16 Oct 2026 | Steward, the devops-2 merge: release hardening on design-v5 — every file a page loads a hashed, immutable name (`core.storage` rewrites the imports of `static/js/dist`; a plain name revalidated after a minute); a NUL byte in the path, the query string, a form field or the session cookie the project's 400, never a 500, with the security headers of every page; the browser tests' live server and the design preview's own server on a port Chromium accepts; the family's second pass in the manifest; nothing deployed (this index row written at the w4-b merge, DL54-154 item 1) | V5.9 §3; `QA/v54/devops/NOTES.md` (second pass), `REVIEW_2.md` |
| DL54-153 | 16 Oct 2026 | W4-B, the motion audit (read first, `QA/v54/w4-b/AUDIT.md`): the Motion library leaves — «Ma situation»'s question change on the Web Animations API through motion.js's gate (same clocks, distance and order; the curve the token's), shell.js's reveal and components.css §29 / `initReveal` / `initCounters` gone (K17), `motion` and its parts out of the package files, the bundle test rewritten; the modules one entry alone imports inlined into it (one script request fewer); the rail's fold instant (R10, measured); the keyboard's tier 0 in the portico and on the skip link; the forced-colours current entry its own marker (W3-D's O2); the review's m2–m4 answered; after W4-B's own review and accessibility check, «Ma situation»'s change at once from the keyboard and whole after an interruption, the links' tier 0, `--ease-exit` back to its one role; the paths outside the slice, for the merge | §1.5 (tiers, R10, K17, «Engine», MS-O1/O2); §2.2; §2.3; §2.6; §3.6 item 2; DL54-101 item 4; `QA/v54/intfix/REVIEW.md` m2–m4; `QA/v54/w3-d/NOTES.md` «Handed to»; `QA/v54/w4-b/REVIEW.md`, `A11Y_PERF.md` |
| DL54-154 | 16 Oct 2026 | Steward, the w4-b merge: W4-B's entry renumbered DL54-153 (after design-v5's DL54-132 … DL54-152); the two no-owner paths assigned as W4-B's slices (`scripts/build_frontend.mjs`'s `INLINED` list, `FRONTEND_DEPENDENCIES.md`'s `motion` row) and the dependency's removal in `package.json` and `package-lock.json` adopted as the steward's own write (plan §3.6 item 2), the two files the steward's whole; the shared CSS gate passed — `dist/main.css` 31 906 → 31 799 B on every page, the console page types 40 140 → 39 978 B —, every ceiling lowered to the merged weight; the home's script 51 249 → 24 138 B gzip, §2.6's 45 KB held on every page type; the family row in the status file, no surface key changed; DL54-152's missing index row added | V5.8 (definitive ruling, 12 Oct 02:15); V5.5; plan §2.2, §2.6, §3.6 item 2; DL54-101; DL54-151; DL54-152; DL54-153 |
| DL54-155 | 16 Oct 2026 | Steward, the w4-d merge (part 1): release engineering on design-v5 — CI's two runs on `ubuntu-24.04` (Python 3.12 · PostgreSQL 16, the production target: the server's major versions with its pinned closure; Python 3.13 · PostgreSQL 17, development), a step asserting both versions; the release of V5.10 named once in the runbook, the checklist and ROLLBACK.md (the annotated tag `v2.0.0` after the fast-forward; `pre-v5-main-2026-10` on `a3ac318` a reference point, never a server rollback; a downgrade a restore; the migration re-check that lists the files); one bar for PRODUCTION_READY; the go-live calendar verified, nothing to fix in code; the release notes drafted and assigned to w4-d; REVIEW_PART1's m4 kept out of the published tree; no tag, nothing deployed | V5.10; V5.9 §14–§17; plan §3.6 item 4; `QA/v54/w4-d/NOTES.md`, `REVIEW_PART1.md` |

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

## DL54-100 · 12 October 2026 · W2-C2: the sheet is the system's drawer with its own head; the targa's popover; the portico panel keeps its adapter until the system has a disclosure primitive

**Decisions** (V5.5; plan §3.4 item 5, §1.12 item 8, §1.11, §1.14; `QA/v54/w2-c2/NOTES.md`). Written as
DL54-96; renumbered DL54-100 at the merge (W3-F2's DL54-96 … DL54-99 reached design-v5 first).

1. **The phone and tablet sheet is the overlay system's modal drawer** (`data-overlay="drawer"`, the navigation drawer
   row of plan §1.14's table), not the bottom-sheet family: it opens from the screen's edge, not from the bottom, and it
   owns its head line (the lock-up and «Fermer», which takes the first focus) in `chrome.css` §7 — so it draws nothing of
   the page-only part (CONTRACT §1: the panels with a head of `dialog.html` / `sheet.html` / `drawer.html`), and every
   public page keeps one stylesheet. Below 48rem it takes the screen «Quiet» (opacity, the body and the foot rise 12 px,
   the drawer's clocks 320 / 200 ms, the head on the bar's row); from 48rem it slides in from the inline end.
2. **O5 read on the contract** (§5: «drawers mirror, sheets do not»): the side sheet is a drawer, so in Arabic it comes
   and goes by the left; the phone's rise is vertical and travels sideways in no language
   (`tests/i18n/test_rtl_browser_w2_c2.py`).
3. **The signed-in targa opens the system's account popover** (`components/account_menu.html` with `popover`), in the
   seat and in the sheet's foot; the key alone is named by the shared top-layer tip (`data-tip="layer"`), refused
   through `overlay:tip` from 100rem where the plate says its word — the control's own CSS tip is page-only since
   DL54-94.
4. **W2-A's hand-overs taken** once `shell.js` imports `overlay.js`: `main.js`'s `initDropdowns` fallback, the account
   menu's `<details>` face and `v4/shell.css` (the file and its import) leave, with V4's segmented language track (no
   caller left) — as W2-A's own comments asked.
5. **The portico panel stays on W2-C1's adapter.** Plan §1.12 item 6 and RTD-m8 want the panel's scrim, dismissal and
   focus from `overlay.js`; the contract's API opens kinds (dialog, alert, drawer, sheet, popover) and has no primitive
   for a disclosure region. Bending the popover family to carry the panel breaks it: without anchor positioning the
   module writes `left` / `top` on every popover (the panel hangs from the content width), its arrows wrap inside the
   panel (the portico's ↑ returns to the door, ← → change door), the top layer and the UA popover rules take the
   panel's geometry and its no-script hover, two auto popovers stack in the order they were shown (the leaving
   panel's photograph must fade out above the arriving one), and the portico's scrim (below the letterhead, never
   over the utility bar) is not the system's. The request is written to W2-A (`QA/v54/w2-c2/NOTES.md`, «For W2-A»); the switch is
   W2-C2's follow-up once it exists.
6. **No hole when the flags are off**: a signed-out end zone with nothing to seat is marked bare and, from 80rem, not
   drawn — it took the row's gap and left the bar 16 px short of the column's edge (N13).

**Source.** Plan §1.11, §1.12 items 6–8, §1.14, §3.4 item 5; surfaces.md §1.3 items 7–8, §1.4 N8 N9 N13 N14 N19, §4.4
O2–O8; `QA/v54/w2-a/CONTRACT.md` §1–§6; DL54-88, DL54-89, DL54-94; `QA/v54/w2-c2/NOTES.md`;
`tests/frontend/test_nav_sheet_w2_c2.py`, `test_browser_w2_c2.py`, `tests/i18n/test_rtl_browser_w2_c2.py`.

## DL54-101 · 12 October 2026 · W2-C2, the fix pass: the letterhead compact from 64rem; every sheet ends on its night foot; the foot's menu keeps the paper's ring; the held scrim; the public pages' script recorded

**Decisions** (the fix pass of the family's one review, `QA/v54/w2-c2/REVIEW.md`, and of its accessibility and
performance check, `QA/v54/w2-c2/A11Y_PERF.md`; what was done and measured is the notes' «Review fixes»). Written
as DL54-97; renumbered DL54-101 at the merge, its citations of the first step's entry (written DL54-96) read
DL54-100.

1. **The letterhead is compact from 64rem, not from 80rem** (REVIEW M1; N11 «one row, ≥ 24 px spare at 1024 px in
   the longest language») — supersedes the full lock-up W2-C1 kept in the 64–80rem band. At 1024 the column is
   944 px (927 beside a 17 px classic scrollbar) and the French row with the 38/20 lock-up needed 945 px under a
   finger, where the plate and «Menu» are 44 px — on an iPad in landscape the letterhead drew two rows (129 px) — and
   933 px on a fine pointer. The lock-up at the scrolled state's 32/17 gives back 44 px: French keeps 42.8 px under a
   finger and 37.8 beside a 17 px scrollbar, English 52.2 / 47.2, signed out and in. One block now serves the bands
   64–90rem (the lock-up, the 16 px gaps, the doors' 10 px padding, no chevron); the 64–80rem block keeps only the
   doors. Trimming the doors' padding was the other way: it would have changed the bar's rhythm the 80–90rem band
   already shares with this one.
2. **Every sheet ends on its night foot — amends DL54-100 item 1** (REVIEW M2; plan §1.12 item 8: «the phone and
   tablet sheet … the targa and the promoter sit in the pinned foot»). DL54-100 hid the foot from 48rem because «the
   letterhead keeps its lock-up, la targa and the promoter»; the letterhead's targa stands at the inline end, where
   the side sheet arrives, so the open menu offered no reserved-area entrance and ended on blank paper. From 48 to
   80rem only the head's duplicate lock-up is hidden. The side sheet has its own margin, 24 px (`--grid-margin`
   re-pointed in the sheet: a 371 px column at 768, the primary on one line — REVIEW m3).
3. **The foot is not a night context; its controls carry the night's ring** (A11Y_PERF M2; plan §1.6). The account
   menu that opens from the foot is a paper panel in the top layer that inherits from its trigger's ancestors: under
   `.on-inverse` its focused rows drew the night's ring on white at 1.75 : 1 and its glyphs the night's ink. The foot
   drops `on-inverse`; `.nav-sheet__foot :is(.targa, .account-menu__summary)` takes `--focus-ring-night` and
   `--focus-halo-night` (tokens only — chrome.css holds no literal colour, `test_v5_tokens`); the menu draws the
   paper's #1d8a93 (4.11 : 1) and #4a5a62 glyphs.
4. **The public pages' script is recorded, not deferred** (A11Y_PERF M3, «fix or record»). Plan §2.3 puts
   `overlay.js` in `shell.js`, so the overlay core is on every public page: the home 45 581 → 51 156 B gzip (the
   check's 51 136 + this pass's 20), past §2.6's «a public page ≤ 45 KB» (46 080 B) by 5 076 B; a door page 38 006 →
   43 579, the login 39 683 → 45 255; one more script request before `load` (the home 3 + 9 against the before set's
   3 + 8, a door page 1 + 7 against 1 + 6: §2.6's request ratchet over by one); the console pages 913 B lighter.
   Measured cost on the compressed twin, 216 traces, profile A, CPU × 4 (A11Y_PERF §3): pooled LCP 1 524 → 1 472 ms,
   every cell within +50 ms (the Arabic home at 1440 +18 ms, n = 18), the LCP element unchanged, the first-render task
   62.8 → 46.2 ms, the longest load task 136.6 → 124.6 ms, TBT 180.6 → 134.4 ms (pooled medians), CLS ≤ 0.025. A
   dynamic import at idle (and at once on the first press of «Menu» or the account trigger) was weighed and refused:
   the first press would race the chunk's fetch — a click shim and its replay, «Menu» a link until the module upgrades
   it, the keyboard's first tip missed, the scrim made in the tap — on the phone's one navigation, for no measured
   gain (V5.5: fix only real regressions). The largest share of the home's script is the Motion library's chunk
   (26 611 B), which leaves with W4-B (plan §2.3); without it the home is ≈ 24.5 KB with the overlay core in. For the
   orchestrator and the Performance Lead: the §2.6 line and the request ratchet stand exceeded by the plan's own §2.3
   placement until then.
5. **A press held on the scrim keeps its place** (A11Y_PERF M1), written in W2-A's `overlay.js` — a justified path
   outside the slice (plan §2.2). The platform light-dismisses a menu sheet as a touch goes down; the touch's
   compatibility mouse events and its click are hit-tested after `touchend`, and `syncScrim()` had already re-stacked
   the scrim under the trapped phone sheet (z 51 → 49): the tap unfolded the door, followed Forum or switched the
   language under the finger. `syncScrim()` leaves the z-index alone while `data-held` stands and `release()` re-syncs
   it — so W2-A's DL54-93 item 1 («the page is never reached») now holds over a trapped panel too.
6. **«Menu» and «Fermer» have one width below 48rem** (REVIEW m5): each holds both words in one centred grid cell,
   the other hidden by its class (`.nav-toggle__alt`, `aria-hidden`; no rule selects `[aria-hidden]`, which the trap
   writes — W2-A's guard); 6 px inside instead of 8 keeps the phone row's arithmetic (French 88.6 px, 0.9 px to spare
   at 369, where «Fermer» used to run 5 px past the column). From 48rem the side sheet arrives with its own «Fermer»
   and each button is as wide as its word.
7. **The rest of the pass**: the unfolded door's gloss in the lede's voice, 15/24 in ink (REVIEW m4); the account
   menu's wrapper a flex box in both seats (REVIEW m6: the trigger 2 px high in Arabic); no tap tint on the public
   chrome's links, buttons and summaries (REVIEW m7); under 30rem of height the sheet scrolls as one under its sticky
   head and the foot ends the list (A11Y_PERF m1: 78 % of a 320 × 256 viewport for the list, was 31 %); any
   `overlay:open` closes an open door panel (REVIEW m2: WebKit's press focuses nothing, so the nav's focusout never
   came) — the panel's switch to `overlay.js` stays open for W2-A's disclosure primitive (DL54-100 item 5); the scrim
   and an inline-end drawer beside a classic scrollbar's gutter routed to W2-A (REVIEW m1; the notes' «For W2-A» 4).
8. **The shared payload**: every page type +132 B gzip against the branch before the pass, −455 B against the base
   (`main.css` 42 152 → 41 697); no page sheet changed; one path more outside the slice (`overlay.js`), for the merge
   step to write into the manifest with the sixteen of the first step.

**Source.** `QA/v54/w2-c2/REVIEW.md` M1, M2, m1–m7; `QA/v54/w2-c2/A11Y_PERF.md` M1–M3, m1; `QA/v54/w2-c2/NOTES.md`
«Review fixes»; plan §1.6, §1.11, §1.12 items 6–9, §2.2, §2.3, §2.6; surfaces.md §1.4 N11, N13, N14; DL54-93,
DL54-94, DL54-100; `tests/frontend/test_browser_w2_c2.py`, `tests/frontend/test_nav_sheet_w2_c2.py`,
`tests/i18n/test_rtl_browser_w2_c2.py`.

## DL54-102 · 12 October 2026 · Steward, the w2-c2 merge: the family's two entries renumbered, the 17 paths assigned, the shared CSS gate passed with the shared payload 435 B lighter on every page type, every ceiling lowered to the merged weight, the capture report regenerated, three pins of what the family removed fixed

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w2-c2` into design-v5 on 12 October 2026 —
what the family's own entries and notes hand to the merge step: DL54-100, DL54-101; `QA/v54/w2-c2/NOTES.md`
«Ownership», «What is left», «Review fixes» and its «For W2-A»).

1. **The numbering.** design-v5 stood at `3780a7c` (the confidential-material docs commit, after W3-F2's shipped
   note): W3-F2's entries and its merge's record had taken DL54-96 … DL54-99, so the sync with design-v5 (`63b5860`)
   gave the family's two entries **DL54-100** and **DL54-101** (add 4). The second cited the first five times; those
   citations follow (the index row, «amends DL54-100 item 1», «DL54-100 item 5», the sources), and the sentence that
   called each number provisional now says what it was written as. The notes' closing section says how to read the
   numbers written before (`eec0e7c`); the code, the tests, DS 2026 and ACCESSIBILITY.md cite none of them. This entry
   is DL54-102.
2. **Two conflicts, both areas' work kept.** The decision log: design-v5's entries (W3-F2's three and DL54-99), then
   the family's two. `dist/main.css`: rebuilt — `static/css/dist` and `static/js/dist` deleted, `npm run build` — the
   JS byte for byte the branch's (W3-F2 changed no script), the three page sheets W3-F2 added byte for byte
   design-v5's. `components.css` and DS 2026 merged on their own; each is design-v5's plus exactly the family's diff
   (checked line for line). Nothing of W3-F2's draws what W2-C2 removed: the account menu's callers all pass
   `popover=True`, the language control's all pass `lang_names`, the self-sufficient error letterhead includes neither
   the header nor the nav, and the partial W3-F2 deleted (`accounts/partials/account_menu.html`) is named by no file.
3. **The 17 paths outside the slice are this area's in the manifest** (`2960180`). `scripts/check_ownership.py w2-c2
   3780a7c` listed exactly the paths the family declares (the first step's sixteen and the fix pass's `overlay.js`);
   each was read in the diff and found to be what it declares: `docs/ACCESSIBILITY.md` (the sheet's and the popover's
   rows; 2.4.3 Conforme with G-11 closed, and the summary's counts that follow), `docs/qa/design/capture.py` (the
   menu's geometry read on the sheet), `static/css/main.css` (the `v4/shell.css` import) and `static/css/v4/shell.css`
   (deleted), `static/js/main.js` (`initDropdowns`, deleted), `static/js/src/overlay.js` (the held scrim: four lines,
   A11Y_PERF M1; W2-A owns it from the merge), the V4 faces of `components/account_menu.html` and
   `components/language_segmented.html` (deleted; no caller left), the showcase's two demos, and eight test files
   whose assertions follow the sheet or the popover (no test removed; the drawer's assertions replaced by the sheet's).
   Six slices named as written: `chrome.css`, `nav.js`, `header.html`, `components.css`, `test_design_docs.py`,
   DS 2026. Three more paths came from the merge's own runs (item 9) and are assigned the same way. The check after
   it: 6 inside, 29 slice, 19 generated, and the two steward-only paths the steward wrote (the manifest, the capture
   report) — before: 17 outside; `--validate`: coherent, 25 families, 566 entries (20 added under w2-c2).
4. **The shared CSS gate (the owner's V5.8) passes: the shared payload falls on every page type.** On the bundles
   rebuilt from a clean `static/css/dist` and `static/js/dist`, `gzip.compress(data, 9)`
   (`evidence/v54/w2-c2/merge/budget_gate.log`):

   | Page type | design-v5 `3780a7c` | merged | change | ceiling before → after |
   |---|---|---|---|---|
   | an interior page (`main.css`) | 41 464 | 41 029 | −435 | 41 464 → **41 029** |
   | console page types (`main` + `console` + `portal`) | 50 205 | 49 770 | −435 | 50 927 → **49 770** |
   | «Mes pièces» (+ `documents.css`) | 51 377 | 50 942 | −435 | 52 099 → **50 942** |
   | the company's dashboard (+ `companies.css`) | 51 078 | 50 643 | −435 | 51 800 → **50 643** |
   | the login (+ `entrance.css`) | 46 325 | 45 890 | −435 | 46 325 → **45 890** |
   | the home (+ `hero.css`, `pages.css`) | 56 115 | 55 680 | −435 | 56 115 → **55 680** |
   | a content page (+ `cms/lettura.css`) | 45 520 | 45 085 | −435 | 45 520 → **45 085** |
   | an account page (+ `cms/servizio.css`) | 43 890 | 43 455 | −435 | 43 890 → **43 455** |
   | an error page (+ `cms/errori.css`) | 45 093 | 44 658 | −435 | 45 093 → **44 658** |

   `dist/main.css` 41 464 → 41 029 B: `v4/shell.css` and the V4 drawer's rules out, V4's segmented language track out,
   the sheet drawn on the portico's shared `.portico__*` rules, the fix pass's 132 B in (the family measured −455 B
   against its own base; −435 B on the merged tree). Every page-only sheet — `core/overlay-panels.css` included, which
   nothing of the family links — is byte for byte design-v5's; `console.css` and `portal.css` too. `dist/main.css`
   stands 5 051 B under its 45 KB cap (46 080 B).
5. **Every ceiling is lowered to the weight measured at this merge** — the orchestrator's definitive ruling under the
   owner's V5.8 (12 October 02:15: «savings are locked in: after a merge, the merged weight is the new ceiling»; a page
   type's total «ratchets down like the shared ceilings»), which supersedes plan §2.6 item 3's 1 KB margin that DL54-99
   still applied. The console page types' ceiling, 50 927 B since DL54-87 item 3 and kept by DL54-99, is now **49 770 B**;
   every row of the table above carries its new figure. A family that needs a shared rule pays for it with deletions.
6. **The public pages' script, recorded again for the orchestrator** (DL54-101 item 4, A11Y_PERF M3). Plan §2.3 puts
   `overlay.js` in `shell.js`, so the overlay core (6 476 B gzip) is on every public page: the home 51 156 B gzip of
   script against §2.6's «a public page ≤ 45 KB» (46 080 B), a door page 43 579 B, one more script request before
   `load`; the measured cost on the compressed twin is nil (pooled LCP 1 524 → 1 472 ms, the first-render task 62.8 →
   46.2 ms, TBT 180.6 → 134.4 ms). The figure stands exceeded by the plan's own placement until W4-B removes the Motion
   library's chunk (26 611 B). The merged JS is the branch's, byte for byte.
7. **The capture report and the inventory.** `docs/qa/design/capture.py` (whose selectors now follow the sheet) on
   lane 8 (8788, `ile_v5_l8`, DEBUG off, `--insecure`, one headless Chromium, exit 0): 43 captures, every one as
   expected; 29 differ, all of them the sheet (`4577ed4`) — the menu open fills the screen from the top (G-02: 844 /
   844 px at 390 × 844, 768 / 768 px at 1024 × 768; G-23: `top` 0, the key the script now records), the closed pages
   below 80rem lay out the V4 drawer's hidden icons no more, the open sheet lays out its doors' discs, and without
   script the letterhead holds its row only and sticks (G-04: 57 and 65 px); the 1440 captures are unchanged.
   `scripts/regen_design_inventory.py` then found one stale figure, DS 2026 §13's icons laid out (995 → 865), and wrote
   it (`3921d29`); §2's figures were current after the sync.
8. **The tests.** On the branch after the sync, the manifest, the capture report and the figures,
   `TEST_DATABASE_URL=…/test_ile_v5_l8`, one pytest and one browser at a time, every browser run behind the benchmark
   lock, no run crashed (`evidence/v54/w2-c2/merge/tests_*.log`). **The named set, non-browser** — `test_cms_nav.py`,
   `apps/cms`, `tests/compliance`, `test_overlays.py`, `test_overlays_console_w2_a.py`, `test_layout.py`, the two
   bundle-current tests, `test_design_docs.py`, `test_static_pipeline.py`, `tests/security` (the sentinel test ran),
   with the family's `test_nav_sheet_w2_c2.py`, `test_rtl_static.py`, W3-F2's two unit files, the ownership and
   inventory scripts' tests and what the merge touched besides (`test_v5_tokens`, the comments' leak test,
   `test_css_tokens_exist`, `test_loader_rules`, `test_static_assets`): **1 235 passed, 1 failed** (10 min 14 s) — the
   failure a pin of what the family removed (item 9). **Widened** to every other non-browser file of
   `tests/frontend` and `tests/i18n` (24 files), because that pin sat outside the named set: **727 passed, 2 xfailed,
   5 failed** (6 min 49 s) — three the family's (item 9), two design-v5's own (item 10). After the fixes:
   `test_static_assets` 39, `test_components_w1_c` 30, `test_page_integrity` 24, the overlay, sheet and ownership
   files 160 and `test_design_docs` with the inventory script 46 — all passed. **Browser** (headless Chromium):
   the family's `test_browser_w2_c2` and `test_rtl_browser_w2_c2`, the 320 px header test, W2-C1's
   `test_browser_w2_c1`, `test_browser.py`, `test_rtl_browser_nav` — **58 passed**; W2-A's `test_overlays_browser_w2_a`,
   `test_rtl_browser_overlays` and `test_overlays_console_browser_w2_a` with W3-A's two console browser files (the
   scrim's press changed in `overlay.js`) — **107 passed, 1 failed** (item 10); `test_rtl_browser` with W3-F2's two
   browser files — **39 passed**; W1-D's loader and reduced-motion files and W1-B's icons, which read the chrome —
   **35 passed, 3 failed** (item 10). `ruff check .` clean; `makemigrations --check --dry-run`: no changes. The full
   suite is the integration checkpoint's (V5.5).
9. **Three pins of what the family removed, found by the merge's runs and fixed** (`0ac4c43`, `a52dddf`; the paths
   assigned to w2-c2 as slices, the intents kept). `static/js/main.js`: the header line the family wrote («console.js
   and shell.js import it») tripped `test_main_js_is_an_es_module_without_external_dependencies`, which refuses any
   «import » in the file — reworded, a comment only (`main.js` is served as it is). `test_static_assets.py`: the same
   test pinned the dropdown fallback the family deleted (`aria-expanded`, `Escape` in `main.js`) — they are read in
   `overlay.js`, which owns the disclosures. `test_components_w1_c.py` read `v4/shell.css`, deleted — guarded by the
   file's existence, as its own `v4/buttons.css` test is. `tests/i18n/test_page_integrity.py`: the sheet draws «Fermer»
   on every page, «Close» in English, which is also the helpdesk's French source «Close» (`CLOSED`, une demande
   close): the French-leak guards read the English word as a leak on every English page; a French msgid that is also
   one of the language's own translations is no longer counted — three such homographs in the catalogues («Close»,
   «note», «note interne»). design-v5 passes the same tests; none of the three files was in the family's run list.
10. **Failures that are design-v5's own, handed over** — each reproduced on design-v5 at `3780a7c` the same way
   (`evidence/v54/w2-c2/merge/tests_design-v5_*.log`, `tests_browser_console_menu_isolated.log`), so not this merge's: `test_chips_cards_w1_c.py::
   test_the_chip_is_drawn_by_one_sheet` (W3-F2's `_lettura.css` styles `.registro__row > .chip`; for W3-F2 with W1-C's
   one-sheet rule); `test_script_motion_gate.py::test_no_animate_or_frame_loop_outside_the_gate` (W2-A's
   `overlay/extras.js` calls `requestAnimationFrame`; for W2-A with W1-D's gate); three of `test_loader_w1_d.py` (the
   submit guard now marks `aria-disabled` and lets the submit through, and the logout probe looks for
   `account-menu__link`, which the console's popover rows have not carried since W2-A and which no page carries after
   this merge; for W1-D with W2-A); and W3-A's
   `test_console_phone_browser_w3_a.py::test_menu_is_reached_in_three_keys_and_opens_a_drawer_that_holds_the_whole_rail`
   — the press on the scrim after a keyboard reopen leaves the console drawer open: alone it failed 2 runs of 3 on the
   branch and 2 of 3 on design-v5 (W2-A's intermittent defect, the one its merge saw once under load; cause not
   established; for W2-A).
11. **The worktree's `.env`** was a copy older than design-v5's (it lacked `ILE_CONFIDENTIAL_SENTINELS`, every other
   value equal): refreshed from design-v5's before the tests, so the confidential-material sentinel test ran instead of
   skipping. The file is ignored; nothing of it is committed.

**Why.** Entries renumbered after design-v5's keep the log's one order; paths nobody holds would have no writer for the
next family; the gate is read on the shared payload as V5.8 writes it, and a merged weight that becomes the ceiling
keeps every family on the weight the product has.

**Source.** The owner's V5.8 (`C:/tmp/ile_v5_council/directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`, the
orchestrator's definitive ruling at its end) and V5.5; plan §2.2 (the manifest; merge step 3), §2.3, §2.6; DL54-87
item 3; DL54-94; DL54-95 item 3; DL54-99; DL54-100; DL54-101; `QA/v54/w2-c2/NOTES.md` «Ownership», «Review fixes» and
«Merge step»; `QA/v54/w2-c2/A11Y_PERF.md` M3; the weights in `evidence/v54/w2-c2/merge/budget_gate.log`; the ownership
checks in `evidence/v54/w2-c2/merge/ownership_before.log`, `ownership_after_wt.log` and `ownership_after.log`; the
capture run in `evidence/v54/w2-c2/merge/capture_run.log`; the test runs in `evidence/v54/w2-c2/merge/tests_*.log`.

## DL54-103 · 11 October 2026 · W3-F1, step 1: the public interior as built

**Decision.** Built by W3-F1 (step 1: the doors and the project pages — /parcours/ and its sheets, /entreprises/,
/institutions/, /universites-et-formation/, /projet-pilote/, /forum/ with its registration pages, /le-projet/ and, on
its base, /agami/, /reseau/, /contact/, /attention-aux-fraudes/, each with its ar twin) on plan §3.5 item 1, with these
choices met during the build (plan §5.2):

1. **One grammar for the interior**, `static/css/v5/_interior.css` (a page partial, never in `main.css`, §2.3) and three
   page partials in `templates/pages/partials/` — `_ingresso.html` (the entrance), `_chapter_head.html` (the home's
   section device), `_linea.html` (a real sequence on a level line, open stations). The home's chapter grammar under
   the hero is the interior's: a head at the reading edge (four columns of twelve, sticky from 75rem), a body;
   48 · 64 · 96 px; hairlines before boxes.
2. **A door's lead is drawn where no frame is left** (§1.16). Every audience frame in the repository is that audience's
   navbar-panel frame and its hero-entrance frame, and the panel is on every page; the V1–V4 library is retired (AUM
   §7) and renders nowhere uncaptioned. The entrance's end seat holds «la porta»: the portico's door card (W2-C1) with
   its photograph replaced by a drawing — the night plate, the brand's three steps lit in the door's tint (the night
   plate is the arris's one seat, §1.4), the audience glyph once on the 36 px night disc (BI04), the accent as a 3 px
   rule. Decorative; the stair never mirrors (Q8), the disc moves with the inline start. A curated, captioned
   photograph takes the seat the day it exists (caption and credit under it, D26; the page's LCP image).
3. **D26 as layout slots**: one inset (a notice), one action (the action card of `v5/card.css`: one primary a page — the
   Forum in permanent mode makes the pilot's interest its primary, the pilot keeps the institutions' way as a
   secondary), an authority's host beside its link (`pathways.services.authorities` returns it), a caption and a
   credit under every photograph (a photograph renders only with its caption apparatus), «who can help me» with live
   text only — «Besoin d'aide ? Écrivez-nous :» and the site's address (an existing catalogue string, translated);
   the headings stay verbatim (the reader's questions are proposed in the notes for B1 item 7, never written).
4. **No side column** on an interior page: the sibling spaces and pages are the chrome's doors; a page does not repeat
   its chrome. The pathway pages keep «Dans l'Espace Personnes» as a closing register.
5. **The index in the entrance, never sticky** («Sommaire de la page», an existing string): the pathway sheet's and the
   Forum's V4 sticky bars are gone (W1-C's O2).
6. **Three corners a screen** (§1.3, DL54-14): the chrome draws 6 on every screen, so the interior's cards and its plate
   fold their 8 into that 6 (`.interior { --card-radius: var(--radius-md) }`) — 4 · 6 · full, measured ≤ 3 on every
   capture (1440, 1366, 1024, 390, 360; fr and ar).
7. **One thing once** (RH-5): the universities' presentational breakdown of the prescribed sentence (the same words a
   screen below the lead) is removed; the Forum's sections, the programme and the tribune are said once each.
8. **One diagram language** (CDV §19): `pilot-flow.svg` retired; the pilot's eight stations stand on «la linea» across
   the column (four a row from 48rem, eight from 80rem). W3-D's passage may replace it with one import line.
9. **What is being verified is said in words** on the «attesa» edge (a dashed rule at the reading edge), never a glyph
   in a box (the editorial body keeps ≤ 6 icons, DL54-29 item 1); the Forum's two empty pages keep the empty state's
   own glyph (W1-B: the handshake), drawn as the same row.

**Why.** Plan §3.5 item 1 and §1.18 D26; V5.5 (one direction, built). The measures, the answers to the items handed by
earlier areas and the headings proposed for B1 are in `docs/design-v5/QA/v54/w3-f1/NOTES.md`.

**Source.** Plan §3.5 item 1; §1.18 D26; §1.4 RH-1 … RH-8, SH-1 … SH-9; §1.3; §1.7; §1.16; DESIGN_SYSTEM_V5 BI04, PX15,
PX16, PX24; CREATIVE_DIRECTION_V5 §19; DL54-14; DL54-29; E/ = `C:/tmp/ile_v5_council/evidence/v54/w3-f1/`.

## DL54-104 · 11 October 2026 · W3-F1, step 1: the interior's page sheets, the legacy rules deleted, the CSS as measured, the paths outside the slice

**Decision.**

1. **Page sheets as plain import lists, written in the collected tree** (DL54-77): `ecosystem/ecosystem.css`,
   `forum/forum.css`, `pages/css/interior.css` (new — the institutional pages leave `pages.css`, which is the home's
   alone and 722 B lighter), `pathways/pathways.css` (new — the pathway pages had no page sheet: one CSS request more
   before `load` on the door-persons and pathway-detail page types). Each imports `css/v5/_interior.css` and its own
   partial (`_spaces.css`, `_forum.css`, `_institutional.css`, `_pathways.css`), so that a later family adds one line.
2. **The legacy rules no page draws any more are deleted** (§2.3, W3-F1's rows): `components.css` §24 `.section-nav*`,
   §22 `.pagination__icon-prev` (dead since W1-B), `layout.css` `.section--muted`, `.section--inverse`,
   `.container--wide/--narrow/--prose`; `dist/main.css` 42 472 → 42 316 B gzip. The rest of §9, §10, §18, §19, §24 and
   of layout.css's editorial parts is still drawn by W3-F2's pages and the second step's two pages.
3. **The page types' CSS, as measured** (gzip −9; for the steward to record — §2.6 item 5 under V5.5's performance rule,
   as DL54-44 and DL54-76 did): home 57 132 → 56 254 · institutional pages 46 555 → 45 363 · ecosystem 44 404 → 45 488 ·
   Forum 44 619 → 45 987 · **door-persons and pathway-detail 42 472 → 45 429, 943 B over the Wave-1 ceiling of 44 486**.
   The interior's grammar is new CSS while the legacy page header, breadcrumbs and local navigation stay in
   `main.css` for the pages that still draw them; `main.css` sheds them as W3-F2 and the second step move those pages.
   No LCP or long-task measurement on 8782 in this step.
4. **Paths outside the slice**, each justified (`QA/v54/w3-f1/NOTES.md` §6): the partial `static/css/v5/_interior.css`;
   the new sheets and partials beside the owned ones; `apps/pathways/static/**`; `apps/pathways/services.py`
   (`DEFAULT_ICONS` from the registry, the authorities' host); the app tests retargeted to the markup, their intent
   kept; `tests/frontend/test_icons.py`'s floor of empty-state callers (25 → 21: the pathway sheet's four sections say
   «being verified» in words); `static/img/illustrations/pilot-flow.svg` (deleted); DS 2026 §2.1 and §14.1.

**Source.** Plan §2.2, §2.3, §2.6; DL54-15; DL54-44; DL54-76; DL54-77; V5.5 («fix only real regressions»).

## DL54-105 · 11 October 2026 · W3-F1, step 2: orientation, the advice pages and the wizard as built

**Decision.** Built by W3-F1 (step 2: /orientation/ — the questionnaire's first page, its steps, the pre-evaluation,
the resume code —, /diplomes-et-titres/, /formation/, /attention-aux-fraudes/, each with its ar twin) on plan §3.5
item 1, with these choices met during the build (plan §5.2):

1. **The advice pages read like a pathway's sheet** (DL54-103): the entrance (the space's name, the prescribed title
   and body, the sheet's metadata row without a glyph), one chapter per question, «Dans l'Espace Personnes» as the
   closing register (the page leaves its own row out) and, last, the stone with the page's one action and the live
   «who can help me» line. V4's side column, its CTA band and its two-glyph metadata row leave with their last
   consumers (`_side_links.html`, `_orientation_cta.html`, `_metadata_row.html`).
2. **A real sequence stands on «la linea»** (DL54-103 item 8): the five moments of the diplomas down the reading edge,
   each station open and broken (its details are still being verified — said in words under the line), each
   glossary term under the station it belongs to — V4's timeline squeezed the labels into letter-wide columns at 1440;
   the two moments of «Formation» as two stations, each moment's word («Premier temps», «Second temps») in the
   numeral's seat beside its open ring (the order is in the words), its title at the entry's size, its text at the
   reading size and measure, its one way further. A phase is a record by DL54-55, but two phases in a row are a
   sequence, and «several records in a row are a list, not a row of boxes» (v5/card.css): no card.
3. **The fraud warning is a warning notice of the core components** (v5/notice.css — the amber register, its edge
   broken): the anti-fraud entry's mark (`shield-alert`, the registry's), the prescribed title in the register's word
   (its capitals tracked, TR rule 6), the broken rule — the kind said three times, never by colour; no red, no
   alarm. On «Attention aux fraudes» the prescribed text stays byte-identical as the page's one inset, under a
   visible title, «Votre protection» (an existing string, the entrance's label until now): with the page's h1 just
   above, a hidden title left the notice saying its kind twice only. On the Arabic page the callout's French title is
   a run inside a heading that keeps the page's direction, so it ends on the reading edge beside the mark.
4. **The questionnaire on the core components**: the progress as a quiet register (the count in words over a 2 px
   line on its hairline, filled from the reading edge — no pill, no movement); the question as the fieldset's legend;
   «Plusieurs réponses possibles.» said before the choices and wired to the group; the choices as plates around the
   native controls of v5/field.css (24 px; the whole plate the label's target, the control on top of it); an error
   announced, wired to the group (`aria-describedby`, `aria-invalid`), said in words beside the refusal's mark
   (`circle-alert`), the plates' edges doubled in the refusal's ink; ONE primary, «Continuer», first in the DOM (Enter
   submits it), «Précédent» after it, after a hairline, part of the page — on a phone «Continuer» takes the row.
5. **The keyboard model of a questionnaire that posts a page per answer** (wizard.js): a step reached from the
   questionnaire itself (the referrer is one of its pages) puts the focus on the new question — the legend, a
   programmatic target with no ring and no tab stop — instead of leaving it at the top of the document; a step opened
   any other way keeps the browser's start.
6. **The pre-evaluation keeps one inset**: the informational banner stands in the entrance under the h1 (the result
   and what it is worth read together); the disclaimer joins the record's facts as the page's quiet note; the resume
   code, shown once, keeps the warning's register (a one-time secret, not an editorial inset); the pathway family is a
   register row whose prescribed title links its sheet — its description as written (DL54-103's decision 10).
7. **On the Arabic page** a French question and a French choice read left to right and end on the reading edge —
   the question as every French head of the interior, a choice beside its control; the help and the bodies keep their
   own alignment.

**Why.** Plan §3.5 item 1, §1.18 D26 (one inset, one action, «who can help me»), §1.4 (RH-5 one thing once; SP-8 the
targets), §1.6, §1.7 (the six-icon ceiling), DL54-51 (tier 0), DL54-70 (the questionnaire's foot), DL54-103 (the
interior's grammar); V5.5. The measures and the items answered are in `docs/design-v5/QA/v54/w3-f1/NOTES.md` (step 2).

**Source.** Plan §3.5 item 1; §1.18 D26; §1.3; §1.4; §1.6; §1.7; DL54-51; DL54-55; DL54-70; DL54-103;
E/ = `C:/tmp/ile_v5_council/evidence/v54/w3-f1/step2/`.

## DL54-106 · 11 October 2026 · W3-F1, step 2: «Ma situation»'s guided form leaves main.css, the CSS as measured, the paths outside the slice

**Decision.**

1. **`v4/wizard.css` is retired** (plan §3.5 item 1, §2.3's W3-F1 row): «Ma situation»'s guided form is console-only,
   so its rules leave the cascade every page loads and are rewritten on the V5 tokens as the console partial
   `apps/portal/static/portal/v5/_wizard.css`, one import line in `portal/console.css` after the shell (plan §2.2:
   «each Wave-3 family adds its own partial's import, through the steward»). The markup is other families' and is not
   touched (`templates/portal/situation.html` W3-E, `components/wizard_stepper.html` W3-D, `option_cards.html`): the
   Stepper's rules stand in the partial until the journey family redraws it.
2. **Three corners a screen** (§1.3; W3-A counted five — the panel at 12, the field at 6, the foot at 8): the console's
   4 · 8 · full — the question's panel and «Ce que nous ne demandons pas» at 8 (the console's panel, W3-B's), the
   controls, the OptionCards and the date field at 4 (the plate of v5/field.css), the nodes and the discs full. One
   raised panel (level 2); no light behind the question (the glow is retired); no glass on the foot (SH-5: the two
   sticky bars are glass's one seat): the foot is part of the page at every width, after a hairline, its controls
   wrapping (DL54-70) — on a phone the one act, «Continuer» (the submit on the last question, situation.js), takes
   the row. The current node says itself in words and weight as well as by its ring; a chosen card by its doubled
   edge and the person's own check (O14).
3. **The legacy layout rules no page draws any more** since the two advice pages moved: `.section--rule`,
   `.section--tight`, `.grid-auto`, `.layout-sidebar--end`, `.stack--sm`, `.stack--lg` (`layout.css` 9 296 → 8 795 B).
   The rest of components.css §9, §10, §18, §19, §24 and of layout.css's editorial parts is still drawn by W3-F2's
   pages, the home and the console.
4. **The CSS as measured** (gzip −9, for the steward to record — §2.6 item 5 under V5.5's performance rule, as
   DL54-104 did): `dist/main.css` 42 316 → **41 212** on every page type; door-persons and pathway-detail 45 430 →
   **44 486** (at its Wave-1 ceiling: 943 B over before this step); institutional pages 45 364 → 44 266; ecosystem
   45 489 → 44 385; Forum 46 093 → 44 989; home 56 254 → 55 150; the console page types 49 894 → **49 986**, under
   their 50 086 ceiling (the guided form moves from main.css into the console entry); **the orientation pages 43 659 →
   45 533**, 1 047 B over the interior's Wave-1 ceiling of 44 486 — they draw the interior's grammar now (the partial,
   ≈ 3 KB) where V4 had a 1.3 KB sheet of their own; recorded, not traded against the pages (no LCP or long-task
   measurement on 8782 in this step: the lane is not the production shape).
5. **Paths outside the slice**, each justified (`QA/v54/w3-f1/NOTES.md`, step 2): `apps/portal/static/portal/v5/
   _wizard.css` (new: the guided form's console-only home) and `apps/portal/static/portal/console.css` (its one
   import line, through the steward); `apps/pathways/static/pathways/_pathways.css` (step 1's partial, extended);
   two tests retargeted, their intent kept — `tests/frontend/test_console_shell_w3_a.py` (the import list accepts a
   family's partial after the shell, as W3-B's branch writes it) and `tests/frontend/test_chips_cards_w1_c.py` (the
   interior's chip and tag placements named; Formation no longer draws cards); the DS 2026 §2 table regenerated by
   `scripts/regen_design_inventory.py` (the row of `v4/wizard.css` removed, the weights), as W2-D did.

**Source.** Plan §1.3; §1.4 SH-2, SH-5, SH-8; §2.2; §2.3; §2.6; DL54-15; DL54-55; DL54-70; DL54-73; DL54-77; DL54-104;
V5.5 («fix only real regressions»).

## DL54-107 · 11 October 2026 · W3-F1, the fix pass: the door card carries the door's way in; RH-3 met on /parcours/, the needs form recorded outside it, two pages waived until their frames exist; the questionnaire says its place in words; the door card's CSS loads only on the doors

**Decision.** The senior review (`QA/v54/w3-f1/REVIEW.md`: five majors, eight minors) and the accessibility and
performance check (`QA/v54/w3-f1/A11Y_PERF.md`: one major, two minors), fixed in one pass (V5.5), each on the review's
one direction:

1. **«la porta» carries the door's way in** (M1). The end seat's plate keeps its night, its disc and its accent rule and
   holds what the door offers first, where the portico's panel shows a photograph (`templates/pages/partials/
   _via.html`): on /parcours/ the questionnaire's action card — its title, its sentence, «Commencer le questionnaire
   d'orientation», the page's one primary; on /institutions/ and /universites-et-formation/ the prescribed button and
   its one sentence, the page's one primary; on /entreprises/ the way to «Recueil des besoins» as a secondary — the
   form's submit stays the one action. The drawn stair leaves (and with it m2, its Arabic collision). A curated,
   captioned photograph takes the seat the day it exists (D26); the way in then stands under the lead. Measured
   (`E/fix/measure/`): the door's control at 293–437 px at 1440 × 900 and 1366 × 768 on the four doors, fr and ar (the
   review: 1.8–5.1 screens down); on phones at 490–617 px on /institutions/ and /universites-et-formation/, 697–710 px
   on /entreprises/ and 779–885 px on /parcours/. There the locked lead runs ten to twelve lines at 360–390 px, so CD
   §10's «primary within 560 px at 360 × 800», written for a lead of at most three lines, is not reached: the control
   is not set above the lead, whose disclaimer («ces décisions relèvent exclusivement des autorités compétentes») is
   read first.
2. **RH-3** (M2). On /parcours/, «Comment ça marche» stands on «la linea»: the locked sentence cut on its own « → » into
   four stations, its opening words kept as hidden text and its caveat under them (CD law 8; the owner’s D-U4 allows
   the home the same split of the same text). Joined back, the words are the registry's sentence character for character; a
   sentence of another shape stands whole (`pathways.services.how_it_works`). The largest stretch without a figure is
   now 0.98 / 1.84 / 2.00 screens at 1440 / 390 / 360 (was 2.25 / 4.01). **Recorded outside RH-3's cadence:** the
   needs form of /entreprises/, a task rather than reading — its six short single-line fields stand two by two from
   64rem (≈ 290 px shorter); the stretch that remains is the form (3.15 / 4.23 screens). **Waived until curated,
   captioned frames exist (§1.16):** /forum/ (prescribed prose; 3.99 / 6.18 screens) and /le-projet/ on a phone (2.85
   at 390). The condition that lifts the waiver: the Image Art Director's curated, captioned frames for these slots;
   a frame takes its seat with one partial.
3. **The questionnaire says its place in words** (M3, FM12): «Question n sur N au maximum», the catalogue's string (it,
   en, ar), is the visible count; no percentage, no `<progress>`; the quiet line stays; a test asserts that no «%» is
   rendered in a step. **Its first page holds its action in the entrance** (M4): the inset «À lire avant de commencer»
   under the lead, the action card in the end seat from 64rem («Commencer» at 342 / 370 px at 1440 × 900 /
   1366 × 768; was 1 152 / 1 200), right after the inset on a phone (882 / 986 px at 390 × 844 / 360 × 800; was
   1 512 / 1 644 — after the lead and the inset, which are read first), the three moments after it. **A step's head
   is its compact title** (m5): the page's sentence is said once, on the first page; «Continuer» is inside the first
   screen at 1440 × 900 (832–884 px); at 1366 × 768 the six-choice first question still sets «Continuer» 64 px under
   the fold.
4. **The pilot's eight stations stand in one row from 90rem** (M5), four a row below it: «ACCOMPAGNEMENT» no longer
   breaks in its middle.
5. **The minors.** The Forum's programme numbers its rows 01 … 08 unless every row has a time (CD §20), the first row's
   words whole, «15h00 — Accueil et enregistrement» (m1). The entrance's index is one link a row at every width (m3).
   «Destinataires» is the prescribed sentence as written, the chapter's body (m4; the presentational list and its
   partial deleted). French on an Arabic page says so on its own element — the Forum's untranslated eyebrow and name,
   the trail's link to it, /agami/'s question and answer (m6; A11Y finding 2). On the Arabic page a French lead keeps its
   own start in a box on the reading edge no wider than its words, while heads still end on the reading edge (m7, the
   interior's half; the home's lead is W2-D's, handed to the steward). The portico's double current marker is handed
   to W2-C1 / W2-C2 (m8).
6. **SP-8** (A11Y finding 1): the trail's links and the chapters' forward links are boxes on `--hit-min` (24 px) and on
   `--hit-primary` (44 px) under a coarse pointer, with the «Termes utiles» tags and /contact/'s address; boxes, not
   pseudo-targets, so two rows of links never overlap.
7. **The door card's CSS loads only where a door is drawn** (V5.8: a surface's own CSS loads only where it is drawn):
   `static/css/v5/_porta.css`, imported after the interior's grammar by the two door sheets alone
   (`pathways/pathways.css`, `ecosystem/ecosystem.css`); «Comment ça marche»'s rules in `_pathways.css`. **The CSS as
   measured** (gzip −9 of the bundles, per page type; the shared payload `dist/main.css` 41 203 → 41 203, unchanged):
   persons 44 464 → 44 586 (100 over the interior's ceiling of 44 486); ecosystem 44 362 → 44 483 (under); Forum
   44 970 → 44 671 (185 over); institutional 44 244 → 43 915; orientation 45 513 → 45 172 (686 over). Page-only sheets,
   for the steward to record beside DL54-106's figures (A11Y finding 3). After design-v5's −646 B on `main.css` (W3-B),
   only orientation stays over, by ≈ 40 B; W3-F2's deletions of the legacy page header, trail and local navigation
   bring it under.
8. **Paths outside the slice** (for the merge step's manifest): `static/css/v5/_porta.css` (new, beside
   `_interior.css`); `apps/forum/services.py` and `apps/forum/views.py` (the Forum's untranslated name says its language
   on the page and in the trail); `apps/pathways/views.py` (the cut sentence, `how`; `apps/pathways/services.py` was
   already outside); `apps/pathways/tests/test_compliance.py` (a locked text cut for layout is read back whole).

**Why.** V5.5 (implement → review once → fix → ship), on the review's one direction per item; V5.8 (the CSS budget). The
measures, the runs and what is left are in `docs/design-v5/QA/v54/w3-f1/NOTES.md`, «Review fixes».

**Source.** `QA/v54/w3-f1/REVIEW.md`; `QA/v54/w3-f1/A11Y_PERF.md`; plan §1.4 RH-3, SP-8; §1.16; §1.18 D26;
CREATIVE_DIRECTION_V5 law 8, §10, §19, §20; DESIGN_SYSTEM_V5 §11 (FM12); DL54-103 … DL54-106; V5.8;
E/ = `C:/tmp/ile_v5_council/evidence/v54/w3-f1/`.

## DL54-108 · 12 October 2026 · W3-F1, the budget and consolidation pass: one partial for the public interior's shared components; the shared sheet sheds what the interior replaces; a page sheet holds what its pages draw; the page types as measured

**Decisions** (the owner's V5.8 as the orchestrator's definitive ruling reads it, 12 October 02:15: the shared bundles
never rise and ratchet down; page-only sheets for what a surface draws, measured, after reuse and deletion, with a
performance sanity check; no duplicated component family — the family that merges second consolidates; V5.5):

1. **The sync.** design-v5 at `v54/w3-f2` (`bfd2901`) merged into the branch (`76429f2`): `console.css`'s import list
   in landing order (W3-B's dashboards, then this area's guided form), `layout.css`'s two deletions in one hunk
   united, DS 2026 (§2 regenerated; §2.1 both families' rows; §10's `local_nav.html`, §10.1), this log (design-v5's
   entries first, this area's five renumbered DL54-103 … DL54-107, the fix pass's index row added); `--rank-c-block`
   labelled «riserva» (W2-A's `.section--c` and this area's `.section--tight` were its last consumers); the bundles
   rebuilt from a clean dist.
2. **One partial for the public interior's shared components** (rule 3; W3-F2's review m11). W3-F1's `_interior.css`
   and W3-F2's `_lettura.css` drew the trail, the head, the chapters' device, the register's rows and D26's shared
   slots (an authority's host, a photograph's caption and credit, «who can help me») value for value. They are drawn
   once in `static/css/v5/_pagina.css`, the first import of `pathways/pathways.css`, `ecosystem/ecosystem.css`,
   `forum/forum.css`, `pages/css/interior.css`, `orientation/wizard.css` and `cms/lettura.css`; each surface keeps only
   its own parts in its own partial. The head is one drawing for the two vocabularies (W3-F1's entrance `.ingresso`,
   W3-F2's `components/page_header.html`); a shared rule carries one selector and wins over main.css's legacy
   components by order. W3-F2's twelve pages measured on the lane — every element's computed style and every pixel,
   fr and ar, 1440 and 390 — are identical; W3-F1's pages take W3-F2's drawing where the two differed: the trail's
   links are 24 px boxes whose target grows to 44 px under a finger (they were 44 px boxes at rest:
   `--hit-min` still carries V4's 44 px through `v5/aliases.css`, so DL54-107 item 6's «boxes on `--hit-min` (24 px)»
   were 44 px boxes — corrected here for the trail; the forward links keep their 44 px boxes), the help line's address
   is one box, the quiet chapter's label is untracked. The service pages' sheet keeps its own trail and help line (the
   account and error pages draw none of the rest: importing the shared page would load rules they never draw).
3. **The shared sheet sheds what the interior replaces** — each rule proved unused (the templates, Python, JS and JSON
   of the merged tree and the files the in-flight worktrees changed; a component template checked for its includers)
   or re-drawn by every page that still draws its element: `components.css` §9 keeps the trail's skeleton (its box,
   type, links, hover and current page are re-drawn by the shared page, the account pages and the console's bar);
   §10 keeps the running head the console reads (capitals, case-sensitive forms); the legacy page header's box, title,
   lead, meta and centred variant, the legacy hero (`components/hero.html`: no includer) and §24, the local navigation
   (`components/local_nav.html`: no includer), leave; `register.css` loses the page header's capital titles (DS 2026
   §3: `--track-caps-display` a «riserva»), the folio in the zones' rail, the gloss in the zones' margin, the verso and
   home plates; `layout.css` the annotated block's reading column, the sidebar layout, the accent rule. Left, used:
   §17 (the design showcase; W3-D retires it with its passage), §19 (the console's access point), the jurisdiction bar
   (a component W2-D kept), the outcome's modifiers (composed in templates), the sequence's crossing (W3-D's branch).
4. **A page sheet holds what its pages draw** (rule 2). `components.css` §18, the pathway list, goes to the home's
   `pages.css` (its one consumer; the home already re-drew it and read of §18 only its titles' face and the stretched
   link); the rules of `_interior.css` one surface alone draws go to that surface's partial (the wide chapter → the
   spaces; the register whose rows name WHO → the institutional pages; a row's fragment, a row still being prepared,
   what is still being verified → the pathways), each at the top of its partial. «la linea» stays in `_interior.css`
   for W3-D, which moves it into its passage and imports it where it is drawn.
5. **The CSS as measured** (gzip −9 of bundles rebuilt from a clean dist; design-v5 at `v54/w3-f2` → this pass):
   `main.css` 41 464 → **39 111** (every page); the console page types 50 205 → 48 984, «Mes pièces» 51 377 → 50 156,
   the company's dashboard 51 078 → 49 857; the login 46 325 → 43 972; the home 56 115 → 53 049; the content pages
   45 520 → 43 212, the account pages 43 890 → 41 537, the error pages 45 093 → 42 740; the ecosystem doors 43 396 →
   42 446, the Forum 43 611 → 42 605, the institutional pages 45 547 → 41 908; **the persons pages** (main.css alone →
   + `pathways/pathways.css`, their first page sheet) 41 464 → **42 605**; **orientation** (+ `orientation/wizard.css`)
   42 796 → **43 150**. The two page types that grow do so through their own page-only sheets, for what their pages
   draw: the steward records them as measured (rule 2).
6. **The performance sanity check** (the lane, dev server, uncompressed static; CPU ×4, 150 ms RTT, 1.6 Mbps; a fresh
   context a load; blocks design-v5 · branch · branch · design-v5 · branch, n = 8 a cell a block; medians of the block
   medians): LCP on the person door fr 1440 1 897 → 1 902 ms, a pathway sheet fr 412 1 935 → 1 922, orientation fr 412
   1 937 → 1 912, the person door ar 412 2 097 → 2 134 (blocks 2 094 – 2 146 against 2 082 – 2 112); FCP equal or earlier
   in every cell (the shared sheet 18 KB lighter uncompressed); the LCP element the entrance's lead on both trees. No
   meaningful regression (V5.5).

**Source.** V5.8 (the orchestrator's definitive ruling, 12 October 2026, 02:15); V5.5; `QA/v54/w3-f2/REVIEW.md` m11;
DL54-99; DL54-103 … DL54-107; plan §2.3 (the deletion map); `QA/v54/w3-f1/NOTES.md` «Budget and consolidation» (the
proofs, the comparisons, the measures, the paths outside the slice); E/ =
`C:/tmp/ile_v5_council/evidence/v54/w3-f1/budget/`.

## DL54-109 · 12 October 2026 · Steward, the w3-f1 merge: the family's six entries renumbered, the 31 paths assigned and four slices named as written, the shared CSS gate passed with the shared payload 2 346 B lighter on every page, every ceiling lowered to the merged weight, the public interior's five page types recorded

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w3-f1` into design-v5 on 12 October 2026 —
what the family's own entries and notes hand to the merge step: DL54-103 … DL54-108; `QA/v54/w3-f1/NOTES.md` «Steward»
and «Budget and consolidation» §30 – §34).

1. **The numbering.** design-v5 stood at `8e13cd2` (W2-C2's shipped note): W2-C2's two entries and its merge's record
   had taken DL54-100 … DL54-102 while the branch held DL54-100 … DL54-105 from its budget pass's sync, so the steward's
   sync (`47f7343`) gave the family's six entries **DL54-103 … DL54-108** (add 3; their headings, their index rows and
   their own cross-references — every DL54-100 … DL54-105 in their text was the family's own; the code, the tests, DS
   2026 and the manifest cite none of the moved numbers); the notes' closing section says how to read the numbers
   written before (`a8ebb27`). This entry is DL54-109.
2. **Two conflicts, both areas' work kept.** DS 2026 §2's inventory rows — both hunks there: design-v5's rows (W2-C2's
   prose and weight of `v5/chrome.css`), then `scripts/regen_design_inventory.py --write`, which renumbered the rows in
   `main.css`'s order and took out `v4/wizard.css`'s row (no longer imported); the family had changed no row's prose
   there. The decision log: design-v5's entries, then the family's. `static/css/components.css` and `main.css`'s import
   list merged without a conflict and were read: the merged sheet is design-v5's less exactly the family's deletions
   (§9's and §10's re-drawn rules, the legacy hero, §18, §24) and the branch's less exactly W2-C2's; the import list is
   design-v5's without `v4/wizard.css`. `static/css/dist` and `static/js/dist` deleted and rebuilt (`npm run build`);
   the JS byte for byte design-v5's but for the shared chunks' names, which follow the worktree — the family changed no
   bundled script (`orientation/wizard.js` is an app file loaded as it is). **One semantic conflict**, green on each
   branch and red on the sync, found by the targeted tests: W2-C2's phone sheet draws a primary of its own («Découvrir
   le questionnaire d'orientation», `nav-sheet__primary`) earlier in the document than a page's content, and two of the
   family's gated-door tests took the document's first primary for the page's prescribed button; they read it in `<main
   id="main-content">` now, the intent kept (`78cb0de`).
3. **The 31 paths outside the slice are this area's in the manifest** (`d4f4b40`). `scripts/check_ownership.py w3-f1
   8e13cd2` listed exactly the paths the family declares — the earlier steward's 27 (NOTES §6, §16, §24 and «Steward»)
   and the budget pass's four (§34) —; each was read in the diff and found to be what it declares. Whole files (21): the
   page partials `static/css/v5/_interior.css`, `_pagina.css` (the public interior's shared components, drawn once for
   W3-F1's and W3-F2's pages — V5.8 rule 3) and `_porta.css`; the page sheets and partials
   `apps/pages/static/pages/css/{interior,_institutional}.css`, `apps/ecosystem/static/ecosystem/_spaces.css`,
   `apps/forum/static/forum/_forum.css`, `apps/pathways/static/pathways/{pathways,_pathways}.css`; the console partial
   `apps/portal/static/portal/v5/_wizard.css`; the retired `static/img/illustrations/pilot-flow.svg`; ten test files of
   the pages the area owns. Slices (10): `apps/pathways/services.py` and `views.py`, `apps/forum/services.py` and
   `views.py` (files no family held), `console.css`'s import line (W3-A's), W3-F2's `_lettura.css`, `lettura.css` and
   `test_content_pages_w3_f2.py` (the consolidation), W1-C's chip test and W1-B's icon test. Four of the family's slices
   named as written: `pages.css` (the pathway list's drawing, its one consumer's), `register.css` (the capitals of the
   prescribed titles), `layout.css` (the editorial rules deleted, each proved unused) and DS 2026. The check after it:
   75 inside, 27 slice, 24 generated, and the manifest itself, the one steward-only path (before: 31 outside);
   `--validate`: coherent, 25 families, 597 entries.
4. **The shared CSS gate (the owner's V5.8 and the orchestrator's definitive ruling of 12 October, 02:15) passes: the
   shared bundles fall.** On the bundles rebuilt from a clean `static/css/dist` and `static/js/dist`,
   `gzip.compress(data, 9)` (`evidence/v54/w3-f1/merge2/gate.log`):

   | Page type | design-v5 `8e13cd2` | merged | change | ceiling before → after |
   |---|---|---|---|---|
   | every page, and an interior page with no sheet of its own (`main.css`) | 41 029 | 38 683 | −2 346 | 41 029 → **38 683** |
   | console page types (`main` + `console` + `portal`) | 49 770 | 48 556 | −1 214 | 49 770 → **48 556** |
   | «Mes pièces» (+ `documents.css`) | 50 942 | 49 728 | −1 214 | 50 942 → **49 728** |
   | the company's dashboard (+ `companies.css`) | 50 643 | 49 429 | −1 214 | 50 643 → **49 429** |
   | the login (+ `entrance.css`) | 45 890 | 43 544 | −2 346 | 45 890 → **43 544** |
   | the home (+ `hero.css`, `pages.css`) | 55 680 | 52 621 | −3 059 | 55 680 → **52 621** |
   | a content page (+ `cms/lettura.css`) | 45 085 | 42 784 | −2 301 | 45 085 → **42 784** |
   | an account page (+ `cms/servizio.css`) | 43 455 | 41 109 | −2 346 | 43 455 → **41 109** |
   | an error page (+ `cms/errori.css`) | 44 658 | 42 312 | −2 346 | 44 658 → **42 312** |
   | **the persons pages** (`main.css` alone → + `pathways/pathways.css`, their first page sheet) | 41 029 | 42 177 | +1 148 | — → **42 177** (recorded) |
   | the ecosystem doors (+ `ecosystem/ecosystem.css`) | 42 961 | 42 018 | −943 | — → **42 018** (recorded) |
   | the Forum (+ `forum/forum.css`) | 43 176 | 42 177 | −999 | — → **42 177** (recorded) |
   | the institutional pages (`pages.css` → `pages/css/interior.css`) | 45 112 | 41 480 | −3 632 | — → **41 480** (recorded) |
   | **orientation** (+ `orientation/wizard.css`) | 42 361 | 42 722 | +361 | — → **42 722** (recorded) |

   `dist/main.css` 41 029 → 38 683 B (−2 346 on every page): the legacy trail, page header, hero, local navigation and
   pathway list of `components.css`, the editorial rules of `layout.css` and `register.css` that no template draws, and
   `v4/wizard.css` (11.7 KB) leave the shared sheet — the last for the console partial `v5/_wizard.css`, so
   `console.css` grows by 1 132 B and the console page types are 1 214 B lighter (DL54-106, DL54-108). `portal.css`,
   `entrance.css`, `hero.css`, `documents.css`, `companies.css`, `servizio.css`, `errori.css` and
   `core/overlay-panels.css` are byte for byte design-v5's; `pages.css` loses the institutional pages' rules and gains
   the pathway list's drawing; `lettura.css` imports the shared page (+45 B). `dist/main.css` stands 7 397 B under its
   45 KB cap (46 080 B).
5. **Every ceiling is lowered to the weight measured at this merge** (the definitive ruling: «after a merge, the merged
   weight is the new ceiling»; a page type's total «ratchets down like the shared ceilings»; DL54-102 item 5): every row
   of the table that had a figure carries its new one. A family that needs a shared rule pays for it with deletions.
6. **The public interior's five page types of this area are recorded as measured** — page-only sheets, where V5.8 puts a
   surface's own CSS (rule 2). **The persons pages** (/parcours/, the pathway sheets, «Diplômes et titres», «Formation»)
   loaded `main.css` alone and now load their first page sheet, `pathways/pathways.css` (3 494 B: the shared page, the
   interior's own parts, the door card, the pathways' rules): **42 177 B**, +1 148 B on their own pages while every
   other page type is lighter. **Orientation** grows through its own sheet (`orientation/wizard.css` 1 332 → 4 039 B:
   its V4 sheet replaced by the interior's grammar and the questionnaire's rules): **42 722 B** (+361 B). The ecosystem
   doors (**42 018 B**), the Forum (**42 177 B**) and the institutional pages (**41 480 B**, `pages.css` →
   `pages/css/interior.css`) are lighter than before and recorded at their measured totals. Each grows, where it grows,
   only through its own sheet, only for what its pages draw, after the reuse (the shared page) and the deletions above;
   the performance sanity check is the family's (NOTES §31, the lane, CPU ×4, 150 ms RTT, n = 8 a cell in five blocks):
   FCP equal or earlier in every cell, LCP within the series' spread (+37 ms at most, on the Arabic door) — no
   meaningful LCP or first-render regression (V5.5). From this merge the five totals ratchet down like the others.
7. **The capture report and the inventory.** `docs/qa/design/capture.py` on lane 7 (8787, `ile_v5_l7`, DEBUG off,
   `--insecure`, one headless Chromium, exit 0): 43 captures, every one as expected, and the report the one design-v5
   holds, byte for byte once its line ends are LF (the script writes CRLF; the committed file is kept, nothing to
   commit) — the capture's pages (the home, the privacy page, the login, the 404) lose no figure the report records (the
   status, the overflow, one h1, the direction, no external request, no empty icon, the drawer's and the header's
   geometry, the focus after an invalid submit). `scripts/regen_design_inventory.py`: §2's rows renumbered and
   `v4/wizard.css`'s row out in the sync itself; current after the manifest and the capture.
8. **The tests.** On the branch after the sync, the manifest and the numbering note (`47f7343` … `a8ebb27`),
   `TEST_DATABASE_URL=…/test_ile_v5_l7`, one pytest at a time, every browser run behind the benchmark lock, no lane
   server of the steward's beside them: the area's targeted set without the browser — `tests/i18n`, `tests/compliance`,
   `tests/security`, the orientation, ecosystem, pages and pathways apps, the Forum's public tests, «Ma situation»'s
   view tests, the family's and W3-F2's unit files, `test_layout.py`, `test_design_docs.py`, the two bundle-current
   tests, `test_static_pipeline.py` (a real `collectstatic`), O14, the chips' register, the icons, and what the merge
   touched besides (W2-C2's sheet test, W1-C's chip and component tests, the CMS navigation, the overlays, the loader
   rules, the console shell's tests and sheets, the template comments, the static assets, the chips' registry, the
   tokens, the ownership and inventory scripts' tests) — **2 065 passed, 2 failed, 1 skipped** in 37 min 41 s: the two
   failures were the semantic conflict of item 2, fixed (`78cb0de`; the file then 63 passed); the skip is the
   confidential-material check without its private sentinel table (`ILE_CONFIDENTIAL_SENTINELS`), by design. The browser
   set, five runs — the family's two files (23), the doors' and the home's (47), `tests/i18n`'s RTL files with W2-C2's
   (47), W3-F2's two files and W3-A's questionnaire foot (17), W2-C2's browser file (25) — **159 passed**, no skip, no
   crash. The full suite is the integration checkpoint's (V5.5).

**Why.** Entries renumbered after design-v5's keep the log's one order; paths nobody holds would have no writer for the
next family; the gate is read on the shared payload as V5.8 writes it, and a merged weight that becomes the ceiling
keeps the savings for the product.

**Source.** The owner's V5.8 (`C:/tmp/ile_v5_council/directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`, and the
orchestrator's definitive ruling below it) and V5.5; plan §2.2 (the manifest; merge step 3), §2.3, §2.6; DL54-102 items
4 and 5; DL54-99 items 4 – 6; DL54-103 … DL54-108; `QA/v54/w3-f1/NOTES.md` «Steward», «Budget and consolidation» and the
closing numbering note; the weights in `evidence/v54/w3-f1/merge2/gate.log`; the ownership checks in
`evidence/v54/w3-f1/merge2/ownership_before.log` and `ownership_after.log`.

<!-- W3-C (12 October 2026): the family's ten entries, written as DL54-96 … DL54-105 on its branch (its step-1 entries first as DL54-82 … DL54-85), follow as DL54-110 … DL54-119 — after design-v5's DL54-109 (W3-F2's three entries and the record of their merge, W2-C2's two and theirs, W3-F1's six and theirs reached design-v5 first); renumbered at the steward's pre-merge sync (label w3-c-merge), content unchanged but for the cross-references between the ten. The family's notes, review and accessibility report keep the numbers they were written with: QA/v54/w3-c/NOTES.md «Merge step — the steward's note on numbering» says how to read them. -->

## DL54-110 · 11 October 2026 · W3-C: «Mes pièces» V5.2 — the strip, one partition, the row as the link

**Decision.** The register (`templates/documents/partials/register.html`, the same presenter and authorisation for
`/fr/espace-reserve/mes-documents/` and `/documents/`) is the V5.2 comp, built on the shipped system (W3-A's frame,
W3-B's grammar, W1-C's chip and fields), with the decisions the platform map gave the team (the platform map §5, O77;
DOCUMENT_WORKSPACE §17):
- **«Il registro» is a strip, the screen's ONE raised plane** (the action card's level, as the dashboard's NowPanel):
  three runs — whose move it is — each a count at 20/28 (D7: never the stat card's 28 px numeral), one 16 px mark per
  piece (the colour is the run, the shape is the state; counts alone above 24 pieces) and a link to its group (an
  index, not a filter); then **the page's one primary with its piece and its date**, «Votre prochaine action» — T1's
  piece (`cases.services.next_action(case, reader=user)`) when the reader answers for it, otherwise T1's precedence
  over the open pieces the reader answers for, so the dashboard and «Mes pièces» name the same piece; «Aucune action
  ne vous est demandée pour l’instant.» when nothing is the reader's; the locked count sentence closes it, verbatim.
- **One partition, three groups** (D1): to act (an open piece the person answers for) · in hand (the rest that is
  not settled) · settled (valid) — the strip's runs and the collection's groups are the same sets, drawn by one
  function (`documents.presenters.register_groups`), the rule the dashboard's ledger already follows. The words are
  the catalogue's — «À faire», «En cours», «Valide» — until B1 signs «À vous · En cours · Réglées» (D3, plan §1.18
  D15); the glosses are not drawn.
- **The row is the link** (D2 taken: no row menu): six zones on a subgrid and the note as the row's footer; the title's
  link stretched over the row, above the chip, the actor, the date and the note and under the act — 0 dead probe
  points of 42 (gate 0: 14 of 30); no «Consulter»; an act only on an OPEN piece the reader may file («Déposer la
  pièce», «Remplacer la pièce»), described by the piece's title (W-3). A filed piece, one in review and a valid one
  offer nothing on the row: a replacement is rare and waits on the piece's page — the settled row is the quiet one
  (the research's F9).
- **The Conditions gate promises no act its target cannot do** (W3-B's review, M1, carried over to W3-C): V4's row
  offered «Accepter les Conditions», which opens the Conditions' page — «Page en cours de préparation», nothing to
  accept: the acceptance flow waits on the legal texts (G1; `documents/terms_required.html`). The rows the gate blocks
  say «Bloqué» beside the chip and offer no act; the strip's primary leads to the piece's page («Consulter») and says
  why under the date, with the cause's `lock` — «Acceptation des Conditions d’utilisation requise.», the register row's
  own words —, as the review asks of the dashboard's NowPanel. When the acceptance flow exists, the act returns to the
  row with its real target.
- **The filter** is the key to the marks, in `STATE_ORDER`; a state with no piece is a word, not a link («Autres
  états» would be new copy: not drawn). Below 52rem of register: one 44 px control and a bottom sheet — K5, the
  documents lane's phone (RS §3) —, a native `popover` until the overlay system lands (W2-A), «Fermer» always present.
- **The search** is drawn in the card layout from thirteen pieces on (D9). **The layout follows the register's own
  width** — six columns from 66rem, five with the actor under the title from 52rem, cards below — by a container
  query, as the gate asks; DOCUMENT_WORKSPACE §16.6's cost (more layout work at CPU × 4) is in DL54-113's smoke.
- **Variant B is not built** (D13). The files below stay a real table, named for what it is.

**Measured** (lane 8789, the QA personas, fr / ar): the first card's title at 650 px at 390 × 844 and at 360 × 800
(gate: ≤ 700; the first piece above the bottom bar at both); 0 dead probe points at 1440, 1280, 1100, 390, 360 in fr
and ar; six columns at 1440, five at 1280 and 1100, cards at 768, 390, 360; the strip's primary and the rows' acts end
on one x (1 339 px at 1440; mirrored in Arabic); corners 4 · 8 · full; one shadow value at rest; no animation at load;
no horizontal overflow from 320 to 1440; 0 console errors, 0 CSP reports.

**Source.** Plan §3.5 item 5, §1.2, §1.15; the platform map §3, §5; DOCUMENT_WORKSPACE §0, §6–§14, §17 (D1, D2, D7,
D9, D13); RESEARCH_SYNTHESIS_V52 §3 K5; DL54-78 … DL54-80; `QA/v54/w3-c/NOTES.md`; `tests/frontend/test_documents_w3_c.py`,
`tests/frontend/test_documents_browser_w3_c.py`.

## DL54-111 · 11 October 2026 · W3-C: F8 and F13 — the ladder stops once a piece is filed; lateness speaks azione

**Decision.**
- **F8** (`documents.presenters.present_requirement`): a row's `urgency` runs only while its piece is OPEN (missing,
  to replace, expired, not valid). Once it is filed, in review or valid, the date is drawn calm — the calendar, the
  second ink, no word: the clock is no longer the person's. On the QA data a valid passport due in 18 days lost its
  «upcoming» mark.
- **F13** (`portal.services.present_deadline`): «En retard» goes out as `overdue` — azione: terracotta, a disc with
  clock hands — and «Bientôt» as `soon` — attesa: amber, a dashed ring. Before, `error` and `warning` drew lateness in
  a refusal's garnet, struck. `core.chips.KIND_REGISTER` already held both kinds (W1-C). The bridge's deadlines card
  mapped `error` to `overdue` itself (W3-B, DL54-84): the mapping is now a no-op, harmless.

Presenter changes only: no rule, state, permission or word changes.

**Source.** Plan §1.2 «Deadlines» («Soon = attesa; overdue = azione. Red never means lateness»); the platform map's
F13 and §6 item 0; DOCUMENT_WORKSPACE §3 F8, §9.1 item 2; the tests «a filed piece due tomorrow reads calm», «the
deadlines page draws lateness in azione».

## DL54-112 · 11 October 2026 · W3-C: page partials imported by the page sheet; the piece in the order of need

**Decision.**
- **The three partials of the document workspace** — `apps/portal/static/portal/v5/_workspace.css`, `_table.css`,
  `_depot.css` — are imported by the documents page sheet (`apps/documents/static/documents/documents.css`, loaded by
  the five documents pages), written in the collected tree (`../portal/v5/_x.css`, DS 2026 §2), never by `main.css`
  nor by the console entry every console page loads: the register is drawn by two pages. W1-A's guard
  (`tests/frontend/test_v5_tokens.py::test_the_console_partials_close_the_console_entry`) learns the rule: every console
  partial has ONE importer — the console entry, or the page sheet of the pages that draw it.
- **The piece's page** (`templates/documents/requirement_detail.html`) follows the order of need (DOCUMENT_WORKSPACE §12
  item 2; W-6: V4 put the act last): the state with its rule and this piece's reason; the deposit while the piece is
  open (`templates/documents/partials/depot.html`, after the deposits once it is filed, in review or valid); what is
  asked; the source; the deposits, each «Télécharger» described by its version. Its head names the file by its
  reference (ILE Mono): V4's case band (`portal/partials/case_header.html`) is not drawn on this page — on a phone it
  took 200 px before the piece's state. The deposit's eleven answers composed in place (the Dépôt module, the JSON
  answers of `views.py`) are the family's second step, with the preview drawer on the overlay system.

**Source.** Plan §2.3 («Page-only CSS — never in main.css»; «Console-only CSS»), §3.5 item 5; DS 2026 §2;
DOCUMENT_WORKSPACE §11, §12.

## DL54-113 · 11 October 2026 · W3-C: paths outside the slice, the legacy rules deleted, the CSS weight

**Paths outside the family's slice** (`scripts/check_ownership.py w3-c`), each for one reason, for the merge step to
record:

| Path | Owner | What, and why |
|---|---|---|
| `templates/documents/partials/depot.html` | none (new) | the piece's deposit, included twice by `requirement_detail.html` (open: under the state; settled: after the deposits) — one markup, drawn once |
| `apps/documents/tests/test_requirement_views.py` | none | two V4 pins retargeted, intent kept: the register is a collection of rows and the row is the link (it pinned `doc-collection panel panel--l1`); one blocked ROW, counted on the rows — the strip's primary names the same piece |
| `tests/frontend/test_v5_tokens.py` | W1-A | the console partials' guard: one importer each — the console entry, or the page sheet of the pages that draw it (DL54-112) |
| `templates/dev/showcase.html` | W1-C / W1-P (the dev page) | loads the documents page sheet: its state filter and document row samples are drawn by the partials that left main.css; the row sample drops V4's panel classes |
| `static/js/src/console.js` | W3-A (the slice «the preview drawer and the filter sheet» is W3-C's) | the register's search hides a group whose rows it hides (four lines inside the search block; W2-A's rewrite of the file touches neither them nor their neighbours) |

**Inside shared files, beyond the slice's words:** `static/css/v4/workspace.css` — the deletion map's rows
(SegmentedControl, search, DocumentCollection / Row / Card) with the row menu, their forced-colour and touch lines and
the files table's rules of the portal page (`.files__*`, `.table__link`: their only consumer was «Mes pièces»); the
sheet's header. `register.css`'s register and entry stay: academy, cases, companies, forum, glossary, helpdesk, the home
and selection still draw them — the documents pages no longer do (§2.1: the last named consumer deletes). Panel and
HealthStrip are no longer drawn by «Mes pièces»; the workspace head (`ws-head`) still is, as on the dashboard.

**The weight** (gzip −9, Python's `gzip.compress(…, 9)`, DL54-73): `dist/main.css` 41 802 → 40 470 B (−1 332, every
page of the site); `dist/portal/console.css` and `dist/portal/portal.css` unchanged. **The console page types' three
sheets 50 768 → 49 436 B — 571 B under the ceiling of DL54-73 (50 007 B)**, where W3-B left them 761 B over. The
documents pages' own sheet 1 172 → 4 623 B (+3 451: the register, the files table, the piece — the three page partials
in the one bundle the five documents pages share, cached across them); the documents page type in all 51 940 →
54 059 B (+2 119), 2 880 B over «the three sheets plus the page's own as it weighed at the w3-a merge». The bust rule's
two remedies are taken — the superseded legacy rules deleted from main.css, the rules kept out of every other page as
page partials —; under V5.5 («fix only real regressions») the lane's smoke (the notes: LCP, CLS, long tasks at CPU × 1
and × 4) is the evidence, and the merge step records the documents page type's ceiling as measured.

**Source.** Plan §2.1, §2.2, §2.3 (the deletion map), §2.6; DL54-15; DL54-73 item 3; DL54-85; `OWNERSHIP_V54.json`;
`QA/v54/w3-c/NOTES.md`.

## DL54-114 · 11 October 2026 · W3-C, step 2: the Dépôt — the eleven answers composed in place, on a JSON road that changes no rule

**Decision.**
- **One markup, two roads** (`templates/documents/partials/depot.html`): a required piece's Dépôt (the piece's page,
  and the preview drawer's body) and the loose file's (`templates/documents/upload.html`). The layers of gate 0 are
  kept — the native field (without script it is the whole Dépôt), the zone that keeps the real input inside it, the
  client guards, a real `<progress>` — and «filed ≠ examined»: no verdict, no check; the success is the filed state's
  own mark (ring and dot), drawing itself on the person's act only.
- **The JSON road** (`apps/documents/views.py`, the slice «the Dépôt's JSON answers»; IP S7): the same form to the same
  endpoints with `X-ILE-Depot: 1`; each answer goes out as `{answer, message, …}` — `filed` (with its version),
  the chain's refusals on their field (`empty`, `too_large`, `extension`, `content_mismatch`, `image_invalid`,
  `pdf_active_content`, `required`; a date already past on `expires_on`), `infected`, `throttled` (with its title),
  `terms`, `refused` (a closed file). **Always a 200**: a refusal, the throttle and the gate are answers the Dépôt
  composes, not failures of the request — and Chrome writes every 4xx of an XHR into the console as an error (the gate
  counts console errors). The road without script is byte-for-byte the old one (redirect and message, the 429 page,
  the Conditions page at 403). The header changes the answer's FORM, never the answer: the validation chain, the size
  limit, the MIME and antivirus checks, the storage, the throttle and the permissions run the same lines; an intruder
  meets the same 404 and a third party's piece the same 403 before any answer is composed (tests).
- **Composed in place** (`static/js/src/depot.js`, imported by `console.js` where a Dépôt is drawn): a refusal stays on
  the file's row (the double rule of «rifiuto», the server's sentence, the zone as the one way on); a date already past
  under its field (W1-C's error grammar); the throttle as a notice, the file kept, «Déposer» the retry; the gate in
  place of the form (the dashed frame of `terms_required.html`); a filing — and an antivirus refusal, which records a
  version — as the piece read again, its answer under the new state, the focus on the state's heading. An answer that
  is not the Dépôt's (a login page, a refusal page) reloads the page: nothing is sent twice behind the person's back.
  The client guards read the server's own limits (`documents.presenters.deposit_rules` through the `documents_register`
  tag): the allow-list, the size, the project's clock.
- **Words**: none new. The server's sentences verbatim; the guards' sentences are the chain's (`REJECT_MESSAGES`); the
  blocks (the throttle's notice, the error's, the server's, the gate, the filed line) are `<template>`s of the markup.
  Where gate 0 had a word that is not live («Envoi interrompu», «Réessayer», «Choisir un autre fichier», «Relâchez pour
  déposer», «Vérification du fichier»), the Dépôt says nothing new: the zone is the way to another file, «Déposer» the
  retry, the L2 key the wait — the copy packet lists them.

**Source.** Plan §3.5 item 5 («the Dépôt's 11 answers composed»), §1.9 (L2, L3); IP S7; DOCUMENT_WORKSPACE §11
(11.1–11.3); CD §12; `tests/frontend/test_depot_w3_c.py`, `tests/frontend/test_depot_browser_w3_c.py`;
`QA/v54/w3-c/NOTES.md` (step 2).

## DL54-115 · 11 October 2026 · W3-C, step 2: F13 on every page that draws a deadline register; the register and the entry

**Decision.**
- **F13 beyond the deadlines page.** The case file's checklist (`.table__overdue`, `.table__row--overdue`), its date list
  (`.dates__row--soon`, `--overdue`) and its next step's edge (`.ws-next--overdue`) — `static/css/v4/workspace.css` —
  and the console's next action (`.next-action--soon`, `--overdue`) and the portal tables' late rows (`tr.is-overdue`)
  — `apps/portal/static/portal/portal.css` — drew lateness with a refusal's garnet (`--err-700`, `--state-error-br`,
  `--line-grad-err`). They take the deadline tokens the register and the dashboard draw: «soon» attesa, «overdue»
  azione. A blocked step keeps its own edge. Colour only: no class, no markup, no word changes. The deadlines page's
  dates (`templates/portal/partials/deadline_item.html`) carry the glyph of their register on their own line — alarm-clock
  late, clock close by, the calendar otherwise (`portal.services.present_deadline` gives the row its `urgency`) — in the
  dashboard's grammar of a date (`.db-due`, `_dashboard.css`, already on every console page): no new shared CSS.
- **The shared payload stays flat** (the owner's V5.8: the console page types' 50 927 B are a hard ceiling). Step 2's
  shared CSS, gzip −9: `dist/main.css` 40 470 → 40 472 B, `dist/portal/console.css` 7 012 B unchanged,
  `dist/portal/portal.css` 1 954 → 1 958 B — +6 B on the console page types, after step 1's −1 332 B. The Dépôt's rules
  live in the documents page sheet only (`dist/documents/documents.css` 4 672 → 5 547 B, the five documents pages).
- **The deletion map's row «register.css's register and entry»** (plan §2.3): every rule of the section is still drawn
  by eight page families (academy, cases, companies, forum governance, glossary, helpdesk, the home's pathways,
  selection) and stays; the current entry's rules (`.entry[aria-current]`, and their forced-colour twin) leave — no page
  marks an entry current since the documents register stopped drawing entries. The section's last consumers delete it
  (§2.1: the last named consumer deletes).
- **Paths outside the slice** (for the merge step): `static/css/v4/workspace.css` and `apps/portal/static/portal/portal.css`
  (the F13 rules above: W3-E's and the console's legacy rules; the task names F13 «on every page that shows them»),
  `templates/portal/partials/deadline_item.html` (W3-E's: the date's glyph and grammar, one line);
  `apps/documents/templatetags/documents_register.py` (the `deposit_rules` tag, five lines); `static/js/src/depot.js`
  (new, the Dépôt's module) and its import line in `static/js/src/console.js`; `docs/design/DESIGN_SYSTEM_2026.md`'s
  `form_field.html` consumer line (the upload page now draws it through the Dépôt).

**Source.** Plan §1.2 «Deadlines», §2.1, §2.3; the platform map F13, §6 item 0; `tests/frontend/test_depot_w3_c.py`
(`test_lateness_is_never_drawn_with_a_refusals_colour_on_the_legacy_sheets`,
`test_the_register_entry_keeps_only_what_a_page_still_draws`).

## DL54-116 · 12 October 2026 · W3-C, step 2: the preview drawer and the filter's sheet, on the overlay system

**Decision.**
- **The preview drawer** (`templates/documents/partials/piece_drawer.html`, `static/js/src/piece-drawer.js` imported by
  `console.js` where the register draws it): the overlay system's drawer (W2-A's contract, never a second mechanism),
  `data-overlay-modal="none"` — beside the list on desktop, no scrim, the page usable, another row swapping the content
  without replaying the slide; a modal sheet on a phone (`overlay.js`, ≤ 40rem: the scrim, `aria-modal`, the trap).
  Opened by a plain press on a row's title, a row's act or the strip's act (a modified press keeps the link's own way;
  without script the rows are links to the pieces' pages). **The head at 0 ms from the row** — the reference, the title
  in its own language, the row's line (chip · actor · date) written into slots as words and attributes, nothing inserted
  in the press's task —, the busy key after 400 ms; **the body is the piece's page itself** — its `<article>` fetched
  from the piece's URL, no second template — seated by L3 on a piece's first arrival (`loader.js` `seat`, imported on
  demand), swapped in place on a refresh; `[data-piece-head]` marks what the head already says, not drawn twice. While
  it is open beside the list the workspace makes room (`data-drawer-beside`, written by the module once the drawer's
  first frame is painted — the register's re-layout stays out of the press's frame —, never a document-wide `:has()`):
  the register lays itself out by the width it is left, as its container query was built for.
- **History** (plan §1.14): the first opening pushes the piece's URL (a reload lands on the full page); Back, Esc and
  «Fermer» close it and the register's URL comes back with its `?état=`; a swap replaces the entry (`replaceState`); a
  Forward onto a closed drawer's entry loads that piece's page. **Focus**: the title on opening (a non-modal drawer,
  CONTRACT §4), the row's title on closing; a swap from the list leaves the focus in the list; a row's act or the strip's
  act sends it to the Dépôt's field. «Télécharger» keeps the drawer open (`data-overlay-keep`: a download is not a page).
  **RTL** (O5): the drawer mirrors — it stands on the left in Arabic; the sheets do not.
- **The Dépôt inside the drawer** is the same module (DL54-114) with the drawer as the host of its live regions (an
  announcement is never outside a modal sheet) and the drawer's own refresh: after a filing the piece is read again in
  place AND the register behind it (`.doc-page` swapped: the strip, the row, the files; the search and the filter's
  sheet wired again), the drawer's head and opener moved to the fresh row.
- **The filter's sheet** (DOCUMENT_WORKSPACE §13): the card layout's one 44 px control is a link to the overlay system's
  bottom sheet (`components/sheet.html` — the scrim, the grip, «Fermer», Esc; the focus on the current entry and back on
  the control; without script it shows in place, `:target`). The entries are one partial
  (`templates/documents/partials/state_filter.html`) drawn twice — the in-flow track and the sheet's body. The native
  popover sheet, its motion and its forced-colour rule leave `_workspace.css`: the system draws them, once.
- **The page-only sheet** (W2-A's CONTRACT §1, the owner's V5.8 budget): the two register pages link
  `css/dist/core/overlay-panels.css` in their `extra_head` — the head / body anatomy of the drawer and the bottom sheet
  are page-only since W2-A's budget fix; nothing of it reaches `main.css`. W2-A's guard learns that a partial drawn inside
  pages (`templates/documents/partials/`) is linked when every template that includes it links the sheet — the link
  stays in the page's head, never in a fragment.
- **W2-A's row-menu pins**, retargeted with their intent kept (the register's overlay is the system's): W3-C removed the
  row menu in step 1 (DOCUMENT_WORKSPACE D2), so `test_overlays.py`'s, `test_overlays_console_w2_a.py`'s and
  `test_overlays_console_browser_w2_a.py`'s row-menu tests now hold the row opening its piece in the system's drawer.
- **Corners**: at rest 4 · 8 · full on every documents screen; an open drawer or sheet adds its own 12 (plan §1.3: an
  open overlay may add its one).

**Source.** Plan §1.14 («Preview drawer», «History», O5, O7), §1.15 item 3 (`?état=`), §3.5 item 5; W2-A's CONTRACT.md
§1–§6; DOCUMENT_WORKSPACE §12, §13; `tests/frontend/test_drawer_browser_w3_c.py`, `tests/frontend/test_documents_w3_c.py`,
`tests/frontend/test_documents_browser_w3_c.py`, `tests/frontend/test_overlays.py`; `QA/v54/w3-c/NOTES.md` (step 2).

## DL54-117 · 12 October 2026 · W3-C, step 2: no state read through `:has()` — the drawer's open and close under 200 ms

**Decision.**
- **Measured** (the lane's dev server, headless Chromium, CPU × 4, a fresh context per load, Event Timing — INP's
  definition; n = 9 a cell): the drawer as the rehearsal left it opened at p90 232–296 ms and closed at p90 184–264 ms
  (O7: ≤ 200). The traces named two costs. (1) **A focus that entered or left a row's title re-styled the whole page**
  from `<body>` — ≈ 650 elements a time on «Mes pièces» at 390 (Blink's `:has()` invalidation,
  `allDescendantsMightBeInvalid`), and the open paid it twice (the tap's focus, then the drawer's); 276 for the Dépôt's
  field on a piece's page. The cause
  was W3-C's own `.doc-row:has(.doc-row__link:focus-visible)` and `.doc-depot__zone:has(> input:focus-visible)`: with
  them replaced, the same focus re-styles 4 elements. (2) **The register's re-layout** when the workspace made room.
- **So**: the keyboard's focus in a row and in the Dépôt's zone is read from the input's modality —
  `html[data-input="key"] .doc-row:focus-within`, `html[data-input="key"] [data-enhanced] .doc-depot__zone:focus-within`
  (head.js's flag, as W2-C1 did for the header) —, the zone's wait from `[data-sending]`, which `depot.js` writes with the
  controls' wait; the workspace makes room once the drawer's first frame is painted (`motion.js` `afterPaint`). A source
  guard keeps the three partials' `:has()` free of states. **After**, on the merged branch: open p90 96–136 ms, close
  p90 72–184 ms in the four cells (fr and ar, 1440 beside the list and 390 as a sheet); the filter's sheet open p90
  120 / 104 ms, close 80 / 64 ms (fr / ar).
- **The script rules the step had missed** (W1-D): `depot.js` imported `loader.js` statically and waited on a frame with
  a bare `requestAnimationFrame` — `test_loader_rules` and `test_script_motion_gate` failed. The loader is now asked for
  on demand (once a Dépôt is wired; its calls keep their order on one promise) and the live region's words follow its
  clearing by a timer; the drawer asks for the loader when a piece is opened and seats the fragment only once it is
  there (a fragment that arrives first simply stands: a seat begun after its rows were painted would hide them and
  raise them again).
- **Handed on, not W3-C's**: W1-C's `.form-field:has(… :focus-visible …)::after` and `.opt:has(input:focus-visible)`
  (`main.css`) re-style ≈ 800 elements when the Dépôt's date field takes the focus on a phone — the same remedy
  (`html[data-input="key"] .form-field:focus-within`) is W1-C's to make, every page at once.

**Source.** Plan §1.14 (O7, the INP rule), §1.5 (the one motion gate), §1.6; W2-A's NOTES «INP»; DL54-89
(`html:has(:focus-visible)` → `html[data-input="key"]`);
`tests/frontend/test_depot_w3_c.py::test_no_documents_sheet_reads_a_focus_or_a_state_through_has`,
`tests/frontend/test_depot_browser_w3_c.py::test_the_zone_takes_the_keyboards_ring_and_a_pointer_leaves_it_plain`;
the evidence `C:/tmp/ile_v5_council/evidence/v54/w3-c/s2/inp9-*.json`.

## DL54-118 · 12 October 2026 · W3-C, step 2: paths outside the slice; the CSS as measured

**Decision.**
- **Paths outside the slice**, each for the merge step to write into the manifest (DL54-113 and DL54-115 list
  the earlier ones): `static/js/src/piece-drawer.js` (new: the drawer's module, imported by `console.js` where the
  register draws the drawer — the slice names «the preview drawer and the filter sheet, on overlay.js»);
  `templates/documents/partials/piece_drawer.html` and `state_filter.html` (new partials of the register, beside
  `register.html`); `tests/frontend/test_overlays.py`, `test_overlays_console_w2_a.py`,
  `test_overlays_console_browser_w2_a.py` (W2-A's row-menu pins retargeted, intent kept; the page-only guard taught
  that a partial is linked through the pages that include it); `tests/frontend/test_state_chips_carry_a_register.py`
  (W1-C's two pins of the filter's legend follow it into `state_filter.html`); `static/js/src/depot.js` again (the
  loader on demand, the timer, `data-sending`).
- **The shared payload** (the owner's V5.8; gzip −9 as the stewards weigh it, bundles rebuilt from a clean dist):
  `dist/main.css` 42 152 → **40 876 B** (−1 276, every page type), `dist/portal/console.css` 6 809 B unchanged,
  `dist/portal/portal.css` 1 932 → 1 935 B — **the console page types 50 893 → 49 620 B, 1 307 B under the ceiling of
  50 927 B** (DL54-87 item 3); an interior page 42 152 → 40 876 B (ceiling 42 540). Nothing of the drawer, the sheet or
  the Dépôt reaches a shared bundle.
- **The documents pages' own sheets** (page-only, loaded by the five documents pages and the showcase):
  `dist/documents/documents.css` 1 172 → 5 418 B; the register pages also link W2-A's page-only
  `dist/core/overlay-panels.css` (2 071 B) for the drawer's and the sheet's anatomy.

**Source.** Plan §2.2 (the manifest; the serialized files), §2.3, §2.6; the owner's V5.8 (11 October 2026, 19:40) and the
orchestrator's reading; DL54-87 item 3; W2-A's CONTRACT §1, §7.

## DL54-119 · 12 October 2026 · W3-C, the fix pass: the person's place after a swap; the open piece marked; one clock decides one deadline; the review's minors

**Decision.**
- **After a swap the drawer's close keeps the person's place** (REVIEW M1, A11Y_PERF finding 1). Two causes, two
  remedies, both in `static/js/src/piece-drawer.js`: the register's history entry keeps no scroll of its own while the
  drawer owns the next one (`history.scrollRestoration = "manual"`, set before the first push — the drawer's entry
  inherits it — and given back once the traversal back to the register has landed, after its frame): the browser no
  longer restores the page to where it stood at the first opening. And the focus goes back to the title of the row of
  the piece SHOWN — `overlay:close`'s opener, which a swap moves — when it was inside the drawer (tracked by
  `focusin` / `focusout`; the native close's own focusout comes with the drawer shut) or nowhere, never for a link that
  leaves: the native `<dialog>`, shown once, hands the focus back to the element focused at its `show()` (the first row
  opened) before `overlay.js`'s `settle()` looks, and then finds it outside the panel. Measured on the lane: closed by
  «Fermer», Esc in the drawer, Esc in the list or Back, the page stays (1 028 → the same row at the same height, 561 once
  the table is back) and the focus is on the shown piece's row, in view, fr and ar, 1440 and 1100.
  **Carry-over to W2-A**: `settle()` should read whether the focus was inside the panel before `panel.close()`.
- **The register says which piece is open, and the press stays under the pointer** (REVIEW M2). The row of the piece
  shown holds `aria-current="true"` on its title and the selected state (`data-drawer-open`: the hover's surface and a
  2 px `--accent-mark` rule on the reading edge — the rule the portico's current link carries; an outline in Highlight
  under forced colours), moved on a swap, cleared on closing, written after the drawer's first frame like the
  re-layout. The re-layout keeps the element the person is on where it stood: the pressed row's title on opening, the
  focus (the shown piece's title) on closing — measured before the `data-drawer-beside` toggle, restored by an
  instant scroll after it. DL54-116's decision (cards beside the drawer) is kept.
- **The strip's act steps down while the drawer shows its piece** (REVIEW m2): the strip's next piece takes the open
  row's state and its act becomes a secondary (`data-drawer-stepped` restores it); the drawer's «Déposer» is the one
  primary in view.
- **One clock decides one deadline** (REVIEW M3): `DocumentRequirement.is_overdue` and `ChecklistItem.is_overdue` read
  `core.clock.today()` — as `due_urgency`, the deadlines page and the clock fix of 5 October do; T1 (`_open_obligations`)
  and the case's progress read those properties. Production has one clock either way; on a lane or the preview a
  piece due the day after the reference date is «Bientôt», never «En retard».
- **The minors** (REVIEW m1, m3–m7; A11Y_PERF findings 2–4): the caption ends at «… sur … validées»; below 40rem of
  their region the files are one item each (the name, then «type · taille · date» on one muted line, the act at the
  inline end) and no cell carries `data-label` any more, so portal.css's labelled pop-in never reaches them; a loose
  file's «Supprimer» opens the overlay system's alert dialog (the declarative opener — without script the form posts
  at once; `console.js` names the file and points the dialog's «Supprimer», `btn--danger`, at the row's form); the loose
  road's answer names the file and gives the zone back; the size shown never contradicts a refusal («0 ko», «10,1 Mo»);
  the strip's marks are drawn by the dashboard's ledger rules (V5.8 rule 3, the second family consolidates); the runs'
  ring is drawn inside the strip (`.reg a.reg-run:focus-visible`, above v4/workspace.css's 0-3-0 ring rule); «Télécharger»
  carries a 44 px band under a coarse pointer; a refused file marks its field (`aria-invalid`, the refusal's id in its
  description). The gate's inline link keeps WCAG 2.5.8's inline exception.
- **Paths outside the slice**, for the merge step to write into the manifest: `apps/documents/models.py` and
  `apps/cases/models.py` (M3: one line each, the project's clock); `templates/documents/partials/delete_confirm.html`
  (new: the alert dialog's body and foot, beside the register's partials). `static/js/src/piece-drawer.js`,
  `static/js/src/depot.js` and `templates/documents/partials/depot.html` are DL54-113's and DL54-118's.
- **The weight** (gzip −9): the shared bundles unchanged — `dist/main.css` 40 876, `dist/portal/console.css` 6 809,
  `dist/portal/portal.css` 1 935, the console page types **49 620 B**; the page-only `dist/documents/documents.css`
  5 418 → **5 497 B** (+79: the files' list, the selected state, the band, the loose answer's name, less the ledger
  marks' copy); JS `dist/piece-drawer.js` 2 358 → 3 044 B (under §2.6's 4 KB module row), `dist/console.js` 1 647 → 1 754 B,
  the Dépôt's chunk 3 577 → 3 702 B.

**Source.** `docs/design-v5/QA/v54/w3-c/REVIEW.md` (M1–M3, m1–m7), `A11Y_PERF.md` (findings 1–4); plan §1.14, §1.6,
§2.6; the owner's V5.8; DL54-116; the evidence `C:/tmp/ile_v5_council/evidence/v54/w3-c/fix/`; the tests named in
`docs/design-v5/QA/v54/w3-c/NOTES.md` «Review fixes».

## DL54-120 · 12 October 2026 · Steward, the w3-c merge: the family's ten entries renumbered, the 18 paths assigned and four slices named as written, the shared CSS gate passed with the shared payload 1 359 B lighter on every page, every ceiling lowered to the merged weight, the documents pages' two page types recorded through their own sheet

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w3-c` into design-v5 on 12 October 2026 —
what the family's own entries and notes hand to the merge step: DL54-113, DL54-115, DL54-118, DL54-119;
`QA/v54/w3-c/NOTES.md` «For the merge step» (steps 1 and 2 and the fix pass); `QA/v54/w3-c/REVIEW.md` «For the merge
step»).

1. **The numbering.** design-v5 stood at `e806483` (W3-F1's shipped note): W3-F2's, W2-C2's and W3-F1's entries and the
   records of their merges had taken DL54-96 … DL54-109 while the branch held DL54-96 … DL54-105, so the steward's sync
   (`351b078`) gave the family's ten entries **DL54-110 … DL54-119** (add 14; their headings, their index rows and their
   cross-references between the ten — every DL54-96 … DL54-105 in their text was the family's own; the code, the tests,
   DS 2026 and the manifest cite none of the moved numbers). Checked after the resolution: the log without the family's
   rows and block is design-v5's byte for byte, and the family's block with its numbers shifted back is the branch's.
   The notes' closing section says how to read the numbers written before (`3863fad`). This entry is DL54-120.
2. **Three conflicts, both areas' work kept.** The decision log (item 1). DS 2026 §2's inventory rows: design-v5's rows
   (W3-F2's `components.css` prose, W2-C2's `chrome.css`, the `v4/shell.css` and `v4/wizard.css` rows gone), then the
   `v4/workspace.css` row as the family wrote it — the one row of the table whose prose it changed, which design-v5 had
   not touched since the merge base —, then `scripts/regen_design_inventory.py --write` (`register.css` 21.6 KB,
   `v4/workspace.css` 33.6 KB; `ca6e0e7`). `static/css/dist` and `static/js/dist`: deleted and rebuilt (`npm run build`)
   on the merged sources — every CSS bundle byte for byte design-v5's but `main.css`, `portal/portal.css` and
   `documents/documents.css`; the JS design-v5's plus the family's scripts (`console.js`, `depot.js` with the Dépôt's
   chunk, `piece-drawer.js`), the shared chunks' import order following this worktree's chunk names. `register.css`
   (W3-F1's and the family's deletions in different hunks), the showcase and W2-A's two overlay test files merged on
   their own and were read. No semantic conflict surfaced in the targeted runs (item 8).
3. **The 18 paths outside the slice are this area's in the manifest** (`96e8b3d`). `scripts/check_ownership.py w3-c
   e806483` listed exactly the paths the family declares (step 1's four, step 2's eleven, the fix pass's three); each
   was read in the diff and found to be what it declares. Whole files: the register's and the piece's partials
   `templates/documents/partials/{depot,piece_drawer,state_filter,delete_confirm}.html` and the two modules
   `static/js/src/{depot,piece-drawer}.js`, imported on demand by `console.js` where a page draws them. Slices of files
   no family held: `documents_register.py` (`deposit_rules`: the Dépôt reads the server's own limits),
   `apps/documents/models.py` and `apps/cases/models.py` (`is_overdue` on `core.clock.today()`: one clock decides one
   deadline, REVIEW M3), `apps/documents/tests/test_requirement_views.py` (the V4 register's pins retargeted). Slices of
   files other families hold: `portal.css` (F13 on the deadline tokens, colour only), `deadline_item.html` (the date's
   glyph in the dashboard's grammar; W3-E keeps the partial), the showcase (the documents sheet's link) and five test
   files whose pins follow the register (no test removed). Four slices named as written: `console.js`,
   `v4/workspace.css`, `register.css`, DS 2026. The `views.py` slice (the Dépôt's JSON answers) and the `services.py`
   slice (the deadline kinds) were read: inside their words — the JSON road runs the same validation chain, size limit,
   MIME and antivirus checks, throttle and permission checks as the form's road and changes only the form of the answer.
   The check after it: 26 inside, 19 slice, 21 generated, and the manifest itself, the one steward-only path (before:
   18 outside); `--validate`: coherent, 25 families, 611 entries.
4. **The shared CSS gate (the owner's V5.8 and the orchestrator's definitive ruling of 12 October, 02:15) passes: the
   shared bundles fall.** On the bundles rebuilt from a clean `static/css/dist` and `static/js/dist`,
   `gzip.compress(data, 9)` (`evidence/v54/w3-c/merge/budget_gate_sync.log`, and `budget_gate_merged.log` on design-v5
   after the merge):

   | Page type | design-v5 `e806483` | merged | change | ceiling before → after |
   |---|---|---|---|---|
   | every page, and an interior page with no sheet of its own (`main.css`) | 38 683 | 37 324 | −1 359 | 38 683 → **37 324** |
   | console page types (`main` + `console` + `portal`) | 48 556 | 47 200 | −1 356 | 48 556 → **47 200** |
   | the company's dashboard (+ `companies.css`) | 49 429 | 48 073 | −1 356 | 49 429 → **48 073** |
   | the login (+ `entrance.css`) | 43 544 | 42 185 | −1 359 | 43 544 → **42 185** |
   | the home (+ `hero.css`, `pages.css`) | 52 621 | 51 262 | −1 359 | 52 621 → **51 262** |
   | a content page (+ `cms/lettura.css`) | 42 784 | 41 425 | −1 359 | 42 784 → **41 425** |
   | an account page (+ `cms/servizio.css`) | 41 109 | 39 750 | −1 359 | 41 109 → **39 750** |
   | an error page (+ `cms/errori.css`) | 42 312 | 40 953 | −1 359 | 42 312 → **40 953** |
   | the persons pages (+ `pathways/pathways.css`) | 42 177 | 40 818 | −1 359 | 42 177 → **40 818** |
   | the ecosystem doors (+ `ecosystem/ecosystem.css`) | 42 018 | 40 659 | −1 359 | 42 018 → **40 659** |
   | the Forum (+ `forum/forum.css`) | 42 177 | 40 818 | −1 359 | 42 177 → **40 818** |
   | the institutional pages (+ `pages/css/interior.css`) | 41 480 | 40 121 | −1 359 | 41 480 → **40 121** |
   | orientation (+ `orientation/wizard.css`) | 42 722 | 41 363 | −1 359 | 42 722 → **41 363** |
   | **the piece, the loose upload and the Conditions gate** (+ `documents/documents.css`) | 49 728 | 52 697 | +2 969 | 49 728 → **52 697** (item 6) |
   | **the two register pages** («Mes pièces», `/documents/`: + `documents.css` + `core/overlay-panels.css`) | 49 728 | 54 768 | +5 040 | — → **54 768** (recorded, item 6) |

   `dist/main.css` 38 683 → 37 324 B (−1 359 on every page): the family's deletions — the documents' V4 rules of
   `v4/workspace.css` (SegmentedControl, search, DocumentCollection / Row / Card with the row menu, their forced-colour
   and touch lines, the portal files table's rules) and the current entry's rules of `register.css` (DL54-113,
   DL54-115, DL54-118), each proved by grep at the family's steps; the documents pages draw their own from the page
   sheet. `dist/portal/portal.css` 1 932 → 1 935 B (+3: F13 — «overdue» and «blocked» no longer share one
   rule). `console.css` and every page sheet but `documents.css` byte for byte design-v5's. `dist/main.css` stands
   8 756 B under its 45 KB cap (46 080 B).
5. **Every ceiling is lowered to the weight measured at this merge** (the definitive ruling: «after a merge, the merged
   weight is the new ceiling»; DL54-102 item 5, DL54-109 item 5): every row of the table carries its new figure. A family
   that needs a shared rule pays for it with deletions.
6. **The documents pages' two page types are recorded as measured — through their own page-only sheet** (V5.8 rule 2,
   as DL54-109 item 6 did for orientation). `dist/documents/documents.css` 1 172 → 5 497 B: the three console partials
   of the family (`_workspace.css`, `_table.css`, `_depot.css`, imported by the documents pages' sheet only, never by
   `main.css` or the console entry) — what these pages draw: «il registro»'s strip and groups, the row as the link, the
   files' list, the preview drawer's register side, the piece and the Dépôt. After reuse — the strip's marks are the
   dashboard's ledger rules (REVIEW m7, V5.8 rule 3: the second family consolidates), the deadlines' dates the
   dashboard's `.db-due`, the drawer's and the sheet's anatomy W2-A's own page-only `core/overlay-panels.css`, linked by
   the two register pages only — and after deletion (`main.css` −1 359 B on every page above). The performance sanity
   check is the family's one accessibility + performance check on the lane's compressed twin (`A11Y_PERF.md`: LCP
   −112 … +28 ms against its merge base, the first-render task lower in every cell, CLS ≤ 0.0011, 188–384 ms earlier
   than V4; the drawer's cold open p90 112–120 ms) and the fix pass's INP smoke (open median 72–80 ms, close ≤ 128 ms
   at CPU × 4): no regression to fix under V5.5. **The piece, the loose upload and the Conditions gate** (`main` +
   `console` + `portal` + `documents`): **52 697 B**, +2 969 B on their own pages. **The two register pages** (+
   `overlay-panels.css`, 2 071 B): **54 768 B**, +5 040 B on their own pages. Both ratchet down from here; a family that
   adds to `documents.css` first deletes. No component family is drawn twice: the family's partials share with W3-F2's
   `_lettura.css` / `_servizio.css` and W2-C2's sheets only W1-C's components used in place (`.btn`, `.form-field`,
   `.notice`, `.icon`).
7. **The inventory and the capture report.** `scripts/regen_design_inventory.py` found two stale figures after the sync
   and wrote them (`ca6e0e7`); on design-v5 after the merge the script is run again (the merged tree is the branch's). The capture report is unchanged: `capture.py` captures the home, the privacy
   page, the login and the 404, none of which the family changes (its shared deletions are rules no page draws), as
   DL54-87 item 5 said for W3-B — not regenerated.
8. **The tests.** On the branch after the sync, the manifest, the figures and the notes (`3863fad`),
   `TEST_DATABASE_URL=…/test_ile_v5_l9`, one pytest and one browser at a time, every run behind the benchmark lock, no
   run crashed (`evidence/v54/w3-c/merge/tests_*.log`). **Non-browser** — `apps/documents`, `apps/portal`,
   `apps/cases`, `tests/test_phase_console.py`, `tests/security` (the object-permission and authorisation audits; the
   confidential-material sentinel test ran), `test_chips_registry`, `test_state_chips_carry_a_register`,
   `test_o14_lint`, W2-A's `test_overlays` and `test_overlays_console_w2_a`, `test_design_docs`, the two bundle-current
   tests, `test_static_pipeline` (a real `collectstatic` under the manifest storage), the family's `test_documents_w3_c`
   and `test_depot_w3_c`, and what the merge touched besides (`test_v5_tokens`, `test_dashboard_w3_b`, W3-A's
   `test_console_shell_w3_a` and `test_console_shell_stylesheets`, `test_loader_rules`, `test_css_tokens_exist`, the
   comments' leak test, `test_rtl_static`, the ownership and inventory scripts' tests): **1 817 passed, 3 skipped** (the
   intake suite's own: no legal rule in force), 0 failed (14 min 40 s). **Browser** (headless Chromium): the family's
   `test_documents_browser_w3_c`, `test_depot_browser_w3_c` and `test_drawer_browser_w3_c` with
   `apps/portal/tests/test_browser.py` — **63 passed** (3 min 15 s); W2-A's `test_overlays_browser_w2_a` and
   `test_overlays_console_browser_w2_a`, `tests/i18n/test_rtl_browser_overlays.py` and `tests/i18n/test_rtl_browser.py`
   — **67 passed** (6 min 16 s); 0 skipped, 0 failed. `ruff check .` (CI's lint step): all checks passed; `ruff format
   --check` on the area's changed files finds two deviations, both design-v5's own lines (W2-C2's in
   `test_overlays_console_w2_a.py`, an older one in `test_v5_tokens.py`), not changed; `makemigrations --check
   --dry-run`: no changes. The full suite is the integration checkpoint's (V5.5).
9. **Design-v5's own failures, unchanged by this merge.** `test_script_motion_gate.py::test_no_animate_or_frame_loop_outside_the_gate` fails on W2-A's
   `overlay/extras.js` (`requestAnimationFrame`), exactly as on design-v5 (DL54-102 item 10; for W2-A with W1-D's gate)
   — the family's two modules pass the gate. `test_chips_cards_w1_c.py::test_the_chip_is_drawn_by_one_sheet`, which
   DL54-102 item 10 also listed, passes on the merged tree (the rule it named moved into W3-F1's `_pagina.css` before
   this merge). Neither file is in the area's set; both were run for this record
   (`tests_design-v5_own_failures.log`: 1 failed, 22 passed).
10. **The worktree's `.env`** lacked `ILE_CONFIDENTIAL_SENTINELS` (every other value the lane's): the key was added from
   design-v5's before the tests, the lane's database URLs kept, so the confidential-material sentinel test ran instead of
   skipping. The file is ignored; nothing of it is committed.

**Why.** Entries renumbered after design-v5's keep the log's one order; paths nobody holds would have no writer for the
next family; the gate is read on the shared payload as V5.8 writes it, and the merged weight becomes every ceiling, so
that the next family meets the weight the product has; a surface's own CSS lives in its own sheet, loaded only where it
is drawn, and its page type is recorded at the weight it was measured at.

**Source.** The owner's V5.8 (`C:/tmp/ile_v5_council/directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`, and the
orchestrator's definitive ruling below it) and the V5_5 addenda of 11 October 19:40 and 12 October 01:30; plan §2.2
(the manifest; merge steps 1–5), §2.3, §2.6; DL54-87 item 5; DL54-102 items 4 and 5; DL54-109 items 4–6;
DL54-110 … DL54-119; `QA/v54/w3-c/NOTES.md` «For the merge step» and «Merge step — the steward's note on numbering»;
`QA/v54/w3-c/REVIEW.md` «For the merge step»; `QA/v54/w3-c/A11Y_PERF.md`; the weights in
`evidence/v54/w3-c/merge/budget_gate_sync.log`; the ownership checks in `evidence/v54/w3-c/merge/ownership_before.log`
and `ownership_after_wt.log`; the tests in `evidence/v54/w3-c/merge/tests_*.log`.

## DL54-121 · 12 October 2026 · Steward, the devops merge: production readiness (V5.9) on design-v5 — the family registered outside the waves, F-6 closed by W3-F2's error pages, nothing deployed

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-devops` into design-v5 on 12 October 2026 —
the owner's V5.9 (`C:/tmp/ile_v5_council/directives/V5_9_DELIVERY_AND_PRODUCTION_READINESS.md`) with V5.8's
LEGACY_REFERENCE_ONLY; what the lane hands to the merge: `QA/v54/devops/NOTES.md`, `REVIEW.md`, `VERIFY.md`).

1. **What merged: the repository made deployable, nothing deployed.** The DevOps readiness lane of V5.9 §3 («a small
   DevOps agent may prepare deployment readiness»): 18 commits `6484968` … `9f898e5` on design-v5 `1c03e3b` — the
   implementation, a verification walk and a senior review (both SHIP_AFTER_FIXES, no P0), a fix pass that closed
   every major and minor finding — and the merge step's eight commits. Thirty paths:
   - `docs/deployment/` (new): `PRODUCTION_DEPLOYMENT_RUNBOOK.md` — Ubuntu 24.04 LTS on DigitalOcean from a validated
     tag, steps 1–15 with exact commands (clone, tag checkout, virtual environment, `pip install -c
     requirements/constraints.txt`, the root-only environment file, PostgreSQL with the password off the command line,
     migrate → verify → rollback, `collectstatic`, public media and private documents, Gunicorn on a systemd socket,
     nginx and its catch-all server, permissions, journald logging, the seven timers and the nightly encrypted backup,
     restart, health checks), then static assets vs public media vs private documents, TLS, registrar transfer vs DNS
     cutover, the cutover sequence, legacy, release tags and the three states; `PRODUCTION_CHECKLIST.md` (§A the release
     gate of V5.9 §15 item by item with its evidence, and the go-live blockers; §B before deployment; §C the backup
     before the cutover, restored elsewhere; §D the smoke test); `ROLLBACK.md`; `production.env.example` (the server's
     environment file, placeholders only);
   - `.env.example`: every variable the application reads — settings, code, scripts, tests, compose files — grouped,
     one comment each, the optional ones commented out (under django-environ an empty value is a value:
     `PRIVATE_MEDIA_ROOT=` used to put identity documents in the root of the checkout);
   - `config/settings/prod.py` (V5.9 §6): `DATABASE_URL` and `IP_HASH_SALT` mandatory; `SECURE_HSTS_INCLUDE_SUBDOMAINS`
     and `SECURE_HSTS_PRELOAD` from the environment with no default; `ALLAUTH_TRUSTED_PROXY_COUNT` (allauth's rate
     limits behind nginx); `MEDIA_ROOT` outside the checkout; connection health checks; refused unless
     `ILE_ALLOW_INSECURE_PROD=1`: a wildcard host, a published or short salt, a mail backend that does not deliver, an
     unfilled `<...>` placeholder; refused even through the hatch: a `PRIVATE_MEDIA_ROOT` that overlaps a served
     directory. `base.py`: an empty `PRIVATE_MEDIA_ROOT` means the default. `DEBUG` off, `ALLOWED_HOSTS` and
     `CSRF_TRUSTED_ORIGINS` without a default, `SECURE_PROXY_SSL_HEADER`, the secure cookies, the structured logging and
     the error handlers were verified as they stood;
   - `apps/core/checks.py`: `core.E001` (`REDIS_URL` set although the Redis client library is not installed),
     `core.W001` (a proxy trusted by Django and not by allauth), `core.W002` / `core.W003` (the mail placeholders);
   - two code fixes the verification found: `companies_demo` refuses where demonstration data is not allowed, and
     `rules.legal_ruleset` completes an existing legal source only where a field is empty, so the `seed_all` of a
     release no longer reverts the legal referent's corrections;
   - `requirements/constraints.txt`, the server's pinned closure (19 distributions);
   - the tests: `tests/deployment/` (the runbook held to the code, the production checks, the private documents' one
     exit, the error pages through the real handlers, the pinned closure), the refusal and completeness tests
     extended, two app tests;
   - `docs/DEPLOYMENT.md` and `docs/DEPLOYMENT_READINESS.md` marked superseded (their history kept), `README.md`'s
     deployment pointers, and `docker-compose.staging.yml` passing the variables the production settings made
     mandatory.
2. **The hard limits, checked at the merge.** Nothing deployed; no production host contacted or resolved; no DNS,
   domain or certificate operation; no package installed. The family's diff (4 791 added lines) was scanned in Python:
   no IPv4 address but loopback, `0.0.0.0`, the documentation ranges and two public resolvers; no host or droplet
   name of the production server; the live site's domain only in the existing guard sentence («no @… address until it
   is activated», as `.env.example` and `base.py`'s `FORBIDDEN_EMAIL_DOMAIN` already say) — the new documents use
   `example.com` / `<your-domain>`; no credential (the two strength-check fixtures are synthetic, the key's form already
   at the base). No template, CSS or JS file: no bundle rebuilt, and V5.8's shared CSS gate is not concerned (the
   bundles are design-v5's byte for byte).
3. **The pre-merge sync, and what it changed on the branch.** design-v5 had moved from `1c03e3b` to `4ff9056` (W2-A,
   W3-F2, W2-C2, W3-F1, W3-C and the documentation commit `3780a7c`); the syncs (`e3291a8`, `79135eb`, `b8e3ccf`) met no
   conflict. Two consequences, resolved on the branch: (a) **F-6 is closed, by W3-F2** — W3-F2 draws the 400 and 500
   pages without the request (`core.views._self_sufficient`, `9af0e1a`), so the unknown Host's strict xfail turned
   XPASS(strict) and passed with `--runxfail`: the marker is gone, the test also checks that the page leaks nothing, and
   checklist A-21, the runbook's catch-all paragraph and its known limits say so (`08fa8f2`); the catch-all server
   stays. (b) The completeness rule (it reads the tests too) caught the V5 families' new test variables: `W3F2_SHOTS`,
   `ILE_OVERLAY_SMOKE_ENGINES` and `PLAYWRIGHT_BROWSERS_PATH` are documented in the NOT FOR PRODUCTION section of
   `.env.example`, and `LOCALAPPDATA`, Windows' own, joins the test's `SELF_SET` (`8c5542a`). The two later syncs
   (`79135eb`, W3-F1; `b8e3ccf`, W3-C, under the lock) needed nothing more. The lane's notes record both («At the
   merge», `a350423`).
4. **The family «devops» is in the manifest, outside the waves** (`69a2920`). A family plan §3 does not name: `wave` 0
   (as the steward's infrastructure), `steward` false, DL54-01's branch and worktree, no merge tag (V5.9's tags mark the
   whole product after final QA). Eighteen entries — whole: `docs/deployment/**`, `docs/design-v5/QA/v54/devops/**`,
   `tests/deployment/**`, `apps/core/checks.py`, `requirements/constraints.txt` and the two new app tests; slices:
   `.env.example` (all but w1-0's `ILE_QA_PASSWORD` placeholder), `prod.py` (V5.9 §6's changes), `base.py`
   (`PRIVATE_MEDIA_ROOT`), `apps/core/apps.py`, `companies_demo.py`, `apps/rules/seeds.py`,
   `docker-compose.staging.yml`, `README.md`, the banners of the two superseded documents, and the two extended tests
   (the completeness test: all but w1-0's guard). `scripts/check_ownership.py` accepts the id
   (`steward|devops|w<wave>-<name>`) and its tests admit the families outside the waves, two tests added (`db01929`).
   `check_ownership.py devops design-v5` before the steward's commits: 30 paths, 18 inside, 12 slice → PASS; each slice
   was read in the diff and stays inside it (one line of w1-0's guard reads the example through the module's helper: the
   same bytes). After them the steward's three paths join the list: the manifest (steward-only), the checker and its
   tests (the steward's whole files). `--validate`: coherent, 26 families, 629 entries.
5. **The tests**, `TEST_DATABASE_URL=…/ile_devops`, one pytest at a time, `-m "not browser"`, `-p no:randomly`. Before
   the sync, the family's exposed set (`tests/deployment`, the completeness test, the refusal test): 97 passed, 1
   xfailed (F-6). After the first sync and its two resolutions, the brief's list and the tests of everything the family
   changed — `tests/security`, `tests/test_env_example_is_complete.py`, `tests/compliance`,
   `tests/i18n/test_documentation.py`, `tests/frontend/test_design_docs.py`, `tests/frontend/test_static_pipeline.py`,
   `tests/deployment`, `tests/test_check_ownership.py`, `tests/test_migration_drift.py` (`makemigrations --check`, V5.9
   §7), `tests/test_demonstration_data_switch.py`, `apps/core`, `apps/companies`, `apps/rules`, `apps/documents`,
   `apps/cms/tests/test_media_assets.py`: **752 passed** in 6 min 31 s, no skip, no xfail; after the second sync and the
   steward's commits, 759 passed in 7 min 02 s. On the final branch (`b8e3ccf`, the third sync, under the lock), the
   same list: **759 passed in 7 min 01 s, no skip, no xfail**. `ruff check` and `ruff format --check` clean on the 19
   Python files the merge brings. The full suite stays the integration checkpoint's (V5.5) and CI's.
6. **Not done here, on purpose.** No tag (V5.9 §14: `v5-release-candidate`, then the release tag, on one validated
   commit after final QA); no restart of 8780; no change to v5-live; no push (the publication repository's next
   checkpoint carries it, after its scans); no line in `CHANGELOG_V54.md` or `live_status.json` (devops is not a
   preview surface — the static pipeline's merge, DL54-77, is the precedent). No CI change: installing CI's
   requirements with `-c requirements/constraints.txt` would make CI run the server's versions — the steward's
   `ci.yml`, left for its own change. Nothing deployed: the owner deploys and cuts over himself (V5.9 §17).
7. **The owner's open questions** (the lane's notes, «Open questions for the owner», re-read at the merge; the twelfth,
   F-6's template fix, is moot now that F-6 is closed):
   1. **F-5, the back-office sign-in path — a go-live blocker.** `/backoffice/login/` accepts the password alone for
      an account that has a TOTP device (Django's admin form has no MFA stage, and the middleware asks whether a device
      is enrolled, not whether this session used it). The runbook closes the path at nginx (a redirect to allauth's
      sign-in) as a mitigation; the fix belongs to the accounts lane. Who takes it, and is the recommended change
      (staff sign in through allauth; the middleware requires the session's second factor) acceptable?
   2. The release tag: `v2.0.0` (the version the platform already displays) or `v1.0.0` (the directive's example)? The
      candidate is `v5-release-candidate`, then `-2`, never a moved tag.
   3. The host names: the apex, `www` or both, and which is canonical; is a temporary validation host (a new
      subdomain pointed at the droplet) acceptable?
   4. HSTS: who inventories the domain's subdomains, and when may `includeSubDomains` be turned on? The preload list
      is a separate decision.
   5. The database: PostgreSQL 16 on the droplet (the runbook's default) or a DigitalOcean Managed PostgreSQL cluster
      in an EU region? Development and CI run 17.
   6. Python: run the suite once on 3.12 (Ubuntu 24.04's) before the release, or install 3.13 on the server?
   7. SMTP: the provider, the sender domain (SPF, DKIM), and whether outbound SMTP is open from the droplet (2525 is a
      common alternative).
   8. Redis: accept rate limits counted per Gunicorn worker (up to three times the configured figure), or add the
      Redis client library (a new dependency) and run Redis?
   9. Backups: the off-server EU location, who holds the encryption key, a retention aligned with the privacy terms,
      and DigitalOcean's droplet backups or snapshots?
   10. Access logs: the runbook masks the client address; is a raw-IP log with a short retention wanted for incident
       response?
   11. Health: an endpoint that also checks the private storage and the mail queue — wanted?
   13. Which server: the firewall and catch-all steps are for a fresh droplet; if the designated server already hosts
       other sites, who owns its nginx `default_server` and its firewall?
   14. EU hosting (CR-08): written confirmation of the region of the droplet, of the database and of the backups.

**Why.** A family no plan section names still needs one writer per path, or the next family to touch these files would
have none; the sync makes the merged branch the one that was tested; a defect another family's merge has closed is
closed in the documents too, or the runbook would send the owner after a fault that no longer exists; and V5.9 keeps
every step that touches a server, a domain, a certificate or a release tag for after final QA, and for the owner.

**Source.** The owner's V5.9 §3–§18 and V5.8; DL54-01 (the ref names); DL54-77 (a merge that is not a preview
surface); DL54 «How it is kept»; plan §2.2 (a file not in the manifest has no writer until the steward assigns it);
`QA/v54/devops/NOTES.md` (with «Review fixes» and «At the merge»), `REVIEW.md`, `VERIFY.md`; the ownership checks and
the test logs in `evidence/v54/devops/merge/`.

## DL54-122 · 11 October 2026 · W3-D: a threshold is a place — SELECTION on threshold A

**Decision.**
- **A file in `SELECTION` («Phase gérée par un acteur autorisé») stands ON threshold A, and on no step** (plan §1.18
  D16, OJ2). `portal.services.journey_for` mapped every status that is not a step to step 1: `seed-person`'s file read
  «Phase gérée par un acteur autorisé» in its header while its journey said «Vous êtes ici · 1» (W3-B's notes).
- **Each step now carries** its `status` (its glyph: `core.icons.JOURNEY`, through the registry), its `state` (done ·
  current · upcoming) and, on the step a threshold opens, that `threshold`: its key (`a` before the administrative
  procedure, `b` before the arrival), its caption (the site's own jurisdiction labels, `pages.services.
  JURISDICTION_SEGMENTS`'s catalogue entries — no new copy), its own state, and, when the file stands on it, the file's
  state in its own words. `is_current` and `frontier` keep their meaning for the callers that read them.
- **The case file dates the threshold** (`cases.presenters.journey_with_dates` follows the presenter's states): the
  steps before it carry their dates, the step after it none — even when the trail once reached it (the seed's trail
  went to the administrative procedure and came back).
- **SUSPENDED and CLOSED keep V4's first step.** Where a suspended file stopped, and the record a closed one became,
  are in the audit trail, not in the status; the dashboard never shows them (`active_case`), the case file does. Left
  for the family that reads the trail into the journey (the research's §7.3 contract).
- `journey_for` lives in `apps/portal/services.py`; the manifest's W3-D slice names `apps/cases/services.py` — the
  function was changed where it lives (DL54-126).

**Source.** Plan §3.5 item 6 («`SELECTION` on threshold A»), §1.18 D16; `JOURNEY_SIGNATURE.md` §5.7, §7.3;
`QA/v54/w3-b/NOTES.md` «Handed over»; `tests/frontend/test_journey_w3_d.py`.

## DL54-123 · 11 October 2026 · W3-D: one rail drawing for the console

**Decision.**
- **One sheet draws every journey of the console**: `apps/portal/static/portal/v5/_journey-rail.css`, imported by
  `console.css` after the dashboards — the dashboard's «Mon parcours» and the case file's journey
  (`components/journey_rail.html`), the case file's timeline (`case_timeline.html`), «Ma situation»'s Stepper
  (`wizard_stepper.html`). One vocabulary: behind the file a 10 px ink dot (never a check, O14), where it stands an
  18 px laguna ring on a flat wash — a disc, not a shadow —, ahead a 12 px open ring; the line 2 px, laguna where the
  file has been, the decorative hairline ahead; each item draws the stretch from its node to the next item's — no
  gradient, no measure, no script; the grid mirrors it in Arabic.
- **The level line from 56rem of the component's own width** (a container query; the research's 46rem). Measured on
  the lane: at 46rem the eight columns of a file on threshold A came to 88 px and «Accompagnement» (110 px) left its
  column; from 56rem a column is never under 108 px. Under 56rem — the phone, the tablet, a narrow column — **the
  card and its disclosure**: what is true now (the current item's glyph and words, «Étape n sur 7» on a step, «Vous
  êtes ici»), then the list behind the native `<details>` «Où j’en suis», closed, as a spine. At the wide width
  `::details-content` lays the closed list out and the card and the summary leave; without it, the card and its
  disclosure stay at every width — nothing is hidden. The case file draws the component `descriptive`: the spine at
  every width.
- **A threshold is a narrow column** (2rem; the whole column when the file stands on it) with its hairline across the
  line and its caption over the heads of the steps it opens; «Maroc» and «Italie» are the line's two ends; every head
  sits on the line's side of its row. «Vous êtes ici» has one place: the row that is the current item's alone.
- **One marker a column (D16):** the phase glyph; no numeral (the public passage's); the holder on a row of its own
  only when the presenter knows it — never today (A′, OJ1: the actors' mapping D9 is not signed). **No beads** (OJ3):
  on the dashboard the pieces are «il registro» (W3-B, DL54-80), drawn once.
- **Still at load.** No animation, no transition, no `will-change`: the drawing is its own still, the reduced-motion
  state and the no-JS state. «Le relais» (one light, once, from where the file was last seen) needs a stored
  last-seen position — a policy (class C, plan §7.2), not pursued in V5.4 — so the family ships **no
  `journey-rail.js`**: the rail is complete without a script (the plan's slice keeps the file's name for the day the
  relay is decided). W3-B's dashboard rule that stopped V4's line drawing itself left with V4's line.

**Why.** «One passage and one rail drawing, never a third» (the gate): three components drawing positions on a line
with three vocabularies would be three drawings. A container query decides by the space the rail really has (the
dashboard at 1024 with the compact rail, a tablet, a phone), never by the viewport.

**Source.** Plan §3.5 item 6, §1.18 D16, §1.5, §1.2 (O14), §7.2; `JOURNEY_SIGNATURE.md` §5.3, §5.5, §6.2, §7.1, §7.2;
DL54-80; the lane's measures (`QA/v54/w3-d/NOTES.md`); `tests/frontend/test_journey_w3_d.py`,
`tests/frontend/test_journey_browser_w3_d.py`.

## DL54-124 · 11 October 2026 · W3-D: one passage drawing for the public pages

**Decision.**
- **The public passage is «la linea»**: a real sequence on a level line, the numerals over open stations (an outline
  is open: nothing on this site settles a step for anyone), the words under them; down the reading edge on a phone,
  across from 48rem as many columns as stations. W3-F1 drew it first for the door pages and named it the passage's
  language; `static/css/v5/_journey-passage.css` (a page-only partial) is its home and `components/stepper.html` its
  component — with what a passage needs beyond W3-F1's drawing: a flow's place (`current`: the steps behind filled in
  ink, its own ring thicker in the primary, its rank in words) and the 16 px text below 64rem (RE-4).
- **On the home** the orientation's four neutral steps (gate G3 closed) are drawn by it; `pages.css` imports the
  partial (written in the collected tree); the home's `.sequence` rules and `register.css`'s shore crossing left with
  their last consumer; `components.css` §16 (the V1 stepper) left with `stepper.html`'s redraw.
- **The door pages wait for W3-F1's merge** (the plan's order: W3-F1 merges before W3-D). Then, in one step: the
  `.linea` rules of `static/css/v5/_interior.css` §5 leave for `_journey-passage.css`; each page sheet that draws «la
  linea» imports `../css/v5/_journey-passage.css` after `_interior.css`; `templates/pages/partials/_linea.html`
  includes `components/stepper.html` (or its callers call it); `components.css` §17 and `components/timeline.html`
  (then drawn by the showcase only) retire; `v5/_wizard.css`'s Stepper rules leave (the rail draws the Stepper).

**Source.** Plan §3.5 items 1 and 6, §1.18 D16, §2.3 («`_journey-passage.css` → the page sheets of the pages that draw
it»); W3-F1's `templates/pages/partials/_linea.html` comment and notes («W3-D may draw the public passage on these
pages: one import line in a page sheet»); DL54-41.

## DL54-125 · 11 October 2026 · W3-D: a date on the rail in the sans; «Ma situation» moves nothing at load

**Decision.**
- **A date on the rail is in tabular figures, in the sans** — the journey's and the timeline's: «ILE Mono» has one
  seat, the references (`v5/base.css`, plan §1.1). The research set them in the mono; the foundation binds.
- **«Ma situation» moves nothing at load.** The guided form's script gave the submit its secondary role after the
  first paint and its six colour transitions played at every visit; `static/js/src/situation.js` applies that role
  under `transition: none` in one style pass and restores the transition once the state has been painted (through
  motion.js's `afterPaint`, the one gate). The file was in no family's slice beyond W1-D's motion gate, «until W3-D's
  journey work takes the file» (W1-D's notes).

**Source.** Plan §1.1 («ILE Mono for references»), §1.5 («the console has no entrance and no stagger at load»);
`static/css/v5/base.css`; `QA/v54/w1-d/NOTES.md` (situation.js).

## DL54-126 · 11 October 2026 · W3-D: the paths outside the slice; the deletions; the CSS as measured

**Decision.**
1. **Paths outside the slice**, each justified, for the merge step to write into the manifest:
   `apps/portal/services.py` (`journey_for`, `JOURNEY_THRESHOLDS`, `_JOURNEY_POSITION`: where the function lives —
   the slice's `apps/cases/services.py` names the wrong file); `apps/cases/presenters.py` (`journey_with_dates`: in no
   slice); `apps/core/dev.py` (`_demo_journey`: the showcase's journey through the presenter, not a copy);
   `static/js/src/situation.js` (DL54-125); `templates/pages/home/_orientation.html` (the passage on the home, W2-D's
   chapter, through the serialized rule); `apps/pages/tests/test_home.py` (the two orientation tests follow the
   markup, their intent kept); `tests/frontend/test_design_showcase.py` (W1-A's: the showcase's marker for the stepper
   follows the passage's markup, `linea__step`). Inside shared files, beyond the slices' words: `v4/workspace.css` — the Timeline with
   the JourneyRail (the case file's timeline is W3-D's component); `pages.css` — the home's `.sequence` rules with the
   import line; `_dashboard.css` — W3-B's journey rule, removed as W3-B's notes asked; DS 2026 — §2's sentence on
   `v4/workspace.css`, §2.1's rows of `pages.css` and `console.css`, §11.7's journey row, §12's keyframe sentences.
2. **Deleted** (plan §2.3, W3-D's row): `components.css` §16 (19 → 18 sections); `v4/workspace.css`'s JourneyRail and
   Timeline with `rail-draw`, `rail-draw-y`, `tl-light`; `register.css`'s shore crossing; the home's orientation rules.
   Kept, because pages still draw them: `register.css`'s `.sequence` (W3-E's console pages) and `components.css` §17
   (W3-F1's pages until its merge).
3. **The CSS, gzip -9 of the committed bundles against design-v5** — see `QA/v54/w3-d/NOTES.md` «The weight».

**Source.** Plan §2.2, §2.3, §2.6 items 3 and 5; DL54-15; DL54-87; `scripts/check_ownership.py w3-d design-v5`.

## DL54-127 · 12 October 2026 · W3-D, the fix pass: the rail in a page-only sheet; «Mon parcours»; a file off the line

**Decision.**
1. **The rail is a page-only sheet** (the review's M1, the accessibility check's blocking finding; the owner's V5.8:
   the shared ceilings are hard). `apps/portal/static/portal/v5/_journey-rail.css` leaves `console.css` for
   `apps/portal/static/portal/journey.css` → `css/dist/portal/journey.css`, an import list like the console's entry,
   linked after the shell's two sheets (`{{ block.super }}` in `extra_head`: the cascade position the rail held as
   `console.css`'s last import) by the four pages that draw a journey — the dashboard and «Mon parcours» only when the
   person has a file, the case file, «Ma situation». gzip -9 of the committed bundles: **the console page types (main +
   console + portal) 51 530 → 49 614 B, 1 313 B under design-v5's 50 927** (DL54-87's ceiling); `main.css` 40 599 B
   (design-v5 41 880); the journey's pages add their 2 688 B sheet. Requests: one stylesheet more on the four journey
   pages only, inside W1-0's «before» counts.
2. **«Mon parcours» draws the journey** (M2): the rail's «Mon parcours» entry wears the journey's glyph, and the page
   now answers it — `components/journey_rail.html` at the page's head with `journey_for(active_case(user))` and the
   dashboard's label «Où j’en suis» (no new copy), the pre-assessments under it; no file, no journey and no sheet.
   `portal.services.pathways_page` gives `journey`; `templates/portal/pathways.html` (W3-E's slice) is a path outside
   the slice, justified below.
3. **A status with no place on the line has no current item** (M3; DL54-122's «V4's first step» superseded). SUSPENDED
   and CLOSED: `journey_for` marks nothing current and nothing says «Vous êtes ici» — the header's chip says the state;
   the card's «Vous êtes ici» belongs to the current item's branch, so a list with none says it nowhere. The case file
   reads the trail (`cases.presenters.journey_with_dates`): the last place the file held on the line, from its
   transitions in order, puts every step up to there behind it, dated where the trail knows the date, the item there
   marked `stop` (`journey__step--stop` / `journey__threshold--stop`: the line is not travelled past it). The held node
   of a suspended file waits for the trail contract (JS §7.3). `portal.services.journey_place` names a status's place.
4. **The polish** — the timeline newest first, its first row lit, an assignment's actor not repeated when it is the
   role its detail says (m1; `tl__row--last` → `tl__row--latest`); on a threshold the phone card is headed by the
   threshold's caption (m5); the level line's last stretch runs from step 7 to the rail's end under «Italie», as the
   spine carries it (m3); the closed `<details>` revealed at the wide width by both `content-visibility` and `display`
   on `::details-content` (m6 — Safari and Firefox not installed here: to check before the owner's report); the
   journey's lines take no pointer (`pointer-events: none`: a tap on the Stepper's line selects its question).
5. **Not in this pass**: the consolidation with W3-F1 (M4 — `v54/w3-f1` is not on design-v5; the five steps stay
   written in `QA/v54/w3-d/NOTES.md` «For W3-F1»); «Ma situation»'s counter (m4 — W3-E's view and template); the
   inspector's focusable scroller (W3-E), the forced-colours current entry and `html:has(.console-drawer[open])` (W3-A /
   W4-B) — handed over.
6. **Paths outside the slice** (for the merge step to write into the manifest, with DL54-126's seven):
   `apps/portal/static/portal/journey.css` (the journey's page-only entry: the slice names the partial, not an entry —
   V5.8 asks for one); `templates/portal/dashboard.html` (W3-B's: the sheet's link, one line), `templates/cases/detail.html`
   and `templates/portal/situation.html` (W3-E's: the sheet's link, one line each), `templates/portal/pathways.html`
   (W3-E's: the link and the journey at the head — M2); `apps/portal/services.py` gains `pathways_page`'s `journey` (one
   key) beside `journey_for`; `static/css/dist/portal/journey.css` is generated.

**Source.** `QA/v54/w3-d/REVIEW.md` M1–M4, m1–m6; `QA/v54/w3-d/A11Y_PERF.md` findings 1–3 and «Seen on the way»;
`QA/v54/w3-d/NOTES.md` «Review fixes»; the owner's V5.8 (11 October 2026); DL54-87; DL54-122; `tests/frontend/
test_journey_w3_d.py`, `tests/frontend/test_journey_browser_w3_d.py`.

## DL54-128 · 12 October 2026 · W3-D, the integration pass: one passage drawing; «Ma situation»'s one page-only sheet; each journey page loads only what it draws

**Decision.**
1. **The sync.** `v54/w3-f1` appeared on design-v5 at 07:01 (`a2644b0`, the W3-F1 steward's merge); this branch merged
   design-v5 there (174 commits). Both areas' work kept: `pages.css`'s header, DS 2026 (§2's rows design-v5's,
   regenerated; §2.1's `pages.css` and `console.css` rows; §10's `wizard_stepper.html` the rail's), the decision log
   (design-v5's numbering), the bundles rebuilt from a clean dist. design-v5 then moved — W3-C's merge (DL54-110 …
   DL54-120, «Mes pièces» as DS 2026 §11.8) and its shipped note, `4ff9056` — and this branch merged it again: the
   union of the two families' deletions in `v4/workspace.css`, the journey's DS section §11.9. Then the devops merge
   (`1a61a7c`, recorded as DL54-121; design-v5 `3d5351b`: production readiness — documents, settings and tests, no
   stylesheet, template or script), merged a third time (15 October). This family's seven entries follow design-v5's
   last: DL54-88 … DL54-93 of the first step and the fix pass are DL54-122 … DL54-127 and this entry DL54-128, their
   cross-references with them.
2. **One passage drawing** (the review's M4; the definitive ruling's rule 3: the family that merges second
   consolidates). W3-F1's «la linea» (`static/css/v5/_interior.css` §5, its Arabic line, its forced colours) folds into
   `static/css/v5/_journey-passage.css`, which drew the same grammar: the door pages, the advice pages, the
   questionnaire and the home draw from one partial; their page sheets (`pathways.css`, `ecosystem.css`,
   `orientation/wizard.css`) import it after `_interior.css`; `templates/pages/partials/_linea.html` includes
   `components/stepper.html` (W3-F1's callers and contract kept, `current=None`: an explanation is never a progress);
   a page's modifiers stay in its own partial (`_pathways.css`, `_spaces.css`, `orientation/wizard.css`) and qualify
   the drawing without redrawing it. Where the two hands differed, the door pages are kept as W3-F1 drew them: W3-F1's
   Arabic rule for a French station is homed; the passage's «16 px below 64rem» line (RE-4), never exercised on the
   home (whose stations carry no text), is dropped so the stations' text stays 15 px as on the door pages. The ring is
   open to its ground (no paper fill): on the home it sits on the BRAND gradient. Measured on the lane (156 captures,
   fr / ar, 1440 / 390, normal and forced colours): the home, the Forum, the institutional pages and every console page
   identical; the door pages identical but for their rings' rim antialias (40–124 pixels a page, ≤ 4/255 a channel).
3. **Retired, with their proof** (a grep of every template, Python, JS and JSON file of design-v5 at `a2644b0`, of
   this tree, and of the files each in-flight worktree changed — `v54-w3-c` and its trial, `v54-devops`; `v54-w3-e`
   absent): `components.css` §17 and `components/timeline.html` (their last caller the design showcase's demo, with
   `DEMO_TIMELINE`); the Stepper's rules of `apps/portal/static/portal/v5/_wizard.css` (§2, the phone row, the
   forced-colours line: the rail draws it; its count stays the form's); DS 2026 §10.1's «Avanzamento» row
   (`progress.progress`, gone with §16). Proved again after the third sync (design-v5 at `3d5351b`; in flight
   `v54-w3-e`, `v54-intfix`, `v54-sec-f5`): no new user.
4. **The shared payload paid for** (rules 1 and 2). «Ma situation»'s guided form (`v5/_wizard.css`) is that page's
   alone: it leaves `console.css` (on every console page since W3-F1's merge) for a page-only sheet,
   `apps/portal/static/portal/situation.css`, which only `templates/portal/situation.html` links, after the shell's
   two sheets — the place in the cascade it held. And each journey page loads only what it draws: the console's one
   rail drawing is a vocabulary and two components — `v5/_journey-nodes.css` (one line, three nodes, written once),
   `v5/_journey-rail.css` (the journey and the timeline) and `v5/_journey-stepper.css` (the Stepper); `portal/journey.css`
   = nodes + rail (the dashboard, «Mon parcours», the case file), `portal/situation.css` = the form + nodes + Stepper.
   Each forced-colour rule keeps its selector's specificity; the console pages measured identical, normal and forced.
   gzip -9 against design-v5 at `a2644b0`: `main.css` 38 683 → 37 030 B (every page); **the console page types (main +
   console + portal) 48 556 → 45 740 B**; the journey pages 48 161 B (their sheet 2 421 B), «Ma situation» 47 942 B
   (its sheet 2 202 B), every other page type lighter (−1 230 … −2 816 B). After the second sync, against design-v5
   at `4ff9056`: `main.css` 37 324 → 35 483 B; **the console page types 47 200 → 44 196 B**; the journey pages
   46 617 B, «Ma situation» 46 398 B, «Mes pièces» 52 697 → 49 693 B, every page type lighter (−583 … −3 004 B);
   the same figures after the third sync, against design-v5 at `3d5351b`, on bundles rebuilt from a clean dist. No
   page type grows: rule 2's performance check is not triggered. Requests: four stylesheets on the journey pages and
   on «Ma situation» (the shell's three and the page's one), three on every other console page — as before this pass
   for the journey pages, one fewer for «Ma situation» than its two page sheets would have made.
5. **`tests/frontend/test_design_docs.py`'s token check** reads, for a partial, the custom properties of the partials
   its entry imports before it (sibling imports only): the rail and the Stepper compose the vocabulary of
   `_journey-nodes.css`, as the build composes them.
6. **Paths outside the slice** (for the merge step, with DL54-126's and DL54-127's): `static/css/v5/_interior.css`,
   `apps/portal/static/portal/v5/_wizard.css`, `templates/pages/partials/_linea.html`,
   `templates/ecosystem/partials/pilot_flow.html` (one comment), `templates/components/timeline.html` (deleted),
   `templates/dev/showcase.html`, `apps/core/dev.py`, `apps/portal/static/portal/console.css` (W3-F1's import line
   out), `apps/portal/static/portal/situation.css` (new), `templates/portal/situation.html` (W3-E's: its one sheet),
   `apps/portal/static/portal/v5/_journey-nodes.css` and `_journey-stepper.css` (new, W3-D's — the slice names
   `_journey-rail.css`), `tests/frontend/test_interior_w3_f1.py`, `tests/frontend/test_orientation_w3_f1.py`,
   `apps/ecosystem/tests/test_compliance.py`, `tests/frontend/test_design_docs.py`, `tests/frontend/test_design_showcase.py`;
   generated: `static/css/dist/portal/situation.css`.
7. **The design showcase draws the journey again** (found by the resumed verification, 15 October): it links
   `portal/journey.css`, `portal/situation.css` and, for the passage, `pages/css/pages.css` (a partial is never an
   output of its own; the home's sheet is the passage's one importer without a page grammar — its home rules find no
   element there), as W2-A and W3-C link their page sheets; since the journey's CSS left `main.css` and `console.css`
   its demos were bare (and, with the journey's sheet alone, its Stepper half drawn by the vocabulary). In the
   product «Ma situation»'s sheet stays linked by that page alone (`templates/dev/` is never served without DEBUG;
   the journey test says so of the product's templates). Development only; no page type's weight moves.

**Source.** `QA/v54/w3-d/REVIEW.md` M4; `QA/v54/w3-d/NOTES.md` «For W3-F1» and «Integration pass»; the orchestrator's
definitive CSS ruling (`directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`, last section); DL54-87; DL54-109;
`tests/frontend/test_journey_w3_d.py`.

## DL54-129 · 15 October 2026 · Steward, the w3-d merge: the family's seven entries kept as numbered, the 19 paths assigned and seven slices named as written, the shared CSS gate passed with `main.css` 1 841 B lighter on every page and the console page types 3 004 B lighter, every ceiling lowered to the merged weight, the journey's two page types recorded through their own sheet

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w3-d` into design-v5 on 15 October 2026 —
what the family's entries and notes hand to the merge step: DL54-126 item 1, DL54-127 item 6, DL54-128 item 6;
`QA/v54/w3-d/NOTES.md` «Paths outside the slice», «Integration pass — resumed» (the decision-log numbers, the weights,
the tests) and «Handed to»; `QA/v54/w3-d/REVIEW.md` and `A11Y_PERF.md`, both SHIP_AFTER_FIXES, and `P0_RECHECK.md`,
SHIP).

1. **The order and the numbering.** The plan's order (§3.5 item 6: W3-D merges after W3-F1) was met: `v54/w3-f1` has
   stood on design-v5 since 12 October. The steward took `DESIGN_V5_MERGE_LOCK` at 21:14:58 with design-v5 at
   `3d5351b` (DL54-121, the devops record) — the branch's merge base: the family's third sync (`9237de4`, 15 October)
   had merged it and numbered the family's seven entries **DL54-122 … DL54-128** after it, so `git merge design-v5` in
   the branch said «Already up to date» and nothing was renumbered. Checked: the family's change to the log is
   additive only (seven rows, seven entries, no line of design-v5's removed). This entry is DL54-129 (W3-E's branch
   numbers its own from DL54-130).
2. **No conflict.** The branch contained design-v5's head, so the merge into design-v5 (`--no-ff`) wrote no conflict.
   `static/css/dist` and `static/js/dist` were deleted and rebuilt (`npm run build`) in the branch: byte for byte the
   committed bundles. On design-v5 after the merge (`e35714c`, whose tree is the branch's: `git diff v54-w3-d e35714c`
   is empty) the same rebuild (`cec9425`): the CSS byte for byte the branch's; the JS byte for byte design-v5's before
   the merge but `situation.js`, the family's one script change — the branch's shared chunks and the entries that import
   them differed only by their names, which follow the worktree's path.
3. **The 19 paths outside the slice are this area's in the manifest** (`9b1fc84`). `scripts/check_ownership.py w3-d
   design-v5` listed exactly the paths the family declares (DL54-126's seven, DL54-127's four, DL54-128's eight); each
   was read in the diff and found to be what it declares. One whole file: `templates/components/timeline.html`
   (retired with `components.css` §17, its last caller the showcase's demo). Eighteen slices: `apps/portal/services.py`
   (the journey's presenter and `pathways_page`'s `journey` — the plan's slice names `apps/cases/services.py`, where
   nothing changed, and its entry says so), `apps/cases/presenters.py` (`journey_with_dates`, `timeline`; no family
   held it), `apps/core/dev.py` (the showcase's journey through the presenter), `static/js/src/situation.js` (still
   at load), `templates/pages/home/_orientation.html` (the passage), the journey sheets' links in
   `templates/cases/detail.html`, `templates/portal/dashboard.html`, `templates/portal/pathways.html` (with the journey
   at its head) and «Ma situation»'s sheet in `templates/portal/situation.html`, the consolidation's
   `static/css/v5/_interior.css` (§5 out), `templates/pages/partials/_linea.html` (an include of the one component),
   `templates/ecosystem/partials/pilot_flow.html` (a comment), `templates/dev/showcase.html` (the links; the timeline's
   demo out), and five test files whose pins follow (`apps/pages/tests/test_home.py`,
   `tests/frontend/test_design_showcase.py`, W3-F1's `test_interior_w3_f1.py`, `test_orientation_w3_f1.py` and
   `apps/ecosystem/tests/test_compliance.py` — no test removed). Whole files beside them: the family's four new sheets
   (`portal/journey.css`, `portal/situation.css`, `v5/_journey-nodes.css`, `v5/_journey-stepper.css`), which the
   import-line slice's glob had matched. Seven slices named as written: the page sheets' import lines (with `pages.css`'s
   V4 sequence rules, `_dashboard.css`'s one journey rule and `_wizard.css`'s Stepper rules), `console.css`,
   `components.css` §16–§17, `v4/workspace.css`, `register.css`, `test_design_docs.py`'s composition helpers, DS 2026;
   a note on `apps/cases/services.py`. The check after it: 17 inside, 31 slice, 29 generated, and the manifest itself,
   the one steward-only path (before: 19 outside); `--validate`: coherent, 26 families, 651 entries.
4. **The shared CSS gate (the owner's V5.8 and the orchestrator's definitive ruling of 12 October, 02:15) passes: both
   shared bundles fall and no page type grows.** On the bundles rebuilt from a clean `static/css/dist` and
   `static/js/dist`, `gzip.compress(data, 9, mtime=0)` (`evidence/v54/w3-d/merge/budget_gate_branch.log`, and
   `budget_gate_merged.log` on design-v5 after the merge):

   | Page type | design-v5 `3d5351b` | merged | change | ceiling before → after |
   |---|---|---|---|---|
   | every page, and an interior page with no sheet of its own (`main.css`) | 37 324 | 35 483 | −1 841 | 37 324 → **35 483** |
   | console page types (`main` + `console` + `portal`) | 47 200 | 44 196 | −3 004 | 47 200 → **44 196** |
   | **a journey page** — the dashboard with a person's file, «Mon parcours» with a file, the case file (+ `portal/journey.css`) | 47 200 | 46 617 | −583 | — → **46 617** (recorded, item 6) |
   | **«Ma situation»** (+ `portal/situation.css`) | 47 200 | 46 398 | −802 | — → **46 398** (recorded, item 6) |
   | the company's dashboard (+ `companies.css`) | 48 073 | 45 069 | −3 004 | 48 073 → **45 069** |
   | the help desk · the selection · the Academy (+ their sheets) | 48 075 · 48 285 · 47 818 | 45 071 · 45 281 · 44 814 | −3 004 | → **45 071 · 45 281 · 44 814** |
   | the piece, the loose upload and the Conditions gate (+ `documents.css`) | 52 697 | 49 693 | −3 004 | 52 697 → **49 693** |
   | the two register pages (+ `documents.css` + `core/overlay-panels.css`) | 54 768 | 51 764 | −3 004 | 54 768 → **51 764** |
   | the login (+ `entrance.css`) | 42 185 | 40 344 | −1 841 | 42 185 → **40 344** |
   | the home (+ `hero.css`, `pages.css`) | 51 262 | 49 844 | −1 418 | 51 262 → **49 844** |
   | a content page · an account page · an error page (+ their `cms` sheet) | 41 425 · 39 750 · 40 953 | 39 584 · 37 909 · 39 112 | −1 841 | → **39 584 · 37 909 · 39 112** |
   | the persons pages (+ `pathways.css`) · the ecosystem doors (+ `ecosystem.css`) | 40 818 · 40 659 | 39 068 · 38 910 | −1 750 · −1 749 | → **39 068 · 38 910** |
   | the Forum (+ `forum.css`) · the institutional pages (+ `interior.css`) | 40 818 · 40 121 | 38 504 · 37 749 | −2 314 · −2 372 | → **38 504 · 37 749** |
   | orientation (+ `orientation/wizard.css`) | 41 363 | 39 597 | −1 766 | 41 363 → **39 597** |

   `dist/main.css` 37 324 → 35 483 B (−1 841 on every page): the family's deletions — `components.css` §16 (the V1
   stepper and the progress bar) and §17 (the timeline), `v4/workspace.css`'s JourneyRail and Timeline with
   `rail-draw`, `rail-draw-y` and `tl-light`, `register.css`'s shore crossing — each proved unused on design-v5 and in
   flight (DL54-128 item 3). `dist/portal/console.css` 7 941 → 6 778 B: «Ma situation»'s guided form left it for that
   page's own sheet. The page sheets that shed «la linea» fall (`forum.css` −473, `interior.css` −531); those that now
   import the passage rise by its share (`pathways.css` +91, `ecosystem.css` +92, `orientation/wizard.css` +75,
   `pages.css` +423 for the home's V4 sequence rules) — every one of their page types lighter than before.
   `portal.css` and every other sheet byte for byte design-v5's.
5. **Every ceiling is lowered to the weight measured at this merge** (the definitive ruling: «after a merge, the merged
   weight is the new ceiling»; DL54-120 item 5): every row of the table carries its new figure. A family that needs a
   shared rule pays for it with deletions.
6. **The journey's two page types are recorded as measured — through their own page-only sheet** (V5.8 rule 2).
   `dist/portal/journey.css` (2 421 B: the vocabulary `v5/_journey-nodes.css` and the rail `v5/_journey-rail.css` —
   the dashboard's journey, the case file's spine and timeline, «Mon parcours»'s head), linked by
   `portal/dashboard.html` (a person with a file), `portal/pathways.html` (with a file) and `cases/detail.html`;
   `dist/portal/situation.css` (2 202 B: W3-F1's guided form, then the vocabulary and the Stepper), linked of the
   product's templates by `portal/situation.html` alone (the DEBUG-only showcase links both). **A journey page: 46 617 B;
   «Ma situation»: 46 398 B** — each lighter than the console page type it was on design-v5 (47 200 B), so rule 2's
   performance check is not triggered; the family's accessibility + performance check and its P0 re-check stand for
   the sheet (`A11Y_PERF.md`, `P0_RECHECK.md`). Requests: four stylesheets on those pages (the shell's three and the
   page's one), three on every other console page. Both ratchet down from here.
7. **No duplicate component family** (V5.8 rule 3): the family that merged second consolidated before its merge —
   W3-F1's «la linea» folded into `static/css/v5/_journey-passage.css` (one passage drawing: the door pages, the
   pathway sheets, the questionnaire and the home), the Stepper's rules out of W3-F1's `v5/_wizard.css` (one rail
   drawing: the dashboard, the case file, «Mon parcours», «Ma situation»); the door pages measured identical but for
   their rings' rim antialias (DL54-128 item 2).
8. **The inventory and the capture report.** `scripts/regen_design_inventory.py`: current on the branch; on design-v5
   after the merge, current as well (the merged tree is the branch's) — nothing to write.
   The capture report is unchanged: `capture.py` records the home, the privacy page, the login and the 404 (icons, h1,
   overflow, direction); the family's one change there is the home's orientation steps drawn on the passage, with no
   icon and only while gate G3 is closed, and its shared deletions are rules none of those pages draws — not
   regenerated, as DL54-87 item 5 and DL54-120 item 7 said for W3-B and W3-C.
9. **The tests.** On the branch after the manifest (`9b1fc84`), `TEST_DATABASE_URL=…/test_ile_v5_l6`, one pytest and one
   browser of the steward's at a time, every run behind the benchmark lock, no run crashed
   (`evidence/v54/w3-d/merge/tests_*.log`). **Non-browser** (29 min 18 s) — `apps/cases`, `apps/portal`,
   `tests/test_phase_console.py`, `tests/security` (the object-permission and authorisation audits; the
   confidential-material sentinel test ran), `apps/orientation`, the home's `test_home.py`, `apps/ecosystem`,
   `apps/pathways`, the family's `test_journey_w3_d`, W3-F1's `test_interior_w3_f1` and `test_orientation_w3_f1`,
   `test_chips_cards_w1_c`, `test_script_motion_gate`, `test_design_docs`, the two bundle-current tests,
   `test_static_pipeline` (a real `collectstatic` under the manifest storage), `test_design_showcase`, W3-A's
   `test_console_shell_stylesheets` and `test_console_shell_w3_a`, `test_dashboard_w3_b`, `test_o14_lint`, `test_icons`,
   the ownership and inventory scripts' tests: **1 404 passed, 3 skipped** (the intake suite's own: no legal rule in
   force), 1 xfailed (the showcase's captions, an older marker), **1 failed — design-v5's own** (item 10). **Browser**
   (headless Chromium, 11 min 17 s): the family's `test_journey_browser_w3_d`, W3-F1's `test_browser_w3_f1` and
   `test_orientation_browser_w3_f1`, `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py`,
   `apps/ecosystem/tests/test_browser.py` and `apps/pages/tests/test_browser.py` (the home among them) — **113 passed**, 0
   skipped, 0 failed. On design-v5 after the merge and the rebuild (`cec9425`): the bundle, docs, pipeline, ownership and
   inventory tests, the family's own, the showcase, the chips and W3-F1's two import-list files — **297 passed**, 1 xfailed
   (5 min 32 s). `ruff check .` (CI's lint step): all checks passed; `ruff format --check` on the area's changed Python
   files finds one file, `tests/frontend/test_design_docs.py`, whose two deviations are design-v5's own lines (the same on
   design-v5), not changed; `makemigrations --check --dry-run`: no changes; `manage.py check`: no issue; `git diff --check`
   clean; no CR byte in a text file the branch changes. The full suite is the integration checkpoint's (V5.5).
10. **Design-v5's own failure, unchanged by this merge.**
   `test_script_motion_gate.py::test_no_animate_or_frame_loop_outside_the_gate` fails on W2-A's
   `static/js/src/overlay/extras.js` (`window.requestAnimationFrame`), exactly as on design-v5 at `3d5351b` (DL54-102 item
   10, DL54-120 item 9: `tests_design-v5_own_failure.log`, 1 failed, 5 passed); its fix is `v54-intfix`'s (`822b3ae`), not
   yet on design-v5. The test stops at the first offending module, so its check was run over every module of both trees
   (`motion_gate_all.py`, logged with it): one violation on each, that line, and no other — the family's modules,
   `situation.js` among them, pass the gate.
11. **`live_status.json`: the family row, no surface key.** The journey is drawn inside other families' page types: the
   dashboards (v5 since W3-B), the home and the door pages (v5 since W2-D and W3-F1), and «Ma situation», «Mon
   parcours» and the case file, whose pages W3-E completes (V4's Panel and workspace head on «Ma situation», the
   results and the empty state of «Mon parcours», the case file's page) — so no page type's composition is completed
   by this merge alone, as W3-A's and W2-A's merges said of their systems. The family row says what shipped; W3-E's
   merge marks those three page types.

**Why.** Entries numbered after design-v5's keep the log's one order; paths nobody holds would have no writer for the
next family; the gate is read on the shared payload as V5.8 writes it, and the merged weight becomes every ceiling, so
that the next family meets the weight the product has; a surface's own CSS lives in its own sheet, loaded only where it
is drawn, and its page type is recorded at the weight it was measured at; the preview never says a page is V5 before
its whole composition is.

**Source.** The owner's V5.8 (`C:/tmp/ile_v5_council/directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`, and the
orchestrator's definitive ruling below it) and the V5_5 addenda of 11 October 19:40 and 12 October 01:30; plan §2.2
(the manifest; merge steps 1–5), §2.3, §2.6, §3.5 item 6; DL54-87 item 5; DL54-120; DL54-122 … DL54-128;
`QA/v54/w3-d/NOTES.md`, `REVIEW.md`, `A11Y_PERF.md`, `P0_RECHECK.md`; the weights in
`evidence/v54/w3-d/merge/budget_gate_branch.log`; the ownership checks in `evidence/v54/w3-d/merge/ownership_before.log`
and `ownership_after_wt.log`; the tests in `evidence/v54/w3-d/merge/tests_*.log`.

## DL54-130 · 15 October 2026 · Steward, the sec-f5 merge: F-5 closed on design-v5 — the back office's own sign-in signs no one in, a second factor an account holds is presented in every session; the family registered outside the waves; nothing deployed

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-sec-f5` into design-v5 on 15 October 2026 —
the owner's V5.9 (`C:/tmp/ile_v5_council/directives/V5_9_DELIVERY_AND_PRODUCTION_READINESS.md`: never deploy, never
touch production); what the lanes hand to the merge: `QA/v54/sec-f5/NOTES.md`, with «Review fixes» and «At the
merge», and `REVIEW.md`).

1. **What merged: the DevOps lane's go-live blocker F-5, fixed** (DL54-121 item 7.1; checklist A-13). With
   `BACKOFFICE_MFA_ENFORCED=True`, an account holding a TOTP device reached `/backoffice/` on its password alone
   through Django's admin sign-in form (the unfold site's own `login` view: no MFA stage, no rate limit), because the
   policy asked whether a device was *enrolled*, never whether *this session* had presented it. Twelve commits
   `9eef573` … `01609b1` on design-v5 `3d5351b` — the reproduction first, as a strict xfail (`9eef573`); the fix
   (`1dd3185`, `a340bff`, `e6170d6`, `812e8ef`, `17c9dd9`); the lane's notes and the DevOps documents (`8d98992`); an
   independent review; a fix pass for its four findings (`98b0067`, `a29e3cd`, `035da86`, `96ba940`); the notes and
   the review (`01609b1`) — and the merge step's four commits on the branch. Twenty-two paths:
   - **(a) the back office's own sign-in signs no one in** — `apps/accounts/admin_site.py`: `BackofficeAdminSite`,
     unfold's site, whose `login` never reads the request body and never calls `authenticate` or `login`. Signed out
     → allauth's sign-in, with a `next` that is a page of this back office or else its index (Django's
     `url_has_allowed_host_and_scheme`, then a path under the index: no open redirect); signed in as an active staff
     account → the page, or first the second factor; signed in otherwise → 403 (no form to sign in as another
     account, no loop). Installed as the default admin site by `apps/accounts/admin_apps.py` (an `AdminConfig` in
     place of `django.contrib.admin`, beside `unfold.apps.BasicAppConfig`); the lane diffed the registry (107 models)
     and the 118 admin URL patterns against design-v5: identical.
   - **(b) the policy asks about the session** — `accounts.services.second_factor_due`, for an account that reads
     other people's data: **Enrol** as before (no TOTP device and the flag on → the activation page); **Present**,
     new — the account HOLDS a second factor and this session has not presented one of its own authenticators
     (allauth's `mfa` step in the session's authentication log, or a device the session has just enrolled through
     allauth's own activation) → allauth's MFA re-authentication, then back, whatever the flag says. The flag makes
     enrolment mandatory; allauth asks an enrolled account for its code at every sign-in anyway, so a signed-in session
     without the step came through another door. Enforced at three points: `BackofficeMFAMiddleware` (the back
     office; the reserved area and now `/documents/`, whose endpoints serve the reserved area's pieces outside its URL
     prefix; allauth's pages that manage the factor, whose password re-authentication was the way round it — the
     exemptions are now the exact sign-out routes, never a fragment anywhere in a path), the admin site's
     `has_permission`, and `mfa_required_for_backoffice`.
   - **the documents**: «the flag makes enrolment mandatory; a device the account holds is asked for in every
     session» in `base.py`, `prod.py` (which cited a removed name), `.env.example`, `README.md`, `docs/SECURITY.md`,
     `docs/security/PERMISSION_MODEL.md` and `accounts.W001`; DevOps's checklist A-13, runbook and notes say «fixed
     by», with the test names; nginx's redirect of `/backoffice/login/` (runbook step 11) stays as a second layer.
   - **the tests**: `apps/accounts/tests/test_backoffice_second_factor.py` (90 tests: every way into the back office
     of the lane's table, and each review finding); `test_mfa_middleware.py` (its two assertions of the account-level
     rule now require the session's step); the runbook test's docstring; the design preview's framing test, which
     linked `/backoffice/login/` and now links the preview's own index (signed out, a back-office address ends at
     allauth's sign-in, a page the frame may hold).
2. **The review** (lane `sec-f5-review`, `QA/v54/sec-f5/REVIEW.md`, on `8d98992`): **SHIP_AFTER_FIXES, nothing
   blocking — F-5 closed.** 143 of the reviewer's 144 attack tests held, among them a sweep of all 657 admin URL
   patterns (GET, POST and HEAD; with the middleware and with the admin site alone; both values of the flag); the
   same attacks reproduce F-5 on design-v5; rate limits, CSRF, no user enumeration, session rotation and the audit
   trail did not regress. Four minor findings, each fixed with its tests by lane `sec-f5-fix2` before this merge:
   (1) security — after a *password* re-authentication allauth resumes a suspended POST by calling the view itself,
   past the middleware, so a session that never presented the factor could regenerate the owner's recovery codes (it
   opened nothing, and those pages were open to everyone before the fix) → a session that owes the factor resumes
   nothing on a password step (`98b0067`); (2) documents — `prod.py` cited the removed `EXEMPT_FRAGMENTS`, and several
   places described the flag as switching the factor on or off (`96ba940`); (3) efficiency — the policy read the
   account's authenticators at every `has_permission` call; now once per request, 8 → 2 of an admin list page's
   queries (`035da86`); (4) tests — a documented helper no production code called; the policy now decides through it
   (`a29e3cd`). The reviewer's whole suite on the fixed branch: 144 passed.
3. **The other security properties and the hard limits, checked at the merge.** Rate limits: every sign-in is
   allauth's (Django's admin form had none), and the one new door, the MFA re-authentication, is allauth's, limited.
   CSRF: global and untouched. No user enumeration: the closed view answers every POST alike, whatever the account.
   Session rotation: every sign-in still goes through Django's `login()`. Audit: every sign-in and failed sign-in is
   still audited; the closed view authenticates no one. Nothing deployed; no server, DNS record or certificate
   touched; no package added (allauth 65.19.4, Django 5.2.17, django-unfold 0.107.0, as installed); no password typed
   into a real page — the tests' accounts use the test-only password of the existing auth tests. The family's diff
   (1 989 added lines) scanned in Python: no IPv4 address but loopback (the documented local test database), no
   production host or droplet name, no live domain, only `example.test` addresses, no credential but that test-only
   password and one other marked «test-only».
4. **The pre-merge sync**: design-v5 had moved from `3d5351b` to `fec37d3` (W3-D's merge, DL54-129, its shipped
   note); the sync (`ddd468d`) met no conflict, and the two sides share no path (W3-D: templates, CSS, JS, presenters
   and their tests; this family: accounts, settings, documents). No template, CSS or JS in the family: no bundle
   rebuilt, and V5.8's shared CSS gate is not concerned (the bundles are design-v5's byte for byte). No test outside
   `apps/accounts` creates an authenticator, so the Present rule meets no other family's tests.
5. **The family «sec-f5» is in the manifest, outside the waves** (`93eff12`): wave 0 as devops, `steward` false,
   DL54-01's branch and worktree, no merge tag. Twenty-one entries, each with its reason — whole: the admin site and
   its `AdminConfig`, F-5's test module, `docs/design-v5/QA/v54/sec-f5/**`; slices: the policy in `middleware.py`,
   `services.py`, `decorators.py`, `apps.py` (beside W1-D's receiver) and `checks.py` (four of them files no family
   held), the updated assertions of `test_mfa_middleware.py` (beside W2-B's slice), the admin pair and the flag's
   comment in `base.py`, the flag's words in `prod.py`, `.env.example` and `README.md` (beside devops's slices), the
   A07 and §12.2 rows of `docs/SECURITY.md`, the paragraph and the L-10 row of `PERMISSION_MODEL.md`, F-5's lines in
   four of devops's files (checklist A-13, the runbook, its notes, the runbook test's docstring) and the framing test
   in W1-P's `test_design_preview.py`. `scripts/check_ownership.py` accepts the id `sec-f<n>` — the fix of a go-live
   security finding, named after it; F-7's is in flight — and its id test holds five new cases (`814e005`).
   `check_ownership.py sec-f5 design-v5` before the steward's commits: 22 paths, 5 inside, 17 slice → PASS; each
   slice was read in the diff and stays inside it. After them the steward's three paths join the list: the manifest
   (steward-only), the checker and its tests (the steward's whole files). `--validate`: coherent, 27 families, 672
   entries.
6. **The tests**, `TEST_DATABASE_URL=…/ile_v5_l4`, one pytest at a time, `-p no:randomly`, on the merged branch:
   the merge brief's list — `tests/backoffice`, `apps/accounts`, `tests/security` (the production settings' refusals
   among them), `tests/deployment` (`test_production_checks.py` among them), `tests/compliance`,
   `tests/frontend/test_design_docs.py` — with the checker's tests, `tests/test_env_example_is_complete.py` and
   `tests/test_migration_drift.py` (`makemigrations --check`, V5.9 §7): **574 passed in 12 min 12 s, no skip, no
   xfail**. Then `tests/frontend/test_design_preview.py` and `tests/i18n/test_documentation.py` (`-m "not browser"`;
   W3-D's merge changed the preview's `apps/core/dev.py`, and the family the preview's framing test): 307 passed; that
   framing test in Chromium: 1 passed. `manage.py check`: no issue. `ruff check` and `ruff format --check`: clean on
   the 15 Python files the merge brings. The logs are in `evidence/v54/sec-f5/merge/`.
7. **Not done here, on purpose.** No tag (V5.9 §14: the release tags mark the whole product after final QA); no
   restart of 8780; no change to v5-live; no push; no line in `CHANGELOG_V54.md` or `live_status.json` (not a preview
   surface — DL54-77, DL54-121). The full suite stays the integration checkpoint's (V5.5) and CI's; on the server,
   D-12 (the TOTP code asked before the back office opens) is the owner's check after his deployment. **main** (the V4
   line) is the merge brief's next step, after the lock: a `cherry-pick -x` of the fix's ten code-and-test commits
   (not the notes, manifest or decision-log commits), kept only if it applies cleanly and main's back-office,
   accounts and security tests pass, aborted otherwise — the release comes from design-v5 either way. The lane's
   observations for the owner stay decisions, not fixes: how long the proof lasts (the session — 8 hours after its
   last write, the cookie ending with the browser), one password-change path instead of two, rate limits counted per
   Gunicorn worker. **The number**: this entry takes DL54-130, design-v5's next free one. W3-E's branch had numbered
   its twelve entries DL54-130 … DL54-141 (DL54-129 item 1); they follow this one at its sync, as W3-D's followed the
   devops merge's DL54-121.

**Why.** F-5 was the back office's go-live blocker: a second factor that a password alone can skip is no second
factor. The fix closes both the door (the admin's own form) and the rule (the account asked about instead of the
session) — either alone would have left the other open; and a family no plan section names still needs one writer
per path, or the next change to these files would have none.

**Source.** The owner's V5.9 §6 and §14–§17; DL54-121 (item 7.1: F-5 as the owner's first open question; the family
outside the waves as precedent); DL54-01 (the ref names); DL54-77 (a merge that is not a preview surface); DL54 «How
it is kept»; plan §2.2 (a file not in the manifest has no writer until the steward assigns it); checklist A-13;
`QA/v54/devops/NOTES.md` (F-5); `QA/v54/sec-f5/NOTES.md` (with «Review fixes» and «At the merge»), `REVIEW.md`; the
ownership checks and the test logs in `evidence/v54/sec-f5/merge/`.

## DL54-131 · 16 October 2026 · Steward, integration checkpoint 3: the full suite on design-v5 after Wave 3's merges, its reds fixed at their root; the family «intfix» registered outside the waves; the tag `v54/checkpoint-3`

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-intfix` into design-v5 on 16 October 2026 —
the owner's V5.5 («full regression only at important integration checkpoints»), V5.8's definitive ruling and V5.9
(never deploy, never touch production); what the branch hands to the merge: `QA/v54/intfix/NOTES.md` — step 1, the
checkpoint's two passes and «At the merge» — and `REVIEW.md`).

1. **What the checkpoint is.** The full regression V5.5 keeps for the important integration points, run on design-v5
   once Wave 3's queued merges had landed — W3-F1, W3-C and the DevOps readiness merge (DL54-109, DL54-120,
   DL54-121), then W3-D's (DL54-129), which joined it during the first pass — with the steward's fixes for every red.
   The branch `v54-intfix` was cut from design-v5 at `8e13cd2` (12 October) and merged design-v5 four times: `e6ecbde`
   (at `a2644b0`), `aff19e7` (at `3d5351b`), `a059610` (at `fec37d3`) and `23600fc` (at `f447c28`, the sec-f5 merge
   and DL54-130 — the pre-merge sync, under the lock). Every source merged without a conflict; the generated bundles
   were rebuilt from a clean dist each time.
2. **The full suite** (lane 3, `test_ile_v5_l3`, Chromium, `-p no:randomly`; NOTES «Checkpoint 3» and «second pass»):
   - first pass, on `aff19e7` (design-v5 at `3d5351b` with step 1's fixes), a fresh test database: **5 058 passed, 0
     failed**, 3 skipped, 2 xfailed (507 deselected) in 1 h 03 min 45 s; in Chromium **507 passed, 0 failed, 1 error**
     (a teardown, item 4) in 55 min 11 s, then, on `d8fdc42`, **507 passed, 0 failed, 0 errors** in 49 min 38 s;
   - second pass, on `a059610` (design-v5 at `fec37d3`, W3-D's merge), a fresh test database: 5 108 passed, **3
     failed** — design-v5's own since W3-D's merge (item 5) —, 3 skipped, 2 xfailed (519 deselected) in 1 h 01 min 40
     s; the three files fixed and their neighbours on `34c5471`: **954 passed, 0 failed**, 1 xfailed; in Chromium on
     `34c5471`: **519 passed, 0 failed, 0 errors** in 52 min 23 s, with a teardown survey (a pytest plugin, kept as
     evidence) that found no test leaving a request of the live server running;
   - the skips are `apps/cases/tests/test_intake.py`'s three cases that need a legal rule in force (none is); the
     xfails the two declared debts. No browser run crashed. Firefox and WebKit are not installed: Chromium only.
3. **Step 1's four fixes** (12 October: the reds DL54-102 item 10 handed over, and CI's):
   - (a) `31e3084` — `test_design_preview.py`'s reset test packed SO_LINGER as Windows' `struct linger` (two `u_short`);
     Linux's is two `int` and refuses the short option with errno 22, as GitHub's runner did: `"HH"` on Windows, `"ii"`
     elsewhere (proved in a `python:3.13-slim` container). What the test proves is unchanged;
   - (b) `822b3ae` — W2-A's `overlay/extras.js` asked for a frame itself (`requestAnimationFrame`), against W1-D's rule
     that only `motion.js` does (`test_script_motion_gate`): `overlay.js` imports `nextFrame` from `motion.js` and hands
     it over in the core it installs (extras.js still imports nothing); one re-read per frame of resizes, as before;
   - (c) `96b389d` — **a real bug of the overlay system**: on a console page at phone width, «Menu», Esc, then Space
     within one frame, and a press on the scrim no longer closed the drawer (W3-A's «Menu» test failed 2 runs in 3 on
     design-v5). A dialog's native `close` event comes late; settled again after the drawer had reopened, it took the
     new opening's trap away (`aria-modal`, the scrim, the lock, the focus; the panel left `inert`). Two parts, both
     needed: the late event settles only a dialog that is closed; `open()` settles a close it has not heard. The new
     test `test_a_drawer_closed_and_opened_again_within_a_frame_keeps_its_trap_and_a_press_on_the_scrim_closes_it`
     failed 4 runs of 4 before the fix and passed 10 of 10 after; the review served the chunk with either half undone
     and the test failed each time;
   - (d) `37dd8ad` — the loader: with `loader.js` lost, `shell.js` took back its face but main.js's double-submit guard
     stayed (`data-submitted`, `aria-disabled` for ever — WCAG 4.1.3) on every `data-single-submit` form; the catch now
     lifts it with the face. Two of `test_loader_w1_d.py`'s tests were stale — W3-F2 guarded the profile form and W2-C2
     retired the account menu's V4 face, legitimately — and read today's markup, asserting as much or more;
     `test_loader_rules.py` pins the release.
4. **The checkpoint's own find** (`d8fdc42`): `test_drawer_browser_w3_c.py::test_a_modified_press_keeps_the_links_own_way`
   closed its Ctrl+click tab still on `about:blank` while the live server went on rendering the piece's page in its
   request's transaction; pytest-django's flush (`TRUNCATE`) deadlocked with it once in the first browser run. The test
   now lets the tab load the link's own path before closing it (58 runs of 58 with no request in flight at its
   return). No product code involved.
5. **W3-D's three reds** (design-v5's own since its merge; reproduced on a pristine `fec37d3`):
   - `f2f1e67` — a four-line `{# #}` in `templates/dev/showcase.html` rendered into the page (Django's `{# #}` is one
     line): the same words in `{% comment %}` (development only);
   - `71a3675` — `test_v5_tokens.py::test_the_console_partials_close_the_console_entry` gave each console partial ONE
     importer (DL54-112); W3-D composes one vocabulary (`v5/_journey-nodes.css`) into two page sheets of the portal
     (DL54-128 item 4). **Supersedes DL54-112's «one importer» rule** with what it protected: a partial is the console
     entry's or page sheets', never both; the entry imports a partial once; and no product template, through its chain
     of `{% extends %}`, links two sheets that import the same partial — mutations caught;
   - `34c5471` — `apps/pages/tests/test_templates_static.py` banned any `@import` in the home's sheet (`3093261`, when the
     sheet was served as written); the home links its bundle now, which inlines W3-D's passage partial. **Supersedes
     `3093261`'s ban**: the source may import local `_` partials only, the bundle the home links holds no `@import`, and
     the tokens, logical-properties, no-URL, no-`!important` and wording checks run on the imported partials too.
6. **The review** (lane `intfix-review`, `REVIEW.md`, on `792dd9d`): **SHIP** — no P0, no major; each fix at its root;
   no test weakened (the two corrections above follow a recorded decision, with written reasons); no family's design
   touched. Its runs: 19 of 19 JS and 22 of 22 CSS bundles rebuilt byte for byte; 741 static tests passed (one
   mtime-only red, m1, closed by this merge's clean rebuild); 162 browser tests passed. Four minors and two nits,
   handed on (item 10).
7. **The family «intfix» is in the manifest, outside the waves** (`1f4d63f`): wave 0 as devops and sec-f5, `steward`
   false — its fixes are held to slices like any family's —, DL54-01's branch and worktree, no merge tag (this entry's
   tag marks design-v5). Twelve entries, each with its reason: whole, `docs/design-v5/QA/v54/intfix/**`; slices, each
   file staying its owner's — `overlay.js` and `overlay/extras.js` (W2-A's), `shell.js`'s catch (in W1-D's section),
   the showcase's comment block, the SO_LINGER layout (W1-P's test), the drawer test's wait (W3-C's), the loader's
   rule and three tests (W1-D's), the overlay's new test (W2-A's), the console partials' guard (W1-A's file, beside
   W3-C's slice) and the home sheet's import rule (beside W1-B's and W2-D's slices). `scripts/check_ownership.py`
   accepts the id `intfix` (`473aa20`, three id cases). `check_ownership.py intfix design-v5` before the steward's
   commits: 37 paths, 2 inside, 11 slice, 24 generated → PASS, each slice read in the diff; after them the steward's
   three paths join (the manifest, the checker and its test). `--validate`: coherent, 28 families, 684 entries.
8. **The tests at the merge** (on `v54-intfix` after the sync, `1f4d63f`): the test files the branch changed and those
   that cover its sources (the overlay's, the shell's and the showcase's), `test_design_docs`, `test_static_pipeline`,
   both bundle-currency tests, `tests/security` and sec-f5's two test modules (the sync's newest code): **1 824 passed,
   0 failed**, 1 xfailed (the showcase's declared debt) in 10 min 19 s; in Chromium the overlay and console browser
   tests (the late settle's test and W3-A's «Menu» test among them), `apps/portal/tests/test_browser.py`, W2-C2's phone
   menu, `test_loader_w1_d` and the browser tests of the files the branch changed (the drawer's; the preview's, sec-f5's
   framing test among them): **200 passed, 0 failed, 0 errors** in 22 min 05 s, no crash; `manage.py check`,
   `makemigrations --check --dry-run`, `ruff check .`: clean. On design-v5 after the merge and the rebuild (`7440612`):
   both bundle-currency tests, the static pipeline, the overlay's and the loader's rules, the static assets, the motion
   gate and the checker's tests — 166 passed.
9. **The weight (V5.8).** No stylesheet changed: every `css/dist` bundle rebuilt from clean on design-v5 after the merge
   is byte for byte the one before it, so the shared payload and every recorded page-type ceiling stand where DL54-129
   put them (`main.css` 35 483 B on every page; the console page types 44 196 B). JS (gzip −9, design-v5's chunk names
   after the rebuild): the overlay core chunk 6 476 → 6 520 B (19 456 → 19 546 B minified), the extras chunk 1 600 →
   1 597 B, the `overlay.js` entry 143 → 153 B, the `shell.js` entry 1 164 → 1 212 B; every other entry and chunk the
   same, the chunk names read as one — no product page fetches anything new (`motion.js`'s chunk is already in the graph
   of every page that loads the overlay system); only the dev specimen board that loads `overlay.js` alone now fetches
   the Motion chunk.
10. **Left, and handed on.** The review's m2 and m3 to W1-D (shell.js's catch is the one release only while every
   guarded form submits through a `.btn` — a static test of that premise, or the release on the early return too;
   `initMisc`'s comment in `main.js` still names loader.js as the guard's only lifter), m4 to W2-A (a resize step in
   the 400 % test, so fix (b)'s path has a behavioural test), n1 to the steward's next pass over `test_v5_tokens.py`
   (cite DL54-128 item 4 for the third way not taken; say the chain check follows `{% extends %}` only). The review's
   «seen on the way», not this branch's: a year of cache (`WHITENOISE_MAX_AGE`) on the three fixed-name scripts imported
   from inside the bundles (`loader.js`, `depot.js`, `piece-drawer.js`) → the DevOps owners and W1-D; a live server
   that can draw a port Chromium refuses → the test infrastructure. Not run: GitHub's runner on this tree, Firefox and
   WebKit. main (the V4 line) untouched. No push; nothing deployed.
11. **The record.** Merged with `--no-ff` (`6f89147`); both dist trees rebuilt from clean on design-v5 (`7440612`);
   `regen_design_inventory.py`: the inventory tables and the counts are current, nothing to write; `CHANGELOG_V54.md`
   gains an «integration checkpoint 3» line and `live_status.json` its date (no surface changes state: the checkpoint is
   no preview surface — every page type keeps the state its family gave it); the annotated tag **`v54/checkpoint-3`**
   goes on the commit that writes them; v5-live is then checked out at the tag and 8780 restarted as
   `evidence/v54/SERVERS.md` says (`ile_v5`). **The number**: DL54-131, design-v5's next free one; W3-E's branch
   numbered its entries from DL54-130 (DL54-130 item 7) and follows this one at its sync.

**Why.** Wave 3's surfaces were merged one by one, each with its targeted tests and none with the whole suite: four reds
had reached design-v5 (one a real overlay bug a person meets on a phone, one a refusal no one could end) and CI's hosted
job was red. A checkpoint that runs everything, fixes each red where it starts — the product where the product was wrong,
the test where the test was stale, with the reason written — and tags the result gives the owner a known-good point
for the preview and for the next GitHub checkpoint.

**Source.** The owner's V5.5 (5 October 2026: «full regression only at important integration checkpoints»), V5.8
(definitive ruling, 12 October 02:15), V5.9; DL54-01; DL54-77 (the previous checkpoint); DL54-102 item 10 (the reds handed
over); DL54-112; DL54-128 item 4; DL54-129; DL54-130; plan §2.2 (a file not in the manifest has no writer until the
steward assigns it); `QA/v54/intfix/NOTES.md`, `REVIEW.md`; the logs and JUnit files in
`C:/tmp/ile_v5_council/evidence/v54/intfix/` (`cp3_*`, `cp3_w3d_*`, `cp3_merge_*`).

## DL54-132 · 16 October 2026 · Steward, the sec-f7 merge: F-7 closed on design-v5 — who may move a case file is the domain's, the lifecycle's «Chi può» column as data, enforced by `transition` and offered by `transitions_available`; a person whose file is suspended or closed is told so; the family registered outside the waves; nothing deployed

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-sec-f7` into design-v5 on 16 October 2026 —
the owner's V5.5 and V5.9 (`C:/tmp/ile_v5_council/directives/V5_9_DELIVERY_AND_PRODUCTION_READINESS.md`: never deploy,
never touch production); what the lanes hand to the merge: `QA/v54/sec-f7/NOTES.md`, with «Review fixes» and «At the
merge», and `REVIEW.md`).

1. **What merged: the finding F-7, fixed** (W3-D's review; confirmed by the orchestrator on design-v5 `fec37d3`).
   `cases.policies.case_policy` gives a file's owner «change» while the file is active, and `cases.services.transition`
   and `transitions_available` filtered only by the declared graph (`models.transitions_from`) and that object policy —
   never by WHO may make each move. A person could move their own file ORIENTED → ADMIN_PROCESS («Procédure
   administrative en cours»), ADMIN_PROCESS → PRE_DEPARTURE, PRE_DEPARTURE → ENTERED, and TRAINING → SELECTION whenever
   an authorised actor was assigned (CR-03's reserved activity), and the journey «La soglia» then drew it as a fact. The
   specification is `docs/platform/CASE_LIFECYCLE.md` §4, its «Chi può» column and rule 2 («Una transizione non
   dichiarata in questa tabella è rifiutata dal dominio, non solo nascosta nell'interfaccia»); the column lived only in
   the document. Fifteen commits on design-v5 `fec37d3`: the domain fix with its tests (`0168c4b` — its twelve
   reproductions failed on `fec37d3` before any code changed), the back office pinned (`ef1d545`), the dashboard of a
   held file (`290c5ae`, `045fad3`), `CASE_LIFECYCLE.md`'s pointer (`b955215`), the lane's notes (`9a9bb5c`); an
   independent review; a fix pass for its findings (`949074b` … `659be72`); the notes and the review (`36ab4b9`) — and
   the merge step's four commits on the branch (the sync, DS 2026 §11.7, the manifest, «At the merge»). Seventeen paths:
   `apps/cases/{models,services,admin}.py`, `apps/selection/services.py`, `apps/audit/services.py`,
   `apps/portal/services.py`, five test modules (three new), one condition of `templates/portal/dashboard.html`, one
   paragraph of `CASE_LIFECYCLE.md` and of DS 2026 §11.7, the lane's reports and the manifest. No migration, no CSS, no
   JS, no new word in a catalogue.
2. **The table as enforced** — `cases.models.TRANSITION_ACTORS`, `SUSPEND_ACTORS`, `CLOSE_ACTORS`, `CLOSE_ACTORS_FROM`,
   `RESUME_ACTORS` and `transition_actors`; the effective right is `cases.services.permitted_transitions`, the object
   policy's «change» AND the column, never one without the other, so the fix narrows and widens nobody's access:

   | From → to | §4, «Chi può» | Enforced |
   |---|---|---|
   | DRAFT → ORIENTED | sistema | the platform only (the orientation service, `actor=None`) |
   | ORIENTED → REVIEW_REQUIRED | sistema, operatore | the platform; an operator assignee |
   | ORIENTED → TRAINING | operatore, ente formativo | an operator assignee — the training body is named, not granted: the policy gives it no «change» (Q2) |
   | ORIENTED → ADMIN_PROCESS | operatore | an operator assignee |
   | REVIEW_REQUIRED → ORIENTED, → TRAINING | professionista | a professional assignee |
   | TRAINING → SELECTION | soggetto autorizzato | the authorised actor through `selection.services.open_process` only (`as_authorised_actor=True`), its assignment standing; CR-03 |
   | SELECTION → ADMIN_PROCESS | soggetto autorizzato | the authorised actor through `selection.services.conclude` with a referral, its assignment standing |
   | SELECTION → TRAINING | — (not in §4) | the authorised actor through `conclude` without a referral, even once its assignment ended; the administrator — `BEYOND_SECTION_4` |
   | ADMIN_PROCESS → PRE_DEPARTURE | operatore | an operator assignee |
   | PRE_DEPARTURE → ENTERED | operatore | an operator assignee |
   | ENTERED → POST_ENTRY | sistema — automatica | the platform; the administrator, standing in for the automation nothing performs — `BEYOND_SECTION_4` (Q5) |
   | POST_ENTRY → CLOSED | operatore, persona | an operator assignee, the person, the administrator |
   | any active state → SUSPENDED | persona, operatore, amministratore | the person, an operator assignee, the administrator — a reason required |
   | any state → CLOSED | persona, amministratore | the person, the administrator |
   | SUSPENDED → the state it left | chi ha sospeso, o superiore | the account that suspended it (this suspension's own audit event) and the administrator |
   | REVIEW_REQUIRED → ADMIN_PROCESS, TRAINING → ADMIN_PROCESS, TRAINING → ORIENTED, ADMIN_PROCESS → REVIEW_REQUIRED, PRE_DEPARTURE → ADMIN_PROCESS; SUSPENDED → any other state | — (not in §4) | nobody (rule 2); the platform's own path still makes them (Q1) |

   The capacities are read as the policy reads them (`_capacities`): a superadmin is the administrator; the owner is the
   person, whatever else the account holds; otherwise every live assignment's role; otherwise the administrator role —
   an administrator assigned to a file acts in its assignment's capacity. A refused move raises `TransitionNotPermitted`
   (a `TransitionRefused`) in the domain's existing sentence; the 403 stays the object policy's, in the view.
   `transitions_available` is `permitted_transitions` minus what CR-03 still blocks, in the lifecycle's order: the case
   page never offers a move the domain refuses. `test_the_data_says_what_section_4_says` reads §4's table from the
   document and holds the data to it plus exactly `BEYOND_SECTION_4`, each departure with its reason; the day the owner
   changes the table, the test says the data must follow.
3. **Every other way a status changes** (NOTES §3, «Review fixes» 2–6). `services.transition` stays the only writer of a
   file's status; the orientation service and the seeds keep the platform's path (`actor=None`, unchecked as before, now
   recorded as nobody's — `audit.services.record(..., system=True)`, label «system», finding 6); the selection service
   moves the file in the authorised actor's capacity and `conclude` moves it before it revokes the mandate's assignment.
   Every move is judged on the file's row as it stands, locked (`SELECT … FOR NO KEY UPDATE`, the lock a status write
   takes anyway; finding 5); «chi ha sospeso» is read from this suspension's own event (finding 3); CR-03 counts
   AUTHORISED_ACTOR assignments only (the review's observation). The back office hands out no capacity (finding 2):
   `CaseFileAdmin`'s owner and suspension reason read-only and no add form; the assignment inline shown, never edited;
   `CaseAssignmentAdmin` grants through `services.assign` and ends through `services.revoke_assignment` (one audit event
   and one notification each), and only for an account the assignment's own policy lets change it. No management
   command, signal, form, API or data migration writes a status (NOTES §3).
4. **Part B, the dashboard of a held file** (the same review's second item). W3-B's person dashboard told a person whose
   latest file is suspended or closed «Vous n'avez pas encore de dossier…» and offered the questionnaire, because
   `portal.services.active_case` keeps the active statuses only — and for a suspended file the questionnaire would open
   a second file beside it. `portal.services.held_case` (the latest SUSPENDED file, else the latest CLOSED one, through
   `readable_by`); the NowPanel's two held variants (`_held_now`: «Dossier suspendu» with the reason in its writer's
   words, the file as the primary; the closed state's label, the domain's sentence «Un dossier clôturé ne se rouvre
   pas : on en ouvre un nouveau.» and the questionnaire that opens a new file); on a held file no next action and no
   takeover, the journey from its trail (W3-D's `journey_with_dates`: where it stopped, nothing «here»); the one
   template change — the «Dossier» section's suspension notice steps aside when the NowPanel draws the reason; a closed
   file names no next action on its own page either (`next_action`, §4 rule 5). `active_case`'s other callers are
   unchanged (the reassessment never touches a held file). DS 2026 §11.7 now says six variants (`25aac85`, written by
   the steward: the notes' hand-over).
5. **The review** (lane `sec-f7-review`, `QA/v54/sec-f7/REVIEW.md`, on `9a9bb5c`): **SHIP_AFTER_FIXES, nothing blocking
   — F-7 closed for the person, nothing regressed.** Every account of a cast of 16 in every state, sent every state as a
   forged target through the transition view, moved exactly §4's set for its capacity (the administrator its wider set:
   finding 1); every move wrote one audit event naming the account and one notification to the person, every refusal
   neither; the page's offer equals what the domain accepts for 21 accounts in every state; the same matrix on `fec37d3`
   reproduces F-7. Two major findings in F-7's own subject — (1) the administrator on every declared row: from the case
   page it opened SELECTION with no mandate and concluded it, claimed an orientation and a professional review; (2) the
   back office let role:operator give itself a capacity the column refuses (the file's owner, another assignment's role
   or file) and then make that capacity's moves, with no domain event — five minor ones and one observation, each fixed
   with its tests by lane `sec-f7-fix2` before this merge: finding 1 (`949074b`, `659be72`), 2 (`5020315`),
   3 (`83634d4`), 4 (`fa172e1`), 5 (`f140de6`), 6 (`e55d5e6`), the CR-03 observation (`d5b0ae1`); finding 7 (words of a
   held file) goes to the owner's copy packet B1. Each new test was run against the code before its fix and failed
   there, but for the three kinds of exception «Review fixes» names. The reviewer's 89 tests on the fixed branch: 85
   passed; the four others encode the reading finding 1 removed.
6. **The other security properties, checked at the merge.** Object permissions and the `readable_by` queryset unchanged:
   the column is intersected with the policy, so nobody gains a move, and the training body and the authorised actor
   gain nothing on the case's path. An audit event on every transition, in the move's atomic block, on the locked row.
   The suspension rule: a reason to suspend, never rewritten in the back office. CLOSED read-only for everybody. CR-03's
   authorised-actor check, stricter (the assignment's role counts). Notifications unchanged: one to the person per move,
   one per grant and per revocation. Nothing deployed; no server, DNS record or certificate touched; no package added;
   personas only through minted sessions, no password typed. The family's 2 747 added lines scanned in Python: loopback
   only (the documented local test database), `example.test` addresses only, no URL, no credential, no production host
   or droplet name, no live domain (`evidence/v54/sec-f7/merge/scan_added_lines.log`).
7. **The pre-merge sync** (`fcd4153`): design-v5 had moved from `fec37d3` to `8ab5b89` — 41 commits: the sec-f5 merge
   and DL54-130; integration checkpoint 3 (the intfix merge, its rebuild, DL54-131, the changelog line). No conflict and
   no path in common. Both dist trees deleted and rebuilt from clean on the branch: the CSS byte for byte; the JS
   identical once esbuild's chunk names are read as one — they follow the worktree, the Motion library being resolved
   through the `node_modules` junction —, so design-v5's committed tree was kept and the branch carries design-v5's
   bundles byte for byte: the merge brings none, and nothing is rebuilt on design-v5. **The weight (V5.8)**: no
   stylesheet changed — `main.css` 35 483 → 35 483 B on every page, the console page types 44 196 → 44 196 B; every
   recorded ceiling stands where DL54-129 put it.
8. **The family «sec-f7» is in the manifest, outside the waves** (`a999215`): wave 0 as devops, sec-f5 and intfix,
   `steward` false, DL54-01's branch and worktree, no merge tag. Fourteen entries, each with its reason — whole: F-7's
   test module, the held file's, the selection exits', `docs/design-v5/QA/v54/sec-f7/**`; slices: the column as data in
   `cases/models.py` (beside W3-C's slice), its enforcement in `cases/services.py` (beside W3-B's `next_action` and
   W3-D's `journey_for`), the back office's two screens in `cases/admin.py` and `audit.services.record`'s `system`
   keyword (files no family held), the selection service's two moves (beside W3-A's slice), the held file's presenter in
   `portal/services.py` (beside W3-B's), the dashboard's one condition (W3-B's file), the audited move in
   `test_views.py`, `CASE_LIFECYCLE.md`'s pointer paragraph and DS 2026 §11.7's NowPanel paragraph (beside W3-B's). The
   checker already accepts `sec-f<n>` (DL54-130); its test names the family among those outside the waves.
   `check_ownership.py sec-f7 design-v5` before the manifest's commit: 15 paths, 5 inside, 10 slice → PASS, each slice
   read in the diff; after it the steward's two paths join the list (the manifest, steward-only; the checker's test, the
   steward family's). `--validate`: coherent, 29 families, 698 entries. `regen_design_inventory.py`: the inventory
   tables and the counts are current.
9. **The tests** on the merged branch (`a999215`), `TEST_DATABASE_URL=…/ile_v5_l7`, one pytest at a time,
   `-p no:randomly`: **1 106 passed, 3 skipped** in 17 min 19 s (`-m "not browser"`) — the merge brief's list:
   `apps/cases` (183, F-7's 82 among them), `apps/portal` (215, the held file's 13 among them), `tests/security` (157),
   `tests/test_phase_console.py` (8), `apps/notifications` (95), `tests/deployment` (54),
   `tests/frontend/test_design_docs.py` (40) and both bundle-currency tests (8); with `apps/selection` (86) and
   `apps/audit` (8), which the fix reaches, `tests/backoffice` (5) and sec-f5's `test_backoffice_second_factor.py` (90 —
   sec-f5's admin site and this family's admin screens on one committed tree for the first time), the checker's test
   (57), `tests/test_migration_drift.py` (2) and W3-B's and W3-D's static tests of the dashboard and the journey
   (60 + 41). The three skips are `test_intake.py`'s cases that need a legal rule in force (none is). In Chromium,
   `apps/portal/tests/test_browser.py` and `tests/frontend/test_dashboard_browser_w3_b.py` (the dashboard's template and
   presenter changed; the overlay and loader scripts came with the sync): **35 passed** in 1 min 37 s.
   `manage.py check`: no issue; `makemigrations --check --dry-run`: no changes; `ruff check .`: clean. On design-v5
   after the merge (`2ebfed1`, its tree the branch's): both bundle-currency tests, the checker's test and
   `test_design_docs` — 105 passed; `manage.py check`: no issue; `--validate` and `regen_design_inventory.py`: current.
10. **The record, and what is not done here, on purpose.** Merged with `--no-ff` (`2ebfed1`); design-v5's tree is the
   branch's, nothing rebuilt (the bundles design-v5's byte for byte). No tag — the next checkpoint's tag carries the fix
   to the preview; no restart of 8780; no change to v5-live; no push; no line in `CHANGELOG_V54.md` or
   `live_status.json` (not a preview surface — DL54-77, DL54-121, DL54-130). **main** (the V4 line) is the merge brief's
   next step, after the lock: a `cherry-pick -x` of Part A's eleven commits (`0168c4b`, `ef1d545`, `b955215`, `949074b`,
   `5020315`, `83634d4`, `fa172e1`, `f140de6`, `e55d5e6`, `d5b0ae1`, `659be72`; not Part B's `290c5ae` and `045fad3`,
   not the notes, the manifest or this entry), kept only if it applies cleanly and main's `apps/cases` and
   `tests/security` pass, aborted otherwise — the release comes from design-v5 either way. A dry run in a throwaway
   worktree of main (removed) applies the first three and stops at `949074b`: its test module rewrites a comment that
   the notes commit `9a9bb5c` had corrected; the outcome is logged in `evidence/v54/sec-f7/merge/main_cherry_pick.log`.
11. **The owner's questions** (NOTES §5 and «Review fixes»; none blocks the merge, each a decision, not a fix):
   - **Q1** — the five rows the graph declares and §4 does not, and SUSPENDED → any state but the one it left, are
     nobody's now: a file in ADMIN_PROCESS that needs a professional review cannot go back to REVIEW_REQUIRED. Either §4
     gains these rows with their actors, or the graph loses them;
   - **`BEYOND_SECTION_4`'s two departures** — SELECTION → TRAINING (the authorised actor's conclusion without a
     referral, and the administrator's way out of a selection that can no longer be concluded) and ENTERED → POST_ENTRY
     (the administrator): to confirm, §4 gaining them, or to remove;
   - **Q2** — the training body, named by §4 on ORIENTED → TRAINING, refused «change» by the policy: a training
     service's path like the authorised actor's, or §4 corrected; **Q3** — the authorised actor acts through the
     selection process only, never the case page (§4 could say «tramite il processo di selezione»);
   - **Q4** — «superiore» read as the administrator alone: an operator does not lift a person's own suspension, nor a
     colleague's; **Q5** — ENTERED → POST_ENTRY, «sistema — automatica», has no performer: chain it on the recorded
     entry, or name the operator; **Q6** — §4's «con motivazione» on the way back from SUSPENDED is not asked;
   - **Q7, Q8** — the professional no longer suspends or closes a file, the operator closes from POST_ENTRY only (both
     follow §4; confirm); **Q9** — an administrator who owns a file acts on it as its owner (kept);
   - **Q11, Q12** (pre-existing) — a suspended file's owner who takes the questionnaire again opens a second file (the
     dashboard no longer offers it, the questionnaire's own entry still does); `conclude` revokes only the concluding
     operator's assignment;
   - **the words of a held file** for copy packet B1 — the four of NOTES §6 (a refusal that says what, not who; «lift my
     suspension» offered as the previous state's label; «Votre dossier» twice on the suspended panel; «pour l'instant»
     on a closed file) and the review's finding 7 (a closed file's «Mes documents» empty state promising a list; a
     suspended file's page naming a next action its panel does not);
   - **for the back-office hardening or the owner** — the policies' administrator branch ignores read-only (on a CLOSED
     file the transition view answers the administrator with the domain's refusal, the owner with 403; the checklist
     policy lets an administrator change a closed file's lines); `CaseFileAdmin` has no queryset limit (role:operator
     reads every case file in the back office, where PERMISSION_MODEL §5.1 says «assigned»); the checklist inline writes
     no `case.checklist.status` event. Q10 (the assignment inline) is done: finding 2.

   **The number**: DL54-132, design-v5's next free one; W3-E's branch numbered its entries from DL54-130 (DL54-130
   item 7) and follows this one at its sync.

**Why.** A lifecycle column that only a document holds is an interface rule, and an interface can be bypassed: the
person announced their own administrative procedure, departure and entry, and the reserved selection, and the journey
drew each as a fact. Declaring the column as data beside the graph, enforcing it where the status is written and
deriving the offered controls from the same rule closes the door and the hint together; intersecting it with the object
policy keeps the fix a narrowing. The review's two majors were the same flaw seen from the administrator and from the
back office, and fixing them before the merge keeps one rule with no second door. A held file's owner told «pas encore
de dossier» was told something false and offered a second file.

**Source.** The owner's V5.5 and V5.9; `docs/platform/CASE_LIFECYCLE.md` §4 (the «Chi può» column, rules 1–5) and CR-03;
W3-D's review (F-7 and the dashboard item); DL54-01 (the ref names); DL54-77 (a merge that is not a preview surface);
DL54-121 and DL54-130 (families outside the waves); DL54-129, DL54-131 (the shared payload); plan §2.2 (a file not in
the manifest has no writer until the steward assigns it); `QA/v54/sec-f7/NOTES.md` (with «Review fixes» and «At the
merge»), `REVIEW.md`; the ownership checks, the scan, the weight and the test logs in
`C:/tmp/ile_v5_council/evidence/v54/sec-f7/merge/`.

## DL54-133 · 15 October 2026 · W3-E: the person's registers on one grammar

**Decision.** «Mes échéances», «Communications», «Mes demandes», «Mon parcours» and their records (the communication,
the request) are drawn on what the platform families shipped, as one grammar with the dashboard and «Mes pièces»:
- **the head** is W3-A's workspace head (`.ws-head`): the title and its line of context; **no eyebrow** («Espace réservé»
  repeated the level the breadcrumb gives — C-4, W3-A's note); a record's own words as its title (a subject, a request)
  isolated in their direction (`dir="auto"`) and hugging their box on the reading edge (DL54-64's rule);
- **the band** is the dashboard's ledger line (`.db-ledger`) under the head: the register's count, the figure at 20/28
  and 500 (never a stat card's numeral), in the bridge's own live words; each event counted once — a late date is
  counted «en retard», not also «à venir»; «Communications» keeps its sentence, the page's one live region;
- **the rows** are the dashboard's row (`.db-task`) with the registers' columns — the words · the state as a chip ·
  the date; a communication: its seal · its words · its act —, the first line of every cell on the title's (baseline);
- **the whole row is the way to its record** (the requests, the communications): the title's link stretched over the
  row (z 1), the row's act above it (z 2) — W3-C's row (DL54-110);
- **the date** is the dashboard's (`.db-due`, the glyph of its register); **its distance in words is not drawn**: no
  live string says «dans 9 jours» or «en retard de 3 jours» (B1 item 4) — the chip says late or near;
- **«Non lue»** is a word with the ink dot and the heavier weight, never a colour; the count of the unread event is
  said once on the page (the band) — the rail's «Communications (n)» is W3-A's;
- the sections under the dashboard's head (`.db-h2`) with their domain glyph.
What only these pages draw is a page-only sheet (`portal/registers.css` → `v5/_registers.css`, linked by the six
templates); everything else is reused from the console's shared partials.

**Measured** (lane 8785, fr / ar × 1440, 1280, 390, 360): 0 overflow, 0 CSP, 0 console error, one h1, ≤ 3 corners a
first viewport, no shadow, no uppercase label; 0 dead points in 180 probes of the linked rows; text under 14 px at 390:
0 %. The swap test passes on every screen (DL54-136).

**Source.** Plan §3.5 item 7, §1.2, §1.18 D17; the platform map §3 («Requests, messages, deadlines, pathways, detail
pages»); DL54-64, DL54-78, DL54-110; `QA/v54/w3-e/NOTES.md` step 1.

## DL54-134 · 15 October 2026 · W3-E: three producers in the chip registry; an archived request and a cancelled date carry nothing

**Decision.** The person's registers draw every state through the `{% chip %}` pair, the register from the member:
`core.chips` gains `enquiries.SubmissionStatus` (new neutro · in_progress esame · handled conforme · archived nullo),
`forum.RegistrationStatus` (pending «Reçue» esame — the Forum's team confirms it — · confirmed conforme · cancelled
nullo · attended conforme) and `portal.DeadlineStatus` (open attesa · done conforme · cancelled nullo), their enums in
`test_chips_registry.PRODUCERS`. A computed state is a literal register (a late date azione, a near one attesa).
`components/badge.html` is no longer included by these pages; its last console includer is the bridge's
`portal/partials/card.html`, which moves with the bridge pages (step 2).

**Why.** The registry's own rule: the register is the member's, never the word's. Through `badge.html`'s legacy kinds an
archived request and a cancelled date went out as `neutral` — neutro, «a fact is recorded» —, where nullo is «withdrawn,
not applicable, archived: it carries nothing».

**Source.** Plan §1.2; DL54-52, DL54-53; `apps/core/chips.py`; `tests/frontend/test_chips_registry.py`,
`test_state_chips_carry_a_register.py`.

## DL54-135 · 15 October 2026 · W3-E: the empty state is design V5's component

**Decision.** `components.css` §23 (W3-E's section of the deletion map) draws DS V5 §10.8's «EmptyState (page)» for
every page that includes `components/empty_state.html`: the domain's glyph in its 40 px toned disc, the title at 20/28
and 600, one sentence, one action, on the reading edge under a hairline; no dashed box, nothing centred (on V5 a broken
edge is the register of what is due); under forced colours the disc keeps a 1 px outline (W1-B's hand-off, DL54-34).
V4's box leaves `v4/workspace.css`. On the console the empty state spans the main column (W3-B's `.portal__main
.empty-state` kept): its hairline lines up with the lists'. The pages that compose it their own way (the interior's
`.lettura`, the service pages, the Forum, the home's news) keep their sheets; the home's news row and the Forum now draw
the spec's 40 px disc (V4's was 48 px) — theirs to resize in their sheets if they want it.

**Why.** Five families drew the V5 empty state in their own scope while the component kept V4's look («W3-E redraws the
component»: W1-B, W2-D, W3-F1, W3-F2); the component itself now says it, and the console's pages get it.

**Source.** Plan §2.3 (W3-E's rows); DS V5 §10.8; DL54-33, DL54-34; `QA/v54/w3-f2/NOTES.md` (the empty state is W3-E's).

## DL54-136 · 15 October 2026 · W3-E: «la lettera» — a communication is a letter, the team's mark its seal; the identity carriers named

**Decision.** One communication (`portal/message_detail.html`) is drawn as the letter it is: the team's mark —
`ile-mark`, the registry's «Équipe du projet, as an actor or a sender» — on its toned disc as the letter's seal, «L'équipe
du projet», when it came and whether it was read in words; a hairline; the text at the reading size and measure; the
record it is about. The same seal stands on every row of «Communications» (20 px, its floor). The screens with neither
the journey's rail nor a register name what says ILE on them at rest — the seal and the dot grammar (the
communications), the seal, the ledger's figures and the L2 key (the letter), «i cerchi» and the date glyphs (the
dates), the references in ILE Mono (the requests, the pre-assessments), the door with the key out of the lock (the 503)
— and pass the swap test: with the console's chrome taken away and another product's frame and face put in its place,
each still reads as ILE's (`evidence/v54/w3-e/swap/`).

**Source.** Plan §3.1 item 7, §3.5 item 7; `apps/core/icons.py` (`ile-mark`, the ACTOR map); `QA/v54/w3-e/NOTES.md`.

## DL54-137 · 15 October 2026 · W3-E: the reserved area's 503 is a page of service

**Decision.** `portal/unavailable.html` (rendered with HTTP 503 while `reserved_area_enabled` is off) is drawn in the
error pages' grammar (W3-F2, DL54-97: `cms/errori.css`, `errors/_door.html`, `errors/_way_on.html`), with nothing of its
own: the door at rest with the key out of the lock, «Espace réservé» in the label's seat where an error page names its
status, the page's own two sentences, «Retour à l'accueil», the way on and «who can help me». No new copy.

**Source.** Plan §3.5 items 2 and 7; DL54-97; CREATIVE_DIRECTION_V5 §20 (the door at rest).

## DL54-138 · 15 October 2026 · W3-E, step 1: the paths outside the slice; the CSS as measured

**Decision.** The merge step writes these into w3-e's slice:
- `apps/core/chips.py`, `tests/frontend/test_chips_registry.py` (W1-C's) — three producers and their enums (DL54-134);
- `apps/portal/static/portal/registers.css`, `apps/portal/static/portal/v5/_registers.css` — new: the person's
  registers' page-only sheet and its partial;
- `apps/portal/static/portal/portal.css` — the V4 item list (`portal-list`), the message body (`portal-message`) and
  the orientation results (`portal-result`) deleted (no other reader), one line saying where they went;
- `apps/portal/tests/test_views.py` — `test_requests_list_is_paginated` counts the rows' hook (`data-request`).

**Measured** (gzip -9, `weigh_pages.py`, design-v5 `3d5351b` → this branch): `main.css` 37 324 → 37 232 B (−92 on every
page); `portal.css` 1 935 → 1 669 B; `console.css` +12 B («Ma situation»'s act rules in `v5/_wizard.css`, which W3-D's
merge moves into the page's own sheet); the console page types 47 200 → 46 854 B (−346 on every console page); the
registers' page sheet 1 624 B (first sheet, recorded at its measured size) on its six pages.

**Source.** Plan §2.2 (the manifest), §2.3, §2.6; the owner's V5.8 and its definitive ruling (shared bundles ratchet
down; a surface's own CSS in a page-only sheet).

## DL54-139 · 15 October 2026 · W3-E: «Ma situation»'s one act is the phone's action bar

**Decision.** Below 64rem the questionnaire's act group (`.wiz__act`, `data-console-action`: the shell's O63 contract,
W3-A's `_shell.css`) is the page's bar where the four entries of the bottom bar stood, «Menu» kept at the reading end:
«Continuer» across it while stepping, the form's submit on the last question (situation.js gives the submit its role;
without script the submit is the act). «Précédent» and the position stay in the page's foot, part of the page (DL54-70).
The save of the questions answered so far waits for the last question on a phone — two acts do not hold beside «Menu»,
and the Stepper reaches the last question in one press. Above 64rem the foot's end is unchanged.

**Why.** W3-A left the foot in the page with its one act «a candidate for the action bar when the wizard is redrawn»
(DL54-70), W3-F1 handed it on; at 390 × 844 «Continuer» stood behind the bottom bar, under the first viewport — now it is
in the thumb's reach, with 48 + 61 px of chrome.

**Paths outside the slice.** `apps/portal/static/portal/v5/_wizard.css` (W3-F1's: §5's act group, away from W3-D's
hunks); `tests/frontend/test_console_phone_browser_w3_a.py` (the questionnaire's foot test, rewritten to the contract,
its intent kept) and `tests/frontend/test_console_shell_w3_a.py` (the frame's first block may be the workspace head).

**Source.** Plan §3.5 item 7; DL54-70; O63; `QA/v54/w3-a/NOTES.md`, `QA/v54/w3-f1/NOTES.md` (the hand-offs).

## DL54-140 · 15 October 2026 · W3-E, step 2: the registers' grammar draws the organisations' and the other spaces' pages

**Decision.** The console's secondary pages beyond the person's — the guichet (the person's requests, a request,
opening one, the professional's queue, the dispatch desk), the Academy (the catalogue, «Mes formations», a course, a
follow-up, a plan), the selection (the workspace, a process, the person's panel, the identity communicated), the
company's pages beyond its dashboard and the Forum permanent's governance — are drawn in step 1's register grammar: the
workspace head with no eyebrow (C-4) and, at its reading end, the page's one act; the band; the dashboard's row with
the state as a chip and the whole row as the way to its record; facts on hairlines; empty regions as one line (the
dashboards' `db-empty`). Six devices join the same partial (`v5/_registers.css` §9–§14): **the clause** (what a record
is not, after a hairline — V1's `.note`), **a sequence of steps and the log** (each its place in ILE Mono; the current
step `aria-current="step"`), **the exchange** (each turn headed by a function, its actor's glyph through the registry's
ACTOR map, a date and its kind; the professional's note on the area's ground), **the answerable party** (its actor's
glyph, role, name, facts and clause, flat between two hairlines), **the form of an act** (a title, a sentence, W1-C's
fields) and **the filter** (the register's counts as links on a hairline, the tabs' one indicator). One page-only
sheet, `portal/registers.css`, for every page of the grammar (cached once across ≈ 40 pages); a module's own sheet only
for what it draws beyond. `.reg-page` is one `minmax(0, 1fr)` column — a wide child overflows inside itself. The
console's `.data-table` (`portal.css`; these pages are its readers) loses its tracked capitals, navy rule and display
serif; every console table scrolls by the same rules.

**Why.** The platform map's «Requests, messages, deadlines, pathways, detail pages» answer holds for the modules: their
V1 grammar (folio ordinals, register entries with arrows, the green sequence, the band on the process ground, the
forms' capitals) was the hybrid «V4 + fondation» on screens a person, a company and a partner use every week. One
grammar, drawn once: the second family to draw a component consolidates (V5.8).

**Measured.** 192 drawings (48 page types × fr / ar × 1440 / 390): ≤ 3 corners a first viewport (≤ 2 on the area's
pages), 0 raised panel and 0 shadow, 0 CSP, 0 console error, one h1, no eyebrow, no capitals, no animation at load, 0 %
text under 14 px at 390; 0 overflow at 320–430 (clipped content counted); forced colours and reduced motion drawn.

**Source.** Plan §3.5 item 7, §3.1 item 7, §1.3, §1.4; the platform map §3; DL54-133; `QA/v54/w3-e/NOTES.md` step 2.

## DL54-141 · 15 October 2026 · W3-E, step 2: the company's register — its counts are its filter

**Decision.** «Mes besoins en compétences» draws the register's counts **as its filter** (E-3): «Tous» and the
dashboard's own groups by who holds a need — À faire, En cours, Clos (W3-B's grouping, extracted as
`portal.services._need_groups`; `needs_register` gives the filter and the chosen group's rows; the companies' view asks
it) —, each its count and the marks of its states coloured by the group (O62), a group with no need a word, `?état=`
in the URL. The needs' rows are the dashboard's needs columns with the whole row as the way to the need. **The V1
company band leaves every page**: each page draws its own subject (the register, a need with its reference, state and
acts, «Mon entreprise», a form), the space is the rail's (one rail per space, W3-A — S-5); the partial is deleted and the
dashboard links no module sheet. **No chart** (E-4): none was drawn; the analysis stays a table of counts. The
declaration draws one h1.

**Why.** Four count tiles were V4's answer and «the counts become the needs table's filter, not tiles» is the platform
map's; the band repeated an identity the rail and the dashboard already say.

**Source.** The platform map §3 (the company: E-3, E-4, S-5); DL54-79 (the company's dashboard); W3-A NOTES (the two
h1).

## DL54-142 · 15 October 2026 · W3-E, step 2: the bridge's states through their producers; the audience glyph

**Decision.** The bridge's registers (`portal/partials/card.html`) draw every state with the `{% chip %}` pair: a
request's member (its producer named by the item), a scan's member (its chip word, as on the person's dashboard), a
date's urgency as a literal register (azione late, attesa close by), the head's late dates azione and its unread count
neutro. A communication not yet read is the person's dashboard's grammar — the ink dot, the weight, «Non lue» —, never
a chip; a membership's role is a fact of the row's line. `components/badge.html` is **retired on console pages** (the
dev showcase is its one includer). «Mon organisation» draws the account's **audience glyph** — `institution`,
`university`, `building` for a company (the registry's AUDIENCE) — where it drew the company's building for everyone.

**Why.** The registry's rule (the register is the member's, never a legacy kind's) and the platform map's «distinct
audience glyphs: institution ≠ university ≠ building ≠ person».

**Source.** Plan §1.2; the platform map §3 (institution and university); DL54-80, DL54-134.

## DL54-143 · 15 October 2026 · W3-E, step 2: a section head's glyph holds at its size; the Forum's closed page

**Decision.** A section head (`.db-h2`, 16 px) carries a glyph only where the registry names the section's concept
and the symbol holds at 16 px: `book-open`, `inbox`, `list-ordered`, `pen-line`, `file-plus`, `map`, `building`,
`history`, `briefcase`. `concierge-bell`, `wrench`, `settings`, `calendar-range` (floor 20) and `handshake` (24) are
not drawn smaller than they hold: those heads carry their words alone. The Forum permanent's closed module (503, G11)
is drawn as the reserved area's twin, in the error pages' grammar — the door at rest with the key out, «Forum
permanent» in the label's seat, «pas encore ouvert».

**Why.** The icon system's floors (plan §1.7) are measured: a glyph below its floor reads as a smudge.

**Source.** Plan §1.7; `apps/core/icons.py` (MIN_SIZE); DL54-137; W3-F2's error pages.

## DL54-144 · 15 October 2026 · W3-E, step 2: the paths outside the slice; the CSS as measured; the staff's debt

**Paths outside the slice** (for the merge step's manifest): `apps/portal/static/portal/portal.css` (the console's
table on V5, the scroll rules from `selection.css`, four dead rules and the V1 sequence's current step deleted);
`templates/portal/partials/card.html` (W3-B's: the states through their producers, the unread grammar, the
organisation's glyph — the retirement of `badge.html` on console pages is W3-E's per §3.5 item 7); `apps/portal/services.py`
beyond its secondary pages' presenters (the bridge's card presenters; `_company_needs` split into `_need_groups`, output
unchanged); `apps/companies/views.py` (the needs register's filter, two lines); `apps/helpdesk/tests/test_views.py` (two
pins retargeted, intent kept).

**Measured** (gzip -9, mtime 0; step 1 `d912f9a` → step 2): `main.css` 37 232 B (flat); the console page types
46 854 → 46 689 B (−165 on every console page); `portal/registers.css` 1 624 → 2 593 B; `helpdesk.css` 875 → 262,
`academy.css` 618 → 192, `selection.css` 1 085 → 463, `companies.css` 873 → 189 B; a module's page type +1.6 to +2.4 KB (it
loads the one grammar's sheet instead of its V1 module sheet), the company's dashboard −1 038 B (no module sheet).

**Design debt.** The staff and back-office pages are drawn with the console's chrome only (the dispatch desk, the
analysis; the Django admin untouched): their working screens — density, saved views, the staff's filter bars — are not
redesigned in V5.4.

**Source.** Plan §2.2, §2.3, §2.6; the owner's V5.8 and its definitive ruling; the platform map §3 («Staff and
back-office»); `QA/v54/w3-e/NOTES.md` step 2.

## DL54-145 · 16 October 2026 · W3-E, step 3: the case file in design V5

**Decision.** `templates/cases/detail.html` is composed — never a new component family — on what the platform families
shipped, in the order of a file's five questions, the DOM's order too: **the head** (W3-A's ContextHeader: «Dossier» and
the reference in ILE Mono, the objective, the state as a chip and since when — the title says the level, **no eyebrow
repeating it**, C-4; no action: the page's one primary is the NowPanel's); **1 · where am I** — W3-D's journey,
descriptive; **2 · what next** — W3-B's NowPanel, the screen's one raised plane, over the same one next action as the
dashboard and the documents (T1, `portal.services.case_now_panel`): a checklist line has no page of its own, so its act
leads to the line's row on this page (`#line-<pk>`); a mandated reader (a professional, an operator, an administrator)
is told the file's next step in nobody's voice — «Prochaine étape», whose it is in the facts, no primary, a piece still
readable («Consulter»); no account date takes it over here (the takeover is the dashboard's); below 64rem its primary
is the page's action bar (`data-file-action-bar`, the shell's O63 contract) and is not drawn twice; **3 · what is
asked** — «Exigences», the checklist as **the register's rows**, never a table (C-3): the dashboard's row in four
columns (the line, who answers for it — a fact every line states —, what the team wrote, the source in ILE Mono; the
state as a chip; the date with its glyph and word while the line is open; the line's menu), the line a piece satisfies
the way to that piece; then «Pièces du dossier» — the dashboard's «il registro» and every piece the reader may read in
the register's order (the register's own presenter and authorisation), the row the way to the piece, its act where the
reader acts, the NowPanel's piece drawn there only; **4 · who intervenes** — each live mandate as the registers'
answerable party (the role's glyph through the registry, the role and its organisation, the authorisation in ILE Mono,
until when); **5 · what changed** — beside from 80rem, under before: the timeline (W3-D), the pre-assessment, and for
the person only their communications and dates (a mandated reader's own inbox is not shown on somebody else's file).
Two columns from 80rem (the file 2/3, what changed 1/3, no inner scroll: W3-D's O1 is gone with the inspector); one
column before.

**Why.** The platform map's answer for the case file («compose it first: journey, NowPanel, the checklist as register
rows (C-3), the people, the feed»); the V4 page was a panel board — five raised panels, the next step without its act,
a five-column table with a select and a button on every row, an inspector that scrolled inside itself. The reference
case (`EE167596D4`) holds three pieces and no checklist line: the V4 page told its person «Aucune pièce n'est encore
demandée» — the case file now draws the pieces it asks for.

**Source.** Plan §3.5 item 7, §1.15; the platform map §3 «Case file»; the UI-UX audit C-1 … C-8; DL54-81 … DL54-86
(W3-B); DL54-122 … DL54-128 (W3-D); DL54-140; `QA/v54/w3-e/NOTES.md` step 3.

## DL54-146 · 16 October 2026 · W3-E, step 3: the state changes — the row menu and the alert dialog (C-5, C-6)

**Decision.** A line the reader may move — the object policy, asked per line by the view; the POST asks again — offers
its **row menu**: «⋮», a real button, the overlay system's popover, named «Actions» and described by the line (W-3), with
one item, «Nouvel état de cette ligne», a link to the line's **alert dialog** (W2-A's `kind="alert"`, `role=alertdialog`,
the 40 px disc of a consequence): the line in its own language and its state as a chip; **the consequence named** —
«Seules les évolutions permises par l'état actuel sont proposées. Chaque changement est enregistré.» (the dialog's
description); the states it may move to as radios with their chips — the current one is not offered, so a press never
records a change that changes nothing; **«Annuler» the safe default** — it takes the focus, Esc presses it, the scrim
never closes the dialog —, then «Mettre à jour». **The focus returns** to the row's «⋮» when the dialog closes
(`static/js/src/console.js` §2f opens the dialog with the trigger as its opener, the dialog first and then the menu's
close: closed first, the menu gave the focus to «⋮», whose top-layer tip opened inside the menu's own close). After the
POST the page returns to the row (`#line-<pk>`, `scroll-margin`), which takes the focus, and the status region says
what changed. **The file's state**: one act («Nouvel état») opening the same dialog family — the moves the domain
permits this reader (`transitions_available`), none chosen in advance; under the closure its consequence («Un dossier
clôturé ne se rouvre pas : on en ouvre un nouveau.», the domain's own sentence); «Motif» with its rule as the field's
help, tied to it (C-6: a condition never in the label alone). No bulk edit: each change of a legal checklist is one
audited act with its author. Without script every item and opener is a link that shows its dialog in place.

**Why.** C-5 rejected the bulk edit and adopted the rest; W2-A handed over «the staff consequence dialogs on the modal».
The permissions, the state machine, the audit trail and the object-permission checks are unchanged — presenter changes
and the line's redirect only.

**Measured.** In headless Chromium, fr 1440 and ar 390: the menu opens on Enter with the focus on its item; the dialog
opens as an alertdialog, `aria-modal`, described, the focus on «Annuler»; ten Tabs stay inside; Esc closes it and the
focus is back on «⋮»; a press on the scrim leaves it open; the POST lands on `#line-<pk>` with the focus on the row and
«La ligne a été mise à jour.» in the status region; the file's dialog the same, the closure's consequence tied; without
script the dialog shows in place; 0 console errors, 0 duplicate ids.

**Source.** Plan §1.14; W2-A CONTRACT §1–§6; the platform map C-5, C-6; `QA/v54/w3-e/NOTES.md` step 3.

## DL54-147 · 16 October 2026 · W3-E, step 3: v4/workspace.css leaves the cascade

**Decision.** The deletion map's last row («the rest of v4/workspace.css — the file», W3-E's): the sheet and its import
line leave `main.css`. What other console pages still drew of it — the ContextHeader (the dashboards' and the case file's
head), the workspace head of the secondary pages, the actor's glyph disc, the frame's focus ring — moves **with its
values unchanged** to the console partial `apps/portal/static/portal/v5/_frame.css`, imported last by `console.css`: the
shell's rules on the heads are the frame's own and more specific, its focus rules are the chrome's, the dashboards write
none, and no `main.css` rule of equal weight reaches the frame (checked) — no tie changes hands. Everything else left
with the V4 case file (Panel and its gradient edge, the meter and `notch-fill`, the ResponsibilityBar, the HealthStrip
and `strip-fill` — the case file moves nothing at load —, the dates and threads lists, the compact context bar and its
script, the V4 table, the intervenants, the state form, the file bar); `components/health_strip.html` with its last
consumer. No page drew the V4 case band or the shell's next action any more: their partials leave, the shell's two
blocks stay empty, `portal.css` sheds their rules and the pre-assessment's V1 section rhythm, title and folio counter.
The V1 devices these pages were the last to draw leave `main.css` (grep-proved on design-v5 and the in-flight branches:
every other user is a W3-E template already redrawn): the folio, the entry's ordinal and responsible actor, the night
verso. `--rubric-on-navy`, `--t-numeral-size`, `--t-numeral-lh` lose their last consumer: reserves (DS 2026 §3).

**Why.** «Delete what you supersede» (plan §2.1); the V5.8 ruling: the shared bundles ratchet down, a family that draws
pays with deletions.

**Source.** Plan §2.1, §2.3; V5.8 «definitive ruling»; W3-B NOTES (Panel, ContextHeader, HealthStrip «leave with their
last consumers»); W3-C NOTES (the case band); W3-D NOTES (`strip-fill`); step 2's notes (`portal-section`, the folio
counter).

## DL54-148 · 16 October 2026 · W3-E, step 3: «Mes dossiers», the pre-assessment, «Ma situation»'s one total

**Decision.** «Mes dossiers» (`templates/cases/index.html`) and the case's pre-assessment (`templates/cases/assessment.html`)
are drawn in the registers' grammar: the workspace head without an eyebrow; the rows (the file's objective and reference,
whose it is, its count in words, its late lines in the dates' grammar, its state as a chip, since when — the whole row
the way to the file); the pre-assessment's head says its file once on its line of facts (no V4 band), the outcome at the
console's scale with its rules version, date and clause, the rules applied as the registers' sequence in their order of
application, the requirements found missing, the sources, the replay **on the page's own ground** — V1's night verso, in
which its text stood at 1.06 : 1 (W3-F1's finding O4), is gone —, a divergence said as a warning; the demonstration
notice still precedes the outcome. «Ma situation» counts one total: the counter under the Stepper counts the questions
the page asks and the ones answered (it said «sur 7» — the fields the rules read — under eight nodes and «1 / 8»; W3-D's
m4).

**Source.** Plan §3.5 item 7; DL54-140; W3-F1 NOTES l.304; W3-D NOTES «Handed to» (m4).

## DL54-149 · 16 October 2026 · W3-E, step 3: the paths outside the slice; the CSS as measured; the load check

**Paths outside the slice** (for the merge step's manifest): `apps/cases/views.py` (the detail's context — presenter
reads — and the line's redirect to its row; W3-B's slice is the two `reader=` arguments, kept); `apps/cases/presenters.py`
(the dead `checklist_health` out; W3-D's two functions untouched); `apps/portal/views.py` («Ma situation»'s one total);
`apps/portal/static/portal/portal.css` (the case band's, the next action's and the pre-assessment's dead rules);
`apps/portal/static/portal/v5/_frame.css` and `case.css`, `v5/_case.css` (new: the frame's console partial; the case
file's page-only sheet); `static/js/src/console.js` (§2f, the row menu's dialog opener — a second import line keeps
W2-A's and W3-A's pinned one —, §2c's dead compact bar out); `templates/portal/base_portal.html` (W3-A's: the two
blocks empty); `templates/portal/partials/{case_header,next_action}.html` (deleted: «the portal list partials»);
`templates/components/health_strip.html` (deleted) and `templates/dev/showcase.html` (its sample; W3-D's four-line
comment a block comment — design-v5's own red in `test_template_comments_do_not_leak`); `static/css/register.css`,
`base.css`, `layout.css` (the V1 devices left without a reader); `apps/portal/tests/test_situation.py` (the one total's
test, added); tests retargeted, intent kept —
`tests/frontend/test_dashboard_w3_b.py`, `test_depot_w3_c.py`, `test_documents_w3_c.py`, `test_journey_w3_d.py`,
`test_overlays.py`, `tests/i18n/test_rtl_static.py`; DS 2026 (§2.1's rows, §3's three reserves, §8.2's note, §10's
glyph / form_field / page_header lines and health_strip's section, §11.10, §12's note).

**Measured** (gzip -9, mtime 0, the stewards' `weigh_pages.py`; design-v5 `fec37d3` · this branch before step 3
`7f7ca9a` → after): `main.css` 35 483 · 35 290 → **31 906 B** (−3 384 on every page in this step); the console page
types 44 196 · 43 572 → **40 140 B** (−3 432 on every console page); every page type lighter but the case file where it
draws its dialogs. The case file — at design-v5 «a journey page» (46 617 B), 45 993 B before this step — **45 968 B**
where it draws no dialog (shared + the registers' sheet + `portal/case.css` 814 B + the journey's), **48 039 B** where
it draws its dialogs (+ W2-A's page-only panels, 2 071 B: what the overlay system asks of a page that draws a dialog),
recorded at its first own sheet; «Mes dossiers» and the pre-assessment 43 572 → 42 733 B (44 196 on design-v5; the
shared sheets alone, then with the registers' sheet). **The load check** (V5.8 rule 2; the lane, the tree before this
step on a twin port, interleaved blocks, cache disabled, CPU × 4, n = 5, medians): LCP 604 → 536 ms (person, fr 1440),
424 → 548 (fr 412), 508 → 516 (professional, ar 1440), signs mixed within the machine's spread; FCP +20 to +44 ms (three
more stylesheets, uncompressed on the dev server); CLS ≤ 0.0005; no meaningful regression.

**Source.** Plan §2.2, §2.6; V5.8 «definitive ruling»; DL54-87; `QA/v54/w3-e/NOTES.md` step 3.

## DL54-150 · 16 October 2026 · W3-E, the fix pass: the case file's first screen, its one line, its voice; the closures

**Decision.**
- **The case file's journey is drawn compact** — W3-D's own forms, the dashboard's and «Mon parcours»'s: the level line
  where its column holds 56rem, else the card (what is true now, the step's rank, «Vous êtes ici») and the spine behind
  the disclosure, closed — «Où j'en suis» for the person, «Parcours» for a mandated reader (nobody's voice). The dated
  spine (`descriptive`) was 460–521 px tall and pushed the NowPanel out of the first screen (LA-9): the NowPanel's
  title now stands at y 464 and its act at 657–701 at 1366 × 768 (762 and 895 before), its title at y 428 at 360 × 800,
  clear of the phone's bar (top 739). The dated history is the feed's («Où en est votre demande»). DL54-145's
  «descriptive» is superseded; the component keeps the variant (W3-D's), which no page draws now.
- **The NowPanel's checklist line is drawn once.** «Exigences» skips it, as «Pièces du dossier» skips the NowPanel's
  piece (W3-B's rule); the count «n sur m» stays the file's. The panel carries what the row said — the team's note
  beside who answers, the source in ILE Mono («Fondement») — and its wrapper keeps the line's id (`#line-<pk>`: the
  line's POST and its dialog's «Fermer» return there). Its act is the line's own, «Nouvel état de cette ligne», which
  opens the line's alert dialog (the overlay system's opener, no arrow: it goes nowhere): the person's primary — and
  the phone's action bar —, a mandated reader's quiet secondary where the policy lets them move the line, nothing where
  it does not. No «Continuer» that only scrolled to a copy whose act hid behind «⋮».
- **The history's voice**: `cases.presenters.timeline(case, reader=…)` says «Vous» for the person's acts to the person
  only and «La personne» (`ResponsibleActor.PERSON`) to anybody else; a line's change names the line in its own words,
  its direction its own; in the side column the date heads its event, which takes the column's width (a long state's
  chip no longer breaks in two).
- **The family's irreversible closures are the case file's alert dialog** (plan §1.14 «staff consequence dialogs on the
  modal»): the guichet's «Clore la demande» for the person and the appointed professional, the selection's «Clore le
  processus» for the authorised actor — one act on the page, the consequence said before it (the domain's sentence, the
  dialog's description), the reason (or the outcome, never chosen in advance, and the note) inside, «Annuler» the safe
  answer that takes the focus (Esc presses it, the scrim never closes it), the act in the garnet outline; the page links
  W2-A's page-only panels where it draws one. One dialog body for the family's acts (`.reg-dialog`, the registers'
  sheet). The selection's evidence table (a select and «Mettre à jour» a row) is recorded as the staff's design debt.
- **A held file's NowPanel** (sec-f7's variants, on design-v5): on the file's own page it never offers the way to that
  page, keeps the person's act for the person, and does not address a mandated reader as the owner; the page's own
  suspension notice is drawn only when the NowPanel does not draw the reason — one reason, drawn once (DS 2026 §11.7).
- **The registers' grammar**: a line of facts never ends or opens on its point (each part opens with it, the line clips
  the one that would open it); the filter is one row that scrolls under 52rem; a title in the other direction than the
  page stands on the page's reading edge wrapped or not (`:dir()`, DL54-64); a section's sentence and its sources hold
  the reading measure; a head's acts take the line on a phone (WCAG 1.4.10: a draft need scrolled sideways at 320–375);
  a row link's ring keeps its room under forced colours; the row menu is the system's icon control (40 / 44 px) in a
  column of its own at the row's end; a training plan's state is a chip through its producer (`academy.PlanStatus`);
  the guichet's opening form carries the person's seal beside its promise, the pre-assessment's outcome its journey
  phase's glyph (plan §3.1 item 7).

**Measured** (gzip -9, mtime 0): the shared bundles unchanged — `main.css` 31 906 B, main + console + portal 40 140 B
on every console page; the registers' sheet 2 593 → 2 875 B, the case file's 814 → 955 B (page-only); the case file
45 968 → 46 391 B, 48 039 → 48 462 B where it draws its dialogs; the guichet's request and the selection's process add
W2-A's panels (2 071 B, one request) where they draw the closure. Nothing moves at load; 0 CSP report, 0 console error,
0 horizontal overflow on the fix pass's loads.

**Source.** `QA/v54/w3-e/REVIEW.md`, `A11Y_PERF.md`; `QA/v54/w3-e/NOTES.md` «Review fixes».

## DL54-151 · 16 October 2026 · Steward, the w3-e merge: the family's eighteen entries renumbered, the 33 paths assigned and two slices named as written, one test retargeted where sec-f7 met the case file, the shared CSS gate passed with `main.css` 3 577 B lighter on every page and the console page types 4 056 B lighter, every ceiling lowered to the merged weight, the area's page types recorded through their own sheets, nineteen surfaces V5

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w3-e` into design-v5 on 16 October 2026 —
what the family's entries and notes hand to the merge step: DL54-138, DL54-144, DL54-149, DL54-150;
`QA/v54/w3-e/NOTES.md` «Paths outside the slice» (steps 1–3 and the fix pass), «Left, and for others» and «Handed
on»; `QA/v54/w3-e/REVIEW.md` «For the merge step» and `A11Y_PERF.md`, both SHIP_AFTER_FIXES).

1. **The order and the numbering.** The plan's order (§3.5 item 7: W3-E after W3-C and W3-D) was met: `v54/w3-d` has
   stood on design-v5 since 15 October. The steward took `DESIGN_V5_MERGE_LOCK` at 05:41:42 with design-v5 at
   `11070b5` (the private-root probe's test, after the sec-f7 merge). The branch's merge base was `fec37d3` (W3-D's
   shipped note); design-v5 had since recorded the sec-f5 merge (DL54-130), integration checkpoint 3 (DL54-131) and
   the sec-f7 merge (DL54-132), so the steward's sync (`dcf11a2`, 63 commits) gave the family's eighteen entries
   **DL54-133 … DL54-150** (add 3: their headings, their index rows and their cross-references between the eighteen —
   every DL54-130 … DL54-147 in their text was the family's own; the code, the tests, DS 2026 and the manifest cite
   none of them). Checked after the resolution: the log without the family's rows and block is design-v5's byte for
   byte, and the family's block and rows with their numbers shifted back are the branch's. The notes and the review
   keep the numbers they were written with; the notes' closing section gives the mapping. This entry is DL54-151.
2. **Both areas kept.** The sync wrote two conflicts: the decision log (item 1) and `static/js/dist` (`merge=binary`):
   both dist trees deleted and rebuilt (`npm run build`) on the merged sources — the CSS byte for byte the branch's,
   the JS the merged sources' (intfix's `overlay.js`, `overlay/extras.js` and `shell.js` with the family's
   `console.js`), the chunks' names following the worktree. `apps/portal/services.py` (sec-f7's `held_case`,
   `now_panel`'s held variants and `_held_now` beside the family's `case_now_panel`, which reads them — its review's
   minor 11, prepared before the merge), DS 2026 (sec-f7's §11.7 beside the family's §11.10, which already said the held
   file's NowPanel draws the reason once) and the design showcase (the same comment fix on both sides) merged on their
   own and were read. Where the two areas meet, the steward wrote two lines (`398590e`): `_held_now`'s docstring named
   the V4 case band the family deleted (`portal/partials/case_header.html`) — it names the case file's page now —, and
   `HELD_NOW_VARIANTS` reads sec-f7's two constants (the values unchanged). The targeted run found the one semantic
   conflict (`ab0a79a`): sec-f7's `apps/cases/tests/test_transition_actors.py` read the moves the case page offers as
   V4's select options; the family's case file draws them as the radios of the file's state dialog (C-5) — so ten
   cases of `test_the_case_page_offers_exactly_what_its_view_accepts` failed (the page «offered» nothing), and
   `test_the_administrator_neither_opens_nor_concludes_a_selection_from_the_case_page`'s absence check would have passed
   on nothing. Both now read the dialog's form (`_moves_on_the_page`, the radios named `status` in `#file-state-form`;
   a checklist line's dialog names its radios `status` too), and the second asserts the closure is offered beside the
   absent move: intent kept, nothing weakened; the file stays sec-f7's (a slice in the manifest, item 3).
3. **The 33 paths outside the slice are this area's in the manifest** (`c8859fc`), and the merge's one retargeted test
   (`6518c78`). `scripts/check_ownership.py w3-e design-v5` listed exactly the paths the family declares (steps 1–3
   and the fix pass: DL54-138, DL54-144, DL54-149, DL54-150); each was read in the diff and found to be what it
   declares. Whole files: the family's five new sheets — the page-only entries `portal/registers.css` and
   `portal/case.css`, their partials `v5/_registers.css` and `v5/_case.css`, and the console partial `v5/_frame.css`
   (what other console pages still drew of `v4/workspace.css`, moved unchanged) — and
   `templates/components/health_strip.html`, retired with its last consumer. Twenty-seven slices, each naming what was
   written and whose file it stays: the case module's (`cases/presenters.py`'s `timeline(reader=…)`, `cases/views.py`'s
   `detail()` and the line's redirect), the companies' `needs()` filter, W1-C's four producers and their test, the
   portal's `situation()` total and two of its tests, two of the help desk's tests (no family held them), `portal.css`'s
   V5 table and its dead rules, W3-F1's `_wizard.css` §5, W4-D's three V1 sheets (`base.css`, `layout.css`,
   `register.css` — the devices these pages were the last to draw), W3-A's `console.js` (§2f in, §2c out), W3-D's
   `case_timeline.html`, the showcase's HealthStrip sample, and ten test files retargeted with their intent kept (W3-A's
   two, W3-B's, W3-C's two, W3-D's two, W2-A's, W1-A's RTL scanner). Two of the family's slices named as written
   (`apps/portal/services.py`: the secondary pages' and the case file's presenters, the bridge's cards, W3-B's
   `_need_groups`, and the steward's merge line in sec-f7's docstring; DS 2026: §2.1's rows, §3's three reserves, §8.2,
   §10, §11.10, §12). The check after it: 69 inside, 41 slice, 32 generated, and the manifest itself, the one steward-only path (before: 33 outside); `--validate`: coherent, 29 families, 730 entries.
4. **The shared CSS gate (the owner's V5.8 and the orchestrator's definitive ruling of 12 October, 02:15) passes: both
   shared bundles fall.** On the bundles rebuilt from a clean `static/css/dist` and `static/js/dist`,
   `gzip.compress(data, 9, mtime=0)`, each page type with the sheets its templates link on each side
   (`evidence/v54/w3-e/merge/budget_gate_branch.log`, and `budget_gate_merged.log` on design-v5 after the merge):

   | Page type | design-v5 `11070b5` | merged | change | ceiling before → after |
   |---|---|---|---|---|
   | every page, and an interior page with no sheet of its own (`main.css`) | 35 483 | 31 906 | −3 577 | 35 483 → **31 906** |
   | console page types (`main` + `console` + `portal`) — the company's dashboard among them now | 44 196 | 40 140 | −4 056 | 44 196 → **40 140** |
   | **the case file** (+ `portal/registers.css`, `portal/case.css`, `portal/journey.css`) | 46 617 | 46 391 | −226 | 46 617 → **46 391** |
   | **the case file where it draws its dialogs** (+ `core/overlay-panels.css`) | 46 617 | 48 462 | +1 845 | — → **48 462** (recorded, item 6) |
   | **a register page** — «Mes dossiers», the pre-assessment, «Mes demandes», a request, «Communications», a letter, «Mes échéances», the company's pages, the Forum's governance (+ `portal/registers.css`) | 44 196 · 45 069 (the company's) | 43 015 | −1 181 · −2 054 | — → **43 015** (recorded) |
   | «Mon parcours» with a file (+ registers + journey) | 46 617 | 45 436 | −1 181 | 46 617 → **45 436** |
   | a need's page (+ registers + `companies.css`) | 45 069 | 43 204 | −1 865 | 45 069 → **43 204** |
   | the help desk (+ registers + `helpdesk.css`) · an open request, its closure drawn (+ panels) | 45 071 · 45 071 | 43 277 · 45 348 | −1 794 · +277 | → **43 277 · 45 348** (recorded) |
   | the selection (+ registers + `selection.css`) · the actor's process, its closure drawn (+ panels) | 45 281 · 45 281 | 43 478 · 45 549 | −1 803 · +268 | → **43 478 · 45 549** (recorded) |
   | the Academy (+ registers + `academy.css`) | 44 814 | 43 207 | −1 607 | 44 814 → **43 207** |
   | a journey page — the dashboard with a person's file (+ journey) | 46 617 | 42 561 | −4 056 | 46 617 → **42 561** |
   | «Ma situation» (+ `portal/situation.css`) | 46 398 | 42 346 | −4 052 | 46 398 → **42 346** |
   | the reserved area's 503 (`main.css`, now + `cms/errori.css`: the error pages' grammar) | 35 483 | 35 535 | +52 | — → **35 535** (recorded) |
   | the piece, the loose upload and the Conditions gate (+ `documents.css`) | 49 693 | 45 637 | −4 056 | 49 693 → **45 637** |
   | the documents' two register pages (+ `documents.css` + panels) | 51 764 | 47 708 | −4 056 | 51 764 → **47 708** |
   | the login · the home · a content page · an account page · an error page | 40 344 · 49 844 · 39 584 · 37 909 · 39 112 | 36 767 · 46 267 · 36 007 · 34 332 · 35 535 | −3 577 | → **36 767 · 46 267 · 36 007 · 34 332 · 35 535** |
   | the persons pages · the doors · the Forum · the institutional pages · orientation | 39 068 · 38 910 · 38 504 · 37 749 · 39 597 | 35 491 · 35 333 · 34 927 · 34 172 · 36 020 | −3 577 | → **35 491 · 35 333 · 34 927 · 34 172 · 36 020** |

   `dist/main.css` 35 483 → 31 906 B (−3 577 on every page): `v4/workspace.css` out of the cascade with its last named
   consumer (the deletion map's last row, «the file») and the V1 devices these pages were the last to draw (the folio,
   the entry's ordinal and its responsible actor, the night verso) — each proved unused on design-v5 and in flight
   (`v54-w4-b` and `v54-devops-2` read again at the merge: no template of theirs draws them). `dist/portal/console.css`
   6 778 → 7 189 B (+411: `v5/_frame.css`, the survivors of `v4/workspace.css` every console page still draws, moved
   from `main.css`); `dist/portal/portal.css` 1 935 → 1 045 B. The module sheets fall (`academy.css` 618 → 192,
   `companies.css` 873 → 189 and linked by a need's page alone, `helpdesk.css` 875 → 262, `selection.css` 1 085 → 463);
   `portal/situation.css` 2 202 → 2 206 B (the act group's §5 rules). The JS: the same weight (60 726 B gzip over the
   19 files; `console.js` 1 753 → 1 744 B).
5. **Every ceiling is lowered to the weight measured at this merge** (the definitive ruling: «after a merge, the merged
   weight is the new ceiling»; DL54-120 item 5, DL54-129 item 5): every row of the table carries its new figure.
6. **The area's page types are recorded as measured — through their own page-only sheets** (V5.8 rule 2). The
   registers' grammar is one sheet (`portal/registers.css`, 2 875 B), linked by the pages that draw a register; the case
   file's own CSS another (`portal/case.css`, 955 B), linked by the case file alone, after the registers' and before
   the journey's (W3-D's order); W2-A's panels (2 071 B) are linked only where a dialog is drawn — the overlay system's
   rule (CONTRACT §1): the case file where the reader may move a line or the file, the help desk's request and the
   selection's process where they draw the irreversible closure (the review's M4). The three page types that grow do so
   by that one page-only sheet, for what they draw; the 503 by the error pages' sheet it now shares (a page of service
   in their grammar, DL54-137). The family's accessibility + performance check measured them on a compressed twin
   (`A11Y_PERF.md`: on every page type LCP −68 … +28 ms at n = 9, the first-render task lower or equal, CLS ≤ 0.0005, the
   dialog's cold open p90 ≤ 152 ms; the case file's seven stylesheets — W3-E's share three — a budget letter for W4-C,
   not a regression). Every figure ratchets down from here.
7. **No duplicate component family** (V5.8 rule 3): one registers' partial for every page the family drew
   (`v5/_registers.css`); the dialogs' one body (`.reg-dialog`: the case file's `.file-dialog` grid moved there when
   the help desk and the selection drew theirs — the second to draw it consolidates, DL54-150); the dialogs themselves
   W2-A's (`components/dialog.html`, `kind="alert"`); the empty state `components.css` §23 (V5's component, DL54-135).
8. **The inventory and the capture report.** `scripts/regen_design_inventory.py`: current on the branch and, after the
   merge, on design-v5 (nothing to write: the merged tree is the branch's). The capture report is unchanged: `capture.py` records the home, the privacy page,
   the login and the 404 (icons, h1, overflow, direction); the family changed none of them, and its shared deletions
   are rules none of them draws — not regenerated, as DL54-120 item 7 and DL54-129 item 8 said for W3-C and W3-D.
9. **The tests.** On the branch, `TEST_DATABASE_URL=…/test_ile_v5_l5`, one pytest and one browser of the steward's at a time,
   every run behind the benchmark lock, no run crashed (`evidence/v54/w3-e/merge/tests_*.log`). **Non-browser** (16 min
   17 s) — `apps/cases`, `apps/portal`, `apps/companies`, `apps/academy`, `apps/helpdesk`, `apps/selection`,
   `apps/forum` (the governance's among them), `apps/notifications`, `tests/test_phase_console.py`, `tests/security`
   (the object-permission and authorisation audits; the confidential-material sentinel test ran),
   `test_chips_registry`, `test_state_chips_carry_a_register`, `test_o14_lint`, `test_design_docs`, the two
   bundle-current tests, `test_static_pipeline` (a real `collectstatic` under the manifest storage), the family's
   `test_case_file_w3_e` and the files it retargeted or reads (W3-D's journey, W3-A's shell and its stylesheets, W3-B's
   dashboard, W3-C's two, W2-A's two overlay files, W1-C's chips, the icons, the showcase, the motion gate, the template
   comments, the RTL scanner), the ownership and inventory scripts' tests: **2 000 passed, 10 failed, 3 skipped** (the
   intake suite's own: no legal rule in force), 1 xfailed (the showcase's captions, design-v5's own strict marker) —
   the ten failures the one semantic conflict of item 2; after `ab0a79a` and `3690323` (one end-to-end test of the held
   file's page added to the family's file) the three files concerned: **162 passed**. **Browser** (headless Chromium,
   16 min 54 s): `apps/portal/tests/test_browser.py`, `tests/i18n/test_rtl_browser.py` and
   `test_rtl_browser_overlays.py`, W3-D's `test_journey_browser_w3_d`, W3-A's `test_console_phone_browser_w3_a` and
   `test_console_shell_browser_w3_a`, W3-B's `test_dashboard_browser_w3_b`, W2-A's `test_overlays_console_browser_w2_a`,
   W3-C's `test_documents_browser_w3_c` and `test_drawer_browser_w3_c` — **199 passed**, 0 skipped, 0 failed. On
   design-v5 after the merge and the rebuild (`3667aba`): the bundle, docs, pipeline, ownership and inventory tests, the
   family's own, the showcase, the chips, the template comments, W3-D's journey, the console's stylesheets and the
   motion gate — **232 passed**, 1 xfailed (22 s). `ruff check .`: all checks passed; `ruff format --check` on the
   area's changed Python files: one file, `apps/cases/views.py`, whose one deviation is design-v5's own (the same on
   design-v5), not changed; `makemigrations --check --dry-run`: no changes; `manage.py check`: no issue; `git diff
   --check` clean; no CR byte in a text file the branch changes; no inline style or script, no external URL, no secret
   in the added lines. The full suite is the integration checkpoint's (V5.5).
10. **`live_status.json`: the family row and nineteen surface keys** — the page types whose composition this family
   completes, each `v5` at `v54/w3-e`: «Mes dossiers» (`cases-index`), the case file (`case-file`), «Ma situation»
   (`situation`), «Mes demandes» and a request (`requests`, `request-detail`), «Mon parcours» with and without results
   (`journey`, `journey-results`), «Mes échéances» (`deadlines`), «Communications» (`messages`), the Academy
   (`academy-catalogue`, `academy-course`, `academy-mine`, `academy-enrolment`), the help desk (`helpdesk`,
   `helpdesk-detail`, `helpdesk-new`) and the company's pages beyond its dashboard (`company-profile`, `company-needs`,
   `company-need-form`) — each a census id. The surfaces other families completed keep their rows (the dashboards and
   the bridge W3-B's, the documents W3-C's, the 403 W3-F2's). The selection and the Forum's governance have no census
   id: they ship without a key. `CHANGELOG_V54.md`: the entry first.
11. **Handed on** (`QA/v54/w3-e/NOTES.md` «Left, and for others» and «Handed on»; none of it holds the merge): **B1**
   — the copy packet (a deadline's distance; a heading over the pre-assessments; the case file's words on a mandated
   reader's screen — «Vous êtes ici», «Où en est votre demande», «Ce qui vous a été indiqué», the assessment's empty
   sentence, «Exigences»'s lead, «au titre d'un mandat daté» shown to an administrator; the guichet's band without its
   figure); **W3-A** — the rail's «Communications (n)» beside the band's count (D17: «a dot on the rail»), the
   organisations' accounts offered the person's file entries in «Espace réservé», the Forum governance's rail;
   **W1-C** — the register is per state, not per audience («Réponse disponible» azione for the professional); **W3-D /
   W4-D** — the journey component's `descriptive` variant has no consumer now; **the staff's design debt** — the
   selection's evidence table (a select and «Mettre à jour» a row), the dispatch desk and the territorial analysis
   (their chrome only), the Django admin; **the showcase's owner** — the V4 samples whose rules left with their pages
   (the case file's, the company's facts) and `companies/partials/need_table.html`; **the companies module** —
   `companies/services.py`'s `next_action` docstring names the deleted `portal/partials/next_action.html`; **W4-C** —
   the case file's seven stylesheets (the one-sheet variant: one request less, 2.6 KB not reused from cache); **W4-B
   and devops-2** (in flight) — they sync with this merge. The drawer's scrim after a keyboard reopen (step 3's note
   for W2-A) was the overlay's late settle that integration checkpoint 3 fixed: on this branch since the sync.

**Why.** Entries numbered after design-v5's keep the log's one order; paths nobody holds would have no writer for the
next family; a test that pins another family's retired markup is retargeted to the markup that replaced it, its intent
kept, never deleted; the gate is read on the shared payload as V5.8 writes it, and the merged weight becomes every
ceiling; a surface's own CSS lives in its own sheet, loaded only where it is drawn, and its page type is recorded at
the weight it was measured at; the preview says a page is V5 when its whole composition is.

**Source.** The owner's V5.8 (`C:/tmp/ile_v5_council/directives/V5_8_CONTINUE_GITHUB_CSS_BUDGET.md`, and the
orchestrator's definitive ruling below it) and the V5_5 addenda; plan §2.2 (the manifest; merge steps 1–5), §2.3 (the
deletion map's last row), §2.6, §3.5 item 7; DL54-120; DL54-129; DL54-132; DL54-133 … DL54-150;
`QA/v54/w3-e/NOTES.md`, `REVIEW.md`, `A11Y_PERF.md`; the weights in `evidence/v54/w3-e/merge/budget_gate_*.log`; the
ownership checks in `evidence/v54/w3-e/merge/ownership_*.log`; the tests in `evidence/v54/w3-e/merge/tests_*.log`.

## DL54-152 · 16 October 2026 · Steward, the devops-2 merge: release hardening on design-v5 — every file a page loads a hashed, immutable name; a NUL byte the project's 400, never a 500; the browser tests' live server on a port Chromium accepts; the family's second pass registered; nothing deployed

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-devops-2` into design-v5 on 16 October 2026 —
the owner's V5.9 §3, «make the repository production-deployable», with its limits: never deploy, never connect to or
modify a server, DNS, domain or certificate
(`C:/tmp/ile_v5_council/directives/V5_9_DELIVERY_AND_PRODUCTION_READINESS.md`); what the lane hands to the merge:
`QA/v54/devops/NOTES.md` — «Second pass (16 Oct)», «Second pass — review fixes» and «At the merge (the steward, 16
October 2026) — second pass» — and `REVIEW_2.md`).

1. **What merged: the DevOps family's second pass — four items, each reproduced, fixed and proved** (branch
   `v54-devops-2` from design-v5 `8ab5b89`; the items handed on by integration checkpoint 3's review, «outside this
   branch», and by gates 2–4, N-4 then N-G).
   - **(a) Stale scripts after a release.** WhiteNoise serves a hashed name immutable for ten years, but the bundles of
     `static/js/dist` import one another by plain relative names, which the manifest storage never rewrote: measured on
     a real `collectstatic` under the production settings, 10 of the 48 files the templates reach (the seven chunks,
     `loader.js`, `depot.js`, `piece-drawer.js`) were plain names cached for a year (`WHITENOISE_MAX_AGE = 31536000`),
     so a returning browser could run the previous release's module beside the new pages. Now
     `core.storage.CompressedManifestModulesStorage` (`STORAGES["staticfiles"]`) rewrites the imports of
     `static/js/dist` to the hashed names — Django's module patterns, on that directory only (REVIEW_2 m3, m6) — so
     every file a page loads is a hashed, immutable name and one page load is one release (the previous release's files
     stay collected: never `--clear`); a plain name is revalidated after a minute (`WHITENOISE_MAX_AGE = 60`). Held by
     `tests/deployment/test_static_caching.py` (10 tests): a real collectstatic, twice into one root as a release does;
     the graph walked from every `{% static %}`; every specifier the hashed name it resolves to; the worst chain over
     every directory order computed from the files (2 of the 4 passes Django settles).
   - **(b) The NUL-byte 500.** A NUL in the path, the query string, a form field or the session cookie reached
     PostgreSQL (psycopg's `DataError`): a 500 and an ERROR traceback per request, for anyone. Now
     `cms.middleware.NulByteMiddleware` (after `LocaleMiddleware`, before everything that reads a value) answers with
     the URLconf's 400 page — one WARNING, no traceback: the path, the query string and the session cookie in
     `__call__`; a POST's form in `process_view`, where CSRF reads it, never for a `csrf_exempt` view (REVIEW_2 M1: the
     public webhook's multipart POST had become a 500); a body Django will not parse left to the next reader (m1). The
     four security-header middlewares (X-Frame-Options, django-csp, the back office's relaxation, the extra headers)
     moved right after `TextGZipMiddleware`, their order kept, so the guard's 400 — and the legacy 410s and the
     redirects — carry the headers of every page (m2). Held by `tests/deployment/test_nul_bytes.py` (23 tests: the
     vectors, the webhook and a `csrf_exempt` view, the headers, the chain's order) and the design preview's landing
     test.
   - **(c) collectstatic and the deploy checks.** Under `config.settings.prod`: exit 0, 615 files copied, 1 449
     post-processed; `check --deploy --fail-level WARNING` as DL54-121 left it (W005 and W021 while the template keeps
     both HSTS directives off, nothing with both on) — measured by the lane and the review, and held at the merge by
     `tests/deployment/test_production_checks.py`.
   - **(d) The browser suite's port flake.** pytest-django's `live_server` let the operating system choose its port, and
     this workstation hands ports out from 1024, among the seventeen Chromium refuses (`net::ERR_UNSAFE_PORT`: the W3-A
     run's 4045). `tests/live_server.py`, imported by the root `conftest.py`, draws and binds a port from 20000–32767 —
     the bind is the test of freedom, so two lanes never share one; the design preview's own `_runserver` draws through
     the same helper (REVIEW_2 m4's last step, placed by the steward at the merge, `4b56576`).
   - **The documents.** The runbook (step 8, step 11, the static section, the known limits) and the checklist (A-21,
     A-22, D-7, D-10) say what a browser caches and which layer answers a NUL (behind nginx a NUL in the path is nginx's
     own 400; the smoke test proves the guard on the query string); `.env.example` documents
     `DJANGO_LIVE_TEST_SERVER_ADDRESS` in its NOT FOR PRODUCTION section.
2. **The review** (`devops2-review`, `QA/v54/devops/REVIEW_2.md`, on `6010a5c`): **SHIP_AFTER_FIXES** — three of the
   four fixes held under every attack it built (a release simulated twice into one root, Chromium importing every
   rewritten module, nginx 1.24 in WSL passing WhiteNoise's headers through, six concurrent live-server sessions on
   three ports); one major (M1), six minors, four nits. The fix pass (`0596d94` … `7248f6d`) closed every one, each held
   by a test that fails before the fix; m4's last line, in W1-P's file, was left to the steward and is placed. One red
   found on the way: the design preview's landing test, broken by the guard since `fabc2d9`, rewritten as a test of its
   own (the file stays W1-P's).
3. **The hard limits, checked at the merge.** Nothing deployed; no server, DNS record, domain or certificate touched or
   contacted; no package installed. The family's 2 189 added lines (17 paths, the manifest among them) scanned in
   Python: no IPv4 address but 127.0.0.1, URLs on `localhost` only and one `https://<host…>` placeholder, `example.com`
   / `example.test` addresses only, no credential, secret-like assignment or high-entropy token, no production host,
   droplet name or live domain. No template, stylesheet or script: V5.8's shared CSS payload is not concerned.
4. **The pre-merge sync** (`53b9695`), under the lock, taken at 06:42:48 once the W3-E merge had released it: design-v5
   had moved from `8ab5b89` to `a833403` — 69 commits: the sec-f7 merge (DL54-132); `11070b5`, this family's
   private-root probe fixed by the orchestrator between the passes (GitHub's Linux runner could not create the runbook's
   root); the W3-E merge (DL54-151). No conflict, no path in common. The merge brought stylesheet sources and
   `static/js/src/console.js`, so both dist trees were rebuilt from clean: `static/css/dist` byte for byte the committed
   tree, `static/js/dist` identical but for esbuild's chunk names (12 entries, 7 chunks; the names follow the worktree);
   design-v5's committed tree kept.
5. **The family «devops» extended in the manifest** (`5a8415a`): it keeps its id, wave 0 and DL54-01's branch name; its
   note names the second branch, `v54-devops-2`. `base.py`'s slice extended (`STORAGES["staticfiles"]`,
   `WHITENOISE_MAX_AGE`, the header middlewares' place, the guard's entry) and six entries added — whole:
   `apps/core/storage.py`, `tests/live_server.py`, `tests/test_live_server.py`; slices: the guard in
   `apps/cms/middleware.py` (`LegacyURLMiddleware` stays a file no family held), the root `conftest.py`'s import and
   docstring paragraph, the design preview's NUL test and `_runserver`'s port (the file stays W1-P's). Each slice read
   in the diff and staying inside it. `check_ownership.py devops design-v5`: 16 paths, 8 inside, 2 slice, 6 outside →
   FAIL before; **16 paths, 11 inside, 5 slice → PASS** with the extended manifest, after which the manifest joins the
   diff as the steward's own steward-only path (as at the sec-f5 and sec-f7 merges). `--validate`: **29 families, 736
   entries**.
6. **The tests** on the merged branch (`5a8415a`: the tree merged here, but for the notes),
   `TEST_DATABASE_URL=…/ile_v5_l9`, one pytest at a time, `-p no:randomly`: the brief's list with the live-server tests
   and the design preview's file, **719 passed** in 5 min 56 s, no skip (`tests/deployment` 90, `tests/security` 157,
   `apps/cms` 45, the static pipeline 3, both bundle-currency tests 8, `test_design_docs.py` 40, the environment
   template 14, the checker's tests 57, the live server 8, the design preview 297); what the new middleware order
   reaches, with W3-E's pages, which meet it for the first time on this tree, **401 passed** in 8 min 03 s
   (`apps/integrations` 45, `apps/accounts` 189, the back office 5, the public pages 9, the downloads 12, the layout 29,
   the 429 page 7, the routing 30, W3-E's case file 22, the portal's views 35, the help desk's views 18); in Chromium
   through the new plumbing, **41 passed** in 3 min 40 s (W2-A's console overlays 15, the portal 8, the live server 1,
   the design preview 17 on `_runserver` and `live_server`), with another lane's browser suite running beside it.
   `manage.py check`: no issue; `makemigrations --check --dry-run`: no changes; `ruff check .` and `ruff format --check`
   (the family's 11 Python files) clean; `bash -n` on the three documents' 46 bash blocks: 0 errors. The full suite
   stays the next integration checkpoint's and CI's.
7. **The record, and what is not done here, on purpose.** Merged with `--no-ff` (`8664694`); design-v5's tree is the
   branch's, nothing rebuilt (the bundles design-v5's byte for byte). No tag (V5.9 §14: the release tags mark the whole
   product after final QA); no restart of 8780; no change to v5-live; no push; no line in `CHANGELOG_V54.md` or
   `live_status.json` (not a preview surface — DL54-77, DL54-121). Not on main (the V4 line; the release comes from
   design-v5).
8. **Open, handed on** (none holds the merge):
   - **W4-B's dist** (the Motion library removed) lands after this merge: `test_static_caching.py` walks whatever dist
     is collected, so W4-B's merge runs the proof again — a cycle, a computed `import()` or a chain longer than Django
     settles fails it, the file named (the review collected W4-B's `static/js` with this storage: exit 0, 15 dist
     modules, 36 imports, all rewritten).
   - JSON bodies with a NUL (the integrations API, behind its key) are left to their view; not probed.
   - One difference with the previous behaviour stays, by design: a multipart body Django refuses, from a client holding
     a CSRF cookie, now meets CSRF with the fields the failed parse left empty — 403 «CSRF token missing» where it was a
     400 (the site's upload forms send one file each, far below the limits).
   - Not exercised on this workstation: nginx, Gunicorn, a server (the review measured nginx 1.24 in WSL); the runbook
     says how to check each on the server. CI still installs `requirements/dev.txt` without `-c
     requirements/constraints.txt` (the steward's `ci.yml`, DL54-121 item 6).
   - For the owner, at each release: `collectstatic` without `--clear` (runbook step 8) — a page opened before a release
     keeps importing the files of its own release.

**Why.** A hashed entry that imports plain names is a cache that lies at the next release: the browser keeps a module
whose content changed under the same URL, and only rewriting the imports makes one page load one release; a request no
URL of the site can hold should meet the site's 400, not leave a traceback in the logs for every scanner; a guard placed
before the readers must not become the reader that breaks a view (the webhook), nor answer what the next reader answers
better (CSRF); headers written on the way out belong above everything that can answer early; a browser-suite failure
with no cause in the code costs a re-run and hides real reds. A family's second branch is still the family: one writer
per path, its slices extended where its diff grew.

**Source.** The owner's V5.9 §3–§18 and V5.5; DL54-01 (the ref names); DL54-77 (a merge that is not a preview surface);
DL54-121 (the devops merge), DL54-130 … DL54-132 (families outside the waves), DL54-151 (the W3-E merge, synced here);
integration checkpoint 3's review (`QA/v54/intfix/REVIEW.md`, «outside this branch»); plan §2.2 (a file not in the
manifest has no writer until the steward assigns it); `QA/v54/devops/NOTES.md` (with «Second pass», «Second pass —
review fixes» and the steward's section), `REVIEW_2.md`; the ownership checks, the scan, the builds and the test logs in
`C:/tmp/ile_v5_council/evidence/v54/devops/merge-2/`.

## DL54-153 · 16 October 2026 · W4-B, the motion audit: the Motion library leaves; R10 enforced; the keyboard's tier 0 in the chrome; the reveals gone

(Written as DL54-132 on the branch, after design-v5's DL54-131. design-v5 then gave DL54-132 to the sec-f7 record,
DL54-133 … DL54-151 to W3-E and its merge and DL54-152 to the devops-2 merge: the steward renumbered this entry
DL54-153 at the merge — the table row, this heading and the mentions of it in `QA/v54/w4-b/NOTES.md` and
`A11Y_PERF.md`; DL54-154 item 1.)

1. **The audit came first, read-only** (`docs/design-v5/QA/v54/w4-b/AUDIT.md`): every page type's motion — at load, on a
   gesture, on scroll —, its tier, tokens and reduced-motion still, measured on lane 8 (68 loads, fr and ar, 1440 and
   390, the setting on and off; an instrument recording every CSS transition and animation and every
   `element.animate()`) and read from every sheet (249 declarations) and script. The tiers and their ceilings hold; one
   indicator per page; nothing at load in the console but the entrance release; under the setting every overlay is one
   80 ms opacity and nothing else moves; 0 animations and 0 `will-change` at rest. Five findings, fixed below — and four
   lines it marked compliant that the review and the accessibility check measured otherwise (item 10; AUDIT.md §11).
2. **The Motion library leaves (F2).** Its last callers were shell.js's reveal and «Ma situation»'s question change.
   The change now runs on `play()` — the Web Animations API through the gate — with the clocks it had (the leaving
   question's fade on `--motion-fast`, then the arriving one on `--motion-standard` from 16 px in the reading direction,
   −16 px in Arabic) and with the token's curve, `--ease-enter`, where Motion had applied its own default: the call
   passed `easing:`, Motion One's name, which Motion 13 ignores. Timing probe, frame by frame, at 1440 and 390, fr and
   ar: leave 120 ms → arrive 200 ms, 331–349 ms in all (Motion's 336–352 ms); the arrival is front-loaded (opacity
   0.93 at half time where Motion's ease-out gave 0.76 — the enter curve of MS-O1); and the one frame in which Motion
   showed the arriving question at full opacity before animating it is gone. A curve is never typed in a script
   (motion.js's contract): the curve became the token. `motion.js` keeps its whole contract (`reducedMotion`,
   `withMotion`, `play`, `nextFrame`, `afterPaint`, `tween`, `settled`, `durationToken`, `easingToken`) and loses the
   re-exports and the JS springs (their CSS `linear()` twins stay). `npm uninstall motion --package-lock-only
   --ignore-scripts` — on the orchestrator's instruction for this area — removed `motion`, `framer-motion`,
   `motion-dom`, `motion-utils` and `tslib` from `package.json` and `package-lock.json` without touching any
   `node_modules`; `test_frontend_bundle_is_current.py`'s Motion-exports assertion is rewritten in the same commit (plan
   §2.7): the helpers exported, no source importing the library, no package file declaring it, no bundle carrying its
   code.
3. **K17 — the reveals that hide text (F1)**: shell.js's `[data-reveal]` (Motion's `inView` + `animate` + `stagger`),
   `components.css` §29 (`.reveal`, its stagger, its permanent `will-change`, its reduced-motion guard, and `.counter`)
   and `main.js`'s `initReveal` and `initCounters` (a count-up on `requestAnimationFrame` outside the gate — W1-D's
   hand-off) are deleted: no template, no CMS content (`ile_v5`, `ile_v5_l8`) and no page's DOM carried them, and a
   failing script would have left their text at opacity 0. So shell.js's reveal is not ported: on design-v5 it moved
   nothing on any page, and nothing moves after.
4. **One script request fewer (W2-C1's A11Y_PERF item 5, handed to W4-B).** `scripts/build_frontend.mjs` no longer makes
   an entry of a module one entry alone imports (`nav.js` → `shell.js`, `hero.js` → `home.js`): its code is inlined into
   its importer instead of a chunk plus a stub nobody loads — plan §2.6's request ratchet, over by one since DL54-101,
   holds again. With item 2: **the home 51 249 → 24 138 B gzip (9 → 7 script requests)**, a public page 43 674 → 16 781
   (7 → 6), an entrance page 45 351 → 18 462, a console page 46 070 → 19 178, «Ma situation» 47 292 → 20 415 (gzip -9,
   the steward's measure: the import closure of each page's entries + `main.js` + `head.js`, + `rail-pref.js` in the
   console). §2.6's «a public page ≤ 45 KB» holds everywhere.
5. **The rail folds at once (F3; plan §1.5 R10).** R10 ships the collapse instant «unless `contain: layout` brings it to
   60 fps at CPU × 4»; W3-A had shipped a 200 ms transition of the rail's `inline-size` and of the page's
   `padding-inline-start` — layout properties, re-laying the workspace on every frame. Measured (n = 5, the dashboard at
   1440): at CPU × 1, 15 frames in 260 ms, gaps of 16.7 ms; at CPU × 4, 8 frames, gaps of 67–117 ms; with
   `contain: layout` on the workspace and the rail, 9.5 frames, gaps of 50–117 ms. The two transitions leave
   `_shell.css`; `console.js`'s `is-ready` (W3-E's file, in review) stays as a harmless hook.
6. **The keyboard never animates the chrome (F4, F5; tier 0, R-07).** The portico had no `html[data-input="key"]` rule:
   Esc after a pointer's opening ran the panel's 120 ms exit and the chevron's 200 ms turn, the arrows' indicator faded
   120 ms. One rule in `chrome.css` zeroes the door word, the chevron, the panel, its photograph and the architrave from
   the keyboard (a mouse movement gives the pointer its motion back). The skip link — reached only from the keyboard —
   loses its 120 ms slide (V1 `base.css`).
7. **The forced-colours current entry (W3-D's O2; WCAG 2.4.7).** The current page of the rail and of the phone bar drew
   the focus ring's outline at rest: focusing it changed 0 pixels (fr and ar, 1440 and 390). Its marker is now its lit
   Highlight disc and, in the rail, its word underlined (the bar's words stand on the screen's bottom edge, where an
   underline is cut); focusing it changes 508–1 060 pixels.
8. **The checkpoint review's minors.** m2: a static test that every guarded form submits through a `.btn`
   (`tests/frontend/test_single_submit_w4_b.py`: the project's forms and their includes, allauth's button element,
   allauth's own templates — a mutation to a plain button fails it) rather than a release on shell.js's early return,
   which would give up the double-submit guard; m3: `initMisc`'s comment names shell.js's catch as the guard's other
   lifter; m4: the 400 % overlay test gains its resize step (a separate test, both motion settings; with the re-read
   removed both fail). W3-D's O3 measured: an `[open]` toggle in the console re-styles the disclosure's own 112
   elements, with or without the remaining `html:has()` rules (574 elements on the page) — `html:has(.console-drawer[open])`
   left with W2-A (`e5fa845`); nothing to fix.
9. **Paths outside the slice, for the merge step to write into the manifest:** `package.json`, `package-lock.json`
   (steward-only: the uninstall the orchestrator asked of this area); `scripts/build_frontend.mjs` (no owner: item 4,
   handed by W2-C1 to «W4-B / the steward»); `docs/design-v2/FRONTEND_DEPENDENCIES.md` (no owner: the registry's row of
   the dependency that left); and, through W4-B's delegation, `static/js/src/situation.js` (item 2),
   `static/js/src/shell.js` (the reveal), `static/js/main.js`'s `initCounters` and `initMisc`'s comment (items 3, 8),
   `static/css/v5/chrome.css` (items 6, 10), `static/css/base.css` (item 6), `apps/portal/static/portal/v5/_shell.css`
   (items 5, 7, 10), `static/css/v5/base.css` (W1-A's) and `static/css/v5/overlays.css` and
   `static/css/v5/_overlay-panels.css` (W2-A's) (item 10), `templates/base.html` (the comment that named Motion),
   `docs/design/DESIGN_SYSTEM_2026.md` (§11.6, §12, §16; the figures by `regen_design_inventory.py`),
   `docs/ACCESSIBILITY.md` (§7), and the tests that pinned what changed: `test_console_shell_w3_a.py`,
   `test_console_shell_browser_w3_a.py` and `test_console_phone_browser_w3_a.py` (the rail's transition, the
   forced-colours outline at rest), `test_design_docs.py` (the reduced-motion check and a runtime name),
   `test_css_tokens_exist.py` (a runtime name), `test_overlays_browser_w2_a.py` (m4). `components.css` is in W3-E's diff
   too (§23, far from §29): a trial merge of the two branches merges it without a conflict.
10. **After the review and the accessibility check (`QA/v54/w4-b/REVIEW.md` m1–m4, `A11Y_PERF.md` findings 1–3;
    one fix pass, V5.5).** Four lines the audit had marked compliant (AUDIT.md §11):
    - **«Ma situation» from the keyboard (the check's major, the review's m1).** Enter or Space on «Continuer»,
      «Précédent» or a Stepper link ran the pointer's 120 + 200 ms, and the focused question's ring showed ≈ 320 ms
      after the key. `situation.js` now asks the input's modality beside the gate — `html[data-input="key"]`, which
      head.js writes on the keydown, before the click — and creates no animation: the question swaps in the key's own
      task with the focus and its ring on it, as under reduced motion. Pre-existing (the branch point animated the same
      way through Motion), but this area rewrote that very animation.
    - **An interruption (the review's m2, the check's finding 2).** A return within the 120 ms leaving fade
      («Continuer» then «Précédent»; the Stepper's Q3 then Q1) left no question drawn and the focus on `body`: the first
      change's late step hid the question the second had shown — the closure race design-v5 already had. Each change
      now takes a turn (a generation token) and a late step whose turn has passed does nothing; a change asked while
      another is in flight lands it first — its animations cancelled, no inline opacity left — and plays its own
      arrival only. Measured: exactly one question, at opacity 1 and in place, no `style` attribute, the focus, the
      counter and the Stepper on it — for the return, the Stepper's return, a double «Continuer» and a return during
      the arrival (fr and ar, 1440 and 390).
    - **Links (the review's m3, the check's finding 3).** Plain links had no keyboard rule: the console bar's trail ran
      the links' 120 ms colour fade from Tab. One rule beside the links' transition in `v5/base.css`:
      `html[data-input="key"] a { transition-duration: 0ms; }`. A 45-Tab walk of the dashboard and a 30-Tab walk of a
      door page now start no transition (fr and ar).
    - **The curves (the review's m4; MS-O1 / MS-O2).** Ten declarations kept the superseded council table's
      `--ease-exit` — the portico's pointer exit, the menu items' and the close control's hover colours, the rail's rows,
      tools and foot, the phone bar — where a small surface leaves on `--ease-enter` at 120 ms and the way into a hover
      is `--ease-enter`. All ten swap; the two hover rules that only switched the curve back lose that clause. The
      portico's exit no longer holds near-full opacity for its first ~40 ms: 0.27 at 33 ms. No sheet names `--ease-exit`
      but the token files (no object crosses the view today), and `tests/frontend/test_motion_rules_w4_b.py` holds it.
    The JS change weighs 145 B gzip on «Ma situation» only (20 415 → 20 560 B); the shared CSS goes down again
    (`main.css` −6 B, the console page type −9 B gzip). Eight browser cases (the keyboard walk and the interruptions in
    `test_motion_browser_w4_b.py`, the trail from Tab) and two static guards, each red on the previous tree.

**Why.** The plan's Wave 4 motion lane: the tiers and rulings of §1.5 checked on the product as built, the Motion
dependency removed «once unused», and the reveals that hide text removed (K17) — with the home's script back under
§2.6's 45 KB, which DL54-101 had recorded as exceeded until this family.

**Source.** Plan §1.5 (tiers, MS-O1/O2/O3/O4, R10, K17, «Engine»), §2.2, §2.3 (deletion map: §29, `initReveal`), §2.6,
§2.7 (`test_frontend_bundle_is_current.py:45`), §3.6 item 2; DL54-101 item 4; DL54-102; `QA/v54/intfix/REVIEW.md` m2–m4;
`QA/v54/w3-d/NOTES.md` «Handed to» (O2, O3); `QA/v54/w2-c1/A11Y_PERF.md` item 5; `QA/v54/w1-d/NOTES.md` (the counters);
`QA/v54/w4-b/AUDIT.md`, `NOTES.md`, `REVIEW.md`, `A11Y_PERF.md`; evidence in `C:/tmp/ile_v5_council/evidence/v54/w4-b/`.

## DL54-154 · 16 October 2026 · Steward, the w4-b merge: the motion audit on design-v5 — the Motion library out of every bundle and of the package files, W4-B's entry renumbered DL54-153, the four paths outside the slice assigned, both shared CSS bundles lower again, the home's script back under §2.6's 45 KB

**Decisions** (the steward's, for the infrastructure, at the merge of `v54-w4-b` into design-v5 on 16 October 2026 —
what the family's entry and notes hand to the merge step: DL54-153 items 9 and 10; `QA/v54/w4-b/NOTES.md` §6, §7,
«Review fixes» and «At the merge (for the steward)»; `QA/v54/w4-b/REVIEW.md` «For the merge step» and `A11Y_PERF.md`,
both SHIP_AFTER_FIXES, every finding fixed in the family's one fix pass, V5.5).

1. **The order and the numbering.** The steward took `DESIGN_V5_MERGE_LOCK` at 07:32:08 with design-v5 at `5bf2f90`
   (the devops-2 record). The plan runs Wave 4 in sequence (§3.6; the manifest's `after` puts W4-A before W4-B); the
   orchestrator launched W4-B on 16 October ahead of W4-A, beside W3-E, and asked for its merge first — W4-A, in
   flight on lane 6 with no commit of its own yet, syncs with this one. The branch's merge base was `8ab5b89`
   (integration checkpoint 3's status); design-v5 had since recorded the sec-f7 merge (DL54-132), W3-E and its merge
   (DL54-133 … DL54-151) and the devops-2 merge (DL54-152), so the steward's sync (`d707d32`, 91 commits) gave the
   family's one entry **DL54-153** — its heading, its index row and its own note; the six mentions of it in
   `NOTES.md` and `A11Y_PERF.md` follow (`7e20cbf`), and the three that say design-v5's DL54-132 is sec-f7's stay as
   written. Checked after the resolution: the log without the family's row and block is design-v5's byte for byte, and
   the family's row and block with the number shifted back are the branch's but for that note. design-v5's index had
   no row for DL54-152 (the devops-2 record wrote its block only): this entry adds it beside its own. This entry is
   DL54-154.
2. **Both areas kept.** The sync wrote three conflicts: the decision log (item 1); DS 2026 §2's inventory table,
   generated — design-v5's side (W3-E removed the `v4/workspace.css` row), then `regen_design_inventory.py --write`
   (`components.css` 14.9 KB and 9 sections: W4-B's §29 out of the sheet whose §23 W3-E rewrote; `v5/base.css` 7.9 KB;
   `v5/chrome.css` 51.0 KB); and both dist trees (`merge=binary`), deleted and rebuilt with `npm run build` on the
   merged sources — every bundle neither side conflicted on came out byte for byte the merge's. Four files merged on
   their own and were read: `static/css/base.css` (W3-E's folio selectors cut; W4-B's skip-link transition gone),
   `static/css/components.css` (W3-E's §23 empty state; W4-B's §29 deleted), W3-A's `test_console_shell_w3_a.py` and
   `test_console_phone_browser_w3_a.py` (W3-E's header and action-bar cases beside W4-B's R10 and forced-colours
   ones). No merged source imports the library or an export `motion.js` lost — every importer, W3-E's `console.js`
   among them, reads `afterPaint`, `durationToken`, `easingToken`, `nextFrame`, `play`, `reducedMotion` or `settled` —;
   no template, W3-E's new ones included, draws `.reveal` or `[data-reveal]`; devops-2's module storage rewrites the
   imports of whatever entries the build writes, and its import-chain analysis passes on the new graph (item 6).
3. **The four paths outside the slice**, each read in the diff and found to be what the family declares. Two are
   this area's in the manifest (`bac3e12`), as slices of files no family held: `scripts/build_frontend.mjs` (the
   `INLINED` list — a module one entry alone imports is inlined into it instead of becoming an entry: `nav.js` into
   `shell.js`, `hero.js` into `home.js` — and the two comments it rewrote; W2-C1's A11Y_PERF item 5, handed to «W4-B /
   the steward») and `docs/design-v2/FRONTEND_DEPENDENCIES.md` (the `motion` row and the «Decisione d'uso» paragraph:
   the registry's own rule). The other two, `package.json` and `package-lock.json`, carry the dependency's removal,
   which the plan gives the steward in this very merge (§3.6 item 2: «the `motion` dependency removed by the steward
   once unused, with `test_frontend_bundle_is_current.py:45` rewritten in the same merge»): the area ran
   `npm uninstall motion --package-lock-only --ignore-scripts` on the orchestrator's instruction, touching no
   `node_modules`, and the steward adopts it as its own write — the lock read: `motion`, `framer-motion`, `motion-dom`,
   `motion-utils` and `tslib` gone, no remaining package requiring any of them, the root without runtime
   `dependencies`. They stay the steward's whole files with no family slice (`b113836`): the checker classifies a
   steward-only path before any slice, so an entry there would change no verdict, and `tests/test_check_ownership.py`
   pins «package.json: steward (whole file), steward only» — the slices first written for them in `bac3e12` broke that
   pin in the targeted run (item 6) and were taken out. The check: before, 7 inside, 6 slice, 23 generated,
   16 delegated, 2 outside, 2 steward-only; after, 7 inside, 8 slice, 23 generated, 16 delegated, and the three
   steward-only paths the steward writes itself at this merge (the manifest, the two package files); 0 outside.
   `--validate`: coherent, 29 families, 738 entries. design-v5's own `node_modules` still holds the five packages: no
   build imports them, and this programme's standing rule allows no `npm ci` or `install` — they leave at the next
   `npm ci`.
4. **The shared CSS gate (the owner's V5.8 and the orchestrator's definitive ruling of 12 October, 02:15) passes:
   both shared bundles fall again.** On the bundles rebuilt from a clean dist, `gzip.compress(data, 9, mtime=0)`,
   each page type with the sheets its templates link — W4-B changes no page's list
   (`evidence/v54/w4-b/merge/budget_gate_branch.log`; `budget_gate_merged.log` on design-v5 after the merge):

   | Page type | design-v5 `5bf2f90` | merged | change |
   |---|---|---|---|
   | every page, and an interior page with no sheet of its own (`main.css`) | 31 906 | 31 799 | −107 |
   | console page types (`main` + `console` + `portal`) | 40 140 | 39 978 | −162 |
   | the case file · where it draws its dialogs (+ panels) | 46 391 · 48 462 | 46 229 · 48 289 | −162 · −173 |
   | a register page · «Mon parcours» with a file | 43 015 · 45 436 | 42 853 · 45 274 | −162 |
   | a journey page · «Ma situation» | 42 561 · 42 346 | 42 399 · 42 184 | −162 |
   | a need's page · the help desk · the selection · the Academy | 43 204 · 43 277 · 43 478 · 43 207 | 43 042 · 43 115 · 43 316 · 43 045 | −162 |
   | the help desk's and the selection's closures drawn (+ panels) | 45 348 · 45 549 | 45 175 · 45 376 | −173 |
   | the piece, the loose upload, the gate · the documents' registers (+ panels) | 45 637 · 47 708 | 45 475 · 47 535 | −162 · −173 |
   | the login · the home · a content page · an account page · an error page and the 503 | 36 767 · 46 267 · 36 007 · 34 332 · 35 535 | 36 660 · 46 160 · 35 900 · 34 225 · 35 428 | −107 |
   | the persons pages · the doors · the Forum · the institutional pages · orientation | 35 491 · 35 333 · 34 927 · 34 172 · 36 020 | 35 384 · 35 226 · 34 820 · 34 065 · 35 913 | −107 |

   `dist/main.css` −107 B (`components.css` §29 and its guard, the skip link's slide, the keyboard rules of the portico
   and of the links, the curves back to their roles); `dist/portal/console.css` 7 189 → 7 134 B (the rail's two layout
   transitions and their print silencer out; the forced-colours current marker); `core/overlay-panels.css`
   (page-only) 2 071 → 2 060 B. **Every ceiling is lowered to the weight measured at this merge** (the ruling: «after a
   merge, the merged weight is the new ceiling»): the merged column above.
5. **The script budget (plan §2.6) holds on every page type again** (the steward's measure of DL54-101: the import
   closure of the entries a page's template loads + `main.js` + `head.js`, + `rail-pref.js` in the console, gzip −9;
   `evidence/v54/w4-b/merge/jsweigh.log`): the home 51 249 → **24 138 B** (9 → 7 script requests), a public page
   43 674 → 16 781 (7 → 6), an entrance page 45 351 → 18 462 (8 → 7), a console page 46 060 → 19 168 (9 → 8), «Ma
   situation» 47 282 → 20 537 (10 → 9). DL54-101's «the home over 45 KB until W4-B removes the library» is closed, and
   the request ratchet over by one since DL54-101 holds.
6. **The tests.** On the branch, `TEST_DATABASE_URL=…/test_ile_v5_l8`, one pytest and one browser of the steward's at a time,
   the benchmark lock absent at every start, no run crashed (`evidence/v54/w4-b/merge/tests_*.log`). **Non-browser**
   (15 min) — the merge brief's list: the motion gate, both bundle-current tests, the static pipeline (a real
   `collectstatic` under the manifest storage), the loader's rules and W1-D's loader file, the entrance's two files and
   the login form's, W2-A's overlay files, W2-C2's sheet and browser files, W3-D's journey, W3-A's shell files and the
   console's stylesheets, the design docs, `apps/pages/tests`, `tests/security` (the confidential-material sentinel
   test ran) —, with the family's two static files (`test_motion_rules_w4_b.py`, `test_single_submit_w4_b.py`), W1-D's
   reduced motion, devops-2's `tests/deployment/test_static_caching.py` (a real `collectstatic` twice under the
   production settings, and the import-chain analysis on the graph W4-B's build writes) and the checker's and the
   inventory's tests: **846 passed, 1 failed** — `tests/test_check_ownership.py`'s pin «package.json: steward (whole
   file), steward only», which the steward's own first manifest entries broke (item 3), fixed: the file **57 passed**;
   0 skipped. **Browser** (headless Chromium, 32 min 33 s): the family's `test_motion_browser_w4_b.py`, W1-D's loader
   and reduced-motion files, the entrance's files and `test_rtl_browser_entrance.py`, W2-A's two overlay files and
   `test_rtl_browser_overlays.py`, W2-C2's sheet and browser files, W3-D's journey, W3-A's shell and phone files,
   `tests/i18n/test_rtl_browser.py`, `apps/pages/tests` (the hero) — **310 passed**, 0 skipped, 0 failed. On design-v5
   after the merge (`844e11f`) and its clean rebuild (byte for byte the merged bundles: no build commit): the bundle,
   docs, motion-gate, ownership and inventory tests and the family's static files — **124 passed**. `ruff check .`: all
   checks passed; `manage.py check`: no issue; `makemigrations --check --dry-run`: no changes; `git diff --check`
   clean; no CR byte in a text file the branch changes; no inline style or script, no external URL, no secret in the
   added lines. The full suite is the integration checkpoint's (V5.5).
7. **`live_status.json`: the family row w4-b** — state v5, its review as the decision, the tag. No surface key
   changes: every surface W4-B moved (the portico on every public page, «Ma situation»'s question change, the
   console's rail and trail, the overlays' hovers, the forced-colours marker) was already `v5` at the tag of the family
   that composed it, and W4-B composes no page — the surfaces keep their families' tags (DL54-151 item 10: the preview
   says a page is V5 when its whole composition is). `CHANGELOG_V54.md`: the entry first.
8. **The inventory and the capture report.** `regen_design_inventory.py`: current on the branch after the sync's
   `--write` and on design-v5 after the merge. The capture report is not regenerated: `capture.py` records the icons,
   the h1, the overflow and the direction of the home, the privacy page, the login and the 404, and W4-B changed motion
   only.
9. **Handed on** (`NOTES.md` §7 and «Left for others»; none of it holds the merge): **W4-D** — the legacy sweep:
   `components/hero.html` (no template includes it), the `.entrance` / `.entrance__cta` rules of `components.css`,
   `--duration-reveal`, `--reveal-distance` and `--reveal-index` in `_legacy-tokens.css`, `cms_nav.py`'s `hero_lines`,
   `data-reveal-once` on `orientation/result.html`, the dead guard `html.js .page-home .reveal` of `pages.css`;
   **W1-A** — `v5/tokens.css` l. 468 calls the springs the «CSS twins of motion.js» (the JS twins left); **W3-A** —
   `console.js`'s `is-ready` and its header line on the rail's width, a hook without a transition now; **W4-C** — the
   motion seen at speed by a person, Firefox and WebKit. The intfix review's «three dynamic-import entries with fixed
   names under a one-year cache» (NOTES §7, for DevOps / W1-D) is met by the devops-2 merge (DL54-152: every file a
   page loads a hashed, immutable name; a plain name revalidated after a minute).

**Why.** An entry numbered after design-v5's keeps the log's one order; the dependency's removal is the steward's by
the plan, so the steward reads it and owns it at the merge rather than reverting what the orchestrator asked of the
area; paths nobody held get their writer with their reason; the gate is read on the shared payload as V5.8 writes it,
and the merged weight becomes every ceiling; the preview names a family's work by its row when it composes no page.

**Source.** Plan §1.5 («Engine», R10, K17), §2.2 (the serialized files: `package.json` and `package-lock.json` the
steward only; merge steps 1–5), §2.6, §2.7, §3.6 item 2; the owner's V5.5 and V5.8 (and the definitive ruling below
it); DL54-101; DL54-151; DL54-152; DL54-153; `QA/v54/w4-b/NOTES.md`, `REVIEW.md`, `A11Y_PERF.md`, `AUDIT.md`; the
weights in `evidence/v54/w4-b/merge/budget_gate_*.log` and `jsweigh.log`; the ownership checks in
`evidence/v54/w4-b/merge/ownership_*.log`; the tests in `evidence/v54/w4-b/merge/tests_*.log`.

## DL54-155 · 16 October 2026 · Steward, the w4-d merge (part 1): release engineering on design-v5 — CI on the server's major versions beside the development stack, the release of V5.10 named once in the deployment documents, one bar for PRODUCTION_READY, the go-live calendar verified, the release notes drafted; no tag, nothing deployed

**Decisions** (the steward's, for the infrastructure, at the merge of part 1 of `v54-w4-d` into design-v5 on 16 October
2026). The briefs: the owner's V5.10 (the release decision, which the orchestrator carries out after the fourteen
gates, never a family), V5.9 (never deploy; never touch a server, DNS, a domain or a certificate; never name the
production server) and V5.5. What the lane hands to the merge: `QA/v54/w4-d/NOTES.md` («Part 1 — release
engineering», «Part 1 — review fixes», «Part 1 — at the merge (the steward)») and `REVIEW_PART1.md`
(SHIP_AFTER_FIXES). W4-D wrote no entry of its own on the branch, because four families append to this log in
parallel; this entry records the part's decisions as well, as the lane's notes ask.

1. **CI: one job, two runs — the production target and the development stack** (`4676ffd`, `ecd691f`, `db311e0`).
   - **The runner.** `runs-on: ubuntu-24.04`, the server's release. `ubuntu-latest` moves to Ubuntu 26 from
     19 October 2026 (GitHub's notice of 17 September).
   - **The matrix.** One job, its id `test` unchanged, runs twice with `fail-fast: false`, each run on its own runner
     and its own database: «Python 3.12 · PostgreSQL 16 (production target) — check · migrations · ruff · pytest»
     and «Python 3.13 · PostgreSQL 17 (development) — …».
   - **The install.** Both runs install `requirements/dev.txt` with `-c requirements/constraints.txt`, the set the
     server installs (left open by DL54-121 item 6).
   - **The version step.** A step after the install, «The interpreter and the database are the matrix's», asserts
     the interpreter's minor version and the database's major, so each job's name is true. Both checks were run both
     ways: 3.12.10 and 3.13.5 each pass with their own version and fail with the other; against PostgreSQL 17,
     `PG_MAJOR=17` passes and `16` fails.
   - **What the production-target run proves** (the comment, the runbook and checklist A-26 now say the same): the
     server's major versions, with the pinned closure and its Linux wheels. It runs setup-python's CPython 3.12.x
     and the Alpine image of PostgreSQL 16, not Ubuntu's own builds (the review's m2). The Debian image is not
     taken: the server cluster's collation follows the droplet's locale, which is not known here, so neither image
     is the server's build.
   - **Proved before the change.** The constraints resolve with `dev.txt` for Linux CPython 3.12 and 3.13 (67
     distributions each, the 19 pins kept, wheels only) and install in a throwaway 3.12 venv (`pip check` clean).
     The 817 tracked sources compile under 3.12.10. `check`, `makemigrations --check` and a targeted suite (394
     passed) run on 3.12.
   - GitHub has no branch protection and no ruleset, so the new job names break no required check. A watcher of the
     old name must follow (item 9).
2. **The release, named once in the three deployment documents** (`d2e217b`, `579c01d`, `9c67417`, `cce5d9b`). The
   runbook, the checklist and ROLLBACK.md now describe V5.10's release:
   - **The release tag.** `v2.0.0`, annotated (the platform's own label «v2.0.0 — Fase 1»), on the commit GitHub's
     `main` points to after the fast-forward promotion. There is no candidate tag (the candidate is named by its
     SHA), and a tag is never moved.
   - **The reference point.** `pre-v5-main-2026-10` on `a3ac318304beb4504134762bfa6e9c4e4ce600f1`, the pre-V5
     platform. V5.10 calls it a «rollback/reference point»: it belongs to the repository's history and is never a
     rollback target of the server, which never ran it. It predates F-5, F-7, F-8 and the NUL guard.
   - **The checklist.** A-1 (the publication repository's design-v5 snapshot); A-2 (`ls-remote` of `main`,
     `design-v5` and both tags with their `^{}` lines, no other tag; both CI runs green); A-27 (decided); C-7. The
     `ILE_TAG` and `PREVIOUS_TAG` examples read `v2.0.0`.
   - **ROLLBACK.md §7.** No migration differs today: the 39 numbered files of `a3ac318`'s tree and of design-v5 at
     `0a8351b` are identical, byte for byte. The re-check on the release is
     `git diff --name-status pre-v5-main-2026-10 v2.0.0 -- 'apps/*/migrations/*.py'`. The former pattern
     `'apps/*/migrations/'` matched no file (the review's M1), so it printed nothing whatever the release held; the
     runbook's step 15 preview had the same cause and was fixed with it. A downgrade is a restore of the verified
     pre-migration dump, never a `migrate` backwards on live data.
   - **The test.** `tests/deployment/test_release_tags_w4_d.py` holds the tag to the version label, and the three
     documents to one release and one reference SHA. Every migration pattern in the documents must list the files
     `git ls-files` lists. The tripwire holds the 39 files' blob ids at `0a8351b` (m3), and CI holds the production
     target.
3. **PRODUCTION_READY: one bar** (`e968e0d`; the review's M2). The runbook's *States* and checklist §A now state it
   in the same words: **«A-1 … A-22 ticked with evidence on that commit, and each of A-23 … A-28 closed or accepted
   in writing by the owner as open until go-live»**.
   - The final handoff names each of A-23 … A-28 with its state. It also lists the parts of A-1 … A-22 that run on
     the server or on the temporary host (A-8, A-10, A-11, A-13, A-14, A-15, A-16, A-21, A-22), which are the
     owner's, at the deployment.
   - The state's other conditions stand: the candidate is GitHub's `main` by fast-forward; `pre-v5-main-2026-10`
     preserves `a3ac318`; `v2.0.0` is annotated on `main`'s commit; the handoff (V5.9 §17) is written.
   - RELEASE_CANDIDATE: one design-v5 snapshot on GitHub, named by its SHA, on which the fourteen gates of V5.10
     passed (the release notes' *Release gates*), with CI green on both runs.
   - DEVELOPMENT_COMPLETE: every V5 family merged into design-v5, Wave 4 and F-8 included, and the full suite green
     there.
   - «GitHub pushed» is none of these.
4. **The go-live calendar: nothing to fix in code** (`98ae0ad`, `0fe5b66`; plan §3.6 item 4).
   - **What it lists.** `GO_LIVE_PHASE.md` lists everything that reads a date or a phase flag: G1 … G6, G11 and the
     publication windows. G0, G7, G8, G10 and G12 read neither; G9 reads only the `analytics` default, which no
     code reads (m5).
   - **What a visitor sees** from 16 October to 15 December 2026: rendered on a fresh seed at five frozen moments,
     French and Arabic, every internal link followed. There is no past-dated call to action, no countdown, no open
     registration for the past event, and no phase that shows nothing.
   - **The test.** `tests/compliance/test_go_live_calendar_w4_d.py` holds it, with a control that finds the
     registration button while registration is open. The review confirmed it on a lane server under today's clock,
     on the QA copy and on a fresh deployment.
5. **The release notes, a draft** (`883b48c`, `a6b9dc2`). `docs/RELEASE_NOTES_v2.0.0.md` is now w4-d's whole file
   (item 6).
   - **What it holds.** What v2.0.0 is; the security and robustness work (F-8 «pending F-8's merge»); the weights,
     before → after; pointers to the deployment documents; the owner's open decisions; the known limits; and the
     fourteen V5.10 gates, «to be filled by the release-candidate validation».
   - **The rule figure** is the seed's: 16 candidates over 15 sources, 11 drafted from the norm and 5 taken from the
     previous platform (m1).
   - **One paragraph is the owner's to word** (m4). It left the public notes; its substance goes to the
     release-candidate report and the owner's handoff, not to a published file. A family's QA folder is published
     with design-v5's snapshots, so the review's own description of m4 was shortened at the merge (`859c7d8`): its
     finding, verdict and fix are kept.
6. **The pre-merge sync and the manifest.** I took `DESIGN_V5_MERGE_LOCK` at 11:18:17, with design-v5 at
   `0a8351b`.
   - **The sync.** `0a8351b` is the branch's own base, so `git merge design-v5` printed «Already up to date». No
     source changed on either side, so no bundle was rebuilt.
   - **The manifest** (`331512d`). The release notes are now w4-d's whole file: no family held them. The six
     delegated edits are w4-d slices, each read in the diff and staying inside it:
     - `.github/workflows/ci.yml`, the steward's delegated edit (the file stays the steward's);
     - devops's runbook, checklist and ROLLBACK.md;
     - README's «Requisiti» line, beside devops's and sec-f5's slices;
     - the release-gate assertion of `test_runbook_matches_the_code.py`.

     The files other than ci.yml stay devops's. The family's note says the same, for part 2's merge.
   - **The check.** `check_ownership.py w4-d design-v5`: 5 inside, 6 delegated, 1 outside → FAIL before; 6 inside,
     6 slice → PASS with the extended manifest. After its commit, the manifest joins the diff as the steward's own
     steward-only path. `--validate`: 29 families, 745 entries.
7. **The scan and the tests.**
   - **The scan** of the added lines (12 paths, 1 391 lines): no IPv4 address, no server name, no e-mail address, no
     secret-like assignment or token. The only URLs are github.com (the repository's own address) and github.blog
     (the runner notice). No CR, no NUL; `git diff --check` clean.
   - No template, stylesheet or script changed, so V5.8's shared CSS payload is unchanged (`dist/main.css` 31 799 B
     on every page, the console page types 39 978 B).
   - **The tests** ran on the merged branch at `859c7d8`, which is the tree merged here apart from the notes; after
     the merge, design-v5's tree is the branch's (`5f5b636`). `TEST_DATABASE_URL=…/ile_v5_l9`, `-p no:randomly`,
     one pytest: **384 passed** in 4 min 18 s, none skipped, none failed
     (`evidence/v54/w4-d/merge-1/tests_branch.log`):
     - `tests/deployment` 99;
     - `tests/security` 157 (the confidential-material guard ran with its private table);
     - `test_design_docs.py` 40; the environment template 14; the checker's tests 57;
     - both bundle-currency tests 10; the go-live calendar 3; the personal-data guard 4.
   - **Also clean:** `manage.py check` (no issue) and `makemigrations --check --dry-run` (no changes), both on
     `ile_v5_l9`, on the branch and again on design-v5 after the merge; `ruff check` and `ruff format --check` on
     the branch's three test files. The full suite is the release-candidate validation's (V5.10 gate 6).
8. **The record, and what is not done here, on purpose.**
   - Merged with `--no-ff` (`ca7bf3f`). design-v5's tree is the branch's, and nothing was rebuilt.
   - No tag: part 2 follows on the same branch, and the release tags (`pre-v5-main-2026-10`, `v2.0.0`) are the
     orchestrator's, after the fourteen gates (V5.10).
   - No push; no restart of 8780; no change to v5-live.
   - No line in `CHANGELOG_V54.md` or `live_status.json`: this is not a preview surface (DL54-77, DL54-121, DL54-152
     item 7).
   - W4-C's measurement windows ran back to back, so the test runs took their turn through
     `PERFORMANCE_BENCHMARK_LOCK`: taken atomically when free, released at the end.
9. **Open, handed on** (none of it holds the merge):
   - **F-3, real.** `core.gates`' `virtual_forum_enabled()` and `newsletter_enabled()` read the flag alone. The phase
     console declares `depends_on=("legal_pages_available",)` for both and says a closed dependency blocks the flag.
     Either a targeted fix lane before the release-candidate validation, with the fixtures `NOTES.md` lists, or the
     report's outstanding list with its class (gate 12).
   - **F-4.** The sign-in page invites a sign-up that G2 keeps closed (`templates/account/login.html`, W2-B's page,
     after W4-A).
   - **The stale rule count «13 / 3»** in `docs/platform/RULE_ENGINE_GOVERNANCE.md` (l. 233) and `docs/QA_REPORT.md`
     (l. 266, a report dated 21 September 2026). Neither file has an owner, and both are outside this merge's diff:
     for part 2's merge, with an assignment.
   - **For the owner** (`NOTES.md` «For the owner»):
     - the Forum's future-tense prescribed sentences after its event (F-1);
     - `forum_permanent_mode` at the deployment (F-2);
     - the Virtual Forum not before the legal pages;
     - Phase 3's authorisation;
     - GitHub's settings (wiki on, Dependabot off, secret scanning and push protection on).
   - **The orchestrator's CI watch.** The job names changed; the id `test` did not. The first push runs two jobs in
     parallel, and the release's commit needs both green (A-2, A-26).
   - **Once `v2.0.0` exists.** ROLLBACK.md §7 reads «at `v2.0.0`», and the tripwire then holds the released files
     only.
   - **The leftover container `ile-w4d-pg16`** (never started, holding no port). Remove it with
     `docker rm -f -v ile-w4d-pg16` when Docker answers; it was not touched at the merge, because Docker is shared.
   - **W4-D part 2.** The deletion map's last row, the dead code and DS 2026 final; then the release notes' figures
     and gates.

**Why.**
- CI runs on the server's major versions with the server's closure, so «it runs on 3.12» becomes a green run rather
  than a compile.
- The release has one name, one reference point and one restore rule in every document the owner deploys from.
- The orchestrator's report and the owner's reading of PRODUCTION_READY must rest on the same evidence: one bar, in
  the same words, in both documents.
- A delegated edit recorded as a slice tells the next steward who wrote which part of a file.
- A review file is published with the tree, so it does not carry what its own finding keeps out of it.

**Source.** The owner's V5.10, V5.9 §14–§17 and V5.5. DL54-01; DL54-77; DL54-121 item 6; DL54-152; DL54-154. Plan
§2.2 (a file not in the manifest has no writer until the steward assigns it) and §3.6 item 4. `QA/v54/w4-d/NOTES.md`,
`REVIEW_PART1.md` and `GO_LIVE_PHASE.md`. The ownership checks, the scan and the test logs are in
`C:/tmp/ile_v5_council/evidence/v54/w4-d/merge-1/`.
