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

---

## 9. V5.12 — placements made (W2, lane C; DECISIONS §6)

The rows of §2 that entered the site through the slot registry `apps/pages/imagery.py` (files and provenance in
`static/img/v5/<family>/`, built by `tools/build_derivatives.py`; register rows in `docs/IMAGE_LICENSES.md` §3.1). Each
frame passed the §6 check at full resolution in the build's crop; what the check changed is recorded here.

| Slot | Frame | Placement | §6 check — outcome |
|---|---|---|---|
| `home.pilot.cedar` + `home.pilot.marble` | 30563520 · 6713855 | home «Projet pilote», the diptych «le même geste», B/W → colour as the band enters (static colour under reduced motion) | no lettering in the carving; the faces stay out of both 4:5 crops; the marble block is not a recognisable work |
| `home.ecosystem` | 33543226 | home «Un écosystème institutionnel», beside the promoter | the lanyard badge and strap redacted; the handwriting on the papers blurred; no face in the frame |
| `pathways.hero` | 7594198 | `/parcours/` entrance, LCP (4:5; 3:2 on a phone) | nothing legible on the desk, no logo on the laptop |
| `companies.hero` | 7180823 | `/entreprises/` entrance, LCP (3:2) | the crop stops under the chin (O55); the caliper's mark and scale blurred; red −15 % saturation. **3:2 only**: the gesture is horizontal, a 4:5 cut lost the hand or the piece |
| `institutions.hero` | 6949366 | `/institutions/` entrance, LCP (4:5; 3:2 on a phone) | the name cards are blank; the screens are off; no emblem |
| `universities.hero` | 9489906 | `/universites-et-formation/` entrance, LCP (4:5; 3:2 on a phone) | **re-cropped to the reading room's end bay**: the two readers (identifiable at 1600 px) and the spiral stair (O54) are outside the crop |
| `universities.exchange` | 31367507 | `/universites-et-formation/`, beside «Pour aller plus loin» | **every face is outside the crop** (three identifiable students in the full frame, O55): the exchange is told by the hands, a book and a folder; the book covers and the folder's lines blurred |

Not placed in W2: the portico's four dedicated frames, `/orientation/`, `/formation/`, `/diplomes-et-titres/`,
`/projet-pilote/`, `/le-projet/`, `/reseau/`, `/vivre-en-italie/` (wave W3). `/forum/` and `/agami/` stay without stock
(owner Q4, Q5).

## 10. V5.15 — placements made (W3, lane C; label v515-c-build)

The imagery pass of V5.15 §5: each important public page that had no frame gets one, in one slot. Files and provenance in
`static/img/v5/<family>/`; register rows in `docs/IMAGE_LICENSES.md` §3.3. Each frame passed the §6 check at full
resolution in its build crop.

| Slot | Frame | Placement | §6 check — outcome |
|---|---|---|---|
| `training.hero` | 5265332 | `/formation/` frontispiece, LCP (3:2) | the one face of the full frame (in profile) is above the crop; the jacket's brand mark blurred; the helmets' decals out of the crop. 3:2 only |
| `training.after` | 15290006 | `/formation/`, under «Second temps»; B/W → colour as it enters | nobody in the frame; no lettering |
| `diplomas.hero` | 4792286 | `/diplomes-et-titres/` frontispiece, LCP | nothing legible on the papers (the guide to documents, never the console) |
| `pilot.plain` + `pilot.fields` | 11010756 + 36909829 | `/projet-pilote/` frontispiece: the diptych «two territories», the plain (LCP) and the fields a step lower | no person, no sign; the alts name no place (stock is never documentary) |
| `project.hall` | 10323211 | `/le-projet/` frontispiece (night), LCP | the readers are small, seen from a gallery; the near readers of the frame's foot are below the crop |
| `network.table` | 34632581 | `/reseau/` frontispiece (night), LCP | straight from above: tops of heads, no face |
| `living.street` | 12900263 | `/vivre-en-italie/` band under the head, 21:9 (3:2 on a phone), LCP | the cars, their plates and the cyclist are below the crop; the house number blurred; the alt names no city |
| `contact.square` | 14581980 | `/contact/` frontispiece, LCP | five passers-by from behind, small; the square, not a doorway, is the subject (O54) |
| `companies.territory` | 5906831 | `/entreprises/`, a 21:9 band between «Trois temps» and the form | no person; the alt names no place |
| `institutions.chamber` | 32266781 | `/institutions/`, beside the recipients' statement; B/W at rest, colour under the pointer or the focus | the flags and arms are above the crop; the printed sheet on the desk blurred |

Not placed, on purpose: `/forum/` (Q4) and `/agami/` (Q5) keep no stock; FAQ, glossary, fraud and the legal pages stay
type-led (their heads carry a drawn motif instead). The mega menu keeps the four dedicated portico frames (§3.2 of the
register): lane A's redesign may draw them; none of them appears on a page.

## 11. V5.22 — frames and re-crops prepared for the V2 compositions (lane M; labels v522-m-build, v522-m-improve1)

SECTION_SYSTEM_V2 §8: seven new frames and four re-crops, each in ONE slot of `apps/pages/imagery.py` (files and
provenance in `static/img/v5/<family>/`, register rows in `docs/IMAGE_LICENSES.md` §3.4). Lane M prepares them; the
compositions that draw them belong to lanes H, P1 and P2, so a new slot appears on its page when that page is
recomposed, and a re-crop that a V2 composition needs is a named **variant** of its slot (`{% photo "<key>" "<class>"
variant="<name>" %}`): today's pages keep drawing the default rendering until their lane adopts the variant. Every frame
passed the §6 check at full resolution in its build crops; what the check found is held by the crops themselves
(`tests/compliance/test_imagery_v512.py::test_v522_the_full_resolution_check_holds_in_the_crops`). Per SECTION_SYSTEM_V2
§8, no photographer's name is copied here: the credit is in `PROVENANCE.json` and in the caption.

**Erratum (V5.24 §2, lane v524-px, 5 Nov 2026).** No credit is shown anywhere any more: `components/photo.html` draws no
`<figcaption>` and no attribute replaces it, so «the credit shown» / «credit visible» in the rows below describe the
V5.22 state, not the product. The author stays in the family's `PROVENANCE.json` only (`IMAGE_LICENSES.md` §3.5); the
licence check (`test_every_slot_is_licensed_and_its_author_recorded`) still reads licence, author and page per slot; the
production-facing guard is `tests/compliance/test_imagery_credits_v524.py`. A curated plate (`cms.MediaAsset`) keeps
its caption and draws a byline only when its licence demands it (`attribution_required`; §1.10 of the licences).

| Slot | Frame | Placement (lane) · ratios · `sizes` | Treatment | §6 check — outcome |
|---|---|---|---|---|
| `home.integrity.stone` | Pexels 11499083 | home S5 + S6, the K integrity band's ground (H) · 21:9 from 64 rem, 4:5 below · `100vw` | desaturated −35 % in the file; decorative (alt `""`), the credit shown | dressed courses in raking light, frontal; no opening, arch, step, door or window anywhere in the frame (O54); no mark or lettering; nobody. The faces' grain is softened (it weighed 2.5× the 21:9 ceiling): the courses, joints and light carry the ground under its 60 % veil |
| `project.volumes` | Pexels 29976379 | Le projet, D panorama after «il racconto» (P2) · 21:9 / 16:9 (48–64 rem) / 4:5 · `(min-width: 48rem) 112vw, 100vw` (M22 scales the drifting image 1.12) | colour, cool grade | the spines' title labels end at y 0.35 of the frame: every crop starts at 0.37, so no title is in any crop and nothing is redacted; nobody; not the Universités reading room (another scale, another subject) |
| `pathways.family.work` | Pexels 29454379 | Parcours PA-1, lane «Travail» (P1) · 3:2 at the lane head, 21:9 strip below · `(min-width: 64rem) 21vw, (min-width: 48rem) calc(100vw - 5rem), (min-width: 26.875rem) calc(100vw - 3rem), calc(100vw - 2.5rem)` | «select» | an empty aisle between pallet racks; the cartons' labels are a few pixels high at 720 and 1 200 w; no person |
| `pathways.family.study` | Pexels 6334273 (round 1) | Parcours PA-1, lane «Études et formation» (P1) · as above | «select» | at desk level, not from above: a hand writes in a ruled notebook with a white pen, an open book behind it; warm (brown tweed, pink shirt, pale wood: mean saturation 49–54, so «select» visibly changes it); the face is above the frame (both crops start under the collar, y ≥ 0.14); the books carry nothing legible; the handwritten figures and words beyond the pen are softened by ONE box where the page already falls out of focus (no seam); the pen's line and the drawn arrows stay sharp. Replaces 6549915 (a second overhead tabletop beside «Famille», nearly neutral, with a redaction seam) |
| `pathways.family.family` | Pexels 27177298 (round 1) | Parcours PA-1, lane «Famille» (P1) · as above | «select» | a shared table from straight above on an openwork wooden top: bowls of olives, tomatoes, a dip and peanuts; one hand holds out a spoon, the other holds the olive bowl; no face (the arms enter from the edges), no lettering, no brand; the glasses and a third hand at the top edge (y < 0.13) and the bread board at the right (x > 0.82) are outside both crops. Replaces 3184192 (the generic brunch table) |
| `pathways.family.other` | Pexels 9250930 | Parcours PA-1, lane «Autres voies» (P1) · as above | «select» | netted vine rows in mist under trees and hills; no person; a car and a mast in the haze are a few pixels; the alt names no place (stock is never documentary); not the Entreprises greenhouses at dusk |
| `training.before` | Pexels 34526423 | Formation F1 «la traversata», station 1 (P1) · 4:5 from 64 rem, 3:2 below · `(min-width: 90rem) 25rem, (min-width: 64rem) 28vw, (min-width: 48rem) 34rem, (min-width: 26.875rem) calc(100vw - 3rem), calc(100vw - 2.5rem)` | «develop» | hands wiring the control relays of an electrical training bench, between blue wire ducts and red leads; the face (x 0.17–0.27) is outside both crops, which start at x 0.30 (O55); a breaker's maker's logo and label, a miniature breaker's markings, the relays' model codes and terminal numbers and a CE label are erased by a median filter — the shapes stay crisp, so nothing reads as a blurred patch (a Gaussian blur did, in focus); the supply panel's lettering and the louvred window stay outside the crops; not the welding head nor the companies' calliper. Chosen over 34938452 (the same subject on a workbench), whose Pexels author is a company account: the caption would have printed a commercial brand under the frame |
| `home.pilot.cedar` | Pexels 30563520 | home S4, D panorama «lo stesso gesto» (H) · variant `pannello`: 2:3 full-height panel from 64 rem, 3:2 band below · `(min-width: 64rem) 34vw, 100vw` | «develop» | re-crop: the 2:3 holds the chisel hand, the ringed hand and the carving; the 3:2 stops before the shirt's pocket; no face. The default 4:5 (today's diptych) is unchanged |
| `home.pilot.marble` | Pexels 6713855 | as above (H) · variant `pannello` | «develop» | re-crop: the 2:3 panel from x 0.31 (round 1, QA M2) trims the thumb, never the blade — the blade's outer corner sits at 0.814 of the panel, so under S4's ~30 % × 82 vh cover the blade on the stone stays ≥ 6.8 % inside the drawn edge at 1024 × 768, ≥ 14 % at 1280 × 800 and 1440 × 900, 17.7 % at 1920 × 1080 (`evidence/v522/m/imp1_pilot_panels_cover_sim.json`); the whole frame as the 3:2 band; no face; the block is not a recognisable work |
| `home.ecosystem` | Pexels 33543226 | home S7, A «la campata» under the arch (H) · variant `campata`: 4:3 from 64 rem, 3:2 below · `(min-width: 80rem) 57vw, (min-width: 64rem) 50vw, 100vw` | colour | re-crop 4:3: the red wall at the start edge leaves; the lanyard and handwriting redactions stay; no face |
| `universities.exchange` | Pexels 31367507 | Universités U1, the filiera's destination (P1; drawn today on 6/12) · 3:2 · `(min-width: 100rem) 41.75rem, (min-width: 90rem) 38rem, (min-width: 75rem) 33.5rem, (min-width: 64rem) calc(50vw - 3.25rem), (min-width: 48rem) calc(100vw - 5rem), (min-width: 26.875rem) calc(100vw - 3rem), calc(100vw - 2.5rem)` (6/12 of the page container at each container step, the container's width below, its margin 24 px from 430 px and 20 px under). Round 1 corrects the value this row stated, and the real page's browser test made it exact: 45vw was right only near 1 040 px (8 px short at 1 199), 3 rem 8 px short under 430 px, 42 rem 4 px over at the 1 440 container; measured in headed Chromium at 12 widths, fr and ar, |drawn − sizes| ≤ 0.4 px (`evidence/v522/m/imp1_univ_sizes_steps.json`) | colour | re-crop: from x 0.58 (the book's edge is at 0.555) and y 0.44 (the lowest chin at 0.40) — the gesture and the folio case only; the three redactions of V5.12 are gone with what they covered (the covers read as censored objects at 768) |

**Ceilings** (SECTION_SYSTEM_V2 §7.3; every AVIF width a rendering can serve): body 45 KB; band and panorama 60 KB at
1 920 w; the 2:3 pilot panel 60 KB at 1 600 w; the family frame 30 KB (its 3:2 tops at 720 w, its 21:9 strip at 1 200 w);
the K ground 60 KB at 21:9 and 40 KB at 4:5 (800 w). The WebP fallback, for a browser without AVIF, is held to the
**same** ceiling (round 1: no allowance; §7.3 records none) and is not built at a width it cannot fit at q 40
(`webp_not_built`), so that browser takes the next width down; the ground's and the panorama's phone 4:5 gain a 640 w
step so that their fallback keeps two widths. **The board** `/__design-v5/specimens/imagery/` draws every frame
through the product's `{% photo %}` at its V2 width (development only: a test fixture reachable by URL, not linked
from the preview's index).

**Contract for the composing lanes.** A slot's `sizes` is the width its V2 composition draws per the Director's anatomy
(§2); a composition that draws another width states it with `{% photo … sizes="…" %}` (the tag's own argument, so
`imagery.py` need not change). The home pilot and the ecosystem adopt their variants; once they do, their default crops
(the pilot's 4:5) are no longer drawn and can be retired by a later imagery pass.
