# Interruzione dell'anteprima V5 del 2 ottobre 2026 — diagnosi, correzione, prova

| | |
|---|---|
| **Oggetto** | L'anteprima `http://127.0.0.1:8780/__design-v5/` ha risposto `500 OperationalError … FATAL: sorry, too many clients already` dalle 15:36 alle 15:53 e di nuovo dalle 17:20 alle 17:27 del 2 ottobre 2026. Direttiva del proprietario del 2 ottobre, §11–§12: diagnosticare, non alzare il limite, rendere stabile l'anteprima |
| **Ruolo** | Ingegnere infra/Django dell'anteprima (stream B/D) |
| **Data** | 2 ottobre 2026, 19:00–21:30 (ora locale; PostgreSQL scrive in UTC, due ore indietro) |
| **Esito** | **Causa trovata e riprodotta; corretta nella riga di proprietà dell'anteprima.** Una raffica di file di prova non apre più alcuna connessione; il server dell'anteprima non ne tiene mai più di otto, e zero a riposo. Il limite del server PostgreSQL non è stato toccato |
| **Strumenti** | server propri della worktree su `127.0.0.1:8784–8786`, stesso ambiente del server ufficiale (`DATABASE_URL=…/ile_v5`, `ILE_DESIGN_PREVIEW=1`, `runserver --noreload`), avviati e spenti a ogni misura; `pg_stat_activity` e `pg_settings` in sola lettura; `Get-NetTCPConnection` e `Win32_Process`; Playwright headless, profili propri sotto `C:/tmp/ile_v5_council/.profiles/stream-b/`; corsia di test `ile_lane4` |
| **Lucchetto** | `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` atteso in ciclo (30 s, fino a 25 min) prima di ogni server, raffica, browser ed esecuzione di test: assente a ogni attesa |
| **Prove** | fuori dal repository, `C:/tmp/ile_v5_council/.work/stream-b/`: `harness.py` (server, raffiche, censimento), `probe_server.py` (osservatore nel processo), `browser_probe.py`, `abort_probe.py`, `named_census.py`, `queries_probe.py`, `log_minutes.py`, `log_pages.py`, `shots.py`, `hub_shots.py`, `measure_links.py`, `gate.py`; risultati in `results.jsonl`, `matrix-*.txt`, `hub-*.txt`, `browser-final.txt`, `final2.txt`; catture in `shots-final/` |

Il server ufficiale su 8780 non è stato fermato né riavviato, il Chrome del proprietario (9223) e quello di QA (9222) non sono stati toccati, nessuna sessione PostgreSQL altrui è stata terminata, nessuna impostazione del server PostgreSQL è stata cambiata. Niente di ciò che segue è una decisione di design.

**Aggiornamento del 4 ottobre 2026**, dopo la revisione indipendente del commit `da75812` (`PREVIEW_REVIEW_W2.md`, PASS_WITH_FIXES): il rilievo maggiore W2-1 — il tetto perdeva un posto per sempre quando `request_finished` non arrivava — è corretto e rimisurato (§3.5, §5, §7); i rilievi minori W2-3 e W2-4 sono annotati dove appartengono (§1.1, §2.3, §6). Le aggiunte di quel giorno sono marcate *(4 ottobre …)*; il resto della nota è quello del 2 ottobre.

---

## 0. In breve

**La causa.** Su questi server di sviluppo ogni chiamata a una vista apre una connessione a PostgreSQL prima ancora che la vista giri — `ATOMIC_REQUESTS = True` la avvolge in una transazione — anche quando la vista spedisce un foglio di stile di una maquette. `runserver` dà un thread a ogni socket, senza limite; la connessione appartiene al thread e, con `CONN_MAX_AGE = 60`, non viene chiusa alla fine della richiesta. Quando il socket si chiude il thread finisce, e **nessuno chiude la connessione di un thread finito**: resta aperta, di nessuno, finché il garbage collector di Python non trova per caso l'oggetto che la tiene — in un server fermo, mai.

**Il 2 ottobre.** Cinque agenti di revisione catturavano le pagine dell'anteprima con browser headless, un profilo nuovo per ogni cattura: ogni caricamento di pagina apriva sei socket o più, cioè sei thread, cioè sei connessioni e più, che sopravvivevano al browser. Negli 80 secondi prima del primo errore il server ha ricevuto 60 caricamenti di pagina (1 353 richieste). I 300 posti di PostgreSQL sono finiti — per l'anteprima e per ogni altro server di sviluppo e corsia di test sullo stesso PostgreSQL.

**La correzione** (tutta nella riga di proprietà dell'anteprima, §5):

1. nessuna vista dell'anteprima chiede una transazione: un file di prova non apre più una connessione, e nemmeno i due selettori, che ora non leggono nulla;
2. sul server dell'anteprima una connessione vive quanto la sua richiesta (`CONN_MAX_AGE = 0`);
3. un tetto: mai più di **8** connessioni dal server dell'anteprima, qualunque cosa arrivi (`designpreview.middleware`), misurabile con una riga di SQL perché le connessioni portano un nome.

**I numeri.**

| | Com'era | Ora |
|---|---|---|
| 200 file di prova, 32 alla volta | picco 91 connessioni, **85 lasciate** (invariate 75 s dopo) | **0** durante, **0** dopo |
| 600 file di prova, 64 alla volta | fermata dalla sicurezza a 271 richieste: 155 connessioni, il server PostgreSQL a 234 di 300 | **0** durante, **0** dopo, 600 risposte 200 |
| 5 browser headless che caricano una maquette | 32 connessioni, ancora 32 con le pagine aperte da 70 s, ancora 32 a browser chiusi | **0** |
| 600 richieste all'hub (che legge il database), 64 alla volta | 109 di picco e 61 lasciate già con 200 richieste a 32 | picco **8**, **0** dopo, 600 risposte 200 |
| Connessioni del server a riposo | 48 su 8780 alle 20:33, senza un solo thread di richiesta vivo | **0** |

---

## 1. Il modello di connessione dei server di sviluppo

### 1.1 Le impostazioni

`config/settings/base.py` (righe 154–156), valide in sviluppo e in produzione; `config/settings/dev.py` non toccava il database prima di oggi. `config/settings/test.py` sostituisce la voce `default` per intero: sotto i test `CONN_MAX_AGE` ricade sul valore di Django, 0.

| Impostazione | Valore | Che cosa comporta |
|---|---|---|
| `DATABASES["default"]` | `env.db_url("DATABASE_URL", …)` — PostgreSQL 17.11 nel contenitore `italylegalentry-db-1`, porta 5439 | un solo database per processo |
| `CONN_MAX_AGE` | `env.int("DB_CONN_MAX_AGE", default=60)` | una connessione è tenuta per essere riusata **dallo stesso thread** fino a 60 s dopo l'apertura |
| `ATOMIC_REQUESTS` | `True` | ogni vista è avvolta in `transaction.atomic()` (`django/core/handlers/base.py:345–354`): entrarci chiama `ensure_connection()`, cioè **apre la connessione prima che la vista giri** |
| `CONN_HEALTH_CHECKS` | non impostato → `False` | nessun controllo prima del riuso |
| `OPTIONS["pool"]` | assente; `psycopg_pool` non è installato | **nessun pool**: psycopg 3.3.5 apre una connessione per ogni wrapper di Django, e Django ha un wrapper per thread |

Versioni: Python 3.13.5, Django 5.2.17, psycopg 3.3.5 (binary), asgiref 3.12.1.

*(4 ottobre, revisione W2-3.)* Il repository lo sapeva: `.env.example`, righe 32–33, dal 21 settembre (`156e41a`) — «Secondi di vita di una connessione al database riusata. 0 = nessun riuso.», `DB_CONN_MAX_AGE=0`. Il `.env` del worktree `design-v5` è una copia precedente a quella riga, e nemmeno quello di `main` ce l'ha: i server giravano con i 60 s di `base.py`. Con quella riga ogni richiesta avrebbe aperto e chiuso la propria connessione (il candidato 1 del §3.3).

### 1.2 La catena dei middleware: chi legge il database, e quando

Misurato con `queries_probe.py` (impostazioni dev, database `ile_v5`) e letto nel codice.

| Middleware | Legge il database? |
|---|---|
| `SecurityMiddleware`, `WhiteNoiseMiddleware`, `TextGZipMiddleware`, `RequestIDMiddleware`, `LocaleMiddleware`, `LanguageCookieMiddleware`, `CommonMiddleware`, `CsrfViewMiddleware`, `XFrameOptionsMiddleware`, `CSPMiddleware`, `BackofficeCSPMiddleware`, `ExtraSecurityHeadersMiddleware` | mai |
| `SessionMiddleware`, `AuthenticationMiddleware`, `MessageMiddleware` | pigri: solo se la sessione o l'utente vengono usati **e** la richiesta porta il cookie di sessione |
| `allauth.account.middleware.AccountMiddleware` | guarda la sessione a ogni risposta HTML 2xx che sia una navigazione (`Sec-Fetch-Dest: document` o assente): una lettura di `django_session` se c'è il cookie; nulla per un iframe o una sottorisorsa |
| `accounts.middleware.BackofficeMFAMiddleware` | solo sotto `/backoffice/` e `/espace-reserve/` |
| `cms.middleware.LegacyURLMiddleware` | **a ogni 404**: una lettura di `cms_redirect` — anche per un file di prova che manca |
| il contesto dei template (`core.context_processors.site`) | a ogni template reso con la richiesta: `SiteSettings`, i flag |
| **`ATOMIC_REQUESTS`** (non è un middleware, ma è ciò che conta) | **a ogni vista**, sempre: apre la connessione senza eseguire una sola istruzione |

Per risposta, prima della correzione:

| Richiesta | Connessione aperta | Istruzioni vere |
|---|---|---|
| hub | sì | 3 `SELECT` (flag, `SiteSettings`, documenti legali) |
| selettore (primo schermo, tipografico), anche il 400 | sì | 1 `SELECT` (`SiteSettings`, dal contesto: il template non lo stampa) |
| **file di prova** — HTML, CSS, font, immagine | **sì** | **nessuna**: la connessione si apre per la transazione e basta |
| file di prova mancante (404) | sì | 1 `SELECT` (`cms_redirect`) |
| `/static/…` | no (lo serve `StaticFilesHandler`, fuori dalla catena) | — |
| `/fr/` | sì | 12 `SELECT` |

In `pg_stat_activity` le connessioni dei file di prova si riconoscono: stato `idle`, **colonna `query` vuota** — non hanno mai eseguito nulla. Alle 19:04 se ne vedevano, fra le altre, due gruppi di sei, ciascuno aperto nello stesso secondo: i sei socket di un browser.

### 1.3 `runserver`: un thread per socket, senza limite

`django/core/servers/basehttp.py:256–281`: `runserver` costruisce `type("WSGIServer", (socketserver.ThreadingMixIn, WSGIServer), {})` con `daemon_threads = True`.

* **Un processo** (due nell'elenco dei processi: `python.exe` del venv è un lanciatore, l'interprete è suo figlio). Con `--noreload` non c'è il processo del ricaricatore.
* **Un thread per connessione TCP accettata**, non per richiesta, e **nessun limite** al loro numero. La coda d'ascolto è di 10 (`request_queue_size`): a 64 connessioni simultanee qualche client viene rifiutato dal sistema operativo (misurato: 2–3 su 600), e non c'entra con il database.
* **Keep-alive**: `WSGIRequestHandler.handle()` (righe 226–235) serve una richiesta dopo l'altra sullo stesso socket finché il client lo tiene aperto; il thread vive quanto il socket. Fa eccezione una risposta senza `Content-Length`: un documento HTML di prova passa compresso in streaming, esce con `Connection: close`, e il suo socket — con il suo thread — finisce lì.
* Il thread principale non tiene connessioni: `runserver` chiude quella aperta dal controllo delle migrazioni (`runserver.py:137–140`).
* Non è `ThreadedWSGIServer` (righe 86–111), che chiude le connessioni dopo ogni richiesta: quello lo usano soltanto i test (`live_server`), che per di più girano con durata zero (§1.1). **Per questo nessun test se n'era accorto**: il difetto esiste soltanto dove `runserver` incontra `CONN_MAX_AGE = 60`, cioè su ogni server di sviluppo e in nessun test.

### 1.4 Quando una connessione viene chiusa — e quando no

La connessione di Django è locale al thread (`asgiref.local.Local(thread_critical=True)`).

* `close_old_connections` è collegato a `request_started` e `request_finished` (`django/db/__init__.py:57–63`) e chiude la connessione **del thread che sta servendo la richiesta**, se è inutilizzabile o più vecchia di `CONN_MAX_AGE` (`close_if_unusable_or_obsolete`, `base/base.py:591–616`).
* Con `CONN_MAX_AGE = 60`, alla fine di una richiesta la connessione ha pochi millisecondi: **resta aperta**.
* Un thread fermo ad aspettare la prossima richiesta sul suo socket non esegue alcun ciclo di richiesta: la sua connessione resta aperta **oltre** i 60 s, finché il client tiene il socket. `CONN_MAX_AGE` limita l'età al riuso, non la vita.
* Quando il socket si chiude il thread finisce. Il wrapper della connessione è in un ciclo di riferimenti (`wrapper.ops.connection` è il wrapper stesso): non muore con il thread, aspetta il garbage collector ciclico; e la connessione a PostgreSQL si chiude soltanto quando l'oggetto viene distrutto.
* Il collettore gira quando il processo alloca. **In un server che non riceve richieste non gira**: gli orfani restano. PostgreSQL non li scade da sé: `idle_session_timeout = 0`.

Con `CONN_MAX_AGE = 0` la stessa `close_if_unusable_or_obsolete` chiude la connessione a `request_finished`, sempre: alla fine di ogni richiesta, comunque finisca (wsgiref chiama `close()` sulla risposta anche quando il client ha riattaccato).

---

## 2. Censimento, e ricostruzione dell'interruzione

### 2.1 I limiti del server PostgreSQL

| | |
|---|---|
| `max_connections` | 300 |
| `superuser_reserved_connections` | 3 — ma il ruolo `ile` è superutente (`rolsuper = t`) e li può prendere: il muro è a 300, ed è quello il messaggio «sorry, too many clients already» |
| `reserved_connections` | 0 |
| limiti per ruolo e per database | nessuno (`rolconnlimit = -1`, `datconnlimit = -1` ovunque) |
| `idle_session_timeout`, `idle_in_transaction_session_timeout`, `tcp_keepalives_idle` | 0, 0, 0: una connessione ferma non scade mai |

L'indirizzo che PostgreSQL vede è sempre `172.20.0.1` (il gateway di Docker), con una porta che non è quella del client Windows: la corrispondenza fra connessioni e processi è fatta dal lato Windows, contando per processo i socket verso `127.0.0.1:5439`, e torna con i totali per database.

### 2.2 Chi tiene che cosa

Alle 20:33:41 del 2 ottobre, con il server ufficiale ancora sul codice vecchio:

| Server | PID (interprete) | Avviato | Thread | Socket HTTP aperti | Connessioni a PostgreSQL | Database | La più vecchia |
|---|---|---|---|---|---|---|---|
| 8770 | 26400 | 28/09 06:48:52 | **1** | 0 | **8** | `ile` | 3 giorni 22 h |
| 8771 | 18100 | 28/09 06:48:52 | **1** | 0 | **7** | `ile_qa` | 4 giorni 13 h |
| 8772 | 28612 | 28/09 06:49:00 | **1** | 0 | **16** | `ile` | 3 giorni 22 h |
| **8780** | 37080 | 02/10 14:47:10 | **1** | 0 | **48** | `ile_v5` | 3 h 05 min |
| pytest, corsia 4 (il mio) | — | — | — | — | 1 | `test_ile_lane4` | 23 s |

**Quattro processi con un solo thread — quello principale — e nessun socket HTTP aperto tengono 79 connessioni.** Non c'è un thread che le possa usare o chiudere: sono tutte orfane. Quella di 8771 è stata aperta dieci secondi dopo l'avvio del server, quattro giorni e mezzo fa, e da allora è ferma.

L'andamento di `ile_v5` nel pomeriggio: 17 connessioni alle 18:30 (censimento dell'orchestratore), 31 alle 19:04, 37 alle 19:05 — in quel momento 12 thread e 10 socket keep-alive del Chrome del proprietario —, 48 alle 20:23 e alle 20:33, 55 alle 21:12. Cresce a ogni visita e non scende da sé.

Nessun'altra connessione: nessun server temporaneo di agenti, nessuna corsia di test oltre la mia, al momento dei tre censimenti. Esistono 119 database `test_ile_*` lasciati dalle corsie: non tengono connessioni.

### 2.3 Il registro del server

`C:/tmp/ile_v5_council/.work/servers/srv8780.log` comincia alle 14:47:13 (l'avvio del processo ancora in esecuzione); al momento della lettura: 25 294 richieste, 1 236 documenti HTML.

* **106 risposte 500**, tutte lo stesso errore: 84 fra le 15:36:20 e le 15:53, 22 fra le 17:20 e le 17:27:39. 100 su file di prova, 6 su `/fr/`.
* **Tutte e 106 nello stesso punto**: `_get_response` (`handlers/base.py:197`) → `contextlib.inner` → `transaction.Atomic.__enter__` (`transaction.py:198`) → `ensure_connection` → `psycopg.connect` → `FATAL: sorry, too many clients already`. È la transazione di `ATOMIC_REQUESTS` che tenta di aprire la connessione, **prima** della vista; nessun errore viene da un middleware o da una query.
* Durante l'interruzione molte richieste continuavano a ricevere 200 (alle 15:36, 581 su 590): i thread che avevano già una connessione sul loro socket keep-alive lavoravano; falliva ogni socket nuovo.

Carico per minuto (documenti HTML / richieste):

| Finestra | Documenti | Richieste | Punte |
|---|---|---|---|
| 14:50–15:19 | 268 | 6 232 | 15:03 → 29 / 671 |
| 15:20–15:36 | 164 | 4 977 | 15:26 → 43 / 998 · 15:35 → 42 / 936 · 15:36 → 25 / 590 |
| 15:37–15:55 | 66 | 566 | 15:39 → 18 / 115, di cui 44 errori |
| 17:00–17:28 | 191 | 4 644 | 17:11 → 19 / 571 · 17:20 → 22 / 514 |

Il secondo più carico: 72 richieste (15:02:55); 69 alle 15:36:00.

*(4 ottobre, revisione W2-4.)* Il registro è ripartito da zero con il riavvio del 2 ottobre alle 21:52 e di nuovo con quello del 4 ottobre alle 08:12: i conteggi di questa sezione non sono più ricontrollabili da nessuno. Ciò che la revisione W2 aveva già riletto prima del riavvio — le 106 risposte 500, la loro distribuzione, le rotte, il punto della traccia — sta nel suo §2.1; il carico per minuto e i «60 caricamenti, 1 353 richieste» del §2.4 restano sulla parola di questa nota. Per i prossimi avvii: un registro con il nome dell'avvio, o aperto in aggiunta (fuori dalla proprietà dell'anteprima).

### 2.4 Che cosa è successo

Gli script del consiglio sull'hero (`C:/tmp/ile_v5_council/.work/hero-council/*/common.py`, `design/capture.py`) puntano tutti a 8780 e aprono **un contesto persistente di Chromium per ogni configurazione o per ogni caricamento** («One fresh profile per page load, removed afterwards»). Secondo l'orchestratore, in quei minuti cinque agenti di revisione catturavano pagine da 8780 e altri eseguivano suite di test.

Misurato su un server identico (§3.4): **ogni browser che carica una maquette costa 6 thread e 6,4 connessioni**, che restano finché il browser è aperto e *dopo* che è stato chiuso.

Fra le 15:35:00 e le 15:36:20, dopo quaranta secondi di silenzio, sono arrivati 60 caricamenti di pagina (1 353 richieste). A 6,4 connessioni l'uno sono 384 richieste di connessione in 80 secondi, a un server PostgreSQL che ne aveva al più 271 libere: le 29 di 8770, 8771 e 8772 erano già lì da ore o da giorni, e 8780 aveva dietro di sé 407 caricamenti e 9 725 richieste dalle 14:47. Il collettore ne ha liberate una parte lungo la strada — a raffica, non a comando — e alle 15:36:20 non è bastato. Alle 15:39 gli errori erano 44 su 115 richieste. Il carico è poi caduto (15 richieste fra le 15:40 e le 15:49), i browser si sono chiusi, una raccolta ha liberato gli orfani; alle 15:54 il servizio era tornato. Alle 17:20 la stessa sequenza, più breve: 55 caricamenti e 1 234 richieste fra le 17:18 e le 17:21.

Dopo l'interruzione gli script hanno imparato a ritentare — fino a cinque volte, con 8–10 s d'attesa e un browser nuovo a ogni tentativo — quando una risposta è ≥ 400 (lo dicono i loro commenti). Sul codice di prima ogni tentativo era un caricamento in più sullo stesso muro.

**Ciò che non si può più sapere**: il numero esatto di connessioni per processo alle 15:36 — `pg_stat_activity` non ha memoria — e se in quel momento giravano server temporanei o corsie di test di altri agenti. Non cambia la diagnosi: il meccanismo, da solo, supera i 300 con il carico che il registro documenta, e l'ho fermato a mano due volte mentre lo riproducevo (§3.3).

---

## 3. Riproduzione controllata

### 3.1 Metodo

`harness.py` avvia un server proprio dalla worktree (porta 8784, ambiente del server ufficiale) e gli dà un `application_name` unico (`PGAPPNAME`): le sue connessioni si contano in `pg_stat_activity` senza confonderle con quelle altrui. Una raffica è `n` GET con `c` thread e `urllib` — un socket per richiesta, come `curl` e come un browser appena lanciato — sui venti file che un caricamento di H-B chiede davvero (dal registro delle 15:36:20). Il censimento è letto ogni 40 ms durante la raffica, poi a +1, +10, +30, +65 e +75 s; il server è spento alla fine di ogni cella, il che libera tutto ciò che teneva.

**Sicurezza**: il PostgreSQL è condiviso. Una raffica smette di inviare quando il server in prova tiene 110 connessioni o il server PostgreSQL 215 in tutto. È scattata due volte, sul codice com'era.

### 3.2 Il meccanismo, visto da dentro

`probe_server.py` è lo stesso `runserver` con un osservatore accanto: un riferimento debole a ogni wrapper creato, e a richiesta una lettura prima e dopo `gc.collect()`.

| Momento | PostgreSQL: connessioni del server | Nel processo: thread | wrapper in memoria | con connessione aperta | Raccolte gen0 / gen1 / gen2 |
|---|---|---|---|---|---|
| avvio | 0 | 2 (principale e osservatore) | 1 | 0 | 115 / 10 / 0 |
| 200 richieste a 32 | picco 89 | — | — | — | — |
| +2 s | **87** | **2** | 88 | **87** | 126 / 11 / 1 |
| +72 s (oltre `CONN_MAX_AGE`) | **87** | 2 | 88 | 87 | 126 / 11 / 1 — nessuna raccolta in 70 s |
| dopo `gc.collect()` | **0** | 2 | 1 | 0 | 8 421 oggetti irraggiungibili liberati |

200 richieste hanno aperto 200 connessioni: una per richiesta. 113 le ha liberate il collettore durante la raffica, 87 sono rimaste, di nessuno — i thread che le avevano aperte non esistono più — e sono sparite nell'istante in cui il collettore è stato chiamato a mano.

### 3.3 Raffiche di file di prova: com'era, e con ciascun candidato

Connessioni del server in prova. «Picco» è il massimo letto durante la raffica, «dopo» è a +1 s e non cambia fino a +75 s (com'era) o a +10 s (candidati).

| n × c | Com'era: picco | Com'era: dopo (+1 s … +75 s) | Candidato 1 — `DB_CONN_MAX_AGE=0`: picco / dopo | Candidato 2 — vista senza transazione: picco / dopo | Definitivo (1 + 2 + tetto): picco / dopo |
|---|---|---|---|---|---|
| 50 × 8 | 30 | **33** | 5 / 0 | 0 / 0 | **0 / 0** |
| 50 × 32 | 38 | **39** | 11 / 0 | 0 / 0 | **0 / 0** |
| 50 × 64 | 39 | **42** | 12 / 0 | 0 / 0 | **0 / 0** |
| 200 × 8 | 44 | **46** | 8 / 0 | 0 / 0 | **0 / 0** |
| 200 × 32 | 91 | **85** | 14 / 0 | 0 / 0 | **0 / 0** |
| 200 × 64 | 84 | **84** | 13 / 0 | 0 / 0 | **0 / 0** |
| 600 × 8 | 94 | **49** | 5 / 0 | 0 / 0 | **0 / 0** |
| 600 × 32 | **142, fermata a 254 richieste** (PostgreSQL a 221) | **143** | 13 / 0 | 0 / 0 | **0 / 0** |
| 600 × 64 | **155, fermata a 271 richieste** (PostgreSQL a 234) | **160** | 13 / 0 | 0 / 0 | **0 / 0** |

* **Connessioni per richiesta in volo, com'era**: non c'è un rapporto. Con 8 richieste in volo il server ne teneva fino a 94: il numero segue i socket aperti *finora*, non la concorrenza. A 32 e a 64 in volo crescevano di circa 0,56 per richiesta, senza un tetto: da sola, la raffica da 600 avrebbe preso i 300 posti in tre secondi.
* **Quanto sopravvivono le ferme**: in tutte e nove le celle il numero a +75 s è quello a +1 s. Fuori dalla prova: tre giorni e ventidue ore su 8770 e 8772, quattro giorni e tredici ore su 8771 (§2.2).
* **Candidato 1** toglie gli orfani: ogni richiesta apre e chiude la sua connessione, una per richiesta in volo dentro la vista (5–14 lette, al più `c` in teoria). Non richiede codice: la variabile esiste già.
* **Candidato 2** toglie la connessione: un file di prova non ne apre.
* Le 600 richieste passano in 1,0–1,6 s; erano 2,5 s com'era (600 × 8, la sola cella arrivata in fondo) e 2,7–3,1 s con il candidato 1: una connessione in meno da aprire a ogni file.

### 3.4 Browser headless

`browser_probe.py`: cinque Chromium headless, un profilo ciascuno, ognuno carica il selettore che incornicia H-B (il documento, la maquette nell'iframe, ciò che la maquette chiede: 35 richieste su 6 socket).

| | Com'era: connessioni | thread del server | Definitivo: connessioni | thread |
|---|---|---|---|---|
| prima | 0 | 5 | 0 | 5 |
| 1 browser | 3 | 11 | 0 | 11 |
| 2 | 13 | 17 | 0 | 17 |
| 3 | 19 | 23 | 0 | 23 |
| 4 | 25 | 29 | 0 | 29 |
| 5 | **32** | 35 | **0** | 35 |
| pagine aperte, ferme (70 s / 20 s) | **32** — la più vecchia 77 s: oltre `CONN_MAX_AGE` | 34 | 0 | 35 |
| browser chiusi, +3 s | **32** | 4 | 0 | 7 |
| browser chiusi, +33 s | **32** | 4 | 0 | 4 |

Sei thread per browser, in entrambi i casi: è il pool di socket di Chromium, e un thread fermo non costa nulla. La differenza è che ora un thread non tiene una connessione.

### 3.5 Le pagine che leggono il database, e il tetto

Raffiche sull'hub (tre `SELECT` a richiesta), connessioni del server in prova:

| Configurazione | n × c | Picco | Dopo | Risposte |
|---|---|---|---|---|
| quella del 2 ottobre (`CONN_MAX_AGE = 60`, nessun tetto) | 200 × 32 | **109** | **61** (invariate a +75 s) | 200 × 200, in 30,3 s |
| durata zero, senza tetto | 200 × 32 | 12 | 0 | 200 × 200, in 10,2 s |
| durata zero, senza tetto | 600 × 64 | 12 | 0 | 600 × 200, in 31,2 s |
| **definitiva** (durata zero, tetto 8) | 50, 200, 600 × 8, 32, 64 — nove celle | **8** in otto celle, 7 in una | **0** in tutte | tutte 200; 600 × 64 in 34,5 s |
| **definitiva**, carico misto (hub, i due selettori, un file di prova mancante, `/fr/`, un CSS) | 600 × 64 | **8** | **0** | 500 × 200 e 100 × 404 (il file mancante), in 14,2 s |

Senza tetto il picco letto è 12 e potrebbe arrivare a `c`; con il tetto è 8, a 8, a 32 e a 64 richieste in volo. Nessuna richiesta ha aspettato abbastanza da ricevere un 503. Rimisurato dopo l'ultima modifica al codice (`final2.txt`): file di prova 600 × 64 → 0 / 0; hub 600 × 64 → picco 7, 0 dopo; carico misto 600 × 64 → picco 8, 0 dopo; cinque browser → 0.

`abort_probe.py`: 180 richieste il cui client riattacca subito, metà con RST — hub, pagina dal vivo, file mancante. Picco 4 connessioni; poi l'hub risponde 200 in 0,1 s e il server è a 0. Una GET interrotta non perde il suo posto.

**Correzione del 4 ottobre (revisione W2, rilievo W2-1).** La frase che stava qui — «una richiesta interrotta non perde il suo posto» — valeva per le GET soltanto. A `da75812` il posto tornava a `request_finished`, e sotto `runserver` quel segnale parte da `ServerHandler.close()` (`django/core/servers/basehttp.py`), che **prima** legge il corpo della richiesta non ancora letto e **poi** chiude la risposta. Un client che annuncia un corpo e non lo manda tiene la lettura, il thread e il posto finché tiene il socket; uno che azzera la connessione (RST) dopo la risposta fa fallire quella lettura, `wsgiref` inghiotte l'errore, il segnale non parte, il thread finisce e il posto è perso per la vita del processo — con zero connessioni aperte, nulla nel registro nel momento in cui succede, e la riga di SQL del §5 che dice 0. La revisione lo ha misurato (`PREVIEW_REVIEW_W2.md` §2.3): otto POST con `Content-Length: 100000` e dieci byte, risposte `403` dal CSRF prima della lettura del corpo, poi azzerate → hub, selettori e file di prova 503 fino al riavvio. Le rotte dell'anteprima (GET e HEAD) non lo provocano, ma il tetto sta davanti a ogni rotta del sito. Dal commit di oggi il posto torna **quando la risposta esce dal middleware** — la pagina è completa, la connessione del thread viene chiusa prima — per ogni risposta che non sia uno stream diverso da un file; il segnale, quando arriva, non trova nulla da rendere. Il test che fissava il contrario è invertito, due test nuovi tengono il caso (§7), e il 503 dice «posti», non «connessioni in uso».

Rimisurato il 4 ottobre su un server mio (`127.0.0.1:8784`, stesso ambiente dell'ufficiale più `PGAPPNAME=ile-design-preview-sb` per contare le sue connessioni soltanto; `C:/tmp/ile_v5_council/.work/stream-b/w2-fix/measure.py`, risultati in `measure.json`, registro del server in `srv8784.err.log`; censimento con `docker exec … psql` in sola lettura; `old_ceiling.py` è il plugin pytest che rimette il comportamento di `da75812` da fuori, con cui i tre test del §7 cadono), lucchetto assente a ogni attesa:

| Prova | Esito |
|---|---|
| 8 GET dell'hub con `Content-Length: 100000` e dieci byte, socket tenuti aperti | tutte 200; mentre i corpi sono attesi: hub 200 in 0,08 s, file di prova 200 (posti liberi); 0 connessioni |
| … le otto chiuse con RST | hub, selettore, file di prova 200 subito e 25 s dopo; 0 connessioni |
| 8 POST uguali (403 dal CSRF), chiuse con RST | la prova della revisione: hub 200 in 0,09 s, selettore e file di prova 200, 0 connessioni, hub 200 25 s dopo |
| 16 POST di seguito, ciascuna azzerata dopo il 403 (il doppio del tetto) | hub 200, 0 connessioni |
| hub 600 × 64 | 600 × 200 in 35,9 s; **picco 5**, 0 dopo 1 s e dopo 10 s; mediana 3,8 s, massimo 10,4 s; nessun 503 |
| misto 600 × 64 (hub, selettore, file mancante, `/fr/`, file di prova) | 480 × 200 e 120 × 404 in 14,1 s; **picco 3**, 0 dopo |
| file di prova 600 × 64 | 600 × 200 in 2,1 s; **picco 0**, 0 dopo |
| a riposo, prima e dopo; dopo l'arresto del server | 0; 0; 0 (porta chiusa) |

Il picco è più basso del 2 ottobre (8) perché la connessione di una pagina viene chiusa prima che la pagina sia spedita, non a `request_finished`: lo stesso tetto, meno tempo per connessione. Resta scoperto, e scritto nella docstring del middleware e nel test, lo stream che non è un file: tiene il posto finché il suo thread lo chiude, e un client che azzera dopo averlo ricevuto glielo farebbe perdere; oggi nel sito non ce n'è nessuno.

---

## 4. Le domande del proprietario

| Domanda | Risposta |
|---|---|
| **Perché l'anteprima ha esaurito le connessioni** | Perché ogni richiesta — anche di un file statico di prova — apriva una connessione (`ATOMIC_REQUESTS`), su un thread per socket (`runserver`), e la connessione non veniva mai chiusa: né alla fine della richiesta (`CONN_MAX_AGE = 60`), né alla fine del thread (nessuno chiude la connessione di un thread finito). Il numero di connessioni seguiva il numero di socket aperti da quando il server era partito, non il lavoro in corso |
| **Quanti server e processi erano attivi** | Quattro server di sviluppo, quattro interpreti Python (otto processi nell'elenco: ogni `python.exe` del venv lancia il suo interprete): 8770, 8771 e 8772 dal 28 settembre, 8780 dalle 14:47. Tenevano già 29 connessioni orfane prima dell'interruzione. Tutte e 106 le risposte 500 registrate sono di 8780; che cosa girasse d'altro alle 15:36 non è più ricostruibile (§2.4) |
| **Durata di una connessione** | Di fatto illimitata. `CONN_MAX_AGE = 60` vale soltanto se lo stesso thread riceve un'altra richiesta dopo 60 s. Un thread fermo sul suo socket la tiene finché il browser tiene il socket (misurato: 77 s e oltre); un thread finito la lascia aperta finché il collettore non la trova (misurato: invariata a +75 s; sui server ufficiali, quattro giorni e mezzo) |
| **Numero di worker** | Un processo; **un thread per socket, senza limite**; coda d'ascolto di 10. Nessun pool di connessioni: una connessione per thread che tocca il database |
| **Concorrenza di test e browser** | Cinque agenti, un Chromium nuovo per cattura, sei socket a browser: fino a 43 caricamenti di pagina e 998 richieste al minuto, 72 richieste nel secondo più carico; 60 caricamenti negli 80 s prima del primo errore. Le corsie di test pesano poco: un processo pytest tiene una connessione (misurato sulla corsia 4), e il server dei test chiude le sue a ogni richiesta |
| **Connessioni non chiuse** | Sì, ed è il difetto. Alle 20:33 quattro processi senza un thread di richiesta vivo ne tenevano 79. Dopo una raffica di 200 richieste, 87 wrapper con connessione aperta in un processo con due thread; `gc.collect()` le porta a zero |

---

## 5. La correzione

Tutta dentro la riga di proprietà dell'ingegnere dell'anteprima; il limite del server PostgreSQL resta 300.

| # | Che cosa | Dove | Effetto misurato |
|---|---|---|---|
| 1 | **Nessuna vista dell'anteprima chiede una transazione**: `transaction.non_atomic_requests` applicato da `_preview_only`, sul callable che l'URLconf tiene | `apps/designpreview/views.py` | un file di prova non apre una connessione: 0 / 0 / 0 in tutte e nove le celle, anche con `CONN_MAX_AGE = 60` |
| 2 | **I due selettori non leggono più nulla**: `frame.html` è reso senza i context processor della richiesta, che leggevano `SiteSettings` per valori che il template non stampa | `apps/designpreview/views.py` (`_render_frame`) | selettore: 0 istruzioni, 0 connessioni; cinque browser: 0 connessioni |
| 3 | **Una connessione vive quanto la sua richiesta** sul server dell'anteprima: `CONN_MAX_AGE = 0`, `CONN_HEALTH_CHECKS = True` | blocco dell'anteprima in `config/settings/dev.py` | hub: 0 connessioni dopo ogni raffica |
| 4 | **Un tetto**: `ConnectionCeilingMiddleware`, primo della catena, soltanto con il flag | `apps/designpreview/middleware.py`, installato dallo stesso blocco | mai più di 8, a 8, 32 e 64 richieste in volo |
| 5 | **Un nome**: `application_name = ile-design-preview` (`PGAPPNAME` lo sostituisce) | stesso blocco | il conteggio è una riga di SQL |

**Come è fatto il tetto.** Una richiesta prende uno di `ILE_DESIGN_PREVIEW_DB_CEILING` posti (8; la variabile d'ambiente omonima lo cambia) prima che qualunque cosa possa leggere il database, e lo rende **quando la risposta esce dal middleware** — il primo della catena, quindi l'ultimo a vedere la risposta: la pagina è completa, nulla di ciò che segue legge il database — **dopo** aver chiuso la connessione del suo thread (Django la chiuderebbe comunque a `request_finished`, per la durata zero; il middleware non aspetta quel segnale, che sotto `runserver` può non arrivare: §3.5, correzione del 4 ottobre). Un thread apre una connessione soltanto mentre tiene un posto, quindi connessioni aperte ≤ posti presi ≤ 8; il thread principale non ne tiene. Una risposta che è un file rende il posto allo stesso modo, prima di essere spedita: un file non chiede nulla al database mentre viaggia, e un lettore lento di un video non deve far aspettare gli altri. Uno stream che non è un file — l'anteprima non ne ha, `apps/` nessuno — è la sola risposta che tiene il posto mentre viene spedita e lo rende a `request_finished`. Chi trova tutti i posti presi aspetta fino a 20 s, poi riceve un 503 in chiaro («Anteprima occupata: questo server ha 8 posti per le richieste che usano il database, e sono tutti presi da più di 20 secondi…», `Retry-After: 2`): con richieste che durano da pochi millisecondi (un file) a una sessantina (l'hub) l'attesa non si vede, e nelle misure non è mai scattato.

**Come si misura.** In ogni momento:

```sql
select count(*) from pg_stat_activity where application_name = 'ile-design-preview';
```

0 a riposo, al più 8 sotto qualunque raffica. Verificato su un server avviato esattamente come quello ufficiale, senza `PGAPPNAME` (`named_census.py`): 0 a riposo; 600 file di prova a 64 → picco 0; 300 pagine dell'hub a 64 → picco 8, poi 0; 300 pagine dei selettori a 64 → picco 0. (Finché il server ufficiale non viene riavviato sul codice nuovo le sue connessioni non portano il nome: si contano per database, `datname = 'ile_v5'`.) La riga conta **connessioni, non posti**: un posto tenuto senza connessione (uno stream in spedizione) non lo vede, ed è per questo che il 503 e la sua riga di registro parlano di posti. Un 503 con la riga a 0 significa posti tenuti senza connessione; dal commit del 4 ottobre una pagina non può più tenerne uno dopo essere uscita dal middleware.

**Perché non il resto.** Un pool di psycopg limiterebbe anch'esso, ma `psycopg_pool` non è installato e non si installa nulla. Un motore di database proprio dell'anteprima sarebbe stato più invasivo di un middleware e non verificabile nei test. Alzare `max_connections` sposta il muro: 79 connessioni sono già ferme per sempre, e crescono a ogni visita.

**Che cosa non fa.** L'hub legge ancora il database (estende `base.html`: tre `SELECT`), quindi con PostgreSQL saturo *da altri* l'hub risponderebbe 500; i selettori e le maquette no — non lo toccano più. Un file di prova che manca costa ancora una lettura di `cms_redirect` (il middleware è di un'altra proprietà): chiusa a fine richiesta, sotto il tetto.

---

## 6. Ciò che resta fuori dalla mia proprietà

Raccomandazioni per l'orchestratore, con la prova accanto.

| # | Che cosa | Prova | Proposta |
|---|---|---|---|
| R1 | **Riavviare 8780** sul commit di oggi | 48 connessioni orfane alle 20:33 con 1 thread e 0 socket, 55 alle 21:12; il processo ha in memoria il codice vecchio | dopo il riavvio: 0 a riposo, e la riga di SQL del §5 lo dimostra |
| R2 | **8770, 8771, 8772 perdono allo stesso modo** e non sono dell'anteprima | 8 + 7 + 16 = 31 connessioni, 1 thread ciascuno, le più vecchie di 4 giorni e 13 ore; liberarle richiede il riavvio del processo (non ho terminato sessioni altrui) | riavviarli con `DB_CONN_MAX_AGE=0` nell'ambiente: la variabile esiste già (`base.py:155`), non serve codice. Misurato sul codice di prima: 0 orfani in tutte e nove le celle (candidato 1) |
| R3 | **I server temporanei degli agenti** | stesso codice, stessa perdita | stessa variabile nel comando d'avvio; chi avvia con `ILE_DESIGN_PREVIEW=1` ha già durata zero e tetto |
| R4 | **Per sempre, in sviluppo**: `CONN_MAX_AGE = 0` in `config/settings/dev.py`, fuori dal blocco dell'anteprima | connessioni persistenti hanno senso sotto gunicorn, dove i thread durano; sotto `runserver` i thread durano quanto un socket | una riga, del coordinatore delle integrazioni |
| R5 | **Seconda linea, sul server PostgreSQL di sviluppo**: `idle_session_timeout` di qualche minuto | `idle_session_timeout = 0`: un orfano non scade mai, di chiunque sia — anche di un pytest sopravvissuto al suo terminale | è un'impostazione del server: decisione dell'orchestratore. Non è «alzare il limite». Chi tiene connessioni a lungo deve allora avere `CONN_HEALTH_CHECKS = True` |
| R6 | **Le corsie di test** | 1 connessione per processo pytest; nessun residuo ai tre censimenti; 119 database `test_ile_*` senza connessioni | nulla da correggere; i processi pytest rimasti dopo un arresto si cercano come dice la nota di progetto sulle corsie |
| R7 | **Gli script di cattura** aprono un browser nuovo per ogni caricamento e, da oggi, ritentano fino a cinque volte su una risposta ≥ 400 | 6 thread e 6,4 connessioni per browser, sul codice di prima (§3.4) | con la correzione un browser non costa connessioni: nulla da cambiare negli script |

*(4 ottobre, revisione W2-3.)* Il limite del server PostgreSQL era già stato alzato una volta per lo stesso sintomo, da 100 a 300 (`docker-compose.yml`, righe 4–8, `06f9986`, 21 settembre), con il commento «which looks like a code failure and is a capacity one»: le misure di questa nota dicono il contrario — era un difetto del codice, e il limite non c'entrava. Il commento va corretto da chi possiede il file; R2–R4 restano la via (R4, `CONN_MAX_AGE = 0` in `config/settings/dev.py` fuori dal blocco dell'anteprima, è preferibile alla riga nei `.env`, perché un `.env` invecchia: il §1.1 lo mostra).

---

## 7. I test

`tests/frontend/test_design_preview.py`, 132 test (erano 120; 130 al 2 ottobre, due aggiunti il 4 ottobre per il rilievo W2-1), corsia `ile_lane4`.

| Test | Che cosa tiene |
|---|---|
| `test_a_burst_of_proof_requests_opens_no_connection_and_leaves_none_behind` | **la regressione**: 120 richieste, 8 alla volta, un socket ciascuna, alla classe di server che `runserver` costruisce (non `live_server`, che chiude le connessioni da sé e avrebbe nascosto il difetto) e con la durata che ha ogni server di sviluppo (60 s; sotto i test sarebbe 0): nessuna connessione creata nel processo, e PostgreSQL conta gli stessi backend prima, durante e dopo |
| `test_no_preview_view_asks_for_a_transaction` | le quattro viste sono marcate dove Django guarda; le pagine del sito tengono la loro transazione |
| `test_a_picker_and_a_proof_file_read_nothing` | 0 istruzioni per selettori (200 e 400) e file di prova |
| `test_a_burst_on_pages_that_read_the_database_stays_under_the_ceiling` | hub, pagina del sito e file mancante attraverso il middleware, tetto 2, con `CONN_MAX_AGE = 60`: mai più di 2 backend, 0 alla fine |
| `test_no_more_connections_than_the_ceiling_whatever_arrives` | 24 thread contro un tetto di 3, senza caso: PostgreSQL ne conta 3 in più, ogni volta |
| `test_the_ceiling_makes_a_request_wait_and_then_says_so_in_plain_words` | attesa, 503 in chiaro, intestazioni, posto reso |
| `test_a_file_response_gives_its_slot_back_before_it_is_sent` | un file non letto non tiene il posto; dal 4 ottobre nemmeno una pagina mai chiusa (al 2 ottobre l'asserzione diceva il contrario: era il difetto W2-1, fissato come voluto) |
| `test_a_slot_is_not_lost_when_request_finished_never_comes` (4 ottobre) | tetto 1: una pagina servita su un thread che finisce senza `close()` lascia il posto libero; il segnale che arriva tardi non rende nulla due volte (semaforo limitato); una vista che solleva lascia il posto libero; uno stream non-file tiene il posto finché il suo thread lo chiude |
| `test_a_client_that_resets_after_its_page_costs_the_server_no_slot` (4 ottobre) | attraverso il server di `runserver`, tetto 1: tre GET dell'hub con `Content-Length: 100000` e dieci byte, risposte 200, thread fermi sulla lettura del corpo; nel frattempo altre richieste servite subito; dopo tre RST hub, selettore e file di prova 200, nessuna connessione lasciata |
| `test_the_ceiling_is_installed_by_the_preview_block_alone`, `test_dev_settings_read_the_flag_from_the_environment` | il blocco di `dev.py`: durata zero, tetto, nome — su oggetti propri, senza toccare `base` |

**I denti, verificati.** Con la vista dei file di prova di nuovo in transazione il primo test fallisce su ciascuna delle sue due metà, provate una alla volta: «96 connections were opened by 96 request threads», e «a burst of proof requests left PostgreSQL backends behind» (20 backend ancora sul database, 0 dopo `gc.collect()`). Con un middleware che rende il posto senza chiudere, il test del tetto conta 4, 7, 10, 13, 16, 19… backend invece di 4 ogni volta (i tre della raffica e quello del test).

**Due difetti trovati scrivendoli, entrambi nei test.** Dentro una transazione PostgreSQL risponde a `pg_stat_activity` dall'istantanea presa alla prima domanda: la prima stesura contava «prima, durante e dopo» tre volte la stessa fotografia, e sarebbe passata anche sul codice vecchio; ora ogni conteggio scarta l'istantanea (`pg_stat_clear_snapshot()`). E sotto le impostazioni di test la durata di una connessione è zero: senza darle i 60 s dei server di sviluppo, «nessuna lasciata» sarebbe stato vero di qualunque codice.

---

## 8. Lo stesso commit, il catalogo

Fuori dall'argomento di questa nota, ma nello stesso commit e sotto gli stessi test: l'hub ha tre gruppi di più all'inizio e alla fine — «H-E — nuova direzione» (la pagina finale, i tre concetti, il campione CTA-A / CTA-B), «Consiglio sull'hero» (l'esito in una frase, attribuito al consiglio; il verbale e le due tavole come percorsi scritti, non serviti e non copiati), e tre gruppi per i prototipi della seconda ondata — e il selettore del primo schermo ha quattro scelte in più: H-E (tasto `e`) e i concetti E1, E2, E3, senza tasto perché in quella barra il `3` è la fase.

* **Ciò che non è ancora su disco dice «manca» e diventa un link da solo**: ogni link è risolto a ogni richiesta. Visto dal vivo durante questo lavoro: alle 20:00 esisteva soltanto il concetto 3, alle 20:40 i tre concetti erano link senza che il server fosse stato toccato. La pagina finale di H-E e il campione CTA mancano ancora.
* **La barra del selettore del primo schermo è cambiata sotto 48 rem**, ed è una conseguenza, non una scelta di design: nove scelte non stanno accanto alla lingua a nessuna larghezza di telefono (servono 287 px; accanto al marchio, alla lingua e ad «Apri» ce ne sono 210 a 360, 240 a 390, 280 a 430). Ora hanno una riga loro: tre righe, 121 px, a 360, 390 e 430 px, in ogni stato — come il selettore tipografico (105 px) — dove prima erano due (85 px). Da 48 rem la barra perde i nomi dei gruppi sotto 105 rem (prima sotto 86): 77 px a 1440, 1366 e 1280, come prima; a 1024 le larghezze vanno su una seconda riga, 117 px (erano 77), come già accadeva al selettore tipografico. Misurato in Chromium headless, nessun traboccamento, bersagli di 27 × 32 px o più.
* Le note di H-C e H-D non dicono più «revisione indipendente in attesa»: il consiglio le ha esaminate. Il resto della pagina non classifica un primo schermo rispetto a un altro; l'ordine della maggioranza è scritto una volta, nel gruppo del consiglio, come suo.

---

## 9. Limiti di questa diagnosi

* La ricostruzione delle 15:36 poggia sul registro di 8780, sugli script degli agenti e sul meccanismo riprodotto; non su un censimento di quel minuto, che non esiste.
* Le misure sono su questa macchina, con il PostgreSQL condiviso in uso da altri: i tempi delle raffiche sono indicativi, i conteggi di connessioni no.
* Il tetto vale per il processo che ha il flag dell'anteprima. Gli altri server di sviluppo restano come erano finché non vengono riavviati (R2).
* Non ho verificato il comportamento sotto gunicorn: la produzione non usa `runserver`, e lì i thread durano. È materia del Blueprint, non di questa nota.
