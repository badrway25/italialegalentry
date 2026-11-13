# V3 — SHELL DELLA PIATTAFORMA («la scrivania»)

Superficie `platform-shell` · **round 2**, 24 settembre 2026 · vincolante con `DESIGN_SYSTEM_V2.md` e
`MOTION_SYSTEM.md` · risponde a `docs/design-v3/reviews/platform-shell.md`.

**Provenienza delle misure.** Due insiemi, tenuti distinti perché non hanno lo stesso valore.

- *Round 1* — stato attuale, Chromium headless di Playwright contro `http://127.0.0.1:8770` con
  sessione lato server per `qa-person@example.test` e `demo-professionnel@example.test`, a
  1440×900 · 1024×900 · 768×1024 · 390×844. File: `scratchpad/shellaudit/measure.json`. Il § 1 le
  riporta e **le dichiara come tali**: sono del round 1, non ricalcolate qui, salvo le tre righe
  marcate **[ri-verificato]**.
- *Round 2* — questo documento. Foglio candidato `platform-shell.css` + patch, montato su una copia
  di pagina servita con `page.route()` sull'origine `127.0.0.1:8770` (così i font self-hosted e
  `main.css` sono quelli veri), Chromium headless proprio, **mai** la porta 9222. Misure di layout a
  1440×900 · 1280×900 · 1024×900 · 768×1024 (touch) · 390×844 (touch) · 360×800 (touch) ·
  1440×900 in `dir="rtl" lang="ar"`. Misure di colore: composizione alfa esatta in Python
  (luminanza relativa WCAG 2.x) **e** lettura dei pixel reali su PNG di screenshot per tutto ciò che
  dipende da un'opacità o da una maschera. Tutto in
  `C:\Users\<user>\AppData\Local\Temp\claude\shellfix\` (`measure.json`, `pix.png`, `contrast.py`).
  Ogni numero del round 2 è marcato **[m]**.

Nota operativa invariata: `:8771` risponde 200 ma non serve l'area riservata; l'audit della
piattaforma si fa su `:8770`.

---

## 0. RICHIESTE DI DEROGA

Cinque, numerate. Nessun'altra deviazione dai documenti vincolanti esiste in questo documento; se ne
trovate una non elencata qui, è un difetto e va segnalata come tale.

### A1 — `DESIGN_SYSTEM_V2` § 7 (DENSE vieta «ombre») contro § 2 (livello 3 porta `--shadow-3`)

**Clausola.** § 7, riga della tabella DENSE: vietate «ombre, vetro, reveal». § 2, riga livello 3:
«elevato (popover, menu, inspector) → `--shadow-3`». `PREMIUM_2026_PRINCIPLES` § 14 ripete il
divieto come test: «DENSE non ha ombre né vetro».

**Che cosa chiedo.** Che il divieto del § 7 si legga come rivolto alle **superfici in flusso della
pagina** — fogli, righe, pannelli, banda, rail, inspector — e **non** alle superfici transitorie
fuori flusso che occludono il contenuto e si chiudono: menu account, menu lingua, palette comandi.
Per queste ultime `--shadow-3` (menu) e `--shadow-5` (palette) restano.

**Perché.** Un pannello che galleggia sopra un testo e che il lettore deve poter distinguere dal
testo sottostante non è un ornamento: senza separazione il menu e il paragrafo che copre diventano
una sola immagine. Il § 7 vieta l'ombra come *materiale della pagina*, non come *segnale di
occlusione*; il § 2 assegna l'ombra esattamente a ciò che occlude. La lettura proposta è l'unica che
non annulla una delle due clausole.

**Che cosa costa.** (a) `grep box-shadow` su una pagina DENSE non torna più vuoto: il test del § 14
va riscritto per escludere `[popover]`, `.pbar__panel`, `.pcmd` — tre selettori, elencati qui.
(b) Rinuncio all'ombra ovunque altrove, **compreso il punto in cui il round 1 la usava**: la barra
scrollata perde `--shadow-2` (e con essa la transizione di `box-shadow`, che il vincolo di
prestazione vieta comunque), e l'inspector — che è **in flusso**, è un elemento della griglia, non
un pannello che galleggia — perde `--shadow-2` e scende dal livello 3 al livello 1. Il round 1
dichiarava `data-mode="DENSE"` e nella stessa pagina metteva `--shadow-2` sulla barra e
sull'inspector: quella contraddizione è eliminata, non negoziata. Il pannello account resta con
`--shadow-3` perché è esattamente il caso che questa deroga copre — `position: absolute`, copre il
contenuto, si chiude.
(c) La profondità dello spazio di lavoro deve venire da terreno, filetto e scala — ed è il § 4.4.

### A2 — `DESIGN_SYSTEM_V2` § 6 («sistema cartografico … **mai** su STANDARD/DENSE/LEGAL») contro § 9.1 («case band … con la banda territoriale al margine finale»)

**Clausola.** § 6, punto «Sistema cartografico»: graticola e isoipse «mai su STANDARD/DENSE/LEGAL».
§ 9.1, punto (2): la case band porta «la banda territoriale al margine finale». Il fascicolo è DENSE
per il § 7. Le due clausole non possono essere vere insieme.

**Che cosa chiedo.** Che il § 9.1 prevalga sul § 6 **limitatamente a due apparizioni nominate**, e a
nessun'altra: (1) un frammento di graticola 320 × 56 al margine finale della barra di piattaforma;
(2) la banda territoriale al margine finale della banda del fascicolo. Nessuna isoipse, mai, in
nessuna pagina della piattaforma. Nessuna terza apparizione senza una riga in questo documento.

**Perché.** Il § 9.1 è la clausola *specifica* per questa superficie ed è più recente del divieto
generale; il divieto generale esiste per impedire che la texture invada le pagine di lettura, non
per togliere alla piattaforma la sua unica firma grafica. La graticola non appare mai sotto un
testo, non porta informazione e sparisce in `forced-colors`.

**Che cosa costa.** Il test che oggi asserisce «nessun `<svg>` di territorio su DENSE» diventa
«nessun `<svg>` di territorio su DENSE **fuori da** `.pbar__grid` e `.pband__terr`»: due classi in
una lista bianca, e la lista bianca è la guardia contro la terza apparizione.

### A3 — `DESIGN_SYSTEM_V2` § 9.1 («case band `--mid-2` … riferimento in `--accent-dark`») contro § 1.3.5 («un capitolo mezzanotte per pagina fuori da HOME e FORUM»)

**Clausola.** § 9.1 (2) vuole la banda del fascicolo su `--mid-2`. § 9.1 (1) vuole la barra su
`--mid-1`. § 1.3.5 ammette **un** capitolo mezzanotte fuori da HOME e FORUM. Barra + banda = due.

**Che cosa chiedo.** Che il capitolo mezzanotte della piattaforma sia **la barra**, e che la banda
del fascicolo stia su `--min-1`. Conseguenza dichiarata: il riferimento di pratica non può stare in
`--accent-dark` (è un colore per fondo scuro) e **non sta nella banda affatto** — sale nella barra,
sulla targa, dove è già su mezzanotte e dove il § 9.1 (1) lo colloca («contesto in mono»). Un fatto,
un posto.

**Perché.** Il round 1 aveva fatto la stessa scelta **in silenzio**, ed è la sola cosa che il
revisore gli ha contestato senza chiamarla errore. La motivazione regge: due fasce scure impilate su
una pagina di lavoro alta 4 000 px rendono la piattaforma un cruscotto scuro, che è il registro
respinto dal committente, e violerebbero una regola di colore esplicita per rispettare una regola di
componente.

**Che cosa costa.** La banda perde il contrasto drammatico del fondo scuro; lo recupera con la scala
tipografica (Newsreader 48/52 **[m]**), con la banda territoriale (A2) e con il salto di terreno
`--min-0` → `--min-1`, misurato **1,076** di rapporto — percepibile come area, mai come testo.

### A4 — `DESIGN_SYSTEM_V2` § 9.1 («rail → striscia orizzontale scorrevole **36 px**») contro il vincolo WCAG 2.2 sui bersagli

**Clausola.** § 9.1 (3): sotto 1024 il rail diventa «striscia orizzontale scorrevole 36 px».

**Che cosa chiedo.** 44 px, non 36.

**Perché.** Sotto 1024 quella striscia è l'unico posto in cui un dito naviga. 36 px sta sotto il
minimo di 44 che il vincolo di accessibilità impone «dove il disegno lo permette», e qui il disegno
lo permette: 44 px misurati a 768 e a 390 non mandano nulla fuori schermo **[m]** (larghezza di
documento = larghezza di viewport a 360, 390, 768 — § 9, riga «nessuno scorrimento orizzontale»).

**Che cosa costa.** 8 px di cromo in più sul telefono. Nel bilancio complessivo il telefono ne
guadagna 434: la prima riga dello spazio di lavoro passa da `y = 843` (round 1, stato attuale) a
**`y = 409`** sul fascicolo più carico che il modello possa produrre **[m]**.

### A5 — Ritiro di «nessuna chiave di contesto nuova»

**Clausola.** Non è una clausola dei documenti vincolanti: è una promessa che il round 1 aveva fatto
a sé stesso, e che il revisore ha dimostrato inesigibile.

**Che cosa chiedo.** Di introdurre **un** processore di contesto, `accounts.context_processors.shell`,
che espone due chiavi di sola presentazione — `shell_operational` (bool) e `shell_role_label` (str).

**Perché.** Il round 1 gatava la palette e il rail comprimibile su `{% if user.is_staff %}`.
`apps/accounts/roles.py` definisce un RBAC deliberatamente separato da `is_staff` — il docstring di
`OPERATOR` dice testualmente che la vecchia piattaforma è criticata perché «its staff accounts all
carried full administration». `is_staff` **nasconde** la palette agli operatori a cui il § 9.1 la
destina e la **mostra** ad amministratori Django che non lavorano fascicoli. Non esiste oggi né un
filtro né una chiave che sappia dire «ruolo operativo», quindi la promessa era irrealizzabile.

**Che cosa costa.** Una riga in `config/settings/base.py` (dopo `core.context_processors.site`, riga
141) e un file nuovo di 18 righe. Nessun permesso cambia: il processore **legge** i gruppi, non ne
concede; ogni vista conserva il proprio controllo. Il codice esatto è al § 4.9.

---

## 0-bis. RISPOSTA PUNTO PER PUNTO

Ogni voce della revisione è **FATTO** o **CONTESTATO**. Non c'è una terza colonna.

| Revisione | Esito | Dove |
|---|---|---|
| **Violazione 1** — DENSE/ombre | FATTO — deroga A1; nessuna ombra in flusso, nessuna transizione di `box-shadow` | § 0/A1, § 4.4, § 5.1 |
| **Violazione 2** — skip link 4,11:1 | FATTO — `--min-0` su `--accent` = **5,69:1** calcolato; `--accent-ring` non regge più testo | § 4.2, § 6 |
| **Violazione 3** — `--accent` sul misuratore | FATTO — le tacche sono `--ink-2`; `--accent` resta a link, CTA, fuoco, barra della voce corrente | § 4.3, § 8 |
| **Violazione 4** — `{% if user.is_staff %}` | FATTO — deroga A5, predicato di ruolo reale, insieme nominato | § 4.9 |
| **Violazione 5** — i quattro fatti perduti | FATTO — sospensione, `status_since`, `overdue`, multi-attore con organismo e la frase di ripiego, tutti nella banda; due trame affiancate | § 4.3 |
| **Violazione 6** — banda `--mid-2` sovrascritta in silenzio | FATTO — deroga A3, dichiarata e argomentata | § 0/A3 |
| **Violazione 7** — `shell.plate.copy` senza innesco | FATTO — voce **eliminata** | § 5 |
| **Violazione 8** — citazioni sbagliate | FATTO — parallasse = § 0 di MOTION (riga PROFONDITÀ), non § 2; la terza molla 380/35 è **rifiutata** | § 2 n. 6, § 3 n. 1 |
| **Lacuna 1** — la banda fuori dal fascicolo | FATTO — la banda è un telaio attorno a `page_header.html`, che resta intatto | § 4.3 |
| **Lacuna 2** — lista template incompleta | FATTO — 23 voci, con il form POST di logout e il CSRF nominati | § 4.8 |
| **Lacuna 3** — `site.contact_email` | FATTO — **resta** nel piè di pagina del portale, accanto ai link legali | § 4.8 n. 1 |
| **Lacuna 4** — ordine di caricamento CSS | FATTO — `<link>` espliciti, nessun `@layer`, e il perché | § 4.10 |
| **Lacuna 5** — media query fantasma | FATTO — scritte e misurate a sei larghezze | § 4.1, § 9 |
| **Lacuna 6** — `.pbar` senza `position` | FATTO — `sticky`, `inset-block-start: 0`, `z-index: var(--z-header)` | § 4.2 |
| **Lacuna 7** — sbordo del rail a scroll 0 | FATTO — il fondo è una colonna della griglia, il rail è `max-block-size` (non `block-size`) | § 4.4 |
| **Lacuna 8** — `content-visibility` senza `contain-intrinsic-size` | FATTO — `content-visibility` **rimosso**: quattro sezioni corte non lo meritano | § 7 |
| **Lacuna 9** — targa senza stato vuoto | FATTO — la barra è una griglia `auto 1fr auto`, lo slot vuoto non muove nulla | § 4.2 |
| **Lacuna 10** — chiusura dei `<details>` | FATTO — compito 6 di `shell-portal.js`, e i due menu hanno una voce di moto | § 4.11, § 5.6 |
| **Lacuna 11** — lock-up sotto 480 | FATTO — `.visually-hidden` sul testo, nome accessibile intatto, nessuna modifica a `cms_nav.py` | § 4.2 |
| **Lacuna 12** — `rgb(29 138 147 / .30)` letterale | FATTO — `color-mix()` + `@supports` di ripiego | § 4.6 |
| **Lacuna 13** — `behavior: 'smooth'` implicito | FATTO — non è moto: uscita da MOTION, entra nei compiti JS con `behavior: 'auto'` sempre | § 4.11 n. 7 |
| **Lacuna 14** — `scaleY()` su righe con bordo | FATTO — l'evidenziatore **non ha** bordo né raggio, e il motivo è scritto | § 4.4, § 5.2 |
| **Lacuna 15** — `--ok-800` e `--seal-700` | FATTO (token eliminati) + **numero contestato**: vedi sotto | § 4.1 |
| **Cheap 1** — scheletro Linear | FATTO — la geometria cambia: dorso, margine di registro, rigatura, tre terreni | § 4.4 |
| **Cheap 2** — il chip `⌘K` | FATTO — nessun chip: legenda in mono, come un folio; sparisce sotto 1024 | § 4.2 |
| **Cheap 3** — monogramma due volte | FATTO — **nessun monogramma**, da nessuna parte | § 4.2, § 4.4 |
| **Cheap 4** — graticola all'8 % invisibile | FATTO — misurata a cinque opacità sui pixel; 8 % = **1,119:1**, scartato; 22 % = **1,419:1** | § 4.2, § 9 |
| **Cheap 5** — lo spazio di lavoro vuoto | FATTO — quattro mosse materiali, tutte misurate | § 4.4 |
| **Cheap 6** — «ع» al posto del nome | FATTO — `{{ l.name }}` da `site.languages`, come oggi; nessuna lingua codificata | § 4.2 |
| **Cheap 7** — misuratore a segmenti da kit | FATTO — tacche verticali 2 × 14 in cadenza mono: tacche di registro, non barra di avanzamento | § 4.3 |
| **Cheap 8** — la griglia di stati uniforme | FATTO — tre tabelle separate, solo gli stati che il componente ha | § 4.6 |

**Punto contestato, uno.** Lacuna 15 afferma che gli usi dichiarati stanno su `--min-3` «dove
`--ok-700` misura 5,32:1 e `--seal-600` **3,99:1**». Il primo numero è esatto: `#1e7a4d` su
`#ffffff` = **5,322:1**, ricalcolato. Il secondo no: `#8c6d4b` su `#ffffff` = **4,768:1**;
**3,995:1** è il rapporto di `--seal-600` su `--min-1`, non su `--min-3`. Calcolo: luminanza
relativa WCAG 2.x, `(L₁+0,05)/(L₂+0,05)`, in `contrast.py`. **La conclusione della lacuna resta
integralmente accolta**: entrambi i colori passano già dove servono, i due token nuovi non servono, e
`--ok-800` e `--seal-700` sono **eliminati** da questo documento.

---

## 1. VERDETTO SULLO STATO ATTUALE

Misure del round 1, invariate salvo dove indicato. Non è una shell «da migliorare»: è la stessa del
21 settembre con i colori ripuntati da `bridge.css`.

1. **A 390 la barra è alta 161 px ed è `sticky`.** `.portal-bar` → `{h: 161}`; `.portal-bar__inner`
   ha `flex-wrap: wrap` e impila wordmark / contesto / account su tre righe (`crop_390_top.png`).
   Il 19 % del viewport è occupato per sempre, su una pagina alta 7 994 px.
2. **La prima priorità è sotto la piega sul telefono.** `.next-action` inizia a `y = 843` in un
   viewport di 844. A 1440 inizia a `y = 444`: il 49 % della piega è cromo.
3. **Il portale non porta il marchio.** `.portal-bar__brand` contiene solo
   `<span class="portal-bar__wordmark">`, 135,4 × 28 px, Newsreader 18 px. Il lock-up ufficiale
   esiste già — `cms_nav.brand_lockup`, variante `dark` compresa — e il sito pubblico lo usa.
   **[ri-verificato]** `brand_lockup("dark")` emette `<img class="lock__mark" … alt="">` più
   `.lock__text`, e `v2/shell.css` gli dà tassello `--min-0` 46 px raggio 6 e wordmark `--on-dark`.
4. **L'inspector non esiste.** `querySelector('.portal-inspector, .inspector, [data-inspector]')` →
   `null` a ogni larghezza, per la persona e per il professionista.
5. **Il rail è un `<ul>` nudo.** 240 px, righe da 44, `background-color: rgba(0,0,0,0)`, nessun
   glifo, nessuna parola di stato. **[ri-verificato]** il numero dei non letti è cucito dentro la
   stringa dell'etichetta: `portal/services.py` riga 668,
   `messages_label = _("Communications (%(count)d)")`.
6. **Sotto 1024 il rail non diventa una striscia.** A 768 `.portal__aside` è `position: static`;
   a 390 è alto 278 e spinge `.portal__main` a `y = 1418`. Chip alti 38 px.
7. **Profondità: zero.** `shadowCount = 0` su barra, banda, prochaine étape, rail e figli diretti
   della colonna. Dei sette livelli di superficie la piattaforma ne usa **uno**.
8. **Moto: zero.** Le 20 transizioni dichiarate nel cromo sono `color, text-decoration-color; .18s`.
   **[ri-verificato]** `static/js/dist/shell.js` = 1 136 B grezzi / **613 B gz**; il chunk condiviso
   di Motion = 70 441 B grezzi / **26 120 B gz** (il round 1 diceva 26 143: ricalcolato, è 26 120).
   `shell.js` agisce su `.site-header` e `[data-reveal]`, che nel portale non esistono.
9. **Un secondo blu strutturale.** `.next-action__inner` ha `border-left-color: rgb(95,132,181)`.
   **[ri-verificato]** `--state-info-br: #5f84b5` è in `static/css/tokens.css` riga 66 e **non** è
   ripuntato da `bridge.css`. Peggio di come il round 1 l'aveva detto: l'intera famiglia legacy è un
   blu — `--state-done-fg` e `--state-info-fg` sono `#1e4a85` (righe 61 e 64). La pillola di stato
   della banda **non** userà quella famiglia (§ 4.3).
10. **Tipografia fuori scala.** `.page-header__title` = 38/36 a 1440, 32/36 a 1024 e 768, 28/36 a
    390. Né 38 né 28 sono fra gli undici corpi ammessi; 38/36 ha interlinea minore del corpo.
11. **Il contesto è detto due volte con due grammatiche.** `CONTEXTE …` nella barra in mono a 17 px
    e `DOSSIER …` nella banda a `--t-entry`. Un fatto, due trattamenti.
12. **60 px per due parole.** `.breadcrumbs` è una fascia alta 60. Con titolo e filetto: 255 px di
    cromo prima della banda del fascicolo. **[ri-verificato]** al round 2: montando la briciola
    esistente dentro `.pband__crumbs` senza altro che `padding: 0`, la stessa `<nav>` misura
    **28 px** **[m]** — i 60 sono padding, non contenuto.
13. **Lo staff non ha una shell propria.** **[ri-verificato]** `grep -rn "data-mode" templates/`
    → zero occorrenze: il contratto del § 7 non è applicato da nessuna parte.
14. **Bersagli sotto i 44 px.** «Site public» 72,1 × 29; sommario account 83 × 36; lingua 91,7 × 36;
    tre link del piè di pagina × 28. A 390 account e lingua scendono a 28.
15. **Appiccicosità scalibrata.** `.portal__aside` si ferma a `top: 96px` mentre la barra è alta 62,
    e nessun `scroll-padding-block-start` compensa la barra al fuoco.

---

## 2. UI-UX-PRO-MAX — interrogazioni, esiti, decisioni

| # | Interrogazione (verbatim) · dominio | Esito | Decisione |
|---|---|---|---|
| 1 | `application shell navigation rail sidebar dashboard layout` · `ux` | *Sticky Navigation*, *Keyboard Navigation*, *Breadcrumbs* (da 3 livelli in su) | **ACCETTATO in parte.** La compensazione diventa `scroll-padding-block-start` su `:root` (difetto 15); la tastiera entra nel § 6. **RIFIUTATO** il punto briciole: il portale ha 2 livelli, ma la briciola è l'unica via di ritorno da un dettaglio di pratica — resta, ridotta a 28 px misurati dentro la banda |
| 2 | `sidebar navigation collapsed icon rail` · `ux` | le stesse tre righe: il corpus **non ha una voce sul rail comprimibile** | **RIFIUTATO per assenza di dato.** Il pattern viene da 21st.dev e dal Council, non da qui. Dichiarato perché il silenzio del database non è un avallo |
| 3 | `command palette cmd+k enterprise application` · `ux` | **0 risultati** | **NESSUNA CORRISPONDENZA IN DATABASE.** Le regole della palette vengono da WAI-ARIA `combobox` |
| 4 | `dashboard information density enterprise product` · `product` | *B2B Service* → «Accessible & Ethical + Minimalism & Swiss», «Bento Box Grid, Micro-interactions», «Professional blue + neutral grey» | **RIFIUTATO il registro** (grigio-blu anonimo respinto dal committente). **ACCETTATO** «Micro-interactions». **RIFIUTATO «Bento Box Grid»**: la griglia di riquadri uguali è ciò che il Council ha bocciato 3/10 — ed è anche la ragione per cui la colonna centrale del § 4.4 è **un registro continuo**, non una pila di schede |
| 5 | `keyboard shortcuts power user productivity` · `product` | *Productivity Tool* → «Flat Design + Micro-interactions»; *Developer Tool/IDE* → «Dark Mode + Minimalism» | **RIFIUTATO «Flat Design»** (è il difetto 7 messo a norma) e **rifiutato il registro dev-tool**. Trattengo **solo** la legittimità delle scorciatoie per i ruoli operativi |
| 6 | `depth elevation layered surfaces premium dark interface` · `style` | `dimensional-layering`: «z-index 1-4, elevation sm/md/lg/xl, backdrop-filter, parallax», accessibilità `risk:high` | **ACCETTATO il principio** (la profondità si legge per strati), **RIFIUTATA l'implementazione**: nessuna quinta scala d'ombre, nessun `translateZ()`, **nessun parallasse** — vietato da **`MOTION_SYSTEM` § 0, riga PROFONDITÀ, colonna «esempio vietato»: «parallasse costante su tutta la pagina»** (il round 1 citava il § 2: errore, il § 2 è «Le nove famiglie»). `backdrop-filter` solo dove è già ammesso, cioè **non qui** |
| 7 | `sidebar panel slide reveal stagger navigation` · `gsap` | Scroll Reveal 400-600 ms `power2.out`; Stagger List «non oltre ~8 figli» | **ACCETTATA la disciplina, RIFIUTATA la libreria**: GSAP non è installato e non lo sarà. Le durate 400-600 non esistono nel sistema → `--motion-base` 240 ms. **Accettato** il tetto: il rail ha 10-13 voci, quindi **una** animazione di gruppo, non 13 |
| 8 | `government legal platform application shell premium` · `--design-system` | «Enterprise Gateway»; `#1E40AF / #3B82F6 / #16A34A / #EFF6FF`; EB Garamond + Lato **via Google Fonts CDN**; «AVOID: motion effects» | **RIFIUTATO quasi per intero.** (a) font da CDN remoto: `style-src 'self'` lo vieta; (b) tre colori interattivi dove il sistema ne ammette **uno**; (c) «AVOID: motion effects» è il registro respinto il 24 settembre. **ACCETTATA** solo la checklist: niente emoji come icone, ≥ 4,5:1, focus visibile, `prefers-reduced-motion`, 44 × 44, verifica a 375/768/1024/1440 |

---

## 3. 21ST.DEV — candidati confrontati

Nessun pacchetto installato: React, Tailwind, `cn()`, `lucide-react`, raggi `rounded-xl/2xl` sono
fuori contratto. Si estrae il **pattern** e lo si riscrive in Django + token V2. `get_component`
chiamato su tre (⬢); mai `generate` né `iterate_generation`.

| # | Candidato · URL | Che cosa prendo | Che cosa rifiuto, e perché |
|---|---|---|---|
| 1 ⬢ | **Animated Sidebar** (beui/starc007) · `21st.dev/@starc007/components/animated-sidebar` | (a) larghezze come **token** (`--shell-rail`, `-collapsed`) lette dalla griglia, non numeri magici; (b) `data-rail="expanded\|collapsed"` sul contenitore, i figli si disegnano da soli — ideale per una shell resa dal server; (c) il **principio** della molla critica, «so it cannot overshoot»; (d) da compresso, `aria-label` **e** `title` riportano il nome accessibile perso dall'etichetta; (e) aprire un gruppo mentre è compresso **espande il rail**; (f) foglio mobile con trappola del fuoco, Escape, blocco scroll con ripristino, `inert` da chiuso | `animate={{ width }}` anima la **larghezza** → layout a ogni frame (sostituito da FLIP, § 5.3); `filter: blur(3px)` sui sottomenu (`filter` vietato); raggi `rounded-xl/2xl`; `whileTap scale(.98)`; scrim `bg-black/40` codificato; **e i numeri della molla: 380/35/0.75 è una terza molla, e `MOTION_SYSTEM` § 1 ne ammette due.** Prendo il principio, uso `SPRING_SETTLE` 260/30 e `SPRING_FOLLOW` 400/40. Verificato che bastino: rapporto di smorzamento ζ = c/(2√(k·m)) con m = 1 → **SPRING_FOLLOW ζ = 40/(2√400) = 1,000**, criticamente smorzata, sovraelongazione nulla; **SPRING_SETTLE ζ = 30/(2√260) = 0,930**, sovraelongazione teorica `exp(−πζ/√(1−ζ²))` = **0,034 %** — su una corsa di 160 px sono 0,05 px, cioè meno di un pixel fisico. Nessun rimbalzo osservabile, nessuna terza molla |
| 2 ⬢ | **sidebar-001** (unlumen) · `21st.dev/@unlumen/components/sidebar-001` | (a) **un solo** evidenziatore hover spostato sul rettangolo della voce puntata, invece di N sfondi → 1 strato composito invece di 13 ripitture; (b) i **trattini per voce** come *texture* del rail; (c) la voce corrente portata in vista se è fuori dal riquadro scorrevole | **Rifiutato l'attenuamento dei fratelli** (`opacity: .3` sul testo): «nessuna opacità sul testo» § 3.2, e fallisce in `forced-colors`. Rifiutato `x: 8/6/0` (traslazione fisica: si rompe in RTL). Rifiutato `layoutId` per il marcatore viaggiante: viaggiare presuppone una SPA. Rifiutati drag-to-resize e `animate={{height:'auto'}}` |
| 3 | **Dashboard Sidebar** «Charcoal Ink / Alabaster» (arunjdass) · `21st.dev/@arunjdass/components/dashboard-sidebar` | La prova che il rail deve avere un **fondo proprio**, non essere trasparente sulla tela — risposta diretta al difetto 5. Da qui nasce il **dorso** del § 4.4 | La navigazione annidata a più livelli: la nostra ha 10-13 voci piatte. Rifiutata l'estetica «AI product» dei riquadri con gradiente. **E rifiutati i due capitoli cromatici**: su questa superficie ne abbiamo uno solo (deroga A3) |
| 4 ⬢ | **Page Header with Breadcrumbs** (7ovr) · `21st.dev/@7ovr/components/page-header-2` | La struttura **briciole → titolo + azioni → metadati**: è la fusione che elimina i 255 px del difetto 12; azioni allineate al margine finale del titolo | Il `status badge` di solo colore: da noi lo stato è **glifo + parola + forma**. Rifiutata la fila di bottoni tutti uguali: la banda ha **un'** azione primaria |
| 5 | **Command Menu with Global Search** (ephraimduncan) · `21st.dev/@ephraimduncan/components/command-menu-04` | I **filtri di tipo** e le sezioni «recenti»: da noi «Dossiers · Documents · Personnes · Actions», con la pratica corrente precaricata dalla targa | Rifiutata la ricerca globale su *tutto*: con permessi per ruolo, una palette che mostra ciò che non si può aprire è una fuga d'informazione. Interroga **solo** endpoint già autorizzati per il ruolo (§ 4.9) |
| 6 | **Sidebar with Search and Profile** (uiable) · `21st.dev/@uiable/components/sidebar-5` | Il **piede del rail con l'identità** invece di un account perso nella barra: dà al rail un fondo e una fine | Rifiutata la «pro-upgrade promo card». Rifiutati i badge numerici senza testo alternativo. **E rifiutato il monogramma**: iniziali-in-un-cerchio è il componente più di serie di ogni kit, e il round 1 l'aveva preso due volte. Il piede porta **nome + etichetta di ruolo**, come un blocco di firma su un atto |
| 7 | **Information Drawer** (hyperiux) · `21st.dev/@hyperiux/components/information-drawer` | Pannello di dettaglio a tutta altezza con fallback `prefers-reduced-motion` esplicito: è la forma dell'inspector sotto 1200 | Rifiutato GSAP. Rifiutato il cassetto **modale**: l'inspector non è una decisione, è contesto. Rifiutato il «fade a stadi»: sotto 1200 l'inspector non entra, **è già lì** |
| 8 | **Sidebar Dashboard Skeleton** (cnippet-dev) · `21st.dev/@cnippet-dev/components/v-skeleton-8` | Lo scheletro che **rispecchia** la griglia reale: è lo stato di caricamento del § 9.6, e serve alla palette che interroga dopo l'apertura | Rifiutata l'animazione «shimmer» (loop su `background-position` di un'area grande: vietato). Il nostro scheletro è **fermo**, livello 1, con `aria-busy`. **E rifiutato l'uso sul rail**: il rail è reso dal server insieme alla pagina, non ha mai uno stato di caricamento — era la cella riempita per completare una matrice (cheap 8) |

---

## 4. LA PROPOSTA

Tre regioni, un cambio di terreno, un marchio solo, e **una stanza che ha un materiale**: la
scrivania di un'istituzione, non il cruscotto di una SaaS.

File nuovi: `static/css/v3/tokens-shell.css`, `static/css/v3/platform-shell.css`,
`static/js/src/shell-portal.js` → `static/js/dist/shell-portal.js`,
`apps/accounts/context_processors.py`.

### 4.0 Modalità di pagina — la regola che chiude la violazione 1

Il § 7 assegna il modo alla **pagina**. La shell è **condivisa** fra pagine di modo diverso: la
stessa barra sta sopra un cruscotto RICH e sopra un fascicolo DENSE.

> **La shell è scritta per DENSE e non cambia con il modo della pagina.** La scrivania non cambia
> materiale perché è cambiato il foglio che c'è sopra.

Attribuzione, esplicita, così che `data-mode` non sia una decisione dell'implementatore:

| `data-mode` | Template |
|---|---|
| `RICH` | `portal/dashboard.html`, `companies/dashboard.html`, `academy/catalogue.html`, `academy/course_detail.html`, `academy/plan_detail.html`, `academy/mine.html`, `academy/enrolment_detail.html` |
| `DENSE` | `cases/index.html`, `cases/detail.html`, `cases/assessment.html`, `portal/requests.html`, `portal/request_detail.html`, `portal/documents.html`, `portal/deadlines.html`, `portal/messages.html`, `portal/message_detail.html`, `portal/pathways.html`, `portal/situation.html`, `documents/*.html`, `helpdesk/*.html`, `selection/*.html`, `companies/needs.html`, `companies/need_detail.html`, `companies/need_form.html`, `companies/analysis.html`, `forum/governance/*.html` |
| `STANDARD` | `companies/profile.html`, `companies/profile_form.html`, `portal/unavailable.html` |

L'attributo sta su `<body>` via `{% block body_class %}`… no: su `<html>` non si può da un template
figlio, quindi sta su `<body>`, aggiunto da `base_portal.html` con
`{% block body_data %}data-mode="DENSE"{% endblock %}` e sovrascritto dai sette template RICH e dai
tre STANDARD. Il test del § 7 conta gli override, non i template.

### 4.1 Token

`static/css/v3/tokens-shell.css` — **otto variabili di layout, un segno di direzione, e nessun colore nuovo.** I token
`--ok-800` e `--seal-700` del round 1 sono eliminati (lacuna 15).

```css
:root {
  --shell-bar-h: 56px;
  --shell-rail: 224px;
  --shell-rail-collapsed: 64px;
  --shell-inspector: 320px;
  --shell-strip-h: 44px;
  --shell-row-h: 40px;
  --shell-margin: 56px;   /* il margine del registro dentro il foglio centrale */
  --shell-rule: 28px;     /* il passo della rigatura = l'interlinea del corpo (17/28) */
  --dir: 1;
}
[dir="rtl"] { --dir: -1; }

@media (max-width: 47.999rem)                           { :root { --shell-bar-h: 52px; } }
@media (min-width: 75rem) and (max-width: 89.999rem)    { :root { --shell-inspector: 300px; } }
@media (pointer: coarse)                                { :root { --shell-row-h: 44px; } }
```

Le tre media query esistevano nel round 1 solo come commenti. Verificate in browser: a 768 e 390
(contesto `has_touch`) `(pointer: coarse)` corrisponde e ogni riga del rail misura **44 px**; a 1440
misura **40 px** **[m]**.

**Rapporti usati in questo documento.** Tutti ricalcolati in `contrast.py` (luminanza relativa
WCAG 2.x). Nessuno è ereditato dal round 1 senza ricalcolo.

| Coppia | Rapporto | Dove |
|---|---:|---|
| `--min-0` su `--accent` | **5,692** | testo dello skip link e della CTA primaria |
| `--min-3` su `--accent` | 6,316 | alternativa, non usata (§ 10 del DS fissa `--min-0`) |
| `--min-3` su `--accent-ring` | **4,110** | **fallisce AA** — è ciò che il round 1 prescriveva |
| `--ink` su `--min-1` | 13,594 | titolo e valori della banda |
| `--ink-2` su `--min-1` | 6,004 | righe del rail a riposo, tacche del misuratore |
| `--ink-3` su `--min-1` | 5,142 | etichette dei fatti, briciole |
| `--accent` su `--min-1` | 5,291 | link dentro la banda |
| `--accent-ring` su `--min-1` | 3,443 | anello di fuoco (≥ 3:1, non testuale) |
| `--hairline-strong` su `--min-1` | 3,136 | bordo di componente, tacche vuote |
| `--ink-2` su `--min-3` | 7,167 | pillola di stato, famiglia «in lavorazione» |
| `--ok-700` su `--min-3` | **5,322** | pillola, famiglia «concluso» |
| `--pending-700` su `--min-3` | **6,984** | pillola «in attesa» e testata della sospensione |
| `--err-700` su `--min-3` | **6,536** | «n en retard» |
| `--seal-600` su `--min-1` | **3,995** | anello del ruolo d'autorità (non testuale, ≥ 3:1) |
| `--seal-600` su `--min-3` | **4,768** | il numero che la revisione dava a 3,99 |
| `--on-dark` su `--mid-1` | 15,509 | wordmark e valore della targa |
| `--on-dark-2` su `--mid-1` | 9,683 | controlli della barra a riposo |
| `--on-dark-3` su `--mid-1` | 6,439 | etichetta della targa, legenda dei tasti |
| `--on-dark` su `--mid-2` | 14,079 | valore della targa (fondo `--mid-2`) |
| `--on-dark-3` su `--mid-2` | 5,846 | etichetta della targa |
| `--on-dark` su `--mid-4` | 10,562 | voci del pannello account |
| `--accent-dark` su `--mid-1` | 10,014 | anello di fuoco sui controlli scuri |
| `--terr-line` su `--mid-1` | 6,072 | riferimento (la graticola sta **molto** sotto: § 4.2) |

**Salti di terreno** (percepibili come area, mai leggibili come testo):
`--min-1`/`--min-0` = **1,076** · `--min-2`/`--min-0` = **1,064** · `--min-2`/`--min-1` = **1,144** ·
`--min-3`/`--min-1` = **1,194** · `--mid-0`/`--mid-1` = **1,055**.

**Filetti compositi** (α su fondo, composizione esatta):
`--hairline-dark-strong` su `--mid-1` → `#465359`, rapporto **2,202** ·
`--hairline-dark` su `--mid-1` → `#2a373e`, rapporto **1,429** ·
`--hairline` su `--min-0` → rapporto **1,365** **[m, letto sui pixel]**. Quest'ultimo è la **soglia
di percettibilità** che il resto del documento usa: è il filetto informativo che il sistema già
accetta come visibile, quindi nessuna grafica di questa superficie può stare sotto di esso.

### 4.2 Regione 1 — la barra di piattaforma (56 px, `--mid-1`)

`templates/partials/portal_chrome.html`, riscritto. Il contenitore:

```css
.pbar { position: sticky; inset-block-start: 0; z-index: var(--z-header);
        background: var(--mid-1); color: var(--on-dark);
        border-block-end: 1px solid var(--hairline-dark-strong); }
.pbar__inner { position: relative; display: grid;
  grid-template-columns: auto minmax(0,1fr) auto;   /* marchio · contesto · controlli */
  align-items: center; column-gap: var(--s-4);
  block-size: var(--shell-bar-h);
  max-inline-size: var(--container); margin-inline: auto;
  padding-inline: var(--grid-margin); }
```

`grid-template-columns: auto 1fr auto` chiude la **lacuna 9**: su una pagina senza
`portal_context` la colonna centrale resta vuota e **nulla si muove** — niente `margin-inline-start:
auto` da riposizionare, niente caso speciale. Misurato: la barra è alta **57 px** (56 + il filetto) a
1440/1280/1024/768 e **53 px** a 390/360 **[m]**.

**1. Lock-up ufficiale, variante scura.** `{% brand_lockup "dark" %}`, la stessa del piè di pagina
pubblico. Nessuna tagline, nessuna didascalia (`BRAND_ASSETS.md` § 1). Scalato **come unità** dentro
56 px — il tassello del § 8.1 è 46 px e non ci sta, quindi l'unità scende conservando il rapporto
46/20 ≈ 2,30 → **34/15** (2,27):

```css
.pbar .lock--dark { gap: 10px; }
.pbar .lock--dark .lock__mark { inline-size: 34px; block-size: 34px; padding: 3px; }
.pbar .lock__wm { font-size: 15px; letter-spacing: .115em; }
.pbar .lock__tm { font-size: .5em; }
```

Larghezza misurata dell'unità: **229,2 × 34 px** a 1440, 1280, 1024 e 768 **[m]**.

**Sotto 768 resta il solo tassello** (lacuna 11). `v2/shell.css` righe 187-189 fa oggi
`.lock__text { display: none }` sotto 23rem, che **distrugge il nome accessibile**: il wordmark è
l'unico testo del lock-up, `<img>` ha `alt=""`, e `brand_lockup` non emette `aria-label`. La
correzione non tocca `apps/cms/templatetags/cms_nav.py`:

```css
@media (max-width: 47.999rem) {
  .pbar .lock__text { position: absolute; inline-size: 1px; block-size: 1px;
                      overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
}
```

Specificità 0,2,0 contro 0,1,0 della regola di `shell.css`, e `platform-shell.css` carica dopo: vince
senza `!important`. Misurato a 390 e 360: il lock-up occupa **34 px** e il wordmark resta nell'albero
di accessibilità **[m]**.

**2. Filetto** `--hairline-dark-strong` 1 × 24 px (`#465359`, 2,202 sul fondo), nascosto sotto 768.

**3. La targa di contesto** `.pbar__plate` — non più testo, una targa: fondo `--mid-2`, bordo 1 px
`--hairline-dark-strong`, raggio `--radius-control` (2), altezza 32 (**44 su `(pointer: coarse)`**),
`padding-inline: 10px`; etichetta `--t-caption` mono `--on-dark-3` (5,846), valore `--t-folio` mono
`--on-dark` (14,079) con `font-variant-numeric: tabular-nums slashed-zero` e
`text-overflow: ellipsis`. Per un ruolo operativo è un `<button>` che apre la palette precaricata su
quel riferimento; per la persona uno `<span>`. **Il riferimento sparisce dalla banda** (difetto 11 +
deroga A3). Sotto 768 l'etichetta «Dossier» diventa `.visually-hidden` e la targa misura **110,4 ×
44** **[m]**.

> **Non c'è nessuna copia negli appunti.** La voce di moto `shell.plate.copy` del round 1 è
> eliminata: il suo innesco contraddiceva la definizione della targa per entrambi i ruoli, e per la
> persona sarebbe stato un affordance solo da puntatore, senza via da tastiera (violazione 7).

**4. Innesco della palette** `.pbar__cmd`, **solo ruoli operativi** (`{% if shell_operational %}`,
§ 4.9): fondo `--mid-2`, glifo `search` 16, etichetta «Rechercher» `--t-ui` `--on-dark-2`, e la
legenda dei tasti.

> **Niente chip `⌘K`** (cheap 2). La legenda non è un tasto disegnato: è **stampata**, in mono, come
> un folio — `--t-folio`, `--track-folio`, `--on-dark-3`, separata da un filetto verticale, senza
> fondo, senza bordo, senza raggio. Il tasto di plastica è la parte a buon mercato; la scorciatoia
> no. In un registro una scorciatoia si scrive, non si modella.
> ```css
> .pbar__cmd-keys { font-family: var(--f-mono); font-size: var(--t-folio);
>   letter-spacing: var(--track-folio); color: var(--on-dark-3);
>   padding-inline-start: var(--s-3); border-inline-start: 1px solid var(--hairline-dark-strong); }
> @media (max-width: 63.999rem) { .pbar__cmd-keys { display: none; }
>   .pbar__cmd { inline-size: 44px; padding-inline: 0; justify-content: center; }
>   .pbar__cmd-label { position: absolute; inline-size: 1px; block-size: 1px;
>     overflow: hidden; clip-path: inset(50%); white-space: nowrap; } }
> ```
> `shell-portal.js` riscrive `Ctrl K` in `⌘ K` su piattaforme Apple (compito 5). Misurato: innesco
> **200,5 × 32** a 1440, **44 × 44** a 768 e sotto **[m]**.

**5. Account** — `<details class="pbar__menu" data-dropdown>` nativo.
**Nessun monogramma** (cheap 3): il sommario porta il nome breve in `--t-ui` `--on-dark` e sotto di
esso l'etichetta di ruolo in `--t-caption` mono maiuscolo `--on-dark-3` — due righe, 16 + 14, dentro
32 px. Un'identità istituzionale si dichiara con il ruolo, non con due iniziali in un cerchio.
Pannello livello 3: `--mid-4`, 1 px `--hairline-dark-strong`, **280 px**, `--shadow-3` (deroga A1),
voci ≥ 44 px (48 su `(pointer: coarse)`), con Profil, Sécurité, **«Site public ↗»** (spostato qui:
non è un'azione primaria di uno spazio di lavoro), separatore, Se déconnecter.

> **Il logout resta un form POST.** `templates/components/account_menu.html` contiene
> `<form method="post" action="{{ logout_url }}">{% csrf_token %}<button type="submit">`. La
> riscrittura è **di solo CSS**: il pannello stila `.pbar__panel a` **e** `.pbar__panel button` con
> la stessa regola. Trasformare quel bottone in un `<a>` romperebbe il logout e toglierebbe il
> token CSRF; non si fa, e il test che lo impedisce è al § 4.8.

Sotto 768 nome e ruolo diventano `.visually-hidden` e il sommario è un bersaglio da **44 × 44**
con il solo glifo `user` **[m]**.

**6. Lingua** — `<details class="pbar__lang" data-dropdown>`. **Resta guidato dai dati**
(cheap 6): il template attuale cicla `site.languages` e rende `{{ l.name }}` con `lang`, `hreflang`,
`dir` e `aria-current`; **questo non cambia**. La «ع» del round 1 era una scorciatoia da disegnatore
che sostituiva «العربية» con una lettera e codificava quattro lingue su una lista di database: è
ritirata. L'unica aggiunta è un codice in mono accanto al nome, `{{ l.code|upper }}`, che sotto 768
resta da solo (il glifo `globe` si nasconde) dentro un bersaglio da 44 × 44 **[m]**.

**Lo sfondo che il committente non ha trovato memorabile.** Al margine finale la barra porta un
**frammento di graticola** 320 × 56 — lo stesso sistema cartografico dell'hero, ritagliato — in
`--terr-line`, `aria-hidden`, SVG inline ≈ 1,1 KB, una sola ripittura, `display: none` in
`forced-colors`, `scaleX(-1)` in RTL, con
`mask-image: linear-gradient(to inline-start, #000 0 34%, transparent 86%)` perché non passi mai
sotto un testo.

> **L'opacità non è più una supposizione** (cheap 4). Ho reso il frammento a cinque opacità su
> `--mid-1`, fotografato e letto i pixel:
>
> | opacità | pixel della linea | rapporto con il fondo |
> |---:|---|---:|
> | 8 % | `#122326` … `#12262e` | **1,119** |
> | 14 % | `#152f37` | 1,245 |
> | 18 % | `#16343c` | 1,326 |
> | **22 %** | `#183942` | **1,419** |
> | 30 % | `#1c454d` | 1,674 |
>
> La soglia fissata al § 4.1 è **1,365** — il filetto informativo del sistema. **L'8 % del round 1
> misura 1,119 e sta sotto la soglia: il revisore aveva ragione, era un'idea che nessuno avrebbe
> visto.** Si adotta **22 %**, misurato 1,419. (Lettura fatta senza maschera: la maschera può solo
> abbassare il valore verso l'interno, quindi 1,419 è il valore al margine finale, dove la grafica è
> più forte, ed è lì che la soglia deve valere.)

Stato `.pbar[data-scrolled]`: fondo `--mid-1` → `--mid-0` (salto di terreno 1,055) e filetto
inferiore `--hairline-dark-strong` → `--accent-dark`. **Nessuna ombra e nessuna transizione di
`box-shadow`** — vietata sia dalla deroga A1 sia dal vincolo di prestazione.

### 4.3 Regione 2 — la banda (`--min-1`)

`templates/portal/partials/case_header.html` **non viene riscritto: viene diviso.** La banda è un
**telaio**, e dentro il telaio ci sono due cose che esistono già.

```
.pband                          background --min-1; border-block-end 1px --hairline; overflow clip
 .pband__inner                  container; padding-block var(--s-4) var(--s-6)
  .pband__crumbs                riga 1 — components/breadcrumbs.html, invariato, 28 px [m]
  .pband__head                  riga 2 — flex, align-items: flex-end, gap var(--s-6)
   {% block portal_header %}      ← components/page_header.html, INVARIATO
   .pband__actions                margin-inline-start:auto — {% block page_actions %}, UNA azione
  {% if case %} portal/partials/case_facts.html {% endif %}   riga 3
```

**Che cosa rende la banda fuori dal fascicolo** (lacuna 1, MUST-FIX 3). La banda è resa
**sempre**, non `{% if case %}`. Dentro la riga 2 c'è il blocco `portal_header`, che oggi porta già
`components/page_header.html` (o `companies/partials/company_header.html`) su **39 dei 51 template
della famiglia del portale** — contati aprendo la catena `{% extends %}` di ogni template. Altri tre
sono basi intermedie senza titolo proprio (`academy/base_academy.html`,
`forum/governance/base_governance.html`, `helpdesk/base_helpdesk.html`): il titolo lo danno i loro
figli, e non richiedono alcuna modifica. Restano **nove** da migrare (§ 4.8 n. 14). Quel componente
**non si tocca**: `eyebrow`, `lead`, `meta`, `lang` e `align` continuano a esistere e a essere resi.
La banda si limita a neutralizzare il `.container` e a ridare al titolo la scala giusta:

```css
.pband .page-header { max-inline-size: none; margin: 0; padding: 0; }
.pband .page-header__title { font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-title); line-height: var(--t-title-lh);   /* 48/52 */
  letter-spacing: var(--track-display); color: var(--ink); margin: 0; }
@media (max-width: 74.999rem) {
  .pband .page-header__title { font-size: var(--t-band); line-height: var(--t-band-lh); } /* 32/36 */
}
.pband .page-header__eyebrow { font-family: var(--f-mono); font-size: var(--t-folio);
  letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--ink-3);
  margin: 0 0 var(--s-2); }
.pband .page-header__lead { font-family: var(--f-serif); font-style: italic;
  font-size: var(--t-lead); line-height: var(--t-lead-lh); color: var(--ink-2);
  max-inline-size: 62ch; margin: var(--s-3) 0 0; }
.pband__crumbs.breadcrumbs { padding: 0; margin: 0; min-block-size: 28px; max-inline-size: none;
  font-size: var(--t-caption); line-height: var(--t-caption-lh); }
@media (max-width: 47.999rem) { .pband__head { display: grid; gap: var(--s-3); }
  .pband__actions { margin-inline-start: 0; } .pband__actions .btn { inline-size: 100%; } }
```

Così **non esistono due sistemi di titolo**: il difetto 10 è chiuso (48/52 e 32/36, entrambi nella
scala degli undici corpi, entrambi con interlinea maggiore del corpo) e nessuna pagina perde il
proprio `<h1>`. Misurato: titolo **610,4 × 52** a 1440, **406,9 × 36** a 1024 e 768, **350 × 36** a
390 **[m]** — non più le due righe schiacciate che il round 1 produceva perché l'azione primaria
comprimeva il titolo.

Restano **nove** template della famiglia il cui `<h1>` sta dentro `portal_content` invece che nel
blocco: la banda per loro mostra briciole + azione e il titolo resta più in basso. Vanno migrati, e
l'elenco è finito (§ 4.8 n. 14).

#### I fatti del fascicolo — `portal/partials/case_facts.html` (nuovo)

Contratto identico a quello che `case_header.html` ha oggi: `case`, `responsible` (precaricato dalla
vista), `progress`. **Nessuna vista cambia. Nessuna parola cambia.** Le quattro cose che il round 1
lasciava cadere (violazione 5, MUST-FIX 2) hanno ciascuna il proprio posto:

```html
<dl class="pband__facts">
  <div class="pband__fact"><dt>{% translate "Objectif" %}</dt>
    <dd>{{ case.get_purpose_display }}</dd></div>

  <div class="pband__fact pband__fact--state"><dt>{% translate "État" %}</dt>
    <dd><span class="pstate pstate--{{ family }}">{% svg_icon glyph "icon icon--sm" %}
          <span>{{ case.get_status_display }}</span></span>
        <span class="pband__since">{% blocktranslate with date=case.status_since|date:"d.m.Y" %}depuis le {{ date }}{% endblocktranslate %}</span>
    </dd></div>

  <div class="pband__fact"><dt>{% translate "Responsable" %}</dt>
    <dd>{% if responsible %}
      <ul class="pband__actors">{% for a in responsible %}
        <li><span class="pweave pweave--{{ a.role|lookup:OWNER_WEAVE }}" aria-hidden="true"></span>
            {% svg_icon a.role|lookup:OWNER_GLYPH "icon icon--sm" %}
            {{ a.get_role_display }}{% if a.organisation %} — {{ a.organisation.name }}{% endif %}</li>
      {% endfor %}</ul>
    {% else %}{% translate "Vous — aucun intervenant n’est assigné à ce dossier" %}{% endif %}</dd></div>

  {% if progress %}
  <div class="pband__fact"><dt>{% translate "Avancement" %}</dt>
    <dd><span class="ptally" aria-hidden="true">…cinque <i>…</i></span>
        <span>{% blocktranslate with done=progress.done total=progress.total %}{{ done }} sur {{ total }} éléments complétés{% endblocktranslate %}</span>
        {% if progress.overdue %}<span class="pstate pstate--late">{% svg_icon "warning" "icon icon--sm" %}
          <span>{% blocktranslate count n=progress.overdue %}{{ n }} en retard{% plural %}{{ n }} en retard{% endblocktranslate %}</span></span>{% endif %}
    </dd></div>{% endif %}
</dl>

{% if case.suspension_reason %}
<p class="pband__suspension" role="status">
  <span class="pband__susp-head">{% translate "Dossier suspendu" %}</span>
  <span>{{ case.suspension_reason }}</span></p>
{% endif %}
```

1. **`case.suspension_reason`** — stato giuridico del fascicolo, quindi non negoziabile. Blocco a
   tutta larghezza sotto i fatti, fondo `--min-3`, bordo iniziale 3 px `--pending-700`, testata
   «Dossier suspendu» in mono `--pending-700` (**6,984** su `--min-3`), `role="status"`.
2. **`status_since`** — `.pband__since`, `--ink-3`, accanto alla pillola, stringa `blocktranslate`
   invariata.
3. **`progress.overdue`** — pillola `--err-700` (**6,536**) con glifo `warning` **e** la parola.
4. **`responsible` multi-attore** — `<ul>` con `get_role_display` + `organisation.name`, e la frase
   di ripiego «Vous — aucun intervenant n'est assigné à ce dossier» **verbatim**. Il § 9.3 chiede
   «due trame affiancate» per il multi-attore: ogni voce porta il proprio `.pweave` da 10 px con la
   trama del responsabile (pieno = persona · hachures 45° = équipe · punti = formazione · linee =
   autorità · tratteggio = territorio), rese in `repeating-linear-gradient` sui token
   `--owner-*`; due voci = due trame l'una sotto l'altra, in colonna, che è l'affiancamento che una
   colonna da 290 px consente.

```css
.pweave { inline-size: 10px; block-size: 14px; flex: none; }
.pweave--person     { background: var(--owner-person); }
.pweave--project    { background: repeating-linear-gradient(45deg, var(--owner-project) 0 2px, transparent 2px 4px); }
.pweave--training   { background: radial-gradient(var(--owner-training) 1px, transparent 1.2px) 0 0/4px 4px; }
.pweave--authority  { background: repeating-linear-gradient(to bottom, var(--owner-authority) 0 1px, transparent 1px 3px); }
.pweave--territory  { background: repeating-linear-gradient(to bottom, var(--owner-territory) 0 2px, transparent 2px 5px); }
@media (forced-colors: active) { .pweave { forced-color-adjust: none; } }
```

**La pillola di stato** — `.pstate`, glifo + parola + forma + colore, mai il colore da solo. La
famiglia **non** viene dal set legacy `--state-*-fg`: quella famiglia è `#1e4a85` e `#5f84b5`, cioè
esattamente il secondo blu strutturale del difetto 9. Mappa esaustiva sui **undici** stati di
`cases.models.CaseStatus`, come `dict` letterale in `apps/portal/templatetags/portal_shell.py`
(§ 4.3-bis) — nessuna vista toccata:

| famiglia | stati | glifo | colore su `--min-3` |
|---|---|---|---:|
| `--done` | `entered`, `post_entry`, `closed` | `check` | `--ok-700` 5,322 |
| `--work` | `draft`, `oriented`, `training`, `selection`, `admin_process`, `pre_departure` | `clock` | `--ink-2` 7,167 |
| `--wait` | `review_required` | `person` | `--pending-700` 6,984 |
| `--halt` | `suspended` | `minus` | `--pending-700` 6,984 |
| `--late` | (non è uno stato: è `progress.overdue`) | `warning` | `--err-700` 6,536 |

Tutti i glifi esistono in `static/img/icons.svg`; nessun asset nuovo qui.

#### 4.3-bis Le tre mappe — `apps/portal/templatetags/portal_shell.py` (nuovo)

Un template Django non sa risolvere `dict[variabile]`, quindi le mappe del rail, della pillola e
delle trame vivono in **un** modulo di tag con **un** filtro. È presentazione pura: non tocca una
vista, non tocca un permesso, non tocca una parola.

```python
"""Presentation maps for the platform shell. No view, no permission, no wording."""
from django import template
register = template.Library()

RAIL_GLYPH = {"dashboard": "compass", "situation": "person", "cases": "briefcase",
              "requests": "list", "pathways": "map-pin", "documents": "document",
              "deadlines": "calendar", "messages": "mail", "academy": "university",
              "helpdesk": "handshake", "selection": "check", "company": "building",
              "helpdesk-queue": "handshake"}

STATE_FAMILY = {"entered": "done", "post_entry": "done", "closed": "done",
                "draft": "work", "oriented": "work", "training": "work", "selection": "work",
                "admin_process": "work", "pre_departure": "work",
                "review_required": "wait", "suspended": "halt"}
STATE_GLYPH = {"done": "check", "work": "clock", "wait": "person",
               "halt": "minus", "late": "warning"}

OWNER_WEAVE = {"role:person": "person", "role:professional": "project",
               "role:training_provider": "training", "role:university": "training",
               "role:authorised_actor": "authority", "role:institution": "authority",
               "role:company": "territory"}
OWNER_GLYPH = {"person": "person", "project": "briefcase", "training": "university",
               "authority": "shield", "territory": "building"}

@register.filter
def lookup(key, mapping):
    """`{{ item.key|lookup:RAIL_GLYPH }}` — a missing key renders nothing, never a broken glyph."""
    return mapping.get(key, "")
```

Le mappe si espongono ai template con `{% load portal_shell %}` e un
`{% with RAIL_GLYPH=... %}`; in pratica i tre partial le prendono da un `simple_tag`
`{% shell_maps as maps %}` che torna il modulo come `dict`. **Una chiave assente non rende nulla**:
il giorno in cui `services.navigation` aggiunge una voce, la riga compare senza glifo invece di
rompersi, e la mappa si aggiorna in un posto solo.

**Il misuratore** (violazione 3, cheap 7). Il § 9.1 e il § 6 impongono un «misuratore a tacche»: è
vincolante. Quello che non è vincolante è disegnarlo come la barra segmentata di ogni kit da
cruscotto. Sono **cinque tacche verticali 2 × 14 px, passo 6**, allineate alla cadenza del mono —
tacche di registro, non segmenti di progresso:

```css
.ptally { display: inline-flex; align-items: center; gap: 6px; vertical-align: -2px;
          margin-inline-end: var(--s-3); }
.ptally i { display: block; inline-size: 2px; block-size: 14px; background: var(--hairline-strong); }
.ptally i[data-on] { inline-size: 3px; background: var(--ink-2); }
```

**`--accent` non compare.** Le tacche piene sono `--ink-2` (6,004 su `--min-1`), le vuote
`--hairline-strong` (3,136), e la differenza è anche **di forma** — 3 px contro 2 — perché il colore
non basta mai da solo. Il conteggio letterale accompagna **sempre** le tacche
(«2 sur 9 éléments complétés») e le tacche sono `aria-hidden`: illustrano il numero, non lo
sostituiscono. Senza `progress` il misuratore non si disegna.

**La banda territoriale** (deroga A2). Al margine finale,
`templates/portal/partials/territory_band_base.svg` — già nel repo — ritagliato all'altezza della
banda, in `--terr-line-lt`, mascherato come la graticola. Opacità **30 %**, misurata sui pixel:
linea `#a8c3c2` su fondo `#ecebe6`, rapporto **1,564** **[m]** — sopra la soglia di 1,365. A 22 %
misurava 1,376, appena sopra; si sceglie 30 % perché su carta il margine è più stretto che su
mezzanotte.

**Altezza della banda, misurata** — il round 1 prometteva «≈ 168 px» senza misurarlo, e non era
vero. Questi sono i valori reali **[m]**:

| larghezza | pagina senza fascicolo | fascicolo, nessuna sospensione | fascicolo sospeso |
|---|---:|---:|---:|
| 1440 | **154** | 294 | **340** |
| 1280 | 154 | 314 | 360 |
| 1024 | 138 | 318 | 364 |
| 768 | 138 | 345 | 391 |
| 390 | **182** | 270 | **356** |
| 360 | 182 | 270 | 376 |

Ogni cella è misurata, non dedotta: tre rese per larghezza (senza `case`, con `case` e senza
`suspension_reason`, con entrambi), sei larghezze, diciotto misure.

Le tre fasce di oggi (60 + 133 + 117 = **310 px**) portavano quattro fatti, nessun titolo in scala e
nessuna azione. La banda porta gli stessi quattro fatti, il titolo a 48/52, l'azione primaria,
la sospensione e la banda territoriale, e su una pagina qualunque — cioè la maggioranza — costa
**154 px a 1440 e 138 px a 1024**: meno della metà. Sul fascicolo più carico che il modello possa
produrre — due intervenienti con l'organismo, tre elementi in ritardo, una sospensione motivata —
costa **340 px**, cioè 30 px più delle tre fasce di oggi, e porta cinque cose in più.

Sotto 768 la banda tiene **identità e stato giuridico** — briciole, titolo, azione, `État` con la
data, e la sospensione — e i tre fatti di riferimento (`Objectif`, `Responsable`, `Avancement`)
scendono in testa alla colonna come prima sezione del registro, «Le dossier». Non sono nascosti,
non sono in un `<details>`, non perdono una parola: sono spostati di 40 px. È ciò che porta la prima
riga dello spazio di lavoro a **`y = 409`** sul fascicolo sospeso e a **`y = 235`** su una pagina
qualunque, contro `y = 843` di oggi **[m]**.

### 4.4 Regione 3 — lo spazio di lavoro: **«il registro aperto»**

> Questa sezione è la risposta a MUST-FIX 10 e ai segnali 1 e 5. Il round 1 arricchiva il cromo e
> lasciava la stanza vuota: `--min-0` con dei fogli sopra. Quattro mosse, tutte misurate, nessuna
> ombra, nessuna immagine, nessun byte di rete.

```css
.pshell { display: grid;
  grid-template-columns: var(--shell-rail) minmax(0,1fr) var(--shell-inspector);
  column-gap: var(--s-8); align-items: stretch;
  max-inline-size: var(--container); margin-inline: auto; padding-inline: var(--grid-margin);
  background-image: repeating-linear-gradient(to bottom,
      var(--hairline) 0 1px, transparent 1px var(--shell-rule)); }
.pshell[data-rail="collapsed"] { --shell-rail: var(--shell-rail-collapsed); }
@media (max-width: 74.999rem) { .pshell { grid-template-columns: var(--shell-rail) minmax(0,1fr); } }
@media (max-width: 63.999rem) { .pshell { grid-template-columns: minmax(0,1fr); background-image: none; } }
```

**Nessun figlio dichiara `grid-column` nell'intervallo a tre colonne.** Il round 1 lo faceva; in
browser, alla prima riduzione a una colonna, `grid-column: 2` e `3` creavano **colonne implicite** e
la griglia si rompeva — a 768 il rail misurava 0 px di larghezza e l'inspector 42 **[m]**. Sotto
1200 l'inspector prende `grid-column: 1 / -1`; sotto 1024 lo prende anche il dorso. Nient'altro.

**Mossa 1 — tre terreni, e la profondità viene da lì.** `--min-0` tela · `--min-1` area (dorso del
rail, inspector, banda) · `--min-2` foglio (colonna centrale). Ogni confine è un filetto
`--hairline` da 1 px. È la riga del § 12 del design system — «scala di superfici, non ombre», contro
«Material elevation ovunque» — applicata alla lettera, ed è ciò che rende la deroga A1 un costo
accettabile invece di una rinuncia. Salti misurati: `--min-1`/`--min-0` **1,076**,
`--min-2`/`--min-1` **1,144**, `--min-2`/`--min-0` **1,064**.

**Mossa 2 — il dorso.** Il fondo del rail non è il rail: è una **colonna della griglia** che corre
per tutta l'altezza del documento, e il rail appiccicoso ci galleggia dentro.

```css
.prail-col { background: var(--min-1); border-inline-end: 1px solid var(--hairline); }
.prail { position: sticky; inset-block-start: var(--shell-bar-h);
  max-block-size: calc(100vh - var(--shell-bar-h));
  max-block-size: calc(100dvh - var(--shell-bar-h));
  overflow-y: auto; overscroll-behavior: contain;
  display: flex; flex-direction: column; }
```

Questo chiude la **lacuna 7**. Il round 1 dava al rail `block-size: calc(100dvh - var(--shell-bar-h))`
— un'altezza **fissa** su un elemento appiccicoso la cui origine naturale sta ~168 px sotto la barra:
a scroll 0 sbordava dal viewport esattamente dell'altezza della banda. Con `max-block-size` il rail è
alto quanto il suo contenuto e non sborda mai; con `align-items: stretch` il **dorso** arriva in
fondo alla pagina, che è ciò che si voleva davvero. E poiché `.prail-col` è un elemento di griglia,
la riga è alta almeno quanto il rail: su una pagina corta non c'è nulla da traboccare. Misurato a
1440: dorso **224 × 645**, rail **223 × 645**, nessuno sbordo **[m]**.

**Mossa 3 — la rigatura.** La tela porta una rigatura di 1 px ogni **28 px**, che è l'interlinea del
corpo (17/28): la scrivania e il testo battono lo stesso tempo. È `--hairline` su `--min-0`, cioè
rapporto **1,365** letto sui pixel **[m]** — non una texture inventata, il filetto che il sistema
già usa. Si vede **solo** nei margini di pagina (40 px per lato) e nelle due gole fra le colonne
(32 px l'una): **144 px di un viewport da 1440**, da cima a fondo, dietro i fogli. Mai sotto un
testo, perché sotto il testo c'è un foglio opaco. Sparisce sotto 1024, dove non ci sono gole, e in
`forced-colors`.

**Mossa 4 — il margine del registro.** La colonna centrale non è una pila di schede: è **un registro
continuo** con un margine permanente da 56 px, chiuso da un filetto che corre per tutta l'altezza
della colonna. Nel margine stanno gli ordinali dei folii — che `register.css` genera già con
`counter()` e che ogni sezione del portale emette già come `<span class="folio__ordinal">`.

```css
.pcol { background: var(--min-2);
  border-inline: 1px solid var(--hairline); border-block-end: 1px solid var(--hairline);
  padding-inline: var(--shell-margin) var(--s-8); padding-block: var(--s-8) var(--s-12);
  position: relative; align-self: start; min-inline-size: 0; }
.pcol::before { content: ""; position: absolute; inset-block: 0;
  inset-inline-start: calc(var(--shell-margin) - 1px); inline-size: 1px; background: var(--hairline); }
.pcol .folio__ordinal { position: absolute; inline-size: calc(var(--shell-margin) - var(--s-3));
  inset-inline-start: calc(-1 * var(--shell-margin)); text-align: end; }
.pcol :where(p, li, dd, blockquote) { max-inline-size: 62ch; }
@media (max-width: 63.999rem) { .pcol { padding-inline-start: var(--s-8); }
  .pcol::before { content: none; }
  .pcol .folio__ordinal { position: static; inline-size: auto; text-align: start; } }
```

**È questa la geometria che non è Linear** (cheap 1). Un rail a glifi e una barra scura li ha
chiunque; una colonna di lavoro con un margine di registro numerato che corre per 4 000 px, no —
quella è la grammatica del progetto, non un'etichetta appiccicata a uno scheletro altrui.

> **62ch, non 65ch, e il motivo è un numero.** Il § 3.2 dice «misura ≤ 75 caratteri
> (`max-inline-size: 65ch`)». Misurato in browser: in Fira Sans a 17 px l'avanzamento di `0` (cioè
> `1ch`) è **9,35 px** mentre il carattere minuscolo medio è **7,849 px**, quindi 65ch = 607,8 px =
> **77,4 caratteri medi** — sopra il limite che la stessa riga fissa. A 62ch la colonna misura
> **74,9 caratteri** a 1024 e **69,1** a 1440 **[m]**. In arabo, Noto Naskh a 17/1,8: **58,1** **[m]**.

**Il rail** — `templates/portal/partials/rail.html` (nuovo), consuma `portal_nav` così com'è.

- Riga: `display: grid; grid-template-columns: 20px minmax(0,1fr) auto; gap: var(--s-3);
  min-block-size: var(--shell-row-h); padding-inline: var(--s-4) var(--s-3); color: var(--ink-2)`
  (6,004). Misurata **223 × 40** a 1440 e **× 44** su puntatore grossolano **[m]**; l'etichetta più
  lunga («Demandes qui me sont confiées») va a capo in due righe da 20 e la riga resta **40**.
- **Glifo per voce**, dal `key` stabile che `portal.services.navigation()` già espone; tutti e
  tredici i simboli esistono oggi in `static/img/icons.svg` — verificato per id —, **nessun asset
  nuovo**: `dashboard→compass · situation→person · cases→briefcase · requests→list ·
  pathways→map-pin · documents→document · deadlines→calendar · messages→mail · academy→university ·
  helpdesk→handshake · selection→check · company→building · helpdesk-queue→handshake`. La mappa è un
  `dict` `RAIL_GLYPH` del § 4.3-bis: nessuna vista toccata.
- **Trama del rail**: tre filetti da 1 px (passo 6) al margine iniziale di ogni riga, `--hairline`,
  resi su `::before` con tre `linear-gradient`. Texture a costo zero, e in `forced-colors`
  `forced-color-adjust: none` la conserva.
- **Voce corrente**: `aria-current="page"`, fondo `--min-2`, testo `--ink` 500, barra `--accent`
  3 px al margine iniziale (`inset-block: 8px`), più il testo nascosto «page actuelle». Il colore
  non è mai solo: fondo + barra + peso + `aria-current` + parola.
- **Conteggio**: terza colonna riservata a `{{ item.count }}`, resa solo se la chiave esiste —
  `--min-3`, 1 px `--hairline`, `--t-caption` mono tabulare, con `<span class="visually-hidden">non
  lus</span>`. Oggi `portal_nav` non porta `count` e il conteggio resta cucito nell'etichetta
  (difetto 5): **lo slot resta vuoto, nessuna vista cambia oggi**, e il giorno in cui
  `services.navigation` aggiunge `count` il badge appare senza altro lavoro.
- **Piede del rail**: **nome + etichetta di ruolo** (da `shell_role_label`, § 4.9) e la riga legale
  in `--t-caption` `--ink-3`. **Nessun monogramma** (cheap 3).
- **Rail compresso** (64 px), reso **solo** per i ruoli operativi (`{% if shell_operational %}`):
  `<button class="prail__toggle" aria-expanded aria-controls="prail">`; `shell-portal.js` commuta
  `data-rail` su `.pshell` e lo ricorda in `localStorage`. Senza JS il rail resta esteso. Da
  compresso: solo glifo centrato, `aria-label` **e** `title` con l'etichetta intera (pattern 21st
  #1). **Il suggerimento è il `title` nativo**: il round 1 inventava un «suggerimento di livello 3»,
  cioè un componente nuovo con un'ombra su una pagina DENSE, per un problema che l'attributo nativo
  risolve con il ritardo, la posizione e il comportamento del sistema operativo. Per la **persona**
  la navigazione resta sempre piena — decisione del Council.
- **Sotto 1024** la `<ul>` diventa striscia orizzontale: `display: flex; overflow-x: auto;
  scroll-snap-type: inline mandatory;` altezza **44 px** (deroga A4), chip glifo + etichetta +
  eventuale conteggio su **tre** colonne — il round 1 ne dichiarava due e il conteggio finiva in una
  riga implicita, portando due chip a 52 px **[m]** —, `scroll-snap-align: start`, bordi sfumati con
  `mask-image` per dire che continua. Misurato: tutte le righe **44**, il chip più largo **321 px**,
  e **nessuno scorrimento orizzontale di pagina** a 360, 390 e 768 **[m]**.

**L'inspector** — `templates/portal/partials/inspector.html` (nuovo) con `{% block portal_inspector %}`.

- **Livello 1, non livello 3**: `--min-1`, 1 px `--hairline`, raggio 0, **nessuna ombra**
  (deroga A1). Si stacca dalla tela per terreno (1,076) e dal foglio centrale per terreno (1,144) e
  per filetto. `position: sticky; inset-block-start: calc(var(--shell-bar-h) + var(--s-6));
  max-block-size: calc(100dvh - var(--shell-bar-h) - var(--s-12)); overflow-y: auto;
  overscroll-behavior: contain;`
- Sezioni: `--t-folio` maiuscolo `--ink-3` con filetto inferiore, corpo `--t-small`. Contenuto già
  presente nel contesto di `dashboard.html`: **pré-évaluation** (con la frase «Prochaines étapes à
  caractère informatif…» **sempre presente**), **messages**, **échéances**, **compte**. Spostarle qui
  è un cambio di *template*, non di vista.
- Stato vuoto: filetto, glifo **arco + gradini** (`icon-arch`, nuovo simbolo nello sprite, ≈ 340 B),
  una frase che dice *chi* riempie la regione e *quando*, azione inline.
- Sotto 1200 l'inspector **non sparisce**: `grid-column: 1 / -1`, `position: static`,
  `columns: 2` — misurato 944 × 180 a 1024 **[m]** —, una colonna sotto 768. Non è mai modale.
- **Nessun `content-visibility`** (lacuna 8): quattro sezioni corte non giustificano il salto di
  barra di scorrimento che `content-visibility: auto` senza `contain-intrinsic-size` produce, e con
  `contain-intrinsic-size` rompe l'aritmetica di `max-block-size`. Rimosso.

### 4.5 Il prochaine étape

`templates/portal/partials/next_action.html` esce dal cromo ed entra nella colonna centrale come
**primo foglio del registro**, prima di ogni sezione: markup invariato salvo la rimozione di
`.container` (dentro `.pcol` il contenitore è già lì). Conserva il bordo iniziale `--accent` 3 px del
§ 9.2, il titolo `--t-entry` serif, il responsabile con glifo a sigillo (anello `--seal-600`, 3,995
su `--min-1`, non testuale) e la frase «Cette étape ne dépend pas de vous». **Il secondo blu del
difetto 9 sparisce con `--state-info-br`**: il bordo è `--accent`, l'unico accento.

### 4.6 Stati — tre componenti, tre tabelle

Il round 1 applicava una sola griglia rest/hover/focus/active/current/disabled/loading/error a tre
componenti che non hanno quegli stati: «loading: scheletro fermo» per una **riga di rail** resa dal
server insieme alla pagina era una cella riempita per completare una matrice (cheap 8). Qui ogni
componente ha gli stati che ha.

**Riga del rail** — cinque stati.

| Stato | Che cosa cambia |
|---|---|
| rest | `--ink-2` su `--min-1` |
| hover (`@media (hover: hover)`) | evidenziatore unico `--min-2` (§ 5.2), testo `--ink` |
| focus-visible | `outline: 2px solid var(--accent-ring); outline-offset: 2px; box-shadow: 0 0 0 5px color-mix(in srgb, var(--accent-ring) 30%, transparent)` |
| active | `translateY(1px)`, 120 ms |
| current | barra `--accent` 3 px + fondo `--min-2` + peso 500 + `aria-current="page"` + testo nascosto |

Non ha `disabled` (una voce non disponibile non si rende: `ROLE_SURFACES` la omette), non ha
`loading`, non ha `error`.

**Controlli della barra** (targa, innesco, sommari) — cinque stati.

| Stato | Che cosa cambia |
|---|---|
| rest | `--on-dark-2` su `--mid-2`, bordo `--hairline-dark-strong` |
| hover | fondo `--mid-3`, testo `--on-dark` |
| focus-visible | `outline: 2px solid var(--accent-dark); outline-offset: 2px; box-shadow: 0 0 0 5px color-mix(in srgb, var(--accent-dark) 30%, transparent)` |
| active | `translateY(1px)`, 120 ms |
| expanded (`<details[open]>`) | il chevron ruota di 180° (`transform`, 240 ms), `aria-expanded="true"` sul sommario |

**Palette** (`.pcmd`, radice `<dialog class="pcmd">` livello 5: `--min-2`, `--shadow-5` e scrim,
deroga A1) — cinque stati, e sono **suoi**: rest (campo vuoto, sezioni «recenti»), loading
(scheletro di livello 1 **fermo**, `aria-busy="true"`, annuncio `aria-live="polite"` al termine),
results (conteggio in `aria-live="polite"`), empty («Aucun résultat» + suggerimento), error
(`--err-700` + glifo `warning` + parola, `role="alert"`).

**Ripiego per `color-mix`** (lacuna 12). L'alone non è più il letterale `rgb(29 138 147 / .30)` del
round 1, che era `--accent-ring` codificato a mano. `color-mix(in srgb, …)` è disponibile ovunque
dal 2023; dove non lo è, l'anello resta visibile senza alone:

```css
@supports not (color: color-mix(in srgb, red, blue)) {
  .prail__link:focus-visible, .pbar__plate:focus-visible, .pbar__cmd:focus-visible,
  .pbar__menu > summary:focus-visible, .pbar__lang > summary:focus-visible {
    box-shadow: none; outline-width: 3px; }
}
```

### 4.7 Lo skip link

`base.html` ha già `<a class="skip-link" href="#main-content">` come primo elemento del `<body>` e
`<main id="main-content" tabindex="-1">`. Il round 1 inventava «Aller au contenu» e `#contenu`, che
non esistono, e gli dava `--min-3` su `--accent-ring` = **4,110:1**, un fallimento AA sul primo
elemento focalizzabile di ogni pagina autenticata (violazione 2). Si riusa quello che c'è:

```css
.page-portal .skip-link { background: var(--accent); color: var(--min-0);
  border-radius: var(--radius-control); font-family: var(--f-sans);
  font-size: var(--t-ui); line-height: var(--t-ui-lh);
  min-block-size: 44px; display: inline-flex; align-items: center; }
.page-portal .skip-link:focus-visible { outline: 2px solid var(--on-dark);
  outline-offset: 2px; box-shadow: none; }
```

`--min-0` su `--accent` = **5,692:1** calcolato — ed è la coppia che il § 10 del design system fissa
per il bottone primario, quindi non si introduce una seconda convenzione. (`--min-3` su `--accent`
darebbe 6,316 e passerebbe anche; si sceglie `--min-0` per coerenza con il sistema.) `--accent-ring`
torna al ruolo che il suo commento in `tokens.css` gli assegna — «focus ring, UI strokes», un token
da 3:1 — e non regge più testo da nessuna parte.

Nota per l'implementatore: `static/css/base.css` riga 409 mette
`transition: transform … ` su `.skip-link` **fuori** da `@media (prefers-reduced-motion:
no-preference)`. È una violazione preesistente di `MOTION_SYSTEM` § 3; si corregge nello stesso
commit, spostando quella transizione dentro il blocco.

### 4.8 Template e file toccati — lista completa

| # | File | Che cosa succede |
|---|---|---|
| 1 | `templates/portal/base_portal.html` | riscritto: `<body data-mode>`, `{% block extra_head %}` (§ 4.10), la banda resa **sempre**, `.pshell`, `next_action` dentro `.pcol`, `{% block portal_inspector %}`. Il `{% block site_footer %}` **conserva `{{ site.contact_email }}`** accanto ai tre link legali (lacuna 3): il piè di pagina si riduce alla navigazione, non all'indirizzo di contatto — un'istituzione non toglie il proprio recapito dalla pagina |
| 2 | `templates/partials/portal_chrome.html` | riscritto in `.pbar` (§ 4.2) |
| 3 | `templates/portal/partials/case_header.html` | **eliminato**, dopo che il suo corpo è passato a `case_facts.html` |
| 4 | `templates/portal/partials/case_facts.html` | **nuovo** — i quattro fatti, verbatim, più la sospensione (§ 4.3) |
| 5 | `templates/portal/partials/rail.html` | **nuovo** |
| 6 | `templates/portal/partials/inspector.html` | **nuovo** |
| 7 | `templates/portal/partials/command_palette.html` | **nuovo**, solo ruoli operativi |
| 8 | `templates/portal/partials/next_action.html` | `.container` rimosso; nient'altro |
| 9 | `templates/components/page_header.html` | **invariato** — la banda lo stila, non lo sostituisce |
| 10 | `templates/components/breadcrumbs.html` | **invariato** — la banda lo stila con `.pband__crumbs` |
| 11 | `templates/components/account_menu.html` | solo classi: `.pbar__panel`. **Il `<form method="post">` con `{% csrf_token %}` e il `<button type="submit">` restano** (§ 4.2) |
| 12 | `templates/components/language_switcher.html` | solo classi + `{{ l.code\|upper }}`; il ciclo su `site.languages` resta |
| 13 | `templates/portal/dashboard.html` | quattro sezioni spostate in `{% block portal_inspector %}`; `data-mode="RICH"` |
| 14 | nove template con l'`<h1>` in `portal_content` | l'`<h1>` passa in `{% block portal_header %}` via `page_header.html`: `companies/need_detail.html`, `companies/need_form.html`, `companies/profile.html`, `documents/index.html`, `documents/requirement_detail.html`, `documents/terms_required.html`, `documents/upload.html`, `portal/documents.html`, `portal/situation.html`. In più `companies/profile_form.html`: il suo `<h1>` di riga 21 diventa `<h2>` (ne ha già uno nel blocco) |
| 15 | i sette template `RICH` e i tre `STANDARD` | sovrascrivono `{% block body_data %}` (§ 4.0) |
| 16 | `apps/portal/static/portal/portal.css` | **stesso commit**: si rimuovono i blocchi `.portal-bar*`, `.case-header*`, `.next-action*`, `.portal`/`.portal__aside`/`.portal__main` (rischio «due sistemi conviventi», § 8) |
| 17 | `apps/accounts/context_processors.py` | **nuovo** (§ 4.9) |
| 18 | `config/settings/base.py` | una riga dopo `core.context_processors.site` (riga 141) |
| 19 | `apps/portal/views.py` + `urls.py` | **una** vista nuova, `palette`, `login_required` + `never_cache` + `require_GET` + `_noindex`, che chiama solo `portal.services` / `cases.services` già filtrate per utente. Nessun permesso nuovo |
| 20 | `static/css/v3/tokens-shell.css`, `static/css/v3/platform-shell.css`, `static/js/src/shell-portal.js` | **nuovi** |
| 21 | `apps/portal/templatetags/portal_shell.py` | **nuovo** — le tre mappe e un filtro `lookup` (§ 4.3-bis) |
| 22 | `static/img/icons.svg` | `icon-arch` aggiunto (≈ 340 B). Nessun altro simbolo: i tredici del rail, i cinque della pillola e i cinque dei responsabili esistono già |
| 23 | `static/css/base.css` riga 409 | la `transition` dello `.skip-link` entra in `@media (prefers-reduced-motion: no-preference)` (§ 4.7) |

**Due test nuovi**, sul modello di `tests/frontend/test_v2_bridge_is_temporary.py`:
`test_v3_shell_has_no_twin.py` (in `portal.css` non restano selettori `.portal-bar`, `.case-header`,
`.next-action`, `.portal`) e `test_v3_logout_is_a_form.py` (in `components/account_menu.html`
l'azione di logout è un `<form method="post">` con `{% csrf_token %}` e un `<button type="submit">`,
mai un `<a>`).

### 4.9 Il predicato di ruolo (deroga A5)

`apps/accounts/context_processors.py`:

```python
"""Shell presentation only. This module GRANTS NOTHING: it reads the role catalogue so the
platform chrome can decide what to draw. Every view keeps its own permission check."""
from accounts import roles

#: The roles DESIGN_SYSTEM_V2 §9.1 names for the command palette and the collapsible rail:
#: « operatore / professionista / redattore / admin ». MODERATOR and STAFF are deliberately
#: NOT here — community moderation and the project team are not case-work roles, and adding
#: them would widen a binding clause instead of applying it.
SHELL_OPERATIONAL: tuple[str, ...] = (
    roles.OPERATOR,          # operatore
    roles.PROFESSIONAL,      # professionista
    roles.LEGAL_EDITOR,      # redattore
    roles.LEGAL_APPROVER,    # redattore
    roles.CONTENT_EDITOR,    # redattore
    roles.ADMINISTRATOR,     # admin
    roles.SUPERADMIN,        # admin
)

def shell(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {"shell_operational": False, "shell_role_label": ""}
    labels = roles.role_labels(user)
    return {
        "shell_operational": roles.has_role(user, *SHELL_OPERATIONAL),
        "shell_role_label": labels[0] if labels else "",
    }
```

`roles.has_role()` torna `True` per un `is_superuser`, ed è voluto: «admin» del § 9.1 comprende
l'amministrazione generale. `roles.role_labels()` torna **etichette tradotte**, mai il nome tecnico
del gruppo («role:operator» non compare in nessuna pagina: il modulo lo vieta).

In `config/settings/base.py`, riga 142:

```python
"core.context_processors.site",
"accounts.context_processors.shell",
```

Nei template: `{% if shell_operational %}` per l'innesco della palette (§ 4.2 n. 4) e per il toggle
del rail (§ 4.4). `{{ shell_role_label }}` nel sommario account e nel piede del rail.

**La palette non amplia nulla.** Interroga la vista `portal:palette`, che chiama
`portal.services` / `cases.services` — gli stessi servizi «deny by default» che le pagine usano — e
non introduce né un permesso né una query non filtrata. Una palette che mostrasse ciò che il ruolo
non può aprire sarebbe una fuga d'informazione, e questo resta il criterio.

### 4.10 Caricamento e cascata (lacuna 4)

`base.html` precarica sei layer V2 e collega `css/main.css`, che li `@import`a in ordine;
`base_portal.html` aggiunge il proprio foglio in `{% block extra_head %}`, **dopo** `main.css`.
La shell V3 va lì, in tre `<link>` espliciti:

```django
{% block extra_head %}
<link rel="stylesheet" href="{% static 'css/v3/tokens-shell.css' %}">
<link rel="stylesheet" href="{% static 'portal/portal.css' %}">
<link rel="stylesheet" href="{% static 'css/v3/platform-shell.css' %}">
{% endblock %}
```

Ordine e motivo, riga per riga:

1. `tokens-shell.css` prima di tutto: non contiene selettori, solo `:root`, e i suoi valori devono
   essere leggibili sia da `portal.css` (durante la transizione) sia dalla shell.
2. `portal.css` resta finché i suoi blocchi di cromo non sono stati rimossi (stessa PR, n. 16 del
   § 4.8). Dopo la rimozione la riga resta: `portal.css` continua a stilare `.portal-section`,
   `.data-table`, `.register`, `.sequence`, cioè il **contenuto**, non il cromo.
3. `platform-shell.css` per ultimo, perché deve poter vincere su `v2/shell.css` (le due regole del
   lock-up, § 4.2) e su `register.css` (`.folio__ordinal` che passa nel margine, § 4.4) senza usare
   `!important`.

**Nessun `@layer`.** Il progetto non usa i layer da nessuna parte: introdurne uno qui invertirebbe
la cascata, perché **qualunque** regola non stratificata batte qualunque regola stratificata — e
`register.css`, `components.css` e `portal.css` sono tutte non stratificate. L'isolamento è
ottenuto dal **prefisso `p`** (`.pbar`, `.pband`, `.pshell`, `.prail`, `.pcol`, `.pinspect`,
`.pstate`, `.ptally`, `.pweave`, `.pcmd`), che non collide con nessuno dei prefissi esistenti
(`.portal-*`, `.page-header*`, `.case-header*`, `.breadcrumbs*`, `.local-nav*`). Le uniche regole
che raggiungono classi altrui sono **sette**, tutte discendenti da `.pband` o `.pbar`, tutte elencate
in questo documento: `.pband .page-header`, `.pband .page-header__title`,
`.pband .page-header__eyebrow`, `.pband .page-header__lead`, `.pband__crumbs.breadcrumbs`,
`.pbar .lock--dark …`, `.pcol .folio__ordinal`. `bridge.css` non interviene: la shell usa token V2
diretti, mai token legacy.

**Nessun preload.** I tre fogli sono `<link>` in testa, non target di `@import`: non c'è catena da
spezzare (i preload di `base.html` esistono perché `main.css` li importa).

### 4.11 `shell-portal.js` — i compiti, per esteso

Modulo ES, `type="module"`, `script-src 'self'`, bundlato da esbuild come gli altri. Sette compiti,
nessun altro.

1. **Sentinella di scroll.** Un `IntersectionObserver` su una sentinella di 1 px sopra la banda →
   `data-scrolled` su `.pbar`. Nessun ascoltatore di `scroll`, nessuna lettura di layout.
2. **Evidenziatore del rail.** `pointerover` delegato su `.prail__list`, **solo** dentro
   `matchMedia('(hover: hover)')`; posiziona `.prail__hover` con `SPRING_FOLLOW`.
3. **Compressione del rail.** `click` sul toggle → `data-rail` su `.pshell`, `aria-expanded`
   aggiornato, stato in `localStorage['ile.rail']`, e FLIP sulla colonna centrale (§ 5.3).
4. **Palette.** Apertura con `Ctrl/⌘ K` e con l'innesco; `role="combobox"` + `aria-expanded` +
   `aria-controls` + `aria-activedescendant`; `fetch` su `portal:palette` con `AbortController`;
   trappola del fuoco, `inert` sul resto, Escape, fuoco restituito all'innesco.
5. **Legenda dei tasti.** Su `navigator.platform`/`userAgentData` Apple, riscrive il testo di
   `.pbar__cmd-keys` da `Ctrl K` a `⌘ K`. Una sola scrittura di DOM al caricamento.
6. **Chiusura dei `<details>`** (lacuna 10, MUST-FIX 9). Per ogni `[data-dropdown]`: Escape chiude e
   restituisce il fuoco al `<summary>`; `pointerdown` fuori chiude; `focusout` verso un nodo esterno
   chiude; `aria-expanded` sul `<summary>` segue `open`. Il commento di
   `language_switcher.html` promette esattamente questo comportamento («JS closes it on Escape,
   outside click and focus loss») e il JS che lo forniva è andato perso nella riscrittura V2:
   `grep -r data-dropdown static/js/src/` non torna nulla. Questo compito lo **restituisce**, ed è la
   condizione perché i due menu possano diventare pannelli da 280 px.
7. **Striscia: portare in vista la voce corrente.** Sotto 1024, dopo il primo `rAF`, **una** chiamata
   a `el.scrollIntoView({ behavior: 'auto', inline: 'nearest', block: 'nearest' })`.
   **`behavior` è sempre `'auto'`, mai `'smooth'`** (lacuna 13): `'smooth'` è un'animazione temporata
   dallo user-agent che non corrisponde a nessuna delle quattro durate del sistema. Non essendo
   un'animazione, questa riga **non compare** nel § 5 e non ha una voce di catalogo — il round 1 la
   dichiarava come moto e poi le dava uno stato ridotto che era il suo unico stato.

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` § 6

Sei voci. La shell rivendica **quattro** delle sette funzioni — orientamento, feedback, profondità,
stato. Non ha gerarchia (non c'è un reveal editoriale in uno spazio di lavoro), non ha causalità (il
cambio di stato di un fascicolo è la voce della superficie `case-file`, non di questa), non ha
delizia: la delizia è dell'hero e non si contrabbanda in una scrivania.

1. **`shell.bar.scrolled`** · ORIENTAMENTO · sentinella `IntersectionObserver` sopra la banda ·
   `--motion-slow` 320 ms · `--ease-standard` · `background-color` `--mid-1`→`--mid-0` e
   `border-block-end-color` `--hairline-dark-strong`→`--accent-dark` · **ridotto**: lo stato si
   applica senza transizione · *budget*: 2 ripitture per cambio di stato, 0 layout.
   **Nessun `box-shadow`**: il round 1 ne transiva uno, che la deroga A1 vieta sulle superfici in
   flusso e che il vincolo di prestazione vieta comunque di animare.
2. **`shell.rail.hover-follow`** · FEEDBACK · `pointerover` su `.prail__list`, solo
   `@media (hover: hover)` · `SPRING_FOLLOW` (400/40, ζ = 1,000) · `transform: translate3d(0,Ypx,0)
   scaleY(S)` su **un solo** `.prail__hover`, `transform-origin: 0 0` · **ridotto**: l'evidenziatore
   salta alla riga, senza molla · *budget*: 1 strato composito invece di 13 ripitture di sfondo;
   `will-change: transform` solo mentre il puntatore è dentro la lista.
   **`.prail__hover` non ha bordo e non ha raggio, ed è una decisione, non un'omissione** (lacuna
   14): le righe non sono tutte alte uguale — un'etichetta lunga va a capo — quindi `scaleY` è
   necessario, e `scaleY` deformerebbe qualunque bordo o raggio. Un rettangolo pieno `--min-2` senza
   contorni è l'unica forma che `scaleY` non può rovinare.
3. **`shell.rail.collapse`** · ORIENTAMENTO · clic sul toggle (solo ruoli operativi) · etichette
   `--motion-instant` 120 ms `--ease-in`, assestamento della colonna con `SPRING_SETTLE` (260/30,
   ζ = 0,930, sovraelongazione calcolata 0,034 %) · etichette `opacity 1→0` +
   `translateX(calc(-4px * var(--dir)))`; la colonna di contenuto usa **FLIP** (misura prima/dopo,
   poi `transform` fino a 0) · **ridotto**: la larghezza cambia, nulla anima · *budget*: la larghezza
   del rail cambia in **un** frame; mai animati `width` né `grid-template-columns`.
4. **`shell.palette.open`** · PROFONDITÀ · `Ctrl/⌘ K` o clic sull'innesco · `--motion-slow` 320 ms ·
   `--ease-out` in entrata, `--ease-in` in uscita · scrim `opacity 0→1`, pannello `opacity` +
   `translateY(8px→0)` · **ridotto**: apertura immediata, scrim fermo · *budget*: promozione solo
   durante l'animazione; fuoco nel campo, Escape chiude, fuoco restituito all'innesco.
5. **`shell.inspector.section-state`** · STATO · cambio del dato (nuovo messaggio, scadenza risolta)
   · `--motion-base` 240 ms · `--ease-standard` · il chip transisce **fra due parole**, non fra due
   colori; riga inserita/rimossa con `SPRING_SETTLE` su `transform` · **ridotto**: testo aggiornato
   senza transizione · *budget*: mai su liste oltre 8 righe.
6. **`shell.menu.disclose`** · PROFONDITÀ · apertura di `.pbar__menu` o `.pbar__lang` (`<details>`
   nativi) · `--motion-base` 240 ms — il token che `MOTION_SYSTEM` § 1 destina a «pannelli, tab,
   accordion», ed è quello che un `<details>` è · `--ease-out` in entrata, `--ease-in` in uscita ·
   pannello `opacity 0→1` + `translateY(-8px→0)`, chevron del sommario `rotate(180deg)` ·
   **ridotto**: il pannello appare al valore finale, il chevron è già ruotato, nulla a opacità 0 ·
   *budget*: un solo strato promosso, `@keyframes` dentro `@media (prefers-reduced-motion:
   no-preference)`, chiusura gestita dal compito 6 di `shell-portal.js`.

**Due voci del round 1 non ci sono più.** `shell.plate.copy` è eliminata (violazione 7): il suo
innesco contraddiceva la definizione della targa. `shell.strip.reveal-current` è eliminata (lacuna
13): non è moto, è una posizione di scorrimento impostata una volta prima del primo disegno, e ora
vive nel § 4.11 compito 7.

**Nessun loop ambientale nella shell**: né DENSE né RICH ne hanno diritto per il § 4 di
`MOTION_SYSTEM`, e la shell non se ne prende uno di straforo.

Tutte le `transition` e tutte le `@keyframes` di `platform-shell.css` stanno dentro
`@media (prefers-reduced-motion: no-preference)`; fuori da quel blocco il valore è quello finale.

---

## 6. ACCESSIBILITÀ E RTL

- **Tabulazione = ordine visivo**: skip link (già primo nel DOM in `base.html`) → lock-up → targa →
  palette → account → lingua → briciole → titolo → azione primaria → rail → contenuto → inspector.
- `:root { scroll-padding-block-start: calc(var(--shell-bar-h) + 8px) }`: un ancoraggio non finisce
  mai sotto la barra appiccicosa (difetto 15, e punto 1 di UI-UX-Pro-Max).
- Regioni annunciate: `<header role="banner">` sulla `.pbar`,
  `<nav aria-label="Navigation de l'espace réservé">` sul rail,
  `<main id="main-content" tabindex="-1">` (**quello che esiste già**, § 4.7),
  `<aside aria-labelledby="pinspect-title">`.
- **Bersagli**: ogni controllo del cromo ≥ 24 × 24 e **≥ 44 × 44 su `(pointer: coarse)`**, striscia
  compresa. Misurato **[m]**: a 390 targa 110,4 × **44**, innesco 44 × **44**, account 44 × **44**,
  lingua 44 × **44**, riga della striscia 186,5 × **44**, azione primaria 350 × **44**. A 1440 (fine)
  32 px di altezza, ≥ 24. Il round 1 dichiarava la regola e fissava i controlli a 32 senza override:
  su puntatore grossolano fallivano tutti.
- **Stato mai per colore**: pillola = glifo + parola + forma; misuratore = tacche (3 px piene / 2 px
  vuote) **+ conteggio letterale**; voce corrente = barra + fondo + peso + `aria-current` + testo
  nascosto; responsabile = trama + glifo + parola.
- `prefers-reduced-motion` è uno **stato completo**: rail compresso o esteso, menu aperto o chiuso,
  palette aperta o chiusa, inspector pieno o vuoto sono identici nei contenuti, nulla a opacità 0,
  nulla fuori posizione.
- `forced-colors: active`: graticola e banda territoriale `display: none`; rigatura della tela
  `background-image: none`; trame del rail e trame dei responsabili conservate con
  `forced-color-adjust: none` **solo** su quei segmenti; la barra della voce corrente diventa
  `Highlight`; tutti i confini passano a `CanvasText`; fuoco con l'outline di sistema.
- **RTL**: **solo** proprietà logiche (`inset-inline`, `padding-inline`, `border-inline-*`,
  `margin-inline-start: auto`). Si specchiano graticola e banda (`scaleX(-1)`), frecce, chevron delle
  briciole, direzione della striscia, segno di `translateX` (via `--dir`). **Non** si specchiano il
  lock-up (`dir="ltr"` sempre), il riferimento di pratica, i numerali, il misuratore. Misurato a
  1440 in `dir="rtl" lang="ar"`: lock-up al margine finale (x 1110,8), dorso del rail a destra
  (x 1116), inspector a sinistra (x 100), **nessuno scorrimento orizzontale** **[m]**.
- `:lang(ar)`: `letter-spacing: 0` e `text-transform: none` su targa, folio, etichette dei fatti,
  etichetta di ruolo e titoli dell'inspector; `min-inline-size: 120px` sui controlli della barra;
  interlinea 1,8 nel corpo della colonna — misurata: **58,1 caratteri medi** di misura **[m]**.
- **`HUMAN_QA_REQUIRED`**: sessione reale NVDA/JAWS/VoiceOver su shell, menu e palette; Windows High
  Contrast reale; revisione araba madrelingua delle etichette del rail e dei nomi di lingua resi da
  `site.languages`; dispositivi iOS/Android reali per la striscia a 44 px e per `100dvh` con la
  barra del browser.

---

## 7. PRESTAZIONI

| Voce | Costo misurato | Come rientra |
|---|---|---|
| `static/css/v3/platform-shell.css` | candidato **18 954 B grezzi · 4 015 B gz** [m, `gzip -9`] | Sostituisce il cromo di `portal.css` (24 115 B grezzi / 6 615 B gz). Tetto per il foglio completo (palette e stati vuoti compresi): **≤ 26 KB grezzi / ≤ 5,5 KB gz**, verificato in CI |
| `static/css/v3/tokens-shell.css` | ≈ 0,6 KB · ≈ 0,3 KB gz | Otto variabili di layout + `--dir`, **nessun colore** |
| `shell-portal.js` | **budget ≤ 2,5 KB gz**, non ancora misurato perché non ancora scritto | Sette compiti del § 4.11; il controllo di dimensione sta nel passo di build |
| `static/js/head.js` | 206 B gz [m] | già caricato |
| `static/js/main.js` | 5 293 B gz [m] | già caricato |
| `static/js/dist/shell.js` | 613 B gz [m] | già caricato |
| Chunk condiviso Motion | **26 120 B gz** [m] | Oggi il portale lo scarica e non anima nulla (difetto 8): qui finalmente lo paga |
| **Totale JS di pagina** | 206 + 5 293 + 613 + 26 120 + ≤ 2 560 = **≤ 34 792 B gz ≈ 34,0 KB** | Budget 45 KB gz — margine ≈ 11 KB |
| Graticola + banda territoriale | ≈ 1,1 KB + ≈ 1,4 KB SVG inline | Nessuna richiesta di rete, nessuna bitmap |
| Immagini | **0 KB** per viewport | Il marchio è SVG, il territorio è SVG, la rigatura è un gradiente |

Il round 1 dichiarava «totale JS di pagina ≈ 28,2 KB gz» contando solo `shell-portal.js` e il chunk
di Motion, e dimenticando `main.js` e `head.js`, che ogni pagina del portale scarica. Il totale
onesto è 34,0 KB gz e rientra lo stesso.

**Paint e layout.** La barra ripittura **2 volte** al cambio di stato di scroll (fondo + filetto) e
mai altrimenti; l'evidenziatore del rail è un solo strato composito (`transform` puro); il rail
compresso non anima `width` né `grid-template-columns` — la larghezza cambia in un frame e il
contenuto si riassesta con FLIP. Nessun `filter`, **nessuna ombra animata**, nessun loop ambientale,
nessun `backdrop-filter` (la barra scrollata cambia **terreno**, non sfoca: `backdrop-filter` resta
riservato all'header pubblico). Nessun `content-visibility`.

**Prova richiesta prima dell'accettazione.** Pannello Performance di Chrome durante scroll, hover del
rail, compressione e apertura della palette → **0 layout e 0 paint oltre il primo frame**; INP <
200 ms su toggle e palette; CPU rallentata 4×; e `document.documentElement.scrollWidth ===
window.innerWidth` a 360, 390, 768, 1024, 1280, 1440 in LTR e in RTL (già verificato sul candidato,
§ 9).

---

## 8. RISCHI

| Rischio | Perché farebbe sembrare il prodotto a buon mercato | Guardia |
|---|---|---|
| **Deriva dev-tool** — barra scura + scorciatoia + rail a glifi | Il committente vende una porta istituzionale, non un IDE | La guardia non è più un'etichetta appiccicata allo scheletro: **la geometria cambia** — dorso continuo, margine di registro numerato, rigatura sulla cadenza del corpo, tre terreni. In più: lock-up ufficiale a tutta forza, targa mono come riferimento di pratica, titolo Newsreader 48/52, palette solo ai ruoli operativi e mai unico modo di raggiungere qualcosa, e **nessun chip di tastiera** |
| **Il teal ovunque** | Teal + scuro = fintech | `--accent` **solo** su link, CTA, fuoco, barra della voce corrente e bordo del «prochaine étape». Il territorio è grafica: graticola **22 %**, banda **30 %** — misurati, sopra la soglia di 1,365 e sotto qualunque soglia di lettura. Il misuratore **non** usa `--accent` (violazione 3) |
| **Densità presa per ricchezza** | Tre regioni piene di riquadri = il cruscotto 3/10, con ombre in più | «Prochaine étape» resta **una** cosa, primo foglio del registro; l'inspector porta contesto, **mai una decisione e mai un numero non calcolato**; la banda ha **una** azione primaria; e non ci sono ombre in flusso da aggiungere |
| **L'inspector diventa una discarica** | Colonna destra come «dove metto quello che avanza» | Quattro sezioni fisse; una quinta richiede una riga in questo documento e una chiave di contesto; ogni sezione ha uno stato vuoto che dice chi la riempie |
| **Le tacche del misuratore mentono** | Un misuratore che il modello non calcola è decorazione | Le cinque tacche sono `aria-hidden`, **sempre** accompagnate dal conteggio letterale, e derivano da `progress.done / progress.total`; senza quel dato il misuratore non si disegna |
| **Il rail compresso perde il nome delle cose** | Un rail a soli glifi è illeggibile per chi non conosce il prodotto | `aria-label` **e** `title` su ogni voce compressa (il `title` nativo è il suggerimento: nessun componente nuovo, nessuna ombra); compressione **solo** ai ruoli operativi, mai alla persona; stato ricordato, mai imposto |
| **La graticola diventa rumore — o sparisce** | Una texture su tutto è il contrario del premium; una texture invisibile è un'idea sprecata | Due sole apparizioni (deroga A2), sempre mascherate, mai sotto un testo, assenti in `forced-colors`, **e con un pavimento di percettibilità misurato**: nessuna grafica di questa superficie sotto 1,365:1 di rapporto con il proprio fondo |
| **La rigatura legge come un quaderno** | Carta a righe = scuola, non istituzione | Passo 28 px, cioè l'interlinea del corpo, non un passo arbitrario; visibile **solo** nelle gole e nei margini (144 px su 1440), mai sotto un testo; assente sotto 1024 e in `forced-colors` |
| **`100dvh` e la barra mobile del browser** | Rail e inspector che saltano a ogni scroll su iOS | `dvh` con ripiego `vh` dichiarato due volte, `overscroll-behavior: contain` sui due contenitori scorrevoli, `max-block-size` e non `block-size`, verifica su dispositivo reale (`HUMAN_QA_REQUIRED`) |
| **Due sistemi di navigazione conviventi** | `portal.css` e `platform-shell.css` insieme = doppie regole e un cromo ibrido | La riscrittura **rimuove** i blocchi `.portal-bar`, `.case-header`, `.next-action` e `.portal` da `portal.css` nello stesso commit; `test_v3_shell_has_no_twin.py` li conta |
| **La migrazione dei titoli si ferma a metà** | Due sistemi di titolo su 51 template | 38 template non richiedono alcuna modifica (il loro titolo è già nel blocco); **nove** sono elencati per nome al § 4.8 n. 14; un test asserisce che ogni template della famiglia del portale ha esattamente un `<h1>` e che quell'`<h1>` è dentro `.pband` |

---

## 9. APPENDICE — le misure del round 2

Chromium headless di Playwright dal `.venv` del progetto, browser proprio, **mai** la porta 9222.
Foglio candidato montato con `page.route()` su `http://127.0.0.1:8770/candidate.html`, così che
`main.css`, i token V2 e i font self-hosted siano quelli veri. `device_scale_factor: 1`;
`has_touch: true` a 768, 390 e 360.

**Layout** (tutte in px; «spazio di lavoro» = `y` della prima riga di `.pshell`).

«banda» in tre condizioni: senza `case` / con `case` e senza sospensione / con entrambi. «spazio di
lavoro» = `y` della prima riga di `.pshell` nelle stesse tre condizioni.

| viewport | barra | banda (3 condizioni) | spazio di lavoro (3 condizioni) | riga del rail | misura (caratteri medi) | scroll orizzontale |
|---|---:|---|---|---:|---:|---|
| 1440 × 900 | 57 | **154** / 294 / **340** | **211** / 351 / **397** | 40 | 69,1 | no |
| 1280 × 900 | 57 | 154 / 314 / 360 | 211 / 371 / 417 | 40 | 53,3 | no |
| 1024 × 900 | 57 | 138 / 318 / 364 | 195 / 375 / 421 | 40 | 74,9 | no |
| 768 × 1024 (touch) | 57 | 138 / 345 / 391 | 195 / 402 / 448 | 44 | 74,9 | no |
| 390 × 844 (touch) | 53 | **182** / 270 / **356** | **235** / 323 / **409** | 44 | 36,2 | no |
| 360 × 800 (touch) | 53 | 182 / 270 / 376 | 235 / 323 / 429 | 44 | 32,4 | no |
| 1440 × 900 `ar`/`rtl` | 57 | — / — / 340 | — / — / 397 | 40 | 58,1 | no |

Riferimento dello stato attuale, round 1: `.next-action` a `y = 444` a 1440 e a `y = 843` a 390.

**Componenti** (larghezza × altezza).

| | 1440 | 1024 | 390 (touch) |
|---|---|---|---|
| lock-up (unità) | 229,2 × 34 | 229,2 × 34 | 34 × 34 (testo `.visually-hidden`) |
| targa di contesto | 175,5 × 32 | 135,9 × 32 | 110,4 × **44** |
| innesco della palette | 200,5 × 32 | 200,5 × 32 | 44 × **44** |
| sommario account | 153,5 × 32 | 153,5 × 32 | 44 × **44** |
| sommario lingua | 159,9 × 32 | 159,9 × 32 | 44 × **44** |
| riga del rail / chip | 223 × 40 | 223 × 40 | 186,5 × **44** (più largo: 321) |
| azione primaria della banda | 176,6 × 44 | 176,6 × 44 | 350 × **44** |
| titolo della banda | 610,4 × 52 (48/52) | 406,9 × 36 (32/36) | 350 × 36 (32/36) |
| dorso del rail | 224 × 645 | 224 × 645 | 350 × 45 (striscia) |
| colonna centrale | 632 | 688 | 350 |
| inspector | 320 × 338 | 944 × 180 (2 colonne, in coda) | 350 (1 colonna, in coda) |

**Colore.** Rapporti calcolati in `contrast.py` (luminanza relativa WCAG 2.x, composizione alfa
esatta); percettibilità letta sui pixel di `pix.png` (PNG di screenshot, `device_scale_factor: 1`).

| Misura | Valore | Metodo |
|---|---:|---|
| `--min-3` su `--accent-ring` (round 1) | **4,110** | calcolato — fallisce AA |
| `--min-0` su `--accent` (round 2) | **5,692** | calcolato |
| `--ok-700` su `--min-3` | 5,322 | calcolato |
| `--seal-600` su `--min-3` | **4,768** | calcolato — la revisione dava 3,995, che è il valore su `--min-1` |
| `--hairline` su `--min-0` (soglia) | **1,365** | pixel |
| graticola `--terr-line` su `--mid-1` a 8 % | **1,119** | pixel — sotto la soglia |
| graticola a 14 % / 18 % / 22 % / 30 % | 1,245 / 1,326 / **1,419** / 1,674 | pixel — adottato 22 % |
| banda `--terr-line-lt` su `--min-1` a 22 % / 30 % | 1,376 / **1,564** | pixel — adottato 30 % |
| `--hairline-dark-strong` composita su `--mid-1` | `#465359`, **2,202** | composizione alfa |
| salti di terreno `--min-1`/`--min-0` · `--min-2`/`--min-1` | 1,076 · 1,144 | calcolato |

**Tipografia.** Avanzamento di `1ch` in Fira Sans 17 px: **9,35 px**; carattere minuscolo medio:
**7,849 px**; rapporto 1,191 → `65ch` = 77,4 caratteri medi, `62ch` = 73,9. Da cui il § 4.4.

**Molle.** ζ = c / (2√(k·m)), m = 1. `SPRING_FOLLOW` 400/40 → ζ = **1,000** (critica, zero
sovraelongazione). `SPRING_SETTLE` 260/30 → ζ = **0,930**, sovraelongazione `exp(−πζ/√(1−ζ²))` =
**0,034 %**. Nessuna terza molla è necessaria e nessuna è ammessa.

**Peso.** `platform-shell.css` candidato: 18 954 B grezzi, **4 015 B gz** (`gzip -9`).
`portal.css` oggi: 24 115 B / 6 615 B gz. `shell.js`: 1 136 B / **613 B gz**. Chunk Motion:
70 441 B / **26 120 B gz**. `main.js`: 19 944 B / **5 293 B gz**. `head.js`: 233 B / **206 B gz**.
