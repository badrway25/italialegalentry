# ROLE JOURNEYS — che cosa fa ciascun ruolo, passo per passo

Versione 1.0 · 20 settembre 2026 · Fonte: Technical Blueprint v1.0 §4, §5, §6 · Direttiva di rebase §60

Ogni percorso qui descritto è anche un **test end-to-end obbligatorio**.

---

## 1. Persona

### Percorso principale

```
pagina pubblica
   → questionario di orientamento (anche senza account)
   → creazione account e consensi
   → profilo
   → obiettivo
   → domande dinamiche
   → esito con motivazione, requisiti, fonti
   → fascicolo creato
   → checklist con responsabili
   → documenti richiesti
   → Academy
   → eventuale revisione professionale
   → monitoraggio
```

### Che cosa vede quando entra

Il cruscotto della persona risponde, nell'ordine, a nove domande. Non sono sezioni decorative: sono
il contenuto.

| Domanda | Risposta nell'interfaccia |
|---|---|
| Dove sono? | Stato del fascicolo, in parole, non in codice |
| Qual è il mio obiettivo? | La finalità dichiarata e il percorso individuato |
| Che cosa ho completato? | Avanzamento reale, non una percentuale inventata |
| Che cosa manca? | Requisiti mancanti, in ordine di urgenza |
| Che cosa devo fare adesso? | **Una sola** azione prioritaria, in evidenza |
| Chi è responsabile? | Per ogni voce aperta, il soggetto competente |
| Quali documenti servono? | Elenco con stato di ciascuno |
| Quali fonti lo dicono? | Fonte accanto a ogni requisito |
| Serve una revisione umana? | Se sì, come chiederla |

### Aree

`Il mio percorso` (timeline) · `Prossima azione` · `Orientamento` · `Il mio fascicolo` ·
`Documenti` · `Checklist` · `Formazione` · `Scadenze` · `Comunicazioni` · `Sportello` · `Cronologia`

### Regole di esperienza

- Un compito per momento cognitivo.
- Divulgazione progressiva: le spiegazioni stanno accanto alla domanda, non in una pagina di aiuto.
- Ritorno indietro sempre possibile.
- Salvataggio e ripresa: una persona che chiude il browser non ricomincia.
- Revisione prima dell'invio definitivo.
- Nessun messaggio entusiasta. Nessun «Perfetto!», nessun «Ci siamo quasi!».
- **Ogni area elencata qui sopra si raggiunge cliccando.** Non è un principio di stile: il 22
  settembre 2026 `Formazione` e `Sportello` esistevano, rispondevano 200 con un solo `h1` e senza
  errori di console, ogni test unitario passava — e non erano linkate da nessuna parte. Ciascun
  modulo aggiungeva la propria riga alla navigazione dall'interno di sé stesso, quindi la riga
  compariva una volta che ci si era già.
- **«Ritorno indietro sempre possibile» vale anche fra i ruoli.** Ogni ruolo atterra sulla propria
  superficie al login, e ciascuna di quelle superfici linkava al cruscotto; nessuna era linkata
  **dal** cruscotto. Per un soggetto autorizzato, cliccare «Tableau de bord» era un viaggio di sola
  andata, e la via di ritorno era rifare il login.

Entrambe sono ora sorvegliate da `apps/portal/tests/test_navigation_reaches_every_surface.py`, che
verifica l'elenco **e la pagina resa** — perché un template che tronca una riga lascerebbe verde un
test sul servizio e l'utente comunque bloccato.

### Test end-to-end

`landing → orientamento → account → questionario → esito → fascicolo → documento → Academy → cruscotto`

---

## 2. Impresa

### Percorso principale

```
pagina pubblica imprese
   → segnalazione del fabbisogno (form pubblico, quando i gate lo consentono)
   → creazione account impresa
   → verifica dell'impresa
   → definizione del fabbisogno strutturato
   → profilo professionale richiesto
   → tempistiche e territorio
   → monitoraggio dell'avanzamento
```

### Che cosa vede

Il cruscotto dell'impresa ruota attorno ai **fabbisogni**, mai attorno alle persone.

| Sezione | Contenuto |
|---|---|
| Identità dell'impresa | Dati, stato di verifica |
| I miei fabbisogni | Elenco, stato, data, territorio, settore |
| Dettaglio fabbisogno | Mansioni, qualifiche, competenze obbligatorie e preferenziali, lingua, sicurezza, esperienza, quantità, tempistiche |
| Formazione richiesta | Fabbisogni formativi collegati |
| Attori responsabili | Chi sta seguendo quale fase, con nome e ruolo |
| Avanzamento | Stato di ciascun fabbisogno |
| Comunicazioni | Messaggi |

### Vincoli invalicabili

- **Nessun elenco di persone navigabile.** Nessuna ricerca libera. Nessuna scheda candidato.
- Un'impresa vede dati personali solo dentro un processo di selezione attivo, solo per le persone che
  un soggetto autorizzato vi ha collegato, solo per i campi necessari, solo con consenso specifico
  registrato, e ogni accesso è tracciato.
- In P0 la visibilità è **zero**.

### Test end-to-end

`landing → esprimere un fabbisogno → account impresa → creare il fabbisogno → modificarlo → vederne lo stato`

---

## 3. Soggetto autorizzato

### Percorso

```
accesso → coda delle pratiche assegnate → pratica → contesto del mandato
   → fabbisogno collegato → persone assegnate → fase → decisione o azione
   → evidenza richiesta → audit
```

### Che cosa vede

| Elemento | Nota |
|---|---|
| Contesto dell'autorizzazione | Tipo, giurisdizione, riferimento, validità. Se scaduta, la coda è vuota |
| Solo le pratiche assegnate | Nessuna vista globale |
| Fabbisogno di riferimento | Il collegamento che giustifica il trattamento |
| Persone collegate | Solo i dati necessari alla fase |
| Fase e decisioni | Con registrazione delle motivazioni |
| Evidenze | Che cosa deve documentare |
| Traccia di audit | La propria, visibile |

### Vincolo

Ogni fase di ricerca, preselezione o selezione **identifica sempre** il soggetto responsabile. Il suo
nome è visibile nel fascicolo della persona e nel cruscotto dell'impresa. Non esiste un processo di
selezione senza attore.

### Test end-to-end

`accesso → lavoro assegnato → pratica → azione → evento di audit registrato`

---

## 4. Professionista

```
accesso → richieste di revisione assegnate → fascicolo → documenti → nota professionale
   → risposta → chiusura
```

Vede **solo** i fascicoli espressamente assegnati, per la durata dell'assegnazione. Mandato o
abilitazione dove necessari. Le note professionali non sono visibili alla persona salvo esplicita
condivisione.

---

## 5. Ente formativo

```
accesso → coorti e corsi assegnati → iscritti → avanzamento → completamenti → attestazioni
```

Vede **solo i dati necessari alla formazione assegnata**: non il fascicolo, non la valutazione
giuridica, non i documenti non attinenti.

---

## 6. Istituzione

```
accesso → perimetro della convenzione → progetti → iniziative territoriali
   → indicatori aggregati → lavori del Forum → documenti condivisi → milestone
```

**Nessun accesso ai fascicoli individuali. Nessun accesso ai dati riservati delle imprese.**
Il perimetro è definito dall'accordo, non dal ruolo: due istituzioni con accordi diversi vedono cose
diverse.

---

## 7. Università e ricerca

```
accesso → programmi → progetti di partenariato → mobilità accademica
   → ricerca e diritto comparato → Forum → documenti condivisi
```

Nessun accesso ai fascicoli privati.

---

## 8. Legal/Rule Editor

```
accesso → elenco regole → nuova versione → condizioni → fonte → validità
   → invio in revisione → (un altro editor) approvazione → attivazione
   → verifica che una valutazione usi la versione corretta
```

Non amministra utenti. Non accede ai fascicoli. Non approva le proprie regole.

### Test end-to-end

`creare versione → revisione → approvazione da parte di un secondo utente → attivazione →
una valutazione usa la versione corretta`

---

## 9. Redattore di contenuti

```
accesso → bozza → revisione → approvazione → programmazione → pubblicazione → archiviazione
```

Non accede ai fascicoli, non modifica le regole giuridiche, non amministra utenti.

### Test end-to-end

`bozza → revisione → pubblicazione`

---

## 10. Partecipante del Forum

```
accesso → profilo di partecipazione → commissioni → tavoli → proposte
   → progetti → milestone → monitoraggio
```

I partecipanti **non possono consultare informazioni private di altri utenti**. Il Forum è uno spazio
di governance, non una rubrica.

---

## 11. Amministratore

Configurazione tecnica e utenti, con separazione dei privilegi, MFA obbligatoria e log su ogni
operazione. Non è il ruolo operativo predefinito: chi lavora quotidianamente sui contenuti o sulle
pratiche usa i ruoli specifici.

---

## 12. Matrice di copertura dei test end-to-end

| Percorso | Esiste oggi | Priorità |
|---|---|---|
| Persona: dall'orientamento al fascicolo | **sì** — verificato nel browser, fascicolo E12273C5DF | P0 |
| Impresa: dal fabbisogno pubblico al fabbisogno gestito | **sì** — `apps/companies/tests` | P0 |
| Legal/Rule Editor: versione → approvazione → attivazione | **sì** — `apps/rules/tests/test_governance.py` | P0 |
| Redattore: bozza → revisione → pubblicazione | parziale | P0 |
| Soggetto autorizzato: coda → pratica → azione → audit | **sì** — `apps/selection/tests` | P1 |
| Professionista: revisione assegnata | **sì** — `apps/helpdesk/tests`, `apps/cases/tests/test_views.py` | P1 |
| Forum: pagina pubblica → iscrizione → area autenticata | **sì, ma chiusa** dal flag `virtual_forum` | P1 |
| Permessi a livello di oggetto, **tredici** asserzioni della direttiva §61 | **sì** — `tests/security/test_object_permissions.py`; l'asserzione 13 ha fatto emergere un difetto reale | P0 |

Aggiornato il 21 settembre 2026. Un «sì» qui significa che il percorso è stato **esercitato**, non
che il codice esiste: da un test d'integrazione HTTP, da un test di dominio contro il servizio reale,
o nel browser. La colonna non ammette «il modello c'è».
