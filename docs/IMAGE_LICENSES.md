# IMAGE LICENSES — Italy Legal Entry™

Registro delle immagini self-hosted della piattaforma: provenienza, licenza, uso previsto e stato della
verifica editoriale. Ogni file sotto `static/img/photos/` deve avere una riga in questo documento
(requisito R-LEG-014, R-DES-007, R-PRV-002; registro vietato F15 e F24).

| Campo | Valore |
|---|---|
| Data di riferimento | 17 settembre 2026 |
| Pipeline | `scripts/fetch_images.py` (download → crop editoriale opzionale → strip metadati → derivati WebP/JPEG → `manifest.json`) |
| Manifest | `static/img/photos/manifest.json` (sorgente di verità per `cms.MediaAsset` via `apps/cms/seeds_media.py`) |
| Test | `apps/cms/tests/test_media_assets.py` (manifest, file, limiti di peso, vocabolario vietato, seed idempotente, presenza in questo documento) |
| Direzione artistica | Impl. p.7 §3.1 Note: imprese, persone in formazione, università, sale istituzionali, cooperazione, workshop, professionisti, relazioni internazionali, formazione tecnica, mondo accademico, Italia contemporanea, collaborazione Italia–Marocco, integrazione |
| Soggetti vietati | frontiere, valigie, file/code, passaporti, aeroporti, porte/soglie, griglie/cancelli, iconografia stereotipata della migrazione, cliché turistici (Colosseo, Ponte Vecchio, gondole) |

## 1. Policy

1. **Nessun hotlink.** Le immagini sono scaricate, ottimizzate e servite dal nostro dominio (`static/`
   o `MEDIA_ROOT`). La CSP è `img-src 'self' data:`; `images.unsplash.com` e `images.pexels.com` sono
   nel registro delle stringhe vietate (F24) e il manifest non contiene l'host della CDN.
2. **Licenza verificata prima del download.** Sono ammesse solo: Unsplash License, Pexels License,
   CC0, CC BY 4.0 (con attribuzione), materiale fornito dal committente con autorizzazione scritta
   (loghi: gate G6), SVG/illustrazioni originali del team.
3. **Attribuzione registrata comunque.** La Unsplash License non richiede attribuzione; il nome
   dell'autore viene registrato quando disponibile. Il 17/09/2026 le pagine `unsplash.com/photos/<id>`
   hanno risposto con un controllo anti-bot (HTTP 401) e i file della CDN non contengono metadati
   EXIF/XMP: per tutte le immagini l'autore è quindi registrato come
   «Unsplash contributor (author lookup unavailable offline)», da completare in back-office
   (`MediaAsset.author`) e qui appena la consultazione è possibile.
   **Mai mostrata** (V5.24 §2, 2 nov 2026; corsia v524-px): la licenza Pexels e la licenza Unsplash non la
   richiedono, quindi nessuna didascalia del prodotto stampa più un credito — il credito resta nel
   `PROVENANCE.json` della famiglia (registro degli slot) e in `MediaAsset.credit` (libreria). Una tavola curata
   (`cms.MediaAsset`) mostra la riga d'autore solo quando la licenza lo esige (`MediaAsset.attribution_required`:
   CC BY 4.0, o `attribution=required` in `license_notes`); si veda il punto 10 e il §3.5.
4. **Verifica visiva obbligatoria.** Ogni candidata è stata scaricata e visionata a piena risoluzione
   prima dell'inclusione; le immagini scartate sono elencate in §4 con il motivo, per non rivalutarle.
   Un'immagine entra in `CURATED` solo con `forbidden_subject_check = true`.
5. **Nessun logo, nessun testo di terzi, nessun prodotto riconoscibile.** Dove necessario si applica un
   crop editoriale (ammesso dalla licenza) registrato nel manifest (`crop`, `crop_reason`).
6. **Nessun metadato.** EXIF, XMP e profilo ICC vengono rimossi (privacy dell'autore, peso).
7. **Peso.** Ogni derivato ≤ 350 KB. WebP qualità ~78 (480/960/1440/1920 px, mai upscaling) +
   fallback JPEG 1440 px qualità 80.
8. **Testi alternativi.** `alt_fr` concreto, descrittivo, non stereotipato (sorgente FR); `alt_it`,
   `alt_en`, `alt_ar` restano vuoti finché i traduttori non li forniscono (mai traduzione automatica).
   Vocabolario vietato negli slug/alt/titoli (test): door, porta, passport, valise, suitcase, frontière,
   border, aéroport, airport, queue, file, grille, gate.
9. **Loghi istituzionali** (Regione del Veneto, Comune di Rovigo, partner): mai in `static/`; solo
   `partners.Partner.logo` con `authorized=True` e riferimento scritto (gate G6). Il test verifica che
   nessun file in `static/img/` contenga `veneto`, `rovigo`, `regione`, `comune`, `logo` nel nome.
10. **Un'immagine che esige l'attribuzione** (CC BY 4.0, o una licenza «altra» con clausola di attribuzione)
    **non entra mai nel registro degli slot** (`apps/pages/imagery.py`): la pipeline degli slot non disegna
    didascalie e il test `tests/compliance/test_imagery_v512.py::test_every_slot_is_licensed_and_its_author_recorded`
    esige la Pexels License per ogni slot, così un fotogramma con obbligo di attribuzione non può entrarvi
    inosservato. Entra soltanto come tavola curata `cms.MediaAsset` con `license=cc_by` — la didascalia della
    tavola ne stampa la riga d'autore (`attribution_required`) — oppure viene **sostituita** da un fotogramma
    Pexels/Unsplash dello stesso soggetto attraverso la pipeline esistente (`tools/build_derivatives.py`,
    `scripts/fetch_images.py`: originale fuori dal repository, riga nel `PROVENANCE.json` con licenza, autore,
    pagina, sha256, ritagli e oscuramenti; riga in §3; riga in `docs/design-v5/ASSET_USAGE_MATRIX.md`; un
    fotogramma = un solo slot; O54/O55). Mai nascosta: un credito dovuto si mostra o l'immagine si sostituisce
    (V5.24 §3; corsia v524-px, 5 nov 2026).

## 2. Come aggiungere un'immagine

1. Verificare licenza e soggetto (§1); scaricare e **guardare** la foto a piena risoluzione.
2. Aggiungere un `Candidate` a `CURATED` in `scripts/fetch_images.py`: `photo_id`, `slug`
   (ascii minuscolo, trattini), `usage_slot`, `subject`, `title_fr`, `alt_fr` (≤ 200 caratteri),
   eventuale `crop` (riferito a una larghezza di 1800 px) con `crop_reason`.
3. Eseguire `.venv/Scripts/python scripts/fetch_images.py` (opzioni: `--only <slug>`, `--force`,
   `--cache-dir`, `--check` per la verifica offline). Gli originali restano nella cache temporanea, mai
   nel repository.
4. Aggiungere la riga in §3 di questo documento.
5. Eseguire `manage.py seed_all --only cms.media` (o il seed completo) e i test
   `apps/cms/tests/test_media_assets.py`.
6. Nei template usare **solo** `cms.MediaAsset` (con `alt`) o i file di `static/img/photos/` tramite
   `{% static %}`; mai URL esterni.

## 3. Immagini accettate (15)

Slot d'uso previsti: `hero` (home P3, istituzionale/cooperazione), i quattro accessi
(`entrance_person`, `entrance_company`, `entrance_institution`, `entrance_university`), `forum_event`,
`training_classroom`, `university`, `workshop`, `news_default`, `orientation`, `living`,
`reserved_area`, `cooperation`, `academic`. Larghezze dei derivati: 480/960/1440/1920 WebP (solo ≤
larghezza master) + 1440 JPEG. Tutte le foto: Unsplash License (https://unsplash.com/license), scaricate il
2026-09-17 da `https://images.unsplash.com/photo-<photo_id>?w=2400&q=82&fm=jpg`, autore «Unsplash
contributor (author lookup unavailable offline)», `source_url = https://unsplash.com/photos/<photo_id>`,
verifica soggetti vietati: sì.

| Slug | Photo id (Unsplash) | Slot | Soggetto (alt FR) | Master (px) | Note editoriali |
|---|---|---|---|---|---|
| `reunion-cooperation` | `1517048676732-d65bc937f952` | hero | Professionnels réunis autour d’une table de réunion, prenant des notes pendant un échange de travail | 2400×1600 | luce naturale, sala riunioni; nessun volto riconoscibile in primo piano |
| `entretien-accompagnement` | `1454165804606-c3d57bc86b40` | entrance_person | Deux personnes travaillent côte à côte avec des ordinateurs et un carnet de notes pendant un entretien | 2400×1602 | consulenza/accompagnamento |
| `equipe-entreprise` | `1522202176988-66273c2fd55f` | entrance_company | Trois collègues échangent avec le sourire autour d’une table de travail équipée d’ordinateurs | 2400×1600 | impresa, team |
| `dialogue-institutionnel` | `1517245386807-bb43f82c33c4` | entrance_institution | Participant qui prend la parole pendant une réunion de travail, ordinateur et carnet ouverts devant lui | 2400×1600 | schermo sfocato, nessun testo leggibile |
| `etudiants-bibliotheque` | `1523240795612-9a054b0db644` | entrance_university | Étudiants qui rient en travaillant ensemble dans une bibliothèque universitaire | 2400×1600 | università, formazione |
| `public-conference` | `1540575467063-178a50c2df87` | forum_event | Public attentif assis dans une salle de conférence pendant une intervention | 2400×1600 | sala conferenze (Forum) |
| `salle-de-formation` | `1524178232363-1fb2b075b655` | training_classroom | Salle de formation : un formateur s’adresse à des participants assis en rangées | 1653×1600 (crop da 2400×1600) | **crop** `(560,0,1800,1200)` rif. 1800 px: rimosso lo schermo proiettato con testo di terzi leggibile |
| `campus-universitaire` | `1562774053-701939374585` | university | Façade d’un bâtiment universitaire donnant sur une pelouse entourée d’arbres | 2400×1571 | edificio accademico generico, nessuna insegna |
| `atelier-de-travail` | `1552664730-d307ca884978` | workshop | Atelier de travail : une animatrice organise des notes adhésives sur un mur devant une équipe | 2400×1600 | workshop, co-progettazione |
| `micro-conference` | `1475721027785-f74eccf877e2` | news_default | Micro sur pied au premier plan, devant une salle de conférence en arrière-plan flou | 2400×1600 | immagine di default per Actualités |
| `orientation-ecran` | `1516321318423-f06f85e504b3` | orientation | Main qui pointe un élément à l’écran d’un ordinateur pendant une séance d’orientation | 2400×1600 | wizard di orientamento; schermo sfocato |
| `demarches-ecriture` | `1434030216411-0b793f4b4173` | living | Personne qui remplit des documents à la main sur une table, avec une tasse et un carnet | 2400×1600 | «Vivre en Italie»: pratiche quotidiane |
| `espace-de-travail` | `1519389950473-47ba0277781c` | reserved_area | Vue de dessus d’un espace de travail avec ordinateurs, carnets et casque audio | 1533×1600 (crop da 2400×1600) | **crop** `(0,0,1150,1200)` rif. 1800 px: rimossi marchi visibili su un computer e un caricatore |
| `collaboration-bureau` | `1600880292203-757bb62b4baf` | cooperation | Deux collègues se félicitent en se tapant dans la main, dans un bureau aux murs de briques | 2400×1600 | partner/cooperazione; a destra una finestra ad arco (non una porta) |
| `bibliotheque-savoir` | `1568667256549-094345857637` | academic | Grande bibliothèque circulaire aux rayonnages remplis de livres | 2400×3360 (verticale) | mondo accademico; unico formato verticale della libreria |

Peso totale dei derivati: ≈ 6,9 MB (73 file + manifest: 13 foto × 5 derivati, 2 foto ritagliate × 4 —
nessun derivato 1920 per master < 1920 px). Nessun file supera 350 KB (massimo: `bibliotheque-savoir-1440.webp`, 337 KB).

### 3.1 V5.12 — le fotografie del registro degli slot (W2, corsia C; DECISIONS §6)

Pipeline: originali Pexels fuori dal repository → `tools/build_derivatives.py` (crop registrato, oscuramenti
registrati, il grading V5 unico, Lanczos, AVIF + WebP 480/800/1200/1600 senza upscaling, metadati e ICC rimossi) →
`static/img/v5/<famiglia>/` + `PROVENANCE.json` (autore, pagina Pexels, crop, oscuramenti, byte, sha256). Licenza:
Pexels License (https://www.pexels.com/license/), autore registrato nel `PROVENANCE.json` e **non mostrato** (V5.24
§2, corsia v524-px: fino al 5 nov 2026 la didascalia stampava «Photo : autore / Pexels»; §3.5). Mai hotlink. Regole: un fotogramma = un solo slot in tutto il sito (anche rispetto alle famiglie hero e
portico); nessuna persona riconoscibile (O55); nessun arco, gradino, volta, porta o finestra a griglia come soggetto
(O54); lo stock non è mai documentario (nessun luogo, data o evento nelle alt e nelle didascalie). Test:
`tests/compliance/test_imagery_v512.py`. Peso: 88 file, 2768 KB in tutto; i file presi da un desktop 1x e da un
telefono 3x rispettano 60 KB (LCP) / 45 KB (corpo).

| Slug | Fonte | Autore | Slot | Rapporti | Oscuramenti | Nota |
|---|---|---|---|---|---|---|
| `table-travail-institutions` | Pexels 33543226 | Emre Gokceoglu | `home.ecosystem` | 3:2 | the lanyard badge (mark and name); the lanyard's printed strap; legible handwriting on the papers | hands and documents around a working table; no face in the frame |
| `atelier-mesure-precision` | Pexels 7180823 | Thirdman | `companies.hero` | 3:2 | the caliper's maker's mark and scale lettering | the craftsman's hands, the caliper and the piece; the crop stops under the chin (O55); red sweater -15 % sat.; 3:2 only: the gesture is horizontal and a 4:5 cut loses either the hand or the piece |
| `table-des-institutions` | Pexels 6949366 | Werner Pfennig | `institutions.hero` | 4:5, 3:2 | — | an empty council table: microphones, screens off, blank name cards; no emblem |
| `personne-fenetre-dos` | Pexels 7594198 | Mikhail Nilov | `pathways.hero` | 4:5, 3:2 | — | a man at a desk by a window, seen from behind; nothing legible on the desk |
| `main-cedre-ciseau` | Pexels 30563520 | Moussa Idrissi | `home.pilot.cedar` | 4:5 | — | the hand guiding the chisel through the cedar carving; the face and the shirt's pocket stay out |
| `main-marbre-ciseau` | Pexels 6713855 | Tima Miroshnichenko | `home.pilot.marble` | 4:5 | — | the hand and the chisel on marble; the block is not a recognisable work |
| `bibliotheque-salle-lecture` | Pexels 9489906 | Yaroslav Shuraev | `universities.hero` | 4:5, 3:2 | — | the reading room's end bay: bookcases, a lamp, the long tables by the windows; the two readers and the spiral stair stay out of the crop (O55, O54) |
| `etudiants-echange-campus` | Pexels 31367507 | Yusuf Çelik | `universities.exchange` | 3:2 | the book cover's title; the second book cover; the folder's printed lines | the exchange told by hands: a student's gesture, a book held, a folder; every face stays out of the crop (O55) |

### 3.2 Le famiglie V5 precedenti (hero della home e pannelli «Il portico»)

Righe del registro mancanti fino a V5.12 (audit corsia C, I-5); la provenienza completa è nei rispettivi
`PROVENANCE.json` (`static/img/photos/hero/`, `static/img/portico/`). Licenza: Pexels License, autore registrato.
Nota: le due famiglie condividono oggi tre fotogrammi (il pannello e la tessera dello stesso pubblico, regola AUM 1 «un
contesto»); i quattro fotogrammi dedicati del portico sono un elemento della W3 (DECISIONS §6).

| Famiglia | Slug | Fonte | Autore | Pagina | Alt (fr) |
|---|---|---|---|---|---|
| hero | `lectrice-bibliotheque-dos` | Pexels 29492060 | Julio Lopez | https://www.pexels.com/photo/young-adult-studying-in-modern-library-setting-29492060/ | Lectrice vue de dos, assise seule à une longue table de bibliothèque en bois, sous une lampe allumée |
| hero | `chai-cuve-chene` | Pexels 30557565 | Liv Kao | https://www.pexels.com/photo/winemaker-cleaning-oak-barrels-in-french-cellar-30557565/ | Vu d’en haut, un ouvrier de chai nettoie au jet d’eau une grande cuve en chêne |
| hero | `table-en-seance` | Pexels 6949886 | Werner Pfennig | https://www.pexels.com/photo/tablets-on-table-in-conference-room-6949886/ | Table de réunion publique en séance : micros, verre d’eau et chevalet vierge au premier plan, un orateur et une participante flous à l’arrière-plan |
| hero | `paillasse-deux-etudiantes` | Pexels 3735757 | Polina Tankilevitch | https://www.pexels.com/photo/women-in-white-laboratory-gown-standing-3735757/ | Deux étudiantes en blouse blanche, vues de dos, travaillent à une paillasse de laboratoire en bois |
| portico | `lectrice-bibliotheque-dos` | Pexels 29492060 | Julio Lopez | https://www.pexels.com/photo/young-adult-studying-in-modern-library-setting-29492060/ | Lectrice vue de dos, assise seule à une longue table de bibliothèque en bois |
| portico | `chai-cuve-chene` | Pexels 30557565 | Liv Kao | https://www.pexels.com/photo/winemaker-cleaning-oak-barrels-in-french-cellar-30557565/ | Vu d’en haut, un ouvrier de chai nettoie au jet d’eau une grande cuve en chêne |
| portico | `table-en-seance` | Pexels 6949886 | Werner Pfennig | https://www.pexels.com/photo/tablets-on-table-in-conference-room-6949886/ | Table de réunion publique en séance : micros et chevalet vierge au premier plan, deux participants flous à l’arrière-plan |
| portico | `cours-tableau-dos` | Pexels 37811164 | Eduard Perez | https://www.pexels.com/photo/university-lecture-scene-with-female-teacher-writing-on-whiteboard-37811164/ | Cours vu du fond de la salle : une enseignante écrit au tableau, des étudiants vus de dos au premier plan |


### 3.3 V5.15 — il passaggio immagini della W3 (corsia C, label v515-c-build)

Stessa pipeline e stesse regole del §3.1 (un fotogramma = un solo slot, O54, O55, stock mai documentario, mai hotlink).
Undici fotogrammi nuovi, uno per pagina importante che ne era priva (V5.15 §5): le intestazioni («il frontespizio») di
Formation, Diplômes et titres, Projet pilote (dittico), Le projet, Réseau, Contact, Vivre en Italie, e tre composizioni di
sezione (Institutions, Entreprises, Formation). Il parametro `soft` del builder ammorbidisce (invece di accentuare) i
fotogrammi a trama fine, perché restino nei budget senza blocchi. Peso totale `static/img/v5/`: 184 file, 7455 KB.
Nessuna foto per il Forum (Q4) né per AGAMI (Q5); le quattro immagini del portico (mega menu) restano quelle dedicate di
`static/img/portico/` (§3, non ripetute altrove).

| Slug | Fonte | Autore | Slot | Rapporti | Oscuramenti | Nota |
|---|---|---|---|---|---|---|
| `atelier-soudure-geste` | Pexels 5265332 | Jeswin  Thomas | `training.hero` | 3:2 | the jacket's brand mark | a trainee hands the torch to another over the vice; the one face in the full frame (right, in profile) is above the crop (O55); the helmets' decals are outside it; 3:2 only (a 4:5 cut brings the profile back) |
| `microscopes-rangee` | Pexels 15290006 | Vladimir Srajber | `training.after` | 3:2 | — | a row of microscopes on a pale bench: structured learning, nobody in the frame |
| `classeur-documents-ouvert` | Pexels 4792286 | Anete Lusina | `diplomas.hero` | 3:2 | — | an open accordion case of papers on a wooden table, from above; nothing legible on the papers |
| `plaine-peupliers-hiver` | Pexels 11010756 | Serena Koi | `pilot.plain` | 4:5 | — | a row of bare poplars over a ploughed plain in the mist; the alt names no place (stock is never documentary) |
| `champs-montagnes-printemps` | Pexels 36909829 | mouad simou | `pilot.fields` | 4:5 | — | flowering fields under a snow-capped range; the alt names no place |
| `grande-salle-etude` | Pexels 10323211 | versolaluce | `project.hall` | 3:2 | — | a great study hall seen from a gallery: glazed walls, long tables; the people are small, seen from above, none turned to the camera; the near readers of the full frame's foot are below the crop (O55) |
| `table-commune-vue-haut` | Pexels 34632581 | Jaykumar Bherwani | `network.table` | 3:2 | — | one long shared table from straight above: laptops, papers, the tops of heads — no face (O55) |
| `rue-facades-couleurs` | Pexels 12900263 | Helena Jankovičová Kováčová | `living.street` | 21:9, 3:2 | the house number | a street of stucco façades, shutters and balconies; the parked cars, their plates and the cyclist stay below the crop; the alt names no city |
| `place-civique-palais` | Pexels 14581980 | Serena Koi | `contact.square` | 3:2 | — | a civic square between two palazzi; five passers-by seen from behind, small, none identifiable (O55); the square, not a doorway, is the subject (O54); the alt names no city |
| `serres-plaine-crepuscule` | Pexels 5906831 | Serena Koi | `companies.territory` | 21:9 | — | greenhouse tunnels across a cultivated plain at dusk: the productive territory; nobody in the frame; the alt names no place |
| `hemicycle-pupitres` | Pexels 32266781 | Héctor Berganza | `institutions.chamber` | 3:2 | the printed sheet on the desk | the desks and microphones of an assembly hall; the flags and coats of arms under the windows are above the crop; the chamber is not recognisable in the crop |

### 3.4 V5.22 — sette fotogrammi nuovi e quattro ritagli (corsia M, label v522-m-build e v522-m-improve1; SECTION_SYSTEM_V2 §8)

Stessa pipeline e stesse regole del §3.1 (un fotogramma = un solo slot in tutto il sito, verificato anche sull'impronta
sha256 dell'originale; O54, O55; nessun cliché; nessun testo o marchio leggibile; lo stock non è mai documentario; mai
hotlink; Q4 e Q5 intatti). Originali fuori dal repository (`.work/v522-m/originals/`, scaricati una volta dalla CDN
Pexels, l'autore letto dall'API con la chiave dell'ambiente, mai stampata né scritta). Novità del builder:
`ceilings` (il tetto del tipo, SECTION_SYSTEM_V2 §7.3, vale per OGNI larghezza AVIF servibile: corpo 45 KB, banda e
panorama 60 KB, pannello 2:3 del pilota 60 KB, fotogramma di famiglia 30 KB, fondo K 60 KB a 21:9 e 40 KB a 4:5); il
WebP di ripiego sta sotto lo **stesso** tetto (revisione 1, v522-m-improve1: nessuna tolleranza, il §7.3 non ne
prevede) e una larghezza WebP che non vi rientra a q 40 non viene costruita (`webp_not_built` nel PROVENANCE; ogni
larghezza AVIF resta); `desat` (desaturazione nel file), `tone: "cool"`, la modalità d'oscuramento `median` (cancella i tratti stampati e lascia nitide le forme), `keep` (un ritaglio aggiunge un rapporto senza toccare
i file già pubblicati). **Per la regola del §8 («nessun nome di persona copiato in un altro documento») l'autore non è
riportato qui: è nel `PROVENANCE.json` della famiglia soltanto (V5.24 §2, corsia v524-px: nessuna didascalia lo
mostra più; fino al 5 nov 2026 «Photo : autore / Pexels»; §3.5).**

| Slug | Fonte | Autore | Slot | Rapporti | Oscuramenti | Nota |
|---|---|---|---|---|---|---|
| `pierre-appareillee` | Pexels 11499083 | PROVENANCE.json | `home.integrity.stone` | 21:9, 4:5 | — | conci squadrati in luce radente, frontali, nessuna apertura né segno; fondo decorativo (alt vuoto) della banda dell'integrità, −35 % di saturazione nel file, grana ammorbidita (`soft` 1,6) sotto il velo di pietra al 60 % |
| `codici-rilegati` | Pexels 29976379 | PROVENANCE.json | `project.volumes` | 21:9, 16:9, 4:5 | — | volumi rilegati in cuoio, nervature e dorature in luce radente; ogni ritaglio parte sotto le etichette dei titoli (y 0,37), nessun titolo leggibile; grading freddo; scala e soggetto diversi dalla sala di lettura delle Università |
| `entrepot-allee-rayonnages` | Pexels 29454379 | PROVENANCE.json | `pathways.family.work` | 3:2, 21:9 | — | corsia di magazzino logistico in prospettiva tra alte scaffalature, vuota; le etichette dei cartoni sono illeggibili a ogni larghezza servita |
| `notes-cahier-livre` (revisione 1) | Pexels 6334273 | PROVENANCE.json | `pathways.family.study` | 3:2, 21:9 | le cifre e le parole scritte a mano oltre la penna, in **un solo** riquadro (due riquadri contigui lasciano una cucitura di tratti nitidi), dove la pagina è già fuori fuoco | all'altezza del tavolo, non dall'alto: una mano scrive con una penna bianca in un quaderno a righe, un libro aperto dietro, un secondo libro al bordo; caldo (tweed bruno, camicia rosa, legno chiaro); il volto è sopra l'inquadratura (entrambi i ritagli partono sotto il colletto); pagine e copertine senza nulla di leggibile. Sostituisce 6549915 (vista dall'alto accanto a «Famille», quasi neutro: il «select» non cambiava nulla; una cucitura negli oscuramenti del dizionario) |
| `table-partagee-vue-haut` (revisione 1) | Pexels 27177298 | PROVENANCE.json | `pathways.family.family` | 3:2, 21:9 | — | tavola condivisa vista dall'alto su un piano di legno traforato: ciotole di olive, pomodori, una salsa e arachidi; una mano porge il cucchiaio, l'altra tiene la ciotola di olive; nessun volto, nessuna scritta, nessun marchio; i bicchieri e una terza mano al bordo superiore e il tagliere del pane a destra restano fuori da entrambi i ritagli. Sostituisce 3184192 (la tavola da brunch generica) |
| `vignes-brume-aube` | Pexels 9250930 | PROVENANCE.json | `pathways.family.other` | 3:2, 21:9 | — | filari di vite sotto reti nella foschia, alberi e colline; nessuna persona; l'alt non nomina il luogo |
| `banc-electrique-mains` | Pexels 34526423 | PROVENANCE.json | `training.before` | 4:5, 3:2 | il logo e l'etichetta stampata di un salvamotore; le diciture di un interruttore modulare; i codici dei relè e i numeri dei morsetti; un'etichetta CE — cancellati con un filtro mediano (le forme restano nitide, nessuna macchia sfocata) | mani che cablano i relè di un banco didattico elettrico, tra canaline blu e cavi rossi; il volto (x 0,17–0,27) è fuori da entrambi i ritagli, che partono da x 0,30 (O55); le diciture del pannello di alimentazione e la finestra a lamelle restano fuori |
| `main-cedre-ciseau` (ritaglio) | Pexels 30563520 | §3.1 | `home.pilot.cedar`, variante `pannello` | + 2:3, 3:2 | — | il pannello 2:3 a tutta altezza (2 023 × 3 035) e la fascia 3:2 dei telefoni; la tasca della camicia resta fuori; il 4:5 del §3.1 invariato |
| `main-marbre-ciseau` (ritaglio) | Pexels 6713855 | §3.1 | `home.pilot.marble`, variante `pannello` | + 2:3, 3:2 | — | il pannello 2:3 (2 667 × 4 000) da x 0,31 (revisione 1): taglia il pollice, mai la lama — il suo spigolo cade a 0,814 del pannello, così sotto la copertura della home (~30 % × 82 vh) la lama sulla pietra resta ≥ 6,8 % dentro il bordo a 1024 × 768 e ≥ 14 % da 1280 × 800; l'intero fotogramma come fascia 3:2; nessun volto; il 4:5 del §3.1 invariato |
| `table-travail-institutions` (ritaglio) | Pexels 33543226 | §3.1 | `home.ecosystem`, variante `campata` | + 4:3 | gli oscuramenti del §3.1 (cordino, scritta) restano | il 4:3 sotto l'arco (6 869 × 5 152): esce la parete rossa al bordo iniziale; il 3:2 del §3.1 invariato serve i telefoni |
| `etudiants-echange-campus` (ritaglio) | Pexels 31367507 | §3.1 | `universities.exchange` | 3:2 (nuovo ritaglio) | **nessuno** (erano tre) | ritagliato sulle mani: il gesto che spiega, la custodia tenuta contro di sé; il libro, le copertine e ogni volto fuori dal ritaglio — le due copertine sfocate si leggevano come oggetti censurati a 768 px |

Pesi e tetti: tutti i file AVIF **e WebP** dei rapporti V5.22 rientrano nel tetto del loro tipo (test
`tests/compliance/test_imagery_v512.py::test_v522_every_new_frame_holds_its_kind_ceiling_on_every_width`); larghezze,
qualità e byte di ciascun file nel `PROVENANCE.json` della famiglia. La tavola dei fotogrammi, disegnati dal tag
`photo` alle loro larghezze V2: `/__design-v5/specimens/imagery/` (solo sviluppo: un banco di prova raggiungibile
per URL, non collegato dall'indice dell'anteprima).

**Candidate scartate (V5.22, verificate a piena risoluzione o sul provino a 940 px):** pietra — 17082070 (finestra ad
arco), 14325123 (archi), 30222051 (gradini e portale), 27504687 (finestra con persiane come soggetto), 33646494
(finestra ad arco: O54), 37064755 e 12998849 (pietrame irregolare, non conci squadrati), 5483977 (mattoni dipinti, non
pietra); volumi — la maggior parte dei provini mostra titoli leggibili su tutta l'altezza dei dorsi: 29976379 è il solo
che consente un ritaglio sotto le etichette; studio — 6550119 e 5238080 (scrittura a mano grande e leggibile), 5238117
(anelli e orologio in primo piano); famiglia — 4393008 (piatti da ristorante, non una tavola di famiglia), 6232533
(tavola delle feste: connotazione stagionale), 5616129 (bottiglia con etichetta di marca); vigne — 13166995 (linee
elettriche, cielo rosa), 30067713 (lampione nella notte, tono cupo), 36189155 (una casa colonica come soggetto, tono
scuro); formazione tecnica — 5265337 (breadboard di elettronica con diciture stampate, non un quadro elettrico),
18471553 (pannello didattico con marchio, senza mani), 28942196 (scatola di un inverter con diciture, senza mani),
9242810, 9242812, 33992840 (volti riconoscibili, O55); 34938452 (mani che serrano un ripartitore su barra DIN: il soggetto giusto, ma l'autore Pexels è un account aziendale, e la didascalia avrebbe stampato un marchio commerciale sotto la foto); 11679118 (kit elettronico con marchi e un monitor di marca); 6412539 (una mano che taglia un filo: debole come «formazione»).

**Candidate scartate (revisione 1, v522-m-improve1):** studio, all'altezza del tavolo — 37860169 e 37778746 (appunti a
mano grandi e leggibili su tutta la pagina: andrebbero oscurati quasi interi), 32410282 e 35376343 (caratteri
leggibili; nel secondo una bottiglia con etichetta e un astuccio con personaggi di marca), 8640080 (una rivista con il
titolo leggibile), 5386435 e 5386468 (l'autore Pexels è l'indirizzo di un sito: la didascalia avrebbe stampato un URL;
nel secondo parole leggibili), 6238011, 6237967 e 7054509 (toni freddi: il «select» non cambierebbe quasi nulla),
6519141 (biglietto d'auguri con testo stampato, bicchiere da festa), 5912284 (elenco leggibile e schermo di un
portatile), 11977130 (vista dall'alto); famiglia — 27177297 (la stessa tavola, gesto meno condiviso), 38431262 e
38431258 (piatti da ristorante, patatine), 7220884 e 7220887 (piatti composti come una bandiera: cliché), 5779178 e
5779181 (tavola delle feste, un telefono in mano).

### 3.5 V5.24 — i crediti visibili rimossi (corsia v524-px, 5 nov 2026)

Decisione del committente (V5.24 §2–§3, 2 nov 2026): nessun «Pexels», «Photo by …», «Source : Pexels», «Pexels.com»
visibile sotto le immagini del sito pubblico e della piattaforma, ovunque la licenza permetta l'uso senza
attribuzione; la provenienza resta INTERNA. Verifica (evidence `v524/IMAGERY_ATTRIBUTION.md`): ogni fotografia
servita è Pexels License (i 26 fotogrammi del registro degli slot, i 4 dell'hero, 1 del portico — «Attribution is
not required») o del committente (la porta); la libreria Unsplash ritirata (§3) non è servita in nessuna pagina
(«No permission needed»); nessun asset CC BY esiste nel repository né nei seed → nessuna sostituzione. Che cosa è
cambiato: `templates/components/photo.html` non disegna più la `<figcaption class="foto__credit">` e nessun
attributo la rimpiazza; `pages.imagery.Picture.credit` non esiste più (`record()` e `provenance()` restano);
`cms.MediaAsset.attribution_required` (CC BY 4.0 o `attribution=required`) e `forum.ForumMedia.attribution_required`
governano la riga d'autore delle tavole curate — `pages/partials/_ingresso.html`, `news/detail.html` (corsia PX) e,
per contratto, `pathways/detail.html`, `forum/partials/hero.html`, `forum/partials/permanent_sections.html` (corsie
PUB1 e PUB2); `is_publishable` non cambia (il credito resta registrato). Le regole CSS `.foto__credit` sono selettori
morti finché la corsia proprietaria di ciascun foglio li toglie (LIB, PUB1, HOME, PUB2). Test di produzione — il
«Pexels-visible-label check» del gate finale (V5.24 §23, §30): `tests/compliance/test_imagery_credits_v524.py`
(sorgenti, 184 pagine pubbliche in quattro lingue, le pagine dei personaggi, le pagine d'errore, il registro).
Il nome dell'autore resta nel solo `PROVENANCE.json` della famiglia (SECTION_SYSTEM_V2 §8).

### 3.6 V5.32 — il giro di correzione della revisione d'integrazione (corsia B, label v532-b-correction, 12 nov 2026)

Stessa pipeline e stesse regole del §3.4 (un fotogramma = un solo slot, anche per impronta sha256 dell'originale; O54,
O55; nessun testo o marchio leggibile; lo stock non è mai documentario; mai hotlink). Due fotogrammi nuovi, presi dalla
cache del consiglio (`proof/research/images/originals`, già vagliati nelle sue note di triage: 6814351 «PASS with one
crop», 5894283 «STRONG»), e uno spostamento. P1-1: la scheda «après l'arrivée» di Formation mostrava i microscopi, che
sono il fotogramma del percorso «Recherche scientifique» — ora mostra una lezione per adulti, e i microscopi passano allo
slot `pathways.research`, disegnato soltanto dal percorso (stessi file, stessa alt). P2-1: il percorso «Travail
indépendant et entrepreneuriat» disegnava il calibro di Entreprises (variante `tappa` di `companies.hero`, ora tolta) —
ora ha il proprio fotogramma; il calibro resta a Entreprises soltanto. L'abbinamento dei percorsi è uno solo
(`pages.services.PATHWAY_FRAMES`: l'esploratore di Parcours, la testa della scheda, il risultato del questionario, la
scena della home). Autore: solo nel `PROVENANCE.json` della famiglia (§3.4).

| Slug | Fonte | Autore | Slot | Rapporti | Oscuramenti | Nota |
|---|---|---|---|---|---|---|
| `cours-paperboard-dos` | Pexels 6814351 | PROVENANCE.json | `training.after` | 3:2 | la parola scritta a mano sul foglio del paperboard, cancellata con un filtro mediano (il foglio resta bianco, nessuna macchia sfocata) | un formatore di spalle scrive su un paperboard davanti a due partecipanti seduti, anch'essi di spalle: una lezione per adulti; nessuno riconoscibile (O55); la porta vetrata con le lamelle al bordo sinistro resta fuori dal ritaglio, che parte da x 0,14 (O54); trattamento «develop» come prima |
| `cordonnier-etabli-vue-haut` | Pexels 5894283 | PROVENANCE.json | `pathways.independent` | 3:2 | lo schermo acceso di un telefono sul banco, cancellato con un filtro mediano | visto dall'alto tra due travi sfocate: un calzolaio al suo banco allaccia un paio di scarpe nere, il grembiule e gli attrezzi intorno; il ritaglio parte sotto il mento (y 0,235; il volto finisce a 0,215), nessun volto (O55); `soft` 0,5 (la trama fitta del grembiule e del pavimento) |
| `microscopes-rangee` (spostato) | Pexels 15290006 | §3.3 | `pathways.research` (era `training.after`) | 3:2 | — | gli stessi file e la stessa alt del §3.3; disegnato soltanto dal percorso «Recherche scientifique», a colori, senza trattamento |

## 4. Candidate scartate (verificate visivamente il 17/09/2026)

| Photo id | Motivo |
|---|---|
| `1521737604893-d14cc237f11d` | grandi porte-finestra dominano lo sfondo (F15: niente porte/soglie) |
| `1541339907198-e08756dedf3f` | cliché della laurea con skyline extraeuropeo riconoscibile |
| `1531482615713-2afd69097998` | porta visibile sullo sfondo (lettura prudenziale di F15) — unica candidata «formazione tecnica»: **slot da coprire con una nuova selezione** |
| `1556761175-b413da4baf72` | scritta a parete e lattina con marchio nell'inquadratura |
| `1573164713714-d95e436ab8d6` | foto di prodotto (tablet/laptop con desktop del produttore) |
| `1497366216548-37526070297c` | lungo corridoio di vetrate a griglia: evoca griglie/soglie |
| `1523580494863-6f3031224c94` | logo di terzi sugli schermi del palco |
| `1505373877841-8d25f7d46678` | interfaccia di un prodotto terzo come soggetto della slide |
| `1553877522-43269d4ea984` | logo del produttore sul computer; monocromo a basso contrasto |
| `1529156069898-49953e39b3ac` | scena turistica/ricreativa estranea alla piattaforma |
| `1455390582262-044cdead277a` | marchio inciso sul pennino |
| `1486406146926-c627a92ad1ab` | grattacieli con facciate a griglia, nessun legame con l'Italia contemporanea |
| `1513584684374-8bab748fbf90` | villa privata con decorazioni stagionali, fuori tema |

Nessuna candidata ha risposto 404.

## 5. Lacune note e prossime selezioni

- **Italia contemporanea / collaborazione Italia–Marocco / integrazione**: nessuna candidata del lotto
  iniziale rappresenta esplicitamente questi temi. Da selezionare (con gli stessi criteri) in un lotto
  successivo; in alternativa fotografie originali del Forum di Rovigo (2 ottobre 2026) con liberatorie.
- **Formazione tecnica**: l'unica candidata è stata scartata (porta sullo sfondo); da coprire.
- **Attribuzioni**: completare `author` per ogni foto appena la consultazione di Unsplash è possibile.

## 6. Font

Vedi `docs/DESIGN_SYSTEM.md` (font open-source self-hosted in `static/fonts/`, `font-display: swap`,
nessun Google Fonts — F24, R-DES-004).

Registro corrente (design V4, 24/09/2026 — `docs/design/DESIGN_SYSTEM_2026.md` §6): Newsreader
(Production Type), Noto Naskh Arabic (Google), IBM Plex Sans, IBM Plex Mono e IBM Plex Sans Arabic
(IBM Corp.), tutti **SIL Open Font License 1.1**. I file latini di Plex Sans e Plex Mono provengono dai
pacchetti npm `@fontsource/ibm-plex-sans` e `@fontsource/ibm-plex-mono` 5.3.0 (stessa licenza OFL sui
font; MIT sul pacchetto), copiati in `static/fonts/` con `scripts/fetch_fonts.py --from-fontsource`.
Fira Sans e Fira Mono (Carrois Apostrophe, OFL 1.1) sono stati ritirati con V4.

## 7. Loghi e materiale del committente

Nessun logo istituzionale è presente nel repository. Loghi di Regione del Veneto, Comune di Rovigo e
partner verranno caricati **solo** in `partners.Partner.logo` dopo trasmissione con autorizzazione
scritta (gate G6) e registrati qui con fonte «fornito dal committente con autorizzazione del <data>».
Il logo attuale del sito (tagline «Digital Pathways to Italy» + porta) era
`LOGO_PENDING_CLIENT_CONFIRMATION` (F12–F15). **Confermato dal committente il 23 settembre 2026**
(addendum «Asset ufficiali»): è il logo di riferimento del progetto, recuperato verbatim dal
markup inline di legalitalentry.it in `static/brand/original/logo-mark.svg`. Provenienza,
anatomia e regole d'uso in `docs/design-v2/BRAND_ASSETS.md`.

### 7.1 Fotografia del committente

| Campo | Valore |
|---|---|
| Soggetto | facciata di una fontana monumentale romana, usata dentro l'arco dell'hero («arch-photo-bg») |
| Autore | **il titolare del progetto** (dichiarato in sessione il 23 settembre 2026) |
| Diritti | del titolare; nessuna licenza di terzi |
| Origine tecnica | servita nel sito attuale dal CDN Unsplash (`photo-1525874684015-58379d421a52`); qui scaricata una volta a 2400 px |
| Copia locale | `docs/design-v2/brand-original/arch-photo-original-2400.jpg` (949 KB, evidenza, non servita) |
| Derivati serviti | *da produrre dal file master del titolare* (AVIF/WebP, ≤ 120 KB per viewport) in `static/brand/v2/` |
| Runtime | **mai** richiesta al CDN né al sito legacy |
