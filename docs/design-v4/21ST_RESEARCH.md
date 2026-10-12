# 21st.dev — ricerca per componente strategico (V4)

Data: 24 settembre 2026, ore 20:40–20:55 · Strumento: MCP `mcp__21st__search` (metadati, gratuito;
`get_usage` → `tier: paid`, ricerche illimitate) · Nessuna generazione AI usata (consuma crediti del
committente) · Il codice di un candidato si recupera con `get_component` **solo** quando il pattern è
stato scelto e va adattato — e viene **riscritto** in HTML/CSS/Motion del design system ILE, mai
copiato: la CSP (`script-src 'self'`, `style-src 'self'`) e il vincolo «Django resta il cuore» escludono
componenti React/Tailwind così come sono.

Regola di lettura (§10 della direttiva): ogni componente è **materia prima**. Si distilla il pattern
— struttura, gerarchia, grammatica d'interazione, moto — e si ricompone nel linguaggio ILE. Nessun
candidato è «coerente così com'è», perché tutti sono shadcn/Tailwind/React; l'adattamento è la regola,
non l'eccezione.

Legenda «BEST PATTERN»: il candidato il cui *comportamento* è il più vicino a ciò che serve, non il più
bello nella preview.

**Nota dopo il chiarimento del committente (20:58).** Gradienti, sfondi a strati, luce mesh/radiale,
blur, vetro controllato, superfici arrotondate, ombre più ricche, spotlight, Motion avanzato e SVG
animato sono **autorizzati** quando usati professionalmente; le regole visive precedenti (niente
ombre, raggio 2 px, niente vetro) non vincolano più. I «respinti» qui sotto restano respinti **per
la ragione scritta accanto** — effetto senza informazione, infantile, AI-generico, loop su un
indicatore di stato — non perché un effetto sia moderno. Dove un candidato era stato scartato per
una regola V2 ormai revocata, la voce è stata riletta: lo spotlight che segue il puntatore (cat. 18)
e il vetro sul pannello dell'hero/login (cat. 6, 9) sono ora **ammessi** e il Creative Director
decide dove.

---

## 1. App shell / sidebar / navigation rail

**SEARCH QUERY:** `app shell sidebar navigation rail collapsible icons dashboard layout`
**CANDIDATES REVIEWED (10):** Animated Sidebar (starc007, #29334) · Sidebar with Search and Profile
(uiable, #28489) · Dashboard Sidebar «Charcoal Ink / Alabaster» (arunjdass, #14941) · Dashboard with
Collapsible Sidebar (uniquesonu, #5556) · Sidebar with Browser-like Tabs (arunachalam, #9748) · Sidebar
Light (inference-sh, #19361) · Sortable Sidebar Navigation (sean0205, #29833) · Animated Sidebar with
spring highlight + animated active bar (unlumen, #21517) · SidebarShowcase (ruixen.ui, #8252) · WhatSaaS
App Shell (jasonmohab-ali, #14820).
**BEST PATTERN:** starc007 #29334 per la **meccanica** (rail di icone su desktop che si espande in
sidebar, foglio con gestione del fuoco su mobile) + unlumen #21517 per l'**indicatore attivo animato**
(una barra che scorre fra le voci, evidenziazione a molla sul hover).
**WHY:** è l'unica coppia che copre insieme i quattro requisiti di §15 — icone coerenti, stato attivo
premium con indicatore animato, collasso, strategia mobile — senza pannelli promozionali, badge
inventati o «upgrade to pro».
**ADAPTATION FOR ILE:** rail 64 px con icone dello sprite ILE + etichetta al passaggio/espansione;
gruppi semantici («Parcours», «Dossier», «Communications», «Espace»); indicatore attivo = una barra
verticale che **trasla** fra le voci (Motion `animate` su `translateY`, 240 ms `--ease-layout`);
collasso persistito in `localStorage` (convenienza per-visitatore); su ≤1024 px diventa il cassetto
già esistente. Contatori **solo** da dati reali (documenti «à fournir», messaggi non letti). Niente
avatar finti nel piede: la voce account resta nella barra di contesto in alto.

## 2. Data table / righe con stato e azioni

**SEARCH QUERY:** `data table rows status badge row actions sticky header sortable`
**CANDIDATES REVIEWED (10):** Data Table (ephraimduncan, #28327) · Team Members Data Table (7ovr,
#25151, TanStack) · Card Frame Table (cnippet, #22188) · Payments Table (bundui, #25160) · Card Table
(felipemenezes098, #22174) · Invoice History Table (cnippet, #22187) · Data Table Skeleton (cnippet,
#19002) · Payments Table with Cell Selection (bundui, #25169) · Streaming Data Rows (rmahammad, #29368)
· Sortable Table (ddoemonn, #23561).
**BEST PATTERN:** ephraimduncan #28327 (menu azioni per riga, pastiglie di stato, intestazione, paginazione)
+ ddoemonn #23561 per le **righe che si riordinano animate** (FLIP) + cnippet #19002 per lo
**scheletro** che rispecchia la tabella.
**WHY:** #28327 ha esattamente la gerarchia che §21 chiede (stato come chip, azione per riga in un
menu, non link sottolineati); #23561 mostra che l'ordinamento può essere una transizione di layout e
non un salto; #19002 dà uno scheletro «vero» per le viste dello staff dove il caricamento esiste.
**ADAPTATION FOR ILE:** la tabella resta **semantica** (`<table>`, `caption`, `scope`) dove è una
tabella (viste staff, registri lunghi); riga con hover di superficie (livello 1 di profondità), riga a
fuoco con anello, chip di stato V3 (già ricostruita), **menu azioni** a fine riga in un popover del
sistema (§27), intestazione appiccicosa dentro `.scroll-x`. Per la collezione documenti dell'utente
**non** si usa la tabella: si usa il *document workspace* (§16 → categoria 8 qui sotto).

## 3. Chip / badge di stato

**SEARCH QUERY:** `status chip badge semantic icon label pill system`
**CANDIDATES REVIEWED (10):** HeroUI Chip (#13843) · Status con punto pulsante (diceui, #25393) ·
Interfaces Badge (jshguo, #11843) · Pill (haydenbleasel, #1600) · coss Badge 8 varianti semantiche
(#11356) · Badge (sean0205, #3558) · Styled Badges (ai2, #29986) · Status Badge (#4869) · HeroUI Badge dot
(#13824) · Astryx Badge di Meta (#17206, varianti semantiche + palette).
**BEST PATTERN:** coss #11356 (8 varianti semantiche, 3 misure, icona, polimorfico) per il **contratto**;
Astryx #17206 per la **separazione fra semantica e categoria** (neutral/info/success/warning/error
distinti dai colori di tag).
**WHY:** entrambi trattano il chip come **sistema** (varianti × misure × icona) e non come un pallino
colorato; nessuno dei due usa il colore da solo.
**ADAPTATION FOR ILE:** la vidimazione V3 (`static/css/v3/chip.css`) resta il fondamento **semantico**
— parola in inchiostro, registro nel filetto, mai un verdetto — ma la **forma** cambia secondo §17 e
§40: raggio `full` (pillola), padding 4/10, icona 14 px dal sprite per registro (clock · warning ·
check · close · minus), corpo semi-trasparente, bordo 1 px della marca. Le sette forme restano
distinguibili senza colore (stile e geometria del filetto diventano stile e geometria del **bordo**).
Il «punto pulsante» di diceui è **respinto**: un loop animato su un indicatore di stato è rumore
(MOTION §3), e un dossier non è «online».

## 4. Caricamento file

**SEARCH QUERY:** `file upload dropzone drag drop progress preview`
**CANDIDATES REVIEWED (8):** File Dropzone (joyco, #19201) · File Upload with Preview (ephraimduncan,
#18108) · UploadThing Dropzone (#18847) · Image Preview Dropzone (#18045) · Upload Dropzone Empty State
(#29988) · Animated File Upload (educalvolpz, #18031) · File Upload «Documents & Signing» (uvain, #27137)
· File Upload con border-beam (extend-hq, #15587).
**BEST PATTERN:** uvain #27137 — «gestisce le tre cose che succedono davvero: tipo sbagliato, file
troppo grande, trasferimento fallito a metà — progresso per file, riprova, guardie che si spiegano».
**WHY:** è l'unico pensato per **documenti firmati/legali** e non per gallerie di immagini; copre
errore, sostituzione e riprova, che §29 elenca.
**ADAPTATION FOR ILE:** dropzone grande su superficie livello 1 con bordo tratteggiato che diventa
pieno al trascinamento (`--motion-fast`), pulsante «Parcourir» del sistema, elenco file con stato
(in coda · in carico · analisi antivirus · accettato · errore) come chip V3, barra di progresso reale
(`<progress>`), versioni precedenti in un `<details>`. Niente anteprime immagine per i PDF: tipo +
nome + dimensione + hash corto. Il «border beam» animato di extend-hq è **respinto** (effetto
gratuito).

## 5. Navbar premium / mega-menu

**SEARCH QUERY:** `premium navbar sticky blur mega menu scroll state`
**CANDIDATES REVIEWED (10):** Morphing Scroll Navbar (laziekiki, #27428) · Header 1 scroll-blur (efferd,
#8964) · Navbar Section 2 con mega-menu a espansione (solaceui, #18120) · Sticky Header Navbar a pillola
(diarmuradi, #27109) · Navbar Menu «bignav» (Aceternity, #1024) · Navbar 1 flottante (preetsuthar17,
#2046) · Navbar hover (#620) · Scroll Navigation Menu (#3910) · Header 3 con cassetto mobile e menu
annidati (efferd, #8971) · Navbar 5 con dropdown a 2 colonne (shadcnblocks, #2307).
**BEST PATTERN:** efferd #8971 per la **struttura** (sticky, blur allo scroll, cassetto mobile animato,
menu annidati) + solaceui #18120 per il **mega-menu che si espande** dal bordo della barra invece di
un dropdown flottante.
**WHY:** #8971 è il più completo sui requisiti di §13 (sticky, blur, cassetto, annidamento) senza
diventare una «pillola» galleggiante da landing page (#27109, #2046: **respinti**, leggono «SaaS
generico»); #18120 dà la sensazione di prodotto — la barra si apre, non spunta un rettangolo.
**ADAPTATION FOR ILE:** la carta intestata V2 resta (lock-up ufficiale a sinistra, lingua e accesso a
destra); allo scroll la barra passa a 56 px con `backdrop-filter` **solo qui** (§38) e un filetto
inferiore che appare; il mega-menu si **espande** sotto la barra a tutta larghezza con tre colonne
(voci · descrizione breve · una fotografia curata per sezione), entrata 240 ms `--ease-enter`, uscita
120 ms; l'indicatore della voce attiva **trasla**; su ≤1279 px il cassetto già esistente, con la stessa
gerarchia. La ricerca pubblica entra come pannello (categoria 21).

## 6. Layout di autenticazione

**SEARCH QUERY:** `login page split layout brand panel institutional authentication`
**CANDIDATES REVIEWED (8):** Split Login con aside animato e citazione (hirael, #28369) · Sign In Split
Screen (felipemenezes098, #19050) · Auth Section 2 (solaceui, #20036) · login minimalista (ephraimduncan,
#2428) · Login due colonne (lavikatiyar, #9106) · Auth Section 1 con pannello grain-gradient (solaceui,
#20035) · Sign Up Split Panel (diarmuradi, #28171) · Auth Page (efferd, #7014).
**BEST PATTERN:** hirael #28369 — lato sinistro con marchio e un solo messaggio, destra con il modulo; +
solaceui #20035 per il **materiale** del pannello (gradiente a grana, non fotografia stock).
**WHY:** §46 chiede «brand/motion visual + form», fiducia e chiarezza, e vieta la carta centrata
generica; #28369 è quello con meno rumore (nessun social login, nessuna testimonianza inventata).
**ADAPTATION FOR ILE:** pannello sinistro = capitolo mezzanotte con la **porta ad arco** (asset
ufficiale) e il territorio a isoipse *fermo* (movimento ridotto = completo), un solo testo: il titolo
bloccato; destra = modulo su carta con campi V4 (altezza 48, etichette visibili, errore inline),
pulsante primario V4, secondo fattore dove richiesto. **Niente** social login, citazioni, testimonianze,
foto di persone.

## 7. Bottoni

**SEARCH QUERY:** `button system variants primary secondary ghost destructive loading icon sizes`
**CANDIDATES REVIEWED (8):** Button fluid (micka_design, #10319) · coss Button 7 varianti/10 misure
(#11387) · cnippet Button (#18666) · HeroUI Button (#13641) · Interfaces Button (jshguo, #11857) · Button
(saurabh, #24395) · originui Button (#140) · Astryx Button (#17231).
**BEST PATTERN:** coss #11387 per la **matrice** varianti × misure × loading; HeroUI #13641 per
`danger-soft` (la variante distruttiva **morbida**, non una lastra rossa) e lo stato `pending`.
**WHY:** §12 chiede PRIMARY, SECONDARY, SOFT, OUTLINE, GHOST, LINK, DESTRUCTIVE, ICON con loading e
success; solo #11387 e #13641 ne coprono l'insieme; #13641 conferma che il distruttivo può essere
morbido, che è la scelta già fatta in V3.
**ADAPTATION FOR ILE:** il sistema V3 (`v3/buttons.css`, misurato) evolve in V4: raggio `md` (8 px)
invece di 2, altezza 44/40/52, **SOFT** nuovo (accento al 10 % con testo accento), OUTLINE = l'attuale
secondario, GHOST senza bordo, loading con il misuratore a tacche (già specificato) e stato success
(spunta 400 ms poi ritorno), ombra di livello 1 **solo** sul primario (§39, ruolo definito), luce
verticale già in V3. Icona 20 px sinistra/destra con spaziatura ottica.

## 8. Righe / schede documento (document workspace)

**SEARCH QUERY:** `document list file manager rows metadata expandable actions`
**CANDIDATES REVIEWED (8):** File List Item con menu di overflow (felipemenezes098, #28496) · File Tree
View (cnippet, #24877) · Table Row Actions (#23696) · File Actions Menu con scorciatoie (cnippet, #23640)
· Expand Menu (unlumen, #25320) · Item List with Actions (bundui, #28596) · Tree View accessibile
(ddoemonn, #23573) · Item Action List (sean0205, #28284).
**BEST PATTERN:** #28496 (riga: icona · nome · metadati · menu di overflow) + #28284 (riga: icona ·
titolo+descrizione · azione) — la **riga documento** di §16 è l'unione dei due.
**WHY:** nessun candidato è un «document workspace» completo (non esiste su 21st per un caso legale);
la riga è il pattern giusto, e i due candidati mostrano le due metà — identità+metadati e
descrizione+azione.
**ADAPTATION FOR ILE:** `DocumentRow` V4: [identità: tipo con glifo · titolo · versione] [stato: chip
V4] [responsabile: glifo attore + tipo + nome] [scadenza con urgenza progressiva] [salute: scadenza /
revisione] [azione primaria: bottone] [menu secondario: popover]. Riga espandibile (`<details>`) per
motivazione di rifiuto e cronologia versioni. Su mobile → `DocumentCard` impilata (§61). Testata del
workspace con conteggi **reali** e filtro segmentato (categoria 15).

## 9. Modale e cassetto

**SEARCH QUERY:** `modal dialog drawer sheet overlay blur focus trap premium`
**CANDIDATES REVIEWED (8):** Modal accessibile (ddoemonn, #23539) · Reshaped Modal (#17825, posizioni
center/bottom/start/end/full) · Smooth Drawer (kokonutd, #25000) · Drawer trascinabile (ddoemonn,
#23558) · Animated Dialog → bottom sheet su mobile (rmahammad, #26905) · Dotted Dialog (#1462) · Modal
che diventa Drawer per dimensione (efferd, #4514) · Center Morph Modal (starc007, #29357).
**BEST PATTERN:** rmahammad #26905 (coreografia enter/exit scala+scorrimento, **foglio inferiore su
mobile**, testata e piede fissi con corpo scorrevole) + Reshaped #17825 per il cassetto laterale con
la stessa API.
**WHY:** §25 e §26 chiedono esattamente questi due comportamenti; #26905 è l'unico con la variante
mobile a schermo intero e la struttura header/body/footer.
**ADAPTATION FOR ILE:** il `<dialog>` nativo resta (focus trap, Esc, inert gratis); V4 gli dà
composizione generosa (testata con glifo di contesto e chiusura, corpo, piede con azioni), scrim con
`backdrop-filter` (§38), entrata 240 ms scala .96→1 + dissolvenza, uscita 160 ms; su ≤640 px foglio
inferiore. Il cassetto = stesso `<dialog>` posizionato a fine riga (`inset-inline-end: 0`),
scorrimento 320 ms `--ease-enter`. Il morph dal centro (#29357) è **respinto**: spettacolo per un
atto di conferma.

## 10. Command menu / ricerca globale

**SEARCH QUERY:** `command palette global search menu keyboard`
**CANDIDATES REVIEWED (6):** Command Menu with Global Search (ephraimduncan, #27378) · Command Palette
(ddoemonn, #23522) · Command Palette Raycast-like (rafa-porto, #2075) · Command Menu (preetsuthar17,
#4430) · Search Modal (efferd, #8115) · Command Menu a pillola (serafimcloud, #23173).
**BEST PATTERN:** #27378 — tipi di risultato filtrabili, sezioni «recenti», ricerca fra oggetti
dell'app.
**WHY:** è l'unico orientato agli **oggetti** (documenti, progetti) e non alle sole azioni; la
piattaforma cerca fascicoli, pièce, richieste.
**ADAPTATION FOR ILE:** Ctrl/⌘ K **solo per i ruoli staff** (decisione del Council già presa),
risultati **permission-aware** (la stessa queryset delle viste, mai un oggetto fuori portata: 404,
mai 403), gruppi per tipo con glifo, frecce e Invio, Esc. Per la persona: ricerca semplice nel
registro documenti. La pillola che cresce (#23173) è **respinta**.

## 11. Timeline / stepper / avanzamento

**SEARCH QUERY:** `timeline stepper journey progress vertical steps status`
**CANDIDATES REVIEWED (6):** Vertical Titled Stepper (sean0205, #29815) · Stepper (sean0205, #3734) ·
Vertical Descriptive Stepper (#29866) · Basic Stepper (#29925) · Animated Progress Stepper con linea a
molla e punto viaggiante (shadcnspace, #28558) · Stepper (corr, #28565).
**BEST PATTERN:** #29866 (verticale, titoli + descrizioni + icona che diventa spunta) per il
**binario del percorso** del fascicolo; #28558 per la **linea che avanza** (una sola volta, non in
loop).
**WHY:** §48 chiede «dynamic journey rail» che risponda a *dove sono / cosa manca / chi è
responsabile*: il verticale descrittivo porta responsabile e descrizione; la linea animata dà il
momento firmato senza spettacolo continuo.
**ADAPTATION FOR ILE:** `JourneyRail` V4: le 7 tappe bloccate, ogni tappa con responsabile (glifo
attore), stato come chip, «Vous êtes ici» come nodo attivo con anello; la linea si disegna una
volta al caricamento (`--motion-emphasized`, `pathLength`), poi ferma; sotto 1024 px orizzontale
compatta. Il «punto pulsante» di #28558 è **respinto**.

## 12. Stati vuoti

**SEARCH QUERY:** `empty state illustration action contextual`
**CANDIDATES REVIEWED (6):** Empty State (serafimcloud, #1435) · Interactive Empty State (#22301) ·
Empty componibile (cnippet, #19745) · Empty Background (uiable, #18266) · Empty State con marquee di
scheletri (#19377) · Empty State Kit — sei stati (laziekiki, #27024).
**BEST PATTERN:** cnippet #19745 (componibile: media · titolo · descrizione · azioni) + laziekiki
#27024 per la **tassonomia** (inbox, ricerca, pagina mancante, accesso negato, superficie vuota).
**WHY:** §57 vuole visuale + spiegazione + azione, senza illustrazioni infantili; la tassonomia
evita di reinventare cinque stati diversi.
**ADAPTATION FOR ILE:** `EmptyState` V4 con un **glifo grande del sistema** (documento, cartella,
lente, scudo) su superficie livello 0 con bordo tratteggiato, titolo UI, una frase, un'azione
primaria; sei varianti nominate. Il marquee di scheletri (#19377) è **respinto** (moto senza
informazione).

## 13. Hero — percorsi SVG e nodi

**SEARCH QUERY:** `hero animated svg paths connected nodes routes diagram`
**CANDIDATES REVIEWED (8):** Hero Section «Animated Roadmap» (ravikatiyar162, #8113 e #8111) ·
Animated SVG Background (uniquesonu, #5800) · Path drawing (motion.dev ufficiale, #24528) · Animated SVG
Text Path (#2485) · SVG Path Drawing Text (#2786) · Path Drawing Portfolio Hero (#26183) · Line Draw SVG
(pulkitxm, #18352).
**BEST PATTERN:** motion.dev #24528 (il tracciato che si disegna con `pathLength`, esempio ufficiale
della libreria già in uso) + #8113 per l'idea delle **tappe su un percorso** che si rivelano allo
scroll.
**WHY:** §31 chiede quattro vie che attraversano l'arco e proseguono: è geometria di percorso, non
sfondo decorativo; #5800 (linee casuali che si disegnano e svaniscono) è **respinto** perché è
esattamente la «decorazione pseudo-tecnica» di §5.
**ADAPTATION FOR ILE:** quattro tracciati distinti (Personne · Entreprise · Institution ·
Université/Formation) da quattro nodi d'origine, attraverso l'arco della porta (asset ufficiale),
verso i servizi; si disegnano una volta (`--motion-emphasized`), hover/focus/tap su un pubblico →
la sua via si accende e le altre si attenuano, appare l'etichetta ancorata e la CTA relativa si
evidenzia; etichette come legende ai margini su mobile. Nessuna coordinata, nessun «svg».

## 14. Tabs / controllo segmentato

**SEARCH QUERY:** `tabs segmented control animated indicator filter`
**CANDIDATES REVIEWED (6):** Segmented Tabs con fondo scorrevole e hover fluido (micka_design,
#26923) · Segmented Control Tabs (cnippet, #24931) · Segmented Control accessibile (radiogroup, frecce)
(ddoemonn, #23552) · Animated Tabs underline/pill/segment (educalvolpz, #24930) · Animated Tabs clip-path
(#1962) · Filter Grid con conteggi live e reflow (ddoemonn, #23525).
**BEST PATTERN:** ddoemonn #23552 per la **semantica** (radiogroup, frecce, controllato/non
controllato) + micka_design #26923 per il **fondo che scorre** sotto la voce scelta.
**WHY:** §24 e §23 chiedono il filtro segmentato (Tous / À fournir / En examen / …) con moto sottile
sulla selezione; #23552 è l'unico accessibile per costruzione.
**ADAPTATION FOR ILE:** `SegmentedControl` V4 = `<fieldset>` di radio nativi con etichette visive,
un «thumb» che trasla (Motion, 180 ms `--ease-layout`), conteggi reali fra parentesi, tastiera
nativa. Le tab del sistema (già WAI-ARIA) ricevono lo stesso indicatore scorrevole.

## 15. Tooltip / popover / menu

**SEARCH QUERY:** `tooltip popover dropdown menu context menu consistent surface`
**CANDIDATES REVIEWED (6):** Popover originui (#403) · Inline Dropdown (#2531) · Menu coss (#11561,
icone, scorciatoie, sottomenu, checkbox) · Smart Popover → cassetto su mobile (efferd, #4526) ·
Menubar Compact (uiable, #29428) · Dropdown Menu originui (#383).
**BEST PATTERN:** coss #11561 per il **contratto del menu** (icone, scorciatoie, gruppi, distruttivo
separato) + efferd #4526 per il **popover che diventa foglio** su mobile.
**WHY:** §27 chiede una sola famiglia di sovrapposizioni con superficie, ombra, bordo, raggio e moto
coerenti; #11561 mostra la ricchezza del contenuto, #4526 la strategia mobile.
**ADAPTATION FOR ILE:** una sola superficie di livello 3 (`--surface-3`, ombra ruolo 3, raggio
`lg`, bordo hairline) per tooltip, popover, dropdown e menu azioni; popover con Popover API
nativa (`popover` + `anchor`) dove Chrome la supporta, `<details>` come ripiego; entrata 120 ms
scala .98→1; il menu azioni di riga separa l'azione distruttiva con un filetto.

## 16. Centro notifiche

**SEARCH QUERY:** `notification center inbox unread read categories timestamp`
**CANDIDATES REVIEWED (6):** Notification Center Tabs — All/Unread/Mentions, «tutto letto» (7ovr,
#28432) · Notification Inbox Popover (ruixen.ui, #8245) · Notification Panel «visto vs trattato»
raggruppato per giorno (uvain, #27135) · Button with Unread Badge (#29964) · Activity Tabs With Unread
(7ovr, #28490) · Notification Center (#25496).
**BEST PATTERN:** uvain #27135 — distingue **ciò che hai visto da ciò che hai trattato**, raggruppa
per giorno, filtra per tipo.
**WHY:** §55 chiede letto/non letto, categoria, priorità, orario; #27135 è l'unico che pensa la
notifica come un atto da trattare, coerente con una piattaforma dove ogni notifica ha un
responsabile.
**ADAPTATION FOR ILE:** pannello dal campanello della barra di contesto (livello 3), gruppi per
giorno, filtro per categoria (dossier · documenti · messaggi · scadenze), riga con glifo di
categoria, titolo, orario tabulare, punto «non letto», azione «segna come letto»; la pagina
`/notifications/` esistente ne è la versione intera. Nessun conteggio finto.

## 17. Schede opzione (wizard)

**SEARCH QUERY:** `selectable option cards radio tiles wizard choice icon description`
**CANDIDATES REVIEWED (6):** Icon Card Radio Group 2×2 (sean0205, #28351) · Glass Radio Group (#5408)
· Styled Radio Group (ai2, #28307) · Choicebox (shugar, #3944) · Radio Group in Card con separatori
(#28339) · Select con icone (originui, #287).
**BEST PATTERN:** shugar #3944 «Choicebox» — radio/checkbox grande con più dettaglio e area di tocco
generosa.
**WHY:** §50 chiede stato di selezione, glifo, titolo, spiegazione, tastiera; il choicebox è l'unico
che nasce come **controllo di modulo** (radio nativo) e non come card cliccabile.
**ADAPTATION FOR ILE:** `OptionCard` V4 = `<label>` intorno a un `<input type=radio>` nativo; superficie
livello 1, raggio `lg`, glifo del sistema, titolo UI, una riga di spiegazione; selezionata = bordo
accento 2 px + spunta + leggero sollevamento (livello 2); focus = anello di sistema; il vetro
(#5408) è **respinto** (§38: niente vetro sulle card).

## 18. Pannelli interattivi / card

**SEARCH QUERY:** `interactive panel card hover lift spotlight border light premium`
**CANDIDATES REVIEWED (6):** Spotlight Card (preetsuthar17, #2220) · Spotlight che segue il cursore
(ibelick, #1500) · Spotlight Card (jahed, #2487) · Card Spotlight (Aceternity, #986) · Animated Feature
Spotlight 3D (ruixen, #8591) · Hover Card shadcn (#216).
**BEST PATTERN:** ibelick #1500 — una **luce che segue il puntatore** sul bordo/superficie, sottile.
**WHY:** §41 ammette «spotlight» e «light» come effetti di hover; #1500 è il più contenuto; il 3D
(#8591) e il gradiente radiale pieno (#986) sono **respinti** (§78: «troppo»).
**ADAPTATION FOR ILE:** `Panel` V4 livello 1 con hover = sollevamento a livello 2 (ombra ruolo 2) +
bordo che si schiarisce; **spotlight solo** sui pannelli delle quattro vie in home (IMMERSIVE),
mai sul cruscotto (§67: dashboard MICRO/INTERACTIVE). Implementato con `--mx/--my` aggiornate da
un listener `pointermove` con `requestAnimationFrame`, radiale al 6 % dell'accento.

## 19. Toast

**SEARCH QUERY:** `toast notification system success error stacked accessible live region`
**CANDIDATES REVIEWED (6):** Animated Toast (dev.shejanmahamud, #28245) · Toast Base UI impilato con
azioni e posizioni (cnippet, #24297) · Toast Notification a molla (framecn, #19994) · Alert (#334) ·
Stacked Alerts Frame (#29367) · Dismissible Alert Stack (7ovr, #26527).
**BEST PATTERN:** cnippet #24297 — pila con timeout, pulsante d'azione, icona di stato, posizioni.
**WHY:** §56 chiede quattro tipi, effimero, regione live accessibile; #24297 è il più completo e il
meno teatrale.
**ADAPTATION FOR ILE:** i messaggi Django (`messages`) diventano toast V4 in `role="status"`
(`aria-live="polite"`, l'errore in `role="alert"`), in basso a fine lettura, chip di stato V3 come
icona, chiusura, timeout 6 s con pausa al hover/focus, entrata 240 ms dal basso; i messaggi che
devono restare (esito legale) restano `notice` nella pagina.

## 20. Progress / avanzamento documenti

**SEARCH QUERY:** coperta da 11 (stepper) e 2 (tabella): «document health strip» di §16.
**CANDIDATES REVIEWED:** i sei stepper + «Streaming Data Rows» (#29368) per il **morphing dei
numeri** — **respinto**: MOTION §2 ammette il numero che scorre solo per un totale calcolato.
**BEST PATTERN:** nessun candidato dedicato; il pattern è una **striscia di conteggi** (7 richiesti · 1
convalidato · 4 in attesa · …) come segmenti proporzionali.
**ADAPTATION FOR ILE:** `HealthStrip` V4: una barra segmentata a sei registri (conforme · neutro ·
attesa · azione · rifiuto · nullo) con larghezze dai conteggi reali, etichette con cifra tabulare,
ogni segmento cliccabile = filtro. Dati solo dal registro (§90).

## 21. Ricerca pubblica

**SEARCH QUERY:** `site search overlay panel results grouped keyboard public website`
**CANDIDATES REVIEWED (5):** Sidebar ricercabile con gruppi (uiable, #19371) · Search Tool con risultati
raggruppati (serafimcloud, #12365) · URL Search Group (#29166) · Searchable FAQ Accordion (cnippet,
#24932) · Autocomplete Base UI (coss, #11338).
**BEST PATTERN:** cnippet #24932 (filtra in tempo reale un elenco già in pagina) + coss #11338 per
l'**autocomplete accessibile** con gruppi.
**WHY:** §30 dice «pannello premium se giustificato»; il sito pubblico ha FAQ, glossario e pagine:
la ricerca che filtra ciò che è già in pagina (FAQ, glossario) è giustificata e senza backend nuovo;
un overlay globale pubblico no, finché non c'è un indice.
**ADAPTATION FOR ILE:** campo di ricerca nel mega-menu (pannello, non modale) con autocomplete sui
titoli delle pagine pubbliche (un JSON statico generato al build, permission-free perché pubblico),
gruppi per sezione, tastiera; nelle FAQ e nel glossario un filtro live. Nessun oggetto riservato.

## 22. CTA premium

**SEARCH QUERY:** `premium call to action section gradient light panel buttons`
**CANDIDATES REVIEWED (6):** Gradient CTA Banner (shadcnspace, #28147) · Gradient CTA Button con
ombre inset stratificate (mengto, #25501) · Animated Gradient Button (uiable, #29276) · Glassmorphism
CTA con bordo conico rotante (mengto, #25647) · Button Colorful (kokonutd, #3) · Floating Dots CTA
(mengto, #25583).
**BEST PATTERN:** #28147 per la **sezione** (fondo a gradiente morbido, titolo, testo, un bottone
primario) + #25501 per il **bottone**: gradiente caldo + ombre inset stratificate + velo che si
riempie al hover.
**WHY:** §33 chiede sezioni ad alta intensità e §12 un primario «chiaramente premium»; i due
candidati mostrano il materiale (gradiente + luce inset) senza particelle né bordi che ruotano.
**ADAPTATION FOR ILE:** il pannello CTA (`cta_panel`) V4 diventa una superficie di livello 2 con
fondo a gradiente di marca (navy evoluto → teal profondo, o il secondo accento caldo se il Creative
Director lo adotta), luce radiale in alto a sinistra, titolo UI, un primario V4 con gradiente
verticale di 8 % e ombra di livello 1; hover = il velo chiaro che si riempie (`--motion-standard`).
**Respinti:** il bordo conico rotante e i puntini che salgono (#25647, #25583) — moto senza
informazione; il bottone «colorful» (#3) — arcobaleno, AI generico.

---

## Sintesi per il Creative Director

- **Accettati come pattern** (da distillare): rail+indicatore animato (1), riga documento (8),
  segmentato accessibile (14), scelta a choicebox (17), pannello notifiche «visto/trattato» (16),
  dialog con foglio mobile (9), tracciato che si disegna una volta (13), toast in pila (19), split
  login sobrio (6), health strip (20).
- **Respinti con ragione**: punti pulsanti, border-beam, morph dal centro, 3D, marquee di scheletri,
  pillola galleggiante, linee SVG casuali, numeri che scorrono, bordi conici rotanti, particelle.
  Ognuno è «effetto senza informazione» (§78), «decorazione pseudo-tecnica» (§5) o «AI generico»
  (§75). Vetro, gradienti, spotlight e ombre ricche **non** sono in questa lista: sono materiale
  autorizzato, e il Creative Director decide dove e quanto.
- **Nessun componente viene installato** (`npx shadcn add` non gira qui): ciò che entra è HTML del
  template Django + CSS del design system V4 + Motion vanilla dove il moto lo richiede.
