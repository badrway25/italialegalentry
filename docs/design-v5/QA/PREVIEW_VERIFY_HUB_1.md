# Verifica indipendente delle correzioni dell'hub — commit `8602220`

| | |
|---|---|
| **Oggetto** | `design-v5: preview — hub catch-up, review fixes round 1 (HC-1 … HC-8, HS-1 … HS-3)` — commit `8602220` su `design-v5` (genitore `37bf897`), 8 file, +877 −95. Da verificare: HC-1 … HC-8 di `PREVIEW_REVIEW_HUB_CATALOGUE.md`, HS-1 … HS-3 di `PREVIEW_REVIEW_HUB_SERVING.md`; poi le regressioni nell'hub, nei selettori, nella cornice e nel confronto |
| **Ruolo** | Verificatore indipendente, etichetta `hub-verify-1`: non ha costruito né rivisto nulla dell'anteprima |
| **Data** | 4 ottobre 2026, 19:44–20:30 (ora locale) |
| **Verdetto** | **PASS** — gli undici rilievi sono **chiusi**, il maggiore e i dieci minori; nessuna regressione trovata; nessun rilievo nuovo. Sette osservazioni, nessuna chiede un'azione su questo commit |
| **Strumenti** | server proprio della worktree su `127.0.0.1:8786` (`DB_CONN_MAX_AGE=0`, `DATABASE_URL=…/ile_v5`, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, `PGAPPNAME=ile-design-preview-hv1`, `runserver --noreload`), avviato una volta alle 20:01 e spento alle 20:13 con il suo albero di due processi (porta chiusa, nessun processo rimasto, 0 connessioni dopo); richieste grezze `http.client`, un socket ciascuna, il percorso spedito com'è scritto; censimento con una sessione psycopg in autocommit (`application_name = hv1-census`) letta ogni 40 ms; Playwright 1.63.0 headless (Chromium), profilo proprio `C:/tmp/ile_v5_council/.profiles/hub-verify-1/`; corsia `ile_lane5` / `test_ile_lane5`, senza connessioni prima di ogni esecuzione; Python 3.13, Django 5.2.17, pytest 9.0.3, ruff 0.16.8 |
| **Lucchetto** | `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` atteso in codice (`gate.py`: controllo ogni 15 s finché il file esiste) all'inizio, prima di `ruff`, di ciascuna delle dieci esecuzioni di test (una completa, otto mutazioni, una simulazione), dell'avvio del server, di ciascuna delle cinque raffiche e della sessione del browser: 19 attese, tutte di 0 s (`gate.log`) |
| **Prove** | fuori dal repository, `C:/tmp/ile_v5_council/.work/hub-verify-1/` (copia della cartella di lavoro della sessione): `gate.py`, `gate.log`; `srv.py`, `srv8786-probe.log`; `run_pytest.sh`, `lane5_busy.py`, `lane5-full.log`; `hv1_mutate.py`, `run_mutations.sh`, `mut-*.log`; `hv1_noalias.py`, `noalias.log`; `probe.py` → `probe.json` e `hub.html`; `traversal.py` → `traversal.json`; `aliases.py`; `burst.py` → `burst.json`; `look.py` → `look.json`; `shots/*.png` (64) |

Non ho fermato, riavviato né interrogato il server ufficiale su 8780 né i server 8770, 8771 e 8772: stessi processi all'inizio (19:46) e alla fine (20:13), 22340, 3520, 7032, 27536. Non ho usato il Chrome del proprietario (9223, processo 27532); quello di QA (9222) non era acceso. Nessun comando git che scrive; la cartella delle prove è stata soltanto letta; nella worktree nessun file è stato toccato prima di questa nota (mutazioni in memoria, caricate da fuori; `ruff --no-cache`, `pytest -p no:cacheprovider`, `PYTHONDONTWRITEBYTECODE=1`). Niente di ciò che segue è una decisione di design.

---

## 0. In breve

| Rilievo | Stato | In una riga | § |
|---|---|---|---|
| **HC-1** (maggiore) | **chiuso** | sei link «palco», uno per primaria e per lingua; la riga dice del parametro; ciascun link disegna la primaria che nomina (`t0` → `bench-t0`, `a` → `cta-a`, `b` → `cta-b`), in fr e in ar, a 1440 e a 390; un test sul pacchetto vero lega `bench.js` ai link | 1.1 |
| HC-2 | chiuso | «prima … poi», nessun «sinistra» né «destra»; misurato a otto larghezze in due lingue; la riga K5 e la nota delle larghezze dicono «fino a 390 px» e le due disposizioni, vere a ogni misura | 1.2 |
| HC-3 | chiuso | «i quattro pubblici», «i momenti su misura», «una linea in piano»; «udienz», «momenti propri», «linea di livello» assenti dall'hub reso | 1.3 |
| HC-4 | chiuso | stock (Pexels), provvisorie fino a O54/O55 e O81, un'alternativa trattenuta per O55: vero contro la pagina e le fonti | 1.4 |
| HC-5 | chiuso | un fatto («il cui movimento ha un verso»), «marchio» una volta; vero contro `LOADER_SIGNATURE.md` | 1.5 |
| HC-6 | chiuso | «In arrivo» nomina il registro del fascicolo di «La soglia» V5.2, che sta sopra (gruppo 22) | 1.6 |
| HC-7 | chiuso | link alla pagina di verifica: 200, sigilli, 0 violazioni CSP, nessun traboccamento; le porte A e B si vedono | 1.7 |
| HC-8 | chiuso | il commento sopra H-E non nomina più `IN_CONSTRUCTION`; le due menzioni rimaste sono attuali | 1.8 |
| HS-1 | chiuso | le metà alias sono test a sé; su questo volume girano (la mutazione `alias` le fa cadere); con un volume senza nomi 8.3, simulato, si saltano con il motivo | 1.9 |
| HS-2 | chiuso | un test tiene l'invariante delle lingue; un lato senza la pagina araba lo fa cadere | 1.10 |
| HS-3 | chiuso | i quattro testi sono attuali, e tre della stessa classe in più | 1.11 |
| Guardie | intatte | il resolver è identico al byte a `e10002f`; 137 percorsi ostili e 14 traversate e unità (12 verso un file vero fuori dalla radice) → 151 × 404, nessun contenuto nei corpi | 2.2 |
| Tetto | tiene | cinque raffiche 200 × 32: file di prova e confronto 0 connessioni; con l'hub picco 3 (tetto 8); 0 a +1 s e a +10 s; 0 a riposo | 2.4 |
| Test | verdi | 163 passati in 50,43 s, nessuno saltato; otto mutazioni, otto cadute | 2.5 |
| Regressioni | nessuna | hub: 27 gruppi, 159 link, nessun «manca»; selettori, cornice, confronto e 32 pagine collegate: 0 violazioni CSP, 0 errori, 0 traboccamenti | 3 |

---

## 1. I rilievi, uno per uno

### 1.1 HC-1 (maggiore) — chiuso

**Il rilievo.** «palco · fr» e «palco · ar» aprivano `stage.html` e `stage-ar.html` senza query; `bench.js` sceglie la primaria da `?cta=t0|a|b`, e senza query vale `t0`: il posto mostrava soltanto T0.

**Ora.** Gruppo H-E, riga «Le due CTA sul loro banco»: otto link — «stati · fr», «stati · ar» e sei «palco», uno per primaria e per lingua, con la query nell'etichetta (`palco · fr · T0 · ?cta=t0`, `palco · fr · CTA-A · ?cta=a`, `palco · fr · CTA-B · ?cta=b`, e gli stessi per `stage-ar.html`). La riga dice: «… e un primo schermo di sostituzione, il palco. Sul palco una CTA alla volta: il parametro cta sceglie T0, CTA-A o CTA-B. È un banco di prova, non un eroe e non una proposta: i suoi numeri vanno ripresi su H-E.»

**Prova.**

* `bench.js` sul pacchetto vero: `const CLASS = { t0: "bench-t0", a: "cta-a", b: "cta-b" }` e `get("cta") || "t0"`. I tre valori dei link sono esattamente quelli che lo script conosce.
* In Chromium, aprendo gli `href` letti dall'hub stesso: 12 caricamenti su 12 (sei link, a 1440 × 900 e a 390 × 844) con `data-cta` e la classe della primaria uguali al link — `t0` → `btn btn--primary bench-t0`, `a` → `btn btn--primary cta-a`, `b` → `btn btn--primary cta-b`; `dir="ltr"` in fr, `dir="rtl"` in ar; 200 con i sigilli; 0 violazioni CSP, 0 errori in console, 0 richieste fallite, nessun traboccamento.
* Guardato: `stage-contact-1440.png` mette le sei CTA ingrandite una sotto l'altra. T0 ha il filo d'oro statico; CTA-A l'intarsio d'oro e l'ombra; CTA-B il filo chiaro e l'ombra, senza oro; in arabo sono specchiate, con la freccia verso sinistra. Tre primarie diverse, ciascuna dove il link la nomina. A 390, `stage-stage-ar-html-cta-a-390.png`: l'intarsio a tutta larghezza, sotto la porta.
* La riga sull'hub (`hub-1440-row-cta.png`, `hub-390-row-cta.png`): otto link su 4 righe a 1440 e su 7 a 390, tutti dentro la finestra; la pagina non trabocca.
* Test: `test_h_e_says_where_it_stands_and_each_measurement_page_what_it_is_not` (i tre link francesi con la loro query, nessun link nudo, i tre arabi «manca» nel pacchetto finto) e il nuovo `test_the_cta_rig_still_reads_the_primary_the_hub_s_links_name`, sul pacchetto vero. Mutazioni mie: i due link nudi di `37bf897` → 3 test cadono; via i due link CTA-B → 2.

Il palco in sé non dice quale CTA mostra: lo dice l'etichetta del link, come chiedeva la correzione del revisore. **Chiuso.**

### 1.2 HC-2 — chiuso

**Il rilievo.** Fra 48 e 54 rem la nota della barra diceva «l'una accanto all'altra … a sinistra … a destra» mentre le cornici stavano una sotto l'altra; la riga K5 diceva «390 px», falso sotto 424 px di finestra.

**Ora.** La barra del confronto: «Le due pagine a 390 px, ciascuna con il suo scorrimento; in ordine d'arrivo — prima la seconda ondata, poi la terza ondata — e non di preferenza: decide il proprietario.» Nella pagina non c'è «sinistra» né «destra». La riga K5: «… Alla stessa larghezza: 390 px, affiancate, da 864 px di finestra; sotto, una sotto l'altra, larghe quanto la finestra permette, fino a 390 px.» La nota delle larghezze dell'hub: «il confronto disegna i suoi due telefoni fino a 390 px, affiancati da 864 px di finestra e l'uno sotto l'altro in una più stretta».

**Prova** (Chromium, `compare-{fr,ar}-*.png`; le stesse cifre in fr e in ar):

| Finestra | Disposizione | Pagina in ogni cornice | Nota della barra | Stato nelle didascalie | Traboccamento · CSP · errori |
|---|---|---|---|---|---|
| 1440 × 900 | affiancate (x 312 e 736) | 390 px | disegnata | 2 su 2 | 0 · 0 · 0 |
| 864 × 900 | affiancate (x 24 e 448) | 390 px | disegnata | 2 su 2 | 0 · 0 · 0 |
| 863 × 900 | una sotto l'altra | 390 px | disegnata, vera | 2 su 2 | 0 · 0 · 0 |
| 800 × 900 | una sotto l'altra | 390 px | disegnata, vera | 2 su 2 | 0 · 0 · 0 |
| 600 × 900 e 424 × 900 | una sotto l'altra | 390 px | nascosta sotto 48 rem, come nei selettori | 2 su 2 | 0 · 0 · 0 |
| 423 × 900 | una sotto l'altra | 389 px | nascosta | 2 su 2 | 0 · 0 · 0 |
| 390 × 844 | una sotto l'altra | 356 px | nascosta | 2 su 2 | 0 · 0 · 0 |

* «Prima» è la cornice di sinistra da 54 rem e quella in alto sotto; la pagina è `dir="ltr"`, e la prima è sempre «seconda ondata».
* A 1440 la rotella sulla prima cornice la porta a 600 px e lascia l'altra a 0. I tasti `r` e `f` portano a `lang=ar` e a `lang=fr`.
* Guardati `compare-fr-800x900.png` (due cornici una sotto l'altra, sotto la frase «prima … poi»), `compare-fr-863x900.png`, `compare-ar-1440x900.png`, `compare-ar-390x844.png`.
* La riga K5 e la nota delle larghezze sono vere a ogni misura della tabella.
* Test: la frase nuova, nessun «sinistra» né «destra», il test nel browser che misura anche 800 × 900. Mutazione mia (la frase di `37bf897`) → 2 test cadono.

**Chiuso.**

### 1.3 HC-3 — chiuso

Sull'hub reso (`hub.html`; `hub-1440-g-research-icons.png`, `hub-1440-g-research-journey.png`): l'introduzione del gruppo 24 dice «… i quasi gemelli, i quattro pubblici, i glifi da sostituire»; la riga «La tavola semantica» «I quattro pubblici, i domini, …, i momenti su misura, …»; il gruppo 22 «una linea in piano». Nell'intero testo dell'hub «udienz», «momenti propri» e «linea di livello» non compaiono. Test: le parole nuove ci sono, «udienz» e «linea di livello» no. Mutazione mia («le quattro udienze» rimesse) → 1 test cade. **Chiuso.**

### 1.4 HC-4 — chiuso

La riga «La fila, quattro volte»: «Mostra fotografie stock (Pexels), provvisorie finché il proprietario non risponde a O54 e O55 e non decide O81; fra le alternative, una è trattenuta per O55. È una pagina soltanto locale, da non pubblicare.» L'ho confrontata con le fonti:

* la fascia di `doors.html`: «Every photograph is PROVISIONAL until O54 and O55 are ruled and the context is adopted. Pexels License»;
* la riga C delle alternative contiene Pexels 35699765, che `IMAGE_ART_DIRECTION.md` (ramo `design-research-v5`, r. 173 e 449) segna «held — O55 ruling pending»; nessun'altra fotografia della pagina è fra le quattro trattenute della nota d'igiene (r. 60);
* O81 è «the photographs (Q1–Q10)» in `DECISION_LOG.md` A20.

Ogni parte della riga regge. Test aggiornato; mutazione mia (la riga di `37bf897`) → 1 test cade. **Chiuso.**

### 1.5 HC-5 — chiuso

La riga «Passo»: «… Il solo il cui movimento ha un verso — corre nel senso della lettura e in arabo si specchia — e il solo che esce dal marchio: gli serve spazio accanto.» È un fatto, non un merito. `LOADER_SIGNATURE.md` dice «brisk, horizontal, directional» (r. 32) e che in RTL il filo corre verso sinistra mentre il marchio non si specchia (r. 214); la frase dice infatti che si specchia il movimento, non il marchio. «marchio» compare una volta. Lette insieme, le tre righe dei candidati dicono ciascuna il suo movimento e un fatto o un vincolo, nell'ordine A/B/C delle parole del brief («porta / luce / percorso»). Il test della neutralità passa. **Chiuso.** Sullo stile, l'osservazione O6.

### 1.6 HC-6 — chiuso

«In arrivo», riga «Fascicolo»: «Per ora esistono soltanto campioni di ricerca: la tipografia, la navigazione e il registro del percorso nel fascicolo («La soglia» V5.2), qui sopra.» Il gruppo 22 (che elenca «il passaggio pubblico, il binario del cruscotto, il fascicolo e il formato compatto») sta prima del gruppo 27. «Nessuna ha ancora una maquette», nell'introduzione del gruppo, resta vero: sono campioni di ricerca. Guardato `hub-1440-g-upcoming.png`. **Chiuso.**

### 1.7 HC-7 — chiuso

La riga «La porta dal suo master» ha due link, «frammento» e «verifica · oggi e il frammento» → `research/hero/door-master/check/door-snippet.html`, e la frase «La pagina di verifica mette la porta di oggi accanto a quella del frammento, così com'è scritto: una verifica, non una maquette.»

* La pagina di verifica risponde 200 con i sigilli, `text/html`; 0 violazioni CSP, 0 errori, nessun traboccamento a 1440 né a 390 (alta 900 e 1 015 px).
* Guardate `door-door-snippet-1440.png` e `door-door-snippet-390.png`: la porta A, «today: SVG image, doorway-arch-400.webp», accanto alla porta B, «the snippet as written», e la riga della pagina «not a comp, not a design proposal».
* Il frammento da solo trabocca di 18 px a 390, come la riga dice.
* Mutazione mia (link tolto) → 3 test cadono.

**Chiuso.**

### 1.8 HC-8 — chiuso

`services.py`, r. 430–435: «They were announced before they were built, until their files reached the disk on 4 October 2026; the currency test now holds those files like every other catalogued file. …» — senza `IN_CONSTRUCTION`. Le sole menzioni rimaste, la docstring del modulo (r. 15–16) e il commento della costante (r. 460–465), dicono che oggi nulla è annunciato prima di essere costruito, e `IN_CONSTRUCTION = ()`: sono attuali. **Chiuso.**

### 1.9 HS-1 — chiuso

La metà alias di ciascun test è ora un test a sé:

* `test_no_new_entry_reaches_a_dotted_folder_through_its_short_name_alias`, sul pacchetto finto: passa da `_short_name` e dichiara lo skip se il volume non dà alias;
* `test_beside_the_new_entries_the_real_package_s_working_folders_stay_closed_through_their_short_names`, sul pacchetto vero: skip fuori da Windows; chiede al volume se genera nomi 8.3 su `door-master`, una cartella dal nome lungo (qui `DOOR-M~1`); se sì, almeno un alias dev'essere controllato.

Le metà per nome restano nei due test di prima. Prove:

* **Su questo volume girano.** La mia mutazione `alias` (via la tilde sulla stringa e il controllo del percorso reale) fa cadere le due metà alias nuove, il test alias più vecchio, tre casi alias di `test_proof_refuses_what_it_must_with_a_404` e il test dei collegamenti: 7 in tutto, gli stessi della revisione del servizio.
* **Su un volume senza nomi 8.3, simulato** (`hv1_noalias.py`: in memoria `_alias` risponde "" e `_short_name` il nome lungo): **3 saltati con il motivo** — «this volume does not generate 8.3 names: the alias half was not checked», due volte, e «this volume does not generate 8.3 names» per il test più vecchio — e 3 passati, le metà per nome. Nessun passaggio in silenzio.

**Chiuso.**

### 1.10 HS-2 — chiuso

`test_every_side_of_a_comparison_names_a_page_in_every_language` vuole, per ogni confronto e ogni lato, `set(side.files) == set(LANGS)`; il commento di `Side.files` lo dice. Mutazione mia (il secondo lato senza la pagina araba): il test cade, con altri 17 che incontrano il 500 (`KeyError: 'ar'`, 68 righe nel registro). È la prima delle due correzioni proposte dal revisore; il ramo di codice non è cambiato (O7). **Chiuso.**

### 1.11 HS-3 — chiuso

1. il commento sopra `"he"`: vedi HC-8;
2. il commento del test dell'hub, r. 399: «(H-E, the sixth, has its own test, below.)»;
3. il messaggio d'asserzione: «H-E and its concepts are absent from the fake package; …»;
4. `bar_group.html`: «the bar of a picker or of the compare view (frame.html, compare.html)» e «as designpreview.services._frame or designpreview.services.compare_view builds it».

In più, della stessa classe: il commento del foglio sopra `.dp-frame-root`, la docstring del test della barra nel browser («on disk or not») e quella del modulo di test («Four tests look at the real directory»: contati, sono quattro). **Chiuso.** Due testi dello stesso genere restano: O1.

---

## 2. Guardie, tetto, test

### 2.1 Perimetro, fine riga, `ruff`, segreti

* Da `e10002f` a `8602220`, fuori dalla riga del Preview Engineer ci sono soltanto `docs/design-v5/QA/PREVIEW_HUB_CATCHUP.md` e i due rapporti di revisione (O3). `8602220` tocca `services.py`, `designpreview.css` (un commento), `bar_group.html` (un commento), `hub.html` (la nota delle larghezze) e il file di test. `config/`, `middleware.py`, `views.py`, `urls.py` e `__init__.py` non sono toccati; `middleware.py` è identico a `e10002f`.
* `git ls-files --eol`: `i/lf w/lf` per gli otto file; 0 byte CR nella worktree e nei blob; nessun BOM; `git diff --check 37bf897 8602220` pulito.
* `ruff check --no-cache` e `ruff format --check --no-cache` sui due file Python toccati e sull'app intera: «All checks passed!», «2 files already formatted», «6 files already formatted».
* Nessun URL esterno nelle righe aggiunte a codice, template e test; template senza attributi `style` né gestori inline, un solo `<script src>` per pagina; «password» e «token» nel diff stanno soltanto nella prosa dei rapporti.

### 2.2 Il resolver delle prove

* La sezione del resolver, da `PROOF_CONTENT_TYPES` a `proof_exists`, ha la stessa impronta SHA-256 in `e10002f`, `37bf897` e `8602220`.
* **137 richieste grezze → 137 × 404** (`probe.py`). Le famiglie:
  * le sette cartelle puntate accanto alle voci nuove (`he/.work`, `he/.source`, `concepts/e1–e3/.work`, `he-motion/.work`, `door-master/.work`) e tre della radice (`.work`, `.ecd`, `.vendor`), ciascuna su un file servibile che c'è davvero (99 bersagli su disco: il 404 è del resolver, non dell'assenza);
  * per nome, per alias 8.3 (`WORK~1`, `SOURCE~1`, `ECD~1`, `VENDOR~1`, in minuscolo, con `%7E`), con il punto codificato (`%2e`, `%2E`, `%252e`, il punto a larghezza piena `%EF%BC%8E`), con un punto o uno spazio finale;
  * script e registri per nome e per alias (`measure.py`, `MEASURE.PY`, `BUILD_~1.PY`, `LAYOUT~1.PY`, `perflog.ps1`, `PERFLOG.PS1`, `perf_run.log`, `PERF_RUN.LOG`) e suffissi (`.py.`, `.py%20`, `::$DATA`, `%3A%3A$DATA`, `.py/.html`, `STAGE-~1.HTM`);
  * unità, UNC, cartelle, dispositivi (`CON.html`, `NUL.css`), l'alias di una cartella non puntata (`DOOR-M~1`).
* Il controllo «nessun contenuto nel corpo» ha segnalato dieci di questi 404, a torto: cercava `SIGNING`, che la pagina 404 di `DEBUG` ripete con il percorso chiesto, e il bersaglio era sbagliato (`SIGNING_SHEET.md` sta dentro la radice). Rifatte con un file vero fuori dalla radice (`council/ICON_SEMANTIC_MAP.md`) e con cinque sue righe come aghi (`traversal.py`): **14 traversate e unità → 14 × 404, 0 righe nei corpi** — dodici verso quel file (`..%2f` a uno e a due livelli, `%2e%2e/`, `..%5c`, `%5c..%5c`, `....//`, `research/../../`, `research/%2e%2e/%2e%2e/`, `research/hero/..%2f..%2f..%2f`, l'unità `C:/` e `C%3A/`, l'UNC), due verso `SIGNING_SHEET.md` attraverso `..`. Il controllo, `SIGNING_SHEET.md` chiesto per il suo nome sotto la radice, risponde 200 con 5 righe su 5: il metodo vede il contenuto quando c'è.
* I test di guardia ci sono tutti e sono verdi: `test_proof_refuses_what_it_must_with_a_404`, il test dell'alias, quello dei collegamenti, le due metà per nome sulle cartelle nuove e le due metà alias.

### 2.3 La vista di confronto

* `compare/` senza query, `?pair=mes-pieces&lang=fr` e `&lang=ar` → 200, `X-Robots-Tag: noindex, nofollow`, `Cache-Control: no-store`, `X-Frame-Options: DENY`, CSP con `frame-src 'self'` e `frame-ancestors 'none'` (12 direttive, 239 byte); le cornici sono le quattro pagine della tabella.
* 15 query ostili (`pair=zz`, vuoto, `MES-PIECES`, `../.work`, `..%2F..%2F.work`, un file di prova servibile, un percorso puntato, `lang=.work`, `de`, `AR` e vuota, `<script>`, `C:/Windows/win.ini`, `//evil.example/x`, `mes-pieces%20`) → **15 × 400**, sigillate, senza iframe.

### 2.4 Il database: il tetto sotto una raffica 200 × 32

Server mio con `PGAPPNAME=ile-design-preview-hv1`; censimento ogni 40 ms (`burst.py`); un secondo di quiete prima di ogni cella; letture a +1 s e a +10 s; il lucchetto atteso prima di ogni cella.

| Raffica, 200 × 32 | Risposte | Tempo | Letture | Picco | +1 s | +10 s |
|---|---|---|---|---|---|---|
| file di prova: H-E, palco con query, banco, verifica, porta, i due «Mes pièces» | 200 × 200 | 1,03 s | 25 | **0** | 0 | 0 |
| solo confronto: fr, ar, senza query, un 400 | 150 × 200, 50 × 400 | 1,06 s | 26 | **0** | 0 | 0 |
| hub e confronto, metà e metà | 200 × 200 | 6,97 s (mediana 1,06 s, massimo 2,39 s) | 168 | **3** | 0 | 0 |
| di nuovo | 200 × 200 | 7,05 s | 170 | 3 | 0 | 0 |
| misto: hub, i due selettori, confronto, palco, un file mancante, `/fr/`, un foglio statico | 175 × 200, 25 × 404 | 3,50 s | 85 | 3 | 0 | 0 |

A riposo, prima di ogni cella e dopo tutte: 0. Dopo l'arresto del server: nessuna connessione client sull'intero PostgreSQL, a parte la mia lettura. Nel registro del server nessun 500 né 503 (3 310 × 200, 65 × 400, 176 × 404). Il picco è letto a campione; che non superi 8 lo dicono il semaforo e il suo test, `test_no_more_connections_than_the_ceiling_whatever_arrives`, verde nell'esecuzione completa.

### 2.5 I test

```
DATABASE_URL=…/ile_lane5  TEST_DATABASE_URL=…/ile_lane5   (→ test_ile_lane5; nessuna connessione prima)
.venv/Scripts/python -m pytest tests/frontend/test_design_preview.py --ds=config.settings.test -q -p no:randomly -p no:cacheprovider -rfEsxX
→ 163 passed in 50.43s
```

Nessuno saltato, compresi i tre test nel browser, le metà alias e i quattro test sul pacchetto vero.

**I denti.** `hv1_mutate.py` è un plugin pytest caricato da fuori della worktree (`-p hv1_mutate`): riscrive in memoria, per una sola esecuzione, `services.py` (ogni sostituzione verificata a una sola occorrenza, poi `exec` nel modulo); nessun file della worktree è toccato. Le esecuzioni coprono i 152 test che non sono né nel browser né raffiche (11 deselezionati); `left-right` copre i 13 test del confronto, browser compreso.

| Mutazione | Test che cadono |
|---|---|
| `stage-bare` — i due «palco» nudi di `37bf897` | 3: `test_the_hub_never_links_what_is_not_on_disk`, `test_h_e_says_…`, `test_the_cta_rig_still_reads_…` |
| `stage-no-b` — via i due link CTA-B | 2: `test_h_e_says_…`, `test_the_cta_rig_still_reads_…` |
| `no-check` — via il link alla pagina di verifica | 3: `test_h_e_says_…`, `test_no_new_entry_reaches_a_dotted_folder` (24 percorsi), `test_the_catalogue_names_every_file_…` |
| `left-right` — la frase dell'ordine di `37bf897` | 2: `test_the_compare_view_frames_…`, `test_a_browser_draws_the_two_phones_…` |
| `udienze` — «le quattro udienze» rimesse | 1: `test_the_hub_shows_the_third_wave_…` |
| `doors-old` — la riga delle porte di `37bf897` | 1: lo stesso |
| `side-fr-only` — un lato senza la pagina araba | 18, fra cui `test_every_side_of_a_comparison_names_a_page_in_every_language`; negli altri il 500 (`KeyError: 'ar'`) |
| `alias` — via la tilde sulla stringa e il controllo del percorso reale | 7: tre casi alias del test dei 404, il test dell'alias, quello dei collegamenti, le due metà alias nuove |
| simulazione: un volume senza nomi 8.3 | nessuna caduta: 3 saltati con il motivo, 3 passati (§1.9) |

### 2.6 Le pagine normali

`/fr/`, `/ar/` e `/fr/compte/login/` sul mio server, con il flag: 11 direttive, 221 byte, nessun `frame-src`, `X-Frame-Options: DENY`, nessun `X-Robots-Tag` — le cifre di W1, W2 e delle due revisioni di `37bf897`. L'hub: 11 direttive, 221 byte, sigillato.

---

## 3. Le regressioni cercate

* **L'hub, sul pacchetto vero.**
  * Risponde 200, sigillato, con 27 gruppi. Nel markup ci sono 16 etichette «prototipo di ricerca — non approvato»; le etichette disegnate sono 17, con quella del controllo.
  * I link sono 159: 130 file di prova, 23 voci dei selettori, 2 del confronto, 4 pagine dal vivo. Rispondono tutti 200 con i sigilli, tranne `/fr/espace-reserve/` (302 verso l'accesso, come in W1). **Nessun «manca».**
  * A 1440 × 900 e a 390 × 844: nessun traboccamento orizzontale, 0 violazioni CSP, 0 errori in console, 0 richieste fallite.
* **Le parole, sull'intero testo dell'hub.**
  * «raccomand» compare una volta: è il verdetto del gate 0 su H-B, circoscritto, tenuto da W1, W2 e dalla revisione del catalogo (O4).
  * «vincit» una volta, in «non impone un vincitore»; «superiore» una volta, in «la barra superiore».
  * «il solo» tre volte, sempre per un fatto: Mandata non chiede di cambiare una regola; il movimento di Passo ha un verso, e Passo esce dal marchio.
  * «più forte», «migliore», «preferit», «il più» e «il meno» non compaiono.
  * Lo stato di H-E, «la sua revisione indipendente non è conclusa», è ancora vero: nella worktree `qa-v5` ci sono i pareri dei seggi, non il verbale.
* **I selettori e la cornice** (`frame.html`).
  * Gli stati provati: i nove primi schermi in fr, fase 3; H-E ed E1 in ar; H-0 nell'intérim; quattro stati del selettore tipografico. Ciascuno a 1440 e a 390: 32 caricamenti, tutti 200, con 0 violazioni CSP, 0 errori e nessun traboccamento.
  * In ciascuno la barra disegna lo stato: «prototipo di ricerca — non approvato», «non approvato» a 390, «controllo — non una proposta» per V4.
  * Le combinazioni che non esistono lo dicono («questa combinazione non esiste», «combinazione inesistente»), senza cornice.
  * Guardate `picker-hero-variant-he-lang-fr-phase-3-1440.png` e `picker-hero-variant-e1-lang-ar-phase-3-390.png`.
* **Il confronto**: le sedici misure del §1.2.
* **Le pagine collegate dai gruppi H-E e della terza ondata**: 32, caricate una per una a 1440. Tutte 200, con 0 violazioni CSP, 0 errori, 0 richieste fallite e nessuna risposta ≥ 400.
* **Le schermate guardate** (64, in `shots/`):
  * a 1440 e a 390, le righe e i gruppi che le correzioni toccano: H-E, la riga delle CTA, la porta dal master, le icone, «La soglia», la fila delle porte, «Passo», «In arrivo», «Mes pièces» con K5, la nota delle larghezze;
  * i sei palchi a 1440 e a 390, con il loro foglio ingrandito;
  * la pagina di verifica e il frammento;
  * il confronto a otto larghezze, in fr e in ar;
  * due selettori e la testa dell'hub.

---

## 4. Osservazioni (nessuna azione su questo commit)

* **O1 — due riassunti nel codice.** La docstring di `compare_files` (`services.py`, r. 773) dice «from left to right». Quattro riassunti dicono «side by side at the same phone width»: `__init__.py` r. 11, `services.py` r. 42, la docstring di `views.compare`, l'intestazione di `compare.html` r. 11.
  * Sono veri della disposizione da 54 rem. `compare.html` (r. 25–27), il foglio e la docstring di `Comparison` dicono entrambe le disposizioni, e nessuno di questi testi arriva al proprietario.
  * È la classe di HS-3: si possono sistemare con il prossimo commit che tocca questi file.
* **O2 — 8780.** Il server ufficiale è ancora il processo 22340, sul codice di prima di `37bf897`. L'hub del proprietario non mostra nulla di queste correzioni finché l'orchestratore non lo riavvia.
* **O3 — le note fuori dalla riga scritta.** `8602220` committa `PREVIEW_HUB_CATCHUP.md` e i due rapporti di revisione in `docs/design-v5/QA/`, fuori dai percorsi della riga del Preview Engineer.
  * È la pratica delle revisioni precedenti (O1 del servizio, O7 del catalogo).
  * All'orchestratore: scrivere `docs/design-v5/QA/PREVIEW_*.md` nella riga.
* **O4 — il verdetto del gate 0 su H-B.** La frase è «Raccomandata al gate 0 dal verificatore di design (R3B) e dal reparto composizione, che avevano davanti le sole H-0, H-A e H-B».
  * Resta, circoscritta, come W1, W2 e la revisione del catalogo l'hanno tenuta.
  * Tenerla o toglierla decide l'orchestratore.
* **O5 — il palco arabo.** In `stage-ar.html` la promessa è in francese, marcata `lang="fr" dir="ltr"`. È una scelta del file di ricerca, non dell'hub, e l'hub lo chiama «un primo schermo di sostituzione … non un eroe e non una proposta».
* **O6 — lo stile di HC-5.** «Il solo il cui movimento ha un verso» è corretto. «L'unico il cui movimento abbia un verso» si leggerebbe più piano. È facoltativo.
* **O7 — HS-2, il ramo di codice.** `compare_files` e `compare_view` leggono ancora `side.files[lang]`. Un confronto con una lingua sola risponderebbe 500, ma il test lo ferma prima del commit.
  * Se un confronto dovrà avere una lingua sola, serve la seconda correzione del revisore: `side.files.get(lang, "")` e la frase dei selettori.

---

## 5. Limiti

* **I browser.** Soltanto Chromium headless (Playwright 1.63.0): niente Firefox, niente Safari, nessun telefono vero, nessuna emulazione del tocco.
* **I test.** Soltanto `tests/frontend/test_design_preview.py` e i sottoinsiemi delle mutazioni, non la suite intera.
* **Le mutazioni.** Otto mutazioni e una simulazione, non tutte le combinazioni. Il volume senza nomi 8.3 è simulato in memoria, non provato su un volume vero.
* **Il censimento.** È un campionamento, ogni 40 ms. Il limite di 8 poggia sul semaforo e sul suo test.
* **Le fonti.** Ho confrontato le righe dell'hub con le fonti soltanto dove toccano i rilievi, non i rapporti di ricerca per intero:
  * `bench.js`, `doors.html`, `check/door-snippet.html`;
  * `LOADER_SIGNATURE.md` r. 28–36, 210–218, 474–482;
  * `IMAGE_ART_DIRECTION.md` r. 60, 173, 449;
  * `DECISION_LOG.md` A20.
* **Le pagine arabe.** Impaginazione, stato, errori e traboccamento controllati; nessun lettore arabo le ha lette.
* **H-E.** I suoi file possono cambiare mentre il consiglio su H-E è in corso: ciò che ho visto è lo stato delle 20:04–20:06.
* **I server altrui.** 8770–8772 e 8780 non sono stati interrogati, per regola.

---

## 6. Ciò che la verifica conferma

* **HC-1.** Sei link, uno per primaria e per lingua. Ciascuno disegna la primaria che nomina, a ogni larghezza e in entrambe le lingue; la riga dice del parametro; un test sul pacchetto vero lo tiene.
* **HC-2 … HC-8.** Le frasi sono vere a ogni larghezza misurata e contro le fonti, e l'italiano è corretto. Il link della verifica porta alla pagina con le due porte; il commento è attuale.
* **HS-1 … HS-3.** Le metà alias non passano più in silenzio, l'invariante delle lingue è tenuto da un test, i testi sono attuali.
* **Il servizio.**
  * Le guardie sono intatte: il resolver è identico al byte, e 151 percorsi ostili rispondono 404.
  * Il confronto rifiuta ogni query estranea (15 × 400).
  * Il tetto tiene: picco 3, poi 0.
  * Le pagine normali non cambiano.
* **I test.** 163 test verdi, che cadono quando devono.

**Verdetto: PASS.** Nessun rilievo aperto, nessun rilievo nuovo. Nulla di ciò che ho verificato impedisce di riavviare 8780 su `8602220` (O2).
