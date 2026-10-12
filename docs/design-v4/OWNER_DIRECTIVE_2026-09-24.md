# DIRETTIVA PRIORITARIA DEL PRODUCT OWNER — 24 settembre 2026, ore 20:27

Copia fedele della direttiva ricevuta in sessione (100 sezioni). Supera le precedenti istruzioni
visuali dove sono in conflitto. Il testo è del committente; le sole modifiche sono la conversione
in Markdown e la numerazione dei titoli.

---

**Preambolo.** Non interrompere in modo pericoloso un test, una migration, una scrittura DB o
un'operazione atomica in corso. Termina l'operazione atomica corrente, crea un checkpoint Git
pulito e POI FERMA LA PROPAGAZIONE DELL'ATTUALE DESIGN. Il design visuale attuale NON è approvato.
Non continuare ad applicarlo ad altre pagine.

## 0. Evidenza concreta del problema

Il Product Owner sta osservando il lavoro direttamente in Chrome. Pagina rappresentativa:
`/fr/espace-reserve/mes-documents/`. Il risultato è troppo: editoriale; statico; piatto; semplice;
tradizionale; amministrativo; poco tecnologico; poco sofisticato; poco distintivo; poco premium;
poco «2026». Questa pagina è un ESEMPIO DI DESIGN NON ACCETTATO.

Problemi visivi osservabili: sidebar quasi esclusivamente testuale; app shell molto semplice; navbar
piatta; assenza di profondità; titolo serif enorme che domina come pagina editoriale; tabella
assimilabile a un documento amministrativo; azioni rese come normali link sottolineati; badge/status
quasi rettangolari e primitivi; assenza di affordance premium; assenza di card/panel/workspace
strutturati quando sarebbero utili; nessuna gerarchia sofisticata fra documenti, stati, scadenze e
azioni; poco feedback visuale; poca micro-interazione; quasi nessuna percezione di movimento; scarsa
separazione fra «informazione» e «azione»; pochissima sensazione di prodotto digitale contemporaneo.
Questo NON è il target.

## 1. Nuova regola: DESIGN FREEZE

Non estendere più l'attuale linguaggio UI ad altre schermate. Prima di continuare il rollout devi
creare e far approvare una nuova V4 visual foundation su un set limitato di pagine. Pagine campione
obbligatorie: 1. Homepage pubblica · 2. Navbar / mega navigation · 3. Login · 4. Dashboard Persona ·
5. Mes Documents · 6. Fascicolo Digitale · 7. Orientation Wizard · 8. Company Dashboard. Solo dopo il
PASS visuale di queste superfici puoi propagare il nuovo sistema.

## 2. Il problema non si risolve con «un po' più di CSS»

Non limitarti a: aumentare border-radius; aggiungere qualche box-shadow; mettere gradienti;
aggiungere hover; cambiare font; aggiungere animazioni isolate. È necessario ripensare: visual
hierarchy; composition; surface system; app shell; navigation; interaction grammar; density; motion
language; forms; table/list architecture; visual storytelling; micro-interactions; image/media
strategy. Serve un PRODUCT DESIGN REBASE, non un reskin.

## 3. Target esatto

Una piattaforma che, a colpo d'occhio, sembri progettata nel 2026 da un team senior internazionale.
Percezione: PREMIUM · ELEGANT · MODERN · DYNAMIC · POLISHED · INSTITUTIONAL-GRADE · LEGAL-TECH ·
TRUSTWORTHY · HIGH-END · INTUITIVE · MEMORABLE. Riferimento: «grande piattaforma digitale
internazionale». NON: «sito Django ben ordinato». NON: «portale amministrativo con font elegante».
NON: «editorial website».

## 4. Istituzionale non significa editoriale

L'equivalenza «istituzionale = editoriale + sobrio + serif + linee sottili + spazi vuoti» è SBAGLIATA
per questo progetto. Italy Legal Entry deve essere: istituzionale + digitale + tecnologico +
interattivo + sofisticato + premium. L'editorialità può esistere nelle pagine lunghe di contenuto.
NON deve dominare: dashboard; document workspace; wizard; case management; B2B; auth; strumenti
operativi.

## 5. Rimuovere elementi decorativi senza valore

Rilevati: «33.97° N · 6.85° W», «45.41° N · 11.88° E», «svg», «Suspendre le mouvement». Non devono
apparire automaticamente perché sembrano sofisticati. Regola: NO USER VALUE = REMOVE. Coordinate
geografiche SOLO se hanno una funzione reale, rappresentano un luogo pertinente e l'utente comprende
perché sono presenti. Non mostrare: coordinate casuali; jargon visuale; label di debug; nomi tecnici
SVG; controlli di animazione fuori contesto. «Suspendre le mouvement» può esistere come controllo di
accessibilità SOLO se realmente necessario, elegantemente integrato, dal significato chiaro;
altrimenti affidarsi a `prefers-reduced-motion`.

## 6. Nuovo modello di governance multi-agente

Il problema non è la mancanza di agenti: è la mancanza di una gerarchia creativa efficace. Struttura:
EXECUTIVE CREATIVE DIRECTOR → ART DIRECTION LEAD · PRODUCT DESIGN LEAD · UX LEAD · MOTION LEAD ·
FRONTEND ARCHITECT · DESIGN SYSTEM LEAD · PLATFORM UX LEAD · ACCESSIBILITY LEAD · PERFORMANCE LEAD ·
SPECIALIST REVIEWERS · IMPLEMENTATION SQUAD. Una sola figura, l'EXECUTIVE CREATIVE DIRECTOR, ha la
responsabilità finale della coerenza visuale. Nessun agente implementatore può auto-approvare il
proprio lavoro.

## 7. Agenti specialistici richiesti

CREATIVE: Executive Creative Director · Digital Art Director · Premium UI Director · Institutional
Digital Design Specialist · Brand Identity Designer · Visual Composition Specialist · Color/Material
Designer · Typography Specialist · Image Art Director. PRODUCT: Principal Product Designer · Legal-Tech
UX Specialist · Case Management UX Specialist · Public Service UX Specialist · Dashboard UX Designer ·
Complex Form UX Specialist · Document Workflow Specialist · Information Architect. MOTION: Motion
Design Director · Microinteraction Designer · SVG Motion Specialist · Scroll Interaction Specialist ·
Motion Performance Engineer. FRONTEND: Principal Django Frontend Architect · Senior CSS Systems
Engineer · Motion Engineer · React Island Engineer · 21st.dev Specialist · UI-UX-Pro-Max Specialist ·
Responsive Specialist. PLATFORM: App Shell Specialist · Navigation Specialist · Table/Data Grid
Specialist · Search & Command UX Specialist · Document Workspace Specialist · Onboarding Specialist ·
Notification/Inbox Specialist · B2B Product Designer. QA: Visual QA Lead · Chrome QA Specialist ·
Accessibility Reviewer · RTL Reviewer · Mobile Reviewer · Performance Reviewer · Independent Red Team
Designer.

## 8. UI-UX-Pro-Max — utilizzo dimostrabile

Non «installed» ma «changed these concrete decisions». Per ogni superficie campione una review via
UI-UX-Pro-Max in `docs/design-v4/UI_UX_PRO_MAX_AUDIT.md`: CURRENT PROBLEM · SKILL RECOMMENDATION ·
ACCEPTED · REJECTED · IMPLEMENTED. Esempio MES DOCUMENTS: information hierarchy, document workspace
pattern, action hierarchy, status treatment, responsive strategy, empty/error state strategy,
table/list recommendation.

## 9. 21st.dev — utilizzo dimostrabile

Per ogni componente strategico almeno 5 candidati utili. Categorie: premium navbar; mega-menu; hero;
button systems; interactive panels; document cards; status chips; file upload; tabs; drawers; modals;
data tables; contextual sidebar; app shell; command menu; search; timelines; progress visualization;
empty states; auth layouts; notification center. Per ogni categoria: SEARCH QUERY · CANDIDATES
REVIEWED · BEST PATTERN · WHY · ADAPTATION FOR ILE, in `docs/design-v4/21ST_RESEARCH.md`. Non copiare
un componente intero se non è coerente: distillare il pattern.

## 10. 21st.dev non deve trasformare ILE in shadcn generico

Componenti come materia prima. ILE non deve sembrare: shadcn default; Aceternity clone; Magic UI
demo; generic SaaS. Ogni componente: RECOMPOSED · RESKINNED · ADAPTED · INTEGRATED nel design system.

## 11. Motion come sistema, non come patch

MOTION SYSTEM V4. Token: motion-fast · motion-standard · motion-emphasized · motion-slow ·
spring-soft · spring-snappy · ease-enter · ease-exit · ease-layout. Pattern: page enter · panel enter
· panel swap · modal · drawer · nav · hover · press · list insert · status change · wizard · file
upload · loading · tooltip · tab transition. Il moto deve sembrare appartenere allo stesso prodotto.

## 12. Button system — rifarlo completamente

I bottoni attuali non sono accettati. Varianti: PRIMARY · SECONDARY · SOFT · OUTLINE · GHOST · LINK ·
DESTRUCTIVE · ICON · FLOATING/CONTEXTUAL dove utile. Requisiti: curvatura moderna (non
necessariamente pill); radius coerente; ottima hit area; icon placement; hover; active/pressed;
focus; loading; success; disabled; subtle motion; shadow/light dove appropriato. Il PRIMARY deve
essere chiaramente premium. No rettangoli HTML con bordo quasi inesistente.

## 13. Navbar — completo redesign

Signature component. PUBLIC NAV: premium sticky; subtle transparency/blur; animated background on
scroll; active-state motion; sophisticated language control; account entry; high-quality mega-menu;
search; excellent mobile drawer. PLATFORM NAV: non «public nav + sidebar» — una vera app navigation.

## 14. Platform app shell — rifare

Esplorare: compact navigation rail + contextual workspace navigation + page command area. Possibile
desktop: LEFT RAIL (global domains) · SECONDARY CONTEXT PANEL (workspace navigation) · TOP CONTEXT BAR
(search / notifications / user / actions) · MAIN WORKSPACE · OPTIONAL RIGHT INSPECTOR. Non tutto
insieme se eccessivo. Shell altamente professionale.

## 15. Sidebar

La sidebar attuale non è accettata (lista di link con una riga verticale). Target: icone coerenti;
gruppi semantici; active state premium; subtle depth; animated indicator; collapse behavior;
contextual counters SOLO se reali; tooltips collapsed; keyboard support; mobile strategy. Non
colorata o giocosa: sofisticata.

## 16. «Mes Documents» — pagina pilota obbligatoria

Ripensata come DOCUMENT WORKSPACE, non pagina editoriale + tabella. Gerarchia: DOCUMENT WORKSPACE
HEADER (Mes documents · brief context · global progress · primary action se disponibile) · DOCUMENT
HEALTH / COMPLETION STRIP (7 required · 1 validated · 4 pending … dati reali) · FILTER / SEARCH
CONTROL (Tous · À fournir · En examen · À remplacer · Validé · Expiré) · DOCUMENT COLLECTION
(adaptive list/grid; desktop: rich rows o panels). Ogni riga: DOCUMENT IDENTITY (type/title,
version) · STATUS (semantic premium chip) · RESPONSIBILITY (person / company / authority / provider)
· DEADLINE · DOCUMENT HEALTH · PRIMARY ACTION · SECONDARY MENU. Righe con hover, focus, dettaglio
espandibile, stato animato, azioni contestuali. No «Consulter» sottolineato: azioni vere.

## 17. Document status system

Stati con un design reale: VALIDÉ · EN EXAMEN · À FOURNIR · MANQUANT · EXPIRÉ · À REMPLACER · NON
VALIDE · DÉPOSÉ · BLOQUÉ. Colore semantico + icona + etichetta + pattern sottile opzionale. Chip
moderni con padding, radius, font, border, background, iconography corretti. No rettangoli HTML. No
colore da solo.

## 18. Responsibility visualization

«Responsable» deve essere visivamente significativo: PERSON · COMPANY · TRAINING BODY · PROFESSIONAL
· AUTHORITY · ITALY LEGAL ENTRY. Indicatori d'attore sofisticati: glifo astratto tipo avatar + tipo
attore + nome quando disponibile. NON creare avatar di persone finte.

## 19. Deadlines

Urgenza comunicata con eleganza: NORMAL · UPCOMING · SOON · OVERDUE. Non dipingere tutto di rosso:
urgenza progressiva sottile.

## 20. Actions

«Consulter», «Bloqué», «Accepter les Conditions…» sembrano improvvisati. Modello: azione primaria =
bottone; secondaria = menu o ghost; bloccata = controllo disabilitato + spiegazione (tooltip/callout).
No hyperlink clutter.

## 21. Table system

Dove le tabelle restano semanticamente corrette: premium DataTable (sticky header; row hover; focused
row; status chip; sorting; filter; search; responsive detail; column management per viste staff; row
action menu; bulk selection solo dove permesso). La collezione documenti dell'utente non deve essere
per forza una tabella classica.

## 22. Lists

Gerarchia; spaziatura; stato; hover; focus; metadati significativi; icone solo dove utili. No UL nudi
nelle superfici principali.

## 23. Chips / badges

Sistema completo: STATUS · FILTER · CATEGORY · ROLE · INFO · WARNING · SUCCESS · ERROR. Semantiche
diverse non devono avere trattamento identico. Moto sottile su selezione/filter chips.

## 24. Sliders / segmented controls

Non aggiungere slider perché nominati. Controlli moderni dove semanticamente corretti: segmented
filter (Tous / À faire / En cours / Terminé); toggle solo per impostazione binaria; slider solo per
valore continuo reale. Modernità ≠ controlli casuali.

## 25. Modals

Composizione generosa; header; close; icona contestuale; gerarchia; footer actions; background blur;
scale/fade sottile; focus trap; ESC; variante mobile full-screen dove appropriato. No dialog da
browser.

## 26. Drawers

Per ispezione contestuale: document preview; filters; activity; quick-edit. Moto fluido e premium.

## 27. Popups / tooltips / popovers

Tooltip · popover · dropdown · menu · context menu con superficie, ombra, bordo, raggio e moto
coerenti.

## 28. Forms

Campi premium: altezza adeguata; etichette chiare; hint opzionale; superficie moderna; focus ring;
validazione; icone solo se utili; sezioni raggruppate; conditional reveal; success feedback. Floating
labels solo se l'usabilità non ne soffre. Nessun modulo che sembri Django HTML grezzo.

## 29. File upload

Qualità flagship: dropzone grande e moderna; browse; drag feedback; progress; preview; stato di
scansione/processing se supportato; errore; sostituzione; cronologia versioni. Il moto rinforza lo
stato.

## 30. Search

Pubblico: overlay/pannello premium se giustificato. Piattaforma: ricerca globale permission-aware;
possibile command palette per power user dello staff. Nessun oggetto non autorizzato esposto.

## 31. Hero doorway — V4

Conservare `doorway__arch` come fondamento e migliorarlo sostanzialmente. Il grafico deve spiegare
visibilmente QUATTRO VIE D'ACCESSO: PERSONNE · ENTREPRISE · INSTITUTION · UNIVERSITÉ / FORMATION, non
linee decorative casuali: quattro percorsi chiaramente differenziati. Concetto possibile: quattro
nodi d'origine → attraverso l'arco → nell'ecosistema condiviso → verso percorsi/servizi. Interazione:
hover/focus su un pubblico → la sua via diventa prominente → appare etichetta/contesto → la CTA
relativa si evidenzia; su touch, tap equivalente. Animazione: disegno iniziale + moto ambientale
sottile + enfasi interattiva. Mai infantile.

## 32. Doorway labeling

Etichette leggibili ma integrate; evitare quattro badge fluttuanti attaccati a caso all'SVG:
callout ancorati; etichette SVG inline; legende ai bordi; disclosure guidata dall'interazione.
Layout mobile eccellente.

## 33. Public home — più storytelling visivo

Livelli d'intensità: hero alto; vie per pubblico alto; processo alto; spiegazione lunga più calma;
forum alto; news medio; footer rifinito. Evitare sezioni a densità uniforme.

## 34. Imagery è ora richiesta

Introdurre contenuto visivo curato. Temi: cooperazione universitaria/accademica; formazione
professionale; dialogo istituzionale; luogo di lavoro moderno; consulenza professionale; formazione
prima della partenza; integrazione/apprendimento; relazioni Italia/Marocco dove autentiche. Qualità
editoriale. Nessuna immagine stock cliché.

## 35. Image art direction

L'Image Art Director definisce: sistema di crop; proporzioni; grading; contrasto; overlay; trattamento
dei bordi; moto; maschere; linguaggio bordo/raggio. Le immagini appartengono allo stesso design
system. Nessun mix casuale da Pexels.

## 36. Image interaction

Dove appropriato: leggero scale su hover; mask reveal; crossfade; scroll reveal; parallax 1–3 %;
overlay leggero. Nessuno zoom aggressivo.

## 37. Background system

Tassonomia reale: NEUTRAL · SOFT · DARK · BRAND · IMMERSIVE · DATA · FOCUS. Tecniche: mesh gradients;
luce radiale; grana sottile; campo di tracciati SVG; linea topografica; griglia; forma architettonica.
Nessun blob casuale.

## 38. Glass / blur

Ammesso solo in: sticky nav; overlay; pannello hero selezionato; controlli flottanti selezionati. Non
glassificare ogni card. Verifica del contrasto.

## 39. Depth system

Livelli: 0 flat/base · 1 interactive · 2 elevated · 3 floating · 4 modal. Ognuno con bordo, ombra,
superficie, blur definiti. Nessun box-shadow casuale.

## 40. Border radius

Scala moderna: xs · sm · md · lg · xl · full, usata con intenzione. Bottone md/lg; chip full; panel
lg/xl; riga di tabella non necessariamente arrotondata da sola. Evitare gli estremi: tutto squadrato
e tutto pill.

## 41. Hover language

Ogni elemento interattivo definisce uno stato hover: surface lift; luce; border shift; movimento
dell'icona; transform sottile; underline animato; spotlight. Nessun effetto arbitrario. Il touch ha
uno stato alternativo.

## 42. Focus language

Il focus da tastiera deve apparire premium quanto l'hover. Nessun focus di default rimosso senza
sostituzione. Token di focus di marca.

## 43. Press / active

Feedback tattile: piccola scala/traslazione o risposta di superficie. Rispetto del reduced motion.

## 44. Scroll experience

Il sito pubblico guadagna una progressione di scroll premium: chapter progress; section reveal;
sticky visual; path construction; background transitions; nav state change. Nessun scroll hijacking.
La piattaforma usa poco spettacolo di scroll: efficienza del compito prima di tutto.

## 45. Page transitions

Transizioni sottili senza ritardare la navigazione: content fade/slide; shared header transition.
Nessuna animazione a schermo intero da un secondo a ogni clic.

## 46. Auth screens

Login rivalutato da zero: autenticazione istituzionale premium. Possibile composizione divisa:
brand/motion visual + form. Fiducia, chiarezza, sicurezza, modernità. No card generica centrata.

## 47. Person dashboard

Immediatamente informativo. Header: Bonjour / contesto attuale · stato del percorso · prossima azione
primaria. Poi: visualizzazione del percorso; prossimi compiti; documenti; scadenze; formazione;
messaggi/helpdesk. Evitare 8 card uguali: composizione.

## 48. Fascicolo digitale

Workspace di punta. Progettato intorno a: DOVE SONO? · COSA VIENE DOPO? · CHI È RESPONSABILE? · COSA
MANCA? Serve: binario dinamico del percorso; responsabilità; documenti; compiti; cronologia. Split
workspace premium dove utile.

## 49. Orientation wizard

Onboarding guidato premium: una domanda chiara; contesto; opzioni selezionabili rifinite; progresso;
indietro; salva; transizioni fluide; riepilogo vivo dove utile. Non SurveyMonkey.

## 50. Option cards

Per le scelte del wizard, tile interattive: stato di selezione; icona/visual; titolo; spiegazione;
tastiera. Superfici arrotondate moderne e moto premium.

## 51. Result page

Distinguere visivamente: percorso potenziale · elementi mancanti · avvertenze · verifica richiesta ·
fonti. Non ridurre a paragrafo + elenco.

## 52. Company UX

Dashboard B2B enterprise-grade: bisogni; competenze; timeline; formazione; attore responsabile; stato
del progetto. Nessuna estetica da marketplace di candidati.

## 53. Academy

Esperienza corso visivamente ricca: copertina/art direction; progresso; continua; moduli; risorse.
Non una tabella di corsi.

## 54. Forum

Forum pubblico più immersivo. Autenticato: workspace di cooperazione professionale. Sensazione di
rete/progetto senza istituzionalismo finto.

## 55. Notifications

Centro notifiche vero: non letto/letto; categoria; priorità; orario. Animazione sottile.

## 56. Toasts

Sistema di toast rifinito: success · info · warning · error. Non conservare messaggi effimeri.
Regione live accessibile.

## 57. Empty states

Nessuna tabella vuota + testo. Stati contestuali premium: visual; spiegazione; azione. Nessuna
illustrazione infantile.

## 58. Skeletons

Skeleton di caricamento per superfici ricche; non solo spinner. Nessuno skeleton dove il rendering
server è istantaneo salvo caricamento reale.

## 59. Error states

Errori progettati: errore inline; errore di pagina; errore di permesso; errore di rete. Con
recupero.

## 60. Mobile

Il redesign mobile è lavoro separato. La sidebar diventa navigazione appropriata. Le tabelle si
trasformano con grazia. Le azioni restano raggiungibili. Nessuna tabella desktop schiacciata a 390 px.

## 61. Mobile documents

Mes Documents su mobile: document card / righe impilate. Ogni card: titolo; stato; attore
responsabile; scadenza; azione principale. Nessuna dipendenza da tabella orizzontale.

## 62. RTL

Tutti i nuovi sistemi visivi testati in RTL: navigazione; rail; sidebar; direzione delle icone;
drawer; timeline; vie della porta; tabelle; document card.

## 63. Design tokens V4

Ricostruire/estendere: COLORS · SURFACES · GRADIENTS · TYPOGRAPHY · SPACING · RADIUS · SHADOW · BLUR
· BORDER · MOTION · FOCUS · ICON SIZE · CONTROL HEIGHT · Z-INDEX. Nessun valore arbitrario nei
componenti.

## 64. Component inventory

Una libreria definitiva: Button · IconButton · Chip · Badge · Status · Avatar/Glyph · Input · Select
· Textarea · Checkbox · Radio · Switch · Tabs · SegmentedControl · Tooltip · Popover · Dropdown ·
Modal · Drawer · Toast · Breadcrumb · Pagination · Table · DocumentRow · DocumentCard · Upload ·
Timeline · JourneyRail · ResponsibilityBar · EmptyState · Skeleton · PageHeader · ContextHeader ·
Search · CommandMenu. Ogni implementazione usa il componente centrale dove applicabile.

## 65. Remove duplicate local CSS

Audit dei template per stili una tantum; consolidare nel design system. Nessun template reinventa
bottone, badge, stato, input, riga.

## 66. Iconography

Fondamento iconografico coerente, adattato. Nessun mix casuale. Diagrammi di prodotto firmati in SVG
custom. Nessuna emoji.

## 67. Premium animation budget

Classificare i componenti: STATIC · MICRO · INTERACTIVE · IMMERSIVE. Solo le sezioni pubbliche
immersive hanno moto alto. Dashboard prevalentemente MICRO/INTERACTIVE.

## 68. Performance

Misurare prima/dopo: JS · CSS · LCP · CLS · INP se disponibile. Nessuna libreria eccessiva.

## 69. Accessibility

WCAG 2.2 AA non negoziabile. Nuovi componenti premium con tastiera, focus, reduced motion,
contrasto, semantica per screen reader. Nessun sacrificio dell'accessibilità per l'estetica.

## 70. Chrome headed — required

Google Chrome visibile come ambiente primario di revisione visiva. Non solo screenshot headless.
Ciclo: IMPLEMENT · REFRESH · OBSERVE · FIX · REFRESH. Sviluppo visivo osservabile.

## 71. Visual approval gates

GATE A: Homepage + Navbar. GATE B: Login + Platform Shell. GATE C: Person Dashboard + Documents.
GATE D: Fascicolo + Wizard. GATE E: Company + Academy + Forum. Ogni gate rivisto da: Creative
Director · UX Lead · Motion Lead · Frontend Lead · Accessibility reviewer.

## 72. No self-approval

L'agente che implementa una pagina non può esserne il revisore finale. Revisore indipendente
obbligatorio.

## 73. Screenshot comparison

Per ogni gate: BEFORE e AFTER. L'AFTER deve essere visibilmente e materialmente superiore. Non
sottile.

## 74. Premium scorecard

Per ogni gate: Premium Feel · Modernity · Visual Depth · Motion · Clarity · Institutional Credibility
· Originality · Interaction Quality · Mobile · Accessibility. Nessuna media: una dimensione critica
debole blocca la propagazione.

## 75. Test «generic AI UI»

Ai revisori indipendenti: «Potrebbe essere scambiato per un template generico Claude/AI?» Se sì:
FAIL, con il perché esatto.

## 76. Test «editorial»

«Sembra ancora principalmente una pubblicazione editoriale/legale?» Per le pagine operative la
risposta deve essere NO.

## 77. Test «2026»

«Nascosto il logo, questa interfaccia competerebbe plausibilmente con prodotti digitali
professionali premium progettati nel 2026?» Se no: FAIL.

## 78. Test «too much»

«Abbiamo aggiunto effetti inutili solo per sembrare moderni?» Se sì: rimuoverli. Premium è
ricchezza controllata.

## 79. Copy and functional content

Non riscrivere contenuti bloccati. Non reintrodurre formulazioni vietate. Il redesign visivo non può
alterare il significato legale.

## 80. Brand assets

Continuare a usare il logo Italy Legal Entry esistente e la grafica porta/arco secondo l'ultima
direttiva sugli asset. Non ripristinare slogan vietati.

## 81. Images

L'Image Art Director sceglie un insieme coerente. Nessun agente sceglie foto stock casuali per conto
suo. Una sola libreria visiva.

## 82. Image source

Provider legali (Pexels/Unsplash) dove adatti. Verificare licenza/fonte. Self-host degli asset finali
approvati. Nessun hotlink.

## 83. Image quality gate

Rifiutare se: ovviamente stock; stretta di mano generica; posata; bassa risoluzione; irrilevante;
cliché sull'immigrazione; grading incoerente.

## 84. Design work should be visible early

Non ridisegnare 100 template prima di mostrare una direzione corretta. Prima perfezionare: HOME ·
LOGIN · PERSON DASHBOARD · MES DOCUMENTS. Queste quattro superfici stabiliscono il linguaggio V4.
Poi propagare.

## 85. Mes Documents is the primary control page

Usare la pagina come superficie di regressione/controllo visivo. Il risultato V4 deve far sembrare
ovviamente obsoleto il vecchio screenshot. Deve contenere visibilmente: shell migliore; spaziatura
migliore; navigazione migliore; stati migliori; azioni migliori; gerarchia documentale migliore;
controlli premium; superfici moderne; hover/focus; comportamento responsive professionale.

## 86. No «folio» as default answer

Se restano trattamenti folio/registro/editoriali, limitarli dove aggiungono valore reale. Non devono
dominare la piattaforma operativa.

## 87. Serif usage

Rivalutare la dominanza del serif. Elegante in: titoli editoriali pubblici; momenti display scelti.
Le schermate applicative operative hanno bisogno di una tipografia UI digitale più forte. Non
rendere una dashboard come una rivista.

## 88. Platform typography

Scala tipografica UI moderna; gerarchia più stretta; densità leggibile; trattamento numerico/tabulare
per date/stati/dati.

## 89. User efficiency

Premium significa anche meno passi cognitivi. Identificare: clic inutili; azioni poco chiare;
navigazione ripetuta; testo ridondante; stato nascosto. Migliorarli senza cambiare il flusso legale.

## 90. Do not build «features» just for wow

Niente finti: grafici; KPI; assistente AI; mappe; coordinate; dati animati. Solo dati reali di
prodotto.

## 91. Debug / development artifacts

Niente di visibile all'utente: svg; label di debug; nomi di componenti; etichette tecniche di
coordinate; identificatori di test — salvo significato esplicito. Aggiungere scansioni automatiche
dove pratico.

## 92. Copy review

UI copy chiara, umana, professionale, istituzionale. Nessun gergo da sviluppatori.

## 93. Quality of details

Rivedere: allineamento a 1 px; baseline delle icone; altezza dei bottoni; allineamento degli input;
allineamento verticale dei chip; line-height; peso ottico dei bordi; spazio bianco; tempi di hover.
Il premium dipende dai dettagli.

## 94. Design system demo page

Creare/aggiornare la vetrina dei componenti solo per sviluppo. Non procedere se i componenti core
appaiono incoerenti l'uno accanto all'altro.

## 95. Tooling blockers

Se 21st.dev o UI-UX-Pro-Max non sono davvero operativi, dirlo subito: INSTALLED? · AUTHENTICATED? ·
AVAILABLE? · LIMITS? · CREDITS? · PAID PLAN NEEDED? Non fingere che siano stati usati se l'accesso non
è disponibile.

## 96. Tool usage evidence

Il rapporto finale elenca: UI-UX-Pro-Max — analisi esatte usate; 21st — ricerche/pattern/componenti
esatti esaminati; Motion — schermate/componenti esatti che lo usano. Nessuna affermazione vaga.

## 97. Implementation order

1. checkpoint · 2. stop alla propagazione · 3. audit della pagina indicata · 4. analisi
UI-UX-Pro-Max · 5. ricerca 21st · 6. sintesi del Creative Director · 7. Design System V4 · 8.
Homepage/nav V4 · 9. Login/app shell V4 · 10. Mes Documents V4 · 11. Person Dashboard V4 · 12.
revisione Chrome · 13. revisione indipendente · 14. correzioni · 15. solo dopo il PASS, propagare ·
16. Fascicolo · 17. Wizard · 18. Company · 19. Academy · 20. Forum · 21. pagine restanti · 22. mobile ·
23. RTL · 24. accessibilità · 25. prestazioni · 26. red team · 27. QA finale.

## 98. End condition

Non dichiarare la fase completa perché i test passano: i test passano già. La fase è completa solo
quando la QUALITÀ VISIVA DEL PRODOTTO è materialmente cambiata.

## 99. Final status

DESIGN_V4_ACCEPTED · CONDITIONALLY_READY · NOT_READY. DESIGN_V4_ACCEPTED richiede: sito pubblico
davvero premium; piattaforma davvero premium; pagine operative non più editoriali; sistema di
componenti sofisticato; linguaggio d'interazione moderno visibile; Motion coerente; navbar premium;
bottoni premium; stati premium; overlay premium; UX documenti premium; immagini forti; revisione
Chrome superata; accessibilità/prestazioni accettabili.

## 100. Start now

Finire solo il compito atomico corrente. Poi STOP alla propagazione del vecchio sistema visivo.
Iniziare V4. Non inviare un altro piano teorico e aspettare. Usare agenti esperti. Usare gli
strumenti resi disponibili. Costruire, renderizzare in Chrome, criticare, correggere e iterare. Il
target non è più «interfaccia istituzionale pulita»: è «un ecosistema digitale istituzionale/legal-tech
2026 di classe mondiale, premium, dinamico e altamente rifinito».


---

# CHIARIMENTO PRIORITARIO SULLA DIRETTIVA V4 — 24 settembre 2026, ore 20:58

Il freeze e la direttiva V4 **non** vanno letti come un divieto verso design moderno, gradienti,
blur, UI arrotondata, Motion, immagini, superfici ricche o altri pattern premium. La V4 esiste
precisamente perché il risultato precedente era troppo editoriale, sobrio, semplice e conservatore.

**Vincoli che restano assoluti:** testi legali; prohibited wording; responsabilità degli attori;
workflow; IAM/permissions; privacy/GDPR; sicurezza; accessibilità; performance; Django come core;
brand asset ufficiali; nessuna falsa identità ministeriale; nessuna funzione inventata.

**Scelte visuali precedenti che non sono più vincolanti** (possono essere completamente sostituite):
precedente art direction editoriale; serif dominante; folio/register come linguaggio principale;
palette precedente; precedente button system; precedente sidebar; precedente navbar; precedente
surface system; precedente livello di motion; precedente scelta di evitare glass/gradienti/rounded
components; precedente impostazione minimalista.

**La V4 autorizza espressamente, se usati professionalmente:** gradienti sofisticati; layered
backgrounds; mesh/radial lighting; blur; controlled glassmorphism; modern rounded surfaces; richer
shadows; premium hover states; advanced Motion; animated SVG; scroll-linked effects; modern imagery;
premium panels; sophisticated buttons; modern chips/badges; drawers; overlays; command/search UI;
modern app shell; more visual depth.

Non scegliere automaticamente la soluzione più austera perché «istituzionale». Istituzionale non
significa editoriale. Nuova priorità estetica: **INSTITUTIONAL CREDIBILITY + PREMIUM 2026 DIGITAL
PRODUCT + VISUAL IMPACT + MOTION + USABILITY.**

**UI-UX-Pro-Max** è una fonte di competenza, non un generatore di design system da accettare o
rifiutare in blocco. Davanti a «navy + Garamond + Google Fonts» si analizza separatamente: navy →
mantenibile o evolvibile se contribuisce al sistema premium; Garamond → probabilmente non adatto come
font UI dominante (accentua l'estetica editoriale rifiutata), eventuale uso display molto limitato a
giudizio del Creative Director; Google Fonts → non necessariamente il servizio remoto: se un font
open-source è valido, self-hosting per privacy, prestazioni e controllo. Comportamento richiesto:
**SKILL RECOMMENDATION → EXPERT ANALYSIS → PROJECT ADAPTATION → LIVE PROTOTYPE → CHROME REVIEW**, non
«→ generic design system» né «→ respinto per le regole visive precedenti».

Le direttive visuali dei prompt precedenti non giustificano più: interfacce piatte; rettangoli;
link sottolineati come CTA; sidebar testuali; tabelle editoriali; grandi H1 serif; assenza di
immagini; assenza di motion; assenza di profondità; design volutamente austero. Sono precisamente i
problemi che V4 deve correggere.

**UI-UX-Pro-Max**: usarlo molto più intensamente, con problem statement specifici per superficie
(es.: «Design a premium 2026 legal-tech document workspace for an international institutional
platform. It must feel sophisticated, dynamic and contemporary, not editorial or bureaucratic.
Include modern app-shell patterns, polished status chips, contextual actions, rich document
rows/cards, hover/focus/motion states, responsive mobile transformation and WCAG 2.2 AA
considerations. Avoid generic SaaS and default shadcn appearance.»), per navbar, hero, buttons,
login, dashboard, document workspace, case workspace, wizard, company area, Academy, Forum.

**21st.dev**: cercare componenti e pattern specifici (premium floating/sticky navbar; animated mega
menu; modern application shell; rich document management; premium data table; modern status chips;
premium modal/drawer; animated tabs; contextual sidebar; premium file upload; interactive timeline;
advanced command menu; sophisticated auth; animated hero; SVG path visualization; spotlight panel;
premium CTA), confrontando più candidati per categoria.

**Nessun design generico**: il Design Council combina ILE brand + documenti di progetto + UI-UX-Pro-Max
+ 21st.dev + Motion + senior design judgment. Il freeze è corretto ma non deve trasformarsi in una
fase conservatrice: il suo scopo è evitare di propagare il design editoriale rifiutato. Procedere
con un vero salto visuale.
