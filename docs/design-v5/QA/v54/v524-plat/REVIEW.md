# v529-plat-review — PLAT (platform, typography only) — PASS

Branch `v524-plat` @ 2cc26c58 (design-v5 31f5ceff included), served on 8790 (ile_v5_l6, acceptance personas). Headed
chromium-1234 run under CHROMIUM_LOCK_A (taken 00:18, released at the end). Harness: `.work/v529-plat-review/`
(review.py, review2.py, run_8790.py, pytest.txt). Data: `review.json`, `review_docs.json`. Stills: `*_top.png`,
`*_full.png`, `menu_{fr,ar}_390_open.png`, `person_fr_1440_reduced.png`, `person_fr_1440_keyboard.png`.

## Covered
- Person (overdue), company and institution dashboards at 1440/1024/390 fr; ar at 1440 and 390 (company: 390).
  «Mes documents» at 1440/1024/390 fr and 390 ar. A requirement page (`/documents/requirements/…`) at 1440/390 in fr and
  ar. The case file in ar at 1440 and 390 (where W3.2 lands). «Mon organisation» in ar at 390.
- Mobile menu (drawer) at 390 fr+ar: opens, takes focus, 16 items, min font 14 px, min target 44 px, weights 400/500,
  Tab stays inside, Escape closes and returns focus to «Menu», axe 0.
- Reduced motion (person fr 1440): 0 running animations, both `data-rise` sections visible.
- Keyboard (person fr 1440): 22 Tabs, each a visible 1.6 px solid ring; `html[data-input=key]` set.
- axe (wcag2a/aa, 21aa) on 10 cells: 0 violations.
- Every cell: status 200, one h1, horizontal overflow 0, 0 console errors, no near-black text (< rgb 20). The only text at
  ≥ 600 is the rail wordmark (brand, R1) and the footer's `<strong>`. Headings are 500 in `rgb(34,47,61)` (text-1).
  Arabic uses Readex Pro, rtl.

## Essentials
- Targeted tests: apps/portal, apps/documents, apps/cases, the lane's static and browser modules, test_typography_v2,
  test_console_shell_browser_w3_a and test_arabic_completeness. Result: **1021 passed, 1 failed**. The failure is
  `test_il_lume_marks_the_current_page…`: Lume's glyph ink comes from SYS's re-valued ink. It is red on design-v5 too,
  and PLAT touches no Lume file. It belongs to the SYS steward / CLOSING.
- Locked copy: the template diff adds classes only (`t-label`). No text changed and no msgid was added.
- Contact channels: compared in process on 8790 against 8780 (fr/ar contact and the home). The configured WhatsApp
  link matches in every place (3/3/2) and the tel links are 3/3/2. Neither value is printed here.
- Budgets (gzip -9 -n, base design-v5 → branch): main.css is unchanged at 32 645 (≤ 32 716). The other sheets:
  console 8 032→7 969, platform 5 014→4 998, registers 2 984→2 960, journey 2 728→2 726, situation 2 243→2 243,
  case 955→955, documents 5 564→5 531.
- Preserved families: Navbar/rail, Lume, contact, privacy, forms and the role model are not touched by the diff. The
  drawer and rail behave as before.

## V5.29 §23
1 raw grids: not this stream (no composition change; the platform's lattices and tables are the designed ones).
2 heavy black: **NO** — 0 near-black text on every page; ink is text-1/-2/-3.
3 headings on bold: **NO** — every h1–h3 is 500. Hierarchy comes from size: 34.7 / 20 px desktop, 24 / 20 px phone.
4–10: not this stream (backgrounds and materials are unchanged by R8, plus FAQ, icons, protezione, Institutions,
editorial).

## Not blocking — notes for CLOSING / AR (not fixed, R14)
- On the requirement page in /ar/, the breadcrumb's last crumb shows the record's French title while the h1 is in
  Arabic. The template is AR's (documents), not PLAT's. It is an Arabic leftover candidate.
- The person NowPanel in /ar/ shows the passport line in French, isolated `lang=fr dir=ltr`. The title has a catalogue
  entry but the detail does not, so D1's whole-line rule keeps both in the record's words, the same as the case file.
  AR should decide whether the title alone may be shown in Arabic.
- The bottom-bar labels and the rail group and role labels are 12 px. These are the shell's existing label role,
  untouched by PLAT; the drawer items are 14 px.
- At 390 the institution eyebrow «ESPACE INSTITUTIONS» wraps onto two lines. This is micro and not blocking.
- At 390, «Mon organisation» in ar: the atrium drawing sits near the eyebrow. This is the builder's candidate; it reads
  acceptably in the still.
- Not measured: INP/CLS on 8782. The diff is CSS type tokens only, adds 0 JS and changes no layout (overflow 0
  everywhere).

Verdict: **PASS** — 0 blockers. MERGE per FINAL_DELIVERY_V2 §3.7 (1)–(4).

## The verdict as the workflow returned it to the steward, verbatim

```json
{
  "review": [{"page":"Person dashboard (overdue) fr/ar 1440/1024/390","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS. 200, one h1, overflow 0, no console errors, axe 0. No near-black text; headings are 500 on text-1. Reduced motion: 0 running animations and the data-rise sections are visible. Keyboard ring is visible on every stop. Arabic is on Readex Pro, rtl."},{"page":"Company dashboard fr 1440/1024/390, ar 390","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS. The type roles carry the hierarchy; references stay in the mono. Overflow 0, axe 0, 0 errors."},{"page":"Institution dashboard + Mon organisation fr/ar","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS. Fact labels use t-label; the atrium and calm panel are unchanged. The eyebrow wraps at 390 (micro). Axe 0 in fr 1440 and ar 390."},{"page":"Documents (Mes documents + requirement page) fr/ar","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS. 200, one h1, overflow 0, axe 0. On the ar requirement page the breadcrumb's last crumb stays in the record's French; that template is AR's (note)."},{"page":"Platform mobile menu (drawer) fr/ar 390","composition":4,"motion":4,"imagery":4,"interaction":4,"institutional":4,"coherence":4,"note":"PASS. The drawer opens and takes focus, Tab stays inside, and Escape closes it and returns focus to Menu. Min font 14 px, min target 44 px, weights 400/500, axe 0."}],
  "minors": [{"severity":"minor","where":"/documents/requirements/<pk>/ in ar (templates/documents, AR's)","detail":"The breadcrumb's last crumb shows the record's French title while the h1 is in Arabic.","fix":"CLOSING/AR: pass the crumb through documents.services.displayed_text as the h1 does."},{"severity":"minor","where":"/ar/espace-reserve/ NowPanel (apps/portal/services.py now_panel)","detail":"The passport line stays in French, isolated lang=fr dir=ltr. The title has a catalogue entry but the detail does not, so the whole-line rule (D1) keeps both in the record's words, as the case file does.","fix":"AR to decide whether the title alone may be shown in Arabic. Post-acceptance."},{"severity":"minor","where":"tests/frontend/test_console_shell_browser_w3_a.py::test_il_lume_marks_the_current_page…","detail":"1 failure out of 1022 targeted tests. Lume's glyph ink comes from SYS's re-valued ink; it is red on design-v5 too, and PLAT touches no Lume file.","fix":"SYS steward / CLOSING."},{"severity":"minor","where":"_shell.css bottom bar / rail labels","detail":"The bottom-bar labels and the rail group and role labels are 12 px on phones and desktop. This is the shell's existing label role and not in the PLAT diff.","fix":"Post-acceptance candidate (R14)."}],
  "new_strings": [],
  "not_done": ["Lume glyph colour test (test_console_shell_browser_w3_a::test_il_lume_marks…) fails the same way on design-v5, from SYS's ink; Lume is not PLAT's to change — for the SYS steward / CLOSING","Three portal residues are left in TYPOGRAPHY_BURNDOWN for CLOSING, plus academy.css's .academy-attendance__ref, whose template is another lane's","Post-acceptance candidate, not fixed (composition, preserved family): /ar/espace-reserve/mon-organisation/ at 390, the atrium drawing sits over the eyebrow line","No headed under-a-slot review and no 8782 INP/CLS measurement; both belong to the reviewer's gate","Not merged into design-v5 and not tagged (by order)"]
}
```

No fix round (PASS, 0 blockers). The steward's merge (DL54-197) carries the minors and the builder's not_done with
their owner lanes (AR / CLOSING / after acceptance); §9.8's exception recorded: typography and colour tokens on
the platform (R8, V5.29).
