# Revisione indipendente dell'hub che si mette in pari e della vista di confronto — servizio, sicurezza, test — commit `37bf897`

| | |
|---|---|
| **Oggetto** | `design-v5: preview — the hub catches up (research step 0, X-1 … X-5) and a compare view for the two phone «Mes pièces»` — commit `37bf897` su `design-v5` (genitore `e10002f`), 10 file, +1 452 −153, compresa la nota `docs/design-v5/QA/PREVIEW_HUB_CATCHUP.md` |
| **Lente** | servizio, sicurezza e test: il perimetro del diff; le guardie del resolver delle prove; la vista di confronto come possibile cornice aperta; CSP, `X-Robots-Tag`, `Cache-Control`; vista non atomica e tetto delle connessioni; i denti dei test nuovi; `ruff`; LF. La neutralità delle parole, il disegno, il movimento e l'accessibilità sono di altre revisioni |
| **Ruolo** | Revisore indipendente, etichetta `review-serving` (non ha costruito nulla dell'anteprima) |
| **Data** | 4 ottobre 2026, 18:28–19:10 (ora locale) |
| **Verdetto** | **PASS_WITH_FIXES** — nessun rilievo bloccante, nessun maggiore; **tre minori** (HS-1: le metà «alias 8.3» dei due test nuovi passano in silenzio dove il volume non dà alias; HS-2: la tabella dei confronti non ha un invariante sulle lingue, e una chiave mancante sarebbe un 500 — oggi non raggiungibile; HS-3: quattro testi rimasti a «in costruzione» o a «frame.html» soltanto). Le guardie sono intatte e provate, la vista di confronto non incornicia nulla che non sia nella sua tabella, il tetto tiene: **8** connessioni di picco, **0** dopo |
| **Strumenti** | server proprio della worktree su `127.0.0.1:8785` (`DB_CONN_MAX_AGE=0`, `DATABASE_URL=…/ile_v5`, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, `runserver --noreload`), avviato e spento sei volte, fermato ogni volta con il solo albero dei suoi processi; censimento con una sessione psycopg in autocommit (`application_name = rs-census`) letta ogni 40 ms; richieste grezze `http.client`, un socket ciascuna, il percorso spedito com'è scritto; Playwright 1.63.0 headless (Chromium), profilo proprio `C:/tmp/ile_v5_council/.profiles/hub-review-serving/`, rimosso alla fine; corsia `ile_lane5` / `test_ile_lane5`; Python 3.13, Django 5.2.17, django-csp 4.0, pytest 9.0.3, ruff 0.16.8 |
| **Lucchetto** | `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` atteso in codice (`gate.py`: controllo ogni 15 s finché il file esiste, e inoltre corsia 5 senza connessioni e porta 8785 libera) prima di ogni esecuzione di test, di ogni mutazione, di ogni avvio del server; ricontrollato dentro lo script prima di ogni avvio del browser. 16 attese registrate in `gate.log` più le 2 del browser: tutte di 0 s |
| **Prove** | fuori dal repository, `C:/tmp/ile_v5_council/.work/hub-review-serving/` (copia della cartella di lavoro della sessione, `…/scratchpad/review-serving/`): `gate.py` e `gate.log`; `rs_mutate.py` (le sei mutazioni, in memoria); `live.py` (server, raffiche, censimento); `probe.py` (rotte, query ostili, resolver, link dell'hub, browser); `pages.py`, `normal.py`, `leakcheck.py`, `latent.py`, `aliases.py`; risultati `lane5-full.log`, `mut-*.log`, `live/burst-default.json`, `live/burst-named.json`, `live/probe.json`, `live/pages.json`, `live/normal.json`, `live/srv8785-*.log`; `resolver_old.txt` / `resolver_new.txt`, `po_old.txt` / `po_new.txt`, `old_tests.txt` / `new_tests.txt`. Le uscite di `leakcheck.py` e `latent.py` sono citate qui |

Il server ufficiale su 8780 e i server 8770, 8771, 8772 non sono stati fermati, riavviati né interrogati (stessi processi all'inizio e alla fine: 22340, 3520, 7032, 27536); il Chrome del proprietario (9223, processo 27532) non è stato toccato e quello di QA (9222) non era acceso; nessuna sessione PostgreSQL altrui terminata, nessuna impostazione cambiata; la cartella delle prove è stata soltanto letta; nessun comando git che scrive. Niente di ciò che segue è una decisione di design.

---

## 0. In breve

| Domanda della revisione | Risposta | § |
|---|---|---|
| Il diff resta nella riga dell'ingegnere dell'anteprima? | **sì** per tutto il codice: app, template, foglio, script, file di test; `config/` intatto, il middleware del tetto e `_preview_only` identici. Fuori dalla riga scritta c'è soltanto la nota `PREVIEW_HUB_CATCHUP.md`, come la nota dell'interruzione in `da75812` (O1) | 1.1 |
| Le guardie del resolver delle prove sono intatte e ancora provate? | **sì** — la sezione del resolver (102 righe) è identica al byte a `e10002f`; nessun test di guardia tolto o indebolito, otto rifiuti nuovi; **65 richieste grezze → 65 × 404** sul pacchetto vero, nelle cartelle nuove | 1.2 |
| La vista di confronto può diventare una cornice aperta? | **no** — le pagine vengono da `COMPARISONS`; 30 query ostili: 27 × 400 senza iframe, 3 × 200 soltanto dove i valori effettivi sono quelli della tabella; aggiunge `frame-src 'self'` e nient'altro; `frame-ancestors 'none'` e `DENY`: incorniciata dall'hub, il browser la rifiuta | 1.3, 1.6 |
| Sigilli | `X-Robots-Tag: noindex, nofollow` e `Cache-Control: no-store` su 200, 400 e `HEAD`; meta robots; nessun cookie | 1.3 |
| Non atomica, nessuna lettura, tetto | **sì** — 200 richieste di solo confronto a 32: **0** connessioni; 200 richieste hub + confronto a 32: picco **8**, **0** a +1 s e a +10 s, due volte (con il nome di default e con un nome mio) | 1.4 |
| I test | **159 passati, 0 saltati** in 50,6 s sulla corsia 5; sei mutazioni applicate fuori dall'albero, sei cadute | 1.5 |
| `ruff`, LF | puliti; `i/lf w/lf`, 0 byte CR, nessun BOM, `git diff --check` pulito | 1.1 |
| Rilievi | nessun bloccante, nessun maggiore; tre minori: HS-1, HS-2, HS-3 | 2 |

---

## 1. Le prove

### 1.1 Perimetro, LF, `ruff`, segreti

- `git diff --name-only e10002f..HEAD`: `apps/designpreview/{__init__,services,urls,views}.py`, `templates/dev/designpreview/compare.html` (nuovo) e `hub.html`, `static/css/dev/designpreview.css`, `static/js/dev/designpreview.js`, `tests/frontend/test_design_preview.py` — tutti nella riga del Preview Engineer di `AGENT_OWNERSHIP.md` — e la nota `docs/design-v5/QA/PREVIEW_HUB_CATCHUP.md` (O1). `config/` non compare; `apps/designpreview/middleware.py` non è toccato; `_preview_only` è identico riga per riga (`po_old.txt` / `po_new.txt`).
- `git ls-files --eol`: `i/lf w/lf` per i dieci file; 0 byte CR nell'albero e nei blob del commit; nessun BOM; newline finale ovunque; `git diff --check e10002f..HEAD` pulito.
- `ruff check` sui cinque file Python toccati e sull'app intera: «All checks passed!»; `ruff format --check`: «5 files already formatted» (6 sull'app intera).
- Segreti: nelle righe aggiunte e nel messaggio di commit nessuna chiave, token, password o URL di database; gli URL sono tutti `http://127.0.0.1:8780/…`, nella nota. I valori delle quattro chiavi API presenti nell'ambiente di questa macchina (fra cui quella di Pexels) non compaiono in nessun file di testo dell'intera cartella delle prove (ricerca a stringa fissa, stampati soltanto i nomi dei file: zero).

### 1.2 Le guardie del resolver delle prove

- **Il codice.** La sezione «Proof serving» di `services.py` — `PROOF_CONTENT_TYPES`, `resolve_proof_file`, `real_proof_path`, `proof_exists`, `proof_url`, 102 righe — è identica al byte fra `e10002f` e `37bf897` (stesso SHA-256, `resolver_old.txt` / `resolver_new.txt`). La rotta `proof/<path:path>` e i suoi decoratori non cambiano.
- **I test.** 65 funzioni di test prima, 76 dopo: una rinominata (`test_what_is_in_construction_…` → `test_what_is_not_on_disk_…`), undici nuove. Nessuna asserzione di guardia è stata tolta: le righe tolte riguardano soltanto lo stato «in costruzione» di H-E, i conteggi e i nomi dei template. `test_proof_refuses_what_it_must_with_a_404` ha otto casi nuovi (le cartelle `.work` di `he-motion` e di `door-master` per nome, `WORK~1` di `he-motion`, quattro `.py` delle corsie nuove, una cartella nuova chiesta come tale); due test nuovi guardano le cartelle puntate accanto alle voci nuove, sul pacchetto finto (`test_no_new_entry_reaches_a_dotted_or_short_name_folder`) e sul pacchetto vero (`test_beside_the_new_entries_the_real_package_s_working_folders_stay_closed`).
- **Sul pacchetto vero**, 65 richieste grezze nelle cartelle che il commit porta sull'hub. Ogni bersaglio esiste su disco — un 404 è del resolver, non dell'assenza — e gli alias sono quelli che il volume dà davvero (`GetShortPathNameW`, `aliases.py`): `he/.work` → `WORK~1`, `he/.source` → `SOURCE~1`, la `.work` dei tre concetti e di `he-motion` → `WORK~1`.

| Famiglia | Esempi | Richieste | 404 |
|---|---|---|---|
| cartelle puntate per nome | `he/.work/uiux/U1.txt`, `he/.work/perf_run.log`, `he/.source/8771-ar.html`, `concepts/e2/.work/21st/…png`, `he-motion/.work/spec_only.json` | 8 | 8 |
| i loro alias 8.3 | `WORK~1`, `work~1`, `WORK%7E1`, `SOURCE~1`, nei tre concetti e in `he-motion` | 9 | 9 |
| punto codificato, doppia codifica, larghezza piena, punto o spazio finale | `%2ework`, `%2Esource`, `%252ework`, `.%77ork`, `%EF%BC%8Ework`, `.work.`, `.work%20`, `WORK~1.` | 8 | 8 |
| traversata dentro una cartella puntata e fuori dalla radice | `cta/../.work/…`, `cta/%2e%2e/.work/…`, `cta/..%2f.work/…`, `..%2f` fino a `SIGNING_SHEET.md`, `..%5c`, `%5c..`, `....//` | 8 | 8 |
| script e bytecode delle corsie nuove, per nome e per alias | `he-motion/probe_he_motion.py`, `PROBE_~1.PY`, `__pycache__/….pyc`, `__PYCA~1/….pyc`, `he-21st/measure.py`, `BUILD_~1.PY`, `colour/build_specimen.py`, `documents/_tools/build.py`, `journey/_scratch/aria_probe.py`, `uiux-platform/proto/build.py` | 15 | 15 |
| suffissi | `.py.`, `.py%20`, `.py::$DATA`, `.py%3A%3A$DATA`, `.py/.html`, `SPEC-F~1.JSO`, `INDEX~1.HTM`, `index.html::$DATA` | 8 | 8 |
| unità, UNC, cartelle, dispositivi | `C:/tmp/…`, `C%3A/…`, `he/C:/x.html`, `//127.0.0.1/c$/…`, `he/`, `he`, `_tools/`, `CON.html`, `NUL.css` | 9 | 9 |

Il controllo «nessun contenuto nel corpo» ha segnalato quattro di questi 404: è la pagina 404 di `DEBUG` che ripete il percorso chiesto. Ricontrollati con `leakcheck.py`: 0 righe dei file nei corpi, su 5 cercate per ciascuno. Una sessantaseiesima richiesta, tenuta a parte, porta un `%00` (`…probe_he_motion.py%00.html`) e risponde 500: `DataError` in `cms/middleware.py:75`, nessun frame dell'anteprima nella traccia del registro — l'O2 di W1 e W2, invariato (O3).

### 1.3 La vista di confronto non è una cornice aperta

**Il codice.** `views.compare` passa a `_picker` una funzione che chiama `services.compare_view(root, pair, lang)`: un `pair` che non è una chiave di `COMPARISONS` o una `lang` che non è in `LANGS` sollevano `UnknownChoice` → 400; il file di ciascuna cornice è `side.files[lang]`, scritto nella tabella; l'URL è `proof_url(file)` soltanto se `proof_exists(root, file)` — lo stesso resolver delle prove —, altrimenti la frase che dice che cosa manca. Niente della query arriva in un `src`; i link della lingua sono costruiti da `compare_url` sulla tabella. Il 400 è quello di `frame.html`: senza barra, senza iframe, il valore ripetuto con l'escape.

**Le rotte, sul mio server.**

| Richiesta | Stato | Sigilli | CSP | `X-Frame-Options` | Cornici |
|---|---|---|---|---|---|
| `compare/` senza query | 200 | sì | `frame-src 'self'` · `frame-ancestors 'none'` | `DENY` | `uiux-platform/proto/docs-fr.html`, `documents/index.html` |
| `?pair=mes-pieces&lang=fr` | 200 | sì | idem | `DENY` | idem |
| `?pair=mes-pieces&lang=ar` | 200 | sì | idem | `DENY` | `uiux-platform/proto/docs-ar.html`, `documents/ar.html` |
| `HEAD ?pair=mes-pieces&lang=fr` | 200 | sì | idem | `DENY` | — |
| `?pair=zz`, in `GET` e in `HEAD` | 400 | sì | idem | `DENY` | nessuna |
| `POST`, `PUT`, `DELETE` | 403 dal CSRF, prima della vista | no: risposta di Django, nulla dell'anteprima (O6) | | | |
| `OPTIONS` | 405, `Allow: GET, HEAD` | no (O6) | | | |
| `/__design-v5/compare` | 301 → `/__design-v5/compare/` | | | | |
| `compare/x`, `compare/../proof/index.html` | 404 | | | | |

- Le quattro pagine incorniciate rispondono 200 con `frame-ancestors 'self'`, `X-Frame-Options: SAMEORIGIN`, i due sigilli e `text/html; charset=utf-8`.
- La policy della vista è quella del sito con una direttiva in più: 12 direttive, 239 byte, contro le 11 e i 221 byte di `/fr/`, `/ar/`, `/fr/compte/login/` e dell'hub sullo stesso server; `script-src 'self'`, `style-src 'self'`, nessun `unsafe`. `Content-Language: it`, meta robots, un solo `<script>` con `src`, nessun attributo `style`. Né l'hub né la vista di confronto mettono un cookie.
- **30 query ostili** (`probe.py`): `pair=zz`, vuoto, `MES-PIECES`, con uno spazio prima o dopo, con un trattino Unicode, `../.work`, `..%2F..%2F.work`, `%2e%2e%2f%2e%2e%2fSIGNING_SHEET.md`, il percorso relativo di una pagina della tabella e il suo percorso assoluto sotto `/__design-v5/proof/`, un percorso puntato e il suo alias, `C:/Windows/win.ini`, un URL esterno assoluto e uno senza schema, `mes-pieces%00`, `<script>…`, il parametro ripetuto nei due ordini, cinquemila caratteri, `pair[]=`, `lang=de`, `AR`, vuota, `../../.work`, `fr%00`, `lang` ripetuta, parametri estranei (`src=`, `frame=`, `w=`), `lang=it`. **27 × 400**: tutte sigillate, `frame-ancestors 'none'`, `DENY`, nessun iframe, il valore con l'escape (`&lt;script&gt;`). **3 × 200**, dove i valori effettivi sono quelli della tabella: `pair=../.work&pair=mes-pieces` (Django prende l'ultimo valore), `pair[]=mes-pieces` (un'altra chiave: vale il default), la coppia legittima con i parametri estranei (ignorati). In ogni risposta, ogni `src` è una delle quattro pagine della tabella.

### 1.4 Il database: non atomica, nessuna lettura, il tetto

- `views.compare` è avvolta da `_preview_only`, invariato e più esterno: `non_atomic_requests` sta sul callable che l'URLconf tiene (`test_no_preview_view_asks_for_a_transaction` lo verifica anche per il confronto); `_render_frame` rende `compare.html` senza i context processor della richiesta; `test_a_picker_and_a_proof_file_read_nothing` conta 0 istruzioni per fr, ar, il 400 e `HEAD`; `test_a_burst_of_proof_requests_opens_no_connection_and_leaves_none_behind` ha la vista nella sua raffica.
- **Le raffiche** (`live.py`; un socket per richiesta; ogni cella preceduta da un secondo di quiete e seguita dalle letture a +1 s e a +10 s):

| Server | Raffica | n × c | Risposte | Tempo | Picco | +1 s | +10 s |
|---|---|---|---|---|---|---|---|
| nome di default, `ile-design-preview` (la riga di SQL del §5 della nota dell'interruzione) | solo confronto: fr, ar, senza query, un 400 | 200 × 32 | 150 × 200, 50 × 400 | 1,99 s | **0** | 0 | 0 |
| | hub e confronto, metà e metà | 200 × 32 | 200 × 200 | 7,04 s (mediana 1,01 s, massimo 2,48 s) | **8** | 0 | 0 |
| | di nuovo | 200 × 32 | 200 × 200 | 6,62 s | 3 | 0 | 0 |
| nome mio, `ile-design-preview-rs` (`PGAPPNAME`) | solo confronto | 200 × 32 | 150 × 200, 50 × 400 | 1,06 s | **0** | 0 | 0 |
| | hub e confronto | 200 × 32 | 200 × 200 | 10,32 s (mediana 1,55 s, massimo 3,03 s) | **8** | 0 | 0 |
| | di nuovo | 200 × 32 | 200 × 200 | 7,61 s | 3 | 0 | 0 |

  A riposo, prima e dopo: 0; dopo l'arresto del server: 0. Nella seconda esecuzione il nome di default è rimasto a 0 per tutto il tempo: nessun altro server dell'anteprima ha aperto una connessione in quella finestra (e il registro di 8780 non ha richieste dopo le 16:50), quindi la prima esecuzione conta il mio server soltanto. Nessun 503, nessun 500 nei due registri. Da 26 a 243 letture per cella.

### 1.5 I test

```
DATABASE_URL=…/ile_lane5  TEST_DATABASE_URL=…/ile_lane5   (→ test_ile_lane5)
.venv/Scripts/python -m pytest tests/frontend/test_design_preview.py -q -p no:randomly -p no:cacheprovider -rfEsxX
→ 159 passed in 50.63s
```

0 saltati, 0 xfail, 0 avvisi: hanno girato i tre test nel browser, i test degli alias 8.3 e del collegamento, i due test sul pacchetto vero.

**I denti.** `rs_mutate.py` è un plugin pytest caricato con `-p rs_mutate` da fuori della worktree: riscrive in memoria, per una sola esecuzione, la guardia o la vista a partire dal suo stesso sorgente (`inspect.getsource`, una sostituzione, `exec` nel modulo); nessun file della worktree è toccato. Eseguito sui 147 test che non sono né nel browser né raffiche (12 deselezionati):

| Mutazione | Test che cadono | Messaggio, per esempio |
|---|---|---|
| `dot` — via il controllo del segmento puntato, sulla stringa e sul percorso reale | 10: sei casi di `test_proof_refuses_what_it_must_with_a_404` (`.work/notes.txt`, `.git-status-after.txt`, `hc/.work`, `.evidence`, `he-motion/.work`, `door-master/.work`), il test dell'alias, quello del collegamento, **i due test nuovi** | 200 dove si attende 404 |
| `alias` — via la tilde sulla stringa e il controllo del percorso reale; il punto sulla stringa resta, quindi soltanto un alias arriva a una cartella puntata | 7: `WORK~1/notes.txt`, `GIT-ST~1.TXT`, `he-motion/WORK~1/frames.html`, il test dell'alias, quello del collegamento, **i due test nuovi** | «('research/hero/he-motion', 'WORK~1') — assert (200 == 404)»; sul pacchetto vero «research/hero/he/SOURCE~1/8771-ar.html» sarebbe servito |
| `ext` — `.py` fra le estensioni servite | 6: `home/build.py`, `hd/build_hd.py` e **i quattro casi nuovi** (`probe_he_motion.py`, `he-21st/measure.py`, `build_specimen.py`, `_tools/build.py`) | 200 dove si attende 404 |
| `openpair` — la vista incornicia un file di prova servibile dato come `?pair=` | 1: `test_the_compare_view_answers_400_to_an_unknown_choice[pair=research/documents/index.html]` | «assert 200 == 400» |
| `atomic` — la vista perde il marchio `non_atomic_requests` | 2: `test_no_preview_view_asks_for_a_transaction`, `test_a_picker_and_a_proof_file_read_nothing` | «Expected to perform 0 queries but 8 were done» |
| `framable` — la vista incorniciabile da chiunque (`frame-ancestors *`, senza `X-Frame-Options`) | 1: `test_the_compare_view_frames_the_two_phones_of_mes_pieces_side_by_side` | «the compare view itself is framed by no one» |

La mutazione `alias` prova anche che, su questo volume, le metà alias dei due test nuovi vengono eseguite davvero (altrove no: HS-1).

### 1.6 Nel browser

Chromium headless, profilo proprio, un ascoltatore di `securitypolicyviolation` in ogni frame:

| Pagina | Finestra | Cornici: x, y, larghezza × altezza | Larghezza della pagina incorniciata | Scorrimento (la sinistra a 500) | Stato disegnato | Traboccamento | Violazioni CSP · errori · richieste fallite |
|---|---|---|---|---|---|---|---|
| confronto fr | 1440 × 900 | (312, 169) e (736, 169), 392 × 715 | 390 px | 500 · 0 | 2 su 2 | 0 | 0 · 0 · 0 |
| confronto ar | 1440 × 900 | (312, 201) e (736, 201), 392 × 683 | 390 px | 500 · 0 | 2 su 2 | 0 | 0 · 0 · 0 |
| confronto fr | 390 × 844 | (16, 161) e (16, 860), 358 × 579, una sotto l'altra | 356 px | 500 · 0 | 2 su 2 | 0 | 0 · 0 · 0 |
| confronto ar | 390 × 844 | (16, 213) e (16, 912), 358 × 579 | 356 px | 500 · 0 | 2 su 2 | 0 | 0 · 0 · 0 |

Ogni cornice mostra esattamente il file della tabella (`location.pathname`).

- **Chi può incorniciare che cosa.** Nell'hub — stessa origine, la policy del sito, dove `frame-src` ricade su `default-src 'self'` — ho inserito due iframe. La vista di confronto: rifiutata dal browser, «Framing 'http://127.0.0.1:8785/' violates the following Content Security Policy directive: "frame-ancestors 'none'". The request has been blocked.», documento vuoto. Una pagina di prova (`documents/index.html`): caricata, per il suo `frame-ancestors 'self'`.
- **Le 27 pagine che il commit porta sull'hub** (`pages.py`: i link del gruppo di H-E e dei cinque gruppi della terza ondata, letti dall'hub stesso — file di prova, le quattro voci di H-E nel selettore, le due del confronto): 27 × 200, **0 violazioni CSP**, 0 errori in console, 0 richieste fallite, 0 risposte ≥ 400.
- **L'hub** sul pacchetto vero: 27 gruppi, 154 link (125 file di prova, 23 voci dei selettori, 2 del confronto, 4 pagine dal vivo), **nessun «manca»**; ogni link 200, tranne `/fr/espace-reserve/` (302 verso l'accesso, come in W1); ogni link dell'anteprima sigillato.

### 1.7 Le pagine normali

`/fr/`, `/ar/`, `/fr/compte/login/` sul mio server, con il flag: 11 direttive, 221 byte, nessun `frame-src`, `frame-ancestors 'none'`, `DENY`, nessun `X-Robots-Tag` — le stesse direttive e la stessa lunghezza che W1 e W2 hanno misurato; `test_the_production_policy_of_a_normal_page_is_unchanged` passa. Il commit non tocca né `config/` né un middleware.

---

## 2. Rilievi

### Bloccanti — nessuno

### Maggiori — nessuno

### HS-1 — MINORE · le metà «alias 8.3» dei due test nuovi passano in silenzio dove il volume non dà alias

**Fatto.** `test_no_new_entry_reaches_a_dotted_or_short_name_folder` (`tests/frontend/test_design_preview.py`, righe 1436–1437) e `test_beside_the_new_entries_the_real_package_s_working_folders_stay_closed` (righe 3334–3335) guardano l'alias soltanto `if alias:`, e `_alias` (riga 1370) risponde `""` fuori da Windows o dove `GetShortPathNameW` non dà un nome corto. Su un volume senza nomi 8.3 i due test passano senza aver guardato un alias, e «nessuno saltato» resterebbe vero. Il test più vecchio sullo stesso tema, `test_proof_refuses_a_dotted_folder_through_its_short_name_alias`, lo dice con uno skip esplicito («this volume does not generate 8.3 names»). Su questa macchina la metà alias gira davvero: la mutazione `alias` fa cadere entrambi (§1.5).

**Correzione.** In ciascuno dei due test portare la metà alias in un test proprio che passi da `_short_name` (che già fa `pytest.skip` quando il volume non dà alias), oppure contare gli alias controllati e chiamare `pytest.skip("this volume does not generate 8.3 names: the alias half was not checked")` quando sono zero — in un test separato dalla metà per nome, perché uno skip a metà nasconderebbe anche quella. In `test_beside_…`, su Windows, almeno un alias controllato.

### HS-2 — MINORE · la tabella dei confronti non ha un invariante sulle lingue: una chiave mancante è un 500 (oggi non raggiungibile)

**Fatto.** `compare_files()` (`apps/designpreview/services.py`, riga 772) e `compare_view()` (riga 790) leggono `side.files[lang]`, e le opzioni della lingua chiamano `compare_files` per **tutte** le lingue a ogni richiesta. Se un confronto della tabella non nomina una pagina per ogni lingua di `LANGS`, ogni richiesta di quel confronto — anche nella lingua che c'è — e l'hub, se ne collega la lingua mancante, rispondono 500 (`KeyError`) invece della frase «questa combinazione non esiste» che i selettori danno per i loro buchi. Verificato in memoria (`latent.py`, nulla scritto): un confronto il cui secondo lato ha soltanto il francese → `KeyError 'ar'` per `lang=fr`, per `lang=ar` e per la voce dell'hub. Oggi K5 ha le due lingue sui due lati e nessuna richiesta lo provoca; ma la docstring di `compare_view` promette che nessun valore porta altrove, e un valore noto porterebbe a un 500.

**Correzione.** Una riga di test che fissi l'invariante — `assert all(set(side.files) == set(services.LANGS) for comparison in services.COMPARISONS.values() for side in comparison.sides)` — oppure, se un confronto potrà avere una lingua sola, `side.files.get(lang, "")` e il ramo dei selettori per ciò che non esiste: la lingua barrata, nessuna cornice, la frase, 200.

### HS-3 — MINORE · quattro testi dicono ancora «in costruzione» o «frame.html» soltanto

**Fatto.** `IN_CONSTRUCTION` è vuoto e la nota lo dice, ma:

1. `apps/designpreview/services.py`, righe 430–432, il commento sopra `"he"` in `HERO_VARIANTS`: «Announced before they are built (IN_CONSTRUCTION): until a file is in the proof directory its choice is struck through…»;
2. `tests/frontend/test_design_preview.py`, riga 396: «(H-E, the sixth, is in construction: its own test, below.)»;
3. stesso file, riga 1615, messaggio di un'asserzione: «H-E and its concepts are in construction; …» — nel pacchetto finto sono barrati perché assenti, non perché in costruzione;
4. `templates/dev/designpreview/bar_group.html`, righe 2 e 4: «one group of choices in a picker's bar (frame.html)», «as designpreview.services._frame builds it» — ora lo include anche `compare.html`, con il gruppo della lingua costruito da `services.compare_view`.

È la classe del rilievo W2-5: nessun effetto sul comportamento.

**Correzione.** 1: «H-E and its three concept frames: until a file is in the proof directory its choice is struck through…», senza `IN_CONSTRUCTION`; 2: «(H-E, the sixth, has its own test, below.)»; 3: «H-E and its concepts are absent from the fake package; …»; 4: «(frame.html, compare.html)» e «as services._frame or services.compare_view builds it».

---

## 3. Osservazioni (nessuna azione su questo commit)

- **O1 — la nota fuori dalla riga scritta.** `docs/design-v5/QA/PREVIEW_HUB_CATCHUP.md` non è fra i percorsi della riga del Preview Engineer in `AGENT_OWNERSHIP.md`. Lo stesso valeva per `PREVIEW_OUTAGE_2026-10-02.md` (`da75812`), che la revisione W2 ha contato nella riga di proprietà, e questa revisione andrà nella stessa cartella con il commit del correttore. Nessun nome in comune con `qa-v5` (che ha `HERO_COUNCIL_REVIEW.md`, `PERF_FIRST_RENDER.md`, `hero-council/`). Per l'orchestratore: scrivere `docs/design-v5/QA/PREVIEW_*.md` nella riga, perché regola e pratica dicano la stessa cosa.
- **O2 — le cartelle delle corsie con il trattino basso** (`research/documents/_previews`, `_tools`, `_uiux`, `research/journey/_scratch`). Come scrive la nota dell'ingegnere, pagine, immagini, JSON e note vi sono servibili, gli script no (per estensione), e l'hub non le collega. I valori delle quattro chiavi dell'ambiente non sono in alcun file di testo della cartella delle prove; le parole come «password» o «secret» nelle cartelle nuove sono testi di linee guida UX. Solo loopback, solo sviluppo; una regola in più sul resolver resta una decisione dell'orchestratore.
- **O3 — `%00` → 500**, preesistente: `DataError` in `cms/middleware.py:75`, nessun frame dell'anteprima nella traccia; l'O2 di W1 e W2, invariato, non di questo commit.
- **O4 — i denti contro una cornice aperta stanno su un caso.** La mutazione `openpair` cade su un solo caso parametrizzato (`pair=research/documents/index.html`); i tre valori di `test_no_new_entry_…` sono percorsi puntati, che una regressione «accetta un file servibile» rifiuterebbe comunque. Più robusta un'asserzione di proprietà: in ogni risposta della vista, ogni `src` sta in `compare_files()` — sui nove casi del 400 e su un paio di file servibili dati come `pair`.
- **O5 — cornici della stessa origine, senza `sandbox`.** È il modello dei selettori dal primo giorno: le pagine di prova eseguono i propri script, sotto `script-src 'self'`, sull'origine dell'intero sito di sviluppo. Il confronto non lo cambia.
- **O6 — i rifiuti senza sigilli.** 403 del CSRF, 405, 404 sono risposte di Django: non portano `X-Robots-Tag` né `Cache-Control`, e nulla dell'anteprima. La docstring di `apps/designpreview/__init__.py` nomina il 404 e il 405, non il 403. Invariato dalle revisioni precedenti.

---

## 4. Limiti di questa revisione

- Soltanto Chromium headless; nessun Firefox, nessun Safari.
- 8770–8772 e 8780 non sono stati interrogati, per regola: «la CSP di produzione non cambia» poggia sul test in processo, su `config/` invariato e sulla misura del mio server (11 direttive, 221 byte, come in W1 e W2), non su un confronto al byte con `main` a seme di hash fisso.
- Soltanto `tests/frontend/test_design_preview.py` e i sottoinsiemi delle mutazioni; non la suite intera.
- Il rifiuto di un chiamante che non è il loopback è provato soltanto dai test: il mio server ascolta su `127.0.0.1`.
- Le prove sugli alias 8.3 valgono per il volume `C:`, che genera nomi corti.
- Nelle cartelle con il trattino basso ho cercato i valori delle chiavi dell'ambiente e alcune parole nei file di testo, non dati personali in immagini o catture.
- Sei regressioni plausibili, non tutte le combinazioni delle guardie.
- Neutralità delle parole, disegno, movimento, accessibilità: altre lenti, non giudicate qui oltre a ciò che i test dicono.

---

## 5. Ciò che la revisione conferma

- Il commit sta nella riga dell'ingegnere per tutto il codice; `config/`, il middleware del tetto e `_preview_only` non cambiano; LF; `ruff` pulito; nessun segreto.
- Il resolver delle prove è lo stesso al byte e i suoi test ci sono tutti, con otto rifiuti in più; sul pacchetto vero, nelle cartelle nuove, 65 richieste ostili → 65 × 404.
- La vista di confronto incornicia soltanto le pagine della sua tabella: 27 query ostili su 30 → 400 senza iframe, le altre 3 → le pagine della tabella; aggiunge `frame-src 'self'` e nient'altro; non si lascia incorniciare (il browser lo rifiuta); ogni sua risposta 200, 400 e `HEAD` è sigillata.
- Non apre transazioni e non legge il database: 200 richieste → 0 connessioni; con l'hub, picco 8 e 0 dopo, due volte.
- I test sono 159, passano senza un salto, e cadono quando devono: sei mutazioni, sei cadute.

**Verdetto: PASS_WITH_FIXES.** Nulla impedisce di riavviare 8780 su `37bf897`. HS-1, HS-2 e HS-3 sono test e testi, senza effetto sul servizio: da chiudere nel commit del correttore.
