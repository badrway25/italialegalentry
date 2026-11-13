# Revisione indipendente della correzione dell'interruzione e del catalogo H-E — commit `da75812`

| | |
|---|---|
| **Oggetto** | `design-v5: preview — connection outage diagnosed and fixed; H-E, concepts, CTA, council and wave-2 prototypes catalogued` — commit `da75812` su `design-v5` (genitore `aa2eab4`), 9 file, +1 720 −108; e la nota `docs/design-v5/QA/PREVIEW_OUTAGE_2026-10-02.md` |
| **Ruolo** | Revisore indipendente dello stream B/D (non ha costruito nulla dell'anteprima né della correzione) |
| **Data** | 2 ottobre 2026, 21:22–22:50 (ora locale) |
| **Verdetto** | **PASS_WITH_FIXES** — **la causa è provata, non affermata**, e la correzione tiene ciò che dichiara: mai più di 8 connessioni, zero a riposo, nessun limite alzato, solo sviluppo. Nessun rilievo bloccante; **due maggiori** (W2-1: il tetto perde un posto per sempre quando `request_finished` non arriva — otto volte e l'anteprima risponde 503 fino al riavvio; W2-2: l'hub stampa una classifica dei cinque primi schermi), tre minori, otto osservazioni |
| **Strumenti** | server propri su `127.0.0.1:8786` e `8787` (stesso ambiente del server ufficiale: `DATABASE_URL=…/ile_v5`, `ILE_DESIGN_PREVIEW=1`, `runserver --noreload`), avviati e spenti a ogni misura, ciascuno con un `application_name` proprio; il commit precedente da una worktree temporanea `C:/tmp/ile_wt/_review_prefix` (`git worktree add --detach … aa2eab4`, rimossa alla fine); `pg_stat_activity`, `pg_settings`, `pg_roles` in sola lettura attraverso `docker exec italylegalentry-db-1 psql`, una sessione interrogata ogni 50 ms durante le raffiche; Playwright 1.63.0 headless (Chromium), profili propri sotto `C:/tmp/ile_v5_council/.profiles/stream-b/review-w2` (rimossi alla fine); corsia `ile_lane5`; confronto con `main` su `127.0.0.1:8770` e con l'albero di `main` in sola lettura |
| **Lucchetto** | `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` atteso in ciclo (30 s, fino a 25 min) prima di ogni server, raffica, browser ed esecuzione di test: 40 attese, tutte di 0 s. Tre mancanze mie, lanciate senza l'attesa: una riesecuzione di otto test (13 s) alle 22:09 e due `pytest --collect-only` (nessun test eseguito, 6 s) alle 22:20 |
| **Prove** | fuori dal repository, `C:/tmp/ile_v5_council/.work/stream-b-review-w2/`: `rw2.py` (server, raffiche, censimento), `gate.py`, `s1_pre.py`, `s2_probe.py` + `probe_server.py`, `s3_post.py`, `s4_live.py`, `s5_catalogue.py`, `s6_ceiling.py`, `s7_leak.py` + `fixed_server.py`, `settings_probe.py`, `inproc_page.py`, `rw2_mutate.py`; risultati in `results.jsonl`, `run.log`, `s4_live.json`, `s5_catalogue.json`, `s6_*.json`, `s7_*.json`, `settings_probe.json`, `probe-pre.jsonl`, `lane5-preview.log`, `bodies/`, `shots/`, `server-*.log` |

Il server ufficiale su 8780 non è stato fermato né riavviato da me (lo ha riavviato l'orchestratore alle 21:52:32, insieme a 8770, 8771 e 8772, durante questa revisione); il Chrome del proprietario (9223) e quello di QA (9222) non sono stati toccati; nessuna sessione PostgreSQL altrui terminata, nessuna impostazione del server cambiata; la cartella vera delle prove è stata soltanto letta. Niente di ciò che segue è una decisione di design.

---

## 0. In breve

| | Commit precedente `aa2eab4` (misurato da me) | Commit `da75812` (misurato da me) |
|---|---|---|
| 200 file di prova, 32 alla volta | 0 → picco **92** → **84** lasciate, uguali a +1, +10, +30 e +75 s | **0** durante, **0** dopo |
| 200 file di prova, 64 alla volta | picco **108**, **108** lasciate fino a +75 s; il server PostgreSQL a 197 di 300 | **0** / **0** |
| 600 file di prova, 64 alla volta | non ripetuta: avrebbe preso i posti degli altri | **0** / **0**, 600 × 200 in 1,6 s |
| 200 pagine dell'hub, 32 alla volta | fermata dalla mia sicurezza a 192 richieste: **151** connessioni, 151 lasciate a +30 s | picco **8**, **0** dopo |
| 600 pagine dell'hub, 64 alla volta | — | picco **8**, **0** dopo, 600 × 200 in 37,9 s |
| 5 browser headless sul selettore che incornicia H-B | 7 · 13 · 19 · 26 · **32**; 32 con le pagine ferme da 20 s; **32** a browser chiusi, +3 s e +30 s | **0** a ogni passo |
| Thread del processo dopo la raffica | 4–5: nessun thread di richiesta vivo, 84–108 connessioni di nessuno | 2–7, 0 connessioni |

La correzione fa ciò che dice. Due cose vanno chiuse in un commit successivo, e nessuna delle due impedisce di tenere acceso il server riavviato: il tetto conta *posti*, e un posto si può perdere senza che nessuna connessione sia aperta (W2-1); la pagina con cui il proprietario sceglie riporta l'ordine del consiglio (W2-2).

---

## 1. Che cosa è stato verificato

| # | Richiesta | Esito | § |
|---|---|---|---|
| 1a | La causa riprodotta sul commit precedente, su un server mio | **sì** | 2.1 |
| 1b | Il meccanismo visto da dentro: chi tiene le connessioni, che cosa le libera | **sì** | 2.1 |
| 1c | La correzione tiene il tetto dichiarato e non lascia nulla dopo 10 s | **sì** — 0 già a +1 s in ogni cella | 2.2 |
| 1d | Il tetto regge anche con client che si comportano male | **in parte** — regge il conteggio delle connessioni; non regge il conteggio dei posti (W2-1) | 2.3 |
| 2a | Nessun limite alzato | **sì** | 2.4 |
| 2b | Solo sviluppo: sotto `config.settings.prod` nessuna impostazione dell'anteprima | **sì** | 2.4 |
| 2c | Dentro la riga di proprietà dell'ingegnere dell'anteprima; LF | **sì** | 2.4 |
| 2d | Le pagine normali non cambiano; la CSP di `/fr/` identica al byte | **sì**, a parità di seme di hash; contro il processo vivo di 8770 l'ordine delle direttive è diverso per costruzione (O1) | 2.5 |
| 3a | `variant=he`, `e1`, `e2`, `e3`: 200 con «manca» finché il file non c'è, dal vivo quando arriva, senza riavvio | **sì** | 2.6 |
| 3b | Valori sconosciuti → 400 | **sì** | 2.6 |
| 3c | I rifiuti del resolver intatti (uscita dalla radice, segmenti con il punto, nomi 8.3, `.py` / `.ps1` / `.log`) | **sì** — 49 × 404 su 50; il cinquantesimo è il `%00` → 500 già noto, non dell'anteprima (O2) | 2.7 |
| 3d | Intestazioni e meta robots ovunque; template puliti per la CSP | **sì** | 2.8 |
| 3e | Parole neutre, nessun candidato favorito | **no** (W2-2) | 2.9 |
| 4 | I test, eseguiti da me sulla corsia `ile_lane5` | **130 passati**; i denti verificati con tre mutazioni applicate dall'esterno | 2.10 |

---

## 2. Le prove

### 2.1 La causa, riprodotta

**Censimento all'inizio (21:22).** 89 connessioni client sull'intero PostgreSQL (limite 300, `idle_session_timeout = 0`, ruolo `ile` superutente, nessun limite per ruolo o database): `ile` 24 ferme, la più vecchia di 3 giorni e 23 ore; `ile_qa` 7, 4 giorni e 14 ore; `ile_v5` 57, 3 ore e 54 minuti — il server ufficiale 8780 (PID 37080, avviato alle 14:47:10) ancora sul codice vecchio. Erano 17 alle 18:30 e 48 alle 20:33: cresceva a ogni visita, come scrive la nota.

**Raffiche di file di prova sul commit precedente** (`s1_pre.py`; server 8786 dalla worktree `aa2eab4`, un server nuovo per cella; i 22 file che un caricamento di `home/options/hb-phase3.html` chiede davvero, un socket per richiesta):

| n × c | Prima | Picco | Alla fine | +1 s | +10 s | +30 s | +75 s | Thread del processo: prima → +1 s → +75 s | Che cosa sono |
|---|---|---|---|---|---|---|---|---|---|
| 200 × 32 | 0 | 92 | 84 | 84 | 84 | 84 | **84** | 5 → 5 → 4 | 84 `idle`, colonna `query` **vuota** |
| 200 × 64 | 0 | 108 | 108 | 108 | 108 | 108 | **108** | 5 → 5 → 4 | 108 `idle`, `query` vuota |

Oltre i 60 s di `CONN_MAX_AGE` nulla cambia; spento il server, 0. Le cifre non coincidono con quelle della nota (85 e 84) e non devono: dipendono dal momento in cui passa il garbage collector.

**Da dentro il processo** (`s2_probe.py`: lo stesso `runserver` con un osservatore — un riferimento debole a ogni wrapper che apre una connessione):

| Momento | PostgreSQL | Thread Python | Connessioni aperte finora / da quanti thread / di cui vivi | Wrapper in memoria / con connessione aperta | Raccolte gen0 / gen1 / gen2 |
|---|---|---|---|---|---|
| avvio | 0 | 2 | 1 / 1 / 1 | 1 / 0 | 115 / 10 / 0 |
| 200 × 32, +2 s | **101** | **2** | 201 / 201 / **1** | 102 / **101** | 126 / 11 / 1 |
| +70 s | **101** | 2 | 201 / 201 / 1 | 102 / 101 | 126 / 11 / 1 — nessuna raccolta in 68 s |
| dopo `gc.collect()` | **0** | 2 | — | 1 / 0 | 9 858 oggetti irraggiungibili |

Duecento richieste, duecento connessioni, duecento thread; i thread sono finiti, 101 connessioni sono rimaste aperte di nessuno, e sono sparite nell'istante in cui il collettore è stato chiamato. È il meccanismo che la nota descrive (§1.4, §3.2), con gli stessi contatori del collettore.

**Cinque browser headless** (`s4_live.py`, un profilo ciascuno, 35 richieste per caricamento): 7, 13, 19, 26, 32 connessioni; 32 con le pagine aperte e ferme da 20 s; 32 a browser chiusi, a +3 s e a +30 s; 4 thread nel processo. (Le quattro che c'erano prima del primo browser le avevano lasciate le quattro pagine del sito chieste un momento prima.)

**Il registro del server ufficiale**, letto alle 21:33, prima che il riavvio lo sovrascrivesse (W2-4): 106 risposte 500 — 15:36 9 · 15:37 3 · 15:38 9 · 15:39 44 · 15:40 13 · 15:41 1 · 15:43 1 · 15:50 1 · 15:52 2 · 15:53 1, poi 17:20 2 · 17:21 4 · 17:25 8 · 17:26 5 · 17:27 3 — 100 su `/__design-v5/proof/…` e 6 su `/fr/`. Ogni traccia passa per `handlers/base.py:197` → `contextlib.py:84` → `transaction.py:198 __enter__` → `ensure_connection` → `psycopg.connect`: l'errore nasce nella transazione di `ATOMIC_REQUESTS`, **prima** della vista, come dice la nota. Nessuna delle tracce contiene un frame di `designpreview`: la vista non era ancora stata chiamata (il mandato di questa revisione la dava come ultimo frame).

**Ciò che toglie la causa lo conferma.** Con la vista dei file di prova rimessa in transazione (dall'esterno, §2.10) il test di regressione conta «96 connections were opened by 96 request threads»; senza, zero.

### 2.2 La correzione, misurata

Un solo server per tutte e sette le celle (`s3_post.py`), connessioni contate per `application_name`:

| Che cosa | n × c | Picco | +1 s | +10 s | +30 s | Risposte | Tempo |
|---|---|---|---|---|---|---|---|
| file di prova | 200 × 32 | **0** | 0 | 0 | 0 | 200 × 200 | 0,6 s |
| file di prova | 200 × 64 | **0** | 0 | 0 | 0 | 200 × 200 | 1,1 s |
| file di prova | 600 × 64 | **0** | 0 | 0 | 0 | 600 × 200 | 1,6 s |
| hub (tre `SELECT`) | 200 × 32 | **8** | 0 | 0 | 0 | 200 × 200 | 10,9 s |
| hub | 200 × 64 | 4 | 0 | 0 | 0 | 200 × 200 | 11,0 s |
| hub | 600 × 64 | **8** | 0 | 0 | 0 | 600 × 200 | 37,9 s (mediana 4,1 s, massimo 12,1 s) |
| misto: hub, i due selettori, un file mancante, `/fr/`, un CSS | 600 × 64 | 3 | 0 | 0 | 0 | 500 × 200, 100 × 404 | 11,2 s |

A riposo, dopo tutte: 0. Nessun 503. Inoltre:

* **Tetto dall'ambiente e nome di default** (`s6_ceiling.py named`: server avviato senza `PGAPPNAME`, `ILE_DESIGN_PREVIEW_DB_CEILING=3`): le connessioni portano `ile-design-preview`; hub 200 × 32 → picco **3**, 0 dopo; file di prova 200 × 64 → 0 / 0.
* **Keep-alive**: 64 socket persistenti, 384 richieste (hub e selettore): picco 5; con i 64 socket aperti e fermi da 10 s, **0** — un thread vivo su un socket fermo non tiene più una connessione.
* **Cinque browser**: 0 a ogni passo.
* **Il server ufficiale dopo il riavvio** dell'orchestratore (PID 28896, 21:52:32): alle 22:04 l'intero PostgreSQL non aveva una sola connessione client; dopo cinque GET su 8780 (hub 200 in 0,14 s, due selettori, un file di prova, `/fr/`) e una su 8770, `select count(*) … where application_name = 'ile-design-preview'` → **0**, e nessuna connessione su `ile`.

Il censimento è un campionamento (venti letture al secondo, 755 durante la raffica più lunga): che il tetto non possa essere superato lo dice il semaforo, e lo conta senza caso `test_no_more_connections_than_the_ceiling_whatever_arrives`.

### 2.3 Il tetto e i client che si comportano male

`s6_ceiling.py`, `s7_leak.py`; server proprio, cartella delle prove di servizio.

| Prova | Esito |
|---|---|
| 120 GET abbandonate appena inviate (metà con RST) su hub, `/fr/`, file mancante | picco 4, 0 dopo 3 s, hub 200: **nessun posto perso** — come la prova dell'ingegnere |
| 40 GET azzerate a metà risposta | nessun posto perso |
| 8 POST con `Content-Length: 100000` e dieci byte di corpo, socket tenuti aperti | tutte ricevono `403 Forbidden` (CSRF, prima che il corpo sia letto); poi **hub e file di prova 503 dopo 20,0 s**, «Anteprima occupata: le 8 connessioni al database concesse a questo server sono in uso…» — mentre PostgreSQL conta **0** connessioni del server |
| … quattro chiuse con FIN | i posti tornano: hub 200 in 0,06 s |
| … quattro chiuse con RST | **i quattro posti non tornano più**: posti liberi 4 su 8 |
| 8 POST come sopra, tutte chiuse con RST dopo la risposta | hub **503** dopo 20 s; 25 s dopo ancora **503**; selettore e file di prova **503**; 0 connessioni, nessun thread di richiesta vivo: **l'anteprima è spenta fino al riavvio**, e nel registro non c'è una riga nel momento in cui succede |

È il rilievo W2-1. Il 503 stesso è come dichiarato: `text/plain`, `Retry-After: 2`, `Cache-Control: no-store`, `X-Robots-Tag: noindex, nofollow`, `X-Content-Type-Options: nosniff`.

### 2.4 Nessun limite alzato, solo sviluppo, perimetro

* **Limiti.** Il commit non tocca `docker-compose.yml` né `base.py`; `max_connections` compare soltanto come fatto nella nota e in un'asserzione («the answer to the outage is not a higher limit»). PostgreSQL: `max_connections = 300`, come prima.
* **Impostazioni risolte in un interprete nuovo per caso** (`settings_probe.py`; chiave di 64 caratteri generata e buttata con il processo):

| Caso | Impostazioni con «PREVIEW» nel nome | App | Primo middleware (quanti) | `CONN_MAX_AGE` | `OPTIONS` | `/__design-v5/` | Modulo `designpreview` importato |
|---|---|---|---|---|---|---|---|
| `prod`, ambiente pulito | nessuna | no | `SecurityMiddleware` (18) | 60 | `{}` | `Resolver404` | no |
| `prod` con `ILE_DESIGN_PREVIEW=1`, `…_DB_CEILING=3`, `PGAPPNAME`, `…_PROOF_DIR` | nessuna | no | `SecurityMiddleware` (18) | 60 | `{}` | `Resolver404` | no |
| `prod`, le stesse e `DJANGO_DEBUG=1` | nessuna | no | `SecurityMiddleware` (18) | 60 | `{}` | `Resolver404` | no |
| `test`, con le stesse variabili | nessuna | no | `SecurityMiddleware` (18) | 0 | `{}` | `Resolver404` | no |
| `dev`, senza flag | flag `False`, cartella | no | `SecurityMiddleware` (18) | 60 | `{}` | `Resolver404` | no |
| `dev`, flag e `DJANGO_DEBUG=0` | flag `False`, cartella | no | `SecurityMiddleware` (18) | 60 | `{}` | `Resolver404` | no |
| `dev`, flag | flag, cartella, tetto 8 | sì | `ConnectionCeilingMiddleware` (19) | 0 | `application_name = ile-design-preview` | `designpreview:hub` | sì |

  Sotto `prod` il file `.env` non viene letto. Senza il flag `dev.DATABASES` e `dev.MIDDLEWARE` sono gli oggetti di `base`: gli altri server di sviluppo non cambiano.
* **Perimetro.** `git diff --name-status aa2eab4 da75812`: un file nuovo dell'app (`middleware.py`), la nota, e sette file modificati — `services.py`, `views.py`, `designpreview.css`, `frame.html`, `hub.html`, il test, e `config/settings/dev.py`, i cui due blocchi aggiunti stanno entrambi dentro `if ILE_DESIGN_PREVIEW:`. Tutto nella riga di proprietà. `git ls-files --eol` → `i/lf w/lf` per tutti; 0 byte CR, nessun BOM, newline finale, `git diff --check` pulito. Nelle righe aggiunte nessun segreto: l'URL del database è abbreviato.

### 2.5 Le pagine normali

* **Lo stesso seme, lo stesso database, i due commit affiancati** (8786 `da75812`, 8787 `aa2eab4`, `PYTHONHASHSEED=0`): `/fr/`, `/ar/`, `/fr/compte/login/`, `/fr/espace-reserve/` — stesso stato (200, 200, 200, 302), stessi nomi di intestazione, stessi valori (fuori da data, cookie, identificativo di richiesta e, sul login, `Expires`, che è un orario), **stessa CSP al byte**, stesso corpo al byte una volta tolti il token CSRF e la porta negli URL assoluti (53 044, 54 566, 21 447 e 0 byte). Nessun `X-Robots-Tag`.
* **Quattro alberi, lo stesso seme, in processo** (`inproc_page.py`, `PYTHONDONTWRITEBYTECODE=1`, nulla scritto in `main`): l'albero di `main`, `aa2eab4` con il flag, `da75812` con il flag — cioè attraverso il middleware del tetto — e `da75812` senza. CSP di `/fr/` e di `/fr/compte/login/`: SHA-256 `7e7d7b0b…205b1` in tutti e quattro (lo stesso valore della revisione W1; la stringa è in `s4_live.json`, i corpi in `bodies/`); corpo di `/fr/`: 52 992 byte, SHA-256 `f4e18130…` in tutti e quattro.
* **Contro il processo vivo di 8770**: le stesse 11 direttive con gli stessi valori, 221 byte, intestazioni con gli stessi nomi e valori; le due stringhe grezze **non** sono uguali al byte, perché l'ordine delle direttive è diverso (O1).

### 2.6 Il catalogo

`s5_catalogue.py`: server proprio con `ILE_DESIGN_PREVIEW_PROOF_DIR` su una cartella di servizio; la cartella vera non è stata toccata.

| Stato della cartella | Hub, gruppo «H-E — nuova direzione» | `variant=he` / `e1` / `e2` / `e3` |
|---|---|---|
| niente di H-E | 7 voci «… · manca», nessun link | 200, nessun iframe, «Il file research/hero/he/… non è nella cartella delle prove», bandierina «non approvato · il file manca», la scelta barrata |
| una cartella `concepts/e2/` vuota | — | ancora «manca»: una cartella non è un file |
| i sei file scritti, senza riavvio | 7 link, nessun «manca» | 200, iframe sul file giusto; `he&lang=ar` incornicia `ar.html` con «da non firmare come /ar/»; i sei file serviti con gli stessi byte |
| `index.html` tolto di nuovo | — | `he` di nuovo senza iframe, «il file manca» |

* **Sconosciuto → 400**, sigillato, senza iframe, con i valori noti e «Torna a H-0»: `variant=hz`, `HE`, `e4`, `e0`, `e`, vuoto, `he%00`, `<script>…` (riflesso con l'escape), `lang=de`, `lang=AR`, `phase=9`, e `system=zz`, `surface=nope`, `lang=de` sul selettore tipografico. Con un parametro ripetuto vale l'ultimo valore, come sempre in Django.
* **Noto ma mai costruito → 200 e lo dice**: `e1&lang=ar`, `he&phase=interim`, `e3&phase=interim` — «Questa combinazione non esiste: E1 è un prototipo di ricerca, costruito soltanto in fr · fase 3.»
* **Sulla cartella vera** (sola lettura): hub 200 con 130 link e 4 «manca» (la pagina finale fr e ar, la sua voce del selettore, il campione CTA); le 36 combinazioni del primo schermo tutte 200 e sigillate; `e1`, `e2`, `e3` dal vivo, `he` con «manca»; H-0, H-A, H-B portano «maquette del gate 0 — non approvata», gli altri sei «prototipo di ricerca — non approvato».
* Il tasto `e` porta a H-E, `d` a H-D; `1` e `2` non fanno nulla: i concetti non hanno tasto.

### 2.7 Il resolver delle prove

50 richieste grezze (`http.client`, nessuna normalizzazione del percorso) su una cartella di servizio con una cartella `.work` (alias 8.3 `WORK~1`, verificato con `dir /x`), una giunzione verso una cartella esterna, file `.py`, `.ps1`, `.log`, `.sh`, `.jsonl`, `.gz`, un nome con la tilde:

* **49 × 404**: `../`, `..%2f`, `%2e%2e/`, `..%5c`, barre rovesciate, `..%252f`, `....//`, `C:/Windows/win.ini`, `C:%5c…`, `/C:/…/.env`, `//127.0.0.1/c$/…`; `linkout/outside.html` (la giunzione); `.work/notes.html`, `%2ework/…`, `home/.hidden.html`, `home/.git-status-after.txt`; `WORK~1/notes.html`, `work~1/…`, `home/a~b.html`; `build.py`, `perf_run.log`, `run.ps1`, `run.py`, `notes.sh`, `data.jsonl`, `archive.gz`, `page.html.py`; `run.py/.html`, `run.py::$DATA`, `phase3.html::$DATA`, `phase3.html.`, `phase3.html%20`, `phase3.html:stream.css`; cartelle, barra finale, `//`, `./`, `CON.html`, `NUL.css`, un file mancante.
* **1 × 500**: `tools/run.py%00.html` — `DataError` in `cms/middleware.py:75`, nessun frame dell'anteprima: è l'osservazione O2 delle due revisioni precedenti, invariata.
* Serviti come devono: `index.html`, `home/phase3.html`, `assets/css/x.css`, un file con una stringa di query, una cartella dal nome lungo che finisce in `.work` senza cominciare con il punto — e `HOME/PHASE3.HTML`, lo stesso file, perché questo file system non distingue le maiuscole.

### 2.8 Intestazioni, meta robots, CSP

* `X-Robots-Tag: noindex, nofollow` e `Cache-Control: no-store` su hub, 36 + 18 stati dei selettori, le risposte 400, i file di prova, le `HEAD`, il 503 del tetto. `<meta name="robots" content="noindex, nofollow">` e `lang="it"` su hub e selettori; `Content-Language: it`.
* I rifiuti sono risposte di Django e non portano le due intestazioni — 404 di un file mancante, 403 del CSRF su `POST` / `PUT` / `DELETE`, 405 di `OPTIONS` (`Allow: GET, HEAD`) — come dice `apps/designpreview/__init__.py`.
* Un file di prova: `X-Frame-Options: SAMEORIGIN` e `frame-ancestors 'self'`; un selettore: `frame-src 'self'`; l'hub: la policy del sito, senza aggiunte.
* **Nel browser** (11 pagine: hub, `he`, `he` ar, `e1`, `e2`, `e3`, una combinazione mai costruita, `hb`, `hd`, un 400, il selettore tipografico): **0 violazioni CSP in tutti i frame**, 0 richieste fallite, 0 errori in console (salvo la riga del browser per il documento 400 stesso), 0 attributi `style`, 0 `<style>`, 0 script inline. Sorgenti dei tre template: nessun `style=`, nessun gestore, un solo `<script>` con `src` e `defer`.

### 2.9 La barra, rimisurata, e le parole dell'hub

Il foglio dell'anteprima è cambiato: 80 misure in Chromium headless, dieci stati a otto larghezze.

| Larghezza | Primo schermo (nove scelte) | Tipografia |
|---|---|---|
| 360, 390, 430 | **121 px**, tre righe di scelte, in tutti e sette gli stati provati; la bandierina dice «non approvato/a» sempre, seguita da «il file manca», «combinazione inesistente» o «da non firmare come /ar/» | 105 px |
| 768 | 117 px; 137 con l'avviso dell'arabo | 117 px; 137 |
| 1024 | 117 px (il palco è 651 px su 768) | 117 px; 137 |
| 1280, 1366, 1440 | 77 px | 77 px (97 a 1280 con l'avviso dell'arabo) |

Nessun traboccamento, né della pagina né della barra, nessun link fuori dalla finestra; il bersaglio più piccolo è 26 × 32 px. Le cifre della nota (§8) tornano. L'hub a 1440 e a 390: nessun traboccamento orizzontale, etichette italiane, nessun ornamento.

**Le parole.** Il gruppo «La home» non è cambiato nel merito: descrive, dice che cosa ogni direzione chiede alle regole, e per H-C e H-D rimanda al consiglio. Il gruppo di H-E dice «Direzione nuova autorizzata dal proprietario il 2 ottobre; in costruzione; revisione indipendente a seguire; decide il proprietario — O67» sotto l'etichetta «prototipo di ricerca — non approvato»: un fatto, non un merito. Il gruppo «Consiglio sull'hero» dice: «Cinque seggi su cinque: nessuno tra H-0, H-A, H-B, H-C e H-D raggiunge, così com'è costruito, il livello richiesto; **nell'ordine dato dalla maggioranza: H-D, H-C, H-A, H-B, H-0.** Il consiglio non approva nulla e non impone un vincitore: decide il proprietario (O67).» È il rilievo W2-2.

### 2.10 I test

* `tests/frontend/test_design_preview.py` su `ile_lane5`: **130 passati** in 45,0 s, nessuno saltato (compresi l'alias 8.3, la giunzione, i due test nel browser e il confronto con la cartella vera).
* **I denti**, con tre mutazioni applicate da un plugin fuori dal repository (`rw2_mutate.py`, `-p rw2_mutate`; nessun file della worktree toccato):

| Mutazione | Test che cadono |
|---|---|
| la vista dei file di prova di nuovo in transazione | 3 — «96 connections were opened by 96 request threads»; «Expected to perform 0 queries but 10 were done»; il test che guarda il marcatore |
| il posto reso senza chiudere la connessione | 2 — `[4, 7, 10, 13, 16, 19, …]` invece di 4 ogni volta; «PostgreSQL counted 14 backends from a burst under a ceiling of 2» |
| un tetto che non limita | 4 — fra cui «PostgreSQL counted 7 backends from a burst under a ceiling of 2» |

  Sono i numeri che la nota dichiara al §7.
* **La suite intera non è stata eseguita.** L'ho avviata sulla corsia 5 e l'ho fermata io a circa 190 test su 3 370 (un test ogni quattro secondi: ore); ai primi 107 nessun fallimento né errore. Un tentativo successivo di dimensionare un'esecuzione più piccola sui vicini è stato rifiutato dal controllo dei permessi della sessione, e non l'ho ripetuto. Vale quindi soltanto per il modulo dell'anteprima.

---

## 3. Rilievi

### W2-1 — MAGGIORE · il tetto perde un posto per sempre quando `request_finished` non arriva

**Fatto.** `ConnectionCeilingMiddleware` rende il posto a `request_finished`, tranne per un `FileResponse`. Sotto `runserver` quel segnale parte da `ServerHandler.close()` (`django/core/servers/basehttp.py:156–158`), che **prima** legge il corpo della richiesta non ancora letto (`self.get_stdin().read()`) e **poi** chiude la risposta. Se la lettura resta in attesa — un corpo annunciato e mai arrivato — il posto resta preso finché il client tiene il socket. Se la lettura fallisce — il client azzera la connessione — `wsgiref` inghiotte l'eccezione, `request_finished` non parte, il thread finisce e il posto non torna: nessun altro lo può rendere. Misurato al §2.3: otto richieste così e hub, selettori e file di prova rispondono 503 dopo 20 s, per sempre, con zero connessioni aperte e nessun thread di richiesta vivo. La riga di SQL del §5 della nota non lo vede (dice 0), e la frase del 503 dice una cosa non vera («le 8 connessioni … sono in uso»).

Il test `test_a_file_response_gives_its_slot_back_before_it_is_sent` fissa proprio questo come voluto: una pagina mai chiusa, servita da un thread che è già finito, tiene l'unico posto («a page keeps its slot until it is finished»).

**Quanto pesa.** Le rotte dell'anteprima sono GET e HEAD e non lo provocano: 160 GET interrotte non hanno perso nulla. Ma il server dell'anteprima è il sito intero, e il tetto sta davanti a ogni rotta: basta un invio a cui il server risponde prima di aver letto il corpo e che il client abbandona dopo la risposta. L'ho misurato con il 403 del CSRF su una richiesta senza cookie; per costruzione vale per ogni risposta data senza leggere il corpo. Otto in tutta la vita di un processo `--noreload`, e l'anteprima è di nuovo spenta — per un motivo che non è il database. La frase della nota «Una richiesta interrotta non perde il suo posto» (§3.5) vale per le GET soltanto.

**Correzione** — verificata fuori dal repository, senza toccare un file. In `__call__`, rendere il posto all'uscita dal middleware per ogni risposta che non sia uno stream diverso da un file:

```python
if isinstance(response, FileResponse) or not getattr(response, "streaming", False):
    give_back()
```

`give_back()` chiude già la connessione del thread prima di rendere il posto, e all'uscita dal primo middleware una risposta non in streaming è già scritta per intero: «connessioni aperte ≤ posti presi» resta vero, e un client fermo o sparito non tiene più nulla. Con la modifica applicata dall'esterno (`fixed_server.py`): otto corpi attesi → hub 200 in 0,45 s; dopo otto RST → hub, selettore e file di prova 200; hub 600 × 64 → picco 7, 0 dopo; misto 600 × 64 → picco 6, 0 dopo; e **129 test su 130** passano — cade soltanto l'asserzione che fissa il comportamento da cambiare. Da fare nello stesso commit: invertire quell'asserzione; aggiungere il test di regressione (tetto 1, una pagina servita su un thread che finisce senza `response.close()`, la richiesta successiva riceve 200); correggere la docstring del middleware e la frase del §3.5; far dire al 503 «posti», non «connessioni in uso». Resta scoperto, e va scritto, lo stream che non è un file: in `apps/` oggi non c'è uno `StreamingHttpResponse`, soltanto due `FileResponse`.

**Nel frattempo.** Se il registro di 8780 mostra «Design preview: the 8 database slots stayed taken for 20 s» mentre la riga di SQL dice 0, i posti sono persi: riavviare.

### W2-2 — MAGGIORE · l'hub stampa una classifica dei cinque primi schermi

**Fatto.** §2.9: «nell'ordine dato dalla maggioranza: H-D, H-C, H-A, H-B, H-0». È attribuita, è detta una volta sola, e un test la tiene. Tre cose però:

1. è una classifica sulla pagina con cui il proprietario decide O67. Il rilievo W1-1 l'ha già detto di un'altra frase attribuita: «L'attribuzione […] è onesta ma non toglie la classifica dalla pagina»;
2. è più netta del verbale da cui viene (`HERO_COUNCIL_REVIEW.md` §0, §1.1, §1.2): «Fourth place has no majority»; tre dei quattro confronti a coppie finiscono 3 a 2; un seggio mette H-D ultimo e un altro mette H-C primo; «This is a count of places. It is not a score, and the chairs' scores cannot be added»; e il seggio che preferisce H-C scrive «It does not say H-C should be chosen»;
3. la direttiva V5.3, §11: «Voglio vedere H-E realmente in Chrome. Non voglio scegliere sulla base del report del council.»

**Correzione.** Togliere l'ordine dalla frase del gruppo — restano «cinque seggi su cinque: nessuno … raggiunge … il livello richiesto», «il consiglio non approva nulla e non impone un vincitore: decide il proprietario», e il percorso del verbale, dove l'ordine sta con le sue riserve — e aggiornare le due asserzioni che lo tengono (`test_the_hub_says_that_a_research_prototype_is_not_approved_wherever_one_stands`, `test_the_hub_names_the_council_record_as_text_and_serves_none_of_it`) e la frase della docstring di `services.py`. Se l'orchestratore vuole invece l'ordine sulla pagina, che sia con le sue riserve. Testo soltanto: nessun effetto sulla stabilità né sulla sicurezza.

### W2-3 — MINORE · la diagnosi tace due fatti del repository che completano il «perché»

**Fatto.** (a) `.env.example`, righe 32–33, dal 21 settembre (`156e41a`): «Secondi di vita di una connessione al database riusata. 0 = nessun riuso.» — `DB_CONN_MAX_AGE=0`. Il `.env` in uso in `design-v5` è una copia precedente a quella riga (gli mancano undici chiavi dell'esempio) e nemmeno quello di `main` ce l'ha: i server giravano con i 60 s di `base.py`. Con la riga ogni richiesta avrebbe aperto e chiuso la sua connessione: è il «candidato 1» del §3.3 della nota (picco 5–14, 0 dopo — misura dell'ingegnere, che non ho ripetuto). (b) `docker-compose.yml`, righe 4–8 (`06f9986`, 21 settembre): il limite è già stato alzato una volta, da 100 a 300, per lo stesso sintomo, con il commento «which looks like a code failure and is a capacity one». Le misure di oggi dicono il contrario.

**Correzione.** Due frasi nella nota (§1.1 e §6, R2–R4). Per l'orchestratore, fuori dalla proprietà dell'anteprima: la riga nei `.env` di ogni worktree oppure, meglio perché un `.env` invecchia, `CONN_MAX_AGE = 0` in `config/settings/dev.py` fuori dal blocco dell'anteprima (è R4; anche la documentazione di Django sconsiglia le connessioni persistenti sotto il server di sviluppo, che apre un thread per richiesta); e il commento di `docker-compose.yml` da correggere da chi lo possiede.

### W2-4 — MINORE · il registro citato dalla nota è stato sovrascritto dal riavvio

**Fatto.** `C:/tmp/ile_v5_council/.work/servers/srv8780.log` è ripartito da zero con il riavvio delle 21:52. Ciò che avevo già riletto sta al §2.1: le 106 risposte 500, la loro distribuzione, le rotte, il punto della traccia. Non avevo ancora ricontato il carico per minuto e i «60 caricamenti, 1 353 richieste» del §2.3–§2.4 della nota: ora non lo può più fare nessuno.

**Correzione.** Una riga al §2.3 della nota; per l'orchestratore, i registri dei server aperti in aggiunta o con un nome per avvio.

### W2-5 — MINORE · due commenti rimasti indietro

**Fatto.** `apps/designpreview/__init__.py` («the hero picker (H-0, H-A, H-B and the two research directions H-C, H-D)») e l'intestazione di `static/js/dev/designpreview.js` («Hero picker: 0 a b c d for the variant») non conoscono H-E, il tasto `e` e i tre concetti senza tasto. Il comportamento è giusto: il tasto viene dai dati.

**Correzione.** Aggiornare le due frasi.

---

## 4. Osservazioni (nessuna azione su questo commit)

* **O1 — la CSP contro il processo vivo di 8770.** django-csp 4.0 itera un `set` (`csp/utils.py:93`): l'ordine delle direttive dipende dal seme di hash del processo, e due processi avviati senza `PYTHONHASHSEED` non emettono la stessa stringa nemmeno dallo stesso albero. L'identità al byte è quella del §2.5, a parità di seme.
* **O2 — `%00` → 500**, preesistente, di `cms.LegacyURLMiddleware`: invariato (le due revisioni precedenti lo danno già sul tabellone).
* **O3 — l'hub legge ancora il database.** Selettori e maquette non lo toccano più; l'hub sì (tre `SELECT`). Finché un altro server di sviluppo perde connessioni — qualunque `runserver` senza durata zero — un PostgreSQL saturo da altri farebbe rispondere 500 all'hub. Dopo il riavvio delle 21:52 anche 8770 si comporta come con la durata zero (nessuna connessione dopo una richiesta; il suo ambiente non lo posso leggere): vale finché ogni avvio se ne ricorda. Ciò che rende stabile l'ambiente, e non soltanto l'anteprima, è R4 su `main` (W2-3).
* **O4 — il tetto mette in coda tutto**, anche ciò che non chiede nulla al database: con 64 richieste in volo sull'hub l'attesa mediana è 4,1 s e la massima 12,1 s, su 20. Il collo è il processore, non il tetto (la nota misura 34,5 s con il tetto e 31,2 s senza); a questo passo — una stima, non una misura — i primi 503 arriverebbero oltre circa trecento richieste dell'hub in coda, come previsto. Il semaforo non serve in ordine d'arrivo.
* **O5 — le cifre che non coincidono con la nota** stanno tutte dentro il caso del collettore: 84 e 108 lasciate dove la nota ha 85 e 84; 101 nel processo dove ha 87; 151 sull'hub, fermata dalla sicurezza, dove ha 109 di picco e 61 lasciate.
* **O6 — a 1024 px** la barra del primo schermo è 117 px (era 77): 40 px di palco in meno. La nota lo dice.
* **O7 — i rifiuti** (404, 403, 405) non portano i sigilli, e non mostrano nulla dell'anteprima: invariato dalle revisioni precedenti.
* **O8 — limiti di questa revisione.** La raffica 600 × 64 sul commit precedente non è stata ripetuta (avrebbe preso i posti degli altri); la suite intera non è stata eseguita (§2.10); l'ultimo elenco di processi e porte, a fine lavoro, è stato rifiutato dal controllo dei permessi della sessione: che i miei server siano spenti lo dicono il controllo della porta dopo ogni arresto (`run.log`) e l'ultimo censimento di PostgreSQL, a lavoro finito — nessuna connessione client, nessuna con i miei nomi.

---

## 5. Ciò che la revisione conferma

* La causa è quella scritta nella nota, ed è provata: `ATOMIC_REQUESTS` apre una connessione per ogni chiamata a una vista, `runserver` dà un thread a ogni socket, e la connessione di un thread finito resta aperta finché il collettore non la trova. Riprodotta su un server mio, vista da dentro il processo, ritrovata nel registro dell'interruzione.
* La correzione la toglie dove nasce — un file di prova e un selettore non aprono più una connessione — e mette un tetto a ciò che resta: 0 / 0 / 0 su tre raffiche di file di prova, mai più di 8 sull'hub a 32 e a 64 richieste in volo, 0 un secondo dopo ogni raffica, 0 con 64 socket fermi, 0 con cinque browser.
* Nessun limite è stato alzato; sotto `prod` e sotto `test` non esiste un'impostazione, un'app, un middleware o una rotta dell'anteprima, nemmeno con le variabili nell'ambiente; senza il flag gli altri server di sviluppo non cambiano; il commit sta nella riga di proprietà, in LF, senza segreti.
* Una pagina normale è la stessa al byte prima e dopo la correzione, intestazioni e corpo, e la sua CSP è quella di `main`.
* Il catalogo dice il vero: ciò che non è su disco è «manca», diventa un link alla richiesta successiva, torna «manca» se il file va via; un valore sconosciuto è un 400; il resolver non serve nulla di ciò che deve rifiutare.
* I test sono 130, passano, e cadono quando devono.

**Verdetto: PASS_WITH_FIXES.** Il server riavviato può restare acceso così com'è. W2-1 e W2-2 vanno chiusi in un commit successivo dell'ingegnere dell'anteprima — il primo prima di considerare l'anteprima stabile per giorni, il secondo prima di dire al proprietario «PREVIEW READY»; W2-3, W2-4 e W2-5 nello stesso passaggio, per la parte che gli appartiene.
