# V3 — FONDI E SUPERFICI · «la materia, non la tinta»

Area `backgrounds` · Creative Technologist + Color & Material · Vincolanti: `DESIGN_SYSTEM_V2.md`
§1.3/§2/§6/§7, `MOTION_SYSTEM.md`, `BRAND_ASSETS.md` §1.
**Round 2 — riscrittura dopo `docs/design-v3/reviews/backgrounds.md`.**

Tutte le misure di questo documento sono del **24.09.2026**, prese con il Chromium headless di
Playwright (`HeadlessChrome/153.0.8010.12`) lanciato da `.venv/Scripts/python.exe` su
`127.0.0.1:8771/fr/` (Fase 3 aperta) **e** `127.0.0.1:8770/fr/` (Fase 3 chiusa), a **1440 · 1200 ·
768 · 390** px, più zoom 200 % e 400 %, `dir=rtl`, `forced-colors: active`,
`prefers-contrast: more`, `prefers-reduced-motion: reduce`. Contrasti calcolati in Python
(luminanza relativa WCAG 2.x), composizioni alfa calcolate e poi **ri-verificate campionando i
pixel** dello screenshot. Il registro completo di come ogni numero è stato ottenuto è al **§9**.
Dove il round 1 aveva un numero sbagliato, il numero è corretto **e segnalato**.

---

## 0. RICHIESTE DI DEROGA (numerate, esplicite)

> Nessun altro scostamento dai documenti vincolanti esiste in questo documento. Il sistema di moto
> non ne chiede nessuno: **il sistema di fondi non anima nulla** (§5).

**DEROGA 1 — `DESIGN_SYSTEM_V2.md` §6, «Sistema cartografico … **mai** su STANDARD/DENSE/LEGAL».**
*Che cosa chiedo:* che la **graticola** (non le isoipse) sia ammessa anche in modo STANDARD, nella
sola forma definita al §4.3: un reticolo **di margine**, confinato alla fascia
`--grat-margin` (100 px a 1440, 52 px a 1200, 40 px a 768, 20 px a 390), mai sotto la colonna di
testo, a `opacity: var(--material)` con `--material: 0` in DENSE e LEGAL.
*Perché:* la clausola §6 è scritta per l'oggetto che nomina nella stessa riga — le isoipse generate
da `scripts/territory.py`, «≤ 43 KB inline per pagina IMMERSIVE». Quel costo è la ragione del
divieto. La graticola di margine non è quell'oggetto: è **0 byte di asset** (sei gradienti CSS),
non è inline nell'HTML, non entra nell'albero di accessibilità e non attraversa mai il testo. Senza
di essa le pagine STANDARD restano ciò che il §1.2 misura oggi: una tinta unica per 2 211 px.
*Che cosa costa:* +6 layer di background per sezione su STANDARD. Misurato sulla home reale:
`LayoutCount` **Δ 0**, `RecalcStyleDuration` **7,8 ms contro 9,1 ms della pagina di oggi**,
`TaskDuration` **204 ms contro 233 ms** (§7). Le isoipse restano vietate fuori da IMMERSIVE: questa
deroga non le tocca.
*Se negata:* `[data-mode="standard"]{ --material: 0 }` è una riga sola e il sistema resta valido —
le pagine STANDARD tornano a fondo + soglia, senza materia.

**DEROGA 2 — `DESIGN_SYSTEM_V2.md` §1.3-5, «Un capitolo mezzanotte per pagina fuori da HOME e
FORUM».** *Che cosa chiedo:* che la clausola dica **per iscritto** ciò che l'implementazione
corrente già fa, cioè che **si contano i capitoli dentro `<main>`; la cornice del sito non è un
capitolo**. *Perché:* misurato il 24.09 su sei rotte, `.site-footer` ha
`background-color: rgb(10, 21, 28)` = `--mid-0` su **tutte**, comprese `/fr/faq/` (STANDARD, zero
capitoli scuri ammessi) e le quattro landing. Se il piè di pagina contasse, **ogni pagina pubblica
del sito violerebbe la clausola oggi**, comprese quelle in modo LEGAL. La lettura «il piè di pagina
è cornice» è l'unica che rende la regola applicabile. *Costo:* nessuno; è una chiarificazione. Ne
discende il conteggio del §6 e il test `test_v3_chapter_count.py`.
*Nota:* il §1.6 del round 1 condannava il FORUM contando anche il piè di pagina. Quel conteggio era
sbagliato e il §1.6 è riscritto: il FORUM viola comunque, ma per un'altra ragione e in due punti,
non in uno (§1.6).

**DEROGA 3 — `DESIGN_SYSTEM_V2.md` §1.1, la tavolozza è chiusa.** *Che cosa chiedo:* due neutri
nuovi, `--min-edge: #e4e2db` e `--mid-edge: #16272f`, **usabili solo come stop di gradiente dentro
la soglia**, mai come `background-color` di una sezione, mai come colore di testo, mai come bordo.
*Perché:* una rampa che va da `--min-0` a `--mid-1` senza uno stop intermedio più profondo del
proprio estremo chiaro non ha un «orizzonte»: legge come sfocatura (rischio §8-3). *Costo:* due
token. Verificati comunque come se fossero fondi di lettura: su `--min-edge`, `--ink` **12,52:1**,
`--ink-3` **4,74:1**, `--accent` **4,87:1**, anello `--accent-ring` **3,17:1**; su `--mid-edge`,
`--on-dark` **13,63:1**, `--on-dark-3` **5,66:1**, `--accent-dark` **8,80:1** (§4.2).
*Test che la tiene onesta:* `test_v3_edge_tokens_are_ramp_only.py` — `--min-edge`/`--mid-edge` non
compaiono in nessuna dichiarazione `color`, `border-*-color` o `background-color` del CSS compilato.

---

## 0-bis. RISPOSTA PUNTO PER PUNTO ALLA REVISIONE

### MUST-FIX

| # | Esito | Dove |
|---|---|---|
| 1 | **FATTO** — il confine `_pilot` → `_trust` non è più scritto a mano: è **derivato dal fratello DOM**. Con `pilot` presente (8771) `trust` riceve una **risalita** di 96 px da `--mid-1`; con `pilot` assente (8770) riceve una **piega** di 96 px da `--min-0`. Verificato su entrambe le build a quattro larghezze | §4.3, §9-2 |
| 2 | **FATTO** — tutte le classi `th--from-*` sono cancellate. La soglia nasce da nove regole di fratello adiacente. Verificato sulla build a Fase 3 chiusa, dove `_banner` compare, e `_pilot`/`_antifraud`/`_reserved` spariscono: `--ground-prev` si ricuce da solo su tutte e otto le sezioni | §4.3, §9-2 |
| 3 | **FATTO** — `--th` non è più un numero: è `min(<ideale>, var(--th-room))`, e `--th-room` è legato al token di rango della sezione. Tabella rango→soglia al §4.2. **0 sconfinamenti su 10 sezioni × 4 larghezze × 2 build, più zoom 200 % e 400 %, più `dir=rtl`** | §4.2, §6, §9-3 |
| 4 | **FATTO** — i tre `--th-*-mid` sono dichiarati in `:root` **e** ricalcolati: `#556165`, `#5d686b`, `#edebe7`, con il fallback `@supports not (color-mix…)` completo (`#5c6769`, `#646e70`, `#edebe7`) — il round 1 dava un solo fallback su tre | §4.2, §4.3, §9-4 |
| 5 | **FATTO, e in modo più forte di quanto chiesto.** Spostare il kill-switch su `.ground` non basta: le regole di passaggio hanno specificità (0,2,0) e vincono comunque su `--lume`. Il kill-switch è ora uno **scalare ereditato**, `--material`, letto al punto d'uso — nessuna specificità lo può battere. Verificato: `prefers-contrast: more` → `--material: 0`, `::before` opacity **0**, `::after` opacity **0**, banda di luce **0 px**, rampa **96 px conservata** | §4.3, §9-6 |
| 6 | **FATTO** — §4.7 è CSS, con il selettore nominato, e lo stato non è mai solo colore: bordo `--hairline` → `--hairline-strong` (**2,47:1 fra i due**, e 3,59:1 sul foglio), `--shadow-2` che compare (ruolo 2, solo in hover, come prescrive §2), fondo `--min-2` → `--min-3`, `:focus-within` identico all'hover, `active` con `translateY(1px)` e l'ombra che sparisce | §4.7 |
| 7 | **FATTO** — la soglia **non anima**. Zero durate nuove, zero tracciati immersivi, zero elementi `.tide` nel DOM. Il sistema di fondi aggiunge **0 animazioni**: misurato, `document.getAnimations().length` = **3 prima e 3 dopo** (le due falde della marea + la rotta legata allo scroll). Sulla quota: misurata, non asserita — le quattro landing e il FORUM hanno **0 animazioni, 0 loop ≥ 20 s, 0 ScrollTimeline, 0 gradienti** | §5, §7, §9-7 |
| 8 | **FATTO** — `--accent-dark` non compare più in questo documento. Regola scritta: **la luce è sempre il colore di testo del proprio capitolo a bassa alfa, mai una tinta** | §4.2, §8-2 |
| 9 | **FATTO** — §4.6 riscritta con markup `<picture>`/`<img class="ground__plate" alt="">`, selettori, `srcset`/`sizes`, tre classi di inquadratura (niente `style=""`), la politica `alt`, e la direzione artistica (soggetto, taglio, terzo quieto) | §4.6 |
| 10 | **FATTO** — il file è `templates/partials/portal_chrome.html`, **non** `templates/portal/partials/portal_chrome.html`. Riga corretta e §4.8 nuova con i selettori reali (`.portal-bar`, `.case-header`, `.next-action`, `.portal__aside`, `.portal__main`, `.portal-account`, `.portal-footer`) e i loro padding misurati | §4.8 |
| 11 | **FATTO, e la causa era un'altra.** Con la soglia derivata, `_antifraud` riceve una piega da solo (32/24/24 px) senza che nessuno la scriva. `_reserved` perde ogni classe `ground` — `padding-block-start: 0` e un pannello opaco: non c'è materia da mostrare — e diventa invece il **foglio** che avrebbe dovuto essere. In più: il filetto fra `hero` ed `entrances` **non nasce da `pages.css:47-49`**, nasce da `components.css:1188-1192`; cancellare solo la prima regola lo lascerebbe in pagina | §1.3, §4.5 |
| 12 | **FATTO, e il difetto è doppio.** `.forum-cta` (forum.css:141) non è l'unico fondo tricolore del FORUM: anche `.forum-hero` (forum.css:24-25) è `rgb(15, 37, 71)` = `--brand-navy`, misurato, alto 388 px. Entrambi riparati al §4.9 | §1.6, §4.9 |
| 13 | **CONTESTATO, con misura, e insieme risolto per iscritto** — vedi DEROGA 2 | §0, §6 |
| 14 | **FATTO, e sostituito da qualcosa che non può rompersi:** niente shorthand `mask`. Solo longhand (`mask-image`, `mask-repeat`, `mask-size`), quindi `mask-mode: alpha` non viene mai azzerato. Verificato che il difetto era reale (`mask-mode` prima dello shorthand → `match-source`; dopo → `alpha`) | §4.4, §9-5 |
| 15 | **FATTO** — `graticola-deriva` è **cancellata** (§5). §7 è rimisurato sulla **home reale con il candidato applicato**, non sul prototipo statico | §5, §7, §9-8 |

### VIOLAZIONI

| # | Esito |
|---|---|
| 1 | **RIMOSSA.** Nessun tracciato immersivo, nessuna durata di 600 ms, nessun `.tide` nel DOM. |
| 2 | **RIMOSSA.** `--accent-dark` non è più speso come luce ambientale. |
| 3 | **CONTESTATA** con misura + **DEROGA 2** (la regola di conteggio è scritta). |
| 4 | **RIMOSSA.** §4.6 ha markup: l'URL vive in `srcset`/`src`, cioè in attributi HTML sotto `img-src 'self'` — misurato l'header CSP della build: `img-src 'self' data:`. Nessun `style=""`, nessun foglio generato. |
| 5 | **RIMOSSA.** Vedi MUST-FIX 6. E le due cifre del round 1 sono ricalcolate: l'hover era **1,043:1** (non 1,03) e l'active **1,144:1** (non ~1,06). Entrambe restano insufficienti; la correzione non cambia il verdetto, cambia il numero. |
| 6 | **RIPARATA** al §4.9, su entrambi i fondi navy, e il test del §8-6 ora corrisponde a codice che il documento ripara. |

### LACUNE — tutte chiuse

1 → §4.2/§4.3 (token dichiarati + fallback) · 2 → §4.3 (fratelli) · 3 → §4.2 (tabella rango) ·
4 → §4.7 (CSS) · 5 → §4.8 (percorso corretto) · 6 → §4.5 (`_banner` **è** nella tabella: su :8770 è
visibile oggi, misurato) · 7 → §4.5 · 8 → §4.5 (`chapter--dark` **resta**: è l'unico aggancio di
`shell.css:483-486`) · 9 → §5 (il moto è cancellato, il comando non serve) · 10 → §9-7 (quota
misurata) · 11 → §4.3 (`--material`) · 12 → §4.4 (solo longhand) · 13 → §4.3 (la maschera del
`::before` parte da `transparent` a y=0: nessuna cucitura) · 14 → classe morta cancellata ·
15 → §5/§7 · 16 → §4.2 (composizione corretta: **#245a62, 2,26:1** — il round 1 diceva #22535b e
2,05:1 e aveva torto) · 17 → §4.2 (`--contact` **cancellato**; il test citato non esiste, verificato:
l'unica asserzione `box-shadow` in `tests/frontend/test_design_docs.py:794` riguarda l'anello di
focus) · 18 → §4.6.

### SEGNALI «CHEAP» — vedi §3-bis per la risposta di merito

1 → §3-bis (la pila è cambiata, non difesa) · 2 → §4.7 · 3 → `--contact` cancellato ·
4 → `.tide` come elemento e come linea continua è cancellato · 5 → §4.3 (nessuna cucitura) ·
6 → la luce non si muove più, perché niente si muove · 7 → §4.6 · 8 → §3-bis e §5.

---

## 1. VERDETTO SULLO STATO ATTUALE (rimisurato il 24.09)

**1.1 — La home ha tre fondi in 7 921 px, e due di essi non si distinguono.**
Colonna `x=20` campionata ogni 40 px fra `y=1050` e `y=7290` (157 campioni): **tre soli valori**,
`#f4f3f0` ×**112**, `#ecebe6` ×26, `#0e1b23` ×19 (il round 1 scriveva 111: ricontato). Rapporto fra
i due fondi di carta **1,076:1**; fra `--min-0` e `--min-2` **1,064:1**. `layout.css:143` dichiara
*«Ground changes ARE the composition: no page ships with a single ground»*: sulla home quel cambio
esiste nel CSS e non sullo schermo.

**1.2 — La FAQ è una pagina intera senza un solo cambio di superficie.**
`/fr/faq/`, 2 211 px: `background-image` contiene `gradient` **zero** volte su tutto il documento;
l'unico elemento con un `background-color` proprio è il piè di pagina. Idem glossario, note legali,
avvertenze, contatti.

**1.3 — Il confine fra capitolo di carta e capitolo mezzanotte è una riga di gesso — e ha due
origini, non una.** Campionamento a `x=40` e `x=700` su uno screenshot a piena pagina a 1440:
`y=1001` (hero→entrances), `y=3518` (pathways→pilot), `y=4268` (pilot→trust), `y=5270`
(trust→antifraud): in tutti e quattro il pixel di confine è **`#d3d2cc`**, esattamente uno.
`#d3d2cc` su `#0e1b23` vale **11,55:1**: su un dislivello di **15,78:1** il sistema disegna una
linea più chiara del fondo scuro di undici volte. Non separa, graffia.
**Correzione al round 1:** le origini sono **due**, e il round 1 ne citava una sola.
- `apps/pages/static/pages/css/pages.css:47-49` produce `y=3518`, `y=4268`, `y=5270`;
- `static/css/components.css:1188-1192` — `.hero { border-block-end: var(--border-width) solid var(--border-hairline) }` — produce `y=1001`, e `entrances` ha `border-block-start-width: 0px` (misurato, e confermato via CDP `CSS.getMatchedStylesForNode`).
Cancellare solo la prima regola, come chiedeva il round 1, avrebbe lasciato in pagina il filetto del
confine più visibile della home.

**1.3-bis — E c'è un quinto confine, che oggi non ha né filetto né rampa.**
`home-reserved` finisce a `y=7196`; `.site-footer` comincia a `y=7292`; in mezzo ci sono **96 px di
`--min-0`** (campionati: `#f4f3f0` da y=7288 a y=7291) e poi, senza transizione, `#0a151c`. È un
salto di **16,65:1** senza alcun segno. Il round 1 non lo aveva visto.

**1.4 — Fuori dall'hero non esiste un solo gradiente su tutta la home.**
Censimento esatto: **nove** elementi portano un `background-image` con un gradiente —
`doorway__arch` 192 529 px², `doorway__overlay` 190 760, `doorway__glow` 20 022, tre
`jurisdiction__segment` (6 687 + 6 687 + 4 446) e tre `jurisdiction__swatch` (192 ×3). Totale
**421 707 px²** su 11 406 240, cioè **3,70 %** (il round 1 diceva 416 685 px² / 3,65 % e contava
cinque elementi su nove). Tutto sta nei primi 1 002 px; per i restanti **6 919 px, l'87 % della
pagina**, nessuna luce, nessuna profondità, nessuna materia.

**1.5 — La piattaforma è monocroma al 95 %.**
Censimento della colonna `x=8` ogni 4 px su `docs/design-v2/before/*_desktop.png`: `person_dashboard`
(3 599 px) **95 %** un solo valore · `case_file` (3 286 px) **95 %** · `company_dashboard` (1 649 px)
**96 %** · `orientation` (1 706 px) **96 %**. Il fascicolo, il cruscotto e il wizard non hanno né
foglio, né rail, né canvas: hanno filetti su una tinta.

**1.6 — Il FORUM usa il tricolore come fondo di sezione in DUE punti, non in uno.**
Misurato su `/fr/forum/` a 1440:
- `header.forum-hero` — `background-color: rgb(15, 37, 71)` = `--brand-navy`, **alto 388 px** (`apps/forum/static/forum/forum.css:24-25`);
- `section.forum-cta` — stesso colore, alto 176 px (`forum.css:141`).

Il round 1 nominava solo il secondo. §1.3-4 dice che il tricolore vive **solo nel marchio**.
In più, due fondi che non sono fondi: `.forum-section--accent` (`forum.css:104`) e `.forum-cta`
sono entrambi `.container`, cioè si fermano a 1 320 px e hanno `border-radius` — §1.3-5 dice che il
confine di capitolo «è un confine di sezione con transizione di sfondo, **non un box**».
Conteggio dei capitoli mezzanotte del FORUM secondo la regola della DEROGA 2 (dentro `<main>`,
la cornice non conta): oggi **due** fondi scuri dentro `main` (hero navy + CTA navy) — dentro il
tetto di due, ma del colore sbagliato.

**1.7 — La graticola esiste, è bella, e vive in un solo posto.** `scripts/territory.py` produce un
reticolo a modulo 160 px con tacche e due strati di isoipse, e `hero.css` lo usa **solo dentro
`.hero`**: il linguaggio proprietario del progetto è confinato a 900 px su 7 921.

**1.8 — Nessun template dichiara `data-mode`** (`templates/base.html:45` → `<body class="…">`, nessun
attributo), benché DESIGN_SYSTEM_V2 §7 lo dia per normativo. E a 390×844 i fondi sono gli stessi tre
valori: non c'è nulla da degradare, perché non c'è nulla.

**1.9 — Lo spazio verticale che la soglia userà esiste già, e ha un nome.** Misurato a
1440/768/390 su entrambe le build: `.section--b` = **96/64/48** px di `padding-block-start`,
`.section--c` = **48/32/32**, `.section--d` = **32/24/24**, `.hero` = **96/61,44/48**
(`clamp(48px, 8vw, 96px)`, `components.css:1190`), `.home-pilot.chapter--dark` = **96/96/96**
(`--s-24` letterale, `voyage.css:13`), `.site-footer` = **48/48/48** (`--s-12`, `shell.css:381`) più
un `margin-block-start` di **96/64/48**, `.home-banner` e `.home-reserved` = **0**.
Questa tabella è il motivo per cui la soglia non aggiunge un pixel (§4.2).

---

## 2. UI-UX-PRO-MAX — interrogazioni e verdetti

| # | Query esatta (`--domain`) | Ritorno (condensato) | Esito |
|---|---|---|---|
| 1 | `layered background gradients mesh depth premium section surfaces` (`style`) | `aurora-ui` (mesh gradient, loop 8-12 s, `filter: saturate(1.2)`, `blend-mode: screen`); `glassmorphism` (`backdrop-filter: blur(15px)`); `skeuomorphism` (gradienti a 8-12 stop, overlay di grana, ombre multistrato) | **RIFIUTATO ×2, ACCETTATO ×1.** Aurora = la «SaaS purple wash» vietata dal brief, e `filter: saturate()` su area grande viola il budget. Glassmorphism = `backdrop-filter` consentito **solo** sull'header scrollato (§2 livello 6). Da skeuomorphism prendo **una cosa sola**: la grana come materia, e i gradienti **multi-stop invece che a due stop**. Rifiuto il resto (ombre realistiche, rilievi, legno/pelle). Il rilievo interno che il round 1 aveva preso (`--contact`) è **cancellato**: era il bisello del 2010. |
| 2 | `dark section transition light to dark band boundary scroll` (`ux`) | `scroll-behavior: smooth`; evitare scroll orizzontale; stato attivo in navigazione | **RIFIUTATO — e il corpus è muto.** Nessun risultato pertinente: il corpus UX non possiede alcun vocabolario per il confine fra due capitoli. Registrato come lacuna del corpus, non come licenza. |
| 3 | `noise grain texture paper material surface elevation` (`color`) | Un solo risultato, `White Noise & Ambient Sound` (palette indaco su `#0F172A`) — coincidenza lessicale su «noise» | **RIFIUTATO.** Nessuna palette esterna entra: i token V2 sono vincolanti. |
| 4 | `institutional government legal platform premium background surface` (`--design-system`) | Pattern **Scroll-Triggered Storytelling** («pause scroll animation when offscreen», «render each chapter in its final readable state under reduced motion»); stile **Liquid Glass**; palette nero+oro; Cormorant/Montserrat da Google Fonts | **ACCETTATO il pattern, RIFIUTATO tutto il resto.** Il pattern conferma la struttura a capitoli. Liquid Glass rifiutato (CSP + `blur` su area grande). Font da CDN rifiutati (`style-src 'self'`). Palette rifiutata. |
| 5 | `scroll linked background color change section pinning parallax performance` (`gsap`) | Parallax «Subtle»: `yPercent 5-15`, `scrub`; «mai parallasse sul corpo del testo»; «`will-change: transform` solo sullo strato e rimuoverlo a scroll fermo» | **NON PIÙ APPLICABILE.** Nel round 1 adottavo queste regole per `graticola-deriva`. Quel moto è cancellato (§5): non c'è alcuno strato di parallasse da governare. La regola resta scritta come divieto: nessun fondo di questo sistema si muove. |
| 6 | `swiss editorial cartographic archive blueprint grid texture` (`style`) | `editorial-grid-magazine` — griglia asimmetrica, capilettera, `cost:low`, `risk:low` | **RIFIUTATO.** È la direzione editoriale che il proprietario ha respinto il 23.09. La cito per dire che il corpus non contiene «cartografico»: quel linguaggio è nostro (`scripts/territory.py`). |

**Dove il corpus ha torto.** Alla query 4 lo strumento offre «government = accessibile ed etico,
evita gli effetti di moto». Il fondo che propongo non introduce **nessun** moto su nessun modo, ed è
quindi più conservativo del suo consiglio. Ma non uso quella prudenza come argomento: il §3-bis
spiega dove sta il progetto, e il §5 spiega perché la cosa viva della pagina non è il fondo.

---

## 3. 21ST.DEV — candidati confrontati

Sette candidati reali, tre studiati nel codice (`get_component` su 1537, 1468, 5293). Nessuno
installato: React + Tailwind + `style={{}}` inline sono incompatibili con Django SSR e con
`style-src 'self'`. Si estrae il **pattern**.

| # | Componente · URL | Che cosa prendo | Che cosa rifiuto |
|---|---|---|---|
| 1 | **Dot Pattern** (MagicUI / dillionverma) · id 1537 — *codice letto* | **Il motivo non finisce, viene mascherato** — `mask-image` sul livello del motivo. È ciò che trasforma una texture in atmosfera. Adottato, **ma la maschera è verticale e non radiale** (§3-bis). | `<svg><pattern>` in React con `useId()`; `fill-neutral-400/80` (colore fuori token). |
| 2 | **Card with Noise Pattern** (Ali-Hussein-dev) · id 1468 — *codice letto* | La grana come **filtro SVG `feTurbulence` piastrellato**, sotto un velo semitrasparente. Il principio: la grana è alfa, non colore. | Il tassello da 500 px (200 px bastano); `bg-zinc-950` in classe; «optimized for dark mode only»; l'entrata in Framer Motion su un fondo. |
| 3 | **Dark Gradient Background** (jatin-yadav05) · id 5293 — *codice letto* | La **struttura a pila**: fondo → grana → disegno → ognuno su `inset:0` con la propria opacità. | Il gradiente a 5 stop `#000 → #22d3ee`; la grana **hotlinkata** da `cdn.21st.dev` (CSP); quattro `style={{}}` inline; lo strato diagonale a 45°. **E la griglia ortogonale a campo pieno** — vedi §3-bis. |
| 4 | **Grid Background** (meghtrix) | Che griglia + grana insieme leggono come *materiale*, mentre la griglia da sola legge come *tabella*. È la ragione per cui la grana non è opzionale. | **La griglia stessa.** Vedi §3-bis: è il pezzo che ho tolto. |
| 5 | **Dot Grid** (paper-design, Paper Shaders) | Niente, se non la conferma che la qualità percepita del riferimento 2026 sta nel **campo** e non nel singolo elemento. | **WebGL.** Un contesto GL per tutta la pagina per disegnare dei punti è l'opposto del rapporto costo/valore che cerchiamo. |
| 6 | **Mesh Gradient Shader** (nlace-com) | Niente. | WebGL + palette a 4 colori estranei: la «SaaS purple wash» nominata nel brief. |
| 7 | **Background Gradient Animation** (Aceternity) | Niente, ma è il **controesempio utile**: è il fondo più copiato del 2024-25 e oggi legge come template. | Blob animati in `background-position`, `filter: blur()` in loop: due divieti espliciti di MOTION_SYSTEM §2. |

### 3-bis. LA CRITICA CHE VALE PIÙ DI TUTTE LE ALTRE

Il revisore scrive: *«la pila che la specifica spedisce — fondo piatto + rumore + griglia ortogonale
+ un bagliore radiale d'angolo — **è** la ricetta jatin-yadav05/meghtrix, la formula di fondo scuro
più copiata del 2024-25. L'unico differenziatore dichiarato è che il modulo è 160 px per coincidere
con `scripts/territory.py` — una corrispondenza che nessuno può percepire al 2,8 % di opacità sotto
una maschera radiale.»*

**Ha ragione, e non è difendibile.** Un modulo che coincide con un'altra cosa che nessuno vede non è
una decisione di progetto, è una nota a piè di pagina. Nel round 2 due dei quattro strati sono
cambiati, e sono cambiati perché quella ricetta è sbagliata per questo prodotto, non perché è
copiata.

**Che cosa se ne va.**
1. **Il bagliore radiale d'angolo.** Un radiale che scalda un angolo è il tell più riconoscibile del
   fondo generato. Sparisce del tutto.
2. **La griglia ortogonale a campo pieno.** Una maglia uniforme e infinita, sfumata ai bordi, è
   esattamente il riferimento 3 e 4. E dice la cosa sbagliata: la carta nautica non ha una maglia in
   mezzo al foglio — ha il foglio **vuoto** e il **margine graduato**.

**Che cosa arriva al loro posto, e perché è nostro.**
1. **La graticola diventa un apparato di margine.** Due filetti di neat line all'altezza esatta del
   bordo della colonna di testo, e fuori di essi una **graduazione**: tacche di minuto ogni
   `--grat-module / 4` lunghe 8 px, tacche di grado ogni `--grat-module` lunghe metà fascia. È
   l'inverso della ricetta 2024-25 — densa al margine, vuota al centro — e risolve da sé il rischio
   «legge come una tabella», perché **non attraversa mai il testo**. La fascia in cui vive esiste già
   ed è misurata: `calc((100% − min(100%, var(--container))) / 2 + var(--grid-margin))` =
   **100 px a 1440, 52 px a 1200, 40 px a 768, 20 px a 390** — cioè il margine tipografico del sito,
   non un valore inventato.
2. **La luce non è più un campo, è un bordo.** Al confine, sul primo pixel del nuovo capitolo, una
   banda di 16 px che decade a zero. È la luce che prende il **filo del foglio posato sopra un
   altro**. Ha una causa fisica, non è un'atmosfera; e poiché vive sullo strato della soglia, non può
   «scivolare con la superficie che illumina» (segnale cheap 6): non si muove niente.
3. **Il segno del confine non è una linea che attraversa la pagina.** È una tacca di graduazione: un
   filetto di 1 px che corre **solo dentro la fascia di margine**, su entrambi i lati, e si ferma
   contro la neat line formando un angolo a T. A 1440 sono due segni da 100 px su una pagina larga
   1 440. Non può diventare il «divisore teal che si disegna» del 2021-23, perché non attraversa la
   pagina, non è continuo e non si anima.

Il modulo resta 160 px perché è quello della graticola dell'hero, ma **quella non è più la
giustificazione**: la giustificazione è che ogni capitolo di questo sito, d'ora in poi, ha il
margine di una carta e non il bordo di un `<div>`. Questo si vede — e si vede soprattutto sulle
pagine che oggi non hanno niente (§1.2, §1.5).

**Sul «niente è dinamico».** Il revisore ha ragione anche qui, e ha ragione che la staticità non si
può difendere invocando il registro istituzionale. Ma la diagnosi era sbagliata. Misurato:
`/fr/parcours/`, `/fr/entreprises/`, `/fr/institutions/`, `/fr/universites-et-formation/`,
`/fr/forum/` e `/fr/faq/` hanno **0 animazioni, 0 gradienti su tutto il documento, e un solo
`background-color` proprio in tutta la pagina — il piè di pagina.** Ciò che rende quelle pagine
morte non è l'assenza di moto: è che sono una tinta. Il rimedio di questo documento è la materia e
la soglia. Il moto che quelle pagine meritano **non è del fondo**: il fondo che si muove da solo è
la definizione del decorativo. Le voci di moto restano dove hanno un autore — l'hero, la rotta, il
rail — e sono di altre specifiche (`hero-doorway.md`, `scroll.md`, `platform-shell.md`). Questo
documento **non chiede nessuna quota di moto**, e la lascia intera a chi ne ha una da spendere.

---

## 4. LA PROPOSTA — «la materia»

Principio: **il fondo non è una tinta, è un materiale con un margine, e il passaggio da un materiale
all'altro è un evento con un'altezza.** Quattro strati, un contratto di modalità, una soglia che
nessuno scrive a mano.

### 4.1 Anatomia di un capitolo (dal basso)

```
0 GROUND    background-color         il token del capitolo (--min-0/1/2, --mid-0/1)
1 SOGLIA    background-image ×4      la rampa (alta --th) + la banda di luce + due tacche di confine
2 ::before  z-index -2               l'apparato di margine: 2 neat line + 4 colonne di graduazione
3 ::after   z-index -1               la grana: colore pieno mascherato dalla turbolenza, 3,5 / 5 %
  contenuto  z-index auto            non toccato: nessuna regola tocca i figli di .ground
```

Gli strati 1-3 sono `pointer-events: none`, non entrano nell'albero di accessibilità, **non si
animano mai** e non promuovono alcun livello di compositing.

> **Perché i pseudo-elementi hanno `z-index` negativo e non positivo.** Il round 1 scriveva
> `.ground > * { position: relative; z-index: 2 }` per tenere il contenuto sopra gli strati. È una
> riga che rompe la pagina: applicata all'hero, trasforma i tre `svg.hero__territory`
> (`position: absolute; z-index: -1`) in elementi `position: relative`, che rientrano nel flusso.
> Misurato: l'hero passa da **899 px a 3 359 px** e la home da 7 917 a 10 277. La soluzione corretta
> è `isolation: isolate` su `.ground` e `z-index: -2 / -1` sui due pseudo-elementi: il contenuto non
> viene toccato affatto. Per l'hero, che porta già il proprio disegno, serve **una sola riga in
> `v2/hero.css`**: `.hero__territory { z-index: -3 }`, e l'hero riceve `ground--bare` (nessun
> apparato di margine: ha la propria graticola).

### 4.2 Token e misure

Tutti i rapporti sono ricalcolati in questo round. Quelli che il round 1 aveva sbagliati sono
segnati **[corretto]**.

| Token | Valore | Verifica (WCAG 2.x, calcolata e ri-campionata) |
|---|---|---|
| `--min-edge` | `#e4e2db` | fondo della rampa chiara (DEROGA 3). `--ink` **12,52:1** · `--ink-2` **5,53:1** · `--ink-3` **4,74:1** · `--accent` **4,87:1** · `--accent-hover` **6,56:1** · `--accent-ring` **3,17:1** · `--err-700` **5,04:1**. vs `--min-0` = 1,168:1 |
| `--mid-edge` | `#16272f` | cima del capitolo mezzanotte (DEROGA 3). `--on-dark` **13,63:1** · `--on-dark-2` **8,51:1** · `--on-dark-3` **5,66:1** · `--accent-dark` **8,80:1** · `--terr-line` **5,34:1**. vs `--mid-1` = 1,138:1 |
| `--th-descent-mid` | `color-mix(in oklab, var(--min-edge) 34%, var(--mid-edge))` → **`#556165`** | stop mediano della discesa. Fallback non-oklab (sRGB): **`#5c6769`** |
| `--th-ascent-mid` | `color-mix(in oklab, var(--mid-edge) 62%, var(--min-edge))` → **`#5d686b`** | stop mediano della risalita. Fallback sRGB: **`#646e70`** *(il round 1 non lo dava)* |
| `--th-fold-mid` | `color-mix(in oklab, var(--min-0) 55%, var(--min-edge))` → **`#edebe7`** | stop mediano della piega. Fallback sRGB: **`#edebe7`** (identico) |
| `--grat-rule` | `rgb(15 106 114 / .30)` carta · `rgb(63 166 175 / .30)` mezzanotte | la neat line. Composita **#afcaca su `--min-0`, 1,561:1**; **#1d454d su `--mid-1`, 1,676:1**. Riferimento: il filetto che sostituisce, `--hairline` su `--min-0`, vale 1,365:1 |
| `--grat-ink` | `rgb(15 106 114 / .22)` carta · `rgb(63 166 175 / .22)` mezzanotte · `/ .16` su `--mid-0` | le tacche. Composita **#c2d5d4, 1,375:1** su carta; **#193a42, 1,438:1** su mezzanotte |
| `--grat-module` / `--grat-step` / `--grat-tick` | `160px` (`96px` < 48rem) · `module/4` · `--s-2` (8px) | grado / minuto / lunghezza della tacca di minuto. La tacca di grado è `--grat-margin / 2` |
| `--grat-margin` | `calc((100% − min(100%, var(--container))) / 2 + var(--grid-margin))` | **misurato: 100 px @1440 · 52 px @1200 · 40 px @768 · 20 px @390.** È il margine tipografico del sito: l'apparato non entra mai sotto il testo |
| `--grain-ink` / `--grain-amount` | `#15222a` / `.035` carta · `#cfe0e2` / `.05` mezzanotte | **misurato sullo screenshot del candidato: σ del canale verde 1,003 sulla carta, 1,331 sul mezzanotte, 1,458 sul piè di pagina — contro 0,000 oggi.** Composizione estrema: 1,067:1 sulla carta, 1,118:1 sul mezzanotte: la grana non porta mai informazione |
| `--grain-tile` | `200px` | il tassello dell'SVG |
| `--lume` | discesa/piega chiara `rgb(255 255 255 / .55)` · risalita `rgb(238 242 241 / .12)` · piega scura `rgb(238 242 241 / .06)` | **Regola: la luce è sempre il colore di testo del proprio capitolo a bassa alfa, mai una tinta.** `--accent-dark` non compare. Ampiezza di picco misurata: **+12,8 punti di luminanza relativa** sul filo chiaro (una riga), **+1,7 punti** sul filo scuro, su una banda di **16 px** (`--lume-fall: --s-4`; 8 px sulle pieghe) |
| `--tide` | `var(--terr-line-lt)` in discesa · `var(--terr-line)` in risalita · `transparent` sulle pieghe | la tacca di confine, **larga solo `--grat-margin`**, alta 1 px, su entrambi i lati. Campionata: **#136c74** su carta (**4,20:1** sul fondo), **#3ea4ad** su mezzanotte (**6,07:1**). `--terr-line` è grafica (§1.3-2): non è testo, non è un controllo, e non attraversa la pagina |
| `--material` | `1` · `0` in DENSE, LEGAL, `prefers-contrast: more`, `.ground--flat` | lo scalare ereditato che spegne materia e luce senza poter essere battuto da nessuna specificità (§4.3) |
| ~~`--contact`~~ | — | **CANCELLATO.** Era il bisello 2010, e la sua giustificazione («per non rompere il test `grep box-shadow`») citava un test che non esiste: verificato, l'unica asserzione `box-shadow` di `tests/frontend/test_design_docs.py` è alla riga 794 e riguarda l'anello di focus. Il foglio usa `--shadow-2` **solo in hover**, come prescrive DESIGN_SYSTEM_V2 §2, e nessun quinto ruolo entra |

**Composizione corretta [corretto].** `--terr-line` a α.45 su `--mid-1` dà **`#245a62`, 2,26:1** —
non `#22535b` / 2,05:1 come scriveva il round 1. Nel round 2 la tacca di confine non usa più
un'alfa: usa il token pieno (6,07:1 su mezzanotte, 4,20:1 su carta), perché è **corta** e può
permettersi di essere netta.

**La tabella rango → soglia (MUST-FIX 3).** `--th` non è mai un numero scritto a mano:

```
--th = min(--th-ideale, --th-room)      --th-ideale = --s-24 (96px) su discesa e risalita
                                                     = --s-12 (48px) sulle pieghe
```

| Selettore che porta `.ground` | `--th-room` | 1440 | 1200 | 768 | 390 | `--th` risultante (1440/768/390) |
|---|---|---|---|---|---|---|
| `.hero` (primo capitolo, nessun predecessore) | `0px` | 0 | 0 | 0 | 0 | **0 / 0 / 0** |
| `.section` senza rango, `.section--b` | `--rank-b-block` | 96 | 96 | 64 | 48 | risalita **96 / 64 / 48** |
| `.section--c` | `--rank-c-block` | 48 | 48 | 32 | 32 | piega **48 / 32 / 32** |
| `.section--d` | `--rank-d-block` | 32 | 32 | 24 | 24 | piega **32 / 24 / 24** |
| `.home-pilot` (`--s-24` letterale, `voyage.css:13`) | `--s-24` | 96 | 96 | 96 | 96 | discesa **96 / 96 / 96** |
| `.site-footer` (§4.5, il margine diventa padding) | `calc(--rank-b-block + --s-12)` | 144 | 144 | 112 | 96 | discesa **96 / 96 / 96** |
| `.forum-cta` (§4.9, idem) | `calc(--s-8 + clamp(1.5rem,4vw,2.5rem))` | 72 | 72 | ~60 | 56 | discesa **72 / ~60 / 56** |
| `.ground:not(.section)` — `_banner`, `_reserved` | `0px` | 0 | 0 | 0 | 0 | **0 / 0 / 0** |

**Prova, non affermazione.** Applicato il foglio candidato alla home reale servita da
`127.0.0.1:8771` e `:8770` e misurato, per ogni `.ground`, `offsetTop` del primo figlio contro il
valore *risolto* di `--th`:

> **0 sconfinamenti** su 10 sezioni × 4 larghezze × 2 build (Fase 3 aperta e chiusa), più
> **zoom 200 %** (viewport CSS 720 px) e **zoom 400 %** (360 px), più `dir="rtl"`.
> In ogni caso misurato `offsetTop == --th` esatto, cioè la soglia occupa il padding che la sezione
> ha già e **non un pixel in più**.

E la prova indipendente: l'altezza del documento passa da **7 921 px a 7 917 px** a 1440, cioè
**−4 px** — esattamente i quattro filetti da 1 px che il documento cancella. Nessuna altezza
aggiunta, nessuna altezza tolta oltre quella.

> `--th` è dichiarato con `@property … syntax:"<length>"`. Senza registrazione,
> `getComputedStyle(el).getPropertyValue('--th')` restituisce la stringa `min(48px, 96px)` e il test
> del §6 non può leggerla. Con la registrazione restituisce `48px`. Questo è il motivo tecnico dei
> quattro `@property` in testa al file, non una preferenza di stile.

### 4.3 Il file — `static/css/v3/ground.css`

`@import url("v3/ground.css");` in coda a `static/css/main.css`, dopo `v3/buttons.css`.
**3 542 → 9 495 B raw, 2 304 B gzip** (misurati, §7).

```css
/* ============================================================================
   GROUND V3 — «la materia, non la tinta» · docs/design-v3/specs/backgrounds.md
   ========================================================================== */

/* Registrati perché --th deve COMPUTARE a una lunghezza: il test del §6 la legge,
   e min()/calc() non si risolvono su una custom property non registrata. */
@property --th        { syntax: "<length>"; inherits: false; initial-value: 0px }
@property --th-room   { syntax: "<length>"; inherits: false; initial-value: 0px }
@property --lume-fall { syntax: "<length>"; inherits: false; initial-value: 0px }
/* Lo scalare della materia: ereditato, letto al punto d'uso, quindi nessuna
   specificità lo può battere. È questo il kill-switch, non una regola. */
@property --material  { syntax: "<number>"; inherits: true;  initial-value: 1 }

:root{
  --min-edge:#e4e2db;
  --mid-edge:#16272f;
  --th-descent-mid:color-mix(in oklab, var(--min-edge) 34%, var(--mid-edge));
  --th-ascent-mid: color-mix(in oklab, var(--mid-edge) 62%, var(--min-edge));
  --th-fold-mid:   color-mix(in oklab, var(--min-0)   55%, var(--min-edge));
  --grat-module:160px;
  --grat-step:calc(var(--grat-module) / 4);
  --grat-tick:var(--s-2);
  --grat-ink:rgb(15 106 114 / .22);
  --grat-rule:rgb(15 106 114 / .30);
  --grain-ink:#15222a; --grain-amount:.035; --grain-tile:200px;
  --ground:var(--min-0); --ground-prev:transparent;
  --th-mid:transparent; --th-end:transparent;
  --lume:transparent; --tide:transparent;
}
@supports not (color: color-mix(in oklab, #fff 50%, #000)){
  :root{ --th-descent-mid:#5c6769; --th-ascent-mid:#646e70; --th-fold-mid:#edebe7 }
}
@media (max-width:47.999rem){ :root{ --grat-module:96px } }

/* ---- 0 GROUND + 1 SOGLIA — un solo elemento porta fondo e soglia ---------
   Quattro strati, tutti ancorati in alto a y=0, tutti no-repeat:
   1-2 le due tacche di confine, larghe SOLO la fascia di margine;
   3   la banda di luce sul filo del nuovo materiale;
   4   la rampa, alta --th. L'ultimo stop è var(--ground) e NON transparent:
       interpolare verso `transparent` passa per il nero premoltiplicato e
       produce un avvallamento (misurato: −6 livelli di verde a 96px). */
.ground{
  position:relative; isolation:isolate;
  --grat-margin:calc((100% - min(100%, var(--container))) / 2 + var(--grid-margin));
  background-color:var(--ground);
  background-image:
    linear-gradient(var(--tide), var(--tide)),
    linear-gradient(var(--tide), var(--tide)),
    linear-gradient(to bottom, var(--lume) 0, transparent 100%),
    linear-gradient(to bottom, var(--ground-prev) 0, var(--th-mid) 46%, var(--th-end) 78%, var(--ground) 100%);
  background-size:
    var(--grat-margin) 1px, var(--grat-margin) 1px,
    100% calc(var(--lume-fall) * var(--material)), 100% var(--th);
  background-position: left 0 top 0, right 0 top 0, left 0 top 0, left 0 top 0;
  background-repeat:no-repeat;
}

/* ---- 2 ::before — l'apparato di margine ---------------------------------
   Due neat line al bordo esatto della colonna di testo, e fuori di esse la
   graduazione: tacche di minuto (--grat-step, lunghe --grat-tick) e tacche di
   grado (--grat-module, lunghe metà fascia). La maschera parte da `transparent`
   a y=0: l'apparato NON comincia mai con un bordo netto, quindi non esiste la
   cucitura orizzontale che il round 1 produceva a y=--th.
   Le posizioni sono fisiche ma perfettamente SIMMETRICHE (left + right con gli
   stessi valori): in dir=rtl la composizione è identica a sé stessa, e per
   background-position non esiste equivalente logico. */
.ground::before{
  content:""; position:absolute; inset:0; z-index:-2; pointer-events:none;
  opacity:var(--material);
  background-image:
    linear-gradient(var(--grat-rule), var(--grat-rule)),
    linear-gradient(var(--grat-rule), var(--grat-rule)),
    repeating-linear-gradient(to bottom, var(--grat-ink) 0 1px, transparent 1px var(--grat-step)),
    repeating-linear-gradient(to bottom, var(--grat-ink) 0 1px, transparent 1px var(--grat-step)),
    repeating-linear-gradient(to bottom, var(--grat-ink) 0 1px, transparent 1px var(--grat-module)),
    repeating-linear-gradient(to bottom, var(--grat-ink) 0 1px, transparent 1px var(--grat-module));
  background-repeat:no-repeat;
  background-size:
    1px 100%, 1px 100%,
    var(--grat-tick) 100%, var(--grat-tick) 100%,
    calc(var(--grat-margin) / 2) 100%, calc(var(--grat-margin) / 2) 100%;
  background-position:
    left var(--grat-margin) top, right var(--grat-margin) top,
    left calc(var(--grat-margin) - var(--grat-tick)) top,
    right calc(var(--grat-margin) - var(--grat-tick)) top,
    left 0 top, right 0 top;
  -webkit-mask-image:linear-gradient(to bottom, transparent 0, #000 var(--s-24), #000 calc(100% - var(--s-16)), transparent 100%);
          mask-image:linear-gradient(to bottom, transparent 0, #000 var(--s-24), #000 calc(100% - var(--s-16)), transparent 100%);
}
/* Un capitolo che porta già il proprio disegno (l'hero, una lastra fotografica). */
.ground--bare::before{ content:none }

/* ---- 3 ::after — la grana ------------------------------------------------
   SOLO longhand: lo shorthand `mask` azzera mask-mode a match-source, e la
   dichiarazione `mask-mode: alpha` del round 1 era morta (verificato). */
.ground::after{
  content:""; position:absolute; inset:0; z-index:-1; pointer-events:none;
  background-color:var(--grain-ink);
  opacity:calc(var(--grain-amount) * var(--material));
  -webkit-mask-image:url("../../img/v3/grain.svg"); mask-image:url("../../img/v3/grain.svg");
  -webkit-mask-repeat:repeat; mask-repeat:repeat;
  -webkit-mask-size:var(--grain-tile) var(--grain-tile); mask-size:var(--grain-tile) var(--grain-tile);
  mask-mode:alpha;
}
/* Il guard giusto è mask-mode, non mask-image: un motore può supportare
   mask-image e non mask-mode, ed è quel caso che ci preoccupa. */
@supports not (mask-mode:alpha){ .ground::after{ display:none } }

/* ---- CHE COSA È UN CAPITOLO --------------------------------------------- */
.ground--paper   { --ground:var(--min-0) }
.ground--area    { --ground:var(--min-1) }
.ground--sheet   { --ground:var(--min-2) }
.ground--midnight{ --ground:var(--mid-1); color:var(--on-dark);
  --grat-ink:rgb(63 166 175 / .22); --grat-rule:rgb(63 166 175 / .30);
  --grain-ink:#cfe0e2; --grain-amount:.05 }
.ground--utility { --ground:var(--mid-0); color:var(--on-dark-2);
  --grat-ink:rgb(63 166 175 / .16); --grat-rule:rgb(63 166 175 / .22);
  --grain-ink:#cfe0e2; --grain-amount:.05 }

/* ---- QUANTO SPAZIO HA LA SOGLIA (l'ordine conta) ------------------------ */
.ground{ --th-room:var(--rank-b-block) }
.ground:not(.section){ --th-room:0px }
.ground.section--c{ --th-room:var(--rank-c-block) }
.ground.section--d{ --th-room:var(--rank-d-block) }
.ground.section--a, .ground.section--flush-top{ --th-room:0px }
.ground.home-pilot{ --th-room:var(--s-24) }
.ground.site-footer{ --th-room:calc(var(--rank-b-block) + var(--s-12)) }

/* ---- DA DOVE VIENE: il fratello DOM che la precede ----------------------
   Le sezioni della home sono fratelli emessi da un ciclo su
   HomeSection.objects.visible() filtrato da section_gate_open()
   (apps/pages/services.py:634-668) e da PHASE3_ONLY_SECTIONS
   (apps/pages/content.py:103). Nessuna classe dice «vengo dal mezzanotte»:
   lo dice il DOM. Riordina, chiudi un gate, apri il banner — la rampa si
   ricuce da sola. */
.ground--paper    + .ground{ --ground-prev:var(--min-0) }
.ground--area     + .ground{ --ground-prev:var(--min-1) }
.ground--sheet    + .ground{ --ground-prev:var(--min-2) }
.ground--midnight + .ground{ --ground-prev:var(--mid-1) }
.ground--utility  + .ground{ --ground-prev:var(--mid-0) }

/* ---- CHE TIPO DI PASSAGGIO È ------------------------------------------- */
/* PIEGA — due materiali della stessa riva. Nessuna tacca: non è un capitolo nuovo. */
:is(.ground--paper,.ground--area,.ground--sheet) + :is(.ground--paper,.ground--area,.ground--sheet),
:is(.ground--midnight,.ground--utility) + :is(.ground--midnight,.ground--utility){
  --th:min(var(--s-12), var(--th-room));
  --th-mid:var(--th-fold-mid); --th-end:var(--min-edge);
  --lume:rgb(255 255 255 / .45); --lume-fall:var(--s-2); --tide:transparent }
:is(.ground--midnight,.ground--utility) + :is(.ground--midnight,.ground--utility){
  --th-mid:var(--mid-edge); --th-end:var(--mid-edge); --lume:rgb(238 242 241 / .06) }
/* DISCESA — carta, poi mezzanotte. Il filo illuminato è quello della carta. */
:is(.ground--paper,.ground--area,.ground--sheet) + :is(.ground--midnight,.ground--utility),
.site-footer.ground{
  --th:min(var(--s-24), var(--th-room));
  --th-mid:var(--th-descent-mid); --th-end:var(--mid-edge);
  --lume:rgb(255 255 255 / .55); --lume-fall:var(--s-4); --tide:var(--terr-line-lt) }
/* RISALITA — mezzanotte, poi carta. Il filo illuminato è quello del mezzanotte. */
:is(.ground--midnight,.ground--utility) + :is(.ground--paper,.ground--area,.ground--sheet){
  --th:min(var(--s-24), var(--th-room));
  --th-mid:var(--th-ascent-mid); --th-end:var(--min-edge);
  --lume:rgb(238 242 241 / .12); --lume-fall:var(--s-4); --tide:var(--terr-line) }
/* Il piè di pagina non è fratello delle sezioni (sta fuori da <main>): il suo
   predecessore è il fondo del corpo, campionato #f4f3f0 nei 96px sopra di lui.
   Il margine diventa padding: stessa altezza, ma la rampa ha dove stare. */
.site-footer.ground{ --ground-prev:var(--min-0);
  margin-block-start:0; padding-block-start:calc(var(--rank-b-block) + var(--s-12)) }

/* ---- 4 LA LASTRA — una fotografia che è diventata un fondo (§4.6) ------- */
.ground--plate{ overflow:clip }
.ground--plate::before{ content:none }
.ground__plate{ position:absolute; inset:0; z-index:-2; display:block; pointer-events:none }
.ground__plate img{ inline-size:100%; block-size:100%; object-fit:cover; object-position:50% 50% }
.ground__plate--upper img{ object-position:50% 22% }
.ground__plate--lower img{ object-position:50% 78% }
.ground--plate .ground__veil{ position:absolute; inset:0; z-index:-2; pointer-events:none;
  background-image:
    linear-gradient(to bottom, var(--ground) 0, rgb(14 27 35 / .22) var(--th), transparent 60%),
    radial-gradient(ellipse at 50% 42%, rgb(14 27 35 / 0) 24%, rgb(14 27 35 / .94) 100%) }

/* ---- STATI — solo dove il foglio È il controllo (§4.7) ------------------ */
.ground--sheet{ border:1px solid var(--hairline) }
a.ground--sheet, button.ground--sheet,
.ground--sheet:has(> a[href]), .ground--sheet:has(> * > a[href]){ cursor:pointer }
@media (prefers-reduced-motion: no-preference){
  a.ground--sheet, button.ground--sheet,
  .ground--sheet:has(> a[href]), .ground--sheet:has(> * > a[href]){
    transition: background-color var(--motion-fast) var(--ease-out),
                border-color     var(--motion-fast) var(--ease-out),
                box-shadow       var(--motion-fast) var(--ease-out),
                transform        var(--motion-instant) var(--ease-in) }
}
@media (hover: hover){
  a.ground--sheet:hover, button.ground--sheet:hover,
  .ground--sheet:has(> a[href]:hover), .ground--sheet:has(> * > a[href]:hover){
    --ground:var(--min-3); border-color:var(--hairline-strong); box-shadow:var(--shadow-2) }
}
a.ground--sheet:focus-within, button.ground--sheet:focus-within, .ground--sheet:focus-within{
  --ground:var(--min-3); border-color:var(--hairline-strong); box-shadow:var(--shadow-2) }
a.ground--sheet:active, button.ground--sheet:active,
.ground--sheet:has(> a[href]:active), .ground--sheet:has(> * > a[href]:active){
  --ground:var(--min-1); border-color:var(--hairline-strong); box-shadow:none;
  transform:translateY(1px) }
.ground--sheet[aria-disabled="true"], .ground--sheet:has([aria-disabled="true"]){
  --ground:var(--min-1); --grain-amount:0; border-color:var(--hairline);
  box-shadow:none; cursor:not-allowed }

/* ---- CONTRATTO DI MODALITÀ --------------------------------------------- */
[data-mode="dense"], [data-mode="legal"], .ground--flat{ --material:0 }
[data-mode="standard"] .ground--plate, [data-mode="dense"] .ground--plate,
[data-mode="legal"] .ground--plate{ display:none }

@media (prefers-contrast: more){ :root{ --material:0 } }

@media (forced-colors: active){
  .ground{ background-image:none !important; background-color:Canvas !important; color:CanvasText }
  .ground::before, .ground::after, .ground__plate, .ground--plate .ground__veil{ display:none }
  /* La composizione sopravvive come sequenza di sezioni separate da una riga di
     sistema: gli stessi selettori di fratello che definiscono un passaggio. */
  :is(.ground--paper,.ground--area,.ground--sheet,.ground--midnight,.ground--utility) + .ground,
  .site-footer.ground{ border-block-start:1px solid CanvasText !important }
  .ground--sheet{ border:1px solid CanvasText }
}
```

### 4.4 L'asset — `static/img/v3/grain.svg` (**326 B raw, 246 B gzip**, misurati)

Generato una volta da `scripts/grain.py` (seed fisso, come `territory.py`) e versionato:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><filter id="g" x="0" y="0"
 width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".82" numOctaves="3"
 seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect
 width="200" height="200" filter="url(#g)"/></svg>
```

È usato come **maschera**, non come immagine: il browser lo rasterizza una volta e il colore della
grana resta un token (scura sulla carta, chiara sul mezzanotte) con **un solo file**;
`stitchTiles="stitch"` elimina la cucitura fra i tasselli.

**Il difetto `mask-mode` del round 1 era reale, e la paura che lo accompagnava no.** Due misure
distinte, entrambe in Chromium 153:

1. *Il difetto.* `mask-mode: alpha` dichiarato **prima** dello shorthand `mask:` computa a
   **`match-source`** — la dichiarazione era morta. Dichiarato **dopo**, computa `alpha`. Nel round 2
   il problema non esiste perché **lo shorthand non viene usato**: solo longhand.
2. *La conseguenza.* Ho reso la stessa grana con `mask-mode: alpha`, `luminance` e `match-source` e
   ho campionato σ del canale verde su 6 400 pixel:

   | | `alpha` | `luminance` | `match-source` |
   |---|---|---|---|
   | carta (`--grain-amount .035`) | σ **1,017** | σ **0,965** | σ **1,017** |
   | mezzanotte (`.05`) | σ **1,363** | σ **1,071** | σ **1,363** |

   Un motore che legge la luminanza invece dell'alfa dà una grana **più debole del 5 % sulla carta e
   del 21 % sul mezzanotte — mai invertita.** La carta non diventa sporca, il mezzanotte non diventa
   lattiginoso: il rischio §8-7 del round 1 era sopravvalutato, e la voce di QA umana §6-2 è
   riscritta di conseguenza. `match-source` è identico ad `alpha` su questo asset, il che spiega
   perché il difetto del round 1 non si vedeva.

**Piano B** (solo per un motore senza `mask-mode`, dove `@supports` azzera la grana): PNG `LA`
96×96 = 8 498 B, stesso seed, stesso risultato.

### 4.5 I template e le regole legacy da cancellare

**Solo classi. Nessuna parola, nessun `alt`, nessun `aria-label`, nessuna stringa nuova**, e nessun
elemento decorativo nuovo: la tacca di confine è un layer di background, non un `<div>`. Il round 1
inseriva un `<div class="tide" aria-hidden>` come primo figlio di sei partial; quel `<div>` non
esiste più. `apps/cms/forbidden.py` non è toccato e non ha nulla da scansionare che prima non ci
fosse — l'unica eccezione possibile è §4.6, che ha la sua politica scritta.

| File | Modifica |
|---|---|
| `templates/base.html:45` | `<body class="… " data-mode="{% block page_mode %}standard{% endblock %}">` |
| `templates/pages/home/_hero.html:30` | aggiungere `ground ground--midnight ground--bare` (`chapter--dark` **resta**: è l'unico aggancio di `shell.css:483-486`, l'anello di focus su scuro) |
| `_banner.html:7` | `ground ground--area`. **Non è un caso ipotetico: su `:8770` il banner è renderizzato oggi**, fra hero ed entrances, `background rgb(236,235,230)`, `padding-block 0`, `border-block-start 2px`. Senza questa classe la catena di fratelli si spezza e `entrances` perde il predecessore |
| `_entrances.html` | `ground ground--paper` |
| `_orientation.html`, `_news.html` | `ground ground--area` (oggi lo fanno con `section--process`, che è uno shorthand `background` — vedi sotto) |
| `_pathways.html`, `_trust.html`, `_ecosystem.html` | `ground ground--paper` |
| `_pilot.html:22` | `ground ground--midnight` (`chapter--dark` resta) |
| `_antifraud.html` | `ground ground--area` — riceve una piega da 32/24/24 px per derivazione, senza che nessuno la scriva |
| `_reserved.html` | **nessuna classe `ground`.** `padding-block-start: 0` e contenuto dentro un pannello opaco: non c'è materia da mostrare. Invece `.home-reserved__panel` diventa **`ground ground--sheet`** — il foglio che avrebbe dovuto essere fin dall'inizio, con il suo bordo e i suoi stati (§4.7) |
| `templates/partials/footer.html:2` | `ground ground--utility` sul `<footer class="site-footer on-inverse">` |
| `templates/partials/portal_chrome.html` e §4.8 | la piattaforma |
| `templates/forum/partials/hero.html:7`, `templates/forum/partials/cta_row.html:8` | §4.9 |

**Le regole legacy da cancellare — e perché non basta la prima.** `.ground` usa i *longhand* di
background; ogni shorthand `background:` rimasto, a specificità pari o superiore, azzera
`background-size`, `background-position` e `background-repeat` e fa dipingere la rampa su tutta la
sezione. Verificato lasciandole in piedi: il capitolo `_pilot` diventa un campo teal pieno.

| File : riga | Dichiarazione | Azione |
|---|---|---|
| `apps/pages/static/pages/css/pages.css:47-49` | `.page-home .section:not(.section--process) + .section:not(.section--process){ border-block-start: 1px solid var(--rule-hair) }` | **cancellare** (produce i filetti a y=3518, 4268, 5270) |
| `static/css/components.css:1191` | `.hero{ border-block-end: var(--border-width) solid var(--border-hairline) }` | **cancellare** — è l'origine del filetto a y=1001, che il round 1 attribuiva a `pages.css`. `padding-block` della stessa regola (riga 1190) **resta**: è il rango dell'hero |
| `static/css/v2/hero.css:15` | `.hero{ background: var(--mid-1) }` | sostituire con `background-color` o cancellare: lo fornisce `.ground--midnight` |
| `static/css/v2/hero.css` (`.hero__territory`) | `z-index: -1` | → `z-index: -3`, così la grana sta sopra il territorio (§4.1) |
| `static/css/layout.css:144-146` | `.section--process{ background: var(--paper-deep) }` | **cancellare**: lo fornisce `.ground--area` |
| `static/css/v2/voyage.css:10-14` | `.home-pilot.chapter--dark{ background: var(--mid-1); padding-block: var(--s-24) }` | cancellare `background`; `padding-block` **resta** (è `--th-room` del pilot) |
| `static/css/v2/shell.css:375-382` | `.site-footer{ background: var(--mid-0); padding-block: var(--s-12) }` | cancellare `background`; `padding-block` resta, e il `margin-block-start` ereditato da `components.css:2776` viene azzerato e trasferito nel padding da `ground.css` (invarianza d'altezza verificata: contenuto del footer a y=7336 con il candidato, y=7340 oggi — i 4 px dei filetti cancellati) |
| `apps/pages/static/pages/css/pages.css:131-136` | `.home-banner{ background: var(--surface-2); border-block-start: 2px …; border-block-end: 1px … }` | cancellare i tre: il banner è un `ground--area` con la sua piega |
| `apps/pages/static/pages/css/pages.css:584-592` | `.home-reserved__panel{ background: var(--surface-1); border: …; border-radius: var(--radius-sm) }` | sostituire con `ground ground--sheet`; `border-radius` → 0 (DESIGN_SYSTEM_V2 §2: raggio 0 sui fogli) |
| `apps/forum/static/forum/forum.css:24-25, 104, 141` | §4.9 | |
| `apps/portal/static/portal/portal.css:21, 111, 262` | §4.8 | |
| `static/css/main.css` | `@import url("v3/ground.css");` in coda | |

### 4.6 La lastra — una fotografia che è diventata un fondo

Risponde al reclamo del proprietario («non abbastanza immagini eleganti moderne coerenti») ed è
**CSP-legale per costruzione**: l'URL dell'immagine non entra mai nel CSS. Vive negli attributi
`srcset`/`src`, che sono HTML e ricadono sotto `img-src`. Header CSP della build, misurato:
`img-src 'self' data:`. Nessun `style=""`, nessun foglio generato, nessuna custom property con
`url()`.

**Il markup, per esteso.**

```html
{# Una lastra è un capitolo mezzanotte la cui superficie è una fotografia. #}
<section class="section section--b ground ground--midnight ground--plate ground--bare"
         id="{{ s.anchor }}" aria-labelledby="{{ s.anchor }}-title" data-section="{{ s.key }}">
  <picture class="ground__plate ground__plate--upper" aria-hidden="true">
    <source type="image/avif"
            srcset="{{ d.plate.avif_480 }} 480w, {{ d.plate.avif_800 }} 800w, {{ d.plate.avif_1200 }} 1200w"
            sizes="100vw">
    <source type="image/webp"
            srcset="{{ d.plate.webp_480 }} 480w, {{ d.plate.webp_800 }} 800w, {{ d.plate.webp_1200 }} 1200w"
            sizes="100vw">
    <img src="{{ d.plate.webp_800 }}" alt="" width="1200" height="675"
         loading="lazy" decoding="async" fetchpriority="low">
  </picture>
  <div class="ground__veil" aria-hidden="true"></div>
  <div class="container"> … il capitolo, invariato … </div>
</section>
```

**I selettori** sono al §4.3 (`.ground--plate`, `.ground__plate`, `.ground__plate--upper/--lower`,
`.ground__veil`). Tre classi di inquadratura, **non** tre `style="object-position:…"`: il CMS
sceglie una classe da una lista chiusa, come già fa per le varianti dell'hero.

**Il velo** è due gradienti su un elemento proprio: (1) dal colore del capitolo alla trasparenza
attraverso `--th`, così **la lastra eredita la stessa soglia di tutti gli altri capitoli** e la
fotografia non comincia con un taglio netto; (2) la vignetta già esistente del `doorway__overlay`,
`radial-gradient(ellipse at 50% 42%, rgb(14 27 35 / 0) 24%, rgb(14 27 35 / .94) 100%)`. Sopra,
la grana del `::after` al 5 %: **qualunque fotografia atterra nella stessa materia del resto del
sito.**

**Il duotono è di build, non di redazione.** `scripts/duotone.py`, ombre `--mid-1` **#0e1b23**,
luci `--min-edge` **#e4e2db**. **Non** `--terr-line`: una fotografia virata al teal è precisamente
«un filtro applicato a una stock», che è il rischio che il revisore nomina. Ombre d'inchiostro e
luci di carta danno una **fotoincisione**, cioè la stessa coppia di materiali che regge tutto il
sito. AVIF + WebP a 480/800/1200, **≤ 120 KB per viewport**, `sizes="100vw"`.

**Direzione artistica — le regole di taglio, che mancavano del tutto.**
1. **Il terzo quieto.** Il testo del capitolo vive su un terzo dell'immagine in cui la deviazione
   standard della luminanza è < 12 su 255. Se nessun terzo lo è, la fotografia non è una lastra.
2. **Mai volti riconoscibili**, mai persone identificabili: è un fondo, e un fondo non ha un
   soggetto che possa essere frainteso come un caso, un beneficiario o un testimonial.
3. **Mai cronaca migratoria** (DESIGN_SYSTEM_V2 §6), mai frontiere, mezzi di trasporto in situazione,
   file d'attesa, documenti reali.
4. **Soggetti ammessi**: architettura istituzionale e portuale, superfici (pietra, intonaco, acqua,
   carta), geografia a distanza, laboratori e aule vuoti. Cioè **luoghi, non storie**.
5. **Taglio**: l'orizzonte della fotografia non cade mai dentro i primi `--th` px — sarebbe un
   secondo confine in competizione con la soglia.
6. **Una lastra per pagina**, e mai due di fila. Test: §6.

**La politica di alt e ARIA — la superficie dove la regola delle parole vietate morde.**
Una lastra è **decorativa per definizione**: porta zero informazione. Perciò `alt=""` **sempre**,
`aria-hidden="true"` sul `<picture>`, nessun `title`, nessuna didascalia, nessuna `figcaption`,
nessuna etichetta nascosta. **Nessuna parola entra nella pagina insieme alla fotografia.** Se una
fotografia porta informazione non è una lastra: è una `<figure>` con una didascalia, e quella
didascalia passa dal registro bloccato (`{% locked %}`) come ogni altro testo, quindi passa per
`apps/cms/forbidden.py` come ogni altro testo. Questa distinzione è normativa, e il test del §6 la
fa rispettare.

### 4.7 Stati — come CSS, con il selettore nominato

**Che cos'è «un `.ground--sheet` interattivo».** Non è un'astrazione: è una di queste tre forme, e
il CSS del §4.3 le nomina tutte e tre.

| Forma | Esempio reale già in pagina |
|---|---|
| `a.ground--sheet` / `button.ground--sheet` — il foglio **è** il controllo | `a.entry` delle quattro entrate (`routes.css:40`), `.local-nav__link` |
| `.ground--sheet:has(> a[href])` — il foglio contiene un link diretto | `.home-reserved__panel` (§4.5) |
| `.ground--sheet:has(> * > a[href])` — il link è dentro il titolo | `article.card--link` delle news (`templates/components/card.html`) |

Un `.ground--sheet` che non corrisponde a nessuna delle tre **non è interattivo** e non ha stati:
è un pannello. Questo è il contratto, ed è testabile.

| Stato | Comportamento | Compagno non-cromatico | Misura |
|---|---|---|---|
| rest | `--ground: var(--min-2)`, `border: 1px solid var(--hairline)`, nessuna ombra | — | bordo su fondo **1,45:1** |
| hover (`@media (hover:hover)`) | `--ground: var(--min-3)` · `border-color: var(--hairline-strong)` · `box-shadow: var(--shadow-2)` · 180 ms `--ease-out` | **l'elevazione compare** (ruolo 2, solo in hover, DESIGN_SYSTEM_V2 §2) | il bordo cambia di **2,47:1** fra i due colori e passa da 1,45:1 a **3,59:1** sul fondo. Il fondo cambia di 1,043:1 — è il **terzo** indizio, mai il solo |
| focus-within | identico all'hover, **più** l'anello del controllo interno | elevazione + anello | anello `--accent-ring` **3,70:1** su `--min-0`, **3,17:1** anche nel punto più scuro della rampa |
| active | `--ground: var(--min-1)` · `border-color: var(--hairline-strong)` · **ombra via** · `transform: translateY(1px)` · 120 ms `--ease-in` | **il foglio si abbassa e perde l'elevazione** (DESIGN_SYSTEM_V2 §10) | spostamento 1 px + perdita d'ombra |
| disabled (`[aria-disabled="true"]`) | `--ground: var(--min-1)` · `--grain-amount: 0` · bordo `--hairline` · `cursor: not-allowed` | **la superficie perde la materia** | oltre alla parola, che è del componente |
| loading (`[aria-busy="true"]`) | lo scheletro vive **sopra** `.ground--sheet`; la grana **resta** | la pagina non «si accende» a fine caricamento | — |
| error | il fondo **non diventa mai rosso**: `--err-700` resta bordo + testo + icona (§1.3-3) | — | — |

**Le due cifre del round 1, ricalcolate.** Il revisore ha ragione nel merito e sbaglia i numeri:
l'hover proposto (`--min-2` → `--min-3`) valeva **1,043:1**, non 1,03:1; l'active
(`--min-2` → `--min-1`) valeva **1,144:1**, non ~1,06:1. Entrambi restano sotto qualunque soglia
differenziale utile, e restano indifendibili come **unico** segnale. Il round 2 non li elimina: li
declassa a terzo indizio dietro il bordo e l'elevazione.

Tutte le `transition` vivono dentro `@media (prefers-reduced-motion: no-preference)`. Fuori da quel
blocco gli stati sono **identici ma istantanei**: nessun contenuto cambia, nulla resta a opacità 0.

### 4.8 La piattaforma — con i file e i selettori che esistono davvero

`templates/portal/partials/portal_chrome.html` **non esiste**. La directory contiene
`access_point.html`, `card.html`, `case_header.html`, `deadline_item.html`, `next_action.html`,
`territory_band_base.svg`, `territory_band_layer-1.svg`. Il file vero è
**`templates/partials/portal_chrome.html`**, incluso da `templates/portal/base_portal.html:23`.

| Regione | File · elemento | Classe | `--th-room` misurato |
|---|---|---|---|
| Barra di contesto | `templates/partials/portal_chrome.html:16` → `<div class="portal-bar">` | `ground ground--midnight` | `padding: var(--s-3) var(--grid-margin)` (portal.css:29-37) → 12 px, nessuna rampa: è cornice, e come il piè di pagina non conta come capitolo (DEROGA 2) |
| Fascia del caso | `templates/portal/partials/case_header.html` → `.case-header` | `ground ground--area` | `.case-header__inner` `padding-block: var(--s-6)` (portal.css:115-121) → 24 px |
| Prossima azione | `.next-action` (portal.css:172) | `ground ground--paper` | `margin-block: var(--s-6)` → nessuna rampa |
| Rail di navigazione | `templates/portal/base_portal.html:38` → `<aside class="portal__aside">` | `ground ground--area` | 0 (appiccicoso) |
| Canvas di lavoro | `base_portal.html:42` → `<div class="portal__main">` | `ground ground--paper` | 0 |
| Fogli | `.portal-section`, `.portal-account` (portal.css:241, 261), `templates/portal/partials/card.html` | `ground ground--sheet` | — |
| Piè di pagina di piattaforma | `base_portal.html:58` → `.portal-footer` | `ground ground--utility` | `.portal-footer__inner` `padding-block: var(--s-6)` → 24 px |

**Dichiarazioni da cancellare:** `portal.css:21` `.portal-bar{ background: var(--navy-deep) }`,
`portal.css:111` `.case-header{ background: var(--paper-deep) }`, `portal.css:262`
`.portal-account{ background: var(--paper-deep) }` — tutte shorthand, tutte sostituite dal ground.

**Il contratto di modo, e perché la piattaforma non annega nell'atmosfera.**
`base_portal.html` dichiara `{% block page_mode %}rich{% endblock %}`; i template densi —
fascicolo, liste, tabelle, back-office (DESIGN_SYSTEM_V2 §7) — lo sovrascrivono con `dense`.
In DENSE `--material: 0`: **i fondi restano, la materia sparisce.** È esattamente la riparazione
che il §1.5 chiede — il fascicolo guadagna un rail, un canvas e dei fogli, non una texture sotto una
tabella di 200 righe.

### 4.9 Il FORUM — riparazione del tricolore (MUST-FIX 12)

| File : riga | Oggi (misurato) | Domani |
|---|---|---|
| `apps/forum/static/forum/forum.css:24-25` | `.forum-hero{ background: var(--forum-navy) }` → `rgb(15,37,71)` = `--brand-navy`, alto **388 px** | cancellare il `background`; `templates/forum/partials/hero.html:7` → `class="forum-hero ground ground--midnight"`. Regola esplicita (il predecessore è il breadcrumb, non un `.ground`): `.ground.forum-hero{ --ground-prev:var(--min-0); --th-room:var(--rank-b-block) }` + la regola di discesa. `padding-block-start` passa da 80 px a `var(--rank-b-block)`: **+16 px a 1440, +8 px a 390** — è la correzione di un valore fuori scala, ed è l'unica variazione d'altezza dichiarata in questo documento |
| `apps/forum/static/forum/forum.css:141` | `.forum-cta{ margin-block-start: 2rem; padding: clamp(1.5rem,4vw,2.5rem); background: var(--forum-navy); border-radius: var(--forum-radius) }`, alto **176 px** | cancellare `background` e `border-radius` (DESIGN_SYSTEM_V2 §2: raggio 0 sui capitoli). `templates/forum/partials/cta_row.html:8`: togliere `container` dal `<section>` e avvolgere il contenuto in un `<div class="container">` — **nessuna parola cambia**. Poi `ground ground--midnight`, `margin-block-start: 0` e `padding-block-start: calc(var(--s-8) + clamp(1.5rem,4vw,2.5rem))`: invariante in altezza, e la discesa ha 72 px a 1440 e 56 px a 390 |
| `apps/forum/static/forum/forum.css:104` | `.forum-section--accent{ background: var(--forum-sand); border-radius: … }` su un `.container` | `ground ground--area` a piena larghezza, raggio 0: un fondo che si ferma a 1 320 px è un box, e §1.3-5 dice che il confine di capitolo non è un box |
| `.forum-cta__title` | `color: var(--forum-gold-soft)` | `--on-dark-2`: l'oro è del marchio (§1.3-4) |

Le due regole esplicite che il FORUM richiede, da aggiungere in coda a `v3/ground.css` (né
`.forum-hero` né `.forum-cta` hanno un `.ground` come fratello immediato: il primo segue il
breadcrumb, il secondo una `.forum-section` senza fondo proprio):

```css
/* Il FORUM: due capitoli mezzanotte che oggi sono navy. Il predecessore di
   entrambi è il fondo di pagina, campionato --min-0 sopra ciascuno dei due. */
.ground.forum-hero, .ground.forum-cta{
  --ground-prev:var(--min-0);
  --th-mid:var(--th-descent-mid); --th-end:var(--mid-edge);
  --lume:rgb(255 255 255 / .55); --lume-fall:var(--s-4); --tide:var(--terr-line-lt);
  --th:min(var(--s-24), var(--th-room)) }
.ground.forum-hero{ --th-room:var(--rank-b-block); padding-block-start:var(--rank-b-block) }
.ground.forum-cta{ --th-room:calc(var(--s-8) + clamp(1.5rem, 4vw, 2.5rem));
  margin-block-start:0; padding-block-start:calc(var(--s-8) + clamp(1.5rem, 4vw, 2.5rem)) }
```

Conteggio risultante per il FORUM (regola della DEROGA 2): **due** capitoli mezzanotte dentro
`<main>` — `forum-hero` e `forum-cta` — dentro il tetto di due delle pagine IMMERSIVE, e nessun
`--brand-*` rimasto come fondo. `.forum-card__title{ color: var(--forum-navy) }` e gli altri usi di
navy **come testo** restano fuori dall'area `backgrounds`: sono nominati qui e consegnati a
`company-forum-academy.md`.

---

## 5. MOTION — la voce che questo sistema aggiunge a `MOTION_SYSTEM.md` §6

**Nessuna.**

Il round 1 proponeva tre voci. Il round 2 ne propone **zero**, e la ragione non è la prudenza:

- **`ground/soglia-marea` — CANCELLATA.** Era un tracciato immersivo di 600 ms — una durata che non
  esiste nel set (`--motion-draw` è 900 ms, `v2/tokens.css:111`) — e il §8-5 ne ammetteva fino a
  cinque per pagina dove il sistema ne ammette uno. Non la riscrivo a 900 ms e non la limito a una:
  **una linea che si disegna a ogni confine di sezione è il tic di divisore del 2021-23**, esattamente
  come dice il revisore. La soglia è completa dal primo frame, in ogni stato, per tutti.
- **`ground/graticola-deriva` — CANCELLATA.** Faceva scorrere il `::before`, cioè oggi farebbe
  scorrere **una graduazione di margine**. Uno strumento che deriva è uno strumento che mente. E
  risolve da sé la contraddizione fra §5 e §7 che il revisore ha trovato: non c'è nessuno strato da
  promuovere, perché non c'è nessuna animazione.
- **`ground/rail-lume` — TOLTA DA QUESTA SPECIFICA.** L'indicatore di posizione del rail è del rail,
  non del suo fondo. Consegnata a `platform-shell.md`, nominata qui perché il round 1 la rivendicava.

**Conseguenze verificabili, non promesse.**
- Il sistema di fondi non contiene una sola `@keyframes`, una sola `animation`, un solo
  `will-change`, un solo `transform` a riposo. Le uniche `transition` sono quelle del §4.7, tutte
  dentro `@media (prefers-reduced-motion: no-preference)`, tutte su `--motion-fast` (180 ms) e
  `--motion-instant` (120 ms), tutte con `--ease-out` / `--ease-in`. **Nessuna durata nuova, nessuna
  curva nuova, nessun overshoot, nessuna molla.**
- Misurato sulla home reale con il candidato applicato: `document.getAnimations().length` = **3**,
  identico alla pagina di oggi (le due falde della marea dell'hero, 28 s e 34 s, e la rotta legata
  allo scroll). **Il sistema di fondi aggiunge zero animazioni.**
- **La quota resta intera per chi ne ha bisogno.** Misurato: `/fr/parcours/`,
  `/fr/entreprises/`, `/fr/institutions/`, `/fr/universites-et-formation/`, `/fr/forum/` e
  `/fr/faq/` hanno **0 animazioni, 0 loop ≥ 20 s, 0 ScrollTimeline**; `/fr/` ha **2 loop ≥ 20 s**
  (una sola marea su due falde, come ammette DESIGN_SYSTEM_V2 §5) **e 1 ScrollTimeline** (la rotta).
  Questo documento non spende nulla di tutto ciò: le quattro landing e il FORUM restano libere per
  `scroll.md` e `hero-doorway.md`.
- `prefers-reduced-motion: reduce` → verificato: `document.getAnimations().length` = **0**,
  `::before` e `::after` restano `display: block`, la rampa resta a 96 px. Stato completo:
  contenuto identico, nessun elemento a opacità 0, niente di invisibile.

**`ground/grana-viva` — RIFIUTATA e da tenere rifiutata.** Una grana che si muove è grana
cinematografica: ridisegna il fondo a ogni frame, costa un paint a schermo pieno per frame, e nel
2026 è il segnale visivo più economico che esista. Nessuna delle sette funzioni la copre («estetica»
non è una funzione). Scritta qui perché qualcuno la proporrà.

---

## 6. ACCESSIBILITÀ, RTL E TEST

**Che cosa cambia.** Il filetto da 11,55:1 sul capitolo mezzanotte sparisce (entrambe le origini,
§1.3). Al suo posto: una rampa alta quanto il padding che la sezione ha già, un filo di luce di
16 px, e due tacche di graduazione da `--grat-margin` × 1 px in `--terr-line` (**6,07:1** su
mezzanotte) o `--terr-line-lt` (**4,20:1** su carta) — grafica, mai testo, mai un controllo, e mai
attraverso la pagina.

- Nel punto più scuro della rampa chiara (`--min-edge`): `--ink` **12,52:1**, `--ink-2` **5,53:1**,
  `--ink-3` **4,74:1**, `--accent` **4,87:1**, `--accent-hover` **6,56:1**, anello `--accent-ring`
  **3,17:1**, `--err-700` **5,04:1**. Nel punto più chiaro della rampa scura (`--mid-edge`):
  `--on-dark` **13,63:1**, `--on-dark-2` **8,51:1**, `--on-dark-3` **5,66:1**, `--accent-dark`
  **8,80:1**.
- **Regola dura**: la soglia occupa il `padding-block-start` della sezione e **non può contenere
  contenuto**. Misurata, non sperata: 0 sconfinamenti su 80 combinazioni sezione × larghezza ×
  build, più zoom 200 % e 400 %, più RTL (§4.2).
- `prefers-contrast: more` → `--material: 0`. Verificato sull'elemento, non sul `:root`: `::before`
  opacity **0**, `::after` opacity **0**, banda di luce **0 px**, **rampa conservata a 96 px**.
  L'alto contrasto toglie la texture, non il confine.
- `forced-colors: active` → verificato: `background-image: none`, `background-color: Canvas`,
  pseudo-elementi `display: none`, e **un filetto `1px solid CanvasText` su ogni passaggio**
  (misurato `1px rgb(0,0,0)` su `pilot` e su `trust`). La composizione sopravvive come sequenza di
  sezioni separate da una riga di sistema.
- `prefers-reduced-motion` → il fondo è immobile per costruzione; nessuna `@keyframes` esiste.
- **Il colore non è mai solo**: il cambio di capitolo è fondo + rampa + filo di luce + tacca +
  `<h2>` + landmark di sezione. Nessuna informazione vive nel fondo.

**RTL.** L'apparato di margine è **simmetrico**: gli stessi valori su `left` e su `right`. Per
`background-position` non esiste un equivalente logico, e una composizione simmetrica non ne ha
bisogno: in `dir="rtl"` è identica a sé stessa. Verificato forzando `dir=rtl` sulla home: **0
sconfinamenti**, nessuna asimmetria. Non si specchia la graticola (un reticolo non ha direzione),
non la grana (rumore), non la rampa (verticale). Non esiste più alcun `--lume-x` da specchiare,
perché non esiste più il radiale d'angolo. Il `.tide` come elemento non esiste più.

**I test da scrivere.**

| File | Asserzione |
|---|---|
| `tests/frontend/test_v3_threshold_is_clear.py` | per ogni `.ground`, il primo figlio ha `offsetTop >= getComputedStyle(el).getPropertyValue('--th')` — a 1440, 768, 390, e a zoom 200 % |
| `tests/frontend/test_v3_threshold_is_derived.py` | `grep -c "th--from-" templates/` == 0; e in `v3/ground.css` esistono le cinque regole `+ .ground` |
| `tests/frontend/test_v3_no_hairline_on_chapters.py` | nessun `.ground` adiacente a un `.ground` ha un `border-block-start-color` con rapporto > 4:1 sul proprio fondo, fuori da `forced-colors` |
| `tests/frontend/test_v3_five_grounds.py` | ogni `background-color` di sezione del CSS compilato è uno dei cinque token; **fallisce oggi su `.forum-hero` e `.forum-cta`, e il §4.9 li ripara** |
| `tests/frontend/test_v3_chapter_count.py` | conta i `.ground--midnight` **dentro `<main>`**: ≤ 2 su HOME e FORUM, ≤ 1 altrove; `.ground--utility` della cornice non conta (DEROGA 2) |
| `tests/frontend/test_v3_edge_tokens_are_ramp_only.py` | `--min-edge`/`--mid-edge` non compaiono in nessun `color`, `border-*-color`, `background-color` |
| `tests/frontend/test_v3_material_switch.py` | con `data-mode="dense"` / `"legal"` e con `prefers-contrast: more`, `--material` computa `0` su ogni `.ground` |
| `tests/frontend/test_v3_plate_is_mute.py` | ogni `.ground__plate img` ha `alt=""`, il `<picture>` ha `aria-hidden="true"`, nessun `title`; nessuna `figcaption` dentro un `.ground--plate`; al massimo una lastra per pagina e mai due di fila |
| `tests/frontend/test_v3_no_ground_motion.py` | `v3/ground.css` non contiene `@keyframes`, `animation`, `will-change`; ogni `transition` è dentro `@media (prefers-reduced-motion: no-preference)` |

**HUMAN_QA_REQUIRED.**
1. Grana a 3,5 % su pannello 6-bit e su OLED a bassa luminanza: si vede? fa rumore? (σ misurata
   1,003 sulla carta, 1,331 sul mezzanotte).
2. La graduazione di margine su Safari (macOS e iOS) e Firefox: i sei layer di background si
   allineano con `--grat-margin` in `calc()` con `min()`? È l'unico punto del foglio che dipende da
   un `calc()` con percentuale dentro `background-size`.
3. `mask-mode` su Safari e Firefox: **non** per l'inversione, che è misurata come inesistente
   (§4.4), ma per l'ampiezza: se un motore legge la luminanza la grana cala del 5 % sulla carta e del
   21 % sul mezzanotte. Verificare che resti percepibile.
4. Alto contrasto Windows, tema chiaro **e** scuro.
5. Percezione della rampa in bassa visione: deve leggersi come *confine*, non come *sfocatura*.
6. La tacca di confine a 390 px è larga 20 px per lato: è ancora leggibile come segno intenzionale o
   sembra un artefatto? È la misura più a rischio del documento.

---

## 7. PRESTAZIONI — rimisurate sulla home reale, non su un prototipo

**Byte (misurati).** `static/css/v3/ground.css` **9 495 B raw / 2 304 B gzip** ·
`static/img/v3/grain.svg` **326 B / 246 B** · **JavaScript 0 B, e zero nuovi punti d'ingresso.**
Totale **9 821 B raw / 2 550 B gzip**. Budget JS invariato (≤ 45 KB gzip): questo documento non
aggiunge una riga di JavaScript, non ha bisogno di un `IntersectionObserver`, non ha bisogno di un
comando di pausa e quindi non introduce **nessuna stringa nuova** da far passare da
`apps/cms/forbidden.py`. Il round 1 budgetava «< 700 B» per un meccanismo di pausa che, come nota il
revisore, non esisteva: serviva un observer per pagina, un entry point e un comando etichettato
nuovo. Quel costo è **zero** perché l'oggetto che lo richiedeva è cancellato.

**Paint, layout e stile — CDP `Performance`, 12 passi di scroll a 1440, home reale.**

| | candidato applicato | pagina di oggi |
|---|---|---|
| `LayoutCount` | **4** | **4** |
| `RecalcStyleCount` | 68 | 66 |
| `LayoutDuration` | **0,9 ms** | 1,5 ms |
| `RecalcStyleDuration` | **7,8 ms** | 9,1 ms |
| `TaskDuration` | **204 ms** | 233 ms |
| `document.getAnimations()` | **3** | **3** |

Il sistema aggiunge **0 layout e 0 animazioni**, e il costo di stile e di task è dentro il rumore di
misura (le differenze sono a favore del candidato in tre voci su cinque: non rivendico un
miglioramento, rivendico che il costo non è misurabile). Nessun `filter`, nessuna `box-shadow`
animata, nessun `background-position` animato, nessun `backdrop-filter` fuori dall'header scrollato.
Due pseudo-elementi per capitolo, **nessuno promosso**: nessun `will-change`, nessun `transform` a
riposo, nessun livello di compositing nuovo — e questa volta l'affermazione è coerente con il §5,
perché al §5 non c'è più niente.

**Banding — misurato sui pixel del candidato, non stimato.** Passo massimo fra righe adiacenti sul
canale verde, colonna x=720:

| Passaggio | altezza | passo max | passo medio |
|---|---|---|---|
| discesa `pathways → pilot` | 96 px | **6 livelli** | 2,73 |
| risalita `pilot → trust` | 96 px | **7 livelli** | 2,28 |
| piega `news → ecosystem` | 48 px | **4 livelli** | 1,31 |
| discesa `main → site-footer` | 96 px | **6 livelli** | 2,63 |

La grana con σ ≈ 1,0–1,4 dithera passi di questa dimensione. **La grana non è decorazione: è
l'anti-banding della soglia**, e per questo non è sacrificabile. Nota di metodo: il round 1 chiudeva
la rampa su `transparent`; l'interpolazione verso `rgba(0,0,0,0)` passa per il nero premoltiplicato
e produceva un avvallamento di **−6 livelli** in fondo alla rampa (misurato). Il round 2 chiude su
`var(--ground)`.

---

## 8. RISCHI

| # | Come questo può sembrare economico invece che premium | Guardia |
|---|---|---|
| 1 | **La pila è la ricetta più copiata del 2024-25.** Era vero, ed è il rischio che il round 1 non nominava. | Due strati su quattro sono cambiati: via il bagliore radiale d'angolo, via la maglia ortogonale a campo pieno. Al loro posto un apparato di **margine** graduato e una luce che è un **filo**, non un campo (§3-bis). Test: `v3/ground.css` non contiene `radial-gradient` fuori dal velo della lastra, e nessun `repeating-linear-gradient` ha `background-size` che superi `--grat-margin` in larghezza. |
| 2 | **La graticola legge come una tabella.** Provato a 5,5 % non mascherata. | Non attraversa mai il testo: vive nella fascia `--grat-margin`, cioè fuori dalla colonna. Test: `background-size` dei layer del `::before` non supera mai `--grat-margin` (la neat line è 1 px, le tacche sono `--grat-tick` e `--grat-margin / 2`). |
| 3 | **La rampa legge come una sfocatura JPEG.** | Tre stop con accelerazione al centro (46 % / 78 %), tratto ripido ≥ 24 px, la grana come dither, e — nuovo — un **filo illuminato** sul primo pixel che dà al passaggio un bordo, che una sfocatura non ha. Misura: passo massimo 6-7 livelli su 96 px (§7). |
| 4 | **La grana non sopravvive alla compressione.** A 3,5 % scompare in un JPEG q70, in un PDF, in una slide. | La grana **non porta mai informazione**: nessuna differenza di superficie dipende da lei. Se sparisce restano fondo, rampa, filo e tacca. Scritto come regola, non sperato. |
| 5 | **Le soglie diventano un tic.** | Il tetto non è più un numero arbitrario, è **derivato**: ogni fondo scuro produce al massimo due passaggi (la sua discesa in entrata e la sua risalita in uscita), e il numero di fondi scuri è già limitato da DESIGN_SYSTEM_V2 §1.3-5 più la cornice. Massimo strutturale: **2 × 2 + 1 = 5** su HOME e FORUM, **2 × 1 + 1 = 3** altrove. Sulla home misurata oggi: **4** — risalita a `entrances`, discesa a `pilot`, risalita a `trust`, discesa al piè di pagina. Le pieghe non portano tacca, non si animano e non contano: sono il respiro fra due sezioni della stessa riva, e la loro altezza è il padding che c'era già. |
| 6 | **Il tricolore rientra dalla finestra.** Due fondi navy nel FORUM, non uno (§1.6). | Cinque fondi ammessi e nessun altro; `test_v3_five_grounds.py` fallisce oggi sui due fondi del FORUM, e il §4.9 li ripara. Il test e la riparazione sono nello stesso documento. |
| 7 | **Un motore sbaglia `mask-mode` e la grana si inverte.** | **Misurato: non si inverte.** Luminanza invece di alfa dà σ 0,965 contro 1,017 sulla carta e 1,071 contro 1,363 sul mezzanotte (§4.4). Il guard `@supports not (mask-mode: alpha)` degrada a zero grana, mai a grana sbagliata; il piano B in PNG (8 498 B) resta misurato. |
| 8 | **La piattaforma eredita l'atmosfera della vetrina.** Un fascicolo con grana sotto una tabella di 200 righe è la definizione del superfluo. | `data-mode="dense"` → `--material: 0` con **uno scalare ereditato che nessuna specificità può battere** (il round 1 usava una regola che le regole di passaggio vincevano). In piattaforma la materia vive solo dove c'è struttura; i **fondi** (rail, canvas, fogli, barra) restano, perché è la loro assenza il difetto misurato al §1.5. |
| 9 | **Regressione silenziosa**: qualcuno rimette un `border-block-start` fra due capitoli. | `test_v3_no_hairline_on_chapters.py`; e la cancellazione riguarda **due** regole, non una (§4.5). |
| 10 | **Il segno di confine è troppo timido a 390 px** (20 px per lato). | Rischio reale, non risolto in CSS: è in HUMAN_QA §6. Se cade, la risposta è portare la tacca a `max(var(--grat-margin), var(--s-10))` sotto 48rem — una riga, già scritta qui, non un ripensamento. |
| 11 | **`.ground` rompe una pagina che ha già strati assoluti.** | Successo davvero nel round 1: `.ground > * { position: relative }` portava l'hero da 899 px a 3 359 px (§4.1). La regola è cancellata; il contratto è `isolation: isolate` + `z-index: -2 / -1`, e nessun figlio viene toccato. Test: `v3/ground.css` non contiene alcun selettore `.ground > *`. |

---

## 9. REGISTRO DELLE MISURE (come ogni numero è stato ottenuto)

Tutto con `C:\tmp\italylegalentry\.venv\Scripts\python.exe`, Playwright Chromium **headless**
(`HeadlessChrome/153.0.8010.12`), browser proprio, mai la porta 9222. Il foglio candidato è stato
servito **same-origin** (una route Playwright che risponde a `/__p.css` e un'iniezione di `<link>`
nella risposta HTML) perché `style-src 'self'` rifiuta `add_style_tag` — il rifiuto stesso è una
verifica della CSP. **Nessun file del repository è stato modificato tranne questa specifica.**

| # | Numero | Metodo |
|---|---|---|
| 1 | fondi, gradienti, altezze, filetti del §1 | `getComputedStyle` su ogni `[data-section]` + screenshot a piena pagina (1440×7921) campionato con PIL; origine del filetto dell'hero trovata con CDP `CSS.getMatchedStylesForNode` |
| 2 | soglia derivata dai fratelli | classi applicate via JS su :8771 **e** :8770, 4 larghezze; letti `--ground-prev`, `--th-mid`, `--tide` computati su ogni `.ground`. Su :8770 la catena si ricuce con `_banner` presente e `pilot`/`antifraud`/`news`/`reserved` assenti |
| 3 | 0 sconfinamenti | `firstElementChild.getBoundingClientRect().top − el.getBoundingClientRect().top` confrontato con il valore **risolto** di `--th` (registrato via `@property`), a 1440/1200/768/390, su due build, a zoom 200 %/400 %, e in `dir=rtl` |
| 4 | `#556165` `#5d686b` `#edebe7` e i fallback sRGB | dodici `<div>` con i `color-mix()` renderizzati e **campionati a pixel**, non letti da `getComputedStyle` (che restituisce `oklab(…)`) |
| 5 | `mask-mode` prima/dopo lo shorthand, e σ nei tre modi | due `<div>` con l'ordine invertito; poi sei pannelli 600×120 con `alpha`/`luminance`/`match-source`, σ su 6 400 px per pannello |
| 6 | `--material` nei quattro stati | `page.emulate_media(forced_colors / contrast / reduced_motion)` + `data-mode="legal"`; letti `--material`, `opacity` dei due pseudo-elementi, `background-size` e i bordi |
| 7 | quota di moto delle sei pagine | `document.getAnimations()` dopo `networkidle` **e dopo uno scroll a metà pagina** (perché una ScrollTimeline si registra allo scroll); più il censimento degli script caricati per rotta |
| 8 | CDP `Performance` | `Performance.getMetrics` prima e dopo 12 passi di scroll, candidato e baseline, stessa sessione, stesso viewport |
| 9 | banding e σ della grana | screenshot del candidato a piena pagina, differenze fra righe adiacenti sul canale verde a x=720; σ su finestre di 40×40 px scelte fuori dal testo |
| 10 | byte | `wc -c` e `gzip -9` sul file candidato e sull'SVG |
