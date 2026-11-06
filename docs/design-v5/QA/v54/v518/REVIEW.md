# V5.18 — integrated final review (label `v518-review`)

29 Oct 2026. Reviewer: subagent `v518-review`. I committed nothing to any branch. The scratch merge was made in a detached worktree that has since been removed.

## Verdict: FIXES_REQUIRED (2 blockers; both are steward/catalogue actions, no design work)

Every audit finding the four lanes claimed is fixed **measures fixed in the integrated tree**. No visual regression appeared in 704 public loads, 516 platform loads (9 personas) or the loader traces. Two things must still happen before the owner sees the candidate:

1. **The catalogue pass is still pending.** 22 msgids are missing in it, en and ar, among them lane B's 2FA steps. So the 2FA page shows French steps on Arabic, Italian and English pages (measured at ar 390: «Installez une application d'authentification…» under Arabic headings). `tests/i18n/test_catalogues.py` fails 4 tests. Fix: `scripts/i18n_audit.py --sync`, paste the it/en/ar texts from `docs/design-v5/QA/v518/b/NOTES.md` (no machine translation), then `--compile`.
2. **B-1 and P-9 are fixed in code but not yet in the owner's data.** Read-only SQL on `ile_v5`, today, still returns three `companies_needevent.note` rows «Démonstration : état positionné par la commande companies_demo.» and one `PrivateDocument.description` «Diplome ou titre de formation». They are visible on `/xx/espace-reserve/entreprise/mes-besoins/BF25965A42/` and `…/B0740869B4/` (all widths and languages), and on Mes documents for qa-doc-person. Fix: the steward runs `C:/tmp/ile_v5_council/servers/acceptance/fix_preview_text_v518d.py` as a dry run, then with `--apply`. The script is lane D's, outside the repository, and accepts only `ile_v5`.

Once both are done, the candidate can be reported as **FINAL VISUAL ACCEPTANCE READY**.

## How the review ran

- **Scratch merge.** `git worktree add --detach C:/tmp/ile_wt/v518-review 238dc1c`, then I merged `v518-a` (a9ad225), `v518-b` (24b3bbb), `v518-c` (b2ebd35) and `v518-d` (3d16ead) in that order. The result was 6c534f6; it is not kept.
  - **Conflicts: four, all in test files.** Two or more lanes each fixed the same T3 guard.
    - `tests/frontend/test_dashboard_browser_w3_b.py`: a×b, and b×d (the settle filter and the «moving» admission). I kept lane B's `MOVING_JS`. Lane D's `RISEN_JS` came in without conflict and is now unused.
    - `apps/pages/tests/test_browser.py` (a×c, tiles «nothing loops»): I kept lane C's version (DocumentTimeline-only, plus no infinite iterations).
    - `tests/frontend/test_browser_w3_f1.py` (a×c, RADII_JS): I kept lane A's composed opacity **and** lane C's `.lume-veil` skip.
  - **The steward must resolve these the same way.** No production file conflicted.
- **Built bundles are in sync with the sources.** After the merge, `node scripts/build_frontend.mjs` and `build_css.mjs` left the tree clean, so the committed `dist/` matches the merged sources.
- **Server.** Port 8787 served the review tree with `config.settings.dev`, `ILE_DESIGN_PREVIEW=1`, `ILE_DESIGN_PREVIEW_PORT=8787` and `ILE_REFERENCE_DATE=2026-10-03`, on database `ile_v5_l7` (0 pending migrations, 19 accounts). The launcher was a copy of the acceptance launcher, which adds the 5 acceptance personas, so all 9 are present. Launcher and settings: `.work/v518-review/seed/`.
- **Headed Chromium (chromium-1234) under `C:/tmp/ile_locks/CHROMIUM_LOCK`, label `v518-review`.** Five sessions, each under 25 minutes, released after each run:
  - sweep: about 12.5 min;
  - verify + loader: about 9 min;
  - two platform sessions;
  - one extra session: 19:40:54–19:42:10.
  No stale lock was taken over.
- **Tests (headless, database `ile_l7r`).** I ran every test file the four lanes changed, plus test_rtl_static, test_design_docs, test_catalogues and the `_fronte.css` token test: **602 passed, 6 failed** (details below). I started a full non-browser run and stopped it at about 10 % because it would have taken hours. **Stop incident.** The stop matched every python process whose command line contained `pytest` and `not browser`, and it killed four. A single run of mine accounts for at most two (the venv launcher plus its interpreter), so **two of the four may have belonged to another session's pytest**. Please check whether any lane or steward run on 127.0.0.1:5439 ended without a result around that time, and rerun it if so.
- **Crawl.** Read-only GETs as anon (442 URLs) and as each of the 9 personas (221–359 URLs each). The visible text and attributes were scanned for the §7 and §8 terms.
- **Evidence.** All in `C:/tmp/ile_v5_council/.work/v518-review/`:
  - `sweep/` (704 JSON rows, plus shots at 1440/768/390/360);
  - `findings/verify.json` and shots;
  - `lume/lume.json` and frames;
  - `plat/plat_all.json`, `plat/plat_qa-doc-person.json`, `plat/extra/`;
  - `crawl.json`;
  - `pytest_targeted.log`.

## Audit findings — verified in the integrated tree

| Id | Status | Measured |
|---|---|---|
| B1 | **Fixed** | The compass glyph never overlaps the label in 32 cases (fr/it/en/ar × 1440/1024/768/390 × motion/reduced). For example, fr 1440: glyph x92–128, text x164–297. ar 1440: glyph 1296–1332, text 1195–1260. With motion the result is identical to the reduced-motion still. |
| B2 | **Fixed, one 5 px residue** | Page-header CTA bottom ÷ viewport height, worst case per page: Entreprises 0.95, Institutions 0.81, Universités 0.87, Parcours 1.007. The only miss is **ar 375×667 Parcours**: the CTA runs 620–672 against 667, so its top 47 of 52 px are visible. Polish item 1. |
| B3 | **Fixed** | The Entreprises mega panel shows «Besoins professionnels» with its title only, under the locked door gloss. No duplicate sentence (shot `findings/mega_fr_1.png`). |
| P7 | **Fixed** | Breadcrumb «Accueil» on `/fr/le-projet/` under a coarse pointer: `::after` is 44 px tall, and the link answers 21 px above and below its centre in fr and ar. On a fine pointer there is no extension (correct). |
| P8 | **Fixed** | `apps/pages` test_the_hero_holds_its_geometry passes (48 px peek). `--utility-h: 0px`. |
| P10 | **Fixed** | ar `.form-field__optional` and `.steps-head__tile` are 14 px at 1440 and 390. No text under 13 px in `main`. |
| P11 | **Fixed** | Sheet language links are 44 px tall at 768/430/390/360 in all 4 languages, with fine and coarse pointers. No sheet overflow. |
| P12 | **Fixed** | Login → platform now engages the central veil at the click (`html.lume-go` at 24–65 ms). The mark is centred: 712/1440, 376/768, 188/390, 172/360. It arrives on the dashboard; under reduced motion it is the still doorway. The time before arrival (1.5–2.2 s) is the server's sign-in, not an added delay. |
| T1 / T2 | **Fixed** | `_fronte.css` token and RTL static tests pass. |
| T3 | **Fixed** | Routing floor 23 and gated legal pages, seat label, c-rise guards, three corners and tiles all pass. **test_dashboard_browser_w3_b passes in full, including the 4 bridge cases and 390x844-fr.** |
| B-1 | **Code fixed, data NOT applied** | Blocker 2. |
| P-1 | **Fixed** | Forum head at load: `reveal-rule` on the night band, `rise-in` on text, eyebrow, title, lead and sommaire title, plus 5 sommaire rows. Nothing is still running after 2.75 s. Under reduced motion only the loader's still remains. |
| P-2 | **Fixed (FR); needs the catalogue** | 2FA is a three-step panel with the shield tile and a «non activée» chip, and c-rise runs on the column. In it/en/ar the steps are French until the catalogue pass is done (blocker 1). |
| P-3 / m-5 | **Fixed** | qa-fresh-person in ar/it/en shows the translated H1 (for example «لوحة المتابعة», with the lang attribute matching). French keeps the locked head. |
| P-4 | **Resolved by removal** | The Personnes panel has six uniform title-only entries. It reads evenly (`findings/mega_fr_0.png`). |
| P-5 | **Fixed** | The empty Mes documents shows the ILE empty-state tile, the documents glyph and «Déposer un fichier hors exigence». |
| P-6 | **Kept, correctly** | `IT00000000000`, `+39 0000 000000` and `referent@example.test` are reserved or example values. The run's rule forbids plausible fake identifiers, so leaving them is right. **However**, see polish item 6 for `RO-187264`. |
| P-7 | Information only | Privacy open fields, as decided under V5.16 and V5.17. |
| P-8 | **Fixed** | 0 hub 404s in the anon crawl, against 7 before. |
| P-9 | **Data NOT applied** | Blocker 2. |
| M-2 | **Fixed** | The company's Mes besoins, need detail and Mon entreprise pages have the atrium head (seal, eyebrow, phone band) and c-rise. Nothing moves under reduced motion. |
| m-6 | **Fixed** | `_platform.css` has no gradient; they moved to `_platform-grounds.css`. test_design_docs passes. |

## V5.18 §3 — responsiveness

The 704-load sweep covered 22 public pages × 8 widths × 4 languages.

- **Horizontal overflow:** 0. The only overflow is Django's DEBUG technical 404, a dev artefact.
- **Desktop navbar:** one row with no clipping at 1024, 1280 and 1440 on every page and in every language. The header is 65 px and there is no burger.
- **Mega menus:** all panels stay inside the viewport.
- **Phone sheet:** full height. It mirrors in Arabic, and its doors expand inside the width.
- **Forms at 360:** no control under 40 px. The only exception is the off-screen honeypot `website_url`.

**Platform: 9 personas.**
- Coverage:
  - fr at 1440/768/390/360, ar at 1440/390, it at 390, en at 1280;
  - every rail destination at fr 1440, fr 390 and ar 390;
  - account security pages and the company's need detail pages.
- **Results:** 0 overflow, 0 text under the floor. Every console page has the atrium head and motion, and none moves under reduced motion.

## V5.18 §4 — Lume loader

I traced 30 transitions: public→public, language change, public→login, login→platform and platform→platform, at fr 1440, ar 390, it 768 and en 360, plus ar 1280 and fr 390 under reduced motion.

- **Every transition shows the branded veil, centred.** The public veil's mark is at vw/2 ± 8 px. Platform→platform centres the veil on the workspace pane (x 836 at 1440, beside the rail), which is the scoped console veil as designed.
- There is no header-only cue and no added delay.
- Under reduced motion the veil is the still doorway.

## V5.18 §5 — motion

- Public heads now animate in every family. Forum is fixed (P-1).
- Console pages, the company space and the account/security column rise once with a finite animation.
- Nothing loops; the tiles test passes. Reduced motion leaves only the loader's still.

## V5.18 §7 / §8 — terminology and unfinished content

- **Terminology:** no «variant», «fixture», `role:` or «demo» in product text.
  - «Persona» appears only as the correct Italian account type and in one Italian photo alt text.
  - `qa-*@example.test` appears only as the signed-in preview account's own e-mail.
- **Unfinished content:** 0 visible surfaces and 0 empty `href`s.
  - «Placeholder» matches only `placeholder=` attributes.
  - «À venir» is only the deadlines heading.
  - «Parcours en construction…» and «A project under construction» are the deliberate legal hedges.
- **Owner-visible demonstration text:** only B-1 and P-9, until blocker 2 is done.

## Tests (headless, `ile_l7r`): 602 passed, 6 failed

| Test | Attribution |
|---|---|
| `test_catalogues` × 4 | **Blocker 1.** Catalogue pass pending (22 msgids). |
| `test_content_pages_browser_w3_f2::test_every_content_page_holds_the_grammar…` | The formwork pages' corner set (12/6/8/999/4/6.4 px) on contact, recueil and collaboration. This is lane B's design, **left for the Director's ruling (DL54-173)**. It was already red on design-v5 and is unchanged by this wave. |
| `test_o14_lint::test_the_one_check_of_the_templates…` | `templates/partials/header.html` uses `check` (lane A's header). Already red on design-v5. Lane A must either seat it in the lint's list or replace the glyph. |

## Polish (does not block the owner's review; for the steward or the next wave)

1. **The Parcours CTA misses by 5 px at ar 375×667** (620–672 against 667). Fix: trim one spacing step above `.via__action` below 24rem, or shorten the lead's top margin in Arabic.
2. **On phones the via title is shown after its own button** (fr and ar 360/390 Parcours: button, then «Identifiez la voie régulière à explorer»). This comes from the CSS `order` swap B2 introduced. Visual order and DOM order now differ (WCAG 1.3.2 / 2.4.3 risk). Fix: also move `.via__title` before the action with `order`, or drop the title's order so the title, the button and the text read in sequence.
3. **Lane B's `_conto-console.css:36` writes `c-rise … both`, against lane A's V5.18 rule «backwards, never both»** (`_motion.css:177`, `_reveal.css:393`). With `both`, the transform stays in effect after the rise ends, so the column remains a containing block for positioned descendants. No break was measured (`.tfa-steps__step` is `position: relative`). Fix: change it to `backwards`.
4. **Stale comments in `test_dashboard_browser_w3_b.py`** still say c-rise «fills both». After lane A's change, a finished c-rise leaves `getAnimations()`, so lane B's `MOVING_JS` and lane D's `RISEN_JS` admissions are now redundant but harmless. Fix: drop `RISEN_JS` when the steward resolves the merge.
5. **The «Étape n sur 7 — …» case chip wraps to two lines at fr 390/360** (qa-doc-person dashboard and Mes dossiers, qa-waiting-person Mes dossiers 360, it 390 Mes dossiers). It wraps as a 12 px-radius block 44 px tall. It reads acceptably, and the w3-b test passes on its own fixture. Lane D may ellipsise the step title on phones.
6. **The preview data has `RO-187264` as the company's registration number** (`apps/designpreview/preview_data.py:63`, from 984117c, an earlier wave). It has the shape of a Rovigo REA number, so it could belong to a real company, against this run's rule. Fix: use a clearly reserved value, as done for the VAT number.
7. **In the Institutions mega panel, Arabic «منتدى Vénétie–Maroc» has no second line**, while French has «Dialogue juridique…». The line is missing in Arabic.
8. **Sector labels show in French on en/ar** («Bâtiment et travaux publics» on Mon entreprise and Mes besoins) while Italian is translated. These are data or catalogue labels.
9. **Ownership crossings to record at the merge** (as the lanes declared):
   - lanes A, B and D all edited `test_dashboard_browser_w3_b.py`;
   - lanes A and C both edited `test_browser_w3_f1.py` and the `apps/pages` tiles test;
   - lane B edited `templates/portal/documents.html` and the new `templates/mfa/index.html`, and placed the account column's c-rise in `_conto-console.css`.
10. **Information:**
    - the locked French CTA «PROPOSEZ UNE COLLABORATION» on the ar/it/en organisation dashboards;
    - the documents' requirement texts in French on other languages (data);
    - the unreferenced `static/js/dist/chunks/chunk-ESW3PKTX.js` (lane A's note).

## Scores — integrated families (V5.15 §26, 1–5)

| Family | Score |
|---|---|
| Home, navbar and mega menus | 4.5 |
| Lume loader (all five transitions) | 4.5 |
| Public family heads (Parcours, Entreprises, Institutions, Universités & Formation) | 4 |
| Content pages (FAQ, Glossaire, Vivre, Forum, Le projet) | 4 |
| Login, signup and forms | 4 |
| Person space (dashboard, case file, documents, journey, Academy, Guichet) | 4 |
| Company space | 4 (4.5 once blocker 2 is done) |
| Institution / University spaces | 4 |
| Profile and security | 3.5 (4 once blocker 2 is done) |
| Motion across families | 4 |
| RTL | 4 |
| Terminology and unfinished content | 4.5 |

Platform Refinement meets the V5.18 §1 target of 4 or more. No family scores below 4 once the two blockers are cleared.

## Clean-up

- Server 8787 stopped.
- The `node_modules` junction was removed before the worktree, so design-v5's own `node_modules` is untouched.
- `C:/tmp/ile_wt/v518-review` removed with `git worktree remove` and pruned.
- The `.env` copy left with the worktree.
- `ile_v5_l7` was only read: the crawl's GETs, plus the persona switch's own sessions.
