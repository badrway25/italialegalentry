# W4-A shipped — 17 October 2026

**Mobile + RTL sweep — every page on a phone and in Arabic: the chrome, the first object, the targets, the overflow,
the mirrors.** Tag **`v54/w4-a`** (design-v5 `49be845`, the status commit, as for the earlier families); merge commit
`b067c7b`. The owner's preview on http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at
01:25 (down from 01:24:58, answering at 01:25:12) and verified by request (`verify_8780.log`: 34 requests, every one as
expected; no traceback in the server log). Steward's merge, label `w4-a-merge`, under `DESIGN_V5_MERGE_LOCK` — a retry:
the first attempt (16 October, 22:16–22:48) stopped at the tests because the shared database was down; this one ran on
the database bridge (`evidence/v54/SERVERS.md`, «16 Oct 2026 — the database bridge») from 00:20:34 on 17 October.
Reviewed once and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` were both SHIP_AFTER_FIXES with no P0, and every finding
was fixed in the one fix pass (`NOTES.md` «Review fixes»); the steward's targeted run on the lane database, the
accessibility check's runner on the QA records and the requests on 8780 checked the merged tree. The record: DL54-157
(the family's decisions) and DL54-158 (the merge).

## What shipped

W4-A composes no page: it swept every page the product draws — 106 page states, in French and in Arabic, on eight phone
sizes, at 320 px and under a mouse — and fixed each defect in the file of the family that draws it.

- **The phone's frame and first screen.** The phone's chrome stays within the plan's 120 px (114 on the persons' and
  the company's pages); no page is wider than the phone from 320 to 932 px; the page's first object is in the first
  screen, the error pages with the phone on its side included (the door moves to the row's end).
- **Every isolated target under a finger is 44 × 44** (SP-8, read with WCAG 2.5.8's exception for a link inside a
  sentence): the footer's links, the help line's address, a notice's e-mail address (the go-live notice on every public
  form included), the passages' forward links, the consent's privacy link, «Profil», a loose file's «Supprimer», the
  documents' links, the lock-up at 320, the Stepper of «Ma situation» from 360; under a mouse, 24 px at least.
- **Arabic, the other direction.** The company's phone and e-mail read left to right («+39 0000 000000»); a name written
  in the other direction than the page — a file, an answerable party, a reference, a step's words, the company's own
  name in its head — stands on the page's reading edge; a French title in the console's phone bar is cut at its own end;
  the Forum's video controls never mirror; a reference's point no longer closes an Arabic line; a French sentence an
  actor or the team wrote on the selection's pages keeps its period at its end.
- **The keyboard on a phone.** A stop that Tab brings in from below keeps its whole focus ring on the public pages (86
  cut rings → 0); the console phone bar's account ring stays inside the bar.
- **Reading on a phone.** The passage's station words at 16 px below 64rem on every page that draws «la linea»; the
  team's strings the review named go through the typography filter (no phone line starts with «»» or «;»).
- **Shared CSS (V5.8): lighter again.** `main.css` 31 799 → **31 637 B** gzip on every page (−162); the console page
  types 39 978 → **39 798 B** (−180); every page type lighter, paid by deleting rules nothing draws.

## The merge

- **Sync**: design-v5 `b06ea1e` was already the branch's merge base — «Already up to date», no conflict; the merge's
  tree is the branch's own.
- **Ownership** (`fd338df`, on the branch): the one path no family held, `static/css/dev/showcase.css`, is W4-A's slice
  in the manifest (the showcase's phone layout only; its palette stays unassigned). After it: 5 inside, 2 slice, 13
  generated, 37 delegated (each read in its owner's file), and the manifest itself (the steward's own write), no family
  path outside; `--validate`: coherent, 30 families, 784 entries. The 2 770 added lines scanned: no external URL, no
  inline style or script, no secret, no CR, no NUL.
- **Bundles** rebuilt from a clean dist on the branch and on design-v5 after the merge: byte for byte the committed
  trees both times, no build commit. `regen_design_inventory.py --write`: six DS 2026 §2 weights follow the tree
  (`442e41c`). The capture report is unchanged (none of its recorded values can move: W4-A's rules apply under a finger,
  at ≤ 20.5rem or on a phone on its side).
- **Tests** (lane `test_ile_v5_l6` on the bridge, one pytest and one browser of the steward's at a time, no run crashed;
  V5.5: targeted, not the full suite; `C:/tmp/ile_v5_council/evidence/v54/w4-a/merge/tests_*.log`): on the branch,
  non-browser **2 028 passed**, 2 xfailed (the two standing ones), and in headless Chromium **335 passed** — every
  browser file of the brief, the ten the outage had left to the merge step included —, 0 failed, 0 skipped; on design-v5
  after the merge **277 passed** (bundles, docs, ownership, inventory, the showcase, the area's static half, O14, RTL
  static), then the preview's, the checker's and the docs' tests with the new status files **394 passed**.
  `manage.py check`, `makemigrations --check` and `ruff check .` clean.
- **The QA records** (NOTES' hand-off to the merge step): the accessibility check's runner under a finger on 14
  signed-in page states × fr, ar × 390, 360, 320 and 844 × 390 — 106 loads: no overflow, axe 0 violations, the first
  object in the first screen, every target 44 × 44 but the two recorded exceptions at 320, nothing new
  (`evidence/v54/w4-a/merge/a11y-qa/`; DL54-158 item 9).
- **Shared CSS gate (V5.8)** passed: both shared bundles lower, every page type lighter; every ceiling lowered to the
  merged weight (DL54-158 item 5, the table of every page type).
- `live_status.json`: the family row w4-a — state v5, its review as the decision, the tag. No surface key changes (W4-A
  composes no page). `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780

All checked by request after the restart (`verify_8780.log`). A phone-sized window (or the preview's phone frame) shows
what changed; Arabic under `/ar/`.

- http://127.0.0.1:8780/__design-v5/ — the strip names `v54/w4-a`; the index http://127.0.0.1:8780/__design-v5/index/
  lists the family with its review (http://127.0.0.1:8780/__design-v5/decisioni/w4-a/REVIEW.md).
- Public pages: the home http://127.0.0.1:8780/fr/ and http://127.0.0.1:8780/ar/ (the footer's links under a finger, the
  ring from Tab), the FAQ http://127.0.0.1:8780/fr/faq/, the contact form http://127.0.0.1:8780/fr/contact/formulaire/
  (the go-live notice's address), the training page http://127.0.0.1:8780/fr/formation/ (the station words, the forward
  links), the Forum's registration http://127.0.0.1:8780/fr/forum/inscription/, orientation
  http://127.0.0.1:8780/fr/orientation/, the persons' door http://127.0.0.1:8780/fr/parcours/, the product's error page
  http://127.0.0.1:8780/_errors/404/ (a phone on its side: the door at the row's end; an unknown address on 8780 shows
  Django's debug page, DEBUG being on there).
- Through the preview's persona switch («Personas» → «Entrer», no password): as «Personne avec dossier»
  (qa-doc-person) the dashboard http://127.0.0.1:8780/fr/espace-reserve/ («Profil» on its edge, the phone bar's account
  ring), «Mes pièces» http://127.0.0.1:8780/ar/espace-reserve/mes-documents/ (the names on the reading edge) and «Ma
  situation» http://127.0.0.1:8780/fr/espace-reserve/ma-situation/ (the Stepper's 44 px columns from 360); as «Personne,
  conditions non acceptées» (qa-person) the help desk http://127.0.0.1:8780/ar/espace-reserve/guichet/ (the French
  subjects and the references on the Arabic reading edge) and «Mon parcours»
  http://127.0.0.1:8780/ar/espace-reserve/mon-parcours/ (the saved result's French title on the reading edge); as
  «Entreprise — Cantiere Adriatico» (qa-company) the company's dashboard
  http://127.0.0.1:8780/ar/espace-reserve/entreprise/ (its name an isolate on the reading edge) and «Mon entreprise»
  http://127.0.0.1:8780/ar/espace-reserve/entreprise/mon-entreprise/ (the e-mail and the phone left to right).

## Not done

- **Measures not made at the merge**: no browser on 8780 (by rule; the steward's browser runs were on the lane 8786);
  the accessibility runner's pointer pass at 1440 and the performance comparison were not re-run on the QA records (no
  script changed, both shared bundles are lighter, and the check measured both on this code); Firefox, WebKit, a real
  phone and a screen reader were never run (W4-C's cross-engine pass).
- **The lane's records changed under the bridge**: `ile_v5_l6` is a copy of the rebuilt `ile_v5`, so the two
  organisation accounts W4-A created on the old lane clone (`w4a-institution@example.test`,
  `w4a-university@example.test`) no longer exist — the organisations' bridge for an institution and a university was not
  looked at again.
- **Handed on** (DL54-158 item 10; none of it holds the merge): **the owner and counsel** — the locked French copy's
  ordinary spaces beside «:» and inside «« »» (D14, B1 item 8); **W4-D** — the 149 team-authored `{% translate %}` lines
  to pass through `typo`, its deletion map over the rules W4-A deleted in `_legacy-tokens.css`, `components.css` and
  `register.css`, the release notes' CSS table (still design-v5's weights before this merge), DS 2026 §2's prose count
  of the legacy type classes («14», two left); **W4-C** — WebKit, Firefox and real devices, the Academy's filter row's
  focus, the console's foot scroll padding above phone widths and the trail's 24 px under a mouse, the console drawer's
  brand ring 4 px over the screen's top; **W3-A** — its rail tools at 36 px under a mouse (its reading of SP-8). By
  design, recorded: «Ma situation»'s Stepper at 320 (40 px a column), the dev showcase's own samples.
- **W4-C's merge** comes after this one and renumbers its decision-log entries (its branch also starts at DL54-157).
- **The full suite** was not run (V5.5: the integration checkpoint runs it). Nothing was pushed to GitHub; nothing was
  deployed; production untouched.
