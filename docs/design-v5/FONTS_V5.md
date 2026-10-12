# FONTS V5 — type «Una voce» in the product

W1-A (the foundation family), 5 October 2026. Decision: `docs/design-v5/V5_4_EXECUTION_PLAN.md` §1.1 (Host Grotesk for
everything; «ILE Wordmark» for the name; «ILE Mono» for references; Vazirmatn for Arabic) and §2.3 («Fonts»). This file
records where each shipped face comes from, how it was built and renamed, its hash, its licence, how it loads and what it
costs. The stylesheet is `static/css/v5/fonts.css`; the licences are in `static/fonts/licenses/`.

## 1. The five faces, in six files

| File (`static/fonts/`) | CSS family · style · weights | Code points | Bytes | SHA-256 |
|---|---|---|---|---|
| `v5-host-grotesk-var-400-700.woff2` | Host Grotesk · normal · variable `wght` 400–700 | 224 | 19 208 | `458475e1e1b89620b618b98268e495d150df18c3885c7b55875a12b1370f2f3c` |
| `v5-host-grotesk-400-italic.woff2` | Host Grotesk · italic · 400 | 224 | 14 096 | `b65558a91c0ac909c3f25b8832811ace521cf3455aff7d0b0f0e58b778cdc60c` |
| `v5-ile-wordmark-600.woff2` | ILE Wordmark · normal · 600 (Newsreader, `opsz` 20) | 11 | 1 748 | `94d2e525f5377ebaf92e57ab71599e1dc18447cadf543dfc0b2b336bf25ae06d` |
| `v5-ile-mono-400.woff2` | ILE Mono · normal · 400 — the reference core | 46 | 2 688 | `699d02a2741c5540656f073a0ed8c28a4b8d8bd9aaf2156d6d279960ac4addff` |
| `v5-ile-mono-400-ext.woff2` | ILE Mono · normal · 400 — the rest of the subset | 179 | 7 272 | `00c1f05ab30eda2fe0f858c247400292ebe03069b3b9437c19deb51c54e89a67` |
| `v5-vazirmatn-var-400-700-arabic.woff2` | Vazirmatn · normal · variable `wght` 400–700 | 363 | 32 228 | `e303c6e31432690e237fa45d115400f350b0c55ed0255ff34e23ced8a8521fbd` |

Upstream versions, read from each file's name ID 5: Host Grotesk 1.003 · Newsreader 1.003 · IBM Plex Mono 2.3 ·
Vazirmatn 33.003. Not carried (§1.1): Markazi Text, Source Serif 4, and every V4 face (IBM Plex Sans, IBM Plex Sans Arabic,
IBM Plex Mono's fontsource files, Newsreader's full variable files, Noto Naskh Arabic) — 26 files, ≈ 965 KB, removed with
`static/css/fonts.css`. `scripts/fetch_fonts.py` generated that V4 sheet; it is no longer the source of any shipped face.

## 2. Provenance and build

**The gate-0 files.** The typography council built them in September 2026 with fontTools 4.60.2 and brotli
(`C:/tmp/ile_v5_council/scratch/typography/tools/subset_measure.py`, `measure_v5.py`): the variable masters from
`google/fonts` (`ofl/hostgrotesk`, `ofl/newsreader`, `ofl/ibmplexmono`) and the `@fontsource-variable/vazirmatn` Arabic file;
`fontTools.varLib.instancer` to limit or pin the axes (Host Grotesk `wght` 400–700; Newsreader `wght` 600 at `opsz` 20;
Vazirmatn `wght` 400–700); `fontTools.subset` with the French / Italian / English charset (Latin-1, ı Œ œ Ÿ ˆ ˜, the
general punctuation, € № ™, the four arrows and ↗, − ∕ ≤ ≥), the Arabic block ranges for Vazirmatn plus U+0020 and U+00A0,
and the text «ITALY LEGAL ENTRY™» for the wordmark; `hinting = False`, `desubroutinize = True`, name IDs 0–6, 13, 14 kept
(the copyright and the licence travel with the file). They were copied byte for byte into the foundation,
`C:/tmp/ile_v5_council/proof/assets/fonts/`, which gate 0 measured (0 CSP violations, swap CLS ≤ 0.007 with the matched
fallbacks: `TYPOGRAPHY_REVIEW.md` §5.3).

**Into the product (W1-A).** `C:/tmp/ile_v5_council/evidence/v54/w1-a/tools/build_v5_fonts.py`, a dev-time step outside the
product's requirements (plan §2.3; no runtime dependency, no network):

```
C:/Python313/python.exe C:/tmp/ile_v5_council/evidence/v54/w1-a/tools/build_v5_fonts.py          # write
C:/Python313/python.exe C:/tmp/ile_v5_council/evidence/v54/w1-a/tools/build_v5_fonts.py --check  # compare, write nothing
```

What it does, file by file:

- **Host Grotesk, roman and italic.** Glyphs, tables and axes untouched. The name table is corrected: the subset kept the
  upstream default instance's «Light» in name IDs 1, 3, 4 and 6 («Host Grotesk Light», «HostGrotesk-Light») although its
  `wght` axis now starts at 400, whose named instance is «Regular» — the check plan §2.3 asked for. They now read «Host
  Grotesk», «1.003;LMNT;HostGrotesk-Regular» (`-Italic`), «Host Grotesk Regular» (`Italic`), «HostGrotesk-Regular»
  (`-Italic`). Host Grotesk declares no Reserved Font Name.
- **«ILE Mono».** IBM Plex declares the Reserved Font Name «Plex», and a subset is a Modified Version (OFL 1.1, condition 3):
  name IDs 1, 3, 4 and 6 are renamed «ILE Mono», «2.3;ILE;ILEMono-Regular», «ILE Mono Regular», «ILEMono-Regular» (the
  script fails if any of IDs 1, 3, 4, 6, 16, 17 still contains «Plex»); IBM's copyright (ID 0, «Copyright 2017 IBM Corp. All
  rights reserved.») and the licence (IDs 13, 14) are kept; ID 10 says what was modified («Modified Version of IBM Plex Mono
  Regular: subset to Latin-1 and punctuation, renamed ILE Mono because Plex is a Reserved Font Name. SIL Open Font License
  1.1.»). FOUNDATION_NOTES §6 and TYPOGRAPHY_REVIEW C7 asked for this rename; the CSS family string is free either way.
- **«ILE Mono» in two files.** The renamed subset is split by `fontTools.subset` into the **reference core** — space,
  `# + , - . / : _`, the digits, the capitals, U+00A0: what a case or document reference is made of (EE167596D4) — and
  **the rest** (lower case, the other punctuation, Latin-1, the typographic marks), with complementary `unicode-range`s in
  `static/css/v5/fonts.css`. A page whose references are digits and capitals downloads 2 688 bytes of mono instead of
  9 116; the Arabic console (Vazirmatn + Host Grotesk + the wordmark + the core = 55 872 bytes) then holds the 56 KB budget
  of plan §2.6, which the whole subset broke (63.6 KB measured on lane 3).
- **«ILE Wordmark»** and **Vazirmatn**: byte copies. Neither family declares a Reserved Font Name.
- **Reproducible.** The fonts are opened with `recalcTimestamp=False`, so `head.modified` keeps the upstream date and two
  runs write the same bytes (`--check` exits 0 on a clean tree).

## 3. Licences

| Text (`static/fonts/licenses/`) | Covers | Copyright line | Reserved Font Name |
|---|---|---|---|
| `OFL-HostGrotesk.txt` | `v5-host-grotesk-*` | Copyright 2023 The Host Grotesk Project Authors | none |
| `OFL-Newsreader.txt` | `v5-ile-wordmark-600.woff2` | Copyright 2020 The Newsreader Project Authors | none |
| `OFL-IBMPlexMono.txt` | `v5-ile-mono-400.woff2`, `v5-ile-mono-400-ext.woff2` | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" | «Plex» — honoured by the rename |
| `OFL-Vazirmatn.txt` | `v5-vazirmatn-var-400-700-arabic.woff2` | Copyright 2015 The Vazirmatn Project Authors | none |

Each is the SIL Open Font License 1.1 text shipped with the family, copied from the gate-0 folder with LF line ends —
IBM's came with CRLF, the repository holds every file with LF (SHA-256: Host Grotesk `f04ad087…`, IBM Plex Mono
`37784b44…`, Newsreader `fdfad381…`, Vazirmatn `17e35506…`). The header of
`static/css/v5/fonts.css` points to them.

## 4. How the faces load

- `font-display: swap` on every face; `unicode-range` as the council set it, so the Arabic file never loads on a Latin page
  and the Latin files never draw Arabic. A face downloads only when text needs it.
- **Preloads** (`templates/base.html`, plan §1.1 «Loading»; PFR §0): a Latin page preloads Host Grotesk and the wordmark
  (2); an Arabic page Vazirmatn, Host Grotesk for the Latin runs and the digits, and the wordmark (3). The preload hrefs are
  the files the bundle's `url()` names, so under the manifest storage they are one request.
- **«ILE Mono» has one seat** — references, hashes, rule versions (`code`, `.t-ref`, `.ctx__ref`, `.doc-workspace__ref`,
  `.error-page__ref`). The legacy sheets set their footer labels, the pilot's shore names, the questionnaire's count,
  journey and timeline dates and chip counters in the mono; `static/css/v5/base.css` gives those the sans with tabular
  figures, so a page without a reference downloads no mono.
- **Metric-matched fallbacks** (`size-adjust` / `ascent-override` / `descent-override`, line gap 0), the typography lane's
  method (`P/research/type/tools/fallback_metrics.py`, 626 characters of product copy; W1-A's
  `evidence/v54/w1-a/tools/fallback_extra.py` for the two faces the foundation left without one):

| Face | Fallback | size-adjust | ascent | descent | Platform |
|---|---|---|---|---|---|
| Host Grotesk | ILE Sans Fallback = Segoe UI | 105.5 % | 96.2 % | 29.9 % | Windows |
| Host Grotesk | ILE Sans Fallback Arial = Arial | 104.5 % | 97.1 % | 30.1 % | Windows, and macOS / iOS (same Arial metrics) |
| Host Grotesk | ILE Sans Fallback Android = Roboto | 105.1 % | 96.6 % | 30.0 % | Android (computed from the file, not verified on a device) |
| Vazirmatn | ILE Arabic Fallback = Segoe UI | 97.1 % | 105.6 % | 55.3 % | Windows |
| ILE Wordmark | ILE Wordmark Fallback = Georgia | 103.4 % | 71.1 % | 25.6 % | Windows, macOS |
| ILE Mono | ILE Mono Fallback = Consolas | 109.1 % | 93.9 % | 25.2 % | Windows |

  Not computed, because the fonts are not on this machine: Apple's own system faces (SF, Helvetica, Geeza Pro) — before the
  integration milestone (plan §7) — and the Android Arabic face (Noto Naskh / Noto Sans Arabic).
- **Swap CLS** (the gate: ≤ 0.01 with the matched fallbacks, DL54-04). Measured on lane 3 with the typography lane's
  method — every woff2 held for 1.5 s, the layout shifts of the swap summed (`evidence/v54/w1-a/tools/cls_swap.py`,
  `evidence/v54/w1-a/cls-swap-1/cls_swap.json`), Windows fallbacks, 5 October 2026: **0.0000 – 0.0009** on the home
  (1440, 390), the login, the dashboard, the documents (1440, 390), the Arabic home (390) and the Arabic dashboard; with
  the overrides stripped, up to 0.0200 (the documents at 390) — the fallbacks are load-bearing. The Android fallback
  (Roboto) is computed, not yet measured; Apple's before the milestone.

## 5. What a page downloads (font bytes, measured on lane 3, 8783, 1440 × 900, 5 October 2026)

| Page | V4 (W1-0 «before» set, 8782) | V5 (W1-A) | Budget (plan §2.6) |
|---|---|---|---|
| a Latin public page (home, login, door, FAQ) | 304 340 / 217 732 B | 20 956 B (Host Grotesk + the wordmark) | ≤ 25 KB |
| a Latin console page (dashboard, documents, case file) | 217 732 B | 23 644 B (+ ILE Mono's core) | ≤ 32 KB |
| an Arabic public page | 484 456 – 525 044 B | 53 184 B (Vazirmatn + Host Grotesk + the wordmark) | ≤ 56 KB |
| an Arabic console page | 484 456 B | 55 872 B (+ ILE Mono's core) | ≤ 56 KB |

Unthrottled lane figures, from the file sizes the browser fetched (`evidence/v54/w1-a/<label>/audit.json`); the
performance PASS is measured on 8782 by the Performance Lead, never here. Each measurement is kept with its date in
`docs/design-v5/QA/v54/w1-a/IMPLEMENTATION_NOTES.md`.

## 6. What holds this file

- `tests/frontend/test_v5_tokens.py::test_fonts_v5_md_records_every_shipped_face_with_its_bytes_and_hash` — every woff2
  in `static/fonts/` is in the table of §1 with its size and SHA-256, and each licence text with the opening of its hash
  (§3): a face rebuilt, added or removed without this file turns the suite red.
- `tests/frontend/test_v5_tokens.py::test_the_five_faces_are_self_hosted_with_their_licences` and
  `::test_the_matched_fallbacks_cover_windows_apple_through_arial_and_android` — the six files, `font-display: swap`,
  the `unicode-range`s, the four OFL texts, IBM's Reserved Font Name, the fallback faces `local()` only.
- `tests/frontend/test_layout.py::test_fonts_css_references_only_local_files_that_exist` — the stylesheet's six `url()`s
  and the licences it points to; `::test_html_lang_and_dir_attributes` — the preloads per script (2 Latin, 3 Arabic).
- `tests/frontend/test_design_docs.py::test_listed_font_files_exist_and_every_font_file_is_listed` — DESIGN_SYSTEM_2026
  §6.2 lists the same files.
- In a browser: `tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded` (Host Grotesk and the wordmark
  loaded on a Latin page, no Arabic face, no request to another host) and
  `tests/i18n/test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded` (Vazirmatn then Host Grotesk on an
  Arabic page, the V4 faces gone).
