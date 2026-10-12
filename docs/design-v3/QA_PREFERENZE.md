# QA sotto le due preferenze che rompono le pagine in silenzio

Strumento: `scripts/qa_chrome_media.py` · Chrome Stable 153.0.8010.53, finestra visibile ·
24 settembre 2026

---

## 1. Che cosa cerca, e perché queste due

**Movimento ridotto.** Un reveal scritto come «parti da opacità 0 e anima fino a 1» non diventa
*fermo* quando si disattivano le animazioni: **sparisce**. L'elemento non viene mai dipinto. È il
modo più comune in cui una pagina diventa inutilizzabile per chi ha impostato la preferenza, e
`DESIGN_SYSTEM_V2` chiede l'opposto — con la preferenza attiva la composizione è **completa** e
ferma. Lo script riporta ogni elemento percepibile rimasto sotto il 10 % di opacità, ogni elemento
spostato di più di 4 px dal suo posto, e ogni animazione ancora in corso.

**Colori forzati.** Il contrasto elevato di Windows sostituisce ogni colore con una coppia di
sistema e **scarta** `background-image` e `box-shadow`. Un comando la cui forma viene solo da un
riempimento non ha più forma: il browser lo dipinge del colore della pagina. Lo script riporta ogni
bottone, pastiglia, campo e carta il cui bordo calcolato resti senza spessore o di stile `none`.

## 2. Risultato

| Pagina | Elementi esaminati | Reveal | Invisibili | Ancora animati | Comandi | Senza forma |
|---|---:|---:|---:|---:|---:|---:|
| `/fr/` | 274 | 3 | 0 | 0 | 2 | 0 |
| `/fr/le-projet/` | 164 | 0 | 0 | 0 | 0 | 0 |
| `/fr/reseau/` | 173 | 0 | 0 | 0 | 0 | 0 |
| `/fr/contact/` | 163 | 0 | 0 | 0 | 2 | 0 |
| `/ar/` (RTL) | 272 | 3 | 0 | 0 | 4 | 0 |
| `/_design/` | 836 | 1 | 0 | 0 | 61 | 0 |

**Nessun rilievo.** 1 882 elementi esaminati con il movimento ridotto, nessuno rimasto invisibile,
nessuna animazione sopravvissuta alla preferenza. 69 comandi sotto i colori forzati, tutti con un
bordo proprio.

Il secondo risultato non è fortuna: è la conseguenza diretta di una scelta di sistema. Un'interfaccia
che separa le superfici con **un filetto** invece che con un riempimento o un'ombra attraversa il
contrasto elevato senza perdere nulla, perché il filetto è esattamente ciò che il contrasto elevato
conserva. La stessa scelta che rende il sito piatto lo rende robusto qui.

Nota su `/fr/contact/`: due soli comandi perché su questa porta il modulo non è pubblicato
(`form-unavailable`, fase 3 chiusa su 8770). Da rimisurare su 8771, dove la fase è aperta.

### 2.1 Gli indicatori disegnati come sfondo di uno pseudo-elemento

`docs/ACCESSIBILITY.md` porta il cancello aperto **G-26**, che afferma: «sotto contrasto elevato di
Windows le barre `aria-current`, i punti d'errore e i filetti dipinti come sfondo di uno
pseudo-elemento spariscono». Il primo controllo di §2 non poteva vederli: guarda il **bordo** dei
comandi, e un filetto disegnato come `background` di un `::before` non è un bordo.

Seconda sonda, che legge ogni pseudo-elemento due volte — una per modalità — e confronta:

| Pagina | Pseudo-elementi esaminati | Perduti |
|---|---:|---:|
| `/fr/` | 16 | 0 |
| `/fr/le-projet/` | 7 | 0 |
| `/ar/` | 16 | 0 |
| `/_design/` | 25 | 0 |

**Sulle pagine pubbliche l'affermazione di G-26 non si riproduce.** E nemmeno su quelle della
piattaforma, misurate la sera stessa con la sessione QA (`qa-person`, server 8771, cookie
consegnato via CDP):

| Pagina (con sessione) | Elementi | Invisibili | Ancora animati | Comandi | Senza forma | Pseudo | Perduti |
|---|---:|---:|---:|---:|---:|---:|---:|
| `/fr/espace-reserve/` (cruscotto, binario con `aria-current`) | 246 | 0 | 0 | 2 | 0 | 12 | 0 |
| `/fr/espace-reserve/mes-documents/` (registro, 11 pastiglie) | 252 | 0 | 0 | 1 | 0 | 14 | 0 |
| `/fr/espace-reserve/dossiers/…/` (fascicolo) | 246 | 0 | 0 | 9 | 0 | 11 | 0 |

I punti d'errore dei moduli sono stati misurati sulla vetrina (`/_design/`, modulo legato a dati
non validi): fra i 25–27 pseudo-elementi esaminati, nessuno perduto. Le tre cose che G-26 nomina
— guida `aria-current`, punti d'errore, filetti dipinti come sfondo di uno pseudo-elemento — sono
tutte misurate e nessuna sparisce. Resta di G-26 la parte sulle ombre di `components.css`, che è
un'altra cosa (§3.7 di SHOWCASE.md), e la prova su Windows reale, che l'emulazione non sostituisce.

## 3. Perché lo strumento non usa Playwright

`connect_over_cdp` si collega all'endpoint del **browser** e poi enumera e aggancia tutti i
bersagli della finestra. Per un browser che Playwright possiede è la cosa giusta; per la finestra
Chrome condivisa e visibile che la direttiva impone di usare, no: quella finestra contiene anche le
schede dell'utente, e una pagina di accesso con quattro iframe hCaptcha è bastata a far smettere di
rispondere l'aggancio. Novanta secondi di timeout, ogni volta, su un browser il cui endpoint HTTP
rispondeva all'istante e il cui websocket completava l'handshake in millisecondi — **misurati
entrambi** prima di concludere.

`scripts/cdp.py` apre **un** websocket verso **una** scheda e non chiede mai al browser degli
altri. Niente in una scheda estranea può bloccarlo, e lui non può disturbare una scheda estranea.
Implementa di RFC 6455 solo quanto serve a CDP: frame client mascherati, le tre forme di lunghezza,
i frame di continuazione (una `Runtime.evaluate` che restituisce una pagina di HTML arriva
frammentata) e un pong per ogni ping. Solo libreria standard, nessuna dipendenza aggiunta.

## 4. Quattro difetti nella sonda stessa

Tre difetti su quattro rendevano il risultato **più pulito di quanto fosse lecito credere**, ed è
la ragione per cui `tests/frontend/test_forced_colors_probe.py` esiste: un rilevatore il cui ramo
di scoperta non è mai stato eseguito non è una prova di niente. Otto test lo pilotano con letture
sintetiche, compresa quella che capita davvero nel browser.

1. **`a.skip-link` a y −104.** Il link di salto *deve* stare fuori schermo finché non riceve il
   fuoco. Ora la sonda salta gli elementi posizionati in modo assoluto o fisso il cui rettangolo è
   interamente fuori dal viewport.
2. **`menu-in-end`, durata `1e-05s`.** L'idioma usuale per il movimento ridotto non porta la durata
   a `0s` ma a un capello sopra, così che `animationend` continui a scattare e il codice che lo
   attende non resti appeso per sempre. Chrome la riporta alla lettera, come «1e-05s», e un
   confronto con `0s` la chiama animazione in corso. Ora la soglia è 20 ms.
3. **Una lista di selettori scritta a mano trovava 1 indicatore su 18.** La prima versione della
   seconda sonda elencava dodici selettori «che contano». Contati nel browser, la home ne ha
   diciotto che dipingono. Una lista di che cosa controllare è una lista di che cosa mancare:
   ora scandisce tutti gli pseudo-elementi.
4. **Il rilevatore cercava la trasparenza, e il contrasto elevato non rende nulla trasparente.**
   Sostituisce il colore con uno di sistema: un indicatore diventa `Canvas`, cioè **identico al
   fondo su cui sta**, e resta pienamente opaco. Ora il confronto è con il colore che ha dietro.
   Nella stessa passata sono emersi altri due difetti, entrambi trovati dai test e non
   dall'esecuzione: il ramo che segnala un indicatore perduto leggeva due chiavi che non esistono
   più e sarebbe andato in errore alla prima scoperta; e la scorciatoia «finisce per `, 0)`» per
   dire *trasparente* legge `rgb(0, 0, 0)` come trasparente, perché il nero puro finisce
   esattamente così. Sotto contrasto elevato il nero è `CanvasText`, il colore più comune della
   pagina.

La sonda riporta anche quanti elementi ha esaminato. Un controllo che dice «nessun problema» senza
dire quante cose ha guardato non si distingue da un controllo che non ha guardato niente.

## 5. Ingrandimento — WCAG 2.2 §1.4.10 (Reflow)

Misurato con lo stesso client, riducendo il **viewport CSS** invece di applicare `zoom` al corpo
della pagina. La differenza non è formale: `document.body.style.zoom` ingrandisce il disegno e
lascia il viewport della misura che aveva, così un impaginato che a schermo reale ripiegherebbe
mantiene le sue colonne da scrivania e il controllo passa dove l'utente vedrebbe un disastro.
Ridurre il viewport è ciò che fa davvero il browser: il 400 % di una finestra da 1280 px è un
viewport da 320 px.

| Pagina | 100 % (1280) | 200 % (640) | 400 % (320) |
|---|---|---|---|
| `/_design/` | nessuno scorrimento orizzontale | nessuno | nessuno |
| `/fr/` | nessuno | nessuno | nessuno |

Nessun elemento deborda dal viewport a nessun livello, esclusi i contenitori `.scroll-x`, che
**devono** essere più larghi: sono scorrevoli per progetto, ed è lì che vive la tabella di §3.6.
