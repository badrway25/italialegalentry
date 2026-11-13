# DESIGN V3 — SUPERFICIE `public-sections` · **ROUND 2**

Sezioni, schede, pannelli e piè di pagina del sito pubblico: **tutto ciò che sta sotto l'hero**.
24 settembre 2026. Base rimisurata: `http://127.0.0.1:8771/fr/` (Fase 3 aperta), `:8770/fr/`
(Fase 3 chiusa) e `/ar/`, Chromium headless di Playwright lanciato dal `.venv` del progetto,
1440×900 · 768×1024 · 390×844. Vincolanti: `DESIGN_SYSTEM_V2.md`, `MOTION_SYSTEM.md`,
`ANTI_PATTERNS.md`, `BRAND_ASSETS.md` §1.

> **Round 1 è stato respinto** (premium_lift 4/10, non conforme, non implementabile). Il §2 di
> questo documento risponde voce per voce, con la misura. Le tre idee che il revisore ha
> smontato — i quattro movimenti, la graticola grigia, il rail laterale — **non sono state
> riparate: sono state abbandonate**, due perché appartengono ad altre spec del Council e una
> perché era architettonicamente falsa. Ciò che resta è più piccolo e vero.

---

## 0. RICHIESTE DI EMENDAMENTO

Due sole, numerate, come chiede la direttiva. Tutto il resto di questa spec sta dentro
`DESIGN_SYSTEM_V2.md` e `MOTION_SYSTEM.md` senza deroghe. **Non si introduce nessun token nuovo**
(round 1 ne proponeva uno, `--seal-050`: è ritirato, §4.1).

### EMENDAMENTO 1 — `--seal-100` come **terreno** della minuta antifrode

- **Clausola**: `DESIGN_SYSTEM_V2.md` §1.3 regola 3, «bronzo **solo** sigilli (autorità, jeu de
  règles, attestati)». `--seal-100 #EFE6DA` è registrato in §1.1 fra i bronzi; §2 non lo elenca
  fra i livelli di superficie.
- **Che cosa chiedo**: usarlo come fondo di **un solo oggetto per pagina**, la fascia antifrode,
  che è un atto d'autorità (dichiara che i visti sono rilasciati esclusivamente dalle autorità
  competenti). Il bronzo resta il colore dell'autorità: qui è la *carta* dell'atto, non un
  ornamento.
- **Perché serve**: la fascia deve leggersi come «altro documento», e i tre fondi minerali non lo
  permettono. **Misurato** (CIELAB D65, ΔE2000): `--min-1` contro `--min-0` = **1,99** — *sotto*
  la soglia di percettibilità (≈2,3); `--min-2` contro `--min-0` = **1,53**. `--seal-100` contro
  `--min-0` = **5,40**, cioè 2,2× la soglia. È l'unico fondo del sistema che cambia davvero
  documento senza aprire un capitolo mezzanotte.
- **Che cosa costa**: il bronzo compare sotto l'hero **solo dentro questo oggetto** — fondo,
  filetto alto di 4 px, glifo scudo, filetto di margine — e in nessun altro punto della
  superficie (§8 rischio 2 dà la prova). Il rischio «lusso di plastica»
  (ANTI_PATTERNS §3) è governato in §8 rischio 2. Se il Council rifiuta: la fascia scende su
  `--min-1` (ΔE2000 1,99 — invisibile) e l'oggetto perde la sua ragione; in quel caso si toglie
  del tutto e l'antifrode torna a essere un blocco di testo in colonna, dichiarandolo.
- **Rapporti calcolati su `--seal-100 #EFE6DA`** (WCAG 2.x, ricalcolati riga per riga):
  `--ink` **13,14** · `--ink-2` **5,80** · `--ink-3` **4,97** · `--accent` **5,11** ·
  `--accent-hover` **6,89** · `--accent-ring` **3,33** · `--seal-600` **3,86** ·
  `--hairline-strong` **3,03** · `--err-700` 5,29. Contro `--min-0`: 1,113:1 di luminanza,
  ΔE2000 5,40. `--seal-100` su `--mid-0` = 14,95.

### EMENDAMENTO 2 — un'intestazione di sezione per pagina può prendere `--t-title`

- **Clausola**: `DESIGN_SYSTEM_V2.md` §3.2, «`--t-title` 48/52 = titoli di pagina (Tableau de
  bord, Dossier)»; «`--t-band` 32/36 = titoli di sezione».
- **Che cosa chiedo**: **una sola** intestazione di sezione per pagina pubblica può salire a
  `--t-title`. Sulla home è `[data-section="entrances"]`, il molo, che §8.5 chiama «l'oggetto più
  importante del sito».
- **Perché serve**: il difetto 1.2 non è la dimensione, è che **sette titoli sono identici**
  (misurato: 7 `.section__title`, tutti 38 px/36 px peso 400, larghezza 420,75 px). La scala
  degli undici corpi ha esattamente un gradino fra 32 e 48; senza quel gradino la gerarchia deve
  essere portata solo dalla composizione, che a 8,2 schermate di distanza non si vede.
- **Che cosa costa**: un 48 px in una pagina che ha già un `--t-display` 100 px (l'H1 dell'hero)
  e nessun altro titolo di pagina; il rango resta leggibile come subordinato. Su una pagina con
  un `h1` a `--t-title` l'emendamento **non si applica** (una pagina non può avere due 48).
- **Se il Council rifiuta**: il rango di apertura è portato dal solo peso del filetto (2 px
  contro 1 px) e dalla campata del titolo (7 colonne contro 6). Una riga di CSS, già scritta in
  §4.2, si cancella. Il disegno regge, più piatto.

---

## 1. VERDETTO SULLO STATO ATTUALE — rimisurato

Ogni cifra qui sotto è stata **ricalcolata il 24 settembre in un browser mio**, non ripresa dal
round 1. Le voci corrette rispetto al round 1 sono marcate **[CORRETTO]**; quelle che il revisore
ha riprodotto e che restano valide sono marcate **[CONFERMATO]**.

**1.1 — L'unico accento interattivo sparisce sotto l'hero. [CONFERMATO]**
`--accent #0F6A72` compare 19 volte fra y = 1 363 e y = 1 878 e mai più nei 6 040 px successivi.
Causa a monte: `static/css/v2/bridge.css` mappa `--navy: var(--brand-navy)`. Prova nuova,
misurata su questa superficie: `ol.register.register--entrances` porta
`border-block: 2px solid rgb(15,37,71)` — **il navy del tricolore ufficiale disegna la cornice
dell'oggetto più importante della pagina**, contro §1.3 regola 4. Questa spec non aspetta la
correzione a monte: ridichiara entrambi i bordi (§4.3).

**1.2 — Sette titoli identici, e la causa esatta. [CORRETTO — il round 1 diceva «qualcosa
sovrascrive il token», che è vago e sbagliato]**
Sette `.section__title` a `font-size: 38px` / `line-height: 36px`, peso 400, `--ink`, larghezza
**420,75 px**. L'interlinea è **minore** del corpo: i quattro titoli che vanno a capo misurano
72 px per due righe da 38 px — le righe si toccano. Il meccanismo, letto dal `:root` calcolato in
pagina:

| proprietà | 1440×900 | 390×844 |
|---|---|---|
| `--t-band-size` (famiglia legacy, `tokens.css`) | **38px** | **28px** |
| `--t-band` (famiglia V2, `v2/tokens.css:89`) | **2rem** = 32px | **2rem** = 32px |
| `--t-band-lh` (dichiarato da **entrambe**) | **2.25rem** = 36px | **2.25rem** = 36px |

`base.css:175` compone `h2` con `font-size: var(--t-band-size); line-height: var(--t-band-lh)`.
`tokens.css` alza `--t-band-size` a 38 px dentro `@media (min-width: 90rem)` **senza** dare la
`--t-band-lh` corrispondente, mentre `v2/tokens.css` ridichiara `--t-band-lh` su `:root`; le
media query non aggiungono specificità, quindi **la dichiarazione V2, che viene dopo
nell'ordine di `@import`, vince su quella legacy**. Il titolo prende la *misura* da una famiglia
e l'*interlinea* dall'altra. Non è un override misterioso: sono due famiglie di token che
condividono un nome. La riparazione è di una riga (§4.2) e non tocca nessun token.

**1.3 — Sei folii byte per byte identici. [CONFERMATO]**
Sette `.section__header`, sei con folio. Sei `.folio__ordinal` a **44 px** `--ink-3`; sei
`.folio__head` a **13 px, letter-spacing 1,04 px, peso 600**; sei `.folio` con
`border-block-start: 2px solid rgb(85,100,107)` = `--ink-3`. Cambia solo la stringa: il folio ha
risolto la duplicazione del CSS, non la gerarchia.

**1.4 — L'intestazione occupa un terzo della misura e lascia il resto vuoto. [CONFERMATO,
con le due larghezze distinte]**
`.section__header { max-inline-size: 420.75px }`. Il `.container` misura **1 320 px di box** e
**1 240 px di contenuto** (`padding-inline: 40px`): il round 1 citava 1 240 px e aveva ragione,
ma non diceva quale delle due. Carta vuota alla destra dell'intestazione: **819,25 px**, su
**sette** intestazioni (non otto: il round 1 contava una sezione che non ha intestazione).

**1.5 — La scala delle superfici non esiste, e il contrasto non era la misura giusta.
[CORRETTO — la metrica del round 1 era sbagliata, la diagnosi era giusta]**
Il round 1 accusava i fondi con il rapporto di contrasto WCAG (1,06:1, 1,08:1). Il rapporto di
contrasto è una metrica di **leggibilità del testo**: non dice se un occhio distingue due
superfici. La metrica giusta è la differenza di colore. Ricalcolata (CIELAB D65, ΔE2000, soglia
di percettibilità ≈ 2,3):

| coppia | rapporto WCAG | **ΔE2000** | verdetto |
|---|---|---|---|
| `--min-1` `#ECEBE6` su `--min-0` `#F4F3F0` | 1,076 | **1,99** | **sotto soglia: il cambio di terreno non si vede** |
| `--min-2` `#FBFAF8` su `--min-0` | 1,064 | **1,53** | **sotto soglia: il foglio non si vede** |
| `--seal-100` `#EFE6DA` su `--min-0` | 1,113 | **5,40** | si vede |

E i confini: `--hairline #D3D2CC` fa **1,37:1** sulla tela e **1,45:1** sul foglio. Un pannello
che esiste *solo* grazie a quel filetto è un componente identificato da un bordo sotto il 3:1 che
la 1.4.11 chiede. **Zero `box-shadow` sotto l'hero** (censimento: gli unici tre elementi con
ombra su `main` sono `doorway__arch`, `doorway__inner` e il velo della porta — tutti dentro
l'hero).

**1.6 — Dieci sezioni, zero separatori, tre fondi. [CONFERMATO]**
Divario fra sezioni consecutive: **0 px in tutti i casi**; sei sezioni su dieci hanno
`background-color: rgba(0,0,0,0)`; tre soli fondi non trasparenti su **7 921 px** di scorrimento.
Questa superficie **non ridisegna i fondi**: sono della spec `backgrounds` (§9).

**1.7 — Le sezioni non si muovono. [CONFERMATO]**
`[data-reveal]` esiste in due soli template: `_hero.html` (3 nodi) e `_pilot.html` (8), **11 in
tutto**. Le otto sezioni di questa superficie e il piè di pagina hanno **0 animazioni**. Il
sistema di reveal di `shell.js` è scritto, testato, e non applicato qui.

**1.8 — L'antifrode è la scatola di marketing che la direttiva vieta. [CONFERMATO, con la
misura della riga peggiorata]**
`background: #F4F3F0` **identico alla tela**, `border-inline-start: 4px rgb(15,37,71)` (di nuovo
il navy), `padding: 48px`, scudo 40 px in un tondo grigio, altezza 472 px. Il corpo è in
**Newsreader 22 px/36,3 px su 822,8 px**. Il round 1 stimava «≈80–85 caratteri per riga». È
**falso per difetto**: contato con `Range.getClientRects()` sul nodo vivo, il corpo è di
**640 caratteri su 7 righe = 91,4 caratteri per riga**, contro il massimo di 75 di §3.2. E un
avviso composto nella stessa voce serif della prosa editoriale non legge come avviso.

**1.9 — Le attualità sono un wireframe. [CONFERMATO]**
Nessuna scheda in pagina: la sezione rende `.empty-state` **672 × 218 px**,
`border: 1px dashed #D3D2CC`, `text-align: center`, icona documento generica, in una colonna di
1 240 px, con «Toutes les actualités →» abbandonato 600 px più in basso.

**1.10 — Il piè di pagina è, alla lettera, quello vietato. [CONFERMATO, con l'inventario reale]**
`grid-template-columns: 348.172px 248.688px 248.703px 298.422px` — **quattro colonne**, che §8.7
vieta per nome. Altezza 629 px a 1440 e **1 307 px a 390**, l'**11,69 %** di una pagina da
11 183 px. **Ogni link è alto 24 px** su entrambi i formati. La causa è una sola dichiarazione:
`static/css/v2/shell.css:408` — `.site-footer a { min-block-size: 24px }`, il minimo esatto della
2.5.8, mai il bersaglio da 44 px che la direttiva chiede dove il disegno lo consente.

**1.11 — Dettagli. [PARZIALMENTE CORRETTO — il revisore ha ragione su un punto e io su tre]**

- **Il bersaglio dei percorsi: il round 1 aveva torto.** `.pathway-list__title a::after` è
  `position: absolute; inset: 0px`: il bersaglio puntatore è **l'intera riga**, misurata
  **588 × 141 px** (e 169 px per le righe a tre capi) a 1440, **350 × 141–169** a 390. La 2.5.8
  **passa già** e l'accusa del round 1 è ritirata. **Ma il difetto esiste, ed è un altro**:
  l'anello di focus è disegnato sul box in linea dell'`<a>`, alto **13 px**, dentro una riga di
  141 px — misurato con `.focus()` sul nodo vivo, `outline: rgb(29,138,147) solid 2px`,
  `offset 2px`, `height 13`; la riga stessa non ha `outline` (`none`). Chi naviga da tastiera
  vede un trattino di 13 px sospeso in una riga di 141. È un difetto di **apparenza del focus**,
  non di dimensione del bersaglio, e la riparazione è diversa (§4.4).
- **Il lead**: reso `font-style: normal` a **22 px/28 px** in Newsreader, mentre §3.2 prescrive
  `--t-lead` **20/28 corsivo**. [CONFERMATO]
- **La barra di giurisdizione**: il componente `.jurisdiction` è alto **105 px**, di cui la barra
  `.jurisdiction__bar` **20 px** con 8 segmenti da 18 px, su una sezione di **1 002 px**. Il solo
  dispositivo chiesto all'unanimità dal Council occupa il 2 % della sezione che lo ospita.
  [CONFERMATO, con la distinzione fra componente e barra]
- **Il pannello dell'area riservata**: **1 240 × 118 px**, `background rgb(244,243,240)` identico
  alla tela, `border: 1px solid rgb(211,210,204)` a 1,37:1. [CONFERMATO]

---

## 2. RISPOSTA ALLA REVISIONE — ogni MUST-FIX

Nessuna voce è lasciata aperta. **Dodici MUST-FIX, dodici FATTI**; e quattro affermazioni della
revisione sono **contestate con la misura** in §2.1 — una delle quali, la 2.5.8 sui percorsi,
contesta una mia accusa del round 1 e le dà ragione.

| # | MUST-FIX | Esito | Dove / con quale numero |
|---|---|---|---|
| 1 | Risolvere i movimenti contro il contratto CMS, o abbandonarli | **FATTO — abbandonati** | §4.0. Niente `data-movement`, niente numeri romani, niente elenco fisso. Il meccanismo è `[data-section="<chiave>"]`, **già nel DOM** su entrambe le configurazioni vive (verificato: 10 attributi a :8771, 7 a :8770). `banner` ha il suo trattamento (§4.8). Il congedo è definito in entrambi gli stati di `reserved` (§4.7). Zero righe di `services.py`. |
| 2 | Ricostruire il piè di pagina su quello vero | **FATTO** | §4.7. Inventario completo misurato: **16 link a :8771, 12 a :8770**; `footer_menu` misurato **8 righe con G3 aperto, 5 con G3 chiuso** — non è «5 voci», è una lunghezza variabile *osservata variare fra due configurazioni vive*. Layout per lunghezza variabile, frase `blocktranslate` conservata, `site-footer__mark` conservata, `{% if gates.phase3_public %}` ridichiarato, due `<nav aria-label>` e tre `<h2>` conservati. La rivendicazione «16 → 16» è sostituita da una formula e da due misure. |
| 3 | Risolvere il confine di `<main>` | **FATTO — non si fondono** | §4.7. `_reserved` resta dentro `<main>` e dentro il ciclo di `home_sections()`; `partials/footer.html` resta fratello di `</main>` e resta `contentinfo`. Sono **due elementi che condividono una grammatica**, non un elemento che ne avvolge due. Il costo è scritto. |
| 4 | Ripristinare ogni ramo di template caduto | **FATTO** | §4.2, §4.5, §4.6, §4.7: `visually-hidden` di fallback, ogni `{% if X.lang %}`, `{% if s.note %}`, `{% if d.url %}`, il `{% else %}` di `_ecosystem`. Il rischio 8 (§8) elenca ora **attributi**, non solo parole. |
| 5 | Riscrivere il rischio 6 con l'inventario vero | **FATTO** | §8. **Nessuna classe è rinominata su questa superficie.** `section__title`, `section__header`, `section__lead`, `folio*`, `register--entrances`, `register__item`, `entry*`, `card__title`, `empty-state`, `antifraud-panel*`, `#icon-shield`, `pathway-list*`, `site-footer*`, `home-trust__column` restano tutti. Elenco con numeri di riga e il motivo per ciascuno. |
| 6 | Specificare piega e rail come componenti veri, o tagliarli | **FATTO — tagliati** | La piega è `th--fold` + `.tide` della spec `backgrounds` §4.1–4.3; il rail è il `readbar` della spec `scroll` §4.5. Erano **due riscritture peggiori di oggetti che il Council ha già assegnato**. Vedi §9. |
| 7 | Sanare la contraddizione 1.4.11 | **FATTO** | §4.3. Non c'è più nessuna malta interna: i pannelli sono separati da **48 px di carta**, e l'identificazione del componente è portata dal molo (2 px `--hairline-strong`, **3,59:1** su `--min-2`, **3,37:1** su `--min-0`) e dall'ormeggio (3 px `--route-n`, **5,96–8,05:1** su `--min-2`). Nessun confine informativo sotto il 3:1. L'argomento di §1.5 è riscritto con la metrica giusta (ΔE2000). |
| 8 | Togliere il bordo bronzo da `.btn--seal` | **FATTO** | §4.5. La classe `btn--seal` non esiste più. L'azione è SECONDARY come §10 la definisce: `border-color: var(--hairline-strong)` — **3,03:1** su `--seal-100`, ricalcolato — e `color: var(--ink)` a 13,14:1, altezza 48 px. Il bronzo resta su filetto e glifo. |
| 9 | Delimitare la riprogettazione di `empty_state.html` | **FATTO — non si tocca** | §4.8. `components/empty_state.html` non cambia di un byte: `role="status"`, il ramo `action_label`/`action_url` e l'icona restano. `_news.html` avvolge l'include in `.home-news__empty` e **questa spec stila solo quel discendente**. Gli altri 20 chiamanti non vedono nulla. §9.6 resta di chi lo possiede. |
| 10 | Cancellare `.reglist`; usare il reveal esistente | **FATTO** | §4.4: `.reglist` è cancellata, `.pathway-list` è migliorata **in posto** ed è l'unica grammatica di riga della superficie. §5: questa spec **non spedisce nessun reveal**; dichiara quale dei quattro ruoli della spec `scroll` prende ogni oggetto, e argomenta in §5 perché un fade-up scaglionato non è l'ingresso giusto. |
| 11 | Secondo canale sulla tacca; correggere §1.11; 44 px e row-gap | **FATTO / in parte CONTESTATO** | La tacca non esiste più (rail tagliato). §1.11 è corretto sopra: **il bersaglio da 141 px c'era già, l'accusa 2.5.8 è ritirata**; il difetto vero è l'anello di focus da 13 px, e il rimedio è misurato: l'anello passa alla riga intera, **133 px** a 1440 e **161 px** a 390. I link del congedo: **44 px misurati** su tutti e 16, `row-gap: var(--s-1)` = 4 px. |
| 12 | Rispondere alla commissione vera | **FATTO** | §4.9, che è la parte più lunga di questo documento. La fotografia **c'è nel repository** (15 slug, 73 file, quattro dei quali già assegnati ai quattro accessi) e **non esce**; la causa esatta è nominata; la decisione è messa al committente per iscritto, con il brief, il budget, i byte e la percentuale di superficie fotografica prima e dopo. «Immagini: zero nuove» è ritirata. |

### 2.1 Punti della revisione che contesto, con la misura

1. **«§1.11 è un errore di misura» — d'accordo sul bersaglio, non sulla conclusione.**
   Il revisore scrive: «`.pathway-list__title a::after { inset: 0 }` dà già un bersaglio da
   141 px, quindi l'accusa 2.5.8 è falsa e la riga da 56 px proposta è una regressione».
   **La prima metà è giusta e l'ho ritirata.** La seconda no: `.reglist` da 56 px è cancellata,
   ma non perché fosse una regressione del bersaglio — perché era una seconda grammatica
   identica. E resta un difetto che la revisione non nomina: **l'indicatore di focus misura
   13 px** (`.focus()` sul nodo vivo: `height: 13`, `outline: rgb(29,138,147) solid 2px`,
   `outline-offset: 2px`; l'elemento di riga ha `outline: none`). Con la correzione di §4.4 lo
   stesso nodo misura **133 px** a 1440 e **161 px** a 390. La riga cresce, non si accorcia:
   **141 px → 133 px** a 1440 perché la descrizione passa a `--t-body` su 64ch, e il bersaglio
   resta 4,4 volte il minimo della 2.5.8.

2. **«§4.7 taglia quattro destinazioni di navigazione» — vero nel round 1, e il numero vero è
   peggiore di quello che dice la revisione.**
   La revisione dice «5 legali + 9 navigazione + email + antifrode». È esatto **a :8771**.
   A **:8770**, che è l'altra configurazione viva, ho contato **12 link**: email + 5 legali +
   Accueil + **5** righe di `footer_menu`, e nessun antifrode. Quindi `footer_menu` non è «una
   misura di un seed»: è una lunghezza che **cambia fra due server accesi adesso**, 8 contro 5.
   Qualunque layout che nomini un numero di voci è rotto per costruzione. §4.7 ne tiene conto.

3. **«§1.5 condanna i pannelli con 1,37:1 e li ricostruisce a 1,37:1» — la contraddizione c'era,
   ma anche la premessa era sbagliata.**
   Il rapporto di contrasto WCAG non misura se due superfici si distinguono. Ricalcolato in
   CIELAB: `--min-1` su `--min-0` = **ΔE2000 1,99**, sotto la soglia di percettibilità. Quindi
   l'accusa del round 1 («1,06:1, 1,08:1») era giusta nella conclusione e sbagliata nello
   strumento. In questo round la misura è ΔE2000 dappertutto e il confine informativo è sempre
   ≥ 3:1 in WCAG **perché è un bordo, non un fondo**.

4. **«§4.4(a) disegna la graticola in grigio invece che nel teal del territorio» — accolto, ma
   la riparazione non è cambiare il colore.** La graticola è già assegnata: la spec
   `backgrounds` §4.2 la definisce a `--grat-module: 160px` — **lo stesso modulo di
   `scripts/territory.py`** — con `--grat-ink` a 2,8 % su carta, dentro `.ground::before`, con
   lume, grana e rampe. Riscriverla qui in un altro colore avrebbe prodotto **due sistemi di
   fondo sulla stessa pagina**. Cancellata (§9).

---

## 3. UI-UX-PRO-MAX e 21ST.DEV — che cosa resta dopo la revisione

Le interrogazioni del round 1 restano valide come registro di lavoro (il revisore le ha rieseguite
e sono tornate identiche, incluso il «0 risultati» della query sugli avvisi istituzionali). Ciò che
cambia è **che cosa ne sopravvive al taglio**:

| Fonte | Round 1 | Round 2 |
|---|---|---|
| `hirael/feature-10` — bento `gap-px bg-border` | il pattern portante di §4.2 | **RESPINTO IN BLOCCO.** Il revisore ha ragione: `gap: 1px; background: var(--mortar)` è il cliché shadcn/Tailwind 2024-26, e rinominare `bg-border` in `--mortar` non lo cambia. Resta soltanto: `tabular-nums` e `rtl:rotate-180` sulla freccia — due dettagli, non un'architettura. |
| `ln-dev7/footer-17` — due righe, due colonne in mobile | forma del congedo | **TENUTO nella forma** (identità sopra, rotte sotto; due colonne strette in mobile, non una colonna lunga — misurato: 1 307 → 1 148 px a 390). **RESPINTA** la CTA assente: l'antifrode resta un controllo bordato, non una nota. |
| `cnippet-dev/v-alert-6`, `shadcn/alert` | prova d'accusa | invariato: triangolo + titolo + descrizione in una scatola **è** il difetto 1.8. §4.5 non prende nulla da qui. |
| `ibelick/scroll-progress` — indice laterale | il rail dei movimenti | **RESPINTO.** Era il sommario di un sito di documentazione e appartiene alla spec `scroll` (§4.5, `readbar`), dove è già disegnato meglio, con `scroll(root block)` nativo e le tacche costruite dalle intestazioni vere. |
| `shadcndesign/cta-section-1` | proporzione della fascia di chiusura | **TENUTO** solo come proporzione (etichetta, titolo, una frase, **una** azione) per la soglia di §4.7. Respinto il fondo in tinta piatta e il tono «get started». |
| `ziegfiroyt/blog25` — registro senza schede | sostituiva `card.html` nelle attualità | **RESPINTO per vincolo verificabile**: `apps/pages/tests/test_home.py:408` asserisce `<h3 class="card__title"><a href="…">` dentro il blocco `news`. Le attualità restano schede; §4.6 le rende **piatte** (`card--flat`, ramo già esistente del componente), che è una riga di template e nessuna classe nuova. |
| «sage neutral + calm teal» (query colore) | origine di `--mortar-edge` | invariato nella conclusione — **il problema non sono le tinte, è il rapporto del confine** — ma il token inventato è ritirato: `--hairline-strong` esisteva già ed è quello che il sistema prescrive. |

---

## 4. LA PROPOSTA — «IL MARGINE»

Sotto l'hero non ci sono quattro movimenti. C'è **una pagina con un margine solo.**

Ogni oggetto di questa superficie è legato allo **stesso margine di lettura**: il molo lo tocca con
l'ormeggio dei quattro pannelli, i percorsi con il filetto delle righe, l'orientamento con la
riga del testo prescritto, la minuta con il filetto del sigillo, la soglia con il montante
dell'arco. Scorrendo 7 400 px si vede **una sola linea verticale sul bordo di lettura**, che
cambia peso e colore a seconda del registro in cui si sta: teal delle vie → ardesia dei percorsi →
bronzo dell'atto → teal della soglia. Non è un ornamento e non è un indice: è il bordo del
documento, e dice in quale parte del documento sei senza scrivere una parola e senza muovere un
pixel.

Questo è **il momento d'autore** di questa superficie, ed è verificabile: un ritaglio di 200 px
qualunque, preso in qualunque punto sotto l'hero, contiene quel margine e lo identifica.
È anche la ragione per cui non c'è più nessun numero romano: la posizione nel documento la dice
il margine, non un'etichetta.

### 4.0 Il meccanismo — `[data-section]`, e nient'altro

Il round 1 derivava i movimenti «dalla classe di rango già presente». Era **falso**: `section--c`
e `section--d` compaiono in più di un gruppo, e il raggruppamento vero era per chiave di sezione,
che vive in `services.py`.

La derivazione giusta era già nel DOM e il round 1 non l'ha vista: **ogni partial emette già
`data-section="<chiave>"`** (verificato in pagina: `hero banner entrances orientation pathways
pilot trust antifraud news ecosystem reserved`). Il CSS seleziona su quell'attributo.
Conseguenze, tutte verificate su entrambe le configurazioni vive:

- **riordino dal back-office**: irrilevante. Ogni sezione si veste da sé; non esiste nessun
  oggetto che dipenda dall'ordine.
- **sezione spenta o cancellata dal gate**: irrilevante. Non c'è nessuna numerazione che possa
  saltare, nessun gruppo che possa restare vuoto, nessun protagonista che possa mancare.
  A :8770 mancano `pilot`, `antifraud`, `news` e `reserved` e **non manca nulla del disegno**
  tranne gli oggetti di quelle quattro sezioni.
- **sezione nuova**: eredita il trattamento di base (`.shead` + il margine) senza una riga.
- **`data-movement`**: non esiste. Nessun `{% if s.key in … %}`, nessun campo in `services.py`,
  nessuna decisione chiesta al Council.

Regola dura, perché un attributo di dato è anche un contratto: **il CSS può leggere
`[data-section]`, mai scriverlo, e nessun selettore di questa spec dipende da `:nth-child` sulla
lista delle sezioni.** (Gli unici `:nth-child` sono dentro il molo, che ha esattamente quattro
figli per contratto di template — `test_home.py:545` lo asserisce.)

### 4.1 Token — **zero nuovi**

Il round 1 proponeva `--seal-050 #E7DDCD` e tre alias. Tutti ritirati:

| round 1 | round 2 |
|---|---|
| `--seal-050 #E7DDCD` | **ritirato.** `--seal-100 #EFE6DA` esiste già in §1.1 e misura ΔE2000 **5,40** contro `--min-0` — sopra soglia. Emendamento 1. |
| `--mortar: var(--hairline)` | **ritirato.** Non c'è più nessuna malta. |
| `--mortar-edge: var(--hairline-strong)` | **ritirato.** Era un alias di un token esistente; si usa `--hairline-strong` col suo nome. |
| `--graticule-pitch: 160px` | **ritirato.** È `--grat-module` della spec `backgrounds`. |
| `--rail-inline: 88px` | **ritirato** col rail. |

**Rapporti usati da questa superficie, tutti ricalcolati il 24 settembre** (WCAG 2.x, luminanza
relativa; nessuno ripreso da un documento):

| combinazione | rapporto | uso |
|---|---|---|
| `--ink` su `--min-2` | **15,56** | titolo e corpo dei pannelli |
| `--ink-2` su `--min-0` / `--min-2` | **6,46** / 6,84 | glosse e lead |
| `--ink-3` su `--min-0` | **5,53** | folio, date, didascalie |
| `--accent` su `--min-2` / `--min-0` | **6,05** / 5,69 | l'unico accento interattivo |
| `--accent-ring` su `--min-0` / `--min-2` | **3,70** / 3,94 | anello di focus |
| `--hairline-strong` su `--min-0` / `--min-2` / `--min-1` / `--seal-100` | **3,37** / **3,59** / **3,14** / **3,03** | **ogni confine che porta informazione** |
| `--route-1/2/3/4` su `--min-2` | **6,05 / 6,76 / 8,05 / 5,96** | gli ormeggi |
| `--seal-600` su `--seal-100` / `--min-0` | **3,86** / 4,30 | filetto e glifo della minuta |
| `--ink` / `--ink-2` / `--ink-3` su `--seal-100` | **13,14 / 5,80 / 4,97** | testo della minuta |
| `--on-dark` / `-2` / `-3` su `--mid-0` | **16,37 / 10,22 / 6,79** | congedo |
| `--accent-dark` su `--mid-0` | **10,57** | accento del congedo |
| `--terr-line` su `--mid-0` | **6,41** | glifo di chiusura (grafica) |
| `--hairline-dark-strong` **composito** su `--mid-0` | `rgba(214,226,228,.28)` sopra `#0A151C` = **`#434E54`**, cioè **2,16:1** | **decorativo soltanto**, mai un confine informativo — vedi §4.7 |
| `--hairline-dark` composito su `--mid-0` | **`#273238`**, **1,41:1** | idem |

> Nota di metodo: `DESIGN_SYSTEM_V2.md` §1.2 dà `--ink-3` su `--min-0` = 5,48. Ricalcolato qui
> fa **5,53** (L = 0,121079 contro 0,896283). Lo scarto è dello 0,9 % e non cambia nessuna
> decisione, ma la cifra che uso è quella che ho calcolato io. Stessa cosa per `--seal-600` su
> `--min-1`: il sistema non la dà, misura **3,99**.

### 4.2 La testata — da colonna di 420 px a oggetto a due fuochi

`templates/pages/partials/_section_header.html`. **Contratto invariato** (`title_id`, `heading`,
`intro`, `fallback_title`, `eyebrow`, `date`). **Nessuna classe rinominata**: `section__header`,
`section__title`, `section__lead`, `folio`, `folio__head`, `folio__date` restano tutte, perché
`apps/pages/tests/test_home.py:247, :505, :507, :522` asseriscono la stringa esatta
`<h2 class="section__title" id="…">`.

Tre cose cambiano: si aggiunge `shead` come classe di composizione, si toglie l'ordinale da 44 px
(la posizione nel documento la dicono il margine e il `readbar` della spec `scroll`; un numero
d'ordine di sezione non è un'informazione per un visitatore), e si aggiunge un filetto che
attraversa la misura.

```django
{% comment %}
Contratto invariato. `date` è «una data di revisione OPPURE una fonte» (vedi il commento
originale di questo file): NON è un <time>, perché una fonte dentro un <time> senza `datetime`
è markup non valido. Resta uno <span> con cifre tabellari.
{% endcomment %}
<header class="section__header shead"{% if rank %} data-rank="{{ rank }}"{% endif %}>
  {% if eyebrow %}
  <p class="folio shead__folio">
    <span class="folio__head">{{ eyebrow }}</span>
    <span class="shead__rule" aria-hidden="true"></span>
    {% if date %}<span class="folio__date">{{ date }}</span>{% endif %}
  </p>
  {% endif %}
  {% if heading %}<h2 class="section__title" id="{{ title_id }}"{% if heading.lang %} lang="{{ heading.lang }}"{% endif %}>{{ heading }}</h2>{% else %}<h2 class="visually-hidden" id="{{ title_id }}">{{ fallback_title }}</h2>{% endif %}
  {% if intro %}<p class="section__lead"{% if intro.lang %} lang="{{ intro.lang }}"{% endif %}>{{ intro }}</p>{% endif %}
</header>
```

Il ramo `{% else %}<h2 class="visually-hidden">` — il bersaglio di `aria-labelledby` quando
l'editor lascia il titolo vuoto, coperto da `test_blank_heading_keeps_an_accessible_section_title`
— **è ripristinato verbatim**. `{% if heading.lang %}` e `{% if intro.lang %}` anche: sono la
marcatura 3.1.2 della lingua di parte sui testi prescritti senza versione ufficiale IT/EN/AR.

`rank` è passato da un solo chiamante, `_entrances.html`:
`{% include "pages/partials/_section_header.html" with … rank="open" %}`. Gli altri cinque non
passano nulla e prendono il rango interno. È l'unica variabile nuova del contratto ed è
facoltativa.

```css
/* static/css/v3/sections.css */

/* 1.4 — la colonna da 420,75 px. `layout.css:171` la impone a OGNI `.section__header`; qui si
   toglie il tetto e si dà la misura al titolo e al lead separatamente. Effetto fuori home: §4.10. */
.section__header { max-inline-size: none; }

.shead {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  column-gap: var(--gutter);
  row-gap: var(--s-4);
  margin-block-end: var(--s-12);
  align-items: end;
}
.shead__folio {
  grid-column: 1 / -1;
  display: flex; align-items: baseline; gap: var(--s-4); margin: 0;
  font-family: var(--f-mono);
  font-size: var(--t-folio); line-height: var(--t-folio-lh);
  letter-spacing: var(--track-folio); text-transform: uppercase;
  font-weight: 400;                      /* 1.3: era 600 */
  color: var(--ink-3);                   /* 5,53:1 */
  border-block-start: 0;                 /* 1.3: il folio aveva un 2px --ink-3 che ora è il filetto */
}
.shead__rule { flex: 1 1 auto; block-size: 1px; background: var(--hairline-strong); align-self: center; }  /* 3,37:1 */
.shead .folio__date { font-variant-numeric: tabular-nums; }
.shead .folio__ordinal { display: none; }   /* resta nel DOM: `test_home.py:230` lo asserisce */

.shead .section__title {
  grid-column: 1 / span 6; margin: 0;
  font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-band);              /* 32px — la famiglia V2, non --t-band-size */
  line-height: var(--t-band-lh);         /* 36px — la 1.2 si chiude usando la COPPIA giusta */
  letter-spacing: 0;
  color: var(--ink); max-inline-size: 18ch;
}
.shead .section__lead {
  grid-column: 8 / -1; margin: 0; align-self: end;
  font-family: var(--f-serif); font-style: italic;     /* 1.11 */
  font-size: var(--t-lead); line-height: var(--t-lead-lh);   /* 20/28 */
  color: var(--ink-2); max-inline-size: 38ch;
}
/* EMENDAMENTO 2 — un solo rango d'apertura per pagina */
.shead[data-rank="open"] .section__title {
  grid-column: 1 / span 7;
  font-size: var(--t-title); line-height: var(--t-title-lh);
  letter-spacing: -0.015em;              /* §3.2: tracking negativo solo >= 40px */
  max-inline-size: 15ch;
}
.shead[data-rank="open"] .shead__rule { block-size: 2px; }

/* la testata su capitolo mezzanotte (pilot) */
.chapter--dark .shead__folio { color: var(--on-dark-3); }              /* 6,44:1 su --mid-1 */
.chapter--dark .shead__rule  { background: var(--hairline-dark-strong); } /* decorativo: 2,20:1 composito */
.chapter--dark .shead .section__title { color: var(--on-dark); }       /* 15,51:1 */
.chapter--dark .shead .section__lead  { color: var(--on-dark-2); }     /* 9,68:1 */

@media (max-width: 63.999rem) {
  .shead { row-gap: var(--s-3); margin-block-end: var(--s-8); }
  .shead .section__title, .shead .section__lead { grid-column: 1 / -1; max-inline-size: 34ch; }
}
:lang(ar) .shead__folio { letter-spacing: normal; text-transform: none; }
:lang(ar) .shead .section__title { letter-spacing: 0; }    /* §3.2: tracking 0 in arabo, anche a 48px */
```

**Misurato in Chromium headless con questo CSS applicato alla pagina viva** (1440×900, `/fr/`,
:8771), contro la stessa pagina senza:

| | oggi | con la testata |
|---|---|---|
| larghezza dell'intestazione | 420,75 px | **1 240 px** (la misura intera) |
| titolo | 38 px / **36 px** di interlinea, peso 400 | **32 px / 36 px** interni, **48 px / 52 px** in apertura |
| lead | 22 px, `font-style: normal`, sotto il titolo | **20 px / 28 px corsivo**, larghezza 418 px, in colonna 8-12 |
| il vuoto più grande dell'intestazione | **819,25 px, tutto al bordo finale** | **411 px, fra i due fuochi, attraversato dal filetto** |
| filetto del folio | assente (il folio aveva un bordo chiuso a 420 px) | **1 082–1 127 px** secondo la lunghezza della testatina |

### 4.3 Il molo — i quattro accessi

§8.5 lo chiama «un molo di quattro pontili» e chiede: pannelli di livello 2, **indice**, etichetta
mono, glifo proprietario, **linea d'ormeggio che si traccia in hover/focus**, zig-zag 7/5 · 5/7,
bersaglio ≥ 44 px, l'intero pannello è il bersaglio. Esiste già quasi tutto, e il round 1
proponeva di sostituirlo con una griglia bento. Errore. Si **incornicia**, come dice la
direttiva, e la cornice non è un box.

**Markup: invariato.** `components/entrances.html` non cambia di un carattere.
`<ol class="register register--entrances">` → `<li class="register__item" data-route="…">` →
`<a class="entry">` → `span.entry__ordinal` + `svg.route__glyph` + `h3.entry__title` +
`span.entry__gloss` + `span.entry__cta` + `svg.entry__arrow`. Le asserzioni di
`test_home.py:208, :214, :217, :230, :247, :248, :545` e di `test_browser.py:120, :148, :174,
:247` continuano a passare perché **nessuna stringa di markup cambia**.

```css
/* static/css/v3/panels.css */
.register--entrances {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  column-gap: var(--gutter);
  row-gap: var(--s-12);                 /* 48px di CARTA: il separatore è lo spazio, non un filetto */
  margin: 0; padding: var(--s-8) 0 0; list-style: none;
  /* register.css disegna `.register { border-block: 2px solid var(--navy) }` = #0F2547, il navy
     del marchio sotto l'hero (difetto 1.1). Si ridichiarano ENTRAMBI i bordi. */
  border-block-start: 2px solid var(--hairline-strong);   /* IL MOLO — 3,37:1 su --min-0 */
  border-block-end: 0;
}
.register--entrances > .register__item { margin: 0; }
.register--entrances > .register__item:nth-child(1) { grid-column: 1 / span 7; }
.register--entrances > .register__item:nth-child(2) { grid-column: 8 / span 5; }
.register--entrances > .register__item:nth-child(3) { grid-column: 1 / span 5; }
.register--entrances > .register__item:nth-child(4) { grid-column: 6 / span 7; }
.register--entrances > [data-route="person"]      { --route: var(--route-1); }  /* 6,05:1 su --min-2 */
.register--entrances > [data-route="company"]     { --route: var(--route-2); }  /* 6,76:1 */
.register--entrances > [data-route="institution"] { --route: var(--route-3); }  /* 8,05:1 */
.register--entrances > [data-route="university"]  { --route: var(--route-4); }  /* 5,96:1 */

.register--entrances .entry {
  position: relative; display: grid;
  grid-template-columns: 96px minmax(0, 1fr);
  grid-template-areas: "glyph title" "glyph gloss" "cta cta";
  grid-template-rows: auto 1fr auto;
  column-gap: var(--s-6); row-gap: var(--s-3);
  align-items: start; block-size: 100%;
  /* NON p-6 uniforme: il lato d'ormeggio e il piede pesano di più (32) del capo e del lato
     libero (24). La spaziatura porta la gerarchia, che è l'anti-pattern che §1 di
     ANTI_PATTERNS nomina per nome. */
  padding: var(--s-6) var(--s-6) var(--s-8) var(--s-8);
  background: var(--min-2); color: var(--ink); text-decoration: none;
  border: 0; border-radius: 0;
  /* nessuna box-shadow: il rilievo del foglio (`--contact`, ruolo 2 di §2) lo dà `ground.css`
     della spec `backgrounds` quando arriva. `grep box-shadow` sui quattro file di questa spec
     restituisce ZERO. */
}
/* L'ORMEGGIO — l'unico elemento che identifica il pannello come componente, >= 3:1 ovunque. */
.register--entrances .entry::before {
  content: ""; position: absolute; inset-block: 0; inset-inline-start: 0;
  inline-size: 3px; background: var(--route, var(--route-1));
  transform: scaleY(0.38); transform-origin: top;
}
.register--entrances .entry:is(:hover, :focus-visible)::before,
.register--entrances .register__item:focus-within .entry::before { transform: scaleY(1); }
.register--entrances .entry:focus-visible { outline: 2px solid var(--accent-ring); outline-offset: 2px; }

.register--entrances .entry__ordinal {
  grid-area: glyph; align-self: start; justify-self: center;
  font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  font-variant-numeric: tabular-nums; letter-spacing: var(--track-folio); color: var(--ink-3);
}
.register--entrances .route__glyph {
  grid-area: glyph; align-self: start; margin-block-start: var(--s-6);
  inline-size: 96px; block-size: 64px; color: var(--route, var(--route-1));
}
.register--entrances .entry__title  { grid-area: title; margin: 0; font-family: var(--f-serif); font-weight: 400; font-size: var(--t-entry); line-height: var(--t-entry-lh); }
.register--entrances .entry__gloss  { grid-area: gloss; font-size: var(--t-body); line-height: var(--t-body-lh); color: var(--ink-2); max-inline-size: 46ch; }
.register--entrances .entry__cta    { grid-area: cta; align-self: end; justify-self: start; display: inline-flex; align-items: center; min-block-size: 44px; font-size: var(--t-ui); color: var(--accent); }
.register--entrances .entry__arrow  { grid-area: cta; align-self: center; justify-self: end; color: var(--accent); }

@media (prefers-reduced-motion: no-preference) {
  .register--entrances .entry::before { transition: transform var(--motion-fast) var(--ease-out); }
}
@media (max-width: 63.999rem) {
  .register--entrances { row-gap: var(--s-8); }
  .register--entrances > .register__item:nth-child(n) { grid-column: 1 / -1; }
}
@media (max-width: 47.999rem) {
  .register--entrances .entry {
    grid-template-columns: minmax(0, 1fr);
    grid-template-areas: "glyph" "title" "gloss" "cta";
    grid-template-rows: auto auto 1fr auto;
    padding: var(--s-5) var(--s-5) var(--s-6) var(--s-6);
  }
  .register--entrances .route__glyph { inline-size: 72px; block-size: 48px; margin-block-start: var(--s-2); }
}
@media (forced-colors: active) {
  .register--entrances .entry { border: 1px solid CanvasText; }
  .register--entrances .entry::before { background: CanvasText; forced-color-adjust: none; }
}
```

**Perché questo non è una card.** Una card è un rettangolo chiuso con quattro bordi uguali, un
raggio e un'ombra. Questo pannello ha **due bordi, di due pesi e due significati** — il molo
sopra (3,37:1, comune ai quattro) e l'ormeggio sul lato di lettura (5,96–8,05:1, diverso per
ciascuno) — e **due lati aperti sulla carta**. È una L, non un box: la forma di una lastra
appoggiata a un registro. È anche il motivo per cui la 1.4.11 è soddisfatta **per costruzione**
invece che per concessione: quello che identifica il componente non è il suo fondo (ΔE2000 1,53
contro la tela — invisibile, e va bene così, perché non è quello a identificarlo) ma i suoi due
bordi, entrambi sopra il 3:1.

**Perché l'ormeggio non è un `translateY(-2px)` con l'ombra.** §8.5 chiede letteralmente «linea
d'ormeggio che si traccia in hover/focus». Al riposo l'ormeggio è tracciato al **38 %** dell'altezza
del pannello: il pontile è ormeggiato, ma non del tutto. In hover o in focus scende a fondo. È
CAUSALITÀ resa come FEEDBACK, costa un `transform` su uno pseudo-elemento, non solleva niente e
non disegna nessuna ombra. Confronto onesto: il `translateY(-2px)` + `shadow-sm` del round 1 era
la `Card` di shadcn con altri token.

**Misurato** (1440×900, CSS applicato alla pagina viva): zig-zag conservato — pannelli
**713,3 / 502,7 / 502,7 / 713,3 px**, alti 320/320/348/348 (oggi 258/258/294/294, cresciuti perché
la glossa passa da `--t-small` a `--t-body` 17/28); `border-width: 0px` su tutti e quattro;
`box-shadow: none` su tutti e quattro; gli unici tre elementi con `box-shadow` su `main`
restano quelli dell'hero.

### 4.4 Il registro — una sola grammatica di riga

`.reglist` è **cancellata**. `components/pathway_list.html` è l'unica grammatica di riga della
superficie ed è migliorata in posto, con **le stesse classi** (`test_home.py:325` conta
`class="pathway-list__item"` × 8; `:313` verifica che a gate chiuso `pathway-list` **non** ci sia).

Una sola aggiunta al contratto del componente, facoltativa e retrocompatibile:

```django
{% comment %}
Contratto: `items` = [{title, text, url, lang, meta}] — `meta` è NUOVO e facoltativo (una data
di pubblicazione, una fonte). `lang` per l'intera lista. Ogni riga è interamente cliccabile
(link steso) e il link del titolo resta l'unico tab stop.
{% endcomment %}
<ol class="pathway-list"{% if lang %} lang="{{ lang }}"{% endif %}>
  {% for item in items %}
  <li class="pathway-list__item">
    <span class="pathway-list__num" aria-hidden="true"></span>
    <h3 class="pathway-list__title"{% if item.lang %} lang="{{ item.lang }}"{% endif %}>{% if item.url %}<a href="{{ item.url }}">{{ item.title }}</a>{% else %}{{ item.title }}{% endif %}</h3>
    {% if item.meta %}<p class="pathway-list__meta">{{ item.meta }}</p>{% endif %}
    {% if item.text %}<p class="pathway-list__desc"{% if item.lang %} lang="{{ item.lang }}"{% endif %}>{{ item.text }}</p>{% endif %}
    {% if item.url %}{% svg_icon "arrow" "icon pathway-list__arrow icon--flip-rtl" %}{% endif %}
  </li>
  {% endfor %}
</ol>
```

```css
/* static/css/v3/sections.css (suite) */
.pathway-list { border-block-start: 2px solid var(--hairline-strong); }   /* lo stesso molo */
.pathway-list__item {
  grid-template-columns: 4.5rem minmax(0, 1fr) auto;
  gap: var(--s-2) var(--s-6);
  padding-block: var(--s-5);
  border-block-end: 1px solid var(--hairline);       /* 1,37:1 — DECORATIVO: vedi sotto */
  min-block-size: 88px;
}
.pathway-list__num {
  font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  font-variant-numeric: tabular-nums; color: var(--ink-3);       /* 5,53:1 */
  align-self: start; padding-block-start: 6px;
}
.pathway-list__title { font-family: var(--f-serif); font-weight: 400; font-size: var(--t-entry); line-height: var(--t-entry-lh); }
.pathway-list__title a { color: var(--ink); }
.pathway-list__meta { grid-column: 2; margin: 0; font-family: var(--f-mono); font-size: var(--t-folio); font-variant-numeric: tabular-nums; color: var(--ink-3); }
.pathway-list__desc { grid-column: 2; color: var(--ink-2); font-size: var(--t-body); line-height: var(--t-body-lh); max-inline-size: 64ch; }
.pathway-list__arrow { color: var(--accent); }

/* 1.11 — l'anello di focus passa dal box in linea di 13 px alla riga intera. */
.pathway-list__title a:focus-visible { outline: none; }
.pathway-list__item:focus-within { outline: 2px solid var(--accent-ring); outline-offset: 2px; }  /* 3,70:1 */
```

**Il filetto a 1,37:1 è ammesso qui e non lo era nel round 1.** Differenza sostanziale: nel bento
del round 1 la malta era **l'unica cosa** che diceva dove finiva una cella e cominciava la
successiva, quindi portava informazione e doveva stare a 3:1. In una lista, il confine fra due
righe è già portato dal numero d'ordine, dal titolo in serif e da 88 px di altezza minima: il
filetto è **ritmo, non informazione**. La 1.4.11 si applica a «visual information required to
identify user interface components and states»; qui non è richiesta. Il confine che *porta*
informazione — l'inizio della lista — è il molo a 2 px e 3,37:1.

**Misurato**: bersaglio puntatore invariato (la riga intera, `::after { inset: 0 }` conservato),
**133 px** a 1440 e **161 px** a 390 (prima 141/169 — la riga si accorcia di 8 px perché la
descrizione sale a `--t-body` su 64ch, cioè ~73 caratteri per riga, sotto il 75 di §3.2).
Indicatore di focus: **da 13 px a 133 px**.

### 4.5 La minuta — l'avviso antifrode

Non una casella: una **fascia a tutta pagina su carta d'atto**, che esce dal contenitore e tocca
i due bordi. È l'unico oggetto della superficie che lo fa, ed è il motivo per cui si legge come
un documento inserito nel documento e non come una striscia.

**Markup — ogni ramo dell'originale conservato, `#icon-shield` compreso.** Nessun simbolo nuovo
in `icons.svg` (il round 1 ne proponeva uno, `icon-seal`: ritirato — lo scudo è il glifo che il
sistema ha già e che `test_home.py:363` e `test_institutional.py:200` asseriscono).

```django
<section class="section home-antifraud avviso" id="{{ s.anchor }}" aria-labelledby="home-antifraud-title" data-section="antifraud">
  <div class="avviso__sheet">
    <div class="container avviso__inner">
      <p class="antifraud-panel__mark avviso__seal" aria-hidden="true">{% svg_icon "shield" "icon icon--xl" %}</p>
      <div class="antifraud-panel">
        <h2 class="antifraud-panel__title" id="home-antifraud-title"{% if d.title.lang %} lang="{{ d.title.lang }}"{% endif %}>{{ d.title }}</h2>
        <p class="antifraud-panel__body"{% if d.body.lang %} lang="{{ d.body.lang }}"{% endif %}>{{ d.body }}</p>
        {% if s.note %}<p class="home-section__note"{% if s.note.lang %} lang="{{ s.note.lang }}"{% endif %}>{{ s.note }}</p>{% endif %}
        {% if d.url %}<p class="antifraud-panel__actions"><a class="btn btn--secondary btn--arrow" href="{{ d.url }}">{% translate "Lire la page « Attention aux fraudes »" %} {% svg_icon "arrow" "icon icon--flip-rtl" %}</a></p>{% endif %}
      </div>
    </div>
  </div>
</section>
```

```css
/* static/css/v3/notice.css */
.avviso { padding-block: 0; }                       /* il rango verticale passa al foglio */
.avviso__sheet {
  background: var(--seal-100);                      /* EMENDAMENTO 1 — DeltaE2000 5,40 su --min-0 */
  border-block-start: 4px solid var(--seal-600);    /* 3,86:1 sul proprio fondo, 4,30:1 sulla tela */
  border-block-end: 1px solid var(--hairline-strong);  /* 3,03:1 */
  padding-block: var(--s-16);
}
.avviso__inner {
  display: grid; grid-template-columns: repeat(12, minmax(0, 1fr));
  column-gap: var(--gutter); row-gap: var(--s-6); align-items: stretch;
}
/* il margine dell'atto: lo scudo in testa, e sotto di lui il filetto che scende per tutta
   l'altezza del testo. Grafica pura, niente parole, nessun glifo nuovo. */
.avviso__seal {
  grid-column: 1 / span 2; margin: 0; color: var(--seal-600);
  display: flex; flex-direction: column; align-items: center; gap: var(--s-6);
  background: none; border: 0; border-radius: 0;    /* 1.8: il tondo grigio sparisce */
}
.avviso__seal .icon { inline-size: 96px; block-size: 96px; flex: 0 0 auto; }
.avviso__seal::after { content: ""; inline-size: 1px; flex: 1 1 auto; background: var(--seal-600); }

.avviso .antifraud-panel {
  grid-column: 3 / span 8;
  display: block; background: none; border: 0; padding: 0; border-radius: 0;
}
.avviso .antifraud-panel__title {
  margin: 0 0 var(--s-4);
  font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-band); line-height: var(--t-band-lh); color: var(--ink);   /* 13,14:1 */
}
.avviso .antifraud-panel__body {
  margin: 0 0 var(--s-6);
  font-family: var(--f-sans);                       /* 1.8: la voce UI, non la prosa editoriale */
  font-size: var(--t-body); line-height: var(--t-body-lh); color: var(--ink);
  max-inline-size: 62ch;
}
.avviso .home-section__note { color: var(--ink-2); font-size: var(--t-small); }  /* 5,80:1 */
.avviso .antifraud-panel__actions { margin: 0; }
/* §10 SECONDARY, senza una goccia di bronzo. Si scrivono i CUSTOM PROPERTY del sistema
   (`components.css:10-39` compone .btn da --btn-bg / --btn-fg / --btn-border), non le proprietà
   risolte: scrivere `border-color` direttamente lascerebbe l'hover al valore di riposo. */
.avviso .btn--secondary {
  --btn-bg: transparent;
  --btn-fg: var(--ink);                             /* 13,14:1 */
  --btn-border: var(--hairline-strong);             /* 3,03:1 su --seal-100 */
  --btn-bg-hover: transparent;
  --btn-fg-hover: var(--ink);
  min-block-size: 48px;    /* --control-height misura 44px; §10 chiede 48 sui controlli: è della spec `buttons` */
}
/* `.btn` non legge nessun --btn-border-hover, ma transisce `border-color`: qui va la proprietà. */
.avviso .btn--secondary:hover { border-color: var(--ink-2); }     /* 5,80:1 */
.avviso .btn--secondary:focus-visible { outline: 2px solid var(--accent-ring); outline-offset: 2px; }  /* 3,33:1 */

/* Se il back-office mette l'avviso subito dopo il capitolo mezzanotte, la fascia si posa sul
   buio esistente invece di aprire un terzo capitolo. Nessun JS, nessun :has(). */
.chapter--dark + .avviso .avviso__sheet {
  background: var(--mid-2); border-block-start-color: var(--seal-300); border-block-end-color: var(--hairline-dark-strong);
}
.chapter--dark + .avviso :is(.antifraud-panel__title, .antifraud-panel__body) { color: var(--on-dark); }  /* 14,08:1 */
.chapter--dark + .avviso .home-section__note { color: var(--on-dark-2); }                                /* 8,79:1 */
.chapter--dark + .avviso .avviso__seal { color: var(--seal-300); }                                       /* 7,00:1 */
.chapter--dark + .avviso .avviso__seal::after { background: var(--seal-300); }
.chapter--dark + .avviso .btn--secondary { --btn-border: var(--on-dark-3); --btn-fg: var(--on-dark); }    /* 5,85:1 / 14,08:1 */

@media (max-width: 63.999rem) {
  .avviso__sheet { padding-block: var(--s-12); }
  .avviso__seal { grid-column: 1 / -1; flex-direction: row; align-items: center; }
  .avviso__seal .icon { inline-size: 64px; block-size: 64px; }
  .avviso__seal::after { inline-size: auto; block-size: 1px; }
  .avviso .antifraud-panel { grid-column: 1 / -1; }
}
@media (forced-colors: active) {
  .avviso__sheet { background: Canvas; border-block-start: 4px solid CanvasText; border-block-end: 1px solid CanvasText; }
  .avviso__seal, .avviso__seal::after { color: CanvasText; background: CanvasText; }
}
```

**Risposta al segnale «cookie banner govtech».** Il revisore ha ragione che una fascia beige con
un filetto bronzo è a un cattivo render dal `alert-warning` di Bootstrap. La difesa non è il
colore, è **l'apparato**: nessuna icona in un tondo, nessun triangolo, nessun rosso, nessun
raggio, nessuna barra colorata a sinistra, nessun controllo di chiusura; **un margine di due
colonne** con il sigillo in testa e il filetto dell'atto che scende per tutta l'altezza del
testo; il titolo in serif e il corpo nella voce UI; un filetto alto di 4 px e uno basso di 1 px,
cioè **due pesi diversi**, che è ciò che distingue una testata da una cornice. E un banner di
consenso non è mai alto 509 px né occupa un rango verticale intero.

**Misurato** (1440×900, CSS applicato alla pagina viva):

| | oggi | con la minuta |
|---|---|---|
| caratteri per riga del corpo | **91,4** (640 caratteri su 7 righe di 822,8 px) | **71,1** (640 su 9 righe di 588,1 px) — dentro il 75 di §3.2 |
| voce del corpo | Newsreader 22 px/36,3 px | Fira Sans 17 px/28 px |
| fondo | `#F4F3F0`, identico alla tela | `#EFE6DA`, ΔE2000 5,40 dalla tela |
| bordo | `border-inline-start: 4px rgb(15,37,71)` (navy del marchio) | `border-block-start: 4px rgb(140,109,75)`, `border-block-end: 1px rgb(122,134,139)` |
| altezza | 537 px (sezione), 472 px (pannello) | **510 px** a 1440, **798 px** a 390 (oggi 917) |
| larghezza | 1 240 px in colonna | **1 440 px**, a tutta pagina |

### 4.6 Attualità ed ecosistema

**Attualità.** Le schede restano — `test_home.py:408` asserisce `<h3 class="card__title"><a
href="…">` dentro il blocco `news`, e togliere `card.html` da qui romperebbe quella prova per
guadagnare una grammatica che §4.4 già fornisce. Cambia **una parola nel template**:

```django
{% include "components/card.html" with title=article.title url=article.url eyebrow=article.category text=article.summary meta=article.date lang=article.lang flat=True %}
```

`flat` è un parametro **già esistente** del componente («True → no box, hairline rule only»). Il
risultato è tre lastre piatte sotto un filetto invece di tre scatole. E il link d'indice risale
accanto all'intestazione invece di restare abbandonato 600 px più in basso:

```django
{# _news.html, subito dopo l'include di _section_header.html #}
{% if d.index_url %}<p class="home-section__more home-news__index"><a class="link-arrow" href="{{ d.index_url }}">{% translate "Toutes les actualités" %} {% svg_icon "arrow" "icon icon--flip-rtl" %}</a></p>{% endif %}
```

```css
.home-news .shead { margin-block-end: var(--s-6); }
.home-news__index { margin: 0 0 var(--s-8); }
.home-news__index a { min-block-size: 44px; display: inline-flex; align-items: center; gap: var(--s-2); }
.home-news__grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: var(--gutter); border-block-start: 2px solid var(--hairline-strong); padding-block-start: var(--s-6); }
.home-news__grid .card--flat { padding: 0 var(--s-6) 0 0; border: 0; border-radius: 0; background: none; }
.home-news__grid .card__eyebrow { font-family: var(--f-mono); font-size: var(--t-folio); letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--ink-3); }
.home-news__grid .card__title { font-family: var(--f-serif); font-weight: 400; font-size: var(--t-entry); line-height: var(--t-entry-lh); }
.home-news__grid .card__title a { color: var(--ink); }
.home-news__grid .card__meta { font-family: var(--f-mono); font-size: var(--t-folio); font-variant-numeric: tabular-nums; color: var(--ink-3); }
@media (max-width: 63.999rem) { .home-news__grid { grid-template-columns: 1fr; row-gap: var(--s-6); } }
```

**Ecosistema.** `_ecosystem.html` cambia **solo classi di contenitore**; entrambi i rami del
gate G3 restano, compreso quello che il round 1 aveva dimenticato:

```django
{% if d.promoter_quote %}
<p class="home-ecosystem__text"{% if d.promoter_quote.lang %} lang="{{ d.promoter_quote.lang }}"{% endif %} data-faq="{{ d.promoter_quote.key }}">{{ d.promoter_quote.answer }}</p>
{% else %}
<p class="home-ecosystem__text">{% blocktranslate with project=site.project_name promoter=d.promoter %}{{ project }} est promu par {{ promoter }}.{% endblocktranslate %}</p>
{% endif %}
```

```css
.home-ecosystem__grid { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: var(--gutter); row-gap: var(--s-8); }
/* NIENTE bronzo qui: il promotore è un'associazione privata e il commento del template dice
   «nothing suggests a public authority». Il bronzo è dei sigilli, e sulla home c'è un solo
   oggetto d'autorità, la minuta. Il margine del plinto è il neutro forte. */
.home-ecosystem__promoter { grid-column: 1 / span 7; padding-inline-start: var(--s-6); border-inline-start: 3px solid var(--hairline-strong); }  /* 3,37:1 */
.home-ecosystem__partners { grid-column: 9 / span 4; }
.home-ecosystem__label { font-family: var(--f-mono); font-size: var(--t-folio); letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--ink-3); margin: 0 0 var(--s-2); }
.home-ecosystem__name { font-family: var(--f-serif); font-weight: 400; font-size: var(--t-entry); line-height: var(--t-entry-lh); margin: 0 0 var(--s-3); }
.home-ecosystem__list { list-style: none; margin: 0; padding: 0; border-block-start: 1px solid var(--hairline-strong); }
.home-ecosystem__partner { display: grid; grid-template-columns: 40px minmax(0, 1fr); column-gap: var(--s-4); align-items: center; min-block-size: 56px; border-block-end: 1px solid var(--hairline); }
.home-ecosystem__logo { grid-column: 1; max-inline-size: 40px; block-size: auto; }
.home-ecosystem__partner-name { grid-column: 2; font-size: var(--t-ui); }
.home-ecosystem__empty { font-size: var(--t-body); color: var(--ink-2); max-inline-size: 46ch; }
@media (max-width: 63.999rem) { .home-ecosystem__promoter, .home-ecosystem__partners { grid-column: 1 / -1; } }
```

**La pillola di stato del partner autorizzato è cancellata.** Il revisore ha ragione:
`_ecosystem.html` espone solo `card.partner.name` e `card.partner.logo_public`,
`partners.services.authorized_partners()` restituisce **solo** partner autorizzati (gate G6), e
non esiste nessun campo di stato, nessuna parola, nessuna chiave di traduzione. Inventare una
formulazione pubblica sull'autorizzazione legale di un partner su una pagina il cui commento di
template dice «nothing suggests a public authority» era un difetto di verità di prodotto, non
una scelta di disegno. La frase prescritta sull'autorizzazione scritta resta parola per parola
dov'è: è un fatto giuridico e non ha bisogno di un badge.

### 4.7 Il congedo — la soglia e il piè di pagina, **vicini, non fusi**

Il round 1 li fondeva in un solo oggetto su `--mid-0`. Era sbagliato due volte: apriva un terzo
capitolo mezzanotte (HOME ne ammette due, già spesi da hero e rotta) e chiedeva a un elemento di
avvolgere una sezione dentro `<main>` e un `contentinfo` fuori.

**La decisione, e il suo costo.** `_reserved` **resta** dentro `<main id="main-content">` e dentro
il ciclo di `home_sections()` — quindi resta ordinabile e gateabile dal back-office.
`partials/footer.html` **resta** fratello di `</main>` — quindi resta `contentinfo`. Non c'è
nessun elemento che li avvolge. Sono **due elementi che condividono una grammatica**: la soglia
chiude la carta, il congedo la porta nel buio. *Costo*: la continuità è visiva, non strutturale,
quindi dipende dal fatto che i due fondi combacino — la soglia finisce su `--min-0` e la rampa
del piè di pagina (`th--from-paper` della spec `backgrounds` §4.5) comincia su `--min-0`. Se
quella spec non arriva, fra i due resta un taglio netto invece di una discesa: peggiore, non
rotto. Il collaudo è un campione di pixel a `x = 40` sul confine (§8).

#### (a) La soglia — `_reserved.html`

È il momento in cui la pagina si chiude con la stessa grammatica con cui si è aperta: la porta.
L'arco è **disegnato a scala architettonica**, non come glifo, e la CTA prescritta sta nella sua
apertura.

```django
<section class="section section--rule home-reserved soglia" id="{{ s.anchor }}" aria-labelledby="home-reserved-title" data-section="reserved">
  <div class="container soglia__inner">
    <p class="home-reserved__mark soglia__arch" aria-hidden="true">
      <svg viewBox="0 0 200 320" fill="none" stroke="currentColor" stroke-width="1.5" focusable="false">
        <path d="M8 318V118a92 92 0 0 1 184 0v200"/>
        <path d="M26 318V124a74 74 0 0 1 148 0v194"/>
      </svg>
      <span class="soglia__step"></span><span class="soglia__step"></span><span class="soglia__step"></span>
    </p>
    <div class="home-reserved__text soglia__text">
      <h2 class="home-reserved__title" id="home-reserved-title"{% if d.title.lang %} lang="{{ d.title.lang }}"{% endif %}>{{ d.title }}</h2>
      <p class="home-reserved__body"{% if d.body.lang %} lang="{{ d.body.lang }}"{% endif %}>{{ d.body }}</p>
    </div>
    <a class="btn btn--primary home-reserved__button" href="{{ d.url }}"{% if d.button.lang %} lang="{{ d.button.lang }}"{% endif %}>{{ d.button }}</a>
  </div>
</section>
```

Il lucchetto grigio sparisce; `home-reserved__mark`, `home-reserved__title`, `home-reserved__body`
e `home-reserved__button` restano. `section--rule` è la classe che la spec `scroll` §4.2 chiede su
una sezione che segue un'altra con lo stesso suolo (sulla home `ecosystem → reserved` è l'unico
caso). Il bottone passa da `btn--secondary` a `btn--primary`: §8.4 e §10 vogliono **una** azione
primaria alla soglia, e `v3/buttons.css` la dipinge già in `--accent` con testo `--min-0`
(5,69:1) — non più il navy del marchio.

```css
/* static/css/v3/congedo.css */
.soglia__inner {
  display: grid; grid-template-columns: 200px minmax(0, 1fr) auto;
  column-gap: var(--s-12); row-gap: var(--s-6); align-items: end;
  padding-block: var(--s-16) var(--s-12);
  border-block-start: 2px solid var(--hairline-strong);
}
.soglia__arch { position: relative; margin: 0; display: block; inline-size: 200px; block-size: 320px; color: var(--terr-line-lt); }  /* 5,69:1 — grafica del territorio su chiaro */
.soglia__arch svg { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; }
/* i tre gradini: larghezza data dagli inset, nessun transform permanente. Il primo figlio di
   .soglia__arch è l'<svg>, quindi i gradini sono nth-child 2, 3, 4. */
.soglia__step { position: absolute; block-size: 6px; background: var(--accent); }   /* 5,69:1 */
.soglia__step:nth-child(2) { inset-block-end: 0;    inset-inline: 0; }
.soglia__step:nth-child(3) { inset-block-end: 12px; inset-inline: 14px; }
.soglia__step:nth-child(4) { inset-block-end: 24px; inset-inline: 28px; }
.soglia__text { max-inline-size: 52ch; }
.home-reserved__title { font-family: var(--f-serif); font-weight: 400; font-size: var(--t-band); line-height: var(--t-band-lh); color: var(--ink); margin: 0 0 var(--s-3); }
.home-reserved__body  { font-size: var(--t-body); line-height: var(--t-body-lh); color: var(--ink-2); margin: 0; }   /* 6,46:1 */
@media (max-width: 63.999rem) {
  .soglia__inner { grid-template-columns: 1fr; align-items: start; padding-block: var(--s-12) var(--s-8); }
  .soglia__arch { inline-size: 132px; block-size: 200px; }
}
@media (forced-colors: active) { .soglia__arch { color: CanvasText; } .soglia__step { background: CanvasText; forced-color-adjust: none; } }
```

**L'arco non si disegna.** L'hero traccia il suo arco in 900 ms; questo è già tracciato dal primo
frame. La porta si apre all'inizio della pagina; alla fine è semplicemente aperta. Si posano solo
i tre gradini (§5).

**Quando `reserved` non c'è** — che è la configurazione viva a :8770, dove il gate G3 è chiuso o
la bandiera `reserved_area_public_link` è spenta — la sezione non esiste e **non si disegna niente
al suo posto**: nessun segnaposto, nessun vuoto. La pagina si chiude sul glifo arco+gradini del
piè di pagina, che §8.7 prescrive comunque («Il glifo arco+gradini come chiusura») e che qui vive
a 56 × 40 px. I due stati sono entrambi finiti; nella configurazione aperta la chiusura è a due
scale, nella chiusa a una. Verificato su entrambi i server.

#### (b) Il piè di pagina — l'inventario vero

**Inventario misurato il 24 settembre**, lo stesso conteggio su entrambe le configurazioni vive:

```
N = 1 (contact@…)
  + 5 (legali: Mentions légales, Privacy Policy, Cookie Policy, Conditions d’utilisation, Avertissement)
  + 1 (Accueil)
  + len(footer_menu)                                  # righe CMS, LUNGHEZZA VARIABILE
  + (1 se gates.phase3_public E safe_url 'pages:antifraud' risolve)
```

| | `len(footer_menu)` | N calcolato | N misurato |
|---|---|---|---|
| **:8771** (Fase 3 aperta) | **8** — Personnes, Entreprises, Institutions, Universités & Formation, Forum Vénétie–Maroc, Actualités, Projet, Contact | 1+5+1+8+1 = **16** | **16** |
| **:8770** (Fase 3 chiusa) | **5** — Personnes, Entreprises, Forum Vénétie–Maroc, Projet, Contact | 1+5+1+5+0 = **12** | **12** |

Quindi la rivendicazione del round 1, «16 prima, 16 dopo», è sostituita da: **N → N, per ogni N**,
e i due N esistono davvero e sono diversi. Il layout non nomina nessun numero di voci: la lista è
`repeat(auto-fill, minmax(9rem, 1fr))`, che a 1 240 px dà 3 colonne, a 768 px ne dà 2 e a 390 px
ne dà 2 — con 5 righe CMS o con 18.

**Che cosa sopravvive, elencato perché il revisore ha chiesto gli attributi e non solo le parole:**

| elemento | esito |
|---|---|
| `<footer class="site-footer …" id="site-footer">` | conservato (`test_layout.py:50` cerca il prefisso; si aggiunge `congedo` **dopo** `site-footer`) |
| `.site-footer__version` | conservato verbatim (`test_layout.py:103`) |
| `.site-footer__antifraud` | conservato verbatim (`test_layout.py:119, :125`) |
| `{% if gates.phase3_public %}{% safe_url 'pages:antifraud' %}` | **ridichiarato tale e quale**, gate compreso |
| `{% blocktranslate %}«… est un écosystème d’information et d’orientation promu par …»` | conservato, nel gruppo «Le projet» |
| `{% brand_words %}` → «Italy Legal Entry™ — marque déposée» | conservato nell'identità (`test_layout.py:104-105`; `test_footer_trademark_words_per_language` copre IT/EN) |
| `{% brand_lockup "dark" %}` | conservato |
| `contact@agamieuromed.org` | conservato |
| `<nav aria-label="Informations légales">` e `<nav aria-label="Navigation du site">` | **entrambi conservati** |
| `<h2>Informations légales</h2>`, `<h2>Navigation</h2>`, `<h2>Le projet</h2>` | **tutti e tre conservati e visibili**, resi come testatine mono |
| il commento `CONTENT_PENDING_LEGAL_REVIEW` sull'Allegato 1 | conservato |
| © · anno · `site.version_label` · «contenus vérifiés le» + `<time datetime>` | conservati |
| quattro colonne (§8.7 le vieta per nome) | **sostituite da due righe**: identità; poi tre gruppi |
| `min-block-size: 24px` (`v2/shell.css:408`) | **superato da 44 px** |
| selettore di lingua nel piè di pagina | **non aggiunto**, deliberatamente — §4.7(c) |

```django
{% load i18n cms_nav %}{% footer_menu as footer_nav %}
<footer class="site-footer congedo on-inverse" id="site-footer">
  <div class="container">
    <div class="site-footer__inner congedo__identity">
      <div class="site-footer__col site-footer__col--identity">
        <p class="site-footer__brand">{% brand_lockup "dark" %}</p>
        <p class="site-footer__promoter">{{ site.promoter }}</p>
        {% comment %}
        CONTENT_PENDING_LEGAL_REVIEW — siège social, numéro RUNTS et code fiscal appartiennent aux
        « Mentions légales » officielles (Allegato 1, BLOCKED_BY_MISSING_OFFICIAL_SOURCE).
        {% endcomment %}
        {% brand_words as words %}{% if words %}<p class="site-footer__mark">{% brand "site-footer__wordmark-inline" %} — {{ words }}</p>{% endif %}
      </div>
      <p class="site-footer__contact"><a class="site-footer__email email" href="mailto:{{ site.contact_email }}">{% svg_icon "mail" "icon icon--sm" %}<span>{{ site.contact_email }}</span></a></p>
      <p class="congedo__close" aria-hidden="true">{% svg_icon "arch-steps" "icon congedo__glyph" %}</p>
    </div>

    <div class="congedo__grid">
      <nav class="site-footer__col site-footer__nav congedo__group congedo__group--legal" aria-label="{% translate 'Informations légales' %}">
        <h2 class="site-footer__heading">{% translate "Informations légales" %}</h2>
        <ul class="site-footer__list congedo__links">
          <li><a href="{% url 'legal:notices' %}">{% translate "Mentions légales" %}</a></li>
          <li><a href="{% url 'legal:privacy' %}">Privacy Policy</a></li>
          <li><a href="{% url 'legal:cookies' %}">Cookie Policy</a></li>
          <li><a href="{% url 'legal:terms' %}">{% translate "Conditions d’utilisation" %}</a></li>
          <li><a href="{% url 'legal:disclaimer' %}">{% translate "Avertissement" %}</a></li>
        </ul>
      </nav>
      <nav class="site-footer__col site-footer__nav congedo__group congedo__group--site" aria-label="{% translate 'Navigation du site' %}">
        <h2 class="site-footer__heading">{% translate "Navigation" %}</h2>
        <ul class="site-footer__list congedo__links">
          <li><a href="{% url 'pages:home' %}">{% translate "Accueil" %}</a></li>
          {% for item in footer_nav %}<li><a href="{{ item.url }}"{% if item.new_tab %} target="_blank" rel="noopener"{% endif %}>{{ item.label }}</a></li>{% endfor %}
        </ul>
      </nav>
      <section class="site-footer__col congedo__group congedo__group--project">
        <h2 class="site-footer__heading">{% translate "Le projet" %}</h2>
        <p class="congedo__sentence">{% blocktranslate with project=site.project_name promoter=site.promoter %}{{ project }} est un écosystème d’information et d’orientation promu par {{ promoter }}.{% endblocktranslate %}</p>
        {% if gates.phase3_public %}{% safe_url 'pages:antifraud' as antifraud_url %}{% if antifraud_url %}
        <a class="site-footer__antifraud" href="{{ antifraud_url }}">{% svg_icon "shield" "icon" %}<span>{% locked "p3.antifraud.title" %}</span></a>
        {% endif %}{% endif %}
      </section>
    </div>

    <div class="site-footer__bottom congedo__foot">
      <p>© {% now "Y" %} {{ site.promoter }}</p>
      <p class="site-footer__version">{{ site.version_label }}{% if site.content_verified_on %} — {% translate "contenus vérifiés le" %} <time datetime="{{ site.content_verified_on|date:'Y-m-d' }}">{{ site.content_verified_on|date:"d.m.Y" }}</time>{% endif %}</p>
    </div>
  </div>
</footer>
```

```css
/* static/css/v3/congedo.css (suite) */
.congedo { background: var(--mid-0); color: var(--on-dark); }           /* 16,37:1 */
/* v2/shell.css:408 impone `.site-footer a { min-block-size: 24px }` — la causa misurata di 1.10.
   Stessa specificità (0,1,1), più avanti nella cascata. */
.congedo a { min-block-size: 44px; }

.congedo__identity {
  display: grid; grid-template-columns: minmax(0, 32ch) 1fr auto;
  column-gap: var(--s-12); row-gap: var(--s-4); align-items: end;
  padding-block: var(--s-12) var(--s-8);
}
.congedo__identity .site-footer__brand { margin: 0 0 var(--s-3); }
.congedo__identity .site-footer__promoter { margin: 0; color: var(--on-dark-2); font-size: var(--t-ui); line-height: 20px; }  /* 10,22:1 */
.congedo__identity .site-footer__mark { margin: var(--s-1) 0 0; color: var(--on-dark-3); font-size: var(--t-caption); line-height: 16px; }  /* 6,79:1 */
.congedo__identity .site-footer__contact { margin: 0; }
.congedo .site-footer__email { display: inline-flex; align-items: center; gap: var(--s-2); padding-block: 12px; color: var(--on-dark); font-size: var(--t-ui); }
.congedo__close { margin: 0; display: flex; align-items: flex-end; }
.congedo__glyph { inline-size: 56px; block-size: 40px; color: var(--terr-line); }   /* 6,41:1 — grafica */

.congedo__grid {
  display: grid; grid-template-columns: repeat(12, minmax(0, 1fr));
  column-gap: var(--gutter); row-gap: var(--s-6);
  border-block-start: 1px solid var(--hairline-dark-strong);   /* DECORATIVO: 2,16:1 composito, §4.1 */
  padding-block: var(--s-8) var(--s-6);
}
.congedo__group--legal   { grid-column: span 4; }
.congedo__group--site    { grid-column: span 5; }
.congedo__group--project { grid-column: span 3; }
.congedo .site-footer__heading {
  margin: 0 0 var(--s-2); font-family: var(--f-mono); font-size: var(--t-folio); line-height: 16px;
  letter-spacing: var(--track-folio); text-transform: uppercase; font-weight: 400; color: var(--on-dark-3);   /* 6,79:1 */
}
.congedo__links {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
  column-gap: var(--gutter); row-gap: var(--s-1);       /* 4px: mai due bersagli a contatto */
  list-style: none; margin: 0; padding: 0;
}
.congedo__links a { display: flex; align-items: center; block-size: 44px; font-size: var(--t-ui); line-height: 20px; color: var(--on-dark-2); }
.congedo__links a:hover { color: var(--on-dark); text-decoration: underline; text-underline-offset: 3px; }
.congedo a:focus-visible { outline: 2px solid var(--accent-dark); outline-offset: 2px; }   /* 10,57:1 */
.congedo__sentence { margin: 0 0 var(--s-3); color: var(--on-dark-2); font-size: var(--t-ui); line-height: 24px; max-inline-size: 38ch; }
.congedo .site-footer__antifraud {
  display: inline-flex; align-items: center; gap: var(--s-2); block-size: 44px;
  padding-inline: var(--s-4); border: 1px solid var(--accent-dark); color: var(--accent-dark);   /* 10,57:1 */
  font-size: var(--t-ui); text-decoration: none;
}
.congedo__foot {
  display: flex; flex-wrap: wrap; gap: var(--s-1) var(--s-8);
  border-block-start: 1px solid var(--hairline-dark); padding-block: var(--s-4) var(--s-8);
  font-size: var(--t-caption); line-height: 16px; color: var(--on-dark-3); font-variant-numeric: tabular-nums;
}
.congedo__foot p { margin: 0; }

@media (max-width: 63.999rem) {
  .congedo__group--legal, .congedo__group--site { grid-column: span 6; }
  .congedo__group--project { grid-column: 1 / -1; }
}
@media (max-width: 47.999rem) {
  .congedo__identity { grid-template-columns: 1fr auto; padding-block: var(--s-8) var(--s-6); }
  .congedo__group--legal, .congedo__group--site, .congedo__group--project { grid-column: 1 / -1; }
  .congedo__grid { padding-block: var(--s-6); }
  .congedo__links { grid-template-columns: 1fr 1fr; column-gap: var(--s-4); }
  .congedo__sentence { max-inline-size: none; }
}
@media (forced-colors: active) { .congedo__glyph { color: CanvasText; } }
```

**Misurato** (il piè di pagina vero, ristrutturato e stilato nel browser sulle due configurazioni
vive; il round 1 dichiarava «≈ 560 px» senza misurare, ed era **falso**):

| viewport | oggi | congedo | Δ |
|---|---|---|---|
| :8771 1440×900 (16 link) | 629 px | **644 px** | +15 |
| :8771 768×1024 | 861 px | **904 px** | +43 |
| :8771 390×844 | **1 307 px** | **1 148 px** | **−159 (−12,2 %)** |
| :8770 1440×900 (12 link) | 533 px | **632 px** | +99 |
| :8770 768×1024 | 765 px | **764 px** | −1 |
| :8770 390×844 | 1 157 px | **1 008 px** | −149 (−12,9 %) |

| | oggi | congedo |
|---|---|---|
| altezza minima di un link | **24 px** (tutti e 16) | **44 px** (tutti e 16) |
| larghezza minima di un link | 37,6 px | **151,5 px** a 1440, 167 px a 390 |
| colonne | 4 fisse (348/249/249/298) | 2 righe; le liste a `auto-fill` (3 colonne a 1440, 2 a 768 e a 390) |
| quota della pagina a 390 | **11,69 %** di 11 183 px | **10,41 %** di 11 024 px |

**Onestà sul desktop**: il congedo **cresce** di 15 px a 1440 su :8771 e di 99 px su :8770. Non è
un difetto mascherato, è il prezzo dichiarato: 15 link passano da un bersaglio di 24 px a uno di
44 px, cioè +20 px per riga, e la compressione da quattro colonne a tre gruppi restituisce quasi
tutto quel costo su :8771 ma non su :8770, dove le liste hanno meno righe da impilare. Se il
Council preferisce i 533 px di :8770 ai 44 px di bersaglio, è una scelta esplicita e la dico qui
invece di nasconderla in una stima.

#### (c) Le lingue nel piè di pagina — **non si aggiungono**

§8.7 nomina «navigazione + legale + lingue» e il round 1 aveva messo una riga «FR IT EN ع» senza
markup, senza `hreflang` e con un glifo arabo singolo senza nome accessibile. È cancellata, e non
sostituita. Ragioni, in ordine: il commutatore esiste già
(`templates/components/language_switcher.html`, un `<details>` nativo con `lang`, `hreflang`,
`dir` e `aria-current` su ogni voce, funzionante senza JS); duplicarlo aggiungerebbe quattro
destinazioni al conteggio N e due controlli per la stessa cosa nella stessa pagina; e un secondo
commutatore che non fosse quel componente sarebbe una terza grammatica di lingua. **Quello che
resta da verificare, e che dichiaro come dipendenza**: sotto 768 px la barra istituzionale entra
nel drawer (§4 di DESIGN_SYSTEM_V2), quindi il commutatore è raggiungibile solo aprendo il menu.
Se la spec `navbar` decide che non basta, il posto giusto è il drawer, non il piede.

### 4.8 Il banner istituzionale, l'orientamento, la fiducia, lo stato vuoto

Il revisore ha notato che `banner` non compariva **da nessuna parte** nel round 1 pur essendo
vivo a :8770. Ecco le quattro sezioni che il round 1 aveva lasciato senza trattamento.

**`banner`** (`_banner.html` → `forum/partials/home_banner.html`, testi prescritti
`p2.home.banner.*`, gate `forum_banner`). Sta subito sotto l'hero e **non prende `.shead`**: è un
avviso di utilità, non un capitolo. Trattamento: lo stesso apparato della minuta **un rango più
in basso** — nessun bronzo (il bronzo è per l'atto unico della pagina), filetto alto di 1 px
`--hairline-strong` (3,14:1 su `--min-1`), fondo `--min-1` come oggi, nessun raggio.

```css
.home-banner { border-block-start: 1px solid var(--hairline-strong); background: var(--min-1); }
.home-banner__dismiss { position: absolute; inset-block-start: var(--s-2); inset-inline-end: var(--s-2);
  inline-size: 44px; block-size: 44px; display: inline-flex; align-items: center; justify-content: center; }  /* era sotto i 44 */
.home-banner__dismiss:focus-visible { outline: 2px solid var(--accent-ring); outline-offset: 2px; }
```

Il contenuto del partial del Forum (titolo, meta, citazione, bottone prescritti) **appartiene alla
spec `company-forum-academy`**: questa spec stila il contenitore e il controllo di chiusura, e
non tocca una parola.

**`orientation`.** La frase prescritta `p3.persons.how_it_works` prende il margine, come ogni
testo che porta un obbligo:

```css
.home-orientation__how {
  padding-inline-start: var(--s-6);
  border-inline-start: 2px solid var(--hairline-strong);   /* 3,14:1 su --min-1 */
  font-size: var(--t-body); line-height: var(--t-body-lh); max-inline-size: 62ch; color: var(--ink);
}
```

**`trust`.** Due layout dipendenti dal gate, **entrambi specificati** (il round 1 non ne
specificava nessuno):

```css
.home-trust__grid { display: grid; grid-template-columns: repeat(12, minmax(0,1fr)); column-gap: var(--gutter); row-gap: var(--s-8); }
/* G3 aperto: quattro FAQ prescritte citate verbatim */
[data-trust="faq"] .home-trust__item { grid-column: span 6; padding-inline-start: var(--s-6); border-inline-start: 2px solid var(--hairline-strong); }
[data-trust="faq"] .home-trust__question { font-family: var(--f-serif); font-weight: 400; font-size: var(--t-entry); line-height: var(--t-entry-lh); margin: 0 0 var(--s-2); }
[data-trust="faq"] .home-trust__answer { font-size: var(--t-body); line-height: var(--t-body-lh); color: var(--ink-2); max-inline-size: 58ch; margin: 0; }
/* G3 chiuso: ciò che la piattaforma fa / non fa. Forma + parola, MAI il colore da solo. */
[data-trust="interim"] .home-trust__column { grid-column: span 6; }
[data-trust="interim"] .home-trust__column-title { font-family: var(--f-mono); font-size: var(--t-folio); letter-spacing: var(--track-folio); text-transform: uppercase; font-weight: 400; color: var(--ink-3); }
[data-trust="interim"] .home-trust__list { list-style: none; margin: 0; padding: 0; }
[data-trust="interim"] .home-trust__statement { padding-inline-start: var(--s-6); border-inline-start: 2px solid var(--accent); padding-block: var(--s-3); font-size: var(--t-body); line-height: var(--t-body-lh); max-inline-size: 58ch; }
[data-trust="interim"] .home-trust__list--not .home-trust__statement { border-inline-start-style: dashed; border-inline-start-color: var(--ink-3); }  /* 5,53:1, e la DIFFERENZA è il tratteggio */
@media (max-width: 63.999rem) { .home-trust__item, .home-trust__column { grid-column: 1 / -1; } }
```

Il verde semantico **non** entra qui: «ciò che la piattaforma fa» non è uno stato regolare o
terminato, è una dichiarazione. La differenza fra le due colonne è portata dal **titolo in
parole** (che esiste già nel template), dal tratto pieno contro il tratteggio e dalla posizione.
Mai dal colore da solo. La barra di giurisdizione resta dov'è e come sta: è di
`components/jurisdiction.html` e della spec che possiede §9.3, e questa spec non la ridisegna —
si limita a osservare, misurato, che è alta 20 px su una sezione di 1 002 px e che chi la possiede
dovrebbe saperlo.

**Lo stato vuoto.** `components/empty_state.html` **non cambia di un byte**: `role="status"`,
il ramo `{% if action_url %}`, il parametro `icon` restano. Gli altri 20 chiamanti (portal,
forum, community, glossary, news, partners, pathways, deadlines, messages, requests, academy,
helpdesk…) non vedono nulla. `_news.html` avvolge l'include:

```django
{% else %}
  {% translate "Aucune actualité publiée pour le moment." as empty_title %}
  {% translate "Les informations du projet seront publiées ici." as empty_text %}
  <div class="home-news__empty">{% include "components/empty_state.html" with title=empty_title text=empty_text icon="document" %}</div>
{% endif %}
```

```css
/* Discendente scoped: NIENTE fuori da .home-news__empty è toccato. */
.home-news__empty .empty-state {
  border: 0; border-block-start: 2px solid var(--hairline-strong); border-radius: 0;
  text-align: start; display: grid; grid-template-columns: 24px minmax(0, 1fr);
  column-gap: var(--s-4); row-gap: var(--s-2); padding: var(--s-6) 0 0; max-inline-size: 58ch;
}
.home-news__empty .empty-state__icon { grid-column: 1; grid-row: 1; inline-size: 24px; block-size: 24px; color: var(--ink-3); }
.home-news__empty .empty-state__title { grid-column: 2; margin: 0; font-family: var(--f-serif); font-weight: 400; font-size: var(--t-entry); line-height: var(--t-entry-lh); }
.home-news__empty .empty-state__text  { grid-column: 2; margin: 0; color: var(--ink-2); font-size: var(--t-body); line-height: var(--t-body-lh); }
```

Il rettangolo tratteggiato da 672 × 218 px fuori asse diventa una riga di registro allineata alla
colonna, sotto lo stesso molo del resto della superficie. **Il glifo arco+gradini che §9.6
prescrive per gli stati vuoti richiede un simbolo nuovo in `icons.svg` e riguarda 21 template:
non è di questa spec.** È consegnato a chi possiede §9.6, e questa spec usa l'icona che il
componente riceve già.

### 4.9 Le immagini — la decisione che il committente deve prendere

Il round 1 scriveva **«Immagini: zero nuove»** e marcava l'unico slot `BLOCKED_BY_MISSING_ASSET`.
Il revisore ha ragione su tutta la linea: è la scusa vietata riscritta come virtù. È ritirata.
Ecco i fatti, verificati nel repository e in pagina.

**(1) Le fotografie ci sono.** `static/img/photos/` contiene **15 slug** in 4 larghezze (480, 960,
1440, 1920) più un JPEG di ripiego, **73 file**, tutti self-hosted, con `manifest.json` che porta
licenza, sorgente, SHA-256 dell'originale e `usage_slot`. **Quattro di quegli slot sono
esattamente i quattro accessi di questa superficie**: `entrance_person`
(`entretien-accompagnement`), `entrance_company` (`equipe-entreprise`), `entrance_institution`
(`dialogue-institutionnel`), `entrance_university` (`etudiants-bibliotheque`). Più
`orientation` (`orientation-ecran`), `news_default` (`micro-conference`), `reserved_area`
(`espace-de-travail`).

**(2) Non escono, e la causa non è questa superficie.** `apps/cms/models.py:309`:
`is_publishable` richiede `caption_fr AND credit AND caption_place AND caption_date`;
`pages/services.py:213` restituisce `None` per un asset che non li ha, quindi lo slot non
raggiunge nessun template. La spec `imagery` §1.4 misura il risultato: `MediaAsset.objects.count()
== 15`, `publishable == 0`, perché `apps/cms/seeds_media.py:182` crea gli asset con
`is_decorative=False` e **non scrive nessuno dei quattro campi**. Il cancello anti-stock funziona
perfettamente: ha chiuso la porta su tutto.

**(3) E anche se qualcuno scrivesse le didascalie, non basterebbe.** `manifest.json` porta
`"author": "Unsplash contributor (author lookup unavailable offline)"` su **ogni** voce: il campo
`credit` non è compilabile in modo veritiero da ciò che il repository contiene. Sono **due
blocchi diversi** e non vanno confusi: uno è lavoro editoriale di mezza giornata, l'altro
richiede una connessione e una verifica di attribuzione.

**(4) E se anche si risolvessero entrambi, il soggetto resterebbe sbagliato.** I `subject` del
manifest, parola per parola: «Deux collègues se félicitent dans un bureau», «Trois collègues
échangent autour d'une table de travail», «Personne qui remplit des documents à la main». Il
committente dice che mancano immagini **eleganti, moderne e coerenti**. Rispondere a una critica
di gusto con la libreria che quella stessa critica respingerebbe non è una risposta: è un
riempimento. Nessun direttore artistico firmerebbe quattro congratulazioni da stock sulle quattro
porte dell'ecosistema.

**(5) Quindi: il disegno c'è, l'asset è una decisione del committente.** Ecco lo slot,
completamente specificato, e il brief.

```django
{# components/entrances.html, dentro <a class="entry">, prima di entry__ordinal #}
{% if e.photo %}
<figure class="entry__plate">
  {% include "pages/partials/_picture.html" with photo=e.photo sizes="(min-width: 64rem) 42vw, 100vw" %}
  <figcaption class="entry__plate-caption">{{ e.photo.place }} · {{ e.photo.date|date:"Y" }} · {{ e.photo.credit }}</figcaption>
</figure>
{% endif %}
```

```css
.register--entrances .entry:has(.entry__plate) {
  grid-template-areas: "plate plate" "glyph title" "glyph gloss" "cta cta";
  grid-template-rows: auto auto 1fr auto;
  padding-block-start: 0;
}
.entry__plate { grid-area: plate; margin: 0 calc(var(--s-6) * -1) var(--s-6) calc(var(--s-8) * -1); }
.entry__plate img { display: block; inline-size: 100%; block-size: auto; aspect-ratio: 3 / 1; object-fit: cover; }
.entry__plate-caption {
  padding: var(--s-2) var(--s-6) 0 var(--s-8);
  font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  font-variant-numeric: tabular-nums; color: var(--ink-3);       /* 5,53:1 */
}
```

La didascalia **non è una tassa, è il disegno**: la lastra porta luogo · anno · autore in mono
sotto il taglio, come una tavola d'archivio. È ciò che rende evidente che riempire i quattro
campi non è burocrazia — è la metà visibile dell'oggetto. *Ripiego di `:has()`*: se un motore non
lo supporta, la regola non si applica, `.entry__plate` cade in una riga implicita sopra il glifo
e il pannello resta leggibile — degrada, non si rompe. Nessun JavaScript è coinvolto.

**Brief fotografico — quattro fotogrammi, uno per accesso.**

- *Soggetto*: **l'atto del percorso, non la persona come simbolo.* Una mano che annota un
  fascicolo; un'aula di formazione vista dal fondo nel momento di una domanda; un corridoio
  universitario con una bacheca; un tavolo di riunione con la pratica in due lingue sopra.
- *Vietato*: aeroporti, passaporti, valigie, varchi, bandiere, tricolore, insegne di Stato
  (ANTI_PATTERNS §5.9); cronaca migratoria (§2); strette di mano, congratulazioni, sorrisi da
  stock, avatar generati, loghi finti (§1).
- *Luce*: naturale, una sorgente, niente flash, niente HDR; i neri devono restare **sopra**
  `--mid-1` perché la lastra possa portare un velo senza chiudersi.
- *Colore*: desaturazione ≈ 0,85, ombra calda, così che le quattro lastre leggano come **una sola
  campagna** contro la carta `--min-2`.
- *Inquadratura*: **3:1 orizzontale**, soggetto nel terzo esterno, i due terzi interni abbastanza
  quieti da reggere l'ormeggio e il titolo.
- *Consegna*: originali a 2 400 px; derivati **AVIF q50 + WebP q78** a 480/960/1440; e per ogni
  fotogramma `caption_place`, `caption_date`, una frase di fatto in `caption_fr` e un
  **`credit` con un nome**.
- *Byte*: ≤ **32 KB per lastra a 1440** in AVIF, quindi ≤ 64 KB per viewport (al massimo due
  lastre in vista in una sezione alta 1 010 px) — dentro i 120 KB per viewport. `loading="lazy"`,
  `decoding="async"`. L'AVIF **non esiste ancora** nella pipeline (`imagery` §1.6) ed è una
  consegna di quella spec, non di questa.

**Che cosa si guadagna, misurato.** Superficie fotografica della home oggi: **0,94 %** a 1440
(`imagery` §1.2: la lastra della porta, 401 × 267 px su 1440 × 7 921). Con le quattro lastre 3:1
nel molo: 713×238 + 503×168 + 503×168 + 713×238 = **508 396 px²**, più i 107 067 px² dell'hero,
su 1440 × 7 388 = 10 638 720 px² → **5,79 %**. Sei volte la superficie di oggi, con quattro
immagini e sotto il budget di byte.

**Che cosa si perde senza.** Niente si rompe: `photo_for_slot` restituisce `None`, `{% if e.photo %}`
non rende nulla, la griglia perde l'area `plate` e il pannello resta quello misurato in §4.3.
Al suo posto c'è il glifo del rilievo — **un disegno d'autore, generato con seme fisso, non un
segnaposto**. Ma è meno di quello che il committente ha chiesto, e lo scrivo qui invece di
chiamarlo «completo senza».

> **AL COUNCIL E AL COMMITTENTE.** Questa superficie, con il molo, la testata, la minuta, il
> registro e la soglia, consegna **la misura**. Non consegna **lo spettacolo fotografico** che il
> committente ha chiesto, e non può consegnarlo con la libreria che c'è: quindici fotografie da
> stock, senza didascalia, senza credito verificabile, con soggetti che la stessa critica
> respingerebbe. Le vie d'uscita sono due e costano entrambe: **(A)** commissionare i quattro
> fotogrammi del brief qui sopra — una giornata di ripresa o una commissione su licenza, più la
> pipeline AVIF della spec `imagery`; **(B)** risolvere online l'attribuzione Unsplash, curare
> quindici didascalie e accettare i soggetti che ci sono. **La decisione è del committente**, non
> del disegno, e questa spec non la assorbe in silenzio. Finché non è presa, le quattro lastre
> non si rendono e la superficie resta quella misurata in §4.3.

### 4.10 File e template toccati

**Nuovi** — quattro fogli di stile, **nessun file JavaScript**, **nessun token nuovo**, **nessun
simbolo nuovo in `icons.svg` tranne uno**:

| file | contenuto |
|---|---|
| `static/css/v3/sections.css` | `.shead`, la correzione di 1.2/1.4/1.11, `.pathway-list`, `.home-news__*`, `.home-ecosystem__*`, `.home-trust__*`, `.home-orientation__how` |
| `static/css/v3/panels.css` | il molo (`.register--entrances`, `.entry`, l'ormeggio) e la lastra fotografica |
| `static/css/v3/notice.css` | la minuta (`.avviso*`) e `.home-banner` |
| `static/css/v3/congedo.css` | la soglia (`.soglia*`) e il piè di pagina (`.congedo*`) |

Il simbolo nuovo è **`icon-arch-steps`** in `static/img/icons.svg` (arco + tre gradini, tratto
1,5, da 36 a 37 simboli, ≈ 0,3 KB): lo chiede `DESIGN_SYSTEM_V2` §8.7 per la chiusura del piè di
pagina e oggi non esiste. `icon-seal` del round 1 è ritirato: si usa `icon-shield`, che esiste ed
è asserito dai test.

**`static/css/main.css`** — quattro `@import` dopo `v3/buttons.css`.
**`templates/base.html`** — **e le quattro `<link rel="preload" as="style">` corrispondenti**,
che il round 1 aveva dimenticato (lacuna 13). `base.html` mantiene una riga di preload per ogni
livello proprio per togliere la catena di richieste che allunga l'LCP; aggiungere un `@import`
senza il suo preload significa reintrodurre un salto di catena per ciascuno:

```django
<link rel="preload" href="{% static 'css/v3/sections.css' %}" as="style">
<link rel="preload" href="{% static 'css/v3/panels.css' %}" as="style">
<link rel="preload" href="{% static 'css/v3/notice.css' %}" as="style">
<link rel="preload" href="{% static 'css/v3/congedo.css' %}" as="style">
```

Nessun'altra modifica a `base.html`: `<main id="main-content">` e `{% block site_footer %}`
restano come sono (§4.7).

**Template modificati** — otto, tutti solo contenitori, classi e rami già esistenti:

| file | modifica |
|---|---|
| `pages/partials/_section_header.html` | `shead` + `data-rank` facoltativo, l'ordinale resta nel DOM, il filetto, **tutti i rami ripristinati** |
| `pages/home/_entrances.html` | una parola: `rank="open"` nell'include |
| `pages/home/_news.html` | `flat=True` sull'include della scheda; il link d'indice risale; `<div class="home-news__empty">` |
| `pages/home/_ecosystem.html` | classi di contenitore; **entrambi i rami del gate conservati** |
| `pages/home/_antifraud.html` | `.avviso__sheet` > `.container.avviso__inner`; `#icon-shield` conservato; tutti i rami conservati |
| `pages/home/_reserved.html` | la soglia; `section--rule`; `btn--primary` |
| `pages/home/_banner.html` | una classe sul controllo di chiusura |
| `partials/footer.html` | due righe invece di quattro colonne; **ogni classe, ogni landmark, ogni `<h2>`, ogni gate conservati** |
| `components/pathway_list.html` | `{% if item.meta %}` facoltativo |
| `components/entrances.html` | **nulla oggi**; il blocco `{% if e.photo %}` solo se §4.9 è approvata |

**Modifica trasversale, dichiarata.** `.section__header { max-inline-size: none }` (§4.2) tocca
**tutti** i chiamanti del selettore, non solo la home: `templates/components/section_header.html`
è incluso 9 volte (`ecosystem/{companies,institutions,pilot,universities}.html`,
`pathways/{index,index_interim,detail,diplomas}.html`, `dev/showcase.html`) e
`pages/partials/_section_header.html` 6 volte. La lacuna 10 del revisore è questa: lasciare la
colonna da 420,75 px viva su quelle pagine significa lasciare due grammatiche di intestazione.
La correzione minima — togliere il tetto e dare la misura al titolo e al lead separatamente — si
applica a tutte e quindici; **la composizione a due fuochi no**, perché
`components/section_header.html` non ha né folio né `date` e riscriverne il contratto è lavoro
delle spec `company-forum-academy` e `person-dashboard`. Guardia: schermate a 1440 e 390 delle
otto pagine pubbliche coinvolte, prima e dopo (§8, rischio 6).

**Nessuna vista, nessun `services.py`, nessun `models.py`, nessuna migrazione, nessun testo
bloccato, nessuna stringa nuova visibile all'utente.** Il round 1 introduceva nomi di movimento e
testate di riga in francese senza chiave di traduzione (lacuna 11): non esistono più, perché non
esistono più i movimenti. Tutte le stringhe visibili di questa spec sono già nel repository e già
tradotte.

---

## 5. MOTO — voci per `MOTION_SYSTEM.md` §6

**Questa superficie spedisce una sola animazione, ed è CSS puro.** Zero byte di JavaScript nuovo.
`static/js/src/sections.js` del round 1 è cancellato.

| Nome | Funzione | Innesco | Durata | Curva | Proprietà | Stato ridotto | Prestazioni |
|---|---|---|---|---|---|---|---|
| `mooring.draw` | **FEEDBACK** | `:hover` in `@media (hover: hover)` · `:focus-visible` · `:focus-within` sulla riga | `--motion-fast` **180 ms** | `--ease-out` | `transform: scaleY(.38 → 1)` sullo pseudo-elemento `.entry::before`, origine `top` | **identico**: l'hover non è moto essenziale; lo stato finale è lo stesso, senza transizione | 4 pseudo-elementi di 3 px, compositor puro, nessun layout, nessun `will-change` |

Il blocco `transition` vive dentro `@media (prefers-reduced-motion: no-preference)`; la
dichiarazione di stato (`:hover → scaleY(1)`) vive **fuori**, perché con moto ridotto l'ormeggio
deve comunque scendere a fondo, solo senza interpolazione. È la lettura letterale di
`MOTION_SYSTEM` §3: fuori dal blocco, il valore è quello finale.

*Nota sui token, verificata in pagina*: `--motion-fast` è dichiarato **due volte** —
`tokens.css:173` a 120 ms (famiglia legacy) e `v2/tokens.css:108` a **180 ms** (la famiglia
normativa); `--ease-out` anche — `tokens.css:176` `cubic-bezier(0.2,0,0,1)` e `v2/tokens.css:104`
`cubic-bezier(.25,1,.5,1)`. In entrambi i casi vince V2 perché arriva dopo nell'ordine di
`@import` di `main.css`, quindi i valori usati qui sono **180 ms** e la curva normativa. È la
stessa collisione di famiglie che produce il difetto 1.2, e qui cade dalla parte giusta: va
sanata dalla spec che possiede la demolizione di `tokens.css`, non da questa.

### 5.1 I gradini della soglia — perché non li animo

`soglia-steps` del round 1 (DELIZIA, 320 ms, `stagger(0.1, {from:"last"})`) richiedeva
`inView` + `stagger`, quindi un file JavaScript nuovo per tre `<span>`. I tre gradini restano a
`scaleX(.7)` **ferma**, come composizione: l'hero traccia l'arco e posa i gradini in 900 ms
all'ingresso; alla fine della pagina la porta è semplicemente aperta. Una pagina che disegna la
stessa porta due volte non ha una firma, ha un tic. Se il Council la vuole animata, la chiave è
la spec `scroll` (ruolo `reveal.tile`), non un secondo bundle.

### 5.2 I reveal — questa spec li **dichiara**, non li scrive

`MOTION_SYSTEM` §0 vieta per nome il `fade-in-up` generico su tutto ciò che entra in viewport, e
`shell.js` ne implementa già uno (320 ms, `translateY(-10px) scale(1.012)`, stagger 60 ms). Il
round 1 ne scriveva un **secondo**, a 240 ms / 12 px / 60 ms — cioè lo stesso identico gesto con
altri due numeri, tre volte per ogni intestazione. Il revisore ha ragione: era l'anti-pattern a
scala ridotta.

La spec `scroll` §4.3 ha già la risposta giusta — quattro ruoli dichiarati
(`plate` / `register` / `tile` / `figure`) invece di una funzione sola, con l'escursione
**positiva** e senza `scale()` sul testo. Questa superficie **non scrive un reveal**: dichiara
quale ruolo prende ogni suo oggetto, come attributo nel markup, e nient'altro.

| oggetto | `data-reveal` | perché |
|---|---|---|
| `.shead` di ogni sezione | `plate` | il filetto si traccia, poi testatina / titolo / lead: è la sola sequenza in cui l'ordine di arrivo **è** la gerarchia |
| i quattro `.register__item` del molo | `tile` | al massimo quattro per riga, l'ormeggio guida |
| le righe di `.pathway-list` | `register` | scaglionamento 40 ms, massimo 8, poi 0 |
| `.avviso__sheet` | **nessuno** | un avviso che arriva in ritardo è un avviso meno visibile. La minuta è completa e ferma dal primo frame. |
| `.soglia` | **nessuno** | §5.1 |

Se la spec `scroll` non fosse adottata, questa superficie resta **esattamente com'è misurata in
§4**, con una sola animazione. Nessuna dipendenza dura.

### 5.3 Quel che questa superficie **non** aggiunge, e perché va detto

`MOTION_SYSTEM` §4 ammette su una pagina IMMERSIVE **un** loop ambientale e **un** oggetto
indicizzato allo scroll. La home ne ha **due** indicizzati allo scroll, verificati nel sorgente:
`static/js/src/home.js:95` lega la fotografia della porta a `scroll()` con `offset: ["start
start", "end start"]`, e `:116` lega `.voyage__line` a `scroll()` sulla sezione del pilota.
**La pagina è già un oggetto sopra il budget.** Questa superficie non aggiunge il terzo — il rail
del round 1 lo avrebbe fatto — e lo segnala ai proprietari delle spec `hero-doorway` e `scroll`,
che è dove la decisione va presa.

---

## 6. ACCESSIBILITÀ, RTL, FORCED-COLORS, MOTO RIDOTTO

**1.4.11 (non-text contrast).** Ogni confine che porta informazione su questa superficie è ≥ 3:1,
calcolato: molo 2 px `--hairline-strong` **3,37:1** su `--min-0` e **3,59:1** su `--min-2`;
ormeggio 3 px `--route-n` **5,96 / 6,05 / 6,76 / 8,05:1** su `--min-2`; filetto della testata
3,37:1; molo del registro e delle attualità 3,37:1; filetto della minuta `--seal-600` **3,86:1**
sul proprio fondo; bordo del bottone SECONDARY **3,03:1**; anello di focus `--accent-ring`
**3,70:1** su `--min-0`, **3,94:1** su `--min-2`, **3,33:1** su `--seal-100`, `--accent-dark`
**10,57:1** su `--mid-0`. I due soli filetti sotto il 3:1 sono **dichiarati decorativi** e lo
sono per costruzione: `--hairline` fra due righe di registro (1,37:1 — il confine è già portato
da ordinale, titolo serif e 88 px di altezza) e `--hairline-dark-strong` composito nel congedo
(**#434E54, 2,16:1** — separa due blocchi che hanno già intestazioni proprie e 32 px di spazio).

**1.4.3 (contrasto del testo).** Tutti i valori in §4.1. Il minimo su testo è `--ink-3` su
`--seal-100` a **4,97:1** e `--ink-3` su `--min-0` a **5,53:1**; nessun testo scende sotto 4,5.

**2.5.8 (target size).** Link del congedo **44 px** misurati, tutti e 16, con `row-gap: 4px`
fra righe adiacenti; `.entry__cta` 44 px; il pannello intero è il bersaglio del molo
(713 × 320 px a 1440, 350 × 348 px a 390); le righe di registro 133–161 px; il controllo di
chiusura del banner 44 × 44; il bottone della soglia 48 px. L'accusa 2.5.8 del round 1 sui
percorsi è **ritirata**: era già conforme (§1.11).

**Apparenza del focus.** Il difetto vero: l'anello era disegnato sul box in linea di 13 px.
`.pathway-list__item:focus-within { outline: 2px solid var(--accent-ring); outline-offset: 2px }`
con `a:focus-visible { outline: none }` sposta l'indicatore sulla riga — **misurato: da 13 px a
133 px** a 1440 e a **161 px** a 390. Stesso schema sul molo (`.entry:focus-visible`).

**1.4.12 (spaziatura del testo).** La misura del corpo della minuta scende da **91,4** a
**71,1 caratteri per riga** (contati su 640 caratteri con `Range.getClientRects()`), sotto il 75
di §3.2. Nessun `max-inline-size` di questa spec supera i 64ch ≈ 73 caratteri.

**2.4.6 / struttura.** La gerarchia delle intestazioni non cambia. Misurata oggi su
`:8771/fr/`: **9 `h2` e 17 `h3` dentro `main`**, più **3 `h2`** nel piè di pagina. Il markup di §4
non aggiunge né toglie una sola intestazione — cambia solo dove stanno i contenitori — e il diff
di §8 rischio 7 verifica i tre conteggi. Nessuna intestazione fantasma,
nessun `aria-hidden` su un'intestazione, nessun `role` nuovo. `aria-labelledby` continua a
puntare al `title_id`, e il ramo `visually-hidden` che lo tiene vivo a titolo vuoto è
ripristinato.

**3.1.2 (lingua di parte).** Ogni `{% if X.lang %} lang="{{ X.lang }}"{% endif %}` dei testi
prescritti è ripristinato in tutti i markup di §4: `heading.lang`, `intro.lang`, `s.note.lang`,
`d.title.lang`, `d.body.lang`, `d.button.lang`, `d.promoter_quote.lang`, `quote.lang`,
`statement.lang`, `item.lang`, `article.lang`, `e.lang`.

**RTL.** Solo proprietà logiche: `inset-inline-start`, `padding-inline`, `border-inline-start`,
`border-block`, `grid-column` per numero, `margin-inline`. Si specchia solo ciò che ha una
direzione di lettura — l'ormeggio (`inset-inline-start`, che si specchia da sé), la freccia
(`icon--flip-rtl`, già esistente), il filetto della testata (è `flex: 1`, si adatta), il margine
dei testi prescritti. **Non** si specchiano: il lock-up, il titolo bloccato, i numerali tabellari,
il glifo dello scudo, l'arco della soglia (`transform-origin: center` sui gradini, non `left`).
Verificato sul vivo su `/ar/` con il CSS applicato: `dir="rtl"`, `.shead__folio` con
`letter-spacing: normal` e `text-transform: none`, titolo d'apertura a 48 px con tracking 0.

**`forced-colors: active`.** Ogni confine che porta informazione è un `border` o un
`background-color` su un elemento vero, mai un gradiente, quindi sopravvive: il molo e il filetto
della minuta restano, l'ormeggio prende `CanvasText` con `forced-color-adjust: none` (è
l'identificazione del componente e deve restare), il pannello guadagna
`border: 1px solid CanvasText` perché il suo fondo `--min-2` sparisce, la fascia della minuta
passa a `Canvas` con due bordi `CanvasText` di peso diverso, l'arco e il glifo di chiusura
passano a `currentColor` = `CanvasText`.

**`prefers-reduced-motion` è uno stato completo.** L'unica animazione della superficie è
`mooring.draw`, e il suo stato ridotto è **identico** (stesso valore finale, senza transizione).
Nessun elemento di questa spec parte da `opacity: 0`, nessun tratto resta non disegnato, nessun
gradino resta a metà, niente è nascosto in attesa di JavaScript. Se JavaScript non si carica
affatto, la superficie è completa: **non c'è JavaScript di questa superficie**.

**HUMAN_QA_REQUIRED.**
1. La lettura della minuta da parte di un revisore giuridico: deve leggere «atto», non
   «promozione». È giudizio, non misura.
2. La resa di `--seal-100` su e-ink e su gamma stretta (il ΔE2000 di 5,40 è calcolato in sRGB).
3. NVDA e VoiceOver sull'ordine di lettura del congedo e della soglia, che sono due elementi
   vicini e non fusi: si deve sentire il passaggio da `main` a `contentinfo`.
4. `tests/i18n/test_rtl_browser.py` da estendere alle nuove firme (`.shead__rule`, `.avviso`,
   `.soglia`, `.congedo`).
5. **La decisione fotografica di §4.9**, che non è una QA ma una scelta del committente.

---

## 7. PRESTAZIONI

**Byte CSS — misurati, non stimati.** Estratti dal documento tutti i blocchi ```css di §4 e
compressi: **25 935 byte grezzi**, **6 222 byte con `gzip -9`** = **6,08 KB gzip** per i quattro
file insieme (il round 1 dichiarava «≈ 3,4 KB gzip» su cinque file, senza comprimere niente).
Ripartizione approssimativa fino alla consegna dei file veri: `sections.css` ≈ 8 KB grezzi,
`panels.css` ≈ 5, `notice.css` ≈ 4, `congedo.css` ≈ 8. In compenso questa spec **sostituisce** i
blocchi `folio`, `register`, `section__header` e `site-footer` di `register.css` (28 837 B grezzi,
7 701 gzip) e `components.css` (77 736 B grezzi, 12 867 gzip): il bilancio netto atteso è vicino a
zero, e la verifica è il `gzip -9` di quei due file prima e dopo.

**Byte JavaScript: zero.** Misurato, il bundle attuale della home in gzip:
`dist/chunks/chunk-P4EHGXV4.js` **26 120 B** + `js/main.js` **5 293** + `dist/home.js` **896** +
`dist/shell.js` **613** + `js/motion.js` **189** + `js/head.js` **206** = **33 317 B = 32,5 KB
gzip**, contro il tetto di 45 KB. Questa superficie **non aggiunge un byte**: nessun file nuovo,
nessun import nuovo, il chunk Motion condiviso non cresce.

**Immagini.** Oggi la superficie non ne carica nessuna. Con §4.9 approvata: quattro AVIF
≤ 32 KB a 1440, al massimo due in un viewport di 900 px dentro una sezione alta 1 010 px →
**≤ 64 KB per viewport**, dentro i 120 KB. `loading="lazy"`, `decoding="async"`, `srcset`
480/960/1440 con `sizes="(min-width: 64rem) 42vw, 100vw"`, nessun `fetchpriority` (la lastra non
è mai l'LCP: l'LCP è nell'hero).

**Catena di richieste.** Quattro `@import` in `main.css` **e** quattro `<link rel="preload"
as="style">` in `base.html` (§4.10). Senza il preload ogni `@import` costa un salto di catena sul
percorso critico del render; `base.html` mantiene una riga per ogni livello proprio per questo, e
il round 1 aveva aggiunto cinque import e zero preload.

**Paint e layout.** Si anima **una sola proprietà su tutta la superficie**: `transform` su quattro
pseudo-elementi di 3 px. Zero `filter`, zero `box-shadow` animato, zero `box-shadow` di qualunque
tipo (censimento sul DOM vivo con il CSS applicato: gli unici elementi con `box-shadow` dentro
`main` restano i tre dell'hero), zero proprietà fisiche, zero listener di scroll, zero
`IntersectionObserver` aggiunti.

**Altezza della pagina, misurata con il CSS applicato alla pagina viva:**

| | oggi | con questa spec | Δ |
|---|---|---|---|
| 1440×900 (:8771) | 7 921 px | **7 388 px** | **−533 (−6,7 %)** |
| 390×844 (:8771) | 11 183 px | **11 604 px** | **+421 (+3,8 %)** |

Il desktop si accorcia perché la testata smette di impilare titolo e lead e la minuta si
comprime. Il mobile si allunga, e dico da dove viene: i quattro pannelli del molo passano da
258–294 px a 348–432 px, perché la glossa sale da `--t-small` a `--t-body` 17/28 e la CTA prende
un bersaglio da 44 px. È **+421 px in cambio di quattro bersagli conformi e di un corpo
leggibile**; se il Council preferisce i 11 183 px, la leva è la glossa e si dice quale.

**Accettazione.** Pannello Performance durante l'hover del molo: 0 layout e 0 paint oltre il primo
frame. INP < 200 ms sull'hover di pannello e di riga. CPU rallentata 4× a 390 px. Prova a moto
normale e a moto ridotto. `gzip -9` sui quattro file. `curl` del `<head>` per verificare che ogni
`@import` abbia il suo `preload`.

---

## 8. RISCHI E REGRESSIONI

1. **Il margine legge come un filetto qualunque invece che come una firma.**
   *Guardia*: tre soli pesi su tutta la superficie — 1 px (ritmo), 2 px (molo), 3 px (ormeggio) —
   e nessun quarto. Prova: un censimento dei `border-*-width` sotto l'hero deve restituire
   **tre soli valori**; un censimento dei `border-*-color` deve restituire `--hairline`,
   `--hairline-strong`, `--seal-600`, `--route-1..4`, `--accent`, `--ink-3` e nient'altro — in
   particolare **nessun `rgb(15,37,71)`**.

2. **Il bronzo legge come lusso di plastica** (ANTI_PATTERNS §3: «oro/giallo saturo, gradienti
   metallici»). *Guardia*: `--seal-600` è desaturato e piatto, senza gradiente, senza ombra,
   senza lucidatura; compare su **un solo oggetto dell'intera superficie** — la minuta — e lì
   quattro volte (fondo `--seal-100`, filetto alto di 4 px, glifo scudo, filetto di margine).
   Nessun altro elemento sotto l'hero è bronzo: il plinto del promotore è `--hairline-strong`
   proprio per questo (§4.6). Mai `--brand-gold`, che resta la chiave della porta. Prova: un
   censimento dei colori calcolati sotto l'hero deve restituire `#8C6D4B` **solo** dentro
   `[data-section="antifraud"]`. Se in revisione umana la fascia legge «premio» invece di
   «atto», si toglie il fondo e resta il filetto — una riga.

3. **La minuta legge come una cookie bar.** *Guardia*: nessun raggio, nessuna icona in un tondo,
   nessun controllo di chiusura, nessun `role="alert"`, nessun rosso, due filetti di peso diverso,
   un margine di due colonne, 509 px di altezza e un rango verticale intero. Prova: schermata a
   1440 e a 390 **senza il resto della pagina** — se ritagliata da sola legge come una striscia,
   il disegno ha fallito.

4. **`--seal-100` non si distingue su uno schermo scadente.** *Guardia*: ΔE2000 **5,40**, 2,2
   volte la soglia di percettibilità; e l'oggetto non dipende dal fondo per essere identificato —
   lo identificano il filetto di 4 px a 3,86:1 e la larghezza a tutta pagina. HUMAN_QA 2.

5. **Il congedo cresce a desktop.** *Misurato e dichiarato*: +15 px a 1440 su :8771, +99 su
   :8770. *Guardia*: è il prezzo di 44 px di bersaglio su 15 link, scritto in §4.7 e non
   nascosto. Se il Council lo rifiuta, la leva è il bersaglio, non il layout, e la decisione è
   sua.

6. **Regressione dei test — inventario reale, con i numeri di riga.**
   **Nessuna classe è rinominata su questa superficie.** Ogni asserzione qui sotto è stata
   letta, non ipotizzata:

   | asserzione | file:riga | esito |
   |---|---|---|
   | `<h2 class="section__title" id="home-entrances-title">` | `test_home.py:247` | **passa** — la classe non cambia; `shead` sta sul `<header>` |
   | `<h2 class="section__title" id="home-trust-title">…` ×3 | `test_home.py:505, :507, :522` | **passa** — idem, `lang="fr"` compreso |
   | `<h2 class="visually-hidden" id="home-entrances-title">` | `test_home.py` (`test_blank_heading…`) | **passa** — il ramo `{% else %}` è ripristinato |
   | `class="antifraud-panel__body"` e `… lang="fr"` | `test_home.py:60, :66` | **passa** — la classe e l'ordine degli attributi non cambiano |
   | `"#icon-shield" in block` | `test_home.py:363`, `test_institutional.py:200`, `test_views.py:134` | **passa** — nessun `icon-seal`, lo scudo resta |
   | `class="empty-state"` nel blocco news | `test_home.py:392` | **passa** — il componente non è toccato, solo avvolto |
   | `<h3 class="card__title"><a href="…">` ×3 | `test_home.py:408` | **passa** — `flat=True` cambia solo la classe dell'`<article>` |
   | `<ol class="register register--entrances` ×1, `<li class="register__item">` ×4 | `test_home.py:208, :214, :545` | **passa** — markup identico |
   | `class="entry__ordinal"` in ogni voce | `test_home.py:230` | **passa** — l'elemento resta nel DOM (è `display: none` solo nella testata, non nel molo, dove è **visibile** come indice, che §8.5 richiede) |
   | `class="entry__title"` ×4, `<h3 class="entry__title"` ×4 | `test_home.py:217, :248` | **passa** |
   | `class="pathway-list__item"` ×8; `'class="pathway-list"' not in block` a gate chiuso | `test_home.py:325, :313` | **passa** — classi invariate, nessun `.reglist` |
   | `class="home-trust__column"` ×2 | `test_home.py:334` | **passa** |
   | `.register--entrances .entry` count 4, `is_visible()` | `test_browser.py:120, :121, :148, :174, :247` | **passa** |
   | `<footer class="site-footer` | `test_layout.py:50` | **passa** — `congedo` è aggiunta **dopo**, il prefisso resta |
   | `class="site-footer__version"` | `test_layout.py:103` | **passa** — attributo intero invariato |
   | `class="site-footer__antifraud"` presente / assente secondo il gate | `test_layout.py:119, :125` | **passa** — attributo intero invariato, gate ridichiarato |
   | «marque déposée» / «marchio depositato» | `test_layout.py:105`, `test_footer_trademark_words_per_language` | **passa** — `{% brand_words %}` conservato verbatim; nessun template di questa spec scrive una formulazione di marchio a mano, quindi le due varianti FR/IT che `apps/cms/forbidden.py` elenca come vietate (righe 23-24 della lista) e il carattere vietato da `FORBIDDEN_CHARACTERS` non possono entrare |
   | `card__title` ×3, `empty-state` ×1 su showcase | `test_design_showcase.py:121, :122` | **passa** — nessun componente condiviso modificato |

   *Guardia*: il collaudo è `pytest apps/pages tests/frontend tests/i18n` + `test_browser.py`
   **prima** di qualunque aggiornamento dei test. Se una sola di queste asserzioni cade, la causa
   è un errore di implementazione, non un aggiornamento dovuto: **questa spec non chiede a nessuno
   di modificare un test.**

7. **Perdita di un fatto — il collaudo è un diff, e adesso elenca gli attributi.**
   Il testo estratto della home prima e dopo deve essere **identico parola per parola** su
   `/fr/`, `/it/`, `/en/`, `/ar/`, su **entrambi** i server. Oltre alle parole, il diff deve
   preservare:
   - `id="{{ title_id }}"` su ogni `h2` di sezione, e la coppia `aria-labelledby` ↔ `id`;
   - ogni `lang="…"` di parte (l'elenco in §6);
   - `data-section`, `data-route`, `data-faq`, `data-partners`, `data-articles`, `data-pathways`,
     `data-trust`, `data-locked`, `data-banner`, `data-dismissible`;
   - `role="status"` su `.empty-state`; `aria-hidden="true"` su `.entry__ordinal`,
     `.route__glyph`, `.avviso__seal`, `.soglia__arch`, `.congedo__close`;
   - `aria-label` sui due `<nav>` del piè di pagina e sull'`<ol>` del molo;
   - `datetime="{{ …|date:'Y-m-d' }}"` sul `<time>` di «contenus vérifiés le»;
   - `target="_blank" rel="noopener"` sulle righe `footer_menu` che lo chiedono;
   - `translate="no"` sul nome del promotore;
   - il conteggio delle intestazioni: **9 `h2` + 17 `h3`** in `main`, **3 `h2`** nel piè di pagina.
   E `cms.forbidden.scan()` deve restituire **vuoto** su ogni pagina in ogni lingua: nessuna
   formulazione vietata entra in `alt`, `aria-label`, `title`, `figcaption` o testo nascosto.
   Le uniche stringhe nuove di questa spec sono in `figcaption` (§4.9) e vengono dai campi
   `caption_place` / `caption_date` / `credit` dell'asset, non da un template.

8. **La modifica trasversale su `.section__header`.** *Guardia*: schermate a 1440 e 390 di
   `/fr/entreprises/`, `/fr/institutions/`, `/fr/universites-et-formation/`, `/fr/projet-pilote/`,
   `/fr/parcours/`, `/fr/parcours/diplomes/` prima e dopo, più `test_gated_pages.py:127`
   (`<h2 id="destinataires-title" class="section__title">`), che non tocca la larghezza.

9. **Il vero blocco resta a monte.** Finché `static/css/v2/bridge.css` mappa
   `--navy: var(--brand-navy)`, il tricolore continua a colare nei controlli e nei bordi (difetto
   1.1). Questa spec **non aspetta**: ridichiara il bordo del molo e il bordo dell'avviso. Ma
   assume come precondizione che `v3/buttons.css` resti in carico e che il bottone primario su
   chiaro sia `--accent` con testo `--min-0` (5,69:1), perché la soglia di §4.7 lo usa.

---

## 9. CIÒ CHE QUESTA SPEC **NON** POSSIEDE

Il round 1 ha fallito soprattutto per questo: ha riscritto, peggio, tre oggetti che il Council
aveva già assegnato. L'elenco è qui in cima alla memoria e non in fondo.

| oggetto | proprietario | che cosa questa spec fa |
|---|---|---|
| Fondi, graticola, grana, lume, rampe, linea di marea | spec **`backgrounds`** §4.1–4.5 | **consuma**. La graticola del round 1 (grigia, a 160 px, in `--mortar`) e la «piega» sono cancellate: sono `--grat-module` e `th--fold` + `.tide`, meglio disegnate. Questa spec **non dichiara un solo `background-image`.** |
| Reveal, cuciture fra sezioni, sezione pinnata, barra di lettura | spec **`scroll`** §4.2–4.5 | **dichiara**. Il rail dei movimenti è il `readbar`; i quattro ruoli di reveal sono i suoi; questa spec mette gli attributi e non scrive JavaScript. `section--rule` su `_reserved` viene da lì. |
| Pipeline fotografica, apparato di didascalia, AVIF | spec **`imagery`** §1.4–1.6 | **dipende**. §4.9 disegna lo slot e il brief; la causa del blocco (`seeds_media.py:182` non scrive i quattro campi; nessun AVIF; `MAX_BYTES` tarato a 350 KB contro un budget di 120) è misurata là. |
| `.btn--primary` / `--secondary` / `--tertiary`, il navy nel `bridge` | spec **`buttons`** + `v3/buttons.css` | **consuma**. §4.5 e §4.7 usano SECONDARY e PRIMARY come §10 li definisce, senza ridipingerli. |
| `components/empty_state.html` e §9.6 | chi possiede §9.6 | **non tocca**. Solo un discendente scoped (§4.8). Il glifo arco+gradini per gli stati vuoti è consegnato là. |
| `components/section_header.html` e le quattro pagine ecosistema | spec **`company-forum-academy`** | **corregge il minimo** (la colonna da 420,75 px) e **consegna** la composizione a due fuochi, che richiede un contratto diverso. |
| `components/jurisdiction.html` (§9.3) | chi possiede §9.3 | **non tocca**. Misura e segnala: componente 105 px, barra 20 px, 8 segmenti da 18 px, su una sezione di 1 002 px. |
| `forum/partials/home_banner.html` | spec **`company-forum-academy`** | **non tocca** il contenuto; stila il contenitore e porta il controllo di chiusura a 44 px. |
| La porta dell'hero e la rotta del pilota | spec **`hero-doorway`**, **`scroll`** | **non tocca**. Segnala il superamento del budget: **due** oggetti legati allo scroll contro l'uno ammesso (`home.js:95` e `:116`). |
