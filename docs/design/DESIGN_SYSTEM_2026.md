# DESIGN SYSTEM 2026 — Italy Legal Entry™

Direzione artistica **A — «Le Registre»**, decisa il 20 settembre 2026 e vincolante
(`docs/design/ART_DIRECTION_DECISION.md`); la direzione stessa, che è la fonte di ogni regola qui
scritta, è `docs/design/ART_DIRECTION_A.md`.

Questo documento è la **documentazione di ciò che esiste nel codice**, non di ciò che si vorrebbe:
ogni valore, contratto e comportamento è stato letto dai file sorgente. Il codice resta la fonte di
verità; il documento è tenuto allineato da test che ricalcolano i contrasti, confrontano i valori
letterali dei token, pesano i file e verificano che ogni percorso, test e screenshot citato esista.

| Campo | Valore |
|---|---|
| Data di riferimento | 21 settembre 2026 |
| Sostituisce | `docs/DESIGN_SYSTEM.md` (sistema a due inchiostri + bronzo, IBM Plex, ADR-008). Quel documento è ritirato: la sua struttura è conservata qui, il suo contenuto è vero solo dove questo documento lo ripete |
| Sorgenti documentate | `static/css/main.css`, `static/css/v5/fonts.css`, `static/css/tokens.css`, `static/css/_legacy-tokens.css`, `static/css/base.css`, `static/css/layout.css`, `static/css/components.css`, `static/js/head.js`, `static/js/main.js`, `static/img/icons.svg`, `static/img/illustrations/`, `static/fonts/`, `templates/base.html`, `templates/partials/`, `templates/components/` |
| Stato della costruzione | **token, scala tipografica, livello di layout e linguaggio grafico proprio (`static/css/register.css`) sono rifatti e committati**; `components.css` e la maggior parte dei 169 template sono ancora sul sistema vecchio e vivono sullo shim di demolizione (§17). Nessuna pagina è a metà: lo shim mappa i vecchi nomi sul nuovo sistema, così la resa è già quella nuova mentre il refactoring procede componente per componente. Il primo componente riscritto sul nuovo linguaggio è `templates/components/entrances.html`; il primo componente nuovo è `templates/components/jurisdiction.html` |
| Documento gemello | `docs/ACCESSIBILITY.md` (WCAG 2.2 AA, modello tastiera, lacune **G-01 … G-27**) |
| Decisioni collegate | ADR-008 (tipografia IBM Plex) — **superata** da §6.1; ADR-009 (server-rendered + progressive enhancement) — invariata |
| Test di veridicità | `tests/frontend/test_design_docs.py` — token e valori letterali, famiglie, tabella dei contrasti ricalcolata, componenti, icone, font, moduli JS, breakpoint, keyframe, pesi dei file, percorsi e test citati, shim legacy, inventario dei fogli delle app |
| Screenshot | `docs/qa/design/` — rigenerabili con `docs/qa/design/capture.py` (i PNG sono git-ignorati) |

> **Che cosa è cambiato e perché.** Il committente ha respinto il risultato visivo precedente come
> generico. Un Design Council di quattro giudici indipendenti ha scelto la direzione A: *il sito è un
> registro*. Ogni cosa ha una **posizione** (un ordinale), un'**autorità** (un attore responsabile
> nominato) e una **data o una fonte**. Le conseguenze sul design system sono cinque, e sono tutte
> rotture: la coppia tipografica cambia (IBM Plex → Newsreader / Fira Sans / Noto Naskh Arabic), il
> bronzo sparisce e al suo posto c'è la **rubrica** rossa il cui unico compito è marcare l'ordine, il
> verde di successo è abolito perché **nessun colore significa mai «approvato»**, i raggi vanno a 0
> con due eccezioni funzionali, e il contenitore smette di congelarsi a 1200 px. Dove il documento
> ritirato motivava una decisione che la direzione A ha rovesciato, questo documento lo dice a voce
> alta invece di lasciar cadere la riga in silenzio.

## Indice

1. Principi e anti-pattern · 2. Architettura CSS · 3. Token · 4. Colore · 5. Contrasto WCAG misurato ·
6. Tipografia · 7. Griglia, breakpoint e layout · 8. Il linguaggio grafico proprio ·
9. Superfici, bordi, elevazione · 10. Catalogo componenti · 11. Pattern di navigazione · 12. Motion ·
13. Iconografia · 14. Illustrazioni e fotografia · 15. RTL e arabo ·
16. Moduli JS e progressive enhancement · 17. Lo shim legacy e il conto alla rovescia ·
18. Come estendere il sistema · 19. Screenshot QA · 20. Controlli automatici · 21. Difetti noti

---

## 1. Principi e anti-pattern

### 1.1 Principi

1. **Un registro, non una brochure e non uno sportello.** Italy Legal Entry™ pubblica un elenco
   numerato, datato e attribuito di ciò che sono le vie regolari verso l'Italia, di chi è
   responsabile a ogni passo, e di ciò che questa organizzazione fa e non fa. La pagina è densa
   perché un registro è denso; è calma perché un registro non argomenta, registra.
2. **Istituzionale, mai istituzione.** AGAMI è un soggetto privato che pubblica, non
   un'amministrazione. Nessuno stemma, nessun emblema UE o della Repubblica, nessun lockup a tre
   bande in stile `.italia`, nessuna dicitura «sito ufficiale», nessun bottone SPID / CIE / pagoPA.
   Le persone che questo sito protegge sono già state avvicinate da qualcuno che diceva di agire per
   un'amministrazione: sembrare un'autorità pubblica è il rischio, non sembrare noiosi.
3. **Posizione, autorità, data.** Ogni sezione porta un ordinale, un responsabile nominato e una data
   o una fonte. È la stessa tripletta del modello di dominio (`rule_id` / `approved_by` /
   `valid_from`, `order` / `responsible_actor` / `due_date`), scritta due volte: una nei dati, una
   nella grammatica visiva.
4. **Token prima di tutto.** Nessun colore fuori da `static/css/tokens.css`: `base.css`,
   `layout.css` e `components.css` non contengono un solo valore esadecimale
   (`tests/frontend/test_static_assets.py::test_no_hardcoded_colours_outside_tokens_and_fonts`;
   unica eccezione ammessa, lo chevron `data:` del `<select>`). La regola vale anche per i fogli
   delle app (§2.1).
5. **Nessun colore significa mai «approvato».** Non esiste uno stato verde di successo. Un passo
   concluso è **TRASMESSO** o **CHIUSO**: un fatto sul fascicolo, non un verdetto. È la stessa
   ragione per cui l'esito `eligible` non esiste nel dominio — questa piattaforma non approva nulla.
   Il verde `--cooperation` significa *bilaterale* (il lato marocchino), mai *sì*.
6. **Progressive enhancement reale** (ADR-009). Ogni pagina funziona senza JavaScript: `<details>`
   per dropdown e accordion, pannelli delle tab impilati, menu interamente visibile, dialog
   raggiungibile via `:target`. La visibilità del contenuto non dipende mai da uno script.
7. **Accessibilità per costruzione.** Anello di focus a due toni su ogni superficie, controlli da
   44 px, contrasti misurati e bloccati da test, `prefers-reduced-motion` che azzera i token di
   durata, semantica nativa prima di ARIA. Dettagli in `docs/ACCESSIBILITY.md`.
8. **RTL nativo, arabo progettato.** Solo proprietà logiche; le regole `[dir="rtl"]` esistono
   unicamente dove la semantica lo richiede. L'arabo non è una traduzione del latino: ha la sua
   coppia display/testo, la sua interlinea e il suo registro (§15).
9. **Zero terze parti.** Font, icone, immagini e script self-hosted; CSP `default-src 'self'`.
10. **Sobrietà del movimento.** Nulla si muove allo scroll. Quattro livelli di motion, nessuna
    animazione in loop, nessun parallax, nessun autoplay (§12).

### 1.2 Anti-pattern rifiutati

| Anti-pattern | Perché è rifiutato | Dove è impedito nel codice |
|---|---|---|
| Aspetto «template SaaS / ThemeForest» | è la diagnosi letterale del committente («un sito standard generato da un'AI») | `--radius-control: 2px` e `--radius-marker: 50%` sono gli unici raggi; nessun `--radius-pill`; nessuna illustrazione 3D o isometrica |
| «Card soup» | una scheda è definita dalla sua scatola, non dai suoi angoli | la card è sostituita dall'**entrata** (§8.4): filetti e ordinali, nessun box. Una card sopravvive solo se passa per intero il test del benchmark (link a una pagina di dettaglio, contenuto unico rispetto ai fratelli, tipi di contenuto eterogenei, ≤ 4 in riga, un solo link) |
| Eyebrow maiuscolo spaziato | era la firma SaaS più visibile della build respinta: sei eyebrow su una sola home, tutti a 12 px / peso 600 / `letter-spacing: 1.44px` / bronzo | l'eyebrow è **abolito**: lo sostituisce il folio (§8.2). La classe `.eyebrow` sopravvive solo nello shim, in inchiostro e non in rubrica (§17) |
| Gradienti, neon, glassmorphism, `backdrop-filter` | decorazione senza compito, leggibilità imprevedibile, costo di compositing | nessun gradiente **decorativo**; le uniche funzioni `gradient()` del sistema sono le tre tratteggiature della barra di giurisdizione, che codificano il responsabile e non decorano nulla (§1.4, §8.7). Il velo `backdrop-filter` dell'header è l'unica altra eccezione dichiarata e va cancellato con la migrazione di `components.css` |
| Ombre da «floating UI» | in questo sistema la separazione è un filetto o un cambio di fondo | `--shadow-surface` è l'unica ombra dichiarata; i quattro token d'ombra legacy risolvono a `none` (§17) |
| Verde di successo | nessun elemento dell'interfaccia deve poter essere letto come un'approvazione | non esiste `--state-ok-*`: la terna si chiama `--state-done-*` ed è **blu** |
| Motion decorativo, parallax, carousel, autoplay | distrazione, WCAG 2.2.2, Core Web Vitals | nessun carousel; nulla si anima allo scroll; `prefers-reduced-motion` globale |
| Fotografia di repertorio | «quattro persone in felpa attorno a un tavolo di legno di recupero» è la categoria più pubblicata di Unsplash | una `<figure>` senza `<figcaption>` completa di luogo, data, frase di fatto e credito è un errore di build (§14.2). Il sito parte con **zero fotografie** |
| Emoji o librerie di icone miste | incoerenza | un solo sprite originale, `{% svg_icon %}` |
| Tricolore come palette | «non bandiera italiana» | nessun accostamento rosso/bianco/verde né rosso/verde nel sistema delle giurisdizioni; il rosso è **solo** rubrica, il verde **solo** asse marocchino |
| Loghi e stemmi di enti | non autorizzati (gate G6) | `tests/frontend/test_static_assets.py::test_illustrations_avoid_stereotyped_subjects` vieta file con `veneto`, `rovigo`, `regione`, `comune` in `static/img/` |
| Popup, cookie wall, banner invadenti | nessun cookie non tecnico | `templates/components/institutional_banner.html` non è dismissibile e non è un overlay |

### 1.3 Benchmark (R-DES-001, R-A11Y-002)

Designers Italia / Bootstrap Italia ed Europa Component Library restano riferimenti di **usabilità**
(navigazione prevedibile, breadcrumb, focus evidente, mobile-first, «fornire sempre un equivalente
testuale»), mai di identità. Sono esclusi **per identità, non per licenza**: Blu Italia `#0066cc` e
la sua rampa, ECL `#0E47CB` + `#FFD633`, Titillium Web. La ricerca completa è in
`docs/design/BENCHMARK_RESEARCH_2026.md`. Due regole sono adottate alla lettera: *quattro livelli di
titolo al massimo per pagina* (.italia) e *gli angoli squadrati si addicono agli elementi che
richiedono una presentazione formale e strutturata* (.italia).

### 1.4 Eccezioni dichiarate

| Dove | Cosa | Motivazione e limite |
|---|---|---|
| `.site-header::before` (`components.css` §7) | `backdrop-filter: saturate(140%) blur(8px)` sotto un velo opaco al 94 % | **Eccezione in scadenza.** La direzione A vieta il `backdrop-filter` per nome; l'header non è ancora stato riscritto. Il velo sta su uno pseudo-elemento *di proposito*: un elemento con `backdrop-filter` diventa containing block dei discendenti `position: fixed` e schiacciava il drawer (G-02, chiusa). Non riportarlo sull'elemento: `tests/frontend/test_design_docs.py::test_sticky_header_does_not_trap_fixed_drawer` lo impedisce |
| `--rubric-on-navy` | 4.46:1 sul navy | sotto la soglia del testo **per costruzione**: è un filetto, mai testo. §5 lo documenta con requisito 3.0 |
| `.jurisdiction__segment--*` (`register.css`) | tre `repeating-linear-gradient` | **non è un gradiente decorativo, è una tratteggiatura**: codifica il responsabile di un tratto e fa da equivalente per chi non può usare il colore (45° verde = Marocco, −45° navy = Italia, 90° inchiostro = autorità competente, nessuna tratteggiatura = piattaforma). Sotto `forced-colors` l'immagine di sfondo cade e restano il bordo e la legenda, che portano da soli il significato. È l'unico uso di `gradient()` ammesso nel sistema, **confermato come eccezione dichiarata dall'autore della direzione il 21 settembre 2026**: il divieto colpisce il gradiente come decorazione, e questa è una codifica, non una decorazione |

---

> **Questo documento descrive il sistema «Le Registre», superato il 24 settembre 2026.** La fonte
> di verità visiva è ora `docs/design-v2/DESIGN_SYSTEM_V2.md`; i layer 8–13 qui sopra sono i suoi.
> Le righe 1–7 restano perché sono ancora caricate e ancora vere, e perché la migrazione è in corso
> — non perché siano la direzione.

## 2. Architettura CSS

`static/css/main.css` è la **sorgente** della cascata: importa i layer in ordine. Il browser non la
riceve così. `npm run build:css` (`scripts/build_css.mjs`, esbuild, lo stesso binario del JS) risolve
gli `@import` nell'ordine dichiarato e scrive `static/css/dist/main.css`, senza commenti e minificato,
**senza abbassamento di sintassi** (nessun `target`: la cascata non viene reinterpretata).
`templates/base.html` applica soltanto quel file (`rel="stylesheet"`) e non precarica più i layer, che
sono dentro il bundle. Lo stesso comando minifica ogni foglio d'app in
`static/css/dist/<percorso statico>` (per esempio `css/dist/pages/css/pages.css`). Fu introdotto
nel gate A il 26/09/2026. Le 21 richieste occupavano per circa 1,3 s le sei connessioni HTTP/1.1,
mentre la fotografia LCP aspettava in coda; il CSS gzip passa da circa 95 a circa 35 KB. Prima di
adottarlo sono stati confrontati circa 7 milioni di valori calcolati, bundle contro sorgenti, su 30
combinazioni pagina × larghezza: 0 differenze. `static/css/dist/` è versionata come `static/js/dist/`
(l'host di produzione esegue `collectstatic`, non Node);
`tests/frontend/test_css_bundle_is_current.py` rifiuta un bundle più vecchio delle sorgenti. Dopo
ogni modifica a un foglio: `npm run build:css`, oppure `npm run watch:css`. Le mappe sorgente si
scrivono solo in watch e non si versionano. **Design V5 (5 ottobre 2026, W1-A).** La cascata si chiude con
i quattro fogli di `static/css/v5/`: le facce, i token, gli alias che danno ai nomi V1 / V2 / V4 i valori V5 e i
ruoli di base; `fonts.css` di V4 non apre più la cascata, i token V1 sì. Un foglio con prefisso `_` è un
**parziale** ovunque si trovi: `scripts/build_css.mjs` non lo tratta mai come ingresso, e lo porta nel bundle
del foglio che lo importa (`_legacy-tokens.css` qui sotto è il primo). Il CSS di una sola pagina vive in parziali di
`static/css/v5/` importati dai fogli di pagina, quello della sola console in parziali importati dall'ingresso della
console, `apps/portal/static/portal/console.css`: nessuno dei due entra in `main.css`, così una pagina pubblica non
scarica la console (piano V5.4 §2.3, DL54-15). Ogni foglio non parziale di `static/css/` è un layer di `main.css`, ogni
parziale è importato da almeno un ingresso
(`tests/frontend/test_design_docs.py::test_breakpoints_keyframes_and_stylesheets_are_documented`,
`tests/frontend/test_css_bundle_is_current.py::test_a_partial_is_never_an_entry_and_always_imported`), e i parziali
della console chiudono il loro ingresso come `v5/*` chiude `main.css`
(`tests/frontend/test_v5_tokens.py::test_the_console_partials_close_the_console_entry`).

**Un import si scrive nell'albero raccolto** (steward, 11 ottobre 2026). Ogni `@import` e ogni `url()` di un foglio
sorgente, commenti compresi, si scrive come si risolve nell'albero di `collectstatic` (`static/<p>` → `<p>`,
`apps/<app>/static/<p>` → `<p>`), dal percorso raccolto del foglio stesso: un parziale di `static/css/v5/` è
`../css/v5/_x.css` da `accounts/entrance.css` o `portal/console.css`, `../../css/v5/_x.css` da `pages/css/hero.css`, mai
`../../../../static/css/v5/_x.css`: esiste solo nei sorgenti e ferma `collectstatic` in produzione, e
`scripts/build_css.mjs`, che risolve con la stessa mappa, lo rifiuta
(`tests/frontend/test_static_pipeline.py::test_every_reference_of_every_source_sheet_resolves_in_the_collected_tree`).

I pesi qui sotto sono quelli delle **sorgenti**, in ordine di cascata:

| Ordine | File | Peso (non compresso, indicativo) | Contenuto |
|---|---|---|---|
| 1 | `tokens.css` | 11.3 KB | 105 custom property su `:root`, cinque fasce di breakpoint, override `:lang(ar)` / `[dir=rtl]`, override `prefers-reduced-motion` |
| 2 | `_legacy-tokens.css` | 11.1 KB | **impalcatura di demolizione**, non design system: 142 nomi vecchi mappati sul nuovo sistema (undici adottati da V5 e usciti il 5 ottobre 2026), più 14 classi tipografiche legacy. Il file solo si accorcia (§17) |
| 3 | `base.css` | 12.7 KB | reset, i dieci ruoli tipografici, cifre, skip link, `.prose`, helper bidi, stampa; link e focus sono passati a `v5/base.css` (W1-A, mappa delle cancellazioni del piano V5.4 §2.3) |
| 4 | `layout.css` | 5.8 KB | contenitori, la griglia a tre zone, sezioni per rango, griglia editoriale, utility di composizione |
| 5 | `components.css` | 14.9 KB | 10 sezioni numerate: icone → pattern di contenuto → overlay → motion (le §5–§7 della cromatura e la §25 del piè di pagina sono passate a `v5/chrome.css`, W2-C1; la §1 dei bottoni, la §3 delle pastiglie, la §4 delle notice, la §13 delle card, le §14–§15 di schede e accordion e le regole di campo della §20 a `v5/buttons.css`, `v5/chip.css`, `v5/notice.css`, `v5/card.css`, `v5/tabs.css` e `v5/field.css`, W1-C; la §8 del menu account e la §21 del dialog a `v5/overlays.css`, W2-A; il resto della §20 — il form di ricerca, l'indice alfabetico e le loro liste — e la §28 della pagina legale al partial di pagina `v5/_lettura.css`, che le pagine di contenuto caricano con `cms/lettura.css`, W3-F2; la §26 delle pagine d'errore, intera, e della §27 la cornice, la scheda e i pannelli delle pagine del conto al partial di pagina `v5/_servizio.css`, che le pagine del conto caricano con `cms/servizio.css` e le pagine d'errore con `cms/errori.css`, W3-F2 passo 2 — della §27 restano il secondo titolo che l'ingresso disegna e la tabella della console). **Non ancora migrato**: vive sui nomi dello shim |
| 6 | `register.css` | 21.2 KB | **il linguaggio grafico proprio** (§8): folio, registro ed entrata, sequenza, barra di giurisdizione, lastra e fascia verso, nota marginale, elenco delle fonti, esito, regione vuota, più il livello `@media (forced-colors: active)` |
| 7 | `v2/tokens.css` | 6.1 KB | **design V2** (`docs/design-v2/DESIGN_SYSTEM_V2.md`): i token di «due rive, una porta» — due capitoli di superficie, un solo accento interattivo, tre voci tipografiche, quattro durate, tre curve |
| 8 | `v2/bridge.css` | 2.4 KB | **impalcatura di migrazione, esiste per essere cancellata**: ripunta terreno, navy e rosso rubrica del sistema vecchio sui valori nuovi, così nessuna pagina resta a metà fra due direzioni finché la propagazione non è finita. Se ne va con `register.css` |
| 9 | `v4/tokens.css` | 15.5 KB | **design V4** (`docs/design-v4/DESIGN_SYSTEM_V4.md`, dopo la direttiva del committente del 24/09/2026): i token di «il portico e la console», caricati **per ultimi con i nomi V2** — il navy evoluto dal marchio ufficiale, l'accento come famiglia con due gradienti, le ricette di sfondo, cinque profondità e sei ruoli d'ombra, cinque raggi, la superfamiglia Plex (`--font-ui`, `--font-ref` e `--font-mono` ripuntati), la scala della console `--u-*`, misure di layout e controlli, dieci livelli `z`, sei durate e tre curve (i nomi V2 sono alias). Ripete l'override sotto `md` e il moto ridotto perché un `:root` successivo vince su una media query precedente; non ridefinisce `--border-strong` / `--border-accent`, che nello shim sono colori (le linee sono `--line-*`) |
| 10 | `v4/workspace.css` | 24.6 KB | **design V4, i componenti delle pagine della console** (gate C: dashboard e Mes pièces): Panel L1/L2 con bordo a gradiente via mask, ContextHeader e testata di workspace, il misuratore a tacche, ResponsibilityBar, Glyph, HealthStrip a segmenti proporzionali (`attr()` tipizzato, ripiego a segmenti uguali), liste di date e di messaggi, EmptyState; col gate D (fascicolo): la testata
di contesto con eyebrow, responsabile e misuratore, la barra di contesto compatta in vetro allo scroll, la
griglia 8/4 con inspector appiccicoso, la Table semantica a testata appiccicosa che sotto 64rem diventa schede etichettate, gli
intervenants, la barra dell'azione primaria del telefono. I cruscotti della persona e dell'impresa, la griglia di
lavoro a 12 colonne, i fatti e la Table dei bisogni se ne sono andati con il design V5 (W3-B: `v5/_dashboard.css`,
§11.7); il SegmentedControl, la ricerca e DocumentCollection / DocumentRow / DocumentCard con il menu di riga se ne
sono andati con «Mes pièces» V5 (W3-C: i partial `_workspace.css`, `_table.css` e `_depot.css` della console,
importati dal foglio delle pagine dei documenti, §11.8); la JourneyRail (orizzontale da 64rem, che si disegnava a ogni visita, e descrittiva nel fascicolo) e la
Timeline del fascicolo (`tl-light`) con il viaggio «La soglia» (W3-D: `v5/_journey-rail.css`, §11.9); Panel, ContextHeader e HealthStrip escono con i loro ultimi
consumatori (il fascicolo, «Ma situation» e i cruscotti: le pagine dei documenti non ne disegnano più). Solo token |
| 11 | `v4/hero.css` | 4.4 KB | **ciò che resta di «il portico»: la pittura della porta** per `components/doorway.html` — oggi la sola pagina d'ingresso (`templates/allauth/layouts/entrance.html`): le fermate dei gradienti come classi, la fotografia, l'arco, la porta interna, la chiave, i tre gradini e le loro regole sotto colori forzati. L'hero V4 della home (capitolo IMMERSIVE, griglia 6/6, le quattro vie, la corrente, la legenda in vetro) è uscito con l'hero V5.4 (W2-D, 8 ottobre 2026): l'hero V5 è `templates/pages/home/_hero.html` col proprio foglio di pagina `apps/pages/static/pages/css/hero.css` (§2.1) e il modulo `static/js/src/hero.js`. Il file esce da `main.css` con `_door.css` di W2-B (il partial di static/css/v5/ che prende il palcoscenico come disegnato) |
| 12 | `v5/fonts.css` | 6.1 KB | **design V5, tipo «Una voce»** (`docs/design-v5/V5_4_EXECUTION_PLAN.md` §1.1, §2.3; W1-A): cinque facce self-hosted — Host Grotesk variabile 400–700 e corsivo 400, «ILE Wordmark» (Newsreader 600, 11 code point), «ILE Mono» (il sottoinsieme di IBM Plex Mono rinominato), Vazirmatn variabile 400–700 — con `font-display: swap`, `unicode-range` e le facce di ripiego metriche (Segoe UI, Arial, Roboto; Georgia per il nome, Consolas per i riferimenti). Sostituisce `fonts.css` e i 26 woff2 di V4 (§6) |
| 13 | `v5/tokens.css` | 62.2 KB | **design V5, i token** (`docs/design-v5/DESIGN_SYSTEM_V5.md` §2–§4 emendato dal piano V5.4 §1.1–§1.6, §1.8): primitive (carta, inchiostro, notte, laguna, i materiali degli stati con il lapis di «En examen» e nessun viola), semantica (superfici, testo, linee, accento, il fuoco, i registri, le scale `--t-*` a otto taglie e `--u-*`, cinque livelli d'ombra nel colore della notte, il vetro a 0.94, il moto), componenti; caricati **dopo** V4: chiudono la cascata, e ripetono gli override stretti e del moto ridotto dei nomi che dichiarano |
| 14 | `v5/aliases.css` | 8.2 KB | **design V5, gli alias** (DS V5 §13): i nomi V1 / V2 / V4 ripuntati sui valori V5 — architettura A, «in place, alias-first» (piano §2.1): ogni pagina cambia valore senza cambiare un template, ed è «V4 + fondation» finché la sua famiglia non passa. Una regressione si corregge qui, mai in un template |
| 15 | `v5/base.css` | 7.7 KB | **design V5, i ruoli di base**: pesi e tracking dei titoli, il nome in «ILE Wordmark» ovunque compaia, «ILE Mono» al suo solo posto, i link nell'accento, **il sistema di fuoco unico** (§1.6: anello 2 px a 2 px, alone solo sui campi di testo, `Highlight` nei colori forzati), il testo digitato a 16 px, l'arabo (titoli 600 senza ×1.15, nessun maiuscolo, enfasi col peso), e la correzione «nessuna pagina peggiore» del controllo di consegna (la riga d'aiuto araba dell'ingresso sulla riga di 24 px; le due della barra console sul telefono — le etichette a 12 px, il titolo a 14 px con 8 px fra gli elementi — sono uscite con la barra, che W3-A ha ridisegnato: §11.6). Ultimo foglio della cascata, scritto per quella posizione |
| 16 | `v5/buttons.css` | 14.9 KB | **design V5, i bottoni** (piano V5.4 §1.4 SH-9, §1.5, §1.8; W1-C): la lastra con l'API di proprietà ereditata da V3 (`--btn-fill`, `--btn-ink`, `--btn-edge` e i loro stati, `--btn-box-h`, `--btn-pad` e `--btn-pad-end`: nel margine finale la chiave del loader trova il suo posto, e la freccia vi toglie 4 px per la compensazione ottica); il primario **piatto** in laguna — nessun gradiente, nessuna luce, nessuna ombra: l'unico trattamento di firma è il CTA dell'hero —, il secondario su carta col bordo strutturale, soft, ghost (l'azione discreta, etichetta nell'accento), danger a contorno granata, icona di 40 px con area di 44; le taglie 36 · 44 · 52 dai token di controllo; le varianti in riga (`--link`, `--text`) e `.link-arrow`; **un solo gesto di pressione** (il riempimento di pressione e 1 px in giù a 0 ms, rilascio su `--spring-snappy`); disabled per colore e cursore, mai per opacità; la notte per contesto e `.btn--inverse` (il primario come lastra di carta); 44 px sotto un puntatore grossolano; su una pagina araba l'etichetta latina che va a capo resta centrata nella lastra (`base.css` la isola da sinistra a destra e la allineerebbe al suo inizio); da tastiera nessuna transizione (`html[data-input="key"]`, livello 0); gerarchia a bordi nei colori forzati. La faccia d'attesa è del loader (`v5/loader.css`: la chiave nel margine finale, ogni variante sulla propria superficie). Sostituisce `components.css` §1, il foglio V3 dei bottoni e `v4/buttons.css` |
| 17 | `v5/field.css` | 19.4 KB | **design V5, i campi «la lastra»** (piano §1.4 SP-3, §1.6, §1.8, §1.13; W1-C): l'impalcatura del form (gruppi senza riquadro, legenda 20/28, azioni dopo un filetto); il campo — etichetta sopra 14/20 a 8 px, 24 px fra due campi, aiuto ed errori 13/20; il controllo come lastra — carta, filetto a 3:1, angoli di 4 px, nessuna ombra, 44 px in console e 52 px sulle pagine pubbliche, testo digitato a 16 px —, il select col gallone disegnato dall'inchiostro delle icone, il file (il suo bottone è un piccolo secondario: 36 px, 44 px sotto un puntatore grossolano), il campo password col comando mostra / nascondi; gli stati: hover, il filetto di 2 px che si disegna dal bordo di lettura al focus (subito da tastiera e a moto ridotto), invalido con bordo doppio, marca disegnata e parole, avviso, disabled, sola lettura, autofill; checkbox, radio e switch nativi disegnati dai token (24 px; 44 px di area sotto un puntatore grossolano); da tastiera il bordo, il comando mostra / nascondi e la spunta cambiano senza transizione (`html[data-input="key"]`, livello 0). Sostituisce le regole di campo di `components.css` §20 e il comando password di `v4/buttons.css` |
| 18 | `v5/chip.css` | 6.6 KB | **design V5, la pastiglia di stato «i cerchi»** (piano §1.2, §1.3, §1.8; W1-C): una marca, una parola e un bordo su un corpo tenue — lo stato detto tre volte senza colore: la parola, la **marca** del registro dallo sprite (cerchio aperto = in corso, pieno = risolto, il lucchetto per una dipendenza) e lo **stile del bordo** (pieno · tratteggiato per ciò che è dovuto · puntinato per ciò che non porta nulla). Otto registri da `data-register` (`apps/core/chips.py`), i cui token sono in `v5/tokens.css`, sulla carta, sul foglio e sulla notte: «conforme» è inchiostro e un disco pieno — nessun colore e nessuna spunta dice «approvato» (O14) —, «En examen» è lapis. Tre taglie esatte, 20 · 24 · 28 px, in ogni scrittura; la parola lunga va a capo, mai in una cella di tabella; la jauge di fase di un fascicolo in tre tacche; nessun hover né focus: uno stato non è un controllo. L'elemento ha un solo produttore, la coppia `chip` … `endchip` (`templates/components/chip.html`). Con essa `.tag`, l'etichetta di un termine — nessun registro, nessuna marca; 44 px di bersaglio sotto un puntatore grossolano quando è un link. Sostituisce `v3/chip.css`, la §3 di `components.css` e la pillola di `v4/workspace.css` |
| 19 | `v5/card.css` | 8.0 KB | **design V5, le card per funzione** (piano §1.3, §1.4, §1.15; W1-C): tre funzioni, mai una scatola per tutto — la **scheda** `.card` (ciò che esiste e si legge: foglio e filetto, livello 1; con un link l'intera scheda è il bersaglio; più schede di seguito sono una lista, `.card--flat`), la scheda d'**azione** `.card--action` (la sola cosa da fare sullo schermo, e una sola azione: è il piano rialzato, livello 2, uno per schermo) e la striscia di **sintesi** `dl.summary` (celle su un solo foglio, parole e cifre a misura di testo). Nessuna card-cifra, nessuna griglia di card uguali, niente che si trascini o si nasconda: il sistema ordina per priorità, il secondario si ripiega con una disclosure nativa. Angolo `--radius-lg`; al contatto il filetto si rafforza e il titolo si sottolinea — nessuna ombra si anima. Con esse `.meta-row`, la riga di metadati. Sostituisce la §13 di `components.css` |
| 20 | `v5/notice.css` | 4.2 KB | **design V5, le notice** (piano §1.2; W1-C): il messaggio sul lavaggio del suo registro, detto tre volte senza colore — la marca, il titolo, lo **stile** del filetto di 3 px al bordo di lettura: informazione in ardesia e attesa in lapis (pieno), fatto compiuto in **inchiostro** (pieno; nessun verde: nessun colore significa «approvato»), avvertenza in ambra (**tratteggiato**), errore in granata (**doppio**), nota istituzionale su carta col filetto oro; `.alert` per i messaggi di sessione. Sostituisce `components.css` §4 e la regola della notice di `v4/shell.css` |
| 21 | `v5/tabs.css` | 6.9 KB | **design V5, le schede e la disclosure** (piano §1.5 MS-O3; W1-C): le schede WAI-ARIA con **un solo indicatore**, che viaggia sotto l'etichetta scelta (solo `transform`: `--spring-snappy` sulle pagine pubbliche, `--ease-layout` in console; fermo da tastiera, al caricamento, al ridimensionamento e a moto ridotto) mentre il pannello arriva di 12 px dal lato del viaggio; pannelli impilati col proprio titolo senza script; l'accordion su `<details>`: filetti, riga di 56 px, gallone disegnato che ruota; da tastiera l'etichetta della scheda e il gallone cambiano senza transizione (`html[data-input="key"]`, livello 0). Sostituisce `components.css` §14 e §15 |
| 22 | `v5/overlays.css` | 22.3 KB | **design V5, il sistema degli overlay** (piano V5.4 §1.14; W2-A; il contratto `docs/design-v5/QA/v54/w2-a/CONTRACT.md`): un solo sistema sugli elementi nativi — il dialog e l'alertdialog, il drawer, lo sheet dal basso, il popover / menu e il tooltip — con `static/js/src/overlay.js`. Un foglio di carta col filetto, la testa (il disco del glifo di una conseguenza, il titolo, «Fermer» a 44 px sempre presente), il corpo che scorre da sé, il piede appiccicoso; ombra 3 per il popover, 4 per i modali; lo scrim è l'unico `.overlay-scrim` (il `::backdrop` del pannello per l'opzione nativa), `--scrim-modal`, sola opacità, mai sfocato; angoli 4 · 8 · 12 (i due in alto di uno sheet, il bordo libero di un drawer). Il moto è una transizione nei due sensi — `@starting-style` all'entrata, `allow-discrete` su `display` e `overlay` all'uscita, nulla che dia forma al pannello sotto `[open]` —: il dialog dal centro (.96 → 1 in 320 ms, fuori in 120), il drawer «Slide» dal suo bordo (320 / 200, `--ease-layout` all'uscita, lo scrim con lui, un solo `--dir` per i due versi), lo sheet sulla molla dello sheet (550 / 200, 48 px di margine sotto il bordo, l'area sicura), il menu da 4 px dal suo comando (200 / 120, ancorato sul bordo finale del comando nel proprio verso), il tooltip dopo 400 ms (un gruppo caldo mostra il vicino subito, il ponte di 6 px lo rende raggiungibile, se ne va a 0 ms); da tastiera 0 ms (`html[data-input="key"]`, ultimo nel foglio); sotto il moto ridotto una sola opacità di `--motion-reduced`, nessuna trasformazione; il blocco dello scroll senza spostamento (`html[data-overlay-lock]`, `scrollbar-gutter: stable` dove la pagina aveva una barra); ≤ 40rem il dialog e il menu diventano sheet — il menu sopra l'unico scrim, che prende tutta la pressione che lo chiude, col suo nome in testa (`.overlay__caption`) —, nessun tooltip; colori forzati, puntatore grossolano, stampa. Sostituisce `components.css` §21. **Il foglio è condiviso** — ogni pagina lo carica — e porta ciò che ogni pagina può disegnare: il pannello col suo moto, l'unico scrim, il drawer (quello della console), il popover / menu (sheet sul telefono), il tooltip del livello superiore, il blocco dello scroll. I pannelli con una testa (il dialog e l'alertdialog, lo sheet e la sua maniglia, testa / corpo / piede di `dialog.html`, `sheet.html` e `drawer.html`), il `::backdrop` del modale nativo e il tooltip `::after` del controllo sono **solo di pagina**: il parziale `v5/_overlay-panels.css`, che l'ingresso `apps/core/static/core/overlay-panels.css` porta in `css/dist/core/overlay-panels.css` (§2.1), collegato soltanto dalle pagine che li disegnano (il bilancio CSS V5.8 del committente: i tetti condivisi sono rigidi; DL54-94) |
| 23 | `v5/loader.css` | 11.5 KB | **design V5, il loader «Lume»** (piano V5.4 §1.9; DL54-07, DL54-08, DL54-09; W1-D): il marchio a strati nelle sue unità (`.sig`, `.sig__l`: la base, la stanza dietro la porta con la sua luce, la chiave d'oro col gemello d'inchiostro) con la primitiva del giro di chiave — un giro 0 → 360° sul proprio gambo, `--ease-turn`, mai tenuta specchiata — per l'ingresso del login, l'hero e il loader; la chiave occupata di ogni bottone d'invio (L2: `.btn.is-busy::after`, la maschera di `key.svg` nel colore del testo, al centro del padding di fine riga qualunque sia la taglia, un giro di `--motion-emphasized` poi tiene attenuata all'80 % — 3 : 1 sul suo fondo su ogni variante —, accesa alla risposta in pagina; nessuna chiave dove non ha posto: un bottone-link o un bottone-icona aspetta con `aria-busy` e resta com'è); la seduta delle righe di un frammento asincrono (L3: `[data-seat].is-seating`, 4 px in `--motion-standard`, scaglione `--motion-stagger`); lo stato di riposo dei due strati che il rilascio anima. Il rilascio stesso — la porta che si illumina sulla prima pagina della console dopo un accesso riuscito — è il parziale generato `v5/_loader-light.css` (`scripts/gen_loader_light.py`), importato dal solo ingresso della console. Solo token, solo proprietà logiche, nessun `will-change` |
| 24 | `v5/chrome.css` | 50.5 KB | **design V5, la cromatura pubblica «Il portico»** (piano V5.4 §1.11, §1.12; W2-C1): la barra istituzionale a 32 px col promotore e le quattro lingue nominate; la testata 64 → 56 px (vetro solo scrollata, da 80rem, senza pannello aperto); la barra con le quattro porte come bottoni di disclosure, il filetto, Forum e Projet; «l'architrave», l'unico indicatore; i pannelli delle porte appesi alla larghezza del contenuto, 8 | 4 — la glossa, le voci su righe a filetto con la seconda riga viva, «Voir l'espace», il piede anti-frode, la fotografia a colori col glifo del pubblico; «la targa» nella zona finale della testata; il foglio sotto 80rem — il drawer modale del sistema di overlay, «Quiet» sul telefono, laterale da 48rem (W2-C2); il lock-up e il piè di pagina (§11). Sostituisce `v2/shell.css`, `components.css` §5–§7 e §25 e `v4/shell.css` |

Convenzioni:

- **BEM-like**: `.block`, `.block__element`, `.block--modifier`. Stati tramite attributi, non classi:
  `[aria-current]`, `[aria-expanded="true"]`, `[aria-selected="true"]`, `[open]`,
  `[data-open="true"]`. Uniche classi di stato: `.is-visible` e
  `.is-active`.
- **Custom property di componente** (non sono token globali): `--btn-fill`, `--btn-ink`, `--btn-edge` e i loro
  stati (`-hover`, `-press`), `--btn-box-h`, `--btn-pad`, `--btn-pad-end`, `--notice-wash`, `--notice-word`, `--notice-rule`,
  `--field-draw`, `--tabs-x`, `--tabs-y`, `--tabs-w` e `--tabs-dir` (dichiarate in `v5/tabs.css` col loro valore
  senza script e scritte da `initTabs` sul widget),
  `--timeline-line`, `--stack-gap`, `--reveal-index` (impostata da `main.js`),
  `--portico-lead`, `--portico-h` e `--portico-scrim-top` (dichiarate in `v5/chrome.css` col loro valore senza
  script e scritte da `nav.js` sull'header, così ogni figlio le eredita: §11.5), gli orologi del sistema degli overlay
  `--overlay-in`, `--overlay-in-ease`, `--overlay-out`, `--overlay-out-ease`, `--overlay-scrim-in` e la sua posa chiusa
  `--overlay-closed-opacity`, `--overlay-closed-translate`, `--overlay-closed-scale`, con `--overlay-edge`,
  `--overlay-side` e `--overlay-bleed` (dichiarate sul pannello in `v5/overlays.css`, ripuntate da ogni famiglia;
  `--overlay-scrim-in`, che legge il solo `::backdrop` nativo, nel parziale di pagina `v5/_overlay-panels.css`),
  `--overlay-drag` (0 … 1, dichiarata nel parziale di pagina, scritta da `overlay.js` mentre si trascina la maniglia
  di uno sheet), `--dir` (1, o −1 sotto `[dir="rtl"]`: la sola variabile del verso) e `--tip-warm` (registrata con
  `@property` nel parziale di pagina: il gruppo caldo del tooltip `::after`).
- **Hook JS** solo tramite `data-*`, mai tramite classi di stile.
- **Classi di contesto**: `html.no-js` / `html.js`, `.on-inverse` / `.surface-inverse`,
  `body.is-rtl`, `:lang(ar)`.
- **Niente attributi `style`, niente `<style>` inline, niente handler inline**: la CSP è
  `style-src 'self'`, `script-src 'self'`
  (`tests/frontend/test_static_assets.py::test_owned_templates_have_no_forbidden_strings_inline_styles_or_handlers`).
- **La struttura si disegna con `border`, `outline` o testo, mai con un `background` su uno
  pseudo-elemento**: è la condizione perché il livello `@media (forced-colors: active)` possa
  restituire ogni filetto e ogni stato. Quel livello esiste, in fondo a `register.css`, e copre i
  dispositivi di §8; `components.css` non lo ha ancora e lo riceverà con la migrazione (G-26).

### 2.1 Fogli di stile e script delle app

`main.css` copre la shell e i componenti. Un'app che ha bisogno di layout propri aggiunge **un**
foglio in `apps/<app>/static/<app>/` e lo carica dal blocco `extra_head` (gli script dal blocco
`extra_scripts`, sempre `type="module"`, mai inline). Regole: classi con prefisso dell'app, solo
token esistenti, solo proprietà logiche, nessun componente del catalogo ridefinito, focus ereditato
da `base.css`, movimento solo con i token di durata. Le soglie locali (`40rem`, `88rem`, `90rem`)
sono ammesse per un singolo layout e non diventano breakpoint di sistema (§7.2).
`tests/frontend/test_design_docs.py::test_conforming_app_stylesheets_use_only_design_tokens` applica
queste regole a ogni foglio sotto `apps/*/static/`. Dal 21 settembre 2026 **tutti e cinque** i fogli
le rispettano e non esiste più un'eccezione dichiarata; il meccanismo che tiene in vista un foglio
non conforme — un elenco nominato più
`tests/frontend/test_design_docs.py::test_stage1_app_stylesheets_use_only_design_tokens` — resta al
suo posto, vuoto, per il prossimo.

| File | Caricato da | Conformità al sistema |
|---|---|---|
| `apps/pages/static/pages/css/pages.css` | `templates/pages/home.html`, `templates/dev/showcase.html` | conforme dal 21 settembre 2026 (G-25 chiusa); nessun colore letterale, nessun gradiente letterale. Dal 9 ottobre 2026 (V5.4, W2-D passo 3 «la home attorno all'hero», DL54-41) la parte della home è **riscritta sui token V5**: i capitoli sotto l'hero sono un solo oggetto — una fascia sul suo fondo (carta, pietra, l'unico capitolo BRAND con `var(--grad-brand)`, la notte), una testa al bordo di lettura (il segno dei tre gradini in inchiostro — il glifo d'identità `ile-steps` dello sprite, §13, mai specchiato —, il titolo 28/36 a 600, l'attacco 20/28) e un corpo; da 75rem la testa prende quattro colonne di dodici e resta in vista (`position: sticky`) mentre il corpo scorre, sotto sta sopra il corpo; spazi 48 · 64 · 96 px, filetti prima delle scatole, una riga ha il titolo 17/24 a 600 sopra il testo 15/24 (16/24 sotto 64rem) e mai più piccolo di ciò che intitola. Nessun occhiello, nessun ordinale (i numerali restano all'unica sequenza vera, i quattro passi neutri dell'orientamento a gate chiuso). Il registro dei quattro accessi (una cornice, quattro righe; due campate da 48rem), il registro degli otto percorsi su due colonne, l'enunciato del progetto pilota sulla notte, le quattro domande con le loro risposte su una colonna alla misura di lettura, «il gradino» anti-frode su una lastra propria (`.gradino`: foglio rialzato sulla pietra, filetto d'inchiostro al bordo di lettura, il paragrafo a 36 rem, sulle colonne del capitolo via `subgrid`), le notizie come righe (a capitolo vuoto una sola riga: il glifo dello spazio vuoto, `newspaper`, nel disco del componente, la frase, la promessa — senza la cornice tratteggiata del componente V4, niente centrato; dalla correzione della revisione senior, DL54-42, il capitolo è sulla home solo quando un articolo è in linea, a gate aperto come a gate chiuso — la riga vuota resta nel parziale e nel foglio, come ripiego), le due campate dell'ecosistema, la riga dell'area riservata sulla notte che il piè di pagina continua, con la chiave `ile-key`. I glifi d'identità stanno sul bordo di lettura col disegno, non con la scatola: la scatola è tirata dei margini vuoti del simbolo. Bianco e nero solo nell'hero (DL54-12): il foglio non dichiara alcun `filter`. Sulla pagina araba il capitolo si specchia; una riga francese in una testa finisce sul bordo di lettura, un blocco francese di lettura tiene il proprio allineamento. Le transizioni leggono `--motion-*` (V5); le pagine istituzionali e il pannello della pagina anti-frode sono usciti dal foglio con l'interno pubblico (W3-F1, 11 ottobre 2026): caricano `pages/css/interior.css`. Dalla stessa correzione (DL54-42): sulla pagina araba un invito del registro o una riga dei percorsi che sta in francese si legge da sinistra a destra, e la sua freccia punta nel verso della lettura; la freccia di un percorso sta a riposo a .6 dove un puntatore passa sopra (aspettava a 0, e nulla a riposo distingueva una riga che apre da una che non apre); l'invito del registro può andare su due righe (un ingrandimento del solo testo spingeva la pagina del telefono 66 px oltre il bordo). Sostituisce `v2/routes.css` e `v2/voyage.css`, usciti da `main.css`. Dall'11 ottobre 2026 (V5.4, W3-D) importa per prima cosa `static/css/v5/_journey-passage.css`, il parziale del passaggio pubblico «la linea» (§10, `stepper.html`; §11.9): i quattro passi neutri dell'orientamento a gate chiuso ne sono disegnati — le regole `.home-orientation .sequence*` se ne sono andate; la vetrina (solo in sviluppo) lo collega per il suo esempio del passaggio, e nessuna regola della home vi trova un elemento |
| `apps/pages/static/pages/css/hero.css` | `templates/pages/home.html` | conforme (foglio di pagina V5.4, W2-D, 8 ottobre 2026 — mai in `main.css`, piano §2.3, DL54-06): **l'hero finale** — desktop il flusso di E2 (l'enunciato, UN sentiero: un intarsio di bronzo sulla parete chiara all'altezza dell'imposta della porta con le stazioni vive della sequenza pilota, la svolta nella pietra, la luce d'oro nella nicchia notturna fino alla porta del committente; le quattro origini appese al sentiero: fotografia in bianco e nero a riposo, parola, frase), telefoni la composizione di E3 (enunciato → fascia notturna con la porta e le sei stazioni sulla rotaia → quattro tessere 2 × 2 unite dalla spina), poi la descrizione dell'hero come prima riga della piega. Solo token: i colori, le ombre e le pitture letterali dell'hero sono nominati nella §4.2 di `static/css/v5/tokens.css`; solo proprietà logiche (il palcoscenico è `direction: ltr`); nessun keyframe — le luci le muove `static/js/src/hero.js` (WAAPI, `transform` e `opacity`, un solo orologio, una volta per sessione, la mano la rimanda); a riposo nulla si muove; con `prefers-reduced-motion` l'immagine completa; sotto colori forzati parola + bordo. Il bottone «Masquer cette annonce» del banner vive ora nell'unica entry della home, `static/js/src/home.js` (bundle `static/js/dist/home.js`): il vecchio `pages/js/home.js` dell'app è cancellato (una richiesta in meno). La correzione di revisione del 9 ottobre 2026 (QA/hero-final/*_s2r2.md, misurata sul prototipo e rimisurata nel prodotto: QA/v54/w2-d/NOTES.md §7): la cella delle origini sulla scala di 4 px (12 · 4 · 8); **la parete prende la pagina** — parte dal margine di pagina (32 px) a ogni larghezza desktop (il contenitore di 1320 px del prototipo non è la colonna della cromatura del prodotto), finisce 16 px prima della spalla, e il palcoscenico poggia sulla spalla (pad della nicchia 0): colonne di 196 px a 1440 × 900 (frasi 4 · 5 · 5 · 3 righe), 222–277 px da 1536 (≤ 4 righe), lastre 192 px a 1440 e ≥ 160 da 1280, lastra 4 : 5 da 1680 × 940; **la porta poggia sul pavimento della nicchia** (16 px) e l'altezza che avanza è aria sopra l'arco e sopra l'enunciato, non una fascia vuota sotto le colonne; la composizione tiene l'altezza dell'hero (un elemento vuoto che ne attraversa le tracce: la riga della descrizione aveva assorbito il `min-block-size` della griglia); ogni testo francese allineato al bordo d'inizio sulla pagina araba (enunciato, frasi, inviti, etichette delle stazioni; «المغرب» mai sotto 14 px); le etichette del muro a 600 sull'intarsio più scuro; parole delle tessere 16 px con la freccia alla parola; la lista delle stazioni sopra il reset di lista del prodotto (i nodi sulla rotaia); la luce viaggiante con perla, coda di cometa e traccia che resta; la chiave che gira in 800 ms con alone e bagliore; la fascia più chiara al varco (riposo .9); il bottone di replay sopra la chiave; e il registro sotto l'hero (`_entrances.html`) non disegnato dove l'hero porta già le quattro frasi (≥ 64 rem e i tablet con la frase nella tessera), a 16 px dove resta. La correzione della revisione senior (`QA/v54/w2-d/REVIEW.md` e `A11Y_PERF.md`, 9 ottobre 2026; DL54-42, misure in `QA/v54/w2-d/NOTES.md` «Review fixes»): **da 96 rem la parete sta sulla colonna della pagina** — parte dal bordo del contenuto del contenitore, dove partono il logo e i capitoli (148 px a 1536, 280 a 1920, 600 a 2560); fino a 1535 px prende ancora la pagina —, la nicchia cede alla parete (quattro colonne di `--col-min` ci stanno sempre — 12 rem, 12,5 dove le frasi sono a 15 px: anche sotto una barra di scorrimento classica, che toglie 2 px a ogni colonna perché il limite è letto in `vw` e la griglia in `%`, la quarta parola tiene la sua riga (DL54-43) —: una finestra alta e stretta disegna una porta più piccola) e la lastra è larga quanto la sua colonna e alta quanto l'altezza lascia sotto il sentiero, tra 3 : 2 e 4 : 5 (192,8 × 189,5 px a 1536 × 864, 214,7 × 268,4 a 1920 × 1080), dai tagli 4 : 5 (3 : 2 nelle finestre alte al più 736 px) coperti dalla scatola; **al desktop la descrizione sta sulla colonna della pagina**, sulla carta della pagina, posta dalla griglia dell'hero (la linea `body-start`: segue la direzione della pagina, non quella del paragrafo), e la nicchia poggia sul bordo inferiore della composizione (la luce della parete e la grana sono della composizione, su `.he-ground`; la nicchia ritaglia le proprie ombre); la riga dell'ultima parola può entrare nei 16 px prima della spalla, così la sua freccia non va a capo e le quattro frasi stanno su una riga (parole a 15 px tra 1280 e 1312); «Maroc» a 700; nessuna luce propria sulla stazione della porta al desktop; la variante interim sui telefoni senza rotaia, con la porta sull'asse della spina e dimensionata dall'altezza della finestra, l'attacco non disegnato lì e a 17/28 al desktop; dove nulla passa sopra (`hover: none`) l'alone della chiave resta acceso piano e i quattro inviti stanno a riposo nel layout desktop; la riga delle stazioni ha la sua altezza prima che la lista arrivi |
| `apps/ecosystem/static/ecosystem/ecosystem.css` | `templates/ecosystem/_layout.html` | conforme: un elenco di import — la pagina dell'interno pubblico (`static/css/v5/_pagina.css`: la traccia, la testa, i capitoli, il registro e gli slot condivisi di D26, disegnati una volta per le pagine di W3-F1 e per quelle di contenuto di W3-F2 — consolidati da W3-F1 alla sua fusione, 12 ottobre 2026: V5.8, un componente, un disegno), poi la grammatica propria dell'interno pubblico V5.4 (W3-F1, 11 ottobre 2026), il partial `static/css/v5/_interior.css`, importati nel foglio di pagina — mai in `main.css` (piano §2.3) — e scritto, come ogni import, nell'albero raccolto: la traccia (i suoi link su scatole di 24 px, il bersaglio di 44 sotto un puntatore grossolano senza una riga più alta — SP-8; i link in avanti dei capitoli su scatole di `--hit-min`); l'ingresso «l'ingresso» (il nome dello spazio, l'h1 e l'attacco al bordo di lettura; nel posto finale, su una porta, la carta della porta «la porta», con la via d'ingresso della porta — `static/css/v5/_porta.css`, importato dai soli fogli delle porte —, sulla prima pagina del questionario la sua scheda d'azione, su una pagina lunga «Sommaire de la page», un link per riga a ogni larghezza); i capitoli della home (una testa al bordo di lettura col segno dei tre gradini, sticky da 75rem, un corpo); il registro (righe su filetti, la riga intera è il bersaglio, nessun glifo né freccia); gli slot di D26 (un riquadro, un'azione — la scheda d'azione —, l'host di un link d'autorità, didascalia e credito sotto ogni fotografia, «Besoin d'aide ? Écrivez-nous :» col solo testo vivo); il francese prescritto sulla pagina araba nella propria direzione (una testa finisce sul bordo di lettura; un attacco di più righe tiene il proprio inizio, in una scatola sul bordo di lettura non più larga delle sue parole). Tre raggi a schermo (6 piegato sul 6 della cromatura, 4, pieno); nessun movimento — e `_porta.css`, la carta della porta (la lastra notturna, il glifo del pubblico una volta sul disco notturno di 36 px, l'accento della porta come filetto di 3 px — la carta della porta del portico — e su di essa ciò che la porta offre per primo: il titolo o la frase della via e il suo unico controllo, nelle facce notturne dei bottoni; dalla correzione della revisione senior di W3-F1 (M1) i tre gradini disegnati al posto della fotografia, che si leggevano come un'immagine mancata, sono usciti; una fotografia curata e con didascalia prende il posto il giorno in cui esiste, e la via passa sotto l'attacco), e `_spaces.css`, ciò che gli spazi disegnano in più (la citazione prescritta dell'Espace Entreprises come enunciato; i sei campi brevi a una riga del modulo dei bisogni due a due da 64rem; le otto stazioni del progetto pilota su «la linea»: quattro per riga da 48rem, otto da 90rem — sotto, a 1280 e 1366, «ACCOMPAGNEMENT» si spezzava a metà parola). La frase dei destinatari dell'Espace Institutions è detta com'è scritta, come corpo del capitolo: tagliata in righe si leggeva come una lista con refusi. Sostituisce il foglio V1–V4 degli spazi (colonna laterale, foto, diagramma a schede, illustrazione) Dalla fusione di W3-D (12 ottobre 2026) «la linea» non è più del partial: è il passaggio pubblico `static/css/v5/_journey-passage.css` (W3-D, §10 `stepper.html`, §11.9), importato subito dopo `_interior.css` — un solo disegno per la home e per le pagine che disegnano una sequenza, le cui varianti di pagina restano nei loro parziali. |
| `apps/pages/static/pages/css/interior.css` | `templates/pages/institutional_base.html` | conforme: le pagine istituzionali (il progetto, il promotore, la rete, il contatto, l'anti-frode), un elenco di import — la pagina dell'interno pubblico (`static/css/v5/_pagina.css`: la traccia, la testa, i capitoli, il registro e gli slot condivisi di D26, disegnati una volta per le pagine di W3-F1 e per quelle di contenuto di W3-F2 — consolidati da W3-F1 alla sua fusione, 12 ottobre 2026: V5.8, un componente, un disegno), poi la grammatica propria dell'interno pubblico V5.4 (W3-F1, 11 ottobre 2026), il partial `static/css/v5/_interior.css`, importati nel foglio di pagina — mai in `main.css` (piano §2.3) — e scritto, come ogni import, nell'albero raccolto: la traccia (i suoi link su scatole di 24 px, il bersaglio di 44 sotto un puntatore grossolano senza una riga più alta — SP-8; i link in avanti dei capitoli su scatole di `--hit-min`); l'ingresso «l'ingresso» (il nome dello spazio, l'h1 e l'attacco al bordo di lettura; nel posto finale, su una porta, la carta della porta «la porta», con la via d'ingresso della porta — `static/css/v5/_porta.css`, importato dai soli fogli delle porte —, sulla prima pagina del questionario la sua scheda d'azione, su una pagina lunga «Sommaire de la page», un link per riga a ogni larghezza); i capitoli della home (una testa al bordo di lettura col segno dei tre gradini, sticky da 75rem, un corpo); il registro (righe su filetti, la riga intera è il bersaglio, nessun glifo né freccia); gli slot di D26 (un riquadro, un'azione — la scheda d'azione —, l'host di un link d'autorità, didascalia e credito sotto ogni fotografia, «Besoin d'aide ? Écrivez-nous :» col solo testo vivo); il francese prescritto sulla pagina araba nella propria direzione (una testa finisce sul bordo di lettura; un attacco di più righe tiene il proprio inizio, in una scatola sul bordo di lettura non più larga delle sue parole). Tre raggi a schermo (6 piegato sul 6 della cromatura, 4, pieno); nessun movimento — e `_institutional.css` (l'indirizzo unico in grande — 44 px sotto un puntatore grossolano —, la riga del marchio, il testo prescritto dell'anti-frode come unico riquadro della pagina — dal secondo passo di W3-F1 un avviso d'avvertimento dei componenti di base, mai il colore da solo: il segno dell'anti-frode, il titolo «Votre protection» nella parola del registro, il filetto spezzato; niente rosso, nessun allarme). Nuovo (W3-F1): le cinque pagine lasciano `pages.css`, che è della sola home Dalla fusione di W3-D (12 ottobre 2026) «la linea» non è più del partial (è il passaggio pubblico `static/css/v5/_journey-passage.css`, §11.9): queste pagine non la disegnano e non la caricano. |
| `apps/pathways/static/pathways/pathways.css` | `templates/pathways/index.html`, `templates/pathways/detail.html`, `templates/pathways/index_interim.html`, `templates/pathways/diplomas.html`, `templates/pathways/training.html` | conforme: l'Espace Personnes, un elenco di import — la pagina dell'interno pubblico (`static/css/v5/_pagina.css`: la traccia, la testa, i capitoli, il registro e gli slot condivisi di D26, disegnati una volta per le pagine di W3-F1 e per quelle di contenuto di W3-F2 — consolidati da W3-F1 alla sua fusione, 12 ottobre 2026: V5.8, un componente, un disegno), poi la grammatica propria dell'interno pubblico V5.4 (W3-F1, 11 ottobre 2026), il partial `static/css/v5/_interior.css`, importati nel foglio di pagina — mai in `main.css` (piano §2.3) — e scritto, come ogni import, nell'albero raccolto: la traccia (i suoi link su scatole di 24 px, il bersaglio di 44 sotto un puntatore grossolano senza una riga più alta — SP-8; i link in avanti dei capitoli su scatole di `--hit-min`); l'ingresso «l'ingresso» (il nome dello spazio, l'h1 e l'attacco al bordo di lettura; nel posto finale, su una porta, la carta della porta «la porta», con la via d'ingresso della porta — `static/css/v5/_porta.css`, importato dai soli fogli delle porte —, sulla prima pagina del questionario la sua scheda d'azione, su una pagina lunga «Sommaire de la page», un link per riga a ogni larghezza); i capitoli della home (una testa al bordo di lettura col segno dei tre gradini, sticky da 75rem, un corpo); il registro (righe su filetti, la riga intera è il bersaglio, nessun glifo né freccia); gli slot di D26 (un riquadro, un'azione — la scheda d'azione —, l'host di un link d'autorità, didascalia e credito sotto ogni fotografia, «Besoin d'aide ? Écrivez-nous :» col solo testo vivo); il francese prescritto sulla pagina araba nella propria direzione (una testa finisce sul bordo di lettura; un attacco di più righe tiene il proprio inizio, in una scatola sul bordo di lettura non più larga delle sue parole). Tre raggi a schermo (6 piegato sul 6 della cromatura, 4, pieno); nessun movimento — e `_porta.css`, la carta della porta che porta il questionario d'orientamento (la riga di `ecosystem.css`), e `_pathways.css` (la riga dei metadati di una scheda, i «Termes utiles» in una riga di etichette di una sola altezza — 44 px sotto un puntatore grossolano —, l'host dei link delle autorità; «Comment ça marche» su «la linea»: la frase prescritta tagliata sulle sue frecce in quattro stazioni, la sua riserva sotto — CREATIVE_DIRECTION_V5 legge 8, D-U4 —; dal secondo passo di W3-F1 i termini italiani di «Diplômes et titres» sotto la stazione a cui appartengono, i due tempi di «Formation» su «la linea» giù per il bordo di lettura — la parola di ciascun tempo al posto del numerale, accanto all'anello aperto, il titolo alla misura di voce, il testo alla misura di lettura —, e il richiamo anti-frode come avviso d'avvertimento dei componenti di base: il segno dell'anti-frode, il titolo prescritto nella parola del registro, le maiuscole spaziate, il filetto spezzato). Nuovo (W3-F1): le pagine dei percorsi non avevano foglio di pagina — una richiesta CSS in più prima di `load` su questi modelli Dalla fusione di W3-D (12 ottobre 2026) «la linea» non è più del partial: è il passaggio pubblico `static/css/v5/_journey-passage.css` (W3-D, §10 `stepper.html`, §11.9), importato subito dopo `_interior.css` — un solo disegno per la home e per le pagine che disegnano una sequenza, le cui varianti di pagina restano nei loro parziali. |
| `apps/portal/static/portal/portal.css` | `templates/portal/base_portal.html` | conforme: solo token esistenti, solo proprietà logiche, nessun gradiente |
| `apps/portal/static/portal/console.css` | `templates/portal/base_portal.html` | conforme: **l'ingresso della console, design V5** (piano V5.4 §2.3, §3.5 voce 3; W3-A) — è la sola **lista di import** della console: `static/css/v5/_loader-light.css` (il rilascio del loader, W1-D), poi `v5/_shell.css`, il parziale della cromatura «Tre livelli» (§11.6): rail notturna 248 / 64 px al bordo di lettura, a tre livelli (spazio → sezione → pagina) con il piede fisso; barra di contesto 56 px in vetro con il solo breadcrumb; cornice di pagina a 1320 con un unico bordo d'inizio e un'unica testata di pagina; sotto 64rem la rail distesa — barra superiore e barra inferiore notturne (quattro voci al più + «Menu»), cassetto `<dialog>` con la rail intera e il suo piede; poi `v5/_dashboard.css`, il parziale dei cruscotti — la persona, l'impresa, il ponte (§11.7, W3-B). Non sono qui il parziale del viaggio «La soglia» (W3-D) né il modulo guidato di «Ma situation» (W3-F1, `v5/_wizard.css`, che vi stava dalla fusione di W3-F1): sono dei fogli di sola pagina `portal/journey.css` e `portal/situation.css` (righe seguenti; V5.8 del committente e la sentenza definitiva dell'orchestratore, 12 ottobre 2026: i fogli condivisi non salgono mai, il CSS proprio di una superficie va in un foglio caricato solo dove serve). Ogni famiglia della console aggiunge qui l'import del proprio parziale. Solo token, solo proprietà logiche, nessun gradiente; due raggi (4 px e pieno), nessuna ombra nella navigazione |
| `apps/portal/static/portal/journey.css` | `templates/portal/dashboard.html`, `templates/portal/pathways.html`, `templates/cases/detail.html`, `templates/dev/showcase.html` | conforme: **il foglio di sola pagina del viaggio «La soglia»**, design V5 (piano V5.4 §3.5 voce 6; W3-D; V5.8 del committente, 11 ottobre 2026, e la sentenza definitiva dell'orchestratore, 12 ottobre: i fogli condivisi — `main.css` su ogni pagina, `main.css` + `console.css` + `portal.css` su ogni pagina della console — non salgono mai, il CSS proprio di una superficie va in un foglio di pagina caricato solo dove serve, e ogni pagina carica solo ciò che disegna). È la sola **lista di import** del percorso e della Timeline sull'unico disegno di binario della console: il vocabolario, `v5/_journey-nodes.css` (una linea, tre nodi), poi `v5/_journey-rail.css` (la spina, le parole, la linea in piano, la carta e la sua divulgazione, la Timeline, la pagina «Mon parcours»; §10, §11.9). Lo collegano, dopo i due fogli della cromatura (`{{ block.super }}` in `extra_head`: il posto nella cascata che il binario aveva come ultimo import di `console.css`), le tre pagine che disegnano il percorso o la Timeline — il cruscotto e «Mon parcours» solo quando la persona ha un fascicolo —, e la vetrina (solo in sviluppo) per i suoi esempi; lo Stepper di «Ma situation» è lo stesso disegno, nel foglio di quella pagina (`portal/situation.css`, riga seguente). Solo token, solo proprietà logiche, nessun gradiente, nulla che si muova |
| `apps/portal/static/portal/situation.css` | `templates/portal/situation.html`, `templates/dev/showcase.html` | conforme: **il foglio di sola pagina di «Ma situation»**, design V5 (alla fusione di W3-D, 12 ottobre 2026, per la sentenza definitiva dell'orchestratore su V5.8: i fogli condivisi non salgono mai, il CSS proprio di una superficie va in un foglio di pagina, e ogni pagina carica solo ciò che disegna). È la sola **lista di import** della pagina, nell'ordine della cascata che aveva: il modulo guidato, `v5/_wizard.css` (W3-F1, piano V5.4 §3.5 voce 1 — i raggi della console 4 · 8 · pieno, un solo pannello sollevato, nessuna luce dietro la domanda, le OptionCards, il piede parte della pagina dopo un filetto; dalla fusione di W3-F1 a quella di W3-D stava in `console.css`, su ogni pagina della console), poi il suo Stepper sull'unico disegno di binario — il vocabolario `v5/_journey-nodes.css` e `v5/_journey-stepper.css` (W3-D, §10 `wizard_stepper.html`). Nel prodotto lo collega solo «Ma situation», dopo i due fogli della cromatura: la pagina non carica mai la linea in piano, la carta né la Timeline; la vetrina (solo in sviluppo) lo collega per i suoi esempi dello Stepper e delle OptionCards. Solo token, solo proprietà logiche |
| `apps/core/static/core/overlay-panels.css` | `templates/dev/designpreview/specimens/overlays.html`, `templates/dev/showcase.html` | conforme: **l'ingresso solo di pagina del sistema degli overlay** (design V5, W2-A; il bilancio CSS V5.8 del committente, 11 ottobre 2026, DL54-94) — una lista di import: il parziale `static/css/v5/_overlay-panels.css`, scritto nell'albero raccolto (§2), con i pannelli che nessuna pagina del prodotto disegna oggi — il dialog e l'alertdialog, lo sheet dal basso e la sua maniglia, testa / corpo / piede di `dialog.html`, `sheet.html` e `drawer.html` —, il `::backdrop` del modale nativo e il tooltip `::after` del controllo. Lo collega solo la pagina che disegna uno di quei pannelli (`docs/design-v5/QA/v54/w2-a/CONTRACT.md` §1): oggi la tavola degli overlay e la vetrina; domani i dialog del personale (W3-E), la conferma di un'azione distruttiva (W3-F2), il cassetto dell'anteprima e lo sheet dei filtri (W3-C). Il resto del sistema è `v5/overlays.css`, in `main.css` |
| `apps/accounts/static/accounts/entrance.css` | `templates/allauth/layouts/entrance.html` | conforme (34.5 KB): **l'ingresso «Il varco»** (design V5, piano V5.4 §1.13 «Le vie convergono al varco»; W2-B: il palcoscenico e il modulo) — due pannelli 5/7 da 64rem. Il palcoscenico è una nicchia notturna dietro il muro chiaro della pagina (lo spessore del muro in due anelli di pietra, l'ombra che il muro getta nella nicchia) con la porta del committente sulla soglia — disegnata da `static/css/v5/_door.css`, il parziale che questo foglio importa —, quattro vie nei colori dei pubblici che salgono dal bordo inferiore e convergono sulla soglia, una pozza calda ai piedi dei gradini e la riga d'aiuto; su una pagina più lunga dello schermo (la registrazione) la scena resta in vista sotto la testata. Gli stati li scrive `static/js/src/entrance.js` come classi (`is-ways`, `is-held`, `is-frame`) e il foglio li disegna: un passaggio di luce per ogni focus da puntatore, un'opacità altrimenti, nulla dalla tastiera né sotto il moto ridotto; all'invio dell'accesso la chiave del palcoscenico gira una volta e tiene (`loader.js`, §16). Sotto 64rem una fascia con la porta e la riga d'aiuto, poi il modulo (72 px sotto 44rem d'altezza). La grana del 3 % è della sola nicchia, da 64rem: sulla fascia non si vede, e il suo file vi era il più grande dipinto della pagina (L9: «la porta, non la grana»); da 64rem la nicchia tocca il piè di pagina notturno, una sola notte, come l'ultimo capitolo della home. Solo token, solo proprietà logiche, nessun gradiente né colore letterale: i gradienti del palcoscenico — le ombre della nicchia, lo spessore del muro, la soglia, la pozza, le vie e la loro luce — sono il parziale di sola pagina `static/css/v5/_varco.css` (6.6 KB), che questo foglio importa dopo la porta e che li compone dai colori del blocco §4.3 di `v5/tokens.css` con `color-mix(in srgb, … N%, transparent)`; come token di pittura in `main.css` gli stessi gradienti pesavano 579 B gzip su ogni pagina del sito (DL54-15: le regole di una sola pagina vanno nei parziali di pagina). La scena è `direction: ltr`: un disegno non si specchia. Nel sorgente il modulo precede il palcoscenico (dopo il link di salto la prima sosta è nel modulo): le due parti sono collocate su linee di griglia, ciascuna nella propria cella per intero, e la notte del posto del palcoscenico è dipinta dalla scatola stessa della pagina (`.varco::before`), così un browser che dipinge prima di aver letto il palcoscenico non sposta nulla e non mostra il fondo chiaro al suo posto. **Il modulo** (passo 2) non ha scheda: è una colonna di 25rem posata sul fondo stesso della pagina, appesa all'alto del suo pannello a una distanza che dà lo schermo (`clamp(3rem, 14vh − 1rem, 12rem)` da 64rem) e mai centrata sulla propria altezza — il titolo sta alla stessa quota su ogni pagina d'ingresso, all'altezza della cima dell'arco, e nulla si sposta se il browser dipinge prima di aver letto tutta la colonna (il foglio V4, centrato, era l'ultima fonte di spostamento della pagina). Una sola gerarchia, che scrive il layout: l'occhiello «Espace réservé» con la chiave del registro delle icone (`ile-key`, la stessa della targa), UN titolo (28/36, 36/44 da 48rem), la frase a 17/28, i campi — «la lastra» del sistema, `static/css/v5/field.css` —, UN primario a tutta colonna, 52 px, piatto; poi ciò che è quieto: l'assicurazione (solo sull'accesso: la risposta bloccata della FAQ sulla protezione dei dati, alla lettera, sotto un filetto, dietro il gate di Fase 3) e, sulle pagine che non sono un modulo, la via del ritorno all'accesso. Il foglio aggiunge ai campi: la riga dell'etichetta con il link «mot de passe oublié» alla sua fine — scritto DOPO il controllo nel sorgente (dalla tastiera l'indirizzo è seguito dalla password, mai da un link) e collocato dalla griglia (`:has(> .form-field__aside)`) —, il comando mostra / nascondi del sistema (`v5/field.css` §5: il glifo in un bersaglio di 44 px), che senza script l'ingresso non disegna e che non lascia mai a un campo mostrato l'ortografia né le correzioni della tastiera (`shell.js` §3), i segnaposto non disegnati, l'asterisco non disegnato quando ogni campo è obbligatorio, il codice a una sola volta in cifre tabulari. Il primario dei moduli che completano un accesso — quelli che nominano il palcoscenico (`data-loader-host`) — tiene a riposo la stessa chiave che il loader fa girare quando è occupato: la stessa maschera — un solo token, `--key-mask` di `v5/tokens.css`, letto da questo foglio e da `static/css/v5/loader.css` —, la stessa scatola, il centro dello stesso margine finale; all'invio l'etichetta non si muove di un pixel. Un messaggio di sessione, che `templates/base.html` scrive prima dell'ingresso, prende posto nella colonna del modulo (`main` diventa la griglia di cui l'ingresso prende le linee, `subgrid`): il palcoscenico tocca sempre la testata. Nessun moto proprio: il moto del modulo — il filetto del focus, la pressione, la chiave — è del sistema. `templates/429.html` rende sulla stessa pagina il «troppe richieste» di allauth (per chi è già entrato, la pagina d'errore del prodotto) |
| `apps/cms/static/cms/lettura.css` | `templates/faq/index.html`, `templates/glossary/index.html`, `templates/news/index.html`, `templates/living/index.html`, `templates/partners/index.html`, `templates/community/landing.html`, `templates/enquiries/contact.html`, `templates/legal/document.html`, `templates/consents/newsletter_confirm.html` | conforme (foglio di pagina V5.4, W3-F2 passo 1 — mai in `main.css`, piano §2.3, DL54-15): **le pagine di contenuto «la lettura»** — la lista di import di `static/css/v5/_pagina.css` (la traccia, la testa, i capitoli, il registro e gli slot condivisi di D26, disegnati una volta per queste pagine e per quelle di W3-F1 — consolidati da W3-F1 alla sua fusione, 12 ottobre 2026; la revisione m11) e di `static/css/v5/_lettura.css`, che tutte le pagine di contenuto caricano (le FAQ, il glossario, le notizie, «Vivre en Italie», i partner, il Forum Virtuel, i moduli di richiesta, le pagine legali, i consensi della newsletter): la traccia, la testa al bordo di lettura, i capitoli con un solo dispositivo di sezione, il registro su filetti condivisi, gli strumenti, gli slot di D26; solo token, solo proprietà logiche, nessun gradiente |
| `apps/cms/static/cms/servizio.css` | `templates/allauth/layouts/base.html`, `templates/accounts/delete_done.html` | conforme (foglio di pagina V5.4, W3-F2 passo 2 — mai in `main.css`, piano §2.3, DL54-15): **le pagine del conto** — la sola lista di import di `static/css/v5/_servizio.css`, «le pagine di servizio»: le pagine del conto (il profilo, le pagine di gestione di allauth, la richiesta di cancellazione e la sua risposta: la traccia, le sezioni del conto al bordo di lettura da 64rem e in banda sotto, la pagina nelle otto colonne del corpo, le sezioni su filetti, i fatti come registro, il bottone di pericolo dietro la sua pagina di conferma) e le regole delle pagine d'errore, che caricano lo stesso partial con `cms/errori.css`; tre raggi per schermo, nessuna ombra a riposo, solo token, solo proprietà logiche |
| `apps/cms/static/cms/errori.css` | `templates/errors/base_error.html`, `templates/errors/standalone.html` | conforme (foglio di pagina V5.4, W3-F2, la correzione della revisione M1 — mai in `main.css`): **le pagine d'errore** (400, 403, 404, 410, 429, 500) — importa la porta come disegnata (`static/css/v5/_door.css`, il partial dell'ingresso) e `static/css/v5/_servizio.css`, poi dice il posto della **porta a riposo** (`templates/errors/_door.html`; CREATIVE_DIRECTION_V5 §20, DS V5 PX21): l'arco, la fotografia del committente come servita, la porta interna, i tre gradini e la chiave fuori dalla serratura, posata di fianco sulla soglia; ferma — nessuna luce, nulla si muove, il moto ridotto è la stessa immagine —, mai specchiata (il palcoscenico è `direction: ltr`), mentre il suo posto segue la pagina: compatta sopra l'etichetta sotto 64rem, al bordo di lettura, e da 64rem nel posto finale della testa, accanto a ciò che è successo e a ciò che si può fare; l'arco, non la sua scatola, sul bordo; sulla carta nessuna ombra. Le pagine del conto non la caricano (V5.8: il CSS di una superficie dove serve); 400 e 500 la disegnano con soli file statici, autosufficienti |
| `apps/forum/static/forum/forum.css` | `templates/forum/index.html`, `templates/forum/register.html`, `templates/forum/register_done.html` | conforme: un elenco di import — la pagina dell'interno pubblico (`static/css/v5/_pagina.css`: la traccia, la testa, i capitoli, il registro e gli slot condivisi di D26, disegnati una volta per le pagine di W3-F1 e per quelle di contenuto di W3-F2 — consolidati da W3-F1 alla sua fusione, 12 ottobre 2026: V5.8, un componente, un disegno), poi la grammatica propria dell'interno pubblico V5.4 (W3-F1, 11 ottobre 2026), il partial `static/css/v5/_interior.css`, importati nel foglio di pagina — mai in `main.css` (piano §2.3) — e scritto, come ogni import, nell'albero raccolto: la traccia (i suoi link su scatole di 24 px, il bersaglio di 44 sotto un puntatore grossolano senza una riga più alta — SP-8; i link in avanti dei capitoli su scatole di `--hit-min`); l'ingresso «l'ingresso» (il nome dello spazio, l'h1 e l'attacco al bordo di lettura; nel posto finale, su una porta, la carta della porta «la porta», con la via d'ingresso della porta — `static/css/v5/_porta.css`, importato dai soli fogli delle porte —, sulla prima pagina del questionario la sua scheda d'azione, su una pagina lunga «Sommaire de la page», un link per riga a ogni larghezza); i capitoli della home (una testa al bordo di lettura col segno dei tre gradini, sticky da 75rem, un corpo); il registro (righe su filetti, la riga intera è il bersaglio, nessun glifo né freccia); gli slot di D26 (un riquadro, un'azione — la scheda d'azione —, l'host di un link d'autorità, didascalia e credito sotto ogni fotografia, «Besoin d'aide ? Écrivez-nous :» col solo testo vivo); il francese prescritto sulla pagina araba nella propria direzione (una testa finisce sul bordo di lettura; un attacco di più righe tiene il proprio inizio, in una scatola sul bordo di lettura non più larga delle sue parole). Tre raggi a schermo (6 piegato sul 6 della cromatura, 4, pieno); nessun movimento — e `_forum.css`: l'ingresso sulla notte (l'unico capitolo notturno sopra quello del piè di pagina, RH-8) con l'indice della pagina, il programma come documento (PX15: una colonna degli orari solo quando ogni riga ha un orario, altrimenti righe numerate 01 … 08 e l'orario di una riga detto nelle sue parole), la tribuna come registro (PX16), il modulo d'iscrizione sul suo foglio (campi «la lastra» a 16 px) e l'unica azione «Participer et collaborer». Le pagine della governance del Forum Permanente stanno nella console e non caricano nulla di qui Dalla fusione di W3-D (12 ottobre 2026) «la linea» non è più del partial (è il passaggio pubblico `static/css/v5/_journey-passage.css`, §11.9): queste pagine non la disegnano e non la caricano. |
| `apps/orientation/static/orientation/wizard.css` | `templates/orientation/start.html`, `templates/orientation/step.html`, `templates/orientation/result.html`, `templates/orientation/resume.html`, `templates/orientation/save_unavailable.html` | conforme: il foglio di pagina del questionario (V5.4, W3-F1 secondo passo, 11 ottobre 2026) — tre import, la pagina dell'interno pubblico (`static/css/v5/_pagina.css`, condivisa con le pagine di contenuto di W3-F2), la grammatica propria di W3-F1 (`static/css/v5/_interior.css`) e il passaggio pubblico «la linea» (`static/css/v5/_journey-passage.css`, W3-D: dalla fusione di W3-D, 12 ottobre 2026), scritti nell'albero raccolto, poi le regole del questionario sui componenti di base di `static/css/v5/`: la prima pagina (l'ingresso con l'unico riquadro «À lire avant de commencer» sotto l'attacco e l'unica azione — la scheda d'azione con «Commencer» — nel suo posto finale da 64rem, subito dopo il riquadro su un telefono; poi i tre momenti su «la linea»); il passo (il titolo compatto della pagina — la sua frase è detta una volta, sulla prima pagina —; il progresso come registro quieto — «Question n sur N au maximum» a parole, mai una percentuale né un `<progress>` (FM12) — sopra una linea di 2 px sul suo filetto, piena dal bordo di lettura; la domanda come legenda; «Pourquoi cette question ?» come divulgazione nativa; le scelte come lastre intorno ai controlli nativi di `v5/field.css`, 24 px, l'intera lastra il bersaglio; l'errore a parole accanto al suo segno, collegato al gruppo con `aria-describedby` e `aria-invalid`, i bordi delle lastre raddoppiati nell'inchiostro del rifiuto — mai il colore da solo; UNA primaria, «Continuer», prima nel DOM, poi «Précédent», dopo un filetto, parte della pagina); la pre-valutazione (il banner informativo nell'ingresso sotto l'h1, l'unico riquadro; la famiglia di percorsi come riga di registro; la lista indicativa, i suoi «Points d'attention» sul bordo spezzato dell'avvertimento; la nota del documento — l'avvertimento, il riferimento, la data, le due versioni —; sulla pietra il codice di ripresa mostrato una volta, nel registro dell'avvertimento, e le azioni). Tre raggi a schermo (4, pieno e il 6 della cromatura); nessuna ombra a riposo; nulla si muove da sé (le durate sono token, 0 ms in movimento ridotto e da tastiera); il francese prescritto sulla pagina araba nella propria direzione, una domanda e una scelta finiscono sul bordo di lettura |
| `apps/orientation/static/orientation/wizard.js` | `templates/orientation/step.html`, `templates/orientation/result.html` | modulo ES: mostra il bottone di stampa (`.js-print`, nascosto senza JS) e tiene il modello di tastiera del questionario (W3-F1, secondo passo): ogni risposta è un invio e una pagina nuova, quindi un passo raggiunto DAL questionario stesso («Commencer», «Continuer», «Précédent», una risposta rifiutata — il referrer è una sua pagina) mette il focus sulla nuova domanda, la legenda del gruppo, invece di lasciarlo in cima al documento; un passo aperto altrimenti tiene l'inizio del browser. Lo stesso dopo uno swap HTMX — HTMX non è incluso nel progetto: oggi quel ramo non scatta mai e il wizard funziona con ricariche complete |

---

## 3. Token (`static/css/tokens.css`)

105 custom property su `:root`. **La separazione dei prefissi è deliberata**: i cinque compiti
strutturali del colore hanno ciascuno il proprio prefisso (`--paper*`, `--ink*`, `--navy*`,
`--rubric*`, `--cooperation`), i filetti sono `--rule-*`, gli stati `--state-*`, la scala `--t-*`,
lo spazio `--s-*`. Un token `--t-*` è sempre una dimensione tipografica e non è mai un colore.

Colonne: *Valore* = dichiarazione letterale nel file (fascia `xs`, quando la fascia conta);
*Risolto* = valore finale (esadecimale per gli alias `var()`, px per le dimensioni, con l'indicazione
della fascia dove il token scatta ai breakpoint). «riserva» = token definito che
**nessun foglio di `static/css/` consuma** — compreso lo shim di §17; un foglio di un'app può già usarlo, ed è a questo
che serve una riserva: non rimuovere, non duplicare. Il test
`tests/frontend/test_design_docs.py::test_reserve_labels_match_the_design_system_stylesheets`
verifica l'etichetta nei due sensi.

### 3.1 GROUND — le tre superfici calde (`--paper*`, `--surface-input`)

Tre fondi, e nessun quarto. Il cambio di fondo **è** la composizione: nessuna pagina esce con un solo fondo (§4.2).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--paper` | `#faf7f0` | — | il fondo della pagina: il sito spiega |
| `--paper-deep` | `#f0ebe0` | — | il processo: passi, moduli, procedure, intestazione del fascicolo |
| `--paper-edge` | `#e4ded0` | — | zebratura delle tabelle, riempimento dei filetti |
| `--surface-input` | `#ffffff` | — | solo i controlli di form |

### 3.2 INK — il testo (`--ink*`)

Tre inchiostri, tutti sopra 4.5:1 su ognuno dei tre fondi (§5). Non esiste un inchiostro decorativo.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--ink` | `#10161d` | — | tutto il testo corrente e tutti i titoli su carta |
| `--ink-secondary` | `#3a362e` | — | standfirst, glosse, etichette di folio |
| `--ink-muted` | `#5f584c` | — | marginalia, didascalie, crediti |

### 3.3 STRUCTURE — il navy, l'istituzione che parla (`--navy*`, `--paper-on-navy`, `--paper-muted-on-navy`)

Il navy non è «il colore del marchio»: è **una sola fascia per pagina**, quella in cui l'istituzione parla in prima persona (§4.2).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--navy` | `#0e2a47` | — | filetto della testata, la fascia verso, il footer, il filetto di banda da 2 px, la barra della piattaforma |
| `--navy-deep` | `#08182f` | — | solo la barra superiore della piattaforma |
| `--paper-on-navy` | `#faf7f0` | — | testo su navy; anche l'anello di focus inverso |
| `--paper-muted-on-navy` | `#c3cbd6` | — | testo secondario su navy; filetti su navy |

### 3.4 ORDER — la rubrica (`--rubric*`)

Il rosso marca **l'ordine e nient'altro**: è ciò che il rosso significa nei registri giuridici e amministrativi da prima della stampa. Ordinali, filetto dell'elemento corrente, filetto di testa di un registro, marcatori delle fonti, richiami superiori nel margine.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--rubric` | `#a4231b` | — | ordinali e filetti d'ordine su carta — sicuro come testo a qualunque corpo (6.92:1) |
| `--rubric-on-navy` | `#d9705c` | — | filetto d'ordine su navy — **solo filetto, mai testo** (4.46:1) |

### 3.5 AXIS — la cooperazione (`--cooperation`)

Il verde significa *bilaterale*, mai *sì*. Esiste perché navy-Italia contro verde-Marocco sia un segnale leggibile in un diagramma a due sponde; fuori da lì non compare.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--cooperation` | `#1b6b4a` | — | la metà marocchina di un diagramma bilaterale, il Forum, il progetto pilota, i marchi dei partner |

### 3.6 RULES — quattro pesi, quattro significati (`--rule-*`)

Una linea su questo sito significa sempre qualcosa. Quattro filetti, nessun quinto: il censimento dei bordi della build respinta restituiva quattro valori diversi per «una linea», nessuno dei quali voleva dire niente.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--rule-hair` | `#d8d1c4` | — | 1 px — ritmo fra righe dello stesso tipo, non semantico |
| `--rule-ink` | `#8c8374` | — | 1 px — un confine strutturale (fine di una zona, sotto la testata) |
| `--rule-band` | `var(--navy)` | `#0e2a47` | riserva — 2 px, apre una banda e chiude una lastra; consumato quando `components.css` sarà migrato |
| `--rule-order` | `var(--rubric)` | `#a4231b` | riserva — 2 px, l'elemento corrente e la testa di un registro; stessa attesa |

### 3.7 STATE — cinque terne, nessun verde (`--state-*`)

Ogni stato è una terna fg / bg / border: fg ≥ 4.5:1 sul proprio bg, border ≥ 3:1 sul fondo di pagina (§5). **`--state-done-*` è blu, non verde**: un passo concluso è un fatto sul fascicolo, non un verdetto.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--state-done-fg` | `#1e4a85` | — | testo di «TRASMESSO / CHIUSO» — deliberatamente identico a info |
| `--state-done-bg` | `#e8edf4` | — | fondo dello stato concluso |
| `--state-done-br` | `#5f84b5` | — | bordo dello stato concluso |
| `--state-info-fg` | `#1e4a85` | — | testo informativo |
| `--state-info-bg` | `#e8edf4` | — | fondo informativo |
| `--state-info-br` | `#5f84b5` | — | bordo informativo |
| `--state-warn-fg` | `#7a4e00` | — | testo di avvertenza |
| `--state-warn-bg` | `#faf0df` | — | fondo di avvertenza |
| `--state-warn-br` | `#a88232` | — | bordo di avvertenza (3.32:1: `#b08a3c` era caduto a 2.998 quando il fondo si è spostato) |
| `--state-error-fg` | `#8f1d1d` | — | testo d'errore, asterisco dei campi obbligatori, bordo del campo in errore |
| `--state-error-bg` | `#f8e7e5` | — | fondo d'errore |
| `--state-error-br` | `#c4635f` | — | bordo d'errore |
| `--state-pending-fg` | `#5e4b14` | — | testo «in attesa» (modulo non disponibile, moderazione) |
| `--state-pending-bg` | `#f4eedc` | — | fondo in attesa |
| `--state-pending-br` | `#a08a46` | — | bordo in attesa |

### 3.8 FAMILIES — le cinque facce (`--font-*`)

Dettagli, licenze e file in §6.1 e §6.2.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--font-display` | `"Newsreader", "Iowan Old Style", "Palatino Linotype", Georgia, serif` | — | display e testo corrente latino: **il corpo del testo è nel serif** |
| `--font-ui` | `"Fira Sans", "Segoe UI", system-ui, -apple-system, sans-serif` | — | interfaccia latina: bottoni, navigazione, etichette, celle di tabella |
| `--font-ref` | `"Fira Mono", ui-monospace, "Cascadia Mono", Consolas, monospace` | — | codici di riferimento e numeri di pratica; sostituisce `--font-mono`, dichiarato e mai caricato |
| `--font-display-ar` | `"Noto Naskh Arabic", "Newsreader", serif` | — | display e testo corrente arabo |
| `--font-ui-ar` | `"IBM Plex Sans Arabic", "Fira Sans", sans-serif` | — | interfaccia araba |

### 3.9 SCALA — dieci ruoli più l'ordinale (`--t-*`)

I valori in tabella sono quelli della fascia `xs` (320–429 px). Le dimensioni display **scattano** a ogni breakpoint (§6.5): niente `clamp()`, perché l'interpolazione fluida è ciò che ha appiattito la gerarchia precedente. Il corpo del testo non cambia mai dimensione: cambia solo la misura. Ogni interlinea è un multiplo di 4 px (`tests/frontend/test_static_assets.py::test_every_line_height_is_a_multiple_of_four`).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--t-plate-size` | `40px` | 40 px | la sola riga display di una pagina |
| `--t-plate-lh` | `44px` | 44 px | interlinea della lastra |
| `--t-title-size` | `32px` | 32 px | H1 di pagina |
| `--t-title-lh` | `40px` | 40 px | interlinea del titolo |
| `--t-band-size` | `28px` | 28 px | H2 di sezione |
| `--t-band-lh` | `36px` | 36 px | interlinea della banda |
| `--t-entry-size` | `20px` | 20 px | H3, titolo di un'entrata |
| `--t-entry-lh` | `28px` | 28 px | interlinea dell'entrata |
| `--t-lead-size` | `19px` | 19 px | standfirst |
| `--t-lead-lh` | `28px` | 28 px | interlinea dello standfirst |
| `--t-prose-size` | `17px` | 17 px | testo corrente — **non cambia mai fra i breakpoint** |
| `--t-prose-lh` | `28px` | 28 px | interlinea del testo corrente (32 px in arabo) |
| `--t-gloss-size` | `15px` | 15 px | testo secondario dentro un'entrata |
| `--t-gloss-lh` | `24px` | 24 px | interlinea della glossa (28 px in arabo) |
| `--t-caption-size` | `13px` | 13 px | marginalia, didascalie, crediti |
| `--t-caption-lh` | `20px` | 20 px | interlinea della didascalia |
| `--t-ui-size` | `15px` | 15 px | bottoni, navigazione, etichette, celle di tabella |
| `--t-ui-lh` | `20px` | 20 px | interlinea dell'interfaccia |
| `--t-folio-size` | `13px` | 13 px | titolo corrente ed etichette maiuscole — l'unico registro tracciato |
| `--t-folio-lh` | `16px` | 16 px | interlinea del folio |
| `--t-numeral-size` | `22px` | 22 px | l'ordinale del rail (44 px a `xl`) |
| `--t-numeral-lh` | `24px` | 24 px | interlinea dell'ordinale |

### 3.10 TRACKING — sei valori, ognuno legato a un ruolo (`--track-*`)

L'unico `--tracking-tight: -0.01em` applicato su tutto l'intervallo 12–64 px e su entrambe le casse è cancellato. In arabo ogni tracking è azzerato a livello di token, non con una lista di regole per componente (§15.1).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--track-plate` | `-0.02em` | — | la lastra |
| `--track-title` | `-0.015em` | — | l'H1 |
| `--track-band` | `-0.01em` | — | l'H2 |
| `--track-normal` | `0` | — | tutto il resto: zero |
| `--track-folio` | `0.08em` | — | il folio: l'unico oggetto a maiuscole tracciate del sistema (0 in arabo) |
| `--track-caps-display` | `0.03em` | — | riserva — una lastra in maiuscolo, al massimo una per pagina (0 in arabo); il suo ultimo consumatore, la regola dei titoli prescritti in maiuscolo di `register.css` sul titolo della testata di pagina, che la pagina dell'interno pubblico (`v5/_pagina.css`, `--track-display-caps`) e la cornice della console ridisegnano, è uscito da `register.css` col passo di bilancio di W3-F1 (12 ottobre 2026) |

### 3.11 SPACE — unità di base 4 px (`--s-*`)

Una sola lista, nessun valore fuori da essa. I passi 5, 7, 9, 10, 20 non esistono: è una scelta, non una dimenticanza. Lo spazio *fra* le sezioni è sempre maggiore dello spazio *dentro* le sezioni (§3.12).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--s-1` | `4px` | 4 px | l'unità |
| `--s-2` | `8px` | 8 px | passo della griglia |
| `--s-3` | `12px` | 12 px | passo della griglia |
| `--s-4` | `16px` | 16 px | passo della griglia |
| `--s-6` | `24px` | 24 px | passo della griglia |
| `--s-8` | `32px` | 32 px | passo della griglia |
| `--s-12` | `48px` | 48 px | passo della griglia |
| `--s-16` | `64px` | 64 px | passo della griglia |
| `--s-24` | `96px` | 96 px | passo della griglia |
| `--s-32` | `128px` | 128 px | riserva — il passo più alto, per una lastra a piena altezza |

### 3.12 RANK — lo spazio esterno è funzione del rango (`--rank-*`)

Quattro ranghi: **A** lastra, **B** spread (titolo + prosa + margine), **C** registro, tabella, sequenza, **D** notice, fascia marginale, testo legale. La build respinta usava 72/72 su ogni sezione a 1440 e 80/80 a 1920: sei battute di durata identica.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--rank-a-after` | `var(--s-12)` | 48 px a `xs`, 96 px da `lg` | spazio dopo una lastra (che non ha padding interno) |
| `--rank-b-block` | `var(--s-12)` | 48 px a `xs`, 96 px da `lg` | padding verticale di una sezione di rango B — è anche il default di `.section` |
| `--rank-c-block` | `var(--s-8)` | 32 px a `xs`, 48 px da `lg` | riserva — padding verticale di una sezione di rango C; i suoi ultimi due consumatori, `.section--c` e `.section--tight`, regole che nessun template disegnava, sono usciti da `layout.css` con W2-A e W3-F1 (12 ottobre 2026) |
| `--rank-d-block` | `var(--s-6)` | 24 px a `xs`, 32 px da `lg` | padding verticale di una sezione di rango D |

### 3.13 GRID e contenitori (`--grid-*`, `--container*`)

Sei fasce nominate, ognuna **progettata**, non derivata dal reflow (§7.2). Il contenitore cresce a ogni fascia sopra i 1200 px invece di convertire ogni pixel in margine.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--grid-columns` | `4` | 4 a `xs`, 6 a `sm`, 12 da `md` | riserva — il numero di colonne della fascia, dichiarato per i layout futuri |
| `--grid-gutter` | `12px` | 12 / 16 / 24 px | gutter della fascia; è anche il canale vuoto fra contenuto e margine |
| `--grid-margin` | `20px` | 20 / 24 / 40 px | margine esterno; `padding-inline` di `.container` |
| `--container` | `100%` | 100% fluido, poi 1176 / 1320 / 1440 px | larghezza massima di `.container` |
| `--container-rail` | `0px` | 0 px sotto `lg`, poi 176 / 200 / 220 px | larghezza del rail del folio; a 0 il folio è una linea orizzontale |

### 3.14 MEASURE — l'interlinea è legata alla misura (`--measure-*`, `--width-form`)

L'interlinea non è legata a un nome di stile ma alla misura della riga (§6.6). Tetto assoluto: 68 caratteri, nessuna eccezione.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--measure-prose` | `68ch` | 68ch | testo corrente — tetto rigido |
| `--measure-lead` | `45ch` | 45ch | standfirst e intestazioni di sezione |
| `--measure-gloss` | `50ch` | 50ch | glossa dentro un'entrata |
| `--measure-note` | `34ch` | 34ch | nota marginale |
| `--width-form` | `528px` | 528 px | riserva — larghezza dei moduli, account e login; consumata quando i form saranno migrati |

### 3.15 RADIUS ed elevazione (`--radius-*`, `--shadow-surface`)

Raggio 0 con due eccezioni, entrambe funzionali. Elevazione: nessuna. Tutto si separa con un filetto o con un cambio di fondo (§9).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--radius-control` | `2px` | 2 px | perché un controllo si legga come un controllo: bottoni e campi |
| `--radius-marker` | `50%` | — | riserva — il cerchio del marcatore di passo; lo stepper non è ancora migrato |
| `--shadow-surface` | `0 8px 32px rgb(14 42 71 / 0.18)` | — | riserva — l'unica ombra del sistema, per le due superfici che galleggiano davvero (drawer e `dialog`); oggi quei due componenti usano ancora i token d'ombra dello shim, che valgono `none` |

### 3.16 MOTION (`--motion-*`, `--ease-out`)

Tre durate e una sola curva. `prefers-reduced-motion: reduce` le azzera in blocco (§3.19, §12).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--motion-fast` | `120ms` | — | livello 1, stato: chevron, filetto `aria-current`, checkbox, pressione |
| `--motion-base` | `200ms` | — | livello 2, superficie: drawer, pannello del mega-menu, dialog |
| `--motion-slow` | `320ms` | — | livello 3, il segno: il filetto rubrica che si disegna una volta sola |
| `--ease-out` | `cubic-bezier(0.2, 0, 0, 1)` | — | la curva d'uscita, unica in tutto il sistema |

### 3.17 Z-INDEX — cinque livelli, nominati (`--z-*`)

Nessun numero magico nei componenti: un livello o è in questa lista o non esiste.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--z-base` | `0` | — | riserva — il piano della pagina |
| `--z-sticky` | `10` | — | sommario di pagina e sotto-navigazioni sticky |
| `--z-header` | `20` | — | la testata |
| `--z-drawer` | `30` | — | riserva — il drawer di navigazione e il suo velo stavano qui; il foglio che li sostituisce (W2-C2, §11.2) è un pannello del sistema di overlay, sul piano di `--z-modal` |
| `--z-dialog` | `40` | — | il dialog, e il livello più alto della lista: lo shim vi fa risolvere `--z-modal` e `--z-skiplink`, così il dialog senza JavaScript e lo skip link stanno sopra tutto (§17) |

### 3.18 CHROME — una sola misura, calcolata in CSS (`--chrome-*`)

`--chrome-block-size` è calcolata in CSS da `--chrome-utility` più `--chrome-masthead` e oggi ha due consumatori: `scroll-padding-block-start` in `base.css` e `--nav-drawer-top` nello shim, cioè il bordo superiore del drawer. Il velo del drawer non la consuma ancora, ed è esattamente la causa di G-23. L'obiettivo è che nessun JavaScript scriva geometria su un elemento di cui hanno bisogno anche i suoi fratelli.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--chrome-utility` | `32px` | 32 px | la barra istituzionale |
| `--chrome-masthead` | `64px` | 64 px a `xs`/`sm`, 72 px da `md` | la testata |
| `--chrome-block-size` | `calc(var(--chrome-utility) + var(--chrome-masthead))` | 96 px a `xs`/`sm`, 104 px da `md` | l'altezza reale della cromatura, calcolata in CSS |

### 3.19 Override contestuali

| Contesto | Token ridefiniti | Effetto |
|---|---|---|
| `:root:lang(ar)`, `:root[dir="rtl"]` | `--font-display` → `var(--font-display-ar)`; `--font-ui` → `var(--font-ui-ar)`; `--t-prose-lh` 32px; `--t-gloss-lh` 28px; `--t-entry-lh` 32px; `--track-folio` 0; `--track-caps-display` 0 | L'arabo ha la sua coppia display/testo, come il latino: un vero Naskh per la lettura, un sans di costruzione kufica per l'interfaccia. Il Naskh ha bisogno di spazio per i segni diacritici, quindi l'interlinea si apre e le dimensioni **non** si riducono. Ogni tracking è azzerato **a livello di token**, non con una lista di regole per componente: è una garanzia più stretta di un elenco mantenuto a mano (§15.1) |
| `@media (prefers-reduced-motion: reduce)` | `--motion-fast`, `--motion-base`, `--motion-slow` → `0ms`; in `static/css/v5/tokens.css` ogni durata V5 (`--motion-*` e le tre durate delle molle) → `0ms`, con `html.rm` come gemello di revisione | Ogni transizione costruita sui token diventa istantanea. Lo shim propaga l'azzeramento ai nomi legacy `--duration-fast/base/slow` (§17). Dal 5 ottobre 2026 (W1-D) il moto ridotto è uno stato, non un interruttore: la rete di sicurezza universale `0.01ms !important` di `components.css` §29 è stata rimossa (resta una guardia: `.reveal`; i keyframe del mega-menu e del dialog V2 se ne sono andati con la cromatura V5 e col
sistema degli overlay), `--motion-reduced` (80 ms) vale per la sola opacità di un overlay, e il moto via script passa dall'unico cancello `static/js/src/motion.js` — `docs/ACCESSIBILITY.md` §7; test `tests/frontend/test_v5_tokens.py::test_reduced_motion_is_a_state_every_duration_lands_at_zero`, `tests/frontend/test_rm_flag_parity.py::test_the_twin_is_the_media_block_and_nothing_else` |

I cinque scatti di breakpoint di `tokens.css` (`26.875rem`, `48rem`, `75rem`, `90rem`, `100rem`) non
sono override contestuali ma la scala stessa: sono documentati in §6.5 e §7.2.

---

## 4. Colore — i cinque compiti strutturali

### 4.1 La regola

Cinque compiti. **Un colore a cui non si può assegnare uno di questi cinque non è nel sistema.**

| Compito | Colore | Significato | Dove può comparire |
|---|---|---|---|
| **INK** | `--ink` e i suoi due gradi | il testo | tutto il testo corrente, tutti i titoli su carta |
| **GROUND** | la famiglia `--paper*` | la pagina | tre superfici calde, nessuna quarta |
| **STRUCTURE** | `--navy` | l'istituzione che parla | filetto della testata, **la** fascia verso della pagina, il footer, il filetto di banda da 2 px, la barra della piattaforma |
| **ORDER** | `--rubric` | la posizione in una sequenza | ordinali, filetto dell'elemento corrente, filetto di testa di un registro, marcatori dell'elenco delle fonti, richiami superiori nel margine |
| **AXIS** | `--cooperation` | il lato marocchino | la metà marocchina di un diagramma bilaterale, il Forum, il pilota, i marchi dei partner — **e nient'altro**, così che navy-Italia contro verde-Marocco diventi un segnale leggibile |

Più le cinque terne di stato, usate solo dove uno stato esiste.

Il test è operativo: *se non sai dire quale dei cinque compiti sta facendo un segno colorato,
toglilo.* Applicato alla build che questo sistema sostituisce, quel test ha rimosso **tutte e 38** le
dichiarazioni di bronzo di `components.css`, dove un solo colore era contemporaneamente il testo
dell'eyebrow, il marcatore di navigazione attiva, il colore di default delle icone, il filetto delle
citazioni, il filetto dei notice, un punto decorativo nel selettore di lingua, la sottolineatura del
menu, il filetto superiore di un pannello, l'angolo del breadcrumb e il colore dei titoli del footer.
Nel documento ritirato quel bronzo era un principio («accento bronzo `#9a7b2f` usato solo per
filetti, numerazioni e marcatori»): la direzione A lo ha rovesciato, perché nella build reale non era
usato solo per quello.

### 4.2 Il cambio di fondo è la composizione

**Nessuna pagina esce con un solo fondo.** Tre fondi, ciascuno con un significato:

- `--paper` — il sito spiega.
- `--paper-deep` — il processo: passi, moduli, procedure, il flusso di orientamento,
  l'intestazione del fascicolo nella piattaforma (`.section--process` in `layout.css`).
- `--navy` — **l'istituzione parla**: la lastra della home, la dichiarazione del promotore, il
  disclaimer, la fascia del Forum, «ciò che la piattaforma non fa» (`.section--verso`).
  **Esattamente una fascia navy per pagina, mai due.**

Nel sistema ritirato `.section--inverse` era definita, documentata e usata **zero volte** su 169
template, così che l'unica superficie scura di qualunque pagina era il footer, che diventava per
sbaglio l'evento visivo più pesante del sito. `.section--verso` esiste per essere usata: apre con un
filetto navy da 2 px dove incontra la carta e chiude con un filetto `--rubric-on-navy` da 2 px.

Ogni cambio di fondo va accompagnato da un **cambio di misura**: una fascia navy porta un enunciato
da 44 caratteri, non un paragrafo da 68.

### 4.3 Nessun colore significa mai «approvato»

Lo stato verde di successo è eliminato da tutto il sistema, pubblico e piattaforma. La terna che
prima si chiamava `--color-success-*` oggi si chiama `--state-done-*` ed è **blu**: è, nei valori,
identica alla terna informativa, e questo è voluto — «concluso» è un'informazione, non un giudizio.
Un passo concluso si legge **TRASMESSO** o **CHIUSO**.

Non è una scelta estetica. È la stessa ragione per cui l'esito `eligible` non esiste nel modello di
dominio: questa piattaforma non approva nulla, e nessun elemento dell'interfaccia deve poter essere
letto come un'approvazione. Lo shim mappa `--color-success-*` sulla terna blu proprio perché nessun
template già scritto possa reintrodurre un verde di verdetto mentre viene migrato (§17).

### 4.4 Comportamento del contrasto

- Testo ≥ **4.5:1**. Il sistema **non usa** la riduzione a 3:1 per il testo grande: ogni token di
  testo supera 4.5:1 sul proprio fondo (§5).
- Filetti, bordi, marcatori di stato, anelli di focus: ≥ **3:1** contro la superficie **su cui sono
  disegnati**, non contro l'elemento che circondano.
- **Mai il solo colore.** Ogni stato porta una parola e, dove lo spazio lo consente, un peso di
  filetto o un glifo.
- Ogni token è definito per **entrambi** i fondi. Un componente su navy usa `--paper-on-navy` e
  `--rubric-on-navy`; non esiste una «variante inversa» improvvisata per componente.
- **Al massimo tre eventi cromatici per schermata.** Si contano, a qualunque posizione di scroll, i
  segni che non sono inchiostro, carta o filetto. Quattro significa che uno è decorazione.

### 4.5 Vietato

Nessun gradiente decorativo — le tre tratteggiature della barra di giurisdizione codificano il
responsabile e sono dichiarate in §1.4. Nessun `backdrop-filter` (l'unica eccezione residua è
dichiarata in §1.4 ed è in scadenza). Nessun glassmorphism, nessuna macchia, nessun oggetto
decorativo fluttuante. **Nessun
secondo blu**: i link sono `--ink` con una sottolineatura (`text-underline-offset: 0.18em`,
`text-decoration-color` a un mix del 45 %), mai un blu di link distinto — nel sistema ritirato
`#1e4a85` era contemporaneamente il colore dei link, il colore di un badge di stato e, a un capello,
il navy strutturale. Nessuno stato affidato al solo colore. Nessuna tinta fuori dalle cinque terne.
Nessuna rubrica come testo su navy. Nessun `--radius-pill`. **Nessun dark mode**: `color-scheme:
light` è dichiarato esplicitamente in `tokens.css` e in `base.css`, perché una palette invertita
dall'utente distrugge l'unico cambio di fondo che ha un significato — la fascia verso smetterebbe di
essere un contro-fondo e diventerebbe ordinaria. Il budget va invece al livello
`@media (forced-colors: active)`, che oggi non esiste (G-26).

---

## 5. Contrasto WCAG misurato

**Design V5 (5 ottobre 2026, W1-A).** Il contrasto che una pagina rende è quello della **cascata effettiva**, non quello
dei valori letterali di `static/css/tokens.css`: `static/css/v2/bridge.css`, `v4/tokens.css` e `static/css/v5/aliases.css`
ripuntano i nomi V1 / V2 / V4 sui valori V5, e `static/css/v5/tokens.css` chiude la cascata. La sezione ha quindi due
tabelle: **5.1** quella che le pagine rendono, ricalcolata sulla cascata effettiva; **5.2** quella dei valori letterali
V1, che documenta il primo strato e se ne va con le sue dichiarazioni (piano V5.4 §2.3, la mappa delle cancellazioni).
Requisito: **4.5** = testo normale (SC 1.4.3), **3.0** = componenti dell'interfaccia e oggetti grafici (SC 1.4.11).

### 5.1 La cascata effettiva (design V5)

`tests/frontend/test_v5_tokens.py` legge la cascata come il browser — i fogli di `static/css/main.css` in ordine, vince
l'ultima dichiarazione su `:root` di primo livello — e ricalcola **502 coppie** costruite dalle famiglie di token
(`tests/frontend/test_v5_tokens.py::test_contrast_on_the_effective_cascade`), con 0 coppie sotto la soglia: ogni testo su
ogni carta e su ogni notte, la parola, la marca e il bordo di ognuno degli otto registri sul proprio corpo, sulle carte,
sul lavaggio della selezione e sulla superficie disabilitata, gli avvisi, l'anello di fuoco su ogni fondo, il vetro, le
lastre, i primari, le linee, i nodi, le scadenze, il sigillo. Uno strato traslucido è composto sul suo fondo prima del
calcolo (`--glass-light` su `--p-notte-900`): è ciò che l'occhio incontra. Le regole d'uso che ne derivano:

- **Il testo** tiene 4.5 su ogni carta; il più debole è `--text-3`, 5.14 sull'area (carta-100) e 5.10 sul lavaggio della
  selezione. Sulla notte `--text-on-night-3` sta su notte-900, -850 e -800 (4.73), **mai su notte-700** (4.03, D-doc-2).
- **Le quattro audience** stanno solo sulla notte e sulle fotografie, mai sulla carta: da 8.92 (Impresa) a 12.85
  (Istituzione in «argento», C8) su notte-900; Persona è sulla sabbia (O19).
- **Gli otto registri** — «I cerchi · Il registro»: conforme inchiostro, un disco pieno senza glifo (O14) · esame lapis
  (C1: nessun viola resta nella tavolozza) · neutro ardesia · attesa ambra, bordo tratteggiato · azione cotto · rifiuto
  granata, barrato · blocco grafite, `lock` · nullo cenere, bordo punteggiato. La parola tiene almeno 5.38 sul proprio
  corpo (nullo), la marca almeno 3.28 (nullo). I bordi spezzati di attesa e nullo, al passo 600, sono il loro significato
  e tengono da 3.14 a 3.96 su ogni carta (C3); il tratteggio a α 0.78 tiene 3.05 sulla marca d'ambra (C4), i puntini 3.94
  su rifiuto, il reticolo 3.59 su blocco (`tests/frontend/test_v5_tokens.py::test_the_broken_edges_and_the_hatch_reach_3_to_1`).
- **Sulla notte** le otto marche sono state risolte di nuovo sulla scala della carta rispecchiata (C5): ognuna tiene 3:1
  anche su notte-700 (la più bassa, nullo, 3.05), e nessuna delle 28 coppie è sotto 0.05 in OKLab in nessuna delle
  quattro visioni — normale, protanopia, deuteranopia, tritanopia secondo Machado 2009; la più vicina, neutro / rifiuto in
  protanopia, è a 0.052 (`tests/frontend/test_v5_tokens.py::test_the_night_marks_separate_in_four_visions`). Sulla carta
  la sola coppia sotto 0.05 è rifiuto / blocco in protanopia, portata dalla croce contro il lucchetto e dai puntini contro
  il reticolo.
- **La selezione e la superficie disabilitata** (D-doc-6): ogni parola di stato tiene 4.5 su entrambe; ogni marca tiene
  3:1 sul lavaggio della selezione (la più bassa, nullo, 3.11) e sulla superficie disabilitata (attesa, 3.05) — tranne
  nullo sulla superficie disabilitata, 2.89, esclusa per regola qui sotto.
- **L'anello di fuoco** laguna-550 tiene 3:1 su ogni carta — 3.41 sul lavaggio della selezione, il suo fondo più basso,
  3.55 sul corpo lapis di «En examen» (C1) — e laguna-400 sulla notte (6.53 anche su notte-700).
- **Il vetro** delle due barre appiccicose è a α 0.94 (C7): «Italy» del lock-up sopra l'hero notturno passa da 3.79 a
  4.62, il link a 5.39 (`tests/frontend/test_v5_tokens.py::test_the_glass_of_the_pinned_bars_is_094`).
- **I primari sono piatti** (SH-9): etichetta bianca 5.29 sul primario, 8.51 premuto; sulla notte il primario è la lastra
  di carta, inchiostro a 15.56.
- **Le linee**: `--line-structure` (3.37 sulla pagina) è il perimetro di un componente; `--line-rhythm` (1.37) è
  decorativa e non è mai il solo perimetro di un controllo; sulla notte `--line-night` tiene 3.63 su notte-900.
- **Le scadenze**: «presto» è ambra (3.96 sul bianco), «in ritardo» è cotto (5.98); il rosso non significa mai ritardo, e
  una scadenza non è mai disegnata senza il suo glifo (D-doc-3).
- I controlli disabilitati sono esenti da SC 1.4.3.

`tests/frontend/test_v5_tokens.py::test_the_design_system_2026_contrast_table_is_the_effective_cascade` pretende che ogni
riga di questa tabella sia una coppia tenuta dal test, con l'esadecimale che la cascata risolve e il rapporto ricalcolato
(tolleranza ± 0.01): il documento non può allontanarsi da ciò che una pagina rende.

<!-- contrast-v5:start -->
| Coppia | Primo piano | Sfondo | Rapporto | Requisito |
|---|---|---|---|---|
| testo corrente sulla pagina (portico) | `--text-1` #15222a | `--p-carta-50` #f4f3f0 | 14.62:1 | 4.5 |
| testo corrente sul bianco (campi, fogli della console) | `--text-1` #15222a | `--p-carta-0` #ffffff | 16.23:1 | 4.5 |
| testo secondario sulla pagina | `--text-2` #4a5a62 | `--p-carta-50` #f4f3f0 | 6.46:1 | 4.5 |
| testo terziario sull'area, il fondo più scuro della carta | `--text-3` #55646b | `--p-carta-100` #ecebe6 | 5.14:1 | 4.5 |
| testo terziario sul lavaggio della selezione | `--text-3` #55646b | `--surface-selected` #d9eef0 | 5.10:1 | 4.5 |
| link sulla pagina | `--accent-text` #0f6a72 | `--p-carta-50` #f4f3f0 | 5.69:1 | 4.5 |
| link sul lavaggio della selezione | `--accent-text` #0f6a72 | `--surface-selected` #d9eef0 | 5.24:1 | 4.5 |
| link in hover sull'area | `--accent-text-hover` #0b555c | `--p-carta-100` #ecebe6 | 7.13:1 | 4.5 |
| testo sulla notte | `--text-on-night-1` #eef1f6 | `--p-notte-900` #0b1a33 | 15.33:1 | 4.5 |
| testo secondario sulla notte | `--text-on-night-2` #b9c5d6 | `--p-notte-900` #0b1a33 | 9.94:1 | 4.5 |
| testo terziario sul livello più chiaro che gli è permesso | `--text-on-night-3` #8a9bb3 | `--p-notte-800` #16304f | 4.73:1 | 4.5 |
| laguna sulla notte (link, voce corrente) | `--accent-night` #7fd1d8 | `--p-notte-900` #0b1a33 | 9.93:1 | 4.5 |
| oro come testo sul livello notturno più chiaro | `--identity-key-night-text` #dfc176 | `--p-notte-800` #16304f | 7.66:1 | 4.5 |
| Persona (sabbia, O19) sulla notte | `--aud-persona` #e6cdb0 | `--p-notte-900` #0b1a33 | 11.34:1 | 4.5 |
| Impresa sulla notte | `--aud-impresa` #8fbfe8 | `--p-notte-900` #0b1a33 | 8.92:1 | 4.5 |
| Istituzione («argento», C8) sulla notte | `--aud-istituzione` #d9dee6 | `--p-notte-900` #0b1a33 | 12.85:1 | 4.5 |
| Università sulla notte | `--aud-universita` #a8cfc0 | `--p-notte-900` #0b1a33 | 10.21:1 | 4.5 |
| conforme (inchiostro): la parola sul suo corpo | `--tone-conforme-text` #15222a | `--tone-conforme-bg` #ecebe6 | 13.59:1 | 4.5 |
| conforme (inchiostro): la marca sul suo corpo | `--tone-conforme-mark` #15222a | `--tone-conforme-bg` #ecebe6 | 13.59:1 | 3.0 |
| esame (lapis, C1): la parola sul suo corpo | `--tone-esame-text` #1d3f82 | `--tone-esame-bg` #e6efff | 8.71:1 | 4.5 |
| esame (lapis, C1): la marca sul suo corpo | `--tone-esame-mark` #5278c1 | `--tone-esame-bg` #e6efff | 3.77:1 | 3.0 |
| neutro (ardesia): la parola sul suo corpo | `--tone-neutro-text` #434f5c | `--tone-neutro-bg` #eaeff4 | 7.23:1 | 4.5 |
| neutro (ardesia): la marca sul suo corpo | `--tone-neutro-mark` #586674 | `--tone-neutro-bg` #eaeff4 | 5.09:1 | 3.0 |
| attesa (ambra): la parola sul suo corpo | `--tone-attesa-text` #694700 | `--tone-attesa-bg` #ffeccf | 7.25:1 | 4.5 |
| attesa (ambra): la marca sul suo corpo | `--tone-attesa-mark` #aa7600 | `--tone-attesa-bg` #ffeccf | 3.42:1 | 3.0 |
| azione (cotto): la parola sul suo corpo | `--tone-azione-text` #873300 | `--tone-azione-bg` #ffe9e0 | 7.18:1 | 4.5 |
| azione (cotto): la marca sul suo corpo | `--tone-azione-mark` #aa4300 | `--tone-azione-bg` #ffe9e0 | 5.12:1 | 3.0 |
| rifiuto (granata): la parola sul suo corpo | `--tone-rifiuto-text` #830a2c | `--tone-rifiuto-bg` #ffe8e9 | 8.79:1 | 4.5 |
| rifiuto (granata): la marca sul suo corpo | `--tone-rifiuto-mark` #932039 | `--tone-rifiuto-bg` #ffe8e9 | 7.17:1 | 3.0 |
| blocco (grafite): la parola sul suo corpo | `--tone-blocco-text` #242c35 | `--tone-blocco-bg` #e2e7eb | 11.34:1 | 4.5 |
| blocco (grafite): la marca sul suo corpo | `--tone-blocco-mark` #353e49 | `--tone-blocco-bg` #e2e7eb | 8.71:1 | 3.0 |
| nullo (cenere): la parola sul suo corpo | `--tone-nullo-text` #55646b | `--tone-nullo-bg` #f1f0ec | 5.38:1 | 4.5 |
| nullo (cenere): la marca sul suo corpo | `--tone-nullo-mark` #7a868b | `--tone-nullo-bg` #f1f0ec | 3.28:1 | 3.0 |
| attesa: il bordo tratteggiato sull'area (C3) | `--tone-attesa-edge` #aa7600 | `--p-carta-100` #ecebe6 | 3.32:1 | 3.0 |
| nullo: il bordo punteggiato sull'area (C3) | `--tone-nullo-edge` #7a868b | `--p-carta-100` #ecebe6 | 3.14:1 | 3.0 |
| esame: la marca sul lavaggio della selezione | `--tone-esame-mark` #5278c1 | `--surface-selected` #d9eef0 | 3.62:1 | 3.0 |
| nullo: la marca sul lavaggio della selezione | `--tone-nullo-mark` #7a868b | `--surface-selected` #d9eef0 | 3.11:1 | 3.0 |
| attesa: la marca sulla superficie disabilitata | `--tone-attesa-mark` #aa7600 | `--surface-disabled` #e3e2dd | 3.05:1 | 3.0 |
| nullo: la parola sulla superficie disabilitata | `--tone-nullo-text` #55646b | `--surface-disabled` #e3e2dd | 4.73:1 | 4.5 |
| conforme: la marca notturna su notte-700 (C5) | `--tone-conforme-night-mark` #eef1f6 | `--p-notte-700` #1d3b5e | 10.08:1 | 3.0 |
| esame: la marca notturna su notte-700 (C5) | `--tone-esame-night-mark` #668ed8 | `--p-notte-700` #1d3b5e | 3.49:1 | 3.0 |
| neutro: la marca notturna su notte-700 (C5) | `--tone-neutro-night-mark` #93a3b2 | `--p-notte-700` #1d3b5e | 4.42:1 | 3.0 |
| attesa: la marca notturna su notte-700 (C5) | `--tone-attesa-night-mark` #b37d03 | `--p-notte-700` #1d3b5e | 3.18:1 | 3.0 |
| azione: la marca notturna su notte-700 (C5) | `--tone-azione-night-mark` #f28452 | `--p-notte-700` #1d3b5e | 4.46:1 | 3.0 |
| rifiuto: la marca notturna su notte-700 (C5) | `--tone-rifiuto-night-mark` #ffa0a8 | `--p-notte-700` #1d3b5e | 5.90:1 | 3.0 |
| blocco: la marca notturna su notte-700 (C5) | `--tone-blocco-night-mark` #c5d0dd | `--p-notte-700` #1d3b5e | 7.31:1 | 3.0 |
| nullo: la marca notturna su notte-700 (C5) | `--tone-nullo-night-mark` #858480 | `--p-notte-700` #1d3b5e | 3.05:1 | 3.0 |
| avviso informativo: la parola sul lavaggio ardesia (C2) | `--notice-info-text` #434f5c | `--notice-info-bg` #f3f5f8 | 7.66:1 | 4.5 |
| avviso informativo: il filetto sul lavaggio | `--notice-info-edge` #586674 | `--notice-info-bg` #f3f5f8 | 5.39:1 | 3.0 |
| avviso in attesa: la parola sul lavaggio lapis (C1) | `--notice-pending-text` #1d3f82 | `--notice-pending-bg` #f2f5fb | 9.22:1 | 4.5 |
| avvertenza: la parola sul lavaggio | `--notice-warning-text` #694700 | `--notice-warning-bg` #fdf4e6 | 7.70:1 | 4.5 |
| errore: la parola sul lavaggio | `--notice-error-text` #830a2c | `--notice-error-bg` #fdf2f1 | 9.36:1 | 4.5 |
| errore: il filetto sulla pagina | `--notice-error-edge` #932039 | `--p-carta-50` #f4f3f0 | 7.55:1 | 3.0 |
| anello di fuoco sulla pagina | `--focus-ring` #1d8a93 | `--p-carta-50` #f4f3f0 | 3.70:1 | 3.0 |
| anello di fuoco sul bianco | `--focus-ring` #1d8a93 | `--p-carta-0` #ffffff | 4.11:1 | 3.0 |
| anello di fuoco sul lavaggio della selezione | `--focus-ring` #1d8a93 | `--surface-selected` #d9eef0 | 3.41:1 | 3.0 |
| anello di fuoco sul corpo lapis di esame (C1) | `--focus-ring` #1d8a93 | `--tone-esame-bg` #e6efff | 3.55:1 | 3.0 |
| anello notturno sulla notte | `--focus-ring-night` #7fd1d8 | `--p-notte-900` #0b1a33 | 9.93:1 | 3.0 |
| anello notturno sul livello notturno più chiaro | `--focus-ring-night` #7fd1d8 | `--p-notte-700` #1d3b5e | 6.53:1 | 3.0 |
| «Italy» sul vetro a 0.94 sopra la notte (C7) | `--brand-green` #157a3c | `--glass-light` su `--p-notte-900` #ededec | 4.62:1 | 4.5 |
| link sul vetro sopra la notte (C7) | `--accent-text` #0f6a72 | `--glass-light` su `--p-notte-900` #ededec | 5.39:1 | 4.5 |
| testo sul vetro sopra la carta | `--text-1` #15222a | `--glass-light` su `--p-carta-50` #fbfaf8 | 15.56:1 | 4.5 |
| testo sulla lastra notturna (sulla trama della notte) | `--text-on-night-1` #eef1f6 | `--plate-night` su `--p-notte-900` #0b1a33 | 15.33:1 | 4.5 |
| C6: testo sullo scrim AA sopra un pixel bianco | `--text-on-night-1` #eef1f6 | `--scrim-photo-aa` su `#ffffff` #636c7c | 4.68:1 | 4.5 |
| C6: testo secondario sulla lastra fotografica sopra un pixel bianco | `--text-on-night-2` #b9c5d6 | `--plate-night-photo` su `#ffffff` #3c485c | 5.29:1 | 4.5 |
| C6: Impresa sulla lastra fotografica sopra un pixel bianco | `--aud-impresa` #8fbfe8 | `--plate-night-photo` su `#ffffff` #3c485c | 4.74:1 | 4.5 |
| etichetta bianca sul primario piatto | `#ffffff` | `--fill-primary` #12777f | 5.29:1 | 4.5 |
| etichetta bianca sul primario premuto | `#ffffff` | `--fill-primary-press` #0b555c | 8.51:1 | 4.5 |
| inchiostro sulla lastra di carta, il primario sulla notte | `--text-1` #15222a | `--fill-primary-night` #fbfaf8 | 15.56:1 | 4.5 |
| il primario sulla pagina (il suo perimetro) | `--fill-primary` #12777f | `--p-carta-50` #f4f3f0 | 4.77:1 | 3.0 |
| linea di struttura (perimetro di un componente) sulla pagina | `--line-structure` #7a868b | `--p-carta-50` #f4f3f0 | 3.37:1 | 3.0 |
| bordo notturno sulla notte | `--line-night` su `--p-notte-900` #667483 | `--p-notte-900` #0b1a33 | 3.63:1 | 3.0 |
| scadenza vicina (ambra) sul bianco | `--deadline-soon-mark` #aa7600 | `--p-carta-0` #ffffff | 3.96:1 | 3.0 |
| scadenza superata (cotto) sul bianco | `--deadline-overdue-mark` #aa4300 | `--p-carta-0` #ffffff | 5.98:1 | 3.0 |
| la chiave d'oro sul disco navy del sigillo | `--seal-glyph` #c39a2b | `--seal-disc` #0f2547 | 5.80:1 | 3.0 |
<!-- contrast-v5:end -->

**Coppie fuori da ogni pagina, per regola.** `PLATFORM_COLORS.md` §6.3 aveva trovato **23 coppie sotto la soglia** oltre
alle 363 del consiglio. Tre hanno ora una risposta di token e tengono: il link sul vetro sopra la notte (C7, 5.39),
Istituzione sulla lastra notturna sopra un pixel bianco («argento», C8, 5.16), Persona sulla stessa (la sabbia, O19,
4.56). Le altre venti non le compone nessuna pagina, per una regola scritta: **C6** — sopra una fotografia la lastra è
`--plate-night-photo` (α 0.80) o uno scrim, mai `--plate-night` (α 0.72), che sta solo sulla trama della notte (la
legenda dell'hero, il pannello del login); sullo scrim AA solo `--text-on-night-1`; `--text-on-night-3` non incontra mai
una fotografia — **D-doc-2** — `--text-on-night-3` mai su notte-700 — e la **superficie disabilitata** — è il fondo
di un controllo disabilitato, e un controllo disabilitato non porta stato: nessuna parola, marca o bordo di registro vi è
disegnato (in `static/css/` la consumano solo i token dei controlli disabilitati, `--btn-disabled-fill` e
`--field-bg-disabled`: il bottone e il campo disabilitati di `static/css/v5/buttons.css` e
`static/css/v5/field.css`). La tabella le elenca con il rapporto misurato;
`tests/frontend/test_v5_tokens.py::test_the_23_pairs_of_pc_6_3_are_answered` tiene la risposta di ciascuna: una coppia
con risposta di token deve tenere, una coppia esclusa deve stare qui con la sua regola, e una coppia esclusa che
arrivasse a tenere va spostata fra quelle tenute.

<!-- contrast-v5-ruled-out:start -->
| Coppia | Primo piano | Sfondo | Rapporto | Regola |
|---|---|---|---|---|
| testo secondario sulla lastra notturna sopra un pixel bianco | `--text-on-night-2` #b9c5d6 | `--plate-night` su `#ffffff` #4f5a6c | 3.99:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| laguna sulla lastra notturna sopra un pixel bianco | `--accent-night` #7fd1d8 | `--plate-night` su `#ffffff` #4f5a6c | 3.99:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| oro come testo sulla lastra notturna sopra un pixel bianco | `--identity-key-night-text` #dfc176 | `--plate-night` su `#ffffff` #4f5a6c | 3.99:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| Impresa sulla lastra notturna sopra un pixel bianco | `--aud-impresa` #8fbfe8 | `--plate-night` su `#ffffff` #4f5a6c | 3.58:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| Università sulla lastra notturna sopra un pixel bianco | `--aud-universita` #a8cfc0 | `--plate-night` su `#ffffff` #4f5a6c | 4.10:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| testo terziario sulla lastra notturna sopra un pixel bianco | `--text-on-night-3` #8a9bb3 | `--plate-night` su `#ffffff` #4f5a6c | 2.46:1 | C6 — `--text-on-night-3` non incontra mai una fotografia |
| testo terziario sulla lastra notturna sopra un pixel grigio medio | `--text-on-night-3` #8a9bb3 | `--plate-night` su `#808080` #2c3749 | 4.24:1 | C6 — `--text-on-night-3` non incontra mai una fotografia |
| il glifo d'oro del marchio sulla lastra notturna sopra un pixel bianco | `--brand-gold` #c39a2b | `--plate-night` su `#ffffff` #4f5a6c | 2.65:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| parola notturna di esame sulla lastra notturna sopra un pixel bianco | `--tone-esame-night-text` #a4c1f4 | `--plate-night` su `#ffffff` #4f5a6c | 3.82:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| parola notturna di neutro sulla lastra notturna sopra un pixel bianco | `--tone-neutro-night-text` #b2c1cf | `--plate-night` su `#ffffff` #4f5a6c | 3.79:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| parola notturna di attesa sulla lastra notturna sopra un pixel bianco | `--tone-attesa-night-text` #dcba84 | `--plate-night` su `#ffffff` #4f5a6c | 3.79:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| parola notturna di azione sulla lastra notturna sopra un pixel bianco | `--tone-azione-night-text` #edb096 | `--plate-night` su `#ffffff` #4f5a6c | 3.74:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| parola notturna di rifiuto sulla lastra notturna sopra un pixel bianco | `--tone-rifiuto-night-text` #f0acb1 | `--plate-night` su `#ffffff` #4f5a6c | 3.73:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| parola notturna di blocco sulla lastra notturna sopra un pixel bianco | `--tone-blocco-night-text` #c2ccd6 | `--plate-night` su `#ffffff` #4f5a6c | 4.28:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| parola notturna di nullo sulla lastra notturna sopra un pixel bianco | `--tone-nullo-night-text` #c1c0bc | `--plate-night` su `#ffffff` #4f5a6c | 3.83:1 | C6 — sopra una fotografia la lastra è `--plate-night-photo` o uno scrim, mai `--plate-night` |
| testo secondario sullo scrim AA sopra un pixel bianco | `--text-on-night-2` #b9c5d6 | `--scrim-photo-aa` su `#ffffff` #636c7c | 3.03:1 | C6 — sullo scrim AA solo `--text-on-night-1` |
| laguna sullo scrim AA sopra un pixel bianco | `--accent-night` #7fd1d8 | `--scrim-photo-aa` su `#ffffff` #636c7c | 3.03:1 | C6 — sullo scrim AA solo `--text-on-night-1` |
| oro come testo sullo scrim AA sopra un pixel bianco | `--identity-key-night-text` #dfc176 | `--scrim-photo-aa` su `#ffffff` #636c7c | 3.03:1 | C6 — sullo scrim AA solo `--text-on-night-1` |
| testo terziario su notte-700 | `--text-on-night-3` #8a9bb3 | `--p-notte-700` #1d3b5e | 4.03:1 | D-doc-2 — `--text-on-night-3` mai su notte-700 |
| la marca di nullo sulla superficie disabilitata | `--tone-nullo-mark` #7a868b | `--surface-disabled` #e3e2dd | 2.89:1 | superficie disabilitata — un controllo disabilitato non porta stato |
| il bordo punteggiato di nullo sulla superficie disabilitata | `--tone-nullo-edge` #7a868b | `--surface-disabled` #e3e2dd | 2.89:1 | superficie disabilitata — un controllo disabilitato non porta stato |
<!-- contrast-v5-ruled-out:end -->

### 5.2 I valori letterali di `static/css/tokens.css` (V1)

Questa tabella **non è ciò che le pagine rendono**: documenta le dichiarazioni letterali del primo strato della cascata,
che gli strati successivi ripuntano. Resta finché quelle dichiarazioni esistono — se ne vanno con la mappa delle
cancellazioni di W1-A, e la tabella con loro. Le 29 coppie di `tests/frontend/test_static_assets.py::test_wcag_contrast`
portano gli stessi nomi V1, ma quel test le ricalcola sulla **cascata effettiva**: tengono tutte, sui valori che le
pagine rendono.

Rapporti **ricalcolati dal test** a partire dai valori letterali di `static/css/tokens.css` con la
formula di luminanza relativa WCAG 2.x. **—** = elemento decorativo senza requisito.
`tests/frontend/test_design_docs.py::test_contrast_table_matches_recomputed_ratios` ricalcola ogni
riga con tolleranza ± 0.05 e verifica anche che l'esadecimale scritto qui sia quello che il token
dichiara nel file;
`tests/frontend/test_design_docs.py::test_contrast_table_covers_every_pair_locked_by_the_asset_tests`
pretende che ognuna delle 29 coppie bloccate da
`tests/frontend/test_static_assets.py::test_wcag_contrast` compaia qui **con la stessa soglia**.

Ogni figura è calcolata contro il fondo nominato sulla riga. Le terne di stato furono
**riverificate contro `--paper` `#faf7f0`** quando quel fondo si spostò (21 settembre 2026): `--state-warn-br` fu
portato da `#b08a3c` a `#a88232` perché sul nuovo fondo il vecchio valore cadeva a 2.998:1.

<!-- contrast-table:start -->
| Coppia | Primo piano | Sfondo | Rapporto | Requisito | Esito |
|---|---|---|---|---|---|
| testo corrente sulla carta | `--ink` #10161d | `--paper` #faf7f0 | 17.00:1 | 4.5 | AAA |
| testo corrente sul fondo di processo | `--ink` #10161d | `--paper-deep` #f0ebe0 | 15.30:1 | 4.5 | AAA |
| testo corrente sul bordo di tabella | `--ink` #10161d | `--paper-edge` #e4ded0 | 13.56:1 | — | n/a (decorativo) |
| testo corrente dentro un campo | `--ink` #10161d | `--surface-input` #ffffff | 18.19:1 | 4.5 | AAA |
| testo secondario sulla carta | `--ink-secondary` #3a362e | `--paper` #faf7f0 | 11.23:1 | 4.5 | AAA |
| testo secondario sul fondo di processo | `--ink-secondary` #3a362e | `--paper-deep` #f0ebe0 | 10.11:1 | — | n/a (decorativo) |
| marginalia e didascalie sulla carta | `--ink-muted` #5f584c | `--paper` #faf7f0 | 6.57:1 | 4.5 | AA |
| marginalia sul fondo di processo | `--ink-muted` #5f584c | `--paper-deep` #f0ebe0 | 5.91:1 | 4.5 | AA |
| marginalia su zebratura di tabella | `--ink-muted` #5f584c | `--paper-edge` #e4ded0 | 5.24:1 | — | n/a (decorativo) |
| navy sulla carta (titoli di struttura, bottone a filo) | `--navy` #0e2a47 | `--paper` #faf7f0 | 13.62:1 | 4.5 | AAA |
| navy sul fondo di processo | `--navy` #0e2a47 | `--paper-deep` #f0ebe0 | 12.26:1 | — | n/a (decorativo) |
| navy dentro un campo (bordo del campo a fuoco) | `--navy` #0e2a47 | `--surface-input` #ffffff | 14.57:1 | — | n/a (decorativo) |
| carta su navy (la fascia verso, il footer) | `--paper-on-navy` #faf7f0 | `--navy` #0e2a47 | 13.62:1 | 4.5 | AAA |
| carta attenuata su navy | `--paper-muted-on-navy` #c3cbd6 | `--navy` #0e2a47 | 8.91:1 | 4.5 | AAA |
| carta sulla barra della piattaforma | `--paper-on-navy` #faf7f0 | `--navy-deep` #08182f | 16.60:1 | 4.5 | AAA |
| carta attenuata sulla barra della piattaforma | `--paper-muted-on-navy` #c3cbd6 | `--navy-deep` #08182f | 10.86:1 | — | n/a (decorativo) |
| rubrica sulla carta (ordinali) | `--rubric` #a4231b | `--paper` #faf7f0 | 6.92:1 | 4.5 | AA |
| rubrica sul fondo di processo | `--rubric` #a4231b | `--paper-deep` #f0ebe0 | 6.23:1 | 4.5 | AA |
| rubrica dentro un campo | `--rubric` #a4231b | `--surface-input` #ffffff | 7.41:1 | — | n/a (decorativo) |
| cooperazione sulla carta (lato marocchino) | `--cooperation` #1b6b4a | `--paper` #faf7f0 | 6.04:1 | 4.5 | AA |
| cooperazione sul fondo di processo | `--cooperation` #1b6b4a | `--paper-deep` #f0ebe0 | 5.44:1 | — | n/a (decorativo) |
| concluso: testo su fondo | `--state-done-fg` #1e4a85 | `--state-done-bg` #e8edf4 | 7.52:1 | 4.5 | AAA |
| informazione: testo su fondo | `--state-info-fg` #1e4a85 | `--state-info-bg` #e8edf4 | 7.52:1 | 4.5 | AAA |
| avvertenza: testo su fondo | `--state-warn-fg` #7a4e00 | `--state-warn-bg` #faf0df | 6.37:1 | 4.5 | AA |
| errore: testo su fondo | `--state-error-fg` #8f1d1d | `--state-error-bg` #f8e7e5 | 7.43:1 | 4.5 | AAA |
| errore: testo sulla carta | `--state-error-fg` #8f1d1d | `--paper` #faf7f0 | 8.31:1 | 4.5 | AAA |
| in attesa: testo su fondo | `--state-pending-fg` #5e4b14 | `--state-pending-bg` #f4eedc | 7.27:1 | 4.5 | AAA |
| filetto strutturale sulla carta | `--rule-ink` #8c8374 | `--paper` #faf7f0 | 3.50:1 | 3.0 | AA (1.4.11) |
| perimetro del campo sul campo | `--rule-ink` #8c8374 | `--surface-input` #ffffff | 3.74:1 | 3.0 | AA (1.4.11) |
| filetto strutturale sul fondo di processo | `--rule-ink` #8c8374 | `--paper-deep` #f0ebe0 | 3.15:1 | — | n/a (decorativo) |
| filetto d'ordine sulla carta | `--rubric` #a4231b | `--paper` #faf7f0 | 6.92:1 | 3.0 | AA (1.4.11) |
| filetto d'ordine su navy | `--rubric-on-navy` #d9705c | `--navy` #0e2a47 | 4.46:1 | 3.0 | AA (1.4.11) |
| filetto di banda sulla carta | `--navy` #0e2a47 | `--paper` #faf7f0 | 13.62:1 | 3.0 | AA (1.4.11) |
| bordo dello stato concluso sulla carta | `--state-done-br` #5f84b5 | `--paper` #faf7f0 | 3.60:1 | 3.0 | AA (1.4.11) |
| bordo informativo sulla carta | `--state-info-br` #5f84b5 | `--paper` #faf7f0 | 3.60:1 | 3.0 | AA (1.4.11) |
| bordo di avvertenza sulla carta | `--state-warn-br` #a88232 | `--paper` #faf7f0 | 3.32:1 | 3.0 | AA (1.4.11) |
| bordo d'errore sulla carta | `--state-error-br` #c4635f | `--paper` #faf7f0 | 3.71:1 | 3.0 | AA (1.4.11) |
| bordo in attesa sulla carta | `--state-pending-br` #a08a46 | `--paper` #faf7f0 | 3.16:1 | 3.0 | AA (1.4.11) |
| filetto di ritmo sulla carta (decorativo) | `--rule-hair` #d8d1c4 | `--paper` #faf7f0 | 1.42:1 | — | n/a (decorativo) |
| zebratura di tabella sulla carta (decorativa) | `--paper-edge` #e4ded0 | `--paper` #faf7f0 | 1.25:1 | — | n/a (decorativo) |
<!-- contrast-table:end -->

Le regole d'uso V1 che derivavano da questa tabella — la rubrica come testo a qualunque corpo, `--rubric-on-navy`
solo filetto e mai testo (G-27, chiusa), il capello e il bordo di tabella decorativi, l'anello di fuoco navy a
13.62:1, il perimetro delle terne di stato verificato contro `--paper` — descrivono il primo strato, non ciò che le
pagine rendono: le regole in vigore sono quelle della 5.1. Restano vere per quel file finché le sue dichiarazioni
esistono.

---

## 6. Tipografia

**Design V5, tipo «Una voce» (5 ottobre 2026, W1-A).** Decisione: `docs/design-v5/V5_4_EXECUTION_PLAN.md` §1.1,
ratificata dal consiglio. **Una sola famiglia, Host Grotesk, per ogni ruolo latino**, pubblico e console; l'unico serif
di una pagina è **il nome**, sempre in «ILE Wordmark»; «ILE Mono» per i riferimenti; Vazirmatn per ogni ruolo arabo. I
nomi V1 / V2 / V4 delle famiglie (`--font-display`, `--font-ui`, `--f-serif`, `--font-ref` …) restano e risolvono sulle
famiglie V5 attraverso `static/css/v5/aliases.css`, così ogni pagina cambia faccia senza cambiare un template. Le regole
TY-2, TY-3, la clausola serif della legge 2 della direzione creativa e HET §0 punto 9 sono **ritirate** finché B è il
sistema (DL54-10); il test A-bis — il display di Newsreader sulla promessa e sui titoli di capitolo, alla cieca contro B —
è fissato sulla home composta (W2-E), e cambia il sistema solo alle condizioni scritte nel piano.

### 6.1 Famiglie

| Ruolo | Token | Famiglia | Licenza | Uso |
|---|---|---|---|---|
| Ogni ruolo latino | `--f-sans` (= `--font-display`, `--font-ui`, `--f-serif`) | Host Grotesk → ILE Sans Fallback (Segoe UI) → ILE Sans Fallback Arial → ILE Sans Fallback Android (Roboto) → Segoe UI → Roboto → Helvetica Neue → Arial → system-ui → sans-serif | SIL Open Font License 1.1 | titoli, corpo del testo, interfaccia, tutta la console |
| Il nome | `--f-wordmark` | ILE Wordmark (Newsreader 600, `opsz` 20, gli 11 code point di «ITALY LEGAL ENTRY™») → ILE Wordmark Fallback (Georgia) → Iowan Old Style → Georgia → serif | SIL Open Font License 1.1 | **ogni** resa del nome: il lock-up, il rail della console, la riga del nome nell'hero, la riga legale del piè di pagina. Le maiuscole sono CSS: il testo bloccato resta com'è scritto |
| Riferimenti | `--f-mono` (= `--font-ref`, `--font-mono`) | ILE Mono (il sottoinsieme di IBM Plex Mono 400, rinominato) → ILE Mono Fallback (Consolas) → ui-monospace → Cascadia Mono → Consolas → monospace | SIL Open Font License 1.1 | `code`, `kbd`, `pre`, `.t-ref`, i riferimenti di pratica e di documento, gli hash, le versioni delle regole — **e nient'altro** |
| Ogni ruolo arabo | `--f-sans-ar` (= `--font-display-ar`, `--font-ui-ar`; `--f-sans` sotto `:lang(ar)`) | Vazirmatn → Host Grotesk → ILE Arabic Fallback (Segoe UI) → Segoe UI → Geeza Pro → Noto Sans Arabic → sans-serif | SIL Open Font License 1.1 | titoli a 600 senza il fattore ×1.15, testo corrente, console; Host Grotesk subito dopo disegna le cifre occidentali e le sequenze latine |
| Il controllo «ع» | `--f-arabic-sys` | Segoe UI → Noto Sans Arabic → Geeza Pro → system-ui → sans-serif | faccia di sistema | l'unico glifo arabo di una pagina latina: un webfont per una lettera non si paga |

**Perché una voce.** I due giudizi sul tipo nella direzione V5.3 coincidono: il serif spinge la pagina verso il
registro editoriale che il committente ha rifiutato, e la promessa dell'hero chiede un grottesco. Con un grottesco
promesso, un serif sui titoli interni sarebbe una seconda voce che deve guadagnarsi il posto; la piattaforma non perde
nulla (è identica al pixel in A e in B: `TYPOGRAPHY_REVIEW.md` §3.B). Host Grotesk tiene un colore pari e caldo da 12 a 64
px, imposta il 500 sul navy senza impastarsi, ha un corsivo vero e non porta l'identità di nessuno; la sua cifra è
tabellare (giusta in console; nel testo pubblico l'occhio intorno all'«1» è il limite noto). Il premium non è affidato al
carattere: è la composizione, il palcoscenico della porta, la luce, il mestiere — il 500 sulla sola riga display, il
tracking per taglia, la spaziatura forzata a 64 px verificata sulle fotografie.

**La storia, in una riga.** V4 aveva IBM Plex Sans per l'interfaccia e Newsreader per il display e il corpo del testo
(ADR-008, superata); V5 ritira entrambi con i loro 26 file. Il nome resta Newsreader — non è stato ridisegnato né il
committente ha autorizzato a toglierlo — ma in un file di 1 748 byte che contiene soltanto le sue lettere.

Pesi disponibili: Host Grotesk variabile 400–700 (tondo) e 400 corsivo (caricato all'uso, per i titoli degli atti citati
nelle fonti; mai sul portico); Vazirmatn variabile 400–700; ILE Wordmark 600; ILE Mono 400. `font-synthesis: none` resta
dichiarato globalmente su `html` in `base.css`: **nessun falso grassetto, nessun falso corsivo, in nessuno script**. Il
peso agisce, legge e intitola: **500 per ciò che agisce** (controlli, link, schede, etichette di valore), **400 per i
valori e il testo corrente**, **600 per i titoli**; 700 solo per `strong`.

I valori della cascata effettiva (`static/css/v5/tokens.css`), tenuti da
`tests/frontend/test_v5_tokens.py::test_the_design_system_2026_css_blocks_are_the_cascade_values`:

```css
--f-sans-lat: "Host Grotesk", "ILE Sans Fallback", "ILE Sans Fallback Arial", "ILE Sans Fallback Android", "Segoe UI", Roboto, "Helvetica Neue", Arial, system-ui, sans-serif;
--f-sans-ar: "Vazirmatn", "Host Grotesk", "ILE Arabic Fallback", "Segoe UI", "Geeza Pro", "Noto Sans Arabic", sans-serif;
--f-mono: "ILE Mono", "ILE Mono Fallback", ui-monospace, "Cascadia Mono", Consolas, monospace;
--f-wordmark: "ILE Wordmark", "ILE Wordmark Fallback", "Iowan Old Style", Georgia, serif;
--f-arabic-sys: "Segoe UI", "Noto Sans Arabic", "Geeza Pro", system-ui, sans-serif;
--t-display: clamp(2.5rem, 1.94rem + 2.29vw, 4rem);
--t-display-lh: 1.0625;
--t-title: 2.25rem;
--t-title-lh: 2.75rem;
--t-band: 1.75rem;
--t-band-lh: 2.25rem;
--t-entry: 1.25rem;
--t-entry-lh: 1.75rem;
--t-lead: 1.25rem;
--t-lead-lh: 1.75rem;
--t-body: 1.0625rem;
--t-body-lh: 1.75rem;
--t-ui: 0.9375rem;
--t-ui-lh: 1.25rem;
--t-small: 0.8125rem;
--t-small-lh: 1.25rem;
--t-caption: 0.75rem;
--t-caption-lh: 1rem;
--t-folio: 0.8125rem;
--t-folio-lh: 1rem;
--t-field: 1rem;
--measure-body: 36rem;
--measure-lead: 36rem;
--measure-small: 29rem;
--u-title: 1.75rem;
--u-title-lh: 2.25rem;
--u-section: 1.25rem;
--u-section-lh: 1.75rem;
--u-card: 1.0625rem;
--u-card-lh: 1.5rem;
--u-body: 0.9375rem;
--u-body-lh: 1.5rem;
--u-ui: 0.875rem;
--u-ui-lh: 1.25rem;
--u-small: 0.8125rem;
--u-small-lh: 1.25rem;
--u-caption: 0.75rem;
--u-caption-lh: 1rem;
--u-eyebrow: 0.75rem;
--u-eyebrow-lh: 1rem;
--u-numeral: 1.75rem;
--u-numeral-lh: 2rem;
--u-ref: 0.8125rem;
--u-ref-lh: 1.25rem;
--w-body: 400;
--w-control: 500;
--w-title: 600;
--w-display: 500;
--w-strong: 700;
--w-wordmark: 600;
--track-display: -0.026em;
--track-title: -0.024em;
--track-band: -0.02em;
--track-entry: -0.012em;
--track-display-caps: 0.02em;
--track-eyebrow: 0.06em;
--track-folio: 0.06em;
--ar-title-lh: 1.4;
--ar-body-lh: 1.75;
--ar-console-lh: 1.7;
```

### 6.2 File self-hosted (`static/fonts/`, 6 file woff2, ≈ 75 KB in totale)

Ogni faccia ha il suo `unicode-range`: una pagina latina scarica Host Grotesk e il nome (e il nucleo di ILE Mono, 2.6 KB, solo se mostra
un riferimento: le cifre e le maiuscole di cui è fatto; il resto del sottoinsieme arriva solo se serve), una pagina
araba Vazirmatn, Host Grotesk e il nome. Provenienza, comandi di sottoinsieme e di
rinomina, hash: `docs/design-v5/FONTS_V5.md`.

| File | Famiglia | Peso · stile | Sottoinsieme | KB |
|---|---|---|---|---|
| `v5-host-grotesk-400-italic.woff2` | Host Grotesk | 400 · corsivo | latino fr / it / en | 13.8 |
| `v5-host-grotesk-var-400-700.woff2` | Host Grotesk | variabile 400–700 · tondo | latino fr / it / en, frecce, ≤ ≥ | 18.8 |
| `v5-ile-mono-400-ext.woff2` | ILE Mono (IBM Plex Mono, rinominato) | 400 · tondo | il resto del sottoinsieme: minuscole, punteggiatura, latino-1 | 7.1 |
| `v5-ile-mono-400.woff2` | ILE Mono (IBM Plex Mono, rinominato) | 400 · tondo | il nucleo dei riferimenti: cifre, maiuscole, `# + , - . / : _` | 2.6 |
| `v5-ile-wordmark-600.woff2` | ILE Wordmark (Newsreader, `opsz` 20) | 600 · tondo | gli 11 code point del nome | 1.7 |
| `v5-vazirmatn-var-400-700-arabic.woff2` | Vazirmatn | variabile 400–700 · tondo | arabo, più U+0020 e U+00A0 | 31.5 |

**Il budget per pagina** (piano §2.6, misurato da `TYPOGRAPHY_REVIEW.md` per il sistema B): ≤ 25 KB su una pagina
latina pubblica, ≤ 32 KB in console, ≤ 56 KB su una pagina araba — contro i 218–304 KB e i 484–525 KB di V4. ILE Mono ha
un solo posto proprio per questo: le etichette del piè di pagina, i nomi delle rive del progetto pilota, il conteggio del
questionario, le date dei percorsi e i contatori dei chip, che V2–V4 componevano nel mono, ora sono nel sans a cifre
tabellari (`static/css/v5/base.css`). Il conto per pagina è in `docs/design-v5/QA/v54/w1-a/IMPLEMENTATION_NOTES.md`.

### 6.3 Licenza

Tutte e quattro le famiglie sono distribuite con **SIL Open Font License 1.1**, e il testo di ciascuna viaggia con i file
in `static/fonts/licenses/` (Host Grotesk · Newsreader per il nome · IBM Plex Mono · Vazirmatn), richiamato
dall'intestazione di `static/css/v5/fonts.css`. Uso, incorporazione e ridistribuzione — anche in woff2 e in sottoinsiemi —
sono consentiti; i font non si vendono da soli; **un nome riservato non può essere usato per una versione modificata**.
IBM Plex dichiara il nome riservato «Plex», e un sottoinsieme è una versione modificata: per questo il file di
riferimento si chiama «ILE Mono» nella sua tabella dei nomi, conserva il copyright di IBM e la licenza, e lo dice nel
name ID 10. Host Grotesk, Newsreader e Vazirmatn non dichiarano nomi riservati; nella tabella dei nomi di Host Grotesk il
«Light» rimasto dall'istanza predefinita del master è stato corretto in «Regular», perché l'asse del file comincia a 400.
Nessuna richiesta a terzi in runtime (CSP `font-src 'self'`; lo scanner `apps/cms/forbidden.py` vieta gli host dei font
esterni; test `tests/frontend/test_layout.py::test_fonts_css_references_only_local_files_that_exist` e
`tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded`).

### 6.4 Strategia di caricamento e cancelli di QA

- `font-display: swap` su tutte le facce; `unicode-range` per faccia: il file arabo non si scarica mai su una pagina
  latina e i file latini non disegnano mai l'arabo. Vazirmatn contiene il proprio spazio (U+0020, U+00A0): una riga araba
  non prende in prestito gli spazi di Host Grotesk, e una faccia latina arrivata tardi non reimpagina il testo arabo.
- **Facce di ripiego metriche** (`size-adjust`, `ascent-override`, `descent-override`, interlinea 0), calcolate dai file
  su 626 caratteri di testo reale del prodotto: Host Grotesk contro Segoe UI (Windows), Arial (Windows, e macOS / iOS con
  le stesse metriche) e Roboto (Android, calcolato dal file, non verificato su un dispositivo); Vazirmatn contro Segoe UI;
  il nome contro Georgia; ILE Mono contro Consolas. Senza di esse la pagina dei documenti si spostava di 0.33 a uno swap
  tardivo; con esse lo spostamento resta ≤ 0.007 (`TYPOGRAPHY_REVIEW.md` §5.3). Misurato sul prodotto (5 ottobre 2026,
  ogni woff2 trattenuto 1.5 s, ripieghi di Windows): da 0.0000 a 0.0009 sulla home, il login, la dashboard e i documenti
  a 1440 e a 390, e sulle pagine arabe; fino a 0.0200 con le correzioni tolte — il cancello è 0.01 (DL54-04,
  `docs/design-v5/FONTS_V5.md` §4). Le metriche delle facce di sistema Apple
  si calcolano prima della milestone d'integrazione (piano §7).
- **Preload per scrittura** in `templates/base.html` (piano §1.1, «Loading»; PFR §0: precaricare le facce del primo
  schermo ha portato il primo compito di rendering della home francese da 350 a 221 ms). Le pagine latine precaricano
  `v5-host-grotesk-var-400-700.woff2` e `v5-ile-wordmark-600.woff2` (due preload); le pagine arabe
  `v5-vazirmatn-var-400-700-arabic.woff2`, `v5-host-grotesk-var-400-700.woff2` e `v5-ile-wordmark-600.woff2` (tre). Gli
  `href` sono i file che il bundle nomina, quindi sotto lo storage a manifest preload e `url()` sono una richiesta sola.
  **G-24, chiusa il 21/09/2026**: allora i preload LTR nominavano due file che la redirezione aveva cancellato, quindi
  ogni pagina LTR pagava due 404 e nessun preload utile. Il test confronta ogni `preload` di `templates/base.html` con i
  file realmente presenti in `static/fonts/`, così il difetto non può tornare in silenzio.
- Cancelli di QA: lo swap CLS ≤ 0.01 con i ripieghi di Windows e di Android, il budget per pagina, la spaziatura forzata
  del display a 64 px giudicata sulle fotografie a 1440 e a 390 (W1-A, scheda `type`); le misure di prestazione si fanno
  sul gemello compresso 8782, mai su un server di sviluppo.

### 6.5 La scala: otto taglie pubbliche, la console un gradino più su sui telefoni

Otto taglie pubbliche — **64 · 36 · 28 · 20 · 17 · 15 · 13 · 12** — e una sola fluida, la riga display (`clamp` 40 → 64
da 390 a 1440 px, peso 500, −0.026 em a 64, −0.02 em sotto 48rem). Il tracking segue la taglia, più grande più stretto,
e **si ferma a 20 px**: sotto, solo le maiuscole sono tracciate. Ogni interlinea sta sulla linea dei 4 px. Il corpo del
testo non cambia mai taglia fra i breakpoint. I dieci ruoli di V1 cadono sulle stesse otto taglie (`static/css/v5/aliases.css`):

| Ruolo | Classe | Taglia / interlinea | Peso, tracking |
|---|---|---|---|
| display (lastra) | `.t-plate`, la riga della promessa | 40 → 64 / 1.0625 | 500, `--track-display` |
| titolo | `h1`, `.t-title` | 36 / 44 | 600, −0.024 em |
| banda | `h2`, `.t-band` | 28 / 36 | 600, −0.02 em |
| entrata | `h3`, `.t-entry` | 20 / 28 | 600, −0.012 em |
| standfirst | `.t-lead`, `.lead` | 20 / 28 | 400, tondo (nessun corsivo) |
| prosa | `body`, `.t-prose` | 17 / 28 | 400 |
| glossa | `.t-gloss` | 15 / 24 | 400 |
| didascalia | `.t-caption`, `figcaption`, `small` | 13 / 20 | 400 |
| interfaccia | `.t-ui` | 15 / 20 | 500 |
| folio | `h4`, `h5`, `h6`, `.t-folio` | 13 / 16 | 600, `--track-folio`, maiuscolo |
| ordinale | `.t-numeral` | 28 / 32 | cifre tabulari |

**La console** tiene i suoi ruoli `--u-*` (titolo 28/36 · sezione 20/28 · scheda 17/24 · corpo 15/24 · etichetta
14/20 · meta 13/20 · didascalia 12/16 · eyebrow 12/16 · numerale 28/32 · riferimento 13/20); l'eyebrow e il contatore
salgono da 11 a 12 px. **Sotto 48rem o con un puntatore grossolano** ogni ruolo sale di un gradino — corpo 16,
etichetta 15, meta 14, didascalia 13, eyebrow 12, riferimento 14: il testo sotto i 14 px scende dal 63–67 % al 29–33 %
dei nodi, senza overflow (`TYPOGRAPHY_REVIEW.md` F2, «A+»). **Il testo digitato è a 16 px in ogni campo, a ogni
larghezza** (15 px facevano zoomare iOS). **Mai sotto i 12 px in latino, mai sotto i 14 px in arabo**: sotto `:lang(ar)`
i ruoli piccoli delle due scale salgono a 14 px.

### 6.6 Misura e interlinea

Le misure sono in `rem`, non in `ch`: una misura in `ch` dava 80 caratteri per riga nel paragrafo antifrode (lo zero di
queste facce è largo, ed è tabellare) e cambiava larghezza allo swap, perché `ch` non è corretto da `size-adjust`
(`TYPOGRAPHY_REVIEW.md` F1).

| Misura | Corpo | Interlinea | Token |
|---|---|---|---|
| ≈ 70 caratteri (prosa) | 17 px | 28 px (1.65) | `--measure-body` = `--measure-prose` = 36rem |
| standfirst | 20 px | 28 px (1.4) | `--measure-lead` = 36rem |
| glossa, testo piccolo | 15 px | 24 px (1.6) | `--measure-small` = `--measure-gloss` = 29rem |
| nota marginale | 13 px | 20 px (1.54) | `--measure-note` |

In arabo (Vazirmatn) i titoli hanno interlinea 1.4, il corpo resta sui 32 px che V1 apre per i diacritici, la console
1.7.

**Gli spazi del francese, solo sulle stringhe scritte dal team** (piano V5.4 §1.1; W2-D passo 3, DL54-41). Il francese
mette uno spazio accanto alla punteggiatura alta — prima di `: ; ! ? »`, dopo `«` — e scritto come spazio ordinario è
un punto d'a capo: sulla home, ai telefoni, una riga cominciava con « : la séquence… » e un link finiva su una
virgoletta sola. Il filtro `typo` (`apps/pages/templatetags/pages_typo.py`, `{% load pages_typo %}`) scrive quello
spazio come spazio non separabile, U+00A0 (Host Grotesk non ha U+202F), e non tocca altro. È **a richiesta** e va
applicato soltanto a variabili editoriali — i titoli, gli attacchi e le note delle sezioni della home, le stringhe
d'interfaccia del catalogo — mai a un testo prescritto: uno spazio non separabile cambia i caratteri di una stringa
bloccata, che `tests/i18n/test_locked_texts.py` confronta esattamente (disegnare il francese bloccato con gli spazi
non separabili è una decisione del committente e del legale, B1 punto 8). La regola è tenuta due volte: i template lo
applicano solo a variabili editoriali, e il filtro restituisce intatta qualunque stringa che sia un testo prescritto o
ne porti sei parole di fila (`tests/frontend/test_french_typography_w2_d.py`). Le interruzioni dentro un'inversione
verbo–pronome delle domande prescritte («reconnaît- / elle») non si correggono qui: il capitolo della trasparenza le
evita lasciando andare a capo le domande come vengono, senza bilanciarle.

### 6.7 Le maiuscole

**La capitalizzazione è una decisione CSS, mai una decisione di contenuto.** Le maiuscole vengono da tre posti soltanto:
il nome (sempre «ILE Wordmark», +0.13 em nel lock-up), l'eyebrow della console e il folio (`h4`, `h5`, `h6`, `.t-folio`:
13 px 600, `--track-folio`, `font-feature-settings: "case" 1`), e le stringhe maiuscole del contenuto bloccato. Ogni
sequenza maiuscola è tracciata (≥ +0.02 em); nessuna sequenza minuscola lo è. In arabo maiuscolo e tracking cadono
(`:lang(ar) :is(h4, h5, h6, .t-folio, .eyebrow)`), perché l'arabo non ha cassa e il tracking spezza le legature; l'enfasi
è il peso 500, mai il corsivo.

### 6.8 Cifre

`td`, `th`, `time[datetime]`, `.t-numeral`, `.t-ref`, `.folio__ordinal`, `.entry__ordinal` ricevono
`font-variant-numeric: lining-nums tabular-nums` (Host Grotesk le ha tabellari per costruzione). `code`, `kbd`, `pre` e
`.t-ref` usano ILE Mono con `slashed-zero lining-nums tabular-nums`: lo zero barrato serve sui codici di riferimento,
dove `0` e `O` devono essere distinguibili a voce. Le date, i contatori e i conteggi che V2–V4 componevano nel mono
passano al sans, con le cifre tabellari. In arabo si usano le cifre occidentali (corretto per il Marocco), isolate LTR con
`<bdi>`.

---

## 7. Griglia, breakpoint e layout

### 7.1 Contenitori

| Classe | Larghezza massima | Uso |
|---|---|---|
| `.container` | `--container` — fluido sotto 1200 px, poi 1176 / 1320 / 1440 px | il contenitore di ogni banda; `padding-inline: var(--grid-margin)` |
| `.container--read` | 42rem = 672 px | una colonna di lettura centrata, per la prosa **non annotata** |
| `.container--spread` | `--container` | un registro che occupa tutto il contenitore: il rail è vuoto e gli ordinali diventano la prima colonna della lista |
| `.container--flush` | — | azzera il padding laterale (lastre a pieno vivo) |
| `.container--wide`, `.container--narrow`, `.container--prose` | alias legacy | impalcatura di demolizione: `--wide` vale `--container`, `--narrow` e `--prose` valgono 42rem. Migrano a `--read` / `--spread` (§17) |

**Il contenitore cambia a ogni fascia sopra i 1200 px.** La build respinta si congelava a 1200 px e
convertiva ogni pixel sopra i 1440 in margine: misurato, 1200 px di contenuto a x=360 su uno schermo
da 1920, cioè il 37.5 % dello schermo come gutter morto, e lo screenshot a 1920 era lo screenshot a
1440 con i bordi bianchi più larghi. Qui 1920 rende un contenitore da 1440 e il rail si allarga a
220 px. Entrambi i sistemi di riferimento fanno così: .italia arriva a 1320 a XXL, ECL a 1368 a XL.

### 7.2 Breakpoint

Sei fasce nominate. I breakpoint sono decisioni di contenuto, non nomi di dispositivo, e ogni fascia
è **progettata**, non derivata dal reflow.

| Soglia | px | Fascia | Cosa cambia |
|---|---|---|---|
| `26.875rem` | 430 | `sm` | 6 colonne, gutter 16, margine 24; lastra 46/52, titolo 34/40, standfirst 20, ordinale 24 |
| `48rem` | 768 | `md` | 12 colonne, gutter 24, margine 40; lastra 60/64, titolo 42/48, banda 32/40, ordinale 28/32; testata a 72 px; ranghi A e B a 64 px; griglia editoriale `.col-*`; `.entrances` a 2 colonne; stepper orizzontale; timeline 4 + 4; footer a 2 colonne; `.form-row--2` |
| `56rem` | 896 | — | soglia locale di `.split` (testo / figura 7fr / 5fr) |
| `64rem` | 1024 | — | (`.layout-sidebar`, uscito col suo ultimo consumatore — W3-F2, W3-F1 —, e la navigazione locale in colonna, uscita con le sue pagine), varianti `.lg:col-*`, footer a 4 colonne, `.hide-mobile` / `.hide-desktop`; **le quattro porte entrano nella testata** (pannelli senza fotografia; «Menu» porta Forum · Projet · lingue: §11.1) |
| `72rem` | 1152 | — | `.entrances` a 4 colonne |
| `75rem` | 1200 | `lg` | **il rail del folio diventa verticale** (176 px) e il contenitore si fissa a 1176 px; lastra 76/80, titolo 48/52, banda 36/44, ordinale 40/40; ranghi A e B a 96 px, C a 48 px, D a 32 px |
| `80rem` | 1280 | — | **navigazione desktop** (le sei voci del portico e le fotografie dei pannelli al posto del drawer, bottone «Menu» nascosto), timeline a 8 in riga; fino a 90rem la testata è **compatta** — lock-up 32/17, gap 16, porte senza chevron — perché la colonna `lg` è 1096 px e le sei voci francesi col lock-up intero ne chiederebbero 1178 (§11.1) |
| `90rem` | 1440 | `xl` | contenitore 1320 px, rail 200 px; lastra 88/92, titolo 52/56, banda 38/44, ordinale 44/44; la testata riprende lock-up 38/20, gap 24 e i chevron delle porte; la targa resta la sola chiave (§11.3) |
| `100rem` | 1600 | `xxl` | contenitore 1440 px, rail 220 px; lastra 104/108; la targa mostra la parola «Espace réservé» e, con l'utente autenticato, il nome accanto al glifo (§11.3) |

Media query «solo sotto»: `max-width: 40rem` (640 px: il sistema degli overlay — il dialog e il menu diventano
sheet dal basso, un drawer modale prende tutta la larghezza, un drawer accanto alla lista si apre come sheet
modale, nessun tooltip; `static/js/src/overlay.js` legge la stessa soglia: W2-A), `max-width: 20.5rem` (328 px: il nome del lock-up sparisce e resta il solo marchio — il
nome a 14 px, 227.5 px, e il bottone «Menu» senza parola, 44 px, con 12 px fra loro non entrano nei 280 px di
contenuto di uno schermo da 320; da 329 px il nome è a schermo, dunque su ogni telefono da 340 in su, 360 e 375
compresi: W2-C1, 9/10/2026), `max-width: 23rem` (368 px: la parola «Menu» del bottone di navigazione diventa solo
per screen reader; da 369 px il nome, 12 px di gap e il bottone con la parola — 84 px, padding 8 sotto 48rem —
entrano nei 329 px della colonna; la parola sparisce *prima* che il bottone tocchi il bordo, non nel momento in
cui lo tocca), `max-width: 47.99rem` (`portal.css`: pop-in delle tabelle che portano `data-label`, §14.5 della
direzione artistica), `max-width: 47.999rem` (la barra istituzionale non è disegnata: promotore, targa e
lingue passano in testa al cassetto; il gap della testata scende a 12 px e il padding di «Menu» a 8; freccia della
pathway list nascosta), `max-width: 63.999rem` (`.hide-mobile`, navigazione locale a pastiglie, nessuno scrim del
portico), `max-width: 79.999rem` (drawer), `max-width: 89.999rem` (la fascia compatta della testata fra 80 e 90rem:
§11.1) e `max-width: 99.999rem` (la targa: sotto 1600 px la sola chiave, 32 × 32, col nome in tooltip; con l'utente
autenticato il solo glifo della persona sulla stessa targhetta; §11.3). Sotto `lg` il rail vale 0 px e il folio
diventa una linea orizzontale sopra il blocco: il dispositivo sopravvive a ogni larghezza, cambia
solo il suo asse.

**La navigazione ha due soglie proprie (64rem e 80rem), che non sono fasce della griglia.** Da 64rem le quattro
porte entrano nella testata e i loro pannelli si aprono senza fotografia; Forum, Projet e le lingue restano in
«Menu». Da 80rem la testata porta le sei voci, i pannelli la loro fotografia, e il cassetto sparisce. Le soglie
vivono in due file che devono restare allineati: `@media (min-width: 64rem)`, `@media (min-width: 80rem)` e
`@media (max-width: 79.999rem)` (drawer) in `static/css/v5/chrome.css`, e
`BAR = window.matchMedia("(min-width: 64rem)")` / `DESKTOP = window.matchMedia("(min-width: 80rem)")` in
`static/js/src/nav.js`
(`tests/frontend/test_design_docs.py::test_navigation_breakpoint_is_consistent_and_documented`).
Conseguenze: un tablet in orizzontale e un laptop da 1024–1279 px hanno le porte nella barra e «Menu» per il
resto; «mobile» in `.hide-mobile` significa «sotto 64rem», non «modalità drawer»; a 1280 px qualunque zoom del
browser oltre il 100 % riporta al drawer.

Tre fasce convivono con tre soglie ereditate (`56rem`, `64rem`, `72rem`) che appartengono al sistema
vecchio e non a una fascia della griglia. Vanno riassorbite in `md` / `lg` quando `components.css`
sarà migrato; finché ci sono, sono elencate qui perché una soglia non documentata è una soglia che
qualcuno reinventa.

### 7.3 Le tre zone

Da `lg` in su ogni banda si compone di tre zone sulla griglia a 12 colonne, in `layout.css`:

```
│ RAIL              │ CONTENT                        │ MARGIN     │
│ --container-rail  │ minmax(0, 1fr)                 │ --container-rail
│ ordinale          │ titolo, prosa, registro,       │ nota, data,
│ titolo corrente   │ tabella, sequenza              │ fonte, cautela
│ indice locale     │                                │
```

- `.zones` — la griglia. Sotto `lg` è una colonna sola; da `lg` è
  `var(--container-rail) minmax(0, 1fr) var(--container-rail)` con `gap: 0 var(--grid-gutter)` e
  `align-items: start`.
- `.zones__rail` — il folio: ordinale, filetto, titolo corrente, data o fonte.
- `.zones__content` — la colonna di lavoro; la prosa che contiene riceve `--measure-prose`.
- `.zones__margin` — la nota marginale: `--font-ui` a `--t-caption-size`, `--ink-muted`, misura
  `--measure-note`, e un `padding-inline-start` di un gutter. **Quel gutter è il canale vuoto**: è
  ciò che fa leggere il margine come un margine invece che come una seconda colonna di contenuto.
- `.zones--no-margin` e `.zones--no-rail` tolgono la terza (o la prima) zona invece di lasciare un
  vuoto: il contenuto si prende lo spazio.

**Una pagina che non ha marginalia reali non riceve questo layout**: riceve una colonna di lettura
centrata (`.container--read`). È l'innesto obbligatorio della direzione C, e serve a eliminare una
classe di difetto invece di gestirla — è esattamente il difetto che ha prodotto la colonna da 576 px
sola dentro 1200 px per 1100 px di scroll nella build respinta. La colonna non era il problema: lo
era il vuoto accanto.

Quattro rotture della griglia sono permesse, e nessun'altra; una pagina può contenerne **al massimo
due**: **PLATE** (a pieno vivo, una volta per pagina, solo sulla sezione di rango A), **SPREAD** (un
registro che occupa tutte le colonne, solo quando il rail è vuoto per quella banda), **INSET** (un
avviso che rientra, per farlo leggere come un'interruzione dentro l'argomentazione) e **MARGIN
PROMOTION** (una nota marginale senza blocco ospite, accanto a una lastra — usata per la
dichiarazione anti-frode nella home e praticamente in nessun altro posto). Una sezione che non ne fa
nessuna è una **banda standard**: la maggior parte delle sezioni sono bande standard. Le rotture sono
eventi.

### 7.4 Ritmo verticale e rango

**Unità di base 4 px. Ogni interlinea è un multiplo di 4. Ogni spazio di blocco viene da una sola
lista** (§3.11). Nessun valore fuori da quella lista, e nessuna spaziatura impilata (`margin` più
`padding` che fanno lo stesso lavoro su elementi adiacenti — regola ECL, adottata).

**Lo spazio fra le sezioni è sempre maggiore dello spazio dentro di esse**, e il rango della sezione
decide quanto:

| Rango | Tipo di sezione | Classe | `xs`/`sm` | `md` | `lg`+ |
|---|---|---|---|---|---|
| **A** | lastra | `.section--a` | 0 + 48 dopo | 0 + 64 | 0 + 96 |
| **B** | spread: titolo + prosa + margine | `.section--b`, default di `.section` | 48 / 48 | 64 / 64 | 96 / 96 |
| **C** | registro, tabella, sequenza | `.section--c` | 32 / 32 | 32 / 32 | 48 / 48 |
| **D** | notice, fascia marginale, legale | `.section--d` | 24 / 24 | 24 / 24 | 32 / 32 |

Fondi: `.section--process` (`--paper-deep`), `.section--verso` (`--navy`, testo `--paper-on-navy`,
filetto navy da 2 px in apertura e filetto `--rubric-on-navy` da 2 px in chiusura). `.section--rule` e gli
alias dell'impalcatura di demolizione `.section--tight`, `.section--muted` e `.section--inverse` sono usciti
con i loro ultimi consumatori (W3-F1, 11 ottobre 2026: le pagine dell'interno pubblico disegnano i propri
capitoli, `static/css/v5/_pagina.css`).

**Disciplina della linea di base.** La prima linea di base del titolo di una sezione, quella del suo
ordinale di folio e quella della sua prima nota marginale **si allineano**. È un solo
`margin-block-start` per zona, calcolato dalla differenza delle tre interlinee, ed è verificabile in
un test di browser. È il dettaglio artigianale che più di ogni altro dice «composto» invece che
«impaginato»; non è ancora implementato nei componenti, perché vive nel livello che si sta
riscrivendo.

**Come ogni sezione smette di sembrare identica alle altre.** Tre regole, ciascuna un test e non
un'aspirazione: (1) nessun tipo di corpo compare due volte di seguito su una pagina; (2) nessun rango
di sezione compare due volte di seguito — una pagina ha esattamente un rango A, al massimo tre ranghi
B, il resto C e D; (3) una pagina usa almeno quattro dei sei tipi di corpo (`PROSE`, `REGISTER`,
`TABLE`, `SEQUENCE`, `PLATE`, `NOTICE`) e almeno due fondi. Una home legge quindi `A-C-B-C-D-B-C` e
non `B-B-B-B-B-B`. Nella build respinta cinque sezioni di contenuto della home rendevano — misurato —
eyebrow a 12 px, poi H2 a 33.76 px / interlinea 38.82 / peso 500 / x=152 / larghezza 576, poi un lead
a 21 px: non simili, **identiche alla seconda cifra decimale**, cinque volte.

### 7.5 Angoli, ombre, controlli — la fondazione V5

**Angoli «Lo spigolo»** (piano V5.4 §1.3, DL54-14): 2 · 4 · 6 · 8 · 12 · pieno, **sui nomi esistenti**, una sola scala
per il portico e la console. `xs` gli angoli interni e gli inserti annidati · `sm` bottoni, campi, tooltip, scheletro,
checkbox, le lastre dell'hero · `md` la targa, le righe di menu, il binario segmentato · `lg` schede, pannelli, fotografie
su carta, popover · `xl` dialoghi, cassetti, fogli · `full` chip, contatori, indicatori — mai un bottone né una scheda. Gli
angoli annidati sono concentrici (il cursore 4 dentro un binario 6, a 2 px); le bande fotografiche 21 : 9 non hanno
raggio; l'arco è l'unica curva grande. **Al massimo tre raggi distinti su uno schermo a riposo** (`full` compreso, l'arco
e le bande escluse; un overlay aperto ne aggiunge uno suo): dove uno schermo ne mostrerebbe un quarto, la famiglia che lo
possiede piega il ruolo più vicino su uno già presente, nei propri file. I nomi V2 / V4 seguono: `--radius-control` (i
bottoni e i campi) vale `sm`, `--radius-tile` vale `md`.

**Ombre** (§1.4, SH-1 … SH-9): cinque livelli, ciascuno con un significato — 0 tela · 1 foglio · 2 rialzato (il NowPanel,
una scheda in hover) · 3 popover, menu, pannello del portico · 4 modale e cassetto, con uno scrim — nel colore della notte,
`rgba(7, 18, 38, α)`: mai nero, mai colorato, mai luminoso. L'alone è ritirato (`--shadow-glow` non disegna nulla), ogni
primario è piatto, il filo luminoso solo sulle lastre notturne. Il filetto prima della scatola: una riga e la navigazione
non portano ombra; un'ombra non si anima mai. **Il vetro ha un solo posto**: le due barre appiccicose, una volta
scrollate — blur 12 px, statico, α 0.94 («Italy» sull'hero notturno da 3.79 a 4.61 : 1); i pannelli in vetro di V4
prendono la lastra notturna piena, e lo scrim del modale è solo opacità.

**Controlli** (§1.8): `sm` 36 solo con un puntatore fine (barre dense della console, il binario segmentato) · `md` 44 il
predefinito, e ogni controllo sotto un puntatore grossolano · `lg` 52 i primari pubblici, i campi dei moduli pubblici, la
CTA dell'hero e del login · icona 40 con un puntatore fine, 44 con uno grossolano. Il bersaglio minimo è 24 px con un
puntatore fine, 44 sotto un puntatore grossolano e per ogni primario; W1-C applica queste misure ai componenti, e fino ad
allora il nome V4 `--hit-min` conserva il suo significato di 44 px (`static/css/v5/aliases.css`).

**Fuoco** (§1.6): un solo sistema, in `static/css/v5/base.css`. Solo `:focus-visible`: un anello `--focus-ring` di 2 px
(laguna-550) a 2 px dall'elemento, che ne segue il raggio; laguna-400 nei contesti notturni (`.on-inverse`, il rail,
l'hero, il piè di pagina, le fasce verso: `static/css/v5/tokens.css` ripunta il token, nessun selettore ripete
l'anello); due toni sulle fotografie (`.on-image`: carta dentro, notte fuori); l'alone di 5 px solo sui campi di testo;
`Highlight` nei colori forzati; mai animato. Tiene 3:1 contro entrambi i vicini su ogni fondo (§5.1). Il tratto di
200 ms che si disegna sotto un campo appartiene al campo (W1-C); `scroll-padding-block-start` resta in `base.css`,
perché il fuoco non finisca sotto una barra appiccicosa (WCAG 2.4.11). Le regole di fuoco proprie di un componente —
i bottoni, i campi, la cromatura — sono della famiglia che lo possiede.

```css
--radius-xs: 2px;
--radius-sm: 4px;
--radius-md: 6px;
--radius-lg: 8px;
--radius-xl: 12px;
--radius-full: 999px;
--shadow-1: 0 1px 2px rgba(7, 18, 38, 0.06);
--shadow-2: 0 1px 2px rgba(7, 18, 38, 0.06), 0 8px 24px -8px rgba(7, 18, 38, 0.14);
--shadow-3: 0 4px 8px -2px rgba(7, 18, 38, 0.08), 0 16px 40px -12px rgba(7, 18, 38, 0.2);
--shadow-4: 0 12px 24px -6px rgba(7, 18, 38, 0.16), 0 32px 64px -16px rgba(7, 18, 38, 0.3);
--shadow-door: 0 40px 64px -32px rgba(7, 18, 38, 0.6);
--glass-light: rgba(251, 250, 248, 0.94);
--blur-nav: 12px;
--control-sm: 36px;
--control-md: 44px;
--control-lg: 52px;
--control-icon: 40px;
--hit-primary: 44px;
--input-h: 44px;
--row-min-h: 64px;
--table-row-h: 48px;
--drawer-row-h: 64px;
--chip-h: 24px;
--segmented-h: 36px;
--rail-item-h: 44px;
--focus-ring-width: 2px;
--focus-ring-offset: 2px;
--page-pad: 32px;
--container-lg: 1176px;
--container-xl: 1320px;
--container-xxl: 1440px;
--utility-h: 32px;
--header-h: 64px;
--header-h-scrolled: 56px;
--rail-w-compact: 80px;
--rail-w-open: 248px;
```

### 7.6 Spaziatura e ritmo — le regole V5

Il piano V5.4 §1.4 rende **vincolanti** le regole che il sistema di gusto aveva proposto (`TASTE_SYSTEM.md` §5, §6),
misurate sui riferimenti e sulle sonde. La fondazione ne porta i token; le famiglie che possiedono i componenti e le
pagine le applicano, e la scala della coerenza (piano §3.1) le misura su ogni cattura.

**Spaziatura.**

- **SP-1 Una scala.** Ogni spazio fra due vicini è un passo della scala di 4 px — 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 ·
  48 · 64 · 80 · 96 · 128 (`--s-*`); fuori scala soltanto le eccezioni ottiche nominate, che sono token di componente:
  il capello (1–2 px), lo spazio di 6 px della pastiglia e i suoi 3 px dal lato della marca, il richiamo di −4 px della
  freccia. Misurato prima di V5: la home al 96–100 % sulla scala, la console al 77–83 % a 1440. La coerenza passa al
  95 % sulle pagine pubbliche e al 90 % in console; l'obiettivo, tolte le eccezioni, è il 98 %.
- **SP-2 Le cose vicine stanno vicine.** Lo spazio fra due gruppi è almeno 2.5 volte quello dentro un gruppo.
- **SP-3 Un'etichetta appartiene al suo controllo.** Etichetta sopra, 14 / 20 a peso 500, a 8 px dal controllo; 20–24
  px fra due campi; un segnaposto non rinomina mai l'etichetta.
- **SP-4 Un componente, un padding.** Pannello 24 (16 se denso); bottone 16 / 20 / 24 in linea per le altezze
  36 / 44 / 52; riga di registro almeno 64; riga di tabella 48.
- **SP-5 Le sezioni.** Capitoli pubblici 96 / 64 / 48 (desktop / tablet / telefono); in console padding di pagina
  32 / 16 e 24 fra i pannelli.
- **SP-6 Nessun resto.** Nessun intervallo non progettato sopra i 64 px dentro uno schermo composto: un grande vuoto è
  un cambio di capitolo sulla scala, o si toglie.
- **SP-7 Un telefono si ricompone, non si rimpicciolisce.** Capitoli 48, schede a 16 l'una dall'altra, padding 16; le
  taglie di lettura salgono di un gradino invece di scendere (la console: §6.5).
- **SP-8 I bersagli.** 24 px il minimo di ogni bersaglio; 44 px per le azioni primarie, i controlli dei moduli, il
  rail, le barre, le righe dei cassetti e ogni bersaglio sotto un puntatore grossolano (§7.5).

**Ritmo.**

- **RH-1 La linea dei 4 px.** Ogni interlinea è un multiplo di 4 px
  (`tests/frontend/test_v5_tokens.py::test_line_heights_sit_on_the_4px_line`,
  `tests/frontend/test_static_assets.py::test_every_line_height_is_a_multiple_of_four`).
- **RH-2 Un padding, i fondi a serie.** Un padding di sezione per pagina pubblica e uno più grande per il cambio di
  capitolo; il fondo cambia ogni due o tre sezioni, e l'allineamento di un titolo cambia solo con il fondo.
- **RH-3 Un'immagine o una figura ogni due schermi** sulla home e sulle pagine delle porte; il vuoto non si chiude mai
  con un'immagine di repertorio, una griglia di schede a glifo o una trama.
- **RH-4 Una home corta**: da 3 a 8 schermi a 1440, 9.5 al massimo a 390.
- **RH-5 Una cosa una volta**: ogni informazione importante è detta una volta, con forza; le quattro audience al massimo
  due volte nel primo schermo e mezzo; il nome è disegnato una volta.
- **RH-6 La pagina è una catena di domande**: ogni blocco risponde a quella che il precedente ha sollevato; un blocco
  senza una domanda si toglie.
- **RH-7 Un solo dispositivo di sezione, al bordo di lettura**: il micro-marchio, un'etichetta, un titolo, allineati
  all'inizio; una sola banda centrata per pagina al massimo. La console ha il suo eyebrow, non questo dispositivo.
- **RH-8 Denso, poi quieto**: dopo un blocco denso viene un blocco quieto; al massimo due capitoli notturni per pagina,
  mai adiacenti.

```css
--s-1: 4px;
--s-2: 8px;
--s-3: 12px;
--s-4: 16px;
--s-5: 20px;
--s-6: 24px;
--s-8: 32px;
--s-10: 40px;
--s-12: 48px;
--s-16: 64px;
--s-20: 80px;
--s-24: 96px;
--s-32: 128px;
--btn-pad-sm: var(--s-4);
--btn-pad-md: var(--s-5);
--btn-pad-lg: var(--s-6);
--card-pad: var(--s-6);
--card-edge: 1px solid var(--line-rhythm);
--card-shadow: var(--shadow-1);
--panel-raised-shadow: var(--shadow-2);
--menu-row-h: 36px;
```

---

## 8. Il linguaggio grafico proprio

> **Design V5 (5 ottobre 2026, W1-A)** — i sette dispositivi qui sotto sono quelli di «Le Registre». V2 ne ha superato
> la direzione (la nota prima del §2); V5 li rivaluta tutti insieme attraverso gli alias, senza cambiare un template, e
> ogni pagina resta «V4 + fondation» finché la sua famiglia non passa (piano V5.4 §2.1). Dove questo blocco e le schede
> sotto non coincidono, questo blocco è il codice:
>
> - **il nome** è disegnato in «ILE Wordmark» (Newsreader 600, `opsz` 20, gli 11 code point del nome) in ogni sua resa
>   — il lock-up, il rail della console, la riga del nome nell'hero, la riga legale del piè di pagina — con le maiuscole
>   in CSS e il testo bloccato com'è scritto (`static/css/v5/base.css`, §6.1) — non più il Newsreader 500 di «Le
>   Registre» (8.1);
> - **la rubrica non è rossa**: da V2 `--rubric` risolve all'inchiostro terziario (#55646b) e `--rubric-on-navy` al
>   testo terziario della notte (#8a9bb3), in `static/css/v2/bridge.css`. L'ordine si marca con l'inchiostro; il rosso e
>   il verde stanno solo nel marchio — nessun filetto tricolore (O57);
> - **i quattro filetti** risolvono alla carta-200 (`--rule-hair`, 1.37 sulla pagina: ritmo, decorativo),
>   all'inchiostro-400 (`--rule-ink` e `--rule-order`, 3.37: il perimetro) e al navy del marchio (`--rule-band`,
>   #0f2547);
> - **il folio**: l'ordinale a 28 / 32 (`--t-numeral-size`), in Host Grotesk a cifre tabellari; il titolo corrente e la
>   data a 13 px (`--t-folio-size`, `--t-caption-size`);
> - **l'entrata**: il titolo in Host Grotesk 600, nessun serif (DL54-10); la glossa nel sans; l'attore nel registro del
>   folio;
> - **la lastra**: il display a `clamp` 40 → 64 px, peso 500 (`--t-plate-size`);
> - **la nota marginale**: 13 px su 20 (`--t-caption-size`), misura `--measure-note` (34ch);
> - **la barra di giurisdizione**: le tratteggiature restano codifiche, non decorazioni (§1.4);
> - **gli stati** sono gli otto registri di «I cerchi · Il registro» (§5.1): i token di ogni registro, sulla carta e
>   sulla notte, sono in `static/css/v5/tokens.css` (§4.1 del file); la pastiglia stessa è della famiglia dei
>   componenti (W1-C).

Il sito deve essere riconoscibile **senza una sola fotografia**. Sette dispositivi fanno quel lavoro:
sono l'identità. Vivono tutti in `static/css/register.css`, che è il settimo layer della cascata
(§2), e sono stati spediti **presto**, non per ultimi: il monito operativo del Council è che senza di
essi una build intermedia è austera senza essere ancora distintiva, che è il posto peggiore in cui
mostrare qualcosa a un committente.

Una regola vale per tutto il file e va letta prima delle schede: **la struttura è disegnata con
`border`, `outline` o testo, mai con un `background` su uno pseudo-elemento**. È la condizione
perché il livello `@media (forced-colors: active)` in fondo a `register.css` possa restituire ogni
filetto e ogni stato con `CanvasText`, `Highlight` e `Canvas` invece di vederli sparire sotto il
contrasto elevato di Windows.

### 8.1 Il marchio e i lockup

**Il marchio** è il dispositivo del folio a 24 px: un quadrato che contiene tre filetti orizzontali di
lunghezza disuguale — lungo, corto, lungo — impilati su un ritmo di 4 px, il secondo in rubrica, gli
altri in inchiostro. Si legge come voci in un registro e, a dimensione di favicon, come un blocco
istituzionale stabile. Non è un tempio, non è una bandiera, non è una soglia, non è un passaporto: è
letteralmente la struttura della pagina stessa, che è la definizione di un'identità invece che di un
logo.

| Lockup | Contenuti | Usato a |
|---|---|---|
| A | marchio + wordmark + descrittore | ≥ 1280 px nella testata, nel footer |
| B | marchio + wordmark | 768–1279 px, barra della piattaforma |
| C | marchio da solo | ≤ 767 px, favicon, avatar, titolo corrente sticky |

Wordmark: Newsreader 500 a 22 px, `--track-title`. **Spazio di rispetto ≥ 1× l'altezza delle
maiuscole** (≈ 24 px a 1440) su tutti i lati — nella build respinta il bordo destro del wordmark
stava a x=338 e la prima voce di menu cominciava a x=343: cinque pixel. Il descrittore è a
`--t-folio-size`; in arabo il descrittore è in arabo e sta sul lato speculare, mentre il wordmark
resta latino e isolato LTR. Il `™` resta `dir="ltr" translate="no"`, in apice, circa al 55 %
dell'altezza delle maiuscole.

**Da ritirare**: la favicon attuale (tre barre verticali su una base bronzo, un'astrazione di
edificio pubblico) e il frontone di `entrance-institution.svg`, che oggi compare negli accessi della
home, nel footer e **sei volte identico** in una lista di sei voci della pagina Istituzioni (§14.1).

### 8.2 Il folio

Il segno più forte del sito, e **il sostituto dell'eyebrow**. Da `lg` in su sta nel rail; sotto `lg`
diventa una linea orizzontale sopra il blocco.

```
lg+, nel rail:                    sotto lg, orizzontale:

  03                              ─────────────────────────────────────
  ─────                           03 — LES PARCOURS RÉGULIERS — 20.09.2026
  LES PARCOURS
  RÉGULIERS
  ─────
  Révisé le
  20.09.2026
```

Ordinale a `--t-numeral-size` (44 px a `xl`) in **rubrica**, cifre tabulari. Un filetto rubrica da
24 px sotto. Il titolo corrente a `--t-folio-size`. Una data o una fonte a `--t-caption-size` in
`--ink-muted`. **L'ordinale è generato da un contatore CSS ed è presentazionale**: l'ancora è sempre
uno slug (`#parcours-reguliers`), così rinumerare non rompe mai un link.

L'eyebrow è abolito. Nella build respinta c'erano sei eyebrow su una sola home, tutti a 12 px / peso
600 / `letter-spacing: 1.44px` / bronzo / x=152 / larghezza 576, definiti una volta in `base.css` e
duplicati alla lettera in altri tre file. La classe `.eyebrow` sopravvive solo nello shim, resa nel
registro del folio e **in inchiostro, non in rubrica** — perché l'unico compito della rubrica è
l'ORDINE, e un eyebrow non è una posizione (§17).

*Implementazione.* `.folio` (`register.css`) è un `flex` allineato sulla linea di base, aperto da un
filetto rubrica da 2 px, con `.folio__ordinal` a `--t-numeral-size` in rubrica e cifre tabulari,
`.folio__head` nel registro del folio e `.folio__date` a `--t-caption-size`. Da `75rem` in su,
dentro `.zones__rail`, diventa una colonna: l'ordinale va a capo sopra il filetto e il titolo
corrente sotto. Il contatore è di pagina — `.page-home main { counter-reset: folio }` e
`.page-home .section .folio__ordinal::before { counter-increment: folio }` — quindi le sezioni si
numerano da sole e il back-office può riordinarle senza rompere un link che qualcuno ha salvato.
Dentro una fascia verso il **filetto** del folio passa a `--rubric-on-navy` mentre l'ordinale
passa a `--paper-on-navy` e il titolo corrente a `--paper-muted-on-navy`: la rubrica su navy è un
filetto e non è mai il colore di un testo (§5).

### 8.3 I quattro filetti del registro

Quattro pesi, quattro significati, nessun quinto. **Una linea su questo sito significa sempre
qualcosa.**

| Filetto | Peso e colore | Significato |
|---|---|---|
| capello | 1 px `--rule-hair` | ritmo fra righe dello stesso tipo |
| inchiostro | 1 px `--rule-ink` | un confine strutturale (fine di una zona, sotto la testata) |
| banda | 2 px `--navy` (token `--rule-band`) | apre una banda; chiude una lastra |
| ordine | 2 px `--rubric` (token `--rule-order`) | l'elemento corrente; la testa di un registro |

Il censimento dei bordi di una sola pagina della build respinta restituiva navy 1 px su 32 elementi,
`#c4cad1` 1 px su 29, `#dde1e5` 1 px su 17 e bronzo 2 px su 5: quattro valori per «una linea», nessuno
dei quali significava nulla.

### 8.4 L'entrata

L'oggetto atomico di contenuto. **Sostituisce la card ovunque.**

```
──────────────────────────────────────────────────────────────  1px capello
 01   Travail salarié                            ENTREPRISE   →
      entrées pour travail dans le cadre des quotas annuels
──────────────────────────────────────────────────────────────
 02   Travail qualifié — Carte bleue européenne  ENTREPRISE   →
      pour les profils hautement qualifiés, sur la base d'un titre
──────────────────────────────────────────────────────────────
```

Anatomia: ordinale in rubrica (tabulare, da contatore CSS) · titolo `.entry__title` nel serif ·
glossa `.entry__gloss` nel sans · **attore responsabile** `.entry__actor` nel registro del folio ·
freccia. Tutta la riga è un solo bersaglio, `min-block-size: 104px`. Le righe possono avere altezze
diverse: si allineano sul loro filetto superiore, mai su una griglia di base forzata. Hover e focus:
l'ordinale passa a `--rubric` e compare un filetto rubrica da 2 px sul bordo d'attacco della riga.
Nessun cambio di fondo, nessuna ombra, nessun sollevamento.

*Implementazione.* `.register` è una lista senza marcatori chiusa fra due filetti navy da 2 px, con
`counter-reset: entry`; `.register__item + .register__item` porta il capello da 1 px fra le righe.
`.entry` è una griglia a tre colonne con **aree nominate** (`ordinal` / `title` `gloss` `actor` /
`arrow`) dichiarate a ogni larghezza: un elemento assegnato a un'area che il template non dichiara
finisce in una riga implicita, ed è ciò che aveva allungato in silenzio una riga d'accesso a 821 px
su telefono. Il filetto d'attacco è `border-inline-start: 2px solid transparent` a riposo, così lo
stato corrente non sposta di un pixel il contenuto.

Una card esiste in questo sistema **solo** se passa per intero il test del benchmark: porta a una
pagina di dettaglio, ha contenuto unico rispetto ai fratelli, raggruppa tipi di contenuto
*eterogenei*, ne stanno al massimo quattro in riga, ha un solo link. Applicato alla build che questo
sistema sostituisce, praticamente nulla lo passa. L'entrata rimpiazza: le quattro colonne «Quatre
accès», le cinque pastiglie da 999 px di «Les parcours réguliers», il tre-in-riga della pagina
Imprese, la lista di sei Destinatari con le sue sei icone di tempio identiche, e le card dell'indice
delle notizie.

Il primo consumatore è `templates/components/entrances.html`, riscritto come registro: i quattro
accessi dell'ecosistema non sono più quattro colonne identiche con quattro illustrazioni, ma quattro
righe `.entry` dentro un `.register--entrances`. La lista numerata `.pathway-list` (§10) è il
prossimo candidato.

### 8.5 La nota marginale

Il dispositivo che nessun altro fa sul web, e quello che fa leggere la pagina come **pubblicata**
invece che come assemblata.

Una nota marginale sta nella terza zona, a `--t-caption-size` in `--ink-muted`, **allineata alla prima
linea di base del blocco che annota**, legata a un punto del testo da un richiamo superiore in
rubrica (`¹ ² ³`). Porta: la fonte, la data, la cautela giuridica, la clausola «ciò che la
piattaforma non fa», la versione del ruleset, l'autorità responsabile. Dove un blocco non ha nota
marginale, la terza zona non viene disegnata affatto (`.zones--no-margin`) e il contenuto si prende
lo spazio: la colonna non resta mai come un vuoto. Sotto `lg` la nota scende sotto il suo blocco,
rientrata della colonna dell'ordinale, con il richiamo conservato.

È qui che vive l'apparato giuridico. Oggi quelle clausole sono righine grigie e note a piè di pagina
a basso contrasto; come apparato marginale con richiami e fonti diventano la firma dell'istituzione.

*Implementazione.* `.zones__margin` e `.zones--no-margin` sono in `layout.css`; `.note`,
`.note__marker` e `.ref-marker` sono in `register.css`, e da `75rem` in su la prima nota del margine
riceve il `margin-block-start` che la porta sulla prima linea di base del blocco che annota.
L'apparato di chiusura che ne discende — `.sources`, l'elenco numerato delle fonti con ordinale in
rubrica, titolo, riferimento normativo e data di consultazione — è nello stesso file: è l'elemento
che più di ogni altro converte «il risultato di un questionario» in «una constatazione
istituzionale», ed è l'unico elemento che la pagina di esito precedente non aveva affatto.

### 8.6 La lastra e la fascia verso

**Lastra** — a pieno vivo, una volta per pagina: o una fotografia in 2:1 con didascalia d'archivio
(§14.2), o una **fascia verso** navy e tipografica. Chiusa in basso da un filetto
`--rubric-on-navy` da 2 px; aperta in alto da un filetto navy da 2 px dove incontra la carta.
`.plate` è in `register.css` (le regole di `.plate--verso`, che nessun template disegna, sono uscite col passo di bilancio di W3-F1, 12 ottobre 2026); `.section--verso` in `layout.css` è la stessa
dichiarazione applicata a una sezione in flusso. `.plate__figure img` impone `aspect-ratio: 2 / 1` e
`object-fit: cover`, quindi il rapporto della lastra fotografica non è una scelta dell'autore.

Il cambio di fondo è accoppiato a un **cambio di misura**, e lo è nel CSS e non nella buona volontà:
`.plate--verso .plate__statement` vale `26ch` sotto `48rem` e `44ch` sopra. Una fascia navy porta un
enunciato, non un paragrafo.

La lastra della home è **tipografica**, non fotografica: navy, a pieno vivo, display a 88 px, con il
folio `00` e `ÉDITION 2026` nel rail e la dichiarazione anti-frode promossa nel margine. Non è
decorazione: sul sito pubblico respinto `grep -ic "fraude"` sulla home restituiva 0 e la pagina
dedicata rispondeva 404 perché chiusa dal gate di Fase 3; a gate aperto l'avvertimento stava a
y=7333 su un telefono, cioè 8.7 scorrimenti più in basso. Metterlo nel margine della lastra rende il
messaggio di sicurezza più importante del sito la seconda cosa su cui cade l'occhio, senza costare
nulla alla composizione.

### 8.7 La barra di giurisdizione

L'unico innesto che tutti e quattro i giudici del Council hanno chiesto per nome, e la risposta
grafica alla domanda che è il vero soggetto del progetto: **chi risponde di questa fase**.

Una banda segmentata con legenda che dichiara quale tratto di un processo appartiene all'**Italia**,
al **Marocco**, alla **piattaforma** e a un'**autorità competente**. Va sotto l'enunciato della home
e nell'intestazione del fascicolo nella piattaforma. I segmenti si distinguono per posizione,
etichetta e peso di filetto, **mai per il solo colore**: il navy vale Italia, `--cooperation` vale
Marocco, e la guardia contro l'impersonificazione vieta qualunque accostamento rosso/bianco/verde o
rosso/verde dentro questo componente. Nessun marchio di partner compare nella barra senza un campo
`authorisation_ref` sul componente.

*Implementazione.* `.jurisdiction` (`register.css`) è una barra alta 20 px chiusa da un bordo
`--rule-ink` da 1 px, divisa in `.jurisdiction__segment` la cui larghezza relativa arriva da un
attributo `data-share` da 1 a 6 — **non da uno stile inline**, perché la CSP pubblica è `self` senza
`unsafe-inline` e un attributo `style` verrebbe scartato in produzione, lasciando quattro segmenti
uguali: un diagramma che racconta in silenzio la cosa sbagliata. Ogni responsabile ha la sua
**tratteggiatura** oltre al colore — 45° in `--cooperation` per il Marocco, −45° in `--navy` per
l'Italia, 90° in `--ink` per l'autorità competente, nessuna tratteggiatura per la piattaforma — così
la barra resta leggibile in scala di grigi, a colori forzati e per chi non distingue i colori. La
legenda `.jurisdiction__legend` è una `<ul>`, quindi uno screen reader legge responsabili e tratti
in ordine, e la barra stessa è un `role="img"` con un'etichetta.

Il passaggio fra le due sponde, dentro la sequenza, è uno **stacco strutturale** e non un cambio di
colore: `.sequence__crossing` è un filetto orizzontale etichettato, chiuso sopra e sotto da un
`--rule-ink` da 1 px, e il filetto continuo che corre accanto ai passi è `--cooperation` sopra il
passaggio e `--navy` sotto (`.sequence__step--italy .sequence__marker`). Un cambio di sola tinta
fallirebbe in scala di grigi e contraddirebbe la regola «mai il solo colore» (§4.4).

Il componente è `templates/components/jurisdiction.html` (§10).

---

## 9. Superfici, bordi, elevazione

**Elevazione: nessuna.** Zero `box-shadow` sul contenuto. L'unica ombra ammessa in tutto il sistema è
sulle due superfici che galleggiano davvero — il drawer di navigazione e `dialog` — a un solo valore,
`--shadow-surface`. Tutto il resto si separa con un **filetto** e con un **cambio di fondo**.

*Stato misurato.* `register.css` non dichiara un solo `box-shadow`: il linguaggio grafico proprio
non ha bisogno di elevazione, ed è la prova che la regola è costruibile. `--shadow-surface` non è
ancora consumata, perché drawer e `dialog` vivono ancora in `components.css` e usano i nomi dello
shim; i quattro token d'ombra legacy (`--shadow-hairline`, `--shadow-sm`, `--shadow-md`,
`--shadow-lg`) risolvono deliberatamente a `none`, così che nessun file migrato possa conservare
un'ombra di soppiatto. Restano quindi in `static/css/` sei `box-shadow` con un valore letterale, e
**nessuna di esse è un'elevazione**: i due anelli di fuoco di `base.css`, due filetti `inset` da
3 px che marcano una voce di sottomenu corrente e due anelli `0 0 0 1px` che ispessiscono il bordo
di un campo a fuoco o in errore. Il cancello T3 della direzione — *`grep box-shadow` restituisce
solo la dichiarazione dell'anello di fuoco* — non è ancora soddisfatto, perché le otto dichiarazioni
restanti di `components.css` continuano a nominare i token d'ombra anche se valgono `none` (G-26).

**Raggio: 0.** Due eccezioni, entrambe funzionali: **2 px** (`--radius-control`) su controlli di form
e bottoni, perché un controllo si legga come un controllo, e **50 %** (`--radius-marker`) sul cerchio
di un marcatore di passo. `--radius-pill` è cancellato: lo shim lo fa risolvere al raggio di
controllo, perché una pastiglia non è una forma che questo sistema possiede. Nella build respinta un
censimento dei raggi della sola home a 1440 restituiva 2 px ×12, 3 px ×7, 50 % ×5 e 999 px ×5:
quattro raggi su una pagina. .italia enuncia il principio dal lato opposto: *«gli angoli squadrati si
addicono maggiormente a elementi che richiedono una presentazione più formale e strutturata»*.

**Superfici in scatola: due in tutto il sistema.**

1. **NOTICE** — un filetto da 4 px sul bordo d'attacco nel colore dello stato, un fondo tinto al 5 %
   dalla terna, un titolo a `--t-folio-size`, corpo a `--t-prose-size`, nessuna pastiglia d'icona,
   nessuna ombra, nessun raggio. Quattro varianti legate a un innesco (ECL): *informazione* (qualcosa
   è cambiato), *concluso* (un'azione è terminata), *avvertenza* (un'azione conseguente è davanti),
   *errore* (un'azione è fallita, più il recupero). Più tre varianti editoriali (.italia): **Nota**,
   **Importante**, **Approfondimento** — sono per il contenuto permanente delle pagine lunghe ed è lì
   che vivono i disclaimer giuridici. Si collocano all'inizio di una sezione e si usano con
   parsimonia, *perché ciascuna conservi il proprio valore di segnale*.
2. **PANNELLO DI FORM** — `--surface-input` bianco, 1 px `--rule-ink`, raggio 2 px, nessuna ombra.

**Nient'altro è in scatola.** Nessun riquadro tratteggiato con un'icona centrata. Una regione vuota è
**un filetto e una frase allineata a sinistra** che nomina chi la riempie e quando, con l'azione che
la risolve come link di testo in linea: è la classe `.empty` di `register.css`, un
`border-block-start` da 1 px e una misura `--measure-gloss`, e nient'altro. Il portale rende oggi sei
riquadri tratteggiati su un solo cruscotto, cinque dei quali identici, ciascuno con la stessa icona
due volte: nell'intestazione e al centro del riquadro.

Allo stesso principio rispondono gli altri due oggetti di stato di `register.css`: `.outcome` — i
cinque esiti di regola (`--possible`, `--missing`, `--warning`, `--stop`, `--review`), ciascuno una
**parola** a corpo di titolo con un filetto di stato da 4 px sul bordo d'attacco, mai una scatola
colorata — e la pastiglia di stato, che dal design V5 è un componente a sé (`chip.html`, §10): la parola, la marca
del suo registro e lo stile del bordo, mai il solo colore.

**Bottoni: tre ranghi, non uno di più.**

| Rango | Trattamento | Regola |
|---|---|---|
| PRIMARIO | pieno navy, testo carta, 44 px, raggio 2 px | esattamente uno per vista |
| SECONDARIO | contorno navy da 1 px, testo navy, 44 px | zero o più |
| TESTO | inchiostro, sottolineato, freccia facoltativa | ovunque |

Da cancellare: `.btn--ghost`, `.btn--upper` (usato una volta, per sembrare diverso) e il link
d'accesso maiuscolo in bronzo. E una regola scritta: **l'azione primaria di un flusso mantiene lo
stesso rango su ogni superficie su cui compare.** Nella build respinta «avvia il questionario di
orientamento» era un bottone pieno navy sulla home e un bottone a contorno nel portale.

**`border: 1px` corrisponde solo ai controlli di form e a `dialog`.** È il test T4 del Council, ed è
la garanzia anti-scheda più efficace proposta da chiunque: *una scheda è definita dalla sua scatola,
non dai suoi angoli.* Anche questo cancello non è ancora soddisfatto da `components.css` (G-26).

---

## 10. Catalogo componenti (`templates/components/`)

41 file. Ogni componente è un include Django senza logica di business: riceve variabili di contesto
(`{% include "components/x.html" with a=… b=… %}`) e produce markup BEM stilato da `components.css`.

**Stato del catalogo rispetto alla direzione A.** Due componenti sono già sul nuovo linguaggio:
`entrances.html`, riscritto come registro di quattro entrate, e `jurisdiction.html`, che è nuovo.
Gli altri venticinque vengono dal catalogo precedente e sono tuttora quelli che le pagine
includono. Il livello di token li ha già cambiati di aspetto — il bronzo è diventato rubrica, le
ombre sono sparite, i raggi sono 2 px o 0, il verde di successo è diventato blu — perché ognuno
consuma nomi mappati dallo shim (§17). Il contratto di ciascuno, le sue garanzie di accessibilità e
i suoi consumatori restano validi e sono documentati qui. Ciò che cambia con il resto della
migrazione è il **numero** dei componenti: `card.html` e `pathway_list.html` convergono anch'essi
sull'entrata (§8.4) e `hero.html` sulla lastra (§8.6). Finché quella migrazione non è fatta, questa
sezione descrive ciò che esiste, non ciò che si vorrebbe.

Regole comuni:

- **Testi prescritti**: passare il valore ottenuto con `{% locked "chiave" as var %}` e, se la lingua
  effettiva differisce da quella della pagina, `lang=` con il risultato di `{% locked_lang "chiave" %}`
  (quasi tutti i componenti accettano `lang`). Mai copiare il testo nel template.
- **HTML nei parametri** (`body`, `text`, `meta`, `actions`): l'autoescape resta attivo; chi passa
  HTML deve marcarlo sicuro a monte (`format_html`, `mark_safe` su contenuto già sanificato).
- **Link verso altre app**: `{% safe_url 'ns:name' as u %}` e rendere il link solo se `u` non è vuoto.
- **Icone**: `{% svg_icon "nome" "classi" %}` — decorative per default (`aria-hidden="true"`).
- «Usato in» elenca file presenti nell'albero di lavoro (il test verifica che esistano e che
  contengano l'include o il blocco CSS; «e almeno altri N» è un **minimo**, non un totale, così i
  template aggiunti dopo non lo rendono falso). Restano senza consumatore `accordion.html` (solo
  markup diretto), `hero.html`, `institutional_banner.html`, `metadata_row.html` e
  `tabs.html`: per questi l'esempio è ricavato dal contratto ed è dichiarato come tale. I cinque
  componenti del sistema degli overlay — `dialog.html`, `drawer.html`, `popover.html`, `sheet.html`,
  `tooltip.html` (W2-A) — hanno per ora un solo consumatore, la tavola campione dell'anteprima
  (`templates/dev/designpreview/specimens/overlays.html`); li adottano il secondo passo di W2-A (il cassetto, il
  popover del conto e il menu di riga della console), W2-C2 (lo sheet del telefono, il popover della targa) e W3-C
  (il cassetto dell'anteprima, lo sheet dei filtri).

#### `accordion.html`

- **Scopo**: domande/risposte e sezioni richiudibili; `<details>`/`<summary>` nativi.
- **Blocco CSS**: `.accordion` (`.accordion__item`, `.accordion__summary`, `.accordion__body`; `.accordion__panel` è
  lo stesso riquadro col nome che gli dà il markup delle FAQ), in `static/css/v5/tabs.css`.
- **Contratto**: `items` = lista di dict `{id, title, body (HTML sicuro), open (bool), lang}`; `single`
  (True → un solo pannello aperto: attributo `name` nativo + fallback JS `data-accordion="single"`);
  `group` (valore di `name` quando `single`, default `accordion`).
- **Varianti**: nessun modificatore. La marca è un gallone disegnato in CSS su ogni `summary`, che ruota quando
  `[open]`; l'icona in linea del template gli cede il posto.
- **Accessibilità**: ruolo, stato espanso/chiuso e tastiera (Invio/Spazio) forniti dal browser;
  funziona senza JS; `summary` alto almeno 56 px; `id` per item → permalink `#id`, che `initAccordions` apre
  all'arrivo (§16).
- **Usato in**: `templates/faq/_item.html`, `templates/faq/index.html` (markup diretto; usa
  `.accordion__panel` al posto di `.accordion__body` — G-19, chiusa: il foglio definisce entrambe).
- **Esempio (dal contratto — nessun `{% include %}`)**:

```django
{% include "components/accordion.html" with items=faq_items single=True group="faq-general" %}
```

#### `account_menu.html`

- **Scopo**: il popover del conto (piano V5.4 §1.14; W2-A): «Espace réservé», «Profil», «Sécurité du compte» e,
  dopo un filetto, «Se déconnecter».
- **Blocco CSS**: il comando `.account-menu__summary` (`.account-menu__name`) — la sua base in
  `static/css/v5/overlays.css` §9, per i due volti; la sua sede lo disegna (`v5/_shell.css` nella console,
  `v5/chrome.css` nella testata) —; il pannello è il popover del sistema (`.overlay--popover`, le righe
  `.overlay__item`); il volto `<details>` di V4 è uscito con `v4/shell.css` (W2-C2).
- **Contratto**: legge `user` dal contesto; `popover` (True: ogni chiamante lo dice); `menu_id` (l'id del
  popover; "account-menu" per default). Le voci compaiono solo se la route esiste: `portal:dashboard`,
  `accounts:profile`, `mfa_index`, `account_logout` (via `safe_url`). Il componente si include di nuovo per le
  righe (`overlay_part` = "body", il contratto di `popover.html`).
- **Varianti**: un solo volto: un vero `<button popovertarget>` — il glifo della persona, il nome breve, uno
  chevron —, nominato «‹nome breve› — Mon compte» (le parole che mostra per prime, WCAG 2.5.3, poi ciò che apre: due
  stringhe vive), e `components/popover.html`, un gruppo nominato «Mon compte»; ≤ 40rem uno sheet dal basso che resta
  un menu, sopra l'unico scrim, con «Mon compte» in testa. Tre sedi: la barra della console (`console-account`), la
  targa della testata (`account-menu`) e il piede del foglio sotto 48rem (`account-menu-sheet`) — W2-C2, con
  `overlay.js` importato da `shell.js`; il `<details data-dropdown>` di V4 è uscito.
- **Accessibilità**: il fuoco sulla prima riga e di ritorno al comando dopo Esc o una scelta, le frecce,
  `aria-expanded` sul comando, il clic fuori e la perdita di fuoco lo chiudono, righe di 44 px sotto un dito, nulla che
  si animi da tastiera. Il logout è un `<form method="post">`
  con CSRF e un vero `<button>`, non un link GET. Nella console il nome non è mai tagliato (il solo glifo sotto
  48rem, su due righe nella fascia); dove una sede lo taglia con un'ellissi — la targa della testata — resta **da
  correggere**: `text-overflow: ellipsis` è vietato su testo d'identità, giuridico e di navigazione (§11.1).
- **Usato in**: `templates/partials/portal_chrome.html` (la barra superiore della console sotto 64rem, il popover —
  `popover=True menu_id="console-account"`; da 64rem il conto è al piede della rail, §11.6), `templates/partials/header.html`
  (la sede della targa nella testata V5 e la testa del cassetto, il volto `<details>`; W2-C1 → W2-C2).
- **Esempio reale — `templates/partials/portal_chrome.html`**:

```django
{% include "components/account_menu.html" with popover=True menu_id="console-account" %}
```

#### `badge.html`

- **Scopo**: etichetta di stato compatta per gli include che nominano un `kind`. **È una pastiglia**
  (`chip.html`): il `kind` è tradotto una sola volta in registro, e la marca è quella del registro.
- **Blocco CSS**: `.chip` (`static/css/v5/chip.css`); la classe `badge` resta sull'elemento come aggancio
  per le pagine che lo collocano, e nessuna regola la dipinge.
- **Contratto**: `label`; `kind` ∈ `neutral | info | primary | success | warning | error | pending | soon |
  overdue` (opzionale). Nessuna icona scelta da chi include: il glifo di una pastiglia è la sua marca.
- **Varianti**: nessun modificatore. `core.chips.KIND_REGISTER` traduce: `success` → *conforme* (inchiostro e
  disco pieno: **mai verde, mai una spunta**, §4.3), `warning` → *attesa*, `error` → *rifiuto*, `pending` →
  *esame*, `soon` → *attesa*, `overdue` → *azione* (il rosso non significa mai ritardo), gli altri → *neutro*.
- **Accessibilità**: il significato è nella parola, poi nella marca e nello stile del bordo, mai nel solo
  colore; la marca è decorativa (`aria-hidden`).
- **Usato in**: `templates/portal/messages.html`, `templates/portal/requests.html`,
  `templates/portal/request_detail.html`, `templates/portal/partials/card.html`,
  `templates/portal/partials/deadline_item.html` (include).
- **Esempio reale — `templates/portal/messages.html`**:

```django
{% translate "Non lue" as unread_label %}{% include "components/badge.html" with label=unread_label kind="primary" %}
```

#### `blockquote.html`

- **Scopo**: citazione istituzionale (es. `p1.companies.quote`).
- **Blocco CSS**: `.blockquote-institutional`.
- **Contratto**: `text` (la frase, virgolette incluse quando prescritte); `cite` (opzionale); `lang`.
- **Varianti**: nessuna. Filetto da 2 px sul lato d'attacco, serif a `--font-size-h3` (che lo shim
  fa valere `--t-entry-size`). Il filetto era bronzo ed è ora rubrica, perché `--border-accent`
  risolve a `--rubric`: **è un uso da riesaminare**, perché una citazione non è una posizione in una
  sequenza e la rubrica ha un solo compito (§4.1).
- **Accessibilità**: `<blockquote>` + `<cite>` semantici; `lang` per il fallback francese.
- **Usato in**: `templates/dev/showcase.html` (la vetrina). Nessuna pagina lo include più: dall'11 ottobre 2026 (V5.4, W3-F1, l'interno pubblico)
  la citazione prescritta dell'Espace Entreprises è l'enunciato del capitolo «La démarche»
  (`.citazione`, `apps/ecosystem/static/ecosystem/_spaces.css`).
- **Esempio (dal contratto)**:

```django
{% include "components/blockquote.html" with text=quote.text lang=quote.lang_attr %}
```

#### `breadcrumbs.html`

- **Scopo**: filo d'Arianna sotto l'header (blocco `breadcrumbs` di `base.html`).
- **Blocco CSS**: `.breadcrumbs` (il componente include già `.container`).
- **Contratto**: `breadcrumbs` = lista di `{"label": str, "url": str | ""}` fornita dalla view;
  l'ultimo elemento è la pagina corrente. «Accueil» è aggiunto automaticamente (`pages:home`).
- **Varianti**: nessuna. I separatori sono chevron disegnati in CSS (bordi ruotati), specchiati in
  RTL. Il disegno (design V5): lo scheletro — la lista, l'elemento, lo chevron e il suo specchio — in `components.css`
  §9, per ogni superficie; il resto lo disegna ciascuna: la pagina dell'interno pubblico (`static/css/v5/_pagina.css`
  §1, W3-F1 e W3-F2: 13/20, la pagina corrente in inchiostro, ogni link una scatola di 24 px, il suo bersaglio di 44
  sotto un dito), le pagine del conto (`static/css/v5/_servizio.css` §1), la barra della console
  (`apps/portal/static/portal/v5/_shell.css` §3). La scatola, il carattere, i link, il loro hover e la pagina corrente
  sono usciti da `components.css` col passo di bilancio di W3-F1 (12 ottobre 2026): ogni superficie li ridisegnava.
- **Accessibilità**: `<nav aria-label="Fil d’Ariane">` + `<ol>`; ultimo elemento `aria-current="page"`
  e non linkato; i separatori non sono contenuto.
- **Sotto la direzione A**: il breadcrumb va derivato **dallo stesso albero di menu della
  navigazione**, presente solo a profondità ≥ 2, e reso a `--t-folio-size` dentro il rail da `lg` in
  su. Uno stub a un livello `Accueil > Contact` è peggio di niente, ed è ciò che ogni pagina rende
  oggi.
- **Usato in**: `templates/community/index.html`, `templates/faq/index.html`,
  `templates/forum/index.html`, `templates/pathways/index.html`, `templates/news/index.html` (e almeno
  altri 30 template; 34 al momento dell'ultima verifica — il consolidamento dei template dell'area
  riservata ne ha tolti tre, e la soglia è scritta con margine perché è un minimo, non un conteggio).
- **Esempio reale — `templates/community/calendar.html`**:

```django
{% block breadcrumbs %}{% include "components/breadcrumbs.html" %}{% endblock %}
```

  Le pagine del conto scrivono lo stesso markup con le stesse classi nel loro partial della traccia, perché le view
  di allauth non ne danno una (W3-F2, passo 2).

#### `busy_key.html`

- **Scopo**: la chiave occupata — L2 del loader «Lume» (piano V5.4 §1.9, W1-D) — fuori da un bottone: la sola chiave,
  nel colore del testo, per una riga o una voce che aspetta (una pièce in elaborazione, la testa di una regione mentre
  arriva un frammento). In un bottone non serve markup: `v5/loader.css` la disegna su `.btn.is-busy::after`, al centro
  del padding di fine riga qualunque sia la taglia — l'etichetta non si sposta e la chiave non la tocca: 7 px
  dall'ultima lettera in un bottone, 5 in uno piccolo, 3 in uno piccolo in arabo (a 8 px fissi dal bordo ne distava
  1,2 e 0,3) — e `shell.js` mette `aria-busy` e la classe a ogni invio, nel task stesso del clic. Tre regole dello hook
  (revisione del 9 ottobre 2026):
  - **solo un controllo `.btn` aspetta**: un controllo d'invio che non è un bottone del sistema (l'uscita del menu del
    conto) non dichiara uno stato che l'occhio non vede;
  - **la chiave solo dove ha posto**: un bottone-link (`.btn--tertiary`, `.btn--link`, `.btn--text`, `.btn--inline`) è
    il suo testo e un `.btn--icon` la sua icona — senza padding la chiave finiva sopra le ultime lettere
    dell'etichetta. Quelle varianti ricevono `aria-busy` e nessuna classe: aspettano e restano come sono, senza chiave
    e senza la lastra che la regola occupata di V4 darebbe loro. L'elenco (`KEYLESS` in `shell.js`) è letto da
    `test_loader_rules` contro i fogli: una variante nuova senza padding non può essere dimenticata;
  - **nessuna attesa è per sempre**: un form la cui risposta non sostituisce la pagina perché è un file lo dichiara con
    `data-loader="none"` e non aspetta affatto (l'esportazione dei dati del conto, `templates/accounts/profile.html`;
    `test_loader_rules` lo esige per ogni form che invia a una vista che risponde con un allegato); ogni altra attesa
    che nessuna pagina chiude finisce da sé (§16, `loader.js`).
- **Blocco CSS**: `.busy-key` (`__turn`), in `v5/loader.css`: `key.svg` ritagliata simmetrica sul gambo (viewBox
  10 11 40 94), 16 px (`--key-size`); quando l'host è `.is-busy` fa un giro di `--motion-emphasized` su `--ease-turn`,
  poi tiene attenuata all'80 % dell'inchiostro. È l'unico indizio visivo dello stato, quindi WCAG 1.4.11 le chiede
  3 : 1 sul suo fondo: misurata sui pixel, 4,0 : 1 sul teal che ogni bottone occupato ha oggi (al 55 % leggeva 2,7), e
  mai sotto 3,9 : 1 sull'inchiostro e sul fondo propri di ogni variante, per il giorno in cui un bottone occupato
  terrà la sua superficie; `.is-lit` la accende (`loader.js`: `busy()` / `settle()`).
- **Contratto**: `css_class` (opzionale). Lo stato viene dall'host, mai dal componente; decorativa (`aria-hidden`):
  l'host dice `aria-busy`, le parole dicono il resto.
- **Varianti**: nessuna; la misura è `--key-size` sull'host.
- **Accessibilità**: decorativa; sotto `prefers-reduced-motion: reduce` il token vale 0 ms e la chiave è ferma, attenuata;
  sotto colori forzati segue `ButtonText`.
- **Usato in**: `templates/dev/designpreview/specimens/loader.html` (la tavola campione); le righe dei frammenti
  asincroni delle famiglie dell'onda 3.
- **Esempio reale — `templates/dev/designpreview/specimens/loader.html`**:

```django
<p class="lb__row-wait is-busy" aria-busy="true">{% include "components/busy_key.html" %}<span>Ouverture du document…</span></p>
```

#### `card.html`

- **Scopo**: la **scheda** — la prima delle tre funzioni di una card (`static/css/v5/card.css`): ciò che esiste
  e si legge (una notizia, uno spazio collegato, una fase) e, con `url`, si apre. Le altre due funzioni si
  scrivono dove si compongono, non qui: la scheda d'azione e la striscia di sintesi (§10.1).
- **Blocco CSS**: `.card` (`__eyebrow`, `__title`, `__text`, `__meta`), in `static/css/v5/card.css`.
- **Contratto**: `title`; `url` (opzionale: l'intera scheda diventa il bersaglio); `eyebrow`; `text`;
  `meta` (str o HTML sicuro); `lang`; `flat` (True → una voce di lista: senza scatola, il filetto della riga
  sopra).
- **Varianti**: `.card--link` (automatica con `url`), `.card--flat`. Foglio e filetto, angolo di 8 px,
  l'ombra del foglio (livello 1) e nient'altro: al contatto il filetto si rafforza e il titolo si sottolinea,
  nessuna ombra si anima. Più schede di seguito sono una **lista** (`flat`), mai una riga di scatole uguali.
  Una voce `flat` ha sotto l'ultima riga lo stesso spazio che sopra la prima (20 px): le liste che la
  contengono tengono un passo di riga piccolo, e il filetto della voce seguente cadrebbe sul testo.
- **Seconda azione e contenuto avvolto**: un link che sta da solo nella riga `__meta` — la seconda azione
  della scheda, «Voir le parcours …» — è un bersaglio di 24 px (SP-8) su una riga che resta 13/20. Il
  contenuto può essere avvolto in **una** `<section>` con nome (il caso del catalogo, `templates/dev/showcase.html`;
  le due fasi di «Formation» l'hanno lasciato col secondo passo di W3-F1): tiene il flusso della scheda — lo
  stesso passo fra le parti, la riga `__meta` al piede — così le seconde azioni di due schede affiancate
  stanno sulla stessa linea.
- **Accessibilità**: «stretched link» — lo pseudo-elemento del link del titolo copre la scheda, quindi
  c'è **un solo tab stop** e il nome accessibile è il titolo; l'anello di fuoco è quello del sistema, sul
  titolo. Il titolo è sempre `<h3>`: collocare la scheda sotto un `h2`.
- **Usato in**: `templates/pages/home/_news.html` (include). Le due fasi di «Formation» non sono più due schede:
  dal secondo passo di W3-F1 sono due stazioni di «la linea», una sequenza reale. Dall'11 ottobre 2026 (v5.4, w3-f1, l'interno pubblico) «Pour aller plus loin» degli spazi dell'ecosistema è un registro
  di righe (`.registro`, `static/css/v5/_pagina.css` §4), non più una lista di schede.
- **Esempio reale — `templates/pages/home/_news.html`**:

```django
{% include "components/card.html" with title=article.title url=article.url eyebrow=article.category text=article.summary meta=article.date lang=article.lang %}
```

#### `case_timeline.html`

- **Scopo**: la **Timeline** di un fascicolo, disegnata dall'unico disegno di binario della console (design V5,
  W3-D, §11.9): che cosa è accaduto, dal più recente — letta dal registro di audit
  (`cases.presenters.timeline`), append-only, mai composta a mano. Una spina coi nodi del binario: ogni evento
  dietro il fascicolo un punto d'inchiostro pieno (nessuna spunta, O14), il più recente — la prima riga — l'anello
  laguna sul suo velo: dove il fascicolo sta ora apre la lista (l'ispettore che la contiene scorre in sé, e la sua
  prima riga è quella in vista); la data in cifre tabulari, il titolo dell'evento, lo stato prodotto come chip col
  suo registro, l'attore come TIPO («Vous», il ruolo tenuto sul fascicolo, l'équipe del progetto) — mai il nome di
  una persona, e mai detto due volte (il dettaglio di un'assegnazione è già il ruolo). Fermo al caricamento: il nodo
  più recente è dipinto acceso, nulla si muove (il `tl-light` di V4 è uscito). Il titolo della Timeline è della
  pagina e la sua formulazione è del committente (B1 voce 4).
- **Blocco CSS**: `.tl` (`__row`, `__node`, `__when`, `__what`, `__title`, `__detail`, `__actor`; modificatore
  `--latest`), in `apps/portal/static/portal/v5/_journey-rail.css` §5, sul vocabolario di `v5/_journey-nodes.css` (i
  parziali del foglio di sola pagina `portal/journey.css`, §2.1).
- **Contratto**: `rows` (`cases.presenters.timeline(case)`, dal più recente: when, title, detail, chip_label,
  chip_register, actor); `label` (opzionale, `aria-label` della lista).
- **Varianti**: nessuna.
- **Accessibilità**: `<ol role="list">`, la data è un `<time>`, il chip porta la parola; il nodo è decorativo; a
  colori forzati i punti in `CanvasText`, l'ultimo anello in `Highlight`, la linea in `GrayText`.
- **Usato in**: `templates/cases/detail.html`.
- **Esempio reale — `templates/cases/detail.html`**:

```django
{% include "components/case_timeline.html" with rows=timeline %}
```
#### `chip.html`

- **Scopo**: la **pastiglia di stato** del design V5, «i cerchi» (piano V5.4 §1.2): una marca, una parola e
  un bordo. Lo stato è detto tre volte senza colore — la parola, la marca del registro (cerchio aperto = in
  corso, pieno = risolto, il lucchetto per una dipendenza), lo stile del bordo — e mai da una spunta:
  «conforme» è inchiostro e un disco pieno (O14). **Non si include**: è resa dalla sola coppia
  `{% chip %}` … `{% endchip %}` di `apps/core/templatetags/ile_core.py`, unico produttore dell'elemento —
  una pastiglia non esiste mai senza la sua marca.
- **Blocco CSS**: `.chip` (`__g` la marca, `__w` la parola, `__meter` la jauge; taglie `--s` 20 px e `--l`
  28 px), in `static/css/v5/chip.css`; i colori di ogni registro sono token di `static/css/v5/tokens.css`,
  ripuntati da `[data-register]`.
- **Contratto**: `label` (la parola, già resa: il blocco della coppia); `register` (uno degli otto di
  `apps/core/chips.py`, vuoto per un valore sconosciuto); `mark` (il simbolo dello sprite, dal registro delle
  icone — mai scelto qui); `size` (la taglia densa o la grande); `notches` (le tre fasi dello stato di un fascicolo);
  `css_class` (le classi che **collocano** la pastiglia nella pagina, mai una che la dipinge); `role`; `lang`;
  `title`. Chi scrive un template passa alla coppia il membro e il nome del suo enum —
  `{% chip row.state "documents.RequirementState" %}` — oppure `register="neutro"` per uno stato che il
  template conosce da sé.
- **Varianti**: otto registri (*conforme · esame · neutro · attesa · azione · rifiuto · blocco · nullo*);
  «Manquant» e «À remplacer» sono un solo registro e due marche. Un valore che `chips.py` non conosce è
  disegnato sul tono neutro col bordo puntinato, senza `data-register`, ed è scritto nel log.
- **Accessibilità**: la parola è il nome; la marca è decorativa (`aria-hidden`) e il suo disegno, non il
  suo colore, distingue i registri (la coppia più vicina, ambra / terracotta, è un colore solo per un
  deuteranope). Uno stato non è un controllo: nessun hover, nessun focus, nessun puntatore. Nei colori
  forzati corpo, bordo, marca e parola passano ai colori di sistema e lo stile del bordo resta. In arabo
  la marca è dal lato di lettura e non si specchia; il testo non scende sotto i 14 px.
- **Usato in**: `templates/components/document_row.html`, `templates/portal/dashboard.html`,
  `templates/cases/detail.html`, `templates/companies/dashboard.html`, `templates/helpdesk/requests.html`,
  `templates/components/badge.html` e ogni altro template che mostra uno stato (la coppia, mai l'include:
  `tests/frontend/test_state_chips_carry_a_register.py` tiene l'elenco).
- **Esempio reale — `templates/components/document_row.html`** (la coppia rende `components/chip.html`):

```django
{% chip row.state "documents.RequirementState" %}{{ row.state_label }}{% endchip %}
```

#### `cta_panel.html`

- **Scopo**: invito all'azione a fine pagina; fascia tra due filetti o fascia navy.
- **Blocco CSS**: `.cta-panel` (`__inner`, `__title`, `__text`, `__actions`).
- **Contratto**: `title`; `text` (opzionale); `primary_label` + `primary_url`; `secondary_label` +
  `secondary_url` (opzionali); `lang`; `variant` (`"inverse"` → fascia navy, aggiunge `.on-inverse`).
- **Varianti**: `.cta-panel--inverse`. Bottoni: primario `.btn--primary.btn--arrow` (freccia
  specchiata in RTL), secondario `.btn--secondary`; in variante inverse entrambi ricevono
  `.btn--inverse`. La variante inverse è una superficie navy e **conta come la fascia verso della
  pagina**: non può coesistere con un'altra (§4.2).
- **Accessibilità**: `<section aria-labelledby="cta-<slug del titolo>">` con `<h2>`. L'`id` deriva da
  `title|slugify`: due pannelli con lo stesso titolo, o un titolo interamente non latino (slug
  vuoto), producono `id` duplicati o ambigui — G-13: al massimo un CTA panel per pagina finché non è
  corretto.
- **Usato in**: `templates/portal/partials/access_point.html` (markup diretto). Nessuna pagina pubblica lo
  include né lo disegna più (la fascia dell'orientamento di «Diplômes et titres» e di «Formation» è uscita col
  secondo passo di W3-F1): dall'11 ottobre 2026 (V5.4, W3-F1, l'interno pubblico) l'unica azione di una pagina è la scheda d'azione di
  `static/css/v5/card.css` (`card card--action`, D26 «one action»), composta nella pagina.
- **Esempio (dal contratto)** (l'etichetta del bottone è un testo prescritto, passato tramite
  `{% locked … as %}`):

```django
{% locked "p3.universities.button" as button_label %}
{% include "components/cta_panel.html" with title=_("Proposer un partenariat") text=_("Présentez votre établissement et votre proposition : chaque demande est lue par l’équipe du projet.") primary_label=button_label primary_url=links.university_proposal %}
```

#### `dialog.html`

- **Scopo**: il dialog modale e l'alertdialog del sistema degli overlay (piano V5.4 §1.14; W2-A; il contratto
  `docs/design-v5/QA/v54/w2-a/CONTRACT.md`): una conferma, una decisione breve, una conseguenza. Mai per contenuti
  obbligatori o pubblicità. Un `<dialog>` nativo che `static/js/src/overlay.js` apre modale — `show()` sopra l'unico
  scrim, con la trappola in script e `aria-modal` (la regola INP del piano: `showModal()` rende inerte tutta la pagina e
  la ristila intera; `data-overlay-modal="native"` lo tiene dove una pagina è leggera): Esc lo chiude, lo scrim lo chiude — solo se il puntatore vi è sceso **e** risalito, mai un alertdialog, mai
  con un campo già scritto —, il fuoco torna a chi l'ha aperto (o a `data-overlay-return`), Tab e Maiusc+Tab girano
  dentro il pannello.
- **Blocco CSS**: `.overlay` (`__head`, `__glyph`, `__title`, `__close`, `__body`, `__foot`) con `.overlay--dialog`,
  `.overlay--alert`, `.overlay--wide`, nel parziale **solo di pagina** `static/css/v5/_overlay-panels.css` (la base
  `.overlay` e il suo moto sono di `static/css/v5/overlays.css`): la pagina che disegna un dialog collega
  `css/dist/core/overlay-panels.css` nel suo `extra_head` (§2.1; il contratto §1).
- **Contratto**: `id` (obbligatorio); `title`; `body` (HTML sicuro) — oppure `body_template`, un template incluso col
  contesto e `overlay_part` = "body"; `actions` (HTML sicuro dei bottoni del piede: il primario per ultimo, un'azione
  distruttiva per ultima come `btn--danger`; un bottone che chiude soltanto porta `data-overlay-close`) — oppure
  `actions_template` (incluso con `overlay_part` = "actions"); `kind` = "alert" (`role="alertdialog"`: lo scrim non lo
  chiude mai ed Esc è la sua risposta sicura, il bottone marcato `data-overlay-safe`, che prende anche il fuoco);
  `glyph` (il disco di 40 px di una conseguenza); `wide` (48rem invece di 36); `describedby` (l'id della frase che un
  alertdialog legge); `return_id` (dove porta «Fermer» senza script; `main-content` per default).
- **Varianti**: dal centro dello schermo, l'unica eccezione all'origine (MS §6): scala .96 → 1 con l'opacità in
  `--motion-emphasized` (320 ms), lo scrim in 200 ms, fuori in 120 ms insieme; larghezza `min(100% − 32 px, 36rem)`
  (`--wide` 48rem), altezza massima `min(100dvh − 32 px, 44rem)`; ≤ 40rem uno sheet dal basso sulla molla dello sheet.
  Una delle superfici a cui il sistema concede l'ombra 4 (§9).
- **Accessibilità**: `aria-labelledby` → il titolo; `aria-modal="true"`; la pagina dietro non prende né una pressione
  (lo scrim) né il fuoco (la trappola lo riporta dentro), ed esce dall'albero dell'accessibilità finché il dialog è
  aperto (`aria-hidden` sul resto della pagina, mai `inert`: un motore non pota nulla per il solo `aria-modal`); un
  corpo che scorre senza nulla da mettere a fuoco diventa una fermata sua (`tabindex="0"`, WCAG 2.1.1: a 400 % il corpo
  dell'alertdialog); «Fermer» 44 × 44 px, sempre presente (un link `href="#…"` che
  `overlay.js` fa bottone: senza script il dialog si mostra al suo posto via `:target` e «Fermer» riporta indietro); il
  fuoco entra nel compito dell'input (`[data-overlay-focus]`, la risposta sicura di un alertdialog, il primo controllo
  del corpo, poi del piede, poi il titolo) ed esce verso l'apritore; da tastiera nulla si anima; sotto il moto ridotto
  una sola opacità di 80 ms; sotto colori forzati il pannello tiene un bordo `CanvasText`. `docs/ACCESSIBILITY.md` §7.
- **Usato in**: `templates/dev/designpreview/specimens/overlays.html` (la tavola campione: la cancellazione del conto
  come alertdialog, il ritiro di un bisogno come dialog con un campo); la vetrina di sviluppo
  `templates/dev/showcase.html` (due dialog aperti dal sistema, `data-overlay-open`: `initDialogs` ha lasciato
  `main.js` col suo ultimo chiamante).
- **Esempio (dal commento di contratto del componente)**:

```django
<a class="btn btn--secondary" href="#confirm-delete" data-overlay-open>{% translate "Supprimer mon compte" %}</a>
{% include "components/dialog.html" with id="confirm-delete" kind="alert" glyph="trash-2" title=dialog_title body=dialog_body actions=dialog_actions %}
```

#### `doorway.html`

- **Scopo**: la porta del committente (`docs/design-v2/BRAND_ASSETS.md` §2) disegnata una volta per ogni
  palcoscenico che la chiede: arco 3:4 320 × 427 a x 288–608 / y 80–507 di un palcoscenico 640 × 520,
  fotografia dentro l'arco, arco interno navy al 52 % da 13,7 %, chiave al 34 %, tre gradini 66/80/94 %,
  contorno che si traccia una volta.
- **Blocco CSS**: `.doorway__door` (`__body`, `__img`, `__veil`, `__arch-inset`, `__inner`, `__glow`, `__key`,
  `__steps`, `__arch`), in `v4/hero.css`; i colori delle fermate dei gradienti sono classi, nessun colore
  letterale nel markup.
- **Contratto**: `prefix` (opzionale, default «doorway»), per gli id di clip e gradienti quando due porte
  condividono una pagina; incluso DENTRO un `<svg>` in unità di palcoscenico (la home `0 0 640 520`,
  la porta compatta `264 64 368 456`). La coreografia arriva dallo script della pagina
  attraverso `data-doorway-trace`, `data-doorway-steps`, `data-doorway-key`, `data-doorway-photo`.
- **Varianti**: nessuna: la porta è la porta.
- **Accessibilità**: l'`<svg>` che la contiene è `aria-hidden`: la porta è immagine di marca,
  l'informazione della pagina è nel testo; completa al primo frame, con `prefers-reduced-motion:
  reduce` nulla si muove; sotto colori forzati contorno e gradini in `CanvasText`.
- **Usato in**: `templates/portal/partials/now_panel.html` (il NowPanel dei cruscotti: l'unico stato vuoto della
  console che mostra la porta — «pas encore de dossier» della persona, `viewBox` `264 64 368 456`, prefisso
  `db-door`; W3-B, piano V5.4 §2.3 e §3.1 voce 7), dall'11 ottobre 2026 la sola pagina che lo include. La home
  (`templates/pages/home/_hero.html`, W2-D) e l'ingresso (`templates/allauth/layouts/entrance.html`, W2-B)
  disegnano lo stesso palcoscenico col proprio markup in unità di palcoscenico — la fotografia in un `<img>` /
  `<picture>`, la chiave come livello HTML che gira sul compositore (il primitivo `.sig__l` / `.sig__turn` del
  loader, §12) —; l'ingresso con le stesse classi `.doorway__*`, dipinte da `static/css/v5/_door.css` (§2.1), e
  così le pagine d'errore (`templates/errors/_door.html`, la porta a riposo con la chiave fuori dalla serratura,
  attraverso `cms/errori.css`). Il componente e la sua pittura in `v4/hero.css` restano finché il NowPanel lo
  include.
- **Esempio**:

```django
{% include "components/doorway.html" %}
```

#### `document_row.html`

- **Scopo**: una pièce richiesta di un fascicolo come riga a SEI zone sulle colonne che tutte le righe della
  collezione condividono — pièce · stato · responsabile · scadenza · azione · apertura — e, quando c'è, la NOTA come
  piede della riga sulla sua misura intera (il motivo di un rifiuto, la ragione di una sostituzione richiesta) (design
  V5, «Mes pièces» V5.2: V5.4 plan §3.5 item 5; `DOCUMENT_WORKSPACE.md` §6; W3-C). **La riga è il link**: il link del
  titolo è steso su tutta la riga, sopra il chip, l'attore, la data e la nota, sotto l'azione — nessun punto della riga
  che mostra il suo hover è morto (nel gate 0 lo erano 14 su 30). Nessun menu di riga e nessun «Consulter»:
  «Télécharger» e i depositi stanno sulla pagina della pièce. L'azione c'è solo su una pièce APERTA che il lettore può
  depositare — «Déposer la pièce», «Remplacer la pièce» — ed è descritta dal titolo della pièce (W-3); una pièce
  depositata, in esame o valida non offre niente sulla riga (la riga tranquilla); dove il cancello delle Condizioni
  blocca il deposito la riga dice «Bloqué» accanto al chip e non offre un atto che la sua destinazione non può
  compiere (il flusso di accettazione attende i testi legali, G1): la striscia dice perché. Lo stato è una parola col suo registro (`data-register` da
  `apps/core/chips.py`), mai scelto qui; nessuna riga dice «approvato». La data tiene sempre il suo glifo (la mappa
  DUE del registro: `calendar` · `clock` · `alarm-clock`, quest'ultimo mai sotto i 20 px) con «Bientôt» / «En
  retard» accanto; una pièce depositata ha la data calma (F8, `documents.presenters`).
- **Blocco CSS**: `.doc-row` (`__piece`, `__title`, `__link`, `__qualifier`, `__meta`, `__state`, `__blocked`, `__note`
  con `--refusal`, `__resp`, `__actor`, `__actor-note`, `__due`, `__act`, `__gate`, `__open`) con `.doc-due` (`__mark`,
  `__word`; `--upcoming`, `--soon`, `--overdue`), in `apps/portal/static/portal/v5/_workspace.css` — un partial della
  console importato dal foglio delle pagine dei documenti (`apps/documents/static/documents/documents.css`), mai da
  `main.css` né dall'ingresso della console. La griglia è il subgrid della collezione (`.doc-collection`): segue la
  larghezza che il registro RICEVE (container query `wscase`): sei colonne da 66rem, cinque con l'attore sotto il
  titolo da 52rem, scheda sotto 52rem (lo stesso markup, posto con `order`).
- **Contratto**: `row` (una voce di `documents.presenters.register_rows` / `register_for_case`: id, title, words,
  mandatory, current, version_count, health, state, state_label, state_reason, action_blocked, responsible,
  responsible_note, responsible_glyph, due_date, urgency, due_word, act {label, url, glyph, aria_label} oppure None,
  detail_url).
- **Varianti**: la scheda sotto 52rem di registro è la stessa riga; il gruppo «À faire» porta il filetto di 3 px del
  suo colore sul bordo di lettura.
- **Accessibilità**: `<li>` di una lista `role="list"` dentro una sezione titolata per gruppo; il titolo della pièce è
  il link (descritto dalla nota, quando c'è); ogni zona dice il suo nome alle tecnologie assistive («État»,
  «Responsable», «Échéance», nascosti alla vista); la scadenza è un `<time>` isolato da sinistra a destra; l'urgenza è
  parola + glifo, mai colore solo; l'azione nomina ciò che fa e porta `aria-describedby` verso il titolo; il titolo in
  un'altra lingua della pagina è isolato (`lang`, `dir`) sul bordo di lettura; la freccia di apertura è decorativa e
  si specchia in arabo.
- **Usato in**: `templates/documents/partials/register.html`.
- **Esempio reale — `templates/documents/partials/register.html`**:

```django
{% for row in group.rows %}{% include "components/document_row.html" with row=row %}{% endfor %}
```

#### `drawer.html`

- **Scopo**: il pannello laterale del sistema degli overlay (piano V5.4 §1.14; W2-A): la navigazione dal bordo di
  lettura, un dettaglio dal bordo finale. Un `<dialog>` nativo che `overlay.js` apre: «Slide» — tutto il pannello
  viaggia dal suo bordo, opaco, in 320 ms sulla curva d'entrata, ed esce in 200 ms sulla curva di layout, lo scrim con
  lui. Modale per default (sopra l'unico scrim, la trappola in script, `aria-modal`; Esc, lo scrim, «Fermer» o un link
  al suo interno lo chiudono); `modal=False` è il pannello ACCANTO alla lista sul desktop (`show()`: niente scrim, la pagina resta
  usabile; Esc, «Fermer» e Indietro), uno sheet modale sul telefono.
- **Blocco CSS**: `.overlay` con `.overlay--drawer` (`data-overlay-edge="start"` per il bordo di lettura), in
  `static/css/v5/overlays.css`; la testa, il corpo e il piede del componente — e lo sheet modale del pannello accanto
  alla lista sul telefono — sono del parziale solo di pagina `static/css/v5/_overlay-panels.css`: la pagina che usa
  il componente collega `css/dist/core/overlay-panels.css` (§2.1). Il cassetto della console non lo collega: ha la sua
  testa (`.console-drawer__head`).
- **Contratto**: `id` (obbligatorio); `title`; `body` (HTML sicuro) — oppure `body_template`; `actions` (HTML sicuro
  del piede) — oppure `actions_template`; `edge` = "start" (la navigazione, dal bordo di lettura; per default il bordo
  finale, un dettaglio); `modal` (False → accanto alla lista); `history` (True → l'apertura aggiunge una voce di
  cronologia e Indietro chiude il drawer; un cambio di contenuto la sostituisce); `return_id`.
- **Varianti**: 420 px (`--drawer-w`), tutta l'altezza, angoli di 12 px sul solo bordo libero; il viaggio è
  `calc(100% · bordo · --dir)`, quindi in arabo la navigazione viene da destra e un dettaglio da sinistra; ≤ 40rem un
  drawer modale prende tutta la larghezza, quello accanto alla lista si apre come sheet modale.
- **Accessibilità**: `aria-labelledby` → il titolo; il fuoco va alla voce corrente (`aria-current`), altrimenti al
  primo controllo, portato nella vista del pannello quando la lista lo nasconde (la pagina dietro non scorre mai);
  quello accanto alla lista va al proprio titolo; torna all'apritore; modale, la pagina dietro esce dall'albero
  dell'accessibilità (`aria-hidden`) finché è aperto; «Fermer» 44 px sempre presente; da tastiera nulla si anima;
  sotto il moto ridotto una sola opacità, nessun viaggio.
- **Usato in**: il cassetto della console sotto 64rem (`templates/partials/portal_chrome.html`: lo stesso
  `<dialog>` sui ganci del sistema — `overlay overlay--drawer`, `data-overlay="drawer"`, dal bordo di lettura —,
  con le sue misure e la sua notte, 320 px / 88vw, in `v5/_shell.css`; «Menu» il suo apritore `href`, §11.6);
  `templates/dev/designpreview/specimens/overlays.html` (la navigazione dal bordo di lettura, il dettaglio accanto
  alla lista con la sua voce di cronologia).
- **Esempio (dal commento di contratto del componente)**:

```django
<a href="#detail" data-overlay-open>{% translate "Mes documents" %}</a>
{% include "components/drawer.html" with id="detail" title=title modal=False history=True body_template="documents/_detail.html" %}
```

#### `empty_state.html`

- **Scopo**: stato vuoto di liste e ricerche.
- **Blocco CSS**: `.empty-state` (`__icon`, `__title`, `__text`).
- **Contratto**: `title`; `text` (opzionale); `action_label` + `action_url` (opzionali); `icon`
  (default `document`).
- **Varianti**: nessuna. **In contrasto con la direzione**: oggi è un riquadro tratteggiato centrato
  con un'icona. La direzione A vuole al suo posto un filetto e una frase allineata a sinistra che
  nomina chi riempie la regione e quando, con l'azione risolutiva in linea (§9). `.empty-state__icon`
  è sulla lista di demolizione.
- **Accessibilità**: `role="status"`; il titolo è un `<p>` (non altera la gerarchia dei titoli).
- **Usato in**: `templates/accounts/profile.html`, `templates/news/index.html`,
  `templates/glossary/index.html`, `templates/partners/index.html` (e almeno altri 15 template; 17
  al momento dell'ultima verifica).
- **Esempio reale — `templates/accounts/profile.html`**:

```django
{% include "components/empty_state.html" with title=_("Aucune organisation") text=_("Votre compte n’est rattaché à aucune organisation pour le moment.") %}
```

#### `entrances.html`

- **Scopo**: i **quattro accessi** dell'ecosistema (Persona, Impresa, Istituzione, Università).
  Esattamente quattro, mai di più (R-ECO-001). **Il primo componente riscritto sulla direzione A**:
  non più quattro colonne identiche con quattro illustrazioni, ma un registro di quattro entrate
  (§8.4). Il pattern precedente era quello vietato due volte insieme — «una sezione di schede
  identiche» e «ogni scheda con la sua icona» — e dava alle porte dell'ecosistema il trattamento di
  una griglia di servizi qualunque.
- **Blocco CSS**: `.register` con il modificatore `.register--entrances`, righe `.entry`
  (`__title`, `__gloss`, `__cta`, `__arrow`); dal 9 ottobre 2026 (V5.4, W2-D passo 3) le regole sono
  nel foglio di pagina della home, `apps/pages/static/pages/css/pages.css`, sui token V5
  (`v2/routes.css`, il «molo a zig-zag», è cancellato). Le regole `.entrances` e `.entrance` di
  `components.css` non hanno più consumatori nella home (`.entrance` è oggi il layout d'ingresso di
  `templates/allauth/layouts/entrance.html`) e vanno cancellate con la migrazione di quel file.
- **Contratto**: `entrances` (opzionale) = lista di 4 dict `{title, text, button, url, lang, actor}`; se
  omessa il componente rende i quattro blocchi prescritti dal registro (`p3.entrances.*`) con i link
  `pathways:index`, `ecosystem:companies`, `ecosystem:institutions`, `ecosystem:universities` (via
  `safe_url`: un accesso la cui destinazione non esiste ancora è mostrato senza link invece che
  nascosto). `heading_level` = `"h2"` (default) o `"h3"`.
- **Gate**: i testi `p3.*` sono di Fase 3 — chi include il componente senza `entrances` deve farlo
  solo con `gates.phase3_public` aperto. Quando un gate si chiude cambia la **destinazione**, non la
  presenza della riga.
- **Varianti**: `.register--entrances`. Una cornice, quattro righe (due campate da 48rem): filetto
  di struttura sopra la prima, capello fra le righe; ogni riga è il titolo prescritto (15/20 a 600,
  maiuscole del testo stesso), la frase (15/24; 16/24 sotto 64rem) e l'invito con la sua freccia accanto
  alle parole — l'unico segno d'avanzamento del blocco. **Nessun ordinale e nessun glifo di rilievo** (V5.4,
  W2-D passo 3; DESIGN_SYSTEM_V5 PX02: i quattro non sono in classifica): l'ordinale `01`–`04` e i quattro
  glifi di V2 (il partial dei glifi di rilievo della home, cancellato) sono ritirati, come lo furono
  le quattro illustrazioni (§14.1). Sotto l'hero V5.4 il registro **non è disegnato dove l'hero porta già
  parola, frase e invito** (desktop e tablet: la regola è di `hero.css`, DL54-40), e sui telefoni è l'unica
  copia delle quattro frasi; lì il suo attacco, che nominerebbe i quattro una terza volta, non è disegnato.
- **Accessibilità**: `<ol>` senza nome proprio (la sezione che lo include è etichettata dal suo titolo; il
  `nav` dell'hero porta già «Les quatre accès de l’écosystème»); tutta la riga è un solo link, quindi un
  solo tab stop e il titolo come nome accessibile; `lang` sul singolo testo in fallback francese; la freccia
  è decorativa e si specchia in arabo (`icon--flip-rtl`).
- **Usato in**: `templates/pages/home/_entrances.html`. La home passa sempre la lista `entrances`
  costruita da `pages.services` e `heading_level="h3"` perché il titolo di sezione è l'`h2`.
- **Esempio reale — `templates/pages/home/_entrances.html`**:

```django
{% include "components/entrances.html" with entrances=d.entrances heading_level="h3" %}
```

#### `form_errors.html`

- **Scopo**: riepilogo degli errori in cima al form (WCAG 3.3.1).
- **Blocco CSS**: `.form-errors` (sopra `.notice.notice--error`).
- **Contratto**: `form` (Django Form). Rende gli errori non di campo e una lista di link
  `#<id_for_label>` verso ogni campo visibile in errore.
- **Varianti**: nessuna.
- **Accessibilità**: `role="alert"`, `tabindex="-1"`, `id="form-errors"`: al caricamento `main.js`
  (`initFormErrorFocus`) vi porta il focus e lo scorre al centro del viewport (G-05, chiusa il
  20/09/2026). Senza JS il riepilogo resta in cima al form, con `role="alert"`.
- **Usato in**: `templates/allauth/elements/form.html`.
- **Esempio reale — `templates/allauth/elements/form.html`**:

```django
{% if attrs.form %}{% include "components/form_errors.html" with form=attrs.form %}{% endif %}
```

#### `form_field.html`

- **Scopo**: **unico** modo di rendere un campo: etichetta, controllo, aiuto, errori.
- **Blocco CSS**: `.form-field` (`__label`, `__required`, `__help`, `__aside`, `__check`, `__control`, `__toggle`,
  `__errors`, `__error-list`).
- **Contratto**: `field` (BoundField); `help` (sostituisce `help_text`); `consent` (True → stile del
  consenso obbligatorio, mai pre-spuntato; attivato anche dalla classe widget `consent-checkbox` di
  `core.forms.ConsentBooleanField`). Il comando mostra / nascondi di una password è il glifo del sistema
  (`v5/field.css` §5: un solo nome che non cambia, `aria-pressed` come solo canale); `shell.js` §3 tiene il
  cursore (W2-B); senza script l'ingresso non lo disegna (`entrance.css`). **La casella della riga
  dell'etichetta** (W2-B): un campo il cui form imposta `help_beside_label` (`accounts.forms.LoginForm`, sulla
  password) ha il suo aiuto come `.form-field__aside`, scritto DOPO il controllo — l'ordine della tastiera — e
  collocato alla fine della riga dell'etichetta dal foglio che lo disegna (`entrance.css`); conserva l'id
  dell'aiuto, quindi il campo ne resta descritto. L'aiuto è un `<div>`: un aiuto può essere un blocco (le regole
  di una nuova password sono una lista), e una lista scritta in un `<p>` lo chiudeva.
- **Varianti**: `.form-field--error` (il bordo del controllo raddoppia, 2 px in granata, e ogni messaggio porta
  una marca disegnata: mai il solo colore), `--required`, `--consent` (la riga del consenso, senza riquadro).
  Il controllo è «la lastra» di `static/css/v5/field.css`: 44 px in console, 52 px sulle pagine pubbliche,
  testo digitato a 16 px; al focus l'anello del sistema — con l'alone di 5 px sulle pagine pubbliche; in console
  l'area di lavoro tiene il suo compagno di 2 px (`v4/workspace.css`) — e un filetto di 2 px che si disegna dal
  bordo di lettura. L'asterisco è legato all'ultima parola dell'etichetta da uno spazio indivisibile: non va
  mai a capo da solo. I widget nascosti
  sono resi nudi; il campo honeypot `website_url` va nel wrapper fuori schermo `.hp-wrap` con
  `aria-hidden="true"`.
- **Accessibilità**: contratto completo in `docs/ACCESSIBILITY.md` §6. In breve: `<label for>` sempre
  presente; asterisco `aria-hidden` + attributo `required`; Django 5.2 aggiunge `aria-invalid="true"`
  e `aria-describedby="<auto_id>_helptext <auto_id>_error"` e il componente usa **esattamente quegli
  id**; lista errori con `role="alert"`; checkbox con etichetta cliccabile a fianco.
- **Usato in**: `templates/allauth/elements/fields.html`, `templates/accounts/profile.html`,
  `templates/forum/partials/registration_form.html`, `templates/documents/partials/depot.html` (e
  almeno altri 9).
- **Esempio reale — `templates/accounts/profile.html`**:

```django
{% for field in form.visible_fields %}{% include "components/form_field.html" with field=field %}{% endfor %}
```

#### `form_unavailable.html`

- **Scopo**: sostituisce **ogni** form pubblico finché il gate G2 (`core.gates.public_forms_enabled()`)
  è chiuso, cioè finché i testi legali ufficiali italiani non sono pubblicati.
- **Blocco CSS**: `.form-unavailable` (sopra `.notice.notice--pending`).
- **Contratto**: nessuna variabile; usa `site.contact_email` (unico indirizzo pubblico).
- **Varianti**: nessuna.
- **Accessibilità**: `role="status"`; icona `clock` decorativa; il messaggio offre sempre
  l'alternativa e-mail. Hook di test: `data-gate="forms-closed"`.
- **Usato in**: `templates/enquiries/contact.html`, `templates/enquiries/collaboration_proposal.html`,
  `templates/forum/register.html`, `templates/news/_newsletter.html`, `templates/community/join.html`
  (e almeno altri 6).
- **Esempio reale — `templates/enquiries/contact.html`**:

```django
{% if not forms_open or not form %}
  {% include "components/form_unavailable.html" %}
```

#### `hero.html`

- **Scopo**: apertura tipografica di pagina. **In uscita**: la direzione A conosce tre aperture — la
  lastra (§8.6), il blocco titolo e la sola linea di folio — e `hero.html` è l'antenato della prima.
- **Blocco CSS**: `.hero` (`__content`, `__eyebrow`, `__rule`, `__title`, `__subtitle`, `__body`,
  `__actions`, `__figure`).
- **Contratto**: `title` (obbligatorio); `eyebrow`, `subtitle`, `body`; `lang`; `primary_label` +
  `primary_url`; `secondary_label` + `secondary_url`; `illustration` (percorso statico di un SVG
  decorativo → layout `.split`); `variant`; `heading_level` (`"h1"` default, `"p"` quando la pagina ha
  già il suo `h1`).
- **Varianti**: `.hero--editorial` (default), `.hero--inverse` (navy, aggiunge `.on-inverse`, bottoni
  `.btn--inverse`), `.hero--muted`, `.hero--compact`. Lo slot `__eyebrow` è **abolito** dalla
  direzione: va sostituito dal folio. **Mai due lead**: la home respinta metteva due paragrafi
  consecutivi che dicevano la stessa cosa in due caratteri e a due corpi.
- **Accessibilità**: `<section aria-labelledby="hero-title">` — `id` fisso: **un solo hero per
  pagina** (G-13); filetto `aria-hidden`; illustrazione `alt=""`, `loading="eager"`, dimensioni
  esplicite (niente CLS); titolo limitato a 18ch.
- **Usato in**: nessuna pagina — nessun `{% include %}`; dal primo passo di W3-F1 `templates/pathways/detail.html`
  non usa più `.hero__figure` (l'immagine di un percorso è `.pathway-figure`). Le sue regole (`components.css` §10)
  sono uscite col passo di bilancio di W3-F1 (12 ottobre 2026); il file resta, senza disegno, per W4-D. Fino al
  5 ottobre 2026 anche `templates/pages/home/_hero.html` (markup diretto con le stesse classi): dall'8 ottobre l'hero
  V5.4 ha le proprie classi (`.he`, `.he__*`, `.he-*`, in `apps/pages/static/pages/css/hero.css`).
- **Esempio (dal contratto)**:

```django
{% include "components/hero.html" with title=hero.title subtitle=hero.subtitle lang=hero.lang primary_label=hero.button primary_url=hero.url variant="editorial" %}
```

#### `institutional_banner.html`

- **Scopo**: fascia informativa sotto l'header (es. banner del Forum fino al 2 ottobre 2026, gate
  `forum_banner_visible()`), nel blocco `banner` di `base.html`. Non è un popup e non è dismissibile.
- **Blocco CSS**: `.institutional-banner` (`__inner`, `__title`, `__meta`, `__quote`, `__actions`).
- **Contratto**: `title`; `meta` (data/luogo), `quote`, `button_label` + `button_url` (opzionali);
  `lang`; `label` (aria-label della regione, default = `title`).
- **Varianti**: nessuna. Una colonna → tre colonne (≥ 64rem).
- **Accessibilità**: `<section role="region" aria-label>`; titolo come `<p>` (non entra nella
  gerarchia dei titoli); citazione in `<blockquote>`.
- **Usato in**: nessun consumatore. Il banner del Forum sulla home non usa questo componente: il
  partial `_banner.html` della home avvolge il partial dell'app `forum` in un blocco `.home-banner`
  con un bottone «Masquer cette annonce» aggiunto solo da JavaScript (§2.1); resta una fascia in
  flusso, mai un overlay.
- **Esempio (dal contratto)**:

```django
{% block banner %}{% if gates.forum_banner_visible %}{% include "components/institutional_banner.html" with title=banner.title meta=banner.meta quote=banner.quote button_label=banner.button button_url=banner.url lang=banner.lang %}{% endif %}{% endblock %}
```

#### `glyph.html`

- **Scopo**: il disco con il glifo di un ATTORE (persona, impresa, istituzione, università, scudo per
  un'autorità) accanto al suo tipo e, quando esiste, al nome reale (design V4, `DESIGN_SYSTEM_V4.md` §8.6).
  Mai una fotografia di persona, mai il glifo da solo: le parole le stampa chi lo include.
- **Blocco CSS**: `.glyph` (`__icon`; modificatori `--sm` 24, `--md` 32, `--lg` 40, `--dark`, `--none` =
  disco tratteggiato per un attore senza glifo), in `v4/workspace.css`.
- **Contratto**: `glyph` (id dello sprite, può essere vuoto); `size` (opzionale: `sm` · `md` · `lg`); `dark`
  (opzionale, su navy). I glifi degli attori vengono da `documents.requirements.ACTOR_GLYPHS`: person · company = building · authority = shield · professional = briefcase · training_body = university · authorised_actor = handshake · project_team = institution (revisione del gate E).
- **Varianti**: tre misure, scuro, senza glifo.
- **Accessibilità**: decorativo, `aria-hidden`; il testo accanto porta l'informazione.
- **Usato in**: `templates/components/document_row.html`, `templates/portal/dashboard.html`.
- **Esempio reale — `templates/components/document_row.html`**:

```django
{% include "components/glyph.html" with glyph=row.responsible_glyph size="sm" %}
```

#### `health_strip.html`

- **Scopo**: lo stato delle pièce di un fascicolo come UNA barra di segmenti proporzionali — uno per stato,
  nell'ordine dell'enum, col registro dello stato — e sotto i conteggi come parole («7 pièces demandées ·
  1 sur 7 validées · 4 en attente») (design V4, `CREATIVE_DIRECTION.md` §3.5.2). La barra è decorativa sopra
  le parole. Dal design V5 la pagina «Mes pièces» non la disegna più: il suo registro è la striscia «il registro»
  (tre corse per chi deve agire, `documents/partials/register.html`, W3-C) e il filtro di stato ne è la legenda; la
  barra resta al fascicolo, sopra la sua checklist, finché la famiglia del fascicolo (W3-E) non la ridisegna.
- **Blocco CSS**: `.health` (`__strip`, `__segment`, `__counts`, `__n`, `__sep`, `__open`), in
  `v4/workspace.css`; la larghezza dei segmenti viene da `data-share` letto con `attr()`
  tipizzato (ripiego: segmenti uguali). I segmenti portano **le marche dei chip**, per gli otto registri: leggono
  `--chip-mark` e `--chip-pattern`, che `[data-register]` ripunta (`static/css/v5/tokens.css`) — mai il
  verde di un verdetto, mai l'accento (revisione del gate C) — con un canale non cromatico: tratteggio su
  «attesa», punti su «rifiuto», tratteggio incrociato su «blocco»; «nullo» è un contorno.
- **Contratto**: `counts` (`documents.requirements.counts`: total, valid, open, per_state); `filters`
  (`documents.presenters.state_filters`: value, label, count, register — nell'ordine del registro, `STATE_ORDER`);
  `compact` (opzionale, non più chiamato: le parole più piccole del cruscotto V4, la cui regola è uscita con lui —
  W3-B); `bare` (opzionale: la sola barra, quando le parole accanto sono della pagina — la checklist del fascicolo, il
  cui conteggio è «éléments complétés», da `cases.presenters.checklist_health`).
- **Varianti**: `bare` nel fascicolo.
- **Accessibilità**: la barra è `aria-hidden`, i conteggi sono testo; ogni segmento porta colore E registro
  (`title` = parola · conteggio).
- **Usato in**: `templates/cases/detail.html`.
- **Esempio reale — `templates/cases/detail.html`**:

```django
{% include "components/health_strip.html" with counts=checklist_health.counts filters=checklist_health.filters bare=True %}
```

#### `journey_rail.html`

- **Scopo**: il viaggio **«La soglia»** alla densità della console (design V5, W3-D, §11.9; piano V5.4 §3.5 voce 6,
  §1.18 D16): le sette tappe bloccate di un fascicolo (`portal.services.JOURNEY_STEPS`) su una linea in piano fra le
  due rive, «Maroc» e «Italie», attraversata da due soglie — A, le autorità competenti (`stamp`), B, il territorio
  italiano (`ile-arch`), ciascuna con la didascalia di giurisdizione del sito. **Una soglia è un luogo**: un fascicolo
  in `SELECTION` vi sta sopra (OJ2) e la voce corrente della lista è allora la soglia. Una sola lista, un solo DOM;
  il verso lo decide la larghezza **del componente** (una container query a 56rem), mai il template: la linea in
  piano, oppure la carta — ciò che è vero ORA (la tappa con il suo glifo, il suo rango «Étape n sur 7», «Vous êtes
  ici»; su una soglia la sua didascalia apre la carta al posto del rango: dove sta quella fase) e la lista dietro la
  divulgazione nativa «Où j’en suis», chiusa, come spina. «Vous êtes ici» è della voce corrente, e solo sua: un
  fascicolo il cui stato non ha posto sulla linea (`SUSPENDED`, `CLOSED`: la pastiglia della testata dice lo stato)
  non ha voce corrente e nulla lo dice; nel fascicolo le tappe che il registro ha raggiunto sono dietro di lui,
  datate, e la voce dove si è fermato (`--stop`) non disegna linea percorsa oltre. Fermo al caricamento: la linea
  percorsa, l'anello e «Vous êtes ici» sono dipinti dal primo frame, nulla si muove (D16: «in V5.4 the rail is
  drawn still at load, with no relay»).
- **Blocco CSS**: `.journey` (`__step`, `__threshold`, `__shore`, `__node`, `__label`, `__gate`, `__now`, `__here`,
  `__when`, `__actor`; modificatori di stato `--done`, `--current`, `--upcoming`, `--stop`, di posto `--1` … `--7`,
  `--a`, `--b`, `--start`, `--end`, di lista `--descriptive`, `--on-a`), più `.journey-rail` (il contenitore della
  query), `.journey-now` (la carta) e `.journey-fold` (la divulgazione), in
  `apps/portal/static/portal/v5/_journey-rail.css` §1–§4, sul vocabolario di `v5/_journey-nodes.css` (i parziali del
  foglio di sola pagina `portal/journey.css`, §2.1); `.journey-page` (§6) lo colloca in testa alla pagina «Mon parcours». Il vocabolario: dietro il fascicolo un
  punto d'inchiostro di 10 px (mai una spunta, O14), dove sta un anello laguna di 18 px sul suo velo (un disco, non
  un'ombra), avanti un anello aperto di 12 px; la linea di 2 px laguna dov'è passato il fascicolo, il filetto
  decorativo avanti — ogni voce disegna il tratto dal suo nodo a quello della voce dopo, l'ultima tappa fino alla
  fine del binario sotto «Italie» (le rive sono i due capi della linea): nessun gradiente, nessuna misura, nessuno
  script.
- **Contratto**: `steps` (`portal.services.journey_for`: status, label, side, state, is_current, stop, frontier,
  threshold, detail, actor — o `cases.presenters.journey_with_dates`, che aggiunge `reached_at` e quello della
  soglia su cui il fascicolo sta e, per un fascicolo fuori dalla linea, le tappe che il registro ha raggiunto, `stop`
  sull'ultima); `label` (il nome accessibile della lista e le parole della divulgazione);
  `descriptive` (opzionale: il fascicolo — la spina a ogni larghezza, accanto a ogni tappa raggiunta la data in cui
  lo è stata, quando il registro la conosce; una tappa non raggiunta non ha data, e nessuna inventata).
- **Varianti**: la linea in piano (≥ 56rem del componente: il cruscotto da 64rem), la carta e la sua divulgazione
  (< 56rem: il telefono, il tablet, una colonna stretta), `descriptive` nel fascicolo. Dove un browser non sa disporre un
  `<details>` chiuso (`::details-content`), la carta e la divulgazione restano a ogni larghezza: nulla è nascosto.
- **Accessibilità**: `<ol>` semantico col suo nome; sette voci esposte, otto quando il fascicolo sta su una soglia
  (la voce corrente è allora la soglia); le rive e la soglia che non è il posto del fascicolo sono `aria-hidden` —
  la didascalia di questa è detta, nascosta, nella tappa che apre; `aria-current="step"` su una sola voce; ogni stato
  è una parola o una forma, mai il colore solo; un marcatore per colonna (D16): il glifo della fase, nessun numero
  (il numerale è del passaggio pubblico), nessuna spunta; il riepilogo della divulgazione di 44 px; a colori forzati
  linee e nodi nei colori di sistema, il velo tolto.
- **Usato in**: `templates/portal/dashboard.html`, `templates/portal/pathways.html`, `templates/cases/detail.html`.
- **Esempio reale — `templates/portal/dashboard.html`**:

```django
{% include "components/journey_rail.html" with steps=journey label=journey_label %}
```
#### `jurisdiction.html`

- **Scopo**: la **barra di giurisdizione** (§8.7) — chi risponde di ciascun tratto di un processo.
  L'unico innesto che tutti e quattro i giudici del Design Council hanno nominato per proprio conto,
  perché codifica la **giurisdizione** e non la sequenza, e la giurisdizione è il soggetto reale di
  questo progetto.
- **Blocco CSS**: `.jurisdiction` (`__title`, `__bar`, `__segment`, `__legend`, `__key`, `__swatch`,
  `__caption`) — in `static/css/register.css`.
- **Contratto**: `segments` = lista di dict `{owner, label, share}`, dove `owner` ∈
  `morocco | italy | platform | authority` e `share` è un intero da 1 a 6 (larghezza relativa del
  tratto); `title` e `caption` opzionali.
- **Varianti**: `.jurisdiction__segment--morocco`, `--italy`, `--platform`, `--authority`. Quattro
  responsabili, quattro **tratteggiature**: la texture non è decorazione, è l'equivalente per chi non
  può usare il colore (§1.4). La larghezza viaggia in `data-share`, **mai in uno stile inline**: la
  CSP pubblica è `self` senza `unsafe-inline` e un attributo `style` verrebbe scartato in produzione,
  lasciando quattro segmenti uguali.
- **Accessibilità**: la barra è un `role="img"` con etichetta; la legenda è una `<ul>`, quindi uno
  screen reader legge responsabili e tratti in ordine; i campioni sono `aria-hidden` perché
  ripetono la parola che hanno accanto; sotto `forced-colors` le tratteggiature cadono e restano
  bordi e legenda.
- **Usato in**: nessun template, dal 9 ottobre 2026. Chiudeva il capitolo della trasparenza della home; con
  l'hero V5.4 era il terzo disegno della stessa cosa sulla stessa pagina — il modello Marocco → Italia, dal paese
  d'origine al territorio italiano — sotto il sentiero dell'hero e la rotta del progetto pilota, e il passo 3 di
  W2-D lo dice una volta sola, nell'hero (DL54-41). Il componente, le sue regole e i dati
  (`pages.services.jurisdiction_segments`, ancora nel contesto del capitolo) restano: rimetterlo è una riga.
- **Esempio — l'inclusione com'era nel capitolo della trasparenza della home**:

```django
{% include "components/jurisdiction.html" with title=jurisdiction_title caption=jurisdiction_caption segments=d.jurisdiction %}
```

#### `language_segmented.html`

- **Scopo**: il controllo lingua (piano V5.4 §1.11): quattro link, ciascuno col nome della sua lingua nella sua
  lingua. Link puri, nessuno script: scegliere una lingua è una navigazione.
- **Blocco CSS**: `.lang-seg` (`__list`, `__list--names`, `__item`, `__link`, `__code`, `__name`), in
  `v5/chrome.css` (W2-C1): nella barra istituzionale i quattro nomi per esteso — Italiano · Français · English ·
  العربية, mai «ع» (DL A25) — separati da un punto disegnato, con una linea di 2 px sotto la lingua corrente (che
  risponde anche all'hover), bersagli di 24 px col puntatore fine e 44 con quello grosso (piano V5.4 §1.11); nel
  foglio del menu gli stessi nomi su carta, i loro inchiostri notturni ripuntati (§11.2; la traccia segmentata di V4
  è uscita col cassetto per cui era disegnata, W2-C2); al piede della rail della console — e del suo
  cassetto, che ne porta il piede — gli stessi quattro nomi, in colonna, aperti sopra il controllo che porta il
  nome della lingua corrente (§11.6; W3-A).
- **Contratto**: `lang_names` (True nella barra istituzionale: i nomi visibili); usa `site.languages` (`code`,
  `name`, `url`, `active`, `dir`), come `language_switcher.html`.
- **Varianti**: nessuna: un solo disegno (`lang_names` è accettato e non cambia nulla). Sotto 80rem è il primo elemento del foglio
  (`language_switcher.html`, il `<details>` di V1, è ritirato dal 25/09/2026: revisione del gate A,
  correzione 7).
- **Accessibilità**: `<nav aria-label="Choisir la langue">`; ogni link ha `lang`, `hreflang` e `dir`
  propri e il nome della lingua per esteso, visibile; lingua attiva `aria-current="true"` + la linea di 2 px + il
  peso, mai il solo colore; bersaglio di 24 px col puntatore fine, 44 con quello grosso (SC 2.5.8). Sono link, non un
  `<select>`: nessun cambio di contesto su input (SC 3.2.2).
- **Usato in**: `templates/partials/utility_bar.html`, `templates/partials/main_nav.html` (in testa al
  foglio sotto 80rem), `templates/portal/partials/rail_nav.html` (il piede della rail della console, nella rail e nel suo cassetto). La direzione lo voleva nella testata: misurato a 1440, le sette sezioni del
  menu CMS (905 px) più il lock-up (303 px) non lasciano spazio a un controllo da 152 px in una riga
  da 1240 — finché l'architettura resta a sette voci, sta nella barra istituzionale.
- **Esempio reale — `templates/partials/utility_bar.html`**:

```django
{% include "components/language_segmented.html" %}
```

#### `loader.html`

- **Scopo**: il loader «Lume» — il marchio a strati, l'host di L1 (piano V5.4 §1.9; DL54-07, DL54-08, DL54-09; W1-D).
  Il marchio verbatim (`docs/design-v2/BRAND_ASSETS.md` §1) negli strati che `v5/loader.css` colloca nelle sue unità:
  la base — i due piani tricolori, la porta ad arco, i tre gradini —, la stanza dietro la porta con la sua luce, la
  chiave d'oro col suo gemello d'inchiostro. A riposo è, pixel per pixel, il marchio di un solo file: l'anello della
  chiave lascia vedere la porta navy. Due gesti, un solo movimento diviso dalla navigazione (DL54-07): l'INGRESSO — la
  chiave gira una volta sul proprio gambo e tiene, all'invio del login (`loader.js` `engage()`, `.is-engaged`) — e il
  RILASCIO — la porta che si illumina dall'occhio della chiave, la chiave che si legge in inchiostro, poi il ritorno al
  marchio verbatim, sulla prima pagina della console dopo un accesso riuscito, una volta per sessione (`release=True`,
  `data-lume="release"`: un'animazione CSS del parziale `_loader-light.css` della sola console, che parte al primo
  frame e non ha bisogno di script). I piani, la porta e i gradini non si muovono mai; la chiave non è mai tenuta,
  disegnata o servita specchiata; l'host è `direction: ltr` in ogni lingua.
- **Blocco CSS**: `.sig` (`__l`, `__base`, `__room`, `__lume`, `__key`, `__turn`, `__face`, `__face--ink`), in
  `v5/loader.css`; il rilascio in `v5/_loader-light.css` (generato da `scripts/gen_loader_light.py`); la riga delle
  parole `.loader__status` e il comando `.loader__retry`.
- **Contratto**: `release` (il seggio della console: il rilascio al caricamento), `id` (lo nomina un form
  nell'attributo data-loader-host per l'ingresso all'invio; la riga di stato è `<id>-status`), `css_class`, e le parole
  di un'attesa lunga, `word` (1 s), `slow` (10 s), `retry` («Réessayer»), scritte dal template che include con le
  proprie traduzioni: il componente non porta stringhe sue, e il seggio del rilascio non ne ha.
- **Varianti**: la misura è `--sig-size` del consumatore (160 px; la rail 24 e la barra 20 da `_loader-light.css`); un
  palcoscenico passa il proprio viewBox in `--vx --vy --vw --vh` e colloca la chiave nel suo riquadro.
- **Accessibilità**: decorativo (`aria-hidden`): lo stato lo portano l'`aria-busy` del controllo e la riga
  `role="status"`; sotto `prefers-reduced-motion: reduce` ogni token vale 0 ms e il marchio mostra il fermo — lo stato
  finale del rilascio, senza tragitto; nulla gira in loop e nulla dura più di 1,6 s (2.2.2); sotto colori forzati
  niente luce né inchiostro, il marchio tiene i suoi colori. `docs/ACCESSIBILITY.md` §7.
- **Usato in**: `templates/partials/portal_chrome.html` (il seggio del rilascio: la tegola della rail e quella della
  barra, altrimenti l'`<img>`), `templates/dev/designpreview/specimens/loader.html`; l'ingresso del login (W2-B) e la
  chiave dell'hero (W2-D) sulla stessa primitiva.
- **Esempio reale — `templates/partials/portal_chrome.html`**:

```django
<span class="rail__tile" aria-hidden="true">{% if lume_release %}{% include "components/loader.html" with release=True %}{% else %}<img src="{% static 'brand/original/logo-mark.svg' %}" alt="" width="24" height="24" decoding="async">{% endif %}</span>
```

#### `local_nav.html`

- **Scopo**: navigazione locale di una sezione (colonna laterale). È l'antenato dell'**indice locale
  del rail** (§8.2).
- **Blocco CSS**: `.local-nav` (`__title`, `__list`, `__link`).
- **Contratto**: `items` = lista di dict `{label, url, current (bool), children (stessa forma)}`;
  `title` (opzionale); `label` (aria-label, default = `title`).
- **Varianti**: desktop = colonna con filetto e voce corrente marcata (avvolgerla in
  `.layout-sidebar__aside` per renderla sticky); sotto 64rem = lista di pastiglie. **Da correggere**:
  sotto `lg` deve diventare un filetto segmentato scorrevole alto 44 px, non una nuvola di pastiglie
  da 999 px — oggi `.local-nav__link` è alto 34 px su telefono e tablet e 40 px a 1280, cioè la
  navigazione *rimpicciolisce* quando si passa dal mouse al dito.
- **Accessibilità**: `<nav aria-label>`; voce corrente `aria-current="page"` + grassetto + filetto.
- **Usato in**: nessuna pagina. Nessuna pagina lo include più (la colonna laterale di «Diplômes et titres» e di «Formation» è uscita col secondo passo di
  W3-F1: le loro aree sorelle sono un registro di chiusura, «Dans l'Espace Personnes»): dall'11 ottobre 2026 (V5.4, W3-F1, l'interno pubblico) gli spazi dell'ecosistema e le pagine istituzionali non hanno più colonna
  laterale — gli spazi fratelli sono le porte della navigazione («Il portico») e una pagina non ripete la
  sua cromatura. Dal design V4 la console non lo usa più: la rail (`partials/portal_chrome.html`) l'ha
  sostituito; dal design V5 nemmeno le pagine del conto, che hanno la loro lista delle sezioni (W3-F2, passo 2). Le
  sue regole (`components.css` §24) sono uscite col passo di bilancio di W3-F1 (12 ottobre 2026); il file resta, senza
  disegno, per W4-D.
- **Esempio (dal contratto)**:

```django
{% include "components/local_nav.html" with items=local_nav_items title=_("Les espaces de l’écosystème") %}
```

#### `metadata_row.html`

- **Scopo**: riga di metadati (data, luogo, categoria, ultima revisione). È il materiale della nota
  marginale (§8.5): posizione, autorità, data.
- **Blocco CSS**: `.meta-row` (`__item`), in `static/css/v5/card.css`.
- **Contratto**: `items` = lista di dict `{label, value, icon, datetime (ISO → <time>), url}`.
- **Varianti**: nessuna.
- **Accessibilità**: `<dl>` con coppie `<dt>`/`<dd>`; date in `<time datetime>` (cifre tabulari da
  `base.css`, §6.8). Il separatore « : » dopo `<dt>` è contenuto CSS con tipografia francese, non
  localizzato (G-14).
- **Usato in**: `templates/pathways/_review_meta.html` (markup diretto `.meta-row`, senza glifo: la natura e
  l'ultima verifica di una scheda dell'Espace Personnes, di «Diplômes et titres» e di «Formation», nell'ingresso).
  La riga con i suoi due glifi è uscita col secondo passo di W3-F1.
- **Esempio (dal contratto)**:

```django
{% include "components/metadata_row.html" with items=event_meta %}
```

#### `notice.html`

- **Scopo**: messaggi in pagina (informazione, esito, avvertenza, errore, attesa, nota
  istituzionale). È una delle **due sole superfici in scatola** del sistema (§9).
- **Blocco CSS**: `.notice` (`__icon`, `__title`, `__body`); alias `.alert` per i messaggi Django.
- **Contratto**: `kind` ∈ `info | success | warning | error | pending | institutional` (default
  `info`); `title` (opzionale); `text` (str o HTML sicuro); `icon` (default per tipo: `info`, `check`,
  `warning`, `clock`); `lang`.
- **Varianti**: `.notice--info/success/warning/error/pending` — i registri del piano V5.4 §1.2 in
  `static/css/v5/notice.css`: lavaggio del registro e filetto `inline-start` di 3 px, **pieno** per
  informazione (ardesia), attesa (lapis) e fatto compiuto (`success`: inchiostro, mai verde — §4.3),
  **tratteggiato** per l'avvertenza (ambra), **doppio** per l'errore (granata) — e `.notice--institutional`
  (carta, cornice a filetto, marca navy, filetto oro). Mancano le tre varianti editoriali della direzione
  (**Nota**, **Importante**, **Approfondimento**).
- **Accessibilità**: `role="alert"` solo per `error`, `role="status"` per tutti gli altri; icona +
  titolo + stile del filetto (pieno, tratteggiato, doppio): il tipo non è mai comunicato dal solo colore.
- **Usato in**: `templates/community/discussion.html`, `templates/accounts/delete_request.html`,
  `templates/glossary/term.html`, `templates/living/sheet.html` (e almeno altri 18).
- **Esempio reale — `templates/community/discussion.html`**:

```django
{% translate "Discussion fermée : il n’est plus possible de répondre." as closed_text %}
{% include "components/notice.html" with kind="info" text=closed_text %}
```

#### `option_cards.html`

- **Scopo**: le scelte di una domanda a radio o a caselle come **OptionCard** (design V4,
  `CREATIVE_DIRECTION.md` §3.7, `DESIGN_SYSTEM_V4.md` §8 «OptionCard»): un `<label>` intorno all'input NATIVO;
  dal secondo passo di W3-F1 una lastra di `v5/field.css` — 4 px, un filetto, nessuna ombra —, titolo 14/20
  500; selezionata = il bordo raddoppiato nel riempimento primario, il fondo `--surface-selected` e la spunta
  della persona nel segno pieno (O14: una spunta segna l'atto della persona, mai uno stato); ≥ 52 px,
  `touch-action: manipulation`. Nessun disco con glifo:
  nessuna opzione qui ha un glifo onesto (una lingua, «oui», «non»), e uno decorativo sarebbe inventato.
- **Blocco CSS**: `.opts` (`__legend`, `__help`, `__hint`, `__grid`; modificatore `--error`) e `.opt` (`__mark`,
  `__title`), in `apps/portal/static/portal/v5/_wizard.css` (partial della console, W3-F1: uscito da `main.css` con
  `v4/wizard.css`).
- **Contratto**: `field` (un `BoundField` con `RadioSelect` o `CheckboxSelectMultiple`; ogni scelta è resa da
  `{{ choice.tag }}`, quindi tastiera, invio e validazione restano del browser).
- **Varianti**: nessuna: radio o caselle secondo il widget del campo.
- **Accessibilità**: `<fieldset>` + `<legend>` = la domanda; l'aiuto è collegato con `aria-describedby`; l'input
  è il controllo (invisibile ma a tutta scheda, focalizzabile: anello sulla scheda con `:has(:focus-visible)`);
  a colori forzati bordo `CanvasText`, selezione `Highlight`.
- **Usato in**: `templates/portal/situation.html`.
- **Esempio reale — `templates/portal/situation.html`**:

```django
{% include "components/option_cards.html" with field=field %}
```

#### `page_header.html`

- **Scopo**: intestazione standard delle pagine interne; contiene **l'unico `<h1>`**. È l'antenato
  dell'apertura B della direzione (blocco titolo, senza fascia).
- **Blocco CSS**: `.page-header` (`__eyebrow`, `__title`, `__lead`, `__meta`); include `.container`. Il disegno
  (design V5): la pagina dell'interno pubblico (`static/css/v5/_pagina.css` §2 — un disegno con l'ingresso di W3-F1)
  e la cornice della console (`apps/portal/static/portal/v5/_shell.css` §4); di `components.css` §10 resta la sola
  testata corrente in maiuscolo che la console legge (W3-F1, passo di bilancio, 12 ottobre 2026).
- **Contratto**: `title`; `eyebrow`, `lead` (opzionali); `lang`; `meta` (HTML sicuro, es. una metadata
  row); `align` (`"center"`).
- **Varianti**: `.page-header--center` (senza disegno: nessun chiamante la usa, e la sua regola è uscita col passo
  di bilancio di W3-F1). Lo slot `__eyebrow` è abolito (§8.2). Il titolo va reso in
  **minuscolo per CSS**: un redattore non deve poter cambiare l'identità digitando maiuscole nel CMS
  (§6.7). **Da cancellare da ogni schermata del portale**: lì ripropone il teaser di marketing della
  home come `<h1>` a chi ha già fatto il login.
- **Accessibilità**: `<header>` di contenuto; titolo limitato a 22ch, lead a 60ch — il lead va
  riportato al tetto reale di `--measure-lead` (45ch, §6.6).
- **Usato in**: `templates/cases/index.html`, `templates/faq/index.html`,
  `templates/glossary/index.html`, `templates/partners/index.html` (e almeno altri 28).
- **Esempio reale — `templates/cases/index.html`**:

```django
{% include "components/page_header.html" with title=_("Mes dossiers") %}
```

#### `pagination.html`

- **Scopo**: paginazione «precedente / pagina n su N / successivo».
- **Blocco CSS**: `.pagination` (`__list`, `__link`, `__status`).
- **Contratto**: `page_obj` (Django `Page`); `query` (stringa urlencoded degli altri parametri). Non
  rende nulla se c'è una sola pagina.
- **Varianti**: nessuna.
- **Accessibilità**: `<nav aria-label="Pagination">`; link da 44 px con `rel="prev"`/`rel="next"`;
  stato testuale `aria-current="page"`; frecce `.icon--flip-rtl`; cifre tabulari (§6.8).
- **Usato in**: `templates/news/index.html`, `templates/community/room.html`.
- **Esempio reale — `templates/news/index.html`**:

```django
{% include "components/pagination.html" with page_obj=page_obj query=query %}
```

#### `pathway_list.html`

- **Scopo**: lista editoriale numerata (gli 8 percorsi regolari). **È l'oggetto esistente più vicino
  all'entrata** (§8.4) e la prova che il pattern funziona: diventerà il registro del sistema.
- **Blocco CSS**: `.pathway-list` (`__item`, `__num`, `__title`, `__desc`, `__arrow`), disegnato per intero dal foglio
  della home (`apps/pages/static/pages/css/pages.css` §6), il suo solo consumatore: le regole di `components.css` §18
  sono uscite dal foglio condiviso col passo di bilancio di W3-F1 (12 ottobre 2026); della §18 la home leggeva ancora
  il carattere dei titoli e il link esteso alla riga, che il suo foglio dice ora.
- **Contratto**: `items` = lista di dict `{title, text, url, lang}`; `lang` (per l'intera lista).
- **Varianti**: nessuna. Numeri `01`–`08` da contatore CSS (`decimal-leading-zero`), oggi in rubrica;
  freccia nascosta sotto 48rem — **da correggere**, perché la freccia è l'affordance e sotto 48rem è
  esattamente dove serve.
- **Accessibilità**: `<ol>` (l'ordine è semantico); numeri `aria-hidden`; stretched link con un solo
  tab stop; titoli `<h3>`.
- **Usato in**: `templates/pages/home/_pathways.html` (include). Dall'11 ottobre 2026 (v5.4, w3-f1, l'interno pubblico) l'Espace
  Personnes disegna gli otto percorsi come il registro dell'interno (`.registro`, nessun numerale: un
  catalogo, non una classifica, come sulla home).
- **Esempio reale — `templates/pages/home/_pathways.html`**:

```django
{% include "components/pathway_list.html" with items=d.pathway_items %}
```

#### `popover.html`

- **Scopo**: il pannello ancorato del sistema degli overlay (piano V5.4 §1.14; W2-A): un menu, il conto, il menu di
  una riga. Un `popover` nativo: il suo comando lo apre e lo chiude, un clic fuori o Esc lo chiudono, tutto senza
  script. `overlay.js` aggiunge il posto — sul bordo finale del comando, sotto se c'è posto, altrimenti sopra, a 4 px —,
  il fuoco sulla prima voce e di ritorno al comando, le frecce, e la chiusura quando il fuoco lo lascia (S-7) o una voce
  è scelta.
- **Blocco CSS**: `.overlay` con `.overlay--popover`; le righe `.overlay__list`, `.overlay__item`, `.overlay__sep`; in
  `static/css/v5/overlays.css`.
- **Contratto**: `id` (obbligatorio); `body` (HTML sicuro: un `ul.overlay__list` di link o bottoni `.overlay__item`,
  `li.overlay__sep` fra i gruppi) — oppure `body_template`; `label` (il nome accessibile del pannello, quello di un
  gruppo — e, sul telefono, la riga in testa allo sheet); `anchored` (True → resta ancorato sul telefono invece di
  diventare uno sheet). Il comando è del chiamante, un
  vero `<button popovertarget>`.
- **Varianti**: arriva con 4 px di caduta LONTANO dal comando e l'opacità in 200 ms, esce in 120 ms (MS-O6); il posto
  è il posizionamento ad ancora del browser, letto nel verso del pannello (`self-block-end span-self-inline-start`:
  in arabo il bordo sinistro del menu sul bordo sinistro del comando), con il ribaltamento e il contenimento di
  `position-try-fallbacks`; senza ancora le parti rare di `overlay.js` (`overlay/extras.js`, caricate solo lì) lo
  calcolano con gli stessi ribaltamenti e lo seguono allo scroll; ≤ 40rem uno sheet dal basso che resta un menu — né
  trappola né blocco dello scroll; Esc, il fuoco che esce e una scelta lo chiudono — sopra l'unico scrim, che prende
  tutta la pressione che lo chiude, dalla discesa al clic: la pagina dietro non la riceve mai (un campo non prende il
  fuoco, un link non si segue); in testa il suo nome (`label`: il titolo della pièce, «Mon compte») nel piccolo
  inchiostro secondario (`.overlay__caption`, nascosto alle tecnologie assistive: il nome del gruppo lo dice già).
- **Accessibilità**: righe di 36 px, 44 sotto un puntatore grossolano; la pressione di una riga è un colore a 0 ms,
  nessuna trasformazione; il fuoco entra sulla prima voce (la corrente se c'è) e torna al comando dopo Esc o una
  scelta; un clic fuori o il fuoco che esce non lo spostano; il comando porta `aria-expanded`; da tastiera nulla si
  anima.
- **Usato in**: `components/account_menu.html` (il conto nella barra superiore della console),
  `components/document_row.html` (il menu di ogni riga di «Mes documents»);
  `templates/dev/designpreview/specimens/overlays.html` (il conto e il menu di una riga, nei due versi).
- **Esempio (dal commento di contratto del componente)**:

```django
<button class="btn btn--icon btn--ghost" type="button" popovertarget="row-menu" aria-label="{% translate 'Ouvrir le menu de la pièce' %}">{% svg_icon "ellipsis-vertical" "icon" %}</button>
{% include "components/popover.html" with id="row-menu" body=row_menu %}
```

#### `section_header.html`

- **Scopo**: intestazione tipografica di sezione (senza box). Diventa lo **slot HEAD** dell'anatomia
  di sezione (§7.4), affiancato dal folio nel rail.
- **Blocco CSS**: `.section__header` (`.section__title`, `.section__lead`, `.eyebrow`) — in
  `layout.css`.
- **Contratto**: `title` (reso come `<h2>`); `eyebrow`, `lead` (opzionali); `lang`; `align`
  (`"center"`); `id` (ancora per la navigazione di pagina).
- **Varianti**: `.section__header--center`. Lo slot `eyebrow` è abolito (§8.2); `.section__lead` è
  già sul serif e su `--measure-lead`.
- **Accessibilità**: `id` sul contenitore per `aria-labelledby`/ancore;
  `scroll-padding-block-start: calc(var(--chrome-block-size) + var(--s-4))` evita che la cromatura
  sticky copra il titolo raggiunto via ancora.
- **Usato in**: `templates/pages/partials/_section_header.html` (la testa dei capitoli della home, markup
  diretto `.section__header`). Nessuna pagina lo include più («Diplômes et titres» l'ha lasciato col secondo
  passo di W3-F1): dall'11 ottobre 2026 (V5.4, W3-F1, l'interno pubblico) i capitoli dell'interno hanno la propria testa, `templates/pages/partials/
  _chapter_head.html` — il segno dei tre gradini, il titolo, l'attacco — la stessa della home.
- **Esempio (dal contratto)**:

```django
{% include "components/section_header.html" with id="demarche-header" title=_("Trois temps, une même démarche") %}
```

#### `sheet.html`

- **Scopo**: lo sheet dal basso del sistema degli overlay (piano V5.4 §1.14; W2-A): una scelta o un filtro sul
  telefono, la navigazione del telefono (W2-C2). Un `<dialog>` nativo che `overlay.js` apre modale (sopra l'unico
  scrim, la trappola in script, `aria-modal`).
- **Blocco CSS**: `.overlay` con `.overlay--sheet` e la maniglia `.overlay__grip`, nel parziale solo di pagina
  `static/css/v5/_overlay-panels.css`: la pagina che disegna uno sheet collega `css/dist/core/overlay-panels.css`
  (§2.1); il menu che diventa sheet sul telefono è di `static/css/v5/overlays.css`.
- **Contratto**: `id` (obbligatorio); `title`; `body` (HTML sicuro) — oppure `body_template`; `actions` (HTML sicuro
  del piede) — oppure `actions_template`; `history` (True → Indietro lo chiude); `return_id`.
- **Varianti**: dal basso sulla molla dello sheet (`--spring-sheet`, 550 ms, nessun rimbalzo), fuori in 200 ms sulla
  curva di layout; 48 px di margine sotto il bordo dello schermo, così un trascinamento verso l'alto non mostra mai un
  vuoto, e l'area sicura rispettata; solo gli angoli in alto, 12 px; sul desktop largo al massimo 40rem, centrato. Non
  si specchia.
- **Accessibilità**: Esc, lo scrim (mai con un campo già scritto), «Fermer» o un link lo chiudono; la maniglia
  (`overlay/extras.js`, caricata a riposo dove una pagina disegna uno sheet), trascinata in giù oltre un terzo o in
  fretta, lo chiude e lo scrim segue la mano — è decorativa (`aria-hidden`):
  «Fermer» è sempre lì (WCAG 2.5.7); il fuoco va alla voce corrente o al primo controllo e torna all'apritore.
- **Usato in**: `templates/dev/designpreview/specimens/overlays.html` (le lingue, ciascuna col proprio nome).
- **Esempio (dal commento di contratto del componente)**:

```django
<a href="#languages" data-overlay-open>{% translate "Langue" %}</a>
{% include "components/sheet.html" with id="languages" title=title body_template="partials/_languages.html" %}
```

#### `stepper.html`

- **Scopo**: il **passaggio pubblico «la linea»** (design V5, W3-D, §11.9; piano V5.4 §1.18 D16: il numerale è il
  marcatore del passaggio pubblico) — l'unico disegno di passaggio del sito: una sequenza vera su una linea in
  piano, i numerali sopra stazioni aperte (un contorno è aperto: nulla, su questo sito, chiude un passo per
  qualcuno), le parole sotto. W3-F1 l'ha disegnata per primo sulle porte («the site keeps one diagram language: the
  public passage, when W3-D draws it, is the same line»); questo componente e il suo parziale ne sono la casa.
- **Blocco CSS**: `.linea` (`__step`, `__num`, `__label`, `__text`, `__rank`; modificatori `--across`, `--pending`,
  `--done`, `--current`), in `static/css/v5/_journey-passage.css`, parziale di sola pagina (§2.3 del piano)
  importato dai fogli delle pagine che lo disegnano — la home (`apps/pages/static/pages/css/pages.css`) e,
  dalla fusione di W3-D (12 ottobre 2026), le porte, le pagine dei consigli e il questionario
  (`pathways/pathways.css`, `ecosystem/ecosystem.css`, `orientation/wizard.css`, subito dopo `_interior.css`,
  dove W3-F1 l'aveva disegnata per primo: un disegno solo). Le varianti di pagina — i due tempi di
  «Formation», le tappe dei diplomi, la prima lettera di un frammento, le otto stazioni del progetto pilota —
  qualificano il disegno nei parziali delle pagine (`_pathways.css`, `_spaces.css`, `orientation/wizard.css`),
  senza ridisegnarlo. In arabo le parole francesi di una stazione finiscono dal lato dell'anello.
- **Contratto**: `steps` = lista di str **oppure** di dict `{label | heading, text | body, pending, lang}`;
  `current` (opzionale: il posto, a base 1, di un flusso); `label` (il nome accessibile della lista); `lang`;
  `across` (True: in riga dal 48rem quando il passaggio ci sta); `cols` (le stazioni di una riga dal 48rem).
- **Varianti**: lungo il bordo di lettura (il telefono, e ovunque non sia in riga); in riga sulla sua colonna dal
  48rem (`across`), tante colonne quante stazioni per i passaggi brevi; il posto di un flusso (`current`: i passi
  dietro pieni d'inchiostro — le risposte della persona, mai una spunta —, il suo anello più spesso nel primario, le
  parole in peso, il rango «Étape n sur N» sotto); una stazione da verificare (`pending`: l'anello spezzato).
- **Accessibilità**: `<ol>` semantico; i numerali sono contatori CSS, decorativi (`aria-hidden`); con `current`
  `aria-current="step"` e il nome «Progression» se il chiamante non ne dà; senza `current` è una spiegazione,
  mai un avanzamento; lo stato non dipende dal colore (riempimento, spessore, peso); a colori forzati in
  `CanvasText` e `Highlight`.
- **Usato in**: `templates/pages/home/_orientation.html` (i quattro passi neutri dell'orientamento a gate chiuso),
  `templates/pages/partials/_linea.html` (il contratto di W3-F1, senza `current`: una spiegazione non è un
  avanzamento) e dunque `templates/ecosystem/companies.html`, `templates/ecosystem/partials/pilot_flow.html`,
  `templates/pathways/detail.html`, `templates/dev/showcase.html`. Lo stesso markup, scritto a mano con le
  varianti di pagina, in `templates/pathways/index.html`, `index_interim.html`, `diplomas.html`,
  `training.html` e `templates/orientation/start.html`.
- **Esempio reale — `templates/pages/home/_orientation.html`**:

```django
{% include "components/stepper.html" with steps=d.steps lang=d.steps_lang across=True %}
```
#### `tabs.html`

- **Scopo**: schede per contenuti paralleli brevi. Non usare per contenuti che l'utente deve
  confrontare.
- **Blocco CSS**: `.tabs__list`, `.tabs__tab`, `.tabs__panel`, `.tabs__panel-title` (radice `.tabs`), in
  `static/css/v5/tabs.css`; l'indicatore è uno solo, `.tabs__list::after`, mosso con `transform`.
- **Contratto**: `tabs` = lista di dict `{id, label, body (HTML sicuro)}`; `id` (id del widget,
  default `tabs`: obbligatorio se ce n'è più d'uno in pagina). La scelta non è ricordata da una visita all'altra.
- **Varianti**: nessuna.
- **Accessibilità**: pattern WAI-ARIA Tabs ad attivazione automatica: `role="tablist"`/`tab`/
  `tabpanel`, `aria-selected`, `aria-controls`, `aria-labelledby`, roving `tabindex`, pannelli
  `tabindex="0"`; frecce (invertite in RTL, mai con Alt / Ctrl / Meta), Home, Fine. `#id-pannello` nell'URL
  apre quella scheda. L'indicatore viaggia solo per una scelta del puntatore: da tastiera, al caricamento e a
  moto ridotto è al suo posto senza tragitto. **Senza JS** la tablist è nascosta e tutti i pannelli sono
  impilati con il proprio `<h3>`. L'opzione `remember` è stata tolta (G-21, chiusa).
- **Usato in**: nessun consumatore.
- **Esempio (dal contratto)**:

```django
{% include "components/tabs.html" with tabs=training_tabs id="formation" %}
```

#### `tooltip.html`

- **Scopo**: un controllo di sola icona e il gemello visibile del suo nome (piano V5.4 §1.14, R-21; W2-A): il tooltip è
  l'`::after` del controllo stesso, che legge il suo `aria-label` — nessun markup in più, nessuno script per apparire.
- **Blocco CSS**: `.tooltip` (l'unico tooltip del livello superiore, che `overlay.js` posa per un controllo dentro un
  contenitore che taglia: le parole della rail, «⋮» di una riga), in `static/css/v5/overlays.css`; l'`::after` di un
  controllo `[data-tip]` senza `layer` e il gruppo `[data-tip-group]` sono del parziale solo di pagina
  `static/css/v5/_overlay-panels.css` — nessuna pagina del prodotto li disegna oggi —: la pagina che li usa collega
  `css/dist/core/overlay-panels.css` (§2.1). Mai su un bottone d'invio: il suo `::after` è la chiave del loader.
- **Contratto**: `label` (obbligatorio: il nome accessibile e le parole del tooltip, una stringa viva); `icon`;
  `href` (un link) oppure un bottone di `type` ("button" per default); `css_class` ("btn btn--icon btn--ghost" per
  default); `side` = "block-end" | "inline-end" | "inline-start" (sopra per default); `layer` (True → il tooltip del
  livello superiore, dentro un contenitore che taglia); `popovertarget` (il menu che il bottone apre).
- **Varianti**: sotto il puntatore aspetta `--tooltip-delay` (400 ms) e appare in `--motion-fast`; dentro un gruppo
  (`data-tip-group` sulla barra) un vicino appare subito, 0 + 0 ms, e il gruppo si raffredda 400 ms dopo — in CSS, con
  `--tip-warm`; dentro una lista che scorre, una tabella, il corpo di un drawer, `layer` mostra l'unico tooltip
  condiviso nel livello superiore (`popover="manual"`), oltre il bordo che taglierebbe l'`::after`.
- **Accessibilità**: WCAG 1.4.13 — raggiungibile (il bordo trasparente di 6 px fa da ponte verso il controllo),
  persistente, congedabile: Esc lo toglie ovunque sia il fuoco, una pressione sul controllo lo toglie finché il puntatore
  non esce; col fuoco della tastiera è subito lì; se ne va a 0 ms; nessun tooltip su un controllo il cui menu è aperto,
  né sul telefono (≤ 40rem) né dove nulla passa sopra; sotto il moto ridotto l'attesa resta (è una soglia), la
  dissolvenza no; sotto colori forzati un contorno `CanvasText`. Il tooltip del livello superiore prende le sue
  parole da `data-tip-label` dove il nome del controllo è il suo stesso contenuto, si posa oltre il bordo
  dell'antenato che `data-tip-beyond` nomina, e una pagina può rifiutarlo (`overlay:tip`, annullabile).
- **Usato in**: la parola di un glifo che sta da solo nella rail della console (O11: `console.js` marca i
  controlli `data-rail-tip`, §11.6), «⋮» delle righe di «Mes documents»;
  `templates/dev/designpreview/specimens/overlays.html` (un gruppo di quattro comandi, il comando di un menu di riga,
  tre tooltip del livello superiore in una lista che scorre).
- **Esempio (dal commento di contratto del componente)**:

```django
{% translate "Télécharger" as label %}
<div class="cluster" data-tip-group>{% include "components/tooltip.html" with label=label icon="download" href=download_url %}</div>
```

#### `wizard_stepper.html`

- **Scopo**: lo **Stepper** di un modulo guidato («Ma situation»), disegnato dall'unico disegno di binario della
  console (design V5, W3-D, §11.9): le domande come nodi sulla linea del binario — un punto d'inchiostro pieno
  quando la domanda ha una risposta (la stessa regola di `PersonProfile.answered()`: «je ne sais pas encore» non è
  una risposta, 0 lo è; mai una spunta, O14), l'anello laguna sul suo velo sulla domanda mostrata, un anello aperto
  altrove. La linea resta un filetto: alle domande si risponde in qualunque ordine, nulla è «percorso». Ogni voce
  è un link alla sua domanda: funziona senza JavaScript (ancora in pagina) e con (`situation.js` mostra quella
  domanda e sposta il segno corrente).
- **Blocco CSS**: `.wstep` (`__item`, `__link`, `__node`, `__label`; modificatori `--done`, `--current`), in
  `apps/portal/static/portal/v5/_journey-stepper.css`, sul vocabolario di `v5/_journey-nodes.css` (i parziali del foglio
  di sola pagina di «Ma situation», `portal/situation.css`, dopo il modulo guidato, §2.1); la linea non prende il
  puntatore (`pointer-events: none`): un tocco sul tratto che attraversa una voce
  sceglie la sua domanda.
- **Contratto**: `fields` (i campi visibili del modulo, nell'ordine delle domande); `answered` (l'insieme dei
  nomi di campo con una risposta, dal profilo, non ricalcolato qui); `label` (opzionale).
- **Varianti**: una spina all'inizio della riga; sotto 64rem una linea in piano di nodi, il titolo della domanda
  stessa che nomina il passo (otto voci con l'etichetta metterebbero la prima domanda sotto la piega).
- **Accessibilità**: `<ol role="list">` con `aria-label`, `aria-current="step"` sulla domanda corrente
  (spostato dallo script), voci di 44 px (sotto 64rem colonne uguali, mai sotto 24 px); nessuna barra nativa,
  nessuna percentuale.
- **Usato in**: `templates/portal/situation.html`.
- **Esempio reale — `templates/portal/situation.html`**:

```django
{% include "components/wizard_stepper.html" with fields=form.visible_fields answered=answered_fields %}
```
### 10.1 Pattern CSS senza file template

| Pattern | Classi | Note |
|---|---|---|
| Bottoni | `.btn` + `--primary`, `--secondary`, `--soft`, `--ghost`, `--link` (`--text`), `--danger`, `--icon`, `--inverse`, `--sm`, `--lg`, `--block`, `--upper`, `--arrow` | `static/css/v5/buttons.css` (§2). Un primario per vista, piatto; 44 px (36 `--sm` solo col puntatore fine, 52 `--lg`); stati: riposo, hover, `:focus-visible` (l'anello del sistema), pressione (un solo gesto: riempimento di pressione e 1 px in giù), `:disabled` / `[aria-disabled="true"]` / `.is-disabled` → per colore e cursore, mai per opacità, e il puntatore lo raggiunge ancora; la faccia busy è del loader |
| Pastiglia di stato | `{% chip membro "app.Enum" %}parola{% endchip %}` → `.chip` | `static/css/v5/chip.css` (§2); `chip.html` qui sopra. Mai scritta a mano: la coppia dà registro e marca; 24 px (20 `size="s"`, 28 `size="l"`) |
| Etichetta | `.tag` (`a` o `span`) | un **termine**, non uno stato: una voce del glossario sotto un percorso, il livello chiesto a una competenza, il tipo di un messaggio. Carta e filetto, nessun registro, nessuna marca; come link risponde al puntatore, tiene l'anello del sistema e ha 44 px di bersaglio sotto un puntatore grossolano |
| Scheda d'azione | `.card.card--action` (`.card__eyebrow`, `__title`, `__text`, `.card__action`) | la sola cosa da fare su uno schermo: che cosa, perché, e **una** azione in `.card__action`. È il piano rialzato (livello 2): uno per schermo. `static/css/v5/card.css` |
| Striscia di sintesi | `dl.summary` > `.summary__item` (`dt` + `dd`) | pochi fatti su ciò che lo schermo elenca, in celle su un solo foglio separate da filetti; valori a misura di testo — **mai** una riga di card-cifra né un numero grande. `static/css/v5/card.css` |
| Link con freccia | `.link-arrow` | CTA secondaria nelle liste; freccia `.icon--flip-rtl`, traslazione di 3 px su hover col puntatore fine (invertita in RTL, ferma a moto ridotto) |
| Icone | `.icon`, `--sm`, `--lg`, `--xl`, `--accent`, `--flip-rtl` | §13 |
| Messaggi Django | `.messages` > `.alert.alert--{tag}` | resi da `base.html` in una regione `role="status" aria-live="polite"`; `error` → `role="alert"` |
| Form | `.form`, `.form__group` / `.form__fieldset`, `.form__legend`, `.form__intro`, `.form__required-note`, `.form__actions`, `.form-row.form-row--2`, `.input`, `.search-form` | `static/css/v5/field.css` (§2): gruppi senza riquadro a due campi e mezzo di distanza, legenda 20/28, azioni dopo un filetto; il form completo è descritto in `docs/ACCESSIBILITY.md` §6 |
| Sommario di pagina | `.sommaire` (`__title`, `__list`, `__link`) | dall'11 ottobre 2026 (V5.4, W3-F1) nel posto finale dell'ingresso di una pagina lunga dell'interno (la scheda di un percorso, il Forum: `templates/pages/partials/_ingresso.html`, `static/css/v5/_interior.css` §2), «Sommaire de la page» come titolo visibile; **mai sticky** (la barra `.section-nav` sotto la cromatura, che copriva la colonna laterale, è uscita col suo ultimo consumatore); un link per riga, sul suo filetto, a ogni larghezza (sotto 64rem una riga di link che vanno a capo leggeva due voci come una frase, «QU'EST-CE QUE LE FORUM  OBJECTIFS») |
| Pagine d'errore | `.error-page` (`__door`, `__body`, `__head`, `__code`, `__title`, `__text`, `__ref`, `__actions`, `__links`), `.aiuto` | design V5 (W3-F2, passo 2 e la correzione della revisione), `static/css/v5/_servizio.css` e la porta di `static/css/v5/_door.css`, caricati da `cms/errori.css`: una pagina quieta — **la porta a riposo** (`templates/errors/_door.html`: la chiave fuori dalla serratura, ferma, mai specchiata, decorativa `aria-hidden`; compatta sopra l'etichetta su un telefono, nel posto finale della testa da 64rem), lo stato come etichetta della testa («Erreur 404», decorativa `aria-hidden`), un `h1`, una frase, un solo primario e la via del ritorno (`data-history-back`, solo con script; sul 403 per chi non è entrato il primario è l'accesso, con `next` all'indirizzo rifiutato), `nav aria-label="Navigation de secours"` come capitolo quieto («Privacy Policy» `lang="en"`), «chi può aiutarmi». 403, 404, 410 e 429 nella shell pubblica (`templates/errors/base_error.html`); 400 e 500 in una cornice autosufficiente (`templates/errors/standalone.html`: nessun database, nessun context processor, `core.views`) |
| Pagine del conto | `.conto` (`__main`, `__head`, `--solo`), `.conto-nav` (`__list`, `__link`), `.conto-facts`, `.conto-links`, `.conto-actions`, `.conto-danger`; gli elementi di allauth (`.account-page__title`, `.account-page__text`, `.account-panel`) | design V5 (W3-F2, passo 2), `static/css/v5/_servizio.css`: una sola cornice (`templates/allauth/layouts/base.html` → `manage.html`) per il profilo, le pagine di gestione di allauth e la richiesta di cancellazione — la traccia, le sezioni del conto al bordo di lettura da 64rem e in banda sotto, la pagina nelle otto colonne del corpo; l'ingresso resta «Il varco» (`.account-page--entrance`, W2-B); `.account-table` resta in `components.css` per la console |
| Pagina legale | `.legal-page`, `.legal-page__meta`, `.legal-page__courtesy` | misura di lettura da `.container--prose` (alias legacy di 42rem) |
| Contatore | `.counter` + `data-counter` | **sulla lista di demolizione**: «contatori da startup» è un anti-pattern dichiarato e il componente ha zero usi |
| Segnaposto di sviluppo | `.dev-placeholder` | mai nel markup di produzione |

### 10.2 Shell (`templates/base.html` + `templates/partials/`)

| File | Contenuto |
|---|---|
| `templates/base.html` | `<html lang dir class="no-js">`; preload font per direzione (G-24); il bundle `css/dist/main.css` (§2); `head.js` sincrono; skip link; `utility_bar` → `header` → blocco `banner` → `<main id="main-content" tabindex="-1">` (blocco `breadcrumbs`, regione messaggi, `main_content` ⊃ `content`) → `footer`; `main.js` come modulo |
| `templates/partials/utility_bar.html` | fascia navy `role="region" aria-label="Barre institutionnelle"`: promotore, link «Espace réservé» oppure menu account, selettore lingua |
| `templates/partials/header.html` | la testata sticky «Il portico»: il lock-up, la barra (`<nav aria-label="Navigation principale" data-portico>`), la zona finale con «la targa» (il popover del conto, autenticati) e «Menu» (un link `href="#nav-sheet"`, `data-overlay-open`, `data-nav-toggle`), lo scrim del portico; **dopo** l'header, al livello del `body`, il foglio sotto 80rem (`main_nav.html` con `nav_variant="sheet"`, §11.2) |
| `templates/partials/main_nav.html` | voci da `cms.MenuItem` (fallback statico in `apps/cms/templatetags/cms_nav.py`), filtrate da gate/flag e da route risolvibili; due disegni di un albero: la barra (una porta di disclosure + il suo pannello per voce con figli, §11.1) e il foglio (il drawer modale del sistema di overlay, le porte che si aprono sul posto, §11.2) |
| `templates/partials/footer.html` | fascia navy `.on-inverse`: identità, `nav` «Informations légales» con **cinque link distinti**, `nav` «Navigation du site», blocco progetto con link anti-frode solo se `gates.phase3_public`; riga finale con © e versione |
| `templates/partials/seo_head.html` | canonical, `hreflang` per le 4 lingue + `x-default`, Open Graph, Twitter card, `theme-color` |

---

---

## 11. Pattern di navigazione

Il modello tastiera completo, con i criteri WCAG, è in `docs/ACCESSIBILITY.md` §3. Qui il disegno.

La struttura che la direzione A prescrive è a tre piani più uno: **barra istituzionale** 36 px navy
non sticky (promotore mai troncato, quattro lingue in linea, area riservata con la parola e il
lucchetto), **testata** 72 px su carta con un filetto `--rule-ink` da 1 px sotto — opaca, senza blur,
senza ombra, senza rimpicciolimento allo scroll — e **navigazione primaria** su due righe, dove la
prima riga sono i quattro pubblici ed è **permanente in ogni stato di gate e in ogni lingua**. Il
gate si attacca alla **destinazione**, non alla riga. Il quarto piano è il **titolo corrente sticky**
(§11.5): la testata e la riga di navigazione scorrono via e restano 48 px che portano marchio, titolo
di pagina, **ordinale e titolo corrente della sezione in vista** e ricerca. È la cromatura di firma
della direzione, ed è ciò che fa sapere al lettore la propria posizione dentro il registro.

Quanto segue descrive ciò che `static/css/v5/chrome.css` e `static/js/src/nav.js` rendono **oggi**: la cromatura
pubblica del design V5, «Il portico» — la «Fase 3 — menu aperto» del committente, sviluppata (piano V5.4 §1.11,
§1.12; W2-C1). Il markup è in `templates/partials/utility_bar.html`, `header.html` e `main_nav.html`; i pannelli
ricevono il loro contenuto da `apps/cms/templatetags/cms_nav.py` (`_portico()`), **solo da contenuto vivo**: la
glossa bloccata della porta, i figli CMS o i due link di compito della scheda della porta, una seconda riga dove
esiste una frase viva breve — intera, mai scritta qui.

### 11.1 «Il portico» (≥ 64rem; con la fotografia da 80rem) — pattern «disclosure navigation»

Non è un `role="menubar"`: è una lista di bottoni di disclosure, il modello raccomandato per la navigazione di un
sito (le frecce fanno solo ciò che il modello di §3 di `docs/ACCESSIBILITY.md` dice, Tab resta prevedibile).

- **Anatomia**: la barra istituzionale (32 px, notte, non sticky: il promotore, le quattro lingue nominate); la
  testata su carta, sticky, 64 px → 56 px quando la pagina si è mossa (vetro solo allora, col puntatore fine, da
  80rem, senza pannello aperto); le **quattro porte** come bottoni, un filetto, Forum, Projet (D-U3); «la targa»
  nella zona finale (§11.3). Da 64 a 80rem la testata porta le sole porte, i pannelli si aprono senza fotografia e
  «Menu» porta Forum · Projet · lingue · la ricerca (il foglio, §11.2). **La testata tiene la sua colonna, misurata**: da 64 a
  90rem è compatta — lock-up 32/17, gap 16, porte senza chevron. Da 80 a 90rem perché la colonna `lg` è 1096 px e le
  sei voci francesi col lock-up intero ne chiederebbero 1178; da 64 a 80rem perché a 1024 la colonna è 944 px (927
  accanto a una barra di scorrimento classica di 17 px) e col lock-up intero la riga francese ne chiedeva 945 sotto un
  dito, dove la targa e «Menu» sono a 44 px — su un iPad in orizzontale la testata andava su due righe (W2-C2,
  REVIEW M1). Compatta, la riga lascia almeno 24 px in fr · en · it · ar, con e senza utente autenticato, col
  puntatore fine e grosso e accanto alla barra (N11; francese 42,8 px sotto un dito, 37,8 accanto alla barra;
  `tests/frontend/test_browser_w2_c2.py::test_the_band_holds_one_row_with_24_px_to_spare_at_1024`). La zona finale è
  la sola chiave fino a 100rem; il bordo di
  chiusura della zona finale coincide col bordo della colonna in fr · it · en · ar da 1280 a 1920, con e senza
  utente autenticato (`tests/frontend/test_browser_w2_c1.py::test_the_letterhead_holds_its_column_at_every_desktop_width`).
  Se una riga non tiene le sue voci — text spacing (1.4.12), un'etichetta lunga del back-office — la lista va a capo
  e la testata cresce di una riga; non taglia mai (`test_the_bar_wraps_under_text_spacing_and_never_clips`).
- **Markup** (`templates/partials/main_nav.html`): per ogni sezione `li.main-nav__item--section` contiene
  `button.main-nav__door[data-portico-door]` con `aria-expanded` e `aria-controls="<id>-portico"` e, subito dopo,
  il pannello `div.portico[data-portico-panel]`: Tab percorre barra → pannello aperto → porta successiva senza
  script. Forum, senza figli, è un link semplice.
- **Il pannello** è la scheda della porta, aperta: appeso alla larghezza del contenuto (`.site-header__inner`), mai al
  viewport (N1); su 8 | 4 — la glossa bloccata sotto la campata del lock-up e, subito sotto di lei, «Voir l'espace»
  (la lede è un blocco solo, come nel comp; il vuoto sotto è l'aria della griglia), le voci su righe a filetto a
  partire dall'inizio in linea della prima porta (`--portico-lead`, misurata da `nav.js`: N2), il piede anti-frode
  dove il menu porta quella pagina — e, nelle ultime quattro colonne, la fotografia della porta **a
  colori, nella gradazione V5** (4 : 5, 640 / 960, `lazy` + `fetchpriority=low`, prefetch a idle dopo `load` da
  80rem, mai sui telefoni, mai con Save-Data; `static/img/portico/`, `PROVENANCE.json`), col glifo del pubblico
  **una volta** su un disco notte di 36 px e il filetto del pubblico di 3 px al piede. **Una sola altezza per le
  quattro porte** (`--portico-h`, misurata da `nav.js` quando cambiano la larghezza, la barra o i font — mai allo
  scatto 64 ↔ 56, dove costava un long task a ogni rotella); nei pannelli il cui contenuto finisce ben sopra
  l'altezza condivisa (`.portico--short`, segnato alla misura) l'ultima riga si chiude con un filetto, così una
  lista breve finisce invece di sfumare. Una glossa francese prescritta su una pagina araba porta `lang` e `dir`
  sul paragrafo: il blocco è a bandiera a destra nella sua colonna finché la copia non è firmata (B1). «Projet» è
  un pannello piano, appeso al bordo di chiusura della barra, senza fotografia. Carta, ombra L3, angoli inferiori
  12 px, il filetto della testata che corre dentro il bordo superiore; sotto, lo scrim.
- **Voci**: titolo 17/24 peso 500 su righe di 48 px; la seconda riga (`MenuItem.description_<lang>` o la frase viva
  della destinazione) intera, mai troncata, solo nella lingua della pagina; nessun glifo per voce (DE-2).
- **«L'architrave»**, l'unico indicatore: 2 px sul giunto fra barra e pannello, `translateX() scaleX()` sulla molla
  `--spring-snappy`, posizionata in pixel fisici da `nav.js` (una sola via di codice per le due direzioni); segue la
  voce più vicina al puntatore e il focus, torna su `aria-current`; non viaggia al primo posizionamento, da tastiera
  né a movimento ridotto. Senza script ogni voce disegna la propria linea.
- **Puntatore**: apertura dopo 120 ms di intenzione, cambio dopo 80 ms, chiusura dopo una grazia di 250 ms — col
  puntatore fine soltanto; un click **fissa** un pannello aperto dall'hover; il **triangolo sicuro** per le porte
  2–4: finché il puntatore si muove verso il pannello aperto, attraversare una porta vicina non cambia pannello
  (`tests/frontend/test_browser_w2_c1.py::test_the_safe_triangle_holds_for_doors_two_to_four`, con la distanza in
  px). Lo scrim solo per click, tocco e tastiera, mai sulla barra istituzionale.
- **Tastiera** (`docs/ACCESSIBILITY.md` §3): ← → fra le voci nel senso della lettura (invertite in arabo); a
  pannello aperto la porta successiva si apre al loro posto; ↓ apre ed entra; ↑ dalla prima voce torna alla porta;
  Home / Fine; Invio alterna e lascia il focus sulla porta; Esc chiude e restituisce il focus; il focus che lascia la
  navigazione chiude (1.4.13). Da tastiera la pagina salta alla fermata, senza scorrimento morbido (`html:has(:focus-visible)
  { scroll-behavior: auto }`, piano §1.12 item 5); le fermate della testata stessa — il lock-up, le sei voci, la zona finale —
  portano `scroll-margin-block-start: -80px`, il negativo dello scroll padding della pagina, così un focus dentro la barra
  appiccicosa (una porta, Shift+Tab dalla pagina) non riporta più la pagina in cima; le voci dei pannelli tengono il padding
  (2.4.11: `test_focus_is_not_obscured_by_the_sticky_letterhead`).
- **Motion** (§12): il pannello è una transizione, mai un keyframe — in, opacità + 8 px dalla barra, 200 ms
  `--ease-enter`; out 120 ms; istantaneo da tastiera e al cambio di porta; il contenuto cambia in 120 ms di
  opacità; alla prima apertura col puntatore le voci salgono di 4 px a 30 ms di distanza; le fotografie si
  incrociano in 200 ms (`contain: paint`). A movimento ridotto un'unica opacità di 80 ms (`--motion-reduced`).
- **Senza script**: un pannello si apre su `:hover` e `:focus-within` (G-12: non chiudibile con Esc).
- **Voce corrente**: `aria-current="true"` sulla porta della sezione antenata (inchiostro pieno, l'architrave a
  riposo sotto di lei), `aria-current="page"` sulla voce del pannello (filetto di 2 px al bordo di lettura).
- Verificato da `tests/frontend/test_browser.py::test_mega_menu_is_keyboard_operable`,
  `tests/frontend/test_browser_w2_c1.py` (modello tastiera, intenzione, fissaggio, triangolo sicuro, fotografie,
  senza script, 2.4.11) e `tests/i18n/test_rtl_browser_nav.py` (N19: l'architrave, le voci e le frecce in arabo);
  screenshot `docs/qa/design/state-megamenu-open-fr-1440.png`, `docs/qa/design/state-megamenu-open-ar-1440.png`.

### 11.2 Drawer (< 80rem: telefono, tablet, laptop fino a 1279 px) — il foglio del sistema di overlay

Il menu sotto 80rem è **il foglio** (piano V5.4 §1.12 item 8; W2-C2): il drawer modale del sistema di overlay
(`static/js/src/overlay.js`; il contratto `docs/design-v5/QA/v54/w2-a/CONTRACT.md`), disegnato da `main_nav.html` con
`nav_variant="sheet"` e incluso da `header.html` **dopo** la testata, al livello del `body`: un pannello intrappolato
non sta mai nel contesto di impilamento dell'header sticky.

- **Apertura e chiusura**: «Menu» è un link `href="#nav-sheet"` con `data-overlay-open` (e `data-nav-toggle`, il gancio
  stabile dei test), che `overlay.js` fa bottone (`role`, `aria-controls`, `aria-expanded`, `aria-haspopup="dialog"`):
  `show()`, `aria-modal="true"`, la trappola (Tab e Shift+Tab girano dentro), la pagina dietro `aria-hidden` e senza
  pressione (l'unico scrim), lo scroll bloccato senza scatto (`html[data-overlay-lock]`). Esc, lo scrim, «Fermer» o
  un link del foglio lo chiudono e il fuoco torna su «Menu»; una finestra allargata oltre 80rem lo chiude (`nav.js`,
  `initSheet`) e porta il fuoco sul lock-up della testata.
- **Anatomia**: il foglio possiede la sua riga di testa — il lock-up e «Fermer» (`data-overlay-focus`: prende il
  primo fuoco) sulla riga e sulla misura della testata, così la barra diventa la testa del foglio senza salti (a 390
  × 844 i due lock-up coincidono al pixel). Sotto 48rem «Menu» e «Fermer» hanno una sola larghezza per lingua, quella
  della parola più lunga: ciascun bottone porta le due parole nella stessa cella, l'altra nascosta
  (`.nav-toggle__alt`, `aria-hidden`), così nell'apertura cambiano solo la parola e il glifo (88,6 px in francese, 6 px
  dentro: la riga del telefono tiene da 369 px in ogni lingua). Poi l'ordine della Fase 3: **le lingue** (i quattro nomi della barra
  istituzionale, su carta) → **le quattro porte**, righe di 64 px (`--drawer-row-h`) col glifo del pubblico su un
  disco notte di 36 px — il disco del pannello (§11.1) —, che si aprono sul posto (`<details name="nav-sheet-doors">`,
  esclusive; l'accordion di `main.js` dove `name` non è supportato; nessuna animazione d'altezza): la glossa bloccata
  con la voce del lede — 15/24 in inchiostro, un passo sopra le seconde righe da 13 px: la scheda della porta,
  aperta —, le voci a filetto con la loro seconda riga viva, «Voir l'espace»; la porta della sezione corrente è aperta e
  marcata (`aria-current`) → un filetto di struttura → **Forum · Projet**, righe di 52 px (Projet si apre come le
  porte) → **la ricerca**, quella delle domande frequenti — l'unica ricerca pubblica, solo quando la pagina è
  pubblica —, nominata dalla sua etichetta visibile → **la primaria** «Découvrir le questionnaire d'orientation» →
  **la riga anti-frode** → **il piede fissato, su notte**: «la targa» a 44 px a tutta larghezza (§11.3) o,
  autenticati, il comando del popover del conto; il promotore. Il piede non è un contesto notturno (`on-inverse`): i
  suoi comandi prendono l'anello della notte, e il menu del conto che vi si apre — un pannello di carta nel livello
  superiore, che eredita dagli antenati del comando — tiene quello della carta (#1d8a93, 4,11 : 1; con l'anello
  della notte le sue righe ne disegnavano uno a 1,75 : 1 sul bianco: W2-C2, A11Y_PERF M2).
- **Fasce**: sotto 48rem il foglio prende lo schermo, «Quiet»: un'opacità mentre le righe salgono di 12 px e la testa
  resta sulla riga della barra (in 320 ms su `--ease-enter`, fuori in 200 ms su `--ease-layout`: gli orologi del
  drawer). Da 48rem è il foglio laterale, largo `--drawer-w`, che entra dal bordo di chiusura e ne esce («Slide»: un
  drawer si specchia, quindi da sinistra in arabo; la salita del telefono è verticale e non si specchia), su un
  margine suo di 24 px (`--grid-margin` ripuntato nel foglio: una colonna di 371 px a 768, la primaria su una riga);
  la sua testa lascia il lock-up alla testata accanto, il piede resta — la targa della testata sta sotto il foglio, e
  senza il piede il menu aperto non offriva l'ingresso all'area riservata (W2-C2, REVIEW M2). Da 64rem le porte sono
  nella barra: il foglio porta Forum · Projet · le lingue · la ricerca, e il piede. Sotto 30rem di altezza — un
  telefono di lato, una finestra al 400 % (1.4.10) — il piede non è fissato: il foglio scorre per intero sotto la sua
  testa appiccicosa, il piede alla fine della lista, come il cassetto della console (a 320 × 256 la lista prende il
  78 % della vista, prima il 31 %; un fermo del fuoco non sta mai sotto la testa). Movimento ridotto: l'unica opacità
  di 80 ms del sistema, nessuna salita.
- **Bersagli**: nessuno sotto 44 px col puntatore grosso; l'anello di «Italiano» è intero dentro il corpo del foglio
  (R3A-2). Il ciclo della trappola: 17 fermi sul telefono, 16 a 768, 10 a 1024 — la targa del piede (o il comando del
  conto) fra loro.
- **Senza script**: «Menu» è un link al foglio, che si mostra sul posto (`:target`); «Fermer» è un link indietro; le
  porte si aprono nativamente; la testata resta sticky, alta quanto la sua sola riga.
- **Misure** (W2-C2, 11 ottobre 2026; `docs/design-v5/QA/v54/w2-c2/NOTES.md`): l'apertura a freddo sulla home a CPU × 4,
  390 px al tocco, n = 9, p90 168 ms in francese e in arabo (N9 ≤ 200 ms); il foglio alto 844 px su 844 px disponibili
  a 390 × 844 e 768 px su 768 px a 1024 × 768, lo scrim a tutto schermo, la testa del foglio sopra di lui —
  `docs/qa/design/state-drawer-open-fr-390.png`, `docs/qa/design/state-drawer-open-ar-390.png`,
  `docs/qa/design/state-drawer-open-fr-1024.png`, `docs/qa/design/state-drawer-open-ar-1024.png`;
  `tests/frontend/test_browser_w2_c2.py::test_the_sheet_opens_and_closes_on_the_overlay_system`,
  `tests/i18n/test_rtl_browser_w2_c2.py::test_in_arabic_the_side_sheet_comes_and_goes_by_the_left`.
- **G-02 (chiusa il 20/09/2026)**: il velo della testata sta sullo pseudo-elemento `.site-header::before`, mai
  sull'header, che altrimenti diventava containing block dei discendenti `position: fixed`; il foglio, poi, sta fuori
  dall'header (`tests/frontend/test_design_docs.py::test_sticky_header_does_not_trap_fixed_drawer`).
- **G-23 (chiusa l'08/10/2026)**: il velo non copre più i comandi della testata a menu aperto — prima partendo dal suo
  piede reale, dal foglio in poi perché la testa del foglio sta sopra di lui, «Fermer» dov'era «Menu».
- **G-04 (chiusa l'08/10/2026)**: senza JavaScript la testata non contiene più il menu, che si mostra sul posto
  (`docs/qa/design/a11y-nojs-fr-390.png`, `docs/qa/design/a11y-nojs-fr-1024.png`;
  `tests/frontend/test_browser_w2_c1.py::test_without_script_a_door_opens_on_hover_and_the_sheet_opens_in_place`).
- **G-11 (chiusa l'11/10/2026)**: a foglio aperto il resto della pagina esce dall'albero dell'accessibilità e non
  prende il fuoco: il cursore virtuale non può più uscire dal menu.

### 11.3 Il controllo lingua e «la targa»

Il controllo lingua è un solo componente (`language_segmented.html`, §10): nella barra istituzionale i quattro nomi
per esteso — Italiano · Français · English · العربية, mai «ع» (DL A25) — come link `translate_url` della pagina
corrente con `lang`, `hreflang` e `dir`, la lingua corrente segnata dalla linea e dal peso, mai dal solo colore;
nel foglio sotto 80rem gli stessi quattro nomi, su carta, per primi (§11.2). Nessuna
disclosure, nessun `<select>` nella cromatura pubblica; al piede della rail della console — nella rail e nel suo
cassetto — la lingua corrente è il controllo e i quattro nomi si aprono sopra di esso (§11.6).

**«La targa»** (piano V5.4 §1.11) è l'ingresso all'area riservata, nella zona finale della testata, in entrambi gli
stati della barra: una targhetta piatta — filetto d'inchiostro, raggio 6, la chiave d'oro `ile-key` come ornamento,
le parole in inchiostro; mai dorata, mai metallo. L'hover tinge la targa, la chiave non si muove (O1). Da 100rem la
parola «Espace réservé» — la soglia misurata (piano §1.11: «dove entra»): fra 90 e 100rem la colonna è 1240 px e le
sei voci francesi col lock-up intero lasciano 59 px, meno dei 140 della targa con la parola; sotto, la sola chiave
(32 × 32, 44 col puntatore grosso) col nome nel nome accessibile e nel tooltip del livello superiore del sistema di
overlay (`data-tip="layer"`, `data-tip-side="block-end"`: dopo l'attesa al passaggio del puntatore, subito al fuoco da
tastiera, via con Esc o una pressione — 1.4.13; da 100rem, dove la targa dice la sua parola, `nav.js` lo rifiuta con
l'`overlay:tip` annullabile del sistema; W2-C2). Resa solo dietro `reserved_area_public_link`
+ `reserved_area_enabled`: spenti i flag, nessun buco — la zona finale, senza nulla da ospitare, è marcata
`site-header__end--bare` e da 80rem, dove nemmeno «Menu» è disegnato, non è disegnata: la barra finisce sul bordo
della colonna, senza lo spazio vuoto della spaziatura della riga (misurato a 1280 / 1440 / 1920 in fr e ar,
`tests/frontend/test_browser_w2_c2.py::test_the_flag_off_leaves_no_hole_in_the_letterhead`; W2-C2). Con l'utente
autenticato la stessa sede apre **il popover del
conto** del sistema di overlay (`account_menu.html` con `popover`, W2-C2): appeso al bordo di chiusura del comando
(in arabo il suo bordo sinistro su quello del comando), il fuoco sulla prima riga, ↓ ↑ Home Fine, Esc e il fuoco di
ritorno al comando, chiuso quando il fuoco esce. Il comando ha la stessa compattezza: sotto 100rem il solo glifo della
persona sulla targhetta da 32 px (44 col puntatore grosso; il nome resta nel nome accessibile, nessun chevron), da
100rem il nome accanto al glifo, al più 6rem; il glifo è in inchiostro come le parole — l'oro è della chiave. Sotto
80rem la targa — e, autenticati, il comando del popover — è anche nel piede del foglio, su notte (da 48rem la targa
della testata sta sotto il foglio laterale): il filetto `--line-night`, le parole in carta, la chiave d'oro, a tutta
larghezza su 44 px. Sotto 40rem il popover vi si apre come uno sheet dal basso sopra l'unico scrim, che prende tutto
il tocco che lo chiude — lo scrim resta al suo posto sopra il foglio finché la pressione dura, così gli eventi di
compatibilità del tocco non raggiungono le righe sotto (W2-C2, A11Y_PERF M1); da 40rem è ancorato al comando. Il
comando della sede e del piede sta sul centro della riga anche in arabo: il suo involucro è una scatola flex, non un
blocco che prende lo strut di 32 px di Vazirmatn.

### 11.4 Breadcrumb, navigazione locale, sommario di pagina, paginazione

| Pattern | Dove | Regola |
|---|---|---|
| Breadcrumb | blocco `breadcrumbs` di `base.html`, prima del contenuto | derivato dallo stesso albero di menu della navigazione; «Accueil» automatico; ultimo elemento = pagina corrente, non linkata; solo a profondità ≥ 2 |
| Navigazione locale | `.layout-sidebar__aside`, poi il rail | colonna sticky ≥ 64rem; sotto, un filetto segmentato scorrevole da 44 px e non una nuvola di pastiglie; `aria-current="page"` |
| Sommario di pagina | `.sommaire` nell'ingresso | ancore alle sezioni di una pagina lunga, nel posto finale dell'ingresso; mai sticky (W3-F1) |
| Paginazione | fine lista | precedente / «Page n sur N» / successivo |
| Footer | ogni pagina | due `nav` etichettate: cinque link legali distinti + navigazione del sito, con **i quattro pubblici sempre presenti**, in entrambi gli stati di gate e nelle quattro lingue |
| Skip link | primo elemento di `<body>` | «Aller au contenu principal» → `#main-content` (`docs/qa/design/state-skiplink-fr-390.png`, `docs/qa/design/state-skiplink-ar-390.png`) |

### 11.5 La cromatura come una sola misura

`--chrome-block-size` è calcolata in CSS da `--chrome-utility` più `--chrome-masthead` e la consuma
`scroll-padding-block-start` in `base.css`; sotto la testata V5 `v5/chrome.css` la ripete come `--header-h` + 16 px
(`html:has(.site-header)`), misurata da
`tests/frontend/test_browser_w2_c1.py::test_focus_is_not_obscured_by_the_sticky_letterhead` (2.4.11). **Nessun
JavaScript scrive geometria su un elemento di cui hanno bisogno anche i suoi fratelli**: `nav.js` scrive
`--portico-scrim-top`, `--portico-lead` e `--portico-h` sull'**header**, e lo scrim e i pannelli — suoi discendenti —
le ereditano (fu ciò che chiuse G-23 per il cassetto di allora; il foglio, dall'11 ottobre 2026, possiede la sua testa).

### 11.6 La console — «Tre livelli»: la rail, la barra di contesto, la cornice di pagina; sotto 64rem la rail distesa

La cromatura di ogni pagina autenticata (piano V5.4 §1.18 D06, §3.5 voce 3; W3-A). File:
`templates/partials/portal_chrome.html`, `templates/portal/partials/rail_nav.html`,
`templates/portal/base_portal.html`, `apps/portal/static/portal/v5/_shell.css` (parziale importato da
`console.css`, §2.1), `static/js/rail-pref.js`, `static/js/src/console.js` (§16). I dati vengono da **un solo
costruttore**, `portal.services.shell_navigation(user, space, active)`: ogni produttore di una pagina della console
lo interroga, così le chiavi della rail di uno spazio sono le stesse su ognuno dei suoi indirizzi.

**Gli spazi.** Uno spazio è un insieme di pagine con UNA rail: «Espace réservé», che ogni conto ha, e «Espace
entreprise», lo spazio di lavoro dell'impresa. Una pagina appartiene a uno spazio per la sua rotta; nulla è
memorizzato. Un conto che ha due spazi trova, in testa alla rail, la via verso l'altro — chiamata con il nome di
quello spazio — e mai tra le pagine. Le dieci destinazioni di «Espace réservé» restano dieci per tutti; i registri
che un ruolo possiede le precedono; e «Communications d’identité» — il pannello con cui una persona decide se
un'impresa può conoscere la sua identità, che il modulo di selezione elencava in una rail propria, sulle sole sue
pagine — è una pagina di «Échanges» per il conto a cui qualcuno l'ha chiesta, e per nessun altro: le chiavi dipendono
dal conto, mai dalla pagina.

**La rail, tre livelli per forma, mai per decorazione.**

| Livello | Dove | Forma |
|---|---|---|
| 1 · lo spazio | la testa: il marchio fermo sulla sua tegola di carta (40 px, raggio `sm`, marchio a 24 px: il seggio del rilascio del loader, W1-D), il nome in «ILE Wordmark» e, sotto il nome, lo spazio della pagina | una riga di testo propria nel secondo inchiostro della notte; poi, per chi ha due spazi, la riga dell'altro con la sua freccia |
| 2 · la sezione | «Mon rôle» (i registri che un ruolo possiede, per primi) · «Parcours» · «Dossier» · «Échanges» | una parola sull'asse del testo, nell'inchiostro più piccolo della notte; un filetto, senza parola, dove la parola ripeterebbe la sua unica voce («Academy») o il nome dello spazio |
| 3 · la pagina | le voci | glifo (20 px in un disco di 32) + parola, righe da 44 px (40 sotto 760 px d'altezza con un puntatore fine), raggio `sm` |

- **Un solo asse del testo a 64 px** — il nome, lo spazio, le sezioni, le pagine, il conto — e **una sola colonna
  dei glifi a 32 px**, che non si sposta quando la rail si piega: 248 px aperta, 64 px compatta.
- **«Il lume»** segna la pagina corrente: il suo glifo su un **disco di carta acceso** (`--surface-raised`, la
  stessa materia della tegola del marchio), sulla lastra notturna della riga, la parola al peso dei titoli. Nessuna
  barra al bordo, nessun filetto accanto alla lista. Una volta per copia della rail (la rail fissa, il cassetto).
- **Il piede è fisso** e la lista scorre tra testa e piede: il conto — il glifo e la parola di chi è (Persona ≠
  Impresa ≠ Istituzione ≠ Università ≠ professionista ≠ équipe del progetto: i ruoli prima, poi il tipo di conto;
  `apps/core/icons.py`) con il nome, che porta al profilo —, «Se déconnecter», il controllo della rail, la lingua
  (quella corrente con il proprio nome; le quattro si aprono **sopra** il controllo, in colonna sull'asse del
  testo) e «Site public», nelle sue due parole. L'ultima riga del piede tiene nelle quattro lingue («Italiano» e
  «Sito pubblico» sono la coppia più lunga: 15 px di margine misurati); se una parola non entra — la spaziatura
  del testo scelta dalla persona, SC 1.4.12 — va a capo sotto la riga, mai sopra il controllo vicino. A 1366 × 657
  la rail aperta di una persona sta intera: dieci pagine, tre parole di sezione, la testa e il piede. Una parola
  su due righe (il registro di un ruolo) tiene 4 px d'aria nella sua riga, che sale a 48 px.
- **Aperta per default da 80rem** — a 1280, 1366, 1440 e 1920 nessuno incontra una rail di sole icone —; tra 64rem
  e 80rem il default è la rail compatta, 64 px di soli glifi, finché le etichette brevi della rail compatta con
  etichette (80 px, DS V5 SC01) non sono firmate (B1; DL54-60). La scelta è ricordata
  (`localStorage`, chiave ile.rail) ed è scritta sul `<body>` **prima del primo frame** da `rail-pref.js`; senza
  script la rail resta aperta e il suo controllo non è offerto. La larghezza si muove solo per il gesto della
  persona (200 ms, `--ease-layout`; 0 ms a movimento ridotto): **nulla si anima al caricamento**, salvo il rilascio
  del loader sul marchio, una volta per accesso (§12).
- **Un glifo che sta da solo** (le voci della rail compatta, «Se déconnecter», il controllo della rail) mostra la
  sua parola al passaggio (dopo i 400 ms del tooltip) e al fuoco della tastiera — l'unico tooltip del livello
  superiore del sistema degli overlay (W2-A, O11): sulla riga del controllo, **oltre il bordo della rail**
  (`data-tip-beyond`) — mai sopra la rail, dove coprirebbe il controllo accanto finché il puntatore vi si posa —,
  intera nel viewport, a capo se è lunga. Resta finché il puntatore vi si posa e se ne va con Esc, ovunque sia il
  fuoco (SC 1.4.13); la rail aperta la rifiuta quando la parola è già accanto al glifo (`overlay:tip`). La parola del conto dice il nome e chi è («… — Université ou organisme de formation»): ciò che la
  rail aperta ha dovuto tagliare si mostra intero allo stesso modo. La parola resta sempre nel DOM per i lettori di
  schermo.
- **Tastiera**: ↑ ↓ Home Fine tra le voci; l'anello di fuoco è disegnato dentro la riga (il bordo di scorrimento
  della lista taglierebbe un anello esterno).

**La barra di contesto** (56 px, `--ctx-h`; da 64rem l'unica sede del vetro nella console) è il **livello della
pagina**: il breadcrumb. Da 64rem il conto, la lingua e «Site public» stanno al piede della rail; sotto 64rem la
barra è la testa della rail distesa (qui sotto).

**Sotto 64rem: la rail distesa** (W3-A, passo 2; DL54-66 … DL54-71). La rail non è disegnata al bordo di lettura: è
distesa in tre pezzi, nella stessa notte (O13: «la stessa cromatura notturna») — le due barre non portano vetro, né
ombra, né filetto: la notte finisce dove comincia la carta.

| Pezzo | Che cosa porta | Misure |
|---|---|---|
| **la barra superiore** — la testa della rail | il marchio fermo sulla sua tegola di carta (32 px disegnati, 44 al dito; porta alla prima pagina dello spazio; il seggio del rilascio del loader, W1-D), il livello della pagina come titolo (l'ultima voce del breadcrumb, 15 / 20 · 600) e il conto: il menu di V4 finché il sistema di overlay non porta il popover — sul telefono il solo glifo sul disco notturno del piede della rail, 44 px al dito, il nome resta il suo nome accessibile; da 48rem il nome accanto. Nessun «≡» | 48 px sotto 48rem, 56 px nella fascia fino a 64rem |
| **la barra inferiore** — le pagine della rail | quattro voci al più e «Menu», una volta sola, alla fine di lettura: il glifo (20 px in un disco di 32) sopra la sua parola; nella fascia da 48rem il glifo sul suo disco **accanto** alla parola, la riga della rail | alta quanto la sua voce più alta: 52 px con le parole su una riga, 66 con una parola su due (55 e 72 in arabo); 56 px nella fascia |
| **il cassetto** — la rail intera | la testa, la via verso l'altro spazio, le sezioni e le pagine, e **il piede della rail**: chi è il conto (→ il profilo), «Se déconnecter» come riga **con la sua parola** (un dito non trova hover), la lingua con il proprio nome (le quattro si aprono sopra, come nella rail) e «Site public». Il controllo della rail non c'è: nel cassetto nulla si piega | `<dialog>` nativo dal bordo di lettura, 320 px o l'88 % dello schermo; righe da 44 px |

- **Le parole sono le etichette vive, intere**: nessuna è accorciata e nessuna è nuova (le etichette brevi sono
  testo: B1). 12 / 14 nelle lingue latine — il pavimento della scala —, 14 / 17 in arabo (D21). Una voce prende la
  larghezza che le sue parole chiedono; un'etichetta sta su una riga o sulle sue **due corse** — «Tableau» · «de
  bord», «Demandes qui me» · «sont confiées» —, mai su tre, mai spezzata dentro una parola, mai tagliata. È il
  costruttore a dividerla (`portal.services._bar_lines`: allo spazio che lascia più corta la corsa più lunga):
  un foglio di stile sa dimensionare una sede sulla parola più lunga o sulla riga intera, non sulle due righe
  bilanciate. Una barra le cui parole non stanno su una riga di un telefono (`_bar_stacks`) le disegna subito sulle
  due corse; una barra araba, o di due voci, tiene la sua riga. L'aria fra due voci (6 px per lato, dentro il
  bersaglio) cede **prima** delle parole, e due parole di voci diverse non stanno mai a meno di 6 px.
- **Tre voci dove quattro non stanno** (`_bottom_yield`): sotto 22,5rem per ogni barra — esce «Mes dossiers» dalla
  barra di una persona (il cruscotto si apre sul fascicolo), «Mes documents» da quella di un conto con due spazi,
  «Mon entreprise» da quella dello spazio impresa —; sotto 30rem per la barra che porta il registro di un ruolo
  («Demandes qui me sont confiées», «Désignation des professionnels», «Processus assignés»), da cui esce «Mes
  documents». La voce resta nel cassetto, a una pressione di più.
- **«Il lume»** sulla barra è lo stesso disco di carta acceso della rail, la parola nel primo inchiostro della
  notte; il peso non cambia — una parola non cambia riga quando la sua pagina diventa la corrente. Nessuna barretta
  al bordo. Nella fascia la voce corrente non ha lastra: un'etichetta che va a capo lascia la sua sede più larga
  delle sue parole, e una lastra lo disegnerebbe.
- **«Menu»** è un collegamento al cassetto (`#console-drawer`, `data-overlay-open`): il sistema degli overlay
  (`overlay.js`, importato da `console.js`, §16) gli dà il ruolo e i tasti di un bottone e apre il cassetto come
  drawer modale — Invio e Spazio, `aria-expanded`, la trappola con `aria-modal` e l'unico velo, il fuoco sulla pagina
  in cui si è, Esc, la pressione sul velo, il fuoco di ritorno, nulla aggiunto all'indirizzo; «Slide» dal bordo di
  lettura in 320 ms, fuori in 200 ms. **Senza script** resta un collegamento e porta comunque al cassetto: il foglio
  del sistema lo mostra (`html.no-js .overlay:target`) e il controllo di chiusura, un collegamento anch'esso,
  riporta alla pagina. Esc chiude prima la lista delle lingue, poi il cassetto; una finestra
  allargata oltre 64rem chiude il cassetto. Mentre il cassetto è aperto la pagina dietro il velo non scorre. Nel
  cassetto un nome lungo — un indirizzo e-mail — va su una seconda riga, mai sotto un'ellissi: la rail lo mostra
  intero nella parola accanto al controllo, e un cassetto quella parola non l'ha.
- **La cromatura che resta sullo schermo**: 114 px in francese, italiano e inglese, 103 px in arabo, su ogni conto
  misurato da 360 a 430 px — 120 al più (V4: 113 con le parole spezzate e tagliate, 174 sul fascicolo, 177 su «Ma
  situation»). Dove il viewport è corto (sotto 30rem d'altezza: un telefono in orizzontale) o molto stretto (sotto
  22,5rem: una finestra al 400 %, SC 1.4.10) la barra superiore se ne va con la pagina e resta la sola barra
  inferiore; nel cassetto, allora, il piede non è più fisso e la rail intera scorre sotto la testa.
- **La barra d'azione di una pagina** (O63). Una pagina che tiene UN atto alla portata del pollice dichiara la sua
  barra (`data-console-action`; oggi la barra del fascicolo, `data-file-action-bar`, letta com'è): prende il posto
  delle quattro voci, sul vetro della pagina, e «Menu» tiene la stessa estremità della stessa riga — 48 + 61 px.
  Il piede del questionario su «Ma situation» («Précédent», il suo conto, «Continuer», «Enregistrer et
  recalculer») non è una barra d'azione: sotto 64rem chiude il suo modulo dove il modulo finisce e i suoi controlli
  vanno a capo invece di stringersi.
- **Aree sicure, bersagli, fuoco.** La pagina disegna fino al bordo (`viewport-fit=cover`): le quattro
  `env(safe-area-inset-*)` sono lette una volta, sui lati logici (`--safe-top`, `--safe-bottom`, `--safe-start`,
  `--safe-end`, le ultime due scambiate in arabo), e imbottiscono la barra superiore, la barra inferiore, il
  cassetto e la cornice di pagina. Ogni controllo delle due barre e del cassetto è almeno 44 × 44 px, con ogni
  puntatore. Ciò che riceve il fuoco si ferma libero dalle due barre (`scroll-padding-block`, SC 2.4.11). Colori
  forzati: le due barre prendono un filetto, la voce corrente il contorno e il disco del sistema. Movimento
  ridotto: il cassetto è al suo posto senza scorrere; nulla della cromatura si anima al caricamento.
- **In arabo** la tegola è al bordo destro, il conto a sinistra, «Menu» all'estremità sinistra della barra e il
  cassetto esce da destra; il marchio non si specchia mai (lo stesso file in ogni lingua), né il glifo dei gradini;
  un titolo scritto in un'altra lingua — un corso in francese su una pagina araba — è tagliato alla SUA fine.
- **Sulla carta** la pagina è la pagina: né rail, né barre, né cassetto, né lo spazio che la pagina tiene per loro
  (una barra fissa sarebbe stampata su ogni foglio) — reso subito: la transizione della larghezza della rail tace
  in stampa.

**La cornice di pagina.** Un solo bordo d'inizio per tutto ciò che una pagina disegna, a 32 px dalla rail (16 px
sotto 48rem), in una colonna di 1320 px al massimo; 32 px sotto la barra, la testata di pagina, 32 px, il contenuto
(SP-5). **Una sola testata di pagina**, qualunque markup la famiglia della pagina porti ancora — `page_header.html`,
`.ctx`, `.ws-head`, i titoli delle pagine dei documenti: il titolo alla taglia della console (28 / 36, 600), la sua
riga di contesto al corpo (15 / 24), l'azione primaria della pagina alla fine della riga del titolo; il livello è il
breadcrumb, nella barra. Il piè di pagina è una riga sola sullo stesso bordo.

**Skip link.** Dopo «Aller au contenu principal» (§11.4) la console ne offre un secondo: la rail da 64rem
(`#console-rail`), «Menu» sotto (`#console-menu`, il collegamento della barra inferiore che lo script rende il bottone
del cassetto) — dove la navigazione era l'ultima tappa del Tab: tre tasti per arrivarci.

**Angoli e ombre.** La cromatura disegna 4 px e pieno: due dei tre raggi di una schermata della console (§7.5);
il terzo è l'8 dei pannelli. Un bottone, nella console, prende l'angolo che V5 dà a un controllo — 4 px — dalla
cornice (`.console .btn`), dove il foglio V4 dei bottoni ne disegna ancora 6: la piega «6 → 4» del piano, una volta
per ogni pagina. Nessuna ombra nella navigazione (SH-2); il menu della lingua, l'unico strato della rail, prende il
livello dei menu mentre è aperto.

**Dopo la revisione** (W3-A, il passo di correzione; DL54-72).
- **Uno spazio comincia dove comincia la sua rail.** Il marchio della rail, la tegola della barra superiore e il
  marchio del cassetto portano, per un conto che possiede il registro di un ruolo, alla prima voce di «Mon rôle» (la
  designazione dei professionisti, le richieste affidate, i processi assegnati) — non al cruscotto di una persona, il
  cui unico atto è il questionario di un richiedente —; per ogni altro conto, al cruscotto, che per lo staff resta a
  un tasto, sotto «Parcours» (`portal.services.shell_space`, nessuna query in più).
- **La prima pagina di uno spazio chiude il suo breadcrumb su sé stessa** — «Espace réservé › Tableau de bord»,
  «Espace entreprise › Tableau de bord», la parola che la rail accende —, come ogni altra pagina; il nome dello
  spazio non è mai un collegamento alla pagina in cui si è. Sotto 64rem il titolo della barra superiore dice la
  pagina.
- **Il bordo di scorrimento della lista.** Dove la lista prosegue sotto il piede, una fascia della lastra notturna
  (24 px) sta alla sua fine e dice che altro segue; la notte della rail, che scorre con la fine della lista
  (`background-attachment: local`), la copre quando l'ultima riga è in vista o quando nulla scorre. Due immagini
  nominate in `tokens.css` («console chrome»: `--rail-scroll-edge`, `--rail-scroll-cover` — un foglio d'app non
  disegna gradienti), nessuno script, nessun movimento; in colori forzati non c'è. Lo stesso nel cassetto.
- **Bersagli**: le tre pagine legali del piè di pagina sono alte 24 px almeno, 44 × 44 sotto un puntatore
  grossolano; le righe del menu del conto nella barra superiore, 44 px al dito. Gli **skip link** disegnano il loro
  anello dentro la scatola notturna (dove la rail è compatta la scatola sta sulla carta: 9,93 : 1 a ogni larghezza).
- **La riga sopra il titolo del ContextHeader** — il nome del conto, spesso in un'altra lingua — abbraccia le sue
  parole come il titolo: in arabo sta sul bordo di lettura. **Nella fascia** il nome del conto accanto al suo glifo
  va su una seconda riga invece di perdere la sua fine (SC 1.4.12).

Verifica: `tests/frontend/test_console_shell_w3_a.py` (il costruttore, i produttori, il markup, i fogli; la barra
di ogni conto, le due corse di un'etichetta, la voce che esce), `tests/frontend/test_console_shell_browser_w3_a.py`
(1366 × 657, la scelta prima del primo frame, i tre tasti, «il lume», le parole dei glifi, l'arabo) e
`tests/frontend/test_console_phone_browser_w3_a.py` (sei conti × quattro lingue × da 320 a 412 px: le parole intere,
due righe al più, 120 px di cromatura; il cassetto, «Menu» senza script, la fascia, l'arabo, le aree sicure, i
colori forzati, il movimento ridotto, la barra d'azione, la carta).

---

### 11.7 I cruscotti — la persona, l'impresa, il ponte: il NowPanel, «il registro», ciò che si piega

La prima pagina di «Espace réservé» per una persona (piano V5.4 §3.5 voce 4, §1.15, §1.18 traccia T; W3-B). File:
`templates/portal/dashboard.html`, `templates/portal/partials/now_panel.html` (il NowPanel, lo stesso sul cruscotto
dell'impresa), `apps/portal/static/portal/v5/_dashboard.css` (parziale importato da `console.css` dopo
`v5/_shell.css`, §2.1), `portal.services.dashboard_context` e `now_panel`, `cases.services.next_action` (T1). Il
cruscotto dell'impresa e il ponte dei conti che non sono una persona seguono più sotto, nella stessa grammatica. Le
carte sono quelle di W1-C (`static/css/v5/card.css`): **la carta d'azione** per il NowPanel, **la striscia di sintesi**
per i fatti del fascicolo; nessuna griglia di carte uguali, nessuna cifra in grande, nessuna lavagna da riordinare
(§1.15 del piano: l'ordine lo dà il sistema).

**L'ordine — anche quello del DOM: h1 → NowPanel → percorso.**

| # | Regione | Che cosa dice | Forma |
|---|---|---|---|
| — | la testata | chi e quale fascicolo: il nome del conto, il titolo, il riferimento (ILE Mono), lo stato e da quando | la testata della cornice (§11.6); nessuna azione: il primario è del NowPanel (O50) |
| 1 | il NowPanel | che cosa fare ora: la pièce, il suo stato, la sua data, chi ne risponde, e **il solo primario** che lo fa | la carta d'azione, **l'unico piano rialzato** dello schermo (SH-8) |
| 2 | «Mon parcours» | dove si è | il binario «La soglia» (§11.9, W3-D): la linea in piano da 56rem del componente, la carta e la sua divulgazione sotto; fermo al caricamento |
| 3 | «Dossier» | l'obiettivo, l'avanzamento, chi interviene | la striscia di sintesi; da 64rem accanto al NowPanel (la griglia la colloca, il DOM la tiene dopo il percorso, che non ha controlli: il fuoco va NowPanel → fascicolo) |
| 4 | «Mes documents» | «il registro» per chi tiene la pièce, poi ogni pièce che la persona deve trattare, ciascuna col suo atto, poi quelle in mano ad altri | piatte sotto filetti, righe da 64 px allineate in sottogriglia |
| 5 | «Mes échéances» · «Communications» | le date e i messaggi | liste piatte, una riga ciascuno |
| 6 | Academy · «Derniers dépôts» · le fonti della pre-valutazione | ciò che è secondario | `<details>` nativi (la divulgazione di W1-C, §10): il default lo sceglie il server dai dati — Academy aperta se c'è un'iscrizione — e non è ricordato |
| 7 | «Mon compte» | email, tipo, ultimo accesso; Profil, Sécurité du compte, Back-office | una riga quieta al piede, finché il popover del conto (W2-A) non la tiene |

**Il NowPanel — quattro varianti, scelte dal sistema** (`now_panel`, mai dalla persona, mai ricordate):
«à vous» (l'azione è della persona: occhiello «Votre prochaine action», il primario è l'atto stesso con le parole del
registro — «Déposer la pièce», «Remplacer la pièce»; quando la porta delle CGU blocca il deposito, «Consulter» sulla
pagina della pièce, che dice la porta, e la nota del registro «Acceptation des Conditions d'utilisation requise.»: mai
un bottone che promette un atto che la sua pagina non sa fare — il flusso d'accettazione attende G1) · «en attente
d'un tiers» (occhiello «Prochaine étape», «Cette étape ne dépend pas de vous.», nessun primario, un «Consulter»
quieto) · «rien à faire» («Aucune action ne vous est demandée pour l'instant.», e «Responsable»: l'incarico vivo più
recente del fascicolo, ruolo — organizzazione, come lo dice la striscia del fascicolo) · «pas encore de dossier» («Le
questionnaire d'orientation», «Commencer le questionnaire» — e **la porta del committente**, il componente
`doorway.html` così com'è disegnato: l'unico stato vuoto della console che la mostra). **Una data scaduta prende il
NowPanel** — salvo che l'azione sia già scaduta o un esito bloccante fermi il percorso — ed è disegnata lì soltanto:
il suo titolo e la sua nota, sotto l'«Origine :» della pagina delle scadenze, sono parole dell'équipe in nessuna lingua
registrata, disegnate nella loro direzione (`dir="auto"`, la scatola sul bordo di lettura del pannello); se era la sola
data, «Mes échéances» non è disegnata (il pannello porta la data e la via a tutte). La regione è nominata dall'occhiello
e dall'obbligo (`aria-labelledby="db-now-eyebrow db-now-title"`): chi deve muovere, poi che cosa. Ogni pièce è
disegnata **una volta**: quella del NowPanel non torna nella lista (`data-piece`, verificato); una pièce che la persona
ha depositato, o in esame, non nomina nessuno al posto di chi la tiene — la pastiglia lo dice.

**T1 — una sola prossima azione** (`cases.services.next_action(case, reader=…)`), su ogni obbligo aperto del
fascicolo — le voci della checklist E le pièce che attende —, sulla precedenza che il dominio già aveva: un esito
bloccante (che porta alla sua pagina), poi l'obbligo scaduto, poi la data più vicina (a parità una voce prima di una
pièce), poi l'obbligo aperto della persona (altrimenti il primo di chiunque), poi il questionario, poi niente. Un
cambio di presentatore e nient'altro: nessuna regola, nessun permesso, nessuno stato. Le pièce si leggono con
l'autorizzazione dell'app dei documenti, al momento della query: un titolo riservato alla persona e
all'amministrazione non arriva a chi non può leggerlo. Il fascicolo e il cruscotto nominano la stessa pièce.

**«Il registro»** (O62): le pièce raggruppate per chi le tiene — da trattare (la persona), in corso (altri), valide
— ognuna col segno del suo stato a 16 px, il colore del gruppo (`--ledger-to-act`, `--ledger-in-hand`,
`--ledger-settled`): il colore è il gruppo, la forma è lo stato. Le parole dei gruppi sono del catalogo («À faire»,
«En cours», «Valide») finché la revisione dei testi non firma «À vous · En cours · Réglées» (B1). I segni sono
decorazione sopra le parole e i conteggi.

**Le misure.** Una sola ombra sullo schermo, quella del NowPanel (con l'alone del nodo corrente del percorso, di
W3-D: due valori); angoli 8 (carte, striscia) · 4 (controlli) · pieno (chip, dischi). Nulla si muove al caricamento:
la riga che V4 disegnava sotto il percorso a ogni visita è ferma sul cruscotto. Una data non è mai detta dal solo
colore: glifo, data e — vicina o passata — «Bientôt», «En retard». Un non letto è peso, punto d'inchiostro e la
parola «Non lue». Le parole di un record — nelle liste il titolo di una data, l'oggetto di un messaggio, il nome di un
file; la motivazione della pre-valutazione; il nome di un'organizzazione — sono isolate nella loro direzione
(`dir="auto"`), come nel registro del ponte. Sotto 48rem i fatti del NowPanel
due per due (il disco di «Responsable» e la sua parola restano insieme), il primario a tutta larghezza, una riga di
pièce su tre righe; sotto un puntatore grossolano ogni link è alto 44 px — quello di una riga di lista con le parole
centrate, la data subito sotto; quello dentro la frase di una regione vuota anche. Le due cifre dell'avanzamento e la
parola fra loro non si separano (spazi non separabili). Il titolo e il testo del NowPanel passano il filtro della
spaziatura francese (`typo`, W2-D): un guillemet non resta mai solo a fine riga. Ogni parola è del catalogo: nessun
testo nuovo.

**Il cruscotto dell'impresa** (W3-B, secondo passo): `templates/companies/dashboard.html`,
`portal.services.company_dashboard` e `company_now_panel` sopra `companies.services` (`next_action`, `needs_of`,
`communications`), invariato; la vista ne fa una chiamata. La stessa grammatica e le stesse regole:

| # | Regione | Che cosa dice | Forma |
|---|---|---|---|
| — | la testata | «Entreprise», la denominazione legale come h1 (nella sua direzione, la scatola sul bordo di lettura), la verifica come parola col suo registro — un fatto che il progetto ha verificato sull'entità, mai l'approvazione di qualcuno —, settore, luogo | la testata della cornice; nessuna azione |
| 1 | il NowPanel | la prossima azione dell'impresa, una sola: dichiarare l'impresa, completare o trasmettere un bisogno, esprimere il primo — col **solo primario** nelle parole del presentatore; per trasmettere una bozza completa, quando il conto può farlo, l'atto stesso della pagina del bisogno — il suo modulo POST e le sue parole, «Transmettre au projet» —, con «Ouvrir le besoin» quieto accanto; «en attente d'un tiers» mentre l'équipe verifica l'impresa o esamina i bisogni (nessun primario); «rien à faire». Il bisogno di cui parla presta il suo stato e il suo riferimento (ILE Mono) ed è disegnato lì soltanto (`data-need`) | la carta d'azione, l'unico piano rialzato |
| 2 | «Mon entreprise» | l'immatricolazione (ILE Mono) e il referente; la denominazione è già l'h1, detta una volta; la frase sulla verifica | la striscia di sintesi; da 64rem accanto al NowPanel |
| 3 | «Mes besoins en compétences» | «il registro» dei bisogni per chi li tiene — da fare (le bozze dell'impresa), in corso (trasmessi, in esame, presi in carico, in attesa: del progetto o di un attore), chiusi (chiusi, ritirati) —, poi le bozze con il loro atto, poi gli altri bisogni con chi ne risponde, poi i chiusi: cinque al più; «Tous mes besoins»; «Nouveau besoin», secondario, sotto | piatti sotto filetti, la sottogriglia delle pièce su tre colonne; l'ultima colonna una misura fissa (15rem al più), così il font che arriva non ridimensiona le colonne condivise |
| 4 | «Communications» | i messaggi del conto | lista piatta |

Senza impresa: la testata del workspace con le sue parole, il NowPanel della dichiarazione e, accanto, «Communications»
(come la pagina della persona senza fascicolo). Nessuna persona su questo
schermo, nessun conteggio di persone: il cruscotto gira intorno ai bisogni. Le parole dei gruppi sono del catalogo
(«À faire», «En cours» come sul cruscotto della persona; «Clos», lo stato del bisogno); la porta resta lo stato vuoto
della persona soltanto.

**Il ponte** (W3-B, secondo passo): i conti che non sono una persona — un'istituzione, un'università, un professionista,
un conto d'impresa senza il ruolo della persona — non hanno ancora né fascicolo né prossima azione propria (i loro
spazi sono P1 della matrice dei requisiti): **nessun NowPanel**, la pagina non afferma ciò che il sistema non sa. I
loro registri (`portal.services.bridge_cards`, invariato, costruito solo per loro: F9; `templates/portal/partials/card.html`)
sono sezioni piatte nella grammatica della persona, e il sistema ne ordina la priorità: nella colonna principale
prima ciò che scade e ciò che è arrivato (le date — una scaduta detta dalla sua pastiglia in *azione*, terracotta come
sul cruscotto della persona, mai il rosso di un rifiuto —, le comunicazioni), poi ciò che hanno inviato e depositato;
di fianco l'organizzazione cui appartengono, come i fatti del fascicolo sulla pagina di una persona. In testa alla
colonna principale, un solo link quieto dove vive il lavoro del conto, quando un tale luogo esiste — il suo spazio
(«Espace entreprise») o il registro del suo ruolo («Processus assignés»…), con le parole della rail; nessuno per
un'istituzione o un'università: nessuna affermazione. Ogni sezione: il
glifo del dominio, la parola, uno stato che merita di essere detto come pastiglia («1 en retard», «1 non lue»), il
solo link alla pagina intera; poi le righe con data, tipo e stato (il titolo di una riga, parole di un record, nella
sua direzione); una regione vuota è una riga. Poi la pre-valutazione, la stessa sezione della persona (il registro
dell'orientamento le cede il posto: mai due volte), e la riga del conto. Le sei carte uguali con la cifra in grande se
ne sono andate con le loro regole.

**Le misure del secondo passo.** Un piano rialzato sull'impresa (il NowPanel) e un valore d'ombra, nessuno sul ponte;
angoli 4 · 8 · pieno; nulla si muove al caricamento; nessun trabocco a 1440, 1024, 834 (la banda 768–1023) e 390; in
arabo tutto specchiato, le parole di un record nella loro direzione dentro un isolato in linea, così la riga resta sul
bordo di lettura. I portatori d'identità (§3.1 voce 7 del piano): «il lume» nella rail, «I cerchi» — ogni stato una
pastiglia: la verifica, i bisogni, il bisogno del NowPanel —, «il registro» dei bisogni, ILE Mono per i riferimenti e
l'immatricolazione; sul ponte «il lume», «I cerchi» e i glifi del registro dei concetti.

### 11.8 «Mes pièces» — il registro, la riga, lo stato

Il registro delle pièce richieste, nella console (piano V5.4 §3.5 voce 5, §1.2; `DOCUMENT_WORKSPACE.md` §0, §6–§14;
W3-C). File: `templates/documents/partials/register.html` (disegnato da `templates/portal/documents.html` e da
`templates/documents/index.html`, lo stesso presentatore e la stessa autorizzazione), `templates/components/document_row.html`
(§10), `templates/documents/requirement_detail.html` e `templates/documents/partials/depot.html` (una pièce),
`documents.presenters` (`register_context`, `register_groups`, `next_piece`, `row_act`, `state_filters`). Fogli: tre
partial della console — `apps/portal/static/portal/v5/_workspace.css` (il registro), `_table.css` (i file stessi),
`_depot.css` (una pièce) — importati dal foglio delle pagine dei documenti, `apps/documents/static/documents/documents.css`,
nell'albero raccolto (`../portal/v5/_x.css`, §2): solo le pagine che disegnano il registro li caricano, mai `main.css`
né l'ingresso della console.

**L'ordine di un fascicolo** (un blocco `.ws-case` per fascicolo, il container delle sue misure):

| # | Regione | Che cosa dice | Forma |
|---|---|---|---|
| — | la testata della pagina | il titolo bloccato «Mes pièces» e la sua riga di contesto (sul telefono solo per le tecnologie assistive: il primo schermo è delle pièce — W-1) | la testata della cornice (§11.6); nessuna azione: il primario è della striscia |
| 1 | la testa del fascicolo | «Pièces du dossier», il riferimento (ILE Mono, isolato), la ricerca al bordo finale — nella disposizione a schede solo da tredici pièce | una riga |
| 2 | «il registro» | tre corse per chi deve agire — «À faire» (una pièce aperta di cui risponde la persona), «En cours» (tutto il resto non regolato: una pièce aperta che spetta a un altro attore, una depositata, una in esame), «Valide» —, ciascuna un conteggio a 20/28, un segno di 16 px per pièce (il colore è la corsa, la forma è lo stato, `aria-hidden` — i segni sono «il registro» come lo disegna il cruscotto: `.db-ledger__marks` e il colore del suo gruppo `.db-ledger__group--*`, `_dashboard.css`; qui solo il loro posto, una famiglia disegnata una volta, V5.8 regola 3) e un link al suo gruppo (un indice, non un filtro; il suo anello di focus disegnato dentro la corsa, che la striscia ritaglia); poi **il solo primario della pagina** con la sua pièce e la sua data («Votre prochaine action»: la pièce di T1 quando il lettore può agire, altrimenti la precedenza di T1 sulle pièce aperte su cui agisce); la frase bloccata dei conteggi la chiude e si ferma a «… sur … validées» (la terza proposizione contava le pièce aperte, un insieme che nessuna corsa mostra) | **l'unico piano rialzato** dello schermo (il livello della carta d'azione, come il NowPanel del cruscotto); l'atto primario finisce sullo stesso asse degli atti delle righe |
| 3 | il filtro di stato | gli stati nell'ordine del registro (`STATE_ORDER`: scaduto, non valido, mancante, da sostituire, in esame, depositato, valido), ciascuno il segno della sua pastiglia e il suo conteggio — la legenda dei segni; uno stato senza pièce è una parola, non un link; `?état=` nell'URL, condivisibile, senza script | da 52rem di registro una traccia segmentata (8 · 4); sotto, **un solo controllo di 44 px** — un link al foglio — che apre le stesse voci (`documents/partials/state_filter.html`, un solo markup disegnato due volte) nel **foglio dal basso del sistema degli overlay** (`components/sheet.html`, W2-A: lo scrim, la presa, «Fermer» sempre presente, Esc; il focus sulla voce corrente e di ritorno sul controllo; senza script il link lo mostra sul posto) |
| 4 | la collezione | **gli stessi tre gruppi** della striscia, nello stesso ordine e con le stesse parole — una partizione, un vocabolario —, ciascuno una sezione col suo titolo; una riga per pièce (`document_row.html`) | un foglio piatto sotto un filetto, righe divise da filetti, sei colonne in sottogriglia; il gruppo «À faire» col filetto di 3 px del suo colore |
| 5 | la nota del registro | «L’état d’une pièce dit ce que le dossier a reçu, et rien de plus. Aucune ligne de ce registre ne vaut acceptation.» | accanto al registro, 16 px sotto, mai una nota grigia in fondo |
| 6 | i file stessi | «Tous les fichiers de votre compte», «Documents de mon organisation», «Autres fichiers déposés» (ogni «Supprimer» descritto dal suo file; chiede prima, nell'alertdialog del sistema degli overlay — il nome del file nella domanda, «Annuler» la risposta sicura, «Supprimer» il contorno granata che invia il form della riga; senza script il form parte subito: `documents/partials/delete_confirm.html`) | **una vera tabella**, il nome del file è il link che lo scarica, intero; sotto 40rem della sua regione ogni file è una voce d'elenco — il nome sulla sua riga, poi «tipo · dimensione · data» su una riga attenuata, l'atto al bordo finale, il filetto del registro tra i file —, mai uno scorrimento laterale; nessuna cella porta `data-label`, così il pop-in etichettato di `portal.css` (etichette maiuscole, filetti blu di 2 px) non le raggiunge |

**La disposizione segue la larghezza che il registro riceve** (container query `wscase`, non il viewport): sei colonne
— pièce · stato · responsabile · scadenza · atto · apertura — da 66rem; cinque, con l'attore sotto il titolo, da 52rem;
schede sotto 52rem (lo stesso markup, poste con `order`: l'identità prima, poi lo stato e la data, l'attore, la nota,
l'atto a tutta larghezza). Misurato sui dati QA: 1440 sei colonne; 1280 e 1100 cinque; 390 e 360 schede, il titolo
della prima scheda a 650 px (la soglia del cancello: 700 a 390 × 844).

**La riga è il link** (§10 `document_row.html`): ogni punto della riga che mostra il suo hover apre la pièce (0 punti
morti su 42 sondati, fr e ar, 1440 e 390); l'atto, il solo altro controllo, sta sopra. Nessun menu di riga, nessun
«Consulter». Un atto c'è solo su una pièce aperta su cui il lettore agisce; la riga regolata è quella tranquilla.

**Lo stato e la data.** Ogni stato è la pastiglia «i cerchi» (W1-C) con il suo registro: «En examen» in lapis, «Valide»
in inchiostro senza spunta (O14). La data tiene sempre il suo glifo nella sua sede di 20 px (`alarm-clock` mai sotto
i 20 px), con «Bientôt» (ambra, *attesa*) o «En retard» (terracotta, *azione*) accanto: il rosso non dice mai il
ritardo. **F8**: la scala dell'urgenza si ferma quando la pièce è depositata — una pièce depositata in scadenza domani
si legge calma. **F13**: sulle pagine delle scadenze una data passata parla `overdue` (*azione*) e una vicina `soon`
(*attesa*); «En retard» non è più disegnato come un rifiuto. **Un solo orologio decide una scadenza**: il ritardo di una
pièce e di una voce della checklist (`is_overdue` dei modelli, che T1 legge) si misura su `core.clock` come l'urgenza
del registro e la pagina delle scadenze — su una corsia o sull'anteprima la data di riferimento sta per oggi.

**Una pièce** (`requirement_detail.html`), nell'ordine del bisogno: lo stato (la parola, la sua regola, il motivo di
questa pièce), il deposito mentre la pièce è aperta (dopo i depositi quando è depositata, in esame o valida), ciò che
è chiesto, la fonte numerata, i depositi — per ciascuna versione la data, l'impronta, la dimensione, poi due righe che
non si fondono mai: ciò che l'antivirus ha detto del FILE, ciò che una persona ha concluso della PIÈCE; «Télécharger»
descritto dalla sua versione. La banda del fascicolo non è disegnata: la testa nomina il fascicolo col suo riferimento.
Sotto lo stato, vuoto a riposo, lo spazio dove arriva la risposta del Dépôt a un deposito (`[data-piece-answer]`);
`[data-piece-head]` segna ciò che la testa dell'anteprima dice già dalla riga (la pastiglia, la scadenza).

**Il Dépôt** (`templates/documents/partials/depot.html`, un solo markup per le due strade — una pièce richiesta e un
file fuori requisito, `upload.html` —; `static/js/src/depot.js`, importato da `console.js` dove un Dépôt è disegnato;
`_depot.css`; `DOCUMENT_WORKSPACE.md` §11). I livelli: il campo nativo con le sue formati (senza script è tutto il
Dépôt: il controllo del browser, un vero invio, la risposta del server come pagina); la zona che tiene l'input vero
dentro di sé — con lo script l'input la copre, trasparente: una pressione ovunque apre la scelta, un file lasciato
cadere è dell'input stesso, nessuno script legge un file —, tratteggiata a 8 px, piena in laguna con il suo lavaggio
quando un file la sorvola; le guardie del client, che ripetono le regole del server lette dal form
(`documents.presenters.deposit_rules`: vuoto, oltre la dimensione, fuori dall'elenco; una data di validità già passata,
per cortesia — decide l'orologio del server); il trasferimento con il suo `<progress>` vero, «Annuler» accanto, la chiave
L2 sul bottone. **Le undici risposte** (§11.1) composte sul posto, mai una pagina nuova: la stessa form allo stesso
endpoint con l'intestazione `X-ILE-Depot`, a cui `views.py` risponde in JSON (sempre 200: una risposta del Dépôt, non un
fallimento della richiesta) — un rifiuto resta sulla riga del file (la frase del server, il doppio filetto di
*rifiuto* al bordo di lettura, la zona come sola via: un altro file); una data già passata sotto il suo campo; la
limitazione come avviso, il file ancora scelto e «Déposer» come nuovo tentativo; il cancello delle Condizioni al posto
del form, la sua frase e il suo link nella cornice tratteggiata della porta chiusa (la stessa di
`terms_required.html`); un deposito come la pièce riletta (il suo stato è cambiato), la risposta sotto lo stato con il
segno dello stato depositato che si disegna (anello, poi punto: una transizione da `@starting-style`, mai al
caricamento, 0 ms sotto movimento ridotto — nessuna spunta, nessun verdetto); la rete o il server in errore, la loro
frase. Un file rifiutato marca il suo campo in errore (`aria-invalid`, il rifiuto nella sua descrizione), come ogni
campo in errore; la dimensione mostrata non contraddice mai un rifiuto («0 ko», «10,1 Mo»). Sulla strada fuori
requisito la risposta nomina il file prima della frase del server e la zona torna per un altro file. Una risposta che
non è del Dépôt ricarica la pagina: decide il server, nulla è mai inviato due volte. Due
regioni vive, fuori da ciò che una rilettura sostituisce, dicono l'inizio (il file scelto) e la fine (la risposta),
assertive per un rifiuto; i blocchi composti non sono vivi. Ogni parola è del catalogo: le frasi del server e i
blocchi `<template>` del markup.

**L'anteprima** (`templates/documents/partials/piece_drawer.html`, `static/js/src/piece-drawer.js`; `DOCUMENT_WORKSPACE.md`
§12; piano §1.14 «Preview drawer»): il titolo di una riga, il suo atto e l'atto della striscia aprono la pièce nel
**drawer del sistema degli overlay**, non modale accanto al registro sul desktop (`data-overlay-modal="none"`: niente
scrim, la pagina resta usabile — un'altra riga sostituisce il contenuto e lo scorrimento non si ripete) e un foglio
modale sul telefono (≤ 40rem). La testa è piena a 0 ms dalla riga — «Pièce demandée» e il riferimento, il titolo nella
sua lingua, la riga stessa: la pastiglia, l'attore, la data, scritti come parole e attributi in posti già disegnati —,
con «Fermer» e la chiave L2 dopo i 400 ms che l'occhio perdona; il corpo è la pagina della pièce stessa (il suo
`<article>`, letto dal suo URL), posata da L3 al primo arrivo di una pièce; ciò che la testa dice già
(`[data-piece-head]`) non è disegnato due volte. Mentre è aperto accanto all'elenco, lo spazio di lavoro gli fa posto
una volta dipinto il primo fotogramma del drawer (il nuovo layout del registro resta fuori dal fotogramma della
pressione) e il registro si dispone secondo la larghezza che gli resta (la sua container query: schede a 1440). **La
storia**: l'apertura spinge l'URL della pièce (un ricaricamento porta alla pagina intera); Esc, «Fermer» e Indietro lo
chiudono e torna l'URL del registro con il suo `?état=`; una sostituzione rimpiazza la voce (`replaceState`); mentre il
drawer possiede la sua voce, quella del registro non ha scorrimento da ripristinare (`history.scrollRestoration`
manuale): la pagina resta dove la persona è. **Il registro dice quale pièce è aperta**: il titolo della sua riga
`aria-current`, la riga nello stato selezionato (la superficie dell'hover e un filetto di 2 px al bordo di lettura);
la striscia quando nomina quella pièce, il suo atto ridotto a secondario — il drawer tiene l'atto; spostato a ogni
sostituzione, tolto alla chiusura. Quando il registro si ridispone, la riga premuta resta sotto il puntatore. Il focus
va al titolo all'apertura e torna al titolo della riga della pièce mostrata alla chiusura — anche dopo una
sostituzione, e dentro il viewport; l'atto di una riga lo manda al campo del Dépôt;
dopo un deposito la pièce e il registro dietro di essa sono riletti (la striscia, la riga, i file). In arabo il drawer
sta a sinistra (O5). Senza script le righe sono link alle pagine delle pièce. Le due pagine del registro collegano il
foglio di sola pagina del sistema (`css/dist/core/overlay-panels.css`, CONTRACT §1 di W2-A): la testa e il corpo del
drawer e del foglio non entrano in `main.css`.

**Il focus della tastiera** su una riga e sulla zona del Dépôt si legge dalla modalità d'ingresso
(`html[data-input="key"] … :focus-within`, head.js), e l'attesa della zona da `[data-sending]`, scritto da `depot.js`:
mai uno stato letto attraverso `:has()`. Un `:has(:focus-visible)` faceva ridisegnare a Blink tutta la pagina da
`<body>` a ogni focus che entrava o usciva dal titolo di una riga (≈ 650 elementi su «Mes pièces» a 390; 4 dopo), e
l'apertura e la chiusura dell'anteprima lo pagavano due volte.

**Le parole sono del catalogo**: nessun testo nuovo. Le parole dei gruppi e le loro glosse proposte («À vous · En
cours · Réglées»), «Prochaine pièce à fournir», le distanze («dans 4 jours»…), «Sans échéance» sono della revisione
dei testi (B1, voce 3): elencate nelle note della famiglia, mai scritte qui.

### 11.9 Il viaggio — «La soglia»: un passaggio pubblico, un binario della console

Il percorso Marocco → Italia come segno del prodotto (piano V5.4 §3.5 voce 6, §1.18 D16; ricerca
`JOURNEY_SIGNATURE.md` §5.3–§5.7; W3-D). **Un disegno di passaggio e un disegno di binario, mai un terzo**:

| Disegno | Dove | File | Marcatore (D16) |
|---|---|---|---|
| il **passaggio pubblico** «la linea» | la home (i quattro passi neutri dell'orientamento a gate chiuso) e, con un import nel loro foglio dopo `_interior.css`, le porte, le pagine dei consigli e il questionario (dalla fusione di W3-D) | `components/stepper.html`, `static/css/v5/_journey-passage.css` | il **numerale** sopra una stazione aperta |
| il **binario** della console | «Mon parcours» sul cruscotto e in testa alla pagina «Mon parcours», il percorso e la Timeline del fascicolo, lo Stepper di «Ma situation» | `components/{journey_rail,case_timeline,wizard_stepper}.html`; `apps/portal/static/portal/v5/_journey-nodes.css` (il vocabolario) composto da `_journey-rail.css` (il percorso, la Timeline) nel foglio di sola pagina `apps/portal/static/portal/journey.css` e da `_journey-stepper.css` (lo Stepper) in quello di «Ma situation», `portal/situation.css` (mai nei fogli condivisi: V5.8; ogni pagina carica solo ciò che disegna) | il **glifo** della fase (`core.icons.JOURNEY`); il titolare, quando lo si conosce, su una riga propria |

**Il binario.** Una linea in piano fra le due rive («Maroc» al bordo di lettura, «Italie» alla fine), attraversata da
due soglie — A, le autorità competenti (`stamp`), prima della prima tappa sul lato italiano; B, il territorio italiano
(`ile-arch`, l'unico arco del viaggio), prima dell'arrivo —, ciascuna con la didascalia di giurisdizione del sito
(`pages.services.JURISDICTION_SEGMENTS`, le stesse voci del catalogo). Una soglia è una colonna stretta (2rem) con il
suo filetto che attraversa la linea, e **un luogo**: un fascicolo in `SELECTION` («Phase gérée par un acteur
autorisé») vi sta sopra — la colonna si allarga, la voce corrente della lista è la soglia, nessuna tappa è corrente
(OJ2; `portal.services.journey_for`, che fino a W3-D lo metteva sulla tappa 1). **Uno stato senza posto sulla linea**
(`SUSPENDED`, `CLOSED`) non ha voce corrente: nulla vi dice «Vous êtes ici» — la pastiglia della testata dice lo
stato; nel fascicolo `cases.presenters.journey_with_dates` legge il registro, e le tappe fino all'ultimo posto tenuto
sulla linea sono dietro il fascicolo, datate, la voce dove si è fermato senza linea percorsa oltre (il nodo «in
attesa» di un fascicolo sospeso aspetta il contratto del registro, ricerca §7.3). I nodi: dietro il fascicolo un
punto d'inchiostro di 10 px, mai una spunta (O14); dove sta un anello laguna di 18 px sul suo velo (un disco, non
un'ombra); avanti un anello aperto di 12 px. La linea: 2 px, laguna fin dove il fascicolo è passato, il filetto
decorativo dopo; ogni voce disegna il tratto dal suo nodo a quello della voce dopo, l'ultima tappa fino a «Italie»
(nessun gradiente, nessuna misura, nessuno script; in arabo la stessa griglia si specchia; la linea non prende mai il
puntatore). Le densità: **la linea in piano** da 56rem della larghezza del componente (una container query: sul
cruscotto da 64rem), le parole di ogni tappa sotto il suo nodo al bordo di lettura, «Vous êtes ici» sulla riga che è
solo della voce corrente; **la carta** sotto (il telefono, una colonna stretta): ciò che è vero ora — il glifo e le
parole della voce corrente, «Étape n sur 7» (su una soglia, la sua didascalia in testa), «Vous êtes ici» — poi le
sette tappe dietro la divulgazione nativa «Où j’en suis», chiusa, come spina (dove `::details-content` manca, la
carta e la divulgazione restano a ogni larghezza); **la descrittiva** nel fascicolo: la spina con la data di ogni
tappa raggiunta (in cifre tabulari, alla fine della riga: «ILE Mono» resta ai riferimenti). La pagina «Mon parcours»
porta in testa lo stesso componente del cruscotto, con le stesse parole, quando la persona ha un fascicolo; sotto,
le pre-valutazioni salvate. La Timeline del fascicolo è la stessa spina, gli eventi in inchiostro dal più recente, il
primo acceso; lo Stepper di «Ma situation» la stessa spina, un nodo per domanda (pieno quando c'è una risposta: alle
domande si risponde in qualunque ordine, quindi la linea non è mai «percorsa»), una linea in piano di nodi sotto
64rem. **Il peso**: il binario è il CSS proprio del viaggio, mai nei fogli condivisi della console (V5.8 del
committente, DL54-87) — un vocabolario (`_journey-nodes.css`: una linea, tre nodi) e due componenti: il percorso e
la Timeline (`_journey-rail.css`) nel foglio di sola pagina `portal/journey.css`, che collegano il cruscotto, «Mon
parcours» e il fascicolo dopo i due fogli della cromatura; lo Stepper (`_journey-stepper.css`) nel foglio di sola
pagina di «Ma situation», `portal/situation.css`, dopo il modulo guidato. Ogni pagina carica solo ciò che disegna
(la sentenza definitiva dell'orchestratore, 12 ottobre 2026).

**Fermo al caricamento.** Nessuna animazione, nessuna transizione, nessun `will-change` nei parziali del viaggio: il disegno
è il suo stesso fermo, che è anche lo stato a moto ridotto e quello senza JavaScript. «Le relais» della ricerca — una
luce, una volta, da dove il fascicolo era visto l'ultima volta a dove sta — chiede una posizione «vista l'ultima
volta» conservata: è una politica (classe C, piano §7.2), non perseguita in V5.4; per questo non c'è un
`journey-rail.js`. **A′** (OJ1): nessuna parentesi di titolare finché la mappa degli attori (D9) non è firmata; le
perline dei documenti (OJ3) non sono disegnate: sul cruscotto le pièces sono «il registro» (W3-B, DL54-80), una volta.
Le parole OJ5 / OJ6 aspettano B1; il titolo della Timeline e le parole delle distanze delle scadenze sono del
committente (B1 voce 4).

**Il passaggio pubblico.** «La linea», una sequenza vera su una linea in piano: i numerali sopra stazioni aperte, le
parole sotto; lungo il bordo di lettura sul telefono, in riga dal 48rem quando ci sta (tante colonne quante stazioni);
un flusso (`current`) riempie in inchiostro i passi dietro e ispessisce nel primario il suo anello. W3-F1 l'ha
disegnata per primo sulle porte; alla fusione di W3-D (12 ottobre 2026) le due mani sono diventate un solo
disegno — il parziale e il componente di qui, che le porte caricano dopo `_interior.css` e che
`pages/partials/_linea.html` include —, le porte identiche al pixel ma per l'antialias del bordo degli anelli
(l'anello è aperto fino al suo fondo, quale che sia il capitolo: sulla home il fondo è il gradiente BRAND); il modello Marocco → Italia stesso, sulla home, lo dice una volta il sentiero
dell'hero (DL54-41). I portatori d'identità della console (§3.1 voce 7 del piano): sul cruscotto e nel fascicolo «La
soglia» — le due rive, le due soglie, la linea percorsa —, accanto a «il lume» nella rail e a «I cerchi».

## 12. Motion

> **Design V5 (11 ottobre 2026, W2-A)** — il sistema degli overlay (`static/css/v5/overlays.css`; piano V5.4 §1.14,
> §1.5 MS-O2, MS-O4, MS-O5, MS-O6) non porta **nessun keyframe**: ogni overlay è una transizione nei due sensi, così
> una seconda pressione riparte da dove il pannello è (O1) — l'entrata da `@starting-style`, l'uscita con
> `transition-behavior: allow-discrete` su `display` e `overlay`, che tengono il pannello nel livello superiore per
> la durata dell'uscita; nulla che dia forma al pannello è scritto sotto `[open]` / `:popover-open` (B1), e il
> pannello che esce è `inert` (B2). Lo scrim di un tipo modale è l'unico `.overlay-scrim` (la regola INP): la stessa
> opacità, sugli orologi del pannello che sta sopra. Gli orologi: il dialog dal centro, .96 → 1 con l'opacità in `--motion-emphasized`,
> lo scrim in `--motion-standard`, fuori in `--motion-fast` sulla curva d'entrata (una piccola superficie, MS-O2); il
> drawer «Slide», `translate` di ±100 % in `--motion-emphasized`, fuori in `--motion-standard` su `--ease-layout`, lo
> scrim con lui; lo sheet su `--spring-sheet` (550 ms), fuori in 200 ms su `--ease-layout`; il menu con 4 px di caduta
> lontano dal comando in 200 ms, fuori in 120; il tooltip dopo la soglia `--tooltip-delay`, in `--motion-fast`, e un
> vicino del gruppo caldo a 0 ms. Da tastiera 0 ms (`html[data-input="key"]`, e `[data-instant]` per un'apertura
> `instant` da script), l'ultima regola del foglio; sotto `prefers-reduced-motion: reduce` una sola opacità di
> `--motion-reduced` e nessuna trasformazione in nessun fotogramma. Il parziale solo di pagina
> `v5/_overlay-panels.css` (il dialog, lo sheet, il `::backdrop` nativo, il tooltip `::after`), che viene dopo
> `main.css`, ripete per le sue famiglie il moto ridotto e il gradino 0 dopo le loro regole. Il keyframe `dialog-in`
> di `components.css` §21 se n'è andato col dialog V2. `static/js/src/overlay.js` non anima nulla: scrive lo stato
> al tempo zero e lascia il moto al foglio.
>
> **Design V5 (9 ottobre 2026, W2-B)** — l'ingresso «Il varco» (piano V5.4 §1.13 «Le vie convergono al varco») porta
> sei keyframe fuori dalla cascata, nel foglio della pagina e nel suo parziale. In
> `apps/accounts/static/accounts/entrance.css`: **`varco-run`** — la luce di una via che corre dalla notte alla soglia —,
> **`varco-draw`** — la via accesa che si disegna dietro la sua luce —, **`varco-out`** — la perla che si spegne dove
> arriva — e **`varco-glint`** — l'opacità della luce nella frase d'arrivo, e della via accesa dietro di essa, che si
> spegne quando la luce arriva (la correzione di revisione dell'11 ottobre 2026: quattro perle su filetti grigi si
> leggevano come scintille). In `static/css/v5/_door.css`:
> **`door-frame-rise`** e **`door-frame-hold`** — la luce che sale sul telaio della porta: un ritaglio che sale dalla
> soglia mentre il disegno al suo interno resta fermo. Muovono solo `transform` e `opacity` di strati dipinti una volta;
> quelli di un passaggio hanno il solo `from` e finiscono sullo stato proprio dell'elemento, senza riempimento: un
> secondo dopo l'ultimo gesto `document.getAnimations()` è vuoto. Le durate sono token — il passaggio `--motion-slow` più
> `--motion-fast` (i 600 ms del piano: una sequenza di livello 2), il ritorno `--motion-standard`, i gradini con lo
> scaglione `--motion-stagger`, la frase d'arrivo `--motion-route-light` con lo scaglione `--motion-route-stagger` (2,4 s
> in tutto, una volta, dopo il dipinto della porta) —, la curva è `--ease-sine` (la luce). Dalla tastiera il foglio azzera
> le transizioni (`html[data-input="key"]`, livello 0) e lo script non chiede il passaggio; sotto
> `prefers-reduced-motion: reduce` ogni token vale 0 ms e ogni stato compare al suo termine, senza viaggio. All'invio
> dell'accesso la chiave del palcoscenico gira una volta e tiene: è `sig-turn` di `v5/loader.css`, lo stesso primitivo.
> Nulla gira in loop; nulla parte da solo dopo la frase d'arrivo.
>
> **Design V5 (8 ottobre 2026, W1-D)** — il loader «Lume» (piano V5.4 §1.9; DL54-07, DL54-08, DL54-09) porta due
> keyframe in cascata, in `v5/loader.css`: **`sig-turn`** — la chiave che gira una volta sul proprio gambo, `rotateY`
> 0 → 360°, e torna sul marchio verbatim: l'ingresso del login (`--motion-slow`, `--ease-turn`, poi tiene) e la chiave
> occupata di ogni bottone d'invio (`--motion-emphasized`, `.btn.is-busy::after`, poi tiene attenuata e si accende alla
> risposta) — e **`sig-seat`** — le righe di un frammento asincrono che salgono di 4 px in `--motion-standard`, con lo
> scaglione `--motion-stagger`, al primo arrivo soltanto. Il rilascio — la porta che si illumina dall'occhio della
> chiave sulla prima pagina della console dopo un accesso riuscito, una volta per sessione, attraverso il caricamento
> della pagina — vive nel parziale generato `v5/_loader-light.css` della sola console (`lume-light-o`, `lume-light-t`,
> `lume-ink-o`: una fase, `--motion-door`, allineata in fase; curve letterali uguali ai token, perché `var()` dentro
> `@keyframes` non anima). Nulla gira in loop; ogni durata è un token azzerato sotto `prefers-reduced-motion: reduce`, e
> `fill-mode: both` posa ogni strato sul suo fermo; nessun `will-change`. `btn-busy` di `v4/buttons.css` se n'è andato
> col foglio il 9 ottobre 2026 (W1-C): la chiave di `v5/loader.css` è la sola faccia d'attesa di un bottone.
>
> **Design V5 (5 ottobre 2026, W1-A)** — i token di moto entrano in `static/css/v5/tokens.css` come il piano V5.4
> §1.5 li ha decisi: **nessuna durata aggiunta né cambiata** (`--motion-fast` 120, `--motion-standard` 200,
> `--motion-emphasized` 320, `--motion-slow` 480 per le sole righe pubbliche, `--motion-draw` 900, le luci delle vie
> 1200 / 400, lo scaglione 60, la chiave 1200, la porta 1600, la luce 2200, la soglia d'attesa 400); due aggiunte,
> `--motion-reduced` (80 ms: sotto il moto ridotto un overlay usa una sola opacità) e `--ease-turn`
> (`cubic-bezier(0.77, 0, 0.175, 1)`, l'unica curva della chiave che gira — loader, login, hero; DL54-05); le molle
> come gemelle `linear()` (`--spring-soft` / `-snappy` / `-sheet`). Il blocco del moto ridotto è ripetuto in V5
> perché un `:root` successivo vince su una media query precedente: azzera `--motion-fast`, `--motion-standard`,
> `--motion-emphasized`, `--motion-slow`, `--motion-draw`, `--motion-route-light` e le tre durate delle molle; non
> azzera `--motion-key`, `--motion-door` e `--motion-luce` (un ciclo a 0 ms gira su se stesso: i fogli che li usano
> mostrano lo stato di riposo), né la soglia `--motion-wait`, gli scaglioni e `--motion-reduced`. Le curve sono
> `--ease-enter`, `--ease-exit`, `--ease-layout`, `--ease-sine` e `--ease-turn`, nessuna con un punto di controllo
> fuori da [0, 1] sull'asse y: nessun rimbalzo. `tests/frontend/test_v5_tokens.py::test_the_narrow_overrides_of_the_names_v5_declares_are_restated`
> tiene il blocco. **L'uso della regola** — la cancellazione del blocco universale di `components.css`,
> `--motion-reduced` solo sull'opacità, il cancello unico del moto via script — e i suoi test sono di W1-D. Nessun
> keyframe nuovo in W1-A.
>
> **Design V4 (24/09/2026, sera)** — `docs/design-v4/DESIGN_SYSTEM_V4.md` §7 è ora normativo, sopra il
> MOTION_SYSTEM V2 citato sotto: sei durate (`--motion-fast` 120, `--motion-standard` 200,
> `--motion-emphasized` 320, `--motion-slow` 480, `--motion-draw` 900 ms, `--motion-ambient` 28 s), tre
> curve (`--ease-enter`, `--ease-exit`, `--ease-layout`; i nomi V2 `--ease-out` / `--ease-in` /
> `--ease-standard` e `--motion-instant` / `--motion-base` sono alias in `v4/tokens.css`), due molle
> (`SPRING_SOFT`, `SPRING_SNAPPY` in `static/js/src/motion.js`), quindici pattern e un budget per
> modalità. `--motion-slow` cambia significato (320 → 480 ms): gli otto siti V2 che lo usavano sono
> passati a `--motion-emphasized`. Il divieto di effetti legati allo scroll e di vetro che segue è
> abrogato dal chiarimento del committente delle 20:58; le regole restano vere per i layer 1–7 finché
> non sono migrati. I keyframe `tide-1`, `tide-2` e le varianti RTL se ne sono andati con `v2/hero.css`;
> `route-current` (la corrente lungo le quattro vie della porta, 28 s lineari) se n'è andato con l'hero V4
> (W2-D, 8 ottobre 2026). **L'hero V5.4** (`templates/pages/home/_hero.html`, `apps/pages/static/pages/css/hero.css`,
> `static/js/src/hero.js`; HERO_FINAL.md, DL54-05, DL54-08, DL54-11) non dichiara keyframe: ogni luce è un elemento
> che già esiste, mosso con la Web Animations API su `transform` e `opacity` soltanto, su un solo orologio — la
> scoperta (≈ 3,55 s al desktop, ≈ 2,8 s al telefono: le quattro nominate → il sentiero, una perla di luce con la sua
> scia calda e l'intarsio che resta acceso dietro di lei → l'arco → i gradini → la chiave che gira una volta in 800 ms
> sulla propria curva `--he-ease-turn` (tokens §4.2; il loader tiene `--ease-turn`), con un alone dietro e un bagliore
> sull'anello quando il volto torna → la porta che si apre come luce e resta socchiusa a .9 → le quattro insieme → la
> quiete), una volta per sessione, interrotta dove sta da una pressione, un tasto, la perdita della vista (la chiave
> atterra in avanti al passo del proprio giro); la mano (hover a puntatore fine, tocco) la rimanda lungo l'unico
> sentiero ogni volta, in ≈ 1,3 s (V5.5), e così il focus da tastiera su un accesso; un bottone reale sopra la chiave
> d'oro (`.he-replay`, nominato dal catalogo, disegnato solo da `hero.js` su una pagina che si muove; al passaggio del
> puntatore e al focus l'alone della chiave si accende) rimanda l'intera sequenza con Invio, Spazio o un clic (la
> correzione di revisione del 9 ottobre); dalla correzione della revisione senior (DL54-42) la pressione di un dito
> aspetta — lo stato e la luce si armano 100 ms dopo l'appoggio, o al sollevamento se viene prima, e cadono su
> `pointercancel`: uno scorrimento che parte da una tessera non mostra nulla, un tocco li tiene 700 ms mentre la pagina
> seguente risponde —, e dove nulla passa sopra (`hover: none`) la stessa luce breve riparte una volta ogni volta che
> l'hero torna in vista dopo esserne uscito, mentre l'alone della chiave resta acceso piano a riposo; la luce impiega ≈ 930 ms dalla riva alla porta su qualunque parete (≈ 700 ms
> sotto la mano), anche dove la parete prende la pagina; gli stati della mano sono CSS, a
> 0 ms dalla tastiera; a riposo 0 animazioni, 0 `will-change`; con `prefers-reduced-motion: reduce` l'immagine
> completa, identica all'hero assestato, senza bottone; sotto colori forzati nessuna luce. Dal 9 ottobre 2026 (dopo
> l'unione di W1-D) il modulo passa dall'unico cancello del movimento: chiede `reducedMotion()` a `motion.js` —
> l'impostazione della persona o il flag `html.rm` dell'anteprima, sotto il quale prima la scoperta partiva lo stesso —
> e ogni `animate()` e ogni attesa di frame passano da `play()`, `nextFrame()` e `afterPaint()`; le stesse chiamate,
> negli stessi frame, sullo stesso orologio (W2-D, `QA/v54/w2-d/NOTES.md` §8.4). Il `mega-in` di `v4/shell.css` e i `menu-in*` di
> `components.css` se ne sono andati con la cromatura V5 (W2-C1): il pannello del portico è una transizione (§11.1). `v4/workspace.css` aggiungeva, col fascicolo (gate D),
> **`tl-light`** (l'ultimo nodo della Timeline che si accendeva una volta al caricamento): **uscito** col
> viaggio V5 (W3-D, §11.9), che dipinge quel nodo acceso dal primo frame. il pattern 1 «page enter» (`ws-in`, `console.css`) è stato costruito per la revisione del gate B e
> **rimosso** alla revisione del gate E: il suo `translate` faceva del workspace il contenitore di una barra
> `position: fixed` (gate D) e la sua opacità 0 → 1 nascondeva all'osservatore l'elemento LCP reale (gate E).
> La console arriva completa. `v4/buttons.css` aggiungeva `btn-busy`, il misuratore a tre tacche del bottone
> occupato (`.btn.is-busy`), in loop per 1200 ms lineari: **rimosso** col foglio quando la chiave L2 di
> `v5/loader.css` ne ha preso il posto (W1-D, poi W1-C). `v4/workspace.css` aggiunge due keyframe del
> pattern «draw» (una volta, al caricamento, mai in loop): **`notch-fill`** (le tacche del misuratore, 320 ms
> con scaglione di 60) e **`strip-fill`** (i segmenti della HealthStrip, 320 ms), solo sotto
> `prefers-reduced-motion: no-preference`. **`rail-draw-y`** e **`rail-draw`** (la linea della JourneyRail che si
> disegnava, verticale e orizzontale, 900 ms con scaglione di 120, a ogni visita) sono **usciti** col viaggio V5
> (W3-D, §11.9): «la console non ha entrata né scaglione al caricamento» (piano V5.4 §1.5) e il binario è fermo da
> sé — la regola del cruscotto che lo fermava (W3-B) se n'è andata con lui.
>
> **Superato dal 24 settembre 2026** da `docs/design-v2/MOTION_SYSTEM.md`, che è normativo: sette
> funzioni ammesse, quattro durate {120, 180, 240, 320 ms} più un tracciato immersivo, tre curve,
> due molle, **un solo oggetto vivo per pagina** e il moto ridotto come stato completo. Le regole
> qui sotto restano vere per i layer 1–7 della cascata finché la propagazione non è finita.
>
> Ciò che la direzione V2 cambia in modo sostanziale: lo scroll **può** animare, ma solo attraverso
> `scroll()` / ScrollTimeline e solo dove serve a orientare (la rotta del progetto pilota che si
> disegna, la fotografia della porta che scorre di 18 px). Non è parallasse decorativa: è
> l'avanzamento del lettore lungo un percorso, ed è interrompibile, fermo fuori schermo e assente
> con «riduci movimento». (Entrambi gli usi sono usciti: la fotografia con l'hero V4, la rotta del
> progetto pilota col passo 3 di W2-D, il 9 ottobre 2026 — sotto l'hero V5.4 i capitoli della home non
> si muovono: restano le transizioni di 120 ms sulle frecce delle righe e dei link, azzerate dal moto
> ridotto.)
>
> I keyframe della cascata V2 sono `tide-1` e `tide-2` — la marea del territorio nell'hero: due
> strati di curve di livello che traslano di 12 e 9 px su 28 e 34 secondi, lineari e alternati,
> **ognuno nel proprio elemento `<svg>`** perché così la traslazione vive sul compositore e non
> ridipinge il disegno. Le varianti `tide-1-rtl` e `tide-2-rtl` sono le stesse con la specchiatura
> araba composta nella trasformazione. Sono l'unico oggetto vivo della home, in pausa fuori dal
> viewport, a scheda nascosta e su richiesta («Suspendre le mouvement»), e non esistono affatto
> sotto `prefers-reduced-motion: reduce`.

**Nulla si muove allo scroll.** `.reveal`, lo stagger con `IntersectionObserver`, il `will-change`
che tiene vivo un layer di compositing per tutta la vita della pagina e il timeout di sicurezza da
2.5 s sono sulla lista di demolizione, insieme a `initCounters()` e `.counter`. La visibilità del
contenuto non deve mai dipendere dal successo di uno script: oggi un'eccezione in uno dei sei
inizializzatori che girano prima di `initReveal()` lascerebbe ogni blocco `.reveal` a `opacity: 0`
per sempre. `--duration-reveal` e `--reveal-distance` valgono già `0ms` e `0` nello shim, così che
nulla si animi mentre i template vengono ripuliti.

Non si muovono mai: il contenuto della pagina allo scroll, le fotografie, i titoli, il wordmark, i
numeri, le fasce di sezione, le righe di tabella e di lista, la testata (nessun rimpicciolimento,
nessun nascondersi allo scroll). La calma istituzionale è contenuto che semplicemente *è lì*.

Quattro livelli. Tutto ciò che sta fuori da questi quattro si cancella.

| Livello | Che cosa | Durata | Curva | Spostamento |
|---|---|---|---|---|
| **1 STATO** | chevron di disclosure, filetto `aria-current`, checkbox e radio, pressione `:active` | `--motion-fast` (120 ms) | `--ease-out` | ≤ 4 px |
| **2 SUPERFICIE** | drawer, pannello del mega-menu, dialog, dropdown | `--motion-base` (200 ms) in ingresso | `--ease-out` | la propria dimensione: un drawer percorre `translateY(-100%)`, non 8 px |
| **3 IL SEGNO** | **la firma** — un filetto rubrica da 2 px che si disegna dal bordo d'attacco sotto la destinazione quando il sistema sposta il lettore contro la sua volontà: focus sul riepilogo degli errori, cambio di passo del wizard, arrivo di un messaggio | `--motion-slow` (320 ms), una sola volta | `--ease-out` | la larghezza del filetto stesso |
| **4 AVANZAMENTO** | upload, avanzamento del wizard | il lavoro reale trascorso | lineare | — |

Tetti: nulla supera 320 ms salvo il livello 4; nulla percorre più di 12 px salvo una superficie di
livello 2. Vietati: parallax, animazioni legate allo scroll, loop decorativi, gradienti in
movimento, carousel in autoplay, e l'hover come **unico** riscontro di qualunque cosa — ogni
affordance di hover ha un equivalente `:active` e `:focus-visible`, perché quattro degli eventi di
movimento della build respinta erano solo-hover e quindi non esistevano su un telefono.

**Il movimento ridotto è la postura di default.** Tutto il nuovo va avvolto in
`@media (prefers-reduced-motion: no-preference)`; il livello 3 degrada a un filetto statico disegnato
all'istante (il segno compare comunque, semplicemente non si disegna). Il blocco
`prefers-reduced-motion: reduce` esistente resta esattamente com'è scritto: è implementato bene e per
intero, ed è migliore di quello della maggior parte dei prodotti commerciali. Tre livelli, tutti
attivi insieme: `tokens.css` azzera `--motion-fast`, `--motion-base` e `--motion-slow` (e quindi, via
shim, `--duration-fast`, `--duration-base` e `--duration-slow`); `components.css` §29 forza
`transition-duration: 0.01ms !important`, `animation-duration: 0.01ms !important`,
`animation-iteration-count: 1 !important`, `scroll-behavior: auto !important` e disattiva i keyframe
di mega-menu e dialog; `main.js` legge la stessa media query.

Keyframe esistenti in `components.css` — nessuno: i tre `menu-in*` del mega-menu V1 sono stati cancellati con la
cromatura V5 (W2-C1: il pannello del portico è una transizione, §11.1) e `dialog-in` col dialog V2 (W2-A: il
dialog del sistema degli overlay è una transizione, §10).

---

## 13. Iconografia

- **Un solo sprite, una sola mano** (design V5, W1-B; piano V5.4 §1.7, §2.3, §2.4). `static/img/icons.svg` è
  GENERATO da `scripts/build_icons.py` a partire da una sorgente per simbolo in `static/icons/src/<id>.svg` (griglia
  24 × 24; area viva 21.5 unità per i disegni pittorici) e dal registro `apps/core/icons.py`, che è l'unico elenco
  dei simboli: 110 simboli V5 e 3 alias V4 (`home`, `list`, `globe`) finché i loro produttori non vengono
  ripuliti — il catalogo di «Vivre en Italie», una card del cruscotto, i default dei percorsi; `user` e `key`
  sono usciti il 9 ottobre 2026, quando nessun produttore li emetteva più. Le rail della console leggono le
  mappe `NAV` e `COMPANY_NAV` del registro. Mai modificare lo sprite a mano; `python
  scripts/build_icons.py --check` è il test di attualità. Peso ≤ 32 KB grezzi (≈ 6.5 KB gzip), una richiesta.
- **Un concetto, un glifo** (R-DES-009 confermata). Il registro ha tre livelli e gli stati: *identità* (`ile-arch`,
  `ile-key`, `ile-steps`, `ile-mark`: dal marchio, mai tonalizzati, mai specchiati), *concetto* (pubblici, attori,
  domini, fasi: possono portare la tonalità del 12 % e raggiungono i template attraverso le mappe del registro —
  `{{ chiave|concept:"dominio" }}`, `{{ attore|actor_glyph }}` — non come letterali), *utilità* (azioni, direzione,
  avvisi: monolinea, mai tonalizzate) e gli *stati* «i cerchi» (`st-*`: contorno = aperto, pieno = concluso;
  dipinti dalla chip con il colore del registro, mai scelti da un template). **Persona ≠ Impresa ≠ Istituzione ≠
  Università**: `person`, `building`, `institution`, `university`, mai sotto i 16 px nei dischi. Geometria: disegni
  ILE e donatori Lucide 1.48.0 (ISC) sotto il trattamento ILE — `docs/design-v5/ICON_LICENSES.md`; nessuna libreria
  di icone nel prodotto.
- **Il tratto**: ogni tracciato dello sprite porta `vector-effect: non-scaling-stroke`, quindi lo `stroke-width`
  della regola `.icon` (`components.css` §2) è in px CSS a ogni misura — **1.5 px da 14 a 24 px, 1.67 px a 32 px,
  2 px a 48 px** — **terminali quadri, giunzioni a spigolo**, `currentcolor`. Misure della scala: `.icon--xs` 14 ·
  `.icon--sm` 16 · `.icon--md` 20 (default) · `.icon--lg` 24 · `.icon--xl` 32 · `.icon--hero` 48 (`--icon-xs` …
  `--icon-hero`). Un componente che dimensiona `.icon` da sé conserva il tratto da 1.5 px: nessun foglio scrive uno
  `stroke-width` più sottile su un glifo (lo stato vuoto lo scriveva a 1.25 — tolto il 9 ottobre 2026).
  `.icon--inline` mette un glifo SULLA riga di un testo (un occhiello): il reset disegna ogni svg come blocco, e
  senza quella classe il glifo resterebbe da solo sopra le sue parole.
- **Soglie di misura** (`MIN_SIZE`): ogni simbolo ha la misura minima sotto cui non si rende, misurata sullo sprite
  costruito (lo spazio negativo che un pixel di chiusura cancella a DPR 1 ≤ 10 %; `ile-arch` 16, `ile-mark` 20,
  `concierge-bell` 20, `handshake` 24 — i due polsini si fondono a 20 px…). I **gemelli** (`TWINS`, somiglianza ≥ 0.75 a 16 px) non stanno mai insieme in una lista,
  un menu, una riga o un insieme di avvisi. I simboli con un segno di spunta (`CHECK_BEARING`: `check`,
  `circle-check`, `badge-check`, `vote`) segnano solo un atto della persona o un atto di un'autorità, mai una chip,
  un nodo del percorso, un registro, una rail o un disco attore.
- **Uso**: `{% svg_icon "nome" %}` → `<svg class="icon" aria-hidden="true" focusable="false"><use
  href="/static/img/icons.svg?v=<impronta>#icon-nome"></use></svg>` (lo sprite è servito con l'impronta del suo
  contenuto). Secondo argomento = classi; terzo = etichetta (`role="img"` + `aria-label`, al posto di
  `aria-hidden`). Il tag passa dal registro: un alias V4 disegna il simbolo V5; un nome vuoto non disegna nulla.
  Colore = `currentcolor`; **nessun esadecimale letterale dentro `static/img/`** (§14.1 per le illustrazioni).
- **Decorativa per default**: accanto a un testo l'icona è nascosta alle tecnologie assistive; un controllo con la
  sola icona deve avere testo `.visually-hidden` o `aria-label`. Mai il colore da solo: il colore della chip e la
  parola portano lo stato, il cerchio lo rende riconoscibile.
- **Colori forzati**: un'icona è l'inchiostro del testo che ha accanto. Il browser dà a `<svg>`
  `forced-color-adjust: preserve-parent-color`, che segue la tavolozza di sistema solo finché il `color` dell'svg è
  ereditato: un componente che colora il suo glifo gli lasciava l'esadecimale d'autore (frecce navy a 1.4:1 su una
  tela scura, l'inchiostro notturno del piede a 1.8:1 su una chiara). Sotto `forced-colors: active` la regola `.icon`
  rieredita (`color: inherit !important`) e non dipinge un fondo proprio (`background: none !important`):
  `CanvasText` nel testo, `LinkText` in un link, `ButtonText` in un pulsante — 502 icone su 26 celle, 0 fuori
  tavolozza, 0 sotto 3:1 (DL54-34).
- **Stato vuoto**: il glifo dice QUALE spazio è vuoto. Una pagina vuota porta il glifo di concetto del suo dominio
  (FAQ `circle-help`, glossario `book-a`, attualità `newspaper`, Forum `handshake`, «Vivre en Italie» `sprout`, una
  lista della console il proprio); una regione sotto il proprio titolo, e una pagina il cui dominio non ha un glifo
  nel registro, portano `empty` — una cornice tratteggiata, il segno neutro «qui non c'è ancora nulla» (`EMPTY_STATE`).
  Mai `document` per difetto: è il glifo di «Mes pièces» (DL54-33).
- **Direzionalità — la lista chiusa** (`FLIP_RTL`): `arrow`, `arrow-start`, `chevron-end`, `logout`, `send`,
  `signpost`, `panel-left-close` ricevono `.icon--flip-rtl` dal tag stesso (`transform: scaleX(-1)` sotto
  `[dir="rtl"]`) e nessun altro simbolo lo porta. Non si specchiano: il marchio e i suoi glifi (`ile-steps`
  compreso: la scala sale come i gradini della scena), gli stati, i pubblici, `chevron` (giù), `arrow-up-right`,
  `history`, `refresh-cw`, `list-ordered`, `split` e ogni icona non direzionale.
- **Densità** (.italia): al massimo **sei icone nel corpo editoriale di una pagina pubblica**; il chrome è esente.
  Una colonna di glifi è tutto o niente. Una riga porta un glifo solo quando dice qualcosa (uno stato, un attore).
  Mai un'icona come punto elenco. Sempre accoppiata a un'etichetta di testo, o con l'etichetta disponibile alle
  tecnologie assistive.
- **Colore**: `.icon--accent` eredita la rubrica (6.92:1 sulla carta): va riesaminato caso per caso, perché un'icona
  non è una posizione in una sequenza e l'unico compito della rubrica è l'ORDINE (§4.1).
- **Test**: `tests/frontend/test_icons.py` (registro = sprite, origini delle sorgenti, soglie, gemelli, lista di
  flip, atti di spunta, attualità della build, nessuna libreria), `test_svg_wellformed.py`,
  `test_static_assets.py`, `test_design_docs.py` (questo elenco), `tests/i18n/test_page_integrity.py` (lo specchio in
  arabo), `tests/i18n/test_rtl_browser.py`, `tests/frontend/test_browser_w1_b.py` (le rail, lo stato vuoto e i colori
  forzati, nel browser).

Elenco completo degli `id` dello sprite (`static/img/icons.svg`, prefisso `icon-`):

<!-- icon-list:start -->
113 icone.

110 simboli V5 e 3 alias V4, nell'ordine dello sprite (generato da `scripts/build_icons.py` dal registro `apps/core/icons.py`).

| Gruppo | Icone |
|---|---|
| Identità — dal marchio | `ile-arch`, `ile-key`, `ile-steps`, `ile-mark` |
| Stati — «i cerchi» | `st-attesa`, `st-attesa-replace`, `st-neutro`, `st-esame`, `st-conforme`, `st-azione`, `st-rifiuto`, `st-nullo` |
| Pubblici e soggetti | `person`, `building`, `institution`, `university`, `briefcase`, `stamp`, `badge-dot`, `badge-check`, `circle-user-round` |
| Domini della piattaforma | `layout-dashboard`, `compass`, `signpost`, `folder`, `document`, `send`, `calendar-clock`, `mail`, `concierge-bell`, `inbox`, `book-open`, `list-ordered`, `wrench`, `map`, `handshake`, `calendar-range`, `table`, `file-plus`, `sprout`, `settings`, `bell`, `shield`, `award` |
| Il percorso | `scroll-text`, `clipboard-list`, `building-2` |
| Selezione e vie regolari | `pen-line`, `factory`, `id-card`, `users`, `store`, `flask-conical`, `split` |
| Vivere in Italia | `languages`, `house`, `heart-pulse`, `stethoscope`, `school`, `vote`, `scale`, `hard-hat`, `receipt` |
| Contatti e pagine pubbliche | `at-sign`, `phone`, `map-pin`, `shield-alert`, `megaphone`, `book-a`, `circle-help`, `newspaper`, `hash`, `history`, `quote` |
| Azioni e direzione | `upload`, `refresh-cw`, `download`, `eye`, `eye-off`, `trash-2`, `plus`, `minus`, `pencil`, `copy`, `mail-open`, `list-filter`, `arrow-down-up`, `printer`, `search`, `arrow`, `arrow-start`, `arrow-up-right`, `chevron`, `chevron-end`, `close`, `check`, `menu`, `ellipsis-vertical`, `panel-left-close`, `logout`, `lock` |
| Avvisi e tempo | `info`, `warning`, `circle-alert`, `clock`, `circle-pause`, `circle-check`, `calendar`, `alarm-clock`, `empty` |
| Alias V4 — fino allo sweep dei loro produttori: ciascuno disegna il simbolo V5 del suo uso residuo (`apps/core/icons.py`, `LEGACY`) | `home`, `list`, `globe` |
<!-- icon-list:end -->

> **G-01 (chiusa il 20/09/2026).** Lo sprite non era XML ben formato: il commento iniziale conteneva
> la sequenza `--` (nel nome della classe `.icon--flip-rtl`), vietata dentro un commento XML. Il
> browser scaricava il file (HTTP 200, `image/svg+xml`) ma non lo interpretava e **nessuna icona
> veniva disegnata su nessuna pagina**. L'owner ha riformulato il commento; verifica in Chromium:
> `DOMParser` senza `parsererror` e, nel report `docs/qa/design/capture-report.json`, **865 icone disposte**
> sulle 43 catture, 0 vuote (`emptyIcons`). Regressione impedita da
> `tests/frontend/test_design_docs.py::test_icon_sprite_is_well_formed_xml`, da
> `tests/frontend/test_svg_wellformed.py::test_svg_is_wellformed_xml` (ogni SVG sotto `static/`) e da
> `docs/qa/design/capture.py`, che esce con codice 1 se un'icona disposta non disegna nulla.

---

## 14. Illustrazioni e fotografia

### 14.1 Illustrazioni (`static/img/illustrations/`)

Cinque SVG originali al tratto, ereditati dal sistema ritirato (il sesto, `pilot-flow` — una curva di crescita
col nodo finale d'oro —, è stato ritirato l'11 ottobre 2026 da W3-F1: la pagina del progetto pilota disegna la
sequenza su «la linea»). **Tutti e cinque sono da ritirare o da ridisegnare**, e i loro colori sono la prova: tratto `#0f2b52`, accenti `#9a7b2f` (bronzo) e
`#1f6b48` (verde), nodi in `#fbfaf7`. Il bronzo non esiste più; il verde è riservato all'asse
marocchino e non può marcare il nodo finale di una sequenza; il navy e la carta sono cambiati di
qualche punto. I colori sono scritti dentro i file SVG (sono immagini, non CSS), quindi non seguono i
token: vanno aggiornati a mano o i file vanno cancellati.

| File | viewBox | Soggetto | Destino |
|---|---|---|---|
| `entrance-person.svg` | 160 × 120 | figura e percorso a tappe | ritirare: le quattro entrate diventano un registro di righe (§8.4) |
| `entrance-company.svg` | 160 × 120 | edifici e lista di fabbisogni | ritirare |
| `entrance-institution.svg` | 160 × 120 | portico generico (nessun emblema) e due archi di dialogo | ritirare: compare identico sei volte in una lista di sei voci della pagina Istituzioni |
| `entrance-university.svg` | 160 × 120 | libro aperto e tocco accademico | ritirare |
| `orientation.svg` | 240 × 160 | domande, ramificazione, bussola | ridisegnare sui colori del sistema o ritirare |

`favicon.svg` segue la stessa regola ed è da rifare sul marchio del folio (§8.1); `og-default.png`
(1200 × 630) è l'immagine di condivisione.

### 14.2 Fotografia

Registro, licenze e pipeline: `docs/IMAGE_LICENSES.md`, che **sopravvive intatto alla redirezione**.
La sua lista di soggetti vietati (niente porte, frontiere, valigie, file, passaporti, aeroporti,
soglie, cancelli; nessuna iconografia stereotipata della migrazione; nessun cliché turistico) e il
suo §4, con il registro di tredici candidati rifiutati *e la ragione di ciascuno*, sono l'artefatto
più forte dell'area e restano come sono.

Ciò che la direzione A cambia è quanto segue.

- **Un'immagine compare solo dove documenta qualcosa di specifico.** Non «la pagina imprese ha
  bisogno di una foto», ma *«questa è la Sala della Gran Guardia, Rovigo, 2 ottobre 2026»*.
- **Al massimo una fotografia per pagina**, ed è sempre una **lastra**: a pieno vivo, nessun raggio,
  nessuna ombra, nessuna cornice, nessun contorno sfalsato, nessun bordo. O è la sezione di rango A
  della pagina, o non esiste. Non c'è un mezzo difendibile a 484 px: l'hero respinto era un
  francobollo di 484 × 363 (l'11 % di un viewport da 1440, il 4 % della sua area) dietro un contorno
  bronzo sfalsato che sbordava di 22 px su due lati e si leggeva come un errore di registro di stampa.
- **Il contratto della didascalia.** Nessuna immagine è resa senza didascalia; quattro campi
  obbligatori, imposti dal template: *luogo — data — una frase di fatto — credito*. Una `<figure>`
  senza `<figcaption>` è un **errore di build**. Oggi il sito pubblico ha sei `<figure>` e **zero**
  `<figcaption>`, mentre `figcaption` è pienamente stilato in `base.css` e non è usato da nessuno.
  Questa sola regola uccide la libreria di repertorio, perché non c'è nulla di vero da scrivere sotto
  la fotografia di persone sconosciute attorno a un tavolo in una città senza nome.
- **Due rapporti, nessun altro**: `2 / 1` per la lastra di banda (territorio, sede, architettura,
  un convegno), `3 / 2` per la lastra di documento (il rapporto nativo della libreria delle fonti,
  così non avviene alcun ritaglio). `object-position` va memorizzato **per asset** nel manifest,
  accanto al campo `crop` esistente, così il soggetto resta tenuto sotto il ritaglio e il rapporto di
  un contenitore non decide mai che cosa mostra una fotografia.
- **Due categorie di soggetto, e una terza vietata**: TERRITORIO (Rovigo, il Polesine, il tessuto
  industriale veneto; porti, istituti di formazione e architettura civile marocchini) e DOCUMENTO
  (registri, carta bollata, scaffalature d'archivio, moduli, firme, sigilli). Mai: persone al
  portatile, riunioni attorno a legno di recupero, muri di post-it, studenti che ridono,
  «collaborazione», «lavoro di squadra», «spazio di lavoro».
- **Il sito parte con zero fotografie**, fino a che non esiste il reportage del Forum del 2 ottobre
  2026. Un sito senza immagini si legge sobrio; un sito con sei immagini di repertorio
  intercambiabili si legge come un template, che è il verdetto già emesso. È possibile perché la
  pagina è retta dal linguaggio grafico di §8, non dalle immagini: la sezione di rango A della home è
  una **lastra tipografica**, non fotografica. Lo slot della lastra esiste comunque; cambia solo il
  suo riempimento.
- **Tecnica** (invariata): derivati WebP a 480 / 960 / 1440 / 1920 px (mai upscaling) + JPEG 1440 px
  di fallback, ciascuno ≤ 350 KB, metadati rimossi; `<picture>` con `<source type="image/webp"
  srcset>` e `<img>` con `width`/`height` espliciti, `loading="lazy"` sotto la piega,
  `decoding="async"`. Mai un host esterno (CSP `img-src 'self' data:`).
- **Testo alternativo**: `MediaAsset.alt(lang)`; la sorgente è `alt_fr`, le altre lingue restano vuote
  finché non arrivano dai traduttori (mai traduzione automatica) — in quel caso l'alt francese va
  marcato con `lang="fr"`. Immagini puramente decorative: `alt=""`. **Nessun testo è mai sovrapposto
  a una foto** (il contrasto non è garantibile).

---

## 15. RTL e arabo

**L'ingegneria RTL della build precedente è eccellente e si conserva per intero**: zero overflow
orizzontale su 50 misurazioni, proprietà logiche ovunque, barre di avanzamento specchiate, tabelle
specchiate, marcatori di disclosure specchiati. Ciò che si rifà è il **prodotto arabo**: nel sistema
ritirato il design arabo consisteva in uno scambio di font e otto regole che tolgono cose.

### 15.1 Tipografia araba

L'arabo è **progettato, non tradotto**. Il blocco `:root:lang(ar), :root[dir="rtl"]` di `tokens.css`
gli dà una coppia display/testo propria, come il latino ce l'ha: `--font-display-ar` (Noto Naskh
Arabic, un vero Naskh, il registro dei documenti amministrativi marocchini) e `--font-ui-ar` (IBM
Plex Sans Arabic, dove una costruzione kufica è corretta). Nel sistema ritirato Plex Sans Arabic
faceva **tutti e sei** i livelli, quindi l'edizione araba non aveva alcun contrasto display/testo.

**L'interlinea si apre, le dimensioni non si riducono**: `--t-prose-lh` passa da 28 a 32 px,
`--t-gloss-lh` da 24 a 28, `--t-entry-lh` da 28 a 32. La giustificazione è misurata: al vecchio
impianto dell'H2 (33.76 px / interlinea 38.82 px) due righe consecutive di arabo vocalizzato
producevano rettangoli di glifo che **si sovrapponevano di 12.2 px**, con 51 px d'inchiostro dentro
una riga da 38.8 px; a corpo 16 px l'arabo riceveva 1.6 px di interlinea totale contro gli 8 px del
latino.

**Ogni tracking è azzerato a livello di token** — `--track-folio` e `--track-caps-display` vanno a 0 —
e non con una lista di regole per componente. È una garanzia più stretta: nel sistema ritirato
`base.css` applicava `letter-spacing: -0.01em` a `h1`–`h6` senza condizioni e il blocco `:lang(ar)`
azzerava soltanto `--tracking-eyebrow` e `--tracking-button`, quindi **ogni titolo arabo portava un
tracking negativo** (misurato: −0.48 px sull'H1, −0.34 px sull'H2), esattamente la cosa che spezza le
legature. Il test giusto è statico: *nessun `letter-spacing` diverso da zero deve essere raggiungibile
sotto `:lang(ar)`*.

`font-synthesis: none` è globale e rende visibile, invece che sbavato, un peso mancante. **Il peso
700 è vietato in arabo** sull'interfaccia, dove sono sottoinsiemati solo 400/500/600.

### 15.2 Il registro senza cassa

L'arabo non ha maiuscole, quindi il registro che in latino è portato dal maiuscolo tracciato è
portato qui da **peso 600 più un filetto rubrica da 2 px sul bordo d'attacco**, a 15 px.
`base.css` toglie maiuscolo e tracking a `h4, h5, h6, .t-folio` sotto `:lang(ar)`; lo shim fa lo
stesso per `.eyebrow`. Questa è un'**aggiunta** per l'arabo, non una sottrazione.

### 15.3 Specchiatura sotto questa direzione

1. **Direzione dal server**: `<html lang="ar" dir="rtl">` e `body.is-rtl`
   (`core.context_processors.site`).
2. **Solo proprietà logiche**: `margin-inline-*`, `padding-inline-*`, `inset-inline-*`,
   `border-inline-*`, `inline-size` / `block-size`, `text-align: start | end`. Non esiste un solo
   `left` / `right` fisico in `base.css` e `layout.css`; in `components.css` compaiono unicamente
   nella posizione dello chevron del `<select>`.
3. **Il rail si specchia sul bordo di chiusura**, il margine sul bordo d'attacco; il canale vuoto si
   specchia con loro. `layout.css` lo ottiene senza una sola regola `[dir="rtl"]`, perché le tre zone
   sono una griglia e il `padding-inline-start` del margine è logico.
4. **Gli ordinali del folio restano in cifre occidentali** (corretto per il Marocco) e vanno avvolti
   in `<bdi>`.
5. **Dati latini dentro una pagina araba**: `direction: ltr; unicode-bidi: isolate` per `.ltr`,
   `.brand__wordmark`, `.email`, `.phone`, `code`, `time[datetime]` e per gli input `email`, `tel`,
   `url`, `number`, `password` (questi ultimi con `text-align: end`).
6. **Le frecce sono CSS o SVG e si specchiano con `.icon--flip-rtl`.** Nessun `→` dentro una stringa
   traducibile: oggi le frasi prescritte francesi conservano frecce verso destra su una pagina dove
   ogni freccia araba punta a sinistra.
7. **Tastiera**: frecce ←/→ invertite nel mega-menu e nelle tab (`document.documentElement.dir`).
8. **Verifica**: `tests/frontend/test_browser.py::test_no_horizontal_overflow_and_screenshots`,
   `tests/compliance/test_public_pages.py::test_arabic_is_rtl_and_others_ltr`,
   `tests/frontend/test_layout.py::test_login_page_in_arabic_is_rtl`; screenshot
   `docs/qa/design/home-ar-390.png`, `docs/qa/design/home-ar-768.png`,
   `docs/qa/design/home-ar-1440.png`, `docs/qa/design/login-ar-1440.png`,
   `docs/qa/design/privacy-ar-768.png`, `docs/qa/design/404-ar-768.png`.

### 15.4 Il francese prescritto è un oggetto progettato, non una perdita

Cento testi prescritti esistono solo in francese (ADR-004). Il risultato misurato è che una pagina
araba tipica è al **44 %** in arabo, `/ar/forum/` all'**1.1 %**, e che aprire la Fase 3 farebbe
scendere la home araba dal **73.5 % al 17.9 %**.

La direzione introduce un componente di prima classe, `.prescribed`, che è **l'unico** modo in cui
del francese bloccato viene mai reso: filetto rubrica da 4 px sul bordo d'attacco, fondo
`--paper-deep`, una fascia a tutta larghezza (così non condivide mai una riga, una cella di griglia o
un confronto a due colonne con del testo arabo), un'etichetta araba che dichiara che il testo è
francese e che la versione araba è in preparazione, una **sintesi araba di 2–3 righe scritta dai
redattori** — esplicitamente *non* una traduzione del testo bloccato, così il test sul contenuto
prescritto continua a passare — e infine l'isola LTR con le facce latine restituite
(`[lang="fr"] { --font-display: Newsreader; }`), così il francese prescritto sembra il disegno
francese e non uno straniero.

L'isolamento bidi va su un `<bdi>` interno, **non sul blocco**. È il difetto visibile peggiore della
build araba: `base.css` imposta `direction: ltr` sul *blocco*, quindi `text-align: start` risolve a
**sinistra** e ogni blocco di fallback finisce sul margine opposto. Misurato: un hero del Forum le cui
due righe cominciano a 1136 px di distanza su bordi opposti; righe di percorso con ~760 px di spazio
vuoto fra l'ordinale e il titolo, otto volte.

### 15.5 Difetto aperto G-03

Le stringhe d'identità in caratteri latini che non portano `.brand__wordmark` (wordmark del footer,
nome del promotore nella barra e nel footer, riga del ©) non sono isolate: in arabo il footer mostra
«™Italy Legal Entry» e la barra tronca l'inizio del nome del promotore
(`docs/qa/design/a11y-zoom400-ar-320.png`). La direzione aggiunge una regola che risolve la causa a
monte: `text-overflow: ellipsis` è **vietato** su testo d'identità, giuridico e di navigazione, e il
promotore va a capo su due righe sotto `md` invece di essere tagliato.

`docs/I18N_RTL.md` esiste e resta il riferimento per traduzioni e procedure RTL; qui restano le sole
regole di disegno.

---

## 16. Moduli JS e progressive enhancement

Tre file senza bundler (più i bundle esbuild di `static/js/src/`), ≈ 17.4 KB non compressi in totale.

| File | Caricamento | Ruolo |
|---|---|---|
| `static/js/head.js` | `<script src>` sincrono in `<head>` | una riga: sostituisce `no-js` con `js` su `<html>` prima del primo paint. È un file esterno perché la CSP è `script-src 'self'` senza nonce |
| `static/js/rail-pref.js` | `<script src>` sincrono in testa al `<body>` della console (`portal/base_portal.html`) | una funzione: scrive l'attributo data-rail sul body («open» o «closed») prima che la rail sia analizzata — la scelta ricordata (chiave ile.rail di localStorage), altrimenti aperta da 80rem e compatta sotto — così lo stato non sposta il workspace dopo il primo frame (CLS fino a 1,19 misurato dalla revisione del gate C). Senza questo script il foglio tiene la rail aperta (§11.6). File esterno e classico, non nel bundle: la CSP vieta lo script in linea e un modulo sarebbe differito |
| `static/js/main.js` | `<script type="module">` a fine `<body>` | modulo ES senza `import`; esporta `init`; ogni comportamento si aggancia a un attributo `data-*`; nessun testo nel JS (tutte le stringhe restano nell'HTML tradotto dal server) |
| `static/js/src/entrance.js` | `<script type="module">` dal layout dell'ingresso (`templates/allauth/layouts/entrance.html`; bundle `static/js/dist/entrance.js`) | il palcoscenico che risponde alla persona (piano V5.4 §1.13, W2-B): legge dove si trova la persona e che cosa contiene il modulo — il focus sul campo e-mail, un indirizzo valido (letto alla pausa di battitura, `--motion-wait`; subito se il campo è svuotato o lasciato), la password o il codice — e scrive lo stato come classi sull'elemento `data-varco-stage` (`is-ways`, `is-held`, `is-frame`); chiede un solo passaggio di luce quando il focus viene da un puntatore, mai dalla tastiera né sotto il moto ridotto (il cancello di `motion.js`); dice la frase d'arrivo una volta, dopo il dipinto della porta, e mai dopo un accesso rifiutato, da un'altra pagina d'ingresso, dalla cronologia o sulla fascia. Solo classi, scritte quando cambiano: nessuno stile, nessun `animate()`, nessun testo. Senza JS il palcoscenico è completo e fermo; il giro della chiave all'invio è di `loader.js` |
| `static/js/src/loader.js` | importato da `shell.js` al primo invio di un form, mai prima (`import()` dinamico; bundle `static/js/dist/loader.js`) | la macchina a stati del loader «Lume» (piano V5.4 §1.9, W1-D): `busy()` / `settle()` / `rest()` per la chiave occupata (L2), `engage()` con le parole a 1 s e a 10 s e «Réessayer», `release()` di un host in pagina, `seat()` per le righe di un frammento al primo arrivo (L3); `OUTCOME_BEARING` (ricalcolo della situazione, pre-valutazione, eleggibilità, verifica di scansione) non riceve mai L1; `aria-disabled`, mai `disabled`, e solo dove `main.js` rifiuta davvero il secondo invio (`data-single-submit`); «Réessayer» riporta il fuoco sul controllo d'invio prima di nascondersi. **Nessuna attesa è per sempre**: un'attesa è un prestito di 10 s (`SLOW_AFTER`, il momento in cui «Réessayer» è offerto), più il tempo che i file del form chiedono a 16 KiB/s; alla scadenza il form torna a riposo da solo e si può inviare di nuovo — salvo dove un host offre «Réessayer», che lascia la scelta alla persona. Un invio annullato da un listener che gira dopo lo hook (una risposta data in pagina) è a riposo nel task seguente; una pagina che torna dalla cache è a riposo (`pageshow`). Un controllo occupato si riconosce dal suo `aria-busy`, non dalla sua faccia. `shell.js` mette `aria-busy` solo su un controllo `.btn`, la classe `.is-busy` — la chiave — solo dove ha posto (non sui bottoni-link né su `.btn--icon`: l'elenco `KEYLESS`), e salta, senza importare il modulo, un form `data-loader="none"` — la cui risposta è un file —, un form che si apre altrove (`target`) o che chiude un dialog. Nessuna stringa: le parole le porta il template che include |

Inventario di `main.js` (funzioni chiamate da `init()`):

| Funzione | Hook | Cosa aggiunge | Cosa funziona comunque senza JS |
|---|---|---|---|
| `initFormErrorFocus` | `#form-errors` | dopo un invio non valido porta il focus sul riepilogo degli errori e lo scorre al centro del viewport, senza animazione a movimento ridotto | il riepilogo è comunque in cima al form, con `role="alert"` e un link per ogni campo in errore |
| *(la navigazione pubblica non è più qui: `initNavigation` è in `static/js/src/nav.js`, sotto)* | | | |
| *(i `<details data-dropdown>` non sono più qui: `initDropdowns` è uscita quando ogni pagina ha caricato `overlay.js`, che li tiene — W2-C2)* | | | |
| `initAccordions` | `data-accordion` | esclusività per i browser senza `<details name>`; un link a una riga (`#id` di un `details.accordion__item`) la apre, all'arrivo e a ogni `hashchange` | accordion pienamente funzionante (più pannelli aperti insieme); il permalink porta alla domanda chiusa |
| `initTabs` | `data-tabs` | tab ARIA ad attivazione automatica, roving tabindex, frecce (invertite in RTL) / Home / Fine, apertura da `#hash`; misura l'etichetta scelta e scrive `--tabs-x`, `--tabs-y`, `--tabs-w`, `--tabs-dir` sul widget — l'unico indicatore, che `v5/tabs.css` muove con `transform` (`.is-travelling` solo per una scelta del puntatore) e che un `ResizeObserver` tiene al suo posto | pannelli impilati con il proprio titolo; tablist nascosta |
| `initSteppers` | `data-stepper`, `data-step`, `data-step-marker`, `data-step-next`, `data-step-prev`, `data-step-current`, `data-step-focus` | pannelli lato client, `aria-current="step"`, focus sul titolo del passo | tutti i passi visibili in sequenza |
| `initReveal` | `.reveal`, `.reveal--stagger` | comparsa allo scroll — **da cancellare** (§12): nulla si muove allo scroll in questa direzione | contenuto sempre visibile |
| `initCounters` | `data-counter`, `data-counter-format` | conteggio animato — **da cancellare** (§12): zero usi, e «contatori da startup» è un anti-pattern dichiarato | valore statico nell'HTML |
| `initMisc` | `data-history-back`, `data-single-submit`, `data-section-nav` | «pagina precedente», blocco del doppio invio (W1-D: `aria-disabled`, mai `disabled` — il focus resta; il form è marcato `data-submitted` finché la risposta non sostituisce la pagina o l'attesa non finisce: `loader.js` toglie il segno a «Réessayer», alla scadenza dei 10 s e quando la risposta è data in pagina, `pageshow` lo toglie al ritorno dalla cache; la chiave occupata di L2 la mette `shell.js`), `aria-current` sul sommario di pagina | il link «indietro» è `.js-only`; il form si invia normalmente |

**`static/js/src/nav.js` — «Il portico»** (W2-C1, W2-C2): `initNavigation` è uscita da `main.js` ed è importata
dall'unico ingresso pubblico `static/js/src/shell.js`, distribuito in `static/js/dist/` (§2.1), che importa anche
`overlay.js` (W2-C2: il foglio, il popover della targa, il tooltip della chiave). Tre parti: lo
stato scrollato della testata (un `IntersectionObserver` su una sentinella di 24 px, nessun listener di scroll);
la barra e i pannelli — hook `data-portico`, `data-portico-door`, `data-portico-panel`,
`data-portico-architrave`, `data-portico-scrim`, `data-portico-photo` (§11.1) — con l'intenzione del puntatore,
il triangolo sicuro, il modello tastiera, l'architrave, la misura di `--portico-lead` e `--portico-h`, lo scrim e
il prefetch a idle delle fotografie (le porte misurate lasciano lo schermo subito: la transizione discreta del loro
`display` le teneva 120 ms, abbastanza perché il browser chiedesse le fotografie pigre, Save-Data o no — N8, W2-C2);
il foglio (§11.2) — `initSheet`: lo chiude una finestra allargata oltre 80rem; tutto il resto è di `overlay.js`. Lo
scrim, la chiusura leggera, Esc e il ritorno del fuoco del pannello sono ancora di `nav.js`: il contratto degli overlay
non ha un primitivo per una regione di disclosure (chiesto a W2-A, `docs/design-v5/QA/v54/w2-c2/NOTES.md`). Senza
script: le porte si aprono su hover e `:focus-within`, il foglio si mostra sul posto (`:target`), tutti i link sono
raggiungibili.

**`static/js/src/console.js` — la cromatura della console** (W3-A, §11.6; bundle `static/js/dist/console.js`,
caricato da `portal/base_portal.html`): lo stato della rail — `data-rail` sul body, il controllo
`data-rail-toggle` con il suo `aria-expanded`, la scelta scritta a ogni pressione e la larghezza seguita finché
nessuna scelta è ricordata —; la pagina corrente tenuta in vista nella lista (`data-rail-scroll`) quando lo
schermo è corto; la parola di un glifo che sta da solo (`data-rail-tip`: sulla riga del controllo, oltre il bordo
della rail, al passaggio e al fuoco della tastiera; via con Esc — il tooltip del livello superiore del sistema degli
overlay, a cui la rail dice quali controlli e quando); le frecce tra le voci (`data-rail-item`); il cassetto dei
telefoni (`data-console-drawer`) e il popover del conto, del sistema degli overlay che il modulo importa
(`overlay.js`, qui sotto): «Menu» e il controllo di chiusura sono collegamenti (`data-overlay-open`,
`data-overlay-close`) che il sistema fa bottoni, il cassetto è un drawer modale col fuoco di ritorno a «Menu»; una finestra allargata oltre 64rem
chiude il cassetto e il popover del conto, il fuoco alla rail. L'unica attesa di
frame — la transizione della larghezza parte solo dopo il primo frame — passa da `motion.js`. Senza script: la
rail è aperta, le parole sono accanto ai glifi, il menu della lingua è un `<details>` e, sotto 64rem, «Menu»
porta al cassetto che il foglio mostra (`:target`).

**`static/js/src/overlay.js` — il sistema degli overlay** (W2-A; piano V5.4 §1.14; il contratto
`docs/design-v5/QA/v54/w2-a/CONTRACT.md`; bundle `static/js/dist/overlay.js`, importato da `console.js` e — W2-C2 —
da `shell.js`, che lo portano sulle loro pagine): un solo modulo per il dialog e l'alertdialog, il drawer, lo sheet,
il popover / menu e il tooltip del livello superiore, sugli elementi nativi — il `<dialog>` e il suo `cancel`, le
richieste di chiusura (`closedby`), l'API popover, `beforetoggle` e `toggle`. **La regola INP del piano è scattata**:
`showModal()` rende inerte tutta la pagina e la ristila intera (≈ 860 elementi sull'arabo «Mes documents», ≈ 1 000
sulla home della fase 3, a CPU × 4), quindi un tipo modale si apre con `show()`, `aria-modal="true"` e l'unico scrim
(`.overlay-scrim`, fatto a riposo), con la trappola in script — Tab che gira e un fuoco riportato dentro — e il resto
della pagina `aria-hidden` finché il pannello è aperto (un motore non pota nulla per il solo `aria-modal`; mai `inert`,
che ristila ogni elemento, e nessuna regola del progetto seleziona `aria-hidden`); `data-overlay-modal`="native" tiene
`showModal()`. Esporta `open(pannello, {opener, focus, instant, history})`,
`close(pannello, {reason, focus, instant})`, `toggle`, `isOpen` e `initOverlays(radice)` (idempotente: dopo aver
inserito del markup) e annuncia `overlay:open` / `overlay:close` sul pannello. Aggiunge ciò che la piattaforma non dà:
lo stato e il fuoco nel compito dell'input, portato nella vista del pannello aperto (la pagina non scorre mai); il
fuoco di ritorno all'apritore o al suo successore (`data-overlay-return`); Tab che gira dentro un pannello modale; lo
scrim (`data-overlay-dirty` lo ferma quando un campo è stato scritto), che sta anche sotto un menu mostrato come sheet
sul telefono e tiene tutta la pressione, dalla discesa al clic (`data-held`), «Fermer» (`data-overlay-close`), un link in un drawer, una scelta in un menu, il fuoco che
lascia un menu, la maniglia di uno sheet (`data-overlay-grip`, `data-overlay-dragging`), Indietro
(`data-overlay-history`) ed Esc per il drawer non modale (`data-overlay-modal`); la risposta sicura di un alertdialog
(`data-overlay-safe`); il blocco dello scroll con la gronda della barra (`data-overlay-lock`); il lato di un menu
scelto prima dell'apertura (`data-overlay-side`, misurato a riposo su cloni inerti, `data-overlay-measure`),
l'ancora, e senza posizionamento ad ancora il posto calcolato con gli stessi ribaltamenti (`data-overlay-phone` lo
lascia ancorato sul telefono); il pannello che esce reso `inert`; Esc e la pressione che tolgono un tooltip
(`data-tip-off`) e l'unico tooltip del livello superiore per un controllo `data-tip`="layer" (`data-tip-side`; le
parole di `data-tip-label`, il posto oltre l'antenato di `data-tip-beyond`, che segue uno scroll finché il controllo
tiene il fuoco o il puntatore, il rifiuto di una pagina con `overlay:tip`, annullabile); i menu che sono ancora un `<details data-dropdown>` (la lingua della rail): uno aperto
per volta, `aria-expanded` sul `summary`, Esc, il clic fuori e la perdita di fuoco li chiudono, e uno aperto prende
l'Esc prima del pannello in cui sta — la lista delle lingue prima del cassetto.
Apritori: `data-overlay-open` su un link `href="#id"` — che diventa bottone, con Spazio, `aria-expanded`,
`aria-controls`, `aria-haspopup` — o su un bottone; un menu col suo `popovertarget`. Scrive solo proprietà CSSOM
(`left`, `top`, `translate`, i nomi dell'ancora, `--overlay-drag`), nessun attributo `style`, nessuna stringa; non
attende mai una transizione; non anima nulla — il moto è del foglio (§12). Senza script: un apritore `href="#id"`
mostra il suo pannello al suo posto (`:target`), subito, un menu si apre comunque, un tooltip appare comunque al
passaggio e al focus. Lo caricano `console.js` (ogni pagina della console) e la vetrina di sviluppo; W2-C2 lo
aggiunge a `shell.js`. **Le parti rare** — la maniglia di uno sheet, Indietro, il posto senza posizionamento ad
ancora, il corpo di un dialog che scorre reso fermata, la pressione sul `::backdrop` di un modale nativo — stanno in
`static/js/src/overlay/extras.js`, importato a richiesta (a riposo dove una pagina ne disegna una, subito dove il
motore non ha il posizionamento ad ancora): nessuna pagina della console lo scarica (piano §2.6; DL54-93).

`main.js` non usa `localStorage`: l'opzione `remember` delle schede, che scriveva la scelta senza rileggerla
(G-21), è stata tolta con design V5 (W1-C). L'unica chiave del sito è `ile.rail` — «open» o «closed», scritta
da `console.js` a ogni pressione del controllo della rail e letta da `rail-pref.js`, qui sopra —: nessun dato
personale, nessun identificatore; è memoria tecnica, non un cookie di tracciamento.
Fuori da `static/js/`, gli script delle app sono elencati in §2.1.

Ciò che il JavaScript **non** fa, e non deve fare: scrivere geometria su un elemento di cui hanno
bisogno anche i suoi fratelli (§11.5), nascondere contenuto in attesa di un observer (§12), o
contenere una stringa visibile all'utente.

Verifica senza JS: `docs/qa/design/a11y-nojs-fr-390.png`, `docs/qa/design/a11y-nojs-fr-1024.png` e
`docs/qa/design/a11y-nojs-fr-1440.png` (Playwright con `java_script_enabled=False`), più
`tests/frontend/test_static_assets.py::test_main_js_is_an_es_module_without_external_dependencies`.

---

## 17. Lo shim legacy e il conto alla rovescia

`static/css/_legacy-tokens.css` **non fa parte del design system**. È un'impalcatura di demolizione,
dichiarata come tale nel suo stesso intestazione, e la sua unica proprietà interessante è che
**accorcia soltanto**.

Perché esiste. La direzione A ha sostituito l'intero insieme dei token; 169 template e ~6 000 righe
di CSS fanno ancora riferimento ai nomi vecchi. Sostituire entrambi in un solo commit vorrebbe dire
una modifica non revisionabile e un sito rotto per tutta la durata del refactoring. I nomi vecchi
vivono quindi qui, **mappati sul nuovo sistema**, e vengono rimossi file per file man mano che ogni
foglio viene migrato. L'effetto immediato è che la resa è già quella nuova — il bronzo è rubrica, le
ombre sono `none`, i raggi sono 2 px, il verde di successo è blu — mentre il markup è ancora quello
vecchio. È la mitigazione del rischio che il Council ha classificato come **critico**: «una versione
a metà sembra peggio di quella di oggi», e la risposta è sequenziare per *sistema* e mai per pagina.

**Design V5 (5 ottobre 2026, W1-A).** Ogni riga qui sotto è il valore che **lo shim dichiara**. La resa è quella della
cascata effettiva: dove uno strato successivo ridichiara un nome, vince quello strato — oggi due nomi, `--radius-pill`
(pieno, 999 px, già da V4) e `--font-mono` (ILE Mono), ridichiarati in `static/css/v5/aliases.css`. Undici nomi sono
usciti dallo shim perché V5 li adotta con i suoi valori: `--radius-xs`, `--radius-sm`, `--radius-md` (2 · 4 · 6, §7.5),
`--control-height` e `--control-height-sm` (44 e 36), i cinque nomi del fuoco (§7.5) e `--z-modal` (50); i tetti di
`tests/frontend/test_legacy_token_shim.py` si sono abbassati con loro.

**142 nomi** e 14 classi sono oggi nello shim. Ogni riga è un debito con un sostituto nominato, e
il conto alla rovescia è tenuto da due file. `tests/frontend/test_legacy_token_shim.py` tiene i
**tetti** — 142 token, 14 classi e 1 515 usi complessivi dei nomi ritirati in `static/css/`, nei
fogli delle app e nei template — più la regola che nessun file scritto dopo la redirezione parli
la lingua vecchia; sono massimi, non obiettivi, e si abbassano nel commit stesso in cui una
migrazione toglie delle voci. Il test
`tests/frontend/test_design_docs.py::test_every_legacy_shim_token_is_documented_with_its_replacement`
tiene la metà documentale: ogni nome del file compare qui con il valore esatto a cui risolve,
nessuna riga qui documenta un nome che il file non dichiara più, e il numero scritto sopra è
quello che il tetto registra. Il conto alla rovescia è quindi visibile e non può scivolare.

Regola d'uso: **nessun codice nuovo può fare riferimento a un nome di questo file.** Un componente
nuovo usa i token di §3; un componente migrato smette di usare i nomi vecchi nello stesso commit in
cui viene migrato.

**Superfici → GROUND**

Quattro superfici diventano tre più il bianco dei campi. `--surface-1` non è più «una superficie rialzata»: risolve alla carta, perché in questo sistema nulla si rialza.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--surface-0` | `var(--paper)` | `--paper` |
| `--surface-1` | `var(--paper)` | `--paper` |
| `--surface-2` | `var(--paper-deep)` | `--paper-deep` |
| `--surface-3` | `var(--paper-edge)` | `--paper-edge` |
| `--surface-inverse` | `var(--navy)` | `--navy` |
| `--surface-overlay` | `rgb(14 22 29 / 0.55)` | valore letterale, nessun token di destinazione |
| `--color-white` | `var(--surface-input)` | `--surface-input` |

**Testo → INK**

Dieci colori di testo diventano tre inchiostri più i due colori su navy. I link sono `--ink` con una sottolineatura: non esiste più un blu di link.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--text-body` | `var(--ink)` | `--ink` |
| `--text-strong` | `var(--ink)` | `--ink` |
| `--text-secondary` | `var(--ink-secondary)` | `--ink-secondary` |
| `--text-muted` | `var(--ink-muted)` | `--ink-muted` |
| `--text-placeholder` | `var(--ink-muted)` | `--ink-muted` |
| `--text-brand` | `var(--navy)` | `--navy` |
| `--text-on-inverse` | `var(--paper-on-navy)` | `--paper-on-navy` |
| `--text-on-inverse-muted` | `var(--paper-muted-on-navy)` | `--paper-muted-on-navy` |
| `--text-link` | `var(--ink)` | `--ink` |
| `--text-link-hover` | `var(--navy)` | `--navy` |

**Rampa primaria → STRUCTURE**

La rampa a dieci passi diventa due navy. I toni intermedi non erano tinte del sistema: erano gradazioni in cerca di un compito.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--color-primary-50` | `var(--paper-deep)` | `--paper-deep` |
| `--color-primary-100` | `var(--paper-edge)` | `--paper-edge` |
| `--color-primary-300` | `var(--rule-ink)` | `--rule-ink` |
| `--color-primary-700` | `var(--navy)` | `--navy` |
| `--color-primary-800` | `var(--navy)` | `--navy` |
| `--color-primary-900` | `var(--navy)` | `--navy` |
| `--color-primary-950` | `var(--navy-deep)` | `--navy-deep` |
| `--color-neutral-950` | `var(--ink)` | `--ink` |
| `--color-secondary-800` | `var(--cooperation)` | `--cooperation` |

**Bronzo → ORDER**

**Il caso peggiore del sistema vecchio**: un colore con otto compiti diversi in 38 dichiarazioni. Ognuna risolve ora alla rubrica, il cui unico compito è l'ORDINE, e ognuna va riesaminata quando il suo file viene migrato: parecchie perderanno il colore del tutto.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--color-accent-200` | `var(--rule-hair)` | `--rule-hair` |
| `--color-accent-600` | `var(--rubric)` | `--rubric` |
| `--color-accent-700` | `var(--rubric)` | `--rubric` |
| `--border-accent` | `var(--rubric)` | `--rubric` |

**Stati**

`--color-success-*` risolve alla terna **DONE**, che è blu: è la mappatura che impedisce a un template già scritto di reintrodurre un verde di verdetto mentre viene migrato (§4.3).

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--color-success-fg` | `var(--state-done-fg)` | `--state-done-fg` |
| `--color-success-bg` | `var(--state-done-bg)` | `--state-done-bg` |
| `--color-success-border` | `var(--state-done-br)` | `--state-done-br` |
| `--color-info-fg` | `var(--state-info-fg)` | `--state-info-fg` |
| `--color-info-bg` | `var(--state-info-bg)` | `--state-info-bg` |
| `--color-info-border` | `var(--state-info-br)` | `--state-info-br` |
| `--color-warning-fg` | `var(--state-warn-fg)` | `--state-warn-fg` |
| `--color-warning-bg` | `var(--state-warn-bg)` | `--state-warn-bg` |
| `--color-warning-border` | `var(--state-warn-br)` | `--state-warn-br` |
| `--color-error-fg` | `var(--state-error-fg)` | `--state-error-fg` |
| `--color-error-bg` | `var(--state-error-bg)` | `--state-error-bg` |
| `--color-error-border` | `var(--state-error-br)` | `--state-error-br` |
| `--color-pending-fg` | `var(--state-pending-fg)` | `--state-pending-fg` |
| `--color-pending-bg` | `var(--state-pending-bg)` | `--state-pending-bg` |
| `--color-pending-border` | `var(--state-pending-br)` | `--state-pending-br` |
| `--notice-fg` | `var(--state-info-fg)` | `--state-info-fg` |
| `--notice-bg` | `var(--state-info-bg)` | `--state-info-bg` |
| `--notice-border` | `var(--state-info-br)` | `--state-info-br` |

**Bordi → RULES**

Tre bordi decorativi diventano due filetti con un significato. `--border-hairline` e `--border-subtle` collassano entrambi su `--rule-hair`, perché la distinzione fra loro non voleva dire nulla.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--border-hairline` | `var(--rule-hair)` | `--rule-hair` |
| `--border-subtle` | `var(--rule-hair)` | `--rule-hair` |
| `--border-strong` | `var(--rule-ink)` | `--rule-ink` |
| `--border-inverse` | `var(--paper-muted-on-navy)` | `--paper-muted-on-navy` |
| `--border-width` | `1px` | valore letterale, nessun token di destinazione |
| `--border-width-strong` | `2px` | valore letterale, nessun token di destinazione |

**Spazio**

Tredici passi diventano dieci: 20, 40 e 80 px non avevano posto su un ritmo di 4 px con otto gradini e risolvono al passo più vicino.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--space-1` | `var(--s-1)` | `--s-1` |
| `--space-2` | `var(--s-2)` | `--s-2` |
| `--space-3` | `var(--s-3)` | `--s-3` |
| `--space-4` | `var(--s-4)` | `--s-4` |
| `--space-5` | `var(--s-6)` | `--s-6` |
| `--space-6` | `var(--s-6)` | `--s-6` |
| `--space-8` | `var(--s-8)` | `--s-8` |
| `--space-10` | `var(--s-12)` | `--s-12` |
| `--space-12` | `var(--s-12)` | `--s-12` |
| `--space-16` | `var(--s-16)` | `--s-16` |
| `--space-20` | `var(--s-24)` | `--s-24` |
| `--space-24` | `var(--s-24)` | `--s-24` |
| `--stack-gap` | `var(--s-4)` | `--s-4` |
| `--gutter` | `var(--grid-gutter)` | `--grid-gutter` |

**Contenitori e sezioni**

`--container-max` si congelava a 1200 px a ogni larghezza superiore; `--container-wide` esisteva e non serviva a nulla di strutturale. Entrambi risolvono al contenitore che cresce per fascia (§7.1).

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--container-max` | `var(--container)` | `--container` |
| `--container-wide` | `var(--container)` | `--container` |
| `--container-narrow` | `42rem` | valore letterale, nessun token di destinazione |
| `--container-prose` | `42rem` | valore letterale, nessun token di destinazione |
| `--section-gap` | `var(--rank-b-block)` | `--rank-b-block` |

**Raggi**

Quattro raggi su una sola pagina diventavano 0 con due eccezioni, e lo shim fa risolvere `--radius-pill` al raggio di controllo: una pastiglia non era una forma di «Le Registre». V4 l'ha ripresa (`--radius-pill` vale `--radius-full`, i chip sono pastiglie) e V5 la tiene; `--radius-xs`, `--radius-sm` e `--radius-md` sono usciti dallo shim il 5 ottobre 2026, adottati con i valori di «Lo spigolo» (§7.5).

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--radius-pill` | `var(--radius-control)` | `--radius-control` |
| `--forum-radius` | `0` | valore letterale, nessun token di destinazione |

**Elevazione**

Tutti e quattro valgono `none`, così che un file migrato non possa conservare un'ombra di soppiatto. Il drawer e il `dialog` useranno `--shadow-surface` esplicitamente.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--shadow-hairline` | `none` | valore letterale, nessun token di destinazione |
| `--shadow-sm` | `none` | valore letterale, nessun token di destinazione |
| `--shadow-md` | `none` | valore letterale, nessun token di destinazione |
| `--shadow-lg` | `none` | valore letterale, nessun token di destinazione |

**Tipografia — pesi, interlinee, tracking**

Le interlinee relative restano solo finché `components.css` non usa le coppie corpo/interlinea della scala (§6.5), dove ogni interlinea è un valore assoluto multiplo di 4 px.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--weight-regular` | `400` | valore letterale, nessun token di destinazione |
| `--weight-medium` | `500` | valore letterale, nessun token di destinazione |
| `--weight-semibold` | `600` | valore letterale, nessun token di destinazione |
| `--leading-tight` | `1.15` | valore letterale, nessun token di destinazione |
| `--leading-heading` | `1.2` | valore letterale, nessun token di destinazione |
| `--leading-body` | `1.6` | valore letterale, nessun token di destinazione |
| `--leading-display` | `1.05` | valore letterale, nessun token di destinazione |
| `--leading-relaxed` | `1.65` | valore letterale, nessun token di destinazione |
| `--tracking-normal` | `var(--track-normal)` | `--track-normal` |
| `--tracking-tight` | `var(--track-band)` | `--track-band` |
| `--tracking-button` | `var(--track-normal)` | `--track-normal` |
| `--tracking-eyebrow` | `var(--track-folio)` | `--track-folio` |

**Controlli e cromatura**

`--control-height` e `--control-height-sm` sono usciti dallo shim il 5 ottobre 2026: `static/css/v5/aliases.css` li ripunta su `--control-md` (44 px, l'obiettivo interno per SC 2.5.8) e `--control-sm` (36 px), §7.5. `--nav-drawer-top` parte da `--chrome-block-size`, che è calcolata in CSS e quindi ereditata (§11.5).

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--icon-size` | `20px` | valore letterale, nessun token di destinazione |
| `--icon-size-sm` | `16px` | valore letterale, nessun token di destinazione |
| `--icon-size-lg` | `24px` | valore letterale, nessun token di destinazione |
| `--utility-height` | `var(--chrome-utility)` | `--chrome-utility` |
| `--header-height` | `var(--chrome-masthead)` | `--chrome-masthead` |
| `--nav-drawer-top` | `var(--chrome-block-size)` | `--chrome-block-size` |

**Focus**

I cinque nomi del fuoco — `--focus-ring-color`, `--focus-ring-inverse`, `--focus-ring-width`, `--focus-ring-offset`, `--focus-ring-offset-color` — sono usciti dallo shim il 5 ottobre 2026. L'anello navy su carta, con il suo contro-anello, non esiste più: V5 ha un solo sistema di fuoco (§7.5, `static/css/v5/base.css`) — i due toni restano soltanto sulle fotografie — e `static/css/v5/aliases.css` ripunta i nomi che i layer vecchi leggono ancora sui suoi token.

**Motion**

`--duration-reveal` e `--reveal-distance` valgono già `0ms` e `0`: `.reveal` è cancellata dalla direzione e il suo azzeramento fa sì che nulla si animi mentre i template vengono ripuliti (§12).

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--duration-fast` | `var(--motion-fast)` | `--motion-fast` |
| `--duration-base` | `var(--motion-base)` | `--motion-base` |
| `--duration-slow` | `var(--motion-slow)` | `--motion-slow` |
| `--duration-reveal` | `0ms` | valore letterale, nessun token di destinazione |
| `--reveal-distance` | `0` | valore letterale, nessun token di destinazione |
| `--reveal-index` | `0` | valore letterale, nessun token di destinazione |

**I sei orfani, mappati il 21 settembre 2026**

Sei nomi erano consumati da `base.css`, da `components.css` e da due fogli delle app **senza essere
dichiarati da nessuna parte**: la redirezione aveva sostituito i token e lo shim li aveva
dimenticati. Ogni `var()` cadeva quindi sul valore iniziale, in silenzio — le transizioni perdevano
la curva, il testo breve centrato perdeva il tetto di misura, e lo skip link, i dropdown e il dialog
senza JavaScript perdevano il livello dichiarato. Sono stati aggiunti allo shim il 21/09/2026 (G-25,
chiusa), il che chiude anche l'unico caso in cui due fogli delle app erano dichiarati non conformi
(§2.1). `--z-skiplink` risolve al livello del dialog, che è il più alto della lista nominata (§3.17):
lo skip link deve stare sopra tutto ciò che può coprirlo.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--ease-standard` | `var(--ease-out)` | `--ease-out` |
| `--measure-narrow` | `42ch` | valore letterale, nessun token di destinazione |
| `--z-below` | `-1` | valore letterale, nessun token di destinazione |
| `--z-dropdown` | `var(--z-header)` | `--z-header` |
| `--z-skiplink` | `var(--z-dialog)` | `--z-dialog` |

**Bottoni**

Custom property di componente, non token: restano dopo la migrazione, cambiano solo i valori che ricevono.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--btn-bg` | `var(--navy)` | `--navy` |
| `--btn-fg` | `var(--paper-on-navy)` | `--paper-on-navy` |
| `--btn-bg-hover` | `var(--navy-deep)` | `--navy-deep` |
| `--btn-fg-hover` | `var(--paper-on-navy)` | `--paper-on-navy` |
| `--btn-border` | `var(--navy)` | `--navy` |

**Locali delle app**

`apps/forum` e `apps/pathways` avevano inventato una palette privata ciascuno. Risolvono al sistema e i locali spariscono con la migrazione di quei file.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--forum-navy` | `var(--navy)` | `--navy` |
| `--forum-ink` | `var(--ink)` | `--ink` |
| `--forum-paper` | `var(--paper)` | `--paper` |
| `--forum-sand` | `var(--paper-deep)` | `--paper-deep` |
| `--forum-line` | `var(--rule-hair)` | `--rule-hair` |
| `--forum-muted` | `var(--ink-muted)` | `--ink-muted` |
| `--forum-gold` | `var(--rubric)` | `--rubric` |
| `--forum-gold-soft` | `var(--rule-hair)` | `--rule-hair` |
| `--forum-space` | `var(--s-6)` | `--s-6` |
| `--pilot-line` | `var(--rule-hair)` | `--rule-hair` |
| `--pilot-node` | `var(--rubric)` | `--rubric` |
| `--timeline-line` | `var(--rule-hair)` | `--rule-hair` |

**Scala tipografica vecchia**

Undici token di dimensione, otto dei quali schiacciati in una fascia di 9 px sotto i 24 px con quattro valori duplicati, mappati sui dieci ruoli. `--font-size-h4` valeva 18 px fissi, cioè meno del lead: risolve ora al folio, che è il quarto livello vero (§6.5).

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--font-size-display` | `var(--t-plate-size)` | `--t-plate-size` |
| `--font-size-h1` | `var(--t-title-size)` | `--t-title-size` |
| `--font-size-h2` | `var(--t-band-size)` | `--t-band-size` |
| `--font-size-h3` | `var(--t-entry-size)` | `--t-entry-size` |
| `--font-size-h4` | `var(--t-folio-size)` | `--t-folio-size` |
| `--font-size-lead` | `var(--t-lead-size)` | `--t-lead-size` |
| `--font-size-body` | `var(--t-prose-size)` | `--t-prose-size` |
| `--font-size-small` | `var(--t-gloss-size)` | `--t-gloss-size` |
| `--font-size-legal` | `var(--t-gloss-size)` | `--t-gloss-size` |
| `--font-size-caption` | `var(--t-caption-size)` | `--t-caption-size` |
| `--font-size-label` | `var(--t-ui-size)` | `--t-ui-size` |
| `--font-size-button` | `var(--t-ui-size)` | `--t-ui-size` |
| `--font-size-eyebrow` | `var(--t-folio-size)` | `--t-folio-size` |
| `--font-body` | `var(--font-ui)` | `--font-ui` |
| `--font-heading` | `var(--font-display)` | `--font-display` |
| `--font-mono` | `var(--font-ref)` | `--font-ref` |
| `--measure-lead-legacy` | `var(--measure-lead)` | `--measure-lead` |

**Il difetto che il conto alla rovescia ha fatto emergere (G-25, chiusa il 21/09/2026)**

Documentare lo shim riga per riga è ciò che ha reso visibile il suo difetto peggiore: sei nomi
consumati e dichiarati da nessuna parte, che
`tests/frontend/test_css_tokens_exist.py::test_every_referenced_custom_property_is_defined`
segnalava già su quattro file senza che nessuno leggesse il segnale. Le sei righe sono state
aggiunte e il difetto è chiuso; la tabella qui sopra le porta con il valore a cui risolvono, così la
prossima volta la discrepanza si vede nel documento prima che in un log.

---

## 18. Come estendere il sistema

### 18.1 Aggiungere un token

1. **Dire a quale dei cinque compiti appartiene** (§4.1). Se non si riesce, il token non entra. Se è
   un valore usato da un solo componente, è una custom property di componente (`--btn-bg`), non un
   token.
2. Verificare che non esista già: parecchi token sono «riserva» e sono lì proprio per questo.
3. Aggiungerlo in `static/css/tokens.css` nella famiglia giusta, rispettando i prefissi (§3) e la
   griglia (spazi multipli di 4 px, interlinee multiple di 4 px).
4. Se è un colore usato per testo o per il perimetro di un controllo: aggiungere la coppia a
   `CONTRAST_PAIRS` in `tests/frontend/test_static_assets.py` **e** una riga alla tabella di §5. La
   soglia è 4.5 per il testo e 3.0 per gli oggetti grafici, calcolata contro **`--paper`**, non
   contro il bianco.
5. Documentarlo nella tabella di §3 (token, valore letterale, risolto, uso):
   `tests/frontend/test_design_docs.py::test_every_token_is_documented_with_its_literal_value`
   fallisce finché token e documento non coincidono, e
   `tests/frontend/test_design_docs.py::test_token_family_headings_match_tokens_css` fallisce se il
   token non appartiene a nessuna famiglia documentata.
6. Se dipende dalla lingua o dal movimento, aggiungere l'override nel blocco `:root:lang(ar)` o in
   quello `prefers-reduced-motion` e documentarlo in §3.19.

### 18.2 Aggiungere un componente

1. Prima chiedersi se è un'**entrata** (§8.4). Nove volte su dieci lo è. Il catalogo di §10 e i
   pattern di §10.1 vengono prima di un blocco nuovo; un box nuovo va giustificato contro §1.2 e
   contro il test del benchmark delle card.
2. Creare `templates/components/<nome>.html` con un **commento di contratto** in testa (ogni
   variabile, obbligatoria o no, e cosa succede senza JS). Nessuna logica di business, nessun testo
   prescritto copiato, stringhe UI in francese dentro `{% translate %}`, link ad altre app via
   `safe_url`.
3. CSS in una nuova sezione numerata di `static/css/components.css`: BEM, **solo token di §3** (mai
   un nome dello shim), solo proprietà logiche, stati via attributi ARIA, bersagli ≥ 44 px, focus
   ereditato da `:focus-visible`, comportamento RTL pensato subito. La struttura si disegna con
   `border`, `outline` o testo, mai con un `background` su uno pseudo-elemento.
4. Verificare i quattro cancelli di composizione: raggio 0 (due eccezioni), nessun `box-shadow`,
   `border: 1px` solo su controlli e `dialog`, nessun colore che significhi «approvato».
5. JS solo se migliora un markup che già funziona: nuova funzione `init…` in `static/js/main.js`,
   hook `data-*`, nessun handler inline, rispetto di `prefers-reduced-motion`.
6. Accessibilità: elemento nativo prima di ARIA; nome accessibile per ogni controllo; tastiera
   completa; provare a 320 px, in arabo e senza JS.
7. Documentare: scheda in §10 con lo stesso schema (scopo, blocco CSS, contratto, varianti,
   accessibilità, usato in, esempio) e riga nel modello tastiera di `docs/ACCESSIBILITY.md` §3 se è
   interattivo. Il test fallisce se un file in `templates/components/` non ha la sua scheda, e
   viceversa.

### 18.3 Aggiungere un'icona

Disegnarla sulla griglia 24 × 24 con tratto 1.5 e **terminali quadri**, senza `fill`/`stroke` e senza
un solo esadecimale nel file; aggiungere `<symbol id="icon-<nome>" viewBox="0 0 24 24">` in
`static/img/icons.svg`; **validare il file come XML** (mai `--` dentro un commento); aggiungere il
nome all'elenco di §13. Se indica una direzione di lettura, usarla sempre con `.icon--flip-rtl`.
Ricordare il tetto: al massimo sei icone per pagina.

### 18.4 Togliere una riga dallo shim

1. Scegliere **un** foglio o **un** template e sostituire tutti i nomi legacy che usa con i token di
   §3, nello stesso commit.
2. Cancellare da `static/css/_legacy-tokens.css` le righe che nessun altro file usa più.
3. Aggiornare la tabella di §17: il test confronta il file riga per riga con il documento, quindi il
   conto alla rovescia si aggiorna da solo o la suite diventa rossa.
4. Se il foglio era dichiarato non conforme in §2.1, toglierlo da lì e dalla costante
   `KNOWN_NON_CONFORMING_APP_STYLESHEETS` di `tests/frontend/test_design_docs.py`.

---

## 19. Screenshot QA (`docs/qa/design/`)

Generati da `docs/qa/design/capture.py` (Playwright, Chromium, `device_scale_factor=1`) contro il
server di sviluppo locale con `DJANGO_DEBUG=False` (altrimenti Django mostra la propria pagina 404
tecnica), su un **database dedicato** (`DATABASE_URL` proprio, `migrate` + `seed_all`: il database di
sviluppo condiviso non va né migrato né popolato da chi cattura). Data di sistema 20/09/2026, quindi
gate di Fase 3 chiuso e form pubblici chiusi (G2).

Il report `docs/qa/design/capture-report.json` registra per ogni cattura stato HTTP, `dir`, numero di
`h1`, overflow orizzontale, richieste esterne, blocchi `.reveal` nascosti, icone disposte e icone
vuote; le catture del drawer aggiungono la geometria del pannello e del velo, quelle senza JavaScript
la geometria dell'header, quelle del form in errore l'elemento che ha il focus dopo un invio non
valido: **43 catture**, stato HTTP atteso ovunque (200; 404 per la pagina inesistente), 0 overflow,
0 richieste esterne, un solo `h1` per pagina, 0 blocchi `.reveal` nascosti al caricamento, 0 icone
vuote. Lo script esce con codice 1 se una di queste condizioni non è rispettata. I PNG sono
git-ignorati: rigenerarli in locale.

**Queste catture precedono la migrazione di `components.css`**: mostrano i token, la scala e il
layout nuovi sotto i componenti vecchi, quindi vanno lette come la linea di base da cui si misura la
redirezione e non come il risultato. Vanno rigenerate a ogni passo della migrazione. La matrice
della direzione aggiunge una cattura a **colori forzati** per archetipo, che `capture.py` non
produce ancora anche se il livello `forced-colors` esiste ormai in `register.css` (G-26).

| Pagina | Francese (LTR) | Arabo (RTL) |
|---|---|---|
| Home | `docs/qa/design/home-fr-390.png`, `docs/qa/design/home-fr-768.png`, `docs/qa/design/home-fr-1440.png` | `docs/qa/design/home-ar-390.png`, `docs/qa/design/home-ar-768.png`, `docs/qa/design/home-ar-1440.png` |
| `/privacy-policy/` — pagina legale bloccata (gate G1) | `docs/qa/design/privacy-fr-390.png`, `docs/qa/design/privacy-fr-768.png`, `docs/qa/design/privacy-fr-1440.png` | `docs/qa/design/privacy-ar-390.png`, `docs/qa/design/privacy-ar-768.png`, `docs/qa/design/privacy-ar-1440.png` |
| `/compte/login/` — allauth sul design system | `docs/qa/design/login-fr-390.png`, `docs/qa/design/login-fr-768.png`, `docs/qa/design/login-fr-1440.png` | `docs/qa/design/login-ar-390.png`, `docs/qa/design/login-ar-768.png`, `docs/qa/design/login-ar-1440.png` |
| `/page-inexistante/` — 404 | `docs/qa/design/404-fr-390.png`, `docs/qa/design/404-fr-768.png`, `docs/qa/design/404-fr-1440.png` | `docs/qa/design/404-ar-390.png`, `docs/qa/design/404-ar-768.png`, `docs/qa/design/404-ar-1440.png` |

| Stato / variante | File |
|---|---|
| Skip link con focus | `docs/qa/design/state-skiplink-fr-390.png`, `docs/qa/design/state-skiplink-ar-390.png` |
| Drawer aperto a 390 px e a 1024 px (sotto 80rem; G-02 chiusa, G-23 aperta) | `docs/qa/design/state-drawer-open-fr-390.png`, `docs/qa/design/state-drawer-open-ar-390.png`, `docs/qa/design/state-drawer-open-fr-1024.png`, `docs/qa/design/state-drawer-open-ar-1024.png` |
| Mega-menu aperto da tastiera, focus nel pannello | `docs/qa/design/state-megamenu-open-fr-1440.png`, `docs/qa/design/state-megamenu-open-ar-1440.png` |
| Focus su un campo | `docs/qa/design/state-focus-field-fr-1440.png`, `docs/qa/design/state-focus-field-ar-1440.png` |
| Form con errori (riepilogo + errori di campo) | `docs/qa/design/state-form-errors-fr-390.png`, `docs/qa/design/state-form-errors-ar-390.png` |
| `prefers-reduced-motion: reduce` | `docs/qa/design/a11y-reduced-motion-fr-1440.png` |
| Zoom 200 % (1280 px → 640 px CSS) | `docs/qa/design/a11y-zoom200-fr-640.png` |
| Zoom 400 % (1280 px → 320 px CSS) | `docs/qa/design/a11y-zoom400-fr-320.png`, `docs/qa/design/a11y-zoom400-ar-320.png` |
| JavaScript disattivato (a 390 e 1024 px mostra G-04) | `docs/qa/design/a11y-nojs-fr-390.png`, `docs/qa/design/a11y-nojs-fr-1024.png`, `docs/qa/design/a11y-nojs-fr-1440.png` |

Nella stessa cartella `tests/frontend/test_browser.py` scrive le proprie catture a 360 / 768 / 1440.

---

## 20. Controlli automatici

Nessuno di questi sostituisce axe-core o una prova manuale: bloccano le regressioni dei contratti.
La colonna «Che cosa protegge» è la ragione per cui il test esiste; se il test si può soddisfare
senza soddisfare quella ragione, il test è scritto male.

| Che cosa protegge | Test |
|---|---|
| I token esistono, hanno le famiglie previste e i dieci ruoli della scala | `tests/frontend/test_static_assets.py::test_tokens_file_is_complete` |
| Ogni interlinea è un multiplo di 4 px | `tests/frontend/test_static_assets.py::test_every_line_height_is_a_multiple_of_four` |
| Il corpo del testo non cambia mai dimensione fra i breakpoint | `tests/frontend/test_static_assets.py::test_prose_size_never_changes_across_breakpoints` |
| 29 coppie di contrasto, ricalcolate dai valori reali | `tests/frontend/test_static_assets.py::test_wcag_contrast` |
| Nessun colore fuori dai token in `static/css/` | `tests/frontend/test_static_assets.py::test_no_hardcoded_colours_outside_tokens_and_fonts` |
| Ogni custom property citata da un foglio è definita da qualche parte | `tests/frontend/test_css_tokens_exist.py::test_every_referenced_custom_property_is_defined` |
| Ogni icona usata nei template esiste nello sprite | `tests/frontend/test_static_assets.py::test_every_icon_used_in_templates_exists_in_sprite` |
| Lo sprite è XML ben formato e ogni `<symbol>` ha il suo `viewBox` | `tests/frontend/test_design_docs.py::test_icon_sprite_is_well_formed_xml`, `tests/frontend/test_svg_wellformed.py::test_svg_is_wellformed_xml` |
| Le illustrazioni evitano i soggetti vietati e i marchi di enti | `tests/frontend/test_static_assets.py::test_illustrations_avoid_stereotyped_subjects` |
| Nessuno stile inline, nessun handler `on*`, nessun host esterno | `tests/frontend/test_static_assets.py::test_owned_templates_have_no_forbidden_strings_inline_styles_or_handlers`, `tests/frontend/test_static_assets.py::test_static_assets_have_no_external_hosts_or_forbidden_strings` |
| `main.js` è un modulo ES senza dipendenze e rispetta il movimento ridotto | `tests/frontend/test_static_assets.py::test_main_js_is_an_es_module_without_external_dependencies` |
| `fonts.css` cita solo file locali che esistono; i font sono davvero self-hosted | `tests/frontend/test_layout.py::test_fonts_css_references_only_local_files_that_exist`, `tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded` |
| Landmark, skip link, `main` focusabile, un solo `h1` | `tests/frontend/test_layout.py::test_shell_landmarks_skip_link_and_single_h1` |
| Nessuna risorsa esterna, nessuno stile inline nella shell | `tests/frontend/test_layout.py::test_no_external_resources_or_inline_styles` |
| `lang` / `dir` e preload dei font per direzione | `tests/frontend/test_layout.py::test_html_lang_and_dir_attributes` |
| Il solo bundle `css/dist/main.css` è applicato; nessun layer precaricato | `tests/frontend/test_design_docs.py::test_base_template_stylesheet_links_match_the_documented_architecture` |
| Nessun overflow orizzontale a 360 / 768 / 1440 in fr e ar | `tests/frontend/test_browser.py::test_no_horizontal_overflow_and_screenshots` |
| Mega-menu e drawer da tastiera | `tests/frontend/test_browser.py::test_mega_menu_is_keyboard_operable`, `tests/frontend/test_browser.py::test_mobile_drawer_and_language_switcher` |
| Il breakpoint della navigazione è identico in CSS, JS e documenti | `tests/frontend/test_design_docs.py::test_navigation_breakpoint_is_consistent_and_documented` |
| Ogni token è documentato con il suo valore letterale e appartiene a una famiglia | `tests/frontend/test_design_docs.py::test_every_token_is_documented_with_its_literal_value`, `tests/frontend/test_design_docs.py::test_token_family_headings_match_tokens_css` |
| L'etichetta «riserva» è vera nei due sensi | `tests/frontend/test_design_docs.py::test_reserve_labels_match_the_design_system_stylesheets` |
| La tabella dei contrasti è ricalcolata e copre ogni coppia bloccata | `tests/frontend/test_design_docs.py::test_contrast_table_matches_recomputed_ratios`, `tests/frontend/test_design_docs.py::test_contrast_table_covers_every_pair_locked_by_the_asset_tests` |
| Ogni riga dello shim è documentata con il suo sostituto: il conto alla rovescia è visibile | `tests/frontend/test_design_docs.py::test_every_legacy_shim_token_is_documented_with_its_replacement` |
| Lo shim **non cresce**: tetti sul numero di token, di classi e di usi dei nomi ritirati, e nessun file scritto dopo la redirezione parla la lingua vecchia | `tests/frontend/test_legacy_token_shim.py::test_the_shim_does_not_grow`, `tests/frontend/test_legacy_token_shim.py::test_the_shim_class_list_does_not_grow`, `tests/frontend/test_legacy_token_shim.py::test_the_legacy_usage_count_does_not_grow`, `tests/frontend/test_legacy_token_shim.py::test_no_new_file_is_written_against_the_retired_system` |
| Nessuna riga dello shim punta a un token che non esiste | `tests/frontend/test_legacy_token_shim.py::test_every_shim_token_resolves_to_a_real_token` |
| Ogni componente ha la sua scheda, e ogni scheda un componente reale | `tests/frontend/test_design_docs.py::test_every_component_file_has_a_section_and_vice_versa` |
| I blocchi CSS e i consumatori citati esistono davvero | `tests/frontend/test_design_docs.py::test_component_css_blocks_and_consumers_are_real`, `tests/frontend/test_design_docs.py::test_usato_in_minimum_counts_are_true` |
| Le variabili del contratto sono davvero usate dal template | `tests/frontend/test_design_docs.py::test_documented_contract_variables_are_used_by_the_component_template` |
| I file citati (percorsi, test, screenshot) esistono | `tests/frontend/test_design_docs.py::test_cited_paths_exist`, `tests/frontend/test_design_docs.py::test_cited_tests_exist`, `tests/frontend/test_design_docs.py::test_referenced_screenshots_can_be_produced_by_the_capture_script` |
| I pesi dei file dichiarati restano entro il 10 % del vero | `tests/frontend/test_design_docs.py::test_documented_file_weights_are_roughly_true` |
| I fogli delle app usano solo token esistenti, nessun colore letterale, nessun gradiente | `tests/frontend/test_design_docs.py::test_conforming_app_stylesheets_use_only_design_tokens`, `tests/frontend/test_design_docs.py::test_app_asset_inventory_is_truthful` |
| Lo stato delle lacune resta coerente fra i due documenti, i marcatori xfail e il report delle catture | `tests/frontend/test_design_docs.py::test_gap_status_and_xfail_markers_stay_in_lockstep`, `tests/frontend/test_design_docs.py::test_capture_report_is_current_and_backs_the_documented_figures` |
| Una pagina d'errore non viene scambiata per una cattura valida | `tests/frontend/test_design_docs.py::test_capture_script_never_accepts_an_error_page_as_a_valid_capture` |
| Nessun `backdrop-filter` sull'header che contiene il drawer `position: fixed` | `tests/frontend/test_design_docs.py::test_sticky_header_does_not_trap_fixed_drawer` |

**Cancelli che la direzione richiede e che non hanno ancora un test**, perché il livello che
dovrebbero sorvegliare non è ancora scritto: `grep box-shadow` restituisce solo l'anello di fuoco;
`border: 1px` corrisponde solo ai controlli e a `dialog`; nessun tipo di corpo e nessun rango di
sezione si ripete due volte di seguito; ogni pagina usa almeno quattro dei sei tipi di corpo e almeno
due fondi; una `<figure>` senza `<figcaption>` è un errore di build; nessun `letter-spacing` diverso
da zero è raggiungibile sotto `:lang(ar)`; nessuna stringa maiuscola nei cataloghi `.po`. Sono
elencati qui perché un cancello non scritto è un cancello che nessuno ricorda (G-26).

---

## 21. Difetti noti

L'elenco completo, con criterio WCAG, evidenza, correzione proposta e modalità di verifica in QA, è
in `docs/ACCESSIBILITY.md` §13 (**G-01 … G-27**); qui i difetti che toccano il design system. Una
riga «chiusa» resta in tabella con la data e l'evidenza della chiusura.

| Id | Gravità | Difetto | File | Correzione proposta |
|---|---|---|---|---|
| G-01 | chiusa il 20/09/2026 (era bloccante) | sprite delle icone non ben formato (`--` in un commento XML): nessuna icona disegnata | `static/img/icons.svg` | fatto dall'owner: commento riformulato; 546 icone disposte e 0 vuote nel report delle catture (§13) |
| G-02 | chiusa il 20/09/2026 (era bloccante) | `backdrop-filter` su `.site-header` lo rendeva containing block di `.nav-drawer` e `.nav-overlay`: drawer alto 65 px, overlay 0 px | `static/css/components.css` | fatto dall'owner: velo spostato su `.site-header::before` (§1.4); drawer alto quanto lo spazio disponibile; dal foglio (W2-C2) il menu sta fuori dall'header (§11.2) |
| G-03 | alta (RTL) | stringhe d'identità latine non isolate in arabo: «™Italy Legal Entry» nel footer, promotore troncato all'inizio nella barra | `static/css/base.css`, `apps/cms/templatetags/cms_nav.py` | `dir="ltr"` nel tag `brand`, `<bdi>` su promotore e riga del ©, e divieto di `text-overflow: ellipsis` su testo d'identità (§15.5) |
| G-04 | chiusa l'08/10/2026 (era alta) | senza JS, sotto 80rem, l'header sticky conteneva l'intero menu: **781 px**; a 390 × 844 restavano 63 px di pagina visibili, a 1024 × 768 nessuno | `static/css/v5/chrome.css` | fatto (W2-C1): l'header non sticky senza JS; dal foglio (W2-C2) la testata non contiene più il menu, che si mostra sul posto (`:target`) (§11.2) |
| G-09 | chiusa il 21/09/2026 | le numerazioni decorative erano in bronzo a 3.83:1, sotto la soglia del testo | `static/css/tokens.css` | chiusa dalla redirezione: il bronzo non esiste più e gli ordinali sono in `--rubric`, 6.92:1 sulla carta — sicuri come testo a qualunque corpo (§5) |
| G-13 | bassa | `id` derivato dal titolo in `cta_panel.html`; `id` fisso in `hero.html` | `templates/components/cta_panel.html`, `templates/components/hero.html` | accettare un parametro `id` |
| G-14 | bassa | separatore « : » francese generato in CSS dopo `<dt>` in `.meta-row` | `static/css/v5/card.css` | spostare il separatore nel template, tradotto |
| G-15 | chiusa il 21/09/2026 | `--font-mono` nominava IBM Plex Mono, che non era self-hosted: il registro tecnico era il monospazio di sistema | `static/css/tokens.css` | chiusa dalla redirezione: `--font-ref` nomina Fira Mono, i cui due file sono in `static/fonts/`; dal 5 ottobre 2026 (design V5, W1-A) il ruolo è «ILE Mono», un file self-hosted dichiarato in `static/css/v5/fonts.css` (§6.2) |
| G-16 | chiusa il 20/09/2026 | `docs/I18N_RTL.md` era citato dai CSS e dai cataloghi ma non esisteva | `docs/` | il documento è stato scritto: `docs/I18N_RTL.md` |
| G-19 | chiusa il 09/10/2026 (era bassa) | le FAQ usano `.accordion__panel`, classe che il design system non definiva (il componente usa `.accordion__body`) | `static/css/v5/tabs.css` | fatto (W1-C): il foglio della disclosure definisce `.accordion__panel` come `.accordion__body` — misura di lettura, rientro della riga, 24 px prima del filetto |
| G-20 | bassa | `.reveal--stagger` non produce uno scaglionamento visibile e ritarda l'hover dei figli | `static/css/components.css` | la direzione cancella `.reveal` per intero (§12): il difetto sparisce con il modificatore |
| G-21 | chiusa il 09/10/2026 (era bassa) | `remember` delle tab scriveva in `localStorage` ma non rileggeva | `static/js/main.js` | fatto (W1-C): l'opzione è tolta dal componente e da `initTabs` (piano V5.4 §1.15: la scelta non è ricordata) |
| G-22 | media — chiusa il 20/09/2026 | due fogli dello Stage 1 erano fuori sistema: token inesistenti con ripieghi esadecimali, `linear-gradient`, anello di focus proprio a 3.01:1 | `apps/forum/static/forum/forum.css`, `apps/orientation/static/orientation/wizard.css` | fatto dagli owner: solo token reali, fondo piatto, focus di `base.css` |
| G-23 | chiusa l'08/10/2026 (era media) | a drawer aperto e pagina non scrollata l'overlay era dipinto sopra la fascia bassa dell'header (partiva da 72 px, l'header finiva a 113 px): wordmark e bottone «Menu» velati | `static/css/v5/chrome.css`, `static/js/src/nav.js` | fatto (W2-C1): il velo partiva dal piede reale dell'header; dal foglio (W2-C2) la testa del foglio sta sopra il velo, «Fermer» dov'era «Menu» (§11.2) |
| G-24 | chiusa il 21/09/2026 (era media) | `templates/base.html` precaricava per le pagine LTR due woff2 che la redirezione aveva cancellato (`ibm-plex-sans-400-normal-latin.woff2`, `ibm-plex-serif-500-normal-latin.woff2`): due 404 per pagina e nessun preload utile | `templates/base.html` | fatto: le pagine LTR precaricano ora `newsreader-200-800-normal-latin.woff2` e `fira-sans-500-normal-latin.woff2`, quelle RTL `noto-naskh-arabic-400-700-normal-arabic.woff2` e `ibm-plex-sans-arabic-400-normal-arabic.woff2` (§6.4) |
| G-25 | chiusa il 21/09/2026 (era media) | sei custom property erano consumate da quattro fogli e **non erano dichiarate da nessuna parte**: lo shim non le aveva mappate, quindi ogni `var()` cadeva sul valore iniziale — una transizione perdeva la curva, una misura perdeva il tetto e tre livelli di `z-index` valevano `auto` | `static/css/_legacy-tokens.css` | fatto: le sei righe sono state aggiunte allo shim, mappate sui token di §3 (§17); `tests/frontend/test_css_tokens_exist.py::test_every_referenced_custom_property_is_defined` passa su tutti i fogli e i due fogli delle app sono tornati conformi (§2.1) |
| G-26 | media (processo) | tre cancelli dichiarati dalla direzione non hanno ancora un test e non sono soddisfatti da `components.css`: nessun `box-shadow` fuori da `.nav-drawer` e `dialog` (restano otto dichiarazioni che nominano i token d'ombra, anche se valgono `none`), `border: 1px` solo su controlli e `dialog`, e il livello `@media (forced-colors: active)`, che `register.css` ha e `components.css` no. Manca inoltre la cattura a colori forzati nella matrice degli screenshot | `static/css/components.css`, `docs/qa/design/capture.py`, `tests/frontend/` | estendere a `components.css` il livello a colori forzati di `register.css` durante la sua migrazione, e scrivere i tre test con esso (§20) |
| G-27 | chiusa il 21/09/2026 (era bassa) | `.plate--verso .folio__ordinal` dipingeva l'ordinale del folio in `--rubric-on-navy`, che vale 4.46:1 sul navy: sotto `md` il numerale è di 22–24 px, quindi non è testo grande e mancava la soglia di 4.5:1 per 0.04, contro la regola «solo filetto, mai testo» della direzione | `static/css/register.css` | fatto: dentro una fascia verso il numerale è `--paper-on-navy` e la rubrica su navy è rimasta il solo filetto; le cinque dichiarazioni che la consumano in `static/css/` sono tutte bordi (§5) |

*Nota sul conto alla rovescia.* `tests/frontend/test_legacy_token_shim.py` esiste dal 21 settembre
2026 e tiene i tetti: 142 token, 14 classi e 1 515 usi complessivi dei nomi ritirati in
`static/css/`, nei fogli delle app e nei template. **Sono massimi, non obiettivi**: si abbassano nel
commit stesso in cui una migrazione toglie delle voci, e non si alzano mai.
`tests/frontend/test_legacy_token_shim.py::test_the_shim_is_gone` è la linea d'arrivo, dichiarata
come test xfail perché resti visibile: quando passa, si cancella lo shim, si toglie il suo `@import`
da `static/css/main.css` e si cancella quel file di test. La metà documentale della garanzia è
`tests/frontend/test_design_docs.py::test_every_legacy_shim_token_is_documented_with_its_replacement`,
che confronta il file riga per riga con §17.

---

*Fine del DESIGN SYSTEM 2026. La direzione che lo genera è `docs/design/ART_DIRECTION_A.md`; la
decisione che la rende vincolante è `docs/design/ART_DIRECTION_DECISION.md`; il documento gemello
sull'accessibilità è `docs/ACCESSIBILITY.md`.*
