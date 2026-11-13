# V5.22 lane M — Imagery V2 · senior review, round 2 (label `v522-m-qa2`)

Branch `v522-m`, worktree `C:/tmp/ile_wt/v522-m`, head `12976c3` (round 1 of the builder, label `v522-m-improve1`; base
`8c0941c`). Reviewed 31 Oct 2026, 00:55–01:35.

**How.**
- I read the binding inputs again (V5.22, V5.20, SECTION_SYSTEM_V2 §0–§10 with §3.1, §7.3, §8 and §9 in full), my round-1
  report, the builder's NOTES §9 and the diff `ffb4f8f..12976c3` (87 files) as well as `8c0941c..12976c3`.
- I measured every served file from disk with my own script (`qa2_files.json`), and ran the **unmodified** V5.12 budget
  logic on the new tree, with sizes read from disk rather than from the provenance.
- I looked at the two new frames, the marble re-crop and the rest of the set at their largest served width, with zooms
  on every risk area. I compared each new crop against its original.
- I served the branch on 8784 from the worktree (dev settings, database `ile_v5_l4`, `ILE_DESIGN_PREVIEW=1`, reference
  date 2026-10-03). I checked it in **headed** Chromium (chromium-1234) on lock slot A, in two sessions: 01:02:56–01:11:30
  (headed checks) and 01:21:15–01:24:24 (the browser pytest run). Both were released. Slot B was held by lane S's
  reviewer throughout and was not touched.
- I compared Universités with the fdd6e34 audit (`pages2/p1_universites_fr_768.jpg`), and the weights with 8780.
- Targeted tests ran on a private database (`ile_t_m_qa2`). Scripts: `C:/tmp/ile_v5_council/.work/v522-m-qa2/`.

## Verdict: PASSED (round 2)

Both majors and all five minors of round 1 are fixed, and I verified each fix myself (§1).

- **The V5.12 assertions hold again.** Run unchanged on the new files, the old test fails on exactly 19 items. All 19
  are the three §7.3 kinds that contradict it, and they are held under their own ceilings in both formats with no
  allowance.
- **The marble panel keeps the gesture** at every common laptop size, under both the Director's geometry and the one
  lane S built.
- **The two replaced frames are real improvements.**
- **The live change is exact:** |drawn − `sizes`| ≤ 0.2 px in 32 headed cases.
- **The frame set scores 4.0 against a bar of 4.** It passes, narrowly. The three weakest frames are named in §5.

Four minors remain (§3). None blocks the lane:
- one inherited file over a ceiling (n1);
- one `sizes` value that drifted from lane S's built route board (n2);
- the catalogue sync, which the steward must carry in M's merge (n3);
- one missing request to lane S (n4).

Fix n1, n2 and n4 before M's merge; the merge order S → M allows it. n3 is the steward's.

## 1. Round-1 findings, verified

| Round 1 | Status | What I checked |
|---|---|---|
| **M1** strict test rule (WebP allowance; `universities.exchange` dropped from the V5.12 budget) | **Fixed** | `WEBP_ALLOWANCE` is gone from the builder; no provenance row records an allowance. `test_the_weights_hold_their_budget` has its V5.12 body back, plus two cited tables (`OWN_CEILING_V522`: the two 2:3 panels and the ground's 4:5, from the limit only; `OWN_LADDER_V522`: the four family frames, from the ladder only). **The unmodified V5.12 logic on the new tree (sizes from disk) fails on exactly 19 items:** 6 panel files (cedar 2:3 800 AVIF 47 863 B and WebP 59 528 B, 1200 AVIF 56 143 B, 1600 AVIF 57 781 B; marble 2:3 1600 AVIF 50 786 B and WebP 59 966 B), all under the panel's 60 KB; 5 ground 4:5 files, where the old code raises `KeyError` because V5.12 has no limit for role «ground»; and 8 family-frame ladders. Nothing else fails. Every AVIF **and** WebP of every V5.22 ratio is under its §7.3 ceiling. `universities.exchange` is under the V5.12 assertions in both formats: WebP 1200 w is 45 178 B and 1600 w is 44 898 B, against a limit of 46 080 B. 19 WebP widths are not built and are listed. The new guard keeps V5.12 slots out of the exemptions. The docstrings and NOTES §5 are corrected. All four V5.20 conditions are met |
| **M2** marble 2:3 cut on the gesture | **Fixed** | The crop is now x 0.31–0.7545, full height. Cover simulation on the served 1 600 w AVIF, panel 30 % × 82 vh, centred: the blade corner sits 6.9 % inside the drawn edge at 1024 × 768, 14.1 % at 1280 × 800, 14.2 % at 1440 × 900, 17.7–17.9 % at 1280 × 720, 1366 × 768, 1536 × 864 and 1920 × 1080 (`qa2_marble_panel_cover_A.jpg`, `qa2_pilot_cover_A.jpg`). Under lane S's built `.panorama--coppia` (two ~50 % columns, cover crops 15–19 % top and bottom) the fist, the whole blade and the contact all stay in frame (`qa2_pilot_cover_B.jpg`). The object-position advice for H is in NOTES §9.1 |
| **m1** study frame (seam, neutral, second overhead tabletop) | **Fixed** | 6334273 is shot at desk level and is warm (mean saturation 49.4–54.2 on all 10 files). It has one redaction box with no seam: at 3× on the 1 200 w strip the only marks are an illegible scribble, two arrows and a bracket, and the blur reads as depth of field. The face is above both crops. The family frame 27177298 is checked against its original: the beer glass, the third hand (with a ring), the plaid sleeve and the bread board are all outside both crops, and no face, lettering or brand remains. The site now has three overhead tabletops instead of four |
| **m2** circular board assertion; no real-page check | **Fixed** | The browser test now measures the real Universités page (fr, ar, 6 widths) with each `vw` read against the layout viewport. The board no longer compares drawn width with `sizes`. **Headed, my own probe, 4 languages × 8 widths:** \|drawn − `sizes`\| ≤ 0.2 px in all 32 cases, and the raw evaluation (scrollbar included) is never below the drawn width (§6). The three `sizes` errors the builder found (the 430 px margin, 45vw, 42rem) are corrected in the code and in AUM §11 |
| **m3** board announced, mock compositions, internal vocabulary, 100vw overflow | **Fixed** | `apps/designpreview/live.py` is back to the base. The index has 0 links to the board, which answers 200 by URL only. No lane-M preview label is claimed. Each frame is drawn alone on paper with its data sheet, with no composition and no treatment (`qa2_board_1440_full.jpg`, `qa2_board_390_full.jpg`). No `vw` is used. Headed with the classic 15 px scrollbar at 8 widths: overflow 0, `scrollX` 0 after `scrollTo(10000, y)`, 0 console errors. The variant keys `pannello` and `campata` remain as registry identifiers in `<code>`; that is acceptable in a fixture the owner never sees |
| **m4** catalogue | **Prepared; merge condition (n3)** | The `.po` fragments cover **exactly** the 7 msgids the audit reports missing, in it, en and ar, and every msgid is byte-identical to `imagery.py`. The branch still fails the 4 catalogue cases, as expected under §9.7 |
| **m5** AUM §11 `sizes` | **Fixed** | The row states the code's exact seven-step value and the measurement behind it |

## 2. §9.9 acceptance for lane M

| Item | Result | Evidence |
|---|---|---|
| Every new slot renders at 1440 and 390 with explicit dimensions, lazy loading and exact `sizes` | **Met.** On the bench at all 8 widths, all 11 renderings take their art-directed ratio. Each is `loading="lazy"` and `decoding="async"`, has width and height on the `<img>` and on every `<source>`, and carries no fetchpriority. The browser's pick is sound for the density. On the one live consumer, `sizes` is exact to ±0.2 px. The other slots are placed by H, P1 and P2, who are asked to assert drawn = `sizes` with the same probe (NOTES §9.10). One drift from lane S's built route board: n2 | `qa2_headed.json` (board, universites) |
| File ceilings (§7.3) | **Met** for every V5.22-governed ratio, AVIF and WebP, every width. The largest file per rendering is in §6. The one inherited exception reachable through a V5.22 variant is n1 | `qa2_files.json` |
| No frame repeats anywhere | **Met.** The id check covers the V5 families, the hero and the portico. The dHash check (16 × 16) compares every new frame with the 269 raster files served and finds no near-duplicate. *Pre-existing and not M's:* the hero and the portico share three ids (29492060, 30557565, 6949886), both preserved families | `dupes2.py` |
| Complete provenance and licence rows | **Met.** Every V5.22 row has its id, page, licence, author, original size and sha256, crops as fractions and pixels, master size, redactions with reason (and mode), treatment, ceilings, WebP floor, `webp_not_built` and label. The two new originals' sha256 match the provenance. IMAGE_LICENSES §3.4 and AUM §11 have a row per rendering, and none of the lines lane M added carries a photographer's name | provenance check |
| AUM §6 at full resolution | **Met.** No arch, step, vault, door or gridded window as the subject. Nobody identifiable. No cliché. No readable text or brand at any served width: the warehouse labels are illegible blobs at 4× on the 1 200 w strip, and the ecosystem's handwriting blur reads as depth of field at 1 600 w | `look/` |
| B/W only where §8 says | **Met.** The treatments are exactly §8's. The stone is desaturated in the file (mean saturation 26.9–33.8). The «select» frames are in colour (49.4–96.6), and at rest in grayscale they still read as four distinct frames | `qa2_family_select_rest_vs_colour.jpg` |
| Full-scroll weight at 390 DPR 2 rises ≤ 250 KB | **Met.** Universités +1.5 KB (fr and ar). Every other page is byte-identical, with the same requests. Projected rises once the lanes place the frames: home +51.2 KB, Le projet +42.5 KB, Parcours +66.5 KB, Formation +28.1 KB (I recomputed each from the served files) | §6 |
| Images beautiful, relevant, art-directed (set ≥ 4) | **Met: 4.0** | §5 |
| §9.9.7 tests change only under the strict rule | **Met** | §1 M1 |
| §9.9.8 preview label | **Met:** none claimed (lane M has none) | — |

## 3. Findings (all minor)

**n1 — The `campata` variant inherits an unbudgeted V5.12 width over the body ceiling**
(`apps/pages/imagery.py` `home.ecosystem` variant `campata` = 4:3 from 64 rem, `narrow="3x2"`;
`tests/compliance/test_imagery_v512.py` `CEILINGS_V522[("home.ecosystem", "campata")] = {"4x3": …}` only)

- Below 64 rem the variant draws the V5.12 3:2 ladder, which goes up to 1 600 w.
- That 1 600 w AVIF is 49 206 B and its WebP 70 778 B, both over §7.3's body ceiling of 46 080 B.
- With `sizes` `100vw`, a 768 px tablet at DPR 2 takes it (headed, on the bench: `table-travail-institutions-3x2-1600.avif`).
  So does a 430 px phone at DPR 3.
- Neither guard sees it:
  - V5.12 budgets only the 480/800/1200 of a 3:2;
  - `CEILINGS_V522` governs only the variant's 4:3;
  - the test's comment («a variant may keep a V5.12 ratio … test above») assumes the V5.12 test holds that ratio, and
    it does not at 1 600.
- §8.2 lists «narrow 3:2» among this re-crop's crops. It is not a regression: today's default rendering serves the same
  file at the same widths. The two crops side by side: `qa2_campata_narrow_3x2_vs_4x3.jpg`.

*Fix:* give `Variant` an optional width ladder and cap `campata`'s narrow 3:2 at 1 200 w (AVIF 34 673 B, WebP 45 836 B).
Then add `"3x2": 45 KB` to the variant's entry in `CEILINGS_V522`, so the test governs the variant's every served ratio.
This keeps the V5.12 files byte-identical. The alternative is to re-encode the 1 600 w under 45 KB.

**n2 — `FAMILY_SIZES` does not match lane S's built route board** (`apps/pages/imagery.py` `FAMILY_SIZES`;
S's `static/css/v5/_sec-tracciato.css` on `v522-s` `4c738be`)

- **Below 64 rem**, S's lanes are indented by the trunk (`.tracciato__corsia { padding-inline-start: var(--s-12) }`,
  48 px). The 21:9 strip is therefore drawn 48 px narrower than the container width `FAMILY_SIZES` states: +10 % at
  768, +20 % at 430, +22 % at 390, +25 % at 360.
- **From 64 rem**, the head is 3fr of (lane − 32 px gap), not 21vw:
  - 290 px vs 302 at 1440 (+4 %);
  - 254 vs 269 at 1280 (+6 %);
  - 212 vs 215 at 1024 (+1.4 %).
- The 480/720/1200 ladder is coarse, so no pick changes at the audited widths. The value is still not the exact
  `sizes` §7.3 asks for, and at 320 @2 it would fetch 720 w instead of 480 w.
- S is still in review; the merge order is S → M.

*Fix:* when rebasing on S's merge, restate `FAMILY_SIZES` from S's final geometry. For example, below 48 rem
`calc(100vw - 2.5rem - 3rem)`, with the matching 430 px and 48 rem steps, and container-stepped values from 64 rem as
`universities.exchange` already has. Ask P1 to assert drawn = `sizes` with `PROBE` on /xx/parcours/ (NOTES §9.10
already asks this).

**n3 — Merge condition: the catalogue sync** (round-1 m4, carried over; the steward's, not M's)

The branch fails `tests/i18n/test_catalogues.py` in 4 cases (`[it|en|ar]` and the audit script). On `ile_t_m_qa2` the
targeted run gave 474 passed and those 4 failed.

*Fix:* the steward's M merge carries `scripts/i18n_audit.py --sync`, the msgstr of
`evidence/v522/m/imp1_catalogue_entries_{it,en,ar}.po` (verified to cover exactly the 7 missing msgids) and `--compile`.
design-v5 then stays at FAILURES 0 until S-close (§9.9.7).

**n4 — A request to lane S is missing: the panorama partial cannot draw the `pannello` variant**
(NOTES §7 and §9.10, «Requests to other lanes»)

- S's `templates/components/sezioni/panorama.html` on `v522-s` calls `{% photo slot "panorama__foto" %}` and
  `{% photo pair "panorama__foto" %}` with no `variant` and no `sizes`. Through S's partial, the home pilot would get the
  default 4:5 halves, not the 2:3 panels.
- Its `.panorama--coppia` draws two equal columns of about 50 %, not §3.1 S4's ~30 % edge panels with the title in the
  seam. M's NOTES ask H to call the tag directly, but they file nothing with S, the file's owner (§9.7).
- The marble crop holds under both geometries (§1, M2), but `pannello`'s `sizes` (`34vw`) would under-state S's
  coppia by about 30 %.

*Fix:* add to NOTES a request to S: `panorama.html` passes `variant` and `sizes` through to `{% photo %}`, or H draws S4
with the tag in its own partial. Tell H that `pannello`'s `sizes` must follow whichever geometry ships (NOTES §9.10's
`max(34vw, 54.67vh)` assumes the 30 % panels).

## 4. Notes, not M's to fix

- **Lane S, request 7.S.2 still open.** S's `photo.html` on `v522-s` writes `data-reveal="mask"` on every non-eager frame,
  so the role-«ground» stone would be masked like a body frame until S handles `role == "ground"`.
- **Director, from round 1 and still true:**
  - Le projet will show books twice (`project.hall`'s shelves and `project.volumes`).
  - The campus re-crop loses its academic cue, and at 768 the gesture reads as a thumbs-up (`qa2_univ_fr_768_before_after.jpg`).
    The censored-looking blurs are gone.
- **Candidates for a later imagery pass:** `pathways.family.work` (retail warehouse), the `campata` 4:3 (corporate
  meeting table), `universities.exchange`, and `project.volumes`, whose 1 920 w is AVIF q 31 under the 60 KB ceiling
  and will be upscaled about 1.7× on a 1440@2 screen.

## 5. The frames — art direction (1–5, at the size and treatment each will be seen)

| Frame | Score | Why |
|---|---|---|
| `home.integrity.stone` (11499083) | 4 | Quiet ashlar in raking light, dark and desaturated; right for a ground under a 60 % veil |
| `project.volumes` (29976379) | 4 | Rich, cinematic spines and gilt; no title. Execution is soft (q 31 at 1 920 w), so 4, not 4.5 |
| `pathways.family.work` (29454379) | 3.5 | A strong vanishing point, but it reads as a retail warehouse. Labels are illegible |
| `pathways.family.study` (6334273, new) | 4 | At desk level, warm and intimate; a common stock trope, honestly executed. No seam |
| `pathways.family.family` (27177298, new) | 4 | Vivid and specific: the carved openwork table, hands sharing. Far better than the brunch table; still «food from above» |
| `pathways.family.other` (9250930) | 4.5 | Vines in warm mist; the best of the four, and it holds in grayscale |
| `training.before` (34526423) | 4 | Authentic «training»; the median erasures hold |
| `home.pilot.cedar` 2:3 | 4.5 | Hand, chisel and arabesque, complete at every size |
| `home.pilot.marble` 2:3 (re-crop) | 4.5 | Fist, whole blade and contact, a strong close-up (was 3) |
| `home.ecosystem` 4:3 | 3.5 | A clean crop, but a generic corporate meeting table |
| `universities.exchange` | 3.5 | Clean; the academic cue is gone and there is a thumbs-up reading at 768 |

**Mean 4.0** (44 / 11). The bar is 4: met. Sheets: `qa2_set_contact_sheet.jpg`, `qa2_family_select_rest_vs_colour.jpg`.

## 6. Page scores (§26; 1–5, 3 = clean but editorial or static)

Lane M visibly changes one page.

| Page | Comp. | Motion | Imagery | Interaction | Institutional | Coherence | Note |
|---|---|---|---|---|---|---|---|
| `/xx/universites-et-formation/` (fr, it, en) | 2.5 | 2.5 | 3.5 | 2 | 3.5 | 4 | The re-crop removes the censored-looking blurs and is exact, lazy and unchanged under reduced motion and without JS. The page is still a header plus one editorial split. Composition, motion and interaction belong to P1's U1 «la filiera» (§3.8), which is not built yet |
| `/ar/universites-et-formation/` | 2.5 | 2.5 | 3.5 | 2 | 3.5 | 4 | The same. The photograph is not mirrored, and the alt is the French fallback with `lang="fr"` until n3 |

The home, Le projet, Parcours and Formation are byte-identical on this branch: the same photographs, requests and
weights.

## 7. Measurements

**Live `sizes` on Universités** (headed, classic 15 px scrollbar; fr shown, it, en and ar identical):

| Width | `sizes` (vw on layout) | Drawn | Raw `sizes` (vw on window) | File |
|---|---|---|---|---|
| 1440@1 | 608.0 | 608.0 | 608.0 | 800 w |
| 1280@1 | 536.0 | 536.0 | 536.0 | 800 w |
| 1024@1 | 452.5 | 452.4 | 460.0 | 480 w |
| 768@2 | 673.0 | 672.8 | 688.0 | 1 600 w |
| 430@2 | 367.0 | 367.2 | 382.4 | 800 w |
| 390@2 | 335.0 | 335.2 | 350.4 | 800 w |
| 375@2 | 320.0 | 320.0 | 335.2 | 800 w |
| 360@2 | 305.0 | 304.8 | 320.0 | 800 w |

- In all 32 cases: overflow 0, `scrollX` 0, 0 console errors, transform `none` on img, picture and figure.
- Reduced motion (fr and ar at 1440 and 390): opacity 1, no transform, no clip, no filter.
- No-JS (fr and ar at 1440 and 390): the frame loads (608 × 405 at 1440, 335 × 223 at 390).
- Keyboard: in 80 Tab steps, focus never lands in the figure. The card after it shows its lagoon ring
  (`qa2_univ_fr_1440_focus_link.jpg`).

**Largest served file per V5.22 rendering, AVIF / WebP against the §7.3 ceiling (KB):**

| Rendering | AVIF | WebP |
|---|---|---|
| stone 21:9 / 60 | 60.0 | 48.3 |
| stone 4:5 / 40 | 37.3 | 39.0 |
| volumes 21:9 / 60 | 57.6 | 44.5 |
| volumes 16:9 / 60 | 56.1 | 58.1 |
| volumes 4:5 / 45 | 42.5 | 45.0 |
| work 3:2 · 21:9 / 30 | 28.8 · 29.7 | 26.3 · 28.9 |
| study 3:2 · 21:9 / 30 | 9.3 · 14.3 | 12.6 · 19.0 |
| family 3:2 · 21:9 / 30 | 28.0 · 29.8 | 28.8 · 29.6 |
| vines 3:2 · 21:9 / 30 | 22.0 · 29.5 | 29.1 · 28.6 |
| bench 4:5 · 3:2 / 45 | 44.9 · 39.8 | 44.7 · 43.6 |
| cedar 2:3 / 60 · 3:2 / 45 | 56.4 · 41.1 | 58.1 · 44.9 |
| marble 2:3 / 60 · 3:2 / 45 | 49.6 · 17.4 | 58.6 · 22.3 |
| ecosystem 4:3 / 45 | 44.0 | 43.5 |
| campus 3:2 / 45 | 42.3 | 44.1 |

- 289 files are listed in provenance, with no hash mismatch, no orphan and no missing derivative.
- `build_derivatives.py --check` is ok.

**Full-scroll photograph weight, 390 × 844 DPR 2** (headed; `qa2_headed.json`):

| Page | fdd6e34 (8780) | v522-m (8784) | Delta |
|---|---|---|---|
| `/fr/` | 53.0 | 53.0 | 0 |
| `/fr/le-projet/` | 53.2 | 53.2 | 0 |
| `/fr/parcours/` | 10.7 | 10.7 | 0 |
| `/fr/formation/` | 31.6 | 31.6 | 0 |
| `/fr/universites-et-formation/` | 36.2 | 37.7 | +1.5 |
| `/ar/universites-et-formation/` | 36.2 | 37.7 | +1.5 |

The NOTES §4 figures (86.7, 54.3 …) count every image, SVG included. My «all images» column gives the same values, so
the two reports agree.

## 8. Tests and checks (`TEST_DATABASE_URL=…/ile_t_m_qa2`)

- `tests/compliance/test_imagery_v512.py`, `tests/i18n/test_catalogues.py`, `tests/compliance/test_figure_caption.py`,
  `apps/pages/tests/test_home.py` and `tests/frontend/test_design_preview.py` (non-browser): **474 passed, 4 failed**.
  The 4 failures are the catalogue cases (n3).
- `tests/frontend/test_imagery_v522_m.py` and `tests/frontend/test_browser_v515_c.py` (browser): **22 passed**.
- `ruff check` reports «All checks passed!» and `ruff format --check` reports the 5 changed Python files as already
  formatted. No changed text file has CRLF.
- No tracked file carries any form of the WhatsApp number (`git grep`). On 8784 the footer shows it from the
  database's SiteSettings, as option B requires.
- The branch changes no product stylesheet or script, so `main.css` stays at 32 718 B.

## 9. Evidence (this folder, prefix `qa2_`)

- `qa2_univ_{fr,it,en,ar}_{1440,1280,1024,768,430,390,375,360}.jpg` (32)
- `qa2_univ_rm_{fr,ar}_{1440,390}.jpg`, `qa2_univ_nojs_{fr,ar}_{1440,390}.jpg`
- `qa2_univ_fr_1440_full.jpg`, `qa2_univ_ar_390_full.jpg`, `qa2_univ_fr_1440_focus_link.jpg`
- `qa2_univ_fr_768_before_after.jpg` (fdd6e34 audit, then this branch)
- `qa2_board_1440_full.jpg`, `qa2_board_390_full.jpg`
- `qa2_marble_panel_cover_A.jpg`, `qa2_pilot_cover_A.jpg`, `qa2_pilot_cover_B.jpg`, `qa2_pilot_cover.json`
- `qa2_set_contact_sheet.jpg`, `qa2_family_select_rest_vs_colour.jpg`, `qa2_campata_narrow_3x2_vs_4x3.jpg`
- `qa2_headed.json` (Universités, reduced motion, no-JS, keyboard, bench, weights)
- `qa2_files.json` (files from disk, the unmodified V5.12 logic, §7.3 per rendering, the `<picture>` sources)
- Scripts in `C:/tmp/ile_v5_council/.work/v522-m-qa2/`: `measure2.py`, `cover2.py`, `look_marble2.py`, `dupes2.py`,
  `po_check.py`, `headed2.py`, `headed3.py`

The lane server 8784 was stopped at the end of the review. Chromium slot A was released at 01:24:24.
