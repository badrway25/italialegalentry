# Lane A: finishing review F1 (v515f-a-qa1)

Branch `v515-a`, worktree `C:/tmp/ile_wt/v515-a`, head `6a54102`. design-v5 HEAD `7f2a02d` is already an ancestor (checked with `merge-base --is-ancestor`). Reviewed 29 October 2026.

Setup: lane server 8783 (`config.settings.dev`, database `ile_v5_l3`, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`). HEADED Chromium 1234 (Playwright `headless=False`). Chromium lock held 09:58–10:09, released, then taken by v515f-b-qa1. Server stopped at the end.

Probes and logs: `C:/tmp/ile_v5_council/.work/v515f-a-qa1/` (cast.py, megaf1.py, sheetf1.py, kb.py, rise.py, console.py, plus the *.json outputs). Captures: `qf1-*.png` in this folder.

## Previous findings (round 3)

| # | Sev. | Finding | Verdict |
|---|---|---|---|
| M-1 | major | Slow path: the key turns twice and the room goes dark | **FIXED.** fr 1440 at 1.5 s latency (`qf1-cast-slow1440.png`). The leaving page turns the key once (`is-departing` from ≈ 430 ms, back at identity by ≈ 760 ms), then holds with «Chargement…». The arrival reads `--lume-t` 480 ms and its key is `matrix(1,0,0,1,0,0)` on every logged frame (3 202 → 3 550 ms). The veil fades 1 → 0 in ≈ 210 ms. The arrival's first frame shows the room *more* lit than the leaving frame, never darker (`.work/v515f-a-qa1/handoff.png`). |
| M-1b | major | The front half of the arrival's turn is lost in the long first frame | **FIXED.** fr 1440 fast: `--lume-t` 150 ms, the key rests at 450 ms, then 1° … 25° … 43° … 91° … 120° … 360° between 540 and 840 ms, ≈ 9 visible frames (`qf1-cast-fast1440.png`). ar 390: `--lume-t` 116 ms, rests on 2 frames, then turns over ≥ 10 frames 327 → 430+ ms (`qf1-cast-ar390.png`). |
| M-2 | major | Mega panel: ellipses, empty short-door cards, Institutions clamped, Projet plain, notice in fr only | **FIXED.** 0 clipped lines on every door at fr/ar/en 1440, it 1280 and fr/ar 1024 (`mega.json`). Short doors are destination rows of 96 px (glyph disc, title, whole line, night arrow disc; `qf1-mega-fr-1440-d1.png`). Every entry has a glyph on all 30 panels probed. Projet has glyphs, and AGAMI has «Le promoteur du projet» (`qf1-mega-fr-1440-d4.png`). The notice stands in the foot in fr, and in it/en/ar with `lang="fr"`. Below 80rem the Personnes titles show alone (`qf1-mega-fr-1024-d0.png`). |
| m | minor | Two current markers on `/fr/forum/` | **FIXED.** Only «Forum Vénétie–Maroc» has `aria-current=page`. Checked also: on `/fr/faq/` Personnes is true and FAQ is page; on `/fr/agami/` Projet is true and AGAMI is page; `/fr/entreprises/` marks Entreprises only. |
| m | minor | Sheet entries have no glyphs | **FIXED.** Every sheet entry has a 32 px disc at fr 390, ar 375, it 360, en 430, fr 768 and ar 390 reduced motion (`sheet.json`, `qf1-sheet-*.png`). |
| m | minor | Warm veil for the page's life | **FIXED as asked** (the class is removed while hidden). See the new N-1 below for a remaining side effect. |
| m | minor | LCP | **Not re-measured** by this review. The builder's 5-sample figures stand: /fr/ 2 452 / 2 512 ms, /fr/faq/ 2 216 / 2 164 ms. `rise.js` is `fetchpriority=low`. Still a request to the Performance Lead on 8782. |
| m | minor | Reveal hooks dormant | **Carry-over.** The hook contract is now written in NOTES as a lane C request. |
| m | minor | `/vivre-en-italie/` 0 targets | **Carry-over.** Still 0 on `ile_v5_l3`. |
| m | minor | French lede/FAQ/Forum in en/it/ar | **Carry-over** (lanes C/D). Still visible: the Personnes lede is French in the ar and en panels, and the ar home h1 is French. |

## What I checked beyond the findings

- **Keyboard.** Tab order fr and ar: skip link, brand, five doors, Forum, Projet, language, Espace réservé, then the page. The door focus ring is drawn, though not through `outline` (`qf1-focus-door-fr-1440.png`). Enter opens the panel. Tab moves into its first entry with a visible ring (`qf1-kb-open-fr-1440.png`). Esc closes it and returns focus to the door (`aria-expanded=false`). Enter on a link plays the loader (`key1440`). Esc during a 2.5 s wait cancels and leaves the page intact with focus on the Forum item (`qf1-cast-esc.png`).
- **Reduced motion, slow path.** No rotation on any frame of either page (`transform: none`). The veil fades to the still, and the arrival from 480 ms fades away.
- **Header** at 1280/1024/768/430/390/375/360 × fr/ar/it/en: no horizontal scroll anywhere, 65/57 px bands, and the brand on one line in ar 360/375 (`.work/v515f-a-qa1/heads.png`, `qf1-head-*.png`).
- **Motion language.** On fr 1440, ar 390 and it 768, 0 rise targets are held in view on home, faq, glossaire, forum, parcours and entreprises. The same holds on a jump, a reload, keyboard, an anchor and reduced motion (`rise.json`).
- **Platform** (as qa-person). The dashboard at fr 1440 and ar 390 shows the rail lit and still (`qf1-console-*.png`).
- **Budgets**, gzip -9, my measurements match the builder's: main.css 33 448 / 33 600, head.js 1 248 / 1 250, shell.js 4 690 / 4 700, portico.css 2 993 / 3 000, rise.js 873.
- **pytest, lane l3.** Ran `test_cms_nav.py`, `test_rtl_static.py` and the non-browser part of `test_lume_v515_a.py`: 111 passed and 1 failed. The failure is `test_portico_gives_every_door_its_panel_from_live_content` (Projet «Actualités» absent on the test database). The builder reports it as pre-existing on design-v5; I did not re-verify that on the stashed tree.

## New findings

**N-1, minor: the warm veil prints a ghost.** Files: `static/css/v5/lume.css` (`html.lume-warm`). While the tab is shown, the veil's stage layer stays at opacity ≈ 0.002 over the whole page. That moves the pixels under the arch by 1 RGB level:
- the dark footer: (7,18,38) → (8,19,39);
- the white sheet and the console: 254 → 253.

The result is a faint arch/rectangle in the centre of every page. It shows up on large uniform areas when the screenshot is scaled down. I noticed it by eye in the FAQ footer, the console dashboard and the ar 375 and it 360 sheets, before measuring it. On a good panel or OLED it can be perceived. It does not block showing the work to the owner, but a premium surface should not carry it.

Fix: keep the pre-warm off the painted area. Use `clip-path: inset(50%)` or translate the warmed layer outside the viewport while warm, and keep the opacity transition only for `lume-go`. Alternatively, set `content-visibility` on the stage and warm only the ground. Then re-film the click's longest leaving frame to confirm round 2's 29–41 ms still holds.

**N-2, minor: the Entreprises panel says the same sentence twice.** The lede «Signalez les besoins professionnels de votre entreprise et découvrez…» sits beside the first row's line «Signalez les besoins professionnels de votre entreprise.» In en/it/ar that row has no line, so it is a title over an empty half-row (`qf1-mega-en-1440-d1.png`).

Fix: either drop the row line when it repeats the lede's opening, or vertically centre a title-only destination row so the 96 px row does not read as unfilled.

**N-3, minor: Projet's panel speaks a slightly different grammar.** It has no eyebrow kicker, while the other four doors have one («PERSONNES», «ENTREPRISES»…). Its AGAMI glyph (the team's mark, bars under an arch) reads at 20–24 px as a bar-chart icon.

Fix: give Projet the same kicker, and consider the registry's institution/building glyph for AGAMI, or the brand's arch alone.

**N-4, minor (watch): no headroom left in the budgets.** head.js has 2 B of headroom and portico.css has 7 B. The next change to either file will breach its budget unless something is taken out.

Fix: record in NOTES which rule or line would go first.

## Scores (V5.15 §26)

| Family | Score | Why |
|---|---|---|
| Navbar Premium (letterhead) | 4 | One row at all desktop widths in 4 languages and no horizontal scroll at 8 widths. One current item now. The focus ring is visible, and the brand stays one LTR run in ar. |
| Mega menu | 4 | Both majors are resolved: no ellipsis, whole lines on level paired rows, short doors as real destination rows, glyphs everywhere, the notice in every language. The remaining polish items are N-2 and N-3, and the French lede in en/ar (lanes C/D). |
| Phone sheet | 4 | Glyphs now match the panel, there is no bidi split of the brand, 56–130 px rows, the notice in the door, no horizontal scroll from 360 to 768. |
| Global Lume Loader | 4 | The slow path is now coherent: one turn, the light only grows. The fast path shows the whole turn at fr 1440 and ar 390. Reduced motion, keyboard and Esc are correct. N-1 (the ±1-level ghost) keeps it from 4.5. |
| Motion language (public) | 4 | Unchanged and still sound: nothing held in view under any entry mode. The richer vocabulary is dormant pending lane C. |
| Platform motion | 4 | The rail is lit and still; the dashboard is unchanged. |

**Minimum 4, no major.** Lane A meets the bar (≥ 4 in every family, no major) and can be shown to the owner. N-1 should be fixed before the merge if the budget allows; N-2 to N-4 are polish.
