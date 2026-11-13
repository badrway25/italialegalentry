# La vetrina del design system — `/_design/`

Stato: **in servizio**, solo in sviluppo · Creata il 24 settembre 2026 · Direttiva §53

---

## 1. Che cos'è, e perché non esiste in produzione

Una sola pagina che rende ogni superficie del sistema una accanto all'altra: le cinque varianti di
bottone con le loro tre misure e i loro stati, le sette pastiglie, i sei messaggi, il campo di
modulo nel suo stato d'errore, la modale, la tabella, lo stato vuoto, le trentasei icone, i
quarantaquattro colori con il loro valore, le undici misure tipografiche alla loro grandezza reale.

Prima non esisteva. Verificare una modifica a `.btn--primary` — letto da 62 bottoni in 54 template —
voleva dire visitare una dozzina di pagine, metà delle quali dietro una sessione autenticata con un
fascicolo nello stato giusto. Il risultato prevedibile: le modifiche si verificavano su una pagina
sola, e le incoerenze fra superfici restavano invisibili finché non le notava il committente.

**Il cancello è doppio.**

| Strato | Che cosa garantisce |
|---|---|
| `config/urls.py`, dentro `if settings.DEBUG:` | con DEBUG spento il modulo `core.dev` **non viene mai importato**: non è una rotta che risponde 404, è codice che non è nel processo |
| `core.dev.design_showcase`, `if not settings.DEBUG: raise Http404` | un URLconf è un file, e i file si modificano |
| `static/css/dev/showcase.css` fuori da `main.css` | nessun visitatore di produzione scarica un byte di questo foglio di stile |

I tre vincoli sono verificati da `tests/frontend/test_design_showcase.py` (11 test) e da
`test_design_docs.py::test_the_dev_stylesheet_stays_out_of_the_production_cascade`.

## 2. Due scelte che vale la pena tenere

**I valori dei colori sono letti, non copiati.** La vista analizza `static/css/v2/tokens.css` a
ogni richiesta: l'esadecimale scritto sotto un quadrato è quello che il browser dipinge. Una
vetrina che ridichiara la palette in Python è una seconda fonte di verità, e le seconde fonti di
verità divergono.

**La pagina controlla la propria copertura.** La CSP è `style-src 'self'`: nessun attributo
`style=""` può portare un colore, e nessuna funzionalità CSS trasforma il *valore* di un attributo
nel *nome* di una proprietà personalizzata. Ogni campione ha quindi bisogno di una regola
`[data-swatch="…"]` scritta a mano. Quella duplicazione marcisce, perciò la vista confronta i due
file e stampa in cima alla pagina i token rimasti senza quadrato. Tre test tengono lo stesso
invariante in CI, nelle due direzioni: token senza regola, e regola senza token.

## 3. Che cosa ha trovato il primo giorno

Tutto misurato in Google Chrome Stable 153.0.8010.53, finestra visibile, su `http://127.0.0.1:8770/_design/`.

### 3.1 `success` è identico a `info` — ed è voluto, e per poco non l'ho «corretto»

| | sfondo | testo | filetto |
|---|---|---|---|
| `badge--info` | `rgb(232,237,244)` | `rgb(30,74,133)` | `rgb(95,132,181)` |
| `badge--success` | `rgb(232,237,244)` | `rgb(30,74,133)` | `rgb(95,132,181)` |
| `notice--info` | `rgb(232,237,244)` | `rgb(21,34,42)` | `rgb(95,132,181)` |
| `notice--success` | `rgb(232,237,244)` | `rgb(21,34,42)` | `rgb(95,132,181)` |

Byte per byte gli stessi colori. Messi in fila nella vetrina sembrano un difetto evidente, e avevo
già scelto il verde sostitutivo e calcolato i suoi rapporti di contrasto — `#0c5535` su `#dcefe4`,
7,40:1, la stessa aria che l'azzurro dà a `info`. Poi ho aperto `static/css/tokens.css` e ho letto
le tre righe di commento sopra la terna:

> No green means "approved". A finished step is TRANSMIS or CLOS: a fact about the file, never a
> verdict. Same reasoning as the absent `eligible` outcome in the domain — this platform approves
> nothing.

La regola è scritta in tre punti indipendenti, e regge:

| Dove | Che cosa dice |
|---|---|
| `static/css/tokens.css` §STATE | il commento qui sopra |
| `docs/design/DESIGN_SYSTEM_2026.md` §4.3, §3.7 e la tabella degli anti-pattern | «non esiste `--state-ok-*`: la terna si chiama `--state-done-*` ed è **blu**» |
| `apps/rules/models.py` | gli esiti del dominio sono cinque e `eligible` non c'è, deliberatamente |

Lo shim `--color-success-*` punta sulla terna blu **apposta**, perché un componente che si chiama
ancora «success» non possa dipingere di verde. Dipingere di verde «la sua domanda è stata accolta»
sarebbe comunicare un verdetto che questa piattaforma non ha l'autorità di dare, e la direttiva di
rebase §2 vieta esplicitamente di toccare il significato dei flussi.

**Quindi il colore resta.** Il difetto reale è un altro, ed è di vocabolario: le classi si chiamano
`badge--success` e `notice--success`, nomi che sopravvivono al sistema precedente e che invitano
esattamente all'errore che stavo per fare. Il CSS non porta il commento; solo i token lo portano.
Da decidere nella revisione: rinominare in `--done` con alias temporaneo, oppure scrivere la regola
accanto alle classi. Nel frattempo la vetrina la spiega, in pagina, fra le pastiglie e i messaggi:
è il punto esatto in cui la confusione nasce.

**Conferma indipendente, arrivata lo stesso pomeriggio.** La specifica `badges.md`, riscritta dal
giro di riparazione mentre scrivevo questo paragrafo, ha commesso e poi ritirato lo stesso errore.
Il suo §4.1 si intitola «La decisione giuridica che governa tutto il resto: nessun verde», cita il
commento di `tokens.css` per esteso e dice del proprio primo giro: *«assegnava `--ok-700` (verde)
al registro conforme e trattava `--state-done-fg == --state-info-fg` come un difetto: rovesciava
una decisione scritta senza citarla»*.

E risolve il problema vero — i due stati indistinguibili — **senza colore**: *conforme* prende un
filetto di chiusura sotto il corpo e una spunta, *neutro* non prende né l'uno né l'altra, «senza
che nessuno dei due diventi un verdetto». Sostituisce anche il vocabolario ereditato con sette
registri — neutro, attesa, azione, conforme, rifiuto, nullo, sigillo — che è esattamente il
rimedio di cui sopra: i nomi `success` e `info` spariscono, e con loro l'invito all'errore.

### 3.2 La palette V2 dichiara un verde che la regola vieta

`static/css/v2/tokens.css` riga 51 introduce una famiglia verde con l'etichetta «regular, done,
valid»:

```
--ok-700: #1e7a4d;   --ok-100: #dcefe4;   --ok-300: #7ccfa0;   /* regular, done, valid */
```

Nessun componente la legge — quattro occorrenze in tutto il progetto, tre delle quali sono i
campioni di questa vetrina e la quarta è un alias in `bridge.css`. È quindi innocua oggi, e carica
domani: è il verde «done» che §4.3 dichiara inesistente, pronto per essere collegato da chiunque
guardi la palette senza leggere il documento.

In più, come coppia testo/fondo non regge la misura: `--ok-700` su `--ok-100` dà **4,44:1**, sotto
il minimo di 4,5 per un testo. Se un giorno qualcuno la collegasse, fallirebbe anche il contrasto.

E la contraddizione è esplicita, non implicita. `DESIGN_SYSTEM_V2` §1.3 regola 3 dice
«**Verde solo semantico** (regolare, terminato, valido)»; `DESIGN_SYSTEM_2026` §4.3 dice che
nessun colore può mai significare «approvato» e che per questo non esiste `--state-ok-*`. Le due
frasi non possono valere insieme: «terminato, valido» in verde è esattamente ciò che la prima
vieta.

Da decidere nella revisione V3, e va deciso da chi ha l'autorità sul significato dei flussi, non
dal colore: cancellare la terna, oppure ridocumentarla per ciò che può significare senza violare
la regola — «regolare» nel senso di conforme alla via legale, mai «approvato» — e correggerne
comunque il rapporto di contrasto.

### 3.3 `warning` e `pending` si distinguono per un margine che nessuno vede

Sfondi `rgb(250,240,223)` contro `rgb(244,238,220)`; filetti `rgb(168,130,50)` contro
`rgb(160,138,70)`. Distinti nel codice, indistinguibili sullo schermo. Qui nessuna regola di
dominio impone l'identità — «avvertenza» e «in attesa» sono due cose diverse e devono sembrarlo —
quindi è materia legittima per la specifica delle pastiglie. Il valore della vetrina è che la
differenza si misura in un colpo d'occhio invece che confrontando due pagine.

### 3.4 `badge--primary` è dipinto con il navy del marchio — chiuso la sera stessa

`rgb(15,37,71)` = `#0F2547` = `--brand-navy`, per la catena
`--color-primary-900` → `--navy` → `--brand-navy`. La regola non lascia margine: `DESIGN_SYSTEM_V2`
§1.3 regola 4, per intero, è «**Il tricolore vive solo nel marchio.** Nessun altro elemento usa
`--brand-*`.»

È la stessa catena già corretta sul bottone principale il 23 settembre, ma l'argomento è diverso e
va detto con precisione: là la regola operativa era la 1 (un solo accento interattivo) perché una
CTA è interattiva. Una pastiglia non lo è, quindi la regola 1 non la tocca; la tocca la 4, che
vieta `--brand-*` fuori dal marchio a prescindere dall'interazione.

**Chiuso** da `static/css/v3/chip.css`: `primary` → registro *neutro*, filetto `--ink-2`, parola
`--ink`. Il navy non compare più in nessuna pastiglia (misurato: sette `kind`, nessuna marca fuori
da `--ink-2`, `--ink`, `--pending-700`, `--err-700`).

### 3.5 Su fondo scuro, `secondary` e `ghost` sono lo stesso bottone

| | sfondo | testo | bordo | raggio | spaziatura | altezza |
|---|---|---|---|---|---|---|
| `.btn--inverse.btn--secondary` | trasparente | `rgb(238,242,241)` | `1px rgba(255,255,255,.55)` | 2px | 8/24 | 44px |
| `.btn--inverse.btn--ghost` | trasparente | `rgb(238,242,241)` | `1px rgba(255,255,255,.55)` | 2px | 8/24 | 44px |

Causa: in `components.css` `.btn--inverse` (riga 98) ha la stessa specificità di `.btn--ghost`
(riga 73) ed è dichiarato dopo, quindi sovrascrive l'unica proprietà che distingueva il ghost
(`--btn-border: transparent`). `.btn--inverse.btn--primary` esiste già a riga 106 proprio per
ripristinare una distinzione persa allo stesso modo; `ghost` non ha mai ricevuto lo stesso
trattamento.

Inoltre `.btn--ghost` su carta prende `--btn-fg: var(--color-primary-900)` → `rgb(15,37,71)`: di
nuovo il navy del marchio, questa volta come colore di testo di un comando interattivo — e qui,
trattandosi di un comando, vale la regola 1 oltre alla 4.

**Difetto latente, non attivo — poi chiuso lo stesso giorno.** Contato nei template: `btn--ghost`
compare quattro volte, `btn--inverse` otto, e l'unico punto che le combina era questa vetrina.
Non ho scritto una regola ad hoc: il sistema completo dei bottoni (`static/css/v3/buttons.css`,
sera del 24 settembre) dichiara la mezzanotte per contesto e tratta `.btn--inverse` come sinonimo,
e in quel sistema il secondario ha superficie `--mid-3` e bordo mentre il discreto non ha né l'una
né l'altro. Misurato dopo: secondario scuro `#1b2f3a` con bordo `#708087`, discreto scuro
trasparente con lavaggio `--mid-2` in hover. Il navy del marchio non compare più in nessun bottone.

### 3.6 Il `data-label` delle tabelle non è letto da nessuna regola

Ogni cella di `.account-table` porta un `data-label` con l'intestazione della sua colonna —
markup il cui unico scopo è un ripiegamento in schede su schermo stretto. **Nessun foglio di stile
del progetto contiene la stringa `data-label`.** Misurato a 320 px: la tabella resta una tabella,
larga 355 px dentro una colonna di 280, e scorre lateralmente dentro `.scroll-x`. Da decidere
nella revisione delle tabelle: scrivere il ripiegamento, oppure togliere l'attributo.

### 3.7 L'elevazione: quello che è chiuso, quello che è aperto, e una domanda senza risposta

Misurato: la carta ha `box-shadow: none`. Nel codice, `_legacy-tokens.css` azzera i quattro token
storici, e `components.css` — menu, `dialog`, pannelli, carte — chiede ancora l'elevazione con
quei nomi in sette punti, che risolvono tutti a nulla.

Anche qui la prima lettura era troppo larga, e correggerla è stata la terza volta in questa
sessione. `DESIGN_SYSTEM_V2` §7 non spegne le ombre: le lega alla **modalità di pagina**.

| Modo | Ombre |
|---|---|
| IMMERSIVE, RICH | nessun limite dichiarato |
| STANDARD | vietate «oltre il ruolo 2» → `--shadow-2` è ammessa |
| DENSE (fascicolo, liste, tabelle, back-office) | **vietate** |
| LEGAL | nessun moto decorativo |

Quindi un fascicolo piatto è conforme, non difettoso. Restano però tre cose vere:

1. **`--shadow-5` non è collegata in nessun punto.** Zero usi. §2 la definisce come il livello 5,
   «overlay: drawer, dialog, palette». Le sovrapposizioni esistono su pagine di ogni modalità.
2. **`components.css` è ancora sullo shim.** È il cancello aperto **G-26**, già registrato nel
   documento V1, e riguarda tutta la libreria, non una superficie.
3. **Una domanda che il documento non risolve: una sovrapposizione prende la modalità della pagina
   che la ospita, o il proprio livello?** Se una modale aperta da un fascicolo è DENSE, non può
   avere ombra e non si stacca dal fondo; se è livello 5, deve averla.

Il punto 3 non è teorico: la riparazione della specifica `case-file`, in corso mentre scrivo, ha
incontrato esattamente questa ambiguità e l'ha risolta **eliminando il `<dialog>`** — «abandoning
the `<dialog>` removed the last overlay that would have justified `--shadow-5`». È una risposta
difendibile, ma è una modifica di prodotto fatta per sciogliere un'ambiguità di documento, e la
decisione non spetta a chi scrive il CSS. Da portare al committente insieme al resto.

Questo tocca un punto preciso del rilievo — *popup, modale e cassetto non professionali*. La causa
non è che siano disegnati male: è che il livello che dovrebbe distinguerli dal fondo non è mai
stato collegato, e la regola che direbbe se gli spetta è ambigua.

### 3.8 Le pastiglie di stato sono squadrate, il sistema le vuole tonde — superato per decisione

`DESIGN_SYSTEM_V2` §2, ultima riga: «Raggi: 0 sui capitoli e sui fogli, 2 px sui controlli, 6 px
sul tassello del marchio, **999 sulle pillole di stato**. Nessun altro.» Misurato:
`border-radius: 0px` su `.badge`, altezza 24 px, corpo 13 px. Anche qui lo shim decide:
`--radius-pill: var(--radius-control)`, con il commento «una pillola non è una forma che questo
sistema ha» — vera sotto V1, revocata da V2.

**Superato**, non corretto: la specifica delle pastiglie (round 3) decide 2 px sul lato finale e 0
sul filetto — una vidimazione, non una pillola — e `chip.css` la implementa così. V2 §2 va
aggiornato su questo punto quando la palette viene riconciliata.

### 3.9 Due difetti della vetrina stessa, trovati e corretti subito

- **Cinque comandi senza etichetta.** Rendere lo stesso modulo due volte sulla stessa pagina dà a
  entrambe le copie gli stessi `id`, e `<label for="id_email">` si lega al **primo**: tutti i campi
  del secondo modulo perdevano l'etichetta. Corretto con `auto_id="id_err_%s"` (un `prefix`
  avrebbe rinominato anche i campi, e i dati non si sarebbero più legati). Ora sorvegliato da
  `test_no_element_id_appears_twice`.
- **L'àncora finiva sotto l'indice appiccicoso.** `base.css` imposta
  `scroll-padding-block-start` per l'intestazione del sito; questa pagina ne aggiunge una seconda
  sotto. Corretto in `showcase.css`, e l'indice non è più appiccicoso sotto 64 rem, dove
  occuperebbe tre righe su un telefono.

## 4. Dove guardare

```
apps/core/dev.py                     la vista, i dati dimostrativi, il lettore di token
templates/dev/showcase.html          la pagina: include i componenti reali, non li ricopia
static/css/dev/showcase.css          impalcatura + una regola per token (la CSP impone la mano)
tests/frontend/test_design_showcase.py   11 test: assenza, veridicità, copertura
docs/qa/chrome/design-v3/showcase_*.png  schermate Chrome visibile, 1440 × 900
```

Per aprirla: server di sviluppo su 8770, poi `http://127.0.0.1:8770/_design/`.
