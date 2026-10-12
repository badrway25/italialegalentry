# W1-K calibration — the UX chair (scales: UX · Mobile)

Label **w1k-ux** · 5 October 2026 · blind calibration on the shared stills
`C:/tmp/ile_v5_council/evidence/v54/w1-k/stills/` (INDEX.md), plus this chair's own harness for S2 and S3 · plan
`docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.1 (design-v5 `889c6b1`) · DL54-03, DL54-16. Read-only: no git write; no
product or proof file touched.

## Scores

| Surface | UX | Mobile |
|---|---|---|
| **S1**: the V4 reserved area, person account (`v54/base`) | **3** | **3** |
| **S2**: the gate-0 login comp «Il varco» | **4** | **3** |
| **S3**: H-E as built (the frozen V5.3 archive) | **4** | **4** |

Scale (Hd §8.3 l. 610 = plan §3.1 item 1): 1 fails · 2 weak · 3 competent, below the bar · **4 at the owner's bar**
(«credible alongside excellent international digital products», V5.1 §96) · 5 above it. Whole numbers, no means.

**Instruments (§3.1 item 2).**
- **UX:** the family's acceptance list (a calibration surface has none). On console pages (S1): LA-9's five answers
  and one primary, read on the first-viewport stills at 1440, 1366 × 768 and 390. On public pages (S2, S3): RH-6's
  chain of questions.
- **Mobile:** the phone set 360 × 800 · 375 × 667 · 390 × 844 · 412 × 915 · 844 × 390, **emulated** (headless
  Chromium, DPR 2, mobile + touch; no real device, no Safari).
- **Rule text behind both:** TS §6 (RH-5, RH-6), §7 (LA-9, LA-11), §16 (IN-3, IN-7, IN-8, IN-9, IN-11, IN-12) and
  §17 (RE-1, RE-3, RE-4, RE-5, RE-6, RE-7).

## Evidence — one line per score

| | Scale | Score | The still, and what in it |
|---|---|---|---|
| S1 | UX | 3 | `S1/S1-documents-fr-1440x900.png`: the document workspace answers «what is missing» and «who is responsible», but it has no primary (three equal outline buttons; «Remplacer la pièce» also sits on the «Déposé» passport) and no «what changed». The dashboard (`S1-dashboard-fr-1440x900.png`) gives 5 of 6 at 1440 and loses «what is missing» at 390. LA-9 tally: 19 ✓ · 10 ◐ · 7 ✗ of 36; «what changed» 0 of 6. |
| S1 | Mobile | 3 | `S1/S1-documents-fr-390x844.png`: the first screen goes on a serif title, a three-line lead and the progress card. It shows one piece without its act, and the «À remplacer 1» chip is off-screen in the scroller. The tab bar label hyphenates («Communica-tions»), and the header has a second menu trigger (☰). The pages reflow without overflow. Only 360 and 390 were seen. |
| S2 | UX | 4 | `S2/S2-login-fr-1440x900.png`: every block answers its own question, in the visitor's order: identity, the no-account path, the fields with «Mot de passe oublié ?» and a working show/hide, one primary, and «Mes données sont-elles protégées ?» answered in words. The error state (`w1k-ux/harness/S2-error-fr-1440x900.png`) shows a specific summary with the focus ring on it and keeps the e-mail. |
| S2 | Mobile | 3 | `w1k-ux/harness/S2-844x390.png`: in landscape, no field is in the first screen (letterhead, door band, h1, lead). At 375 × 667 only 17 px of the primary shows. On every phone the fields are 15 px and the labels 14 px (IN-8, RE-4). Portrait 360, 390 and 412: form and primary are inside the first screen. |
| S3 | UX | 4 | `S3/S3-rest-fr-1366x768.png`: one viewport answers what it is (the promise), what to do first (one primary), whom it is for (four whole-tile entrances) and which path it is (MAROC → ENTRÉE EN ITALIE), and the next chapter peeks on a whole line. Only chapter 01's four «ÊTES-VOUS … ?» repeat a question already answered (`S3-rest-fr-1440x900-full.png`). |
| S3 | Mobile | 4 | `S3/S3-rest-fr-360x800.png` and `w1k-ux/harness/S3-375x667.png`: the phone has its own first screen. The promise, the primary, the model as a rail beside the door and the four entrances 2 × 2 are all inside at 360, 375, 390 and 412. 0 targets are under 44 px in portrait. Landscape keeps the entrances, the primary and the door. |

## The instruments as run

### S1 — LA-9 on the first-viewport stills

Columns: W where am I · N what is next · M what is missing · R who is responsible · C what changed · P the one primary.
Marks: ✓ answered · ◐ partly · ✗ absent.

| Still | W | N | M | R | C | P |
|---|---|---|---|---|---|---|
| `S1-dashboard-fr-1440x900.png` | ✓ | ✓ | ✓ | ✓ | ◐ | ✓ |
| `S1-dashboard-fr-1366x768.png` | ✓ | ✓ | ◐ | ✓ | ◐ | ✓ |
| `S1-dashboard-fr-390x844.png` | ✓ | ✓ | ✗ | ✓ | ◐ | ✓ |
| `S1-documents-fr-1440x900.png` | ◐ | ◐ | ✓ | ✓ | ✗ | ✗ |
| `S1-documents-fr-1366x768.png` | ◐ | ◐ | ✓ | ✓ | ✗ | ✗ |
| `S1-documents-fr-390x844.png` | ✓ | ◐ | ◐ | ✓ | ✗ | ✗ |

- **C** is ◐ at best. The only change shown is «Brouillon depuis le 21.09.2026»: no event, and no date for the last
  deposit or review.
- **P** on the dashboard is «Continuer». It sits at the top right, away from the card it serves, and doesn't say what
  it continues.
- **R** shows two «Responsable» values (La personne · Professionnel) without saying what each is responsible for.
- **At 1366 × 768** the fold cuts the «3 pièces demandées» line, and the rail collapses to unlabelled icons.
- **Documents:** the h1 says «Mes pièces», the rail says «Mes documents», and the breadcrumb stops at «Espace réservé».
  The act the person needs (the «À remplacer» row, «Scan partiel : page 2 manquante») carries the same weight as
  «Remplacer la pièce» on a passport already deposited.
- **«Mon parcours»** (outside LA-9's three page types; `S1-journey-fr-1440x900-full.png`) is a list of
  pre-evaluations, while the dashboard's «Mon parcours» is the seven-station band. Its next act («Reprendre le
  questionnaire», for a questionnaire still «En cours») is at the bottom of the page, after the informative steps,
  outside the first viewport.
- **The request record** (`S1-request-fr-1440x900.png`) is clear, but doesn't say what happens next.

### S2 — RH-6: the question each block answers

| Block (`S2-login-fr-1440x900.png`) | The question it answers |
|---|---|
| Letterhead: lock-up, IT · FR · EN · ع, «Retour à l'accueil» | Is this ILE, in my language? Can I go back? |
| The night stage: door, key, steps | Is this the entrance to my space? (answered by the signature, without words) |
| Help line · promoter line | What if I am stuck? Who runs this? |
| «Espace réservé», «Connexion», «Si vous n'avez pas encore créé de compte… enregistrer» | What is this page? I have no account — what now? |
| Fields, «Mot de passe oublié ?», «Afficher le mot de passe» | How do I get in? I forgot. What did I type? (the toggle turns to «Masquer le mot de passe», the field to text) |
| «Se souvenir de moi», the primary «Connexion» | The act itself; one primary |
| «Mes données sont-elles protégées ?» | Is my data safe? («Oui», RGPD, EU servers, never passed on without consent) |

No block is without a question.

**States.** The error page (`w1k-ux/harness/S2-error-fr-1440x900.png`, `…-390x844.png`) draws the focus ring on a
summary in an alert region, names the problem and keeps the e-mail.

**Held at 4, not 5, by:**
- **The wait after «Connexion» has no words.** It is a key turning, a line and a glyph: no status text, no
  `aria-busy`, and the label doesn't change (IN-7, IN-12; `w1k-ux/harness/S2-1440-entrance-0450.png`).
- **Tab order.** The help link (stop 8) comes before the form, and «Mot de passe oublié ?» (stop 11) sits between the
  e-mail (10) and the password (12).
- **On phones the help line comes before the task.**
- **The data answer stays French on the Arabic page** (`S2/S2-login-ar-1440x900.png`). It is lawful under RE-6, as a
  whole block.
- **Wording:** the label «Courriel» sits over the placeholder «Adresse e-mail», and «Privacy Policy» appears in
  English inside a French sentence.

### S3 — RH-6

| Block (`S3-rest-fr-1440x900.png`, `…-full.png`) | The question it answers |
|---|---|
| Utility bar: promoter, «Espace réservé», languages | Who runs this? Where do I sign in? |
| The headline | What is this? («Le parcours régulier vers l'Italie, de l'orientation à l'intégration.») |
| Primary «Découvrir le questionnaire d'orientation» · «Comment fonctionne l'orientation» | What do I do first? |
| «Les quatre accès de l'écosystème»: four whole-tile links (352 × 146, the Tab stops right after the two actions) | Is it for me? On hover the tile is framed, its call appears and its route to the door lights up (`w1k-ux/harness/S3-1440-hover-entrance.png`) |
| The niche and the model band | What is the path, and where does it end? |
| «L'écosystème» statement | What is ILE exactly, and who builds it? |
| Four «ÊTES-VOUS UNE … ?» with their calls | Is it for me? **again**: the one block that doesn't raise the next question (still within RH-5's «twice above 1.5 screens») |

- **Motion gates nothing.** The first paint is complete, and the held frames change 2.4–10.6 % of the screen (INDEX).
- **Outside the archive:** the guarantee, the proof and the Forum's date. The archive covers the first screen and
  chapter 01 only.
- **The chrome is inert and not scored.** The navbar's chevrons and the phone «Menu» do nothing in the archive
  (`aria-expanded="false"`, no panel; a tap changes nothing, `w1k-ux/harness/S3-390-menu.png`). The chrome is not
  the hero's.

### Mobile — the phone set

| Size | S1 (stills only) | S2 | S3 |
|---|---|---|---|
| 360 × 800 | Dashboard: h1, ref, «Continuer», next action, then the Dossier card («Brouillon» a second time); no documents. Request: the header title is cut («[redteam for…») | Form and primary inside; the band (door, help) above them | Promise, primary, model rail, door, four entrances and the fold label, all inside |
| 375 × 667 | not seen | The primary's top is at y 650 of 667 | All of the above inside, with the promise on two lines |
| 390 × 844 | As at 360. Journey: title, lead, notice, no result. Documents: one piece, its act below the fold | Form and primary inside | As at 360 |
| 412 × 915 | not seen | Form, primary and the data answer inside | As at 360; the chapter title peeks |
| 844 × 390 | not seen | No field in the first screen | Promise, primary, four entrances and door; the model wraps into two rows of bullets |
| measured | 0 overflow (INDEX); the tab bar marks the current place; two menu triggers; «Communica-tions»; lone «—» lines; two left edges (36 px and 16 px) on journey and request. Arabic: «.Scan partiel…» reordered, and a Latin eyebrow off the reading edge | 0 overflow at all five sizes. Fields 44 px, primary 52 px. Inputs 15 px, labels 14 px, lead 15 px, data answer 13 px. `autocomplete`: email / current-password | 0 overflow at all five sizes. 0 of 13 targets under 44 px in portrait; 6 of 19 in landscape (language links 24 × 44, «Espace réservé» 103 × 24). Chapter 01 sentences 15 px; model labels and calls 13 px capitals. The primary stays on one line at 360 |

## What would move each score one point

- **S1 UX → 4:**
  - give «what changed» a place in the first viewport (the last event, dated);
  - make the act the person needs the workspace's one primary;
  - name the primary for what it does;
  - keep the documents' count above the fold at 1366 × 768 and 390;
  - give «Mon parcours» one meaning.
- **S1 Mobile → 4:**
  - a phone first screen for each page (the next act and what is missing, before the Dossier card; the first piece
    with its act);
  - one menu trigger;
  - tab labels without hyphenation;
  - label or remove the «—» lines;
  - one left edge.
- **S2 UX → 5:**
  - say the wait in words;
  - Tab from the e-mail to the password;
  - put the help after the form on phones;
  - give the data answer in Arabic.
- **S2 Mobile → 4:**
  - 16 px fields and reading text on phones (IN-8, RE-4);
  - a landscape layout with the first field in the first screen;
  - the primary inside 375 × 667.
- **S3 UX → 5:**
  - chapter 01 asks the next question (the guarantee, what happens after the questionnaire) instead of asking for the
    audience again;
  - the chrome built.
- **S3 Mobile → 5:**
  - 16 px reading text in chapter 01;
  - keep the model as a line in landscape;
  - keep «Universités & Formation» clear of its arrow at 360–375.

## How I read the anchors (for later chairs of this lens)

1. UX 4 = the instrument passes with only minor findings: a console still gives all five LA-9 answers and one primary at 1440, 1366 × 768 and 390; on a public page every block raises a new question, and the error and wait states exist.
2. UX 3 = it works and most answers are there, but one answer or the primary is missing at a named size, or a block repeats a question; 2 = two or more answers fail at desktop, or a task lacks its control; 1 = the task cannot be done.
3. Mobile 4 = at all five emulated sizes the task and its primary are in the first screen, with no overflow, 44 px targets, and 16 px fields and reading text (RE-1, RE-3, RE-4, IN-8); one size failing, or a phone rule broken across the page, holds it at 3.
4. Score behaviour and comprehension only; beauty, premium and originality are other scales, so a surface the owner finds visually below the bar can still be at the bar here, and the reverse.
5. Name any size or state you did not see, and never assume it; note a proof's out-of-scope chrome and leave it out; use whole numbers and name the still behind each score.

## Blindness — what I read before scoring

- **Read before scoring:**
  - plan §3.3 item 2, lines 1730–1733, which my brief told me to read. They name the three surfaces and quote the
    owner's verdicts on two of them: the V4 dashboard ≈ 3 / 5; the login «concept good, left side too static, form
    too simple».
  - DL54-16, lines 205–213, which say the owner judged all three below 4 on visual, premium and originality.

  I stopped reading both at those lines.
- **Not read:**
  - the rest of item 2 and the rest of DL54-16;
  - he_design.md §8.3 beyond its scale line (l. 610); the table below that line holds the design chair's H-E scores;
  - any hero-council report or gate-0 review;
  - TS §20 and §26 (verdicts);
  - the directive's lines on these surfaces;
  - the comps' notes;
  - the other chairs' W1-K files and evidence folders.
- **Effect:** those verdicts are about other scales. My scores come from the tallies above. The two UX 4s are where
  the instrument passes, whatever the overall verdict on those surfaces.
- **Note for the next calibration round:** the instructions overlap. The plan writes the owner's verdicts into item 2,
  and §8.3 puts its anchors in the same section as H-E's scores. The instrument text should be kept apart from the
  expected results.

## Method, limits, files

- **S1** was seen only through the stills: fr at 1440 × 900, 1366 × 768, 390 × 844 and 360 × 800; ar at 1440 × 900 and
  390 × 844; four screens. 375 × 667, 412 × 915 and 844 × 390 were not seen.
- **S2 and S3** were also opened in this chair's harness, `w1k-ux/ux_probe.py`:
  - **Server:** `C:/tmp/ile_v5_council/proof` served read-only on 127.0.0.1:8843: GET only, the proof harness's CSP
    header, dot-folders refused, nothing imported from `proof/`.
  - **Browser:** headless Chromium (Playwright 1.63, the repository venv), profile
    `C:/tmp/ile_v5_council/.profiles/w1k-ux/<run>/`, deleted after each run (the folder is gone).
  - **Lock and ports:** the benchmark lock was checked before every launch; it was never present (0 s waited). Ports
    8780 and 9222/9223 were never loaded.
  - **Interaction:** nothing typed. On S2 I pressed «Afficher le mot de passe» and «Connexion» (`type="button"`, the
    comp's own instruction; nothing is sent). On S3 I pressed the navbar's «Personnes» and the phone «Menu». I viewed
    `login/error.html` and `error-ar.html`.
- **Limits:**
  - Emulation, not devices. There is no Safari, so iOS zooming on the 15 px fields is a rule breach (IN-8), not an
    observation.
  - S3's Arabic copy is locked French by rule (declared), so I read the Arabic chain for layout only.
- **Files** in `C:/tmp/ile_v5_council/evidence/v54/w1-k/w1k-ux/`:
  - `harness/`: 39 PNG. The phone set of S2 and S3 at five sizes, first viewport and full page. For S2: the Tab stops,
    hover, toggle, entrance frames and error pages. For S3: hover, focus, nav and menu.
  - `probe_log_phones.json`, `probe_log_s2int.json`, `probe_log_s3int.json`, `ux_probe.py`.
