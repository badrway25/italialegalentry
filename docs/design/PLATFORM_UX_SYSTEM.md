# PLATFORM UX SYSTEM — la superficie autenticata

Versione 1.0 · 21 settembre 2026 · Direzione artistica **A — «Le Registre»**

Questo documento descrive il sistema della **piattaforma**, non del sito pubblico. I due condividono
i token e i ruoli tipografici e **non condividono nient'altro**: chrome, navigazione, densità, ritmo
e vocabolario delle componenti sono distinti, perché rispondono a domande diverse.

---

## 1. La separazione, e perché è netta

Il sito pubblico risponde a **«che cos'è questo progetto e posso fidarmi?»**. La piattaforma risponde
a **«dove sono, che cosa devo fare, chi è responsabile e che cosa succede dopo?»**.

La versione precedente rendeva l'area riservata dentro il guscio pubblico: barra istituzionale,
mega-menu a sette sezioni e footer completo restavano presenti dopo l'accesso, con il lavoro vero
parcheggiato in una barra laterale sotto. Il Design Council le ha dato 3/10 e ha osservato che
falliva tutte e quattro le domande di accettazione del committente. Una persona che aveva effettuato
l'accesso non poteva vedere dove si trovava.

**Regola.** La piattaforma non riusa il mega-menu pubblico. Non riusa il footer pubblico. Non riusa
la densità del sito pubblico.

| | Sito pubblico | Piattaforma |
|---|---|---|
| Chrome | barra istituzionale + mega-menu 7 sezioni | `partials/portal_chrome.html`: marchio, contesto, account, lingua |
| Navigazione | orizzontale, per pubblico | laterale, per compito (`components/local_nav.html`) |
| Footer | quattro colonne, mappa del sito | quattro righe: legale e via d'uscita |
| Ritmo verticale | rank A 96 px, B 48, C 24, D 12 | costante `--s-8` fra sezioni |
| Contenitore | 1176 → 1320 → 1440 | `.portal` a due tracce, `minmax(0, 15rem)` + `minmax(0, 1fr)` |
| Ground | `--paper` | `--paper` con fasce `--paper-deep` per le procedure |

---

## 2. Le tre regioni persistenti

Nell'ordine in cui compaiono, e nell'ordine in cui un lettore ne ha bisogno.

### 2.1 La barra di piattaforma

Marchio, **contesto corrente** (il riferimento del fascicolo, quando ce n'è uno), account, lingua.
Il contesto è l'unica cosa nuova rispetto a una barra ordinaria, ed è ciò che permette di navigare
dentro un fascicolo senza perdere di vista quale.

### 2.2 L'intestazione del fascicolo

Una fascia sul ground di procedura (`--paper-deep`), stabile mentre si naviga dentro il fascicolo.
Risponde a quattro delle nove domande di accettazione **senza scorrere**: dove sono, qual è il mio
obiettivo, in che stato è il fascicolo, chi ne è responsabile.

Non è un'intestazione di pagina: la pagina ha il proprio `h1` sopra. La distinzione è stata imparata
a caro prezzo — quando l'intestazione prescritta era mostrata solo a chi *non* aveva un fascicolo,
ogni persona che ne possedeva uno riceveva una pagina **senza alcun `h1`**, in tutte e quattro le
lingue.

### 2.3 L'azione successiva

**Una** priorità, mai un elenco di cinque. Calcolata da `cases.services.next_action` con un ordine di
precedenza dichiarato: un esito ostativo, poi un requisito scaduto, poi il più prossimo, poi il primo
aperto, poi lo stato stesso.

Porta sempre il **responsabile**. Se l'azione non spetta alla persona, lo dice: un passo che il
consolato deve compiere non è un compito che l'interessato possa eseguire, e mostrarlo come tale ne
sprecherebbe il tempo e ne fraintenderebbe la responsabilità.

---

## 3. Il vocabolario delle componenti

Dieci componenti, nessuna delle quali è una «card». Tutte in `static/css/register.css`, tutte
condivise fra sito e piattaforma, perché la grammatica è una sola.

| Componente | Che cosa afferma | Dove |
|---|---|---|
| `.folio` | Questa sezione ha una **posizione** in una sequenza | ogni sezione di piattaforma |
| `.register` / `.entry` | Un elenco di cose con ordinale, titolo, glossa e attore | fascicoli, proposte, corsi, richieste |
| `.sequence` | Un percorso con una tappa corrente e un attraversamento | ciclo di vita del fascicolo |
| `.data-table` | Fatti in colonne, sempre con intestazione, mai una cella vuota | checklist, pezzi, moduli |
| `.state` | Uno stato, come **parola**, con un filo di 4 px | ovunque ci sia uno stato |
| `.outcome` | Un esito, come parola a dimensione di titolo | pre-valutazione |
| `.sources` | L'elenco numerato dei fondamenti | esito, pezzi |
| `.note` | Una precisazione, sotto un filo | disclaimer, avvertenze |
| `.gloss` | Un inciso accanto alla cosa che spiega | conteggi, «ciò che non chiediamo» |
| `.empty` | Un filo e una frase che nomina chi riempie e quando | ogni regione vuota |

### 3.1 Ciò che il sistema rifiuta

- **Nessuna percentuale.** «4 elementi su 11 completati» è verificabile; una barra al 62% non lo è.
- **Nessuna card.** Un rettangolo con ombra e raggio dice «sono un modulo software». Una voce di
  registro dice «sono una cosa con una posizione, un titolo e un responsabile».
- **Nessuna icona al posto di una parola.** Uno stato è una parola.
- **Nessun colore da solo.** Ogni stato ha parola + filo; il colore è la terza informazione.
- **Nessun dato finto** per far sembrare popolata una schermata. Una regione vuota è un filo e una
  frase.

---

## 4. La regione vuota

Il difetto più frequente nella versione precedente: cinque riquadri tratteggiati di peso uguale,
quattro vuoti, ciascuno con un'icona al centro. Dicevano quali moduli ha il software.

**La forma corretta**, applicata ovunque:

```
────────────────────────────────────────
Vous n’avez pas encore de dossier. Il s’en ouvre un lorsque vous terminez le
questionnaire d’orientation, et il conserve alors votre résultat, votre liste
de pièces et les personnes responsables de chaque étape.  → Commencer l’orientation
```

Un filo, una frase che nomina **chi** riempie la regione e **quando**, e l'azione risolutiva in
linea. Non un riquadro, non un'icona, non un invito generico.

---

## 5. Densità e ritmo

La piattaforma è più densa del sito pubblico, perché chi la usa sta lavorando.

| Misura | Valore |
|---|---|
| Interlinea di prosa | 28 px (32 px in arabo) |
| Spazio fra sezioni | `--s-8` (32 px), costante |
| Spazio interno di una riga di registro | `--s-3` verticale |
| Larghezza massima di una glossa | `--measure-gloss` (50ch) |
| Colonna laterale | 15rem, sticky sopra 64rem, in flusso sotto |

**`min-inline-size: 0` sulle due tracce.** La dimensione minima automatica di un elemento di griglia
è il suo contenuto, non zero: senza questa riga una tabella larga spinge l'intera colonna fuori dal
viewport e **la pagina** scorre lateralmente invece della tabella.

---

## 6. Tabelle larghe su telefono

WCAG 2.2 §1.4.10 vieta lo scorrimento bidimensionale ed eccettua il contenuto che richiede davvero
una disposizione bidimensionale — una tabella di dati lo richiede. L'eccezione non autorizza a
ignorare il problema:

```html
<div class="table-region" role="region" aria-label="…" tabindex="0">
  <table class="data-table"> … </table>
</div>
```

Regione **etichettata** e **focalizzabile**, quindi raggiungibile e scorribile da tastiera, con il
bordo di margine disegnato perché un lettore vedente veda che c'è dell'altro.

**Nessuna colonna viene eliminata sul telefono.** Ogni colonna porta un fatto necessario — che cosa
è richiesto, chi deve agire, in base a quale disposizione, entro quando — e nascondere la
disposizione sul telefono la nasconderebbe proprio ai lettori che più probabilmente vi si trovano.

---

## 7. Arabo e RTL

Non è un interruttore di foglio di stile.

| Aspetto | Trattamento |
|---|---|
| Direzione | `dir="rtl"` reale sull'elemento radice |
| Carattere | `--font-display-ar` / `--font-ui-ar` (Noto Naskh Arabic, IBM Plex Sans Arabic) |
| Interlinea di prosa | 32 px invece di 28 |
| Crenatura | azzerata; i maiuscoletti e lo spaziato non si applicano |
| Proprietà | solo logiche: `inset-inline-start`, `padding-inline`, `border-block-end` |
| Cifre | occidentali, sempre — una data accanto a un identificativo latino deve restare leggibile |

**Verifica continua:** `scripts/qa_rtl_check.py` apre ogni pagina autenticata in arabo a 390 e
1440 px e controlla direzione, scorrimento **reale**, `h1` unico, proprietà di direzione fisica,
regioni di scorrimento etichettate, errori di console.

Una nota di metodo che è costata tempo: `documentElement.scrollWidth` **non** è un segnale di
overflow in RTL. Chromium riporta 445 px contro un viewport di 390 px per una pagina il cui scroller
annidato ritaglia correttamente e che non scorre affatto.

---

## 8. Miglioramento progressivo

Nessuna pagina della piattaforma richiede JavaScript per funzionare. In totale il progetto ne ha
**567 righe**, di cui la maggior parte nel wizard di orientamento, e ogni funzione ha un percorso
senza script.

| Funzione | Senza JS |
|---|---|
| Questionario | un POST per domanda, con il proprio URL |
| Checklist | un form per riga |
| Transizione di stato | un form |
| Navigazione | link |
| Lingua | form `set_language` |

---

## 9. Gli accessi per ruolo

L'instradamento dopo l'accesso non è più uniforme: ogni ruolo arriva sulla superficie in cui lavora.

| Ruolo | Destinazione |
|---|---|
| Soggetto autorizzato | `selection:workspace` |
| Professionista | `helpdesk:queue` |
| Impresa | `companies:dashboard` |
| Ente di formazione | `academy:catalogue` |
| Tutti gli altri | `portal:dashboard` |

La navigazione laterale è costruita da `portal.services.navigation` e non mostra ciò che il ruolo non
può aprire.

---

## 10. Che cosa resta da fare

| Punto | Stato |
|---|---|
| Passaggio con un lettore di schermo reale | **non fatto**, e non sostituibile da un test automatico |
| `components.css` a 3045 righe | eredità del sito pubblico; la piattaforma non vi aggiunge |
| Modulo post-ingresso | gli stati esistono, il contenuto no |
| Workspace università e ricerca | non costruito |
