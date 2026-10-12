# DESIGN V3 — SUPERFICIE: **IMMAGINE**

Area `imagery` · round 2, 24 settembre 2026 · Vincolanti: `DESIGN_SYSTEM_V2.md`, `MOTION_SYSTEM.md`,
`docs/IMAGE_LICENSES.md`, `apps/cms/forbidden.py`. Nessun file del repository è stato toccato per scrivere questo documento: tutte le misure di
questo round sono state prese in Chromium headless (Playwright del `.venv`, browser proprio, **mai** la 9222) sul sito vivo `127.0.0.1:8771`, iniettando il
foglio candidato come `<link>` same-origin (l'iniezione `<style>` è stata **rifiutata dalla CSP** `style-src 'self'` — è la prima prova che il vincolo è in
vigore). Le pesature sono codifiche reali, fatte con Pillow 12.3 (AVIF e WebP disponibili) su tre master fotografici del repository.

---

## 0. RICHIESTE DI DEROGA (numerate, in testa, come prescritto)

**DEROGA 1 — DESIGN_SYSTEM_V2 § 6 e § 7: una lastra su `news/detail`, che è STANDARD.**
§ 6 dice «Altre fotografie solo su IMMERSIVE e RICH»; § 7 classifica «news» come STANDARD. Chiedo che la riga STANDARD del § 7 ammetta **una sola** eccezione
nominata: `news/detail` (il **dettaglio** di un articolo, mai l'indice, mai le card di lista) può portare **una** `.plate--news`.
*Motivo:* un articolo datato non è una pagina informativa: è un documento con una data, un autore e — quando esiste — una fotografia che è **prova** del fatto
che racconta. Il template porta già `hero_image` e `image_caption`: il modello del prodotto ha sempre previsto questa immagine; è il design system che non l'ha
classificata.
*Costo, dichiarato:* la riga STANDARD guadagna **solo** questo. Nessun capitolo mezzanotte, nessuna isoipsa, nessun reveal oltre i 240 ms già ammessi, nessuna
immagine sull'indice `/actualites/` (che resta un registro: occhiello, data, titolo), nessuna ombra oltre il ruolo 2. Il test di modo conta `main .plate` per
`data-mode` e ammette **≤ 1** in `standard` **solo** sulla rotta `news:detail`.
*Se la deroga è negata:* `.plate--news` cade, `news/detail.html` resta esattamente com'è oggi, e questa superficie passa da quattro slot a tre. Non si discute
oltre.

**Nessun'altra deroga è richiesta.** In particolare **non** chiedo più — e ho rimosso — tutto ciò che nel round 1 avrebbe richiesto una deroga senza
dichiararla: l'oggetto indicizzato allo scroll sulla home (MOTION_SYSTEM § 4), l'animazione di `box-shadow`, la fotografia sulle pagine d'autenticazione
(DESIGN_SYSTEM_V2 § 8.8 dice testualmente «nessuna fotografia»), su `le-projet`, su `agami` e su `réseau`.

---

## 0-bis. RISPOSTA PUNTO PER PUNTO ALLA REVISIONE

| MUST-FIX | Esito | Dove |
|---|---|---|
| 1 · otturatore dietro `html.js` | **FATTO** — l'otturatore **non esiste più**. La fotografia non è mai nascosta, da niente. Lo stato JS-gated riguarda solo il cartellino e usa la convenzione della casa | § 4.5, § 5 |
| 2 · token `--plate-ar-*` e collisione `--route` | **FATTO** — tre soli token, `--plate-ar-chapter/portrait/record`. Nessun token si chiama `--route` | § 4.5 |
| 3 · `picture` non dimensionato | **FATTO** — l'immagine è in posizione assoluta a `inset: 0`; `picture{display:block}`. Misurato: riquadro 1440×615 in una banda 1440×617, `objectFitEngaged: true` | § 4.5, § 4.6 |
| 4 · `data-priority` mai emesso | **FATTO** — emesso sulla `<figure>`. Misurato sulla lastra LCP: `content-visibility: visible`; su una lastra sotto la piega: `auto`, riquadro 687×458, rapporto 1.500 | § 4.4, § 4.6 |
| 5 · posizionamento del cartellino di capitolo e contrasto | **FATTO** — lo scrim è **cancellato**; il cartellino è una superficie **opaca** di livello 2 (`--mid-3`) che risale di 24 px dentro la banda. Contrasti ricalcolati su fondo opaco: `--on-dark` 12,29:1, `--on-dark-2` 7,67:1 | § 4.5, § 4.6, § 6 |
| 6 · contraddizione `box-shadow` | **FATTO** — in `plate.css` non esiste **nessuna** dichiarazione `box-shadow` (verificato: 0 occorrenze sul file senza commenti). La cornice è un `border`. L'hover sulla lastra è stato tolto del tutto | § 4.5, § 5 |
| 7 · budget degli oggetti indicizzati allo scroll | **FATTO** — questa superficie non ha **alcun** moto legato allo scroll. La deriva di 24 px è stata rimossa e non sostituita | § 5 |
| 8 · tabella degli slot contro § 6/§ 7 | **FATTO** — `.plate--seal` e `.plate--band` cancellati; `agami`, `réseau`, `le-projet` non prendono immagine; una sola **DEROGA 1** per `news/detail` | § 0, § 4.3 |
| 9 · `.plate-strip` non specificata | **FATTO** — anatomia, CSS, markup, tastiera, mappatura di `ForumMedia`, caso `kind == "video"`, censimento in byte. Lightbox `<dialog>` e `aria-current` **eliminati**, con motivo | § 4.4, § 4.5, § 4.8, § 6 |
| 10 · una sola forma di `Photo` | **FATTO** — una sola dataclass in `pages.services`; `ecosystem.services.Photo` cancellata; `webp_srcset`→`srcset`, `share_image`→`share_path`; `sizes` **non** è un campo di `Photo` e non può più essere vuoto | § 4.8 |
| 11 · sorgente di verità di `place` e `date` | **FATTO** — le quattordici Pexels sono **ritirate come sorgenti**. Tre sole provenienze possono produrre una lastra, con il rifiuto scritto nella pipeline | § 4.9 |
| 12 · percorso dati di `news/detail` | **FATTO** — la vista costruisce la `Photo`; la frase «nessun cambio di vista» è stata cancellata | § 4.8 |
| 13 · hero del Forum | **FATTO** — la lastra **non** va sotto i testi bloccati né sotto i loghi: sta **dopo** `forum-hero__inner`, a piena larghezza. Regola generale: nulla è mai stampato su una lastra | § 4.3, § 4.7 |
| 14 · strato grafico del capitolo pilota | **FATTO** — la rotta, le rive, la sequenza bloccata e la nota giuridica **non** vanno sopra la fotografia: la banda apre il capitolo, la rotta resta sul fondo piatto `--mid-1`, dove `--terr-line` è verificata a 6,07:1 | § 4.3, § 4.7 |
| 15 · modulo JS e cablaggio CSS | **FATTO** — percorso, entry esbuild, `@import`, preload, e la ragione per cui `[data-plate]` non incontra mai `shell.js` | § 4.7 |
| 16 · msgid francese e riferimenti incrociati | **FATTO** — msgid FR; § 1.8→§ 1.7, § 1.11→§ 1.10 corretti; la quarta `<figure>` senza didascalia aggiunta | § 1.7, § 4.4 |
| 17 · sostituire un moto di default | **FATTO** — tutti e tre sono stati rimossi (otturatore, parallasse, hover-scale). Ne resta **uno**, ed è il cartellino che entra nel suo alloggiamento | § 5 |
| 18 · censimento a DPR 2 e tetto a 2000 px | **FATTO** — censimento rifatto misurando *quale gradino Chromium sceglie* a DPR 1/2/3, e tetti per derivato ricavati da codifiche reali | § 4.6, § 7 |

**Punti contestati: nessuno.** Su uno il revisore ha ragione e la misura reale è **peggiore** della sua (§ 4.6, riga B): la sua `4,29:1` al «75 %» è il
composito dello scrim **all'opacità 0,75**, che cade al 94,7 % della corsa; al 75 % *della corsa* il composito misurato è `rgb(137,143,147)` e `--on-dark-2`
vale **1,81:1**. Il round 1 non era al limite: era fuori di tre volte.

---

## 1. VERDETTO SULLO STATO ATTUALE

Il committente dice «uso insufficiente di immagini». È un eufemismo: **non ce n'è nessuna.**

**1.1 Zero fotografie sul sito pubblico.** Audit Chromium headless su dieci rotte in stato 200 — `/fr/`,
`/parcours/`, `/reseau/`, `/actualites/`, `/forum/`, `/agami/`, `/entreprises/`, `/institutions/`, `/universites-et-formation/`, `/le-projet/` — a 1440×900 e
390×844. Ovunque: `photos=0`, `figure=0`, `figcaption=0`. Gli unici `<img>` sono due `logo-mark.svg` e, sulla sola home, `doorway-480.avif` + `key.svg`.

**1.2 La home è alta 7 921 px e contiene lo 0,94 % di fotografia** (ri-misurato in questo round:
`document.documentElement.scrollHeight == 7921` a 1440). La lastra della porta misura **401×267** px CSS = 107 067 px² su 11 406 240 px². Mobile: 189×126 su
390×11 183 = **0,55 %**.

**1.3 Le quattro vie d'accesso** — che DESIGN_SYSTEM_V2 § 7 classifica IMMERSIVE, dove «fotografia» è ammessa —
**non hanno né foto né capitolo mezzanotte.** `/fr/entreprises/` = 5 109 px di sola tipografia. `templates/ecosystem/{companies,institutions,universities,pilot}.html`
includono già `ecosystem/partials/photo.html`: lo slot esiste, la vista lo popola, non esce nulla. La colonna che lo ospita misura **944 px a 1440, 800 a 1280,
648 a 1024, 688 a 768, 350 a 390** — e `.ecosystem-photo` **non ha una sola riga di CSS** in tutto il progetto (`grep` su `static/css/**` → 0).

**1.4 La causa: 15 immagini su 15 sono strutturalmente impubblicabili.** `MediaAsset.objects.count()==15`,
`publishable==0`. `apps/cms/models.py:309` esige `caption_fr and credit and caption_place and caption_date`; `apps/cms/seeds_media.py:182` crea l'asset con
`is_decorative=False` e **non scrive nessuno dei quattro campi**. Il gate anti-stock funziona perfettamente: ha chiuso la porta su tutto, e nessuno se n'è
accorto.

**1.5 6,9 MB di peso morto, e una pipeline che non può produrre altro.** 73 file in `static/img/photos/`. Il
`Candidate` (`scripts/fetch_images.py:139`) non ha **nessun** campo didascalia. È costruita per produrre asset che il gate rifiuterà sempre: non una
configurazione sbagliata, un difetto di progetto.

**1.6 Nessun AVIF nella libreria, e peso fuori budget.** `ls static/img/photos/*.avif` → niente. `MAX_BYTES =
350*1024` (riga 111) contro un budget di **120 KB per viewport**: tarato quasi tre volte sopra il proprio limite. `bibliotheque-savoir-1440.webp` = 345 138 B.
Di passaggio, misurato in questo round e **fuori** da questa superficie: `static/brand/v2/doorway-1200.avif` pesa **123 932 B**, cioè da solo supera il tetto
per viewport; è la lastra della porta, e la annoto per `hero-doorway`.

**1.7 Quattro `<figure>` senza `<figcaption>` latenti** (il round 1 ne contava tre e ne mancava una):
`ecosystem/partials/photo.html:7` emette un `<figure>` **senza mai** didascalia; `news/detail.html:47` e `forum/partials/permanent_sections.html:39` la mettono
sotto `{% if %}`; e **`forum/partials/hero.html:33`** emette `<figure class="forum-hero__figure">` con l'URL MEDIA grezzo, senza didascalia, senza srcset e
senza alcun gate. Il test `ecosystem/tests/test_browser.py:98` asserisce `figures == captions`: passa solo perché `ForumMedia.objects.count()==0` e nessuna foto
esce. Peggio: `ecosystem.services.Photo` (riga 179) **non ha affatto** `place/date/caption/credit`.

**1.8 Nessun regime dichiarato.** `grep -rn "data-mode" templates/ apps/` → zero occorrenze, benché
DESIGN_SYSTEM_V2 § 7 dica «Ogni template dichiara `data-mode`; un test lo verifica». **Questa superficie non se ne appropria**: `backgrounds` lo ha già preso
in carico su `<body>` con `{% block page_mode %}` in `base.html` (docs/design-v3/specs/backgrounds.md § 208). Qui lo si **consuma** (§ 4.3).

**1.9 Una sola anteprima social per tutto il progetto:** `og:image = /static/img/og-default.png` ovunque.

**1.10 `sizes` mente sul riquadro reale, in tutte e tre le fasce.** Ri-misurato a dieci larghezze:
`pages/home/_hero.html` dichiara `(max-width: 47.999rem) 220px, (max-width: 63.999rem) 300px, 380px`; il riquadro misurato è **189** sotto 48rem (−14,1 % del
dichiarato), **316** fra 48 e 64rem (+5,3 %) e **401** sopra (+5,5 %).

**1.11 La dottrina è scritta nel codice:** `templates/components/hero.html:8` dice «The hero is type-led: no
photography», il registro editoriale-severo rifiutato dal committente, scolpito in un commento di template.

---

## 2. UI-UX-PRO-MAX — sette interrogazioni

| # | Query (esatta) | Dom. | Output (condensato) | Esito |
|---|---|---|---|---|
| 1 | `editorial photography art direction hero image treatment overlay premium` | style | `vintage-analog-retro-film` (grana, light leak, `filter: sepia() saturate(.8)`), `pixel-art`, `aurora-ui` | **RIFIUTATO.** Tre stili d'intrattenimento; il `filter` viola il divieto di filter-loop. Il DB di stili non copre la fotografia editoriale istituzionale: lo dichiaro invece di ripiegare su un default. |
| 2 | `responsive images srcset focal point cropping aspect ratio performance LCP` | ux | `max-width:100%`, «srcset con più misure», «alt descrittivo» | **ACCETTATO in parte.** Conferma ciò che già facciamo. Nessuna risposta su punto focale, crop art-directed, CLS o LCP: coperti in § 4.5 e § 7. |
| 3 | `duotone image treatment brand color overlay text contrast on photography` | color | Palette «Photography Studio» (nero puro), «Digital Signage», «Government/Public Service» (#0F172A, accent #0369A1) | **RIFIUTATO.** Restituisce palette di prodotto, non un trattamento d'immagine; la palette «Government» è il grigio-blu generico e cancellerebbe `--mid-1` e `--accent`. |
| 4 | `scroll linked image reveal clip-path mask parallax` | gsap | Parallax Subtle (`yPercent` 5–15, scrub), max 3–4 strati, Scroll Reveal y 8–16 px | **RIFIUTATO in round 2.** Il round 1 l'aveva adottato come M-IMG-2 e il revisore ha avuto ragione due volte: il budget § 4 di MOTION_SYSTEM era già speso dalla home, e 24 px di deriva su una banda 21:9 sono il segnale «premium a poco prezzo» più copiato del web. Rimosso, non sostituito. |
| 5 | `government institutional website photography imagery trust credibility` | ux | **0 risultati** — «did not hit the database» | **NESSUNA CORRISPONDENZA**, dichiarata come lo strumento richiede. La domanda centrale di questa superficie non è nel suo database. |
| 6 | `premium editorial photography system for an institutional legal platform, image slots, captions, credits` | `--design-system` | Pattern *Scroll-Triggered Storytelling*; stile *Motion-Driven*; palette nero puro; Inter via **Google Fonts**; **AVOID: «Heavy text + Poor image showcase»** | **ACCETTATO su un punto.** L'«AVOID» è la diagnosi del § 1 scritta dallo strumento stesso. Adottato il pattern a capitoli. Rifiutati: palette, Inter via CDN (CSP `style-src 'self'`; F24 vieta `fonts.googleapis[.]com`), «parallax 3–5 strati». |
| 7 | `image gallery grid editorial cards with captions and credits` | product | «Museum/Gallery»: *Minimalism & Swiss + Motion-Driven*, *Storytelling-Driven*, «Art-appropriate neutrals + Exhibition accents» | **ACCETTATO come registro.** Il museo è il riferimento giusto: la foto è un **oggetto esposto con cartellino**, non un fondale. È la base della «lastra» — e, in questo round, della decisione che il cartellino sia una **superficie fisica** e non del testo appoggiato sulla fotografia. |

**Dove lo strumento ha torto, e lo dico.** Il suo bias di default («government = accessible & ethical, avoid
motion effects») è il registro respinto dal committente. Qui produce due errori: (a) tratta la fotografia come rischio d'accessibilità invece che come
portatrice di credibilità — ma un sito che parla di **persone** e non ne mostra nessuna non è sobrio, è **vuoto**; (b) confonde quantità e qualità. La risposta
corretta non è «meno immagini»: è **poche lastre, trattate come documenti**.

---

## 3. 21ST.DEV — otto candidati

Nessuno installato; nessun `generate`/`iterate_generation`. `get_component` usato su 2 (27093, 20029).

| # | Componente / URL | Cosa prendo **dopo il round 2** | Cosa rifiuto, e perché |
|---|---|---|---|
| 1 | **Filmstrip Gallery** `21st.dev/@n1m4mz/components/filmstrip-gallery` | Solo due cose: `scroll-snap` su un binario, e `eager` sui primi fotogrammi. | Tutto il resto. La firma «negativo 35 mm» anima sei `filter` per 520 ms: vietato. Ma rifiuto anche ciò che il round 1 aveva preso: il `<dialog>`, `aria-current`, la live-region al `scrollend`. **Un binario non ha un elemento corrente**: `aria-current` su una striscia è un vezzo da carosello, e un lightbox dice «la vera foto è altrove», che è l'opposto di «poche, grandi, incise». E rifiuto il vezzo «35MM · ISO 400»: su una piattaforma legale è costume, non credibilità — motivo per cui in questo round **ho tolto anche il mio folio** (§ 4.4). |
| 2 | **Picture** `21st.dev/@shoota/components/picture` | Il primitivo `<figure>`+`<img>`+`<figcaption>` come **unico** modo di scrivere una foto: il contratto imposto dalla forma anziché dalla disciplina. | `opacity-60 grayscale` a riposo: nasconde la cattiva fotografia invece di curarla; su touch e tastiera il colore non esiste. Didascalia a 12 px bold **sovrapposta al soggetto**. |
| 3 | **Reveal Image Mask** `21st.dev/@daiwiikharihar/components/reveal-image-mask` | **Niente, in round 2.** L'idea (la foto che sboccia da una maschera) era diventata l'otturatore, e l'otturatore era (a) il default Framer 2026 e (b) un pannello opaco che senza JS nascondeva la fotografia. La maschera resta, ma è applicata al **cartellino**, non all'immagine. | Anima `clip-path` in scrub continuo: ridipinge ogni frame. |
| 4 | **Editorial Image Hero** `21st.dev/@felipemenezes098/components/hero-07` | La proporzione: banda panoramica a piena larghezza, testo **fuori** da essa. | Il nostro hero è deciso (porta + territorio) e non si tocca: la banda piena è un capitolo **interno**. |
| 5 | **Editorial Collage Hero** `21st.dev/@felipemenezes098/components/hero-04` | Niente. | Due foto che si tagliano a vicenda sono due crop sbagliati; e quale cartellino per un collage? |
| 6 | **Zoom Parallax** `21st.dev/@efferd/components/zoom-parallax` | **Niente, in round 2.** | Sequestra lo scroll, moltiplica i layer. Il round 1 l'aveva ridotto a 24 px di deriva: anche quella è caduta (§ 5). |
| 7 | **Scroll Portrait Wall** `21st.dev/@ruixen.ui/components/scroll-portrait-wall` | Il **4:5** come formato della persona, e il ritratto come unità. | `mix-blend-exclusion` sul titolo sticky e scrub da `scale 0`: contenuto invisibile. |
| 8 | **Grainient Images Section** `21st.dev/@httpsdesign-layercomja/components/grainient-images-section` | Il ritmo: l'oggetto prima, la sua etichetta dopo — la gerarchia è nel tempo. È l'unico principio sopravvissuto al round 2, e sta in M-IMG-1. | Gradient tiles + grana: decorazione senza funzione. |

**Pattern estratto:** `<figure>` obbligatorio (2) + binario a snap (1) + banda panoramica come capitolo (4) +
verticale 4:5 per la persona (7) + l'oggetto prima, l'etichetta dopo (8). Tutto ri-scritto in Django e nei nostri token. Nessun React, nessun pacchetto, e —
dopo il round 2 — **nessuna animazione presa in prestito**.

---

## 4. LA PROPOSTA — **LA LASTRA**

### 4.1 Principio, in quattro regole

Una fotografia qui non è un'illustrazione né un fondale: è una **lastra da stampa** — un oggetto con un formato, un cartellino e un autore. Poche, grandi,
incise: è così che fotografie di autori diversi leggono come **una sola commissione**.

1. **La gradazione è cotta nel derivato, mai calcolata dal browser.** Nessun `filter`, nessun `mix-blend-mode`,
   nessun gradiente a runtime: paint zero, resa identica su ogni motore, `forced-colors` senza casi speciali. *Il round 1 violava la propria regola*: lo scrim
   era un gradiente calcolato dal browser. È stato cancellato.
2. **Il taglio è deciso, non indovinato.** Tre rapporti in tutto il sistema, e la pipeline emette il crop duro in
   quel rapporto: `object-fit: cover` non deve mai scegliere.
3. **Senza cartellino la lastra non esiste.** Il gate `is_publishable` resta, intatto: lo si **riempie**, non lo si
   aggira. Chi non può riempirlo non entra — ed è questo che, in § 4.9, costa alla proposta quattordici fotografie.
4. **Nulla è mai stampato sopra una fotografia, e la fotografia non si muove mai.** Nessun testo, nessun titolo
   bloccato, nessun logo autorizzato, nessuna rotta SVG, nessuna scala, nessuna deriva, nessun otturatore. Un testo che sta *dentro* la banda sta su una
   **superficie opaca propria**, e il suo contrasto è quello di quella superficie, non della fotografia sotto. Questa è la regola che chiude, insieme, il
   MUST-FIX 5 (contrasto sullo scrim), il 13 (i loghi del Forum), il 14 (lo strato grafico del pilota) e i segnali «cheap» 1, 2, 3, 4 e 6.

### 4.2 Gradazione — perché **non** duotone

Il duotone è la scorciatoia che fa sembrare stock ciò che è stock, e su quattro locali distrugge gli incarnati: una piattaforma che parla di persone marocchine
e italiane non può virare la pelle in teal. **Gradazione, non duotone**: desaturazione parziale, nero portato sul nostro nero, alte luci rullate sul nostro
bianco — la pelle resta pelle, la tavolozza diventa la nostra.

Due gradazioni per master, **costanti della pipeline** (`scripts/fetch_images.py`, dict `GRADES`) — **non** token CSS: il round 1 dichiarava `--plate-ink` e
`--plate-paper` su `:root` e non li usava in nessuna regola. Sono stati tolti dal CSS.

| Grado | Saturazione | Nero | Bianco | Luminanza | Usato su |
|---|---|---|---|---|---|
| `-lume` | 0,78 | `#15222a` | `#f4f3f0` | 1,00 | lastre su fondo minerale (via, attualità, provino) |
| `-notte` | 0,66 | `#0b171e` | `#c8d4d6` | 0,94 | lastre dentro un capitolo mezzanotte (capitolo) |

Saturazione **mai sotto 0,66**: sotto quella soglia è duotone di fatto. (Il round 1 scriveva «desaturazione a 0,72» in prosa, «0,78/0,66» in tabella e
«desaturazione ≤ 0,34» in § 8: tre numeri per una cosa sola. Restano i due della tabella.) **Tutte le pesature del § 4.6 e del § 7 sono state misurate su
derivati gradati esattamente con queste costanti**, non su master grezzi.

### 4.3 Quattro slot, **tre rapporti**, e chi non ha diritto a un'immagine

Il revisore ha ragione: cinque rapporti sono copertura, non convinzione. Tre, e ciascuno significa una cosa.

| Rapporto | Che cosa è | Slot | Classe | Dove | Grado | Per pagina |
|---|---|---|---|---|---|---|
| **21:9** | il territorio, la sala | Capitolo | `.plate--chapter` | home (capitolo cooperazione), Forum pubblico (sotto l'intestazione) | `-notte` | **1** |
| **4:5** | la persona, il lavoro | Via | `.plate--route` | le quattro landing d'ecosistema (`companies`, `institutions`, `universities`, `pilot`) | `-lume` | 1 |
| **3:2** | il documento, il fatto datato | Attualità | `.plate--news` | `news/detail` **solo** (DEROGA 1) | `-lume` | 1 |
| **3:2** | la stessa cosa, in serie | Provino | `.plate--film` in `.plate-strip` | galleria Forum (`forum-media`) | `-lume` | 1 binario |

**Regime (§ 7 del design system), verificato sul `data-mode` che `backgrounds` scrive su `<body>`:**

| `data-mode` | Lastre ammesse in `<main>` | Test |
|---|---|---|
| `immersive` | ≤ 2 (`chapter` + `route`, oppure `chapter` + il binario) | conta `main .plate` per modo |
| `rich` | ≤ 1 | idem |
| `standard` | **0**, tranne la rotta `news:detail` dove è ≤ 1 (DEROGA 1) | idem, con l'eccezione nominata per rotta |
| `dense`, `legal` | **0** | idem |

**Superfici che NON prendono immagini, mai:** fascicolo, documenti, scadenze, messaggi, code di back-office
(DENSE); note legali, privacy, avvertenze anti-frode (LEGAL); FAQ, glossario e **l'indice** `/actualites/` (STANDARD). E, per decisione di questo round e non
per omissione: **`le-projet`, `agami`, `réseau` e le pagine d'autenticazione**. Le prime tre sono informative — regola § 6, nessuna deroga chiesta per tre
pagine che non ne hanno bisogno. L'autenticazione la vieta il design system con parole proprie: § 8.8, «la grammatica della porta (arco tracciato, gradini,
**nessuna fotografia**)». Il round 1 ci aveva messo un `.plate--seal` con gradazione mezzanotte: era una violazione di una clausola esplicita, ed è caduta
insieme al rapporto 4:3 e al rapporto 16:9.

**Dove va la banda, esattamente** (è il punto su cui il round 1 ha sbagliato tre volte):
* **Home** — la banda 21:9 **apre** il capitolo mezzanotte del pilota, subito dopo `.section__header` e **prima** di `.voyage`. La rotta SVG, le rive
  Maroc/Vénétie, la sequenza bloccata e la nota giuridica restano sul fondo piatto `--mid-1`, dove `--terr-line` è verificata a **6,07:1**. Nessuna linea,
  nessuna etichetta, nessuna parola legalmente portante tocca la fotografia. Il capitolo resta **uno**: la banda è un oggetto dentro di esso, non un secondo
  capitolo (`.chapter--dark` invariato: il test dei capitoli conta le sezioni, non le lastre).
* **Forum** — la banda va **dopo** `forum-hero__inner`, a piena larghezza, dentro lo stesso fondo. I testi bloccati (`header.title/subtitle/meta/patronage`) e
  i loghi autorizzati (gate G6) restano dove sono, su fondo pieno. La `<figure class="forum-hero__figure">` senza didascalia di `hero.html:33` viene
  **rimossa**: la banda la sostituisce, con il suo cartellino.

### 4.4 Markup

**`templates/components/plate.html` (nuovo) — l'unico modo di scrivere una foto.** Non si include a mano: si
chiama con il tag `{% plate %}`, che è ciò che garantisce che `sizes` non sia mai vuoto (era il difetto 7 della revisione).

```django
{% load i18n %}{% comment %}
Contratto — `photo`: pages.services.Photo. `variant`: chapter|route|news|film. `sizes`: fornito dal
tag {% plate %} a partire dal variant, mai scritto a mano, mai vuoto. `priority`: una sola per pagina.
`photo` None → non si stampa nulla. Una <figure> senza <figcaption> è qui impossibile.

MAI `data-reveal` su questo elemento: shell.js:34 anima OGNI [data-reveal] di OGNI pagina, e la
lastra ha il suo unico reveal (M-IMG-1). tests/frontend/test_plate.py asserisce
count("[data-plate][data-reveal]") == 0 su tutte le rotte pubbliche.
{% endcomment %}
{% if photo %}
<figure class="plate plate--{{ variant }}" data-plate{% if priority %} data-priority{% endif %}>
  <div class="plate__frame">
    {% if photo.media == 'video' %}
      <video class="plate__film" controls preload="metadata" src="{{ photo.src }}"
        {% if photo.poster %}poster="{{ photo.poster }}"{% endif %}></video>
    {% else %}
      <picture>
        {% if photo.avifset %}<source type="image/avif" srcset="{{ photo.avifset }}" sizes="{{ sizes }}">{% endif %}
        {% if photo.srcset %}<source type="image/webp" srcset="{{ photo.srcset }}" sizes="{{ sizes }}">{% endif %}
        <img class="plate__img plate__img--focus-{{ photo.focus|default:'c' }}" src="{{ photo.src }}"
          alt="{{ photo.alt }}"{% if photo.alt_lang %} lang="{{ photo.alt_lang }}"{% endif %}
          width="{{ photo.width }}" height="{{ photo.height }}" decoding="async"
          loading="{% if priority or eager %}eager{% else %}lazy{% endif %}"
          {% if priority %}fetchpriority="high"{% endif %}>
      </picture>
    {% endif %}
  </div>
  <figcaption class="plate__legend"><span class="plate__legend-in">
    <span class="plate__where">{{ photo.place }} · <time datetime="{{ photo.date|date:'Y-m-d' }}">{{ photo.date|date:'j F Y' }}</time></span>
    <span class="plate__said">{{ photo.caption }}</span>
    <span class="plate__credit">{{ photo.credit }}</span>
    {% if photo.kind == 'archetype' %}<span class="plate__kind">{% translate "Image d’archive : cette photographie ne représente pas des personnes du projet." %}</span>{% endif %}
  </span></figcaption>
</figure>
{% endif %}
```

**Il cartellino sta sempre SOTTO la lastra nel DOM, in tutte e quattro le varianti.** Non c'è più nessuna
contraddizione da sciogliere (difetto 6): sul solo capitolo il blocco **risale di 24 px dentro la banda** con un margine negativo, restando un rettangolo
opaco di livello 2. Nessun `position: absolute`, nessuna sovrapposizione al soggetto, nessuna dipendenza da `position: relative` sul contenitore.

**Il folio è stato tolto.** Il revisore ha ragione: `.plate__folio` era lo stesso costume che il § 3 #1 rifiuta a
un altro, con un altro carattere. Un numero che non risolve a un registro pubblico è un ornamento. Il riferimento di registro resta **nel dato**
(`license_notes`, `folio=…`) per la tracciabilità interna, e **non si stampa**. Il cartellino dice quattro cose vere e nient'altro: dove, quando, che cosa, di
chi.

**`templates/components/plate_strip.html` (nuovo) — il provino.**

```django
{% load i18n ile_core plate_tags %}{% comment %}
Un binario, non un carosello. Nessun elemento «corrente», nessun aria-current, nessun lightbox:
qui una fotografia è già alla misura che l'editore ha scelto. ←/→ sono del browser sul binario
focalizzabile (misurato: 0 → 438 px, una posizione di snap). Home/End NON lo sono (misurato: End
non muove l'asse inline) e stanno in plate.js.
Contratto: `plates` = lista di pages.services.Photo · `label` = nome accessibile del binario.
{% endcomment %}
{% if plates %}
<div class="plate-strip" data-plate-strip>
  <ul class="plate-strip__rail" role="list" tabindex="0" aria-label="{{ label }}">
    {% for photo in plates %}
      <li class="plate-strip__frame">
        {% if forloop.counter0 < 2 %}{% plate photo "film" eager=True %}{% else %}{% plate photo "film" %}{% endif %}
      </li>
    {% endfor %}
  </ul>
  <p class="plate-strip__controls">
    <button type="button" class="btn btn--icon plate-strip__btn" data-plate-step="-1"
      aria-label="{% translate "Image précédente" %}">{% svg_icon "arrow" "icon plate-strip__icon-prev" %}</button>
    <button type="button" class="btn btn--icon plate-strip__btn" data-plate-step="1"
      aria-label="{% translate "Image suivante" %}">{% svg_icon "arrow" "icon" %}</button>
  </p>
</div>
{% endif %}
```

`eager` (senza `fetchpriority`) sui primi due fotogrammi; tutti gli altri `lazy`. Un fotogramma scorrato fuori dal binario è fuori dal viewport per il browser
e non viene scaricato: è il meccanismo su cui poggia il censimento del § 7.

**Il tag** — `apps/pages/templatetags/plate_tags.py` (nuovo; `apps/pages` non ha ancora un pacchetto
`templatetags`):

```python
PLATE_SIZES = {
    "chapter": "100vw",
    "route":   "(min-width: 30rem) 420px, 100vw",
    "news":    "(min-width: 52rem) 720px, 100vw",
    "film":    "240px",
}

@register.inclusion_tag("components/plate.html")
def plate(photo, variant="route", *, priority=False, eager=False):
    if variant not in PLATE_SIZES:                       # un errore di battitura non deve
        raise TemplateSyntaxError(f"unknown plate variant {variant!r}")   # produrre sizes vuoto
    return {"photo": photo, "variant": variant, "sizes": PLATE_SIZES[variant],
            "priority": priority, "eager": eager}
```

**Perché `sizes` NON è un campo di `Photo`** (e il revisore chiedeva di metterlo lì): `sizes` è un fatto di
*layout*, non di *fotografia*. La stessa fotografia serve due slot con due riquadri diversi; metterla sull'oggetto significa che l'oggetto sa dove sarà
disegnato. Il tag risolve `sizes` dal `variant`, quindi **non può essere vuoto** — che era il difetto vero — e resta una sola definizione in tutto il
progetto. Il fallback silenzioso a `100vw` che distruggeva il censimento non è più possibile.

`100vw` nelle fasce basse sovra-dichiara della sola gutter del contenitore (40 px a 1440, 40 px a 390). **Verificato che non cambia un gradino**: a 390/DPR 3
la dichiarazione vera (350 px → 1 050) e `100vw` (390 px → 1 170) scelgono entrambe il gradino 1200w; a 768/DPR 2 (688 → 1 376 contro 768 → 1 536) scelgono
entrambe 1600w. La forma semplice costa zero byte ed è più facile da leggere.

### 4.5 `static/css/v3/plate.css` — il foglio, per intero

**Token nuovi: tre, e solo tre.** `--plate-ar-chapter: 21/9` · `--plate-ar-portrait: 4/5` ·
`--plate-ar-record: 3/2`. Nessun token si chiama `--route` (collideva con `--route-1..4` di `static/css/v2/tokens.css`). Nessun token di colore nuovo: la
lastra usa `--hairline`, `--hairline-dark`, `--hairline-dark-strong`, `--min-1`, `--mid-2`, `--mid-3`, `--ink-2`, `--ink-3`, `--on-dark`, `--on-dark-2` —
cioè il sistema com'è. **`--accent` non compare**: una lastra non è un controllo.

```css
:root{--plate-ar-chapter:21/9;--plate-ar-portrait:4/5;--plate-ar-record:3/2}

/* L'oggetto: una pagina di registro — una riga di margine, una cornice, un'etichetta. */
.plate{margin:0;display:grid;gap:var(--s-4);border-inline-start:1px solid var(--hairline);padding-inline-start:var(--s-4)}
.chapter--dark .plate{border-inline-start-color:var(--hairline-dark)}
.plate__frame{position:relative;overflow:hidden;border:1px solid var(--hairline);border-radius:var(--radius-control);background:var(--min-1)}
.chapter--dark .plate__frame{background:var(--mid-2);border-color:var(--hairline-dark)}
/* <picture> è display:inline; l'immagine è posizionata, quindi l'unica autorità di misura è
   l'aspect-ratio della cornice. Misurato: riquadro 1440×615 in una banda 1440×617. */
.plate__frame picture{display:block}
.plate__img,.plate__film{position:absolute;inset:0;display:block;inline-size:100%;block-size:100%;object-fit:cover}
.plate__film{object-fit:contain;background:var(--mid-1)}
.plate--chapter .plate__frame{aspect-ratio:var(--plate-ar-chapter)}
.plate--route .plate__frame{aspect-ratio:var(--plate-ar-portrait)}
.plate--news .plate__frame,.plate--film .plate__frame{aspect-ratio:var(--plate-ar-record)}
.plate--route{max-inline-size:420px} .plate--news{max-inline-size:720px}
/* aspect-ratio tiene la scatola definita anche sotto size containment: zero CLS. Misurato. */
.plate:not([data-priority]) .plate__frame{content-visibility:auto}

/* Punto focale: cinque celle quantizzate, nessuno style="" — CSP style-src 'self'. */
.plate__img--focus-c{object-position:50% 50%} .plate__img--focus-n{object-position:50% 22%}
.plate__img--focus-s{object-position:50% 78%} .plate__img--focus-is{object-position:24% 50%}
.plate__img--focus-ie{object-position:76% 50%}
[dir="rtl"] .plate__img--focus-is{object-position:76% 50%}
[dir="rtl"] .plate__img--focus-ie{object-position:24% 50%}

/* Il cartellino. `.plate__legend` è l'alloggiamento; `.plate__legend-in` è l'etichetta. */
.plate__legend{overflow:hidden}
.plate__legend-in{display:grid;gap:var(--s-1);--slide:-100%}
[dir="rtl"] .plate__legend-in{--slide:100%}
.plate__where,.plate__credit{margin:0;font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;font-variant-numeric:tabular-nums;color:var(--ink-3)}
.plate__said{margin:0;font-size:var(--t-small);line-height:var(--t-small-lh);color:var(--ink-2);max-inline-size:62ch}
.plate__kind{margin:0;font-size:var(--t-caption);line-height:var(--t-caption-lh);color:var(--ink-3)}
:lang(ar) .plate__where,:lang(ar) .plate__credit{letter-spacing:0;text-transform:none}
.chapter--dark .plate__where,.chapter--dark .plate__credit,.chapter--dark .plate__kind{color:var(--on-dark-2)}
.chapter--dark .plate__said{color:var(--on-dark)}

/* Il capitolo: banda a piena larghezza, l'etichetta che risale dentro di essa. */
.plate--chapter{display:block;border-inline-start:0;padding-inline-start:0;max-inline-size:none}
.plate--chapter .plate__frame{border-inline:0;border-radius:0}
.plate--chapter .plate__legend{position:relative;z-index:1;margin-block-start:calc(var(--s-6) * -1);
  margin-inline:var(--s-10);max-inline-size:46ch}
.plate--chapter .plate__legend-in{padding:var(--s-5) var(--s-6);background:var(--mid-3);
  border:1px solid var(--hairline-dark-strong);border-radius:var(--radius-control)}
@media (max-width:47.999rem){
  .plate--chapter .plate__legend{margin-block-start:calc(var(--s-4) * -1);margin-inline:var(--s-4)}
  .plate--chapter .plate__legend-in{padding:var(--s-4)}}

/* M-IMG-1 · l'etichetta entra nel suo alloggiamento (GERARCHIA).
   Nessun JS interpola: plate.js aggiunge solo .is-in. Senza JS la regola non si applica mai e
   l'etichetta è già a posto — lo stato senza JS È lo stato finale, come hero.css:473 e voyage.css:235. */
@media (prefers-reduced-motion:no-preference){
  .plate__legend-in{transition:transform var(--motion-base) var(--ease-out) 60ms}
  html.js .plate[data-plate]:not(.is-in) .plate__legend-in{transform:translateX(var(--slide))}}

/* Il provino: un binario. */
.plate-strip{display:grid;gap:var(--s-4);max-inline-size:1000px}
.plate-strip__rail{margin:0;padding-block-end:var(--s-2);padding-inline:0;list-style:none;display:grid;
  grid-auto-flow:column;grid-auto-columns:240px;gap:var(--s-6);overflow-x:auto;
  overscroll-behavior-inline:contain;scroll-snap-type:x mandatory;scroll-padding-inline-start:var(--s-1)}
.plate-strip__frame{scroll-snap-align:start}
.plate-strip__controls{display:flex;gap:var(--s-2);justify-content:flex-end}
.plate-strip__btn{min-inline-size:44px;min-block-size:44px}
/* «précédente» riusa la freccia in avanti, specchiata in LTR soltanto — è il pattern già in casa
   di .pagination__icon-prev (static/css/components.css:2573). */
.plate-strip__icon-prev{transform:scaleX(-1)}
[dir="rtl"] .plate-strip__icon-prev{transform:none}

/* forced-colors: l'etichetta smette di sovrapporsi e prende i colori di sistema. */
@media (forced-colors:active){
  .plate__frame{border:1px solid CanvasText} .plate{border-inline-start-color:CanvasText}
  .plate--chapter .plate__legend{margin-block-start:0}
  .plate--chapter .plate__legend-in{background:Canvas;border-color:CanvasText}
  .plate__where,.plate__credit,.plate__said,.plate__kind,
  .chapter--dark .plate__where,.chapter--dark .plate__credit,
  .chapter--dark .plate__said,.chapter--dark .plate__kind{color:CanvasText}}
```

**Verifiche sul file, non sulle intenzioni** (eseguite sul foglio senza commenti):
`box-shadow` **0** · `filter` **0** · `mix-blend` **0** · `gradient` **0** · `!important` **0** · proprietà fisiche (`margin-left/right/top/bottom`,
`padding-left/right`, `left:`, `right:`, `border-left/right`) **0**. La cornice è un `border`, quindi il `grep box-shadow` del DESIGN_SYSTEM_V2 § 2 continua a
restituire **solo i quattro ruoli** — il round 1 ne avrebbe aggiunto un quinto senza accorgersene.

**Stati.** Una lastra non è un controllo; esiste come controllo solo quando è dentro un `<a>` (slot Via).
* *riposo* — gradazione cotta, cornice 1 px, riga di margine. È lo stato definitivo.
* *hover* — **nessuno sulla lastra.** Il pannello di via ha già la sua «linea d'ormeggio» (§ 8.5 del design system) e il suo livello 2: quella è la risposta al
  puntatore, e basta una. Il round 1 metteva `scale(1.02)` sull'immagine — il gesto di default di ogni libreria di componenti, e per di più un'animazione di
  `box-shadow` sulla cornice.
* *focus-visible* — anello 2 px `--accent-ring` + alone 3 px al 30 % **sul link**, mai sull'immagine. **Puntatore e tastiera ricevono ora esattamente la stessa
  risposta**: era il segnale «cheap» 8 della revisione, e si chiude togliendo il gesto al mouse, non aggiungendone uno alla tastiera.
* *active* — `translateY(1px)` sul link (§ 10), 120 ms. Invariato.
* *disabled* — non esiste. *loading* — la cornice su `--min-1` con la sola `aspect-ratio`: nessuno skeleton animato, zero CLS, zero loop.
* *errore* (derivato mancante) — `photo` è `None`, il partial non stampa nulla, la pagina resta corretta.

### 4.6 Le misure — tutte rifatte in questo round

Browser: Chromium headless del `.venv`, su `127.0.0.1:8771`, foglio candidato servito come `<link>` same-origin.

**A · Contrasti, calcolati (luminanza relativa WCAG 2.x), non stimati.**

| Testo | Su | Rapporto | Dove serve |
|---|---|---:|---|
| `--on-dark` `#eef2f1` | `--mid-3` (cartellino di capitolo) | **12,29:1** | la frase del cartellino sul capitolo |
| `--on-dark-2` `#b7c3c4` | `--mid-3` | **7,67:1** | luogo/data e credito sul capitolo (mono 13 px → richiede 4,5:1) |
| `--on-dark-3` `#8fa0a3` | `--mid-3` | 5,10:1 | **non usato**: resta vietato sulla lastra |
| `--ink-3` `#55646b` | `--min-0` | **5,53:1** | luogo/data e credito su fondo minerale |
| `--ink-2` `#4a5a62` | `--min-0` | **6,46:1** | la frase del cartellino su fondo minerale |
| `--ink-3` | `--min-2` | 5,88:1 | idem su foglio |
| `--terr-line` `#3fa6af` | `--mid-1` | 6,07:1 | la rotta del pilota, **sul fondo piatto**, non sulla fotografia |

E la misura che rende il cartellino sicuro per costruzione: **`--mid-3` contro il nero estremo di un derivato
`-notte` (`#0b171e`) = 1,31:1; contro il suo bianco estremo (`#c8d4d6`) = 9,14:1.** Cioè il cartellino non «sparisce» nel punto più scuro possibile della
fotografia solo in virtù del colore — e infatti **non** dipende dal colore: è un rettangolo opaco con un bordo `--hairline-dark-strong`, e il contrasto del suo
testo è quello del suo fondo, sempre, qualunque fotografia ci sia sotto. È tutta la differenza fra questo round e il precedente.

**B · Lo scrim del round 1, letto dai pixel renderizzati** (fotogramma bianco puro sotto
`linear-gradient(to bottom, transparent 38%, rgba(14,27,35,.82) 100%)`, screenshot a DPR 1, lettura del pixel al centro colonna):

| Posizione lungo la corsa | Composito misurato | `--on-dark` | `--on-dark-2` |
|---|---|---:|---:|
| 100 % (ultima riga) | `rgb(58,68,75)` | 8,83:1 ✅ | 5,51:1 ✅ |
| 90 % | `rgb(90,99,104)` | 5,44:1 ✅ | **3,40:1** ❌ |
| 82 % | `rgb(115,123,128)` | 3,82:1 ❌ | **2,38:1** ❌ |
| 75 % | `rgb(137,143,147)` | 2,90:1 ❌ | **1,81:1** ❌ |
| 68 % | `rgb(160,165,168)` | 2,20:1 ❌ | **1,38:1** ❌ |
| 60 % | `rgb(185,189,191)` | 1,68:1 ❌ | **1,05:1** ❌ |

Le due cifre dichiarate dal round 1 (8,85 e 5,52) sono confermate **per la sola ultima riga di pixel** (misurate 8,83 e 5,51). Il revisore ha ragione; le sue
cifre (4,29 e 3,35) sono i compositi **all'opacità** 0,75 e 0,68, che cadono al 94,7 % e all'89,4 % della corsa. **Al 75 % della corsa il valore vero è
1,81:1.** Un cartellino di cinque righe su quel gradiente non era «al limite»: era fuori di tre volte. Lo scrim è stato cancellato, non corretto.

**C · Geometria, sul sito vivo, con il foglio candidato caricato.**

| Misura | 1440×900 DPR 1 | 390×844 DPR 3 |
|---|---|---|
| banda `.plate--chapter .plate__frame` | 1440 × 617 px, rapporto **2,333** (= 21/9) | 390 × 167, rapporto 2,333 |
| cartellino `.plate__legend` | 334 × 122 | 334 × 122 |
| risalita dentro la banda | **24 px** | 16 px |
| **area del cartellino sulla banda** | **0,90 %** | **8,19 %** |
| **a zoom testo 200 %** (root 32 px) | cartellino 334 × **378**, risalita **24 px invariata**, area **0,90 %** | cartellino 334 × 378, risalita 16 px, area **8,19 %** |
| immagine dentro la cornice | 1440 × 615, `objectFitEngaged: true`, `picture{display:block}` | 390 × 165, idem |
| `content-visibility` sulla lastra `data-priority` | **`visible`** | `visible` |
| `content-visibility` su una lastra sotto la piega | **`auto`**, cornice 687 × 458, rapporto **1,500** | — |

Il test del revisore («il cartellino del capitolo non copre mai più del 40 % della banda») passa con **0,90 %** a desktop e **8,19 %** a telefono, e —
questo è il punto — **non cambia a zoom 200 %**, perché la scheda cresce verso il basso, fuori dalla banda, mai dentro. Non è una fortuna: è la ragione per
cui il cartellino è un margine negativo e non un `position: absolute`.

**D · Quale gradino di `srcset` sceglie davvero Chromium** (scala 480/800/1200/1600/2000, URL distinti per
disambiguare 1600 da 2000):

| Slot | `sizes` | 1440 DPR 1 | 1440 DPR 2 | 1920 DPR 2 | 390 DPR 3 |
|---|---|---|---|---|---|
| Capitolo | `100vw` | 1600w | **2000w** | 2000w | 1200w |
| Via | `(min-width: 30rem) 420px, 100vw` | 480w | 1200w | — | 1200w |
| Attualità | `(min-width: 52rem) 720px, 100vw` | 800w | 1600w | — | 1200w |
| Provino | `240px` | 480w | 480w | — | 800w |

È il numero che il round 1 non aveva mai calcolato: **a 1440 con DPR 2 la banda a piena larghezza scarica il
gradino 2000w**, quello che il tetto «fino a 1600 px» lasciava scoperto.

**E · Pesature reali** (Pillow 12.3, AVIF e WebP, su tre master fotografici del repository —
`arch-photo-original-2400.jpg`, `campus-universitaire-1920.webp` e `bibliotheque-savoir-1920.webp`, il caso patologico: scaffali di libri — ritagliati nei tre
rapporti e **gradati con le costanti del § 4.2**). Scala di qualità AVIF 52/52/45/45/40 e WebP 72/68/62 per 480/800/1200/(1600)/(2000). **Peggiore** delle
diciotto combinazioni per gradino:

| Gradino | AVIF peggiore | WebP peggiore | Tetto per derivato |
|---|---:|---:|---|
| 480w | 28,2 KB | 43,0 KB | **105 KB** |
| 800w | 65,1 KB | 87,2 KB | 105 KB |
| 1200w | 99,7 KB (4:5) | 149,5 KB (4:5) → **non emesso** | 105 KB |
| 1600w | 96,7 KB | — (scala WebP ferma a 1200) | 105 KB |
| 2000w | 75,6 KB | — | 105 KB |

**F · Tastiera sul binario.** Binario `tabindex="0"`, `scroll-snap-type: x mandatory`, fotogrammi da 420 px con
gutter 24 px: `ArrowRight` avanza di una posizione di snap (misurato `scrollLeft` 0 → **438**). `End` **non** muove l'asse inline (misurato: 438 → 444, cioè il
solo riassestamento dello snap), e `Home` nemmeno. Quindi ←/→ sono del browser e **Home/End sono scritti in `plate.js`** — cinque righe, e la revisione non
deve più credermi sulla parola.

**G · Peso del codice, misurato.** `plate.css`: **4 164 B** minificato, **1 240 B gzip**. `plate.js` compilato
con l'esbuild del progetto (`bundle`, `format:esm`, `target:es2022`, `minify`): **946 B**, **541 B gzip**. Il round 1 stimava «≈ 2,1 KB gzip» per il JS: il
valore vero è **un quarto**, perché questo modulo **non importa Motion** — non interpola niente, aggiunge una classe e sposta uno `scrollLeft`.

**H · RTL su `/ar/`** (`dir="rtl"` reale, foglio candidato caricato): `border-left: 0px` / `border-right: 1px`,
`padding-left: 0px` / `padding-right: 16px`, `object-position: 76% 50%` per `focus-is` (specchiata), `--slide: 100%`. Nessuna proprietà fisica, nessun
aggiustamento manuale.

**I · L'oggetto in più sulla pagina.** Con la banda inserita, la home passa da **7 921 px a 8 638 px** a 1440 e
da 11 183 a **11 458** a 390 (misurato). La superficie fotografica passa da 107 067 px² a **995 547 px²**, cioè da **0,94 % a 8,00 %** dell'area di pagina a
1440 (×8,5), e da 0,55 % a **1,99 %** a 390 (×3,6). È questa la risposta al «non abbastanza dinamico», non un'animazione in più: **il committente scorre otto
schermate senza incontrare una superficie fotografica, e dopo questa superficie ne incontra una alta 617 px.**

### 4.7 Template toccati, e il cablaggio per intero

**Nuovi** — `templates/components/plate.html` · `templates/components/plate_strip.html` ·
`apps/pages/templatetags/__init__.py` + `plate_tags.py` · `static/css/v3/plate.css` · `static/js/src/plate.js`.

**Riscritti**
* `templates/ecosystem/partials/photo.html` → `{% plate photo "route" priority=True %}` (chiude il primo dei quattro difetti del § 1.7).
* `templates/ecosystem/{companies,institutions,universities,pilot}.html` — due righe ciascuno: l'include della foto e quello del `blockquote` vengono avvolti
  in `<div class="plate-pair"> … </div>`, così la lastra 4:5 (420 px max) e la citazione prescritta stanno affiancate invece di lasciare 524 px di colonna
  vuoti accanto a un ritratto. `.plate-pair{display:grid;grid-template-columns:minmax(0,420px) 1fr;gap:var(--s-12)}` e colonna unica sotto 64rem —
  **tre righe in `apps/ecosystem/static/ecosystem/ecosystem.css`** (il foglio che `_layout.html:13` carica già), **non in `plate.css`**: è composizione di
  pagina, non anatomia della lastra.
* `templates/pages/home/_pilot.html` — la banda 21:9 dopo `.section__header`, **prima** di `.voyage`. La rotta non cambia di una riga.
* `templates/forum/partials/hero.html` — la `<figure class="forum-hero__figure">` senza didascalia (riga 33) è **rimossa**; la banda `.plate--chapter` va
  dopo `forum-hero__inner`, dentro lo stesso fondo, con i testi bloccati e i loghi intatti sopra di essa.
* `templates/forum/partials/permanent_sections.html` — la sezione `forum-media` chiama `plate_strip.html`; la `<figure>` condizionale e i due rami
  `video`/`img` spariscono dentro il contratto della lastra.
* `templates/news/detail.html` — le righe 47–52 diventano `{% plate hero_photo "news" priority=True %}`.
* `templates/pages/home/_hero.html` — **solo `sizes`**, con i tre valori ri-misurati (§ 1.10):
  `(max-width: 47.999rem) 190px, (max-width: 63.999rem) 320px, 400px`. Se `hero-doorway` rivendica la riga, la prenda: qui resta la misura.

**Cancellati** — `templates/pages/partials/_picture.html` e i suoi **tre** chiamanti reali
(`pages/agami.html:20`, `pages/network.html:18`, `pages/project.html:21`): quelle pagine non prendono più una lastra (§ 4.3).

**Cablaggio, per esteso** (era la lacuna 11):
1. `static/css/main.css` — una riga, dopo `@import url("v3/buttons.css");`: `@import url("v3/plate.css");`
2. `templates/base.html` — un preload nella lista delle righe 26–38, dopo quello di `v3/buttons.css`:
   `<link rel="preload" href="{% static 'css/v3/plate.css' %}" as="style">`
3. `static/js/src/plate.js` — nuovo file di primo livello: `scripts/build_frontend.mjs` prende **automaticamente** ogni `*.js` di `static/js/src/` come
   entry point (righe 30–33), quindi non c'è configurazione da scrivere; l'output è `static/js/dist/plate.js` e va committato (il dist è versionato, e
   `tests/frontend/test_frontend_bundle_is_current.py` rifiuta un dist più vecchio dei sorgenti).
4. Caricamento — `<script type="module" src="{% static 'js/dist/plate.js' %}"></script>` nel blocco `{% block extra_scripts %}` delle **quattro** sole
   pagine che portano una lastra: `pages/home.html`, `ecosystem/_layout.html`, `forum/index.html`, `news/detail.html`. Non in `base.html`: 442 B su cinquanta
   pagine che non hanno lastre sono 442 B sprecati cinquanta volte.
5. **Collisione con `shell.js`, risolta togliendo, non aggiungendo** — `static/js/src/shell.js:34` fa
   `document.querySelectorAll("[data-reveal]")` su **ogni** pagina (`base.html:70`). La lastra **non porta `data-reveal`** e non è mai figlia diretta di un
   elemento che lo porta: il suo unico reveal è M-IMG-1, che è una `transition` CSS. Il round 1 le avrebbe date tre animazioni sovrapposte (shell.js +
   otturatore + cartellino). Test: `count("[data-plate][data-reveal]") == 0` su tutte le rotte pubbliche.

**`static/js/src/plate.js` — il modulo per intero** (721 B minificato; non importa Motion):

```js
/**
 * La lastra. Due compiti, nessuna libreria di animazione: il CSS possiede il moto, questo file
 * dice soltanto QUANDO.
 *   [data-plate]        .is-in quando la lastra è al 25 % in vista → M-IMG-1 (GERARCHIA).
 *                       Senza JS la classe non arriva mai e l'etichetta è già a posto.
 *   [data-plate-strip]  i due bottoni scorrono il binario di un fotogramma; Home/End, che il
 *                       browser non dà sull'asse inline (misurato), sono qui.
 */
const plates = document.querySelectorAll("[data-plate]");
if (plates.length) {
  const seen = new IntersectionObserver((entries, obs) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add("is-in");
      obs.unobserve(entry.target);
    }
  }, { threshold: 0.25 });
  for (const plate of plates) seen.observe(plate);
}

for (const strip of document.querySelectorAll("[data-plate-strip]")) {
  const rail = strip.querySelector(".plate-strip__rail");
  if (!rail) continue;
  const smooth = () => (matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth");
  const frameStep = () => {
    const first = rail.firstElementChild;
    if (!first) return rail.clientWidth;
    return first.getBoundingClientRect().width + parseFloat(getComputedStyle(rail).columnGap) || 0;
  };
  for (const button of strip.querySelectorAll("[data-plate-step]")) {
    button.addEventListener("click", () => {
      rail.scrollBy({ left: frameStep() * Number(button.dataset.plateStep), behavior: smooth() });
    });
  }
  rail.addEventListener("keydown", (event) => {
    if (event.key !== "Home" && event.key !== "End") return;   // ← e → sono del browser
    event.preventDefault();
    const end = rail.scrollWidth - rail.clientWidth;
    const start = getComputedStyle(rail).direction === "rtl" ? -end : end;
    rail.scrollTo({ left: event.key === "End" ? start : 0, behavior: smooth() });
  });
}
```

### 4.8 Dati — una sola `Photo`, e i due percorsi che mancavano

**Una sola dataclass, in `apps/pages/services.py`.** `ecosystem.services.Photo` (riga 179) viene **cancellata**;
`ecosystem.services` importa questa. Era il difetto 7: due forme incompatibili trattate come una.

```python
@dataclass(frozen=True)
class Photo:
    src: str                    # il file di ripiego (JPG/WebP) o, per un video, il file media
    srcset: str = ""            # scala WebP ("" quando non ci sono derivati)
    avifset: str = ""           # scala AVIF
    alt: str = ""
    alt_lang: str = ""          # "" quando l'alternativa è nella lingua di pagina
    width: int = 0
    height: int = 0
    focus: str = "c"            # c | n | s | is | ie  → .plate__img--focus-*
    place: str = ""
    date: object = None
    caption: str = ""
    credit: str = ""
    kind: str = "document"      # document | archetype
    media: str = "image"        # image | video
    poster: str = ""            # poster del video, quando esiste un asset di libreria
    share_path: str = ""        # il JPG per og:image — era `share_image` in ecosystem
```

**Rinomine, e chi le paga:** `webp_srcset` → `srcset` · `share_image` → `share_path` · `PHOTO_SIZES`
(`apps/ecosystem/services.py:37`) **cancellata** (ora è `PLATE_SIZES` nel tag). Chiamanti da aggiornare, tutti e quattro noti:
`apps/ecosystem/services.py:446-447` (jsonld `data["image"] = photo.share_path`), `templates/ecosystem/partials/photo.html` (riscritto),
`apps/ecosystem/tests/test_services.py:158-160` e `:179`. `photo_for(space, lang)` diventa una riga:
`return photo_from_asset(space.hero_image, lang)` — la regola del gate vive in **un** punto, come
`tests/compliance/test_figure_caption.py` già dichiara nella sua intestazione.

`photo_from_asset` **rifiuta un asset `is_decorative`**: un'immagine decorativa non ha niente da catalogare, e un
cartellino vuoto è esattamente il difetto che questa superficie esiste per impedire. (La porta dell'hero non passa di qui: è un asset di marca in
`static/brand/v2/`, non un `MediaAsset`.)

**`news/detail` — il percorso dati che il round 1 negava.** Il round 1 scriveva «nessun cambio di vista»: era
falso. `templates/news/detail.html:49` stampa `article.hero_image.file.url`, cioè il file MEDIA grezzo, senza srcset e senza derivati; `apps/news/views.py:93`
passa solo `hero_alt`; `article.image_caption` è un `CharField` a parte. **La vista cambia**, in due righe:

```python
# apps/news/services.py
def hero_photo(article, lang: str) -> Photo | None:
    """La lastra dell'articolo. `image_caption` è la frase DELL'ARTICOLO sulla propria fotografia e
    vince sulla didascalia di libreria; luogo, data e credito restano dell'asset, sempre."""
    photo = photo_from_asset(article.hero_image, lang)
    return None if photo is None else replace(photo, caption=article.image_caption or photo.caption)

# apps/news/views.py, nel context del detail
"hero_photo": services.hero_photo(article, lang),
```

**Il provino del Forum — la mappatura che mancava.** `forum.ForumMedia` (`apps/forum/models.py:397`) porta
`caption`, `credit`, un `asset` opzionale e un `file` grezzo: **niente place, niente date**. Il round 1 rendeva la `figcaption` incondizionale su quel modello,
cioè produceva didascalie vuote — il difetto che indicava al § 1.7. La soluzione **non è un campo nuovo**: il luogo e la data di una fotografia del Forum sono
quelli **dell'evento**, che il modello ha già (`ForumEvent.venue`, `.city`, `.date`).

```python
# apps/forum/services.py
def plates_for(event, lang: str) -> list[Photo]:
    """Le righe media pubblicate, come lastre. Nessuna migrazione: place e date vengono dall'evento —
    una fotografia del Forum è stata scattata al Forum, e questo è un fatto, non una stima."""
    place = ", ".join(p for p in (event.venue, event.city) if p)      # « Sala della Gran Guardia, Rovigo »
    plates = []
    for media in event.media_items.live().select_related("asset"):
        if not (media.caption and media.credit):
            continue                                                  # senza cartellino non è una lastra
        base = photo_from_asset(media.asset, lang) if media.asset_id else None
        plates.append(replace(base or Photo(src=media.url),
                              place=place, date=event.date,
                              caption=media.caption, credit=media.credit,
                              media="video" if media.kind == MediaKind.VIDEO else "image",
                              src=media.url if media.kind == MediaKind.VIDEO else (base.src if base else media.url),
                              poster=base.src if (base and media.kind == MediaKind.VIDEO) else ""))
    return plates
```

* **`kind == "video"` non sparisce** (era il difetto che la revisione temeva): la `.plate--film` contiene un `<video controls preload="metadata">` al posto
  del `<picture>`, nella stessa cornice 3:2, con lo stesso cartellino. Controlli **nativi** — nessun controllo scritto a mano, nessun JS, CSP tranquilla —
  e `preload="metadata"`, quindi il costo in byte a riposo è trascurabile. `object-fit: contain` su `--mid-1`: un video non si ritaglia.
* **`caption` e `credit` diventano obbligatori nel form di back-office** di `ForumMedia` (`apps/forum/forms.py`; nessuna migrazione, i campi restano
  `blank=True` a livello di modello per le righe storiche). Una riga senza di essi non entra nel binario: `plates_for` la salta.
* **Una foto caricata come `file` grezzo** non ha derivati: viene servita com'è, e il form la rifiuta sopra **400 KB** indicando la libreria. È l'unico punto
  del sistema in cui un byte non passa dalla pipeline, e va detto invece di nasconderlo.

**Pipeline — il gate risale a monte.** `scripts/fetch_images.py`:
* `Source` guadagna `provides_capture_metadata: bool` — `unsplash` **False**, `pexels` **False**.
* `Candidate` guadagna `place: str`, `shot_on: dt.date | None`, `caption_fr: str`, `credit: str`, `focus: str`, `grade: str`, `ratios: tuple[str, ...]`.
* **La pipeline solleva `PipelineError` per un candidato non decorativo con `place`, `shot_on`, `caption_fr` o `credit` vuoti.** Il gate `is_publishable` non
  cambia di una riga: si aggiunge un secondo gate **più in alto**, così un asset impubblicabile non può più nemmeno essere prodotto. Era il difetto di
  progetto del § 1.5.
* `MAX_BYTES = 350*1024` (riga 111) **cade**. Al suo posto: scala di qualità AVIF 52/52/45/45/40 e WebP 72/68/62 per 480/800/1200/1600/2000, tetto **105 KB
  per derivato**; un derivato sopra il tetto viene ricodificato un gradino più in basso (minimo q38 AVIF / q55 WebP) e, se resta sopra, **non viene emesso** —
  è così che il 4:5 a 1200 px in WebP (149,5 KB misurati) semplicemente non esiste, e il browser senza AVIF ripiega su 800w. Per la variante `film` il tetto
  è più stretto, perché in un provino le lastre in campo sono quattro e non una: **480w ≤ 20 KB AVIF / 26 KB WebP · 800w ≤ 42 KB AVIF / 52 KB WebP**. Un
  provino è un provino.
* `WEBP_WIDTHS = (480, 960, 1440, 1920)` → `AVIF_WIDTHS = (480, 800, 1200, 1600, 2000)`, `WEBP_WIDTHS = (480, 800, 1200)`, `FILM_WIDTHS = (480, 800)`.
* Crop duro per rapporto: derivati `slug-21x9-1600.avif`, `slug-4x5-1200.webp`, `slug-3x2-480.avif`. `object-fit: cover` non sceglie mai (regola 2).
* `apps/cms/seeds_media.py` scrive finalmente `caption_place`, `caption_date`, `caption_fr`, `credit` dal manifest, e aggiunge a `license_notes`
  `focus=…; kind=…; grade=…; folio=…`. **Zero migrazione**: i quattro campi esistono già su `cms.MediaAsset` dal primo giorno.

### 4.9 Da dove vengono `place` e `date` — e perché quattordici fotografie sono state ritirate

Questa è la lacuna più profonda della revisione, e aveva ragione. `resolve_pexels` (`scripts/fetch_images.py:415-452`) restituisce **due cose**: l'URL
dell'originale e il fotografo. L'API di Pexels non porta né il luogo né la data di ripresa — non è una limitazione della nostra implementazione, è ciò che
l'API espone. Delle quattordici candidate del round 1, **due** asserivano un luogo (C09 «Milano», C14 «Casablanca») e **nessuna** una data. Il test che il
round 1 proponeva in § 8 — «rifiuta una didascalia senza toponimo **e** senza data» — avrebbe rifiutato dodici delle quattordici lastre che il round 1 aveva
scelto. La proposta poggiava su un campo che la sorgente scelta non può riempire.

Non allento il gate (è una porta di pubblicazione, e quelle non si toccano). Non invento le date (un cartellino inventato è peggio di nessuna immagine: la
credibilità è tutto ciò che questa piattaforma vende). Quindi **una fotografia di banco non può essere una lastra**, e la conclusione va scritta per intero
invece di essere aggirata:

> **Una lastra nasce solo da una provenienza che porta il proprio catalogo.** Tre, e nessun'altra.

| # | Provenienza | Che cosa può riempire | Che cosa copre | Quando |
|---|---|---|---|---|
| **P1** | **Forum di Rovigo, 2 ottobre 2026** — copertura commissionata, liberatorie raccolte in sala (`IMAGE_LICENSES` § 5 lo prevede già) | `place` = «Sala della Gran Guardia, Rovigo» · `date` = 2026-10-02 · `credit` = il fotografo · `caption_fr` scritta dalla redazione lo stesso giorno | capitolo Forum · provino Forum (6–10 fotogrammi) · via Institutions · attualità | T+8 giorni |
| **P2** | **Il titolare** — precedente già registrato in `IMAGE_LICENSES` § 7.1 (la facciata romana, dichiarata in sessione il 23/09/2026) | luogo e data **dichiarati per iscritto da lui**, come già fatto una volta | capitolo home (riva nord) · via Personnes/Entreprises, se ha materiale | **subito**, una domanda |
| **P3** | **Wikimedia Commons, solo CC0 e CC BY 4.0**, solo file la cui pagina porta `DateTimeOriginal` | `date` letta da `extmetadata.DateTimeOriginal` · `credit` da `extmetadata.Artist` · `place` **dichiarata dal curatore e verificata a mano** contro la pagina del file | capitolo territorio (pianura veneta, skyline di Casablanca) — **mai persone**: niente liberatorie, niente GDPR | **subito** |

**P3, in concreto** — nuova `Source(key="commons", provides_capture_metadata=True)`:
`https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|size|extmetadata&iiextmetadatafilter=DateTimeOriginal|Artist|LicenseShortName|Credit&titles=File:<nome>`.
La pipeline **rifiuta** il candidato se `LicenseShortName` non è esattamente `CC0` o `CC BY 4.0`, se `DateTimeOriginal` non si risolve in una data, o se il
curatore non ha scritto `place`. `source_url` registrato nel manifest è la **pagina del file**, mai l'host della CDN (policy § 1.1 di `IMAGE_LICENSES`;
`upload.wikimedia.org` va aggiunto al registro F24 per simmetria con Unsplash e Pexels).

**Le quattordici candidate Pexels restano — come brief, non come sorgenti.** Il lavoro editoriale del round 1
era buono; era la sorgente a essere sbagliata. Diventano il **piano di ripresa** consegnato al fotografo: soggetto, rapporto, punto focale, e — la parte che
vale — che cosa **non** deve entrare nell'inquadratura. Il fotografo lavora dove il luogo e la data sono un fatto.

### 4.10 Il piano di ripresa — otto lastre, un provino, e ciò che non deve entrare in campo

| Lastra | Rapporto · grado · focus | Soggetto | Che cosa NON deve entrare | Provenienza · liberatoria |
|---|---|---|---|---|
| **Capitolo home — riva nord** | 21:9 · `-notte` · `c` | Pianura coltivata a mosaico dall'alto, luce radente, nessuna persona | nessun campanile o monumento riconoscibile (è territorio, non cartolina); nessuna costa, nessuna linea d'acqua che evochi una traversata | **P3** (Commons, veneto/pianura padana, CC BY 4.0 con data) o **P2** · nessuna liberatoria |
| **Capitolo Forum — la sala** | 21:9 · `-notte` · `c` | La sala **prima** della riunione: file vuote, palco, luce accesa | nessun volto; nessuna bandiera, nessuna insegna, nessun logo (gate G6); nessuna promessa di presenze che non possiamo garantire | **P1** · nessuna liberatoria (sala vuota) |
| **Capitolo — riva sud** *(riserva del capitolo home, alternanza editoriale)* | 21:9 · `-notte` · `c` | Skyline urbano contemporaneo di Casablanca | né moschea (monumento religioso su piattaforma neutrale) né conceria (orientalismo) né costa (registro di cronaca migratoria) | **P3** · nessuna liberatoria |
| **Via — Institutions** | 4:5 · `-lume` · `ie` | Chi prende la parola a un tavolo di lavoro, taglio stretto sull'oratore | **crop obbligatorio** su bandiere, insegne e testi di terzi: nessuna istituzione va evocata senza autorizzazione (gate G6) | **P1** · liberatoria firmata in sala |
| **Via — Projet pilote** | 4:5 · `-lume` · `is` | Due adulti in colloquio, documenti sul tavolo, mani — l'accompagnamento reale, non il risultato | nessun marchio su schermi o portatili (`redact` feathered, già supportato dalla pipeline, registrato con `redact_reason`); **niente** che possa leggersi come un canale d'ingresso già autorizzato — la nota di sezione del pilota è legalmente portante e l'immagine non deve contraddirla | **P1/P2** · liberatoria |
| **Via — Entreprises** | 4:5 · `-lume` · `c` | Il gesto di lavoro reale del tessuto veneto (agroalimentare, meccanica), DPI indossati | nessun open space generico; nessuna saldatura con scintille (spettacolo industriale da banco stock); nessun marchio | **commissione P1**, mezza giornata in Veneto · liberatoria |
| **Via — Universités** | 4:5 · `-lume` · `c` | Adulti in ascolto in aula luminosa — formazione pre-partenza, non liceo | nessuna scena di laurea, nessuna insegna d'ateneo | **commissione P1** · liberatoria |
| **Attualità — default** | 3:2 · `-lume` · `c` | Mani e documenti in riunione, nessun volto: neutra e riusabile | nessun volto (una foto di default che ritrae qualcuno lo ritrae in articoli che non lo riguardano) | **P1** · nessuna liberatoria |
| **Provino Forum** | 3:2 ×6–10 · `-lume` | La giornata: sala, interventi, firma di un accordo, mani e fogli | stesso obbligo di crop sulle insegne; nessun minore; nessun documento leggibile | **P1** · liberatoria per ogni persona riconoscibile |
| *(eventuale)* **Ritratto di mestiere** | 4:5 · `-lume` · `c` · `kind=archetype` | Un mestiere, una persona, uno sguardo | — | **commissione** · liberatoria + il cartellino **dichiara** di essere un archetipo, in tutte e quattro le lingue |

**Soggetti rifiutati, da non rivalutare** (la lista del round 1 resta, ed è la parte del lavoro che non dipendeva
dalla sorgente): Venezia/gondole/canali e piazze affollate di Venezia e Firenze (cliché turistico, registro vietato F15) · costa di Casablanca (la linea di
costa evoca la traversata) · concerie di Fès (orientalismo) · moschea Hassan II (monumento religioso su piattaforma neutrale) · fabbrica con filo spinato (F15)
· saldatura con scintille (spettacolo industriale da banco) · firma di un **divorzio** (soggetto giuridico estraneo e fuorviante).

**Che cosa si può pubblicare prima del 2 ottobre.** Le due lastre di territorio (P3) e, se il titolare risponde
alla domanda, il capitolo home (P2): **due capitoli su due, subito**. Le quattro vie e il provino arrivano con il Forum. Fino ad allora quegli slot non
stampano nulla — che è esattamente ciò che `photo_from_asset` fa già oggi, e le pagine reggono sulla tipografia. Questo è il gate che funziona, non il gate
aggirato.

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` § 6

**Una sola animazione d'autore su tutta la superficie, e non tocca la fotografia.** Il round 1 ne aveva cinque,
e la revisione ne ha smontate tre come default di catalogo (otturatore, parallasse, hover-scale). Non le ho sostituite con tre default diversi: le ho tolte.
La seconda voce della tabella non ha né durata né curva — è lo scorrimento nativo del browser — e perciò non spende nulla del bilancio del § 1 di
MOTION_SYSTEM.

| Voce | Funz. | Innesco | Durata | Curva | Proprietà | Stato ridotto | Prestazioni |
|---|---|---|---|---|---|---|---|
| **M-IMG-1 · Il cartellino entra nel suo alloggiamento** | GERARCHIA (famiglia ENTRATA) | `inView` una volta, soglia 0,25, su `[data-plate]` → `.is-in` | `--motion-base` **240 ms**, ritardo **60 ms** (il valore alto dello stagger 40–60 ms della famiglia) | `--ease-out` | **`.plate__legend-in`** `translateX(var(--slide) → 0)` dentro `.plate__legend{overflow:hidden}`. **Una** proprietà, **un** layer, **zero** paint | la `transition` e la regola di stato vivono entrambe dentro `@media (prefers-reduced-motion: no-preference)`: fuori da lì l'etichetta è al valore finale. Identica anche **senza JS** (`html.js` assente) | 1 layer, 240 ms, nessun `will-change` necessario su una singola trasformazione di un blocco di 334×122 px |
| **M-IMG-2 · Il binario avanza** | ORIENTAMENTO | i due bottoni del provino | **nativa** — `scrollBy({behavior:"smooth"})`. Nessuna durata è dichiarata, quindi **nessun numero è inventato**: il browser possiede la curva e il tempo | — | `scrollLeft` | `behavior:"auto"` (salto immediato); la preferenza è letta **dal vivo** a ogni clic con `matchMedia`, non una volta | scroll composito del browser |

**Assenze dichiarate — ciò che questa superficie NON fa, e perché.**

| Cosa | Perché no |
|---|---|
| Moto legato allo scroll | MOTION_SYSTEM § 4 ammette **un** oggetto indicizzato allo scroll per pagina IMMERSIVE, e la home ne ha già **due**: `home.js:95` (la fotografia della porta, 18 px, DEPTH) e `home.js:116` (la rotta del voyage, `strokeDashoffset`). Erano già una di troppo prima che arrivassi io; non ne aggiungo una terza e non chiedo la deroga per prenderne il posto. La deriva di 24 px del round 1 era, per giunta, invisibile a 390 px. |
| Otturatore / maschera sull'immagine | È il reveal Framer di catalogo, ed era opaco senza JS: la fotografia semplicemente spariva. Tolto. |
| `scale` in hover sull'immagine | Il gesto di default di ogni libreria di componenti, e sulla cornice era un'animazione di `box-shadow` — vietata. La risposta al puntatore è quella che il pannello di via ha già. |
| Fade-in-up sul cartellino | `fade-in-up` generico su ciò che entra in viewport è **vietato dalla prima riga di ANTI_PATTERNS.md**; il round 1 lo rinominava invece di cambiarlo. Qui il cartellino non dissolve e non sale: **esce dal suo alloggiamento sull'asse di lettura**, che è il gesto di un'etichetta infilata nel suo portacartellino, e ha una direzione perché ha un verso di lettura (RTL la specchia con `--slide`). |
| Un loop ambientale | Questa superficie non ne introduce nessuno. La marea dell'hero resta l'unico della home. |
| Animazione sulla fotografia, di qualunque tipo | Regola 4 del § 4.1. **La fotografia non si muove mai.** Si muove il suo apparato. |

Nessun overshoot, nessuna molla, nessuna curva nuova, nessuna durata nuova. Ogni voce dichiara una delle sette funzioni: «estetica» non compare.

---

## 6. ACCESSIBILITÀ E RTL

**Testo e fotografia.** Nessun testo è mai dipinto su una fotografia (§ 4.1 regola 4). Il solo testo *dentro*
una banda sta su una superficie opaca di livello 2 (`--mid-3`) con `--on-dark` a **12,29:1** e `--on-dark-2` a **7,67:1** — misurati, su fondo opaco, non su un
gradiente. Sul fondo minerale il cartellino è `--ink-2` **6,46:1** e `--ink-3` **5,53:1**. `--on-dark-3` resta **vietato** su qualunque lastra.

**`alt` e vocabolario.** `alt` obbligatorio e descrittivo su ogni lastra; l'`alt` non ripete mai il cartellino —
dice **che cosa** si vede, il cartellino dice dove, quando e di chi è. `alt`, `figcaption`, `aria-label`, `title` e ogni etichetta visually-hidden passano da
`cms.forbidden.scan` **e** dal vocabolario vietato di `IMAGE_LICENSES` § 1.8 (`door, porta, passport, valise, suitcase, frontière, border, aéroport, airport,
queue, file, grille, gate`). Le stringhe nuove di questa superficie sono tre, tutte con **msgid francese** come ogni altra in `templates/components/` (il round
1 ne spediva una in italiano, che sarebbe uscita in italiano sul locale FR primario finché qualcuno non avesse scritto una voce `.po` a rovescio):
«Image d’archive : cette photographie ne représente pas des personnes du projet.» · «Image précédente» · «Image suivante». Nessuna contiene una parola vietata;
nessuna è lo slogan o la tagline del committente.

**`<figure>` senza `<figcaption>`: impossibile per costruzione** — chiude tutti e quattro i difetti latenti del
§ 1.7, compreso `forum/partials/hero.html:33` che il round 1 non aveva contato.

**`forced-colors: active`.** La cornice diventa `1px solid CanvasText`; il cartellino di capitolo **smette di
sovrapporsi** (`margin-block-start: 0`) e si impila sotto la banda su `Canvas/CanvasText`; la riga di margine diventa `CanvasText`. Nessuno scrim da
nascondere: non ce n'è più uno. Il capitolo non perde una parola.

**`prefers-reduced-motion` è uno stato completo.** L'unica `transition` del foglio, **e** la regola che nasconde
l'etichetta, stanno **entrambe** dentro `@media (prefers-reduced-motion: no-preference)`: con la preferenza attiva nessuna delle due esiste e il cartellino è
al valore finale. Nulla è raggiungibile solo col movimento, niente resta a opacità 0, nessun contenuto è nascosto.

**Senza JavaScript.** Lo stato senza JS **è** lo stato finale: `html.js` non compare, la regola non si applica,
il cartellino è a posto e la fotografia — che non è mai stata coperta da nulla — si vede. Il provino resta un binario che si scorre con il dito, con la barra
di scorrimento e con ←/→; perdono solo i due bottoni, che sono una scorciatoia e non l'unico modo.

**Provino.** Bersagli **44 × 44 px** sui due bottoni (`min-inline-size`/`min-block-size`). Binario
`tabindex="0"` con `role="list"` e `aria-label`, perché una regione scorribile deve essere raggiungibile da tastiera (SC 2.1.1). ←/→ sono del browser
(misurato: una posizione di snap, 438 px); Home/End sono in `plate.js`, perché il browser non li dà sull'asse inline (misurato). **Nessun `aria-current`,
nessuna live-region, nessun `<dialog>`**: non c'è un elemento «corrente» da annunciare e non c'è una vista ingrandita da aprire. Ogni fotogramma è una
`<figure>` completa con il suo cartellino, letta in ordine.

**Colore mai da solo.** In questa superficie il colore non porta **nessuna** informazione: non c'è stato
«corrente», non c'è hover, non c'è semantica. L'unica differenza cromatica è il cartellino chiaro/scuro, che segue il fondo della sezione.

**RTL.** Nessuna proprietà fisica in `plate.css` (verificato: 0 occorrenze). Misurato su `/ar/` reale:
`border-right: 1px` / `border-left: 0`, `padding-right: 16px` / `padding-left: 0`, `focus-is` → `object-position: 76% 50%` (specchiata), `--slide: 100%`
(l'etichetta esce dal lato di lettura). Il binario scorre da destra; `plate.js` legge `direction` per Home/End. `:lang(ar)` azzera `letter-spacing` e
`text-transform` sulle righe mono, come prescrive § 3.2.

**Da testare.** (1) NVDA+Chrome e VoiceOver+Safari sul provino: l'ordine di lettura è figura, didascalia, figura,
didascalia; nessun doppio annuncio. (2) Zoom testo 200 % a 390 px — **già misurato**: il cartellino cresce verso il basso, la risalita resta 16 px, l'area
coperta resta 8,19 %. (3) `forced-colors` su capitolo e provino. (4) RTL `/ar/` a 390 e 1440. (5) `reduced-motion` **+** no-JS insieme: la pagina è già lo
stato finale — e questa volta il CSS lo garantisce invece di contraddirlo.

**HUMAN_QA_REQUIRED.** Visione a piena risoluzione di ogni fotografia contro la lista dei soggetti vietati,
**prima** dell'ingresso in `CURATED` (`IMAGE_LICENSES` § 2) · **verifica del `place` dichiarato contro la pagina del file** per ogni candidata P3 (la pipeline
verifica licenza e data, il luogo no) · raccolta e archiviazione delle liberatorie P1, una per persona riconoscibile · giudizio umano sull'opportunità di
mostrare una persona identificabile su una piattaforma che parla di percorsi legali altrui, anche con liberatoria in regola · traduzioni IT/EN/AR di `alt` e
`caption`, **mai** automatiche.

---

## 7. PRESTAZIONI

**Codice, misurato** (§ 4.6 G). `static/css/v3/plate.css` = **4 164 B minificato, 1 240 B gzip**.
`static/js/dist/plate.js` = **946 B, 541 B gzip**, senza Motion e senza alcuna nuova dipendenza. Budget 45 KB gzip per pagina: il margine è intatto, e questa
superficie è la più leggera del set V3.

**Immagini — il censimento per viewport, rifatto a DPR 1, 2 e 3.** Ogni cifra è il **peggiore** delle
diciotto codifiche del § 4.6 E per il gradino che Chromium **effettivamente sceglie** (§ 4.6 D).

| Viewport | Lastre in campo | Gradino | AVIF peggiore | WebP peggiore | Budget |
|---|---|---|---:|---:|---|
| home, primo viewport (hero) | la porta, `doorway-480.avif` | 480w | **24,3 KB** | 31,3 KB | ✅ |
| home 1440 DPR 1, capitolo | 1 × capitolo | 1600w | **72,3 KB** | 74,9 KB *(1200w: la scala WebP si ferma lì)* | ✅ |
| home 1440 **DPR 2**, capitolo | 1 × capitolo | **2000w** | **75,6 KB** | 74,9 KB *(1200w)* | ✅ |
| home 390 DPR 3, capitolo | 1 × capitolo | 1200w | **42,3 KB** | 74,9 KB | ✅ |
| landing di via 1440 DPR 1 | 1 × via | 480w | **28,2 KB** | 43,0 KB | ✅ |
| landing di via 1440 DPR 2 | 1 × via | 1200w | **99,7 KB** | 87,2 KB *(800w: il 1200 WebP 4:5 supera il tetto e non è emesso)* | ✅ |
| landing di via 390 DPR 3 | 1 × via | 1200w | **99,7 KB** | 87,2 KB | ✅ |
| `news/detail` 1440 DPR 2 | 1 × attualità | 1600w | **96,7 KB** | 103,2 KB *(1200w)* | ✅ |
| `news/detail` 390 DPR 3 | 1 × attualità | 1200w | **60,3 KB** | 103,2 KB | ✅ |
| Forum, primo viewport 1440 DPR 2 | 1 × capitolo | 2000w | **75,6 KB** | 74,9 KB | ✅ |
| Forum, provino 1440 DPR 2 | **4** fotogrammi (misurato) | 480w | **72,8 KB** | 104 KB *(tetto film 26 KB × 4)* | ✅ |
| Forum, provino 390 DPR 3 | **2** fotogrammi (misurato) | 800w | **84 KB** | 104 KB *(52 × 2)* | ✅ |

**Nessun viewport supera 120 KB, in nessuno dei due formati, a nessun DPR misurato.** Il peggiore assoluto è
**104 KB** (provino, WebP). Il numero che il round 1 non aveva mai calcolato — 2000w a 1440/DPR 2 — vale **75,6 KB**, e ci sta perché la qualità **scende con
la larghezza** (q40 a 2000 px): su un display 2× il pixel ha metà dell'angolo visivo, e un artefatto vale metà. È una decisione, con una ragione, non un
arrotondamento.

**Perché la scala si ferma a 2000w.** A 1440 px CSS con DPR 2 una banda a piena larghezza chiederebbe 2880 px; la
servo a 2000 e la lascio ingrandire di 1,44×. Su un paesaggio 21:9 gradato la differenza non si vede; il triplo dei byte sì. Il budget è un vincolo, la
nitidezza su una banda panoramica è una preferenza.

**Perché il provino è largo 240 px.** Non è timidezza: è aritmetica. Più fotogrammi in campo = più byte. A
240 px il browser resta sul gradino 480w fino a DPR 2 (misurato), e con `max-inline-size: 1000px` sul binario ne stanno **quattro** in campo (misurato, contro
i cinque di un binario a piena larghezza). 4 × 26 KB = 104 KB. Un provino, del resto, è fatto di provini.

**Paint e layout.** `aspect-ratio` + `width`/`height` dal manifest → **CLS 0 per costruzione**, e
`content-visibility: auto` non lo rompe (misurato: una lastra sotto la piega conserva cornice 687×458 e rapporto 1,500 sotto size containment). Niente
`contain-intrinsic-size`: con un `aspect-ratio` e una larghezza definita l'altezza è definita comunque, e il numero magico `420px` del round 1 era un numero
inventato. Un solo `fetchpriority="high"` per pagina, sulla lastra LCP, che è anche l'unica senza `content-visibility`. Gradazione **cotta**: zero `filter`,
zero `mix-blend-mode`, zero `backdrop-filter`, zero gradienti. Si muove **una** proprietà (`transform`) su **un** layer, per 320 ms, una volta per lastra.
Tutto da `static/`: gli host CDN restano nel registro vietato F24 e il manifest non li contiene.

**La libreria attuale** (6,9 MB, 0 pubblicabili) va **ritirata**, non integrata: nessuna delle quindici può
riempire un cartellino (§ 1.4), e quattro di esse hanno derivati sopra il nuovo tetto di 105 KB.

---

## 8. RISCHI

| Rischio | Perché farebbe sembrare il sito **economico** | Guardia |
|---|---|---|
| **Stock che resta stock** | Sorriso in camera, fondo bianco, mani su tastiera: il lessico del banco immagini si riconosce in 200 ms e distrugge l'autorevolezza. | **La prova è diventata strutturale**: una sorgente senza catalogo non può produrre una lastra (§ 4.9), e la pipeline solleva un errore invece di scrivere un asset che il gate rifiuterà. Restano le quattro prove editoriali: (1) nessuno guarda l'obiettivo sorridendo; (2) nessun isolamento su fondo bianco; (3) c'è almeno un'attrezzatura o un'architettura reale in campo; (4) il cartellino si può scrivere **vero**. |
| **Il cartellino inventato** | Un luogo o una data falsi su una piattaforma che vende credibilità sono il danno peggiore possibile — peggiore di nessuna immagine. | Due gate in serie: la pipeline rifiuta un candidato senza `place`/`shot_on`; `is_publishable` rifiuta l'asset. E HUMAN_QA verifica il `place` contro la pagina del file per ogni candidata P3. |
| **Duotone sugli incarnati** | Volti virati in teal su una piattaforma che parla di persone marocchine e italiane: kitsch nel migliore dei casi, offensivo nel peggiore. | Gradazione e non duotone (§ 4.2): saturazione **mai sotto 0,66**, nessuna rotazione di tinta, controllo esplicito degli incarnati sulle lastre di via. |
| **Troppe immagini** | Una foto per sezione = brochure. Il committente ha chiesto *meno ma molto meglio*. | Quattro slot, tre rapporti, tetto per `data-mode` (§ 4.3) con un test che conta `main .plate` per modo. Tre pagine informative hanno **perso** il loro slot in questo round. |
| **La lastra che diventa una card** | Angoli a 12 px, ombra portata, gradiente sotto: linguaggio da template SaaS. | `--radius-control` (2 px), **zero `box-shadow` nel foglio** (verificato), mai una foto dietro un bottone, mai una foto come fondo di testo. |
| **La banda che diventa l'hero di catalogo** | 21:9 a piena larghezza + gradiente + testo chiaro è il pattern più generico del web, e il round 1 lo aveva scritto. | Il gradiente non esiste più; il testo non tocca mai la fotografia; il cartellino è un oggetto fisico che risale nella banda. Ciò che rende il capitolo riconoscibile è **l'etichetta**, non la banda. |
| **Persone reali spacciate per partecipanti** | Rischio GDPR **e** di credibilità: un archetipo presentato come testimonianza è una bugia. | `kind=archetype` in `license_notes` → il cartellino **dice** «Image d’archive : cette photographie ne représente pas des personnes du projet.», in tutte e quattro le lingue, senza eccezioni. Liberatoria firmata per ogni persona riconoscibile (P1). |
| **Insegne di terzi in campo** | Bandiere, loghi, testi leggibili evocano avalli che non abbiamo (gate G6). | Crop obbligatorio sulle lastre Institutions e sul provino + `redact` feathered già supportato dalla pipeline, registrato nel manifest con `redact_reason`. |
| **Deriva di peso** | 337 KB per una foto: su rete marocchina 3G la lastra arriva dopo il testo, e il premium diventa attesa. | `MAX_BYTES` 350 KB → **105 KB per derivato** (20 KB per il provino), con ricodifica automatica e derivato non emesso se resta sopra; censimento per viewport in CI a DPR 1 e 2 (§ 9). |
| **Ritorno di «istituzionale = sobrio»** | È la scusa che ha prodotto lo 0,94 % del § 1.2. | In DENSE e LEGAL la sobrietà è un **argomento**; in IMMERSIVE è **vietata come motivazione**. Le quattro landing di via sono IMMERSIVE: la lastra non è facoltativa. E il numero da battere ora è scritto: **8,00 %**. |
| **Il Forum non produce le fotografie promesse** | Il 2 ottobre non si ripete: senza copertura, sette slot su dieci restano vuoti per mesi. | Il piano di ripresa (§ 4.10) è un documento da consegnare **prima** dell'evento, con le liberatorie stampate. Se salta, i due capitoli di territorio (P3, senza persone e senza liberatorie) restano pubblicabili da soli, e il sito ha comunque due bande 21:9 dove oggi ha zero. |

---

## 9. I TEST CHE QUESTA SUPERFICIE AGGIUNGE

1. `tests/frontend/test_plate.py` — sul foglio compilato: `box-shadow` = 0, `filter` = 0, gradienti = 0,
   proprietà fisiche = 0, token `--plate-ar-*` = **3**, ogni `transition` e ogni `@keyframes` dentro `@media (prefers-reduced-motion: no-preference)`.
2. Idem, sul DOM renderizzato di ogni rotta pubblica: `[data-plate][data-reveal]` = **0** (collisione con
   `shell.js`) · ogni `.plate` ha esattamente una `figcaption` · `.plate__where`, `.plate__said`, `.plate__credit` non vuoti · al massimo un
   `[fetchpriority="high"]` per pagina · `[data-priority]` presente esattamente sulla lastra LCP.
3. `tests/compliance/test_figure_caption.py` — esteso alle quattro rotte che portano una lastra; la lista
   `PHOTO_PAGES` perde `pages:project`, `pages:agami`, `pages:network` e guadagna `news:detail` e le quattro d'ecosistema.
4. `tests/frontend/test_image_budget.py` **(nuovo)** — in Chromium, la matrice del § 7: per ogni rotta ×
   {1440 DPR 1, 1440 DPR 2, 390 DPR 3}, somma dei byte delle risposte immagine del primo viewport **≤ 120 KB**. È il test che il round 1 avrebbe fallito.
5. `apps/cms/tests/test_media_assets.py` — tetto **105 KB** (20 KB film) per derivato · un `Candidate` non
   decorativo senza `place`/`shot_on`/`caption_fr`/`credit` solleva `PipelineError` · il manifest non contiene un host CDN (F24, ora con
   `upload.wikimedia.org`) · il seed scrive i quattro campi didascalia.
6. `tests/i18n/test_rtl_browser.py` — su `/ar/`: `--slide` = `100%`, `focus-is` → `76% 50%`, il binario scorre
   dal lato di lettura, nessuna proprietà fisica calcolata sulla lastra.
7. Il conteggio `main .plate` per `data-mode` (§ 4.3), con l'eccezione nominata della **DEROGA 1** sulla sola
   rotta `news:detail`.
