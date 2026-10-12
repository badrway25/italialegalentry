# Revisione indipendente del catalogo dell'hub e del confronto — commit `37bf897`

| | |
|---|---|
| **Oggetto** | `design-v5: preview — the hub catches up (research step 0, X-1 … X-5) and a compare view for the two phone «Mes pièces»` — commit `37bf897` su `design-v5` (genitore `e10002f`), 10 file, +1 452 −153, con la nota `docs/design-v5/QA/PREVIEW_HUB_CATCHUP.md` |
| **Ruolo** | Revisore indipendente, etichetta `review-catalogue`: lente del catalogo e dell'esperienza del proprietario. Non ha costruito nulla dell'anteprima |
| **Data** | 4 ottobre 2026, 18:25–19:15 |
| **Verdetto** | **PASS_WITH_FIXES**. Nessun rilievo bloccante. **Un maggiore** (HC-1: i due link «palco» del banco delle CTA mostrano soltanto T0, il riferimento, e dall'hub CTA-A e CTA-B sul primo schermo di sostituzione non si raggiungono). Sette minori, nove osservazioni |
| **Strumenti** | Server proprio della worktree su `127.0.0.1:8785` (`DB_CONN_MAX_AGE=0`, `DATABASE_URL=…/ile_v5`, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, `--noreload`), avviato e spento quattro volte (18:35, 18:38, 18:41, 18:50), con «port open: False» dopo ogni arresto. Playwright 1.63.0 headless (Chromium), profilo proprio `C:/tmp/ile_v5_council/.profiles/hub-review-catalogue/`. Corsia `ile_lane5` / `test_ile_lane5`, con zero connessioni su `test_ile_lane5` prima dell'avvio. Python 3.13.5 |
| **Lucchetto** | `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` atteso in codice (ciclo ogni 15 s, `gate.py`) prima di ogni server (4), di ogni sessione di browser (3), dei test e di `ruff`: 9 attese, tutte di 0 s (`gate.log`) |
| **Prove** | Fuori dal repository, in `C:/tmp/ile_v5_council/.work/hub-review-catalogue/`: `gate.py`, `srv.py`, `probe_http.py` → `probe_http.json` e `hub.html`, `outline.py` → `hub_outline.txt`, `look.py` → `look.json`, `look2.py` → `look2.json`, `look3.py` → `look3.json`, `lane5-pytest.log`, `shots/*.png` (52), `shots/pages/*.png` (50), `srv8785-*.log` |

Non ho toccato né caricato il server ufficiale su 8780 né i server 8770, 8771 e 8772. Non ho usato né il Chrome del proprietario (9223) né quello di QA (9222), e non ho eseguito comandi git che scrivono. Alle 18:55 un altro processo ha cominciato ad ascoltare su 8785 (PID 21212, avviato alle 18:55:24, cioè dopo l'ultimo arresto del mio server alle 18:51). Non è mio e non l'ho toccato. Niente di ciò che segue è una decisione di design.

---

## 0. In breve

L'hub si è messo in pari. Ogni voce X-1 e X-2 della sintesi è sull'hub, nel gruppo della sua corsia, sotto «prototipo di ricerca — non approvato», e punta a un file che risponde 200 con i sigilli. Sul pacchetto vero non compaiono più «manca», «in costruzione» né «La pagina finale». Le frasi di X-4 sono vere, e le ho misurate. Il commit non introduce classifiche e toglie tre raccomandazioni di chi aveva costruito i candidati. A 1440 × 900 il confronto fa ciò che dice. A 390 × 844 si legge: le due pagine stanno una sotto l'altra, ciascuna con il suo scorrimento e con lo stato nella didascalia.

Restano alcuni difetti:

* un posto del catalogo non mostra ciò che la sua riga promette: è HC-1;
* alcune frasi non sono vere a ogni larghezza, oppure non sono un italiano corretto: da HC-2 a HC-6;
* manca un link utile al proprietario: HC-7;
* un commento nel codice è rimasto indietro: HC-8.

---

## 1. Che cosa è stato verificato

| | Richiesta | Esito | § |
|---|---|---|---|
| (a) | Ogni voce X-1/X-2 è sull'hub, nel gruppo giusto, risolta, con una riga onesta e l'etichetta | **ok**, con HC-1 (palco), HC-4 (riga delle porte) e HC-7 (frammento) | 2.2, 2.3 |
| (b) | La riga O54/O55 sulla fila delle porte | **c'è**: il fatto regge, le parole non del tutto (HC-4) | 2.3 |
| (c) | Il confronto si usa a 1440 × 900 | **ok**: 2 × 390 px a x 312 e 736, alti 715 px, didascalie sulla stessa riga, scorrimento indipendente misurato, tasti `f` e `r` | 2.5 |
| (d) | Il confronto si legge a 390 × 844: le due pagine visibili, lo scorrimento indipendente, i nomi neutri | **ok**: una sotto l'altra, 356 px ciascuna, la seconda didascalia affiora a 764 px. Vedi HC-2 e O3 | 2.5 |
| (e) | Le parole di X-4 sono vere | **ok**, misurato: 120/200/480 ms sotto `?rm=1` su caricatori e cassetto, 0 ms sul banco, 0 ms con l'impostazione emulata | 2.6 |
| (f) | Neutralità: nessuna classifica, nessun aggettivo di merito, nessun ordine di preferenza | **ok**, salvo una frase ambigua (HC-5) | 2.4 |
| (g) | Nessun «manca» o «in costruzione» stantio, nessuna revisione o approvazione inventata | **ok** sull'hub. Restano una frase stantia in «In arrivo» (HC-6) e un commento nel codice (HC-8) | 2.2, 2.4 |
| (h) | L'italiano dell'hub è corretto | **in parte**: «udienze» e due calchi (HC-3) | 2.7 |
| (i) | Schermate di hub e confronto a 1440 × 900 e 390 × 844, guardate | **ok** | 2.8 |
| (j) | Test sulla corsia del revisore, `ruff`, fine riga | **ok**: 159 test passati in 54,3 s, `ruff` pulito, `i/lf w/lf` | 2.1 |

---

## 2. Le prove

### 2.1 I test, `ruff`, la fine riga

* **Test.** Ho eseguito `tests/frontend/test_design_preview.py` sulla corsia `ile_lane5` (`TEST_DATABASE_URL=…/ile_lane5`, cioè `test_ile_lane5`, senza connessioni prima dell'avvio). Risultato: **159 passed in 54.27s**, nessuno saltato, compresi i tre test nel browser (`lane5-pytest.log`).
* **`ruff`.** `ruff check` e `ruff format --check` su `apps/designpreview` e sul file di test sono puliti.
* **Fine riga.** `git ls-files --eol` dà `i/lf w/lf` per i 14 file della riga di proprietà e per la nota.

### 2.2 Il catalogo sul pacchetto vero

Ho eseguito `probe_http.py` sul pacchetto vero, in sola lettura.

* L'hub risponde 200 con `X-Robots-Tag: noindex, nofollow` e `Cache-Control: no-store`.
* I suoi 151 link interni rispondono tutti 200 con i due sigilli. Sono 125 file di prova, 9 voci del selettore del primo schermo, 14 del selettore tipografico, 2 del confronto e l'indice.
* Sull'hub non c'è nessun «manca» e nessun riferimento mancante.
* Le 23 voci nuove rispondono tutte 200: X-1, X-2, le voci proprie di H-E e i due confronti.

| Voce della sintesi (§6) | Gruppo dell'hub | Link | Esito |
|---|---|---|---|
| X-1 «Mes pièces» V5.2: `index`, `ar`, `anatomy` | 21 «Ricerca, terza ondata — «Mes pièces» V5.2» | fr · ar · tavola · confronto fr / ar | 5 × 200 |
| X-1 «La soglia» V5.2: `index`, `ar` | 22 | fr · ar | 200 |
| X-1 il campione dei colori | 23 | campione | 200 |
| X-1 le tavole delle icone: `sheet`, `sheet-ar`, `families`, `candidates` | 24 | fr · ar · famiglie · candidati | 200 |
| X-1 la fila delle porte: `doors`, `doors-ar` | 25 | fr · ar, con la riga O54/O55 | 200 |
| X-2 il banco del movimento (`he-motion`) | 2 «H-E — nuova direzione», in fondo | banco | 200 |
| X-2 il banco delle CTA: `states`, `stage` e i gemelli arabi | 2, in fondo | stati fr / ar · palco fr / ar | 200, **ma vedi HC-1** |
| X-2 la porta dal suo master: `snippet` | 2, in fondo | frammento | 200, vedi HC-7 |
| Le voci proprie di H-E: `he/index`, `ar`, `cta/index`, concetti E1–E3 | 2 | fr · ar · selettore · concetti 1–3 · campione | 200, nessun «manca» |

**L'ordine.**

* I cinque gruppi della terza ondata stanno dopo la seconda ondata (gruppo 20) e prima della baseline (26), nell'ordine di X-1.
* Le pagine di misura di H-E vengono dopo le voci proprie di H-E.

**Gli stati vecchi.**

* «in costruzione», «a seguire», «La pagina finale» e «Finché un file» non compaiono più nell'hub reso (`hub_outline.txt`), e `IN_CONSTRUCTION = ()`.
* Il selettore del primo schermo incornicia `he`, `e1`, `e2` ed `e3` con «prototipo di ricerca — non approvato».
* Su `he&lang=ar` la barra dice «da non firmare come /ar/»: la pagina porta la copia bloccata, non tradotta.

### 2.3 Le righe dell'hub, confrontate con le pagine

Ho aperto ogni pagina nuova in Chromium headless a 1440 × 900 e a 390 × 844: 50 schermate in `shots/pages/`, con 0 violazioni CSP, 0 errori in console e 0 richieste fallite per ciascuna. Poi ho letto titoli e sezioni contro la riga dell'hub.

* **«La tavola annotata».** Le dieci sezioni di `anatomy.html` sono le dieci cose che la riga elenca: le sei zone e il piede, i nove casi, la striscia, gli otto stati, le scadenze, la carta, il Dépôt, l'anteprima, la variante B, il conteggio a 20 o 28 px. **Vera.**
* **«La pagina» di «Mes pièces».** La striscia del registro porta l'azione primaria, e i tre gruppi sono «À vous · En cours · Réglées». **Vera.**
* **«La soglia» V5.2.** La pagina contiene il passaggio pubblico (sette stazioni, due soglie, i registri), «Tableau de bord», il fascicolo («Où en est ce dossier») e gli stati. **Vera**, per quanto dicono i titoli.
* **Il campione dei colori.** La pagina dice: «Les jetons de la porte 0 tels qu'ils sont, et les écarts proposés, côte à côte». Contiene 69 stringhe arabe. **Vera.**
* **Le icone.** Le sezioni §1–§8 di `sheet.html` sono le otto voci della riga; `families.html` ha dodici famiglie; `candidates.html` mostra i candidati su carta e su notte. **Vere**, salvo «udienze» (HC-3).
* **La fila delle porte.** La pagina mostra la riga A (gate 0), le righe B e B2 (le proposte, con due tagli della fotografia Persona) e la riga C (le alternative), poi le due rive. **Vera.**
  * La fascia in testa alla pagina dice: «Every photograph is PROVISIONAL until O54 and O55 are ruled and the context is adopted. Pexels License».
  * La riga C contiene Pexels 35699765, che `IMAGE_ART_DIRECTION.md` (passata d'igiene del 4 ottobre) segna «held — O55 ruling pending».
  * La riga dell'hub regge nella sostanza; le sue parole sono il rilievo HC-4.
* **Il banco del primo movimento.** La pagina dice: «a motion bench on a STAND-IN geometry — it is not H-E and not a V5 comp … drawn as a diagram … What is real: the clock…». **Vera.**
* **Le due CTA sul loro banco.**
  * `states.html` ha tre righe, T0 · CTA-A · CTA-B: vero.
  * `stage.html` e `stage-ar.html` prendono **una** CTA primaria dalla query. In `bench.js` il parametro è `?cta=t0|a|b`, con `t0` come valore predefinito.
  * Aperte come le collega l'hub, le due pagine danno `data-cta="t0"` e la classe `bench-t0` sulla CTA primaria. È il rilievo **HC-1**.
* **La porta dal suo master.**
  * `snippet.html` non ha `<html>`. Aperto da solo disegna la fotografia di 400 px e nient'altro. La riga lo dice: **vera**.
  * La pagina che mostra il frammento come porta, `check/door-snippet.html` («A — today · B — the snippet as written»), è su disco ma l'hub non la collega (HC-7).

### 2.4 La neutralità

* **Le parole.** Nei 14 gruppi di ricerca e in H-E non c'è nessuno di questi frammenti: «raccomand», «più forte», «superiore a», «migliore», «preferit», «il più», «il meno», «vincit».
  * Lo dice il test dell'ingegnere, che ho rieseguito, e lo conferma la mia ricerca sul testo reso.
  * I comparativi rimasti descrivono e non giudicano: «un passo più chiara», «più grande», «più stretta», «cinque volte più lento», «non è più notturno».
* **Le raccomandazioni tolte.** Sono sparite le tre raccomandazioni di chi aveva costruito i candidati: la tipografia, il caricatore, e per «Lume» «l'immagine più forte». Il comparativo di «Passo» è diventato un fatto, ma con parole che si possono leggere come un merito (HC-5).
* **H-B.** L'unica raccomandazione rimasta sull'hub è il verdetto indipendente del gate 0 su H-B. È circoscritto («che avevano davanti le sole H-0, H-A e H-B») ed è stato tenuto dalle revisioni W1 e W2 (O5).
* **L'ordine.** I gruppi seguono l'ordine delle ondate. Nel confronto vale l'ordine d'arrivo, ed è detto. CTA-A viene prima di CTA-B per ordine alfabetico.
* **Le revisioni dichiarate.**
  * Su H-E l'hub dice: «la cui revisione indipendente al 4 ottobre non è conclusa». È vero: la prosecuzione del consiglio su H-E era in corso mentre guardavo, e `he/index.html`, `ar.html` e `he.css` sono stati modificati alle 18:24–18:25.
  * Sui cinque gruppi della terza ondata l'hub dice «la revisione indipendente è in attesa». È vero per una revisione di design (O8).
* **Il confronto.**
  * Nomina le due pagine per ruolo, «La proposta dell'audit UI-UX-Pro-Max della piattaforma» e «La proposta dello specialista dello spazio documenti», cioè i ruoli della tabella di proprietà.
  * Nessuna parola dice quale sia la candidata.
  * Lo stato è nella didascalia di ciascuna pagina, a ogni larghezza.
  * In arabo la riga O10 sta sopra le due cornici, a ogni larghezza.

### 2.5 X-3 — il confronto, misurato

| Finestra | Disposizione | Larghezza di pagina in ciascuna cornice | Altezza della cornice | Nota della barra | Rotella sulla prima cornice |
|---|---|---|---|---|---|
| 1440 × 900 fr | affiancate, x 312 / 736, didascalie a y 93 sulla stessa riga | 390 px | 715 px (fondo a 884 su 900) | visibile | sinistra 700 px, destra 0, colonna 0 |
| 1440 × 900 ar | come sopra, cornici da y 201 (sotto la riga O10) | 390 px | 683 px | visibile | come sopra |
| 1366 × 768, 1280 × 720, 1024 × 768 | affiancate, fondo dentro la finestra | 390 px | 583 / 535 / 543 px | visibile | — |
| 864 × 900 | affiancate, x 24 / 448 | 390 px | 675 px | visibile | come sopra |
| 863 × 900 e 800 × 900, fr e ar | **una sotto l'altra** | 390 px | 644 px | **visibile**: dice «l'una accanto all'altra … a sinistra … a destra» (HC-2) | come sopra |
| 390 × 844 fr | una sotto l'altra; prima didascalia a y 65, **seconda a y 764**, che affiora in fondo alla prima schermata | **356 px** | 579 px | nascosta sotto 48 rem; le didascalie dicono autore, ondata e stato | sinistra 700 px, colonna 0 |
| 390 × 844 ar | come sopra, con la riga O10 in testa | 356 px | 579 px | nascosta | come sopra |

* **A 390 × 844, verso la seconda pagina.** Con il puntatore sulla prima cornice, la colonna si muove soltanto quando la prima pagina è arrivata in fondo: 3 189 px, cioè 8 scatti da 400. Con il puntatore sul margine di 16 px o su una didascalia, la colonna si muove subito, 500 px in un colpo (O3).
* **Le soglie.** A 864 px le cornici sono affiancate, a 863 px una sotto l'altra: la soglia è proprio i 54 rem dichiarati.
* **I tasti.** `r` porta a `lang=ar` e `f` a `lang=fr`, misurati con l'attesa della navigazione.
* **Le intestazioni.**
  * Il confronto risponde 200 con `noindex, nofollow`, `no-store`, `X-Frame-Options: DENY`, `frame-ancestors 'none'` e `frame-src 'self'`.
  * `pair=zz`, `pair=../.work`, `pair=MES-PIECES` e `lang=de` rispondono 400.
  * Senza query risponde il confronto in francese.
* **La pulizia.** 0 violazioni CSP in tutte le cornici e 0 errori in console, a ogni larghezza.

### 2.6 X-4 — misurato

| Pagina | `--motion-fast` / `-standard` / `-slow` | `html.rm` | transizione di `.btn` |
|---|---|---|---|
| Mandata, Lume, Passo, cassetto, senza parametro | 120 / 200 / 480 ms | no | 0,12 s × 3, 0,47 s |
| le stesse con `?rm=1` | **120 / 200 / 480 ms** | sì | **0,12 s × 3, 0,47 s** |
| il banco del movimento (seconda ondata) con `?rm=1` | **0 / 0 / 0 ms** | sì | 0 s |
| Mandata e il cassetto con l'impostazione emulata (`reduced_motion="reduce"`) | 0 / 0 / 0 ms | no | `0s`, `none` |

Le misure confermano le frasi dell'hub, una per una:

* **Caricatori, cassetto e tasti.** Il parametro ferma le animazioni proprie del prototipo (`shared/sig.css`: `html.rm … animation: none`; per il cassetto, `drawer-variants.css`) e lascia i token come sono. È ciò che dicono la riga dei caricatori, quella del cassetto e quella dei tasti.
* **Il banco.** «Il banco del movimento azzera da sé le durate sotto lo stesso parametro»: vero.
* **Lo stato vero.** «Lo stato vero è l'impostazione «riduci movimento» del sistema, o la sua emulazione in Chrome»: vero.
* **Dove compare il parametro.** Ogni `rm=1` offerto dall'hub sta nel gruppo dei caricatori, nel cassetto o nel banco: lo verifica il test, rieseguito. I selettori e il confronto non ne offrono.

### 2.7 L'italiano

Ho letto per intero l'hub reso (`hub_outline.txt`) e il confronto. Il testo nuovo è corretto e piano, con queste eccezioni:

* «le quattro udienze» (due volte), «i momenti propri» e «una linea di livello» (HC-3);
* «fotografie d'archivio» (HC-4);
* «Il solo candidato con una direzione» (HC-5).

### 2.8 Gli sguardi

| Schermate | Che cosa ho visto |
|---|---|
| `hub-1440x900.png`, `hub-390x844.png` | L'occhiello «ricerca, tre ondate», l'introduzione, l'avviso con la data di H-E, l'indice dei 27 gruppi. Nessun traboccamento orizzontale (`scrollWidth` = `innerWidth` a entrambe le larghezze), 17 etichette disegnate, 0 violazioni CSP |
| `hub-1440-g-he.png`, `hub-390-g-he.png` | Il gruppo di H-E con le sue sei righe; «da non firmare come /ar/» accanto a «ar · fase 3» alle due larghezze |
| `hub-{1440,390}-g-research-*.png` | I cinque gruppi della terza ondata, ciascuno con l'etichetta e «la revisione indipendente è in attesa»; la riga K5 con i due link al confronto; la riga della fila delle porte |
| `hub-390-keys.png` | «Tasti, confronto» e «Movimento ridotto» si leggono |
| `compare-fr-1440x900.png`, `compare-ar-1440x900.png`, `compare-fr-1440x900-after-wheel.png` | Due telefoni con le didascalie allineate. Dopo la rotella, la pagina di sinistra è scesa fino a «Non valide / Diplôme ou titre de formation» e quella di destra è ferma in cima |
| `compare-fr-390x844.png`, `compare-fr-390x844-bottom.png`, `compare-ar-390x844.png` | Le due pagine una sotto l'altra, lo stato in ogni didascalia, la seconda didascalia sul bordo inferiore |
| `compare-fr-800x900.png` | Due cornici una sotto l'altra, sotto una nota che le dice affiancate (HC-2) |
| `pages/hero_he-21st_stage.html-1440.png` e `…stage.html_q_cta-a-1440.png` | Il filo d'oro statico di T0 contro l'intarsio di CTA-A: l'hub raggiunge soltanto il primo (HC-1) |
| `pages/hero_door-master_snippet.html-1440.png` e `…check_door-snippet.html-1440.png` | Una fotografia sola contro due porte (HC-7) |

---

## 3. Rilievi

### HC-1 — MAGGIORE · «palco · fr» e «palco · ar» mostrano soltanto T0

**Fatto.**

* La riga dell'hub dice: «CTA-A e CTA-B accanto a T0, il riferimento: i loro stati, e un primo schermo di sostituzione».
* Il primo schermo di sostituzione prende una sola CTA primaria dalla query. In `bench.js` il parametro è `?cta=t0 | a | b`, e senza parametro vale `t0`.
* L'hub collega `stage.html` e `stage-ar.html` senza query. Ho misurato `data-cta="t0"` e la classe `bench-t0` sulla CTA primaria, nelle due lingue e alle due larghezze.
* Nulla sul palco dice quale CTA mostra, e né l'hub né la pagina dicono che il parametro esiste.

Chi apre «palco» vede dunque il riferimento, cioè la CTA primaria di H-D copiata, e non ha modo di vedere CTA-A o CTA-B sul primo schermo di sostituzione. Eppure il palco serve solo a questo: `21st/HE_SEARCH.md`, nell'elenco delle pagine, dice «One primary at a time (`?cta=t0`, `a` or `b`)». È un posto che non mostra ciò che la sua riga dice, il genere di difetto che le revisioni precedenti hanno già respinto, e riguarda il materiale di O68.

**Correzione.**

1. In `services.GROUPS`, gruppo H-E, riga «Le due CTA sul loro banco», sostituire i due link `palco` con un link per CTA e per lingua. La query va nell'etichetta, come per gli altri stati:
   * `_proof("palco · fr", f"{_HE_21ST}/stage.html", "fr", query="cta=a")` e lo stesso con `query="cta=b"`;
   * le stesse due voci per `stage-ar.html`;
   * T0 è già sulla pagina degli stati, oppure si tiene con `query="cta=t0"`.
2. Aggiungere alla riga: «Sul palco una CTA alla volta: il parametro cta sceglie T0, CTA-A o CTA-B.»
3. Aggiornare `test_h_e_says_where_it_stands_and_each_measurement_page_what_it_is_not`, il cui `_link_to` vuole l'`href` nudo, e le attese «palco · ar · manca» del pacchetto finto.
4. Rimisurare l'hub a 390 px: la riga avrà da sei a otto link.

### HC-2 — MINORE · fra 48 e 54 rem la barra del confronto descrive due pagine affiancate, ma le cornici stanno una sotto l'altra

**Fatto.**

* A 800 × 900 e a 863 × 900, in francese e in arabo, la nota della barra è disegnata (sparisce soltanto sotto i 48 rem). Dice «l'una accanto all'altra … seconda ondata a sinistra, terza ondata a destra».
* Intanto le due cornici stanno una sotto l'altra, entrambe a x 204 (o 235,5), a y 209 e 953.
* La riga K5 dell'hub dice «alla stessa larghezza di 390 px». Con una finestra sotto i 424 px le due pagine restano uguali ma più strette: 356 px ciascuna a 390 × 844.

**Correzione.**

1. Rendere la frase dell'ordine vera nelle due disposizioni. In `services.compare_view`, per esempio: «Le due pagine a 390 px, ciascuna con il suo scorrimento; in ordine d'arrivo — prima la seconda ondata, poi la terza — e non di preferenza: decide il proprietario.» «Prima» è a sinistra da 54 rem e in alto sotto.
2. Aggiornare la frase attesa da `test_the_compare_view_frames_the_two_phones_of_mes_pieces_side_by_side`.
3. Nella riga K5 scrivere: «alla stessa larghezza — 390 px da 864 px di finestra; sotto, una sotto l'altra, larghe quanto la finestra —».
4. Rimisurare a 800 e a 390.

### HC-3 — MINORE · «le quattro udienze»

**Fatto.**

* Il gruppo 24, nell'introduzione e nella riga «La tavola semantica», traduce «audiences» della revisione delle icone con «udienze».
* In italiano un'udienza è quella di un tribunale, oppure quella concessa da un'autorità. Su una piattaforma legale è la parola sbagliata nel senso peggiore.
* L'italiano del progetto dice «i quattro pubblici» (sei volte nel repository principale), oppure «i quattro accessi».
* Accanto ci sono due calchi. «I momenti propri» rende «custom moments». E il gruppo 22 dice «una linea di livello», che in italiano è una curva di livello; il gruppo 8 del gate 0 dice «la linea in piano».

**Correzione.** Scrivere «i quattro pubblici» (due volte), «i momenti su misura» e «una linea in piano». Nessun test tiene queste parole.

### HC-4 — MINORE · la riga della fila delle porte: «fotografie d'archivio trattenute»

**Fatto.**

* Le fotografie sono stock Pexels; la pagina dice «Pexels License. Test derivatives, not curated». «Fotografie d'archivio» si legge come fotografie storiche o di repertorio.
* «Trattenute» è vero di una sola fotografia: la 35699765, nella riga C, «held — O55 ruling pending».
* Le altre sono «PROVISIONAL until O54 and O55 are ruled and the context is adopted», come dice la pagina stessa.
* La decisione sulle fotografie della fila è O81 («the photographs (Q1–Q10)», `DECISION_LOG.md` A20). La sintesi, al §8 punto 8, scrive: «O81, O82 — the door row, the scope questions of O54 and O55».

**Correzione.**

1. Riscrivere la riga, per esempio: «Mostra fotografie stock (Pexels), provvisorie finché il proprietario non risponde a O54 e O55 e decide O81 — fra le alternative una è trattenuta per O55: una pagina soltanto locale, da non pubblicare.»
2. Aggiornare la frase attesa da `test_the_hub_shows_the_third_wave_each_group_tagged_and_every_link_on_a_file`.

### HC-5 — MINORE · «Il solo candidato con una direzione» si può leggere come un merito

**Fatto.**

* Nel rapporto sul caricatore, «The only candidate with a direction» vuol dire che il movimento di «Passo» ha un verso: il filo corre nel senso della lettura e in RTL si specchia (`LOADER_SIGNATURE.md`, r. 32 «brisk, horizontal, directional», r. 214).
* Di «Mandata» lo stesso rapporto scrive «It has no direction: one build for IT, FR, EN and AR» (r. 478).
* In italiano, «un candidato con una direzione» si legge come «con un senso di direzione», cioè come una qualità. E lo si legge sulla pagina dove il proprietario sceglie O71.
* Inoltre «marchio» compare due volte nella stessa frase.

**Correzione.** «Il solo il cui movimento ha un verso — corre nel senso della lettura e in arabo si specchia — e il solo che esce dal marchio: gli serve spazio accanto.»

### HC-6 — MINORE · «In arrivo — Fascicolo»: «Per ora esistono soltanto i campioni di ricerca: tipografia e navigazione»

**Fatto.** Dalla terza ondata l'hub stesso elenca, nel gruppo 22, una densità del fascicolo: «Il passaggio pubblico, il binario del cruscotto, il fascicolo e il formato compatto», e sulla pagina «Où en est ce dossier». Il «soltanto» è smentito dal catalogo dell'hub.

**Correzione.** «Per ora esistono soltanto campioni di ricerca: la tipografia, la navigazione e il registro del percorso nel fascicolo («La soglia» V5.2), qui sopra.»

### HC-7 — MINORE · «La porta dal suo master»: il link mostra una fotografia sola

**Fatto.**

* La riga dice onestamente che il frammento, aperto da solo, mostra la fotografia senza la porta.
* Misurato: una fotografia di 400 px in alto a sinistra, e 18 px di traboccamento orizzontale a 390.
* La corsia ha anche una pagina che esegue il frammento così com'è scritto, accanto alla porta di oggi: `research/hero/door-master/check/door-snippet.html`. Dice «A — today · B — the snippet as written … not a comp, not a design proposal».
* Quella pagina è su disco (200, 0 violazioni CSP) e l'hub non la collega. È lì che il proprietario vede «la porta dal suo master».

**Correzione.**

1. Aggiungere alla riga `_proof("verifica · oggi e il frammento", "research/hero/door-master/check/door-snippet.html", "fr")`.
2. Aggiungere alla riga una frase: «la pagina di verifica mette la porta di oggi accanto a quella del frammento».
3. Il percorso entra nel conto dei percorsi nuovi: aggiornare `assert len(set(paths)) == 23` in `test_no_new_entry_reaches_a_dotted_or_short_name_folder`.

### HC-8 — MINORE · un commento rimasto indietro

**Fatto.** In `services.py`, alle righe 430–434, sopra H-E in `HERO_VARIANTS`, il commento dice: «Announced before they are built (IN_CONSTRUCTION): until a file is in the proof directory its choice is struck through…». Ma `IN_CONSTRUCTION` è vuoto, e i file di H-E sono tenuti dal test di attualità come ogni altro.

**Correzione.** Dire che H-E è stato annunciato fino al 4 ottobre e che i suoi file ora sono tenuti come tutti gli altri.

---

## 4. Osservazioni (nessuna azione richiesta su questo commit)

* **O1 — E1 in arabo.**
  * `research/hero/he/concepts/e1/ar.html` esiste dal 2 ottobre, ore 22:12. La sua nota dice: «an RTL layout check only (the copy is not translated)… Not a candidate».
  * L'hub («in francese soltanto») e il selettore su `e1&lang=ar` («questa combinazione non esiste … costruito soltanto in fr») sono onesti sulla candidata.
  * Se il proprietario deve sapere che il controllo esiste, il selettore potrebbe dire: «c'è un controllo d'impaginazione RTL, non tradotto, non una candidata».
* **O2 — `research/icons/raster.html`.**
  * È la quinta pagina della corsia delle icone: i 113 simboli a quattro dimensioni.
  * La corsia la indica come sostituta, per la revisione, di `smoke/icons.html`, che è superato («110 symboles», R3A-5). La «Vetrina dei componenti» collega ancora quest'ultimo come «sprite».
  * Non è nell'elenco di X-1, ed è una pagina da desktop: a 390 px trabocca di 1 010 px. Decide l'orchestratore.
* **O3 — lo scorrimento a larghezza di telefono.**
  * La colonna è essa stessa un contenitore che scorre, e ogni cornice occupa 579 px su 844.
  * Con il puntatore sulla prima pagina, la rotella percorre tutta la pagina (3 189 px) prima che la colonna si muova; una didascalia o il margine di 16 px la muovono subito.
  * La seconda didascalia affiora a 764 px, quindi la seconda pagina si vede che c'è.
  * Un link di salto («↓ seconda pagina»), o cornici di circa 45 dvh sotto i 54 rem, metterebbero la seconda pagina a un gesto di distanza. È una questione di comodità per il proprietario, non un difetto.
* **O4 — sotto i 48 rem.** La frase dell'ordine sparisce, come nei selettori. Le didascalie tengono «seconda ondata» / «terza ondata» e lo stato.
* **O5 — il verdetto del gate 0 su H-B.**
  * La frase è: «Raccomandata al gate 0 dal verificatore di design (R3B) e dal reparto composizione, che avevano davanti le sole H-0, H-A e H-B».
  * È l'unica raccomandazione rimasta sull'hub. W1 (O5) e W2 l'hanno tenuta, circoscritta, e il gruppo del consiglio accanto dice che nessuno dei cinque primi schermi raggiunge il livello.
  * Il commit la tiene consapevolmente. Tenerla o toglierla decide l'orchestratore.
* **O6 — il 400 del confronto.** È quello di `frame.html`, e il suo titolo è «Selettore V5». È voluto (`views._picker`).
* **O7 — la nota dell'ingegnere.** `docs/design-v5/QA/PREVIEW_HUB_CATCHUP.md` sta fuori dalla riga di proprietà di `AGENT_OWNERSHIP.md`, come la nota dell'interruzione di `da75812`. Il contenuto è esatto: le sue misure a 1440 coincidono con le mie al pixel.
* **O8 — il red team della ricerca.**
  * `research/RESEARCH_RED_TEAM.md` ha controllato i prototipi sulle regole e sull'attualità delle misure, non sul design.
  * La sua condizione C2 trattiene alcune fotografie in attesa di O54/O55, e una di queste è sulla fila delle porte (35699765).
  * «La revisione indipendente è in attesa» resta vero per una revisione di design.
* **O9 — il riferimento nel confronto.**
  * Le due proposte si misurano contro la «Mes pièces» del gate 0, «la fondazione del gate 0, che resta com'è e fa da riferimento». Quella pagina non è nel confronto.
  * Tre cornici da 392 px, con gli spazi, occupano circa 1 272 px e starebbero a 1440. X-3 ne chiedeva due.
  * Scelgono l'orchestratore o il proprietario.

---

## 5. Limiti di questa revisione

* **La lente.** Ho guardato il catalogo e l'esperienza del proprietario. Non ho rivisto, oltre alla riesecuzione dei test, la sicurezza del resolver, le intestazioni diverse da quelle del confronto, il tetto delle connessioni e il database. I test sulle cartelle puntate e sugli alias 8.3 passano sulla mia corsia.
* **I browser.** Soltanto Chromium headless (Playwright 1.63.0): niente Firefox, niente Safari, nessun telefono vero, nessuna emulazione del tocco. Lo scorrimento di O3 è misurato con la rotella.
* **I rapporti di ricerca.** Li ho letti dove toccano una riga dell'hub, non per intero:
  * `LOADER_SIGNATURE`, `DOCUMENT_WORKSPACE`, `JOURNEY_SIGNATURE`;
  * `IMAGE_ART_DIRECTION` §6.4 e la nota d'igiene;
  * `DECISION_LOG` A2–A4 e A20;
  * `ICON_SEMANTIC_MAP` §11;
  * l'elenco delle pagine di `21st/HE_SEARCH`;
  * `MOTION_SYSTEM` MS7 e RM-2;
  * `RESEARCH_RED_TEAM`.

  Non ho verificato ciò che i prototipi affermano di sé, soltanto ciò che l'hub dice di loro.
* **H-E in movimento.** I file di H-E sono cambiati mentre lavoravo (18:24–18:25, la correzione del costruttore per il consiglio). Ciò che ho visto è lo stato delle 18:41–18:51.
* **Le pagine a 390.** Le pagine di X-1 a 390 px sono catturate, non lette riga per riga. Delle pagine arabe ho controllato lo stato, gli errori e il traboccamento; nessun lettore arabo le ha lette.
* **Il server 8780.** Gira sul codice di prima di questo commit: l'hub ufficiale non mostra nulla di tutto questo finché l'orchestratore non lo riavvia.

---

## 6. Ciò che la revisione conferma

* **Il catalogo.** Il pacchetto vero e l'hub dicono la stessa cosa.
  * Le 23 voci nuove sono su file che rispondono 200 con i sigilli.
  * Nulla è «manca», e H-E non è più «in costruzione» né «finale».
  * Ogni gruppo nuovo porta «prototipo di ricerca — non approvato» e dice chi l'ha guardato.
* **Le righe.** Fuori dai rilievi di questa revisione, le righe dicono ciò che le pagine sono.
* **X-4.** Le frasi sono vere, alla misura: sotto `?rm=1` i token restano a 120/200/480 ms su caricatori e cassetto, scendono a 0 sul banco, e scendono a 0 con l'impostazione del sistema.
* **La neutralità.** Nessuna classifica, nessun aggettivo di merito, nessuna raccomandazione di chi ha costruito i candidati. L'ordine è quello delle ondate o dell'arrivo, ed è detto.
* **Il confronto.**
  * A 1440 × 900 si usa: due telefoni di 390 px, ciascuno con il suo scorrimento, i nomi per ruolo, lo stato in ogni didascalia, i tasti `f` e `r`.
  * A 390 × 844 si legge: le due pagine una sotto l'altra.
  * Ha la sua CSP per vista, senza violazioni, e risponde 400 a ogni valore sconosciuto.
* **I test.** 159 test verdi sulla corsia del revisore; `ruff` pulito; LF ovunque.

**Verdetto: PASS_WITH_FIXES.**

* **HC-1** va chiuso prima di presentare al proprietario l'hub come messo in pari, perché il banco delle CTA è materiale di O68.
* **Da HC-2 a HC-8** si chiudono nello stesso passaggio: testo, un link, un commento. Nessuno tocca la sicurezza o la stabilità.
