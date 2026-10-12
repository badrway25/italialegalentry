# Revisione indipendente dell'anteprima V5, prima ondata — commit `3822588`

| | |
|---|---|
| **Oggetto** | `design-v5: preview — H-C/H-D in the hero picker, type picker, wave-1 research prototypes on the hub` — commit `3822588` su `design-v5` (genitore `f736b89`), 10 file, +1 839 −267 |
| **Ruolo** | Revisore indipendente dello stream B (non ha costruito nulla dell'anteprima) |
| **Data** | 2 ottobre 2026, 12:55–13:35 |
| **Verdetto** | **PASS_WITH_FIXES** — nessun rilievo bloccante; **due rilievi maggiori** (W1-1: l'hub dà a H-C e H-D un vantaggio di parole; W1-2: sotto 48rem nessuno stato dei selettori dice «non approvato»), tre minori, sette osservazioni. Sicurezza, sigilli e CSP: nulla da correggere |
| **Strumenti** | server proprio della worktree su `127.0.0.1:8782` (stesso ambiente dell'ingegnere: `DATABASE_URL=…/ile_v5`, `ILE_DESIGN_PREVIEW=1`, `--noreload`; avviato due volte, spento due volte); confronto con `main` su `127.0.0.1:8770`; corsia `ile_lane5`; Playwright 1.63.0 headless (Chromium), profilo proprio `C:/tmp/ile_v5_council/.profiles/stream-b/review-w1`; Django 5.2.17, django-csp 4.0, Python 3.13.5, pytest 9.0.3 |
| **Lucchetto** | `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` assente a ogni controllo (prima di ciascuna delle due esecuzioni di test, del server, di ciascuna delle otto sessioni di browser) |
| **Prove** | fuori dal repository, `C:/tmp/ile_review_b_w1/`: `probe_routes.py`, `probe_proof.py`, `probe_extra.py`, `probe_nul.py`, `verify_resolver.py`, `probe_csp.py`, `csp_seed.py`, `headers_extra.py`, `absence.py`, `manca.py`, `measure_bar.py`, `measure_bar2.py`, `measure_space.py`, `prototype_fix.py`, `look_hub.py`, `framed_all.py`, `note_wrap.py`, `contrast.py`, i rispettivi `.json`, `lane5.out.log`, `shots/*.png` |

Il server ufficiale su 8780 (stesso PID all'inizio e alla fine) e il Chrome del proprietario su 9223 non sono stati toccati; nessun browser su 9222. Nessuna sessione aperta, nessun modulo compilato. Niente di ciò che segue è una decisione di design.

---

## 1. Che cosa è stato verificato

| | Richiesta | Esito | § |
|---|---|---|---|
| (a) | I test, eseguiti dal revisore su `ile_lane5` | **ok — 279 passati, 0 falliti, 0 saltati** | 2.1 |
| (b) | Le rotte e le opzioni nuove rispondono 200 con `noindex`/`no-store` e il meta robots | **ok** — hub, 20 combinazioni del primo schermo, 70 del selettore tipografico | 2.2 |
| (c) | Valore sconosciuto → 400 | **ok** — 20 richieste, tutte 400 con i valori noti e il ritorno | 2.2 |
| (d) | Le combinazioni mancanti sono nominate, mai un link morto | **ok** | 2.2 |
| (e) | I rifiuti del resolver delle prove tengono | **ok** — 125 richieste grezze, 125 × 404 | 2.3 |
| (f) | CSP di produzione su `/fr/` identica a `main` (8770) | **ok** — stesse 11 direttive e valori; identica byte per byte a parità di seme di hash | 2.4 |
| (g) | Template puliti per la CSP | **ok** | 2.5 |
| (h) | F4 fatto come specificato | **ok** | 2.6 |
| (i) | F5: barra a 390 px, al più due righe | **in parte** — 85 px / 2 righe su 55 stati; **105 px / 3 righe sui 35 stati arabi del selettore tipografico** (W1-3) | 2.7 |
| (j) | L'hub etichetta ogni prototipo di ricerca come non approvato | **ok** | 2.8 |
| (k) | Nessun vantaggio di parole a H-C/H-D su H-0/H-A/H-B | **no** (W1-1) | 2.8 |
| (l) | Il diff resta nella riga di proprietà; LF; nessun segreto | **ok** | 2.9 |
| (m) | Solo sviluppo, solo loopback, anche per la rotta nuova | **ok** | 2.10 |
| (n) | Sguardo headless a 1440 e 390 | **ok**, con W1-2 e W1-4 | 2.11 |

---

## 2. Le prove

### 2.1 I test

```
TEST_DATABASE_URL=postgres://…/ile_lane5
.venv/Scripts/python -m pytest tests/frontend/test_design_preview.py tests/security
    tests/frontend/test_design_docs.py -q -p no:randomly -rxXfs
→ 279 passed in 241.14s
```

116 + 123 + 40. Nessun salto: i test dell'alias 8.3, del collegamento e del pacchetto vero sono stati eseguiti davvero. In più `apps/pages/tests/test_templates_static.py` (74) e `tests/i18n/test_rtl_static.py` (28): 102 passati; il numero dell'ingegnere, 353, si ricompone (116 + 123 + 40 + 74). `ruff check` e `ruff format --check` sull'app e sul file di test: puliti.

La correzione di `test_manage_check_passes_with_the_preview_on` è fondata: oggi `manage.py check` sull'intero progetto stampa `forum.ForumEvent.date: (fields.W161)` (verificato; Django avverte quando un default fisso cade su oggi), `manage.py check designpreview` risponde «no issues».

### 2.2 Rotte, opzioni, intestazioni — richieste grezze `http.client` su 8782

- **Hub**: 200, `X-Robots-Tag: noindex, nofollow`, `Cache-Control: no-store`, `<meta name="robots" content="noindex, nofollow">`, `Content-Language: it`.
- **Primo schermo**, 5 varianti × 2 lingue × 2 fasi = 20: tutte 200 con le due intestazioni e il meta. 14 incorniciano il file atteso (H-C → `research/hero/hc/{index,ar}.html`, H-D → `research/hero/hd/{index,ar}.html`), il file risponde 200 e porta il `lang` scelto. Le 6 mai costruite (l'intérim di H-C e H-D in fr e ar, l'intérim arabo di H-A e H-B) rispondono 200 **senza iframe**, con la frase («…non esiste: H-C è un prototipo di ricerca, costruito soltanto in fr · fase 3, ar · fase 3») e le scelte che vi portano barrate.
- **Tipografia**, 7 sistemi × 5 superfici × 2 lingue = 70: tutte 200 e sigillate; 49 incorniciate, 21 arabe mai costruite (menu, documenti, fascicolo) dette inesistenti; V4 porta «controllo — non una proposta», gli altri «prototipo di ricerca — non approvato».
- **Sconosciuto → 400**, 20 richieste (`variant=zz`, `HC`, `he`, vuoto, `lang=de`, `phase=9`, `system=A`, `surface=login`, `lang=it`, `%00`, `<script>`, `"><img onerror>`, `../../manage.py`, valore ripetuto): tutte 400, sigillate, senza iframe, con i valori noti («Varianti: h0, ha, hb, hc, hd · lingue: fr, ar · fasi: 3, interim») e «Torna a H-0» / «Torna a TYPE A»; il valore è riflesso con l'escape (0 script inline, 0 gestori nel documento).
- **Larghezze**: `²`, `٣٩٠`, cinquemila cifre, `-390`, `390px`, `0x186`, `1e3` → 200 senza classe sui due selettori; `1440`, `390` → la classe. Mai 500.
- **CSP per vista**: i due selettori `frame-src 'self'` (12 direttive), `frame-ancestors 'none'` e `X-Frame-Options: DENY` conservati; i file di prova `frame-ancestors 'self'` + `SAMEORIGIN`; `script-src 'self'; style-src 'self'` ovunque, nessun `unsafe`.
- **Link dell'hub**: 107 `href` distinti → 106 × 200 e un 302 (`/fr/espace-reserve/`, atteso); 0 «manca» sul pacchetto vero. Con una cartella delle prove quasi vuota (in-process, `manca.py`): 96 «manca», 10 link, nessuno verso un file assente; anche una voce di selettore diventa «manca», e il selettore chiesto a mano dice quale file manca.

### 2.3 Il resolver delle prove — 125 richieste grezze, 125 × 404

| Famiglia | Richieste | 404 |
|---|---|---|
| traversata semplice (`home/../../SIGNING_SHEET.md`, `research/hero/hc/../../../index.html`, `..;/`) | 12 | 12 |
| traversata percentuale (`%2e%2e/`, `%2E%2E`, `.%2e`, `%2f`, doppia codifica, `%c0%ae`, punto a larghezza piena) | 14 | 14 |
| barre rovesciate, grezze e `%5c`, UNC | 6 | 6 |
| segmenti puntati per nome lungo (`.work/`, `.ecd/`, `.vendor/`, `research/hero/hc/.work/`, `research/hero/hd/.source/`, `research/navigation/.evidence/`, `.git-status-after.txt`, `./`) | 17 | 17 |
| alias 8.3 (`WORK~1`, `work~1`, `WORK%7E1`, `ECD~1`, `VENDOR~1`, `PROFIL~1`, `GIT-ST~1.TXT`, `SOURCE~1`, `EVIDEN~1`, `INDEX~1.HTM`, `PHONE-~1`) | 19 | 19 |
| file di lavoro (`.py`, `.PY`, `.py.`, `.py%20`, `::$DATA`, `.ps1`, `.log`, `.jsonl`, `.gz`, `.pyc`, senza estensione) | 25 | 25 |
| lettere di unità e assoluti (`C:/…`, `C%3A`, `C:index.html`, `home/C:/…`, `:Zone.Identifier`, `//etc/passwd`) | 16 | 16 |
| cartelle, segmento vuoto, jolly, nomi di dispositivo, spazio o punto finale sul file | 16 | 16 |

Venti file veri (H-C, H-D, fogli e font della ricerca tipografica, stati con `?rm=1`, `?drawer=1`, `?exit=out`) → 200 con il tipo scritto e le due intestazioni. In-process su una radice di scarto (`verify_resolver.py`): alias della cartella e del file → 404; giunzione verso `.work` → 404; giunzione verso l'esterno → 404.

### 2.4 La CSP di produzione

`/fr/`, `/ar/`, `/fr/compte/login/`, `/fr/espace-reserve/` su 8782 (flag acceso) e su 8770 (`main`): stesse 11 direttive con gli stessi valori, stessa lunghezza (221 byte), stessi nomi e valori delle altre intestazioni di sicurezza, nessun `X-Robots-Tag`; lo stesso insieme di direttive su 8780. Le tre stringhe grezze differiscono **solo nell'ordine**: django-csp 4.0 itera un `set`, e l'ordine dipende dal seme di hash del processo. Tolta quella variabile l'identità è al byte: con `PYTHONHASHSEED=0` e poi `12345`, l'albero di `main` (senza flag, app non installata) e quello di `design-v5` (flag acceso, app installata) emettono sulle quattro pagine la stessa intestazione — SHA-256 `7e7d7b0b…205b1` e `822f627f…12b36`, uguali nei due alberi.

### 2.5 Pulizia CSP

Sorgenti (`hub.html`, `frame.html`, `bar_group.html`): nessun `style=`, `<style>`, `on*=`, `javascript:`, riferimento esterno; un solo `<script>`, con `src` e `defer`. Foglio: nessun `url(`, `@import`, `!important`, colore letterale. Script: nessuna rete, nessuno storage, nessun `innerHTML`. Pagine renderizzate (hub, 90 stati, 20 risposte 400): 0 attributi `style`, 0 `<style>`, 0 script inline, 0 gestori. Nel browser: **0 violazioni CSP in tutti i frame** sui 106 link dell'hub e sulle 63 combinazioni incorniciate caricate per intero, 0 richieste fallite, 0 errori in console (due avvisi del driver WebGL nella CTA di firma, del prototipo e del renderer software).

### 2.6 F4

In `ar · fase 3` la barra dice, per tutte e cinque le varianti: «ar · fase 3: la pagina porta la copia bloccata NON tradotta — da non firmare come /ar/.» da 48rem (visibile a 768, 1024, 1280, 1366, 1440) e «da non firmare come /ar/» sotto (360–767). In nessun'altra combinazione. L'affermazione è vera anche per le due ricerche: `research/hero/hc/ar.html` e `hd/ar.html` portano la promessa in francese e la striscia «copie verrouillée NON TRADUITE — ne pas signer». La parte facoltativa (collegare `home/options/index.html`) non è stata presa.

### 2.7 F5 — la barra, misurata (Chromium headless, font web applicati su 90 stati su 90)

| Finestra | Primo schermo (20 stati) | Tipografia fr (35) | Tipografia ar (35) | Stato «non approvato» leggibile |
|---|---|---|---|---|
| 360, 375, 390, 430 | 85 px · 2 righe | 85 px · 2 righe | **105 px · 3 righe** | **0 su 90** |
| 767 | 85 px · 2 righe | 85 px · 2 righe | 85 px · 2 righe | **0 su 90** |
| 768 | 117–137 px · 3–4 righe | 117 px · 3 | 137 px · 4 | 90 su 90 |
| 1024 | 77 px · 2 | 117 px · 3 | 117–137 px · 3–4 | 90 su 90 |
| 1280 | 77 px · 2 | 77 px · 2 | 77 px, **tre stati a 97 px** | 90 su 90 |
| 1366 | 77 px · 2 | 77 px · 2 | 77 px, **due stati a 97 px** | 90 su 90 |
| 1440 | 77 px · 2 | 77 px · 2 | 77 px · 2 | 90 su 90 |

Era 231 px a 390. Le larghezze non sono più disegnate sotto 48rem (0 stati su 90), come F5 chiedeva. Nessun overflow orizzontale a nessuna larghezza; il link più piccolo è 25,7 × 32 px. La terza riga dei 35 stati arabi è l'avviso che va a capo: il gruppo delle superfici è largo 308 px, il contenitore 344 px a 360 e 374 px a 390, e «caratteri arabi provvisori (O10)» ne chiede 171 — come «combinazione inesistente» sui 21 stati arabi che non esistono.

### 2.8 L'hub: etichette e parole

**Etichette — ok.** I cinque gruppi di ricerca (tipografia, caricatore, navigazione, cassetto, CTA) portano «prototipo di ricerca — non approvato» sotto il titolo; H-C e H-D, fra le maquette del gate 0, lo portano sulla propria riga; V4 porta «controllo — non una proposta». Ogni link verso `research/`, verso il selettore tipografico o verso `variant=hc|hd` (61 link) sta sotto una di queste etichette, visibili a 1440 e a 390 (contrasto 6,70:1). L'avviso «Niente di ciò che è mostrato è approvato» resta il primo blocco. Nella barra dei selettori, ordine H-0 · H-A · H-B · H-C · H-D, H-0 per default, nessuna parola di merito.

**Parole — no.** Le cinque note del gruppo «La home»:

| | Parole | Che cosa dice del confronto |
|---|---|---|
| H-0 | 28 | «Il verificatore R3B la indica come da non firmare; resta il termine di confronto.» (verdetto indipendente del gate 0, invariato da `806c429`) |
| H-A | 29 | nulla |
| H-B | 33 | «Raccomandata da due verificatori, non approvata» (indipendente, invariato) |
| H-C | 68 | «Per chi l'ha disegnata è **più forte di H-0 e H-A** e, contro H-B, più ricca di immagini e rotte ma meno calma e più debole sui portatili piccoli» |
| H-D | 67 | «Per chi l'ha disegnata è **nettamente superiore a H-0, H-A e H-B**, al prezzo del primo schermo notturno» |

Le due frasi sono fedeli ai rapporti (`docs/design-v5/research/HERO_HC.md` §10.3, `HERO_HD.md`, ramo `design-research-v5`) e sono attribuite. Restano l'unico giudizio comparativo non verificato della pagina, scritto sulla pagina con cui il proprietario decide O67 (W1-1).

### 2.9 Perimetro, LF, segreti

`git diff --name-status f736b89 3822588`: nove file modificati e uno nuovo (`templates/dev/designpreview/bar_group.html`), tutti nella riga del Preview Engineer di `AGENT_OWNERSHIP.md`; `config/` non è toccato. `git ls-files --eol` → `i/lf w/lf` per tutti; 0 byte CR, nessun BOM, newline finale, `git diff --check` pulito. Scansione delle righe aggiunte e del messaggio di commit (chiavi, token, password, PEM, URL di database, indirizzi): nulla — «keys» sono i tasti.

### 2.10 Solo sviluppo, solo loopback

`resolve()` sulle quattro rotte: `Resolver404` sotto `config.settings.test` con il flag nell'ambiente, sotto `dev` con `DJANGO_DEBUG=0` e flag, sotto `dev` con `DEBUG` e senza flag. Con entrambi: hub, primo schermo e **tipografia** rispondono 404 a `10.0.0.9`, `192.168.1.20`, `127.0.0.2`, `::ffff:127.0.0.1` e a un indirizzo esterno che dichiara `X-Forwarded-For: 127.0.0.1`.

### 2.11 Lo sguardo headless

Hub a 1440 (9 520 px) e a 390 (16 381 px): nessun overflow, Newsreader / IBM Plex Sans / IBM Plex Mono, fondo e inchiostro del sito, etichette italiane, nessun gradiente né ornamento. I tasti funzionano sui due selettori (`c`, `d`, `r`, `i`, `3`, `f`, `a`, `b`, `0`; `v`, `s`, `p`, `b`, `c`, `d`, `1`–`5`), `Ctrl+C` non naviga; con `w=390` su una finestra da 1440 la cornice è 390 px e la barra resta intera. Contrasti nella barra: stato 9,94:1, avviso 9,58:1, scelta barrata 6,13:1.

---

## 3. Rilievi

### W1-1 — MAGGIORE · l'hub dà a H-C e H-D un vantaggio di parole

**Fatto.** §2.8: «più forte di H-0 e H-A», «nettamente superiore a H-0, H-A e H-B». L'attribuzione («per chi l'ha disegnata», «giudizio del solo autore») è onesta ma non toglie la classifica dalla pagina; e la frase dell'hub è più netta del rapporto da cui viene, che di H-C scrive «"clearly" is not a word an author can sign» e, fra i costi, due emendamenti alla Direzione creativa e fotografie che il proprietario non ha scelto.

**Correzione.** Nelle due note di `services.GROUPS` togliere il confronto con le altre varianti; tenere la descrizione, ciò che la direzione chiede alle regole, e lo stato. Proposta, che conserva le tre frasi attese da `test_the_hub_says_that_a_research_prototype_is_not_approved_wherever_one_stands`: H-C «… da 1024 px, sotto non cambia nulla. Chiede due emendamenti alla Direzione creativa e poggia su fotografie provvisorie. Finora c'è soltanto il giudizio del solo autore: revisione indipendente in attesa, decide il proprietario (O67).»; H-D «… sotto i 1024 px è la soluzione A in tono di carta. Il primo schermo non è più notturno e CD §9 andrebbe emendato. Finora c'è soltanto il giudizio del solo autore: …». Aggiungere al test che nessuna nota del gruppo contenga «più forte», «superiore», «migliore». Da chiudere prima di presentare l'hub della prima ondata al proprietario.

### W1-2 — MAGGIORE · sotto 48rem nessuno stato dei selettori dice «non approvato»

**Fatto.** Sotto 48rem `.dp-bar__note` è `display: none` e resta soltanto l'avviso breve: a 360, 375, 390, 430 e 767 lo stato («prototipo di ricerca — non approvato», «maquette del gate 0 — non approvata», «controllo — non una proposta») non è leggibile in **nessuno** dei 90 stati. Resta nel solo attributo `title` dell'iframe. È la finestra della barra dei dispositivi di Chrome; la regola dell'anteprima è dirlo ovunque compaia un candidato. I test controllano che la frase sia nell'HTML, non che sia disegnata.

**Correzione.** Far portare a `.dp-bar__flag` sempre lo stato breve, seguito dall'avviso quando c'è (`services._frame`, `frame.html`). Fattibilità misurata dal revisore cambiando il solo testo nel DOM (`prototype_fix.py`, nulla nel repository): nel primo schermo «non approvato» sta sulla seconda riga a 360–430 (147 px liberi a 360); con «da non firmare come /ar/» intero mancano 1 px a 360 e nasce una terza riga, con «non firmare /ar/» restano 48 px. Nel selettore tipografico **non entra**: mancano 56 px a 360 e 26 a 390; abbreviando le superfici (crusc., docum., fasc.) entra «non approvato» (12 px liberi a 360) ma non «non approvato · O10» (−20 px). Lì la scelta è fra una terza riga breve e uniforme, dichiarata, e le abbreviazioni con l'O10 detto altrove: è una decisione dell'ingegnere e della direzione, da rimisurare a 360, 375, 390, 430. Aggiungere un controllo che fallisca se sotto 48rem lo stato non è disegnato.

### W1-3 — MINORE · F5: tre righe, non due, sui 35 stati arabi del selettore tipografico

**Fatto.** §2.7: 105 px e tre righe a 360–430 su tutti gli stati arabi del selettore tipografico — i 14 incorniciati e i 21 inesistenti. Il messaggio di commit dichiara i 105 px per i primi; il commento del foglio («Below 48rem the bar is two rows»), quello di `frame.html` e il nome `test_below_48rem_the_bar_gives_up_its_widths_and_is_two_rows` dicono due righe, e il test legge la griglia nel CSS, non la misura.

**Correzione.** Insieme a W1-2, perché le due cose si contendono lo stesso spazio: decidere quante righe ha la barra del selettore tipografico sotto 48rem, e far dire lo stesso numero al commento, al template, al nome del test e a una misura nel browser.

### W1-4 — MINORE · a 360 e 390 la nota «da non firmare come /ar/» dell'hub si stacca dal suo link

**Fatto.** A 360 e a 390, 5 note su 6 vanno a capo lontano da «ar · fase 3»; a 390 tutte e cinque finiscono sulla riga del link successivo («fr · intérim»; per H-C e H-D «selettore · fr · fase 3») e si leggono come riferite a quello. Da 430 in su stanno accanto al proprio link. Il difetto è di `806c429` (H-0, H-A, H-B) e ora vale anche per le due righe nuove.

**Correzione.** In `hub.html` tenere il link e la sua nota in un solo elemento che non si spezza (un contenitore `inline-flex` senza a capo); rimisurare a 360 e 390.

### W1-5 — MINORE · tre affermazioni che la misura non conferma

1. Foglio e commit: «77 px … at 1440, 1366 and 1280 for both pickers». A 1366 due stati (`a2`, `ap` · home · ar) e a 1280 tre (`a`, `a2`, `ap` · home · ar) sono a 97 px: la frase «Caratteri arabi provvisori … La home araba è quella dell'intérim.» va a capo.
2. `bar_group.html` rimanda a `designpreview.services._group`, che non esiste: i gruppi li costruisce `_frame`.
3. `apps/designpreview/__init__.py`: «every preview response says X-Robots-Tag … and Cache-Control: no-store». I rifiuti (404 del resolver, 403 del CSRF, 405 di `OPTIONS`) sono risposte di Django e non le portano; nessun contenuto dell'anteprima nel corpo. Dire «ogni risposta 200 e 400».

**Correzione.** Accorciare la frase araba della home, o correggere il numero; correggere i due testi.

---

## 4. Osservazioni (nessuna azione su questo commit)

- **O1 — CSP «identica»:** confrontare per insieme di direttive o a seme di hash fisso (§2.4); le stringhe di due processi non coincidono mai, nemmeno fra i tre server di `main`.
- **O2 — `%00` → 500, preesistente:** `…/proof/tools/shoot.py%00.html` risponde 500 come `/fr/nothing%00here/` su 8770; l'eccezione è `DataError` in `cms.LegacyURLMiddleware`, nessun frame dell'anteprima nella traccia. Il biglietto è già sul tabellone, ancora aperto.
- **O3 — punto finale su una cartella:** `home./phase3.html` e `research/hero/hc./index.html` → 200 (Windows toglie il punto); è lo stesso file servibile, giudicato sul percorso reale. `hc./.work/…` e `.work./…` → 404. Non è una fuga; da sapere.
- **O4 — fra 48rem e 64rem** la barra intera occupa 3–4 righe (117–137 px a 768; a 1024 nel selettore tipografico). Fuori da F5, che riguardava il telefono.
- **O5 — raccomandazioni degli autori altrove:** il gruppo tipografico («raccomanda di tenere l'architettura di A») e il caricatore («raccomanda Mandata»; «l'immagine più forte secondo il suo autore») le riportano, attribuite e conformi ai rapporti. Quando si neutralizzano H-C e H-D, dire anche che i due verificatori di H-B hanno confrontato le sole tre maquette del gate 0.
- **O6 — i link del selettore sull'hub sono solo francesi:** le 14 pagine arabe della ricerca tipografica si raggiungono soltanto dalla barra. Caricate tutte: nessun errore.
- **O7 — W161:** un test che chiedesse a `manage.py check` un progetto senza avvisi fallirebbe oggi, 2 ottobre 2026, e solo oggi.

---

## 5. Ciò che la revisione conferma

- La produzione non si muove: nessun file fuori dalla riga dell'ingegnere, `config/` intatto, la policy di `/fr/` è quella di `main` al byte a parità di seme, la rotta nuova non esiste senza `DEBUG` e flag e non risponde fuori dal loopback.
- Il resolver tiene su 125 richieste grezze e sui casi in-process; H-C, H-D e la ricerca non hanno aperto nulla: `.work/`, `.source/`, `.evidence/` e i loro alias restano chiusi, `.py`, `.ps1`, `.log` restano fuori.
- Ogni risposta 200 e 400 dell'anteprima porta `noindex, nofollow` e `no-store`; le pagine portano il meta robots; nessuno stile o script inline, nessuna violazione CSP in 169 caricamenti completi.
- I due selettori commutano 90 combinazioni: 63 incorniciano il file giusto nella lingua giusta, 27 dicono che cosa non esiste e che cosa esiste; nessun link morto, nessuna caduta su un'altra maquette; i valori sconosciuti ricevono 400.
- F4 è fatto, ed è vero anche per H-C e H-D. F5 ha portato la barra da 231 px a 85 px su 55 stati e a 105 px su 35.
- 279 test verdi sulla corsia del revisore; LF ovunque; nessun segreto.

**Verdetto: PASS_WITH_FIXES.** W1-1 e W1-2 sono testo e CSS, senza effetto sulla sicurezza, e vanno chiusi prima che l'hub della prima ondata sia presentato al proprietario come pronto; W1-3 si chiude con W1-2; W1-4 e W1-5 nello stesso passaggio.
