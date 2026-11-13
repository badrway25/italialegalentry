# FONTS V5 — type «Una voce» in the product · Typography V2

W1-A (the foundation family), 5 October 2026; **Typography V2** (lane T, `v524-t`, 5 November 2026: V5.24 §11–§14,
`evidence/v524/TYPOGRAPHY_V2.md` §3–§4.7, `FINAL_DELIVERY_V2.md` R1, R4 g, §3.1). Decision: `docs/design-v5/V5_4_EXECUTION_PLAN.md`
§1.1 (Host Grotesk for everything; «ILE Wordmark» for the name; «ILE Mono» for references) and, since V2, **Readex Pro for
every Arabic role** in Vazirmatn's place — measured against Host Grotesk, Vazirmatn's Arabic sat 15–20 % smaller (tooth
0.351 em against Host's x-height 0.496; content area 1.562 em) and needed a second leading system; Readex Pro (content area
1.250 em, tooth 0.438, alef 0.740) sits at the same size and colour as the French beside it, on the Latin leadings, in half
the bytes. This file records where each shipped face comes from, how it was built and renamed, its hash, its licence, how it
loads and what it costs. The stylesheet is `static/css/v5/fonts.css`; the licences are in `static/fonts/licenses/`.

## 1. The six faces, in seven files (ILE Serif since V5.31)

| File (`static/fonts/`) | CSS family · style · weights | Code points | Bytes | SHA-256 |
|---|---|---|---|---|
| `v5-host-grotesk-var-400-700.woff2` | Host Grotesk · normal · variable `wght` 400–700 | 224 | 19 208 | `458475e1e1b89620b618b98268e495d150df18c3885c7b55875a12b1370f2f3c` |
| `v5-host-grotesk-400-italic.woff2` | Host Grotesk · italic · 400 | 224 | 14 096 | `b65558a91c0ac909c3f25b8832811ace521cf3455aff7d0b0f0e58b778cdc60c` |
| `v5-ile-wordmark-600.woff2` | ILE Wordmark · normal · 600 (Newsreader, `opsz` 20) | 11 | 1 748 | `94d2e525f5377ebaf92e57ab71599e1dc18447cadf543dfc0b2b336bf25ae06d` |
| `v5-ile-mono-400.woff2` | ILE Mono · normal · 400 — the reference core | 46 | 2 688 | `699d02a2741c5540656f073a0ed8c28a4b8d8bd9aaf2156d6d279960ac4addff` |
| `v5-ile-mono-400-ext.woff2` | ILE Mono · normal · 400 — the rest of the subset | 179 | 7 272 | `00c1f05ab30eda2fe0f858c247400292ebe03069b3b9437c19deb51c54e89a67` |
| `v5-readex-pro-var-400-700-arabic.woff2` | Readex Pro · normal · variable `wght` 400–700 | 222 glyphs (the Arabic blocks, the presentation forms, U+0020, U+00A0) | 16 128 | `9669ea48c988dd5b008349eb499b948ac5f3ee33f19aef001eca576bf956ec0e` |
| `v5-ile-serif-400.woff2` | ILE Serif · normal · 400 (Source Serif 4 Regular, `opsz` 48, renamed) — the home's institutional display role only | 278 glyphs (Latin-1, Œ œ Ÿ ı, the general punctuation block, € ™ № − ∕) | 18 732 | `f2593faaa15a9e45f2e3cd2e64d4cdf3c0a62e0940f7eb7d2f0415d414ddf75d` |

Shipped set: **61 140 B** (77 240 before V2; ceiling 62 000, §5). Upstream versions, read from each file's name ID 5: Host
Grotesk 1.003 · Newsreader 1.003 · IBM Plex Mono 2.3 · Readex Pro 1.205 · Source Serif 4 4.004.

**V5.31 FINAL ART PASS (owner, 11 November 2026, A2): «ILE Serif».** The owner's decision gives the home's statements (the
hero's opening phrase, the sections' H2 statements) an institutional serif: Source Serif 4, 400 roman, from the typography
council's folder (`council/typography/fonts/v5-SourceSerif4-400-opsz48-nosc.woff2`, the static `opsz` 48 cut without small
capitals). Built with `fontTools.subset` on that file: `--unicodes` = the Host Grotesk italic range above, `--layout-features
=kern,liga,ccmp,locl,mark,mkmk` (the figure and fraction features left: a statement never sets a table), `--no-hinting`,
`--drop-tables+=BASE,STAT`, `--name-IDs=*` — 25 820 B → 18 732 B; then name IDs 1, 3, 4, 6 rewritten to «ILE Serif» /
`4.004;ILE;ILESerif-Regular` / «ILE Serif Regular» / `ILESerif-Regular`, because Adobe declares «Source» a Reserved Font Name
and a subset is a Modified Version (the «ILE Mono» rule). Name ID 0 keeps Adobe's copyright. The 400 italic the council also
holds is **not** shipped (a statement is never italic). Public Sans, evaluated once against Host Grotesk for the text and UI
roles (FR 1440 and 390, Chrome), is **not** shipped either: 6–9 % wider, it broke the hero's columns, the station labels and
the pathway rail into extra lines and read generic. The serif is not added to the shared set and no ceiling covers the
two together: the budget is route-aware (§1 bis).

## 1 bis. Route-aware font budget (owner, 12 Nov 2026)

An intentional design-performance decision: the owner approved «ILE Serif» for the home's institutional statements, and its
cost is paid by the home alone. Two separate invariants, never one sum (`tests/frontend/test_fonts_budget_v2.py`):

- **The shared set** — the six files every route may fetch — stays at its ceiling, **61 140 B**, with every per-file ceiling
  unchanged (the variable sans 19 208, the italic 14 096, Readex Pro 16 128, the wordmark 1 748, the two mono files 9 960).
- **The serif is a declared HOMEPAGE-ONLY addition** with its own file ceiling, **18 732 B** (its measure, only down): read
  only under `.page-home` (the one consuming rule in `static/css/v5/_home-a.css`; the built bundles hold it the same way),
  never preloaded, Readex Pro on an Arabic run.

Per route (Chromium, encoded bytes): the Latin home (fr, it, en) **≤ 39 688 B** — Host Grotesk + the wordmark + ILE Serif,
its current measure; every other Latin public page **≤ 20 956 B** and fetches no serif; every Arabic page, the home
included, **≤ 37 084 B** and never fetches the serif. Any other route adopting the serif requires its own owner decision and
its own measured ceiling; growth of either budget is never normalised — a ceiling only goes down.

Not carried (§1.1): Markazi Text, Source Serif 4 under its own name,
every V4 face (IBM Plex Sans, IBM Plex Sans Arabic, IBM Plex Mono's fontsource files, Newsreader's full variable files, Noto
Naskh Arabic — 26 files, ≈ 965 KB, removed with `static/css/fonts.css`) and, since V2, Vazirmatn (`v5-vazirmatn-var-400-700-arabic.woff2`,
32 228 B, and `OFL-Vazirmatn.txt`). `scripts/fetch_fonts.py` generated that V4 sheet; it is no longer the source of any shipped face.

## 2. Provenance and build

**The gate-0 files.** The typography council built them in September 2026 with fontTools 4.60.2 and brotli
(`C:/tmp/ile_v5_council/scratch/typography/tools/subset_measure.py`, `measure_v5.py`): the variable masters from
`google/fonts` (`ofl/hostgrotesk`, `ofl/newsreader`, `ofl/ibmplexmono`); `fontTools.varLib.instancer` to limit or pin the
axes (Host Grotesk `wght` 400–700; Newsreader `wght` 600 at `opsz` 20); `fontTools.subset` with the French / Italian / English
charset (Latin-1, ı Œ œ Ÿ ˆ ˜, the general punctuation, € № ™, the four arrows and ↗, − ∕ ≤ ≥) and the text «ITALY LEGAL
ENTRY™» for the wordmark; `hinting = False`, `desubroutinize = True`, name IDs 0–6, 13, 14 kept (the copyright and the licence
travel with the file). They were copied byte for byte into the foundation, `C:/tmp/ile_v5_council/proof/assets/fonts/`,
which gate 0 measured (0 CSP violations, swap CLS ≤ 0.007 with the matched fallbacks: `TYPOGRAPHY_REVIEW.md` §5.3).

**The Readex Pro source (V2).** `google/fonts` `ofl/readexpro` as published — `ReadexPro[HEXP,wght].ttf` (278 544 B, version
1.205, SHA-256 `268bba7e1e8f3b14d798b3fb0e40ebaa3fc39308c9ac0020e2faf6df181cc30e`), `OFL.txt`, `METADATA.pb` (designers Thomas
Jockin, Nadine Chahine, Bonnie Shaver-Troup, Santiago Orozco, Héctor Gómez; subsets arabic, latin, latin-ext, vietnamese) —
kept outside the repository at `C:/tmp/ile_v5_council/evidence/v524/t/src/readexpro/`, read only through fontTools.

**Into the product.** `C:/tmp/ile_v5_council/evidence/v54/w1-a/tools/build_v5_fonts.py`, a dev-time step outside the product's
requirements (plan §2.3; no runtime dependency, no network):

```
C:/Python313/python.exe C:/tmp/ile_v5_council/evidence/v54/w1-a/tools/build_v5_fonts.py --dst <worktree>/static/fonts          # write
C:/Python313/python.exe C:/tmp/ile_v5_council/evidence/v54/w1-a/tools/build_v5_fonts.py --check --dst <worktree>/static/fonts  # compare, write nothing
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
  9 116. Since V2 the mono has one seat — `code`, `kbd`, `pre`, `.t-ref`, `.ctx__ref`, `.ws-case__ref`,
  `.error-page__ref`, `.db-ref`, `.reg-ref` (TYPOGRAPHY_V2 F-3; `tests/frontend/test_typography_v2.py`): the labels and
  step numbers that still drew it on six public pages are the lanes' burn-down, and a public page then downloads no mono.
- **«ILE Wordmark»**: a byte copy. Newsreader declares no Reserved Font Name.
- **Readex Pro (V2).** `fontTools.subset` on the product's Arabic recipe — `U+0020, U+00A0, U+0600-06FF, U+0750-077F,
  U+0870-08FF, U+200C-200F, U+2010-2011, U+204F, U+2E41, U+FB50-FDFF, U+FE70-FEFC` — with every layout feature kept
  (`init medi fina rlig calt ccmp aalt` in GSUB, `mark mkmk` in GPOS: the harakat U+064B–U+0651 the product's text uses
  are positioned), `hinting = False`, `desubroutinize = True`, name IDs 0–6, 13, 14; then `fontTools.varLib.instancer`
  limiting `wght` to 400–700 and pinning `HEXP` (Hyper Expansion) at its default 0; `recalcTimestamp = False`. The file
  holds 222 glyphs: the Arabic, the two spaces, never the digits or the Latin (the stack hands those to Host Grotesk, gate-0
  A6). Coverage: 47 of the 48 Arabic-block code points the product's texts use — the 48th is U+200E, a bidi control that
  needs no glyph. The family name stays «Readex Pro»: the OFL's Reserved Font Name is «RevReading Lexend», which the file
  never used, and the name table keeps the project's copyright (ID 0) and the licence (IDs 13, 14).
- **Licences**: the SIL OFL 1.1 text of each family, with LF line ends — IBM's came with CRLF, the repository holds every
  file with LF — into `static/fonts/licenses/`.
- **Reproducible.** The fonts are opened with `recalcTimestamp=False`, so `head.modified` keeps the upstream date and two
  runs write the same bytes (`--check` exits 0 on a clean tree; checked on 5 November 2026: the five W1-A files byte-identical
  to the committed ones, Readex Pro built twice to the same SHA-256).

## 3. Licences

| Text (`static/fonts/licenses/`) | Covers | Copyright line | Reserved Font Name | SHA-256 (opening) |
|---|---|---|---|---|
| `OFL-HostGrotesk.txt` | `v5-host-grotesk-*` | Copyright 2023 The Host Grotesk Project Authors | none | Host Grotesk `f04ad087…` |
| `OFL-Newsreader.txt` | `v5-ile-wordmark-600.woff2` | Copyright 2020 The Newsreader Project Authors | none | Newsreader `fdfad381…` |
| `OFL-IBMPlexMono.txt` | `v5-ile-mono-400.woff2`, `v5-ile-mono-400-ext.woff2` | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" | «Plex» — honoured by the rename | IBM Plex Mono `37784b44…` |
| `OFL-ReadexPro.txt` | `v5-readex-pro-var-400-700-arabic.woff2` | Copyright 2018 The Readex Pro Project Authors (https://github.com/ThomasJockin/readexpro), with Reserved Font Name “RevReading Lexend” | «RevReading Lexend» — never used: the subset keeps «Readex Pro» | Readex Pro `b41267a3…` |
| `OFL-SourceSerif4.txt` | `v5-ile-serif-400.woff2` | Copyright 2014 - 2021 Adobe Systems Incorporated (http://www.adobe.com/), with Reserved Font Name 'Source' | «Source» — honoured by the rename to «ILE Serif» | Source Serif 4 `de2e1a9a…` |

Each is the SIL Open Font License 1.1 text shipped with the family (the gate-0 folder for the first three, `google/fonts`
`ofl/readexpro/OFL.txt` for Readex Pro), LF line ends. The header of `static/css/v5/fonts.css` points to them.

## 4. How the faces load

- `font-display: swap` on every face; `unicode-range` as the council set it, so the Arabic file never loads on a Latin page
  and the Latin files never draw Arabic. A face downloads only when text needs it.
- **Preloads** (`templates/base.html`, plan §1.1 «Loading»; PFR §0): a Latin page preloads Host Grotesk and the wordmark
  (2); an Arabic page Readex Pro, Host Grotesk for the Latin runs and the digits, and the wordmark (3). The preload hrefs are
  the files the bundle's `url()` names, so under the manifest storage they are one request. The standalone error page
  (`templates/errors/standalone.html`) preloads the same three.
- **«ILE Mono» has one seat** — references, hashes, rule versions (the class list in §2). The legacy footer labels, the
  questionnaire's count, journey and timeline dates keep tabular figures in the sans (`static/css/v5/base.css`).
- **Metric-matched fallbacks** (`size-adjust` / `ascent-override` / `descent-override`, line gap 0), the typography lane's
  method (`P/research/type/tools/fallback_metrics.py`, 626 characters of product copy; W1-A's
  `evidence/v54/w1-a/tools/fallback_extra.py`; the Arabic value recomputed by lane T on the lane's Arabic sample of 212
  characters with the same method — size-adjust = the mean advance in the web face ÷ the same in Segoe UI; ascent and descent
  = Readex Pro's typo metrics 1.000 / 0.250 em ÷ size-adjust):

| Face | Fallback | size-adjust | ascent | descent | Platform |
|---|---|---|---|---|---|
| Host Grotesk | ILE Sans Fallback = Segoe UI | 105.5 % | 96.2 % | 29.9 % | Windows |
| Host Grotesk | ILE Sans Fallback Arial = Arial | 104.5 % | 97.1 % | 30.1 % | Windows, and macOS / iOS (same Arial metrics) |
| Host Grotesk | ILE Sans Fallback Android = Roboto | 105.1 % | 96.6 % | 30.0 % | Android (computed from the file, not verified on a device) |
| Readex Pro | ILE Arabic Fallback = Segoe UI | 107.1 % | 93.3 % | 23.3 % | Windows (Vazirmatn's were 97.1 / 105.6 / 55.3) |
| ILE Wordmark | ILE Wordmark Fallback = Georgia | 103.4 % | 71.1 % | 25.6 % | Windows, macOS |
| ILE Mono | ILE Mono Fallback = Consolas | 109.1 % | 93.9 % | 25.2 % | Windows |

  Not computed, because the fonts are not on this machine: Apple's own system faces (SF, Helvetica, Geeza Pro) — before the
  integration milestone (plan §7) — and the Android Arabic face (Noto Naskh / Noto Sans Arabic).
- **Swap CLS** (the gate: ≤ 0.01 with the matched fallbacks, DL54-04; V5.24 asks < 0.05). Method: every woff2 held for 1.5 s,
  the layout shifts of the swap summed (`evidence/v54/w1-a/tools/cls_swap.py`), Windows fallbacks. W1-A, lane 3, 5 October
  2026: **0.0000 – 0.0009** on the home (1440, 390), the login, the dashboard, the documents (1440, 390), the Arabic home
  (390) and the Arabic dashboard; with the overrides stripped, up to 0.0200 — the fallbacks are load-bearing. **Typography
  V2, the compressed twin 8782 on the lane's tree, 5 November 2026** (`evidence/v524/t/cls-swap/cls_swap.json`): the figures
  are recorded in `docs/design-v5/QA/v524/t/NOTES.md` §7 — every cell under 0.01 with the matched fallbacks.

## 5. What a page downloads (font bytes, encoded, measured on the lane server 8785, 1440 × 900, 5 November 2026)

| Page | Before V2 (W1-A, 5 Oct) | Typography V2 | Ceiling (TYPOGRAPHY_V2 §4.7) |
|---|---|---|---|
| a Latin public page (login, contact, Le projet, glossary, forum, institutions, fraudes) | 20 956 B | 20 956 B (Host Grotesk + the wordmark) | ≤ 22 000 |
| a Latin public page that still draws a label in the mono (home, parcours, FAQ, AGAMI, entreprises) | 23 644 – 30 916 B | 23 644 – 30 916 B (+ the mono files) — the lanes' burn-down (F-3); 20 956 once the label role lands | ≤ 22 000 (recorded at 30 916 in `tests/frontend/test_browser.py` until then, never up) |
| a Latin console page (dashboard, case file, documents, the company's space and need form) | 23 644 B | 20 956 B | ≤ 24 000 |
| an Arabic public page | 53 184 B | 37 084 B (Readex Pro + Host Grotesk + the wordmark) | ≤ 38 000 |
| an Arabic public page with a mono label (home, FAQ: both files; parcours, AGAMI, entreprises: the core) | 55 872 – 63 144 B | 39 772 – 47 044 B — the lanes' burn-down; 37 084 once the label role lands | ≤ 38 000 (recorded at 47 044 in `tests/i18n/test_rtl_browser.py` until then) |
| an Arabic console page | 55 872 B | 37 084 B | ≤ 40 000 |

The shipped set: **61 140 B ≤ 62 000**; per file: the variable sans ≤ 22 000, the italic ≤ 15 000, the Arabic ≤ 18 000, the
two mono files ≤ 10 000 together, the wordmark ≤ 2 000 (`tests/frontend/test_fonts_budget_v2.py`). Every ceiling is under
the previous system's figures and is never raised (V5.20; CLOSING ratchets each to its measure). Unthrottled lane figures,
from the sizes the browser fetched (`evidence/v524/t/probe/fonts.json`); the performance PASS is measured on 8782 by the
Performance Lead, never here.

## 6. What holds this file

- `tests/frontend/test_fonts_budget_v2.py::test_the_font_budget_is_route_aware_never_one_sum` — §1 bis: the shared set's
  and the serif's ceilings stand apart, no figure of this file adds them, and the home's route ceiling is the Latin page's
  plus the serif's file; `::test_the_home_serif_is_the_seventh_file_licensed_home_only_never_preloaded` — the serif's one
  consuming rule, under `.page-home`, in the sources and in the built bundles.

- `tests/frontend/test_v5_tokens.py::test_fonts_v5_md_records_every_shipped_face_with_its_bytes_and_hash` — every woff2
  in `static/fonts/` is in the table of §1 with its size and SHA-256, and each licence text with the opening of its hash
  (§3): a face rebuilt, added or removed without this file turns the suite red.
- `tests/frontend/test_fonts_budget_v2.py` — the set and each file under its ceiling; Readex Pro in Vazirmatn's place with
  its licence; the subset holds the Arabic and never the Latin or the digits; this file states the ceilings and the
  recomputed Arabic fallback.
- `tests/frontend/test_v5_tokens.py::test_the_five_faces_are_self_hosted_with_their_licences` and
  `::test_the_matched_fallbacks_cover_windows_apple_through_arial_and_android` — the six files, `font-display: swap`, the
  `unicode-range`s, the four OFL texts, IBM's Reserved Font Name, the fallback faces `local()` only.
- `tests/frontend/test_layout.py::test_fonts_css_references_only_local_files_that_exist` — the stylesheet's six `url()`s
  and the licences it points to; `::test_html_lang_and_dir_attributes` — the preloads per script (2 Latin, 3 Arabic).
- `tests/frontend/test_design_docs.py::test_listed_font_files_exist_and_every_font_file_is_listed` — DESIGN_SYSTEM_2026
  §6.2 lists the same files.
- In a browser: `tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded` (Host Grotesk and the wordmark
  loaded on a Latin page, no Arabic face, no request to another host, the bytes within the recorded figure),
  `tests/i18n/test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded` (Readex Pro then Host Grotesk on an
  Arabic page, the body at 17/28, the V4 faces and Vazirmatn gone, the bytes within the recorded figure) and
  `tests/frontend/test_typography_v2.py` (the Arabic guards: nothing under 14 px, the leadings, no Arabic in the mono).
