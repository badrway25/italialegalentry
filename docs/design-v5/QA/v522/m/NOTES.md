# V5.22 lane M — Imagery V2: seven new frames, four re-crops (labels v522-m-build, v522-m-improve1)

Round 1 (QA_ROUND1, label v522-m-improve1) is §9 at the end; where it changed a fact stated below, the statement is
corrected in place and marked «(round 1)».

Branch `v522-m` from design-v5 `8c0941c` (worktree `C:/tmp/ile_wt/v522-m`). Scope: SECTION_SYSTEM_V2 §9.2 and §8 —
the frames the V2 compositions need, their derivatives, provenance, licences, asset matrix, alt texts, guards and the
per-page image-weight report. Lane M composes no section: the home (H), the journeys and spaces (P1) and the system
pages (P2) place these frames when they recompose their sections. Database lane l4 (refreshed from `ile_v5` as a
template clone: it lacked `core.0003`), lane server 8784 (dev settings, `ILE_DESIGN_PREVIEW=1`,
`ILE_DESIGN_PREVIEW_PORT=8784`, `ILE_REFERENCE_DATE=2026-10-03`), Chromium lock slot B (sessions 22:10–22:20,
22:22–22:36, 22:40–22:47, each released).

## 1. What the owner sees, where

- **Now, on the site:** `/xx/universites-et-formation/`, beside «Pour aller plus loin». The campus photograph is
  re-cropped to the two students' hands: one explains with a gesture, the other holds her folio case. The blurred book
  and folder at the centre of the frame are gone; at 768 px they read as censored objects (AUDIT_pages2, U1). No
  redaction is left in that frame. Evidence: `evidence/v522/m/univ_fr_768_before.png` → `univ_fr_768_after.png`
  (and fr/ar at 1440 and 390, reduced motion).
- **Not in the preview (round 1):** the imagery test bench `/__design-v5/specimens/imagery/` is a development
  fixture of `tests/frontend/test_imagery_v522_m.py`, reachable by its URL only. It is no longer linked from the
  preview index, and lane M announces nothing as visible in preview (SECTION_SYSTEM_V2 §9.9.8 gives lane M no label).
  Each frame is drawn alone on paper by the product's own `{% photo %}` tag, with a data sheet (slot, `sizes`, AVIF
  ladder, the kind's ceiling). It draws no composition and no treatment, and names no pattern of the internal library.
- **When H, P1 and P2 merge:** the home's masonry ground, the pilot's two full-height panels and the ecosystem under
  its arch; Le projet's law-volume panorama; the Parcours family lanes' four frames; Formation's first station. Nothing
  on today's pages moves before its lane recomposes it: a re-crop that a V2 composition needs is a named variant of its
  slot, and the default rendering is unchanged.

## 2. The frames (SECTION_SYSTEM_V2 §8.1, §8.2)

All from Pexels (Pexels License), self-hosted, AUM §6 checked at full resolution in their build crops. Nobody
identifiable (O55). No arch, step, vault, door or gridded window as the subject (O54). No cliché. No readable text or
brand: where a crop keeps text, it is softened and the reason recorded. Q4 and Q5 are untouched: no Forum, no AGAMI.
Authors are credited in each family's `PROVENANCE.json` and in the caption only (§8: no person's name is copied into
another document, these notes included).

| Slot | Pexels | Subject | Ratios (served widths) | Treatment | Largest served AVIF / ceiling |
|---|---|---|---|---|---|
| `home.integrity.stone` | 11499083 | dressed stone courses in raking light, frontal, no opening | 21:9 (800–1920) · 4:5 (480, 800) | desaturated −35 % **in the file**; decorative (`alt=""`), role `ground` | 60.0 / 60 KB · 37.3 / 40 KB |
| `project.volumes` | 29976379 | leather-bound volumes, raised bands and gilt tooling in raking light; every crop starts under the title labels | 21:9 (800–1920) · 16:9 (800–1600) · 4:5 (480, 800) | colour, cool grade | 57.6 · 56.1 / 60 KB · 42.5 / 45 KB |
| `pathways.family.work` | 29454379 | an empty logistics aisle between high racks | 3:2 (480, 720) · 21:9 strip (480–1200) | «select» | 28.8 · 29.7 / 30 KB |
| `pathways.family.study` | ~~6549915~~ → 6334273 (round 1, §9.2) | ~~from above: hands, a ruled notebook, a pen, an open bilingual dictionary~~ at desk level: a hand writes in a notebook, an open book behind | 3:2 · 21:9 strip | «select» | 9.3 · 14.3 / 30 KB |
| `pathways.family.family` | ~~3184192~~ → 27177298 (round 1, §9.2) | a shared table from above; ~~one hand pours into the glass another holds out~~ two hands serve each other over bowls of olives and tomatoes on an openwork wooden top | 3:2 · 21:9 strip | «select» | 28.0 · 29.8 / 30 KB |
| `pathways.family.other` | 9250930 | netted vine rows in mist under hills | 3:2 · 21:9 strip | «select» | 22.0 · 29.5 / 30 KB |
| `training.before` | 34526423 | hands wiring the relays of an electrical training bench, blue wire ducts, red leads | 4:5 (480–1200) · 3:2 (480–1200) | «develop» | 44.9 · 39.8 / 45 KB |
| `home.pilot.cedar` variant `pannello` | 30563520 | re-crop: 2:3 full-height panel; 3:2 band on phones | 2:3 (480–1600) · 3:2 (480–1200) | «develop» | 56.4 / 60 KB · 41.1 / 45 KB |
| `home.pilot.marble` variant `pannello` | 6713855 | re-crop: 2:3 panel (round 1: from x 0.31, the whole blade and its contact kept, §9.1); the whole frame as the 3:2 band | 2:3 · 3:2 | «develop» | 49.6 / 60 KB · 17.4 / 45 KB |
| `home.ecosystem` variant `campata` | 33543226 | re-crop: 4:3 under the arch; the V5.12 redactions kept | 4:3 (480–1600) · 3:2 (kept) | colour | 44.0 / 45 KB |
| `universities.exchange` | 31367507 | re-crop: the hands and the folio case only; **no redaction** (there were three) | 3:2 (480–1600) | colour | 42.3 / 45 KB |

**What the full-resolution check changed** (each item is held by a test of `test_imagery_v512.py`):
- *Volumes:* the spines' title labels end at y 0.35 of the frame, so every crop starts at 0.37 and nothing is redacted.
- *Family table* (round 0's frame 3184192, replaced in round 1, §9.2): one partial face at the frame's top edge (y < 0.06) is above both crops (y ≥ 0.09).
- *Study* (round 0's frame 6549915, replaced in round 1, §9.2): when the 1 200 w strip was enlarged, the dictionary's headwords could be read («polyamide», «aromatic»).
  Its two columns are softened, so the page still reads as a dictionary. The handwriting, two handwritten marks and a
  word on a nail sticker are softened too. The hands, the pen and the notebook stay sharp.
- *Training bench:* I first chose 34938452 (hands on a DIN rail). Its Pexels author is a company account, a boiler
  manufacturer, and the product's caption would have printed that commercial brand under the frame. I replaced it with
  34526423: an individual photographer, and a truer «training» image (a vocational bench). The face is at x 0.17–0.27;
  both crops start at x 0.30. A breaker's maker's logo and label, a miniature breaker's markings, the relays' model codes
  and terminal numbers and a CE label are erased by a new **median** redaction mode. In focus, a Gaussian blur at any
  radius read as a censored patch (tried and seen at 14/8 and 6/3 px). The median removes the printed strokes and keeps
  every shape crisp.
- *Campus:* the new crop starts right of the book (its edge at x 0.555) and under every chin (y 0.40); the «folder» is a
  tablet's plain folio case. No redaction is needed.
- *Alt texts were checked against the frames:* the table's carafe is poured, not passed; the rows are grapevines; the
  campus crop no longer shows a campus or books, so its alt now describes two people in conversation (stock is never
  documentary).

**Rejected candidates** (with reasons): `docs/IMAGE_LICENSES.md` §3.4, last paragraph. Contact sheets, previews,
full-resolution zooms and the fetch/search/compare scripts are outside the repository in
`C:/tmp/ile_v5_council/.work/v522-m/`. The originals cache is `.work/v522-m/originals/` (fetched once from the Pexels CDN;
the author is read through the API with the key from the environment, never printed or written).

## 3. Pipeline and registry (what changed in the code)

- `tools/build_derivatives.py`:
  - new ratios 2:3, 4:3 and 16:9;
  - per-recipe `widths` (the family frame tops at 720 w);
  - `ceilings`: the kind's ceiling of §7.3 binds **every** AVIF width a slot can serve, not only the budgeted ones;
  - ~~the WebP fallback gets a recorded 1.4× allowance~~ (round 1: no allowance — the WebP fallback is held to the
    same ceiling as the AVIF), a q 40 floor, and stops at the last width that fits (listed in `webp_not_built`; every
    current browser takes AVIF);
  - `desat` (desaturation in the file), `tone: "cool"`, per-ratio `soft`;
  - the `median` redaction mode;
  - `keep`: a re-crop adds ratios and leaves the committed files byte-identical;
  - provenance written after each frame.
  - `--check` passes (hashes of every listed file); no orphan file is left in `static/img/v5/`.
- `apps/pages/imagery.py`:
  - seven slots;
  - `role="ground"`;
  - `treatment="select"`;
  - a `mid` ratio, drawn from 48 to 64 rem (the panorama's 16:9);
  - **named variants** (`pannello` for the two pilot halves, `campata` for the ecosystem), adopted by
    `{% photo "<key>" "<class>" variant="<name>" %}`;
  - `{% photo … sizes="…" %}` for a composition that draws another width than the slot states.
  - `sizes` follow the V2 anatomy of §2. The panorama says 112vw from 48 rem because M22 scales its image 1.12. The campus
    frame states its 6/12 track exactly at each container step. The browser test measures the drawn width against the
    evaluated `sizes` at five viewports.
- `apps/pages/templatetags/pages_imagery.py`: the `variant` and `sizes` arguments; `foto_scheda` (the board's data
  sheet, escaped by `format_html`).
- The board: `templates/dev/designpreview/specimens/imagery.html` + `static/css/dev/specimen-imagery.css` (dev only;
  one row in `apps/designpreview/live.py` `SPECIMEN_BOARDS`, one row in the specimens README).

### 21st.dev provenance (the components SECTION_SYSTEM_V2 names for the image patterns; read in full, principles adapted to the files)

| Component (id · URL) | Taken for imagery | Not taken |
|---|---|---|
| Parallax Image · 20023 · `21st.dev/@pulkitxm/components/parallax-image` | The image is larger than its frame (inset −intensity) so the drift never shows an edge. ILE's M22 scales 1.12, so `project.volumes` states `112vw` from 48 rem and is fetched for its drawn size. The panorama crop keeps continuous spines to both edges, so the ±3 % drift never cuts a subject | the scroll listener (M22 is CSS `view()`), the framer-motion wrapper |
| Scroll Reveal Image · 24466 · `21st.dev/@unlumen/components/scroll-reveal-image` | The frame widens from the container to the viewport over an inner image already as wide as the end state. The panorama's `sizes` therefore describes the **end** state (full bleed), and the 1 920 w 21:9 exists for it. The narrow start is served by the same file | springs, the 1.6 zoom, the radius animation (S draws the panorama) |
| SVG Clip Mask · 31436 · `21st.dev/@educalvolpz/components/svg-clip-mask` | The arch preset clips the top 40 % of the frame along a curve (`M0,1 L0,0.4 C0,0.18 0.18,0 0.5,0 …`). The ecosystem's 4:3 re-crop keeps the hands, papers and microphone in the lower 60 % and centre band, and leaves background (jackets, wall) in the clipped crown corners; the red wall at the start edge leaves the frame | the morph loop, hover morphing |

## 4. Budgets measured

- **Files** (§7.3, the largest served AVIF): every V5.22 rendering is under its kind's ceiling on every width (table in §2;
  `test_v522_every_new_frame_holds_its_kind_ceiling_on_every_width`). No new eager image: the eager set is the twelve
  V5.12/V5.15 slots, unchanged (`test_v522_no_new_eager_image_anywhere`).
- **Per page, full scroll at 390 × 844 DPR 2** (headed Chromium; `evidence/v522/m/weights_390_dpr2.json` for the live
  pages, `board_weights.json` for each frame's file as the browser picks it):

  | Page | fdd6e34 (8780) | v522-m (8784) | Once its lane draws the V2 frames | Budget |
  |---|---|---|---|---|
  | `/fr/` | 86.7 KB | 86.7 KB | +51.2 KB (stone 37.3, cedar 28.7, marble 10.6, ecosystem 20.2 − today's two 4:5 halves and 3:2: 45.5) | ≤ +250 KB |
  | `/fr/le-projet/` | 54.3 KB | 54.3 KB | +42.5 KB (the volumes' 4:5) | ≤ +250 KB |
  | `/fr/parcours/` | 11.8 KB | 11.8 KB | +66.1 KB (the four 21:9 strips at 720 w) | ≤ +250 KB |
  | `/fr/formation/` | 32.6 KB | 32.6 KB | +28.1 KB (the bench's 3:2 at 800 w) | ≤ +250 KB |
  | `/fr/universites-et-formation/` | 37.2 KB | 38.7 KB | +1.5 KB (live: the re-crop) | ≤ +250 KB |
  | the other 13 audited pages | unchanged | unchanged | — | — |

- **Repository:** 110 new image files (3 509 KB) and 8 replaced (the campus: 280 → 262 KB); `static/img/v5/` holds 294
  files, 10 946 KB.
- **CSS / JS:** no product stylesheet or script changed (`main.css` untouched at 32 718 B gzip -9). The only sheet is
  `css/dev/specimen-imagery.css`, development only and outside every bundle.

## 5. Tests

- `tests/compliance/test_imagery_v512.py` — **37 passed**: 13 existing and 24 new (`test_v522_*`, one parametrized ×11).
  The new tests hold:
  - the kind ceilings on every width; the ladder tops; no new eager image;
  - black and white only where §8 puts it; the ground desaturated in the file (mean saturation 26.9–32.4 vs 60.9–64.2
    graded without it), decorative with its credit;
  - concrete French alts; variants and the per-use `sizes`; the panorama's three bands;
  - the tag's lazy figure, boxes and `sizes` for each rendering;
  - the full-resolution findings kept by the crops (the volumes' labels, the table's face, the campus book and chins,
    the cedar pocket, the bench's face, the median marks, the dictionary);
  - no frame twice by id or by the original's sha256;
  - the register rows, with no person's name.
  - ~~**Strict-rule update (V5.20), cited:** `test_the_weights_hold_their_budget` no longer applies the V5.12 «body
    45 KB, 480 and 800 always budgeted» rule to the ratios V5.22 adds … Every V5.12/V5.15 file keeps the old limits
    unchanged.~~ **Corrected in round 1 (QA M1):** that statement was false. The exemption was keyed by ratio, so it
    also took `universities.exchange`'s 3:2 (a V5.12 slot and ratio) out of the V5.12 assertions, and the WebP was
    capped by a 1.4× allowance that §7.3 does not contain. Round 1 restores the V5.12 assertions for every file and
    exempts only three §7.3 kinds, each from the one assertion it contradicts (§9.3).
- `tests/frontend/test_imagery_v522_m.py` (new, browser) — **5 passed**: at 1440@1, 1440@2, 768@2, 390@2 and 390@3, each
  of the eleven renderings checks out on the board:
  - the drawn width matches the evaluated `sizes` (±4 %);
  - the file taken has the art-directed ratio, and the box keeps it;
  - the browser's pick is the right ladder step for the density;
  - lazy, async, explicit boxes on the `<img>` and on every `<source>`, no fetchpriority.
- `tests/frontend/test_browser_v515_c.py` — 5 passed (the developing frames still develop).
- Neighbouring suites (non-browser): `test_design_preview.py`, `test_design_docs.py`, `test_figure_caption.py`,
  `apps/pages/tests/test_home.py`, `test_frontispiece_v515_c.py`, `apps/ecosystem` — 664 passed, 2 failed. Both
  failures were mine (the board's data-sheet partial in the preview folder): the partial was removed, the data sheet is
  rendered by the tag, and the 26 board/preview tests then passed.
- `ruff check .` 0, `ruff format --check` clean on the changed files, `manage.py check` 0 issues, `build_derivatives.py
  --check` ok, no CRLF in any changed file.
- **Expected on this branch until the catalogue pass:** `tests/i18n/test_catalogues.py` —
  `test_every_source_message_is_in_the_catalogue[it|en|ar]` and `test_audit_script_succeeds_with_full_coverage` fail on
  exactly the seven new alt msgids (`locale/**` belongs to the merge's catalogue pass / S-close, §9.7). The
  professional renderings are in §6, ready for `scripts/i18n_audit.py --sync/--compile`. The campus frame's former msgid
  «Sur un campus, des étudiants échangent, un livre et un classeur à la main» becomes unused, and the sync drops it.

## 6. New user-facing strings (FR msgids in `apps/pages/imagery.py`; professional it/en/ar for the catalogue pass)

Image alternative texts, so no locked copy is involved. The Arabic is right-to-left with no Latin run inside. Until
the catalogue holds a translation, the page renders the French alt with `lang="fr"` (the existing fallback, WCAG 3.1.2).

| # | FR (msgid) | IT | EN | AR |
|---|---|---|---|---|
| 1 | Des volumes reliés en cuir, alignés sur un rayonnage : nervures et dorures des dos dans une lumière rasante | Volumi rilegati in pelle allineati su uno scaffale: nervature e dorature dei dorsi in una luce radente | Leather-bound volumes lined up on a shelf: raised bands and gilt spines in raking light | مجلّدات مكسوّة بالجلد مصفوفة على رف: أضلاع كعوبها وزخارفها المذهّبة تحت ضوء جانبي مائل |
| 2 | Une allée d’entrepôt entre de hauts rayonnages chargés de cartons | Un corridoio di magazzino tra alte scaffalature cariche di scatoloni | A warehouse aisle between tall racks stacked with cartons | ممرّ في مستودع بين رفوف عالية محمّلة بالصناديق الكرتونية |
| 3 (superseded, round 1: §9.6) | Vues d’en haut, des mains sur un cahier, l’une tenant un stylo, à côté d’un dictionnaire bilingue ouvert | Viste dall’alto, due mani su un quaderno, una con la penna, accanto a un dizionario bilingue aperto | Seen from above, hands on a notebook, one holding a pen, beside an open bilingual dictionary | يدان على دفتر من منظر علوي، إحداهما تمسك قلمًا، بجانب قاموس ثنائي اللغة مفتوح |
| 4 (superseded, round 1: §9.6) | Vue d’en haut, une table dressée pour plusieurs : une main verse à boire dans le verre que tend une autre, entre le pain et les salades | Vista dall’alto, una tavola apparecchiata per più persone: una mano versa da bere nel bicchiere che un’altra le porge, tra il pane e le insalate | Seen from above, a table laid for several people: one hand pours a drink into the glass another holds out, between the bread and the salads | مائدة معدّة لعدة أشخاص من منظر علوي: يدٌ تصبّ شرابًا في كأس تمدّها يدٌ أخرى، بين الخبز والسلطات |
| 5 | Des rangées de vignes dans la brume, au pied d’une ligne de collines | Filari di vite nella foschia, ai piedi di una linea di colline | Rows of vines in the mist at the foot of a line of hills | صفوف من الكروم في الضباب عند سفح سلسلة من التلال |
| 6 | Des mains câblent des contacteurs sur un tableau électrique, entre des goulottes bleues et des fils rouges | Due mani cablano dei contattori su un quadro elettrico, tra canaline blu e fili rossi | Hands wiring contactors on an electrical panel, between blue cable ducts and red wires | يدان توصّلان أسلاك الملامِسات في لوحة كهربائية، بين مجاري أسلاك زرقاء وأسلاك حمراء |
| 7 | Deux personnes en conversation : l’une accompagne sa parole d’un geste de la main, l’autre tient une pochette contre elle | Due persone a colloquio: una accompagna le parole con un gesto della mano, l’altra tiene una cartellina stretta a sé | Two people talking: one gestures as they speak, the other holds a folder close | شخصان يتحادثان: أحدهما يرافق كلامه بإشارة من يده، والآخر يضمّ حافظة أوراق إليه |

The masonry ground is decorative (`alt=""`, no msgid). The board's chrome is Italian development text (not catalogued,
like every specimen board).

## 7. Requests to other lanes

- **S** (`templates/components/photo.html`, `_photo.css`, `_sec-tracciato.css`):
  1. Render `treatment == "select"` (the four `pathways.family.*`): black and white at rest; colour when the frame's lane
     is chosen (`:has(:checked)`), hovered or focused; under reduced motion all in colour (B's still). Today photo.html
     renders no grade for it, so the frames show in colour.
  2. `role == "ground"` (`home.integrity.stone`): lazy, not masked like a body frame, `alt=""`, the credit kept, placed
     in a corner by the K band.
  3. `.panorama` and M22: `project.volumes` states `112vw` from 48 rem for the 1.12 drift scale. If the scale changes,
     the composing lane passes `sizes=` to the tag.
- **H:**
  - S4: `{% photo "home.pilot.cedar" "<class>" variant="pannello" %}` and `home.pilot.marble` (34vw from 64 rem; pass
    `sizes=` if the panel differs).
  - S5+S6: `{% photo "home.integrity.stone" "<class>" %}` as the K ground under its 60 % veil.
  - S7: `{% photo "home.ecosystem" "<class>" variant="campata" %}`.
  - `test_home.py::test_black_and_white_rests_only_in_the_hero` gets the stone slot (§8; it is desaturated, not black
    and white).
  - Once the panels are adopted, the pilot's 4:5 crops are no longer drawn; a later imagery pass may retire them.
- **P1:**
  - PA-1: the four `pathways.family.*` at the lane heads (3:2 from 64 rem, 21:9 strip below).
  - F1: `training.before` beside `training.after`.
  - U1: `universities.exchange` as the destination panel. Its `sizes` is the 6/12 track per container step; pass
    `sizes=` if the overlap changes the width.
- **P2:** Le projet's D panorama, `{% photo "project.volumes" "<class>" %}` inside S's `.panorama` with `data-parallax`.
- **Steward (merge):**
  - Ownership family «v522-m» with these slices: `apps/pages/imagery.py`,
    `apps/pages/templatetags/pages_imagery.py` (the imagery tag: unlisted in §9.7, extended here), `tools/build_derivatives.py`,
    `static/img/v5/**`, `docs/IMAGE_LICENSES.md`, `docs/design-v5/ASSET_USAGE_MATRIX.md`,
    `tests/compliance/test_imagery_v512.py`, `tests/frontend/test_imagery_v522_m.py`,
    `templates/dev/designpreview/specimens/imagery.html`, `static/css/dev/specimen-imagery.css`, one row in
    `apps/designpreview/live.py` and one in the specimens README, and these notes.
  - The catalogue pass with §6's renderings.

## 8. Not done (by design or out of scope)

- The frames are not on their pages yet: lanes H, P1 and P2 compose those sections. The board shows them at their V2
  widths meanwhile.
- The «select» grade is rendered by S's `photo.html` (request 7.S.1).
- `locale/**` entries come from the merge's catalogue pass (§5, §6).
- No LCP measurement on 8782: no eager image and no composition changed. The one live change, the campus re-crop, is
  a lazy body frame (+1.5 KB).

Evidence (headed Chromium chromium-1234): `C:/tmp/ile_v5_council/evidence/v522/m/` — the board at 1440, 768 and 390 and
390 under reduced motion (`board_*_s1…s7.png`, no horizontal overflow, no console error); the campus before/after at
1440, 768 and 390 in fr and ar plus reduced motion (`univ_*`); the home pilot and ecosystem unchanged (`home_*`);
`shots.json`, `weights_390_dpr2.json` (both servers, 18 pages), `board_weights.json` (each frame's file at 390@2 and 1440@1).

## 9. Round 1 improvements (QA_ROUND1 → label v522-m-improve1, 30–31 Oct 2026)

The review (`evidence/v522/m/QA_ROUND1.md`) did not pass the lane: a test-rule violation (M1), the marble panel cut on
the gesture (M2), the frame set at 3.7 / 5 against the bar of 4, and five minors (m1–m5). This round fixes all of them
in the files and the frames themselves, replaces two weak frames, and makes the one live `sizes` exact. Same branch and
worktree; tests on a private database (`TEST_DATABASE_URL=…/ile_t_m_imp1`); lane server 8784 (dev settings, database
`ile_v5_l4`, `ILE_DESIGN_PREVIEW=1`, reference date 2026-10-03), stopped at the end; headed Chromium chromium-1234 on
lock slot A (00:27:50–00:42:58 and 00:43–00:44:35, released both times). Scripts: `C:/tmp/ile_v5_council/.work/v522-m-imp1/`.

### 9.1 M2 — the marble's 2:3 panel keeps the gesture

- New crop: x 0.31–0.7545 of the frame (`crop_px [1860, 0, 4527, 4000]`, full height). It trims the thumb, never the
  blade. The blade's outer corner (x 0.672 of the frame) now sits at 0.814 of the panel.
- Cover simulation on the **served** 1 600 w AVIF, as S4 draws it (about 30 % wide × 82 vh, `object-fit: cover`,
  centred; the reviewer's `evidence_crops.py` method). Margin of the blade on the stone from the drawn edge:

  | Viewport | Panel | Margin |
  |---|---|---|
  | 1024 × 768 | 307 × 630 | 6.8 % |
  | 1280 × 800 | 384 × 656 | 14.1 % |
  | 1440 × 900 | 432 × 738 | 14.2 % |
  | 1920 × 1080 | 576 × 886 | 17.7 % |
  | 1024 × 768, a narrower 28 % panel | 287 × 630 | 3.8 % (centred) · 8.4 % at `object-position: 60% 50%` |

  Evidence: `evidence/v522/m/imp1_pilot_panels_cover_sim.jpg` and `.json`.
- Held by `test_v522_the_full_resolution_check_holds_in_the_crops`: the corner at ≤ 0.82 of the panel, full height.
- **For H (S4):** marble `object-position: 60% 50%` (physical, the same in ar: a photograph never mirrors), never toward
  the left; cedar centred (50 %) or up to 40 %, never toward the right (at 1024 × 768 the ringed hand's fingertips are
  near the left edge). In LTR the marble half sits at the band's far edge with its tool pointing out of the band: H may
  mirror the anatomy (marble at the reading edge), never the photograph.

### 9.2 m1 and the set's art direction — two frames replaced

| Slot | Was | Now | Why |
|---|---|---|---|
| `pathways.family.study` | 6549915 (QA: 3 / 5) | **6334273** · slug `notes-cahier-livre` | At desk level, not from above: a hand writes in a ruled notebook with a white pen, an open book behind it. Warm (brown tweed, pink shirt, pale wood): mean saturation 49–54 on every derivative, against 27–29 before, so «select» visibly turns it to colour. The face is above the frame (both crops start under the collar, y ≥ 0.14). The handwritten figures and words beyond the pen are softened by **one** box, where the page already falls out of focus, so there is no seam; the pen's line and the drawn arrows beside it stay sharp. The books carry nothing legible; the pen has no mark |
| `pathways.family.family` | 3184192 (QA: 3 / 5, generic brunch styling) | **27177298** · slug `table-partagee-vue-haut` | Still from above, as §8.1 prescribes for «Famille»: a shared table on an openwork wooden top, bowls of olives, tomatoes, a dip and peanuts; one hand holds out a spoon, the other holds the olive bowl. Warm and textured (mean saturation 85–97). Both crops stop at x 0.81, before the bread board (a filled loaf), and start under the glasses (one of them beer) and a third hand at the top edge (y < 0.13). No face, no lettering, no brand |

- Overhead tabletops on the site: four → three (Réseau's head, Diplômes' head, and «Famille», which §8.1 prescribes).
- New invariant: `test_v522_a_select_frame_carries_colour_for_the_select_to_reveal`. Every derivative of a «select»
  frame has a mean saturation ≥ 45 (measured: work 66.5–69.8, study 49.4–54.2, family 84.8–96.6, other 60.9–70.0).
- The slugs follow the frames (one frame, one slug); §8.1's slugs named the first frames. The slot keys, which the
  other lanes use, do not change.
- Rejected candidates, each with its reason: `docs/IMAGE_LICENSES.md` §3.4, last paragraph. The two originals were
  fetched once from the Pexels CDN into `.work/v522-m-imp1/originals/`; the key came from the environment and was
  neither printed nor written.
- **The campus frame stays as §8.2 decided.** Between the book's edge (x 0.555) and the lowest chin (y 0.40) there is
  no other 3:2 without a redaction, so «the academic cue» could only come back with blurred covers. The thumbs-up
  reading at 768 is a note for P1 (U1 can draw the destination smaller, beside the route) and for the Director.

### 9.3 M1 — the V5.12 budget restored, the WebP held to the ceiling

- **Builder.** `WEBP_ALLOWANCE` is gone. A kind's ceiling binds AVIF and WebP alike, as the builder's docstring
  already said. A WebP width that cannot fit at q 40 is not built and is listed in `webp_not_built`: 19 widths across
  the V5.22 renderings. Every AVIF width stays, under its ceiling. The provenance no longer records an allowance.
- **Two ladder steps.**
  - The panorama's 16:9 gains its 480 w (§8: 480 / 800 / 1 200 / 1 600), so it stays under the V5.12 assertions.
  - The ground's and the panorama's phone 4:5 gain a 640 w. Their 800 w WebP cannot fit 40 / 45 KB at q 40, and the
    `<img>`'s WebP `srcset` must keep two widths (V5.12's `test_the_picture_carries_both_formats_and_explicit_dimensions`).
    A phone without AVIF now gets 640 instead of 480.
- `universities.exchange`'s 1 200 w WebP: 49 674 → **45 178 B** (≤ 46 080). Its 1 600 w WebP is 44 898 B.
- Every AVIF file of a recipe whose crop did not change is byte-identical to round 0 (git shows no change). The only
  AVIF that changed are the marble's 2:3 (new crop) and the two new frames.
- **The test.** `test_the_weights_hold_their_budget` has its V5.12 body again. Only two cited tables let a rendering
  out, each from the ONE assertion its §7.3 kind contradicts:
  - `OWN_CEILING_V522`: the limit, for the two 2:3 pilot panels (60 KB) and the ground's 4:5 (its role has no V5.12
    limit);
  - `OWN_LADDER_V522`: the «480 and 800 / 1 200 and 1 600» widths, for the four family frames, whose ladder §7.3 ends
    at 720 w.

  Every other file is held as before in both formats. That includes `universities.exchange`'s 3:2, every V5.12 and
  V5.15 file, the bench, the volumes, the stone's 21:9, the ecosystem's 4:3, and the cedar's and marble's 3:2.
- **Verification.** I ran the UNMODIFIED V5.12 logic on the new provenance. It fails on exactly 19 items:
  - 6 files of the 2:3 panels (4 AVIF, 2 WebP), all under the panel's 60 KB;
  - 5 files of the ground's 4:5 (no V5.12 limit for role «ground»);
  - 8 family-frame ladders.

  Nothing else fails. Each of these renderings is held on every width, AVIF and WebP, under its kind's ceiling, with
  no allowance (`test_v522_every_new_frame_holds_its_kind_ceiling_on_every_width`, which also asserts that the
  provenance records no allowance and that every unbuilt WebP has its AVIF).
- New guard: `test_v522_only_section_7_3_kinds_leave_the_v512_budget`. The exemptions are a subset of the §7.3 kinds,
  and none is a V5.12 slot's own ratio (the campus 3:2, the ecosystem 3:2, the pilot 4:5).
- **V5.20, the four conditions:**
  1. the old expectation conflicts with §7.3 (the 2:3 panel at 60 KB, the ground a kind of its own, the family frame
     at 720 w);
  2. the new behaviour is implemented on purpose (the builder's kinds);
  3. the invariant is the same or stronger (every width, both formats; the V5.12 assertions unchanged everywhere
     else);
  4. the reason is cited in the test and here.

  The docstrings (builder, test) and §5 above are corrected.

### 9.4 m2 — drawn width = `sizes` on the real page, and the `sizes` made exact

- `tests/frontend/test_imagery_v522_m.py` now opens `/fr/` and `/ar/universites-et-formation/` at 1 600, 1 440,
  1 199 and 1 024 (1×) and at 768 and 390 (2×). It evaluates the `<img>`'s own `sizes` as the browser does, with each
  `vw` read against the layout viewport, so the classic scrollbar is measured, not tolerated. It asserts:
  - |drawn − sizes| ≤ 1.5 px;
  - the raw evaluation is never below the drawn width (no under-fetch);
  - the ratio, the file picked for the density, lazy / async / boxes, and no overflow.
- The test found three real errors in the slot's `sizes`. Round 0's ±4 % and the scrollbar had hidden them:
  - under 430 px the page margin is 20 px, not 24, so the 390 frame was drawn 8 px wider than stated;
  - `45vw` is exact only near 1 040 px (8 px short at 1 199);
  - `42rem` was 4 px over at the 1 440 container.
- New value: `(min-width: 100rem) 41.75rem, (min-width: 90rem) 38rem, (min-width: 75rem) 33.5rem, (min-width: 64rem)
  calc(50vw - 3.25rem), (min-width: 48rem) calc(100vw - 5rem), (min-width: 26.875rem) calc(100vw - 3rem),
  calc(100vw - 2.5rem)`. It is derived from the tokens: 6/12 = (container − 80 − 11 × 24) / 2 + 5 × 24.
  - Headed, 12 widths, fr and ar: |drawn − sizes| ≤ 0.4 px, no under-fetch (`evidence/v522/m/imp1_univ_sizes_steps.json`).
  - The files picked do not change at the audited widths.
- The family frames (`FAMILY_SIZES`) and `training.before` get the same 430 px step.
- The bench test no longer compares drawn and `sizes` (circular there). It keeps the art direction, the pick for the
  evaluated `sizes` at each density, the markup and no overflow.

### 9.5 m3 — the bench is a fixture, not a preview page

- `apps/designpreview/live.py` is back to the base (its `SPECIMEN_BOARDS` row is gone; lane M no longer touches that
  file). The specimens README calls the board a test fixture, not listed in the index. The board answers 200 by URL;
  the index has no link to it.
- Lane M announces nothing as «visible in preview».
- **Neutral vocabulary.** No pattern or lane name in its prose. Only the registry's own identifiers appear, in
  `<code>` (slot keys, variant keys).
- **No mock composition.** No night band, no colophon placeholder, no simulated «select», no paired panels, no drift
  scale. Each frame stands alone on paper. The French page names carry `lang="fr"`.
- **No `vw`.** Boxes are sized in % of the container. Headed at 8 widths with the classic 15 px scrollbar: overflow 0,
  `scrollX` 0 after `scrollTo(10000, …)`, 0 console errors (`imp1_headed_session.json`, `imp1_board_{1440,768,390}_full.jpg`).

### 9.6 m4 — the catalogue, for the steward, and the new strings

`tests/i18n/test_catalogues.py` fails 4 cases (`[it|en|ar]` and the audit script) on exactly the seven V5.22 alt
msgids, two of them new in this round. This is expected under §9.7 (`locale/**` belongs to S-close).

**Ready for the merge:** `evidence/v522/m/imp1_catalogue_entries_{it,en,ar}.po`. The msgids are copied from
`imagery.py` byte for byte; the msgstr are the renderings of §6 and below.

**Merge plan (the steward's call):** carry `scripts/i18n_audit.py --sync`, these msgstr and `--compile` in M's merge
commit, so design-v5 stays at FAILURES 0 until S-close. The sync drops the now unused msgids: the two retired frames'
and the campus's V5.12 alt.

New alternative texts (supersede §6 rows 3 and 4; no locked copy involved; the Arabic is RTL with no Latin run):

| Slot | FR (msgid) | IT | EN | AR |
|---|---|---|---|---|
| `pathways.family.study` | À une table de travail, une main prend des notes au stylo dans un cahier, devant un livre ouvert | A un tavolo di lavoro, una mano prende appunti a penna su un quaderno, davanti a un libro aperto | At a work table, a hand takes notes in pen in a notebook, in front of an open book | على طاولة عمل، يدٌ تدوّن ملاحظات بالقلم في دفتر، أمام كتاب مفتوح |
| `pathways.family.family` | Vue d’en haut, une table partagée : des mains se servent dans des bols d’olives et de tomates, sur un plateau de bois ajouré | Vista dall’alto, una tavola condivisa: alcune mani si servono da ciotole di olive e pomodori, su un piano di legno traforato | Seen from above, a shared table: hands help themselves from bowls of olives and tomatoes on an openwork wooden top | مائدة مشتركة من منظر علوي: أيادٍ تتناول من أوعية الزيتون والطماطم، فوق سطح خشبي مخرّم |

### 9.7 m5 — ASSET_USAGE_MATRIX §11

The `universities.exchange` row states the code's exact value (§9.4) and how it was measured. The study, family and
marble rows describe the new frames and crop. The ceilings paragraph states the WebP rule and calls the board a
fixture. IMAGE_LICENSES §3.4 is updated the same way.

### 9.8 Measurements

- **Files.** Every AVIF and every WebP of every V5.22 rendering is under its kind's ceiling (test). The changed
  renderings' largest AVIF:
  - marble 2:3: 49.6 / 60 KB;
  - study: 9.3 (3:2) · 14.3 (21:9) / 30 KB;
  - family: 28.0 · 29.8 / 30 KB.
- **Repository.** `static/img/v5/` holds 289 files, 10 354 KB (round 0: 294 files, 10 946 KB). No orphan and no missing
  derivative against the provenance. `build_derivatives.py --check` is ok.
- **Weight at 390 × 844 DPR 2,** headed, full scroll: `/fr/universites-et-formation/` 37.7 KB, the same as round 0 (the
  AVIF are byte-identical and the 390@2 pick is still the 800 w).
- **Projected, once the lanes draw the frames** (the files the browser takes at 390@2): Parcours +66.5 KB (the four
  21:9 strips at 720 w; round 0 +66.1). Home +51.2 KB and Le projet +42.5 KB are unchanged. All are far under 250 KB.
- **Headed Universités,** fr / it / en / ar at the 8 widths: 0 overflow, 0 console errors. Reduced motion (fr, ar at 1440
  and 390): opacity 1, no transform, no clip. No-JS: the frame loads (608 × 405 at 1440, 335 × 223 at 390). In ar the
  photograph is not mirrored; its alt is the French fallback with `lang="fr"` until the catalogue pass (§9.6).

### 9.9 Scores (§26, self-assessed; the reviewer verifies)

- **The frame set's art direction: about 4.1** (round 0: 3.7).
  - Raised: marble 3 → 4.5 (the gesture kept at every laptop size), study 3 → 4.5, family 3 → 4.5.
  - Unchanged: stone 4, volumes 4.5, work 3.5, vines 4.5, bench 4, cedar 4.5, ecosystem 3.5, campus 3.5.
- **Universités: imagery 3.5,** the same crop, now with an exact `sizes`. Composition 2.5, motion 2.5 and interaction 2
  belong to P1's U1 «la filiera» (§3.8). Lane M must not build it: `templates/ecosystem/**` is P1's (§9.7). Those
  scores are P1's acceptance bar.
- **The bench** is not a product page, is no longer announced, and is not scored.

### 9.10 Requests to other lanes (in addition to §7)

- **H.** S4:
  - `object-position` as in §9.1; panels ≥ 30 % wide from 64 to 80 rem, or the marble's 60 %;
  - state the panel's real width: at 4:3 screens `cover` draws 82vh × 2/3, wider than 34vw, so for example
    `sizes="(min-width: 64rem) max(34vw, 54.67vh), 100vw"`;
  - assert drawn = `sizes` on `/fr/` and `/ar/` with this test's probe, for the panels, the stone and the `campata`
    variant.
- **P1.** When Parcours, Formation and Universités place the frames:
  - assert drawn = `sizes` there with the same probe (`tests/frontend/test_imagery_v522_m.py::PROBE`; pass `sizes=` to
    `{% photo %}` if the composition draws another width);
  - draw the campus destination smaller at 768 (the thumbs-up reading);
  - `training.before`'s tone against `training.after` (QA note).
- **P2.** Assert drawn = `sizes` for `project.volumes` on Le projet (`112vw` from 48 rem under M22).
- **Steward.**
  - The catalogue sync in M's merge (§9.6).
  - The ownership family «v522-m» no longer needs a slice of `apps/designpreview/live.py` (reverted to the base). The
    other slices of §7 stand.
- **Director** (QA notes, not M's to decide):
  - Le projet will show books twice (`project.hall`'s shelves and `project.volumes`);
  - the campus frame's academic cue against §8.2's no-redaction rule.

### 9.11 Tests (round 1, private database `ile_t_m_imp1`)

- `tests/compliance/test_imagery_v512.py`: **39 passed**. Two are new: the exemptions guard and the «select» colour
  invariant. `test_the_weights_hold_their_budget` is restored as §9.3 says.
- `tests/frontend/test_imagery_v522_m.py` (browser): **17 passed** (12 real-page cases, 5 bench cases).
- `tests/frontend/test_browser_v515_c.py`: 4 passed (the developing frames still develop).
- `tests/frontend/test_design_preview.py`, `apps/pages/tests/test_home.py`, `tests/compliance/test_figure_caption.py`
  (non-browser): 386 passed.
- `tests/i18n/test_catalogues.py`: 4 failed, 49 passed. This is the expected msgid gap (§9.6).
- `ruff check` and `ruff format --check`: clean on the changed Python. `manage.py check`: 0 issues. No CRLF in any
  changed file. `main.css` untouched (no product stylesheet or script changed).

### 9.12 Not done in this round

- `pathways.family.work` (3.5: it reads as retail) and the ecosystem 4:3 (3.5: the V5.12 blurs show at 57vw) keep
  their frames. They are candidates for a later imagery pass.
- Lane M composes no section (§9.9).
- No LCP measurement: no eager image changed.

Evidence of this round (`C:/tmp/ile_v5_council/evidence/v522/m/`):
- `imp1_pilot_panels_cover_sim.{jpg,json}`, `imp1_univ_sizes_steps.json`, `imp1_headed_session.json`;
- `imp1_univ_{fr,it,en,ar}_*.jpg`, `imp1_univ_rm_{fr,ar}_{1440,390}.jpg`, `imp1_univ_nojs_fr_{1440,390}.jpg`;
- `imp1_board_{1440,768,390}_full.jpg` (1440 and 390 recaptured after the `sizes` change);
- `imp1_catalogue_entries_{it,en,ar}.po`.
