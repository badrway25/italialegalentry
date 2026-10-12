# V3 — ESPERIENZA DI SCORRIMENTO E TRANSIZIONI DI SEZIONE

Area `scroll` · **round 2**, riscritto contro `docs/design-v3/reviews/scroll.md`. Superficie effettiva: **la home `/fr/`
(:8771) e il contratto di cucitura che le altre superfici adottano con un attributo**; §8.4 dice quali e a chi appartengono.
Vincolanti: `DESIGN_SYSTEM_V2.md`, `MOTION_SYSTEM.md`, `ANTI_PATTERNS.md`. Nessuna vista Django, nessun contratto dati toccato.

**Come sono state prese le misure di questo round.** Chromium headless di Playwright dal `.venv` del progetto, browser
proprio, mai la 9222. Viewport 1440×900, 1280×900, 768×1024, 390×844. Il foglio candidato non è stato scritto nel repo: è
stato **servito dall'origine della pagina** tramite intercettazione di rotta e agganciato con un `<link>`, perché
`add_style_tag` e ogni `style=""` sono **bloccati dalla CSP di questo sito** (`style-src 'self'` — errore riprodotto e
registrato: *«Applying inline style violates … 'style-src 'self''»*). Il markup candidato è stato costruito nel DOM con sole
classi. Script e fogli in `…/scratchpad/scroll/`: `final.css`, `m1…m11_*.py`; schermate `ship_chart_1440.png`,
`ship_seam_1440.png`, `final_seam_{dark,light}_1440.png`, `last_chart_{1440,1280,768,390}.png`.

---

## 0. RICHIESTE DI DEROGA

Una sola, numerata. Tutto il resto di questo documento sta dentro i documenti vincolanti come sono scritti.

### AMENDMENT REQUEST 1 — `MOTION_SYSTEM.md` §4, «e **un** oggetto indicizzato allo scroll»

**Clausola.** §4 «Un solo oggetto vivo per pagina»: «Una pagina IMMERSIVE può avere **un** loop ambientale (≥ 20 s …) e **un**
oggetto indicizzato allo scroll. Le pagine RICH ne hanno al massimo uno dei due; STANDARD, DENSE e LEGAL nessuno.»

**Modifica chiesta.** Sostituire «e **un** oggetto indicizzato allo scroll» con «e **un oggetto indicizzato allo scroll per
capitolo mezzanotte**». Il resto della clausola resta parola per parola.

**Ragione — la clausola come è scritta vieta la composizione che gli stessi documenti prescrivono.**
`DESIGN_SYSTEM_V2.md` §8.4 impone alla fotografia della porta di scorrere di 18 px («Scroll: la fotografia scorre di 18 px») e
§8.6 impone alla rotta del processo di essere `stroke-dashoffset` **legata allo scroll**; §1.3 regola 5 concede a HOME e FORUM
**due** capitoli mezzanotte. I tre obblighi sono simultanei e stanno tutti sulla home. Misura sul build in produzione oggi
(`http://127.0.0.1:8771/fr/`, 1440×900, a pagina ferma in cima):

```
document.getAnimations() → tide-1  / DocumentTimeline / 28 000 ms
                           tide-2  / DocumentTimeline / 34 000 ms
                           IMG.doorway__img / ViewTimeline / 300
```

più `.voyage__line`, che **non compare** in `getAnimations()` perché `home.js` la guida per frame con lo `scroll()` di Motion
(§1.5). Sono **due** oggetti indicizzati allo scroll contro un tetto di uno, nel build approvato dal Council. La regola non è
stata scritta contro questo: il suo modello di costo è la «chiave che levita per sempre», cioè un oggetto vivo che consuma
budget *mentre la pagina sta ferma*. Un'animazione su `ViewTimeline` non ha durata propria, non gira a pagina ferma e non ha
un driver JS.

**Costo.** Il tetto su HOME/FORUM passa da 1 a 2. **Non introduce un numero nuovo**: il nuovo tetto è
`document.querySelectorAll('main .chapter--dark').length`, già limitato da `DESIGN_SYSTEM_V2.md` §1.3 regola 5 (due su
HOME/FORUM, uno altrove) e già contabile da una macchina. Su STANDARD, DENSE e LEGAL il tetto resta **zero** per costruzione,
perché quelle modalità non hanno capitoli mezzanotte — misurato: `main .chapter--dark` = 0 su `/fr/glossaire/`,
`/fr/privacy-policy/`, `/fr/compte/login/`, `/fr/faq/`, `/fr/parcours/`, `/fr/actualites/`, `/fr/orientation/`,
`/fr/entreprises/`, `/fr/forum/`; = 2 su `/fr/`.

**Prova da aggiungere a `tests/frontend/`:**

```python
scroll_linked = page.evaluate(
    "document.getAnimations().filter(a => a.timeline "
    "&& (a.timeline.constructor.name === 'ScrollTimeline' "
    "||  a.timeline.constructor.name === 'ViewTimeline')).length")
chapters = page.evaluate("document.querySelectorAll('main .chapter--dark').length")
assert scroll_linked <= chapters
```

Misurato sul candidato: home **2 ≤ 2**; `/fr/glossaire/` **0 ≤ 0**.

**Che cosa la deroga NON autorizza.** Nessun moto indicizzato allo scroll fuori da un capitolo mezzanotte: la cucitura (§4.2) è
un reveal `inView` una tantum, i tre ruoli di reveal (§4.3) sono `inView` una tantum, e **nulla di legato allo scroll entra nel
cromo** (§4.5). Il loop ambientale resta uno per pagina, invariato.

---

## 0bis. RISPOSTA PUNTO PER PUNTO ALLA REVISIONE

Ogni MUST-FIX è **FATTO** o **CONTESTATO con la misura**. Nessun terzo stato.

| # | MUST-FIX | Esito |
|---|---|---|
| 1 | Budget degli oggetti indicizzati allo scroll | **FATTO** — AMENDMENT 1 (§0) **e** taglio da otto famiglie a **una**. Inventario misurato sul candidato: `tide-1`, `tide-2` (DocumentTimeline, in pausa fuori viewport), `voyage-draw` (ViewTimeline), `IMG.doorway__img` (ViewTimeline). Un loop, due oggetti indicizzati, due capitoli mezzanotte. |
| 2 | Togliere la barra di lettura da DENSE e LEGAL strutturalmente | **FATTO per soppressione**: la barra non esiste più (§4.5 «ciò che è stato tolto»). Nessuna riga di `templates/partials/header.html` cambia, quindi nessuna pagina DENSE o LEGAL riceve un solo byte di questo capitolato. · **CONTESTATA la premessa** «gate the whole `.readbar` on the template's **existing** `data-mode`»: `data-mode` **non esiste**. Misurato su dieci rotte 200 (`document.documentElement.dataset.mode`) → `undefined` ovunque; `grep -rn "data-mode" templates/ apps/` → **0 occorrenze** (le sole due sono nei prototipi `docs/design-v2/directions/b-*/`), esattamente come misura `imagery.md` §1.8. Il gate strutturale usato qui è un invariante che **esiste**: `html:has(main .chapter--dark)` (§4.2). · Contestata anche l'euristica come *unico* difetto: il bersaglio reale non erano le note legali (`/fr/privacy-policy/` = 1 201 px = **1,33 schermate**, 0 sezioni: non passava il gate) ma **il glossario** — `/fr/glossaire/` = 2 741 px = **3,05 schermate** con **8 `section[id][aria-labelledby]`**: passava il gate «≥ 4 sezioni e ≥ 3 viewport» su una pagina STANDARD. La revisione aveva ragione sulla conclusione, e questa è la pagina che lo prova. |
| 3 | Specificare la linea di livello | **FATTO per sostituzione**: i due gradienti e la linea di livello spariscono; la cucitura è un **bordo di graticola** con CSS completo in §4.2 — selettore, `background` a due strati, `transform-origin`, gate `:has()`, `@media (prefers-reduced-motion)`, `forced-colors`, RTL. `::before` è l'unico pseudo-elemento usato; `::after` resta **deliberatamente libero** e il documento lo dice. |
| 4 | Dichiarare `--at`, aggiungerlo a `RUNTIME_PROPERTIES` | **FATTO per soppressione**: senza barra non c'è `--at`. Verificato eseguendo la **logica del test reale** (`tests/frontend/test_css_tokens_exist.py`: stesse regex, stesso insieme di file, stesso `RUNTIME_PROPERTIES = {"--nav-drawer-top", "--reveal-index"}`) sul foglio di §4: **0 proprietà non definite**, 10 token dichiarati nel file stesso, **0 dichiarati e mai usati**. `RUNTIME_PROPERTIES` non va toccato. |
| 5 | Layout `<64rem` per `.voyage__figure` | **FATTO per soppressione**: il wrapper non esiste, il pin non esiste, le aree di griglia `south/north/line` non vengono orfanate perché `.voyage` non è più una griglia. Il disegno è **una sola scatola a ogni larghezza**, misurata: 1240×317 a 1440, 1096×282 a 1280, 688×180 a 768, 350×180 a 390. |
| 6 | Spostare `view-timeline-name` su `.voyage__stations` | **FATTO nella sostanza, CONTESTATO nella collocazione.** La timeline non sta più su `.home-pilot` — quella parte della critica è accolta. Non va però sulla lista: va **sul disegno**, `.voyage__chart`. Misura con `animation-range: cover 15% contain 100%`: a 1440×900 la linea comincia quando il bordo superiore della carta è a y = 710 del viewport e **finisce quando è a y = 80, con il bordo superiore della lista delle tappe a y = 396** — cioè il tracciato è completo nell'istante in cui il registro arriva all'altezza di lettura. A 390×844: finisce a y = 40 con la lista a y = 220. Sulla lista non funzionerebbe: `.voyage__stations` è alta **93 px** a 1440 (misurato), un decimo della corsa necessaria, e la linea sarebbe ancora a metà quando la lista è già letta. |
| 7 | Separare *corrente* da *superata* per forma, non con due teal | **FATTO per soppressione**: lo stato per tappa non esiste più (vedi 8). Nessun colore porta uno stato in questo capitolato. `--terr-line` disegna **solo** la rotta e le sue tacche — che è testualmente l'uso che `DESIGN_SYSTEM_V2.md` §1.1 le assegna («isoipse, tacche, **rotta** su scuro»). Correzione in più: oggi `.voyage__line` e `.voyage__station` sono disegnate in `--accent-dark` (voyage.css 96, 106), cioè l'accento interattivo su una grafica — una violazione della regola 1 già in produzione. §4.4 la ripara. |
| 8 | Ripensare `aria-current="step"` sulle tappe del pilota | **FATTO, accolto per intero.** Niente `aria-current`, niente `.is-current`, niente `.is-reached`, nessun osservatore di tappa. La sequenza prescritta resta un `<ol>` di etichette bloccate. L'argomento della revisione è corretto e il commento di `_pilot.html` lo dice già: il pilota non è un canale autorizzato, e la posizione di lettura non è una posizione di processo. |
| 9 | Limitare il tratto 600 ms ai capitoli immersivi | **FATTO per soppressione**: `--motion-trace` non viene creato, il ruolo `figure` non esiste, nessuna quinta durata. L'unico tratto lungo resta `--motion-draw` (900 ms) dove già sta, nell'hero. Il disegno della rotta non ha durata: è legato allo scroll. |
| 10 | Registrare il file | **FATTO**, con le righe esatte: §4.1. |
| 11 | I 2 px della barra, colore di riposo delle tacche, `pointer: coarse` | **FATTO per soppressione.** Nessuna barra, quindi `--header-height` invariato, `border-block-end` di `.site-header` invariato, `scroll-padding-block-start` **invariato** (la §6 del round 1 lo cambiava senza bisogno: misurato, `--header-height` + `--s-4` = 80 px contro un'altezza d'header renderizzata di **65 px**, quindi già sufficiente), nessun bersaglio invisibile su `pointer: coarse`. |
| 12 | Contraddizione di direzione | **FATTO.** Un'unica regola, scritta una volta: **ogni escursione di reveal parte da sotto e sale al suo posto**, `translateY(+N → 0)`. La cucitura non trasla affatto: si disegna, `scaleX(0 → 1)` dal lato di lettura. Non può comparire un bordo duro di mezzanotte sopra il gradiente perché **non c'è più gradiente** e non c'è più traslazione: il fondo del capitolo è dipinto dalla sezione stessa, come oggi. |
| 13 | Alzare l'ampiezza o dichiarare l'answer incompleta | **FATTO, con numeri.** Il capitolo del pilota passa da **140 px** di superficie disegnata (`.voyage__svg`) a **531 px di lastra fotografica + 317 px di carta = 848 px** a 1440; la sezione da 750 a **1 484 px**; la pagina da 7 921 a **8 655 px**. A 390 dove §1.6 misurava **zero** grafica legata allo scroll, la carta esiste: 350×180. L'immagine è la `.plate--chapter` di `imagery.md` §4.3 — §8.4 dice esattamente quale metà è delegata e quali due cose chiedo a quella specifica. |

Le **violazioni** 1–7 e le **lacune** 1–17 della revisione sono riprese una per una in §4.5 e §8.2; le sette che la revisione
chiama *cheap signal* sono eliminate, non difese, tranne una difesa esplicita in §8.3.

---

## 1. VERDETTO SULLO STATO ATTUALE (rimisurato in questo round)

**1.1 — L'89 % della pagina non si muove.** 1440×900: documento **7 921 px = 8,80 schermate**; `document.getAnimations()`
restituisce **3** animazioni — `tide-1` (28 s) e `tide-2` (34 s) su `DocumentTimeline`, `IMG.doorway__img` su `ViewTimeline`
(300). A `scrollY = 45 %` le prime due sono `paused` (corretto), la terza `finished`. Fra y = 900 e y = 7 921 **non esiste
alcuna animazione**.

**1.2 — Il reveal esiste in 2 sezioni su 10.** `[data-reveal]` = **11** (3 nell'hero, 8 nel pilota). Altezze misurate delle
otto sezioni che ne hanno zero: `_entrances` 1 010, `_orientation` 519, `_pathways` 987, `_trust` 1 002, `_antifraud` 537,
`_news` 516, `_ecosystem` 659, `_reserved` 214.

**1.3 — E dove esiste, è una sola animazione ripetuta 11 volte.** `shell.js` 52 e 66: `opacity 0→1` +
`translateY(-10px) scale(1.012)`, 320 ms, `--ease-out`, stagger 60 ms — identica per un titolo, un paragrafo e una tappa: la
prima riga di `ANTI_PATTERNS.md` §1. Parte da **−10 px**, cioè scende mentre lo scroll sale; e `scale(1.012)` su un
`--t-title` di 48 px lo porta a 48,58 px, ri-rasterizzando il testo per tutta la durata.

**1.4 — Le transizioni fra sezioni sono accostamenti.** Nove confini, `gapPx = 0` su tutti; `border-top-width: 0px` su 5;
due con lo stesso identico fondo sui due lati (`rgba(0,0,0,0)`): `trust → antifraud` e `ecosystem → reserved`.
`pathways → pilot` è un taglio netto fra `#F4F3F0` e `#0E1B23` con 1 px di `--hairline`.

**1.5 — L'unico oggetto legato allo scroll sotto l'hero gira sul thread principale.** `.voyage__line` non compare in
`document.getAnimations()`; `IMG.doorway__img` sì, con `timeline: ViewTimeline`. Motion non ha potuto accelerare
`strokeDashoffset` ed è ripiegato sul proprio driver JS (`home.js` 115-121). Il nativo c'è:
`CSS.supports('animation-timeline','scroll()') === true`, `CSS.supports('animation-timeline','view()') === true`.

**1.6 — Sotto 64rem lo scroll è fermo.** `voyage.css` 184-186 fa `.voyage__svg{display:none}` sotto 63.999rem. A 390×844 il
documento è alto **11 183 px = 13,25 schermate** — non 8 970, cifra del round 1 che non ho potuto riprodurre e che qui è
corretta — e su quei 11 183 px **non c'è una sola grafica legata allo scroll**. L'unica mutazione di stato è
`.site-header.is-scrolled`. È fatta bene ed è tutto.

**1.7 — Ciò che è già corretto.** Con `prefers-reduced-motion: reduce`: `scroll-behavior` → `auto`,
`document.getAnimations().length === 0`, **0 elementi `[data-reveal]` sotto opacità 1**. Precisione che mancava al round 1:
**10 elementi in tutto** stanno sotto opacità 1, e sono tutti stati di progetto voluti — `DIV.nav-overlay` (0, chiuso),
`IMG.doorway__img` (0.50, §8.4), `SPAN.doorway__glow` (0.70), i tre gradini (0.55 / 0.38 / 0.24) e quattro `svg.route__glyph`
(0.35). Nessuno è un reveal. Difetto di scoping reale: `html.js [data-reveal]:not(.is-in){opacity:0}` esiste solo dentro
`.hero` e `.voyage`, quindi la regola va generalizzata **insieme** al `html.js` che la protegge.

**1.8 — Due fatti nuovi di questo round, che cambiano il capitolato.**
(a) **Le sezioni sono figlie dirette di `<main>` solo sulla home.** Misurato: `main > section` = 10 sulla home, **0** su
`/fr/forum/` (le sue otto stanno in `div.forum-sections`), 0 su `/fr/glossaire/` (in `div.container.glossary`), 0 su
`/fr/faq/`, 0 su `/fr/entreprises/`, 1 su `/fr/parcours/`. Qualunque selettore «generale» sui confini di sezione sarebbe una
regola che non fa nulla su nove superfici su dieci. §4.2 lo risolve con un contratto esplicito, non con un selettore furbo.
(b) **Il contatore `folio` è già preso.** `register.css` 819-826 fa `.page-home main{counter-reset: folio}` +
`.page-home .section .folio__ordinal::before{counter-increment: folio}` e la home rende **6 blocchi `.folio`** su 10 sezioni
(`01 L'ÉCOSYSTÈME` … `06 PROMOTEUR ET PARTENAIRES`, verificato a schermo). Un secondo numero di sezione inventato da questo
capitolato sarebbe una seconda numerazione sulla stessa pagina. §4.5 e §8.4 ne traggono la conseguenza.

---

## 2. UI-UX-PRO-MAX — interrogazioni, esiti, decisioni

| # | Query (dominio) | Cosa è tornato | Decisione, rivista in round 2 |
|---|---|---|---|
| 1 | `scroll-linked animation scroll timeline reveal on scroll premium` (**ux**) | *Smooth Scroll*, *Horizontal Scroll*, *Motion Sensitivity* («Parallax/Scroll-jacking causes nausea») | **PARZIALE.** Presa la regola reduced-motion + stato finale leggibile. **RESPINTO** l'amalgama parallasse = scroll-jacking. Lo scroll-jacking resta vietato e qui non c'è: lo scroll è 1:1, nessuna intercettazione, nessun pin. |
| 2 | `scroll trigger pinned section sticky storytelling chapters` (**gsap**) | tre livelli con `scrub`, `pin:true`; «Don't pin more than 1-2 sections», «Pinning forces layout reflow» | **RESPINTO PER INTERO in round 2**, meccanismo *e* forma. Il round 1 prendeva il tetto di una sezione pinnata; la revisione ha ragione che il pin è la forma da catalogo e che la sua guardia («se la sincronia si perde si elimina il pin») pre-autorizzava a cancellare l'unica idea ambiziosa. Nessun pin, da nessuna parte. Tenuto solo lo **scrub** (moto legato, non temporale). |
| 3 | `parallax depth background layers scroll` (**style**) | `parallax-storytelling`: 3-5 livelli, `perspective:1px`, `scroll-snap`, `locomotive-scroll`, `cost:high` | **RESPINTO lo stile**, e in round 2 respinta anche la parallasse aggiunta: la sola che resta è quella che c'è già (§4.6). **ACCETTATA** la checklist (alternativa mobile, fallback reduced-motion, uscita sempre possibile). |
| 4 | `reading progress indicator long page navigation` (**ux**) | *Progress Indicators*, *Active State*, *Sticky Navigation* | **RESPINTO PER INTERO in round 2.** Il round 1 ne ricavava una barra di lettura; la revisione la chiama «l'ornamento da scroll più generico dell'ultimo decennio» e ha ragione. La pagina **numera già** le proprie sezioni con un dispositivo proprio (§1.8b): la risposta corretta è estenderlo, non affiancargli una barra. §8.4. |
| 5 | `stagger reveal text lines mask duration easing` (**gsap**) | SplitText, `expo.out`, `rotateX:-40`; «stagger ≤ ~8 children»; «y offset 8-16px so it reads as a fade, not a slide»; «don't reveal below-the-fold content as invisible-by-default without a no-JS fallback» | **ACCETTATO**, tradotto in numeri: escursione 6-10 px, stagger 40-60 ms, tetto 8 per gruppo (§4.3); il fallback no-JS corregge §1.7 ed è misurato (§6). **RESPINTO** SplitText (licenza, un nodo per carattere, `expo.out` non è una delle tre curve) e `rotateX` (ri-raster del testo). |
| 6 | `sticky header section anchor focus keyboard` (**ux**) | *Focus States*, *Focus Not Obscured (Enhanced)* (AAA), *Smooth Scroll* | **ACCETTATO**, precisando che si applica il **2.4.11 AA**. Senza barra e senza pin nulla può coprire il focus: `scroll-padding-block-start` resta `calc(var(--header-height) + var(--s-4))` = 80 px contro 65 px di header renderizzato (misurato). |
| 7 | `sticky pinned column staggered entrance hierarchy` (**product**) | **0 risultati** | Registrato allora, irrilevante ora: la colonna appiccicata non esiste più. |

**Merito.** Il bias dichiarato dello strumento («government = accessible & ethical, avoid motion effects») ha prodotto in 4
query su 6 lo stesso consiglio: *non animare*. È il registro respinto dal committente, e va contestato: WCAG 2.2 non vieta il
moto, ne richiede il **controllo** (2.3.3). Ma nel round 1 questo argomento è stato usato per tenere in piedi una barra di
progresso: contestare il bias non è una licenza a spedire l'ornamento generico.

---

## 3. 21ST.DEV — candidati confrontati, e che cosa resta preso in round 2

| Componente | URL | Cosa è buono | Esito in round 2 |
|---|---|---|---|
| **Scroll Reveal Content A** (abui) | `21st.dev/@abui/components/scroll-reveal-content-a` | Pin senza libreria: `sticky top-0 h-[100vh]` + fratello vuoto `h-[300vh]`. | **Nulla preso.** Il pin è uscito del tutto. Guida tutto con `useMotionValueEvent → setState`: re-render per frame. Tre `<Image>` sovrapposte tutte caricate. Nessun reduced-motion. |
| **Scroll 01** (felipemenezes098) | `21st.dev/@felipemenezes098/components/scroll-01` | Due tracciati responsive separati (lista sotto `md`, media `sticky` sopra). | **Preso il principio di due tracciati, non la forma.** Qui i due tracciati sono: registro a 8 colonne sopra 64rem, spina verticale sotto — che il progetto ha già. **Respinta** la dissolvenza-fuori (`opacity → 0` alle estremità: contenuto leggibile reso invisibile da una posizione di scroll). |
| **Element scroll-linked animation** (motiondotdev) | `21st.dev/@motiondotdev/components/motion-scroll-container` | Lega `pathLength` di un tracciato a `scrollXProgress`: la proprietà SVG giusta, normalizzata 0-1. | **PRESO, ed è il cuore di §4.4** — ma in CSS nativo, non in React: `pathLength="1"` è già nel markup del progetto (`_pilot.html` 34) e `@keyframes voyage-draw` lo scrubba su una `ViewTimeline`. **Respinta** la maschera animata (`maskImage` interpolato = paint per frame). |
| **Scroll Progress** (ibelick) | `21st.dev/@ibelick/components/scroll-progress` | `scaleX` con origine logica: forma corretta, zero paint. | **RESPINTO PER INTERO in round 2.** Il round 1 ne prendeva la meccanica e ne rifiutava lo scopo; la revisione osserva che il risultato a schermo resta quel componente. Niente barra. |
| **Progress Indicator** (su2491251) | `21st.dev/@su2491251/components/progress-indicator` | — | **Respinto.** |
| **Product Timeline** (hyperiux) | `21st.dev/@hyperiux/components/timeline` | Dichiara esplicitamente reduced-motion e i due temi. | **Respinto il meccanismo** (Lenis + GSAP: smooth scroll globale, vietato). **Adottata l'abitudine** di dichiarare lo stato ridotto in ogni voce (§5). |
| **Container Scroll Animation** (aceternity) | `21st.dev/@manuarora700/components/container-scroll-animation` | — | `rotateX` 3D su un contenitore durante lo scroll: la firma più riconoscibile del catalogo generato. **Respinto.** |
| **Inversion Circle Scroll Animation** (ajith66310) | `21st.dev/@ajith66310/components/inversion-circle-scroll-animation` | L'idea di **far entrare** un capitolo scuro invece di accostarlo risponde a §1.4. | **Preso il problema, respinta la soluzione** (un cerchio nero in `clip-path` è una tenda). La risposta di §4.2 non è un'entrata in scena: è un **bordo di foglio disegnato**, e ciò che «entra» nel capitolo è la sua lastra fotografica. |
| **Reveal** (asanshay) | `21st.dev/@asanshay/components/reveal` | — | «Fades and **un-blurs**»: `filter: blur()` animato, fuori budget. **Respinto.** |

**Regola di adozione, riscritta.** Dei nove, in round 2 **uno solo** lascia qualcosa nel codice: `pathLength` normalizzato.
Tutto il resto del capitolato viene dal sistema grafico del progetto (graticola con tacche, rotta fra due rive, folio, registro)
o esce. Il round 1 prendeva «il pin CSS, le soglie, `scaleX` con origine logica, i due tracciati»: quattro prestiti di forma da
un catalogo che lo stesso documento dichiarava di rifiutare.

---

## 4. LA PROPOSTA — «una carta, non una pagina»

Due idee, non tre e non dieci.

**(a) Ogni passaggio di sezione è il bordo di un foglio di carta**, disegnato: una linea di graticola a tutta larghezza con la
sua scaletta di tacche, che si traccia dal lato di lettura quando il confine entra in vista. Non è un gradiente e non è un bordo.

**(b) Il capitolo del pilota diventa una carta**: una lastra fotografica in testa al capitolo, sotto di essa la rotta fra le due
rive disegnata a misura d'architettura — 317 px invece di 140 — con le sue stazioni a tacche allineate al registro delle otto
tappe, e il tracciato legato allo scroll in CSS nativo. È l'unico oggetto indicizzato allo scroll che questo capitolato
aggiunge.

Più una manutenzione: il reveal generico diventa **tre ruoli dichiarati**, e il driver JS della rotta sparisce.

### 4.0 Meccanismo — CSS nativo prima, Motion dove il CSS non arriva

- **grafica legata allo scroll** → CSS `animation-timeline: view()` dentro `@supports (animation-timeline: view())` e dentro
  `@media (prefers-reduced-motion: no-preference)`. **Il riposo è sempre lo stato finale**: senza supporto la pagina è finita,
  mai rotta. Verificato: `stroke-dashoffset: 0` è il valore fuori dai due blocchi.
- **misura, orchestrazione, stato** (stagger, cuciture) → `IntersectionObserver` e Motion, **una volta per elemento, zero
  lavoro per frame**. Vietato un handler `scroll` che scrive stile.
- **Collaudo.** `document.getAnimations().filter(a => a.timeline?.constructor.name.endsWith('Timeline') && a.timeline.constructor.name !== 'DocumentTimeline')`
  deve contenere **ogni** oggetto legato allo scroll della pagina e nient'altro. Misurato sul candidato a 1440×900:
  `voyage-draw / ViewTimeline` e `IMG.doorway__img / ViewTimeline`. Due, contro due capitoli mezzanotte.

### 4.1 File toccati — l'elenco completo, con le righe

**Nuovo `static/css/v3/scroll.css`.** Registrazione, che il round 1 aveva dimenticato:

1. `static/css/main.css`, in coda (oggi l'ultimo `@import` è `v3/buttons.css`, riga 25):
   ```css
   @import url("v3/scroll.css");
   ```
2. `templates/base.html`, dopo la riga 38 (`<link rel="preload" href="{% static 'css/v3/buttons.css' %}" as="style">`):
   ```django
   <link rel="preload" href="{% static 'css/v3/scroll.css' %}" as="style">
   ```
   Senza queste due righe il foglio non si carica: `base.html` 39 carica **un solo** stylesheet, `css/main.css`.

**`templates/base.html`**, riga 57 — un attributo, ed è il solo contratto di cucitura:
```django
<main id="main-content" tabindex="-1" data-seam-set>
```

**`templates/pages/partials/_section_header.html`** — tre attributi, e coprono **sei** sezioni della home in un colpo
(`_entrances`, `_orientation`, `_pathways`, `_trust`, `_news`, `_ecosystem`: misurato, sono gli unici sei consumatori del
partial):
```django
<p class="folio" data-reveal="plate">                      <!-- riga 18 -->
<h2 class="section__title" … data-reveal="plate">          <!-- riga 24, su entrambi i rami dell'{% if %} -->
<p class="section__lead" … data-reveal="plate">            <!-- riga 25 -->
```

**`templates/pages/home/_pilot.html`** — ristrutturato, §4.4 dà il markup completo.

**`templates/pages/home/_antifraud.html`** — non usa il partial condiviso: `data-reveal="plate"` sulle righe 11 e 12,
`.antifraud-panel__title` e `.antifraud-panel__body` (2 elementi, stesso genitore `.antifraud-panel__content`, quindi un
gruppo). Non sulla nota né sull'azione: un pannello d'avvertimento non si annuncia in quattro tempi.

**`templates/pages/home/_reserved.html`**, riga 7 — la classe che oggi manca, ed è il confine invisibile di §1.4:
```django
<section class="section section--d home-reserved" id="{{ s.anchor }}" …>
```
Nessun `data-reveal`: un pannello di rango D in fondo alla pagina non ha bisogno di annunciarsi (§4.3, tetto di gruppi).

**`apps/core/templatetags/ile_core.py`**, `voyage_route` (riga 123) — due chiavi in più per stazione, e **niente altro**.
Motivo in §4.4 (le stazioni non possono più essere cerchi). È una derivazione di disegno: nessuna vista, nessun modello,
nessun contratto dati.
```python
stations.append({
    "x": f"{x:.1f}", "y": f"{y:.1f}",
    "y1": f"{y - 5:.1f}", "y2": f"{y + 5:.1f}",   # la tacca di stazione, ±5 unità utente
    "index": i + 1,
})
```

**`static/js/src/shell.js`** — i tre ruoli di reveal e l'osservatore delle cuciture (§4.2, §4.3: codice completo).

**`static/js/src/home.js`** — **si cancellano le righe 106-123**, il blocco «THE ROUTE BETWEEN TWO SHORES»: il driver JS della
rotta (§1.5) passa al CSS.

**`static/css/v2/voyage.css`** — si cancellano le righe **87-109** (`.voyage__svg`, `.voyage__line`, `.voyage__station`:
riscritte in `scroll.css`) e la riga **184-186** (`.voyage__svg{display:none}` sotto 63.999rem: il disegno esiste a ogni
larghezza). Le righe 40-51 (`.voyage` come griglia a tre aree) si riducono a `display: block`. Tutto il resto del file —
stazioni, spina, RTL, forced-colors — resta.

**Che cosa NON viene toccato:** `templates/partials/header.html` (zero righe), nessuna vista, nessun servizio, nessun tag di
navigazione, nessun template di piattaforma, nessuna pagina DENSE o LEGAL.

### 4.2 La cucitura — il bordo di graticola

**Il problema, misurato (§1.4):** nove confini, cinque senza bordo, due invisibili, uno che è un taglio netto fra
`#F4F3F0` e `#0E1B23`.

**La risposta.** Il progetto ha già un linguaggio per il bordo di un foglio: `DESIGN_SYSTEM_V2.md` §6 prescrive una
«graticola 160 px **con tacche**». Ogni confine di sezione è il **bordo di graticola** del foglio che arriva: un filetto a
tutta larghezza e, appesa a esso, una scaletta di tacche al passo dichiarato di 160 px. Si traccia dal lato di lettura quando
il confine entra in vista, una volta, in 240 ms. Non è un gradiente (il round 1 ne aveva due, 128 px + 96 px: spariscono), non
è un effetto, non somiglia a un componente di catalogo, e a 1440 px è **1 440 px di filetto più nove tacche** invece delle due
lineette di 1×16 px che la revisione giustamente chiamava impercettibili.

**Il contratto di portata, esplicito.** `[data-seam-set] > section + section`. `base.html` mette `data-seam-set` su `<main>` e
basta. Misurato: **9 cuciture sulla home**, **0** su `/fr/forum/`, `/fr/glossaire/`, `/fr/faq/`, `/fr/entreprises/`,
`/fr/parcours/`, `/fr/privacy-policy/` — perché su quelle superfici le sezioni non sono figlie dirette di `<main>` (§1.8a).
Non è una regola che fallisce in silenzio: è una regola che **si adotta con un attributo** sul proprio contenitore, e §8.4 dice
a chi tocca farlo.

**Il gate del moto, strutturale.** La cucitura è *disegnata* ovunque; **si traccia** solo dove esiste un capitolo mezzanotte,
cioè solo in IMMERSIVE e RICH (`DESIGN_SYSTEM_V2.md` §7 concede i capitoli scuri solo lì). Il gate non ha bisogno di un
attributo nuovo: `html:has(main .chapter--dark)`. Misurato: `true` sulla home (2 capitoli), `false` sul glossario, sulle note
legali, sul login, sulla FAQ, sui parcours, sulle actualités, sull'orientamento, sulle landing d'ecosistema e sul forum
com'è oggi. Su DENSE e LEGAL non si accende nulla, per costruzione e non per euristica.

```css
:root {
  --seam-rule: var(--hairline-strong);   /* 3,37:1 su --min-0 · 3,14:1 su --min-1 (calcolati) */
  --seam-tick: var(--hairline);          /* 1,37:1 — ritmo, non informazione */
  --seam-h: 10px;
  --seam-tick-h: 6px;
  --seam-pitch: 160px;                   /* il passo di graticola di DESIGN_SYSTEM_V2 §6 */
}

[data-seam-set] > section { position: relative; }

[data-seam-set] > section + section::before {
  content: "";
  position: absolute;
  inset-inline: 0;
  inset-block-start: 0;
  block-size: var(--seam-h);
  background:
    linear-gradient(to bottom, var(--seam-rule) 0 1px, transparent 1px) no-repeat 0 0 / 100% 100%,
    repeating-linear-gradient(to right, var(--seam-tick) 0 1px, transparent 1px var(--seam-pitch))
      no-repeat 0 0 / 100% var(--seam-tick-h);
  transform-origin: left;
  z-index: 1;
  pointer-events: none;
}

[dir="rtl"] [data-seam-set] > section + section::before {
  transform-origin: right;
  background-position: 100% 0, 100% 0;   /* la scaletta parte dal lato di lettura */
}

/* Il fondo che arriva decide l'inchiostro del bordo: è il bordo del foglio che arriva. */
.chapter--dark { --seam-rule: var(--on-dark-3); --seam-tick: var(--hairline-dark-strong); }

/* RIPOSO = STATO FINALE. Il nascondiglio vive qui dentro e in nessun altro posto. */
@media (prefers-reduced-motion: no-preference) {
  html.js:has(main .chapter--dark) [data-seam-set] > section + section:not(.is-seamed)::before {
    transform: scaleX(0);
  }
  html.js:has(main .chapter--dark) [data-seam-set] > section + section::before {
    transition: transform var(--motion-base) var(--ease-out);
  }
}

@media (forced-colors: active) {
  [data-seam-set] > section + section::before {
    background: none;
    border-block-start: 1px solid CanvasText;
    forced-color-adjust: none;
  }
}
```

`::after` di queste sezioni **resta libero**, deliberatamente: il round 1 aveva speso entrambi gli pseudo-elementi e non
aveva più dove mettere la propria firma. Qui ne basta uno.

**Contrasti, calcolati (luminanza relativa WCAG 2.x, non stimati).**
`--hairline-strong` #7A868B su `--min-0` #F4F3F0 = **3,37:1**; su `--min-1` #ECEBE6 = **3,14:1**; su `--min-2` = **3,59:1**.
`--on-dark-3` #8FA0A3 su `--mid-1` #0E1B23 = **6,44:1**. Le tacche sono ritmo, non informazione: `--hairline` = 1,37:1 su
`--min-0`, `--hairline-dark-strong` composita in `#465359` su `--mid-1` = **2,20:1**. Il confine è comunque portato dal
cambio di fondo e dall'intestazione della sezione: il bordo lo **rinforza**, non lo sostituisce, e quindi non è «parte di una
grafica necessaria a capire il contenuto» (1.4.11). Il filetto sta sopra 3:1 in ogni caso.

**JS, in `shell.js` — completo.**
```js
/* 3. Le cuciture: una classe per confine, una volta. ORIENTAMENTO. */
const seams = [...document.querySelectorAll("[data-seam-set] > section + section")];
if (seams.length && document.querySelector("main .chapter--dark")) {
  withMotion(
    () => {
      const io = new IntersectionObserver(
        (entries) => {
          for (const e of entries) {
            if (!e.isIntersecting) continue;
            e.target.classList.add("is-seamed");
            io.unobserve(e.target);
          }
        },
        { rootMargin: "0px 0px -10% 0px" },
      );
      seams.forEach((el) => io.observe(el));
    },
    () => seams.forEach((el) => el.classList.add("is-seamed")),
  );
}
```
Il ramo `settle` è cintura e bretelle: con moto ridotto il blocco `no-preference` del CSS non si applica e la cucitura è già
disegnata. Verificato a schermo: con `prefers-reduced-motion: reduce` il `transform` calcolato dello pseudo-elemento è `none`.

### 4.3 I tre ruoli del reveal

`data-reveal` diventa `data-reveal="plate|register|tile"`; il valore vuoto vale `plate`, così i tre `data-reveal` dell'hero
non cambiano. Tutti **one-shot**: un testo leggibile non può tornare invisibile scorrendo in su, quindi lo scrub legato allo
scroll è riservato alla **grafica**.

| Ruolo | Dove | Proprietà | Durata | Stagger | Innesco (`inView`, una volta) |
|---|---|---|---|---|---|
| `plate` | il blocco d'apertura di una sezione: folio, titolo, lead | `opacity 0→1` + `translateY(10 → 0)` | 320 ms | 60 ms, **max 3** | margine `0 0 -18% 0` |
| `register` | le righe di una sequenza ordinata o di una tabella (`.voyage__stations`) | `opacity 0→1` + `translateY(6 → 0)` | 240 ms | 40 ms, **max 8** poi 0 | `0 0 -12% 0` |
| `tile` | una griglia di schede | `opacity 0→1` + `translateY(10 → 0)` | 320 ms | 60 ms, **max 4** per riga | `0 0 -15% 0` |

`tile` **non ha un solo uso in questo capitolato** ed è dichiarato apposta: le quattro vie e le otto schede dei parcours
appartengono a `public-sections.md`, e quando quella specifica le rivelerà deve usare questo ruolo e non inventare un quarto
meccanismo. Detto qui perché un ruolo non dichiarato è un ruolo che qualcuno riscrive.

Curva sempre `--ease-out`. Sparisce `scale(1.012)` (§1.3). **L'escursione è positiva in tutti e tre: l'elemento parte da sotto
e sale al suo posto**, nella direzione dello scroll — la contraddizione del round 1 (una regola che diceva «sale» e un numero
che diceva `-14px`) non esiste più perché non c'è più un solo numero negativo nel documento.

**Il tetto si conta in GRUPPI, non in elementi.** Un gruppo è ciò che l'occhio percepisce come un evento: gli elementi con lo
stesso ruolo e lo stesso genitore. **≤ 12 gruppi per pagina.** Misurato applicando gli attributi di §4.1 al DOM reale della
home e facendo girare la funzione di raggruppamento qui sotto: **31 elementi in 9 gruppi** — 1 `plate` nell'hero (già
esistente, `.hero__copy`), 7 `plate` su `.section__header` (sei dal partial condiviso più quello del pilota; uno ne ha 2
perché quella sezione non ha lead), 1 `register` di 8 (`.voyage__stations`, già esistente). Più il gruppo di 2
dell'antifrode, che non usa il partial: **10 gruppi, 33 elementi**. Due gruppi di margine sul tetto. Contare gli elementi —
come faceva il tetto «≤ 40 per pagina» del round 1 — non misura nulla: dieci intestazioni che entrano con lo stesso fade sono
dieci eventi identici, ed è la prima riga di `ANTI_PATTERNS.md` §1 anche se gli elementi sono trenta.

**CSS — solo il nascondiglio; il moto è JS.**
```css
:root {
  --reveal-lift: 10px;        /* plate, tile */
  --reveal-lift-fine: 6px;    /* register */
}

@media (prefers-reduced-motion: no-preference) {
  html.js [data-reveal]:not(.is-in) { opacity: 0; }
  html.js [data-reveal="plate"]:not(.is-in),
  html.js [data-reveal="tile"]:not(.is-in) { transform: translateY(var(--reveal-lift)); }
  html.js [data-reveal="register"]:not(.is-in) { transform: translateY(var(--reveal-lift-fine)); }
}
```
I due token sono la sola sede dei due numeri: il JS di `shell.js` li ripete nella tabella `ROLES` perché Motion anima in
JavaScript, e la coppia va tenuta allineata a mano — è l'unico punto di duplicazione del capitolato e lo dichiaro.
**Entrambi i token sono usati** — la revisione contava tre token
dichiarati e mai usati nel round 1, con i valori riscritti a mano accanto; qui il valore vive in un posto solo.
`--seam-lift` non esiste, perché la cucitura non trasla.

Il nascondiglio sta **dentro** `no-preference`, non fuori con un annullamento dopo: così lo stato ridotto è completo per
costruzione e non per correzione, come chiede `MOTION_SYSTEM.md` §3 («fuori da quel blocco il valore è quello finale»).
Verificato con `prefers-reduced-motion: reduce`: **0 elementi `[data-reveal]` sotto opacità 1**. Verificato con JavaScript
disattivato: `<html class="no-js">`, quindi `html.js` non si applica e **nulla è nascosto**.

**JS — `shell.js`, sostituisce interamente il blocco 2 attuale (righe 32-74).**
```js
const ROLES = {
  plate:    { lift: 10, duration: 0.32, stagger: 0.06, cap: 3, margin: "0px 0px -18% 0px" },
  register: { lift:  6, duration: 0.24, stagger: 0.04, cap: 8, margin: "0px 0px -12% 0px" },
  tile:     { lift: 10, duration: 0.32, stagger: 0.06, cap: 4, margin: "0px 0px -15% 0px" },
};

const reveals = [...document.querySelectorAll("[data-reveal]")];
const settleAll = () => reveals.forEach((el) => el.classList.add("is-in"));

/* Un GRUPPO = stesso ruolo + stesso genitore: è ciò che l'occhio percepisce come un evento.
   La chiave della mappa è una stringa `role` per ogni genitore, tenuta in una mappa annidata
   perché un genitore può ospitare due ruoli (un'intestazione `plate` e una lista `register`). */
const groupsOf = (els) => {
  const byParent = new Map();
  for (const el of els) {
    const role = Object.hasOwn(ROLES, el.dataset.reveal) ? el.dataset.reveal : "plate";
    if (!byParent.has(el.parentElement)) byParent.set(el.parentElement, new Map());
    const byRole = byParent.get(el.parentElement);
    if (!byRole.has(role)) byRole.set(role, []);
    byRole.get(role).push(el);
  }
  return [...byParent.values()].flatMap((byRole) => [...byRole].map(([role, list]) => [role, list]));
};

withMotion(() => {
  for (const [role, els] of groupsOf(reveals)) {
    const r = ROLES[role];
    const play = (targets, staggered) => {
      targets.forEach((el) => el.classList.add("is-in"));
      animate(
        targets,
        { opacity: [0, 1], transform: [`translateY(${r.lift}px)`, "translateY(0)"] },
        {
          duration: r.duration,
          ease: EASE_OUT,
          // Oltre il tetto del ruolo lo scaglionamento si spegne: una cascata di dodici
          // elementi non è più gerarchia, è attesa.
          delay: staggered && targets.length <= r.cap ? stagger(r.stagger) : 0,
        },
      );
    };
    inView(
      els[0],
      () => {
        const pending = els.filter((el) => !el.classList.contains("is-in"));
        if (pending.length) play(pending, true);
      },
      { margin: r.margin },
    );
    // Un fratello che entra molto più in basso ha il proprio innesco, o arriverebbe non visto.
    els.slice(1).forEach((el) =>
      inView(
        el,
        () => {
          if (!el.classList.contains("is-in")) play([el], false);
        },
        { margin: "0px 0px -8% 0px" },
      ),
    );
  }
}, settleAll);
```

**Il sistema di reveal legacy non si incrocia con questo, e l'ho misurato.**
(a) `[data-reveal]` **non** seleziona `[data-reveal-once]`: verificato in Chromium,
`document.createElement('div')` con `data-reveal-once="true"` → `.matches('[data-reveal]')` === **false**. I selettori
d'attributo confrontano il *nome* esatto, quindi `templates/orientation/result.html:81` non è toccato — la lacuna 14 della
revisione poggia su un'equivalenza che il browser non fa.
(b) `.reveal` / `.reveal--stagger` (`static/js/main.js` 338-360, `static/css/components.css` 3075-3092) vive in **due
template soli**, `templates/components/hero.html:24` e `templates/components/timeline.html:8`, e in **zero** elementi della
home (misurato: `document.querySelectorAll('.reveal').length === 0`). I due sistemi sono disgiunti oggi. **Regola per quando
non lo saranno:** un elemento non porta mai `.reveal` e `[data-reveal]` insieme; chi migra un componente toglie la classe
nello stesso commit in cui aggiunge l'attributo. `--reveal-index` resta di `main.js` e non è toccato.

### 4.4 La carta del pilota

**Il problema.** Il capitolo mezzanotte del pilota ha 750 px di altezza e **140 px** di superficie disegnata, un SVG alto come
una riga di testo; sotto 64rem non ha niente. Il committente dice che il sito non ha immagini. Questa è la sezione dove
un'immagine è ammessa (`DESIGN_SYSTEM_V2.md` §6: «Altre fotografie solo su IMMERSIVE e RICH, art-directed») e dove significa
qualcosa.

**La risposta: il capitolo diventa una carta.** Tre bande, in quest'ordine, tutte dentro il contenitore:

1. **Il blocco d'apertura** — folio, titolo, lead (ruolo `plate`).
2. **La lastra** — `.plate--chapter` di `imagery.md` §4.3: 21:9, gradazione `-notte`, `<figure>` + `<figcaption>`
   obbligatoria. Misurata al suo posto: **1 240×531 px** a 1440, 1 096×470 a 1280, 688×295 a 768, e **350×233 in 3:2** a 390
   (§8.4, richiesta di coordinamento n. 2).
3. **La carta** — `.voyage__chart`, alta `clamp(180px, 22vw, 320px)`: misurata **1 240×317** a 1440, 1 096×282 a 1280,
   688×180 a 768, 350×180 a 390. Dentro, la rotta fra le due rive con le sue stazioni e le due rive nominate agli angoli.
4. **Il registro** — le otto tappe prescritte, come oggi: otto colonne sopra 64rem, spina verticale sotto.

Superficie disegnata o fotografica del capitolo: **da 140 px a 848 px** a 1440. Sezione: **da 750 a 1 484 px**. Pagina: da
**7 921 a 8 655 px** (+9,3 %, 8,80 → 9,62 schermate) a 1440×900; da **11 183 a 11 590 px** (+3,6 %) a 390×844.

**Perché la carta sta nel contenitore e non a tutta larghezza — misurato.** L'allineamento fra le stazioni del disegno e le
colonne del registro è il motivo per cui il disegno esiste: lo dice il commento di `voyage.css` 53-56, che racconta di
essersi già sbagliato una volta. `voyage_route` mette la stazione *i* a `x = W/2n + (W − W/n)·i/(n−1)`, e
`.voyage__stations` è una griglia di `n` colonne uguali: i due centri coincidono **solo se i due elementi hanno la stessa
larghezza**. Con la carta a tutta larghezza e la lista nel contenitore, a 1440 le stazioni cadrebbero a 90, 246, 402 … contro
colonne centrate a 178, 333, 488 …: fino a 88 px di deriva. Nel contenitore, misurato a 1440: centri delle tacche
`[178, 333, 488, 643, 798, 953, 1108, 1263]`, centri delle colonne `[177,5, 332,5, 487,5, 642,5, 797,5, 952,5, 1107,5, 1262,5]`
— coincidono. A 1280: `[161, 298, 435, …]` contro `[160,5, 297,5, 434,5, …]`. L'ampiezza si compra con la lastra e con
l'altezza della banda, non rompendo l'unica cosa che il disegno deve garantire.

**Perché le stazioni non possono più essere cerchi.** `.voyage__svg` ha `preserveAspectRatio="none"`, quindi la viewBox
1200×140 viene stirata alla banda. A 140 px di banda lo stiramento era 1,2:1 e un cerchio era un ovale che non si notava; a
317 px diventa **1,89:1** e i cerchi si vedono come ellissi (schermata `chart_1440.png` del primo giro, prima della
correzione). Le stazioni diventano **tacche verticali** — che è anche il linguaggio giusto: la cucitura di §4.2 è una scaletta
di tacche, la rotta ne porta una per stazione, e la graticola del progetto è «160 px con tacche». Una linea verticale stirata
verticalmente resta una linea verticale; `vector-effect: non-scaling-stroke` tiene lo spessore in px di dispositivo. Costo:
le due chiavi `y1`/`y2` in `voyage_route` (§4.1). Altezza misurata della tacca: 23 px a 1440, 20 a 1280, 13 a 768 e 390.

**Perché `--terr-line` e non `--accent-dark`.** `DESIGN_SYSTEM_V2.md` §1.1 assegna a `--terr-line` «isoipse, tacche, **rotta**
su scuro» e §1.3 regola 1 riserva `--accent-dark` a link, CTA primaria e focus. Oggi `voyage.css` 96 e 106 disegnano rotta e
stazioni in `--accent-dark`: è l'accento interattivo su una grafica, una deviazione già in produzione. Qui si ripara.
Contrasto calcolato: `--terr-line` #3FA6AF su `--mid-1` #0E1B23 = **6,07:1**, sopra il 3:1 di 1.4.11 con margine, su un fondo
che è **tinta piatta e non fotografia** — il disegno non sta mai sopra la lastra, e questo è il motivo per cui non ci sta.

**Perché il disegno non sta sopra la fotografia.** L'ho calcolato prima di rinunciarci. La gradazione `-notte` di
`imagery.md` §4.2 porta il bianco a `#C8D4D6`; per tenere `--terr-line` a 3:1 sul pixel peggiore servirebbe un velo `--mid-1`
a **α = 0,75** (composita `#3C4950`, rapporto 3,22:1; a α = 0,70 si è a 2,79:1 e si è già sotto). Un velo al 75 % su una
fotografia da 85 KB è 85 KB spesi per il 25 % di una fotografia. La lastra resta una lastra, il disegno resta un disegno, e
il contrasto è deterministico in tutti e due.

**Markup — `templates/pages/home/_pilot.html`, la parte che cambia.**
```django
{% voyage_route d.steps|length as route %}
<div class="voyage">
  {% comment %} La lastra del capitolo: contratto, ritaglio, didascalia e byte sono di
  imagery.md §4.3/§4.4. Qui c'è solo il posto che occupa. {% endcomment %}
  {% include "components/plate.html" with photo=d.photo variant="chapter" %}

  <div class="voyage__chart">
    <svg class="voyage__svg" viewBox="0 0 {{ route.width }} {{ route.height }}"
         preserveAspectRatio="none" aria-hidden="true" focusable="false">
      <path class="voyage__line" pathLength="1" d="{{ route.d }}"/>
      {% for st in route.stations %}<line class="voyage__station"
        x1="{{ st.x }}" y1="{{ st.y1 }}" x2="{{ st.x }}" y2="{{ st.y2 }}"/>{% endfor %}
    </svg>
    <p class="voyage__shore voyage__shore--south">
      <span class="voyage__dot" aria-hidden="true"></span>{% translate "Maroc" %}</p>
    <p class="voyage__shore voyage__shore--north">
      {% translate "Vénétie" %}<span class="voyage__dot" aria-hidden="true"></span></p>
  </div>

  {% translate "Séquence du projet pilote" as sequence_label %}
  <ol class="voyage__stations" aria-label="{{ sequence_label }}"{% if d.steps_lang %} lang="{{ d.steps_lang }}"{% endif %}>
    {% for step in d.steps %}
    <li class="voyage__step" data-reveal="register"> … invariato … </li>
    {% endfor %}
  </ol>
</div>
```
Nessuna stringa nuova, nessuna etichetta nuova, nessun `aria-current`, nessun `hidden`, nessun elemento in più oltre alla
lastra. **`data-voyage` sparisce**: era l'aggancio del driver JS di `home.js`, e il driver si cancella (§4.1); un attributo che
nessuno legge è un attributo che qualcuno rileggerà per sbaglio.

**CSS.**
```css
:root {
  --chart-band: clamp(180px, 22vw, 320px);
  --chart-stroke: 2;     /* px di dispositivo, non-scaling-stroke */
  --chart-tick: 1.5;
}

.voyage { display: block; margin-block-start: var(--s-12); }

.voyage__chart {
  position: relative;
  block-size: var(--chart-band);
  margin-block: var(--s-8);
  contain: layout paint;
}

.voyage__svg { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; display: block; }

.voyage__line {
  fill: none;
  stroke: var(--terr-line);          /* 6,07:1 su --mid-1 */
  stroke-width: var(--chart-stroke);
  stroke-linecap: round;
  stroke-dasharray: 1;
  stroke-dashoffset: 0;              /* IL RIPOSO È LO STATO FINALE */
  vector-effect: non-scaling-stroke;
}

.voyage__station {
  stroke: var(--terr-line);
  stroke-width: var(--chart-tick);
  stroke-linecap: butt;
  vector-effect: non-scaling-stroke;
}

.voyage__shore {
  position: absolute; margin: 0;
  display: inline-flex; align-items: center; gap: var(--s-2);
  font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  letter-spacing: var(--track-folio); text-transform: uppercase;
  color: var(--on-dark-2);           /* 9,68:1 su --mid-1 */
  white-space: nowrap;
}
.voyage__shore--south { inset-block-end: 0; inset-inline-start: 0; }
.voyage__shore--north { inset-block-start: 0; inset-inline-end: 0; }
.voyage__dot { inline-size: 6px; block-size: 6px; border-radius: 50%; background: var(--terr-line); flex: none; }

@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .voyage__chart { view-timeline-name: --voyage; view-timeline-axis: block; }
    .voyage__line {
      animation: voyage-draw linear both;
      animation-timeline: --voyage;
      animation-range: cover 15% contain 100%;
    }
    @keyframes voyage-draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
  }
}

@media (forced-colors: active) {
  .voyage__line, .voyage__station { stroke: CanvasText; }
  .voyage__dot { background: CanvasText; forced-color-adjust: none; }
}
```

**L'intervallo, misurato e non scelto a occhio.** `cover 15% contain 100%` su `.voyage__chart`. A 1440×900 la linea comincia
quando il bordo superiore della carta è a y = 710 del viewport (la carta è appena entrata dal basso) e **finisce quando è a
y = 80 — appena sotto i 65 px dell'header — con il bordo superiore della lista delle tappe a y = 396**, cioè a metà schermo.
A 390×844: comincia analogamente, finisce a y = 40 con la lista a y = 220. Le altre quattro formule provate sono in
`m8_range.py`: `entry 90% exit 10%` e `cover 25% cover 75%` finiscono presto (carta a y = 30, lista a y = 346),
`entry 100% exit 0%` e `contain 0% contain 100%` danno lo stesso esito ma con 160 px di corsa in meno.

**Perché la curva è `linear`, dichiarato e non sottinteso.** `MOTION_SYSTEM.md` §1 vieta «`linear` fuori dai loop», e §2 dà
alla famiglia SCROLL la curva «—» perché la sua durata è «legata, non temporale». Su una `ViewTimeline` `linear` **non è una
curva di attenuazione**: è la mappatura identità fra distanza di scroll e avanzamento, cioè la condizione perché lo scroll
resti 1:1. Qualunque altra funzione renderebbe il disegno più veloce o più lento del dito. Non è una quarta curva e non entra
nel conteggio: la guardia che `MOTION_SYSTEM.md` §1 prescrive conta i `cubic-bezier` nel CSS compilato («al massimo tre»), e
`linear` non è un `cubic-bezier`. Nota di verità: quel test, `tests/frontend/test_motion_system.py`, **non esiste ancora** —
verificato, `tests/frontend/` contiene dieci file e non quello. Il foglio di §4 non scrive alcun `cubic-bezier` in proprio: i
tre restano `--ease-out`, `--ease-in` e `--ease-standard` di `v2/tokens.css` 104-106. `linear` compare in **una sola
dichiarazione** dell'intero capitolato, quella qui sopra.

**Perché `stroke-dashoffset` e non solo `transform`/`opacity`.** Il vincolo di prestazione dice «transform/opacity only».
`MOTION_SYSTEM.md` §2 sanziona esplicitamente l'eccezione — «Proprietà animabili: `transform`, `opacity`, e per gli SVG
`stroke-dashoffset` / `pathLength`» — ed è l'unica proprietà non-transform animata in tutto questo documento. Lo dichiaro qui
perché il round 1 animava anche `fill` e un colore di filetto senza dichiarare nulla.

**Sotto 64rem.** Nessun caso speciale, nessun `::before` da dirottare, nessuna timeline per tappa. La carta è la stessa
scatola, alta 180 px, con lo stesso disegno e lo stesso scrub; il registro sotto resta la spina verticale che `voyage.css`
172-232 disegna già. Si cancella soltanto `.voyage__svg{display:none}`. È la riga che rendeva ferma tutta la pagina mobile
(§1.6).

**Conteggio delle tappe.** Niente in questo capitolato dipende dal numero 8. L'altezza della banda è un `clamp()`; il
tracciato, le stazioni e le colonne vengono tutti da `d.steps|length` attraverso `voyage_route`; l'allineamento è garantito
dalla formula, non dal caso. L'unico numero misurato per otto tappe è l'altezza della sezione (1 484 px a 1440), e la formula
per *n* è `apertura + lastra(21:9) + banda + ceil(n/8)·riga di registro + nota + link`.

### 4.5 Ciò che è stato tolto, e perché

Questa sezione esiste perché nove delle diciassette lacune della revisione riguardavano cose che non ci sono più, e un
documento che le facesse semplicemente sparire sarebbe illeggibile contro la revisione che lo ha prodotto.

| Tolto | Era | Perché |
|---|---|---|
| **La barra di lettura** (`.readbar`, `.readbar__fill`, `.readbar__marks`, `--rail-h`, `--rail-track`, `--at`, la stringa «Sections de la page», le tre righe in `header.html`) | §4.5 del round 1 | Un filetto d'accento saldato sotto un header appiccicato è l'ornamento da scroll più generico dell'ultimo decennio, e il §3 del round 1 lo diceva prima di spedirlo. Inoltre, la pagina **numera già** le proprie sezioni con un dispositivo proprio (§1.8b): affiancargliene un secondo era dare due risposte alla stessa domanda. §8.4 consegna la risposta giusta alla specifica che possiede quel dispositivo. Effetti collaterali: `animation-timeline: scroll(root block)` non entra in `header.html`, quindi nessun fascicolo, nessuna lista, nessuna nota legale riceve moto legato allo scroll; nessun bersaglio di 44 px invisibile in cima a un viewport di 390 px; nessuna proprietà `--at` da dichiarare; nessuna stringa da tradurre in quattro lingue. |
| **La sezione pinnata** (`.voyage__figure`, `position: sticky`, `min-block-size: 24vh`, `scroll-margin-block-start`, i 1 340 px di corsa) | §4.4 del round 1 | «Colonna media appiccicata a sinistra, tappe che scorrono a destra» è la forma Aceternity/Apple che il §3 dello stesso documento rifiutava in due candidati su nove. E la sua guardia — «se la sincronia si perde in collaudo si elimina il pin» — pre-autorizzava a cancellare l'unica idea ambiziosa del capitolato. Con il pin spariscono anche il wrapper che orfanava le aree `south/north/line` sotto 64rem, il disegno per tappa sulla spina, il rischio tastiera, il rischio zoom 200 % su `24vh`, e l'aritmetica scritta a mano su otto tappe. L'ampiezza è stata ricomprata con la lastra e con la banda (§4.4), che non hanno un'uscita di sicurezza. |
| **Le due cuciture a gradiente** (`--seam-h` 128 px, `--seam-h-out` 96 px, `--seam-out`, `.chapter--dark::before/::after`, `:has(+ .section--process)`) | §4.2 del round 1 | «Un gradiente fra due sezioni» è ciò che una pagina generata fa per prima; la disciplina di due sole fermate era giusta e l'artefatto a schermo restava un gradiente. E la regola «ogni cucitura» invitava una pagina che si dissolve a ogni confine. |
| **La parallasse aggiunta** (`parallax.header-dark`, 10 px; la soglia che sale, 14 px) | §4.6 del round 1 | Dieci pixel su una schermata non sono profondità, sono un numero in una tabella che serviva a far arrivare il totale a 42. Tolti, la tabella di §4.6 ha una riga e quella riga esisteva già. |
| **Lo stato della tappa** (`.is-current`, `.is-reached`, `aria-current="step"`, il filetto `--terr-line` per «superata», l'osservatore a `rootMargin -45%`) | §4.4 del round 1 | Tre motivi, tutti della revisione e tutti fondati: annunciava una posizione di lettura come posizione di processo su contenuto legale prescritto; distingueva *corrente* da *superata* con due teal e nient'altro; e metteva `--terr-line` a fare lavoro di stato, contro `DESIGN_SYSTEM_V2.md` §1.3 regola 2. |
| **Il quarto ruolo di reveal** (`figure`, 600 ms) e **`--motion-trace`** | §4.3, §5 del round 1 | Una quinta durata contro `MOTION_SYSTEM.md` §1, e un tratto da 600 ms su un rail di giurisdizione, che è un componente RICH e non un capitolo immersivo (`ANTI_PATTERNS.md` §5, domanda 6). L'unico tratto che resta è quello che c'è già nell'hero, `--motion-draw` 900 ms. |
| **Le due tacche d'angolo 1×16 px** (`seam.ticks`) | §4.2 del round 1 | Erano dichiarate «la nostra firma»; a 1440 px erano due lineette nel margine. Una firma deve essere percepibile per funzionare da firma. Sostituite dal bordo di graticola a tutta larghezza (§4.2). |
| **`.section--rule` come regola generale** e la classificazione dei confini | §4.2 del round 1 | Non serve più classificare i confini: **tutti** i confini di §4.2 ricevono lo stesso bordo, cambi di suolo o no, quindi il caso «confine senza cambio di suolo» non esiste. `_reserved.html` prende comunque la classe `.section` perché senza di essa non è una sezione per nessuno (§1.4). |

### 4.6 Parallasse

| Soggetto | Escursione | Intervallo | Funzione |
|---|---|---|---|
| fotografia della porta (hero) | 18 px (**già esistente**, `home.js` 94-99, `6 → -12`) | `start start → end start` | profondità |

Nient'altro. Nessun `background-attachment: fixed`, nessun `perspective`, nessun `background-position` animato, nessun livello
di sfondo, **nessuna parallasse aggiunta da questo capitolato**. Il round 1 dichiarava «42 px su 10,3 schermate» come criterio;
il numero era composto da tre soggetti di cui due nuovi e da dieci pixel che nessuno avrebbe visto. Meglio uno vero.

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` §6

| Nome | Funzione | Innesco | Durata | Curva | Proprietà | Stato ridotto | Nota prestazioni |
|---|---|---|---|---|---|---|---|
| `seam.edge` | orientamento | `inView` ×1, margine `-10%`; solo se `html:has(main .chapter--dark)` | `--motion-base` 240 ms | `--ease-out` | `scaleX(0 → 1)` su `::before`, origine sul lato di lettura | **disegnato**, nessuna transizione | 1 layer di 1440×10 px, 9 per pagina, una volta ciascuno; nessun layout |
| `reveal.plate` | gerarchia | `inView` ×1, margine `-18%` | `--motion-slow` 320 ms | `--ease-out` | `opacity 0→1` + `translateY(10 → 0)`, stagger 60 ms | valore finale, immediato | ≤ 3 elementi per gruppo |
| `reveal.register` | gerarchia | `inView` ×1, margine `-12%` | `--motion-base` 240 ms | `--ease-out` | `opacity 0→1` + `translateY(6 → 0)`, stagger 40 ms | valore finale | oltre 8 elementi stagger 0 |
| `reveal.tile` | gerarchia | `inView` ×1, margine `-15%` | `--motion-slow` 320 ms | `--ease-out` | `opacity 0→1` + `translateY(10 → 0)`, stagger 60 ms | valore finale | ≤ 4 per riga; **dichiarato, nessun uso qui** (§4.3) |
| `voyage.route` | orientamento | `view()` su `.voyage__chart`, `cover 15% → contain 100%` | legata, non temporale | — (famiglia SCROLL; `linear` = identità, §4.4) | `stroke-dashoffset 1 → 0` su `pathLength="1"` | **tracciato disegnato** | `ViewTimeline` nativa; **sostituisce** il driver JS di §1.5; repaint limitato alla banda |

**Invariate e non toccate da questo capitolato:** `hero.tide` (il loop ambientale, 28 s + 34 s su due strati, in pausa fuori
viewport) e `doorway.photo` (18 px, `ViewTimeline`, `DESIGN_SYSTEM_V2.md` §8.4).

Cinque voci nuove contro le dodici del round 1; **una sola** è indicizzata allo scroll. Nessuna durata nuova, nessuna curva
nuova, nessuna molla, nessun overshoot. Ogni voce dichiara una delle sette funzioni e la sua gemella a moto ridotto.

---

## 6. ACCESSIBILITÀ E RTL

**Non cambia nulla che riguardi il focus, e questa è una correzione rispetto al round 1.** `scroll-padding-block-start`
resta `calc(var(--header-height) + var(--s-4))`. Misura: l'header renderizzato è alto **65 px** (64 + 1 px di bordo) e il
padding vale **80 px** — già sufficiente per il 2.4.11 AA (*Focus Not Obscured (Minimum)*: il focus non può essere
**interamente** coperto). Il round 1 ci aggiungeva 2 px per una barra che non c'è più. Nessun pin, nessuna colonna
appiccicata, nessun elemento fisso: niente può sovrapporsi a ciò che riceve il focus.

**Lo scroll resta 1:1.** Nessuna libreria, nessuno `scroll-snap`, nessuna intercettazione di `wheel`/`touchmove`.
`Page Down`, `Home`, `End`, `Space`, rotellina e barra di scorrimento fanno ciò che fanno oggi. Le ancore usano
`scroll-behavior: smooth`, già disattivato sotto `prefers-reduced-motion` (`base.css` 16-24; verificato: `auto`).

**Moto ridotto = stato completo, verificato e non asserito.** Con `prefers-reduced-motion: reduce` sul candidato a 1440×900:

| Controllo | Misura |
|---|---|
| `document.getAnimations().length` | **0** |
| elementi `[data-reveal]` sotto opacità 1 | **0** |
| `transform` calcolato di `::before` della prima cucitura | **`none`** (cioè disegnata) |
| `stroke-dashoffset` calcolato di `.voyage__line` | **`0px`** (cioè tracciata) |
| `scroll-behavior` di `<html>` | `auto` |
| elementi sotto opacità 1 in tutta la pagina | **10**, tutti stati di progetto voluti (§1.7) |

**Senza JavaScript**, verificato con `java_script_enabled=False`: `<html class="no-js">`, quindi né
`html.js [data-reveal]{opacity:0}` né il nascondiglio della cucitura si applicano. Nulla è invisibile, e non c'è nulla da
annullare.

**Colore mai solo.** In questo capitolato **nessun colore porta uno stato**, perché non c'è nessuno stato: lo stato di tappa
è stato tolto (§4.5). La cucitura è un fatto grafico, non un'informazione: il confine è portato dal cambio di fondo e
dall'intestazione, il bordo lo rinforza.

**`forced-colors: active`**, verificato in Chromium con `forced_colors='active'`: la cucitura perde i due gradienti
(`background-image: none`) e mostra un `border-block-start: 1px solid CanvasText` — misurato `border-top-width: 1px`,
`border-top-color: rgb(0, 0, 0)`. `.voyage__line` e `.voyage__station` diventano `CanvasText` — misurato
`stroke: rgb(0, 0, 0)`. Nulla sparisce.

**RTL e arabo**, verificato su `/fr/` → `http://127.0.0.1:8771/ar/` (200, `dir="rtl"`, `lang="ar"`, 10 sezioni, nessun
overflow orizzontale: `scrollWidth` 1440 = `innerWidth`):

- la cucitura si traccia dal lato di lettura: `transform-origin` calcolato = **`1440px 5px`**, cioè il bordo destro, e la
  scaletta di tacche parte da destra (`background-position` calcolato = `100% 0px, 100% 0px`). I gradienti verticali non si
  specchiano da soli — `transform-origin` non accetta parole chiave logiche — quindi la regola è scritta a mano ed è
  **l'unica** del foglio che lo richiede.
- la rotta ha già `[dir="rtl"] .voyage__svg { transform: scaleX(-1) }` (`voyage.css` 246-248): misurato
  `matrix(-1, 0, 0, 1, 0, 0)`. Il disegno usa `stroke-dashoffset`, non una trasformazione: nessun conflitto, e in arabo il
  tracciato si disegna **da destra**, che è corretto.
- le due rive usano `inset-inline-start/end` e si specchiano da sole; `:lang(ar) .voyage__shore { letter-spacing: 0 }` esiste
  già (`voyage.css` 250-254).
- **Zero stringhe nuove** in tutto il capitolato, quindi zero voci `.po` in `locale/{fr,it,en,ar}` e nessun rischio che un
  documento arabo annunci un'etichetta francese senza `lang` — che era la lacuna 12 della revisione.

**HUMAN_QA_REQUIRED.** (a) Firefox e Safari: `@supports` copre l'assenza di `animation-timeline`, ma il risultato *senza* va
guardato — la rotta deve apparire semplicemente disegnata. (b) Verifica vestibolare umana della carta a 1440×900 e del bordo
di graticola su nove confini di seguito: nove eventi identici a 240 ms sono un rischio di «cinema» che una misura non
cattura. (c) AR/RTL a 1440 e a 390, con la lastra al suo posto. (d) Zoom 200 % e `text-spacing` forzato: la carta è alta in
`vw`, non in `vh`, quindi non dovrebbe interagire con lo zoom del testo — da confermare. (e) Lettore di schermo sul capitolo
del pilota: la `<figcaption>` della lastra e l'`<ol>` delle tappe devono restare due cose distinte.

---

## 7. PRESTAZIONI

**Byte — CSS.** Il foglio di regole misurato (senza intestazione di commento): **4 167 B grezzi / 1 353 B gz**. Con
l'intestazione che questo progetto scrive su ogni file, stimo ~6,5 KB grezzi / ~2,0 KB gz. Contro i ~7,4 KB / 2,2 KB del
round 1, per un capitolato che fa di più: la differenza è tutta roba tolta.

**Byte — JS.** Misurato oggi: `chunks/chunk-P4EHGXV4.js` **26 120 B gz** + `home.js` **896** + `shell.js` **613** +
`motion.js` **189** = **27 818 B gz** (27,17 KiB). Budget 45 KB per pagina. `home.js` **perde** il driver della rotta
(righe 106-123); `shell.js` guadagna i tre ruoli e l'osservatore delle cuciture. Nessun import nuovo da Motion: `animate`,
`inView`, `stagger`, `withMotion` sono già nel chunk e `scroll` resta importato per l'hero. **Tetto che mi impongo:**
`shell.js` ≤ **2 048 B gz** (da 613), che porta la pagina a ≤ **29 253 B gz = 28,6 KiB**, cioè il **63 %** del budget, con
**16,4 KiB di margine**. Se l'implementazione sfora quel tetto, è il codice a essere sbagliato, non il budget.

**Paint, layout, frame — misurati, non asseriti.** Traccia `devtools.timeline` su 70 passi di scroll da 20 px attraverso il
capitolo del pilota, 1440×900, stesso intervallo per i due build:

| | Paint (eventi / ms) | Layout (eventi / ms) | UpdateLayoutTree | FunctionCall |
|---|---|---|---|---|
| build attuale | 202 / 87,9 | **2** / 0,7 | 91 / 11,4 | 913 / 70,4 |
| candidato | 259 / **128,3** | **4** / 1,5 | 120 / 12,7 | 811 / 70,2 |

Cioè **+40 ms di paint su 1,1 s di scorrimento continuo** — circa **0,58 ms per passo**, su un frame da 16,7 ms — e
**4 eventi di layout su 70 passi**. Il costo in più è il repaint della banda disegnata, che è passata da 140 a 317 px: è il
prezzo dichiarato dell'ampiezza, ed è misurato. Il tempo di `FunctionCall` è identico nei due build **soltanto perché il
banco di prova non può cancellare `home.js`**: il driver Motion della rotta gira ancora nel candidato. Nel build reale quelle
righe spariscono ed è l'unico JS per frame che quella sezione abbia (§1.5); il guadagno non è misurato qui e non lo rivendico.

**Nessun `filter`, nessun `box-shadow` animato, nessun `background-position` animato, nessun `will-change` permanente.** I due
gradienti della cucitura sono un `background` dipinto una volta; ciò che si muove è un `transform` su uno pseudo-elemento di
1440×10 px. `.voyage__chart` porta `contain: layout paint`, quindi il repaint della rotta non esce dalla banda.
**Per frame: zero JS** — nessun handler `scroll` scrive stile, gli `IntersectionObserver` scattano su soglia e si
disosservano, e lo scrub è nativo.

**Immagini.** **Zero byte aggiunti da questo capitolato.** La lastra è quella di `imagery.md` §4.3, dentro il suo tetto
dichiarato di ≤ 85 KB al capitolo del pilota e ≤ 120 KB per viewport. Questo documento fornisce il posto, la geometria
misurata e le due richieste di coordinamento (§8.4); non compra pixel per conto suo.

**Loop.** Invariati: uno per pagina (la marea dell'hero, su due strati come concede `DESIGN_SYSTEM_V2.md` §5), in pausa
fuori viewport. Le animazioni guidate dallo scroll non sono loop: non hanno durata propria e non girano a pagina ferma — ma
questa volta l'argomento è al posto giusto, perché la clausola che le riguarda è l'altra, ed è §0.

**Altezza.** 7 921 → **8 655 px** a 1440×900 (+9,3 %); 11 183 → **11 590 px** a 390×844 (+3,6 %). È il prezzo della lastra e
della banda. Se in collaudo la lettura risulta lunga, la leva è `--chart-band`: da `clamp(180px, 22vw, 320px)` a
`clamp(160px, 16vw, 240px)` toglie 87 px a 1440 senza toccare altro. La lastra non è una leva: è la risposta al committente.

---

## 8. RISCHI, GUARDIE E CONSEGNE

### 8.1 Rischi

1. **Nove cuciture identiche leggono come «cinema».** *Guardia:* durano 240 ms, sono una sola proprietà, sono una volta sola
   per confine, e si accendono **solo** dove c'è un capitolo mezzanotte (misurato: la home e nient'altro, oggi). Se in
   collaudo umano (§6, HUMAN_QA b) nove eventi di seguito risultano troppi, la leva è togliere la transizione e lasciare il
   bordo disegnato: una riga, e il disegno resta.
2. **Il bordo di graticola legge come «un bordo».** *Guardia:* è un bordo — di un foglio di carta, con la sua scaletta di
   tacche al passo che il sistema grafico dichiara. Il rischio vero è l'opposto: che a 1,37:1 le tacche siano invisibili. Le
   schermate `final_seam_{dark,light}_1440.png` dicono di no; il giudizio finale è umano.
3. **La lastra non arriva.** `imagery.md` §1.4 misura `MediaAsset.publishable == 0`: oggi **nessuna** fotografia è
   pubblicabile. *Guardia:* `components/plate.html` con `photo=None` non stampa nulla (imagery.md §4.5), quindi il capitolo
   resta esattamente com'è più la carta a 317 px — degradato, non rotto. Ma senza la lastra questo capitolato risponde solo a
   metà del reclamo del committente, e §8.4 lo dice per esteso.
4. **Supporto disomogeneo alle animazioni guidate dallo scroll** (Chromium sì, Firefox/Safari da verificare). *Guardia:*
   `@supports` + **riposo = stato finale**: il caso peggiore è la pagina finita e ferma, mai rotta, mai a opacità 0.
5. **Il contratto `data-seam-set` resta su una superficie sola.** *Guardia:* è dichiarato, misurato e consegnato (§8.4); il
   costo di adozione è un attributo per contenitore. Il rischio che resta è che nessuno lo adotti, e allora il sito avrà una
   home cucita e nove superfici no.
6. **`:has()` nel gate.** Supportato in Chromium, Firefox 121+ e Safari 15.4+. *Guardia:* se il selettore non è compreso, la
   regola intera cade e la cucitura resta **disegnata e ferma** — cioè il caso peggiore è lo stato ridotto, che è completo.
7. **Il capitolato non risponde a «dove sono a 6 000 px».** *Guardia:* non è una guardia, è una consegna. §8.4, punto 3.

### 8.2 Le lacune della revisione, una per una

1 la linea di livello → §4.2 (dispositivo sostituito, CSS completo). · 2 `--at` → tolto, test rieseguito. ·
3 `.voyage__figure` sotto 64rem → tolto. · 4 il disegno mobile → §4.4, la carta esiste a 390 (350×180, misurato). ·
5 la sincronia → §4.4, rimisurata con gli endpoint in pixel. · 6 registrazione → §4.1, righe esatte. ·
7-9 geometria/esistenza/moto ridotto della barra → tolta. · 10 tacche su `pointer: coarse` → tolte. ·
11 colore di riposo delle tacche → tolte. · 12 traduzione di «Sections de la page» → zero stringhe nuove. ·
13 token dichiarati e mai usati → **0**, verificato con la logica del test reale. · 14 il reveal legacy → §4.3, due misure. ·
15 portata → §1.8a e §4.2: dichiarata con i numeri, e ciò che non è coperto è consegnato (§8.4). ·
16 contraddizione di direzione → §4.3, una sola regola. · 17 aritmetica su otto tappe → §4.4, formula per *n*.

### 8.3 I segnali «cheap», uno per uno

1 barra di progresso → **tolta**. · 2 colonna appiccicata + scrollytelling → **tolto**. · 3 gradienti fra sezioni →
**tolti**. · 4 ampiezza totale → §4.4, da 140 a 848 px di superficie disegnata, +9,3 % di pagina. · 5 le tacche d'angolo di
1×16 px come «firma» → **tolte**, sostituite da un bordo a tutta larghezza. · 6 nessuna immagine → §4.4 + §8.4. ·
7 `--rail-track` al 16 % d'inchiostro → **tolto**. · 8 la dissolvenza da e verso il suolo → **tolta**.

**L'unico difeso.** La cucitura è un filetto di 1 px. Un filetto di 1 px a tutta larghezza, con una scaletta di tacche al
passo dichiarato del sistema, che si traccia dal lato di lettura, **è** il bordo di un foglio di carta geografica, ed è la
cosa che questo progetto disegna dalla prima riga di `DESIGN_SYSTEM_V2.md` §0 («un sistema grafico cartografico proprio:
graticola, curve di livello, una rotta con stazioni»). Rifiutarlo perché è sottile sarebbe rifiutare la direzione. Ciò che era
giusto rifiutare nel round 1 non era la sottigliezza: erano i 16 px di lunghezza.

### 8.4 Consegne ad altre specifiche — dichiarate, non implicite

Questo capitolato risponde alla **metà strutturale** del reclamo del committente sulla home: il ritmo, le cuciture, il
disegno, il moto. Tre cose che servono alla risposta completa appartengono ad altri documenti, e le chiedo qui per nome
perché una consegna non dichiarata è una lacuna.

1. **A `imagery.md` — richiesta di coordinamento n. 1.** `.plate--chapter` è dichiarata 21:9 e «terreno **sotto** la rotta»
   (§4.6 di quel documento). Qui la lastra è **sopra** la carta, non sotto, e non porta il disegno: il motivo è calcolato in
   §4.4 (un velo a α = 0,75 servirebbe a tenere `--terr-line` a 3:1 sul bianco `#C8D4D6` della gradazione `-notte`). Chiedo
   che quel documento registri la collocazione e che **M-IMG-2 (la deriva di 24 px) non si applichi alla lastra del capitolo
   del pilota**: una fotografia che deriva sotto un disegno fisso allineato al registro è un disallineamento in movimento.
   Costo: una voce di moto in meno, zero byte.
2. **A `imagery.md` — richiesta di coordinamento n. 2.** Sotto 48rem 21:9 su una lastra larga 350 px dà **167 px**: una
   fessura. Chiedo un ritaglio art-directed **3:2** sotto 48rem per la sola `variant="chapter"` — misurato al suo posto,
   350×233. Costo: un derivato in più per master.
3. **A `public-sections.md` — l'orientamento nella pagina.** §1.6 misura un problema vero: a 6 000 px non si sa dove si è.
   Questo capitolato **non** lo risolve e non ci mette una barra, perché la home ha già il dispositivo giusto e lo usa a
   metà: `register.css` 819-826 numera le sezioni con `.folio__ordinal`, e la home rende **6 blocchi `.folio` su 10 sezioni**
   (misurato a schermo: `01 L'ÉCOSYSTÈME` … `06 PROMOTEUR ET PARTENAIRES`; ne sono privi hero, pilota, antifrode e spazio
   riservato). La correzione è estendere quel folio alle dieci e dargli il totale — un numero di foglio dice *dove sei* e
   *quanto manca* meglio di un filetto di 2 px, ed è già il linguaggio del progetto. È una riga in quattro template e
   appartiene a chi possiede quelle sezioni. **Se quella specifica non lo fa, la home resta senza indicatore di posizione, e
   questo documento lo ha lasciato scoperto sapendolo.**
4. **Al documento di moto.** AMENDMENT 1 (§0) va scritto in `MOTION_SYSTEM.md` §4 nello stesso commit del foglio, con il
   test di §0. Un foglio che spedisce due oggetti indicizzati allo scroll prima che la clausola sia emendata è una deviazione
   non dichiarata, ed è esattamente ciò che questo round doveva smettere di fare.
