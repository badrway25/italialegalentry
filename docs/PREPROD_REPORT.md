# RAPPORTO DI PRE-PRODUZIONE — Italy Legal Entry™

22 settembre 2026 · Fase: **PRE-PRODUCTION HARDENING** · Nessun deploy eseguito, nessun remote
aggiunto, nessuna infrastruttura toccata

---

## 1. Stato

### `PREPROD_RELEASE_CANDIDATE`

Le tre condizioni poste dalla direttiva sono soddisfatte:

| Condizione | Esito |
|---|---|
| **Repository e cronologia puliti** | Cronologia riscritta, scansione successiva a **zero** indirizzi di terzi, zero documenti riservati, zero credenziali |
| **Autorizzazione verificata** | Dieci ruoli × sei forme d'attacco (56 test nuovi), più le tredici asserzioni preesistenti. `tests/security`: 118 passati. Un difetto chiuso — L-14, la cascata |
| **Dati sensibili puliti** | Indirizzo personale redatto in working tree **e** in cronologia, con una guardia che cammina su `git ls-files` |

**Che cosa significa e che cosa non significa.** Significa che questo repository può essere messo su
un ambiente di pre-produzione: il codice regge le impostazioni di produzione, la cronologia si può
consegnare, e non c'è nulla dentro che non debba esserci.

**Non significa che si possa andare in esercizio.** I bloccanti al go-live del §15 sono tutti
aperti, e quattro su sei non dipendono da chi scrive software.

---

## 2. Git

| | |
|---|---|
| Ramo | `main` |
| HEAD | `a525fe7` |
| Commit | `90` |
| Working tree | pulita |
| Remote | **nessuno**, e non ne è stato aggiunto alcuno |

### La cronologia è stata riscritta

**Sì, due volte, il 21 settembre 2026.** Il vecchio HEAD era `53d9b46` e non esiste più: **ogni hash
citato in qualunque materiale anteriore a quella data è morto.**

| Passata | Perché |
|---|---|
| 1ª | Rimuovere i documenti sorgente, i dati personali di terzi e quattordici screenshot committati per errore |
| 2ª | Rimuovere lo **strumento** della prima passata, che era stato committato con dentro i valori che rimuoveva |

La seconda passata è la parte che vale la pena ricordare. Dopo la prima, i valori erano spariti da
ogni file della cronologia tranne uno: lo script che li rimuove. È lo stesso errore commesso poche
ore prima dalla guardia in `tests/compliance/`, che cercava l'hash come letterale e quindi
corrispondeva a se stessa. Due volte è una regola: **uno strumento di redazione non nomina ciò che
redige.** La tabella dei valori vive ora fuori dal repository e lo script si rifiuta di partire
senza di essa — perché una tabella mancante renderebbe ogni commit un'operazione nulla e
`filter-branch` riporterebbe successo su tutti.

**Copia probatoria:** bundle Git completo fuori dal repository, in una posizione privata; sha256
registrato, regole d'uso scritte accanto. Il ripristino è stato **provato**: clonato, HEAD e
conteggio commit verificati, copia cancellata.

Dettagli: `docs/security/HISTORY_REWRITE_2026-09-21.md`.

---

## 3. Scansione PII e segreti

`scripts/history_secret_scan.py` legge **ogni blob raggiungibile da ogni ref**, non la working tree.
Sedici famiglie di pattern.

| Misura | Prima | Dopo |
|---|---:|---:|
| Blob in cronologia | 2124 | 2131 |
| Blob di testo scansionati | 1311 | 1323 |
| **Indirizzi e-mail di terzi** | **2** | **0** |
| Documenti sorgente del committente | 4 file, ogni versione | **0** |
| Screenshot committati per errore | 14 | **0** |
| Dimensione di `.git` | 35 MB | **20 MB** |

Zero occorrenze, prima e dopo, di: chiavi AWS, blocchi di chiave privata, token
GitHub/Slack/Google/Stripe, JWT, codice fiscale, IBAN.

I 285 rilievi residui sono elencati uno per uno in `docs/security/HISTORY_SCAN_AFTER.md` §2 e sono
tutti attesi: digest d'integrità dei testi bloccati, la password del database di sviluppo dichiarata
in `.env.example`, password sintetiche di fixture su `@example.test`, numeri di telefono inventati.

**Nessun rilievo residuo è un dato personale di terzi, una credenziale di produzione o un documento
riservato.**

I 155 blob binari non sono stati grepati, perché una regex su un PNG non dimostra nulla. Sono stati
trattati per percorso, e i 26 screenshot del sito di produzione sono stati **guardati**.

---

## 4. Ambiente di test precedente

Ambiente legacy di test: solo riferimento, non fa parte di questo repository (decisione della titolarità, 11 ottobre 2026); dettagli nel registro privato.

**Nulla di quell'ambiente è entrato in questo repository, e nulla deve entrarci.**

---

## 5. Regole giuridiche in attesa di revisione

**Nessuna regola è in vigore.**

| Stato | N | Provenienza |
|---|---:|---|
| `DRAFT` | 13 | redatte dalla fonte normativa |
| `LEGACY_CANDIDATE` | 3 | derivate dalla piattaforma precedente |
| `ACTIVE` | **0** | — |

Undici erano in vigore con `approved_by` nullo. Era deliberato e documentato, ma il controllo era un
comando che qualcuno doveva ricordarsi di eseguire, e il database accettava la riga senza obiezioni.
La migrazione `rules.0002` le ha riportate indietro e un vincolo di database rifiuta ora una regola
approvata o in vigore la cui etichetta di approvatore è vuota — sul campo testuale e non sulla
chiave esterna, perché l'anonimizzazione di un account ex art. 17 non deve rendere irrappresentabile
una regola in vigore.

**Catena applicata:** `LEGACY_CANDIDATE` → `SOURCE_VERIFIED` → `LEGAL_REVIEW` → `APPROVED` →
`ACTIVE`. `DRAFT → LEGAL_REVIEW` non è più un arco.

**Per ogni regola**, `manage.py rules_pending_review` stampa i nove fatti che la direttiva chiede —
fonte, riferimento, URL, giurisdizione, validità da/a, versione, revisore, stato, provenienza — e
che cosa manca a ciascuna.

**Le quindici fonti non sono verificate:** nessuna porta una data di consultazione reale, un nome o
un URL. Prima era una nota in un documento; ora blocca la catena, perché `SOURCE_VERIFIED` rifiuta
una regola le cui fonti portano un riferimento e nient'altro.

Il primo esito del rapporto ha trovato un difetto nei dati che nessuno aveva visto: **cinque fonti
europee registrate come giurisdizione italiana** — i due articoli del codice dei visti, il codice
frontiere Schengen, la direttiva Carta blu e la 2016/801. Una regola che poggia su una direttiva
cambia quando si muove Bruxelles, non Roma. Corrette.

**Per vedere il motore funzionare in locale**, `manage.py rules_activate_demonstration` percorre la
catena vera con le stesse guardie, usa due account distinti perché i quattro occhi valgono anche per
una dimostrazione, rifiuta di partire dove i dati dimostrativi non sono ammessi, e marchia ogni
regola con **«DIMOSTRAZIONE — nessun giurista ha approvato questa regola»**. L'etichetta finisce
nello snapshot di ogni pre-valutazione, e **la pagina di esito la mostra**, sopra l'esito, nascondendo
le date di consultazione fittizie.

---

## 6. Testi legali italiani ufficiali

**Ancora mancanti.** Stato invariato: `BLOCKED_BY_MISSING_OFFICIAL_SOURCE`.

L'«Allegato 1 — Testi giuridici» esiste solo in francese, come traduzione di cortesia che dichiara
essa stessa che fa fede la versione italiana. Nessun testo è stato tradotto, riassunto o inventato.

Il blocco è **implementato**, non soltanto documentato, e verificato oggi:

| Verifica | Esito |
|---|---|
| Gate `legal_pages_available` | **chiuso** |
| `/fr/mentions-legales/`, `/fr/confidentialite/`, `/fr/conditions/`, `/fr/cookies/` | **404** tutte e quattro |
| Gate `public_forms_enabled` | **chiuso** di conseguenza |

---

## 7. Autorizzazione — esiti

| Suite | Esito |
|---|---|
| `tests/security/test_authorization_audit.py` (nuova) | **56 passati** |
| `tests/security/test_object_permissions.py` (13 asserzioni §61) | passati |
| `tests/security/test_privilege_escalation.py` | passati |
| `tests/security/test_production_settings_refuse_to_start.py` (nuova) | **10 passati** |
| `tests/security` completo | **118 passati, 0 falliti** |

**Come il difetto è saltato fuori, per non prendersi un merito che non c'è.** L-14 non è stato
trovato dalla suite nuova: l'ha fatto emergere un test preesistente che asseriva che una
cancellazione restituisse 302, durante una corsia di regressione. La suite nuova esiste perché
quella forma d'attacco — la cascata — **non era mai stata provata**, e quindi il difetto era potuto
entrare e restare. Ora è coperta in entrambe le direzioni: che una cascata non neghi ciò che il
modello concede, e che non conceda ciò che il modello nega.

La suite nuova incrocia **dieci ruoli** — persona, impresa, attore autorizzato, professionista, ente
formativo, istituzione, università, operatore, rule editor, amministratore — per **sei forme
d'attacco**, invece che ruolo per ruolo:

1. nessuna auto-elevazione di privilegio
2. nessun accesso orizzontale
3. nessun accesso fra imprese
4. nessuna scoperta tramite ricerca
5. nessun download di documento con URL noto
6. **nessuna cancellazione o modifica indiretta per cascata non autorizzata**

La sesta non era mai stata provata, ed è quella che era rotta. `notifications.Notification` è legata
a `portal.Message` in `CASCADE`, e l'admin di Django rifiuta una cancellazione la cui cascata tocca
un modello su cui l'account non ha `delete`. Poiché l'invio crea sempre la riga compagna, **nessun
ruolo poteva più cancellare una comunicazione** — con un 403 nudo, senza pulsante mancante e senza
nulla nell'interfaccia che lo spiegasse. Registrata come **L-14** in
`docs/security/PERMISSION_MODEL.md`.

Il permesso concesso è **per modello**, non per applicazione: si ferma alla notifica e lascia
intoccabile `EmailOutbox`, che è il registro di ciò che è stato davvero inviato. La correzione ovvia
avrebbe dato a un amministratore il potere di cancellare la prova di un invio.

---

## 8. Accessibilità — esito automatico

| Verificato dalla suite | Esito |
|---|---|
| Contrasto sui token reali | passa |
| `h1` unico per pagina | passa |
| Etichette dei form | passa |
| Bersagli ≥ 24 px, o distanziati di 24 px | passa |
| Regioni di scorrimento etichettate e raggiungibili da tastiera | passa |
| Nessun testo sotto 12 px | passa |
| `prefers-reduced-motion`, `forced-colors` | passa |
| Arabo e RTL: 14 coppie pagina/viewport | **0 problemi** |

**Questo è tutto ciò che una macchina può dire, ed è meno di quanto sembri.** Un controllo
automatico verifica che un'etichetta esista, non che dica la cosa giusta; che un `aria-live` sia
dichiarato, non che l'annuncio arrivi al momento utile; che il contrasto superi una soglia, non che
il testo si legga.

---

## 9. `HUMAN_QA_REQUIRED`

`docs/HUMAN_QA_CHECKLIST.md`. **Ogni riga è `HUMAN_QA_REQUIRED`: nulla di quanto elenca è stato
eseguito, e nulla è simulabile.**

| Capitolo | Che cosa richiede |
|---|---|
| Lettore di schermo | NVDA + Firefox, **a schermo spento**, sui due percorsi completi |
| Solo tastiera | otto voci, compreso l'ordine di focus dove la griglia riordina visivamente |
| Ingrandimento | 200 % e 400 %, e le stesse prove **in arabo** |
| Colori forzati, movimento ridotto | quattro voci |
| **Arabo letto da chi legge l'arabo** | sei voci, fra cui la più importante del documento |
| Telefono reale | otto voci, su rete mobile vera, con TalkBack e VoiceOver |

La voce più importante è §5.5: che la pre-valutazione **non si legga come una decisione** in nessuna
delle quattro lingue. Un errore di registro lì non è un difetto di traduzione: è una promessa che la
piattaforma non può mantenere.

Aggiunta in questa fase: le traduzioni **non sono state rilette da una persona**. L'audit verifica
segnaposto, marcatori inline, forme plurali, scrittura, cifre, formulazioni vietate, marchio e
glossario — cioè la **forma**, non la resa.

---

## 10. Prestazioni su stack simil-produzione

Container Linux, gunicorn con tre worker, whitenoise con lo storage a manifesto, `DEBUG=False`,
`config.settings.prod`, PostgreSQL dedicato, intestazioni di sicurezza attive. Dettaglio in
`docs/STAGING_PERFORMANCE.md`.

| Misura | Valore |
|---|---|
| Peggior LCP, 8 pagine × 2 viewport | **712 ms** (home araba, avvio a freddo) |
| LCP tipico | 170–230 ms |
| Peggior CLS | **0,0046** |
| Payload massimo | 425 kB su 22 richieste |
| Risposta del server, mediana su 5 richieste | 18–42 ms |
| Statici | impronta del contenuto, `immutable`, gzip **−90 %** |

Le due anomalie sono scritte invece di essere lisciate: una riga riporta FCP e LCP a zero, che è un
artefatto del `PerformanceObserver` agganciato dopo il primo disegno; un'altra ha un TTFB di 491 ms
contro 41, che è l'avvio a freddo del catalogo arabo.

**Nessun test di carico. Nessuna misura su rete mobile reale.** Il pubblico accede in prevalenza da
telefono in Marocco, e su loopback quella condizione non esiste. Niente punteggio Lighthouse, e il
documento §6 spiega perché: un punteggio preso dalla stessa macchina che esegue il server è un
numero su quella macchina.

---

## 10bis. Verifica end-to-end del release candidate

I due percorsi richiesti dal mandato, percorsi cliccando in un browser reale, su dati sintetici.

### `VISITATORE → ACCOUNT → PROFILAZIONE → ORIENTAMENTO → RULE ENGINE → RISULTATO → FASCICOLO → CHECKLIST → DOCUMENTI`

| Passo | Esito |
|---|---|
| Questionario di orientamento | 3 passi, completato |
| Fascicolo aperto | `E12273C5DF` |
| Esito | «Exigence manquante» — mai una decisione sulla persona |
| Regole applicate | 9 |
| Fonti numerate sulla pagina di esito | **6** |
| Righe di checklist | 9, di cui **4 con una disposizione** |
| Pre-valutazione riproducibile dallo snapshot | **sì** |
| Academy e Sportello raggiungibili dal cruscotto | **sì**, dopo la correzione |
| Avviso «regole non approvate» | **presente, sopra l'esito**, in tutte e quattro le lingue |

### `IMPRESA → ACCOUNT/VERIFICA → FABBISOGNO → COMPETENZE → ATTORI AUTORIZZATI → STATO`

| Passo | Esito |
|---|---|
| Fabbisogni raggiunti cliccando | 4 |
| Competenze sul fabbisogno | 17 |
| Stato del fabbisogno | «VÉRIFIÉE» |
| Attore responsabile nominato | **sì** |
| Analisi territoriale richiesta dall'impresa | **403, rifiutata** — e deve esserlo |

### La coda del percorso, che non era mai stata percorsa

`qa_person_journey.py` si fermava ai documenti. Il flusso del mandato prosegue:
`… → DOCUMENTI → FORMAZIONE/SPORTELLO → MONITORAGGIO`. Percorrerla ha trovato **due difetti della
stessa famiglia**, e nessuno dei due era una pagina rotta.

| Superficie | Risposta | `h1` | Errori di console | Linkata dall'area riservata |
|---|---|---|---|---|
| Academy | 200 | «Academy», uno solo | 0 | **no** → sì |
| Sportello digitale | 200 | «Guichet numérique», uno solo | 0 | **no** → sì |

Ogni test unitario passava. Entrambi i moduli aggiungevano la propria riga alla navigazione
**dall'interno di sé stessi**, il che legge sensatamente finché non ci si chiede come si arrivi
alla prima pagina di un modulo mai aperto: la riga compariva una volta che ci si era già.

Lo stesso difetto, un livello più giù: **ogni ruolo atterra sulla propria superficie al login, e
nessuna di quelle superfici era linkata dal cruscotto.** Per un attore autorizzato, cliccare
«Tableau de bord» era un viaggio di sola andata — la via di ritorno all'unica superficie per cui il
suo ruolo esiste era rifare il login.

È la forma di difetto che nessuna suite avrebbe segnalato: non una pagina rotta, un percorso
mancante verso di essa. Ed è il motivo per cui il mandato chiede di percorrere i **flussi**, non di
collaudare le pagine.

`scripts/qa_journey_tail.py` percorre ora quella coda, e
`apps/portal/tests/test_navigation_reaches_every_surface.py` (20 test) sorveglia l'elenco **e la
pagina resa** — perché un template che tronca una riga lascerebbe verde un test sul servizio e
l'utente comunque bloccato.

### Superficie pubblica

| Verifica | Esito |
|---|---|
| Scansione completa (`--noreload`, Fase 3 aperta) | **804 pagine, 276 link, 0 problemi, 0 link rotti** |
| Arabo e RTL, pagine autenticate | **14 coppie pagina/viewport, 0 problemi** |
| Pagine legali italiane | **404** tutte e quattro, gate G1 chiuso |

Nessuna funzionalità decorativa è stata aggiunta in questa fase.

---

## 11. Test automatici

**2976 test raccolti**, da 2882 all'inizio della fase: **94 nuovi**, tutti guardie aggiunte dopo un
difetto trovato. Nessuno è copertura di superficie.

| Corsia (non si sovrappongono: i numeri si sommano) | Esito |
|---|---|
| `apps/cases` · `accounts` · `orientation` · `pathways` · `portal` | **575 passati**, 3 saltati |
| `apps/rules` · `companies` · `selection` · `academy` · `helpdesk` · `documents` · `forum` · `notifications` · `pages` · `ecosystem` · `enquiries` | **1444 passati, 0 falliti** |
| `tests/security` · `compliance` · `backoffice` · `frontend` · guardie di progetto · 12 app minori | **714 passati**, 1 xfailed |
| `tests/i18n` | **233 passati, 0 falliti** |

L'unico `xfail` è `test_the_shim_is_gone`: il debito dei token legacy, che deve restare rosso
finché la migrazione non finisce. È un test che passerebbe cancellandolo, ed è esattamente perché
esiste.

### Le guardie nuove, e il difetto che ciascuna copre

| Guardia | Test | Difetto che l'ha resa necessaria |
|---|---:|---|
| `tests/security/test_authorization_audit.py` | 56 | La cascata non autorizzata non era mai stata provata come forma d'attacco |
| `apps/portal/tests/test_navigation_reaches_every_surface.py` | 20 | Due moduli funzionanti e irraggiungibili cliccando |
| `apps/rules/tests/test_provenance_chain.py` | 18 | Undici regole in vigore senza approvatore, e quindici fonti mai aperte |
| `tests/security/test_production_settings_refuse_to_start.py` | 10 | Un `.env` di sviluppo che soddisfaceva i controlli di produzione |
| `apps/rules/tests/test_new_version.py` | 6 | Provenienza riciclata da una nuova versione; `--undo` a senso unico |
| `apps/cases/tests/test_demonstration_notice.py` | 6 | Un risultato di dimostrazione indistinguibile da uno vero |
| `apps/portal/tests/test_admin_cascade.py` | 5 | Nessun ruolo poteva cancellare una comunicazione notificata |
| `tests/compliance/test_no_personal_data_in_repository.py` | 4 | Un indirizzo reale committato come evidenza d'audit |
| `tests/test_env_example_is_complete.py` | 3 | Sei variabili lette e non dichiarate, una delle quali obbligatoria |
| `tests/test_migration_drift.py` | 2 | Una deriva di migrazione passata perché il controllo copriva una app su 28 |

Quest'ultima tabella è il riassunto più onesto della fase: **dieci gruppi di test nuovi, e ciascuno
esiste perché un difetto era già lì.** In totale i difetti trovati sono diciassette — alcuni,
come la riscrittura della cronologia o la correzione della giurisdizione di cinque fonti, non si
sorvegliano con un test unitario ma con uno strumento o con un dato corretto.

---

## 12. Controllo delle migrazioni

| Controllo | Esito |
|---|---|
| `manage.py makemigrations --check --dry-run` | **No changes detected** |
| `tests/test_migration_drift.py` | passa, su **tutte e 28 le app** |

Il controllo esisteva già, su **una sola app**, e una deriva era passata: una riformulazione di
etichetta di `choices` aveva lasciato lo stato del modello senza migrazione. Nessuna colonna cambia,
quindi nessun test e nessuna pagina lo mostrava.

---

## 13. `manage.py check --deploy` con impostazioni di produzione

**Nessun avviso, nessun errore.** Prima ne aveva uno.

L'avviso era sul secondo fattore, e sistemarlo ha scoperto qualcosa di peggiore: `prod.py` si
rifiutava di avviarsi su TLS debole o chiave corta, ma **non** sul secondo fattore spento — che apre
i fascicoli di persone reali a una sola password. Era un avviso, cioè una cosa che si legge se per
caso si esegue quel comando. Ora ferma l'avvio.

E un difetto più profondo, trovato scrivendo il test che doveva dimostrare che le tre variabili
obbligatorie fermano l'avvio: **due su tre non lo facevano.** `base.py` leggeva un `.env` accanto al
codice qualunque fosse il modulo di impostazioni, quindi un file di sviluppo copiato su un server non
indeboliva la produzione — la **soddisfaceva**, fornendo `DJANGO_SECRET_KEY` e
`DJANGO_ALLOWED_HOSTS` con valori di sviluppo. Il controllo di coerenza non aveva più nulla da
obiettare. Sotto `config.settings.prod` il file è ora ignorato.

`tests/test_env_example_is_complete.py` verifica che `.env.example` elenchi ogni variabile letta, che
non ne dichiari di ignorate, e che le tre obbligatorie siano marcate come tali. Ne mancavano sei, fra
cui `DJANGO_CSRF_TRUSTED_ORIGINS`, che è obbligatoria e sulla quale il primo `check --deploy` è morto.

---

## 14. Problemi noti

Elenco completo e senza arrotondamenti in `docs/FINAL_REPORT.md` §15. I sette che pesano:

| # | Problema | Gravità |
|---|---|---|
| 1 | **Nessun giurista ha validato le regole.** Non è più un difetto di sistema — nessuna regola è in vigore — ma il lavoro resta da fare | alta |
| 2 | **Le quindici fonti non sono verificate** alla fonte ufficiale: nessuna data, nessun nome, nessun URL | alta |
| 3 | **Le traduzioni non sono state rilette da una persona.** L'audit verifica la forma, non la resa | media |
| 4 | **Nessun passaggio con un lettore di schermo reale** | media |
| 5 | `role:staff` cumula ancora redazione e accesso ai dati delle imprese (L-03) | media |
| 6 | Nessun motore antivirus: ogni file risulta «non analizzato», e la regola di consegna lo dichiara | media |
| 7 | **Ambiente legacy di test**: solo riferimento, non fa parte di questo repository (decisione della titolarità, 11 ottobre 2026); dettagli nel registro privato | **fuori progetto** |

---

## 15. Bloccanti al go-live

Distinti dai bloccanti alla pre-produzione, che sono **zero**.

| # | Bloccante | Di chi è la decisione |
|---|---|---|
| 1 | **Testi legali italiani ufficiali.** Finché non arrivano, le pagine legali non si pubblicano e i form pubblici restano chiusi | committente |
| 2 | **Revisione giuridica delle regole** e verifica delle quindici fonti alla fonte ufficiale | giurista |
| 3 | **Conferma dell'hosting nell'Unione europea** (CR-08). Checklist di dodici punti in `docs/DEPLOYMENT_READINESS.md` §3, compresa la regione dei **backup**, che è l'errore classico | committente + fornitore |
| 4 | **Decisione sull'ambiente legacy di test** (presa l'11 ottobre 2026: solo riferimento, non fa parte di questo repository) | committente |
| 5 | **Rilettura umana delle traduzioni** prima di pubblicare in arabo, italiano e inglese | committente |
| 6 | **Passaggio di accessibilità con un lettore di schermo reale** | committente |

Nessuno dei sei è codice. Due riguardano decisioni, due richiedono un professionista, due richiedono
materiale che non esiste ancora.

**Prima di aggiungere un remote pubblico**, nient'altro da fare: la cronologia è pulita, e
`tests/compliance/test_no_personal_data_in_repository.py` sorveglia la working tree. Ma la
cronologia va riscansionata prima del push, perché un test non la raggiunge.

---

## 16. Che cosa è stato fatto in questa fase, in una tabella

| Area | Prima | Dopo |
|---|---|---|
| Cronologia Git | 2 PDF riservati, 1 indirizzo personale, 14 screenshot | **pulita**, copia probatoria fuori dal repository |
| Documenti del committente | in `docs/source/`, tracciati | fuori dal repository, con il controllo d'integrità rimasto funzionante |
| Regole in vigore senza approvatore | 11 | **0**, e il database le rifiuta |
| Verifica della fonte | una nota in un documento | uno stato della catena che rifiuta |
| Giurisdizione delle fonti | 5 fonti europee marcate IT | corrette |
| `check --deploy` | 1 avviso | **0** |
| `.env` di sviluppo su un server | soddisfaceva i controlli di produzione | ignorato sotto `prod` |
| Secondo fattore spento in produzione | un avviso | **ferma l'avvio** |
| `.env.example` | 6 variabili mancanti | complete, con un test in entrambe le direzioni |
| `makemigrations --check` | su 1 app su 28 | su **28**, come test |
| Cancellazione per cascata | mai provata, e rotta | 56 test di autorizzazione, difetto chiuso |
| Risultato di dimostrazione | indistinguibile da uno vero | **lo dice, sopra l'esito** |
| Prestazioni | `runserver` con `DEBUG=1` | stack simil-produzione, Core Web Vitals misurati |
| Verifica umana | non menzionata | checklist, ogni riga `HUMAN_QA_REQUIRED` |
| Academy e Sportello | funzionanti e **irraggiungibili cliccando** | in navigazione, con 20 test che sorvegliano elenco e pagina resa |
| Ritorno alla superficie del proprio ruolo | viaggio di sola andata dal cruscotto | offerto per ruolo, e solo a chi può usarlo |
| `--undo` della dimostrazione | a senso unico: sedici regole ritirate e nessuna via di ritorno | ritira **e** riapre una versione nuova |
| `new_version` | riciclava la provenienza in `drafted_from_source` | la porta con sé, e riparte dallo stato che essa impone |
| Catalogo `fr` | sedici voci che facevano eco all'italiano al 100 % di copertura | francese reale, verificato leggendo e non contando |
| Comandi su console Windows | morivano su un trattino lungo, dopo aver fatto il lavoro | UTF-8 forzato una volta all'ingresso |
