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
| Sorgenti documentate | `static/css/main.css`, `static/css/fonts.css`, `static/css/tokens.css`, `static/css/_legacy-tokens.css`, `static/css/base.css`, `static/css/layout.css`, `static/css/components.css`, `static/js/head.js`, `static/js/main.js`, `static/img/icons.svg`, `static/img/illustrations/`, `static/fonts/`, `templates/base.html`, `templates/partials/`, `templates/components/` |
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
| `.dialog::backdrop` (`components.css` §21) | `background: var(--surface-overlay)` + `backdrop-filter: blur(2px)` | attenua la pagina dietro il modale; nessun contenuto è posto sopra il blur |
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
scrivono solo in watch e non si versionano. I pesi qui sotto sono quelli delle **sorgenti**, in
ordine di cascata:

| Ordine | File | Peso (non compresso, indicativo) | Contenuto |
|---|---|---|---|
| 1 | `fonts.css` | 13.7 KB | 26 regole `@font-face` generate da `scripts/fetch_fonts.py` (non modificare a mano) |
| 2 | `tokens.css` | 11.6 KB | 105 custom property su `:root`, cinque fasce di breakpoint, override `:lang(ar)` / `[dir=rtl]`, override `prefers-reduced-motion` |
| 3 | `_legacy-tokens.css` | 12.5 KB | **impalcatura di demolizione**, non design system: 153 nomi vecchi mappati sul nuovo sistema, più 14 classi tipografiche legacy. Il file solo si accorcia (§17) |
| 4 | `base.css` | 14.9 KB | reset, i dieci ruoli tipografici, cifre, link, focus, skip link, `.prose`, helper bidi, stampa |
| 5 | `layout.css` | 10.0 KB | contenitori, la griglia a tre zone, sezioni per rango, griglia editoriale, utility di composizione |
| 6 | `components.css` | 75.9 KB | 29 sezioni numerate: controlli → feedback → shell di navigazione → pattern di contenuto → form → overlay → motion. **Non ancora migrato**: vive sui nomi dello shim |
| 7 | `register.css` | 28.2 KB | **il linguaggio grafico proprio** (§8): folio, registro ed entrata, sequenza, barra di giurisdizione, lastra e fascia verso, nota marginale, elenco delle fonti, esito, pastiglia di stato, regione vuota, più il livello `@media (forced-colors: active)` |
| 8 | `v2/tokens.css` | 6.1 KB | **design V2** (`docs/design-v2/DESIGN_SYSTEM_V2.md`): i token di «due rive, una porta» — due capitoli di superficie, un solo accento interattivo, tre voci tipografiche, quattro durate, tre curve |
| 9 | `v2/bridge.css` | 2.4 KB | **impalcatura di migrazione, esiste per essere cancellata**: ripunta terreno, navy e rosso rubrica del sistema vecchio sui valori nuovi, così nessuna pagina resta a metà fra due direzioni finché la propagazione non è finita. Se ne va con `register.css` |
| 10 | `v2/shell.css` | 13.3 KB | carta intestata: barra istituzionale, testata, lock-up ufficiale e la sua unica variante scura, navigazione desktop e cassetto, piè di pagina, anello di focus |
| 12 | `v2/routes.css` | 7.6 KB | le quattro vie d'accesso come molo a zig-zag: indice, glifo di rilievo, tinta, linea d'ormeggio |
| 13 | `v2/voyage.css` | 6.8 KB | la rotta fra le due rive: linea che si disegna allo scroll, stazioni allineate ai punti, dorsale verticale sotto 64rem |
| 14 | `v3/buttons.css` | 17.3 KB | **design V3, il sistema completo dei bottoni**: lastra 48/40/56, luce verticale come materiale (nessuna ombra portata: §2 V2 e la modalità DENSE), hover come colore col bordo intatto, pressione a `translate`, filetto d'ormeggio sulle varianti in riga, mezzanotte per contesto (`.hero`, `.on-inverse`, `.forum-*`) e `.btn--inverse` come sinonimo, disabled a colore, anello di focus con alone, gerarchia sotto colori forzati. Sovrascrive la §1 di `components.css` proprietà per proprietà e possiede da solo i bottoni di `v2/hero.css` e `forum.css` |
| 15 | `v3/chip.css` | 13.3 KB | **design V3, la vidimazione**: la pastiglia di stato come timbro di registro — parola nell'inchiostro del capitolo, colore solo nella marca (filetto + corpo all'8 %), sei registri da `data-register` derivato dall'enum in `apps/core/chips.py` (neutro · attesa · azione · conforme · rifiuto · nullo), significato portato tre volte senza colore (parola, stile del filetto, geometria), sigillo con angolo tagliato e filetto doppio, misuratore di fase, stati interattivi come scarto dal riposo del capitolo. Prende `.badge` subito; `.state` quando i suoi 65 siti portano l'attributo |
| 16 | `v4/tokens.css` | 15.5 KB | **design V4** (`docs/design-v4/DESIGN_SYSTEM_V4.md`, dopo la direttiva del committente del 24/09/2026): i token di «il portico e la console», caricati **per ultimi con i nomi V2** — il navy evoluto dal marchio ufficiale, l'accento come famiglia con due gradienti, le ricette di sfondo, cinque profondità e sei ruoli d'ombra, cinque raggi, la superfamiglia Plex (`--font-ui`, `--font-ref` e `--font-mono` ripuntati), la scala della console `--u-*`, misure di layout e controlli, dieci livelli `z`, sei durate e tre curve (i nomi V2 sono alias). Ripete l'override sotto `md` e il moto ridotto perché un `:root` successivo vince su una media query precedente; non ridefinisce `--border-strong` / `--border-accent`, che nello shim sono colori (le linee sono `--line-*`) |
| 17 | `v4/buttons.css` | 8.3 KB | **design V4, il materiale dei bottoni** sopra il sistema V3: altezze 44/36/52/40, raggio `md`, il primario come gradiente verticale con ombra di livello 1 che diventa alone in hover, luce invertita alla pressione, la variante SOFT (fondo `--accent-wash`), i contesti scuri con il gradiente chiaro; V3 resta il sistema (lastra, varianti, in riga, disabled, focus, colori forzati) |
| 18 | `v4/shell.css` | 21.6 KB | **design V4, la carta intestata come barra di prodotto** sopra `v2/shell.css` e `components.css` §7: barra istituzionale a 32 px con il solo promotore; testata 64 px che allo scroll passa a 56 px in vetro (`--glass-light`, blur 12; 92 % sopra un capitolo scuro, classe da `shell.js`) con il lock-up che scala come unità; voci Plex 15/20 500 su 44 px con l'**indicatore che trasla** (`shell.js`, `SPRING_SNAPPY`; senza script resta la linea per voce di V2); mega-menu che si **espande dal bordo della barra** a tutta larghezza (L3, angoli inferiori `xl`, 4/8, `mega-in`); controllo lingua **segmentato** FR · IT · EN · ع e «Espace réservé» con lucchetto sulla barra istituzionale (le sette voci del menu CMS non lasciano loro posto nella testata: misurato, 905 + 303 px su 1240); sotto 80rem il cassetto entra dal lato del menu con scrim sfocato e porta in testa le stesse azioni |
| 19 | `v4/workspace.css` | 53.2 KB | **design V4, i componenti delle pagine della console** (gate C: dashboard e Mes pièces): griglia di lavoro a 12 colonne con tre misure di pannello, Panel L1/L2 con bordo a gradiente via mask, ContextHeader e testata di workspace, fatti con il misuratore a tacche, ResponsibilityBar, Glyph, HealthStrip a segmenti proporzionali (`attr()` tipizzato, ripiego a segmenti uguali), SegmentedControl di link con lo stato in `?état=`, ricerca 44, DocumentCollection e DocumentRow a sette zone che sotto 48rem diventa DocumentCard, menu di riga come `popover` nativo, JourneyRail orizzontale da 64rem che si disegna una volta, liste di date e di messaggi, EmptyState, la forma a pillola dei chip; col gate D (fascicolo): la testata
di contesto con eyebrow, responsabile e misuratore, la barra di contesto compatta in vetro allo scroll, la
griglia 8/4 con inspector appiccicoso, la JourneyRail descrittiva (verticale, con le date), la Timeline
(`tl-light`), la Table semantica a testata appiccicosa che sotto 64rem diventa schede etichettate, gli
intervenants, la barra dell'azione primaria del telefono; col gate E (cruscotto impresa): i fatti su due
colonne col glifo dell'impresa, la Table dei bisogni. Solo token |
| 20 | `v4/hero.css` | 23.0 KB | **design V4, l'hero della home** («il portico»): capitolo IMMERSIVE (navy evoluto + mesh radiale + grana 3 %), griglia 6/6 da `xl`, titolo bloccato 44→76, **il palcoscenico** — la porta del committente disegnata in un solo SVG (arco, fotografia, arco interno navy, chiave, gradini) con le quattro vie dell'ecosistema che l'attraversano e la **legenda in vetro** (livello 3, blur 16) ancorata per costruzione alle vie; la corrente lungo le vie è l'unico oggetto vivo; sotto 64rem la porta da sola e la legenda come righe. Sostituisce `v2/hero.css`: territorio, marea, striscia delle coordinate e comando «Suspendre le mouvement» sono rimossi (direttiva §5) |
| 21 | `v4/wizard.css` | 11.7 KB | **design V4, il modulo guidato** («Ma situation», gate D): lo Stepper verticale coi nodi che si riempiono, il palcoscenico con la luce FOCUS, le OptionCard su input nativi (`:has(:checked)`), il piede appiccicoso in vetro con «Précédent» · «Continuer» e il submit; sopra la navigazione inferiore sotto 64rem. Solo token |

Convenzioni:

- **BEM-like**: `.block`, `.block__element`, `.block--modifier`. Stati tramite attributi, non classi:
  `[aria-current]`, `[aria-expanded="true"]`, `[aria-selected="true"]`, `[open]`,
  `[data-open="true"]`, `body[data-nav-open="true"]`. Uniche classi di stato: `.is-visible` e
  `.is-active`.
- **Custom property di componente** (non sono token globali): `--btn-bg`, `--btn-fg`, `--btn-border`,
  `--btn-bg-hover`, `--btn-fg-hover`, `--notice-fg`, `--notice-bg`, `--notice-border`,
  `--timeline-line`, `--stack-gap`, `--reveal-index` (impostata da `main.js`), `--nav-drawer-top`
  (impostata da `main.js` all'apertura del drawer). Oggi vivono tutte nello shim.
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
| `apps/pages/static/pages/css/pages.css` | `templates/pages/home.html`, `templates/pages/institutional_base.html` | conforme dal 21 settembre 2026 (G-25 chiusa): i due nomi che richiamava, --ease-standard e --z-below, sono ora dichiarati dallo shim; nessun colore letterale, nessun gradiente |
| `apps/pages/static/pages/js/home.js` | `templates/pages/home.html` | modulo ES senza dipendenze: mostra il bottone «Masquer cette annonce» del banner della home (nascosto senza JS), ricorda la scelta in `sessionStorage` per la sola scheda corrente, porta il focus su `main` |
| `apps/ecosystem/static/ecosystem/ecosystem.css` | `templates/ecosystem/_layout.html` | conforme dal 21 settembre 2026 (G-25 chiusa): i due nomi che richiamava, --ease-standard e --measure-narrow, sono ora dichiarati dallo shim; nessun colore letterale, nessun gradiente |
| `apps/portal/static/portal/portal.css` | `templates/portal/base_portal.html` | conforme: solo token esistenti, solo proprietà logiche, nessun gradiente |
| `apps/portal/static/portal/console.css` | `templates/portal/base_portal.html` | conforme (15.0 KB): **la console V4** (`docs/design-v4/CREATIVE_DIRECTION.md` §3.9) — rail 64/248 fissa al bordo di lettura sul navy con la mesh attenuata, voci 44 px raggio `md` con glifo + parola, gruppi con titolo, voce attiva `--mid-3` + indicatore 3 px, tooltip L3 a rail chiusa; barra di contesto 56 px in vetro appiccicosa (breadcrumb, «Site public», account, lingua segmentata); workspace 1320; sotto 64rem barra superiore, barra inferiore a quattro voci + «Menu» e cassetto `<dialog>` con la rail intera. Solo token, solo proprietà logiche, `var(--mesh-dark)` e `var(--glass-light)` senza alcun gradiente letterale |
| `apps/accounts/static/accounts/entrance.css` | `templates/allauth/layouts/entrance.html` | conforme (5.8 KB): **l'ingresso V4** (`CREATIVE_DIRECTION.md` §3.3) — due pannelli 5/7 da 64rem: la porta sul navy con la riga d'aiuto su una striscia in vetro; il foglio L2 480 px raggio `xl` su fondo FOCUS, titolo Plex 28/36 600, campi 44 px raggio `md`, il solo primario a 52 px; sotto 64rem fascia con l'arco poi il foglio |
| `apps/forum/static/forum/forum.css` | `templates/forum/index.html`, `templates/forum/register.html`, `templates/forum/register_done.html` | conforme dal 20 settembre 2026 (G-22 chiusa): fondo piatto, focus di `base.css`; i suoi locali (`--forum-navy`, `--forum-gold`…) sono mappati sullo shim e spariscono con esso |
| `apps/orientation/static/orientation/wizard.css` | `templates/orientation/start.html`, `templates/orientation/step.html`, `templates/orientation/result.html`, `templates/orientation/resume.html`, `templates/orientation/save_unavailable.html` | conforme dal 20 settembre 2026 (G-22 chiusa): solo token esistenti, focus del sistema |
| `apps/orientation/static/orientation/wizard.js` | `templates/orientation/step.html`, `templates/orientation/result.html` | modulo ES: mostra il bottone di stampa (`.js-print`, nascosto senza JS) e, dopo uno swap HTMX, porta il focus sulla nuova domanda. HTMX non è incluso nel progetto: oggi quel ramo non scatta mai e il wizard funziona con ricariche complete |

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
| `--track-caps-display` | `0.03em` | — | una lastra in maiuscolo, al massimo una per pagina (0 in arabo) |

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
| `--rank-c-block` | `var(--s-8)` | 32 px a `xs`, 48 px da `lg` | padding verticale di una sezione di rango C |
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
| `--z-drawer` | `30` | — | il drawer di navigazione e il suo velo |
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
| `@media (prefers-reduced-motion: reduce)` | `--motion-fast`, `--motion-base`, `--motion-slow` → `0ms` | Ogni transizione costruita sui token diventa istantanea. Lo shim propaga l'azzeramento ai nomi legacy `--duration-fast/base/slow` (§17); `components.css` §29 aggiunge la rete di sicurezza `transition-duration: 0.01ms !important` (§12) |

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

Rapporti **ricalcolati dal test** a partire dai valori letterali di `static/css/tokens.css` con la
formula di luminanza relativa WCAG 2.x (lo stesso algoritmo di `tests/frontend/test_static_assets.py`).
Requisito: **4.5** = testo normale (SC 1.4.3), **3.0** = componenti dell'interfaccia e oggetti grafici
(SC 1.4.11), **—** = elemento decorativo senza requisito.
`tests/frontend/test_design_docs.py::test_contrast_table_matches_recomputed_ratios` ricalcola ogni
riga con tolleranza ± 0.05 e verifica anche che l'esadecimale scritto qui sia quello che il token
risolve davvero;
`tests/frontend/test_design_docs.py::test_contrast_table_covers_every_pair_locked_by_the_asset_tests`
pretende che ognuna delle 29 coppie bloccate da
`tests/frontend/test_static_assets.py::test_wcag_contrast` compaia qui **con la stessa soglia**.

Ogni figura è calcolata contro il fondo nominato sulla riga. Le terne di stato sono state
**riverificate contro `--paper` `#faf7f0`** quando il fondo si è spostato: `--state-warn-br` è stato
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


Regole d'uso che derivano dalla tabella:

- `--rubric` è **sicuro come testo a qualunque corpo** (6.92:1 sulla carta, 6.23:1 sul fondo di
  processo): un ordinale in rubrica non ha bisogno di essere `aria-hidden` per ragioni di contrasto.
  È l'opposto del bronzo che sostituisce, che a 3.83:1 non poteva essere testo.
- `--rubric-on-navy` (4.46:1) è **solo filetto, mai testo**: supera la soglia degli oggetti grafici
  e non quella del testo. La regola vale alla lettera in tutto `static/css/`: le cinque
  dichiarazioni che lo consumano sono tutte `border-color` o `border-block-*`. Lo era stata violata
  in un punto — `.plate--verso .folio__ordinal` lo usava come `color`, e l'ordinale del folio è
  testo reso, sotto i 24 px a `xs` e `sm` — ed è stata corretta il 21/09/2026 (**G-27, chiusa**):
  dentro una fascia verso il numerale è `--paper-on-navy` e la rubrica resta il solo filetto.
- `--rule-hair` (1.42:1) e `--paper-edge` (1.25:1) sono **decorativi**: non possono essere l'unico
  indicatore del perimetro di un controllo. Il perimetro dei campi usa `--rule-ink` (3.50:1 sulla
  carta, 3.74:1 dentro il campo).
- L'anello di focus è `--navy` sui fondi chiari (13.62:1) e `--paper-on-navy` dentro `.on-inverse` /
  `.surface-inverse` (13.62:1 sul navy). Entrambe le tonalità sono molto sopra la soglia di 3:1, ed è
  voluto: l'anello deve restare leggibile anche sopra una zebratura o una terna di stato.
- Le terne di stato superano 3:1 sul fondo di pagina anche nel solo bordo: il perimetro di un notice
  resta percepibile senza il colore di riempimento. Il margine più stretto è `--state-pending-br`
  (3.16:1); il secondo è `--state-warn-br` (3.32:1). Un nuovo valore di stato va verificato contro
  **`--paper`**, non contro il bianco.
- I controlli disabilitati (`opacity: 0.55`) sono esenti da SC 1.4.3.

---

## 6. Tipografia

### 6.1 Famiglie — e perché non le precedenti

| Ruolo | Token | Famiglia | Licenza | Uso |
|---|---|---|---|---|
| Display e testo corrente, latino | `--font-display` | Newsreader → Iowan Old Style → Palatino Linotype → Georgia → serif | SIL Open Font License 1.1 | `h1`–`h3`, `.t-plate`, `.t-lead`, **il corpo del testo**, il wordmark, gli ordinali |
| Interfaccia, latino | `--font-ui` (= `--f-sans` da V4) | IBM Plex Sans → IBM Plex Sans Arabic → Segoe UI → system-ui → sans-serif | SIL Open Font License 1.1 | bottoni, navigazione, etichette, celle di tabella, glosse, didascalie, folio; con il foglio tipografico V4 anche il corpo pubblico e tutta la console |
| Display e testo corrente, arabo | `--font-display-ar` | Noto Naskh Arabic → Newsreader → serif | SIL Open Font License 1.1 | sotto `:lang(ar)` sostituisce `--font-display` |
| Interfaccia, arabo | `--font-ui-ar` | IBM Plex Sans Arabic → IBM Plex Sans → sans-serif | SIL Open Font License 1.1 | sotto `:lang(ar)` sostituisce `--font-ui` |
| Codici e riferimenti | `--font-ref` (= `--f-mono` da V4) | IBM Plex Mono → ui-monospace → Cascadia Mono → Consolas → monospace | SIL Open Font License 1.1 | `code`, `kbd`, `pre`, `.t-ref`, riferimenti di pratica |

**Design V4 (24/09/2026).** L'interfaccia latina è **IBM Plex Sans** e i riferimenti sono **IBM Plex
Mono** (`docs/design-v4/DESIGN_SYSTEM_V4.md` §4.1): il latino e l'arabo dell'interfaccia — IBM Plex Sans
Arabic era già vendorizzato — diventano una sola superfamiglia, con la stessa altezza dell'occhio, la
stessa logica dei pesi e le stesse cifre tabellari; Fira Sans e Fira Mono sono ritirati con i loro dieci
file. La ragione contro Plex qui sotto (ADR-008) resta vera per il **display** — Plex non ha asse ottico
né maiuscoletto, e per questo Newsreader resta la voce pubblica dei titoli, del lead e del wordmark — e
non vale più per l'interfaccia, dove i terminali squadrati e le `tnum` di Plex leggono «strumento» a
13–15 px. I file latini di Plex vengono dai pacchetti npm `@fontsource/ibm-plex-sans` e
`@fontsource/ibm-plex-mono` 5.3.0 (OFL 1.1, gli stessi sottoinsiemi `unicode-range` dell'API di Google),
copiati da `node_modules` con `scripts/fetch_fonts.py --from-fontsource`. `v4/tokens.css` ripunta
`--font-ui`, `--font-ref` e `--font-mono` su `--f-sans` / `--f-mono`, così i livelli 1–7 cambiano faccia
insieme; lo spostamento del corpo pubblico dal serif al sans (V4 §4.2) arriva con il foglio tipografico
V4, non con i token.

**ADR-008 è superata, e va detto per esteso.** ADR-008 giustificava IBM Plex come «una voce
istituzionale europea, distinta da gov.it (Titillium)»: il criterio dichiarato era *evitare gov.it*,
non *ottenere una distinzione*. IBM Plex è stato commissionato da IBM come voce aziendale di
un'impresa tecnologica ed è la superfamiglia aperta «seria» più diffusa dell'ultimo decennio — è la
proposta di default di quasi ogni strumento a cui si chieda un accostamento istituzionale open, ed è
il meccanismo dietro la frase del committente. Oltre al gusto, tre carenze concrete e misurabili:

1. **nessun asse di dimensione ottica**: gli stessi contorni andavano da 12 px a 64 px, un intervallo
   di 5.3×, ed è la ragione per cui l'H1 a 48 px si leggeva molle e gonfio;
2. **nessun vero maiuscoletto** in nessuna famiglia Plex, quindi il sistema sostituiva
   `text-transform: uppercase` a 12 px con 0.12em di tracking in 22 regole — l'eyebrow SaaS che il
   committente ha vietato;
3. **solo cifre lineari**, quindi le date bucavano il testo in minuscolo.

In più `--font-mono: "IBM Plex Mono"` era dichiarato senza che esistesse un solo file Plex Mono: il
registro tecnico era Consolas su Windows e Menlo su macOS, tre texture per un ruolo (lacuna G-15,
**chiusa**: `--font-ref` nomina Fira Mono, che è self-hosted).

**Newsreader** porta un vero asse `opsz` in un solo file: la lastra da 88 px e la prosa da 17 px sono
*disegni diversi*, che è esattamente la carenza qui sopra. È disegnato per la lettura a schermo con
un'altezza dell'occhio ampia, ed è ciò che permette la mossa centrale della direzione: **il testo
corrente è nel serif, non nel sans**. Ha corsivi veri e copertura Latin-Extended completa per i
diacritici francesi e italiani. Se fallisce il cancello di leggibilità a 1× DPR (§6.4), si alza il
corpo a 18/30 e si rimisura la colonna: **non** si torna al sans, perché sarebbe una variante di
colore della build respinta.

**Fira Sans** (ritirato con V4) aveva uno scheletro umanista disegnato per un'interfaccia a corpi
piccoli; leggeva «documentazione» dove la console V4 chiede «strumento». Restano esclusi Inter, Source
Sans, Public Sans, Work Sans e Roboto (tutti anonimi) e Titillium Web (impersonificazione, §1.2).

**Noto Naskh Arabic** è il controparte corretto di un serif latino ed è il registro dei documenti
amministrativi marocchini. IBM Plex Sans Arabic **resta**, come faccia d'interfaccia araba: è già
sottoinsiemata, è già accoppiata per peso entro il 3 %, e il suo compito qui sono etichette, bottoni,
tabelle e moduli, dove una costruzione kufica è corretta. Nel sistema ritirato faceva *tutti e sei* i
livelli arabi, quindi l'edizione araba non aveva alcun contrasto display/testo.

Pesi disponibili: Newsreader è variabile 200–800 (tondo e corsivo), IBM Plex Sans ha 400/500/600 più il
corsivo 400, IBM Plex Sans Arabic 400/500/600, Noto Naskh Arabic è variabile 400–700, IBM Plex Mono 400.
`font-synthesis: none` è dichiarato globalmente su `html` in `base.css`: **nessun falso grassetto,
nessun falso corsivo, in nessuno script**. Un peso mancante deve fallire in modo visibile invece di
sbavare le giunzioni di una faccia araba; per questo il peso 700 è vietato in arabo
sull'interfaccia, dove sono sottoinsiemati solo 400/500/600.

### 6.2 File self-hosted (`static/fonts/`, 26 file woff2, ≈ 965 KB in totale)

Sottoinsiemi `latin`, `latin-ext`, `arabic`, selezionati dal browser tramite `unicode-range`: una
pagina in francese scarica tipicamente Newsreader tondo latin più IBM Plex Sans 400/500/600 latin; una
pagina in arabo i file `arabic` di Noto Naskh e di Plex Sans Arabic. Il totale su disco non è il peso
di una pagina: nessuna pagina scarica corsivi, `latin-ext` e `arabic` insieme.

| File | Famiglia | Peso · stile | Sottoinsieme | KB |
|---|---|---|---|---|
| `ibm-plex-mono-400-normal-latin-ext.woff2` | IBM Plex Mono | 400 · tondo | latin-ext | 13.0 |
| `ibm-plex-mono-400-normal-latin.woff2` | IBM Plex Mono | 400 · tondo | latin | 14.4 |
| `ibm-plex-sans-400-italic-latin-ext.woff2` | IBM Plex Sans | 400 · corsivo | latin-ext | 16.6 |
| `ibm-plex-sans-400-italic-latin.woff2` | IBM Plex Sans | 400 · corsivo | latin | 23.8 |
| `ibm-plex-sans-400-normal-latin-ext.woff2` | IBM Plex Sans | 400 · tondo | latin-ext | 15.6 |
| `ibm-plex-sans-400-normal-latin.woff2` | IBM Plex Sans | 400 · tondo | latin | 22.1 |
| `ibm-plex-sans-500-normal-latin-ext.woff2` | IBM Plex Sans | 500 · tondo | latin-ext | 16.1 |
| `ibm-plex-sans-500-normal-latin.woff2` | IBM Plex Sans | 500 · tondo | latin | 23.6 |
| `ibm-plex-sans-600-normal-latin-ext.woff2` | IBM Plex Sans | 600 · tondo | latin-ext | 16.1 |
| `ibm-plex-sans-600-normal-latin.woff2` | IBM Plex Sans | 600 · tondo | latin | 23.7 |
| `ibm-plex-sans-arabic-400-normal-arabic.woff2` | IBM Plex Sans Arabic | 400 · tondo | arabic | 41.8 |
| `ibm-plex-sans-arabic-400-normal-latin-ext.woff2` | IBM Plex Sans Arabic | 400 · tondo | latin-ext | 6.5 |
| `ibm-plex-sans-arabic-400-normal-latin.woff2` | IBM Plex Sans Arabic | 400 · tondo | latin | 18.7 |
| `ibm-plex-sans-arabic-500-normal-arabic.woff2` | IBM Plex Sans Arabic | 500 · tondo | arabic | 44.2 |
| `ibm-plex-sans-arabic-500-normal-latin-ext.woff2` | IBM Plex Sans Arabic | 500 · tondo | latin-ext | 6.4 |
| `ibm-plex-sans-arabic-500-normal-latin.woff2` | IBM Plex Sans Arabic | 500 · tondo | latin | 19.6 |
| `ibm-plex-sans-arabic-600-normal-arabic.woff2` | IBM Plex Sans Arabic | 600 · tondo | arabic | 44.6 |
| `ibm-plex-sans-arabic-600-normal-latin-ext.woff2` | IBM Plex Sans Arabic | 600 · tondo | latin-ext | 6.5 |
| `ibm-plex-sans-arabic-600-normal-latin.woff2` | IBM Plex Sans Arabic | 600 · tondo | latin | 20.0 |
| `newsreader-200-800-italic-latin-ext.woff2` | Newsreader | variabile 200–800 · corsivo | latin-ext | 93.3 |
| `newsreader-200-800-italic-latin.woff2` | Newsreader | variabile 200–800 · corsivo | latin | 143.4 |
| `newsreader-200-800-normal-latin-ext.woff2` | Newsreader | variabile 200–800 · tondo | latin-ext | 84.6 |
| `newsreader-200-800-normal-latin.woff2` | Newsreader | variabile 200–800 · tondo | latin | 128.9 |
| `noto-naskh-arabic-400-700-normal-arabic.woff2` | Noto Naskh Arabic | variabile 400–700 · tondo | arabic | 91.8 |
| `noto-naskh-arabic-400-700-normal-latin-ext.woff2` | Noto Naskh Arabic | variabile 400–700 · tondo | latin-ext | 10.1 |
| `noto-naskh-arabic-400-700-normal-latin.woff2` | Noto Naskh Arabic | variabile 400–700 · tondo | latin | 19.2 |

I tre `ibm-plex-sans-400/500/600-normal-latin.woff2` di oggi non sono quelli del sistema ritirato — che
erano tre copie byte-identiche dello stesso file variabile (45 712 byte ciascuna), 153 KB di payload
inutile — ma tre istanze statiche distinte del pacchetto `@fontsource/ibm-plex-sans` 5.3.0 (22.1 /
23.6 / 23.7 KB).

**Il budget del percorso latino.** AD-A §3.7.6 fissa un tetto di **320 KB**; Newsreader tondo latin
(128.9) più IBM Plex Sans 400/500/600 latin (69.4) fa 198.3 KB e sta dentro. Una riga in
corsivo nel serif aggiunge 143.4 KB, un'enfasi (`em`, `cite`) nel sans 23.8 KB — il corsivo di Plex Sans
ha un consumatore reale, perché `font-synthesis: none` non lo inclina per finta — e un accento fuori
dal sottoinsieme `latin` 15.6 KB per peso.

### 6.3 Licenza

Tutte e cinque le famiglie sono distribuite con **SIL Open Font License 1.1**: uso, incorporazione e
ridistribuzione (anche in formato woff2 e in sottoinsiemi) sono consentiti; i font non possono essere
venduti da soli; i nomi riservati non possono essere usati per versioni modificate. Newsreader è di
Production Type, Noto Naskh Arabic di Google, IBM Plex Sans, IBM Plex Mono e IBM Plex Sans Arabic di
IBM Corp. (Mike Abbink con Bold Monday). I file di Newsreader, Noto Naskh Arabic e Plex Sans Arabic
sono i sottoinsiemi woff2 pubblicati dalla Google Fonts CSS API, scaricati **una sola volta** da
`scripts/fetch_fonts.py` (unico punto del repository in cui compaiono gli host di Google); quelli di
Plex Sans e Plex Mono vengono dai pacchetti npm `@fontsource/ibm-plex-sans` e `@fontsource/ibm-plex-mono`
5.3.0 (devDependencies, copiati da `node_modules` con `--from-fontsource`). Tutti serviti dal nostro dominio:
nessuna richiesta a terzi in runtime (CSP `font-src 'self'`; lo scanner `apps/cms/forbidden.py` vieta
gli host dei font esterni nelle pagine; test
`tests/frontend/test_layout.py::test_fonts_css_references_only_local_files_that_exist` e
`tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded`).

### 6.4 Strategia di caricamento e cancelli di QA

- `font-display: swap` su tutte le 26 facce: il testo è subito leggibile nel fallback di sistema e
  viene ridisegnato all'arrivo del woff2 (nessun FOIT).
- `unicode-range` per sottoinsieme: `latin-ext` e `arabic` vengono scaricati solo se la pagina
  contiene quei caratteri.
- Stack di fallback metricamente vicini (Georgia per il serif, Segoe UI / system-ui per il sans) per
  contenere lo spostamento di layout allo swap.
- **Preload mirato** in `templates/base.html`, per direzione: le pagine LTR precaricano
  `newsreader-200-800-normal-latin.woff2` (il serif di lettura, quindi l'LCP) e
  `ibm-plex-sans-400-normal-latin.woff2` (l'interfaccia, e con V4 il corpo); le pagine RTL precaricano
  `noto-naskh-arabic-400-700-normal-arabic.woff2` e
  `ibm-plex-sans-arabic-400-normal-arabic.woff2`. **G-24, chiusa il 21/09/2026**: subito dopo la
  redirezione le due righe LTR nominavano ancora `ibm-plex-sans-400-normal-latin.woff2` e
  `ibm-plex-serif-500-normal-latin.woff2` — due file che la redirezione aveva cancellato — quindi
  ogni pagina LTR pagava due 404 e nessun preload utile. Il test confronta ogni `preload` di
  `templates/base.html` con i file realmente presenti in `static/fonts/`, così il difetto non può
  tornare in silenzio.

I sei cancelli di QA tipografica della direzione sono **bloccanti di rilascio** e vanno eseguiti in
Chromium prima di congelare la scala: (1) l'asse `opsz` è davvero applicato fra `.t-plate` e
`.t-prose`; (2) `font-variant-caps: small-caps` produce veri maiuscoletti, altrimenti il registro
`.t-folio` resta maiuscolo tracciato e nessuna classe di maiuscoletto viene definita; (3)
`font-variant-numeric: oldstyle-nums` cambia davvero i glifi, altrimenti la prosa usa le lineari e il
token si **cancella** invece di restare inerte; (4) parità d'inchiostro latino/arabo entro il 5 % a
100 px per 400/500/600 — la coppia precedente raggiungeva il 3 % e uno scambio non deve regredire;
(5) leggibilità del serif a 17 px su un display 1× al 100 % di zoom e su un Android di fascia media;
(6) payload (§6.2).

### 6.5 I dieci ruoli e la scala per fascia

Dieci ruoli più l'ordinale del rail. Quattro display, quattro di testo, due d'interfaccia. Ogni
interlinea è un multiplo di 4 px. **Il corpo del testo non cambia mai dimensione fra i breakpoint**:
cambiano solo le dimensioni display e la misura. Nessun `clamp()` su display e contenitori: le
dimensioni **scattano** ai breakpoint, così il rapporto è progettato a ogni larghezza.

| Ruolo | Classe | xs 320–429 | sm 430–767 | md 768–1199 | lg 1200–1439 | xl 1440–1599 | xxl ≥1600 | Famiglia, peso, asse |
|---|---|---|---|---|---|---|---|---|
| lastra | `.t-plate` | 40/44 | 46/52 | 60/64 | 76/80 | 88/92 | 104/108 | Newsreader 400, `opsz` 72, `--track-plate` |
| titolo | `h1`, `.t-title` | 32/40 | 34/40 | 42/48 | 48/52 | 52/56 | 52/56 | Newsreader 400, `opsz` 48, `--track-title` |
| banda | `h2`, `.t-band` | 28/36 | 28/36 | 32/40 | 36/44 | 38/44 | 38/44 | Newsreader 400, `opsz` 36, `--track-band` |
| entrata | `h3`, `.t-entry` | 20/28 | 20/28 | 21/28 | 22/28 | 22/28 | 22/28 | Newsreader 500, `opsz` 24, tracking 0 |
| standfirst | `.t-lead`, `.lead` | 19/28 | 20/28 | 21/32 | 22/32 | 22/32 | 22/32 | Newsreader 400, `opsz` 24 |
| prosa | `body`, `.t-prose` | 17/28 | 17/28 | 17/28 | 17/28 | 17/28 | 17/28 | Newsreader 400, `opsz` 18 |
| glossa | `.t-gloss` | 15/24 | 15/24 | 15/24 | 15/24 | 15/24 | 15/24 | Fira Sans 400 |
| didascalia | `.t-caption`, `figcaption`, `small` | 13/20 | 13/20 | 13/20 | 13/20 | 13/20 | 13/20 | Fira Sans 400 |
| interfaccia | `.t-ui` | 15/20 | 15/20 | 15/20 | 15/20 | 15/20 | 15/20 | Fira Sans 500 |
| folio | `h4`, `h5`, `h6`, `.t-folio` | 13/16 | 13/16 | 13/16 | 13/16 | 13/16 | 13/16 | Fira Sans 600, `--track-folio`, maiuscolo |
| ordinale | `.t-numeral` | 22/24 | 24/24 | 28/32 | 40/40 | 44/44 | 44/44 | Newsreader 400, cifre tabulari |

**I rapporti che questa scala produce.** A 1440: lastra:banda = 2.32, **banda:prosa = 2.24**,
banda:glossa = 2.53, entrata:prosa = 1.29. A 390: **banda:prosa = 1.65**. La build respinta misurava
banda:prosa = 2.11 a 1440 solo perché la sua «prosa» era un sans da 16 px; contro il proprio lead da
21 px valeva 1.61, e a 390 crollava a 1.35. Pavimenti di riferimento: .italia porta l'H2 a 40 px
sopra un corpo di 16–18 px (≥ 2.2×); ECL 36 px su 16 px = 2.25× a peso 400.

**Quattro livelli di titolo al massimo per pagina** (.italia, adottata alla lettera): `plate` o
`title` (h1) → `band` (h2) → `entry` (h3) → e un'etichetta `.t-folio` facoltativa nel ruolo di h4.
Una pagina che ha bisogno di un quinto livello ha un problema di architettura dell'informazione, non
di tipografia. Per questo `h4`, `h5` e `h6` **sono** il folio in `base.css`: il vecchio
`--font-size-h4` valeva 18 px fissi, cioè *meno del lead* a 1440 e a 768 — un quarto livello di
titolo più piccolo di un paragrafo.

**Token cancellati dalla scala precedente**, con il loro compito assorbito: `--font-size-h4`,
`--font-size-label`, `--font-size-button`, `--font-size-legal`, `--font-size-small`,
`--font-size-eyebrow`. Quattro di questi portavano valori duplicati (14/14, 15/15). I loro compiti
sono di `--t-ui-size`, `--t-caption-size` e `--t-folio-size`. Finché i template non sono riscritti,
i vecchi nomi esistono nello shim e puntano ai nuovi (§17).

### 6.6 Misura e interlinea

L'interlinea è legata alla **misura**, non a un nome di stile. Il sistema ritirato faceva l'opposto:
il lead da 21 px a 45–57 caratteri riceveva 1.7, mentre una definizione da 16 px a **147 caratteri**
riceveva 1.6 e il testo legale da 14 px un 1.55 scritto a mano.

| Misura | Corpo | Interlinea | Token |
|---|---|---|---|
| ≤ 45 caratteri (standfirst) | 19–22 px | 28–32 px (1.45 a `md`+) | `--measure-lead` |
| 62–68 caratteri (prosa) | 17 px | 28 px (1.65) | `--measure-prose` |
| ≤ 50 caratteri (glossa dentro un'entrata) | 15 px | 24 px (1.60) | `--measure-gloss` |
| ≤ 34 caratteri (nota marginale) | 13 px | 20 px (1.54) | `--measure-note` |
| cella di tabella | 15 px | 24 px | — |

**Tetto rigido: 68 caratteri ovunque, nessuna eccezione.** `--measure-prose` è espressa in `ch` e
resta in `ch` per ora; AD-A §2.3 chiede di convertirla in un valore in pixel misurato sull'avanzamento
medio del minuscolo di Newsreader a 17 px in Chromium, perché il vecchio `68ch` rendeva 81 caratteri
con Plex Sans — una scalibrazione del 19 %. La conversione è nel cancello di QA §6.4 e non è ancora
stata eseguita: finché non lo è, `--measure-prose` è un tetto conservativo, non una misura calibrata.

`layout.css` applica la misura dove serve senza che l'autore debba ricordarsene: la prosa dentro
`.zones__content` riceve `--measure-prose`, `.section__header` riceve `--measure-lead`,
`.zones__margin` riceve `--measure-note`.

### 6.7 I due registri di maiuscole

**La capitalizzazione è una decisione CSS, mai una decisione di contenuto.** Nel sistema ritirato 22
titoli erano digitati in maiuscolo nel catalogo `.po` con `text-transform: none` calcolato, tracciati
a −0.48 px, −0.34 px, +0.65 px, +1.04 px o +1.63 px a seconda del file che li stilava: la stessa
stringa compariva a 33.76 px / −0.34 px su una pagina e a 27.2 px / +1.63 px su un'altra. Ogni
stringa maiuscola torna in minuscolo nei cataloghi, e il disegno riceve esattamente **due** registri
maiuscoli:

1. **`.t-folio`** — 13 px Fira Sans 600, `--track-folio`, maiuscolo, `font-feature-settings: "case" 1`.
   Il titolo corrente, la pastiglia di stato, l'intestazione di tabella, l'etichetta dell'attore
   responsabile. È **l'unico oggetto a maiuscole tracciate del sistema**, e in `base.css` è
   letteralmente `h4, h5, h6, .t-folio`.
2. **`.t-plate--caps`** — una riga display in maiuscolo, `--track-caps-display`,
   `font-feature-settings: "case" 1`, ammessa **al massimo una volta per pagina** e solo su una
   lastra.

In arabo entrambi i registri perdono maiuscolo e tracking (`base.css`: `:lang(ar) :is(h4, h5, h6,
.t-folio)`), perché l'arabo non ha cassa e il tracking spezza le legature. Il registro è portato dal
peso 600 e da un filetto (§15.2).

### 6.8 Cifre

Una sola regola in `base.css`, agganciata a ciò che porta davvero dati:
`td`, `th`, `time[datetime]`, `.t-numeral`, `.t-ref`, `.folio__ordinal`, `.entry__ordinal` ricevono
`font-variant-numeric: lining-nums tabular-nums`. Nel sistema ritirato la stessa cosa era fatta da
sette regole sparse fra i componenti e da nessuna regola nei tre fogli delle app che rendono dati
veri.

`code`, `kbd`, `pre` e `.t-ref` usano `--font-ref` con `slashed-zero lining-nums tabular-nums`: lo
zero barrato serve sui codici di riferimento, dove `0` e `O` devono essere distinguibili a voce.

Cifre lineari e tabulari in ogni tabella e in ogni ordinale; cifre di stile antico (`onum`) nel testo
corrente **solo se il cancello §6.4.3 conferma che la faccia le fornisce**. In arabo si usano le
cifre occidentali (corretto per il Marocco), isolate LTR con `<bdi>`.

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
| `64rem` | 1024 | — | `.layout-sidebar` a due colonne con aside sticky, navigazione locale in colonna, varianti `.lg:col-*`, footer a 4 colonne, `.hide-mobile` / `.hide-desktop` |
| `72rem` | 1152 | — | `.entrances` a 4 colonne |
| `75rem` | 1200 | `lg` | **il rail del folio diventa verticale** (176 px) e il contenitore si fissa a 1176 px; lastra 76/80, titolo 48/52, banda 36/44, ordinale 40/40; ranghi A e B a 96 px, C a 48 px, D a 32 px |
| `80rem` | 1280 | — | **navigazione desktop** (mega-menu al posto del drawer, bottone «Menu» nascosto), timeline a 8 in riga |
| `90rem` | 1440 | `xl` | contenitore 1320 px, rail 200 px; lastra 88/92, titolo 52/56, banda 38/44, ordinale 44/44 |
| `100rem` | 1600 | `xxl` | contenitore 1440 px, rail 220 px; lastra 104/108 |

Media query «solo sotto»: `max-width: 23rem` (368 px: la parola «Menu» del bottone di navigazione
diventa solo per screen reader — a 320 px il marchio, che non si riflette per scelta, più il bottone
con la parola non entravano in 265 px di contenuto; la soglia è 23rem e non 20rem perché la parola
deve sparire *prima* che il bottone tocchi il bordo, non nel momento in cui lo tocca),
`max-width: 47.99rem` (`portal.css`: pop-in delle tabelle che portano `data-label`, §14.5 della
direzione artistica), `max-width: 47.999rem` (etichetta del link «Espace réservé» solo per screen
reader, freccia della pathway list nascosta), `max-width: 63.999rem` (`.hide-mobile`, navigazione
locale a pastiglie) e `max-width: 79.999rem` (drawer). Sotto `lg` il rail vale 0 px e il folio
diventa una linea orizzontale sopra il blocco: il dispositivo sopravvive a ogni larghezza, cambia
solo il suo asse.

**La navigazione ha un breakpoint proprio (80rem), che non è una fascia della griglia.** Con il menu
completo di Fase 3, sette voci di primo livello non entrano accanto al wordmark sotto 1280 px. La
soglia vive in tre punti che devono restare allineati: `@media (min-width: 80rem)` e
`@media (max-width: 79.999rem)` in `components.css` §7, e
`DESKTOP = window.matchMedia("(min-width: 80rem)")` in `static/js/main.js`
(`tests/frontend/test_design_docs.py::test_navigation_breakpoint_is_consistent_and_documented`).
Conseguenze: un tablet in orizzontale e un laptop da 1024–1279 px usano il drawer; «mobile» in
`.hide-mobile` significa «sotto 64rem», non «modalità drawer»; a 1280 px qualunque zoom del browser
oltre il 100 % riporta al drawer.

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
filetto navy da 2 px in apertura e filetto `--rubric-on-navy` da 2 px in chiusura), `.section--rule`
(filetto `--rule-hair` superiore). Gli alias `.section--tight`, `.section--muted` e
`.section--inverse` appartengono all'impalcatura di demolizione e risolvono sui ranghi e sui fondi
nuovi (§17).

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

---

## 8. Il linguaggio grafico proprio

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
`.plate` e `.plate--verso` sono in `register.css`; `.section--verso` in `layout.css` è la stessa
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
colorata — e `.state`, la pastiglia dei sette stati visibili del documento (MANCANTE · DEPOSITATO ·
IN ESAME · VALIDO · NON VALIDO · SCADUTO · DA SOSTITUIRE), che porta la parola nel registro del
folio più un filetto, mai il solo colore.

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

35 file. Ogni componente è un include Django senza logica di business: riceve variabili di contesto
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
  markup diretto), `dialog.html`, `hero.html`, `institutional_banner.html`, `metadata_row.html` e
  `tabs.html`: per questi l'esempio è ricavato dal contratto ed è dichiarato come tale.

#### `accordion.html`

- **Scopo**: domande/risposte e sezioni richiudibili; `<details>`/`<summary>` nativi.
- **Blocco CSS**: `.accordion` (`.accordion__item`, `.accordion__summary`, `.accordion__body`).
- **Contratto**: `items` = lista di dict `{id, title, body (HTML sicuro), open (bool), lang}`; `single`
  (True → un solo pannello aperto: attributo `name` nativo + fallback JS `data-accordion="single"`);
  `group` (valore di `name` quando `single`, default `accordion`).
- **Varianti**: nessun modificatore; l'icona `plus` ruota di 45° quando `[open]`.
- **Accessibilità**: ruolo, stato espanso/chiuso e tastiera (Invio/Spazio) forniti dal browser;
  funziona senza JS; `summary` alto almeno 56 px; `id` per item → permalink `#id`.
- **Usato in**: `templates/faq/_item.html`, `templates/faq/index.html` (markup diretto; usa
  `.accordion__panel` al posto di `.accordion__body` — G-19).
- **Esempio (dal contratto — nessun `{% include %}`)**:

```django
{% include "components/accordion.html" with items=faq_items single=True group="faq-general" %}
```

#### `account_menu.html`

- **Scopo**: menu dell'utente autenticato nella barra istituzionale.
- **Blocco CSS**: `.account-menu` (`__summary`, `__name`, `__list`, `__link`, `__sep`).
- **Contratto**: nessuna variabile; legge `user` dal contesto. Le voci compaiono solo se la route
  esiste: `portal:dashboard`, `accounts:profile`, `mfa_index`, `account_logout` (via `safe_url`).
- **Varianti**: nessuna.
- **Accessibilità**: `<details data-dropdown>`; `main.js` sincronizza `aria-expanded` sul `summary`,
  chiude con Esc (focus di ritorno al `summary`), al click esterno e alla perdita di focus. Il logout
  è un `<form method="post">` con CSRF e un vero `<button>`, non un link GET. Il nome lungo è troncato
  con ellissi — **da correggere**: `text-overflow: ellipsis` è vietato su testo d'identità,
  giuridico e di navigazione (§11.1).
- **Usato in**: `templates/partials/utility_bar.html`, `templates/partials/header.html` (in testa al
  cassetto, design V4), `templates/partials/portal_chrome.html`.
- **Esempio reale — `templates/partials/utility_bar.html`**:

```django
{% if user.is_authenticated %}
  {% include "components/account_menu.html" %}
```

#### `badge.html`

- **Scopo**: etichetta di stato compatta (una riga, `white-space: nowrap`).
- **Blocco CSS**: `.badge`.
- **Contratto**: `label`; `kind` ∈ `neutral | info | success | warning | error | pending | primary`
  (opzionale); `icon` (nome icona, opzionale).
- **Varianti**: `.badge--info`, `.badge--success`, `.badge--warning`, `.badge--error`,
  `.badge--pending`, `.badge--primary`. `neutral` non ha regola propria: è l'aspetto di base.
  **`success` non è più verde**: lo shim lo fa risolvere alla terna `--state-done-*`, che è blu
  (§4.3). Il nome del modificatore va rinominato in `--done` con la migrazione.
- **Accessibilità**: il significato è nel testo, mai nel solo colore; ogni coppia fg/bg supera
  7.2:1 (§5).
- **Usato in**: `templates/portal/messages.html`, `templates/portal/requests.html`,
  `templates/portal/request_detail.html`, `templates/portal/partials/card.html`,
  `templates/portal/partials/deadline_item.html` (include); `templates/accounts/profile.html`,
  `templates/community/discussion.html`, `templates/community/initiatives.html`,
  `templates/community/room.html`, `templates/pathways/detail.html`,
  `templates/pathways/diplomas.html`, `templates/allauth/elements/badge.html` (markup diretto
  `<span class="badge …">`).
  La tabella dei documenti dell'area riservata non è più fra i consumatori: porta lo stato in una
  colonna di testo, non in un'etichetta. (Il percorso non è citato fra apici inversi di proposito —
  il test legge ogni percorso citato nella riga come un consumatore da verificare.)
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
- **Usato in**: `templates/ecosystem/companies.html` (il testo prescritto e la sua lingua effettiva
  sono risolti da `ecosystem.services` tramite il registro, mai copiati nel template).
- **Esempio reale — `templates/ecosystem/companies.html`**:

```django
{% include "components/blockquote.html" with text=quote.text lang=quote.lang_attr %}
```

#### `breadcrumbs.html`

- **Scopo**: filo d'Arianna sotto l'header (blocco `breadcrumbs` di `base.html`).
- **Blocco CSS**: `.breadcrumbs` (il componente include già `.container`).
- **Contratto**: `breadcrumbs` = lista di `{"label": str, "url": str | ""}` fornita dalla view;
  l'ultimo elemento è la pagina corrente. «Accueil» è aggiunto automaticamente (`pages:home`).
- **Varianti**: nessuna. I separatori sono chevron disegnati in CSS (bordi ruotati), specchiati in
  RTL.
- **Accessibilità**: `<nav aria-label="Fil d’Ariane">` + `<ol>`; ultimo elemento `aria-current="page"`
  e non linkato; i separatori non sono contenuto.
- **Sotto la direzione A**: il breadcrumb va derivato **dallo stesso albero di menu della
  navigazione**, presente solo a profondità ≥ 2, e reso a `--t-folio-size` dentro il rail da `lg` in
  su. Uno stub a un livello `Accueil > Contact` è peggio di niente, ed è ciò che ogni pagina rende
  oggi.
- **Usato in**: `templates/accounts/profile.html`, `templates/faq/index.html`,
  `templates/forum/index.html`, `templates/pathways/index.html`, `templates/news/index.html` (e almeno
  altri 30 template; 34 al momento dell'ultima verifica — il consolidamento dei template dell'area
  riservata ne ha tolti tre, e la soglia è scritta con margine perché è un minimo, non un conteggio).
- **Esempio reale — `templates/accounts/profile.html`**:

```django
{% block breadcrumbs %}{% include "components/breadcrumbs.html" %}{% endblock %}
```

#### `card.html`

- **Scopo**: teaser (notizie, schede). **In uscita**: la direzione A la sostituisce con l'entrata
  (§8.4). Una card sopravvive solo se passa per intero il test del benchmark.
- **Blocco CSS**: `.card` (`__eyebrow`, `__title`, `__text`, `__meta`).
- **Contratto**: `title`; `url` (opzionale: l'intera card diventa cliccabile); `eyebrow`; `text`;
  `meta` (str o HTML sicuro); `lang`; `flat` (True → senza box, solo filetto superiore).
- **Varianti**: `.card--link` (automatica con `url`), `.card--flat`. Su hover/focus-within dichiara
  ancora `--shadow-sm`, che nel nuovo sistema vale `none`: resta il solo cambio di bordo, ed è il
  comportamento corretto. `.card--flat` è già la forma che sopravvive alla migrazione.
- **Accessibilità**: «stretched link» — lo pseudo-elemento del link del titolo copre la card, quindi
  c'è **un solo tab stop** e il nome accessibile è il titolo. Il titolo è sempre `<h3>`: collocare la
  card sotto un `h2`.
- **Usato in**: `templates/ecosystem/institutions.html`, `templates/ecosystem/companies.html`,
  `templates/ecosystem/pilot.html`, `templates/ecosystem/universities.html`,
  `templates/pages/home/_news.html` (include); `templates/pathways/training.html` (markup diretto
  `.card`).
- **Esempio reale — `templates/ecosystem/institutions.html`**:

```django
{% if links.partners %}<li>{% include "components/card.html" with flat=True url=links.partners title=_("Partenaires") text=_("Les organisations qui participent à l’écosystème.") %}</li>{% endif %}
```

#### `case_timeline.html`

- **Scopo**: la **Timeline** di un fascicolo (design V4, `CREATIVE_DIRECTION.md` §3.6.3, `DESIGN_SYSTEM_V4.md`
  §8.27): che cosa è accaduto, nell'ordine in cui è accaduto — letta dal registro di audit
  (`cases.presenters.timeline`), append-only, mai composta a mano. Nodo 12 px su una spina hairline, data
  tabellare, titolo dell'evento, lo stato prodotto come chip col suo registro, l'attore come TIPO («Vous», il
  ruolo tenuto sul fascicolo, l'équipe del progetto) — mai il nome di una persona. L'ultimo nodo si accende
  una volta al caricamento.
- **Blocco CSS**: `.tl` (`__row`, `__node`, `__when`, `__what`, `__title`, `__detail`, `__actor`; modificatore
  `--last`), in `v4/workspace.css`; keyframe `tl-light` (§12).
- **Contratto**: `rows` (`cases.presenters.timeline(case)`: when, title, detail, chip_label, chip_register,
  actor); `label` (opzionale, `aria-label` della lista).
- **Varianti**: nessuna.
- **Accessibilità**: `<ol role="list">`, la data è un `<time>`, il chip porta la parola; il nodo è decorativo;
  sotto `prefers-reduced-motion: reduce` l'ultimo nodo è semplicemente acceso.
- **Usato in**: `templates/cases/detail.html`.
- **Esempio reale — `templates/cases/detail.html`**:

```django
{% include "components/case_timeline.html" with rows=timeline %}
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
- **Usato in**: `templates/ecosystem/universities.html`, `templates/ecosystem/institutions.html`,
  `templates/ecosystem/pilot.html` (include, un solo pannello per pagina);
  `templates/pathways/_orientation_cta.html` (markup diretto `.cta-panel`).
- **Esempio reale — `templates/ecosystem/universities.html`** (l'etichetta del bottone è un testo
  prescritto, passato tramite `{% locked … as %}`):

```django
{% locked "p3.universities.button" as button_label %}
{% include "components/cta_panel.html" with title=_("Proposer un partenariat") text=_("Présentez votre établissement et votre proposition : chaque demande est lue par l’équipe du projet.") primary_label=button_label primary_url=links.university_proposal %}
```

#### `dialog.html`

- **Scopo**: finestra modale per conferme e dettagli brevi. Mai per contenuti obbligatori o
  pubblicità.
- **Blocco CSS**: `.dialog` (`__header`, `__title`, `__close`, `__body`, `__actions`).
- **Contratto**: `id` (obbligatorio); `title`; `body` (HTML sicuro); `actions` (HTML sicuro dei
  bottoni, opzionale); `light` (True → il click sul backdrop chiude).
- **Varianti**: nessuna. Larghezza `min(100% − 2 × gutter, 36rem)`, altezza massima
  `min(85dvh, 44rem)`. È una delle **due sole superfici** a cui il sistema concede un'ombra
  (`--shadow-surface`) e un bordo da 1 px (§9); oggi usa ancora i nomi dello shim, che valgono `none`.
- **Accessibilità**: `<dialog>` nativo aperto con `showModal()`: focus trap, Esc e sfondo inerte sono
  della piattaforma; `aria-labelledby` → titolo; bottone di chiusura 44 × 44 px con
  `aria-label="Fermer"`; `main.js` porta il focus su `[data-dialog-focus]` o sul primo elemento
  focusabile e lo **restituisce all'elemento che ha aperto**. Senza JS il link `href="#id"` mostra il
  dialog come pannello via `:target`.
- **Usato in**: nessun consumatore.
- **Esempio (dal commento di contratto del componente)**:

```django
<a class="btn" href="#confirm-delete" data-dialog-open="confirm-delete">…</a>
{% include "components/dialog.html" with id="confirm-delete" title=dialog_title body=dialog_body actions=dialog_actions %}
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
  l'ingresso e la porta compatta `264 64 368 456`). La coreografia arriva dallo script della pagina
  attraverso `data-doorway-trace`, `data-doorway-steps`, `data-doorway-key`, `data-doorway-photo`.
- **Varianti**: nessuna: la porta è la porta.
- **Accessibilità**: l'`<svg>` che la contiene è `aria-hidden`: la porta è immagine di marca,
  l'informazione della pagina è nel testo; completa al primo frame, con `prefers-reduced-motion:
  reduce` nulla si muove; sotto colori forzati contorno e gradini in `CanvasText`.
- **Usato in**: `templates/pages/home/_hero.html`, `templates/allauth/layouts/entrance.html`.
- **Esempio reale — `templates/allauth/layouts/entrance.html`**:

```django
{% include "components/doorway.html" with prefix="entrance" %}
```

#### `document_row.html`

- **Scopo**: una pièce richiesta di un fascicolo come riga a sette zone — identità · stato · responsabile ·
  scadenza · salute · azione · menu — dentro un foglio DocumentCollection (design V4, `CREATIVE_DIRECTION.md`
  §3.5.4); sotto 48rem lo stesso markup si impila come scheda. Lo stato è una parola col suo registro
  (`data-register` da `apps/core/chips.py`), mai scelto qui; nessuna riga dice «approvato».
- **Blocco CSS**: `.doc-row` (`__identity`, `__words`, `__title`, `__qualifier`, `__meta`, `__reason`, `__state`,
  `__blocked`, `__responsible`, `__actor`, `__due`, `__due-icon`, `__health`, `__action`, `__menu`, `__more`;
  modificatori `--overdue`, `--compact`), con `.doc-menu` (`__item`) in `v4/workspace.css`.
- **Contratto**: `row` (una voce di `documents.presenters.register_rows`: title, state, state_label, state_css,
  state_reason, responsible, responsible_note, responsible_glyph, due_date, is_overdue, urgency, health,
  mandatory, current, version_count, may_file, action_blocked, detail_url); `compact` (opzionale: sul
  cruscotto — identità · stato · scadenza soltanto, senza responsabile, azione, menu, motivo né «Bloqué»:
  quelli li porta la pagina del registro). La griglia segue la larghezza del FOGLIO (container query
  `collection`): sette zone da 1100 px, cinque con l'azione sulla propria riga sotto, scheda sotto 700.
- **Varianti**: `compact` (tre zone, lista nuda); la scheda sotto 48rem è la stessa riga.
- **Accessibilità**: `<li>` di una lista `role="list"`; la scadenza è un `<time>`; l'urgenza è parola +
  glifo (`warning` · `clock` · `calendar`), mai colore solo; il menu è un `popover` nativo aperto da un
  bottone con nome nascosto; focus dentro la riga = anello inset; l'azione nomina ciò che fa e la porta
  delle CGU è detta sulla riga che blocca, col link che la risolve.
- **Usato in**: `templates/documents/partials/register.html`, `templates/portal/dashboard.html`.
- **Esempio reale — `templates/documents/partials/register.html`**:

```django
{% include "components/document_row.html" with row=row %}
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
  (`__ordinal`, `__title`, `__gloss`, `__cta`, `__arrow`). Le regole `.entrances` e `.entrance` di
  `components.css` non hanno più consumatori e vanno cancellate con la migrazione di quel file.
- **Contratto**: `entrances` (opzionale) = lista di 4 dict `{title, text, button, url, lang}`; se
  omessa il componente rende i quattro blocchi prescritti dal registro (`p3.entrances.*`) con i link
  `pathways:index`, `ecosystem:companies`, `ecosystem:institutions`, `ecosystem:universities` (via
  `safe_url`: un accesso la cui destinazione non esiste ancora è mostrato senza link invece che
  nascosto). `heading_level` = `"h2"` (default) o `"h3"`.
- **Gate**: i testi `p3.*` sono di Fase 3 — chi include il componente senza `entrances` deve farlo
  solo con `gates.phase3_public` aperto. Quando un gate si chiude cambia la **destinazione**, non la
  presenza della riga.
- **Varianti**: `.register--entrances`. Righe da almeno 104 px, ordinale `01`–`04` da contatore CSS
  in rubrica, capello fra le righe, filetto navy da 2 px sopra la prima e sotto l'ultima. La sezione
  passa da ≈ 1900 px a ≈ 460 px su telefono e le quattro vie sono complete entro 1.45 schermate.
  Le quattro illustrazioni sono ritirate con il vecchio markup (§14.1).
- **Accessibilità**: `<ol aria-label="Les quatre accès de l’écosystème">`; l'ordinale è
  `aria-hidden` perché l'ordine è già dato da `<ol>`; tutta la riga è un solo link, quindi un solo
  tab stop e il titolo come nome accessibile; `lang` sul singolo testo in fallback francese.
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
- **Blocco CSS**: `.form-field` (`__label`, `__required`, `__help`, `__check`, `__errors`).
- **Contratto**: `field` (BoundField); `help` (sostituisce `help_text`); `consent` (True → stile del
  consenso obbligatorio, mai pre-spuntato; attivato anche dalla classe widget `consent-checkbox` di
  `core.forms.ConsentBooleanField`).
- **Varianti**: `.form-field--error` (bordo e filetto laterale `--color-error-fg`, che risolve a
  `--state-error-fg`), `--required`, `--consent` (riquadro sul fondo di processo). I widget nascosti
  sono resi nudi; il campo honeypot `website_url` va nel wrapper fuori schermo `.hp-wrap` con
  `aria-hidden="true"`.
- **Accessibilità**: contratto completo in `docs/ACCESSIBILITY.md` §6. In breve: `<label for>` sempre
  presente; asterisco `aria-hidden` + attributo `required`; Django 5.2 aggiunge `aria-invalid="true"`
  e `aria-describedby="<auto_id>_helptext <auto_id>_error"` e il componente usa **esattamente quegli
  id**; lista errori con `role="alert"`; checkbox con etichetta cliccabile a fianco.
- **Usato in**: `templates/allauth/elements/fields.html`, `templates/accounts/profile.html`,
  `templates/forum/partials/registration_form.html`, `templates/documents/upload.html` (e almeno
  altri 9).
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
- **Usato in**: `templates/pages/home/_hero.html` (markup diretto con le stesse classi);
  `templates/pathways/detail.html` (solo l'elemento `.hero__figure`). Nessun `{% include %}`.
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
  le parole. Nessuna legenda: nella pagina del registro il controllo segmentato sotto la barra nomina ogni
  stato col suo punto di registro e il suo conteggio (misurato il 25/09/2026: legenda e controllo dicevano
  le stesse sette cose due volte, a una riga di distanza).
- **Blocco CSS**: `.health` (`__strip`, `__segment`, `__counts`, `__n`, `__sep`, `__open`; modificatore
  `--compact`), in `v4/workspace.css`; la larghezza dei segmenti viene da `data-share` letto con `attr()`
  tipizzato (ripiego: segmenti uguali). I segmenti portano **le marche dei chip** (`conforme` = inchiostro,
  `neutro`/`attesa` = inchiostro 2, `azione` = pending, `rifiuto` = err, `nullo` = hairline-strong) — mai il
  verde di un verdetto, mai l'accento (revisione del gate C) — e un canale non cromatico: tratteggio
  (`--texture-hatch`) su «attesa», punti (`--texture-dots`) su «rifiuto». Il controllo segmentato è `.seg`
  (`__list`, `__item`, `__link`, `__dot`, `__count`) nello stesso foglio, markup in
  `documents/partials/register.html`; il punto ripete marca e stile di bordo del chip (pieno · tratteggiato
  · doppio · punteggiato).
- **Contratto**: `counts` (`documents.requirements.counts`: total, valid, open, per_state); `filters`
  (`documents.presenters.state_filters`: value, label, count, register); `compact` (opzionale: parole più
  piccole); `bare` (opzionale: la sola barra, quando le parole accanto sono della pagina — la checklist del
  fascicolo, il cui conteggio è «éléments complétés», da `cases.presenters.checklist_health`).
- **Varianti**: `compact` sul cruscotto; `bare` nel fascicolo.
- **Accessibilità**: la barra è `aria-hidden`, i conteggi sono testo; ogni segmento porta colore E registro
  (`title` = parola · conteggio), la parola del registro sta nel controllo segmentato accanto al punto.
- **Usato in**: `templates/documents/partials/register.html`, `templates/portal/dashboard.html`,
  `templates/cases/detail.html`.
- **Esempio reale — `templates/documents/partials/register.html`**:

```django
{% include "components/health_strip.html" with counts=block.counts filters=block.filters %}
```

#### `journey_rail.html`

- **Scopo**: le sette tappe bloccate di un fascicolo come binario orizzontale da 64rem — nodo, linea,
  etichetta — verticale sotto; la tappa corrente porta l'anello dell'accento, l'alone e «Vous êtes ici»; la
  frontiera MA→IT è segnata sul primo nodo del lato italiano (design V4, `DESIGN_SYSTEM_V4.md` §8.28).
- **Blocco CSS**: `.journey` (`__step`, `__node`, `__label`, `__here`, `__when`, `__side`, `__actor`;
  modificatori `--current`, `--done`, `--italy`, `--frontier`, `--descriptive`), in `v4/workspace.css`; la linea
  si disegna una volta (`rail-draw` orizzontale, `rail-draw-y` verticale); `__side` è il nome del lato
  («Maroc», «Italie») sulla prima tappa di ciascuno: la frontiera come parola (revisione del gate C, 7c) — sul
  binario orizzontale su una riga propria sopra i nodi, sul verticale sopra l'etichetta. I nodi raggiunti sono
  pieni dell'accento: **posizione**, non verdetto (revisione del gate D, 12c).
- **Contratto**: `steps` (`portal.services.journey_for`: label, side, is_current, frontier, detail, actor — o
  `cases.presenters.journey_with_dates`, che aggiunge `state` e `reached_at`); `label` (opzionale,
  `aria-label` della lista); `descriptive` (opzionale: il fascicolo, CD §3.6.2 — verticale a ogni larghezza,
  accanto a ogni tappa la data in cui è stata raggiunta quando il registro la conosce; una tappa non
  raggiunta non ha data, e nessuna inventata).
- **Varianti**: `descriptive` nel fascicolo; altrimenti orizzontale o verticale secondo la larghezza.
- **Accessibilità**: `<ol>` semantico, numeri da contatori CSS, `aria-current="step"` sulla tappa corrente,
  «Vous êtes ici» come testo; sotto `prefers-reduced-motion: reduce` la linea è semplicemente lì.
- **Usato in**: `templates/portal/dashboard.html`, `templates/cases/detail.html`.
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
- **Usato in**: `templates/pages/home/_trust.html`.
- **Esempio reale — `templates/pages/home/_trust.html`**:

```django
{% include "components/jurisdiction.html" with title=jurisdiction_title caption=jurisdiction_caption segments=d.jurisdiction %}
```

#### `language_segmented.html`

- **Scopo**: il controllo lingua della testata V4 (`docs/design-v4/CREATIVE_DIRECTION.md` §3.2): un
  controllo segmentato di quattro link — FR · IT · EN · ع — con la lingua corrente come cursore in
  rilievo. Link puri, nessuno script: scegliere una lingua è una navigazione.
- **Blocco CSS**: `.lang-seg` (`__list`, `__item`, `__link`, `__code`), in `v4/shell.css`: traccia
  `--min-1` a raggio pieno alta 32 px, cursore `--min-2` con ombra di livello 1 su `[aria-current]`.
- **Contratto**: nessuna variabile; usa `site.languages` (`code`, `name`, `url`, `active`, `dir`),
  come `language_switcher.html`.
- **Varianti**: nessuna. Sotto 80rem è disegnato in testa al cassetto, a tutta larghezza su 44 px
  (`language_switcher.html`, il `<details>` di V1, è ritirato dal 25/09/2026: revisione del gate A,
  correzione 7).
- **Accessibilità**: `<nav aria-label="Choisir la langue">`; ogni link ha `lang`, `hreflang` e `dir`
  propri e il nome della lingua per esteso come testo nascosto; il codice a due lettere è
  `aria-hidden` e maiuscolo per CSS (il nodo di testo resta il codice ISO minuscolo, che l'audit
  del chrome arabo ammette); lingua attiva `aria-current="true"` + cursore + inchiostro pieno, mai
  il solo colore; bersaglio 36 × 28 px dentro una traccia da 32 (SC 2.5.8). Sono link, non un
  `<select>`: nessun cambio di contesto su input (SC 3.2.2).
- **Usato in**: `templates/partials/utility_bar.html`, `templates/partials/header.html` (in testa al
  cassetto), `templates/partials/portal_chrome.html` (barra di contesto e cassetto della console). La direzione lo voleva nella testata: misurato a 1440, le sette sezioni del
  menu CMS (905 px) più il lock-up (303 px) non lasciano spazio a un controllo da 152 px in una riga
  da 1240 — finché l'architettura resta a sette voci, sta nella barra istituzionale.
- **Esempio reale — `templates/partials/utility_bar.html`**:

```django
{% include "components/language_segmented.html" %}
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
- **Usato in**: `templates/ecosystem/_layout.html`, `templates/pages/institutional_base.html` (include);
  `templates/allauth/layouts/manage.html` (markup diretto `.local-nav`). Dal design V4 la console non lo
  usa più: la rail (`partials/portal_chrome.html`) l'ha sostituito.
- **Esempio reale — `templates/ecosystem/_layout.html`**:

```django
<div class="layout-sidebar__aside ecosystem-layout__aside">
  {% include "components/local_nav.html" with items=local_nav_items title=_("Les espaces de l’écosystème") %}
```

#### `metadata_row.html`

- **Scopo**: riga di metadati (data, luogo, categoria, ultima revisione). È il materiale della nota
  marginale (§8.5): posizione, autorità, data.
- **Blocco CSS**: `.meta-row` (`__item`).
- **Contratto**: `items` = lista di dict `{label, value, icon, datetime (ISO → <time>), url}`.
- **Varianti**: nessuna.
- **Accessibilità**: `<dl>` con coppie `<dt>`/`<dd>`; date in `<time datetime>` (cifre tabulari da
  `base.css`, §6.8). Il separatore « : » dopo `<dt>` è contenuto CSS con tipografia francese, non
  localizzato (G-14).
- **Usato in**: `templates/pathways/_metadata_row.html` (markup diretto `.meta-row`).
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
- **Varianti**: `.notice--info/success/warning/error/pending` (terne dei token di stato, bordo
  `inline-start` da 4 px) e `.notice--institutional` (fascia sul fondo di processo con filetto). Come
  per `badge.html`, `success` risolve alla terna blu `--state-done-*` (§4.3). Mancano le tre varianti
  editoriali della direzione (**Nota**, **Importante**, **Approfondimento**).
- **Accessibilità**: `role="alert"` solo per `error`, `role="status"` per tutti gli altri; icona +
  titolo + bordo: il tipo non è mai comunicato dal solo colore.
- **Usato in**: `templates/community/discussion.html`, `templates/accounts/delete_request.html`,
  `templates/glossary/term.html`, `templates/living/sheet.html` (e almeno altri 18).
- **Esempio reale — `templates/community/discussion.html`**:

```django
{% translate "Discussion fermée : il n’est plus possible de répondre." as closed_text %}
{% include "components/notice.html" with kind="info" text=closed_text %}
```

#### `option_cards.html`

- **Scopo**: le scelte di una domanda a radio o a caselle come **OptionCard** (design V4,
  `CREATIVE_DIRECTION.md` §3.7, `DESIGN_SYSTEM_V4.md` §8 «OptionCard»): un `<label>` intorno all'input NATIVO,
  livello 1, raggio `lg`, titolo 15/24 500; hover livello 2; selezionata = bordo accento 2 px, fondo
  `--accent-wash` e spunta che si disegna; ≥ 48 px, `touch-action: manipulation`. Nessun disco con glifo:
  nessuna opzione qui ha un glifo onesto (una lingua, «oui», «non»), e uno decorativo sarebbe inventato.
- **Blocco CSS**: `.opts` (`__legend`, `__help`, `__hint`, `__grid`; modificatore `--error`) e `.opt` (`__mark`,
  `__title`), in `v4/wizard.css`.
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
- **Blocco CSS**: `.page-header` (`__eyebrow`, `__title`, `__lead`, `__meta`); include `.container`.
- **Contratto**: `title`; `eyebrow`, `lead` (opzionali); `lang`; `meta` (HTML sicuro, es. una metadata
  row); `align` (`"center"`).
- **Varianti**: `.page-header--center`. Lo slot `__eyebrow` è abolito (§8.2). Il titolo va reso in
  **minuscolo per CSS**: un redattore non deve poter cambiare l'identità digitando maiuscole nel CMS
  (§6.7). **Da cancellare da ogni schermata del portale**: lì ripropone il teaser di marketing della
  home come `<h1>` a chi ha già fatto il login.
- **Accessibilità**: `<header>` di contenuto; titolo limitato a 22ch, lead a 60ch — il lead va
  riportato al tetto reale di `--measure-lead` (45ch, §6.6).
- **Usato in**: `templates/accounts/profile.html`, `templates/faq/index.html`,
  `templates/glossary/index.html`, `templates/partners/index.html` (e almeno altri 28).
- **Esempio reale — `templates/accounts/delete_request.html`**:

```django
{% include "components/page_header.html" with title=_("Supprimer mon compte") %}
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
- **Blocco CSS**: `.pathway-list` (`__item`, `__num`, `__title`, `__desc`, `__arrow`).
- **Contratto**: `items` = lista di dict `{title, text, url, lang}`; `lang` (per l'intera lista).
- **Varianti**: nessuna. Numeri `01`–`08` da contatore CSS (`decimal-leading-zero`), oggi in rubrica;
  freccia nascosta sotto 48rem — **da correggere**, perché la freccia è l'affordance e sotto 48rem è
  esattamente dove serve.
- **Accessibilità**: `<ol>` (l'ordine è semantico); numeri `aria-hidden`; stretched link con un solo
  tab stop; titoli `<h3>`.
- **Usato in**: `templates/pages/home/_pathways.html` (include); `templates/pathways/index.html`
  (markup diretto `.pathway-list`).
- **Esempio reale — `templates/pages/home/_pathways.html`**:

```django
{% include "components/pathway_list.html" with items=d.pathway_items %}
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
- **Usato in**: `templates/ecosystem/companies.html`, `templates/ecosystem/institutions.html`,
  `templates/ecosystem/universities.html`, `templates/ecosystem/pilot.html`,
  `templates/pages/partials/_section_header.html` (include); `templates/pathways/detail.html` (markup
  diretto `.section__header`).
- **Esempio reale — `templates/ecosystem/companies.html`**:

```django
<section id="demarche" class="ecosystem-section ecosystem-moments" aria-labelledby="demarche-header">
  {% include "components/section_header.html" with id="demarche-header" eyebrow=_("La démarche") title=_("Trois temps, une même démarche") %}
```

#### `stepper.html`

- **Scopo**: indicatore di avanzamento dei flussi a più passi (wizard di orientamento).
- **Blocco CSS**: `.stepper` (`__item`, `__marker`, `__label`) + `progress.progress` +
  `.progress-label`.
- **Contratto**: `steps` = lista di str; `current` = indice **a base 1** del passo corrente.
- **Varianti**: `.stepper__item--done` (marcatore con segno di spunta — il verde è sparito con
  `--color-secondary-800`, che risolve a `--cooperation` e **non va usato per «fatto»**: il
  modificatore va riportato sulla terna `--state-done-*`, §4.3), `.stepper__item--current` (bordo
  2 px, grassetto); verticale → orizzontale (≥ 48rem). Il cerchio del marcatore è l'unico uso
  previsto di `--radius-marker`.
- **Accessibilità**: `<ol aria-label="Progression">`; passo corrente `aria-current="step"`; testo
  «Étape n sur N» sempre visibile; `<progress>` nativo (nessuno stile inline: CSP) con
  `aria-hidden="true"` perché duplica il testo. Lo stato non dipende dal colore: numero → spunta,
  spessore del bordo, grassetto.
- **Usato in**: `templates/pages/home/_orientation.html`, come sequenza esplicativa: con `current=0`
  nessun passo è «corrente» o «completato». In un flusso reale `current` parte da 1.
- **Esempio reale — `templates/pages/home/_orientation.html`**:

```django
{% include "components/stepper.html" with steps=d.steps current=0 %}
```

#### `tabs.html`

- **Scopo**: schede per contenuti paralleli brevi. Non usare per contenuti che l'utente deve
  confrontare.
- **Blocco CSS**: `.tabs__list`, `.tabs__tab`, `.tabs__panel`, `.tabs__panel-title` (radice `.tabs`).
- **Contratto**: `tabs` = lista di dict `{id, label, body (HTML sicuro)}`; `id` (id del widget,
  default `tabs`: obbligatorio se ce n'è più d'uno in pagina); `remember` (chiave `localStorage`).
- **Varianti**: nessuna.
- **Accessibilità**: pattern WAI-ARIA Tabs ad attivazione automatica: `role="tablist"`/`tab`/
  `tabpanel`, `aria-selected`, `aria-controls`, `aria-labelledby`, roving `tabindex`, pannelli
  `tabindex="0"`; frecce (invertite in RTL), Home, Fine. `#id-pannello` nell'URL apre quella scheda.
  **Senza JS** la tablist è nascosta e tutti i pannelli sono impilati con il proprio `<h3>`.
  `remember` oggi **scrive** la scelta ma non la rilegge (G-21).
- **Usato in**: nessun consumatore.
- **Esempio (dal contratto)**:

```django
{% include "components/tabs.html" with tabs=training_tabs id="formation" %}
```

#### `timeline.html`

- **Scopo**: sequenza di tappe (progetto pilota in 8 passi, fasi di un percorso). È l'antenato del
  tipo di corpo `SEQUENCE`.
- **Blocco CSS**: `.timeline` (`__item`, `__marker`, `__label`, `__text`).
- **Contratto**: `steps` = lista di str **oppure** di dict `{label, text}`; `lang`; `label`
  (aria-label).
- **Varianti**: verticale (mobile) → 4 + 4 (≥ 48rem) → 8 in riga (≥ 80rem); porta ancora
  `.reveal.reveal--stagger`, che la direzione cancella (§12). **Da correggere**: la sequenza è
  **verticale, sempre** — mai una riga di cerchi uniti da linee. Il diagramma 4+4 attuale manda il
  connettore del passo 4 al bordo del contenitore e si ferma, costringendo il lettore a saltare in
  basso e a sinistra per il passo 5; a 390 px non ha alcun significato.
- **Accessibilità**: `<ol>`; numeri da contatore CSS con marcatori `aria-hidden`; le linee sono
  pseudo-elementi decorativi — sotto la direzione devono diventare bordi reali, perché uno
  pseudo-elemento dipinto con `background` sparisce a colori forzati (§2).
- **Usato in**: `templates/ecosystem/partials/pilot_flow.html`, `templates/ecosystem/companies.html`
  (include); `templates/pathways/detail.html` (markup diretto `.timeline`). **Non più nella home**:
  dal 24 settembre 2026 la sezione del progetto pilota disegna la stessa sequenza bloccata come
  **rotta fra due rive** (`.voyage`, DESIGN_SYSTEM_V2.md §8.6), con le stazioni allineate ai punti
  della linea e la linea che si disegna allo scroll. Il componente resta per le due pagine
  dell'ecosistema finché non tocca a loro.
- **Esempio reale — `templates/ecosystem/partials/pilot_flow.html`**:

```django
{% include "components/timeline.html" with steps=flow.steps lang=flow.lang_attr label=_("Séquence proposée du projet pilote, étape par étape") %}
```

#### `wizard_stepper.html`

- **Scopo**: lo **Stepper** di un modulo guidato (design V4, `CREATIVE_DIRECTION.md` §3.7 a): le domande come
  lista verticale — un nodo per domanda, pieno se la domanda ha una risposta (la stessa regola di
  `PersonProfile.answered()`: «je ne sais pas encore» non è una risposta, 0 lo è), il corrente con l'anello, la
  linea fra i nodi che avanza. Ogni voce è un link alla sua domanda: funziona senza JavaScript (ancora in
  pagina) e con (`situation.js` mostra quella domanda).
- **Blocco CSS**: `.wstep` (`__item`, `__link`, `__node`, `__label`; modificatori `--done`, `--current`), in
  `v4/wizard.css`.
- **Contratto**: `fields` (i campi visibili del modulo, nell'ordine delle domande); `answered` (l'insieme dei
  nomi di campo con una risposta, dal profilo, non ricalcolato qui); `label` (opzionale).
- **Varianti**: nessuna.
- **Accessibilità**: `<ol role="list">` con `aria-label`, `aria-current="step"` sulla domanda corrente
  (spostato dallo script), voci di 44 px; nessuna barra nativa, nessuna percentuale.
- **Usato in**: `templates/portal/situation.html`.
- **Esempio reale — `templates/portal/situation.html`**:

```django
{% include "components/wizard_stepper.html" with fields=form.visible_fields answered=answered_fields %}
```

### 10.1 Pattern CSS senza file template

| Pattern | Classi | Note |
|---|---|---|
| Bottoni | `.btn` + `--primary`, `--secondary`, `--ghost`, `--link`, `--danger`, `--inverse`, `--sm`, `--lg`, `--block`, `--upper`, `--arrow` | tre ranghi ammessi (§9): `--ghost` e `--upper` sono sulla lista di demolizione. Altezza minima 44 px; `:disabled` / `[aria-disabled="true"]` → opacità 0.55 e `pointer-events: none` |
| Link con freccia | `.link-arrow` | CTA secondaria nelle liste; freccia `.icon--flip-rtl`, traslazione di 3 px su hover (invertita in RTL) |
| Icone | `.icon`, `--sm`, `--lg`, `--xl`, `--accent`, `--flip-rtl` | §13 |
| Messaggi Django | `.messages` > `.alert.alert--{tag}` | resi da `base.html` in una regione `role="status" aria-live="polite"`; `error` → `role="alert"` |
| Form | `.form`, `.form__fieldset`, `.form__legend`, `.form__intro`, `.form__required-note`, `.form__actions`, `.form-row.form-row--2`, `.input`, `.search-form` | il form completo è descritto in `docs/ACCESSIBILITY.md` §6 |
| Avanzamento | `progress.progress`, `.progress-label` | `<progress>` nativo, 6 px; il raggio a pastiglia risolve ora a 2 px |
| Sommario di pagina | `.section-nav` (`__list`, `__link`) + `data-section-nav` | barra sticky sotto la cromatura; `main.js` marca la sezione in vista con `aria-current="true"`. È l'antenato del titolo corrente sticky della direzione |
| Pagine d'errore | `.error-page` (`__code`, `__title`, `__text`, `__ref`, `__actions`, `__links`) | `templates/errors/400.html` … `templates/errors/500.html` su `templates/errors/base_error.html`: un `h1`, codice decorativo `aria-hidden`, azioni di recupero, `nav aria-label="Navigation de secours"`; il riferimento usa `--font-ref` |
| Pagine account | `.account-page` (`--entrance`, `--manage`), `.account-page__card`, `.account-panel`, `.account-table` | `templates/allauth/layouts/` e `templates/allauth/elements/` mappano ogni elemento di django-allauth sul design system |
| Pagina legale | `.legal-page`, `.legal-page__meta`, `.legal-page__courtesy` | misura di lettura da `.container--prose` (alias legacy di 42rem) |
| Contatore | `.counter` + `data-counter` | **sulla lista di demolizione**: «contatori da startup» è un anti-pattern dichiarato e il componente ha zero usi |
| Segnaposto di sviluppo | `.dev-placeholder` | mai nel markup di produzione |

### 10.2 Shell (`templates/base.html` + `templates/partials/`)

| File | Contenuto |
|---|---|
| `templates/base.html` | `<html lang dir class="no-js">`; preload font per direzione (G-24); il bundle `css/dist/main.css` (§2); `head.js` sincrono; skip link; `utility_bar` → `header` → blocco `banner` → `<main id="main-content" tabindex="-1">` (blocco `breadcrumbs`, regione messaggi, `main_content` ⊃ `content`) → `footer`; `main.js` come modulo |
| `templates/partials/utility_bar.html` | fascia navy `role="region" aria-label="Barre institutionnelle"`: promotore, link «Espace réservé» oppure menu account, selettore lingua |
| `templates/partials/header.html` | header sticky: wordmark `{% brand %}`, bottone `Menu` (`data-nav-toggle`), drawer `#nav-drawer` con `<nav aria-label="Navigation principale">`, overlay |
| `templates/partials/main_nav.html` | voci da `cms.MenuItem` (fallback statico in `apps/cms/templatetags/cms_nav.py`), filtrate da gate/flag e da route risolvibili; link + bottone disclosure + pannello per voce con figli |
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

Quanto segue descrive ciò che `components.css` rende **oggi**.

### 11.1 Mega-menu (≥ 80rem) — pattern «disclosure navigation»

Non è un `role="menubar"`: è una lista di link con bottoni di apertura, il modello raccomandato per
la navigazione di un sito (nessuna cattura dei tasti freccia dentro i pannelli, Tab sempre
prevedibile).

- **Markup** (`templates/partials/main_nav.html`): per ogni voce con figli `li[data-nav-item]`
  contiene il link di sezione `a[data-nav-link]` (o `span.main-nav__label` se la voce non ha una URL
  risolvibile), un `button[data-nav-panel-toggle]` con `aria-expanded` e `aria-controls="<id>-panel"`
  e il pannello `div[data-nav-panel]`. Le voci senza figli sono link semplici.
- **Pannello**: due colonne (titolo + descrizione + «Voir l’espace» | sottovoci), larghezza minima
  36rem, filetto superiore da 2 px (oggi in rubrica, perché `--border-accent` risolve a `--rubric`),
  ombra dichiarata ma risolta a `none`; centrato sotto la voce, allineato al bordo di chiusura per
  l'ultima voce. **Regola della direzione, non ancora applicata**: un pannello si rende solo se la
  voce ha **≥ 3 destinazioni distinte**, altrimenti la voce di primo livello è un link semplice —
  oggi il pannello «Personnes» è un riquadro di 576 × 211 px che contiene due link che puntano
  entrambi alla pagina appena cliccata, disallineato di 224 px rispetto al proprio trigger.
- **Stato**: `data-open="true"` sul `li` + `aria-expanded="true"` sul bottone; un solo pannello
  aperto.
- **Tastiera**: Tab percorre link e bottoni nell'ordine del DOM; Invio/Spazio sul bottone apre il
  pannello e porta il focus sul primo elemento; **Esc** chiude e restituisce il focus al bottone;
  **←/→** (invertite in RTL) spostano il focus fra le voci di primo livello *che hanno un pannello*,
  con ritorno circolare; **↓** apre ed entra; uscendo con Tab il pannello si chiude (`focusout`);
  click esterno chiude.
- **Voce corrente**: `aria-current="page"` (URL identica) o `"true"` (sezione antenata) + barra. La
  direzione chiede **tre segnali** — peso 500 → 600, filetto rubrica da 2 px e `aria-current` — di
  cui almeno uno sopravvive alla scala di grigi e ai colori forzati; oggi lo stato corrente e lo
  stato hover sono identici pixel per pixel.
- Verificato da `tests/frontend/test_browser.py::test_mega_menu_is_keyboard_operable`; screenshot
  `docs/qa/design/state-megamenu-open-fr-1440.png`, `docs/qa/design/state-megamenu-open-ar-1440.png`.

### 11.2 Drawer (< 80rem: telefono, tablet, laptop fino a 1279 px)

- Lo **stesso markup** del menu diventa un pannello `position: fixed` sotto l'header (`#nav-drawer`),
  aperto dal bottone «Menu» (`data-nav-toggle`, `aria-controls="nav-drawer"`, `aria-expanded`; icona
  `menu` ↔ `close`). Stato: `body[data-nav-open="true"]`. Il bordo superiore del pannello è
  `var(--nav-drawer-top, var(--header-height))`: all'apertura `main.js` misura il bordo inferiore
  reale dell'header e lo scrive in `--nav-drawer-top`.
- All'apertura il focus va sul primo elemento del drawer; **Esc** chiude e torna al bottone; Tab
  dall'ultimo elemento e Shift+Tab dal primo riportano al bottone; il click sull'overlay chiude; il
  passaggio alla larghezza desktop chiude tutto.
- I sotto-pannelli si aprono in linea con gli stessi bottoni (bersagli da 52 px); le sottovoci sono
  alte almeno 44 px.
- **Destinazione**: la direzione vuole un `<dialog>` con `showModal()` — focus trap, Esc e sfondo
  `inert` gratis — agganciato all'altezza reale della cromatura (`--chrome-block-size`), e un
  contenuto che è **un indice**, non un accordion: quattro righe numerate per i quattro pubblici, poi
  la voce dell'istituzione, poi ricerca, servizi e lingue. Oggi il drawer è vuoto al 72 % (208 px di
  contenuto in un pannello da 731 px), offre quattro destinazioni, e due dei quattro pubblici che la
  home nomina non ci sono affatto.
- **G-02 (chiusa il 20/09/2026)**: il `backdrop-filter` era su `.site-header`, che diventava
  containing block del drawer `position: fixed` (65 px di altezza, overlay 0 px). Spostato sullo
  pseudo-elemento `.site-header::before` (§1.4). Misura dopo la correzione: drawer alto **731 px** su
  **731 px** disponibili a 390 × 844 e **655 px** su **655 px** a 1024 × 768, overlay a tutto schermo
  — `docs/qa/design/state-drawer-open-fr-390.png`, `docs/qa/design/state-drawer-open-ar-390.png`,
  `docs/qa/design/state-drawer-open-fr-1024.png`, `docs/qa/design/state-drawer-open-ar-1024.png`.
- **Difetto aperto G-23**: a drawer aperto e pagina non scrollata l'overlay `.nav-overlay` parte
  ancora da **72 px** dall'alto del viewport, mentre con la barra istituzionale visibile il bordo
  inferiore dell'header è a **113 px**: il velo copre la fascia bassa dell'header, wordmark e bottone
  «Menu» compresi. `--nav-drawer-top` è impostata sul solo drawer e l'overlay, che ne è fratello, non
  la eredita. La correzione strutturale è quella della direzione: consumare `--chrome-block-size`,
  che è calcolata in CSS e quindi ereditata da tutti.
- **Difetto aperto G-04**: senza JavaScript il bottone «Menu» è nascosto e il menu è reso per intero,
  in flusso, dentro l'header — che resta `position: sticky` e misura **781 px**. A 390 × 844 restano
  63 px di contenuto visibile; a 1024 × 768 nessuno (`docs/qa/design/a11y-nojs-fr-390.png`,
  `docs/qa/design/a11y-nojs-fr-1024.png`). Contraddice il principio 6 (§1.1) e ADR-009. La
  correzione è una regola: `html.no-js .site-header { position: static }` dentro
  `@media (max-width: 79.999rem)`.

### 11.3 Selettore lingua e menu account

`<details data-dropdown>` nella barra istituzionale: si aprono e si chiudono senza JS; `main.js`
aggiunge `aria-expanded`, chiusura con Esc (focus al `summary`), chiusura al click esterno e alla
perdita di focus, e ne tiene aperto uno solo per volta. Le lingue sono link `translate_url` della
pagina corrente, non un `<select>`. Schede: §10 `language_segmented.html`, `account_menu.html`. Le
quattro lingue sono in linea, senza disclosure, dal design V4 (§10, `language_segmented.html`).

### 11.4 Breadcrumb, navigazione locale, sommario di pagina, paginazione

| Pattern | Dove | Regola |
|---|---|---|
| Breadcrumb | blocco `breadcrumbs` di `base.html`, prima del contenuto | derivato dallo stesso albero di menu della navigazione; «Accueil» automatico; ultimo elemento = pagina corrente, non linkata; solo a profondità ≥ 2 |
| Navigazione locale | `.layout-sidebar__aside`, poi il rail | colonna sticky ≥ 64rem; sotto, un filetto segmentato scorrevole da 44 px e non una nuvola di pastiglie; `aria-current="page"` |
| Sommario di pagina | `.section-nav[data-section-nav]` | ancore alle sezioni di una pagina lunga; sticky sotto la cromatura; diventa il titolo corrente della direzione |
| Paginazione | fine lista | precedente / «Page n sur N» / successivo |
| Footer | ogni pagina | due `nav` etichettate: cinque link legali distinti + navigazione del sito, con **i quattro pubblici sempre presenti**, in entrambi gli stati di gate e nelle quattro lingue |
| Skip link | primo elemento di `<body>` | «Aller au contenu principal» → `#main-content` (`docs/qa/design/state-skiplink-fr-390.png`, `docs/qa/design/state-skiplink-ar-390.png`) |

### 11.5 La cromatura come una sola misura

`--chrome-block-size` è calcolata in CSS da `--chrome-utility` più `--chrome-masthead`, e oggi ha
due consumatori: `scroll-padding-block-start` in `base.css` e `--nav-drawer-top` nello shim, cioè il
bordo superiore del drawer. **Nessun JavaScript deve scrivere geometria su un elemento di cui hanno
bisogno anche i suoi fratelli** — è esattamente l'errore che produce G-23, perché `main.js` scrive
`--nav-drawer-top` sul solo drawer e il velo, che ne è fratello, non lo eredita. La correzione è far
consumare il token calcolato anche a `.nav-overlay`, e sopprimere la scrittura da JavaScript.

---

## 12. Motion

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
> il keyframe della cascata V4 è **`route-current`** (`v4/hero.css`): la corrente lungo le quattro vie
> della porta — `stroke-dashoffset` da 1 a 0 in 28 s lineari (`--motion-ambient`), l'unico oggetto vivo
> della home, in pausa fuori dal viewport e a scheda nascosta (`.is-offscreen` da `home.js`), assente
> sotto `prefers-reduced-motion: reduce`. `v4/shell.css` aggiunge **`mega-in`**: il mega-menu che si apre
> dal bordo della barra — opacità 0→1, `translateY(-8px)`→0 e `clip-path` dal bordo, 200 ms `--ease-enter`;
> nessuna animazione sotto `prefers-reduced-motion: reduce` (i `menu-in*` di `components.css` restano
> dichiarati e non più applicati sopra 80rem). `v4/workspace.css` aggiunge, col fascicolo (gate D),
> **`tl-light`**: l'ultimo nodo della Timeline che si accende una volta al caricamento — fondo da
> `--hairline-strong` a `--accent`, alone da 0 a 4 px di `--accent-wash`, 320 ms `--ease-enter`; sotto
> `prefers-reduced-motion: reduce` il nodo è semplicemente acceso. il pattern 1 «page enter» (`ws-in`, `console.css`) è stato costruito per la revisione del gate B e
> **rimosso** alla revisione del gate E: il suo `translate` faceva del workspace il contenitore di una barra
> `position: fixed` (gate D) e la sua opacità 0 → 1 nascondeva all'osservatore l'elemento LCP reale (gate E).
> La console arriva completa. `v4/buttons.css` aggiunge **`btn-busy`**: il misuratore a
> tre tacche del bottone occupato (`.btn.is-busy`, impostato da `shell.js` all'invio di un modulo
> `data-single-submit`) — opacità delle tacche in 1200 ms lineari, solo mentre è occupato; sotto
> `prefers-reduced-motion: reduce` le tacche restano ferme. `v4/workspace.css` aggiunge tre keyframe del
> pattern «draw» (una volta, al caricamento, mai in loop): **`notch-fill`** (le tacche del misuratore, 320 ms
> con scaglione di 60), **`strip-fill`** (i segmenti della HealthStrip, 320 ms), **`rail-draw-y`** (la linea verticale del
> JourneyRail, `scaleY` 0→1, stessa durata e stesso scaglione) e **`rail-draw`** (la linea
> della JourneyRail, 900 ms con scaglione di 120); tutti e tre solo sotto `prefers-reduced-motion:
> no-preference`.
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
> con «riduci movimento».
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

Keyframe esistenti in `components.css` — sono quattro e nessuno di più: `menu-in`, `menu-in-rtl`,
`menu-in-end` (le tre varianti di ingresso del pannello del mega-menu, per LTR, RTL e per la voce
allineata al bordo di chiusura) e `dialog-in`. Tutti e quattro sono disattivati a movimento ridotto.

---

## 13. Iconografia

- **Un solo set**: icone al tratto originali, griglia 24 × 24, nessun riempimento. Niente emoji,
  niente librerie di terzi, niente mescolanze (R-DES-009). La direzione chiede **terminali quadri**
  (i terminali arrotondati si leggono consumer) e tratto 1.5: oggi il set ha terminali arrotondati,
  ed è un passaggio di disegno da fare in un colpo solo su tutte e 36.
- **Uso**: `{% svg_icon "nome" %}` → `<svg class="icon" aria-hidden="true" focusable="false"><use
  href="/static/img/icons.svg#icon-nome"></use></svg>`. Secondo argomento = classi; terzo = etichetta
  (`role="img"` + `aria-label`, al posto di `aria-hidden`). Colore = `currentcolor`; **nessun
  esadecimale letterale dentro `static/img/`** — oggi `entrance-person.svg` cuoce `#0f2b52`,
  `#9a7b2f` e `#fbfaf7`, e `orientation.svg` aggiunge `#1f6b48`: tre di quei quattro colori non
  esistono più nel sistema (§14.1).
- **Decorativa per default**: accanto a un testo l'icona è nascosta alle tecnologie assistive; un
  controllo con la sola icona deve avere testo `.visually-hidden` o `aria-label`.
- **Direzionalità**: `arrow` e `chevron-end` indicano «avanti» e ricevono `.icon--flip-rtl`
  (`transform: scaleX(-1)` sotto `[dir="rtl"]`). Non si specchiano: `chevron` (giù),
  `arrow-up-right`, `check`, `search`, `clock`, `quote` e ogni icona non direzionale.
- **Cinque usi legittimi** (.italia): simboleggiare una funzione di interazione; navigazione;
  categorizzare un **tipo di contenuto** (documento, evento, persona, luogo); riscontro di
  caricamento; social. Sempre accoppiata a un'etichetta di testo, o con l'etichetta disponibile alle
  tecnologie assistive. **Al massimo sei icone per pagina.** Mai un'icona per riga. Mai un'icona per
  card: non ci sono card.
- **Colore**: `.icon--accent` eredita oggi la rubrica (6.92:1 sulla carta): è sopra la soglia sia per
  gli oggetti grafici sia per il testo, ma **va riesaminato caso per caso**, perché un'icona non è
  una posizione in una sequenza e l'unico compito della rubrica è l'ORDINE (§4.1).

Elenco completo degli `id` dello sprite (`static/img/icons.svg`, prefisso `icon-`):

<!-- icon-list:start -->
36 icone.

| Gruppo | Icone |
|---|---|
| Accessi e soggetti | `person`, `user`, `building`, `institution`, `university`, `briefcase`, `handshake` |
| Direzione e navigazione | `arrow`, `arrow-up-right`, `chevron`, `chevron-end`, `menu`, `close`, `plus`, `minus`, `home`, `list`, `compass`, `map-pin`, `globe`, `search` |
| Stato e feedback | `check`, `warning`, `info`, `shield`, `clock`, `calendar` |
| Contatto e documenti | `mail`, `phone`, `document`, `download`, `quote` |
| Account e sicurezza | `lock`, `key`, `logout`, `settings` |
<!-- icon-list:end -->

> **G-01 (chiusa il 20/09/2026).** Lo sprite non era XML ben formato: il commento iniziale conteneva
> la sequenza `--` (nel nome della classe `.icon--flip-rtl`), vietata dentro un commento XML. Il
> browser scaricava il file (HTTP 200, `image/svg+xml`) ma non lo interpretava e **nessuna icona
> veniva disegnata su nessuna pagina**. L'owner ha riformulato il commento; verifica in Chromium:
> `DOMParser` senza `parsererror` e, nel report `docs/qa/design/capture-report.json`, **546 icone disposte**
> sulle 43 catture, 0 vuote (`emptyIcons`). Regressione impedita da
> `tests/frontend/test_design_docs.py::test_icon_sprite_is_well_formed_xml`, da
> `tests/frontend/test_svg_wellformed.py::test_svg_is_wellformed_xml` (ogni SVG sotto `static/`) e da
> `docs/qa/design/capture.py`, che esce con codice 1 se un'icona disposta non disegna nulla.

---

## 14. Illustrazioni e fotografia

### 14.1 Illustrazioni (`static/img/illustrations/`)

Sei SVG originali al tratto, ereditati dal sistema ritirato. **Tutti e sei sono da ritirare o da
ridisegnare**, e i loro colori sono la prova: tratto `#0f2b52`, accenti `#9a7b2f` (bronzo) e
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
| `pilot-flow.svg` | 640 × 160 | otto nodi su una linea ascendente fra due territori | ritirare: è una curva di crescita con il nodo finale pieno d'oro, cioè un grafico di crescita disegnato per una sequenza istituzionale, che implica un esito che la piattaforma non promette |

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

Tre file senza bundler (più i bundle esbuild di `static/js/src/`), ≈ 21.5 KB non compressi in totale.

| File | Caricamento | Ruolo |
|---|---|---|
| `static/js/head.js` | `<script src>` sincrono in `<head>` | una riga: sostituisce `no-js` con `js` su `<html>` prima del primo paint. È un file esterno perché la CSP è `script-src 'self'` senza nonce |
| `static/js/rail-pref.js` | `<script src>` sincrono in testa al `<body>` della console (`portal/base_portal.html`) | una funzione: legge la chiave ile.rail di localStorage e scrive l'attributo data-rail sul body prima che la rail sia analizzata, così la preferenza non sposta il workspace dopo il primo frame (CLS fino a 1,19 misurato dalla revisione del gate C). File esterno e classico, non nel bundle: la CSP vieta lo script in linea e un modulo sarebbe differito |
| `static/js/main.js` | `<script type="module">` a fine `<body>` | modulo ES senza `import`; esporta `init`; ogni comportamento si aggancia a un attributo `data-*`; nessun testo nel JS (tutte le stringhe restano nell'HTML tradotto dal server) |

Inventario di `main.js` (funzioni chiamate da `init()`):

| Funzione | Hook | Cosa aggiunge | Cosa funziona comunque senza JS |
|---|---|---|---|
| `initFormErrorFocus` | `#form-errors` | dopo un invio non valido porta il focus sul riepilogo degli errori e lo scorre al centro del viewport, senza animazione a movimento ridotto | il riepilogo è comunque in cima al form, con `role="alert"` e un link per ogni campo in errore |
| `initNavigation` | `data-nav-toggle`, `data-nav-drawer`, `data-nav-overlay`, `data-nav-item`, `data-nav-link`, `data-nav-panel-toggle`, `data-nav-panel` | drawer, mega-menu, `aria-expanded`, Esc, frecce, chiusura su `focusout`/click esterno, ciclo del focus nel drawer | menu interamente visibile sotto 80rem (in flusso dentro l'header: vedi G-04); pannelli su hover/focus-within da 80rem in su; tutti i link raggiungibili |
| `initDropdowns` | `details[data-dropdown]` | `aria-expanded`, Esc, click esterno, perdita di focus, uno aperto per volta | `<details>` si apre e si chiude nativamente |
| `initAccordions` | `data-accordion` | esclusività per i browser senza `<details name>` | accordion pienamente funzionante (più pannelli aperti insieme) |
| `initTabs` | `data-tabs`, `data-tabs-remember` | tab ARIA, roving tabindex, frecce/Home/Fine, apertura da `#hash` | pannelli impilati con il proprio titolo; tablist nascosta |
| `initSteppers` | `data-stepper`, `data-step`, `data-step-marker`, `data-step-next`, `data-step-prev`, `data-step-current`, `data-step-focus` | pannelli lato client, `aria-current="step"`, focus sul titolo del passo | tutti i passi visibili in sequenza |
| `initReveal` | `.reveal`, `.reveal--stagger` | comparsa allo scroll — **da cancellare** (§12): nulla si muove allo scroll in questa direzione | contenuto sempre visibile |
| `initDialogs` | `data-dialog-open`, `data-dialog-close`, `data-dialog-focus`, `data-dialog-light` | `showModal()`, focus iniziale, focus di ritorno, chiusura dal backdrop | il link `#id` mostra il dialog come pannello via `:target` |
| `initCounters` | `data-counter`, `data-counter-format` | conteggio animato — **da cancellare** (§12): zero usi, e «contatori da startup» è un anti-pattern dichiarato | valore statico nell'HTML |
| `initMisc` | `data-history-back`, `data-single-submit`, `data-section-nav` | «pagina precedente», blocco del doppio invio (`disabled` + `aria-disabled`), `aria-current` sul sommario di pagina | il link «indietro» è `.js-only`; il form si invia normalmente |

`localStorage` è usato solo da `initTabs` (chiave `tabs:<remember>`, indice numerico della scheda):
nessun dato personale, nessun identificatore; è memoria tecnica, non un cookie di tracciamento.
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

**153 nomi** e 14 classi sono oggi nello shim. Ogni riga è un debito con un sostituto nominato, e
il conto alla rovescia è tenuto da due file. `tests/frontend/test_legacy_token_shim.py` tiene i
**tetti** — 153 token, 14 classi e 1 636 usi complessivi dei nomi ritirati in `static/css/`, nei
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

Quattro raggi su una sola pagina diventano 0 con due eccezioni. **`--radius-pill` risolve al raggio di controllo, non a 999 px**: una pastiglia non è una forma che questo sistema possiede.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--radius-xs` | `0` | valore letterale, nessun token di destinazione |
| `--radius-sm` | `var(--radius-control)` | `--radius-control` |
| `--radius-md` | `var(--radius-control)` | `--radius-control` |
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

`--control-height` resta a 44 px: è l'obiettivo interno per SC 2.5.8 e non cambia. `--nav-drawer-top` parte da `--chrome-block-size`, che è calcolata in CSS e quindi ereditata (§11.5).

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--control-height` | `44px` | valore letterale, nessun token di destinazione |
| `--control-height-sm` | `36px` | valore letterale, nessun token di destinazione |
| `--icon-size` | `20px` | valore letterale, nessun token di destinazione |
| `--icon-size-sm` | `16px` | valore letterale, nessun token di destinazione |
| `--icon-size-lg` | `24px` | valore letterale, nessun token di destinazione |
| `--utility-height` | `var(--chrome-utility)` | `--chrome-utility` |
| `--header-height` | `var(--chrome-masthead)` | `--chrome-masthead` |
| `--nav-drawer-top` | `var(--chrome-block-size)` | `--chrome-block-size` |

**Focus**

L'anello a due toni sopravvive invariato nel meccanismo e cambia solo di tinta: navy su chiaro (13.62:1), carta su navy (13.62:1). Il bronzo chiaro dell'anello inverso è sparito.

| Nome legacy | Risolve a | Nel nuovo sistema |
|---|---|---|
| `--focus-ring-color` | `var(--navy)` | `--navy` |
| `--focus-ring-inverse` | `var(--paper-on-navy)` | `--paper-on-navy` |
| `--focus-ring-width` | `2px` | valore letterale, nessun token di destinazione |
| `--focus-ring-offset` | `2px` | valore letterale, nessun token di destinazione |
| `--focus-ring-offset-color` | `var(--paper)` | `--paper` |

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
| `--z-modal` | `var(--z-dialog)` | `--z-dialog` |
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
in `docs/ACCESSIBILITY.md` §13 (**G-01 … G-26**); qui i difetti che toccano il design system. Una
riga «chiusa» resta in tabella con la data e l'evidenza della chiusura.

| Id | Gravità | Difetto | File | Correzione proposta |
|---|---|---|---|---|
| G-01 | chiusa il 20/09/2026 (era bloccante) | sprite delle icone non ben formato (`--` in un commento XML): nessuna icona disegnata | `static/img/icons.svg` | fatto dall'owner: commento riformulato; 546 icone disposte e 0 vuote nel report delle catture (§13) |
| G-02 | chiusa il 20/09/2026 (era bloccante) | `backdrop-filter` su `.site-header` lo rendeva containing block di `.nav-drawer` e `.nav-overlay`: drawer alto 65 px, overlay 0 px | `static/css/components.css` | fatto dall'owner: velo spostato su `.site-header::before` (§1.4); drawer alto quanto lo spazio disponibile (§11.2) |
| G-03 | alta (RTL) | stringhe d'identità latine non isolate in arabo: «™Italy Legal Entry» nel footer, promotore troncato all'inizio nella barra | `static/css/base.css`, `apps/cms/templatetags/cms_nav.py` | `dir="ltr"` nel tag `brand`, `<bdi>` su promotore e riga del ©, e divieto di `text-overflow: ellipsis` su testo d'identità (§15.5) |
| G-04 | alta (bloccante senza JS sotto 80rem) | senza JS, sotto 80rem, l'header sticky contiene l'intero menu: **781 px**. A 390 × 844 restano 63 px di pagina visibili, a 1024 × 768 nessuno | `static/css/components.css` | `html.no-js .site-header { position: static; }` dentro `@media (max-width: 79.999rem)` |
| G-09 | chiusa il 21/09/2026 | le numerazioni decorative erano in bronzo a 3.83:1, sotto la soglia del testo | `static/css/tokens.css` | chiusa dalla redirezione: il bronzo non esiste più e gli ordinali sono in `--rubric`, 6.92:1 sulla carta — sicuri come testo a qualunque corpo (§5) |
| G-13 | bassa | `id` derivato dal titolo in `cta_panel.html`; `id` fisso in `hero.html` | `templates/components/cta_panel.html`, `templates/components/hero.html` | accettare un parametro `id` |
| G-14 | bassa | separatore « : » francese generato in CSS dopo `<dt>` in `.meta-row` | `static/css/components.css` | spostare il separatore nel template, tradotto |
| G-15 | chiusa il 21/09/2026 | `--font-mono` nominava IBM Plex Mono, che non era self-hosted: il registro tecnico era il monospazio di sistema | `static/css/tokens.css` | chiusa dalla redirezione: `--font-ref` nomina Fira Mono, i cui due file sono in `static/fonts/` e dichiarati in `static/css/fonts.css` (§6.2) |
| G-16 | chiusa il 20/09/2026 | `docs/I18N_RTL.md` era citato dai CSS e dai cataloghi ma non esisteva | `docs/` | il documento è stato scritto: `docs/I18N_RTL.md` |
| G-19 | bassa | le FAQ usano `.accordion__panel`, classe che il design system non definisce (il componente usa `.accordion__body`) | `templates/faq/_item.html` | usare `.accordion__body` |
| G-20 | bassa | `.reveal--stagger` non produce uno scaglionamento visibile e ritarda l'hover dei figli | `static/css/components.css` | la direzione cancella `.reveal` per intero (§12): il difetto sparisce con il modificatore |
| G-21 | bassa | `remember` delle tab scrive in `localStorage` ma non rilegge | `static/js/main.js` | leggere `tabs:<chiave>` all'inizializzazione oppure rimuovere l'opzione |
| G-22 | media — chiusa il 20/09/2026 | due fogli dello Stage 1 erano fuori sistema: token inesistenti con ripieghi esadecimali, `linear-gradient`, anello di focus proprio a 3.01:1 | `apps/forum/static/forum/forum.css`, `apps/orientation/static/orientation/wizard.css` | fatto dagli owner: solo token reali, fondo piatto, focus di `base.css` |
| G-23 | media | a drawer aperto e pagina non scrollata l'overlay è dipinto sopra la fascia bassa dell'header (parte da 72 px, l'header finisce a 113 px): wordmark e bottone «Menu» velati | `static/css/components.css`, `static/js/main.js` | far consumare `--chrome-block-size` anche a `.nav-overlay` invece di scrivere `--nav-drawer-top` sul solo drawer (§11.5) |
| G-24 | chiusa il 21/09/2026 (era media) | `templates/base.html` precaricava per le pagine LTR due woff2 che la redirezione aveva cancellato (`ibm-plex-sans-400-normal-latin.woff2`, `ibm-plex-serif-500-normal-latin.woff2`): due 404 per pagina e nessun preload utile | `templates/base.html` | fatto: le pagine LTR precaricano ora `newsreader-200-800-normal-latin.woff2` e `fira-sans-500-normal-latin.woff2`, quelle RTL `noto-naskh-arabic-400-700-normal-arabic.woff2` e `ibm-plex-sans-arabic-400-normal-arabic.woff2` (§6.4) |
| G-25 | chiusa il 21/09/2026 (era media) | sei custom property erano consumate da quattro fogli e **non erano dichiarate da nessuna parte**: lo shim non le aveva mappate, quindi ogni `var()` cadeva sul valore iniziale — una transizione perdeva la curva, una misura perdeva il tetto e tre livelli di `z-index` valevano `auto` | `static/css/_legacy-tokens.css` | fatto: le sei righe sono state aggiunte allo shim, mappate sui token di §3 (§17); `tests/frontend/test_css_tokens_exist.py::test_every_referenced_custom_property_is_defined` passa su tutti i fogli e i due fogli delle app sono tornati conformi (§2.1) |
| G-26 | media (processo) | tre cancelli dichiarati dalla direzione non hanno ancora un test e non sono soddisfatti da `components.css`: nessun `box-shadow` fuori da `.nav-drawer` e `dialog` (restano otto dichiarazioni che nominano i token d'ombra, anche se valgono `none`), `border: 1px` solo su controlli e `dialog`, e il livello `@media (forced-colors: active)`, che `register.css` ha e `components.css` no. Manca inoltre la cattura a colori forzati nella matrice degli screenshot | `static/css/components.css`, `docs/qa/design/capture.py`, `tests/frontend/` | estendere a `components.css` il livello a colori forzati di `register.css` durante la sua migrazione, e scrivere i tre test con esso (§20) |
| G-27 | chiusa il 21/09/2026 (era bassa) | `.plate--verso .folio__ordinal` dipingeva l'ordinale del folio in `--rubric-on-navy`, che vale 4.46:1 sul navy: sotto `md` il numerale è di 22–24 px, quindi non è testo grande e mancava la soglia di 4.5:1 per 0.04, contro la regola «solo filetto, mai testo» della direzione | `static/css/register.css` | fatto: dentro una fascia verso il numerale è `--paper-on-navy` e la rubrica su navy è rimasta il solo filetto; le cinque dichiarazioni che la consumano in `static/css/` sono tutte bordi (§5) |

*Nota sul conto alla rovescia.* `tests/frontend/test_legacy_token_shim.py` esiste dal 21 settembre
2026 e tiene i tetti: 153 token, 14 classi e 1 636 usi complessivi dei nomi ritirati in
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
