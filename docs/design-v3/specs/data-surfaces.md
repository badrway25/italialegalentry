# DESIGN V3 — SPEC DI SUPERFICIE: `data-surfaces`

Specialista Dashboard UX + Forms UX · 24 settembre 2026 · **ROUND 2 — RIPARAZIONE**
Superfici: tabelle, filtri, ricerca, stati vuoti, stati di caricamento, formulari — area riservata e moduli pubblici.
Vincolanti: `DESIGN_SYSTEM_V2.md` §1, §2, §3, §7, §9.1, §9.4, §9.6, §10, §11 · `MOTION_SYSTEM.md` §0–§6 · `apps/cms/forbidden.py`.
Revisione di riferimento: `docs/design-v3/reviews/data-surfaces.md` (round 1 — non conforme, non implementabile).

---

## 0. RICHIESTE DI EMENDAMENTO

Due, numerate. Fuori da queste due, questa spec non devia da nessuna clausola di `DESIGN_SYSTEM_V2.md`
o `MOTION_SYSTEM.md`; dove il round 1 deviava senza dichiararlo, la deviazione è stata **rimossa**,
non regolarizzata (vedi §0.3).

### AMENDMENT REQUEST 1 — `DESIGN_SYSTEM_V2.md` §1.1: due tinte semantiche nuove

**Clausola.** §1.1 «Semantica — mai marca»: `--ok-700 #1E7A4D · --ok-100 #DCEFE4 · --ok-300 #7CCFA0 ·
--err-700 #B3261E · --err-100 #F6DEDC · --seal-600 #8C6D4B · --seal-100 #EFE6DA · --seal-300 #C7A77E ·
--pending-700 #705434`. Il §1.2 dà i rapporti **sul canvas `--min-0`**, non su un fondo di livello 100.

**Che cosa chiedo.** L'aggiunta di **due** token, e di due sole righe alla tabella §1.2:

```css
--ok-800:      #17603B;  /* 6.32:1 su --ok-100 — testo della pillola «Valide»      */
--pending-100: #F0E9DD;  /* fondo delle pillole d'attesa (5.79:1 con --pending-700) */
```

Il bronzo **non** riceve un token nuovo. La §4.1 lo toglie dalle pillole e lo rimette dove il DS lo
vuole davvero — il **glifo a sigillo del responsabile quando è l'autorità competente** (DS §9.2,
§9.3) — dove `--seal-600 #8C6D4B` misura **3.99:1** sulla riga `--min-1` e **4.57:1** sulla scheda
`--min-2`, sopra la soglia dei 3:1 per un elemento grafico. Il round 1 inventava uno stato «scellé»
che **nessun modello del prodotto possiede**: è stato eliminato, non ricolorato.

**Ragione (ricalcolata in questa sessione, non ripresa dal round 1).** La pillola di stato del §9.4
è «glifo + parola» su un fondo: il testo semantico deve quindi reggere AA **sul proprio fondo 100**,
che è più chiaro del canvas. Calcolo WCAG 2.x (luminanza relativa, script in §0.4):

| Coppia esistente | Rapporto | Esito |
|---|---:|---|
| `--ok-700 #1E7A4D` su `--ok-100 #DCEFE4` | **4.44:1** | sotto 4.5 — **non passa** |
| `--err-700 #B3261E` su `--err-100 #F6DEDC` | **5.10:1** | passa — nessun token nuovo |
| `--pending-700 #705434` su `--min-0` | 6.29:1 | passa, ma gli stati d'attesa non hanno un fondo 100 |
| `--seal-600 #8C6D4B` su `--min-1` (**glifo**, non testo) | **3.99:1** | passa per un elemento grafico |

Con i token nuovi: `--ok-800` su `--ok-100` = **6.32:1**; `--pending-700` su `--pending-100` =
**5.79:1**. Nessuna tinta esce dalle famiglie semantiche già ammesse e nessuna tonalità nuova entra:
sono due gradini della stessa scala.

**Costo.** Due token in un documento dichiarato FISSATO; `tests/frontend/test_v2_tokens.py` va esteso
con le due righe. `--ok-700` resta il verde grafico (tacche del misuratore, 4.46:1 su `--min-1`), non
diventa mai testo su `--ok-100`. Se il Council rifiuta, l'alternativa è la pillola «valide» senza
fondo (solo bordo + glifo + parola), che perde il terzo canale e indebolisce §9.4: lo dico perché la
scelta resti al Council, non a me.

### AMENDMENT REQUEST 2 — `DESIGN_SYSTEM_V2.md` §2: la pillola «BLOQUÉ» inverte inchiostro e carta

**Clausola.** §2 elenca sette livelli di superficie, tutti su carta (`--min-*`) o su mezzanotte
(`--mid-*`), e §1.3 regola 5 ammette **un capitolo mezzanotte per pagina**.

**Che cosa chiedo.** Un unico oggetto di 24 px può usare `--ink` come **fondo** e `--min-0` come
testo: `.pill--blocked { background: var(--ink); color: var(--min-0) }` — **14.62:1** (calcolato).
Non è un capitolo mezzanotte (non usa `--mid-*`, non ha confine di sezione, non ha transizione di
sfondo): è un timbro.

**Ragione.** Con `.reg` portato al livello 1 (`--min-1`, §4.1) le pillole neutre non hanno più un
fondo chiaro disponibile: `--min-1` su `--min-1` è 1.00:1, invisibile. Resta `--min-3` (bianco),
che la spec assegna al foglio depositato — «Déposé» e «En examen», i due stati in cui la pezza è
arrivata e nulla è ancora deciso — e a nient'altro. «BLOQUÉ» è l'unico
stato in cui la persona **non può agire affatto**; merita l'unico segnale invertito del sistema, e
l'inversione è per definizione irripetibile. Alternativa scartata: `--err-100`/`--err-700`, vietata
perché il rosso è **solo errore** (§1.3 regola 3) e un blocco procedurale non è un errore.

**Costo.** Un settimo caso nella grammatica delle superfici, da annotare in §2. Rischio di lettura
come bottone: mitigato dal raggio 999 px (che nessun controllo ha: §2 dà 2 px ai controlli), dai
12 px maiuscoli, dal glifo `icon-lock` e dall'assenza di qualunque affordance di pressione.

### 0.3 — Le deviazioni del round 1 che NON chiedo di regolarizzare

Rimosse, non emendate: `--radius-tile` su `.reg` (ora 0); i chip a 999 px dei facet (ora controlli a
2 px, §4.3); `--accent` come testo di una pillola non interattiva (ora `--min-3`/`--ink`, §4.1); i
due cicli sotto i 20 s (`skel/shimmer` 1 600 ms e `f/submit-progress` 900 ms — entrambi eliminati,
§5); lo stagger di 30 ms (ora 40 ms, il minimo di `MOTION_SYSTEM` §2); le soglie di 200/400 ms dello
scheletro (ora `--motion-fast` 180 e `--motion-slow` 320, due token esistenti, §4.5).

### 0.4 — Riproduzione delle misure

**Contrasti.** Luminanza relativa WCAG 2.x, `(L1+0.05)/(L2+0.05)`, script
`…/scratchpad/v3ds/contrast.py` e `contrast2.py` eseguiti con `.venv\Scripts\python.exe`. Ogni
rapporto citato in questo documento è uscito da quegli script in questa sessione. Nessuna cifra del
round 1 è stata ricopiata: **tutte** sono state ricalcolate, e una è cambiata (§0.5, MUST-FIX 8).

**Layout.** Chromium di Playwright **153.0.8010.12**, headless, `device_scale_factor=1`,
`locale=fr-FR`, viewport 1440×900 · 1024×900 · 768×900 · 390×844. I fogli di stile reali
(`/static/css/main.css`, `/static/portal/portal.css`) sono serviti dal server di sviluppo su
`127.0.0.1:8771`; la pagina di prova e il foglio candidato sono iniettati con
`page.route()` sulla **stessa origine**, quindi font, token e cascata sono quelli di produzione. Il
foglio candidato è servito come `<link rel="stylesheet">` reale: **nessun `<style>` in linea, nessun
attributo `style=""`** — la misura è stata presa sotto le stesse condizioni CSP della produzione.
Script: `…/scratchpad/v3ds/{probe_chrome.py, probe_ax.py, probe_reg.py, probe2.py, sel.py,
candidate.css}`; uscite `out1.json`, `out2.json`; schermate `s2_*.png`, `shot_*.png`.

**Contenuto della prova.** Non lorem: il registro pezze a 7 righe e la checklist a 9 righe sono
composti con i fatti che i template reali rendono — `titre`, `Facultative`, `state_reason`,
`version {{ n }}`, `état`, `responsable` + `responsible_note`, `source_title` (FONDEMENT),
`échéance`, `action` e il ramo `action_blocked` con il link alle Conditions d'utilisation. **Il
«prima» e il «dopo» sono misurati nello stesso run, con lo stesso contenuto e la stessa cornice**
(folio + conteggi presenti in entrambi): il confronto del round 1 non lo era.

### 0.5 — Registro delle correzioni: i tredici MUST-FIX

| # | Stato | Dove | Che cosa è cambiato |
|---|---|---|---|
| 1 | **FATTO** | §4.1 | `.pill--filed` non usa più `--accent`. Fondo `--min-3` #FFFFFF, testo `--ink` (**16.23:1**), bordo 1 px `--hairline-strong` (**3.14:1** contro la riga `--min-1`). È l'unico fondo con un bordo: un foglio bianco depositato sulla carta minerale. In piu, lo stato «scellé» che il round 1 aveva inventato — nessun modello del prodotto lo possiede — è eliminato, e il bronzo torna al glifo del responsabile-autorità (DS §9.2). |
| 2 | **FATTO** | §4.1 | `.reg { border-radius: 0 }` (misurato: `0px`). `.reg__record` sotto 768 ha anch'esso raggio 0. I 6 px restano al solo tassello del marchio. In più: `.reg` scende al **livello 1** (`--min-1`), perché il §9.4 chiede «riga in hover livello 2» e una riga non può salire al livello 2 se il contenitore ci è già. |
| 3 | **FATTO** | §4.3 | Facet riscritti senza 999 px: controllo QUIET, raggio `--radius-control` 2 px, filetto di 3 px sul bordo di lettura, `aria-current="true"`, glifo di spunta, conteggio nello `<span>`. Bersagli misurati **104.3 × 44 · 129.1 × 44 · 140.4 × 44** e «tout effacer» **221.9 × 44**. |
| 4 | **FATTO** | §4.5, §5 | Nessun ciclo. Lo scheletro è statico (nessuno shimmer). Il progresso d'invio è determinato dai byte reali dell'XHR, oppure non esiste. Zero oggetti vivi su una pagina DENSE, come vuole `MOTION_SYSTEM` §4. Nessuna deroga richiesta. |
| 5 | **FATTO** | §0.6, §3, §4.1, §5 | Ordinamento **tagliato dalla V1**. `aria-sort`, `.reg__sort`, la voce di moto e la giustificazione del candidato 9 sono eliminate. Il lavoro Django che servirebbe è scritto in §0.6 come richiesta di modifica fuori perimetro, indirizzata al product owner. |
| 6 | **FATTO** | §4.2 | La scheda-record ha uno slot nominato per ognuno dei sei fatti, tutti **verbatim**. Il tetto di 128–152 px è abbandonato: era falso. Misura reale **190–218 px** (checklist) e **238–298 px** (registro pezze). Il −54 % è ritirato e sostituito da **−29 %** e **−24 %** misurati (§4.2). |
| 7 | **FATTO** | §4.1 | `<caption class="reg__caption">` è nell'anatomia, primo figlio della `<table>`, e `aria-labelledby` resta sulla regione che scorre quando quella regione esiste. |
| 8 | **FATTO** | §1.5, §6 | «nessun `aria-label`» e «senza nome» cancellati: `templates/portal/dashboard.html:92` porta `aria-labelledby="t-dashboard-1"` verso una `<caption>` invisibile. E `--hairline-strong` su `--min-3` è **3.74:1**, non 3.59 (il 3.59 è la cifra su `--min-2`). |
| 9 | **FATTO** | §4.3, §4.1 | Con l'ordinamento tagliato, l'unico `<form method="get">` dentro `.reg` è `.finder`, e apre e chiude **dentro `.reg__masthead`**: non attraversa mai la tabella. I facet sono `<a>` reali, senza form. La striscia d'aggancio è su **`.reg__head th::after`** (il `th` è `position: sticky`, quindi genera un blocco contenitore affidabile), con un `<div class="reg__sentinel">` prima della tabella per l'`IntersectionObserver`. Niente `::after` su un `<thead>`. |
| 10 | **FATTO** | §4.2, §7 | `.reg__record` **è il `<tr>`**. Sopra 768 resta `display: table-row` (misurato) e non porta né `content-visibility` né `contain`. Sotto 768 diventa `display: grid` (misurato) e **solo allora**, e **solo se il corpo supera 24 record** (`.reg[data-long="true"]`), riceve `content-visibility: auto`. Risparmio d'altezza e risparmio di pittura sono separati e attribuiti (§7). |
| 11 | **FATTO** | §6, §7 | Misurato invece che assunto: il cromo appiccicoso dell'area riservata è **`.portal-bar`, 70 px** (non `--chrome-height` = 100 px, e nemmeno i 56 px del DS §9.1). Il `scroll-padding-block-start` **effettivo** del documento è **80 px** a 1440 e **72 px** a 390 — una sola dichiarazione viva (`shell.css:490`), non tre. Questa spec **non** ne aggiunge una quarta. |
| 12 | **FATTO** | §1.0, §4.0 | Un paragrafo intero sulla domanda del committente, con la distinzione RICH/DENSE che il round 1 non aveva letto, e il momento di firma che questa superficie può permettersi: **il margine di legatura** — gutter di 36 px, ordinale citabile in mono, filetto di rilegatura, misuratore a tacche, testata in Newsreader. |
| 13 | **FATTO** | §4.1 | La sovrapposizione `::after { inset: 0 }` è **eliminata**. Il bersaglio nasce dal padding del link: misurato **310.1 × 28 px** a 1440, **154.2 × 40 px** a 768, **293 × 28 px** a 390. Ogni cella — riferimento, échéance, état — resta selezionabile e copiabile. |

**Dispute: nessuna.** Ho verificato ogni contestazione del revisore prima di accettarla, e le due che
potevano cadere hanno retto: nessuna vista legge `?sort=` (`grep -rn "\"sort\"\|'sort'" apps/portal
apps/documents apps/cases apps/companies` → 0 risultati; `request.GET` compare in `apps/portal` solo
per `page`, righe 86, 104, 111, 123), e `--hairline-strong` su `--min-3` è davvero 3.74. Una sola
precisazione, a **favore** del revisore: il selettore `:has()` annidato è ancora peggio di come lo
descrive. Ho verificato in Chromium 153 che **entrambi** i membri della lista separata da virgola
lanciano `SyntaxError` — `.scroll-x:has(table:has(tbody [data-label]))` **e**
`.table-region:has(table:has(tbody [data-label]))` — quindi la regola `portal.css` L475–479 è
scartata per intero, e non c'è nessun ramo che sopravvive.

### 0.6 — RICHIESTA DI MODIFICA FUORI PERIMETRO: l'ordinamento di colonna

Non è un emendamento al sistema di design: è una domanda di prodotto, e la pongo perché il round 1
l'aveva spacciata per gratuita.

**Stato di fatto, verificato.** Nessuna vista e nessun servizio di `apps/portal`, `apps/documents`,
`apps/cases`, `apps/companies` legge `request.GET["sort"]`. L'unico parametro GET vivo in area
riservata è `page` (`apps/portal/views.py` 86, 104, 111, 123, via `services.paginate`).
`apps/documents/requirements.py:35` fissa l'ordine del registro come **verità di prodotto**:
`STATE_ORDER` — «Rank used to sort a register. Missing and expiring first» — mancanti e in scadenza
per primi, perché sono le righe per cui la persona è venuta.

**Quindi.** L'ordinamento di colonna è **fuori dalla V1 di questa spec**. Non si scrive `aria-sort`,
non si scrive `.reg__sort`, non si promette che «funziona senza JavaScript».

**Che cosa costerebbe, se il product owner lo volesse.** (a) Un parametro `sort` validato contro una
lista bianca per superficie, in `portal.services` e `documents.presenters`, con un valore di default
che **resta** `STATE_ORDER`. (b) Una decisione giuridica: se riordinare una checklist prescritta sia
ammissibile, dato che l'ordine di default porta un significato (già `HUMAN_QA_REQUIRED (f)` nel
round 1 — lì era una nota a piè di pagina, qui è la domanda principale). (c) Il ripristino
dell'ordine del fascicolo sempre disponibile **per nome**, non per icona. (d) `aria-sort` sul `<th>`,
il bottone dentro la cella (mai il `<th>` cliccabile — è la sola cosa che tengo dal candidato 9), e
un `<form method="get">` che, non potendo stare dentro un `<thead>`, si appoggia a
`form="reg-sort"` con il `<form>` dichiarato dentro `.reg__masthead`. Senza (a) e (b), (d) non si
scrive.

---

## 1. VERDETTO SULLO STATO ATTUALE

### 1.0 — La domanda del committente, e perché questa superficie risponde per sottrazione

Il committente ha respinto il lavoro del 24 settembre con due parole: **immagini** e **fondali**.
Questa spec propone ancora **zero fotografie e zero capitolo mezzanotte** sulle liste, e adesso lo
argomenta invece di tacerlo.

`DESIGN_SYSTEM_V2.md` §7 assegna i modi. Il round 1 ha trattato tutte e quindici le superfici come
DENSE: è un errore di lettura. La tabella dice:

- **RICH** — «hub Personnes, Academy, **cruscotti**, fabbisogno impresa»: un capitolo mezzanotte,
  reveal editoriali, grafici con dati reali. **Vietati**: isoipse, marea.
- **DENSE** — «fascicolo, **liste**, **tabelle**, back-office»: transizioni di stato e molla di
  layout. **Vietati**: ombre, vetro, **reveal**.

Il cruscotto è RICH e ha **già** il suo capitolo mezzanotte: la barra di piattaforma `--mid-1` e la
case band `--mid-2` del §9.1. Aggiungerne un secondo violerebbe §1.3 regola 5. `/mes-documents/`,
`/mes-echeances/`, `/mes-demandes/`, `/entreprise/mes-besoins/` e la coda del guichet sono DENSE:
lì il §6 vieta esplicitamente il sistema cartografico («**mai** su STANDARD/DENSE/LEGAL») e il §7
vieta i reveal. Una fotografia in un registro giuridico, inoltre, non è un fondale: è un'immagine
accanto a un elenco di persone e di stati, e la §6 la esclude per ragioni che non sono estetiche.

**Dove sta allora il premio, su una superficie che non può avere né immagine né buio.** Sta nella
materia e nella tipografia, e questa spec ne dà cinque pezzi concreti, non un principio:

1. **Il margine di legatura.** Ogni registro apre con un gutter di **36 px** sul bordo di lettura,
   chiuso da un filetto verticale di 1 px `--hairline` che corre per tutta l'altezza del corpo: il
   dorso di un registro rilegato. Nessun'altra superficie del prodotto ha questo gutter.
2. **L'ordinale citabile.** Dentro quel gutter, il numero di riga in `--f-mono` `--t-folio`
   tabellare. Non è decorazione: è il numero con cui si cita una riga al telefono con l'autorità
   competente. Il prodotto ha già questa grammatica (`.entry__ordinal`, `.folio__ordinal`): qui
   arriva dove serve di più.
3. **Il misuratore a tacche** (DS §9.1, «avancement come misuratore a cinque tacche = conteggio»):
   N tacche per N pezze, piene quelle validate. Non è una barra di percentuale — il commento di
   `register.html` è esplicito, «Counts, never a percentage meter: "3 sur 7" is verifiable» — è il
   conteggio, disegnato.
4. **La testata come frontespizio.** Rubrica mono maiuscola + riferimento del fascicolo, nome della
   regione in **Newsreader 400 a 22/28**, filetto di chiusura 2 px `--hairline-strong`. Non una
   barra di strumenti: un frontespizio.
5. **Lo scheletro che è la rigatura.** Il caricamento non è una banda che scorre: sono le righe del
   registro, disegnate e non ancora riempite, in `--hairline` (1.27:1 su `--min-1`). Il vuoto di un
   registro è la sua rigatura, non un effetto.

E una **assenza dichiarata**: `--terr-line` non compare (grafica di territorio, vietata su DENSE),
il tricolore non compare (vive solo nel marchio), il bronzo compare **solo** sulla pillola «scellé»,
che è letteralmente un sigillo. Se il committente vuole comunque un'immagine su queste pagine,
allora la decisione da prendere è cambiare il modo di pagina nel §7 del DS — cioè un emendamento
suo, non una licenza mia. Non lo chiedo, perché non credo che un registro giuridico migliori con una
fotografia accanto.

### 1.1 — Il prodotto non esegue il proprio sistema di design

Il DS §9.4 prescrive «cifre tabellari, riga in hover livello 2, stato come pillola con glifo +
parola, molla di layout»; il §9.6 «skeleton con `aria-busy`, annuncio `aria-live`»; il §10 «campi
48 px». Sulle quindici superfici misurate nel round 1: cifre tabellari **0**, regole di hover di
riga **0**, pillole **0**, animazioni **0**, `aria-busy` **0**, `aria-live` **0**, skeleton **0**,
paginazione resa **0**, `data-mode` **`null` su tutte e quindici**. Non è un ritardo di
propagazione: è un sistema descritto e mai scritto.

### 1.2 — La tabella è una stampa, non un componente

`.data-table` su `/mes-documents/`: `thead` `position: static`, `font-variant-numeric: normal`,
`td { vertical-align: baseline }`, nessuno sfondo di tabella né di riga. Nessuna regola `tr:hover`
esiste in **nessuno** dei fogli caricati (sonda sul CSSOM: `hoverRules = []`). Ri-misurato in questa
sessione, a 1440, sul registro a 7 righe: **quattordici** elementi interattivi, **undici sotto
24 × 24 px** — i link di titolo misurano 15 px di altezza, le azioni 18. A 390 sono quattordici su
quattordici sotto i 24 px. WCAG 2.2 §2.5.8 chiede 24 × 24.

### 1.3 — Il filetto di testata usa il colore ufficiale del marchio

`thead th { border-block-end: 2px rgb(15,37,71) }` = **#0F2547 = `--brand-navy`**. `bridge.css`
ri-punta `--navy → var(--brand-navy)`: il blu della Repubblica, che §1.1 riserva al lock-up
ufficiale, è oggi il filetto di venti tabelle (`grep -rl data-table templates apps/*/templates` =
**20**). Esce.

### 1.4 — Quattro colori di stato fuori tavolozza, e uno di essi è un secondo accento

`.state` calcolato: `background: rgba(0,0,0,0)`, `border-radius: 0`, `hasSvg: false`, altezza
**16 px**. Non è una pillola: è una parola con un filetto. I colori vengono da `static/css/tokens.css`
(V1): `--state-error-fg #8F1D1D`, `--state-pending-fg #5E4B14`, `--state-warn-fg #7A4E00`,
`--state-done-fg = --state-info-fg #1E4A85`. Nessuno esiste in V2. Il #1E4A85 è un blu: nella
colonna ÉTAT «DÉPOSÉ» ha l'aspetto di un link, cioè un secondo colore interattivo, vietato da §1.3.
**Il round 1 ha diagnosticato questo difetto e poi l'ha riprodotto**, dando a `.pill--filed` il
`--accent` #0F6A72, che è il colore dei link *veri* di questo sito: peggio dell'originale. §4.1 lo
corregge.

### 1.5 — Il pop-in di telefono è la regione peggiore del prodotto, e il suo guardiano è CSS invalido

A 390, ri-misurato in questa sessione con i fatti reali: il registro pezze a 7 righe misura **2 484 px**
di sole righe (330–386 px per riga); la checklist a 9 righe **2 611 px** (283–309 px per riga), e la
pagina intera **2 837 px = 3,36 viewport**. Causa visibile: il pop-in ripete l'intestazione su ogni
cella — cinque etichette maiuscole per riga sul registro, quattro sulla checklist.

Il guardiano che dovrebbe togliere lo scorrimento orizzontale è **CSS invalido**. Verificato in
Chromium 153 con `document.querySelector()`:

```
.scroll-x:has(table:has(tbody [data-label]))      → SyntaxError
.table-region:has(table:has(tbody [data-label]))  → SyntaxError
```

I due selettori sono uniti da una virgola in `portal.css` L475–479: **un selettore invalido in una
lista invalida l'intera regola**, quindi nessuno dei due rami esiste. Risultato misurato sul
cruscotto a 390: `.scroll-x` resta `overflow-x: auto` con `tabindex="0"` e `role="region"` mentre
`scrollWidth === clientWidth === 350` — una regione focalizzabile che non scorre da nessuna parte.
Su `/mes-documents/` la stessa situazione è salvata per caso da una regola diversa e valida in
`documents.css` L159–163: due pagine gemelle con due comportamenti.

**Correzione al round 1 (MUST-FIX 8).** La regione **non è senza nome**:
`templates/portal/dashboard.html:92` porta `aria-labelledby="t-dashboard-1"`, che risolve sulla
`<caption>` invisibile «Éléments du dossier, leur état, le responsable et l'échéance» (riga 94), e
`templates/documents/partials/register.html:30` porta un `aria-label` esplicito. Il difetto reale —
selettore invalido, regione focalizzabile che non scorre — non aveva bisogno di quell'aggiunta, ed è
più grave di come era descritto.

**Secondo difetto, trovato misurando (nuovo).** Le regole del pop-in non si possono **sovrascrivere**:
`table:has(tbody [data-label]) tr` ha specificità **(0,2,0)**, mentre una regola di classe come
`.reg__record` ha **(0,1,0)**. Misurato: con il foglio candidato caricato *dopo* `portal.css`, il
`<tr>` calcolava ancora `display: block` invece di `display: grid`, e la scheda-record non si
formava. Il blocco va **cancellato**, non coperto (§4.7).

**Terzo, verificato e non un difetto.** Il `display: block` del pop-in **non** distrugge la
semantica di tabella in Chromium: letto dall'albero di accessibilità via CDP
(`Accessibility.getPartialAXTree`) a 390, la `<table>` resta `table`, il `<tr>` `row`, il
`<th scope="row">` `rowheader`, il `<td>` `cell`. Il rimedio ARIA resta comunque nella spec (§4.2)
perché WebKit storicamente non si comporta così, ma **non** è vero che oggi la semantica cade, e non
lo scriverò.

### 1.6 — Due sistemi di stato vuoto, uno con la gerarchia rovesciata

`.empty-state` (components.css, 21 template): riquadro `1px dashed` centrato, icona 40 px, **0
azioni**, e `title` a **13 px** sopra un `text` a **17 px** — il titolo è più piccolo del proprio
corpo. Ri-misurato in questa sessione dentro una colonna di 976 px: **274 px** di altezza.
`.empty` (register.css, 31 template): un `<p>` allineato a sinistra, senza `role`, senza glifo,
senza azione. Su tre stati vuoti misurati, **due non offrono alcuna azione risolutiva**.

### 1.7 — I formulari rendono il bordo di default del browser

`companies/need_form.html`, `profile_form.html` e `enquiries/partials/form_shell.html` usano
`class="form__group"`. `grep -c form__group` sul CSS: **0**. `.form__fieldset`, che *è* definita in
components.css, è usata da **0** template. Conseguenza misurata sui quattro `<fieldset>` del
formulario imprese: `border: 2px groove rgb(240,240,240)`, `padding: 5.95px 12.75px` — lo stile
nativo di Chromium, in produzione, anche sul modulo pubblico di raccolta dei fabbisogni.

### 1.8 — Il bordo rosso dell'errore non compare mai: perde la cascata

Sottomissione reale con titolo vuoto. Il riassunto funziona (`role="alert"`, `tabindex="-1"`, il
fuoco ci va). Ma sul controllo in errore: `aria-invalid="true"` ✓, `box-shadow: rgb(143,29,29) 0 0 0
1px` ✓, **`border-color: rgb(122,134,139)`** ✗ — il grigio `--hairline-strong`.
`.form-field--error input:not([type=checkbox]):not([type=radio])` ha specificità **(0,3,1)**; la
regola di base `.form-field input:not([type=checkbox]):not([type=radio]):not([type=file])` ha
**(0,4,1)** e vince. Inoltre il `<ul>` d'errore di campo porta `role="alert"` **e** il riassunto lo
porta: due regioni vive allo stesso caricamento, l'errore annunciato due volte. E `aria-live`
sull'intera pagina = **0**.

### 1.9 — Campi a 44 px, invisibili sul proprio fondo, e un asterisco color errore

Controlli misurati: `height 44px` (il DS §10 prescrive **48**), `background rgb(244,243,240)` =
**`--min-0`, esattamente il colore della pagina**; `border 1px #7A868B`; aiuto a 13 px `--ink-3`
*sotto* il controllo; `.form-field__required` = **`rgb(143,29,29)`**: ogni campo obbligatorio
indossa il colore dell'errore prima di qualunque errore. Il formulario «nouveau besoin» misura
**4 249 px** a 1440 con il bottone d'invio a `y = 3 950` e `.form__actions { position: static }`.

### 1.10 — I filtri sono testo, e il conteggio entra nel nome accessibile

`/formation/`: otto `.academy-filters__link` alti 24–25 px, `background: transparent`, `padding: 0`.
Il conteggio è incollato al nome: `parentText === "Langue italienne1"`. Nessun «tout effacer»
(`0` elementi), nessuna regione viva per il numero di risultati. La ricerca di `/faq/` e
`/glossaire/`: campo 44 px, fondo `--min-0` (di nuovo il colore della pagina), nessun glifo, nessun
bottone di svuotamento, nessun conteggio annunciato.

### 1.11 — Una transizione `all`

`.portal-list__item` calcola `transition-property: all`: qualunque proprietà, comprese quelle di
layout, diventa animabile per caso.

**Nota RTL.** In `ar` a 390 su `/mes-documents/`: `dir=rtl`, overflow orizzontale **0**, `::before`
del pop-in con `text-transform: none` e `letter-spacing: normal`, famiglia `IBM Plex Sans Arabic`.
La logica direzionale è corretta e va preservata. Difetto: riferimenti e date ereditano la famiglia
araba invece del mono occidentale prescritto da §3.1. Secondo difetto, verificato in questa
sessione: **`--dir` non è definito in nessun foglio di `static/css/`** (letto da
`getPropertyValue('--dir')` sul `:root` a 1440 e a 390 → stringa vuota), benché `MOTION_SYSTEM` §5
lo prescriva.

---

## 2. UI-UX-PRO-MAX

Sette interrogazioni. Lo strumento è tarato su «government = accessible & ethical, avoid motion
effects»: è esattamente il registro che il committente ha respinto. Dove sbaglia lo dico.

| # | Query (dominio) | Restituito (condensato) | Esito |
|---|---|---|---|
| 1 | `premium data table design sticky header row hover density` (ux) | Animation › Hover vs Tap: «gli effetti hover non funzionano su touch». Responsive › Table Handling: «usa scroll orizzontale **o** layout a scheda» | **ACCETTATO** il primo: l'hover non porta mai informazione, solo affordance. **ACCETTATO** il layout a scheda; **RESPINTO** lo scroll orizzontale come equivalente: su un registro a 5 colonne è una rinuncia, e la misura (2 484 px per 7 righe) dice che anche il pop-in attuale lo è |
| 2 | `form field height label inline error validation accessibility` (ux) | Forms › Error Placement: errore inline legato con `aria-describedby`. Forms/A11y › Focusable Error Summary: riassunto in cima, fuoco sul contenitore, **mantenere gli errori inline**. Forms › Inline Validation: validare sul `blur` | **ACCETTATO** il contratto del riassunto — «retain inline errors» significa inline **più** riassunto, non due `role="alert"`. **RESPINTO** la validazione sul `blur`: la validazione è server-side e legale (`forbidden.py`, criteri d'età); una validazione JS ottimista che contraddice il server su un modulo giuridico è peggio di nessuna |
| 3 | `empty state skeleton loading state feedback` (ux) | Feedback › Empty States: «messaggio utile **e un'azione**». Loading: «scheletro o progresso stabile con `aria-busy`; mai spinner lampeggiante; non applicare una sola soglia a ogni operazione» | **ACCETTATO**. La soglia variabile diventa una regola concreta, ma espressa **in token**: lo scheletro compare dopo `--motion-fast` (180 ms) e resta almeno `--motion-slow` (320 ms). Il round 1 usava 200/400 ms, due numeri che `MOTION_SYSTEM` §1 non conosce |
| 4 | `filter chips faceted search saved views` (product) | Directory/Listing → «Filter-Heavy Grid + Map», «category color chips», «verified badge», palette «Professional Blue + Success Green» | **RESPINTO**. I chip colorati codificano un'appartenenza senza ordine; qui i facet sono *stati giuridici* e *responsabili*. Il «Professional Blue» è precisamente l'errore già in produzione (#1E4A85). Preso **solo** il principio del conteggio per facet, che è verificabile |
| 5 | `dashboard table list animation stagger row` (gsap) | Stagger List/Subtle: 250–350 ms, «stagger 0,02–0,04 s», «non superare 0,1 s per elemento»; e testualmente: **«non usare `back.out` su tabelle dense: l'overshoot sembra sciatto su UI informativa»** | **ACCETTATO** e citato: giustificazione indipendente della regola «niente overshoot». Sullo stagger le due fonti si incontrano a **40 ms**: è il massimo della loro forchetta e il minimo della nostra (`MOTION_SYSTEM` §2, «scaglionata 40–60 ms»). Il round 1 aveva scritto 30 ms, che è fuori dal nostro sistema: corretto a 40. **RESPINTO** GSAP: Motion 13.4.1 è già nel bundle (misurato: **26 143 byte gzip**), un secondo motore sfonderebbe i 45 KB |
| 6 | `tabular numerals data density typography table` (typography) | «Dashboard Data»: Fira Code per i dati + Fira Sans per le etichette. Cita font Google via `@import` | **ACCETTATO** il principio — è già il nostro: `--f-mono` è **Fira Mono**, `--f-sans` **Fira Sans**. Serve solo applicarlo. **RESPINTO** categoricamente l'`@import` da Google Fonts: CSP `style-src 'self'`, nessun font remoto, e `forbidden.py` cerca quell'host come violazione su ogni pagina pubblica |
| 7 | `government institutional dashboard admin panel` (style) | `data-dense-dashboard`: «padding 8–12 px, font 12–14 px, `--table-row-height: 36px`, sidebar filtri, sticky headers»; `inclusive-design`: «7:1, evitare rosso-verde da solo, indicatori a simbolo» | **ACCETTATO** sticky header e barra filtri. **RESPINTO** la densità: 36 px di riga e 12 px di testo violano WCAG 2.2 §2.5.8 e non sono il registro di un fascicolo giuridico — la riga di base resta **56 px** minimi. **ACCETTATO** «indicatori a simbolo»: pillola glifo + parola + fondo, tre canali, mai il colore da solo |

---

## 3. 21ST.DEV

Nove candidati confrontati; tre letti nel codice (`get_component`: 27049, 19746, 28301). Nulla viene
installato: sono tutti React + Tailwind + shadcn; qui si estrae il **pattern** e si riscrive in
Django + token V2.

| # | Candidato | Che cosa prendo | Che cosa rifiuto |
|---|---|---|---|
| 1 | **Data Table** — arihantcodes *(letto)* | `aria-busy` sulla `<table>`, e **una sola** regione `role="status" aria-live="polite"` sempre renderizzata, col commento «so repeated counts announce reliably»: è la risposta esatta al difetto 1.10. Più `<thead>` sticky con l'ombra che compare solo a scorrimento avvenuto, e `tabular-nums` | Le molle `stiffness 500 / damping 28` e `SPRING_ENTRANCE 260/20` (fuori dalle nostre due), lo `shadow` animato (vietato), lo scambio d'icone con `blur` (vietato), `aria-sort` (fuori perimetro, §0.6) e l'intero impianto React |
| 2 | **Empty** — cnippet-dev *(letto)* | Lo stato vuoto come **sistema di slot** (`header/media/title/description/content`), con l'azione in uno slot *obbligatorio* e il titolo sopra una descrizione più piccola: l'inverso esatto del nostro 13 px sopra 17 px | La variante `media="icon"` con due carte fantasma ruotate di ±10°: decorazione che finge dati. E il blocco centrato `py-20`: il nostro vuoto è allineato alla lettura, come le righe che sostituisce |
| 3 | **Field Validation** — ai2 *(letto)* | Lo stato d'errore guidato da **`aria-invalid` sul controllo**, non da una classe sul genitore: è la cura del difetto 1.8. Più il `describedby` composto `[descId, msgId]`, che §4.6 scrive per esteso | I cinque wrapper esportati come componenti separati: qui lo stato viene dal server, un campo è uno. E la validazione live «as you type» |
| 4 | Data Table — ephraimduncan | La riga di testata completa come **inventario** di ciò che manca | La casella di selezione per riga e le azioni di massa: in questo prodotto **nessun ruolo agisce su più righe insieme**. Da qui anche la decisione di §4.1 di non avere affatto uno stato «selected» |
| 5 | Records Table — theshanelevine | La **prima colonna appiccicosa** su tabelle larghe, se un giorno il registro imprese supera cinque colonne | I «connection-strength indicators» e il footer di calcoli: qui nessun numero è calcolato dall'interfaccia, mai |
| 6 | Advanced Filter Builder — laziekiki | «live results»: il conteggio si aggiorna insieme al filtro | La logica AND/OR componibile: costruire query è un mestiere da back-office |
| 7 | Task Filters — preetsuthar17 | Il **conteggio dei filtri attivi** e l'azione «clear all» che appare solo quando serve | La forma a chip a 999 px (vietata da §10) e i filtri su cinque dimensioni: qui i facet utili sono due |
| 8 | Table Skeleton — uiable | Lo scheletro che **ricalca la tabella** invece di un rettangolo generico: evita il salto di layout | Il pulsare a `opacity` su ogni riga: N elementi animati. Il nostro scheletro **non si muove affatto** (§4.5) |
| 9 | Sortable Table — felipemenezes098 | L'intestazione cliccabile come `<button>` dentro il `<th>`, non il `<th>` reso cliccabile — **tenuto come nota per §0.6**, non implementato qui | TanStack Table: 14 KB di runtime per una funzione che **il prodotto non ha**. Il round 1 scriveva «un ordinamento che il server fa già con un `?sort=`»: falso, e la correzione è in §0.6. Il rifiuto di TanStack resta, con la ragione giusta — restiamo server-rendered e il budget JS è misurato, non elastico |

---

## 4. LA PROPOSTA — «Il registro rilegato»

Un solo file nuovo, **`static/css/v3/data-surfaces.css`** (misurato: 14 146 byte, **3 179 byte
gzip**), più un modulo **`static/js/src/data.js`**. Sostituisce — **cancellando**, non coprendo — il
blocco `.data-table` + pop-in di `apps/portal/static/portal/portal.css` L297–487, `.empty-state` di
`static/css/components.css` L2624–2653 e il blocco `.form-field` L2141–2352 (misurati insieme:
12 875 byte, **3 994 byte gzip**). Nessuna vista Django e nessun contratto dati toccato: tutto passa
da classi, `data-*` e il parametro GET `page`, che è l'unico vivo (§0.6).

### 4.0 — Le due letture del sistema che reggono tutto il resto

**(a) `.reg` è un'AREA, non un foglio.** §2 dà: livello 1 «area» = `--min-1`; livello 2
«interattivo (foglio, **riga**, pannello)» = `--min-2` + hairline, con `--shadow-2` solo in hover. Il
§9.4 chiede «**riga in hover livello 2**». Una riga non può salire al livello 2 se il contenitore ci
è già: quindi il registro è l'area (`--min-1`) e la **riga** è l'oggetto di livello 2 che si
materializza sotto il puntatore (`--min-2`). Misurato: `--min-2` su `--min-1` = **1.14:1**, il
gradino materico più forte della scala minerale — più forte del 1.09:1 che il round 1 otteneva
lavando l'accento al 6 %, e senza usare l'accento su uno sfondo, che §1.3 regola 1 vieta
(«Nessun titolo, icona o **sfondo** lo usa»). Il round 1 aveva un accento al 6 % non dichiarato:
sparisce.

**(b) Non esiste uno stato «selected».** In questo prodotto nessun ruolo agisce su più righe insieme
(candidato 4). Uno stato «selected» sarebbe cromatura che promette un potere inesistente, e il
round 1 lo introduceva insieme al rischio «l'hover letto come selezionato» che poi doveva sorvegliare.
Eliminato: un rischio in meno, una tinta in meno, una guardia in meno.

### 4.1 La tabella — `.reg`

**Anatomia (completa, nell'ordine del DOM).**

```
.reg[data-density][data-long][data-pinned]      area, livello 1
├── .reg__masthead                              frontespizio
│   ├── .reg__rubric        mono maiuscolo + riferimento del fascicolo
│   ├── .reg__name          <h2> Newsreader 400, 22/28
│   ├── .reg__ledger        misuratore a tacche + conteggio
│   │   ├── .reg__tally     N tacche, aria-hidden
│   │   └── .reg__count     <span role="status" aria-live="polite">  ← regione viva unica
│   └── form.finder         (solo se > 8 righe) — apre e CHIUDE qui dentro
├── .facets                 (opzionale)         <a> reali, nessun form
├── .reg__scroll[data-scrollable]
│   ├── .reg__sentinel      <div aria-hidden>, 1px, per l'IntersectionObserver
│   └── table.reg__table
│       ├── caption.reg__caption                ← OBBLIGATORIA (DS §9.4)
│       ├── thead.reg__head  > tr > th[scope=col]
│       └── tbody.reg__body  > tr.reg__record   > th[scope=row] + td[data-role]
└── .reg__foot              {% include "components/pagination.html" %}
```

**Foglio, testata, righe, marcatore — il CSS, per esteso.**

```css
.reg {
  --reg-row: 56px;          /* la riga di base */
  --reg-folio: 36px;        /* il margine di legatura */
  --reg-pin: var(--chrome-height);
  background: var(--min-1);
  border: 1px solid var(--hairline);
  border-radius: 0;                       /* DS §2: capitoli e fogli a 0 */
  color: var(--ink);
}
.page-portal .reg { --reg-pin: 72px; }    /* misurato: .portal-bar = 70px — §6 */
.reg[data-density="compact"] { --reg-row: 48px; }   /* back-office, scelta di template */

.reg__masthead {
  display: grid; grid-template-columns: minmax(0, 1fr) auto;
  align-items: end; gap: var(--s-2) var(--s-6);
  padding: var(--s-4) var(--s-6) var(--s-3);
  border-block-end: 2px solid var(--hairline-strong);
}
.reg__rubric {
  display: block;
  font: 400 var(--t-folio)/var(--t-folio-lh) var(--f-mono);
  letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--ink-3);
}
.reg__name { margin: 0; font: 400 var(--t-entry)/var(--t-entry-lh) var(--f-serif); color: var(--ink); }
.reg__ledger { display: flex; align-items: center; gap: var(--s-3); margin: 0; }
.reg__count {
  margin: 0; font: 400 var(--t-folio)/var(--t-folio-lh) var(--f-mono);
  font-variant-numeric: tabular-nums lining-nums slashed-zero; color: var(--ink-2);
}
.reg__tally { display: inline-flex; gap: 3px; }
.reg__tally i { display: block; inline-size: 3px; block-size: 16px; background: var(--hairline-strong); }
.reg__tally i[data-filled] { background: var(--ok-700); }

.reg__scroll { position: relative; }
.reg__scroll[data-scrollable="true"] { overflow-x: auto; }
.reg__sentinel { block-size: 1px; margin-block-end: -1px; }
.reg__table {
  inline-size: 100%; border-collapse: collapse;
  font: 400 var(--t-ui)/var(--t-ui-lh) var(--f-sans);
  font-variant-numeric: tabular-nums lining-nums slashed-zero;   /* DS §3.2 */
}

.reg__head th {
  position: sticky; inset-block-start: var(--reg-pin); z-index: 2;
  background: var(--min-1);
  text-align: start; vertical-align: bottom;
  padding-block: var(--s-2); padding-inline: 0 var(--s-6);
  font: 600 var(--t-folio)/var(--t-folio-lh) var(--f-sans);
  letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--ink-2);
  border-block-end: 1px solid var(--hairline-strong);   /* il --brand-navy esce (§1.3) */
}
.reg__head th:first-child { padding-inline-start: var(--reg-folio); inline-size: 38%; }
:lang(ar) .reg__head th { text-transform: none; letter-spacing: 0; }

/* la striscia d'aggancio: su ::after del TH, che è sticky e quindi un blocco contenitore
   affidabile — mai su un <thead>, che è un table-header-group (MUST-FIX 9) */
.reg__head th::after {
  content: ""; position: absolute; inset-block-start: 100%; inset-inline: 0;
  block-size: 8px; pointer-events: none; opacity: 0;
  background: linear-gradient(to bottom, rgba(10,21,28,.10), rgba(10,21,28,0));
}
.reg[data-pinned="true"] .reg__head th::after { opacity: 1; }   /* mai box-shadow animato */

.reg__body th, .reg__body td {
  text-align: start; vertical-align: middle;
  padding-block: var(--s-2); padding-inline: 0 var(--s-6);
  border-block-end: 1px solid var(--hairline);
  scroll-margin-block-start: calc(var(--reg-pin) + var(--reg-row));   /* §6, MUST-FIX 11 */
}
.reg__body tr:last-child th, .reg__body tr:last-child td { border-block-end: 0; }

/* il margine di legatura */
.reg__body th[scope="row"] {
  position: relative; font-weight: 400;
  padding-inline-start: var(--reg-folio); min-block-size: var(--reg-row);
}
.reg__body th[scope="row"]::before {          /* il dorso */
  content: ""; position: absolute; inset-block: 0;
  inset-inline-start: calc(var(--reg-folio) - 13px);
  inline-size: 1px; background: var(--hairline);
}
.reg__body th[scope="row"]::after {           /* il marcatore del bordo di lettura */
  content: ""; position: absolute; inset-block: 0; inset-inline-start: 0;
  inline-size: 3px; background: var(--accent);
  transform: scaleY(0); transform-origin: top;
}
.reg__ordinal {
  position: absolute; inset-inline-start: 0; inset-block-start: 11px;
  inline-size: calc(var(--reg-folio) - 17px); text-align: end;
  font: 400 var(--t-folio)/var(--t-folio-lh) var(--f-mono);
  font-variant-numeric: tabular-nums lining-nums slashed-zero; color: var(--ink-3);
}

/* IL BERSAGLIO — dal padding del link, MAI da una sovrapposizione (MUST-FIX 13) */
.reg__link {
  display: flex; align-items: center; min-block-size: 28px;
  padding-inline-end: var(--s-3); color: var(--accent);
  font-size: var(--t-body); text-decoration-thickness: 1px; text-underline-offset: 3px;
}
.reg__link--plain { color: var(--ink); }      /* righe senza destinazione: la checklist */

.reg__body tr:hover th, .reg__body tr:hover td { background: var(--min-2); }   /* livello 2 */
.reg__body tr:has(:focus-visible) th,
.reg__body tr:has(:focus-visible) td { background: var(--min-2); }             /* un solo :has */
.reg__body tr.is-overdue th[scope="row"]::after { background: var(--err-700); transform: scaleY(1); }

.reg__apparatus, .reg__reason { display: block; max-inline-size: 52ch; }
.reg__apparatus, .reg__reason { font: 400 var(--t-caption)/var(--t-caption-lh) var(--f-sans); color: var(--ink-2); }
.reg__cell--action { position: relative; z-index: 1; }
.reg__action { display: inline-flex; align-items: center; min-block-size: 24px; padding-block: 10px; color: var(--accent); }
.reg__foot {
  display: flex; align-items: center; justify-content: space-between; gap: var(--s-4);
  padding: var(--s-3) var(--s-6); border-block-start: 1px solid var(--hairline);
}
@media (min-width: 48rem) { .reg__cell > .reg__rubric--inline { display: none; } }
```

**Misure (Chromium 153, `.portal__main` = 976 px a 1440, 686 px a 768, 348 px a 390).**

| | oggi | V3 | nota |
|---|---:|---:|---|
| registro 7 righe, altezza righe a 1440 | 586,5 px (67–139) | **706 px** (77–121) | +20 %, ed è il prezzo di §4.2 |
| registro 7 righe, bersagli sotto 24 px a 1440 | **11 su 14** | **0 su 22** | WCAG 2.2 §2.5.8 |
| registro 7 righe, bersagli sotto 24 px a 390 | **14 su 14** | **0 su 22** | |
| link primario di riga, 1440 | 160,6 × **15** px | **310,1 × 28** px | dal padding del link |
| link primario di riga, 768 / 390 | — | 154,2 × 40 / 293 × 28 | |
| scorrimento orizzontale, 390 / 768 / 1024 / 1440 | 0 | **0** | `scrollWidth === clientWidth` ovunque |
| testata appiccicosa | `position: static` | `sticky`, offset **72 px** | misurato, §6 |

**`.reg__foot` e la paginazione (GAP 12).** `.reg__foot` è un `<div>` **dopo** la `</table>` e
dentro `.reg`, non un `<tfoot>`: la paginazione non è una riga di dati. Porta il componente che
esiste già e che funziona davvero, perché `?page=` è l'unico parametro GET vivo:

```django
<div class="reg__foot">
  {% include "components/pagination.html" %}
  <p class="reg__count">{% blocktranslate with a=page_obj.start_index b=page_obj.end_index t=page_obj.paginator.count %}{{ a }}–{{ b }} sur {{ t }}{% endblocktranslate %}</p>
</div>
```

```css
.reg__foot { /* vedi sopra */ }
.reg__foot .pagination__list { display: flex; align-items: center; gap: var(--s-2); margin: 0; padding: 0; list-style: none; }
.reg__foot .pagination__link {
  display: inline-flex; align-items: center; gap: 6px;
  min-block-size: 44px; padding-inline: var(--s-3);
  border-radius: var(--radius-control); color: var(--accent); text-decoration: none;
}
.reg__foot .pagination__link:hover { background: var(--min-2); }
.reg__foot .pagination__status {
  font: 400 var(--t-folio)/var(--t-folio-lh) var(--f-mono);
  font-variant-numeric: tabular-nums; color: var(--ink-2);
}
```

`pagination.html` rende già `Page {{ n }} sur {{ total }}` con `aria-current="page"` e
`icon--flip-rtl` sulle frecce: non si tocca il suo markup, si veste. Il `.reg__foot` non si rende
quando `page_obj.paginator.num_pages <= 1`, perché il componente stesso non rende nulla in quel caso.
Questo chiude anche la mezza verità di §1.1: la paginazione resa è 0 **come cromatura**, non come
funzione — `services.paginate` e `components/pagination.html` esistono e sono usati da sette
template.

**Il raggio.** `.reg` calcola `border-radius: 0px` (misurato). `.reg__record` sotto 768 idem. Il
`--radius-tile` di 6 px non compare in questo foglio; `grep radius-tile` su `data-surfaces.css` deve
tornare 0 risultati, e un test lo verifica (§8).

**Pillole — `.pill`.** Le classi non sono inventate: sono i **valori reali** che i presenter già
producono. `documents.requirements.STATE_CSS` ne dà **sette** (`missing · filed · review · valid ·
invalid · expired · replace`, resi come `pill--{{ row.state_css }}`) e
`cases.models.ChecklistStatus` ne dà **cinque** (`pending · in_progress · done · not_applicable ·
blocked`, resi come `pill--{{ item.status }}`). **Dodici classi, tutte scritte qui**, mappate su
**cinque fondi più un contorno**. Il round 1 ne disegnava sei di fantasia e nessuna delle dodici
vere: un implementatore avrebbe trovato cinque classi senza CSS. Tre canali sempre — parola, glifo,
fondo — e mai il colore da solo.

```css
.pill {
  display: inline-flex; align-items: center; gap: 6px;
  block-size: 24px; padding-inline: 8px 10px;
  border: 1px solid transparent; border-radius: 999px;   /* DS §2: 999 alle pillole di stato */
  font: 600 var(--t-caption)/1 var(--f-sans);
  letter-spacing: .04em; text-transform: uppercase; white-space: nowrap;
}
:lang(ar) .pill { text-transform: none; letter-spacing: 0; }
.pill__glyph { inline-size: 12px; block-size: 12px; flex: none; }

/* fondo 1 — ATTESA: il tempo passa, nessuno ha sbagliato */
.pill--missing,
.pill--replace,
.pill--pending,
.pill--in_progress    { background: var(--pending-100); color: var(--pending-700); }

/* fondo 2 — IL FOGLIO DEPOSITATO: arrivato, nulla è deciso. L'unico con un bordo. */
.pill--filed,
.pill--review         { background: var(--min-3); color: var(--ink); border-color: var(--hairline-strong); }

/* fondo 3 — VALIDO: l'unico verde, e «Valide» non vuol dire «approuvé» */
.pill--valid,
.pill--done           { background: var(--ok-100); color: var(--ok-800); }

/* fondo 4 — ERRORE: rosso solo qui (DS §1.3 r. 3) */
.pill--invalid,
.pill--expired        { background: var(--err-100); color: var(--err-700); }

/* fondo 5 — IL TIMBRO: nessuno può agire (AMENDMENT REQUEST 2) */
.pill--blocked        { background: var(--ink); color: var(--min-0); }

/* contorno — NON APPLICABILE: non è uno stato, è un'assenza di stato */
.pill--not_applicable { background: transparent; color: var(--ink-3);
                        border-color: var(--hairline-strong); border-style: dashed; }
```

| Classe resa | Origine | Parola resa | Fondo | Testo | Rapporto | Glifo (esiste nello sprite) |
|---|---|---|---|---|---:|---|
| `.pill--missing` | `STATE_CSS` | Manquant | `--pending-100` | `--pending-700` | **5.79:1** | `icon-minus` |
| `.pill--replace` | `STATE_CSS` | À remplacer | `--pending-100` | `--pending-700` | **5.79:1** | `icon-clock` |
| `.pill--filed` | `STATE_CSS` | Déposé | `--min-3` + bordo `--hairline-strong` | `--ink` | **16.23:1** (bordo **3.14:1**) | `icon-document` |
| `.pill--review` | `STATE_CSS` | En examen | `--min-3` + bordo `--hairline-strong` | `--ink` | **16.23:1** | `icon-search` |
| `.pill--valid` | `STATE_CSS` | Valide | `--ok-100` | `--ok-800` *(AR 1)* | **6.32:1** | `icon-check` |
| `.pill--invalid` | `STATE_CSS` | Non valide | `--err-100` | `--err-700` | **5.10:1** | `icon-warning` |
| `.pill--expired` | `STATE_CSS` | Expiré | `--err-100` | `--err-700` | **5.10:1** | `icon-calendar` |
| `.pill--pending` | `ChecklistStatus` | Da fare | `--pending-100` *(AR 1)* | `--pending-700` | **5.79:1** | `icon-minus` |
| `.pill--in_progress` | `ChecklistStatus` | In corso | `--pending-100` | `--pending-700` | **5.79:1** | `icon-arrow` |
| `.pill--done` | `ChecklistStatus` | Completato | `--ok-100` | `--ok-800` | **6.32:1** | `icon-check` |
| `.pill--not_applicable` | `ChecklistStatus` | Non applicabile | trasparente + bordo **tratteggiato** | `--ink-3` | **5.14:1** su `--min-1` (bordo 3.14:1) | `icon-close` |
| `.pill--blocked` | `ChecklistStatus` **e** `row.action_blocked` | Bloccato | `--ink` *(AR 2)* | `--min-0` | **14.62:1** | `icon-lock` |

Due coppie condividono un fondo — «Déposé»/«En examen» e «Non valide»/«Expiré» — ed è deliberato:
dentro ciascuna coppia la differenza è **reale ma non di gravità**, e a distinguerle restano la
parola e il glifo, cioè due canali su tre. Nessuno stato si affida al colore da solo. Il round 1
aveva sei tinte per sei stati immaginari; qui ci sono **cinque fondi per dodici stati veri**, e il
numero di tinte su una tabella **scende**.

**Come il template sceglie il glifo, senza toccare una vista.** I presenter danno `state_css` e
`status`, non un'icona. La mappa vive accanto ad `attr_is`, nello stesso filtro di presentazione, e
il template scrive `{% svg_icon row.state_css|state_glyph "pill__glyph" %}`:

```python
# apps/core/templatetags/ile_core.py
_STATE_GLYPH = {
    "missing": "minus",  "replace": "clock",   "filed": "document", "review": "search",
    "valid": "check",    "invalid": "warning", "expired": "calendar",
    "pending": "minus",  "in_progress": "arrow", "done": "check",
    "not_applicable": "close", "blocked": "lock",
}

@register.filter
def state_glyph(value: str) -> str:
    return _STATE_GLYPH.get(value, "info")   # ogni id esiste già in static/img/icons.svg
```

Dodici voci, dodici simboli **già presenti** nei 36 dello sprite: nessun disegno nuovo qui. L'unico
simbolo da aggiungere in tutta la spec è `icon-threshold` per gli stati vuoti (§4.4).

**Il bronzo, dove il DS lo vuole.** Non è uno stato: è il **responsabile**. Quando
`row.responsible_actor == "authority"`, il glifo del responsabile è `icon-shield` in `--seal-600`
(**3.99:1** sulla riga `--min-1`, **4.57:1** sulla scheda `--min-2`) — l'anello a sigillo
dell'autorità competente di DS §9.2 e §9.3. È l'unico bronzo di questa superficie.

```css
.reg__owner-glyph { inline-size: 16px; block-size: 16px; flex: none; color: var(--ink-3); }
.reg__owner-glyph--authority { color: var(--seal-600); }
```

I quattro colori legacy (#8F1D1D, #5E4B14, #7A4E00, #1E4A85) spariscono; un test li cerca nel CSS
compilato e fallisce se li trova (§8).

**Riga espandibile.** `<tr class="reg__record">` + `<tr class="reg__detail">`; il commutatore è un
`<button class="reg__expand" aria-expanded aria-controls>` di 44 × 44 nell'ultima cella. Senza
JavaScript il dettaglio è renderizzato **aperto**; `hidden` lo scrive `data.js` all'avvio. Serve dove
una riga ha uno storico (versioni di una pezza, transizioni di uno stato) e **sostituisce una
navigazione** — non nasconde mai un fatto che oggi è visibile (§4.2).

**Selettori del file.** `.reg`, `.reg__masthead`, `.reg__rubric`, `.reg__name`, `.reg__ledger`,
`.reg__tally`, `.reg__count`, `.reg__scroll`, `.reg__sentinel`, `.reg__table`, `.reg__caption`,
`.reg__head`, `.reg__body`, `.reg__record`, `.reg__cell`, `.reg__ordinal`, `.reg__link`,
`.reg__apparatus`, `.reg__reason`, `.reg__owner-glyph`, `.reg__cell--action`, `.reg__action`, `.reg__expand`,
`.reg__detail`, `.reg__foot`, `.pill`, `.pill__glyph`, `.facets`, `.facets__disclosure`,
`.facets__summary`, `.facets__group`, `.facet`, `.facet__glyph`, `.facet__count`, `.facets__clear`,
`.facets__permalink`, `.finder`, `.void`, `.skel`, `.progress`, `.f__*`.

**Codice Python toccato: due filtri di presentazione, zero viste, zero modelli, zero migrazioni.**
`attr_is` (§4.1, per il misuratore) e `state_glyph` (§4.1, per il glifo della pillola), entrambi in
`apps/core/templatetags/ile_core.py`, accanto al `get_item` che c'è già. Nessun contratto dati
cambia: i due filtri leggono ciò che i presenter producono oggi.

**Template toccati.** `templates/documents/partials/register.html`,
`templates/portal/dashboard.html`, `templates/portal/documents.html`,
`templates/companies/partials/need_register.html`, `templates/components/empty_state.html`,
`templates/components/form_field.html`, `templates/components/form_errors.html`, più **un solo
nuovo parziale**: `templates/components/register_masthead.html`.

**Il componente generico è tagliato (GAP 8).** `templates/components/data_table.html` con
`rows`/`columns`/`sortable`/`region_label` non si scrive: `columns` non esiste in nessun contesto di
vista, e le colonne e l'apparato giuridico cambiano da superficie a superficie. Al suo posto un
parziale che incapsula **solo** il frontespizio, con un contratto piccolo e un sito di chiamata
reale, scritto per intero:

```django
{# templates/components/register_masthead.html
   Contratto: `rubric` (testo), `name` (testo), `name_id` (id per aria-labelledby),
   `count_text` (la frase di dominio, già pluralizzata dal chiamante),
   `tally` (iterabile delle righe, facoltativo) e `tally_done` nella forma «attributo=valore»,
   che il chiamante compone con ciò che le sue righe hanno davvero.
   Rende il frontespizio e la regione viva unica della pagina. #}
{% load i18n ile_core %}
<div class="reg__masthead">
  <div>
    <span class="reg__rubric">{{ rubric }}</span>
    <h2 class="reg__name" id="{{ name_id }}">{{ name }}</h2>
  </div>
  <p class="reg__ledger">
    {% if tally and tally|length <= 12 %}
    <span class="reg__tally" aria-hidden="true">{% for row in tally %}<i{% if row|attr_is:tally_done %} data-filled{% endif %}></i>{% endfor %}</span>
    {% endif %}
    <span class="reg__count" role="status" aria-live="polite">{{ count_text }}</span>
  </p>
</div>
```

Il misuratore itera **le righe che il template ha già**: nessun conteggio nuovo, nessun campo
nuovo, nessuna migrazione, nessuna vista toccata. Serve un filtro, e uno solo, da aggiungere a
`apps/core/templatetags/ile_core.py` accanto al `get_item` che c'è già — perché un template Django
non sa leggere un attributo il cui **nome** è una variabile:

```python
@register.filter
def attr_is(obj, spec: str) -> bool:
    """`{{ row|attr_is:"status=done" }}` — vero quando l'attributo (o la chiave) vale `done`.

    Le righe del registro sono dizionari (`documents.presenters.present_requirement`), quelle
    della checklist sono modelli (`cases.models.ChecklistItem`): il filtro regge entrambi.
    """
    name, _, expected = spec.partition("=")
    value = obj.get(name) if isinstance(obj, dict) else getattr(obj, name, None)
    return str(value) == expected
```

Se il chiamante non passa `tally`, il misuratore non si rende e il conteggio resta la frase.

```django
{# templates/portal/dashboard.html — il sito di chiamata, verbatim #}
{% translate "Ce qui reste à faire, et par qui" as checklist_name %}
{% blocktranslate asvar checklist_count count n=checklist|length %}{{ n }} élément{% plural %}{{ n }} éléments{% endblocktranslate %}
<div class="reg" id="checklist"{% if checklist|length > 24 %} data-long="true"{% endif %}>
  {% include "components/register_masthead.html" with rubric=case.reference name=checklist_name name_id="checklist-title" count_text=checklist_count tally=checklist tally_done="status=done" %}
  <div class="reg__scroll">
    <div class="reg__sentinel" aria-hidden="true"></div>
    <table class="reg__table" role="table"> … </table>
  </div>
  <div class="reg__foot">{% include "components/pagination.html" %}</div>
</div>
```

`status=done` è `cases.models.ChecklistStatus.DONE`, che gli elementi della checklist **hanno già**;
sul registro pezze il chiamante passa `tally_done="state_css=valid"`, che è il valore prodotto da
`documents.requirements.STATE_CSS[RequirementState.VALID]`. Nessuno dei due è inventato, e nessuno
dei due è un campo nuovo. Se un registro futuro non avesse un valore adatto, non passa `tally` e non
ha il misuratore: il conteggio verificabile resta la frase, che è il contratto scritto in
`register.html` («Counts, never a percentage meter: "3 sur 7" is verifiable»).

### 4.2 Sotto 768 — la scheda-record al posto del pop-in

**Che cosa è `.reg__record` (MUST-FIX 3 e 10).** È il **`<tr>`**, e nient'altro. Sopra 768 calcola
`display: table-row` (misurato) ed è una riga di tabella in tutto. Sotto 768 calcola `display: grid`
(misurato) ed è una scheda. Non esiste mai come elemento indipendente, e `content-visibility` non
tocca mai un box `table-row`.

**Markup, per esteso.** Modifica **di solo template**: si aggiungono `role`, `data-role` e le classi;
non si toglie né si sposta nessun fatto.

```html
<tr class="reg__record is-overdue" role="row">
  <th scope="row" role="rowheader" class="reg__cell" data-role="title" data-label="Élément">
    <span class="reg__ordinal" aria-hidden="true">03</span>
    <a class="reg__link" href="{{ row.detail_url }}">{{ row.title }}</a>
    <span class="reg__apparatus">
      {% if not row.mandatory %}{% translate "Facultative" %} · {% endif %}
      {% if row.current %}{% blocktranslate with n=row.version_count %}version {{ n }}{% endblocktranslate %} · {% endif %}
      <span class="reg__rubric reg__rubric--inline">{% translate "Fondement" %}</span>{{ item.source_title }}
    </span>
    {% if row.state_reason %}<span class="reg__reason">{{ row.state_reason }}</span>{% endif %}
  </th>
  <td role="cell" class="reg__cell" data-role="state" data-label="État">
    <span class="pill pill--{{ row.state_css }}">{% svg_icon row.state_css|state_glyph "pill__glyph" %}{{ row.state_label }}</span>
  </td>
  <td role="cell" class="reg__cell" data-role="owner" data-label="Responsable">
    <span class="reg__rubric reg__rubric--inline">{% translate "Responsable" %}</span>
    {% if row.responsible_actor == "authority" %}{% svg_icon "shield" "reg__owner-glyph reg__owner-glyph--authority" %}{% endif %}
    {{ row.responsible }}{% if row.responsible_note %} — {{ row.responsible_note }}{% endif %}
  </td>
  <td role="cell" class="reg__cell" data-role="due" data-label="Échéance">
    {% if row.due_date %}<time datetime="{{ row.due_date|date:'c' }}">{{ row.due_date|date:"d.m.Y" }}</time>{% else %}—{% endif %}
  </td>
  <td role="cell" class="reg__cell reg__cell--action" data-role="action" data-label="Action">
    {% if row.may_file %}<a class="reg__action" href="{{ row.detail_url }}">…</a>
    {% elif row.action_blocked %}
      <span class="pill pill--blocked">{% svg_icon "lock" "pill__glyph" %}{% translate "Bloqué" %}</span>
      {% safe_url 'legal:terms' as terms_url %}{% if terms_url %}<a class="reg__action" href="{{ terms_url }}">{% translate "Accepter les Conditions d’utilisation" %}</a>{% else %}<span class="reg__apparatus">{% translate "Acceptation des Conditions d’utilisation requise." %}</span>{% endif %}
    {% else %}<a class="reg__action" href="{{ row.detail_url }}">{% translate "Consulter" %}</a>{% endif %}
  </td>
</tr>
```

**I sei fatti che il round 1 lasciava cadere, e dove stanno adesso (MUST-FIX 6).** Tutti e sei
restano **verbatim**, al pari delle frasi degli stati vuoti, e tutti e sei restano **visibili**: non
uno finisce dietro una `<details>` o dentro `.reg__detail`, perché oggi sono visibili e nasconderli
sarebbe una perdita, non un ridisegno.

| Fatto | Sorgente | Slot | Classe |
|---|---|---|---|
| `Facultative` | `register.html` — `{% if not row.mandatory %}` | riga 3 della scheda, primo segmento | `.reg__apparatus` |
| `version {{ n }}` | `register.html` — `{% if row.current %}` | riga 3, secondo segmento | `.reg__apparatus` |
| `item.source_title` (**FONDEMENT**, DS §9.8) | `dashboard.html:107` | riga 3, terzo segmento, **con rubrica visibile** | `.reg__apparatus > .reg__rubric--inline` |
| `row.state_reason` | `register.html` — `.doc-register__reason` | riga 4, frase intera | `.reg__reason` |
| `responsible_note` | `register.html`, `dashboard.html` | riga 6, dopo il responsabile, separatore « — » | `[data-role="owner"]` |
| `action_blocked` + link **Conditions d'utilisation** + fallback bloccato | `register.html` | riga 7, pillola `--blocked` + azione a 44 px; se `safe_url` non risolve, la frase bloccata «Acceptation des Conditions d'utilisation requise.» resta **verbatim** | `.reg__cell--action` |

**CSS della scheda, per esteso.**

```css
@media (max-width: 47.999rem) {
  /* il frontespizio si impila */
  .reg__masthead { grid-template-columns: minmax(0, 1fr); padding-inline: var(--s-4); }
  .reg__ledger { flex-wrap: wrap; gap: var(--s-2); }
  .reg__count { font-size: var(--t-caption); }

  /* la testata appiccicosa è disattivata: le schede portano le proprie etichette */
  .reg__head {
    position: absolute; inline-size: 1px; block-size: 1px;
    overflow: hidden; clip-path: inset(50%); white-space: nowrap;
  }
  .reg .reg__table, .reg .reg__body, .reg .reg__record > * { display: block; inline-size: auto; }
  .reg .reg__body { display: grid; gap: var(--s-3); padding: var(--s-3); }

  .reg .reg__record {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    grid-template-areas: "state due" "title title" "owner owner" "action action";
    gap: var(--s-2) var(--s-3);
    position: relative;
    padding: var(--s-3) var(--s-4) var(--s-3) calc(var(--reg-folio) + var(--s-2));
    background: var(--min-2);                     /* livello 2: la scheda È la riga */
    border: 1px solid var(--hairline);
    border-radius: 0;                             /* MUST-FIX 2 */
  }
  .reg[data-long="true"] .reg__record { content-visibility: auto; contain-intrinsic-size: auto 208px; }

  .reg .reg__record > [data-role="title"]  { grid-area: title;  padding: 0; border: 0; min-block-size: 0; position: static; }
  .reg .reg__record > [data-role="state"]  { grid-area: state;  padding: 0; border: 0; }
  .reg .reg__record > [data-role="due"]    { grid-area: due;    padding: 0; border: 0; text-align: end;
                                             font-family: var(--f-mono); font-size: var(--t-folio); color: var(--ink-2); }
  .reg .reg__record > [data-role="owner"]  { grid-area: owner;  padding: 0; border: 0; font-size: var(--t-small); color: var(--ink-2); }
  .reg .reg__record > [data-role="action"] { grid-area: action; padding: 0; border: 0; }
  .reg .reg__record [data-role]::before { content: none; }      /* il pop-in muore */

  .reg__record .reg__ordinal { inset-block-start: var(--s-3); inset-inline-start: var(--s-3);
                               inline-size: calc(var(--reg-folio) - 16px); text-align: start; }
  .reg__record th[scope="row"]::before { content: none; }
  .reg__record th[scope="row"]::after  { inset-inline-start: calc((var(--reg-folio) + var(--s-2)) * -1 + 8px); }
  .reg__link { display: block; min-block-size: 0; margin: 0; padding: 0;
               font: 400 var(--t-entry)/var(--t-entry-lh) var(--f-serif); }   /* il fatto, il più grande */
  .reg__record .reg__action { min-block-size: 44px; padding-block: 10px; }
  .reg__rubric--inline { display: inline; margin-inline-end: 6px; }
}
```

**La banda 768–1024 (GAP 13).** Da 768 in su la tabella è una tabella: stessi cinque colonne, stessa
testata appiccicosa, nessuna colonna nascosta (§8). Misurato a 768 e a 1024:
`scrollWidth === clientWidth` (686 e 678 px), quindi **nessuno scorrimento orizzontale** e
`data-scrollable` non viene mai posto. Se un registro futuro supera la larghezza,
`.reg__scroll[data-scrollable="true"]` lo rende scorrevole e `data.js` aggiunge in quel momento —
**e solo in quel momento** — `tabindex="0"`, `role="region"` e `aria-label`. Nessun `:has()`
annidato: un `ResizeObserver` confronta `scrollWidth > clientWidth`, e il CSS legge un solo
attributo.

**Il guadagno, misurato (e la ritirata del −54 %).** Stesso contenuto, stessa cornice, stesso run.

| Superficie, a 390 | oggi | V3 | delta |
|---|---:|---:|---:|
| checklist 9 righe — altezza per scheda | 283–309 px | **190–218 px** | |
| checklist 9 righe — totale righe | 2 611 px | **1 849 px** | **−29 %** |
| checklist — documento intero | 2 837 px (3,36 viewport) | **2 101 px (2,49)** | **−26 %** |
| registro 7 righe — altezza per scheda | 330–386 px | **238–298 px** | |
| registro 7 righe — totale righe | 2 484 px | **1 893 px** | **−24 %** |

Il round 1 prometteva **−54 %** e schede di 128–152 px. **Era falso**, e cade qui: una scheda che
tiene `Facultative`, `version n`, il FONDEMENT, il `state_reason`, il `responsible_note` e il ramo
bloccato con il suo link non entra in quattro righe. Il numero onesto è **−24 % / −29 %**, ottenuto
sopprimendo le etichette ripetute del pop-in e non un solo fatto. Chi volesse il −54 % deve
cancellare tre fatti giuridici dalla riga: non è una decisione di design.

**Il prezzo sul desktop, dichiarato.** A 1440 il registro cresce da 586,5 a **706 px** (+20 %) e la
checklist da 602,5 a **728 px** (+21 %). Comprano: undici bersagli sotto i 24 px che diventano zero,
il margine di legatura con l'ordinale citabile, le cifre tabellari su ogni data, la pillola a tre
canali e il conteggio annunciato. Su un registro di sette righe che sta comunque in una schermata e
mezza, è uno scambio che difendo.

### 4.3 Facet, ricerca, permalink

**`.facet` — un controllo, non un chip (MUST-FIX 3).** È un `<a>` reale (link GET, server-rendered),
espresso con il vocabolario del §10: QUIET, raggio `--radius-control` **2 px**, filetto di 3 px sul
**bordo di lettura** — la stessa grammatica del marcatore di riga, quindi il registro ha un solo
gesto e non due.

```css
.facets {
  display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-2) var(--s-4);
  padding: var(--s-2) var(--s-6); border-block-end: 1px solid var(--hairline);
}
.facets__group { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-2); }
.facet {
  display: inline-flex; align-items: center; gap: 6px;
  min-block-size: 44px; padding-block: 10px; padding-inline: 10px 12px;
  border: 1px solid transparent;
  border-inline-start: 3px solid var(--hairline);
  border-radius: var(--radius-control);            /* 2px — MAI 999 */
  background: transparent; color: var(--ink); text-decoration: none;
  font: 500 var(--t-ui)/var(--t-ui-lh) var(--f-sans);
}
.facet:hover { background: var(--min-2); border-inline-start-color: var(--hairline-strong); }
.facet[aria-current="true"] {
  background: var(--min-2);                        /* livello 2, come la riga in hover */
  border-inline-start-color: var(--accent);        /* il facet È un link: l'accento è al suo posto */
  color: var(--accent); font-weight: 600;
}
.facet__glyph { inline-size: 12px; block-size: 12px; flex: none; visibility: hidden; }
.facet[aria-current="true"] .facet__glyph { visibility: visible; }   /* quattro canali, non uno */
.facet__count { font-family: var(--f-mono); font-variant-numeric: tabular-nums; color: var(--ink-3); }
.facet[aria-current="true"] .facet__count { color: var(--accent); }

.facets__clear {
  display: inline-flex; align-items: center; gap: 6px;
  min-block-size: 44px; padding-block: 10px; padding-inline: 12px;
  border: 0; border-radius: var(--radius-control); background: transparent; color: var(--ink);
  font: 500 var(--t-ui)/var(--t-ui-lh) var(--f-sans);
  text-decoration: underline; text-underline-offset: 3px;     /* QUIET, non una pillola */
}
.facets__clear:hover { background: var(--min-1); }
```

Quattro canali sull'attivo: **parola in grassetto**, **filetto di lettura in `--accent`**, **glifo di
spunta visibile**, **`aria-current="true"`**. Il colore non porta mai l'informazione da solo.
Bersagli misurati a 1440 e a 390: **104,3 × 44**, **129,1 × 44**, **140,4 × 44** px per i facet,
**221,9 × 44** px per «tout effacer». Zero elementi sotto 24 × 24 su tutta la superficie candidata,
a tutte e quattro le larghezze.

Il conteggio esce dal nome accessibile, che è il difetto 1.10:
`<span class="facet__count"><span class="visually-hidden">, </span>12<span class="visually-hidden"> résultats</span></span>`
— «Langue italienne1» non esiste più.

**Sotto 768 i facet si chiudono in un `<details>` nativo** (la stessa scelta che il DS §9.1 fa per
account e lingua), perché tre facet aperti misurano 189 px sopra il primo dato:

```css
@media (max-width: 47.999rem) {
  .facets { padding: 0; border-block-end: 0; }
  .facets__disclosure { border-block-end: 1px solid var(--hairline); }
  .facets__summary {
    display: flex; align-items: center; gap: 6px; min-block-size: 44px;
    padding: 10px var(--s-4); font: 500 var(--t-ui)/var(--t-ui-lh) var(--f-sans);
  }
  .facets__group { flex-direction: column; align-items: stretch; padding: 0 var(--s-4) var(--s-3); }
}
```

Il `<summary>` nomina il facet attivo («État · En attente»), quindi il filtro in vigore è leggibile
**senza aprire**. Misurato a 390: chiuso il primo dato risale a `y = 220` invece di `y = 380`.

**Il masthead rende i controlli solo oltre 8 righe** (`{% if rows|length > 8 %}`): un registro di tre
pezze non si presenta come una console. Sotto 8 righe il frontespizio è rubrica + nome + conteggio,
e basta. **La densità non è più un commutatore.** `localStorage` sparisce: `data-density="compact"`
è un attributo che il **template** pone sulle superfici di back-office, non una preferenza che
l'utente cambia e che poi viaggia in un permalink condiviso (GAP 11 chiuso per soppressione). Un
commutatore di densità con memoria locale è un tic da SaaS, e il revisore ha ragione.

**`.facets__permalink`** copia l'indirizzo corrente negli appunti (`navigator.clipboard`, fallback
`<input readonly>` selezionato). Le **viste salvate restano RIFIUTATE in V1**, con la ragione scritta:
una vista salvata è stato lato server — un modello, una migrazione, permessi per ruolo, cancellazione
GDPR — e il mandato vieta di toccare il contratto dati. In cambio, l'URL *è* la vista. Correzione al
round 1: i parametri GET realmente disponibili sono **il facet (se la vista lo legge) e `page`**, non
l'ordinamento (§0.6).

**`.finder`** (ricerca), e il suo `<form>` che apre e chiude dentro `.reg__masthead` (MUST-FIX 9):

```html
<form class="finder" method="get" role="search">
  <label class="finder__label" for="reg-q">{% translate "Chercher dans ce registre" %}</label>
  <span class="finder__box">
    {% svg_icon "search" "finder__glyph" %}
    <input class="finder__input" id="reg-q" name="q" type="search" value="{{ query }}">
    {% if query %}<button class="finder__clear" type="submit" name="q" value="">…</button>{% endif %}
  </span>
</form>
```

```css
.finder { display: grid; gap: var(--s-1); }
.finder__label { font: 500 var(--t-ui)/var(--t-ui-lh) var(--f-sans); color: var(--ink-2); }
.finder__box { position: relative; display: flex; align-items: center; }
.finder__input {
  block-size: 48px; inline-size: 100%;                 /* DS §10: 48, oggi 44 */
  padding-inline: 44px 48px;
  background: var(--min-3);                            /* oggi --min-0: il colore della pagina */
  border: 1px solid var(--hairline-strong);            /* 3.74:1 su --min-3 — corretto, era 3.59 */
  border-radius: var(--radius-control);
  font: 400 var(--t-body)/1.25 var(--f-sans); color: var(--ink);
}
.finder__glyph { position: absolute; inset-inline-start: 12px; inline-size: 20px; block-size: 20px;
                 color: var(--ink-3); pointer-events: none; }
.finder__clear { position: absolute; inset-inline-end: 2px; inline-size: 44px; block-size: 44px;
                 border: 0; background: transparent; }
```

**La regione viva, unica per pagina.** È `.reg__count` nel frontespizio:
`<span class="reg__count" role="status" aria-live="polite">`. Serve conteggio, filtri e paginazione
insieme (il pattern letto nel candidato 1: una sola regione, sempre renderizzata, «so repeated
counts announce reliably»). **La frase resta la grammatica di dominio già revisionata**, non
vocabolario da foglio di calcolo: `register.html` dice oggi «3 pièces demandées · 1 sur 3 validées ·
2 en attente», e continua a dirlo. Il round 1 proponeva «7 lignes · 3 en attente»: «lignes» esce. Il
misuratore a tacche disegna esattamente quel conteggio — N tacche per N pezze — e sparisce oltre 12
elementi, dove smetterebbe di essere contabile a colpo d'occhio.

### 4.4 Stati vuoti — `.void`

Un sistema solo. `.empty-state` (riquadro tratteggiato centrato, titolo 13 px sopra corpo 17 px,
nessuna azione) viene eliminato; `templates/components/empty_state.html` rende `.void` mantenendo lo
stesso contratto di inclusione (`title`, `text`, `action_label`, `action_url`), così i 21 template
che lo includono non cambiano. `.empty` (register.css, 31 template) rende lo stesso `.void`.

```css
.void {
  display: grid; gap: var(--s-3);
  max-inline-size: var(--measure-gloss);       /* 50ch */
  padding-block: var(--s-6);
  border-block-start: 1px solid var(--hairline);   /* una hairline, DS §9.6 */
}
.void__glyph { inline-size: 64px; block-size: 64px; color: var(--hairline-strong); }
.void__title { margin: 0; font: 400 var(--t-entry)/var(--t-entry-lh) var(--f-serif); color: var(--ink); }
.void__text  { margin: 0; font: 400 var(--t-body)/var(--t-body-lh) var(--f-sans); color: var(--ink-2); }
.void__action {
  justify-self: start; display: inline-flex; align-items: center;
  min-block-size: 48px; padding-inline: var(--s-4);
  border: 1px solid var(--hairline-strong); border-radius: var(--radius-control);
  color: var(--ink); text-decoration: none; font: 500 var(--t-ui)/var(--t-ui-lh) var(--f-sans);
}
```

Anatomia: filetto 1 px `--hairline` · glifo **arco + gradini** a **64 px**, tratto 1,25,
`--hairline-strong` · titolo `--t-entry` 22/28 in `--ink` — **più grande del proprio corpo**, cioè
l'inverso del difetto 1.6 · frase `--t-body` che nomina **chi** riempie la regione e **quando** (le
frasi esistenti sono revisionate legalmente e restano **verbatim**) · azione risolutiva inline come
controllo SECONDARY di 48 px · `role="status"` · allineato alla lettura, **mai** centrato, **mai**
un'illustrazione a colori.

**Markup, per esteso.** `templates/components/empty_state.html` continua a ricevere `title`,
`text`, `action_label`, `action_url` — i 21 siti di chiamata non cambiano — e aggiunge un `kind`
facoltativo (`""`, `"filtered"`, `"restricted"`):

```django
{% load i18n ile_core %}
<div class="void{% if kind %} void--{{ kind }}{% endif %}" role="status">
  {% svg_icon "threshold" "void__glyph" %}
  <h3 class="void__title">{{ title }}</h3>
  <p class="void__text">{{ text }}</p>
  {% if action_url and action_label %}<a class="void__action" href="{{ action_url }}">{{ action_label }}</a>{% endif %}
</div>
```

`templates/documents/partials/register.html` e le trenta altre occorrenze di `<p class="empty">`
passano allo stesso parziale: `{% include "components/empty_state.html" with title=… text=register.empty_text action_label=… action_url=… %}`.
**Le frasi non cambiano di una virgola**: `register.empty_text` e le frasi dei 21 stati vuoti sono
testi revisionati legalmente e restano **verbatim**, come le sei stringhe della riga (§4.2).

**Misura, e una correzione al round 1.** `.void` misura **309 px** a 1440 in una colonna di 976 px,
contro i **274 px** di `.empty-state` misurati nello stesso run. Il round 1 prometteva «≈ 196 px
contro 246»: **falso in entrambi i termini**. `.void` è **più alto di 35 px**, e quei 35 px sono il
glifo portato a 64 px e l'azione risolutiva che oggi manca in due casi su tre. Uno stato vuoto senza
azione è più corto e non serve a niente.

**Tre sottospecie, distinte da una parola nella frase e da nulla più** — nessuna variante cromatica,
nessun riquadro diverso:

| Sottospecie | Quando | Azione | Frase (forma) |
|---|---|---|---|
| `.void` (origine) | la regione non è ancora stata riempita | quella che la riempie, es. «Commencer le questionnaire» | «… se construit à partir de …, elle indiquera …» |
| `.void--filtered` | un facet ha svuotato la lista | **«Effacer les filtres»**, che è il link del facet «Toutes» | «Aucun élément ne correspond à ce filtre.» |
| `.void--restricted` | la regione esiste ma questo ruolo non la vede | nessuna azione risolutiva; un link «Comprendre les rôles» se esiste | la frase **nomina chi la vede**, mai «accès refusé» |

```css
.void--filtered .void__glyph,
.void--restricted .void__glyph { color: var(--hairline-strong); }   /* nessuna differenza di colore */
.void--restricted .void__action { display: none; }
```

Il glifo `icon-threshold` (arco + gradini) va aggiunto allo sprite `static/img/icons.svg`: i 36
simboli attuali non contengono né arco né gradini. È la «grammatica della porta nella piattaforma»
che il DS §6 prescrive esattamente per gli stati vuoti, ed è l'unico disegno nuovo di questa spec.

### 4.5 Caricamento — `.skel`, `.progress`

**Lo scheletro non si muove (MUST-FIX 4).** Niente shimmer, niente banda, niente ciclo. La banda che
attraversa in 1 600 ms era, insieme, una violazione di `MOTION_SYSTEM` §1 (numero inesistente) e §4
(oggetto vivo su una pagina DENSE) **e** il tell di libreria più riconoscibile del documento. Al suo
posto, la rigatura del registro:

```css
.skel { display: grid; }
.skel .skel__row {
  display: grid; grid-template-columns: 1fr 96px 1fr 88px 96px; gap: var(--s-6);
  align-items: center; min-block-size: 56px; padding-inline: 36px var(--s-6);
  border-block-end: 1px solid var(--hairline);
}
.skel__bar { block-size: 12px; background: var(--hairline); }   /* 1.27:1 su --min-1: materia, non testo */
@media (max-width: 47.999rem) {
  .skel .skel__row { grid-template-columns: minmax(0, 1fr); gap: var(--s-2); padding-inline: var(--s-4); }
  .skel .skel__row .skel__bar:nth-child(n+4) { display: none; }
}
```

Quando una regione viene sostituita (facet con JS attivo, paginazione), la regione riceve
`aria-busy="true"` e le righe sono sostituite da **tre** `.skel__row` **dell'altezza di riga
corrente**, misurata prima dello scambio, così la pagina non salta. Compare **solo dopo
`--motion-fast` (180 ms)** di attesa e, una volta comparso, resta almeno **`--motion-slow` (320 ms)**:
due token esistenti, non due numeri nuovi. Al completamento: `aria-busy="false"` e il conteggio
aggiornato nella regione viva.

**`.progress` è determinato o non esiste.**

```css
.progress { block-size: 2px; background: var(--hairline); overflow: hidden; }
.progress__bar { block-size: 100%; background: var(--accent); transform-origin: left;
                 transform: scaleX(0); }
[dir="rtl"] .progress__bar { transform-origin: right; }
```

Per il deposito di una pezza: `scaleX()` guidato dai byte reali di `XMLHttpRequest.upload.onprogress`,
più `<p role="status">Dépôt 3 sur 7 · 1,2 Mo</p>`. Mai una barra finta. Per un `<form>` POST normale,
dove non esiste una frazione reale, **non c'è indicatore**: il bottone prende `aria-busy="true"`,
l'etichetta diventa «Envoi en cours…», il controllo è disabilitato **per attributo**, e il feedback
di attesa è quello del browser. Il filetto indeterminato di 900 ms in ciclo del round 1 era una
finzione e un ciclo: sparisce, e non chiedo nessuna deroga per riaverlo. Nessuno spinner da solo, da
nessuna parte (DS §9.6).

### 4.6 Il sistema di formulari — `.f`

- **`.f__group`** rimpiazza `form__group`, che **non esiste in nessun foglio di stile** e lascia in
  produzione il `2px groove #F0F0F0` del browser: `border: 0; padding: 0; margin-block-end: var(--s-10)`,
  `<legend class="f__legend">` a `--t-band` 32/36 con filetto `--hairline` di chiusura.
- **Campo**: `block-size: 48px` (DS §10; oggi 44), fondo **`--min-3` #FFFFFF** (oggi `--min-0`, il
  colore esatto della pagina), bordo 1 px `--hairline-strong` (**3.74:1** su `--min-3` — cifra
  corretta), `border-radius: var(--radius-control)` 2 px, `padding: 12px 16px`, testo `--t-body` 17.
  `textarea` `min-block-size: 144px`. Misurato sul candidato: **48,0 px**.
- **Etichetta visibile sopra**, `--t-ui` 15/500. **Etichette flottanti RIFIUTATE**: su un modulo
  giuridico l'utente deve poter **rileggere la domanda mentre risponde**, e a zoom 200 % un'etichetta
  francese o araba lunga non entra nel campo.
- **Aiuto** da `--t-caption` 13 a **`--t-small` 14** in `--ink-3` (**5,88:1** su `--min-2`), posto
  **tra etichetta e controllo**: è un'istruzione, non una nota a piè di pagina.
- **Obbligatorio**: l'asterisco color errore (`rgb(143,29,29)` misurato) sparisce. Al suo posto la
  parola «requis» a `--t-caption` `--ink-3` dopo l'etichetta, più `required` sul controllo.

**Contratto d'errore, tre livelli, e il `aria-describedby` che il round 1 non scriveva (GAP 10).**

a) *Controllo* — `[aria-invalid="true"]`, che Django 5.2 scrive già (misurato). Il selettore deve
**vincere la cascata** contro `.form-field input:not([type=checkbox]):not([type=radio]):not([type=file])`,
che ha **(0,4,1)**:

```css
.form-field input[aria-invalid="true"]:not([type="checkbox"]):not([type="radio"]):not([type="file"]),
.f__control[aria-invalid="true"] {
  border: 2px solid var(--err-700);            /* specificità (0,5,1) contro (0,4,1) */
  background: #FEFBFB;
}
```

La correzione durevole è riscrivere la regola di base con `:where(...)`, che azzera la specificità
dei `:not()`; va fatta nel commit che cancella `components.css` L2141–2352, e allora la regola
d'errore torna a (0,2,1) e resta comunque vincente. Lo dico perché l'implementatore non erediti una
guerra di specificità che è già costata un difetto in produzione.

b) *Messaggio* — `<p class="f__error" id="{{ field.auto_id }}_error">` con glifo `icon-warning` di
16 px e testo `--t-small` in `--err-700` (**6,27:1** su `--min-2`). **`role="alert"` viene rimosso da
qui**: oggi il messaggio di campo e il riassunto lo portano entrambi e l'errore è annunciato due
volte. E **l'id del messaggio si accoda a `aria-describedby`** del controllo, insieme all'id
dell'aiuto — il `describedby` composto letto nel candidato 3, che DS §10 richiede:

```django
{# templates/components/form_field.html #}
<input class="f__control" id="{{ field.auto_id }}"
  {% if field.help_text or field.errors %}aria-describedby="{% if field.help_text %}{{ field.auto_id }}_help{% endif %}{% if field.help_text and field.errors %} {% endif %}{% if field.errors %}{{ field.auto_id }}_error{% endif %}"{% endif %}
  {% if field.errors %}aria-invalid="true"{% endif %} …>
```

L'ordine conta: **aiuto prima, errore dopo**, così il lettore di schermo sente l'istruzione e poi che
cosa è andato storto. Se il campo ha più errori, gli id sono elencati tutti, separati da spazio.

c) *Riassunto* — `components/form_errors.html` resta com'è (`role="alert"`, `tabindex="-1"`, fuoco
spostato — misurato funzionante), con due aggiunte: il **conteggio** nel titolo («2 champs à
corriger») e `scroll-margin-block-start: calc(var(--reg-pin) + var(--s-6))`, perché il riassunto
focalizzato non finisca sotto il cromo appiccicoso.

- **Divulgazione progressiva**: `<details class="f__more">` per i gruppi **facoltativi**, aperto
  d'ufficio se uno dei suoi campi è in errore (`{% if %}` di template, nessuna vista toccata). Mai
  per un gruppo obbligatorio, e mai per un fatto già visibile (§4.2). Sul formulario «nouveau besoin»
  (4 249 px, invio a `y = 3 950`) i tre gruppi non obbligatori dietro `<details>` portano il primo
  invio a portata.
- **`.f__actions` appiccicosa** a fondo colonna: `position: sticky; inset-block-end: 0;
  min-block-size: 72px; background: var(--min-2)`, filetto `--hairline` in testa. *Sticky*, non
  `fixed`: non copre mai l'ultimo campo.

### 4.7 Ordine di caricamento e cancellazioni (MUST-FIX 11, e un difetto trovato misurando)

`static/css/v3/data-surfaces.css` entra nella catena di `static/css/main.css` **dopo**
`v3/buttons.css`, e in `templates/base.html` si aggiunge il `<link rel="preload">` corrispondente.

**Ma `main.css` non basta**, ed è il difetto che ho trovato misurando: `templates/portal/base_portal.html`
carica `portal/portal.css` in `{% block extra_head %}`, cioè **dopo** `main.css`. Peggio, il pop-in di
`portal.css` non si può sovrascrivere nemmeno cambiando ordine, perché
`table:has(tbody [data-label]) tr` ha specificità **(0,2,0)** contro la **(0,1,0)** di `.reg__record`.
Misurato: con il candidato caricato per ultimo, il `<tr>` calcolava ancora `display: block` invece di
`display: grid`.

**Quindi il blocco si cancella, nello stesso commit.** Non è opzionale e non è rinviabile:

| File | Righe | Che cosa sparisce |
|---|---|---|
| `apps/portal/static/portal/portal.css` | 297–487 | `.data-table`, `.table-region`, il pop-in e la regola `:has()` invalida |
| `static/css/components.css` | 2624–2653 | `.empty-state` |
| `static/css/components.css` | 2141–2352 | `.form-field` (riscritto con `:where()` come sopra) |
| `apps/documents/static/documents/documents.css` | 159–163 | il rimedio locale `.doc-register .scroll-x { overflow-x: visible }`, che non serve più |
| `static/css/base.css` | 17 | `scroll-padding-block-start` — **dichiarazione morta**: misurato, vince `shell.css:490` |

Test di guardia (§8): nessun selettore del CSS compilato deve contenere `:has(` annidato, e nessuna
regola deve portare i quattro esadecimali legacy.

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` §6

Tutte su `transform` e `opacity`. **Nessun ciclo**, nessuna molla fuori dalle due, nessuna curva
nuova, nessun numero fuori dai quattro token più i due scaglionamenti ammessi da §2 (40–60 ms). Le
voci 1–6 compilano la riga «Tabelle: inserimento/rimozione riga, apertura dettaglio»; la 7 «Stati
vuoti e di caricamento (skeleton)»; la 9 «Piattaforma: caricamento documento → stato».

Ogni `transition` e ogni `@keyframes` di `data-surfaces.css` vive dentro
`@media (prefers-reduced-motion: no-preference)`; fuori da quel blocco il valore è quello finale.
Le proprietà statiche (fondi, bordi, `opacity` di `.reg__head th::after`, `transform: scaleY(1)` del
marcatore in `is-overdue`) stanno **fuori**, così lo stato ridotto non perde niente.

| # | Nome | Funzione | Innesco | Durata / curva | Proprietà | Stato ridotto | Nota di prestazione |
|---|---|---|---|---|---|---|---|
| 1 | `reg/row-insert` | causalità | riga presente dopo uno scambio di regione | `SPRING_SETTLE` (260/30) | `opacity 0→1`, `translateY 8→0` | riga già al valore finale | solo se la regione ha **≤ 24 righe**; oltre, inserimento istantaneo (UI-UX-Pro-Max #5) |
| 2 | `reg/row-remove` | causalità | riga rimossa (filtro, ritiro) | `--motion-fast` 180 · `--ease-in`, poi `SPRING_SETTLE` sui fratelli | `opacity 1→0`, `translateY 0→-8`; fratelli su offset misurato | rimozione immediata | stagger **40 ms** (`MOTION_SYSTEM` §2, minimo della forchetta 40–60), al massimo 8 righe |
| 3 | `reg/filter-change` | stato | facet acceso/spento | `--motion-base` 240 · `--ease-standard` | dissolvenza di `opacity` del conteggio; `scale .8→1` del glifo di spunta | testo aggiornato senza transizione | **le righe non si animano mai** su un cambio di filtro sopra 24 righe: si muove il conteggio, non il dataset |
| 4 | `reg/row-mark` | feedback | puntatore o fuoco sulla riga (`hover: hover`) | `--motion-fast` 180 in · `--motion-instant` 120 out · `--ease-out` / `--ease-in` | `transform: scaleY(0→1)` del marcatore di 3 px | marcatore già a `scaleY(1)` quando la riga è marcata: **nessuna informazione persa** | pseudo-elemento assoluto, 0 layout |
| 5 | `reg/row-expand` | causalità | pressione su `.reg__expand` | `SPRING_SETTLE` | altezza misurata del `<tr>` di dettaglio + `opacity` del contenuto | `hidden` rimosso, nessun moto | `will-change: transform` solo durante l'animazione; tetto **30 righe** nel DOM |
| 6 | `reg/head-pin` | profondità | la sentinella esce dal viewport | `--motion-instant` 120 · `--ease-out` | `opacity 0→1` di `.reg__head th::after` | striscia semplicemente presente da agganciata | **mai `box-shadow` animato**; un `IntersectionObserver` su `.reg__sentinel`, non un listener di scroll |
| 7 | `skel/reveal` | stato | regione con `aria-busy="true"` da più di `--motion-fast` | `--motion-instant` 120 · `--ease-out`, **una volta** | `opacity 0→1` del blocco `.skel` | scheletro presente all'istante | **nessun ciclo**: lo scheletro è fermo. Soglia 180 ms, permanenza minima 320 ms — due token |
| 8 | `f/error-focus` | orientamento | risposta con errori | nessuna animazione sulla scatola | `scrollIntoView({behavior: reducedMotion() ? 'auto' : 'smooth'})`, poi `focus({preventScroll: true})` | salto immediato | `scroll-margin-block-start` evita il ricalcolo sotto il cromo |
| 9 | `f/upload-progress` | feedback | evento `progress` reale dell'XHR | `--motion-instant` 120 · `--ease-standard`, **per aggiornamento** | `transform: scaleX(frazione reale)` di `.progress__bar` | barra al valore corrente, senza transizione; la frase `role="status"` resta | **nessun ciclo**: senza byte reali non c'è barra. Un elemento, `contain: paint` |

**Oggetti vivi su queste pagine: zero.** `MOTION_SYSTEM` §4 assegna zero cicli ambientali a DENSE e a
STANDARD; le pagine RICH di questa famiglia (il cruscotto) spendono il loro budget altrove. Nessuna
voce qui apre un ciclo, quindi non c'è conflitto e non c'è deroga da chiedere.

**Da creare, perché `MOTION_SYSTEM` li dichiara e il codice non li ha (GAP 1 e 2).** Non sono
invenzioni di questa spec: sono clausole normative non ancora scritte, e questa spec è il primo
consumatore che le usa.

```js
// static/js/src/motion.js — aggiunte, con i valori esatti di MOTION_SYSTEM §1
export const SPRING_SETTLE = { stiffness: 260, damping: 30 };  // layout che si riassesta
export const SPRING_FOLLOW = { stiffness: 400, damping: 40 };  // elementi che seguono il puntatore
```

```css
/* static/css/v2/tokens.css — MOTION_SYSTEM §5 lo prescrive, nessun foglio lo definisce */
:root { --dir: 1; }
[dir="rtl"] { --dir: -1; }
```

Tutto passa da `withMotion(fn, settle)`, che è l'unico ingresso e la cui seconda funzione porta allo
stato finale; `matchMedia` viene riletto a ogni chiamata (§3 di `MOTION_SYSTEM`).

---

## 6. ACCESSIBILITÀ E RTL

**Cambia.** `aria-busy` sulla regione in caricamento. **Una** regione `role="status"
aria-live="polite"` per pagina, oggi assente ovunque. `role="alert"` rimosso dal messaggio di campo e
mantenuto solo sul riassunto (fine del doppio annuncio). `aria-describedby` composto [aiuto, errore]
sul controllo (§4.6). `aria-current="true"` sui facet **insieme** a fondo, filetto, peso e glifo di
spunta: mai il colore da solo. `<caption>` obbligatoria su ogni `.reg__table`, e `aria-labelledby`
mantenuto dove già esiste (`dashboard.html:92 → :94`). `role="table|rowgroup|row|columnheader|rowheader|cell"`
scritti esplicitamente nel markup: **non** perché Chromium li perda — misurato, non li perde nemmeno
con `display: block` (§1.5) — ma perché WebKit storicamente sì, e il costo è zero.

**Bersagli, misurati sulla superficie candidata a 390, 768, 1024, 1440: zero elementi sotto
24 × 24 px.** Link di riga da 15 px a **28–40 px** di altezza per 154–310 px di larghezza; facet
**44 px**; svuotamento della ricerca **44 × 44**; espansione **44 × 44**; azione di riga **44 px**
sulla scheda. Oggi, sullo stesso contenuto: **11 elementi sotto 24 px a 1440** e **14 su 14 a 390**.

**Il cromo appiccicoso, misurato invece che assunto (MUST-FIX 11).** L'area riservata **non** usa il
letterhead pubblico: `base_portal.html` sostituisce il blocco `chrome` con `partials/portal_chrome.html`.
L'elemento appiccicoso è `.portal-bar`, e misura:

| | valore misurato |
|---|---|
| `.portal-bar` altezza a 1440 | **70 px** (`position: sticky`, `inset-block-start: 0`, `z-index: 20`) |
| `--chrome-height` risolto a 1440 | 100 px — **non applicabile qui**: è il letterhead pubblico |
| DS §9.1, valore prescritto | 56 px — **il cromo attuale è già fuori spec di 14 px** |
| `scroll-padding-block-start` del documento, 1440 / 390 | **80 px / 72 px** (da `shell.css:490`; `base.css:17` perde la cascata ed è codice morto) |

Quindi: `--reg-pin: 72px` sotto `.page-portal` (70 misurati + 2 px d'aria), `--reg-pin:
var(--chrome-height)` sulle superfici pubbliche. Misurato sul candidato:
`getComputedStyle(th).insetBlockStart` = **72px** a 1440.
`scroll-padding-block-start` del documento **non viene toccato**: 80 px già scavalcano i 70 px della
barra. Quel che serve in più — scavalcare anche la testata appiccicosa della tabella — è
`scroll-margin-block-start: calc(var(--reg-pin) + var(--reg-row))` = **128 px** sulle **celle**, non
sul documento: composto, non in conflitto. Se un giorno la barra scende ai 56 px del DS, `--reg-pin`
scende con lei e nient'altro cambia; un test di frontend misura la barra e `--reg-pin` nello stesso
browser e fallisce se la barra supera il pin.

**Forced-colors.** Le pillole perdono il fondo e tengono `border: 1px solid CanvasText` più il glifo —
nessun `forced-color-adjust: none` qui, la forma non porta informazione. Lo scheletro diventa un
contorno `GrayText`. La testata appiccicosa resta `Canvas` con filetto `CanvasText`. Il marcatore di
riga e il filetto del facet attivo diventano `Highlight`, e `aria-current` continua a portare
l'informazione da solo.

```css
@media (forced-colors: active) {
  .pill { background: Canvas !important; color: CanvasText !important; border: 1px solid CanvasText; }
  .skel__bar { background: Canvas; border: 1px solid GrayText; }
  .reg__head th { background: Canvas; }
  .reg__body th[scope="row"]::after,
  .facet[aria-current="true"] { border-inline-start-color: Highlight; background: Canvas; }
  .reg__head th::after { display: none; }
}
```

**RTL.** Solo proprietà logiche: `inset-inline-start`, `padding-inline`, `border-inline-start`,
`margin-inline`. Oggi la logica direzionale è corretta (misurato in `ar`: overflow orizzontale 0,
`text-transform: none`, `letter-spacing: 0`, `IBM Plex Sans Arabic`) e va preservata.

Non si specchia: i numeri, le date, i riferimenti, il chevron di espansione quando è verticale, il
glifo di spunta. Si specchia: il margine di legatura e il suo filetto (già logici), il marcatore di
riga, il filetto del facet, l'origine di `.progress__bar` (`transform-origin: right` in RTL), le
frecce di paginazione (`icon--flip-rtl`, già in uso).

Difetto da correggere: riferimenti e date devono restare in `--f-mono` **occidentale** dentro
`<span dir="ltr">`, perché oggi ereditano la famiglia araba contro il DS §3.1. Poiché la
sovrapposizione stirata è stata eliminata (MUST-FIX 13), quei `<span>` restano **selezionabili**: una
persona può copiare `103C80FBC6` dal registro, che con l'overlay del round 1 era impossibile.

**HUMAN_QA_REQUIRED.** (a) NVDA e JAWS sulla rimozione del doppio `role="alert"`, sulla regione viva
unica e sul `describedby` composto. (b) VoiceOver iOS **e Safari macOS** sulla scheda-record:
verificare che i ruoli espliciti reggano dove `display: grid` sostituisce `table-row` — in Chromium
153 ho misurato che reggono anche senza, in WebKit va verificato. (c) Zoom 200 % a 320 px sul
frontespizio e sui facet. (d) La testata appiccicosa contro il «trova nella pagina» del browser.
(e) I cinque fondi di pillola più il contorno tratteggiato in Windows High Contrast, in particolare `.pill--blocked` invertita
(AR 2). (f) Se il committente conferma o respinge l'assenza d'immagine su DENSE (§1.0): è una
decisione sua, non mia, e la spec cambia di conseguenza.

---

## 7. PRESTAZIONI

**Byte — misurati, non stimati.**

| | crudo | gzip |
|---|---:|---:|
| `static/css/v3/data-surfaces.css` (build di misura) | 14 146 | **3 179** |
| blocchi cancellati (portal.css 297–487 + components.css 2624–2653 + 2141–2352) | 12 875 | **3 994** |
| **netto sul CSS** | **+1 271** | **−815** |

Il round 1 dichiarava «netto **+1,1 KB**». Misurato, il netto è **−815 byte gzip**: il foglio nuovo
è più denso ma cancella più di quanto aggiunge. `static/js/src/data.js` è più piccolo di quanto
prometteva il round 1, perché non porta più né ordinamento né `localStorage`: il suo budget è un
**tetto**, non una misura — **≤ 2,0 KB gzip**, verificato dal build e fallito in CI se lo supera.
Importa `animate`, `stagger`, `spring`, `inView` dal chunk Motion **già condiviso**, misurato oggi a
**26 143 byte gzip**; `shell.js` misura **613 byte gzip**. Totale per una pagina di dati:
26 143 + ≤ 2 048 + 613 ≈ **28,8 KB gzip**, dentro il tetto di 45 con 16 KB di margine.

**Immagini: zero, e l'argomento è in §1.0, non in una riga.** Un solo simbolo nuovo nello sprite
(`icon-threshold`, ≈ 0,35 KB), che il DS §6 prescrive per gli stati vuoti.

**Paint e layout.** Tutto il moto è `transform`/`opacity`: 0 layout e 0 paint oltre il primo frame
nel pannello Performance. Le due animazioni su altezza misurata (espansione di riga, dettaglio) sono
limitate a 30 righe e portano `will-change: transform` solo mentre corrono. La testata appiccicosa
costa **un** livello di composizione per tabella, e le pagine ne hanno al massimo due. Nessun
`filter`, nessun `box-shadow` animato, nessun `background-position`, **nessun ciclo**.
`transition: all` di `.portal-list__item` viene sostituito da un elenco esplicito.

**I due guadagni, separati (MUST-FIX 10).** Il round 1 li confondeva.

1. **Meno pixel da comporre — dalla scheda-record, non da `content-visibility`.** A 390 il documento
   della checklist passa da **2 837 px a 2 101 px** e il registro da 2 484 a 1 893 px di righe:
   misurato, con `content-visibility` **disattivato**. È il ridisegno che paga.
2. **Meno pittura fuori schermo — da `content-visibility`, e solo dove serve.**
   `.reg[data-long="true"] .reg__record { content-visibility: auto; contain-intrinsic-size: auto 208px }`
   si applica **solo sotto 768** (dove la riga è `display: grid`, misurato) e **solo oltre 24 record**,
   cioè sulle superfici paginate a 20 righe più i casi limite. Sopra 768 la riga è `display:
   table-row` (misurato) e non riceve mai contenimento: applicare il contenimento di dimensione a una
   riga di tabella è esattamente ciò che il revisore teme, e qui non accade. Il valore 208 px è la
   mediana misurata delle schede (190–218 checklist, 238–298 registro) e la parola chiave `auto`
   lascia che il browser ricordi la dimensione reale dopo il primo rendering, così la barra di
   scorrimento non salta. Su nove schede il guadagno non esiste: per questo la soglia.

**CSP.** Tutto è servito da `static/`. Nessun `<style>` in linea, nessun attributo `style=""` nel
markup — e la misura di questa spec è stata presa nelle stesse condizioni, con il foglio candidato
servito come `<link rel="stylesheet">` reale sulla stessa origine del server. Le altezze misurate
sono passate a Motion, che guida la Web Animations API: nessun attributo di stile viene scritto. Dove
occorre una variabile calcolata si usa `element.style.setProperty()` via CSSOM — non è un attributo
`style` analizzato dal parser e non ricade sotto `style-src` — **da verificare comunque contro il
test CSP del progetto prima dell'implementazione**.

---

## 8. RISCHI E TEST DI GUARDIA

| Rischio | Perché sembrerebbe economico | Guardia | Test |
|---|---|---|---|
| **Confetteria di pillole** | Una tinta per stato, su dodici stati, trasformerebbe un registro giuridico in una caramelleria | **Cinque fondi per dodici stati**: attesa, foglio depositato, valido, errore, timbro, più un contorno tratteggiato per «non applicabile». Due coppie condividono deliberatamente un fondo e si distinguono per parola e glifo | test che conta i **fondi distinti** resi su una pagina, non le classi: fallisce oltre cinque |
| **Cromatura da console BI** | Frontespizio + facet + colonne su un registro di tre pezze: strumenti senza materia | Il frontespizio rende i controlli **solo oltre 8 righe**; la densità non è un commutatore ma un attributo di template; l'ordinamento non esiste (§0.6) | `grep localStorage` su `data.js` = 0 |
| **La scheda che perde un fatto giuridico** | Una scheda più corta è più bella | Sei slot nominati, tutti verbatim, tutti **visibili**; nessun fatto oggi visibile finisce dietro una `<details>` | test di rendering che cerca `source_title`, `state_reason`, `Facultative`, `version`, `responsible_note` e la frase bloccata nel DOM a 390 |
| **L'accento che torna su qualcosa di non interattivo** | Il teal è bello anche su una pillola | `--accent` solo su link, CTA primaria, anello di focus e **filetto del facet attivo** (che è un link) | test che cerca `--accent` come `color`/`background` su selettori non interattivi |
| **Un ciclo che rientra da una porta di servizio** | «È solo uno shimmer» | Zero cicli in questo foglio | test che cerca `infinite` e `animation-iteration-count` in `data-surfaces.css` = 0 |
| **Un numero di durata fuori sistema** | 200 ms «sembra giusto» | Solo `--motion-instant/fast/base/slow`, più stagger 40–60 ms | test che conta i letterali `ms` nel CSS compilato di questo foglio |
| **I colori legacy che sopravvivono** | #1E4A85 continuerebbe a far sembrare «DÉPOSÉ» un link | Nessuno dei quattro esiste più | test che cerca `#8f1d1d\|#5e4b14\|#7a4e00\|#1e4a85` nel CSS compilato |
| **Il pop-in che torna da una porta di servizio** | `:has()` annidato è invalido e il browser tace | Il blocco è **cancellato** (§4.7), non coperto | test che passa ogni selettore contenente `:has(` a `document.querySelector()` e fallisce sulla `SyntaxError` |
| **Il raggio del tassello che si allarga** | 6 px «addolcisce» la tabella | `.reg` e `.reg__record` a 0 | `grep radius-tile data-surfaces.css` = 0 |
| **La testata appiccicosa che si scolla dalla barra** | La barra cresce di una riga e il pin resta | `--reg-pin` ≥ altezza misurata di `.portal-bar` | test di browser che misura entrambi e fallisce se la barra supera il pin |
| **Nascondere una colonna** | Riordinare o nascondere può far dire al fascicolo ciò che non dice | Nascondere colonne è **vietato** sul registro pezze: le cinque colonne sono il contratto | test che conta i `<th scope="col">` resi |
