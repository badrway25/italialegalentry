# ASSET USAGE MATRIX — final (V5)

**Italy Legal Entry™ · Executive Creative Director · 27 September 2026 · status PROPOSED — revised after the red team (`RED_TEAM.md` B2, M2, M13, M17) — nothing curated, nothing wired.** Built on `council/IMAGERY.md` §6 (draft matrix), §3 (slot shortlists), §4 (video), §5 (treatment), §7 (budget), with the ECD reconciliations of `CREATIVE_DIRECTION_V5.md` §5. Fonts from `council/TYPOGRAPHY.md` §9; icons from `council/ICON_SEMANTIC_MAP.md` §4 and §8; brand assets from `docs/design-v2/BRAND_ASSETS.md`.

**Binding rules.** (1) **One significant image = one primary context**; reuse only *inside* that context (e.g. the Persona image on the Persona door, the Persona mega-menu panel and the Persona landing — nowhere else). (2) Every asset is **self-hosted**; nothing is hot-linked (CSP and F24). (3) **Licence and author recorded** for every file in `docs/IMAGE_LICENSES.md` (photographs, videos), `docs/design-v2/FRONTEND_DEPENDENCIES.md` + the OFL texts in `static/fonts/` (fonts), `docs/design-v5/ICON_LICENSES.md` (Lucide ISC, new). (4) The editorial rules of `scripts/fetch_images.py` and `docs/IMAGE_LICENSES.md` hold: never borders, luggage, waiting lines, passports, airports, doorways («porte/soglie»), grids («griglie/cancelli»), tourist clichés, logos, readable third-party text, recognisable branded products — **and their prudent reading, which applies until the owner rules on the scope of F15 (O54): covered passages, arcades, steps and vaults are held out of every placement, and nothing below enters `CURATED` before that ruling is recorded in `IMAGE_LICENSES.md` §1** (B2). (5) **Stock is never documentary**: no stock image is captioned as the real Forum (Rovigo, 2 October 2026), a real institution's staff or a real partner, and no identifiable person is captioned **or placed** as an applicant, a beneficiary, a migrant or a Forum attendee (the Pexels License carries no model release): the Persona door shows nobody identifiable, and every other face waits for a legal reading, door by door (O55). **No alt text names a real building or place the picture does not need** (M13). (6) **Nothing below may enter `CURATED`** before the full-resolution check listed in §6.

---

## 1. Brand assets

| FILE | SOURCE | SECTION | PURPOSE | LICENSE | REUSE ALLOWED? |
|---|---|---|---|---|---|
| `static/brand/original/logo-mark.svg` | the owner's mark (recovered from the legacy site) | header lock-up (38 px), footer (white), rail tile (still), loader L1 at the entrance stage only (layered, 240 px, one cycle), favicon source | the brand: two planes, the arched door, the golden key, three steps | owner's rights | **Yes, verbatim** everywhere the brand appears; never redrawn, never recoloured, never mirrored; **its key turns once, on the entrance stage when the person submits (owner O1); the tricolour planes never move** (M10) |
| `static/brand/original/key.svg` | the owner's key | loader L2 (the key alone, `currentColor`, 14–24 px), `ile-key` glyph source | the act of opening | owner's rights | **Yes**, as the key; never a decorative sparkle, never a loop on `filter` |
| `static/brand/v2/doorway-arch-400.webp` (+ `doorway-*.avif/webp` 480/800/1200) | the owner's photograph inside the arch | **home hero** (LCP, preloaded, 42 KB) · **login stage** · error pages (static) | the door: the brand's threshold | owner's rights (`IMAGE_LICENSES.md` §7.1) | **Only as the door**; never cropped out of the arch; never a third use; V5 adds a key-centred navy vignette (0 bytes, owner D-U2); a 600 px AVIF arch strip only if DPR 3 phones show softness (+25–45 KB, measured first) |
| «ILE Wordmark» — `v5-wordmark-Newsreader-600-opsz20.woff2` (+ `…-opsz36.woff2` only if gate 0 asks) | Newsreader 600 (Production Type, OFL 1.1), instanced + subset to «ITALY LEGAL ENTRY™» — 11 code points | **every rendering of the trademark name**: the lock-up, the hero H1, the project page H1, the footer's legal line, the rail (M1) | the wordmark's font, delivered in 1.71 KB instead of 128.9 KB (the `opsz` 36 instance: 1.70 KB; measured in this revision) | SIL OFL 1.1 (no Reserved Font Name); the OFL text now in `council/typography/fonts/OFL-Newsreader.txt` | **Only** for the trademark name, in every place it appears |
| `static/img/favicon.svg` (redrawn) | `ile-arch` on navy, 32 px | browser tab; the rail tile in forced colours | recognisable tab icon (today three bars predating the mark's recovery) | owner's rights (derived from the mark) | favicon + forced-colours tile |
| `static/brand/v2/grain.svg` | V4 | night chapters (3 %) | material | project | night chapters only |

**Forbidden, whatever the surface:** the mark's English tagline and the caption under the door, in any language (F13/F14); the tricolour outside the mark — no exception (the council's notice filet is not adopted, O57); flags anywhere; the arch shape outside the door's allow-list (lock-up and favicon, hero, login, error pages, the journey's threshold B — M2).

---

## 2. Photographs — the V5 library (revised after the red team: statuses in the PURPOSE column)

LICENSE «Pexels» = the Pexels License (https://www.pexels.com/license/): free use and modification; the author is recorded anyway (`fetch_images.py` resolves it through the API); no sale of unaltered copies; **no implied endorsement** by the people or brands shown. All ids are Pexels photo ids; all authors as given by Pexels.

| FILE (slug) | SOURCE | SECTION | PURPOSE | LICENSE | REUSE ALLOWED? | Ratios (focus) · treatment | Weight target · loading |
|---|---|---|---|---|---|---|---|
| `voute-portique` | Pexels 17857002 · Jan van der Wolf | home hero, the layer behind the headline | the portico reduced to its geometry — **DROPPED** (M2, m15): arches behind the door, a new LCP candidate, decoration — kept here for traceability | Pexels | **No** (hero only) | 21:9 (top) · **duotone** notte-950 → carta-50 at 12–16 % · CSS gradient mask toward the door | ≤ 24 KB AVIF · **conditional**: ≥ 64 rem only and only if home LCP ≤ 2.2 s with it (it becomes the LCP element); preloaded with the door |
| `personne-carnet-lumiere` *(not used)* | Pexels 7594098 · Mikhail Nilov (alternative 7584771, same author — owner O23) | **Persona**: home door, mega-menu panel, landing hero | a person deciding his own path — **replaced** by `personne-fenetre-dos` (the same shoot, seen from behind): the front view is an identifiable man on the door that asks «Êtes-vous une personne ?» (M13) | Pexels | within **Persona** only | 3:2 (r) · 4:5 (r) · grade | door ≤ 45 KB @ 960 w · panel ≤ 28 KB @ 480 w (on first intent) · landing ≤ 60 KB (LCP, `fetchpriority=high`) |
| `personne-fenetre-dos` | Pexels 7594198 · Mikhail Nilov | **Persona**: home door, mega-menu panel, landing hero | a person deciding his own path — seen from behind at his desk by the window, nobody identifiable | Pexels | within **Persona** only | 3:2 (c) · 4:5 (c) · grade | door ≤ 45 KB @ 960 w · panel ≤ 28 KB @ 480 w (idle prefetch) · landing ≤ 60 KB (LCP, `fetchpriority=high`) |
| `atelier-mesure-precision` | Pexels 7180823 · Thirdman | **Impresa**: door, panel, landing | the skill a company needs | Pexels | within **Impresa** only | 3:2 (c) · 4:5 (c) · grade (red sweater −15 % sat.) | idem |
| `palazzo-ragione-loggia` *(withdrawn)* | Pexels 39768540 · Dmitry Romanoff | **Istituzione**: door, panel, landing | the civic institutions of the territory (itself a portico) — **WITHDRAWN** (M2, M13): an arcade, and a named Padua monument that a visitor can read as a partnership with that city | Pexels | within **Istituzione** only | 3:2 (r) · 4:5 (r) · grade · sky = text-safe | idem |
| `table-des-institutions` | Pexels 6949366 · Werner Pfennig | **Istituzione**: door, panel, landing (recommended, O60) | institutions deliberating: an empty council table, microphones, blank name cards — no building, no emblem | Pexels | within **Istituzione** only — **then `forum-table-panoramique` (6951299, the same room) leaves the Forum page** | 3:2 (c) · 4:5 (c) · grade | idem |
| `salle-deliberation` *(alternative)* | Pexels 32266781 · Héctor Berganza | Istituzione, if O60 keeps the Forum loop | an unnamed legislative chamber, a desk and a microphone in the foreground | Pexels | within **Istituzione** only | 3:2 (c) · 4:5 (c) · grade · **full-resolution check for flags, insignia and identifiability** | idem |
| `bibliotheque-salle-lecture` | Pexels 9489906 · Yaroslav Shuraev | **Università – Formazione**: door, panel, landing hero | study | Pexels | within **Università – Formazione** only | 3:2 (c) · 4:5 (c) · grade | idem |
| `etudiants-echange-campus` | Pexels 31367507 · Yusuf Çelik | Università – Formazione landing (body) | exchange between students | Pexels | **No** | 3:2 (c) · grade · **redact two book covers** | ≤ 38 KB, lazy |
| `arcades-casablanca-matin` *(rejected)* | Pexels 34453419 · Ayoub Galuia | **the diptych**, Morocco — head of the passage; regular-mobility page | a Moroccan portico — **REJECTED** (B2): the shop shutters close shop entrances — an entrance, on a prudent reading of F15 | Pexels | **only paired** with `arcades-padoue-pluie` | 4:5 (l) · grade · crop the end third (signage), redact pier stickers | ≤ 45 KB each, lazy |
| `arcades-padoue-pluie` | Pexels 38843185 · Konstantinos Kanavoura | **the diptych**, Italy | an Italian portico — **HELD for the F15 ruling (O54)**; if arcades are ruled outside F15, it needs a new Moroccan partner | Pexels | **only paired** with `arcades-casablanca-matin` | 4:5 (c) · grade · crop shop entrances (prudent F15) | idem |
| `main-cedre-ciseau` *(fallback diptych, Morocco)* | Pexels 30563520 · Moussa Idrissi | **the diptych «Lo stesso gesto»** — head of the passage; regular-mobility page | a hand guiding a chisel through a geometric cedar carving — the same gesture on both shores | Pexels | **only paired** with `main-marbre-ciseau` | 4:5 (c) · grade | ≤ 45 KB each, lazy |
| `main-marbre-ciseau` *(fallback diptych, Italy)* | Pexels 6713855 · Tima Miroshnichenko | idem | a hand guiding a chisel on marble — not geolocated, so no caption names a place | Pexels | **only paired** with `main-cedre-ciseau` | 4:5 (c) · grade | idem |
| *(diptych alternates)* | Pexels 30563521 · Moussa Idrissi (a zellige cutter's hands) · 12148970 · Serena Koi (a mosaicist in Soave, Veneto — black-and-white original) | idem | idem | Pexels | only as a pair (12148970 only in a monochrome pair) | 4:5 · **cropped so no face remains** | idem |
| `carnet-page-blanche` | Pexels 5357492 · Maria Mileta | orientation (public pathway page, questionnaire intro); console empty state «no case yet» | the first page of a path | Pexels | within **orientation** only | 21:9 (r) · 3:2 (c) · 4:5 (r) · grade · LTR text over the blank page (scrim ≥ .72), RTL glass plate | ≤ 60 KB band · empty state 240 px, lazy |
| `classeur-pieces-mains` | Pexels 4792285 · Anete Lusina | the public guide to documents («Les pièces») — **never inside the console** | assembling one's own documents | Pexels | **No** | 3:2 (c) · 21:9 (c) · grade · blur legible lines | ≤ 38 KB, lazy |
| `table-travail-institutions` | Pexels 33543226 · Emre Gokceoglu | cooperation (institutions page, ecosystem), network page, **home ecosystem bento tile** | institutions working together | Pexels | **cooperation + network + ecosystem tile** (one message) | 3:2 (c) · 21:9 (c) · grade · **redact the lanyard badge** and legible lines | tile ≤ 45 KB, lazy |
| `forum-prise-de-parole` | Pexels 16856088 · Domingos Henriques | **Forum landing hero** | a participant takes the floor | Pexels | within **Forum** only; **never captioned as the Rovigo Forum** | 4:5 (c) · 3:2 (c) · grade · **redact the printed programme and lanyard text** | ≤ 60 KB (LCP of the Forum page) |
| `marche-marbre-zellige` | Pexels 35816354 · Hassan Bouamoud | **Forum identity band**, Forum mega-menu panel, **home Forum teaser** | two crafts, one step: Veneto–Maroc — **HELD under the same owner flag as the terrazzo steps** (steps read as a threshold on a prudent reading, O54) | Pexels | within **Forum** only | 21:9 (c, diagonal) · 3:2 (c) · grade (sat. −15 only) · title on a plate; the caption never claims the marble's origin | band ≤ 60 KB, lazy |
| `table-mise-mains` *(fallback, Forum band)* | Pexels 6787057 · Artem Podrez | Forum identity band, Forum mega-menu panel, home Forum teaser — only if «la marche» is ruled out | the table is set: hands around blank notebooks on a white table, from above — faceless, weaker than «la marche» | Pexels | within **Forum** only | 21:9 (c) · 3:2 (c) · grade | band ≤ 60 KB, lazy |
| `plaine-peupliers-brume` | Pexels 10005316 · Serena Koi | territory band: Forum (lower band), «Le projet» | the plain of the territory | Pexels | within **territory** (same message on both pages) | 21:9 (b) · grade · duotone night variant · the alt names no place («une plaine») | ≤ 50 KB, lazy · **seen only as a 356 px tile: full-resolution check first** |
| `relecture-document-professionnel` | Pexels 9870135 · Ron Lach | Professionnels page | a professional reviews a file | Pexels | **No** | 3:2 (l) · 4:5 (c) · grade · blur legible lines | ≤ 45 KB |
| `laboratoire-formation-technique` | Pexels 9242821 · Mikhail Nilov | Formation / Academy public landing; default course cover until real covers exist | technical training (closes the «formazione tecnica» gap) | Pexels | within **Formation / Academy** | 3:2 (c) · 16:10 (c) · grade · check trainer-kit labels | ≤ 45 KB · covers ≤ 25 KB |
| `velo-facade-stuc` | Pexels 8551130 · Aneta Zelenková | «Vivre en Italie» | everyday life | Pexels | **No** | 3:2 (b) · 21:9 (b) · grade · crop the graffiti tag · the alt names no country (not geolocated) | ≤ 45 KB |
| `marches-terrazzo-laiton` *(optional)* | Pexels 17687058 · Sinitta Leunen | login side panel ≥ 80 rem — **only if the owner opts in (O24; ECD: no)** | entering: steps and gold | Pexels | **No** | 4:5 (c) · grade | ≤ 60 KB; it would become the login's LCP → preload or drop |

**Mega-menu thumbnails** are the door images above at 3:2 @ 480 w (≤ 28 KB AVIF), fetched on the first hover-intent or focus of the bar, `loading="lazy"` in a closed panel — 0 cost at load. **No photograph on operational screens** (dashboard, «Ma situation», dossier, documents, company, selection, Guichet, back-office); the only images there are the person's own document thumbnails and the «no case yet» empty state.

---

## 3. Video — three decorative loops

| FILE | SOURCE | SECTION | PURPOSE | LICENSE | REUSE ALLOWED? | Edit · encode | Playback |
|---|---|---|---|---|---|---|---|
| `portique-lumiere-boucle` (+ poster = frame 0) | Pexels video 36909064 · STUDIO FOLKUS | **«Le projet»** chapter band 21:9 (moved off the home by the ECD) | the portico in motion — **HELD with the arcades for O54** | Pexels | **No** | trim **before the wooden door** that enters the last seconds (~4.0 s) · ping-pong 0–4 s · 1280 × 548, 24 fps, H.264 CRF ≈ 28 (+ AV1) · graded in the encode · `-an` | ≤ 0.9 MB; `preload="none"`; plays only ≥ 64 rem, ≥ 50 % in view, no reduced motion, no Save-Data, not 2g/3g, after `requestIdleCallback` post-load; pauses off-screen / hidden tab; visible 44 px Pause toggle (2.2.2), choice remembered per viewer in `localStorage` (try/catch) |
| `forum-table-panoramique` (+ poster) | Pexels video 6951299 · Werner Pfennig | **Forum page** band, above the programme | the table is set — **only if Istituzione does not take 6949366, from the same room (O60)** | Pexels | **No** | check the **whole pan for flags** (the same shoot has EU/US/Norwegian flags on 6951392) · ping-pong of 6 s | ≤ 0.6 MB · same contract |
| `atelier-plan-boucle` (+ poster) | Pexels video 7479048 · cottonbro studio | **Formation / Academy** public landing band | work at the bench | Pexels | **No** | **crop the wall lettering** · cross-fade loop 0.6 s on a 6 s segment · lower 21:9 band | ≤ 1.0 MB · same contract |

Never: a video in a hero, a video on the home, welding / grinding / plasma footage (flashes, WCAG 2.3.1), audio. CSP: `media-src` falls back to `default-src 'self'` — no change. Whether `ffmpeg` is installed on the build machine was not checked.

---

## 4. Fonts (pairing A — owner O9)

| FILE | SOURCE | USED BY | PURPOSE | LICENSE | Weight · loading |
|---|---|---|---|---|---|
| `v5-HostGrotesk-var-400-700.woff2` | `google/fonts` `ofl/hostgrotesk` (pinned commit) | every page | interface, body, the console | SIL OFL 1.1 | 18.8 KB · **preloaded everywhere** |
| `v5-HostGrotesk-400-italic.woff2` | idem | `<em>` in prose | italic | OFL | 13.8 KB · on use |
| `v5-SourceSerif4-400-opsz48-nosc.woff2` | `ofl/sourceserif4` | public pages | display, titles | OFL | 25.3 KB · preloaded on public templates |
| `v5-SourceSerif4-400-italic-static.woff2` | idem | the hero lead, the Forum quote | the reading voice | OFL | 19.1 KB · on use (gate §22.1) |
| `v5-IBMPlexMono-400.woff2` (or the fontsource file, to respect the «Plex» RFN) | `@fontsource/ibm-plex-mono` 5.3.0 | references, hashes | data | OFL (RFN «Plex»: rename if self-subset) | 8.8 KB · on use |
| `v5-wordmark-Newsreader-600-opsz20.woff2` | `ofl/newsreader` | every rendering of the trademark name (lock-up, hero H1, project H1, footer legal line, rail) | the wordmark | OFL | 1.71 KB (11 code points, measured) · every page; the `opsz` 36 instance (1.70 KB) only if gate 0 asks |
| `v5-Vazirmatn-var-400-700-arabic.woff2` | `ofl/vazirmatn` | `/ar/` | Arabic interface | OFL | 31.5 KB · preloaded on `/ar/` |
| `v5-MarkaziText-400-arabic.woff2` | `ofl/markazitext` | `/ar/` public | Arabic display | OFL | 20.8 KB · on `/ar/` public |

Retired: the 26 current files (965 KB on disk): Newsreader variable roman and italic, IBM Plex Sans (8), IBM Plex Sans Arabic (9), Noto Naskh Arabic (3), the Plex Mono latin-ext split. Per page: home 73.7 KB (today 356.1) · console 29.3 KB (≈ 214) · Arabic home 81.6 KB (≈ 509). The OFL texts travel with the files (name IDs 0, 1–6, 13, 14 kept).

---

## 5. Icons

| FILE | SOURCE | USED BY | PURPOSE | LICENSE | REUSE |
|---|---|---|---|---|---|
| `static/img/icons.svg` (built from `static/icons/src/*.svg`) | 31 ILE drawings kept (redrawn only by the CSS terminals) + 4 identity glyphs (`ile-arch`, `ile-key`, `ile-steps`, `ile-mark`) + 8 new status marks «i cerchi» (+ `lock` reused) + `arrow-start` (ILE-new) + ≈ 65 Lucide geometries under the ILE treatment | everywhere, through `{% svg_icon %}` and the registry `apps/core/icons.py` | one concept, one glyph | ILE originals: project · Lucide: **ISC** (Feather-derived glyphs MIT); recorded in `docs/design-v5/ICON_LICENSES.md`; no runtime attribution required | ≈ 109 symbols, ≈ 9 KB gz (measured at build), one cached request; the ≈ 12 console shell symbols also inlined server-side (first paint) |
| `components/doorway.html` inline SVG, `_pilot.html` route | ILE | hero, login, passage | the door stage, the route | project | as today |
| `pages/home/partials/_route_glyph.html` («landforms») | ILE (V2) | — | **retired** (unreadable at 20 px on navy) | project | kept in history |

---

## 6. Checks before any photograph or video enters `CURATED`

| Asset | What to check or do at full resolution |
|---|---|
| 31367507 `etudiants-echange-campus` | redact two legible book covers |
| 33543226 `table-travail-institutions` | redact the lanyard badge (mark and name) and any legible paper line |
| 16856088 `forum-prise-de-parole` | redact the printed programme and lanyard text |
| 34453419 `arcades-casablanca-matin` | **rejected** (shutters) — no check needed |
| 8551130 `velo-facade-stuc` | crop or redact the graffiti tag |
| 38843185 `arcades-padoue-pluie` | crop the shop entrances under the arcade (prudent F15) |
| 7180823 `atelier-mesure-precision` | the caliper maker's mark |
| 9242821 `laboratoire-formation-technique` | labels on the trainer kit |
| 7594098 / 7584771 (Persona) | any mark on the book or the laptop lid |
| 9870135, 4792285 | legible document lines → blur |
| 10005316 `plaine-peupliers-brume` | the whole frame (judged only on a 356 px tile) |
| video 36909064 | trim before the door (~4.0 s) |
| video 6951299 | the whole pan for flags |
| video 7479048 | crop the wall lettering |
| 7594198 `personne-fenetre-dos` | the desk objects, the laptop lid and the screen: no logo, no readable text |
| 6949366 `table-des-institutions` | the name cards are blank; the screens are off or show nothing legible; no emblem |
| 32266781 `salle-deliberation` | flags, coats of arms, insignia; whether the chamber is recognisable |
| 30563520 `main-cedre-ciseau` | any lettering in the carving; the face stays out of the 4:5 crop |
| 6713855 `main-marbre-ciseau` | the sculpted head is not a recognisable artwork or a religious figure |
| 30563521 · 12148970 (alternates) | the crop removes every face; the Soave frame's passers-by leave the crop |
| 6787057 `table-mise-mains` | the notebooks are blank; no logo on the cards or sleeves |
| **all fallback candidates** | were seen only as ≈ 350 px Pexels previews in the red-team revision (`scratch/ecd/revision/sheet_*.jpg`); every check above is at full resolution |
| every slug and alt | the `FORBIDDEN_SUBJECT_KEYWORDS` substring test and the file-name ban (veneto, rovigo, regione, comune, logo) — 0 hits on the drafts |

---

## 7. The current library — what happens to each of the 15 photographs

| Slug (Unsplash, author unknown today) | V5 | Why |
|---|---|---|
| `micro-conference` | **retired** from placements | V5 has no photographic fallback; a news item without its cover is a text row (ECD) |
| `atelier-de-travail` | **conditional**: the pilot / «Le projet» page only, if its author can be recorded | one subject (co-design workshop); licence debt |
| `campus-universitaire` | **reserve**, unplaced | — |
| `reunion-cooperation` | retired | generic meeting; its role as the fallback of every page row breaks one-image-one-context |
| `entretien-accompagnement` | retired | replaced by Persona |
| `equipe-entreprise` | retired | three redactions; replaced by Impresa |
| `dialogue-institutionnel` | retired | replaced by Istituzione; its AGAMI use becomes a partner-supplied photograph after gate G6, or none |
| `etudiants-bibliotheque` | retired | two redactions; replaced |
| `public-conference` | retired | replaced by the Forum voice |
| `salle-de-formation` | retired | crop + two redactions; replaced |
| `orientation-ecran` | retired | replaced by `carnet-page-blanche` |
| `demarches-ecriture` | retired | its message belongs to Documentation |
| `espace-de-travail` | retired | three marks removed; the reserved area is operational (0 photos) |
| `collaboration-bureau` | retired | a high-five: a cliché the CD excludes |
| `bibliotheque-savoir` | retired | a second library |

The files stay compliant in the repository history; they are *retired*, not *rejected*. Code follow-ups: remove the generic `hero` fallback (`apps/pages/services.py:371`); stop the AGAMI page borrowing `entrance_institution` (`services.py:882`); point the network page to the cooperation slot (`services.py:906`).

---

## 8. Image budget per page

| Page | Above the fold | Below the fold (lazy) | Video | Count |
|---|---|---|---|---|
| Home | door 42 KB (LCP, unchanged) — no layer (the vault is dropped) | 4 doors ≤ 45 KB each @ 960 w · diptych 2 × ≤ 45 · Forum teaser 21:9 ≤ 60 · ecosystem tile ≤ 45 → **≈ 375 KB desktop / ≈ 250 KB mobile** (480–640 w) · news covers only if news exists | none | door + 8 (owner O20) |
| Audience landing | 4:5 hero @ 960 w ≤ 60 KB (LCP) | 1 content image ≤ 38 | — | 1 + 1 |
| Forum | 4:5 voice ≤ 60 (LCP) | «la marche» (or its fallback) band ≤ 60 · plain ≤ 50 · video poster ≤ 50 (only if O60 keeps the loop) | ≤ 0.6 MB, desktop, only if O60 keeps it | 3–4 |
| Formation / Academy (public) | 3:2 ≤ 45 | video poster ≤ 60 · covers ≤ 25 each | ≤ 1.0 MB, desktop | 1 + covers |
| «Le projet» | — | plain band ≤ 50 · portico poster ≤ 60 (only if O54 allows the arcade loop) | ≤ 0.9 MB, desktop, only if O54 allows it | 1–2 |
| Login | the door (LCP) | — (the terrazzo accent only if O24) | — | 1 |
| Console, dossier, documents, company, back-office | 0 | 0 (except «no case yet»: 240 px, lazy) | — | 0 |

Formats: AVIF q ≈ 50 + WebP q ≈ 72 at 480 / 800 / 1200 / 1600 (+ 1920 for 21:9) + a JPEG 800 fallback; ≤ 90 KB at 1200 for 3:2 and 4:5, ≤ 120 KB at 1600 for 21:9; explicit `width`/`height` + `aspect-ratio` (CLS 0); `loading="lazy"` + `decoding="async"` below the fold; `fetchpriority="high"` only on the one LCP image of a page; the placeholder class (`.img-ph--night` / `.img-ph--paper`) from the manifest's average colour — no LQIP, no inline style. Pillow's built-in AVIF needs ≥ 11.3 in the repository's venv (not inspected).

**Records to update when curated — after the owner's F15 ruling is written into `docs/IMAGE_LICENSES.md` §1 (O54), never before:** `scripts/fetch_images.py` (`CURATED` with crop and redaction boxes measured at full resolution; new fields `treatment`, `focus`, `ratios`; `REJECTED` with the reasons of `IMAGERY` §9); `static/img/photos/manifest.json` (author resolved through the Pexels API); `docs/IMAGE_LICENSES.md` §3 rows, §4 rejected rows, §5 gaps closed («formazione tecnica»: 9242821; «Italia contemporanea»: 38843185, 39768540; «collaborazione Italia–Marocco»: the diptych and «la marche»); a sibling `scripts/fetch_videos.py` for the three loops.
