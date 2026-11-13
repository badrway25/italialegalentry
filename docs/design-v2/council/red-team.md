# RED TEAM — revisione critica indipendente delle tre direzioni (Design Council V2)

Revisore indipendente, non parte di alcuna squadra · 23 settembre 2026 · metodo: prima ho guardato, poi ho letto.
Catture proprie (Chromium headless di Playwright, browser proprio): 6 pagine × 1440×900 a 0,3 s / 1,5 s / 4,5 s
+ pagina intera dopo scroll completo + fold 390×844 → `council/shots/redteam/` (30 immagini, tutte lette).
Confrontate con `before/home_desktop.png`, `before/person_dashboard_desktop.png`, `brand-original/legacy_arch_desktop.png`.
I tre `DIRECTION.md` sono stati letti **dopo** le immagini, solo per verificare le affermazioni contro il codice.

Fatti comuni verificati sul codice (valgono per tutte e tre): stesso stack tipografico (Newsreader / Fira Sans / Fira Mono
+ compagni arabi da `/static/css/fonts.css`), zero Inter, zero CDN, zero `style=`/`<script>` inline, zero canvas/WebGL,
solo tre `cubic-bezier` senza overshoot, `prefers-reduced-motion` presente, nessun overflow orizzontale a 390,
0 errori di console. Il lock-up tricolore e la porta (arco + foto + chiave + gradini) sopravvivono in tutte e tre.
Il test dei sessanta secondi dell'ANTI_PATTERNS è quindi superato da tutte: **non è lì che si decide**.

---

## DIREZIONE A — «Rete luminosa»

| # | Domanda | Risposta | Prova |
|---|---|---|---|
| 1 | Sembra basic? | NO | hero a strati (rete + porta + serif 66 px), testata del fascicolo in inchiostro con rail texturizzato. |
| 2 | Sembra un sito generato / shadcn? | **SÌ, in due punti** | le quattro vie sono quattro card bianche uguali con icona nel quadratino arrotondato e codice mono R1–R4 (anti-pattern § 1, riga 6), appese a un «bus» che non le cambia; la shell è topbar + ricerca `Ctrl K` + sidebar con badge numerici: la grammatica Linear/Vercel. |
| 3 | Premium? | SÌ | scala di superfici reale, hairline, serif leggera, rail 2.0 con texture e legenda. |
| 4 | Moderno 2026? | SÌ | capitolo inchiostro, path che si disegnano, ScrollTimeline, app shell comprimibile. |
| 5 | Impatto visivo significativo? | SÌ, solo nell'hero | dopo la piega la pagina cala: card, poi uno stepper a onda punteggiata, poi una legenda a barre. |
| 6 | Portale premium quanto il sito? | SÌ | è il fascicolo più «prodotto» dei tre: stessa serif, stesso inchiostro, stesso mono, rail 2.0 in testata. |
| 7 | Moto d'autore? | SÌ, con riserve | 0,3 s → 1,5 s → 4,5 s: una linea, due linee, rete completa (sequenza narrata). Ma il titolo è già fermo a 0,3 s (il reveal riga per riga è invisibile); `herepulse` anima `box-shadow` in loop infinito e `hubpulse` anima `r`: contraddice il «solo transform/opacity/stroke-dashoffset» dichiarato al § 6. |
| 8 | Istituzionale e credibile? | SÌ, al limite | il funzionario di prefettura lo accetta; la PMI veneta lo legge «software»; il candidato marocchino trova una didascalia in inglese («A doorway, not a shortcut») su una pagina francese e un nodo «UNIVERSITÉ» due volte nella rete (`net__label` ×2 nel markup). |
| 9 | Facile da usare? | SÌ su desktop, NO al primo schermo mobile | a 390 il fold è la porta con una rete senza etichette: il titolo comincia sotto la piega (y ≈ 1340/1688). |

**Cinque secondi**: «una piattaforma tech/legale sui percorsi verso l'Italia — forse una società di consulenza per l'immigrazione».
Il titolo grande («Le parcours *régulier* vers l'Italie») lavora; la rete a nodi luminosi tira verso «AI/dati».
**Senza fotografia**: SÌ, riconoscibile — arco, arco interno, chiave e gradini sono tracciati SVG, la rete converge lì.
**Contro il baseline respinto**: materialmente più ricco nell'hero, nel processo e nel fascicolo; ma le quattro vie sono la lista
del baseline convertita in card SaaS — un passo indietro rispetto alla lista onesta di prima.
**Tre cose che mi vergognerei di spedire**: (1) le quattro card con l'icona nel quadratino; (2) «UNIVERSITÉ» duplicato +
didascalia inglese nell'hero della pagina FR; (3) il loop infinito su `box-shadow` nel rail e una barra di ricerca `Ctrl K` in
un portale i cui utenti sono candidati e PMI, non power user.
**Punteggi**: WOW 7 · PREMIUM 7 · MODERNITÀ 8 · CREDIBILITÀ ISTITUZIONALE 7 · ORIGINALITÀ 6 · COERENZA 6.
Verdetto sulle nove domande: **NOT DONE** (domanda 2, e 9 su mobile).

---

## DIREZIONE B — «Profondità architettonica»

| # | Domanda | Risposta | Prova |
|---|---|---|---|
| 1 | Sembra basic? | **SÌ** | fold desktop: carta, titolo serif sottile, corsivo, paragrafo, due bottoni, una porta a destra — la stessa sintassi del baseline con una serif migliore; fold mobile: testo + due bottoni a tutta larghezza, la porta sotto la piega, cioè il fold mobile respinto. |
| 2 | Sembra generato / shadcn? | NO | nessuna grammatica da catalogo; le soglie a gradoni con architrave e ordinale serif sono disegnate. |
| 3 | Premium? | SÌ, a metà | la targa del dossier su due piani e il capitolo del processo sì; l'hero è «quiete editoriale» — esattamente la voce della bocciatura. |
| 4 | Moderno 2026? | **NO** | legge studio legale 2019–2022 (Harvey su carta); le linee di piano verticali visibili sotto il testo sembrano una griglia di debug lasciata accesa. |
| 5 | Impatto visivo? | **NO** sul fold | a 0,3 s e a 1,5 s la metà destra dell'hero è una lastra beige vuota (la foto arriva dopo): uno sconosciuto crede che la pagina sia rotta. Impatto solo nel capitolo del processo, 2 000 px più in basso. |
| 6 | Portale premium quanto il sito? | **NO** | il fascicolo è il baseline con il rail spostato in alto e le sezioni incorniciate: zero moto (frame 0,3 s = 4,5 s, hash identico a 1,5 s), «indice» = lista numerata che appare nella colonna sinistra solo sotto il rail, non una shell. |
| 7 | Moto d'autore? | SÌ nell'hero, assente nel portale | la porta si costruisce davvero (piano → contorno → foto → chiave → gradini: tre frame diversi); processo scroll-linked; ma nemmeno «Étape actuelle» si muove nel fascicolo. |
| 8 | Istituzionale e credibile? | SÌ | il più credibile dei tre per il funzionario; la PMI lo legge «avvocati»; il candidato lo legge «serio». |
| 9 | Facile da usare? | SÌ | gerarchia limpida; però sei paragrafi su ~3 600 px di capitolo scuro (≈ 54 vh ciascuno) sono scroll per lo scroll. |

**Cinque secondi**: «uno studio legale internazionale, o una rivista giuridica, che si occupa di Italia».
**Senza fotografia**: SÌ a stato assestato (contorno tracciato, arco navy, chiave, gradini); NO per il primo secondo e mezzo.
**Contro il baseline respinto**: **la stessa cosa rivestita meglio** + un capitolo nuovo (il processo in sezione) + una targa.
Palette, ritmo, struttura del fold mobile e del fascicolo sono quelli del 23 settembre. Il footer è a quattro colonne con 18 link:
il «piè di pagina generico multi-colonna» che il brief esclude per nome.
**Tre cose che mi vergognerei di spedire**: (1) 1,5 s di lastra vuota nell'hero + le linee di piano che sembrano un overlay di
debug; (2) un fascicolo senza un solo movimento e con la navigazione a metà pagina; (3) il footer a quattro colonne.
**Punteggi**: WOW 4 · PREMIUM 6 · MODERNITÀ 5 · CREDIBILITÀ ISTITUZIONALE 8 · ORIGINALITÀ 5 · COERENZA 8.
Verdetto sulle nove domande: **NOT DONE** (domande 1, 4, 5, 6).

---

## DIREZIONE C — «Diplomazia contemporanea»

| # | Domanda | Risposta | Prova |
|---|---|---|---|
| 1 | Sembra basic? | NO | hero a tutta altezza con graticola, isoipse, rotta a sei stazioni che entra dietro la porta, coordinate delle due rive, controllo «Suspendre le mouvement». |
| 2 | Sembra generato / shadcn? | NO, con un avviso | le quattro vie sono fogli 7/5 · 5/7 con indice serif, glifo isoipsa proprio e linea d'ormeggio: non card di serie; il fascicolo ha case band, rail texturizzato e inspector. **Avviso**: buio + linee ciano su griglia è un idioma di catalogo (la squadra cita «Luminous Topography» come componente studiato); a domarlo sono l'arco, il serif e le coordinate — se in produzione si indeboliscono, l'hero torna un demo. |
| 3 | Premium? | SÌ | scala mezzanotte/minerale coerente, hairline, sigilli bronzo, mono per riferimenti; l'unico che traduce la didascalia («Une porte, pas un raccourci»). |
| 4 | Moderno 2026? | SÌ | rotta scroll-linked, sezioni «posate», marea sospendibile (WCAG 2.2.2 preso sul serio), selettore FR/IT/EN/ع già nella barra. |
| 5 | Impatto visivo? | SÌ | il fold più forte dei tre; a 1,5 s la rotta è già completa (0,3 s → 1,5 s: da vuoto a disegnato; 4,5 s identico). |
| 6 | Portale premium quanto il sito? | SÌ | la case band riporta il territorio nel fascicolo con la stessa materia; workspace minerale con inspector; il marcatore «étape actuelle» entra a scala (frame 0,3 s ≠ 1,5 s). Sotto la piega resta però sidebar + colonne come gli altri. |
| 7 | Moto d'autore? | SÌ | rotta → stazioni → porta → gradini è una frase; la marea è l'unico loop ed è sospendibile; il titolo però è già fermo a 0,3 s (reveal invisibile, come in A). |
| 8 | Istituzionale e credibile? | SÌ, con una riserva | il funzionario e il candidato sì; la PMI veneta potrebbe leggere il bottone acqua chiaro su mezzanotte come «exchange crypto»: è il CTA meno istituzionale dei tre. Le coordinate (33.97° N · 6.85° W) sono un vezzo da designer, innocuo. |
| 9 | Facile da usare? | SÌ | a 390 la porta viene prima ma il titolo «ITALY LEGAL ENTRY™» resta dentro la piega; CTA a 725/900 su desktop, ancora sopra la piega. |

**Cinque secondi**: «un programma di cooperazione fra Marocco e Veneto sull'ingresso regolare in Italia — un'istituzione, non una
startup» (l'eyebrow «COOPÉRATION VÉNÉTIE – MAROC» e le due coordinate fanno il lavoro). Rischio minore: «una società cartografica».
**Senza fotografia**: SÌ, la migliore delle tre — contorno teal dell'arco, arco navy, chiave oro, tre gradini, e la rotta che li attraversa.
**Contro il baseline respinto**: materialmente più ricco su tutto: hero, quattro vie, processo, case band, inspector, footer.
**Tre cose che mi vergognerei di spedire**: (1) il processo come **linea che sale a destra**: «la via per l'Italia cresce del 40 %
trimestre su trimestre» — è il grafico di crescita SaaS travestito da rotta; (2) due capitoli scuri per pagina (la squadra lo
ammette al rischio 4) + il `home.html` più pesante dei tre (91 KB, ~43 KB di isoipse inline) sopra una foto da 949 KB: LCP a
rischio finché non esistono i derivati; (3) il CTA acqua su mezzanotte.
**Punteggi**: WOW 8 · PREMIUM 8 · MODERNITÀ 8 · CREDIBILITÀ ISTITUZIONALE 7 · ORIGINALITÀ 7 · COERENZA 8.
Verdetto sulle nove domande: **DONE con riserve** (nessun NO secco; l'avviso su 2 e la riserva su 8 vanno chiusi in produzione).

---

## CLASSIFICA

1. **C — Diplomazia contemporanea** (46/60). Unica che supera le nove domande; unica con un'idea (due rive, una rotta, una porta)
   che il baseline non aveva e che regge anche senza fotografia e senza logo.
2. **A — Rete luminosa** (41/60). Hero e fascicolo forti, ma la squadra torna al default SaaS appena finisce il concetto
   (card, sidebar, `Ctrl K`), e la cura di dettaglio (nodo duplicato, didascalia inglese, loop su `box-shadow`) è la più bassa.
3. **B — Profondità architettonica** (36/60). La più credibile e la più coerente, e per questo la più pericolosa: è la
   direzione respinta con una serif migliore.

Le tre frasi più dure che sottoscrivo: «B è il baseline del 23 settembre con Newsreader 260: il fold mobile è, struttura per
struttura, quello respinto.» · «Le quattro vie di A sono esattamente le quattro card bianche con l'icona nel quadratino che
l'anti-pattern § 1 descrive; appenderle a un filo non le trasforma in un bus.» · «Senza l'arco, l'hero di C è un demo di 21st.dev
con un titolo serif sopra — e la squadra lo sa, perché lo cita come componente studiato.»

## RISCHIO DI CIASCUNA SCELTA

**Scegliere C.** Il rischio è la deriva verso il fintech: se in produzione l'arco perde la foto, il serif si stringe, il teal
finisce su ogni card e le isoipse decorano anche le pagine LEGAL, resta un hero da catalogo su sfondo scuro. Il secondo rischio
è di prestazione (pagina più pesante, due capitoli scuri, foto master). Condizioni per accettarla: un solo capitolo inchiostro
per pagina (il processo su `--min-1` come la squadra stessa propone), rotta del processo non monotona verso l'alto, CTA
riportato a un teal saturo con testo chiaro, budget LCP dimostrato con i derivati AVIF/WebP, isoipse vietate fuori da IMMERSIVE.

**Scegliere A.** Il rischio è «Linear con il logo»: la rete è una metafora che compete con la porta invece di servirla, e ogni
volta che il concetto non copre un componente la squadra ha già mostrato dove va a prendere il default (card, shell, badge,
ricerca). Il fascicolo è il migliore dei tre e potrebbe essere innestato altrove; la home no senza rifare le quattro vie e il
processo. QA di dettaglio da rifare (etichette, lingua, loop).

**Scegliere B.** Il rischio è quello che nessuno nomina: **la più sicura vince per default**. Un consiglio che deve sostenere
«istituzionale» davanti a un funzionario sceglierà B perché non può essere attaccata — e consegnerà, in abiti migliori, ciò che
il committente ha respinto ventiquattro ore prima con le parole «editoriale, austero, statico, piatto». Ogni aggettivo della
bocciatura è ancora vero sull'hero e sul fascicolo di B. Se il consiglio sceglie B, deve aspettarsi la seconda bocciatura e
dire fin d'ora che l'ha scelta per prudenza, non per il brief. Ciò che di B merita di sopravvivere — la porta che si costruisce,
la targa su due piani, il processo in sezione, la disciplina delle durate — può essere trapiantato in C senza portarsi dietro
il registro.
