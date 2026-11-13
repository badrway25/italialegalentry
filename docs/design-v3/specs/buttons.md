# SPEC V3 — BOTTONI E CALL TO ACTION · round 2

Superficie: `.btn` e tutte le varianti, su carta minerale, su mezzanotte e sul navy del forum ·
24 settembre 2026 · vincolante con `DESIGN_SYSTEM_V2.md` §10 e `MOTION_SYSTEM.md`.

**Metodo di questo round.** Ogni numero qui è stato **ricalcolato o rimisurato**, nessuno è
riportato dal round 1. Colore: luminanza relativa WCAG 2.x e L\* CIE calcolati in Python sui valori
reali dei token (`static/css/v2/tokens.css`), compositing `source-over` con arrotondamento a 8 bit
come Chromium. Geometria e cascata: Chromium headless di Playwright (`.venv`) a 1440×900, 1280×1400
e 390×844, `getComputedStyle` / `getBoundingClientRect` / `getBBox`. Pixel: campionamento dei PNG
renderizzati. Byte: `gzip -6` (il default, lo stesso del revisore) sui file reali. Paint e layout:
CDP `Tracing` categoria `disabled-by-default-devtools.timeline`, conteggio degli eventi `Layout` /
`Paint`, due esecuzioni identiche per ogni misura.

**Come il candidato è stato provato.** Il foglio candidato è stato **servito al posto di
`static/css/v3/buttons.css`** intercettando la richiesta (la CSP `style-src 'self'` rifiuta
`add_style_tag`, il che è una prima conferma che la CSP è reale), insieme a un `v2/hero.css` privo
delle righe 188–213 e a un `forum/forum.css` privo delle tre regole citate in §4.6 — cioè
esattamente il mondo che §4.6 descrive. **Nessun file del repository è stato modificato**: le
sorgenti di misura stanno in
`C:\Users\<user>\AppData\Local\Temp\claude\C--tmp-italylegalentry\2835bd7f-e7c1-4c7b-a100-aef407711009\scratchpad\`
(`colour.py`, `cand.css`, `from_spec.css`, `lab.html`, `m1.py`…`m13.py`, `shot_*.png`,
`lab_*.png`, `inv_current.png` / `inv_candidate.png`, `hero_actions_390.png`, `spec_lab_full.png`).

**La prova che questa spec è implementabile.** Il blocco CSS di §4.2 è stato **estratto dal file
markdown che state leggendo** (`re.search(r"```css…")`), servito al posto di
`static/css/v3/buttons.css` su un banco di 30 controlli su tre fondi, e sottoposto a 39 asserzioni
sui valori che la spec dichiara — altezze, riempimenti, inchiostri, bordi, tracking, padding della
freccia, ombre, disabled, larghezza costante del bottone asincrono, durata e sfalsamento del
misuratore, e la risoluzione di tutte e quattordici le variabili nuove. **39 su 39 passano**
(`m13.py`, `spec_lab_full.png`). Non è «il candidato che ho misurato»: è il testo che consegno.

**Prove su disco.** Le tre immagini citate nel round 1 non esistevano; ogni citazione è stata
ripuntata su file che esistono: `docs/design-v3/audit/home_1440_full.png`,
`home_390_full.png`, `forum_1440_full.png`, `orientation_1440_full.png`, `documents_1440_full.png`,
`case_file_1440_full.png`, `login_primary_accent.png`.

---

## 0. RICHIESTE DI EMENDAMENTO

Quattro, numerate, ciascuna con clausola, ragione e costo. Senza A1 e A2 la spec **non è
implementabile**: sono blocchi, non note.

### A1 — DESIGN_SYSTEM_V2 §2: un quinto ruolo d'ombra, «contatto», e la clausola «solo in hover»

**Clausole.** §2 «quattro ruoli, e nessun quinto» + tabella livello 2 «`--shadow-2` **solo in
hover**» + «`grep box-shadow` sul CSS compilato restituisce solo questi quattro ruoli».

**Che cosa chiedo.** Un quinto ruolo `--shadow-contact` (e la sua gemella scura
`--shadow-contact-dark`), **a riposo**, con vincoli scritti nel documento e in un test:

* solo su controlli, e **solo su varianti con riempimento opaco** (`--btn-primary/--secondary/--danger`
  e le loro forme su mezzanotte): mai sotto una superficie trasparente;
* offset y ≤ 1 px, blur ≤ 2 px, spread ≤ 0;
* **mai animata**, mai in transizione: cambia solo per sostituzione di variabile alla pressione;
* non è un'elevazione: non si somma mai a `--shadow-2/3/5` sullo stesso elemento.

**Ragione.** §2 costruisce la profondità «per scala di superfici, non per ombre», e il bottone
secondario su carta ne è la prova: `--min-2` su `--min-0` è **1.06:1** (calcolato). A quel delta la
scala di superficie da sola non esiste percettivamente; il bordo `--hairline-strong` dà il confine
(3.37:1) ma non dà **l'appoggio**. Un'ombra di contatto di 1 px non è elevazione: è la riga dove la
lastra tocca il foglio. È anche ciò che rende **fisica** la pressione, perché sparisce.

**Costo.** Il `grep box-shadow` passa da quattro valori a sei. Un ruolo in più da difendere in ogni
revisione futura. Se l'emendamento è respinto: si cancellano `--shadow-contact` e
`--shadow-contact-dark`, il bottone perde l'appoggio, la pressione resta portata da `translate` 1 px
e dall'inversione della luce interna (§4.3), e §4.1 perde una riga. La spec resta implementabile
**senza** questo emendamento; perde il dettaglio che la fa leggere come una lastra.

### A2 — MOTION_SYSTEM §1 e §4: un ciclo di stato transitorio per il misuratore d'attesa

**Clausole.** §1 «Nessun altro numero» (quattro durate + `--motion-draw` + `--motion-ambient` ≥ 20 s)
e §4 «un solo oggetto vivo per pagina … le pagine STANDARD, DENSE e LEGAL nessuno».

**Che cosa chiedo.** Che `button/busy-meter` sia ammesso come **indicatore di stato transitorio**,
con questi vincoli:

* la sua durata **non è un numero nuovo**: il ciclo è `calc(var(--motion-base) * 4)` = 960 ms e lo
  sfalsamento è `var(--motion-base)` = 240 ms. Ogni numero nel CSS è un token o un multiplo intero
  di un token — mai una costante. (Round 1 diceva 1200 ms e 400 ms: erano costanti inventate.)
* esiste **solo** fra l'inizio di una richiesta dell'utente e la sua fine, non può essercene più di
  uno per volta (un modulo, un submit), e non conta nel bilancio «un oggetto vivo per pagina»;
* **la clausola «in pausa fuori dal viewport» è onorata**, non aggirata: `button.js` osserva il
  bottone con un `IntersectionObserver` e mette `data-offscreen`, che porta
  `animation-play-state: paused`. Lo stato resta comunque annunciato dalla regione live, che non
  dipende dal moto.

**Ragione.** Le due fonti vincolanti si contraddicono già oggi, e la contraddizione non l'ho
introdotta io: §10 **prescrive** un indicatore di caricamento sul bottone («loading con spinner a
tratto + testo»), e uno spinner a tratto è un loop; §4 vieta i loop fuori da IMMERSIVE. Qualunque
bottone con stato di caricamento, con lo spinner o col misuratore, richiede questo emendamento.
L'alternativa onesta è nessun indicatore su nessun submit lento, che è peggio.

**Costo.** Il test che conta i loop deve conoscere l'eccezione, cioè diventa più complicato di
«uno». Rischio: che «indicatore di stato transitorio» diventi un grimaldello. Lo chiudo scrivendo
nell'emendamento che l'eccezione vale **solo** per un'animazione innescata da una richiesta
dell'utente, che muore con la risposta e che è in pausa fuori dal viewport.

### A3 — DESIGN_SYSTEM_V2 §10: «PRIMARY `--accent` pieno» diventa «pieno, con una luce verticale ΔL\* ≤ 3.0»

**Clausola.** §10, «PRIMARY (`--accent` pieno, testo `--min-0`, 48 px, raggio 2)».

**Che cosa chiedo.** Che «pieno» ammetta una **variazione di luminosità verticale** il cui valore
medio è il token e la cui ampiezza è limitata da un numero nel test:

```css
--btn-lit: linear-gradient(180deg, rgba(255,255,255,.03), rgba(10,21,28,.03));
```

applicata **sopra** `background-color: var(--btn-fill)`, per ogni riempimento opaco. Misurato (vedi
§4.1): ΔL\* fra i due estremi = **2.71** su `--accent`, **2.55** su `--accent-dark`, **2.37** su
`--err-700`, massimo **2.81** su `--accent-hover`; lo spostamento della luminosità media rispetto al
token è ≤ **0.45 L\***. Guardia proposta: **ΔL\* ≤ 3.0**. A .035 di alfa il massimo sale a 3.23 e il
test fallisce: la guardia morde davvero.

**Ragione.** È la differenza fra un rettangolo tinto e una lastra illuminata. ΔL\* ~2.7 su 48 px è
sotto la soglia in cui l'occhio legge «gradiente» e sopra quella in cui non legge nulla. Non è un
gradiente SaaS: non cambia tinta (la crominanza resta quella del token), non è caldo, non ha una
diagonale.

**Costo.** Una proprietà `background-image` in più su ogni bottone pieno. E un numero (.03) che
qualcuno può alzare: per questo la guardia è un test, non un commento (§8, rischio 1). Se
l'emendamento è respinto: si toglie `--btn-lighting` dalle tre varianti piene, il riempimento torna
piatto al valore del token, tutti i rapporti di §4.1 migliorano leggermente (la banda peggiore era
5.37:1, il piatto è 5.69:1) e non cambia nient'altro.

### A4 — DESIGN_SYSTEM_V2 §10: lo spinner a tratto diventa il misuratore a tacche della casa

**Clausola.** §10, «Stati: … loading con spinner a tratto + testo».

**Che cosa chiedo.** Che il segnale d'attesa sul bottone sia il **misuratore a tacche**, non uno
spinner. Testo e regione live restano esattamente come §10 li prescrive.

**Ragione.** Non è un capriccio: è **coerenza interna del documento vincolante**. §6 elenca fra gli
elementi della «grammatica della porta nella piattaforma» il **misuratore a tacche**; §9.1 usa il
«misuratore a cinque tacche» per l'avanzamento del fascicolo. Il sistema possiede già un segno per
«quanto manca», e quel segno non è uno spinner. Uno spinner a tratto è l'unico elemento di §10 che
viene da una libreria e non dal disegno di questa casa.

**Costo.** Un'incoerenza con l'abitudine: uno spinner è riconosciuto ovunque, tre tacche no.
Mitigazione: le tacche non compaiono mai da sole — la faccia «busy» porta **etichetta + tacche +
regione live** (§4.5), tre canali. Se l'emendamento è respinto: le tre `<span>` diventano un `<svg>`
con `stroke-dasharray` in rotazione, il resto di §4.5 non cambia di una riga, e A2 resta comunque
necessario perché uno spinner è anch'esso un loop.

### Deviazioni del round 1 che NON sono diventate emendamenti — sono state tolte

| Deviazione round 1 | Che cosa è stato fatto |
|---|---|
| §10 «testo `--min-0`» → `--btn-ink: var(--min-2)` | **Rimossa.** L'inchiostro del primario è `--min-0`. 5.69:1 sul pieno, **5.37:1** sulla banda più chiara della luce verticale, **5.93:1** su quella più scura. Tutto ≥ 4.5. |
| §2 livello 4 sostituito da un alone `0 0 0 2px var(--min-0)` | **Rimossa.** Il bottone **eredita** l'anello di sistema già implementato in `v2/shell.css:477-487` (2 px `--accent-ring` + alone 5 px al 30 %) e non ne inventa uno. §4.4 ricostruisce quell'anello sul bottone solo perché `.btn` dichiara `box-shadow`; i valori sono gli stessi due letterali di `shell.css`. |
| §2 «`--shadow-2` solo in hover» non nominata | **Dichiarata**, dentro A1, come seconda metà della stessa breccia. |
| `--shadow-2` a riposo | Mai usata: `--shadow-contact` non è `--shadow-2` e non si somma a nessuna elevazione. |

### Token nuovi che non sono deviazioni (dichiarati qui perché nessuno li chiami «non dichiarati»)

| Token | Valore | Perché non è una deviazione |
|---|---|---|
| `--accent-dark-hover` | `#a5e0e5` | È **il letterale che il build già serve** in `v2/hero.css:197`, a cui do un nome. §1.1 ha già quattro valori nella famiglia dell'accento (`--accent`, `--accent-hover`, `--accent-ring`, `--accent-wash`): la luminosità scura era l'unica senza il suo passo di hover. §1.3 r.1 limita il numero di **accenti**, non i passi di luminosità di uno solo. |
| `--err-hover` | `#9e2019` | §1.1 non ha un passo di hover per `--err-700`, e senza di esso DANGER non ha hover. Semantica invariata: rosso solo errore. |
| `--surface-disabled` | `#e3e2dd` | §10 prescrive «disabled a colore» e il sistema non ha il colore. |
| `--btn-edge-dark` | `rgba(214,226,228,.45)` | §1.1 ha `--hairline-dark-strong` a .28, che su `--mid-1` dà **2.20:1** — sotto 3:1 per un confine di componente. Non tocco il token esistente (lo usano altre superfici): ne aggiungo uno per i controlli. |
| `--shadow-nil` | `0 0 rgba(0,0,0,0)` | Non è un ruolo d'ombra: è il valore neutro che rende componibile una lista `box-shadow`. Vedi §4.2, nota sulla cascata — senza di esso `box-shadow: none, <ombra>` è **CSS invalido** e l'intera dichiarazione cade. |

---

## 0bis. RISPOSTA PUNTO PER PUNTO ALLA REVISIONE

| # | MUST-FIX | Esito | Dove |
|---|---|---|---|
| 1 | Scrivere la regola mezzanotte; riconciliare le tre liste di contesto | **FATTO** | §4.2 blocco «mezzanotte per contesto»; una sola lista `.chapter--dark, .on-inverse, .forum-cta`, ricavata da un censimento di 45 pagine (§4.0). Misurato col candidato servito e `hero.css:188-213` rimosso: primario `rgb(127,209,216)` su `rgb(14,27,35)` = **10.01:1**, secondario `rgb(27,47,58)` bordo `rgba(214,226,228,.45)` = **4.26:1** sul fondo. |
| 2 | Riconciliare gli esadecimali di §4.1 con le alfe di §4.2 | **FATTO** | §4.1: una sola alfa (.03) per tutti i riempimenti, tutti gli esadecimali ricalcolati e **riconfermati campionando i pixel del PNG** (primario carta: riga alta `#166E76`, riga bassa `#0F676F`, ΔL\* **2.71** misurato = 2.71 calcolato). |
| 3 | Guardie per `.btn--sm`, `.btn--lg`, `.btn--upper`, fallback dei `var()` | **FATTO** | §4.2. Nessuna variante dichiara più `min-block-size`/`padding`/`font-size`: dichiarano **solo variabili** che `.btn` legge, quindi non c'è gara di specificità. Misurato: sm **40 px**, lg **56 px / 17 px**, upper **13 px / 1.04 px di tracking / uppercase**, icon **44×44**. Ogni `var()` ha un fallback. |
| 4 | Definire o ritirare `.btn--ghost` e `.btn--link` | **FATTO** | §4.2: `.btn--link`/`.btn--text` sono alias di TERTIARY, `.btn--ghost` è alias di QUIET. Il suo conteggio è **confermato**: ricontato, 5 occorrenze di `btn--ghost` in 4 file e 4 di `btn--link` in 2, di cui una dentro un commento del mapper allauth → **8 usi in codice**, esattamente la sua cifra. Un file che la revisione non nominava e che va nella lista: `templates/dev/showcase.html`, la vetrina `/_design/`. |
| 5 | Sciogliere la tripla prenotazione di `::after`; il bersaglio ingrandito | **FATTO** | §4.2 e §6. `::after` non è più lo strato di pressione di nessuno (lo strato è stato **cancellato**, vedi §7): `::before` = hover sulle varianti con cornice e **linea d'ormeggio** su quelle senza; `::after` = **solo** il filetto a riposo delle varianti senza cornice. Il bersaglio ingrandito non è più uno pseudo — è l'elemento (`min-block-size`, `min-inline-size`, `padding-block`), quindi il problema di `pointer-events`/`z-index` non esiste. Misurato: TERTIARY **54.8 × 28**, INLINE **116.9 × 25.6**. |
| 6 | Scrivere le `transition` e il blocco `prefers-reduced-motion` | **FATTO** | §4.2, blocco `@media (prefers-reduced-motion: no-preference)`. Include la **neutralizzazione** obbligatoria delle transizioni che `components.css:33-38` e `:139-151` dichiarano fuori da quel blocco — senza di essa il moto ridotto non sarebbe implementato. Misurato con `reduced_motion="reduce"`: `transition` inerte su `.btn`, `::before`, `::after` e `.icon`; hover completo a 50 ms; freccia `translate: none`. |
| 7 | Portare `busy-meter` sui token o dichiarare la breccia §1 | **FATTO, entrambe le cose** | Ciclo = `calc(var(--motion-base) * 4)`, sfalsamento = `var(--motion-base)`; misurato in pagina: `animation: 0.96s linear infinite btn-meter`, `animation-delay: 0.24s`. La breccia residua (un multiplo di token; un loop su pagine non IMMERSIVE) è **A2**. «In pausa fuori dal viewport» è onorata, non scusata. |
| 8 | Dichiarare le due deviazioni §10 e la seconda metà della breccia §2 | **FATTO** | Spinner → misuratore = **A4**. Inchiostro `--min-2` → **rimosso**, si torna a `--min-0`. Seconda metà di §2 = dentro **A1**. |
| 9 | Riparare l'alone di focus | **FATTO** | §4.4: nessun alone codificato a mano. Misurato sui quattro fondi reali sotto un `.btn`: `--accent-ring` dà **3.70 / 3.44 / 4.26 / 3.71** su `--min-0` / `--min-1` / `--mid-1` / `--brand-navy` — passa ovunque; sui contesti scuri l'anello diventa `--accent-dark` (**10.01** su `--mid-1`, **8.73** su navy). Rettangolo bianco: sparito. |
| 10 | Sciogliere la contraddizione su `cases/detail.html:105`; cancellazione → DANGER | **FATTO** | §4.5: i cinque submit lenti sono nominati con file **e riga**. `cases/detail.html:105` **non** è uno di essi (è il submit per riga di una `<select>` in tabella); quello lento è `cases/detail.html:207`, «Enregistrer l'état». `documents/index.html:54` passa a `btn--danger btn--sm`; «Retirer cette autorisation» **resta** QUIET, con ragione scritta (§4.6). |
| 11 | Correggere §7 | **FATTO, con una cifra contestata** | §7. Conteggi: **confermati** i suoi, `.btn` 5 / 2 / 1 e controlli 10 / 6 / 5 su home / forum / orientamento (il suo selettore, che ho ricostruito, è «`<button>` + `<summary>` + `<a class="btn">` visibili»). Costo di `press`: **contesto**, vedi §7 — misuro **+657 B gzip**, non +728, e la cifra non si incassa perché `press` **non viene importato**. Inoltre una correzione che la revisione non aveva colto: il totale JS della home non è 27,6 KB ma **33 168 B gzip**, perché §7 round 1 dimenticava `main.js` (5 309 B) e `head.js` (206 B). |

**Segnali «cheap»:** 1 e 2 tolti (niente luce interna sui riempimenti chiari, niente ombra di
contatto sotto una superficie trasparente — §4.1); 3 risolto e mostrato (`shot_hero_actions.png`);
4 tolto (sette varianti scritte e misurate); 5 difeso con tre canali e token di sistema (§4.5);
6 tolto (`color-mix` sparito, il bordo è un token esistente); 7 tolto per la cancellazione e
**difeso** per la revoca di consenso (§4.6).

---

## 1. VERDETTO SULLO STATO ATTUALE — rimisurato il 24 settembre, dopo `a79fbb2`

Il round 1 descriveva un build che non esiste più: il commit `a79fbb2` ha già portato il primario su
carta sull'accento. §1.1 è quindi **storia**, non diagnosi. Quello che segue è il build di adesso,
misurato oggi.

**1.1 — Il primario su carta porta l'accento; il secondario porta ancora il navy del marchio.**
Misurato su 45 pagine pubbliche, 40 bottoni visibili: `.btn--primary` = `rgb(15,106,114)` ✔;
`.btn--secondary` = riempimento `rgba(0,0,0,0)`, **testo e bordo `rgb(15,37,71)` = `--brand-navy`**
su 11 dei 40. Superficie: **63 occorrenze** di `btn--secondary` nei template. Viola §1.3 r.4 («il
tricolore vive solo nel marchio») esattamente come il primario la violava.

**1.2 — L'hover del primario cambia il riempimento ma non il bordo.** Misurato con `locator.hover()`
prima/dopo: riempimento `rgb(15,106,114)` → `rgb(11,85,92)`, bordo **invariato** a `rgb(15,106,114)`.
Causa: `v3/buttons.css` (a79fbb2) definisce `--btn-border-hover`, ma **nessuna regola lo legge** —
`components.css:41-45` cambia solo `background` e `color`. Risultato: in hover il bordo è **più
chiaro** del riempimento, cioè una lastra illuminata al contrario.

**1.3 — Altezza 44 px, non 48** (§10 prescrive 48): `min-block-size: var(--control-height)` = 44 px
su tutti i `.btn` misurati, in tutte le viewport.

**1.4 — Nessun materiale.** Su tutti i 40 bottoni `box-shadow: none` e `background-image: none`:
riempimento piatto, bordo di 1 px **dello stesso colore del riempimento** sul primario, raggio 2 px.
(`docs/design-v3/audit/home_1440_full.png`.)

| # | Difetto | Prova misurata |
|---|---|---|
| 1.5 | **La pressione non è fisica** | `transform: translateY(1px)` con `transition … transform 180ms`: 1 px in 180 ms su una superficie priva di ombra di contatto. Misurato anche il costo: 12 pressioni su un bottone isolato = **24 Layout / 134 Paint**. |
| 1.6 | **La freccia avanza solo col mouse** | `.btn--arrow:hover .icon { translate: 3px 0 }` esiste, `:focus-visible` no: chi usa la tastiera non vede mai l'affordance. |
| 1.7 | **Disabled a opacità, in due posti** | `components.css:53-57` `{opacity:.55; pointer-events:none}` — §10 vieta letteralmente l'opacità; e **`apps/forum/static/forum/forum.css:145`** ripete `.btn.is-disabled { opacity:.55; cursor:not-allowed; pointer-events:none }` in un foglio d'app caricato **dopo** il sistema di disegno, quindi non sovrascrivibile a pari specificità. |
| 1.8 | **Tre `<span class="btn … is-disabled" aria-disabled="true">` senza CSS nel sistema** | `forum/partials/cta_row.html:17,22` e `virtual_forum_teaser.html:12` — quest'ultimo su un **testo bloccato** (`{% locked "p3.virtual_forum.button" %}`). Fuori dalle pagine del forum, `is-disabled` non ha **nessuna** regola: il controllo disabilitato è indistinguibile da uno attivo. |
| 1.9 | **Lo stato di caricamento non esiste** | `grep -rn "aria-busy\|btn--loading\|is-loading\|btn__spinner" static/ templates/ apps/` → **0 risultati**. |
| 1.10 | **Tre classi usate nei template e mai definite** | `.btn--text` (`documents/index.html:54`, **cancellazione di un documento**), `.btn--quiet` (`cases/detail.html:105`), `.btn--large` (`orientation/start.html:32`). Misurato su `/fr/orientation/`: `.btn--large` = **130.5 × 44**, cioè un `.btn` nudo. |
| 1.11 | **Il confine del secondario su mezzanotte sta a 2.20:1** | `--hairline-dark-strong` `rgba(214,226,228,.28)` su `--mid-1` compone `#465359` = **2.20:1** (calcolato). Lo stesso `.btn--secondary` nel forum ha bordo `rgb(183,195,196)` = `--on-dark-2` = **9.68:1**: due secondari con confini che differiscono di **4,4×**. |
| 1.12 | **Il forum non ha gerarchia e non ha spaziatura** | Misurato su `/fr/forum/`: due `.btn--secondary` affiancati (401.5 × 44 e 269.1 × 44), **nessun primario visibile**, etichette tutte maiuscole dal contenuto bloccato e `letter-spacing: normal`. Il fondo è `rgb(15,37,71)` = **`--brand-navy`**: un capitolo dipinto col navy del marchio (§1.3 r.4 — fuori dalla mia superficie, lo segnalo a `backgrounds`). |
| 1.13 | **Il foglio del sistema non vince la cascata come credeva** | `static/css/v3/buttons.css` è l'ultimo `@import` di `main.css`, ma i fogli d'app entrano da `{% block extra_head %}`, cioè **dopo**. Misurato: con il candidato servito, `.forum-cta .btn--secondary` restava `rgba(0,0,0,0)` con bordo `--on-dark-2` finché non ho rimosso `forum.css:144`. Le regole d'app che dipingono `.btn` sono tre, tutte in `forum.css` (144, 145, 182-185) — e l'intestazione di quel file dichiara: «Global tokens/components (`.btn`, …) are owned by the design system». |
| 1.15 | **«Secondario» e «discreto» sono lo stesso bottone su fondo scuro** | Misurato su un banco che riproduce `templates/dev/showcase.html:163-169`: `.btn--secondary.btn--inverse` e `.btn--ghost.btn--inverse` escono **identici** — riempimento `rgba(0,0,0,0)`, inchiostro `rgb(238,242,241)`, bordo `rgba(255,255,255,.55)`. `components.css:98` dichiara `.btn--inverse` dopo `.btn--ghost` a pari specificità e ne sovrascrive ogni variabile. La vetrina lo aveva già notato e ne aveva rimandato la decisione a questa spec (§4.0) |
| 1.14 | **Due controlli fuori sistema** | `.main-nav__toggle` e `.tide-toggle` hanno `transition: all`; `.tide-toggle` ha `border-radius: 999px`, una pillola, che §10 ammette solo per le pillole di stato. |

Oggi il bottone è un `<input type="submit">` colorato. Non c'è niente da rifinire.

## 2. UI-UX-PRO-MAX

| # | Query esatta (`--domain`) | Uscita (condensata) | Esito e ragione |
|---|---|---|---|
| 1 | `premium button hierarchy primary secondary tertiary states micro-interaction press physics` (`ux`) | Active States → «add pressed state», es. `active:scale-95`; Hover → «subtle visual change»; Disabled → «reduce opacity», es. `opacity-50 cursor-not-allowed` | **PARZIALE.** Accetto «feedback immediato alla pressione» — e in §5 lo porto all'estremo: la discesa è **senza transizione**. **Rifiuto `active:scale-95`**: 5 % su 48 px sposta il bordo di ~7 px, rimbalzo percettivo, overshoot vietato. **Rifiuto `opacity-50`**: è ciò che §10 proibisce. |
| 2 | `button loading state accessible live region announce aria-busy` (`ux`) | ARIA labels sugli icon-button; **«una sola regione live atomica con un messaggio contestuale, non un numero nudo»**; `<button aria-pressed>` mai un `div` cliccabile | **ACCETTATO in pieno.** Diventa §4.5: una `role="status"` per modulo, testo completo, mai «Chargement». |
| 3 e 7 | `government institutional CTA button style sober` · `government` · `call to action conversion primary button placement` | **0 risultati** su tutte e tre | **NESSUN DATO — e va detto.** Il database di stile non ha un registro «istituzionale». Il bias conservatore dello skill («government = avoid motion effects») non è sostenuto dai suoi stessi dati. |
| 4 | `button hover press animation timing easing scale` (`gsap`) | Subtle: 150–200 ms, `y:-1`, **«keep displacement under 2px»**; Standard: 200–300 ms, `y:-4`, `scale:1.02`, **`boxShadow` animata** | **ACCETTATO il tier Subtle** (≤ 2 px, solo transform/opacity): coincide con `--motion-fast` e con «≤ 2 px» di MOTION §2. **RIFIUTATO lo Standard**: `scale:1.02` e `boxShadow` animata violano due vincoli espliciti. |
| 5 | `disabled state contrast non-text minimum 3:1 focus ring visible` (`color`) | Palette per tipo di prodotto, `Muted Foreground: #94A3B8` ovunque, `Ring` sempre un colore dedicato | **RIFIUTATO il contenuto**: `#94A3B8` su carta chiara dà **2.31:1** (calcolato su `--min-0`). **Tengo il segnale trasversale**: l'anello di focus è un colore dedicato — che è già §1.3 e che qui diventa «ereditato dal sistema, non reinventato». |
| 6 | `uppercase label letter-spacing small caps button typography` (`typography`) | «ALL display/buttons/nav UPPERCASE, letterSpacing +2»; «Inter 600–800 per UI»; «12 px labels» | **PARZIALE.** **Accetto**: un'etichetta maiuscola *deve* essere spaziata — qui `.08em`, che a 13 px misura **1.04 px**. **Rifiuto** il peso 600–800 (§3.2 fissa 500) e l'uppercase come default. |

Su tre punti ho contraddetto lo skill con motivazione misurata, su due non aveva dati.

## 3. 21ST.DEV — candidati confrontati

| # | Componente · URL | Cosa è buono | Perché non va per noi | Cosa prendo |
|---|---|---|---|---|
| 1 | **cnippet Button** (Base UI) · `21st.dev/@cnippet-dev/components/cnippet-button` | `inset-shadow-[0_1px_white/16%]` a riposo che **si inverte** in `[:active]:inset-shadow-[0_1px_black/8%]`. `data-loading:text-transparent` + overlay assoluto → zero reflow. `transition-shadow`, non `all` | `disabled:opacity-64` · `disabled:pointer-events-none` · `rounded-lg` · nomi shadcn · React/Tailwind/CVA. E **il suo `after:min-h-11` non funzionerebbe da noi**: uno pseudo dietro il testo non allarga un bersaglio | **L'inversione della luce alla pressione** (§4.3), **il caricamento senza reflow** (§4.5). *Non* prendo lo pseudo-bersaglio |
| 2 | **Loading Button** · `21st.dev/@ddoemonn/components/loading-button` | Quattro facce in **una sola cella di griglia**: la larghezza è il massimo delle etichette. Regione live **fratello**. `aria-busy`+`aria-disabled` invece di `disabled`: resta focalizzabile. `touch-action: manipulation` | Crossfade con `filter: blur(3px)` — vietato · `whileTap={{y:1}}` come molla · `disabled:opacity-50` · focus come `box-shadow` colorata, che muore in `forced-colors` | **La griglia a cella unica** e **la regione live fratello** (§4.5). Misurato sul nostro markup: faccia idle 170.4 px, busy 130.5, done 157.6 → bottone **220.4 px in tutti gli stati** |
| 3 | **Minimal Buttons** · `21st.dev/@saurabh-2607/components/minimal-buttons` | Ombra di contatto **esterna a 1 px** + luce interna. Disabled **a colore**: `disabled:bg-neutral-100 disabled:text-neutral-400`, mai opacità | `border-t-2` di colore diverso dagli altri lati: su raggio 2 px legge come artefatto · `rounded-[13px]` · spinner **anteposto** all'etichetta → sposta il testo · `transition duration-200` su tutto | **L'ombra di contatto a 1 px** (A1) e **il disabled a colore** (§4.4). Rifiuto lo smusso — e rifiuto anche la loro luce interna dove il riempimento è chiaro (§4.1) |
| 4 | **micka_design Button** · `21st.dev/@micka_design/components/button` | È l'unico che dichiara la nostra stessa gerarchia: primary / secondary / **tertiary** / ghost, icone leading e trailing, icon-only, loading | «Fluid button»: il riempimento che scorre è un effetto di catalogo | **La conferma della tassonomia.** Nessun codice |
| 5 | **Gradient CTA Button** · `21st.dev/@mengto/components/gradient-cta` | Fa vedere che cosa *sembra* premium a prima vista: pillola, gradiente arancio, ombre inset stratificate | È **esattamente** ciò che la direttiva vieta. Su un dominio legale il gradiente caldo legge come una promozione | **Nulla: è il contro-esempio**, agli atti perché sia chiaro che è stato guardato e scartato |
| 6 | **Progress Button** · `21st.dev/@ruixen.ui/components/progress-button` | Barra di progresso dentro il bottone | Solo se il progresso è **reale**: §9.5 pretende «progresso reale» sull'upload. Una barra finta a durata fissa è una bugia su uno schermo legale | **Il principio**: se e solo se `upload.onprogress` dà un valore, il bottone lo mostra |

Nulla è installato: da ogni voce si estrae il **pattern** e lo si riscrive coi nostri token. Nessuna
dipendenza npm nuova.

---

## 4. LA PROPOSTA

### 4.0 File, e il contratto di cascata

**Il foglio esiste già.** `static/css/v3/buttons.css` è stato creato da `a79fbb2` con due sole regole
(lo scambio dell'accento sul primario) e **`main.css` lo importa già**, ultimo dopo `v2/voyage.css`.
Questa spec **sostituisce il contenuto di quel file**; l'effetto di `a79fbb2` è conservato per intero
(`.btn--primary` resta su `--accent`). `main.css` **non si tocca**: il round 1 contava una riga che
c'è già.

**Il foglio non vince da solo.** Misurato: i fogli d'app entrano da `{% block extra_head %}`, cioè
dopo `main.css`. Le regole d'app che dipingono `.btn` sono **tre, tutte in
`apps/forum/static/forum/forum.css`**, e §4.6 le rimuove. Perché non ricorro alla specificità per
vincerle: l'intestazione di quel file dichiara che `.btn` appartiene al sistema di disegno; la
riparazione giusta è togliere le regole, non sovrascriverle. La guardia permanente è il test G4 (§8).

**I contesti scuri sono tre, e li ho censiti, non indovinati.** Crawl di 45 pagine pubbliche,
40 bottoni visibili, colore di fondo composito risalendo gli antenati:

| Fondo sotto un `.btn` | Valore | Bottoni | Contenitore |
|---|---|---|---|
| `--min-0` | `rgb(244,243,240)` | 32 | pagine di contenuto, pannelli |
| `--min-1` | `rgb(236,235,230)` | 1 | `section--process` in home |
| `--mid-1` | `rgb(14,27,35)` | 2 | `.hero.chapter--dark` |
| `--brand-navy` | `rgb(15,37,71)` | 2 | `.forum-cta` |

Da qui, **una sola lista**, usata identica in §4.2 e §4.4: **`.chapter--dark`, `.on-inverse`,
`.forum-cta`**. `.on-inverse` copre `site-footer`, `utility-bar`, `hero--inverse` e
`cta-panel--inverse`; verificato leggendo `templates/components/hero.html:8` e `cta_panel.html:5`,
dove `on-inverse` e `btn--inverse` sono messe **dallo stesso `{% if variant == 'inverse' %}`** — per
questo `.btn--inverse` (4 occorrenze) non ha bisogno di nessuna regola in v3 e diventa inerte senza
essere rimossa dai template. `.platform-bar` **non esiste** in nessun template né foglio: il round 1
la citava a vuoto, è sparita.

**La vetrina `/_design/` pone una domanda a questa spec, e questa è la risposta.**
`templates/dev/showcase.html:155-170` (rotta solo con `DEBUG`) mette tre bottoni `btn--inverse` su
`.ds__dark`, che è `background: var(--mid-1)` ma **non porta né `.chapter--dark` né `.on-inverse`**,
e scrive nel testo: «Aucune page du site ne combine encore ces deux classes : le défaut est latent,
et c'est à la spécification des boutons de dire si le bouton discret existe sur fond sombre.»
Due risposte:

1. **Sì, il bottone discreto esiste su fondo scuro**, e §4.2 lo definisce:
   `--btn-ink: var(--accent-dark)` (10.01:1 su `--mid-1`), sfondo di hover `--mid-2`.
2. **Il difetto latente sparisce da solo.** Misurato sul build attuale: `.btn--secondary.btn--inverse`
   e `.btn--ghost.btn--inverse` sono **lo stesso bottone** — riempimento `rgba(0,0,0,0)`, inchiostro
   `rgb(238,242,241)`, bordo `rgba(255,255,255,.55)`, identici — perché `components.css:98` dichiara
   `.btn--inverse` dopo `.btn--ghost` a pari specificità e ne sovrascrive tutte le variabili. In v3
   non succede più: `.btn--inverse` imposta solo i nomi legacy (`--btn-bg/--btn-fg/--btn-border`) che
   **v3 non legge**. Misurato col candidato: primary `rgb(127,209,216)`, secondary `rgb(27,47,58)`,
   ghost trasparente con inchiostro `rgb(127,209,216)` — tre bottoni diversi, senza toccare i
   template.

Perché ciò accada, `.ds__dark` deve indossare `.on-inverse` (§4.6, una parola). Misurato **senza**:
la vetrina dipinge i tre bottoni per la carta sopra un fondo di mezzanotte — il secondario esce
`rgb(251,250,248)`, un foglio quasi bianco su `--mid-1`. `.on-inverse` è il marcatore che il sistema
già possiede per «sono su un fondo scuro»: la vetrina lo deve portare come lo portano il piè di
pagina e la barra istituzionale, invece di allungare la lista dei selettori di v3.

**Modulo JS**: `static/js/src/button.js`, **importato da `static/js/src/shell.js`** (che `base.html`
carica già su ogni pagina). Nessun `<script>` nuovo, nessuna richiesta nuova, nessuna riga in
`base.html` — il round 1 ne chiedeva una. **Nessuna view Django, nessun contesto, nessun contratto
dati toccato.**

### 4.1 Token e colori — tutti calcolati in questo round

```css
/* geometria */
--btn-h: 48px; --btn-h-sm: 40px; --btn-h-lg: 56px; --btn-h-icon: 44px;   /* §10: 48, e 44 per ICON */
--btn-pad-sm: var(--s-5);  /* 20 */
--btn-pad-md: var(--s-6);  /* 24 — la misura che il build ha già */
--btn-pad-lg: var(--s-8);  /* 32 */
/* colore */
--accent-dark-hover: #a5e0e5;            /* il letterale di hero.css:197, ora un token */
--err-hover:         #9e2019;
--surface-disabled:  #e3e2dd;
--btn-edge-dark:     rgba(214,226,228,.45);
/* materiale */
--shadow-contact:      0 1px 0 rgba(10,21,28,.10), 0 1px 2px -1px rgba(10,21,28,.16);
--shadow-contact-dark: 0 1px 0 rgba(10,21,28,.20), 0 1px 2px -1px rgba(10,21,28,.32); /* §2: nel buio le opacità raddoppiano */
--shadow-nil:          0 0 rgba(0,0,0,0);
--btn-lit: linear-gradient(180deg, rgba(255,255,255,.03), rgba(10,21,28,.03));
/* focus — gli stessi due letterali di v2/shell.css:479 e :486, non valori nuovi */
--focus-halo:      rgba(29,138,147,.3);
--focus-halo-dark: rgba(127,209,216,.3);
```

**Niente `--accent-press`, niente `--err-press`.** Il round 1 li definiva e non li usava. La pressione
non cambia colore: cambia posizione, luce e appoggio (§4.3). Due token in meno.

**Niente `letter-spacing: .005em`.** Misurato in Chromium: a 15 px vale **0.075 px**. Non produce
«aria fra le aste»: non produce niente. Il tracking del bottone è **0** (`--track-normal` di §3.2),
tranne `.btn--upper`, dove `.08em` misura **1.20 px a 15 px e 1.04 px a 13 px**.

**Niente `color-mix(in oklab, …)`.** Il bordo del primario è `--accent-hover` (`#0B555C`), un token
che esiste: **1.35:1 contro il riempimento** (lo spessore della lastra) e **7.67:1 contro la carta**
(un confine di componente ampiamente sopra 3:1). Per confronto, il `color-mix` del round 1 risolveva
a `#084D53` — un valore che la spec non dichiarava e che nessuno poteva verificare.

#### La luce verticale (A3) — stop calcolati e poi campionati sul PNG

Una sola alfa, `.03`, bianco in alto e `--mid-0` in basso, applicata sopra ogni riempimento opaco.

| Riempimento | Valore | Stop alto | Stop basso | ΔL\* | Media L\* vs token |
|---|---|---|---|---|---|
| `--accent` | `#0F6A72` | `#166E76` | `#0F676F` | **2.71** | +0.22 |
| `--accent-hover` | `#0B555C` | `#125A61` | `#0B535A` | **2.81** | +0.43 |
| `--accent-dark` | `#7FD1D8` | `#83D2D9` | `#7BCBD2` | **2.55** | −0.45 |
| `--accent-dark-hover` | `#A5E0E5` | `#A8E1E6` | `#A0DADF` | **2.54** | −0.44 |
| `--err-700` | `#B3261E` | `#B52D25` | `#AE251E` | **2.37** | +0.14 |
| `--err-hover` | `#9E2019` | `#A12720` | `#9A2019` | **2.31** | +0.15 |

**Verifica indipendente sul pixel.** Screenshot del primario di `/fr/` (367 × 49 px), colonna
centrale: y = 2 → `#166E76` (L\* 42.20), y = 46 → `#0F676F` (L\* 39.49), **ΔL\* = 2.71**. Identico al
calcolo. Sul primario mezzanotte: y = 2 → `#83D2D9`, y = 46 → `#7CCBD3`, ΔL\* = 2.47 (le righe
campionate sono un pixel dentro il bordo; il calcolo sugli stop dà 2.55). Guardia: **ΔL\* ≤ 3.0**.

#### La tabella normativa dei colori (WCAG 2.x, calcolati)

| Variante · fondo | Riempimento | Etichetta | Peggior rapporto etichetta | Bordo | Bordo vs fondo |
|---|---|---|---|---|---|
| PRIMARY · carta | `--accent` + luce | `--min-0` | **5.37:1** (banda alta; 5.69 al centro, 5.93 in basso) | `--accent-hover` | **7.67:1** (e 1.35:1 contro il riempimento) |
| PRIMARY · mezzanotte | `--accent-dark` + luce | `--mid-1` | **9.43:1** (banda bassa; 10.01 al centro) | `--accent-dark` (nessun bordo: la lastra è chiara, il fondo è il bordo) | riempimento vs fondo **10.01:1** su `--mid-1`, **8.73:1** su navy |
| SECONDARY · carta | `--min-2` piatto | `--ink` | **15.56:1** | `--hairline-strong` | **3.37:1** (3.59:1 contro il riempimento) |
| SECONDARY · mezzanotte | `--mid-3` piatto | `--on-dark` | **12.29:1** | `--btn-edge-dark`, composito `#6F8086` | **4.26:1** su `--mid-1`, **3.71:1** su navy, 3.37:1 contro il riempimento |
| DANGER · carta | `--err-700` + luce | `--min-0` | **5.62:1** (banda alta) | `--err-hover` | **7.08:1** |
| TERTIARY / LINK / TEXT · carta | nessuno | `--accent` | **5.69:1** | filetto `currentColor` al 70 % → `#8DB5B7` | **3.15:1** su `--min-0`, **3.02:1** su `--min-1` |
| TERTIARY · mezzanotte | nessuno | `--accent-dark` | **10.01:1** | filetto al 70 % → `#416D74` | **5.51:1** |
| QUIET / GHOST · carta | nessuno (hover `--min-1`) | `--ink-2` | **6.46:1** a riposo, **6.00:1** in hover | nessuno | — |
| INLINE · carta | nessuno | `--accent`, Fira Mono 13 px, `.08em` | **5.69:1** | come TERTIARY | **3.15:1** |
| DISABLED · carta | `--surface-disabled` | `--ink-3` | **4.73:1** | `--hairline` | 1.37:1 (il confine si spegne: è il segnale) |
| DISABLED · mezzanotte | `--mid-3` | `--on-dark-3` | **5.10:1** | `--hairline-dark` → `#354852` | 1.45:1 |

Il filetto delle varianti senza cornice sta al **70 %**, non al 45 % del round 1: a .45 componeva
**2.01:1** su `--min-0`, sotto la soglia di 3:1 per un elemento non testuale. A .70 misura
**3.15:1 / 3.02:1**; in hover sale a 1 (5.69:1) e la linea d'ormeggio si traccia sopra.

#### Delta di hover (riempimento contro riempimento) — oggi sono 1.08–1.20, qui

| Variante | Riposo → hover | Delta |
|---|---|---|
| PRIMARY carta | `--accent` → `--accent-hover` | **1.35:1** |
| PRIMARY mezzanotte | `--accent-dark` → `--accent-dark-hover` | **1.20:1** |
| SECONDARY carta | `--min-2` → `--min-1` | 1.14:1 *(più il bordo che non cambia e la luce che resta: il secondario non deve gridare)* |
| SECONDARY mezzanotte | `--mid-3` → `--mid-4` | 1.16:1 |
| DANGER | `--err-700` → `--err-hover` | **1.20:1** |
| QUIET / GHOST | trasparente → `--min-1` (carta) / `--mid-2` (scuro) | 1.08:1 / 1.10:1 *(da niente a qualcosa: il delta percettivo è l'apparizione di una superficie, non il suo contrasto)* |

### 4.2 Il foglio — `static/css/v3/buttons.css`

Un bottone è una **lastra poggiata sul foglio**: `.btn` porta riempimento, luce verticale, bordo più
scuro del riempimento e ombra di contatto; **un solo pseudo** dipinge lo stato di hover, sotto
`isolation: isolate`, e questo permette di animare **solo `opacity`**. Raggio 2 px ovunque, mai una
pillola.

**Nota di cascata, obbligatoria da leggere prima di scrivere una riga.** `v3/buttons.css` arriva dopo
`components.css` a pari specificità, quindi cattura ogni proprietà che ridichiara. Il round 1 lo
faceva senza accorgersene e schiacciava `.btn--sm`, `.btn--lg` e `.btn--upper`. Qui la regola è una:
**`.btn` dichiara le proprietà, le varianti dichiarano solo variabili.** Non c'è più nessuna gara di
specificità da vincere fra varianti. Restano da **neutralizzare esplicitamente** sei dichiarazioni di
`components.css` che nessuna variabile può raggiungere; sono scritte sotto, ciascuna con la sua
ragione e il suo numero di riga.

**Nota sulla lista `box-shadow`.** `box-shadow: var(--btn-light, none), var(--btn-contact, none)` —
la forma del round 1 — è **CSS invalido** ogni volta che una delle due variabili non è impostata,
perché `none` non è un membro valido di una lista separata da virgole: l'intera dichiarazione cade e
l'ombra sparisce. L'ho scoperto misurando: il primario e il secondario **su mezzanotte** venivano
fuori con `box-shadow: none` pur avendo `--btn-contact` impostata. Per questo esiste `--shadow-nil`,
e per questo ogni variante dichiara **una sola** variabile con la lista completa.

**E perché le varianti senza riempimento dichiarano `box-shadow: none` a parte.** Se lasciassi che
ereditino `var(--btn-shadow, var(--shadow-nil))`, il valore calcolato sarebbe
`rgba(0,0,0,0) 0px 0px 0px 0px` — invisibile, ma un revisore che misura
`getComputedStyle().boxShadow !== "none"` leggerebbe «ombra», ed è **esattamente** il rilievo che la
revisione ha mosso al round 1 («un'ombra sotto il nulla»). Le quattro famiglie senza riempimento
(`--quiet/--ghost`, le varianti in riga, `--icon`, e ogni stato disabled) dichiarano quindi
`box-shadow: none` in proprio. Misurato sul banco di 30 controlli: l'ombra di contatto compare su
**tutti e soli** i riempimenti opachi (primary, secondary, danger e le loro forme su mezzanotte e su
navy); su ghost, quiet, tertiary, link, text, inline, icon e su **ogni** disabled il valore calcolato
è letteralmente `none`.

```css
/* ============================================================================
   static/css/v3/buttons.css — sostituisce il contenuto creato da a79fbb2.
   ========================================================================== */
:root {
  --btn-h: 48px; --btn-h-sm: 40px; --btn-h-lg: 56px; --btn-h-icon: 44px;
  --btn-pad-sm: var(--s-5); --btn-pad-md: var(--s-6); --btn-pad-lg: var(--s-8);
  --accent-dark-hover: #a5e0e5;
  --err-hover: #9e2019;
  --surface-disabled: #e3e2dd;
  --btn-edge-dark: rgba(214, 226, 228, 0.45);
  --shadow-contact: 0 1px 0 rgba(10, 21, 28, 0.1), 0 1px 2px -1px rgba(10, 21, 28, 0.16);
  --shadow-contact-dark: 0 1px 0 rgba(10, 21, 28, 0.2), 0 1px 2px -1px rgba(10, 21, 28, 0.32);
  --shadow-nil: 0 0 rgba(0, 0, 0, 0);
  --btn-lit: linear-gradient(180deg, rgba(255, 255, 255, 0.03), rgba(10, 21, 28, 0.03));
  --focus-halo: rgba(29, 138, 147, 0.3);        /* = v2/shell.css:479 */
  --focus-halo-dark: rgba(127, 209, 216, 0.3);  /* = v2/shell.css:486 */
}
[dir="rtl"] { --dir: -1; --origin-inline: right; }

/* ---- 1. La lastra --------------------------------------------------------- */
.btn {
  position: relative; isolation: isolate;
  display: inline-flex; align-items: center; justify-content: center; gap: var(--s-3);
  min-block-size: var(--btn-box-h, var(--btn-h));
  padding-block: 0;
  padding-inline: var(--btn-pad, var(--btn-pad-md))
                  var(--btn-pad-end, var(--btn-pad, var(--btn-pad-md)));
  font-family: var(--f-sans); font-size: var(--btn-type, var(--t-ui));
  font-weight: 500; line-height: 1.2;
  letter-spacing: var(--btn-track, 0);
  text-align: center; text-decoration: none;
  color: var(--btn-ink, var(--accent));
  background-color: var(--btn-fill, transparent);
  background-image: var(--btn-lighting, none);
  border: 1px solid var(--btn-edge, transparent);
  border-radius: var(--radius-control);
  box-shadow: var(--btn-shadow, var(--shadow-nil));
  cursor: pointer; touch-action: manipulation;
  transition: none;   /* MOTION §3: fuori dal blocco di moto NIENTE transisce */
  -webkit-tap-highlight-color: transparent;
}

/* ---- 2. Neutralizzazioni di components.css (ognuna con la sua riga) -------- */
/* :41-45 ridipinge l'hover con la scorciatoia `background`, che cancellerebbe la
   luce verticale e farebbe saltare il colore. v3 dipinge l'hover su ::before. */
.btn:hover, .btn:focus-visible, .btn:active {
  background-color: var(--btn-fill, transparent);
  background-image: var(--btn-lighting, none);
  color: var(--btn-ink, var(--accent));
  border-color: var(--btn-edge, transparent);
}
/* :47-49 preme con `transform`; v3 preme con `translate`. Sono due proprietà
   diverse: senza questa riga la corsa sarebbe di 2 px. */
.btn:active { transform: none; translate: 0 1px; box-shadow: var(--btn-shadow-press, var(--shadow-nil)); }
/* :53-57 (e apps/forum/.../forum.css:145) spengono il disabled a opacità e gli
   tolgono il puntatore, cioè la spiegazione. §10 lo vieta. */
.btn:disabled, .btn[aria-disabled="true"], .btn.is-disabled { opacity: 1; pointer-events: auto; }
/* :139-151 dichiarano la transizione e i due `translate` della freccia fuori da
   qualunque media query: sotto «riduci movimento» la freccia si sposterebbe. */
.btn--arrow .icon { transition: none; }
.btn--arrow:hover .icon,
[dir="rtl"] .btn--arrow:hover .icon { translate: none; }

/* ---- 3. Lo strato di hover ------------------------------------------------ */
.btn::before {
  content: ""; position: absolute; inset: -1px; z-index: -1; border-radius: inherit;
  opacity: 0; pointer-events: none;
  background-color: var(--btn-fill-hover, transparent);
}
@media (hover: hover) { .btn:hover::before { opacity: 1 } }
.btn:focus-visible::before { opacity: 1 }   /* il focus PRODUCE lo stato di hover */

/* ---- 5. Varianti con riempimento ------------------------------------------ */
.btn--primary {
  --btn-fill: var(--accent); --btn-ink: var(--min-0); --btn-edge: var(--accent-hover);
  --btn-lighting: var(--btn-lit);
  --btn-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.14), var(--shadow-contact);
  --btn-shadow-press: inset 0 1px 2px rgba(10, 21, 28, 0.18);   /* la luce si inverte */
  --btn-fill-hover: var(--accent-hover);
}
.btn--secondary {
  --btn-fill: var(--min-2); --btn-ink: var(--ink); --btn-edge: var(--hairline-strong);
  --btn-shadow: var(--shadow-contact);
  --btn-shadow-press: inset 0 1px 2px rgba(10, 21, 28, 0.1);
  --btn-fill-hover: var(--min-1);
}
.btn--danger {
  --btn-fill: var(--err-700); --btn-ink: var(--min-0); --btn-edge: var(--err-hover);
  --btn-lighting: var(--btn-lit);
  --btn-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.14), var(--shadow-contact);
  --btn-shadow-press: inset 0 1px 2px rgba(10, 21, 28, 0.18);
  --btn-fill-hover: var(--err-hover);
}

/* ---- 6. Senza cornice, con la scatola (48 px) ----------------------------- */
.btn--quiet, .btn--ghost {
  --btn-fill: transparent; --btn-edge: transparent; --btn-ink: var(--ink-2);
  --btn-fill-hover: var(--min-1);
  box-shadow: none;   /* nessuna ombra sotto una superficie che non c'è */
}

/* ---- 7. Senza cornice, in riga ------------------------------------------- */
.btn--tertiary, .btn--link, .btn--text, .btn--inline {
  --btn-fill: transparent; --btn-edge: transparent; --btn-ink: var(--accent);
  --btn-box-h: 24px; --btn-pad: 0;
  min-inline-size: 24px; padding-block: var(--s-1);
  text-decoration: none;   /* il filetto è ::after, non una sottolineatura di sistema */
  box-shadow: none;
}
.btn--inline { --btn-type: var(--t-folio); --btn-track: var(--track-folio); font-family: var(--f-mono); }
/* ::after = il filetto a riposo. ::before = la linea d'ormeggio che si traccia.
   Nessun elemento porta due lavori sullo stesso pseudo. */
.btn--tertiary::after, .btn--link::after, .btn--text::after, .btn--inline::after {
  content: ""; position: absolute; inset: auto 0 2px 0; block-size: 1px;
  background: currentColor; opacity: 0.7; z-index: 0; pointer-events: none;
}
.btn--tertiary::before, .btn--link::before, .btn--text::before, .btn--inline::before {
  inset: auto 0 2px 0; block-size: 1px; background: currentColor; opacity: 1; z-index: 0;
  transform: scaleX(0); transform-origin: var(--origin-inline, left);
}
.btn--tertiary:hover::before, .btn--link:hover::before, .btn--text:hover::before, .btn--inline:hover::before,
.btn--tertiary:focus-visible::before, .btn--link:focus-visible::before,
.btn--text:focus-visible::before, .btn--inline:focus-visible::before { transform: scaleX(1); }

/* ---- 8. Misure ----------------------------------------------------------- */
.btn--sm    { --btn-box-h: var(--btn-h-sm); --btn-pad: var(--btn-pad-sm); }
.btn--lg    { --btn-box-h: var(--btn-h-lg); --btn-pad: var(--btn-pad-lg); --btn-type: var(--t-body); }
.btn--large { --btn-box-h: var(--btn-h-lg); --btn-pad: var(--btn-pad-lg); --btn-type: var(--t-body); }
            /* alias temporaneo: cade con la riga di orientation/start.html in §4.6 */
.btn--block { inline-size: 100%; }
.btn--icon  {
  --btn-box-h: var(--btn-h-icon); --btn-pad: 0; inline-size: var(--btn-h-icon);
  --btn-fill: transparent; --btn-edge: transparent; --btn-ink: var(--ink-2);
  --btn-fill-hover: var(--min-1);
  box-shadow: none;   /* ICON è un livello di §10, non si combina con --primary */
}
.btn--upper { --btn-track: 0.08em; --btn-type: var(--t-folio); text-transform: uppercase; }
/* misurato: l'inchiostro della freccia sta in un riquadro di 12.5 × 10 px dentro
   un box di 20 × 20, con 4.17 px di vuoto sul lato d'uscita. Il padding finale
   scende di 4 px: 24 ottici da un lato, 24.17 dall'altro. */
.btn--arrow { --btn-pad-end: calc(var(--btn-pad, var(--btn-pad-md)) - 4px); }

/* ---- 9. Mezzanotte per CONTESTO, non per classe --------------------------- */
.chapter--dark .btn--primary, .on-inverse .btn--primary, .forum-cta .btn--primary {
  --btn-fill: var(--accent-dark); --btn-ink: var(--mid-1); --btn-edge: var(--accent-dark);
  --btn-shadow: var(--shadow-contact-dark);
  --btn-shadow-press: inset 0 1px 2px rgba(10, 21, 28, 0.24);
  --btn-fill-hover: var(--accent-dark-hover);
}
.chapter--dark .btn--secondary, .on-inverse .btn--secondary, .forum-cta .btn--secondary {
  --btn-fill: var(--mid-3); --btn-ink: var(--on-dark); --btn-edge: var(--btn-edge-dark);
  --btn-shadow: var(--shadow-contact-dark);
  --btn-shadow-press: inset 0 1px 2px rgba(10, 21, 28, 0.24);
  --btn-fill-hover: var(--mid-4);
}
.chapter--dark .btn--tertiary, .on-inverse .btn--tertiary, .forum-cta .btn--tertiary,
.chapter--dark .btn--link, .on-inverse .btn--link, .forum-cta .btn--link,
.chapter--dark .btn--quiet, .on-inverse .btn--quiet, .forum-cta .btn--quiet,
.chapter--dark .btn--ghost, .on-inverse .btn--ghost, .forum-cta .btn--ghost {
  --btn-ink: var(--accent-dark); --btn-fill-hover: var(--mid-2);
}
.chapter--dark .btn--icon, .on-inverse .btn--icon, .forum-cta .btn--icon {
  --btn-ink: var(--on-dark-2); --btn-fill-hover: var(--mid-2);
}
.chapter--dark .btn, .on-inverse .btn, .forum-cta .btn {
  --btn-ring: var(--accent-dark); --btn-halo: var(--focus-halo-dark);
}

/* ---- 10. Disabled: a colore E a forma, mai a opacità ---------------------- */
.btn:disabled, .btn[aria-disabled="true"], .btn.is-disabled {
  --btn-fill: var(--surface-disabled); --btn-ink: var(--ink-3); --btn-edge: var(--hairline);
  --btn-shadow: var(--shadow-nil); --btn-lighting: none; --btn-fill-hover: transparent;
  box-shadow: none; cursor: not-allowed;
}
.btn--tertiary:disabled, .btn--link:disabled, .btn--text:disabled, .btn--inline:disabled,
.btn--tertiary[aria-disabled="true"], .btn--link[aria-disabled="true"],
.btn--text[aria-disabled="true"], .btn--inline[aria-disabled="true"],
.btn--quiet:disabled, .btn--ghost:disabled,
.btn--quiet[aria-disabled="true"], .btn--ghost[aria-disabled="true"] {
  --btn-fill: transparent; --btn-edge: transparent; --btn-ink: var(--ink-3);
}
.btn:disabled::before, .btn:disabled::after,
.btn[aria-disabled="true"]::before, .btn[aria-disabled="true"]::after,
.btn.is-disabled::before, .btn.is-disabled::after { display: none; }
.chapter--dark .btn:disabled, .on-inverse .btn:disabled, .forum-cta .btn:disabled,
.chapter--dark .btn[aria-disabled="true"], .on-inverse .btn[aria-disabled="true"],
.forum-cta .btn[aria-disabled="true"],
.chapter--dark .btn.is-disabled, .on-inverse .btn.is-disabled, .forum-cta .btn.is-disabled {
  --btn-fill: var(--mid-3); --btn-ink: var(--on-dark-3); --btn-edge: var(--hairline-dark);
}

/* ---- 11. Focus: l'anello del sistema, ricostruito perché .btn dichiara box-shadow.
   Sta QUI, dopo ogni `box-shadow: none` di sopra, perché anche un bottone senza ombra
   e anche un bottone `aria-disabled` devono poter mostrare l'anello. `--btn-shadow`
   resta sempre una LISTA valida (mai `none`), altrimenti la composizione qui sotto cade. */
.btn:focus-visible {
  outline: 2px solid var(--btn-ring, var(--accent-ring));
  outline-offset: 2px;
  box-shadow: var(--btn-shadow, var(--shadow-nil)),
              0 0 0 5px var(--btn-halo, var(--focus-halo));
}

/* ---- 12. Caricamento (§4.5) ---------------------------------------------- */
.btn__faces { display: grid; place-items: center; }
.btn__face {
  grid-area: 1 / 1; display: inline-flex; align-items: center; gap: var(--s-3);
  white-space: nowrap;
}
.btn__face:not([data-face="idle"]) { opacity: 0 }
.btn[aria-busy="true"] .btn__face[data-face="idle"] { opacity: 0 }
.btn[aria-busy="true"] .btn__face[data-face="busy"] { opacity: 1 }
.btn[data-state="done"] .btn__face[data-face="idle"] { opacity: 0 }
.btn[data-state="done"] .btn__face[data-face="done"] { opacity: 1 }
.btn__meter { display: inline-flex; gap: 4px; align-items: center; }
.btn__meter > span { inline-size: 4px; block-size: 4px; background: currentColor; opacity: .25 }
/* lo stato ridotto È questo: tre tacche ferme a tre livelli, leggibili senza moto */
.btn[aria-busy="true"] .btn__meter > span:nth-child(1) { opacity: 1 }
.btn[aria-busy="true"] .btn__meter > span:nth-child(2) { opacity: .6 }
.btn[aria-busy="true"] .btn__meter > span:nth-child(3) { opacity: .3 }

/* ---- 13. Moto — tutto e solo qui dentro (MOTION §3) ---------------------- */
@media (prefers-reduced-motion: no-preference) {
  /* la pressione non ha latenza: scende nel frame dell'evento e risale in 120 ms */
  .btn { transition: translate var(--motion-instant) var(--ease-out); }
  .btn:active { transition: none; }
  /* hover: 180 in (--ease-out), 120 out (--ease-in) — l'asimmetria è nelle due regole */
  .btn::before { transition: opacity var(--motion-instant) var(--ease-in),
                             transform var(--motion-instant) var(--ease-in); }
  .btn:hover::before, .btn:focus-visible::before {
    transition-duration: var(--motion-fast); transition-timing-function: var(--ease-out); }
  /* linea d'ormeggio: 240 in, 120 out */
  .btn--tertiary::before, .btn--link::before, .btn--text::before, .btn--inline::before {
    transition: transform var(--motion-instant) var(--ease-in); }
  .btn--tertiary:hover::before, .btn--link:hover::before, .btn--text:hover::before,
  .btn--inline:hover::before, .btn--tertiary:focus-visible::before, .btn--link:focus-visible::before,
  .btn--text:focus-visible::before, .btn--inline:focus-visible::before {
    transition-duration: var(--motion-base); transition-timing-function: var(--ease-out); }
  /* freccia: 240, e ORA anche su :focus-visible (§1.6) */
  .btn--arrow .icon { transition: translate var(--motion-base) var(--ease-out); }
  .btn--arrow:hover .icon, .btn--arrow:focus-visible .icon,
  [dir="rtl"] .btn--arrow:hover .icon, [dir="rtl"] .btn--arrow:focus-visible .icon {
    translate: calc(3px * var(--dir, 1)) 0; }
  /* facce: 180 --ease-standard, opacity + 3 px */
  .btn__face { transition: opacity var(--motion-fast) var(--ease-standard),
                           translate var(--motion-fast) var(--ease-standard); }
  .btn__face:not([data-face="idle"]) { translate: 0 3px }
  .btn[aria-busy="true"] .btn__face[data-face="busy"],
  .btn[data-state="done"] .btn__face[data-face="done"] { translate: 0 0 }
  .btn[aria-busy="true"] .btn__face[data-face="idle"] { translate: 0 -3px }
  /* misuratore (A2): ciclo 4 × --motion-base, sfalsamento --motion-base. Nessuna costante. */
  @keyframes btn-meter { 0% { opacity: .25 } 25% { opacity: 1 } 60% { opacity: 1 } 100% { opacity: .25 } }
  .btn[aria-busy="true"] .btn__meter > span {
    animation: btn-meter calc(var(--motion-base) * 4) linear infinite; }
  .btn[aria-busy="true"] .btn__meter > span:nth-child(2) { animation-delay: var(--motion-base) }
  .btn[aria-busy="true"] .btn__meter > span:nth-child(3) { animation-delay: calc(var(--motion-base) * 2) }
  .btn[data-offscreen] .btn__meter > span { animation-play-state: paused }
}

/* ---- 14. Contrasto forzato ----------------------------------------------- */
@media (forced-colors: active) {
  .btn { background-color: ButtonFace; color: ButtonText; border-color: ButtonText;
         background-image: none; box-shadow: none; }
  .btn::before, .btn::after { display: none; }   /* luce e filetti sono rumore qui */
  .btn--tertiary, .btn--link, .btn--text, .btn--inline, .btn--quiet, .btn--ghost {
    background-color: Canvas; color: LinkText; border-color: transparent;
    text-decoration: underline; }                /* il filetto torna come sottolineatura */
  .btn:disabled, .btn[aria-disabled="true"], .btn.is-disabled {
    color: GrayText; border-color: GrayText; }
  .btn:focus-visible { outline: 2px solid Highlight; }
}

/* ---- 15. Arabo (§3.2) ----------------------------------------------------- */
:lang(ar) .btn { --btn-track: 0; text-transform: none; }
:lang(ar) .btn--primary, :lang(ar) .btn--secondary, :lang(ar) .btn--danger,
:lang(ar) .btn--quiet, :lang(ar) .btn--ghost { min-inline-size: 120px; }
```

**Misurato col foglio servito** (1280 × 1400, banco di 24 controlli, `lab.html`):

| Variante | Misura | Riempimento | Inchiostro | Bordo |
|---|---|---|---|---|
| `btn--primary` | 103.2 × **48** | `rgb(15,106,114)` + gradiente | `rgb(244,243,240)` | 1 px `rgb(11,85,92)` |
| `btn--primary btn--arrow` | 174.2 × 48, padding **24 / 20** | idem | idem | idem |
| `btn--secondary` | 121.7 × 48 | `rgb(251,250,248)` | `rgb(21,34,42)` | 1 px `rgb(122,134,139)` |
| `btn--danger` | 98.4 × 48 | `rgb(179,38,30)` + gradiente | `rgb(244,243,240)` | 1 px `rgb(158,32,25)` |
| `btn--quiet` / `btn--ghost` | 87.1 × 48 / 89.8 × 48 | trasparente | `rgb(74,90,98)` | trasparente |
| `btn--tertiary` / `--link` / `--text` | 54.8 / 30.5 / 30.3 × **28** | trasparente | `rgb(15,106,114)` | filetto 1 px |
| `btn--inline` | 116.9 × 25.6, **Fira Mono 13 px, ls 1.04 px** | trasparente | `rgb(15,106,114)` | filetto 1 px |
| `btn--icon` | **44 × 44** | trasparente | `rgb(74,90,98)` = `--ink-2` | trasparente |
| `btn--sm` / `btn--lg` | **40** / **56**, fs 15 / **17**, padding 20 / 32 | — | — | — |
| `btn--upper` | 48, **fs 13 px, ls 1.04 px, uppercase** | — | — | — |
| `btn--block` | **1200** × 48 | — | — | — |
| `:disabled` / `[aria-disabled]` / `.is-disabled` (anche su `<span>`) | 48, `cursor: not-allowed`, **`pointer-events: auto`, `opacity: 1`** | `rgb(227,226,221)` | `rgb(85,100,107)` | 1 px `rgb(211,210,204)` |
| mezzanotte: primary / secondary / disabled | 48 | `rgb(127,209,216)` / `rgb(27,47,58)` / `rgb(27,47,58)` | `rgb(14,27,35)` / `rgb(238,242,241)` / `rgb(143,160,163)` | — / `rgba(214,226,228,.45)` / `rgba(214,226,228,.14)` |
| navy (`.forum-cta`): primary / secondary | 48 | idem mezzanotte | idem | idem |
| **ombra di contatto** | presente su primary, secondary, danger e le loro forme scure; `box-shadow` calcolata **letteralmente `none`** su ghost, quiet, tertiary, link, text, inline, icon e su ogni disabled | — | — | — |

`.btn--icon` misura **44 × 44**, non 44 × 48: il round 1 fissava `inline-size` senza toccare
l'altezza. Oggi la classe ha **zero occorrenze** nei template — è il contratto di §10 scritto perché
esista quando servirà, non codice morto per una superficie viva.

### 4.3 Stati — tabella normativa

| Stato | PRIMARY | SECONDARY | TERTIARY / LINK / TEXT | QUIET / GHOST | DANGER | ICON | INLINE |
|---|---|---|---|---|---|---|---|
| **rest** | `--accent` + luce verticale, luce interna .14, contatto | `--min-2`, bordo 3.37:1, contatto, **nessuna luce interna** | `--accent` + filetto al 70 % | `--ink-2`, nessuna cornice, scatola 48 px | `--err-700` **pieno** + luce | glifo `--ink-2`, 44 × 44 | mono 13 px `--accent` + filetto |
| **hover** | `--accent-hover` (Δ 1.35:1), freccia +3 px | `--min-1` (il bordo non cambia) | filetto al 100 % **+ linea d'ormeggio tracciata** | fondo `--min-1` | `--err-hover` (Δ 1.20:1) | fondo `--min-1` | come TERTIARY |
| **focus-visible** | **identico all'hover** + anello 2 px + varco 2 px + alone 5 px al 30 % | idem | idem | idem | idem | idem | idem |
| **active** | `translate: 0 1px`, **contatto azzerato**, la luce interna **si inverte** in `inset 0 1px 2px rgba(10,21,28,.18)` | idem con .10 | filetto al 100 %, `translate: 0 1px` | fondo `--min-1`, `translate: 0 1px` | come PRIMARY | idem | idem |
| **disabled** | `--surface-disabled`, `--ink-3`, bordo `--hairline`, **nessuna luce, nessun contatto, nessun gradiente** | idem | trasparente, `--ink-3`, filetto via | trasparente, `--ink-3` | idem, **mai rosso** | glifo `--ink-3` | `--ink-3` |
| **loading** | faccia «busy» + misuratore, `aria-busy` | idem | n/d | n/d | idem | glifo → misuratore | n/d |
| **error** | faccia «error» + glifo `warning` + etichetta | idem | n/d | n/d | idem | n/d | n/d |

**Il focus produce lo stato di hover**: oggi tastiera e mouse vedono due bottoni diversi (§1.6).
**Il disabled cambia forma, non solo colore**: perde luce, gradiente e contatto — da lastra torna
rettangolo. Colore *e* forma, mai il colore da solo (WCAG 1.4.1).
**La pressione cambia tre cose insieme**: posizione (1 px), appoggio (il contatto sparisce) e verso
della luce (da `inset` chiaro a `inset` scuro). Nessuna delle tre è un'animazione di `box-shadow`:
sono sostituzioni di variabile, istantanee.

**La luce interna esiste solo dove il riempimento è scuro.** Regola scritta, non gusto: `--btn-shadow`
porta una `inset 0 1px 0 rgba(255,255,255,.14)` **solo** se L\* del riempimento ≤ 50. `--accent`
L\* 40.6 ✔, `--err-700` L\* 39.7 ✔, `--accent-dark` L\* 79.1 ✘, `--min-2` L\* 98.3 ✘. È la risposta al
rilievo «smusso macOS 2009»: su un fondo quasi bianco una luce bianca non è luce, è uno smusso, e il
round 1 ne metteva una al **90 %**. Qui il secondario prende il materiale da dove §2 dice che deve
venire — dalla scala di superfici (`--min-2` sopra `--min-0`) più il bordo — e da un'unica riga di
contatto.

### 4.4 Anello di focus, e disabled

**L'anello non è nuovo: è quello del sistema.** `v2/shell.css:477-487` implementa già §2 livello 4
(2 px `--accent-ring`, offset 2 px, alone 5 px al 30 %, e la variante `--accent-dark` per
`.on-inverse`/`.chapter--dark`). Il bottone lo **eredita**. La sola ragione per cui §4.2 lo riscrive
è che `.btn` dichiara `box-shadow` a pari specificità e lo cancellerebbe: la regola `.btn:focus-visible`
ricompone la **stessa** lista — ombra della lastra, poi alone — e aggiunge `.forum-cta` alla lista dei
contesti scuri, che `shell.css` non conosce.

Misurato sui quattro fondi reali censiti in §4.0:

| Fondo | `--accent-ring` | `--accent-dark` | Anello applicato | Rapporto |
|---|---|---|---|---|
| `--min-0` | 3.70:1 | 1.58:1 | `--accent-ring` | **3.70:1** |
| `--min-1` | 3.44:1 | 1.46:1 | `--accent-ring` | **3.44:1** |
| `--mid-1` | 4.26:1 | 10.01:1 | `--accent-dark` | **10.01:1** |
| `--brand-navy` | 3.71:1 | 8.73:1 | `--accent-dark` | **8.73:1** |

Verifica in pagina col candidato servito: primario su carta →
`outline: rgb(29,138,147) solid 2px`, `outline-offset: 2px`, `box-shadow: … , rgba(29,138,147,.3) 0 0 0 5px`;
primario nell'hero → `outline: rgb(127,209,216) solid 2px`, alone `rgba(127,209,216,.3)`. **Nessun
rettangolo bianco**, su nessun fondo. (Round 1: `0 0 0 2px var(--min-0)` dava un rettangolo a
15.77:1 sull'hero.)

Anello → **varco di 2 px del colore del fondo** (è il fondo, non un colore dipinto: `outline-offset`
scopre il fondo reale) → lastra. Tre bande. **Senza transizione**: MOTION §2 famiglia FOCUS dice
«identico, istantaneo», e un anello che arriva in ritardo è un difetto.

**Disabled.** Si usa **`aria-disabled="true"`, non `disabled`**, ovunque ci sia una ragione da
comunicare: il controllo resta focalizzabile e annunciabile, `button.js` annulla l'attivazione in
fase di **cattura** (click e `Enter`/`Space`), `pointer-events: none` **sparisce** dal foglio,
`cursor: not-allowed`. Dove la ragione esiste (regola del Rule Engine, tappa non raggiunta) accanto
al bottone va uno `<span id="…">` referenziato da `aria-describedby` con la frase **già presente**
nel contenuto bloccato: nessun testo nuovo, nessuna formulazione nuova.

`.is-disabled` (tre `<span>` nei template, uno su testo bloccato) riceve **le stesse** dichiarazioni:
oggi fuori dal forum non ne ha nessuna, e dentro il forum ne ha una che §10 vieta.

### 4.5 Caricamento — markup e i cinque submit

```django
{# templates/components/button_async.html — NUOVO #}
<button type="submit" class="btn btn--primary" data-async
        data-busy="{{ busy_label }}" data-done="{{ done_label }}"><span class="btn__faces">
  <span class="btn__face" data-face="idle">{{ label }}{% svg_icon "arrow" "icon icon--flip-rtl" %}</span>
  <span class="btn__face" data-face="busy" aria-hidden="true">{{ busy_label }}<span class="btn__meter"
    aria-hidden="true"><span></span><span></span><span></span></span></span>
  <span class="btn__face" data-face="done" aria-hidden="true">{{ done_label }}{% svg_icon "check" "icon" %}</span>
</span></button>
<span class="btn__status visually-hidden" role="status"></span>
```

Tutte le facce nella **stessa cella di griglia**: la larghezza intrinseca è il massimo delle tre
etichette e **non cambia mai**. Misurato sul markup reale: faccia idle **170.4 px**, busy **130.5**,
done **157.6**; il contenitore `.btn__faces` misura **170.4** e il bottone **220.4 px sia con
`aria-busy="false"` sia con `aria-busy="true"`**. Zero reflow, provato, non promesso.

La regione live è un **fratello**, non il bottone: annuncia «Envoi en cours» poi «Demande envoyée»,
mai «Chargement». Il misuratore è `aria-hidden`: lo stato lo dicono l'etichetta e la regione live.

**La faccia «busy» compare solo dopo 160 ms d'attesa** (soglia in `button.js`): sotto quella soglia
il bottone non cambia mai faccia. Evitare il lampeggio conta più dell'animazione.

Dove il progresso è **reale** (upload, §9.5) le tre tacche diventano una barra indicizzata a
`upload.onprogress`. **Mai una barra finta.**

#### I cinque submit lenti — file e riga, senza ambiguità

| # | File · riga | Azione | Perché è lento |
|---|---|---|---|
| 1 | `templates/orientation/_step.html:37` | «Continuer» | valutazione del Rule Engine a ogni passo |
| 2 | `templates/orientation/result.html:97` | «Enregistrer dans mon espace» | scrittura del percorso nello spazio dell'account |
| 3 | `templates/documents/upload.html:18` e `templates/documents/requirement_detail.html:154` | «Déposer» | trasferimento del file (**progresso reale**, §9.5) |
| 4 | `templates/cases/detail.html:207` | «Enregistrer l'état» | transizione di stato del fascicolo + audit |
| 5 | `templates/forum/partials/registration_form.html:26` | iscrizione al forum | scrittura + notifica |

**Non** sono in questa lista, e la revisione aveva ragione a chiedere che fosse detto:
`cases/detail.html:105` («Mettre à jour» per riga, con una `<select>` accanto — è un POST breve, e
resta `btn--quiet`) e `portal/messages.html:31` («Marquer comme lue», `btn--link btn--sm`). Il round 1
diceva «cambio stato del fascicolo» e «messaggi» senza numeri di riga, ed erano due cose diverse.

#### `static/js/src/button.js` — e perché è piccolo

```js
const BUSY_THRESHOLD = 160;                 // ms: sotto questa soglia la faccia non cambia mai
export function initButtons(root = document) {
  root.addEventListener("click", cancelDisabled, true);      // fase di CATTURA
  root.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") cancelDisabled(e);
  }, true);
  for (const btn of root.querySelectorAll(".btn[data-async]")) {
    const form = btn.form || btn.closest("form");
    if (form) form.addEventListener("submit", onSubmit);
    watchViewport(btn);                     // IntersectionObserver -> [data-offscreen] (A2)
  }
}
```

Il modulo **non importa nulla**: né da `./motion.js`, né da `motion`. Ogni animazione del bottone è
CSS, dentro `@media (prefers-reduced-motion: no-preference)`; il JS mette e toglie attributi. È anche
la ragione per cui il moto ridotto è corretto per costruzione: non c'è un secondo percorso da tenere
allineato.

**`press` di Motion non viene importato.** Il round 1 lo chiedeva per dare `:active` agli
`<a class="btn">` attivati da tastiera. Due ragioni per non farlo, la seconda misurata: (a) `Enter`
su un `<a>` naviga immediatamente — un feedback di 120 ms su una pagina che sta andandosene non è
feedback, è rumore; il mouse riceve `:active` nativamente anche sugli anchor; (b) sonda esbuild
(0.28.2, motion 13.4.1, `--minify --target=es2022`, `gzip -6`), con esattamente i quattro nomi che
`shell.js` e `home.js` importano oggi: **23 179 → 23 836 B gzip, +657 B**. Contesto sulla revisione:
lei misura +728 B; la differenza è l'insieme di import della sonda (la sua passava da `./motion.js`,
includendo `spring` e `withMotion`). Le due misure concordano su ciò che conta — il costo non è zero,
come diceva il round 1 — e divergono di 71 B sul valore. **Nessuna delle due si incassa**, perché
`press` non entra.

### 4.6 File toccati

| File | Modifica | Righe |
|---|---|---|
| `static/css/v3/buttons.css` | **sostituito** (esiste da `a79fbb2`; l'effetto di quel commit è conservato) | ~350 |
| `static/css/main.css` | **nessuna**: l'`@import` c'è già | 0 |
| `static/css/v2/hero.css` | rimozione di `188-213` (`.hero .btn--primary/--secondary` e i loro `:hover`/`:focus-visible`), assorbite dal contesto | −26 |
| `apps/forum/static/forum/forum.css` | rimozione di `144` (`.forum-cta .btn--secondary`), `145` (`.btn.is-disabled` a opacità — §10 lo vieta) e `182-185` (`:focus-visible` locale: misurato, dà un anello `--on-dark` e un alone **navy** di 2 px, cioè un rettangolo del colore del fondo). L'intestazione del file dichiara già che `.btn` appartiene al sistema di disegno | −6 |
| `templates/documents/index.html:54` | `btn--text` → **`btn--danger btn--sm`** | 1 |
| `templates/orientation/start.html:32` | `btn--large` → `btn--lg` (l'alias in §4.2 cade nello stesso commit) | 1 |
| `templates/forum/partials/cta_row.html:12,15,17,20,22` · `templates/pages/home/_reserved.html:15` | aggiunta di `btn--upper` sulle sei etichette che arrivano **già maiuscole** dal contenuto bloccato (`p2.forum.registration.button_*`, `d.button`) | 6 |
| `templates/dev/showcase.html:163` | `class="ds__dark"` → `class="ds__dark on-inverse"` (pagina di sola `DEBUG`; senza questa parola la vetrina dipinge i bottoni della carta su un fondo di mezzanotte — §4.0) | 1 |
| `templates/components/button_async.html` | **nuovo** partial | +8 |
| i cinque `{% include %}` di §4.5 | sostituzione del `<button>` col partial | 6 |
| `static/js/src/button.js` + una riga di `import` in `static/js/src/shell.js` | nuovo modulo, nessun `<script>` nuovo | +75 / +2 |
| `templates/base.html` | **nessuna** | 0 |

`btn--primary`, `btn--secondary`, `btn--arrow`, `btn--sm`, `btn--lg`, `btn--block`, `btn--upper`,
`btn--icon`, `btn--inverse`, `btn--ghost`, `btn--link` e `btn--quiet` conservano nome e semantica:
**nessuna delle loro 188 occorrenze nei template si tocca** (ricontate una per una: primary 73, secondary 65, sm 12, arrow 11, inverse 9, lg 6, ghost 5, link 4, block 1, upper 1, quiet 1, icon 0). Le occorrenze rinominate sono **due**: `btn--text` e `btn--large`. Cambia la resa: ogni `.btn` passa da
44 a 48 px, `.btn--sm` da 36 a 40, `.btn--lg` da 52 a 56. Verificato a 1440 e a 390 su home, forum e
orientamento: nessun contenitore si rompe; a 390 le due CTA dell'hero misurano **350 × 48 entrambe**
(oggi 54 e 44: la pila dentellata di §1.11 sparisce — `hero_actions_390.png`). L'etichetta del
primario va su due righe dentro la scatola da 48: è la lunghezza della stringa, non un difetto del
controllo, e lo segnalo a chi possiede il testo.

**`documents/index.html:54` «Supprimer» diventa DANGER**, e la revisione ha ragione: è una
cancellazione **irreversibile e senza conferma**, e il round 1 la vestiva da link di testo, cioè più
leggera di «Mettre à jour» accanto. La direttiva vieta di aggiungere una conferma (cambierebbe il
workflow), quindi il peso deve stare tutto sul bottone.

**«Retirer cette autorisation» (`selection/disclosures.html:101`) resta QUIET, e non diventa DANGER.**
Non è un'incoerenza con la riga sopra, è la distinzione che la riga sopra rende necessaria:
cancellare un documento distrugge un dato; **revocare un consenso è un diritto**, e il GDPR chiede che
ritirarlo sia facile quanto darlo. Vestire una revoca di consenso da azione pericolosa è un pattern
oscuro. Stessa forma, stessa classe, per `selection/process.html:225` («Mettre à jour», il gemello di
`cases/detail.html:105`): `ghost` e `quiet` erano due nomi per lo stesso ruolo e ora sono la stessa
regola.

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` §6

| Nome | Funzione | Innesco | Durata | Curva | Proprietà | Stato ridotto | Budget misurato |
|---|---|---|---|---|---|---|---|
| `button/press` | **FEEDBACK** | `:active` (mouse e touch su `<button>` e `<a>`) | **0 in discesa**, `--motion-instant` (120 ms) in risalita | `--ease-out` in risalita | `translate: 0 1px`; `--btn-shadow` → `--btn-shadow-press` per **sostituzione**, mai in transizione | nessuna traslazione; la luce si inverte comunque, istantanea: il feedback resta, il moto no | 12 pressioni su un bottone isolato: **12 Layout / 168 Paint**; il build attuale, stessa prova: **24 Layout / 134 Paint** |
| `button/hover-surface` | **FEEDBACK** | `pointerenter` sotto `@media (hover: hover)` **e `:focus-visible`**, stessa regola | 180 ms in entrata · 120 ms in uscita | `--ease-out` / `--ease-in` | `opacity 0→1` su `.btn::before`; nessuna transizione di `background-color` né di `box-shadow` | identico e istantaneo (MOTION §2: l'hover non è moto essenziale) | 12 cicli: **0 Layout / 96 Paint** — **identico** al build attuale (96) |
| `button/arrow-advance` | **ORIENTAMENTO** | `:hover` **e `:focus-visible`** su `.btn--arrow` | `--motion-base` (240 ms) | `--ease-out` | `translate: calc(3px * var(--dir,1)) 0` sull'`.icon` | freccia ferma a 0: l'affordance la portano l'etichetta e `icon--flip-rtl` | 20 × 20 px, compositore |
| `button/mooring-line` | **ORIENTAMENTO** | `:hover`/`:focus-visible` su `.btn--tertiary`, `--link`, `--text`, `--inline` | 240 ms in entrata · 120 ms in uscita | `--ease-out` / `--ease-in` | `transform: scaleX(0→1)` su **`::before`**, `transform-origin: var(--origin-inline, left)` | il filetto di `::after` resta al 70 % (3.15:1): lo stato è leggibile senza la linea | 1 px d'altezza, un nodo |
| `button/face-swap` | **CAUSALITÀ** | `submit` → `aria-busy` dopo 160 ms; risposta → `data-state` | `--motion-fast` (180 ms) | `--ease-standard` | `opacity` + `translate: 0 3px` sulle `.btn__face` | scambio immediato, nessuna traslazione; la regione live annuncia comunque | tre nodi in una cella di griglia ⇒ **220.4 px in ogni stato, misurato** |
| `button/busy-meter` | **STATO** | presenza di `[aria-busy="true"]` | `calc(var(--motion-base) * 4)` = **960 ms**, sfalsamento `var(--motion-base)` = **240 ms** | `linear` (MOTION §1 lo ammette **dentro** i loop) | `opacity` di tre `<span>` da 4 × 4 px | **fermo**: le tre tacche restano a 100 / 60 / 30 % — lo stato resta leggibile senza moto | tre nodi; in pausa fuori dal viewport via `IntersectionObserver` |

`transform-origin: inline-start` **non esiste** in CSS — il round 1 lo scriveva e non sarebbe
compilato. La proprietà accetta `left`/`right`/lunghezze; l'RTL si fa con una variabile
(`[dir="rtl"] { --origin-inline: right }`). Verificato in pagina con `dir="rtl"`: l'origine del
filetto di `.btn--tertiary` (largo 54.8 px) risulta `52.8px 0.5px`, cioè il bordo d'uscita in lettura
araba.

**Stato ridotto, verificato** (`reduced_motion="reduce"`): `transition` inerte su `.btn`, su entrambi
gli pseudo e sull'icona; l'hover è **completo a 50 ms** (`::before` a `opacity: 1`); la freccia resta
a `translate: none`; nessun elemento resta a `opacity: 0`. La pagina è identica nei contenuti.

---

## 6. ACCESSIBILITÀ E RTL

| Punto | Che cosa cambia | Misura |
|---|---|---|
| **Bersaglio (WCAG 2.5.8 AA, 24 px)** | 48 px su tutte le varianti con cornice e su QUIET/GHOST; **44 px** su `.btn--icon` (§10). Le varianti in riga (`--tertiary`, `--link`, `--text`, `--inline`) allargano il bersaglio **sull'elemento stesso** — `min-block-size: 24px`, `min-inline-size: 24px`, `padding-block: var(--s-1)` — non con uno pseudo. Il round 1 usava uno pseudo che ereditava `pointer-events: none` e `z-index: -1` dalla regola base: non poteva allargare niente | misurato: TERTIARY **54.8 × 28**, LINK **30.5 × 28**, TEXT **30.3 × 28**, INLINE **116.9 × 25.6**, ICON **44 × 44** |
| **Focus** | Anello 2 px, offset 2 px, alone 5 px al 30 % — quello del sistema, per contesto | 3.70 / 3.44 / 10.01 / 8.73 sui quattro fondi reali |
| **Colore mai da solo** | disabled = colore + perdita di gradiente, luce e contatto; error = colore + glifo `warning` + testo; busy = etichetta + tacche + regione live; press = posizione + appoggio + verso della luce; hover del tertiary = filetto 70 → 100 % + linea tracciata | — |
| **`forced-colors: active`** | Riempimenti a `ButtonFace`/`ButtonText`, bordo `1px solid ButtonText` su ogni variante con cornice, pseudo a `display: none`, il filetto torna come `text-decoration: underline` sulle varianti in riga, disabled a `GrayText`, focus con `Highlight` | §4.2 blocco 14 · verifica umana in HUMAN_QA |
| **Disabled annunciabile** | `aria-disabled="true"` + `aria-describedby` verso la ragione **già scritta** nel contenuto bloccato; resta nell'ordine di tabulazione; `button.js` annulla click **e** `Enter`/`Space` in fase di cattura | misurato: `pointer-events: auto`, `opacity: 1`, `cursor: not-allowed` su `:disabled`, `[aria-disabled]` e `.is-disabled`, anche su `<span>` |
| **Caricamento** | `aria-busy="true"` sul bottone, `role="status"` su un **fratello**, misuratore `aria-hidden`, attivazione annullata finché dura, **il focus non si sposta** | — |
| **RTL** | Solo proprietà logiche (`padding-inline`, `min-inline-size`, `inset-inline`); la freccia usa `--dir: -1`; il filetto usa `--origin-inline: right` | misurato in `dir="rtl"`: `.btn--arrow` padding **24 / 20** (specchiato correttamente), freccia in hover **`translate: -3px`**, origine del filetto al bordo d'uscita |
| **`:lang(ar)`** | `min-inline-size: 120px` (§3.2) **solo** sulle varianti con cornice, `letter-spacing: 0` su **ogni** variante compresi `.btn--upper` e `.btn--inline`, `text-transform: none` | misurato: primary/secondary/danger/quiet/ghost **120 px**; tertiary/link/text/inline **24 px**; icon `auto` → 44; `letter-spacing: normal` ovunque |

**HUMAN_QA_REQUIRED**: (a) NVDA/VoiceOver sulla sequenza idle → busy → done, per escludere il doppio
annuncio; (b) contrasto forzato Windows su primario, secondario, tertiary e disabled; (c) resa in AR
del gruppo etichetta+freccia col padding compensato; (d) il misuratore con «riduci movimento» su un
upload lento reale; (e) giudizio d'occhio sulla luce verticale a ΔL\* 2.71 su uno schermo non
calibrato — se legge come «gradiente», l'alfa scende a .02 (ΔL\* 1.93, ricalcolato) e il test con lei.

---

## 7. PRESTAZIONI — tutto rimisurato

**Byte CSS.** Il blocco di §4.2, **così come è stampato, commenti compresi**, misura
**15 744 B grezzi / 4 369 B gzip** (misurato estraendolo da questo file e scrivendolo in binario —
non «circa»); senza i commenti, **12 061 / 2 936**. Il progetto serve il CSS non minificato, quindi
il numero che conta è il primo. Sostituisce l'attuale `v3/buttons.css`
(**2 793 / 1 325**), quindi **+12 951 grezzi / +3 044 gzip**; meno
`hero.css:188-213` (**624 / 256**) e le tre regole di `forum.css` (**~330 / ~150**) fa
**≈ +2 638 B gzip** subito. Alla fase 9 la sezione 1 di `components.css` (righe 7-160, **3 627 /
960**) diventa morta e cade: **≈ +1 678 B gzip** a regime — pagato
in commenti che spiegano perché ogni riga esiste, e che sono la ragione per cui il round 2 esiste.

**Byte JS.** `button.js` importa zero: il chunk condiviso **non cambia**. Misura esatta, stessa
compilazione per i due casi (esbuild 0.28.2, `splitting`, `minify`, es2022, `gzip -6`):
`shell.js` senza il modulo **1 084 B grezzi / 584 gzip**, con il modulo **2 225 / 1 000**, cioè
**+1 141 grezzi / +416 gzip**, e **nessuna richiesta HTTP nuova**.

**Bilancio della home — e la correzione al round 1.** Misurato sui file `dist` committati, `gzip -6`:

| File | gzip |
|---|---|
| `head.js` | 206 |
| `main.js` | 5 309 |
| `shell.js` | 613 |
| `chunks/chunk-P4EHGXV4.js` | 26 143 |
| `home.js` | 897 |
| **totale oggi** | **33 168 B** |
| con `button.js` dentro `shell.js` | **33 584 B** (32,8 KiB) |

Il round 1 dichiarava **27,6 KB**: dimenticava `main.js` (5 309 B) e `head.js` (206 B), che
`base.html:41,66` carica su ogni pagina. Budget `FRONTEND_DEPENDENCIES.md` §3: **≤ 45 KB**. Margine
reale **≈ 11,4 KB**. Immagini: **zero** — il misuratore è markup, la freccia è già nello sprite.

**Paint e layout.** CDP `Tracing`, categoria `disabled-by-default-devtools.timeline`, pagina isolata
con **un solo** bottone e nient'altro che si muova, 12 cicli, due esecuzioni identiche (i numeri
sotto si sono ripetuti alla cifra):

| Prova | Build attuale | Candidato |
|---|---|---|
| hover × 12 | 0 Layout · **96 Paint** | 0 Layout · **96 Paint** |
| press × 12 | **24 Layout** · 134 Paint | **12 Layout** · 168 Paint |

Lettura onesta: **l'hover non costa un pixel più di oggi** — il crossfade di `opacity` su uno pseudo
non è più caro della transizione di `background-color` che il build già paga — e **la pressione
dimezza i layout** (1 per pressione invece di 2). In cambio la pressione dipinge ~3 volte in più per
ciclo, perché un `translate` di 1 px su un elemento non promosso e una `box-shadow` che cambia
ridisegnano la regione del bottone: 366 × 48 px, `LayoutDuration` **+0,0014 s su 10 cicli**, cioè
0,14 ms per ciclo.

**MOTION §7 chiede «0 layout e 0 paint oltre il primo frame», e la pressione non lo raggiunge — né qui
né nel build attuale.** Lo scrivo invece di promettere il contrario. Ho provato la mitigazione che il
round 1 proponeva: `will-change` dentro `@media (hover: hover)` su `.btn:hover`. Misurato: da
**168 a 144 Paint** su 12 pressioni, ma con 12 `PaintImage` in più e un layer di compositing per ogni
bottone sotto il puntatore. **La respingo**: 24 Paint su 12 cicli non pagano un layer, e §7 aveva già
ragione a rifiutare i layer permanenti.

Ho anche **cancellato** lo strato di pressione che il round 1 metteva su `::after`: misurato a
+34 Paint per 12 pressioni e +36 `PaintImage`, per un effetto che l'inversione della luce interna
ottiene con **una sola sostituzione di variabile**. Da qui viene anche la soluzione della tripla
prenotazione di `::after`: lo strato non esiste più, quindi il conflitto non esiste più.

**Nessuna transizione** di `background-color`, `box-shadow`, `width`, `height`, `margin` o `filter`
compare in tutto il foglio; verificabile con `grep -n "transition" static/css/v3/buttons.css` — le
proprietà animate sono `opacity`, `translate` e `transform`, e nient'altro.

**Controlli per pagina** (il conteggio del round 1 era ~3× troppo alto). Misurato oggi:

| Pagina | `.btn` visibili | Controlli (`<button>` + `<summary>` + `<a class="btn">` visibili) |
|---|---|---|
| `/fr/` | **5** | **10** |
| `/fr/forum/` | **2** | **6** |
| `/fr/orientation/` | **1** | **5** |

Il round 1 diceva 19 / 9 / 8 e ci appoggiava l'argomento dei «38 riquadri». L'argomento cade: il
peggio realistico è **10 riquadri di ≤ 56 × 380 px**, dipinti una volta al caricamento.

---

## 8. RISCHI E GUARDIE

I test citati dal round 1 (`tests/frontend/test_v2_tokens.py`, `test_motion_system.py`) **non esistono
nel repository** — verificato con `ls tests/frontend/`. Le guardie qui sotto sono nuove, e quelle che
si appoggiano a qualcosa si appoggiano a file che ci sono: `tests/frontend/test_css_tokens_exist.py`
(ogni `var()` referenziato deve essere definito — il foglio di §4.2 lo rispetta: ogni variabile nuova
è dichiarata in `:root`) e `tests/frontend/test_design_docs.py` (i file citati da un documento devono
esistere su disco).

| # | Che cosa potrebbe farlo sembrare economico, o romperlo | Guardia |
|---|---|---|
| 1 | **La luce verticale diventa un gradiente SaaS**: basta portare `.03` a `.08` | **G1** in `tests/frontend/test_v3_buttons.py`: legge i due stop di `--btn-lit` dal CSS, li compone su `--accent`, `--accent-dark` e `--err-700`, e **fallisce se ΔL\* > 3.0**. Il numero sta nel test, non in un commento. A `.035` il massimo è 3.23 e il test fallisce già: la soglia morde |
| 2 | **L'ombra di contatto diventa un'elevazione, o finisce sotto una superficie trasparente** | **G2**: `grep box-shadow` sul CSS compilato deve restituire solo i sei ruoli dichiarati (A1); nessuna `transition`/`animation` deve nominare `box-shadow`; e un test in browser deve trovare `box-shadow === "none"` su ogni `.btn` il cui `background-color` ha alfa 0. Senza l'emendamento A1 questa spec **non è implementabile**: è un blocco |
| 3 | **La luce interna su un fondo chiaro torna a essere uno smusso** | **G3**: il test calcola L\* del riempimento di ogni variante e fallisce se `--btn-shadow` contiene una `inset` bianca dove L\* > 50. Il round 1 ne metteva una al 90 % su `--min-2`: questa guardia l'avrebbe fermata |
| 4 | **Un foglio d'app ricomincia a dipingere i bottoni** (è già successo: `forum.css` 144, 145, 182-185) | **G4**: il test scandisce `apps/*/static/**/*.css` e fallisce se un selettore che contiene `.btn` dichiara `background`, `color`, `border`, `box-shadow`, `opacity`, `pointer-events` o `outline`. È la regola che l'intestazione di `forum.css` già dichiara, resa eseguibile |
| 5 | **Le tre tacche sembrano un caricamento rotto** se la richiesta è più veloce di un ciclo | La faccia «busy» compare solo dopo **160 ms**; sotto quella soglia il bottone non cambia mai faccia. Evitare il lampeggio conta più dell'animazione |
| 6 | **Il primario teal sembra meno «autorevole» del navy** e qualcuno lo rimette | **G5**: il test fallisce se una regola `.btn*` risolve a un token `--brand-*`. La prova non è di gusto: `--brand-navy` pieno misura **13,75:1** contro la carta, cioè una lastra nera che schiaccia la pagina, e §1.3 r.4 lo vieta fuori dal marchio |
| 7 | **La freccia che avanza su ogni bottone diventa un tic** | `.btn--arrow` resta riservato alla CTA principale di una sezione — al massimo due per pagina — e **G6** conta le occorrenze per file (oggi: **11** in 11 file, ricontate) |
| 8 | **Il registro tutto-maiuscolo del forum**: le etichette vengono dal contenuto bloccato, il CSS non può saperlo | Decisione presa, non rinviata: i sei bottoni interessati ricevono `.btn--upper` (§4.6), che su un testo già maiuscolo è un no-op tipografico e aggiunge il tracking mancante. **G7**: il test fallisce se uno di quei testi bloccati smette di essere maiuscolo mentre la classe è presente — così `text-transform` non altererà mai un testo prescritto |
| 9 | **Due secondari affiancati senza primario** (forum, §1.12) | Fuori dalla mia superficie, lo segnalo: la prima delle due azioni deve diventare `btn--primary`. E il fondo `--brand-navy` di `.forum-cta` è un rilievo per la spec `backgrounds` |
| 10 | **La pressione dipinge più di oggi** (§7) | Numero pubblicato, non nascosto: 168 vs 134 Paint su 12 pressioni, 0,14 ms di layout per ciclo. **G8**: prova obbligatoria prima del merge con CPU rallentata 4×; se il Paint per pressione supera **20**, lo `0 1px` della pressione diventa una pura sostituzione di `--btn-shadow` senza `translate` |

### Domande aperte, da chiudere prima dell'implementazione

1. **A1** (quinto ruolo d'ombra «contatto» + la clausola «solo in hover») — **bloccante**.
2. **A2** (ciclo di stato transitorio per il misuratore) — **bloccante** per lo stato di caricamento.
3. **A3** (la luce verticale sul riempimento «pieno») — non bloccante: se respinta, si toglie
   `--btn-lighting` e il resto della spec non cambia.
4. **A4** (misuratore al posto dello spinner) — non bloccante: se respinta, tre `<span>` diventano un
   `<svg>` con `stroke-dasharray`, e A2 resta comunque necessaria.
5. **Chi possiede `apps/forum/static/forum/forum.css`** deve accettare la rimozione delle tre regole
   di §4.6. Se rifiuta, la spec non è implementabile sul forum senza una scalata di specificità che
   contraddice l'intestazione di quel file: preferisco che la decisione sia presa in chiaro.
6. **`DANGER` con conferma in due tempi** sullo stesso bottone: **non proposto**, perché cambierebbe
   il significato dell'interazione e la direttiva vieta di toccare il workflow. Se il prodotto lo
   vuole, lo decide il prodotto — e allora `documents/index.html:54` può tornare più leggero.
