# IMAGERY V5 — «due portici»

Council of the V5 escalation · role **Image Art Director** · 27 September 2026 · status **PROPOSAL, nothing curated, nothing wired** (the repository was read only; no file under `C:/tmp/italylegalentry` was touched).

| What | Where |
|---|---|
| The one Pexels tool of this role (key read from the environment, only ever sent as a header; saves every response; prints compact tables only, ≤ 40 lines; enforces 20 photo / 4 video queries, `per_page` 15, 3 previews per slot) | `C:/tmp/ile_v5_council/scratch/pexels/ile_pexels.py` |
| Saved photo searches (46 from the earlier run + 7 from this run, prefix `v5_`) | `scratch/pexels/search/*.json` |
| Saved video searches (7 earlier + 2 this run) | `scratch/pexels/videos/*.json` |
| Query budget of this run, with the query strings | `scratch/pexels/budget.json` — **photo 7/20, video 2/4** |
| Previews looked at, per slot (3 each, 16 slots) | `scratch/pexels/previews_log.json` → files in `scratch/pexels/medium/<id>.jpg` |
| Contact sheets (one per search) and loop-check frames (first / middle / last) | `scratch/pexels/sheets/*.jpg`, `sheets/frames_<video id>.jpg` |
| Sources read | `scripts/fetch_images.py` (docstring, `CURATED`, `REJECTED`, forbidden vocabulary), `static/img/photos/manifest.json`, `docs/IMAGE_LICENSES.md`, `docs/design-v4/CREATIVE_DIRECTION.md` §5, `docs/design-v2/BRAND_ASSETS.md` §2, `config/settings/base.py` (CSP), `apps/pages/services.py`, `apps/ecosystem/services.py`, council `COLOUR.md`, `MOTION.md`, `CAPTURES_AND_REFERENCES.md` |

Scores use six criteria, 1–5 each: **P** premium feel · **C** credibility · **R** cultural respect · **K** composition and crop latitude · **H** harmony with notte / carta / laguna · **T** text-safe area. Σ is out of 30. All scores were given by one reviewer from the Pexels "medium" preview (≈ 350 px high) or, where stated, from a 356 px contact-sheet tile only. They are an art director's ranking, not a measurement.

---

## 0. In ten lines

1. **Direction: «due portici».** The portico of V4 («il portico e la console») becomes the photographic spine. The Italy–Morocco relationship is shown through what both shores **share**: arcades, stone, craft, the working table. It is never shown as travel, borders or tourist icons. The signature pair is a diptych: an arcade in Padua and an arcade in Casablanca, graded as if taken by the same photographer.
2. **The hero stays the door.** The photograph inside the arch is the owner's own, a brand-locked asset (`BRAND_ASSETS.md` §2: the door «non può perdere … la fotografia dentro l'arco»). It remains the LCP element (`doorway-arch-400.webp`, 42 KB). V5 adds one **duotone vault layer** behind the headline (≤ 24 KB, to be measured). There is **no video in the hero**.
3. **17 new photographs (+ 1 optional login accent) + 3 video loops.** Each has **one primary context**. 12 of the 15 current Unsplash photos leave V5 placements: their authors are unknown, 4 needed redactions, and 6 of them say the same thing ("people at a table with laptops").
4. **Every audience gets its own image and its own micro-visual.** The micro-visual is the actor glyph in a glass disc plus the audience's route colour as a 3 px rule. Persona, Impresa, Istituzione and Università–Formazione never share a picture.
5. **One grade for everything in colour** (CD §5.3). **Duotone only on three non-human layers**: vault, plain, and the portico poster on night. **People are never duotoned**: a monochrome face on an immigration-adjacent platform reads as a file photo.
6. **The arch mask stays exclusive to the door and the login** (CD §5.4). I do not follow the captures' suggestion of arch windows on audience cards (`CAPTURES_AND_REFERENCES.md` §3.3.1). Repeating the mark's shape on every card would spend the brand's strongest asset. Cards get a passe-partout on paper instead.
7. **Three videos, all below the fold**: the home «portico» chapter, the Forum, and Formation/Academy. They use `preload="none"`, their first frame as poster, desktop only, a poster only under reduced motion and Save-Data, and a visible pause toggle (WCAG 2.2.2). **No welding or grinding footage**: arcs and sparks flash (WCAG 2.3.1).
8. **Budget:** LCP is untouched (the door). Above the fold ≤ 70 KB of images. Below the fold ≤ 400 KB desktop and ≤ 250 KB mobile, all lazy. Each video ≤ 0.9 MB, desktop only, after idle. This raises CD §5.6's «porta + 5» on the home to «porta + 8», a deviation to sign (§7).
9. **Nothing is ready for `CURATED`.** Each candidate was judged on a ≈ 350 px preview. Project policy (`IMAGE_LICENSES.md` §1.4) requires a full-resolution check for text, logos and doors before inclusion. The checks are listed in §5.8 (14 rows covering 16 assets).
10. **Honesty on the process.** The earlier attempt of this role made 46 photo and 7 video searches and downloaded 1,394 previews. That is far over the caps now set, and it died after printing raw responses. This run reused those saved files offline and made **7 photo + 2 video queries**. See §10 for every other limit.

---

## 1. What the owner sees today — the diagnosis

| Finding | Evidence |
|---|---|
| **No author is known for any photo.** All 15 are Unsplash, recorded as «Unsplash contributor (author lookup unavailable offline)». | `manifest.json`, `IMAGE_LICENSES.md` §1.3 |
| **One vocabulary, six times.** `reunion-cooperation`, `entretien-accompagnement`, `equipe-entreprise`, `dialogue-institutionnel`, `collaboration-bureau` and `orientation-ecran` are all people with laptops and notebooks at a table. Nothing distinguishes a company from an institution from a person. | manifest slots / alt texts |
| **Four photos survive only through redaction** (`equipe-entreprise`, `etudiants-bibliotheque`, `salle-de-formation`, `espace-de-travail`: blurred screens, brands, a cap, a sweatshirt, a sticker). A premium library does not start from blurred stock. | `fetch_images.py` `CURATED` |
| **A cliché**: `collaboration-bureau` is a high-five. The CD's own list (§5.1 «Rifiutare») excludes posed celebratory gestures. | alt text |
| **Neither Italy nor Morocco appears once.** The gap recorded on 17/09 («Italia contemporanea / collaborazione Italia–Marocco / integrazione») is still open, and so is «formazione tecnica». | `IMAGE_LICENSES.md` §5 |
| **Two library photos** (`etudiants-bibliotheque`, `bibliotheque-savoir`) carry the same message. | manifest |
| **One image, two contexts, today.** `entrance_institution` is the Institutions space hero (`apps/ecosystem/services.py` `SPACES`) **and** the AGAMI page (`apps/pages/services.py:882`). `forum_event` illustrates the network page (`services.py:906`). `hero` is the fallback for every CMS page row without an image (`services.py:371`), so any row can inherit the same meeting photo. | code |
| **The mega-menu has no imagery and the inner pages are text only.** | `CAPTURES_AND_REFERENCES.md` §2 |

---

## 2. The direction — «due portici»

1. **Architecture carries identity; people carry credibility.** Architecture (vaults, loggias, arcades, steps) does the brand work: the portico, the steps, the threshold of the key. People appear where the message is *someone doing something*: planning, measuring, learning, taking the floor, reviewing a file.
2. **One significant image = one primary context.** Reuse is allowed only *inside* that context. For example, the Impresa image appears on the Impresa card on the home, in the Impresa mega-menu panel and on the Impresa landing. It never appears on any other message (§6, column «reuse allowed?»).
3. **Italy and Morocco meet through what they share.** Two arcades, one Padua and one Casablanca. A marble step with a zellige riser: two crafts, one step. Three things are excluded:
   - tourist icons: Colosseum, gondolas, the Galleria in Milan;
   - religious monuments: the Hassan II Mosque and the Mausoleum of Mohammed V dominate every Moroccan search;
   - costume, souks, desert.
   The headscarf is never used as a signifier of "Moroccan". Where it appears, it is incidental inside a mixed group.
4. **People work, listen, speak and learn.** They never pose, never smile at the camera, never shake hands, never stand under flags. Faces stay in natural colour (no duotone, no heavy tint).
5. **Premium means restraint:** one grade, generous crops, few images per page, and **no text on busy pixels**. On cards the text sits beneath the image. On bands it sits inside a measured text-safe zone or on a glass plate (§5.4).
6. **Stock never passes as documentary.** No stock image is captioned as the real Forum (Rovigo, 2 October 2026), a real institution's staff or a real partner. The Forum imagery is written to be replaced by commissioned photographs of the event with releases, as `IMAGE_LICENSES.md` §5 already foresees.

---

## 3. Slot plan — shortlist of three per slot, ranked

Page URLs are `https://www.pexels.com` + the path shown. Pixel sizes are the originals. Every primary is ≥ 2,400 px on its long side (CD §5.1).

### 3.1 Hero layer (home, behind the headline — it will be an LCP candidate, see §7)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 17857002 | Jan van der Wolf | /photo/arched-ceiling-of-walkway-17857002/ | 6000×4000 | 5 4 5 5 4 5 | **28** | **PRIMARY.** Groin vaults of a portico seen from below, with iron tie-rods. No ground, no person, no door, no text. It is the portico reduced to its geometry. As a notte duotone at 12–16 % it reads as a watermark of the brand's architecture. |
| 2 | 18359738 | Jan van der Wolf | /photo/double-barrel-ceiling-of-arcade-18359738/ | 5602×3735 | 4 4 5 4 4 4 | 25 | Alternate. Same author and light, more arches, busier. |
| 3 | 15138264 | Vitali Adutskevich | /photo/passage-in-diminishing-perspective-15138264/ | 6000×4000 | 4 4 5 4 3 3 | 23 | Ochre arcade in perspective. A long vanishing passage invites the «soglia» reading (F15, prudential), and the orange is strong. |

Rejected here: 12366635 (a colonnade framed by a dark arch: literally a doorway view, F15) and 31864645 (Bologna by night: shop signs, postcard mood).

### 3.2 Persona (audience card, mega-menu panel, landing hero 4:5)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 7594098 | Mikhail Nilov | /photo/man-in-white-long-sleeves-wearing-eyeglasses-7594098/ | 6000×4000 | 5 4 5 4 4 4 | **26** | **PRIMARY.** A man at a window, pen raised, thinking, with an open book and notebook. The warm side light is natural, not posed, and not looking at the camera. The message is a person deciding his own path. His origin is ambiguous and international, not a stereotype. The wood panel and white wall give a text-safe start side. |
| 2 | 7584771 | Mikhail Nilov | /photo/a-woman-writing-in-notebook-looking-the-laptop-7584771/ | 6000×4000 | 4 4 5 4 4 3 | 24 | Alternate. A woman planning with a notebook at a window over a city. Gender balance works either way (§3.19). The laptop lid must be checked for a logo at full resolution. |
| 3 | 37790424 | Keyla Brito | /photo/focused-student-writing-in-moody-classroom-light-37790424/ | 6000×4000 | 5 3 5 4 4 4 | 25 | Cinematic blue haze that suits notte, but the look is a strong grade (CD §5.1: «filtri») and the classroom says "student", which is Università's message. |

### 3.3 Impresa

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 7180823 | Thirdman | /photo/man-using-a-caliper-to-measure-an-item-in-a-workshop-7180823/ | 6720×4480 | 4 5 5 4 3 3 | **24** | **PRIMARY.** A young craftsman in a green apron measures a part with a caliper, shot from a low angle. The message is precision and skill, the thing a company is hiring. The red sweater needs the −15 % saturation of the grade. The caliper's maker's mark must be checked. |
| 2 | 5711700 | Anna Shvets | /photo/pensive-mature-man-examining-machine-in-workshop-5711700/ | 6240×4160 | 4 4 5 3 4 4 | 24 | Premium and dark, but the extraction hose dominates the start side and the sector (a wood planer) is not among the companies' real needs (metallurgy, logistics, construction). |
| 3 | 29393030 | Claudio Meloni | /photo/industrial-worker-operating-heavy-machinery-in-workshop-29393030/ | 5885×3923 | 3 5 5 3 4 2 | 22 | Credible lathe work, but a logo on the jacket (redaction) and hi-vis stripes fight the palette. |

### 3.4 Istituzione

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 39768540 | Dmitry Romanoff | /photo/palazzo-della-ragione-in-padua-italy-39768540/ | 6192×4128 | 5 5 5 4 4 5 | **28** | **PRIMARY.** The brick tower and upper loggia of the Palazzo della Ragione in Padua: a civic building of the Veneto that is not a tourist icon. It is itself a portico, so the image carries the V5 thread. The sky gives a text-safe area. It needs no redaction. It shows no seal and implies no endorsement by any living institution. |
| 2 | 19867355 | Markus Winkler | /photo/a-large-empty-room-with-a-large-round-table-19867355/ | 4000×2666 | 4 4 5 4 3 3 | 23 | A modern, anonymous assembly hall with a golden rose window. Correct but cold. |
| 3 | 6949366 | Werner Pfennig | /photo/monitors-and-microphone-on-wooden-table-top-6949366/ | 6720×4480 | 4 4 5 4 4 4 | 25 | A table set with microphones and blank name cards. It comes from the same shoot as the Forum video (§4.2), so it is held in **reserve** to avoid showing the same room twice. |

### 3.5 Università – Formazione (audience)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 9489906 | Yaroslav Shuraev | /photo/women-studying-in-a-library-9489906/ | 6000×4000 | 4 4 5 4 4 3 | **24** | **PRIMARY** (card and landing hero 4:5). Two students read in a wood-panelled reading room with a spiral stair. It is academic without the graduation-cap cliché. The green carpet sits close to laguna after grading. |
| 2 | 31367507 | Yusuf Çelik | /photo/diverse-students-discussion-outdoors-31367507/ | 6720×4480 | 4 5 5 4 4 3 | 25 | **Second image of the same landing** (same context): three students discussing on a campus. Two book covers are legible («Eğitim Felsefesi», «… Higher Education») and must be **redacted**. |
| 3 | 6549627 | Tima Miroshnichenko | /photo/college-students-researching-at-the-library-6549627/ | 6000×4000 | 3 4 5 3 3 3 | 21 | Seen on the contact sheet only; flat light. |

Rejected: 39769780 (Palazzo del Bo, the University of Padua: the inscription «… MAGNA» and a door in frame).

### 3.6 Formation / Academy (section image; its video is §4.3)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 9242821 | Mikhail Nilov | /photo/man-and-woman-inside-a-factory-9242821/ | 4000×2667 | 4 5 5 4 5 3 | **26** | **PRIMARY.** Two young apprentices in aprons and safety glasses at a technical training bench. This finally covers the **«formazione tecnica»** gap of `IMAGE_LICENSES.md` §5, with gender balance. The teal wall is the best palette match of the whole shortlist. Labels on the trainer kit must be checked. |
| 2 | 3846255 | Andrea Piacquadio | /photo/master-showing-apprentice-how-handling-detail-3846255/ | 7680×5120 | 4 5 5 4 3 4 | 25 | A master shows an apprentice: intergenerational transmission, documentary. Held for a future «métiers» page. |
| 3 | 11679118 | Willquezada | /photo/closeup-of-hands-composing-an-electronic-equipment-11679118/ | 6000×4000 | — | — | **REJECTED**: «Lab-Volt» and «Dell» are legible (F15 §1.5). |

### 3.7 Orientation / parcours

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 5357492 | Maria Mileta | /photo/a-person-holding-a-pen-on-the-blank-page-of-the-notebook-5357492/ | 3783×2509 | 4 4 5 5 5 5 | **28** | **PRIMARY.** From above, a hand about to write on the blank page of a notebook, beside a cup of coffee, on dark wood. The message is "the page before your path". The dark wood is notte and the page is carta. The blank page is the text-safe zone, and there is no text anywhere. |
| 2 | 5190599 | cottonbro studio | /photo/person-holding-a-brown-pen-5190599/ | 3500×2333 | 4 4 5 4 5 3 | 25 | Kraft notebooks on a navy card: a lovely palette, but «WEEKLY PLANNER» is legible (redaction). |
| 3 | 8845108 | Yaroslav Shuraev | /photo/person-in-pink-shirt-writing-on-white-notebook-8845108/ | 6720×4480 | 3 4 5 3 2 3 | 20 | The pink shirt is off palette. |

### 3.8 Documentation («Mes pièces», public guide to documents)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 4792285 | Anete Lusina | /photo/person-choosing-document-in-folder-4792285/ | 5487×3663 | 4 5 5 4 5 3 | **26** | **PRIMARY.** Hands searching a pale-teal accordion file. The message is assembling one's own pieces, which is what the platform asks for. The folder is laguna-50 after grading. The papers must be checked for legible lines. |
| 2 | 6077886 | KATRIN BOLOVTSOVA | /photo/a-close-up-shot-of-a-person-going-through-documents-6077886/ | 5472×3648 | 4 4 5 4 5 4 | 26 | A clipped paper stack on a navy desk, shallow focus. Equal score, but it says "bureaucracy" rather than "my file". Alternate. |
| 3 | 8371705 | cottonbro studio | /photo/cardboard-box-full-of-file-folders-8371705/ | 6386×4257 | 4 3 5 4 4 3 | 23 | **REJECTED for compliance.** Rolled documents tied with ribbon read as diplomas, which suggests recognition of qualifications. The platform recognises nothing (CR-11). |

### 3.9 Cooperation / institutions (and the network page, which says the same thing)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 33543226 | Emre Gokceoglu | /photo/business-meeting-discussion-panel-in-ankara-33543226/ | 7728×5152 | 4 5 5 4 4 3 | **25** | **PRIMARY.** Hands, microphones and working papers at a panel table, with faces out of frame: institutions at work, without implying who they are. **Redact** the lanyard badge (red mark and name) and any legible paper line. It is a different shoot from the Forum video. |
| 2 | 6949980 | Werner Pfennig | /photo/people-sitting-in-a-conference-room-6949980/ | 6627×4418 | 3 4 5 4 4 4 | 24 | Four panellists, formal. Same room as §4.2. |
| 3 | 6949366 | Werner Pfennig | (see 3.4) | 6720×4480 | 4 4 5 4 4 4 | 25 | Same room as §4.2; reserve. |

A seventh query (`v5_coop`) produced only form-signing stock and one US flag (8847041). It was not retained.

### 3.10 Forum Vénétie–Maroc — the voice

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 16856088 | Domingos Henriques | /photo/a-man-from-the-audience-speaking-to-the-microphone-16856088/ | 6132×3947 | 4 5 5 4 4 3 | **25** | **PRIMARY.** A participant takes the floor from the audience. A forum is people speaking, not a stage. The subject is dignified, lit well and not posing. **Redact** the printed programme (bottom start) and lanyard text. **The caption must never say or imply that he attended the Rovigo Forum** (§2.6). |
| 2 | 36900082 | Earth Photart | /photo/empty-modern-auditorium-in-milano-italy-36900082/ | 5712×4284 | 4 4 5 4 3 4 | 24 | An empty modern auditorium in Milan: an Italian venue, with curved rows. Small **flags on the stage** (CD §5.1 «bandiere») must be cropped out. Alternate if the page needs a venue. |
| 3 | 35335989 | This And No Internet 2 | /photo/diverse-audience-engaged-at-indoor-seminar-35335989/ | 9005×6003 | 3 4 5 3 3 2 | 20 | A seminar in a sports hall: casual, not premium. |

Rejected: the Pavel Danilyuk seminar series (`fo_audience`, `fo_v_audience`), where a hotel's name is legible on the wall and several attendees wear masks, which dates the images.

### 3.11 Forum — the signature detail («la marche»)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 35816354 | Hassan Bouamoud | /photo/close-up-of-marble-steps-with-mosaic-tiles-35816354/ | 5184×3456 | 5 5 5 5 4 4 | **28** | **PRIMARY — the most "ILE" image of the set.** Grey-veined marble steps whose risers carry a zellige frieze: two crafts, one step, raked light. It echoes the three steps of the mark. It says "Veneto–Maroc" without a flag, a monument or a costume. It is used as the Forum's 21:9 identity band and in the Forum mega-menu panel. Nothing in the image claims where the marble comes from, and the caption must not claim it either. |
| 2 | 37293880 | Huỳnh Như Mavi | /photo/sunlit-shadow-patterns-on-terrazzo-steps-37293880/ | 4799×3199 | 4 3 5 4 4 4 | 24 | Terrazzo steps with sunlit shadows. Seen on the contact sheet only. |
| 3 | 17687058 | Sinitta Leunen | /photo/marble-steps-and-steel-handrail-17687058/ | 6240×4160 | — | — | Assigned to the login (§3.17). It is not reused here. |

### 3.12 Professionnels (lawyers, advisors, patronati)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 9870135 | Ron Lach | /photo/unrecognizable-hand-of-woman-sitting-at-table-and-reviewing-docum… | 4980×3320 | 5 4 5 4 5 4 | **27** | **PRIMARY.** A professional in a white shirt reviews a document, pen in hand, in soft window light. She is anonymous, precise and calm. The oxblood folder is the only accent. The document lines must be blurred if legible at full resolution. |
| 2 | 6077872 | KATRIN BOLOVTSOVA | /photo/a-man-in-a-suit-reading-a-document-6077872/ | 5472×3648 | 4 4 5 4 5 3 | 25 | A man in a suit, face out of frame, pen on a document, on a navy desk. Alternate. |
| 3 | 7433827 | Vlada Karpovich | /photo/a-man-and-a-woman-looking-at-papers-7433827/ | 5828×3885 | 3 4 5 3 3 3 | 21 | Senior professionals at a table: reads as stock. |

Rejected: the whole `pro_desk` lawyer series. The Kaboompics and RDNE shoots are staged around divorce papers, with Lady Justice statuettes, handshakes and a US flag.

### 3.13 – 3.14 Mobility — the diptych «due portici» (Italy | Morocco)

Always shown **together**, in the same ratio (4:5 each on desktop, stacked on mobile), with the same grade. In RTL the pair keeps its order in reading direction; photographs are never mirrored.

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| **IT 1** | 38843185 | Konstantinos Kanavoura | /photo/wet-cobblestone-street-in-historic-padua-italy-38843185/ | 5367×4336 | 5 5 5 4 4 3 | **26** | **PRIMARY (Italy).** A wet cobblestone street under arcades in Padua: contemporary, lived in, no tourists, in the Veneto. Shop entrances sit in the arcade's shadow. Crop to the pier and the street (prudential F15). |
| IT 2 | 29575236 | Hub JACQU | /photo/charming-porticoed-street-in-bologna-italy-29575236/ | 4928×3264 | 4 4 5 4 4 3 | 24 | A Bologna porticoed street. The parked cars' plates must be redacted, and Bologna is not the Veneto. |
| IT 3 | 29575251 | Hub JACQU | /photo/historic-arcades-of-bologna-s-charming-piazza-29575251/ | 4781×3166 | 4 4 4 4 3 4 | 23 | A piazza with café umbrellas and a sign: leans touristic. |
| **MA 1** | 34453419 | Ayoub Galuia | /photo/atmospheric-covered-walkway-in-casablanca-34453419/ | 5963×3975 | 4 5 5 4 4 3 | **25** | **PRIMARY (Morocco).** A covered walkway with square piers and hanging lanterns in Casablanca: the modern portico of a working city. Crop off the end third, which has shop signage and a green sign. Redact stickers and graffiti on the piers. Shutters, not doors (prudential). |
| MA 2 | 34453420 | Ayoub Galuia | /photo/sunlit-street-view-in-casablanca-morocco-34453420/ | 5963×3975 | 4 5 5 4 3 3 | 24 | Low sun on a boulevard with Art Deco façades and small figures. Alternate; same photographer as MA 1, so the grade matches. |
| MA 3 | 33974521 | Earth Photart | /photo/modern-architecture-in-rabat-morocco-33974521/ | 3984×2656 | 3 5 5 3 2 4 | 22 | A Rabat tram, the Grand Théâtre and the Mohammed VI tower: contemporary Morocco, but landmark-heavy, with a saturated blue sky. |

Rejected for this slot: every Hassan II Mosque and Mausoleum frame in `ma_city`, `ma_rabat` and `v5_ma_arcade`. They are sacred places and tourist icons. An arch framing a street (30450186) reads as a door (F15).

### 3.15 Territory — the plain of Rovigo (21:9 band on the Forum page and «Le projet»)

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 10005316 | Serena Koi | /photo/green-grass-field-with-trees-10005316/ | 8256×5504 | 5 4 5 5 5 5 | **29** | **PRIMARY, pending a full-resolution check.** Poplars in fog on a flat field, with one tiny figure. It is the Po plain as people who live there know it: grey, horizontal, quiet, not a postcard. The sky is fully text-safe. It works in colour (already near-monochrome) or as a duotone. **Seen only as a 356 px contact-sheet tile**: this slot's three previews were spent on the rejected frames below. The location is not stated on Pexels, so the alt text says "une plaine", never "Polesine". |
| 2 | 30329183 | drB drB | /photo/serene-landscape-with-reflective-lake-and-trees-30329183/ | 5760×3840 | 4 3 5 4 3 4 | 23 | A flooded field with poplars; contact sheet only. |
| 3 | 37418055 | Maurizio Fecchio | /photo/misty-sunrise-over-river-sile-in-veneto-italy-37418055/ | 6000×4000 | 3 4 5 3 2 4 | 21 | The Sile river (Veneto) at sunrise. HDR processing with a pink cast (CD §5.1 «dominanti cromatiche forti»), usable only as a duotone. The two other frames by this author, 35794575 and 37207370, are rejected outright: lavender HDR. |

### 3.16 Vivre en Italie

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 8551130 | Aneta Zelenková | /photo/a-bicycle-parked-on-the-street-8551130/ | 5419×3613 | 4 3 5 5 5 5 | **27** | **PRIMARY with a caveat.** A black bicycle against a cream stucco façade under two windows: everyday life, carta palette, a whole wall of text-safe area. **Not geolocated in Italy** (probably Central Europe), so C = 3 and the alt text never names a country. Crop or redact the graffiti tag at the end side. |
| 2 | 31593601 | Kris Møklebust | /photo/silhouette-of-biker-in-foggy-park-31593601/ | 5333×4000 | 4 3 5 4 4 4 | 24 | A cyclist in fog, black and white; not geolocated. |
| 3 | 39221767 | cami | /photo/cyclist-on-sunlit-street-by-classical-building-39221767/ | 2560×1707 | — | — | **REJECTED**: recognisably Berlin; would contradict «Vivre en Italie». |

The current `demarches-ecriture` (a hand filling documents) leaves this slot: its message belongs to Documentation.

### 3.17 Login — the door, and an optional accent (owner decision)

CD §5.6: «login: la porta». The owner's door stays. On screens ≥ 80rem an optional 4:5 side panel may carry:

| # | id | photographer | page | px | P C R K H T | Σ | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 17687058 | Sinitta Leunen | /photo/marble-steps-and-steel-handrail-17687058/ | 6240×4160 | 5 4 5 4 4 3 | **25** | Terrazzo steps with brass fixings in warm light, echoing **the mark's three steps and the golden key**. **Owner decision:** a prudential reading of F15 could see steps as a «soglia». The brand itself has steps. |
| 2 | 37865370 | Kari Alfonso | /photo/symmetrical-architectural-staircase-design-37865370/ | 3374×2362 | 4 4 5 4 4 3 | 24 | A symmetrical stone stair, black and white. |
| 3 | — | (none) | — | — | — | — | Recommended default if the owner declines: the door alone, which is what V4 ships. |

### 3.18 Mega-menu thumbnails

Yes, because the captures show today's panels are empty. **One image per panel**, and it is the image of the panel's own context: Persona, Impresa, Istituzione and Università–Formazione use their audience images, and the Forum uses «la marche». This is reuse inside one context, which §2.2 allows. The image is 3:2 at 480 w AVIF (≤ 28 KB). It is fetched on first intent (pointer enters the bar, or focus enters the menu button) with `loading="lazy"` in a closed panel, so it costs nothing at page load.

### 3.19 Dashboard, platform accents, empty states

**No photographs on operational screens** (CD §5.6 and COLOUR.md §3: «no photograph on operational screens»). This covers the console dashboard, «Ma situation», the fascicolo, documents, the company workspace, selection, the Guichet numérique and back-office. Their premium feel comes from material (carta, night rail, glass), type and motion.

The only real images there are the user's own document thumbnails. Empty states use a glyph and one sentence.

One exception is proposed, and it keeps the one-image-one-context rule: the empty state «no case yet → start the orientation» may show the **orientation** image (§3.7) at 4:5, 240 px, lazy.

Gender and origin balance of the primaries:
- men alone: Persona, Impresa, Forum voice;
- women alone: Professionnels;
- two women: Università;
- mixed: Formation, cooperation (hands);
- no people: Istituzione and the architecture.

If the owner prefers a woman for Persona, 7584771 swaps in without changing anything else.

---

## 4. Video — three narrative moments, none in the hero

**Why not the hero.** The door's photograph is brand-locked and is the LCP element. A video there would either replace the owner's photograph, which is forbidden, or add a second moving picture behind it. That would add bytes on the LCP path under slow 4G and CPU ×4, and the motion would compete with the scroll-linked door drift that MOTION.md keeps. The hero's dynamism stays the V4 scroll-linked pair.

Source figures below are the Pexels renditions (sizes as served, from `vfiles`). **Target sizes are estimates for a re-encode that was not run** (no ffmpeg run in this phase).

### 4.1 V1 «portico» — home chapter band 21:9, below the fold

| # | id | author | page | length | source | smallest adequate rendition | loop | verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | 36909064 | STUDIO FOLKUS | /video/elegant-architectural-archways-with-soft-lighting-36909064/ | 7 s | 3840×2160, 60 fps | 1280×720 = 3.1 MB · 960×540 = 1.8 MB | **ping-pong** of 0–4.0 s | **PRIMARY.** A slow lateral dolly along a pale stone arcade with hanging lanterns in soft light. No person, no text. **A dark wooden door enters the frame in the last seconds** (checked on `frames_36909064.jpg`), so the clip is **trimmed before it** (F15). Target: 1280×548, 24 fps, H.264 CRF ≈ 28 ≈ 0.6–0.9 MB; AV1 ≈ 0.4–0.6 MB. |
| 2 | 36902357 | Mark Holmes | /video/medieval-cloister-arches-in-sunlight-36902357/ | 8 s | 3840×2160, 30 fps | 1280×720 = 3.2 MB | ping-pong | A gothic cloister in sun. Beautiful, but a monastic, religious space with no link to Italy or Morocco. Alternate. |
| 3 | 28158986 | HTJ Media Advertising | /video/the-pillars-of-the-memorial-are-lined-up-28158986/ | 11 s | 1920×1080 | 1280×720 | crossfade | The pillars of an unnamed memorial. The context is unknown, so it is not used. |

### 4.2 V2 «la table est mise» — Forum page, above the programme

| # | id | author | page | length | source | smallest adequate rendition | loop | verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | 6951299 | Werner Pfennig | /video/a-panning-shot-of-a-conference-room-6951299/ | 11 s | 3840×2160, 25 fps | **1280×720 = 1.3 MB** · 960×540 = 0.9 MB | ping-pong of 6 s | **PRIMARY.** A slow pan across an empty U-shaped conference table with microphones and blank name cards: the forum awaits. No faces and no text. **Verify the whole pan for flags**: the same shoot contains 6951392, with EU, US and Norwegian flags on the table. Target ≈ 0.4–0.6 MB. |
| 2 | 6951391 | Werner Pfennig | /video/a-conference-room-microphone-6951391/ | 15 s | 3840×2160 | 1280×720 = 0.9 MB | crossfade | A microphone close-up. Alternate. |
| 3 | 34917492 | Max Medyk | /video/engaged-audience-in-business-seminar-34917492/ | 11 s | 1920×1080, 60 fps | 1280×720 | crossfade | An audience with lanyards and people. It would overlap the Forum voice photo (§3.10). |

### 4.3 V3 «l'atelier» — Formation / Academy landing

| # | id | author | page | length | source | smallest adequate rendition | loop | verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | 7479048 | cottonbro studio | /video/man-drilling-a-wood-7479048/ | 33 s | 4096×2160, 25 fps | 1366×720 = 7.0 MB · 960×506 = 4.6 MB | **crossfade 0.6 s** on a 6 s segment | **PRIMARY.** A **locked-off camera** on a craftsman working at a large bench in a pale workshop. A static frame is the easiest kind of loop, and its warm grey sits between carta and notte. **Wall lettering at the top end** must be cropped away (the 21:9 band keeps the lower part). Target ≈ 0.7–1.0 MB. |
| 2 | 5895494 | Gustavo Fring | /video/two-wood-workers-talking-to-each-other-5895494/ | 16 s | 3840×2160, 30 fps | 1280×720 = 3.7 MB | hard (handheld drift) | Two woodworkers consult a notebook. Checked shirts; alternate. |
| 3 | 5895457 | Gustavo Fring | /video/men-doing-woodworks-5895457/ | 21 s | 3840×2160 | 1280×720 | crossfade | Same shoot; alternate. |

**Rejected video families:**
- **All welding, grinding and plasma footage** (`tr_v_weld`). Arcs and spark showers flash. WCAG 2.3.1 cannot be guaranteed on a looping autoplay, and the blue-white casts break the palette.
- Galleria Vittorio Emanuele and Galleria Umberto (`v5_v_portico`): tourist icons and luxury storefronts.
- Pottery, computer-skills-for-seniors and art-school clips (`tr_v_teach`): off message.
- Dancers and shadow studies (`hero_v_shadow`).
- Stock seminar clips with masks, lanyards and legible hotel names (`fo_v_audience`).

### 4.4 Playback contract (A: native `<video>` plus one small ES module, no React, no library)

1. **Markup:**

   ```html
   <video muted playsinline loop preload="none" poster="…-poster-1280.avif" aria-hidden="true" disablepictureinpicture>
   ```

   AV1 `<source>` comes first, H.264 second. **No `autoplay` attribute.** Explicit `width`/`height` and a CSS `aspect-ratio` on the band give CLS 0. The poster is **frame 0 of the encode** (not a separate photo), so the moment playback starts is invisible.
2. **Starting playback.** A module in `static/js/src/` (bundled by esbuild, CSP `script-src 'self'`) starts playback only when **all** of these hold:
   - the band is ≥ 50 % in view (IntersectionObserver);
   - `prefers-reduced-motion: no-preference`;
   - `navigator.connection?.saveData` is not true and the effective type is not 2g or 3g;
   - the viewport is ≥ 64rem;
   - `document.visibilityState` is `visible`;
   - `requestIdleCallback` has fired after `load`.

   It pauses when the band leaves the view or the tab hides. Decoding runs off the main thread, so no long task and no INP cost is expected. **This must be measured**, not assumed.
3. **Pause control (WCAG 2.2.2).** A visible Pause/Play toggle sits in the band's end-bottom corner: 44 px target, a `<button>` with `aria-pressed`, labels in fr, it, en and ar, focus ring per COLOUR.md (the two-tone ring on photographs). The viewer's choice is remembered per viewer in `localStorage` (wrapped in try/catch). Under reduced motion the toggle is not rendered, because nothing moves.
4. **Degradation.** On mobile, under Save-Data, reduced motion or no JS, the poster alone shows, and it is the same frame. `preload="none"` means none of these cases downloads a video byte.
5. **CSP.** `media-src` falls back to `default-src 'self'` (`config/settings/base.py`), so self-hosted MP4 and WebM need **no CSP change**.
6. **Accessibility.** The videos are decorative, with no speech and no audio track (`-an`). The band's heading and text carry the meaning, so no captions are needed.

---

## 5. Art-direction treatment

### 5.1 One grade for every photograph in colour (CD §5.3, unchanged numbers)

The pipeline is Pillow and deterministic: contrast **+8 %**, saturation **−15 %**, a soft S-curve, **blacks lifted toward notte-900 `#0b1a33`**, highlights **+4 % warm**, sharpen 0.5, and every metadata block stripped.

The videos get the same grade in the encode (ffmpeg `eq` + `curves`, approximated and checked side by side against the stills). Two images side by side must look like the work of one photographer. The diptych §3.13–3.14 is the test.

**V5 change:** the CD's 6 % `--accent` veil on paper is **not applied over faces**. A teal veil on skin reads as tint. It stays on architecture and objects only.

### 5.2 Duotone — only three non-human layers

The ramp maps luminance to a straight mix from **notte-950 `#071226`** (shadows) to **carta-50 `#f4f3f0`** (lights), gamma 1.1. It is applied only to:
- `voute-portique` (the hero layer, shown at 12–16 % over the notte mesh);
- the night variant of `plaine-peupliers-brume`;
- the poster of `portique-lumiere-boucle` when that band sits on a night chapter.

**Never on people** (§0.5), and never tinted laguna: the accent stays interactive-only (DS §1.3 «one interactive accent», COLOUR.md §0.10).

### 5.3 Crops, ratios and focal points

The four CD ratios are kept: **3:2** (cards, mega-menu, news), **4:5** (landing heroes, diptych, Forum voice), **21:9** (chapter bands), **16:10** (course covers).

The focal point is a `data-focus` value mapped to the nine `.img--focus-*` classes (CD §5.2; no inline style, CSP-safe). Each ratio is **its own derivative cut around the focus**, not a single master cropped by `object-fit`. That way a 4:5 is composed rather than squeezed.

**RTL:** photographs are **never mirrored**, because hands, handedness and lettering would lie. A text-safe zone is on one physical side of a picture. So in `ar`, a band whose text-safe zone is on the left places its text on a glass plate or in its own column (see `carnet-page-blanche`).

### 5.4 Text on photographs — measured, or not at all

- **Cards:** text sits **below** the image, never on it.
- **Bands and hero:** text sits only (a) inside the image's text-safe zone listed in §5.9, over a notte scrim of **≥ .72** in that zone, or (b) on a glass plate (`--glass-dark` .55, 13.92:1 measured in COLOUR.md).
- The V4 `--grad-photo-dark` at .45 **fails AA** for body text (reported by COLOUR.md §15). V5 does not rely on it for legibility.
- Every text-over-image pair is measured at implementation with the council's `scratch/colour/colourlib.py`, taking the worst pixel under the text box.

### 5.5 Masks, radii, frames

- **The arch shape only in the door**: home hero and login (CD §5.4). No arch windows on cards (disagreement with CAPTURES §3.3.1, explained in §0.6). No blobs and no organic masks.
- **Cards on paper:** radius `lg` 14 px plus a **passe-partout**, meaning the inner hairline `inset 0 0 0 1px rgba(21,34,42,.08)` of CD §5.3. On night: radius 14 with no hairline.
- **Chapter bands:** radius 0, bleeding to the chapter edge.
- **The hero layer** fades toward the door through a CSS `mask-image` linear gradient declared in the stylesheet, not an arch.

### 5.6 Micro-visual per audience

Each audience image carries two things at its bottom-start corner:
1. the **actor glyph** of that audience from the icon sprite: the same persona / impresa / istituzione / università glyph as the doorway legend and MOTION.md's journey, 20 px in a 36 px `--glass-dark` disc;
2. a **3 px rule in the audience's route colour** (DS §1.2, `--route-1..4-dark` on night, their paper counterparts on carta).

Together these give four recognisable, repeatable signatures that work in the mega-menu, the home cards and the landing heroes. They never rely on colour alone, because the glyph carries the meaning. The disc sits at logical `inset-inline-start`, so it moves to the right in RTL.

### 5.7 Motion of stills

This is unchanged from CD §5.5 and MOTION.md rows 2–3:
- hover `scale(1.02)` in 320 ms;
- a one-time reveal `clip-path: inset(0 0 12% 0) → inset(0)` below the fold only;
- parallax only on the door photo (18 px) and 21:9 bands (≤ 3 %, `scroll()`);
- **never on the LCP image**;
- reduced motion: everything still and visible.

### 5.8 Checks at full resolution before `CURATED` (policy §1.4)

| id | what to check or do |
|---|---|
| 31367507 | redact two book covers (legible titles) |
| 33543226 | redact the lanyard badge (mark and name) and any legible paper line |
| 16856088 | redact the printed programme and lanyard text |
| 34453419 | crop the end third (shop signage); redact pier stickers and graffiti |
| 8551130 | crop or redact the graffiti tag |
| 38843185 | crop shop entrances under the arcade (prudential F15) |
| 7180823 | caliper maker's mark |
| 9242821 | labels on the trainer kit |
| 7594098 / 7584771 | any mark on the book or laptop |
| 9870135, 4792285 | legible document lines → blur |
| 10005316 | the whole frame (seen only as a tile) |
| video 36909064 | trim before the door (~4.0 s) |
| video 6951299 | check the full pan for flags |
| video 7479048 | crop the wall lettering |

### 5.9 Treatment per asset

| slug | ratios (focus) | grade | duotone | overlay / text | mask | alt_fr (draft, ≤ 200 chars, vocabulary-checked) |
|---|---|---|---|---|---|---|
| `voute-portique` | 21:9 (t) | — | **yes**, 12–16 % over notte | headline over it; contrast measured on the worst pixel | CSS gradient mask toward the door | decorative: `alt=""`, `aria-hidden` |
| `personne-carnet-lumiere` | 3:2 (r), 4:5 (r) | yes | no | none on cards; landing text beside it | r14 + passe-partout | «Homme assis près d’une fenêtre, stylo en main, qui réfléchit devant un carnet et un livre ouverts» |
| `atelier-mesure-precision` | 3:2 (c), 4:5 (c) | yes | no | none | r14 + passe-partout | «Artisan qui mesure une pièce au pied à coulisse dans un atelier lumineux» |
| `palazzo-ragione-loggia` | 3:2 (r), 4:5 (r) | yes | no | text-safe sky at start (LTR) | r14 + passe-partout | «Tour de brique et loggia à arcades du Palazzo della Ragione, à Padoue, sous un ciel nuageux» |
| `bibliotheque-salle-lecture` | 3:2 (c), 4:5 (c) | yes | no | none | r14 + passe-partout | «Deux étudiantes lisent dans une salle de lecture boisée, près d’un escalier en colimaçon» |
| `etudiants-echange-campus` | 3:2 (c) | yes | no | none | r14 | «Trois étudiants discutent sur un campus, livres à la main» |
| `laboratoire-formation-technique` | 3:2 (c), 16:10 (c) | yes | no | none | r14 | «Deux apprentis en tablier et lunettes de protection travaillent sur un banc d’essai technique» |
| `carnet-page-blanche` | 21:9 (r), 3:2 (c), 4:5 (r) | yes | no | LTR: text over the blank page (scrim ≥ .72); RTL: glass plate | r0 band / r14 card | «Main qui s’apprête à écrire sur la page blanche d’un carnet, à côté d’une tasse de café» |
| `classeur-pieces-mains` | 3:2 (c), 21:9 (c) | yes | no | none / plate | r14 | «Mains qui cherchent un document dans un classeur à soufflets bleu clair» |
| `table-travail-institutions` | 3:2 (c), 21:9 (c) | yes | no | plate on band | r14 / r0 | «Participants assis à une table de travail, micros et documents devant eux, pendant une réunion» |
| `forum-prise-de-parole` | 4:5 (c), 3:2 (c) | yes | no | none; caption never documentary | r14 | «Participant qui prend la parole au micro depuis le public, lors d’une rencontre» |
| `marche-marbre-zellige` | 21:9 (c, diagonal), 3:2 (c) | yes (sat −15 only; the zellige colour is the point) | no | band title on a plate | r0 band / r14 menu | «Marches de marbre ornées d’une frise de zellige, dans une lumière rasante» |
| `relecture-document-professionnel` | 3:2 (l), 4:5 (c) | yes | no | none | r14 | «Personne en chemise blanche qui relit un document, stylo à la main, près d’une fenêtre» |
| `arcades-padoue-pluie` | 4:5 (c) | yes | no | none; the pair's caption below | r14 | «Rue pavée et mouillée, longée d’arcades, dans le centre historique de Padoue» |
| `arcades-casablanca-matin` | 4:5 (l) | yes | no | none | r14 | «Galerie couverte à piliers le long d’une rue de Casablanca, dans la lumière du matin» |
| `plaine-peupliers-brume` | 21:9 (b) | yes | night variant only | sky = text-safe top | r0 | «Peupliers alignés dans la brume sur une plaine agricole» |
| `velo-facade-stuc` | 3:2 (b), 21:9 (b) | yes | no | wall = text-safe | r14 / r0 | «Vélo appuyé contre une façade crème, sous deux fenêtres» |
| `marches-terrazzo-laiton` | 4:5 (c) | yes | no | none | r14 | «Marches en terrazzo et rampe aux fixations dorées, dans une lumière chaude» |
| `portique-lumiere-boucle` (video) | 21:9 1280×548 | yes (encode) | poster on night only | band title on a plate | r0 | decorative, `aria-hidden` |
| `forum-table-panoramique` (video) | 21:9 or 16:9 | yes (encode) | no | plate | r0 | decorative |
| `atelier-plan-boucle` (video) | 21:9 lower band | yes (encode) | no | plate | r0 | decorative |

All 21 slugs and all drafts above were checked by script against `FORBIDDEN_SUBJECT_KEYWORDS`: 0 hits. The check is a substring test, so «outdoor», «importance», «comportant», «aborder», «filet», «profile» and «delegate» would all fail it. The slugs were also checked against the file-name ban (veneto, rovigo, regione, comune, logo): 0 hits. «plaine-peupliers-brume» deliberately avoids «veneto».

---

## 6. ASSET USAGE MATRIX — draft

LICENSE «Pexels» = Pexels License (https://www.pexels.com/license/): free use, modification allowed, credit recorded anyway (`fetch_images.py` resolves the author through the API). Two conditions matter here: **no sale of unaltered copies**, and **no implied endorsement by the people or brands shown**.

| FILE (proposed slug) | SOURCE | SECTION | PURPOSE | LICENSE | REUSE ALLOWED? |
|---|---|---|---|---|---|
| `doorway-arch` (existing, `static/brand/v2/`) | owner's own photograph (fountain) | Home hero; Login | the door, the brand's threshold | owner's rights (BRAND_ASSETS §2; IMAGE_LICENSES §7.1) | **Yes, only as the door**; never cropped out of the arch |
| `voute-portique` | Pexels 17857002 · Jan van der Wolf | Home hero (layer) | the portico as texture of the brand | Pexels | **No** (hero only) |
| `personne-carnet-lumiere` | Pexels 7594098 · Mikhail Nilov | Persona: home card, mega-menu, landing | a person planning their own path | Pexels | Within **Persona** only |
| `atelier-mesure-precision` | Pexels 7180823 · Thirdman | Impresa: card, mega-menu, landing | the skill a company needs | Pexels | Within **Impresa** only |
| `palazzo-ragione-loggia` | Pexels 39768540 · Dmitry Romanoff | Istituzione: card, mega-menu, landing | the civic institutions of the territory | Pexels | Within **Istituzione** only |
| `bibliotheque-salle-lecture` | Pexels 9489906 · Yaroslav Shuraev | Università–Formazione: card, mega-menu, landing hero | study | Pexels | Within **Università–Formazione** only |
| `etudiants-echange-campus` | Pexels 31367507 · Yusuf Çelik | Università–Formazione landing (body) | exchange between students | Pexels | **No** |
| `laboratoire-formation-technique` | Pexels 9242821 · Mikhail Nilov | Formation / Academy landing; default course cover | technical training | Pexels | Within **Formation/Academy** (the default cover until per-course covers exist) |
| `carnet-page-blanche` | Pexels 5357492 · Maria Mileta | Orientation (public pathway page, wizard intro); console empty state «start the orientation» | the first page of a path | Pexels | Within **orientation** only |
| `classeur-pieces-mains` | Pexels 4792285 · Anete Lusina | Public guide to documents («Les pièces»), not inside the console | assembling one's own documents | Pexels | **No** |
| `table-travail-institutions` | Pexels 33543226 · Emre Gokceoglu | Cooperation (institutions page, ecosystem); network page | institutions working together | Pexels | **Cooperation + network** (same message); nowhere else |
| `forum-prise-de-parole` | Pexels 16856088 · Domingos Henriques | Forum page; home Forum teaser | a participant takes the floor | Pexels | Within **Forum** only; never captioned as documentary |
| `marche-marbre-zellige` | Pexels 35816354 · Hassan Bouamoud | Forum identity band; Forum mega-menu panel | two crafts, one step: Veneto–Maroc | Pexels | Within **Forum** only |
| `relecture-document-professionnel` | Pexels 9870135 · Ron Lach | Professionnels page | a professional reviews a file | Pexels | **No** |
| `arcades-padoue-pluie` | Pexels 38843185 · Konstantinos Kanavoura | Mobility diptych, Italy (regular-mobility pathway page) | an Italian portico | Pexels | **Only paired** with `arcades-casablanca-matin` |
| `arcades-casablanca-matin` | Pexels 34453419 · Ayoub Galuia | Mobility diptych, Morocco | a Moroccan portico | Pexels | **Only paired** with `arcades-padoue-pluie` |
| `plaine-peupliers-brume` | Pexels 10005316 · Serena Koi | Territory band: Forum (lower band), «Le projet» | the plain of the territory | Pexels | Within **territory** (the same message on both pages) |
| `velo-facade-stuc` | Pexels 8551130 · Aneta Zelenková | «Vivre en Italie» | everyday life | Pexels | **No** |
| `marches-terrazzo-laiton` (optional) | Pexels 17687058 · Sinitta Leunen | Login side panel ≥ 80rem | entering: steps and gold | Pexels | **No** (owner decision) |
| `portique-lumiere-boucle` (+ poster) | Pexels video 36909064 · STUDIO FOLKUS | Home chapter band «Il portico» | the portico in motion | Pexels | **No** |
| `forum-table-panoramique` (+ poster) | Pexels video 6951299 · Werner Pfennig | Forum page band | the table is set | Pexels | **No** |
| `atelier-plan-boucle` (+ poster) | Pexels video 7479048 · cottonbro studio | Formation / Academy band | work at the bench | Pexels | **No** |
| `micro-conference` (kept) | Unsplash 1475721027785-f74eccf877e2 | News | default image of a news item without its own | Unsplash License | Only as the **news fallback** |
| `atelier-de-travail` (kept) | Unsplash 1552664730-d307ca884978 | Projet pilote space; «Le projet» | co-design workshop | Unsplash License | Pilot / project (one subject) |
| `campus-universitaire` (kept in reserve) | Unsplash 1562774053-701939374585 | not placed | — | Unsplash License | — |

**Leaving V5 placements** (files stay compliant; they are *retired*, not *rejected*):

| slug | why it leaves |
|---|---|
| `reunion-cooperation` | generic meeting; its role as fallback for every page row (`services.py:371`) breaks one-image-one-context by design, so V5 has **no photographic fallback** |
| `entretien-accompagnement` | replaced by Persona |
| `equipe-entreprise` | three redactions; replaced by Impresa |
| `dialogue-institutionnel` | replaced by Istituzione; its second use on the AGAMI page should become a **partner-supplied photograph** after gate G6, or none |
| `etudiants-bibliotheque` | two redactions; replaced |
| `public-conference` | replaced by the Forum voice |
| `salle-de-formation` | crop plus two redactions; replaced |
| `orientation-ecran` | replaced |
| `demarches-ecriture` | its message belongs to Documentation |
| `espace-de-travail` | three marks removed; the reserved area is operational (0 photos) and the login is the door |
| `collaboration-bureau` | high-five cliché |
| `bibliotheque-savoir` | second library |

---

## 7. Budget and performance

| Page | Above the fold | Below the fold (lazy) | Video | Image count vs CD §5.6 |
|---|---|---|---|---|
| Home | door 42 KB (LCP, unchanged) + `voute-portique` ≤ 24 KB | 4 audience cards 3:2 @ 640 w ≤ 38 KB each + Forum teaser ≤ 38 + portico poster 21:9 ≤ 60 + 3 news ≤ 30 each ≈ **340 KB** desktop, ≈ 230 KB mobile (480 w) | V1 ≤ 0.9 MB, desktop only, after idle, in view | door + layer + 9 = **deviation** from «porta + 5» (owner/CD to sign) |
| Audience landing | 4:5 hero @ 960 w ≤ 60 KB (LCP, `fetchpriority="high"`) | 1 content image ≤ 38 KB | — | 1 + 1 = CD ✓ |
| Forum | 4:5 voice ≤ 60 KB (LCP) | marche band ≤ 60 + territory band ≤ 50 + V2 poster ≤ 50 | V2 ≤ 0.6 MB | 4 = CD ✓ (≤ 4) |
| Formation / Academy | section 3:2 ≤ 45 KB | V3 poster ≤ 60; course covers 16:10 ≤ 25 each | V3 ≤ 1.0 MB | 1 + covers = CD ✓ |
| Login | door (LCP) | optional accent 4:5 ≤ 60 KB ≥ 80rem | — | the accent would **become the LCP element** (larger than the door): preload it or drop it |
| Console, fascicolo, documents, B2B, back-office | 0 | 0 | — | CD ✓ |

- **The hero layer will become the LCP element.** Chrome counts CSS and `<img>` backgrounds, and a 1440 × 620 layer is larger than the 400 px door. It must therefore be tiny (≤ 24 KB AVIF, duotone compresses very well), preloaded with the door, and **measured on slow 4G + CPU ×4**. If home LCP exceeds 2.2 s, ship it only from 64rem up, or drop it. Today the home LCP is 1.44–1.67 s desktop (TYPOGRAPHY.md), so the margin is real but not large.
- **Formats:** AVIF (q ≈ 50) plus WebP (q ≈ 72) at 480 / 800 / 1200 / 1600, plus 1920 for 21:9 only, and a JPEG 800 fallback. Targets are ≤ 90 KB at 1200 for 3:2 and 4:5, ≤ 120 KB at 1600 for 21:9. This follows CD §5.2 (480/800/1200/1600, ≤ 120 KB at 1200) rather than the pipeline's current 480/960/1440/1920 WebP ≤ 350 KB.
- **No LQIP.** CLS comes from `width`/`height` plus `aspect-ratio`. The empty frame shows one of two placeholder classes (`.img-ph--night` / `.img-ph--paper`) chosen from the Pexels `avg_color` stored in the manifest. There are no inline styles.
- **Long tasks:** images decode async and videos decode off the main thread. No JS runs per image. The video module is ≈ 1 KB of logic and runs after idle.

---

## 8. What the implementation phase would do (not done here)

1. **`scripts/fetch_images.py`** already supports `source="pexels"`, and an API lookup gives the real author. Changes needed:
   - add the 18 candidates with crop and redaction boxes **measured at full resolution** (§5.8);
   - new optional fields: `treatment` (`grade` | `duotone`), `focus` (tl…br), `ratios` (list);
   - per-ratio derivatives cut around the focus;
   - AVIF output: check the Pillow version of the repo venv, since built-in AVIF needs Pillow ≥ 11.3. This session's system Python has 12.1; the venv was not inspected.
2. **Add to `REJECTED`**, with the reasons from §9.
3. **`docs/IMAGE_LICENSES.md`:**
   - §3 rows;
   - §5 gaps closed:
     - «formazione tecnica»: 9242821;
     - «Italia contemporanea»: 38843185 and 39768540;
     - «collaborazione Italia–Marocco»: the diptych and «la marche»;
   - §4 rejected rows.
4. **Video:** a sibling of `fetch_images.py` (for example `scripts/fetch_videos.py`) would:
   - resolve through `api.pexels.com/videos/videos/<id>` and download the 1920 rendition into the cache outside the repo;
   - use ffmpeg to trim, crop, grade and encode AV1 and H.264 (`-an`, `+faststart`);
   - extract poster frame 0 as AVIF and WebP;
   - write manifest fields `media_type`, `duration_s`, `loop` (`pingpong` | `crossfade`) and `poster`.

   **Whether ffmpeg is installed was not checked.**
5. **Code** (for the owner or the implementer):
   - remove the generic `hero` fallback in `apps/pages/services.py:371`;
   - stop the AGAMI page borrowing `entrance_institution`;
   - point the network page to the cooperation slot.
6. **Templates:**
   - `<picture>` with AVIF and WebP sources and `sizes`;
   - `data-focus` → `.img--focus-*`;
   - `loading="lazy"` + `decoding="async"` below the fold;
   - `fetchpriority="high"` only on the one LCP image per page.

**21st.dev classification for image-related patterns.** This role made no 21st.dev calls, since other council members covered components.

| Pattern | Class | Why |
|---|---|---|
| Scroll reveal | A | CSS `clip-path` + `animation-timeline: view()` in `@supports` |
| Hover zoom | A | CSS |
| Background-video section | A | native `<video>` + ES module |
| Bento grid of audience cards | A | CSS grid |
| Scroll parallax | A within CD limits | JS parallax libraries: D |
| Auto-rotating carousels and galleries | D | motion without purpose, a11y and JS cost |
| Ken Burns zoom on stills | D | competes with the three videos |
| Blob or organic image masks | D | CD §5.4 |
| 3D tilt cards, before/after sliders | D | |

No pattern here justifies C (a React island).

---

## 9. Rejected — do not re-evaluate

| id | reason |
|---|---|
| 11679118 | «Lab-Volt» and «Dell» legible |
| 8371705 | rolled documents read as diplomas (recognition, CR-11) |
| 39769780 | Palazzo del Bo: inscription and a door in frame |
| 39221767 | recognisably Berlin |
| 35794575, 37207370 | lavender HDR cast |
| 12366635 | colonnade framed by a dark arch = doorway view |
| 31864645 | shop signs, postcard night |
| 30450186 | arch framing a street reads as a door |
| 8847041 | US flag |
| 29393030 | logo on jacket; stays an alternate only |
| 6951392 (video) | EU, US and Norwegian flags on the table |
| `pro_desk` series (Kaboompics 7876xxx, Pavel Danilyuk 8112xxx, RDNE 7841xxx) | divorce-themed, Lady Justice statuettes, handshake, US flag |
| every Hassan II Mosque and Mausoleum of Mohammed V frame in `ma_city`, `ma_rabat`, `v5_ma_arcade` | sacred places and tourist icons |
| all welding, grinding and plasma clips in `tr_v_weld` | flashes, WCAG 2.3.1 |
| Galleria Vittorio Emanuele and Umberto clips in `v5_v_portico` | tourist icons, luxury storefronts |
| George Pak campus series (7972xxx, 7973xxx) | reads as a US campus, stock |
| `v5_interp` results | call-centre stock, wrong message |

---

## 10. Limits — what I could not do, and why

1. **Query caps.** The earlier attempt of this role made 46 photo and 7 video searches and saved 1,394 medium previews. That is beyond today's caps of 20 / 4 and 3 per slot. This run reused those files **offline** and spent **7 photo + 2 video queries** (`budget.json`).

   **Disclosure:** the contact-sheet function builds each sheet from all 15 "medium" renditions of a search, in memory and not saved. So I saw thumbnails of more than 3 candidates per slot. The 3-per-slot cap was applied to the previews saved and inspected one at a time with the Read tool: 48 across 16 slots (`previews_log.json`).
2. **Every judgement is from a ≈ 350 px preview**, and for 10005316, 30329183, 37293880 and 6549627 only from a 356 px contact-sheet tile. Legible text, small logos and doors at full resolution are **not verified** (§5.8). Nothing here may enter `CURATED` until that check is done.
3. **Nothing was rendered or measured.** There is no graded, duotoned or cropped derivative and no byte count. There is no LCP, CLS or INP measurement of the hero layer or the videos, and no ffmpeg encode. Every size in §4 and §7 is an **estimate**.
4. **Locations are the photographers' titles, not verified.** 8551130, 9489906, 10005316 and 31593601 are **not geolocated**, so their alt texts name no place.
5. **Releases.** The Pexels License does not come with model or property releases. The platform deals with immigration, which I treat as a sensitive context. So identifiable people must never be captioned as applicants, beneficiaries, migrants or Forum attendees: 16856088, 7594098, 9242821, 31367507, 7180823 and 9489906. The legal reading is the owner's.
6. **Stock is a bridge.** The Forum imagery (§3.10–3.11, §4.2) is written to be replaced by commissioned photographs of the Forum in Rovigo (2 October 2026) with releases (`IMAGE_LICENSES.md` §5).
7. **Owner and CD decisions** this report cannot take:
   - the login accent: steps and the F15 prudential reading;
   - the home image cap («porta + 8»);
   - Persona man or woman (both shortlisted);
   - whether to keep the hero layer, subject to measurement;
   - retiring 12 current photographs;
   - the AGAMI and network page changes;
   - commissioning Forum photography.
8. The Pexels key was read only from `PEXELS_API_KEY` and sent only as a request header. It was never printed, logged or written. No raw API response was printed. No production system was touched, and nothing under `C:/tmp/italylegalentry` was modified.

---

## 11. Files

| File | Content |
|---|---|
| `C:/tmp/ile_v5_council/council/IMAGERY.md` | this report |
| `C:/tmp/ile_v5_council/scratch/pexels/ile_pexels.py` | the one Pexels tool (`budget`, `table`, `search`, `vsearch`, `vtable`, `vfiles`, `vframes`, `preview`, `info`, `sheet`) |
| `…/scratch/pexels/budget.json` | 7 photo + 2 video queries of this run, with their strings |
| `…/scratch/pexels/previews_log.json` | 16 slots × 3 inspected previews |
| `…/scratch/pexels/search/v5_*.json`, `videos/v5_v_*.json` | this run's saved responses (earlier runs' files alongside) |
| `…/scratch/pexels/sheets/v5_*.jpg`, `v_v5_v_*.jpg`, `frames_36909064.jpg`, `frames_6951299.jpg`, `frames_5895494.jpg`, `frames_7479048.jpg` | contact sheets and loop-check frames of this run |
| `…/scratch/pexels/medium/<id>.jpg` | the previews looked at (earlier runs' files alongside) |
