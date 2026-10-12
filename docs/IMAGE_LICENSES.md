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
