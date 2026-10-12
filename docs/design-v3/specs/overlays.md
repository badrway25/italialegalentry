# OVERLAYS V3 — «il vestibolo» — ROUND 2

Superficie: popup, modali, drawer, popover, tooltip, toast, palette comandi. Vincolanti:
`docs/design-v2/{DESIGN_SYSTEM_V2,MOTION_SYSTEM,ANTI_PATTERNS}.md`.

**Questo giro.** La revisione ha trovato la proposta non conforme e non implementabile. Ogni MUST-FIX
è chiuso (§0.2) o contestato con il numero che lo smentisce. Le quattro violazioni del sistema sono
rimosse; quello che resta fuori regola è dichiarato in testa come emendamento numerato (§0.1). Le
lacune sono colmate: il CSS delle dieci varianti è scritto per intero, il meccanismo di uscita è
nominato, il markup del drawer e dei toast è scritto in Django, il cancello di ruolo è espresso nel
vocabolario reale del prodotto. **Tutti i numeri di questo documento sono stati ricalcolati o
rimisurati in questo giro**; dove la revisione ha dato una cifra che non ho potuto riprodurre, la
contesto con la mia misura e con il metodo.

**Metodo di misura (round 2).** Chromium headless di Playwright
`HeadlessChrome/153.0.8010.12` lanciato da `.venv/Scripts/python.exe`, contro
`http://127.0.0.1:8771/fr/` (eroe mezzanotte) e `http://127.0.0.1:8771/fr/note-legali/` (pagina
minerale), viewport 390×844 · 768×1024 · 1024×800 · 1279×800 · 1440×900 e 390×844 / 1279×800 in
`dir="rtl"` su `/ar/`. Il foglio candidato è stato iniettato con `document.adoptedStyleSheets`
(`add_style_tag` è rifiutato da `style-src 'self'`, vedi §7.3) e le superfici sono state misurate
vive con `getComputedStyle`, `getBoundingClientRect`, `elementFromPoint` e campionamento di pixel
sulle schermate. **I rapporti di contrasto composti sono calcolati sulla luminanza relativa WCAG 2.x
senza arrotondare il composito**; dove il composito si arrotonda a interi la cifra cambia nella
seconda decimale (es. 5,32 contro 5,34), e lo dico dove capita. Le dimensioni gzip sono misurate con
`gzip -6`, che riproduce esattamente le cifre della revisione.

---

## 0.1 RICHIESTE DI EMENDAMENTO

Quattro. Ognuna nomina la clausola, chiede una cosa sola, dice perché e dice che cosa costa. Se una
viene respinta, la riga «se respinta» dice che cosa faccio invece: nessuna di esse è un ricatto.

### A1 — DESIGN_SYSTEM_V2 §1.3 regola 2 · il territorio guadagna un membro: **la soglia**

> «Il teal del territorio è grafica. `--terr-line` disegna isoipse, graticola, rotta, glifi; mai
> testo, mai interazione. Isoipse **solo** in modalità IMMERSIVE.»

**Chiedo** di aggiungere a quell'elenco **la soglia**: un filetto di 3 px, a gradiente, sul **bordo
d'ingresso** di un pannello di livello 5, in `--terr-line-lt` su carta e `--terr-line` su mezzanotte.
Non è un'isoipsa, quindi la restrizione IMMERSIVE non la riguarda; è una quinta figura del sistema
cartografico, come la tacca.

**Perché.** Il vestibolo ha bisogno di **una** firma e il sistema non ne ha una per l'overlay.
Senza la soglia il pannello è un rettangolo di carta con un'ombra, che è esattamente il verdetto
della revisione («corrective rather than spectacular»). La soglia è anche informativa, non
decorativa: **sta sul bordo da cui il pannello è entrato**, quindi in `dir="rtl"` migra da sola e
dice da dove viene la cosa che ti ha coperto la pagina.

**Costa.** Un sesto uso ammesso del teal del territorio, e il rischio che in sei mesi ogni scheda
abbia un filetto teal in testa. Guardia: la soglia è disegnata da **un solo selettore**
(`.ovl__panel::before`) e `tests/frontend/test_v3_overlay_tokens.py` conta le occorrenze di
`--ovl-threshold-line` nel CSS compilato (attese: 3 — la dichiarazione, l'override della palette,
l'uso).

**Se respinta.** Il filetto diventa `--hairline-strong` (3,59 : 1 su `--min-2`, misurato) e il
vestibolo perde il suo colore; la grammatica del bordo d'ingresso e il tracciato restano.

### A2 — DESIGN_SYSTEM_V2 §7 · la tabella delle modalità governa **la pagina**, non lo strato overlay

> DENSE — Vietato: «ombre, vetro, reveal». LEGAL — Vietato: «qualunque moto decorativo».

Il fascicolo è DENSE e le note legali sono LEGAL. Una conferma aperta da lì porta `--shadow-5`
(prescritto da §2 livello 5) e un'entrata di 320 ms (prescritta da MOTION_SYSTEM §2, famiglia
OVERLAY). Le due regole si contraddicono e nessuno l'ha scritto.

**Chiedo** che §7 sia letto così: la tabella governa il **contenuto della pagina**; lo strato
overlay è governato in ogni modalità da §2 livello 5 (`--min-2` / `--mid-2` + `--shadow-5` + scrim)
e dalla famiglia OVERLAY di MOTION_SYSTEM §2.

**Perché.** Un overlay non è un reveal: non appare perché sei arrivato con lo scroll, appare perché
l'hai chiesto. Toglierlo il moto su DENSE significa che su un fascicolo la conferma **compare** senza
dire da dove viene né che cosa copre — meno accessibile, non più sobrio (è lo stesso argomento con
cui §2 ha respinto «AVOID: motion effects»).

**Costa.** Su una pagina DENSE compare un'ombra e un moto di 320 ms — solo su richiesta della
persona, mai da sola. `grep box-shadow` continua a restituire quattro ruoli.

**Se respinta.** Su DENSE e LEGAL il pannello perde `--shadow-5` e si separa con il bordo e con lo
scrim (`--min-2` contro lo scrim adiacente: **6,13 : 1** misurato, §4.1), e l'entrata si riduce
allo stato finale immediato, come con reduced-motion.

### A3 — MOTION_SYSTEM §2 · la famiglia OVERLAY esce in **fast 180**, non in slow 320

> Famiglia OVERLAY — Durata: **slow**. Curva: out / in.

**Chiedo** che la riga diventi: entrata `slow` 320 ms `--ease-out`, **uscita `fast` 180 ms
`--ease-in`**. Nessuna durata nuova: 180 è uno dei quattro token.

**Perché.** L'uscita segue una decisione già presa. 320 ms per togliere di mezzo una cosa che la
persona ha appena chiuso è attesa, non orientamento; la stessa tabella dà già `instant/fast` alla
famiglia USCITA per lo stesso motivo. **Correggo anche me stesso**: §1.8 di questo documento
affermava che la famiglia OVERLAY vuole 320 in entrambe le direzioni e poi §5 specificava uscite a
180 — una deviazione non dichiarata che la revisione non ha visto e che dichiaro adesso.

**Costa.** La riga OVERLAY diventa asimmetrica, unica nella tabella. Il test che conta le durate non
cambia (180 è un token esistente).

**Se respinta.** Tutte le uscite di §5 passano a 320 `--ease-in`; l'unica conseguenza tecnica è che
il `close()` differito di §4.7 attende 320 ms invece di 180.

### A4 — DESIGN_SYSTEM_V2 §8.2 · il drawer è a schermo intero **solo sotto 48rem**

> «Sotto 1280: drawer a schermo intero su carta, voci a 52 px, CTA in fondo.»

**Chiedo**: schermo intero sotto `47.999rem`; da `48rem` a `79.999rem` un pannello di
`min(26rem, 78vw)` ancorato al bordo di lettura, con lo scrim **visibile** a fianco.

**Perché.** §1.6, misurato: a 390 px il drawer è largo 390 e copre il **100 %** dell'area dello
scrim; lo scrim viene dipinto a ogni apertura e non si vede mai. A 1024 px un drawer a schermo
intero nasconde una pagina che la persona sta ancora guardando, e lo scrim — il cui unico mestiere è
dire «il resto è sospeso» — non ha niente da velare. Misurato in questo giro: a 1024×800 il pannello
è 416 px e lo scrim ne occupa 608; a 1279×800 il pannello è 416 e lo scrim 863; in `dir="rtl"` a
1279×800 il pannello sta a `x = 863` e lo scrim a sinistra, senza una riga di CSS in più.

**Costa.** Due sagome da verificare invece di una (telefono / tablet-desktop). Sotto 48rem il
`::backdrop` del drawer diventa `transparent`: è il dipinto morto di §1.6, rimosso.

**Se respinta.** Il drawer resta a schermo intero fino a 1279 px, `::backdrop` diventa `transparent`
su tutto l'intervallo (perché non è mai visibile) e §1.6 resta un difetto accettato, non risolto.

---

## 0.2 RISPOSTA ALLA REVISIONE

### MUST-FIX

| # | Esito | Dove | Misura |
|---|---|---|---|
| 1 | **FATTO** · cifra **contestata** | §4.3 | La morsa UA è `max-inline-size / max-block-size: calc(100% - 2em - 6px)`. Sul progetto `font-size` calcolato del `<dialog>` = **17 px** (ereditato da `body`), quindi `calc(100% - 40px)`, non 38: misurato a 390×844, `dialog` = **[20, 326, 350 × 209]**, cioè **20 px di scrim per lato**. I 38 px della revisione corrispondono a un `font-size` di 16 px. **La sostanza resta la loro**: il difetto è reale ed è §1.5. Dopo `max-inline-size:none; max-block-size:none; inline-size:100%; block-size:100%` il rettangolo del `<dialog>` misura **[0, 0, 390 × 844]** e il pannello non sborda più. |
| 2 | **FATTO** diversamente · i due rimedi proposti **contestati** | §4.3, §4.5, §4.7 | Misurato: con un `<dialog>` modale aperto, un `[popover=manual]` mostrato **dopo** è `checkVisibility() === true` ma `document.elementFromPoint` al suo centro restituisce il `<dialog>`, e `button.focus()` lascia `document.activeElement` sul `<dialog>`. Rialzarlo (`hidePopover()` + `showPopover()`) non cambia nulla: un elemento del top layer resta inerte finché un dialogo modale blocca il documento. Il rimedio (b) della revisione produrrebbe quindi un toast **visibile e non cliccabile**, che è peggio di uno invisibile. Non prendo nemmeno il rimedio (a) — spostare la regione `aria-live` dentro l'overlay — perché una live region trasferita nel DOM smette di essere affidabile su NVDA e VoiceOver. Terza via, §4.7: **un toast non coesiste mai con un overlay aperto**; la coda è trattenuta e svuotata alla chiusura. La scala è cancellata e **rimpiazzata da due numeri misurati**: `--layer-pop: 30` (il massimo z-index dentro il contesto di impilamento dell'header è 29, `.nav-overlay`, che questo cambiamento elimina, e 20 per `.main-nav__panel` / `.lang-switcher__list`) e `--layer-toast: 50` (il massimo z-index dell'intera home renderizzata è **40**, `.skip-link`). `--layer-scrim` e `--layer-overlay` sono eliminati. |
| 3 | **FATTO** | §4.7 | Meccanismo (b), verificato vivo: `animate(el, …, { pseudoElement: '::backdrop' })` **passa** attraverso `static/js/dist/motion.js` del progetto — `document.getAnimations()` restituisce un'animazione con `effect.pseudoElement === '::backdrop'` e l'opacità del `::backdrop` è stata letta a 0,805 a metà corsa. Lo stesso vale per `'::before'` (soglia): letto `matrix(0.773642, 0, 0, 1, 0, 0)` a metà corsa. `close()` è chiamato dopo `await Promise.all(anims.map(a => a.finished))`; `Escape` è intercettato con `e.preventDefault()` sull'evento `cancel` (verificato: `defaultPrevented === true`, `dialog.open` resta `true`). Con reduced-motion il ramo `settle` chiama `close()` subito. |
| 4 | **FATTO**, senza CSS nuovo | §4.2, §4.3 | Il pannello della palette porta `class="ovl__panel on-inverse"`: la regola che già esiste in `static/css/v2/shell.css:483` (`.on-inverse :focus-visible`) dà `outline-color: var(--accent-dark)` e l'alone `rgba(127,209,216,.3)`. Misurato vivo sul pannello scuro: `outlineColor: rgb(127, 209, 216)`, `outline-width 2px`, `outline-offset 2px`. `--accent-dark` su `--ovl-panel-dark` (`--mid-2`) = **9,09 : 1**. |
| 5 | **FATTO** · sostituto proposto **contestato** | §4.1 | `--ovl-edge` non è più un derivato dell'accento. Ma `--hairline-dark-strong` **non** funziona: composto su `--mid-2` dà `rgb(74, 89, 97)`, e la palette si apre su una **pagina minerale velata**, non su un capitolo mezzanotte — contro quel fondo misura **1,87 : 1** a `.88` (e 1,75 a `.86`), non 3,17. I 3,17 : 1 della revisione valgono contro un fondo **mezzanotte** velato, che non è il fondo della palette. Sostituto: **`--ovl-edge: var(--on-dark-3)`** (`#8FA0A3`, token del capitolo mezzanotte, non un testo riservato). Misurato **sui pixel renderizzati** a 1440×900: bordo `rgb(143,160,163)` contro fondo `rgb(39,48,55)` = **4,94 : 1**; contro un fondo mezzanotte velato = **6,75 : 1** (calcolato); contro il pannello stesso = **5,85 : 1**. |
| 6 | **FATTO** per rimozione | §4.3, §8 | `backdrop-filter` sparisce dal documento. Nessun emendamento: il vetro era anche il segnale più da catalogo della proposta (§3 candidato 5 lo rifiuta e poi §4.3 lo rimetteva). Al suo posto la palette ha uno scrim **piatto e profondo** (`rgb(10 21 28 / .88)`): la pagina non è smerigliata, è **spenta**. Costa zero byte, zero GPU, e dice una cosa più forte. |
| 7 | **FATTO** | §4.1 | `--ovl-panel-dark: var(--mid-2)`. Tabella scura interamente ricalcolata (§4.1). |
| 8 | **FATTO** | §4.4 | La riga del promotore è nel **capo-lettera del drawer**, verbatim; i tre guardiani del link «Espace réservé» (`{% flag "reserved_area_public_link" %}`, `site.settings.reserved_area_enabled`, `not user.is_authenticated`) sono riportati. |
| 9 | **FATTO** | §4.2, §4.3, §4.4, §4.7 | È un `<dialog>`. La regola `inert` è riscritta (la dà lo UA, non noi). La soppressione del secondo scrim è un attributo, `data-ovl-covered`, verificato: `::backdrop` del drawer sotto passa a `rgba(0,0,0,0)` e torna a `radial-gradient(at 0% 50%, …)` quando l'attributo è tolto. La navigazione senza JS è riscritta in §4.3 (`html.no-js`) e verificata di concetto: un `<dialog>` senza `open` è `display:none` per regola UA, e una regola d'autore di specificità superiore lo rimette in flusso. |
| 10 | **FATTO** | §4.1 | `:root{ --dir: 1 }` · `[dir="rtl"]{ --dir: -1 }`. |
| 11 | **FATTO** | §4.6 | Il cancello è scritto su `apps/accounts/roles.py` (gruppi Django), non su `AccountType`, e dice perché il ruolo **per incarico** `AssignmentRole.OPERATOR` (`apps/cases/models.py:311`) non può governare una superficie di chrome globale. |
| 12 | **FATTO** | §4.0, §5 | `SPRING_SETTLE = { stiffness: 260, damping: 30 }` entra in `static/js/src/motion.js`, che è ora nell'elenco dei file toccati. `SPRING_FOLLOW` non serve a questa superficie e non si aggiunge. |
| 13 | **FATTO** | §7 | Ribasato su misure mie. |
| 14 | **FATTO** | §4.1, §4.3, §5, §8 | La soglia passa da 1 px a **3 px**, diventa un gradiente che sfuma alle due estremità, guadagna una cornice da 1 px che la stacca dallo scrim, e **si disegna** all'apertura. Lo scrim smette di essere una vignetta centrata e diventa **direzionale**: la luce è la porta. Maniglia e raggio 16 px eliminati. |

### Violazioni dei vincoli

| # | Esito |
|---|---|
| 1 · `backdrop-filter` sullo scrim della palette | **Rimossa.** Nessun `backdrop-filter` in questo documento. §7 non lo rivendica più. |
| 2 · `--ovl-edge` = `--accent-dark` scritto a mano | **Rimossa.** `--ovl-edge: var(--on-dark-3)`. Nessun colore letterale nel foglio: ogni valore è un token o un `rgb()` dell'inchiostro dello scrim, dichiarato in §4.1. |
| 3 · `--ovl-panel-dark` = `--mid-4` | **Rimossa.** `var(--mid-2)`, DS §2 livello 5. |
| 4 · anello di focus 2,90 : 1 sul pannello scuro | **Rimossa.** `on-inverse` → `--accent-dark`, 9,09 : 1 misurato. |
| 5 · navigazione mobile senza JS persa | **Rimossa.** §4.3 «SENZA JAVASCRIPT» e §4.4. |

### Segnali di «cheap / generico»

| # | Esito |
|---|---|
| 1 · maniglia 40×4 + raggio 16 px = vaul/shadcn | **Rimossi entrambi.** Niente maniglia: la zona di trascinamento è **la testa** del pannello (44 px pieni, `touch-action:none`), e i controlli dentro la testa ne escono da soli. `--radius-vestibule` è cancellato: i raggi tornano a 0, come DS §2 prescrive per i fogli — **una deviazione dichiarata in meno**. La sagoma diventa un foglio di carta a spigolo vivo sotto un filo di luce, che nel 2026 è più raro di un'altra scheda arrotondata. |
| 2 · matematica della pila alla Sonner | **Rimossa.** Nessuna scala, nessun arretramento. Tre toast al massimo, lista verticale, `gap: var(--s-2)`, tutti a piena opacità; quando uno se ne va i superstiti si riassestano con `SPRING_SETTLE`, che è **esattamente** l'uso che MOTION_SYSTEM §1 prescrive per quella molla («riga inserita/rimossa»). La scala serviva a risparmiare spazio: 3 × 70 px + 2 × 8 px = 226 px, e ne abbiamo. |
| 3 · vignetta impercettibile | **Contestato nel numero, accolto nella sostanza.** Il delta di 16 punti alfa (.62 → .78) **non** è sotto la soglia percettiva: composto su `--min-0` dà `rgb(99,105,109)` L\* = 44,12 e `rgb(61,70,75)` L\* = 29,08, cioè **ΔL\* = 15,03**, quindici volte la JND (≈ 1 L\*). Il difetto vero era un altro e lo accolgo: una vignetta **centrata** non dice niente, e su una pagina mezzanotte è davvero invisibile — misurato, ΔL\* = **0,84** sopra `--mid-1`. Lo scrim diventa direzionale e ancorato alla porta (§4.1), con i valori misurati sui pixel renderizzati in §4.1. |
| 4 · la soglia da 1 px | **Rimosso.** 3 px, gradiente, incorniciata. Misurata riga per riga a 1440×900 sulla pagina minerale: scrim `rgb(96,101,98)` / 1 px `--hairline` `rgb(211,210,204)` / 3 px `--terr-line-lt` `rgb(15,106,114)` / carta `rgb(251,250,248)`. Contrasti: cornice contro scrim **3,92 : 1**, soglia contro cornice **4,17 : 1**, soglia contro carta **6,05 : 1**. La cornice esiste perché senza di essa la soglia e lo scrim adiacente hanno la stessa chiarezza (**1,06 : 1** misurato) e il filetto sparisce nel velo. |
| 5 · `color:#fff` | **Rimosso.** L'intera regola `.ovl__foot .btn--primary` è cancellata: `static/css/v3/buttons.css` già dà al primario `--accent` con etichetta `--min-0` (5,69 : 1), e un secondo posto dove scrivere il primario è il modo di avere due primari. |
| 6 · correttivo, non spettacolare | **Risposto, §4.1 e §5.** Lo spettacolo è in tre cose misurabili e in nessuna nuova: (a) lo scrim è **una luce con una posizione** — `--ovl-origin` è la porta, e la stanza si scurisce allontanandosene (ΔL\* misurato **13,4** a fianco del drawer, **13,8** sopra lo sheet, **20,8** dal pannello all'angolo per la modale centrata, ogni punto letto su un fondo minerale verificato); (b) la soglia **si disegna** mentre il pannello arriva, stessa durata e stessa curva, così la porta si apre invece di essere disegnata; (c) la palette **spegne** la pagina invece di smerigliarla. Quello che il vestibolo non farà mai è stupire: le regole di §4 («niente lavoro dentro un overlay», «mai il fuoco su Fermer», «due azioni al massimo») restano invisibili in una schermata, e io continuo a difenderle come la parte più preziosa del documento. |

### Lacune

Tutte chiuse: (1) §4.7 · (2) §4.0 e §5 · (3) §4.7, con la prova · (4) §4.1 · (5) §4.6 · (6) §4.2 e
§4.7 · (7) §4.5, con il template · (8) §4.3 · (9) §7 · (10) §7.3.

---

## 1. VERDETTO SULLO STATO ATTUALE

Rimisurato il 24 settembre 2026, secondo giro, con il metodo in testa.

- **1.1 Metà delle lingue non è cliccabile.** Riprodotto a 1440×900: i quattro link misurano
  `166 × 32` a `y = 47 / 79 / 111 / 143`; `document.elementFromPoint` al centro di «Italiano»
  restituisce `.main-nav__list`, al centro di «Français» `.container site-header__inner`. Solo
  «English» e «العربية» sono raggiungibili. Con `details[data-dropdown][open]{ position:relative;
  z-index:30 }` tutti e quattro tornano raggiungibili (`reachable: true` su quattro su quattro).
  Su un sito FR/IT/EN/AR è la porta della versione italiana che non si apre.
- **1.2 L'unica modale del sistema non è usata da nessuna parte.** `grep -rn "components/dialog.html"
  templates/` → 0 occorrenze; `initDialogs()` (`static/js/main.js`, 1 282 byte) governa un
  componente che non esiste in produzione. È un difetto di **contratto**, da chiudere prima che
  qualcuno lo usi.
- **1.3 Elevazione zero, e colore della tela invece che del foglio.** `components.css:2491` dichiara
  `box-shadow: var(--shadow-lg)`, ma `_legacy-tokens.css:135` definisce `--shadow-lg: none`.
  Misurato sull'elemento vivo: `box-shadow: "none"`, `--shadow-lg` risolve a `none`, fondo
  `rgb(244, 243, 240)` = `--min-0` (livello 0), contro `--min-2` + `--shadow-5` prescritti dal
  livello 5.
- **1.4 Il navy ufficiale fa da colore d'interazione.** Pulsante primario
  `background-color: rgb(15,37,71)` = `--brand-navy`; filetto superiore 3 px dello stesso.
  DS §1.3 regola 4. (Già corretto per `.btn--primary` da `static/css/v3/buttons.css`; il filetto
  della modale è di questa superficie e muore con §4.3.)
- **1.5 Il telefono riceve una modale da desktop rimpicciolita.** A 390×844 il `.dialog` legacy
  misura **350 × 209 a `x = 20`, `y = 326`**: la morsa UA `dialog:modal` è
  `calc(100% - 2em - 6px)`, e con `font-size: 17px` ereditato dal `body` fa `calc(100% - 40px)`,
  cioè **20 px di scrim per lato** e altrettanti in verticale, qualunque sia il contenuto. Raggio
  2 px, ombra `none`. Nessun bottom sheet esiste:
  `grep -rn "bottom-sheet\|popover\|toast\|tooltip\|inert" static/css/ static/js/` restituisce **una
  riga sola**, ed è un commento.
- **1.6 Lo scrim del drawer è codice morto.** A 390 px il drawer è largo 390 (= tutto il viewport):
  copre il **100 %** dell'area dello scrim, che viene dipinto a ogni apertura e non si vede mai.
- **1.7 Il drawer non ha direzione, gerarchia né chiusura.** `box-shadow: none`, `transform: none` da
  aperto, transizione 240 ms — una discesa di 8 px con dissolvenza; in `dir="rtl"` la trasformazione
  è identica, cioè il moto non ha lato di lettura perché non ha lato. Gli ultimi ~370 px sono carta
  vuota, senza la CTA in fondo prescritta dal DS §8.2.
- **1.8 Tre famiglie di overlay, tre moti, due assenti.** Mega-menu `menu-in` 240 ms; modale
  `dialog-in` 240 ms **senza uscita** (`close()` è istantaneo); `<details>` con
  `animation-name: none` e `transition-duration: 0s`. Il `::backdrop` ha `animation-name: none`: lo
  scrim **salta** da 0 a 0,55 in un frame — misurato `rgba(14, 22, 29, 0.55)`. MOTION_SYSTEM §2
  assegna alla famiglia OVERLAY `slow` 320 ms con `--ease-out` in entrata e `--ease-in` in uscita;
  nessuno dei tre la rispetta. *(Su quale durata debba avere l'uscita, vedi l'emendamento A3: questo
  documento chiede 180.)*
- **1.9 Il fuoco atterra su «Fermer».** Misurato dopo `showModal()`:
  `activeElement = button.dialog__close` — la prima cosa annunciata è «Chiudi, pulsante», non la
  decisione. Il partial non espone `aria-describedby`.
- **1.10 Nessun blocco d'autore, nessun `overscroll-behavior`, nessun `inert`.** Con la modale aperta
  `body` ha `overflow: visible`. **E lo UA non salva: misurato, con un `<dialog>` modale aperto
  `window.scrollBy(0, 400)` sposta comunque il documento.** Il drawer mobile mette `overflow:hidden`
  sul `body` **senza** conservare lo `scrollTop`; `overscroll-behavior` non compare in nessun foglio.
- **1.11 Il contrasto forzato peggiora le cose.** In `forced-colors: active` il `::backdrop` del
  `.dialog` legacy misura `rgba(255,255,255,0.55)` — un velo **bianco semitrasparente** — e conserva
  `backdrop-filter: blur(2px)`. Nessuna regola `@media (forced-colors)` esiste per gli overlay.
- **1.12 Bersagli a 32 px.** `.lang-switcher__link` misura `166 × 32`: sopra il minimo AA (24) ma
  sotto i 44 che il resto del sistema usa — e su telefono quel menu vive dentro il drawer.

---

## 2. UI-UX-PRO-MAX — interrogazioni e verdetti

Invariato rispetto al round 1, con una correzione dichiarata alla riga 3.

| # | Query (`--domain`) | Cosa è tornato (condensato) | Esito |
|---|---|---|---|
| 1 | `modal dialog overlay scrim elevation focus trap` (ux) | 3 risultati **tutti sul fuoco**: anello visibile anche nelle modali; perimetro 2 px e 3:1 di contrasto di stato (AAA, da non spacciare per AA); «Focus Not Obscured». Nulla su scrim o elevazione. | **ACCETTATO in parte.** Prendo l'anello 2 px + offset 2 px (già nostro: misurato `rgb(29,138,147) solid 2px`, alone 5 px al 30 %) e faccio di «Focus Not Obscured» una regola dura sul toast (§6g). **Respinta la lacuna**: §4.1 si fonda su misure mie e sul DS §2. |
| 2 | `bottom sheet drawer mobile swipe to dismiss` (ux) | Niente di pertinente: tastiere mobili, mobile-first, pull-to-refresh → `overscroll-behavior: contain`. | **RESPINTO come risposta, ACCETTATO il frammento**: `overscroll-behavior: contain` obbligatorio su ogni pannello scorrevole (oggi assente ovunque). |
| 3 | `toast notification snackbar timing dismiss` (ux) | «Transient messages for non-critical info; auto-dismiss 3-5 s; mai toast persistenti». | **ACCETTATO il principio, RESPINTI i 3-5 s.** Il pubblico legge in FR/IT/EN/AR, spesso in lingua non materna. Adotto **6 s**, pausa su hover/focus/`document.hidden`, nessuna scadenza con reduced-motion o oltre 120 caratteri (WCAG 2.2.1). «Non-critical» integralmente: `error`/`warning` non diventano mai toast. |
| 4 | `command palette keyboard shortcut power user` (product) | Fuori bersaglio. Utile solo il profilo «Developer Tool»: dark mode + minimalismo svizzero. | **RESPINTO.** Tengo solo la conferma che la palette è l'unica superficie legittimamente **scura** in una pagina chiara — che DS §2 livello 5 già ammette (colonna «scuro»): **una palette scura non è un secondo capitolo mezzanotte** ai sensi di DS §1.3 regola 5, è il livello 5 nella sua variante scura. |
| 5 | `elevation shadow layering depth surface` (style) | `dimensional-layering` (4 ombre, `backdrop-filter`, parallasse, rischio a11y alto); `fluent-2`; `bauhaus`. | **ACCETTATO `fluent-2`; RESPINTI gli altri due.** Respinta la parallasse e l'ombra dura offset (ANTI_PATTERNS §3). Respinti i 4 livelli generici: ne abbiamo quattro **di ruolo**, e restano quattro. |
| 6 | `government accessible institutional interface` (`--design-system`) | «AVOID: Ornate design + Low contrast + Motion effects»; font Atkinson Hyperlegible; checklist. | **RESPINTO il verdetto, ACCETTATA la checklist.** «Avoid motion effects» è il registro bocciato dal committente ed è sbagliato nel merito: un overlay che appare senza moto non dice da dove viene né che cosa copre. Respinto il font: le tre voci sono fissate. |
| 7 | `dropdown menu popover animation entrance exit` (gsap) | «Stagger List»: 250-350 ms, `power1.out`, stagger 0.02-0.04 s; skeleton shimmer in loop. | **ACCETTATO adattato.** Lo stagger delle voci del drawer prende **40 ms** e si ferma all'ottava. `power1.out` è tradotto nella nostra `--ease-out`. Respinto lo shimmer. |
| 8 | `overlay scrim color contrast dark surface` (color) | Tre palette: navy `#0F172A`, slate, ring bianco. | **RESPINTO.** È la palette zinc/slate segnalata da ANTI_PATTERNS §1. Lo scrim resta costruito sul nostro inchiostro `rgb(10 21 28)`. |

---

## 3. 21ST.DEV — candidati confrontati

Nessun pacchetto installato: React, Radix, Base UI, vaul e Tailwind sono fuori dai vincoli
(Django + CSP `script-src 'self'`). Si estrae il **pattern**. Due voci cambiano in questo giro e lo
dico: dal candidato 1 **non** prendo più la sagoma del foglio, e dal candidato 8 **non** prendo più
niente.

| # | Candidato · URL | Cosa prendo | Cosa rifiuto e perché |
|---|---|---|---|
| 1 | **Animated Dialog** (rmahammad) · `21st.dev/@rmahammad/components/animated-dialog` | (a) `mobileVariant="sheet"`: stessa modale, bottom sheet sotto 640 px — risposta diretta a §1.5; (b) Head/Body/Foot con il **solo Body scorrevole**, azioni sempre visibili sopra la tastiera; (c) `forced-colors:border-[ButtonText]` sulla chiusura. | Radix+Framer+Tailwind. `rounded-2xl` su tutto. `shadow-[0_24px_70px…]` inventa un quinto ruolo d'ombra. La «top-edge sheen» a gradiente è decorazione. **Nuovo in questo giro:** rifiuto anche la molla in entrata — le entrate stanno sui quattro token, e una molla in apertura è un rimbalzo travestito. |
| 2 | **Drawer (Base UI)** · `21st.dev/@base-ui/components/drawer-base` | (a) Il gesto come **variabile CSS** (`--drawer-swipe-movement-y`, `--drawer-swipe-progress`): il trascinamento non è un'animazione, è una trasformazione legata al dito — riprodotto con `--ovl-drag` e `--ovl-progress`; (b) lo **scrim che si schiarisce mentre trascini**: causalità pura; (c) `overscroll-contain` + `user-select:none` durante il gesto. | Durate 450 ms e curva `cubic-bezier(0.32,0.72,0,1)`: fuori dai nostri token. Lo stacking dei drawer annidati. `IndentBackground` (la pagina che si rimpicciolisce dietro): fuori registro per un fascicolo amministrativo. |
| 3 | **Reshaped Modal** · `21st.dev/@reshaped/components/reshaped-modal` | Una primitiva con cinque ancoraggi e l'animazione che segue la posizione; blocco dello scorrimento incluso; `Modal.Title` come composizione **obbligatoria**. | «Transparent overlay mode» per i pannelli laterali: senza scrim il pannello non dice che il resto è sospeso. |
| 4 | **HeroUI Drawer** · `21st.dev/@hero_ui/components/heroui-drawer` | La variante **non-dismissable** per le conferme irreversibili → `data-ovl-dismiss="none"`. | Le «backdrop variants» a scelta dell'implementatore: lo scrim è **uno** e non è configurabile. |
| 5 | **Command Palette** (rafa-porto) · `21st.dev/@rafa-porto/components/command-palette` | La struttura: input alto, risultati **raggruppati per tipo**, scorciatoia a destra di ogni riga, navigazione da tastiera pura. | L'estetica Raycast (glow, bordi luminosi, vetro): ANTI_PATTERNS §1 la marca «catalogo». **In questo giro cade anche l'ultimo residuo**: niente `backdrop-filter` da nessuna parte. |
| 6 | **Command Menu with Global Search** · `21st.dev/@ephraimduncan/components/command-menu-04` | I filtri di tipo e la sezione «recenti» → «ultimi fascicoli toccati», presi dal DOM già renderizzato. | La ricerca globale sul prodotto: confini pubblico/privato e permessi di ruolo sono governati lato server. |
| 7 | **Toast** (cnippet-dev, Base UI) · `21st.dev/@cnippet-dev/components/toast` | Pila con auto-dismiss, azione singola, glifi di stato. | Le sei posizioni configurabili: da noi è una per viewport. |
| 8 | **Stack** (diceui) · `21st.dev/@diceui/components/stack` | **Niente.** Nel round 1 prendevo la matematica alla Sonner (scala 1 → .965 → .93, arretramento 8/16 px). La revisione ha ragione: adottata verbatim, legge come la libreria che tutti riconoscono. La pila diventa una lista. | Tutto. La scala serve a risparmiare spazio; tre toast da 70 px stanno in 226 px e lo spazio ce l'abbiamo. |
| 9-10 | **Morphing Dialog** (ibelick) · **Dotted Dialog** (serafimcloud) | Niente da entrambi. Li cito perché sono le due tentazioni giuste da nominare. | La morph richiede `layoutId` di Framer e MOTION_SYSTEM §2 vieta di animare `height`/`width`; inoltre su un fascicolo dice «questa riga *è diventata* la modale», che è falso. Il pattern a pois + blur è decorazione pura. |

---

## 4. LA PROPOSTA — «il vestibolo»

Un vestibolo si attraversa: è breve, è illuminato, e non ci si lavora dentro. **Una primitiva CSS,
cinque ancoraggi, una grammatica: la soglia** — un filetto `--terr-line` di 3 px sul bordo da cui
l'overlay entra, che si disegna mentre il pannello arriva. E una luce che ha una posizione: lo scrim
è più chiaro **vicino alla porta** e si spegne allontanandosene.

**Regola di sostanza.** Nessun overlay contiene un modulo di più di tre campi, una tabella, un
caricamento di documento o un'azione governata dal Rule Engine: quelle stanno in una pagina. Un
overlay porta una **decisione**, una **scelta breve**, una **definizione**, una **notizia effimera**
o un **salto**; due azioni al massimo.

### 4.0 File nuovi e partial toccati

**Nuovi**
- `static/css/v3/overlays.css` — importato in `static/css/main.css` **dopo** `v3/buttons.css`
  (quindi dopo `v2/shell.css`: l'ordine conta, §4.3 nota 3) e aggiunto ai `<link rel="preload">` di
  `templates/base.html`.
- `static/js/src/overlays.js` — impacchettato da esbuild in `static/js/dist/overlays.js`, riusa il
  chunk Motion già caricato.
- `templates/components/overlay.html` — rimpiazza `components/dialog.html`.
- `templates/components/toasts.html` — sostituisce il blocco `{% if messages %}` di
  `templates/base.html` 57-60.
- `templates/components/command_palette.html` — incluso da `templates/portal/base_portal.html`.

**Modificati**
- `templates/partials/header.html` — il drawer diventa un `<dialog class="ovl" data-ovl="drawer">`.
- `templates/base.html` — il blocco messaggi, il `<link>`/preload del foglio, il `<script>` del
  bundle.
- `templates/components/language_switcher.html`, `templates/components/account_menu.html` — la lista
  prende `class="ovl-pop__list"`.
- **`static/js/src/motion.js`** — aggiunge `SPRING_SETTLE` (MUST-FIX 12):
  ```js
  /** MOTION_SYSTEM §1: due molle, nessuna con damping sotto 25. */
  export const SPRING_SETTLE = { stiffness: 260, damping: 30 };
  ```
- **`apps/accounts/roles.py`** — aggiunge la costante `COMMAND_PALETTE_ROLES` (§4.6). Nessun
  permesso nuovo, nessuna migrazione.
- **`apps/core/templatetags/ile_core.py`** — aggiunge il tag `can_command_palette` (§4.6).

**Rimossi da `static/css/components.css`**: i tredici blocchi `.dialog` / `.nav-overlay` /
`.nav-drawer` (**2 659 byte grezzi**, contati). **Rimossi da `static/js/main.js`**: `initDialogs`
(1 282 B), `initNavigation` (5 013 B), `initDropdowns` (1 491 B) = **7 786 byte grezzi** che
migrano in `overlays.js`.

**Nessuna vista, nessun modello, nessuna migrazione, nessun contratto dati.**

### 4.1 Token — solo aggiunte, con rapporti calcolati e misurati

```css
:root{
  /* Direzione di lettura, moltiplicata nel gesto e nel moto (MOTION_SYSTEM §5). */
  --dir: 1;

  /* LO SCRIM. Un inchiostro, due alfa, un'origine: la luce è la porta.
     L'origine è dichiarata per ancoraggio (§4.3) e il gradiente è scritto NELLA regola,
     non in un token: un var() dentro un token si risolve dove il token è DICHIARATO,
     quindi un --ovl-origin su un discendente non arriverebbe mai. Misurato, §4.3 nota 1. */
  --ovl-scrim-near: rgb(10 21 28 / .55);
  --ovl-scrim-far:  rgb(10 21 28 / .86);
  --ovl-scrim-deep: rgb(10 21 28 / .88);   /* solo la palette: la pagina è spenta, non smerigliata */

  /* LE DUE SUPERFICI — DS §2 livello 5, chiaro e scuro. */
  --ovl-panel: var(--min-2);
  --ovl-panel-dark: var(--mid-2);
  --ovl-edge: var(--on-dark-3);            /* il bordo del pannello scuro; vedi la tabella */

  /* LA SOGLIA — emendamento A1. Su carta il teal chiaro, sulla palette il teal scuro. */
  --ovl-threshold-line: var(--terr-line-lt);

  /* Due z-index veri, misurati, e nessuna scala inventata (MUST-FIX 2). */
  --layer-pop: 30;    /* dentro il contesto di impilamento dell'header: massimi misurati 20 e 29 */
  --layer-toast: 50;  /* massimo z-index dell'intera home renderizzata: 40 (.skip-link) */

  /* Scritte dal gesto, lette dal transform e dall'opacità dello scrim. */
  --ovl-drag: 0px;
  --ovl-progress: 0;
}
[dir="rtl"]{ --dir: -1; }
```

Non esistono `--layer-scrim` e `--layer-overlay`: per un `<dialog>` modale **il top layer non è uno
z-index**, e un token che finge il contrario è una trappola. Non esiste `--radius-vestibule`: i
raggi restano quelli di DS §2.

#### Rapporti — carta (livello 5 chiaro)

Da fissare in `tests/frontend/test_v3_overlay_tokens.py`. «Calcolato» = luminanza relativa WCAG 2.x
sul composito non arrotondato; «misurato» = campionato sui pixel di una schermata Chromium con il
fondo sottostante verificato uguale a `--min-0`.

| Confine | Composito | Rapporto |
|---|---|---:|
| `--ovl-panel` `#FBFAF8` contro lo scrim che **tocca** (modale centrata, 1440×900) | vs `rgb(92,99,102)` — *misurato* | **5,87 : 1** ✔ 1.4.11 |
| idem, sheet a 1440×900 · drawer a 1440×900 | vs `rgb(89,96,100)` · `rgb(97,104,106)` — *misurati* | **6,13** · **5,45** ✔ |
| `--ovl-panel` contro lo scrim al minimo assoluto del token (`.55` su `--min-0`) | `#FBFAF8` vs `rgb(115,121,123)` — *calcolato* | **4,24 : 1** ✔ |
| `--ovl-panel` contro lo scrim al massimo (`.86` su `--min-0` / `--mid-1`) | vs `rgb(43,52,58)` / `rgb(11,22,29)` | 12,17 / 17,58 |
| `--hairline` (cornice della soglia) contro lo scrim adiacente | `rgb(211,210,204)` vs `rgb(96,101,98)` — *misurato* | 3,92 : 1 |
| `--ovl-threshold-line` contro la cornice · contro la carta | `rgb(15,106,114)` vs `rgb(211,210,204)` · `rgb(251,250,248)` — *misurati* | 4,17 · **6,05 : 1** |
| `--ink` / `--ink-2` / `--ink-3` / `--accent` su `--ovl-panel` | | 15,56 / 6,87 / 5,88 / **6,05** |
| `--err-700` (riga d'errore) · `--ok-700` (barra toast) su `--ovl-panel` | | 6,27 · 5,10 |
| `--ink-2` (barra toast «info») su `--ovl-panel` | | 6,87 |
| `--accent-ring` (anello di focus) su `--ovl-panel` | | 3,94 : 1 ✔ 1.4.11 |
| etichetta `--min-0` su riempimento `--accent` (azione primaria) | | 5,69 : 1 |

Il bordo `--hairline` del pannello chiaro misura 1,45 : 1 contro la carta: **non porta il confine**,
è ritmo. Il confine lo porta il riempimento contro lo scrim, che è la riga 1 e sta sopra 3 : 1
ovunque il token possa arrivare.

**L'anello di focus e il bordo del pannello.** `--accent-ring` contro lo scrim adiacente misura
1,08 : 1: un anello che sborda dal pannello sparirebbe. Non succede, perché `outline-offset` è 2 px
e ogni controllo sta a `var(--s-4)` = 16 px dal bordo interno (§4.3). È una condizione, non una
speranza: nessun controllo può essere messo a meno di 4 px dal bordo del pannello.

#### Rapporti — mezzanotte (livello 5 scuro, solo la palette)

Il pannello scuro si apre su una **pagina minerale velata**: è lì che va misurato, ed è il punto in
cui la sostituzione proposta dalla revisione non regge (MUST-FIX 5).

| Confine | Composito | Rapporto |
|---|---|---:|
| **riempimento** `--ovl-panel-dark` `#14242E` contro il fondo velato a `.88` | `rgb(20,36,46)` vs `rgb(39,48,55)` — *misurato* | 1,18 : 1 — **non porta il confine** |
| **bordo** `--ovl-edge` = `--on-dark-3` `#8FA0A3` contro lo stesso fondo | `rgb(143,160,163)` vs `rgb(39,48,55)` — *misurato* | **4,94 : 1** ✔ 1.4.11 |
| idem contro un fondo **mezzanotte** velato a `.88` | vs `rgb(10,22,29)` — *calcolato* | 6,75 : 1 ✔ |
| `--ovl-edge` contro il pannello (visibilità da dentro) | | 5,85 : 1 |
| *(respinto)* `--hairline-dark-strong` composto su `--mid-2` | `rgb(74,89,97)` vs `rgb(38,48,53)` | **1,87 : 1** ✘ |
| *(respinto)* `--hairline-strong` `#7A868B` | vs `rgb(38,48,53)` · vs `rgb(115,121,123)` | 3,62 ✔ · **1,18** ✘ |
| soglia `--terr-line` `#3FA6AF` su `--ovl-panel-dark` | *misurato* `rgb(63,166,175)` su `rgb(20,36,46)` | 5,51 : 1 |
| `--on-dark` / `--on-dark-2` / `--on-dark-3` su `--ovl-panel-dark` | | 14,08 / 8,79 / 5,85 |
| `--accent-dark` (anello di focus, via `on-inverse`) su `--ovl-panel-dark` | *misurato* `rgb(127,209,216)` | **9,09 : 1** ✔ |

`--on-dark-3` è un token del capitolo mezzanotte (DS §1.1). Il DS non prescrive un token di bordo
per il livello 5 scuro e non riserva `--on-dark-3` al testo; non è quindi una deviazione, ma lo
scrivo qui perché la scelta non sia archeologia fra sei mesi: **è l'unico token del capitolo giusto
che supera 3 : 1 su entrambi i fondi possibili.**

#### Lo scrim, misurato

Metodo: due schermate della stessa pagina minerale (`/fr/note-legali/`, 1440×900), una senza e una
con l'overlay; per ogni punto si verifica che il pixel **senza** overlay sia esattamente
`#F4F3F0` = `--min-0`, e solo allora si legge il pixel **con** overlay e si risolve l'alfa.

| Ancoraggio | Vicino alla porta | A metà | Lontano | ΔL\* visibile |
|---|---|---|---|---:|
| sheet (gradiente lineare verso l'alto) | α 0,662 · `rgb(89,96,100)` · L\* 40,26 | α 0,722 · L\* 34,74 | α 0,808 · `rgb(55,64,68)` · L\* 26,44 | **13,8** |
| drawer (radiale, origine sul bordo d'ingresso) | α 0,629 · `rgb(97,104,106)` · L\* 43,48 | α 0,692 · L\* 37,38 | α 0,769 · `rgb(64,72,77)` · L\* 30,06 | **13,4** |
| dialog centrata (radiale, origine sul pannello) | α 0,650 · `rgb(92,99,102)` · L\* 41,47 | α 0,698 · L\* 36,93 | angolo `rgb(42,51,57)` · L\* 20,66 (fondo `--min-1`) | **20,8** |

Il token va da `.55` a `.86`, cioè da L\* 50,40 a L\* 21,11 su `--min-0`: **ΔL\* 29,29** di
escursione teorica, di cui la finestra sopra è la parte che si vede davvero (il resto è sotto il
pannello, che è esattamente dove la luce deve stare). Per confronto, la vignetta del round 1 aveva
ΔL\* 15,03 — **non** invisibile, contrariamente alla revisione, ma centrata sul punto che il
pannello copre, quindi sprecata.

**Sopra un capitolo mezzanotte il gradiente non esiste**: `.55` e `.86` su `--mid-1` danno L\* 7,38
e 6,54, **ΔL\* = 0,84**, sotto la soglia percettiva. Non è un difetto da correggere, è fisica:
velare del nero con del nero non produce un gradiente. Lo dico qui perché nessuno lo cerchi con una
lente sull'eroe e pensi che il CSS sia rotto.

### 4.2 Anatomia — una primitiva, cinque ancoraggi

```html
<dialog class="ovl" id="confirm-remove" data-ovl="dialog" data-ovl-size="md"
        aria-labelledby="confirm-remove-t" aria-describedby="confirm-remove-d">
  <div class="ovl__panel" tabindex="-1" autofocus>
    <header class="ovl__head">
      <p class="ovl__eyebrow">Dossier E46E03B461</p>          <!-- mono, facoltativo -->
      <h2 class="ovl__title" id="confirm-remove-t">Retirer ce document du dossier</h2>
      <button class="ovl__close" type="button" data-ovl-close
              aria-label="{% translate 'Fermer' %}">{% svg_icon "close" "icon" %}</button>
    </header>
    <div class="ovl__body" id="confirm-remove-d">…</div>       <!-- UNICA zona scorrevole -->
    <footer class="ovl__foot">…max due azioni…</footer>
  </div>
</dialog>
```

`data-ovl` = `dialog` (centrata) · `sheet` (dal basso) · `drawer` (dal bordo di lettura) ·
`palette` (a 12 vh, scura) · `full` (lettura di un testo prescritto lungo). Sotto `47.999rem`
**ogni** `dialog` è promossa a `sheet` dal CSS: nessun attributo da cambiare nei template.
`data-ovl-size` = `sm` 26rem / `md` 34rem / `lg` 46rem, ignorata da `sheet`, `drawer`, `palette`,
`full`, che hanno la loro misura.

**`autofocus` sul pannello, e non è un dettaglio.** Lo HTML prescrive che `showModal()` dia il fuoco
all'elemento con `autofocus`, e solo in sua assenza al primo elemento focalizzabile. Mettendolo sul
pannello, **§1.9 è risolto dal markup, non dal JavaScript**: verificato vivo,
`document.activeElement.className === "ovl__panel"` subito dopo `showModal()`, con e senza
`overlays.js`. Il pannello ha `tabindex="-1"` (raggiungibile a programma, mai con Tab) e §4.3 gli
toglie l'anello: è un contenitore d'ingresso, non un controllo, esattamente come
`<main id="main-content" tabindex="-1">` che il progetto già usa per lo skip link.

Il pannello della **palette** porta in più `class="ovl__panel on-inverse"`: `on-inverse` non è
decorazione, è il commutatore che `static/css/v2/shell.css:483` usa per l'anello di focus scuro
(MUST-FIX 4).

Il `<dialog>` del **drawer** vive dentro `.site-header__inner`, dove sta oggi `.nav-drawer`: serve
alla degradazione senza JS (§4.3). Verificato che la posizione nel DOM non lo danneggia: con
l'header `is-scrolled` (che ha `backdrop-filter: blur(14px) saturate(1.4)`, `position: sticky`,
`z-index: 20`), un `<dialog>` modale figlio misura comunque **[0, 0, 1440 × 900]**, il suo
`::backdrop` ha `backdrop-filter: none` — il vetro dell'antenato non cola nel top layer — e
`elementFromPoint` sul pannello restituisce il pannello.

### 4.3 CSS — `static/css/v3/overlays.css`, per intero

Tre note prima del codice, tutte verificate:

1. **Un `var()` dentro un token si risolve dove il token è dichiarato.** Nel round 1 lo scrim e la
   soglia erano composti in `:root` e parametrizzati con `--ovl-origin` / `--ovl-threshold-line` su
   un discendente: misurato, **non funzionava** — la soglia della palette restava
   `rgb(15,106,114)` invece di `rgb(63,166,175)`, e il gradiente del drawer restava orizzontale.
   I due gradienti sono quindi scritti **nella regola** che li usa, dove i `var()` si risolvono
   sull'elemento giusto. Riverificato dopo: `radial-gradient(at 0% 50%, …)` sul drawer,
   `linear-gradient(to top, …)` sullo sheet, soglia `rgb(63,166,175)` sulla palette, gradiente
   verticale 3 × 900 px sul bordo del drawer.
2. **`::backdrop` eredita le proprietà personalizzate dal suo elemento d'origine.** Verificato:
   con `--ovl-progress: 0.4` sul `<dialog>`, `getComputedStyle(dialog, '::backdrop').opacity`
   restituisce `0.6`. È su questo che il gesto schiarisce lo scrim senza toccare il DOM.
3. **L'ordine di `@import` conta.** `v3/overlays.css` deve stare **dopo** `v2/shell.css`, che
   dichiara `:focus-visible{ …; box-shadow: 0 0 0 5px rgba(29,138,147,.3) }`. A pari specificità
   vince l'ultimo: se il foglio arrivasse prima, il `box-shadow` dell'anello sostituirebbe
   `--shadow-5` sul pannello nel momento in cui prende il fuoco. `.ovl__panel:focus-visible` qui
   sotto lo risolve comunque, ma l'ordine resta parte del contratto.

```css
/* ============================================================================
   OVERLAYS V3 — «il vestibolo» · docs/design-v3/specs/overlays.md
   Una primitiva (<dialog>), cinque ancoraggi, una soglia.
   ========================================================================== */

/* ---- 1. TOKEN ----------------------------------------------------------- */
:root{
  --dir: 1;
  --ovl-scrim-near: rgb(10 21 28 / .55);
  --ovl-scrim-far:  rgb(10 21 28 / .86);
  --ovl-scrim-deep: rgb(10 21 28 / .88);
  --ovl-panel: var(--min-2);
  --ovl-panel-dark: var(--mid-2);
  --ovl-edge: var(--on-dark-3);
  --ovl-threshold-line: var(--terr-line-lt);
  --layer-pop: 30;
  --layer-toast: 50;
  --ovl-drag: 0px;
  --ovl-progress: 0;
}
[dir="rtl"]{ --dir: -1; }

/* ---- 2. LA PRIMITIVA ---------------------------------------------------- */
/* max-*-size:none annulla la morsa UA `calc(100% - 2em - 6px)` (MUST-FIX 1).
   display è dichiarato solo su [open]: senza l'attributo la regola UA
   `dialog:not([open]){display:none}` deve continuare a vincere. */
.ovl{
  padding:0; border:0; margin:0; inset:0;
  inline-size:100%; block-size:100%;
  max-inline-size:none; max-block-size:none;
  background:transparent; color:var(--ink); overflow:visible;
}
.ovl[open]{ display:flex; }
.ovl::backdrop{
  background:radial-gradient(farthest-corner at var(--ovl-origin, 50% 50%),
             var(--ovl-scrim-near) 0%, var(--ovl-scrim-far) 100%);
  opacity:calc(1 - var(--ovl-progress));
}
/* Regola 2 di §4.6: mai due scrim. overlays.js marca quello sotto. */
.ovl[data-ovl-covered]::backdrop{ background:transparent; }

.ovl__panel{
  position:relative; display:flex; flex-direction:column;
  inline-size:100%; max-inline-size:var(--ovl-max, 34rem);
  max-block-size:min(84dvh, 46rem);
  background:var(--ovl-panel); border:1px solid var(--hairline); border-radius:0;
  box-shadow:var(--shadow-5); overscroll-behavior:contain;
}
/* Contenitore d'ingresso, non controllo: niente anello, e l'ombra di ruolo resta. */
.ovl__panel:focus-visible{ outline:none; box-shadow:var(--shadow-5); }

/* LA SOGLIA — emendamento A1. Posizionata sul padding box, quindi il bordo di 1px
   le fa da cornice e la stacca dallo scrim (1,06:1 senza cornice, misurato). */
.ovl__panel::before{
  content:""; position:absolute; z-index:1;
  inset-block-start:0; inset-inline:0; block-size:3px;
  background:linear-gradient(var(--ovl-threshold-angle, 90deg), transparent 0,
             var(--ovl-threshold-line) 12%, var(--ovl-threshold-line) 88%, transparent 100%);
  transform:scaleX(var(--ovl-threshold-scale, 1)); transform-origin:50% 50%;
}

.ovl[data-ovl-size="sm"]{ --ovl-max:26rem; }
.ovl[data-ovl-size="md"]{ --ovl-max:34rem; }
.ovl[data-ovl-size="lg"]{ --ovl-max:46rem; }

/* ---- 3. I CINQUE ANCORAGGI ---------------------------------------------- */
/* DIALOG — centrata. La luce è il pannello. */
.ovl[data-ovl="dialog"]{
  align-items:center; justify-content:center; padding:var(--s-6); --ovl-origin:50% 50%; }

/* SHEET — dal basso. Gradiente lineare: il chiaro è il bordo d'ingresso del foglio. */
.ovl[data-ovl="sheet"]{ align-items:flex-end; justify-content:center; }
.ovl[data-ovl="sheet"]::backdrop{
  background:linear-gradient(to top, var(--ovl-scrim-near), var(--ovl-scrim-far)); }
.ovl[data-ovl="sheet"] .ovl__panel{
  max-inline-size:none; max-block-size:88dvh; border-inline:0; border-block-end:0;
  transform:translateY(var(--ovl-drag)); }

/* DRAWER — dal bordo di lettura. justify-content:flex-start segue `direction`,
   quindi in RTL entra da destra senza una riga in più (verificato: pannello a x=863
   su 1279). La soglia passa sul bordo d'ingresso, cioè quello che guarda la pagina. */
.ovl[data-ovl="drawer"]{ align-items:stretch; justify-content:flex-start; --ovl-origin:0% 50%; }
[dir="rtl"] .ovl[data-ovl="drawer"]{ --ovl-origin:100% 50%; }
.ovl[data-ovl="drawer"] .ovl__panel{
  max-inline-size:none; inline-size:min(26rem, 78vw); block-size:100dvh; max-block-size:none;
  border:0; border-inline-end:1px solid var(--hairline);
  transform:translateX(calc(var(--ovl-drag) * var(--dir))); }
.ovl[data-ovl="drawer"] .ovl__panel::before{
  --ovl-threshold-angle:180deg;
  inset-block:0; inset-inline:auto 0; inline-size:3px; block-size:auto;
  transform:scaleY(var(--ovl-threshold-scale, 1)); }

/* PALETTE — l'unica superficie scura. La pagina è SPENTA, non smerigliata. */
.ovl[data-ovl="palette"]{
  align-items:flex-start; justify-content:center; padding:12vh var(--s-4) var(--s-4); }
.ovl[data-ovl="palette"]::backdrop{ background:var(--ovl-scrim-deep); }
.ovl[data-ovl="palette"] .ovl__panel{
  --ovl-max:38rem; --ovl-threshold-line:var(--terr-line);
  background:var(--ovl-panel-dark); border-color:var(--ovl-edge); color:var(--on-dark); }
.ovl[data-ovl="palette"] .ovl__title{ color:var(--on-dark); }
.ovl[data-ovl="palette"] .ovl__eyebrow{ color:var(--on-dark-3); }
.ovl[data-ovl="palette"] .ovl__body{ color:var(--on-dark-2); }
.ovl[data-ovl="palette"] .ovl__close{ color:var(--on-dark-2); }

/* FULL — un testo prescritto lungo, letto per intero. */
.ovl[data-ovl="full"]{ align-items:stretch; justify-content:center; padding-block-start:var(--s-8); }
.ovl[data-ovl="full"] .ovl__panel{ --ovl-max:54rem; max-block-size:none; border-block-end:0; }

/* Zona di trascinamento: la TESTA, piena larghezza, 44px+ di altezza.
   Nessuna maniglia grigia (segnale n.1 della revisione). overlays.js ignora i
   pointerdown il cui target ha un .closest('button, a, input, select, textarea'). */
.ovl[data-ovl="sheet"] .ovl__head,
.ovl[data-ovl="drawer"] .ovl__head{ touch-action:none; }

/* ---- 4. SOTTO 48rem: ogni dialog diventa sheet; il drawer va a schermo intero (A4) */
@media (max-width:47.999rem){
  .ovl[data-ovl="dialog"]{ align-items:flex-end; padding:0; }
  .ovl[data-ovl="dialog"]::backdrop{
    background:linear-gradient(to top, var(--ovl-scrim-near), var(--ovl-scrim-far)); }
  .ovl[data-ovl="dialog"] .ovl__panel{
    max-inline-size:none; max-block-size:88dvh; border-inline:0; border-block-end:0;
    transform:translateY(var(--ovl-drag)); }
  .ovl[data-ovl="dialog"] .ovl__head{ touch-action:none; }

  .ovl[data-ovl="drawer"] .ovl__panel{
    inline-size:100%; border:0; border-block-start:1px solid var(--hairline); }
  .ovl[data-ovl="drawer"] .ovl__panel::before{
    --ovl-threshold-angle:90deg;
    inset-block:0 auto; inset-inline:0; inline-size:auto; block-size:3px;
    transform:scaleX(var(--ovl-threshold-scale, 1)); }
  /* Il pannello copre il 100% del viewport: lo scrim non avrebbe niente da velare
     e oggi viene dipinto a vuoto a ogni apertura (§1.6). */
  .ovl[data-ovl="drawer"]::backdrop{ background:transparent; }
  .ovl[data-ovl="palette"]{ padding-block-start:var(--s-8); }
}

/* ---- 5. TESTA / CORPO / PIEDE ------------------------------------------- */
.ovl__head{ flex:0 0 auto; display:grid; grid-template-columns:minmax(0,1fr) auto;
  gap:var(--s-2) var(--s-4); padding:var(--s-6) var(--s-6) var(--s-4); align-items:start; }
.ovl__eyebrow{ grid-column:1; margin:0; font-family:var(--f-mono); font-size:var(--t-caption);
  line-height:var(--t-caption-lh); letter-spacing:var(--track-folio); text-transform:uppercase;
  color:var(--ink-3); font-variant-numeric:tabular-nums; }
.ovl__title{ grid-column:1; margin:0; font-family:var(--f-serif); font-weight:400;
  font-size:var(--t-entry); line-height:var(--t-entry-lh); color:var(--ink); }
.ovl__close{ grid-column:2; grid-row:1 / span 2; inline-size:44px; block-size:44px;
  display:grid; place-items:center; border:0; border-radius:var(--radius-control);
  color:var(--ink-2); background:transparent; cursor:pointer; }
.ovl__body{ flex:1 1 auto; min-block-size:0; overflow-y:auto; overscroll-behavior:contain;
  padding:0 var(--s-6) var(--s-4); font-size:var(--t-body); line-height:var(--t-body-lh); }
.ovl__body > * { max-inline-size:65ch; }
.ovl__foot{ flex:0 0 auto; display:flex; flex-wrap:wrap; gap:var(--s-3); justify-content:flex-end;
  border-block-start:1px solid var(--hairline);
  padding:var(--s-4) var(--s-6) max(var(--s-6), env(safe-area-inset-bottom)); }
/* Il primario NON è ridichiarato qui: static/css/v3/buttons.css è la sola fonte. */

/* Stati che appartengono all'overlay e non al sistema dei bottoni. */
.ovl__alert{ margin:0 0 var(--s-4); padding:var(--s-3) var(--s-4);
  border-inline-start:3px solid var(--err-700); background:var(--err-100); color:var(--err-700);
  font-size:var(--t-ui); line-height:var(--t-ui-lh); }
@media (hover:hover){
  .ovl__close:hover{ background:var(--min-1); color:var(--ink); }
  .ovl[data-ovl="palette"] .ovl__close:hover{ background:var(--mid-3); color:var(--on-dark); }
}
@media (prefers-reduced-motion: no-preference) and (hover: hover){
  .ovl__close{ transition: background-color var(--motion-instant) var(--ease-in),
                           color var(--motion-instant) var(--ease-in); }
  .ovl__close:hover{ transition-duration: var(--motion-fast);
                     transition-timing-function: var(--ease-out); }
}

/* ---- 6. BLOCCO DELLO SCORRIMENTO (§1.10) -------------------------------- */
/* Misurato: showModal() da solo NON ferma il documento. Il body va fissato e lo
   scrollTop conservato; overlays.js scrive --ovl-scroll-y e ripristina con
   { behavior: 'instant' }, perché il sito ha scroll-behavior: smooth. */
html[data-ovl-lock]{ overflow:hidden; }
body[data-ovl-lock]{ position:fixed; inset-inline:0; inline-size:100%;
  inset-block-start:calc(-1 * var(--ovl-scroll-y, 0px)); overflow:hidden; }

/* ---- 7. POPOVER NATIVI (<details>) — risolve §1.1 ----------------------- */
details[data-dropdown][open]{ position:relative; z-index:var(--layer-pop); }
.ovl-pop__list{ background:var(--min-3); border:1px solid var(--hairline);
  box-shadow:var(--shadow-3); border-radius:0; padding-block:var(--s-2); margin:0; }
.ovl-pop__list a, .ovl-pop__list button{ min-block-size:44px; display:flex; align-items:center;
  gap:var(--s-3); padding-inline:var(--s-4); inline-size:100%; }
@media (pointer:fine){ .ovl-pop__list a, .ovl-pop__list button{ min-block-size:36px; } }

/* ---- 8. TOAST ------------------------------------------------------------ */
.ovl-toasts{ position:fixed; z-index:var(--layer-toast); margin:0; padding:0; list-style:none;
  inset-block-end:max(var(--s-6), env(safe-area-inset-bottom)); inset-inline-end:var(--s-6);
  inline-size:min(92vw, 24rem); display:flex; flex-direction:column; gap:var(--s-2); }
.ovl-toasts[data-ovl-shifted]{ inset-block-end:calc(max(var(--s-6), env(safe-area-inset-bottom))
                                                    + var(--s-10)); }  /* 2.4.11, §6g */
.ovl-toast{ display:grid; grid-template-columns:auto minmax(0,1fr) auto; align-items:start;
  gap:var(--s-3); background:var(--min-2); border:1px solid var(--hairline);
  border-inline-start:3px solid var(--ovl-toast-bar, var(--ink-2)); box-shadow:var(--shadow-3);
  padding-block:var(--s-3); padding-inline:var(--s-4) var(--s-3);
  font-size:var(--t-ui); line-height:var(--t-ui-lh); color:var(--ink); }
.ovl-toast[data-tone="success"]{ --ovl-toast-bar:var(--ok-700); }
.ovl-toast[data-tone="info"]{ --ovl-toast-bar:var(--ink-2); }
.ovl-toast__word{ font-weight:500; }
.ovl-toast .ovl__close{ grid-column:3; grid-row:1; }
@media (max-width:47.999rem){ .ovl-toasts{ inset-inline:var(--s-4); inline-size:auto; } }

/* ---- 9. GLOSSARIO INLINE (niente tooltip) -------------------------------- */
.ovl-hint{ display:inline; }
.ovl-hint__trigger{ background:none; border:0; padding:0; font:inherit; color:inherit;
  text-decoration:underline dotted; text-underline-offset:3px; cursor:help; }
.ovl-hint__note{ display:block; margin-block:var(--s-2); max-inline-size:22rem;
  background:var(--min-3); border:1px solid var(--hairline); box-shadow:var(--shadow-3);
  padding:var(--s-3) var(--s-4); font-size:var(--t-small); line-height:var(--t-small-lh);
  color:var(--ink); }
.ovl-hint__trigger[aria-expanded="false"] + .ovl-hint__note{ display:none; }

/* ---- 10. SENZA JAVASCRIPT ------------------------------------------------ */
/* templates/base.html:2 spedisce `class="no-js"`, tolta da static/js/head.js:3.
   Un <dialog> senza [open] è display:none per regola UA; qui una regola d'autore
   di specificità superiore lo rimette in flusso, com'è oggi per .nav-drawer
   (components.css:866 e :879), che questo cambiamento sostituisce. */
html.no-js .nav-toggle{ display:none; }
html.no-js .site-header__inner{ flex-wrap:wrap; }
html.no-js .ovl[data-ovl="drawer"]{
  display:block; position:static; inset:auto; inline-size:auto; block-size:auto;
  max-block-size:none; flex-basis:100%; }
html.no-js .ovl[data-ovl="drawer"] .ovl__panel{
  inline-size:auto; block-size:auto; max-block-size:none; border:0; box-shadow:none;
  background:transparent; transform:none; }
html.no-js .ovl[data-ovl="drawer"] .ovl__panel::before,
html.no-js .ovl[data-ovl="drawer"] .ovl__close{ display:none; }
html.no-js .ovl[data-ovl="drawer"] .ovl__head{ padding-inline:0; }
html.no-js .ovl[data-ovl="drawer"] .ovl__body{ overflow:visible; padding-inline:0; }
html.no-js .ovl[data-ovl="drawer"] .ovl__foot{ padding-inline:0; justify-content:flex-start; }
html.no-js .ovl-toasts{ position:static; inline-size:auto; }
html.no-js .ovl-hint__note{ display:block; }   /* la definizione è nel flusso */

/* ---- 11. CONTRASTO FORZATO (§1.11) --------------------------------------- */
/* Misurato senza queste regole: il gradiente sparisce (le immagini di sfondo non
   sono forzate) e il ::backdrop resta rgba(255,255,255,0) — la modale non vela
   più niente. Con queste regole il velo è opaco e il pannello è identificato dal
   suo bordo, non dal suo riempimento. La specificità [data-ovl] pareggia quella
   delle regole d'ancoraggio che azzerano i bordi. */
@media (forced-colors: active){
  .ovl::backdrop, .ovl[data-ovl="palette"]::backdrop,
  .ovl[data-ovl="sheet"]::backdrop, .ovl[data-ovl="dialog"]::backdrop{ background:Canvas; }
  .ovl[data-ovl] .ovl__panel{
    background:Canvas; color:CanvasText; border:2px solid CanvasText; box-shadow:none; }
  .ovl[data-ovl] .ovl__panel::before{ background:CanvasText; }
  .ovl[data-ovl] .ovl__title, .ovl[data-ovl] .ovl__eyebrow,
  .ovl[data-ovl] .ovl__body{ color:CanvasText; }
  .ovl__close{ border:1px solid ButtonText; color:ButtonText; }
  .ovl-toast, .ovl-pop__list, .ovl-hint__note{
    background:Canvas; color:CanvasText; border:2px solid CanvasText; box-shadow:none; }
  .ovl-toast{ border-inline-start-width:6px; }   /* la barra semantica sopravvive come spessore */
}
```

**Geometria verificata** (pannello, in px, `data-ovl-size="md"`):

| Viewport | dialog | sheet | drawer | palette | full |
|---|---|---|---|---|---|
| 390×844 | 390 × auto, in basso | 390 × auto, in basso | **390 × 844** | 358 × auto, `y = 32` | 390 × 812 |
| 768×1024 | 544, centrata | 768 | **416 × 1024** | 608, `y = 122,9` | 768 × 992 |
| 1024×800 | 544 | 1024 | **416 × 800**, scrim 608 | 608, `y = 96` | 864 × 768 |
| 1279×800 | 544 | 1279 | **416**, scrim 863 | 608 | 864 |
| 1440×900 | 544, `x = 448` | 1440 | 416 | 608, `y = 108` | 864 × 868 |
| 1279×800 **RTL** | 544 | 1279 | **416 a `x = 863`** | 608 | 864 |

In tutti i casi `max-inline-size` e `max-block-size` del `<dialog>` misurano `none`, e il rettangolo
del `<dialog>` è esattamente il viewport. La chiusura misura `44 × 44` ovunque.

### 4.4 Il drawer, rifatto — markup Django

Testa (lock-up 56 px + **la riga del promotore** + chiusura 44 px) · corpo scorrevole (le otto
sezioni come `<details>`, voci a 52 px) · piede fisso (CTA a piena larghezza, poi «Espace réservé» e
le lingue a 44 px). Larghezza `min(26rem, 78vw)` da 48rem in su, schermo intero sotto (A4).

```django
{# templates/partials/header.html — il drawer sostituisce <div class="nav-drawer"> #}
<dialog class="ovl" id="nav-drawer" data-ovl="drawer" data-ovl-dismiss="light"
        aria-labelledby="nav-drawer-t">
  <div class="ovl__panel" tabindex="-1" autofocus>
    <header class="ovl__head ovl__head--letterhead">
      <p class="visually-hidden" id="nav-drawer-t">{% translate "Navigation principale" %}</p>
      <a class="brand brand--lockup" href="{% url 'pages:home' %}"
         aria-label="{{ site.project_name }} — {% translate 'accueil' %}">
        {% if site.settings and site.settings.use_logo_image and site.settings.logo %}
          <img class="brand__logo" src="{{ site.settings.logo.url }}"
               alt="{{ site.project_name }}" width="160" height="40">
        {% else %}{% brand_lockup %}{% endif %}
      </a>
      <button class="ovl__close" type="button" data-ovl-close
              aria-label="{% translate 'Fermer' %}">{% svg_icon "close" "icon" %}</button>
      {# MUST-FIX 8 — verbatim da header.html:26. Sotto 47.999rem .utility-bar è display:none
         (v2/shell.css), quindi questo è l'UNICO posto in cui il promotore compare su telefono. #}
      <p class="ovl__attribution"><strong>{{ site.promoter }}</strong> —
         {% translate "promoteur du projet" %}</p>
    </header>

    <div class="ovl__body">
      <nav class="main-nav" aria-label="{% translate 'Navigation principale' %}">
        {% include "partials/main_nav.html" %}
      </nav>
    </div>

    <footer class="ovl__foot ovl__foot--drawer">
      {% safe_url 'orientation:start' as orientation_url %}
      {% if orientation_url %}
        <a class="btn btn--primary ovl__cta" href="{{ orientation_url }}"
           data-ovl-focus>{% translate "Questionnaire d’orientation" %}</a>
      {% endif %}
      {# MUST-FIX 8 — i tre guardiani esistenti, riportati senza toccarli. #}
      {% flag "reserved_area_public_link" as reserved_link_drawer %}
      {% if not user.is_authenticated and reserved_link_drawer and site.settings.reserved_area_enabled %}
        {% safe_url 'account_login' as login_url_drawer %}
        {% if login_url_drawer %}
          <a class="ovl__foot-link" href="{{ login_url_drawer }}">{% svg_icon "lock" "icon" %}
            <span>{% translate "Espace réservé" %}</span></a>
        {% endif %}
      {% endif %}
      {% include "components/language_switcher.html" %}
    </footer>
  </div>
</dialog>
```

```css
/* Complemento di §4.3 per il capo-lettera del drawer. */
.ovl__head--letterhead{ grid-template-columns:minmax(0,1fr) auto; align-items:center;
  min-block-size:56px; padding-block:var(--s-3) var(--s-4); }
.ovl__head--letterhead .brand{ grid-column:1; grid-row:1; }
.ovl__head--letterhead .ovl__close{ grid-column:2; grid-row:1; }
.ovl__attribution{ grid-column:1 / -1; grid-row:2; margin:0;
  font-size:var(--t-small); line-height:var(--t-small-lh); color:var(--ink-2); }
.ovl__foot--drawer{ flex-direction:column; align-items:stretch; justify-content:flex-start;
  gap:var(--s-4); }
.ovl__foot--drawer .ovl__cta{ inline-size:100%; justify-content:center; min-block-size:48px; }
.ovl__foot-link{ display:flex; align-items:center; gap:var(--s-3); min-block-size:44px;
  color:var(--ink); }
```

`data-ovl-focus` sulla CTA: il fuoco d'ingresso va alla decisione, non alla chiusura (§1.9). Lo
`stagger` delle otto voci è `overlay.drawer.rows` (§5).

### 4.5 Toast e glossario — con il codice che mancava

**Come si separano i messaggi Django (lacuna 7).** `message.tags` non si presta a un test di
appartenenza in un template; `message.level` sì, ed è un intero documentato:
`DEBUG 10 · INFO 20 · SUCCESS 25 · WARNING 30 · ERROR 40`. La soglia è **30**. Lo storage dei
messaggi si può iterare due volte nella stessa resa (`BaseStorage.__iter__` restituisce
`iter(self._loaded_messages)`, che resta popolato), quindi le due liste si scrivono di seguito.

```django
{# templates/components/toasts.html — sostituisce templates/base.html 57-60 #}
{% load i18n %}
{# La regione live esiste SEMPRE, anche vuota: overlays.js ci appende i toast tardivi. #}
<ol class="ovl-toasts" id="ovl-toasts" role="status" aria-live="polite" aria-relevant="additions">
  {% for message in messages %}{% if message.level < 30 %}
  <li class="ovl-toast" data-ovl-toast
      data-tone="{% if message.level == 25 %}success{% else %}info{% endif %}">
    <span class="ovl-toast__glyph" aria-hidden="true">
      {% if message.level == 25 %}{% svg_icon "check" "icon" %}
      {% else %}{% svg_icon "info" "icon" %}{% endif %}</span>
    <p class="ovl-toast__text"><b class="ovl-toast__word">
      {% if message.level == 25 %}{% translate "Terminé" %}
      {% else %}{% translate "Information" %}{% endif %}</b> {{ message }}</p>
    <button class="ovl__close" type="button" data-ovl-toast-close
            aria-label="{% translate 'Fermer' %}">{% svg_icon "close" "icon" %}</button>
  </li>
  {% endif %}{% endfor %}
</ol>
{% if messages %}
<div class="container messages">
  {% for message in messages %}{% if message.level >= 30 %}
  {# error e warning restano NEL FLUSSO: non spariscono, non hanno scadenza. #}
  <div class="alert alert--{{ message.tags|default:'info' }}"
       {% if message.level >= 40 %}role="alert"{% endif %}>{{ message }}</div>
  {% endif %}{% endfor %}
</div>
{% endif %}
```

**La pila.** Tre al massimo, lista verticale, `gap: var(--s-2)`, tutti a piena opacità, il più
recente in fondo (vicino al pollice e all'angolo di lettura). Il quarto rimuove il primo. Nessuna
scala, nessun arretramento (segnale n.2). Barra semantica di 3 px sul bordo iniziale —
`--ok-700` 5,10 : 1 per `success`, `--ink-2` 6,87 : 1 per `info` — **mai `--accent`**: l'accento
interattivo non decora, e una barra `info` in `--accent` sarebbe stata una violazione della regola
1 di DS §1.3 che la revisione non ha visto. Il colore non è mai solo: glifo + parola in grassetto
500 + testo. Chiusura 44 px, scadenza 6 s in pausa su `hover`, `focus-within` e
`document.hidden`; **nessuna scadenza** con reduced-motion o oltre 120 caratteri (WCAG 2.2.1).
Senza JS, `html.no-js .ovl-toasts{ position:static }` rimette la lista nel flusso: è il
comportamento attuale.

**Un toast non coesiste mai con un overlay aperto** (MUST-FIX 2, §4.7). Se ne arriva uno mentre un
overlay è aperto, la coda lo trattiene e lo monta alla chiusura. Non è una perdita: un toast non
porta mai l'unica copia di un'informazione, e la regola di sostanza di §4 dice che dentro un overlay
non si lavora, quindi un overlay aperto non genera quasi mai un toast.

**Glossario: niente tooltip.** `templates/forum/governance/participation.html` ha già scritto la
regola giusta («una colonna, non un tooltip»).

```django
<span class="ovl-hint">
  <button class="ovl-hint__trigger" type="button" aria-expanded="false"
          aria-controls="hint-{{ term.slug }}">{{ term.label }}</button>
  <span class="ovl-hint__note" id="hint-{{ term.slug }}" role="note">{{ term.definition }}</span>
</span>
```

Rivelata al clic o a Invio, **mai** al passaggio del puntatore, mai con informazione necessaria a un
compito. Il bersaglio è testo in linea dentro una frase, quindi l'eccezione di 2.5.8 si applica e i
24 px non sono richiesti; il `<button>` resta però raggiungibile da tastiera e Escape chiude.

### 4.6 Palette comandi, cancello di ruolo, regole dure

`Ctrl/⌘ K` **più** un pulsante visibile nella barra piattaforma (la scorciatoia non è l'unico
accesso, 2.1.1). Input 56 px con prefisso mono che porta il riferimento del fascicolo corrente;
risultati raggruppati (**Fascicoli · Sezioni · Azioni · Aiuto**), responsabile a destra in
`--f-mono`. Le voci vengono dai link **già renderizzati nella pagina**, raccolti a runtime, più una
lista di azioni scritta nel template. Nessuna vista, nessun endpoint, nessun filtro client su dati
protetti. La palette **naviga e filtra**, non esegue mai un'azione governata. Nessun `.ovl__foot`:
una palette non ha azioni di piede.

**Il cancello, nel vocabolario reale del prodotto (MUST-FIX 11).** `AccountType`
{person, company, institution, university, professional, staff} è ciò che un visitatore
**dichiara**; i ruoli sono gruppi Django in `apps/accounts/roles.py` e sono ciò che il progetto ha
**verificato** (il commento di `VerificationStatus` in `apps/accounts/models.py` spiega perché i due
non vanno confusi). DS §9.1 nomina «operatore / professionista / redattore / admin»; tradotto:

```python
# apps/accounts/roles.py — nessun permesso nuovo, nessuna migrazione.
#: DESIGN_SYSTEM_V2 §9.1: i ruoli a cui la barra piattaforma offre la palette comandi.
#: «redattore» sono i due ruoli di redazione: giuridica ed editoriale.
COMMAND_PALETTE_ROLES: frozenset[str] = frozenset(
    {OPERATOR, PROFESSIONAL, LEGAL_EDITOR, CONTENT_EDITOR, ADMINISTRATOR, SUPERADMIN}
)
```

```python
# apps/core/templatetags/ile_core.py — il modulo è già in TEMPLATES["OPTIONS"]["builtins"].
@register.simple_tag(takes_context=True)
def can_command_palette(context) -> bool:
    """Se la barra piattaforma mostra la palette. Visibilità di chrome, non autorizzazione."""
    user = context.get("user")
    if not (user and user.is_authenticated):
        return False
    cached = getattr(user, "_ile_palette", None)
    if cached is None:
        from accounts.roles import COMMAND_PALETTE_ROLES
        cached = bool(COMMAND_PALETTE_ROLES & set(user.groups.values_list("name", flat=True)))
        user._ile_palette = cached
    return cached
```

```django
{% can_command_palette as palette_ok %}
{% if palette_ok %}
  <button class="portal-bar__palette" type="button" data-ovl-open="command-palette"
          aria-haspopup="dialog" aria-controls="command-palette">
    {% svg_icon "search" "icon" %}<span>{% translate "Aller à…" %}</span>
    <kbd class="portal-bar__kbd">Ctrl K</kbd></button>
  {% include "components/command_palette.html" %}
{% endif %}
```

`perms` non basta: `role:professional` non porta permessi di modello (`ROLE_PERMISSIONS` non lo
elenca), quindi `{% if perms.cases %}` escluderebbe il professionista che DS §9.1 include
esplicitamente. Il test è quindi sull'appartenenza al gruppo.

**Perché non il ruolo per incarico.** `AssignmentRole.OPERATOR` (`apps/cases/models.py:311`) è un
ruolo **dentro un fascicolo**, non su un account: esiste solo in relazione a un `CaseFile` e a un
`authorisation_reference`. La palette è chrome **globale**, presente anche dove non c'è un fascicolo
in ambito; gattarla con un ruolo per incarico richiederebbe di scegliere un fascicolo arbitrario per
decidere se disegnare un pulsante, che è un modello di sicurezza diverso e peggiore. E il cancello
non è comunque una barriera: la palette mostra solo link **già renderizzati dal server per quella
persona**, quindi forzarla aperta non espone niente. La frase «visibilità di chrome, non
autorizzazione» va nel docstring perché nessuno la scambi per un controllo.

**Regole dure.** (1) Un solo overlay modale per volta; il drawer è l'unica eccezione e i `<details>`
al suo interno non sono overlay. (2) Escape chiude sempre il più interno per primo, con uno stack in
`overlays.js`, e **mai due scrim a schermo**: quello sotto prende `data-ovl-covered`, che azzera il
suo `::backdrop` (verificato, §4.3). (3) Il fuoco all'apertura va su `[data-ovl-focus]`, altrimenti
sul pannello via `autofocus`, **mai** sulla chiusura; alla chiusura torna a chi ha aperto, o all'`h1`
della pagina se quell'elemento non c'è più. (4) **`inert` non lo mettiamo noi**: `showModal()` rende
inerte tutto ciò che è fuori dal dialogo — verificato, un `<button>` in un popover del top layer non
riceve nemmeno il fuoco mentre una modale è aperta. Quello che dobbiamo mettere noi è il **blocco
dello scorrimento con `scrollTop` conservato**, perché lo UA non lo dà (§1.10, misurato). (5) Lo
sheet usa `dvh`, così il piede resta sopra la tastiera virtuale. (6) Se un overlay è aperto la coda
dei toast è trattenuta.

### 4.7 `overlays.js` — contratto, ciclo di vita, uscita, gesto

```js
import { animate, withMotion, reducedMotion, SPRING_SETTLE } from "./motion.js";

const EASE_OUT = [0.25, 1, 0.5, 1];          // --ease-out
const EASE_IN  = [0.7, 0, 0.3, 1];           // --ease-in
const SLOW = 0.32, BASE = 0.24, FAST = 0.18, INSTANT = 0.12;   // i quattro token, in secondi
const stack = [];                            // overlay aperti, il più interno in fondo
const held  = [];                            // toast in attesa che lo stack si svuoti
```

**Apertura** `open(ovl, opener)`
1. `stack.at(-1)?.setAttribute("data-ovl-covered", "")` — un solo scrim.
2. `ovl.__opener = opener ?? document.activeElement`.
3. Se `stack` è vuoto: `lockScroll()` — legge `window.scrollY` **una volta**, lo scrive in
   `--ovl-scroll-y` su `documentElement` e mette `data-ovl-lock` su `html` e `body`.
4. `ovl.showModal()` — il top layer, l'inerzia del resto e la trappola del fuoco sono dello UA.
5. Il fuoco: `ovl.querySelector("[data-ovl-focus]")?.focus()`; altrimenti lo ha già il pannello per
   via di `autofocus`. **Mai** la chiusura.
6. Entrata, tutta dentro `withMotion` (§5).
7. `stack.push(ovl)`.

**Uscita** `close(ovl)` — questo è il meccanismo che mancava (MUST-FIX 3, lacuna 1)
```js
async function close(ovl){
  if (ovl.__closing) return; ovl.__closing = true;
  ovl.__enter?.forEach(a => a.cancel());
  const panel = ovl.querySelector(".ovl__panel");
  const anims = withMotion(
    () => [
      animate(panel, exitFrames(ovl), { duration: FAST, ease: EASE_IN }),
      // ::backdrop non è selezionabile: si anima con l'opzione pseudoElement.
      animate(ovl, { opacity: [1, 0] },
              { duration: FAST, ease: EASE_IN, pseudoElement: "::backdrop" }),
    ],
    () => null                       // reduced-motion: nessuna animazione, si chiude subito
  );
  if (anims) { try { await Promise.all(anims); } catch { /* annullata */ } }
  ovl.close();                       // solo ADESSO: close() è sincrono e mette display:none
}
```
`ovl.addEventListener("close", …)` fa il resto: `stack.pop()`, toglie `data-ovl-covered` al nuovo
ultimo, `unlockScroll()` se lo stack è vuoto (`window.scrollTo({ top: y, behavior: "instant" })` —
il sito ha `scroll-behavior: smooth` e senza `instant` il ritorno sarebbe un'animazione non
dichiarata), rimette il fuoco su `ovl.__opener` se è ancora nel documento e altrimenti sull'`h1`,
lancia `overlay.return` e svuota `held`.

**Prova che il meccanismo esiste**, misurata in questo giro sulla pagina viva:
`animate(el, …, { pseudoElement: "::backdrop" })` importata da `/static/js/dist/motion.js` produce
un'animazione con `effect.pseudoElement === "::backdrop"` e l'opacità del `::backdrop` letta a
metà corsa vale `0.805`; lo stesso con `"::before"` per la soglia (`matrix(0.773642, 0, 0, 1, 0, 0)`
a metà corsa). Lo stesso funziona con WAAPI nuda (`el.animate(frames, { pseudoElement })`), che
resta la via di ripiego se Motion cambiasse firma. `@starting-style` e
`transition-behavior: allow-discrete` sono supportati dal motore (verificato:
`CSS.supports("transition-behavior","allow-discrete") === true`, `@starting-style` produce una
`CSSStartingStyleRule`) ma **non si usano**: tutto il moto di questa superficie passa da
`withMotion`, che è l'unico punto d'ingresso prescritto da MOTION_SYSTEM §3, e due meccanismi di
uscita in parallelo sono un meccanismo di troppo.

**Escape.** `ovl.addEventListener("cancel", e => { e.preventDefault(); if (ovl.dataset.ovlDismiss
!== "none") close(ovl); })`. Senza `preventDefault()` lo UA chiude all'istante e l'uscita non si
vede mai. Verificato: `defaultPrevented === true` e `dialog.open` resta `true`.

**Clic fuori.** Il `<dialog>` riempie il viewport e il pannello è il suo unico figlio, quindi
```js
ovl.addEventListener("click", e => {
  if (e.target === ovl && ovl.dataset.ovlDismiss !== "none") close(ovl);
});
```
è esattamente «hai cliccato fuori dal pannello» — verificato: un clic a fianco del pannello dà un
colpo con `e.target === ovl`, un clic dentro ne dà zero. Più affidabile del confronto con le
coordinate del `::backdrop`, che non è un elemento.

**Il gesto** (`overlay.sheet.drag`). `pointerdown` sulla testa; si esce subito se
`e.target.closest("button, a, input, select, textarea, summary")` — è così che la testa può essere
sia la maniglia sia il posto dove sta la chiusura. Poi un `pointermove` strozzato da
`requestAnimationFrame` che scrive **due proprietà e basta**:
```js
panel.style.setProperty("--ovl-drag", dy + "px");            // dy < 0 → resistenza dy/3
ovl.style.setProperty("--ovl-progress", String(progress));   // ereditata dal ::backdrop
```
Nessun `getBoundingClientRect` nel ciclo: l'altezza del pannello è misurata una volta al
`pointerdown`. `user-select:none` sul pannello per la durata del gesto. Al `pointerup`: sotto la
soglia (96 px **e** velocità < 0,5 px/ms) `overlay.sheet.settle` con `SPRING_SETTLE`; sopra,
`overlay.sheet.dismiss` e poi `close()`. Con reduced-motion il gesto è disattivato e restano
Escape, la chiusura e il clic fuori (2.5.7: l'alternativa a puntatore singolo esiste sempre).

**La coda dei toast.** `toast(node)`: se `stack.length` il nodo va in `held` (massimo 3, il più
vecchio cade); altrimenti si monta in `#ovl-toasts`. Alla chiusura dell'ultimo overlay,
`held.splice(0).forEach(mount)`. Il timer di 6 s parte al montaggio, non alla creazione.

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` §6

Tutte dentro `withMotion(fn, settle)`. Nessuna curva nuova, nessuna durata nuova. Uscite a 180 ms:
emendamento **A3**. Budget: 0 layout e 0 paint oltre il primo frame nel pannello Performance.

| Nome | Funzione | Innesco | Durata | Curva | Proprietà | Stato ridotto |
|---|---|---|---|---|---|---|
| `overlay.scrim.in` | profondità | apertura | slow 320 | `--ease-out` | `opacity 0→1` su `::backdrop` (`pseudoElement`) | scrim già a 1, fermo |
| `overlay.scrim.out` | orientamento | chiusura | fast 180 | `--ease-in` | `opacity 1→0` su `::backdrop` | `close()` immediato |
| `overlay.threshold.draw` | orientamento | apertura | slow 320 | `--ease-out` | `transform scaleX(0)→scaleX(1)` su `::before` (`scaleY` per il drawer) | soglia intera, ferma |
| `overlay.dialog.in` | profondità | apertura | slow 320 | `--ease-out` | `opacity 0→1`, `translateY 8→0` | pannello completo, immobile |
| `overlay.dialog.out` | orientamento | Escape / chiusura / conferma | fast 180 | `--ease-in` | `opacity 1→0`, `translateY 0→8` | rimozione immediata |
| `overlay.sheet.in` | orientamento | apertura ≤ 47.999rem | slow 320 | `--ease-out` | `translateY 100%→0` | sheet in posizione finale |
| `overlay.sheet.drag` | causalità | `pointermove` sulla testa | **legata al gesto** (MOTION_SYSTEM §2, riga SCROLL: «legata, non temporale») | — | `--ovl-drag` = Δy con resistenza Δy/3 sopra 0; `--ovl-progress` → `::backdrop` | gesto disattivato: restano Escape, chiusura, clic fuori |
| `overlay.sheet.settle` | causalità | `pointerup` sotto soglia (96 px **e** < 0,5 px/ms) | `SPRING_SETTLE` 260/30 | — | `--ovl-drag → 0` | salto immediato a 0 |
| `overlay.sheet.dismiss` | causalità | `pointerup` oltre soglia | fast 180 | `--ease-in` | `translateY → 100%`, `--ovl-progress → 1` | `close()` immediato |
| `overlay.drawer.in` | orientamento | apertura < 80rem | slow 320 | `--ease-out` | `translateX ∓100%→0`, segno da `--dir` | drawer in posizione finale |
| `overlay.drawer.rows` | gerarchia | fine di `drawer.in` | fast 180 per voce, stagger **40 ms**, max 8 | `--ease-out` | `opacity 0→1`, `translateX 8→0` | tutte le voci a opacità 1 |
| `overlay.pop.in` | profondità | `toggle` di `details[data-dropdown]` | fast 180 | `--ease-out` | `opacity 0→1`, `translateY -6→0` | lista già visibile |
| `overlay.pop.out` | orientamento | chiusura / Escape / clic fuori | instant 120 | `--ease-in` | `opacity 1→0` | rimozione immediata |
| `overlay.toast.in` | feedback | montaggio nella lista | base 240 | `--ease-out` | `opacity 0→1`, `translateY 12→0` | toast già al suo posto |
| `overlay.toast.reflow` | causalità | rimozione di un toast | `SPRING_SETTLE` | — | `translateY` dei superstiti (famiglia LAYOUT di MOTION_SYSTEM §2) | salto immediato |
| `overlay.toast.out` | stato | scadenza / chiusura | fast 180 | `--ease-in` | `opacity 1→0`, `translateY 0→8` | rimozione immediata |
| `overlay.palette.in` | profondità | `Ctrl/⌘ K` o pulsante | slow 320 | `--ease-out` | `opacity 0→1`, `translateY 12→0` | palette completa e ferma |
| `overlay.return` | orientamento | chiusura, su chi ha aperto | fast 180 | `--ease-out` | `opacity` di uno `::after` con alone `radial-gradient` **pre-renderizzato** | nessun alone; l'anello di fuoco basta |

**Vincoli.** Nessuna `box-shadow` animata (`overlay.return` anima l'opacità di uno pseudo-elemento,
non un'ombra). Nessun `filter` animato, in nessun punto: il vetro non esiste più in questo
documento. Nessuna scala sul pannello in entrata — l'ho tolta in questo giro, perché `scale(.985→1)`
non è nella riga OVERLAY di MOTION_SYSTEM §2 e perché è la firma di ogni modale del 2024. Nessun
loop ambientale: MOTION_SYSTEM §4 lo spende già sull'eroe.
`matchMedia("(prefers-reduced-motion: reduce)")` è letto **a ogni chiamata**, come fa già
`reducedMotion()` in `static/js/src/motion.js`.

**Reduced motion è uno stato completo, verificato.** Con `prefers-reduced-motion: reduce` attivo e
uno sheet aperto senza JavaScript: `opacity` del pannello `1`, `transform` `matrix(1,0,0,1,0,0)`,
`transform` della soglia `matrix(1,0,0,1,0,0)`, `opacity` del `::backdrop` `1`. Nessun elemento
resta a zero perché **il foglio non contiene né `@keyframes` né `transition`** fuori dal blocco
`@media (prefers-reduced-motion: no-preference)` di §4.3 punto 5: lo stato di riposo del CSS *è* lo
stato finale, e il moto vive solo nel JavaScript, dietro `withMotion`.

---

## 6. ACCESSIBILITÀ E RTL

**Cambia.** (a) Il fuoco d'ingresso non è più la chiusura, e lo è **per markup** (`autofocus` sul
pannello), quindi vale anche se il bundle non arriva — verificato,
`activeElement.className === "ovl__panel"`. (b) `aria-describedby` diventa obbligatorio nel partial e
punta a `.ovl__body`. (c) L'inerzia del resto della pagina è dello UA (`showModal()`), misurata:
mentre una modale è aperta nemmeno un elemento del top layer riceve il fuoco. (d)
`overscroll-behavior: contain` su ogni zona scorrevole. (e) Bersagli: 44 px con `pointer: coarse`,
36 px con `pointer: fine`, mai sotto 24 (2.5.8); la chiusura è 44 × 44 su tutti gli ancoraggi,
misurata. (f) In contrasto forzato il `::backdrop` smette di essere un velo bianco
semitrasparente: `@media (forced-colors: active)` in §4.3 punto 11. Misurato **senza** quel blocco,
il gradiente sparisce del tutto (le immagini di sfondo non sono forzate) e il velo resta
`rgba(255,255,255,0)`, cioè nessun velo: il blocco serve a **restituire** il velo con `Canvas`
opaco, non solo a correggere un colore. (g) Il toast non copre mai un elemento focalizzabile: quando
il fuoco entra negli ultimi 120 px della pagina, `overlays.js` mette `data-ovl-shifted` sulla lista
e la pila arretra di `--s-10` (2.4.11). (h) `role="status"` + `aria-live="polite"` +
`aria-relevant="additions"` sulla regione toast; i messaggi critici restano `role="alert"` nel
flusso. (i) L'anello di focus non sborda mai sullo scrim, dove misurerebbe 1,08 : 1: nessun controllo
sta a meno di 4 px dal bordo interno del pannello.

**RTL.** Solo proprietà logiche. Il drawer usa `justify-content: flex-start` in un contenitore flex,
che segue `direction` da solo: verificato a 1279×800 in `dir="rtl"`, pannello a `x = 863`, scrim a
sinistra, soglia sul bordo sinistro. L'origine dello scrim è l'unica riga specchiata esplicitamente
(`[dir="rtl"] .ovl[data-ovl="drawer"]{ --ovl-origin:100% 50% }`), perché un gradiente non ha
proprietà logiche. Il gesto moltiplica `--dir` (`1` / `-1`). **Non** si specchiano l'asse verticale
dello sheet, il glifo di chiusura, le scale, i numeri. La pila dei toast è ancorata a
`inset-inline-end`, quindi migra a sinistra in AR senza una riga in più. Nella palette il riferimento
del fascicolo è `dir="ltr"` con `unicode-bidi: isolate`, perché è un codice, non una parola.

**HUMAN_QA_REQUIRED.** (1) VoiceOver su iOS col bottom sheet: gesti VO e Pointer Events convivono
solo se verificati a mano. (2) NVDA + Firefox con tre livelli aperti (drawer → `<details>` →
conferma): ordine di Escape e restituzione del fuoco. (3) Trascinamento con dispositivo a
scansione/switch: l'alternativa a pulsante deve esistere e funzionare (2.5.7). (4) Naskh arabo nella
testa dello sheet: interlinea e titolo su due righe a 390 px. (5) Lettura del toast in AR con
`aria-live` e cambio di voce. (6) Windows High Contrast reale su tutti e cinque gli ancoraggi: le
misure di §4.3 punto 11 sono state prese con l'emulazione di Playwright, che usa una tavolozza
chiara. (7) **La coda dei toast trattenuta**: verificare con uno screen reader che un messaggio
annunciato alla chiusura dell'overlay non arrivi durante il ritorno del fuoco.

---

## 7. PRESTAZIONI

### 7.1 Byte — ribasati su misure

**CSS.** Il foglio candidato di §4.3, scritto e provato in questo giro, misura nella sua parte
strutturale **6 648 byte grezzi / 1 828 byte gzip**. Con i commenti, il blocco `forced-colors`, il
blocco `html.no-js`, `.ovl-hint` e il dettaglio dei toast, il budget resta **≈ 11 KB grezzi /
≈ 2,6 KB gzip**. In uscita: **2 659 byte grezzi** di `components.css` (i tredici blocchi `.dialog`,
`.nav-overlay`, `.nav-drawer`, contati).

**JavaScript — la cifra del round 1 era sbagliata e la ritiro.** «≈ 6,5 KB grezzi / ≈ 2,2 KB gzip»
non è credibile per stack, trappola e ritorno del fuoco, blocco dello scorrimento con ripristino,
gesto strozzato a rAF con soglia di velocità, coda di toast con timer e pause, più una palette che
raccoglie link a runtime, li raggruppa e fa navigazione da tastiera. Ancoraggio misurato:
`static/js/main.js` è **19 944 B grezzi → 5 309 B gzip** (rapporto 3,76) per un lavoro
materialmente minore. Stima ribasata, allineata alla revisione: **18–25 KB grezzi / 6–8 KB gzip**.

| Bundle | gzip misurato (`gzip -6`) |
|---|---:|
| `dist/chunks/chunk-P4EHGXV4.js` (Motion) | 26 143 B |
| `dist/shell.js` | 613 B |
| `dist/home.js` | 897 B |
| `main.js` | 5 309 B |
| **totale home, oggi** | **32 962 B = 32,19 KiB** |
| `dist/overlays.js` (stima alta) | + 8 192 B |
| in uscita da `main.js`: `initDialogs` 1 282 + `initNavigation` 5 013 + `initDropdowns` 1 491 = 7 786 B grezzi | − ≈ 2 070 B gzip (a 3,76) |
| **totale home, dopo** | **≈ 39,1 KB gz contro un budget di 45 → margine ≈ 5,9 KB** |

Il margine dichiarato nel round 1 (9,8 KB) non esisteva. **Ordine di taglio, se la palette lo
mangia**, dall'alto: (1) la raccolta runtime dei link della palette si riduce alle sole sezioni
dichiarate nel template — meno codice di scansione e raggruppamento, ~2 KB grezzi; (2)
`overlay.return` (l'alone sul richiamante) cade, è la voce più decorativa delle diciotto; (3) il
gesto di trascinamento cade — non è un mezzo di chiusura, è un'accelerazione, e le tre alternative
(chiusura, Escape, clic fuori) restano; (4) la palette esce dal bundle comune e diventa un modulo a
sé, caricato solo dalle pagine di portale, dove il pubblico non arriva. Sopra tutto: **la palette è
chrome di piattaforma e non deve mai pesare sulle pagine pubbliche.**

### 7.2 Paint e layout

Lo scrim è **un** livello a schermo intero con un gradiente **statico**: si anima solo la sua
`opacity` — zero layout, un solo strato composito. Il pannello anima solo `transform` e `opacity`.
La soglia anima solo `transform` (su `::before`, via `pseudoElement`). Il trascinamento scrive
**due proprietà personalizzate per frame** — `--ovl-drag` sul pannello (letta da `translate`) e
`--ovl-progress` sul `<dialog>` (ereditata dal `::backdrop`, verificato) — e non legge nulla:
l'altezza del pannello è misurata una volta al `pointerdown`. `will-change: opacity` si mette
all'apertura e si toglie alla fine dell'animazione. Gli overlay non contengono immagini: nessun
costo sul budget di 120 KB per viewport.

**Una nota sul blocco dello scorrimento.** `html[data-ovl-lock]{ overflow:hidden }` toglie la barra
di scorrimento classica, dove esiste, e sposta la pagina di ~15 px. Sull'ambiente misurato
(`window.innerWidth - documentElement.clientWidth === 0`) non c'è barra classica e non c'è
spostamento; dove c'è, la cura è `scrollbar-gutter: stable` **sull'`html`, sempre**, che è una
decisione della shell e non di questa superficie — la provo qui e la segnalo a `specs/shell.md`
invece di infilarla nel blocco di lock, dove riserverebbe la gronda solo mentre un overlay è aperto
e restringerebbe l'overlay stesso (misurato: il `<dialog>` passa da 390 a 375 px).

### 7.3 CSP

Il gesto scrive `element.style.setProperty("--ovl-drag", …)`, che è una proprietà inline e **non**
uno stile inline soggetto a `style-src 'self'`. Verificato al banco: `add_style_tag` di Playwright è
**rifiutato**, mentre `document.adoptedStyleSheets` e `element.style.setProperty` passano. Scritto
qui perché chi implementa, se incontrasse il primo errore, non vada a cercare un nonce o un
`<style>`: **non servono, e non sono ammessi.**

---

## 8. RISCHI

| Rischio | Perché farebbe sembrare il lavoro cheap | Guardia |
|---|---|---|
| Il bottom sheet legge «template di app mobile» | maniglia grigia, angoli arrotondati, pulsanti a pillola: catalogo shadcn/vaul | **La maniglia non esiste** (la testa è la zona di trascinamento) e **il raggio non esiste** (0, come DS §2 prescrive per i fogli). Resta un foglio a spigolo vivo sotto un filo di luce. Un test conta `border-radius` diversi da 0, 2, 6 e 999 nel foglio: attesi **zero**. |
| La soglia si propaga e in tre mesi ogni scheda ha un filetto teal | l'emendamento A1 apre una porta | La soglia è disegnata da **un solo selettore** e il test conta le occorrenze di `--ovl-threshold-line` nel CSS compilato (attese: 3). |
| `--terr-line-lt` è lo stesso esadecimale di `--accent` (`#0F6A72`) | un filetto teal in testa al pannello può leggersi come una barra d'accento | È la scelta del DS, non mia: i due token condividono il valore. La soglia non è mai adiacente a un testo, non sottolinea mai niente, non è mai cliccabile e compare su **ogni** overlay, quindi legge come chrome. Un test grep che cercasse l'esadecimale letterale sbaglierebbe bersaglio: il foglio non contiene colori letterali, solo token. |
| La palette legge «clone di Raycast» | glow, bordi luminosi, vetro, ricerca «magica» | Nessun glow, **nessun `backdrop-filter` in tutto il documento**, prefisso mono col riferimento reale del fascicolo, responsabile su ogni riga, nessuna azione governata eseguita dalla palette. |
| Lo scrim direzionale legge «effetto foto» | un gradiente troppo teatrale su un fascicolo amministrativo | L'escursione è dichiarata e misurata (§4.1) e il gradiente **non è mai animato**: si anima solo l'opacità dell'intero strato. Su un capitolo mezzanotte collassa a piatto da solo (ΔL\* 0,84). |
| I toast mangiano informazione legale | un messaggio che sparisce dopo 6 s e non esiste altrove | Solo `success`/`info` (`message.level < 30`); `error`/`warning` restano nel flusso; un toast non porta mai l'unica copia di un'informazione; nessuna scadenza con reduced-motion o oltre 120 caratteri. |
| Il trascinamento ruba lo scroll | il corpo scorre e lo sheet si chiude, o viceversa | Il gesto parte solo dalla testa, e mai da un controllo dentro la testa; `touch-action:none` sulla testa; il corpo ha `overscroll-behavior: contain`; l'alternativa a pulsante è sempre presente. |
| L'overlay diventa il posto dove si lavora | moduli lunghi in modale: il difetto n.1 dei back-office | Regola scritta in §4: mai più di tre campi, mai una tabella, mai un caricamento, mai un'azione del Rule Engine — da verificare in revisione, non in un test. |
| Un quinto ruolo d'ombra si infila per separare il pannello scuro | la palette sembra piatta contro il fondo velato | Sul mezzanotte la separazione è un **bordo** (`--ovl-edge`, 4,94 : 1 misurato), mai un'ombra: `grep box-shadow` continua a restituire quattro ruoli. |
| Qualcuno si fida di `--layer-toast` per mettere qualcosa sopra un overlay | il top layer non è uno z-index, e il round 1 ci è cascato | I due token restano, con il commento che dice contro che cosa sono stati misurati; `--layer-scrim` e `--layer-overlay` sono eliminati perché erano finzione. |

---

## 9. TEST — `tests/frontend/test_v3_overlay_tokens.py`

Quello che va bloccato, e con quale numero:

1. `.ovl` dichiara `max-inline-size: none` **e** `max-block-size: none`; a 390×844 il rettangolo del
   `<dialog>` aperto è `[0, 0, 390, 844]`.
2. Il foglio non contiene `backdrop-filter`, né `--layer-scrim`, né `--layer-overlay`, né
   `--radius-vestibule`.
3. `--ovl-panel-dark` risolve a `--mid-2`; `--ovl-edge` risolve a `--on-dark-3`.
4. Sul pannello `data-ovl="palette"` l'anello di focus calcolato è `rgb(127, 209, 216)`.
5. I rapporti della tabella di §4.1 ricalcolati dai token, con tolleranza 0,02.
6. `border-radius` diversi da 0 / 2 / 6 / 999 nel foglio: **zero**.
7. `--ovl-threshold-line` compare **tre** volte nel CSS compilato.
8. `grep box-shadow` sul CSS compilato restituisce solo i quattro ruoli.
9. Il numero di `cubic-bezier` distinti nel CSS compilato resta tre
   (`tests/frontend/test_motion_system.py`).
10. Ogni `transition` e ogni `@keyframes` del foglio sta dentro
    `@media (prefers-reduced-motion: no-preference)`.
11. Con `prefers-reduced-motion: reduce` nessun elemento dell'overlay ha `opacity: 0` o un
    `transform` diverso dall'identità.
12. `apps.cms.forbidden.scan()` su ogni pagina che monta un overlay, `alt` / `aria-label` /
    `title` / `.visually-hidden` compresi.
13. `templates/components/toasts.html`: un messaggio `SUCCESS` finisce nella `<ol class="ovl-toasts">`,
    un messaggio `ERROR` finisce nel `<div class="container messages">` con `role="alert"`, e
    nessuno dei due compare due volte.
14. `html.no-js`: il drawer è in flusso, `.nav-toggle` è `display:none`, e gli otto link di
    navigazione sono raggiungibili con `elementFromPoint`.
