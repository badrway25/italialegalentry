# VERIFICA UMANA — quello che nessun test automatico può dire

Stato: **HUMAN_QA_REQUIRED** · Nessuna voce di questo documento è stata eseguita

> **Perché esiste.** `docs/ACCESSIBILITY.md` elenca ciò che la suite verifica: contrasto sui token
> reali, `h1` unico per pagina, etichette dei form, bersagli da 24 px, regioni di scorrimento
> raggiungibili, `prefers-reduced-motion`, `forced-colors`. Tutto vero, e tutto insufficiente.
>
> Un controllo automatico verifica che un'etichetta **esista**. Non verifica che dica la cosa
> giusta. Verifica che un `aria-live` sia dichiarato, non che l'annuncio arrivi al momento utile.
> Verifica che il contrasto superi 4,5:1, non che il testo si legga. La differenza fra i due non è
> di grado.
>
> **Non è stato eseguito nulla di quanto segue**, e non è simulabile: non ho un lettore di schermo,
> non ho un telefono, e una persona che usa NVDA ogni giorno nota in trenta secondi cose che una
> checklist non contiene. Dichiarare PASS su queste voci sarebbe falso.

---

## 0. Come leggere gli esiti

| Esito | Significato |
|---|---|
| **PASS** | Provato da una persona, funziona |
| **FAIL** | Provato da una persona, non funziona — apre un difetto |
| **HUMAN_QA_REQUIRED** | Non ancora provato. È lo stato di **tutte** le righe oggi |

Una riga non provata non è una riga passata. Se una sessione finisce senza arrivare in fondo, le
righe rimaste restano `HUMAN_QA_REQUIRED` e si dice quali.

---

## 1. Lettore di schermo — la sessione che conta

**Chi.** Preferibilmente una persona che usa un lettore di schermo quotidianamente. In subordine, un
collaudatore vedente con NVDA e **lo schermo spento**: guardare lo schermo mentre si collauda un
lettore di schermo invalida il collaudo, perché il cervello riempie i buchi che l'utente reale non
può riempire.

**Con che cosa.** NVDA + Firefox su Windows, oppure VoiceOver + Safari su macOS/iOS. Se se ne prova
uno solo, NVDA + Firefox: è la combinazione più diffusa fra chi usa un lettore di schermo su
Windows, che è il pubblico di questa piattaforma.

### 1.1 Percorso persona, dall'inizio alla fine

Il percorso richiesto dal mandato, non una pagina isolata:

`VISITATORE → ACCOUNT → PROFILAZIONE → ORIENTAMENTO → RULE ENGINE → RISULTATO → FASCICOLO →
CHECKLIST → DOCUMENTI`

| # | Da verificare | Perché proprio questo |
|---|---|---|
| 1.1.1 | La pagina iniziale si capisce navigando **per intestazioni** (`H` in NVDA), senza leggerla tutta | È il modo in cui si legge davvero una pagina, non dall'inizio alla fine |
| 1.1.2 | Il salto «vai al contenuto» esiste, si raggiunge col primo `Tab` e **funziona** | Un salto che sposta il focus visivo ma non quello del lettore è peggio di nessun salto |
| 1.1.3 | Il cambio di lingua annuncia la lingua in cui si passa, e la pagina che arriva è annunciata nella **voce giusta** | Questo è il rischio proprio del progetto: quattro lingue, di cui una in un altro alfabeto |
| 1.1.4 | Nel questionario di orientamento: ogni domanda annuncia **posizione e totale** («domanda 2 di 5») | Senza, non si sa quanto manca e non si decide se vale la pena continuare |
| 1.1.5 | Un errore di validazione viene **annunciato**, non solo mostrato, e il focus arriva al campo | L'errore silenzioso è il difetto classico dei form accessibili «a norma» |
| 1.1.6 | Il risultato della pre-valutazione annuncia **che è una pre-valutazione**, prima dell'esito | L'intera posizione giuridica del progetto sta in questa distinzione. Se l'esito arriva prima della qualificazione, la qualificazione non è stata detta |
| 1.1.7 | Le **fonti numerate** si raggiungono e si leggono come elenco | Una fonte che non si può leggere non è una fonte |
| 1.1.8 | Nella checklist, ogni riga annuncia **chi è il responsabile** insieme allo stato | «Da fare» senza «da parte di chi» è la metà utile dell'informazione |
| 1.1.9 | Il caricamento di un documento annuncia esito e **nuovo stato** senza ricaricare la pagina | Un caricamento che riesce in silenzio si ripete tre volte |
| 1.1.10 | Nessuna icona viene letta come testo, nessun testo utile viene letto come icona | |

### 1.2 Percorso impresa

`IMPRESA → ACCOUNT/VERIFICA → FABBISOGNO → COMPETENZE → ATTORI AUTORIZZATI → STATO`

| # | Da verificare |
|---|---|
| 1.2.1 | Lo stato della verifica dell'impresa è annunciato e **comprensibile fuori contesto** |
| 1.2.2 | Nel modulo del fabbisogno, il rifiuto di un criterio d'età annuncia **perché** è rifiutato, non solo che lo è |
| 1.2.3 | La tabella delle competenze si percorre in modo tabellare (`Ctrl+Alt+frecce`) e le intestazioni si annunciano |
| 1.2.4 | L'attore responsabile è annunciato **insieme** al processo, non in un riquadro separato che si può non incontrare mai |

### 1.3 Back-office

| # | Da verificare |
|---|---|
| 1.3.1 | La console delle fasi: lo stato di ogni gate è leggibile senza colore |
| 1.3.2 | L'editor delle regole: il diff fra versioni è percorribile, non solo visibile |
| 1.3.3 | L'anteprima a vuoto di una regola annuncia il risultato |

---

## 2. Solo tastiera

Senza toccare il mouse. Non «anche con la tastiera»: **solo**.

| # | Da verificare | Nota |
|---|---|---|
| 2.1 | Ogni percorso del §1 si completa interamente da tastiera | Se un passo richiede il mouse, il percorso è interrotto, non difficile |
| 2.2 | Il focus è **sempre visibile**, su ogni fondo, compresi i pulsanti scuri | |
| 2.3 | L'ordine di tabulazione segue l'ordine di lettura, anche dove la griglia riordina visivamente | Il rischio sta dove CSS ha spostato qualcosa |
| 2.4 | Nessuna trappola del focus | Menù, riquadri a comparsa, selettore di lingua |
| 2.5 | Il menù a tendina si apre, si percorre con le frecce, si chiude con `Esc` e **restituisce il focus** al pulsante | |
| 2.6 | `Esc` chiude ciò che si è aperto, sempre, senza eccezioni | |
| 2.7 | Nelle tabelle lunghe, la regione di scorrimento è raggiungibile e **scorre con le frecce** | WCAG 2.2 §2.1.1 su un contenitore `overflow` |
| 2.8 | In arabo, `Tab` va nella direzione giusta e le frecce non si invertono | |

---

## 3. Ingrandimento

| # | Da verificare | Criterio |
|---|---|---|
| 3.1 | 200 % su desktop: nulla si sovrappone, nulla si taglia | WCAG §1.4.4 |
| 3.2 | 400 % a 1280 px: **nessuno scorrimento orizzontale** salvo tabelle, diagrammi e blocchi di codice | WCAG §1.4.10 Reflow |
| 3.3 | Solo il testo a 200 % (senza ingrandire la pagina): nessun troncamento | WCAG §1.4.12 |
| 3.4 | A 400 % il menù resta usabile e non copre il contenuto | È il punto in cui i menù cedono |
| 3.5 | Le stesse quattro prove in **arabo** | Il testo arabo cambia altezza di riga e larghezza: quello che regge in francese può non reggere |

---

## 4. Colori forzati e movimento ridotto

| # | Da verificare |
|---|---|
| 4.1 | Windows «Contrasto elevato» attivo: ogni stato resta distinguibile **senza colore** |
| 4.2 | I bordi che portano uno stato (il filetto del registro) restano visibili in colori forzati |
| 4.3 | `prefers-reduced-motion`: nessuna transizione residua |
| 4.4 | Nessuna informazione affidata al solo colore — verificato **guardando**, non leggendo il CSS |

---

## 5. Arabo, letto da chi legge l'arabo

Questo capitolo non è collaudo tecnico. `scripts/qa_rtl_check.py` verifica direzione, scorrimento,
proprietà logiche e regioni: 14 coppie pagina/viewport, 0 problemi. Nessuna di quelle verifiche dice
se il testo **si legge**.

| # | Da verificare | Chi |
|---|---|---|
| 5.1 | I 3618 messaggi tradotti si leggono come italiano/inglese/arabo **redatti**, non tradotti | Un revisore madrelingua per lingua |
| 5.2 | I termini tecnici lasciati in italiano (`nulla osta`, `decreto flussi`, `permesso di soggiorno`) sono la scelta giusta per un lettore marocchino | Revisore arabo |
| 5.3 | Le cifre occidentali dentro testo arabo si leggono bene in contesto | Revisore arabo |
| 5.4 | Il marchio `Italy Legal Entry™` non si spezza né si specchia dentro una riga araba | |
| 5.5 | La pre-valutazione non si legge come una decisione in nessuna delle quattro lingue | **Revisore + referente giuridico** |
| 5.6 | Gli undici termini della piattaforma non ancora nel glossario (`docs/I18N_RTL.md` §5) vengono decisi e trascritti | Le tre corsie insieme |

Il §5.5 è il più importante del documento. Un errore di registro lì non è un difetto di traduzione:
è una promessa che la piattaforma non può mantenere.

---

## 6. Telefono reale

Non l'emulatore. Il pubblico di questa piattaforma accede in prevalenza da telefono, spesso su rete
mobile marocchina.

| # | Da verificare |
|---|---|
| 6.1 | Android con Chrome e iPhone con Safari, entrambi, su rete mobile **vera** |
| 6.2 | I bersagli si colpiscono col pollice, non col puntatore |
| 6.3 | La tastiera virtuale non copre il campo attivo né il pulsante di invio |
| 6.4 | Il tipo di tastiera è quello giusto per ogni campo (numerica, e-mail, telefono) |
| 6.5 | Il caricamento di un documento funziona **dalla fotocamera**, che è come si caricherà davvero |
| 6.6 | Su rete lenta la pagina è leggibile prima che i caratteri tipografici arrivino |
| 6.7 | Le stesse sei prove in arabo, con l'interfaccia di sistema in arabo |
| 6.8 | Con TalkBack e con VoiceOver, almeno il percorso persona |

---

## 7. Che cosa fare degli esiti

Un FAIL qui vale quanto un test rosso. Va aperto come difetto, con la pagina, il viewport, lo
strumento e il comportamento osservato, e va corretto prima della pubblicazione se riguarda un
percorso obbligatorio.

Finché questo documento ha righe `HUMAN_QA_REQUIRED`, `docs/FINAL_REPORT.md` §12 dice
«**parzialmente verificata**» e non «conforme». La differenza è precisamente ciò che questo
documento elenca.
