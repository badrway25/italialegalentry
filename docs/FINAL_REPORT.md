# REPORT FINALE — Italy Legal Entry™

Struttura richiesta dal capitolato §103. Data: **21 settembre 2026**. Ambiente: **sviluppo locale**.

Nessuna operazione è stata eseguita su produzione: `legalitalentry.it` e `app.legalitalentry.it` non
sono stati toccati, nessun DNS è stato modificato, nessun deploy è stato effettuato, nessun database
di produzione è stato scritto, nessuna e-mail reale è stata inviata, nessun form è stato trasmesso a
sistemi esterni. Il sito pubblico esistente è stato solo letto.

---

## 1. Stato

### `CONDITIONALLY_READY`

La piattaforma è costruita, collegata e verificata end-to-end. Non è `LOCAL_RELEASE_READY` per due
ragioni, entrambe esterne al codice e nessuna delle due risolvibile da chi scrive software:

1. **I testi legali italiani ufficiali non esistono nel materiale fornito.** L'«Allegato 1 — Testi
   giuridici» è disponibile solo in francese. Le cinque pagine legali restano non pubblicate, e il
   gate G2 tiene di conseguenza chiusi tutti i form pubblici. Nessun testo è stato tradotto,
   riassunto o inventato: lo stato è `BLOCKED_BY_MISSING_OFFICIAL_SOURCE` e il blocco è implementato,
   non soltanto documentato.

2. **Nessun giurista ha validato le regole giuridiche.** Aggiornato il 22 settembre: **nessuna
   regola è più in vigore.** Undici lo erano senza approvatore, perché il motore potesse essere
   visto funzionare; ora il seed scrive candidate e il database rifiuta una regola approvata o in
   vigore la cui etichetta di approvatore è vuota. Il difetto di sistema è chiuso; il lavoro no.
   Una regola che nessuno ha confermato produce un esito che nessuno può difendere, e infatti la
   piattaforma non ne produce più — il che è corretto, e significa anche che non fa ancora ciò per
   cui esiste.

Tutto il resto è verificabile e verificato — **traduzione compresa**: i quattro cataloghi sono al
**100 %** su 3636 voci, senza voci non tradotte né fuzzy, con l'audit che passa senza errori.

> **Fase successiva conclusa il 22 settembre 2026.** `CONDITIONALLY_READY` descrive la piattaforma
> rispetto al **go-live**, e resta corretto per le due ragioni qui sopra. Rispetto alla
> **pre-produzione** lo stato è `PREPROD_RELEASE_CANDIDATE`: cronologia e repository puliti,
> autorizzazione verificata, dati sensibili redatti. Le due affermazioni non si contraddicono,
> perché rispondono a due domande diverse. `docs/PREPROD_REPORT.md`.

---

## 2. Che cosa è stato costruito

Un ecosistema Django unico, non un sito più una piattaforma:

| Superficie | Contenuto |
|---|---|
| **Sito pubblico istituzionale** | Home, progetto, ecosistema (imprese, istituzioni, università, progetto pilota), percorsi, orientamento, Forum, attualità, FAQ, glossario, vivere in Italia, pagine legali, form |
| **Autenticazione e identità** | Registrazione con tipo dichiarato e verifica umana, login, MFA per chi legge dati di terzi, quindici ruoli, incompatibilità dichiarate, revoca di sessione, instradamento per ruolo |
| **Piattaforma autenticata** | Cruscotto, «La mia situazione», fascicoli, documenti, scadenze, comunicazioni, impresa, selezione autorizzata, sportello digitale, formazione |
| **Back-office** | Console delle fasi, editor delle regole con diff e anteprima, CMS, tassonomie, flag con audit, gestione utenti con protezione contro l'escalation |
| **Servizi di dominio** | 18 operazioni del Blueprint come servizi, ciascuno con la propria autorizzazione interna |

I flussi richiesti funzionano per intero:

```
VISITATORE → ACCOUNT → PROFILAZIONE → ORIENTAMENTO → RULE ENGINE → RISULTATO
           → FASCICOLO → CHECKLIST → DOCUMENTI → FORMAZIONE/SPORTELLO → MONITORAGGIO

IMPRESA → ACCOUNT/VERIFICA → FABBISOGNO → COMPETENZE → FORMAZIONE/PERCORSO
        → ATTORI AUTORIZZATI → STATO/MONITORAGGIO
```

Il primo è stato percorso in un browser reale, cliccando, non costruendo URL.

---

## 3. Architettura, e perché

**Monolite Django modulare, PostgreSQL, reso lato server con miglioramento progressivo.**

| Scelta | Ragione |
|---|---|
| Django confermato (CR-01) | Il documento tecnico nomina un altro stack, ma la base esistente, il team e i vincoli di hosting UE sono Django. Cambiare avrebbe speso il budget in migrazione invece che in funzionalità. |
| Monolite modulare, 28 app | Un fascicolo, una regola, un documento e una notifica si toccano a ogni richiesta. Servizi separati avrebbero introdotto consistenza eventuale dentro un dominio che non la tollera. |
| Servizi di dominio, non endpoint REST (CR-02) | Le 18 operazioni del Blueprint esistono con i loro nomi, come funzioni. Ciascuna applica la propria autorizzazione: una futura API HTTP riuserebbe gli stessi controlli senza riscriverli. |
| Reso lato server | Quattro lingue, RTL reale, WCAG 2.2 AA e una connessione lenta. Una SPA avrebbe spostato il costo sul dispositivo del lettore, che in questo progetto è spesso un telefono. |
| Autorizzazione nella queryset | Una riga che il chiamante non può vedere non viene caricata. Il controllo dopo il fetch è a un refactoring di distanza dal fetch senza controllo. |
| Regole come dati | Le condizioni d'ingresso cambiano per decreto. Una regola nel codice invecchia senza che nessuno se ne accorga. |

---

## 4. Lavoro multi-agente

| Agente | Responsabilità | Proprietà dei file |
|---|---|---|
| Design Council (≈30, sola lettura) | Critica indipendente, tre direzioni artistiche, selezione motivata | nessuna |
| Red team (5 aree) | WCAG, mobile, RTL/i18n, link ed errori, operatività | nessuna |
| Vertical: documents | Requisiti documentali, versioni, decisione, link firmati | `apps/documents/**` |
| Vertical: companies | Profilo impresa con verifica, fabbisogni, competenze, analisi | `apps/companies/**` |
| Vertical: selection | Attore autorizzato, mandato datato, processo, comunicazione d'identità | `apps/selection/**` |
| Vertical: academy | Catalogo, iscrizione, moduli, piano formativo da scarto di competenze | `apps/academy/**` |
| Vertical: helpdesk | Sportello digitale, escalation umana, professionista incaricato | `apps/helpdesk/**` |
| Notifications | Registro chiuso di eventi, preferenze, scansione delle scadenze | `apps/notifications/**` |
| Forum governance | Edizioni, commissioni, tavoli, proposte, progetti, monitoraggio, relazione | `apps/forum/**` |
| Traduzione `it` | 1664 msgid, terminologia allineata alle 1954 voci esistenti | `locale/it/**` |
| Traduzione `en` | 1664 msgid, ortografia britannica, termini d'arte italiani conservati | `locale/en/**` |
| Traduzione `ar` | 1664 msgid, sei forme plurali, cifre occidentali | `locale/ar/**` |

Ogni agente possedeva **soltanto** la propria directory e un proprio database di test; le modifiche
a file condivisi sono state richieste, non eseguite, e applicate dal coordinatore dopo lettura.

Due corsie hanno segnalato difetti **fuori** dal proprio perimetro invece di aggirarli, ed è il
comportamento che questa organizzazione deve produrre: la corsia inglese ha tracciato la collisione
fra l'endonimo «Français» e l'etichetta tradotta, e la corsia documenti ha trovato che una regola di
consegna non dichiarata faceva offrire un link che rispondeva 403. Nessuna delle due ha toccato il
file altrui.

**Il lavoro di coordinamento, svolto direttamente:** rule engine, fascicolo digitale e le sue pagine,
identità e permessi, profilazione, console delle fasi, integrazione, QA e il presente report.

---

## 5. Fase 1 — PASS

Sito istituzionale pubblico, senza contenuti di Fase 3.

| Verifica | Esito |
|---|---|
| Home, progetto, AGAMI, rete, contatto, imprese, partner, attualità | 200 |
| Formulazioni vietate assenti | test di conformità dedicati |
| Nessun indirizzo `@legalitalentry.it` pubblico | test |
| Nessun analytics, nessun font o immagine esterna | test |
| Marchio scritto `Italy Legal Entry™`, mai `®` | test |

## 6. Fase 2 — PASS, con una scadenza

| Verifica | Esito |
|---|---|
| Pagina Forum, iscrizione, conferma | 200 |
| Banner in home, con finestra che si chiude il 2 ottobre 2026 | flag con `enabled_until` |
| Passaggio a «Forum Permanente» dopo l'evento | flag `forum_permanent_mode`, chiuso |
| Nessun nome di persona istituzionale prima del programma definitivo | gate G5 |
| Nessun logo di patrocinio non autorizzato | gate G6 |
| Workspace di cooperazione | costruito, **chiuso** dal flag `virtual_forum` |

## 7. Fase 3 — implementata e gated

Percorsi, dettaglio dei percorsi, orientamento, diplomi, formazione, FAQ, glossario, vivere in
Italia, istituzioni, università, progetto pilota, attenzione alle frodi: **tutte implementate,
tutte dietro il gate `phase3_public`**, che è chiuso sul server interinale e aperto sull'ambiente
di QA. Entrambi sono stati verificati.

---

## 8. Conformità giuridica

| Punto | Stato |
|---|---|
| Testi legali italiani ufficiali | **BLOCCANTE** — Allegato 1 disponibile solo in francese; nessuna traduzione né invenzione |
| Form pubblici | chiusi finché le pagine legali non sono pubblicate (gate G2, implementato) |
| Art. 23 D.Lgs. 286/1998 | mai presentato come titolo del progetto; escluso anche dal seed delle regole (CR-07) |
| Intermediazione di manodopera | mai; nessuna funzione di candidatura, selezione o «matching» |
| Riconoscimento dei titoli | mai rivendicato; il profilo non raccoglie diplomi né istituti |
| Promesse di visto, tempi o esito | nessuna; l'esito più forte riguarda un **percorso**, mai una persona |
| Regole in vigore | **nessuna.** Il seed scrive candidate; una regola vincola qualcuno solo dopo la catena completa, e il database rifiuta una regola approvata senza approvatore registrato |
| Provenienza del contenuto | tracciata per regola: redatta dalla norma, ripresa dalla piattaforma precedente, derivata da essa. Il contenuto ereditato parte da «candidata» e non può saltare la verifica della fonte |
| Date di consultazione delle fonti | assenti sulle quindici fonti reali, e ora **bloccanti**: `SOURCE_VERIFIED` rifiuta una regola le cui fonti non portano data, nome di chi ha verificato, e URL o autorità |
| Giurisdizione delle fonti | dichiarata sulla fonte oltre che sulla regola. Cinque fonti europee erano registrate come italiane — trovato dal rapporto di governance — e sono corrette |
| Risultato prodotto con regole non approvate | la pagina **lo dice**, sopra l'esito, e non mostra le date di consultazione fittizie |

---

## 9. UI/UX

Direzione artistica **A — «Le Registre»**: posizione (ordinale), autorità (attore responsabile),
data e fonte. Cinque ruoli di colore, dieci ruoli tipografici, un solo raggio diverso da zero, una
sola ombra. Nessuna griglia di schede, nessun contatore animato, nessuna barra di avanzamento.

Screenshot: `docs/qa/browser/person_journey_dashboard.png`, `person_journey_documents.png`,
`backoffice_dashboard_gates.png`, più la campagna di riferimento in `docs/qa/visual/`.

Due difetti trovati guardando, non ragionando: la dashboard senza alcun `h1` per chi possiede un
fascicolo, e una colonna di griglia che non si restringeva su telefono. Entrambi corretti.

## 10. Multilingua e RTL — PASS

Quattro lingue (it/fr/en/ar), francese come lingua sorgente. `dir="rtl"` reale, famiglia tipografica
araba dedicata, interlinea e crenatura proprie.

`scripts/qa_rtl_check.py`: **14 coppie pagina/viewport in arabo a 390 e 1440 px, 0 problemi** —
direzione, scorrimento reale, `h1` unico, nessuna proprietà CSS di direzione fisica, regioni di
scorrimento etichettate e raggiungibili da tastiera, nessun errore di console.

## 11. Sicurezza

| Area | Esito |
|---|---|
| Escalation di privilegio dall'admin | chiusa (L-01), 13 test su HTTP reale |
| Ruolo auto-dichiarato alla registrazione | chiuso (L-02): solo `role:person` è concesso su dichiarazione |
| Autorizzazione a livello di oggetto | 13 asserzioni della direttiva §61, tutte passanti |
| Lista e dettaglio in disaccordo | **difetto trovato e corretto** (L-13) |
| Cancellazione bloccata da una relazione dichiarata altrove | **difetto trovato e corretto** (L-14) |
| Assegnazione scaduta o revocata | non concede nulla, verificato al momento della lettura |
| Risposta per ciò che non si può vedere | 404 ovunque, mai 403 |
| Sessioni alla revoca di un ruolo | terminate subito (L-08) |
| MFA | per responsabilità, non per URL (L-10) |
| Separazione dei compiti | `legal_editor` e `legal_approver` incompatibili, applicato in due punti |
| Dati personali nei log | solo identificatori; account anonimizzati pseudonimizzati alla scrittura |
| Rule engine | nessun `eval`, grammatica chiusa, campi dichiarati, profondità e nodi limitati |
| CSP | `self`, nessuno stile inline |
| Cancellazione in cascata nel back-office | **difetto trovato e corretto**: nessun ruolo poteva più cancellare una comunicazione notificata. Il permesso ora è per modello, e `EmailOutbox` — il registro di ciò che è stato inviato — resta fuori dalla concessione |
| Dati personali nel repository | **difetto trovato e corretto**: un indirizzo reale committato come evidenza d'audit. Redatto, con una guardia che cammina su `git ls-files` |

## 12. Accessibilità

WCAG 2.2 AA come obiettivo. Verificato automaticamente: contrasto sui token reali, `h1` unico per
pagina, etichette dei form, regioni di scorrimento raggiungibili, nessun testo sotto 12 px, nessun
bersaglio sotto 24 px, `prefers-reduced-motion`, `forced-colors`.

**Non verificato:** un passaggio con un lettore di schermo reale da parte di una persona. Non è
sostituibile da un test automatico e non è stato fatto.

## 13. Prestazioni

Rimisurate il 21 settembre 2026 su uno **stack simil-produzione**: container Linux, gunicorn con tre
worker, whitenoise con lo storage a manifesto, `DEBUG=False`, impostazioni di produzione,
PostgreSQL dedicato, intestazioni di sicurezza attive. Dettaglio completo, con le due anomalie e
tutto ciò che la misura non dice, in **`docs/STAGING_PERFORMANCE.md`**.

La misura precedente era presa da `runserver` con `DEBUG=1`. Diceva di non essere produzione, il
che era vero ma insufficiente: il server di sviluppo è monoprocesso, serve i file statici senza
compressione né cache e ricarica i template a ogni richiesta. Misurarlo risponde a una domanda che
nessuno ha.

| Misura | Valore |
|---|---|
| Peggior LCP, otto pagine pubbliche × due viewport | **712 ms** (home AR, avvio a freddo) |
| LCP tipico | 170–230 ms |
| Peggior CLS | **0,0046** |
| Payload massimo | 425 kB su 22 richieste |
| Risposta del server, mediana su cinque richieste | 18–42 ms |
| File statici | nome con impronta, `immutable`, gzip **−90 %** |

| Pagina autenticata (`runserver`, misura precedente) | Tempo | Query |
|---|---|---|
| Cruscotto | 104 ms | 37 |
| Elenco dei fascicoli | 39 ms | 14 |
| La mia situazione | 35 ms | 10 |
| I miei documenti | 48 ms | 14 |

Le pagine autenticate **non** sono state rimisurate su staging: il conteggio di query è la cifra
che conta lì, e non cambia con il server davanti.

**Nessun test di carico è stato eseguito, e nessuna misura su rete mobile reale.** Il pubblico di
questa piattaforma accede in prevalenza da telefono in Marocco, e su loopback quella condizione non
esiste. Un punteggio Lighthouse preso da questa macchina sarebbe un numero su questa macchina:
`docs/STAGING_PERFORMANCE.md` §6 spiega perché ci sono i Core Web Vitals grezzi e non un punteggio.

---

## 14. Test automatici

**2976 test raccolti** (`pytest --collect-only`), distribuiti così:

| Area | Test | Area | Test |
|---|---:|---|---:|
| Suite di progetto (`tests/`) | 595 | Pagine pubbliche | 297 |
| Forum (pubblico + governance) | 212 | Area riservata | 188 |
| Ecosistema | 178 | Documenti | 147 |
| Orientamento | 111 | Fascicolo | 100 |
| Percorsi | 98 | Imprese | 97 |
| Rule engine | 95 | Notifiche | 95 |
| Sportello | 94 | Selezione | 82 |
| Account | 81 | Academy | 81 |
| Richieste pubbliche | 72 | Attualità | 68 |
| Glossario | 52 | Community | 48 |
| Integrazioni | 45 | CMS | 45 |
| FAQ | 41 | Vivere in Italia | 33 |
| Partner | 13 | Audit | 8 |

Da 2882 a 2976 in questa fase: **94 test nuovi**, tutti guardie aggiunte dopo un difetto trovato.
Nessuno è copertura di superficie. La suite di progetto è cresciuta di 70 — l'audit di
autorizzazione per forma d'attacco (56), il rifiuto delle impostazioni di produzione (10), la
completezza di `.env.example` (3) — e il rule engine di 18, fra catena di provenienza e versioni.

### Esecuzioni verificate — 22 settembre 2026, sul codice finale

Ogni app e ogni suite di progetto eseguita sul codice finale, in corsie separate con un
`TEST_DATABASE_URL` per corsia. Le corsie non si sovrappongono: i numeri **si sommano**.

| Corsia | Esito |
|---|---|
| `apps/cases` · `accounts` · `orientation` · `pathways` · `portal` | **575 passati**, 3 saltati |
| `apps/rules` · `companies` · `selection` · `academy` · `helpdesk` · `documents` · `forum` · `notifications` · `pages` · `ecosystem` · `enquiries` | **1444 passati, 0 falliti** |
| `tests/security` · `compliance` · `backoffice` · `frontend` · guardie di progetto · 12 app minori | **714 passati**, 1 xfailed — lo shim dei token, un debito che deve fallire finché la migrazione non finisce |
| `tests/i18n` (cataloghi, plurali, RTL, integrità di pagina, testi bloccati) | **233 passati, 0 falliti** |

Le guardie aggiunte dopo un difetto, eseguite singolarmente durante lo sviluppo:

| Guardia | Esito |
|---|---|
| `tests/security/test_authorization_audit.py` | **56 passati** — dieci ruoli × sei forme d'attacco |
| `tests/security/test_production_settings_refuse_to_start.py` | **10 passati**, ciascuno in un processo figlio |
| `tests/test_env_example_is_complete.py` | **3 passati** — e ha già ripagato, fermando una variabile introdotta due minuti prima |
| `apps/rules/tests/test_provenance_chain.py` | **18 passati**, di cui due verificano che sia il **database** a rifiutare |
| `apps/rules/tests/test_new_version.py` | **6 passati** |
| `apps/cases/tests/test_demonstration_notice.py` | **6 passati**, compreso il caso di controllo |
| `apps/portal/tests/test_admin_cascade.py` | **5 passati** |
| `tests/test_migration_drift.py` | **2 passati**, su tutte e 28 le app |
| `tests/compliance/test_no_personal_data_in_repository.py` | **4 passati**, tutti per forma e nessuno per valore |

Controlli che non sono test:

| Controllo | Esito |
|---|---|
| `manage.py check` | nessun problema |
| `manage.py check --deploy` con ambiente di produzione corretto | **nessun avviso** — prima ne aveva uno |
| `manage.py makemigrations --check` | nessuna modifica |
| `ruff check apps tests scripts config manage.py` | pulito |
| `scripts/i18n_audit.py` | it · en · ar · fr tutte **3636/3636, 100,0 %, OK** |
| `scripts/history_secret_scan.py` | 2131 blob, **0 indirizzi e-mail di terzi** |
| `scripts/css_class_audit.py` | 382 classi senza regola, tetto 382 |
| `scripts/qa_rtl_check.py` | 14 coppie pagina/viewport in arabo, **0 problemi** |
| `scripts/qa_browser_crawl.py` | **804 pagine, 276 link, 0 problemi, 0 link rotti** |
| `manage.py rules_pending_review --strict` | esce **0**: nessuna regola in vigore senza approvatore, perché nessuna è in vigore |
| Percorso persona nel browser | 9 regole, **6 fonti numerate**, 9 righe di checklist, pre-valutazione riproducibile, avviso di dimostrazione presente |
| `scripts/qa_journey_tail.py` | Academy e Sportello raggiunti dal cruscotto, un solo `h1` ciascuno, 0 errori di console |
| Percorso impresa nel browser | 4 fabbisogni, 17 competenze, stato «VÉRIFIÉE», analisi territoriale rifiutata all'impresa |

### Un'osservazione operativa

Due esecuzioni di pytest simultanee si bloccano a vicenda: `--reuse-db` le porta entrambe su
`test_ile`, una resta inattiva dentro una transazione tenendo un lock di riga su `auth_group` e
l'altra si blocca per sempre inserendo `role:person`. Osservato due volte, per più di un'ora
ciascuna, senza alcun timeout. Ogni esecuzione concorrente richiede il proprio
`TEST_DATABASE_URL`; è documentato in `docs/QA_REPORT.md` §7.

---

## 14bis. Classificazione di ogni funzionalità richiesta

Le cinque classificazioni chieste dalla direttiva, applicate a ciascuna voce del suo elenco.

**Il criterio, senza sconti.** Una funzionalità è *IMPLEMENTATA E FUNZIONANTE* solo se è stata
**esercitata**: da un test d'integrazione HTTP, da un test di dominio contro il servizio che
l'interfaccia chiama davvero, o nel browser. L'esistenza del modello, della pagina, del mockup o
della documentazione non conta.

| Funzionalità | Classificazione | Prova |
|---|---|---|
| Account e autenticazione | **IMPLEMENTATA E FUNZIONANTE** | allauth, registrazione con tipo dichiarato, verifica umana, login, logout, reimpostazione |
| Ruoli, permessi, autorizzazione a livello di oggetto | **IMPLEMENTATA E FUNZIONANTE** | 15 ruoli, registro deny-by-default, 13 asserzioni §61, incompatibilità applicata in due punti |
| Onboarding e profilazione della persona | **IMPLEMENTATA E FUNZIONANTE** | «Ma situation», 18 test, verificata nel browser; ogni campo dichiara che cosa lo legge |
| Orientamento dinamico | **IMPLEMENTATA E FUNZIONANTE** | Il salvataggio della situazione rivaluta il fascicolo; 8 test di ri-valutazione; l'esito precedente è conservato |
| Rule Engine versionato | **IMPLEMENTATA E FUNZIONANTE** — *contenuto GATED* | 77 test; versioni, quattro occhi, finestre di validità, snapshot, replay. **Le 11 regole in vigore non sono state validate da un giurista** |
| Risultati spiegabili con fonti | **IMPLEMENTATA E FUNZIONANTE** | 5 fonti numerate con riferimento puntuale sulla pagina resa; pagina di pre-valutazione con regole applicate e replay |
| Fascicolo digitale | **IMPLEMENTATA E FUNZIONANTE** | 94 test; elenco e dettaglio da una sola queryset; verificato nel browser cliccando |
| Checklist | **IMPLEMENTATA E FUNZIONANTE** | Responsabile obbligatorio su ogni riga; la persona può avanzare solo ciò che le compete |
| Documenti privati e sicuri | **IMPLEMENTATA E FUNZIONANTE** | 147 test; requisiti, versioni che si sostituiscono, link firmati, classe di accesso, 7 stati |
| Timeline / stato del percorso | **IMPLEMENTATA E FUNZIONANTE** | 11 stati, tabella di transizione dichiarata, audit su ogni cambiamento, sequenza resa |
| Compiti e scadenze | **IMPLEMENTATA E FUNZIONANTE** | Scadenze sul fascicolo e nel portale; `notifications_scan_deadlines` notifica una volta per stato |
| Notifiche | **IMPLEMENTATA E FUNZIONANTE** | 95 test; registro chiuso di 10 eventi, preferenze per categoria, e-mail solo in coda, verificata in sviluppo |
| Sportello digitale ed escalation umana | **IMPLEMENTATA E FUNZIONANTE** | 94 test; coda, mandato al professionista, revoca, messaggi |
| Academy / formazione | **IMPLEMENTATA E FUNZIONANTE** | 81 test; catalogo, iscrizione, moduli, piano formativo dallo scarto di competenze |
| Imprese / B2B e fabbisogni | **IMPLEMENTATA E FUNZIONANTE** | 97 test; dichiarazione con verifica, fabbisogni, competenze, analisi territoriale. **Nessun criterio d'età, e non se ne può digitare uno** |
| Workflow degli attori autorizzati | **IMPLEMENTATA E FUNZIONANTE** | 82 test; attore, mandato datato, processo, comunicazione d'identità decisa dalla persona |
| Area professionale / operatore | **IMPLEMENTATA E FUNZIONANTE** | Coda dello sportello + pagine del fascicolo assegnato; un mandato scaduto o revocato chiude l'accesso |
| Forum / cooperazione secondo le fasi | **IMPLEMENTATA MA CHIUSA DA UN GATE** | 212 test; 11 rotte, tutte 503 dietro `virtual_forum` per ogni ruolo, con un test di controllo che le apre a 200 |
| Amministrazione / CMS | **IMPLEMENTATA E FUNZIONANTE** | Console delle fasi, editor delle regole con diff e anteprima, CMS, tassonomie, flag con audit |
| Log di audit | **IMPLEMENTATA E FUNZIONANTE** | Eventi da cases, documents, helpdesk, selection, accounts, orientation, rules, API; solo identificatori nel flusso di log |
| Consensi e privacy | **IMPLEMENTATA E FUNZIONANTE** | Consenso registrato e revocabile, esportazione art. 15/20 completa, anonimizzazione art. 17 |
| i18n IT/FR/EN/AR | **IMPLEMENTATA E FUNZIONANTE** | Quattro cataloghi al **100 %** (3618 msgid ciascuno), zero non tradotti, zero fuzzy, audit senza errori. I 1664 msgid dei nuovi moduli sono stati tradotti da una corsia per lingua, con l'audit come criterio d'accettazione |
| RTL reale | **IMPLEMENTATA E FUNZIONANTE** | 14 coppie pagina/viewport in arabo, 0 problemi; caratteri, interlinea e proprietà logiche propri |
| Responsive / mobile | **IMPLEMENTATA E FUNZIONANTE** | Nessuno scorrimento orizzontale a 390 px; campagna a 10 viewport |
| Accessibilità | **IMPLEMENTATA E FUNZIONANTE** — *con una riserva* | Contrasto sui token reali, `h1` unico, bersagli ≥ 24 px o distanziati, regioni di scorrimento etichettate. **Nessun passaggio con un lettore di schermo reale** |
| Sicurezza (OWASP, CSP, MFA) | **IMPLEMENTATA E FUNZIONANTE** | 10 lacune del modello dei permessi chiuse, più **due** che non erano note (L-13, trovata da un'asserzione; L-14, trovata da un test che asseriva una cancellazione); CSP `self`; MFA per responsabilità, **applicata anche all'area riservata** e non solo al back-office |
| Test unitari, d'integrazione, E2E, di permesso | **IMPLEMENTATA E FUNZIONANTE** | **2976** test raccolti; una suite dedicata alle 13 asserzioni; **cinque** script di verifica nel browser |
| Post-ingresso e inclusione | **PARZIALE** | Gli stati esistono e transitano; non esiste ancora contenuto proprio della fase |
| Workspace università e ricerca | **NON IMPLEMENTATA** | Esiste la pagina pubblica; nessuno spazio autenticato dedicato |
| Modello di convenzione (`Agreement`) | **NON IMPLEMENTATA** | Il perimetro istituzionale non è verificabile dal codice (L-11) |
| Pagine legali italiane ufficiali | **BLOCCATA DALLA FONTE** | `BLOCKED_BY_MISSING_OFFICIAL_SOURCE`: l'Allegato 1 esiste solo in francese. Il blocco è implementato, non soltanto documentato |

### Che cosa non è stato classificato «funzionante», e perché

Tre voci sono **parziali** e due **non implementate**, ed è preferibile leggerle così che vederle
arrotondate verso l'alto:

- **Post-ingresso** — gli stati si attraversano, il contenuto della fase non esiste.
- **Accessibilità** — tutto ciò che una macchina può verificare è verificato; ciò che solo una
  persona con un lettore di schermo può dire non è stato fatto, e non è sostituibile.
- **Università e ricerca**, **convenzione istituzionale** — non costruite. Dirlo è più utile che
  presentare un modello vuoto come un'architettura.

---

## 15. Problemi noti

| # | Problema | Gravità |
|---|---|---|
| 1 | ~~Le 11 regole in vigore non sono state validate da un giurista~~ — **chiuso come difetto, aperto come lavoro**: nessuna regola è più in vigore, il database rifiuta una regola approvata senza approvatore, e le 16 candidate attendono un giurista | risolto strutturalmente; la revisione resta da fare |
| 2 | Nessuna fonte ha una data di consultazione **reale** — e ora questo blocca la catena invece di essere una nota: `SOURCE_VERIFIED` rifiuta una regola le cui fonti non portano data, nome e URL o autorità | media, ma non più silenziosa |
| 3 | `role:staff` cumula ancora redazione e accesso ai dati delle imprese (L-03) | media |
| 4 | Nessun modello di convenzione: il perimetro istituzionale non è verificabile dal codice (L-11) | media |
| 5 | Nessuna verifica del consenso alla lettura per la visibilità impresa → persona (L-12) | alta quando arriverà la Fase P1 |
| 6 | Nessuna vista di ricerca dedicata per l'audit | bassa |
| 7 | Il modulo Post-ingresso ha gli stati ma non il contenuto | bassa |
| 8 | Nessun workspace dedicato a università e ricerca | bassa |
| 9 | Il cruscotto esegue 37 query; accettabile ma migliorabile | bassa |
| 10 | ~~1664 stringhe non tradotte~~ — **chiuso**: i quattro cataloghi sono al 100 %, audit senza errori | risolto |
| 11 | 382 classi nominate nei template senza regola CSS. Enumerate con un tetto che solo scende; due erano difetti reali e sono corrette | bassa |
| 12 | Il seed di `selection` crea un'organizzazione e un'appartenenza ma nessun `CompanyProfile`, quindi il percorso impresa si ferma a «dichiara la tua impresa» finché non si esegue `companies_demo` | bassa |
| 13 | Nessun motore antivirus installato: ogni file risulta «non analizzato», e la regola di consegna lo dichiara invece di offrire un link che risponde 403 | media |
| 14 | **Ambiente legacy di test**: solo riferimento, non fa parte di questo repository (decisione della titolarità, 11 ottobre 2026); dettagli nel registro privato | **fuori progetto** |
| 15 | Le traduzioni non sono state rilette da una persona. L'audit verifica la forma, non la resa; per un testo istituzionale in arabo serve una rilettura umana prima della pubblicazione | media |
| 16 | ~~La **cronologia Git** contiene ancora i due PDF sorgente~~ — **chiuso** il 21/09/2026 con due passate di `filter-branch`, copia probatoria fuori dal repository e scansione successiva a zero indirizzi. Vedere `docs/security/HISTORY_REWRITE_2026-09-21.md`. *(voce storica: i due PDF sorgente (`docs/source/`, dal primo commit) e la versione non redatta delle catture d'audit. Il repository non ha remote e non è mai stato pubblicato)* | risolto |
| 17 | **Nessun passaggio con un lettore di schermo reale.** Checklist in `docs/HUMAN_QA_CHECKLIST.md`, dove **ogni riga è `HUMAN_QA_REQUIRED`** | media |
| 18 | Nessun test di carico, e nessuna misura su rete mobile reale. Le prestazioni sono misurate su uno stack simil-produzione in loopback: `docs/STAGING_PERFORMANCE.md` §7 dice che cosa quella misura non copre | media |
| 19 | I sette termini di governance decisi dalle corsie di traduzione non sono ancora righe **vincolanti** del glossario: `docs/I18N_RTL.md` §5bis li registra fuori dalla tabella che il test confronta con i cataloghi | bassa |

## 16. Bloccanti

Da distinguere, perché sono due liste diverse e confonderle è il modo più rapido per bloccare
lavoro che si potrebbe fare.

### Alla pre-produzione: **nessuno**

Le tre condizioni poste dalla direttiva di irrigidimento sono soddisfatte — cronologia e repository
puliti, autorizzazione verificata, dati sensibili redatti. Lo stato è `PREPROD_RELEASE_CANDIDATE`,
e il dettaglio è in `docs/PREPROD_REPORT.md`.

### Al go-live: **sei**, e quattro non dipendono da chi scrive software

1. **Testi legali italiani ufficiali.** Finché non arrivano, le pagine legali non si pubblicano e i
   form pubblici restano chiusi. Non è aggirabile senza violare il mandato.
2. **Revisione giuridica delle regole**, e verifica delle quindici fonti alla fonte ufficiale.
   Nessuna regola è in vigore, quindi oggi la piattaforma non afferma nulla di giuridico — ma non
   afferma nemmeno ciò per cui esiste.
3. **Conferma dell'hosting nell'Unione europea** (CR-08, aperto). Checklist di dodici punti in
   `docs/DEPLOYMENT_READINESS.md` §3, compresa la regione dei **backup**, che è l'errore classico:
   applicazione a Francoforte, backup replicati fuori Unione per impostazione predefinita.
4. **Decisione sull'ambiente legacy di test**: presa dalla titolarità l'11 ottobre 2026 — l'ambiente
   è solo un riferimento e non fa parte di questo repository.
5. **Rilettura umana delle traduzioni** prima di pubblicare in arabo, italiano e inglese. L'audit
   verifica la forma di 3636 voci per lingua; non verifica come si leggono. Per un sito
   istituzionale rivolto a un pubblico che legge l'arabo su un telefono, non è un dettaglio.
6. **Passaggio di accessibilità con un lettore di schermo reale.** `docs/HUMAN_QA_CHECKLIST.md`,
   dove ogni riga è `HUMAN_QA_REQUIRED`.

### Già chiuso

~~Riscrivere la cronologia prima di aggiungere un remote~~ — **fatto** il 21 settembre 2026, in due
passate. Resta una conseguenza da non dimenticare: **ogni hash citato prima di quella data non
esiste più**. I riferimenti dentro il repository sono stati aggiornati; quelli in materiale già
consegnato fuori dal repository no, e non possono esserlo.

---

## 17. Git

Ramo `main`, nessun remote. Lo stato preciso di HEAD è nel messaggio finale, perché cambia a ogni
commit e un documento che lo fissa mente il giorno dopo.

**La cronologia è stata riscritta il 21 settembre 2026, quindi ogni hash citato prima di quella
data non esiste più.** Il vecchio HEAD era `53d9b46`. Sono usciti da ogni commit: i due PDF sorgente
del committente con le loro estrazioni testuali integrali, un dato personale di un terzo (rilievo
nel registro privato) e quattordici screenshot committati per errore.
`docs/security/HISTORY_REWRITE_2026-09-21.md` dice che cosa è stato tolto, che cosa è stato
**lasciato** e perché; `docs/security/HISTORY_SCAN_AFTER.md` riporta la scansione successiva: 2131
blob, **zero indirizzi e-mail di terzi**.

La cronologia precedente esiste in un bundle Git fuori dal repository, con le sue regole d'uso
scritte accanto. Contiene tutto ciò che è stato rimosso, per costruzione.

## 18. Comandi per avviare la piattaforma in locale

```bash
cd C:/tmp/italylegalentry

# 1. Database (PostgreSQL 17 in Docker, porta 5439)
docker compose up -d db          # `up`, non `start`: alza max_connections a 300
                                 # (`docker restart` conserva il vecchio limite)

# 2. Dipendenze
.venv/Scripts/python.exe -m pip install -r requirements/dev.txt

# 3. Schema e dati di configurazione
.venv/Scripts/python.exe manage.py migrate
.venv/Scripts/python.exe manage.py seed_all

# 4. Regole giuridiche (idempotente). NESSUNA entra in vigore: il seed scrive candidate.
.venv/Scripts/python.exe manage.py seed_legal_rules
.venv/Scripts/python.exe manage.py rules_pending_review
#    ^ per ogni regola: fonte, riferimento, giurisdizione, validità, versione, revisore,
#      stato, provenienza — e che cosa le manca per il passo successivo.
#      Con --strict esce 1 solo se qualcosa è in vigore senza approvatore o su fonte
#      non verificata, cioè se qualcosa è entrato aggirando il servizio.

# 4bis. Per VEDERE il motore funzionare in locale. Rifiuta di partire dove i dati
#       dimostrativi non sono ammessi, e marchia ogni regola con un approvatore
#       dichiaratamente fittizio che finisce nello snapshot di ogni pre-valutazione.
.venv/Scripts/python.exe manage.py rules_activate_demonstration
#       …e per tornare indietro:
.venv/Scripts/python.exe manage.py rules_activate_demonstration --undo

# 5. Server di sviluppo — Fase 1/2, contenuti Fase 3 chiusi
.venv/Scripts/python.exe manage.py runserver 127.0.0.1:8770 --noreload
#    `--noreload` non è un dettaglio se si eseguono le verifiche nel browser: il
#    ricaricatore chiude le connessioni in corso a ogni salvataggio, e una scansione
#    eseguita durante una modifica ha riportato 770 pagine «con problemi» su 804.

# 6. Ambiente di QA — Fase 3 aperta, form sbloccati dal flag tracciato
#    La password dei tre account QA viene da ILE_QA_PASSWORD, nel .env locale (mai nel
#    repository, mai stampata): senza, lo script si rifiuta di partire (.env.example).
DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_qa \
  .venv/Scripts/python.exe scripts/qa_prepare_env.py
DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_qa \
  ILE_REFERENCE_DATE=2026-10-03 \
  .venv/Scripts/python.exe manage.py runserver 127.0.0.1:8771 --noreload
#    La data di riferimento apre le finestre dei flag di Fase 3, che partono dal
#    2 ottobre 2026: senza di essa il flag è abilitato ma non ancora attivo.

# 7. Dati dimostrativi (solo in sviluppo; `ILE_SEED_DEMONSTRATION_DATA` li governa)
.venv/Scripts/python.exe manage.py companies_demo --account seed-company@example.test --verified

# 8. Test — UN database per esecuzione concorrente, altrimenti si bloccano a vicenda
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_t_main \
  .venv/Scripts/python.exe -m pytest -q
#    Due esecuzioni sullo stesso database si bloccano su un lock di riga in `auth_group`
#    e non scadono mai. Vedere docs/QA_REPORT.md §7.

# 9. Verifiche nel browser (server già avviati, a modifiche ferme)
.venv/Scripts/python.exe scripts/qa_person_journey.py  http://127.0.0.1:8770
.venv/Scripts/python.exe scripts/qa_company_journey.py http://127.0.0.1:8770
.venv/Scripts/python.exe scripts/qa_rtl_check.py       http://127.0.0.1:8770
.venv/Scripts/python.exe scripts/qa_capture_platform.py http://127.0.0.1:8770
.venv/Scripts/python.exe scripts/qa_browser_crawl.py   http://127.0.0.1:8771 phase3

# 10. Ambiente simil-produzione (Linux, gunicorn, whitenoise, DEBUG=False) su 8900.
#     NON è produzione: un solo host, niente TLS davanti, dati sintetici. Ogni numero
#     misurato qui va letto come «staging», mai come produzione.
docker exec italylegalentry-db-1 psql -U ile -d postgres -c "CREATE DATABASE ile_staging OWNER ile;"
docker compose -f docker-compose.yml -f docker-compose.staging.yml --profile staging up -d --build
#     …e per fermarlo:
docker compose -f docker-compose.yml -f docker-compose.staging.yml --profile staging down

# 11. Controlli che non richiedono un server
.venv/Scripts/python.exe scripts/i18n_audit.py          # copertura dei cataloghi
.venv/Scripts/python.exe scripts/css_class_audit.py     # classi senza regola
.venv/Scripts/python.exe -m ruff check apps tests scripts config
.venv/Scripts/python.exe manage.py check
.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
```

**Back-office:** `http://127.0.0.1:8770/backoffice/` — la console delle fasi è in testa alla pagina
iniziale, e l'editor delle regole in «Regole giuridiche».

**Account locali** creati dai seed dimostrativi, tutti su `@example.test` (dominio riservato da
RFC 6761, mai instradabile): `seed-person`, `seed-company`, `seed-actor`, `seed-actor-lapsed`,
`demo-professionnel`, `demo-operateur`. Nessuna password di questi account esiste in produzione.
