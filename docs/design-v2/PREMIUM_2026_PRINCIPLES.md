# PRINCIPI PREMIUM 2026 — regole operative per ITALY LEGAL ENTRY™

Diciotto principi. Ognuno cita la prova (BENCHMARKS.md / fonti primarie) e chiude con un test:
"Lo sai che è soddisfatto quando…". Valgono per il sito pubblico e per la piattaforma.

## 1. Sette livelli di profondità, un token per livello
Canvas → editoriale → interattivo → elevato → focus → overlay → immersivo. La profondità nasce dalla
scala di superfici e dalle hairline (Linear "four-step ladder replaces shadows"), le ombre esistono
solo per ruolo (Vercel card/hover/popover/modal; Fluent 2 rampa 2/4/8/16/28/64, key + ambient,
opacità raddoppiata nel buio), il vetro solo dal livello elevato in su e mai sul contenuto (Apple
Liquid Glass su barre e controlli; Raycast solo sulla palette).
**Test**: ogni superficie del DS ha `--level-n`; `grep box-shadow` restituisce solo i quattro
ruoli; `backdrop-filter` compare solo in elevato/immersivo.

## 2. Un accento per l'unica azione
Mercury #5266eb "per la sola azione che conta", Linear lavanda "mai decorativa", NBIM un blu
elettrico su avorio, Vercel #0070f3.
**Test**: in qualsiasi viewport un solo elemento porta il blu luminoso; link, CTA e focus lo
condividono; nessun titolo, icona o sfondo lo usa.

## 3. Moto d'autore: ogni animazione dichiara la sua funzione
Sette funzioni ammesse — orientamento, gerarchia, causalità, stato, feedback, profondità, delizia.
Stripe: una sola animazione ambientale; motion.dev: Editorial Stagger e Parallax Layers; Rauno:
la frequenza riduce il valore; Emil: mai animare azioni ripetute da tastiera.
**Test**: MOTION_SYSTEM.md elenca ogni animazione con funzione, innesco, durata, curva e
alternativa ridotta; nessuna voce ha funzione "estetica"; nessun `fade-in-up` generico.

## 4. Il moto ridotto è uno stato di prima classe
MDN: miglioramento progressivo (si anima solo con `no-preference`); WCAG 2.3.3 (AAA, obiettivo):
il moto da interazione si può disattivare; Stripe, Mercury, Wise, Vercel dichiarano
`prefers-reduced-motion`; ETH, MIT, BoE no.
**Test**: con "riduci movimento" attivo la pagina è completa e identica nei contenuti, i reveal
sono istantanei, i loop fermi, i video hero mostrano il poster, nulla resta invisibile.

## 5. Niente scroll-jacking; scroll-linked solo con ScrollTimeline e solo dove serve
motion.dev `scroll()` usa ScrollTimeline con accelerazione hardware; scroll-triggered = `inView`;
Lenis/smooth-scroll compaiono solo su siti vetrina (darkroom, Legora); select-interactive: lo
storytelling a scroll che blocca il main thread viene tagliato.
**Test**: rotellina, tastiera e lettore di schermo scorrono 1:1 su tutte le pagine; il rail di
processo è scroll-linked via `scroll()`/`animation-timeline`; nessuno smooth-scroll globale.

## 6. Autorità tipografica: tre voci, pesi intermedi, compagni arabi dichiarati
Nobel/Instrument/Harvey: sans + serif + mono di una famiglia; Mercury 480/420, Linear 590/510;
ECL interlinee multiple di 4; Designers Italia 75 caratteri; Clerk numeri tabellari; ONCF e
Maroc.ma dichiarano il compagno arabo (Helvetica Neue Arabic, Cairo).
**Test**: al massimo tre famiglie latine + i loro compagni arabi in `@font-face`, self-hosted
(CSP `'self'`); nessun peso 700 nei titoli; `letter-spacing` negativo solo ≥ 40 px e 0 in AR;
nessuna riga oltre 75 caratteri; i numeri usano cifre tabellari.

## 7. Dark e light sono capitoli, non modalità
Harvey chiaro con inserti scuri, Legora scuro, Snøhetta token doppi `canvas/area/stroke`, DSFR
schema via attributo, Fluent 2 ombre più intense nel buio.
**Test**: ogni pagina pubblica ha al massimo un capitolo inchiostro, che inizia e finisce a un
confine di sezione con transizione di sfondo; il portale cambia schema con un attributo di
documento senza ricaricare né perdere contrasto.

## 8. Quattro componenti firma, o non è nostro
(a) hero con titolo a reveal riga per riga e un oggetto vivo; (b) **quattro vie di accesso** come
pannelli con scala colore per via (ETH: scale per dipartimento); (c) **processo**
NEED → SKILLS → TRAINING → REGULAR PATHWAY → ENTRY → INCLUSION come rail scroll-linked con
responsabile per tappa (Migrationsverket: sei fasi; Jeton: oggetto indicizzato allo scroll);
(d) **rail giurisdizione/responsabilità** (chi decide, IT/MA/UE) sempre visibile su RICH e LEGAL.
**Test**: i quattro esistono come componenti nominati nel DS con stato statico equivalente,
compaiono in HOME, e uno screenshot senza logo resta riconoscibile come nostro.

## 9. Parità di piattaforma: il portale è premium quanto il sito
Mercury fa leggere un conto "come un rendiconto ben composto"; Linear dà i pixel alla superficie
di lavoro; Attio mette il riepilogo come superficie di prima classe; NBIM apre con il numero vivo.
**Test**: home e fascicolo affiancati condividono font, accento, raggi, ombre, curve; il fascicolo
apre con "Stato della pratica" (fase, prossimo atto, responsabile, scadenza) come hero; nessun
form Django con stile di default.

## 10. Composizione mobile propria, non desktop compresso
IND e Migrationsverket funzionano a una colonna perché nascono come liste di situazioni; Eurostar
ritaglia con focal point; WCAG 2.5.8: target ≥ 24 × 24 px.
**Test**: a 360 px nessuno scroll orizzontale, gutter 16 px, header ≤ 56 px, le quattro vie in
lista verticale con la loro scala colore, il rail di processo verticale, ogni target ≥ 24 px, il
poster sostituisce il video hero.

## 11. Moto e layout consapevoli dell'arabo (RTL)
rtlstyling.com: `translateX` inverte segno; chevron, freccia indietro, avanzamento e caroselli si
specchiano; controlli media, orologi, numeri, loghi e lente di ricerca no; `text-align: end`,
proprietà logiche, `letter-spacing: 0`, niente opacità sul testo, `min-width` sui bottoni,
numerali coerenti.
**Test**: con `dir="rtl"` i reveal entrano dal lato di lettura, il rail avanza da destra, la
suite visiva in AR passa a tre larghezze, nessuna proprietà `left/right` fisica nel CSS nuovo.

## 12. Budget di prestazione prima dell'effetto
web.dev: solo `transform` e `opacity`, `will-change` temporaneo via JS; Motion: ScrollTimeline;
Attio: loop ambientali di 10–30 s; Jeton: niente autoplay pesante; select-interactive: INP come
vincolo.
**Test**: durante ogni animazione DevTools mostra 0 layout/paint; INP < 200 ms e LCP < 2,5 s su
4G simulato; nulla anima fuori dal viewport (IntersectionObserver); immagini e video sotto la
piega sono lazy; il video hero è muto, con poster, e non blocca LCP.

## 13. Sopravvivenza in accessibilità WCAG 2.2 AA
1.4.3 e 1.4.11: 4.5:1 testo, 3:1 componenti e grafica ("2.999:1 non passa"), misurato sul peggior
sfondo sotto il vetro; 2.4.11: il focus non può essere coperto da header sticky o banner; 2.5.8:
target 24 px; hover con equivalente tastiera/touch; alternative testuali per rail, processo e
grafici (OWID: il testo introduce il grafico).
**Test**: axe senza errori su ogni template; `scroll-padding-top` ≥ altezza header; ogni
componente firma ha una versione testuale/lista; il vetro passa con la foto più chiara e più scura.

## 14. Content-first per cinque modalità di pagina
IMMERSIVE (home, landing delle vie), RICH (Academy, corsi, fabbisogno), STANDARD (informativa),
DENSE (dashboard, liste), LEGAL (norme, disclosure, privacy). Legora/Stripe fanno vetrina;
Linear/Mercury fanno prodotto; GOV.UK fa legale.
**Test**: ogni template dichiara `data-mode`; LEGAL ha zero moto decorativo, 65–75 caratteri e
hairline; DENSE non ha ombre né vetro; solo IMMERSIVE può avere video, parallasse e capitolo
scuro.

## 15. Il numero vivo: dati reali come hero, con fonte e data
NBIM (valore del fondo), Bocconi (fatti chiave), Migrationsverket (regole datate), Wise (146
lingue, 200 colori testati: numeri con provenienza).
**Test**: nessun numero senza fonte e data visibili; nessun logo o testimonianza non verificata;
i contatori della piattaforma sono calcolati, non scritti.

## 16. Una curva d'ingresso, una d'uscita, quattro durate
MIT `(.215,.61,.355,1)` ×126; Locomotive ×43; Stripe `(.25,1,.5,1)`; Harvey coppia out/in-out;
nessun overshoot (BoE, Raycast, Wise).
**Test**: il CSS/JS compilato contiene al massimo tre `cubic-bezier` (entrata, uscita,
standard) e durate solo dall'insieme {120, 180, 240, 320 ms} più i loop ≥ 20 s.

## 17. Materiali, non effetti
Legora: pietra, cuoio, luce; Mercury: ritratti e geometrie; ECB: set icone proprio; niente shader,
particelle, 3D (21st.dev, Lusion); niente immaginario migratorio cliché.
**Test**: nessun canvas WebGL nel bundle; ogni pagina IMMERSIVE ha una fotografia o illustrazione
commissionata con focal point; il set icone è nostro a tratto 1,5 px; nessun aereo, passaporto,
valigia, varco, bandiera.

## 18. Nessuna copia: ogni decisione ha due riferimenti e un contro-riferimento
Ogni token, componente o idioma cita almeno due benchmark indipendenti e un caso "da non
prendere" (BENCHMARKS.md); verificato in Chrome visibile a tre larghezze e in AR prima
dell'accettazione.
**Test**: DESIGN_SYSTEM_V2.md ha una colonna "prove" per ogni token; esiste la registrazione
Chrome a 360/768/1440 px in IT e AR per la vertical slice HOME + NAV + LOGIN + DASHBOARD + FASCICOLO.
